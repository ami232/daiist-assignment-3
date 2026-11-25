# Assignment 3 Report

- **Name**: Eli Homsi
- **Student ID**: 18938
- **Group**: BBADBA 5A

## Use case

The users are financial analysts and investors who read companies' annual reports. The system answers only from the annual reports indexed in it: Apple, NVIDIA and Tesla to start with. An analyst can add any other company's annual report with the add-document tool, and a question about a company that is not indexed gets "I don't know" until its report is added. They ask about a company's business, its financial performance and its risk disclosures, and use the answers in their notes and investment decisions.

What matters the most is the cost of a wrong answer compared with "I don't know"; an "I don't know" costs the reader about 10 minutes of looking the answer up in the filing, roughly $12 at an assumed $75 an hour; a wrong answer that is caught later costs about 2 hours of rework, roughly $150, and a wrong answer that is not caught can lead to a poor investment decision. A guess is only worth giving if it is right more than about 92% of the time, so when the filings do not contain the answer, the assistant should say which information is missing instead of estimating or inventing a figure.

## Corpus

| Document | URL | Filing date | Licence | Words indexed |
|---|---|---|---|---|
| Apple 10-K (fiscal 2026) | https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm | 2026-11-03 | Public SEC filing | 20,260 |
| NVIDIA 10-K (fiscal 2026) | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm | 2026-02-25 | Public SEC filing | 32,614 |
| Tesla 10-K (fiscal 2025) | https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm | 2026-01-29 | Public SEC filing | 30,853 |
| **Total** | | | | **83,727** |

Words are counted from the indexed chunks. Microsoft's 10-K was used only for the add-document demo (see "Adding a document") and is not part of the corpus.

## Ingestion

Each 10-K is parsed with BeautifulSoup. I remove scripts, styles and the hidden XBRL header, and drop blank lines, bare page numbers and the repeated "Table of Contents" header. The cleaned text is then split on the "Item N" headings, and I keep only Item 1 (Business), Item 1A (Risk Factors) and Item 7 (MD&A), dropping sections under 50 words, such as table-of-contents rows. Item 8 (the financial statements) is not indexed, so detailed statement figures are answered from the MD&A only.

One problem came up during extraction, as in the HTML tables a label and its number sit in separate cells, so after plain text extraction the numbers ended up far from their labels. I fixed it by joining each table row onto one line ("Net sales | 478.8 | ..."), so a figure stays next to what it describes.

The text is then chunked in two ways so that I could compare them. In the fixed design it is cut into windows of 150 words with 30 words of overlap. In the sections design each section is cut into chunks of up to 300 words with 30 words of overlap, and a chunk never crosses a section boundary. This gives 632 fixed chunks and 289 section chunks, all embedded with gemini-embedding-2. Each chunk stores an id (a hash of its content), the source (for example apple-10k-2026), the company, the location (for example "Item 1A. Risk Factors"), the design and the text.

## Test set

I wrote 36 questions from the topics of the Business, Risk Factors and MD&A sections, before evaluating the system. Claude suggested candidate questions, and I chose which ones to keep and which to change. The reference answers come from the passages the search tool returns for each question, so each one can be checked in the reports.

Of the 36 questions, 20 are single (one passage answers them), 8 are multi (they need two passages, for example a comparison between two companies) and 8 are unanswerable (the reports do not contain the answer). The unanswerable ones stay close to the topic of the corpus and are not obviously off-topic. For example, q21 is a multi question, "Compare how Apple and NVIDIA describe the risk of depending on third-party manufacturers", because it needs the risk section of both reports. And q29, "What was Microsoft's cloud revenue last year?", is unanswerable, so the expected answer is "The indexed reports do not cover this."

## Retrieval

I compared the two chunking designs on the 28 answerable questions. The 8 unanswerable ones are left out because they have no correct passage to find. A hit means the right source and section are in the top k results.

| Design | k=1 | k=3 | k=5 |
|---|---|---|---|
| Fixed (150-word windows) | 0.68 | 0.82 | 0.86 |
| Sections (up to 300 words, never crossing a section) | 0.71 | 0.89 | 0.89 |

In this sense, I chose the sections design. It finds the right passage more often, and since a chunk never crosses a section, its citation (for example "Item 1A") is reliable. That matters because analysts need to check each claim in the original report. It also keeps each topic together and needs fewer chunks (289 instead of 632). The difference is small, only 1 or 2 questions, and the designs differ in both chunk size and structure, so I take it as a hint and not as proof. The price is more words in the prompt: a search returns 5 passages, which adds about 1,000 to 1,500 words with the sections design, about twice as many as the fixed design.

