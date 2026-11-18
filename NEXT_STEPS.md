# What's built, and what is left for you

The code is written and was tested offline, with mock PDFs and fake embeddings, because Gemini and faa.gov
can't be reached from where it was built. The parts the brief says must be **yours** are left for you.
Delete this file before you submit.

## Files

| File | What it does |
|---|---|
| `config.py` | Everything you can change: corpus list, chunking designs, active design, models, citation and refusal format |
| `index.py` | Downloads PDFs, extracts and cleans them (page labels, hyphenation, ligatures), chunks them two ways (`fixed` 200-word windows; `section` heading-based), embeds and stores them in `index/chroma/`. Resumes after a crash or quota stop. `add_file()` is the add-document pipeline |
| `retrieval.py` | Vector search and hybrid (vector + BM25) search; query vectors cached in `index/query_cache.json` |
| `server.py` | MCP tools `search(query)` and `add_document(path)` |
| `agent.py` | LangChain harness: approval before add_document, step limit, and a citation-check guardrail |
| `evaluate.py` | Hit rate at 1/3/5 per design, agent runs, code checks, LLM judge, agreement with you, failures, cost |
| `.claude/agents/corpus-researcher.md` | Subagent that only uses search |

## Steps

**1. Set up.** Clone your fork, unzip this on top of it, then run:
```bash
uv sync
cp .env.example .env      # paste your Gemini key
uv run python api_key.py
```

**2. Check the corpus.** Run `uv run python index.py --show phak-ch15`. This downloads that chapter and
prints chunks without spending quota. Check that:
- the text is readable (two-column PDFs can come out scrambled), and
- `pages` shows the printed page numbers (15-3), not `pdf3`.

If a download fails, save the PDF by hand as `corpus/<doc_id>.pdf` (or `corpus/extra/` for ch14).

**3. Build the index.** Run `uv run python main.py index`. It prints the total word count, which must
be at least 50,000. If it's lower, add a chapter to `CORPUS` in `config.py`; the URL pattern is
`{FAA}/NN_phak_chMM.pdf` with NN = MM + 2. Both designs together use about 1.2 embeddings per
100 words, so about 650 for 55,000 words. If you hit the daily limit, run it again after 09:00
and it carries on.

**4. Write `eval/questions.csv` (yours).** `expected_source` is the doc_id (`phak-ch15`) and
`expected_location` is the printed page (`15-3`); for `multi`, use `;` between pairs in matching
order. Write the unanswerable questions close to the topic, and make **one** of them answerable by
Chapter 14 (Airport Operations) for step 8. Make the first answerable question a good one:
`check.py` uses it.

**5. Choose a design.** Write `AGENTS.md` (your rules; keep the two format lines) and
`eval/judge_rubric.md`, then run `uv run python main.py evaluate`. Compare designs in
`eval/retrieval_summary.csv` and set `ACTIVE_CHUNKING` / `ACTIVE_METHOD` in `config.py`. If you
change them, delete `eval/answers.jsonl` and `eval/judge.jsonl` and run evaluate again. The judge is
skipped until the rubric file no longer contains "TODO".

**6. Grade 20+ answers yourself.** Use `eval/to_grade.csv`, which has no judge verdicts, and fill in
`eval/human_labels.csv` *before* opening `results.csv` or `judge.jsonl`. Then run evaluate again
(it's cached and free) to get the agreement score in `eval/summary.md`.

**7. Classify failures (yours).** Fill in the `cause` column of `eval/failures.csv`. `auto_hint` is
only a first guess.

**8. Before and after adding a document.** Do this last, because it changes the index:
```bash
uv run python main.py ask "<your ch14 unanswerable question>"
uv run python main.py ask "Please add corpus/extra/phak-ch14.pdf to the index"   # type yes
uv run python main.py ask "<same question>"
```
The second run also gives you the approval step for the report.

**9. Subagent transcript.** In the repo, run `claude`, check `/mcp` shows `corpus`, then ask:
"Use the corpus-researcher subagent to answer: …". Paste the transcript into REPORT.md.

**10. Check and submit.**
```bash
uv run python check.py
git add -A && git commit -m "Assignment 3" && git push
```
Commit `index/` and `eval/`. Then open a PR to ami232/daiist-assignment-3, put the PR link on
Blackboard, and upload a zip.

## For REPORT.md's AI-use section

Claude wrote the code: config, index, retrieval, server, agent, evaluate and the subagent file.
It also added a Linux target to `pyproject.toml` so the lock covers GitHub Actions. List any
changes you make yourself.

## Choices already made in the code (you can change any of them)

- **Already-indexed documents.** If the file's contents are the same, nothing is embedded. If
  they differ, the new version replaces the old one.
- **Extra guardrail.** Every citation must match a passage retrieved in that run. The model gets
  one rewrite, and if that also fails the answer is withheld.
- **Restricted paths.** add_document only reads files inside the project folder.
- **Untested on real PDFs.** The heading detector for `section` chunking was only tested on mock
  PDFs, so check it in step 2.
