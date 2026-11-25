# Assignment 3 Report

- **Name**: Marcela Carla Torrelledó Hoyos
- **Student ID**: 19356
- **Group**: BBADBA 5A

## Use case

**Who asks:** the product R&D / regulatory person at a food-supplement brand (my day job) before a new SKU, label or marketing claim is approved for the EU market. Typical questions: *Is this mineral form allowed? Which health claim can I put on the pack and with what wording and dose? What must the label say?*

**What they do with the answer:** they copy the rule (and its article) into the label brief or the claims sheet that goes to design, marketing and the co-packer.

**Cost of a wrong answer vs "I don't know":** a wrong "yes" means a non-compliant label: relabelling a production run, a product withdrawal, or a fine from the national authority, plus reputational damage (claims are the most audited part of a supplement label). "I don't know" only costs an email to the regulatory consultant and a few days. So the system must prefer refusing over guessing, and every answer must point to the exact article so it can be checked.

## Corpus

EU law from EUR-Lex, English HTML, the acts as originally published in the Official Journal. Reuse is allowed under Commission Decision 2011/833/EU (EUR-Lex content: CC BY 4.0). No personal data. The HTML files are committed in `corpus/`.

| Source id | Document | URL | Date | Words |
|---|---|---|---|---|
| Dir 2002/46/EC | Directive on food supplements | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32002L0046 | 10 Jun 2002 | 3,426 |
| Reg 1924/2006 | Nutrition and health claims made on foods | …CELEX:32006R1924 | 20 Dec 2006 | 9,664 |
| Reg 1925/2006 | Addition of vitamins, minerals and other substances to foods | …CELEX:32006R1925 | 20 Dec 2006 | 5,719 |
| Reg 432/2012 | List of permitted health claims | …CELEX:32012R0432 | 16 May 2012 | 16,121 |
| Reg 2015/2283 | Novel foods | …CELEX:32015R2283 | 25 Nov 2015 | 10,648 |
| Reg 1169/2011 | Food information to consumers (labelling) | …CELEX:32011R1169 | 25 Oct 2011 | 23,242 |
| **Total** | 6 documents | | | **68,820** (`index/stats.json`) |

Added later through `add_document`: Commission Regulation (EU) 2022/860 (monacolins from red yeast rice), …CELEX:32022R0860, stored in `corpus/extra/`.

Limitation I accept on purpose: these are the base acts, not the consolidated versions, so amendments are missing unless added (this is exactly what the add-document demo shows).

**Download problems:** EUR-Lex answered the script with a bot-check page instead of the act. `index.py` therefore falls back to the Publications Office Cellar endpoint (`publications.europa.eu/resource/celex/<CELEX>`), and if both fail it tells the user to save the page from a browser. Reg 2022/860 had to be saved from the browser.

## Ingestion

- **Extract:** `index.py` parses the HTML with BeautifulSoup. Paragraphs become lines; **each table row becomes one line** with cells joined by ` | `, so a health claim keeps nutrient, wording and conditions of use together.
- **Clean:** non-breaking spaces and soft hyphens normalised; footnote markers and the footnote list (`(1) OJ L 404, …`) removed.
- **Extraction problem I fixed:** the older HTML of Dir 2002/46/EC nests `<p>` tags that are never closed. Taking the text of each `<p>` therefore returned the whole rest of the document as one line: before the fix, one "line" had **3,477 words**, so all articles and annexes collapsed into one section. The fix (`own_text()`) keeps only the text that belongs to each paragraph itself, which restored one line per paragraph and correct `Article n` / `Annex` tags. Newer acts put each recital in a two-cell table (`(1)` | text), which the row-joining handles.
- **Structure:** a line parser tags every line with its location: `Recital n`, `Article n` (+ article title), `Annex X`, and for the claims table in Reg 432/2012 `Annex (<nutrient>)`; neighbouring claim rows are grouped up to 300 words, so a label can name several nutrients (e.g. `Annex (Linoleic acid; Live yoghurt cultures; Magnesium)`).
- **Chunk metadata:** `source`, `location`, `sections`, `title`, `cite` (= `source, location`, the label the model must cite), `words`, `doc_hash`, `origin` (`corpus` or `added`).
- **Embeddings:** `gemini-embedding-2`, 768 dimensions, one request item per chunk, stored in ChromaDB under `index/chroma`. Chunk ids are a hash of design + source + text, so `main.py index` only embeds chunks without a saved vector, saving after every batch of 40 (the free tier rate-limits after ~80 chunks; the script waits and resumes). Query vectors are cached in `index/query_cache.json`.
- **Number of chunks:** structure = **364**, fixed = **274**.

