# Assignment 3 Report

- **Name**: Jaime Lopez-Baillo Gallego
- **Student ID**: 19031
- **Group**: BBADBA 5A

## Use case

A **startup compliance officer** (often a founder or the first legal officer but not a lawyer) asks whether the startup's AI product is prohibited, high-risk or otherwise regulated, and what duties follow: AI Act classification, GDPR duties and DSA duties for online platforms. They use the answer to decide what to build, what to document and when to pay for a lawyer.

A wrong answer is expensive: AI Act fines go up to EUR 35 000 000 or 7 % of worldwide turnover, GDPR and DSA fines up to 4 % and 6 %. Saying a product is not high-risk when it is means skipped conformity duties; inventing an obligation wastes scarce startup money. "The corpus does not cover this" is cheap by comparison: it sends the officer to a lawyer or the official guidance. So the system is designed to refuse rather than guess, and to cite every claim so it can be checked.

## Corpus

| Document | URL | Date | Licence | Words (indexed) |
|---|---|---|---|---|
| Artificial Intelligence Act, Regulation (EU) 2024/1689 | https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202401689 | 13 June 2024 (OJ 12 July 2024) | EUR-Lex, reuse authorised (Commission Decision 2011/833/EU), © European Union | 86 747 |
| General Data Protection Regulation, Regulation (EU) 2016/679 | https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32016R0679 | 27 April 2016 | same | 53 164 |
| Digital Services Act, Regulation (EU) 2022/2065 | https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32022R2065 | 19 October 2022 | same | 61 533 |
| *Added later:* GPAI Code of Practice, Copyright chapter | https://ec.europa.eu/newsroom/dae/redirection/document/118115 | 10 July 2025 | European Commission, © European Union | ~1 500 |

About 200 000 words in total. The PDFs are in `sources/`.

## Ingestion

**Extraction.** `index.py` reads each PDF with `pypdf` and keeps text by font size: body text is 9.6 pt, footnotes 8.5 pt, so footnotes, running headers/footers ("L 119/1", "Official Journal of the European Union", page numbers) are dropped.

**Problem fixed.** The first version of the font filter also dropped the recital numbers "(1)", "(2)"…, the "CHAPTER I" headings and "HAVE ADOPTED THIS REGULATION", because they are printed small too. Without them the parser could not tell recitals from articles. Fix: an allow-list of structural markers that are kept even at small size (`SMALL_FONT_KEEP`), plus keeping all-caps chapter titles. A second bug: chapter titles were swallowing the following "Article N" line; fixed with a guard in the parser.

**Chunking: by legal structure, not fixed windows.** A legal text is cited by article, paragraph, recital and annex point, so each chunk is one recital, one article (long articles split into groups of paragraphs, max ~350 words, e.g. "Article 6(1)-(3)") or one annex point. Each chunk starts with a heading ("AI Act, Article 6(1)-(3) (Classification rules for high-risk AI systems) [Chapter III]") so the embedding knows where it is. Documents that are not regulations (no "HAVE ADOPTED THIS REGULATION") fall back to 300-word windows with 50-word overlap, cited by page.

**Metadata per chunk:** source, location (citation), kind (article/recital/annex), article number, title, chapter, page start/end, words, file name, file hash.

**Numbers:** 828 chunks (AI Act 342, DSA 253, GDPR 233; 486 article chunks, 312 recital chunks, 30 annex chunks), median 263 words. Embeddings: `gemini-embedding-2`, 768 dimensions, stored in Chroma (`index/chroma`) with a cache of vectors (`index/embeddings.jsonl`) so the corpus is never re-embedded.

## Test set

47 questions in `eval/questions.csv`, written from the perspective of a startup asking about its product, each with an expected source, location and a reference answer taken from the text.

| Kind | Count |
|---|---|
| single (one passage answers it) | 28 |
| multi (needs two passages, often two laws) | 11 |
| unanswerable (not in the three laws) | 8 |

