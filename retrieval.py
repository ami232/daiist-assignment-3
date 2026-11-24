"""
Assignment 3: search over the index. Shared by server.py (search tool) and
evaluate.py (retrieval comparison), so both use exactly the same code.

Two designs, on the same chunks:
- "vector": Gemini embedding of the question, nearest chunks by cosine distance (ChromaDB).
- "hybrid": vector search + keyword search (BM25), merged with reciprocal rank fusion.

Question embeddings are cached in index/query_cache.json, so asking the same
question twice (or re-running the evaluation) does not spend embedding quota.
"""

import json
import math
import os
import re
import threading
from collections import Counter
from functools import lru_cache

from google import genai

from api_key import load_api_key
from index import EMBED_DIM, EMBED_MODEL, INDEX_DIR, embed_one, get_collection

QUERY_CACHE = INDEX_DIR / "query_cache.json"
CANDIDATES = 50  # how many results each method returns before fusion
RRF_K = 60  # standard constant for reciprocal rank fusion


# ---------- vector search ----------

def query_text(question: str) -> str:
    """The format Google suggests for search queries with gemini-embedding-2."""
    return f"task: search result | query: {question}"


_cache_lock = threading.Lock()  # the agent can run two searches at once; only one may touch the cache file


def read_cache() -> dict:
    """Read the query cache. If the file is damaged, keep whatever can still be read."""
    if not QUERY_CACHE.exists():
        return {}
    text = QUERY_CACHE.read_text()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            return json.JSONDecoder().raw_decode(text)[0]  # a damaged tail: keep the first complete object
        except json.JSONDecodeError:
            return {}


def embed_query(question: str) -> list[float]:
    """Embed a question, using the cache when we have embedded it before."""
    key = f"{EMBED_MODEL}/{EMBED_DIM}/{question}"
    with _cache_lock:
        cache = read_cache()
        if key in cache:
            return cache[key]
    client = genai.Client(api_key=load_api_key())
    vector = embed_one(client, query_text(question))
    with _cache_lock:
        cache = read_cache()
        cache[key] = vector
        tmp = QUERY_CACHE.with_suffix(".tmp")
        tmp.write_text(json.dumps(cache))
        os.replace(tmp, QUERY_CACHE)  # atomic: the file is never half-written
    return vector


def vector_search(question: str, k: int) -> list[str]:
    """Ids of the k chunks closest in meaning to the question."""
    result = get_collection().query(query_embeddings=[embed_query(question)], n_results=k, include=[])
    return result["ids"][0]


# ---------- keyword search (BM25) ----------

TOKEN = re.compile(r"[a-z0-9]+(?:[.,][0-9]+)?")  # keeps numbers like 2.5 or 2,5 together
STOPWORDS = set("""a an and are as at be by can do does for from has have how i if in is it its
my of on or our the their there this to was we what when where which who will with you your""".split())


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN.findall(text.lower()) if t not in STOPWORDS]


@lru_cache(maxsize=1)
def bm25_index():
    """Build the BM25 keyword index from the chunk texts stored in index/ (no embeddings needed)."""
    data = get_collection().get(include=["documents"])
    ids, docs = data["ids"], [tokenize(d) for d in data["documents"]]
    df = Counter(term for doc in docs for term in set(doc))
    avg_len = sum(len(d) for d in docs) / len(docs)
    return ids, [Counter(d) for d in docs], [len(d) for d in docs], df, avg_len, len(docs)


def keyword_search(question: str, k: int, k1: float = 1.5, b: float = 0.75) -> list[str]:
    """Ids of the k chunks that best match the question's words (BM25 scoring)."""
    ids, counts, lengths, df, avg_len, n = bm25_index()
    terms = tokenize(question)
    scores = []
    for doc_id, tf, length in zip(ids, counts, lengths):
        score = 0.0
        for term in terms:
            if term in tf:
                idf = math.log(1 + (n - df[term] + 0.5) / (df[term] + 0.5))
                score += idf * tf[term] * (k1 + 1) / (tf[term] + k1 * (1 - b + b * length / avg_len))
        if score > 0:
            scores.append((score, doc_id))
    return [doc_id for _, doc_id in sorted(scores, reverse=True)[:k]]


# ---------- hybrid ----------

def hybrid_search(question: str, k: int) -> list[str]:
    """Merge vector and keyword results: each chunk scores 1/(60 + rank) in each list."""
    fused = Counter()
    for ranking in (vector_search(question, CANDIDATES), keyword_search(question, CANDIDATES)):
        for rank, doc_id in enumerate(ranking, start=1):
            fused[doc_id] += 1 / (RRF_K + rank)
    return [doc_id for doc_id, _ in fused.most_common(k)]


DESIGNS = {"vector": vector_search, "hybrid": hybrid_search}
DEFAULT_DESIGN = "hybrid"  # updated after the retrieval comparison


def search(question: str, k: int = 5, design: str = DEFAULT_DESIGN) -> list[dict]:
    """The top-k chunks for a question, with their text and citation."""
    ids = DESIGNS[design](question, k)
    if not ids:
        return []
    data = get_collection().get(ids=ids, include=["documents", "metadatas"])
    by_id = {i: (doc, meta) for i, doc, meta in zip(data["ids"], data["documents"], data["metadatas"])}
    results = []
    for rank, doc_id in enumerate(ids, start=1):
        doc, meta = by_id[doc_id]
        results.append({
            "rank": rank, "id": doc_id, "source": meta["source"], "title": meta["title"],
            "page": meta["page"], "text": doc,
        })
    return results
