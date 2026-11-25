# Evaluation files

## questions.csv

30+ questions written by you from the documents, before tuning anything.

| Column | Content |
|---|---|
| `id` | `q01`, `q02`… |
| `question` | As a user would ask it. |
| `kind` | `single`, `multi` (two passages) or `unanswerable` (5+ of each of the last two). |
| `expected_source` | Document that answers it, as in your chunk metadata; `;` between several. Empty if unanswerable. |
| `expected_location` | Page, section or article, as in your metadata. Empty if unanswerable. |
| `reference_answer` | Short correct answer; for unanswerable, what the assistant should say. |

Make unanswerable questions close to the corpus's topic, not obviously off-topic.

## human_labels.csv

Your own grades of 20+ agent answers, done before reading the judge's verdicts.

| Column | Content |
|---|---|
| `id` | Question id. |
| `correct` | `1`/`0`: right against the reference (or a proper refusal). |
| `supported` | `1`/`0`: every claim is in the retrieved text. |
| `notes` | Why, for every `0`. |

Commit what your evaluation stage writes here too (answers, verdicts, summary).

## How this project fills them in

- `expected_source` uses the document ids in the chunk metadata: `GDPR`, `ePrivacy`, `SCC 2021/914`.
- `expected_location` uses the chunk locations: `Article 33`, `Recital 26`, `Annex, Clause 9`. A question counts as a retrieval hit at k when one of the top-k chunks covers that location (a recital group such as *Recitals 26-28* covers Recital 26; a fixed-size window covers every unit it overlaps).
- For `multi` questions, sources and locations are paired in order, separated by `;` (e.g. `GDPR;GDPR` and `Article 34;Article 33`). Hit rate counts one of the two; `multi_both@k` in `retrieval.csv` counts both.
- Unanswerable reference answers start with the exact refusal sentence the assistant must use: `The corpus does not cover this.`

## Files the evaluation stage writes

| File | Content |
|---|---|
| `retrieval.csv` | Hit rate at 1/3/5 for every design x search mode, and words added to the prompt. |
| `answers.jsonl` | The agent's answer, tool trace, retrieved citations, tokens and seconds for every question (saved as it goes; re-runs only ask missing ones). |
| `judge.jsonl` | The LLM judge's `correct`/`supported` verdict and reason for every answer. |
| `results.csv` | One row per question: outcome, code checks, judge verdict, failure cause, cost. |
| `failure_overrides.csv` | My own reclassification of failures where the automatic cause was wrong. |
| `add_document_demo.json` | The unanswerable question answered before and after adding a document. |
| `summary.json`, `summary.md` | All the numbers in REPORT.md. |

`human_labels.csv` is filled with `uv run python grade.py`, which shows each answer without the judge's verdict.
