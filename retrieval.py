"""
Retrieval over the index built by ingest.py. Used by evaluate.py and server.py.

Three search methods, all on the same stored vectors (no extra embeddings):

    vector   cosine similarity in ChromaDB
    filter   vector search restricted to the regulation(s) the query names (metadata filter)
    hybrid   vector + BM25 keyword ranking, merged with reciprocal rank fusion

Each hit is a dict with id, doc, location, covers, title, text, words and score.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from functools import lru_cache

from ingest import collection, embed_query

METHODS = ("vector", "filter", "hybrid")

# What the server and the agent use. Phase 4 decision, by hit rate (eval/retrieval_summary.csv):
# paragraph + vector had the best hit@1 (0.556) and hit@5 (0.889) with ~930 words per search at k=5.
SERVED_DESIGN = "paragraph"
SERVED_METHOD = "vector"
DEFAULT_K = 5

# Phase 6 decision (refusal = LLM self-assessment + safety floor). Below this top-1 similarity the
# search tool reports "no relevant passages". 0.60 is under every test-set score (min 0.675), so it
# only catches clearly off-topic queries; the model decides everything else.
SIMILARITY_FLOOR = 0.60


@lru_cache(maxsize=None)
def _acts(design: str, count: int) -> tuple[str, ...]:
    got = collection(design).get(include=["metadatas"])
    return tuple(sorted({m["doc"] for m in got["metadatas"]}))


def indexed_acts(design: str = SERVED_DESIGN) -> list[str]:
    """Acts currently in the index, read from the index itself (so documents added later show up)."""
    return list(_acts(design, collection(design).count()))


def article_key(location: str) -> str:
    """'Article 33(1)-(2)' -> 'Article 33'; 'Annex III, points (4) to (5)' -> 'Annex III'; 'Art. 6' -> 'Article 6'."""
    m = re.match(r"\s*(Article|Art\.?|Annex)\s+(\d+[a-z]?|[IVXLC]+)\b", location, re.I)
    if not m:
        return location.strip()
    word = "Annex" if m.group(1).lower() == "annex" else "Article"
    return f"{word} {m.group(2).upper() if word == 'Annex' else m.group(2)}"
CANDIDATES = 50          # how many candidates each ranker contributes before fusion
RRF_K = 60               # standard reciprocal-rank-fusion constant

# Words that make a query clearly about one regulation. Used by the "filter" method.
DOC_HINTS = {
    "GDPR": [r"\bgdpr\b", r"personal data", r"data subject", r"controller", r"processor", r"data protection",
             r"\bdpo\b", r"\bdpia\b", r"data breach", r"\berasure\b", r"right to be forgotten"],
    "AI Act": [r"\bai act\b", r"\bai\b", r"artificial intelligence", r"high-risk", r"general-purpose",
               r"\bmodel\b", r"chatbot", r"deepfake", r"biometric", r"deployer", r"provider of .*ai"],
    "Data Act": [r"\bdata act\b", r"connected product", r"\biot\b", r"data holder", r"related service",
                 r"cloud", r"switching", r"data processing service", r"smart contract", r"exceptional need"],
}

STOPWORDS = set("""a an the of to in on for and or is are be by with as at from that this which it its
our we you your i can do does what when how if not no any must shall should under per""".split())


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS and len(t) > 1]


def guess_docs(query: str) -> list[str] | None:
    """Regulations the query clearly points to, or None if it points to none (then no filter)."""
    q = query.lower()
    hits = [doc for doc, patterns in DOC_HINTS.items() if any(re.search(p, q) for p in patterns)]
    return hits or None


def _hits(result: dict) -> list[dict]:
    out = []
    for i, doc_text, meta, dist in zip(result["ids"][0], result["documents"][0], result["metadatas"][0], result["distances"][0]):
        out.append({"id": i, "doc": meta["doc"], "location": meta["location"], "covers": meta["covers"],
                    "title": meta["title"], "text": doc_text, "words": meta["words"], "score": round(1 - dist, 4)})
    return out


def vector_search(query: str, design: str, k: int = 5, docs: list[str] | None = None) -> list[dict]:
    col = collection(design)
    where = {"doc": {"$in": docs}} if docs else None
    r = col.query(query_embeddings=[embed_query(query).tolist()], n_results=k, where=where,
                  include=["documents", "metadatas", "distances"])
    return _hits(r)


class BM25:
    """Okapi BM25 over every chunk of one design (k1=1.5, b=0.75)."""

    def __init__(self, ids: list[str], texts: list[str], k1: float = 1.5, b: float = 0.75):
        self.ids, self.k1, self.b = ids, k1, b
        self.docs = [Counter(tokenize(t)) for t in texts]
        self.lens = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lens) / max(len(self.lens), 1)
        df = Counter(term for d in self.docs for term in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def top(self, query: str, n: int) -> list[str]:
        terms = tokenize(query)
        scores = []
        for i, (d, length) in enumerate(zip(self.docs, self.lens)):
            s = 0.0
            for t in terms:
                if t in d:
                    tf = d[t]
                    s += self.idf[t] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * length / self.avg))
            if s > 0:
                scores.append((s, i))
        scores.sort(reverse=True)
        return [self.ids[i] for _, i in scores[:n]]


@lru_cache(maxsize=None)
def _bm25(design: str, count: int) -> BM25:
    """BM25 index for a design; rebuilt when the collection size changes (e.g. after add_document)."""
    got = collection(design).get(include=["documents"])
    return BM25(got["ids"], got["documents"])


def hybrid_search(query: str, design: str, k: int = 5) -> list[dict]:
    col = collection(design)
    dense = vector_search(query, design, k=CANDIDATES)
    sparse = _bm25(design, col.count()).top(query, CANDIDATES)
    fused: Counter = Counter()
    for rank, h in enumerate(dense):
        fused[h["id"]] += 1 / (RRF_K + rank + 1)
    for rank, i in enumerate(sparse):
        fused[i] += 1 / (RRF_K + rank + 1)
    order = [i for i, _ in fused.most_common(k)]
    by_id = {h["id"]: h for h in dense}
    missing = [i for i in order if i not in by_id]
    if missing:   # BM25-only hits: fetch their text and metadata
        got = col.get(ids=missing, include=["documents", "metadatas"])
        for i, t, m in zip(got["ids"], got["documents"], got["metadatas"]):
            by_id[i] = {"id": i, "doc": m["doc"], "location": m["location"], "covers": m["covers"],
                        "title": m["title"], "text": t, "words": m["words"], "score": None}
    return [{**by_id[i], "rrf": round(fused[i], 5)} for i in order]


def search(query: str, design: str = "paragraph", method: str = "vector", k: int = 5) -> list[dict]:
    if method == "vector":
        return vector_search(query, design, k)
    if method == "filter":
        return vector_search(query, design, k, docs=guess_docs(query))
    if method == "hybrid":
        return hybrid_search(query, design, k)
    raise ValueError(f"Unknown method {method!r}; expected one of {METHODS}")
