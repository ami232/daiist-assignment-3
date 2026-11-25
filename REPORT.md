# Assignment 3 Report

- **Name**: Hugo Marsiglia
- **Student ID**: 19610
- **Group**: BBADBA 5A

## Use case

The users are bid managers at small and medium companies. They decide whether and how to bid for EU public tenders. They ask about thresholds, procedures, time limits, exclusion grounds, the ESPD self-declaration and review deadlines.

They act on the answer. A wrong time limit means a missed deadline. A wrong exclusion or threshold rule can get a bid excluded, or make the company prepare for the wrong procedure. "The corpus does not cover this." costs a few minutes of looking elsewhere. So a refusal is better than a guess, and every claim must carry a citation the user can open.

## Corpus

Four English legal texts from EUR-Lex. Licence for all four: reuse allowed under Commission Decision 2011/833/EU, © European Union, https://eur-lex.europa.eu.

| doc_id | Document | URL | Date | Words (all) | Words indexed |
|---|---|---|---|---|---|
| `dir_2014_24` | Directive 2014/24/EU on public procurement | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32014L0024 | 26 February 2014 | 78,032 | 56,585 |
| `reg_2016_7` | Implementing Regulation (EU) 2016/7, ESPD standard form | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0007 | 5 January 2016 | 8,124 | 7,577 |
| `dir_89_665` | Directive 89/665/EEC on review procedures, consolidated version of 17 April 2014 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:01989L0665-20140417 | 21 December 1989 | 3,726 | 3,726 |
| `reg_2025_2152` | Delegated Regulation (EU) 2025/2152, thresholds for 2026-2027 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32025R2152 | 22 October 2025 | 340 | 123 |
| | **Total** | | | **90,222** | **68,011** |

"Words indexed" leaves out the recitals. The rule in `index.py`: if articles and annexes together reach 52,000 words, recitals are dropped. They reach 68,011.

One limit of the corpus: the Directive is the original 2014 text. Its Article 4 still shows the 2014 thresholds (for example EUR 5 186 000 for works). The 2026 amounts are only in `reg_2025_2152`, written as "X is replaced by Y".

A fifth document, Delegated Regulation (EU) 2025/2151 (concession threshold), is kept out of the corpus in `docs_to_add/` for the add-document demo.

## Ingestion

**Extraction.** `index.py` downloads the HTML, parses it with BeautifulSoup and cuts it into sections: one per recital, per article paragraph and per annex part. Each section keeps its document, part (recital, article, annex), location ("Article 58", "Annex XII"), heading and paragraph number. The corpus gives 569 sections, 420 without recitals. Layout tables are flattened to lines such as "(a) text". Footnotes and signature blocks are removed.

**One extraction problem we fixed.** Annex headings swallowed the sub-headings below them. The title of Annex I came out as "CENTRAL GOVERNMENT AUTHORITIES BELGIUM", because the country name is formatted like a heading. Now only the first heading line is the annex title, and the rest stays in the text. Two other fixes: page-footer lines ("ELI: …", "ISSN …") leaked into Article 2 of `reg_2025_2152` and are now dropped, and the text of the ESPD form is read from the hidden "Text of image" blocks, because the form is published as images.

**Two chunking designs**, one ChromaDB collection each:

| Design | Rule | Chunks | By document (2014/24, 2016/7, 89/665, 2025/2152) |
|---|---|---|---|
| A `fixed` | 250 words, 50 words overlap, ignores article borders | 341 | 283, 38, 19, 1 |
| B `structure` | one chunk per article or annex part; split at paragraph borders above 400 words; a tail under 40 words is merged | 257 | 212, 24, 19, 2 |

**Metadata on every chunk:** `chunk_id`, `doc_id`, `doc_title`, `part`, `location`, `locations` (all articles a chunk touches, for design A), `heading`, `paragraph`, `url`, `file_sha256`, `words`, `header`, `design`. The `chunk_id` is a hash of design, document and text, so a rerun never embeds the same chunk twice.

**Embeddings.** `gemini-embedding-2`, 3,072 dimensions, cosine distance. Each chunk is embedded with a title line such as "Directive 2014/24/EU, Article 58, Selection criteria, paragraph 2".

