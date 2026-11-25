"""
Retrieval over the index built by index.py, shared by server.py and evaluate.py.

    retrieve(query, design="B_article", k=5) -> [Hit]
    format_hits(hits)                        -> text with [SOURCE, Location] citations

A retrieval design is a chunking (one Chroma collection) plus a search mode:
"dense" (cosine on Gemini embeddings) or "hybrid" (dense + BM25 fused by
reciprocal rank). Hybrid and the source filter reuse the saved vectors, so they
cost no embedding quota. Query embeddings are cached in index/query_cache.sqlite,
so the same question is never embedded twice. Logs go to stderr only.
"""

from __future__ import annotations

import json
import logging
import math
import re
import sqlite3
import unicodedata
from collections import Counter
from dataclasses import dataclass, field

import index as ix

log = logging.getLogger("rag")

QUERY_CACHE = ix.INDEX_DIR / "query_cache.sqlite"
BOE_NOTICE = ("Texto consolidado del BOE de carácter informativo; no tiene validez jurídica. "
              "Para efectos legales, consulte la publicación oficial.")

# name -> (chunking design = Chroma collection, search mode). Compared in evaluate.py.
RETRIEVAL_DESIGNS: dict[str, tuple[str, str]] = {
    "A_fixed": ("fixed", "dense"),
    "B_article": ("article", "dense"),
    "C_article_hybrid": ("article", "hybrid"),
}
SHIPPED = "B_article"        # chosen by the student from eval/retrieval_summary.csv (tasks.md 3.4)
SHIPPED_K = 5
RRF_K = 60                   # reciprocal-rank-fusion constant (Cormack et al., 2009)
CANDIDATES = 30              # how deep each ranker looks before fusion

MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
          "septiembre", "octubre", "noviembre", "diciembre"]


@dataclass
class Hit:
    id: str
    text: str
    meta: dict
    score: float
    rank: int = 0
    scores: dict = field(default_factory=dict)

    @property
    def citation(self) -> str:
        return f"[{self.meta['source']}, {self.meta['location']}]"

    def covers(self, source: str, location: str) -> bool:
        """True if this chunk is from `source` and contains `location` (fixed windows can span several)."""
        locations = self.meta.get("locations") or self.meta["location"]
        return self.meta["source"] == source and location in locations.split("; ")


def spanish_date(iso: str) -> str:
    """"2026-09-02" -> "2 de septiembre de 2026" (the date format AGENTS.md asks the agent to quote)."""
    try:
        year, month, day = (int(p) for p in iso.split("-"))
        return f"{day} de {MONTHS[month - 1]} de {year}"
    except (ValueError, IndexError):
        return iso


# --------------------------------------------------------------------------- #
# Query embeddings, cached on disk                                             #
# --------------------------------------------------------------------------- #

def _cache() -> sqlite3.Connection:
    QUERY_CACHE.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(QUERY_CACHE)
    db.execute("CREATE TABLE IF NOT EXISTS query_vectors "
               "(model TEXT, dim INTEGER, style TEXT, text TEXT, vector TEXT, PRIMARY KEY (model, dim, style, text))")
    return db


def embed_query(text: str) -> list[float]:
    """The query's vector: from the cache if this exact text was embedded before, else one API call."""
    key = (ix.EMBED_MODEL, ix.EMBED_DIM, ix.EMBED_STYLE, text)
    with _cache() as db:
        row = db.execute("SELECT vector FROM query_vectors WHERE model=? AND dim=? AND style=? AND text=?",
                         key).fetchone()
    if row:
        return json.loads(row[0])
    vector = ix.embed_texts([text], kind="query")[0]
    with _cache() as db:
        db.execute("INSERT OR REPLACE INTO query_vectors VALUES (?, ?, ?, ?, ?)", (*key, json.dumps(vector)))
    return vector


# --------------------------------------------------------------------------- #
# BM25 (lexical), built in memory from the stored chunk texts                  #
# --------------------------------------------------------------------------- #

STOPWORDS = set("""a al algo algun alguna algunas alguno algunos ante antes como con contra cual cuales cuando de del
desde donde dos el ella ellas ellos en entre era es esa esas ese eso esos esta estas este esto estos fue ha han hasta
hay la las le les lo los mas me mi mis mucho muy no nos o os otra otras otro otros para pero poco por porque que quien
se segun ser si sin sobre su sus tambien te tengo tiene tu tus un una uno unos y ya yo""".split())


def tokens(text: str) -> list[str]:
    """Lower-case, accent-free words minus stopwords: "Cotización" and "cotizacion" match."""
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return [w for w in re.findall(r"[a-z0-9]+", text) if w not in STOPWORDS and len(w) > 1]


