"""
Demo for the report: an unanswerable question, before and after adding a document.

    uv run python demo_add_document.py

1. downloads the Payment Accounts Regulations 2015 (legislation.gov.uk, Open Government Licence v3.0)
2. asks the agent a question the corpus cannot answer (BEFORE)
3. adds the document with index.index_file, the same function the add_document tool calls
4. adds it AGAIN to show what happens when a document is already indexed
5. asks the same question (AFTER)
Saves everything in eval/add_document_demo.md.
"""

import urllib.request
from pathlib import Path

import agent
import index as ix
import retrieval

ROOT = Path(__file__).resolve().parent
URL = "https://www.legislation.gov.uk/uksi/2015/2038/data.xml"
FILE = ROOT / "corpus" / "extra" / "payment_accounts_regs_2015.xml"
QUESTION = ("How many days does a bank have to open or refuse a basic bank account "
            "after receiving a completed application?")


def show(title: str, result: dict) -> str:
    cites = "; ".join(sorted(set(c.replace("|", ", ") for c in result["retrieved"]))) or "(none)"
    return f"### {title}\n\n{result['answer']}\n\n_Retrieved: {cites}. Tool calls: {len(result['tool_calls'])}. Guard: {result['guard'] or 'none'}._\n"


def main() -> None:
    FILE.parent.mkdir(parents=True, exist_ok=True)
    if not FILE.exists():
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (course assignment)"})
        FILE.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    already = ix.get_collection().get(where={"source": FILE.stem}, limit=1)["ids"]
    if already:
        print("This document is already in the index, so 'before' would not be a true before. "
              "Delete the index/ folder contents only if you want to redo it.")

    md = ["# Add-document demo", "", f"Question: **{QUESTION}**", ""]
    print("BEFORE ...")
    before = agent.ask(QUESTION)
    md.append(show("Before adding the document", before))
    print(before["answer"], "\n")

    print("Adding the document ...")
    first = ix.index_file(FILE)
    retrieval.reset()
    print(first)
    second = ix.index_file(FILE)
    print("Second time:", second)
    md.append(f"### Adding the document\n\n- First time: {first}\n- Second time (already indexed): {second}\n")

    print("AFTER ...")
    after = agent.ask(QUESTION)
    md.append(show("After adding the document", after))
    print(after["answer"], "\n")

    (ROOT / "eval" / "add_document_demo.md").write_text("\n".join(md), encoding="utf-8")
    print("Saved eval/add_document_demo.md")


if __name__ == "__main__":
    main()
