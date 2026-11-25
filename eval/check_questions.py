"""Check eval/questions.csv against the built index (no embeddings, no API calls).

For every answerable question it checks that each expected source/location exists in
index/chunks_article.jsonl, that the numbers in the reference answer appear in that text,
and that a key phrase appears there. Run: uv run python eval/check_questions.py
"""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEY_PHRASES = {  # a phrase that must appear in the expected article(s)
    "q01": "same body", "q02": "deposits", "q03": "counterparty", "q04": "bonds",
    "q05": "index", "q06": "non-voting", "q07": "remedying", "q08": "85",
    "q09": "borrow", "q10": "repurchase", "q11": "uncovered", "q12": "125 000",
    "q13": "precious metals", "q14": "global exposure", "q15": "10 working days",
    "q16": "reliable", "q17": "397", "q18": "diversified", "q19": "5 years",
    "q20": "risk management function", "q21": "voting rights", "q22": "best possible result",
    "q23": "fee", "q24": "two", "q25": "bar chart", "q26": "synthetic indicator",
    "q27": "ongoing charges", "q28": "six different issues", "q29": "valu",
    "q30": "commitment approach", "q31": "essential characteristics", "q32": "20 %",
    "q33": "remedying", "q34": "debt securities",
}


def norm(text: str) -> str:
    text = re.sub(r"\s+", " ", text.replace("\xa0", " "))
    text = re.sub(r"(?<=\d) (?=\d{3}\b)", "", text)      # 125 000 -> 125000
    text = re.sub(r"(?<=\d),(?=\d)", ".", text)            # 0,02 -> 0.02
    return text.lower()


def numbers(answer: str) -> set[str]:
    answer = re.sub(r"(Art(icle)?\.?|Directive|Regulation) [\d/()a-z.]+", "", answer)
    return set(re.findall(r"\d+(?:\.\d+)?", norm(answer)))


text_of = defaultdict(str)
for line in (ROOT / "index" / "chunks_article.jsonl").open(encoding="utf-8"):
    c = json.loads(line)
    text_of[(c["doc_id"], c["location"])] += " " + c["text"]

rows = list(csv.DictReader((ROOT / "eval" / "questions.csv").open(encoding="utf-8")))
print("Rows:", len(rows), dict(Counter(r["kind"] for r in rows)))
problems = 0
for r in rows:
    if r["kind"] == "unanswerable":
        if r["expected_source"]:
            print(f"{r['id']}: unanswerable but has a source"); problems += 1
        continue
    pairs = list(zip(r["expected_source"].split(";"), r["expected_location"].split(";")))
    missing = [p for p in pairs if p not in text_of]
    if missing:
        print(f"{r['id']}: NOT IN INDEX {missing}"); problems += 1
        continue
    text = norm(" ".join(text_of[p] for p in pairs))
    lost = sorted(n for n in numbers(r["reference_answer"]) if n not in text)
    phrase = KEY_PHRASES.get(r["id"])
    if lost:
        print(f"{r['id']}: numbers not found in {pairs}: {lost}"); problems += 1
    if phrase and norm(phrase) not in text:
        print(f"{r['id']}: key phrase '{phrase}' not found in {pairs}"); problems += 1
print("All questions match the index." if not problems else f"{problems} problem(s) to fix.")