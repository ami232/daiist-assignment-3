"""Test the held-out PostgreSQL manifest specification in an isolated database copy."""
import asyncio
import json
import os
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch

from agent import answer_question, call_mcp, server_session
from evaluate import EVAL, read_csv, save
from index import database


async def main():
    question = next(q["question"] for q in read_csv(EVAL / "questions.csv") if q["id"] == "q30")
    held_out = EVAL / "held_out/backup-manifest-format.md"
    with tempfile.TemporaryDirectory() as folder:
        copied = Path(folder) / "experiment.db"
        with sqlite3.connect(database()) as original, sqlite3.connect(copied) as destination:
            original.backup(destination)
        with patch.dict(os.environ, {"PG_RAG_DB": str(copied)}):
            async with server_session() as session:
                before = await answer_question(question, session)
                added = await call_mcp(session, "add_document", {"path": str(held_out)})
                duplicate = await call_mcp(session, "add_document", {"path": str(held_out)})
                after = await answer_question(question, session)
    result = {"question": question, "before": before, "addition": added, "repeat": duplicate, "after": after}
    save(EVAL / "addition_demo.json", result)
    print(json.dumps({"before": before["answer"], "addition": added, "repeat": duplicate,
                      "after": after["answer"]}, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
