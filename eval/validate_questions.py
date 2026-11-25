"""
Validate eval/questions.csv against the indexed text. Read-only; never calls Gemini.

    uv run python eval/validate_questions.py

1. Format: columns, kinds, counts, expected_source values vs chunk doc_ids.
2. single/multi rows: locate each expected_location in the text (identifier, section or phrase),
   show the passage next to the reference answer, flag names/numbers/identifiers of the reference
   answer missing from the passage, and propose a normalised location for the hit rule.
3. unanswerable rows: show every occurrence of their key terms in the indexed text.
"""

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import index  # noqa: E402

QUESTIONS = ROOT / "eval" / "questions.csv"
COLUMNS = ["id", "question", "kind", "expected_source", "expected_location", "reference_answer"]
KINDS = {"single", "multi", "unanswerable"}
DESIGN = index.DEFAULT_DESIGN
WINDOW = 160  # words of passage scored and shown after the location

# Same patterns as index.py, minus the "(?=:)" lookahead, so a bare "GOVERN 1.1" in the CSV is recognised.
ID_RE = re.compile("|".join(f"(?:{d.id_pattern.replace('(?=:)', '')})" for d in index.DOCS.values() if d.id_pattern)
                   + r"|\b[A-Z]{2}-\d+\b")  # SP 800-53 controls such as SA-1
DOC_NAME_WORDS = {"AI", "RMF", "SSDF", "GAI", "Generative", "Profile", "Incident", "Response", "NIST", "SP"}
STOP = {"the", "and", "for", "are", "with", "that", "this", "from", "into", "its", "their", "which", "each",
        "does", "what", "when", "should", "says", "say", "says", "also", "both", "other", "about", "have",
        "has", "own", "not", "only", "entry", "good", "answer", "points", "where", "moved", "task"}
UNANSWERABLE_TERMS = {
    "q36": [r"\b[Tt]iers?\b"],
    "q37": [r"42001", r"\bISO\b"],
    "q38": [r"EU AI Act", r"\bAI Act\b", r"European Union"],
    "q39": [r"SSDF (?:version )?1\.2", r"[Vv]ersion 1\.2", r"Revision 1\b", r"\bRev\. ?1\b", r"\br1\b"],
    "q40": [r"\bIR-4\b", r"Incident Handling"],
    "q41": [r"OWASP", r"Top 10"],
    "q42": [r"Playbook"],
    "q43": [r"AI 100-2", r"100-2\b", r"[Aa]dversarial machine learning"],
}


def norm(s: str) -> str:
    return s.replace("’", "'").replace("–", "-").replace("—", "-").lower()


def load_docs():
    """doc_id -> dict(words, pages per word, chunks, section starts)."""
    docs = {}
    for spec in index.INDEXED:
        pages = index.extract_pages(spec.path, spec)
        words, wpage = [], []
        for pg in pages:
            for w in pg["text"].split():
                words.append(w)
                wpage.append(pg["page"])
        chunks = index.chunk_file(spec.path, DESIGN)
        docs[spec.doc_id] = {"spec": spec, "words": words, "wpage": wpage, "chunks": chunks,
                             "sections": index.locate_sections(words, spec)}
    return docs


def covering_chunks(doc, lo, hi):
    step = index.DESIGNS[DESIGN]["size"] - index.DESIGNS[DESIGN]["overlap"]
    size = index.DESIGNS[DESIGN]["size"]
    return [c for i, c in enumerate(doc["chunks"]) if i * step < hi and i * step + size > lo]


