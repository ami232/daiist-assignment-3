# Assignment 3 Report

- **Name**: Juan Díaz Bernardo (GitHub: JuanDiazBernardo1234)

- **Student ID**: 19785

- **Group**: BBADBA 5A

## Use case

The assistant answers questions about EU AI Act compliance for someone who has to decide whether an AI system is allowed or what obligations it has: a start-up founder, a compliance officer or a student. They use the answer to decide what to build, document or avoid.

A wrong answer is much more expensive than "the documents do not say". The Article 5 prohibitions carry fines of up to EUR 35 million or 7% of worldwide turnover, so a wrong "this is allowed" can cost a company its product, and a wrong deadline or threshold causes a missed obligation. "I don't know" costs a few minutes of reading. This is why the assistant must cite every claim and must refuse when the corpus does not cover a question.

## Corpus

| Document | URL | Date | Licence | Words | Chunks (structure / fixed) |
|---|---|---|---|---|---|
| Regulation (EU) 2024/1689 (AI Act), consolidated version incorporating Regulation (EU) 2026/1744 | https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng/pdf | 27 July 2026 | EUR-Lex reuse notice: reuse allowed with the source acknowledged | 62,695 | 277 / 242 |
| Commission Guidelines on prohibited AI practices, C(2025) 5052 | https://ec.europa.eu/newsroom/dae/redirection/document/112367 | 2025 | CC BY 4.0 | 64,286 | 260 / 224 |
| Commission Guidelines on the definition of an AI system, C(2025) 5053 | https://ec.europa.eu/newsroom/dae/redirection/document/112455 | 2025 | CC BY 4.0 | 5,486 | 25 / 22 |
| *Held out:* Commission Guidelines on GPAI models, C(2025) 7719 | https://ec.europa.eu/newsroom/dae/redirection/document/118340 | 2025 | CC BY 4.0 | 15,730 | 68 (added later) |

The corpus is public law and public guidance, with no personal data. The full credits are in `corpus/sources.json`. The GPAI guidelines are kept in `holdout/` and are indexed only during the before/after experiment. I chose a consolidated text of the Act because the 2026 amendment changed some articles (Article 4, Article 5, Article 113). The index marks amended chunks and the search result tells the model so.

## Ingestion

**Extraction.** `pypdf` in `layout` mode, because the default mode splits words in two. Then: soft hyphens are rejoined, the EUR-Lex page header, page numbers and the "EN EN" footer are removed, table-of-contents pages are dropped (they have many dotted lines) and footnote blocks are removed.

**One problem I fixed.** A chapter heading swallowed the Article heading that followed it, so 15 articles disappeared, including Article 5. I only saw it because a question about Article 5 could not find it. The title reader now stops at the next heading. A second problem: my original API request returned one vector for a whole list of texts, so a list of 16 texts silently gave 1 vector. The code now sends one `Content` per text and checks the number of vectors returned.

**Two chunking designs** (compared in Retrieval):

- `fixed`: 300-word windows with 50 words of overlap, ignoring structure. The naive baseline. The embedded text is the document title plus the chunk text.

- `structure`: one chunk per article or annex, or per numbered paragraph of the guidelines. Units over 380 words are split by paragraph, then by item, then by point, then by words. Short neighbours are packed up to 300 words and never cross an article or a heading. The embedded text adds a header "document, location, title".

One uncontrolled variable: `structure` also adds the context header to the embedded text, so the comparison is "structure + header" against "fixed", not structure alone.

**Chunk metadata.** `id, design, source, doc, location, title, text, page, page_from, page_to, articles, annexes, para_from, para_to, amended, words`. The citation shown to the model and the user is `[source | location]`, for example `[ai_act_consolidated_2026-07-27 | Article 99(1)–99(3)]`. Chunks: 562 (`structure`) and 488 (`fixed`), average 215 and 299 words.

**Embeddings and store.** `gemini-embedding-2`, 768 dimensions, normalised. The store is plain files in `index/` (chunks as JSONL, a vector cache keyed by a hash of the text, a registry of added documents). Search is a dot product with numpy. I chose plain files instead of ChromaDB so that the index works on Windows and macOS without a database binary and I can explain every line of it. The free tier allows about 1,000 embeddings a day, and vectors are saved after every batch.

