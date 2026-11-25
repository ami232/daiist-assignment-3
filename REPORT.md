# Assignment 3 Report

- **Name**: Gonzalo Mir García
- **Student ID**: 20107
- **Group**: BBADBA 5B 

The corpus and the test questions are in Spanish because the users (Spanish HR staff) and the laws are Spanish. Code, prompts and this report are in English.

## Use case 

**Who asks:** an HR administrator at a Spanish SME (10–100 employees) with no in-house lawyer. They check the statutory rule before acting: how many holiday days, how long a probation period can be, what severance a dismissal costs, which safety obligations apply and what the fine is for missing one.

**What they do with the answer:** they draft a contract clause, compute a severance offer, or decide whether to call the labour lawyer.

**Cost of a wrong answer vs "I don't know":** a wrong figure (for example 20 instead of 33 days per year of severance, or a wrong deadline) means an unlawful dismissal, a lawsuit or a labour-inspection fine. Under LISOS art. 40 a serious breach costs €751–7,500, and a very serious safety breach up to €983,736. "I don't know" costs a call to a lawyer. A wrong answer is therefore far more expensive than a refusal, so the assistant should refuse whenever the text does not support an answer.

## Corpus

Consolidated texts from the BOE open-data API (`/datosabiertos/api/legislacion-consolidada`), current versions as of 2026-11-24. Licence: BOE content may be reused freely with attribution (Aviso legal del BOE; Ley 37/2007 and RD 1495/2011 on re-use of public-sector information). Laws are not covered by copyright (art. 13 Ley de Propiedad Intelectual). The texts contain no personal data.

| Document | URL | Version used | Licence | Words (articles only) |
|---|---|---|---|---|
| Estatuto de los Trabajadores (RDL 2/2015) | https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430 | consolidated, last change in force 2026-11-19 | BOE free reuse | 54,532 |
| Ley de Prevención de Riesgos Laborales (Ley 31/1995) | https://www.boe.es/buscar/act.php?id=BOE-A-1995-24292 | consolidated | BOE free reuse | 19,492 |
| Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000) | https://www.boe.es/buscar/act.php?id=BOE-A-2000-15060 | consolidated, last change 2026-11-19 | BOE free reuse | 24,730 |
| *Added later:* Ley 10/2021 de trabajo a distancia | https://www.boe.es/buscar/act.php?id=BOE-A-2021-11472 | consolidated | BOE free reuse | ~24,500 |

The base corpus has **98,754 words** in 272 articles and dispositions, after removing preambles, signatures and amendment notes.

## Ingestion

- **Extract:** the BOE API returns XML with one `<bloque>` per article and every historical `<version>` of it. `index.py` keeps only the last version, which is the one in force. Headings (`TÍTULO`, `CAPÍTULO`, `Sección`) become a hierarchy path.
- **Clean:** preambles, signatures and *nota inicial* blocks are dropped, along with articles that are repealed or empty. Whitespace and non-breaking spaces are normalised.
- **Extraction problem fixed:** each article carried `nota_pie` paragraphs such as "Se modifica por el art. 1 del Real Decreto-ley…" or "Redacción anterior…". They are not law, but they repeat words like "despido" and "modifica" across many articles and pulled the wrong articles into the results. They are removed (0 remaining in the chunks). The parser also had to take the *last* `<version>`: taking the first would have indexed the 2015 text, for example a birth leave of 16 weeks instead of the current 19.
- **Chunk (chosen design, `article`):** one chunk per article. Articles over 350 words are split at numbered *apartados*, and each part repeats the article heading. `gemini-embedding-2` takes the task as a text prefix (`title: … | text: …` for documents, `task: search result | query: …` for queries). A plain list sent to it is merged into a single vector, so each text is sent as its own `Content`.
- **Metadata per chunk:** `source` (BOE id), `title`, `location` (e.g. `Artículo 49, apdos. 1-2`), `heading`, `hierarchy`, `in_force_since`, `url` and `file_sha1`.
- **Chunks:** 429 (`article` design) and 450 (`fixed` design). Vectors are stored in ChromaDB under `index/chroma` (32 MB) and saved after each batch of 50. `main.py index` embeds only the chunks that have no vector yet.

## Test set 

I wrote 36 questions from the articles, phrased the way an HR user would ask them, before tuning anything. Each reference answer was checked against the article text.

| Kind | Count |
|---|---|
| single | 24 |
| multi (two passages, often across two laws) | 6 |
| unanswerable (close to the topic) | 6 |

