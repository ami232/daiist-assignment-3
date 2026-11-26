"""
Ver con detalle lo que hizo el agente en una pregunta de la evaluación:

    uv run python ver_respuesta.py q26
    uv run python ver_respuesta.py q26 --juez     # añade la nota del juez

Muestra la pregunta, cada búsqueda que hizo (consulta, licitación, fragmentos que
recibió), si saltó el guardarraíl de citas (con el texto que bloqueó) y la respuesta
final. Sirve para el análisis de fallos (eval/failures.csv) y para los ejemplos del
REPORT. Sin --juez no enseña la nota del juez, para no influir en tus notas a ciegas.
"""

import json
import sys

import config
from retrieval import parse_hits


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit(__doc__)
    qid = args[0]
    answers = config.EVAL_DIR / "answers.jsonl"
    recs = [json.loads(l) for l in answers.read_text(encoding="utf-8").splitlines() if l.strip()]
    rec = next((r for r in recs if r["id"] == qid), None)
    if not rec:
        raise SystemExit(f"No hay respuesta para {qid} en eval/answers.jsonl")

    print(f"=== {qid}: {rec['question']}\n")
    print(f"Búsquedas ({rec['tool_calls']} llamadas a herramientas):")
    for n, step in enumerate(rec["trace"], 1):
        args_ = step.get("args", {})
        if step.get("error") or str(step.get("result", "")).startswith("Error"):
            print(f"  {n}. {step['tool']} {args_} -> ERROR: {step.get('result', '')[:120]}")
            continue
        hits = parse_hits(step.get("result", "")) if step["tool"] == "search" else []
        cites = ", ".join(f"[{h['doc_id']}, p. {h['page_start']}]" for h in hits) or step.get("result", "")[:120]
        print(f"  {n}. {step['tool']} {args_}\n     recibió: {cites}")

    g = rec["guardrail"]
    if g.get("fired"):
        print("\nGUARDARRAÍL DE CITAS: " + ("BLOQUEÓ la respuesta" if g.get("blocked") else "pidió corregirla"))
        for p in g.get("problems", []):
            print(f"  - {p}")
        if g.get("original_answer"):
            print("\n--- Respuesta original (la que detectó el guardarraíl) ---\n" + g["original_answer"])
        if g.get("second_answer"):
            print("\n--- Segundo intento ---\n" + g["second_answer"])

    print("\n--- Respuesta final ---\n" + rec["answer"])
    print(f"\n[{rec['total_tokens']} tokens · {rec['seconds']} s]")

    if "--juez" in sys.argv:
        judge = config.EVAL_DIR / "judge.jsonl"
        verdicts = [json.loads(l) for l in judge.read_text(encoding="utf-8").splitlines() if l.strip()] if judge.exists() else []
        v = next((x for x in reversed(verdicts) if x["id"] == qid), None)
        print("\nJuez: " + (f"correct={v['correct']} supported={v['supported']} · {v['reason']}" if v else
                             "sin veredicto (los rechazos los puntúa el código, no el juez)"))


if __name__ == "__main__":
    main()
