# Assignment 3 Report

- **Name**: Jaime Fernandez Redondo
- **Student ID**: 18632
- **Group**: BBADBA 5A

## Use case

An assistant that answers questions about US aviation rules (14 CFR) for drone pilots and general-aviation pilots. For example: how high can a drone fly, what lights does it need at night, what are the VFR weather minimums. People act on these answers, so a wrong "yes, that is allowed" can mean a fine or an accident. A wrong "I don't know" only costs one more lookup. So the assistant must cite the section for every claim and should refuse rather than guess.

## Corpus

Source: the eCFR website (`ecfr.gov`), Title 14, version of 2026-11-01. US federal regulations are public domain (17 U.S.C. § 105). No personal data.

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| 14 CFR Part 107 (small drones) | https://www.ecfr.gov/current/title-14/part-107 | 2026-11-01 | Public domain | 9,033 |
| 14 CFR Part 48 (drone registration) | https://www.ecfr.gov/current/title-14/part-48 | 2026-11-01 | Public domain | 2,403 |
| 14 CFR Part 89 (Remote ID) | https://www.ecfr.gov/current/title-14/part-89 | 2026-11-01 | Public domain | 7,042 |
| 14 CFR Part 101 (model aircraft, balloons) | https://www.ecfr.gov/current/title-14/part-101 | 2026-11-01 | Public domain | 2,687 |
| 14 CFR Part 67 (medical standards) | https://www.ecfr.gov/current/title-14/part-67 | 2026-11-01 | Public domain | 6,588 |
| 14 CFR Part 91 Subpart A (general) | https://www.ecfr.gov/current/title-14/part-91/subpart-A | 2026-11-01 | Public domain | 2,479 |
| 14 CFR Part 91 Subpart B (flight rules) | https://www.ecfr.gov/current/title-14/part-91/subpart-B | 2026-11-01 | Public domain | 19,547 |
| 14 CFR Part 91 Subpart C (equipment) | https://www.ecfr.gov/current/title-14/part-91/subpart-C | 2026-11-01 | Public domain | 8,284 |
| 14 CFR Part 91 Subpart D (special operations) | https://www.ecfr.gov/current/title-14/part-91/subpart-D | 2026-11-01 | Public domain | 6,606 |
| **Total** | | | | **64,669** |

The downloaded XML files (`corpus/`) are not committed to the repo. `main.py index` downloads them again from the eCFR API.

## Ingestion

`main.py index` downloads each part as XML and cuts it into chunks. One chunk is one regulation section. If a section is longer than 200 words, it is split at paragraph breaks and the title is repeated in each piece. Each chunk stores its `source` (for example "14 CFR Part 107"), its `location` (for example "§ 107.51") and an `id`. This gives **461 chunks**. Each chunk is turned into a vector with `gemini-embedding-001` and saved in `index/chunks.jsonl`.

Problems I had:
- **Fixed:** the first version found 0 chunks, because the XML marks sections as `SECTION` in capitals and my filter looked for lowercase.
- **Fixed:** with the model `gemini-embedding-2`, 32 texts came back as one single vector, so only 22 lines were saved instead of 461. I changed to `gemini-embedding-001` and added a check that stops the program if the number of vectors is wrong.
- **Not fixed:** the chunker ignores tables. 8 sections have tables (§§ 67.105, 67.205, 67.305, 91.121, 91.125, 91.155, 91.175, 91.220), and that content is missing from the index. This caused one failure (q18).

## Test set

33 questions in `eval/questions.csv`: 21 single-passage, 6 multi-passage (two sections needed) and 6 unanswerable (the answer is not in the corpus, for example about Part 61 or Part 117). I created the questions of the test set. Each has a reference answer taken from the section.

Examples:
- Single (q01): "What is the maximum altitude a small drone can fly under Part 107?" Expected section: § 107.51.
- Multi (q22): "I want to fly my registered small drone at night. What lighting do I need, and do I also need Remote ID?" Expected sections: § 107.29 and § 89.105.

## Retrieval

I compared three ways of searching over the same chunks. "hit@k" is the share of the 27 answerable questions where the right section is in the top k results.

| Design | hit@1 | hit@3 | hit@5 | Words sent to the model (k=5) |
|---|---|---|---|---|
| vector | 0.704 | 0.963 | **1.000** | 711 |
| bm25 (keywords) | 0.444 | 0.630 | 0.704 | 731 |
| hybrid (both) | 0.556 | 0.778 | 0.889 | 764 |

I chose **vector search**. It is the best at every k and costs about the same in words. Users ask in plain language while the regulations use legal wording, which suits vectors better than keywords. One limit: a "hit" only checks the section, not whether the needed text is inside it. q18 counted as a hit even though the table with the answer was missing.

## Tools and subagent

