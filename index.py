"""
Assignment 3: build the index (`main.py index`).

1. ingest.build_corpus(): download missing sources, extract units (one § or one Rn.) to corpus/text/.
2. chunks_from_units(): drop Tenor, Tatbestand and the lower-court summary (part I of the
   Entscheidungsgründe), then merge consecutive units into ~200-400-word chunks without crossing
   a document or section boundary. Location = the § / Rn. range.
3. embed_and_store(): embed only chunks without a saved vector, store each batch in ChromaDB
   (index/chroma) as soon as it comes back.

server.py's add_document tool imports chunk_file() and embed_and_store().
"""

from __future__ import annotations

import hashlib
import json
import re
import statistics
import sys
import time
from pathlib import Path

import chromadb
from chromadb.config import Settings
from google import genai
from google.genai import errors, types

import ingest
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
CHUNKS_FILE = INDEX_DIR / "chunks.jsonl"  # readable copy, for writing the test set
COLLECTION = "baseline"
EMBED_MODEL = "gemini-embedding-2"
BATCH = 20
MIN_WORDS, MAX_WORDS = 200, 400
KEEP_JUDGMENT_SECTIONS = {"Leitsatz", "Entscheidungsgründe", "Gründe"}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- chunking

def keep_unit(u: dict) -> bool:
    if u["doc_type"] == "statute":
        return True
    if u["section"] not in KEEP_JUDGMENT_SECTIONS:
        return False  # Tenor, Tatbestand
    return not (u["section"] == "Entscheidungsgründe" and u.get("part") == "I.")  # lower court's reasoning


def _words(text: str) -> int:
    return len(text.split())


def _split_long(u: dict) -> list[dict]:
    """Split a unit longer than MAX_WORDS at line breaks (then sentences) into pieces."""
    if _words(u["text"]) <= MAX_WORDS:
        return [u]
    lines: list[str] = []
    for line in u["text"].split("\n"):
        if _words(line) <= MAX_WORDS:
            lines.append(line)
        else:
            lines.extend(s for s in re.split(r"(?<=[.;])\s+(?=[A-ZÄÖÜ(])", line) if s)
    pieces, cur = [], []
    for line in lines:
        if cur and _words("\n".join(cur + [line])) > MAX_WORDS:
            pieces.append("\n".join(cur))
            cur = []
        cur.append(line)
    if cur:
        pieces.append("\n".join(cur))
    return [{**u, "text": p, "piece": i + 1, "pieces": len(pieces)} for i, p in enumerate(pieces)]


def _statute_detail(text: str) -> str:
    """'Abs. 2–3' or 'Nr. 9–12' for a piece of a long §, from its leading paragraph/item numbers."""
    abs_ = re.findall(r"^\((\d+[a-z]?)\)", text, re.M)
    nrs = re.findall(r"^(\d+[a-z]?)\. ", text, re.M)
    for label, found in (("Abs.", abs_), ("Nr.", nrs)):
        if found:
            return f"{label} {found[0]}" if found[0] == found[-1] else f"{label} {found[0]}–{found[-1]}"
    return ""


def _rn_ranges(rns: list[str]) -> str:
    """['4', '11', '12', '13'] -> '4, 11–13': only the Rn. that are actually in the chunk."""
    nums = sorted({int(r) for r in rns if r.isdigit()})
    runs, start = [], None
    for i, n in enumerate(nums):
        if start is None:
            start = n
        if i == len(nums) - 1 or nums[i + 1] != n + 1:
            runs.append(str(start) if start == n else f"{start}–{n}")
            start = None
    return ", ".join(runs)


