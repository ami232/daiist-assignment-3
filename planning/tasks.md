# Implementation Plan — "Asistente Autónomo"

> Owners:
> - **You**: decisions and content the brief reserves for you. Also tested in the comprehension check.
> - **Claude**: code and plumbing.
> - **Together**: Claude prepares options and numbers, you decide.
>
> Order matters: **the test set is written before any retrieval tuning** (Phase 2 before Phase 3).

## Scope boundaries

- **Must have:**
  - the 4-law corpus;
  - 2+ retrieval designs;
  - the `search` and `add_document` tools;
  - the subagent and the harness, with approval + call limit + 1 guardrail;
  - the full evaluation;
  - REPORT.md;
  - `check.py` green on Windows and Actions.
- **Nice to have:**
  - hybrid BM25 design;
  - Cohen's κ;
  - charts of hit@k;
  - `add_document` accepting BOE HTML/PDF as well as XML.
- **Out of scope:**
  - company law (SL);
  - IVA/IRPF computation;
  - regional (autonómico) rules;
  - a UI;
  - multi-user deployment.

---

- [ ] **0. Setup and unknowns**
  - [x] 0.1 **You**: create `.env` with your Gemini key; `uv run python api_key.py` passes. _REQ-13_
  - [x] 0.2 Session 10's `07-own-harness/` was fetched from [ami232/daiist-agents](https://github.com/ami232/daiist-agents) into `planning/reference/`. _REQ-10, REQ-11_
  - [x] 0.3 **Claude**: the key reaches `gemini-embedding-2`, `gemini-3.5-flash-lite` (agent) and `gemini-3.5-flash` (judge). Embeddings: task as a text prefix, `output_dimensionality=768` works and comes back normalised, one vector per `Content`. _Design: open questions 2–3_
  - [x] 0.4 **Together**: find the authoritative BOE source for the held-out document H1. Found Orden PJC/297/2026 (BOE-A-2026-7296), arts. 18–19, verified against the BOE text. _REQ-11.6_
  - [x] 0.5 **Claude**: `uv add "langchain[mcp]>=1.4.7"` (for `MCPAdapter`, as in the course harness); `rank-bm25` only if design C is chosen. `pyproject.toml` and `uv.lock` are updated, not committed yet. _REQ-13_

- [ ] **1. Ingestion without embeddings (no quota spent)**
  - [x] 1.1 **Claude**: `SOURCES` registry + BOE fetcher with caching in `corpus/`. _REQ-2.1–2.4_
  - [x] 1.2 **Claude**: extractor (last version only, notes stripped, repeal stubs dropped, hierarchy path, `@titulo` locations, tables as rows). _REQ-3_
  - [x] 1.3 **Claude**: chunker with `fixed` and `article` strategies and the full metadata set; deterministic IDs. _REQ-4.1–4.2_
  - [x] 1.4 **Claude**: `index/outline.csv` (source, location, path, words, held_out, URL), 180 rows. Word counts printed: 61,016 indexed. _REQ-2.2, REQ-7.2_
  - [x] 1.4b **Claude**: `tests/test_ingest.py`, 16 passing (`uv run pytest`).
  - [ ] 1.5 **You**: pick one extraction problem from REQ-3.4 for the report and explain it in your own words. _REQ-3.4_
  - _Depends on: 0.1_

- [ ] **2. Use case and test set (yours, before tuning)**
  - [x] 2.1 **You**: write the Use case section (in REPORT.md; the explicit in-scope/out-of-scope list is still optional). Cover who asks, what they do with the answer, and the cost of a wrong answer vs a refusal. Fix the in-scope and out-of-scope list. _REQ-1_
  - [x] 2.2 **You**: write `eval/questions.csv` (31 questions: 16 single, 7 multi, 8 unanswerable incl. q31 for the COT2026 demo; reference answers by the student): ≥30 questions in Spanish, ≥5 `multi`, ≥5 `unanswerable` close to the topic. Include one unanswerable question that the held-out document will answer. _REQ-7_
  - [x] 2.3 **Claude**: `tests/test_questions.py` (passing). Format check only: columns, kinds, and that every `expected_source`/`expected_location` exists in `outline.csv`. No content edits. _REQ-7.2_
  - [x] 2.4 **You**: `AGENTS.md`: you chose 7 rules, the refusal phrase and the `[FUENTE, Ubicación]` citation format; Claude drafted the wording. Translated into English on 2026-11-25 (with AGENTS.md, the subagent, tool descriptions and harness messages); the format is now written `[SOURCE, Location]`, the agent is told to answer in Spanish, and the two fixed phrases stay in Spanish. The evaluation ran with the Spanish version; a 5-question smoke test with the English one gave the same outcomes. **Review the reasons before Phase 5.** _REQ-10.6_
  - _Depends on: 1.4_