The MCP server (`server.py`) has two tools. The tool descriptions are the docstrings in the file:
- `search(query)`: "Search the aviation regulations corpus: US Federal Aviation Regulations (14 CFR) on small drones (...), airman medical standards (Part 67) and general operating and flight rules for aircraft (Part 91 subparts A-D). Use it for any question about what the rules require, allow or prohibit; never answer such questions from memory. (...) Returns up to 5 passages, best first, each as '[n] <document> — <section>' followed by the exact regulation text. Cite the section number of every claim you take from a passage. If nothing relevant comes back, the corpus does not cover the question."
- `add_document(path)`: "Add a document to the search index so that search can find it. Takes the local file path of an .xml (eCFR section format), .pdf, .txt, .md or .html document. (...) Chunks already in the index are skipped, so adding the same file twice changes nothing. (...) This changes the shared index: use it only when the user asks to add a document."

Example search result for "What is the maximum altitude a small drone can fly under Part 107?":

```
[1] 14 CFR Part 107 — § 107.51
§ 107.51 Operating limitations for small unmanned aircraft.
A remote pilot in command and the person manipulating the flight controls ...
```

The subagent is in `.claude/agents/corpus-researcher.md`. It can only use `mcp__corpus__search`. It runs one search per rule it needs (at most 4), answers only from the results, cites every claim, says "The corpus does not cover this" when needed, and ends with a `Searches:` line.

Transcript from Claude Code in VS Code (the main agent passed the question to `corpus-researcher`, which answered; shortened).

Question: "What are the remote pilot certification requirements under 14 CFR Part 107?"

The subagent ran 3 searches with `mcp__corpus__search`:
1. "remote pilot certificate eligibility"
2. "aeronautical knowledge test remote pilot"
3. "remote pilot certificate required to operate small unmanned aircraft"

Its answer, with a citation for every claim:
- A remote pilot certificate with a small UAS rating is needed to act as remote pilot in command [14 CFR Part 107, § 107.12].
- To get one you must be at least 16, read, speak, write and understand English, have no condition that would interfere with safe operation, and either pass the initial knowledge test or hold a Part 61 certificate with § 107.74 training [14 CFR Part 107, § 107.61].
- The test covers regulations, airspace, weather, emergency procedures, night operation and more [14 CFR Part 107, § 107.73]. You need photo ID [§ 107.67]. Cheating bars you for 1 year [§ 107.69].
- You apply in the form the Administrator accepts [§ 107.63] and must stay current every 24 calendar months [§ 107.65].
- It listed what the corpus did not return: §§ 107.57 and 107.59 (which § 107.61 depends on), the § 107.74 topics, the second half of § 107.63 and § 61.56.
- It ended with: `Searches: "remote pilot certificate eligibility"; "aeronautical knowledge test remote pilot"; "remote pilot certificate required to operate small unmanned aircraft"` and listed the sections returned (Part 107: §§ 107.12, 107.19, 107.56, 107.61, 107.63 (part 1/2), 107.65, 107.67, 107.69, 107.73, 107.140 (part 1/4); also § 48.20 and § 67.301, not relevant).

What worked: it used several searches, cited a section for each claim and said what it could not find instead of filling the gaps. What I noticed: the main agent shortened the subagent's answer and dropped the `Searches:` line when passing it on, so the line is only in the subagent's own output.

## Adding a document

Each chunk has an `id` made from its source, location and text. `add_document` skips chunks whose id already exists, so adding the same file twice adds nothing.

Test: I called `add_document` on a file that is already indexed (`corpus/part48.xml`):

```
$ uv run python -c "import server; print(server.add_document('corpus/part48.xml'))"
corpus server: 461 chunks loaded
part48.xml was already indexed: 18 chunks found, 0 added.
```

Nothing was added and the index stayed at 461 chunks.

Experiment:
- **Question (q33):** "How often must a pilot complete a flight review under § 61.56?" Part 61 is not in the corpus.
- **Before:** the agent said "The corpus does not cover this". This is a correct refusal.
- **Document added:** § 61.56 from eCFR (public domain), file `extra_docs/14 CFR Part 61.xml`. It became 4 chunks, so the index went from 461 to 465.
- **After:** the agent answered with the 24-calendar-month rule and cited `[14 CFR Part 61, § 61.56(c)]`.
- **Note:** my first attempt through the agent did not work: the file was not yet in `extra_docs/`, so nothing was added. I then added it by calling `add_document` directly. Afterwards I restored the index to 461 chunks so it matches the evaluation results.

## Harness and guardrails

The agent (`agent.py`) uses `gemini-3.5-flash` with `AGENTS.md` as its instructions. The 8 rules in `AGENTS.md`, each with a reason:
1. Search before answering, because memory cannot be cited.
2. Answer only from the search results, because an unsupported claim looks as reliable as a supported one.
3. Cite every claim like `[14 CFR Part 107, § 107.31]`.
4. If the first search is not enough, search again with other words (at most 3 searches).
5. Say "The corpus does not cover this" instead of filling gaps.
6. No legal advice about a specific case.
7. Never add documents on its own.
8. Be brief and reply in the language of the question.

