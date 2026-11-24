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

## PostgreSQL project files

The final set in `questions.csv` has 30 entries. The [report](../REPORT.md#ai-use) records how the questions and grading materials were prepared. The earlier question drafts in `suggested_questions.csv` use the same numeric suffixes as the final set (for example, s03 corresponds to q03). After the index command, corpus/reading contains readable copies grouped by the same IDs. For multi-passage items, separate the source IDs and locations with semicolons in matching order, repeating the source ID if both sections belong to one document.

For a starting point, compare s03 (parallel dump format), s21 (combining and verifying an incremental backup), and s26 (a company's measured restore time). They illustrate a direct lookup, a two-passage decision and an installation-specific question.

For this run, [human_labels.csv](human_labels.csv) contains the 20 final score pairs and reasons Javier approved from the [grading worksheet scores](accepted_review.csv). Codex drafted these grades after the automated verdicts were available. Running `uv run python main.py evaluate` with the same inputs compares these labels with the saved verdicts and writes the result to the `human_agreement` field in [summary.json](summary.json). The [report](../REPORT.md#agreement-on-the-20-graded-answers) explains how to interpret that figure.

### Graded sample

These 20 IDs were sampled by question type using a fixed seed, without using the agent answers or judge verdicts.

- Single — q02, q03, q04, q07, q08, q09, q11, q12, q13, q14, q15, q16
- Multi — q01, q20, q22, q24
- Unanswerable — q25, q28, q29, q30
