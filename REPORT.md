# Assignment 3 Report

- **Name**: Wilrick Dong
- **Student ID**: 20426
- **Group**: BBADBA 5B

## Use case

The objective of this project is to develop a regulatory compliance assistant for entrepreneurs, product managers and companies that need to understand European regulations when developing digital products or implementing AI solutions. Users can ask practical questions about their business activities to determine their obligations under the GDPR, the AI Act and the ePrivacy Directive. A confident but incorrect answer could have significant financial and legal consequences, as Article 83 of the GDPR establishes fines of up to €20 million or 4% of annual worldwide turnover, while Article 99 of the AI Act establishes fines of up to €35 million or 7% of annual worldwide turnover for certain infringements. Beyond financial penalties, incorrect information could lead to reputational damage, operational disruptions and unnecessary compliance costs. Therefore, I believe that refusing to answer a question when there is insufficient evidence is preferable to providing a misleading answer, as consulting a legal professional is considerably less costly than making an incorrect compliance decision.

## Corpus

The binding text (articles and annexes, without recitals) of three EU laws. Recitals were left out to keep two chunking designs within one day of the free embedding quota (about 1,000 texts a day); they explain the law but do not create obligations.

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| GDPR, Regulation (EU) 2016/679 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679 | 27.4.2016 | © European Union; reuse authorised (Commission Decision 2011/833/EU) | 29,435 |
| AI Act, Regulation (EU) 2024/1689 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689 | 13.6.2024 | same | 51,697 |
| ePrivacy Directive 2002/58/EC, consolidated 19.12.2009 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219 | 19.12.2009 | same | 4,763 |
| **Total** | | | | **85,895** |

`main.py index` downloads the three acts from the EU Publications Office (`publications.europa.eu/resource/celex/<CELEX>`, XHTML) into `corpus/`. The ePrivacy Directive is the consolidated 2009 version, because the cookie-consent rule in Article 5(3) only exists since the 2009 amendment.

## Ingestion

- **Extraction**: each act's XHTML marks every article (`id="art_6"`) and annex (`id="anx_III"`). `index.py` takes each one with its heading (e.g. "Lawfulness of processing") and chapter, and keeps paragraphs and lettered points as separate blocks.
- **Cleaning**: footnote references, the consolidated text's amendment markers (`▼M2`, `►M1 … ◄`) and non-breaking spaces are removed; whitespace and punctuation spacing are normalised.
- **Problem fixed**: the consolidated ePrivacy text is full of amendment markers such as `▼M2` and `►M1`, which ended up inside sentences and would have been embedded as noise. They are stripped before chunking (`MARKERS` in `index.py`). A second problem was in embedding: `gemini-embedding-2` returns one *aggregated* vector when given a list of strings, so each chunk is now sent as its own `Content`, and the code checks that it gets one vector per chunk.
- **Chunking, two designs**:
  - *article*: one chunk per article or annex; articles over 450 words are split at paragraph boundaries into parts of about 350 words ("Article 5, part 2 of 7"). Each chunk starts with `GDPR, Article 33 — Notification of a personal data breach…`.
  - *fixed*: 400-word windows with 100 words of overlap, ignoring structure. A window is tagged with every article it holds at least 40 words of.
- **Metadata per chunk**: `source`, `title`, `url`, `location` (Article/Annex), `locations`, `heading`, `chapter`, `part`/`parts`, `words`, `doc_hash`, `added`, `design`.
- **Chunks**: 378 (article design) and 286 (fixed design), embedded with `gemini-embedding-2` at 768 dimensions and stored in ChromaDB (`index/chroma`, 16 MB). Vectors are saved after every API call and only missing chunks are embedded, so a re-run embeds nothing.

## Test set

My initial test set focused exclusively on the GDPR, but I subsequently redesigned it to cover all three regulations and better reflect the intended use case of the agent. I selected articles based on their relevance to practical business decisions, including data collection, consent, automated decision-making, AI risk classification and electronic communications. I also included questions requiring information from multiple articles and unanswerable questions to evaluate whether the agent could recognize the limitations of its knowledge rather than generate unsupported answers. Question 31 was added to extend the original evaluation and provide an additional test of the agent's behaviour.

31 questions in `eval/questions.csv`: **18 single, 6 multi, 7 unanswerable**. q31 (cookie banners in France) was added for the add-document demo: it is close to the corpus's topic but not settled by it. Expected passages: 13 in the GDPR, 12 in the AI Act, 6 in the ePrivacy Directive. The column `original_location` keeps the precise pinpoints (e.g. `Article 5(1)(f)`); hit rates are measured at article level.

