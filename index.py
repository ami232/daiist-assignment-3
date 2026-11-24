"""
Assignment 3: build the index (`main.py index`).

Pipeline: fetch_corpus -> chunk_file -> embed_and_store -> search_index.

Corpus: the English articles of the Chedar help centre (https://learn.chedar.io).
Every article is available as plain markdown by adding `.md` to its URL, so no
HTML cleaning is needed. Articles go to corpus/ (git-ignored).

Three designs are compared in evaluate.py:
  A  structure-aware: one chunk per markdown heading section; tiny sections are
     merged into their neighbour, huge ones are split at paragraph boundaries.
  B  fixed windows: ~350 words with 50 words of overlap, ignoring structure.
  C  hybrid search over A's chunks: vector + BM25 keyword ranks merged by RRF.
     It reuses A's collection, so it needs no chunking or embedding of its own.

Vectors are saved in ChromaDB (index/) batch by batch; only chunks whose id is
not stored yet are embedded, so a crash or the daily quota loses nothing.
"""

import collections
import math
import re
import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"

SITE = "https://learn.chedar.io"
LLMS_URL = f"{SITE}/llms.txt"
EN_ARTICLE = re.compile(r"\((https://learn\.chedar\.io/en/docs/[^)\s]+?)\.md\)")

EMBED_MODEL = "gemini-embedding-2"
EMBED_BATCH = 50

DESIGNS = {
    "A": {"description": "one chunk per heading section (merge < 120 words, split > 450)",
          "min_words": 120, "max_words": 450},
    "B": {"description": "fixed 350-word windows, 50 words overlap, structure ignored",
          "window": 350, "overlap": 50},
    "C": {"description": "hybrid: vector + BM25 over design A's chunks, merged with RRF",
          "base": "A", "pool": 20, "rrf_k": 60},
}
CHOSEN_DESIGN = "A"

NL = "\n"
BLANK = "\n\n"


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- fetching

def _get(client: httpx.Client, url: str, tries: int = 3) -> str:
    for attempt in range(tries):
        try:
            response = client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as error:
            if attempt == tries - 1:
                raise
            log(f"  retry {url} ({error})")
            time.sleep(2 * (attempt + 1))
    raise RuntimeError("unreachable")


def _filename(url: str) -> str:
    return url.removeprefix(f"{SITE}/en/docs/").replace("/", "__") + ".md"


def fetch_corpus(delay: float = 0.2) -> list[Path]:
    """Download every English article to corpus/ (skipping ones already there)."""
    CORPUS_DIR.mkdir(exist_ok=True)
    with httpx.Client(timeout=30, follow_redirects=True,
                      headers={"User-Agent": "chedar-rag-student-project"}) as client:
        urls = list(dict.fromkeys(EN_ARTICLE.findall(_get(client, LLMS_URL))))
        log(f"{len(urls)} English articles listed in llms.txt")
        paths = []
        for url in urls:
            path = CORPUS_DIR / _filename(url)
            if not path.exists():
                text = _get(client, url + ".md")
                path.write_text(f"<!-- source: {url} -->\n{text}", encoding="utf-8")
                time.sleep(delay)
            paths.append(path)
    return paths


# ---------------------------------------------------------------- chunking

def read_article(path: Path) -> tuple[str, str, str]:
    """Return (source url, title, body) of a downloaded article."""
    raw = path.read_text(encoding="utf-8")
    first, _, body = raw.partition("\n")
    match = re.match(r"<!-- source: (\S+) -->", first)
    source = match.group(1) if match else path.stem
    title = next((line[2:].strip() for line in body.splitlines() if line.startswith("# ")),
                 path.stem)
    return source, title, body


def split_sections(body: str) -> list[tuple[list[str], str]]:
    """Split markdown into (heading path, text incl. its heading line) sections.

    '#' lines inside code fences are not headings.
    """
    sections, stack, lines, in_code = [], [], [], False

    def flush():
        text = NL.join(lines).strip()
        if text:
            sections.append((list(stack), text))
        lines.clear()

    for line in body.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        heading = None if in_code else re.match(r"^(#{1,6})\s+(.*\S)", line)
        if heading:
            flush()
            level = len(heading.group(1))
            stack[:] = stack[:level - 1] + [f"{'#' * level} {heading.group(2)}"]
        lines.append(line)
    flush()
    return sections


def words(text: str) -> int:
    return len(text.split())


def paragraphs(text: str, max_words: int) -> list[str]:
    """Blank-line paragraphs; a paragraph over max_words (table, list) is cut by line."""
    result = []
    for paragraph in re.split(r"\n\s*\n", text):
        result.extend(paragraph.splitlines() if words(paragraph) > max_words else [paragraph])
    return result


