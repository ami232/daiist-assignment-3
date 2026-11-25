# Assignment 3 Report

- **Name**: Javier Arce López
- **Student ID**: 20158
- **Group**: BBADBA 5B

## Use case

A sample use case would be myself, Javier Arce. Two and a half years ago I found myself in this exact situation: 20 years old and trying to take my DJ entrepreneurial project to a more serious level. At that moment I had some gigs and was making about 150 to 200 euros per month. However, as I started scaling my business and getting more clients, I had to formalise it, and a tool like this would have been great for the many questions I had at that time. I would have used it to decide whether it was legally appropriate for me to become an autónomo, and what rights and obligations came with it. With that information, I could then talk to an expert and analyse the economic viability of the operation.

Users must know this is a chatbot with a RAG system behind it, so it can make errors, and the cost of an error depends heavily on what the error is about. If the question is whether you have to file the 'Declaración de la Renta', and you are told you don't when you actually do (since 1 January 2023, anyone registered as autónomo at any point in the year must file it, first applied in the 2024 filing campaign), you can be fined. That specific question falls outside the indexed laws, so the assistant should refuse it, which is what I want it to do when an error is this costly. If the question is about what a mutua does or does not cover, the economic consequences are less direct and probably less serious. Overall, I would say the cost of errors is relatively high, because a wrong decision can have economic and legal consequences for the user.

## Corpus

The corpus has four Spanish state laws and regulations, downloaded as consolidated text (XML) from the BOE open-data API. Only the parts that concern an autónomo are indexed. "Units" are articles plus additional, transitional and final provisions, as listed in `index/outline.csv`.