Examples:

- **q08 (single)**: "Our HR team wants an AI tool that infers employees' emotions from facial expressions to measure engagement. Is that allowed?" → AI Act, Article 5(1)(f): no, except for medical or safety reasons.
- **q22 (multi)**: "We're adding optional advertising cookies that track identifiable visitors. Can we install them before opt-in, and must withdrawing consent be as easy as accepting?" → ePrivacy Directive Article 5(3) and GDPR Article 7(3).

## Retrieval

Hit@k: at least one expected passage in the top k (`all@5`: every expected passage of a multi question in the top 5). Base corpus only, 24 answerable questions (`eval/retrieval.csv`, per question in `eval/retrieval_details.csv`).

| Chunks | Search | hit@1 | hit@3 | hit@5 | all@5 | MRR@5 | words added at k=5 |
|---|---|---|---|---|---|---|---|
| **article** | **vector** | **0.96** | **1.00** | **1.00** | **1.00** | **0.97** | **1,374** |
| article | keyword (BM25) | 0.58 | 0.63 | 0.67 | 0.58 | 0.61 | 1,341 |
| article | hybrid (RRF) | 0.75 | 0.88 | 0.88 | 0.75 | 0.81 | 1,355 |
| fixed | vector | 0.79 | 0.96 | 0.96 | 0.88 | 0.86 | 2,000 |
| fixed | keyword | 0.46 | 0.67 | 0.67 | 0.58 | 0.56 | 1,997 |
| fixed | hybrid | 0.67 | 0.83 | 0.88 | 0.75 | 0.75 | 2,000 |

**Chosen design: article chunks, vector search, k = 5** (`index/config.json`), by the rule set before seeing the numbers: highest hit@3, ties broken by hit@5, then by fewer words added to the prompt. It also adds about 30% fewer words than the fixed design. Keyword search was weak because the questions use everyday wording ("make unsubscribing harder") while the law uses legal terms ("withdraw consent"); fusing it with vector search pulled the good vector ranking down.

## Tools and subagent

`server.py` (MCP, stdio, registered as `corpus` in `.vscode/mcp.json` and `.mcp.json`):

- **`search(query)`**: "Search the binding text of three EU laws: the GDPR (Regulation 2016/679), the AI Act (Regulation 2024/1689) and the ePrivacy Directive (2002/58/EC as amended in 2009, cookies and electronic marketing). Use it for any question about obligations, definitions, rights, deadlines, fines or exemptions under these laws, and search again with other words if the first results do not answer the question. Recitals and national laws are not included. Returns the 5 most relevant passages, each with a citation tag such as [GDPR, Article 33] to copy into the answer, the law's full title and URL, and a relevance score."
- **`add_document(path)`**: "Add one document to the searchable index: a .pdf, .html/.xhtml (EU acts from EUR-Lex are split by article), .txt or .md file given by its path on this machine… If the same file content is already indexed, nothing is embedded. If a document with the same name but different content is indexed, its old chunks are replaced. Returns the source name, how many chunks were added and an example citation tag."

One search result (top hit for q08):

```
Result 1  cite as [AI Act, Article 5] (part 2 of 7)  relevance 0.7331
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 5 — Prohibited AI practices (part 2 of 7)
(d) the placing on the market … (e) … facial recognition databases …
(f) the placing on the market, the putting into service for this specific purpose, or the use of AI systems to infer emotions of a natural person in the areas of workplace and education institutions, except where the use of the AI system is intended to be put in place or into the market for medical or safety reasons;
…
```

Subagent `.claude/agents/corpus-researcher.md` (tools: `mcp__corpus__search` only): it searches with the question, re-searches with the law's own terms (at most four searches), answers in at most six sentences with a citation tag after every claim, replies "The corpus does not cover this question." when the passages do not answer, and never fills gaps from memory, national law or case law.

**Transcript from the editor** (VS Code, Copilot Chat in Agent mode, delegating to the `corpus-researcher` subagent):

