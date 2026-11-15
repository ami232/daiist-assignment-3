# Next session: context and to-do

Working notes for finishing Assignment 3. Not part of the submission: delete this file before opening the PR.

## Where things stand (15 Nov 2026)

**Built and working**
- Corpus: AI Act, GDPR, DSA (EU Publications Office XHTML) in `corpus/`, committed. Plus `corpus/ePrivacy_Directive.html` (consolidated 2009 version) for the add-document demo, **not yet in the index**.
- Index: 900 chunks (recitals, articles, annexes; max 600 words; citation header), `gemini-embedding-2`, 768 dims, ChromaDB in `index/` (17 MB). Never rebuilt: `main.py index` embeds only missing chunks.
- Search: `vector` chosen over `hybrid` (hit@5 96.6% vs 75.9%). `DEFAULT_MODE` in `index.py`.
- `server.py`: `search(query, k=5)`, `add_document(path)` (identical file → "Already indexed", changed → replaced, new → added). Returns a clear message when the embedding quota is used up.
- `agent.py`: `gemini-3.5-flash-lite`, AGENTS.md as system prompt, approval before add_document (y/N in a terminal), 6 tool / 8 model calls, citation check guardrail.
- `evaluate.py`: done. Results in `eval/` (summary.json, results.csv, failures.csv, answers, verdicts). Re-running reuses saved answers and verdicts (no tokens).
- Your 35 human labels: done. Agreement with the judge: correct 82.9% (kappa 0.30), supported 71.4% (kappa 0.00).
- `check.py` passes.

**Free-tier limits hit (explain in the report)**
- Embeddings: 1,000/day (`gemini-embedding-2`), reset 09:00 Spain. Every new search query costs one.
- Chat: `gemini-3.5-flash` and `gemini-3-flash-preview` allow only 20 requests/day; `gemini-2.5-flash` retired; `gemini-3.8-flash` timed out. Agent therefore on `gemini-3.5-flash-lite`; judge was `gemini-3-flash-preview` (16) + `gemini-3.1-flash-lite` (19).

## To do

**After 09:00 (needs the API):**
1. In Claude Code: `/mcp` → reconnect `corpus` (the running server is an old copy of server.py), or start a new session.
2. Subagent transcript: ask Claude to "run the corpus-researcher subagent on Haiku: we're building a customer-support chatbot, do we have to tell users they're talking to an AI?" Paste the transcript into REPORT.md (Tools and subagent). The failed run from 15 Nov can stay as a note.
3. Add-document demo, in your own terminal (type `y` at the approval prompt):
   ```bash
   uv run python main.py ask "Please add the document corpus/ePrivacy_Directive.html to the corpus"    # y → 22 chunks added
   uv run python main.py ask "Do we need user consent before setting analytics cookies on our website?"  # after: should cite ePrivacy Directive, Article 5
   uv run python main.py ask "Please add the document corpus/ePrivacy_Directive.html to the corpus"    # y → Already indexed
   ```
   Paste the outputs into REPORT.md (Adding a document). "Before" is already captured (u06 in eval/answers_for_grading.md and the 15 Nov demo run).

**No API needed:**
4. Classify the failures: fill the `cause` column of `eval/failures.csv` (retrieval miss / wrong answer from right passage / unsupported claim / wrong refusal / bad test question). Evidence in the appendix, section 10.
5. Finish REPORT.md: header (name, ID, group), the ✍️ sections, Use case typos ("usually legal team" → "usually no legal team").
6. Restore the template file: `git checkout -- .env.example`.
7. Final checks and submit:
   ```bash
   uv run python check.py --evaluate
   ```
   Delete this file, commit, push, open the PR to ami232/daiist-assignment-3, put the link on Blackboard, upload a zip.

---

# Appendix: report notes

Facts, numbers and reasoning to draft from. Write the prose in your own words.
✍️ YOU = the brief requires this to be your own analysis or decision.
Sources for every number: `eval/summary.json`, `eval/results.csv`, `eval/retrieval_results.csv`, `eval/failures.csv`.

---

## 0. Header
- Name, Student ID, Group: ✍️ YOU (still empty in REPORT.md).

---

