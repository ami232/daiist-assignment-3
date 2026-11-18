"""
Before/after demo for the add_document tool (REPORT.md, "Adding a document").

    uv run python add_demo.py

1. Asks the agent an `unanswerable` test question (the original corpus has no answer).
2. Downloads the Wikipedia article "Padel" (CC BY-SA 4.0) as plain text into corpus/extra/.
3. Asks the agent to add that file. The harness asks YOU to approve the add_document call.
4. Asks the same question again, now with the new document searchable.
5. Asks to add the same file again, to show what happens when it is already indexed.

Writes everything to eval/add_demo.md.
"""

import asyncio
import csv
import json
import sys
from pathlib import Path

from agent import CorpusAgent, console_approval

ROOT = Path(__file__).resolve().parent
EXTRA = ROOT / "corpus" / "extra" / "padel_wikipedia.txt"
QUESTION_ID = "q31"   # the unanswerable question this document answers (see eval/questions.csv)
WIKI_API = ("https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1"
            "&titles=Padel&format=json&formatversion=2")


def fetch_wikipedia() -> None:
    if EXTRA.is_file():
        return
    import httpx

    r = httpx.get(WIKI_API, headers={"User-Agent": "padel-rag-assignment/1.0 (student project)"}, timeout=30)
    r.raise_for_status()
    page = json.loads(r.text)["query"]["pages"][0]
    EXTRA.parent.mkdir(parents=True, exist_ok=True)
    EXTRA.write_text(
        f"Padel (Wikipedia)\n\nSource: https://en.wikipedia.org/wiki/Padel, licence CC BY-SA 4.0, "
        f"revision fetched by add_demo.py.\n\n{page['extract']}\n", encoding="utf-8")
    print(f"Saved {EXTRA.relative_to(ROOT)} ({len(page['extract'].split())} words)", file=sys.stderr)


def question() -> str:
    with (ROOT / "eval" / "questions.csv").open(newline="", encoding="utf-8") as f:
        return next(r["question"] for r in csv.DictReader(f) if r["id"] == QUESTION_ID)


async def main() -> None:
    q = question()
    fetch_wikipedia()
    rel = EXTRA.relative_to(ROOT).as_posix()
    async with CorpusAgent(corpus_only=True) as before_agent:          # the original corpus only
        before = await before_agent.ask(q)
    async with CorpusAgent(approve=console_approval) as agent:
        added = await agent.ask(f"Please add the document {rel} to the corpus.")
    async with CorpusAgent() as agent:                                 # restart: server reloads the index
        after = await agent.ask(q)
        again = await agent.ask(f"Please add the document {rel} to the corpus.")

    def block(title, r):
        return (f"### {title}\n\n**Q:** {r['question']}\n\n**A:** {r['answer']}\n\n"
                f"Tool calls: {', '.join(t['tool'] + '(' + json.dumps(t['args']) + ')' for t in r['trace'])}\n\n"
                f"Approvals: {[e for e in r['events'] if e['event'] == 'approval']}\n")

    md = "\n".join([
        "# Adding a document: before and after", "",
        f"Unanswerable test question {QUESTION_ID}; added document: Wikipedia, *Padel* (CC BY-SA 4.0), as plain text.", "",
        block("1. Before (original corpus)", before),
        block("2. Add the document (human approval required)", added),
        block("3. After", after),
        block("4. Adding the same file again", again),
    ])
    out = ROOT / "eval" / "add_demo.md"
    out.write_text(md, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    # Windows consoles (cp1252) can't print characters like "≥" or "χ" from the papers: replace them instead of crashing.
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(errors="replace")
        except AttributeError:
            pass
    asyncio.run(main())
