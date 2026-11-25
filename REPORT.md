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

TODO: paste the table from `eval/retrieval.md` (hit rate at 1, 3, 5 for `clause` and `window`, and average words sent to the prompt).

TODO (mine): which design I chose and why, using the numbers (hit rate against words in the prompt, and especially the multi-passage questions). Say what the numbers do not show.

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

TODO (mine): choose an unanswerable question (e.g. one about a contract with no governing-law clause), write the new document that answers it, and show:
1. the already-indexed case (adding the same file again embeds nothing),
2. the answer before (a refusal) and after (a correct, cited answer),
3. how many embeddings the addition cost.

## Harness and guardrails

TODO: paste my final `AGENTS.md` rules (rewritten in my words, with the reason of each).

Guardrails in `agent.py`:
1. **Approval**: `add_document` runs only after a yes from the person; without a terminal (evaluation) it is denied.
2. **Call limit**: at most 6 tool calls per question.
3. **Citation check** (my extra guardrail): an answer must cite only contracts the agent really retrieved. If not, the agent gets one retry; if it still fails, the answer is returned with a warning.

TODO (mine): one real case where a guardrail fired (look for the event in `eval/answers.jsonl` or `eval/summary.md`).

## Evaluation

TODO after running `main.py evaluate`:
- Code checks (refusal prefix, valid citations, expected contract cited, key numbers present).
- My rubric (from `eval/rubric.md`) and why I wrote it that way.
- My agreement with the judge on 20+ answers I graded first (`eval/human_labels.csv`), and what the disagreements show.
- Results: correct, unsupported, correct refusals, wrong refusals, made-up answers to unanswerable questions.

## Failures

TODO (mine): failed questions by cause with counts (retrieval miss, wrong answer from the right passage, unsupported claim, wrong refusal, bad test question), starting from `eval/failures.csv`, and what to fix first.

## Decision

TODO (mine): would I let users rely on it, for what, with which safeguard. Cost per question: tokens and seconds from `eval/summary.md`.

## AI use

Draft to complete and adjust (keep it truthful):
- **Corpus**: my fictional contracts were rewritten by Claude (an AI assistant) to be more realistic; I reviewed TODO (how many) of them.
- **Code**: `index.py`, `server.py`, `agent.py`, `evaluate.py` and `eval_check.py` were written with Claude's help; I ran them and fixed problems with it.
- **Test set**: I wrote the questions myself from the contracts. TODO (mine): say honestly if Claude gave me example questions or patterns, and which ones I changed.
- **Grades, rubric, design choice, failure analysis and decision**: mine.
- **Judge**: a Gemini model grades answers using my rubric.
- **Report**: Claude made this skeleton; the analysis sections are mine.