## Test set

The test set contains 38 questions: 21 single-passage questions, 9 multi-passage questions and 8 questions that the indexed corpus cannot answer. In `eval/questions.csv`, each answerable question has a reference answer, an expected source and an expected location. For multi-passage questions, the two sources and locations are separated by a semicolon. Unanswerable questions have an empty expected-source field.

- Single, `q01`: "What is the maximum administrative fine for infringing the prohibitions of AI practices in Article 5?" (Article 99: EUR 35,000,000 or 7%, whichever is higher.)

- Unanswerable, `q32`: "Which Spanish authority supervises the AI Act and what is its address?" (the indexed documents do not identify the Spanish authority or give its address.)

A weakness: `q04` expects Article 5, but the guidelines (paragraph 241) also answer it correctly. The location check marks it as a retrieval miss although the answer is right (see Failures).

## Retrieval

A question counts as a hit at k when every expected passage is in the top k chunks (so a `multi` question needs both). The denominator is 30 answerable questions (21 single-passage and 9 multi-passage). The eight unanswerable questions are evaluated separately for refusal behaviour.

| Design | n | hit@1 | hit@3 | hit@5 |
|---|---|---|---|---|
| fixed, all | 30 | 50.0% | 60.0% | 73.3% |
| structure, all | 30 | 50.0% | 70.0% | 76.7% |
| fixed, single | 21 | 71.4% | 85.7% | 95.2% |
| structure, single | 21 | 71.4% | 90.5% | 95.2% |
| fixed, multi | 9 | 0% | 0% | 22.2% |
| structure, multi | 9 | 0% | 22.2% | 33.3% |

`structure` is equal or better at every k, but with 30 questions the difference is zero questions at k = 1, three at k = 3 and one at k = 5, so it is a weak signal, not proof. Two other arguments favour it: its citations are exact (an article or a paragraph, not "page 12"), and its chunks are shorter (215 against 299 words on average), so the five results add about 1,100 words to the prompt instead of about 1,500. **I chose `structure`** (`index/config.json`).

`multi` questions do badly because one query rarely brings two different passages into the top 5. The agent can search each part separately. The judge graded 9/9 final multi-passage answers as correct, while single-query retrieval with the structure design found both expected passages for 3/9 at k = 5. These checks measure different outcomes.

## Tools and subagent

`server.py` (MCP, stdio) exposes two tools:

- `search(query)`: describes the corpus, tells the model to copy the "cite as" string, says that the ranking always returns something (so the model must judge relevance) and flags amended passages. Example result: `Result 1 | cite as [guidelines_prohibited_practices_C2025-5052 | paragraphs (55)–(57)] | page 22 | score 0.81` followed by the passage.

- `add_document(path)`: adds a PDF/.txt/.md with the same pipeline; reports `added`, `already_indexed` (same content hash: nothing is embedded), or `replaced_previous_version`.

Subagent `.claude/agents/corpus-researcher.md`: tools limited to `mcp__corpus__search`; instructions: search before answering, answer only from results, cite with the "cite as" string, reply "The indexed documents do not cover this." when needed, separate law from guidelines, answer in a few sentences.

### Subagent transcript (Claude Code)

**User**

Use the existing corpus-researcher subagent to answer this question using its MCP search tool. Return the subagent’s answer with its citations.

Is it prohibited to infer the emotions of employees at work, and what exceptions apply?

**Claude Code**

Yes, it is prohibited. The only exception in the Act is for systems used for medical or safety reasons. Below is the corpus-researcher subagent's answer with its citations. Its first run failed because the corpus search server hadn't finished connecting; the second run worked.

The law (prohibition)

The AI Act prohibits selling, putting into service for this purpose, or using AI systems that infer the emotions of a person in the workplace or in education institutions. The only exception is a system intended for medical or safety reasons [ai_act_consolidated_2026-07-27 | Article 5(1)(f)–5(1)(g)].

That passage is not marked as amended, so the results show no 2026 change to this prohibition.

What the Commission guidelines say (their interpretation, not the law)

