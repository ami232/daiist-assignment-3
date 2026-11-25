# Decision log

The decisions taken during the project, with the reason, the alternatives rejected and the evidence behind them. REPORT.md summarises them.

## 1. Use case

- **Chosen:** a consultant who prepares electric-vehicle market reports for clients in the automotive sector.
- **Cost of an error:** a wrong figure in a client report feeds investment decisions (a battery plant, a model launch) and damages the firm's credibility. "I don't know" costs about 10 minutes of checking the source.
- **Rejected:** the English football regulator (licence not confirmed), the F1 regulations (FIA copyright), NIST cybersecurity guidance, NHTSA recall reports.

## 2. Corpus

- **Chosen:** IEA reports under CC BY 4.0, downloaded from the IEA's blob storage (iea.org blocks scripted downloads):
  - Global EV Outlook 2026: executive summary, ch. 1, 2, 5 and 9.
  - Global EV Outlook 2025: executive summary, ch. 1-2.
  - Global Critical Minerals Outlook 2026: executive summary; lithium, nickel, cobalt and graphite outlooks.
- **Size:** about 73k words in the selected pages, about 56k after cleaning.
- **Held out:** "Electric Car Markets in a Time of Uncertainty" (July 2026), kept for the add_document demo.

## 3. Extraction

- **Problem:** `pypdf` split words ("sale s") and mixed chart labels into the text.
- **Fix:** switched to **PyMuPDF**, keeping lines by font size: body about 11 pt, headings 14 pt or more, noise 9 pt or less.
- **Other fixes:** reading order on two-column pages, "CO₂" read as "CO", and paragraphs cut by a page or column break, which are now joined.
- **Found later:** the GEVO 2026 PDF repeats the last lines of p. 18 at the top of p. 19, so one chunk contained a sentence twice.
  - Fix: when a paragraph continues on the next page and the page starts with the same 8 or more words, the repetition is removed.
  - Effect: 1 structured chunk changed, and 71 fixed chunks were re-embedded.
- **Figure notes and footnotes are dropped:** they would add about 10% more embeddings and are mostly sources and descriptions of charts that are not indexed.

## 4. Chunking designs to compare

- **A:** fixed windows of 150 words with a 30-word overlap (469 chunks).
- **B:** one chunk per section, at most 250 words, with a "report · chapter · heading" header (322 chunks).
- **Reason:** it compares fixed size against document structure, and both fit in one day of free embedding quota.
- **Rejected:** fixed 100 against fixed 250 (compares size only), and fixed against hybrid search (does not compare chunkings).

## 5. Embeddings and storage

- **Vectors:** `gemini-embedding-2` with 768 dimensions.
  - Reason: shorter vectors lose very little quality, the structured design already reaches 100% hit@5, and `index/` stays small.
  - Rejected: 1,536 and 3,072 dimensions.
- **Task types:** `RETRIEVAL_DOCUMENT` for chunks and `RETRIEVAL_QUERY` for questions, Google's setup for search.
- **Storage:** JSONL in `index/` with cosine search in numpy.
  - Reason: every chunk is readable with its page, there are no extra dependencies, and a scan of about 320 chunks takes milliseconds.
  - Rejected: ChromaDB, whose binary folder cannot be read in git.
- **Caching:** each vector is saved as soon as it arrives, keyed by a hash of the text, so re-running the index spends nothing.
- **Bug found:** a list of texts was embedded as a single input (10 vectors came back for 469 chunks). Fixed by sending each text separately and checking the count.

## 6. Test set (`eval/questions.csv`)

- **Size:** 32 questions (20 single, 6 multi, 6 unanswerable), written from the PDFs before any tuning.
- **Location format:** document code and printed page number.
- **Answers come from body text, not charts,** and every question states its year, because two editions are in the corpus.
- **Multi questions** compare the two editions (2024 against 2025) or cross documents (battery deployment with lithium demand; lithium price with sodium-ion batteries).
- **Unanswerable questions are near-misses**, with a related figure in the corpus: Spain's sales growth against its sales share, or the 2025 battery-price decline against the 2026 change.
- **q32** (Q2 2026 sales) is answered only by the held-out report, so it is the add_document demo question.
- **q01** is easy on purpose, because `check.py` uses it.

## 7. Retrieval metric

- **Hit:** a chunk from the expected document whose page range includes the expected page, with no ±1 tolerance.
- **Multi questions:** strict, both passages must be in the top k. The partial score is also reported.
- **Unanswerable questions** are left out of hit rate and evaluated end to end.
- **Words added to the prompt** are reported at each k, as the cost side.

