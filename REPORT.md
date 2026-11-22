# Assignment 3 Report

- **Name**: Juan Jacobo Rico Fontán
- **Student ID**: 18693
- **Group**: B

## Use case

The users are property and asset managers (and tenants' advisers) in Spain who need a quick, checkable answer about residential leases: minimum term, rent updates, deposits, large-holder rules in stressed housing zones, and how a homeowners' association works. They act on the answer, for example by drafting a lease clause or answering a tenant. A confident wrong answer (a wrong notice period or a wrong deposit rule) can mean a void clause or a dispute, so it costs clearly more than "the corpus does not cover this question", which only sends the user to the BOE text. That asymmetry is why the assistant must cite every claim and refuse when the passages do not answer.

## Corpus

| Document | URL | Date retrieved | Licence | Words |
|---|---|---|---|---|
| lau.pdf (Ley de Arrendamientos Urbanos, 1994) | https://boe.es/buscar/pdf/1994/BOE-A-1994-26003-consolidado.pdf | 2026-11-21 | BOE, reuse with attribution | 23,672 |
| ley_vivienda.pdf (Ley por el derecho a la vivienda, 2023) | https://www.boe.es/buscar/pdf/2023/BOE-A-2023-12203-consolidado.pdf | 2026-11-21 | BOE, reuse with attribution | 32,288 |
| lph.pdf (Ley de Propiedad Horizontal, 1960) | https://www.boe.es/buscar/pdf/1960/BOE-A-1960-10906-consolidado.pdf | 2026-11-21 | BOE, reuse with attribution | 11,582 |

Total: 67,542 words, three consolidated legal texts.

## Ingestion

Text is extracted from each PDF page by page with pypdf. Repeated page headers and footers (the BOE banner and page numbers) are removed because they would otherwise appear in every chunk and pollute the embeddings. Lines that look like headings (Artículo, Capítulo, Disposición, Título) are tracked as the current section.

Two chunking designs were built and compared:
- **fixed**: 200-word windows with 40 words of overlap.
- **structure**: paragraphs grouped within a section, at most 250 words, merging pieces under 40 words.

Every chunk carries metadata: source file, location (page or page range, e.g. `p.12` or `p.13-14`), section, and the file hash. Embeddings use Gemini (`gemini-embedding-2`, 768 dimensions) stored in ChromaDB with cosine distance, one collection per design. Number of chunks: 423 (fixed) and 497 (structure).

**Extraction problem fixed.** My first download of `ley_vivienda.pdf` used the host `boe.gob.es`, which returned an HTML page instead of a PDF. The file looked fine by name, but indexing failed with `invalid pdf header: b'<!DOC'`. I found it with the `file` command (it reported HTML), re-downloaded from `www.boe.es`, and confirmed with `file corpus/*` that all three files are real PDFs. The same thing happened later with a wrong BOE identifier for the extra document, which is why I now check every download with `file` before indexing.

## Test set

32 questions in `eval/questions.csv`, written after reading the chunks and before tuning anything. The questions and reference answers were drafted with AI help from the texts (see AI use) and are not an independent human-written set.

| Kind | Count |
|---|---|
| single (one passage) | 20 (10 LAU, 5 Ley de Vivienda, 5 LPH) |
| multi (two passages, often two laws) | 6 |
| unanswerable (near the corpus topic) | 6 |

Examples:
- single (q05): "¿Qué fianza hay que prestar en un arrendamiento de vivienda y qué ocurre si no se devuelve a tiempo?" Expected `lau.pdf`, p.25: one month's rent in cash; the balance earns legal interest if not returned within a month of handing back the keys.
- unanswerable (q29): "¿Es obligatorio que el inquilino contrate un seguro de hogar?" Close to the corpus (the LAU says a tenant cannot be required to take out rent-default insurance) but not answered by it, so the right reply is a refusal.

## Retrieval

Hit rate counts a question as a hit when a retrieved chunk has the expected source and an overlapping location. Answerable questions only (n = 26).

| design | method | hit@1 | hit@3 | hit@5 | single@5 | multi@5 | words in prompt @5 |
|---|---|---|---|---|---|---|---|
| fixed | dense | 0.692 | 0.885 | 0.962 | 1.00 | 0.833 | 1000 |
| fixed | bm25 | 0.615 | 0.731 | 0.846 | 0.90 | 0.667 | 1000 |
| fixed | hybrid | 0.692 | 0.846 | 0.846 | 0.95 | 0.500 | 1000 |
| structure | dense | 0.654 | 0.885 | **1.000** | 1.00 | 1.000 | 794 |
| structure | bm25 | 0.615 | 0.731 | 0.769 | 0.90 | 0.333 | 820 |
| structure | hybrid | 0.615 | 0.808 | 0.846 | 1.00 | 0.333 | 834 |

**Chosen: structure + dense, k = 5.** It is the only configuration with hit@5 = 1.000 (including all multi-passage questions), ties for the best hit@3, and puts the fewest words in the prompt (794). It loses only on hit@1 (0.654 vs 0.692), which matters little because the agent reads all five passages. BM25 and hybrid are worse on multi-passage questions: legal Spanish repeats the same terms across laws, so exact word overlap does not separate them.

## Tools and subagent

`server.py` is an MCP server (stdio) with two tools. The descriptions the model reads:

- **search(query)**: "Search the document collection: Spanish housing and rental law: the Ley de Arrendamientos Urbanos (LAU), the 2023 Ley por el derecho a la vivienda and the Ley de Propiedad Horizontal. Use it for every factual question about these documents, and call it again with different wording, or once per sub-question, when a question needs more than one passage. Takes a natural-language `query`. Returns the 5 best-matching passages, each under a citation header `[source | location]` followed by the passage text. If no passage answers the question, the collection does not cover it."
- **add_document(path)**: "Add one new document to the collection so that `search` can find it. Takes the file `path` (.pdf, .html, .txt or .md). The file is extracted, chunked, embedded and stored. If identical content is already indexed nothing is changed; if a file with the same name but different content is indexed, its old passages are replaced. Returns a short report of what was added, replaced or skipped. Only use this when the user asks to add a document."

**One search result** (agent query `fianza arrendamiento vivienda obligatoria devolucion a tiempo intereses`): the tool returns `Query: ...`, `Top 5 passages:` and then numbered passages, each with its header, for example `[1] [lau.pdf | p.30-31] (section: artículo 36.1 ...)` followed by the text on the regional authority returning the deposit and the legal interest after one month.

**Subagent** (`.claude/agents/corpus-researcher.md`, tool `mcp__corpus__search` only):

```
You answer questions using only the `search` tool of the `corpus` MCP server.
1. Call `search` before answering. For a question with several parts, call it once per part, with different wording each time.
2. Answer only from the passages returned. Do not add facts from general knowledge.
3. After every claim, cite the passage header exactly as returned: `[source | location]`. Never cite a passage you did not retrieve.
4. Keep conditions, exceptions, numbers and dates exactly as the passage states them.
5. If the passages do not answer the question, reply exactly: "The corpus does not cover this question." A passage on the same topic that does not answer the question is not an answer.
6. Reply with the short answer and its citations, nothing else.
```

**Transcript from my editor:** TODO_SUBAGENT_TRANSCRIPT

## Adding a document

**Already-indexed document.** Adding the same file twice changes nothing: the second call returned `[structure] already indexed as 'doc.pdf' (identical content): nothing changed.` (identical SHA-1 is skipped; same name with different content replaces the old chunks).

**Test.** Unanswerable question q30: "¿Qué capital mínimo y qué porcentaje de dividendos debe repartir una SOCIMI?". I added the Ley 11/2009 on SOCIMI (BOE-A-2009-17000, 30 pages) as `extra/doc.pdf`. The first call reported `added 'doc.pdf': 113 chunks, 16823 words, 112 new embeddings`.

- **Before:** "The corpus does not cover this question."
- **After:** the agent now retrieves passages of `doc.pdf` and answers the dividend half (only the 100% rule for dividends from participated companies, `[doc.pdf | p.7]`), but says the corpus has no minimum capital. That is a partial answer: the law also states 50% of gains on property sales and 80% of the remaining profit, and article 5 sets a minimum capital of 5 million euros.

Asked separately, the dividend question returned the full 100% / 50% / 80% rule with `[doc.pdf | p.7]`. The question "¿Qué capital social mínimo deben tener las SOCIMI?" was still refused after three searches, so this is a retrieval miss on the added document: article 5 exists in the file but was not returned. I did not diagnose the exact cause; a likely one is that the short article was merged into a larger structure chunk, which dilutes its embedding. So adding a document works mechanically and fixes part of the gap, but retrieval quality on new documents is not guaranteed.

## Harness and guardrails

`AGENTS.md` (system prompt) has eight rules, each with its reason: (1) always search before a factual answer; (2) answer only from retrieved passages; (3) cite every claim as `[source | location]` and never cite what was not retrieved; (4) one search per sub-question for multi-part questions; (5) if the passages do not answer, reply exactly "The corpus does not cover this question."; (6) quote closely, keep conditions and numbers; (7) `add_document` only when asked and with approval; (8) short answers, answer first.

Guardrails in `agent.py`:
1. **Approval.** `add_document` never runs without the user's explicit yes. A callback asks on the terminal; with no terminal, or in evaluation, the answer is no and the tool returns "DENIED" to the model.
2. **Limits.** At most 6 tool calls and 10 model calls per question (`ToolCallLimitMiddleware`, `ModelCallLimitMiddleware`).
3. **Citation guardrail (my own).** Every `[source | location]` in the answer must be a passage that `search` really returned in this run, and a non-refusal answer must cite at least one. If not, the agent is sent back once with the list of problems.

**A case where it fired:** q01 (minimum lease term). The first answer cited a combined `[ley_vivienda.pdf | p.42, lau.pdf | p.13]` and one passage not retrieved; the guardrail sent it back. The retry fixed part of it, but q01 still ended with an invalid citation. The guardrail fired on 4 of 32 questions (q01, q02, q21, q24); q24 was fixed by the retry, q01 and q21 were not, so the final valid-citation rate is 93.8%.

## Evaluation

**Code checks** (no model): citations are valid (all cited passages were retrieved), the answer cites the expected source, and refusals are exact. Result: valid citations 93.8%; cites the expected source on 92.3% of answerable questions.

**LLM judge** (`gemini-3.5-flash-lite`, temperature 0, structured output). Rubric in short: `correct` = same substance as the reference answer (or a proper refusal for unanswerable questions); `supported` = every claim appears in the retrieved passages, judged only against them; be strict, give 0 when unsure, name the failing claim.

**Agreement with my labels** (32 answers labelled before running the judge; see AI use for how the labels were produced):

| | agreement | Cohen's kappa |
|---|---|---|
| correct | 0.938 | 0.467 |
| supported | 0.938 | 0.000 |

The kappa for `supported` is 0.0 although agreement is 93.8%: almost every answer is "supported" in both label sets, so there is no variation for kappa to measure. Agreement is the number to read here. Disagreements (q01, q04, q20, q21): q01 and q21 (I marked `supported = 0` because of citations that were not retrieved, the judge marked 1) and q04 (I marked `correct = 0` because the answer omits the rule that rent updates apply only annually, the judge marked 1). The judge is more lenient than my labels on exactly the cases where a detail is missing or a citation is off. The judge is not fully repeatable: in an earlier run it marked q20 correct and agreement on `correct` was 0.969 (kappa 0.652); in the final run it marked q20 incorrect (0.938, kappa 0.467). The numbers above are from the final run and match `eval/summary.json`.

The first judge run also had 7 `-1` errors (HTTP 503 from Gemini); I added retries for 503/500 and re-ran until none were left.

**Results (32 questions):**

| | n | result |
|---|---|---|
| answerable, correct | 26 | 25 (judge) |
| answerable, unsupported answers | 26 | 0 (judge) |
| answerable, incorrect answers | 26 | 1 (q20, judge) |
| wrong refusals | 26 | 0 |
| unanswerable, correct refusals | 6 | 5 |
| unanswerable, answered instead of refusing | 6 | 1 (q29) |

On my own labels the answerable score is lower: q04 is incomplete and q01 and q21 have citation problems, so 25/26 correct and 24/26 fully supported.

## Failures

The judge flagged two failures (q29 and q20); my own labels and the code checks add more.

| Cause | Count | Questions |
|---|---|---|
| answered instead of refusing (near-miss passage) | 1 | q29 |
| answer mixes two figures without saying which applies | 1 | q20 (2.5% at constitution and 10% of art. 9.1.f) |
| wrong answer from right passage (incomplete) | 1 | q04 |
| invalid / unretrieved citation after retry | 2 | q01, q21 |
| retrieval miss on an added document | 1 | capital question after adding the SOCIMI law |
| retrieval miss on the original corpus | 0 | expected source retrieved for all 26 answerable questions |

q29 is the most important: the agent retrieved the LAU line "en ningún caso podrá exigirse al arrendatario la contratación de seguros de impago de renta" and presented it as an answer about home insurance. It is the "stretch a loosely related passage" case rule 5 forbids. **First fix:** tighten the near-miss rule with this example in `AGENTS.md`, and make the guardrail reject answers whose cited passage does not share the key terms of the question. **Second fix:** re-rank or enlarge `k` for short articles in newly added documents.

## Decision

I would let users rely on it as a first-pass finder of the relevant article for the three covered laws, always with the cited page, because retrieval found the expected passage for every answerable question and refusals were right in 5 of 6 cases. I would not let anyone act on it without opening the cited page: the agent can omit a condition (q04), mix citations (q01, q21), or answer a near-miss question (q29). Safeguards: show the cited passages next to the answer, keep the refusal rule, and add a human check before using an answer in a contract. It is also limited to the consolidated text on the retrieval date (2026-11-21), so it can be out of date after a reform, and the test set is small (32 questions).

Cost and latency per question (evaluation run): mean 5,429 input tokens and 232 output tokens, 1.75 tool calls and 9.7 seconds on `gemini-3.5-flash-lite`.

## AI use

Claude helped in the creation of the code based on the slides, it also helped paraphrasing and structuring the code and text. Claude also helped in the porcess of structuring, linking and uploading of the assignment in both VS Code and Github. Claude never had the chance to commit any code or relevant decisions without my consent and guidance.
