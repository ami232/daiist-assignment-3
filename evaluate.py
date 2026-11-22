"""
Assignment 3: evaluation (`main.py evaluate`).

Stage 1 (this file, so far): retrieval hit rate at k = 1, 3, 5 per retrieval design,
scored with the rule in eval/scoring_rule.md (fixed before any measurement).

Designs compared (every design that has an index in index/ is tried):
  dense_<design>   vector search only (Gemini embeddings in ChromaDB)
  hybrid_<design>  vector search + BM25 keyword search, merged with reciprocal rank fusion

All tuning constants are set below, before the first run, and are not changed afterwards.

Writes: eval/retrieval_results.csv (one row per question and design)
        eval/retrieval_summary.json (the table that goes into REPORT.md)
"""

import csv
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import index

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
QUERY_CACHE = EVAL_DIR / "query_cache.json"      # query vectors, so a re-run costs no quota (not committed)
RESULTS_CSV = EVAL_DIR / "retrieval_results.csv"
SUMMARY_JSON = EVAL_DIR / "retrieval_summary.json"

KS = (1, 3, 5)
POOL = 30                 # candidates taken from each ranking before fusion
RRF_K = 60                # reciprocal rank fusion constant
BM25_K1, BM25_B = 1.5, 0.75
STOPWORDS = set(
    "a an and are as at be but by for from has have how i if in is it its my of on or our so that the their "
    "them then there these they this to us was we what when where which who will with you your do does can "
    "should must".split()
)


# --------------------------------------------------------------------------
# 1. Labels and the scoring rule
# --------------------------------------------------------------------------

def parse_required(row: dict) -> list[tuple[str, str]]:
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    labels = [s.strip() for s in row["expected_location"].split(";") if s.strip()]
    if len(sources) != len(labels):
        raise SystemExit(f"{row['id']}: expected_source and expected_location must list the same number of passages.")
    return list(zip(sources, labels))


def parse_equivalents(row: dict) -> list[tuple[int | None, str, str, bool]]:
    """`[N>][=]source:label`, `;` between several. N = which required passage it stands in for (1-based)."""
    out = []
    for item in (row.get("equivalent_locations") or "").split(";"):
        item = item.strip()
        if not item:
            continue
        m = re.match(r"^(?:(\d+)>)?(=)?([^:]+):(.+)$", item)
        if not m:
            raise SystemExit(f"{row['id']}: cannot read equivalent location {item!r}.")
        number, exact, source, label = m.groups()
        out.append((int(number) if number else None, source.strip(), label.strip(), bool(exact)))
    return out


def matches(chunk: dict, source: str, label: str, exact: bool = False) -> bool:
    """Same document, and the chunk's section is the label or (unless exact) a sub-section of it."""
    if chunk["source"] != source:
        return False
    return chunk["section"] == label or (not exact and chunk["section"].startswith(label + "."))


def outcome(row: dict, ranked: list[dict], k: int) -> str:
    """hit / equivalent / miss for one answerable question, from the top k chunks."""
    top = ranked[:k]
    required, equivalents = parse_required(row), parse_equivalents(row)
    used: set[int] = set()                        # one chunk covers at most one required passage
    covered = [False] * len(required)
    via_equivalent = [False] * len(required)
    for i, (source, label) in enumerate(required):
        for j, chunk in enumerate(top):
            if j not in used and matches(chunk, source, label):
                covered[i] = True
                used.add(j)
                break
    for i in range(len(required)):
        if covered[i]:
            continue
        for number, source, label, exact in equivalents:
            if number not in (None, i + 1):
                continue
            for j, chunk in enumerate(top):
                if j not in used and matches(chunk, source, label, exact):
                    covered[i] = via_equivalent[i] = True
                    used.add(j)
                    break
            if covered[i]:
                break
    if not all(covered):
        return "miss"
    return "equivalent" if any(via_equivalent) else "hit"


# --------------------------------------------------------------------------
# 2. Chunks, BM25, dense search, fusion
# --------------------------------------------------------------------------

def indexed_designs() -> list[str]:
    import chromadb
    from chromadb.config import Settings

    client = chromadb.PersistentClient(path=str(index.INDEX_DIR), settings=Settings(anonymized_telemetry=False))
    names = {c if isinstance(c, str) else c.name for c in client.list_collections()}
    found = []
    for design in index.DESIGNS:
        if f"chunks_{design}" in names and client.get_collection(f"chunks_{design}").count() > 0:
            found.append(design)
    return found


def load_chunks(design: str) -> dict[str, dict]:
    data = index.get_collection(design).get(include=["documents", "metadatas"])
    chunks = {}
    for id_, text, meta in zip(data["ids"], data["documents"], data["metadatas"]):
        chunks[id_] = {"id": id_, "text": text, **meta}
    return chunks


def tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