Examples:

- **multi, m03:** *"Si una empresa no lleva el registro diario de jornada: ¿qué obligación incumple y qué tipo de infracción comete?"* The obligation is in ET art. 34.9; the classification as a serious infringement is in LISOS art. 7.5.
- **unanswerable, u01:** *"¿Cuál es la cuantía del salario mínimo interprofesional este año?"* ET art. 27 says only that the Government sets the minimum wage each year. The amount is in a yearly royal decree that is not indexed.

The unanswerable questions all sit next to the corpus: social-security benefits (LGSS), contribution rates, collective agreements, the minimum-wage amount, and remote-work expenses (Ley 10/2021 was not indexed yet).

## Retrieval

Hit rate on the 30 answerable questions. A hit means a chunk from the expected law and article appears in the top k. `multi_all@k` means both expected passages appear in the top k (multi questions only). Words are the average words passed to the model at k = 5. Source: `eval/retrieval.csv`.

| Design | hit@1 | hit@3 | hit@5 | multi_all@3 | multi_all@5 | words @5 |
|---|---|---|---|---|---|---|
| **article chunks, dense** | **0.933** | **1.000** | **1.000** | **0.833** | 0.833 | 1,425 |
| article chunks, hybrid (dense + BM25, RRF) | 0.900 | 0.967 | 0.967 | 0.500 | 0.833 | 1,520 |
| fixed 250-word windows, dense | 0.900 | 1.000 | 1.000 | 0.500 | 0.833 | 1,250 |
| fixed 250-word windows, hybrid | 0.900 | 0.967 | 0.967 | 0.500 | 0.500 | 1,250 |

 **Choice: article chunks with dense search.** It is best or tied on every column, and it is the only design that gets both passages of a multi question into the top 3 in 5 of 6 cases. Its citations are also exact articles, which an HR user can check. Hybrid search was *worse*: BM25 boosts every article that repeats the query words (q17, "reclamar contra su despido", drops out of the top 5 because a dozen articles contain "despido"). Fixed windows cost about 175 fewer words per prompt, but they split articles and produce citations like `Artículo 37; Artículo 38`.

Caveat: hit@5 = 1.0 suggests the questions use the law's own vocabulary and are easy for retrieval. Questions written in everyday language ("¿me pueden echar estando de baja?") would be a harder test.

## Tools and subagent

**`search(query)`**, as the model reads it: *"Search Spanish labour law: the Estatuto de los Trabajadores (RDL 2/2015), the Ley de Prevención de Riesgos Laborales (Ley 31/1995) and the LISOS (RDL 5/2000) … Use it for any question about employment contracts, working time, holidays, leave, pay, dismissal and severance … Write the query in Spanish with the legal terms you expect in the text … Returns the 5 most relevant passages … each headed by "CITE AS: [law, article/apartado]", the date that version came into force and the BOE link."*

**`add_document(path)`**: *"Add a document to the labour-law index … a BOE consolidated-text XML (best: split by article), or a .pdf, .txt, .md or .html … If the same file (same content) is already indexed, nothing is embedded … If a different version of a document with the same name is indexed, its old chunks are replaced."* It imports `chunk_file` and `embed_and_store` from `index.py`.

One search result, for "¿Cuántos delegados de prevención corresponden a una empresa de 80 trabajadores?" (truncated):

```
[1] CITE AS: [Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 35, apdos. 1-4] | en vigor desde 1996-02-10 | https://www.boe.es/buscar/act.php?id=BOE-A-1995-24292
Artículo 35. Delegados de Prevención.
1. Los Delegados de Prevención son los representantes de los trabajadores ...
De 50 a 100 trabajadores: 2 Delegados de Prevención.
...
```

**Subagent** (`.claude/agents/corpus-researcher.md`, tools: `mcp__corpus__search` only). It searches in Spanish up to 4 times, answers only from the passages, cites each claim with the `CITE AS` text, starts with `El corpus no cubre esta pregunta.` when the passages do not answer, and gives no advice on a specific case.

**Transcript from the editor** (Claude Code, subagent `corpus-researcher`, one call to `mcp__corpus__search` with query "horas extraordinarias máximo al año"):

