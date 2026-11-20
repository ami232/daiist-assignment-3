# Assignment 3 Report

- **Name**: Lucía Muñoz Chicote
- **Student ID**: 19445
- **Group**: BBADBA 5B

## Use case

The users are tenants in Spain, often young people renting for the first time, who want to know where they stand before they talk to their landlord: whether they can leave early, whether a rent rise is legal, who pays for a repair. They act on the answer straight away. They might withhold rent, accept a fee or move out. A wrong answer can cost them their deposit or their home, or lead them to give up a right they have. An “I don’t know, ask your regional housing office” only costs them some time. That’s why the system has to answer only from the text of the law, cite the article, and say clearly when the corpus doesn’t cover the question.

## Corpus

Three Spanish state housing laws, consolidated text downloaded from the BOE open-data API (`index.py` does it, no manual step).

| Document | Short name | URL | Version (consolidated text as of) | Licence | Words indexed |
|---|---|---|---|---|---|
| Ley 29/1994, de Arrendamientos Urbanos | LAU | https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003 | 2026-11-13 | BOE open data: reuse allowed citing the source (BOE legal notice; Ley 37/2007 and RD 1495/2011 on reuse of public-sector information) | 24,192 |
| Ley 12/2023, por el derecho a la vivienda | LDV | https://www.boe.es/buscar/act.php?id=BOE-A-2023-12203 | 2026-10-29 | same | 32,298 |
| Ley 49/1960, sobre propiedad horizontal | LPH | https://www.boe.es/buscar/act.php?id=BOE-A-1960-10906 | 2026-10-05 | same | 12,010 |
| **Total** | | | | | **68,500** |

The laws contain no personal data. Document added later through `add_document`: Real Decreto 42/2022 (Bono Alquiler Joven), BOE-A-2022-802, 36,456 words.

## Ingestion

- **Extract.** The BOE API returns XML: one `<bloque>` per article, disposición or preamble, each with `<p class="...">` paragraphs. `parse_boe()` in `index.py` reads it; TÍTULO/CAPÍTULO headings are kept as section context. `parse_generic()` handles PDF (one unit per page), HTML and Markdown (one unit per heading) for `add_document`.
- **Clean.** HTML entities decoded, whitespace normalised, editorial footnotes (`nota_pie`) and signatures dropped, emptied articles ("Sin contenido") skipped.
- **Extraction problem fixed: historical versions.** The consolidated XML keeps *every* version of every article since 1994. Counting all of them the LAU has 85,197 words; the text in force has 24,192, and 47 LAU blocks have more than one version. Indexing all versions would put repealed wording (e.g. the pre-2026 article 20 that let the landlord pass the IBI to the tenant) next to the law in force. Fix: keep only the last `<version>` of each block. A smaller problem: the LDV writes `Artículo\xa01` with a non-breaking space, so its citations didn't match "Artículo 1"; names are normalised.
- **Chunk.** Two designs (see Retrieval): `articles`, one chunk per article, long articles split at paragraph boundaries into pieces of ≤ 300 words; `fixed200`, 200-word windows over the whole law, ignoring structure.
- **Metadata per chunk:** `source` (LAU/LDV/LPH), `title`, `location` (e.g. "Artículo 36", "Artículo séptimo", "Disposición final segunda", "Preámbulo, apartado II"), `locations` (every article a fixed window spans), `part`/`parts`, `section`, `url`, `version_date`, `in_force_since`, `words`. A header like "LAU – Ley 29/1994… – Artículo 36 (parte 1/2)" is embedded with the text.
- **Embed and store.** `gemini-embedding-2`, 768 dimensions, batches of 50, ChromaDB (cosine) in `index/chroma/`, one collection per design. Each batch is saved as soon as it returns and chunk ids are a hash of the text, so `main.py index` embeds only chunks without a saved vector. Query embeddings are cached in `index/query_cache.json`.
- **Number of chunks:** `articles` 343 (LAU 135, LDV 148, LPH 60); `fixed200` 344 (121, 162, 61). Index size 14 MB.

## Test set

