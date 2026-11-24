# Assignment 3 Report

- **Name**: Deniz Meten
- **Student ID**: 18758
- **Group**: BBADBA 5A

## Use case

I built a RAG assistant for commercial drone operators working under FAA Part 107 rules in the United States.

The main user is a remote pilot or small commercial drone operator preparing for a flight. The system is meant to save time when checking things such as operating limits, airspace, night operations, operations over people, certification, weather, waivers and preflight responsibilities.

A wrong answer matters because bad aviation or compliance advice can lead to an unsafe operation or a rule violation. For that reason I prefer the assistant to say **"I don't know from the indexed FAA corpus"** instead of guessing. I would use the system as a document and decision-support assistant, not as a replacement for current FAA rules, ATC authorization or the original source documents.

## Corpus

The initial corpus contains four official FAA documents related to small-UAS / Part 107 operations.

| Document | URL | Date | Licence / reuse basis | Words |
|---|---|---|---|---:|
| FAA AC 107-2A - Small Unmanned Aircraft System (Small UAS) | https://www.faa.gov/documentlibrary/media/advisory_circular/ac_107-2a.pdf | 2021-02-01 | FAA advisory circular; FAA states advisory circulars may be reproduced in whole or in part without FAA permission. | 39,210 |
| FAA Remote Pilot - Small Unmanned Aircraft Systems Study Guide (FAA-G-8082-22) | https://www.faa.gov/sites/faa.gov/files/regulations_policies/handbooks_manuals/aviation/remote_pilot_study_guide.pdf | 2016-08 | Official U.S. federal government publication. U.S. Government works are generally not protected by U.S. copyright under 17 U.S.C. 105; source attribution is retained and third-party material, if any, is not separately reproduced. | 24,636 |
| FAA Remote Pilot - Small Unmanned Aircraft Systems Airman Certification Standards (FAA-S-ACS-10B) | https://www.faa.gov/training_testing/testing/acs/uas_acs.pdf | 2021-04 | Official U.S. federal government publication. U.S. Government works are generally not protected by U.S. copyright under 17 U.S.C. 105; source attribution is retained and third-party material, if any, is not separately reproduced. | 5,954 |
| FAA Final Rule - Operation of Small Unmanned Aircraft Systems Over People | https://www.faa.gov/sites/faa.gov/files/2021-08/OOP_Final%20Rule.pdf | 2021-01-15 | U.S. federal agency rulemaking document; U.S. Government works are generally not protected by U.S. copyright under 17 U.S.C. 105. | 79,661 |

**Total extracted words: 149,461.**

The corpus is comfortably above the 50,000-word requirement. The source URLs, dates, hashes and extracted word counts are stored in `index/manifest.json`.

## Ingestion

The ingestion pipeline is in `index.py`. It downloads the configured FAA PDFs into the git-ignored `corpus/` folder, extracts them page by page with `pypdf`, cleans the text and keeps the PDF page number as location metadata.

One extraction issue was PDF formatting noise. Raw extraction contained soft hyphens, words split across line breaks, standalone page numbers and lots of artificial line wrapping. I fixed this by removing soft hyphens, joining words broken across lines, normalizing whitespace and dropping standalone page-number noise. I still kept page boundaries so the final citations remain easy to check.

The final chunking design is **page_500**: about **500 words per chunk with 80 words of overlap**, and chunks do not cross PDF-page boundaries. Each chunk stores the document ID, title, URL, date, PDF page, file hash, word count and text.

The initial corpus produced **535 searchable chunks**. Gemini `gemini-embedding-2` created the vectors. The vector cache is saved incrementally, so if indexing is interrupted it continues from already saved vectors rather than embedding everything again.

## Test set

The final test set contains **35 questions**:

- **24 single-passage**
- **6 multi-passage**
- **5 unanswerable**

I kept the questions fairly direct and practical because that is closer to how an actual drone operator would ask them. The unanswerable questions are still close to the topic, so the assistant has to recognize that the corpus is missing the answer rather than just rejecting something obviously unrelated.

Two examples:

- **Single:** What do I need to be allowed to fly a drone at night under Part 107?
- **Multi:** If I want to fly at night in controlled airspace, what different requirements do I need to check first?

The full answer key is in `eval/questions.csv`, including expected source/location information and short reference answers.

## Retrieval

I compared two retrieval designs using the same saved chunk embeddings:

