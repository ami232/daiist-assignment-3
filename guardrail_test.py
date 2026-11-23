"""
Shows the citation guard (agent.py, guardrail 3) firing.

In the real runs the agent never cited a passage it had not retrieved, so the
guard never had to act (35 test questions + 5 questions written to provoke it).
This script runs a REAL search, then gives the guard's own check four answers:
a correct one and three with the kinds of mistakes it is meant to catch.
Output: eval/guardrail_test.md
"""
from pathlib import Path

import agent
import index
import server

QUESTION = "¿Cuántos meses de fianza me pueden exigir al alquilar un piso como vivienda?"
CASES = {
    "Correct citation": "Una mensualidad de renta [LAU (Ley 29/1994), Artículo 36. Fianza].",
    "Invented source (not in the corpus)": "Una mensualidad de renta [Código Civil, Artículo 1561].",
    "Real law, article not retrieved": "Una mensualidad de renta [LAU (Ley 29/1994), Artículo 99].",
    "No citation at all": "Una mensualidad de renta, y el casero puede pedir dos más como garantía.",
}


def decision(answer: str, hits: list[dict]) -> tuple[list, list, str]:
    valid, invalid = agent.check_citations(answer, hits)
    if agent.is_refusal(answer) or (valid and not invalid):
        return valid, invalid, "passes"
    return valid, invalid, "FIRES: the agent is asked to fix it once; if it fails again the answer is replaced by a refusal"


def main() -> None:
    tool_output = server.format_results(index.search(QUESTION, k=server.TOP_K))
    hits = agent.parse_hits(tool_output)
    lines = ["# Citation guard test", "", f"**Question:** {QUESTION}", "",
             "**Passages the search tool really returned:**", ""]
    lines += [f"- {h['source']}, {h['location']}" for h in hits]
    lines += ["", "| answer given to the guard | valid citations | invalid citations | guard |", "|---|---|---|---|"]
    for name, ans in CASES.items():
        valid, invalid, verdict = decision(ans, hits)
        lines.append(f"| **{name}**: {ans} | {valid or '—'} | {invalid or '—'} | {verdict} |")
        print(f"{name:40s} -> {verdict[:5]}")
    Path("eval/guardrail_test.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote eval/guardrail_test.md")


if __name__ == "__main__":
    main()