class BM25:
    def __init__(self, chunks: dict[str, dict]):
        self.ids = list(chunks)
        # The heading and location are searchable too, as they are in the embedded text.
        self.docs = [Counter(tokens(f"{c['title']} {c['location']} {c['heading']} {c['text']}")) for c in chunks.values()]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lengths) / len(self.lengths)
        df = Counter(t for d in self.docs for t in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def rank(self, query: str, pool: int) -> list[str]:
        q = tokens(query)
        scores = []
        for i, doc in enumerate(self.docs):
            s = 0.0
            for t in q:
                f = doc.get(t, 0)
                if f:
                    s += self.idf[t] * f * (BM25_K1 + 1) / (f + BM25_K1 * (1 - BM25_B + BM25_B * self.lengths[i] / self.avg))
            scores.append(s)
        order = sorted(range(len(scores)), key=lambda i: -scores[i])
        return [self.ids[i] for i in order[:pool] if scores[i] > 0]


def dense_rank(design: str, vector: list[float], pool: int) -> list[str]:
    collection = index.get_collection(design)
    return collection.query(query_embeddings=[vector], n_results=min(pool, collection.count()))["ids"][0]


def fuse(rankings: list[list[str]]) -> list[str]:
    score: Counter = Counter()
    for ranking in rankings:
        for position, id_ in enumerate(ranking):
            score[id_] += 1 / (RRF_K + position + 1)
    return [id_ for id_, _ in score.most_common()]


def query_vectors(questions: list[str]) -> dict[str, list[float]]:
    try:
        cache = json.loads(QUERY_CACHE.read_text())
    except (OSError, ValueError):
        cache = {}
    missing = [q for q in questions if q not in cache]
    if missing:
        client = index.gemini_client()
        for n, q in enumerate(missing, 1):
            cache[q] = index.embed_query(q, client)
            index.log(f"  embedded query {n}/{len(missing)}")
            QUERY_CACHE.write_text(json.dumps(cache))     # saved as we go: a quota stop loses nothing
    return {q: cache[q] for q in questions}


# --------------------------------------------------------------------------
# 3. Retrieval stage
# --------------------------------------------------------------------------

def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]


def retrieval_stage() -> dict:
    rows = [r for r in read_questions() if r["kind"].strip().lower() != "unanswerable"]
    designs = indexed_designs()
    if not designs:
        raise SystemExit("No index found in index/. Run `uv run python main.py index` first.")
    vectors = query_vectors([r["question"] for r in rows])

    results, rankers = [], {}
    for design in designs:
        chunks = load_chunks(design)
        bm25 = BM25(chunks)
        rankers[f"dense_{design}"] = lambda r, d=design, c=chunks: [c[i] for i in dense_rank(d, vectors[r["question"]], POOL)]
        rankers[f"hybrid_{design}"] = lambda r, d=design, c=chunks, b=bm25: [
            c[i] for i in fuse([dense_rank(d, vectors[r["question"]], POOL), b.rank(r["question"], POOL)])
        ]

    for name, ranker in rankers.items():
        for row in rows:
            ranked = ranker(row)
            res = {"design": name, "id": row["id"], "kind": row["kind"].strip().lower()}
            for k in KS:
                res[f"k{k}"] = outcome(row, ranked, k)
            res["top5"] = " | ".join(f"{c['source']}:{c['section']}" for c in ranked[:5])
            results.append(res)

    summary = summarise(results)
    write_outputs(results, summary)
    print_summary(summary, results)
    return summary


def summarise(results: list[dict]) -> dict:
    summary: dict = {}
    for design in dict.fromkeys(r["design"] for r in results):
        mine = [r for r in results if r["design"] == design]
        summary[design] = {}
        for label, subset in (("all", mine), ("single", [r for r in mine if r["kind"] == "single"]),
                              ("multi", [r for r in mine if r["kind"] == "multi"])):
            if not subset:
                continue
            summary[design][label] = {"questions": len(subset)}
            for k in KS:
                hits = sum(r[f"k{k}"] == "hit" for r in subset)
                equivalents = sum(r[f"k{k}"] == "equivalent" for r in subset)
                summary[design][label][f"k{k}"] = {
                    "hit": hits, "equivalent": equivalents,
                    "strict": round(hits / len(subset), 3),
                    "lenient": round((hits + equivalents) / len(subset), 3),
                }
    return summary


def write_outputs(results: list[dict], summary: dict) -> None:
    with RESULTS_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["design", "id", "kind", "k1", "k3", "k5", "top5"])
        writer.writeheader()
        writer.writerows(results)
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2))


def print_summary(summary: dict, results: list[dict]) -> None:
    print("\nRetrieval hit rate (strict = labelled passage retrieved; lenient = strict + equivalent passages)\n")
    print(f"{'design':<22}{'subset':<8}{'n':>3}   " + "   ".join(f"k={k}: strict/lenient" for k in KS))
    for design, subsets in summary.items():
        for label, data in subsets.items():
            cells = "   ".join(f"{data[f'k{k}']['strict']:.2f} / {data[f'k{k}']['lenient']:.2f}".rjust(17) for k in KS)
            print(f"{design:<22}{label:<8}{data['questions']:>3}   {cells}")
    print("\nMisses at k=5 (for the failure analysis):")
    by_design = defaultdict(list)
    for r in results:
        if r["k5"] == "miss":
            by_design[r["design"]].append(r["id"])
    for design in summary:
        print(f"  {design}: {', '.join(by_design[design]) or 'none'}")
    print(f"\nWrote {RESULTS_CSV.relative_to(ROOT)} and {SUMMARY_JSON.relative_to(ROOT)}")


def main() -> int:
    retrieval_stage()
    print("\nEnd-to-end evaluation (agent answers, checks, judge): not written yet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
