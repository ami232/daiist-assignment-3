"""
Add-document demo: ask an unanswerable question, add the document that answers it through the
agent (with the approval step), ask again, then try to add it a second time.

    uv run python demo_add_document.py          # you approve add_document in the terminal
    uv run python demo_add_document.py --yes    # scripted approval, logged as such

Writes eval/add_document_demo.md. Run it after the evaluation: it changes the shared index.
"""

import json
import sys
from pathlib import Path

import agent

ROOT = Path(__file__).resolve().parent
QUESTION = "What are the CSF Tiers and what is their purpose?"  # q36 in eval/questions.csv
DOC = "corpus/holdout/NIST.CSWP.29.pdf"
ADD = f"Please add the file {DOC} to the index."


def scripted(tool: str, args: dict) -> bool:
    print(f"[approval] {tool}({args}) approved by the --yes flag", file=sys.stderr)
    return True


def show(title: str, out: dict) -> list[str]:
    calls = ", ".join(f"{c['tool']}({json.dumps(c['args'])})" for c in out["tool_calls"])
    return [f"## {title}", "", out["answer"], "", f"- tool calls: {calls or 'none'}",
            f"- approvals: {out['approvals'] or 'none'}",
            f"- retrieved: {', '.join(out['retrieved_chunk_ids']) or 'none'}",
            f"- guardrail: {out['guardrail']}", f"- {out['usage']} | {out['seconds']} s", ""]


def main() -> None:
    approve = scripted if "--yes" in sys.argv else agent.terminal_approver
    md = ["# Adding a document", "", f"Question: **{QUESTION}**", f"Document: `{DOC}` (NIST CSWP 29, CSF 2.0)", ""]
    steps = [("1. Before: the question is unanswerable", QUESTION, agent.deny_all),
             ("2. Add the document (approval required)", ADD, approve),
             ("3. After: the same question", QUESTION, agent.deny_all),
             ("4. Add it again: duplicate detection", ADD, approve)]
    for title, prompt, approver in steps:
        print(f"\n=== {title}\n> {prompt}")
        out = agent.run_agent(prompt, approve=approver)
        print(out["answer"])
        md += show(title, out)
    (ROOT / "eval" / "add_document_demo.md").write_text("\n".join(md))
    print("\nWrote eval/add_document_demo.md")


if __name__ == "__main__":
    main()
