"""
Retrieval shared by server.py and evaluate.py.

    dense(query_vector, design, k)      : nearest chunks by cosine similarity (ChromaDB)
    bm25(query, design, k)              : keyword ranking (BM25) over the same chunks
    hybrid(query, query_vector, design) : both lists fused with Reciprocal Rank Fusion
    search(query)                       : what the MCP search tool runs (the chosen design)
"""

import math
import re
import time
from collections import Counter

import index as pipeline

K = 5                     # chunks returned by the search tool
SEARCH_METHOD = "dense"   # chosen from eval/retrieval_results.csv: structure + dense had the best hit@1/3/5
RRF_K = 60

_bm25_cache: dict = {}


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:\.[0-9]+)?", text.lower())


def _rows(design: str) -> list[dict]:
    data = pipeline.collection(design).get(include=["documents", "metadatas"])
    return [{"id": i, "text": d, **m} for i, d, m in zip(data["ids"], data["documents"], data["metadatas"])]


def dense(query_vector: list[float], design: str = pipeline.CHOSEN_DESIGN, k: int = K) -> list[dict]:
    res = pipeline.collection(design).query(query_embeddings=[query_vector], n_results=k,
                                            include=["documents", "metadatas", "distances"])
    return [{"id": i, "text": d, "score": 1 - dist, **m}
            for i, d, m, dist in zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0])]


def _bm25_index(design: str):
    count = pipeline.collection(design).count()
    cached = _bm25_cache.get(design)
    if cached and cached["count"] == count:
        return cached
    rows = _rows(design)
    docs = [tokens(pipeline.display_name(r["source"]) + " " + r["section"] + " " + r["text"]) for r in rows]
    df = Counter(t for d in docs for t in set(d))
    cached = {"count": count, "rows": rows, "docs": [Counter(d) for d in docs], "lens": [len(d) for d in docs],
              "df": df, "avg": sum(len(d) for d in docs) / max(len(docs), 1), "n": len(docs)}
    _bm25_cache[design] = cached
    return cached


def bm25(query: str, design: str = pipeline.CHOSEN_DESIGN, k: int = K, k1: float = 1.5, b: float = 0.75) -> list[dict]:
    ix = _bm25_index(design)
    q = tokens(query)
    scores = []
    for row, tf, length in zip(ix["rows"], ix["docs"], ix["lens"]):
        s = 0.0
        for t in q:
            if t in tf:
                idf = math.log(1 + (ix["n"] - ix["df"][t] + 0.5) / (ix["df"][t] + 0.5))
                s += idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * length / ix["avg"]))
        scores.append(s)
    order = sorted(range(len(scores)), key=lambda i: -scores[i])[:k]
    return [{**ix["rows"][i], "score": scores[i]} for i in order]


def hybrid(query: str, query_vector: list[float], design: str = pipeline.CHOSEN_DESIGN, k: int = K) -> list[dict]:
    """Reciprocal Rank Fusion of the dense and BM25 top-20 lists."""
    fused, rows = {}, {}
    for ranking in (dense(query_vector, design, 20), bm25(query, design, 20)):
        for rank, row in enumerate(ranking):
            fused[row["id"]] = fused.get(row["id"], 0.0) + 1.0 / (RRF_K + rank + 1)
            rows.setdefault(row["id"], row)
    best = sorted(fused, key=lambda i: -fused[i])[:k]
    return [{**rows[i], "score": fused[i]} for i in best]


def retrieve(query: str, query_vector: list[float], design: str, method: str, k: int = K) -> list[dict]:
    if method == "dense":
        return dense(query_vector, design, k)
    if method == "hybrid":
        return hybrid(query, query_vector, design, k)
    raise ValueError(method)


def format_results(rows: list[dict]) -> str:
    """Each chunk starts with its citation id in brackets, then source and section."""
    if not rows:
        return "No matching passages in the corpus."
    blocks = []
    for r in rows:
        blocks.append(
            f"[{r['id']}] Source: {pipeline.display_name(r['source'])} FDA drug label ({r['file']}) | "
            f"Section: {r['sections']}\n{r['text']}"
        )
    return "\n\n---\n\n".join(blocks)


def search(query: str, k: int = K) -> str:
    vector = pipeline.embed_query(query)
    for attempt in range(3):
        try:
            return format_results(retrieve(query, vector, pipeline.CHOSEN_DESIGN, SEARCH_METHOD, k))
        except Exception:  # noqa: BLE001 - ChromaDB sometimes fails to open the index while
            # another process (evaluate.py) has it open: reopen it and try again.
            if attempt == 2:
                raise
            pipeline._chroma = None
            time.sleep(2)