Controls in code:
- **Approval:** `add_document` runs only after I type `y` at `Approve? [y/N]`. Without a terminal it is denied, and `evaluate.py` always denies it.
- **Limits:** at most 6 tool calls per question.
- **Citation guardrail:** every section cited in the answer must appear in the retrieved passages. An answer given without any search is replaced by a refusal.

When it fired: in the add-document experiment. The agent called `add_document` without searching, so the guardrail hid its reply. This was a false positive: the guardrail cannot tell a regulation question from a request to add a document. It did not fire during the 33 evaluation questions. Weakness: it accepts a section if its number appears anywhere in the retrieved text, even only as a mention inside another section. That is why it did not catch q05.

## Evaluation

Agent: `gemini-3.5-flash`, vector search. Judge: `gemini-3.5-flash-lite`.

Automatic checks on the 33 questions: all citations valid (33 of 33), guardrail fired 0 times, **6 of 6 unanswerable questions refused correctly**, **1 wrong refusal** (q18).

The judge gets the question, the reference answer, the agent's answer and the retrieved passages, and gives two 1/0 scores:
- `correct`: agrees with the reference on every important point (numbers, conditions, exceptions). For unanswerable questions: 1 only if the agent says the corpus does not cover it.
- `supported`: every claim in the answer appears in the retrieved passages.

Judge result: correct 33 of 33, unsupported 0.

I graded 20 answers by hand (q01 to q18, q20, q21) before looking at the judge. All 20 are single-passage questions, so the multi-passage and unanswerable answers have no human grade. I gave `correct = 0` to q03, q11 and q18, and `supported = 0` to q05, q14 and q16. Agreement with the judge is **0.85 for `correct` and 0.85 for `supported`** (17 of 20 each). The judge missed all six problems, so it is too lenient to trust on its own.

| | Judge | My grades (20 answers) |
|---|---|---|
| correct | 33 of 33 | 17 of 20 |
| unsupported | 0 | 3 of 20 |
| correct refusals | 6 of 6 | not graded |
| wrong refusals | 1 (counted by code) | 1 (q18) |

## Failures

6 of my 20 graded answers had a problem:

| Question | What went wrong | Cause |
|---|---|---|
| q03 | Left out the knowledge test / training requirement from the reference answer | Right passage retrieved, answer incomplete |
| q11 | Left out some of the extra launch limits in § 101.33 | Right passage retrieved, answer incomplete |
| q05 | Described operations over people in Categories 1 to 4, but those sections were not retrieved | Unsupported claim; guardrail missed it (sections only mentioned in another passage) |
| q14 | Added §§ 67.115 and 67.401, which were not retrieved | Unsupported claim |
| q16 | Added exceptions for powered parachutes and weight-shift aircraft that were not retrieved | Unsupported claim |
| q18 | Refused a question that has an answer | Ingestion: the § 91.155 table was missing from the index |

By cause: 2 incomplete answers, 3 unsupported claims, 1 ingestion failure. None were retrieval misses at section level. I only graded 20 of 33 answers, so this is not a failure rate for the whole set.

What to fix first:
1. **Ingest tables** (8 sections) and rebuild the index. It is the cheapest fix and removes the failure that was not the model's fault.
2. **Stricter citation check:** accept a section only if it is the header of a retrieved passage. This would have caught q05 and q14.
3. **Better judge:** a stronger model, or a checklist of conditions from the reference answer, because the current judge found none of the six problems.

I did not apply these fixes, so that the committed index matches the evaluated results.

## Decision

I would **not** let users rely on it as their only source. It works well as a search aid: the right section was in the top 5 for every answerable question, and it refused all six questions outside the corpus. But in 6 of my 20 graded answers it left something out, added an unsupported claim, or was missing data, and the automatic judge noticed none of them. When a missing condition can cost a certificate or cause an accident, that is too risky. Before real use I would require: showing the retrieved passages next to every answer, checking citations against passage headers, regular human grading, and fixing the table ingestion.

Cost and speed per question (average over 33): 5,271 input tokens, 1,054 output tokens, 84.8 seconds. The time includes waiting for free-tier rate limits. I used the free tier, so I paid nothing.

## AI use

I used Claude (Anthropic) throughout this assignment as a coding and development assistant. Claude generated the first versions of index.py, the MCP server, the agent, the evaluation script, AGENTS.md, and the subagent instructions. It also helped me debug technical issues, including API rate limits, embedding errors, and overloaded models.

I used Claude Code in the VS Code terminal to run the corpus-researcher subagent against the MCP server. At my request, Claude Code also enabled the corpus server in my local Claude settings file (.claude/settings.local.json).

I ran the system using my own API key. I made the project decisions, including the use case, chunking strategy, system design choices, refusal behaviour, evaluation criteria, and final ship decision. I created the test set, manually graded all 20 answers before examining the judge's results, investigated the causes of failures, and conducted the add-document experiment. The analysis and conclusions in this report are my own.

Within the implemented system, Gemini models were used for the agent (gemini-3.5-flash), the judge (gemini-3.5-flash-lite), and embeddings (gemini-embedding-001).