Who it applies to: both providers and deployers. All four conditions must be met: the system is sold, put into service or used; it infers emotions; it is in a workplace or education setting; and it has no medical or safety purpose [guidelines_prohibited_practices_C2025-5052 | paragraphs (242)–(243)].

What counts as the workplace: it is read broadly. It covers any physical or virtual work setting and any status (employee, contractor, trainee, volunteer), including job candidates during hiring [guidelines_prohibited_practices_C2025-5052 | paragraph (254)].

Examples:

A call centre that tracks employees' emotions by webcam or voice is prohibited.

The same tool used only for personal training is allowed if the results don't reach HR and can't affect assessment or promotion.

Tracking customers' emotions falls outside Article 5(1)(f).

[guidelines_prohibited_practices_C2025-5052 | paragraph (254)]

The exception is narrow:

"Medical" means CE-marked medical devices.

General wellbeing or stress monitoring is not covered, so detecting burnout or depression stays prohibited.

"Safety" means protecting life and health only, not protecting property against theft or fraud.

Use must be strictly necessary and proportionate, judged objectively, with less intrusive alternatives considered first.

[guidelines_prohibited_practices_C2025-5052 | paragraphs (256)–(259)]

What the exception covers:

Covered: helping employees with autism, and accessibility for blind or deaf people.

Not covered: assessing wellbeing, motivation or job satisfaction.

Stress or boredom: measuring them is prohibited unless there is a specific danger, such as operating dangerous machines or handling dangerous chemicals. Even then, the data can't be used for other purposes like assessing performance.

[guidelines_prohibited_practices_C2025-5052 | paragraph (263)]

Data and other laws:

The data may not be reused for any other purpose.

Systems that detect physical states such as fatigue (for example in pilots or drivers) are not emotion recognition systems at all.

Data protection law still applies to systems under the exception.

[guidelines_prohibited_practices_C2025-5052 | paragraphs (260)–(262)]

Systems outside the ban are high-risk under Annex III point (1)(c). They must meet the Chapter III Section 2 requirements and the Article 50(3) transparency obligation [guidelines_prohibited_practices_C2025-5052 | paragraph (239)] [guidelines_prohibited_practices_C2025-5052 | paragraph (263)].

Any decision about a real system should be checked by a legal professional.

### Harness examples (`agent.py`)

```text

QUESTION: Is it prohibited to infer the emotions of employees at work, and what exceptions apply?

[tool] search('infer emotions workplace employees prohibition exceptions') -> 7160 characters

[1 tool calls, guardrail: ok, 4022+588 tokens, 4.7 s]

Yes, it is prohibited to place on the market, put into service for this specific purpose, or use AI systems to infer the emotions of natural persons in the area of the workplace (which includes employees, candidates during recruitment, self-employed persons, and trainees) [cite as [guidelines_prohibited_practices_C2025-5052 | paragraph (254)], [guidelines_prohibited_practices_C2025-5052 | paragraph (241)], [guidelines_prohibited_practices_C2025-5052 | paragraph (242)–(243)]].

Exceptions:

The prohibition does not apply where the use of the AI system is intended to be put in place or into the market for medical or safety reasons [cite as [guidelines_prohibited_practices_C2025-5052 | paragraph (241)]].

* Medical reasons: Includes uses such as assisting employees with autism, but does not include assessing general wellbeing, motivation levels, job satisfaction, or anxiety based on measured stress levels [cite as [guidelines_prohibited_practices_C2025-5052 | paragraph (263)]].

* Safety reasons: Includes contexts where elevated stress levels or a lack of concentration pose a specific danger, such as when operating dangerous machinery or handling dangerous chemicals. Even in these cases, the data collected cannot be used for other purposes, such as assessing work performance [cite as [guidelines_prohibited_practices_C2025-5052 | paragraph (263)]].

* Additionally, the Commission guidelines state that if deployed strictly for personal training purposes (e.g., helping an individual cope with call centre customers), emotion recognition is allowed provided the results are not shared with HR and do not impact the work relationship [cite as [guidelines_prohibited_practices_C2025-5052 | paragraph (254)]], and physical states such as fatigue or pain are generally excluded from the definition of emotion recognition entirely [cite as [guidelines_prohibited_practices_C2025-5052 | paragraph (260)-(262)]].

(Note: This is a strict prohibition under Article 5(1)(f) of the AI Act; interpretation details are set out in the Commission guidelines. This matter should be checked by a legal professional before implementing any system.)

QUESTION: Which Spanish authority supervises the AI Act and what is its address?

[tool] search('Spain national competent authority address AI Act') -> 5602 characters

[tool] search('Spain Spanish address authority notification') -> 6680 characters

[2 tool calls, guardrail: ok, 7635+136 tokens, 4.4 s]

The indexed documents do not state which Spanish authority supervises the AI Act or its address. The text states that Member States are required to designate their national competent authorities and make their contact information publicly available, but it does not list the specific authorities or addresses for individual Member States [ai_act_consolidated_2026-07-27 | Article 70(1)-(2)].

This question should be checked by a legal professional.

```