## Test set

**Method.** 36 questions in `eval/questions.csv`. Claude Code drafted them from the four documents under my direction, phrased as a bid manager would ask, not in the wording of the articles. They were written and committed before the index existed, so before any retrieval tuning. `eval/validate_questions.py` checks that every expected document and location exists in the extracted corpus.

| Kind | Count | Meaning |
|---|---|---|
| single | 22 | one passage answers it |
| multi | 7 | two passages are needed |
| unanswerable | 7 | close to the topic, but not in the corpus (concessions, utilities, national rules) |

**Two examples.**

- q01, single, expected `dir_2014_24 | Article 27`: "How many days do we get at least to submit a tender in an open procedure?" Reference: "At least 35 days from the date the contract notice was sent."
- q30, unanswerable: "What is the EU threshold for concession contracts from 2026?" Reference: "The corpus does not cover this. Concession thresholds are set under Directive 2014/23/EU and its delegated regulation, which are not in the corpus."

## Retrieval

29 answerable questions, numbers from `eval/retrieval.csv`. For multi questions a hit needs both passages in the top k. Chart: `eval/retrieval.png`.

Two hit tests:

- **Lenient:** the expected location is among the locations the chunk touches.
- **Strict:** the expected location is the chunk's main location, the article with the most words in the chunk.

| Design | Mode | Lenient hit@1 / 3 / 5 | Strict hit@1 / 3 / 5 | Words added to the prompt at k=5 |
|---|---|---|---|---|
| A fixed | vector | 69% / 90% / 97% | 52% / 79% / 86% | 1,237 |
| A fixed | hybrid | 55% / 79% / 90% | 41% / 66% / 76% | 1,237 |
| **B structure** | **vector** | 55% / 86% / 97% | **55% / 86% / 97%** | 1,394 |
| B structure | hybrid | 48% / 66% / 72% | 48% / 66% / 72% | 1,452 |

**Why design B.** I use the strict test, because it is the fair one. A fixed 250-word window often covers two or three articles. Under the lenient test it counts as a hit for each of them, even when the expected article is only the tail of the chunk. Design B has one location per chunk, so its numbers are the same under both tests. Under the lenient test A and B tie at 97% on hit@5 and A wins on hit@1. Under the strict test B wins: 97% against 86% on hit@5 and 55% against 52% on hit@1. B costs about 13% more words in the prompt (1,394 against 1,237). The chosen configuration is B, vector search, k = 5 (`index/config.json`).

**Why hybrid lost.** Hybrid fuses BM25 and vector rankings with reciprocal rank fusion. BM25 scores word overlap. My questions use a bid manager's words, not the law's words, so BM25 ranks the right passage badly. For q05 BM25 puts it at rank 29 of 30, while vector search has it at rank 3. The fusion gives both rankings the same weight, so the weak BM25 list pushes good vector hits out of the top 5. With B hybrid, both passages of a multi question are in the top 5 for only 29% of the multi questions.

**The one miss.** With B vector at k = 5, q26 misses the ESPD form passage (`reg_2016_7 | Annex 2`).

## Tools and subagent

`server.py` is an MCP server with two tools.

**`search(query)`**. The description starts: "Search a corpus of EU public procurement law and return the best-matching passages." It then lists the four documents and what each covers, says that Article 4 of `dir_2014_24` shows the 2014 amounts and `reg_2025_2152` the 2026 ones, and says what the corpus does not cover: national rules, below-threshold contracts, concessions and utilities.

**`add_document(path)`**. The description starts: "Add one document file to the search index. It changes the index, so call it only when the user explicitly asks to add a file." It accepts only an existing .pdf, .html, .htm, .txt or .md file inside the repository.

**One search result** for "How many days do we get at least to submit a tender in an open procedure?" (first of 5, text shortened):