> **User:** ¿Cuántas horas extra puede hacer un trabajador al año y es obligatorio hacerlas?
>
> **corpus-researcher** → `search("horas extraordinarias máximo al año")` → 5 passages (ET arts. 35 apdos. 1-4, 35 apdo. 5, 34 apdos. 1-3, 36 apdos. 1-3, 34 apdo. 9)
>
> **corpus-researcher:** Como máximo se pueden hacer 80 horas extraordinarias al año. Hacerlas es voluntario, salvo que se hayan pactado en convenio colectivo o en el contrato individual de trabajo, y aun así dentro de ese límite [Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdos. 1-4].
>
> - Se consideran horas extraordinarias las que se trabajan por encima de la jornada ordinaria máxima, que es de 40 horas semanales de promedio en cómputo anual [Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 1-3].
> - No cuentan para el límite las compensadas con descanso en los cuatro meses siguientes, ni las trabajadas para prevenir o reparar siniestros urgentes [Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdos. 1-4].
> - Si la jornada anual del trabajador es inferior a la general de la empresa, el máximo se reduce en la misma proporción [Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdos. 1-4].
> - Los trabajadores nocturnos no pueden hacer horas extraordinarias [Estatuto de los Trabajadores (RDL 2/2015), Artículo 36, apdos. 1-3].
> - Se pagan (nunca por debajo de la hora ordinaria) o se compensan con descanso, según convenio o contrato; si no se ha pactado nada, se compensan con descanso en los cuatro meses siguientes [Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdos. 1-4].
> - La jornada se registra día a día y el trabajador recibe con la nómina una copia del resumen [Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdo. 5].
>
> Para saber si las horas extra son obligatorias en su empresa y cómo se pagan, revise el convenio colectivo aplicable y los contratos.

Every claim is in the retrieved passages, and the subagent searched once because the first results covered both parts of the question.

## Adding a document

**If the document is already indexed:** `add_document` compares the file's SHA-1 with the one stored on the chunks for that source. If they are the same, it embeds nothing and answers "Already indexed … Nothing was embedded." If a different version of the same document is indexed, it deletes the old chunks and stores the new ones, so the index never holds two versions of the same law.  *Why: a law is updated in place on the BOE; keeping the old version would let the assistant cite repealed text.*

**Unanswerable question:** u02, *"¿Tiene la empresa que pagar los gastos de internet y equipos de un trabajador en teletrabajo?"*. ET art. 13 refers to Ley 10/2021, which is not indexed.

**Document added:** Ley 10/2021 de trabajo a distancia (BOE-A-2021-11472). Art. 12 states that remote work "deberá ser sufragado o compensado por la empresa" (the company must pay or compensate the costs).

**Answer before** (evaluation run):

> El corpus no cubre esta pregunta porque el régimen detallado de compensación de gastos e internet en el teletrabajo se remite a la Ley 10/2021 de trabajo a distancia, la cual no se encuentra indexada en la base de datos actual. No obstante, el Estatuto de los Trabajadores establece expresamente que la empresa tiene la obligación de suministrar los medios, equipos y herramientas adecuados para el trabajo a distancia [Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 3-4]. …

The refusal is right, but the second sentence is an unsupported claim: art. 37 deals with leave, not equipment. The judge marked it as neither correct nor supported. See Failures.

**Adding it** (`demo_add_document.py`, which calls the MCP tool twice; output in `eval/add_document_demo.json`):

- First call: `Indexed BOE-A-2021-11472.xml as 'Ley de trabajo a distancia (Ley 10/2021)': 70 new chunks embedded (70 in tota…`
- Second call, same file: `Already indexed: BOE-A-2021-11472.xml (Ley de trabajo a distancia (Ley 10/2021)) is in the index with the same content (70 chunks). Nothing was embedded.`

**Answer after** (retrieved: Ley 10/2021 arts. 7, 11, 12, 21 and DT 3ª). The citation guardrail fired on the first attempt and the retry passed:

> Sí, la empresa debe sufragar o compensar los gastos relacionados con el teletrabajo.
>
> El desarrollo del trabajo a distancia debe ser sufragado o compensado por la empresa y no puede suponer que el trabajador asuma gastos relacionados con los equipos, herramientas y medios vinculados a su actividad laboral [Ley de trabajo a distancia (Ley 10/2021), Artículo 12].
>
> Los aspectos principales son:
>
> *   **Dotación de medios:** El trabajador tiene derecho a la dotación y mantenimiento adecuado por parte de la empresa de todos los medios, equipos y herramientas necesarios para su actividad, conforme al inventario que debe incluirse en el acuerdo de trabajo a distancia [Ley de trabajo a distancia (Ley 10/2021), Artículo 11].
> *   **Acuerdo de trabajo:** El acuerdo de trabajo a distancia debe incluir obligatoriamente un inventario de los medios, equipos y herramientas, así como la enumeración de los gastos que pudiera tener el trabajador y la forma de cuantificar la compensación que la empresa debe abonar [Ley de trabajo a distancia (Ley 10/2021), Artículo 7].
> *   **Negociación colectiva:** Los convenios o acuerdos colectivos pueden establecer los mecanismos para la determinación y compensación de estos gastos [Ley de trabajo a distancia (Ley 10/2021), Artículo 12].
>
> Le recomiendo revisar el convenio colectivo de aplicación, ya que este determinará los términos específicos para la compensación de gastos y el uso de los equipos.