- [ ] **3. Embeddings and retrieval comparison**
  - [x] 3.1 **Claude**: `embed_and_store` with batching, persist-per-batch, 429 stop/resume; query-embedding cache; `rag.retrieve` (dense, hybrid BM25 + RRF, source filter). Tested offline with a fake embedder (`tests/test_rag.py`); not yet run against Gemini. _REQ-5, REQ-6_
  - [x] 3.2 **Together**: chunk parameters chosen 2026-11-20: keep B `article` ≤400 words and A `fixed` 200/40. `main.py index` embedded both designs on 2026-11-20 (261 + 382 chunks; per-minute 429s waited out). _REQ-4.3, REQ-5_
  - [x] 3.3 **Claude**: retrieval part of `evaluate.py`: Hit@1/3/5, recall@5 and words-in-prompt per design → `eval/retrieval.csv` + `eval/retrieval_summary.csv`. Designs: A_fixed, B_article, C_article_hybrid. _REQ-6.1–6.2_
  - [ ] 3.4 **You**: shipped design chosen 2026-11-20: **B_article, k=5** (hit@5 1.00 like A, multi recall@5 0.88 vs 0.67; hybrid C worse on every metric). **Still yours:** write the justification in REPORT.md. _REQ-6.4_
  - [x] 3.5 **Claude**: confirm `index/` is under 90 MB and commit it (12.6 MB, commit 89ec7de). _REQ-5.6_
  - _Depends on: Phase 2 (test set frozen)_

- [ ] **4. MCP server and subagent**
  - [x] 4.1 **Claude**: `server.py` `search` (shipped design, formatted citations, BOE notice), with real docstrings. Starts over MCP in ~2.5 s. _REQ-8.1, 8.4, 8.6_
  - [x] 4.2 **You**: already-indexed policy decided 2026-11-20: version-aware (same date → no-op; newer → replace; older → nothing). **Claude**: `add_document` via `index.index_file`, with path validation and error strings. _REQ-8.2–8.5_
  - [ ] 4.3 **Claude**: check the tools from Claude Code (`/mcp`) and confirm `check.py` step 3 passes. `check.py` passes all 4 steps (2026-11-20); `/mcp` check still to do. _REQ-8_
  - [x] 4.4 **Together**: write the description and instructions for `.claude/agents/corpus-researcher.md`. Claude drafted them on 2026-11-23 (Spanish; AGENTS.md rules restated inside, ≤4 searches, hand-back ready to relay). Smoke test the same day on a tarifa plana question: only `search` used, every sentence cited [LETA, Artículo 38 ter], date given, no calculation, BOE notice. Wording reviewed and approved by you on 2026-11-23. You ran it from Claude Code the same day (late *alta* question); the transcript, the 3 searches and the citation check are in REPORT.md › Tools and subagent. _REQ-9_
  - _Depends on: 3.4_

