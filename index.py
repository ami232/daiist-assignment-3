"""
Assignment 3: build the index (`main.py index`). May be index.ipynb instead.

Download the corpus (into corpus/, git-ignored), extract, clean and chunk it
with source and location metadata, embed with Gemini, and store everything in
index/. Save each vector as you get it and embed only chunks without one.

Write the per-file steps as functions (e.g. `chunk_file(path)`,
`embed_and_store(chunks)`): server.py's add-document tool imports them.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from pathlib import Path
from typing import Iterable

import chromadb
import httpx
from pypdf import PdfReader

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
EXTRA_DIR = ROOT / "corpus_extra"
INDEX_DIR = ROOT / "index"
QUERY_CACHE = INDEX_DIR / "query_cache.json"
CORPUS_DRUGS = ("amoxicillin", "lisinopril", "metformin", "atorvastatin", "levothyroxine")
DESIGNS = ("section", "fixed")


def _slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip("-") or "document"


def _extract_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    parts = []
    for number, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        parts.append(f"\n## Page {number}\n{text.strip()}\n")
    return "\n".join(parts)


def text_from_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _extract_pdf(path)
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="replace")
    raise ValueError(f"Unsupported document type: {path.suffix}")


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def openfda_to_text(record: dict) -> str:
    names = record.get("openfda", {}).get("brand_name") or record.get("openfda", {}).get("generic_name") or ["Drug"]
    name = str(names[0])
    out = [f"# {name}"]
    for key, values in record.items():
        if key == "openfda" or not isinstance(values, list):
            continue
        heading = key.replace("_", " ").title()
        if values:
            out.append(f"\n## {heading}\n" + "\n".join(str(v).strip() for v in values if str(v).strip()))
    return clean_text("\n".join(out))


def download_openfda(drug: str, limit: int = 10) -> list[Path]:
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    url = "https://api.fda.gov/drug/label.json"
    for skip in range(0, limit, 100):
        count = min(100, limit - skip)
        params = {"search": f'openfda.generic_name:"{drug}"', "limit": count, "skip": skip}
        try:
            response = httpx.get(url, params=params, timeout=60)
            response.raise_for_status()
            records = response.json().get("results", [])
        except (httpx.HTTPError, json.JSONDecodeError) as error:
            print(f"openFDA download failed for {drug}: {error}", file=sys.stderr)
            break
        for i, record in enumerate(records):
            set_id = record.get("id") or f"{drug}-{skip+i}"
            path = CORPUS_DIR / f"{_slug(drug)}-{_slug(set_id)}.txt"
            path.write_text(openfda_to_text(record), encoding="utf-8")
            saved.append(path)
        if len(records) < count:
            break
        time.sleep(0.1)
    return saved


def _words(text: str) -> list[str]:
    return re.findall(r"\S+", text)


def chunk_section(text: str, source: str, page: str | None = None) -> list[dict]:
    chunks: list[dict] = []
    heading = page or "Document"
    buffer: list[str] = []
    drug = source.rsplit(".", 1)[0].replace("-", " ").title()

    def flush():
        body = clean_text(" ".join(buffer))
        if body:
            numbered = f"[Drug: {drug} | Section: {heading}]\n{body}"
            chunks.append({
                "id": "",
                "text": numbered,
                "metadata": {"source": source, "location": heading, "design": "section"},
            })

    for line in text.splitlines():
        match = re.match(r"^##\s+(.+)$", line.strip())
        if match:
            flush()
            buffer = []
            heading = match.group(1).strip()
            continue
        if line.strip():
            buffer.append(line.strip())
            if len(_words(" ".join(buffer))) >= 220:
                flush()
                buffer = []
    flush()
    return chunks


def chunk_fixed(text: str, source: str) -> list[dict]:
    words = _words(clean_text(text))
    chunks: list[dict] = []
    for start in range(0, len(words), 120):
        window = words[start:start + 150]
        if not window:
            break
        body = " ".join(window)
        chunks.append({
            "id": "",
            "text": body,
            "metadata": {"source": source, "location": f"words {start + 1}-{start + len(window)}", "design": "fixed"},
        })
        if start + 150 >= len(words):
            break
    return chunks


def chunk_file(path: Path | str, design: str) -> list[dict]:
    path = Path(path).resolve()
    if design not in DESIGNS:
        raise ValueError(f"Unknown design: {design}")
    text = clean_text(text_from_file(path))
    source = path.name
    document_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    chunks = chunk_section(text, source) if design == "section" else chunk_fixed(text, source)
    for chunk in chunks:
        payload = json.dumps({"document_hash": document_hash, "text": chunk["text"], "design": design}, sort_keys=True)
        chunk["id"] = hashlib.sha256(payload.encode()).hexdigest()
        chunk["metadata"]["document_hash"] = document_hash
    return chunks


def get_collection(design: str):
    if design not in DESIGNS:
        raise ValueError(f"Unknown design: {design}")
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    return client.get_or_create_collection(name=design)


def embed_texts(texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed a batch with Gemini; callers persist vectors immediately after generation."""
    if not texts:
        return []
    load_api_key()
    from google import genai
    from google.genai import types

    client = genai.Client()
    vectors: list[list[float]] = []
    for text in texts:
        last_error = None
        for attempt in range(3):
            try:
                response = client.models.embed_content(
                    model="gemini-embedding-2",
                    contents=text,
                    config=types.EmbedContentConfig(task_type=task_type),
                )
                vectors.append(response.embeddings[0].values)
                break
            except Exception as error:
                last_error = error
                message = str(error)
                if "429" not in message and "RESOURCE_EXHAUSTED" not in message:
                    raise
                if attempt < 2:
                    time.sleep(65)
        else:
            raise RuntimeError(f"Embedding quota retry exhausted: {last_error}")
    return vectors


