# Assignment 3 Report

- **Name**: Jesús López Cubas
- **Student ID**: 20414
- **Group**: BBADBA 5B

## Use case

**Who asks.** An analyst on a merger arbitrage desk that trades Spanish takeover bids (OPAs). Before sizing a position the analyst needs the rules that decide when the deal closes and whether it can break: how long the CNMV has to authorise the offer, the acceptance period, which conditions let the bidder walk away, what a competing bid does to the timetable, when the bidder can squeeze out minorities, and when the deal also needs CNMC (competition) or foreign investment clearance.

**What they do with the answer.** It feeds the two inputs of a merger arb trade. The time to close sets the annualised return on the spread, and the conditions and walk away rights set the probability that the deal breaks, which sets the downside.

**What a wrong answer costs compared with "I don't know".** A wrong answer misprices the trade. Reading "70 días hábiles" where the rule says "70 días naturales" moves the expected closing date and the annualised return, and missing a condition the bidder can use to withdraw understates break risk. "I don't know" only costs a few minutes reading the article or the offer prospectus, or a call to deal counsel. So the system refuses when the corpus does not answer, cites every claim so the analyst can check it in seconds, and blocks answers whose citations were not retrieved.

Questions and answers are in Spanish because the rules, the CNMV filings and the analyst's working sources are in Spanish.

## Corpus

| ID | Document | URL | Date (version used) | Licence | Words |
|---|---|---|---|---|---|
| RD1066-2007 | Real Decreto 1066/2007, régimen de las ofertas públicas de adquisición de valores | https://www.boe.es/eli/es/rd/2007/07/27/1066/con | 27 Jul 2007, consolidated text (latest amendment in force from 2 Oct 2014) | BOE: reuse authorised under Ley 37/2007 and the BOE legal notice. Legal texts are not protected by copyright (art. 13 LPI) | 22,930 |
| CNMV-QA-OPAS | CNMV, Preguntas y respuestas sobre ofertas públicas de adquisición de valores | https://www.cnmv.es/docportal/Legislacion/FAQ/QAs_OPAs.pdf | Feb 2022 (PDF date) | CNMV legal notice: reuse allowed citing the source and without altering the content | 3,590 |
| LDC-15-2007 | Ley 15/2007, de Defensa de la Competencia | https://www.boe.es/eli/es/l/2007/07/03/15/con | 3 Jul 2007, consolidated text (latest amendment in force from 29 Dec 2023) | BOE, as above | 31,711 |
| LEY19-2003 | Ley 19/2003, movimientos de capitales y transacciones económicas con el exterior | https://www.boe.es/eli/es/l/2003/07/04/19/con | 4 Jul 2003, consolidated text (latest amendment in force from 28 Dec 2022) | BOE, as above | 9,084 |
| RD571-2023 | Real Decreto 571/2023, sobre inversiones exteriores | https://www.boe.es/eli/es/rd/2023/07/04/571/con | 4 Jul 2023, consolidated text (in force from 1 Sep 2023) | BOE, as above | 13,528 |
| **Total** | **5 documents** | | | | **80,843** |

`main.py index` downloads every document itself (BOE open data API as XML, the CNMV file as PDF), so nothing is placed by hand. The texts are legislation and supervisor guidance, with no personal data.

**Why these documents.** The Royal Decree is the OPA rulebook. The CNMV Q&A gives the supervisor's criteria where the decree is open (financing as a condition, dividends during the offer, purchases by third parties). Ley 15/2007 is there because most large OPAs need merger control and a second phase investigation is the main timing risk. Ley 19/2003 and RD 571/2023 cover foreign investment screening, now a common condition when the bidder is from outside the EU.

**What I left out.** The UK Takeover Code (its terms do not allow use in retrieval or AI systems) and Directive 2004/25/EC (EUR-Lex blocks scripted downloads, so it would break the "no manual steps" rule, and the Royal Decree already transposes it).

## Ingestion

**Extraction.**
- *BOE XML (4 documents).* Each article is a `bloque` with several historical versions. I keep only the latest version, drop footnotes and amendment notes, turn tables into one line per row, and keep the article title as the location (`Artículo 23`, `Artículo 7 bis`, `Disposición adicional primera`, `Preámbulo`) and the chapter as the section.
- *CNMV PDF (pypdf).* I remove the running header and footer of every page, join lines broken mid sentence, split the text into the introduction and one block per numbered question (`Pregunta 1` to `Pregunta 14`), and repair words that the PDF splits in two.

