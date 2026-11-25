"""
Before / after: add a document that answers one of your unanswerable questions.

    uv run python before_after.py q31 corpus/nis2.xhtml        # question id from eval/questions.csv
    uv run python before_after.py "your question" corpus/nis2.xhtml --yes

It works on a throw-away COPY of index/ (so the committed index and the evaluation stay as they
were), asks the question, asks the agent to add the file (you approve in the terminal, or pass
--yes), asks the question again, and writes eval/before_after.md for REPORT.md.

Adding a document embeds its passages: about 90 texts for NIS2, from the daily free quota.
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import shutil
import tempfile
from pathlib import Path

import agent
import index as ix

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "eval" / "before_after.md"


def lookup_question(text: str) -> str:
    path = ROOT / "eval" / "questions.csv"
    if path.is_file():
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row["id"].strip() == text.strip():
                    return row["question"]
    return text


def block(title: str, result: agent.AgentResult) -> str:
    calls = "; ".join(f"{c['name']}({c['args'].get('query') or c['args'].get('path', '')})" for c in result.tool_calls if not c.get("refused_by_limit"))
    return (f"### {title}\n\n{agent.format_answer(result)}\n\n"
            f"_Tool calls: {calls or 'none'}. Guardrails: {', '.join(result.guardrails) or 'none'}. "
            f"{result.total_tokens} tokens, {result.seconds:.1f}s._\n")


async def demo(question: str, file: str, approve, model=None) -> tuple[agent.AgentResult, agent.AgentResult, agent.AgentResult]:
    tmp = Path(tempfile.mkdtemp(prefix="index_copy_"))
    try:
        shutil.copytree(ix.INDEX_DIR, tmp / "index")
        env = {"RAG_INDEX_DIR": str(tmp / "index")}
        before = await agent.run_agent(question, approve=approve, model=model, server_env=env)
        added = await agent.run_agent(f"Please add the document {file} to the corpus.", approve=approve, model=model, server_env=env)
        after = await agent.run_agent(question, approve=approve, model=model, server_env=env)
        return before, added, after
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("question", help="a question id from eval/questions.csv, or the question itself")
    parser.add_argument("file", help="the document to add, inside the project folder, e.g. corpus/nis2.xhtml")
    parser.add_argument("--yes", action="store_true", help="approve the add_document call without asking")
    args = parser.parse_args()
    question = lookup_question(args.question)
    target = ROOT / args.file
    if not target.is_file():
        known = next((d for d in ix.DOCS if d.path.name == target.name), None)
        if known is None:
            raise SystemExit(f"{args.file} does not exist. Put the file inside the project folder first.")
        print(f"Downloading {known.source} ...")
        ix.download(known)
    before, added, after = asyncio.run(demo(question, args.file, agent.approve_all if args.yes else agent.ask_in_terminal))
    text = (f"# Before and after adding `{args.file}`\n\n**Question:** {question}\n\n"
            f"{block('Before', before)}\n{block('Adding the document (approval required)', added)}\n{block('After', after)}")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(text)
    print(f"\nWritten to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