```text
5 results, best first. Cite facts with the tag in square brackets, exactly as written, e.g. [dir_2014_24 | Article 27].

--- Result 1  [dir_2014_24 | Article 27]  score 0.8364
chunk_id: 01a2b63cef11701d34a144abecfe85a761a2f25e5882950579ffcba554ea766f
document: Directive 2014/24/EU on public procurement
heading: Open procedure (paragraph 1-4)
text:
1. In open procedures, any interested economic operator may submit a tender in response to a call for competition.
The minimum time limit for the receipt of tenders shall be 35 days from the date on which the contract notice was sent.
[...]
```

**Subagent.** `.claude/agents/corpus-researcher.md` may use only `mcp__corpus__search`. Its instructions, in short: search before answering and stop after four searches; answer only from the returned text; cite every claim with the exact tag `[doc_id | location]`; if the results do not cover the question, reply exactly "The corpus does not cover this." and say where to look; copy numbers exactly; say which period a threshold applies to; say when a rule is a minimum, a maximum or a Member State option; reply in the language of the question in a few sentences. It cannot add documents.

**Transcript from my editor.**

```text
❯ Use the corpus-researcher subagent: what is the minimum time limit for
  receiving tenders in an open procedure, and when can it be shortened?

⏺ corpus-researcher(Minimum tender time limit open procedure)
  ⎿  Done (2 tool uses · 11.0k tokens · 16s)

⏺ Under Directive 2014/24/EU, Article 27, the baseline minimum time limit for
  receipt of tenders in an open procedure is 35 days from the date the contract
  notice was sent.

  It can be shortened on these grounds:

  Ground: Prior information notice (PIN)
  Minimum limit: 15 days
  Condition: PIN not used as the call for competition; contained the required
    info (Annex V Part B §I); sent for publication 35 days–12 months before the
    contract notice
  ────────────────────────────────────────
  Ground: Duly substantiated urgency
  Minimum limit: 15 days
  Condition: Where the 35-day limit is rendered impracticable by urgency (Art.
    27(3))
  ────────────────────────────────────────
  Ground: Electronic submission of tenders
  Minimum limit: 30 days (−5 days)
  Condition: Authority accepts tenders by electronic means per Art. 22

  These are options for the contracting authority. The reductions attach to the
  35-day baseline, and the PIN/urgency and electronic routes can combine.

  Two related constraints pull the other way:
  - Article 47 — the authority must account for the complexity of the contract
  and extend time limits where late additional information or significant
  document changes require it.
  - Article 53 — where free electronic access to the procurement documents can't
  be offered, the limit must be prolonged by 5 days, except in cases of
  substantiated urgency under Art. 27(3).

  All citations are to Directive 2014/24/EU.
```

## Adding a document

**Already indexed.** `add_document` computes the SHA-256 hash of the file. If a file with the same hash is indexed, nothing changes and it returns "already indexed, nothing changed". If a file with the same `doc_id` but different content is indexed, the old chunks are deleted and the new version is indexed. No embedding is spent on a file that is already there.

**Demo** (`eval/add_document_demo.md`). It runs on a temporary copy of the index, so the committed index is unchanged and q30 stays unanswerable in the main evaluation.

- Question: "What is the EU threshold for concession contracts from 2026?" (q30)
- Document added: `docs_to_add/reg_2025_2151.html`, Delegated Regulation (EU) 2025/2151.

| Step | Result |
|---|---|
| Before | "The corpus does not cover this." It points to Directive 2014/23/EU. Retrieved: Article 4, Article 6, Article 13 and Article 92 of the Directive and Article 1 of `reg_2025_2152`. |
| First call | `doc_id reg_2025_2151: added 6 chunks to the 'structure' collection.` |
| Second call, same file | `already indexed, nothing changed (doc_id reg_2025_2151, 6 chunks).` |
| After | "The threshold for concession contracts is EUR 5,404,000, applying from 1 January 2026", cited `[reg_2025_2151 | Article 1]`. |

**The first demo run refused.** In the first run the agent still answered "The corpus does not cover this." after the document was added. That run did not save its searches, so I cannot show why. I then added logging of the searches and the retrieved passages and ran the demo again. The second run is the one in the file. A likely cause is that `AGENTS.md` and the `search` description both say the corpus does not cover concessions, and the agent model does not give the same answer every run. Even the successful answer starts with "The corpus does not cover concession contracts in detail". So adding a document is not enough: the tool description and the rules that list what the corpus covers must be updated too.

