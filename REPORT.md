# Assignment 3 Report

- **Name**: Sophie Jasmine Leonaard
- **Student ID**: 31860
- **Group**: PPLEDBA 5A

## Use case
Workers in the United States often need quick answers about federal labor laws regarding leave and medical care for family members, compensation for overtime work, and payment of the wage. They consult the assistant to verify daily doubts concerning their eligibility for FMLA leave, the compensability of travel or rest period, or possibility of deduction from the wage, before making any decisions at work.

The possible consequences of acting upon an incorrect response will be quite dangerous for the employee and might include the absence of pay, violation of policy of the company, or loss of protection of labor laws. By contrast, the employee's cautious decision not to act ("I don't know, ask HR or the Wage and Hour Division") will cost some time only. This explains why the assistant is restricted exclusively to federal labor laws only (without the state law, company policy, and case law), and does not give a legally reliable answer. For example, the assistant must refuse questions that depend on missing statutes or local rules, such as "How many weeks of paid family leave does the law of the employee's state provide?" or "How many paid sick-leave days must every private employer provide each year under federal law?"


## Corpus
The corpus comes from the eCFR (Electronic Code of Federal Regulations), Title 29, using one fixed snapshot dated 1 November 2026 downloaded through the eCFR versioner API.

| Document | URL | Date | Licence | Words |
| --- | --- | --- | --- | --- |
| 29 CFR Part 825 (Family and Medical Leave Act) | https://www.ecfr.gov/api/versioner/v1/full/2026-11-01/title-29.xml?part=825 | 2026-11-01 | US federal government work, public domain (17 U.S.C. § 105) | 51,930 |
| 29 CFR Part 785 (Hours worked) | https://www.ecfr.gov/api/versioner/v1/full/2026-11-01/title-29.xml?part=785 | 2026-11-01 | same | 7,500 |
| 29 CFR Part 531 (Wage payments under the FLSA) | https://www.ecfr.gov/api/versioner/v1/full/2026-11-01/title-29.xml?part=531 | 2026-11-01 | same | 8,534 |
| **Total indexed** | | | | **67,964** |
| 29 CFR Part 778 (Overtime compensation), added later with `add_document` | https://www.ecfr.gov/api/versioner/v1/full/2026-11-01/title-29.xml?part=778 | 2026-11-01 | same | 39,376 |

Since the eCFR is not an official legal edition of the CFR, every answer is tied to this specific snapshot date, and using one date across all parts prevents conflicts between different regulatory versions. I picked these three parts because they cover the most common workplace issues workers deal with while keeping the indexed corpus manageable (67,964 words) for testing.


## Ingestion
The ingestion script downloads the XML of each part from the eCFR API using gzip compression (without gzip, the API returns an error). It then extracts the text of each section, skips source-citation notes (`CITA` elements), and cleans up whitespace. During extraction, I fixed a formatting issue where eCFR section IDs did not include the `"§"` symbol (e.g., `825.402`). `parse_part` now writes `§ 825.402`, matching how the CFR is normally cited and how locations are written in the test set.

Each chunk stores metadata (`source`, `location`, `sections`, `heading`, `design`, `snapshot`, and `words`) and is embedded using Gemini `gemini-embedding-2` into ChromaDB with cosine similarity. Each chunk ID is a hash of its content, so identical chunks are only embedded once (683 embeddings total across both designs). I compared two chunking designs:
- `fixed`: 200 words per chunk with 40 words of overlap, producing **426 chunks** (Part 825: 325, Part 785: 47, Part 531: 54). A side finding was that changing just one word near the start of a part shifts every window after it, so all 47 chunks of Part 785 had to be re-embedded.
- `section`: One chunk per section, splitting sections longer than 450 words with 90 words of overlap, producing **257 chunks** (Part 825: 170, Part 785: 51, Part 531: 36). With this design, chunks stay isolated and stable when edits happen elsewhere.


## Test set
The test set (`eval/questions.csv`) has 30 questions: 17 single (one passage), 7 multi (two passages), and 6 unanswerable, taken from Part 825 (10), Part 785 (10), and Part 531 (7). To build it, I read the regulation sections first, wrote each question the way a regular worker would ask it, and wrote the reference answer directly from the text. For the unanswerable questions, I wrote questions closely related to the topic (like state paid family leave, mandatory paid sick days, or Part 778 commission formulas) and used `Ctrl+F` to verify that the answers were not in any of the three documents.

