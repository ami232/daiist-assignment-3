# Assignment 3 Report

- **Name**: Emanuel Cohen-Henriquez
- **Student ID**: 18761
- **Group**: BBADBA 5B

## Use case

A student pilot preparing for the FAA private-pilot knowledge test asks about
weather, airspace, aircraft performance, navigation, and aeromedical factors.
An answer may also influence real-flight decisions, where a confident error is
more costly than an explicit refusal. The assistant therefore cites handbook
passages and refuses when the indexed material does not answer the question.

## Corpus

The corpus is the FAA's 2023 *Pilot's Handbook of Aeronautical Knowledge*,
a U.S. Government work in the public domain (17 U.S.C. 105). The seven indexed
chapters contain 97,550 words.

| Document | FAA source | Date | Licence | Words |
|---|---|---:|---|---:|
| Ch. 11 Aircraft Performance | [PDF](https://www.faa.gov/sites/faa.gov/files/13_phak_ch11.pdf) | 2023 | Public domain, 17 U.S.C. 105 | 16,830 |
| Ch. 12 Weather Theory | [PDF](https://www.faa.gov/sites/faa.gov/files/14_phak_ch12.pdf) | 2023 | Public domain, 17 U.S.C. 105 | 12,346 |
| Ch. 13 Aviation Weather Services | [PDF](https://www.faa.gov/sites/faa.gov/files/15_phak_ch13.pdf) | 2023 | Public domain, 17 U.S.C. 105 | 11,437 |
| Ch. 14 Airport Operations | [PDF](https://www.faa.gov/sites/faa.gov/files/16_phak_ch14.pdf) | 2023 | Public domain, 17 U.S.C. 105 | 16,981 |
| Ch. 15 Airspace | [PDF](https://www.faa.gov/sites/faa.gov/files/17_phak_ch15.pdf) | 2023 | Public domain, 17 U.S.C. 105 | 5,427 |
| Ch. 16 Navigation | [PDF](https://www.faa.gov/sites/faa.gov/files/18_phak_ch16.pdf) | 2023 | Public domain, 17 U.S.C. 105 | 18,679 |
| Ch. 17 Aeromedical Factors | [PDF](https://www.faa.gov/sites/faa.gov/files/19_phak_ch17.pdf) | 2023 | Public domain, 17 U.S.C. 105 | 15,850 |

## Ingestion

`pypdf` extracts text page by page. Text is Unicode-normalized, ligatures are
expanded, soft hyphens removed, and printed page labels are retained as
locations. A complex drawing caused text extraction to fail on a page; the
indexer now catches that page-level exception and skips its text so indexing
can continue. It also retries transient embedding errors, including
disconnections.

The chosen section design splits at detected headings, merges sections under
40 words, and windows long sections at 300 words with 40-word overlap. Each
chunk records its document id, title, URL, page or pages, section, design, word
count, and position. The active section collection has 583 chunks after adding
Chapter 14 (107 new chunks); the original fixed design has 504 chunks. Index
storage is 34 MB, below the 90 MB limit.

## Test set

The original test set has 30 questions: 19 single-part, 5 multi-part, and 6
unanswerable. For example, q04 asks how a headwind affects takeoff distance;
q22 asks both about thunderstorm hazards and information used to identify
storms. q26 asks for Category II ILS minimums, which the original corpus did
not cover.

## Retrieval

The saved retrieval comparison uses 24 answerable questions and predates the
Chapter 14 addition.

| Chunking | Method | Hit@1 | Hit@3 | Hit@5 | All passages@1 | All passages@3 | All passages@5 | Words@5 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Fixed | Vector | 0.625 | 0.833 | 0.917 | 0.542 | 0.792 | 0.833 | 999 |
| Fixed | Hybrid | 0.708 | 0.875 | 0.917 | 0.625 | 0.833 | 0.833 | 999 |
| Section | Vector | 0.833 | 0.875 | 0.958 | 0.708 | 0.833 | 0.875 | 968 |
| Section | Hybrid | 0.750 | 0.875 | 0.958 | 0.667 | 0.833 | 0.875 | 1,083 |

Section/vector was selected because it had the best hit@1 and matched the best
hit@5 while returning fewer prompt words than section/hybrid.

## Tools and subagent

The MCP `search` tool returns up to five handbook passages with document and
page citations. `add_document` accepts a file inside the project, uses the same
index pipeline, does nothing for an unchanged indexed file, and replaces
chunks if the contents for that document id change.

The `.claude/agents/corpus-researcher.md` subagent has only the search tool. It
must search first, answer in at most five sentences, cite each factual claim,
and refuse when the passages do not answer. Claude Code 2.1.330 ran this agent
with Claude Opus 5.5:

> **User:** What do runway holding position markings look like and where must an aircraft stop?
>
> **corpus-researcher tool call:** `search("runway holding position markings")`
>
> **Search result:** [phak-ch14 p.14-8] says runway holding position markings
> are four yellow lines, two solid and two dashed, across the taxiway. Before
> reaching the solid lines, stop so no part of the aircraft intersects the
> first solid line; do not cross the double solid lines without ATC clearance.
>
> **corpus-researcher:** Runway holding position markings are four yellow
> lines, two solid and two dashed, painted across the full width of the taxiway
> at the same spot as the runway holding position sign [phak-ch14 p.14-8].
> When you taxi toward a runway, the two solid lines are on your side, so stop
> before them so that no part of the aircraft touches the first solid yellow
> line, and don't cross them until ATC clears you [phak-ch14 p.14-8]. If the
> tower is closed or the airport has no tower, you may taxi onto or across the
> runway only when it is clear and no aircraft is on final approach, and you
> should look both ways [phak-ch14 p.14-8]. When you leave a runway you'll see
> the dashed lines first, and you are clear of the runway only when the whole
> aircraft has passed both the dashed and solid lines; you don't need a
> clearance to cross them on the way out [phak-ch14 p.14-8]. A tip: at some
> airports, an enhanced taxiway centerline marking starts 150 feet before the
> holding position marking to warn you to get ready to stop [phak-ch14 p.14-13].

## Adding a document

Before adding Chapter 14, q27 was refused because the indexed chapters did not
cover runway holding position markings:

> The corpus does not cover this. The available handbook materials focus on
> weather theory, aviation weather services, airspace, navigation, aircraft
> performance, and aeromedical factors, and do not contain information on
> airport markings or runway holding position stopping requirements.

Chapter 14 was added from `corpus/extra/phak-ch14.pdf` with `add_document`.
It contributed 16,981 words and 107 section chunks. After indexing, the same
q27 question was answered from page 14-8:

> Runway holding position markings consist of four yellow lines, two solid
> lines and two dashed lines, painted across the width of the taxiway
> [phak-ch14 p.14-8]. As you approach the runway, you will face the two solid
> yellow lines first [phak-ch14 p.14-8]. You must stop prior to reaching the
> solid lines, ensuring that no portion of the aircraft intersects the first
> solid yellow line until you have received clearance from Air Traffic Control
> (ATC) [phak-ch14 p.14-8]. When exiting the runway, your entire aircraft must
> cross completely over both the dashed and solid lines to be considered clear
> of the runway [phak-ch14 p.14-8].

## Harness and guardrails

`AGENTS.md` describes the student-pilot audience, source restriction,
citations, refusals, real-flight safety reminder, add-document approval, and
answer length. The harness requires a human to type `yes` before
`add_document` runs interactively; non-interactive evaluation refuses the
operation. The additional citation guardrail checks that citations came from
search results in the current run, requires citations on non-refusals, and
retries once before withholding an invalid answer. The agent also has a
12-step call limit. The limit guardrail fired on q28.

## Evaluation

The saved full evaluation was run before Chapter 14 was added: 30/30 answers
were recorded using section/vector and `gemini-flash-latest`. Results were 23
correct answers, 6 correct refusals, and 1 incorrect answer; there were no
invalid citations. The 6 refusal cases were graded directly in code rather
than by the LLM judge.

There are now 22 human labels. The 20 questions with both a human grade and a
judge verdict are answerable questions. Correct verdicts agree on **19/20
(95%)** and supported verdicts agree on **20/20 (100%)**. q09 is the only
disagreement: the human grade marked it correct, while the judge marked it
incorrect because it omitted sudden wind shifts from the reference answer.
The answer was supported, so supported verdicts still agree. The two
human-labeled unanswerable questions, q26 and q30, have no judge verdict
because refusal cases are graded directly in code.

Across all 22 human labels, correct is 22/22 and supported is 21/22; q26's
refusal was correct, but its extra advice was not supported by the retrieved
passages. The saved evaluation averages 8,729 tokens, 176.2 seconds, and 1.77
tool calls per question (2,929 judge tokens on average). These figures are
from the pre-Chapter-14 evaluation.

## Failures

There was one incorrect answer: q09, classified as **wrong answer from the
right passage**. The retrieved cold-front passage supported the answer's
claims, but the answer omitted the reference answer's key fact, sudden wind
shifts. The judge was stricter than the human grade on this point; the failure
and this cause are recorded in `eval/failures.csv`.

## Decision

Use the assistant as a **study aid only**, not for real-flight decisions.
Before flying, verify information against current FAA sources or an instructor.

## AI use

Copilot and Claude Code were used for implementation, indexing, and evaluation
analysis. The human-label rows were manually
reviewed in the assistant session at the user's request; they are not
LLM-judge outputs or independent student grades.
