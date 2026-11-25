"""
Assignment 3: run the agent on every question in eval/questions.csv.
`uv run python answer_questions.py [--model gemini-3.5-flash]`

--model overrides agent.py's MODEL for the questions still to answer; every
saved answer records the model that produced it.

Saves each answer as soon as it is ready in eval/answers.jsonl (answer, tool
trace with the retrieved text, tokens, seconds), so a rate limit or crash
loses nothing: rerunning skips questions already answered. Also writes
eval/answers.md, a readable copy for grading by hand. add_document is always
denied here, so every answer comes from the starting index.
"""

import asyncio
import csv
import json
import re
import sys
from pathlib import Path

from agent import MODEL, open_tools, run_agent

ROOT = Path(__file__).resolve().parent
QUESTIONS = ROOT / "eval" / "questions.csv"
ANSWERS = ROOT / "eval" / "answers.jsonl"
READABLE = ROOT / "eval" / "answers.md"
CITATION = re.compile(r"^\[([^,\]]+), ([^\]]+)\]", re.M)
OVERLOAD_RETRIES = 3  # 503 "high demand" is temporary: wait and retry; a 429 (quota) still stops the run.
OVERLOAD_WAIT = 300   # Failed requests still count against the daily quota, so retry rarely.
ATTEMPT_TIMEOUT = 300  # under heavy load the client can hang on a request; treat that like a 503


def load_answers() -> dict:
    if not ANSWERS.is_file():
        return {}
    rows = [json.loads(line) for line in ANSWERS.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


def write_readable(questions: list[dict], answers: dict) -> None:
    models = sorted({a["model"] for a in answers.values()})
    lines = [f"# Agent answers ({', '.join(models)})", "",
             "Grade these before reading any judge verdicts. The retrieved passages under each answer are",
             "what the agent saw; use them to judge whether every claim is supported.", ""]
    for q in questions:
        a = answers.get(q["id"])
        lines += [f"## {q['id']} ({q['kind']})", "", f"**Question:** {q['question']}", "",
                  f"**Reference:** {q['reference_answer']}", ""]
        if a is None:
            lines += ["*Not answered yet.*", ""]
            continue
        lines += ["**Agent answer:**", "", a["answer"] or "*(empty)*", ""]
        searches = [t for t in a["trace"] if t["tool"] == "search"]
        lines.append(f"*{a['model']}, {len(searches)} search(es), {a['tokens']['total']} tokens, {a['seconds']} s*")
        lines.append("")
        for t in searches:
            cites = CITATION.findall(t["output"] or "")
            lines.append(f"- search `{t['args'].get('query', '')}` → " + ", ".join(f"[{s}, {l}]" for s, l in cites))
        lines += ["", "<details><summary>Retrieved passages</summary>", ""]
        for t in searches:
            lines += [f"**search:** `{t['args'].get('query', '')}`", "", "```text", (t["output"] or "").strip(), "```", ""]
        lines += ["</details>", ""]
    READABLE.write_text("\n".join(lines), encoding="utf-8")


async def main() -> int:
    model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else MODEL
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        questions = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    answers = load_answers()
    todo = [q for q in questions if q["id"] not in answers]
    print(f"{len(answers)} already answered, {len(todo)} to go with {model}.", file=sys.stderr)

    stopped = None
    async with open_tools(approve=lambda tool, args: False) as tools:
        for q in todo:
            result = None
            for attempt in range(OVERLOAD_RETRIES):
                try:
                    result = await asyncio.wait_for(run_agent(q["question"], tools, model), ATTEMPT_TIMEOUT)
                    break
                except Exception as error:  # noqa: BLE001 - quota or API errors: stop and keep what we have
                    overloaded = "503" in str(error) or isinstance(error, TimeoutError)
                    if overloaded and attempt < OVERLOAD_RETRIES - 1:
                        print(f"{q['id']}: model overloaded or hung; retrying in {OVERLOAD_WAIT} s "
                              f"({attempt + 1}/{OVERLOAD_RETRIES})", file=sys.stderr)
                        await asyncio.sleep(OVERLOAD_WAIT)
                        continue
                    stopped = f"{q['id']}: {type(error).__name__}: {str(error)[:300]}"
                    break
            if result is None:
                break
            answers[q["id"]] = {"id": q["id"], "model": model, **result}
            with ANSWERS.open("a", encoding="utf-8") as f:
                f.write(json.dumps(answers[q["id"]], ensure_ascii=False) + "\n")
            print(f"{q['id']} done ({len(result['trace'])} tool calls, {result['seconds']} s)", file=sys.stderr)

    write_readable(questions, answers)
    print(f"{len(answers)}/{len(questions)} answered. Readable copy: {READABLE.relative_to(ROOT)}", file=sys.stderr)
    if stopped:
        print(f"Stopped at {stopped}\nRerun to continue from there.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