- Example answerable (`q05`, single): "Can a meal break be unpaid if I still have to perform work duties while eating?" Expected: `§ 785.19(a)`. Reference: the employee must be completely relieved from duty for the purposes of eating regular meals.
- Example unanswerable (`q28`): "What exact regular-rate formula from 29 CFR Part 778 applies when calculating overtime for an employee paid commissions and bonuses?" Reference: not stated in the supplied documents; ask HR or the Wage and Hour Division (this becomes answerable only after Part 778 is added in the `add_document` demo).

The main limitations are that all 30 questions were written by one person, many answerable questions still use wording fairly close to the regulation text, and a few questions intentionally overlap on the same section.


## Retrieval
Retrieval was evaluated across the 24 answerable questions, where a hit means an expected section appears in the top-k chunks, and "all found" for `multi` questions means every expected section was retrieved:

| Design | Chunks | hit@1 | hit@3 | hit@5 | multi, all sections found @1 / @3 / @5 |
| --- | --- | --- | --- | --- | --- |
| `fixed` | 426 | 0.83 (20/24) | 0.96 | 1.00 | 1/7, 1/7, 3/7 |
| `section` | 257 | 0.96 (23/24) | 0.96 | 1.00 | 0/7, 2/7, 4/7 |

Each search returns 5 chunks, adding roughly 1,000 words to the prompt under `fixed` (5 × 200) and about 1,300 words on average under `section` (67,964 / 257 ≈ 264 words per chunk, up to 450 words). Across the full evaluation run, each question used an average of 4,772 tokens (including the question, search results, and answer).

I chose the section design because keeping each section whole prevents rules and exceptions from being cut off arbitrarily mid-sentence and aligns with how the regulations are structured. This is supported by a higher hit@1 (0.96 vs. 0.83), better multi-section recall at k=3 and k=5, fewer total chunks (257 vs. 426), equal hit@5 (1.00), and stable chunk hashes when text changes.


## Tools and subagent
The MCP server (`server.py`) defines two tools whose descriptions tell the model how to behave:
- `search(query)`: Searches Title 29 CFR Parts 825, 785, and 531 (1 November 2026 snapshot) plus any added documents, returning up to 5 passages ranked by relevance. It tells the model to search for every question about these rules, answer only from the returned passages, and state that the corpus does not cover the question if none of the closest passages contain the answer.
- `add_document(path)`: Indexes an eCFR XML file already saved in the `corpus/` folder (refusing any other path or file type), skips unchanged content-hashed chunks, and removes obsolete chunks from that source. It instructs the model to call `add_document` only when the user explicitly asks to add a document, never to answer a question.

For `q01` (*"How much advance notice is required for foreseeable FMLA leave when 30 days' notice is practicable?"*), `search` returned the exact section as the top hit:

~~~text
[1] 29 CFR Part 825, § 825.302 (relevance 0.84)
§ 825.302 Employee notice requirements for foreseeable FMLA leave. (a) Timing of notice. An employee must provide the employer at least 30 days advance notice before FMLA leave is to begin if the need for the leave is foreseeable based on an expected birth, placement for adoption or foster care, planned medical treatment for a serious health condition ...
~~~

The subagent (`.claude/agents/corpus-researcher.md`) is only allowed to use `mcp__corpus__search`. Its instructions tell it to search with English keywords (and re-search with different terms if needed), answer strictly from the returned passages, cite the source and section for every claim using only sections from the results, stay within federal rules only, keep answers short (answer first, then citation), and refuse without guessing while suggesting HR or the Wage and Hour Division when the answer is not in the text.

I could not run the subagent directly in my editor because the chat panel in VS Code showed `"No models available"` (Claude models in Copilot require a paid plan, and the Claude session had no model access). Instead, the exact same `search` tool was used over MCP by my own agent (`agent.py`), as shown in the evaluation and the `add_document` demo.


## Adding a document
Because each chunk ID is a content hash, running `index_file` on a document that is already indexed skips existing chunks (embedding 0 new ones) and deletes any stored chunks of that source that no longer exist in the file. Running `uv run main.py index` again confirmed this:

