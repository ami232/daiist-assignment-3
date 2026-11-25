# About eval/human_labels.csv

The grades in `human_labels.csv` are **AI-assisted independent annotations, pending human verification**. The file keeps the name `human_labels.csv` because `evaluate.py` and `check.py` expect it.

**How they were made.** An AI assistant (Claude) graded each of the 30 agent answers against the reference answer in `questions.csv`, the FDA label text, and the passages actually retrieved for that question (`retrieved_text` in `agent_answers.jsonl`). It did this **without looking at the LLM judge's verdicts** in `judge_verdicts.jsonl`.

**What this means for the agreement figures.** `agreement_*` and `kappa_*` in `evaluation_summary.json` compare two AI graders (Claude vs. the Gemini judge), not a human against the judge.
