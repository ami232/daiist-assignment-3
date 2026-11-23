"""Download ONE extra document for the add_document before/after demo.

    uv run python fetch_extra.py

It is saved in extra_docs/ (NOT in corpus/), so `main.py index` does not index it: the agent adds it
with the add_document tool during the demo. Source: IRS Topic No. 409 (a US government work,
public domain). It answers the question the corpus could not: how capital gains are taxed.
"""
from __future__ import annotations

import datetime
import json
from pathlib import Path

import requests

from fetch_corpus import html_to_markdown

URL = "https://www.irs.gov/taxtopics/tc409"
TITLE = "Topic No. 409, Capital gains and losses"
OUT = Path(__file__).resolve().parent / "extra_docs" / "irs-capital-gains.md"


def main() -> None:
    response = requests.get(URL, headers={"User-Agent": "DAIIST coursework RAG project", "Accept": "text/html"}, timeout=30)
    response.raise_for_status()
    response.encoding = "utf-8"  # requests guesses ISO-8859-1 for this page and garbles quotes
    body = html_to_markdown(response.text)    
    header = (
        "---\n"
        f"title: {json.dumps(TITLE)}\n"
        f"source_url: {URL}\n"
        f"retrieved: {datetime.date.today().isoformat()}\n"
        "publisher: Internal Revenue Service\n"
        "licence: US government work (public domain)\n"
        "---\n\n"
    )
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(header + body + "\n", encoding="utf-8")
    print(f"saved {OUT.name}: {len(body.split())} words")
    for line in body.splitlines():
        if line.startswith("#"):
            print("  ", line)


if __name__ == "__main__":
    main()