def ref_terms(ref: str):
    """(content words for scoring, key terms that must appear: identifiers, numbers, names)."""
    words = {w for w in re.findall(r"[A-Za-z][A-Za-z\-']{3,}", norm(ref)) if w not in STOP}
    keys = set(ID_RE.findall(ref))
    rest = ID_RE.sub(" ", ref)
    keys |= set(re.findall(r"\b\d+(?:\.\d+)?\b", rest))
    keys |= {w for w in re.findall(r"\b[A-Z]{2,}\b", rest) if w not in DOC_NAME_WORDS}
    for m in re.finditer(r"\b[A-Z][a-z][A-Za-z\-]*(?:\s+(?:the\s+|of\s+|or\s+|to\s+)?[A-Z][a-z][A-Za-z\-]*)*", rest):
        name = m.group(0)
        toks = name.split()
        while toks and toks[0] in DOC_NAME_WORDS:
            toks = toks[1:]
        if not toks:
            continue
        name = " ".join(toks)
        before = rest[:m.start()].rstrip()
        sentence_initial = not before or before[-1] in ".:;("
        if len(toks) == 1 and (sentence_initial or toks[0] in DOC_NAME_WORDS):
            continue
        keys.add(name)
    return words, keys


def locate(doc, loc, ref_words):
    """Best (start, end) word window for this location, its kind, and how many candidates were seen."""
    words, n = doc["words"], len(doc["words"])
    starts, kind = [], None
    if ID_RE.fullmatch(loc):
        kind = "identifier"
        toks = loc.split()
        for i in range(n - len(toks) + 1):
            if [w.strip("():;,.") for w in words[i:i + len(toks)]] == toks:
                starts.append(i)
    else:
        secs = dict((h, p) for p, h in doc["sections"])
        if loc in secs:
            kind = "section"
            pos = sorted(p for p, _ in doc["sections"])
            s = secs[loc]
            e = next((p for p in pos if p > s), n)
            starts = list(range(s, max(s + 1, e - WINDOW // 2), 10))
        else:
            kind = "phrase"
            toks = loc.split()
            starts = [i for i in range(n - len(toks) + 1) if words[i:i + len(toks)] == toks]
    if not starts:
        return None, kind, 0

    def score(i):
        text = norm(" ".join(words[i:i + WINDOW]))
        return sum(1 for w in ref_words if w in text)
    best = max(starts, key=lambda i: (score(i), -i))
    return (best, min(best + WINDOW, n)), kind, len(starts)


def main():
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        rows = list(reader)

    print("=" * 100, "\n1. FORMAT\n" + "=" * 100)
    problems = []
    missing_cols = [c for c in COLUMNS if c not in header]
    print(f"columns: {header}  ->  {'OK' if not missing_cols else 'MISSING ' + str(missing_cols)}")
    kinds = [r["kind"].strip() for r in rows]
    bad_kinds = [(r["id"], r["kind"]) for r in rows if r["kind"].strip() not in KINDS]
    counts = {k: kinds.count(k) for k in KINDS}
    print(f"rows: {len(rows)} (need 30+)  counts: {counts}  (need 5+ multi, 5+ unanswerable)")
    print(f"invalid kind values: {bad_kinds or 'none'}")
    print(f"duplicate ids: {[i for i in {r['id'] for r in rows} if [x['id'] for x in rows].count(i) > 1] or 'none'}")

    docs = load_docs()
    doc_ids = sorted(docs)
    print(f"doc_ids in chunk metadata ({DESIGN}): {doc_ids}")
    for r in rows:
        srcs = [s.strip() for s in r["expected_source"].split(";") if s.strip()]
        locs = [s.strip() for s in r["expected_location"].split(";") if s.strip()]
        if r["kind"] == "unanswerable":
            if srcs or locs:
                problems.append(f"{r['id']}: unanswerable row has a source/location")
            continue
        for s in srcs:
            if s not in docs:
                problems.append(f"{r['id']}: expected_source {s!r} is not a doc_id (have {doc_ids})")
        if len(srcs) != len(locs) and len(srcs) != 1:
            problems.append(f"{r['id']}: {len(srcs)} sources but {len(locs)} locations")
        if r["kind"] == "multi" and len(locs) < 2:
            problems.append(f"{r['id']}: multi row with fewer than two locations")
    print("source/kind mismatches:", "none" if not problems else "")
    for p in problems:
        print("  -", p)

    print("\n" + "=" * 100, "\n2. LOCATIONS (single and multi)\n" + "=" * 100)
    print("Hit rule format: an identifier exactly as written in the document (e.g. GOVERN 1.2, GV-1.2-002, RS.MA-02,\n"
          "PO.1.1), else a PDF page or range written pN or pN-M (PDF page index, not the printed page).\n"
          "A retrieved chunk is a hit if its doc_id matches and the identifier is in its `identifiers`\n"
          "or the page lies within page_start..page_end. Multi rows: one location per source, same order, ';'.")
    proposals = []
    for r in rows:
        if r["kind"] == "unanswerable":
            continue
        srcs = [s.strip() for s in r["expected_source"].split(";")]
        locs = [s.strip() for s in r["expected_location"].split(";")]
        if len(srcs) == 1 and len(locs) > 1:
            srcs = srcs * len(locs)
        ref_words, keys = ref_terms(r["reference_answer"])
        print(f"\n--- {r['id']} [{r['kind']}] {r['question']}")
        print(f"    reference: {r['reference_answer']}")
        passages, new_locs = [], []
        for src, loc in zip(srcs, locs):
            doc = docs.get(src)
            if doc is None:
                print(f"    {src} | {loc}: SOURCE NOT INDEXED")
                new_locs.append(loc)
                continue
            win, kind, ncand = locate(doc, loc, ref_words)
            if win is None:
                print(f"    {src} | {loc!r} ({kind}): NOT FOUND in text")
                new_locs.append(loc)
                continue
            lo, hi = win
            pages = sorted({doc["wpage"][i] for i in range(lo, hi)})
            chunks = covering_chunks(doc, lo, hi)
            text = " ".join(doc["words"][lo:hi])
            passages.append(" ".join(c.text for c in chunks))
            in_meta = kind == "identifier" and any(loc in c.meta["identifiers"].split(";") for c in chunks)
            print(f"    {src} | {loc!r} ({kind}, {ncand} candidate position(s)) -> PDF p{pages[0]}"
                  f"{'-' + str(pages[-1]) if pages[-1] != pages[0] else ''} | chunks "
                  f"{', '.join(c.chunk_id.split(':')[-1] for c in chunks)}"
                  + (f" | in chunk identifiers: {'yes' if in_meta else 'NO'}" if kind == "identifier" else ""))
            print(f"    passage: {text[:600]}")
            if kind == "identifier" and in_meta:
                new_locs.append(loc)
            else:
                new_locs.append(f"p{pages[0]}" + (f"-{pages[-1]}" if pages[-1] != pages[0] else ""))
        joined = norm(" ".join(passages))
        missing = sorted(k for k in keys if norm(k) not in joined)
        print(f"    reference terms missing from the covering chunk(s): {missing or 'none'}")
        new = ";".join(new_locs)
        if new != r["expected_location"]:
            proposals.append((r["id"], r["expected_location"], new))

    print("\n" + "=" * 100, "\nPROPOSED expected_location (not written)\n" + "=" * 100)
    print(f"{'id':<5} | {'current':<52} | proposed")
    for pid, cur, new in proposals:
        print(f"{pid:<5} | {cur:<52} | {new}")

    print("\n" + "=" * 100, "\n3. UNANSWERABLE: key-term hits in the indexed text\n" + "=" * 100)
    for r in rows:
        if r["kind"] != "unanswerable":
            continue
        print(f"\n--- {r['id']} {r['question']}")
        terms = UNANSWERABLE_TERMS.get(r["id"], [])
        total = 0
        for term in terms:
            for doc_id, doc in docs.items():
                for c in doc["chunks"]:
                    for m in re.finditer(term, c.text):
                        total += 1
                        a, b = max(0, m.start() - 160), min(len(c.text), m.end() + 160)
                        print(f"    [{term}] {doc_id} PDF p{c.meta['page_start']}-{c.meta['page_end']} "
                              f"({c.chunk_id.split(':')[-1]}): ...{c.text[a:b]}...")
        if total == 0:
            print(f"    no hits for {terms}")


if __name__ == "__main__":
    main()
