# Assignment 3 Report

- **Name**: Julián Consuegra
- **Student ID**: 19376
- **Group**: BBADBA 5A 

## Use case

*Who asks, what they do with the answer, and what a wrong answer costs compared with "I don't know".*

This tool is meant to be used by startup founders that are considering applying for the EIC Accelerator (the EU's funding program for startups and SMEs under its 2027 Work Programme). Since there are many criteria that have to be taken into account in order to assess eligibility, it is of great use to develop this tool to answer questions in relation to this matter. Answers provided will help founders determine if they are eligible for funding, clarify deadlines when completing the application and understand the rules for different funding amounts. It will be a useful tool that aims to answer questions from the official EIC documents that founders can check and act upon. Sometimes the tool will not be sure about the answers to a question. There are two possible outcomes: Confidently giving a wrong answer or directly stating "I don't know". In the first scenario, a wrong answer would probably mean missing important deadlines, misleading founders into believing they are eligible for the grant when they're actually not, or wasting weeks of work in an application that was not valid in the first place. On the other hand, responding with a direct "I don't know" will most likely make the founder double check with an alternative source before taking action. This would represent less of a risk as it is a genuine response that avoids pursuing a plan under uncertain assumptions. Taking this into account, the tool should only answer when the documents support it, and otherwise say it doesn't know. 

## Corpus

*Table: document, URL, date, licence, words.*

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| EIC Work Programme 2027 (Commission Decision C(2026)7629) | [link](https://eic.ec.europa.eu/document/download/ed9ab103-1ffb-4d5f-a6ad-168ac3b36900_en?filename=EIC-2027-Work-Programme.pdf) | 5 Nov 2026 | Commission reuse policy (Decision 2011/833/EU), reuse allowed with source acknowledged | ~75,500 |
| EIC Accelerator Guide for Applicants, v6.0 | [link](https://eic.ec.europa.eu/document/download/9d96fbf3-4d85-4ad0-9483-c77ce348111d_en?filename=EIC%20Accelerator%20guide%20for%20applicants_WP26.pdf) | 19 Nov 2025 | Commission reuse policy (Decision 2011/833/EU), stated in the document | ~8,000 |
| EIC Fund Investment Guidelines (Horizon Europe Compartment) | [link](https://eic.ec.europa.eu/document/download/6df458e7-fa47-4ace-93fa-86099606bdb0_en?filename=EIC_Fund_Investment_2026_guidelines_f.pdf) | Aug 2026 | Commission reuse policy (Decision 2011/833/EU) | ~8,300 |
| **Total** | | | | **~91,800** |

All three are public documents from the official EIC website and contain no personal data. The Guide for Applicants was written for the 2026 Work Programme (it is the latest version available), so some details may not match the 2027 rules.


## Ingestion

*How you extract, clean and chunk; one extraction problem you fixed; chunk metadata; number of chunks.*

Extraction is done page by page from the chosen PDFs with `pypdf`, while keeping the page number. There were certain cleaning steps in order to only maintain necessary information that is of value for the use of the tool. For example, the Guide's repeated page header was removed, lone page numbers and table of contents lines were removed, and pages that had less than 20 words were skipped (covers, blank pages). The chunks are composed of 200 words with a 40-word overlap, never crossing a page. I used a single chunk size on purpose, to stay within the 1,000-embeddings-a-day limit, and compared two search methods instead, since that needs no extra embeddings.

In the process of extraction I faced a problem that might seem simple at first glance but had to be addressed in order to capture the real meaning of words. The PDFs include some words with stray spaces such as "high -risk" and "co -investment" (38 cases in the Work Programme and 9 in the Investment Guidelines). As seen, there is an extra space just before the hyphen and it could end up being interpreted as two separate pieces. For key processes such as keyword search, this can be critical as it may miss matches due to these slight errors. I fixed this in the cleaning step by removing the space before the hyphen, so the search now sees the actual words. 

To maintain traceability and identify sources, each chunk stores its document (source), document title, page number and word count as metadata. Each chunk also gets a unique ID built from the document, page and chunk number, for example `work_programme_2027-p031-c2`. 

Following the specifications of chunk size, word overlap and no page crossing, I ended up with a total of 631 chunks within my index. They are divided into the three documents: 516 Work Programme, 59 Guide, 56 Investment Guidelines. They were then embedded with gemini-embedding-2 at 768 dimensions. 



## Test set

*How you wrote it, counts by kind, two examples.*

I began thinking on basic common questions that a startup founder could come across when evaluating if they can benefit from a grant. Evidently, the questions were formulated in a way that answers come from information available in the corpus. Also, the wording in which questions are asked was something I paid close attention to and worth noting. The documents are filled with official EIC terms that may be complex or unheard of for the common person. Due to this, I decided to generate a mix of questions in which some followed a wording that included EIC terminology but others (8 out of 37) were formulated more naturally and with everyday wording that founders could use so the search is tested with both kinds of wording.

In total there are 37 questions. There are three kinds of test questions: Single (24), multi (7) and unanswerable (6). For the single questions, there is one passage in the corpus that answers them in a simple and concise manner. This is the most basic type and usually the easiest approach the tool has to generate answers. Additionally, the multi questions require two passages for formulating an answer that can be found in different pages or documents. The tool has to find the appropriate passages and combine them, requiring more effort and increased complexity compared to single questions. This can be seen usually when a single page alone can't fully answer the question. Finally, unanswerable questions are ones that can't be answered with the information available in the corpus. These are included in order to assess the capability the tool has to deal with these situations and prevent it from giving false information instead of genuinely responding "I don't know". 

Below are examples of each type of question based on the explanations given above.

1. Single Question (Q12): “What score does my full proposal need to be considered for an interview?” 
**Answer:** 4/5 per criterion and 13/15 overall (WP p85, Guide p21).

2. Multi Question (Q25): “The guide says I need TRL 6, but what TRL level does my innovation actually need to have reached when I apply?”
**TRL: Technology Readiness Level. Scale from 1-9 of how mature a technology is.**

**Answer:** TRL 5 must be fully completed (validation in a relevant environment), which the Guide describes as TRL 6 or above.
**Sources:** Guide p6 (TRL 6 or above) + Work Programme p85 (all aspects of TRL 5 completed).

3. Unanswerable Question (Q36): “What are the EIC Accelerator cut-off dates for 2028?”
**Expected Answer:** The assistant should say it doesn’t know the 2028 dates.
**Sources**: None. The documents only give the 2027 cut-offs.

## Retrieval

*Hit rate at 1/3/5 per design, words added to the prompt, the design you chose.* 

For the retrieval I focused on and tested two designs: vector search and hybrid search. Vector search is the approach in which questions are turned into number embeddings that capture meaning and the search returns chunks within the corpus that have similar embeddings. Words included in the questions may differ to those used in the answers but their captured meaning is similar under this approach. On the other hand, the hybrid search uses both vector search and keyword search. Keyword search ranks chunks within the corpus depending on how many keywords used in the questions match those in the documents. Rarer words count more, so a match including "TRL" will matter more than one with "grant" which is seen everywhere. This is combined with vector search explained above, and the chunks that rank high under either method come first. Both designs use the same 631 chunks, so the comparison needed no extra embeddings. 

Before including the table with results it is important to clarify what hit@k or hit rate represent under my scenario. This metric reflects the share of answerable questions for which a chunk from an expected page appears in the top k results. 

| Design | hit@1 | hit@3 | hit@5 | Words in top 5 |
|---|---|---|---|---|
| A: vector (after fix) | 0.55 | 0.84 | 0.97 | ~790 |
| B: hybrid (after fix) | 0.45 | 0.71 | 0.84 | ~804 |
| A: vector (before fix) | 0.39 | 0.68 | 0.81 | ~790 |
| B: hybrid (before fix) | 0.39 | 0.58 | 0.68 | ~804 |


Overall, the results were positive and the pages which included answer chunks were consistently placed among the top results. Before delving into details, it is worth highlighting the fix I made to my test labels, which explains the difference between the before and after rows of the table. 

Each question has a label which is the page(s) where I initially stated the answer was. However, considering there is some repeated information throughout the different documents, one answer can appear more than once in different pages. The initial problem was that there were 6 specific cases in which the search returned a correct page number which did contain the correct answer, but it was still marked as wrong. This occurred because the page number it returned didn't coincide with the "correct" page number that was initially established without considering the fact that the same information could also be elsewhere. After identifying this problem, the labels were modified in order to take into account the correct pages that were not considered at first. By doing so, these 6 searches are now correctly marked as hits. The fix did not change the search itself, it made the measurement fair: the first numbers underestimated it. Vector search wins both before and after the fix, so the fix does not change my decision. 

The hit rate drastically improves from 1 to 5 but since the agent reads the top 5 chunks, hit@5 will be the most useful and applicable in my case. Using the top 5 chunks adds about 790 words to the prompt for each question. I accepted this cost because going from top 1 to top 5 raises the hit rate from 0.55 to 0.97. Both vector and hybrid hit@5 have high values (0.97 and 0.84) meaning that for 97% (vector) and 84% (hybrid) of the answerable questions, a correct page was among the first 5 results. The same interpretation can be used for the other hit rates. However, considering that the vector search outperformed hybrid at 1, 3 and 5, I decided to choose this approach. Hybrid search most likely did worse because words like "grant", "proposal" and "EIC" appear on almost every page, so the keyword search pulled in many off-topic pages and pushed correct ones down the ranking.

The weak spot is the multi questions. For the 7 multi questions, both needed passages were in the top 5 for only 2 of them (29%). A single search usually finds one half of the answer, so the agent may need to search more than once. 



## Tools and subagent

*Your tools' descriptions, one search result, the subagent's instructions, one transcript from your editor.*

## Adding a document

*What happens when a document is already indexed. The unanswerable question, the document you added, the answer before and after.*

## Harness and guardrails

*Your AGENTS.md rules, the approval step, and your extra guardrail with one case where it fired.*

## Evaluation

*Code checks, the judge's rubric, your agreement with the judge, and results: correct, unsupported, correct refusals, wrong refusals.*

## Failures

*Failed questions by cause, with counts, and what to fix first.*

## Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

## AI use

*What you used and how, or "none".*
