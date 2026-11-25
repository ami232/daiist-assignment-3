# Assignment 3 Report

- **Name**: Constantin Hatecke
- **Student ID: 20241
- **Group**: BBADBA 5A 

## Use case

Throughout the world, equity and credit analysts as well as investors and economists await the 10-K reports of the largest US financial institutions. They provide the official data to analyze and estimate the health of the businesses and the sector. However, these documents are long and have many different, complicated structures. Using AI helps a lot; however, normal models tend to hallucinate and can end up reporting false data.

The users of this system are analysts covering Goldman Sachs, Morgan Stanley and BlackRock. They ask for specific figures (segment revenues, client assets, fee rates, margins) and for the risks the firms state, and they copy the answers into their notes and models.

AI that gives false data is risky, and the impact can be serious. Sometimes, it's better for the model to say "I don't know," since using wrong data in risk models or client presentations could cost millions, while a quick manual check only takes a few minutes. That is why the system cites a passage for every sentence and refuses rather than guesses. Question answering over SEC filings is a standard test for retrieval-augmented generation in finance (FinanceBench, Islam et al., 2023). Earlier results weren't great, but a well-tuned RAG system can now give a source for every answer.

## Corpus

| document | form | period | URL | licence | words indexed |
|---|---|---|---|---|---|
| Goldman Sachs | 10-K | FY2025 | https://www.sec.gov/Archives/edgar/data/886982/000088698226000091/gs-20251231.htm | Public SEC filing [TODO: confirm wording] | 34,826 (Risk Factors 20,920 + MD&A results 13,906) |
| Morgan Stanley | 10-K | FY2025 | https://www.sec.gov/Archives/edgar/data/895421/000089542126000086/ms-20251231.htm | Public SEC filing | 20,049 (10,574 + 9,475) |
| BlackRock | 10-K | FY2025 | https://www.sec.gov/Archives/edgar/data/2012383/000119312526071966/blk-20251231.htm | Public SEC filing | 29,015 (15,595 + 13,420) |
| Goldman Sachs (added later) | 10-Q | Q3 2026 | https://www.sec.gov/Archives/edgar/data/886982/000088698226000532/gs-20260930.htm | Public SEC filing | 13,941 (MD&A results) |

I picked these three firms because they are directly comparable, and together the sections I kept add up to 83,890 words, which is more than the project requires. This lets me include a range of two-passage questions that come up naturally. I removed the Business section (since it repeats MD&A) and the balance sheet, liquidity, capital, and risk-management parts of MD&A, as analysts rarely compare those. Even after these cuts, there was still plenty of useful information, and I stayed within the free embedding quota. The 10-Q was held back for the add-document test.

## Ingestion

The ingestion is split into 4 parts.

- **Download:** fetching the SEC filing from EDGAR, using my name and email as it is required.
- **HTML to text:** I extracted the text from the filing, which is a web page full of code. I removed the hidden inline XBRL header and converted each table into one line per row, keeping only the readable text.
- **Cut sections:** I kept only the specified sections from each file. I looked for the headings (Risk Factors, MD&A) and kept only those parts. The table of contents at the start lists the same headings, so I used the longest match to find the actual section.
- **Clean:** I removed things that repeat on every page and mean nothing, e.g. page headers like "THE GOLDMAN SACHS GROUP, INC. AND SUBSIDIARIES", page numbers and "Table of Contents" links.

I compared two ways of cutting the text into chunks. Design A uses windows of about 300 words with 50 words of overlap (360 chunks). Design B uses one chunk per subsection of MD&A or per risk factor, splitting long ones into parts of about 300 words (350 chunks).

The main extraction problem was tables. The filings put symbols like $ or % in their own cells, and every number was sitting in its own XBRL tag, so the plain text dump would split "$12.3 billion" across three lines. When a chunk started in the middle of a table, it contained rows like `ROE | 16.6% | 14.0%`, without saying which year each column was or what the table was about. The working fix was that I wrote each row as `label | value | value` with the symbols attached, and added the table's column header (for example `(in millions) | 2025 | 2024`) at the top of any chunk that starts mid-table. 39 chunks in design B needed this.