class BM25:
    def __init__(self, ids: list[str], texts: list[str], k1: float = 1.5, b: float = 0.75):
        self.ids, self.k1, self.b = ids, k1, b
        self.docs = [Counter(tokens(t)) for t in texts]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lengths) / max(len(self.docs), 1)
        df = Counter(w for d in self.docs for w in d)
        n = len(self.docs)
        self.idf = {w: math.log(1 + (n - f + 0.5) / (f + 0.5)) for w, f in df.items()}

    def scores(self, query: str) -> list[float]:
        q = tokens(query)
        out = []
        for doc, length in zip(self.docs, self.lengths):
            s = 0.0
            for w in q:
                tf = doc.get(w, 0)
                if tf:
                    s += self.idf[w] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * length / self.avg))
            out.append(s)
        return out


_corpora: dict[str, tuple[int, dict, BM25]] = {}


def _corpus(collection) -> tuple[dict, BM25]:
    """All stored chunks of a collection ({id: (text, meta)}) and their BM25 index, rebuilt when the count changes."""
    count = collection.count()
    cached = _corpora.get(collection.name)
    if cached is None or cached[0] != count:
        got = collection.get(include=["documents", "metadatas"])
        chunks = {i: (t, m) for i, t, m in zip(got["ids"], got["documents"], got["metadatas"])}
        _corpora[collection.name] = (count, chunks, BM25(list(chunks), [t for t, _ in chunks.values()]))
    _, chunks, bm25 = _corpora[collection.name]
    return chunks, bm25


# --------------------------------------------------------------------------- #
# Retrieve                                                                     #
# --------------------------------------------------------------------------- #

def _dense(collection, query: str, n: int, where: dict | None) -> list[Hit]:
    result = collection.query(query_embeddings=[embed_query(query)], n_results=n, where=where,
                              include=["documents", "metadatas", "distances"])
    return [Hit(i, t, m, 1 - d, scores={"dense": 1 - d})
            for i, t, m, d in zip(result["ids"][0], result["documents"][0], result["metadatas"][0],
                                  result["distances"][0])]


def retrieve(query: str, design: str = SHIPPED, k: int = SHIPPED_K, sources: list[str] | None = None) -> list[Hit]:
    """Top-k chunks for `query` under a retrieval design. `sources` restricts to some documents (e.g. ["RF"])."""
    chunking, mode = RETRIEVAL_DESIGNS[design]
    collection = ix.open_collection(chunking)
    count = collection.count()
    if count == 0:
        raise RuntimeError(f"Collection {chunking!r} is empty: run `uv run python main.py index` first.")
    where = {"source": {"$in": sources}} if sources else None

    if mode == "dense":
        hits = _dense(collection, query, min(k, count), where)
    elif mode == "hybrid":
        dense = _dense(collection, query, min(CANDIDATES, count), where)
        chunks, bm25 = _corpus(collection)
        lexical = sorted(
            ((s, i) for s, i in zip(bm25.scores(query), bm25.ids)
             if s > 0 and (not sources or chunks[i][1]["source"] in sources)),
            reverse=True)[:CANDIDATES]
        fused: dict[str, Hit] = {}
        for rank, hit in enumerate(dense, 1):
            fused[hit.id] = hit
            hit.score = 1 / (RRF_K + rank)
        for rank, (s, i) in enumerate(lexical, 1):
            hit = fused.setdefault(i, Hit(i, chunks[i][0], chunks[i][1], 0.0))
            hit.score += 1 / (RRF_K + rank)
            hit.scores["bm25"] = s
        hits = sorted(fused.values(), key=lambda h: h.score, reverse=True)[:k]
    else:
        raise ValueError(f"Unknown search mode {mode!r}")

    for rank, hit in enumerate(hits, 1):
        hit.rank = rank
    return hits


def format_hits(hits: list[Hit]) -> str:
    """The search tool's output: each passage with its citation, consolidation date and BOE link."""
    if not hits:
        return "No se ha encontrado ningún fragmento.\n\n" + BOE_NOTICE
    parts = []
    for hit in hits:
        m = hit.meta
        header = (f"[{hit.rank}] Cita: {hit.citation} · {m['law_title']} · "
                  f"texto consolidado a {spanish_date(m['updated'])}")
        if m.get("path"):
            header += f"\nUbicación en la norma: {m['path']}"
        parts.append(f"{header}\n{hit.text}\nBOE: {m['url']}")
    return "\n\n---\n\n".join(parts) + "\n\n---\n\n" + BOE_NOTICE


CITATION = re.compile(r"\[([A-Z][A-Z0-9]+), ([^\[\]]+?)\]")


def citations_in(text: str) -> list[tuple[str, str]]:
    """Every [SOURCE, Location] in a text, in order, without duplicates."""
    return list(dict.fromkeys((s, loc.strip()) for s, loc in CITATION.findall(text)))
