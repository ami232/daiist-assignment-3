"""
Assignment 3: build the index (`main.py index`).

    uv run python index.py              # count, ask for approval, embed what's missing, store
    uv run python index.py --dry-run    # count only; never calls Gemini
    uv run python index.py --yes        # skip the approval prompt (or set INDEX_YES=1)

Pipeline per file: download -> extract pages (pypdf) -> clean -> chunk -> embed -> store.
Every embedding is appended to index/embeddings.jsonl the moment it returns, keyed by
sha256(model | text sent), so a re-run or a crash costs no quota. ChromaDB in index/chroma
is rebuilt from that cache. Query embeddings use the same cache (embed_query).

server.py imports chunk_file, embed_and_store, embed_query and get_collection from here.
Library functions log to stderr only: stdout carries the MCP protocol.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import os
import re
import sys
import time
import unicodedata
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CACHE_FILE = INDEX_DIR / "embeddings.jsonl"
CHROMA_DIR = INDEX_DIR / "chroma"

EMBED_MODEL = "gemini-embedding-2"
BATCH_SIZE = 20
DAILY_QUOTA = 1000  # SETUP.md: about 1,000 embedded texts per day

# Chunking designs. Design B (structure-based) is added later.
DESIGNS = {
    "A250": {"size": 250, "overlap": 50},
    "A150": {"size": 150, "overlap": 30},
}
DEFAULT_DESIGN = "A250"


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- documents

CSF_ID = r"\b(?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2}(?:-\d{2})?\b"


@dataclass
class DocSpec:
    doc_id: str
    folder: str                      # "raw" (indexed) or "holdout" (added later via add_document)
    url: str
    sha256: str
    title: str
    version: str
    date: str
    framework: str
    drop: dict[int, str]             # 1-based PDF page -> reason
    body_start: int                  # PDF page printed as "1"
    roman_start: int | None = None   # PDF page printed as "i"
    dehyphenate: bool = False        # typeset hyphenation at line ends (AI 100-1 only)
    id_pattern: str = ""             # identifiers to record per chunk
    strip_patterns: list[str] = field(default_factory=list)  # personal-data passages to cut
    sections: list[tuple[str, str]] = field(default_factory=list)  # (number, title) in reading order, from the TOC

    @property
    def path(self) -> Path:
        return CORPUS / self.folder / f"{self.doc_id}.pdf"


DOCS: dict[str, DocSpec] = {d.doc_id: d for d in [
    DocSpec(
        "NIST.AI.100-1", "raw", "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
        "7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1",
        "NIST AI 100-1: AI Risk Management Framework (AI RMF 1.0)", "1.0", "2023-01", "AI RMF",
        drop={1: "cover", 2: "title page", 4: "table of contents", 5: "lists of figures/tables", 48: "back cover"},
        body_start=6, roman_start=3, dehyphenate=True,
        id_pattern=r"\b(?:GOVERN|MAP|MEASURE|MANAGE) \d+(?:\.\d+)?(?=:)",
        sections=[("", "Executive Summary"), ("Part 1", "Foundational Information"), ("1", "Framing Risk"),
                  ("1.1", "Understanding and Addressing Risks, Impacts, and Harms"),
                  ("1.2", "Challenges for AI Risk Management"), ("1.2.1", "Risk Measurement"),
                  ("1.2.2", "Risk Tolerance"), ("1.2.3", "Risk Prioritization"),
                  ("1.2.4", "Organizational Integration and Management of Risk"), ("2", "Audience"),
                  ("3", "AI Risks and Trustworthiness"), ("3.1", "Valid and Reliable"), ("3.2", "Safe"),
                  ("3.3", "Secure and Resilient"), ("3.4", "Accountable and Transparent"),
                  ("3.5", "Explainable and Interpretable"), ("3.6", "Privacy-Enhanced"),
                  ("3.7", "Fair – with Harmful Bias Managed"), ("4", "Effectiveness of the AI RMF"),
                  ("Part 2", "Core and Profiles"), ("5", "AI RMF Core"), ("5.1", "Govern"), ("5.2", "Map"),
                  ("5.3", "Measure"), ("5.4", "Manage"), ("6", "AI RMF Profiles"),
                  ("Appendix A", "Descriptions of AI Actor Tasks from Figures 2 and 3"),
                  ("Appendix B", "How AI Risks Differ from Traditional Software Risks"),
                  ("Appendix C", "AI Risk Management and Human-AI Interaction"),
                  ("Appendix D", "Attributes of the AI RMF")],
    ),
    DocSpec(
        "NIST.AI.600-1", "raw", "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf",
        "6e73620ab6b64e90ef2c04bf0e0d6246185a2f4b1b13cab0df494496cff89b6a",
        "NIST AI 600-1: AI RMF Generative Artificial Intelligence Profile", "July 2024", "2024-07", "GAI Profile",
        drop={1: "cover", 2: "title page", 3: "about + acknowledgments", 4: "table of contents",
              **{p: "references" for p in range(58, 65)}},
        body_start=5,
        id_pattern=r"\b(?:GV|MP|MS|MG)-\d+\.\d+-\d{3}\b|\b(?:GOVERN|MAP|MEASURE|MANAGE) \d+\.\d+(?=:)",
        strip_patterns=[r"Acknowledgments:.*?(?=A\.1\. Governance)"],
        sections=[("1", "Introduction"), ("2", "Overview of Risks Unique to or Exacerbated by GAI"),
                  ("2.1", "CBRN Information or Capabilities"), ("2.2", "Confabulation"),
                  ("2.3", "Dangerous, Violent, or Hateful Content"), ("2.4", "Data Privacy"),
                  ("2.5", "Environmental Impacts"), ("2.6", "Harmful Bias and Homogenization"),
                  ("2.7", "Human-AI Configuration"), ("2.8", "Information Integrity"),
                  ("2.9", "Information Security"), ("2.10", "Intellectual Property"),
                  ("2.11", "Obscene, Degrading, and/or Abusive Content"),
                  ("2.12", "Value Chain and Component Integration"), ("3", "Suggested Actions to Manage GAI Risks"),
                  ("Appendix A", "Primary GAI Considerations"), ("A.1", "Governance"), ("A.1.1", "Overview"),
                  ("A.1.2", "Organizational Governance"), ("A.1.3", "Third-Party Considerations"),
                  ("A.1.4", "Pre-Deployment Testing"), ("A.1.5", "Structured Public Feedback"),
                  ("A.1.6", "Content Provenance"),
                  ("A.1.7", "Enhancing Content Provenance through Structured Public Feedback"),
                  ("A.1.8", "Incident Disclosure")],
    ),
    DocSpec(
        "NIST.SP.800-61r3", "raw", "https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-61r3.pdf",
        "e5593d6bb85daecec7e8d9549400c7b3473bcc3f06e469c82218073afa7fba2d",
        "NIST SP 800-61r3: Incident Response Recommendations and Considerations (CSF 2.0 Community Profile)",
        "Revision 3", "2025-04", "CSF IR Profile",
        drop={1: "cover", 2: "title page", 3: "legal notices", 4: "author ORCID iDs", 7: "patent notice",
              8: "table of contents", 44: "references", 45: "references"},
        body_start=9, roman_start=5, id_pattern=CSF_ID,
        sections=[("", "Executive Summary"), ("1", "Introduction"), ("1.1", "Purpose and Scope"),
                  ("1.2", "Document Structure"), ("2", "Incident Response as Part of Cybersecurity Risk Management"),
                  ("2.1", "Incident Response Life Cycle Model"), ("2.2", "Incident Response Roles and Responsibilities"),
                  ("2.3", "Incident Response Policies, Processes, and Procedures"),
                  ("3", "CSF 2.0 Community Profile for Cyber Incident Risk Management"),
                  ("3.1", "Preparation and Lessons Learned"), ("3.2", "Incident Response"),
                  ("Appendix A", "List of Symbols, Abbreviations, and Acronyms"), ("Appendix B", "Glossary"),
                  ("Appendix C", "Change Log")],
    ),
    DocSpec(
        "NIST.SP.800-218", "raw", "https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-218.pdf",
        "617746e553a9e2da49bfbd4eef0dfc3094758a39b869314e4173ac36605cde22",
        "NIST SP 800-218: Secure Software Development Framework (SSDF) Version 1.1", "1.1", "2022-02", "SSDF",
        drop={1: "cover", 2: "title page", 3: "legal notices", 7: "patent notice", 9: "table of contents",
              **{p: "references" for p in range(29, 33)}},
        body_start=10, roman_start=3,
        id_pattern=r"\b(?:PO|PS|PW|RV)\.\d+(?:\.\d+)?\b",
        strip_patterns=[r"Acknowledgments\s*\nThe authors thank.*?(?=Audience\s*\n)"],
        sections=[("", "Executive Summary"), ("1", "Introduction"),
                  ("2", "The Secure Software Development Framework"), ("", "The SSDF and Executive Order 14028"),
                  ("", "Acronyms"), ("", "Change Log")],
    ),
    DocSpec(
        "NIST.CSWP.29", "holdout", "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
        "3c31f46fee98cac0c4323453e5109291a213b4de7fef8c058af9bf67f717433c",
        "NIST CSWP 29: The NIST Cybersecurity Framework (CSF) 2.0", "2.0", "2024-02-26", "CSF 2.0",
        drop={1: "cover", 3: "acknowledgments", 4: "table of contents", 32: "colophon"},
        body_start=6, roman_start=2, id_pattern=CSF_ID,
        sections=[("", "Preface"), ("1", "Cybersecurity Framework (CSF) Overview"), ("2", "Introduction to the CSF Core"),
                  ("3", "Introduction to CSF Profiles and Tiers"), ("3.1", "CSF Profiles"), ("3.2", "CSF Tiers"),
                  ("4", "Introduction to Online Resources That Supplement the CSF"),
                  ("5", "Improving Cybersecurity Risk Communication and Integration"),
                  ("5.1", "Improving Risk Management Communication"),
                  ("5.2", "Improving Integration with Other Risk Management Programs"),
                  ("Appendix A", "CSF Core"), ("Appendix B", "CSF Tiers"), ("Appendix C", "Glossary")],
    ),
]}
INDEXED = [d for d in DOCS.values() if d.folder == "raw"]

# Running headers, footers and bare page numbers, removed line by line.
HEADER_LINES = [re.compile(p) for p in [
    r"^NIST AI 100-1\s+AI RMF 1\.0$",
    r"^NIST SP 800-61r3\s+Incident Response Recommendations and$",
    r"^April 2025\s+Considerations for Cyber Risk Management$",
    r"^NIST CSWP 29\s+The NIST Cybersecurity Framework \(CSF\) 2\.0$",
    r"^February 26, 2024$",
    r"^NIST SP 800-218\s+SSDF VERSION 1\.1$",
    r"^This publication is available free of charge from: https://doi\.org/10\.6028/NIST\.SP\.800-218$",
    r"^(?:[0-9]{1,3}|[ivx]{1,4})$",
]]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def download_corpus(docs: list[DocSpec] | None = None) -> None:
    """Fetch each PDF if missing and check it against the checksum the cleaning rules were written for."""
    for doc in docs or list(DOCS.values()):
        doc.path.parent.mkdir(parents=True, exist_ok=True)
        if not doc.path.exists():
            log(f"Downloading {doc.doc_id} ...")
            req = urllib.request.Request(doc.url, headers={"User-Agent": "Mozilla/5.0 (corpus-indexer)"})
            with urllib.request.urlopen(req, timeout=120) as r:
                doc.path.write_bytes(r.read())
        actual = sha256_file(doc.path)
        if actual != doc.sha256:
            raise SystemExit(
                f"{doc.path} does not match the expected checksum.\n  expected {doc.sha256}\n  got      {actual}\n"
                "NIST may have republished it; the page-drop rules would no longer line up. Check before indexing."
            )


def spec_for(path: Path) -> DocSpec | None:
    """The registered document with this file's content, if any (matched by hash, not by name)."""
    digest = sha256_file(path)
    return next((d for d in DOCS.values() if d.sha256 == digest), None)


