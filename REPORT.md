# Assignment 3 Report

- **Name**: Mariano Delpree
- **Student ID**: 19970
- **Group**: BBADBA 5B

## Use case

**Who asks:** Landlords who rent out a flat in Barcelona, and tenants who rent one. They need to know what the law says about their situation: lease duration, deposits, rent updates and limits in stressed areas, ending a contract, seasonal lets or tourist-use flats. The rules depend on the type of contract and the area, and they are spread over three laws I injested into the rag system(state LAU, Catalan Llei 18/2007 and Decret-llei 3/2023).

**What they do with the answer:** They can decide how to rent: which contract type, how long, what rent and deposit to ask for, how much notice to give. A tenant checks what they are required to do and what the landlord can or cannot demand.

**Cost of a wrong answer compared with "I don't know":** If wrong answer is acted on it can mean an unenforceable contract clause, a lease that becomes a standard 5-year housing lease when it was meant to be seasonal, a rent above the legal limit that must be refunded, or a fine for letting a tourist flat without a licence. "I don't know" only costs time: the user looks up the article or asks a lawyer. So the system must cite every claim and refuse when the documents do not cover the question.

## Corpus

Three official texts on renting in Barcelona, in Spanish, downloaded from the BOE on 18/11/2026.

| Document | URL | Date (consolidated to) | Licence | Words |
|---|---|---|---|---|
| Ley 29/1994, de Arrendamientos Urbanos (LAU) | https://www.boe.es/buscar/pdf/1994/BOE-A-1994-26003-consolidado.pdf | 13/11/2026 | BOE reuse conditions (Ley 37/2007) | ~29,500 |
| Ley catalana 18/2007, del derecho a la vivienda | https://www.boe.es/buscar/pdf/2008/BOE-A-2008-3657-consolidado.pdf | 25/03/2026 | BOE reuse conditions (Ley 37/2007) | ~55,700 |
| Decreto-ley catalán 3/2023, viviendas de uso turístico | https://www.boe.es/buscar/pdf/2024/BOE-A-2024-281-consolidado.pdf | 08/11/2023 (no modifications since) | BOE reuse conditions (Ley 37/2007) | ~5,400 |

Total: ~90,600 words, 145 pages.