Two flaws in the "after" answer: it writes "EUR 5,404,000" with commas although the source and rule 6 say "EUR 5 404 000", and it puts two tags inside one bracket.

## Harness and guardrails

`agent.py` is a LangChain agent on Gemini. It starts `server.py` over MCP and uses `AGENTS.md` as its system prompt.

**AGENTS.md rules.** Eleven rules, each with a one-line reason:

1. Search before every answer.
2. Answer only from the search results.
3. Cite every claim with the exact tag `[doc_id | location]`.
4. If the results do not cover the question, say exactly "The corpus does not cover this." and suggest where to look.
5. If only part is covered, answer that part and say what is missing.
6. Copy numbers, days and euro amounts exactly.
7. Say which period a threshold applies to (2014 amounts in Article 4, 2026 amounts in `reg_2025_2152`).
8. Say when a rule is a minimum, a maximum or a Member State option.
9. Never call `add_document` unless the user explicitly asks to add a named file.
10. Keep answers short and in the user's language.
11. No legal advice on a specific dispute.

**Approval step.** `add_document` is interrupted before it runs. The user sees the file path and types y or n. Anything else, or no terminal, counts as a rejection. In the evaluation the agent runs without approval rights, so it cannot add documents.

**Limits.** At most 6 model calls and 4 searches per question.

**Extra guardrail: citation check.** After the agent answers, code checks every `[doc_id | location]` tag against the passages retrieved in that conversation. An answer that is not a refusal must have at least one valid tag. If the check fails, the agent gets one retry with a correction. If it fails again, the answer is replaced by "The corpus does not cover this."

It fired on 6 of 36 questions. Two real cases:

- **q01.** The first answer cited `[dir_2014_24 | Article 27(1)]`, `(2)`, `(3)` and `(4)`. The retrieved tag is `[dir_2014_24 | Article 27]`. The content was right, but the tags did not match any retrieved passage. The retry gave the same answer with the exact tag. The same happened in q12, q26 and q29.
- **q32** (unanswerable, utilities threshold). The first answer said the corpus does not cover utilities, in its own words, with no citation and without the exact refusal sentence. The guardrail saw claims without a citation. The final answer is the exact sentence "The corpus does not cover this."

In q13 the model put two tags inside one bracket, which the check does not read as a citation. The retry fixed it.

## Evaluation

Agent model `gemini-3.5-flash-lite`, judge model `gemini-3.8-flash`, both pinned for the whole run. Numbers from `eval/summary.json`.

**Code checks** (no model needed): every citation tag points to a retrieved passage; the answer has a citation or is a refusal; refusals are compared with the question kind.

**Judge rubric** (`eval/judge_rubric.md`). The judge gets the question, its kind, the reference answer, the agent's answer and the full retrieved passages. It gives two independent grades:

- **correct**: the key fact of the reference is there (number, days, amount, date, yes/no), both parts for a multi question, and nothing contradicts the reference. For an unanswerable question, correct means it refuses and does not answer anyway.
- **supported**: every factual claim is in the retrieved passages. A claim that is true but not in the evidence gets 0. Pointers such as "check national law" are not claims.

**Results on 36 questions.**

| Measure | Result |
|---|---|
| Correct (judge) | 35 of 36 (97%) |
| Unsupported (judge) | 5 of 36 (14%) |
| Correct refusals (unanswerable) | 7 of 7 |
| Wrong refusals (answerable) | 0 of 29 |
| Invalid citations in final answers | 0 |
| Expected passage retrieved by the agent | 28 of 29 |
| Citation guardrail fired | 6 |

**My agreement with the judge.** I graded 20 answers in `eval/human_labels.csv` without looking at the judge's verdicts.

| Grade | Agreement | Cohen's kappa |
|---|---|---|
| correct | 20 of 20 (100%) | 1.0 |
| supported | 5 of 20 (25%) | 0.04 |

All 15 disagreements go the same way: I gave supported = 0 and the judge gave 1.