def split_long(text: str, max_words: int) -> list[str]:
    """Split on blank lines into pieces of at most ~max_words words."""
    pieces, current = [], []
    for paragraph in paragraphs(text, max_words):
        if current and words(BLANK.join(current + [paragraph])) > max_words:
            pieces.append(BLANK.join(current))
            current = []
        current.append(paragraph)
    pieces.append(BLANK.join(current))
    return pieces


def design_a(body: str, min_words: int, max_words: int) -> list[tuple[list[str], str]]:
    """Heading sections; a section under min_words absorbs the next one."""
    merged: list[tuple[list[str], str]] = []
    pending: tuple[list[str], str] | None = None
    for path, text in split_sections(body):
        if pending:
            path, text = pending[0], pending[1] + BLANK + text
        if words(text) < min_words:
            pending = (path, text)
        else:
            merged.append((path, text))
            pending = None
    if pending:
        if merged:
            merged[-1] = (merged[-1][0], merged[-1][1] + BLANK + pending[1])
        else:
            merged.append(pending)
    return [(path, piece) for path, text in merged for piece in split_long(text, max_words)]


def design_b(body: str, window: int, overlap: int) -> list[tuple[list[str], str]]:
    """Fixed word windows; the heading path is the one in force where a window starts."""
    tokens = [(path, word) for path, text in split_sections(body) for word in text.split()]
    chunks = []
    for start in range(0, len(tokens), window - overlap):
        piece = tokens[start:start + window]
        chunks.append((piece[0][0], " ".join(word for _, word in piece)))
        if start + window >= len(tokens):
            break
    return chunks


def chunk_file(path: Path, design: str = CHOSEN_DESIGN) -> list[dict]:
    """Cut one article into chunks: id, text, source, title, section, location."""
    source, title, body = read_article(Path(path))
    spec = DESIGNS[design]
    if design == "A":
        pieces = design_a(body, spec["min_words"], spec["max_words"])
    else:
        pieces = design_b(body, spec["window"], spec["overlap"])
    slug = Path(path).stem
    chunks = []
    for number, (heading_path, text) in enumerate(pieces):
        location = " > ".join(heading_path)
        chunks.append({
            "id": f"{slug}#{number}",
            "text": text,
            "source": source,
            "title": title,
            "section": heading_path[-1].lstrip("# ") if heading_path else title,
            "location": location or title,
        })
    return chunks


# ---------------------------------------------------------------- embedding

_client = None


def _genai_client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())  # raises a clear error if no key
    return _client


def embedding_input(text: str, task: str, title: str = "none") -> str:
    """gemini-embedding-2 takes the task as a text prefix instead of a task_type."""
    if task == "query":
        return f"task: search result | query: {text}"
    return f"title: {title} | text: {text}"


class QuotaExceeded(RuntimeError):
    pass


def embed_texts(texts: list[str], task: str = "document", titles: list[str] | None = None) -> list[list[float]]:
    """Embed texts with Gemini; task is "document" or "query". Batched."""
    if task not in ("document", "query"):
        raise ValueError("task must be 'document' or 'query'")
    from google.genai import types
    client = _genai_client()
    titles = titles or ["none"] * len(texts)
    inputs = [embedding_input(t, task, title) for t, title in zip(texts, titles)]
    vectors: list[list[float]] = []
    for start in range(0, len(inputs), EMBED_BATCH):
        batch = inputs[start:start + EMBED_BATCH]
        for attempt in range(8):
            try:
                # One Content per text: gemini-embedding-2 merges a plain list of
                # strings into a single multi-part input and returns one vector.
                contents = [types.Content(parts=[types.Part(text=s)]) for s in batch]
                response = client.models.embed_content(model=EMBED_MODEL, contents=contents)
                break
            except Exception as error:  # noqa: BLE001
                message = str(error)
                if "429" in message or "RESOURCE_EXHAUSTED" in message:
                    # Free tier: 100 texts per minute (wait it out) and a daily cap (stop).
                    if "per minute" in message.lower() and attempt < 7:
                        log("Per-minute embedding limit hit; waiting 65 s...")
                        time.sleep(65)
                        continue
                    raise QuotaExceeded(message) from error
                if attempt >= 2:
                    raise
                time.sleep(3 * (attempt + 1))
        if len(response.embeddings) != len(batch):
            raise RuntimeError(f"Expected {len(batch)} embeddings, got {len(response.embeddings)}")
        vectors.extend(list(e.values) for e in response.embeddings)
    return vectors


