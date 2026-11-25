# Assignment 3 Report

- **Name**:Beatriz Cruces Alvaro
- **Student ID**: 20081
- **Group**: BBADBA 5B 

## Use case
The person asking is a macro analyst or an equity sales analyst who wants to see how companies (Ralph Lauren, PVH and Tapestry) are doing when they publish their 10-Ks. They use the answers to run analysis with that data. It is better for the answer not to be false: with false data the client would be unhappy and could make an uninformed decision.

If the system says "I don't know", the analyst only loses a little time looking it up in the 10-K; but a false figure is noticed late and can end up in a wrong analysis. That is why I prefer that the system refuses rather than makes something up.

## Corpus

Ralph Lauren 10-K, fiscal year ended March 28, 2026: 85,477 words. URL: https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm

PVH 10-K, fiscal year ended February 1, 2026: 84,674 words. URL: https://www.sec.gov/Archives/edgar/data/78239/000007823926000021/pvh-20260201.htm

Tapestry 10-K, fiscal year ended June 27, 2026: 70,516 words. URL: https://www.sec.gov/Archives/edgar/data/1116132/000111613226000018/tpr-20260627.htm

In total there are 240,667 words in the full filings (counted on the text extracted from the HTML, before keeping only Items 1, 1A and 7).

I chose these three companies (Ralph Lauren, PVH and Tapestry) because they are in the same sector, so questions that compare them make sense, and because I am interested in finance and I think 10-Ks are a very good source for micro analysis of companies. I indexed only Item 1 (Business), Item 1A (Risk Factors) and Item 7 (MD&A) because this is narrative text, which is much easier to extract cleanly than the financial statements in Item 8, and because these are the parts an analyst reads to understand the business, its risks and its results. The documents are public SEC filings and contain no personal data.

## Ingestion

Extraction and cleaning. The three 10-K filings are downloaded from the SEC (EDGAR) as HTML. The HTML is converted to plain text: scripts, styles and the hidden XBRL header are removed, table cells are separated with " | ", and whitespace is normalised. Then only three sections are kept: Item 1 (Business), Item 1A (Risk Factors) and Item 7 (MD&A). Each section starts at its heading and ends at the heading of the next item (for example, Item 1A ends at Item 1B or Item 2).

Extraction problem. In a 10-K the same headings appear twice: once in the table of contents and once at the real section. If the code took the first match, it would keep the table of contents instead of the section. The code looks at every match of a heading, measures how much text follows it until the section's end heading, and keeps the match with the most text. A section with fewer than 500 words is discarded, because it was a table of contents entry or a cross-reference.

Chunking. Each section is split into chunks of 250 words with an overlap of one fifth (50 words), so that a sentence cut at the end of a chunk also appears at the start of the next one. Every chunk carries its company, section, chunk number and fiscal year end, which is what appears in the citations, for example [PVH | Item 1. Business | chunk 5 | fiscal year end 2026-02-01].

Embedding and storage. The chunks are embedded with Gemini (gemini-embedding-2) and stored in ChromaDB with cosine distance, in index/. Vectors are saved, so rebuilding the index only embeds chunks that do not have a vector yet (the free tier allows about 1,000 embeddings per day).

Number of chunks. 553 chunks with 250-word chunks and 347 chunks with 400-word chunks (two collections, tenk_w250 and tenk_w400).

## Test set

The test set has 31 questions in eval/questions.csv: 18 single-passage questions, 7 multi-passage questions (they need information from two passages, for example to compare two companies) and 6 unanswerable questions, which the corpus cannot answer. Each question has a reference answer and the place where it can be found in the documents. For the unanswerable questions, the correct behaviour is to refuse with "The corpus does not cover this."

Examples:

Single-passage (q10): "What are PVH's reportable segments?"


Multi-passage (q25): "Which of Ralph Lauren and Tapestry had higher employee numbers, and how many does each report?" (one passage from each company is needed)


Unanswerable (q26): "What were Ralph Lauren's total assets at the end of its latest fiscal year?" (the balance sheet is in Item 8, which is not indexed)

The unanswerable questions cover different reasons for not answering: the data is in a part of the 10-K that is not indexed (q26, q31), it is in the future (q27), it belongs to a company that is not in the corpus (q28), it asks for an opinion (q29) or it asks for a detail the filings do not give (q30).

## Retrieval

Hit rate at k = 1, 3 and 5 (share of questions where the right passage is among the first k results), and words the agent reads with k = 3:

Design A, 250-word chunks: hit@1 64%, hit@3 84%, hit@5 88%; 750 words in the top 3.
Design B, 400-word chunks: hit@1 60%, hit@3 84%, hit@5 88%; 1,200 words in the top 3.