~~~text
Embeddings needed now: 0 (free tier: about 1,000 a day, questions count too)
section   29 CFR Part 825    embedded 0, kept 170, deleted 0
section   29 CFR Part 785    embedded 0, kept 51, deleted 0
section   29 CFR Part 531    embedded 0, kept 36, deleted 0
~~~

To test adding a new document, I used unanswerable question `q28` (asking for the Part 778 regular-rate formula for commissions and bonuses) and added `corpus/29cfr778_2026-11-01.xml` through the agent after approving the prompt (`Allow add_document(...)? [y/N] y`). This added 155 newly embedded chunks, growing the `section` index from 257 to 412 chunks (afterward, I restored the index back to 257 chunks so the committed index matches the test set):
- **Before adding Part 778:** Two searches only found cross-references to Part 778 inside Part 531 (`§ 531.60`, `§ 531.27`), and the agent properly stated that Part 778 was not included in the corpus and declined to give the formula.
- **After adding Part 778:** All five retrieved passages came from Part 778 (`§ 778.117`, `§ 778.118`, `§ 778.209`, `§ 778.208`, `§ 778.502`, relevance 0.82 to 0.85), and the agent accurately explained the regular-rate rule for a single workweek and for deferred bonuses with citations (full transcripts are in `eval/add_document_demo.md`).

This shows that a reference answer depends on the current state of the corpus: once Part 778 is added, `q28`'s original reference ("not stated in the supplied documents") is no longer true.


## Harness and guardrails
`AGENTS.md` sets seven rules for the assistant. The three rules I consider most important are:
1. **Search first and answer only from what `search` returns (Rules 1 & 2):** LLMs can easily make up plausible-sounding legal rules, so forcing every answer to come strictly from retrieved passages prevents hallucinations that could cost a worker pay or leave rights.
2. **Cite every claim with source and section (Rule 3):** Requiring exact section citations (like `29 CFR Part 825, § 825.302`) lets the worker look up and verify the actual text.
3. **Say when the corpus does not cover the question and stick to federal rules only (Rules 4 & 5):** Clearly stating when something falls outside the corpus (such as state laws, company policies, or missing parts) and suggesting HR or the Wage and Hour Division prevents misleading advice.

In addition to prompt rules, `agent.py` enforces two guardrails in code:
- **Human approval on `add_document`:** Implemented with `@wrap_tool_call` (`approval_guardrail`), the harness pauses before `add_document` runs and asks a person at the keyboard (`[y/N]`), whereas `search` only reads data and needs no approval. Because added documents become the reference for all future answers, human approval stops misleading or wrong files from being indexed. During evaluation, approval is automatically set to `"deny"` so unattended runs cannot change the index (`tried_add_document` was `0/30`), while the prompt fired properly during the `add_document` demo.
- **Model call limit (`CALL_LIMIT = 8`):** Implemented via `ModelCallLimitMiddleware(run_limit=CALL_LIMIT)` to prevent infinite tool loops while still giving enough room for multiple searches and synthesis. In the evaluation, no question took more than 3 searches (at most 4 model calls), so the limit never fired.

Other guardrails considered included refusing when the top search similarity score is too low (risky because the unanswerable questions are very close to the topic and would need careful threshold tuning), while citation validity (`30/30`) and search-before-answer compliance (`30/30`) were checked directly in `evaluate.py`.


## Evaluation
For evaluation, the agent ran on `gemini-3.5-flash-lite`, while the judge ran on `gemini-3.5-flash` for the first 25 questions and `gemini-3.5-flash-lite` for the last 5 (`q26` to `q30`) after the free quota for `gemini-3.5-flash` ran out. Exact code checks confirmed that the agent searched before answering on `30/30` questions, cited only sections that appeared in the retrieved passages on `30/30` questions, and tried `add_document` `0` times.

The final `JUDGE_RUBRIC` in `evaluate.py` checks `correct`, `supported`, and `refused` (with `reasoning` written first before computing one `outcome()` label in code):

~~~text
For a question that the corpus CAN answer:
- correct: the answer states the same essential facts as the reference answer (same numbers,
  same conditions, same exceptions). Extra detail is fine if it is true to the retrieved text.
  A missing key fact, a wrong number or a wrong condition makes it NOT correct.
- supported: every claim in the answer is stated in the retrieved passages. A claim that is not
  in the retrieved passages is unsupported, even if it happens to be true in real life.
