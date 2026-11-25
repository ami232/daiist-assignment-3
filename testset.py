"""
Test-set helper (a tool for writing eval/questions.csv, not a graded entry point).

    uv run python testset.py find "20 hours"                     # every passage that mentions it
    uv run python testset.py find "Ecctis" --source student-visa-guide
    uv run python testset.py check                               # check eval/questions.csv
    uv run python testset.py passages                            # the text behind each question

`find` prints, for each passage, the exact strings for questions.csv: the source
name and the location (a rule number like ST 26.5, or the heading as written in
eval/corpus_outline.md). Search a short key phrase, then try another wording: the
same fact is often worded differently in different documents.

How the two expected_* columns are read (evaluate.py uses the same rules):
    ;   separates the different passages a `multi` answer needs
    |   separates alternative places where the same fact appears
    The two columns must line up position by position.
"""

import argparse
import csv
import difflib
import io
import re
import sys
from collections import Counter

import index as ix

QUESTIONS = ix.ROOT / "eval" / "questions.csv"
COLUMNS = ["id", "question", "kind", "expected_source", "expected_location", "reference_answer"]
KINDS = ("single", "multi", "unanswerable")
MIN_TOTAL, MIN_MULTI, MIN_UNANSWERABLE = 30, 5, 5
COPY_WORDS = 7  # a question sharing this many words in a row with a passage copies its wording
_QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'})


def norm(text: str) -> str:
    """Compare labels ignoring case, quote style, spacing and a final full stop."""
    return re.sub(r"\s+", " ", (text or "").translate(_QUOTES)).strip().rstrip(".").strip().lower()


_corpus = None


def corpus() -> dict[str, list[dict]]:
    global _corpus
    if _corpus is None:
        pages = ix.download_corpus()
        _corpus = {s: ix.parse_blocks(s, p) for s, p in pages.items()}
    return _corpus


def outline_labels(blocks: list[dict]) -> dict[str, str]:
    """Heading path -> its label in the outline: the heading's own name, or the
    full path when that name is used more than once in the document."""
    paths = list(dict.fromkeys(b["heading_path"] for b in blocks))
    repeated = {n for n, c in Counter(p.split(" > ")[-1] for p in paths).items() if c > 1}
    return {p: p if p.split(" > ")[-1] in repeated else p.split(" > ")[-1] for p in paths}


def resolve_location(source: str, location: str) -> tuple[str, str] | None:
    """An expected_location as ('rule', 'ST 1.2'), ('path', 'A > B'), or
    ('name', 'B') for a heading name used more than once; None if not found."""
    blocks = corpus().get(source, [])
    want = norm(location)
    for b in blocks:
        if b["rule"] and norm(b["rule"]) == want:
            return ("rule", b["rule"])
    paths = list(dict.fromkeys(b["heading_path"] for b in blocks))
    for p in paths:
        if norm(p) == want:
            return ("path", p)
    named = [p for p in paths if norm(p.split(" > ")[-1]) == want]
    if len(named) == 1:
        return ("path", named[0])
    if named:
        return ("name", named[0].split(" > ")[-1])
    return None


def chunk_matches(meta: dict, source: str, resolved: tuple[str, str] | None) -> bool:
    """Does a stored chunk (its metadata) cover this expected location?"""
    if resolved is None or meta.get("source") != source:
        return False
    kind, value = resolved
    if kind == "rule":
        return value in (meta.get("rules") or "").split(" | ")
    paths = (meta.get("paths") or "").split(" | ")
    if kind == "path":
        return value in paths
    return any(p.split(" > ")[-1] == value for p in paths)


def expected_parts(row: dict) -> list[list[tuple[str, str]]]:
    """[[(source, location) alternatives] per needed passage] for an answerable row."""
    sources = [[a.strip() for a in part.split("|")] for part in row["expected_source"].split(";")]
    locations = [[a.strip() for a in part.split("|")] for part in row["expected_location"].split(";")]
    return [list(zip(s, l)) for s, l in zip(sources, locations)]