## Tools and subagent

The server offers two tools. The first is `search`, which takes the question, can be limited to one company, and returns the 5 most relevant passages with their source. Its description tells the agent to use it for any question about a company's business, financial results or risks, to limit it to one company when only one report is needed, and to say the answer is not in the reports instead of guessing. The second is `add_document`, which takes the path of a new file and adds it to the index so that `search` can find it. Its description says to use it only when the user asks to add an annual report or a text file, and that a document that is already indexed is not added twice.

For example, for the question "What product categories does Apple list in its Business section?", `search` returns passages like the one below. It shows the company, the document, the section and a score for how close the passage is to the question:

```
[1] Apple | apple-10k-2026 | Item 1. Business | similarity 0.76
Company Background The Company designs, manufactures and markets smartphones, personal computers, tablets, wearables and accessories, and sells a variety of related services. [...]
```

The subagent is a helper defined in the file `.claude/agents/corpus-researcher.md`. It can use only one tool, `search`. Its instructions are:

```
You answer questions about company annual reports using only the `search` tool.

- Search before answering. For comparisons, search each company separately with the `company` filter.
- Use only what the passages say. Cite each claim as (source, location).
- If the passages do not answer the question, say "The indexed reports do not cover this." Do not guess.
- Keep the answer short, with the numbers first.
```

The subagent only needs to read the reports, so it only gets `search`. The `add_document` tool changes the index, so without it the subagent cannot damage the index even if it makes a mistake. The main agent does have `add_document`, but it needs my approval and a check on the file path first. The idea is to give each agent only the tools it needs.

I tested the subagent from the terminal with Claude Code. This is the conversation, shortened with [...]:

```
> Use the corpus-researcher subagent to answer: What does NVIDIA say about export controls on its products?

corpus-researcher (NVIDIA export controls research)
  Backgrounded agent

NVIDIA's FY2026 10-K says export controls have cost it billions and largely shut it
out of China's data center market.

Numbers
- $4.5 billion charge in Q1 FY2026 for excess H20 inventory and purchase obligations
  (nvidia-10k-2026, Item 1) (nvidia-10k-2026, Item 7).
[...]
- At the end of fiscal 2026, NVIDIA says it was "effectively foreclosed" from China's
  data center compute market (nvidia-10k-2026, Item 1A).
[...]

Agent "NVIDIA export controls research" finished (19s)
```

Every claim in the answer shows its source and section, as the instructions require.

## Adding a document

The add-document tool runs the same pipeline as the starter corpus. If the same document is already indexed, nothing is embedded again, and if a file with the same name changed, its old passages are replaced by the new ones.

For the demo I took the unanswerable question "What was Microsoft's cloud revenue last year?" and added Microsoft's 10-K for the year ended June 30, 2026 through the agent, which asked for my approval first. Before adding it, the agent said the indexed reports do not cover Microsoft. After adding it, the agent answered that Microsoft Cloud revenue was $214.4 billion in fiscal year 2026, citing the Microsoft 10-K (Item 7). Afterwards I restored the original index so that the evaluation still treats this question as unanswerable.

## Harness and guardrails

The agent follows the rules in AGENTS.md. It answers only from what `search` returns, cites every claim with its source and section, and says "The indexed reports do not cover this." when the passages do not answer the question. For comparisons it searches each company separately, and it never mixes up companies or years. It calls `add_document` only when the user asks and gives the file path. Answers are short, with the numbers first, and citations follow a strict format: the source id and the item, for example (apple-10k-2026, Item 1A).

Adding a document is the one action that changes the index, so it has two controls. Before `add_document` runs, the agent shows the call and asks "Approve? [y/N]"; if nobody can answer, for example during the evaluation, the call is denied automatically. On top of that, my own guardrail only accepts .htm, .html, .txt and .md files that are inside the project folder, so the agent cannot read other files on the computer. The agent is also limited to 8 model calls and 6 tool calls per question, so one question cannot loop and use up the quota.

To see the path check fire, I tested it on three paths. A path outside the project folder and a file type that is not allowed are both blocked, and a file inside the project is allowed:

- `/etc/passwd` -> "Blocked: '/etc/passwd' is outside the project folder. Only files inside it can be added."
- `notes.pdf` -> "Blocked: only .htm, .html, .txt, .md files can be added."
- `corpus/apple-10k-2026.htm` -> allowed (no message)