I compared two designs: chunks of 250 words and chunks of 400 words (same overlap of one fifth). Hit rate means that the right passage is among the first k results.

I chose design A (250 words). Both designs tie at k = 3 and k = 5 (84% and 88%), but A is better at k = 1 (64% against 60%), so the right passage more often comes first. A is also cheaper: with k = 3 the agent reads 750 words instead of 1,200, so there are fewer tokens per question and less noise for the model. I kept it simple: the smaller chunk is as good or better in every number and costs less.

Questions where the right passage was not found in the top 5: design A: q19, q22 and q24; design B: q19, q21 and q22. Both designs miss q19 and q22, so the problem is not the chunk size but the question (both are multi-passage questions that are quite open).

## Tools and subagent

The MCP server (server.py, server name corpus) exposes two tools. The description of each tool is what the agent reads to decide when to use it:

- search(query, company="", section="", k=5): "Search the 10-K annual reports of Ralph Lauren (RL), PVH and Tapestry (TPR), covering Item 1 Business, Item 1A Risk Factors and Item 7 MD&A (narrative text only, NOT the financial statements or their notes). Use it for every factual question about these companies. Returns the k most relevant passages, each labelled with its citation [company | section | chunk number | fiscal year end]. Optional filters: company ("RL", "PVH" or "TPR") and section ("Item 1. Business", "Item 1A. Risk Factors", "Item 7. MD&A"). If no passage answers the question, the answer is not in the corpus."

- add_document(path): "Add a new document (an .htm, .html or .txt file in this repository) to the search index: it is split into chunks, embedded with Gemini and stored. This spends embedding quota and changes the index, so it needs user approval. If the same file (same name) or identical content is already indexed, nothing is changed and the reply says so; if the same name exists with different content, nothing is changed either and the user must decide (rename the file to add it as a new version)." It reuses the indexing code of index.py (chunk_file) instead of rewriting it.

I wrote the search description to say what is NOT covered (the financial statements), so that the agent does not search for data that is not there and knows when to refuse.

Example of a search call made by the agent (from the Copilot transcript): {"query": "Ralph Lauren total assets balance sheet March 28 2026", "company": "RL", "k": 10}.

Example of a result of search("PVH reportable segments", company="PVH", k=1) (shortened with "[...]"):

_[PVH | Item 1. Business | chunk 5 | fiscal year end 2026-02-01] (similarity 0.837)
the reorganization of the executive leadership structure directly reporting to our Chief
Executive Officer, who is our chief operating decision maker ("CODM"). [...] Our new
reportable segments are: (i) EMEA, (ii) Americas, (iii) APAC, and (iv) Licensing. The new
reportable segments reflect the way the Company is currently being managed and for which
separate financial information is available [...]_

Each passage starts with its citation and a similarity score, so the agent can copy the citation exactly.

The subagent corpus-researcher (.claude/agents/corpus-researcher.md) only has the search tool and follows seven rules: always search first, search per company for comparisons, answer only from the passages, cite one chunk per bracket, state the fiscal year, refuse with exactly "The corpus does not cover this.", and keep it to five sentences.

Transcripts (run in Copilot with the model MAI Code 2 Flash, not with Claude; the custom agent did not receive the MCP tool, so I enabled the search tool by hand in Agent mode):

Answer with citation: report_assets/ (reportable segments of PVH: EMEA, Americas, APAC and Licensing, cited from Item 1 chunk 5).
Refusal: "What was PVH's share price at the end of fiscal 2025?" -> "The corpus does not cover this."

## Adding a document

Policy for duplicates. If a document is already indexed (same name or identical content, compared with a SHA-256 hash), add_document changes nothing and says so. If the same name exists with different content, it also changes nothing and leaves the decision to the user (rename the file to add it as a new version). I chose to ignore it instead of adding it again or replacing it for two reasons: duplicated chunks would fill the top results with the same passage and leave less room for other passages, and every duplicated chunk would waste embeddings, which are limited on the free tier (about 1,000 per day).

Unanswerable question: q26. Before: the agent searched Ralph Lauren and answered "The corpus does not cover this." I then added extra/rl_balance_sheet.txt, with the balance sheet lines copied from the Ralph Lauren 10-K (Total assets $7,739.5 million at March 28, 2026). After: the agent answered 7.7395 billion dollars citing [rl_balance_sheet | Document | chunk 0 | fiscal year end unknown]. Screenshots: report_assets/antes_screenshot.png, add_document_screenshot.png, after_screenshot.png.