def read_questions(path=QUESTIONS) -> tuple[list[dict], list[str]]:
    """Rows with a question, plus problems that stop check.py from reading the file."""
    if not path.is_file():
        return [], [f"{path.name} not found."]
    raw = path.read_bytes()
    problems = []
    if raw.startswith(b"\xef\xbb\xbf"):
        problems.append("the file starts with an invisible BOM, so check.py won't find the `id` column. "
                        "In VS Code, click 'UTF-8 with BOM' at the bottom right > Save with Encoding > UTF-8.")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return [], problems + ["the file isn't UTF-8 (Excel?). Re-save it from Google Sheets "
                               "(File > Download > Comma-separated values) or VS Code."]
    header = text.splitlines()[0] if text.strip() else ""
    if ";" in header and "," not in header:
        return [], problems + ["the file uses ; between columns (Excel with Spanish settings). "
                               "Re-save it as comma-separated, e.g. from Google Sheets."]
    reader = csv.DictReader(io.StringIO(text))
    missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
    if missing:
        return [], problems + [f"missing column(s) {', '.join(missing)}; the header row must be exactly: "
                               + ",".join(COLUMNS)]
    rows = [r for r in reader if (r.get("question") or "").strip()]
    return rows, problems


# ==========================================================================
def find(phrase: str, source: str | None, regex: bool, limit: int) -> None:
    if source and source not in corpus():
        sys.exit(f"Unknown source {source!r}. Sources: {', '.join(corpus())}")
    pattern = re.compile(phrase if regex else re.escape(phrase.translate(_QUOTES)), re.I)
    hits = []
    for s, blocks in corpus().items():
        if source and s != source:
            continue
        labels = outline_labels(blocks)
        headings_hit = set()
        for b in blocks:
            text = b["text"].translate(_QUOTES)
            m = pattern.search(text)
            if m:
                hits.append((s, b, labels[b["heading_path"]], text, m))
            elif b["heading_path"] not in headings_hit and pattern.search(b["heading_path"].translate(_QUOTES)):
                headings_hit.add(b["heading_path"])  # the phrase is in the heading: show the section once
                hits.append((s, b, labels[b["heading_path"]], text, None))
    if not hits:
        print(f"No passage or heading contains {phrase!r}.")
        print("For an unanswerable question, also search other words for the same thing.")
        return
    for n, (s, b, label, text, m) in enumerate(hits[:limit], start=1):
        if m:
            start, end = max(0, m.start() - 120), min(len(text), m.end() + 160)
        else:
            start, end = 0, min(len(text), 280)
        snippet = ("..." if start else "") + text[start:end] + ("..." if end < len(text) else "")
        where = f"{b['rule']}   (or its heading: {label})" if b["rule"] else label
        found = "" if m else "   [the heading matches; first passage under it:]"
        print(f"[{n}] {s}\n    location: {where}{found}\n    {snippet}\n")
    docs = list(dict.fromkeys(h[0] for h in hits))
    more = f" (showing {limit}; add --max {len(hits)} to see all)" if len(hits) > limit else ""
    print(f"{len(hits)} passage(s) in {len(docs)} document(s){more}: {', '.join(docs)}")


