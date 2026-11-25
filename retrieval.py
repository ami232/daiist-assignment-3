"""
Retrieval shared by server.py (the search tool) and evaluate.py (hit rates).

Designs compared in evaluate.py. All use the same structure chunks and saved
vectors (one chunk per recital / article paragraphs / annex point), so
comparing them costs no extra embeddings; they differ in the search method:

    structure        dense (vector) search only
    structure+hybrid dense + BM25 keyword search, merged by reciprocal rank fusion
    structure+filter dense, restricted to a regulation when the query names one

SEARCH_DESIGN is the one the search tool uses: set it from the numbers in
eval/retrieval_summary.csv.
"""

from __future__ import annotations

import math
import re
from collections import Counter

import index

SEARCH_DESIGN = "structure"   # chosen from eval/retrieval_summary.csv: ties filter on hit@5 (1.0), simpler; hybrid worse
DESIGNS = ["structure", "structure+hybrid", "structure+filter"]
DEFAULT_K = 5

# --------------------------------------------------------------------------- BM25

STOPWORDS = set("""a an and are as at be by for from has have in is it its of on or shall
should that the their this to under which with where when who what whether does do
can my our we i any not no""".split())


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


class BM25:
    """Okapi BM25 over the chunks of one collection (k1=1.5, b=0.75)."""

    def __init__(self, ids: list[str], texts: list[str], k1: float = 1.5, b: float = 0.75):
        self.ids, self.k1, self.b = ids, k1, b
        self.docs = [Counter(tokenize(t)) for t in texts]
        self.lens = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lens) / max(len(self.lens), 1)
        df = Counter(term for d in self.docs for term in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def top(self, query: str, n: int) -> list[str]:
        q = tokenize(query)
        scores = []
        for i, d in enumerate(self.docs):
            s = 0.0
            for t in q:
                if t in d:
                    tf = d[t]
                    s += self.idf[t] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * self.lens[i] / self.avg))
            scores.append(s)
        order = sorted(range(len(scores)), key=lambda i: -scores[i])
        return [self.ids[i] for i in order[:n] if scores[i] > 0]


# --------------------------------------------------------------------------- store access

_store: dict[str, dict] = {}   # design base ("structure"/"fixed") -> {ids, texts, metas, bm25}


def load(base: str, refresh: bool = False) -> dict:
    """All chunks of a collection in memory (for BM25 and result lookup)."""
    if refresh or base not in _store:
        got = index.collection(base).get(include=["documents", "metadatas"])
        _store[base] = {
            "ids": got["ids"],
            "by_id": {i: (d, m) for i, d, m in zip(got["ids"], got["documents"], got["metadatas"])},
            "bm25": BM25(got["ids"], got["documents"]),
        }
    return _store[base]


def refresh() -> None:
    """Call after add_document so keyword search sees the new chunks."""
    _store.clear()


# --------------------------------------------------------------------------- search

def sources_named_in(query: str) -> list[str]:
    """Which regulations the query names explicitly (for the metadata filter)."""
    q = query.lower()
    named = []
    if re.search(r"\bai act\b|artificial intelligence act|2024/1689", q):
        named.append("AI Act")
    if re.search(r"\bgdpr\b|general data protection|2016/679", q):
        named.append("GDPR")
    if re.search(r"\bdsa\b|digital services act|2022/2065", q):
        named.append("DSA")
    return named


def dense(base: str, qvec: list[float], n: int, where: dict | None = None) -> list[str]:
    res = index.collection(base).query(query_embeddings=[qvec], n_results=n, where=where, include=[])
    return res["ids"][0]


def rrf(rankings: list[list[str]], k: int = 60) -> list[str]:
    """Reciprocal rank fusion: score = sum over rankings of 1 / (k + rank)."""
    score: Counter = Counter()
    for ranking in rankings:
        for rank, cid in enumerate(ranking, start=1):
            score[cid] += 1 / (k + rank)
    return [cid for cid, _ in score.most_common()]


def search(query: str, k: int = DEFAULT_K, design: str | None = None) -> list[dict]:
    """Top-k chunks for a query: [{id, text, source, location, title, pages, ...}]."""
    design = design or SEARCH_DESIGN
    base = "fixed" if design == "fixed" else "structure"
    qvec = index.embed_query(query)

    if design in ("fixed", "structure"):
        ids = dense(base, qvec, k)
    elif design == "structure+filter":
        named = sources_named_in(query)
        where = None if not named else ({"source": named[0]} if len(named) == 1 else {"source": {"$in": named}})
        ids = dense(base, qvec, k, where)
    elif design == "structure+hybrid":
        store = load(base)
        ids = rrf([dense(base, qvec, 20), store["bm25"].top(query, 20)])[:k]
    else:
        raise ValueError(f"unknown design {design!r}; one of {DESIGNS}")

    store = load(base)
    out = []
    for cid in ids:
        if cid not in store["by_id"]:          # added since load(): refresh once
            store = load(base, refresh=True)
        text, meta = store["by_id"][cid]
        out.append({"id": cid, "text": text, **meta})
    return out


