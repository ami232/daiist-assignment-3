# Assignment 3 Report

- **Matias Arevalo**:
- **19319**:
- **Group**: [BBADBA 5A]

## Use case

**Who asks:** an airline safety analyst who prepares case-study briefings for recurrent pilot training (CRM and flight-path management modules).

**What they do with the answer:** say the training team is building a session on how crews notice and respond to decaying airspeed. The analyst asks, *"What did the NTSB find about airspeed monitoring in Colgan 3407 and Asiana 214, and what did it recommend after each?"* The assistant gathers the findings, probable causes and recommendations from the reports and cites the PDF page of each claim. The analyst checks each citation and picks which lessons go onto the training slides.

**What a wrong answer costs compared with "I don't know":** a wrong answer is costly because it can end up in training material that many pilots see, and from there it is hard to correct. The errors that matter most:
- **Category errors.** Calling a contributing factor the probable cause, or the other way round. In Colgan 3407, failing to monitor airspeed was a *contributing factor*; in Asiana 214, inadequate airspeed monitoring was *part of the probable cause*.
- **Status errors.** Presenting an NTSB *recommendation* as an FAA *requirement*.
- **Changed numbers.** Altered altitudes, speeds or recommendation numbers.

"I don't know" costs only time: the analyst checks the report or another source, such as the NTSB recommendation-status records or FAA rulemaking. So the assistant must cite every claim and say plainly when the reports do not cover a question. That includes anything that happened after a report was published, which these reports cannot contain.

> This tool helps airline safety analysts prepare case-study briefings for recurrent pilot training. Analysts use it to compare findings, probable causes and safety recommendations across NTSB accident reports, and to check each claim against the original page. An unsupported answer could carry an error into training materials, so the assistant says when the reports do not contain enough evidence to answer.

**Out of scope:** what happened after a report was published (recommendation status, FAA rules, airline actions), accidents not in the corpus, and operational advice to pilots.

## Corpus

Three full NTSB aircraft accident reports. All three accidents involve airspeed or energy management, crew monitoring and emergency handling, so they support comparisons. US government works are in the public domain (17 U.S.C. §105), and the reports contain no personal data beyond the crews' professional histories, which the reports publish. `index.py` downloads them into `corpus/` (git-ignored).

| Document | Accident | URL | Date | Licence | PDF pages | Words indexed |
|---|---|---|---|---|---|---|
| NTSB/AAR-10/01 (AAR1001) | Colgan Air 3407, loss of control on approach, Buffalo, 12 Feb 2009 | https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR1001.pdf | 2 Feb 2010 | Public domain | 299 | 85,798 |
| NTSB/AAR-10/03 (AAR1003) | US Airways 1549, dual bird strike and Hudson River ditching, 15 Jan 2009 | https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR1003.pdf | 4 May 2010 | Public domain | 213 | 58,447 |
| NTSB/AAR-14/01 (AAR1401) | Asiana 214, descent below glidepath into the seawall, San Francisco, 6 Jul 2013 | https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR1401.pdf | 24 Jun 2014 | Public domain | 207 | 77,593 |
| **Total** | | | | | **719** | **221,838** (about 261,000 before removing the contents and abbreviation pages) |

## Ingestion

- **Extract:** `pypdf`, one page at a time, so every chunk knows its PDF page.
- **Extraction problem fixed:** pypdf's default mode splits words in these PDFs, for example "th eir", "adequa te", "tim e" and "go -around". A keyword check for "go-around" on the Asiana findings page failed for that reason. Switching to `extraction_mode="layout"` keeps the words whole.
- **Clean:**
  - Remove the running header "NTSB Aircraft Accident Report" and the page-number lines, keeping the printed number as metadata, since PDF page 165 is printed page 151.
  - Rejoin words hyphenated across lines.
  - Fix ligatures.
  - Drop front matter: table-of-contents pages (detected by dot leaders), lists of figures and the abbreviation lists, about 31 pages in all.