1. **Dense** semantic similarity.
2. **Hybrid** retrieval combining semantic and lexical/BM25-style ranking.

| Design | Hit@1 | Hit@3 | Hit@5 | Mean prompt words @5 |
|---|---:|---:|---:|---:|
| dense | 0.533 | 0.867 | 0.933 | 1393.9 |
| hybrid | 0.467 | 0.600 | 0.633 | 1599.1 |

I chose **dense retrieval**. It was better at every hit-rate level and also used a smaller prompt. The biggest difference was at Hit@5: dense reached **93.3%**, compared with **63.3%** for hybrid. Dense also used about **1394** prompt words at k=5 compared with about **1599** for hybrid.

## Tools and subagent

`server.py` exposes two MCP tools:

- **`search(query)`** searches the committed index and returns relevant chunks with source, PDF page, similarity score and a citation label.
- **`add_document(path)`** runs a local document through the same ingestion pipeline and adds it to the index.

For duplicates, the add-document pipeline checks the file SHA-256. If the same bytes are already indexed it returns `already_indexed` and does not embed the document again.

The project also contains `.claude/agents/drone-compliance-researcher.md`. The subagent is restricted to the corpus search tool and is instructed to answer only from retrieved evidence and cite its claims.

### Real subagent transcript

#### Subagent transcript

Search Tools

search
Completed with input: {
  "query": "night operations small UAS Part 107 requirements anti-collision light civil twilight remote pilot recurrent training"
}

search
Completed with input: {
  "query": "14 CFR 107.29 night civil twilight definition 107.65 knowledge test recurrent training 107.205 waiver night anti-collision lighting"
}

search
Completed with input: {
  "query": "civil twilight definition 107.29 sunset sunrise official Part 107"
}

search
Completed with input: {
  "query": "107.205 waiver anti-collision lighting night operations waiverable 107.29"
}

Under 14 CFR § 107.29:

- **Night** means the period between the end of evening civil twilight and the beginning of morning civil twilight, according to the Air Almanac. In the continental U.S., this follows the 30-minute civil-twilight periods around sunrise and sunset. [FAA:ac-107-2a|PDF page 22]
- The small UAS must have **anti-collision lighting visible for at least 3 statute miles**, with a sufficient flash rate to avoid collision. The remote pilot may reduce intensity for safety but may not extinguish the lights. [FAA:operations-over-people-final-rule|PDF page 267]
- The remote pilot in command must complete the applicable **initial knowledge test or training under § 107.65** covering night operations. A certificated remote pilot receives night privileges through that test or recurrent training. [FAA:operations-over-people-final-rule|PDF page 267] [FAA:ac-107-2a|PDF page 22]
- Recurrent training or knowledge-testing requirements generally apply within **24 calendar months** to retain certificate privileges. [FAA:ac-107-2a|PDF page 39]
- During civil twilight, anti-collision lighting is required even when the aircraft is not operating during the formal “night” period. [FAA:operations-over-people-final-rule|PDF page 267]
- The anti-collision-lighting requirements in § 107.29(a)(2) and (b) are eligible for a Part 107 waiver under § 107.205, subject to an applicant demonstrating adequate safety mitigations. [FAA:operations-over-people-final-rule|PDF page 291] [FAA:operations-over-people-final-rule|PDF page 172]

The time definition and operating instructions in AC 107-2A are advisory guidance; the § 107.29 requirements are the regulatory requirements. [FAA:ac-107-2a|PDF page 22] [FAA:operations-over-people-final-rule|PDF page 267]

## Adding a document

I used this originally unanswerable question:

> **If FAA airspace rules allow the flight, can I automatically fly inside a U.S. national park?**

**Before adding a document**, the assistant answered:

> "I don't know from the indexed FAA corpus. The indexed FAA corpus does not contain information regarding U.S. National Park rules or land-management restrictions governing the operation of small unmanned aircraft systems."

I then downloaded the official National Park Service **Reference Manual 60, Chapter 12 – Uncrewed Aircraft Systems** and added it through the `add_document` tool. The harness asked me to approve the tool action before it was allowed to modify the index.

The added document was stored as `added-cbdbd2b4dc2f`, with **4066 extracted words** and **12 chunks**.

**After adding the document**, the same question became answerable. The assistant explained that FAA airspace permission by itself does not automatically authorize launching, landing or operating a drone on National Park Service lands, and cited the newly added NPS document (PDF page 3).

This shows that the add-document pipeline changed the knowledge available to the RAG without rebuilding the original corpus.

