# Decision log (draft for REPORT.md)

Decisions made by Máximo during development, with the alternatives and the evidence considered. How decisions were made: at each decision point Claude (the AI assistant that wrote the code) explained the possible options, with evidence and a recommendation, and Máximo chose which one to take. It is the basis for writing REPORT.md in Máximo's own words.

## 1. Use case (2026-11-21)

- **Chosen:** a consultant at a professional-services firm who prepares electric-vehicle market reports for clients in the automotive sector.
- **Cost of an error:** a wrong figure in a client report feeds investment decisions (sizing a battery plant, launching a model) and damages the firm's credibility. "I don't know" costs about 10 minutes of checking the source.
- **Alternatives rejected:** the English football regulator (licence not confirmed, legal language), the F1 regulations (FIA copyright), NIST cybersecurity guidance, NHTSA recall reports.

## 2. Corpus (2026-11-21)

- IEA reports under CC BY 4.0, downloaded from the IEA's official blob storage (iea.org blocks scripted downloads with a Cloudflare bot check).
- Global EV Outlook 2026 (executive summary, ch. 1, 2, 5 and 9), Global EV Outlook 2025 (executive summary, ch. 1-2) and Global Critical Minerals Outlook 2026 (executive summary and the lithium, nickel, cobalt and graphite outlooks).
- About 73k words in the selected pages and about 56k words of body text after cleaning.
- "Electric Car Markets in a Time of Uncertainty" (July 2026) is held out for the add_document demo.

## 3. Extraction: problem found and fix

- With `pypdf`, words were split ("sale s", "r ecently") and chart labels were mixed into the text. Switched to **PyMuPDF**, which gives the font size of every line: body text is ~11 pt, headings ≥14 pt, and noise (running headers, chart axes, notes) ≤9 pt. Only body text and headings are kept.
- Other fixes: reading order on the two-column pages of the minerals report, "CO₂" coming out as "CO", and paragraphs cut by a page or column break, which are now joined.
- Found later, while testing the MCP server (2026-11-22): the PDF of GEVO 2026 repeats the last two lines of p. 18 at the top of p. 19, so one chunk contained a sentence twice. When a paragraph continues on the next page and the new page starts with the same 8+ words, the repetition is now removed. It changed 1 structured chunk; in the fixed design the windows after that point shifted (71 chunks re-embedded).

## 4. Figure notes and footnotes

- **Decision:** drop them.
- **Reason:** they add ~5,500 words (~10% more embeddings), and almost all of them are sources, abbreviations or descriptions of charts the system cannot see. Some definitions are lost (e.g. "battery pack price").

## 5. Chunking designs to compare

- **Decision:** A = fixed windows of 150 words with a 30-word overlap (469 chunks) versus B = one chunk per report section, max. 250 words, with a "report · chapter · heading" header (322 chunks).
- **Reason:** it compares two different chunking philosophies (fixed size versus document structure) and fits in one day of free-tier quota (~790 embeddings).
- **Rejected:** fixed 100 versus fixed 250 (~980 embeddings, compares size only) and fixed versus hybrid search (does not compare chunkings; hybrid search can be added later as a third design at no embedding cost).
- The final design will be chosen from hit rate @1/3/5.

## 6. Embeddings and storage (2026-11-22)

- **Vector size (decision):** `gemini-embedding-2` with **768** dimensions. Alternatives: 1,536 (~15 MB) and 3,072 (~30 MB, maximum quality). Reason: the model is trained so that shorter vectors lose very little quality, the structured design already reaches 100% hit@5 (so a gain could not even be measured), `index/` stays at 8.4 MB, and changing would cost a full re-embedding (~900 texts, about one day of free quota).
- **Task type (decision):** `RETRIEVAL_DOCUMENT` for chunks and `RETRIEVAL_QUERY` for questions, Google's recommended setup for search, so a short question lands close to the long passage that answers it. Rejected: one generic vector for both (usually slightly worse for question → passage search, and it would need re-embedding).
- **Storage (decision):** JSONL files in `index/` (chunks per design plus one shared vector cache) and cosine-similarity search with numpy, the "similar to ChromaDB" option allowed by the brief. Reason: every chunk can be opened and read with its page, the search is ~20 lines that can be explained, and there is no extra dependency; at ~320 chunks a full scan takes milliseconds. Rejected: ChromaDB (a binary folder that cannot be read in git; its speed only matters at thousands or millions of chunks).
- Each vector is saved as soon as it arrives, keyed by a hash of (model, dimensions, task, text). Re-running `main.py index` spends no embeddings, and question vectors are cached too.
- **Problem found:** with `gemini-embedding-2`, a list of texts is embedded as **one** input and returns a single vector. It was spotted because only 10 vectors had been saved for 469 chunks. Fixed by sending each text as its own `Content` and checking that the number of vectors matches.
- **First sign of the "wrong year" risk (seen before the test set existed):** for the question "What was the EV sales share in Europe in 2024?", the fixed design ranks a chunk from the 2026 report first instead of the 2025 one.