Every chunk keeps its filing, section, heading, and exact line range, so each citation points to a specific place in the text. Before embedding, the firm name, form, year and heading are added to the chunk to keep them distinct. Embeddings use gemini-embedding-2 and are stored in ChromaDB. To make sure that nothing is embedded twice, I store every vector in a cache the moment it is created, so a run stopped by the daily limit could continue where it stopped without losing anything. This proved to be very useful in the end.

## Test set

To test the model, I used 32 questions with a 20/6/6 split: 20 single-passage questions, 6 multi-passage questions (5 comparisons between two firms and 1 combining two parts of BlackRock's filing) and 6 unanswerable questions. They were written before retrieval was built, and each answer was checked against an exact quote in the filing.

I made the unanswerable questions as close as possible to the corpus, so it would be tempting to guess. For example, I used a time period just outside what was reported (like Goldman's Q3 2026, which only the 10-Q covers), a section I removed (Morgan Stanley's liquidity coverage ratio), a firm not in the corpus (JPMorgan), or a breakdown not given in the filing (Goldman's assets from Swiss clients).

Filings often repeat the same figure. For example, Goldman's $58.28 billion revenue shows up on line 10 (summary) and again on line 75 (detailed section). In my first test run, I only noted the line number where I found the info. Because I missed the repeated mentions, many questions came back as "missed," but they weren't real misses. I fixed this by listing every place each answer appears. The questions, answers, and system stayed the same, and this fix applies to every design. It made the test fairer, not the system better.

Two examples:

- **q12 (single):** "What was BlackRock's operating margin in 2025 on a GAAP basis and on an as adjusted basis?" Reference: 29.1% GAAP, 44.1% as adjusted.
- **q21 (multi):** "Whose wealth business grew net revenues faster in 2025: Goldman Sachs Asset & Wealth Management or Morgan Stanley Wealth Management?" Reference: Morgan Stanley, +12% to $31,754 million, against +2% to $16.68 billion at Goldman.

I also added 5 held-out questions on the Goldman 10-Q, a filing never used to build or test anything, to check whether the system works on new SEC data.

## Retrieval

How I tested the model: the 26 answerable questions (the 32 minus the 6 unanswerable ones) go through the same search that the agent uses, without the agent. A hit means one of the top results contains the answer's lines, and for multi-passage questions both passages must be found.

First run (one location per fact):

| design | hit@1 | hit@3 | hit@5 | words@5 |
|---|---|---|---|---|
| A_fixed | 39% | 58% | 77% | 1,651 |
| B_structure | 46% | 85% | 92% | 1,341 |
| B_structure + hybrid (BM25 keywords, reciprocal rank fusion) | 46% | 89% | 89% | 1,338 |

Final run (full answer key: every place a fact is stated):

| design | hit@1 | hit@3 | hit@5 | single hit@5 | multi both@5 | words@3 | words@5 |
|---|---|---|---|---|---|---|---|
| A_fixed | 62% | 81% | 85% | 95% | 50% | 990 | 1,651 |
| B_structure | 54% | 96% | 100% | 100% | 100% | 802 | 1,341 |
| B_structure + hybrid | 58% | 92% | 92% | 95% | 83% | 805 | 1,333 |

There are two ways that a hit is recognized. Either one of the top 5 results includes the line that is labeled as correct in the answer key. Since that could still have gaps, there is a second check, which looks at the chunks and filters for exact text like "$58.28 billion". It only works for questions with figures and is reported separately (not included in the hit rate). If it's found, then it's likely the right info, and if the answer key missed it, it is still considered a success. I checked whether the correct passage is under the top 1, 3, or 5 closest chunks to have an idea of the accuracy. Both checks rank the designs the same way.

The decision after analysis is to use top 5 in design B without the hybrid structure. Within the top 5, which is what the agent reads, B found the right passage for every question (A: 85%) and both passages for every comparison (A: 50%). Additionally, B sends out 20% fewer words to the model, which keeps each question cheaper. A is slightly better at top 1, because a small window often puts the exact sentence first, but the agent reads all 5.

B works better because a chunk that is the whole subsection keeps the whole table together, and risk factors together with their explanation, while fixed 300-word windows tend to cut through them.

The hybrid approach was dropped because it never outperformed B, and its score changed between runs (from 96% to 92%) after adding the 10-Q. B stayed at 100%, so I kept the simpler design. However, since one question is worth about 4 percentage points, the difference isn't huge. Between A and B, though, the difference was clear.

## Tools and subagent

The server (`server.py`) is a small program that gives the agent its tools over MCP. It doesn't re-embed the filings and only embeds each search query the first time; after that it comes from the cache.

Tools:

- **search(query):** returns the 5 closest passages. Each result includes a citation ID, the filing, section, heading, line range, and the text. The description tells the model what's indexed (Risk Factors and the results part of MD&A for the three firms) and what isn't (balance sheet, liquidity, capital). It also says to search once per firm when comparing, and if nothing relevant comes back, it means the filings don't cover the question.
- **add_document(path):** adds a new file (SEC filing, PDF, text, or Markdown) using the same pipeline as the rest of the corpus, so it's searchable right away. The description says to use it only when the user asks and that each call needs approval. Adding the same file twice does nothing; a changed file replaces its old passages. It won't accept files outside the project folder.

A search result looks like this (q12, first of five passages, shortened):

```
5 passages for: BlackRock operating margin 2025 GAAP as adjusted
Cite a passage by its id in square brackets, e.g. [BLK_10K_FY2025#mdna017].

[BLK_10K_FY2025#mdna017] BlackRock 10-K 2025 · MD&A · Non-GAAP Financial Measures · lines 92-123 of item_7_mdna.txt
(columns: (in millions) | 2025 | 2024)
Operating income, as adjusted | $9,600 | $8,110
Revenue, GAAP basis | $24,216 | $20,407
...
Operating margin, GAAP basis | 29.1% | 37.1%
Operating margin, as adjusted | 44.1% | 44.5%
```

Note on `check.py`: the only edit is the fix the professor suggested, adding `env=dict(os.environ)` (and `import os`) where `StdioServerParameters` is created, so `GEMINI_API_KEY` reaches the server on GitHub Actions. I made the same one-line fix where `agent.py` starts the server.

The subagent (`.claude/agents/corpus-researcher.md`) can only use the search tool and follows the same rules as described for the agent.

Transcript:

```
[TODO: paste the subagent transcript]
```

## Adding a document

When a document is added but is already indexed, it is recognized as already done and no new embeddings are spent. If the content has changed, the old passages are deleted and the new ones added.

I tested this with an example. I used the question "What were Goldman Sachs' Asset & Wealth Management net revenues in the third quarter of 2026?", which the 10-Ks cannot answer. Before adding anything, the agent refused: "The indexed filings do not cover this." I then asked it to add Goldman's Q3 2026 10-Q. After my approval it added 58 passages. Asked again, it answered: "$5,051 million ($5.05 billion) for the third quarter of 2026", with citations to the 10-Q.

I then asked the 5 held-out questions on the 10-Q without changing anything. The system found the right passage every time, and the judge rated all 5 answers correct (4 answered, 1 correctly refused). One limit: the sections kept from each filing were chosen by hand for these filings, so a new company's filing would be indexed whole, with more irrelevant passages.

## Harness and guardrails

The agent (`agent.py`) is a LangChain loop in which Gemini 3.5 Flash Lite decides when to search and when to answer, with `AGENTS.md` as its instructions. The instructions: search first, answer only from the passages, cite every sentence, refuse when the filing doesn't cover the question. This seemed to work well.

The approval for `add_document` requires the user to type "y". If there is no terminal, the answer is automatically no. To stop a confused or looping agent, each question is limited to 6 model calls and 4 tool calls to protect the quota.

The last guardrail is a citation check in code. It checks that every cited ID comes from a search the agent ran in that question. If that is not the case, the agent gets one more try; if it fails again, the answer is replaced by a refusal. It actually fired on the first real question: the answer was correct, but the model wrote two IDs in one bracket, which my first version didn't recognize. After fixing the check, the same question used 5,383 tokens instead of 9,768. The lesson: a guardrail needs testing like any other code.

## Evaluation

Each answer goes through code checks first: did the agent search, does it cite, are all cited ids passages the search actually returned, did it refuse, and did it retrieve the expected passage. Then the LLM judge (Gemini 3.1 Flash Lite) grades it on two things, using the reference answer and every passage that the agent retrieved: correct and supported.

It is marked correct when it's the right figure or fact, the right firm, the right period, and the right basis, or when it's a refusal for an unanswerable question. It is marked supported when every claim in the answer can be found in the retrieved passages. I am using a different model from what the agent uses so that it does not grade its own answers.

I graded 20 answers myself before looking at the judge's verdicts. We agreed on 90% of correct grades and 95% of supported grades. Cohen's kappa comes out at 0.0, but that number means little here: I graded every answer correct, so my grades have no variation, and kappa drops to 0 even at 90% agreement.

The three disagreements:

- **q19:** the judge said the answer left out GIP, but it names both GIP and HPS. Judge error.
- **q29:** the judge marked a proper refusal as wrong because it also mentioned a related figure, which the rubric allows. Judge error.
- **q01:** the judge accepted "$4,771 million" as supported, but the agent calculated it and it appears in no passage. I caught it; the judge didn't. Technically correct but needs additional attention before we allow the agent to do its own analysis on cited figures.

The judge is useful as a first pass but makes mistakes in both directions, so final grades use mine where I graded.

| measure | result |
|---|---|
| answerable, correct | 26/26 |
| answerable, every claim supported | 25/26 |
| unanswerable, correctly refused | 6/6 |
| wrong refusals | 0/26 |
| citations valid (code check) | 100% |
| expected passage retrieved by the agent | 100% |
| held-out 10-Q questions correct | 5/5 |

## Failures

| cause | count | questions |
|---|---|---|
| retrieval miss | 0 | |
| wrong answer from the right passage | 0 | |
| unsupported claim | 1 | q01 |
| wrong refusal | 0 | |
| bad test question | 0 | |

The only failure in the final run was the unsupported claim in question 1. The number was right but unsupported: the agent calculated the difference between 2025 and 2024 revenue itself and stated it with a citation, so an analyst checking the citation can't verify it. The held-out question h01 shows the same pattern ("approximately $3.49 billion"). Potentially this needs additional attention before we allow the agent to do its own analysis on cited figures. Other minor things are that, for q16, it mentioned less relevant risks before the one that was actually asked for, and for q22 it doesn't mention that the numbers for Goldman Sachs and BlackRock are actually measured differently.

What to fix first: calculated figures. I would add a rule to `AGENTS.md`, "never state a number that isn't in a passage; if you calculate one, say so and show the inputs", and extend the citation check so it also verifies that every number in an answer appears in one of the cited passages. That turns the most likely remaining error into an answer that is either labelled as a calculation or blocked.

## Decision

I would let analysts rely on it as a finder and first draft: it finds the right passage and gives the figure with a citation that takes seconds to check. I would not let its figures go into models or client documents without that check, mainly because of calculated numbers like q01. The safeguards are the citation shown with every figure, the refusal rule, which held on all 7 questions it should have refused, and, before wider use, the number check described above. The evidence also has limits: 32 questions plus 5 held-out ones, written after reading the filings, are a small and friendly test, and vaguer questions or other companies' filings would likely do worse.

Per question the agent used on average 5,781 tokens (median 4,826, maximum 12,265) and 5.1 seconds (median 3.3, maximum 28.5), with about 2 model calls and one query embedding. 98% of the tokens are input, mostly the retrieved passages, so the number of passages and their size drive the cost. Comparisons and refusals cost the most because the agent searches more than once. The judge adds about 3,500 tokens per question. On the free tier the real limit is requests per day (500 for Flash Lite), not tokens.

## AI use disclosure

I used an AI assistant (Claude, by Anthropic) for code in this assignment, as the README allows. It helped me write and debug code: the ingestion and chunking pipeline, the retrieval and generation calls, the evaluation and LLM-judge scripts, and the plots and tables in this report. I reviewed, ran and tested all code that ended up in the repository, and I can explain each part of it without help.

These parts are my own work:

- **Decisions:** the use case (RAG over the Goldman Sachs, Morgan Stanley and BlackRock 10-K filings), the corpus scope and chunking strategy, the design choice I compared, the refusal behaviour, the judge rubric and the ship decision.
- **Test set:** the questions and reference answers in the evaluation set.
- **Human grades:** every grade in `human_labels.csv` comes from me reading each answer against the source filing.
- **Analysis:** the interpretation of results, the error analysis and the conclusions in this report.

Where the AI suggested a different approach to one of the decisions above, I made the final call and the reasoning in this report is mine.