| Source | structure chunks | fixed chunks |
|---|---|---|
| Dir 2002/46/EC | 26 | 14 |
| Reg 1924/2006 | 52 | 38 |
| Reg 1925/2006 | 34 | 23 |
| Reg 432/2012 | 66 | 65 |
| Reg 2015/2283 | 62 | 42 |
| Reg 1169/2011 | 124 | 92 |

## Test set

39 questions in `eval/questions.csv`: 27 `single`, 6 `multi` (two passages, often from two acts: e.g. the claim wording in Reg 432/2012 plus the label statement required by Reg 1924/2006 Art 10), 6 `unanswerable` (close to the topic: maximum vitamin D dose, CBD, lead limits, a national authority's timeline, FDA rules, and the monacolin limit that only an amendment sets). Each has an expected source and location, checked against the EUR-Lex text.

Examples:
- `q18` single: *How much activated charcoal does a product need to claim it reduces flatulence?* → 1 g per quantified portion, 1 g at least 30 min before and 1 g after the meal (Reg 432/2012, Annex).
- `m02` multi: *Our supplement has 40 mg of vitamin C per daily dose. Is that enough to use the vitamin C immune claim?* → needs "source of" = a significant amount (Reg 1924/2006 Annex), reference value 80 mg (Reg 1169/2011 Annex XIII).

Known issue found while grading, now fixed: my original `m02` reference used "15 % of the reference value" as if it applied per daily dose, but Annex XIII of Reg 1169/2011 applies 15 % per portion only to single-portion packs; otherwise it is per 100 g / 100 ml. I corrected the reference in `eval/questions.csv` (the answer is still "yes": 40 mg in one daily dose is at least 12 mg per 100 g for any dose of 333 g or less) and re-judged m02 against it. The model made exactly the same mistake as my original reference, which shows that a reference answer can carry the error it is supposed to catch.

## Retrieval

Designs compared on the 33 answerable questions (base corpus only). A hit = a top-k chunk from the expected source that covers the expected location; for `multi`, any of the passages, and `all@5` = all of them. `evaluate.py` uses the same rule for both chunkings: a chunk covers the expected location if any section it spans is that `Article n` (or, for the claims table, if the expected nutrient is one of its `Annex (…)` rows); a fixed window spans every section its 300 words touch, so a window that only clips the end of an article still counts, which makes the rule generous to fixed windows rather than biased toward structure chunks.

| Design | hit@1 | hit@3 | hit@5 | all passages@5 | words in prompt (k=5) |
|---|---|---|---|---|---|
| fixed 300-word windows (50 overlap) / vector | 0.61 | 0.79 | 0.91 | 0.76 | 1,492 |
| **structure / vector** | **0.82** | **0.94** | **0.97** | **0.82** | **1,157** |
| structure / BM25 | 0.55 | 0.70 | 0.70 | 0.61 | 1,189 |
| structure / hybrid (RRF) | 0.70 | 0.79 | 0.82 | 0.70 | 1,162 |
| fixed / hybrid (RRF) | 0.55 | 0.76 | 0.85 | 0.76 | 1,492 |

Chosen: **structure / vector, k = 5** (rule: best hit@3, then hit@5, then hit@1, then fewer words; written to `index/config.json`). It is best on every column and also sends ~22 % fewer words to the model than fixed windows. Structure-aware chunks put an article or a group of claim rows into one chunk, so the label the model cites is the real legal location. Keyword search was the weakest: questions are phrased in business words ("reduces tiredness", "how big must it be printed") while the law uses other terms ("x-height", "fatigue"), and adding BM25 through RRF pulled weaker keyword matches above good vector hits.

## Tools and subagent

- `search(query)`: the description in `server.py` tells the model which acts are in the corpus, to use it before answering anything about EU supplement rules, and that each passage starts with a `[source, location]` label to cite.
- `add_document(path)`: indexes a new HTML/PDF/text file; see "Adding a document".
- One search result (query `magnesium reduces tiredness and fatigue health claim conditions of use`, first of 5 passages, shortened):

```
[Reg 432/2012, Annex (Magnesium)]
Reg 432/2012 - Annex, permitted health claims. Columns: nutrient/substance | claim | conditions of use | restrictions/warnings | EFSA ref | entry no.
Magnesium | Magnesium contributes to normal functioning of the nervous system | The claim may be used only for food which is at least a source of magnesium as referred to in the claim SOURCE OF [NAME OF VITAMIN/S] AND/OR [NAME OF MINERAL/S] as listed in the Annex to Regulation (EC) No 1924/2006. | 2009; 7(9):1216 | 242
Magnesium | Magnesium contributes to normal muscle function | … | 2009; 7(9):1216 2010;8(10):1807 | 241, 380, 3083
…
```

- Subagent `.claude/agents/corpus-researcher.md`: only tool `mcp__corpus__search`, at most 4 searches, cite every sentence, refuse with "The corpus does not cover this.".
- Transcript (Claude Code, full export in `subagent_transcript.txt`), prompt: *Use the corpus-researcher subagent: what are the conditions to use the EPA and DHA heart health claim?* Subagent report (shortened):

```
Permitted wording: "EPA and DHA contribute to the normal function of the heart"
[Reg 432/2012, Annex (Docosahexaenoic acid (DHA); Eicosapentaenoic acid and docosahexaenoic acid (EPA/DHA))].
Conditions of use: "The claim may be used only for food which is at least a source of EPA and DHA as
referred to in the claim SOURCE OF OMEGA-3 FATTY ACIDS as listed in the Annex to Regulation (EC)
No 1924/2006. In order to bear the claim information shall be given to the consumer that the beneficial
effect is obtained with a daily intake of 250 mg of EPA and DHA." [same label]
Gaps (not covered by the corpus):
- The EPA/DHA claims on blood pressure and triglycerides (added by a later amendment) did not appear.
- The numeric threshold behind "SOURCE OF OMEGA-3 FATTY ACIDS" was not returned ... must be verified separately.
```

  What I noticed: the subagent stayed inside the corpus and named its gaps. The main Claude Code agent that relayed it then **added facts from its own memory** that no search returned (the 0.3 g ALA / 40 mg EPA+DHA threshold and "Reg. 536/2013"). My citation check runs in `agent.py`, not in the Claude Code relay, so it never saw this answer. If the answer had gone through `agent.py`, the citation check alone would not have stopped it, because it checks the labels that are cited, not sentences without a citation; the number check added in this revision would have flagged numbers such as "0.3 g" that were not in the retrieved passages. The facts the main agent added happen to be correct, but they could not be checked against the corpus, and that is still the failure: an uncited number that sounds authoritative.

## Adding a document

**Already indexed:** `add_document` hashes the file. Same hash already in the index → nothing is embedded, it returns `already_indexed`. Same source name with different content (a new version) → the old chunks of that source are deleted and the new version indexed (`replaced`), so the index never holds two contradicting versions of one act.

Demo (`eval/before_after.json`), question `u01`: *What is the maximum amount of monacolins from red yeast rice allowed per daily portion of a food supplement?*
- **Before** (base corpus): "The corpus does not cover this. The search results do not state a maximum amount of monacolins from red yeast rice, and a regulatory consultant or national authority would need to be consulted for specific limits."
- **Added:** Commission Regulation (EU) 2022/860 (amends Annex III of Reg 1925/2006), 15 chunks. The evaluation script asks the agent to add it and approves that one call automatically; in normal use `agent.py` asks y/N first.
- **After:** "The individual portion of a food supplement for daily consumption must provide **less than 3 mg** of monacolins from red yeast rice [Reg 2022/860, Article 1]."

During the evaluation `CORPUS_ONLY=1` hides added documents, so `u01` stays unanswerable in the scored run.

## Harness and guardrails

- `AGENTS.md` (system prompt): search first, answer only from passages, cite every claim with the exact label, refuse with a fixed sentence when not covered, quote exact wording/numbers, mind the scope (base acts only), no medical advice, add documents only on explicit request. Each rule has its reason in the file.
- **Model:** `gemini-flash-lite-latest` (temperature 0). If Google returns "busy" (503/504) the agent waits 20 s and retries once, then falls back to the next available Flash model; models with no free quota (429) or retired (404) are skipped. So the model can change between questions: in the first run 35 of the 38 answers came from `gemini-flash-lite-latest`, 2 from `gemini-3.5-flash-lite` (q02, q05) and 1 from `gemini-3.6-flash` (m06) (`model` field in `eval/answers.jsonl`); q08 (answered in the final run) and the re-asked q25 both came from `gemini-flash-lite-latest`, so the final count is 36 / 2 / 1 (`answered_by_model` in `eval/summary.json`).
- **Approval:** `HumanInTheLoopMiddleware` interrupts before every `add_document` call; `agent.py` asks y/N in the terminal and rejects when nobody can answer.
- **Limits:** max 4 searches, 1 add_document and 8 model calls per question.
- **Extra guardrail – citation check:** every `[label]` in the answer must be one the search tool returned in that run, and a non-refusal must cite at least once. If not, the model gets one repair turn; if it fails again the answer is replaced by a refusal. Since this revision a paragraph-level label counts as the retrieved article (`Article 11(1)`, `Article 10(2)(a)` or `Article 8, paragraph 2` → `Article 11`, `10`, `8`); the act and the article number must still match, and a label more general than what was retrieved (`Reg 432/2012, Annex` when a nutrient row was retrieved) still triggers the repair. Both cases are tested in `tests/test_guardrails.py`.
- **When it fired (first run, before the change):** 12 of the 38 answers (q05, q18, q22, q24, q25, q26, m01–m05, u01). In 11 the repair turn fixed the citations. Example that worked, q05: the first answer cited `Dir 2002/46/EC, Article 8(1)`, `8(2)`, `8(3)`; after repair it cited `[Dir 2002/46/EC, Article 8]` with the same content. Example where it hurt, q25: the agent cited `Reg 2015/2283, Article 11(1)`, `11(4)`, `17(1)`, `17(4)`; the repair also failed, so a correct answer ("nine months", present in the retrieved Article 11) was replaced by a refusal. The rejected labels of the 12 first drafts (from the `guardrail` column of `eval/results.csv`) fall into four groups:

| Group | Questions | Passes the new rule |
|---|---|---|
| Paragraph of a retrieved article | q05, q25, q26, m03 | yes |
| Paragraph-level, but written as two locations or a range | q22 (`Article 8(1), Article 8(2)(b)`), q24 (`Article 26(1)-2`), m01 (`Article 8, Paragraph 1, and Annex I`) | no |
| Too general: `Reg 432/2012, Annex` when a nutrient row was retrieved | q18, m04, u01 | no, as intended |
| Other formats | m02 (`Annex XIII, Part A`), m05 (`Article 4, Annex II`) | no |

- **Why u01 is in the list:** its first draft cited `[Reg 432/2012, Annex]`, which is too general. The log keeps the guardrail event but not the first draft, so I cannot tell whether that draft answered or refused; after the repair it refused correctly. I therefore do not use it as an example of the guardrail catching a made-up answer.
- **Number check (added in this revision, flag only):** every number with a unit in the answer ("3 mg", "250 mg", "15 %") must appear in the passages retrieved in that run or in the user's question; a table row such as `Vitamin C (mg) | 80` supports "80 mg" only if the answer names vitamin C in the same sentence. Numbers that don't are listed for the reviewer (`unsupported_numbers` in `eval/results.csv`). They do not trigger a repair, because a correct calculation (15 % of 80 mg = 12 mg) is not in the text either and the model should not be pushed to drop it. On the final 39 answers it flags 1: m02 ("12 mg") (`number_check_flagged` in `eval/summary.json`). It only reads digits, so a number written in words, like q25's "nine months", is not checked.

## Evaluation

- **Code checks:** refusal (fixed sentence), has citation, all citations valid, expected source cited, searched at all. Unanswerable questions are graded by code (refusal = correct); refusals on answerable questions are wrong refusals.
- **Judge:** an LLM (Gemini Flash family, same fallback as the agent) with the rubric in `evaluate.py` (`correct` vs reference, `supported` by the retrieved passages, strict on numbers and wording), given the retrieved text as evidence. The judge comes from the same Gemini Flash family as the agent, which is a likely reason for its leniency: it accepts the same small additions the agent makes.
- **Human labels:** I graded **38** answers myself (`eval/human_labels.csv`) without looking at the judge's verdicts. Agreement with the judge on those 38, before the change: **correct 100 % (κ = 1.0)**, **supported 94.7 %, 36 of 38 (κ = 0.0)**. The two disagreements are m02 and u02: I marked them unsupported, the judge marked them supported. Kappa for "supported" is 0 even with 94.7 % agreement because the judge gave "supported" to every answer, so it never varies; the raw agreement hides that the judge cannot catch the unsupported details I found.
- **Why the counts differ (37, 38, 39):** in the first run the agent answered 38 of the 39 questions (q08 failed on every model because Google was busy; q02 was only answered in a second run, by a fallback model) and the judge graded 37 of them (it hit its daily quota on q02). I graded all 38 answers that existed then, and the AI audit covered the 37 judged ones. The final run answered q08 and judged all 39; the agreement figures use the 38 questions that have both a judge verdict and my grade (q08 has no grade of mine).
- **Extra AI audit:** as a third opinion, Claude also checked every answer against its reference and passages (`eval/ai_audit.csv`, labelled as AI). It agreed with the first-run judge on correct 37/37 and on supported 36/37 (difference: m02). It is not used as human labels.
- **Results (final run before the citation-check change, all 39 questions graded):**

| | Judge + code checks | My grades |
|---|---|---|
| Answerable: correct | 32 / 33 (97 %) | 31 / 32 (97 %; q08 not graded by me) |
| Answerable: unsupported claims | 0 | 1 (m02) |
| Answerable: wrong refusals | 1 (q25) | 1 (q25) |
| Unanswerable: correct refusals | 6 / 6 (100 %), made-up answers 0 | 6 / 6 (100 %) |
| Unanswerable: refusal with an unsupported statement | 0 | 1 (u02) |
| Cost per question | 7,008 tokens on average; 19.0 s on average (max 184 s, caused by retries when the model was busy) | |

  The samples are small, so the intervals are wide: the 95 % Wilson interval is 84.7–99.5 % for 32 / 33, 84.3–99.4 % for my 31 / 32, and 61.0–100 % for 6 / 6 (computed with `wilson()` in `evaluate.py`, saved as `wilson_95` in `eval/summary.json`).

- **After the change (q25 re-asked with the new check, m02 re-judged against the fixed reference; `eval/summary.json`):**

| | Judge + code checks | My grades |
|---|---|---|
| Answerable: correct | 33 / 33 (100 %; Wilson 89.6–100 %) | 32 / 32 (100 %; Wilson 89.3–100 %; q08 not graded by me) |
| Answerable: unsupported claims | 0 | 1 (m02) |
| Answerable: wrong refusals | 0 | 0 |
| Unanswerable: correct refusals | 6 / 6 (100 %; Wilson 61.0–100 %) | 6 / 6 (100 %) |
| Unanswerable: refusal with an unsupported statement | 0 | 1 (u02) |
| Answers replaced by a refusal | 0 | |
| Cost per question | 7,004 tokens on average; 19.5 s on average (max 184 s) | |

  q25 now answers "nine months" [Reg 2015/2283, Article 11] and adds the six-month deadline for traditional foods from third countries [Article 17]; I regraded it correct 1, supported 1. Its first draft still needed the repair turn, because it cited `Article 11, Article 17` as one label, a two-location format the new rule still rejects; the repair produced valid labels, so nothing was replaced by a refusal. The other 11 answers in the repair list (`citation_repair_turns`) are cached from the first run and were not re-asked. Agreement with the judge on my 38 grades: correct 100 % (the script prints κ = 1.0, but now the judge and I mark every answer correct, so there is no variation and κ says nothing), supported 94.7 % (36 / 38, κ = 0.0), with the same two disagreements, m02 and u02. The judge re-checked m02 against the corrected reference and still marked it correct and supported.

## Failures

Automatic classification (`eval/failures.csv`): 1 failure, `wrong refusal` (q25) (before the change; 0 after).

Cases from my own grading:

| Question | What happened | My grade |
|---|---|---|
| q25 | Retrieved the right passage (Art 11, "nine months") but cited paragraph labels (`Article 11(1)`); citation check turned it into a refusal | correct 0, supported 1 |
| m02 | Right conclusion, but states the 15 %-per-portion rule without its single-portion condition | correct 1, supported 0 |
| u02 | Correct refusal, but adds "not adopted yet", which the passages do not say | correct 1, supported 0 |

After the citation-check change, q25 is answered correctly ("nine months") and I regraded it correct 1, supported 1; m02 and u02 are unchanged.

**What the failures tell me.** None of them is a retrieval problem: in all three cases the right passage was in the top 5. q25 is a harness problem, not a model problem. The model read Article 11 correctly but cited it at paragraph level (`Article 11(1)`), and my citation check only knew article-level labels, so it threw away a correct answer. m02 and u02 are the opposite risk: the model is mostly right but adds a small detail that is not in the text (dropping the "single portion" condition, saying limits are "not adopted yet"). The LLM judge marked both as supported and I did not, so the judge is too lenient on exactly the kind of small unsupported detail that matters on a label.

For a supplement brand the m02 type is the dangerous one. A wrong refusal costs me an email to the regulatory consultant. A confident "yes, 15 % per portion is enough" that is not exactly what the law says can end up on a claims sheet and then on a production run. So the first thing to fix is not the refusal in q25 but making sure unsupported details are caught; q25 is the easy fix.

## Decision

**I keep the system as it is (structure-aware chunks, vector search, k = 5) and change two things:**

1. **Done: the citation check accepts paragraph numbers.** `Article 11(1)` now counts as a match for the retrieved `Article 11`, because the chunk holds the whole article. The check stays strict on the act and the article, so a citation to something that was never retrieved is still blocked. Replayed on the logged first drafts of the first run, 4 of the 12 repair turns (q05, q25, q26, m03) would not have been needed; the other 8 still are (see the table in "Harness and guardrails"). Result: q25 is now answered correctly and nothing is replaced by a refusal (answerable correct 33 / 33 by the judge, 32 / 32 by my grades). To be honest about why: q25 did not pass because of the paragraph rule, since its new first draft used a two-location label and went through the repair turn, which worked this time. The rule removes the paragraph-label repairs (4 of the 12 in the first run); measuring its full effect would mean re-asking all 12 questions, which I did not do, to save quota and keep my grades valid for the answers I graded.
2. **Do not trust the LLM judge alone on "supported"; add the number check.** The judge agreed with me on what was correct but missed the two unsupported details I found. For anything going on a real label, a person still reads the cited article before it is used. The concrete addition to that human review is the number check: it lists every number that is not in the retrieved passages, so the reviewer knows where to look first. On the final 39 answers it flags only m02 ("12 mg", a correct calculation that the law does not state). It would not catch wording-only additions like u02's "not adopted yet" or m02's missing single-portion condition, so the person reading the article is still needed. The tool is good at finding the right article fast (hit@5 = 0.97); the final check stays human.

Biggest remaining risk: the corpus is the base acts, but my use case needs the current law.** The first question in my use case, *is this mineral form allowed?*, is answered from Dir 2002/46/EC Annex II as published in 2002, but that annex and the claims list in Reg 432/2012 have been amended since, and the novel-food Union list (Implementing Reg 2017/2470) is not in the corpus at all. So an answer can be out of date in either direction: "not listed" for something added later, or "allowed" for something changed later. The fix is to index the consolidated versions from EUR-Lex instead of the base acts, or to add the amending acts and Reg 2017/2470 with `add_document` (the before/after demo shows that path works). I have not downloaded them yet.

**Trade-off:** a looser citation check means a model could cite the right article but the wrong paragraph and still pass; I accept that because the whole article is in front of the reviewer anyway. Keeping a human check costs time, but at ~7,000 tokens and ~20 s per question the system still turns a search through 69,000 words of EU law into a one-minute review, which is where the value is.

## Limitations

- Base acts only: later amendments (e.g. Reg 536/2013 adding EPA/DHA blood-pressure and triglyceride claims, Reg 116/2010 adding the omega-3 nutrition claims) are not in the corpus unless added with `add_document`.
- Free-tier Gemini limits: Google "busy" errors and daily quotas made runs slow and forced fallback between Flash models, so not every answer comes from the same model.

## AI use

I used Claude (Anthropic) to help me write and optimize some parts of the code (index, server, agent), then I used it to make sure the grammar and structure of the report was correct. I also used it to cross check the factual parts of this report (numbers copied from the evaluation outputs), and for an extra AI audit of the answers (`eval/ai_audit.csv`, clearly marked as AI). The rest of things such as use case, corpus choice, the test set, my grades in `human_labels.csv`, the failure analysis and the decision are mine.