The harness accepted the citation locations in both answers. The second answer declined to identify the authority. The model sometimes writes citations as `[cite as [...]]` (the same format slip as in `q28`); the citation guardrail accepts them because the content matches a retrieved passage.

## Adding a document

If the same file is added again, the tool answers `already_indexed` and makes 0 embedding calls. A file with the same name and different content replaces the old chunks.

**Experiment.** Unanswerable question `q31`: "At what training compute is a general-purpose AI model classified as general-purpose under the Commission guidelines (10^23 FLOPs)?" The question itself includes the threshold, so this comparison tests whether the added document supplies a citable source for it. The document added is `holdout/guidelines_gpai_C2025-7719.pdf` (68 chunks).

- **Before:** "The indexed documents do not cover a training compute threshold of 10^23 FLOPs ..." It adds the 10^25 systemic-risk presumption from Article 51(2). The answer declined to give the requested threshold from the original corpus.

- **Adding without approval:** the harness denies it ("The user did not approve adding this document").

- **Adding with approval (simulated):** `added: source 'guidelines_gpai_C2025-7719', 68 chunks, 68 new embeddings.`

- **After:** "an indicative criterion for a model to be considered a general-purpose AI model is that its training compute is greater than 10^23 FLOP and it can generate language ... [guidelines_gpai_C2025-7719 | paragraphs (17)–(19)]."

Running it exposed a real bug: the GPAI PDF gave 0 chunks because its text is indented differently on different pages. The paragraph detector now measures indentation relative to each page. The 562 chunks of the original corpus did not change. The experiment restores `index/` afterwards, so the committed index does not contain the GPAI document.

## Harness and guardrails

`agent.py` is a LangChain `create_agent` on Gemini (`gemini-3.5-flash-lite`), with the tools of `server.py` reached over MCP and `AGENTS.md` as system prompt. The rules in `AGENTS.md`, each with its reason there: search before answering; answer only from the results; cite every claim with the "cite as" string; say when the corpus does not cover the question; search once more before refusing; keep the law/guideline distinction; be short and recommend a legal check; add documents only with approval.

- **Approval:** `add_document` changes the index, so the harness asks the person (`y/N`) before it runs; without a person (evaluation) it is denied.

- **Call limit:** at most 6 tool calls per question.

- **Extra guardrail, citation check:** every `[source | location]` in the answer must be covered by a passage returned by a search in the same run (the same article, annex or paragraph range). If not, the model gets one repair turn; if the citation is still wrong it is removed from the answer. An answer written without any search also gets one turn to search.

**A case where it fired:** in an early test the model cited "Article 4(1)" and the search had returned the chunk "Article 4"; the check rejected it and forced a rewrite. That showed the check was too strict about granularity, so I changed it to accept a sub-paragraph inside an offered article. Afterwards it fired for 2 of 38 evaluation questions (`repaired_citations`), and no invalid citation reached an answer.

## Evaluation

**Submission check.** On 25 November 2026, `uv run python check.py --evaluate` finished with `All checks passed`. The check verified the Gemini connection, the 10.6 MB index and the test-set counts, called the MCP search tool and ran a live `main.py ask` query. The evaluation stage reused the 38 saved answers and wrote its results to `eval/summary.json`.

