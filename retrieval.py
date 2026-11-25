"""
Retrieval over the committed index: vector, BM25, hybrid (reciprocal rank fusion), and an optional
metadata filter that routes a query to the documents its identifiers or names point to.
Also the citation checker used by the harness guardrail and by the evaluation.

Imported by server.py, agent.py and evaluate.py. Logs to stderr only.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

import numpy as np

import index

METHODS = ("vector", "bm25", "hybrid")
RRF_K = 60

# The configuration the search tool serves. Set from the retrieval comparison in evaluate.py.
CHOSEN = {"design": index.DEFAULT_DESIGN, "method": "hybrid", "use_route": True, "k": 5}

# ---------------------------------------------------------------- tokenising (keeps IDs whole)
TOKEN = re.compile(r"[A-Za-z]+(?:[.\-][A-Za-z0-9]+)+|[A-Za-z]+|\d+(?:\.\d+)*")
STOPWORDS = set("""a an and are as at be by does do for from has have how in is it its of on or that the this
to was what when which who why with what's does say says""".split())


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN.findall(text) if t.lower() not in STOPWORDS]


# ---------------------------------------------------------------- routing filter
ROUTES = [
    (re.compile(r"\b(?:GV|MP|MS|MG)-\d+\.\d+-\d{3}\b"), ["NIST.AI.600-1"]),
    (re.compile(r"\b(?:GOVERN|MAP|MEASURE|MANAGE) \d+(?:\.\d+)?\b"), ["NIST.AI.100-1", "NIST.AI.600-1"]),
    (re.compile(r"\b(?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2}(?:-\d{2})?\b"), ["NIST.SP.800-61r3", "NIST.CSWP.29"]),
    (re.compile(r"\b(?:PO|PS|PW|RV)\.\d+(?:\.\d+)?\b"), ["NIST.SP.800-218"]),
    (re.compile(r"\bSSDF\b|secure software development framework|800-218", re.I), ["NIST.SP.800-218"]),
    (re.compile(r"generative ai profile|\bGAI\b|600-1", re.I), ["NIST.AI.600-1"]),
    (re.compile(r"incident response profile|800-61", re.I), ["NIST.SP.800-61r3"]),
    (re.compile(r"\bAI RMF\b|AI risk management framework|100-1", re.I), ["NIST.AI.100-1"]),
    (re.compile(r"\bCSF\b|cybersecurity framework", re.I), ["NIST.SP.800-61r3", "NIST.CSWP.29"]),
]


def route(query: str) -> list[str]:
    """Documents a query explicitly points to (identifier format or document name); [] = no filter."""
    docs: list[str] = []
    for pattern, targets in ROUTES:
        if pattern.search(query):
            docs += [t for t in targets if t not in docs]
    return docs


# ---------------------------------------------------------------- retriever
@dataclass
class Hit:
    chunk_id: str
    text: str
    meta: dict
    score: float
    rank: int


class Retriever:
    """Loads one design's chunks from ChromaDB into memory (a few hundred rows) and searches them."""

    def __init__(self, design: str = index.DEFAULT_DESIGN, only_docs: list[str] | None = None):
        self.design = design
        self.only_docs = only_docs  # load just these documents (the retrieval evaluation uses the original four)
        self.reload()

    def reload(self) -> None:
        try:
            got = index.get_collection(self.design).get(include=["documents", "metadatas", "embeddings"])
        except Exception:  # stale client after another process wrote to the store: reopen it
            got = index.get_collection(self.design, fresh=True).get(include=["documents", "metadatas", "embeddings"])
        if self.only_docs:
            keep = [i for i, m in enumerate(got["metadatas"]) if m["doc_id"] in self.only_docs]
            got = {f: [got[f][i] for i in keep] for f in ("ids", "documents", "metadatas", "embeddings")}
        self.ids: list[str] = got["ids"]
        self.texts: list[str] = got["documents"]
        self.metas: list[dict] = got["metadatas"]
        self.by_id = {cid: i for i, cid in enumerate(self.ids)}
        if self.ids:
            m = np.asarray(got["embeddings"], dtype=np.float32)
            self.matrix = m / np.linalg.norm(m, axis=1, keepdims=True)
        else:
            self.matrix = np.zeros((0, 1), dtype=np.float32)
        # BM25 statistics; titles and identifiers are added so a document name or ID matches its chunks
        self.tokens = [tokenize(f"{m['doc_title']} {m['identifiers'].replace(';', ' ')} {t}")
                       for t, m in zip(self.texts, self.metas)]
        self.tf = [Counter(t) for t in self.tokens]
        self.lengths = np.array([len(t) for t in self.tokens], dtype=np.float32)
        self.avg_len = float(self.lengths.mean()) if len(self.lengths) else 1.0
        df = Counter(tok for toks in self.tokens for tok in set(toks))
        n = len(self.tokens)
        self.idf = {tok: math.log(1 + (n - d + 0.5) / (d + 0.5)) for tok, d in df.items()}

    def __len__(self) -> int:
        return len(self.ids)

    # -- scorers return a score per chunk (higher is better)
    def _vector_scores(self, query: str) -> np.ndarray:
        q = index.embed_query(query).astype(np.float32)
        return self.matrix @ (q / np.linalg.norm(q))

    def _bm25_scores(self, query: str, k1: float = 1.5, b: float = 0.75) -> np.ndarray:
        scores = np.zeros(len(self.ids), dtype=np.float32)
        for tok in set(tokenize(query)):
            idf = self.idf.get(tok)
            if idf is None:
                continue
            for i, tf in enumerate(self.tf):
                f = tf.get(tok)
                if f:
                    scores[i] += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * self.lengths[i] / self.avg_len))
        return scores

    def search(self, query: str, k: int = 5, method: str = "hybrid",
               doc_ids: list[str] | None = None, use_route: bool = False) -> list[Hit]:
        if method not in METHODS:
            raise ValueError(f"method must be one of {METHODS}")
        if not self.ids:
            return []
        allowed = doc_ids or (route(query) if use_route else [])
        mask = np.array([not allowed or m["doc_id"] in allowed for m in self.metas])
        if not mask.any():  # routed to a document that is not indexed: search everything
            mask[:] = True

        if method == "vector":
            scores = self._vector_scores(query)
        elif method == "bm25":
            scores = self._bm25_scores(query)
        else:
            fused = np.zeros(len(self.ids), dtype=np.float32)
            for s in (self._vector_scores(query), self._bm25_scores(query)):
                s = np.where(mask, s, -np.inf)
                for r, i in enumerate(np.argsort(-s)):
                    fused[i] += 1.0 / (RRF_K + r + 1)
            scores = fused
        scores = np.where(mask, scores, -np.inf)
        order = [i for i in np.argsort(-scores) if np.isfinite(scores[i])][:k]
        return [Hit(self.ids[i], self.texts[i], self.metas[i], float(scores[i]), r + 1) for r, i in enumerate(order)]


