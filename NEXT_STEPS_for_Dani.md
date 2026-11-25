# Assignment 3: what you run (in order)

Copy the files from the zip over your clone of `daniteixidor/daiist-assignment-3` (the zip has no `.git`, `.venv` or `.env`). Don't commit until step 7.

**1. Setup** (once)
```bash
uv sync
cp .env.example .env        # paste your Gemini key
uv run python api_key.py
```

**2. Build the index** (downloads the 3 documents into `corpus/`, about 600-700 embeddings)
```bash
uv run python main.py index
```
- Check the printout: total words must be ≥ 50,000. Note the number of chunks per design for the report.
- If it stops with "daily embedding quota reached", run it again after 09:00 Spain time. It resumes and never re-embeds.
- If a download is blocked, open the URL from the error in your browser, save the file to the path it gives, and rerun.

**3. Quick test**
```bash
uv run python main.py ask "Can an advertisement show gross performance only?"
uv run python check.py
```
If the chat model name fails (Google renames models often), set one listed in AI Studio, e.g. `export GEMINI_CHAT_MODEL=gemini-3.6-flash`, and the same for `GEMINI_JUDGE_MODEL`.

**4. Evaluate** (resumable; rerun if it stops on a daily limit)
```bash
uv run python main.py evaluate
```
This writes `eval/retrieval_results.csv`, `index/config.json` (chosen design), `eval/answers.jsonl`, `eval/to_grade.csv`, `eval/judge.jsonl`, `eval/results.csv`, `eval/failures.csv` and `eval/summary.md`.

**5. Your own grading** (must be you, and done BEFORE you open judge.jsonl or summary.md)
- Open `eval/to_grade.csv`. For 20+ rows, fill `eval/human_labels.csv`: `id,correct,supported,notes` (1/0, with a note for every 0).
- Then rerun only the report: `RAG_EVAL_STAGES=report uv run python main.py evaluate` (Windows PowerShell: `$env:RAG_EVAL_STAGES="report"; uv run python main.py evaluate`).
- Open `eval/failures.csv` and fill `manual_cause` where the automatic cause is wrong (e.g. `bad test question`). Rerun the report again.

**6. Demo and transcript**
- `uv run python demo_add_document.py`, and type `y` when it asks for approval. This writes `eval/add_document_demo.md`.
- Open the repo folder in Claude Code (`claude`), run `/mcp` (the corpus server should be connected), and ask: *"Use the corpus-researcher subagent: what must an adviser disclose when using a paid testimonial?"* Copy the transcript into REPORT.md.

**7. Fill REPORT.md**: search for `[[FILL` and replace each one using `eval/summary.md`, `index/documents.json`, `eval/guardrail_log.jsonl` and the demo file. Fill your student ID and group. Then:
```bash
uv run python check.py --evaluate
git add -A && git commit -m "Assignment 3" && git push
```
Open the PR to ami232/daiist-assignment-3, submit the link on Blackboard and upload the zip.

## For the comprehension check: the 10 things to be able to explain
1. Why this use case: a wrong answer means a regulatory violation, "I don't know" means a call to compliance, so the system refuses rather than guesses.
2. Three custom parsers, and the editorial-notes problem (11k words of amendment history removed).
3. The two chunkings (fixed 200/40 vs. structure ≤220 words + heading), and what a "hit" means (same document + section).
4. Dense vs. BM25 vs. hybrid (reciprocal rank fusion: score = Σ 1/(60 + rank)), and why the choice is written to `index/config.json`.
5. `gemini-embedding-2` details: task as a text prefix, 768 dims, each text wrapped in its own `Content` (otherwise one merged vector), vectors saved per batch and keyed by hash, so only new chunks are embedded.
6. MCP: the server speaks over stdio, so nothing may print to stdout. Docstrings are the tool descriptions.
7. add_document: same pipeline. Same hash means nothing changes; same name with new content means the old version is replaced.
8. Harness: create_agent, MCP tools wrapped as LangChain tools, approval wrapper, call limits, citation guardrail (retry once, then refuse).
9. Evaluation: code checks vs. LLM judge (rubric: correct, supported), human agreement with Cohen's kappa, failure causes.
10. Decision: a first stop with sources, not the final word, with the CCO as the safeguard; cost in tokens and seconds per question.
