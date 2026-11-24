"""
Assignment 3: add_document demo (before and after).

Asks q32, which the initial corpus cannot answer, then asks the agent to add
the held-out report "Electric Car Markets in a Time of Uncertainty" (ECMU2026,
July 2026), and asks q32 again. Adding the file needs the user's approval in
the terminal (guardrail 1 in agent.py), so run it yourself:

    uv run python demo_add_document.py

Writes eval/add_document_demo.md. Run it once: after the file is added, a
second run finds it "Already indexed".
"""

from __future__ import annotations

import asyncio
import json
from datetime import date
from pathlib import Path

import agent
import index as ix

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "eval" / "add_document_demo.md"
Q32 = ("By what percentage did global electric car sales change in the second quarter of 2026 "
       "compared with the second quarter of 2025?")
ADD = "Please add the file corpus/ElectricCarMarketsinaTimeofUncertainty.pdf to the corpus."


def documents() -> list[str]:
    return sorted(ix.load_documents())  # registry keyed by doc_id


def section(title: str, prompt: str, r: agent.AgentResult) -> list[str]:
    out = [f"## {title}", "", f"**User:** {prompt}", ""]
    for call in r.trace:
        if call["tool"] == "search":
            hits = ", ".join(f"{d} p.{p}" + (f"-{e}" if e != p else "")
                             for d, p, e in agent.retrieved_pages([call]))
            out.append(f"- `search({json.dumps(call['args']['query'])})` → {hits}")
        else:
            out.append(f"- `{call['tool']}({json.dumps(call['args'])})` → {call['result']}")
    out += ["", "**Agent:**", "", "> " + r.answer.replace("\n", "\n> "), "",
            f"*{len(r.trace)} tool calls, {r.model_calls} model calls, "
            f"{r.input_tokens + r.output_tokens} tokens, {r.seconds}s, citation check: {r.guardrail}*", ""]
    return out


async def main() -> None:
    before_docs = documents()
    async with agent.CorpusAgent() as corpus_agent:   # terminal approval for add_document
        print("1/3 Asking q32 before adding the document...")
        before = await corpus_agent.ask(Q32)
        print(agent.format_result(before), "\n")
        print("2/3 Asking the agent to add the document (you will be asked to approve)...")
        added = await corpus_agent.ask(ADD)
        print(agent.format_result(added), "\n")
        print("3/3 Asking q32 again...")
        after = await corpus_agent.ask(Q32)
        print(agent.format_result(after), "\n")
    after_docs = documents()

    out = ["# add_document demo: q32 before and after", "",
           f"Run on {date.today().isoformat()} with `demo_add_document.py` (agent: `{agent.MODEL}`). "
           "q32 is one of the unanswerable questions of the test set; the held-out report "
           "*Electric Car Markets in a Time of Uncertainty* (IEA, July 2026, ECMU2026) answers it.", "",
           f"Documents in the index before: {', '.join(before_docs)}. After: {', '.join(after_docs)}.", ""]
    out += section("1. Before", Q32, before)
    out += section("2. Adding the document (approval asked in the terminal)", ADD, added)
    out += section("3. After", Q32, after)
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Saved {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    asyncio.run(main())
