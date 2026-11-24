"""Build and query the Assignment 3 FAA Part 107 RAG index.

`uv run python main.py index` downloads the official FAA corpus into corpus/
(git-ignored), extracts page-aware text, builds two chunk-size designs, embeds
only chunks whose vectors are not already cached, and commits the searchable
artifacts to index/.

The per-file functions in this module are imported by server.py's add-document
tool, so the server reuses the exact same ingestion pipeline instead of
rewriting it.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from collections import Counter

import httpx
import numpy as np
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
from pypdf import PdfReader

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
SOURCES_PATH = ROOT / "corpus_sources.json"
CACHE_PATH = INDEX_DIR / "vector_cache.jsonl"
CHUNKS_PATH = INDEX_DIR / "chunks.jsonl"
MANIFEST_PATH = INDEX_DIR / "manifest.json"
SELECTED_DESIGN_PATH = INDEX_DIR / "selected_design.json"
ADDED_DOCS_PATH = INDEX_DIR / "added_documents.json"

EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "gemini-embedding-2")
EMBED_DIM = int(os.getenv("GEMINI_EMBED_DIM", "768"))

# One page-aware chunking scheme is embedded once. Retrieval evaluation then
# compares two search designs over the SAME saved vectors, which avoids paying
# the embedding quota twice.
CHUNK_DESIGN = "page_500"
CHUNKING = {"target_words": 500, "overlap_words": 80}
RETRIEVAL_DESIGNS = ("dense", "hybrid")
DEFAULT_DESIGN = "dense"

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".html", ".htm"}


@dataclass
class PageText:
    page: int
    text: str


@dataclass
class Chunk:
    chunk_id: str
    design: str
    doc_id: str
    source_title: str
    source_url: str
    source_date: str
    source_file: str
    location: str
    page: int
    text: str
    word_count: int
    document_sha256: str
    embedding: list[float] | None = None


def _ensure_dirs() -> None:
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _stable_chunk_id(doc_id: str, design: str, page: int, text: str) -> str:
    payload = f"{doc_id}\n{design}\n{page}\n{text}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def load_sources() -> list[dict[str, Any]]:
    if not SOURCES_PATH.exists():
        raise FileNotFoundError(f"Missing {SOURCES_PATH.name}")
    sources = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    if len(sources) < 3:
        raise ValueError("The assignment requires at least three corpus documents.")
    return sources


def download_source(source: dict[str, Any]) -> Path:
    """Download one configured corpus source if it is not already present."""
    _ensure_dirs()
    destination = CORPUS_DIR / source["filename"]
    if destination.exists() and destination.stat().st_size > 0:
        return destination

    tmp = destination.with_suffix(destination.suffix + ".part")
    headers = {"User-Agent": "DAIIST-Assignment-3 academic RAG project"}
    with httpx.Client(follow_redirects=True, timeout=120.0, headers=headers) as client:
        response = client.get(source["url"])
        response.raise_for_status()
        tmp.write_bytes(response.content)
    tmp.replace(destination)
    return destination


def clean_extracted_text(text: str) -> str:
    """Clean common PDF extraction noise while preserving readable text."""
    if not text:
        return ""
    text = text.replace("\u00ad", "")
    text = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", text)
    lines: list[str] = []
    for raw in text.splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if not line:
            lines.append("")
            continue
        # Standalone page numbers and repeated "This page intentionally..." add
        # retrieval noise but no useful compliance content.
        if re.fullmatch(r"(?:page\s+)?[ivxlcdm\d-]+", line, re.IGNORECASE):
            continue
        if line.lower() == "this page intentionally left blank.":
            continue
        lines.append(line)

    joined = "\n".join(lines)
    joined = re.sub(r"\n{3,}", "\n\n", joined)
    # Join single line wraps inside paragraphs, but retain blank-line paragraph breaks.
    paragraphs = []
    for paragraph in re.split(r"\n\s*\n", joined):
        paragraph = re.sub(r"\s*\n\s*", " ", paragraph).strip()
        paragraph = re.sub(r"\s+", " ", paragraph)
        if paragraph:
            paragraphs.append(paragraph)
    return "\n\n".join(paragraphs)


def extract_pdf(path: Path) -> list[PageText]:
    reader = PdfReader(str(path))
    pages: list[PageText] = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            raw = page.extract_text() or ""
        except Exception as exc:  # one malformed page should not kill the corpus
            print(f"WARNING: could not extract {path.name} PDF page {i}: {exc}", file=sys.stderr)
            raw = ""
        cleaned = clean_extracted_text(raw)
        if cleaned:
            pages.append(PageText(page=i, text=cleaned))
    return pages


def extract_text_file(path: Path) -> list[PageText]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    return [PageText(page=1, text=clean_extracted_text(raw))]


def extract_html(path: Path) -> list[PageText]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    return [PageText(page=1, text=clean_extracted_text(soup.get_text("\n")))]


def extract_file(path: Path) -> list[PageText]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf(path)
    if suffix in {".txt", ".md"}:
        return extract_text_file(path)
    if suffix in {".html", ".htm"}:
        return extract_html(path)
    raise ValueError(f"Unsupported document type {suffix!r}; supported: {sorted(SUPPORTED_EXTENSIONS)}")


def count_words(pages: Iterable[PageText]) -> int:
    return sum(len(page.text.split()) for page in pages)


def _windows(words: list[str], target: int, overlap: int) -> Iterable[list[str]]:
    if not words:
        return
    step = max(1, target - overlap)
    start = 0
    while start < len(words):
        end = min(len(words), start + target)
        window = words[start:end]
        if window:
            yield window
        if end == len(words):
            break
        start += step


def chunk_pages(
    pages: list[PageText],
    *,
    source: dict[str, Any],
    source_file: Path,
    document_sha256: str,
    design: str,
) -> list[Chunk]:
    """Create page-bounded chunks so every citation has an unambiguous page."""
    if design != CHUNK_DESIGN:
        raise ValueError(f"Unknown chunk design {design!r}")
    config = CHUNKING
    chunks: list[Chunk] = []
    for page in pages:
        words = page.text.split()
        for window in _windows(words, config["target_words"], config["overlap_words"]):
            text = " ".join(window).strip()
            if len(text.split()) < 40:
                continue
            cid = _stable_chunk_id(source["doc_id"], design, page.page, text)
            chunks.append(
                Chunk(
                    chunk_id=cid,
                    design=design,
                    doc_id=source["doc_id"],
                    source_title=source["title"],
                    source_url=source.get("url", ""),
                    source_date=source.get("date", ""),
                    source_file=source_file.name,
                    location=f"PDF page {page.page}" if source_file.suffix.lower() == ".pdf" else "document",
                    page=page.page,
                    text=text,
                    word_count=len(text.split()),
                    document_sha256=document_sha256,
                )
            )
    return chunks


def _load_vector_cache() -> dict[str, list[float]]:
    cache: dict[str, list[float]] = {}
    if not CACHE_PATH.exists():
        return cache
    with CACHE_PATH.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                cache[row["chunk_id"]] = row["embedding"]
            except (json.JSONDecodeError, KeyError, TypeError):
                print("WARNING: skipped a malformed vector-cache line", file=sys.stderr)
    return cache


def _normalize(vector: Iterable[float]) -> list[float]:
    arr = np.asarray(list(vector), dtype=np.float32)
    norm = float(np.linalg.norm(arr))
    if not math.isfinite(norm) or norm == 0:
        raise ValueError("Embedding had zero/invalid norm")
    return (arr / norm).tolist()


def _embedding_client() -> genai.Client:
    return genai.Client(api_key=load_api_key())


def embed_document_text(client: genai.Client, text: str) -> list[float]:
    # Embedding 2 no longer accepts task_type. Put the retrieval instruction in
    # the text itself, as Google's Embedding 2 guidance recommends.
    prompt = (
        "Represent this official FAA passage for retrieval by a commercial "
        "small-UAS compliance assistant. Preserve regulatory and operational meaning.\n\n"
        + text
    )
    result = client.models.embed_content(
        model=EMBED_MODEL,
        contents=prompt,
        config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
    )
    if not result.embeddings:
        raise RuntimeError("Gemini returned no embedding")
    return _normalize(result.embeddings[0].values)


def embed_query(client: genai.Client, query: str) -> list[float]:
    prompt = (
        "Represent this question for retrieval from an official FAA Part 107 / "
        "small-UAS compliance corpus.\n\nQuestion: " + query.strip()
    )
    result = client.models.embed_content(
        model=EMBED_MODEL,
        contents=prompt,
        config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
    )
    if not result.embeddings:
        raise RuntimeError("Gemini returned no query embedding")
    return _normalize(result.embeddings[0].values)


def _retry_wait_seconds(error: Exception, attempt: int) -> float:
    """Respect Gemini's retry hint when rate limited; otherwise back off."""
    message = str(error)
    match = re.search(r"retryDelay[^0-9]*(\d+(?:\.\d+)?)s", message, re.IGNORECASE)
    if match:
        return min(75.0, float(match.group(1)) + 2.0)
    if "429" in message or "RESOURCE_EXHAUSTED" in message:
        return min(60.0, 10.0 * (attempt + 1))
    return min(30.0, 2.0 ** attempt)


