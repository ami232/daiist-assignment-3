# Assignment 3 Report

- **Name**: Sebastian Delgado-Aparicio
- **Student ID**: 20013
- **Group**: BBADBA 5B

> **Draft status.** Facts, tables and numbers are filled in from the project files. Places marked **✍️ YOUR WORDS** still need my own wording. Sentences in *"quotes"* under my name are my own words from my review sessions.

## Use case

| | |
|---|---|
| **Who asks** | Tenants (students, young workers, families) and small landlords renting a home in Spain. |
| **What they do with the answer** | Decide how much deposit to pay, whether a rent rise or fee is legal, how much notice to give before leaving, what to do when the landlord ignores a repair. |
| **Cost of a wrong answer** | High and hard to undo: paying money they don't owe, staying in a flat they could leave for free, losing the deposit, accepting an illegal rent rise. |
| **Cost of "I don't know"** | Low: the user asks a lawyer, the regional housing office or a consumer association. |

So the system must prefer refusing over guessing, and every claim must be checkable through a citation to the exact article.

✍️ YOUR WORDS: 3–4 sentences on why you picked this use case and why a wrong answer matters more than "I don't know" here.

## Corpus

Official consolidated texts of the BOE (Spain's official gazette), downloaded as XML from the BOE open-data API (`/datosabiertos/api/legislacion-consolidada`). Only the current version of each article is kept.

| Document | URL | Version (latest change in force) | Licence | Words (current text) |
|---|---|---|---|---|
| Ley 29/1994 de Arrendamientos Urbanos (LAU) | https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003 | 8 Oct 2026 | BOE open data: free reuse citing the source (Ley 37/2007, BOE legal notice) | ~25,900 |
| Ley 12/2023 por el derecho a la vivienda | https://www.boe.es/buscar/act.php?id=BOE-A-2023-12203 | 8 Oct 2026 | same | ~32,500 |
| Real Decreto-ley 7/2019 de medidas urgentes en materia de vivienda y alquiler | https://www.boe.es/buscar/act.php?id=BOE-A-2019-3108 | 29 Feb 2020 | same | ~10,000 |
| **Total (initial corpus)** | | | | **~68,400** |
| *Ley 49/1960 de Propiedad Horizontal (LPH), added later with add_document* | https://www.boe.es/buscar/act.php?id=BOE-A-1960-10906 | 23 Oct 2026 | same | ~12,000 |

Downloaded in November 2026. Laws contain no personal data.

**Limitation found during evaluation:** RDL 7/2019 is an *amending* law. It carries the 2019 wording of the articles it changed in other laws. For example, it carries the 2019 tourist-flat rule of the LPH, but not the express-approval requirement added by LO 1/2025 (in force 3 April 2025), so an answer built from it can be out of date.

✍️ YOUR WORDS: one or two sentences on why these three laws fit the use case.

## Ingestion

- **Extract:** parse the BOE XML; each article (`<bloque>`) keeps only its latest `<version>`; editorial notes (`nota_pie`) are dropped; TÍTULO/CAPÍTULO headings become the article's heading path.
- **Clean:** normalise whitespace and non-breaking spaces.
- **Chunk:** one chunk per article; articles over 400 words are split on paragraph boundaries into numbered parts.
- **Metadata on every chunk:** `source` (law), `location` (article and title), `heading`, `part`, `doc_id`, `url` (BOE link), `words`, `hash`, `design`. The chunk text starts with "SOURCE — LOCATION (heading)".
- **Embed and store:** `gemini-embedding-2` (768 dimensions, RETRIEVAL_DOCUMENT / RETRIEVAL_QUERY) into ChromaDB in `index/` (cosine). A chunk is embedded only if its id and hash are not already stored; query embeddings are cached in `index/query_cache.json`.
- **Number of chunks:** 272 in the chosen design (LAU 117, Ley 12/2023 118, RDL 7/2019 37), plus 54 for the LPH after the demo.

**Extraction problems fixed:**
1. *All historical versions:* each article in the XML holds every past version; keeping them all tripled the word count and mixed old rules with current ones. Only the latest version is kept.
2. *Future text mixed into current text:* LAU Article 10 contains an amendment that only applies from 15 November 2026 (RDL 28/2026), introduced by "Téngase en cuenta que, con efectos de…". It is split into its own chunk labelled `[redacción futura, en vigor desde el 15 de noviembre de 2026]`, and AGENTS.md tells the agent to give that date.

## Test set

35 questions in `eval/questions.csv`: **22 single**, **7 multi** (two passages), **6 unanswerable** (on topic, but not covered by the corpus). Mostly Spanish, a few in English.

Examples:
- *multi:* "Si el arrendador es una empresa, ¿cuánto dura como mínimo el contrato y durante cuánto tiempo no se actualiza la fianza?" → LAU Art. 9 + Art. 36: seven years in both cases.
- *unanswerable:* "¿Cuál es el valor del IRAV publicado para octubre de 2026?" → the corpus only says the rent update cannot exceed the IRAV; it gives no published values.

**A test-set error found and fixed:** the original q34 ("Can the owners' community ban tourist flats?") was labelled unanswerable, but RDL 7/2019 answers it, so the agent "failed" by answering correctly. I checked candidate replacements against the corpus with two searches each (one casual, one in legal Spanish) and replaced it with "¿Puede votar en la junta de propietarios un propietario que debe cuotas de comunidad?", which none of the three laws covers (LPH art. 15.2 does).

✍️ YOUR WORDS: how the questions were written and how you reviewed them. Be honest that they were drafted with AI help from the article texts, and say what you checked or changed.

## Retrieval

Hit = a retrieved chunk has the expected law and article. Measured on the 29 answerable questions, initial corpus only.

| Design | hit@1 | hit@3 | hit@5 | all passages @5 (multi) | words added to prompt @5 |
|---|---|---|---|---|---|
| **articles** (one chunk per article) | 0.793 | **1.000** | 1.000 | **0.931** | 1,427 |
| fixed200 (200 words, 50 overlap) | 0.759 | 0.897 | 1.000 | 0.862 | 1,074 |

**Chosen: articles.** It finds the right article in the top 3 for every question, finds both passages of multi questions more often, and its chunks match how answers are cited. The cost is about 350 more words per prompt.

✍️ YOUR WORDS: one or two sentences on why you'd accept the extra words for these gains.

## Tools and subagent

**`search(query)`**, description given to the model:
> Search Spanish residential rental law (official consolidated BOE texts, in Spanish): the LAU, Ley 12/2023 and RDL 7/2019, plus any document added later with add_document. Use it for any question about renting a home in Spain… Write the query in Spanish legal terms for best results. Call it again with different words if the results do not cover the question. Returns the 5 most relevant passages, each headed with SOURCE, LOCATION and URL. Cite answers as [SOURCE, LOCATION].

**`add_document(path)`**: takes a BOE `.xml`, `.pdf`, `.txt` or `.md`; runs it through `index.index_file` (imported, not rewritten); returns the number of chunks and how many were newly embedded.

**One search result** ("¿Cuántos meses de fianza me pueden exigir al alquilar un piso como vivienda?"):
```
[1] SOURCE: LAU (Ley 29/1994) | LOCATION: Artículo 36. Fianza | URL: https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003 | score 0.7726
LAU (Ley 29/1994) — Artículo 36. Fianza (TÍTULO IV Disposiciones comunes)
1. A la celebración del contrato será obligatoria la exigencia y prestación de fianza en metálico en cantidad equivalente a una mensualidad de renta en el arrendamiento de viviendas…
```

**Subagent** (`.claude/agents/corpus-researcher.md`, tool: `mcp__corpus__search` only). Instructions: search in Spanish legal terms, search at least twice before refusing, answer in at most ~150 words with the direct answer first, cite every claim as [SOURCE, LOCATION], flag future text with its date, never present annulled text, and reply "The corpus does not cover this question." when nothing found covers it.

**Transcript from Claude Code** (2 searches, ~9.7k tokens, 13.5 s):

> **User:** Mi casero quiere subirme el alquiler este año aunque el contrato no dice nada de actualizaciones. ¿Puede hacerlo? Responde citando los artículos.
>
> **corpus-researcher:** No. Si el contrato no incluye ninguna cláusula de actualización, el casero no puede subir la renta cada año.
> - **No hay subida sin un pacto expreso.** … "En defecto de pacto expreso, no se aplicará actualización de rentas a los contratos" [LAU (Ley 29/1994), Artículo 18.1]. Esta regla viene de la reforma del RDL 7/2019 [RDL 7/2019, Artículo primero, apartado Nueve].
> - **Si hubiera pacto, la subida tiene un tope.** … la subida anual nunca puede superar la variación del IRAV [LAU (Ley 29/1994), Artículo 18.1; Disposición adicional undécima].
> - **Hace falta avisar por escrito.** … [LAU (Ley 29/1994), Artículo 18.2].
> - **Hay una excepción: las obras de mejora.** … máximo del 20 % de la renta vigente … [RDL 7/2019, Artículo primero, apartado Diez, que da nueva redacción al art. 19 LAU].

(Full transcript: `eval/subagent_transcript.md`.) For the last point it cited the amending decree instead of the consolidated LAU art. 19: the duplicate-text risk described under Corpus.

## Adding a document

**If the document is already indexed:** each chunk has an id and a content hash. Unchanged → nothing is embedded and the tool says so. Changed → new chunks are embedded and outdated ones removed. In the demo, adding the LPH a second time embedded **0** chunks.

**Unanswerable question (q34):** "¿Puede votar en la junta de propietarios un propietario que debe cuotas de comunidad?"
**Document added:** LPH (Ley 49/1960), BOE-A-1960-10906, 54 chunks.

**Before** (2 searches):
> El corpus no cubre esta pregunta (la regulación sobre la junta de propietarios y la suspensión del derecho de voto por deudas se encuentra en la Ley sobre Propiedad Horizontal, que no está indexada en el corpus…).

**After** (1 search):
> **No** si las deudas están vencidas al iniciarse la junta [LPH (Ley 49/1960), Artículo quince].
> - **Excepción:** Sí puede votar si ha impugnado judicialmente dichas deudas o si ha procedido a su consignación judicial o notarial [LPH (Ley 49/1960), Artículo quince].
> - **Participación:** Aunque no tenga derecho a voto, puede asistir a la junta y participar en las deliberaciones [LPH (Ley 49/1960), Artículo quince].

(Full text: `eval/add_document_demo.md`.)

## Harness and guardrails

`agent.py`: LangChain `create_agent` on `gemini-3.5-flash-lite`, tools from `server.py` over MCP, `AGENTS.md` as the system prompt.

**AGENTS.md rules** (each has its reason in the file):
1. Search before answering and answer only from the search results.
2. Cite every claim as [SOURCE, LOCATION].
3. If the results don't cover the question, say so plainly.
4. Search at least twice before refusing, using Spanish legal terms.
5. Separate the law in force today from future text; never present annulled text as valid.
6. Answer in the language of the question: direct answer first, then the exceptions.
7. Not a lawyer: suggest confirming concrete disputes with a lawyer or the regional housing office.
8. Only add documents when the user explicitly asks.

**Other limits:** at most 6 tool calls and 8 model calls per question.

**Approval before add_document:** a human must type "yes" in the terminal; with no terminal it is denied. Real run: asked to add `corpus/BOE-A-1960-10906.xml`, the call was denied (`[denied] add_document(...)`) and the index was not changed.

**Extra guardrail: citation guard.** Every [SOURCE, LOCATION] in an answer must match a passage the search actually returned in that run. If an answer has an invalid citation or none, the agent gets one retry; if it fails again, the answer is replaced by a refusal.

- **When it fired:** in the same real run as the approval example. The agent's first answer was correct ("El usuario no ha aprobado añadir este documento. No se ha modificado el índice."). It had no citation, so the guard forced a rewrite, and the rewrite was worse ("El corpus no cubre esta pregunta…"). This was a **false positive**: the guard should skip replies that make no legal claim.
- **On legal answers it never had to act:** 0 retries in the 35 test questions and in 5 extra questions written to tempt invented citations (Civil Code, Constitution). A direct test with real search results shows it does fire on an invented source, a wrong article and a missing citation, and lets a correct citation through (`eval/guardrail_test.md`, script `guardrail_test.py`).

## Evaluation

**Code checks** (35 questions):

| Check | Result |
|---|---|
| Citations valid (match a retrieved passage) | 35/35 |
| Expected passage retrieved by the agent | 29/29 |
| Expected passage cited | 28/29 |
| Correct refusals (unanswerable) | 6/6 |
| Answered an unanswerable question | 0/6 |
| Wrong refusals (answerable) | 1/29 (q20) |

**LLM judge rubric** (`RUBRIC` in `evaluate.py`; the judge gets the question, the reference answer, the agent's answer and the retrieved passages, and must not use its own knowledge):
- **correct (1/0):** the main conclusion agrees with the reference and nothing contradicts it; missing a minor detail is fine, missing a condition that changes the outcome is not. For unanswerable questions: it says the corpus doesn't cover it and doesn't answer anyway.
- **supported (1/0):** every factual legal claim appears in the retrieved passages. A plain refusal counts as supported; "consult a lawyer" is not a claim.

Judge models: `gemini-3-flash-preview` (31 answers), with fallbacks `gemini-3.8-flash` (3) and `gemini-3.5-flash` (1) when free-tier limits blocked the first. None is the agent's model.

**Results:**

| | Result |
|---|---|
| Correct | **33/35** (wrong: q04, q20) |
| Unsupported (something made up) | **4/35** (q04, q07, q25, q32) |
| Correct refusals | **6/6** |
| Wrong refusals | **1/29** (q20) |

**My agreement with the judge** (20 answers I graded myself, before seeing the judge's grades):

| | Agreement | Cohen's κ | Disagreements |
|---|---|---|---|
| correct | 95% (19/20) | 0.64 | q04 |
| supported | 80% (16/20) | 0.00 | q04, q07, q25, q32 |

κ is 0 for *supported* because I marked all 20 as supported. When one grader gives the same grade every time, any agreement could be luck, so κ = 0 even at 80% agreement.

After reviewing the 4 disagreements against the passages, I agreed with the judge on all of them (`eval/human_review.csv`): it caught invented details I had missed. In q04 I had even praised the answer as "more complete", and the extra detail was the invented part. The judge was not fully consistent, though: it marked q04 incorrect but q25 correct for the same invented clause.

My words: *"I now agree with the judge, showing its true power."*

✍️ YOUR WORDS: one or two more sentences on what this means: when would you trust the judge alone, and when do you still need a human?

## Failures

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 0 | — |
| Wrong answer from the right passage | 0 | — |
| Unsupported claim | 4 | q04, q25, q07, q32 |
| Wrong refusal | 1 | q20 |
| Bad test question | 1 | original q34 (replaced) |

My reasons (from `eval/failures.csv`):
- **q20 → wrong refusal.** *"It found the right article and didn't conclude anything wrong. It just refused a question the corpus answers. The likely cause is that it didn't trust text that only applies from 15 Nov 2026, so it stopped after one search."*
- **q04 → unsupported claim.** *"The conclusion is right, but it added a condition the passage doesn't contain."* Checked against the corpus: the current LAU art. 11 only says leaving early generates no compensation; the "unless the contract includes a compensation clause" exception comes from the **old** version of art. 11, which the model remembered.
- **q25 → unsupported claim.** *"It's the same invented condition as q04. That's two failures with one cause, so one fix covers both."*
- **q07 → unsupported claim.** *"The facts are right, but the citation points to a paragraph that doesn't say that."* It cites 21.2 for deducting repair costs from rent; the current text puts that in 21.5.
- **q32 → unsupported claim, not wrong refusal.** *"Refusing was correct. What's wrong is the extra explanation, which no passage supports."*
- **Original q34 → bad test question.** *"Our label was wrong, not the agent."*

**What to fix first.** *"Search isn't the weak spot; the agent's writing is. So the first fix is grounding: a rule or check that every condition and citation must appear in a retrieved passage."* Concretely: make the citation guard check the section number too (it would have caught q07); add to AGENTS.md "never add conditions or exceptions that are not written in the passage, even if you remember them" (q04, q25, q32); and force a second search before any refusal in code, not only in the prompt (q20).

## Decision

**Would I let tenants rely on it?** *Not yet: fix first, then release.*

**For what (once fixed):** finding which article of the law covers their problem, and a first explanation before talking to a lawyer or the regional housing office. Not for final decisions such as stopping rent payments, leaving the flat, or keeping or claiming a deposit.

**Safeguards:**
1. Grounding fix: every condition and citation must appear in a retrieved passage.
2. Show the article text and the BOE link next to every answer.
3. Disclaimer: not legal advice; confirm with a lawyer or the regional housing office.
4. Keep the corpus updated when the law changes.
5. Force a second search before refusing.
6. *Re-run the 35-question test after every fix and every corpus update.*

**Why:** *"Because it finds the right article every time, but about 1 in 9 answers adds a condition the law doesn't support, and in q04/q25 that condition was about leaving the flat, which is exactly the kind of decision that costs a tenant money."*

**Cost and latency per question:**

| | |
|---|---|
| Tokens | ~6,430 (6,150 input + 280 output), 1.3 searches on average |
| Cost | $0 on the free tier; ≈ $0.0025 at standard `gemini-3.5-flash-lite` prices ($0.30 / $2.50 per 1M input / output tokens), i.e. ~$2.50 per 1,000 questions |
| Latency | median 38.6 s, mean 46.5 s in the evaluation run (free-tier rate limits caused 31 retries); about 4–6 s per question without throttling |

## AI use

✍️ YOUR WORDS. Facts to include, so the disclosure is complete and accurate:
- **Code:** written with Claude Code: `index.py`, `server.py`, `agent.py`, `evaluate.py`, `guardrail_test.py`, the subagent file and the grading page.
- **Proposed by Claude, reviewed and accepted by me:** the corpus (three BOE laws), article-based chunking (chosen by the retrieval numbers), the AGENTS.md rules, the citation guard, the judge rubric, the first draft of the 35 test questions and reference answers.
- **Decided or done by me:** the topic (Spanish rental law); the replacement unanswerable question (chosen from options Claude checked against the corpus); grading 20 answers before seeing the judge's grades; reviewing the 4 disagreements; classifying every failure, including checking three of them against the law myself; the ship decision and its safeguards.
- **Also used:** Gemini models for embeddings, the agent and the judge.
