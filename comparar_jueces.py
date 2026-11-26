"""
Compara los dos jueces que has usado, sin llamar a ninguna API:

    uv run python comparar_jueces.py

El primer juez (config.EARLIER_JUDGE_MODEL, gemini-3.6-flash) se quedó sin cuota gratuita
tras puntuar unas cuantas respuestas. El juez final (config.JUDGE_MODEL) las puntuó todas.
Este script toma las respuestas que puntuaron LOS DOS y mira en cuántas coinciden, y cómo
coincide cada uno con tus notas (human_labels.csv). Lo guarda en eval/judges_comparison.md.
"""

import csv
import json

import config
from evaluate import ANSWERS, HUMAN, JUDGE, RUBRIC, kappa, load_questions, read_jsonl, sha


def verdicts_for(model: str, questions: list[dict], answers: dict, cached: dict, rubric: str) -> dict:
    """Notas de un juez concreto para las respuestas ACTUALES (misma clave que run_judge)."""
    key_base = sha(rubric + model)
    out = {}
    for q in questions:
        rec = answers.get(q["id"])
        if rec and not rec["refusal"]:
            v = cached.get(f"{q['id']}|{key_base}|{sha(rec['answer'])}")
            if v:
                out[q["id"]] = v
    return out


def agreement(a: dict, b: dict, ids: list[str], field: str) -> str:
    x = [int(a[i][field]) for i in ids]
    y = [int(b[i][field]) for i in ids]
    same = sum(p == q for p, q in zip(x, y))
    return f"{same}/{len(ids)} (kappa {kappa(x, y)})"


def main() -> None:
    questions = load_questions()
    answers = {r["id"]: r for r in read_jsonl(ANSWERS)}
    cached = {r["key"]: r for r in read_jsonl(JUDGE)}
    rubric = RUBRIC.read_text(encoding="utf-8")
    early, final = config.EARLIER_JUDGE_MODEL, config.JUDGE_MODEL
    a = verdicts_for(early, questions, answers, cached, rubric)
    b = verdicts_for(final, questions, answers, cached, rubric)
    human = {}
    if HUMAN.exists():
        with HUMAN.open(newline="", encoding="utf-8") as f:
            human = {r["id"]: r for r in csv.DictReader(f) if (r.get("correct") or "").strip()}

    both = [q["id"] for q in questions if q["id"] in a and q["id"] in b]
    md = [f"# Comparación de jueces: `{early}` y `{final}`\n",
          f"Respuestas (no rechazos) puntuadas por `{early}`: {len(a)} · por `{final}`: {len(b)} · "
          f"por los dos: {len(both)}.\n"]
    if both:
        md += ["## Acuerdo entre los dos jueces\n",
               f"- correct: {agreement(a, b, both, 'correct')}",
               f"- supported: {agreement(a, b, both, 'supported')}\n"]
        with_h = [i for i in both if i in human]
        if with_h:
            md += [f"## Acuerdo con tus notas en esas {len(with_h)} respuestas\n",
                   "| Juez | correct | supported |", "|---|---|---|"]
            for name, v in ((early, a), (final, b)):
                md.append(f"| `{name}` | {agreement(v, human, with_h, 'correct')} | "
                          f"{agreement(v, human, with_h, 'supported')} |")
            md.append("")
        md.append("## Respuestas en las que los jueces no coinciden\n")
        diff = [i for i in both if (a[i]["correct"], a[i]["supported"]) != (b[i]["correct"], b[i]["supported"])]
        if not diff:
            md.append("(ninguna)\n")
        for i in diff:
            h = human.get(i)
            hum = f"{h['correct']}/{h['supported']}" if h else "sin nota"
            md += [f"- **{i}** · tú {hum} · `{early}` {a[i]['correct']}/{a[i]['supported']} · "
                   f"`{final}` {b[i]['correct']}/{b[i]['supported']}",
                   f"  - `{early}`: {a[i].get('reason', '')}",
                   f"  - `{final}`: {b[i].get('reason', '')}"]
    text = "\n".join(md) + "\n"
    (config.EVAL_DIR / "judges_comparison.md").write_text(text, encoding="utf-8")
    print(text)
    print("Guardado en eval/judges_comparison.md")


if __name__ == "__main__":
    main()