**One extraction problem I fixed.** My first parser started a new CNMV question at every "¿". Questions 11 to 13 do not start with "¿" (for example "12. Tras la presentación de una opa, ¿es posible..."), so they were swallowed by question 10 and could not be cited. Now a question starts at a line opening with the next number in sequence ("11.", "12.") that has a "?" within the next 16 lines. Requiring the numbers in order stops numbered lists inside answers from being read as new questions. A second problem was words split by the PDF's spacing ("art ículo", "so ciedad"). Two tokens are joined when the joined word appears unsplit elsewhere in the document. A few splits survive ("finalizad o", "e xigencias"), which does not hurt retrieval much because the embedding still sees the rest of the passage.

**Chunking (chosen design, `struct`).** One chunk per article or CNMV question. Articles above 350 words are split on paragraph boundaries and every part repeats the article heading. Each chunk starts with a header naming the document and chapter (`RD 1066/2007 (OPAs) · CAPÍTULO V Anuncio, presentación y autorización de la oferta`) so it makes sense on its own.

**Chunk metadata.** `doc_id`, `doc_title`, `url`, `location` (the citation, e.g. `Artículo 23`), `section` (chapter), `page` (PDF only), `part` (e.g. `2/3` when an article is split), `design`, `order`, `words`. Chunk ids are a hash of the content, so an unchanged chunk keeps its id and its saved vector across runs.

**Number of chunks.** `struct`: 368 (98 + 19 + 148 + 40 + 63 by document). `fixed`: 507. Plus 1 chunk from the document added in the demo.

**Embedding and store.** `gemini-embedding-2` at 768 dimensions, with the document task type for chunks and the query task type for questions, vectors normalised. ChromaDB with cosine distance in `index/chroma` (16 MB, committed). `main.py index` only embeds chunks without a saved vector, and query vectors are cached in `index/query_cache.json`, which kept the whole project inside the free tier of about 1,000 embeddings a day.

## Test set

I wrote the 35 questions in `eval/questions.csv` myself, in the words an analyst on the desk would use, before tuning anything. For each one I named the document and article that answers it.

| Kind | Count |
|---|---|
| single (one passage) | 24 |
| multi (two passages) | 6 |
| unanswerable | 5 |
| **Total** | **35** |

The unanswerable questions sit right next to the corpus: the UK "put up or shut up" deadline, the actual acceptance level in BBVA's bid for Sabadell, the European Commission's merger control phases, today's spread on a live deal, and short position disclosure thresholds.

Examples:
- **single, q09.** "¿Cuál es el plazo mínimo y máximo durante el que los accionistas pueden aceptar una OPA?" Expected `RD1066-2007, Artículo 23`. Reference: between 15 and 70 natural days, counted from the trading day after the first announcement.
- **multi, q26.** "Si una OPA ha sido autorizada por la CNMV pero todavía no por la CNMC, ¿puede el comprador adquirir las acciones y ejercer sus derechos de voto?" Expected `RD1066-2007, Artículo 26` and `LDC-15-2007, Artículo 9`. Reference: the bidder can run the offer and buy, but cannot vote the shares until the competition decision. It has to notify competition within five days of asking the CNMV to authorise the offer, and if it made the offer conditional it can withdraw when there is no decision before the end of the acceptance period.

## Retrieval

Hit rate on the 30 answerable questions, using the question text as the query. A hit at k means an expected passage is in the top k. For multi questions the last column requires both passages in the top 5.

| Design | Search | Hit@1 | Hit@3 | Hit@5 | Multi, both @5 | Words added to the prompt (top 5) |
|---|---|---|---|---|---|---|
| fixed (200 words, 40 overlap) | dense | 60% | 70% | 83% | 50% | 991 |
| fixed | hybrid (BM25 + dense, RRF) | 37% | 73% | 77% | 33% | 978 |
| **struct (one article or question)** | **dense** | **60%** | **80%** | **90%** | 33% | 1,203 |
| struct | hybrid | 43% | 70% | 73% | 50% | 1,322 |

![Hit rate by design](eval/retrieval.png)

