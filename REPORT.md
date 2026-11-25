# Assignment 3 Report

- **Name**: Leopoldo Sirolli
- **Student ID**: ✍️
- **Group**: BBADBA 5A ✍️ (check)

> Lines marked ✍️ are for you to write in your own words (the brief requires the analysis and decisions to be yours). The bullets under them are the evidence from the runs. Delete this note and the ✍️ markers before submitting.

## Use case

✍️ *Who asks, what they do with the answer, and what a wrong answer costs compared with "I don't know".*

Evidence to use:
- Asker: an analyst or associate on an M&A deal team (bank or law firm) at the start of a transaction, before external counsel is briefed.
- What they do with the answer: decide whether the deal needs an EU notification, how long clearance could take, whether they can close before clearance, and which competition questions the Commission is likely to ask.
- Cost of a wrong answer: a missed or late notification, or closing before clearance (gun-jumping), can be fined up to 10% of aggregate turnover (EUMR Article 14(2)); a wrong timetable misprices the deal. "I don't know" only costs a lookup or a call to counsel. So a confident wrong answer is far worse than a refusal.

## Corpus

| Document (id in metadata) | URL | Date | Licence | Words |
|---|---|---|---|---|
| Council Regulation (EC) No 139/2004, EU Merger Regulation (`EUMR`) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32004R0139 | 20 Jan 2004 | EUR-Lex, reuse authorised (Commission Decision 2011/833/EU) | 14,575 |
| Commission Consolidated Jurisdictional Notice (`JURISDICTIONAL_NOTICE`) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52008XC0416(08) | 16 Apr 2008 | same | 24,649 |
| Guidelines on the assessment of horizontal mergers (`HORIZONTAL_GUIDELINES`) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52004XC0205(02) | 5 Feb 2004 | same | 8,602 |
| Guidelines on the assessment of non-horizontal mergers (`NONHORIZONTAL_GUIDELINES`) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52008XC1018(03) | 18 Oct 2008 | same | 9,265 |
| **Total** | | | | **57,091** |

Added later through `add_document`: Commission Notice on a simplified treatment for certain concentrations (`SIMPLIFIED_NOTICE`), https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52023XC0505(01), 5 May 2023, same licence, 20 chunks.

All are official EU legal texts with no personal data. The texts are fetched from the Publications Office (Cellar) endpoint, because EUR-Lex answers scripts with an empty anti-bot page (HTTP 202, 0 bytes).

## Ingestion

- **Extract:** EUR-Lex XHTML parsed with BeautifulSoup (PDF and text also supported for `add_document`). Footnote reference tags and footnote blocks are removed before text extraction; two-cell table rows (`(a)` | text) are joined into one line.
- **Clean:** whitespace normalised, page furniture and footnote lines dropped.
- **Structure:** each document is cut into units: `Recital N` and `Article N` (with the article title) in the Regulation, numbered `para N` in the notices and guidelines, each with the nearest section heading. Paragraph numbers must run in sequence (n+1), so list items are not mistaken for paragraphs.
- **Extraction problems fixed:**
  1. Footnote numbers glued to words ("Commission(1)", "undertakings(4)"): stripped only when the bracket follows a letter, so legal references like "Article 4(1)" survive.
  2. The Horizontal Guidelines end with their footnote list as plain text: "para 91" swallowed ~80 footnotes (2,332 words) and footnotes 92 to 97 became fake paragraphs. Fix: numbering restarting at "(1)" after the real paragraphs marks the footnote list and ends parsing. Para 91 dropped to 239 words, the document to 8,602 words.
- **Chunk metadata:** `source` (document id), `location` (e.g. `Article 7`, `paras 124-126`, `Article 4 (part 2)`), `units` (every article/recital/paragraph the chunk covers), `section`, `added` (true for documents added later).
- **Chunks:** 286 (fixed design) and 266 (structure design); 552 vectors, `gemini-embedding-2` at 768 dimensions, index/ 17 MB. Every vector is appended to `index/vectors.jsonl` as it arrives, keyed by a hash of the text, so re-runs only embed new or changed chunks.
- **Cost note:** the binding free-tier limit was 30,000 embedding tokens per minute, not 1,000 texts per day; batches of 50 structure chunks never fit in one minute, batches of 20 do.