Examples:
- *single* q03: "How quickly must a controller notify a personal data breach to the supervisory authority?" → GDPR Article 33: without undue delay and, where feasible, within 72 hours.
- *multi* q29: "A company uses an AI tool to screen job candidates in the EU. Which obligations apply under the AI Act and the GDPR?" → AI Act Annex III point 4(a) (high-risk) and GDPR Article 22 (automated decisions).
- *unanswerable* q40: "What is the exact fine in euros that Spain imposes for breaching the AI Act?" → national penalty rules are not in the corpus; Article 99 only sets caps.

## Retrieval

Three search methods over the same structure chunks (`eval/retrieval_summary.csv`, 39 answerable questions, a hit = the expected article/recital/annex is in the top k):

| Design | hit@1 | hit@3 | hit@5 | both parts of multi in top 5 | words added to prompt (top 5) |
|---|---|---|---|---|---|
| **structure** (dense vectors) | 0.615 | 0.949 | **1.000** | 0.182 | 1 362 |
| structure+hybrid (dense + BM25, RRF) | 0.564 | 0.821 | 0.949 | 0.182 | 1 343 |
| structure+filter (dense, restricted to the law named in the query) | 0.615 | 0.949 | **1.000** | 0.182 | 1 350 |

**Chosen: `structure`.** It ties the filter at hit@5 = 1.0 and is simpler. Hybrid was worse at every k: keyword matching pulls in passages that share common legal words ("provider", "data", "Article") but are the wrong article. The filter gave no measured gain and has a risk for this use case: if a user names the GDPR but the obligation is in the AI Act, the filter hides the right passage. Weak spot: one search finds both parts of a multi question only 18 % of the time, so the agent is told to search each part separately (AGENTS.md rule 4).

## Tools and subagent

**MCP server** (`server.py`, stdio) with two tools:

- `search(query)`: "Search EU law for startup compliance: the AI Act, the GDPR and the Digital Services Act, including their recitals and the AI Act annexes, plus any document added later. Phrase the query in the regulation's own terms. Returns the 5 most relevant passages, each headed by "CITE AS: [<law>, <article/recital/annex>]". If none of them answers the question, the corpus does not cover it."
- `add_document(path)`: "Add a document (PDF, .txt or .md) to the search index: it is extracted, chunked by article/recital where it has that structure (fixed-size windows otherwise), embedded and stored. If the same file content is already indexed nothing is done; if a file with the same name but different content is indexed, the old version's chunks are replaced."

One search result (query "notification of a personal data breach to the supervisory authority"):

```
[1] CITE AS: [GDPR, Article 33] — Notification of a personal data breach to the supervisory authority (p. 52)
1. In the case of a personal data breach, the controller shall without undue delay and, where feasible,
not later than 72 hours after having become aware of it, notify the personal data breach to the
supervisory authority competent in accordance with Article 55, unless ...
```

**Subagent** (`.claude/agents/corpus-researcher.md`, only tool `mcp__corpus__search`): search with the regulation's vocabulary (at most 4 searches), answer in at most 150 words, cite every claim in the CITE AS bracket form, copy numbers exactly, and start with "The corpus does not cover this question." when the results don't answer it.

**Transcript (Claude Code):**

```
> Our startup sells an AI system that banks use to evaluate the creditworthiness of loan
  applicants. Is it high-risk under the AI Act, and is there any exception?

● corpus-researcher (tools: mcp__corpus__search) — 2 searches, 11 s

  **Answer:** Yes, almost certainly high-risk. The exceptions are narrow and probably do not
  apply if the system profiles applicants.

  - **Listed use case:** Annex III covers "AI systems intended to be used to evaluate the
    creditworthiness of natural persons or establish their credit score" [AI Act, Annex III,
    points 4-5]. AI systems referred to in Annex III "shall be considered to be high-risk"
    [AI Act, Article 6(1)-(3)]. The reason given is that they decide access to financial
    resources and essential services, and may lead to discrimination [AI Act, Recital 58].
  - **Listed exclusion:** AI systems "used for the purpose of detecting financial fraud" are
    excluded [AI Act, Annex III, points 4-5]. AI systems that Union law provides for prudential
    capital-requirement calculations are also not high-risk [AI Act, Recital 58].
  - **Article 6(3) exception:** A system is not high-risk if it only does a narrow procedural
    task, improves a completed human activity, detects deviations in decision patterns, or does
    a preparatory task. However, it "shall always be considered to be high-risk where the AI
    system performs profiling of natural persons" [AI Act, Article 6(1)-(3)]. Scoring
    individual applicants is likely profiling.
  - **If you rely on an exception:** You must document the assessment before placing the system
    on the market and register it under Article 49(2) [AI Act, Article 6(4)-(8)].

  **Facts that would change the answer:** whether the system profiles applicants or only does
  preparatory or procedural work.
```

