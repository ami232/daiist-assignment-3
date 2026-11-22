"""
Before/after demo for the add_document tool (REPORT.md, Adding a document).

q29 asks about US FDA labelling, which the EU corpus cannot answer. This:
1. asks q29 (before);
2. asks the agent to add the FDA Cosmetics Labeling Guide, refusing approval;
3. asks again, approving it;
4. asks q29 again (after), with AGENTS.md as it is and then with one line
   telling the agent the corpus now includes the FDA guide;
5. calls add_document once more with the same file (already indexed);
6. removes the FDA chunks, so the indexed corpus matches eval/questions.csv
   (where q29 is unanswerable).

Writes eval/add_document_demo.md. `uv run python demo_add_document.py`
"""

import json
from pathlib import Path

from agent import ask
from index import DEFAULT_DESIGN, collection

ROOT = Path(__file__).resolve().parent
FILE = "corpus/added/fda_cosmetics_labeling_guide.html"
URL = "https://www.fda.gov/cosmetics/cosmetics-labeling-regulations/cosmetics-labeling-guide"
Q29 = "What labelling requirements does the US FDA impose to sell a perfume in the United States?"
ADD = f"Please add the document {FILE} to the corpus."


def approver(decision: bool, log: list):
    def approve(tool, args):
        log.append(f"Approval asked: run `{tool}` with {json.dumps(args)} -> {'approved' if decision else 'refused'}")
        return decision
    return approve


def block(title: str, out: dict, log: list | None = None) -> str:
    lines = [f"### {title}", "", f"**Question:** {out['question']}", ""]
    lines += [f"- {entry}" for entry in (log or [])]
    lines += [f"- Tool calls: {json.dumps(out['trace'], ensure_ascii=False)}",
              f"- Guardrail: {out['guardrail'] or 'did not fire'}",
              f"- {out['tokens']['input'] + out['tokens']['output']} tokens, {out['seconds']} s", "",
              "**Answer:**", "", out["answer"], ""]
    return "\n".join(lines)


def main() -> None:
    if not (ROOT / FILE).exists():
        raise SystemExit(f"Download {URL} to {FILE} first.")
    md = ["# Adding a document: before and after", "",
          f"Document: FDA, *Cosmetics Labeling Guide*, {URL} (US government work, public domain).", ""]
    md.append(block("1. Before: q29 on the EU corpus", ask(Q29, approver(False, []))))
    log = []
    md.append(block("2. Add the document, approval refused", ask(ADD, approver(False, log)), log))
    log = []
    md.append(block("3. Add the document, approval given", ask(ADD, approver(True, log)), log))
    md.append(block("4. After: q29 again, same rules", ask(Q29, approver(False, []))))
    note = ("Corpus update: the corpus now also contains the FDA Cosmetics Labeling Guide "
            "(US labelling rules); search it for questions about the United States.")
    md += [f"Rule 5 of AGENTS.md describes the corpus as EU law only, so step 4 refuses without searching. "
           f"Step 4b adds one line to the system prompt, as the team would when it adds a document: *{note}*", ""]
    md.append(block("4b. After: q29 again, corpus description updated",
                    ask(Q29, approver(False, []), extra_rules=note)))
    from server import add_document
    md += ["### 5. The same file again (server tool called directly)", "", add_document(FILE), ""]
    col = collection(DEFAULT_DESIGN)
    ids = col.get(where={"file": Path(FILE).name}, include=[])["ids"]
    col.delete(ids=ids)
    md += ["### 6. Clean-up", "", f"Removed the {len(ids)} FDA passages again, so the indexed corpus matches "
           "the test set, where q29 is unanswerable.", ""]
    (ROOT / "eval" / "add_document_demo.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
