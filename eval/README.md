# Evaluation files

## questions.csv

36 questions written from the documents, before tuning anything. Questions and answers are in Spanish, like the corpus.

| Kind | Count |
|---|---|
| `single` | 24 |
| `multi` | 6 |
| `unanswerable` | 6 |

| Column | Content |
|---|---|
| `id` | `q01` … `q36` |
| `question` | As a user would ask it. |
| `kind` | `single`, `multi` (two passages) or `unanswerable`. |
| `expected_source` | File name of the document that answers it, as in the chunk metadata; `;` between several. Empty if unanswerable. |
| `expected_location` | Article or provision (e.g. `art. 10.3`, `disposición transitoria segunda.2`); one per passage, `;` between several. Empty if unanswerable. |
| `reference_answer` | Short correct answer; for unanswerable, what the assistant should say. |

Unanswerable questions stay on the corpus's topic: the current IRAV value, the penalty for usurpación, cutting off utilities to occupants, Barcelona's licence decision for 2028, reference-index prices, and the tourist tax. The correct behaviour is to say the documents don't contain the answer, not to guess.

## human_labels.csv

Your own grades of 20+ agent answers, done before reading the judge's verdicts.

| Column | Content |
|---|---|
| `id` | Question id. |
| `correct` | `1`/`0`: right against the reference (or a proper refusal). |
| `supported` | `1`/`0`: every claim is in the retrieved text. |
| `notes` | Why, for every `0`. |

Commit what your evaluation stage writes here too (answers, verdicts, summary).