## 1. Use case (already written by you)
- Small fixes: line 9 "there is usually legal team" → probably "usually **no** legal team"; typos "coprotations", "qunatified", "understanidng", "wrong no"" (missing opening quote).
- Fines you cite: AI Act Art 99 (7% / EUR 35M, prohibited practices; 3% / EUR 15M for other obligations such as high-risk), GDPR Art 83 (4% / EUR 20M), DSA Art 52 & 74 (6%). All are in the corpus.

---

## 2. Corpus (table already filled)
- 3 regulations, ~209,600 words raw. After cleaning, the words in chunks: AI Act 89,021 · GDPR 54,608 · DSA 62,757 = **206,386**. You could add a "words after cleaning" note.
- Source: EU Publications Office **CELLAR** API (official back end of EUR-Lex), XHTML, English, Official Journal versions.
  - Why not EUR-Lex directly: it blocks scripted downloads (bot check, HTTP 202 with empty body).
  - Why XHTML, not PDF: every recital, article and annex has its own HTML anchor (`rct_32`, `art_7`, `anx_III`), so the structure comes for free and citations are exact. PDFs would need guessing article boundaries from text.
- Licence: © European Union, reuse with attribution, Commission Decision 2011/833/EU. Legislation has no personal data.
- `corpus/` is committed (licence allows it), so the grader never needs to download, and the index never changes because of a re-download.
- Assumption / limitation: texts **as adopted** (GDPR 2016, DSA 2022, AI Act 2024). No later amendments, no Commission guidelines, no enforcement decisions, and no **ePrivacy Directive** (the cookie rule), which the add-document demo adds.

---

## 3. Ingestion
**Extract** (`index.py: parse_eurlex`)
- One unit per recital, article and annex: 509 recitals, 305 articles, 13 annexes (AI Act only) = **827 units**.
- Preamble citations ("Having regard to…"), signatures and footnote bodies are left out.

**Extraction problems fixed** (the brief asks for one; you have two):
1. **Footnote markers inside sentences.** The XHTML puts "(1)", "(2)"… inline, e.g. *"…the European Economic and Social Committee (1),"*. They are removed so they don't pollute embeddings or citations.
2. **List markers split from their text.** Points like "(a)", "1." sit in their own table cell, so plain text extraction gives "(a)" on one line and the text on the next. `clean_lines()` merges them back: "(a) the relevant design choices;".
3. (Found later, for the added document) Consolidated texts contain amendment markers (`▼B`, `►M2 … ◄`), which are also removed.

**Clean**
- Whitespace normalised. Recital numbers "(32)" and article headings moved out of the text into metadata.

**Chunk** (design decision: structure-based)
- One chunk per recital, article or annex. A unit longer than **600 words** is split at **paragraph boundaries** (never mid-sentence unless one paragraph alone is longer than 600 words).
- Every chunk starts with a citation header, e.g. `GDPR, Article 7 — Conditions for consent` or `AI Act, Annex III — High-risk AI systems… (part 2 of 4)`, so the embedding knows what the text is.
- Result: **900 chunks** (60 of the 827 units were split), avg **229 words**, max 625.

| | Recital chunks | Article chunks | Annex chunks |
|---|---|---|---|
| AI Act | 181 | 144 | 21 |
| GDPR | 173 | 117 | – |
| DSA | 156 | 108 | – |

