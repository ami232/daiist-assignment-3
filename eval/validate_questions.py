"""
Check each reference answer in eval/questions.csv against the label text it cites.

    uv run python eval/validate_questions.py

For every answerable question, an LLM (no outside knowledge allowed) reads the
cited section(s) - the whole top-level section, e.g. all of 2.x for "2.2" - and
says whether the reference answer is supported, which parts are not, and
whether a different section fits better. Unanswerable questions are checked by
searching every indexed section for their key terms (shown for you to judge).

Writes eval/question_validation.md and caches verdicts in
eval/.question_validation_cache.json (rerun only checks changed rows).
This is an automated aid: read the flagged rows yourself before changing them.
"""

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import index  # noqa: E402
from check_questions import load_sections, matching_sections  # noqa: E402

QUESTIONS = ROOT / "eval" / "questions.csv"
OUT = ROOT / "eval" / "question_validation.md"
CACHE = ROOT / "eval" / ".question_validation_cache.json"
MODEL = "gemini-3.5-flash"

PROMPT = """You check a test question for a medication-label question-answering system.
Use ONLY the label text below. Do not use outside medical knowledge.

Question: {question}
Reference answer (what a correct answer must say): {reference}
Cited location(s): {locations}

Label text:
{text}

Return JSON with:
- "supported": "yes" if every claim in the reference answer is stated in the label text,
  "partial" if some claims are not, "no" if the main claim is not.
- "unsupported_parts": list of claims in the reference answer NOT found in the label text (empty if none).
- "section_answers_question": true if the cited text answers the question as asked.
- "better_location": a section number from the text that fits better, or "" if the cited one is right.
- "note": one short sentence for the question author.
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "supported": {"type": "string", "enum": ["yes", "partial", "no"]},
        "unsupported_parts": {"type": "array", "items": {"type": "string"}},
        "section_answers_question": {"type": "boolean"},
        "better_location": {"type": "string"},
        "note": {"type": "string"},
    },
    "required": ["supported", "unsupported_parts", "section_answers_question", "better_location", "note"],
}


def section_text(sections: dict, source: str, location: str) -> str:
    top = location.split(".")[0]
    numbers = matching_sections(sections[source], top) or matching_sections(sections[source], location)
    return "\n\n".join(f"[{source} {n}]\n{sections[source][n]}" for n in numbers)


def check(row: dict, sections: dict, cache: dict) -> dict:
    from google.genai import types

    pairs = list(zip(row["expected_source"].split(";"), row["expected_location"].split(";")))
    pairs = [(s.strip().lower(), loc.strip()) for s, loc in pairs]
    text = "\n\n".join(section_text(sections, s, loc) for s, loc in pairs if s in sections)
    prompt = PROMPT.format(question=row["question"], reference=row["reference_answer"],
                           locations="; ".join(f"{s} {loc}" for s, loc in pairs), text=text)
    key = hashlib.sha1(f"{MODEL}\n{prompt}".encode()).hexdigest()
    if key not in cache:
        response = index.genai_client().models.generate_content(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json",
                                               response_schema=SCHEMA, temperature=0))
        cache[key] = json.loads(response.text)
        CACHE.write_text(json.dumps(cache, indent=1))
    return cache[key]


def main() -> None:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["question"].strip()]
    sections = load_sections()
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    kinds = [r["kind"].strip().lower() for r in rows]
    lines = ["# Test-question validation", "",
             f"Automated check of `eval/questions.csv` against the label text ({MODEL}, label text only). "
             "Read every flagged row yourself; the model can be wrong.", "",
             f"- Total: {len(rows)} ({', '.join(f'{kinds.count(k)} {k}' for k in ('single', 'multi', 'unanswerable'))})"]
    table = ["", "| id | kind | cited | supported | answers question | better location | unsupported parts / note |",
             "|---|---|---|---|---|---|---|"]
    flagged = verified = 0
    for r in rows:
        kind = r["kind"].strip().lower()
        if kind == "unanswerable":
            table.append(f"| {r['id']} | unanswerable | - | check by hand | - | - | see search below |")
            continue
        try:
            v = check(r, sections, cache)
        except Exception as error:  # noqa: BLE001 - record and continue
            table.append(f"| {r['id']} | {kind} | {r['expected_source']} {r['expected_location']} | ERROR | | | {error} |")
            continue
        ok = v["supported"] == "yes" and v["section_answers_question"] and not v["better_location"]
        verified += ok
        flagged += not ok
        detail = "; ".join(v["unsupported_parts"]) or v["note"]
        mark = "" if ok else " ⚠️"
        table.append(f"| {r['id']}{mark} | {kind} | {r['expected_source']} {r['expected_location']} | {v['supported']} | "
                     f"{'yes' if v['section_answers_question'] else 'no'} | {v['better_location'] or '-'} | "
                     f"{detail.replace('|', '/')} |")
        print(f"{r['id']}: {v['supported']}{mark}", flush=True)
    lines += [f"- Reference answer fully supported by the cited section: {verified}",
              f"- Flagged for your review (⚠️): {flagged}"]
    OUT.write_text("\n".join(lines + table) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "eval"))
    main()