**Design chosen: `struct` with dense search.** It has the best hit@3 and hit@5 (24 and 27 of 30 questions against 21 and 25 for `fixed`), and a struct chunk is exactly one article, so its citation is an article the analyst can open and the code can check. A `fixed` window cites ranges like `Artículo 2 a Artículo 3`. The price is about 20% more words in the prompt (1,203 against 991), which is small next to the cost of a wrong deadline. With 30 questions one question is 3.3 points, so the gap between the two dense designs is two or three questions and I do not read more into it than that. `fixed` does better on getting both passages of a multi question (3 of 6 against 2 of 6), which matches where the system fails later.

**Hybrid search hurts both designs**, mostly at hit@1 (60% to 37% and 43%). The questions share generic words ("OPA", "CNMV", "plazo", "oferta") with many chunks, and BM25 rewards the long CNMV answers that repeat them.

**What the numbers do not show.**
- The agent does not search with the question text. It rewrites the query in legal terms and can search up to four times, so end to end retrieval is better than this table. For q26 the question text finds neither passage, but the agent's searches retrieved both.
- One CNMV chunk, `Pregunta 12` (purchases by third parties during an offer, a long answer about competing bids), appears in the top 5 for 18 of the 30 questions and takes a slot from the right passage.
- q22 counts as a miss because I expected `LDC-15-2007, Artículo 9`, but `RD1066-2007, Artículo 26`, which was retrieved, states the same rule for OPAs and the agent answered correctly. The expected location was narrower than it needed to be.

## Tools and subagent

**MCP server (`server.py`).** Two tools, served over stdio. The server loads the committed index and never re-embeds the corpus.

- `search(query)`: "Search Spanish takeover-bid (OPA) rules used by a merger arbitrage desk." The description lists the five documents, tells the model to query in Spanish with the legal terms (plazo de aceptación, venta forzosa, precio equitativo, segunda fase), to use it before answering any question about conditions, prices, deadlines, squeeze-out, competing offers, merger control or foreign investment, and to search again with different wording if the first results do not answer. It returns the top 5 passages, best first, each starting with the exact citation to use.
- `add_document(path)`: "Add one document to the corpus so that search can find it." It runs the file (.pdf, .html, BOE .xml, .txt or .md) through `index.py`'s own pipeline (imported, not rewritten), embeds and stores the chunks, says what happens when the document is already indexed, returns the id to cite, and says to use it only when the user explicitly asks.

