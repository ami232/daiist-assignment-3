"""
Assignment 3, step 8: add a document that answers an unanswerable question.

    uv run python add_document_demo.py

1. Asks the agent question u01 (apixaban is not in the corpus)       -> "before"
2. Asks the agent to add docs_to_add/apixaban.json, with no approval -> refused by the guardrail
3. Asks again; you approve in the terminal (type y)                  -> the label is indexed
4. Runs add_document a second time on the same file                  -> "Already indexed"
5. Asks u01 again                                                    -> "after"

Writes everything to eval/add_document_demo.md. Run it after `main.py evaluate`,
because afterwards u01 is no longer unanswerable. If apixaban is already indexed
(from an earlier run of this demo) it is removed first, so the demo can be repeated.
"""

import asyncio
import csv
from pathlib import Path

import index as pipeline
from agent import ask_approval, run

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "eval" / "add_document_demo.md"
DOC = "docs_to_add/apixaban.json"


def question(qid: str) -> str:
    with (ROOT / "eval" / "questions.csv").open(newline="", encoding="utf-8") as f:
        return next(r["question"] for r in csv.DictReader(f) if r["id"] == qid)


def block(title: str, result: dict) -> str:
    calls = "\n".join(f"- `{s['tool']}({s['args']})` -> {s['result'][:200].splitlines()[0]}" for s in result["trace"])
    return (f"## {title}\n\n**Question:** {result['question']}\n\n**Tool calls:**\n{calls or '- none'}\n\n"
            f"**Answer:**\n\n> {result['answer']}\n\n({result['tokens_in'] + result['tokens_out']} tokens, {result['seconds']} s)\n")


def remove(source: str) -> None:
    registry = pipeline.read_registry()
    if source in registry:
        for design in pipeline.DESIGNS:
            pipeline.collection(design).delete(where={"source": source})
        del registry[source]
        pipeline.write_registry(registry)
        print(f"(removed '{source}' from the index to start the demo clean)")


def main() -> None:
    pipeline.download_corpus()
    remove("apixaban")
    pipeline._chroma = None          # release the index before the agent's server opens it
    q = question("u01")
    parts = ["# Adding a document: before and after\n",
             f"Unanswerable question u01, document added: `{DOC}` (FDA label for apixaban, openFDA, public domain).\n"]

    print("1. before ...")
    parts.append(block("1. Before adding the document", asyncio.run(run(q))))

    add = f"Please add the document {DOC} to the corpus."
    print("2. add request, nobody approves ...")
    parts.append(block("2. Add request without approval (guardrail)", asyncio.run(run(add, approve=lambda p: False))))

    print("3. add request, you approve ...")
    parts.append(block("3. Add request, approved by a person in the terminal", asyncio.run(run(add, approve=ask_approval))))

    print("4. same file again ...")
    again = pipeline.add_file(ROOT / DOC)
    parts.append(f"## 4. Adding the same file again\n\n`add_document('{DOC}')` -> {again}\n")

    print("5. after ...")
    parts.append(block("5. After adding the document", asyncio.run(run(q))))

    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(OUT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
