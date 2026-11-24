"""
Build the index (`uv run python main.py index`).

Pipeline for every ficha in data/fichas/:
    1. ficha_to_sections  -> split the JSON into named sections (que_es, plazo_resolucion, faq...)
    2. chunk_file         -> turn those sections into chunks, with one of two designs
    3. embed_and_store    -> embed the chunks with Gemini and save them in ChromaDB (index/)

Two chunking designs are built, each in its own ChromaDB collection, so
evaluate.py can compare them:
    "fixed"    : all the text of a ficha glued together and cut every 200 words
    "sections" : one chunk per section of the ficha (long sections cut at 300 words,
                 very short ones packed with the next section)

server.py imports these functions (add_file, search) so a new document goes
through exactly the same pipeline.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

import chromadb
from google import genai
from google.genai import types

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
FICHAS_DIR = ROOT / "data" / "fichas"
INDEX_DIR = ROOT / "index"

EMBEDDING_MODEL = "gemini-embedding-2"
DESIGNS = ["fixed", "sections"]
CHOSEN_DESIGN = "fixed"  # best hit@3 in evaluate.py (0.89 vs 0.74), see REPORT.md

FIXED_SIZE = 200  # words per chunk in the "fixed" design
MIN_SECTION = 40  # shorter sections are packed with the next one ("sections" design)
MAX_SECTION = 300  # longest chunk allowed in the "sections" design
BATCH_SIZE = 20  # chunks sent to Gemini in one request

_client = None


def gemini():
    """Create the Gemini client once and reuse it."""
    global _client
    if _client is None:
        _client = genai.Client(api_key=load_api_key())
    return _client


def get_collection(design: str):
    """Open (or create) the ChromaDB collection of one design, stored in index/."""
    db = chromadb.PersistentClient(path=str(INDEX_DIR))
    # We give ChromaDB our own Gemini vectors, so it needs no embedding function.
    return db.get_or_create_collection(name=design, embedding_function=None,
                                       metadata={"hnsw:space": "cosine"})


# ---------------------------------------------------------------- 1. sections

def field_to_text(value) -> str:
    """A ficha field can be a string, a list of strings or a list of FAQ items."""
    if isinstance(value, str):
        return value.strip()
    lines = []
    for item in value:
        if isinstance(item, dict):  # an FAQ item: {"q": question, "a": answer}
            lines.append(f"P: {item['q']}\nR: {item['a']}")
        else:
            lines.append(f"- {item}")
    return "\n".join(lines)


def ficha_to_sections(path: Path) -> tuple[dict, list[tuple[str, str]]]:
    """Read a ficha and return (info, [(section_name, text), ...]).

    info holds what every chunk of this ficha carries: slug, name and sede link.
    """
    ficha = json.loads(Path(path).read_text(encoding="utf-8"))
    info = {
        "source": ficha["slug"],
        "nombre_oficial": ficha["nombre_oficial"],
        "sede_url": ficha.get("sede_url", ""),
    }
    sections = []
    for field, value in ficha.items():
        if field in ("slug", "sede_url") or not value:
            continue
        sections.append((field, field_to_text(value)))
    return info, sections


# ---------------------------------------------------------------- 2. chunks

def split_words(text: str, size: int) -> list[str]:
    """Cut a text into pieces of at most `size` words."""
    words = text.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]


def chunk_file(path: Path, design: str) -> list[dict]:
    """Turn one ficha into chunks. Each chunk is a dict with id, text and metadata."""
    info, sections = ficha_to_sections(path)
    file_hash = hashlib.md5(Path(path).read_bytes()).hexdigest()
    header = f"Trámite: {info['nombre_oficial']}"
    chunks = []

    if design == "sections":
        # Very short sections (e.g. identificacion: "Clave o certificado digital") are
        # packed together with their neighbours, so we don't spend one embedding on 4 words.
        groups, current = [], []
        for section, text in sections:
            current.append((section, text))
            if sum(len(t.split()) for _, t in current) >= MIN_SECTION:
                groups.append(current)
                current = []
        if current:
            groups.append(current)

        for group in groups:
            names = [section for section, _ in group]
            text = "\n".join(f"[{section}] {text}" for section, text in group)
            for n, piece in enumerate(split_words(text, MAX_SECTION)):
                chunks.append({
                    "id": f"{info['source']}#{names[0]}#{n}",
                    "text": f"{header}\n{piece}",
                    "location": "+".join(names),
                    "sections": ",".join(names),
                })

    elif design == "fixed":
        # Glue all sections together, remembering which section each word came from,
        # so we can still tell which sections a fixed chunk covers.
        words, word_section = [], []
        for section, text in sections:
            for word in f"[{section}] {text}".split():
                words.append(word)
                word_section.append(section)
        for n, start in enumerate(range(0, len(words), FIXED_SIZE)):
            end = min(start + FIXED_SIZE, len(words))
            covered = list(dict.fromkeys(word_section[start:end]))  # unique, in order
            chunks.append({
                "id": f"{info['source']}#fixed#{n}",
                "text": f"{header}\n" + " ".join(words[start:end]),
                "location": f"palabras {start}-{end}",
                "sections": ",".join(covered),
            })
    else:
        raise ValueError(f"Unknown design: {design}")

    for chunk in chunks:
        chunk.update(info)
        chunk["file_hash"] = file_hash
    return chunks


# ---------------------------------------------------------------- 3. embeddings

def embed(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts with Gemini. Waits and retries if we hit the rate limit."""
    for attempt in range(5):
        try:
            # Each text must be its own Content: a plain list of strings would be read
            # as ONE multi-part input and come back as a single embedding.
            contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
            result = gemini().models.embed_content(model=EMBEDDING_MODEL, contents=contents)
            return [e.values for e in result.embeddings]
        except Exception as error:  # usually 429: too many requests
            if "429" not in str(error) or attempt == 4:
                raise
            print(f"  rate limit, waiting 60 s ({error.__class__.__name__})", file=sys.stderr)
            time.sleep(60)


