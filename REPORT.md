# Assignment 3 Report

- **Name**:
- **Student ID**:
- **Group**: [BBADBA 5A | BBADBA 5B | PPLEDBA 5A]

## Use case

A sample use case would be myself, Javier Arce. Two and a half years ago I found myself in this exact situation: 20 years old and trying to take my DJ entrepreneurial project to a more serious level. At that moment I had some gigs and was making about 150–200 euros per month. However, as I started scaling my business and getting more clients, I had to formalise my business, and a tool like this would have been great to answer the many questions I had at that time. The tool would be used to decide if it was legally appropriate for me to become an autónomo, and what rights and obligations derived from this. Then, with this information, I could talk to an expert and analyse the economic viability of the operation.

In terms of the correctness of answers, users must know this is a chatbot with a RAG system behind, and that it therefore can make errors. The cost of an error will be highly dependent on what the error is about. If the question is about having to complete the 'Declaración de la Renta', and you are told you are not obliged to do so when you actually are (since 1 January 2023, anyone registered as autónomo at any point in the year must file it, first applied in the 2024 filing campaign), you can receive a fine for this. This specific question falls outside the indexed laws, so the assistant should refuse it, which is exactly the behaviour that matters when errors are costly. However, if the question is about what a mutua does or does not cover, the economic implications are less directly tied and probably less serious. Overall, I would say the cost of errors is relatively high, as it can have economic and legal implications for users if they do not make the right decisions.

## Corpus

*Table: document, URL, date, licence, words.*

## Ingestion

*How you extract, clean and chunk; one extraction problem you fixed; chunk metadata; number of chunks.*

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