**One search result** (q07, the agent's query `plazo CNMV autorizacion OPA plazo maximo resolver`, third of five results, text trimmed):

```
--- Result 3 | cite as [RD1066-2007, Artículo 21] | score 0.782
Source: Real Decreto 1066/2007, régimen de las ofertas públicas de adquisición de valores · CAPÍTULO V Anuncio, presentación y autorización de la oferta
RD 1066/2007 (OPAs) · CAPÍTULO V Anuncio, presentación y autorización de la oferta
Artículo 21. Autorización de la oferta.
1. La Comisión Nacional del Mercado de Valores examinará el folleto presentado y la documentación complementaria y autorizará o denegará la oferta. [...]
3. El acuerdo de autorización o denegación deberá adoptarse en un plazo de veinte días hábiles a partir de la recepción de la solicitud. [...]
```

The first two results were CNMV questions 11 and 12, which mention plazos but not this one. This is the hub chunk problem from the retrieval section.

**Subagent (`.claude/agents/corpus-researcher.md`).** Its only tool is `mcp__corpus__search`. Its description tells the editor to delegate any question about OPA conditions, acceptance periods, equitable price, competing offers, squeeze-out, CNMV criteria, merger control phases or foreign investment authorisation. Its instructions: search only with `search`, in Spanish, at most four times. Answer only from the returned passages, never from its own knowledge of Spanish law or past deals. Cite every claim as `[DOC, location]` and never invent a citation. Quote numbers exactly with their conditions. Start with "El corpus no cubre esta pregunta" when the passages do not answer. Reply in Spanish in about 150 words.

**Transcript from Claude Code** (Claude Code in GitHub Codespaces, with the `corpus` server from `.mcp.json`. Full export in `eval/subagent_transcript.md`):

```
❯ Usa el subagente corpus-researcher para responder: ¿Cuánto tiempo tiene la
  CNMV para autorizar una OPA?

● corpus-researcher(CNMV OPA authorization deadline)
  ⎿  Backgrounded agent (↓ to manage · ctrl+o to expand)

● He lanzado el subagente corpus-researcher con tu pregunta y todavía está
  buscando en el corpus. Cuando termine te paso el plazo con sus citas o, si el
  corpus no lo recoge, te lo digo.

✻ Brewed for 7s · done 6:06 PM

› Message from corpus-researcher
  **Respuesta corta:** la CNMV tiene **20 días hábiles** para autorizar o
  denegar la OPA. El plazo cuenta desde que recibe la solicitud de autorización.

  **Detalle:**
  - **Plazo:** el acuerdo de autorización o denegación debe adoptarse "en un
  plazo de veinte días hábiles a partir de la recepción de la solicitud"
  [RD1066-2007, Artículo 21].
  - **Cuándo vuelve a empezar el plazo:** si los documentos complementarios
  llegan después de la solicitud, o si la CNMV pide información o documentos
  adicionales, el plazo se computa desde la fecha en que se registran esos
  documentos o esa información [RD1066-2007, Artículo 21]. La CNMV puede pedir
  al oferente esa información adicional [RD1066-2007, Artículo 21].
  - **Admisión a trámite (paso previo):** la CNMV tiene "siete días hábiles"
  desde que se completa la documentación para admitir la solicitud a trámite. Si
  no se pronuncia en ese plazo, la solicitud se entiende admitida [RD1066-2007,
  Artículo 17].
  - **Otras autorizaciones administrativas previas:** la CNMV no autorizará la
  oferta hasta que se le acredite la autorización, no oposición o notificación
  que exija otro organismo. La excepción es que hayan transcurrido los plazos
  para entender esa autorización concedida por silencio administrativo
  [RD1066-2007, Artículo 26]. La CNMV aplica este requisito de forma
  restrictiva: se refiere a autorizaciones "requeridas por la oferta" y de
  organismos supervisores [CNMV-QA-OPAS, Pregunta 3].
  - **Ofertas simultáneas en España y en un mercado de fuera de la UE:** la CNMV
  puede adaptar los plazos [RD1066-2007, Artículo 21].
  - **Si la CNMV no resuelve en 20 días:** **el corpus no cubre esta pregunta.**
  Ningún pasaje recuperado dice qué efecto tiene el silencio sobre la
  autorización de la OPA. El silencio positivo del Artículo 17 vale solo para la
  admisión a trámite. El del [LDC-15-2007, Artículo 38] se refiere al control
  de concentraciones de la CNMC, no a la CNMV.

  **Un punto a vigilar:** la ley no dice que los 20 días se cuenten desde la
  admisión a trámite, sino desde "la recepción de la solicitud" [RD1066-2007,
  Artículo 21]. Los pasajes no explican cómo encaja esto con el plazo de
  admisión de 7 días [RD1066-2007, Artículo 17].

  **Citas usadas:**
  - [RD1066-2007, Artículo 21]
  - [RD1066-2007, Artículo 17]
  - [RD1066-2007, Artículo 26]
  - [CNMV-QA-OPAS, Pregunta 3]
  - [LDC-15-2007, Artículo 38]

  Hice tres búsquedas.

● La CNMV tiene 20 días hábiles para autorizar o denegar la OPA, contados desde
  que recibe la solicitud [RD1066-2007, Artículo 21].

  Detalle:
  - El plazo puede volver a empezar. Si los documentos complementarios llegan
    después de la solicitud, o si la CNMV pide información adicional, los 20
    días se cuentan desde que esa documentación queda registrada [RD1066-2007,
    Artículo 21].
  - Antes hay un paso de admisión a trámite. La CNMV tiene 7 días hábiles desde
    que la documentación está completa para admitir la solicitud. Si no dice
    nada en ese plazo, la solicitud queda admitida [RD1066-2007, Artículo 17].
  - Otras autorizaciones pueden retrasarla. La CNMV no autoriza la oferta hasta
    que se le acredite la autorización, no oposición o notificación que exija
    otro organismo. La excepción es que haya vencido el plazo para darla por
    concedida por silencio [RD1066-2007, Artículo 26]. La CNMV aplica esto solo
    a las autorizaciones "requeridas por la oferta" y de organismos supervisores
    [CNMV-QA-OPAS, Pregunta 3].
  - Ofertas simultáneas fuera de la UE: si la oferta también se lanza en un
    mercado de fuera de la UE, la CNMV puede adaptar los plazos [RD1066-2007,
    Artículo 21].

  Lo que no está claro:
  - Si la CNMV no resuelve en 20 días: el corpus no cubre esta pregunta. Ningún
    pasaje dice qué efecto tiene ese silencio sobre la autorización. El silencio
    positivo del Artículo 17 vale solo para la admisión a trámite.
  - Cómo encajan los dos plazos: los 20 días se cuentan desde "la recepción de
    la solicitud" [RD1066-2007, Artículo 21], no desde la admisión. Los pasajes
    no explican cómo se combina esto con los 7 días de admisión [RD1066-2007,
    Artículo 17]. Confírmalo con el asesor de la operación.

✻ Baked for 7s · done 6:06 PM

● Agent "CNMV OPA authorization deadline" finished · 24s
```

The subagent searched three times and gave the same core answer as my harness on q07 (20 business days from receipt of the application, [RD1066-2007, Artículo 21]), with more context: the 7 business day admission step (Artículo 17) and the other authorisations that can hold the CNMV back (Artículo 26 and CNMV Pregunta 3). It also did what rule 5 asks for the part it could not answer: it said the corpus does not say what happens if the CNMV misses the 20 days, instead of guessing. That same phrase inside a full answer is what my refusal check miscounts in q27 (see Failures).

## Adding a document

**When the document is already indexed** (`index.add_document`):
- the same file (same SHA-256) is skipped and nothing is embedded. The tool says it is already indexed and under which id.
- a file with the same name but different content is treated as a new version. Its old chunks are deleted and the new ones embedded, so the corpus never holds two versions of the same document.
- chunk ids are content hashes, so even when a new version is added, chunks whose text did not change keep their saved vectors.

**Demo** (`eval/add_document_demo.md`, run with `evaluate.py --demo-add`).

- **Unanswerable question, q32:** "¿Qué porcentaje de aceptación obtuvo finalmente BBVA en su OPA sobre Banco Sabadell?"
- **Before:** "El corpus no cubre esta pregunta. [...] no contiene datos sobre operaciones concretas como la OPA de BBVA sobre Banco Sabadell."
- **Document added:** the CNMV's notice of the result of the offer, 16 Oct 2025 (`docs/cnmv_resultado_opa_bbva_sabadell.pdf`, from cnmv.es). The agent called `add_document`, the harness stopped for my approval, I approved, and the tool reported 1 chunk, 1 embedded, id `CNMV-RESULTADO-OPA-BBVA-SABADELL`.
- **After:** "La OPA fue aceptada por 1.272.671.801 acciones, que representan un 25,33% [...] del capital social de Banco Sabadell, y un 25,47% de sus derechos de voto [...] la oferta quedó sin efecto [CNMV-RESULTADO-OPA-BBVA-SABADELL, Página 1]."

Since the demo the live index holds six documents, so q32 is now answerable. The agent answers and judge verdicts below were produced before the document was added. The final `check.py --evaluate` run re-ran retrieval with the new chunk in the index, and the only number that moved was the words added by struct hybrid search (1,314 to 1,322).

## Harness and guardrails

`agent.py` uses LangChain's `create_agent` with `gemini-3.5-flash-lite`. It opens one MCP session to `server.py` and wraps its two tools, so the harness uses exactly the same tools as the editor. `AGENTS.md` is the system prompt.

**AGENTS.md rules** (each one has its reason in the file):
1. Answer only from what `search` returned in this conversation, never from own knowledge.
2. Search before answering, in Spanish, with the legal terms, and again with other wording if needed, at most four searches.
3. Cite every claim right after it as `[RD1066-2007, Artículo 23]`, only passages that were retrieved.
4. Quote numbers exactly, say whether days are natural or business days, and give the condition attached.
5. When the passages do not answer, start with "El corpus no cubre esta pregunta" and say what is missing. Same for live deals, predictions, prices and other jurisdictions.
6. When two passages seem to conflict (a CNMV criterion and the decree), say so and cite both.
7. Answer in Spanish, answer first, about 150 words.
8. Never call `add_document` unless the user asks to add a file.

**Approval step.** `HumanInTheLoopMiddleware` interrupts every `add_document` call before it runs and shows the path. The user approves or rejects in the terminal. In a non interactive run (evaluation, `check.py`) the call is rejected automatically, so the evaluation can never change the corpus. The demo above shows one approval.

**Call limits.** At most 6 tool calls and 10 model calls per question, so a confused agent cannot loop and spend the quota.

**Extra guardrail: citation guard.** After the agent answers, code parses every `[DOC, location]` in the answer and checks it against the passages `search` actually returned in that run. A more specific citation is accepted (`Artículo 23.2` for a retrieved `Artículo 23`). If any citation was not retrieved, or a substantive answer has no citation at all, the answer is replaced with a refusal that tells the analyst to check the rule directly. I chose to block rather than only flag, because on this desk an invented citation is worse than no answer.

**Where it fired.** In the first full run it fired on q24 and q30. Both were false positives: the model wrote compound citations, `[RD571-2023, Preámbulo; Artículo 14]` and `[LEY19-2003, Artículo 7 bis; RD571-2023, Artículo 15]`, and my parser read each as a single location that did not exist. Two correct answers were replaced by refusals. I fixed the parser to split compound citations and re-applied the guard to the stored raw answers, and it no longer fires on any of the 35 answers. To show it catching a real problem, `eval/guard_demo.py` takes the stored q07 answer and its trace and runs the same guard on three versions (output in `eval/guard_demo.md`):

| Version of the q07 answer | Guard |
|---|---|
| The real answer, citing `[RD1066-2007, Artículo 21]` (retrieved) | passes |
| One citation changed to `[RD1066-2007, Artículo 22]` (a real article that was not retrieved) | **fires**, answer replaced by a refusal |
| Citations removed | **fires** ("no incluye ninguna cita") |

**Gap found.** The guard skips answers that contain the refusal phrase. In q27 the model wrote "El corpus no cubre esta pregunta detalladamente, pero..." and then answered, so the answer was neither checked by the guard nor counted as an answer (see Failures).

## Evaluation

`main.py evaluate` runs the agent on all 35 questions (answers cached in `eval/answers.jsonl`), checks in code what code can check, sends the rest to an LLM judge, and compares the judge with my grades.

**Code checks** (no model involved):
- **Refusal:** the answer contains "El corpus no cubre esta pregunta". Refusals on unanswerable questions are graded correct in code, refusals on answerable ones are wrong refusals.
- **Citations:** the answer has at least one citation, every citation matches a retrieved passage, and whether the guard fired.
- **Expected source:** whether the expected document and article were retrieved and whether they were cited.
- **Errors:** API errors and empty answers are marked and re-asked, never graded.

**Judge.** `gemini-3.5-flash-lite` with the rubric in `eval/judge_rubric.md`. It gets the question, my reference answer, the retrieved passages and the answer, and returns two 0/1 grades with a one sentence reason:
- **correct:** same facts as the reference (numbers, conditions, deadlines, authority). 0 if any of them differs, if a key condition from the reference is missing, or if the answer hedges. Strict on natural versus business days.
- **supported:** every factual claim is in the retrieved passages, even if the claim is true in real life.

I wanted `gemini-3.8-flash` as the judge, a different and stronger model than the agent, but it and `gemini-3.5-flash` returned 503 (overloaded) errors on the free tier for the whole run, so the judge is the same model as the agent. Verdicts are cached in `eval/judge_cache.json`.

**My grades and agreement.** I graded 23 answers in `eval/human_labels.csv` (q01 to q12, q25 to q35) before reading the judge's verdicts.

| | Agreement with the judge | Cohen's kappa |
|---|---|---|
| correct | 16 of 23 (70%) | -0.08 |
| supported | 23 of 23 (100%) | not defined: both of us gave 1 to every answer |

All 7 disagreements on correctness go the same way. In six (q01, q08, q25, q26, q29, q30) I marked the answer wrong because it left out a condition or deadline in the reference, and the judge accepted it. In q27 the code counted a refusal and I counted a correct answer. The judge never gave a 0 for correctness, so its 70% agreement is no better than chance (kappa below zero). It checks that what the answer says is right and supported, but not that nothing important is missing, and an incomplete answer is exactly the failure that misprices a trade. I trust my grades over the judge.

**Results.**

| Outcome | Judge and code, 35 questions | My grades, 23 questions |
|---|---|---|
| Correct and supported | 29 of 30 answerable | 12 of 18 answerable |
| Correct but unsupported | 0 | 0 |
| Wrong answer | 0 | 6 |
| Correct refusals | 5 of 5 | 5 of 5 |
| Wrong refusals | 1 (q27) | 0 (I count q27 as correct) |
| Answered an unanswerable question | 0 | 0 |

Other code checks over all 35: invalid citations 0, guard fired 0 (after the parser fix), errors 0. Every answer that made a claim cited it.

By my grades, single questions are 10 of 12 correct and multi questions 2 of 6. The system never made up a rule and never answered an unanswerable question. What it does wrong is leave things out.

## Failures

Every failed answer from my 23 grades, classified by cause (`eval/failures.csv`):

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 2 | q25, q30 |
| Wrong answer from the right passage | 4 | q01, q08, q26, q29 |
| Unsupported claim | 0 | |
| Wrong refusal | 1 | q27 |
| Bad test question | 0 | |

- **q01** (single). Retrieved Artículo 4 but left out the second way to acquire control: below 30% when the bidder appoints more than half the board within 24 months.
- **q08** (single). Retrieved Artículo 26 but presented an optional condition (making the offer conditional on competition clearance) as mandatory and left out the bidder's right to withdraw.
- **q25** (multi). The agent searched once, only for the CNMC second phase, so it never retrieved the acceptance period (RD Artículo 23) needed for the full timeline.
- **q26** (multi). Retrieved both passages but left out the five day notification deadline and the right to withdraw.
- **q27** (multi). Opened with "El corpus no cubre esta pregunta detalladamente" and then gave the correct answer. A partial refusal that the code counts as a refusal.
- **q29** (multi). Retrieved both passages but left out the rule that the equitable price is the highest price paid in the previous 12 months.
- **q30** (multi). Did not retrieve RD 571/2023 Artículo 11, so it left out the six month deadline to execute an authorised investment and its extension.

Six of the seven failures are omissions and none are invented facts. Five of the six multi questions failed, against two of twelve single questions. The 12 single questions I did not grade (q13 to q24) only have the judge's verdict, which as shown above misses omissions, so there may be more failures there.

**What to fix first.**
1. **Completeness, 4 failures.** Add a rule to `AGENTS.md`: give every condition, exception and deadline in the retrieved passage that bears on the question, as a list when there are several. Answers average 231 output tokens, so there is room. At the same time, make the judge list the facts in the reference one by one and mark each found or missing before its verdict, so the evaluation can see the problem.
2. **Multi questions, 2 retrieval misses.** Tell the agent to split a question with two parts into one search per part (q25 only searched for one half). Reduce the weight of the hub chunk `Pregunta 12`, for example by splitting it or filtering by document when the question names a law.
3. **Refusal detection, 1 failure.** Count a refusal only when the answer starts with the phrase, and tell the agent not to use the phrase when it then answers. This also closes the gap where such an answer skips the citation guard.

## Decision

**Would I let users rely on it?** Not as the only source for a trading decision. I would let the analysts on the desk use it as a first look up tool with citations, for single rule questions: a deadline, a threshold, a condition in one article. On those it was right 10 times out of 12 in my grades, every claim it made was in the passage it cited, and it refused all five questions outside the corpus. It is not ready for questions that combine several rules, like building the full timeline of a deal with CNMC and foreign investment clearance, where it got 2 of 6.

**With which safeguard.** The citation guard stays on in blocking mode, and the analyst opens the cited article before the answer goes into a position or a model. Anything about a live deal goes to the offer prospectus and to deal counsel. I would review the decision after the three fixes above, with a judge that checks completeness and my grades on all 30 answerable questions.

**Cost and latency per question** (35 questions, free tier):

| | Per question |
|---|---|
| Tokens | 6,848 on average (6,617 input, 231 output) |
| Seconds | 21.5 mean, 6.8 median, 95.5 max (the slow ones were retries after 503 errors) |
| Search calls | 1.4 (one search in 24 questions, two in 5, three in 5, none in 1) |
| Model calls | 2.4 |

Almost all the tokens are the five retrieved passages, so cost is driven by the chunk size chosen above. The median of 6.8 seconds is fine for an analyst between trades. The mean is pulled up by retries when the free tier was overloaded.

## AI use

I used Claude (Anthropic) as an assistant throughout the project:

1. **Code.** Claude helped me write the code and build the base of every part of the project (ingestion, search, MCP server, agent and evaluation), especially the functions and libraries that were new to me. It also drafted `AGENTS.md`, the subagent file, the judge rubric and the reference answers, from my use case and the articles I chose for each question.
2. **Report.** Claude helped me structure this report so that it matches the grading rubric, drafted the text from my decisions, grades and failure classification, and corrected the grammar.
3. **Infrastructure.** Claude helped me set up and run everything in the terminal and in GitHub Codespaces (dependencies, API key setup, Git and the evaluation runs).
