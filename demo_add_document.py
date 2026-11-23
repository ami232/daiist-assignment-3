"""Add-document demo (REQ-11.6): ask a question the corpus cannot answer, add the held-out
document through the agent (you approve it in the terminal), and ask again.

    uv run python demo_add_document.py

Run it in a real terminal: add_document is only allowed after you type "s". Results go to
eval/add_document_demo.json (full answers and traces) and eval/add_document_demo.md (readable).
"""
import asyncio
import csv
import json
import sys
from pathlib import Path

import agent

ROOT = Path(__file__).parent
QUESTION_ID = "q31"
DOCUMENT = "corpus/BOE-A-2026-7296.xml"      # Orden PJC/297/2026, arts. 18-19 (2026 RETA contribution brackets)
ADD_REQUEST = f"Añade al índice el documento {DOCUMENT}."
OUT_JSON = ROOT / "eval" / "add_document_demo.json"
OUT_MD = ROOT / "eval" / "add_document_demo.md"


def question_text(qid: str) -> str:
    with (ROOT / "eval" / "questions.csv").open(encoding="utf-8", newline="") as f:
        return next(row["question"] for row in csv.DictReader(f) if row["id"] == qid)


def quote(text: str) -> list[str]:
    return [f"> {line}" if line else ">" for line in text.splitlines()]


def write_markdown(steps: list[dict]) -> None:
    lines = ["# Demo de add_document", "",
             f"Pregunta {QUESTION_ID} antes y después de añadir `{DOCUMENT}` con `add_document`, "
             "en una sola sesión del agente (agent.py). Generado por `demo_add_document.py`.", ""]
    for step in steps:
        r = step["result"]
        lines += [f"## {step['label']}", "", f"**Mensaje:** {r['question']}", "", "**Herramientas:**", ""]
        for t in r["trace"]:
            if "call" in t:
                lines.append(f"- llamada `{t['call']}({json.dumps(t['args'], ensure_ascii=False)})`")
            elif t["result"] == "add_document" or t["status"] == "error":
                lines.append(f"- resultado `{t['result']}` ({t['status']}): {t['text'].strip()}")
            else:
                cites = ", ".join(agent.sources_in(t["text"])) or "(sin fragmentos)"
                lines.append(f"- resultado `{t['result']}`: {cites}")
        lines += ["", "**Respuesta:**", "", *quote(r["answer"]), "",
                  f"_Citas: {', '.join(r['citations']) or 'ninguna'} · búsquedas: {r['searches']} · "
                  f"tokens: {r['tokens']['total']} · {r['seconds']} s_", ""]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


async def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not sys.stdin.isatty():
        raise SystemExit("Ejecútalo en un terminal: hace falta tu aprobación para add_document.")
    question = question_text(QUESTION_ID)
    steps = []
    async with agent.open_agent(agent.ask_in_terminal) as a:
        for label, message in [("1. Antes de añadir el documento", question),
                               ("2. Petición de añadir el documento", ADD_REQUEST),
                               ("3. Después de añadir el documento", question)]:
            print(f"\n=== {label} ===\n{message}\n")
            result = await agent.ask(a, message)
            print(result["answer"])
            steps.append({"label": label, "result": result})
    OUT_JSON.write_text(json.dumps(steps, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(steps)
    print(f"\nGuardado en {OUT_JSON.relative_to(ROOT)} y {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    asyncio.run(main())
