"""
Helper for grading eval/human_labels.csv by hand: for 20 answers, put every claim of the answer next
to the closest sentence of the passages the agent retrieved in that run, with a word-overlap score.
It shows evidence only; the grades are the grader's. Writes eval/support_check.md.

    uv run python eval/support_check.py
"""

import csv
import json
import re
from pathlib import Path

EVAL = Path(__file__).resolve().parent
STOP = set("the a an of to in and or for on by with is are be that this it as at from which their its your our "
           "we you they not no can may must shall will under than such these those any all has have been was were "
           "if when where also only into per".split())


META = re.compile(r"not legally binding|answer was drafted|Check the cited sources|rests (solely|only|entirely)|Commission's (views|interpretation)|corpus does not|"
                  r"provided (documents|texts|passages)|consult|check with|contact (your|the)|competent authority for|"
                  r"you (may|should|could) (want to )?(check|ask|refer)", re.I)


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+(?:[.,/][0-9]+)*", text.lower()) if w not in STOP and len(w) > 1}


def claims(answer: str) -> list[str]:
    text = re.sub(r"\[[^\]]*\]|`|\*\*|\*", " ", answer)                       # citations and markdown
    parts = re.split(r"(?<=[.!?:])\s+|\n+\s*[-•*]?\s*", text)
    return [re.sub(r"\s+", " ", p).strip(" -•") for p in parts if len(words(p)) >= 3]


def passage_sentences(trace: list[dict]) -> list[tuple[str, str]]:
    sentences = []
    for step in trace:
        if step["type"] != "result":
            continue
        for block in step["text"].split("\n\n---\n\n"):
            cite = re.search(r"Cite as: \[([^\]]+)\]", block)
            body = block.split("\n", 3)[-1]
            for s in re.split(r"(?<=[.;:])\s+|\n", body):
                if len(words(s)) >= 3:
                    sentences.append((cite.group(1) if cite else "?", s.strip()))
    return sentences


def best_match(claim: str, sentences: list[tuple[str, str]]) -> tuple[float, str, str]:
    target = words(claim)
    best = (0.0, "", "")
    for cite, sentence in sentences:
        score = len(target & words(sentence)) / len(target)
        if score > best[0]:
            best = (score, cite, sentence)
    return best


def pick(rows: list[dict], n: int = 20) -> list[dict]:
    """Every refusal of an unanswerable question, then answered questions, shortest first."""
    unanswerable = [r for r in rows if r["kind"] == "unanswerable"]
    others = sorted((r for r in rows if r["kind"] != "unanswerable"), key=lambda r: len(r["answer"]))
    return sorted(unanswerable + others[: n - len(unanswerable)], key=lambda r: int(r["id"][1:]))


def main() -> None:
    questions = {q["id"]: q for q in csv.DictReader((EVAL / "questions.csv").open(encoding="utf-8"))}
    rows = [json.loads(line) for line in (EVAL / "answers.jsonl").read_text(encoding="utf-8").splitlines()]
    out = ["# Support check for grading", "",
           "For each answer: every claim, the closest sentence in the passages retrieved in that run, and the share "
           "of the claim's words found in it. ✅ ≥ 80 %, 🟡 50–80 % (read both), ❌ < 50 % (probably not in the passages). "
           "Word overlap misses paraphrases and can be fooled by a sentence using the same words for something else, "
           "so read the pair before deciding. `supported` = 1 only if every claim is backed. "
           "`correct` = compare the answer with the reference.", ""]
    for r in pick(rows):
        q = questions[r["id"]]
        out += [f"## {r['id']} ({q['kind']}): {q['question']}", "", f"**Reference:** {q['reference_answer']}", "",
                "**Answer:**", "", "> " + r["answer"].replace("\n", "\n> "), ""]
        if r["answer"].strip().startswith("The corpus does not cover"):
            out += ["*Refusal. Supported unless it states facts; check them below if any.*", ""]
        sentences = passage_sentences(r["trace"])
        out += ["| | claim | closest passage sentence | from |", "|---|---|---|---|"]
        for claim in claims(r["answer"]):
            if META.search(claim):  # the notes AGENTS.md asks for are not claims about the regulation
                out.append(f"| ℹ️ note | {claim[:300]} | (AGENTS.md note or advice, not a claim about the EUDR) | |")
                continue
            score, cite, sentence = best_match(claim, sentences)
            mark = "✅" if score >= 0.8 else "🟡" if score >= 0.5 else "❌"
            esc = lambda s: s.replace("|", "\\|")[:300]  # noqa: E731
            out.append(f"| {mark} {score:.0%} | {esc(claim)} | {esc(sentence)} | {cite} |")
        out += ["", f"`{r['id']},?,?,`", ""]
    (EVAL / "support_check.md").write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {EVAL / 'support_check.md'}")


if __name__ == "__main__":
    main()
