# Assignment 3 Report

- **Name**: María Fernández Gómez-Monche
- **Student ID**: 19784
- **Group**: BBADBA 5B 

> Legend: text without a marker is a factual draft from the code (check it is true). `TODO (mine)` = must be written by me, in my words.

## Use case

**Who asks?** In-house lawyers and contract managers at a company that has millions of commercial
agreements with suppliers and clients that needs quick answers about what they say.

**What they do with the answer?** They act on it: they decide whether to renew or terminate a
contract, quote a liability cap or a notice period to a client, or check which law governs a
dispute. They do not read the whole contract again, so the answer is treated as "what the
contract says".

**What a wrong answer costs compared with "I don't know"?** A wrong answer is much more
expensive. An "I don't know" costs a few minutes: the person opens the contract and looks for the
clause. A confident wrong answer (an invented figure, or the right clause from the wrong
contract) leads to a wrong decision, for example giving a client a liability cap that the
contract does not contain. Because the 49 contracts repeat similar clauses with different
numbers, the most dangerous error is mixing up two contracts, and the second one is making up a
figure when the corpus is silent. A wrongly refused question is the cheapest error, so the
system is designed to refuse when it is not sure.

## Corpus

The corpus is 49 fictional business-to-business commercial contracts (`corpus/CONTRACT_001.pdf` to `CONTRACT_050.pdf`, one number is unused), written in English. They are my own data, so they contain no personal data and need no third-party licence. They were rewritten with AI help to look like real contracts (see AI use), and the professor approved reusing them.

| Item | Value |
|---|---|
| Documents | 49 PDFs (the brief asks for at least 3) |
| Words | 51,262 (counted from the PDF text with `pypdf`; the brief asks for at least 50,000) |
| Source / URL | own fictional contracts, in this repository: `corpus/` |
| Date | written and rewritten in November 2026 |
| Licence | own work; no external licence needed |

Each contract has numbered clauses (term, fees, liability, termination, data protection, IP, governing law, confidentiality, and so on) and often a schedule. The contracts are about different services (software, logistics, consulting, and others) and between different companies, but many use similar wording with different figures. That suits the use case: a user can easily get the right clause from the wrong contract, so the system has to be tested on that. The corpus also has real gaps (for example, some contracts have no governing-law clause, and some fees are only "per the Order Form"), which gives genuine questions the corpus cannot answer.

## Ingestion

- **Extraction**: `pypdf` in layout mode, page by page, so each chunk keeps its page.
- **Cleaning**: bullet glyphs (`\x7f` etc.) removed, line breaks and tables normalised.
- **Parsing**: each contract is split into its numbered clauses and schedules.
- **Metadata per chunk**: `source` (file name), `doc_id`, `contract` (title), `design`, `location` (e.g. `Clause 6 (Liability), 6.1-6.3, p. 2`), `page_start`, `page_end`, `words`, `clause`.
- **Two chunking designs**:
  - `clause`: one chunk per clause or schedule, with a header (contract title and parties); clauses under 60 words are merged up to 220 words, clauses over 320 words are split at sub-clauses. 463 chunks, about 124 words each.
  - `window`: 200-word windows with step 160, no header. 300 chunks.
- **Embeddings**: Gemini `gemini-embedding-2`, 768 dimensions, stored in ChromaDB (`index/`, 6.5 MB). `main.py index` only embeds chunks that have no saved vector (chunk id = design + document + hash of the text); the server never embeds the corpus.
- **One extraction problem I fixed**: in 23 contracts the title wraps onto two lines, so the header of the clause chunks lost the parties. I changed the header parsing and re-embedded 222 chunks. TODO (mine): say how you noticed it and how you checked the fix.

## Test set

`eval/questions.csv` has 46 questions: 19 single-passage, 16 that need two or more passages (`multi`), and 11 that the corpus cannot answer (`unanswerable`). The brief asks for at least 30, 5 and 5. Each row has the question, its kind, the expected source file, the expected clause (one per source, separated by `;` for multi questions) and a reference answer.

I wrote the questions from the contracts: I read the clauses, picked a fact (a fee, a notice period, a liability cap, a data-export period), and wrote the question and the reference answer. The unanswerable questions ask for something that looks like it should be in a contract but is not (for example a penalty that the clause never states). TODO (mine): confirm and adjust this paragraph. Be honest about what was yours and what came from examples (see AI use).

