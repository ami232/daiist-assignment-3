# Assignment 3 Report

- **Name**: Bruno Sanchis
- **Student ID**: 20262
- **Group**: BBADBA 5B

## Use case

A neighbour (vecino) of **Santa María de Guía** (Gran Canaria) asks the Moysi Voice AI assistant how to do a municipal procedure (trámite): what it is, who can apply, which documents to upload, the deadlines (plazo de presentación / resolución) and what happens if the council does not answer (silencio administrativo). They use the answer to prepare and submit the application in the sede electrónica.

**A wrong answer is costly.** A wrong deadline can make them miss it, a missing document gets the application rejected or delayed, and a wrong silencio makes them think something was granted when it was denied. **"I don't know" is cheap.** The assistant says "Esa información no consta en la ficha del trámite; puede consultarla en la sede electrónica: <link>", and the vecino checks the official page or calls the council. So the system is designed to refuse rather than guess.

## Corpus

| Document set | Source | Date | Licence | Files | Words |
|---|---|---|---|---|---|
| Fichas de trámites del Ayuntamiento de Santa María de Guía (public fields only) | Catalogue of the sede electrónica, `https://santamariadeguia.sedelectronica.es/catalog/...` (each ficha keeps its own URL), curated into JSON for the Moysi Voice AI project | Nov 2026 | Public-sector information, reusable under Ley 37/2007 (reutilización de la información del sector público); no personal data | 54 indexed + 1 held out (`matrimonio-civil`) | 35,970 |

**Known gap:** the brief asks for 50,000 words and this corpus has about 36,000. I chose to stay with a single municipality (Guía) and only the public factual fields, rather than pad it with other material. The original Moysi files also contain the voice agent's conversation scripts, which are mine and not public, so `export_fichas.py` removes them.

## Ingestion

- **Extract.** The fichas are already structured JSON, so no PDF parsing is needed. [export_fichas.py](export_fichas.py) keeps only the public fields: `nombre_oficial`, `sede_url`, `ambito`, `que_es`, `quien_puede`, `identificacion`, `plazo_*`, `silencio_administrativo`, `documentacion*`, `notificacion`, `normativa`, `faq` and `kb_extra`.
- **Clean.** Lists become bullet lines and FAQ items become `P: … R: …`. Every chunk starts with a header, `Trámite: <nombre_oficial>`, so a passage about "1 mes" still says which trámite it belongs to.
- **Problem fixed.** The field `documentacion_aviso` looked like data but was an instruction to the voice agent ("Todavía no puedes decirle qué documentos necesita… Dile: …"). I found it by searching the kept fields for imperative phrases ("Dile", "pregúntale") and dropped it. A second problem came up while embedding: sending a list of 20 strings to `gemini-embedding-2` returned **one** embedding, because the list is read as one multi-part input. Each text now goes as its own `Content`.
- **Metadata per chunk.** `source` (ficha slug), `location` (`palabras 0-200`, or section names), `sections` (every section the chunk covers), `nombre_oficial`, `sede_url`, and `file_hash` (used to detect changed files).
- **Chunks.** 210 in design A, plus the 4 of `matrimonio-civil` added later in the demo; 303 in design B. Vectors are stored in ChromaDB in `index/` (16 MB). A second `main.py index` embeds 0 chunks.

## Test set

I wrote 33 questions in Spanish, as a vecino would ask them on the phone. Each answer was checked against the ficha text first.

| kind | count |
|---|---|
| single | 21 |
| multi (two sections or two fichas) | 6 |
| unanswerable | 6 |

The unanswerable ones are close to the topic. They ask for a deadline the ficha leaves as "Consultar en la ficha del trámite", a fee that is not published, a timetable, a regional aid that Guía does not manage, and the held-out matrimonio civil.

Two examples:
- `q01` (single): "¿Cuánto tarda el ayuntamiento en resolver una licencia de vado?" → `vados · plazo_resolucion` → "1 mes."
- `q23` (multi): "Si el ayuntamiento no contesta, ¿qué pasa con una solicitud de vado y con una de empadronamiento?" → the vado is understood as denied and the empadronamiento as granted.