## 8. Retrieval results and design choice

Results on the 26 answerable questions:

| Design | hit@1 | hit@3 | hit@5 | words@5 |
|---|---|---|---|---|
| A · fixed 150 (overlap 30) | 58% | 69% | 81% | 750 |
| B · structured (≤250 + header) | 77% | 88% | 100% | 984 |

- **Fixed design:** four of its five misses (q21-q24) are multi questions where the GEVO 2025 passage never appears, because the GEVO 2026 chunk on the same topic always wins. This is the **"wrong edition"** problem.
- **Structured design:** the header puts the edition year and topic into the embedded text, and sections keep each answer together.
- **Chosen: structured, k = 5.** It wins at every k, and k = 5 is the smallest k that finds both passages of every multi question (about 1,300 tokens per search). With k = 3, multi questions drop to 50%.
- **Caveat:** 26 questions is a small sample.

## 9. MCP server and add_document

- **Duplicate policy, based on content:** a SHA-256 hash is stored per file in `index/documents.json`.
  - Same content: nothing changes.
  - Same document with new content: it replaces the old version, so the figures of two versions never mix.
  - Otherwise: added.
  - Reason: the IEA publishes revised reports, and the consultant wants the latest one.
  - Rejected: always refusing, and always adding.
- **Known limit:** a new document is identified by its file name.
- **Format:** PDF only, so new reports get the same cleaning.
- **Index:** a new document goes into the structured design only.
- **On failure, all or nothing:** chunks are saved only after every vector has arrived. Half a report would let the agent wrongly say a page is not in the corpus.
- **Search result format:** 5 passages, each with a header "Source: doc_id, p. page | title (year) | chapter · section | relevance".
- **Tool descriptions:**
  - `search` says what the corpus covers, that chart-only figures are not indexed, to use one query per fact with the year, how to cite, and that no matching passage means the corpus does not contain the answer.
  - `add_document` says what it does, PDF only, the duplicate policy, and to call it only when the user asked.
- **Tests:** re-adding a corpus PDF gives "Already indexed"; a missing file or a non-PDF gives an error; adding and replacing were tested on a scratch copy of the index.

## 10. Subagent `corpus-researcher`

- **Tool:** only `mcp__corpus__search`.
- **Delegation:** any factual question on the corpus topics.
- **Refusal rule:**
  - give a figure only if a passage states it for the same place, year and metric;
  - arithmetic between cited figures is allowed;
  - never use own knowledge or a related figure (Europe for Spain, 2025 for 2026, sales for share, a forecast for an actual value);
  - otherwise answer "The corpus does not cover this."
  - Rejected: no arithmetic at all (it would fail the comparisons), and flagged approximations.
- **Partial questions:** answer the covered part and say what is missing.
- **At most 3 searches:** one per fact plus one reworded search.
- **Run 1 (q23):** correct answer (20% → 28%), but a global 25% was cited as the European forecast (GEVO2025, p. 26).
- **Scope rule added:** the sentence must be about the same region as the question. A global or EU figure is not a European one.
- **Run 2:** correct, every figure labelled "Europe" or "EU only", no scope errors. One minor miss: it said no 2025 UK share was found, but GEVO2026, p. 21 gives one.

## 11. Agent: `AGENTS.md` and `agent.py`

- **Framework:** LangChain `create_agent` on Gemini, with the `server.py` tools over MCP and AGENTS.md as the system prompt.
- **Rules:** the subagent's rules, each with its reason.
  - Rejected: quoting the source sentence for every figure (longer and more expensive).
- **Extra guardrail, a citation check:**
  - every (doc_id, p. N) must be a page a search returned, and figures must be cited;
  - one retry, then the answer is blocked;
  - reason: the main risk is a figure with a false or missing source;
  - rejected: requiring every number to appear in the passages (false alarms on arithmetic), and a topic filter.
- **Approval:** a middleware asks "Approve? [y/N]" before `add_document`. With no terminal it refuses.
- **Limits:** 3 searches and 6 model calls per question.
- **Model:**
  - First `gemini-3.5-flash`, for better reasoning on refusals and scope.
  - The first evaluation run stopped after 10 of 32 questions: the free tier allows **20 requests a day** for that model.
  - Options considered: billing (under USD 1), running about 9 questions a day, or `gemini-3.5-flash-lite`.
  - Chosen: `gemini-3.5-flash-lite` (free, about 10 times faster). All answers were redone with it.
