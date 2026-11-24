# v2 run

A second end-to-end run of all 32 questions, to test fixes for the failure modes of the v1 run. v1 (`eval/`) stays the primary run: my grades, the failure causes and the add-document demo refer to it.

**What changed from v1** (commit `99dfbf4`):
- `search` starts each passage with the citation to copy and the document's version: `Passage n (score s). Cite as: [source, location]. Version: …`;
- AGENTS.md rule 1: if the question asks two or more things, search again for any part the passages don't cover; rule 3: copy the text after "Cite as:", one citation per bracket, never a passage number;
- the citation check splits `[A, x; B, y]` and checks each citation.

**What did not change:**
- the test set and the model (`gemini-3.1-flash-lite`, temperature 0);
- AGENTS.md rule 6, the judge rubric and prompt, and the refusal check;
- the index: the run used the three corpus documents only, without the 58 U-space chunks added for the demo, so v1 and v2 searched the same text.

**Run:** `EVAL_DIR=eval/v2 uv run python evaluate.py` on 23 November 2026, with the agent, server and AGENTS.md at commit `c2d0ff7`. The judge's retry settings were changed during the run (commits `2edbfbc` and `32e447e`); that changes how long a failed call waits, not the verdicts. The Gemini API was overloaded (503 "high demand") for most of the run, so the seconds include retry waits and are not comparable with v1.

**Files:** `answers.jsonl` and `judge.jsonl` are the cached results. `summary.json`, `failures.csv` and `retrieval.csv` are rebuilt from them offline by the same command.
