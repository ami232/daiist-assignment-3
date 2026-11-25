"""
Before/after demo for the add-document tool: `uv run python demo_add_document.py`

1. Copies index/ to a temporary folder, so the committed index (and therefore
   the evaluation) stays exactly as graded.
2. Asks the agent an unanswerable question (Regulation Best Interest's care
   obligation, q37): it should say the corpus does not cover it.
3. Downloads Regulation Best Interest (17 CFR 240.15l-1) and asks the agent to
   add it. The approval step asks YOU at the terminal (type y).
4. Asks the same question again: now it should answer with citations.
5. Asks to add the same file again: shows the "already indexed" behaviour.

Writes eval/add_document_demo.md.
"""

import asyncio
import os
import shutil
import tempfile
from pathlib import Path

from settings import CORPUS_DIR, EVAL_DIR, ROOT

QUESTION = "Under Regulation Best Interest, what does a broker-dealer's care obligation require?"
URL = "https://www.ecfr.gov/api/versioner/v1/full/2026-11-16/title-17.xml?section=240.15l-1"
FILE = CORPUS_DIR / "extra" / "reg-bi.xml"


def download() -> None:
    import httpx
    from index import HEADERS

    if FILE.is_file():
        return
    FILE.parent.mkdir(parents=True, exist_ok=True)
    response = httpx.get(URL, headers=HEADERS, timeout=120, follow_redirects=True)
    response.raise_for_status()
    FILE.write_bytes(response.content)


async def run() -> str:
    from agent import Harness, render

    rel = FILE.relative_to(ROOT)
    out = ["# Adding a document: before and after\n", f"Question: **{QUESTION}**\n"]
    async with Harness() as harness:
        before = await harness.ask(QUESTION)
        out += ["## Before\n", "```", render(before), "```\n"]
        add = await harness.ask(f"Please add the document at {rel} to the corpus.")
        out += ["## Adding the file (approval asked at the terminal)\n", "```", render(add), "```",
                "Tool calls: " + "; ".join(f"{c['tool']}({c['args']}) approved={c.get('approved')} -> {c['result'][:300]}"
                                            for c in add["trace"]) + "\n"]
        after = await harness.ask(QUESTION)
        out += ["## After\n", "```", render(after), "```\n"]
        again = await harness.ask(f"Please add the document at {rel} to the corpus.")
        out += ["## Adding the same file again\n",
                "Tool calls: " + "; ".join(f"{c['tool']} -> {c['result'][:300]}" for c in again["trace"]) + "\n"]
    return "\n".join(out)


def main() -> None:
    download()
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(ROOT / "index", Path(tmp) / "index")
        os.environ["RAG_INDEX_DIR"] = str(Path(tmp) / "index")  # the server subprocess inherits this
        report = asyncio.run(run())
    (EVAL_DIR / "add_document_demo.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