- **Tests:** approval refused means the tool did not run; approval given gives "Already indexed"; a 6-search request ran only 3 searches.
- **Rule 10, added after a test:** when the search limit blocked a search, the agent said the corpus "does not cover" Germany, although it does. Now it writes "Not searched (search limit reached): …". Both models passed the re-test.

## 12. End-to-end evaluation

- **Judge rubric:** the same two 1/0 criteria as the human grades, each with a one-sentence reason.
  - *correct:* the key figures match the reference (rounding is fine). For an unanswerable question: refuses and gives no substitute figure.
  - *supported:* every claim is in the retrieved passages.
  - Rejected: a 1-5 scale (needs a threshold), and a single pass/fail (mixes the two errors).
- **Partial answers count as incorrect:** an incomplete answer is not what the client asked for.
- **Judge model: `gemini-3.5-flash-lite`,** because of the same quota limit.
  - Risk: it grades its own model's answers.
  - The API ignores temperature 0 for this model, so verdicts are saved and reused.
- **Code checks:**
  - citations valid;
  - refusals (an answer starting "The corpus does not" counts as a refusal);
  - expected page retrieved and cited;
  - a warning for numbers not found in the passages (not counted, because computed figures are flagged too).
- **Refusal wording:** only 1 of 6 refusals uses the exact phrase. Counted as a refusal anyway, because what matters is that no figure is given; the wording is reported separately.
- **Blind grading:** the judge runs only once `eval/human_labels.csv` has 20 grades.
- **Answers and verdicts are saved and reused,** so the human grades and the judge refer to the same answers.
- **Run setup:** 3 questions at a time, with a shared rate limiter (the free tier allows 15 requests a minute).
- **Results:**
  - Human grades: correct 31/32, supported 32/32. The only 0 is q13.
  - Judge: 32/32 on both criteria.
  - Agreement: 97% on correct (kappa 0.00, because almost every grade is 1) and 100% on supported.
- **Planted wrong answers:** to check that the judge can give a 0, Claude wrote 8 wrong answers to real questions, with expected grades set by construction (wrong country, wrong year, growth given as share, a forecast given as an actual value, an invented figure, a right figure plus an invented claim, a missed refusal, a partial answer).
  - The judge gave 0 to every expected 0.
  - Its only difference: t06, where it also marked correct as 0.
  - Real and planted answers together: 95% on correct (kappa 0.84) and 100% on supported (kappa 1.00).
  - Rejected: running the judge 3 times to measure stability (it would likely give all 1s again).

## 13. add_document demo

- **First attempt:** the embedding API returned a temporary 503 and the index stayed unchanged, so the all-or-nothing policy worked.
- **Second attempt:**
  - Before: q32 is refused, with only the Q1 figure (−8%, GEVO2026, p. 11).
  - Adding (approved in the terminal): 44 passages; 322 → 366 passages, 3 → 4 documents.
  - After: "+4% year-on-year (ECMU2026, p. 9)", which is correct.
- **The citation check fired** on the confirmation message: it had numbers and no citation, and the agent's fix cited a page no search had returned, so it was blocked.
  - The first trigger was a false positive, so citations are now required only when a search was made.
  - The 32 evaluation answers are not affected.
- **Retrieval evaluation re-run on 4 documents:** hit rates unchanged.

## 14. Failures and decision

- **Latency,** asked one question at a time (the evaluation's timings include waiting for the rate limiter): median 12.8 s (9.8-17.0 s), with one outlier of 229 s when the API was slow.
- **Cost:** about USD 0.002 per question at paid prices (USD 0.30 / 2.50 per million input / output tokens), plus about USD 0.001 for the judge. The project ran on the free tier.
- **q13, a bad test question caused by inconsistent documents:**
  - the two editions disagree on the UK's 2024 share ("nearly 30%" in GEVO2025, p. 17; "1 in 4" in GEVO2026, pp. 21-22);
  - the agent cited both correctly, but the question does not say which edition to use;
  - fix: name the edition, or accept both figures;
  - rejected: "wrong answer from the right passage".
- **First fix to make (not applied):** an AGENTS.md rule, "If two passages give different figures for the same metric, place and year, say so and give the edition of each." It is not applied because it would invalidate the graded answers.
- **Decision: yes, as an assistant with review.** The consultant opens the cited page before a figure goes into a client report (about 2 minutes instead of 10).
  - Not for figures outside the corpus.
  - Rejected: using it without review (a small test, and contradictory sources), and not shipping yet.