def embed_query(question: str) -> list[float]:
    return embed([question])[0]


def embed_and_store(chunks: list[dict], collection) -> int:
    """Embed only the chunks that are not in the collection yet. Returns how many were new.

    Vectors are saved after every batch, so if the daily quota runs out we lose
    nothing: the next run continues where this one stopped.
    """
    existing = set(collection.get(ids=[c["id"] for c in chunks])["ids"]) if chunks else set()
    new = [c for c in chunks if c["id"] not in existing]
    for i in range(0, len(new), BATCH_SIZE):
        batch = new[i:i + BATCH_SIZE]
        collection.add(
            ids=[c["id"] for c in batch],
            documents=[c["text"] for c in batch],
            embeddings=embed([c["text"] for c in batch]),
            metadatas=[{k: c[k] for k in ("source", "location", "sections", "nombre_oficial",
                                          "sede_url", "file_hash")} for c in batch],
        )
        print(f"  embedded {i + len(batch)}/{len(new)}", file=sys.stderr)
    return len(new)


# ---------------------------------------------------------------- used by server.py

def add_file(path: str, design: str = CHOSEN_DESIGN) -> str:
    """Index one ficha. If it is already indexed: skip it when unchanged, replace it when changed."""
    path = Path(path).expanduser()
    if not path.is_file() or path.suffix != ".json":
        return f"Error: {path} is not a JSON ficha."
    collection = get_collection(design)
    chunks = chunk_file(path, design)
    source = chunks[0]["source"]

    old = collection.get(where={"source": source})
    if old["ids"]:
        old_hashes = {m["file_hash"] for m in old["metadatas"]}
        if old_hashes == {chunks[0]["file_hash"]}:
            return f"Skipped: '{source}' is already indexed and the file has not changed."
        collection.delete(ids=old["ids"])  # changed file: remove the old version first
        embed_and_store(chunks, collection)
        return f"Replaced: '{source}' had changed; removed {len(old['ids'])} old chunks, added {len(chunks)}."

    embed_and_store(chunks, collection)
    return f"Added: '{source}' ({len(chunks)} chunks)."


def search(query: str, k: int = 5, design: str = CHOSEN_DESIGN, query_vector=None) -> list[dict]:
    """Return the k chunks closest to the query, each with its text and metadata."""
    vector = query_vector if query_vector is not None else embed_query(query)
    result = get_collection(design).query(query_embeddings=[vector], n_results=k)
    hits = []
    for text, meta, distance in zip(result["documents"][0], result["metadatas"][0],
                                    result["distances"][0]):
        hits.append({"text": text, "distance": round(distance, 3), **meta})
    return hits


# ---------------------------------------------------------------- main

def main() -> None:
    files = sorted(FICHAS_DIR.glob("*.json"))
    for design in DESIGNS:
        collection = get_collection(design)
        all_chunks = [chunk for path in files for chunk in chunk_file(path, design)]
        print(f"[{design}] {len(files)} fichas -> {len(all_chunks)} chunks")
        added = embed_and_store(all_chunks, collection)
        print(f"[{design}] embedded {added} new chunks; collection now holds {collection.count()}")


if __name__ == "__main__":
    main()