- **Chunk (two designs, both about 350 words):**
  - **`fixed`:** sliding windows of 350 words with a 50-word overlap, ignoring the report's structure.
  - **`sections`:** detects the NTSB's numbered headings ("1.1 History of Flight", "3.1 Findings", "4.1 New Recommendations") and never crosses one. Whole paragraphs are packed up to 350 words, and a longer paragraph is split at sentence ends. Each chunk is embedded with a header line, "report title | section", so a passage from *3.2 Probable Cause* carries that label into its vector.
- **Metadata per chunk:** `doc_id`, `section`, `page_start`, `page_end` (PDF pages), `printed_start`, `printed_end`, `title`, `words`, `design`.
- **Embedding:** `gemini-embedding-2`, 768 dimensions, normalised, stored in ChromaDB (`index/chroma`, cosine). The chunk id is a hash of the embedded text, and each batch of 20 is stored as soon as it returns, so a re-run embeds only what is missing.
- **Two pitfalls handled:**
  - Passing a plain list of strings to `gemini-embedding-2` returns *one* vector for the whole list, so each text is sent as its own `Content`.
  - The free tier's daily limit made us index over two days.
- **Chunk counts:** 885 (`sections`) and 740 (`fixed`) for the three reports.

## Test set

- **37 questions:** 24 single, 7 multi (two reports or two passages), 6 unanswerable.
- **How they were written:** from reading the reports, mainly the findings, probable-cause and recommendation sections, which are what an analyst briefs from, with 4 from the executive summary and factual body. Each answerable question has its PDF page, checked against the extracted text.
- **The unanswerable questions** stay on topic. They ask what happened *after* a report was published (recommendation closure dates, FAA rules, airline training costs), or about an accident that is not in the corpus (Atlas Air 3591).
- **Two questions test the errors named in the use case:**
  - q31, probable cause vs contributing factor.
  - q35, which asks for an FAA rule when the report contains only an NTSB recommendation.

Examples:
- *q31 (multi):* "Was the crew's airspeed monitoring part of the probable cause or only a contributing factor in Colgan 3407, and in Asiana 214?" → AAR1001 p.169 (contributing factor) and AAR1401 p.147 (part of the probable cause).
- *q27 (unanswerable):* "On what date did the NTSB close recommendation A-10-66…?" The report states the recommendation but not its later status, so the assistant should say the reports do not cover it.

## Retrieval

Measured on the 31 answerable questions, base corpus only (`evaluate.py`, step 1). A hit means the chunk covers the expected PDF page; for a *multi* question, every expected page must be in the top k.

| Design | Chunks | hit@1 | hit@3 | hit@5 | Passage recall@5 | Words added to the prompt (top 5) |
|---|---|---|---|---|---|---|
| `fixed` (350 words, 50 overlap) | 740 | 0.13 | 0.23 | 0.26 | 0.29 | 1,750 |
| `fixed` + hybrid (BM25 + dense, RRF) | 740 | 0.13 | 0.29 | 0.39 | 0.40 | 1,750 |
| **`sections`** | 885 | **0.23** | **0.39** | **0.52** | **0.53** | **1,319** |
| `sections` + hybrid | 885 | 0.23 | 0.39 | 0.48 | 0.52 | 1,391 |

**Chosen design: `sections`, dense only.** It doubles hit@5 over fixed windows and puts 25% fewer words into the prompt. Two reasons: a chunk never mixes two sections, so a findings chunk is about findings only; and the "report title | section" header in each embedded text lets a query like "Asiana probable cause" match the *3.2 Probable Cause* chunk. Hybrid search helps the fixed windows (exact terms like "A-10-10" rescue some misses) but slightly hurts sections, so it is not used.

**Why the absolute numbers look low:** most misses are not irrelevant passages. Each answerable question has one expected page, usually in the report's *Findings* (chapter 3), but the same fact is argued at length in the *Analysis* (chapter 2), and the search often returns that page instead. For q03 (stick-pusher), for example, the top 5 are all from *2.2.3 Response to Stick Shaker*, pp. 100–103, which contain the answer; the expected page is the finding on p. 166. The end-to-end results below (29/31 answerable correct) show these passages are enough to answer. A fairer retrieval test would list every page that supports the answer; we kept the single page written before tuning.