## Retrieval

A hit means one of the top-k chunks comes from the expected ficha **and** covers the expected section. 27 answerable questions, Gemini `gemini-embedding-2`, cosine distance.

| Design | hit@1 | hit@3 | hit@5 | words added to the prompt (k=5) |
|---|---|---|---|---|
| **A · fixed 200-word windows** | 0.48 | **0.89** | **0.93** | 968 |
| B · one chunk per ficha section (short sections packed, max 300 words) | **0.52** | 0.74 | 0.89 | 724 |

Both designs put the right **ficha** in the top 1 for all 27 questions; they differ only on the section. B usually loses because it returns the ficha's FAQ chunk, which often repeats the fact. **Chosen design: A (fixed)**, by hit@3. The cost is about 240 more words per search, and citations are less readable (`[vados · palabras 0-200]`).

## Tools and subagent

**`search(query)`**: "Search the official procedure sheets (fichas de trámites) of the Ayuntamiento de Santa María de Guía (Gran Canaria): what each trámite is, who can apply, how to identify, required documents, deadlines, silencio administrativo, notifications, legal basis and FAQs. Use it for any question about a municipal procedure in Guía. Write the query in Spanish. Returns the 5 most relevant passages; each one starts with its citation [trámite-slug · section] and ends with the link to the trámite in the sede electrónica."

**`add_document(path)`**: "Add one trámite ficha (a JSON file with the same fields as data/fichas/*.json) to the index, using the same chunking and Gemini embeddings as the rest of the corpus. If the trámite is already indexed: it is skipped when the file has not changed, and replaced when it has. Returns what happened."

One search result (first of 5, for "¿Cuánto tarda en resolverse la licencia de vado?"):

```
[vados · palabras 400-600]
Trámite: Licencia de vado (solicitud, modificación y baja) y cambio de titular de la licencia de ocupación
… P: ¿Cuánto tardan en contestar? R: El plazo para resolver es de un mes. Si pasa el mes sin respuesta,
el silencio se entiende como denegación, así que conviene llamar al ayuntamiento a preguntar por el expediente. …
Sede: https://santamariadeguia.sedelectronica.es/catalog/t/4429600f-873d-4f6c-878b-a0b48f4541c2
```

**Subagent** ([.claude/agents/corpus-researcher.md](.claude/agents/corpus-researcher.md)): its only tool is `mcp__corpus__search`. It searches up to three times, answers in Spanish in at most 120 words with `[slug · section]` citations and the sede link, and otherwise says exactly that the information "no consta".

**Transcript from Claude Code:**
Fresh Claude Code session in this folder. The main agent delegated the question to `corpus-researcher`, which made one `search` call and returned this answer:

> **Me:** Usa el subagente corpus-researcher: ¿qué documentos necesito para pedir un vado en Guía?
>
> **Claude Code:** *(delegates to corpus-researcher; one search in the corpus)*
>
> Para pedir un vado nuevo en Guía hay que solicitar la licencia de vado [vados · palabras 0-200]. Documentos:
> - El último recibo del IBI o la referencia catastral [vados · palabras 200-400].
> - Fotografías de la fachada, la entrada y el entorno [vados · palabras 200-400].
> - Además, conviene aportar un croquis en planta con las medidas del vado y la primera ocupación o licencia de apertura del garaje o local [vados · palabras 200-400].
>
> Lo pide el titular del garaje o local, o su representante, con clave o certificado digital [vados · palabras 0-200]. Para dar de baja un vado hay que indicar sus datos (número y licencia). Para cambiar el titular no se pide ningún documento [vados · palabras 200-400].
> El ayuntamiento tiene un mes para resolver. Si en ese plazo no responde, la solicitud se entiende denegada [vados · palabras 0-200].
> Sede electrónica: https://santamariadeguia.sedelectronica.es/catalog/t/4429600f-873d-4f6c-878b-a0b48f4541c2

