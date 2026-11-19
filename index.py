"""
Assignment 3: build the index (`main.py index`).

Corpus: official FDA prescription-drug labels (openFDA, public domain).
Pipeline, one function per step so server.py can reuse it:

    download_corpus()          -> corpus/<drug>.json (skipped if already there)
    load_document(path)        -> list of (section_key, section_title, clean text)
    chunk_file(path, design)   -> list of chunks with source + section metadata
    embed_and_store(chunks, design) -> embeds only chunks without a saved vector
    add_file(path)             -> what add_document in server.py runs

Two chunking designs are built, so evaluate.py can compare them:
    "fixed"     : 220-word windows over the whole label, ignoring sections
    "structure" : split at label sections first, then pack sentences up to 220 words
"""

import hashlib
import json
import math
import re
import sys
import time
from pathlib import Path

import chromadb
import httpx
from bs4 import BeautifulSoup
from chromadb.config import Settings
from google import genai
from google.genai import types

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
REGISTRY = INDEX_DIR / "documents.json"   # which files are indexed, with their hash

EMBED_MODEL = "gemini-embedding-001"
EMBED_DIM = 768                 # smaller vectors keep index/ well under 90 MB
CHUNK_WORDS = 220
FIXED_OVERLAP = 30
BATCH = 20                      # texts per embedding request
DESIGNS = ["fixed", "structure"]
CHOSEN_DESIGN = "structure"     # chosen from eval/retrieval_results.csv (see REPORT.md)

OPENFDA = "https://api.fda.gov/drug/label.json"

# The corpus. Each label is pinned by its set_id (found with the search the first
# time, on 18 Nov 2026), so the same labels are downloaded every time.
DOCUMENTS = [
    # `.exact` matches the whole generic name, so combination products
    # (e.g. sitagliptin + metformin) are not picked up by mistake.
    {"source": "metformin", "set_id": "ec43efb2-8a50-4bac-9576-f4303841a497",
     "search": 'openfda.generic_name.exact:"METFORMIN HYDROCHLORIDE"'},
    {"source": "warfarin", "set_id": "61ab23a7-bc67-4777-854a-bf43c788a69a",
     "search": 'openfda.generic_name.exact:"WARFARIN SODIUM"'},
    {"source": "atorvastatin", "set_id": "8cc6240a-58d3-4bca-aa1e-662228957f75",
     "search": 'openfda.generic_name.exact:"ATORVASTATIN CALCIUM"'},
    {"source": "lisinopril", "set_id": "dd015c18-1ea6-44e3-9186-8d2f8444d874",
     "search": 'openfda.generic_name.exact:"LISINOPRIL"'},
    {"source": "sertraline", "set_id": "687ebdc4-6946-454e-8d46-3207488ccf32",
     "search": 'openfda.generic_name.exact:"SERTRALINE HYDROCHLORIDE"'},
    {"source": "amoxicillin", "set_id": "987786a1-d748-4b42-abb5-62a2f38ef195",
     "search": 'openfda.generic_name.exact:"AMOXICILLIN"'},
]

# Not part of the corpus: used to show add_document (README step 8). Saved in
# docs_to_add/ and indexed only when someone runs add_document on it.
EXTRA_DOCUMENTS = [
    {"source": "apixaban", "search": 'openfda.generic_name.exact:"APIXABAN"'},
]
EXTRA_DIR = ROOT / "docs_to_add"

