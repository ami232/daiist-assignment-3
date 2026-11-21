# Assignment 3 Report

- **Name**: Francisco Roca
- **Student ID**: 15701
- **Group**: BBADBA 5A

## Use case

**Who asks:** English-speaking tenants, landlords and neighbours in Spain: expats, international students and foreign owners. They do not read Spanish legal texts, but they have to sign Spanish contracts and deal with Spanish landlords and owners' associations.

**What they do with the answer:** decide whether to sign, pay, refuse or complain. Typical questions: can my landlord keep my deposit, how long is my contract really, can they raise the rent, do I have to accept this repair, can the owners' association ban tourist lets.

**Cost of a wrong answer vs "I don't know":** a wrong deadline or amount can make a tenant lose a right (e.g. miss the 30-day notice, accept an illegal deposit) or make a landlord break the law. "I don't know" costs the user a phone call to a lawyer or the consumer office. So a wrong answer is much worse than a refusal. The system is built to refuse rather than guess, and every claim must cite the article so the user (or their lawyer) can check it.

## Corpus

| Document | Short name | URL | Consolidated version (last update) | Licence | Words |
|---|---|---|---|---|---|
| Ley 29/1994, de Arrendamientos Urbanos | LAU | https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003 | 13/11/2026 | BOE reuse conditions (free reuse with source cited; Ley 37/2007, Real Decreto 1495/2011) | 23,653 |
| Ley 12/2023, por el derecho a la vivienda | LDV | https://www.boe.es/buscar/act.php?id=BOE-A-2023-12203 | 07/10/2026 | same | 25,125 |
| Ley 49/1960, sobre propiedad horizontal | LPH | https://www.boe.es/buscar/act.php?id=BOE-A-1960-10906 | 03/10/2026 | same | 11,610 |
| **Total** | | | | | **60,388** |

Added later with `add_document` (see "Adding a document"): Ley 5/2018 on illegal occupation of homes (BOE-A-2018-7833), `docs_to_add/BOE-A-2018-7833.html`.

Laws are public documents with no personal data. The texts are in Spanish; the questions and answers are in English.

## Ingestion

`index.py` downloads the consolidated HTML from boe.es (saved in `corpus/`, git-ignored, re-downloaded by `main.py index`), extracts the law text with BeautifulSoup from the `#textoxslt` block and walks it paragraph by paragraph. Headings (`Artículo 9. Plazo mínimo.`, `Disposición adicional primera`, `TÍTULO II`, `CAPÍTULO II`) are detected with a regex that also accepts the spelled-out article numbers of the LPH (`Artículo noveno`, `Artículo diecisiete`).

**Extraction problems I fixed:**
- **Amendment notes.** Inside each article the BOE page has `<blockquote>` notes like "Se modifica por el art. 1.9 de la Ley 4/2013…" and version stamps ("Texto añadido, publicado el…"). They are not law, but they contain law names and article numbers, so they matched queries and got cited. They are removed before chunking.
- **LPH article numbers in words.** The first regex only knew `Artículo 9`, so LPH articles were merged into huge chunks with no location. The regex now accepts ordinals in words.

**Two chunking designs:**
- **fixed:** 300-word windows with 50 words overlap over each law, ignoring structure. 243 chunks.
- **structure:** one chunk per article (or disposición / preámbulo); articles longer than 300 words are split on paragraph boundaries into "parte 1/3, 2/3…". The embedded text is prefixed with the law title, the enclosing Título/Capítulo and the article heading, so a short paragraph still carries its context. 315 chunks.

**Metadata on every chunk:** `source` (LAU/LDV/LPH), `title`, `location` (e.g. `Artículo 9`), `heading`, `part` (Título · Capítulo), `design`, `origin` (`corpus` or `added`), `words`, `chunk_index`, and for fixed windows `locations` (every article the window touches).

**Embeddings:** `gemini-embedding-2`, 768 dimensions, task type `RETRIEVAL_DOCUMENT` for chunks and `RETRIEVAL_QUERY` for queries, stored in ChromaDB (`index/chroma`, cosine distance). Chunk ids are a hash of model + dimension + design + text, so `main.py index` only embeds chunks without a saved vector; a second run embeds nothing. Query vectors are cached in `index/query_cache.json`. The whole `index/` is 13 MB.