Two things to note. First, the answer also cited [RL | Item 7. MD&A | chunk 36], which does not hold that figure. This shows that my guardrail only checks that a cited chunk was really retrieved, not that the chunk supports the claim, so a correct answer can still carry a citation that proves nothing. Second, the added document has no fiscal year end in its metadata ("unknown"), because add_document only knows the metadata of the three registered 10-Ks. A new document is searchable, but its citation cannot say which fiscal year it refers to, so the person has to check it.

What this test shows: the system refuses when the information is missing and answers with a citation once the information is added, without changing the code.


## Harness and guardrails

agent.py is a LangChain agent with AGENTS.md as the system prompt, human approval before add_document runs, and a limit of 8 model calls per question. The extra guardrail checks that every citation in the answer refers to a chunk that was really retrieved. It only checks citations written as chunk N, so a citation with a non-numeric id is not checked (seen once in q19 in an earlier run, not in the final run).

AGENTS.md rules. The system prompt has nine rules, each with the reason why it exists:

1. Always call search before answering a factual question and never answer from memory, because the model may remember older filings or invent figures, and analysts act on these numbers.
2. Use only what the retrieved passages say and do not guess numbers, because a wrong figure that looks sourced costs more than no answer.
3. Cite every fact exactly as the search result labels it, only passages that were retrieved, and one chunk per bracket, so that the reader (and the code) can check each claim.
4. For a comparison, search once per company with the company filter, because the three filings use similar wording and one unfiltered search can return passages from only one company.
5. If the passages do not contain the answer, reply exactly "The corpus does not cover this.", because search always returns passages, even irrelevant ones, so refusing has to be a rule. A wrong refusal costs less than a wrong number.
6. Always state the fiscal year (RL ends March 28, 2026; PVH, February 1, 2026; TPR, June 27, 2026), because the year-ends differ.
7. Report what the filings say and never recommend buying or selling or forecast.
8. Use add_document only when the user explicitly asks, because it changes the index and spends embedding quota.
9. Answer in at most five sentences, because short answers are easier to check against their citations.

Approval step. A middleware wraps every tool call. If the tool needs approval (add_document), the harness stops and asks in the terminal: Allow add_document({...})? [y/N]. Only "y" lets the call run. Any other answer returns an error message to the agent saying that the user refused and that it must not try again, so the index is not changed. For the automatic evaluation, approval can be switched off with auto_approve, but the evaluation questions never ask to add a file.

Call limit. ModelCallLimitMiddleware(run_limit=8) stops the agent after 8 model calls in one question. It is a hard stop for loops: for example, in q03 the agent searched again and again without finding the passage and was stopped by this limit.

Extra guardrail: citation check in code. After the agent answers, the code collects every citation the search tool really returned (company, section and chunk number) and compares it with the citations written in the answer. If the answer cites a passage that was never retrieved, the answer is replaced by "Answer withheld: it cites passages that were not retrieved [...]". This is checked in code with a regular expression, not by a model, so it cannot be argued with. Limits: it only checks that a cited chunk was retrieved, not that the chunk supports the claim (see the q26 case above), and it only reads citations written as chunk N, so a citation with another kind of id (seen once in q19 in an earlier run, not in the final run) is not checked.

Did it fire? In the evaluation run of the 31 questions the guardrail never fired: no answer was withheld (0 cases of "Answer withheld" in eval/results.json). So I have no real case where it blocked an answer. It works as a safety net, and the cases it missed are the ones that matter: in an earlier run of q19 the agent cited a chunk with a non-numeric id, which the check does not read, and in q26 (after adding the document) it accepted a citation that was retrieved but did not support the figure.
## Evaluation

Code checks: for answerable questions the agent must search, give at least one valid citation and not refuse; for unanswerable ones it must say "the corpus does not cover this". The judge is gemini-3.5-flash (stronger than the agent, gemini-3.5-flash-lite) and returns grounded, correct and passed. I graded all 31 answers myself in eval/human_labels.csv, with two marks per answer: correct (against the reference answer, or a proper refusal) and supported (every claim appears in the retrieved text), plus a note for each 0.

Results on the 31 questions.

- Code checks: 29 of 31 passed (the two that failed are q03, where the agent hit the call limit without answering, and q29, where the refusal did not use the exact phrase).
- Judge: 29 of 31 passed (q03 and q22 failed).
- Answerable questions: 23 of 25 correct, with 1 unsupported answer.
- Unanswerable questions: 5 of 6 counted as correct refusals, and 0 wrong refusals (the agent never refused a question that had an answer). The sixth, q29, did refuse, but with other words, so the code check did not count it.

Agreement with the judge. We agree on "correct" in 31 of 31 answers (100%) and on "passed" in 31 of 31 (100%). On "supported" we agree in 30 of 31 (96.8%). The only difference is q22: the judge says the answer is grounded in the retrieved passages (generic text about tariff risk), while I marked it as unsupported because it did not contain the figure that answers the question.