`eval_check.py` checks the file before evaluating: counts, kinds, unique ids, that every `expected_source` exists and that every expected clause exists in that contract, so a typo in the answer key is not mistaken for a retrieval miss.

Two examples:

| id | kind | question | expected source / location | reference answer |
|---|---|---|---|---|
| q12 | multi | Which client gets a longer period to pay invoices, the one in contract 003 or the one in contract 006? | `CONTRACT_003.pdf` 4.2; `CONTRACT_006.pdf` 5.2 | Contract 006 (120 days) gives longer than contract 003 (90 days). |
| q46 | unanswerable | What monthly fee does Logistica Integral pay for each of its 8 locations? | none | Schedule 1 of contract 026 refers to an order form that is not in the corpus; no monthly fee amount is stated. |

TODO (mine): one sentence on why you chose these two (q12 needs two searches; q46 is a near-miss, because the contract mentions fees but gives no amount).

## Retrieval

I compared two ways of cutting the contracts into pieces, and measured how often a passage with the answer shows up among the first 1, 3 or 5 results (the hit rate). The first design, clause, makes one chunk per clause (465 chunks). The second, window, uses fixed windows of text (300 chunks). I used the 35 questions that have an answer.

With clause, the right passage was first in 40% of the questions, in the top 3 in 89% and in the top 5 in 94%. With window it was 14%, 60% and 69%. The five results also carry less text with clause (about 598 words) than with window (about 980), so the agent reads less and each question costs less. The difference is biggest on questions that need passages from two contracts: with clause 88% of them are fully covered in the top 5, with window only 38%. On single-passage questions the two designs are closer (100% against 95% at five results), so window is not bad for simple lookups, but it is much worse when the answer is spread over several places.

I chose clause. It wins on every measure, and a clause is also the natural unit in a contract: a question about a liability cap or a notice period is almost always answered by one clause, and a window often mixes the end of one clause with the start of the next one, which makes the match less clean.

What these numbers do not show: the hit rate only says that a good passage is among the results, not that the agent uses it well. Clause is weak at the first position (it is only first in 40% of the questions, and in none of the multi-contract ones), so the agent has to read several results and cannot trust the first one. Also, my test set is small (35 questions), so a difference of one or two questions moves the percentages a lot.


## Tools and subagent

The MCP server (`server.py`, started by the agent over stdio) has two tools.

**`search(query)`**. Description given to the model:

> Search a collection of 49 B2B commercial contracts and return the 5 passages that best match the query. Use it whenever the question is about what a contract says: who the parties are, fees, liability caps, termination and notice, data protection, intellectual property, governing law, exclusivity, penalties. Each result starts with its citation, `[CONTRACT_xxx.pdf | clause / page]`, followed by the passage text. Cite the source and clause of every claim you make. Mention the contract's parties or subject in the query when you know them: clauses of different contracts look alike. Results are the closest passages, not guaranteed answers: if none of them says what the question asks, the corpus does not cover it. Lower `distance` means closer.

The description tells the model when to call the tool, how to cite, and how to tell that the corpus is silent. TODO: paste one real search result here (run `uv run python -c "import index; [print(h['metadata']['source'], h['metadata']['location'], round(h['distance'],3)) for h in index.retrieve('liability cap contract 047', 3)]"` tomorrow after 09:00, or ask the agent a question and copy the tool output).

**`add_document(path)`**. Description given to the model:

> Add one more contract (a PDF file) to the searchable corpus: extracts and chunks it like the rest, embeds the chunks (this spends embedding quota) and stores them in the index. If the same file is already indexed with the same content, nothing is embedded and the tool says so; if a file with the same name but different content is indexed, its old chunks are replaced. Only call it when the user asks to add a document, and say what you added.

**Subagent**: `.claude/agents/corpus-researcher.md`, with `tools: mcp__corpus__search`, so it can only search. Its instructions say to answer only from the passages, search again with other words (up to 3 searches per contract), check that a passage belongs to the right contract, search each part of a two-contract question separately, copy figures exactly, and start with `NOT IN CORPUS:` when the passages do not say it.

TODO (mine): paste one transcript of the subagent from your editor (Copilot or Claude Code) answering a question, and say in one sentence what you noticed (did it search more than once? did it cite correctly?).

## Adding a document