> **Me:** Use the corpus-researcher subagent: do we need a DPIA before launching an AI tool that monitors employees?
>
> **corpus-researcher:** Yes — usually before launch, if the processing is likely high-risk.
>
> As controller, you must carry out a DPIA prior to processing where the processing — in particular using new technologies, and given its nature, scope, context and purposes — is likely to result in a high risk to individuals’ rights and freedoms [GDPR, Article 35]. A DPIA is in particular required for a systematic and extensive evaluation of personal aspects based on automated processing (including profiling) on which decisions are based that produce legal effects or similarly significantly affect the person [GDPR, Article 35]. An AI tool that monitors employees and feeds into decisions that significantly affect them (for example performance evaluation, task allocation, or terms of work) therefore typically triggers that obligation before go-live; if it does not meet the high-risk threshold (and is not on your supervisory authority’s DPIA list), a DPIA is not mandated solely because the tool is AI [GDPR, Article 35].
>
> Separately, AI systems intended to monitor and evaluate the performance and behaviour of persons in work-related relationships are listed as high-risk (unless an Article 6(3) derogation applies; systems that perform profiling remain high-risk) [AI Act, Annex III]; [AI Act, Article 6]. Where a GDPR DPIA applies, deployers of high-risk AI systems must use the provider’s information to comply with that DPIA duty [AI Act, Article 26]. That GDPR DPIA is distinct from the AI Act fundamental-rights impact assessment, which applies only to specified deployers (mainly public bodies/public services and certain Annex III point 5 uses), not automatically to every private employer using workplace-monitoring AI [AI Act, Article 27].
>
> (Answer from corpus-researcher.)

## Adding a document

**Already indexed** (policy chosen: skip if identical, replace if changed): `add_document` hashes the file. If the same content is already in the index, it embeds nothing and says so. If a document with the same name but different content exists, its old chunks are deleted and the new version is embedded. A file can never replace one of the three base laws: it is renamed "… (added)" instead.

**Demo** (full transcript in `eval/before_after.md`):

- **Unanswerable question q31**: "We're launching a cookie banner in France. Does the French regulator require refusing cookies to be as easy as accepting them?" The corpus requires consent for cookies (ePrivacy, Article 5(3)) and makes *withdrawing* consent as easy as giving it (GDPR, Article 7(3)), but says nothing about the French regulator or the *refuse* option.
- **Before**: one search ("cookie banner refuse easy accept France ePrivacy GDPR"), then "The corpus does not cover this question."
- **Document added**: the CNIL's news item of 14 December 2021, "Refusing cookies should be as easy as accepting them: the CNIL continues its action and issues new orders", saved as `extra_docs/CNIL_cookie_refusal_2021.md`. The harness asked `Approve? [y/N]`, the demo run answered `y`, and 2 chunks were embedded. Asked to add it a second time, the tool embedded nothing and said it was already in the index.
- **After**: "Yes. The French data protection regulator (the CNIL) actively enforces the requirement that refusing cookies must be as easy as accepting them [CNIL cookie refusal 2021, § Refusing cookies should be as easy as accepting them…]", followed by three points (refusing must be as easy and visible as accepting, the refusal must actually stop the cookies, and fines can reach 2% of annual worldwide turnover), all cited to the new document. Two details in it are not in the CNIL text (see Failures).

## Harness and guardrails

`agent.py` uses LangChain `create_agent` on `gemini-3.5-flash-lite`, with the MCP server's tools and `AGENTS.md` as the system prompt.

**AGENTS.md rules** (each with its reason in the file): use only the corpus; apply the law to the user's situation; cite every material claim as `[GDPR, Article 33]` and never invent a citation; combine passages for multi-part questions; keep conditions and exceptions; refuse with exactly "The corpus does not cover this question."; keep answers clear and concise.

**Approval**: `HumanInTheLoopMiddleware` interrupts every `add_document` call. The terminal shows the tool and its arguments and asks `Approve? [y/N]`; anything but `y` rejects, and the model is told the user did not approve. Evaluation runs pass a function that always rejects.

**Limits**: at most 6 tool calls and 10 model calls per question (`ToolCallLimitMiddleware`, `ModelCallLimitMiddleware`).

**Extra guardrail, citation check**: after the agent answers, the harness parses every `[Source, Location]` tag and compares it with the tags returned by `search` in that run (`Article 6(1)(b)` counts as `Article 6`). If a tag was not retrieved, or a non-refusal answer has no tag, the agent gets one retry with the problem spelled out; if it fails again, the harness replaces the answer with the refusal.

**One case where it fired** (`eval/guardrail_case.json`): asked "What does GDPR Recital 47 say about direct marketing as a legitimate interest?", which is not covered because recitals are not indexed, the first draft had no citation tag. The guardrail sent it back, and the retry answered "The corpus does not cover this question." In the 31-question evaluation it never fired: every answer passed on the first try.

