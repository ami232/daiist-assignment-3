# Assignment 3 Report

- **Name**: Máximo Garrido Blanco
- **Student ID**: 18994
- **Group**: BBADBA 5B

I took every decision in this project myself, based on the options and recommendations Claude gave me at each step. Each decision is logged with its reason and the alternatives I rejected in [DECISIONS.md](DECISIONS.md).

## Use case

**Who asks:** a consultant who writes electric-vehicle market reports for automotive clients and needs figures for them: sales, shares, the EV fleet, batteries, critical minerals and projections.

**What a wrong answer costs:** a wrong figure feeds client investment decisions and damages the firm's credibility. "I don't know" costs about 10 minutes of checking the source.

**What follows for the system:** it must refuse rather than guess. A near-miss (the right topic but the wrong country, year or metric) counts as a wrong answer.

## Corpus

IEA reports under **CC BY 4.0**, with no personal data. Only the chapters on car markets, batteries, minerals and outlooks are indexed.

| Document | doc_id | Date | Words indexed |
|---|---|---|---|
| [Global EV Outlook 2026](https://iea.blob.core.windows.net/assets/857aa690-2a43-453f-9f12-147cc8f0a1dd/GlobalEVOutlook2026.pdf) | GEVO2026 | May 2026 | 32,901 |
| [Global EV Outlook 2025](https://iea.blob.core.windows.net/assets/7ea38b60-3033-42a6-9589-71134f4229f4/GlobalEVOutlook2025.pdf) | GEVO2025 | 2025 | 12,986 |
| [Global Critical Minerals Outlook 2026](https://iea.blob.core.windows.net/assets/19c60aa0-ee07-4a20-a138-33c967ac5008/GlobalCriticalMineralsOutlook2026.pdf) | GCMO2026 | July 2026 | 9,999 |
| **Total** | | | **55,886** |
| [Electric Car Markets in a Time of Uncertainty](https://iea.blob.core.windows.net/assets/a096b500-9d47-411d-a5db-b297a5d95927/ElectricCarMarketsinaTimeofUncertainty.pdf) (held out for `add_document`) | ECMU2026 | July 2026 | 7,508 |

The two editions of the Global EV Outlook are included on purpose: consultants compare years.

## Ingestion

- **Extraction:** PyMuPDF. Lines are kept by font size: body text is about 11 pt and headings 14 pt or more; headers, chart labels and footnotes (9 pt or less) are dropped. Paragraphs cut by a page or column break are joined.
- **Problems I fixed:** `pypdf` split words ("sale s"), so I switched to PyMuPDF. The GEVO 2026 PDF repeats the last lines of p. 18 at the top of p. 19, so a sentence was duplicated; repeated lines at a page break are now removed.
- **Chunking:** one chunk per report section, at most 250 words, starting with a `[report · chapter · heading]` line. That gives **322 chunks**, or 366 after the demo. The comparison design used fixed 150-word windows (469 chunks).
- **Metadata:** doc_id, title, year, page, page_end, chapter and heading.
- **Embeddings:** `gemini-embedding-2` with 768 dimensions, stored as JSONL in `index/` and searched by cosine similarity with numpy.

## Test set

I wrote 32 questions from the PDFs before tuning anything: **20 single, 6 multi and 6 unanswerable**.
- Every question states its year, because two editions are in the corpus.
- Multi questions compare the two editions or cross two documents.
- Unanswerable questions are near-misses: the corpus has a related figure, such as Spain's sales *growth* when the question asks for its *share*.
- q32 is answered only by the held-out report.

Examples:
- **q09 (single):** "How much battery capacity was deployed in EVs worldwide in 2025 and how much did deployment grow from 2024?" Answer: 1.2 TWh, almost +30% (GEVO2026, p. 92).
- **q23 (multi):** "How did the electric share of new car sales in Europe change between 2024 and 2025?" Answer: about 20% (GEVO2025, p. 17) to 28% (GEVO2026, p. 21).

## Retrieval

A hit is a chunk from the expected document whose pages include the expected page. A multi question counts only if both passages are found. Results on the 26 answerable questions:

| Design | hit@1 | hit@3 | hit@5 | words@5 |
|---|---|---|---|---|
| Fixed, 150 words with a 30-word overlap | 58% | 69% | 81% | 750 |
| **Structured, sections ≤250 words + header** | **77%** | **88%** | **100%** | 984 |

**Why fixed loses:** most of its misses are multi questions where the 2025 passage never appears, because the 2026 chunk on the same topic always wins (the "wrong edition" problem). The structured header puts the edition and topic into the embedded text.

**I chose structured with k = 5**, the smallest k that finds both passages of every multi question (about 1,300 tokens per search).

## Tools and subagent

**Tools** (`server.py`):
- **`search(query)`:** returns the 5 best passages, each with its source and page. Its description tells the model what the corpus covers, to search one fact at a time with the year, and to cite as (doc_id, p. page).
- **`add_document(path)`:** indexes a new PDF. Its description says to call it only when the user asks.

**One search result** (q01, shortened):

```text
[1] Source: GEVO2026, pp. 18-19 | Global EV Outlook 2026 (2026) | Chapter 1 · Close to 55% of new cars sold in China were electric in 2025 | relevance 0.82
[...] an estimated 44 million electric cars were on Chinese roads at the end of 2025 [...]
```

**Subagent** ([corpus-researcher.md](.claude/agents/corpus-researcher.md)): Claude Code delegates to it any factual question on EV sales, shares, batteries, minerals or projections, and it can only use `search`. Its instructions:
- make at most 3 searches, one per fact, with the year and the region in the query;
- check the edition and the region of every figure (a global or EU figure is not a European one);
- give a figure only if a passage states it for the same place, year and metric (simple arithmetic between cited figures is allowed), and never substitute a related figure;
- otherwise answer "The corpus does not cover this.", or answer the covered part and say what is missing;
- answer in 1-4 sentences, citing every figure as (doc_id, p. page).

**Transcript** (q23, from Claude Code; full version in [eval/subagent_transcript.md](eval/subagent_transcript.md)):

> **User:** Use the corpus-researcher subagent: How did the electric share of new car sales in Europe change between 2024 and 2025?
>
> **Subagent** (after 3 searches): "around 20%" in 2024 (GEVO2025, p. 17) and 28% in 2025 (GEVO2026, p. 21), a rise of about 8 percentage points.

In a first run it cited a global figure as a European one, so I added a rule to check the region of every figure.

## Adding a document

**If the document is already indexed:** a SHA-256 hash of each file decides what happens. Same content → nothing changes and no embeddings are spent; a new version → it replaces the old one; otherwise → added. Indexing is all or nothing.

**Demo** ([eval/add_document_demo.md](eval/add_document_demo.md)), with q32: how did global EV sales change in Q2 2026 compared with Q2 2025?

| Step | What happened |
|---|---|
| Before | "The corpus does not cover … the second quarter of 2026." It mentions only the first-quarter figure (−8%, GEVO2026, p. 11). |
| Add | The agent called `add_document` on the ECMU report and I approved it in the terminal. 44 passages were added (3 → 4 documents). |
| After | "Global electric car sales grew by 4% year-on-year in the second quarter of 2026 (ECMU2026, p. 9)." This is correct. |

My first attempt failed halfway with a temporary API error, and the index stayed unchanged, as intended.

## Harness and guardrails

`agent.py` runs LangChain `create_agent` on `gemini-3.5-flash-lite`, with the MCP tools and [AGENTS.md](AGENTS.md) as its system prompt.

**AGENTS.md** has 12 rules, each with its reason:
- answer only from `search`, and cite every figure from a page that was retrieved;
- give a figure only for the same place, year and metric, and never substitute a related one;
- refuse with "The corpus does not cover this.", or answer the covered part of a question;
- at most 3 searches; check the edition and scope of every passage;
- if the search limit stops a search, write "Not searched" instead of claiming the corpus lacks it;
- use `add_document` only when the user asks;
- answer in 1-4 sentences.

**Approval step:** a middleware stops every `add_document` call and asks `Approve? [y/N]` in the terminal. Without a "y", nothing changes. With no terminal (`check.py`, `evaluate.py`) the call is refused.

**Extra guardrail: citation check.** Every (doc_id, p. N) in an answer must be a page a search returned, and figures must be cited. On failure the agent gets one retry; after that the answer is blocked.

**When it fired:** in the demo, the agent's confirmation message had numbers and no citation. Asked to fix it, the agent cited a page no search had returned, and the answer was blocked. Because those numbers came from the tool itself, the check now requires citations only when a search was made.

## Evaluation

`main.py evaluate` runs the agent on the 32 questions and checks the answers in code. The LLM judge (`gemini-3.5-flash-lite`) runs only after I had graded the answers myself, without seeing any verdict.

**Code checks:** citations valid 32/32; 6 correct refusals and 0 wrong refusals; the expected page retrieved and cited in 26/26.

**Judge rubric** (the same as my grades, each 1 or 0):
- **correct:** the key figures match the reference (rounding is fine) and every part of the question is answered. For an unanswerable question, it refuses and gives no substitute figure.
- **supported:** every claim is in the retrieved passages.

| | correct | supported |
|---|---|---|
| My grades | 31/32 | 32/32 |
| Judge | 32/32 | 32/32 |
| Agreement | 97% (kappa 0.00) | 100% |

**Results:** 31/32 correct, 0 unsupported, 6/6 correct refusals and 0 wrong refusals.

**The only disagreement is q13.** The answer gave two different UK figures; I graded it 0 and the judge 1.

**Kappa** is 0 because almost every grade is 1, so I also gave the judge **8 planted wrong answers** (wrong country, wrong year, growth given as share, a forecast given as an actual value, invented figures, a missed refusal, a partial answer). It caught all of them. Counting real and planted answers together, agreement is 95% on correct (kappa 0.84) and 100% on supported (kappa 1.00).

## Failures

| Cause | Count |
|---|---|
| Retrieval miss | 0 |
| Wrong answer from the right passage | 0 |
| Unsupported claim | 0 |
| Wrong refusal | 0 |
| Bad test question | 1 (q13) |

**q13:** the two IEA editions disagree on the UK's 2024 share ("nearly 30%" in GEVO2025 against "1 in 4" in GEVO2026). The agent cited both correctly, but my question did not say which edition to use.

**What to fix first:** a rule in AGENTS.md telling the agent to flag when two passages give different figures for the same thing, and from which edition each comes.

Earlier problems, all already fixed:
- a wrong refusal when the search limit was hit (fixed with the "Not searched" rule);
- a scope error in the subagent (fixed with the scope rule);
- a false positive of the citation check.

## Decision

**Yes, as an assistant with review.** The consultant can use it to find and cite IEA figures, opening the cited page before a figure goes into a client report. That takes about 2 minutes instead of 10. It is not for figures outside these reports.

**Safeguards:** the citation check, the refusal and "Not searched" rules, and the rule on conflicting editions once it is applied.

**Why not without review:** 32 questions are a small test, the agent is a small model, and q13 shows the sources can contradict each other.

**Cost and latency per question:**

| | Value |
|---|---|
| Tokens | about 6,500 on average |
| Calls | 2 model calls and 1-2 searches |
| Latency | median 12.8 s |
| Cost at paid prices | about USD 0.002, plus USD 0.001 for the judge |
| Cost of this project | free: everything ran on the free tier |

**Model:** I first chose `gemini-3.5-flash`, but its free tier allows only 20 requests a day, so I switched to `gemini-3.5-flash-lite`.

## AI use

I used **Claude Code** (Anthropic, model Claude Opus) throughout the project:
- **Code:** it wrote all the code (`index.py`, `retrieval.py`, `server.py`, `agent.py`, `evaluate.py`, `demo_add_document.py`) and the subagent and AGENTS.md files, ran the tests and the evaluation, and found and fixed bugs.
- **Options:** at each decision point it explained the options so that I could decide which option we would use.
- **My decisions:** I made every decision, each one logged with its alternatives in DECISIONS.md: the use case, corpus, chunking designs and final design, refusal rules, judge rubric, failure classification and ship decision.
- **Test set and grades:** I wrote the 32 test questions; Claude only checked their format and that each answer is on the stated page. I graded all 32 answers myself before the judge ran.
- **Planted answers:** at my request, Claude wrote the 8 planted wrong answers and their expected grades, which are reported separately from my grades.
- **This report:** Claude helped me write it clearly and in a well-organised way, so that the information and decisions I gave it were better written. Starting from its first version, I reviewed and edited it until the report turned out how I wanted.
