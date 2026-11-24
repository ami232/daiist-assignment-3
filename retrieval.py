"""
Retrieval over the 10-K index, shared by server.py, agent.py and evaluate.py.

Two designs, same chunks and same vectors (design C costs no extra embeddings):

- "plain"  (design B): structure-based chunks, nearest neighbours over the whole corpus.
- "filter" (design C): same chunks, but if the question names a company the search
  is restricted to that company's chunks. If it names two or more (a comparison),
  each company is searched on its own and the results are interleaved, so one
  company cannot crowd the other out of the top k.
"""

from __future__ import annotations

import os
import re

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

import index  # noqa: E402

# Chosen by the numbers (eval/retrieval_summary.csv): "plain" ties "filter" at
# hit@5 (0.92) and beats it at hit@3 (0.85 vs 0.81), and it is simpler. The
# company header on every chunk already steers the search to the right report.
DEFAULT_DESIGN = "plain"
DEFAULT_K = 5

COMPANY_PATTERNS = {
    "Tesla": r"\btesla\b|\bcybertruck\b|\bmodel [3sxy]\b|\boptimus\b|\bmegapack\b|\bpowerwall\b|\bgigafactor",
    "Ford": r"\bford\b|\blincoln\b|\bf-150\b|\bmustang\b|\bblueoval\b|\bmodel e\b|\bford pro\b",
    "GM": r"\bgm\b|\bgeneral motors\b|\bchevrolet\b|\bchevy\b|\bcadillac\b|\bbuick\b|\bgmc\b|\bcruise\b|\bultium\b",
}

_collection = None


def collection():
    global _collection
    if _collection is None:
        _collection = index.get_collection()
    return _collection


def detect_companies(query: str) -> list[str]:
    """Companies the question names, in a fixed order."""
    return [name for name, pattern in COMPANY_PATTERNS.items() if re.search(pattern, query, re.I)]


def embed_query(query: str) -> list[float]:
    return index.embed_texts([query], task_type="RETRIEVAL_QUERY")[0]


def _query(vector: list[float], k: int, where: dict | None) -> list[dict]:
    result = collection().query(query_embeddings=[vector], n_results=k, where=where)
    return [
        {"id": i, "text": d, "metadata": m, "distance": dist}
        for i, d, m, dist in zip(result["ids"][0], result["documents"][0], result["metadatas"][0], result["distances"][0])
    ]


def retrieve(query: str, k: int = DEFAULT_K, design: str = DEFAULT_DESIGN, vector: list[float] | None = None) -> list[dict]:
    """Top-k chunks for a question. Pass `vector` to reuse a saved query embedding."""
    vector = vector if vector is not None else embed_query(query)
    companies = detect_companies(query) if design == "filter" else []
    if not companies:
        return _query(vector, k, None)
    if len(companies) == 1:
        return _query(vector, k, {"company": companies[0]})
    per_company = [_query(vector, k, {"company": c}) for c in companies]
    merged, seen = [], set()
    for rank in range(k):
        for hits in per_company:
            if rank < len(hits) and hits[rank]["id"] not in seen:
                merged.append(hits[rank])
                seen.add(hits[rank]["id"])
    return merged[:k]


def citation(metadata: dict) -> str:
    return f"[{metadata['source']}, {metadata['location']}]"


def format_hits(hits: list[dict]) -> str:
    """Search results as text the model reads: a citation line, then the passage."""
    if not hits:
        return "No passages found."
    blocks = []
    for n, hit in enumerate(hits, 1):
        m = hit["metadata"]
        blocks.append(
            f"Result {n} {citation(m)} {m['company']} | {m['item']}. {m['item_title']} | {m['section']}\n"
            f"{hit['text'].split(chr(10), 1)[-1]}"
        )
    return "\n\n---\n\n".join(blocks)