- **14 of the 15 come from the grading tool, not from the answers.** For my first 19 grades `grade.py` showed me only the first 70 words of each retrieved passage. The judge saw the full passages. My notes say so, for example for q04: "The Article 33 excerpt cuts off before the four-year limit". So on these 14 answers my grade measures the excerpt, not the evidence. `grade.py` now shows the cited passages in full; I graded the 20th answer (q33) that way and agreed with the judge. I kept my original 19 labels as they were.
- **1 is a real disagreement (q30).** The answer refuses and adds that Directive 2014/23/EU governs concessions. I counted that as a claim that is not in the passages. The judge counted it as a pointer to where to look, which the rubric allows.

So the agreement on "supported" does not tell me yet whether the judge can be trusted on that grade. On "correct" we agree on all 20, including the one wrong answer (q11).

## Failures

5 of 36 answers failed at least one grade. The causes below are suggested by the evaluation code from the checks and the judge (`eval/failures.csv`).

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 0 | |
| Wrong answer from the right passage | 1 | q11 |
| Unsupported claim | 4 | q23, q24, q26, q33 |
| Wrong refusal | 0 | |
| Bad test question | 0 | |

- **q11** (contract modification). Article 72 was retrieved. The answer presents the 10% and 15% limits as a rule on their own, "regardless of thresholds". The Directive needs both conditions together: below the percentage and below the Article 4 threshold. This is the only wrong answer, and it is about money.
- **q23, q24** (2026 thresholds). The amounts are right. The date "from 1 January 2026" is not in the retrieved passages: it is in Article 2 of `reg_2025_2152`, and only Article 1 was retrieved. The date is in `AGENTS.md` and in the `search` description, so the agent took it from its instructions.
- **q33** (German below-threshold contract). It refuses correctly, then adds the same 2026 date without evidence.
- **q26** (ESPD). The answer says the exclusion grounds are in Part III. A passage of Annex 2 was retrieved, but not the part that says so. This is the same question that misses at k = 5 in the retrieval test.

**What to fix first.** The threshold date: three of the five failures (q23, q24, q33) have the same cause. `reg_2025_2152` is 123 words in two chunks. Storing Article 1 and Article 2 as one chunk puts the amount and the date in the same passage. Second, q11: add a rule that conditions joined by "and" in the text must be given together. Third, q26: split the ESPD form by Part so each part heading is in its own chunk.

Other weaknesses seen in the answers, not counted as failures: amounts written with commas ("EUR 5,404,000") against rule 6; in q24 the 2026 amount carries the tag of Article 4, which shows the 2014 amount; answers average 136 words although rule 10 asks for short answers.

## Decision

I would let bid managers use it as a first lookup, not as the final word.

- **For what:** finding the rule and the article for a time limit, an exclusion ground, the ESPD or a review deadline. 35 of 36 answers were correct, no answerable question was refused, and all 7 unanswerable questions were refused.
- **Not for:** the final go or no-go on a threshold or a contract modification without reading the article. The one wrong answer (q11) was on a value limit, and the 2026 threshold answers carried a date the passages did not show.
- **Safeguards:** every answer cites the article, and the user opens the cited article before acting. The citation guardrail blocks tags that were not retrieved. The exact refusal sentence is kept when the corpus does not cover the question. Adding a document needs human approval.
- **Limits of this evidence:** 36 questions, drafted from the same documents; one judge model; my own "supported" grades are not usable yet (see Evaluation); the agent model does not give the same answer every run, as the first demo run showed.

**Cost and latency per question** (agent `gemini-3.5-flash-lite`, paid standard prices of USD 0.30 per million input tokens and USD 2.50 per million output tokens):

| | Mean | p90 |
|---|---|---|
| Input tokens | 8,116 | 12,983 |
| Output tokens | 275 | 421 |
| Seconds | 2.4 | 3.6 |
| Model calls | 2.39 | |
| Cost | USD 0.0031 per question (USD 3.12 per 1,000) | |

## AI use

Claude Code wrote the code and drafted the test set; I wrote and edited the report from its first draft; the human labels in eval/human_labels.csv are my own.