I wrote 33 questions in plain language, the way a tenant would ask them, without legal terms. I wrote them myself. For each one I wrote down the law and article that answer it and the correct answer in one sentence. There are three types. 21 are single (one article), across the LAU, LDV and LPH. 6 are multi and need two articles put together (for example, the minimum term when the landlord is a company plus who pays the agency fee). 6 are unanswerable: they sound like housing questions but depend on other laws, such as padrón registration, the Bono Alquiler Joven or regional tax deductions. I wrote the reference answers from what I knew of the LAU. Three of them (q08, q22, q25) turned out to be out of date after the 2026 reform: I found q08 before running the evaluation and q22 and q25 while grading, and corrected all three against the current text.

| Kind | Count |
|---|---|
| single (one article) | 21 |
| multi (two articles) | 6 |
| unanswerable | 6 |
| **Total** | **33** |

Examples:
- **single**, q14: *"I handed back the keys two months ago and haven't got my deposit back. Is there a deadline?"* → LAU, Artículo 36 → one month from returning the keys; after that, legal interest.
- **multi**, q24: *"The landlord is selling the flat. Do I have the right to buy it first? Can the new owner kick me out?"* → LAU, Artículo 25 + Artículo 14.
- **unanswerable**, q29: *"How much is the Bono Alquiler Joven (youth rent subsidy) and how do I apply?"* → set by a royal decree on subsidies, not by the three laws.

## Retrieval

Hit = the expected law and article is in the top k. 27 answerable questions; for multi, a hit means at least one of the two articles, and "all@5" means both.

**A. Searching with the question as written (English):**

| Design | Method | hit@1 | hit@3 | hit@5 | all@5 | Words added to the prompt (k=5) |
|---|---|---|---|---|---|---|
| articles | vector | **0.74** | **0.96** | **1.00** | **0.96** | 989 |
| articles | BM25 | 0.04 | 0.04 | 0.04 | 0.04 | 219 |
| articles | hybrid (RRF) | 0.63 | 0.93 | 1.00 | 0.96 | 1,032 |
| fixed200 | vector | 0.67 | 0.93 | 0.96 | 0.89 | 1,079 |
| fixed200 | BM25 | 0.04 | 0.04 | 0.07 | 0.07 | 192 |
| fixed200 | hybrid (RRF) | 0.56 | 0.93 | 0.96 | 0.89 | 1,078 |

**B. Searching with the query the agent actually sent.** The agent rewrites the English question as a Spanish search, e.g. q14 → *"fianza plazo devolucion devolucion de la fianza arrendamiento"*:

| Design | Method | hit@1 | hit@3 | hit@5 |
|---|---|---|---|---|
| articles | vector | 0.67 | 0.89 | 0.89 |
| articles | BM25 | 0.33 | 0.78 | 0.85 |
| articles | hybrid | 0.74 | 0.89 | 0.89 |
| fixed200 | vector | 0.70 | 0.93 | 0.93 |
| fixed200 | BM25 | 0.41 | 0.67 | 0.81 |
| fixed200 | hybrid | 0.70 | 0.85 | 0.93 |

Chosen: **articles + vector, k = 5** (`retrieval.py`: `SEARCH_DESIGN`, `SEARCH_METHOD`, `SEARCH_K`).

I chunked by article because the article is the unit a tenant needs and the unit the system cites. A fixed-size chunk can cut a rule in half or mix two articles, and then the citation would point to the wrong place. I used vector search instead of keyword search because tenants don’t use the law’s words: they say “leave early”, not “desistimiento”, and “deposit”, not “fianza”. Here the questions are also in English and the law in Spanish, which is why BM25 on the questions as written found almost nothing (4%). With the questions as written (table A), this setup found the right article first in 74% of questions and within the top 5 in 100%, against 67% and 96% for fixed-size chunks with vector search. With the Spanish queries the agent actually sends (table B), the options are within 1–2 questions of each other, so the numbers alone don’t separate them; the citation argument is what decided it. The failures it still has are in multi questions where the second article uses different vocabulary from the question (q26: it found LAU Art. 17 but not the gran tenedor definition in LDV Art. 3).

