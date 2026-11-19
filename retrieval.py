"""
Retrieval for the corpus assistant.

Three ways to search the same chunks:
  vector  meaning: the question's embedding against every chunk's embedding.
  bm25    words: classic keyword ranking (accents and plurals ignored).
  hybrid  both: the two rankings merged with reciprocal rank fusion.

compare_retrieval.py uses this now; server.py and evaluate.py will import it later.
"""

import collections
import math
import re
import unicodedata

import numpy as np

import index as ix

MODES = ("vector", "bm25", "hybrid")
RRF_K = 60  # standard constant: a chunk ranked 1st in a list adds 1/61, 2nd adds 1/62, ...

STOPWORDS = set("""a al algo ante con contra cual cuales cuando cuanto cuantos cuanta cuantas de del
desde donde el ella ellos en entre era es esta estan este esto estoy fue ha hay la las le les lo los
me mi mis muy ni no nos o para pero por que se si sin sobre su sus te tengo tiene tienen tu un una
uno unos y ya yo""".split())


def tokens(text: str) -> list[str]:
    """Lowercase words without accents, stopwords or plural endings: 'Vacaciones' -> 'vacacion'."""
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    out = []
    for word in re.findall(r"\d+(?:[.,]\d+)*|[a-z]+", text):
        if word in STOPWORDS:
            continue
        if word.isalpha():
            if len(word) > 4 and word.endswith("es"):
                word = word[:-2]
            elif len(word) > 3 and word.endswith("s"):
                word = word[:-1]
        out.append(word)
    return out


class BM25:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tf = [collections.Counter(tokens(d)) for d in docs]
        self.length = np.array([sum(t.values()) for t in self.tf], dtype=float)
        self.avg = float(self.length.mean()) if len(docs) else 1.0
        df = collections.Counter()
        for t in self.tf:
            df.update(t.keys())
        n = len(docs)
        self.idf = {w: math.log(1 + (n - d + 0.5) / (d + 0.5)) for w, d in df.items()}

    def scores(self, query: str) -> np.ndarray:
        s = np.zeros(len(self.tf))
        for word in set(tokens(query)):
            idf = self.idf.get(word)
            if idf is None:
                continue
            for i, t in enumerate(self.tf):
                f = t.get(word, 0)
                if f:
                    s[i] += idf * f * (self.k1 + 1) / (
                        f + self.k1 * (1 - self.b + self.b * self.length[i] / self.avg))
        return s


def _ranks(scores: np.ndarray) -> np.ndarray:
    """Position of each item when sorted best-first (0 = best)."""
    order = np.argsort(-scores, kind="stable")
    ranks = np.empty(len(scores), dtype=int)
    ranks[order] = np.arange(len(scores))
    return ranks


class Retriever:
    """All chunks of one design, ready to search."""

    def __init__(self, design: str):
        self.design = design
        self.chunks, self.matrix = ix.load_index(design)
        if not self.chunks:
            raise RuntimeError(f"no embedded chunks for design {design}; run `uv run python index.py` first")
        self.bm25 = BM25([c["text"] for c in self.chunks])

    def search(self, question: str, query_vector, mode: str = "vector", k: int = 5) -> list[dict]:
        """Top k chunks as {'chunk', 'score' (of this mode), 'cosine'}, best first."""
        if mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}")
        cosine = self.matrix @ np.asarray(query_vector, dtype=np.float32)
        if mode == "vector":
            score = cosine
        else:
            words = self.bm25.scores(question)
            if mode == "bm25":
                score = words
            else:  # hybrid: a chunk with no keyword match gets nothing from the keyword list
                score = 1.0 / (RRF_K + _ranks(cosine) + 1)
                score = score + np.where(words > 0, 1.0 / (RRF_K + _ranks(words) + 1), 0.0)
        order = np.argsort(-score, kind="stable")[:k]
        return [{"chunk": self.chunks[i], "score": float(score[i]), "cosine": float(cosine[i])}
                for i in order]
