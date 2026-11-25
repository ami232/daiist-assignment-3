"""
Demo of add_document through the agent (for REPORT.md, section "Adding a document").

Run 1 asks the agent to add corpus/AAR2002.pdf. The approval callback prints the
prompt and answers "y" (scripted, because this demo runs without a terminal; with
`main.py ask` a human types it). Run 2 asks again with the same file to show the
"already indexed" path, which spends no embeddings.

Output: eval/add_document_demo.txt
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import agent  # noqa: E402

OUT = ROOT / "eval" / "add_document_demo.txt"
REQUEST = "Please add the report corpus/AAR2002.pdf (Atlas Air 3591) to the index."


def scripted_yes(path: str) -> bool:
    print(f"The agent wants to add {path!r} to the index (spends embedding quota). Approve? [y/N] y (scripted)")
    return True


def run(label: str) -> str:
    r = agent.answer(REQUEST, approve=scripted_yes)
    lines = [f"== {label}", f"User: {REQUEST}"]
    for step in r["trace"]:
        lines.append(f"Tool call: {step['tool']}({step['args']})")
        lines.append(f"Tool result: {step['result']}")
    lines.append(f"Agent: {r['answer']}")
    lines.append(f"({r['tool_calls']} tool calls, {r['seconds']}s, {r['model']})\n")
    return "\n".join(lines)


if __name__ == "__main__":
    text = run("Run 1: new document") + "\n" + run("Run 2: same file again")
    OUT.write_text(text, encoding="utf-8")
    print(text)
