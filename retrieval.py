"""
Search over the index built by index.py. Used by server.py (the search tool) and evaluate.py.

Three search methods over either chunking (see index.DESIGNS):
  - dense:   cosine similarity between Gemini embeddings of question and chunk (ChromaDB);
  - keyword: BM25, a classic keyword score (exact words, numbers and section codes);
  - hybrid:  both lists merged with reciprocal rank fusion (RRF).

Question embeddings are cached in index/query_cache.json, so the same question is
never embedded twice (each embedding counts against the Gemini quota).
"""

from __future__ import annotations

import json
import math
import os
import re
from collections import Counter

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")  # keep ChromaDB quiet

import index as ix

# The design server.py serves, chosen from eval/retrieval.csv (31 answerable questions):
# sections/dense had the best hit rate at every k (84% at 1, 100% at 3 and 5) and found
# both passages of 75% of multi questions in the top 5. Keyword search was weak (36% at 1)
# and pulled hybrid down to 52% at 1. k = 5 rather than 3 for the multi questions.
CHOSEN_CHUNKING = "sections"
CHOSEN_METHOD = "dense"
TOP_K = 5

METHODS = ("dense", "keyword", "hybrid")
CANDIDATES = 30  # how deep each list goes before hybrid fuses them
RRF_K = 60  # standard constant of reciprocal rank fusion

QUERY_CACHE = ix.INDEX_DIR / "query_cache.json"

STOPWORDS = set(
    """a an and are as at be by can do does for from has have how i if in into is it its may must
    of on or our should so that the their them then there these this to under we what when where
    which who will with without you your shall not no""".split()
)


# --------------------------------------------------------------------------- query embeddings

def _load_cache() -> dict[str, list[float]]:
    try:
        return json.loads(QUERY_CACHE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def embed_query(question: str) -> list[float]:
    """Embed a question in gemini-embedding-2's query format, with a disk cache."""
    cache = _load_cache()
    if question in cache:
        return cache[question]
    vector = ix.embed_texts([f"task: search result | query: {question}"])[0]
    cache = _load_cache()  # re-read: another process may have added entries meanwhile
    cache[question] = vector
    tmp = QUERY_CACHE.with_suffix(".tmp")
    tmp.write_text(json.dumps(cache))
    tmp.replace(QUERY_CACHE)  # atomic, so a reader never sees a half-written file
    return vector


# --------------------------------------------------------------------------- BM25

def tokenize(text: str) -> list[str]:
    """Lower-case words, numbers and Food Code section codes; '57°C' -> ['57', 'c']."""
    text = text.lower().replace("°", " ")
    tokens = re.findall(r"\d-\d{3}\.\d{2,3}|\d+(?:\.\d+)?|[a-z]+", text)
    return [stem(t) for t in tokens if t not in STOPWORDS]


def stem(word: str) -> str:
    """A very small stemmer, so 'cooling', 'cooled' and 'cools' all become 'cool'."""
    if not word.isalpha() or len(word) <= 4:
        return word
    for suffix in ("ations", "ation", "ings", "ing", "edly", "ed", "ies", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)] + ("y" if suffix == "ies" else "")
    return word


class BM25:
    def __init__(self, texts: list[str], k1: float = 1.5, b: float = 0.75):
        self.docs = [Counter(tokenize(t)) for t in texts]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lengths) / max(len(self.docs), 1)
        df = Counter(term for d in self.docs for term in d)
        n = len(self.docs)
        self.idf = {term: math.log(1 + (n - f + 0.5) / (f + 0.5)) for term, f in df.items()}
        self.k1, self.b = k1, b

    def scores(self, query: str) -> list[float]:
        terms = tokenize(query)
        out = []
        for doc, length in zip(self.docs, self.lengths):
            s = 0.0
            for term in terms:
                f = doc.get(term)
                if f:
                    s += self.idf[term] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * length / self.avg))
            out.append(s)
        return out


# --------------------------------------------------------------------------- retriever