The subagent used only the `search` tool, cited every claim in the CITE AS form and ended with the facts that would change the verdict, as its instructions require.

## Adding a document

`add_document` hashes the file: the same content already indexed → nothing is done ("already indexed"); same file name with different content → the old chunks are deleted and replaced; only .pdf/.txt/.md accepted. It needs human approval in the harness.

**Question q44** (unanswerable): "What does the General-Purpose AI Code of Practice require signatories to do on copyright?" Added document: the Commission's GPAI Code of Practice, Copyright chapter (`sources/added/gpai_code_copyright.pdf`), indexed as 9 page-window chunks because it is not a regulation.

- **Before:** "The corpus does not contain the text of the General-Purpose AI Code of Practice itself." It then gave only what the AI Act requires (copyright policy, training-content summary) [AI Act, Article 53(1)(c)].
- **After:** it answered from the Code: draw up and implement a copyright policy (Measure 1.1) [GPAI Code of Practice (Copyright), p. 4]; do not circumvent paywalls and exclude persistently infringing websites when crawling (Measure 1.2) [pp. 4-5]; follow robots.txt and other machine-readable rights reservations (Measure 1.3) [p. 5].

Full answers in `eval/before_after.json`. The committed index keeps the added document, so asking q44 live now gives the "after" answer; the evaluation reads the "before" answer from its cache.

## Harness and guardrails

`agent.py`: LangChain `create_agent` on Gemini (`gemini-3.5-flash-lite`, with fallbacks for quota/overload), MCP tools bridged into LangChain, `AGENTS.md` as the system prompt.

**AGENTS.md rules:** 
- 1) answer only from search results.
- 2) cite every claim in the exact CITE AS form. 
- 3) when the results don't answer, start with "The corpus does not cover this question.". 
- 4) search again with the regulation's wording, at most 4 searches. 
- 5) for classification questions quote the deciding test and say which facts would change it. 
- 6) quote fines, thresholds and deadlines exactly. 
- 7) be short. 
- 8) only add documents when asked.

**Approval:** a middleware intercepts every `add_document` call and asks the user `Allow? [y/N]`; with no one at the terminal it is denied and the model is told not to retry. Also call limits: at most 6 tool calls and 8 model calls per question.

**Extra guardrail: citation check.** After the agent answers, code checks that every citation points to a passage the search tool actually returned (same law and same article/recital/annex) and that a non-refusal answer cites something. If not, the agent gets one retry with the problem spelled out; if it fails again the answer is replaced by the refusal. Reason: an invented citation in a compliance answer is worse than no answer.

It fired on 2 of 47 questions. Example, q29: the first draft cited `[GDPR, Article 9, GDPR, Article 22(4)]`, which it had not retrieved. The check replied "These citations are not in your search results… Cite only passages you retrieved, or search for them."; the agent searched for GDPR Article 9 and Article 22, and the final answer cited only retrieved passages.

## Evaluation

**Code checks** refused or not, number of citations, all citations valid, expected passage retrieved, number of searches, guardrail fired. A refusal on an answerable question is graded wrong by code.