## Tools and subagent

`server.py` is an MCP server (stdio) with two tools. Their descriptions are what the model reads to decide when to call them, so they say what the corpus holds, when to use the tool and what the result looks like.

- **`search(query)`:** "Search NTSB aircraft accident reports and return the 5 most relevant passages. The corpus holds full NTSB accident reports: Colgan Air 3407 (AAR1001…), US Airways 1549 (AAR1003…) and Asiana 214 (AAR1401…), plus any report added later with add_document. … Search once per sub-question (for a comparison, search each accident separately) and use specific terms (flight number, system, recommendation number like A-10-10). Returns numbered passages, each headed by a citation such as `[AAR1001 p.165 (printed 151) | 3.1 Findings]` … If no passage addresses the question, the corpus does not cover it."
- **`add_document(path)`:** "Add one PDF report to the searchable corpus (it changes the index; ask the user first). … If the same file (same SHA-256) is already indexed, nothing is done and no embedding quota is spent. If a document with the same id but different content exists, it is treated as a new version: its old chunks are removed and replaced."

One search result (top passage for *"Atlas Air 3591 probable cause"*):

```
[AAR2002 p.76]
(Atlas Air Inc. Flight 3591 | section 3.2 Probable Cause | printed page 60)
The NTSB determines that the probable cause of this accident was the inappropriate response by
the first officer as the pilot flying to an inadvertent activation of the go-around mode, ...
```

The first line is the tag the agent must copy into its answer. The second line gives the analyst the section and the printed page, because the printed page differs from the PDF page by 14–17.

**Subagent:** `.claude/agents/corpus-researcher.md`, with access to `mcp__corpus__search` only (it cannot add documents). Its instructions repeat the core rules: split the question and search each accident separately, answer only from the passages, cite every sentence, keep the NTSB's categories, refuse plainly when not covered.

**Transcript from the editor** (Claude Code; full text in `eval/editor_transcript.md`): asked *"How did the NTSB characterize the role of crew fatigue in Colgan Air Flight 3407 and Asiana Airlines Flight 214? … cite the PDF pages"*, the subagent ran four searches, one per accident and kind of information ("Colgan Air 3407 crew fatigue findings", "Asiana 214 flight crew fatigue", "Asiana 214 probable cause contributing factors fatigue", "Colgan Air 3407 probable cause contributing to the accident"). It answered that for Colgan fatigue "likely impaired" the pilots but its extent "cannot be conclusively determined" (Finding 24) `[AAR1001 p.166-167]` and is not among the contributing factors `[AAR1001 p.169]`, while for Asiana "flight crew fatigue" is contributing factor (5) `[AAR1401 p.18]`. It kept the categories apart, and labelled a Board Member Statement arguing fatigue was a factor as "one member's opinion, not an NTSB finding" `[AAR1001 p.176]`, which is AGENTS.md rule 3 working. The main agent, given the similar test question q22, ran two broader searches, missed Finding 24 and wrongly said fatigue was not in Colgan's findings: the subagent's extra, narrower searches are what found it.

## Adding a document

**Unanswerable question before:** q26, *"What did the NTSB determine was the probable cause of Atlas Air Flight 3591's crash?"* With the three base reports the right answer is a refusal.

**Document added:** NTSB/AAR-20/02 (AAR2002), Atlas Air 3591, Trinity Bay, Texas, 23 Feb 2019, https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR2002.pdf, public domain. 141 pages, 168 `sections` chunks. Only the chosen design is embedded for new documents, so adding a report costs about 170 embeddings.

