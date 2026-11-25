"""Helper for writing eval/questions.csv (not part of the pipeline).

  uv run python questions_helper.py init                       create eval/questions.txt
  uv run python questions_helper.py headings "Reg 1223/2009"   locations you can cite
  uv run python questions_helper.py show "Reg 1223/2009" "Article 4"   read that text
  uv run python questions_helper.py build                      questions.txt -> questions.csv, checked
"""
import csv
import sys
import textwrap
from collections import Counter
from pathlib import Path

import index

TXT, CSV = index.ROOT / "eval" / "questions.txt", index.ROOT / "eval" / "questions.csv"
KINDS = ("single", "multi", "unanswerable")
FILES = {info["source"]: name for name, info in index.CORPUS.items()}
TEMPLATE = """# One question per line:  question | kind | source | location | reference answer
# kind: single, multi (needs two passages) or unanswerable (source and location stay empty)
# multi: two sources and two locations separated by ;  e.g.  Reg 1223/2009;CPNP guide | Article 4;p. 12
# unanswerable: the reference answer is what the assistant should say
# Lines starting with # are ignored. Delete these lines or leave them.
"""
_cache = {}


def labels(source):
    if source not in _cache:
        words, _ = index.load_words(index.CORPUS_DIR / FILES[source])
        _cache[source] = list(dict.fromkeys(s for _, _, s in words)), words
    return _cache[source]


def need(source):
    if source not in FILES:
        sys.exit(f"Unknown source {source!r}. Use one of: {', '.join(FILES)}")


def build():
    rows, problems = [], []
    for n, line in enumerate(TXT.read_text().splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 5:
            problems.append(f"line {n}: expected 5 fields separated by |, found {len(parts)}")
            continue
        question, kind, source, location, answer = parts
        if kind not in KINDS:
            problems.append(f"line {n}: kind must be one of {KINDS}, not {kind!r}")
        if not question or not answer:
            problems.append(f"line {n}: question and reference answer cannot be empty")
        if kind == "unanswerable" and (source or location):
            problems.append(f"line {n}: unanswerable questions have an empty source and location")
        if kind != "unanswerable":
            sources = [s.strip() for s in source.split(";") if s.strip()]
            places = [s.strip() for s in location.split(";") if s.strip()]
            if not sources or not places:
                problems.append(f"line {n}: source and location are required")
            if kind == "multi" and (len(sources) != 2 or len(places) != 2):
                problems.append(f"line {n}: multi needs two sources and two locations separated by ;")
            for i, place in enumerate(places):
                src = sources[i] if len(sources) == len(places) else (sources[0] if sources else "")
                if src not in FILES:
                    problems.append(f"line {n}: unknown source {src!r}")
                elif place not in labels(src)[0]:
                    problems.append(f"line {n}: {src} has no location {place!r} (see: headings \"{src}\")")
        rows.append((question, kind, source, location, answer))
    if problems:
        sys.exit("Fix these first:\n  " + "\n  ".join(problems))
    with CSV.open("w", newline="", encoding="utf-8") as f:
        out = csv.writer(f)
        out.writerow(["id", "question", "kind", "expected_source", "expected_location", "reference_answer"])
        for i, (q, k, s, l, a) in enumerate(rows, 1):
            out.writerow([f"q{i:02d}", q, k, s, l, a])
    kinds = Counter(r[1] for r in rows)
    print(f"Wrote {CSV.name}: {len(rows)} questions {dict(kinds)}")
    print("By document:", dict(Counter(x.strip() for r in rows for x in r[2].split(";") if x.strip())))
    for ok, msg in ((len(rows) >= 30, "at least 30 questions"), (kinds["multi"] >= 5, "at least 5 multi"), (kinds["unanswerable"] >= 5, "at least 5 unanswerable")):
        print(("OK   " if ok else "MISSING ") + msg)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "init":
        if TXT.exists():
            sys.exit(f"{TXT} already exists; not touching it.")
        TXT.write_text(TEMPLATE)
        print("Created eval/questions.txt")
    elif cmd == "headings" and len(sys.argv) == 3:
        need(sys.argv[2])
        print(", ".join(labels(sys.argv[2])[0]))
    elif cmd == "show" and len(sys.argv) == 4:
        need(sys.argv[2])
        words = [w for w, _, s in labels(sys.argv[2])[1] if s == sys.argv[3]]
        if not words:
            sys.exit(f"No text under {sys.argv[3]!r}. Run: headings \"{sys.argv[2]}\"")
        print(textwrap.fill(" ".join(words[:700]), 110) + (f"\n... ({len(words)} words in total)" if len(words) > 700 else ""))
    elif cmd == "build":
        build()
    else:
        print(__doc__)


main()