**Unanswerable question.** q05: "Which law governs the contract between Veltrix Group and SunBridge
Logistics?" Contract 002 has no governing-law clause, so the right answer is a refusal.

**Document added.** I wrote `eval/added/CONTRACT_051.pdf`, a short amendment to contract 002 that
states that Spanish law governs the agreement and that the courts of Barcelona have exclusive
jurisdiction (clauses 2 and 3). I gave it the next contract number so that the citation format
`[CONTRACT_xxx.pdf | clause]` keeps working.

**Before.** The agent answered `NOT IN CORPUS`: it found contract 002 but the corpus has no
governing-law provision for it (3 tool calls, 8,787 input tokens, 18.4 s).

**Adding it.** I asked the agent to add the file. The approval step asked me to confirm and I
answered yes. The index went from 463 to 465 `clause` chunks, so only the 2 new chunks were
embedded; nothing else was re-embedded.

**After.** The same question gave: "The contract between Veltrix Group S.A. and SunBridge
Logistics S.L. is governed by the laws of Spain [CONTRACT_051.pdf | Clauses 2-4, 2.1]" (1 tool
call, 2,968 input tokens, 12.9 s).

**Already indexed.** [Result of adding the same file again: ...]

**What I noticed.** [Your own observation: for example, that one added document changes the answer
at once and costs only 2 embeddings, and that the first attempt exposed a bug in my citation
guardrail, which I fixed.]

## Harness and guardrails

 Use the corpus-researcher subagent: What uptime percentage does NexaCore guarantee to Retailmax each month?

⏺ corpus-researcher(Uptime NexaCore Retailmax)
Backgrounded agent (↓ to manage · ctrl+o to expand)

The corpus-researcher subagent is searching the contracts for NexaCore's monthly uptime commitment to Retailmax. I'll give you its answer and citations when it finishes.

Waiting for 1 background agent to finish

Message from @corpus-researcher (ctrl+o to expand)

NexaCore guarantees Retailmax 95% platform uptime per calendar month [CONTRACT_001.pdf | Clause 4 (Service Level Agreement (SLA)), 4.1]. If downtime goes over 5% in a month, NexaCore's only liability is a service credit. The credit can be no more than that month's fee, is applied to the next invoice and is not paid in cash [CONTRACT_001.pdf | Clause 4, 4.3]. Service credits are the Client's "sole and exclusive remedy" for downtime [CONTRACT_001.pdf | Clause 4, 4.4].

The contract header names NexaCore Technologies S.L. as Provider and Retailmax España S.A. as Client, so these passages come from the right contract.

Agent "Uptime NexaCore Retailmax" finished · 7s