**What happened** (full log in `eval/add_document_demo.txt`, produced by `eval/add_document_demo.py`):
1. *Run 1:* the user asks the agent to add `corpus/AAR2002.pdf`. The agent calls `add_document`. The approval step asks "Approve? [y/N]", answered "y" (scripted in the demo, because it runs without a terminal; with `main.py ask` a person types it). Result: *"Added AAR2002: new. 168 chunks (168 embedded now, 0 already stored, 0 old chunks removed). It is now searchable."*
2. *Run 2, same file again:* *"Already indexed: AAR2002 (141 pages, 168 chunks) with identical content. Nothing changed, no embeddings used."* The registry (`index/documents.json`) stores each file's SHA-256, so an identical file is recognised before any embedding call. A file with the same name but different content replaces the old chunks (they are pruned by id), and a run cut off by the quota is resumed, because chunks are stored per batch and only missing ids are embedded.

**Answer before and after** (`eval/before_after.json`; "before" restricts search to the three base reports with `RAG_DOCS`):
- *Before:* "The reports in the corpus do not cover Atlas Air Flight 3591. The searchable corpus currently holds accident reports for Colgan Air 3407 (AAR1001), US Airways 1549 (AAR1003), and Asiana 214 (AAR1401)."
- *After:* "The NTSB determined that the probable cause of the Atlas Air Flight 3591 accident was the inappropriate response by the first officer (as the pilot flying) to an inadvertent activation of the go-around mode, which led to his spatial disorientation and nose-down control inputs … `[AAR2002 p.76]`", followed by the three contributing factors, correctly labelled as contributing factors.

## Harness and guardrails

`agent.py` uses LangChain's `create_agent` on Gemini (`gemini-3.5-flash`, falling back to `gemini-3.5-flash-lite` and `gemini-3.1-flash-lite` when the free tier answers 503 "high demand"). It connects to `server.py` over MCP and uses `AGENTS.md` as its system prompt.

**AGENTS.md rules** (each with its reason in the file):
1. Search before answering, and answer only from the passages.
2. Search narrowly: one search per accident and per kind of information.
3. Attribute every statement to its author: only Findings, Probable Cause and Recommendations are NTSB conclusions; Board Member Statements and appendix "Comments of …" sections are not.
4. Cite every factual sentence with the exact tag.
5. Keep the NTSB's categories (probable cause / contributing factor / finding).
6. A recommendation is not a requirement.
7. Quote numbers, recommendation ids and times exactly.
8. If not covered, say "The reports in the corpus do not cover this." and answer only the covered part.
9. Never call `add_document` unless the user asked.
10. Be brief (about 200 words).

Rules 2 and 3 were added after a failure (see *Failures*): an early answer presented the Korean investigation board's comments as an NTSB recommendation.

**Approval:** `add_document` runs only after a person types "y" at the terminal. Without a terminal (evaluation, CI) it is denied and the agent is told the document was not added.

**Limits:** at most 6 tool calls and 8 model calls per question (LangChain middleware), one retry with backoff, then the fallback models.

**Extra guardrail, citation check:** after the agent answers, the code parses every `[DOC p.N]` tag and checks that the page falls inside a passage a `search` call in this run actually returned, and that a non-refusal cites at least once. If not, the agent gets one repair turn with the list of problems; if it still fails, the answer is withheld and replaced by a notice telling the analyst to check the report directly. This targets the costliest error in the use case: a claim with a page number that was never read.

*Where it fired:* on q04 (recommendation A-10-17) the first draft stated the recommendation without a tag. The check returned "the answer makes claims but cites no passage", and the repaired answer ended with `[AAR1001 p.171]`, a page the search had returned. It fired twice in the final run (q04 and q29), and both were repaired.

*Where it misfired, and the fix:* in the first evaluation run the check *withheld* the correct refusal for q26 ("The reports in the corpus do not cover Atlas Air Flight 3591 …"). The refusal detector required the exact sentence "…do not cover this", so a refusal that named the missing item looked like an uncited claim. That run also scored only 1/6 correct refusals for the same reason. The detector now matches the stem "the reports in the corpus do not cover", and the final run has 6/6 correct refusals. The lesson: a guardrail that matches exact wording breaks as soon as the model follows the rule that allows it to explain what is missing.

## Evaluation