# --------------------------------------------------------------------------- extract and clean

def to_roman(n: int) -> str:
    vals = [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, s in vals:
        while n >= v:
            out, n = out + s, n - v
    return out


def page_label(spec: DocSpec | None, pdf_page: int) -> str:
    if spec is None:
        return str(pdf_page)
    if pdf_page >= spec.body_start:
        return str(pdf_page - spec.body_start + 1)
    if spec.roman_start and pdf_page >= spec.roman_start:
        return to_roman(pdf_page - spec.roman_start + 1)
    return f"pdf{pdf_page}"


def clean_text(text: str, spec: DocSpec | None) -> str:
    text = unicodedata.normalize("NFKC", text)  # ligatures (ﬁ, ﬀ) and odd spaces
    for pattern in (spec.strip_patterns if spec else []):
        text = re.sub(pattern, "", text, flags=re.S)
    lines = [l.rstrip() for l in text.splitlines()]
    lines = [l for l in lines if not any(h.match(l.strip()) for h in HEADER_LINES)]
    text = "\n".join(lines)
    if spec and spec.dehyphenate:
        text = re.sub(r"([a-z])-\n([a-z])", r"\1\2", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_pages(path: Path, spec: DocSpec | None) -> list[dict]:
    """[{page, label, text}] for every kept page, cleaned."""
    from pypdf import PdfReader
    import logging
    logging.getLogger("pypdf").setLevel(logging.ERROR)

    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages, 1):
        if spec and i in spec.drop:
            continue
        text = clean_text(page.extract_text() or "", spec)
        if text:
            pages.append({"page": i, "label": page_label(spec, i), "text": text})
    return pages


# --------------------------------------------------------------------------- chunk

def locate_sections(words: list[str], spec: DocSpec | None) -> list[tuple[int, str]]:
    """Word position of each known heading, searched in order so a later heading is never found
    before an earlier one. The number may be printed as "2", "2." or "2:". Unfound headings are logged."""
    found, start = [], 0
    for number, title in (spec.sections if spec else []):
        title_tokens = title.split()
        prefixes = [[]]
        if number:
            *head, last = number.split()
            prefixes = [head + [last + end] for end in ("", ".", ":")]
        hit = None
        for i in range(start, len(words)):
            for pre in prefixes:
                cand = pre + title_tokens
                if words[i:i + len(cand)] == cand:
                    hit = i
                    break
            if hit is not None:
                break
        if hit is None:
            log(f"  [{spec.doc_id}] heading not found: {number} {title}")
            continue
        found.append((hit, f"{number} {title}".strip()))
        start = hit + 1
    return found


@dataclass
class Chunk:
    chunk_id: str
    text: str
    meta: dict


def chunk_pages(pages: list[dict], spec: DocSpec | None, doc_id: str, doc_hash: str,
                design: str = DEFAULT_DESIGN, title: str | None = None) -> list[Chunk]:
    """Design A: fixed word windows with overlap, within one document, recording pages and section."""
    size, overlap = DESIGNS[design]["size"], DESIGNS[design]["overlap"]
    words, word_page, word_label = [], [], []
    for pg in pages:
        for w in pg["text"].split():
            words.append(w)
            word_page.append(pg["page"])
            word_label.append(pg["label"])
    headings = locate_sections(words, spec)

    id_re = re.compile(spec.id_pattern) if spec and spec.id_pattern else None
    chunks, step = [], size - overlap
    n = 1 if len(words) <= size else 1 + math.ceil((len(words) - size) / step)
    for i in range(n):
        lo, hi = i * step, min(i * step + size, len(words))
        text = " ".join(words[lo:hi])
        sec = next((h for pos, h in reversed(headings) if pos <= lo), "")
        ids = list(dict.fromkeys(id_re.findall(text))) if id_re else []
        first = ids[0] if ids else ""
        function = re.split(r"[ .\-]", first)[0] if first else ""
        meta = {
            "doc_id": doc_id,
            "doc_title": title or (spec.title if spec else doc_id),
            "doc_version": spec.version if spec else "",
            "doc_date": spec.date if spec else "",
            "framework": spec.framework if spec else "",
            "page_start": word_page[lo],
            "page_end": word_page[hi - 1],
            "page_label": word_label[lo] if word_label[lo] == word_label[hi - 1]
                          else f"{word_label[lo]}-{word_label[hi - 1]}",
            "section": sec,
            "identifiers": ";".join(ids),
            "function": function,
            "design": design,
            "word_count": hi - lo,
            "content_hash": hashlib.sha256(text.encode()).hexdigest(),
            "doc_hash": doc_hash,
        }
        chunks.append(Chunk(f"{doc_id}:{design}:{i:04d}", text, meta))
    return chunks


def chunk_file(path: str | Path, design: str = DEFAULT_DESIGN) -> list[Chunk]:
    """Extract, clean and chunk one PDF. Registered NIST documents get their own cleaning rules
    (recognised by content hash); any other PDF gets the generic cleaning only."""
    path = Path(path).resolve()
    spec = spec_for(path)
    doc_hash = sha256_file(path)
    title = None
    if spec is None:
        from pypdf import PdfReader
        meta = PdfReader(str(path)).metadata or {}
        title = str(meta.get("/Title") or path.stem)
    doc_id = spec.doc_id if spec else path.stem
    pages = extract_pages(path, spec)
    return chunk_pages(pages, spec, doc_id, doc_hash, design, title)


# --------------------------------------------------------------------------- embed (cached)

_cache: dict[str, np.ndarray] | None = None


def _load_cache() -> dict[str, np.ndarray]:
    global _cache
    if _cache is None:
        _cache = {}
        if CACHE_FILE.exists():
            for line in CACHE_FILE.read_text().splitlines():
                if line.strip():
                    row = json.loads(line)
                    _cache[row["key"]] = np.frombuffer(base64.b64decode(row["vec"]), dtype=np.float32)
    return _cache


def _embed_input(text: str, kind: str, title: str = "") -> str:
    """The exact string sent. gemini-embedding-2 takes the task as a text prefix, not task_type."""
    if kind == "query":
        return f"task: search result | query: {text}"
    return f"title: {title or 'none'} | text: {text}"


def _key(sent: str) -> str:
    return hashlib.sha256(f"{EMBED_MODEL}|{sent}".encode()).hexdigest()


def missing(texts: list[str]) -> list[str]:
    cache = _load_cache()
    return [t for t in dict.fromkeys(texts) if _key(t) not in cache]


def _client():
    from google import genai
    from api_key import load_api_key
    return genai.Client(api_key=load_api_key())


def embed_texts(sent_texts: list[str]) -> list[np.ndarray]:
    """Vectors for these exact strings: from the cache, else from Gemini, appended to the cache per batch.
    Callers are responsible for the approval step before calling this with uncached texts."""
    from google.genai import errors, types

    cache = _load_cache()
    todo = missing(sent_texts)
    if todo:
        client = _client()
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        done = 0
        for b in range(0, len(todo), BATCH_SIZE):
            batch = todo[b:b + BATCH_SIZE]
            # One Content per text: a plain list of strings is merged into ONE content by the SDK
            # for gemini-embedding-2, which would return a single blended vector for the batch.
            contents = [types.Content(parts=[types.Part(text=t)]) for t in batch]
            for attempt in range(6):
                try:
                    resp = client.models.embed_content(model=EMBED_MODEL, contents=contents)
                    break
                except errors.APIError as e:
                    msg = str(e)
                    if e.code == 429 and "PerDay" not in msg and attempt < 5:
                        wait = 2 ** attempt * 10
                        log(f"  rate limited, waiting {wait}s ...")
                        time.sleep(wait)
                        continue
                    raise SystemExit(f"Gemini stopped the run after {done} new embeddings (all saved): {msg[:300]}")
            if len(resp.embeddings) != len(batch):
                raise SystemExit(f"Asked for {len(batch)} embeddings, got {len(resp.embeddings)}; nothing from this batch saved.")
            with CACHE_FILE.open("a") as f:
                for t, e in zip(batch, resp.embeddings):
                    vec = np.asarray(e.values, dtype=np.float32)
                    cache[_key(t)] = vec
                    f.write(json.dumps({"key": _key(t), "model": EMBED_MODEL, "dim": len(vec),
                                        "vec": base64.b64encode(vec.tobytes()).decode()}) + "\n")
                f.flush()
                os.fsync(f.fileno())
            done += len(batch)
            log(f"  embedded {done}/{len(todo)}")
    return [cache[_key(t)] for t in sent_texts]


def embed_query(query: str) -> np.ndarray:
    """Query vector, cached by text so the same question never costs quota twice."""
    return embed_texts([_embed_input(query, "query")])[0]


# --------------------------------------------------------------------------- store

def get_collection(design: str = DEFAULT_DESIGN, fresh: bool = False):
    """Open the store. Retries briefly: two processes opening ChromaDB at the same moment can fail
    with "Could not connect to tenant" (seen when the evaluation and another script overlapped).
    fresh=True drops ChromaDB's per-process client cache first. Needed after another process (the
    MCP server's add_document) changed the collection: the cached client is stale and fails with
    "Error finding id"."""
    import chromadb
    if fresh:
        from chromadb.api.client import SharedSystemClient
        SharedSystemClient.clear_system_cache()
    for attempt in range(5):
        try:
            client = chromadb.PersistentClient(path=str(CHROMA_DIR))
            return client.get_or_create_collection(f"chunks_{design}", metadata={"hnsw:space": "cosine"},
                                                   embedding_function=None)
        except (ValueError, AttributeError, KeyError) as e:
            if attempt == 4:
                raise
            log(f"  ChromaDB not ready ({type(e).__name__}); retrying ...")
            time.sleep(1 + attempt)


def doc_sent_texts(chunks: list[Chunk]) -> list[str]:
    return [_embed_input(c.text, "document", c.meta["doc_title"]) for c in chunks]


def embed_and_store(chunks: list[Chunk], design: str = DEFAULT_DESIGN) -> int:
    """Embed (cache first) and upsert into ChromaDB. Returns how many chunks were stored."""
    if not chunks:
        return 0
    vectors = embed_texts(doc_sent_texts(chunks))
    col = get_collection(design)
    for b in range(0, len(chunks), 500):
        part = chunks[b:b + 500]
        col.upsert(ids=[c.chunk_id for c in part], documents=[c.text for c in part],
                   metadatas=[c.meta for c in part], embeddings=[v.tolist() for v in vectors[b:b + 500]])
    return len(chunks)


def is_indexed(doc_hash: str, design: str = DEFAULT_DESIGN) -> bool:
    return bool(get_collection(design).get(where={"doc_hash": doc_hash}, limit=1)["ids"])


# --------------------------------------------------------------------------- main

def approve(n_new: int, assume_yes: bool) -> bool:
    if n_new == 0 or assume_yes:
        return True
    if not sys.stdin.isatty():
        log("Not a terminal, so no one can approve. Re-run with --yes (or INDEX_YES=1) to embed.")
        return False
    return input(f"Embed {n_new} new texts with Gemini ({EMBED_MODEL})? [y/N] ").strip().lower() == "y"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the index.")
    parser.add_argument("--design", default=DEFAULT_DESIGN, choices=DESIGNS)
    parser.add_argument("--dry-run", action="store_true", help="count chunks and missing vectors; never call Gemini")
    parser.add_argument("--yes", action="store_true", help="embed without asking")
    args = parser.parse_args()
    assume_yes = args.yes or os.environ.get("INDEX_YES") == "1"

    download_corpus()
    all_chunks: list[Chunk] = []
    print(f"Design {args.design}: {DESIGNS[args.design]}")
    print(f"{'document':<20}{'pages kept':>11}{'words':>8}{'chunks':>8}")
    for doc in INDEXED:
        chunks = chunk_file(doc.path, args.design)
        pages = extract_pages(doc.path, doc)
        words = sum(len(p["text"].split()) for p in pages)
        print(f"{doc.doc_id:<20}{len(pages):>11}{words:>8}{len(chunks):>8}")
        all_chunks += chunks

    new = missing(doc_sent_texts(all_chunks))
    tokens = sum(len(t.split()) for t in new) * 4 // 3
    print(f"\nTotal chunks: {len(all_chunks)}  |  already embedded: {len(all_chunks) - len(new)}  |  "
          f"to embed now: {len(new)} (~{tokens:,} tokens, {len(new) / DAILY_QUOTA:.0%} of the ~{DAILY_QUOTA}/day quota)")

    if args.dry_run:
        print("Dry run: no Gemini call made.")
        return
    if not approve(len(new), assume_yes):
        print("Stopped before any Gemini call.")
        sys.exit(1 if new else 0)

    embed_and_store(all_chunks, args.design)
    # Drop chunks of indexed documents that no longer exist (re-chunked); documents added later stay.
    col = get_collection(args.design)
    current = {c.chunk_id for c in all_chunks}
    for doc in INDEXED:
        stale = [i for i in col.get(where={"doc_id": doc.doc_id}, include=[])["ids"] if i not in current]
        if stale:
            col.delete(ids=stale)
    print(f"Stored {col.count()} chunks in {CHROMA_DIR.relative_to(ROOT)} (collection chunks_{args.design}).")


if __name__ == "__main__":
    main()
