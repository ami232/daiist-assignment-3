# Assignment 3 Report

- **Name**: Sebastian Delgado-Aparicio
- **Student ID**: 20013
- **Group**: BBADBA 5B

## Use case

| | |
|---|---|
| **Who asks** | Tenants (students, young workers, families) and small landlords renting a home in Spain. |
| **What they do with the answer** | Decide how much deposit to pay, whether a rent rise or fee is legal, how much notice to give before leaving, what to do when the landlord ignores a repair. |
| **Cost of a wrong answer** | High and hard to undo: paying money they don't owe, staying in a flat they could leave for free, losing the deposit, accepting an illegal rent rise. |
| **Cost of "I don't know"** | Low: the user asks a lawyer, the regional housing office or a consumer association. |

So the system must prefer refusing over guessing, and every claim must be checkable through a citation to the exact article.

I picked Spanish rental law partly because of my own experience renting a flat, where many situations came up in which an assistant like this would have helped me understand my rights and handle things better. It's also a good test case because the law has been reformed several times in a few years (RDL 7/2019, Ley 12/2023, and a change to LAU art. 10 announced for November 2026 that was repealed before it took effect), and many tenants rely on websites that fall behind the official text: while grading, I found two legal websites still describing old versions of LAU articles 11 and 21. The assistant is for a tenant with a concrete problem, such as an ignored repair, a deposit or leaving early, who wants to know which article applies before going to a lawyer or the housing office. A wrong answer is much worse than "I don't know": in q04 the agent said leaving early gives the landlord no right to compensation "salvo que el propio contrato incluya alguna previsión al respecto" (unless the contract itself provides for it), but the current art. 11.3 says leaving gives the landlord no right to compensation, so a tenant could stay in a flat they could leave for free, or pay money they don't owe, while "I don't know" only sends them to ask someone else.

## Corpus