- [ ] **5. Harness (`agent.py`)**
  - [x] 5.1 **Claude**: adapt the session 10 harness: `create_agent` with the Gemini chat model, MCP tools from `server.py`, `AGENTS.md` as system prompt; `answer()` returns the trace, tokens and seconds; CLI output. Model name still to confirm (0.3). _REQ-10.1, 10.5_
  - [x] 5.2 **Claude**: human approval middleware for `add_document`, auto-denied when there is no TTY. _REQ-10.2_
  - [x] 5.3 **Claude**: tool-call limit (≤4 searches, ≤8 model calls). _REQ-10.3_
  - [ ] 5.4 **You**: guardrail chosen 2026-11-20: citation validator (repair once, then refuse). **Claude**: implemented (`agent.validate_citations`, tested with a scripted model). It never fired in the 31-question evaluation. Captured on 2026-11-23 with 7 probe questions → `eval/guardrail_cases.md`: it fired twice, both repaired. (1) User asked for apartado-level citations, the model cited `[LETA, Artículo 38 ter, apartado 3]`, the validator flagged it, and the model searched again and rewrote with `[LETA, Artículo 38 ter]`. (2) A greeting: the model answered without citations, and the validator turned it into the refusal phrase (false positive, worth a line in the failure analysis). **You**: pick the case for REPORT.md › Harness and guardrails. _REQ-10.4_
  - [x] 5.5 **Claude**: `check.py` passes fully on Windows (2026-11-20). _REQ-13_
  - _Depends on: Phase 4_

- [ ] **6. End-to-end evaluation**
  - [x] 6.1 **Claude**: resumable run of `answer()` on all questions → `eval/answers.jsonl` (tokens, seconds), plus `eval/answers.md` for hand grading. 31/31 answered on 2026-11-20. _REQ-11.1_
  - [x] 6.2 **Claude**: code checks (refusal phrase, citation validity, expected source cited, BOE notice) → `eval/checks.csv`. _REQ-11.2_
  - [x] 6.3 **You**: rubric written (`eval/judge_rubric.md`). **Claude**: judge implemented (gemini-3.5-flash, structured output, resumable) → `eval/judge.csv`. 31/31 judged on 2026-11-23, but `evaluate.evidence()` was deduplicating on label + first 80 chars (the shared hierarchy path), so the judge saw only one part of split articles in 16 answers. Fixed (full-text key, new test); those 16 verdicts dropped (old file kept outside the repo) and re-judged: 8 done on 2026-11-23, the last 8 (q16, q19, q21, q22, q23, q25, q28, q31) on 2026-11-25: **31/31 judged**. The judge now stops at once on a daily-quota 429 instead of retrying (`max_retries=2`). _REQ-11.3_
  - [x] 6.4 **You**: grade at least 20 answers in `eval/human_labels.csv` **before opening `judge.csv`**. 31/31 graded before the judge ran. _REQ-11.4_
  - [x] 6.5 **Claude**: agreement (% and κ) and summary counts; `eval/summary.json`. Final on 2026-11-25: correct 29/31 (21 answerable + 7 correct refusals + q31; wrong refusal q25: RGAT art. 29 was retrieved; q31 has no refusal phrase, code checks flag it `answered_unanswerable` but both you and the judge marked it correct), supported 31/31. Agreement with you: correct 0.968 (κ 0.78, disagree q15), supported 0.935 (κ 0.0 because the judge marked all 31 supported; disagree q11, q15). _REQ-11.4–11.5_
  - [x] 6.6 **Together**: add-document demo. Done 2026-11-23 with `demo_add_document.py` (one agent session, you approved in the terminal) → `eval/add_document_demo.{json,md}`. Before: LGSS art. 308 rule + refusal for the bracket. Add: COT2026 added, 8 chunks. After: Tramo 1 of the reduced table, ≤670 €, bases 653,59–718,94 [COT2026, Artículo 18] (figures checked against the chunk). Issues for the report: the add confirmation was turned into the refusal phrase by the citation validator (same false positive as the greeting). Fixed on 2026-11-23 at your request: in a turn that ran add_document (approved or denied), an answer without citations is accepted; any citation it makes is still checked (`agent.citation_problems`, new test; no evaluation answer called add_document, so `eval/` is unaffected; first run kept as `eval/add_document_demo_v1.{json,md}`). Demo re-run the same day with the fix (`eval/add_document_demo.{json,md}`): step 2 now confirms the addition, guardrail not fired. Index restored again afterwards (261/382, no COT2026). Points from v2 for the failure analysis: step 1 explains why it cannot answer but does not use the fixed refusal phrase (rule 3); step 3 lists Tramo 2 as well although 600 € falls in Tramo 1, and has one uncited sentence on the annual regularisation. Second issue: the "after" answer treats 600 € invoiced as net yield and picks the user's bracket (rule 5). Index restored afterwards (your decision, 2026-11-23) to commit 5a3c6b1: 261 article / 382 fixed chunks, no COT2026, so evaluation stays on the 4-law corpus and q31 stays unanswerable. Original plan: Ask the chosen unanswerable question, add H1/H2 via `add_document` with approval, ask again, and save both answers. Restore or keep the index depending on the duplicate policy. _REQ-11.6_
  - _Depends on: Phase 5_