**Code checks.** All 38 runs included a search. Every citation present passed the location check. All 30 answerable responses included a citation. The refusal detector flagged 8/8 unanswerable responses and 0/30 answerable responses. The refusal check is a phrase search ("indexed documents do not cover/state/contain ..."). The first version missed phrasings such as "do not state", which counted four correct refusals as failures; I widened the phrases after seeing it.

**LLM judge:** `gemini-3.1-flash-lite` (a different model from the agent), with the question, the reference answer, the answer and all retrieved passages as evidence. Rubric: `correct` = states every key fact of the reference and does not contradict it, or, for unanswerable questions, clearly says the documents do not cover it and invents nothing; `supported` = every factual claim is in the retrieved passages (the legal-check sentence is ignored).

**Agreement with the judge.** Across the 38 answers, the ratings in `eval/human_labels.csv` agreed with the LLM judge on correctness in 36 cases (94.7%) and on support in 36 cases (94.7%). The disagreements were `q31` and `q37` for correctness, and `q02` and `q31` for support.

Cohen’s kappa was 0.000 for correctness and −0.027 for support. Most ratings were positive, so expected agreement by chance was already high. With so few negative cases the sample cannot tell me whether the judge detects errors.

**Results (judge):** correct 94.7% overall (single 100%, multi 100%, unanswerable 75%); supported 97.4%. The comparison file rated 38/38 answers correct and 37/38 supported. Refusal wording was detected in 8/8 unanswerable responses. The judge graded 6/8 of those responses as correct overall. The detector flagged 0/30 answerable responses as refusals.

## Failures

1. **Refusal grading disagreement (`q31` and `q37`).** The code check detected refusal wording in all eight unanswerable responses. The judge graded six as correct and flagged `q31` and `q37` as incorrect. In `q31`, the answer said the documents did not cover the requested threshold and then mentioned a different threshold from Article 51(2). In `q37`, the answer said the documents did not contain the requested guidance. The code check establishes that both responses included a refusal. Determining whether each full response met the rubric requires reviewing it against the retrieved passages.

2. **Unsupported claim, 1 question** (`q02`): the answer adds "or the proportionate limits established for their size", which is not in Article 99(6). Category: unsupported claim (small).

3. **Alternative evidence and expected-location mismatches** (`q04`): the expected passage is Article 5, the agent answered correctly from guidelines paragraph 241, so the location check counts a retrieval miss. 5 `multi` questions (`q22`, `q23`, `q24`, `q27`, `q30`) are also marked as not retrieving an expected passage, and 2 more (`q28`, `q29`) retrieved both but cited only one, although the answers were judged correct; the second passage was often covered by a different chunk than the one I listed. The hit rate for `multi` is probably a lower bound.

4. **Format problem, 1 question** (`q28`): citations written as "[cite as [...]]". The guardrail still accepted them because the content matched.

5. **Reference text outdated, 1 question** (`q03`): my reference says "ensure ... a sufficient level of AI literacy" (the original Article 4), the amended Article 4 says "support the development of AI literacy". The answer follows the amended text.

**What to fix first:** the judge (a stricter refusal rule), then add more negative cases, because with this test set the evaluation cannot discover many errors. Then test whether systematically issuing a separate query for each part improves retrieval on `multi` questions.

## Decision

**I would use this assistant to find and quote relevant passages from the AI Act and the Commission guidelines.** Before making a compliance decision, I would have a legal professional check the cited text. The corpus covers only three documents, and the 38-question evaluation contains too few observed errors to estimate how often the assistant might give a wrong answer with serious consequences.

The assistant checks citations against passages retrieved for the question and requires approval before adding a document. The code check detected refusals on all eight unanswerable questions. Before relying on the assistant in practice, I would test it on a larger set of difficult questions and verify the amended provisions against the Official Journal.

**Cost and latency per question** (38 questions, `gemini-3.5-flash-lite` for the agent): mean 6,475 tokens (median 4,698; total 246,061), mean 8.4 s (median 5.5 s), 1.4 tool calls on average. Most of the tokens are the search results (5 passages of about 215 words each).

## AI use

I used AI assistance to write and debug parts of the code. I also used it to revise wording in the report