I asked the subagent which uptime percentage NexaCore guarantees to Retailmax each month. It answered 95% per calendar month and cited `[CONTRACT_001.pdf | Clause 4, 4.1]`, which matches the reference answer of question q07 in my test set. It also added the consequence of missing the target (service credits capped at that month's fee, as the sole remedy, with the clauses cited) and checked the contract header (NexaCore Technologies as Provider, Retailmax España as Client) before using the passages, so it followed the instruction to confirm that the passage belongs to the right contract.
It used only the `search` tool, made a search, and finished in 7 seconds. What I noticed: the answer is longer than the question needs, so the "short answer" rule in the subagent's instructions is only partly followed.

Guardrails in `agent.py`:
1. **Approval**: `add_document` runs only after a yes from the person; without a terminal (evaluation) it is denied.
2. **Call limit**: at most 6 tool calls per question.
3. **Citation check** (my extra guardrail): an answer must cite only contracts the agent really retrieved. If not, the agent gets one retry; if it still fails, the answer is returned with a warning.

In practice a guardrail fired in the evaluation on question q01, which compares the liability limits of contracts 049 and 047. The agent kept searching and reached the limit of 6 tool calls, so it was stopped and gave a wrong answer, because a passage of one of the two contracts was never retrieved. The limit did its job (it stopped a loop that was costing tokens), but it also showed me a retrieval problem. The citation check also fired once by mistake in my before/after test of adding a document: after the agent added the new contract, the check did not count the new document as something it had retrieved, so it asked for a retry. I fixed the check so that it counts the sources of both search and add_document.

## Evaluation

I ran the agent on all 46 test questions, 35 with an answer and 11 without one. Each answer went through two kinds of checks. The first are checks in code: whether a refusal starts with NOT IN CORPUS, whether every cited contract was really retrieved, whether the expected contract is cited and whether the key numbers of the reference appear. The second is a language model used as a judge, which decides if the answer is correct and if it is supported by the passages, following a rubric.

The rubric (in `eval/rubric.md`) is short on purpose. An answer is correct only if it gives the facts of the reference answer, and a partial answer counts as not correct. An answer is supported only if everything it says is in the retrieved passages. For the questions without an answer, the correct behaviour is to refuse, and inventing a figure is the worst failure.

Before looking at the judge, I graded 20 answers myself (`eval/human_labels.csv`): single-contract, multi-contract and unanswerable questions. Then I compared. On whether the answer is correct we agree on 19 of 20 (95%), and on whether it is supported we agree on 20 of 20. The one disagreement is q16: the agent gave the right law for contract 001 but said it could not find contract 029. I graded it as not correct because it is only half an answer; the judge accepted it. So the judge is a bit more generous than I am with partial answers, and I read its scores with that in mind.

Results: of the 35 questions with an answer, 32 are correct (91%), one was wrongly refused and none contains an unsupported claim. Every answer that was not a refusal cites a contract that was really retrieved (35 of 35). Of the 11 questions without an answer, 10 were refused correctly (91%) and in one case the agent answered anyway. The agent cites the expected contract in 33 of 35 answers and includes the key numbers of the reference in 28 of 35 (80%); this second number is lower than the judge's score because some correct answers just word the number differently or leave out extra details.

## Failures

Five questions need a comment (`eval/failures.csv`). I classified them myself.

Retrieval miss (2): in q01 a passage of contract 047 or 049 was not retrieved, and the agent also hit the limit of 6 tool calls. In q16 the search did not find the governing-law clause of contract 029, so the agent said it was not in the corpus; here the judge also accepted a weak answer.

Agent formatting error (1): in q33, about the uptime guaranteed to a reseller, the answer is supported by the contract (it says there is no service level beyond the standard description), but the agent did not start it with NOT IN CORPUS as the rules require, so the code check flags it. The content is fine; the format is wrong.

Judge too strict (2): in q34 (a 22% commission) and q40 (a fixed fee of EUR 180,000) the answers are correct and cited, but the judge gave them 0 because my reference answers also list extra details (subscription and per-order fees, quarterly instalments) that the question did not ask for. This is not a failure of the system. It is partly a weakness of my reference answers, which are longer than the questions need.

The automatic first guess in `eval/summary.md` labels two of these as "wrong answer from the right passage" and one as an unsupported claim, but when I read them I did not agree, so my classification above is the one I trust.

What I would fix first: retrieval for questions that compare two contracts, because that is where the real misses are. Then I would make the refusal format stricter in the instructions, and shorten the reference answers so the judge does not punish correct answers.

## Decision

I would let people use it for looking up facts in these contracts (a fee, a notice period, which law applies), as long as they see the cited contract and clause and can check it. On my test set it answers 91% of the questions correctly, always cites a contract it really retrieved and refuses in 91% of the questions that have no answer. I would not let anyone rely on it alone for questions that compare several contracts, or for anything with legal consequences, because that is where it misses passages and it can also answer when it should refuse. The safeguard is that a person reads the cited clause before acting, and that adding a document always needs a human yes.

Cost per question: on average 5,064 input tokens and 108 output tokens, 1.7 tool calls and 8.0 seconds (median 7.4, worst case 28.7 seconds and 19,861 input tokens). The input is much bigger than the output because the agent reads several clauses before answering. The judge adds about one more call for each question when I evaluate. I did not compute a price in euros, because it depends on the current price of the model.

## AI use

Draft to complete and adjust (keep it truthful):
- **Corpus**: my fictional contracts were rewritten by Claude (an AI assistant) to be more realistic; I reviewed TODO (how many) of them.
- **Code**: `index.py`, `server.py`, `agent.py`, `evaluate.py` and `eval_check.py` were written with Claude's help; I ran them and fixed problems with it.
- **Test set**: I wrote the questions myself from the contracts.
- **Grades, failure causes and the final choices**: the 20 grades and the failure causes in `eval/failures.csv` are mine. 
- **Judge**: a Gemini model grades answers using my rubric.
- **Report**: Claude made the skeleton from my results; I worte them and reviewed them.
