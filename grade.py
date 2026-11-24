"""
Assignment 3: grade the agent's answers yourself. `uv run python grade.py`

Shows one answer at a time (question, reference answer, agent answer, short
snippets of what it retrieved) WITHOUT the judge's verdict, asks for
correct 1/0, supported 1/0 and notes, and appends to eval/human_labels.csv.
Stop any time with q or Ctrl-C; the next run continues with ungraded answers.

    uv run python grade.py            # ungraded answers, in a fixed shuffled order
    uv run python grade.py q07 q23    # only these ids
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
    tokens = chunk["text"].split()
    text = " ".join(tokens[:words]) + (" ..." if len(tokens) > words else "")
    mark = "*" if any((chunk["doc_id"], loc) in cited for loc in chunk["locations"]) else " "
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
    wanted = set(sys.argv[1:])
    todo = [r for r in rows if r["id"] not in done and (not wanted or r["id"] in wanted)]
    random.Random(3).shuffle(todo)  # mixed kinds, same order every run
    print(f"{len(done)} graded, {len(todo)} to grade. The brief asks for at least 20.")
    print("correct   = right against the reference (or a proper refusal for an unanswerable question)")
    print("supported = every claim is in the retrieved text (starred passages are the cited ones)\n")

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
        with evaluate.HUMAN.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([row["id"], correct, supported, notes])
        print("  saved.\n")

    print(f"\n{len(graded_ids())} answers graded in eval/human_labels.csv. "
          "Run `uv run python main.py evaluate` to compare with the judge.")


if __name__ == "__main__":
    main()