## Test set

I wrote 36 questions in English from the law texts (`eval/questions.csv`), phrased the way a foreign tenant or landlord would ask them, each with the expected law and article and a reference answer taken from the article.

| Kind | Count | |
|---|---|---|
| single (one passage) | 22 | q01–q22 |
| multi (two passages) | 7 | q23–q29 |
| unanswerable (not in the corpus) | 7 | q30–q36 (squatting procedure, property transfer tax, regional rules, current index values…) |

Examples:
- **single, q01:** "What is the minimum length of a rental contract for a primary residence if the landlord is an individual?" → LAU Artículo 9: five years; a shorter term renews compulsorily year by year up to five years unless the tenant gives 30 days' notice.
- **multi, q24:** "What is a large landlord (gran tenedor) and what must they do if a vulnerable tenant asks for the extraordinary extension at the end of the contract?" → LDV Artículo 3 (more than ten urban residential properties or more than 1,500 m²) + LAU Artículo 10 (must accept up to one extra year).

The questions are in English but the corpus is in Spanish, so retrieval is cross-lingual. That is deliberate: it is the real situation of the users.

## Retrieval

`evaluate.py` searches with each answerable question (29) and checks whether the expected article is in the top k. For multi questions, hit@k counts if any expected article is found, and `all@5` if all of them are.

| Design | Method | hit@1 | hit@3 | hit@5 | all@5 | words added to prompt (top 5) |
|---|---|---|---|---|---|---|
| fixed | vector | 0.76 | 0.97 | 1.00 | 0.93 | 1,493 |
| fixed | hybrid (vector + BM25, RRF) | 0.76 | 0.93 | 1.00 | 0.97 | 1,493 |
| **structure** | **vector** | **0.90** | **0.97** | **0.97** | **0.90** | **910** |
| structure | hybrid | 0.79 | 0.97 | 0.97 | 0.86 | 940 |

**Chosen: structure + vector, k = 5.** It has by far the best hit@1 (0.90 vs 0.76) and puts 40% fewer words in the prompt. Fixed windows look better at hit@5, but that is partly an artefact: a 300-word window often spans two or three articles, so it "hits" more articles while each chunk is less precise, and the citation the agent must give is ambiguous. Hybrid search did not help: the questions are in English, so BM25 on Spanish text adds mostly noise and pushes the right article down (hit@1 0.90 → 0.79).

Misses with the chosen design: q06 and q07 at rank 2 (a neighbouring article of the same chapter ranks first), and q26 (tourist lets, LPH Artículo diecisiete) not in the top 5 for the English question. The agent recovers these because it searches in Spanish with legal terms (AGENTS.md rule 1); for q26 it searched "vivienda turística mayoría tres quintas partes LPH artículo diecisiete" and found it.

## Tools and subagent

**MCP server** (`server.py`, MCP Python SDK, stdio), two tools:

- `search(query)`: "Search Spanish residential-tenancy law: the Ley de Arrendamientos Urbanos (LAU, Ley 29/1994), the Ley por el derecho a la vivienda (LDV, Ley 12/2023) and the Ley de Propiedad Horizontal (LPH, Ley 49/1960), consolidated BOE texts, plus any law added later with add_document. Use it for any question about renting a home in Spain: contract length and renewals, rent and rent updates, deposits (fianza), repairs and works, selling a rented flat, tensioned-market zones, large landlords (grandes tenedores), and owners' associations. Write the query in Spanish with the legal terms if you know them. Call it again with other words if the first results do not answer the question. Returns the 5 most relevant passages, each with the citation to use, e.g. [LAU, Artículo 9]…"
- `add_document(path)`: "Add one law to the searchable index. `path` is a local BOE HTML page… parsed article by article, chunked, embedded with Gemini and stored. If the same law is already indexed with identical text, nothing is embedded; if its text changed, the old chunks of that law are replaced… Only call it when the user explicitly asks to add a document." It imports `chunk_file` and `embed_and_store` from `index.py`; it does not reimplement the pipeline.

**One search result** (first of five for q01):