## Test set

✍️ *How you wrote it (one or two sentences).*

- 34 questions: **22 single**, **6 multi** (two passages), **6 unanswerable**.
- Spread over all four documents; several phrased as a deal team would ask, without the legal keyword (e.g. q09, q11, q17, q19, q20).
- Unanswerable questions sit next to the corpus: Italian national thresholds, the Foreign Subsidies Regulation, Form CO contents, filing fees, the post-Illumina Article 22 policy, and the simplified procedure (q29, used for the before/after test).

Two examples:

| id | kind | question | expected | reference answer |
|---|---|---|---|---|
| q11 | single | We are forming a JV just to build a wind farm, which it will hand over once it is built. Is that a notifiable concentration? | JURISDICTIONAL_NOTICE, para 104 | No, a JV set up for a short finite project such as building a plant does not operate on a lasting basis. |
| q24 | multi | If we close a notifiable deal before Commission clearance, what is our legal exposure? | EUMR, Article 7 ; Article 14 | Closing early breaches the standstill obligation, which can be fined up to 10% of aggregate turnover. |

## Retrieval

Hit = every expected passage is in the top k (answerable questions only, n = 28). Words = average words of the top 5 chunks added to the prompt.

| Design | hit@1 | hit@3 | hit@5 | words@5 |
|---|---|---|---|---|
| A. Fixed 250-word windows, 50 overlap | **0.46** | 0.68 | 0.82 | 1,247 |
| B. Structure: article/paragraph units, packed to ~300 words, section header embedded | 0.39 | **0.79** | **0.86** | **1,162** |
| C. B + BM25 keyword search, fused with reciprocal rank fusion | 0.32 | 0.64 | 0.71 | 1,206 |

![retrieval](eval/retrieval.png)

✍️ *The design you chose and why (your decision).* Evidence: the agent receives k = 5, where B is best (0.86); B is clearly best at k = 3 (0.79 vs 0.68); fewest prompt words; chunks follow legal units so citations point at one provision. A wins only at k = 1, which the agent never uses. C lowers every number: legal vocabulary ("concentration", "undertakings", "turnover") repeats across almost every passage, so keyword overlap pulls in passages that share words but not meaning. Served design: B, without hybrid (`index/config.json`).

## Tools and subagent

**`search(query)`**: description the model reads:
> Search the EU merger control corpus: the EU Merger Regulation (Regulation 139/2004), the Commission Consolidated Jurisdictional Notice, and the horizontal and non-horizontal merger assessment guidelines, plus any document added later. Use it for any question about EU merger control: what counts as a concentration, control and joint ventures, turnover thresholds and how turnover is calculated, notification, deadlines and procedure, referrals, and how the Commission assesses competitive effects. Write the query in plain English with the key legal terms. Call it again with a different query if the first results do not cover the question. Returns the 5 most relevant passages, each with its source document id and location (article, recital or paragraph) and a ready-made citation such as [EUMR, Article 1].

**`add_document(path)`**:
> Add one document (.html, .pdf, .txt or .md file on this machine) to the corpus index. The file goes through the same pipeline as the corpus: text extraction, cleaning, chunking by article/paragraph, Gemini embedding, storage in index/. The document id is the file name in capitals (e.g. simplified_notice.html -> SIMPLIFIED_NOTICE). If the same file is already indexed, nothing is embedded or changed. If a file with the same id but different content is added, it replaces the old version. Returns the status (added, replaced or already_indexed), the document id and the number of chunks stored.

One search result (from `check.py`, query = q01):
```
[1] source: EUMR | location: Article 1
cite as: [EUMR, Article 1]
1. Without prejudice to Article 4(5) and Article 22, this Regulation shall apply to all concentrations with a Community dimension as defined in this Article.
2. A concentration has a Community dimension where:
(a) the combined aggregate worldwide turnover of all the undertakings concerned is more than EUR 5000 million; and ...
```