I tested the check directly because my first two full agent runs with `/etc/passwd` failed with a temporary Google "503 high demand" error. On a later run the agent refused the request on its own, without using any tool, because its instructions say to add only company reports. So there are two layers of protection: the agent's instructions and the path check in the code. When the check blocks a path, the agent never asks for approval and never calls `add_document`.

## Evaluation

The evaluation has two parts. The code checks that every citation matches a passage the agent really retrieved, and that unanswerable questions are refused. At first only 18 of 36 answers passed, because the model cited the company name instead of the source id. After I made the citation rule stricter in AGENTS.md, all 36 pass.

The rest is graded by an LLM judge with two rules. An answer is correct if it gives the same facts as the reference answer, or if it refuses when the question is unanswerable. It is supported if every claim appears in the retrieved passages, so a claim that is true but not in the passages counts as unsupported.

I graded 32 answers myself before looking at the judge. We agreed on about 94% of the "correct" grades and 97% of the "supported" grades. The judge was stricter than me on two answers and more generous on one. Comparing our grades also helped me find a bug in the judge: it could not see all the passages for questions about two companies. I fixed it. The judge is the same model as the agent (gemini-3.1-flash-lite), so it may accept answers too easily. That is why I also graded 32 answers myself.

| | Judge | My grades |
|---|---|---|
| Correct | 33 of 36 | 31 of 32 |
| Supported | 36 of 36 | 31 of 32 |

All 8 unanswerable questions were refused, and none of the answerable ones were refused by mistake. For unsupported answers, the judge found 0 of 36, and I found 1 of 32 (q33, which added a remark that is not in the passages).

## Failures

| Cause | Count | Questions | What happened |
|---|---|---|---|
| Retrieval miss | 5 | q22, q24, q25, q26, q27 | All need two passages. One search returns only 5 chunks, so it cannot cover two companies or two sections at once. |
| Wrong answer from the right passage | 1 | q04 | The right passage was found, but the answer left out the main figures. |
| Unsupported claim | 1 | q33 | The answer added a remark that is not in the passages. |
| Wrong refusal | 0 | none | No answerable question was refused. |
| Bad test question | 1 | q18 | The reference answer had more facts than the question asked for. |

The hit rate measures a single search, but the agent searches once per company or topic, so the retrieval misses did not always stop it from answering well. For example, q22 and q24 were graded correct.

I would fix the unsupported claim (q33) first. For the question "What is the salary of Apple's CEO?", the agent correctly refused, but then added that this information is usually in the Proxy Statement (Form DEF 14A), which is not in the retrieved passages. The fix is a rule in AGENTS.md that the assistant must not add anything that is not in the retrieved passages, because an unsupported claim that nobody catches costs far more than an honest "I don't know". Second, I would fix the missing figures (q04) with a rule to give the main figures first, because a correct source with missing numbers is still a weak answer for an analyst.

## Decision

I would let users rely on it, but as a first quick lookup and not as a final source. An analyst can use it to get a fast, cited answer, and then check the original report before using the result in an investment decision. It works best for simple questions, such as what a company does or which risks it describes. For figures and for comparisons between companies, the analyst should confirm the number in the original report.

My reason is that on my 32 graded answers it was right about 97% of the time, above the 92% I calculated in my use case as the level where a guess is worth giving. But the sample is small, and 31 out of 32 is not enough to show that it is really above 92%. It is also mostly about one company, and the mistakes I found were a missing figure and a claim that was not in the reports. So I would keep three safeguards: every claim shows its source so it can be checked, the assistant refuses when the reports do not contain the answer instead of guessing, and adding a document needs the user's approval and only accepts files inside the project folder.

Over the 36 questions the median latency was about 3.7 seconds. A question used about 4,500 input tokens and 365 output tokens, which costs about 0.2 cents per question at the paid price of gemini-3.1-flash-lite, 25 cents per million input tokens and 1.50 dollars per million output tokens. I used the free tier, so the real cost was zero. Either way it is far below the cost of a missed or wrong answer in my use case.

## AI use

I used Claude for project guiding, clarifying concepts, organization, brainstorming and general questions. It assisted me with the code (writing parts of it and debugging) and with the test set (suggesting candidate questions and drafting reference answers from the retrieved passages). I made the decisions: the use case, the design choice, my own grades of 32 answers made before reading the judge, the failure analysis and the final ship decision.
