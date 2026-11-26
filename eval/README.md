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

## Implemented workflow

1. Read the corpus and write your own questions and reference answers in
   `questions.csv` before tuning retrieval. Do not copy AI-written questions into
   the student-authored test set. Use `operations`, `fema`, and `uk-strategy` as
   source IDs. Locations are the original `PDF page N` or hierarchical
   `section: ...` markers in the cleaned corpus. For multi-passage questions,
   put two source IDs and two locations in matching order separated by `;`.
   Repeat a source ID when two pages come from the same document. Choose
   distinct pages/sections for the two passages.
2. Run `uv run python main.py index` after reviewing corpus/design settings and
   adding your Gemini key to ignored `.env`. The index saves each new vector
   immediately; a failed run resumes from the cache. Query embeddings are cached
   separately. Changing only k reuses the corpus vectors.
3. Run `uv run python evaluate.py --stage retrieval`. It compares both designs
   at k=1,3,5. A single question hits if its source and page/section are found.
   A multi question hits only if **all** its labelled page/section pairs are
   retrieved. Unanswerable questions have no gold evidence and are excluded from
   hit-rate denominators. Location-level matching is not semantic entailment.
4. Review the results and choose `selected_design` yourself. The initial
   `small` setting is provisional, not a measured winner. Record your reason in
   REPORT.md, then run `uv run python evaluate.py --stage answers`.
5. Open the generated `eval/runs/<run-id>/human_review.html`. It shows actual
   answers, references and retrieved evidence, without judge verdicts. Grade 20+
   answers yourself in `human_labels.csv`; explain every zero. Write the run ID
   into `human_labels_run.txt` to bind those grades to these exact answers.
6. Run `uv run python main.py evaluate`. It resumes saved answers and only then
   runs the LLM judge and reports agreement. Original blind labels are snapshotted
   before judging. Do not replace them after seeing judge grades; record any
   later reconsideration separately.
7. Select one of your unanswerable questions and a new public, licensed document
   that answers it. Register the document under `additional_documents` and run
   `uv run python demo_add_document.py qNN corpus/your-document.md`. The demo
   prompts for approval before calling the add tool in an isolated index copy,
   saves genuine before/after outputs, and preserves the baseline test corpus.

All run outputs carry a fingerprint of questions, prompts, settings, code and
chunk membership. Old answers are not silently reused after these change.
Human labels and report interpretation must remain your own work. Provisional
failure labels are automated diagnoses to inspect, not final human analysis.

No Gemini answers, judge results, human labels or subagent transcripts have been
fabricated. Offline tests use synthetic fixtures in temporary directories only.