Note: text models allow about 20 requests per day, so the judge was run in two days, saving its progress after every verdict.


## Failures

q03: retrieval miss. The chunk with the answer (Item 7, chunk 4) never reached the top 5 results. The agent searched again and again, 8 times, until the call limit stopped it, and it did not find the passage.

q22: wrong answer, and maybe a bad test question. The answer was generic. The figure of 80 basis points is in Item 7, but the agent searched in Item 1A, where it is not. The question may also be too open, so part of the failure may be mine as the author of the test set.

q29: wrong refusal wording. The agent refused, but it did not use the exact phrase "The corpus does not cover this.", so the code check did not count it as a correct refusal.

q19: not a failure in the final run. In an earlier run during development, the agent cited a chunk with an id that is not a number, and the citation check, which only reads chunk N, did not verify it. In the final run, q19 cites normal chunk numbers and passes. I keep it here because it shows a limit of the guardrail.

Counts by cause. Retrieval miss: 2 (q03 and q22; q22 may also be a question that is too open, so part of it could be a bad test question). Wrong refusal: 1 (q29, which refused with the wrong wording). Wrong answer from the right passage: 0. Unsupported claim: 0. Out of 31 questions, 2 had a wrong or missing answer and 1 was a correct refusal that the code check did not count.

Judge's suggested causes against mine. The evaluation script suggests a cause for each failure, and I decide myself. For q22 the judge also says retrieval miss and I agree. For q03 it said "unsupported claim", but the agent did not say anything false: it ran out of model calls, so I classify it as a retrieval miss. For q29 it said "unsupported claim (answered an unanswerable question)", but the agent did refuse, only with other words, so I classify it as a wrong refusal caused by the wording. The judge's own verdict on q29 was that it is a correct refusal, which shows that the judge reads the meaning while the code check reads the exact phrase.

What I would fix first. First q22, because the agent searched in the wrong section (Item 1A, when the 80 basis points are in Item 7) and gave a confident but incomplete answer, which in my use case costs more than no answer. Second q03: the agent could not find the passage and searched 8 times, which is why it was slow and it ended without an answer. I would make it stop after about three failed searches and reply "I don't know", with one short sentence saying which section of the 10-K it probably is in, so the analyst can check by hand.
## Decision

Cost and latency per question (from eval/results.json, 31 questions, agent only): median 2.4 seconds (mean 3.9, slowest 37.1) and median 4,370 tokens (mean 7,324, most expensive 62,541). The mean is above the median because a few questions need several searches, for example the ones that hit the limit of 8 model calls.

Evidence for the decision. 23 of the 25 answerable questions were correct (92%); the two that were not are q03 (no answer, call limit) and q22 (generic answer without the figure). The agent never refused a question that had an answer (0 wrong refusals), and it refused all 6 unanswerable questions, although one of them (q29) did not use the exact phrase. The guardrail never had to withhold an answer in this run.

Decision. In my use case a false figure always costs more than "I don't know", and I would let analysts rely on this system. When I compared my answers with the passages the agent retrieved, most answers were correct and the figures came from the chunks, with the source cited. It gave me the information I wanted, and often more. The answers that failed did so because the agent did not find the right passage, not because it made up data. It would help me in my daily work, which is the kind of job I want to do, and it is safer to use a RAG system that only reads the 10-Ks I give it than to search the whole internet, because the figures are traceable and what is shown to a client is truthful. The limit is that it only covers three companies and three sections of each 10-K.

Safeguards I would add. (1) If the answer was not found as written in the filing and the agent had to deduce or calculate it (for example, computing a percentage from two figures), the answer should say so, so that the analyst knows to check it. If it is found as written, the analyst can trust it. (2) The citation should also say the page of the 10-K, so the analyst can go straight to it and check. Today the citation gives the section and the chunk number, not the page. The two failures and what I would fix first are in the section "Failures".

## AI use


I used Claude for help with code (the evaluation script and helper scripts), for explanations I did not understand, and for spelling corrections of my notes.

I also used Claude to write up this report, in two different ways. For the descriptive parts (corpus, ingestion, tools, harness, evaluation results and the description of the failures), Claude drafted the text from my code and my results, and I reviewed and checked it. For the parts that are my own thinking (the use case, why I chose these companies and sections, my safeguards, what I would fix first and the final decision), I explained my ideas to Claude in my own words in the chat, in Spanish, and Claude translated and rewrote them in professional English. The ideas and the reasoning are mine; Claude only improved the wording.

The test set, my grades and notes, the refusals policy and the decision about whether to trust the system are my own work.
