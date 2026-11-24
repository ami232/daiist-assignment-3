# Assignment 3 Report

- **Name**: Deniz Meten
- **Student ID**: 18758
- **Group**: BBADBA 5A

## Use case

For this project, I am building a RAG assistant for commercial drone operators flying under FAA Part 107 rules in the United States.

The main user would be a remote pilot or small commercial drone operator preparing for a flight. They could ask questions about things such as operational limits, night operations, flying over people, Remote ID, pilot certification, airspace requirements, waivers and preflight responsibilities.

The purpose of the system is to help the user find answers from official FAA documents instead of searching through long manuals manually.

A wrong answer matters because incorrect aviation or compliance advice could lead to an unsafe flight, a rule violation, or an operation being carried out without the correct authorization. Because of this, I would rather the system say that it does not know or that the available documents do not contain enough information than give an unsupported answer.

## Corpus

The planned corpus will use official FAA documents related to commercial small-drone operations.

| Document | Source | Role in the corpus | Words |
|---|---|---|---:|
| FAA AC 107-2A – Small Unmanned Aircraft System (Small UAS) | FAA | Main Part 107 operational guidance | To be measured during ingestion |
| FAA Remote Pilot – Small Unmanned Aircraft Systems Study Guide | FAA | Pilot knowledge, weather, airspace and operating rules | To be measured during ingestion |
| FAA Remote Pilot – Small Unmanned Aircraft Systems Airman Certification Standards | FAA | Required pilot knowledge and certification standards | To be measured during ingestion |
| FAA Final Rule – Operation of Small Unmanned Aircraft Systems Over People | FAA | Rules concerning operations over people and night operations | To be measured during ingestion |

The documents are being selected because they are official FAA sources and directly relate to the decisions a commercial drone operator may need to make.

The final corpus will contain at least three documents and more than 50,000 words in total, as required by the assignment. Exact word counts, document dates, URLs and licence/reuse information will be recorded after the documents are downloaded and processed.

## Ingestion

*To be completed after the corpus is downloaded and indexed. This section will explain text extraction, cleaning, chunking, metadata, the number of chunks and any extraction problem that had to be fixed.*

## Test set

*To be completed after the corpus is indexed. The final test set will contain at least 30 questions, including at least 5 multi-passage questions and at least 5 questions that cannot be answered from the corpus.*

## Retrieval

*To be completed after testing at least two retrieval designs. Hit rate at k = 1, 3 and 5 will be compared before choosing the final design.*

## Tools and subagent

*To be completed after the MCP search and add-document tools and the Claude/Copilot subagent are implemented.*

## Adding a document

*To be completed after testing the add-document tool and the before/after unanswerable-question experiment.*

## Harness and guardrails

The agent will be designed to answer only from retrieved FAA evidence and provide citations for factual claims.

The add-document tool will require user approval before it can modify the index.

The planned additional guardrail is that the agent should refuse to give a factual answer when the retrieved evidence is not sufficient to support it. This is important for this use case because an unsupported answer about drone operations could be more harmful than saying that the corpus does not contain enough information.

*The final implementation and an example of the guardrail firing will be added after testing.*

## Evaluation

*To be completed after running the full evaluation. This will include citation checks, refusals, LLM-judge results and my own manual grading of at least 20 answers.*

## Failures

*To be completed after evaluation. Failures will be classified as retrieval miss, wrong answer from the right passage, unsupported claim, wrong refusal or bad test question.*

## Decision

*To be completed after evaluation. The final decision will state whether I would allow users to rely on the system, for which types of questions, with what safeguards, and the measured cost and latency per question.*

## AI use

Generative AI is being used to assist with code structure, debugging, implementation of the RAG pipeline, MCP integration and formatting.

The project decisions required by the assignment, including the use case, retrieval design, refusal behaviour, test questions, human evaluation and final ship decision, will be reviewed and decided by me.