## Harness and guardrails

`agent.py` uses LangChain with Gemini and calls the corpus tools over MCP. `AGENTS.md` contains the system rules.

The main safeguards are:

1. **Approval before add-document.** If the agent wants to add a document, the terminal shows the path and asks for `y/n` approval before the tool runs.
2. **Maximum of five tool calls per run.** This prevents uncontrolled search loops and unnecessary API usage.
3. **Citation-integrity guardrail.** Factual answers must contain corpus citations, and the citations must match evidence returned by search. If the first draft uses malformed or unsupported citation labels, the harness tries to repair the draft using the exact allowed labels instead of simply returning the unsupported answer.
4. **Corpus-limited refusal.** If the retrieved evidence is not enough, the system is instructed to refuse rather than fill the gap from outside knowledge.

A real guardrail case happened during testing on the night-operation question. The model initially produced citation labels that did not exactly match the labels returned by search, so the citation-integrity guardrail blocked the draft. I then changed the harness to normalize citation formatting and automatically retry with the allowed labels. In the final evaluation the guardrail fired on **2.9%** of questions.

## Evaluation

The final evaluation ran the agent on all **35 questions**. Code checked retrieval, citation validity, refusals, token usage and latency. A Gemini judge then graded correctness and support against the reference answer and retrieved evidence.

The judge rubric was strict:

- `correct = 1` if the answer was materially correct against the reference answer.
- `supported = 1` only if substantive factual claims were supported by retrieved evidence.
- for unanswerable questions, a clear corpus-limited refusal counted as correct.
- the judge was told not to use outside knowledge.

Final results:

- **Judge correctness: 97.1%**
- **Judge support: 97.1%**
- **Code-level valid citation rate: 71.4%**
- **Correct refusal rate: 60.0% of unanswerable questions**
- **Wrong refusal rate: 3.3% of answerable questions**
- **Mean agent time: 19.0 seconds per question**
- **Mean total tokens: 6027 tokens per question**

I completed **20 manual labels before viewing the final judge results**. Human/judge agreement was:

- **Correctness agreement: 100.0%**
- **Support agreement: 100.0%**
- **Joint agreement: 100.0%**

One thing I noticed is that the code-level citation rate (**71.4%**) is lower than the semantic judge support rate (**97.1%**). The code checker is stricter: harmless formatting differences or extra citation labels can be classified as citation/unsupported-claim failures even when the actual statement is supported by the retrieved passage. This was also the main issue I had to debug during development.

## Failures

The final failure classifier produced:

- **pass: 23**
- **unsupported claim: 9** (examples: q07, q11, q13, q16)
- **retrieval miss: 2** (examples: q25, q29)
- **wrong refusal: 1** (examples: q26)

The first thing I would improve is **citation handling**, because most of the non-pass cases were classified as unsupported claims even though overall judge support was very high. I would make citation rendering fully deterministic instead of letting the language model decide the final citation format.

The next priority would be the two retrieval misses. Dense retrieval was already much stronger than hybrid, but a reranker or better section-aware metadata could help those remaining cases.

The wrong refusal shows why the refusal threshold also needs to stay conservative but not too aggressive. The system should prefer a safe refusal when evidence is genuinely missing, but it should not refuse an answerable question just because one retrieval result is slightly weak.

## Decision

I **would let users use this system as a preflight / compliance lookup assistant, but I would not let them rely on it as the only authority for a real flight decision**.

The evaluation is strong enough for decision support: correctness and support were both **97.1% / 97.1%**, dense Hit@5 was **93.3%**, and human/judge agreement was **100.0%**.

My main safeguard would be to always show the original source/page citation and require the user to verify the official FAA/NPS source for any high-risk or unusual operation. If the evidence is missing or unclear, the assistant should refuse instead of guessing.

Operationally, one question used about **6027 tokens** and took about **19.0 seconds** on average.

## AI use

I used generative AI to help with code structure, debugging, MCP/LangChain integration, evaluation code, formatting and report drafting. AI also helped brainstorm and format candidate evaluation questions in my normal writing style, which I reviewed and approved before running the evaluation.

I manually entered the 20 human labels before viewing the final judge results. During development I also used AI to discuss the interpretation of some model answers while I was doing the manual review.

The final project decisions — use case, choosing dense retrieval after reviewing the metrics, refusal policy, safeguards and the final decision on how the system should be used — were reviewed and accepted by me.
