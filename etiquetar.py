"""
Tus notas a ciegas, una respuesta cada vez (paso "human labels" del enunciado):

    uv run python etiquetar.py            # sigue por la primera respuesta sin nota
    uv run python etiquetar.py q12        # empieza en q12

Para cada respuesta del agente enseña la pregunta, tu respuesta de referencia, la
respuesta del agente y los fragmentos que recuperó (la evidencia), y te pide:

    correct   1/0  ¿dice lo mismo que la referencia? (o, si no tiene respuesta, ¿lo reconoce?)
    supported 1/0  ¿TODO lo que afirma aparece en la evidencia?
    notes          por qué, obligatorio cuando pones algún 0

Usa los mismos criterios que tu rúbrica (eval/rubric.md). Guarda cada nota al momento
en eval/human_labels.csv: puedes salir con "q" y seguir otro día. NUNCA enseña la nota
del juez, para que tus notas sean a ciegas.
"""

import csv
import json
import sys
import textwrap

import config
from retrieval import find_citations

LABELS = config.EVAL_DIR / "human_labels.csv"
FIELDS = ["id", "correct", "supported", "notes"]
WIDTH = 100


def wrap(text: str, indent: str = "  ") -> str:
    out = []
    for para in str(text).splitlines() or [""]:
        out.append(textwrap.fill(para, WIDTH, initial_indent=indent, subsequent_indent=indent) if para.strip() else "")
    return "\n".join(out)


def ask(prompt: str, valid: set[str]) -> str:
    while True:
        value = input(prompt).strip().lower()
        if value in valid:
            return value
        print(f"  Escribe una de estas opciones: {', '.join(sorted(valid))}")


def load_labels() -> dict[str, dict]:
    if not LABELS.exists():
        return {}
    with LABELS.open(newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f) if (r.get("id") or "").strip()}


def save_labels(labels: dict[str, dict], order: list[str]) -> None:
    rank = {qid: i for i, qid in enumerate(order)}
    rows = sorted(labels.values(), key=lambda r: rank.get(r["id"], 999))
    with LABELS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def show(q: dict, rec: dict, all_evidence: bool) -> None:
    print("\n" + "=" * WIDTH)
    print(f"{q['id']} · tipo {q['kind']}")
    print("PREGUNTA:\n" + wrap(q["question"]))
    print("TU RESPUESTA DE REFERENCIA:\n" + wrap(q["reference_answer"]))
    print("RESPUESTA DEL AGENTE:\n" + wrap(rec["answer"]))

    hits = rec.get("retrieved", [])
    cited = set(find_citations(rec["answer"]))
    shown = 0
    print(f"\nEVIDENCIA ({len(hits)} fragmentos recuperados):")
    for h in hits:
        is_cited = any(d == h["doc_id"] and h["page_start"] <= p <= h["page_end"] for d, p in cited)
        tag = f"[{h['doc_id']}, p. {h['page_start']}]"
        if is_cited or all_evidence:
            print(f"\n  {tag}{'  <- citado en la respuesta' if is_cited else ''}\n" + wrap(h["text"], "    "))
            shown += 1
        else:
            print(f"  {tag} (no citado; escribe 't' para verlo)")
    if not hits:
        print("  (el agente no recuperó nada)")


def main() -> None:
    with (config.EVAL_DIR / "questions.csv").open(newline="", encoding="utf-8") as f:
        questions = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    answers_path = config.EVAL_DIR / "answers.jsonl"
    if not answers_path.exists():
        raise SystemExit("Aún no hay respuestas: ejecuta antes `uv run python main.py evaluate`.")
    answers = {}
    for line in answers_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            answers[r["id"]] = r

    order = [q["id"] for q in questions if q["id"] in answers]
    labels = load_labels()
    start = sys.argv[1] if len(sys.argv) > 1 else None
    todo = order[order.index(start):] if start in order else [i for i in order if i not in labels]
    by_id = {q["id"]: q for q in questions}

    print(__doc__)
    print(f"Llevas {len(labels)} notas (el mínimo son 20). Quedan {len(todo)} respuestas en la cola.")
    for qid in todo:
        q, rec = by_id[qid], answers[qid]
        all_evidence = False
        show(q, rec, all_evidence)
        if qid in labels:
            print(f"\n(Ya tenías nota: correct={labels[qid]['correct']} supported={labels[qid]['supported']})")
        while True:
            c = ask("\ncorrect? [1 = sí / 0 = no / t = ver toda la evidencia / s = saltar / q = salir] ",
                    {"1", "0", "t", "s", "q"})
            if c == "t":
                all_evidence = True
                show(q, rec, all_evidence)
                continue
            break
        if c == "q":
            break
        if c == "s":
            continue
        s = ask("supported? [1 = todo está en la evidencia / 0 = algo no está] ", {"1", "0"})
        note = input("notes (por qué; obligatorio si has puesto algún 0): ").strip()
        while (c == "0" or s == "0") and not note:
            note = input("  Escribe por qué has puesto un 0: ").strip()
        labels[qid] = {"id": qid, "correct": c, "supported": s, "notes": note}
        save_labels(labels, order)
        print(f"  Guardado. Llevas {len(labels)} notas.")

    print(f"\nTotal: {len(labels)} notas en eval/human_labels.csv.")
    if len(labels) >= 20:
        print("Ya tienes las 20 mínimas. Vuelve a ejecutar `uv run python main.py evaluate` para ver el acuerdo con el juez.")


if __name__ == "__main__":
    main()
