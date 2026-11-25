"""
Grade the assistant's answers by hand, one at a time, and save them in eval/human_labels.csv.

    uv run python label.py

For each answer it shows the question, the reference answer you will compare with, the assistant's
answer and the text of the passages the answer cites. You type your own verdict:

    correct    1 = the answer says what the reference says (both parts for a "multi" question;
                   for an unanswerable question: the assistant said it does not know)
               0 = it is wrong, incomplete or invents something
    supported  1 = every claim is backed by the cited text shown below it
               0 = something is not in the cited text

It never shows the LLM judge's verdict, so your grades stay independent. Progress is saved after
every answer: stop with q and continue another day, it skips what you have already graded.
You need at least 20 graded answers; the answerable questions come first.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
LABELS = EVAL / "human_labels.csv"
MIN_LABELS = 20
SHOW_CHARS = 1800

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass


def unit(location: str) -> str:
    m = re.search(r"(Article\s+\d+[a-z]?|Recital\s+\d+|Annex\s+[IVXLC0-9]+)", location or "", re.I)
    return re.sub(r"\s+", " ", m.group(1)).lower() if m else (location or "").strip().lower()


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def read_labels() -> dict[str, dict]:
    if not LABELS.is_file():
        return {}
    with LABELS.open(newline="", encoding="utf-8") as f:
        return {r["id"].strip(): r for r in csv.DictReader(f) if r.get("id", "").strip()}


def write_labels(labels: dict[str, dict]) -> None:
    with LABELS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "correct", "supported", "notes"])
        w.writeheader()
        for key in sorted(labels):
            w.writerow({k: labels[key].get(k, "") for k in ("id", "correct", "supported", "notes")})


def ask_bit(prompt: str, allow_skip: bool = True) -> str:
    extra = ", s = saltar esta pregunta" if allow_skip else ""
    while True:
        value = input(f"{prompt} [1 = sí, 0 = no{extra}, q = salir]: ").strip().lower()
        if value in {"1", "0", "q"} or (allow_skip and value == "s"):
            return value
        print("  Escribe 1, 0" + (", s" if allow_skip else "") + " o q.")


def cited_passages(record: dict) -> list[dict]:
    """The retrieved passages that the answer cites, falling back to the top ones if none matches."""
    found, seen = [], set()
    for source, location in record.get("citations") or []:
        for hit in record.get("retrieved") or []:
            if norm(hit["source"]) == norm(source) and unit(hit["location"]) == unit(location):
                key = (hit["source"], hit["location"])
                if key not in seen:
                    seen.add(key)
                    found.append(hit)
    return found


def show(question: dict, record: dict, done: int, total: int) -> None:
    line = "=" * 78
    print(f"\n{line}\n{question['id']}  ({question['kind']})   -   graded so far: {done}  (minimum {MIN_LABELS}), left: {total}\n{line}")
    print(f"\nPREGUNTA:\n{question['question']}")
    print(f"\nRESPUESTA DE REFERENCIA (la correcta):\n{question['reference_answer']}")
    print(f"\nRESPUESTA DEL ASISTENTE:\n{record['answer']}")
    passages = cited_passages(record)
    if passages:
        print("\nTEXTO CITADO (lo que hay en el documento):")
        for hit in passages:
            body = hit["body"]
            cut = body[:SHOW_CHARS] + (" [...]" if len(body) > SHOW_CHARS else "")
            print(f"\n  [{hit['source']} | {hit['location']}]\n  {cut}")
        if any(len(h["body"]) > SHOW_CHARS for h in passages):
            print('\n  (texto largo: para leerlo entero usa  uv run python index.py --show "GDPR Article 33"  cambiando el nombre)')
    else:
        print("\n(El asistente no cita ningún texto.)")
    print()


def main() -> None:
    questions_path, answers_path = EVAL / "questions.csv", EVAL / "answers.jsonl"
    if not questions_path.is_file() or not answers_path.is_file():
        raise SystemExit("Falta eval/answers.jsonl. Ejecuta primero:  uv run python main.py evaluate")
    with questions_path.open(newline="", encoding="utf-8") as f:
        questions = [r for r in csv.DictReader(f) if r.get("id", "").strip()]
    records = {}
    for line in answers_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            records[rec["id"]] = rec
    labels = read_labels()
    order = [q for q in questions if q["kind"] != "unanswerable"] + [q for q in questions if q["kind"] == "unanswerable"]
    pending = [q for q in order if q["id"] not in labels and q["id"] in records]
    print(__doc__)
    print(f"Ya tienes {len(labels)} respuestas etiquetadas. Quedan {len(pending)}.")
    for n, q in enumerate(pending):
        show(q, records[q["id"]], len(labels), len(pending) - n)
        correct = ask_bit("¿Es CORRECTA?")
        if correct == "q":
            break
        if correct == "s":
            continue
        supported = ask_bit("¿Está RESPALDADA por el texto citado?", allow_skip=False)
        if supported == "q":
            break
        notes = input("Nota (opcional, Enter para dejarla vacía): ").strip()
        labels[q["id"]] = {"id": q["id"], "correct": correct, "supported": supported, "notes": notes}
        write_labels(labels)
        print(f"  Guardado ({len(labels)} etiquetadas).")
    print(f"\nTienes {len(labels)} respuestas etiquetadas en eval/human_labels.csv.")
    if len(labels) >= MIN_LABELS:
        print("Ya llegas al mínimo. Ahora puedes lanzar de nuevo:  uv run python main.py evaluate")
    else:
        print(f"Te faltan {MIN_LABELS - len(labels)} para el mínimo. Vuelve a lanzar:  uv run python label.py")


if __name__ == "__main__":
    main()
