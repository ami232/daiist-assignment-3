"""Before/after experiment in an isolated copy, leaving baseline evaluation intact.

python demo_add_document.py qNN corpus/approved-additional-document.md
Jimena chooses the previously unanswerable question and registers an additional
public, licensed document in corpus_config.json before running this command.
"""

import argparse
import asyncio
import json
import shutil
import sqlite3
import tempfile
from pathlib import Path

from agent import AgentRunner, terminal_approval
from api_key import load_api_key
from evaluate import atomic_json, read_questions
from runtime import ROOT, read_config


async def main(
    question_id: str,
    document: str,
    *,
    questions_file=None,
    development=False,
    approval=terminal_approval,
    approval_record=None,
):
    questions = read_questions(
        questions_file or ROOT / "eval/questions.csv", enforce_minimum=not development
    )
    question = next((q for q in questions if q["id"] == question_id), None)
    if question is None or question["kind"] != "unanswerable":
        raise ValueError("Choose one of your baseline unanswerable questions.")
    config = read_config()
    proposed = next(
        (d for d in config.get("additional_documents", []) if d["path"] == document),
        None,
    )
    if proposed is None:
        raise ValueError(
            "Register this document and its provenance in additional_documents first."
        )
    load_api_key()  # pass to subprocesses through the environment; never copy .env
    with tempfile.TemporaryDirectory(prefix="assignment3-demo-") as temporary:
        root = Path(temporary)
        for name in [
            "server.py",
            "runtime.py",
            "index.py",
            "ingestion.py",
            "api_key.py",
            "AGENTS.md",
            "corpus_config.json",
            "policy_config.json",
        ]:
            shutil.copy2(ROOT / name, root / name)
        (root / "index").mkdir()
        for file in (ROOT / "index").iterdir():
            if file.is_file() and file.name not in {
                "vectors.sqlite3",
                "vectors.sqlite3-journal",
                "vectors.sqlite3-wal",
                "vectors.sqlite3-shm",
            }:
                shutil.copy2(file, root / "index" / file.name)
        with (
            sqlite3.connect(ROOT / "index" / "vectors.sqlite3") as source_db,
            sqlite3.connect(root / "index" / "vectors.sqlite3") as target_db,
        ):
            source_db.backup(target_db)
        for doc in config["documents"] + [proposed]:
            path = Path(doc["path"])
            if path.is_absolute() or not (ROOT / path).resolve().is_relative_to(
                (ROOT / "corpus").resolve()
            ):
                raise ValueError(
                    "Demo requires registered relative paths under corpus/."
                )
            (root / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / path, root / path)
        async with AgentRunner(root, approval=approval) as runner:
            before = await runner.ask(question["question"])
            adder = runner.wrap(
                next(
                    t
                    for t in (await runner.session.list_tools()).tools
                    if t.name == "add_document"
                )
            )
            added = json.loads(await adder.ainvoke({"path": document}))
            addition_trace = list(runner.trace)
            if "error" in added:
                raise ValueError(added["error"])
            after = await runner.ask(question["question"])
        result = {
            "question_id": question_id,
            "question": question["question"],
            "document": proposed,
            "before": before,
            "addition": added,
            "addition_trace": addition_trace,
            "after": after,
            "before_refused": before["refused"],
            "after_refused": after["refused"],
            "interpretation": "Jimena must inspect evidence and explain the change. An answer change alone does not prove correctness.",
            "baseline_unchanged": True,
            "role": "development engineering check"
            if development
            else "submission experiment",
            "approval_record": approval_record,
        }
        atomic_json(
            ROOT / ("review" if development else "eval") / "before_after.json", result
        )
        print(
            json.dumps(
                {
                    "before": before["answer"],
                    "after": after["answer"],
                    "addition": added,
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question_id")
    parser.add_argument("document")
    args = parser.parse_args()
    asyncio.run(main(args.question_id, args.document))