I checked the answer against [data/fichas/vados.json](data/fichas/vados.json). Every document, the plazo (1 mes) and the silencio (desestimatorio) match the ficha. The citations use real chunk locations, not the `[vados · sección]` placeholder that the LangChain agent sometimes copies.

## Adding a document

**Already indexed?** `add_document` compares an md5 hash of the file with the one stored in the chunks' metadata.
- Same hash: nothing is embedded ("Skipped").
- Different hash: the old chunks of that ficha are deleted and the new ones added ("Replaced"), so an outdated plazo never stays in the index next to the new one.

Demo ([eval/add_document_demo.json](eval/add_document_demo.json)), with `matrimonio-civil.json` held out of the first index:

| | |
|---|---|
| Question | ¿Qué tengo que hacer para casarme por lo civil en el Ayuntamiento de Guía? |
| Before | "Esa información no consta en la ficha del trámite; puede consultarla en la sede electrónica: …" |
| `add_document("data/extra/matrimonio-civil.json")` | `Added: 'matrimonio-civil' (4 chunks).` |
| Same call again | `Skipped: 'matrimonio-civil' is already indexed and the file has not changed.` |
| After | "Para casarse por lo civil en el Ayuntamiento de Guía hay que realizar dos partes [matrimonio-civil · que_es]: 1. Expediente matrimonial … en el Registro Civil … 2. Solicitud de fecha y oficiante … No es necesario aportar ningún documento en la sede …" |

## Harness and guardrails

[agent.py](agent.py) uses LangChain `create_agent` on `gemini-3.5-flash-lite`, with [AGENTS.md](AGENTS.md) as the system prompt. The tools come from `server.py` over MCP, through the official `mcp` client; `langchain-mcp-adapters` does not support `mcp` 2.x.

- **AGENTS.md rules**:
  - search first;
  - answer only from the results;
  - cite every claim and give the sede link;
  - use the exact "no consta" sentence when the information is missing;
  - decline anything that is not a Guía trámite;
  - answer in Spanish, in at most 120 words;
  - call `add_document` only when asked.
- **Approval.** `add_document` is wrapped: it asks `Allow add_document(<path>)? [y/N]` and runs only on "y". With no interactive user (evaluation, CI) it is denied.
- **Tool-call limit.** `ToolCallLimitMiddleware(run_limit=5)`.
- **Extra guardrail: plazo check.** After the agent answers, every number and every written deadline ("un mes", "diez días") in the answer must appear literally in the text that `search` returned. Citations and links are ignored. If one does not appear, the answer is replaced by "no consta" plus the link. It fired **3 times** in the evaluation, and all 3 were **false positives**:
  - `q23`: the model wrote "tres meses" while the ficha says "3 meses";
  - `q24`: "10 días" while the ficha says "diez días";
  - `q11`: the plan scale written as "1:50" while the retrieved FAQ says "uno a cincuenta".

  I decided to keep it strict on purpose. In this use case blocking a correct answer costs a phone call, while letting an invented deadline through can cost the application.

## Evaluation

[evaluate.py](evaluate.py) runs the agent on all 33 questions ([eval/answers.csv](eval/answers.csv)). The judge's verdicts are in [eval/verdicts.csv](eval/verdicts.csv) and the totals in [eval/summary.json](eval/summary.json).

**Code checks:**
- citations point to a ficha and section that exist in the index;
- answerable questions carry a citation;
- refusal detection (the exact "no consta" sentence);
- whether the guardrail fired.

**LLM judge** (`gemini-3.5-flash-lite`, temperature 0, JSON output). It sees the question, my reference answer, the agent's answer and **all** the retrieved text. It scores **correct** (key facts match the reference, or a proper refusal on an unanswerable question) and **supported** (every claim, especially numbers, deadlines, fees and documents, is in the retrieved text). A first run passed the judge only the first 6,000 characters of the evidence, and it wrongly marked two answers as unsupported. I fixed that and re-ran everything.