def _embed_with_retry(client: genai.Client, text: str, attempts: int = 8) -> list[float]:
    for attempt in range(attempts):
        try:
            return embed_document_text(client, text)
        except Exception as error:
            if attempt == attempts - 1:
                raise
            wait = _retry_wait_seconds(error, attempt)
            if "429" in str(error) or "RESOURCE_EXHAUSTED" in str(error):
                print(f"  Gemini rate limit reached; waiting {wait:.0f}s and retrying...")
            time.sleep(wait)
    raise AssertionError("unreachable")


def embed_and_store(chunks: list[Chunk]) -> list[Chunk]:
    """Embed only uncached chunks and append every new vector immediately."""
    _ensure_dirs()
    cache = _load_vector_cache()
    missing = [chunk for chunk in chunks if chunk.chunk_id not in cache]
    print(f"Embedding cache: {len(cache)} saved vectors; {len(missing)} new vectors needed.")

    client = _embedding_client() if missing else None
    if missing:
        with CACHE_PATH.open("a", encoding="utf-8") as cache_file:
            for i, chunk in enumerate(missing, start=1):
                embedding = _embed_with_retry(client, chunk.text)
                cache[chunk.chunk_id] = embedding
                cache_file.write(json.dumps({"chunk_id": chunk.chunk_id, "embedding": embedding}) + "\n")
                cache_file.flush()
                os.fsync(cache_file.fileno())
                if i == 1 or i % 25 == 0 or i == len(missing):
                    print(f"  embedded {i}/{len(missing)} new chunks")
                # Gemini's free embedding tier is token-rate limited per minute.
                # Pace requests so normal ~500-word chunks stay comfortably below it.
                time.sleep(1.7)

    for chunk in chunks:
        embedding = cache.get(chunk.chunk_id)
        if embedding is None:
            raise RuntimeError(f"No saved vector for chunk {chunk.chunk_id}")
        chunk.embedding = embedding
    return chunks


