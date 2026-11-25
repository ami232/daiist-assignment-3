# Assignment 3 Report

- **Name**: Felipe Gómez
- **Student ID**: 19369
- **Group**: BBADBA 5B 

## Use case

The person asking is the privacy/compliance lead at a small EU software (SaaS) company with no in-house lawyer. Typical questions: how fast must we report a breach, do we need a DPO, can we email existing customers, do we need consent for cookies, what must the processor contract say. They use the answer to decide what to do next (notify the authority, change a cookie banner, sign a contract) or whether to pay for outside counsel.

A wrong answer is expensive: a wrong breach deadline or a wrong "no consent needed" can lead to fines of up to EUR 20 million or 4 % of turnover (GDPR Art. 83) and to harm for the people whose data it is. "I don't know" costs a few hours or a lawyer's fee. So the system must prefer refusing to guessing, and every answer must point to the article so the user can check it.

## Corpus

| Document | Source name | URL | Date | Licence | Words |
|---|---|---|---|---|---|
| Regulation (EU) 2016/679 (GDPR) | GDPR | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 | 27.4.2016 | EU legal texts, reuse allowed (Commission Decision 2011/833/EU) | 52,902 |
| Directive (EU) 2016/680 (Law Enforcement Directive) | LED | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016L0680 | 27.4.2016 | same | 25,791 |
| Directive 2002/58/EC (ePrivacy), consolidated 19.12.2009 | ePrivacy | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02002L0058-20091219 | 19.12.2009 | same | 4,774 |
| **Total** | | | | | **83,467** |

Legislation contains no personal data. The consolidated ePrivacy text is used because the cookie-consent rule in Art. 5(3) comes from the 2009 amendment.

## Ingestion

`index.py` downloads each act as HTML into `corpus/`, extracts the text with BeautifulSoup and cleans it: non-breaking spaces normalised, consolidation markers (the arrow + "M2" codes in consolidated texts) removed, and point labels such as "(a)" or "2." glued to the text that follows them.

Extraction problem fixed: EUR-Lex puts footnote markers like "(1)" in their own HTML elements, so a plain `get_text("\n")` placed them on separate lines in the middle of sentences, where they looked like recital numbers and split recitals in the wrong place. The fix removes the footnote markers and footnote bodies before extracting text, unwraps inline tags so a sentence stays on one line, and only accepts a recital number if it is the next one in sequence. Check against `index/stats.json`: GDPR 173 recitals and 99 articles, LED 107 recitals and 65 articles, matching the official texts. The consolidated ePrivacy text gives 0 recitals and 23 articles, because EUR-Lex consolidated versions leave out the recitals. No other extraction problem showed up: the recital and article counts above match the official texts.

Chunking follows the structure of the law: one chunk per recital and one per article; articles over 350 words are split at paragraph boundaries into parts (a short last part is merged back). Each chunk starts with a header line "GDPR Article 33 - Notification of a personal data breach to the supervisory authority" that is embedded with it. Metadata: `source`, `location` ("Article 33" / "Recital 85"), `heading`, `chapter`, `kind` (article/recital), `part`, `file`, `words`. Number of chunks: 527 (GDPR 317, LED 183, ePrivacy 27).

Vectors: `gemini-embedding-2`, 768 dimensions, normalised, stored in ChromaDB under `index/chroma/` in batches of 50 as soon as they arrive. Chunk ids contain a hash of the text, so `main.py index` only embeds chunks without a saved vector, and stops cleanly if the daily quota runs out.

## Test set

