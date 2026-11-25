"""
Before/after demo for the add-document tool (REPORT.md, "Adding a document").

    uv run python add_document_demo.py

1. Asks an unanswerable test question (q27, U-space) on the base corpus.
2. Asks the agent to add Commission Implementing Regulation (EU) 2021/664 on
   U-space; the harness asks YOU to approve add_document in the terminal.
3. Asks q27 again.
4. Asks to add the same file again (already-indexed behaviour).

Writes everything to eval/add_document_demo.md. Run it in a real terminal so
the approval prompt can be answered.
"""

import csv
import sys
from pathlib import Path

import agent

ROOT = Path(__file__).resolve().parent
DOC = "corpus/reg-2021-664-u-space.html"
DOC_URL = "https://publications.europa.eu/resource/celex/32021R0664"
OUT = ROOT / "eval" / "add_document_demo.md"


def download() -> None:
    path = ROOT / DOC
    if path.is_file():
        return
    import httpx

    path.parent.mkdir(exist_ok=True)
    r = httpx.get(DOC_URL, follow_redirects=True, timeout=120,
                  headers={"Accept": "application/xhtml+xml", "Accept-Language": "eng"})
    r.raise_for_status()
    path.write_bytes(r.content)


def show(title: str, trace: dict) -> list[str]:
    print(f"\n===== {title}\n{trace['answer']}\n", flush=True)
    calls = "; ".join(f"{c['name']}({c['args']})" for c in trace["tool_calls"]) or "none"
    events = "; ".join(trace["guardrail_events"]) or "none"
    return [f"## {title}", "", f"**Tool calls:** {calls}", "", f"**Harness events:** {events}", "",
            trace["answer"], ""]


def main() -> None:
    if not sys.stdin.isatty():
        sys.exit("Run this in a terminal: it asks you to approve add_document.")
    download()
    q = next(r for r in csv.DictReader(open(ROOT / "eval" / "questions.csv", encoding="utf-8")) if r["id"] == "q27")
    lines = ["# Adding a document: before and after", "",
             f"Question {q['id']} (marked unanswerable in the test set): {q['question']}", "",
             f"Document added: Commission Implementing Regulation (EU) 2021/664 on a regulatory framework "
             f"for the U-space ({DOC_URL}), file `{DOC}`.", ""]
    lines += show("Before", agent.answer(q["question"]))
    lines += show("Add the document (approval asked in the terminal)",
                  agent.answer(f"Please add the document {DOC} to the index."))
    lines += show("After", agent.answer(q["question"]))
    lines += show("Adding the same file again",
                  agent.answer(f"Please add the document {DOC} to the index."))
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