`main.py evaluate` runs retrieval, then the agent on all 37 questions (base corpus, approval denied), then code checks, the LLM judge and agreement with the human labels. Answers and verdicts are cached in `eval/answers.jsonl` and `eval/judge.jsonl`; results are in `eval/results.csv` and `eval/summary.json`.

**Models:** answers from `gemini-3.5-flash-lite`, judge `gemini-3.1-flash-lite`, so the judge never grades its own model's output. We first used `gemini-3.5-flash` for both, but the free tier allows it 20 requests a day, which ran out mid-run (about 3 model calls per question) and left the judge stuck on retries. The agent's fallback chain had already answered 31 of 37 questions with the lite model, so we made that the default and re-asked the other 6 with it, so all 37 answers come from one model.

**Code checks** (no model needed): every cited page lies in a retrieved passage; the expected page was retrieved and cited (±1 page); unanswerable questions are refused and answerable ones are not.

**Judge rubric** (structured output, temperature 0): `correct` (key facts of the reference, no factual error; a category error or a recommendation presented as a requirement counts as wrong; an unanswerable question needs a clear refusal), `supported` (every claim appears in the retrieved passages), and a failure category (`retrieval_miss`, `wrong_from_right_passage`, `unsupported_claim`, `wrong_refusal`, `bad_question`). The judge sees the passages the agent retrieved, so "supported" is checked against what the agent actually read.

**Results (37 questions):**

| Measure | Result |
|---|---|
| Correct (judge) | **35/37** (29/31 answerable, 6/6 unanswerable) |
| Supported | judge 36/37; our grades 24/30 (see agreement below) |
| Correct refusals (code) | 6/6 |
| Wrong refusals (code) | 1 (q23, partial: it refused the Flight 1549 half) |
| Citations valid (code) | 37/37 |
| Expected page retrieved and cited (code) | 12/31, see *Retrieval* for why this is low |
| Citation check fired | 2 (both repaired) |

**Agreement with the judge** (30 answers graded by hand before reading the verdicts, `eval/human_labels.csv`):

| Field | Agreement | Cohen's κ | Disagreements |
|---|---|---|---|
| correct | 29/30 (0.97) | 0.65 | q11: the judge was wrong (see *Failures*) |
| supported | 24/30 (0.80) | −0.06 | q03, q05, q06, q18, q22 (human 0, judge 1); q30 (human 1, judge 0) |

The judge is reliable on *correct* but not on *supported*: its κ is no better than chance. It passed five answers that we found unsupported, and four of those were wrong details rather than missing context: two invented recommendation numbers (q05 cites "A-10-10", q06 "A-10-16"; neither id appears in any retrieved passage, which we checked in the saved trace), a callout credited to the wrong pilot (q18: the passage says the pilot monitoring said "it's low"), and a stick-pusher claim cited to a page about the stick shaker (q03). The judge reads for the gist and checks the overall claim, not each id, name and page, which is exactly where the use case's costliest errors sit. **By our grades, 24 of 30 answers are fully supported, not the judge's 36 of 37**, and the judge's "supported" score should not be reported on its own.

## Failures

By the judge, three questions failed in the final run; our own grading found five more unsupported answers (see *Evaluation*). Two failures were found and fixed during development.