```
--- Result 1  cite as [LAU, Artículo 9]
Law: Ley 29/1994, de 24 de noviembre, de Arrendamientos Urbanos.
Section: Artículo 9. Plazo mínimo. (parte 1/3)
Part: TÍTULO II. De los arrendamientos de vivienda · CAPÍTULO II. De la duración del contrato

1. La duración del arrendamiento será libremente pactada por las partes. Si esta fuera inferior a cinco años,
o inferior a siete años si el arrendador fuese persona jurídica, llegado el día del vencimiento del contrato,
este se prorrogará obligatoriamente por plazos anuales hasta que el arrendamiento alcance una duración mínima
de cinco años, … salvo que el arrendatario manifieste al arrendador, con treinta días de antelación …
```

**Subagent** (`.claude/agents/corpus-researcher.md`, tools: `mcp__corpus__search` only):

> You are a legal researcher for Spanish residential-tenancy law. Your only source is the `search` tool of the `corpus` MCP server. The laws are in Spanish; you reply in English.
> 1. Search in Spanish with legal terms (deposit → fianza, renewal → prórroga, early termination → desistimiento). For a question with two parts, search each part separately. If the first results miss, search again with different words (at most 4 searches).
> 2. Answer only from the returned passages. Never add a rule, amount or deadline that is not in them.
> 3. Cite every claim exactly as the result says, e.g. `[LAU, Artículo 9]`. Never cite an article you did not receive.
> 4. If the passages do not answer the question, say "I don't know: the corpus does not cover this" and say what is missing. Do not guess from memory.
> 5. Reply in English in 3-6 sentences: the direct answer first, then conditions, then citations.

**Transcript from Claude Code** (project folder `daiist-assignment-3`, where `.mcp.json` starts `server.py`):

```
> Use the corpus-researcher agent: how much deposit can a landlord ask for a residential lease?

● Delegating to the corpus-researcher agent now.
● corpus-researcher(Deposit limit for residential leases)

  [prompt to subagent] How much deposit (fianza/garantía adicional) can a landlord ask for in a residential
  lease in Spain? Please cite the relevant articles from the Urban Leases Act (LAU) and any modifications
  introduced by the 2023 Housing Law (Ley 12/2023).

  [tool] mcp__corpus__search {"query": "fianza depósito garantía adicional arrendamiento vivienda"}
  [tool] mcp__corpus__search {"query": "garantías adicionales fianza arrendamiento Ley 12/2023 vivienda"}
  [result 1 of both] --- Result 1  cite as [LAU, Artículo 36]
    Section: Artículo 36. Fianza. (parte 2/2)
    En el caso del arrendamiento de vivienda, en contratos de hasta cinco años de duración, o de hasta siete
    años si el arrendador fuese persona jurídica, el valor de esta garantía adicional no podrá exceder de dos
    mensualidades de renta. En el caso de los arrendamientos temporales … una mensualidad de la renta. …

  [subagent answer]
  Mandatory fianza (statutory deposit): at signing the landlord must demand a cash deposit of one month's rent
  for residential leases. It is not updated during the first five years (seven if the landlord is a legal
  entity), but on each renewal it may be brought up to one month's current rent. [LAU, Artículo 36, parts 1/2
  and 2/2]
  Additional guarantees (garantías adicionales): the parties may agree extra security, capped at two months'
  rent for leases of up to five years (seven if the landlord is a legal entity) and one month for temporary
  leases. The landlord can never require the tenant to take out rent-default insurance. [LAU, Artículo 36,
  part 2/2]
  Role of Ley 12/2023: the retrieved passages from that law do not contain any changes to the deposit caps.
  The two-month cap (introduced by earlier amendments and now in the consolidated LAU text) is the operative
  rule. [LDV, Preámbulo, part 36/41]
  In summary: at most three months' rent up front: one month of fianza plus at most two months of additional
  guarantee, and never compulsory rent-default insurance.

● Agent "Deposit limit for residential leases" completed · 17s
```

The subagent used only `search`, searched in Spanish, and the amounts match LAU Artículo 36. Two weaknesses, the same ones I found when grading the harness: "introduced by earlier amendments" is not in the retrieved text (unsupported, although harmless), and it cites the LDV preamble for a negative claim ("the LDV did not change the caps") that the preamble chunk does not actually state.

