# Assignment 3 Report

- **Name**: Paul Khairallah
- **Student ID**: 18966
- **Group**: BBADBA 5B

## Use case

A driver in Spain (an international student, a new resident, a novice driver) checks a traffic rule before acting on it: how much they can drink and still drive, whether their foreign licence is still valid, what a fine or a speeding ticket will cost in money and points. They act on the answer directly. A wrong answer ("0.5 g/l is fine for you", "you can drive on that licence for a year") means a fine, lost points, a suspended licence or a crash. "The corpus does not cover this, check the DGT" costs one more lookup. So the system has to refuse rather than guess, and every claim has to point to the article so the user can check it.

## Corpus

Consolidated texts (the version in force today) from the BOE open-data API (`/datosabiertos/api/legislacion-consolidada/id/{id}/texto`), downloaded by `index.py` into `corpus/`.

| Source | Document | BOE id / URL | Version in force from | Licence | Words indexed | Chunks |
|---|---|---|---|---|---|---|
| LSV | Ley sobre Tráfico, Circulación de Vehículos a Motor y Seguridad Vial (RDL 6/2015) | [BOE-A-2015-11722](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11722) | latest change 2026-10-01 | BOE reuse conditions (Resolución AEBOE 27-06-2024): commercial and non-commercial reuse allowed, cite the source, don't distort the meaning | 32,815 | 188 |
| RGC | Reglamento General de Circulación (RD 1428/2003) | [BOE-A-2003-23514](https://www.boe.es/buscar/act.php?id=BOE-A-2003-23514) | latest change 2026-10-01 | same | 41,491 | 249 |
| RGCond | Reglamento General de Conductores (RD 818/2009) | [BOE-A-2009-9481](https://www.boe.es/buscar/act.php?id=BOE-A-2009-9481) | latest change 2023-12-07 | same | 22,236 | 133 |
| ITV *(added later, see "Adding a document")* | Real Decreto 920/2017, inspección técnica de vehículos | [BOE-A-2017-12841](https://www.boe.es/buscar/act.php?id=BOE-A-2017-12841) | consolidated text | same | 9,802 | 49 |
| **Total (base corpus)** | | | | | **96,542** | **570** |

Legislation contains no personal data. Annexes kept: LSV I-IV, VIII, IX (definitions, points table, courses, speeding-fine table); RGC II-III (sports events, special vehicles); RGCond III (documents for licences). Left out on purpose: card layouts, exam logistics, medical criteria and the sign catalogue (~60k words), which a driver's "what is the rule" question doesn't need and the daily embedding quota couldn't afford. Preambles are left out too, since they explain why the law changed, not what it says.

## Ingestion

- **Extract**: BOE XML is split into `<bloque>` elements (article, heading, annex), each with dated `<version>`s. `index.py` keeps the version in force today (latest `fecha_vigencia` not in the future).
- **Clean**: tables become one `cell | cell` line per row; footnotes, image placeholders and signatures are dropped; all whitespace (including `&nbsp;`) is normalised.
- **Chunk**: structure-based. One chunk per article, annex or annex section. Articles over 350 words are split at paragraph boundaries into parts, and each part repeats the article heading. Every chunk's text starts with `[SOURCE · document title]` and the article heading, so the vector knows which law and article it comes from. Median 146 words, max 350, **570 chunks**.
- **Metadata per chunk**: `source` (LSV/RGC/RGCond), `boe_id`, `doc_title`, `location` (e.g. `Artículo 20`, `Anexo II`, `Anexo II, Artículo 3`, `Norma aprobatoria, Disposición final primera`), `heading`, `section` (Título > Capítulo > Sección), `part`/`parts`, `url` (BOE deep link to the article), `version_date`, `words`, `text_hash`.
- **Embedding**: two collections over the same chunks: `gemini-embedding-2` and `gemini-embedding-001` (the one search uses, see Retrieval), 768 dimensions, `RETRIEVAL_DOCUMENT` / `RETRIEVAL_QUERY`, stored in ChromaDB (`index/chroma`, cosine). Each batch is written as soon as it returns. A chunk is re-embedded only if its `text_hash` changed, metadata-only changes are updated in place, and chunks a new version no longer has are deleted. `index/chunks.jsonl` mirrors the collection for BM25. Query vectors are cached in `index/query_cache.json`.

**Extraction problems fixed:**
1. **Editorial notes, including repealed wording.** The BOE puts notes inside `<blockquote>`: "téngase en cuenta…", "se modifica por…", and sometimes the whole previous wording ("Redacción anterior: …"). The first index had RGC art. 50 part 2 made entirely of the old text, which gives a 50 km/h general urban limit, next to the current 30 km/h rule. A model could have quoted the repealed limit with a valid citation. Dropping `<blockquote>`s changed 198 chunks, which were re-embedded.
2. **Superseded articles with no repeal marker.** The XML still contains the old RGC arts. 151–173 (sign rules replaced in 2025–26). They only have their 2004 version, so they look in force, and their numbers collide with the new arts. 151–158 (urban traffic, in force since 1-10-2026). The official consolidated web page leaves them out, so `index.py` saves the block ids that page shows (`corpus/*.blocks.txt`) and keeps only those (36 blocks dropped).
3. **Annex text hidden in heading blocks.** Annexes come as heading-type blocks with the body inside, so the first chunker skipped them, losing the points table (LSV Annex II) and the speeding-fine table (Annex IV).
4. **Tables flattened into run-on text.** The speed table in RGC art. 48 lost which limit belonged to which vehicle; it now renders one row per line.
5. **Duplicate article numbers.** RGC Annex II has its own Artículo 1–35, and the approving decree has its own dispositions, so locations are prefixed (`Anexo II, Artículo 20`, `Norma aprobatoria, …`).

## Test set

The questions and reference answers were drafted with an AI assistant directly from the article texts (each reference checked against the passage it cites); I chose English for the questions and kept the set without changes. Grading the answers later exposed one weak reference: q22's includes the driver's duties although the question only asks about passengers (see Failures). 37 questions in English, written from the passages (the corpus is Spanish, so retrieval is cross-lingual): **23 single, 7 multi (two passages), 7 unanswerable**. The unanswerable ones sit right next to the corpus: ITV frequency, criminal penalties for drink-driving, Madrid's low-emission zone, the V-16 beacon, exchanging a UAE licence, insurance cover amounts, DGT fees. In each case the corpus touches the topic but doesn't hold the answer.

Examples:
- `q25` (multi): *"I've had my licence for one year and blew 0.20 mg/l. Is that over my limit, and how many points do I lose?"* → RGC art. 20 (novice limit 0.15 mg/l) + LSV Annex II (more than 0.15 up to 0.30 mg/l for novices = 4 points).
- `q35` (unanswerable): *"Can I exchange my UAE driving licence for a Spanish one without taking the test?"* RGCond arts. 18–23 say an exchange depends on an international agreement but never list countries, so the right answer is that the corpus doesn't say.

## Retrieval

Hit = **every** expected passage (source + location) in the top k, over the 30 answerable questions. any@5 (at least one expected passage in the top 5) is 1.00 for A and G. For a multi question hit@1 is impossible by construction, so its ceiling is 23/30 = 0.77. Spanish queries come from `gemini-3.5-flash-lite` rewriting the question in Spanish legal terms (cached in `eval/translations.json`). Words = average words of the k chunks added to the prompt. Full per-question ranks are in `eval/retrieval.csv`.

| Design | Embedding | hit@1 | hit@3 | hit@5 | multi hit@5 | words@5 |
|---|---|---|---|---|---|---|
| A dense, English question | gemini-embedding-2 | **0.73** | **0.90** | 0.93 | 0.71 | **1156** |
| B dense, Spanish rewrite | gemini-embedding-2 | 0.63 | 0.83 | 0.90 | 0.57 | 1212 |
| C BM25, Spanish rewrite | (keywords) | 0.40 | 0.73 | 0.83 | 0.57 | 1207 |
| D hybrid B+C (RRF) | gemini-embedding-2 | 0.50 | 0.83 | 0.90 | 0.71 | 1217 |
| E fusion A+C (RRF) | gemini-embedding-2 | 0.60 | 0.87 | 0.93 | 0.86 | 1173 |
| F fusion A+B (RRF) | gemini-embedding-2 | 0.67 | 0.87 | 0.93 | 0.71 | 1178 |
| **G dense, English question** | **gemini-embedding-001** | 0.57 | 0.83 | **1.00** | **1.00** | 1319 |
| H dense, Spanish rewrite | gemini-embedding-001 | 0.60 | 0.83 | 0.87 | 0.43 | 1298 |

Words added at k = 1 / 3: A 244 / 717, G 268 / 811. Same chunks for every design; the two embedding models have separate ChromaDB collections (`trafico`, `trafico_e001`), since their vectors aren't comparable (cosine ~0.01 between the two models' vectors of the same chunk).

**Chosen: G (dense, gemini-embedding-001, on the user's question, k = 5).** The search tool returns 5 passages, so hit@5 is what decides whether the agent sees the evidence. G is the only design with every expected passage in the top 5 for all 30 answerable questions, including both passages of all 7 multi questions; A misses the second passage of q24, q26 and q27. The cost is ~14% more words in the prompt (1319 vs 1156) and a worse top-1/top-3 ranking, which matters less because the agent reads all 5. Rewriting the question into Spanish hurts with both models (B < A, H < G). A practical note: gemini-embedding-2 and its preview share one daily free quota (1,000), which the indexing used up; gemini-embedding-001 has its own. I keep G: retrieving all the passages an answer needs matters more than ranking the first relevant one higher, especially for multi-part legal questions where the limit and the penalty sit in different articles.

## Tools and subagent

`server.py` (MCP, stdio, server name `corpus`) loads `index/` at startup and never embeds the corpus. Tool descriptions are the docstrings in `server.py`:

- **search(query, source="")**: "Search Spanish traffic law: the Ley de Tráfico (LSV …), the Reglamento General de Circulación (RGC …) and the Reglamento General de Conductores (RGCond …) … Use it for every question about Spanish driving rules; search again with different words, or once per sub-question … Returns the 5 most relevant passages (in Spanish), each headed by its citation in the form [SOURCE, location] … If nothing in the passages answers the question, the corpus does not cover it." If the query can't be embedded (quota), it falls back to keyword search and says so at the top of the result.
- **add_document(path)**: "Add one consolidated Spanish law (a BOE XML file …) to the search index … If that document is already indexed, it is updated in place … Changes the shared index, so only run it when the user asked for it."

One search result (query `tasa alcohol aire espirado general conductores`, first of 5):

```
[RGC, Artículo 20] Artículo 20. Tasas de alcohol en sangre y aire espirado.
Document: Reglamento General de Circulación (RD 1428/2003) | version in force from 2004-01-23 | https://www.boe.es/buscar/act.php?id=BOE-A-2003-23514#a20
No podrán circular por las vías objeto de la legislación sobre tráfico, circulación de vehículos a motor y seguridad vial los conductores de vehículos ni los conductores de bicicletas con una tasa de alcohol en sangre superior a 0,5 gramos por litro, o de alcohol en aire espirado superior a 0,25 miligramos por litro. …
```

**Subagent** (`.claude/agents/corpus-researcher.md`, tool `mcp__corpus__search` only): searches once per sub-question (max 4), answers only from the passages, cites `[SOURCE, location]`, gives numbers with units and conditions, and starts with `The corpus does not cover this.` when it can't answer. Reply is at most 6 sentences plus a `Sources:` line.

**Transcript** (Claude Code in the Claude desktop app, repo folder open, `corpus` MCP server approved). Prompt: *"Use the corpus-researcher subagent: I've had my licence for a year and blew 0.20 mg/l. Am I over the limit and how many points do I lose?"*

```
The corpus-researcher agent is running in the background. It's looking up two things: the alcohol
limit for a driver with one year of licence, and how many points are lost for going over it. I'll
send you its cited answer when it finishes.

Yes, you're over the limit, and at 0.20 mg/l you lose 4 points. This comes from the
corpus-researcher agent's search of the BOE texts. I haven't read the retrieved passages myself.

The limit for you
* For two years after getting your licence you are a novice driver (conductor novel). Your limit is
  0.3 g/l in blood or 0.15 mg/l in exhaled air (aire espirado), whatever vehicle you drive
  [RGC, Artículo 20].
* At 0.20 mg/l you are over it. The general limit for experienced drivers is 0.5 g/l in blood or
  0.25 mg/l in exhaled air, so one of them would be under it at 0.20 mg/l [RGC, Artículo 20].

Points
* For drivers whose licence is under two years old, and for professional drivers, a reading above
  0.15 and up to 0.30 mg/l costs 4 points. Above 0.30 mg/l it costs 6 points [LSV, Anexo II].

Fine
* Driving over the alcohol limit, when it is not a crime, is a very serious offence (infracción muy
  grave) [LSV, Artículo 77]. Very serious offences carry a €500 fine [LSV, Artículo 80].
* The fine goes up to €1,000 only if you were already fined for alcohol in the previous year, or if
  you are over double your permitted rate, which would be 0.30 mg/l for you [LSV, Artículo 80].
* The fine can be raised by up to 30% depending on how serious the offence was, your record or
  repeat offending [LSV, Artículo 81].

Not covered by the corpus: the points bands are given only in mg/l of exhaled air, with no blood
(g/l) figures. The passages say nothing about criminal penalties, so check those with the DGT.
```

The subagent split the question into its parts (limit, points), searched for each, cited every claim and stated what the corpus does not cover, as its instructions require.

## Adding a document

**Already indexed → update in place.** Chunk ids are `SOURCE:block:part` and each stores a hash of its text. Re-adding the same file embeds nothing and reports `unchanged`. A newer consolidated version re-embeds only the changed articles, updates metadata-only changes without new vectors, and deletes chunks the new version no longer contains (repealed articles), reporting `updated`. *Why:* BOE texts are amended in place, so the useful behaviour is "bring it up to date" without spending quota on unchanged articles and without keeping a repealed rule next to the new one.

Unanswerable question **q31**: *"My car is 6 years old. How often does it need to pass the ITV inspection?"* Document added: Real Decreto 920/2017 (ITV), 49 chunks (articles only).
- **Before** (from the evaluation run): "The corpus does not cover this. The frequency of ITV inspections based on vehicle age is not specified in the current texts of the LSV, RGC, or RGCond. You should check … the DGT or an authorized ITV station."
- **add_document** (`corpus/ITV__BOE-A-2017-12841.xml`): `added`, 49 chunks, 49 embedded. **Called again:** `unchanged`, 0 embedded, 49 reused.
- **After**: "If your car is a standard passenger car (category M1 …): Up to 4 years old: Exempt [ITV, Artículo 6]. From over 4 years to 10 years old: Every 2 years (biennial) [ITV, Artículo 6]. Over 10 years old: Annually [ITV, Artículo 6]. Since your car is 6 years old, it must pass the ITV inspection every 2 years [ITV, Artículo 6]." This matches art. 6. Full record in `eval/add_document_demo.json`.

## Harness and guardrails

`agent.py`: LangChain `create_agent` with `server.py`'s tools over MCP stdio, `AGENTS.md` as the system prompt, `gemini-3.5-flash-lite` (fallback: Groq `openai/gpt-oss-120b` when Gemini fails).

- **AGENTS.md rules** (each with its reason in the file): search first and answer only from passages; cite every claim exactly as `[SOURCE, location]`; refuse with `The corpus does not cover this.` and no facts from memory; one search per sub-question; exact numbers with units and conditions; user's language; no legal advice beyond the text; `add_document` only on explicit request. The ones that matter most to me are grounded answers, exact citations and refusing what the corpus doesn't support. Next change: rule 3 should say explicitly that a refusal may point the user to the relevant authority (DGT, city council, Código Penal), since that is useful and the judge currently penalises it; I left the evaluated version unchanged so the results match it.
- **Approval**: `HumanInTheLoopMiddleware` interrupts before every `add_document` call. In a terminal it asks `Allow? [y/N]`; with no terminal it rejects unless `--approve-add` is given. Tested: *"Please add corpus/ITV__… to the index"* with no terminal → `Rejected add_document(...)`, and the agent answered that the document was not added.
- **Call limits**: 6 tool calls and 8 model calls per question.
- **Extra guardrail: citation check.** Every `[SOURCE, location]` in the answer must be a passage that `search` actually returned in this run (or a sub-reference of one, e.g. `Artículo 76.z3`), and a non-refusal answer must cite something. On failure the agent gets one rewrite; if it still fails, the answer is replaced by a refusal listing the passages it did retrieve. **Where it fired** (first full run, `eval/answers_run1.jsonl`): 5 of 37 answers. In q08, q29, q30 the model grouped citations (`[LSV, Artículo 63, LSV, Anexo II]`) and the rewrite fixed them. In q33 it cited a sub-paragraph. In **q20** two rewrites still failed, so a probably-correct answer was replaced by a refusal: the guardrail was too strict. Fix: the parser now splits grouped citations and accepts sub-references, and AGENTS.md asks for one citation per bracket. A second model (gpt-oss) later wrote `Artículo 4` with a narrow no-break space, which also failed until spaces were normalised. I keep the citation check: given the legal and safety risk, its benefit outweighs an occasional unnecessary refusal. It already tries one correction (the agent rewrites the answer) before falling back to a refusal; after the parser fix it did not fire in the final run.

## Evaluation


- **Code checks** (`evaluate.py`): refusal detected (answer starts with the refusal sentence); every citation valid (in the retrieved passages); answer cites something; expected passage retrieved; expected passage cited; number of searches.
- **Judge**: `gemini-3-flash-preview`, a stronger model than the agent's flash-lite (fallbacks: `gemini-3.6-flash`, then Groq `gpt-oss-120b`; `results` records which model graded each answer). It gets the question, the reference answer, **the retrieved passages as the only evidence** and the answer, and returns JSON `correct` / `supported` / `unsupported_claims` / `reason`. Rubric (full text in `evaluate.py`, `JUDGE_RUBRIC`): *correct* = the reference's key facts with no contradiction, or for unanswerable questions a refusal that doesn't supply the missing answer; *supported* = every factual claim, including law names and decree numbers, is in the passages.
- **Agreement with the judge** (24 answers graded by hand in `eval/human_labels.csv`, from `eval/grading_sheet.md`, before reading the verdicts):

| | Agreement | Cohen's κ | Disagreements |
|---|---|---|---|
| correct | 23/24 = 0.96 | 0.65 | q22 (judge 0, me 1) |
| supported | 17/24 = 0.71 | 0.11 | q20, q26, q31, q32, q34, q36 (judge 0, me 1); q35 (judge 1, me 0) |

  I trust the judge for correctness, but not for supportedness until the rubric is tightened to allow refusals that name the relevant authority. On *correct* the judge only differs on q22, where it counted the driver's duties from the reference as missing in an answer about passengers. On *supported* the judge is stricter than me on harmless extras (q26's "31–40 km/h over") and on refusals that name where the rule lives (Código Penal, DGT, insurance law); it is more lenient on q35, where it missed the unsupported "no tests needed" claim I marked 0. κ for *supported* is low partly because almost every answer is supported (few 0s), so a handful of disagreements weighs heavily.

- **Results** (`eval/summary.json`, `eval/results.csv`; agent `gemini-3.5-flash-lite`, search design G):

| | Count |
|---|---|
| Answerable (30): correct and supported | 26 |
| Answerable: correct but with an unsupported claim (q19, q20, q26) | 3 |
| Answerable: wrong (q22) | 1 |
| Answerable: wrong refusals | 0 |
| Unanswerable (7): refused, nothing unsupported (q33, q37) | 2 |
| Unanswerable: refused, but the refusal adds an unsupported claim (q31, q32, q34, q36) | 4 |
| Unanswerable: answered instead of refusing (q35) | 1 |
| Code checks: answers whose citations are all valid | 37/37 |
| Code checks: expected passage retrieved / cited | 29/30 / 29/30 (q30 missed) |
| Citation guardrail fired | 0 (5 in run 1, before the parser fix) |

  Judge models: `gemini-3-flash-preview` graded 10 answers; it then kept failing (free-tier limit / overload) and **27 verdicts came from the Groq fallback `gpt-oss-120b`**. Several "unsupported" verdicts on refusals are debatable (e.g. q31's "not specified in the LSV, RGC or RGCond" is a statement about the corpus, not a legal fact); my own grades disagree with all of them (see agreement above).

## Failures

| Question | What happened | Cause |
|---|---|---|
| q35 (unanswerable) | Answered the UAE licence exchange instead of refusing, and claimed no tests are needed. The passages only say an exchange depends on an agreement; they never name the UAE. | Unsupported claim |
| q19 | Correct 2-year rule, plus an uncited sentence saying very serious offences take longer, which no passage says. | Unsupported claim |
| q22 | Judged wrong for leaving out the driver's hazard-light / warning-device duty, but the question asked what the *passengers* should do. My reference included the driver's duties, which the question didn't ask for. | Bad test question |
| q26 | Right fine (300 €) and points (2), but it described the band as "31–40 km/h over" when the table's 151–170 km/h band on a 120 road is 31–50 over. | Wrong answer from the right passage |

**Counts by cause** (4 failures out of 37): unsupported claim 2 (q35, q19), bad test question 1 (q22), wrong answer from the right passage 1 (q26), retrieval miss 0, wrong refusal 0.

**What to fix first.** (1) Require the retrieved passages to establish that the rule applies to the user's specific case, otherwise refuse: this addresses q35, the most consequential failure. (2) Then stop unsupported extras (q19). (3) Then correct the q22 test reference, which affects the evaluation rather than user safety.

The judge also marked the refusals of q31, q32, q34 and q36 as unsupported because they name where the rule lives (Código Penal, DGT, insurance legislation). I graded them as supported: they refuse correctly and only point the user to the right authority. I record these as a **judge-calibration issue, not an assistant failure**.

## Decision

Yes, I would let drivers rely on it for routine Spanish driving regulations (limits, points, fines, licence ages and validity), always with a direct BOE citation for every claim and a disclaimer that it is a guide, not legal advice. Foreign licence exchanges and other high-risk or ambiguous cases should require human verification before a definitive answer is given: q35 shows the agent can still answer one of those confidently from general articles that don't cover the user's case. Cost and latency per question (final run): **6,208 input + 143 output tokens** for the agent on average, **13.6 s mean, 35.5 s max**, plus ~1 query embedding per search; the judge adds ~3,400 tokens per graded answer (evaluation only).

## AI use

I used Claude to write and debug the code, to compare the retrieval designs, and to draft the test questions and reference answers from the articles. 