| Id | Document | Part indexed | Consolidated as of | Units | Words |
|---|---|---|---|---|---|
| LETA | [Ley 20/2007, Estatuto del trabajo autónomo](https://www.boe.es/buscar/act.php?id=BOE-A-2007-13409) | Whole law | 2026-09-02 | 61 | 16,424 |
| LGSS | [Real Decreto Legislativo 8/2015, Ley General de la Seguridad Social](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724) | Title IV (RETA) and Title V (cese de actividad) | 2026-11-11 | 47 | 18,173 |
| RF | [Real Decreto 1619/2012, Reglamento de facturación](https://www.boe.es/buscar/act.php?id=BOE-A-2012-14696) | The regulation only, without the decree that approves it | 2026-03-31 | 36 | 11,852 |
| RGAT | [Real Decreto 1065/2007, Reglamento de gestión e inspección tributaria](https://www.boe.es/buscar/act.php?id=BOE-A-2007-15984) | Title II: tax censuses, NIF, tax address, record books | 2026-10-28 | 34 | 14,567 |
| **Total indexed** | | | | **178** | **61,016** |
| COT2026 (held out) | [Orden PJC/297/2026, cotización 2026](https://www.boe.es/buscar/act.php?id=BOE-A-2026-7296) | Arts. 18 and 19: 2026 RETA contribution tables | 2026-07-16 | 2 | 2,192 |

The BOE reuse conditions (Ley 37/2007 and RD 1495/2011; [aviso legal](https://www.boe.es/informacion/aviso_legal)) allow commercial and non-commercial reuse if the source is cited, the text is not distorted, the update date is kept, and consolidated texts are stated to be informational only. Every search result carries the citation, the consolidation date and the BOE link, and ends with the BOE notice. The corpus contains no personal data.

## Ingestion

`index.py` runs the same pipeline for every file, and `add_document` reuses it:

1. Fetch the consolidated XML and its metadata (`.meta.xml`: title, consolidation date) into `corpus/`, with a cache.
2. Extract the text. Only the latest version of each block is kept. Editorial notes are stripped, repeal stubs such as "(Derogado)" or "(Sin contenido)" are dropped, and tables become one line per row. Each article keeps its hierarchy path (Título > Capítulo > Sección) and its BOE anchor. Only the ranges in the table above are kept.
3. Chunk with two strategies, using the parameters chosen by me:
   - `article`: one chunk per article; articles over 400 words are split at *apartado* boundaries into parts (e.g. "parte 1/3").
   - `fixed`: windows of 200 words with a 40-word overlap.
4. Embed with `gemini-embedding-2` (768 dimensions, the task as a text prefix) and store in Chroma (`index/chroma`, cosine distance).

Each chunk carries `source`, `location` (e.g. "Artículo 38 ter"), `locations`, `law_title`, `boe_id`, `url` (BOE link to the article), `path` (hierarchy), `part`, `n_words`, `updated` (consolidation date), `block_id` and `design`.

| Design | LETA | LGSS | RF | RGAT | Total | Mean words | Max words |
|---|---|---|---|---|---|---|---|
| `article` (shipped) | 77 | 75 | 51 | 58 | **261** | 238 | 402 |
| `fixed` | 103 | 114 | 74 | 91 | **382** | 199 | 200 |

**An extraction problem I fixed.** : BOE annotations inside the law text. "Téngase en cuenta…" and "Se modifica por…" made up 10.9k of LETA's 27.6k raw words. Footnote (nota_pie) paragraphs inside headings ("CAPÍTULO II … Se añade por el art. 1.8 de la Ley 31/2015") also contributed heavily to this. This text carries no value, and therefore had to be removed.

## Test set

`eval/questions.csv` has 31 questions in Spanish, written before any retrieval tuning. Each has an expected source and location, and a reference answer written by me.

| Kind | Count | Meaning |
|---|---|---|
| single | 16 | answered by one passage |
| multi | 7 | needs two or more passages |
| unanswerable | 8 | close to the topic but not covered by the corpus; q31 is the one the held-out document answers |
| **Total** | **31** | 23 answerable questions are used for the retrieval comparison |

Two examples:

- q05 (single): *¿Qué es la tarifa plana y cuánto pagaría durante el primer año?* (What is the flat rate and how much would I pay in the first year?) Expected: [LETA, Artículo 38 ter]. Reference: a reduced Social Security contribution for the first 12 full calendar months after registering, with no contribution for cese de actividad or vocational training. The amount is set every year by the State Budget Act, which is not in the corpus, so no figure can be given.
- q21 (unanswerable): *¿Qué modelo uso para darme de alta en Hacienda, el 036 o el 037?* (Which form do I use to register with the tax agency, 036 or 037?) The forms are approved by a ministerial order that is not in the corpus, so the reference is the fixed refusal phrase.

To write the questions, I reflected on some of the doubts that appeared when I was immersed in this process myself. I brainstormed with the help of AI to remember some of the things that I found difficult to understand at that time. I then structured the ideas into blocks and developed the 31 questions from these blocks. The fact that 8 questions ended up being unaswerable was not intentional (if all would have been unanswerable, I would have changed some), and helps prove the scope limit of the solution. 

## Retrieval

Three designs were compared on the 23 answerable questions (`eval/retrieval.csv`, `eval/retrieval_summary.csv`). Hit@k counts a question as a hit when an expected passage is among the top k results. Recall@5 is the share of the expected passages in the top 5, and Words@k is the number of words the top k results add to the prompt.

| Design | Chunking | Search | Hit@1 | Hit@3 | Hit@5 | Recall@5 | Recall@5 (multi) | Words@1 | Words@3 | Words@5 |
|---|---|---|---|---|---|---|---|---|---|---|
| A_fixed | fixed 200/40 | dense | **0.870** | 0.957 | **1.000** | 0.899 | 0.667 | 200 | 599 | 999 |
| **B_article** | article ≤400 | dense | 0.826 | 0.957 | **1.000** | **0.964** | **0.881** | 317 | 836 | 1,343 |
| C_article_hybrid | article ≤400 | BM25 + dense (RRF) | 0.652 | 0.870 | 0.913 | 0.790 | 0.595 | 291 | 823 | 1,379 |

**Shipped design: B_article, k = 5.**: With k = 5, all five results go into the prompt. What matters is whether every needed passage is in that set. The order within the top 5 matters much less. That makes Recall@5 the deciding metric rather than Hit@1.

B finds more of what's needed. It ties A on Hit@5 (both find at least one correct passage for every question) and beats it on Recall@5: 0.964 vs 0.899.
Also, on questions that need more than one passage, B reaches 0.881 and A reaches 0.667. Fixed 200-word chunks cut articles apart, so one answer gets spread across several chunks, and some of them miss the top 5. Whole-article chunks keep the answer together.

## Tools and subagent

The MCP server `corpus` (`server.py`) has two tools. Their docstrings are the descriptions the agent reads:

- `search(query)` searches the corpus with the shipped design (B_article, k = 5). Its description lists the four laws and what each covers. It tells the agent to search before answering any question about an autónomo's rights or obligations, more than once with other words if needed, and to write the query in Spanish using the law's own terms. It returns the 5 most relevant fragments, each with a ready-to-copy citation `[SOURCE, Location]`, the law title, the consolidation date, the text and the BOE link, followed by the BOE notice. Errors (empty query, embedding quota) come back as strings starting with "Error:".
- `add_document(path)` adds a BOE consolidated-text XML from inside the repository (e.g. `corpus/BOE-A-2026-7296.xml`) through the same pipeline, embedding only new chunks. If the law is already indexed with the same consolidation date, nothing changes; a newer version replaces the old one; an older version changes nothing. The description says the tool changes the index and should be used only when the user asks. It returns a one-line summary or an "Error:" message, and rejects paths outside the repository, missing files and non-XML files.

Here is one search result, for q05 with the query `tarifa plana reduccion cuotas inicio actividad autonomos` (the first of 5 fragments, text shortened):

```text
[1] Cita: [LETA, Artículo 38 ter] · Ley 20/2007, de 11 de julio, del Estatuto del trabajo autónomo. · texto consolidado a 2 de septiembre de 2026
Ubicación en la norma: TÍTULO V Fomento y promoción del trabajo autónomo > CAPÍTULO II Incentivos y medidas de fomento y promoción del Trabajo Autónomo
Artículo 38 ter. Reducciones en la cotización a la Seguridad Social aplicables por inicio de una actividad por cuenta propia. (parte 1/3)
La cotización a la Seguridad Social de los trabajadores por cuenta propia o autónomos que causen alta inicial o que no hubieran estado en situación de alta en los dos años inmediatamente anteriores, […]
BOE: https://www.boe.es/buscar/act.php?id=BOE-A-2007-13409#a3-5
---
[…4 more fragments…]
---
Texto consolidado del BOE de carácter informativo; no tiene validez jurídica. Para efectos legales, consulte la publicación oficial.
```

The subagent (`.claude/agents/corpus-researcher.md`) has one tool, `mcp__corpus__search`. Its description tells Claude Code to delegate any question on an autónomo's rights or obligations that must rest on the text of the law. It also says what the subagent is not for: personal calculations, regional rules, VAT or income tax outside the invoicing regulation, and companies. The instructions restate the AGENTS.md rules (only what search returns, a `[SOURCE, Location]` citation for every claim, the fixed refusal phrase, partial answers, no personal calculations, the consolidation date with figures, the BOE notice), allow at most 4 searches, and ask for an answer the calling agent can pass on unchanged.

### Subagent transcript (Claude Code, 2026-11-23)

The `corpus-researcher` subagent was called by me from Claude Code with a question taken from a real situation a friend brought to me a few days ago. Therefore, it was not in the test set.
Question passed to the subagent:

> Empecé a operar hace 10 días y todavía no me he dado de alta. Es esto un problema? Me puedo dar de alta de forma retrospectiva?

*(I started trading 10 days ago and still haven't registered. Is this a problem? Can I register retroactively?)*

The subagent made 3 searches, under the limit of 4 in its instructions:

| # | `search` query | Passages returned |
|---|---|---|
| 1 | `plazo solicitud de alta trabajador autónomo RETA inicio de actividad` | [LETA, Artículo 38 ter], [LGSS, Artículo 307], [LGSS, Artículo 305], [LGSS, Artículo 337] ×2 |
| 2 | `declaración censal de alta antes del inicio de actividades` | [RGAT, Artículo 9] ×3 parts, [RGAT, Artículo 13], [RGAT, Artículo 15] |
| 3 | `alta fuera de plazo efectos de las altas cotización desde el día de inicio de la actividad recargo` | [LGSS, Artículo 319], [LGSS, Artículo 307], [LETA, Artículo 38 ter], [LGSS, Artículo 313], [LETA, Artículo 25] |

Searches 1 and 2 ran in parallel, one for each registration: the RETA and the tax census. The third looked for the consequences of registering late.

The subagent's answer, verbatim:

> Sí, puede ser un problema, tanto en Hacienda como en la Seguridad Social. Los fragmentos recuperados no dan un plazo concreto para el alta en el RETA, pero sí explican qué pasa con las cuotas de los días anteriores al alta.
>
> **Hacienda (declaración censal de alta)**
> - Quien deba figurar en el Censo de Empresarios, Profesionales y Retenedores tiene que presentar una declaración de alta en ese censo [RGAT, Artículo 9].
> - La declaración debe presentarse antes de empezar la actividad o de realizar las operaciones [RGAT, Artículo 9]. Esto es según el texto consolidado a 28 de octubre de 2026.
> - La actividad se considera empezada en cuanto se realiza cualquier entrega, prestación o adquisición de bienes o servicios, se cobra o se paga, o se contrata personal, con la finalidad de producir o distribuir bienes o servicios [RGAT, Artículo 9]. Si ya ha hecho alguna de estas cosas, el plazo para esta declaración ya ha pasado.
>
> **Seguridad Social (RETA)**
> - Las personas autónomas están obligadas a solicitar su afiliación y a comunicar su alta en el RETA "en los términos, plazos y condiciones" que fijan la ley y sus normas de desarrollo [LGSS, Artículo 307]. El fragmento no dice qué plazo es.
> - Si se cumplen los requisitos del régimen y no se pidió el alta, las cotizaciones de los periodos anteriores al alta se exigen igualmente. Esas cotizaciones cuentan para las prestaciones una vez pagadas con los recargos que correspondan [LGSS, Artículo 319].
> - Además de las sanciones administrativas por pagarlas fuera de plazo, esas cotizaciones generan intereses al tipo de interés legal del dinero, desde la fecha en que debieron pagarse [LGSS, Artículo 319]. Esto es según el texto consolidado a 11 de noviembre de 2026.
> - La cuota reducida por inicio de actividad (tarifa plana) hay que pedirla en el momento del alta en el RETA [LETA, Artículo 38 ter]. Conviene pedirla en la misma solicitud de alta.
>
> **Lo que no está cubierto**
> Sobre si se puede pedir el alta en el RETA con fecha anterior, qué plazo exacto hay, si un alta tardía afecta a la tarifa plana y cuánto serían los recargos o la sanción:
>
> > No se ha encontrado contenido relacionado a tu pregunta en los documentos a los que tengo acceso. Consulte con un técnico especialista.
>
> No he calculado cuánto tendría que pagar en cuotas atrasadas, recargos o intereses. Es mejor que un gestor o asesor lo calcule y que haga cuanto antes el alta en Hacienda y en el RETA.
>
> > Texto consolidado del BOE de carácter informativo; no tiene validez jurídica. Para efectos legales, consulte la publicación oficial.

Every citation was checked against the indexed chunks:
- The rule "antes de iniciar la actividad" and the definition of when an activity starts are in RGAT art. 9.4. That text is in part 4/4 of the chunk, which search 2 returned.
- LGSS arts. 307 and 319 say what the answer claims.
- The consolidation dates (28-10-2026 for the RGAT, 11-11-2026 for the LGSS) match the index metadata.

The question was only partly covered, and the subagent applied rule 4: it answered what the corpus covers and used the fixed refusal phrase for the rest (a backdated *alta* in the RETA, the exact deadline and the amount of the surcharges). It also followed rule 5 and calculated no amounts.

## Adding a document

When a document is already indexed, the consolidation date in its metadata decides what happens. The same date changes nothing (0 new fragments), a newer version replaces the old chunks, and an older version changes nothing. Chunk IDs are deterministic, so only chunks without a saved vector are embedded.

The demo ran on 2026-11-23 with `demo_add_document.py`, in one agent session, with the approval typed in the terminal. The full record is in `eval/add_document_demo.md` and `.json`.

| Step | Message | Tools | Result |
|---|---|---|---|
| 1. Before | q31: *Actualmente facturo entorno a 600 euros al mes. ¿Qué tramo de cotización me corresponde?* (I invoice about 600 € a month; which contribution bracket applies to me?) | 1 search | Explains the rule (contributions follow net yield; the Budget Act sets a general and a reduced table each year) [LGSS, Artículo 308] and says the documents do not give the brackets. It does not use the fixed refusal phrase. |
| 2. Add | *Añade al índice el documento corpus/BOE-A-2026-7296.xml.* | `add_center` (a tool that does not exist, rejected), then `add_document`, approved | "Añadido: COT2026 (BOE-A-2026-7296, consolidado a 16 de julio de 2026). 8 fragmentos nuevos, 0 omitidos." The agent confirms the addition. |
| 3. After | the same q31 | 1 search | Cites [COT2026, Artículo 18] and [LGSS, Artículo 308], gives the consolidation date and places 600 € in Tramo 1 of the reduced table (net yield ≤ 670 €/month, bases 653.59 to 718.94 €), which matches the chunk. |

The demo showed three problems:
- Step 3 also lists Tramo 2, although 600 € falls in Tramo 1, and has one uncited sentence on the annual regularisation.
- Step 3 treats 600 € invoiced as net yield and picks the user's bracket, which goes against rule 5 (no personal calculations).
- In the first run (`eval/add_document_demo_v1.md`), the citation validator turned the add confirmation into the refusal phrase. The fix: in a turn that ran `add_document`, an answer without citations is accepted, and any citation it makes is still checked.

Afterwards the index was restored to the 4-law corpus (261 / 382 chunks), so the evaluation runs without COT2026 and q31 stays unanswerable.

## Harness and guardrails

`agent.py` builds a LangChain agent (`create_agent`) with `gemini-3.5-flash-lite`, the two MCP tools from `server.py`, and `AGENTS.md` as the system prompt. `main.py ask "…"` prints the tool calls, the answer, each citation with its BOE link, and the number of searches, tokens and seconds.

AGENTS.md has seven rules, each with its reason. It also tells the agent to always answer in Spanish and to copy the two fixed Spanish phrases exactly.
1. Answer only from what `search` returns; search before answering, more than once if needed.
2. Cite every claim as `[SOURCE, Location]`, copied exactly from the search result.
3. If the corpus does not cover the question, answer with the fixed refusal phrase.
4. If only part is covered, answer that part and refuse the rest with the same phrase.
5. Do not calculate the user's own contribution, tax or benefit; explain the rule and recommend a professional.
6. Give the consolidation date with every amount, percentage or deadline.
7. End every answer that cites the law with the BOE notice.

The guardrails are middleware, so the model cannot skip them:
- Any `add_document` call needs approval. It is shown in the terminal ("Allow add_document(…)? It changes the index. [y/N]") and runs only after a yes. With no terminal (evaluation, CI) it is denied automatically, and the agent is told the index was not changed.
- Each question is limited to 4 `search` calls and 8 model calls.
- My extra guardrail is a citation validator. After each model answer, it checks that every `[SOURCE, Location]` cited appeared in that turn's search results, and that any answer other than the refusal cites something. If not, the model gets one chance to repair the answer; a second failure turns the answer into the refusal phrase.

The validator never fired in the 31-question evaluation. Seven probe questions were written to trigger it (`eval/guardrail_cases.md`), and it fired on two. In the first, asked to cite each requirement down to its *apartado*, the model cited `[LETA, Artículo 38 ter, apartado 3]`; the validator flagged it, and the model searched again and rewrote the answer with `[LETA, Artículo 38 ter]`. In the second, a greeting answered without citations was turned into the refusal phrase, a false positive.

In Case 1, asked for citations down to the *apartado*, the model invented `[LETA, Artículo 38 ter, apartado 3]`; the validator flagged it and the model rewrote the answer with retrieved citations. The check compares citation labels and ignores what the fragments say. It also misfired on answers without legal claims: a greeting and the `add_document` confirmation (since fixed) became the refusal. In the 31 evaluation questions it never fired because the model already cited correctly. Its effect is therefore wtill to evaluate in future (if we ship the product)

## Evaluation

| Check | Result |
|---|---|
| Answered / correct refusals / wrong refusals / unanswerable answered | 22 / 7 / 1 (q25) / 1 (q31) |
| Every citation appears in that run's search results | 31/31 |
| Answers citing at least one expected source | 100 % |
| BOE notice present when citing | 100 % |
| Citation validator fired | 0 |

The judge is `gemini-3.5-flash`, a stronger model than the agent's, and it grades each answer with my rubric (`eval/judge_rubric.md`). For each question it gets the question, its kind, the reference answer, the full text of every retrieved fragment and the agent's answer. Using only those inputs, it returns `correct` (1/0), `supported` (1/0) and notes. The rubric covers refusals (a refusal of an answerable question is 0), partial answers (1 if the covered part is correct and the uncovered part is clearly flagged), and personal calculations.

I graded all 31 answers before opening `judge.csv`. Agreement between my grades and the judge's:

| Column | Agreement | Cohen's κ | 1s (me / judge) | Disagreements |
|---|---|---|---|---|
| correct | 96.8 % | 0.78 | 28 / 29 | q15 (I gave 0, the judge 1) |
| supported | 93.5 % | 0.00 | 29 / 31 | q11, q15 (I gave 0, the judge 1) |

κ is 0 for `supported` because the judge marked all 31 answers supported, and with no 0s from the judge κ has no variation to measure. The judge missed the two unsupported details I found (the 3 % in q11 and the simplified invoice in q15).

Results according to the judge (`eval/summary.json`):

| | Count |
|---|---|
| Correct | 29 / 31 |
| Supported | 31 / 31 (my grades: 29) |
| Correct answers to answerable questions | 21 / 23 |
| Correct refusals | 7 / 8 unanswerable (plus q31, a correct non-refusal) |
| Wrong refusals | 1 (q25) |

## Failures

Seven questions were flagged for review in `eval/failures.md`: those with a failed code check, a 0 from me or the judge, or a `multi` question citing only part of the expected passages. My classification:

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 2 | q04 (LGSS art. 317 not retrieved), q07 (3 of 6 articles not retrieved) |
| Wrong answer from the right passage | 1 | q15 (had RF art. 7.2 but said an ordinary invoice is needed) |
| Unsupported claim | 1 | q11 (attributes the 3 % to "autónomos agrarios") |
| Wrong refusal | 1 | q25 (RGAT art. 29 retrieved and enough to answer) |
| Bad test question | 1 | q31 (the answer explains the rule; the reference demands a refusal) |
| Not a failure | 1 | q01 (complete with LGSS art. 305; LETA art. 1 repeats it) |

There were five failures. Two were retrieval misses on multi-part questions (q04, q07). Two were wrong answers given with the right passage retrieved (q11, q15). One was an unneeded refusal (q25). The wrong answers come first. In the use case, I defines that an error costs more than a refusal, and these answers looked well cited. The judge also missed both (κ = 0 on "supported"), so the evaluation cannot detect them. 

The fix: for each amount, percentage or deadline, the agent quotes the sentence that supports it, and the validator checks that the quote appears in a retrieved fragment. Second, add an AGENTS.md rule to search once for each part of the question. In q07 the agent made one search out of four allowed.

## Decision

Cost and latency per question for the agent only (`eval/answers.jsonl`, 31 questions, `gemini-3.5-flash-lite`):

| | Mean | Median | p90 | Max |
|---|---|---|---|---|
| Tokens (input + output) | 7,385 | 6,683 | 8,647 | 13,483 |
| Seconds | 8.9 | 3.0 | 5.0 | 174.8 |

- Tokens are almost all input: 7,099 on average, against 286 of output.
- One outlier (q24, 175 s), most likely spent waiting out a rate limit, pulls up the mean time. Without it, every answer took under 8 s.
- 26 questions needed 1 search and 2 model calls; 5 needed 2 searches and 3 model calls. Multi questions cost more (8,505 tokens on average, against 6,883 for single).
- Each question also embeds its search queries with `gemini-embedding-2` (cached).
- The judge (`gemini-3.5-flash`) is an evaluation cost only. Its free tier allows about 20 requests a day, so judging all 31 answers took more than one day.

My final evaluation of the tool is that it CAN be shipped. We ship it, with two fixes first. By my grades, 28 of 31 answers were correct, and it refused 7 of 8 unanswerable questions (q31 was a test-set error). Every citation came from that run's search results and links to the BOE, so users can check each claim. A question costs about 7,400 tokens and the median answer takes 3 s. In the use case, the tool prepares users before they see an adviser and sends them to a specialist when the corpus has no answer. The fixes address the costliest failures: quote-checking for amounts and deadlines (q11, q15) and one search per question part (q04, q07).

## AI use

I used Claude Code to write the code: ingestion, retrieval, the MCP server, the agent harness, the evaluation scripts and the tests. It also drafted AGENTS.md and the subagent definition, which I reviewed and approved. It built the data tables in this report from the evaluation files and wrote the English translations of the Spanish questions and answers. I also used Claude to draft and edit parts of the report text, and an AI assistant to brainstorm while writing the questions (see Test set).

The following are mine:
- the use case
- the 31 questions and their reference answers
- the choice of rules in AGENTS.md and the refusal phrase
- the judge rubric
- the chunking parameters and the choice of the shipped design
- the policy for documents that are already indexed
- the choice of the citation validator as the extra guardrail
- my grades of the 31 answers
- the classification of the failures
- the decision to ship