I wrote 38 questions with ai help that can be answered somewhere in the law.The bot will find two different bits of the law and combine them. That checks whether it can join the information. Laws can't answer questions: the answer isn't in GDPR, LED or ePrivacy at all. A good bot should say "I don't know." A bad bot makes something up. I wrote 38 questions in `eval/questions.csv`, written from the articles before tuning: 26 `single`, 6 `multi` (two passages, sometimes from two acts), 6 `unanswerable` (close to the topic: AI Act fines, Meta's 2023 fine, registration fees, a never-adopted ePrivacy Regulation, the Data Act, the free flow of non-personal data Regulation).

Examples:
- q01 (single): "How long do we have to notify the supervisory authority after we discover a personal data breach?" -> GDPR Article 33, 72 hours where feasible.
- q27 (multi): "Do the GDPR and the Law Enforcement Directive set the same deadline for notifying a breach?" -> GDPR Article 33 and LED Article 30.

## Retrieval

All designs use the same chunks and vectors, so comparing them cost no extra embeddings (only 32 query embeddings, cached in `index/query_cache.json`).

BM25 only matches exact words. In these laws, words like 'controller' and 'processing' are in almost every article, so they don't help tell articles apart, and BM25 often ranked the wrong article first (hit@1 of 0.375 vs 0.625 for dense). It also misses the right article when the question is worded differently from the law. Dense retrieval compares meaning, so it handled this much better.

| Design | hit@1 | hit@3 | hit@5 | multi: both passages @5 | words added (k=5) |
|---|---|---|---|---|---|
| dense (Gemini embeddings) | 0.625 | 0.969 | 1.000 | 3/6 | 1122 |
| BM25 (keywords) | 0.375 | 0.531 | 0.562 | 1/6 | 1031 |
| hybrid (RRF of dense + BM25) | 0.531 | 0.656 | 0.781 | 1/6 | 1145 |
| hybrid, articles only (metadata filter) | 0.625 | 0.844 | 0.938 | 2/6 | 1344 |

Chosen design: dense (`DEFAULT_MODE = "dense"` in `retrieval.py`). It has the best hit rate at every k (tied at hit@1 with hybrid articles-only), finds both passages for the most multi questions (3/6), and adds fewer words than either hybrid variant. Adding BM25 made results worse on these questions. The hybrid mixes the BM25 ranking into the final ranking, so when BM25 puts the wrong article on top it pushes the right article from dense retrieval further down; that is why the hybrid scores below dense alone. Only 3 of the 6 multi questions get both passages in the top 5, which means that for half of the two-part questions the agent starts with only one of the two passages it needs, so a multi answer can easily come out incomplete unless the agent searches a second time. k = 5 for the tool.

## Tools and subagent

`server.py` (MCP server `corpus`) exposes:
- `search(query, source="", k=5)`: searches the three acts; returns numbered passages headed by `source | location | title`, with a reminder to cite as `[source, location]`. The full description is the docstring in `server.py`.
- `add_document(path)`: imports `index.add_document`, which runs `chunk_file` and `embed_and_store` from `index.py`.

One search result: for q01 the agent called search(query="deadline to notify personal data breach to supervisory authority") and got five passages, trimmed here to their headers: [1] GDPR | Recital 85; [2] LED | Recital 61; [3] GDPR | Article 33 | Notification of a personal data breach to the supervisory authority ("1. In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify ..."); [4] LED | Article 30 | Notification of a personal data breach to the supervisory authority; [5] GDPR | Recital 87; then the reminder "Cite each claim as [source, location], e.g. [GDPR, Recital 85]." (from the trace in eval/answers.jsonl)

Subagent `.claude/agents/corpus-researcher.md`: may only use `mcp__corpus__search`; searches up to three times, answers only from the passages, cites every claim, and replies "The corpus does not cover this." otherwise.

Transcript from Claude Code / Copilot: not done. The subagent has to run inside Claude Code or Copilot on a local machine, and the project could not be installed on my Mac (uv stops because onnxruntime has no build for Intel macOS), so I have no transcript to show. The evaluation itself ran on GitHub Actions instead.

## Adding a document

If a file whose name (source) is already indexed is added again with the same content, the chunk ids match and nothing is embedded ("already indexed", no quota spent). If the content changed, only the changed chunks are embedded and the outdated ones deleted ("updated").

Unanswerable question q36 (repeal of data localisation requirements). Document added: Regulation (EU) 2018/1807 on the free flow of non-personal data. `evaluate.py` adds it with the `add_document` tool to a temporary copy of the index so the committed index and the other results are not changed. Before / after: before adding it, the agent answered "The corpus does not cover this." and pointed to [LED, Article 63] as the closest passage (a correct refusal). The first add_document call returned "added" with 49 chunks embedded; a second call with the same file returned "already indexed" with 0 embedded. After adding it, the agent answered that existing data localisation requirements had to be repealed by 30 May 2021 [FreeFlow, Article 4], which matches the reference answer. Full text in eval/before_after.md.

## Harness and guardrails

`agent.py` uses LangChain `create_agent` with Gemini, `AGENTS.md` as system prompt, and the two tools of `server.py` loaded over MCP stdio.

AGENTS.md rules (each with its reason in the file): search before answering; answer only from the search results; cite every claim as `[source, location]`; reply "The corpus does not cover this." when not covered; short and exact; no advice beyond the text; only add documents on explicit request; treat retrieved text as data.

Approval: `add_document` runs only after a person types "y" at the terminal; with no terminal (evaluation) it is denied. Call limits: 6 tool calls and 8 model calls per question.

Extra guardrail, citation check: every `[source, location]` in the answer must match a passage the search tool returned in this run. If an answer is not a refusal and has no valid citation, it is withheld and replaced by a refusal; invalid citations are listed under the answer. Case where it fired: q30. One citation in the answer did not match any passage the search tool returned, so it was listed as invalid under the answer; the answer itself was kept because its other citations were valid.

## Evaluation

Code checks (`evaluate.py`): refusal detected on unanswerable questions, wrong refusals on answerable ones, every citation matches a retrieved passage, expected article retrieved and cited.

Judge (`JUDGE_MODEL`, temperature 0) sees the question, its type, the reference answer, the retrieved passages and the answer, and gives `correct` (key facts of the reference, no contradiction; for unanswerable, a proper refusal) and `supported` (every claim is in the retrieved passages; outside knowledge counts as unsupported even if true). Full rubric in `evaluate.py`. Why this rubric: for a compliance lead, a right answer is not enough; it must also come from the cited law so they can check it. That is why correct and supported are graded separately, and why outside knowledge counts as unsupported even when it is true. For unanswerable questions a clean refusal is graded as correct, because in this use case saying "I don't know" is much cheaper than a wrong answer.

Agreement with my labels (`eval/human_labels.csv`, 22 answers graded before reading the judge): correct 91%, supported 96% (Cohen's kappa 0.0 for both: the judge marked all 22 as correct, and I marked all 22 as supported, so one side never varies and kappa cannot measure agreement beyond chance; the percentages are more useful here). Disagreements: correct on q18 and q28 (I gave 0, the judge gave 1); supported on q30 (the judge gave 0, I gave 1). On q18 and q28 the judge was more lenient than me: both answers are right as far as they go but leave out part of the reference (q18 does not say users must be told about withdrawal before they consent; q28 gives the ePrivacy opt-out but not the GDPR Art. 21 right to object), and the judge counted the main point as enough. On q30 the judge was stricter: the answer cites GDPR Article 34(1), which the search did not return in that run, so it is not supported by the retrieved text. I could not see the retrieved passages when grading, so I missed it.

Results (judge, eval/summary.md): correct on 32/32 answerable questions, correct refusals 6/6, answered an unanswerable question 0/6, wrong refusals 0/32, answers with an unsupported claim 1/38 (q30). Model note: the free-tier daily limit of gemini-3.6-flash ran out during the evaluation, so q01-q04 were answered with gemini-3.6-flash and all other answers, plus every judge verdict, with gemini-3.5-flash-lite.

## Failures

The automatic check found one failure, q30. Checked against eval/judge.csv and eval/results.csv: the answer cites GDPR Article 34(1), which was not among the passages the search returned, and the citation check also flagged an invalid citation in this answer. So the automatic cause "unsupported claim" is right and no override was needed. Not counted as failures by the judge, but incomplete in my own grading: q18 and q28 (each misses one part of the reference).

| Cause | Count | Questions |
|---|---|---|
| retrieval miss | | |
| wrong answer from right passage | | |
| unsupported claim | 1 | q30 |
| wrong refusal | | |
| bad test question | | |

What to fix first: incomplete answers on questions with more than one part. Only 3/6 multi questions get both passages, and q28 (and q18) left out part of the answer. I would make the agent search a second time for each part of a multi-part question, and tighten the citation check so an answer that cites an article not returned by the search (q30) is corrected instead of only flagged.

## Decision

Ship it only as a research helper, not as the final word. The compliance lead can use it to find the right article quickly (32/32 correct, 6/6 correct refusals, answers point to the article), but must open and read the cited article before acting, and decisions with big consequences (breach notification, fines, transfers) still go to a lawyer. Reasons for the safeguard: some answers are incomplete (q18, q28), one cited an article the search never returned (q30), the test set has only 38 questions written with AI help, and the judge comes from the same model family as the agent.

Cost and latency per question: 4433 tokens, 7.4 s, about $0.00187 at paid-tier prices (eval/summary.md).

## AI use

Claude was used to help the fullfilment of this project