**Subagent** (`.claude/agents/corpus-researcher.md`, tool: `mcp__corpus__search` only):
> Search with the key legal terms of the question. If the results do not cover every part, search again with different wording (at most 4 searches). Answer in at most 6 sentences, using only what the returned passages say. Do not use your own knowledge of EU law. Put a citation after every claim exactly as the result labels it. Quote thresholds, amounts and deadlines exactly. If the passages do not answer the question, reply `The corpus does not cover this question.` and, in one line, what the closest passages were about.

✍️ **Transcript from your editor** (paste here: ask the corpus-researcher subagent one question in VS Code Copilot or Claude Code and copy the conversation).

## Adding a document

- **Already indexed:** same document id and same file hash: nothing is embedded or changed, returns `already_indexed`. Same id, different content: treated as a new version, old chunks removed, new ones stored (`replaced`). ✍️ *One line on why you chose this behaviour.*
- **Unanswerable question q29:** "Our deal is a joint venture with no activities in the EEA. Does it qualify for the simplified procedure and a short-form CO filing?"
- **Document added:** Commission Notice on a simplified treatment for certain concentrations (2023), 20 chunks.
- **Before:** "The corpus does not cover this question (it does not contain the rules on the simplified procedure or the short-form CO filing). The search results only cover the jurisdictional concepts of joint ventures, joint control, and full-functionality under the Jurisdictional Notice."
- **After:** "Yes, a joint venture with no activities in the EEA qualifies for the simplified procedure [SIMPLIFIED_NOTICE, para 5(a)]. ... provided that the joint venture has no current or expected turnover within the territory of the EEA, and the undertakings concerned have not planned to transfer any assets within the EEA to the joint venture at the time of notification [SIMPLIFIED_NOTICE, para 5(a)]. Eligible concentrations of this type are notified by completing the relevant sections of the Short Form CO [SIMPLIFIED_NOTICE, para 26]."

The evaluation keeps the test set reproducible: added documents are excluded when answering the 34 questions (`CORPUS_EXCLUDE_ADDED=1`), so q29 stays unanswerable there.

## Harness and guardrails

**AGENTS.md rules** (system prompt), each with its reason in the file: search before every answer; answer only from search results; cite every claim as `[SOURCE, location]`; refuse with the exact sentence `The corpus does not cover this question.`; answer the covered part of partial questions; quote thresholds and deadlines exactly; be short, no legal advice; call `add_document` only when the user asks. ✍️ *Review and own these; edit any you would decide differently.*

**Approval step:** `add_document` is wrapped: before it runs, the harness prints the path and asks `Approve? [y/N]`; anything but "y" returns "Not run: the user did not approve" to the model. With no terminal (evaluation, check.py) it is refused unless `AGENT_AUTO_APPROVE=1`.

**Call limits:** at most 6 tool calls and 8 model calls per question (LangChain `ToolCallLimitMiddleware`, `ModelCallLimitMiddleware`).

**Extra guardrail, citation check:** every `[SOURCE, location]` in the answer must point at a passage the search tool returned in this run, and an answer that is not a refusal must cite something. On failure, the model gets one rewrite with the list of bad citations; if it fails again, the answer is replaced by the refusal.

**A case where it fired (check.py run):** the agent wrote `[EUMR, Article 1; JURISDICTIONAL_NOTICE, para 125]`, two sources in one bracket. The guardrail rejected it, the model rewrote it as separate valid citations, and the final answer passed.

✍️ *What you learned from it:* in the first evaluation run the checker was too strict: it read "paras 92, 104" as the range 92 to 104 and required co-cited paragraphs to sit in the same chunk. It fired on 7 answers; 6 were fixed on retry, but on q28 it threw away a correct answer (a wrong refusal caused by the guardrail itself). Fixed by parsing lists and ranges and accepting a paragraph covered by any returned passage; q28 was re-answered.

## Evaluation

**Code checks** (`eval/results.csv`): refusal (answer opens with the refusal sentence), number of citations, citation validity against the passages returned in that run, correct refusal on unanswerable, wrong refusal on answerable, whether the agent's own searches retrieved the expected passage, guardrail events.