# Label sections we keep, in label order, with a readable title.
# Fields ending in _table (HTML copies), package labels and product data lists are left out.
SECTIONS = {
    "boxed_warning": "Boxed Warning",
    "indications_and_usage": "Indications and Usage",
    "dosage_and_administration": "Dosage and Administration",
    "dosage_forms_and_strengths": "Dosage Forms and Strengths",
    "contraindications": "Contraindications",
    "warnings_and_cautions": "Warnings and Precautions",
    "warnings": "Warnings",
    "precautions": "Precautions",
    "adverse_reactions": "Adverse Reactions",
    "drug_interactions": "Drug Interactions",
    "general_precautions": "General Precautions",
    "laboratory_tests": "Laboratory Tests",
    "use_in_specific_populations": "Use in Specific Populations",
    "pregnancy": "Pregnancy",
    "nursing_mothers": "Nursing Mothers",
    "pediatric_use": "Pediatric Use",
    "geriatric_use": "Geriatric Use",
    "drug_abuse_and_dependence": "Drug Abuse and Dependence",
    "overdosage": "Overdosage",
    "description": "Description",
    "clinical_pharmacology": "Clinical Pharmacology",
    "mechanism_of_action": "Mechanism of Action",
    "pharmacokinetics": "Pharmacokinetics",
    "nonclinical_toxicology": "Nonclinical Toxicology",
    "clinical_studies": "Clinical Studies",
    "how_supplied": "How Supplied",
    "storage_and_handling": "Storage and Handling",
    "patient_counseling_information": "Patient Counseling Information",
    "information_for_patients": "Information for Patients",
}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)  # never stdout: the MCP server imports this file


# --------------------------------------------------------------------------- download

def download_corpus() -> None:
    """Fetch each label once from openFDA into corpus/<source>.json
    (and the extra label for the add_document demo into docs_to_add/)."""
    CORPUS_DIR.mkdir(exist_ok=True)
    EXTRA_DIR.mkdir(exist_ok=True)
    for doc in DOCUMENTS + EXTRA_DOCUMENTS:
        folder = EXTRA_DIR if doc in EXTRA_DOCUMENTS else CORPUS_DIR
        path = folder / f"{doc['source']}.json"
        if path.exists():
            continue
        query = f'set_id:"{doc["set_id"]}"' if doc.get("set_id") else doc["search"]
        log(f"downloading {doc['source']} ...")
        response = httpx.get(OPENFDA, params={"search": query, "limit": 1, "sort": "effective_time:desc"}, timeout=60)
        response.raise_for_status()
        label = response.json()["results"][0]
        path.write_text(json.dumps(label, indent=1), encoding="utf-8")


# --------------------------------------------------------------------------- extract + clean

