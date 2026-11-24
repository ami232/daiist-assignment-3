"""
Retrieval over the stored index, shared by server.py (the search tool) and evaluate.py
(hit rate per design), so both measure exactly the same search.

Two methods over any chunking design:
- "vector": cosine similarity between the query vector and the chunk vectors (ChromaDB).
- "hybrid": the vector ranking fused with a BM25 keyword ranking by reciprocal rank
  (RRF). Keyword search costs no embeddings, and legal questions often hinge on exact
  terms ("Gran Reserva", "1,2 mm", "artículo 31").
"""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter

import config

STOPWORDS = set(
    "a al algo algun alguna algunas alguno algunos ante antes como con contra cual cuales cuando de del desde "
    "donde dos el ella ellas ellos en entre era es esa esas ese eso esos esta estas este esto estos fue ha han "
    "hasta la las le les lo los mas me mi mis mucho muy ni no nos o os otra otras otro otros para pero poco por "
    "porque que quien se sea segun ser si sin sobre su sus tambien tanto te tiene tienen todo todos tu tus un una "
    "uno unos y ya puedo puede debe deben tengo tiene cuanto cuanta cuantos cuantas que".split()
)


def tokenize(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return [t for t in re.findall(r"[a-z0-9]+(?:[.,][0-9]+)?", text) if t not in STOPWORDS and len(t) > 1]


class BM25:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.docs = [Counter(tokenize(d)) for d in docs]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lengths) / max(len(self.lengths), 1)
        df = Counter(t for d in self.docs for t in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def scores(self, query: str) -> list[float]:
        terms = tokenize(query)
        out = []
        for d, length in zip(self.docs, self.lengths):
            s = 0.0
            for t in terms:
                if t in d:
                    tf = d[t]
                    s += self.idf[t] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * length / self.avg))
            out.append(s)
        return out


class Retriever:
    """Search one design's ChromaDB collection by vector, or by vector + BM25."""

    def __init__(self, design: str = config.CHOSEN_DESIGN, method: str = config.CHOSEN_METHOD,
                 sources: list[str] | None = None):
        """`sources` limits the search to some documents (evaluate.py compares the designs on the
        base corpus only, so a document added later through add_document cannot move the numbers)."""
        from index import get_collection

        self.design, self.method, self.sources = design, method, sources
        self.collection = get_collection(design)
        self.reload()

    def reload(self) -> None:
        """Re-read every chunk (after add_document) for keyword search."""
        data = self.collection.get(include=["documents", "metadatas"], where=self._where())
        self.ids, self.texts, self.metas = data["ids"], data["documents"], data["metadatas"]
        self.position = {i: n for n, i in enumerate(self.ids)}
        self.bm25 = BM25(self.texts) if self.method == "hybrid" and self.texts else None

    def search(self, query: str, vector: list[float], k: int = config.TOP_K) -> list[dict]:
        pool = max(k, 30) if self.method == "hybrid" else k
        result = self.collection.query(query_embeddings=[vector], n_results=min(pool, len(self.ids)),
                                       include=["documents", "metadatas", "distances"], where=self._where())
        vector_ids = result["ids"][0]
        if self.method == "vector":
            return [self._hit(i, rank, 1 - d) for rank, (i, d) in enumerate(zip(vector_ids, result["distances"][0]), 1)][:k]

        # Reciprocal rank fusion: score = sum over rankings of 1 / (60 + rank).
        keyword = self.bm25.scores(query)
        keyword_ids = [self.ids[n] for n in sorted(range(len(keyword)), key=lambda n: -keyword[n])[:pool] if keyword[n] > 0]
        fused: dict[str, float] = {}
        for ranking in (vector_ids, keyword_ids):
            for rank, i in enumerate(ranking, 1):
                fused[i] = fused.get(i, 0.0) + 1 / (60 + rank)
        best = sorted(fused, key=lambda i: -fused[i])[:k]
        return [self._hit(i, rank, fused[i]) for rank, i in enumerate(best, 1)]

    def _where(self) -> dict | None:
        return {"source": {"$in": self.sources}} if self.sources else None

    def _hit(self, chunk_id: str, rank: int, score: float) -> dict:
        n = self.position[chunk_id]
        return {"id": chunk_id, "rank": rank, "score": round(float(score), 4), "text": self.texts[n], **self.metas[n]}


def citation(hit: dict) -> str:
    """The citation format the agent must copy: [source, location]."""
    return f"[{hit['source']}, {hit['location']}]"


def format_results(hits: list[dict]) -> str:
    """What the search tool returns to the model: each chunk with its citation."""
    if not hits:
        return "No results."
    blocks = []
    for h in hits:
        blocks.append(
            f"Result {h['rank']} | cite as {citation(h)} | {h['title']}, page {h['page']}\n{h['text']}"
        )
    return "\n\n---\n\n".join(blocks)


def location_matches(found: str, expected: str) -> bool:
    """'Sección 3.c.1' answers 'Sección 3.c'; 'Anexo III, Parte A' answers 'Anexo III'."""
    found, expected = found.strip(), expected.strip()
    return found == expected or found.startswith(expected + ".") or found.startswith(expected + ",")


def hit_matches(hit: dict, source: str, location: str) -> bool:
    """A chunk answers (source, location) if it is from that document and covers that unit.
    Fixed-size windows can straddle units, so every unit a chunk touches counts."""
    if hit["source"] != source:
        return False
    return any(location_matches(loc, location) for loc in str(hit.get("locations", hit["location"])).split("|"))
