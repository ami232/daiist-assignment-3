"""Shared retrieval code for index.py, server.py, agent.py and evaluate.py.

One place defines the embedding model, the vector cache, the Chroma collections and the
search designs, so the server, the agent and the evaluation all retrieve the same way.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
CACHE_FILE = INDEX_DIR / "embedding_cache.jsonl"
CORPUS_DIR = ROOT / "corpus"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
AGENT_MODEL = "gemini-flash-lite-latest"
JUDGE_MODEL = "gemini-3-flash-preview"  # a stronger model than the agent's
JUDGE_FALLBACK = "gemini-3.5-flash-lite"  # used only if the judge model's free daily quota runs out

# Designs compared in evaluate.py. Each "index design" is one set of chunks (one Chroma collection);
# "search designs" combine an index design with a search method.
INDEX_DESIGNS = ("structure", "fixed")
SEARCH_DESIGNS = {
    "fixed-dense": ("fixed", "dense"),
    "structure-dense": ("structure", "dense"),
    "structure-hybrid": ("structure", "hybrid"),
}
# Chosen by the hit-rate numbers in evaluate.py (see REPORT.md, "Retrieval").
ACTIVE_DESIGN = "structure-dense"
TOP_K = 5


def log(msg: str) -> None:
    """Log to stderr: stdout is reserved for the MCP protocol in server.py."""
    print(msg, file=sys.stderr, flush=True)


# ----------------------------------------------------------------------------- embeddings
_client = None


def client():
    global _client
    if _client is None:
        from google import genai
        from google.genai import types

        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key(), http_options=types.HttpOptions(timeout=60000))
    return _client


def _key(text: str, task: str) -> str:
    return hashlib.sha256(f"{EMBED_MODEL}|{EMBED_DIM}|{task}|{text}".encode()).hexdigest()


_cache: dict[str, list[float]] | None = None


def load_cache() -> dict[str, list[float]]:
    global _cache
    if _cache is None:
        _cache = {}
        if CACHE_FILE.exists():
            with CACHE_FILE.open(encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        row = json.loads(line)
                        _cache[row["k"]] = row["v"]
    return _cache


def embed(texts: list[str], task: str = "RETRIEVAL_DOCUMENT", batch: int = 25) -> list[list[float]]:
    """Embed texts, reusing saved vectors. New vectors are appended to the cache file immediately,
    so a crash or the daily free-tier limit never loses work already paid for."""
    from google.genai import types

    cache = load_cache()
    missing = [t for t in dict.fromkeys(texts) if _key(t, task) not in cache]
    if missing:
        INDEX_DIR.mkdir(exist_ok=True)
        log(f"embedding {len(missing)} new text(s) with {EMBED_MODEL} ({len(texts) - len(missing)} reused)")
    for i in range(0, len(missing), batch):
        part = missing[i:i + batch]
        for attempt in range(8):
            try:
                # gemini-embedding-2 is multimodal: a plain list of strings is treated as the parts of ONE
                # content and returns a single vector. Each text must be its own Content.
                res = client().models.embed_content(
                    model=EMBED_MODEL, contents=[types.Content(parts=[types.Part(text=t)]) for t in part],
                    config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM, task_type=task))
                break
            except Exception as e:  # noqa: BLE001 - rate limits: wait and retry
                msg = str(e)
                if ("429" in msg or "RESOURCE_EXHAUSTED" in msg or "503" in msg) and attempt < 7:
                    wait = 20 * (attempt + 1)
                    m = re.search(r"retry in ([\d.]+)s", msg)
                    if m:
                        wait = float(m.group(1)) + 2
                    if "per day" in msg.lower() or "PerDay" in msg:
                        raise RuntimeError("Daily embedding quota reached; rerun after the reset. "
                                           "Vectors embedded so far are saved.") from e
                    log(f"rate limited; waiting {wait:.0f}s")
                    time.sleep(wait)
                else:
                    raise
        if len(res.embeddings) != len(part):
            raise RuntimeError(f"asked for {len(part)} embeddings, got {len(res.embeddings)}")
        with CACHE_FILE.open("a", encoding="utf-8") as f:
            for t, emb in zip(part, res.embeddings):
                k = _key(t, task)
                cache[k] = emb.values
                f.write(json.dumps({"k": k, "v": [round(x, 6) for x in emb.values]}) + "\n")
    return [cache[_key(t, task)] for t in texts]


def embed_query(text: str) -> list[float]:
    return embed([text], task="RETRIEVAL_QUERY")[0]


# ----------------------------------------------------------------------------- chroma
def collection(design: str):
    import chromadb

    c = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return c.get_or_create_collection(name=design, metadata={"hnsw:space": "cosine"})


def all_chunks(design: str) -> list[dict]:
    col = collection(design)
    got = col.get(include=["documents", "metadatas"])
    return [{"id": i, "text": d, **m} for i, d, m in zip(got["ids"], got["documents"], got["metadatas"])]


# ----------------------------------------------------------------------------- BM25 (lexical)
_TOKEN = re.compile(r"[a-z0-9]+(?:[./-][a-z0-9]+)*")


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


class BM25:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.toks = [tokenize(d) for d in docs]
        self.k1, self.b = k1, b
        self.avg = sum(map(len, self.toks)) / max(len(self.toks), 1)
        df = Counter(t for d in self.toks for t in set(d))
        n = len(self.toks)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
        self.tf = [Counter(d) for d in self.toks]

    def scores(self, query: str) -> list[float]:
        q = tokenize(query)
        out = []
        for tf, d in zip(self.tf, self.toks):
            s = 0.0
            for t in q:
                if t in tf:
                    f = tf[t]
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * len(d) / self.avg))
            out.append(s)
        return out


_bm25: dict[str, tuple[BM25, list[dict]]] = {}


def _bm25_for(design: str, corpus_only: bool = False) -> tuple[BM25, list[dict]]:
    chunks = [c for c in all_chunks(design) if not corpus_only or c.get("origin") == "corpus"]
    key = f"{design}:{corpus_only}:{len(chunks)}"
    if key not in _bm25:
        _bm25.clear()
        _bm25[key] = (BM25([c["text"] for c in chunks]), chunks)
    return _bm25[key]


# ----------------------------------------------------------------------------- search
_mats: dict[str, tuple[int, list[dict], "np.ndarray"]] = {}


def _matrix(design: str):
    """All chunks of a design and their L2-normalised vectors, cached until the collection changes."""
    col = collection(design)
    count = col.count()
    cached = _mats.get(design)
    if cached and cached[0] == count:
        return cached[1], cached[2]
    got = col.get(include=["documents", "metadatas", "embeddings"])
    order = sorted(range(len(got["ids"])), key=lambda i: got["ids"][i])
    chunks = [{"id": got["ids"][i], "text": got["documents"][i], **got["metadatas"][i]} for i in order]
    mat = np.asarray([got["embeddings"][i] for i in order], dtype=np.float32)
    mat /= np.linalg.norm(mat, axis=1, keepdims=True)
    _mats[design] = (count, chunks, mat)
    return chunks, mat


def search(query: str, design: str = ACTIVE_DESIGN, k: int = TOP_K, exclude_added: bool = False) -> list[dict]:
    """Return the top-k chunks (dicts with id, text, source, location, score) for a query.

    dense  : cosine similarity of Gemini embeddings (Chroma).
    hybrid : reciprocal-rank fusion (k=60) of the dense ranking and a BM25 ranking over the same chunks.
    exclude_added: hide documents added later with add_document (used to keep the evaluation reproducible).
    """
    index_design, method = SEARCH_DESIGNS[design]
    n_dense = max(k, 30) if method == "hybrid" else k
    # Exact cosine search over every stored vector. With a few hundred chunks this is instant, and unlike
    # Chroma's approximate HNSW query it is deterministic (the same query always returns the same chunks).
    chunks, mat = _matrix(index_design)
    q = np.asarray(embed_query(query), dtype=np.float32)
    sims = mat @ (q / (np.linalg.norm(q) or 1.0))
    order = [i for i in np.argsort(-sims, kind="stable") if not (exclude_added and chunks[i].get("origin") != "corpus")]
    dense = [{**chunks[i], "score": round(float(sims[i]), 4)} for i in order[:n_dense]]
    if method == "dense":
        return dense[:k]
    bm, chunks = _bm25_for(index_design, corpus_only=exclude_added)
    s = bm.scores(query)
    order = sorted(range(len(chunks)), key=lambda i: (-s[i], chunks[i]["id"]))
    lexical = [chunks[i] for i in order][:30]
    fused: dict[str, float] = {}
    by_id = {}
    for rank_list in (dense, lexical):
        for r, c in enumerate(rank_list):
            fused[c["id"]] = fused.get(c["id"], 0.0) + 1.0 / (60 + r + 1)
            by_id.setdefault(c["id"], c)
    top = sorted(fused, key=lambda i: -fused[i])[:k]
    return [{**by_id[i], "score": round(fused[i], 5)} for i in top]


def format_results(results: list[dict]) -> str:
    """Text the model reads: every chunk with a citation tag [source, location] and its chunk id."""
    if not results:
        return "No results."
    out = []
    for r in results:
        out.append(f"[{r['id']}] {r['source']} | {r['location']}\n{r['text']}")
    return "\n\n---\n\n".join(out)