def clean_text(text: str) -> str:
    """Remove HTML remnants, odd characters and repeated whitespace."""
    if "<" in text and ">" in text:
        text = BeautifulSoup(text, "html.parser").get_text(" ")
    text = text.replace(" ", " ").replace("•", " - ").replace("●", " - ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalise(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def load_document(path: Path) -> tuple[str, list[tuple[str, str, str]]]:
    """Return (source name, [(section_key, section_title, text), ...]).

    Supports openFDA label JSON (our corpus) and, for add_document, .txt/.md files
    (one section per Markdown heading) and .pdf files (one section per page).
    """
    path = Path(path)
    source = re.sub(r"[^a-z0-9_]+", "_", path.stem.lower()).strip("_")
    suffix = path.suffix.lower()

    if suffix == ".json":
        label = json.loads(path.read_text(encoding="utf-8"))
        sections = []
        for key, title in SECTIONS.items():
            value = label.get(key)
            if isinstance(value, list) and value:
                text = clean_text(" ".join(v for v in value if isinstance(v, str)))
                if len(text.split()) >= 5:
                    sections.append((key, title, text))
        # openFDA repeats sub-sections (e.g. "pregnancy" is also inside
        # "use_in_specific_populations"). Drop any section whose text is already
        # contained in another kept section, so the same passage is not indexed twice.
        kept = []
        for key, title, text in sections:
            n = normalise(text)
            if any(n in normalise(other) for k2, _, other in sections if k2 != key and len(other) > len(text)):
                continue
            kept.append((key, title, text))
        return source, kept

    if suffix == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        pages = [(f"page_{i + 1}", f"Page {i + 1}", clean_text(p.extract_text() or "")) for i, p in enumerate(reader.pages)]
        return source, [p for p in pages if p[2]]

    if suffix in {".txt", ".md"}:
        raw = path.read_text(encoding="utf-8")
        parts = re.split(r"^#+\s+(.+)$", raw, flags=re.M)
        sections = []
        if parts[0].strip():
            sections.append(("intro", "Introduction", clean_text(parts[0])))
        for title, body in zip(parts[1::2], parts[2::2]):
            key = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
            if body.strip():
                sections.append((key, title.strip(), clean_text(body)))
        return source, sections

    raise ValueError(f"Unsupported file type {suffix!r}: use .json (openFDA label), .pdf, .txt or .md")


# --------------------------------------------------------------------------- chunk

def split_sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.;:])\s+(?=[A-Z0-9(\-\[])", text) if s.strip()]


def pack(sentences: list[str], limit: int = CHUNK_WORDS) -> list[str]:
    """Greedily pack sentences into chunks of at most `limit` words."""
    chunks, current = [], []
    for sentence in sentences:
        words = sentence.split()
        while len(words) > limit:                      # one very long "sentence" (tables)
            if current:
                chunks.append(" ".join(current)); current = []
            chunks.append(" ".join(words[:limit])); words = words[limit:]
        if len(current) + len(words) > limit and current:
            chunks.append(" ".join(current)); current = []
        current += words
    if current:
        chunks.append(" ".join(current))
    return chunks


def display_name(source: str) -> str:
    return source.replace("_", " ").title()


def chunk_file(path: Path, design: str = CHOSEN_DESIGN) -> list[dict]:
    """Turn one document into chunks. Every chunk carries source, section and position."""
    source, sections = load_document(path)
    doc_hash = file_hash(path)
    chunks = []

    if design == "structure":
        for key, title, text in sections:
            for n, piece in enumerate(pack(split_sentences(text))):
                chunks.append({
                    "id": f"{source}:{key}:{n + 1}",
                    "text": piece,
                    "source": source, "section": title, "sections": title,
                    "position": n + 1,
                })

    elif design == "fixed":
        words, owners = [], []          # every word remembers which section it came from
        for key, title, text in sections:
            for w in text.split():
                words.append(w); owners.append(title)
        step = CHUNK_WORDS - FIXED_OVERLAP
        for n, start in enumerate(range(0, max(len(words) - FIXED_OVERLAP, 1), step)):
            span = owners[start:start + CHUNK_WORDS]
            covered = list(dict.fromkeys(span))
            chunks.append({
                "id": f"{source}:w{n + 1}",
                "text": " ".join(words[start:start + CHUNK_WORDS]),
                "source": source, "section": covered[0], "sections": "; ".join(covered),
                "position": n + 1,
            })
    else:
        raise ValueError(f"unknown design {design!r}")

    for c in chunks:
        c["file"] = Path(path).name
        c["doc_hash"] = doc_hash
        c["words"] = len(c["text"].split())
    return chunks


def embedding_text(chunk: dict) -> str:
    """What gets embedded: a short header with the drug and section, then the text."""
    return f"{display_name(chunk['source'])} drug label. Section: {chunk['section']}.\n{chunk['text']}"


# --------------------------------------------------------------------------- embed + store

_client = None


def gemini() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=load_api_key())
    return _client


def embed_texts(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed with Gemini, retrying on rate limits. Vectors are L2-normalised."""
    for attempt in range(8):
        try:
            result = gemini().models.embed_content(
                model=EMBED_MODEL,
                contents=texts,
                config=types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM),
            )
            vectors = []
            for e in result.embeddings:
                norm = math.sqrt(sum(v * v for v in e.values)) or 1.0
                vectors.append([v / norm for v in e.values])
            return vectors
        except Exception as error:  # noqa: BLE001
            message = str(error)
            if "429" in message or "RESOURCE_EXHAUSTED" in message or "503" in message:
                if "PerDay" in message or "per day" in message.lower():
                    raise RuntimeError("Daily embedding quota used up. Run again after 09:00 (Spain); saved vectors are kept.") from error
                wait = 20 * (attempt + 1)
                log(f"rate limited, waiting {wait}s ...")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("Embedding kept failing after retries.")


def embed_query(query: str) -> list[float]:
    return embed_texts([query], task="RETRIEVAL_QUERY")[0]


_chroma = None


def collection(design: str = CHOSEN_DESIGN):
    global _chroma
    if _chroma is None:
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        _chroma = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return _chroma.get_or_create_collection(design, metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str = CHOSEN_DESIGN) -> int:
    """Embed and store only the chunks that are not stored yet. Returns how many were embedded."""
    col = collection(design)
    existing = set(col.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in existing]
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        vectors = embed_texts([embedding_text(c) for c in batch])
        col.add(                       # saved straight away: a crash loses at most one batch
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{k: c[k] for k in ("source", "section", "sections", "position", "file", "doc_hash", "words")} for c in batch],
        )
        log(f"  [{design}] embedded {min(i + BATCH, len(todo))}/{len(todo)}")
    return len(todo)


# --------------------------------------------------------------------------- registry + add_document

def file_hash(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


def read_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}


def write_registry(registry: dict) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    REGISTRY.write_text(json.dumps(registry, indent=2, sort_keys=True), encoding="utf-8")


def add_file(path: str | Path, designs: list[str] | None = None) -> str:
    """Index one file. Same name + same content: nothing happens.
    Same name + new content: the old chunks are deleted and the new version indexed."""
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        return f"Not added: {path} does not exist."
    designs = designs or [CHOSEN_DESIGN]
    source, _ = load_document(path)
    new_hash = file_hash(path)
    registry = read_registry()
    old = registry.get(source)

    if old and old["sha256"] == new_hash and all(d in old.get("designs", []) for d in designs):
        return f"Already indexed: '{source}' ({old['chunks']} chunks) has the same content. Nothing changed."

    replaced = ""
    if old and old["sha256"] != new_hash:
        for d in designs:
            collection(d).delete(where={"source": source})
        replaced = f" Replaced the previous version (hash {old['sha256']})."

    total = 0
    for d in designs:
        chunks = chunk_file(path, d)
        embedded = embed_and_store(chunks, d)
        total = len(chunks)
        log(f"{source}: {len(chunks)} chunks in '{d}', {embedded} newly embedded")
    words = sum(len(t.split()) for _, _, t in load_document(path)[1])
    kept_designs = set(old.get("designs", [])) if old and not replaced else set()
    registry[source] = {"file": path.name, "sha256": new_hash, "chunks": total, "words": words,
                        "designs": sorted(kept_designs | set(designs))}
    write_registry(registry)
    return f"Added '{source}' from {path.name}: {total} chunks, {words} words.{replaced}"


# --------------------------------------------------------------------------- main

def build_index() -> None:
    download_corpus()
    registry = read_registry()
    total_words = 0
    for doc in DOCUMENTS:
        path = CORPUS_DIR / f"{doc['source']}.json"
        source, sections = load_document(path)
        words = sum(len(t.split()) for _, _, t in sections)
        total_words += words
        for design in DESIGNS:
            chunks = chunk_file(path, design)
            embedded = embed_and_store(chunks, design)
            log(f"{source}: {words} words, {len(chunks)} '{design}' chunks ({embedded} newly embedded)")
        label = json.loads(path.read_text(encoding="utf-8"))
        registry[source] = {
            "file": path.name, "sha256": file_hash(path), "words": words, "designs": DESIGNS,
            "chunks": len(chunk_file(path, CHOSEN_DESIGN)),
            "set_id": label.get("set_id"), "effective_time": label.get("effective_time"),
            "title": (label.get("openfda", {}).get("brand_name") or [""])[0],
        }
    write_registry(registry)
    for design in DESIGNS:
        log(f"collection '{design}': {collection(design).count()} chunks")
    log(f"corpus: {len(DOCUMENTS)} documents, {total_words} words")


if __name__ == "__main__":
    build_index()