def _location(group: list[dict]) -> str:
    first, last = group[0], group[-1]
    doc = first["doc_id"]
    if first["doc_type"] == "judgment":
        if not first["rn"]:
            return first["location"]  # "BGH … , Leitsatz"
        return f"{doc}, Rn. {_rn_ranges([u['rn'] for u in group])}"
    head_first = first["location"].removesuffix(f" {doc}")
    head_last = last["location"].removesuffix(f" {doc}")
    if head_first == head_last:
        detail = _statute_detail("\n".join(u["text"] for u in group)) if "piece" in first else ""
        return f"{head_first} {detail} {doc}".replace("  ", " ") if detail else first["location"]
    return f"§§ {head_first.removeprefix('§ ')}–{head_last.removeprefix('§ ')} {doc}"


def _make_chunk(group: list[dict]) -> dict:
    first = group[0]
    text = "\n".join(u["text"] for u in group)
    location = _location(group)
    if first["doc_type"] == "judgment":
        header = f"{location} ({first['title']})"
    else:
        titles = list(dict.fromkeys(u["title"] for u in group if u["title"]))
        header = f"{location}: {'; '.join(titles)}"
    meta = {
        "doc_id": first["doc_id"],
        "doc_type": first["doc_type"],
        "location": location,
        "section": first.get("section", ""),
        "title": first["title"],
        "decision_date": first.get("decision_date", ""),
        "version": first.get("version", ""),
        "url": first["url"],
        "words": _words(text),
    }
    chunk_id = hashlib.sha1(f"{location}\n{text}".encode()).hexdigest()[:20]
    return {"id": chunk_id, "text": f"{header}\n{text}", "metadata": meta}


def chunks_from_units(units: list[dict]) -> list[dict]:
    pieces = [p for u in units if keep_unit(u) for p in _split_long(u)]
    groups: list[list[dict]] = []
    for p in pieces:
        cur = groups[-1] if groups else None
        same_block = cur and cur[0]["doc_id"] == p["doc_id"] and cur[0].get("section") == p.get("section")
        size = sum(_words(u["text"]) for u in cur) if cur else 0
        if same_block and size + _words(p["text"]) <= MAX_WORDS:
            cur.append(p)
        else:
            groups.append([p])
    # a short tail (< MIN_WORDS) joins the previous chunk of the same block if that stays under 1.25 x MAX
    merged: list[list[dict]] = []
    for g in groups:
        prev = merged[-1] if merged else None
        g_words = sum(_words(u["text"]) for u in g)
        if (prev and g_words < MIN_WORDS and prev[0]["doc_id"] == g[0]["doc_id"]
                and prev[0].get("section") == g[0].get("section")
                and sum(_words(u["text"]) for u in prev) + g_words <= MAX_WORDS * 1.25):
            prev.extend(g)
        else:
            merged.append(g)
    return [_make_chunk(g) for g in merged]


def units_from_file(path: str | Path) -> list[dict]:
    """Units from a judgment XML (rechtsprechung-im-internet.de) or a units .jsonl from corpus/text/."""
    path = Path(path)
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if path.suffix == ".xml":
        return ingest.extract_judgment(path)
    raise ValueError(f"Unsupported file type: {path.name} (expected a BGH judgment .xml or a units .jsonl)")


def chunk_file(path: str | Path) -> list[dict]:
    return chunks_from_units(units_from_file(path))


# ---------------------------------------------------------------- embedding and storage

class DailyQuotaExhausted(RuntimeError):
    pass


def get_collection(name: str = COLLECTION):
    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return client.get_or_create_collection(name, configuration={"hnsw": {"space": "cosine"}})