Word counts come from `pdftotext` and include page headers, footers and the index. 
Fuente de los datos: Agencia Estatal Boletín Oficial del Estado (https://www.boe.es).

## Ingestion

**Extract, clean, chunk** (`index.py`):
1. Read each BOE PDF page by page with `pypdf` and apply Unicode normalisation (e.g. the ligature "ﬁ" becomes "fi").
2. Remove the repeated page header and footer ("BOLETÍN OFICIAL DEL ESTADO / LEGISLACIÓN CONSOLIDADA / Página N") and the "no legal value" disclaimer.
3. Skip the cover and table of contents, so the text starts at "TEXTO CONSOLIDADO".
4. Rebuild paragraphs from wrapped lines (in these PDFs a line that continues ends with a space).
5. Follow the legal headings (Título › Capítulo › Sección › Artículo / Disposición, plus the preamble and annex) and make **one chunk per article**. Articles over 300 words are split between numbered apartados, never mid-sentence.
6. Start each chunk with a short header naming the law, its Título/Capítulo and the article.
7. Embed the chunks with Gemini (`gemini-embedding-2`) and store them in ChromaDB (`index/chroma`) in batches of 20, saving each batch straight away. Chunk ids are a hash of the text, so re-running only embeds new or changed chunks.

**Extraction problems fixed:**
- Long Sección titles in Llei 18/2007 run onto a second line, and the parser only kept the first line, so the rest of the title ended up inside the article text. I fixed it by joining the wrapped line back onto the title.
- The LAU PDF I had downloaded was corrupted (saved as text, so it couldn't be opened). I replaced it with a clean copy from boe.es.

**Chunk metadata:** source file, law short name, article and its heading, apartados covered, Título / Capítulo / Sección, first and last page, and a ready-made citation (e.g. `LAU, Artículo 36, apartados 1–5, p. 25`).

**Number of chunks:** 440 (LAU 129, Llei 18/2007 289, Decret-llei 3/2023 22), averaging 218 words.

## Test set

36 questions in `eval/questions.csv`, written in Spanish from the three corpus documents before any tuning. Each question was drafted from a specific article, and its reference answer was checked against the official BOE text. `multi` questions need two passages, sometimes from different laws. `unanswerable` questions stay on topic (rent indices, okupas, tourist flats) but ask for facts the documents don't contain.

| Kind | Count |
|---|---|
| `single` | 24 |
| `multi` | 6 |
| `unanswerable` | 6 |
| **Total** | **36** |

**Example (`multi`, q27):**
"Un propietario de Barcelona quiere alquilar su piso a turistas por estancias de 10 noches. ¿Se aplica la LAU? ¿Qué permiso necesita?"
Expected: the LAU does not apply (art. 5.e excludes tourist lets of 31 days or less), and Barcelona requires a prior urban-planning licence (Decreto-ley 3/2023, art. 1.1 and Annex).

**Example (`unanswerable`, q32):**
"¿Cuál es la pena por ocupar un piso vacío (usurpación)?"
Expected: the assistant says the documents don't cover it (the penalty is in the Código Penal, art. 245) instead of answering from memory.

## Retrieval

**Designs compared:** two chunkings × three search methods (`retrieve.py`, `evaluate.py`).
- **Chunkings.** *structure*: one chunk per article, as above. *fixed*: plain 300-word windows with 50 words of overlap that ignore the legal structure (326 chunks).
- **Search methods.** *dense*: Gemini embedding similarity. *bm25*: keyword matching. *hybrid*: both rankings merged with reciprocal rank fusion.

A hit means the expected article from the expected document is in the top k. A `multi` question counts only if every expected passage is there. Results are over the 30 answerable questions. "Words added" is the average number of words the top-k chunks add to the prompt.

| Design | hit@1 | hit@3 | hit@5 | words added (k=1 / 3 / 5) |
|---|---|---|---|---|
| structure + dense | **0.70** | 0.93 | **0.97** | 247 / 719 / 1,185 |
| structure + bm25 | 0.60 | 0.83 | 0.90 | 255 / 733 / 1,226 |
| **structure + hybrid** | 0.67 | **0.97** | **0.97** | 249 / 726 / **1,179** |
| fixed + dense | 0.53 | 0.83 | 0.87 | 300 / 899 / 1,499 |
| fixed + bm25 | 0.57 | 0.80 | 0.87 | 300 / 900 / 1,500 |
| fixed + hybrid | 0.60 | 0.93 | 0.97 | 300 / 900 / 1,500 |

**Chosen design: structure + hybrid, k = 3.**
- Structure chunking matches or beats fixed windows with every search method, while adding about 20% fewer words to the prompt.
- Hybrid has the best hit@3 and ties dense at k=5. Dense is better at hit@1 by a single question.
- k = 3 leaves room for both passages of two-passage questions but wont bloat the agent with unnecessary context.

Per-question results are in `eval/retrieval_per_question.csv`.

## Tools and subagent

**Tools** (`server.py`, over MCP):
- `search(query)`: searches the LAU, Llei 18/2007 and Decret-llei 3/2023 (structure chunking + hybrid search) and returns the top 3 passages, each headed by its citation.
- `add_document(path)`: copies a PDF into `documents/`, chunks it with `index.py`, embeds only the new chunks and stores them.

**One search result** (`search("¿Cuánto es la fianza?")`, first passage):
```
[1] LAU, Artículo 36, apartados 1–5, p. 25 (source: BOE-A-1994-26003-consolidado.pdf)
[LAU — Ley 29/1994, de 24 de noviembre, de Arrendamientos Urbanos]
TÍTULO IV. Disposiciones comunes
Artículo 36. Fianza (apartados 1–5)
1. A la celebración del contrato será obligatoria la exigencia y prestación de fianza en metálico en cantidad equivalente a una mensualidad de renta en el arrendamiento de viviendas…
```

**Subagent** (`.claude/agents/corpus-researcher.md`): it can only use `search`. It searches in Spanish with legal terms (up to 3 times), answers only from the passages, cites every claim, and replies "The corpus does not cover this" when nothing fits.

**Transcript** (Claude Code, main agent delegating to `corpus-researcher`):

> **User:** use the corpus researcher subagent to answer "cual es el periodo que el arrendador tiene para devolver la fianza"
>
> **Main agent → Agent(corpus-researcher):** Answer in Spanish, from the indexed corpus only, with citations: "¿Cuál es el periodo que el arrendador tiene para devolver la fianza?" Search with legal terms … check both LAU (Artículo 36) and Llei 18/2007 if relevant. Quote the exact period and any consequence of late return. If something is not covered, say so.
>
> **Subagent tool calls** (2 × `mcp__corpus__search`, ~16 s, ~9.7k tokens):
> 1. `search("devolución fianza plazo un mes entrega de llaves interés legal")`
> 2. `search("fianza restitución arrendatario Llei 18/2007 dipòsit fiança")`
>
> **Subagent report:**
>
> La LAU no fija un plazo exacto para que el arrendador devuelva la fianza. Lo que sí establece es que, si no la devuelve en un mes, empieza a deber intereses. En concreto, "el saldo de la fianza en metálico que deba ser restituido al arrendatario al final del arriendo, devengará el interés legal, transcurrido un mes desde la entrega de las llaves por el mismo sin que se hubiere hecho efectiva dicha restitución" (LAU, Artículo 36, apartados 1–5, p. 25). Dicho de forma práctica: el arrendador tiene **un mes desde la entrega de las llaves**. Si se pasa de ese mes, la cantidad pendiente genera **el interés legal**.
>
> Relacionado con esto:
> - Al terminar el contrato, las partes deben dejar por escrito el estado de la vivienda en un "documento de finalización del arrendamiento" firmado por las dos. Si no se firma, o si no recoge ningún desperfecto, "se presumirá, salvo prueba en contrario, que la vivienda fue entregada en estado adecuado de conservación" (LAU, Artículo 36, apartados 5–7, p. 25). Esto importa si el arrendador quiere descontar daños de la fianza.
> - En Cataluña la fianza "se debe depositar en el Registro de fianzas de los contratos de alquiler de fincas urbanas", de acuerdo con la Ley 13/1996 (Llei 18/2007, Artículo 66, apartados 3–4, p. 48). La LAU prevé que, cuando la fianza está depositada ante la Administración autonómica y esta no la devuelve en un mes desde que termina el contrato, la cantidad depositada "devengará el interés legal correspondiente" (LAU, Disposición adicional tercera, apartados 1–2, pp. 30–31). Ojo: esta regla trata de lo que la Administración devuelve al arrendador, no de lo que el arrendador devuelve al inquilino.
>
> **Lo que el corpus no cubre:** la Llei 18/2007 no indica ningún plazo propio para devolver la fianza al inquilino. Tampoco aparece cómo se recupera la fianza del Registro de fianzas catalán, ni otras consecuencias del retraso aparte del interés legal (por ejemplo, sanciones). Eso estaría en la Ley 13/1996 del Registro y depósito de fianzas, que no forma parte del corpus.
>
> **Main agent → User:**
>
> **Respuesta:** la LAU no fija un plazo cerrado para devolver la fianza. Lo que sí dice es que, **pasado un mes desde que el inquilino entrega las llaves**, el saldo que no se haya devuelto empieza a generar **el interés legal**: "devengará el interés legal, transcurrido un mes desde la entrega de las llaves por el mismo sin que se hubiere hecho efectiva dicha restitución" (LAU, Artículo 36, apartados 1–5, p. 25). En la práctica, tienes un mes.
>
> **Si quieres descontar desperfectos:**
> - Al terminar el contrato, ambas partes deben firmar un "documento de finalización del arrendamiento" que recoja el estado de la vivienda.
> - Si no se firma, o si no menciona ningún desperfecto, "se presumirá, salvo prueba en contrario, que la vivienda fue entregada en estado adecuado de conservación" (LAU, Artículo 36, apartados 5–7, p. 25).
>
> **En Cataluña:**
> - La fianza debe depositarse en el Registro de fianzas, según la Ley 13/1996 (Llei 18/2007, Artículo 66, apartados 3–4, p. 48).
> - Si la Administración tarda más de un mes en devolverte el depósito, también genera interés legal (LAU, Disposición adicional tercera, apartados 1–2, pp. 30–31). Esta regla trata de lo que la Administración te devuelve a ti, no de lo que tú devuelves al inquilino.
>
> **Lo que el corpus no cubre:** la Llei 18/2007 no fija un plazo propio para devolver la fianza. Tampoco explican los documentos cómo recuperar el depósito del Registro de fianzas ni si hay sanciones por retraso aparte del interés legal. Eso estaría en la Ley 13/1996, que no está en el corpus.

## Adding a document

Before we could not answer q36, "¿Cuánto es la tasa turística por noche en Barcelona?"

**Document added:** Ley 2/2026, de 6 de marzo, which amends the tax on stays in tourist establishments (`BOE-A-2026-6642.pdf`, 9 pages, 17 chunks), added through the `add_document` tool: "17 chunks, 17 newly embedded". 

| | Answer |
|---|---|
| Before | "The documents I have do not cover this. […] This information is typically regulated by tax laws or municipal ordinances regarding the tax on stays in tourist establishments." |
| After | "Para Barcelona ciudad, a partir del 1 de abril de 2026 […] **Vivienda de uso turístico: 4,50 €** (Llei 2/2026, Preámbulo, apartados 1–6, p. 4)", plus the rates for hotels, hostels and cruise ships. |

Full output in `eval/before_after.json`.

## Harness and guardrails

**AGENTS.md rules** (the system prompt for `agent.py`):
1. Search first and answer only from the results.
2. Cite every claim.
3. Say when the documents don't cover the question.
4. Say which part of a question is not covered.
5. Search again with legal terms, up to 3 times.
6. Answer in the user's language, with exact figures.
7. Call `add_document` only when the user asks.

**Approval:** a wrap tool call runs before every tool call and asks `Allow add_document(...)? [y/N]`. Without a "y" the tool doesn't run, and the model is told the user refused. Because the harness enforces this, neither the model nor injected text can skip it.

**Limits:** at most 6 model calls and 3 searches per question and this is also enforced by middleware from langchain.

**Extra guardrail: citation check.** After the model answers, each "law, article" it cites must match a citation the search actually returned. If not, a warning is added to the answer. This catches citations invented or recalled from memory, the most dangerous failure for legal advice.
- *Case where it fired:* q27 (tourist flat let for 10 nights). The answer cited "LAU, Artículo 5" to say the LAU does not apply, but the search had only returned Decret-llei 3/2023 passages. The harness appended: "⚠ Guardrail: LAU, artículo 5 not found in the retrieved passages. Verify before relying on this answer." The claim happens to be right, but it came from the model's memory, not the corpus.
- *False positive fixed:* in the first version, the q36 refusal ("the corpus contains the LAU, the Catalan Housing Law…") was flagged because "LAU, the…" looked like a citation. The check now only counts "law, Artículo / Disposición / Anexo / Preámbulo".

## Evaluation

The agent (`agent.py`) answered all 36 questions; `evaluate.py` checks and grades them. Results are in `eval/answers.csv`, `eval/results.json` and `eval/summary.json`.

**Code checks:**
- **Refusal:** the answer says the corpus does not cover the question ("no cubre", "do not cover"…). For an answerable question it only counts as a refusal if it also cites nothing, so a cited partial answer is not a refusal.
- **Valid citations:** every "law, article" cited appears in a retrieved passage (the guardrail from `agent.py`).
- **Expected passage retrieved:** the search returned the expected article from the expected document.

**Judge:** `gemini-3.1-flash-lite` receives the question, the reference answer, the retrieved passages and the answer. It writes its reasoning first, then returns two pass/fail verdicts:
1. **Correct:** gives the key facts of the reference answer (figures, deadlines, conditions) without contradicting it. For an unanswerable question, it is correct only if it says the corpus does not cover it.
2. **Supported:** every legal claim is in the retrieved passages. A plain refusal is supported.

**Agreement with my grades** (`eval/human_labels.csv`, 23 answers): **87 %** on correct, **91 %** on supported. We disagreed on 4 questions:
- q04, q10: the judge was stricter. It marked q10 incorrect for leaving out conditions of the reference answer.
- q23: I was stricter. The answer omitted the concrete date.
- q27: the judge marked the LAU art. 5 citation unsupported. I accepted it because the guardrail caught it and notified the user to verify this information (the information also happened to be correct).

**Results** (outcome = code checks + judge):

| Outcome | Count |
|---|---|
| Correct | 27 / 30 answerable |
| Incorrect | 1 |
| Unsupported | 2 |
| Correct refusals | 6 / 6 unanswerable |
| Wrong refusals | 0 |

## Failures

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 1 | q27 (multi): the Decret-llei passage was found but LAU art. 5 was not, and the answer cited it anyway (the guardrail fired). |
| Wrong answer from the right passage | 1 | q10: the right article was retrieved, but the answer left out some of the conditions for the 10 % rent increase. |
| Unsupported claim | 1 | q04: adds "salvo pacto de penalización" to LAU art. 11.3. That exception is not in the retrieved text, which is the current wording after the 2023 reform. |
| Wrong refusal | 0 | |
| Bad test question | 0 | q23 is borderline: the reference expects a concrete date that the passage only gives indirectly. |

**What to fix first:** retrieval for questions that need two passages from different laws. Multi-passage hit@3 is 0.83, against 1.00 for single-passage questions, and q27 shows what happens on a miss: the model fills the gap from memory. Two possible fixes:
- raise k to 5 when the question names more than one law;
- tell the agent in AGENTS.md to run one search per law.

## Decision

**Yes, as a first-pass reference for landlords, not as legal advice.** It answered 27 of 30 answerable questions correctly and refused all 6 out-of-scope ones without making anything up. Every claim carries a citation the user can check in the BOE.

**Safeguards:**
- Always show the citation guardrail's warning. It caught the one answer built on an article the system never read (q27).
- Before acting on anything with legal consequences, the user should open the cited article to check.
- The corpus must be kept up to date. q04 shows the model falling back on outdated wording and things like the tourist-tax rates change every year.

**Cost and latency per question** (agent only, 36 questions):
- **4,807 tokens** on average (median 3,616, max 11,649);
- **12.7 s** on average (median 4.8 s, max 113 s, the slowest runs coinciding with Gemini returning overload errors);
- $0 on the Gemini free tier with `gemini-flash-lite`.

The judge adds about one more call per question during evaluation only.

## AI use

AI helped me with much of the code especially creating the scripts to seperate the pdf text, clean it and chunk it accordingly whether it was structured or fixed and it especially helped out with scripts for th structured ones where i had to cut long articles and seperate them into smaller chunks of apartados. This was very improtant so nothing was chunked appropiately as I wanted to test it in different ways. I also used it to format this report so it would look nice in the md file styling. It also helped me measure some tests like the cost and latency questions as well as format table with results from evaluations onto the report.