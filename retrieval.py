"""
Search over the committed index, shared by server.py and evaluate.py.

Designs (all use the same saved chunk vectors; none re-embeds the corpus):
    vector          cosine similarity between the question and chunk vectors
    hybrid          vector + BM25 keyword ranking, merged by reciprocal rank fusion
    vector_filter   vector, restricted to the author(s) the question names
    hybrid_filter   hybrid, restricted the same way
    per_author      vector; when the question names two or more authors, each author is
                    searched separately and their best chunks are interleaved, so one
                    author cannot crowd out the other (added after the first results,
                    in which two-passage questions were the weak spot)

Question vectors are cached in index/query_vectors.json, so asking the same
question twice costs one embedding, not two.
"""

import json
import math
import os
import re
from collections import Counter
from pathlib import Path

import numpy as np

import index as ix

DESIGNS = ["vector", "hybrid", "vector_filter", "hybrid_filter", "per_author"]
DEFAULT_DESIGN = "per_author"  # chosen from eval/retrieval_summary.csv; see REPORT.md
DEFAULT_K = 5
QUERY_CACHE = ix.INDEX_DIR / "query_vectors.json"
CANDIDATES = 50   # how deep each ranking goes before fusion
RRF_K = 60        # standard reciprocal-rank-fusion constant

# Words in a question that name an author or work -> the author (the first word of a chunk's source).
AUTHOR_WORDS = {
    "hobbes": "hobbes", "leviathan": "hobbes",
    "locke": "locke", "second treatise": "locke",
    "mill": "mill", "on liberty": "mill",
    "wollstonecraft": "wollstonecraft", "vindication": "wollstonecraft",
}

STOPWORDS = set("""a about above after again against all am an and any are as at be because been before
being below between both but by can could did do does doing down during each few for from further had has
have having he her here hers him his how i if in into is it its itself just me more most my no nor not now
of off on once only or other our out over own same she should so some such than that the their theirs them
then there these they this those through to too under until up very was we were what when where which while
who whom why will with would you your according does say says said think thinks""".split())


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z]+", text.lower().replace("’", "'"))
    return [w[:-1] if w.endswith("s") and len(w) > 3 else w for w in words if w not in STOPWORDS]


def load_cache() -> dict:
    """Saved question vectors. A damaged file costs re-embedding, never a crash."""
    try:
        return json.loads(QUERY_CACHE.read_text())
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        try:  # keep the valid part (two processes once wrote the file at the same time)
            return json.JSONDecoder().raw_decode(QUERY_CACHE.read_text())[0]
        except json.JSONDecodeError:
            return {}


def save_cache(cache: dict) -> None:
    """Merge with what other processes saved, then replace the file in one step (atomic)."""
    merged = load_cache() | cache
    tmp = QUERY_CACHE.with_suffix(f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(merged))
    os.replace(tmp, QUERY_CACHE)


class Searcher:
    """Loads index/ once; answers searches with any design."""

    def __init__(self):
        self.collection = ix.get_collection()
        self.refresh()
        self.cache = load_cache()

    def refresh(self) -> None:
        """Reload chunks (after add_document) and rebuild the keyword index."""
        data = self.collection.get(include=["documents", "metadatas", "embeddings"])
        self.ids = data["ids"]
        self.texts = data["documents"]
        self.metas = data["metadatas"]
        self.vectors = np.asarray(data["embeddings"], dtype=np.float32)
        self.authors = np.array([m["source"].split(",")[0].lower() for m in self.metas])
        # BM25 over chunk text plus its citation, so author and chapter words count too.
        self.tokens = [tokenize(f"{m['source']} {m['chapter']} {t}") for m, t in zip(self.metas, self.texts)]
        self.lengths = np.array([len(t) for t in self.tokens], dtype=np.float32)
        self.term_freqs = [Counter(t) for t in self.tokens]
        df = Counter(word for t in self.tokens for word in set(t))
        n = len(self.tokens)
        self.idf = {w: math.log(1 + (n - d + 0.5) / (d + 0.5)) for w, d in df.items()}

    # ------------------------------------------------------------------ pieces

    def query_vector(self, query: str) -> np.ndarray:
        if query not in self.cache:
            self.cache[query] = ix.embed([query], task_type="RETRIEVAL_QUERY")[0]
            save_cache(self.cache)
        return np.asarray(self.cache[query], dtype=np.float32)

    def named_docs(self, query: str) -> set[str]:
        q = query.lower()
        return {doc for word, doc in AUTHOR_WORDS.items() if re.search(rf"\b{word}\b", q)}

    def vector_scores(self, query: str) -> np.ndarray:
        return self.vectors @ self.query_vector(query)  # vectors are normalised: dot = cosine

    def bm25_scores(self, query: str, k1: float = 1.5, b: float = 0.75) -> np.ndarray:
        avg = self.lengths.mean()
        scores = np.zeros(len(self.tokens), dtype=np.float32)
        for word in set(tokenize(query)):
            if word not in self.idf:
                continue
            tf = np.array([f.get(word, 0) for f in self.term_freqs], dtype=np.float32)
            scores += self.idf[word] * tf * (k1 + 1) / (tf + k1 * (1 - b + b * self.lengths / avg))
        return scores

    # ------------------------------------------------------------------ search

    def search(self, query: str, k: int = DEFAULT_K, design: str = DEFAULT_DESIGN) -> list[dict]:
        """Top-k chunks as dicts: id, source, location, text, score (cosine similarity)."""
        if design not in DESIGNS:
            raise ValueError(f"unknown design {design!r}; use one of {DESIGNS}")
        allowed = np.ones(len(self.ids), dtype=bool)
        if design.endswith("_filter"):
            named = self.named_docs(query)
            if named:
                allowed = np.isin(self.authors, list(named))

        cosine = self.vector_scores(query)
        named = sorted(self.named_docs(query))
        if design == "per_author" and len(named) >= 2:
            per_doc = [[i for i in np.argsort(-cosine) if self.authors[i] == doc][:k] for doc in named]
            interleaved = [i for group in zip(*per_doc) for i in group]
            ranking = interleaved[:k]
        elif design == "per_author":
            mask = np.isin(self.authors, named) if named else allowed
            ranking = [i for i in np.argsort(-cosine) if mask[i]][:k]
        elif design.startswith("vector"):
            ranking = [i for i in np.argsort(-cosine) if allowed[i]][:k]
        else:
            fused = Counter()
            keyword = self.bm25_scores(query)
            for scores in (cosine, keyword):
                ranked = [i for i in np.argsort(-scores) if allowed[i]][:CANDIDATES]
                for rank, i in enumerate(ranked):
                    fused[i] += 1 / (RRF_K + rank + 1)
            ranking = [i for i, _ in fused.most_common(k)]

        return [{
            "id": self.ids[i],
            "source": self.metas[i]["source"],
            "location": self.metas[i]["location"],
            "chapter": self.metas[i]["chapter"],
            "paragraphs": self.metas[i]["paragraphs"],
            "text": self.texts[i],
            "score": round(float(cosine[i]), 3),
        } for i in ranking]


_searcher: Searcher | None = None


def get_searcher() -> Searcher:
    global _searcher
    _searcher = _searcher or Searcher()
    return _searcher