## Adding a document

**Already indexed:** chunk ids are a hash of the text, so `add_document` first chunks the file and compares ids with the chunks already stored for that law (`source`). Same ids → nothing is embedded; running it a second time returns *"Already indexed: L5/2018 (Ley 5/2018…), 12 chunks with identical text. Nothing was embedded."* If the law is indexed but its text changed (a newer consolidated version), the stale chunks of that law are deleted and only the new ones are embedded, so the index never holds two versions of one law.

**Unanswerable question, q30:** "Within what period must the occupant of a home produce a title justifying their possession when the owner asks a court for immediate recovery of a squatted home?" That procedure is in the Ley de Enjuiciamiento Civil as amended by Ley 5/2018, not in LAU/LDV/LPH.

**Document added:** Ley 5/2018, de 11 de junio (BOE-A-2018-7833), with `uv run python main.py ask "Add the document docs_to_add/BOE-A-2018-7833.html"`. The approval guardrail asked `Approve? [y/N]`, I typed `y`, and 12 new chunks were stored (index: 315 → 327 chunks in the chosen design).

**Before** (base corpus only; `evaluate.py` hides added documents with `CORPUS_BASE_ONLY=1`):
> I don't know: the indexed laws (the Urban Leases Act, the Housing Law, and the Owners' Associations Act) do not cover the specific procedural deadlines for an occupant to justify their possession in a court action for the immediate recovery of a squatted home. That specific procedure is regulated by the Civil Procedure Law (*Ley de Enjuiciamiento Civil*, specifically the summary procedure for illegal squatting under Article 250.1.4º), which is not part of the indexed corpus…

**After:**
> … the court's decree admitting the lawsuit (*decreto de admisión de la demanda*) requires the occupants to provide a title justifying their possessory status (*título que justifique su situación posesoria*) within **5 days** from receiving notice [L5/2018, Artículo único]. If the occupants fail to provide sufficient justification within that 5-day period, the court will issue an order (*auto*) directing the immediate delivery of possession … [L5/2018, Artículo único]. No appeal lies against this court order [L5/2018, Artículo único].

The refusal became a correct, cited answer (full text in `eval/before_after.md`).

## Harness and guardrails

`agent.py` uses LangChain `create_agent` with Gemini (`gemini-3.8-flash`, temperature 0), the two MCP tools loaded over stdio from `server.py`, and `AGENTS.md` as the system prompt.

**AGENTS.md rules** (each with its reason in the file): (1) always search, in Spanish legal terms; (2) answer only from the results; (3) cite every claim as `[LAU, Artículo 9]`, only articles received; (4) if not covered, start with "I don't know: the indexed laws do not cover this", say what is missing and where to look; (5) answer partially and say which part is missing; (6) short, direct answer first, in English, with the Spanish term in brackets; (7) no personal litigation advice; (8) add documents only when the user asks.

**Approval:** middleware `ApproveAddDocument` intercepts every `add_document` call and asks `Approve? [y/N]` in the terminal. Without a terminal (evaluation) it refuses automatically and tells the model nothing was added.

**Call limits:** at most 8 model calls and 6 searches per question, so a confused model cannot loop and burn quota.

**Model fallback:** Gemini Flash often returned 503 "high demand", so `ModelFallbackMiddleware` falls back to `gemini-3.6-flash` and then `gemini-3.5-flash-lite`. After the evaluation, `check.py` showed that `main.py ask` could hang for over 300 s when the main model never answered (504 deadline errors, which do not trigger the fallback). I added a 40 s request timeout (`GEMINI_TIMEOUT`) so a hung request fails and the fallback takes over. Because a timeout does not change what the model answers, `evaluate.py` now caches answers per explicit `AGENT_REVISION` instead of per hash of `agent.py`; the graded answers were re-keyed, not regenerated.

**Extra guardrail: citation check.** After the agent answers, code extracts every `[LAW, Article]` in the answer and checks it against the citations the search tool actually returned in that run; a non-refusal answer must cite at least once. On failure the agent is told what was wrong and gets one retry; if it fails again the answer is withheld and replaced with an "I don't know" that points to boe.es.

