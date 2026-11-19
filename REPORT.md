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

## Retrieval

*Hit rate at 1/3/5 per design, words added to the prompt, the design you chose.*

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