**A flaw found in the demo**: when the agent was asked to add a document, its confirmation ("The document … has been successfully added") has nothing to cite, so the check replaced it with the refusal, even though the document had been added. The check now skips runs that call `add_document`.

## Evaluation

**Code checks** (`evaluate.py`, all 31 questions):

| Check | Result |
|---|---|
| Citation tags all retrieved in that run (non-refusals) | 24 / 24 |
| Answer cites an expected article (answerable) | 24 / 24 |
| Expected passage among the retrieved results (answerable) | 24 / 24 |
| Refused exactly when unanswerable | 31 / 31 |
| Refusal text exactly "The corpus does not cover this question." | 7 / 7 |
| Citation guardrail fired | 0 |

**Judge**: `gemini-3.1-flash-lite`, a different model from the agent, using the rubric in `eval/rubric.md` (correctness and support graded separately, 0 or 1, no partial credit for multi questions, exact-refusal rule for unanswerable questions). It gets the question, its type, the expected answer and locations, every retrieved passage and the answer.

| Questions | n | Mean correctness | Mean support | Strict pass |
|---|---|---|---|---|
| All | 31 | 1.00 | 1.00 | 1.00 |
| Single | 18 | 1.00 | 1.00 | 1.00 |
| Multi | 6 | 1.00 | 1.00 | 1.00 |
| Answerable (single + multi) | 24 | 1.00 | 1.00 | 1.00 |
| Unanswerable | 7 | 1.00 | 1.00 | 1.00 |

Correct: 24 / 24 answerable. Unsupported: 0 (judge), 1 (my grades: q21). Correct refusals: 7 / 7. Wrong refusals: 0. Missed refusals: 0.

