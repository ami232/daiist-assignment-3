"""
Add-document demo: `uv run python demo_add_document.py`

1. Asks the agent an unanswerable question (terrorist content takedown deadline).
2. Asks the agent to add the Terrorist Content Online Regulation, with approval
   denied: nothing is added.
3. Asks again, approval given: the regulation goes through index.py's pipeline.
4. Calls add_document on the same file again: skipped as already indexed.
5. Asks the question again.
6. Removes the added chunks again (vectors stay cached), so `main.py evaluate`
   keeps measuring the corpus the test set was written for.

Writes eval/add_document_demo.md.
"""

import csv
import json
from pathlib import Path

import agent
import index as ix
import server

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "eval" / "add_document_demo.md"


def question() -> str:
    with (ROOT / "eval" / "questions.csv").open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if "terrorist" in r["question"].lower():
                return r["question"]
    return "How fast do we have to take down terrorist content after an authority orders it?"


def show(title: str, r: dict) -> str:
    cites = "\n".join(f"- [{c}] {loc}" for c, loc in r["citations"].items()) or "- none"
    calls = "\n".join(f"- {t['tool']}({json.dumps(t['args'])})" for t in r["trace"])
    return f"### {title}\n\n{r['answer']}\n\nCitations:\n{cites}\n\nTool calls:\n{calls}\n"


def main() -> None:
    path = ix.download("tco", ix.EXTRA_DOCS["tco"])
    rel = path.relative_to(ROOT)
    q = question()
    parts = [f"# Add-document demo\n\nQuestion: {q}\n\nDocument: {ix.EXTRA_DOCS['tco']['title']}, {ix.EURLEX.format(celex=ix.EXTRA_DOCS['tco']['celex'])}\n"]

    parts.append(show("1. Before", agent.run(q, approver=lambda a: False)))

    asked = []
    r = agent.run(f"Please add the file {rel} to the index.", approver=lambda a: asked.append(a) or False)
    parts.append(show("2. Add request, approval denied", r) + f"\nApproval asked for: {asked}\n")

    asked = []
    r = agent.run(f"Please add the file {rel} to the index.", approver=lambda a: asked.append(a) or True)
    parts.append(show("3. Add request, approved", r) + f"\nApproval asked for: {asked}\n")

    parts.append(f"### 4. Same file again (direct tool call)\n\n{server.add_document(str(rel))}\n")

    parts.append(show("5. After", agent.run(q, approver=lambda a: False)))

    for design in ix.DESIGNS:
        ix.write_design(design, [c for c in ix.read_design(design) if c["source"] != "tco"])
    manifest = ix.read_manifest()
    manifest.pop("tco", None)
    ix.write_manifest(manifest)
    parts.append("### 6. Clean-up\n\nTCO chunks removed from index/ again (vectors kept in the cache, so re-adding costs nothing), "
                 "so the evaluation runs on the original corpus.\n")

    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(OUT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
