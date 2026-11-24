# Assignment 3 Report

- **Name**: Eli Homsi
- **Student ID**: 18938
- **Group**: BBADBA 5A

## Use case

**Who asks.** Financial analysts and investors who read companies' annual reports. The system answers only from the annual reports indexed in it: Apple, NVIDIA and Tesla to start with. An analyst can add any other company's annual report with the add-document tool, and a question about a company that is not indexed gets "I don't know".

**What they do with the answer.** They ask about a company's business, its financial performance and its risk disclosures, and use the answers in their notes and investment decisions.

**What a wrong answer costs compared with "I don't know".** An "I don't know" costs the reader about 10 minutes of looking the answer up in the filing, roughly $12 at an assumed $75 an hour. A wrong answer that is caught later costs about 2 hours of rework, roughly $150. A wrong answer that is not caught can lead to a poor investment decision. A guess is only worth giving if it is right more than about 92% of the time, so when the filings do not contain the answer, the assistant should say which information is missing instead of estimating or inventing a figure.

## Corpus

| Document | URL | Filing date | Licence | Words indexed |
|---|---|---|---|---|
| Apple 10-K (fiscal 2026) | https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm | 2026-11-03 | Public SEC filing | 20,260 |
| NVIDIA 10-K (fiscal 2026) | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm | 2026-02-25 | Public SEC filing | 32,614 |
| Tesla 10-K (fiscal 2025) | https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm | 2026-01-29 | Public SEC filing | 30,853 |
| **Total** | | | | **83,727** |

Words are counted from the indexed chunks. Microsoft's 10-K was used only for the add-document demo (see "Adding a document") and is not part of the corpus.

## Ingestion

**Extract and clean.** Each 10-K is parsed with BeautifulSoup. Scripts, styles and the hidden XBRL header are removed. Blank lines, bare page numbers and the repeated "Table of Contents" header are dropped.

**Sections.** The text is split on the "Item N" headings, and only Item 1 (Business), Item 1A (Risk Factors) and Item 7 (MD&A) are kept. Sections under 50 words, such as table-of-contents rows, are dropped.

**One extraction problem I fixed.** HTML tables put a label and its number in separate cells, so after plain text extraction the numbers ended up far from their labels. Each table row is now joined onto one line ("Net sales | 478.8 | ..."), so a figure stays next to what it describes.

**Chunking, two designs.** Fixed: windows of 150 words with 30 words overlap over the whole document. Sections: chunks of up to 300 words with 30 words overlap that never cross a section boundary.

**Chunk metadata.** Each chunk stores id (a hash of its content), source (for example apple-10k-2026), company, location (for example "Item 1A. Risk Factors"), design and text.

**Number of chunks.** 289 chunks for the sections design and 632 for the fixed design, embedded with gemini-embedding-2.

**Known limit.** Item 8 (the financial statements) is not indexed, so detailed statement figures are answered from the MD&A only.

## Test set

**How it was written.** I wrote the questions from the topics of the Business, Risk Factors and MD&A sections of the three reports, before evaluating the system. Claude suggested candidate questions, and I chose which ones to keep and which to change. The reference answers were written from the passages the search tool returns for each question, so each one can be checked in the reports.

**Counts.** 36 questions: 20 single (one passage answers them), 8 multi (they need two passages, for example a comparison between two companies) and 8 unanswerable (the reports do not contain the answer). The unanswerable questions are close to the topic of the corpus and not obviously off-topic.

**Two examples.**

- **Multi (q21):** "Compare how Apple and NVIDIA describe the risk of depending on third-party manufacturers." It needs the risk section of both reports.
- **Unanswerable (q29):** "What was Microsoft's cloud revenue last year?" The expected answer is "The indexed reports do not cover this."

## Retrieval

I compared two ways of cutting the reports into chunks, using 28 answerable questions. A hit means the right source and section are in the top k results.

| Design | k=1 | k=3 | k=5 |
|---|---|---|---|
| Fixed (150-word windows) | 0.68 | 0.82 | 0.86 |
| Sections (up to 300 words, never crossing a section) | 0.71 | 0.89 | 0.89 |

