"""
Rivaroxaban before-and-after demo: one unanswerable question, before and after
adding the held-out Xarelto label with the add_document tool.

    uv run python eval/rivaroxaban_demo.py            # asks you to approve add_document
    uv run python eval/rivaroxaban_demo.py --question "..."   # use another question

It works on a temporary COPY of index/, so the committed index (and therefore
the unanswerable questions in the evaluation) is not changed. Steps:
  1. copy index/ to a temp folder and point the server at it (CORPUS_INDEX_DIR);
  2. ask the question with agent.py (add_document refused);
  3. ask the agent to add corpus/held_out/rivaroxaban.xml; agent.py's approval
     step asks you to type y (this is the harness's approval guardrail);
  4. count the rivaroxaban chunks now in the copy;
  5. ask exactly the same question again.
Writes eval/rivaroxaban_demo.md and eval/rivaroxaban_demo.json with the real outputs.
Costs ~210 embeddings (the Xarelto label, section chunks) and a few model calls.
"""

import argparse
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_QUESTION = "My mother has just been switched to Xarelto 20 mg for atrial fibrillation. Should she take it with food?"
LABEL = "corpus/held_out/rivaroxaban.xml"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    workdir = Path(tempfile.mkdtemp(prefix="rivaroxaban-demo-"))
    shutil.copytree(ROOT / "index", workdir / "index")
    os.environ["CORPUS_INDEX_DIR"] = str(workdir / "index")  # read by index.py, in this process and the server
    sys.path.insert(0, str(ROOT))
    import agent  # noqa: E402
    import index  # noqa: E402

    index.download_corpus()  # makes sure the held-out label is on disk
    record = {"question": args.question, "timestamp": datetime.now(timezone.utc).isoformat(),
              "index_copy": str(workdir / "index"), "label_file": LABEL}

    def chunks_for(source: str) -> int:
        stored = index.get_collection(index.DEFAULT_DESIGN).get(where={"source": source}, include=[])
        return len(stored["ids"])

    record["chunks_before"] = {"total": index.get_collection(index.DEFAULT_DESIGN).count(),
                               "rivaroxaban": chunks_for("rivaroxaban")}
    print(f"1) Index copy: {record['chunks_before']}")

    print("2) Asking before adding the label ...")
    before = agent.run_agent(args.question, approve=agent.deny)
    print(before["answer"], "\n")

    print(f"3) Asking the agent to add {LABEL} (it will ask for your approval) ...")
    added = agent.run_agent(f"Please add the drug label file {LABEL} to the index.",
                            approve=agent.ask_in_terminal)
    add_calls = [t for t in added["trace"] if t["tool"] == "add_document"]
    print(added["answer"], "\n")

    index._chroma = None  # reopen: the server process wrote to the copy
    record["chunks_after"] = {"total": index.get_collection(index.DEFAULT_DESIGN).count(),
                              "rivaroxaban": chunks_for("rivaroxaban")}
    print(f"4) Index copy now: {record['chunks_after']}")

    print("5) Asking the same question again ...")
    after = agent.run_agent(args.question, approve=agent.deny)
    print(after["answer"])

    def summary(result):
        return {"answer": result["answer"], "raw_answer": result["raw_answer"], "guardrail": result["guardrail"],
                "citations": [f"[{d} {s}]" for d, s in agent.cited(result["raw_answer"])],
                "retrieved": [f"[{d} {s}]" for d, s in agent.retrieved_passages(result["trace"])],
                "search_queries": [t["args"].get("query") for t in result["trace"] if t["tool"] == "search"],
                "model": result["model"], "tokens": result["tokens"], "seconds": result["seconds"]}

    record.update({"before": summary(before), "after": summary(after),
                   "add_document_calls": [{"args": t["args"], "output": t["output"], "error": t["error"]} for t in add_calls],
                   "add_reply": added["answer"]})
    (ROOT / "eval" / "rivaroxaban_demo.json").write_text(json.dumps(record, indent=1, ensure_ascii=False))

    added_ok = record["chunks_after"]["rivaroxaban"] > 0
    lines = ["# Rivaroxaban before-and-after demo", "",
             f"Run {record['timestamp']} on a temporary copy of index/ (the committed index is unchanged).", "",
             f"**Question:** {args.question}", "",
             "## Before", "", f"Index: {record['chunks_before']['total']} chunks, rivaroxaban chunks: {record['chunks_before']['rivaroxaban']}", "",
             "```", before["answer"], "```", "",
             f"Retrieved: {', '.join(record['before']['retrieved']) or 'none'}", "",
             "## Adding the document", "", f"File: `{LABEL}` (Xarelto label, DailyMed set id {agent_setid()})", "",
             *[f"- add_document({c['args']}) -> {c['output'][:300]}" for c in record["add_document_calls"]],
             "" if add_calls else "- add_document was not called (approval refused or the agent did not call it)", "",
             f"Index after: {record['chunks_after']['total']} chunks, rivaroxaban chunks: {record['chunks_after']['rivaroxaban']}"
             + ("" if added_ok else "  **(nothing was added: the after-answer below is not a valid demo)**"), "",
             "## After", "", "```", after["answer"], "```", "",
             f"Citations: {', '.join(record['after']['citations']) or 'none'}", "",
             f"Retrieved: {', '.join(record['after']['retrieved']) or 'none'}", ""]
    (ROOT / "eval" / "rivaroxaban_demo.md").write_text("\n".join(lines), encoding="utf-8")
    print("\nwrote eval/rivaroxaban_demo.md and eval/rivaroxaban_demo.json")
    shutil.rmtree(workdir, ignore_errors=True)


def agent_setid() -> str:
    sys.path.insert(0, str(ROOT))
    import index
    return index.HELD_OUT["rivaroxaban"]


if __name__ == "__main__":
    main()
