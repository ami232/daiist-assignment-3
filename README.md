# Gift-shop supply-chain assistant

Jimena Navarro Del Águila · DAIIST Assignment 3

A document-grounded assistant for an online gift-box shop facing supplier delays and Christmas demand. It searches public guidance, answers with citations and refuses requests for missing private or live information.

Start with **REPORT.md**. Source attribution is in **CORPUS_NOTICES.md**. **PROJECT_EXPLAINED.md** is the accompanying study reference.

## Run

Use Python 3.12 and uv. Run `uv sync`, then set `GEMINI_API_KEY` in an ignored `.env` file using `.env.example`, or in the environment.

```bash
uv run python main.py index
uv run python main.py ask "What trade-off should I consider before holding extra stock for Christmas?"
uv run python main.py evaluate
uv run python check.py --evaluate
uv run python -m unittest discover -q
```

The index and actual evaluation outputs are saved. Unchanged corpus text reuses vectors. Evaluation verifies content hashes before reusing answers and Claude verdicts. Cached evaluation needs no new provider calls; new Gemini requests need a valid key. New Claude judging requires an authenticated Claude Code CLI, as configured in `evaluation_config.json`.

## Results and evidence

- Three public sources: 57,121 cleaned words.
- Small chunks at k=5: Hit@5 23/25 versus 22/25 for large; about 22% less passage context.
- Current test set: 31 questions, including five multi-passage and six unanswerable.
- Real judge results: 29/31 correct and 30/31 supported.
- All 21 engineering tests and the instructor extended checker pass.
- Actual editor-subagent transcript and isolated before/after document addition are included.

The original 20 reported human ratings remain separate from the current AI evaluation. Original agreement was 85% for correctness, 90% for support and 80% for both. Those grades are not transferred to revised answers. See the report for the method and limitations.

The main data are in `eval/latest_run.json`, `eval/gift_shop_summary.json` and the referenced run directory. Earlier runs are retained as evidence and are not presented as current results. AI assistance and the supplementary q36 case are disclosed in the report.
