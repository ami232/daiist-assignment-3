# Assignment 3 Report

- **Name**: Nicolas Aguado
- **Student ID**: 20446
- **Group**: BBADBA 5B

## Use case

A compliance analyst at a UK bank or payments firm asks what three regulations require, for example "how many weeks does a payer have to ask for a refund of a direct debit?" or "which risk factors must a firm consider in its money-laundering risk assessment?". They use the answer to decide what the firm must do, or to point a colleague to the exact regulation.

A wrong answer is expensive: a made-up deadline or a missing obligation can become a compliance breach or a fine. "I don't know" costs only a few minutes, because the analyst opens the regulation. So the assistant should prefer a refusal to a guess, and every claim must carry a citation the analyst can check.

## Corpus

Three statutory instruments, downloaded from legislation.gov.uk on 2026-11-25 (current revised version, XML). Licence: Open Government Licence v3.0. They contain no personal data.

| Document | URL | Words (regulations only) | Chunks |
|---|---|---|---|
| Money Laundering, Terrorist Financing and Transfer of Funds (Information on the Payer) Regulations 2017 (SI 2017/692) | https://www.legislation.gov.uk/uksi/2017/692 | 58,955 | 292 |
| Payment Services Regulations 2017 (SI 2017/752) | https://www.legislation.gov.uk/uksi/2017/752 | 41,747 | 239 |
| Electronic Money Regulations 2011 (SI 2011/99) | https://www.legislation.gov.uk/uksi/2011/99 | 19,185 | 122 |
| **Total** | | **119,887** | **653** |

A fourth document, the Payment Accounts Regulations 2015 (SI 2015/2038, same licence), was added later for the add-document experiment below (53 chunks).

## Ingestion

- **Extraction.** The XML has the regulations in `<Body>`, plus schedules, commentaries and explanatory notes. I keep only the Body and skip the rest.
- **Problem fixed.** My first word count was 218,941, far too high. The XML also holds editorial commentaries (about 16,000 words per document) and schedules, which are not the rule text. Counting by section showed it, and I switched to the Body only (about 120,000 words).
- **Chunking.** Structure-based: one chunk per regulation. A regulation longer than 300 words is split at its numbered paragraphs, so a chunk is a whole paragraph or group of paragraphs. A paragraph longer than 300 words alone is cut by words. Each chunk starts with a header: document, regulation and heading.
- **Metadata per chunk.** `source` (document), `location` (e.g. `regulation 80` or `regulation 20(3)-(6)`), `part`, `heading`, and a hash of the text.
- **Embedding.** `gemini-embedding-2`. A second problem: when sent a list of texts, this model returns one merged vector instead of one per text. I now embed one text at a time and save each vector in ChromaDB (`index/`) right away, so a crash or the daily limit loses nothing. `main.py index` embeds only chunks that have no saved vector, or whose text changed.
- **Size.** 653 chunks, 126,894 words including headers.

## Test set

32 questions in `eval/questions.csv`: 19 `single`, 6 `multi` (two passages) and 7 `unanswerable`. The unanswerable ones are close to the topic but not in the corpus (contactless limit, FCA application fee, Financial Ombudsman limit, EU AMLD6, sanctions freeze, Basel III, open banking consent). Questions were drafted from a sample of real passages with Claude's help, then I checked them (see AI use).

- Single: "Can a bank take money from a customer's account before it has received the payment order?" (Payment Services Regulations, regulation 81).
- Multi: "Up to what point can a payer cancel a direct debit, and if the order reaches the bank on a non-business day, when is it treated as received?" (regulations 83 and 81).

## Retrieval

Three designs over the same chunks, so comparing them needs no extra embeddings: **dense** (Gemini vectors), **bm25** (keywords) and **hybrid** (dense and bm25 merged by reciprocal rank fusion). Hit means every expected (document, regulation) is in the top k. 25 answerable questions.

| Design | hit@1 | hit@3 | hit@5 | Words added to the prompt (k=5) |
|---|---|---|---|---|
| dense | 72% | 96% | 96% | 1,061 |
| bm25 | 24% | 80% | 84% | 1,178 |
| hybrid | 72% | 92% | 100% | 1,137 |

**Chosen: hybrid**, by hit@5 (25/25 against 24/25 for dense). The agent reads 5 passages, so hit@5 is what matters most; keywords help when a question names a specific term and meaning-based search helps when the wording differs. Caution: with 25 questions, one question is 4 points, so the gap with dense is small. Dense is better at k=3 (96% against 92%).

## Tools and subagent

`server.py` exposes two MCP tools; the docstrings are the descriptions the model reads.

- `search(query)`: "Search UK financial-crime and payments regulation: the Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, the Payment Services Regulations 2017 and the Electronic Money Regulations 2011 (plus any document added later). Use it for any question about what these rules require, allow or define. Returns the 5 best-matching passages, each starting with a citation in square brackets: [document, regulation number]. Answer only from the returned text and cite it. If nothing returned answers the question, say the corpus does not cover it."
- `add_document(path)`: "Add a document to the search index. `path` is a file on this computer: .xml (legislation.gov.uk), .pdf, .txt or .md. It is split into chunks with citations, embedded with Gemini and stored. If the document is already indexed, unchanged chunks are skipped (no embedding cost) and only changed or new chunks are embedded. Returns how many chunks were new and how many were already there. Changes the index, so it needs approval."

A `search` result looks like:

```
[payment_services_regs_2017, regulation 80]
Payment Services Regulations 2017, regulation 80 - Requests for refunds for payment transactions initiated by or through a payee
80 1 The payer must request a refund under regulation 79 from its payment service provider within 8 weeks from the date on which the funds were debited. 2 The payment service provider may require ...
```

