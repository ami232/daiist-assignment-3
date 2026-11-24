# Assignment 3 Report

- **Name**: Eduardo Alfaro
- **Student ID**: 19911
- **Group**: BBADBA 5B

## Use case

**Who asks:** an equity or credit analyst (or a finance student) covering U.S. automakers, who needs figures and management statements from the FY2025 annual reports of Tesla, Ford and GM: segments, workforce, market share, risks, 2025 results, tariff costs, EV strategy, outlook.

**What they do with the answer:** put the figures into a valuation model, a comparison table or a client note.

**Cost of a wrong answer vs. "I don't know":** a wrong figure is silent. It looks exactly like a right one, carries a citation, and goes straight into a model or a client note, where it can change a valuation, a comparison between companies or a recommendation before anyone notices. The most dangerous errors are not invented numbers but mislabelled ones: a gross cost presented as a net impact (Ford's tariffs: about $3 billion gross, about $2 billion net EBIT impact), a 2026 outlook presented as a 2026 result, an adjusted figure compared with a GAAP one, or millions read as billions. "The reports do not cover this" costs only a few minutes: the analyst opens the original filing or looks for another source. So the assistant must prefer refusing to guessing, and every figure must be checkable in seconds.

## Corpus

Form 10-K annual reports for fiscal year 2025, from SEC EDGAR. Only Item 1 (Business), Item 1A (Risk Factors) and Item 7 (MD&A) are indexed.

| Document | Company | Filed | URL | Licence | Words (Items 1, 1A, 7) |
|---|---|---|---|---|---|
| `tesla_10k_fy2025` | Tesla, Inc. | 2026-01-29 | https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm | Public SEC filing (EDGAR content is public information and may be copied and redistributed) | 27,236 |
| `ford_10k_fy2025` | Ford Motor Company | 2026-02-11 | https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm | Public SEC filing | 47,965 |
| `gm_10k_fy2025` | General Motors Company | 2026-01-27 | https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm | Public SEC filing | 30,231 |
| **Total** | | | | | **105,432** |

No personal data beyond the names of executives acting in their public roles. Three companies from the same sector (electric and traditional automakers) make cross-company comparisons natural, which is where the two-passage questions come from.

**Why only Items 1, 1A and 7:** they hold what the analyst asks about: the business and its segments (Item 1), the risks management declares (Item 1A) and the explanation of the year's results, costs and outlook (Item 7, MD&A). The full reports are about 230,000 words, much of it financial statement tables, notes, exhibits and legal text. With the free embedding quota (about 1,000 texts a day) the full filings would have taken several days to embed, while these three Items still give more than twice the required 50,000 words.

**Licence:** SEC filings are public records; sec.gov states that its information is public and may be copied and redistributed. The raw files are downloaded into `corpus/` (git-ignored) by `index.py`.

## Ingestion

Pipeline (`index.py`), one function per step: `download_filing` → `html_to_lines` → `clean_lines` → `find_items` → `chunk_file` / `chunk_item` → `embed_and_store`.

- **Extract:** BeautifulSoup over the EDGAR inline-XBRL HTML; the hidden XBRL header is removed; one line per leaf block (paragraph) and one line per table row, cells joined with ` | `.
- **Clean:** drop page furniture ("Table of Contents", running headers such as "Item 7. ... (Continued)", "GENERAL MOTORS COMPANY AND SUBSIDIARIES", page numbers); normalise quotes and dashes; re-join paragraphs split by a page break and bullets split from their text. Page numbers are used to give every line its printed page before they are dropped.
- **Locate Items:** the table of contents repeats every heading, so each Item is the occurrence followed by the most text before the next Item heading.
- **Chunk (structure-based):** one section (sub-heading) at a time, at most 250 words per chunk; a section under 50 words is merged with the next; an over-long paragraph is split at sentence ends, then at semicolons. Each chunk text starts with a context header, e.g. `Ford 10-K FY2025 | Item 7. Management's Discussion and Analysis ... | Revenue`.
- **Extraction problems fixed:**
  1. Tables came out one cell per line (`$`, `13,145`, `617`, ...) and were unreadable; now one row per line: `Crossovers | 13,145 | 617 | 64.8%`.
  2. GM puts section headings in bold at the start of the paragraph ("Overview Our vision is ..."), so GM had only 14 sections; bold lead-ins are now split off as headings (63 sections).
  3. One GM risk factor was a single 706-word sentence (a list joined by semicolons) and became an oversized chunk; it is now split at semicolons.
- **Chunk metadata:** `source`, `company`, `fiscal_year`, `item`, `item_title`, `section`, `page_start`, `page_end`, `location` (e.g. `Item 7, p. 43`), `words`, `url`.
- **Number of chunks:** 606 (Tesla 166, Ford 265, GM 175); median about 190 words.
- **Embeddings:** `gemini-embedding-2` (3,072 dimensions), stored in ChromaDB under `index/` (17 MB), saved batch by batch; chunks already in the index are never embedded again.

## Test set

32 questions in `eval/questions.csv`: 20 `single`, 6 `multi`, 6 `unanswerable`, spread across the three companies and Items 1, 1A and 7.

**How they were written:** by reading the cleaned reports (`corpus/clean/*.md`, which keep headings and printed page numbers), before comparing retrieval designs or tuning anything, phrased as an analyst would ask rather than copied from the text. A little above the minimum of each kind, so a question found faulty could be dropped. Each answer and page was then checked against the cleaned text, which led to three changes:
- q10 (GM dealerships): the report gives 4,566 in GMNA and 6,276 in GMI, not the total; the reference answer now shows the breakdown and the sum (10,842), so an answer that gives the breakdown is not graded wrong.
- q26 (Tesla energy vs. automotive revenue): both figures were on p. 37, so it did not really need two passages; it was rewritten to also ask what drove the energy revenue increase, which is explained on p. 38.
- q31 (Tesla CEO compensation): the reports mention the 2025 CEO Performance Award but give no total compensation; the reference answer now says so, so a refusal that mentions the award is graded correct.

**Unanswerable questions** are close to the topic: other EV makers (Rivian, Lucid, Stellantis), a period not covered (Ford's actual Q1 2026 results, a trap because the report contains a full-year 2026 outlook), information that lives in the proxy statement (CEO compensation), and an investment recommendation. The Rivian question is the one used for the add-document test.

**Two examples:**

| id | kind | question | reference answer |
|---|---|---|---|
| q21 | multi | Which company reported the larger tariff-related cost burden in 2025, Ford or GM, and how do their disclosures differ? | GM reported $3.1 billion in tariff-related costs [GM, Item 7, p. 32]. Ford reported about $3 billion in gross tariff costs and a $2 billion net EBIT impact after offsets [Ford, Item 7, p. 43]. |
| q30 | unanswerable | What were Ford's actual consolidated revenues and adjusted EBIT in the first quarter of 2026? | The corpus contains fiscal year 2025 information, not actual Q1 2026 results. |

q21 tests the gross vs. net distinction; q30 tests whether the assistant presents a forecast as an actual result.

## Retrieval

Hit = a chunk from the expected document whose pages include the expected page is in the top k; for `multi`, every expected passage must be retrieved.

- **Design B (`plain`):** structure-based chunks, nearest neighbours over the whole corpus.
- **Design C (`filter`):** same chunks and vectors, restricted to the company the question names (detected from names and brands: "Cybertruck" → Tesla, "F-150" → Ford, "Chevrolet" → GM); for several companies, one search per company with the results interleaved, so one company cannot fill the top k.

Both designs use the same 606 embeddings, so comparing them cost no extra quota; only the 26 answerable questions were embedded (saved in `eval/query_vectors.json`). Words added to the prompt are the words of the top-5 chunks.

| Design | Questions | n | hit@1 | hit@3 | hit@5 | Words added (k=5) |
|---|---|---|---|---|---|---|
| B `plain` | all | 26 | 0.65 | **0.85** | **0.92** | 868 |
| | single | 20 | 0.85 | 0.95 | 1.00 | 853 |
| | multi | 6 | 0.00 | **0.50** | 0.67 | 920 |
| C `filter` | all | 26 | 0.65 | 0.81 | **0.92** | 864 |
| | single | 20 | 0.85 | 0.95 | 1.00 | 867 |
| | multi | 6 | 0.00 | 0.33 | 0.67 | 853 |

(`multi` hit@1 is 0 by definition: one chunk cannot hold two expected passages.)

**Reading the numbers:** on `single` questions the two designs are identical. Every chunk starts with a header naming the company ("Ford 10-K FY2025 | ..."), so its embedding already carries the company and the nearest neighbours already come from the right report; the filter has nothing left to do. On `multi` questions the filter is worse at k = 3: interleaving forces one result per company and pushes out a second relevant passage from the same company (q22 lost Ford p. 1). Both designs miss the same two `multi` questions at k = 5: q21 (GM's $3.1 billion tariff figure on p. 32 is not retrieved; p. 27, which discusses tariffs without the figure, is) and q25 (a single query returns only Ford passages).

**Chosen design: B with k = 5.** It is the simplest and is equal or better than C on every metric; k = 5 finds every `single` answer at a cost of about 870 words of context. The weakness on comparisons is handled in the tool description instead of in retrieval: `search` asks the model to search once per company, and AGENTS.md rule 2 says the same.

## Tools and subagent

**`search(query)`** description (what the model reads):

> Search the FY2025 Form 10-K annual reports of Tesla, Ford and General Motors (Item 1 Business, Item 1A Risk Factors, Item 7 MD&A), as filed with the SEC. Use it for any question about these companies' business, segments, risks, 2025 results, costs, tariffs, EV strategy or outlook. Write the query in English and name the company. For a comparison between companies, search once per company so each report's passage is found. Returns the 5 most relevant passages, each headed by its citation [source, Item, page] followed by the passage text. Cite those labels exactly. If no passage answers the question, the reports do not cover it.

**`add_document(path)`** description:

> Add a Form 10-K annual report to the searchable index. `path` is a local EDGAR .htm/.html file (absolute, or relative to the project folder). Its Items 1, 1A and 7 are cleaned, chunked with source and page metadata, embedded with Gemini and stored, after which `search` finds them. A file already in the index is not embedded twice. Returns how many passages were added, or why nothing was added.

**One search result** (query: "Which company reported a bigger tariff cost in 2025, Ford or GM?", first result):

```
Result 1 [ford_10k_fy2025, Item 7, p. 43] Ford | Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations | Key Trends and Economic Factors Affecting Ford and the Automotive Industry
In 2025, Ford's gross costs related to tariffs implemented or revised in 2025 was about $3 billion, including the impact of tariff relief, and the net EBIT impact was about $2 billion after offsets. ...
```

**Subagent** (`.claude/agents/corpus-researcher.md`): tool `mcp__corpus__search` only; it searches once per company, answers only from the passages, cites every claim, keeps gross/net and actual/forecast apart, refuses with "The reports in the corpus do not cover this." and never recommends buying or selling.

**Transcript from the editor** (Claude Code, exported with `/export`; also in `subagent_transcript.txt`):

```text
 ▐▛███▛█   Claude Code v2.1.330
▝▜██████▀  Opus 5.5 · Claude Enterprise
 ▝▝   ▝▝   ~\Documents\Assigment_1_AI\daiist-assignment-3


● Your organization may apply global configuration to Claude Code. These
  settings are centrally managed by your IT administrator.

> Use the corpus-researcher subagent to answer: Which company had the larger    
  global workforce at the end of 2025, Ford or Tesla?                           

● Please run /login · API Error: 401 OAuth access token is invalid.

> /login 
  ⎿  Login successful

● corpus-researcher(Compare Ford vs Tesla workforce)
  ⎿  Backgrounded agent (↓ to manage · ctrl+o to expand)

● The corpus-researcher subagent is searching the Ford and Tesla 10-Ks now. I'll
  post its answer, with citations, when it finishes.

✻ Brewed for 1m 33s · done 18:14

› Message from corpus-researcher
  Ford had the larger workforce at the end of 2025. Ford reported about 169
  thousand employees and Tesla reported 134,785. The two figures are counted
  differently, so the comparison is approximate (see the scope notes below).

  - **Ford:** "The approximate number of individuals employed by us and entities
  that we consolidated as of December 31" is 169 thousand in total for 2025,
  down from 171 thousand in 2024 [ford_10k_fy2025, Item 1, p. 17]. The 2025
  total is made up of:
    - United States: 87 thousand
    - Rest of World: 76 thousand
    - Ford Credit: 6 thousand
    - Company excluding Ford Credit: 163 thousand [ford_10k_fy2025, Item 1, p.
  17].
  - **Tesla:** "As of December 31, 2025, our employee headcount worldwide was
  134,785" [tesla_10k_fy2025, Item 1, p. 11].

  **Scope notes:**
  - **Ford:** the figure is approximate and rounded to thousands. It covers Ford
  and the entities it consolidates, including Ford Credit. Joint ventures that
  Ford does not consolidate are not included. The report does not say whether
  the count is full-time only [ford_10k_fy2025, Item 1, p. 17].
  - **Tesla:** the figure is an exact "employee headcount worldwide". The
  passage does not say whether it is full-time only or how subsidiaries are
  treated [tesla_10k_fy2025, Item 1, p. 11].
  - **Both:** the as-of date is December 31, 2025 for both companies.

  **Difference:** about 169,000 − 134,785 = about 34,215 more employees at Ford.
  Using Ford excluding Ford Credit, the gap is about 163,000 − 134,785 = about
  28,215 (own calculation from the cited figures). Because Ford's figure is
  rounded, read these differences as approximate, to the nearest thousand.

  Not asked, but the same search also returned GM: about 155 thousand worldwide
  at December 31, 2025 [gm_10k_fy2025, Item 1, p. 7].

● Ford had the larger workforce at the end of 2025: about 169 thousand
  employees, against Tesla's 134,785.

  ┌─────────────────────────┬────────────────────┬─────────────────────────┐
  │                         │ Employees at Dec   │         Source          │
  │                         │      31, 2025      │                         │
  ├─────────────────────────┼────────────────────┼─────────────────────────┤
  │ Ford (with the entities │ ~169 thousand      │ [ford_10k_fy2025, Item  │
  │  it consolidates)       │ (2024: ~171        │ 1, p. 17]               │
  │                         │ thousand)          │                         │
  ├─────────────────────────┼────────────────────┼─────────────────────────┤
  │ – United States         │ ~87 thousand       │ [ford_10k_fy2025, Item  │
  │                         │                    │ 1, p. 17]               │
  ├─────────────────────────┼────────────────────┼─────────────────────────┤
  │ – Rest of World         │ ~76 thousand       │ [ford_10k_fy2025, Item  │
  │                         │                    │ 1, p. 17]               │
  ├─────────────────────────┼────────────────────┼─────────────────────────┤
  │ – Ford Credit           │ ~6 thousand        │ [ford_10k_fy2025, Item  │
  │                         │                    │ 1, p. 17]               │
  ├─────────────────────────┼────────────────────┼─────────────────────────┤
  │ – Ford excluding Ford   │ ~163 thousand      │ [ford_10k_fy2025, Item  │
  │ Credit                  │                    │ 1, p. 17]               │
  ├─────────────────────────┼────────────────────┼─────────────────────────┤
  │ Tesla (worldwide        │ 134,785            │ [tesla_10k_fy2025, Item │
  │ employee headcount)     │                    │  1, p. 11]              │
  └─────────────────────────┴────────────────────┴─────────────────────────┘

  How big the gap is: Ford had about 34,215 more people (169,000 − 134,785).
  Leaving out Ford Credit, the gap is about 28,215 (163,000 − 134,785) (own
  calculation from the cited figures). Ford rounds its figure to the nearest
  thousand, so both gaps are only good to about ±1,000.

  The two counts aren't measured the same way:
  - Ford gives an approximate number of "individuals employed by us and entities
    that we consolidated." It includes Ford Credit and leaves out joint
    ventures Ford doesn't consolidate. It doesn't say whether the count is
    full-time only.
  - Tesla gives an exact "employee headcount worldwide." It doesn't say whether
    the count is full-time only or how subsidiaries are treated.
  - Neither difference is large enough to change which company is bigger.

  The same search also returned General Motors: about 155 thousand employees
  worldwide at December 31, 2025 [gm_10k_fy2025, Item 1, p. 7].

✻ Crunched for 7s · done 18:14

● Agent "Compare Ford vs Tesla workforce" finished · 14s
```

## Adding a document

**Already indexed:** `add_document` skips it and says so ("Not added: gm_10k_fy2025 is already indexed (175 passages). Nothing was embedded."). The alternative, replacing (delete the old chunks and embed the file again), was rejected: a 10-K is filed once a year and its content does not change afterwards; a correction is filed as a separate 10-K/A with its own file name, which would be indexed as a new source. Replacing would therefore spend 170-260 embeddings per report for nothing, and if it stopped halfway it would leave the report half indexed. Skipping is cheap, safe and never loses data.

The document's identity is its `source` (company and fiscal year, e.g. `rivian_10k_fy2025`), read from the 10-K cover page ("Exact name of registrant") and the EDGAR file name, so the same report copied to another folder is still recognised (a renamed file loses the year from its name, which is a known limitation).

**Before/after.** Unanswerable question q27: *"How many vehicles did Rivian deliver worldwide in fiscal year 2025, and what was its year-over-year delivery growth?"*

- **Before** (evaluation run; two searches, "Rivian vehicle deliveries 2025" and "Rivian deliveries growth 2025"):
  > The reports in the corpus do not cover this. The corpus covers only the Form 10-K annual reports for Tesla, Ford, and General Motors, and does not include information on Rivian.
- **Adding the document:** Rivian's FY2025 10-K (`rivn-20251231.htm`, filed 2026-02-12, https://www.sec.gov/Archives/edgar/data/1874178/000187417826000008/rivn-20251231.htm), added through the agent, which asked for approval first:

  ```text
  > uv run python main.py ask "Please add the document corpus/extra/rivn-20251231.htm to the index."
  The agent wants to add 'corpus/extra/rivn-20251231.htm' to the index (this spends embedding quota). Approve? [y/N] y
  The agent wants to add 'corpus/extra/rivn-20251231.htm' to the index (this spends embedding quota). Approve? [y/N]
  The reports in the corpus do not cover this.
  [figure check fired: 20251231, 279; retried once]
  [2 tool calls, 4 model calls, 5620+141 tokens, 154.3s]
  ```

  The first, approved call embedded and stored 279 chunks (the index went from 606 to 885). The rest of the transcript shows two things. The approval guardrail worked: a second call was not approved (Enter = no) and did nothing. The figure check misfired again: the agent's confirmation quoted the tool's reply ("rivn-20251231", "279 passages"), the check only counts search results as evidence, so it flagged those numbers; on the retry the agent tried to add the file again and, refused, ended with the refusal sentence. The document was added correctly, but the final message is wrong. The same fix as in Failures applies, plus counting every tool result (not only searches) as evidence.
- **After** (same question; two searches, 5.8 s):
  > In fiscal year 2025, Rivian delivered **42,247 vehicles** worldwide [rivian_10k_fy2025, Item 7, p. 61]. The year-over-year delivery growth was **-18%** (a decrease from 51,579 vehicles delivered in 2024 to 42,247 vehicles delivered in 2025, representing a decrease of 9,332 vehicles) [rivian_10k_fy2025, Item 7, p. 62].

  Correct and cited: the report gives deliveries of 51,579 (2024) and 42,247 (2025), a change of (9,332), (18)% (Item 7, pp. 61-62).

## Harness and guardrails

- **Model:** `gemini-3.5-flash-lite` for the agent and the judge. On the free tier the flash models (3.8, 3.6, 3.5) allow 20 requests a day each and 3.8-flash returned 503 "high demand" for hours, so the 32 questions (about 100 model calls plus 32 judge calls) could not be run on them before the deadline. One model answers every question so the results are comparable; the first 6 answers obtained with `gemini-3.6-flash` are kept in `eval/answers_gemini-3.6-flash_first6.jsonl` for comparison.
- **System prompt:** `AGENTS.md` (10 rules, each with its reason: search first, one search per company, evidence only, exact citations, gross/net/adjusted, actual vs. forecast, units and own calculations, fixed refusal sentence, no investment advice, no add_document without permission).
- **Approval:** `add_document` runs only after the user types `y` at the terminal; with nobody at the keyboard (evaluation) it is refused.
- **Call limits:** at most 6 tool calls and 10 model calls per question; patient retries on Gemini 503/429 errors, with no fallback to a weaker model.
- **Extra guardrail: figure check.** Every number in the answer must appear in the retrieved passages (allowing for millions vs. billions) or follow from two of them by a sum, difference or ratio. If not, the agent is told which figures are unsupported and gets one retry; figures still unsupported are flagged under the answer.

  **Where it fired:** twice in 32 answers, and both times wrongly. In q07 (Ford adjusted EBIT) it flagged "3,428 million" and "33.6%", a correct decline and percentage change; the agent rewrote the answer and it was still right. In q24 (Ford vs. GM wholesales) it flagged "596,000", the correct difference between 4,395 and 3,799 thousand; on the retry the agent removed the figure and wrote that "the reports in the corpus do not state the exact difference", turning a correct answer into a wrong one. The cause is in the code: to stay fast, the check stops computing derived figures when the passages hold many numbers, which is always the case with tables (every figure is also tried in thousands and millions, so the number of pairs explodes). See Failures.

## Evaluation

`main.py evaluate` ran the agent (`gemini-3.5-flash-lite`) on all 32 questions with `add_document` refused, saving each answer as it arrived (`eval/answers.jsonl`), then ran the code checks, the judge and the agreement with my grades. Outputs: `eval/e2e_results.csv` (one row per question), `eval/judge_verdicts.csv`, `eval/e2e_summary.json`.

**Code checks** (what code can check without judgement):
- *Refusals:* the answer contains the fixed sentence "The reports in the corpus do not cover this" (AGENTS.md rule 8). Gives correct refusals (unanswerable and refused), wrong refusals (answerable and refused) and missed refusals.
- *Citations:* every `[source, Item, p.]` label in the answer must match a passage the agent actually retrieved; also whether the expected documents are cited.
- *Figure check:* whether the guardrail fired and whether any figure was still unsupported.

**Judge:** `gemini-3.5-flash-lite`, temperature 0, JSON output. It sees the question and its kind, the reference answer, the retrieved passages and the answer, and grades with my rubric (`eval/judge_rubric.md`): `correct` and `supported`, binary, with borderline cases decided in advance (rounding accepted; gross vs. net confusion is wrong; a `multi` answer must get every part right; a refusal may mention related information if it says it is not the answer; a correct own calculation counts as supported even without its label; a true statement missing from the retrieved passages is unsupported).

**Results:**

| Measure | Value |
|---|---|
| Correct (judge, 32 answers) | 31/32 (0.97) |
| Supported (judge, 32 answers) | 32/32 (1.00) |
| Correct (my grades, 22 answers) | 18/22 (0.82) |
| Supported (my grades, 22 answers) | 19/22 (0.86) |
| Correct refusals (code) | 6/6 |
| Wrong refusals (code) | 0/26 |
| Citations that match a retrieved passage (code) | 31/32 |
| Figure check fired | 2 (q07, q24) |

**Agreement with the judge** on the 22 answers I graded: 86% on `correct` and 86% on `supported`. Every disagreement goes the same way: the judge is more lenient than I am. On `correct` it passed q18 (generic risks instead of the specific battery-cell supplier dependence), q21 (compares GM's EBIT-adjusted impact with Ford's net EBIT impact to conclude) and q23 (omits the 4-point difference the question asks for); it only failed q24. On `supported` it gave 1 to every answer, while I found unsupported statements in q21, q24 and q32. A lite judge misses exactly the nuances the rubric was written for, so I take my own grades, not the judge's 0.97, as the measure of quality.

The one invalid citation (q02) is a format slip: the agent cited `[ford_10k_fy2025, Item 1, p. 2]` for a passage labelled `Item 1, p. 2-3`; the figure itself is right.

## Failures

Failures among the 22 answers I graded (a question counts once per cause; q21 fails both criteria), checked against the passages the agent retrieved:

| Question | What happened | Cause |
|---|---|---|
| q18 | The passage with the expected factor (Tesla p. 14: only a very limited number of qualified battery-cell suppliers) was not retrieved; the answer lists other, generic production risks | Retrieval miss |
| q21 | Had the figures for both companies, but concluded that GM bore the larger burden by comparing GM's EBIT-adjusted impact with Ford's net EBIT impact, two different measures | Wrong answer from the right passage (and an unsupported conclusion) |
| q23 | Retrieved both expected passages and gave both market shares, but not the 4-point difference asked for | Wrong answer from the right passage |
| q24 | Retrieved both passages and computed the difference correctly, but the figure-check guardrail wrongly flagged it and the agent removed it on the retry | Wrong answer from the right passage, caused by the guardrail |
| q32 | Refused correctly but without searching (against AGENTS.md rule 1), adding claims about missing market prices and valuations that no passage supports | Unsupported claim |

**Counts:** retrieval miss 1, wrong answer from the right passage 3, unsupported claim 1 (plus the conclusion in q21), wrong refusal 0, bad test question 0 among the graded answers. Retrieval also shows one bad test question: q01 expects Ford's 169,000 employees on p. 1, but the same figure is on p. 17, which the search ranks first; both pages are valid answers.

**What to fix first: the figure-check guardrail.** It is the only failure that the system caused itself, and it can turn correct answers into wrong ones on exactly the questions where it matters most (comparisons that need a calculation). Fix: compute derived figures from the values as written, before scaling them to thousands and millions, so the pool of pairs stays small and is never skipped. I left it unfixed so the submitted code is exactly the code that was evaluated.

**Next:** the comparison answers (q21, q23, q24) need a rule or a check that a `multi` answer gives every part asked for, including the difference or the conclusion, computed on like-for-like measures. q18 points to retrieval: risk factors are long and phrased generically, so a hybrid (keyword + vector) search or smaller chunks in Item 1A would help.

## Decision

**Yes, but only for single-fact lookups, and not yet as it stands.** Analysts could rely on it to find one figure or one statement in one report: a segment, a headcount, a market share, a reported cost, a declared risk. Of the 15 `single` questions I graded it answered 14 correctly and all 15 with supported statements (the miss, q18, was a retrieval miss), its citations point to the exact page, and it never refused a question it could answer while refusing all six it could not (6/6 correct refusals, 0 wrong refusals). Its refusals are the strongest part of the system: when it does not know, it says so.

It should not be relied on for comparisons between companies or for answers that need a calculation. That is where all three of its wrong answers from the right passage are (q21, q23, q24): it had the right figures and still compared unlike measures or left out the difference the question asked for. In this use case those are exactly the errors that do damage, because they look right and carry citations.

**Before analysts use it:**
1. **Fix the figure-check guardrail** so that derived figures are always checked and every tool result counts as evidence. Today it turned a correct answer into a wrong one (q24) and corrupted the add-document confirmation.
2. **Improve comparisons and calculations:** a rule, and a check in code, that a `multi` answer gives every part asked for, compares like-for-like measures (gross with gross, net with net) and shows its arithmetic; and a stronger model than the free-tier lite one.
3. **Use a stricter judge** (a stronger model, or two judges that must agree) before trusting automatic scores. The lite judge rated 31/32 correct where I rated 18/22, and it missed every nuance my rubric was written for, so today only human grading tells the real quality.

**Safeguard in use:** the analyst checks every cited page before a figure goes into a model or a note. The citations make this take seconds, and it is the only protection against the errors the system still makes.

**Latency:** the median is acceptable (12 s), but the tail is not: 10% of questions took about 3 minutes or more and one took 14 minutes, because the free tier throttles and drops requests. A paid tier, with higher quotas and no 503 errors, would make latency stable and allow a stronger model; at about 6,450 tokens per question the cost should stay small (to be checked against current prices).

**Cost and latency per question** (32 questions, `gemini-3.5-flash-lite`): on average about 6,450 tokens (6,180 input, 276 output), 2.2 model calls and 1.4 searches (one query embedding each); median 12 s, 90th percentile 171 s, maximum 823 s. The long tail is free-tier congestion (503 errors and retries), not the agent's work. The judge adds one call per answer.

## AI use

I used Claude Code (Anthropic) to help me write and debug the code, to research and develop ideas, and to help me draft this report. I verified and edited everything it produced; the project's decisions, the test questions, my own grades and the analysis are mine.
