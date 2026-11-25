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

### Evidence locations in this implementation

Search results include the book section in `location` and a precise
`passage_location`, for example `12.1@0:400`. The numbers are half-open word
offsets within that section. Use the precise passage location in
`expected_location` to avoid counting an unrelated chunk from the same long
section as a hit. For two passages from one book, keep one `expected_source`
and separate the two locations with `;`. For several books, use matching
semicolon-separated source and location lists.

The retrieval evaluation records both any-evidence hits and complete-evidence
hits. A multi-passage question is fully covered only if every annotated passage
is found. It refuses to run until there are at least 30 student-written
questions, 5 multi and 5 unanswerable. Questions and human grades are supplied
by the student; pipeline tests use separate synthetic fixtures.

## human_labels.csv

Your own grades of 20+ agent answers, done before reading the judge's verdicts.

| Column | Content |
|---|---|
| `id` | Question id. |
| `correct` | `1`/`0`: right against the reference (or a proper refusal). |
| `supported` | `1`/`0`: every claim is in the retrieved text. |
| `notes` | Why, for every `0`. |

Commit what your evaluation stage writes here too (answers, verdicts, summary).

## Evaluation order

1. Finish at least 30 student-authored questions. The evaluation code checks the
   exact source/passage references before making model calls.
2. Run `python evaluate.py --retrieval-only` and choose `dense` or `hybrid` from
   the measured hit rates. Set `selected_retrieval_design` in project_config.json.
3. Run `python evaluate.py --answers-only`. It saves model answers and evidence
   in human_review.json without running the judge. Successful answers are saved
   individually so an interrupted run can resume.
4. Grade at least 20 answers in human_labels.csv before reading judge verdicts.
   Enter your own 0/1 scores and explain every zero. Blank grades do not count.
   For a local review form, run `python review.py` and open the printed address.
   It shows each answer, your reference and the retrieved passages. Both scores
   start blank; only your explicit choices are saved to human_labels.csv.
   The form requires notes for every zero, rejects stale evidence/grades and
   locks a review once its blind grades have been bound. It never calls an LLM.
5. Run `python evaluate.py --bind-human-labels`. This binds your grades to the
   actual displayed answers, retrieved evidence and rubric, preserving a blind
   copy. It does not invoke the judge.
6. Run `python main.py evaluate`. It computes the judge results, independent
   correctness/support agreement, code checks and an unfilled failure-review
   table for your analysis. On the submitted repository, the question set,
   chosen design, saved answers, human grades and binding are already present,
   so this command runs without interactive steps.

The rubric is in judge_rubric.json. Correctness and support are independent;
reliability requires both, valid citations and successful guardrail checks.
Model verdicts and development fixtures are never written into human_labels.csv.
Failure categories and the report's analysis remain the student's work.