## Tools and subagent

**`search(query)`** description (docstring in `server.py`):
> Search Spanish housing law: the Ley de Arrendamientos Urbanos (LAU, Ley 29/1994), the Ley por el derecho a la vivienda (LDV, Ley 12/2023) and the Ley de Propiedad Horizontal (LPH, Ley 49/1960), in their consolidated text from the BOE. Use it for any question about renting a home in Spain (contract length, extensions, deposit/fianza, rent updates, stressed-market areas, repairs, ending the contract, selling a rented home) or about owners' communities (comunidad de propietarios, meetings, shared costs, works). Write the query in Spanish with the legal terms if you know them; call it again with other wording if the first results miss. Returns the 5 most relevant passages. Each starts with "Cite as: [SOURCE, location]", the exact label to cite, followed by the law, section, date of the text and BOE link.

**`add_document(path)`** description:
> Add a document to the housing-law index so search can find it. `path` is a local file: a BOE consolidated-law XML (preferred), or a PDF, HTML, TXT or MD file. The file is chunked by article (PDF: by page; HTML/MD: by heading), embedded and stored. If the same document is already indexed with identical text, nothing is embedded. If a document with the same source is indexed but its text changed (e.g. a newer consolidated version), the old chunks are replaced by the new ones, so search never returns two versions of the same law. Returns what was done and how many chunks.