**Subagent** (`.claude/agents/corpus-researcher.md`): it may use only `mcp__corpus__search`. Its instructions: search with a focused query (twice if two rules are needed), answer only from the passages, cite each claim with the bracket copied exactly, and reply "The corpus does not cover this." when the passages do not answer.

**Transcript from Claude Code:**

I did not run the subagent from Claude Code before the deadline, so I have no real transcript to paste and I did not invent one. The subagent file exists and is written to answer the question "how many weeks does a payer have to request a refund of a direct debit?" with the search tool only. The same search tool, called through my own agent (`agent.py`), returns regulation 80 of the Payment Services Regulations 2017 ("within 8 weeks"), as shown in the search result above.

## Adding a document

If a document is already indexed, `add_document` does not duplicate it. Each chunk has a deterministic id and a hash of its text: unchanged chunks are skipped, changed or new chunks are embedded and replaced.

Experiment (`demo_add_document.py`, saved in `eval/add_document_demo.md`). Unanswerable question: *"How many days does a bank have to open or refuse a basic bank account after receiving a completed application?"*

- **Before:** "The corpus does not cover this. The search results do not contain information regarding timeframes for opening or refusing a basic bank account."
- **Document added:** Payment Accounts Regulations 2015, 53 chunks embedded. Adding it a second time: 53 already indexed, 0 embedded.
- **After:** "A bank (designated credit institution) must open or refuse to open a basic bank account without undue delay, and no later than 10 business days from receiving the completed application [payment_accounts_regs_2015, regulation 24]."

## Harness and guardrails

`agent.py` uses LangChain `create_agent` on Gemini, with the MCP tools from `server.py` and `AGENTS.md` as the system prompt. Rules in `AGENTS.md` (each with its reason): always search first and answer only from the results (my memory of the law may be wrong); cite every claim with the exact bracket (the analyst must be able to check); say "The corpus does not cover this." if the passages do not answer (a wrong answer costs more than none); search again when two regulations are needed; keep answers short; never call `add_document` unless the user asks.

- **Approval before `add_document`.** The tool asks "Approve? [y/N]" in the terminal. With no terminal (as in the evaluation) the answer is always no.
- **Call limit.** At most 6 tool calls per question.
- **Extra guardrail: citation guard.** After the answer, code checks that every citation was in a passage retrieved in this run. If the answer has no citation, or cites something not retrieved, and it is not a refusal, it is replaced by a refusal. Reason: an answer that cannot be verified is worse than none.
- **Case where it fired.** In the final evaluation the citation guard never fired (0 of 32). The error path fired once in the first run (q05): all Gemini models returned quota or overload errors and the agent stopped with a refusal instead of guessing. So the citation guard is implemented but I have no real case where it fired.

## Evaluation

- **Code checks:** valid citations (each cited passage was retrieved): 32/32. Expected regulation cited on answerable questions: 25/25. Refusals detected from the fixed phrase.
- **LLM judge** (Gemini, rubric and the retrieved text as evidence): `correct` = matches the reference in substance, or, for an unanswerable question, a clear refusal with no invented answer. `supported` = every claim appears in the retrieved text.
- **Agreement with my own grades:** I graded 22 answers before reading the judge's verdicts (`eval/human_labels.csv`). Agreement: `correct` 22/22 (100%), `supported` 22/22 (100%).

| Result | Count |
|---|---|
| Correct | 32/32 |
| Supported (no unsupported claims) | 32/32 |
| Correct refusals (unanswerable) | 7/7 |
| Wrong refusals (answerable) | 0/25 |
| Unanswerable answered anyway | 0/7 |

Caveats: the first run scored 31/32 because one question (q05) failed on a Google API error, and I re-ran it. Because of quota limits the agent fell back to a smaller model for 24 of the 32 answers in that first run. My 22 grades had no disagreement with the judge, so they show agreement but say little about whether the judge would catch errors. The judge is from the same model family as the agent, which can make it lenient.

## Failures

No failure in the final run, so all five classes (retrieval miss, wrong answer from the right passage, unsupported claim, wrong refusal, bad test question) have a count of 0. The only failure seen, q05 in the first run, was an infrastructure error (API quota), not one of the five classes.

The result is probably too good to trust fully. The questions come from single passages and are close paraphrases of them, so they are easy: retrieval finds the right regulation in the top 5 every time (100% hit@5), although only 72% at rank 1. What to fix or test first: (1) harder questions, with different wording, partial answers and rules that sit in schedules, which the corpus leaves out; (2) a judge from a different model family; (3) more unanswerable questions that are almost answerable.

## Decision

I would let analysts rely on it as a fast lookup of what these three regulations say, as long as they open the cited regulation before acting, because every answer carries a checkable citation and the system refused all 7 unanswerable questions. I would not let them rely on it for legal advice or for anything outside these documents: the corpus is a snapshot from 2026-11-25, it skips schedules and amendments published later, and the test set is small and easy.

**Cost and latency:** on average 3,127 input and 198 output tokens per question and 18.7 seconds (including retries when Google was overloaded). It used the free Gemini tier, so the money cost was zero.

## AI use

I used Claude (Anthropic) throughout. It wrote most of the code (`index.py`, `retrieval.py`, `server.py`, `agent.py`, `evaluate.py`, the demo script), drafted the 32 test questions and reference answers from passages sampled from the corpus, drafted the `AGENTS.md` rules and subagent file. 
I ran every command, set up the repository and API key, checked the questions and answers, graded 22 answers myself, and reviewed the results.