def _write_chunks(chunks: list[Chunk]) -> None:
    tmp = CHUNKS_PATH.with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(asdict(chunk), ensure_ascii=False) + "\n")
    tmp.replace(CHUNKS_PATH)


def _read_added_docs() -> list[dict[str, Any]]:
    if not ADDED_DOCS_PATH.exists():
        return []
    return json.loads(ADDED_DOCS_PATH.read_text(encoding="utf-8"))


def _write_added_docs(rows: list[dict[str, Any]]) -> None:
    ADDED_DOCS_PATH.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def build_index() -> None:
    _ensure_dirs()
    configured = load_sources()
    all_chunks: list[Chunk] = []
    corpus_rows: list[dict[str, Any]] = []

    print(f"Configured corpus: {len(configured)} official FAA documents")
    for source in configured:
        path = download_source(source)
        pages = extract_file(path)
        words = count_words(pages)
        sha = _sha256_file(path)
        corpus_rows.append({**source, "words": words, "pages_extracted": len(pages), "sha256": sha})
        print(f"  {source['doc_id']}: {words:,} words, {len(pages)} extracted pages")
        all_chunks.extend(
            chunk_pages(
                pages,
                source=source,
                source_file=path,
                document_sha256=sha,
                design=CHUNK_DESIGN,
            )
        )

    # Documents added later through the MCP tool are kept in index/ metadata.
    # If their original local file still exists, rebuilding can include them;
    # otherwise their already-committed chunks remain in chunks.jsonl until the
    # user deliberately removes them.
    previous_added_chunks: list[Chunk] = []
    if CHUNKS_PATH.exists():
        added_hashes = {row.get("sha256") for row in _read_added_docs()}
        for row in load_index_rows():
            if row.get("document_sha256") in added_hashes:
                previous_added_chunks.append(Chunk(**row))

    all_chunks = embed_and_store(all_chunks)
    # Preserve added-document chunks during a normal corpus rebuild.
    by_id = {c.chunk_id: c for c in [*all_chunks, *previous_added_chunks]}
    final_chunks = list(by_id.values())
    _write_chunks(final_chunks)

    total_words = sum(row["words"] for row in corpus_rows)
    chunk_count = sum(1 for c in final_chunks if c.design == CHUNK_DESIGN)
    manifest = {
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
        "embedding_model": EMBED_MODEL,
        "embedding_dimensions": EMBED_DIM,
        "total_word_count": total_words,
        "corpus": corpus_rows,
        "chunking": {"name": CHUNK_DESIGN, **CHUNKING, "chunks": chunk_count},
        "retrieval_designs": list(RETRIEVAL_DESIGNS),
        "default_design": DEFAULT_DESIGN,
        "added_documents": _read_added_docs(),
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    if not SELECTED_DESIGN_PATH.exists():
        SELECTED_DESIGN_PATH.write_text(
            json.dumps({"design": DEFAULT_DESIGN, "reason": "Default until retrieval evaluation is reviewed."}, indent=2),
            encoding="utf-8",
        )

    print(f"Total corpus words: {total_words:,}")
    if total_words < 50_000:
        raise RuntimeError("Corpus is below the assignment minimum of 50,000 words.")
    print(f"Saved {len(final_chunks):,} searchable chunks to {CHUNKS_PATH.relative_to(ROOT)}")
    print(f"Chunking: {CHUNK_DESIGN} -> {chunk_count:,} chunks")
    print(f"Retrieval designs available: {', '.join(RETRIEVAL_DESIGNS)}")


def load_index_rows() -> list[dict[str, Any]]:
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError("index/chunks.jsonl is missing. Run `uv run python main.py index` first.")
    rows: list[dict[str, Any]] = []
    with CHUNKS_PATH.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    if not rows:
        raise RuntimeError("The committed index is empty.")
    return rows


def selected_design() -> str:
    if SELECTED_DESIGN_PATH.exists():
        try:
            design = json.loads(SELECTED_DESIGN_PATH.read_text(encoding="utf-8"))["design"]
            if design in RETRIEVAL_DESIGNS:
                return design
        except Exception:
            pass
    return DEFAULT_DESIGN


def _candidate_rows(rows: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    rows = rows or load_index_rows()
    candidates = [row for row in rows if row.get("design") == CHUNK_DESIGN]
    if not candidates:
        raise RuntimeError(f"No chunks stored for chunking design {CHUNK_DESIGN!r}")
    return candidates


def search_with_vector(
    query_vector: list[float],
    *,
    k: int = 5,
    rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Dense cosine retrieval over the single saved chunk collection."""
    candidates = _candidate_rows(rows)
    q = np.asarray(query_vector, dtype=np.float32)
    scored: list[dict[str, Any]] = []
    for row in candidates:
        emb = np.asarray(row["embedding"], dtype=np.float32)
        score = float(np.dot(q, emb))
        scored.append({**row, "score": score, "dense_score": score})
    scored.sort(key=lambda row: row["score"], reverse=True)
    return scored[: max(1, int(k))]


_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _terms(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def _bm25_scores(query: str, rows: list[dict[str, Any]]) -> list[float]:
    """Small dependency-free BM25 implementation for the hybrid comparison."""
    query_terms = list(dict.fromkeys(_terms(query)))
    if not query_terms:
        return [0.0] * len(rows)
    docs = [_terms(row.get("text", "")) for row in rows]
    lengths = [len(doc) for doc in docs]
    avgdl = sum(lengths) / max(1, len(lengths))
    n_docs = len(docs)
    dfs = {term: sum(1 for doc in docs if term in set(doc)) for term in query_terms}
    k1, b = 1.5, 0.75
    scores: list[float] = []
    for doc, dl in zip(docs, lengths):
        counts = Counter(doc)
        score = 0.0
        for term in query_terms:
            df = dfs[term]
            idf = math.log(1.0 + (n_docs - df + 0.5) / (df + 0.5))
            tf = counts.get(term, 0)
            if tf:
                denom = tf + k1 * (1.0 - b + b * dl / max(avgdl, 1.0))
                score += idf * (tf * (k1 + 1.0)) / denom
        scores.append(score)
    return scores


def search_hybrid(
    query: str,
    query_vector: list[float],
    *,
    k: int = 5,
    rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Hybrid dense + BM25 retrieval using reciprocal-rank fusion."""
    candidates = _candidate_rows(rows)
    q = np.asarray(query_vector, dtype=np.float32)
    dense_scores = [float(np.dot(q, np.asarray(row["embedding"], dtype=np.float32))) for row in candidates]
    lexical_scores = _bm25_scores(query, candidates)

    dense_order = sorted(range(len(candidates)), key=lambda i: dense_scores[i], reverse=True)
    lexical_order = sorted(range(len(candidates)), key=lambda i: lexical_scores[i], reverse=True)
    dense_rank = {idx: rank for rank, idx in enumerate(dense_order, start=1)}
    lexical_rank = {idx: rank for rank, idx in enumerate(lexical_order, start=1)}

    fused: list[dict[str, Any]] = []
    for i, row in enumerate(candidates):
        # RRF avoids arbitrary score scaling between cosine similarity and BM25.
        score = 1.0 / (60 + dense_rank[i]) + 1.0 / (60 + lexical_rank[i])
        fused.append({
            **row,
            "score": score,
            "dense_score": dense_scores[i],
            "lexical_score": lexical_scores[i],
        })
    fused.sort(key=lambda row: row["score"], reverse=True)
    return fused[: max(1, int(k))]


def search_with_method(
    query: str,
    query_vector: list[float],
    *,
    k: int = 5,
    design: str | None = None,
    rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    design = design or selected_design()
    if design == "dense":
        return search_with_vector(query_vector, k=k, rows=rows)
    if design == "hybrid":
        return search_hybrid(query, query_vector, k=k, rows=rows)
    raise ValueError(f"Unknown retrieval design {design!r}; choose from {RETRIEVAL_DESIGNS}")


def search_index(query: str, *, k: int = 5, design: str | None = None) -> list[dict[str, Any]]:
    client = _embedding_client()
    vector = embed_query(client, query)
    return search_with_method(query, vector, k=k, design=design)


def format_search_results(results: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for i, row in enumerate(results, start=1):
        citation = f"[FAA:{row['doc_id']}|{row['location']}]"
        blocks.append(
            f"{citation}\n"
            f"Rank: {i} | similarity: {row['score']:.4f}\n"
            f"Source: {row['source_title']}\n"
            f"Source date: {row.get('source_date', '')}\n"
            f"Location: {row['location']}\n"
            f"URL: {row.get('source_url', '')}\n"
            f"Passage: {row['text']}"
        )
    return "\n\n---\n\n".join(blocks)


def index_local_document(path: str | Path) -> dict[str, Any]:
    """Index a user-approved local file using the same pipeline as the corpus."""
    _ensure_dirs()
    source_path = Path(path).expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(f"Document does not exist: {source_path}")
    if source_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported document type: {source_path.suffix}")

    sha = _sha256_file(source_path)
    added = _read_added_docs()
    duplicate = next((row for row in added if row.get("sha256") == sha), None)
    if duplicate:
        return {"status": "already_indexed", "document": duplicate}

    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", source_path.name)
    stored = CORPUS_DIR / "added" / safe_name
    stored.parent.mkdir(parents=True, exist_ok=True)
    if source_path != stored:
        shutil.copy2(source_path, stored)

    pages = extract_file(stored)
    words = count_words(pages)
    doc_id = "added-" + sha[:12]
    source = {
        "doc_id": doc_id,
        "title": source_path.stem.replace("_", " "),
        "url": "",
        "date": "",
    }
    new_chunks: list[Chunk] = []
    new_chunks.extend(
        chunk_pages(
            pages,
            source=source,
            source_file=stored,
            document_sha256=sha,
            design=CHUNK_DESIGN,
        )
    )
    new_chunks = embed_and_store(new_chunks)

    existing = load_index_rows() if CHUNKS_PATH.exists() else []
    merged = {row["chunk_id"]: row for row in existing}
    for chunk in new_chunks:
        merged[chunk.chunk_id] = asdict(chunk)
    tmp_chunks = [Chunk(**row) for row in merged.values()]
    _write_chunks(tmp_chunks)

    record = {
        "doc_id": doc_id,
        "title": source["title"],
        "original_path": str(source_path),
        "stored_file": str(stored.relative_to(ROOT)),
        "sha256": sha,
        "words": words,
        "chunks": len(new_chunks),
        "added_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    added.append(record)
    _write_added_docs(added)
    return {"status": "indexed", "document": record}


def main() -> None:
    build_index()


if __name__ == "__main__":
    main()
