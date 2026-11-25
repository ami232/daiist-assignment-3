"""Demonstrate an approved addition in an isolated copy of the saved index.

Preview first; --approve records permission for the exact displayed file hash.
The original corpus, questions, answers and human ratings are never modified.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile

from api_key import load_api_key
from evaluation_support import corpus_fingerprint, digest
from index import chunk_file
from retrieval import ROOT, Store

FILES = (
    "api_key.py", "retrieval.py", "prepare_corpus.py", "index.py", "server.py",
    "agent.py", "answer_guardrails.py", "evaluation_support.py", "AGENTS.md",
    "project_config.json",
)

WORKER = r'''
import asyncio, json, os, sqlite3, sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from agent import ToolBridge, run_agent
from evaluation_support import code_checks, corpus_fingerprint
from retrieval import Store

async def main():
    output, document, question, expected_hash = sys.argv[1:]
    output, document = Path(output), Path(document).resolve(strict=True)
    settings = json.loads(Path("project_config.json").read_text())
    approvals = []
    def approve(preview):
        allowed = preview["sha256"] == expected_hash and Path(preview["path"]) == document
        approvals.append({**preview, "approved": allowed,
                          "authorization": "Explicit --approve for the exact previewed document"})
        return allowed
    parameters = StdioServerParameters(command=sys.executable, args=[str(Path("server.py").resolve())],
        cwd=str(Path.cwd()), env={"GEMINI_API_KEY": os.environ["GEMINI_API_KEY"],
                                 "RETRIEVAL_DESIGN": settings["selected_retrieval_design"]})
    try:
        async with stdio_client(parameters) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                bridge = ToolBridge(session, approval=approve)
                await bridge.invoke("add_document", {"path": str(document)})
                (output / "addition.json").write_text(json.dumps({"approvals": approvals,
                    "trace": bridge.trace}, indent=2) + "\n")
                if not bridge.trace or bridge.trace[-1]["status"] != "success":
                    raise RuntimeError("The addition did not complete; its trace is saved")
        result = await run_agent(question, design=settings["selected_retrieval_design"],
                                 approval=None, as_of=settings["evaluation_as_of"])
        with (output / "answer_attempts.jsonl").open("a") as stream:
            stream.write(json.dumps(result, ensure_ascii=False) + "\n")
        (output / "after_attempt.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        if result.get("primary_runtime_error") and result.get("draft") is None:
            raise RuntimeError("The after-answer request failed; resume when the provider is available")
        result["code_checks"] = code_checks(result)
        (output / "after_answer.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        (output / "after_index_status.json").write_text(json.dumps({"status": Store(create=False).status(),
            "corpus_sha256": corpus_fingerprint(Store(create=False))}, indent=2) + "\n")
        print("Saved the real addition trace and after-answer.", flush=True)
    finally:
        with sqlite3.connect("index/corpus.sqlite3") as source:
            with sqlite3.connect(output / "index_after.sqlite3") as target:
                source.backup(target)

asyncio.run(main())
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    parser.add_argument("--question-id", default="q03")
    parser.add_argument("--output", type=Path, default=ROOT / "eval/add_document_demo")
    parser.add_argument("--approve", action="store_true", help="Approve exactly the previewed file")
    args = parser.parse_args()
    document, output = args.document.resolve(strict=True), args.output.resolve()
    _, file_hash, chunks = chunk_file(document)
    preview = {"name": document.name, "sha256": file_hash, "bytes": document.stat().st_size,
               "chunks": len(chunks), "question_id": args.question_id,
               "isolated_index": True, "approved": args.approve}
    print(json.dumps(preview, indent=2), flush=True)
    if not args.approve:
        print("Preview only. Obtain explicit approval before rerunning with --approve.")
        return
    with (ROOT / "eval/questions.csv").open() as stream:
        question = next(q for q in csv.DictReader(stream) if q["id"] == args.question_id)
    if question["kind"] != "unanswerable":
        raise ValueError("Select an originally unanswerable question")
    before = next(json.loads(line) for line in (ROOT / "eval/answers.jsonl").read_text().splitlines()
                  if json.loads(line)["id"] == args.question_id)
    baseline = corpus_fingerprint(Store(create=False))
    state = {"baseline_sha256": baseline, "document_sha256": file_hash,
             "question": question, "code_sha256": {name: digest((ROOT / name).read_bytes()) for name in FILES}}
    output.mkdir(parents=True, exist_ok=True)
    state_path = output / "state.json"
    if state_path.exists() and json.loads(state_path.read_text()) != state:
        raise ValueError("Demo inputs changed; use a new output directory to preserve the old run")
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    (output / "before_answer.json").write_text(json.dumps(before, indent=2, ensure_ascii=False) + "\n")
    (output / "approved_preview.json").write_text(json.dumps(preview, indent=2) + "\n")
    if (output / "after_answer.json").exists():
        print("The completed demonstration is already saved; no calls repeated.")
        return
    with tempfile.TemporaryDirectory(prefix="financial-health-demo-") as temporary:
        workspace = Path(temporary)
        for name in FILES:
            shutil.copyfile(ROOT / name, workspace / name)
        (workspace / "index").mkdir()
        (workspace / "corpus").mkdir()
        isolated_document = workspace / "corpus" / document.name
        shutil.copyfile(document, isolated_document)
        checkpoint = output / "index_after.sqlite3"
        database = checkpoint if checkpoint.exists() else ROOT / "index/corpus.sqlite3"
        with sqlite3.connect(database) as source, sqlite3.connect(workspace / "index/corpus.sqlite3") as target:
            source.backup(target)
        worker = workspace / "demo_worker.py"
        worker.write_text(WORKER)
        env = dict(os.environ, GEMINI_API_KEY=load_api_key())
        env.pop("GEMINI_MODEL", None)
        result = subprocess.run([sys.executable, str(worker), str(output), str(isolated_document),
                                 question["question"], file_hash], cwd=workspace, env=env)
    if corpus_fingerprint(Store(create=False)) != baseline:
        raise RuntimeError("The baseline corpus unexpectedly changed")
    (output / "baseline_preserved.json").write_text(json.dumps({"corpus_sha256": baseline,
        "unchanged": True}, indent=2) + "\n")
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