**LLM judge:** `gemma-4-31b-it` (backups `gemma-4-26b-a4b-it` and `gemini-3.5-flash-lite` when Google's servers were overloaded) grades each answer against the question, the reference answer and the retrieved passages with this rubric (`eval/rubric.md`):
- **correct (1/0):** the answer states the same decisive fact as the reference (verdict, number, deadline, threshold, obligation); multi questions must cover both parts; for unanswerable questions, 1 only if it says the laws don't contain it without stating the missing fact.
- **supported (1/0):** every factual claim is in the retrieved passages, directly or by plain paraphrase; statements about what the corpus covers don't count; no partial credit.

Of the 47 grades, 15 came from Gemma 31B, 18 from Gemma 26B and 14 from flash-lite. Flash-lite is the same model family as the agent, so those 14 may be lenient.

**Agreement with the judge** (20 answers in `eval/human_labels.csv`):

| Field | Agreement | Cohen's kappa |
|---|---|---|
| correct | 20/20 = 1.00 | 1.00 |
| supported | 16/20 = 0.80 | 0.39 |

The judge is reliable for "correct" but not for "supported": it passed three answers (q07, q15, q29) that contain claims not in the passages, and failed one (q11) that I judged supported. So the "unsupported" count below is probably an undercount.

**Results (47 questions):**

| Result | Count |
|---|---|
| Correct | 47/47 (answerable 38/38, unanswerable 8/8, plus q44 after adding the document) |
| Unsupported (judge) | 3 (q11, q13, q31) |
| Invalid citations in final answers | 0 |
| Correct refusals (exact refusal sentence) | 5/8; the other 3 unanswerable answers (q40, q42, q44) said "the corpus does not cover…" in their own words, and the judge still graded them correct |
| Wrong refusals | 0 |

## Failures

All three failures are **unsupported claims**: the answer is correct but contains a claim not in the retrieved passages (`eval/failures.csv`):

| Cause | Count | Question |
|---|---|---|
| Extraction error (number lost from the passage) | 1 | q13: the PDF extraction turned "10^25" into "greater than 10.", because the superscript is small text and the font filter dropped it; the agent wrote 10^25 from memory |
| Retrieval gap on a multi question | 1 | q31: GDPR Article 35 was never retrieved (one search only); the agent added the DPIA triggers from memory |
| Judge too strict (not a real failure) | 1 | q11: "health data is a special category" is not stated in the passages, but the answer is right and cited correctly |

The human/judge disagreements add three more unsupported claims the judge missed (q07, q15, q29): the agent pads correct answers with general knowledge (e.g. a list of high-risk duties it never retrieved).

**What to fix first:** the extraction of superscripts (q13). It silently corrupts numbers inside the right passage, and numbers (fines, thresholds) are exactly what this use case depends on. Second: force a separate search per law on multi questions and extend the citation guardrail to flag uncited sentences, not just bad citations.

## Decision

**Would I let users rely on it?** Yes for orientation, no as the final word. A startup compliance officer can use it to find which articles apply and what they say: every correct answer pointed to the right article, it never refused an answerable question, it never invented a citation, and it said "not covered" on all unanswerable questions. But about 1 in 8 answers adds a claim that is not in the passages (3 by the judge, 3 more caught in my grading), and one number came from a corrupted passage. For fines and classification decisions that is not safe without a check.

**Safeguard:** the answer always shows its citations and the retrieved passages; the officer must read the cited article before acting, and any "is it high-risk?" or fine question goes to a lawyer before a final decision. The citation guardrail stays on.

**Cost and latency per question:** about 5 700 tokens for the agent (mean) plus about 3 200 for the judge in evaluation; 4.1 s median and 14.2 s mean per question (the mean is pulled up by Google overload retries). On the Gemini free tier this cost nothing; the limit was the daily quota, not money.

## AI use

I used Claude code as a coding assistant during this assignment. It helped me to organize my ideas, understand concepts, understand the results and also improving the formatting of the report (adding specifications for some parts). It wrote most of the code, including debugging after each error. It also helped me with the test set. My decisions were the use case and corpus, the test questions, the choice of the search design, the answers before reading the judge, the failure analysis and the final decision. 