- refused: the answer says the documents do not cover the question or declines to answer.
For a question that the corpus CAN NOT answer:
- refused: the answer clearly says the documents do not cover it (it may suggest asking HR or the
  Wage and Hour Division). Giving a specific answer from memory is NOT a refusal.
- supported: nothing in the answer goes beyond the retrieved passages.
~~~

I reviewed the draft rubric and kept it unchanged because it already separated factual accuracy (correct), strict grounding in the retrieved passages (supported), and proper abstention (refused), which matched how I graded the answers manually.

| Metric | Judge | My grades |
| --- | --- | --- |
| Answerable questions correct | 24/24 | 22/24 (`q20`, `q23` graded 0) |
| Unanswerable questions refused correctly | 5/6 | 5/6 (`q27` graded 0) |
| Wrong refusals (answerable questions refused) | 0 | 0 |
| Unsupported claims | 0 on answerable | 1 (`q20` `supported = 0`) |

My grades agreed with the judge on **28/30** questions for `correct` and **29/30** for `supported`, with disagreements on `q20` and `q23` where the judge was more lenient than I was. Across all 30 questions, the agent averaged **21.5 seconds** and **4,772 tokens** per question.


## Failures
| Cause | Count | Questions |
| --- | --- | --- |
| Retrieval miss (`multi` question; `§ 785.11` not retrieved) | 1 | `q20` |
| Bad test question or bad reference | 2 | `q23` (reference took an illustrative example in `§ 531.36(a)` as a rule, whereas deductions for facilities may reduce cash wages below minimum wage in non-overtime weeks), `q27` (actually answerable from `§ 825.207(a)`: FMLA leave is unpaid and accrued paid leave may be substituted) |
| Wrong answer from the right passage | 0 | |
| Unsupported claim | 0 (1 under stricter manual grading on `q20`) | |
| Wrong refusal | 0 | |

There was also a minor issue on `q25`, where the agent refused properly (`1,1`) but forgot to suggest asking HR or the Wage and Hour Division as stated in the reference. On `q27`, the judge marked the answer as a `"hallucination"` only because the test set expected a refusal, even though the judge's own reasoning pointed out that the answer came directly from the retrieved passages.

The first thing I would fix is cleaning up the test set by correcting `q23`'s reference answer to match `§ 531.36(a)` and rewriting `q27` so it is genuinely unanswerable (I left them unchanged for this report because I found the mistakes after seeing the results, so keeping the test set frozen and documenting the errors is fairer). After that, I would improve retrieval for `multi` questions (where only 4/7 found all expected sections in the top 5) by having the agent break complex questions into smaller, separate search queries instead of running one combined query.


## Decision
I would let workers rely on this assistant only as a quick first lookup to find relevant federal CFR sections, not as a final authority for making important workplace decisions. While it performed well on single-topic federal rules (24/24 correct according to the judge and 22/24 under my stricter grading, 30/30 searches run before answering, 30/30 valid citations, and no made-up answers on truly unanswerable questions), its limitations make blind trust too risky. Specifically, the test set only has 30 self-written questions worded close to the regulation text, multi-section recall is weaker (4/7 at top-5), state laws and company policies are not covered, the eCFR snapshot is unofficial, and each query takes an average of 21.5 seconds and 4,772 tokens.

To use it safely, three safeguards should stay in place:
1. Always show exact `29 CFR` section citations so the worker can read the original regulation text themselves.
2. Keep the human-approval step on `add_document` so unverified documents cannot enter the index.
3. Always include a reminder to check with HR or the U.S. Department of Labor Wage and Hour Division before making decisions that affect pay or leave.


## AI use
AI was used throughout the project as a coding and review assistant. It explained technical concepts in plain language, caught a formatting bug where `questions.csv` had been saved with `;` separators instead of commas, and pointed out borderline answers (`q10`, `q20`, `q21`, `q23`, `q25`, `q27`) that I should re-read carefully before grading (without assigning my grades). I made all key design and evaluation decisions myself, such as choosing the workplace-rules topic and federal-only scope, selecting titles, choosing `section` chunking and forming the retrieval hypothesis, setting the guardrails (human approval for `add_document` and `CALL_LIMIT = 8`), grading answers in `eval/human_labels.csv` and writing the failure analysis and final decision.
