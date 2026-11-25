# Assignment 3 Report

- **Name**: Javier Comín Segú
- **Student ID**: 20106
- **Group**: BBADBA 5A

## Use case

*Who asks, what they do with the answer, and what a wrong answer costs compared with "I don't know".*

The user is a compliance officer at a small EU company that develops or deploys an AI system and processes personal data. They ask what the AI Act, the GDPR or the Data Act require (for example the deadline to notify a personal data breach, or which AI practices are prohibited) and use the answer to decide whether a system or a contract is allowed to go ahead. A wrong answer is expensive: a fine, or a decision taken on a rule that does not exist (the GDPR and AI Act fines reach millions of euros). "I don't know" costs a few minutes of reading the text, so the assistant should prefer it to a plausible guess.

## Corpus

| Document | URL | Date | Licence | Words indexed |
|---|---|---|---|---|
| AI Act, Regulation (EU) 2024/1689 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689 | 2024-06-13 | (c) European Union, reuse authorised with acknowledgement (Decision 2011/833/EU) | 49,477 |
| GDPR, Regulation (EU) 2016/679 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679 | 2016-04-27 | same | 29,438 |
| Data Act, Regulation (EU) 2023/2854 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32023R2854 | 2023-12-13 | same | 21,211 |
| *Held out for the add-document test:* NIS2, Directive (EU) 2022/2555 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022L2555 | 2022-12-14 | same | 18,348 |