**Words added to the prompt.** A search returns 5 passages. With the sections design this is about 1,000 to 1,500 words per search. The fixed design would add about half as many.

**Design chosen: sections.** It finds the right passage more often, and a chunk never crosses a section, so its citation (for example "Item 1A") is reliable. This matters because analysts need to check each claim in the original report. It also keeps each topic together and needs fewer chunks (289 instead of 632). The difference is small, only 1 or 2 questions, and the designs differ in both chunk size and structure, so I see it as a hint and not as proof. The cost is more words in each prompt.

## Tools and subagent

**search(query, company=None, k=5).** Description: "Search the indexed company annual reports (Business, Risk Factors and Management's Discussion and Analysis of each report) and return the most relevant passages with citations. Use it for any question about a company's business, financial performance, risks or outlook. Pass `company` to search only that company's report; leave it empty to search all of them. `k` is the number of passages to return (1 to 10, default 5). [...] If no passage answers the question, the answer is not in the indexed reports: say so, do not guess. If the company asked about is not indexed, the tool says which companies are."

**add_document(path, company=None).** Description: "Add one document to the index so that `search` can find it. Use it only when the user asks to add a company's annual report (a 10-K or 20-F saved as .htm or .html) or a plain text (.txt, .md) file. [...] The file goes through the same pipeline as the starter corpus: extract, clean, chunk, embed, store. If the same document is already indexed (identical text), nothing is embedded. If a document with the same file name is indexed but its text changed, its old passages are replaced by the new ones."

**One search result.** Query: "What product categories does Apple list in its Business section?"

```
[1] Apple | apple-10k-2026 | Item 1. Business | similarity 0.76
Company Background The Company designs, manufactures and markets smartphones, personal computers, tablets, wearables and accessories, and sells a variety of related services. [...]
```

**Subagent** (`.claude/agents/corpus-researcher.md`, tools: `mcp__corpus__search` only):

```
You answer questions about company annual reports using only the `search` tool.

- Search before answering. For comparisons, search each company separately with the `company` filter.
- Use only what the passages say. Cite each claim as (source, location).
- If the passages do not answer the question, say "The indexed reports do not cover this." Do not guess.
- Keep the answer short, with the numbers first.
```

**Why the subagent only has `search`.** The subagent only needs to read the reports, so I gave it only the `search` tool. `add_document` changes the index, so leaving it out means the subagent cannot alter the index even if it makes a mistake. The main agent can use `add_document`, but it has an approval step and a path check to control it. This follows the idea of giving each agent only the tools it needs.

**Transcript from my editor** (Claude Code in the terminal, shortened with [...]).

```
> Use the corpus-researcher subagent to answer: What does NVIDIA say about export controls on its products?

corpus-researcher (NVIDIA export controls research)
  Backgrounded agent

I've started the corpus-researcher subagent on the question. It's searching NVIDIA's
indexed reports for passages on export controls, and I'll pass on its cited answer
when it finishes.

NVIDIA's FY2026 10-K says export controls have cost it billions and largely shut it
out of China's data center market.

Numbers
- $4.5 billion charge in Q1 FY2026 for excess H20 inventory and purchase obligations.
  It followed an April 2025 U.S. government rule requiring a license to export H20 to
  China (including Hong Kong and Macau) and D:5 countries (nvidia-10k-2026, Item 1)
  (nvidia-10k-2026, Item 7).
- About $60 million in H20 revenue came from licenses granted in August 2025 for
  certain China-based customers (nvidia-10k-2026, Item 1) (nvidia-10k-2026, Item 7).
[...]

Impact and risks
- At the end of fiscal 2026, NVIDIA says it was "effectively foreclosed" from China's
  data center compute market (nvidia-10k-2026, Item 1A).
[...]

These citations come from the corpus-researcher subagent's searches. I did not run
the searches again myself.

Agent "NVIDIA export controls research" finished (19s)
```

The subagent searched only the indexed reports, and every claim carries a (source, item) citation, as its instructions require.

## Adding a document

**If the document is already indexed.** The add-document tool runs the same pipeline as the starter corpus. If the same document is already indexed, nothing is embedded again. If a file with the same name changed, its old passages are replaced by the new ones.