The answer is now correct and every claim is in arts. 7, 11 and 12 of Ley 10/2021. Note: the committed index now contains Ley 10/2021, so u02 is answerable from here on. The evaluation results above were produced before the document was added, and the retrieval comparison filters to the base corpus.

## Harness and guardrails

`agent.py` uses LangChain `create_agent` on `gemini-3.1-flash-lite`, with fallbacks to `gemini-flash-lite-latest` and `gemini-3.5-flash-lite`. The tools come from `server.py` over MCP stdio, through one persistent session wrapped as LangChain tools. `AGENTS.md` is the system prompt.

- **AGENTS.md rules** (each with its reason in the file): search before every answer; answer only from the results; cite every claim with the `CITE AS` text; start with `El corpus no cubre esta pregunta.` when not covered and say what is missing; give no advice on a specific case; call `add_document` only when explicitly asked; be brief.
- **Approval step:** `HumanInTheLoopMiddleware(interrupt_on={"add_document": approve/reject})` with an in-memory checkpointer. In a terminal the harness prints the tool call and asks `Approve? [y/N]`. Without a terminal (evaluation, CI) it rejects the call.
- **Call limits:** at most 8 model calls and 5 tool calls per question. `ModelRetryMiddleware` and `ModelFallbackMiddleware` handle Gemini 503 errors.
- **Extra guardrail: citation check.** After the agent answers, code extracts every `[law, location]` citation and checks it against the `CITE AS` strings the search tool returned in this run. An answer with no citation that is not a refusal fails the check. On failure the agent gets one retry with the problem spelled out; if the retry fails too, the answer is replaced by a refusal.
  - **Case where it fired (m03):** the first answer cited `[LISOS (RDL 5/2000), Artículo 7, apdo. 5]`, but search had returned the chunk `Artículo 7, apdos. 1-9`. The guardrail rejected it, and the agent rewrote the answer citing the retrieved chunk.
  - **Overall:** it fired on 9 of 36 questions. All 9 recovered on the retry, so none ended as a forced refusal. In most cases the cited location was *more precise* than the chunk (an apartado inside a retrieved range), not invented. See Failures.

## Evaluation

**Code checks** (`evaluate.py`, `eval/results.csv`):

| Check | Result |
|---|---|
| Refused (starts with the refusal phrase) | 6 of 6 unanswerable, 0 of 30 answerable |
| Citations present and valid (every citation was returned by search) | 36 of 36 |
| Expected article cited (answerable questions) | 30 of 30 |
| Errors | 0 |

