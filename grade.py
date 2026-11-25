"""
Assignment 3: grade the agent's answers yourself. `uv run python grade.py`

Shows one answer at a time (question, reference answer, agent answer, the
cited passages in full and short snippets of the other retrieved passages)
WITHOUT the judge's verdict, asks for
correct 1/0, supported 1/0 and notes, and appends to eval/human_labels.csv.
Stop any time with q or Ctrl-C; the next run continues with ungraded answers.

    uv run python grade.py            # ungraded answers, in a fixed shuffled order
    uv run python grade.py q07 q23    # only these ids
    uv run python grade.py --redo q07 # grade these again; the old rows are replaced
    uv run python grade.py --redo     # grade every graded answer again
"""

import csv
import random
import sys
import textwrap

import evaluate

COLUMNS = ["id", "correct", "supported", "notes"]
WIDTH = 96


def graded_ids() -> set[str]:
    if not evaluate.HUMAN.exists():
        return set()
    with evaluate.HUMAN.open(newline="", encoding="utf-8") as f:
        return {r["id"].strip() for r in csv.DictReader(f) if (r.get("id") or "").strip()}


def wrap(text: str, indent: str = "  ") -> str:
    lines = []
    for paragraph in text.strip().splitlines():
        lines.append(textwrap.fill(paragraph, WIDTH, initial_indent=indent, subsequent_indent=indent) or indent)
    return "\n".join(lines)


def snippet(chunk: dict, cited: set[tuple[str, str]], words: int = 70) -> str:
    """Cited passages in full (the judge sees them in full too); the rest cut to `words`."""
    tokens = chunk["text"].split()
    is_cited = any((chunk["doc_id"], loc) in cited for loc in chunk["locations"])
    if is_cited:
        words = len(tokens)
    text = " ".join(tokens[:words]) + (" ... [cut, type f for the full text]" if len(tokens) > words else "")
    mark = "*" if is_cited else " "
    return f" {mark}[{chunk['doc_id']} | {'; '.join(chunk['locations'])}]\n{wrap(text, '     ')}"


def ask_bit(prompt: str) -> str:
    while True:
        reply = input(prompt).strip().lower()
        if reply in ("1", "0", "q", "s", "f"):
            return reply
        print("    type 1, 0, s (skip), f (full retrieved text) or q (quit)")


def main() -> None:
    questions = evaluate.read_questions()
    rows = evaluate.current_answers(questions)
    if not rows:
        raise SystemExit("No answers yet. Run `uv run python main.py evaluate` first.")
    done = graded_ids()
    redo = "--redo" in sys.argv[1:]
    wanted = {a for a in sys.argv[1:] if a != "--redo"}
    if redo:
        todo = [r for r in rows if r["id"] in done and (not wanted or r["id"] in wanted)]
    else:
        todo = [r for r in rows if r["id"] not in done and (not wanted or r["id"] in wanted)]
    random.Random(3).shuffle(todo)  # mixed kinds, same order every run
    print(f"{len(done)} graded, {len(todo)} to grade. The brief asks for at least 20.")
    print("correct   = right against the reference (or a proper refusal for an unanswerable question)")
    print("supported = every claim is in the retrieved text (starred passages are the cited ones,")
    print("            shown in full; the others are cut to 70 words, type f to see them in full)\n")

    if not evaluate.HUMAN.exists() or evaluate.HUMAN.stat().st_size == 0:
        with evaluate.HUMAN.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(COLUMNS)

    for number, row in enumerate(todo, start=1):
        cited = set(evaluate.rag.parse_citations(row["answer"]))
        print("=" * WIDTH)
        print(f"{row['id']}  ({row['kind']})   [{number}/{len(todo)}]")
        print(f"\nQUESTION\n{wrap(row['question'])}")
        print(f"\nREFERENCE ANSWER\n{wrap(row['reference_answer'])}")
        print(f"\nAGENT ANSWER\n{wrap(row['answer'])}")
        print(f"\nRETRIEVED ({len(row['retrieved'])} passages, * = cited)")
        for chunk in row["retrieved"]:
            print(snippet(chunk, cited))
        print()
        try:
            correct = ask_bit("  correct?   [1/0, s skip, f full text, q quit] ")
            while correct == "f":
                for chunk in row["retrieved"]:
                    print(snippet(chunk, cited, words=10_000))
                correct = ask_bit("  correct?   [1/0, s skip, q quit] ")
            if correct == "q":
                break
            if correct == "s":
                continue
            supported = ask_bit("  supported? [1/0] ")
            while supported not in ("1", "0"):
                supported = ask_bit("  supported? [1/0] ")
            needs_note = "0" in (correct, supported)
            notes = input("  notes" + (" (why 0)" if needs_note else " (optional)") + ": ").strip()
            while needs_note and not notes:
                notes = input("  a note is needed for every 0: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if redo:  # replace the old row of this id, keep the order of the file
            with evaluate.HUMAN.open(newline="", encoding="utf-8") as f:
                old = [r for r in csv.reader(f)]
            new = [[row["id"], correct, supported, notes] if r and r[0].strip() == row["id"] else r for r in old]
            with evaluate.HUMAN.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(new)
        else:
            with evaluate.HUMAN.open("a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([row["id"], correct, supported, notes])
        print("  saved.\n")

    print(f"\n{len(graded_ids())} answers graded in eval/human_labels.csv. "
          "Run `uv run python main.py evaluate` to compare with the judge.")


if __name__ == "__main__":
    main()