**Where it fired (q26):** the first answer cited `[LPH, artículo séptimo; lph]`, a malformed citation not in the search results. The agent was told so, rewrote the answer with valid citations, and passed on the retry. In an earlier run, before I fixed the normaliser, it also fired falsely on `[LAU, Artículo 9.1]` and `[LDV, Artículo 3, k]`; I fixed that by normalising sub-paragraphs to the article.

**Where it fired wrongly:** in the add-document demo the agent's reply (that the document was added) had no citations and was not a refusal, so the check blocked it twice and replaced it with the withheld message, although the document was correctly added. The fix is to skip the citation check when the run made no `search` call (an action, not a legal claim). I did not change `agent.py` after grading, because that would invalidate every cached answer I had graded by hand.

## Evaluation

`main.py evaluate` runs the agent on all 36 questions with the base corpus (answers cached in `eval/answers.jsonl`), then:

**Code checks** (`eval/results.csv`): refusal detected (regex on the start of the answer), number of citations, all citations valid (in the search results), cites an expected article, expected article retrieved, correct refusal / wrong refusal.

**LLM judge** with this rubric (JSON output, temperature 0):
- `correct` = 1 if the answer gives the same key facts as the reference (numbers, deadlines, yes/no, who) with no contradicting fact; for an unanswerable question, 1 only if it says the corpus does not cover it and does not invent the fact.
- `supported` = 1 if every factual claim is stated in the retrieved text (paraphrase is fine); a refusal is supported.

The judge is told to judge only against the reference and the retrieved text, not its own knowledge. Configured judge: `gemini-3.8-flash`; because of 429 quota errors that day, all 36 verdicts were actually given by the fallback `gemini-3.5-flash-lite`.

**Results (36 questions):**

| Metric | Code / judge | My grades |
|---|---|---|
| Correct | 35/36 (28/29 answerable) | 35/36 |
| Unsupported | 0/36 | **12/36** |
| Correct refusals | 7/7 | 7/7 |
| Wrong refusals | 0/29 | 0/29 |
| Citations valid (code) | 36/36 | |
| Cites an expected article (code) | 29/29 | |

**Agreement with the judge** (I graded all 36 in `eval/human_labels.csv`):

| Field | Agreement | Cohen's kappa |
|---|---|---|
| correct | 36/36 (100%) | 1.00 |
| supported | 24/36 (67%) | 0.00 |

On `correct` we agree completely. On `supported` the judge said 1 for all 36, so its kappa is 0: it agrees with me only by chance. My 12 zeros: q05, q13, q14, q15, q18 (the main answer matches the reference, but the agent adds extensions the article does not say: e.g. the LAU distinguishes rent updates from other increases, and requires the need to recover the home to be communicated without expressly requiring writing; the rule on withdrawals from the reserve fund refers to the works in LPH Artículo 10); q23 (extras around an ambiguous question); q27 (the "energy rating A or B" alternative is not in the cited article); q29 (see Failures); q30, q33, q34, q35 (correct "I don't know", but they add explanations from outside the sources, e.g. naming Ley de Enjuiciamiento Civil Article 250.1.4º or the regional ITP tax).

I was deliberately stricter than my own rubric on refusals: the rubric says "a refusal is supported", but a refusal that adds specific law from memory is exactly what rule 2 forbids, so I graded those 0. Even excluding those four refusals, the judge missed 8 unsupported answers. Conclusion: **a flash-lite judge cannot be trusted to measure support**; it checks the headline fact and accepts plausible extra detail. The code checks are reliable but only verify that cited articles were retrieved, not that they say what is claimed.

## Failures

Using my grades (13 answers with correct = 0 or supported = 0):

| Cause | Count | Questions |
|---|---|---|
| Unsupported claim (extra detail not in the passage, main answer right) | 6 | q05, q13, q14, q15, q18, q27 |
| Unsupported claim inside a correct refusal | 4 | q30, q33, q34, q35 |
| Bad test question | 1 | q23 |
| Retrieval miss (leading to a wrong answer) | 1 | q29 |
| Wrong answer from the right passage | 0 | |
| Wrong refusal | 0 | |