**Why 600 words** (✍️ YOU decided; reasoning from our discussion):
- Free tier: 1,000 embeddings per day. 350 words gave 1,055 chunks (doesn't fit in one day); 450 gave 962 (too tight once questions are embedded); 600 gave 900 (fits, leaves ~100 for queries).
- The average only rises from 197 to 229 words, because most recitals and articles are short anyway.

**Why keep recitals** (✍️ YOU decided):
- They are not binding, but often hold the practical answer. Example: GDPR Recital 32, "pre-ticked boxes… should not constitute consent"; Article 7 never mentions pre-ticked boxes.
- 3 of your questions are answered by recitals (s01 Recital 32, s22 Recital 12, s23 Recital 47).
- Tagged `type: recital`, and AGENTS.md rule 5 tells the agent to say when a point comes only from a recital.

**Metadata per chunk:** `source` (AI Act / GDPR / DSA), `location` (Article 7 / Recital 32 / Annex III), `type` (article / recital / annex), `title` (article heading), `part` / `parts`, `file`.

**Embed and store**
- `gemini-embedding-2`, **768 dimensions** (smaller than default to keep `index/` small: **17 MB**, limit 90 MB). ChromaDB, cosine distance.
- Retrieval prefixes: documents `title: … | text: …`, queries `task: search result | query: …`.
- Saved every 50 chunks, so a crash or the quota loses nothing.
- **Never rebuilt:** a chunk counts as indexed if its citation (law + location + part) is already stored. Re-running `main.py index` embeds 0 chunks. Query vectors are cached in `index/query_cache.json`.

---

## 4. Test set
- 35 questions: **23 single, 6 multi, 6 unanswerable** (the brief requires ≥ 30, ≥ 5 multi, ≥ 5 unanswerable).
- Coverage: GDPR 9 single, AI Act 8 single, DSA 6 single. All 6 multi questions combine two laws (5× AI Act + GDPR, 1× DSA + GDPR).
- Written before tuning anything, from the documents, in founder language ("our signup form", "our CV-screening tool").
- Unanswerable questions are close to the topic: Spanish AESIA enforcement (u01), DSA fines actually imposed (u02), Commission AI-system guidelines (u03), EU-US Data Privacy Framework (u04), later amendments (u05), cookie consent (u06).
- Possible examples to quote: s01 (pre-ticked boxes → GDPR Recital 32), m01 (CV screening: AI Act Art 12 logging + GDPR Art 22 automated decisions), u06 (cookies).
- ✍️ YOU: how you wrote them, and which two examples you show.

---

## 5. Retrieval
Two designs over the **same** vectors (so no extra embeddings; the quota made re-chunking for a second design cost a second day):
- **vector**: cosine similarity on the embeddings, top k.
- **hybrid**: vector top 30 + BM25 keyword top 30, merged by reciprocal rank fusion (score = Σ 1/(60 + rank)).

Hit rate = share of the 29 answerable questions where a chunk with the expected `source` + `location` is in the top k (multi: any expected passage counts; "all@5" = every expected passage).

| Design | hit@1 | hit@3 | hit@5 | all expected @5 | words added @5 |
|---|---|---|---|---|---|
| **vector** | **62.1** | **96.6** | **96.6** | **82.8** | 1,376 |
| hybrid | 37.9 | 55.2 | 75.9 | 62.1 | 1,491 |

- Chosen: **vector** (`DEFAULT_MODE` in index.py). ✍️ YOU: the decision in your words.
- Why hybrid loses (evidence): questions use everyday words ("employees stressed", "cancel a subscription"), the law uses legal terms. BM25 matches common words and its ranking pulls the right passages down when fused. BM25 alone found the expected passage in the top 5 for only 34%.
- Only vector miss: **s08** (emotion recognition at work). It finds AI Act Recital 44 (which explains this ban) but not Article 5. Article 5 is long (4 chunks) and lists many prohibitions, so its vectors are spread across topics.
- hit@3 = hit@5, so k = 3 would cut prompt size by about 40% without losing hits on this test set (a possible improvement to mention).
- Limitation: hit rate only counts *your* labelled passage; another passage that also answers it counts as a miss.

---

## 6. Tools and subagent
**search(query, k=5)** description (from `server.py`, paste in full): what the corpus is, when to use it, "Cite as" format, articles/annexes binding vs recitals explanatory, no later amendments or enforcement.

**add_document(path)** description: EUR-Lex HTML (recitals/articles/annexes), PDF (by page), .txt/.md; same pipeline as the corpus (imports `index.chunk_file` and `index.embed_and_store`, not rewritten).

One search result (from `check.py`):
```
[1] Cite as: GDPR, Recital 32 | type: recital
Consent should be given by a clear affirmative act establishing a freely given, specific,
informed and unambiguous indication of the data subject's agreement…
```

Subagent `.claude/agents/corpus-researcher.md`:
- Tool: `mcp__corpus__search` only.
- Instructions: search (and re-search with other wording), answer only from passages, cite `(GDPR, Article 7)`, articles vs recitals, exact refusal phrase, ≤ 200 words.
- ✍️ YOU: one transcript from Claude Code, still to do.

---

## 7. Adding a document
**Duplicate rule** (✍️ YOU decided):
- Same file, identical content → "Already indexed … Nothing added" (no embeddings spent).
- Same file name, different content → new chunks embedded, old ones removed ("Replaced").
- New file → added. Chunk IDs come from the exact text, which is how identical content is detected.

**Document chosen:** ePrivacy Directive 2002/58/EC, **consolidated version** (19.12.2009).
- Why: the GDPR defines what valid consent is, but the obligation to ask for it before storing cookies comes from **ePrivacy Article 5(3)**. Every startup website hits this question.
- Why consolidated: in the original 2002 text Article 5(3) only gave users a **right to refuse**. Consent came with the 2009 amendment (Directive 2009/136/EC). The original would give an outdated answer.
- 22 chunks, cited as `ePrivacy Directive, Article 5`. Needed two code changes: the parser reads consolidated EUR-Lex format, and the citation check accepts sources added later.

**Question:** u06, "Do we need user consent before setting analytics cookies on our website?"

**Before** (already captured):
- In the evaluation it answered "generally yes" from GDPR Recital 30, which is wrong reasoning (judge and you both scored 0/0).
- In the demo run it said "does not cover this fully", then answered from GDPR consent rules (Recitals 32, 40, Article 7). It cannot state Article 5(3).

**Approval** (already captured):
- No terminal → `add_document … refused: no terminal to ask for approval`; index unchanged (900 chunks).
- With your `y` → the tool ran, but hit the daily embedding quota; the server now returns a clear "Not added: quota… run again after 09:00" instead of a traceback.

**After** and **duplicate**: tomorrow after 09:00 (3 commands). Paste outputs.

---

## 8. Harness and guardrails
- LangChain `create_agent` on **gemini-3.5-flash-lite**, MCP tools loaded from `server.py`, `AGENTS.md` as system prompt.
- AGENTS.md: 7 rules, each with its reason (search first; only from results; cite every claim; exact refusal phrase; articles vs recitals; point to a lawyer; version caveat). ✍️ YOU: reword the reasons in your voice if you haven't.
- **Approval:** a middleware wraps every tool call; `add_document` only runs if a human types `y`. No terminal = no.
- **Call limits:** 6 tool calls and 8 model calls per question.
- **Extra guardrail, citation check** (✍️ YOU chose it): after the model answers, code checks that every "(Law, Article N)" cited was actually returned by search in this run, and that a non-refusal answer cites at least one passage. Otherwise the answer is withheld and replaced by a refusal.
- **One case where it fired: u04** (EU-US Data Privacy Framework). The draft was a refusal, but it cited **GDPR Article 46**, which search had not returned (from the model's memory). The check caught it; the shown answer was the safe refusal.
- Approval also fired in the demo (no terminal → refused).

---

## 9. Evaluation
**Code checks** (no LLM): refusal detected by the exact phrase; citations must be in retrieved passages; expected passage retrieved / cited; guardrail fired.

**Judge:** LLM with a rubric, shown the question, reference answer, assistant answer and all retrieved passages. Returns `correct` (0/1), `supported` (0/1) and a reason.
- Rubric (✍️ YOU approved): correct = same conclusion + all key points of the reference (strict: missing one = 0; refusing an answerable = 0; refusing an unanswerable = 1). Supported = every claim about the law is in the retrieved passages, each citation points to a passage that says it; judged only against the passages; a pure refusal = 1.
- Judge models: **gemini-3-flash-preview (16 answers) + gemini-3.1-flash-lite (19)**. Different from the agent's model so it doesn't grade itself. Mixed because 3-flash-preview's free tier allows 20 requests/day. Limitation to state.

**Results (35 questions):**
| | |
|---|---|
| Correct (judge) | **82.9%** (29/35); answerable 82.8% |
| Unsupported (judge) | **5** answers, 16.7% of non-refusals |
| Correct refusals | **5/6** (u06 answered instead) |
| Wrong refusals | **0/29** |
| Expected passage retrieved / cited | 100% / 100% |
| Citation check fired | 1 (u04) |

**Your grades vs the judge (35 graded):**
| | Agreement | Kappa | You 1 / judge 0 | You 0 / judge 1 |
|---|---|---|---|---|
| correct | 82.9% | 0.30 | 4 (s09, s11, s13, s15) | 2 (m01, m03) |
| supported | 71.4% | **0.00** | 4 (s03, s06, s07, s09) | 6 (s08, s16, m01, m03, m04, m06) |

- By kind: unanswerable 100% / 100%; single 82.6% / 73.9%; **multi 66.7% / 33.3%**.
- Your own totals: correct 31/35, supported 28/35. You found **7 unsupported**, the judge found 5, and they overlap in only **1** (u06).
- Why kappa is low: almost every answer is 1, so chance agreement is high; kappa removes it.
- Reading (✍️ YOU): judge reliable for refusals, partly for correctness, not for support, especially when a claim combines two laws.

---

## 10. Failures
Failed by the judge (9, in `eval/failures.csv`): s03, s06, s07, s09, s11, s13, s15, s16, u06.
Failed by you (7 with a 0): s08, s16, m01, m03, m04, m06, u06.
Categories: retrieval miss · wrong answer from the right passage · unsupported claim · wrong refusal · bad test question.
✍️ YOU classify. Evidence per case:

| id | Expected passage retrieved? | Judge reason / your note (short) |
|---|---|---|
| s03 | yes | judge: "risk depends on encryption" not in passages; you: fine |
| s06 | yes | judge: mentions US surveillance laws, supplementary measures, not in passages |
| s07 | yes | judge: says "only one exception" but Art 50(1) also has a law-enforcement exception |
| s08 | expected Art 5 **not in top 5** (retrieval miss in retrieval eval) | you: fatigue monitoring presented as a medical/safety exception; Recital 18 says fatigue is outside the definition |
| s09 | yes | judge: omits Art 6(3) exceptions + claims not in passages |
| s11 | yes | judge: missed Feb 2025 / Aug 2025 deadlines |
| s13 | yes | judge: missed SME participation in standardisation |
| s15 | yes | judge: missed disclosure of automated means |
| s16 | yes | both: missed the Art 25(2) GDPR/consumer-law carve-out; you: overstates Art 25(3) |
| m01 | yes (one of two) | you: applies Art 12(3) fields that only apply to biometric identification; mislabels Annex III points |
| m03 | yes | you: fails to conclude a FRIA is needed for credit scoring (Art 27(1)) |
| m04 | **GDPR Art 9 not retrieved** | you: religion/health → Art 9 claim not backed by a retrieved passage |
| m06 | yes | you: "separate regulators" not in passages; ignores Art 99(7)(c) |
| u06 | n/a | both: should refuse (cookie rule is ePrivacy 5(3), not in corpus); answered from GDPR Recital 30 |

Patterns worth noting:
- Retrieval is rarely the problem (100% of answers retrieved an expected passage). Most failures are **generation**: missing key points from a passage it had, or adding claims from memory.
- Multi questions (combining two laws) fail more on support.
- "What to fix first" (✍️ YOU): e.g. a stricter "list every condition and exception" rule, extending the citation check to flag uncited sentences, retrieving per law for multi questions, k = 3 vs 5…

---

## 11. Decision
✍️ YOU: would you let users rely on it, for what, with which safeguard.
Facts for it:
- 82.9% correct, 0 wrong refusals, 5/6 correct refusals, but 7 of 35 answers had unsupported claims by your grading, and the judge can't detect them reliably (kappa 0).
- The cost of a wrong answer in your use case is a fine on turnover (your Use case section).
- Safeguards available: citations on every claim (user can check the official text), citation check, refusal phrase, "ask a lawyer" rule.

**Cost per question** (agent, gemini-3.5-flash-lite):
- **5,667 tokens** on average (min 3,552, max 13,002), **4.3 s** (min 2.0, max 8.6), **1.2 searches**.
- Search adds ~1,376 words of passages per search (k = 5).
- Judge: ~3,386 tokens per verdict (evaluation only).
- Embeddings: 1 per new question (cached after). Index: 900 one-time.

**Operating limits found** (free tier, Nov 2026):
- Embeddings: 1,000/day. The index used ~90% of one day.
- Chat: gemini-3.5-flash and gemini-3-flash-preview allow only **20 requests/day**; gemini-2.5-flash retired for new users; gemini-3.8-flash timed out. That is why the agent runs on a lite model.
- A real deployment would need a paid tier.

---

## 12. AI use
✍️ YOU, but the facts:
- Claude Code (Anthropic) used for the code: index.py, server.py, agent.py, evaluate.py, the subagent file, the AGENTS.md draft, debugging (quotas, model changes), and these notes.
- Yours: use case, corpus choice, keeping recitals, chunk size, the vector/hybrid choice, the citation-check guardrail, AGENTS.md rules, the duplicate rule, the rubric, the 35 questions, your 35 grades, the failure classification and the decision.
