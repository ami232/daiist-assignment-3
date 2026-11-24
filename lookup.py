"""
Read the corpus while writing the test set. No API calls, no quota.

    uv run python lookup.py toc GDPR                  # articles/annexes with their titles
    uv run python lookup.py show GDPR "Article 6"     # full text of an article, paragraph by paragraph
    uv run python lookup.py find "24 hours"           # where a phrase appears in the INDEXED scope
    uv run python lookup.py find "24 hours" --all     # ... also in recitals and in NIS2 (held out)

`find` is how you check that an "unanswerable" question really is: if the
phrase only appears in recitals or NIS2, the initial index cannot answer it.
"""

import argparse
import re
import sys
import textwrap
from pathlib import Path

from index import HELD_OUT, INITIAL_CORPUS, RAW
from ingest import INDEXED_KINDS, parse_file

sys.stdout.reconfigure(encoding="utf-8")


def load(include_held_out: bool) -> list:
    files = INITIAL_CORPUS + (HELD_OUT if include_held_out else [])
    units = []
    for f in files:
        _, us = parse_file(RAW / f)
        units += us
    return units


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("toc"); t.add_argument("doc")
    s = sub.add_parser("show"); s.add_argument("doc"); s.add_argument("ref", help='"Article 6", "Annex III" or "Recital 32"')
    f = sub.add_parser("find"); f.add_argument("phrase"); f.add_argument("--all", action="store_true")
    a = p.parse_args()

    if a.cmd == "toc":
        units = [u for u in load(True) if u.doc.lower() == a.doc.lower() and u.kind != "recital"]
        seen = set()
        for u in units:
            key = (u.kind, u.ref)
            if key not in seen:
                seen.add(key)
                words = sum(x.words for x in units if (x.kind, x.ref) == key)
                print(f"{('Article ' if u.kind == 'article' else 'Annex ') + u.ref:14} {words:5}w  {u.title}")
    elif a.cmd == "show":
        kind, ref = a.ref.split(maxsplit=1)
        for u in load(True):
            if u.doc.lower() == a.doc.lower() and u.kind == kind.lower() and u.ref == ref:
                print(f"\n[{u.doc} {u.location}]  {u.title}")
                print(textwrap.fill(u.text, 100))
    else:
        rx = re.compile(re.escape(a.phrase), re.I)
        hits = [u for u in load(a.all) if rx.search(u.text)]
        for u in hits:
            indexed = u.kind in INDEXED_KINDS and u.doc != "NIS2"
            m = rx.search(u.text)
            snippet = u.text[max(m.start() - 80, 0):m.end() + 80]
            print(f"{'INDEXED ' if indexed else 'not idx '} {u.doc:8} {u.location:32} ...{snippet}...")
        print(f"\n{len(hits)} match(es); {sum(1 for u in hits if u.kind in INDEXED_KINDS and u.doc != 'NIS2')} in the indexed scope.")


if __name__ == "__main__":
    main()