def embed_texts(client: genai.Client, texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed a batch. Waits out per-minute limits; raises DailyQuotaExhausted on the daily one."""
    for attempt in range(8):
        try:
            # One Content per text: gemini-embedding-2 merges a plain list of strings into ONE embedding.
            result = client.models.embed_content(
                model=EMBED_MODEL,
                contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
                config=types.EmbedContentConfig(task_type=task),
            )
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except errors.ClientError as error:
            if error.code != 429:
                raise
            if "PerDay" in str(error) or "per day" in str(error).lower():
                raise DailyQuotaExhausted(str(error)) from error
            wait = 30 * (attempt + 1)
            log(f"rate limited, waiting {wait}s ({attempt + 1}/8)")
            time.sleep(wait)
    raise RuntimeError("still rate limited after 8 attempts")


def embed_and_store(chunks: list[dict], collection=None, source: str = "base") -> int:
    """Embed the chunks that have no saved vector yet and store each batch at once. Returns how many were embedded."""
    collection = collection or get_collection()
    existing = set(collection.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in existing]
    if not todo:
        return 0
    client = genai.Client(api_key=load_api_key())
    done = 0
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        vectors = embed_texts(client, [c["text"] for c in batch])
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{**c["metadata"], "source": source} for c in batch],
        )  # persisted now: a crash later loses nothing
        done += len(batch)
        log(f"embedded {done}/{len(todo)}")
    return done


def remove_stale(collection, chunks: list[dict]) -> int:
    """Delete base-corpus chunks that the current chunking no longer produces (added documents are kept)."""
    current = {c["id"] for c in chunks}
    stored = collection.get(where={"source": "base"}, include=[])["ids"]
    stale = [i for i in stored if i not in current]
    if stale:
        collection.delete(ids=stale)
    return len(stale)


# ---------------------------------------------------------------- main

def report(chunks: list[dict], all_units: list[dict]) -> None:
    sizes = sorted(c["metadata"]["words"] for c in chunks)
    kept = sum(sizes)
    total = sum(_words(u["text"]) for u in all_units)
    dropped: dict[str, int] = {}
    for u in all_units:
        if not keep_unit(u):
            key = "Entscheidungsgründe part I (lower court)" if u["section"] == "Entscheidungsgründe" else u["section"]
            dropped[key] = dropped.get(key, 0) + _words(u["text"])
    print(f"\nwords extracted {total:,}; dropped " + ", ".join(f"{k} {v:,}" for k, v in dropped.items()) + f"; indexed {kept:,}")
    by_type = {t: [c for c in chunks if c["metadata"]["doc_type"] == t] for t in ("statute", "judgment")}
    print(f"chunks {len(chunks)} (statute {len(by_type['statute'])}, judgment {len(by_type['judgment'])})")
    q = statistics.quantiles(sizes, n=10)
    print(f"words per chunk: min {sizes[0]}, p10 {q[0]:.0f}, median {statistics.median(sizes):.0f}, "
          f"p90 {q[-1]:.0f}, max {sizes[-1]}, mean {statistics.mean(sizes):.0f}")
    bins = [(0, 100), (100, 200), (200, 300), (300, 400), (400, 500), (500, 10_000)]
    print("histogram: " + ", ".join(f"{a}-{b if b < 10_000 else '+'}: {sum(a <= s < b for s in sizes)}" for a, b in bins))


def main() -> None:
    ingest.build_corpus()
    files = sorted(ingest.TEXT.glob("*.jsonl"))
    all_units = [u for f in files for u in units_from_file(f)]
    chunks = [c for f in files for c in chunk_file(f)]
    assert len({c["id"] for c in chunks}) == len(chunks), "duplicate chunk ids"

    INDEX_DIR.mkdir(exist_ok=True)
    with CHUNKS_FILE.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps({"id": c["id"], **c["metadata"], "text": c["text"]}, ensure_ascii=False) + "\n")
    report(chunks, all_units)

    collection = get_collection()
    removed = remove_stale(collection, chunks)
    started = time.time()
    try:
        embedded = embed_and_store(chunks, collection)
    except DailyQuotaExhausted:
        stored = collection.count()
        print(f"\nDaily embedding quota reached. {stored} chunks stored; run `main.py index` again after the reset.")
        sys.exit(1)
    print(f"\nembedded {embedded} new chunk(s) in {time.time() - started:.0f}s; removed {removed} stale; "
          f"collection '{COLLECTION}' holds {collection.count()} chunks")


if __name__ == "__main__":
    main()