**LLM judge rubric** (in `evaluate.py`; the judge sees the question, the reference answer, the agent's answer and all retrieved passages):

- `correct` = 1 if the answer states the reference's key facts without contradicting it. For unanswerable questions, 1 only for a refusal with no substantive answer.
- `supported` = 1 if every factual claim is in the retrieved passages, even when the claim happens to be true.

The judge model was `gemini-3.5-flash`, falling back to flash-lite models during 503 errors (23, 11 and 2 verdicts respectively).

**Results** (judge, `eval/summary.json`):

| | Count |
|---|---|
| Correct answers to answerable questions | 28 / 30 |
| Unsupported (supported = 0) | 2 / 36 (q01, u02) |
| Correct refusals | 6 / 6 by code; 5 / 6 by the judge (u02 refused but added an unsupported claim) |
| Wrong refusals | 0 / 30 |

By kind, correct: single 1.00, multi 0.67, unanswerable 0.83.

**Agreement with my grades:** I graded 20 answers by hand (q01–q10, m01–m06, u01–u04) in `eval/human_labels.csv`, without seeing the judge's verdicts, checking each claim against the article text.

| | Agreement | Cohen's κ |
|---|---|---|
| correct | 100 % (20/20) | 1.00 |
| supported | 90 % (18/20) | 0.62 |

Both disagreements (q05, m01) go the same way: I marked them unsupported and the judge did not. In both answers the agent widens an exception beyond the text. In q05 it limits the copy of the notice to the workers' representatives to "economic causes", while art. 52.c covers economic, technical, organisational and production causes. In m01 it says the severance need not be paid at once "for economic causes", while the text allows it only when the economic situation *prevents* paying it. The judge catches invented facts (q01, u02) but misses subtle distortions of a rule's scope, so its `supported` count is an upper bound.


## Failures 

| Question | Cause | Detail |
|---|---|---|
| m05 | retrieval miss | The agent's searches returned LPRL art. 21 but not LISOS art. 13, so the answer covers only the first part (the worker may stop work and leave). It does not mention that impeding this is a very serious infringement, and it does not say that this part is not covered, as rule 4 requires. |
| m06 | wrong answer from the right passage | Classed the infringement as serious (art. 22.2) but left out the fine amounts (art. 40.1.e: €3,750–12,000) the question asked for. |
| u02 | unsupported claim | A correct refusal, plus an invented obligation cited to an unrelated article (art. 37). The citation check passed because art. 37 *had* been retrieved: it checks that a citation is real, not that it supports the sentence. |
| q01 | unsupported claim | The core answer is right (30 days, not exchangeable for money), but it adds "salvo en los supuestos de extinción del contrato". That exception is true in practice but does not appear in art. 38: it comes from the model's own knowledge, in an uncited sentence. The guardrail let it through because it only requires at least one citation per answer, not one per claim. |

| m04 | (correct, but formatting) | The content is right, but the citations copy the whole `CITE AS: [...] \| en vigor desde ... \| url` header inside the brackets. The citation check accepted them because its regex finds the inner `[law, article]`. |
| q05, m01 | unsupported claim (found by my grading, not by the judge) | The agent widens an exception beyond the text (see Evaluation). These are subtle scope errors, but for an HR user they change who the rule applies to. |

By cause: retrieval miss 1, wrong answer from the right passage 1, unsupported claim 4 (2 found by the judge, 2 more by my grading), wrong refusal 0, bad test question 0.

**What to fix first:**

1. **Multi-part questions are the weak spot** (correct on 4 of 6). Make the agent search once per part of the question (m05 missed the second law because it searched only once), and require it to say which part is not covered instead of skipping it.
2. **Support check per sentence:** the citation guardrail proves that citations are real, not that every sentence has one or that it says what the passage says (q01, u02, and the scope errors in q05 and m01). A cheap LLM check of "does passage X support sentence Y, with the same scope" would catch them.
3. **Relax the citation matcher** to accept an apartado that falls inside a retrieved range. That would remove most of the 9 retries, which add latency without catching errors.

## Decision 

**Would I let users rely on it?** Yes, as a first lookup with a mandatory check, not as a final authority. On single-article questions it was 24 of 24 correct and fully cited, and it refused all 6 out-of-scope questions with no wrong refusals. On multi-part questions it misses parts (4 of 6), and once it added an unsupported sentence to a refusal.

**For what:** looking up statutory minimums and maxima (holidays, leave, probation, working time, severance formulas, prevention bodies, fine ranges), always with the BOE article link to check before acting.

**Not for:** questions that depend on the collective agreement, on social-security law, or on the facts of a specific dismissal.

**Safeguards:** every answer shows its article citations and BOE links; the citation guardrail stays on; the UI states that the collective agreement can improve on the legal minimum; and anything involving a dismissal or a fine goes to a lawyer.

**Cost and latency per question** (36 questions):

- **Tokens:** 7,696 input and 280 output on average. That is about 8k tokens of a flash-lite model, so a fraction of a cent per question at paid prices and €0 on the free tier.
- **Latency:** median 30 s, mean 108 s. The mean is inflated by Gemini 503 "high demand" errors on the evaluation day: some questions waited 4–12 minutes in retries. Without them a question takes about 10–30 s (1–2 model calls, 1–2 searches, plus a retry when the citation guardrail fires).
- **Embeddings:** each new question uses 1 query embedding (cached in `index/query_cache.json`).

## AI use

I used Claude Code (Anthropic) to write the code (`index.py`, `retrieval.py`, `server.py`, `agent.py`, `evaluate.py`, `demo_add_document.py`), to draft AGENTS.md, the subagent, the test questions and this report from the evaluation output, and to propose candidate use cases. I chose the use case and corpus, reviewed the questions against the BOE text, graded 20 answers by hand, and wrote the decisions and analysis. 