One search result (the agent's query for q14, first of 5):
```
--- Result 1 ---
Cite as: [LAU, Artículo 36] (parte 1/2)
Law: Ley 29/1994, de 24 de noviembre, de Arrendamientos Urbanos | Section: TÍTULO IV Disposiciones comunes | Consolidated text as of 2026-11-13 | https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003
Artículo 36. Fianza.
1. A la celebración del contrato será obligatoria la exigencia y prestación de fianza en metálico en cantidad equivalente a una mensualidad de renta en el arrendamiento de viviendas y de dos en el arrendamiento para uso distinto del de vivienda.
2. Durante los cinco primeros años de duración del contrato, ...
```

**Subagent** (`.claude/agents/corpus-researcher.md`, tool: `mcp__corpus__search` only): searches with Spanish legal terms, up to 3 searches; answers in 3–8 sentences citing every claim with the exact "Cite as" label; if the passages don't answer, starts with "I can't find the answer in the corpus laws (LAU, LDV, LPH)." and says what is missing; flags rules that depend on the contract date, a company landlord / gran tenedor, or a zona tensionada.

**Transcript from Claude Code** (full export in `eval/subagent_transcript.txt`). In Claude Code, opened in the repo folder, `/mcp` showed `corpus` connected with 2 tools; the main session delegated the question to `corpus-researcher`, which answered only from `search` results (3 searches) with the exact citation labels, and listed what it had not retrieved (arts. 9, 10 and 17.6) instead of filling the gaps from memory.

<details><summary>Transcript</summary>

```text
▗ ▗   ▖ ▖  Claude Code v2.1.322
           Opus 5.5 · Claude Team
 ▘▘   ▝▝   ~/Desktop/daiist-assignment-3

  Fable 5.2 is here for your longest and toughest coding tasks. It draws down usage faster than Opus 5.5. Switch with /model.

⏺ Your organization may apply global configuration to Claude Code. These
  settings are centrally managed by your IT administrator.

❯ Use the corpus-researcher subagent to answer: my landlord wants to raise the  
  rent in the middle of the contract, can he?                                   

⏺ corpus-researcher(Mid-contract rent increase question)
  ⎿  Backgrounded agent (↓ to manage · ctrl+o to expand)

⏺ I've passed your question to the corpus-researcher subagent. It's checking the
  indexed BOE texts (the LAU, the 2023 housing law and the LPH) for three
  things: whether rent can change during the contract, raises tied to
  improvement works, and limits at renewal, including in stressed-market areas.
  I'll send you its answer with the article citations when it finishes.

✻ Churned for 7s · done 9:21

› Message from corpus-researcher
  **Short answer:** Mostly no. During the contract, the landlord can only raise
  the rent through the yearly update, and only if the contract provides for one.
  That update is capped by the IRAV index. On top of that, he can raise it for
  improvement works under strict conditions, or if the tenant agrees.

  **Annual update (art. 18 LAU, consolidated text as of 2026-11-13)**
  - The rent can only change once a year, on the anniversary of the contract,
  and only as the parties agreed: "la renta sólo podrá ser actualizada por el
  arrendador o el arrendatario en la fecha en que se cumpla cada año de vigencia
  del contrato, en los términos pactados por las partes" [LAU, Artículo 18].
  - **If the contract says nothing:** there is no update at all. "En defecto de
  pacto expreso, no se aplicará actualización de rentas a los contratos" [LAU,
  Artículo 18].
  - **Which index applies:** if the contract provides for an update but does not
  name an index or method, the rent is updated by "la variación anual del
  Índice de Referencia para la Actualización Anual de los Contratos de
  Arrendamiento de Vivienda (IRAV)" [LAU, Artículo 18].
  - **Cap:** "En todo caso, el incremento producido como consecuencia de la
  actualización anual de la renta no podrá exceder del resultado de aplicar la
  variación porcentual experimentada por el [...] (IRAV)" [LAU, Artículo 18]. So
  even a clause tied to CPI (IPC) or a fixed percentage cannot go above the
  IRAV.
  - The INE (Spain's statistics office) was told to define this index "con el
  objeto de evitar incrementos desproporcionados en la renta" [LAU, Disposición
  adicional undécima].
  - **Procedure:** the new rent can only be charged "a partir del mes siguiente
  a aquel en que la parte interesada lo notifique a la otra parte por escrito,
  expresando el porcentaje de alteración aplicado". The tenant can ask for the
  INE certificate. A note on the previous month's rent receipt counts as notice
  [LAU, Artículo 18].

  **Improvement works (art. 19 LAU)**
  - **Without the tenant's consent:** only after "cinco años de duración del
  contrato, o siete años si el arrendador fuese persona jurídica" (a company or
  other legal entity). The increase is the money invested × the legal interest
  rate + 3 points, "sin que pueda exceder el aumento del veinte por ciento de la
  renta vigente". Public subsidies must be deducted from the amount invested,
  and the contract can exclude this right ("salvo pacto en contrario") [LAU,
  Artículo 19 (parte 1/2)].
  - **When it applies:** from the month after the landlord's written notice,
  which must show the calculation and include copies of the cost documents [LAU,
  Artículo 19 (parte 1/2)].
  - **With the tenant's consent:** at any time, improvement works can be done
  and the rent raised "previo acuerdo entre arrendador y arrendatario", without
  interrupting or restarting the compulsory extension (art. 9) or the tacit
  extension (art. 10). The works must go beyond the landlord's ordinary repair
  duty under art. 21 [LAU, Artículo 19 (parte 2/2)].
  - **Related:** if the tenant has to put up with improvement works, the rent
  goes down in proportion to the part of the home they cannot use [LAU, Artículo
  22].

  **Extensions (prórroga) and new contracts in stressed areas (zona
  tensionada)**
  - Art. 19.4 says an agreed increase does not interrupt "el periodo de prórroga
  obligatoria [...] o de prórroga tácita" [LAU, Artículo 19 (parte 2/2)]. This
  suggests the extensions run under the same contract and the same rent rules
  (the annual update only).
  - **Gap:** I did not retrieve the text of arts. 9 and 10, so I cannot quote a
  rule that expressly bans renegotiating the rent at extension.
  - **Large landlord (gran tenedor) in a declared zona tensionada:** the
  starting rent of a *new* contract cannot exceed the reference price index, and
  extra charges cannot be passed on to get around that cap [LAU, Artículo 17
  (parte 4/5)].
    - This only applies to contracts signed after Ley 12/2023 came into force
  and once the index system is approved [LAU, Disposición transitoria séptima].
    - The same cap applies to a home not rented as a primary residence in the
  last five years, if the ministry's resolution says so [LAU, Artículo 17 (parte
  5/5)].
  - **New contract above the previous rent:** it can only go beyond the old
  contract's annual update by up to 10% over the last rent of the previous five
  years, and only in listed cases: recent renovation, an energy-saving
  improvement of 30%, accessibility works, or a contract of 10 years or more
  [LAU, Artículo 17 (parte 3/5)].
  - **Successive temporary (short-stay) contracts:** cannot increase the rent by
  more than the IRAV per year [LAU, Artículo 17 (parte 5/5)].
  - **How zones are declared:** by the housing authority, for three years,
  renewable every year [LDV, Artículo 18 (parte 3/5)].
  - **Whether these rules apply depends on three things:** whether the zone is
  declared, whether the landlord is a gran tenedor, and when the contract was
  signed.

  **What the corpus doesn't cover / where I'm uncertain**
  1. I did not retrieve the general rule of art. 17.6 (the cap for a new
  contract on a home in a zona tensionada, any landlord). I only have its
  exceptions, quoted above.
  2. The retrieved passages say nothing about the temporary 2% (2023) and 3%
  (2024) caps on annual updates. They also don't give a specific reform name or
  date. The consolidated LAU dated 2026-11-13 simply shows the IRAV as the
  default index and the cap, which is the version in force as of November 2026
  as far as the corpus shows.
  3. I did not retrieve arts. 9 and 10 (contract length and extensions).
  4. The actual IRAV figures, which zones are declared, and the gran tenedor
  definition are not in the passages I retrieved. Regional rules and the
  tenant's own contract clause would also need checking.

  I stopped at 3 searches. More searches on arts. 9, 10 and 17.6 would close
  gaps 1 and 3.

⏺ Mostly no. Under the LAU, the rent can't simply be renegotiated partway
  through the contract. During the contract there are only three ways it can go
  up:

  1. The yearly update, and only if the contract provides for one (art. 18 LAU)
  - It can only happen once a year, on the contract's anniversary, "en los
    términos pactados por las partes."
  - If your contract says nothing about updates, the rent can't be updated at 
    all: "En defecto de pacto expreso, no se aplicará actualización de rentas."
  - The rise can never exceed the IRAV, the official index that the INE (Spain's
    national statistics office) publishes for updating rental contracts. This
    holds even if your contract ties the update to IPC (inflation) or a fixed
    percentage.
  - He must tell you in writing and state the percentage. The new rent only
    applies from the following month, and you can ask for the INE certificate. A
    note on the previous month's rent receipt counts as notice.

  2. Improvement works (art. 19 LAU)
  - Without your consent: only after the contract has lasted 5 years (7 if the
    landlord is a company). The rise is the amount invested × the legal interest
    rate + 3 points, capped at 20% of the current rent.
    - Any public subsidies he received must be subtracted from the investment.
    - He must notify you in writing, showing the calculation and enclosing
      copies of the cost documents.
    - The contract can rule this out entirely.
  - With your consent: at any time, for works that go beyond ordinary repairs.
    Agreeing to this doesn't restart your extension periods.
  - While works are going on, your rent goes down in proportion to the part of
    the home you can't use (art. 22).

  3. You agree to it. Nothing obliges you to accept a mid-contract increase
  outside the two routes above.

  Stressed-market areas (zonas tensionadas, art. 17). These rules cover new
  contracts, not your current one. In a declared zone, a landlord who owns many
  properties (a gran tenedor) can't set a new contract's starting rent above the
  official reference price index. Whether this matters for you later depends on
  whether your area is declared, whether he counts as a gran tenedor, and when
  the contract was signed.

  What to do: check your contract for an update clause. If there's none, he
  can't raise the rent. If there is one, the annual rise is capped at the IRAV
  and needs written notice.

  What the subagent didn't confirm:
  - It didn't retrieve arts. 9 and 10 (contract length and extensions). It
    infers that the rent can't be renegotiated at an extension, but it has no
    text that says so expressly.
  - It didn't retrieve the general cap in art. 17.6 that applies to any landlord
    in a zona tensionada.
  - The corpus doesn't contain the current IRAV figures, the list of declared
    zones, or the definition of gran tenedor. Regional rules may also apply.

  This is a reading of the state law in the corpus, not legal advice for your
  situation. I can send the subagent back to search arts. 9, 10 and 17.6 to fill
  those gaps.

✻ Worked for 10s · done 9:22

⏺ Agent "Mid-contract rent increase question" finished · 30s
```

</details>

## Adding a document

- **Already indexed:** chunk ids are a hash of their text. If every chunk of the file is already stored, `add_document` embeds nothing and says "Already indexed … unchanged". If the same source is stored but its text changed (a newer consolidated version from the BOE), the new chunks are embedded and the old ones deleted, so search never shows two versions of one law. Tested: adding `corpus/BOE-A-1960-10906.xml` (LPH) again → *"Already indexed: LPH (…), 60 chunks, unchanged. Nothing was embedded."*
- **Unanswerable question:** q29, Bono Alquiler Joven. **Document added:** Real Decreto 42/2022 (BOE-A-2022-802), 219 chunks. The daily limit of 1,000 embeddings stopped it after 150 chunks; those were kept, and the rest were embedded the next day without re-embedding anything (`add_document_demo.py`).
- **Before:** *"I can't find the answer in the corpus laws (LAU, LDV, LPH). The provided laws do not contain details about the amount or application process for the Bono Alquiler Joven, and you should consult your comunidad autónoma's housing department, official government portals, or an information office for assistance."*
- **After:** the search now returns only Real Decreto 42/2022 passages (Artículos 1, 8, 11, 30 and the Preámbulo), and the answer gives the amount: *"the state regulations set the Bono Alquiler Joven at **250 euros per month** for a period of two years (up to 6,000 euros in total), provided the applicant meets income limits and rent caps [BOE-A-2022-802, Preámbulo, Artículo 8, Artículo 11]"*, and says that the application itself is handled by each comunidad autónoma. It still opens with the refusal sentence ("I can't find the answer in the corpus laws (LAU, LDV, LPH)..."), because `AGENTS.md` and that sentence describe the corpus as three fixed laws; after an `add_document` the prompt should describe the corpus as whatever is indexed. Full output: `eval/add_document_demo.md`.
- **add_document result:** *"Replaced BOE-A-2022-802 (...): 219 chunks in the index (69 newly embedded, 150 reused, 0 outdated chunks removed)."*

## Harness and guardrails

`agent.py`: LangChain `create_agent` on `gemini-3.5-flash-lite` (fallback `gemini-flash-lite-latest` when the first is overloaded; `gemini-2.5-flash` is no longer offered to new API keys), with the tools of `server.py` over MCP stdio and `AGENTS.md` as the system prompt.

- **AGENTS.md rules (each with its reason in the file):** search before answering; answer only from the search results; cite every claim with the exact label; when not covered, start with the fixed refusal sentence and say what is missing; answer partly when only part is covered; flag conditions (contract date, company landlord, zona tensionada); be short, no personal legal advice; `add_document` only on request.
- **Approval:** `HumanInTheLoopMiddleware` interrupts every `add_document` call. In a terminal it asks "Approve? [y/N]"; with no terminal (evaluation, CI) it rejects. Example: *"Añade al índice el archivo corpus/BOE-A-1960-10906.xml"* → `[approval] add_document(...) rejected: no human at the terminal.` → the agent replied that the file was not added because the call was not approved.
- **Call limits:** at most 8 model calls and 4 searches per question.
- **Extra guardrail: citation check.** After the agent answers, code checks that every `[SOURCE, location]` it cites is a passage `search` returned in that run, and that an answer that isn't a refusal cites something. If not, the agent gets one chance to fix it with the list of valid labels; if it still fails, the answer is replaced by a refusal. Paragraph references ("Artículo 21.4") count as their article.
- **Where it fired:** in the first evaluation run, q21 (tourist flats): the agent wrote `[LPH, Artículo séptimo, LPH, Artículo diecisiete]` in one bracket, the check didn't recognise it, asked for a repair, and the repaired answer passed. q10 (broken tap): the agent cited `[LAU, Artículo 21.4]` and the first version of the check only accepted "Artículo 21", so it fired twice and replaced a correct answer with a refusal: the guardrail itself caused a wrong refusal. The parser was fixed (paragraphs, several citations per bracket) and all answers regenerated; in the final run it did not fire. Limitation, seen in q26: it checks that the cited article was *retrieved*, not that the claim is *in* that article.

## Evaluation

`main.py evaluate` runs everything; results are in `eval/` (`retrieval_results.csv`, `retrieval_agent_queries.csv`, `answers.jsonl`/`answers.csv`, `judge.csv`, `results.csv`, `summary.md`/`summary.json`).

**Code checks** (per answer, in `results.csv`): refused or not vs. the question kind (correct refusal, wrong refusal, answered an unanswerable question); every citation is a retrieved passage; the answer cites the expected article; the expected article was retrieved at all; whether the guardrail fired.

**LLM judge** (`gemini-3.5-flash-lite`), given the question, its kind, the reference answer, the agent's answer and, as evidence, the exact passages the agent retrieved. Rubric:
- *correct* 1/0: same key facts as the reference (numbers, deadlines, who does what, conditions); for multi, both parts; for unanswerable, 1 only if it says the laws don't cover it and doesn't guess.
- *supported* 1/0: every factual claim appears in the evidence (paraphrase OK); a pure refusal is supported.

I’m keeping the rubric: correct (1/0) and supported (1/0), with a note for every 0. Splitting them separates two different risks. An answer can be right but include things that aren’t in the retrieved article (q06), and for a legal assistant that’s still a problem, because the tenant can’t check where it comes from. Binary scores also make it easier to compare my grades with the judge’s. One limit: it doesn’t score form (language mixing, the line in Arabic), so I record those as quality notes alongside.

**Agreement with my grades** (33 answers in `eval/human_labels.csv`, graded before reading the judge):

| | Agreement | Cohen's κ | Disagreements |
|---|---|---|---|
| correct | 100% | 1.00 | none |
| supported | 88% | 0.00 | q06, q11, q20, q26 |

The judge marked all 33 answers *supported*; I found 4 with claims that are not in the retrieved text. The 88% only reflects that 29 of 33 really were supported; κ = 0 shows the judge adds nothing beyond "always 1" on this criterion.

**Results (final run, articles + vector):**

| Result | Count |
|---|---|
| Correct (of 27 answerable) | 26 |
| Incorrect (answerable) | 1 (q11) |
| Unsupported (my grades) | 4 (q06, q11, q20, q26) |
| Correct refusals (of 6 unanswerable) | 5 |
| Answered an unanswerable question | 1 (q31, see Failures) |
| Wrong refusals | 0 |
| Invalid citations | 0 |

## Failures

Data for each case (from `results.csv`, my notes and the trace):

| Id | What went wrong | Expected article retrieved? | My note |
|---|---|---|---|
| q11 (knock down a wall) | Answered with LPH rules for owners, missed the landlord's written consent | No: the agent searched owners'-community wording; LAU art. 23 never came back | cites LPH instead of LAU Art 23, applies an owner rule to the tenant |
| q06 (pay day / 3 months upfront) | Adds "total upfront can't exceed 3 months" by summing deposit + guarantee itself | Yes | mixes guarantees with paying rent in advance |
| q20 (noisy neighbours) | Says eviction "for up to three years" | Yes (LPH art. 7) | misreads the 3-year penalty |
| q26 (landlord with 15 flats) | States the "more than 10 properties" definition without retrieving LDV art. 3 | LAU 17 yes, LDV 3 no | definition never retrieved |
| q31 (home insurance) | Didn't use the refusal sentence; said the laws don't require it and cited LAU art. 36, which does forbid requiring non-payment insurance | n/a | graded correct by me and the judge |
| q25 (damp) | Correct, but the answer starts with a meaningless line in Arabic | Yes | quality issue |
| q08, q22, q25 references | Reference answers outdated by the 2026 LAU reform; the agent was right, the reference wrong | | corrected |

| Category | Cases | Count | Why |
|---|---|---|---|
| Retrieval miss | q11, q26 | 2 | q11: it searched the LPH and never retrieved LAU Art. 23, so it could not give the key fact (the landlord’s written consent). q26 (main cause): it never retrieved LDV Art. 3. |
| Wrong answer from the right passage | q20 | 1 | It had LPH Art. 7 but mixed two different penalties and said “eviction for up to three years”. |
| Unsupported claim | q06 (+ q26) | 1 (+1) | q06: the article was right, but the “3 months in total” rule is its own sum of deposit and guarantee and is not written in the law. q26 also filled the gap from the missing LDV Art. 3 with the “gran tenedor” definition from its own knowledge (counted once, under retrieval miss). |
| Wrong refusal | — | 0 | |
| Bad test question | q31, q08, q22, q25 | 4 | q31: I marked it unanswerable, but LAU Art. 36 forbids requiring non-payment insurance; the agent got it right, said that part and said the rest is not covered. q08, q22, q25: my references were outdated after the 2026 reform; the agent was right because it uses the text in force. |
| **Total** | | **8** | 4 system failures, 4 test-set errors |

Quality notes (not failures of content): wrong answer language in q18, q21, q29, q30; a meaningless Arabic line at the start of q25; the typo “PHS” for LPH in q32.

What I’d fix first is retrieval, because it’s behind the only incorrect answer (q11: it searched the LPH and missed LAU Art. 23 on landlord consent) and behind q26. Two concrete changes: a filter or boost for the LAU when the question is about the tenant–landlord relationship, and, for multi questions, a second search on the concepts the first article mentions but doesn’t define (such as “gran tenedor”). After that, I’d force the answer language to match the question, which is cheap and fixes four cases.

## Decision

Cost per question (33 questions, final run): **5,689 tokens** on average (input + output, all model calls), **6.0 s** on average, 11.7 s max; 1–3 model calls and 1–2 searches per question, one query embedding per new search. On the free tier this costs 0 €, limited by 15 requests/minute per model and 1,000 embeddings/day.

I would let people rely on it, but only as a first step to understand their rights, not as a substitute for legal advice. With 32/33 correct, and 5 of 6 unanswerable questions refused (the sixth, q31, was partly answerable from LAU Art. 36), it’s reliable for direct questions about the LAU. It also did better than my own reference answers on the 2026 reform, because it reads the current BOE text. The supported score (29/33) shows it sometimes adds things that aren’t in the article, so I’d require three protections: every answer shows the article text it’s based on, so the tenant can check it; it says “I don’t know” instead of guessing when nothing relevant comes up; and when the answer leads to an action with consequences (not paying, leaving the flat, going to court) it recommends confirming with the housing office or a lawyer.

## AI use

I used Claude Code (Anthropic) as a coding assistant throughout the assignment.

- **Code:** Claude wrote the code (`index.py`, `retrieval.py`, `server.py`, `agent.py`, `evaluate.py`, `add_document_demo.py`, `AGENTS.md` and the subagent file) and debugged it with me: the BOE XML keeping old versions of each article, the embedding batch error, the Gemini models that were unavailable or overloaded, the free-tier rate and daily quota limits, and the incompatibility of `langchain-mcp-adapters` with the current MCP library.
- **Options, not decisions:** for each choice it gave me options with pros and cons and I picked: the corpus (I changed from US supplement regulation to Spanish housing law because it interested me more), English questions, articles + vector, and keeping the rubric.
- **Checking my work:** it checked my reference answers against the current BOE text and showed me where they didn’t match; I decided to correct q08, and found q22 and q25 myself while grading. It also compared my written sections with the results and pointed out two things that didn’t match the data (q31 was not refused; table B), which I fixed.
- **Report:** it filled in the factual parts (corpus table, ingestion, retrieval tables, tool descriptions, guardrails, results, cost) from the code and the evaluation output.
- **Mine:** the use case, the 33 questions and reference answers, my 33 grades and notes (graded before seeing the judge), the design choice, the rubric decision, the failure classification, what to fix first, and the decision. The system itself uses Gemini (embeddings, agent, judge); I did not use it to write anything.