| Question | Cause | What happened |
|---|---|---|
| q23 (multi) | wrong refusal (partial) | Asked how starting the APU on Flight 1549 preserved flight-envelope protection, and what autothrottle wakeup might have done for Asiana 214. The agent said the corpus does not cover the Flight 1549 part, although the retrieved passage (AAR1003 p.19) says the APU gives an extra electrical source; it did not connect that to normal law. It refused rather than guess, which is the cheaper error. |
| q30 (unanswerable) | unsupported claim | The refusal was correct, but the agent added a count of earlier dual-engine bird strikes ("108 … between 1990 and 2008", per the judge) that was not in the passages it retrieved. A number from memory is the error the use case fears most. |
| q05, q06 (single) | unsupported claim: invented id | The answers are right in substance but name a recommendation id that is in none of the retrieved passages ("A-10-10", "A-10-16"). Both passed the citation check, because the page cited was retrieved; only the id was invented. The judge missed both. |
| q18 (single) | unsupported claim: wrong attribution | Credits the "it's low" callout to the pilot flying; the retrieved passage (AAR1401 p.27) says the pilot monitoring. |
| q03, q22 | unsupported claim: wrong page / overstated | q03 cites a stick-shaker page for a stick-pusher conclusion; q22 states fatigue was not in Colgan's findings without having retrieved the findings. |
| q11 (single) | judge error / bad question | The judge marked it wrong, saying A-10-66 was addressed to manufacturers. The report (AAR1003 p.141) lists A-10-66 among the recommendations *to the FAA*: "Require manufacturers of turbine-powered aircraft to develop a checklist…". The agent's answer is right; our question ("did the NTSB ask aircraft manufacturers…") misled the judge. |
| (development) Asiana recommendations | misattribution | An early answer cited AAR1401 p.207, the Korean investigation board's comments, as an NTSB recommendation. Those pages and the Board Member Statements had been labelled with the previous section heading. Fixed by detecting "Board Member Statement" and "Comments of the …" as headings (51 chunks re-embedded) and adding AGENTS.md rules 2 and 3. |
| (development) q26 refusal | guardrail misfire | The citation check withheld a correct refusal (see *Harness and guardrails*). Fixed in the refusal detector. |

**By cause (judge plus our grades, 37 answers):** 6 unsupported claims (q03, q05, q06, q18, q22, q30; three of them a wrong id, name or number), 1 wrong refusal (q23), 1 judge error (q11); no retrieval miss changed whether an answer was correct.

**What to fix first:** invented ids and numbers (q05, q06, q30). Add a code check that every recommendation id (A-NN-NN), time and number in an answer appears in a retrieved passage, and route a failing answer to the same repair turn as the citation check. It is cheap, needs no model, and targets the "changed numbers" error in the use case. Second: give each answerable question all its supporting pages (Findings *and* Analysis) so the retrieval numbers measure what matters. Smaller: in AAR2002, numbered findings ("2. There was insufficient information…") are detected as section headings, so some chunks carry a wrong section label; the heading pattern should require a short title line.

## Decision

**Yes, as a first-draft research assistant, not as a source.** An analyst can use it to find and draft what the reports say about a cause, finding or recommendation, because every claim comes with a page the code has checked was actually retrieved, and it refused all six out-of-corpus questions. They should not paste its answers into training material unchecked: by our own grading, 6 of 30 answers contained an unsupported detail, including two invented recommendation numbers that our citation check and the LLM judge both missed.

**Safeguards:** the analyst opens every cited page before a claim goes onto a slide (the citation check makes this possible, it does not replace it); `add_document` needs explicit approval; the id-and-number check above must be added before wider use, since recommendation ids are what the analyst would copy onto a slide.

**Cost and latency per question** (final run, mean of 37): 9,674 input and 211 output tokens, 1.6 tool calls, 16.3 s, plus one query embedding per search. The index cost about 1,800 embeddings for both designs of the three reports (885 + 740 chunks plus re-embeds after fixes) and 168 for Atlas Air. Everything ran on the Gemini free tier, so the money cost was zero; the binding limits were the daily quotas (about 1,000 embeddings, and 20 requests a day for `gemini-3.5-flash`), which is why indexing was spread over two days and the lite model answers.

## AI use

### AI use disclosure

I used Claude Code (Claude Opus) to write most of the implementation in `index.py`, `server.py`, `agent.py`, and `evaluate.py`, configure the Claude Code subagent, and run the indexing and automated evaluation. It also helped draft `AGENTS.md`, the LLM judge rubric, and an early version of this report. I used ChatGPT to draft evaluation questions, which the professor confirmed was allowed.

I made the main project decisions, including the choice of use case and corpus, the final retrieval design, and how the tool should be used. I manually graded 30 agent answers and wrote most of the final report, including my interpretation of the results, the failure analysis, and the recommendation on when to rely on the tool.