| Result | Value |
|---|---|
| Correct (judge) | 25/33 (0.76) |
| Supported (judge) | 30/33 (0.91) |
| Correct refusals (unanswerable) | 5/6 |
| Wrong refusals (answerable) | 7/27 |
| Answerable answers with a citation | 22/27 |
| Valid citations (code check) | 25/33 (0.76) |
| Guardrail fired | 3 (all false positives) |

Invalid citations come mostly from the model copying the placeholder: it writes `[vados · sección]` instead of a real location.

**Agreement with my grades:** I graded q01–q20 by hand in [eval/human_labels.csv](eval/human_labels.csv). The judge and I agree on **20/20 for `correct`** and **18/20 for `supported`**.
- The two `supported` disagreements are q11 and q15. In both, the assistant wrongly answered "no consta". I marked them supported, because a refusal claims nothing that is not in the fichas. The judge marked them unsupported because the refusal itself was wrong. Here I think the judge mixes up "wrong" and "unsupported".
- My first pass marked the five wrong refusals (q02, q06, q11, q15, q20) as correct. After rereading the rubric I changed them to 0: a vecino who gets "no consta" when the ficha has the answer has not been helped. In that first pass I agreed with the judge on 74% for `correct`.

## Failures

First classification from `failure_hint` in [eval/verdicts.csv](eval/verdicts.csv), checked by reading each answer:

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss: the agent's own search query did not bring the right passage | 4 | q02, q06, q15, q20 |
| Wrong refusal: right passage retrieved, but the plazo check blocked the answer | 3 | q11, q23, q24 |
| Unsupported claim: answered from outside knowledge instead of refusing | 1 | q33 (bono de alquiler joven) |
| Wrong answer from the right passage | 0 | |
| Bad test question | 0 | |

Note on the retrieval misses: with the user's question as the query, retrieval always found the right ficha. The agent rewrites the question into keywords before searching, and those rewritten queries are what failed. For example, q02 searched "vado silencio administrativo santa maria de guia" and got avisos-denuncias, corte-via and obras-edificacion, but not vados. Words like "Santa María de Guía" appear in every ficha, so they add noise and no signal.

**What to fix first:** the plazo check, so that "un mes" and "1 mes" count as the same plazo. It caused 3 of the 8 failures, all of them correct answers that were blocked, and the fix is small: turn written numbers into digits before comparing. Next I would tell the agent to search first with the vecino's own words (4 of 8 failures), and replace the "[slug · section]" placeholder in AGENTS.md with a real example so citations are valid.

## Decision

Cost and latency per question: **about 4,500 tokens** and **33 s on average**. The time includes waiting and retrying when the free-tier Gemini API answered 503 "high demand"; a normal answer takes 5 to 10 s. On the free tier the money cost is 0.

I would let vecinos rely on it to find out what a trámite needs (documents, plazos, silencio), but not as the final word. 76% of the answers were correct. Of the 8 failures, 7 were "no consta" when the ficha did have the answer: annoying, but the vecino is sent to the sede link and loses nothing. Only 1 (q33) was a confident answer from outside the fichas. Safeguard: every answer shows its citations and the sede electrónica link, and the interface tells the vecino to check plazos there before submitting anything.

## AI use

I used Claude Code (Claude Opus) as a programming assistant. It wrote the code of `export_fichas.py`, `index.py`, `server.py`, `agent.py` and `evaluate.py` following decisions I took when it asked me:
- municipality: Guía only;
- public fields only;
- which two chunking designs to compare;
- the plazo-check guardrail;
- the duplicate-document policy;
- the model;
- the refusal sentence;
- the held-out ficha;
- the choice of design A by the numbers;
- keeping the guardrail strict.

It also produced a first draft of `eval/questions.csv` from the fichas, which I reviewed and own, and the explanatory document in `docs/`. My own grades in `eval/human_labels.csv`, the failure priorities and the ship decision are mine.