## 7. Test set (`eval/questions.csv`)

- **Written by Máximo** from the PDFs, in English, before any retrieval tuning. Claude only checked it (format, counts, that each answer is in the indexed text on the stated page, and that unanswerable questions are not answered by the corpus) and suggested where coverage was thin. The questions themselves were not changed by Claude.
- **Counts:** 32 questions = 20 `single`, 6 `multi`, 6 `unanswerable`. By document (answerable passages): GEVO2026 most, then GEVO2025 and GCMO2026.
- **Location convention:** `expected_source` = document code (`GEVO2026`, `GEVO2025`, `GCMO2026`); `expected_location` = printed page number. For `multi`, both lists are `;`-separated in the same order.
- **Design choices:**
  - Answers are taken from body text, not charts (charts are not indexed), and every question states the year it refers to, because two editions of the same report are in the corpus.
  - `multi` questions compare the two editions (2024 vs 2025 figures) or cross documents (EV battery deployment + lithium demand; lithium price spike + sodium-ion batteries).
  - After a first review, two questions on the outlook chapter (ch. 9, the largest chapter and the most relevant one for a consultant) replaced two regional market questions.
  - **Unanswerable questions are near-misses:** the corpus contains related figures that could tempt the system into an unsupported answer (Spain's +80% sales growth vs Spain's sales *share*; the 2025 battery price decline vs the full-year 2026 change; other countries' 2040 targets vs a Spain 2040 projection). Two very specific questions first drafted (nickel content of a Tesla Model 3, maintenance cost of a VW ID.3) were replaced because they would be too easy to refuse.
  - `q32` (Q2 2026 global EV sales vs Q2 2025) is unanswerable with the initial corpus but answered by the held-out July 2026 report ("4% higher year-on-year"): it is the question for the add_document before/after demo.
  - `q01` is an easy, clearly answerable `single` question because `check.py` uses it to test the search tool and `main.py ask`.
- **Two examples:** q09 (`single`): "How much battery capacity was deployed in electric vehicles worldwide in 2025 and how much did deployment grow from 2024?" → GEVO2026 p. 92, "1.2 TWh, almost +30%". q23 (`multi`): "How did the electric share of new car sales in Europe change between 2024 and 2025?" → GEVO2025 p. 17 + GEVO2026 p. 21, "about 20% → 28%".

## 8. Retrieval metric

- **Hit definition (decision):** a retrieved chunk is a hit for an expected passage when it comes from the expected document **and** its page range includes the expected page (exact page, no ±1 tolerance, so errors are not hidden).
- **Multi-passage questions (decision):** strict — a `multi` question counts as a hit at k only if **both** expected passages are in the top k, because the agent cannot answer correctly with only one. The partial score (share of expected passages found) is reported as a secondary figure to explain failures.
- Unanswerable questions have no expected passage and are excluded from hit rate (they are evaluated end to end).
- Also reported: words added to the prompt at each k (sum of the words of the top-k chunks), because larger chunks may raise hit rate at a higher token cost.

## 9. Retrieval results and design choice

Results on the 26 answerable questions (`eval/retrieval_summary.md`, per question in `eval/retrieval_results.csv`):

| Design | hit@1 | hit@3 | hit@5 | words@5 |
|---|---|---|---|---|
| A · fixed 150 (overlap 30) | 58% | 69% | 81% | 750 |
| B · structured (sections ≤250 + header) | 77% | 88% | 100% | 984 |

- `single`: fixed 75% / 90% / 95%; structured 100% / 100% / 100%.
- `multi` (strict): fixed 0% / 0% / 33%; structured 0% / 50% / 100%. Strict hit@1 is 0% by construction for both designs, because one chunk rarely covers two passages; partial@1 (fixed 50%, structured 33%) shows that one passage is usually found first.
- **Why fixed fails:** four of its five misses at k=5 (q21-q24) are multi questions where the GEVO 2025 passage is never retrieved; the GEVO 2026 chunk with the same topic always wins. This is the **"wrong edition"** problem, also visible in single questions (q13, a 2024 UK figure: top-1 is a 2026 chunk). Fixed chunks carry no title or year in their text, and they cut sections in the middle. (The fifth miss, q03, appeared after the duplicated-lines fix in section 3 shifted the fixed windows: the table above is the re-run; before the fix fixed scored 58% / 73% / 85%. Structured did not change.)
- **Why structured works:** each chunk starts with "report title · chapter · heading", so the edition year and topic are part of the embedded text. IEA headings often state the key figure (e.g. "Close to 55% of new cars sold in China were electric in 2025"), and whole sections keep the answer together.
- **Decision (Máximo): structured design, k = 5.** It wins at every k, and k=5 is the smallest k that finds both passages of every multi question, at ~990 words (~1,300 tokens) per search, about 30% more than fixed. k=3 would drop to 50% on multi questions.
- **Caveat:** 26 questions is a small sample (one question ≈ 4 points), and the questions were written from body text, which helps any design. The "wrong edition" pattern is the robust finding.

## 10. MCP server and duplicate policy for add_document (2026-11-22)

- **Decision (Máximo): content-based policy.** `index/documents.json` stores a SHA-256 hash of each indexed file and its number of chunks.
  - Same content as a document already indexed → nothing is changed and no embeddings are spent ("Already indexed").
  - Same document (same document id: a known IEA report, or the file name for new documents), different content → the new version **replaces** the old one, so two versions with different figures never mix in search results.
  - Otherwise → added.
- **Reason:** the IEA publishes revised versions of its reports (GEVO 2026 has a "revised version" with corrections), and a consultant always wants the latest one; keeping both would let the agent cite a corrected figure. Rejected: always refuse (cannot update a corrected report) and always add (duplicate chunks, mixed versions).
- **Known limit:** a new document is identified by its file name, so two different reports saved with the same file name would be treated as versions of one document.
- **Accepted formats (decision):** PDF only, so a new report goes through the same font-size cleaning, chapters and headings as the rest of the corpus. Rejected: also .txt/.md (a second, simpler pipeline whose chunks would cite less precisely; not needed for IEA reports).
- **Index a new document goes to (decision):** the structured design only (the one the server searches). Reason: half the embeddings, and the fixed-vs-structured comparison stays on the same 3 documents the test set was written for. Rejected: both designs.
- **On failure (decision):** all or nothing. Chunks are written to the index only after every vector has arrived, so a failure (e.g. the daily quota running out mid-report) leaves the index unchanged and returns an error; vectors already received stay cached, so a retry does not pay for them again. Rejected: saving what arrived (half a report would be searchable, and the agent could wrongly say the document does not contain something that is on a missing page).
- Errors (missing file, wrong format, quota) are returned to the caller as tool errors instead of stopping the server.
- `search` returns the 5 best passages, each with a header "Source: <doc_id>, p. <page> | title (year) | chapter · section | relevance" so the agent can cite (doc_id, p. page) with the same codes as the test set.
- **Tool descriptions (reviewed and approved by Máximo):** Claude explained what each description needs to tell the model; Máximo reviewed them and approved them. `search` states what the corpus covers (reports, chapters, topics), that chart-only figures are not indexed, to use one focused query per fact with the year (two editions cover the same topics), how to cite, and that no matching passage means the corpus does not contain the answer. `add_document` states what it does, PDF only, the duplicate policy, and to call it only when the user asked to add that file.
- **Tested** over MCP stdio as `check.py` does: both tools listed; q01 answered by GEVO2026 pp. 18-19 at rank 1; adding a corpus PDF again → "Already indexed" in 0.0 s; missing file and non-PDF → error. Added / replaced tested on a scratch copy of the index with a one-page test PDF (the July 2026 report is still held out for the demo).

## 11. Subagent `corpus-researcher` (2026-11-22)

`.claude/agents/corpus-researcher.md`, a Claude Code subagent whose only tool is `mcp__corpus__search`.

- **When to delegate (decision):** any factual question on the corpus topics (EV sales, shares, stock, prices, batteries, critical minerals, projections), so Claude Code delegates automatically and the searches do not fill the main conversation. Rejected: only when the user names the subagent (predictable, but it would rarely be used).
- **Refusal rule (decision):** give a figure only if a retrieved passage states it for exactly what was asked (same place, year and metric); simple arithmetic between two cited figures is allowed, showing both; never own knowledge, estimates or a related figure instead (Europe for Spain, 2025 for 2026, sales for share, forecast for actual). Otherwise: "The corpus does not cover this." Reason: in this use case a wrong figure is expensive and a refusal costs ~10 minutes. Rejected: no arithmetic at all (would fail the multi questions that compare 2024 and 2025) and flagged approximations (exactly the near-miss trap the unanswerable questions test). The same rule will go into `AGENTS.md` for `agent.py`.
- **Partly answerable questions (decision):** answer the covered part with its citation and say which part is not covered. Rejected: refuse the whole question (throws away verified information).
- **Search budget (decision):** at most 3 searches per question: one per fact (multi questions need two) plus one reworded search. Each search adds ~1,300 tokens. Rejected: one search (too few for multi questions) and no limit (unpredictable cost).
- Answer format: 1-4 sentences, every figure cited as (doc_id, p. page), the same codes as the test set.
- **First test in Claude Code (q23, both runs in `eval/subagent_transcript.md`):** delegation worked, only `search` was used, 3 searches. The answer (about 20% → 28%) was correct and cited. One error: the European forecast of "around 25%" for 2025 was cited to GEVO2025, p. 26, where that 25% is the **global** share; the European forecast is on p. 10. The figure was right, but the citation pointed to a passage about another scope. This is the same family as the "wrong edition" problem (right topic, wrong scope), so it was fixed in the instructions, not in retrieval. (A second error first reported by Claude, a wrong GEVO2025, p. 10 citation, turned out to be a mistake in Claude's own check: that page does give the European figure.)
- **Scope rule added (decision):** before using or citing a figure, check that its sentence is about the same region as the question (world, Europe, EU, country); a global or EU figure is not a European one. The same rule will go into `AGENTS.md`.
- **Second run with the scope rule:** correct answer, every figure labelled "Europe as a whole" or "EU only" and supported at the cited page, and no scope errors; the global passages it retrieved were not used. One minor miss: it said no 2025 UK share was found, although a retrieved passage gives "over 1 in 3" (GEVO2026, p. 21). This is a side detail, not a wrong figure. Run 2 is the transcript for REPORT.md, with run 1 as the "before".

## 12. Our agent: `AGENTS.md` and `agent.py` (2026-11-22)

`agent.py` uses LangChain `create_agent` on Gemini, with the two tools of `server.py` over MCP (stdio) and `AGENTS.md` as system prompt. It prints the answer, the cited passages and a cost line; `CorpusAgent.ask()` returns the answer, the tool trace, the tokens and the seconds for `evaluate.py`.

- **Rules in `AGENTS.md` (decision):** the same rules as the subagent, already tested in two runs (section 11), each with its reason: answer only from `search`, cite every figure as (doc_id, p. page), refuse unless a passage states the figure for the same place, year and metric (arithmetic between cited figures allowed), never substitute a related figure, answer the covered part, at most 3 searches, check year and scope, use `add_document` only on an explicit request, 1-4 sentences. Rejected: also quoting the source sentence for every figure (easier to verify, but longer and more expensive).
- **Extra guardrail (decision): citation check.** Before the answer is shown, code checks that every (doc_id, p. N) in it points to a page that a search returned for this question, and that an answer with figures cites them. If not, the agent is asked once to fix it; if it still fails, the answer is blocked with a message to check the sources by hand. Reason: the main risk of the use case is a figure with a false or missing source in a client report. Rejected: requiring every number to appear in the passages (false alarms on legitimate arithmetic and rounding) and a topic filter (cheap, but the real risk is in on-topic questions).
- **Model (decision): `gemini-3.5-flash`**, which reasons better about when to refuse, year, scope and arithmetic. Measured: ~8-19 s per model call today (it thinks before answering), 33-48 s and ~5,600 tokens for q01. `gemini-3.5-flash-lite` answered q01 correctly in 2.3 s; it is kept as the fallback if the free quota runs out. (`gemini-2.5-flash` is no longer available to new keys.)
- **Model changed to `gemini-3.5-flash-lite` (decision, 2026-11-24):** the first full evaluation run stopped after 10 of 32 questions with a 429 error: the free tier allows only **20 requests per day** for `gemini-3.5-flash` (quota `GenerateRequestsPerDayPerProjectPerModel-FreeTier`, value 20, reset at 09:00 Spain time), and each question takes about 2 model calls. Finishing the evaluation, the judge and the add_document demo would have taken 4-5 days with no margin to fix anything. Options considered: enable billing and keep `gemini-3.5-flash` (under USD 1 for the whole evaluation at USD 0.75 / 3.75 per million tokens), wait and run about 9 questions a day, or switch to `gemini-3.5-flash-lite` (free, about 10 times faster, had already answered q01 and the 6-country test correctly). Máximo chose `gemini-3.5-flash-lite`; all answers are redone with it (the 10 answers from `gemini-3.5-flash` are not used).
- **Call limits (decision):** at most 3 searches (`ToolCallLimitMiddleware`, extra calls are blocked and the agent answers with what it has) and 6 model calls (`ModelCallLimitMiddleware`) per question, consistent with the subagent.
- **Approval before `add_document`:** a LangChain middleware intercepts the tool call and asks "Approve? [y/N]" in the terminal; anything but "y" refuses it and nothing changes. Without a terminal (`check.py`, `evaluate.py`) it is refused automatically.
- **Tests:**
  - `check.py`: all checks pass. q01 is answered correctly, 44 million (GEVO2026, p. 18), with the citation check passing.
  - Approval refused → the tool did not run, and the agent said the document was not added.
  - Approval given for a corpus PDF → "Already indexed".
  - A question asking for 6 separate searches → only 3 ran.
- **Known limitations found in the tests:**
  - When the search limit blocks a search, the agent wrote "the corpus does not cover" Japan, Brazil and Germany, although Germany's 2025 share is in the corpus (GEVO2026, p. 21). It is a wrong refusal caused by the limit, not by the corpus.
  - When the citation check asks for a fix, the second attempt can search again, with up to 3 more searches.
- **Rule added after the tests (decision):** if the search limit stops a search, the agent must write "Not searched (search limit reached): ..." instead of "The corpus does not cover this" (`AGENTS.md`, rule 10). Re-test with the 6-country question:
  - `gemini-3.5-flash`: China ~55% and US just under 10% (GEVO2026, p. 10), then "Not searched (search limit reached): India, Japan, Brazil and Germany". It took 105 s.
  - `gemini-3.5-flash-lite`: China, US and India answered, then "Not searched (search limit reached): Japan, Brazil and Germany". It took 6 s.
  - Neither model claims that the corpus lacks a figure it never searched.

## 13. End-to-end evaluation (2026-11-24)

`evaluate.py` part 2 runs the agent on every question of `eval/questions.csv`, checks the answers in code, writes a file for blind human grading, runs an LLM judge once the human grades exist, and reports the agreement, the results and the cost per question (`eval/e2e_summary.md`, `eval/e2e_results.csv`).

- **Judge rubric (decision): the same two 1/0 criteria as the human grades**, each with a one-sentence reason:
  - *correct*: the key figures and facts match the reference answer (rounding and hedging such as "almost 30%" vs "nearly 30%" are fine); for an unanswerable question, 1 only if the answer says the corpus does not cover it and presents no substitute figure.
  - *supported*: every figure and claim appears in the passages that `search` returned, judged against the passages only.
  - Reason: with the same scale as `eval/human_labels.csv`, agreement is compared criterion by criterion with no threshold to choose. Rejected: a 1-5 scale (needs a threshold to compare with 1/0 grades) and a single pass/fail (mixes "wrong" with "unsupported" and does not help to classify failures).
- **Partial answers (decision): correct = 0.** An answer is correct only if it answers every part of the question; covering one part and flagging the other as not covered or not searched gets 0. Reason: an incomplete figure set is not what the client asked for, and counting it as correct would inflate the score. Rejected: correct = 1 when the gap is flagged.
- **Judge model (decision): `gemini-3.5-flash-lite`.** First chosen: `gemini-3.5-flash`, the strongest model that works with the key. After the agent moved to `gemini-3.5-flash-lite` because of the 20-requests-a-day limit (section 12), the judge's 32 calls on `gemini-3.5-flash` would have taken 2 days. Máximo chose `gemini-3.5-flash-lite` for the judge too, so the evaluation finishes in a day. Known risk: the model grades its own answers and is weaker at spotting substituted figures; the agreement with the human grades measures exactly this. The code asks for temperature 0, but the API ignores it for `gemini-3.5-flash-lite` (warning: "uses fixed sampling defaults"), so the judge is not fully deterministic: a borderline answer could get a different verdict in another run. The verdicts are saved in `eval/judge_verdicts.jsonl` and reused, so the reported results can be checked.
- **Code checks (decision): all four, with the number check as a warning only.**
  - *Citations valid*: every (doc_id, p. N) points to a page a search returned for that question (the same check as the guardrail; a blocked answer fails).
  - *Refusals*: an unanswerable question must get an answer that starts with "The corpus does not cover this"; an answerable one must not.
  - *Expected page retrieved and cited*: whether a search returned the page in `expected_location`, and whether the answer cites it. This separates retrieval misses from wrong answers taken from the right passage.
  - *Numbers not in the passages* (warning): numbers in the answer, years and citations left out, that no retrieved passage contains. Not counted as a failure because computed figures (28 - 20 = 8) and formats are flagged too.
- **Reuse of answers (decision):** answers and verdicts are saved in `eval/` and reused while the question, `AGENTS.md`, the model and the call limits are unchanged (`EVAL_FRESH=1` runs everything again). Reason: the human grades must refer to the same answers that the judge grades, and the free quota is small. Rejected: running from scratch every time (answers change between runs).
- **Blind grading (decision): two steps.** The first run writes `eval/answers_to_grade.md` (question, reference, answer, cited and other retrieved passages, no verdicts). The judge does not run until `eval/human_labels.csv` has 20 grades, so Máximo grades before any verdict exists. Rejected: running the judge at once and not opening its file (depends on discipline instead of the code).
- **Questions asked 3 at a time (decision):** each worker has its own agent and `server.py` process, so traces do not mix (`EVAL_WORKERS`). It changes only the wall-clock time of the evaluation, not the answers or the latency reported per question.
- **What counts as a refusal (decision):** in the first full run 5 of the 6 unanswerable questions were refused correctly but began "The corpus does not cover which manufacturer..." or "The corpus does not state..." instead of the exact phrase "The corpus does not cover this." (AGENTS.md, rule 5), so the strict check marked them as failures. Máximo chose to count any answer that starts with "The corpus does not" as a refusal, because what matters to the consultant is that no figure is given as the answer; whether the exact phrase is used is reported separately as a format detail (1 of 6). Rejected: the exact phrase only (1/6, exaggerates the failure) and tightening rule 5 now (would invalidate all answers).
- **Rate limit of `gemini-3.5-flash-lite`:** the free tier allows 15 requests a minute (the first parallel run hit it after 9 questions). The agent and the judge share one client-side limiter at 12 requests a minute, and a per-minute 429 puts the question back in the queue. Because of the limiter, the seconds measured with 3 questions at a time include waiting, so they overstate the latency of a single question.
- **Results (2026-11-24):** Máximo graded all 32 answers (`eval/human_labels.csv`) before the judge ran. Human grades: correct 31/32, supported 32/32; the only 0 is q13 (the answer gives "nearly 30%" and "1 in 4" for the UK in 2024 without resolving the discrepancy). Judge: correct 32/32, supported 32/32. Agreement: correct 31/32 (97%), supported 32/32 (100%). Cohen's kappa is 0.00 for correct (undefined for supported) because almost every grade is 1: with so little variation, kappa cannot show agreement beyond chance, and the judge has not been seen to give a 0. Two judge calls (q22, q23) failed with a temporary 503 and were redone on the next run.
- **Test of the judge on planted wrong answers (decision):** because almost every real grade is 1, kappa could not show whether the judge ever gives a 0. Máximo chose to add planted wrong answers (rejected: re-running the judge 3 times to measure stability, which would probably give all 1s again, and reporting kappa as it is). `eval/judge_traps.csv` holds 8 answers to real questions, each written by Claude to contain one error that matters in this use case: another country's figure, another year, sales growth given as share, a forecast given as an actual value, an invented figure, a right figure plus an invented claim, a missed refusal and a partial answer. They are judged with the passages their base question retrieved. At Máximo's request their expected grades were set by Claude by construction (the planted error decides them), not graded by Máximo; the 32 human grades of real answers are unchanged.
  - Result: the judge gave 0 to every expected 0 (7/7 for correct, 7/7 for supported). The one disagreement is t06 (right surplus figure plus an invented "40%" growth): expected correct 1, supported 0; the judge gave correct 0 as well, so it is stricter than the rubric when an answer adds a wrong claim. On t08 (partial answer) both expected and judge give supported 1, although the answer wrongly says the corpus lacks the growth figure.
  - Real and planted answers together: correct 38/40 (95%, kappa 0.84), supported 40/40 (100%, kappa 1.00).
