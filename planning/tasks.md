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
  - [ ] 0.1 **You**: create `.env` with your Gemini key; `uv run python api_key.py` passes. _REQ-13_
  - [x] 0.2 Session 10's `07-own-harness/` was fetched from [ami232/daiist-agents](https://github.com/ami232/daiist-agents) into `planning/reference/`. _REQ-10, REQ-11_
  - [ ] 0.3 **Claude**: list the models the key can access; confirm the `gemini-embedding-2` task type and dimension options; pick the chat model with you. _Design: open questions 2–3_
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
  - [ ] 2.1 **You**: write the Use case section. Cover who asks, what they do with the answer, and the cost of a wrong answer vs a refusal. Fix the in-scope and out-of-scope list. _REQ-1_
  - [ ] 2.2 **You**: write `eval/questions.csv`: ≥30 questions in Spanish, ≥5 `multi`, ≥5 `unanswerable` close to the topic. Include one unanswerable question that the held-out document will answer. _REQ-7_
  - [ ] 2.3 **Claude**: format check only: columns, kinds, and that every `expected_source`/`expected_location` exists in `outline.csv`. No content edits. _REQ-7.2_
  - [ ] 2.4 **You**: write `AGENTS.md` rules, each with its reason, and the exact refusal phrase. _REQ-10.6_
  - _Depends on: 1.4_

- [ ] **3. Embeddings and retrieval comparison**
  - [ ] 3.1 **Claude**: `embed_and_store` with batching, persist-per-batch, 429 stop/resume; query-embedding cache; `rag.retrieve` (dense, hybrid, filter). _REQ-5, REQ-6_
  - [ ] 3.2 **Together**: choose the chunk parameters for designs A and B 🟨; Claude runs `main.py index` for B (day 1) and A (day 1 or 2, depending on quota). _REQ-4.3, REQ-5_
  - [ ] 3.3 **Claude**: retrieval part of `evaluate.py`: Hit@1/3/5 and words-in-prompt per design → `eval/retrieval.csv`. _REQ-6.1–6.2_
  - [ ] 3.4 **You**: pick the shipped design and k from the table, and write the justification. _REQ-6.4_
  - [ ] 3.5 **Claude**: confirm `index/` is under 90 MB and commit it. _REQ-5.6_
  - _Depends on: Phase 2 (test set frozen)_

- [ ] **4. MCP server and subagent**
  - [ ] 4.1 **Claude**: `server.py` `search` (shipped design, formatted citations, BOE notice), with real docstrings. _REQ-8.1, 8.4, 8.6_
  - [ ] 4.2 **You**: decide the already-indexed policy 🟨. **Claude**: implement `add_document` by importing `index.py`, with path validation and error strings. _REQ-8.2–8.5_
  - [ ] 4.3 **Claude**: check the tools from Claude Code (`/mcp`) and confirm `check.py` step 3 passes. _REQ-8_
  - [ ] 4.4 **Together**: write the description and instructions for `.claude/agents/corpus-researcher.md`. **You**: run it from Claude Code on a real question and paste the transcript into REPORT.md. _REQ-9_
  - _Depends on: 3.4_

- [ ] **5. Harness (`agent.py`)**
  - [ ] 5.1 **Claude**: adapt the session 10 harness: `create_agent` with the Gemini chat model, MCP tools from `server.py`, `AGENTS.md` as system prompt; `answer()` returns the trace, tokens and seconds; CLI output. _REQ-10.1, 10.5_
  - [ ] 5.2 **Claude**: human approval middleware for `add_document`, auto-denied when there is no TTY. _REQ-10.2_
  - [ ] 5.3 **Claude**: tool-call limit. _REQ-10.3_
  - [ ] 5.4 **You**: choose the extra guardrail 🟨. **Claude**: implement it. **You**: capture one case where it fired. _REQ-10.4_
  - [ ] 5.5 **Claude**: `check.py` passes fully on Windows. _REQ-13_
  - _Depends on: Phase 4_

- [ ] **6. End-to-end evaluation**
  - [ ] 6.1 **Claude**: resumable run of `answer()` on all questions → `eval/answers.jsonl` (tokens, seconds). _REQ-11.1_
  - [ ] 6.2 **Claude**: code checks (refusal phrase, citation validity, expected source cited) → `eval/checks.csv`. _REQ-11.2_
  - [ ] 6.3 **You**: write the judge rubric 🟨. **Claude**: implement the judge with structured output → `eval/judge.csv`. _REQ-11.3_
  - [ ] 6.4 **You**: grade at least 20 answers in `eval/human_labels.csv` **before opening `judge.csv`**. _REQ-11.4_
  - [ ] 6.5 **Claude**: agreement (% and κ) and summary counts; `eval/summary.json`. _REQ-11.4–11.5_
  - [ ] 6.6 **Together**: add-document demo. Ask the chosen unanswerable question, add H1/H2 via `add_document` with approval, ask again, and save both answers. Restore or keep the index depending on the duplicate policy. _REQ-11.6_
  - _Depends on: Phase 5_

- [ ] **7. Failure analysis and decision (yours)**
  - [ ] 7.1 **Claude**: export the failed questions with retrieved chunks, answer, checks and verdicts into a review table.
  - [ ] 7.2 **You**: classify each failure (retrieval miss / wrong answer from the right passage / unsupported claim / wrong refusal / bad test question), count by cause, and say what to fix first. _REQ-12.1–12.2_
  - [ ] 7.3 **You**: the ship decision: whether users may rely on it, for what, and with which safeguard, using the cost per question in tokens and seconds. _REQ-12.3_

- [ ] **8. Report and submission**
  - [ ] 8.1 **Together**: REPORT.md. Claude fills in the factual tables (corpus, counts, hit rates, costs); you write the analysis, decisions and AI-use disclosure.
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