**Judge:** `gemini-3.1-flash-lite` (all 34 answers; a different model from the agent, `gemini-3.5-flash-lite`, to avoid grading its own style), temperature 0, JSON output, given the question, reference answer, question type, retrieved passages and answer. Rubric (`eval/rubric.md`): **correct** = same key facts as the reference (wording free, extra true detail fine; multi needs every part; unanswerable needs a refusal with no substantive answer); **supported** = every claim is in the retrieved passages, judged against the passages, not the judge's own knowledge.

**Results** (34 questions):

| | count |
|---|---|
| Answerable: correct and supported | **27 / 28** |
| Unsupported answers | 0 |
| Wrong refusals | 0 |
| Unanswerable: correct refusals | **6 / 6** |
| Answered an unanswerable question | 0 |
| Answers with a citation the code check rejects | 3 (q06, q08, q27, format only: two sources in one bracket, or sub-paragraphs cited as "Article 9, paras 1-2") |

**Agreement with my labels** (34 graded, `eval/human_labels.csv`):

| | agreement | Cohen's kappa |
|---|---|---|
| correct | 0.88 (30/34) | -0.05 |
| supported | 1.00 (34/34) | 1.00 |

✍️ *Interpret the agreement.* Evidence: disagreements on q09, q27, q31, q34. Kappa is near zero despite 88% agreement because almost every label is 1 for both, so agreement by chance is already ~88%; kappa only counts agreement beyond chance, and the 4 disagreements go in both directions.
- q09: judge said correct, I said wrong. The answer opens "No, you do not have sole control" and then calls it negative sole control, which *is* sole control: the opening contradicts the passage it cites.
- q27: judge said incorrect (less concise than the reference), I said correct: it covered both mechanisms and the 15-day deadlines.
- q31, q34: judge said incorrect because the refusal added one line on what the corpus does cover; that line is allowed by AGENTS.md rule 4, so I graded them correct.

## Failures

✍️ *Failed questions by cause, with counts, and what to fix first.* Evidence (`eval/failures.csv`, plus your grades):

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 0 | (but retrieval alone hit@5 = 0.86: 4 of 28 questions lacked an expected passage in the top 5 of a single search; the agent recovered by searching again) |
| Wrong answer from the right passage | 1 to 2 | q09 (you: right passage para 54, contradictory conclusion); q27 per judge |
| Unsupported claim | 0 | |
| Wrong refusal | 0 in the final run | (q28 in the first run, caused by the over-strict guardrail, fixed) |
| Bad test question | ✍️ | e.g. is q27's reference too short for a two-part question? |

Also: 3 answers with malformed citations (format, not fabrication).

What to fix first (your call): e.g. q09-type errors are the dangerous ones, a confident yes/no that contradicts the cited passage; a rule requiring the answer to state the conclusion in the passage's own terms, or a second check of yes/no answers, targets that.

## Decision

✍️ *Would you let users rely on it, for what, with which safeguard?* Evidence:
- 27/28 correct and supported, 6/6 correct refusals, 0 unsupported claims, every citation checkable.
- The one serious error (q09) was a wrong yes/no conclusion with a correct citation, and the LLM judge missed it: only the human caught it.
- Small test set (34), one model run, free-tier models.

**Cost and latency per question:** about 6,700 input and 330 output tokens; 8.1 s on average (max 22 s); about 1 to 3 searches. Embedding the corpus once: 552 chunks. ✍️ (optional: price at paid-tier rates)

## AI use

✍️ Check and complete. Draft:
- Claude (Anthropic) wrote most of the code (index.py, retrieval.py, server.py, agent.py, evaluate.py), the first drafts of AGENTS.md, the judge rubric and the subagent instructions, and generated the question worksheet (passage text per location) from the parsed corpus. I reviewed and adopted these.
- My decisions: use case and corpus, the questions and reference answers, the chunking design choice, the behaviour for re-added documents, my 34 grades, the analysis and the ship decision. ✍️ (Also mention any other AI tool you used, e.g. to draft the test questions.)
- Models used at run time: `gemini-embedding-2` (embeddings), `gemini-3.5-flash-lite` (agent), `gemini-3.1-flash-lite` (judge).