# ---------------------------------------------------------------- formatting and citations
def page_ref(meta: dict) -> str:
    a, b = meta["page_start"], meta["page_end"]
    return f"p{a}" if a == b else f"p{a}-{b}"


def format_hits(hits: list[Hit]) -> str:
    """What the search tool returns: each passage with its citation and metadata."""
    if not hits:
        return "No passages found. The index may be empty."
    out = []
    for h in hits:
        m = h.meta
        ids = m["identifiers"].replace(";", ", ")
        cite = f"[{m['doc_id']}, {page_ref(m)}]"
        lines = [
            f"--- Result {h.rank} | chunk_id: {h.chunk_id}",
            f"Document: {m['doc_title']} (doc_id {m['doc_id']}, version {m['doc_version']})",
            f"Location: PDF {page_ref(m)} (printed page {m['page_label']})"
            + (f" | section: {m['section']}" if m["section"] else ""),
            f"Identifiers in this passage: {ids}" if ids else "Identifiers in this passage: none",
            f"Cite as: {cite}" + (f" or [{m['doc_id']}, <identifier from the list above>]" if ids else ""),
            "Text:",
            h.text,
        ]
        out.append("\n".join(lines))
    return "\n\n".join(out)


CITATION = re.compile(r"\[\s*([A-Za-z0-9.\-]+)\s*,\s*([^\[\]]+?)\s*\]")
PAGES = re.compile(r"^p\.?\s*(\d+)(?:\s*[-–]\s*p?\.?\s*(\d+))?$", re.I)
CHUNK_ID = re.compile(r"chunk_id: (\S+)")
REFUSAL = "I don't know based on the indexed documents."


def is_refusal(answer: str) -> bool:
    """The fixed refusal sentence, tolerating typographic apostrophes, case and the final period."""
    norm = answer.strip().replace("’", "'").replace("*", "").lower()
    return norm.startswith(REFUSAL.lower().rstrip("."))


def retrieved_chunk_ids(tool_outputs: list[str]) -> list[str]:
    return list(dict.fromkeys(cid for t in tool_outputs for cid in CHUNK_ID.findall(t)))


def citation_supported(doc_id: str, location: str, metas: list[dict], texts: list[str]) -> bool:
    """A citation is valid if some retrieved chunk has this doc_id and the location is one of its
    identifiers, appears in its text, or is a PDF page range overlapping it."""
    loc = location.strip()
    pm = PAGES.match(loc)
    for m, t in zip(metas, texts):
        if m["doc_id"] != doc_id:
            continue
        if pm:
            a = int(pm.group(1))
            b = int(pm.group(2) or a)
            if a <= m["page_end"] and b >= m["page_start"]:
                return True
        elif loc in m["identifiers"].split(";") or re.search(rf"(?<![\w.]){re.escape(loc)}(?![\w-])", t):
            return True
    return False


def check_citations(answer: str, chunk_ids: list[str], retriever: Retriever) -> dict:
    """Code check of an answer against the chunks actually retrieved in that run."""
    rows = [retriever.by_id[c] for c in chunk_ids if c in retriever.by_id]
    metas = [retriever.metas[i] for i in rows]
    texts = [retriever.texts[i] for i in rows]
    known_docs = set(index.DOCS) | {m["doc_id"] for m in retriever.metas}
    cites = [(d, l) for d, l in CITATION.findall(answer) if d in known_docs]
    # One citation may list several locations: [NIST.SP.800-218, PS.2, PS.2.1] -> each must hold.
    invalid = [f"[{d}, {l}]" for d, l in cites
               if not all(citation_supported(d, part, metas, texts) for part in re.split(r"[;,]", l) if part.strip())]
    return {
        "refusal": is_refusal(answer),
        "n_citations": len(cites),
        "invalid": invalid,
        "cited_docs": sorted({d for d, _ in cites}),
    }