- **q29** ("Can I terminate the contract if the landlord will not do repairs, and how long do they have to reply to a quote?"): the agent (answered by the fallback flash-lite) searched once, got Artículos 21, 21 bis, 22 and 23 but not Artículo 27, and then stated that the LAU "does not specifically provide a right to terminate the contract", which is false: Artículo 27.3.a allows it. The repair-deadline half (15 days) was right. The cause is a retrieval miss for the second part (it ignored rule 1, "search each part separately"), made worse by an unsupported negative claim drawn from the absence of evidence. `evaluate.py` first labelled it "wrong answer from right passage" because one of the two expected articles was retrieved; the trace shows the real cause is the retrieval miss.
- **q23** ("I am renting to a company…") is ambiguous: the reference assumes the company is the landlord, but it can be read as the company being the tenant. The agent covered both cases and included the expected answer (so correct = 1), plus unsupported extras. The question should be reworded.
- **Unsupported extras** are the main failure: the model gets the key fact right but "completes" the answer from its own knowledge of Spanish law. Often the extra is true, but the user cannot check it in the cited article, which breaks the promise of the use case.

**What to fix first:**
1. A **support check** in code or with a stronger judge: split the answer into claims and require each to match a sentence of a cited chunk; drop or flag those that do not. This targets 10 of the 13 failures.
2. **Force one search per part** for two-part questions (q29), e.g. ask the model to list the sub-questions before searching.
3. **Avoid flash-lite for answers:** 15 of 36 answers came only from the fallback flash-lite because the main model was overloaded, including q29. Retry the main model with backoff before falling back.
4. Skip the citation check for runs with no search (the add-document false positive), and reword q23.

## Decision

**Would I let users rely on it? Not as a source of final answers.** For the narrow use "find which article of LAU/LDV/LPH covers my situation and give me the gist", yes: 35/36 key facts correct, 7/7 correct refusals, 0 wrong refusals, and every citation points to a real article returned by search, so the user can always open it. But 1 answer in 3 adds details that are not in the cited article, and one answer (q29) told a tenant they lack a right they actually have. Telling a tenant "you cannot terminate" is exactly the costly error from the use case.

**Safeguards for that limited use:** show the cited article text next to the answer (not only the citation) and label the answer "summary, check the article"; keep the citation guardrail; add the support check above before widening use; and keep refusing anything outside the three laws (regional rules, tax, procedure), which it already does well.

**Cost and latency per question** (36 questions, base corpus):

| | Mean | Median | Max |
|---|---|---|---|
| Agent tokens (in / out) | 5,890 (5,369 / 521) | 4,867 | 20,225 |
| Agent seconds | 117 s | 30 s | 689 s |
| Searches | 1.25 | 1 | 3 |
| Judge tokens | 2,831 | | |
| Judge seconds | 1.4 s | | |

Embedding cost is negligible: one query embedding per search (cached), and the index is built once (315 + 243 chunk embeddings). Everything ran on the Gemini free tier, so the actual cost was 0; at paid Flash prices, about 6k tokens per question is a fraction of a cent. Latency is the real problem: an answer itself takes roughly 10–30 s, but the mean of 117 s comes from waiting on 503 "high demand" errors and retries before a fallback model answered. A real deployment would need a paid tier.

## AI use

I used Claude Code (Anthropic) throughout, as allowed (the professor told us AI may now also be used for the report):
- **Code:** Claude wrote most of `index.py`, `retrieval.py`, `server.py`, `agent.py` and `evaluate.py`, and debugged the problems (Gemini embedding batching, MCP 2.x API changes, model availability and 503/429 errors).
- **Corpus and test set:** I chose the use case and the laws; Claude drafted the questions and reference answers from the law texts, which I reviewed. At my request it translated the test set, AGENTS.md and the agent's messages to English.
- **Grading:** the human grades in `eval/human_labels.csv` are mine: I decided each `correct` / `supported` value and the reasons in the notes column; Claude only copied them into the CSV.
- **Report:** Claude drafted this report from the evaluation outputs and my grades and reasons; I reviewed it.