# ==========================================================================
def shingles(text: str, n: int = COPY_WORDS) -> set[str]:
    words = re.findall(r"[a-z0-9£]+", text.translate(_QUOTES).lower())
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def check(path=QUESTIONS, need_answers: bool = True) -> int:
    """Print every problem; return 1 if there are errors. need_answers=False
    (retrieval only) lets reference answers still be missing."""
    rows, problems = read_questions(path)
    shown = path.relative_to(ix.ROOT) if path.is_relative_to(ix.ROOT) else path
    print(f"Checking {shown}: {len(rows)} question(s)\n")
    errors = warnings = 0

    def error(qid: str, message: str) -> None:
        nonlocal errors
        errors += 1
        print(f"  ERROR    {qid}: {message}")

    def warning(qid: str, message: str) -> None:
        nonlocal warnings
        warnings += 1
        print(f"  warning  {qid}: {message}")

    for p in problems:
        error("file", p)
    if not rows:
        print("No questions yet." if not errors else f"\n{errors} error(s).")
        return 1 if errors else 0

    sources = list(corpus())
    corpus_shingles = set().union(*(shingles(b["text"]) for bl in corpus().values() for b in bl))
    seen_ids = set()
    kinds = Counter()

    for r in rows:
        qid = r["id"].strip() or "(no id)"
        kind = (r["kind"] or "").strip().lower()
        kinds[kind] += 1
        src, loc = (r["expected_source"] or "").strip(), (r["expected_location"] or "").strip()
        if not r["id"].strip():
            error(qid, f"no id for {r['question'][:50]!r}")
        elif qid in seen_ids:
            error(qid, "this id is used more than once")
        seen_ids.add(qid)
        if kind not in KINDS:
            error(qid, f"kind is {r['kind']!r}; use single, multi or unanswerable")
            continue
        if not (r["reference_answer"] or "").strip():
            (error if need_answers else warning)(qid, "no reference_answer" + ("" if need_answers else " yet"))
        copied = shingles(r["question"]) & corpus_shingles
        if copied:
            warning(qid, f"the question copies the documents' wording ({sorted(copied)[0]!r}...); "
                         "rephrase it the way a student would ask")

        if kind == "unanswerable":
            if src or loc:
                error(qid, "unanswerable questions must leave expected_source and expected_location empty")
            continue
        if not src or not loc:
            error(qid, "answerable questions need both expected_source and expected_location")
            continue

        s_parts, l_parts = src.split(";"), loc.split(";")
        if len(s_parts) != len(l_parts) or any(len(a.split("|")) != len(b.split("|"))
                                               for a, b in zip(s_parts, l_parts)):
            error(qid, "expected_source and expected_location don't line up: same number of ; parts "
                       "and of | alternatives in each part, in the same order")
            continue
        if kind == "single" and len(s_parts) > 1:
            warning(qid, "a single question with ; - use | for other places with the same fact "
                         "(; means the answer needs several passages, i.e. multi)")
        if kind == "multi" and len(s_parts) < 2:
            warning(qid, "a multi question needs two passages, separated by ;")

        for part in expected_parts(r):
            for source, location in part:
                if source not in sources:
                    close = difflib.get_close_matches(source, sources, n=1)
                    hint = f" Did you mean {close[0]}?" if close else ""
                    error(qid, f"unknown source {source!r}.{hint}")
                    continue
                resolved = resolve_location(source, location)
                if resolved is None:
                    blocks = corpus()[source]
                    options = sorted({b["rule"] for b in blocks if b["rule"]} | set(outline_labels(blocks).values()))
                    by_norm = {norm(o): o for o in options}
                    close = difflib.get_close_matches(norm(location), list(by_norm), n=2, cutoff=0.5)
                    names = [by_norm[c] for c in close]  # most similar first
                    hint = f" Closest: {' / '.join(names)}" if names else " Check eval/corpus_outline.md."
                    error(qid, f"{location!r} is not a rule or heading in {source}.{hint}")
                elif resolved[0] == "name":
                    warning(qid, f"{location!r} is a heading used more than once in {source}; "
                                 "use its full path from the outline")

    first = next((r for r in rows if r["kind"].strip().lower() != "unanswerable"), None)
    print(f"\nCounts: {len(rows)} questions ({kinds['single']} single, {kinds['multi']} multi, "
          f"{kinds['unanswerable']} unanswerable). Needed: {MIN_TOTAL}+ in total, "
          f"{MIN_MULTI}+ multi, {MIN_UNANSWERABLE}+ unanswerable.")
    short = [name for name, have, need in (("questions", len(rows), MIN_TOTAL),
                                           ("multi", kinds["multi"], MIN_MULTI),
                                           ("unanswerable", kinds["unanswerable"], MIN_UNANSWERABLE))
             if have < need]
    if short:
        print(f"Still short of: {', '.join(short)}.")
    if first:
        print(f"check.py will test with {first['id'].strip()}: {first['question'].strip()!r}")
    print(f"\n{errors} error(s), {warnings} warning(s).")
    return 1 if errors else 0