def citation(chunk: dict) -> str:
    """The exact citation string the agent must use, e.g. "AI Act, Article 6(1)-(3)"."""
    return f"{chunk['source']}, {chunk['location']}"


def format_results(chunks: list[dict]) -> str:
    """Search results as the model sees them: a citation line, then the text."""
    if not chunks:
        return "No passages found."
    blocks = []
    for n, c in enumerate(chunks, start=1):
        pages = f"p. {c['page_start']}" if c["page_start"] == c["page_end"] else f"pp. {c['page_start']}-{c['page_end']}"
        title = f" — {c['title']}" if c.get("title") else ""
        body = c["text"].split("\n", 1)[-1]       # drop the embedded heading; the citation line replaces it
        blocks.append(f"[{n}] CITE AS: [{citation(c)}]{title} ({pages})\n{body}")
    return "\n\n".join(blocks)


# --------------------------------------------------------------------------- citations
# Shared by agent.py's citation guardrail and evaluate.py's code checks.

REFUSAL = "The corpus does not cover this question."
CITATION_RE = re.compile(r"\[([^\[\]]{3,200})\]")
CITE_AS_RE = re.compile(r"CITE AS: \[([^\[\]]+)\]")


def units(location: str) -> set[tuple[str, str]]:
    """Legal units a location refers to, at article/recital/annex level:
    "Article 6(1)-(3)" -> {("article","6")}; "Recitals 52-53" -> {("recital","52"), ("recital","53")};
    "Annex III, points 4-5" -> {("annex","III")}; "pp. 53-54" -> {("page","53"), ("page","54")}."""
    loc = location.strip()
    m = re.match(r"(?i)^recitals?\s+(\d+)(?:\s*-\s*(\d+))?", loc)
    if m:
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        return {("recital", str(n)) for n in range(a, b + 1)}
    m = re.match(r"(?i)^(?:art\.?|article)\s*(\d+[a-z]?)", loc)
    if m:
        return {("article", m.group(1))}
    m = re.match(r"(?i)^annex\s+([IVXLC]+)\b", loc)
    if m:
        return {("annex", m.group(1).upper())}
    m = re.match(r"(?i)^pp?\.\s*(\d+)(?:\s*-\s*(\d+))?", loc)
    if m:
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        return {("page", str(n)) for n in range(a, b + 1)}
    return {("other", loc.lower())}


def parse_citation(text: str, sources: set[str]) -> tuple[str, str] | None:
    """"AI Act, Article 6(3)" -> ("AI Act", "Article 6(3)") if the source is known."""
    for src in sorted(sources, key=len, reverse=True):
        if text.lower().startswith(src.lower()):
            rest = text[len(src):].lstrip(" ,—-:")
            return (src, rest) if rest else None
    return None


def cited(answer: str, sources: set[str]) -> list[tuple[str, str]]:
    """All (source, location) citations in an answer. A bracket may hold several,
    separated by ';'. Brackets that don't start with a known source are ignored."""
    out = []
    for m in CITATION_RE.finditer(answer):
        for part in m.group(1).split(";"):
            c = parse_citation(part.strip(), sources)
            if c:
                out.append(c)
    return out


def citation_valid(c: tuple[str, str], retrieved: list[tuple[str, str]]) -> bool:
    """A citation is valid if some retrieved passage has the same source and
    covers the same article/recital/annex (paragraph-level detail may differ)."""
    return any(c[0] == r[0] and units(c[1]) & units(r[1]) for r in retrieved)


def retrieved_citations(tool_outputs: list[str]) -> list[tuple[str, str]]:
    """Citations the search tool actually returned, parsed from its output."""
    return [tuple(x.split(", ", 1)) for out in tool_outputs for x in CITE_AS_RE.findall(out) if ", " in x]


def is_refusal(answer: str) -> bool:
    return answer.strip().lower().startswith(REFUSAL.lower().rstrip("."))


def known_sources() -> set[str]:
    return {m["source"] for _, (_, m) in load("structure")["by_id"].items()}