def embed_and_store(chunks: list[dict], design: str) -> dict:
    collection = get_collection(design)
    new_chunks = [c for c in chunks if collection.get(ids=[c["id"]], include=[])["ids"] == []]
    stored = 0
    for start in range(0, len(new_chunks), 10):
        batch = new_chunks[start:start + 10]
        try:
            vectors = embed_texts([c["text"] for c in batch], "RETRIEVAL_DOCUMENT")
        except Exception as error:
            print(f"Embedding stopped: {type(error).__name__}: {error}", file=sys.stderr)
            break
        collection.upsert(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
        )
        stored += len(batch)
        time.sleep(2)
    return {"stored": stored, "skipped": len(chunks) - len(new_chunks), "total": len(chunks)}


def add_file(path: Path | str, designs: Iterable[str] = DESIGNS) -> dict:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    if path.suffix.lower() not in {".txt", ".md", ".pdf"}:
        raise ValueError("Document must be .txt, .md, or .pdf")
    results = {}
    for design in designs:
        chunks = chunk_file(path, design)
        results[design] = embed_and_store(chunks, design)
    return results


def main() -> int:
    all_files = sorted(p for p in CORPUS_DIR.glob("*") if p.suffix.lower() in {".txt", ".md", ".pdf"})
    if not all_files:
        for drug in CORPUS_DRUGS:
            download_openfda(drug, limit=1)
        all_files = sorted(p for p in CORPUS_DIR.glob("*") if p.suffix.lower() in {".txt", ".md", ".pdf"})
    if not all_files:
        print("No corpus documents downloaded.", file=sys.stderr)
        return 1
    totals = {"section": 0, "fixed": 0}
    for path in all_files:
        result = add_file(path)
        for design, counts in result.items():
            totals[design] += counts["total"]
    print(f"Indexed {len(all_files)} documents for 2 designs.")
    print("Chunk counts:", totals)
    word_count = sum(len(_words(text_from_file(p))) for p in all_files)
    print(f"Corpus words: {word_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