- [ ] **7. Failure analysis and decision (yours)**
  - [x] 7.1 **Claude**: export the failed questions with retrieved chunks, answer, checks and verdicts into a review table. Done 2026-11-25: stage 4 of `evaluate.py` (`write_failure_review`, new test) → `eval/failures.csv` (empty `cause`/`fix` columns for 7.2) and `eval/failures.md` (reasons, expected vs retrieved by the agent, searches, answer, both grades with notes, fragments). 7 questions: q07 and q25 (graded 0 by you and the judge), q11 and q15 (only you), q31 (no refusal phrase), q01 and q04 (multi citing 50 % / 75 % of what was expected).
  - [ ] 7.2 **You**: classified on 2026-11-25 (`cause` and `why` in `eval/failures.csv`, kept on re-runs; counts in `eval/failures.md`): retrieval miss 2 (q04, q07), wrong answer from the right passage 1 (q15), unsupported claim 1 (q11), wrong refusal 1 (q25), bad test question 1 (q31), not a failure 1 (q01). **Still yours:** what to fix first. Original task: classify each failure (retrieval miss / wrong answer from the right passage / unsupported claim / wrong refusal / bad test question), count by cause, and say what to fix first. _REQ-12.1–12.2_
  - [ ] 7.3 **You**: the ship decision: whether users may rely on it, for what, and with which safeguard, using the cost per question in tokens and seconds. _REQ-12.3_

- [ ] **8. Report and submission**
  - [ ] 8.1 **Together**: REPORT.md. Claude fills in the factual tables (corpus, counts, hit rates, costs); you write the analysis, decisions and AI-use disclosure. Factual parts filled in on 2026-11-25 (Corpus, Ingestion, Test set, Retrieval, Tools and subagent, Adding a document, Harness, Evaluation, Failures table, cost and latency). **Still yours** (marked `[TO WRITE]`): extraction problem (1.5), how the questions were written, design justification (3.4), guardrail case (5.4), what to fix first (7.2), decision (7.3), AI use, and name / student ID / group.
  - [ ] 8.2 **Claude**: final `uv run python check.py --evaluate` locally. **You**: run **Verify Assignment 3** on your fork's Actions with the secret set. _REQ-13_
  - [ ] 8.3 **You**: push to the fork, open the PR to `ami232/daiist-assignment-3`, submit the link on Blackboard, upload the zip.

## Requirement → task trace

| REQ | Tasks |
|---|---|
| 1 | 2.1 |
| 2 | 1.1, 1.4 |
| 3 | 1.2, 1.5 |
| 4 | 1.3, 3.2 |
| 5 | 3.1, 3.2, 3.5 |
| 6 | 3.1, 3.3, 3.4 |
| 7 | 2.2, 2.3 |
| 8 | 4.1–4.3 |
| 9 | 4.4 |
| 10 | 2.4, 5.1–5.5 |
| 11 | 6.1–6.6 |
| 12 | 7.1–7.3 |
| 13 | 0.1, 0.5, 5.5, 8.2 |

## Critical path

0.1 → 1.x → **2.2 (your test set)** → 3.2 (embed, quota day 1–2) → 3.4 → 4.x → 5.x → 6.1 → 6.4 → 7 → 8. The two risks are your test-set authoring time and the embedding quota, which can push the timeline by a day.