# ==========================================================================
PASSAGES = ix.ROOT / "eval" / "reference_passages.md"
PASSAGE_WORDS = 600  # per passage shown


def location_blocks(source: str, resolved: tuple[str, str]) -> list[dict]:
    """The blocks at an expected location: the rule itself, or the text directly under the heading."""
    kind, value = resolved
    blocks = corpus()[source]
    if kind == "rule":
        return [b for b in blocks if b["rule"] == value]
    if kind == "path":
        return [b for b in blocks if b["heading_path"] == value]
    return [b for b in blocks if b["heading_path"].split(" > ")[-1] == value]


def passages() -> int:
    """eval/reference_passages.md: for each question, the text at its expected
    location (the first place listed for each passage it needs)."""
    rows, problems = read_questions()
    if problems or not rows:
        print("Run `uv run python testset.py check` first.")
        return 1
    lines = ["# Passages for your reference answers", "",
             "For each answerable question, the text at the first expected location of each passage it "
             "needs, plus the other places the same fact appears. Write each reference answer in your own "
             "words from these. After changing a location, regenerate with "
             "`uv run python testset.py passages`.", ""]
    for r in rows:
        kind = r["kind"].strip().lower()
        lines += [f"## {r['id'].strip()} ({kind})", "", f"**{r['question'].strip()}**", ""]
        if kind == "unanswerable":
            lines += ["No passage answers this. The reference answer is what the assistant should say instead: "
                      "your refusal sentence, and where to look.", ""]
            continue
        parts = expected_parts(r)
        for n, alternatives in enumerate(parts, start=1):
            if len(parts) > 1:
                lines += [f"### Passage {n}", ""]
            (source, location), others = alternatives[0], alternatives[1:]
            resolved = resolve_location(source, location) if source in corpus() else None
            if resolved is None:
                lines += [f"`{location}` is not in {source}: run `uv run python testset.py check`.", ""]
                continue
            lines += [f"From `[{source}, {location}]`:", ""]
            budget = PASSAGE_WORDS
            for b in location_blocks(source, resolved):
                words = b["text"].split()
                lines += ["> " + " ".join(words[:budget]) + (" ..." if len(words) > budget else ""), ">"]
                budget -= len(words)
                if budget <= 0:
                    break
            lines[-1] = ""
            if others:
                lines += ["Also in: " + ", ".join(f"`[{s}, {l}]`" for s, l in others), ""]
    PASSAGES.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {PASSAGES.relative_to(ix.ROOT)} ({len(rows)} questions).")
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # Windows consoles lack some characters
    parser = argparse.ArgumentParser(description="Search the corpus and check eval/questions.csv.")
    sub = parser.add_subparsers(dest="command", required=True)
    f = sub.add_parser("find", help="list every passage that contains a phrase")
    f.add_argument("phrase")
    f.add_argument("--source", help="only this document, e.g. appendix-student")
    f.add_argument("--regex", action="store_true", help="treat the phrase as a regular expression")
    f.add_argument("--max", type=int, default=30, help="show at most this many passages (default 30)")
    sub.add_parser("check", help="check eval/questions.csv")
    sub.add_parser("passages", help="write eval/reference_passages.md for writing reference answers")
    args = parser.parse_args()
    if args.command == "find":
        find(args.phrase, args.source, args.regex, args.max)
        return 0
    if args.command == "passages":
        return passages()
    return check()


if __name__ == "__main__":
    sys.exit(main())