Total indexed at the start: 3 documents, 100,126 words (articles and annexes; recitals are left out, see Ingestion). Legislation contains no personal data. Licence, checked on 2026-11-25 against the European Commission legal notice (https://commission.europa.eu/legal-notice_en): the Commission's reuse policy is implemented by its Decision of 12 December 2011 (2011/833/EU); EU-owned content may be reused under CC BY 4.0, which requires credit and an indication of changes; third-party content, logos and industrial property are excluded. Here every passage is shown as extracted (whitespace cleaned, see Ingestion) and cited by document and article. The EUR-Lex legal notice page itself did not load in my check, so the table says only "reuse authorised with acknowledgement". The texts are downloaded by `index.py` from the Publications Office (`publications.europa.eu`, content negotiation for XHTML) because EUR-Lex itself blocks scripted requests.

## Ingestion

*How you extract, clean and chunk; one extraction problem you fixed; chunk metadata; number of chunks.*

- **Extract**: the XHTML of the Official Journal is parsed with BeautifulSoup. Articles, annexes (and optionally recitals) are found by their element ids (`art_N`, `anx_X`, `rct_N`); chapter and section titles come from the enclosing elements. Lists, which the Journal encodes as two-column tables (marker | text), are flattened to lines that keep their marker, so `(a)` stays attached to its text.
- **Clean**: footnote paragraphs, soft hyphens, zero-width spaces and non-breaking spaces are removed; whitespace is collapsed.
- **Chunk, design `article` (structure-based)**: one chunk per article or annex. An article above 450 words is split at paragraph or point boundaries into pieces of about 300 words, so a chunk never cuts a sentence in the middle of a paragraph. Each chunk starts with a header, for example `GDPR, Article 28(3) (part 2/4) - Processor [CHAPTER IV - ...]`, and that header is part of the embedded text.
- **Chunk, design `fixed` (baseline)**: a sliding window of 250 words with 25 words of overlap, ignoring structure; the window is about as large as an average article chunk (about 215 words), so the comparison isolates the effect of structure.
- **Metadata** on every chunk: `source` (short document name), `location` (article with paragraph or point range, annex with points, or page for a PDF), `units` (articles covered), `chapter`, `title`, `words`, and the vector. Chunk ids contain a hash of the text, so a rerun embeds only chunks without a saved vector.
- **Recitals** are excluded by default (`include_recitals=False` in `DOCS`): they would double the number of chunks and the free embedding quota is about 1,000 texts a day.
- **Extraction problem fixed**: the first parser returned about ten words for Article 3 of the AI Act and Article 4 of the GDPR, the definitions. They are lists inside tables that are direct children of the article, and my flattening function only looked inside the children of a block. Fixing it recovered the definitions (Article 3 became 10 chunks of 180 to 300 words, and the corpus grew by about 7,500 words). A second, minor one: one article title in the official file ends in a stray grave accent, removed in `clean()`.
- **Number of chunks**: 461 (`article`) and 446 (`fixed`) for the three documents. `uv run python index.py --stats` prints this without calling the API.

## Test set

eval/questions.csv has 37 questions: 22 single, 8 multi (two passages, e.g. GDPR Art. 33 + Art. 34, or AI Act Art. 5 + Art. 99) and 7 unanswerable. They cover the AI Act, the GDPR and the Data Act, and the unanswerable ones stay close to the topic (e.g. a Digital Services Act penalty, the Spanish supervisory authority, a fine on a named company, an "AI officer" rule that does not exist). One of them (q31, NIS2 early warning deadline) is answered by NIS2, which is held out of the index on purpose for the before/after test.

I wrote the questions myself, although Claude helped me with the wording of some questions and provided ideas about what I could ask. Every expected_location was checked by code against the chunks produced by the index. No question was written or changed after seeing any retrieval or agent result.

One reference answer had a formatting error: in q17 (AI Act Art. 73) an unquoted comma split the CSV field, so the last clause ("ten days in the event of a death") was dropped when the file was read. The corrected row, a single quoted field, reached my local copy only after the final evaluation run, so the judge graded q17 against the shorter reference. I did not re-judge q17; all other rows and all agent answers are unchanged.

## Retrieval

*Hit rate at 1/3/5 per design, words added to the prompt, the design you chose.*

Designs compared by `main.py evaluate` (`eval/retrieval_results.csv`): `fixed` and `article` chunking, each with vector search and with hybrid search (vector ranking and BM25 fused by reciprocal rank). Hybrid reuses the same vectors, so it costs no extra embeddings. A hit means a returned chunk comes from the expected source and covers the expected article, annex or recital; for a `multi` question every expected passage must be in the top k.

Results over the 30 answerable questions (counts in brackets; `multi all@5` is the 8 multi-passage questions with every passage in the top 5):

| design | search | chunks | hit@1 | hit@3 | hit@5 | multi all@5 | words in top 5 |
|---|---|---|---|---|---|---|---|
| fixed | vector | 446 | 0.73 (22) | 0.83 (25) | 0.90 (27) | 0.625 (5/8) | 1,248 |
| article | vector | 461 | 0.70 (21) | 0.87 (26) | 0.87 (26) | 0.50 (4/8) | 1,161 |
| **article (chosen)** | **hybrid (chosen)** | 461 | 0.63 (19) | 0.77 (23) | 0.87 (26) | 0.625 (5/8) | 1,219 |
| fixed | hybrid | 446 | 0.70 (21) | 0.80 (24) | 0.87 (26) | 0.625 (5/8) | 1,248 |

By hit rate alone `fixed` with vector search is the best design (22, 25 and 27 of 30 at k = 1, 3 and 5) and `article` with hybrid search, the one in use, is the weakest at k = 1 and k = 3 (19 and 23 of 30), so the numbers do not favour my choice at k = 1 and I say so. I kept `article`/hybrid for four reasons. (1) The agent reads the top 5, and at k = 5 the four designs differ by one question at most (26 or 27 of 30), which is too small a gap to call. (2) The weak spot is the multi-passage questions, and three of the four designs find all passages for 5 of the 8 and the fourth for 4, so changing the chunking does not fix it; query decomposition would. (3) `article` chunks never mix two articles, so a citation points to one article. Fixed windows ignore structure and can span two. (4) The end-to-end evaluation and my 37 labels were produced with this setup; switching would have meant rerunning the agent and grading everything again. If I had more time I would switch to `fixed`/vector and regrade. To change the design the server uses, edit `CHOSEN_DESIGN` in `index.py` and `CHOSEN_MODE` in `retrieval.py`.

## Tools and subagent

*Your tools' descriptions, one search result, the subagent's instructions, one transcript from your editor.*

`server.py` exposes two tools over MCP (stdio):

- **`search(query, source="", k=5)`**: its description says what the corpus is (EU legislation only: no case law, guidance or national law), when to use it, how to write the query, and how to cite what it returns. It returns passages best first, each headed by `[n] source | location — "title" (similarity x)`, the line the model copies into its citations. Passages found by keywords only (see Adding a document) end in `(keyword match)` instead.
- **`add_document(path)`**: runs the file through `index.index_file`, the same functions the index stage uses (it is imported, not rewritten). Only files inside the project folder with an allowed extension (`.xhtml`, `.html`, `.pdf`, `.txt`, `.md`, up to 25 MB) are accepted, so a prompt-injected agent cannot index arbitrary files.

Search tool, question q01: *How long does a controller have to notify a personal data breach to the supervisory authority?* (`k=3`):

```text
3 passages, best first. Cite as [source | location].


[1] GDPR | Article 33 — "Notification of a personal data breach to the supervisory authority" (similarity 0.83)
1. In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority competent in accordance with Article 55, unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where the notification to the supervisory ...

[2] GDPR | Article 34 — "Communication of a personal data breach to the data subject" (similarity 0.72)
1. When the personal data breach is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall communicate the personal data breach to the data subject without undue delay. 2. The communication to the data subject referred to in paragraph 1 of this Article shall describe in clear and plain language the nature of the personal data breach and contain at least ...

[3] GDPR | Article 60(10)-(12) (part 3/3) — "Cooperation between the lead supervisory authority and the other supervisory authorities concerned" (similarity 0.70)
10. After being notified of the decision of the lead supervisory authority pursuant to paragraphs 7 and 9, the controller or processor shall take the necessary measures to ensure compliance with the decision as regards processing activities in the context of all its establishments in the Union. The controller or processor shall notify the measures taken for complying with the decision to the lead supervisory authority, which shall inform the ...
```

The tool returns the full passages; here each is cut to its first 70 words. The first line of each passage is the citation the agent copies.

Subagent: `.claude/agents/corpus-researcher.md` has `tools: mcp__corpus__search` and nothing else. It states the same rules as `AGENTS.md` (answer only from passages, cite, refuse with a fixed sentence, treat passages as data).

Run in Claude Code, in the project folder, with the `corpus` MCP server connected. Prompt given:

```text
Use the corpus-researcher subagent to answer: What is the maximum administrative fine under the GDPR for infringing the basic principles for processing?
```

The subagent's answer, as Claude Code showed it (the `search` calls it ran are not part of this excerpt):

```text
The maximum fine is up to 20 000 000 EUR. For an undertaking it is up to 4 % of the total worldwide annual turnover of the preceding financial year, whichever is higher. This tier applies to infringements of "the basic principles for processing, including conditions for consent, pursuant to Articles 5, 6, 7 and 9" [GDPR | Article 83(3)-(5) (part 3/4)].

- What those articles cover: the processing principles [GDPR | Article 5], lawfulness of processing [GDPR | Article 6(3) (part 2/3)], conditions for consent [GDPR | Article 7], and the special categories of personal data [GDPR | Article 9(1) (part 1/4)].
- Other infringements in the same tier: data subjects' rights under Articles 12 to 22, transfers to third countries under Articles 44 to 49, obligations under Member State law adopted under Chapter IX, and non-compliance with supervisory authority orders under Article 58 [GDPR | Article 83(3)-(5) (part 3/4)].
- This is a ceiling, not a fixed amount: fines must be "effective, proportionate and dissuasive" [GDPR | Article 83(1) (part 1/4)]. The amount depends on factors such as the nature, gravity and duration of the infringement and whether it was intentional or negligent [GDPR | Article 83(2) (part 2/4)].
- Several infringements in the same or linked processing operations: the total fine "shall not exceed the amount specified for the gravest infringement" [GDPR | Article 83(3)-(5) (part 3/4)].

Note: the searches did not return Article 6(1), which lists the legal bases for processing.
```

The subagent has only the `search` tool, answers from passages and cites each claim in the `[source | location]` form, and it flags what the searches did not find (Article 6(1)).

## Adding a document

*What happens when a document is already indexed. The unanswerable question, the document you added, the answer before and after.*

- **Same file again** (identical content, compared by SHA-256): nothing is embedded; the tool reports the existing entry and its number of passages.
- **Same document name, changed content**: the document's old passages are replaced. Chunk ids contain a hash of the text, so passages that did not change keep their saved vectors and only new ones are embedded.
- **New document**: its passages are embedded in batches, appended to `index/article/chunks.jsonl` as they arrive, and searchable immediately. If the free daily embedding quota runs out, `add_document` still adds the passages, without a vector, and says so; `search` then finds them by keywords (BM25) and marks them `(keyword match)`. Adding the same file again once the quota has reset creates the vectors. `search` itself also falls back to keyword ranking when it cannot embed the question.

**Question** (q31, unanswerable on purpose, answered by NIS2 Art. 23): *What is the deadline for an essential entity to submit an early warning of a significant cybersecurity incident to its CSIRT?* The document added is NIS2 (`corpus/nis2.xhtml`, Directive (EU) 2022/2555), held out of the index until now. The demo (`before_after.py`) runs on a throw-away copy of `index/`; the agent adds the file after a human approval step.

**Before:** *I don't know based on the indexed documents. I searched for the deadline for an essential entity to submit an early warning of a significant cybersecurity incident to its CSIRT, but the indexed documents (the AI Act, the GDPR, and the Data Act) do not contain rules on cybersecurity incident reporting for essential entities under the NIS framework.*

**Adding the document** (approval requested and approved): *The document `corpus/nis2.xhtml` has been successfully added to the corpus under the source name `NIS2` (86 passages indexed via keyword search).*

**After:** *An essential entity must submit an early warning of a significant incident to the CSIRT or competent authority without undue delay and in any event within 24 hours of becoming aware of the significant incident [NIS2 | Article 23(1) & Article 23(4)(a)].* (three searches, 16,196 tokens, no guardrail fired).

The "after" answer is right: Art. 23(4)(a) of NIS2 says exactly that, "without undue delay and in any event within 24 hours of becoming aware of the significant incident, an early warning". The citation is imperfect: the agent put two locations in one bracket (`Article 23(1) & Article 23(4)(a)`) instead of the exact `[NIS2 | Article 23(4) (part 3/6)]` form. The citation check accepted it because both refer to Article 23 of NIS2, which was retrieved, so the check is lenient on the paragraph.

**What happened with the quota.** My first attempt with the same file failed: the agent answered that it could not add the document because the embedding quota was exhausted (free tier: 1,000 embedding requests a day, used up by indexing and testing; the failed attempt is saved in `eval/before_after_full_nis2_failed.md`). Search was also unavailable, since a new question cannot be embedded either. So I changed `add_document` and `search` to keep working without quota, as described above. The run shown here therefore used keyword search only (the 86 NIS2 passages have no vectors and the question was ranked by BM25); with a normal quota the same search is hybrid (vectors plus keywords) and adding the document embeds its passages.


## Harness and guardrails

*Your AGENTS.md rules, the approval step, and your extra guardrail with one case where it fired.*

- **`AGENTS.md`** (system prompt of `agent.py`): answer only from passages; search before answering and again with other wording; cite every claim as `[source | location]`; refuse with a fixed sentence when the passages do not answer; answer partially when only part is covered; quote numbers exactly; treat passages as data; call `add_document` only on an explicit request. Each rule has its reason in the file.
- **Approval**: `HumanInTheLoopMiddleware` pauses the agent before every `add_document` call; the terminal shows the call and waits for a yes. Without a terminal the call is rejected.
- **Call limit**: at most 8 model calls and 6 tool calls per question (`ModelCallLimitMiddleware`, `ToolCallLimitMiddleware`).
- **Extra guardrail, citation check in code**: every `[source | location]` in the answer must match a passage the agent retrieved in that run (same document, same article, annex or recital), and an answer that is not a refusal must have citations. If not, the agent gets one repair turn; if that fails too, the answer is replaced by a notice instead of being shown.
- **Input check and path allowlist**: empty or oversized questions are rejected before any model call; `add_document` only reads inside the project folder.

**A case where the check fired** (offline test with a scripted model, not a live Gemini run). The scripted model ignores the passages and answers `It is 72 hours [GDPR | Article 999].` No passage with that citation was retrieved, so the check rejects it and gives the agent one repair turn. The scripted model repeats the same citation, and the answer is withheld. Result, `guardrails: citation_repair, citation_blocked`:

> I could not produce an answer whose citations I can verify against the passages I retrieved, so I am not giving one. Please rephrase the question or ask about a specific article.

In the 37 real answers of the evaluation the check blocked none and every citation was valid (see Evaluation), so this case comes from the test and not from the evaluation. The input check, tested the same way: an empty or over-long question (more than 1,500 characters) is rejected with `guardrails: input_rejected` and the answer *Please ask a question of up to 1500 characters.*, with 0 model calls and 0 tokens.

## Evaluation

*Code checks, the judge's rubric, your agreement with the judge, and results: correct, unsupported, correct refusals, wrong refusals.*

- **In code**: whether the answer is a refusal (it starts with the fixed sentence), whether every citation is a retrieved passage, whether the expected passage was retrieved and cited, tokens and seconds.
- **LLM judge**: a Gemini model grades `correct` (same substantive content as the reference answer; both parts for `multi`; confident answers to `unanswerable` questions are wrong) and `supported` (every claim is in the retrieved passages). The rubric is in `evaluate.py`; refusals and guardrail blocks are decided in code and not sent to the judge. The rubric tells the judge to be strict and grade content, not style. `correct` = 1 only if the answer has the same substantive content as the reference (same rule, numbers, deadlines and conditions, nothing essential missing, and for a `multi` question both parts); 0 if it contradicts the reference, leaves out something essential or answers an unanswerable question confidently; extra detail that is true and relevant does not lower it. `supported` = 1 only if every factual claim is stated in the passages the assistant retrieved; 0 if any claim is not in them, even if it is true, and a citation does not make a claim supported.
- **Agreement with me**: `eval/human_labels.csv` has my grades for all 37 answers (criterion below). `main.py evaluate` reports percentage agreement and Cohen's kappa.

**My labelling criterion** (`eval/human_labels.csv`, 37 answers, all graded by me with `label.py`): `supported` = 1 unless the answer states something that is not in the documents or contradicts them; `correct` = 1 when it gives the substance of the reference answer, and for a `multi` question every component the question asks for.

Results of `uv run python main.py evaluate` (37 questions: 22 single, 8 multi, 7 unanswerable; design `article`/hybrid):

| measure | result |
|---|---|
| Correct answers (answerable), by the judge | 26 / 30 (87 %) |
| Unsupported answers | 1 of 30 answers given |
| Correct refusals (unanswerable) | 7 / 7 (answered anyway: 0; blocked by the guardrail: 0) |
| Wrong refusals (answerable) | 0 / 30 |
| Answers blocked by the citation check | 0 |
| Valid citations | 37 / 37 |
| Agreement with my 37 labels, `correct` | 95 % (Cohen's kappa 0.64); disagreements on q20 and q29 |
| Agreement with my 37 labels, `supported` | 95 % (kappa -0.03); disagreements on q02 and q12 |
| Agreement on both | 89 % |

Two cautions about these figures. The agreement is computed on all 37 labels, but 7 verdicts (the refusals) are decided in code and agree by construction; over the 30 answers the LLM actually judged it is 28/30 (93 %) for `correct` and 28/30 (93 %) for `supported`. The kappa for `supported` is close to zero although the raw agreement is 95 % because almost every answer is supported in both gradings, and kappa is unstable when one class is that rare.

**Where I disagree with the judge** (four answers; the judge's reasons are in `eval/judge_verdicts.csv`).

- **q02, `supported`: judge 0, me 1.** The answer adds "direct marketing" and "children". They are not in the passage it cites but they are in GDPR Arts. 21 and 8, so I counted them as supported by the documents. The judge's rubric is stricter: every claim must be stated in the passages the assistant retrieved. That is the usual meaning of "grounded" in a RAG system, so here the difference is one of criterion more than a judge error, and my criterion is the more lenient one.
- **q12, `supported`: judge 1, me 0.** The sentence about SMEs adds "limits set for SMEs", which Art. 99(6) does not say in those words. Here I was stricter than the judge.
- **q20, `correct`: judge 0, me 1.** The question asks from when providers may no longer charge for switching; the answer gives the date. The judge penalised the missing transitional period, which is in my reference answer but is not what the question asks. The judge was too strict, and the reference answer is broader than the question.
- **q29, `correct`: judge 0, me 1.** The answer states how the Data Act right relates to the GDPR rights (Art. 1(5)) but does not cite or explain GDPR Art. 20, which my reference includes. I counted the relation the question asks about as complete; the judge counted the missing Art. 20 content as an omission. It also shows the retrieval weakness on multi-document questions (the GDPR passage was never retrieved), so the judge's complaint is not baseless.

Both disagreements on `correct` come from `gemma-4-31b-it` (2 of its 16 answers) and both on `supported` from `gemini-3-flash-preview` (2 of its 14), which suggests the stricter reading of completeness belongs to Gemma and the stricter reading of grounding to Gemini; with so few answers I would not push that further.

**The judge.** Free-tier Gemini keys allow 20 requests per model per day, so the 30 answers were graded by two models, none of them the agent: `gemini-3-flash-preview` and `gemma-4-31b-it` (a Gemma model, not Gemini). Of the 30 answers sent to a judge, `gemini-3-flash-preview` graded 14 and `gemma-4-31b-it` 16; the other 7 verdicts (refusals) are decided in code. The judge is not very stable: earlier runs of the same answers, graded partly by `gemini-3.5-flash` and partly by the agent model itself (the quota ran out), gave 29 and then 27 correct answers out of 30, against 26 in the final run, so a difference of one or two answers between runs is noise and I read the figures that way. The model that graded each answer is in the `by` column of `eval/judge_verdicts.csv`. The Gemini 3.x models ignore the temperature setting (LangChain warns that they use fixed sampling defaults), so the agent's answers are not deterministic; they are cached in `eval/answers.jsonl`, and all figures here come from one run of the agent.

## Failures

*Failed questions by cause, with counts, and what to fix first.*

`eval/failures.csv` lists the 5 answers the judge marked as failures. My own labels flag 3 (q12, q27, q28); q02, q20 and q29 are the disagreements discussed above. `final_cause` in that file holds the causes below.

| id | kind | cause | what happened |
|---|---|---|---|
| q27 | multi | `wrong_answer_right_passage` | The code check says both expected passages were retrieved, but the answer gives only the AI Act exception (Art. 10(5)) and leaves out the general GDPR prohibition (Art. 9(1)). Judge and I agree it is incomplete. |
| q28 | multi | `retrieval_miss` | GDPR Art. 22 was never retrieved; the answer covers only the AI Act side. Judge and I agree. |
| q29 | multi | `retrieval_miss` | GDPR Art. 20 was never retrieved. The judge marked it incorrect; I marked it correct because the relation asked about is stated. |
| q20 | single | `bad_test_question` | My reference answer includes the transitional period, which the question does not ask for. I marked it correct. |
| q02 | single | `unsupported_claim` | The judge flags "children"; I marked it supported (see above). |

By cause, on the judge's 5: `retrieval_miss` 2, `wrong_answer_right_passage` 1, `bad_test_question` 1, `unsupported_claim` 1. On my own labels (3 failures): `unsupported_claim` 1 (q12, the SME phrase, which the judge did not flag), `wrong_answer_right_passage` 1 (q27) and `retrieval_miss` 1 (q28).

The pattern is clear: **in q27, q28 and q29 the half that comes from the GDPR is the one that is missing**, in questions that cross the GDPR with the AI Act or the Data Act. What I would fix first is how multi-document questions are searched: a second search restricted to the other document (`source="GDPR"`) for any question that mentions two regulations. `AGENTS.md` rule 2 already asks for one search per part, but the agent does not always follow it, so I would check it in code instead of trusting the prompt.

## Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

Cost per question, from the same run: 6,203 tokens on average (95th percentile 16,033), 10.7 s (95th percentile 15.8 s) and 2.3 model calls (agent model `gemini-3.5-flash-lite`; the judge adds one call per answer).

I would let a compliance officer use it as a first reader that finds the article and quotes it, not as the final word. On my 37 questions the judge found 26 of 30 answerable ones correct (87 %), every citation was valid, one answer was unsupported, and it refused all 7 unanswerable ones instead of guessing. The risk is in what the test set barely measures: questions that need two documents (5 of 8 have every passage in the top 5, so a missing passage can make an answer look complete when it is not) and the small number of questions per case. The safeguard I would require is that the user checks the cited article before acting, which the `[source | location]` citations make possible, and that questions across documents are always re-read in full. At about 10 s and a few thousand tokens per question the cost is not the problem. First fix: retrieve each part of a multi-document question separately.

## AI use

*What you used and how, or "none".*

I used Claude throughout the project while complying with the AI policy. I initially used it to gain an overview of the project and better understand its requirements. I also used it to refine certain parts of my code and help me correct grammatical errors. I relied on it most when I ran out of my usage quota in the terminal and had to explore alternative solutions to continue working. Additionally, I used Claude to ensure that everything met the project requirements, that I had not overlooked anything, and to review my work for any potential issues.
