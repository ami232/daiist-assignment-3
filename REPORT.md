# Assignment 3 Report

- **Name**:
- **Student ID**:
- **Group**: [BBADBA 5A | BBADBA 5B | PPLEDBA 5A]

## Use case

Target users are patients or laypeople seeking general understanding of FDA prescribing information for common oral medicines. The wrong result can lead to unsafe personal dosing or ignored interaction/contraindication warnings, so “I don't know” is preferable to unsupported medical advice. The system is for label lookup and education, not diagnosis or individualized treatment.

## Corpus

Selected drugs: amoxicillin, lisinopril, metformin, atorvastatin, and levothyroxine. The committed corpus contains five FDA/openFDA label text files totaling 63,605 whitespace-separated words. Source: https://api.fda.gov/drug/label.json — openFDA drug-label data; licence: CC0.

| Document | URL | Licence | Filename |
|---|---|---|---|
| Amoxicillin label | https://api.fda.gov/drug/label.json | CC0 | amoxicillin-0e877b33-af19-d857-e063-6394a90a08ea.txt |
| Atorvastatin label | https://api.fda.gov/drug/label.json | CC0 | atorvastatin-05b0f170-ac97-4a83-b03a-659a4b493ee2.txt |
| Levothyroxine label | https://api.fda.gov/drug/label.json | CC0 | levothyroxine-0235176b-ec39-44c4-a9e1-e0729a7989fa.txt |
| Lisinopril label | https://api.fda.gov/drug/label.json | CC0 | lisinopril-03a22769-c7ac-496c-80c4-98f76c371987.txt |
| Metformin label | https://api.fda.gov/drug/label.json | CC0 | metformin-19e4bfb8-2ed1-4a6b-adf5-853ad2953362.txt |

## Ingestion

Labels were downloaded from openFDA and converted to text with `## Section` headings. Two designs are implemented: section-aware chunks up to 220 words with `[Drug | Section]` prefixes, and fixed 150-word windows with 30-word overlap (implemented with 120-word stride). Chunk IDs include the document content hash and design. The clean corpus has five documents and 63,605 words; it produced 166 section chunks and 531 fixed chunks. The index is about 15.8 MB. An extraction issue was corrected by retaining section headings and adding explicit source/location metadata instead of relying on raw HTML-only text.

## Test set

The draft test set has 30 questions: 20 single, 5 multi-passage, and 5 unanswerable. It is grounded in the five label texts. Two examples: amoxicillin adult dosing, and lisinopril dosing plus monitoring after myocardial infarction. Student review is still required before human grading and report conclusions.

## Retrieval

Quota-safe lexical retrieval over the committed collections measured hit-rate@1/3/5 as: section 52%/68%/80%, fixed 56%/60%/60%, on 25 answerable questions. Section was stronger at k=3 and k=5; fixed was 4 percentage points higher at k=1. Gemini query-embedding hit rates could not be run because the embedding request quota was exhausted. Section is currently the MCP default, but final design selection should consider the complete intended metric and remain an explicit student decision.

## Tools and subagent

The MCP server was verified by `check.py`: `search(query)` and `add_document(path)` are discoverable with required string arguments. The subagent configuration is restricted to search. The editor session could not establish the MCP tool and therefore did not produce a usable real transcript.

## Evaluation

The test set has 30 rows: 20 single, 5 multi, and 5 unanswerable. The human-label file has 20 placeholders and must be graded before agreement is calculated. End-to-end evaluation could not complete in this session because repeated 30-question agent calls exceeded practical latency and API limits; no correctness or judge numbers are fabricated here.

## Failures

Do not infer failure counts until evaluation output is generated. Candidate classifications are retrieval miss, wrong answer from the right passage, unsupported claim, wrong refusal, and bad test question.

## Decision

The system should not yet be approved for unsupervised patient reliance. It may be useful as a cited evidence lookup with pharmacist/clinician review, but evaluation and human grading are incomplete.

## Cost and latency

The standard `main.py ask` check completed in 137–138 seconds in successful runs. Embedding hit per-minute and daily quota limits. A 30-question evaluation is not practically complete under the current free-tier limits without quota reset or a new project/key.

## AI use

AI coding assistance was used to implement and debug the Python pipeline, MCP server, agent, evaluation stage, test-set draft, and report scaffolding. Student decisions—test-set review, human grades, chunk-design choice, failure analysis, and ship decision—remain to be completed and reported honestly.