def _collection(design: str):
    import chromadb
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    return client.get_or_create_collection(
        f"chedar_{design}", configuration={"hnsw": {"space": "cosine"}})


def embed_and_store(chunks: list[dict], design: str = CHOSEN_DESIGN) -> int:
    """Embed only chunks not stored yet; save after every batch. Returns new count."""
    collection = _collection(design)
    known = set(collection.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in known]
    log(f"[{design}] {len(chunks)} chunks, {len(known)} already stored, {len(todo)} to embed")
    done = 0
    for start in range(0, len(todo), EMBED_BATCH):
        batch = todo[start:start + EMBED_BATCH]
        try:
            vectors = embed_texts([c["text"] for c in batch], "document", [c["title"] for c in batch])
        except QuotaExceeded as error:
            log(f"[{design}] QUOTA REACHED (429) after {done} new vectors; "
                f"{len(todo) - done} chunks remain. Run again after the daily reset.\n  {error}"[:600])
            return done
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{k: c[k] for k in ("source", "title", "section", "location")} for c in batch],
        )
        done += len(batch)
        log(f"[{design}] stored {done}/{len(todo)}")
    return done


def tokenize(text: str) -> list[str]:
    return re.findall(r"[^\W_]+", text.lower())


_bm25: dict[str, dict] = {}


def _bm25_index(design: str) -> dict:
    """Term counts per chunk of a collection, built once and kept in memory."""
    if design not in _bm25:
        stored = _collection(design).get()
        counts = [collections.Counter(tokenize(t)) for t in stored["documents"]]
        doc_freq = collections.Counter(term for c in counts for term in c)
        lengths = [sum(c.values()) for c in counts]
        _bm25[design] = {"ids": stored["ids"], "docs": stored["documents"],
                         "metas": stored["metadatas"], "counts": counts,
                         "doc_freq": doc_freq, "lengths": lengths,
                         "avg_len": sum(lengths) / len(lengths)}
    return _bm25[design]


def bm25_search(query: str, k: int, design: str, k1: float = 1.5, b: float = 0.75) -> list[dict]:
    """Rank a collection's chunks by BM25; `score` is the BM25 score."""
    idx = _bm25_index(design)
    n = len(idx["ids"])
    terms = set(tokenize(query))
    scores = []
    for i, counts in enumerate(idx["counts"]):
        norm = k1 * (1 - b + b * idx["lengths"][i] / idx["avg_len"])
        score = 0.0
        for term in terms & counts.keys():
            df = idx["doc_freq"][term]
            idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
            score += idf * counts[term] * (k1 + 1) / (counts[term] + norm)
        if score > 0:
            scores.append((score, i))
    scores.sort(reverse=True)
    return [{"id": idx["ids"][i], "text": idx["docs"][i], **idx["metas"][i], "score": score}
            for score, i in scores[:k]]


def hybrid_search(query: str, k: int, base: str, pool: int, rrf_k: int) -> list[dict]:
    """Reciprocal rank fusion of the vector and BM25 rankings; `score` is the RRF score."""
    fused, chunks = collections.Counter(), {}
    for ranking in (search_index(query, pool, base), bm25_search(query, pool, base)):
        for rank, chunk in enumerate(ranking, start=1):
            fused[chunk["id"]] += 1 / (rrf_k + rank)
            chunks[chunk["id"]] = chunk
    return [{**chunks[i], "score": score} for i, score in fused.most_common(k)]


def search_index(query: str, k: int = 5, design: str = CHOSEN_DESIGN) -> list[dict]:
    """Return the k best chunks as chunk dicts plus `score` (cosine similarity for A and B)."""
    spec = DESIGNS[design]
    if "base" in spec:
        return hybrid_search(query, k, spec["base"], spec["pool"], spec["rrf_k"])
    collection = _collection(design)
    vector = embed_texts([query], "query")[0]
    found = collection.query(query_embeddings=[vector], n_results=k)
    results = []
    for chunk_id, text, meta, distance in zip(found["ids"][0], found["documents"][0],
                                              found["metadatas"][0], found["distances"][0]):
        results.append({"id": chunk_id, "text": text, **meta, "score": 1 - distance})
    return results


# ---------------------------------------------------------------- main

def main() -> int:
    paths = fetch_corpus()
    log(f"{len(paths)} articles in corpus/")
    for design in DESIGNS:
        if "base" in DESIGNS[design]:
            continue  # hybrid design: reuses its base design's vectors
        chunks = [c for p in paths for c in chunk_file(p, design)]
        embed_and_store(chunks, design)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