**Demo.** I used the unanswerable question "What was Microsoft's cloud revenue last year?" and added Microsoft's 10-K through the agent, which asked for my approval first.

- **Before:** the agent said the indexed reports do not cover Microsoft.
- **After:** the agent answered that Microsoft Cloud revenue was $214.4 billion in fiscal year 2026, citing the Microsoft 10-K (Item 7).

Afterwards I restored the original index so that the evaluation still treats this question as unanswerable.

## Harness and guardrails

**A case where it fired.** I tested the guardrail on three paths. A path outside the project folder and a file type that is not allowed are both blocked, and a file inside the project is allowed:

- `/etc/passwd` -> "Blocked: '/etc/passwd' is outside the project folder. Only files inside it can be added."
- `notes.pdf` -> "Blocked: only .htm, .html, .txt, .md files can be added."
- `corpus/apple-10k-2026.htm` -> allowed (no message)

I ran this by calling the check directly, because the full agent run with the same request failed twice with a temporary Google "503 high demand" error. When the check blocks a path, the agent never asks for approval and never calls `add_document`.

## Evaluation

**Code checks.** The code checks two things: that every citation matches a passage the agent really retrieved, and that unanswerable questions are refused. At first only half of the answers passed, because the model cited the company name instead of the source id. After I made the citation rule stricter in AGENTS.md, all 36 pass.

**Judge rubric.** An LLM judge grades each answer with two rules. **Correct:** it gives the same facts as the reference answer (or refuses when the question is unanswerable). **Supported:** every claim appears in the retrieved passages, even a true claim counts as unsupported if it is not there.

**Agreement with the judge.** I graded 32 answers myself before looking at the judge. We agreed on about 94% of "correct" grades and 97% of "supported" grades. The judge was stricter than me on two answers and more lenient on one. Comparing our grades also helped me find a bug in the judge (it could not see all the passages for questions about two companies), which I fixed.

**Results.**

| | Judge | My grades |
|---|---|---|
| Correct | 33 of 36 | 31 of 32 |
| Supported | 36 of 36 | 31 of 32 |

- **Correct refusals:** all 8 unanswerable questions were refused.
- **Wrong refusals:** none.

## Failures

| Cause | Count | Questions | What happened |
|---|---|---|---|
| Retrieval miss | 5 | q22, q24, q25, q26, q27 | All need two passages. One search returns only 5 chunks, so it cannot cover two companies or two sections at once. |
| Wrong answer from the right passage | 1 | q04 | The right passage was found, but the answer left out the main figures. |
| Unsupported claim | 1 | q33 | The answer added a remark that is not in the passages. |
| Wrong refusal | 0 | none | No answerable question was refused. |
| Bad test question | 1 | q18 | The reference answer had more facts than the question asked for. |

The hit rate measures a single search, but the agent searches once per company or topic. So the retrieval misses did not stop it from answering well, for example q22 and q24 were graded correct.

**What to fix first.** First, the unsupported claim (q33): I would add a rule in AGENTS.md that the assistant must not add anything that is not in the retrieved passages, because an unsupported claim that nobody catches costs far more than an honest "I don't know". Second, the missing

## Decision

**Would users rely on it?** Yes, but as a first quick lookup and not as a final source. An analyst can use it to get a fast, cited answer, and then check the original report before using the result in an investment decision.

**For what.** It works best for simple questions, such as what a company does or which risks it describes. For figures and for comparisons between companies, the analyst should confirm the number in the original report.

**Why.** On my 32 graded answers it was right about 97% of the time, above the 92% I calculated in my use case as the level where a guess is worth giving. But the sample is small and mostly about one company, and the mistakes I found were a missing figure and a claim that was not in the reports.

**Safeguards.**
- Every claim shows its source, so it can

## AI use

I used Claude for project guiding, clarifying concepts, organization, brainstorming and general questions. It assisted me with the code (writing parts of it and debugging) and with the test set (suggesting candidate questions and drafting reference answers from the retrieved passages). I made the decisions: the use case, the design choice, my own grades of 32 answers made before reading the judge, the failure analysis and the final ship decision.