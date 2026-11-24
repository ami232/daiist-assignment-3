"""
Show the add_document tool changing an answer: ask a question the corpus cannot
answer, add the document that covers it, ask again.

    uv run python demo_add_document.py          # you approve the add_document call in the terminal
    uv run python demo_add_document.py --yes    # approve it automatically (for this demo only)

The unanswerable question is about steel erection (q34 in eval/questions.csv).
The document is Subpart R of 29 CFR 1926, downloaded from the eCFR into corpus/extra/.
Results are written to eval/before_after.md. The index changes, so afterwards
either commit it or run `git restore index/` to go back to the original.
"""

import sys
from pathlib import Path

import agent
import index

ROOT = Path(__file__).resolve().parent
QUESTION = "At what height must connectors working on structural steel beams be given fall protection?"


def show(title: str, result: dict) -> str:
    lines = [f"### {title}", "", f"**Answer:** {result['answer']}", ""]
    lines.append(f"Citations: {', '.join(result['citations']) or 'none'}. "
                 f"Searches: {sum(1 for t in result['tool_calls'] if t['tool'] == 'search')}.")
    return "\n".join(lines)


def main() -> int:
    auto_yes = "--yes" in sys.argv
    approve = (lambda tool, args: True) if auto_yes else agent.ask_user

    print("Before: asking the question with Subpart R not indexed ...")
    before = agent.ask(QUESTION, approve=approve)
    print(before["answer"], "\n")

    entry = index.fetch_subpart("R", ROOT / "corpus" / "extra")
    path = (ROOT / "corpus" / "extra" / entry["file"]).relative_to(ROOT)
    print(f"Downloaded Subpart R to {path}. Asking the agent to add it ...")
    request = f"Please add the document at {path.as_posix()} to the index."
    added = agent.ask(request, approve=approve)
    print(added["answer"], "\n")
    ran = [t for t in added["tool_calls"] if t["tool"] == "add_document" and not t["denied"]]
    if not ran:
        print("add_document did not run (not approved), so there is no 'after' to show.")
        return 1
    print("Tool result:", ran[0]["result"], "\n")

    print("After: asking the same question again ...")
    after = agent.ask(QUESTION, approve=approve)
    print(after["answer"], "\n")

    report = ["# Before and after adding a document", "", f"Question: {QUESTION}", "",
              show("Before (Subpart R not indexed)", before), "",
              f"### Adding the document", "", f"Request: {request}", "",
              f"add_document result: {ran[0]['result']}", "",
              show("After (Subpart R indexed)", after), ""]
    (ROOT / "eval" / "before_after.md").write_text("\n".join(report), encoding="utf-8")
    print("Wrote eval/before_after.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