class Retriever:
    """All chunks of one chunking design, searchable by dense, keyword or hybrid."""

    def __init__(self, chunking: str = CHOSEN_CHUNKING, sources: list[str] | None = None):
        self.chunking = chunking
        self.collection = ix.open_collection(chunking)
        # Optionally search only some documents (evaluate.py compares designs on the original corpus).
        self.where = {"source": {"$in": sources}} if sources else None
        self.reload()

    def reload(self) -> None:
        """Read every chunk from ChromaDB and rebuild the keyword index (after add_document)."""
        data = self.collection.get(where=self.where, include=["documents", "metadatas"])
        self.ids = data["ids"]
        self.texts = data["documents"]
        self.metas = data["metadatas"]
        self.position = {chunk_id: i for i, chunk_id in enumerate(self.ids)}
        # Keyword search sees the heading too, like the embedding's "title:".
        self.bm25 = BM25([f"{m['heading']} {m['cite']} {t}" for m, t in zip(self.metas, self.texts)])

    def __len__(self) -> int:
        return len(self.ids)

    def _hit(self, i: int, score: float) -> dict:
        return {"id": self.ids[i], "text": self.texts[i], "score": round(score, 4), **self.metas[i]}

    def dense(self, query_vector: list[float], k: int) -> list[dict]:
        result = self.collection.query(query_embeddings=[query_vector], n_results=min(k, len(self)), where=self.where)
        return [
            self._hit(self.position[chunk_id], 1 - distance)  # ChromaDB gives distance = 1 - cosine
            for chunk_id, distance in zip(result["ids"][0], result["distances"][0])
        ]

    def keyword(self, query: str, k: int) -> list[dict]:
        scores = self.bm25.scores(query)
        best = sorted(range(len(scores)), key=lambda i: -scores[i])[:k]
        return [self._hit(i, scores[i]) for i in best if scores[i] > 0]

    def hybrid(self, query: str, query_vector: list[float], k: int) -> list[dict]:
        """Reciprocal rank fusion: a chunk scores 1/(60 + rank) in each list it appears in."""
        fused: dict[str, float] = {}
        for ranked in (self.dense(query_vector, CANDIDATES), self.keyword(query, CANDIDATES)):
            for rank, hit in enumerate(ranked, start=1):
                fused[hit["id"]] = fused.get(hit["id"], 0.0) + 1 / (RRF_K + rank)
        best = sorted(fused, key=lambda chunk_id: -fused[chunk_id])[:k]
        return [self._hit(self.position[chunk_id], fused[chunk_id]) for chunk_id in best]

    def search(self, query: str, method: str = CHOSEN_METHOD, k: int = TOP_K, query_vector=None) -> list[dict]:
        if method == "keyword":
            return self.keyword(query, k)
        vector = query_vector if query_vector is not None else embed_query(query)
        if method == "dense":
            return self.dense(vector, k)
        if method == "hybrid":
            return self.hybrid(query, vector, k)
        raise ValueError(f"Unknown method {method!r}; use one of {METHODS}.")


def format_hits(query: str, hits: list[dict]) -> str:
    """The text the search tool returns: one numbered block per chunk, with the label to cite."""
    if not hits:
        return f'No passages found for "{query}". The documents may not cover this.'
    blocks = [f'{len(hits)} passages for "{query}". Cite each fact with the label in square brackets.']
    for n, hit in enumerate(hits, start=1):
        blocks.append(
            f"[{n}] Cite as: [{hit['cite']}]\n"
            f"Source: {hit['document']}, {hit['location']}. {hit['heading']}\n"
            f"{hit['text']}"
        )
    return "\n\n".join(blocks)


CITE_RE = re.compile(r"\[([^\[\]]+?(?:§\s?\d-\d{3}\.\d{2,3}|p\.\s?\d+))\]")


def normalize_cite(label: str) -> str:
    """'Food Code 2026 § 3-501.17' -> 'Food Code 2026 §3-501.17'; 'p.14' -> 'p. 14'."""
    label = re.sub(r"\s+", " ", label).strip()
    label = re.sub(r"§\s+", "§", label)
    return re.sub(r"\bp\.\s*(\d)", r"p. \1", label)


def cites_in(text: str) -> list[str]:
    """Every citation label in an answer, e.g. ['Food Code 2026 §3-501.17', 'Cooling Guide p. 1']."""
    return [normalize_cite(c) for c in CITE_RE.findall(text)]


def cites_offered(tool_output: str) -> list[str]:
    """Labels the search tool offered: the lines 'Cite as: [...]'."""
    return [normalize_cite(c) for c in re.findall(r"Cite as: \[([^\]]+)\]", tool_output)]