Official consolidated texts of the BOE (Spain's official gazette), downloaded as XML from the BOE open-data API (`/datosabiertos/api/legislacion-consolidada`). Only the current version of each article is kept.

| Document | URL | Version (latest change in force) | Licence | Words (current text) |
|---|---|---|---|---|
| Ley 29/1994 de Arrendamientos Urbanos (LAU) | https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003 | 13 Nov 2026 | BOE open data: free reuse citing the source (Ley 37/2007, BOE legal notice) | ~23,600 |
| Ley 12/2023 por el derecho a la vivienda | https://www.boe.es/buscar/act.php?id=BOE-A-2023-12203 | 8 Oct 2026 | same | ~31,600 |
| Real Decreto-ley 7/2019 de medidas urgentes en materia de vivienda y alquiler | https://www.boe.es/buscar/act.php?id=BOE-A-2019-3108 | 29 Feb 2020 | same | ~9,800 |
| **Total (initial corpus)** | | | | **~65,000** |
| *Ley 49/1960 de Propiedad Horizontal (LPH), added later with add_document* | https://www.boe.es/buscar/act.php?id=BOE-A-1960-10906 | 23 Oct 2026 | same | ~11,900 |

Downloaded on 23 November 2026. The four XML files are committed in `corpus/` as a dated snapshot, so `main.py index` rebuilds exactly the evaluated index (without them it would download whatever the BOE publishes on the day). Laws contain no personal data.

**The law changed during the project.** The first download (12 November) contained a change to LAU art. 10 due on 15 November 2026 (RDL 28/2026). On 12 November the Congreso de los Diputados repealed RDL 28/2026 before it took effect, and the BOE removed that text on 13 November. On 23 November the corpus was downloaded again, the index rebuilt (5 chunks of the repealed text removed, nothing else changed in the article chunks), the test question that depended on the repealed text (q20) replaced, and retrieval, the agent and the judge re-run for it. All figures in this report are for the 23 November corpus. The original q20 and its results are kept in `eval/old_q20_repealed.jsonl`.

**Limitation found during evaluation:** RDL 7/2019 is an *amending* law. It carries the 2019 wording of the articles it changed in other laws. For example, it carries the 2019 tourist-flat rule of the LPH, but not the express-approval requirement added by LO 1/2025 (in force 3 April 2025), so an answer built from it can be out of date.

The LAU (Ley 29/1994) is the base law for renting a home and covers deposits, duration, repairs and leaving early, while RDL 7/2019 and Ley 12/2023 are the two recent reforms that changed it (contract length, stressed zones, large landlords, rent limits). Together they come to about 65,000 words, and I kept only the current version of each article, labelling text that is not yet in force as future text (as happened with an LAU art. 10 change announced for 15 November 2026, which was later repealed).

## Ingestion

- **Extract:** parse the BOE XML; each article (`<bloque>`) keeps only its latest `<version>`; editorial notes (`nota_pie`) are dropped; TÍTULO/CAPÍTULO headings become the article's heading path.
- **Clean:** normalise whitespace and non-breaking spaces.
- **Chunk:** one chunk per article; articles over 400 words are split on paragraph boundaries into numbered parts.
- **Metadata on every chunk:** `source` (law), `location` (article and title), `heading`, `part`, `doc_id`, `url` (BOE link), `words`, `hash`, `design`. The chunk text starts with "SOURCE — LOCATION (heading)".
- **Embed and store:** `gemini-embedding-2` (768 dimensions, RETRIEVAL_DOCUMENT / RETRIEVAL_QUERY) into ChromaDB in `index/` (cosine). A chunk is embedded only if its id and hash are not already stored; query embeddings are cached in `index/query_cache.json`.
- **Number of chunks:** 267 in the chosen design (LAU 112, Ley 12/2023 118, RDL 7/2019 37), plus 54 for the LPH after the demo.

**Known issue (not fixed):** the *Disposiciones* at the end of each law (83 chunks: 38 in the LAU, 37 in Ley 12/2023, 8 in RDL 7/2019) carry the last TÍTULO of their law as their heading, because the heading path is not reset when the articles end. Their `location`, which citations and the hit rates use, is correct. Fixing it changes those chunks' text, so it would mean re-embedding them and re-running the agent and the judge; it is listed as a fix for the next version.

**Extraction problems fixed:**
1. *All historical versions:* each article in the XML holds every past version; keeping them all tripled the word count and mixed old rules with current ones. Only the latest version is kept.
2. *Future text mixed into current text:* the BOE puts amendments that are not yet in force inside the current article, after "Téngase en cuenta que, con efectos de…". In the 12 November download, LAU art. 10 contained such an amendment (RDL 28/2026, due 15 November 2026). The pipeline splits that text into its own chunk labelled `[redacción futura, en vigor desde el …]`, and AGENTS.md tells the agent to give the date. RDL 28/2026 was then repealed before taking effect (see Corpus), so the current corpus has no future text; the split stays in the pipeline for the next amendment.

## Test set

35 questions in `eval/questions.csv`: **22 single**, **7 multi** (two passages), **6 unanswerable** (on topic, but not covered by the corpus). Mostly Spanish, a few in English.

Examples:
- *multi:* "Si el arrendador es una empresa, ¿cuánto dura como mínimo el contrato y durante cuánto tiempo no se actualiza la fianza?" → LAU Art. 9 + Art. 36: seven years in both cases.
- *unanswerable:* "¿Cuál es el valor del IRAV publicado para octubre de 2026?" → the corpus only says the rent update cannot exceed the IRAV; it gives no published values.

The 35 questions (22 single-article, 7 multi-article, 6 unanswerable) were built and discussed with Claude as he is more efficient to extract things from the article texts, and I reviewed and modified all of them before running the test so they can challenge the model more. We found that q34 ("can the building ban tourist flats?") was marked unanswerable although RDL 7/2019 answers it, so I replaced it with "can an owner who owes community fees vote?" after checking that none of the three laws covers it. I also replaced q20, which asked about an LAU art. 10 change that was repealed before it took effect, with a question on the current art. 10; I didn't change any other question. Because the questions were written from the articles themselves, they are probably easier to search for than real tenant questions, which is a limitation of this test.

## Retrieval

Hit = a retrieved chunk has the expected law and article. Measured on the 29 answerable questions, initial corpus only (23 November version).

| Design | hit@1 | hit@3 | hit@5 | two-article questions with both articles @5 | words added to prompt @5 |
|---|---|---|---|---|---|
| **articles** (one chunk per article) | **0.759** | **0.966** | **1.000** | **5/7** | 1,427 |
| fixed200 (200 words, 50 overlap) | 0.690 | 0.828 | 0.897 | 4/7 | 1,070 |

(Over all 29 answerable questions, "every expected article in the top 5" is 0.931 for articles and 0.793 for fixed200. On the 12 November corpus, before the repealed text was removed and q20 replaced, the figures were 0.793 / 1.000 / 1.000 for articles and 0.759 / 0.897 / 1.000 for fixed200, with both articles for 5/7 and 3/7 two-article questions: articles was the better design in both versions.)

I chose one chunk per article because it put the right article in the top 3 for 28 of 29 questions (97% against 83% for 200-word pieces) and in the top 5 for all of them, and, for the 7 two-article questions, delivered both articles in 5 of them (against 4). With fixed pieces, 3 of 29 questions would reach the agent without the article they need, even in the top 5, which means at best an incomplete answer or a wrong "I don't know" and at worst an answer from memory, so about 350 extra words per question (a fraction of a cent) is a cheap price, and it also matches how lawyers cite: by article.

## Tools and subagent

Descriptions given to the model (docstrings in `server.py`):

**`search(query)`**
> Search Spanish residential rental law (official consolidated BOE texts, in Spanish): the LAU (Ley 29/1994 de Arrendamientos Urbanos), Ley 12/2023 por el derecho a la vivienda and RDL 7/2019 de medidas urgentes en materia de vivienda y alquiler, plus any document added later with add_document.
>
> Use it for any question about renting a home in Spain: contract duration and extensions, rent and rent updates, deposits (fianza) and guarantees, who pays repairs, expenses and agency fees, ending the contract, eviction protections, stressed-market areas. Write the query in Spanish legal terms for best results (e.g. "fianza vivienda mensualidades"). Call it again with different words if the results do not cover the question.
>
> Returns the 5 most relevant passages, each headed with SOURCE (law), LOCATION (article or preamble) and URL. Cite answers as [SOURCE, LOCATION]. If no passage covers the question, the corpus does not answer it.

**`add_document(path)`**
> Add a legal document to the rental-law corpus so search can find it.
>
> `path` is a local file: a BOE consolidated-text .xml (from the BOE open-data API), or a .pdf, .txt or .md. The file is cleaned, split by article, embedded with Gemini and stored in the index.
>
> If the same file is already indexed and unchanged, nothing is embedded and it says so. If it was indexed before but its text changed, the old chunks are replaced. Returns how many chunks the document has and how many were newly embedded.

It imports `index.index_file` (the same pipeline as `main.py index`, not rewritten).

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
> **corpus-researcher:**
>
> No. Si el contrato no incluye ninguna cláusula de actualización, el casero no puede subir la renta cada año.
>
> - **No hay subida sin un pacto expreso.** Durante el contrato, la renta solo puede actualizarse en la fecha en que se cumple cada año de vigencia, y "en los términos pactados por las partes". La ley dice: "En defecto de pacto expreso, no se aplicará actualización de rentas a los contratos" [LAU (Ley 29/1994), Artículo 18.1]. Esta regla viene de la reforma del RDL 7/2019 [RDL 7/2019, Artículo primero, apartado Nueve].
> - **Si hubiera pacto, la subida tiene un tope.** Cuando la cláusula no indica qué índice se usa, se aplica el IRAV. Aunque lo indique, la subida anual nunca puede superar la variación del IRAV [LAU (Ley 29/1994), Artículo 18.1; Disposición adicional undécima].
> - **Hace falta avisar por escrito.** La renta actualizada solo se puede cobrar a partir del mes siguiente a que una parte se lo notifique a la otra por escrito, indicando el porcentaje aplicado. Basta una nota en el recibo del mes anterior [LAU (Ley 29/1994), Artículo 18.2].
> - **Hay una excepción: las obras de mejora.** Si el casero hace obras de mejora después de los primeros cinco años de contrato (siete si el casero es una empresa o persona jurídica), puede subir la renta, salvo que el contrato diga lo contrario. La subida se calcula con el interés legal del dinero más tres puntos sobre lo invertido. Tiene un máximo del 20 % de la renta vigente y debe notificarse por escrito con el desglose de costes [RDL 7/2019, Artículo primero, apartado Diez, que da nueva redacción al art. 19 LAU]. Este texto procede de la versión del RDL que modifica la LAU; no he recuperado el artículo 19 en la versión consolidada.
>
> URLs: https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003 ; https://www.boe.es/buscar/act.php?id=BOE-A-2019-3108

(Also in `eval/subagent_transcript.md`.) For the last point it cited the amending decree instead of the consolidated LAU art. 19: the duplicate-text risk described under Corpus.

## Adding a document

**If the document is already indexed:** each chunk has an id and a content hash. Unchanged → nothing is embedded and the tool says so. Changed → new chunks are embedded and outdated ones removed. In the demo, adding the LPH a second time embedded **0** chunks. Calling the real tool over MCP on the same file (24 Nov 2026) returns: *"'LPH (Ley 49/1960)' is already indexed and unchanged (54 chunks). Nothing was embedded."*

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

`agent.py`: LangChain `create_agent` on `gemini-3.5-flash-lite`, tools from `server.py` over MCP, `AGENTS.md` as the system prompt. The agent first ran on `gemini-3.5-flash`, whose free tier allows 20 requests a day; that ran out after 10 questions (those answers are kept in `eval/answers_gemini-3.5-flash_first10.jsonl`), so all 35 were answered with `gemini-3.5-flash-lite`. Flash-lite ignores `temperature=0` (fixed sampling), so a re-run can word answers slightly differently; the saved answers in `eval/answers.jsonl` are the ones evaluated.

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
| Expected passage cited | 29/29 |
| Correct refusals (unanswerable) | 6/6 |
| Answered an unanswerable question | 0/6 |
| Wrong refusals (answerable) | 0/29 |

**LLM judge rubric** (`RUBRIC` in `evaluate.py`; the judge gets the question, the reference answer, the agent's answer and the retrieved passages, and must not use its own knowledge):
- **correct (1/0):** the main conclusion agrees with the reference and nothing contradicts it; missing a minor detail is fine, missing a condition that changes the outcome is not. For unanswerable questions: it says the corpus doesn't cover it and doesn't answer anyway.
- **supported (1/0):** every factual legal claim appears in the retrieved passages. A plain refusal counts as supported; "consult a lawyer" is not a claim.

Judge models: `gemini-3-flash-preview` (31 answers), with fallbacks `gemini-3.8-flash` (3) and `gemini-3.5-flash` (1) when free-tier limits blocked the first. None is the agent's model.

**Results:**

| | Result |
|---|---|
| Correct | **34/35** (wrong: q04) |
| Unsupported (something made up) | **4/35** (q04, q07, q25, q32) |
| Correct refusals | **6/6** |
| Wrong refusals | **0/29** |

On the original q20 (the repealed art. 10 change), the agent had refused although the corpus then contained the text: 33/35 correct and 1/29 wrong refusals on the 12 November corpus.

**My agreement with the judge** (20 answers I graded myself, before seeing the judge's grades):

| | Agreement | Cohen's κ | Disagreements |
|---|---|---|---|
| correct | 95% (19/20) | 0.00 | q04 |
| supported | 80% (16/20) | 0.00 | q04, q07, q25, q32 |

κ is 0 for both because I gave all 20 answers the same grade in each column (all correct, all supported). When one grader gives the same grade every time, any agreement could be luck, so κ = 0 even at 95% agreement. (With the original q20, which I graded as not correct, κ for *correct* was 0.64; the new q20 was graded on 24 November, before the judge ran on it, and we agreed.)

After reviewing the 4 disagreements against the passages, I agreed with the judge on all of them (`eval/human_review.csv`): it caught invented details I had missed. In q04 I had even praised the answer as "more complete", and the extra detail was the invented part. The judge was not fully consistent, though: it marked q04 incorrect but q25 correct for the same invented clause.

My words: *"I now agree with the judge, showing its true power."*

The AI judge was better than me at spotting invented details: it found 4 that I missed, and in q04 I had even praised the invented part as "more complete". But it gave q04 and q25 different grades for the same mistake, so I would trust it alone to grade at scale and flag problems, while a human still has to check every flagged answer against the law text, especially when the claim could cost a tenant money.

## Failures

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 0 | — |
| Wrong answer from the right passage | 0 | — |
| Unsupported claim | 4 | q04, q25, q07, q32 |
| Wrong refusal | 1 | original q20 (replaced) |
| Bad test question | 1 | original q34 (replaced) |

My reasons (from `eval/failures.csv`):
- **Original q20 → wrong refusal.** *"It found the right article and didn't conclude anything wrong. It just refused a question the corpus answers. The likely cause is that it didn't trust text that only applies from 15 Nov 2026, so it stopped after one search."* The question was later replaced because the law change it asked about was repealed; it stays here because the failure (refusing after one search, against AGENTS.md rule 4) happened, and it is the evidence for safeguard 5. The new q20 was answered correctly.
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
| Latency | median 36.8 s, mean 45.2 s in the evaluation run (free-tier rate limits caused many retries); about 4–6 s per question without throttling |

## AI use

Claude wrote the code (the BOE download and cleaning, chunking, the MCP server, agent.py, the evaluation scripts and the grading page), ran the guardrail tests, and drafted the first version of the 35 questions, so that I can refine and modify them into being more challenging for the AI Judge. I made the decisions: the topic, one chunk per article after seeing the comparison, the replacement for q34, my own grades for 35 answers (given before I saw the judge's), the classification of the failures, and the ship decision with its safety measures. I also wrote the report and Claude helped me check my spelling and narrative of the report. Checking three failures against the law myself showed why this matters: two legal websites, and a web lookup by Claude in another chat, described an older version of articles 11 and 21, and only the BOE text in the corpus was current.

Models used: Gemini (`gemini-embedding-2` for embeddings, `gemini-3.5-flash-lite` for the agent, `gemini-3-flash-preview` with fallbacks for the judge) and Claude (Claude Code) for coding and drafting.