**Agreement with my grades** (29 questions graded in `eval/human_labels.csv` before reading the judge's verdicts; q25 and q31 not graded by me):

| Grade | Agreement | Cohen's κ | My zeros | Judge zeros |
|---|---|---|---|---|
| Correct | 29 / 29 (100%) | undefined (both gave 1 everywhere) | 0 | 0 |
| Supported | 28 / 29 (96.6%) | 0.00 | 1 (q21) | 0 |

κ is 0 for support even with 96.6% agreement because the judge never gave a 0, so it agrees no better than chance on the one case that matters. Our only disagreement is q21.

The final evaluation consisted of 31 questions, combining automated code checks, an LLM judge following a predefined evaluation rubric, and my own manual assessment of 29 responses.

Although the LLM judge considered all evaluated responses correct and supported, I disagreed with its assessment of Question 21, which concerned automated loan rejection.

I considered the answer correct in its general interpretation of the GDPR but unsupported in part because it generalized the safeguards described in Article 22(3) to all exceptions to the restrictions on automated decision-making. More specifically, Article 22(3) establishes these particular safeguards for the exceptions relating to contractual necessity and explicit consent under Article 22(2)(a) and Article 22(2)(c). The exception based on authorization by law is addressed differently.

I therefore assigned the response a correctness score of 1 but a support score of 0. I decided to maintain my original grade despite the disagreement with the LLM judge because, in a legal compliance context, the distinction between what legislation explicitly states and what an agent infers is particularly important.

This disagreement also demonstrates why an automated judge should not be considered a perfect substitute for human evaluation.

## Failures

Failed questions by cause (31 test questions; the demo is listed separately because it is not part of the test set):

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 0 | every answerable question had an expected passage in the top 5 |
| Wrong answer from the right passage | 0 | |
| Unsupported claim | 1 | q21 (Article 22(3) safeguards generalised to all exceptions) |
| Wrong refusal | 0 | q26, q27 and q30 were refused without a search, but correctly |
| Bad test question | 0 | |
| *Outside the test set* | 2 | demo "after" answer: two details not in the CNIL text (unsupported claim); citation check blocked a confirmation (guardrail error, fixed) |


Despite the strong evaluation results, I identified several weaknesses that suggest the system is not yet sufficiently reliable for unrestricted real-world use.

#### 6.1. Question 21 – Unsupported generalization

The first issue was the agent's interpretation of Article 22 of the GDPR. Although it retrieved relevant information and provided a broadly correct answer, it extended the scope of a legal provision beyond what the cited text explicitly supported.

I would classify this as a generation and grounding failure rather than a retrieval failure. The relevant information was available, but the agent did not interpret its precise legal scope correctly.

#### 6.2. Refusals without retrieval

Three questions were refused without the agent performing a search. Although these refusals were accepted by the evaluation, the agent reached its conclusion without consulting the corpus.

I consider this a tool-use and agent reasoning weakness rather than an observed incorrect answer. The agent may have correctly identified that these questions were outside its scope, but the same behaviour could cause it to incorrectly refuse an answerable question in the future.

I would improve the system prompt by requiring at least one retrieval attempt before refusing substantive regulatory questions.

#### 6.3. Unsupported information after document indexing

During the demonstration, the agent's answer after adding the CNIL document introduced two details that were not present in the document.

This represents a generation and grounding failure. The agent appears to have supplemented the retrieved information with additional knowledge or assumptions rather than limiting itself to what could be verified from the corpus.

In a conventional chatbot, additional context may be useful. However, in a regulatory compliance assistant, unsupported information creates unnecessary legal risk, even when it happens to be factually correct.

#### 6.4. Citation validation failure

The citation verification mechanism incorrectly blocked a confirmation message. This occurred because the citation requirement was applied to a response that did not contain a substantive regulatory claim.

I would classify this as a validation or guardrail failure. The mechanism itself was useful, but its implementation was too restrictive.

A better approach would distinguish between substantive regulatory answers, which require citations, and operational messages, such as document indexing confirmations, which do not.

#### 6.5. Reliability of the evaluation

Although the LLM judge reported perfect results, I do not believe that this proves the system is entirely reliable. The test set contains only 31 questions, and the questions were designed around a known and relatively limited corpus.

Furthermore, the disagreement on Question 21 demonstrates that the evaluation process itself has limitations. An answer can appear correct to an automated judge while containing subtle but important legal inaccuracies.

To improve the evaluation, I would introduce more complex questions involving ambiguous scenarios, exceptions to general rules, interactions between multiple regulations, misleading assumptions and questions that are only partially answerable from the corpus.

My first priority would be to improve answer grounding and citation verification. A system that retrieves the correct information but generates unsupported legal conclusions can still create considerable risk for its users.

## Decision

Based on the results, I would allow users to use the agent as a preliminary regulatory research assistant, but I would not recommend relying on it as the sole source of legal advice.

I would trust the system for relatively straightforward questions, such as identifying relevant articles, retrieving explicit regulatory requirements, explaining general obligations and locating information within the three regulations.

However, I would not rely on it for complex legal interpretations, decisions involving exceptions to legislation, determining whether a specific company is fully compliant, or questions requiring information outside the available corpus.

Before deploying the system, I would introduce the following safeguards:

- Require citations for all substantive legal claims.
- Require retrieval before refusing substantive regulatory questions.
- Clearly communicate when information is incomplete or uncertain.
- Distinguish between legal research assistance and professional legal advice.
- Require human verification for high-risk compliance decisions.
- Regularly update the corpus and expand the evaluation dataset.

From an operational perspective, the system is efficient, with an average consumption of approximately 3,400 tokens and a response time of around three seconds per question. This makes it suitable for preliminary research and repeated use.

Ultimately, I believe the main challenge is not reducing the cost or response time but ensuring that every legal claim is sufficiently supported. The system's value comes from making regulatory information more accessible while reducing research time, without creating a false sense of legal certainty.

Cost and latency per question (31 questions, `gemini-3.5-flash-lite` free tier): on average **3,405 input + 187 output tokens**, **3.1 s** (median 2.4 s), 0.9 searches. Indexing cost 664 embeddings, one time; queries cost one embedding each, cached in `index/query_cache.json`.

## AI use

I used Claude (Anthropic) throughout:
- **Code**: it wrote `index.py`, `retrieval.py`, `server.py`, `agent.py`, `evaluate.py` and the subagent file, and ran the indexing and evaluation.
- **Corpus**: it found and parsed the corpus.
- **Tools**: it built the corpus reader and grading pages I used.
- **Report**: it filled in the factual sections, numbers and tables of this report.
- **CSV**: it converted my questions to the CSV columns the assignment requires.
- **Assembly**: it placed my sections and my editor transcript into this file, and compiled the failure-count table from my analysis.

I used generative AI to review the accuracy, completeness, structure and clarity of my report. AI also helped me articulate the limitations identified during the evaluation and organize my failure analysis. The technical results are based on the project experiments and evaluation, while the final assessment and deployment decision reflect my own judgment.
