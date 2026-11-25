# Assignment 3 Report

- **Name**: Adolfo Gutierrez de Gandarilla Domínguez
- **Student ID**: 19003
- **Group**: BBADBA 5B

## Use case

**Who asks.** Staff of Spanish sports clubs, federations and event
organisers who are not lawyers: club managers, team delegates, federation
administrators, organisers of a race or a match. They ask practical questions
about their legal obligations, for example *"¿Qué sanción tiene un club si sus
aficionados lanzan objetos al campo?"*, *"¿Puede un deportista negarse a un
control de dopaje fuera de competición?"* or *"¿Qué requisitos tiene una
competición para ser oficial?"*. Questions and answers are in Spanish, like
the laws.

**What they do with the answer.** They decide what to do next: prepare a
document, accept or refuse a request, warn an athlete, or call the
federation's lawyer.

**What a wrong answer costs compared with "I don't know".**

| Answer | What happens | Rough cost |
|---|---|---|
| Correct, with citation | They act correctly and can check the article cited | Saves a lawyer's consultation (~€150) |
| **"The laws I have don't answer this, ask a lawyer / the federation"** | One consultation with a lawyer or the federation | **~€150 and a few days** |
| **Wrong but confident** | They act on it: an event without the required measures, a missed deadline, an athlete told something false about doping controls | **Fines from a few thousand to hundreds of thousands of euros, a club sanctioned, an athlete banned for years** |

A confident wrong answer is **far worse** than a refusal, so the assistant
must **only answer from the text of the laws, cite the article for every
claim, and say "I don't know" whenever the laws it has don't cover the
question**. A useful refusal is a success, not a failure. This is why the
evaluation counts wrong answers and unsupported claims separately from
refusals, and why the ship decision looks first at how often it makes things
up.

**What it is not.** It is not legal advice and it doesn't know case law,
regional laws or federation rules, only the three national laws below.

## Corpus

Three Spanish national laws on sport, downloaded as **consolidated
text** (the current version, with all amendments applied) from the open-data
API of the *Boletín Oficial del Estado* (BOE). The API returns the law already
divided into blocks (preamble, headings, articles), each with its title.

| Document | BOE identifier and URL | Published | Consolidated text updated | Licence | Words (current text, without preamble) |
|---|---|---|---|---|---|
| Ley 39/2022, de 30 de diciembre, del Deporte | [BOE-A-2022-24430](https://www.boe.es/buscar/act.php?id=BOE-A-2022-24430) | 31/12/2022 | 19/11/2026 | Not subject to copyright; BOE reuse conditions | ~40,700 |
| Ley Orgánica 11/2021, de 28 de diciembre, de lucha contra el dopaje en el deporte | [BOE-A-2021-21650](https://www.boe.es/buscar/act.php?id=BOE-A-2021-21650) | 29/12/2021 | 20/12/2025 | Not subject to copyright; BOE reuse conditions | ~28,700 |
| Ley 19/2007, de 11 de julio, contra la violencia, el racismo, la xenofobia y la intolerancia en el deporte | [BOE-A-2007-13408](https://www.boe.es/buscar/act.php?id=BOE-A-2007-13408) | 12/07/2007 | 19/12/2025 | Not subject to copyright; BOE reuse conditions | ~14,400 |
| **Total** | | | | | **~83,800** |

**Licence.** Laws and regulations are **excluded from copyright** in Spain
(article 13 of the *Ley de Propiedad Intelectual*: *"No son objeto de
propiedad intelectual las disposiciones legales o reglamentarias…"*), and
the BOE allows its content to be reused provided the source and the date of
the version are cited. The texts contain **no personal data** (only the
names of the King and the ministers who signed them, in the signature block,
which I drop).

**Why these three.** Together they cover the main legal obligations of a
club or federation: how sport is organised (licences, competitions,
federations, sports justice), anti-doping (controls, sanctions, health of
athletes), and violence and racism at events (security measures, sanctions
for clubs and spectators).

**Why I leave out the preambles.** The preamble explains *why* the law was
made but contains no binding rule. It mentions many of the topics without
stating the rule, so it would compete with the actual articles in the search
and could lead to unsupported answers. It also saves embedding quota.
Including the preambles, the three texts have ~100,700 words.

## Ingestion

**Extract.** `index.py` downloads each law from the BOE open-data API
(`/datosabiertos/api/legislacion-consolidada/id/{BOE id}/texto`) as XML. The
XML is already split into blocks (*preámbulo*, *encabezado* for Título and
Capítulo headings, *precepto* for articles and *disposiciones*), and each block
keeps every historical version. I keep **only the latest version** of each
block, and **only the articles and disposiciones**: the preamble, signatures
and initial note are dropped.

**Clean.**
- **BOE editorial notes removed.** The consolidated text contains 13 notes
  written by the BOE about amendments (e.g. *"Se añade una letra f) al
  apartado 1 por la disposición final 8.1 de la Ley 4/2023…"*). They are not
  law and would add dates and article numbers that don't apply, so I drop
  `<blockquote>` notes without a class. I keep the one marked "always show",
  which says that the *Comité Español de Disciplina Deportiva* was abolished.
- **Unicode normalisation.** Article titles contain a non-breaking space
  ("Artículo\xa01"), so "Artículo 1" in a question or in my test set did not
  match the metadata. NFKC normalisation and whitespace collapsing fix it.
- **One extraction problem I fixed: article 33 of Ley 19/2007** is titled
  *"Articulo 33"* (without the accent) in the BOE, so my first version stored
  its location as the whole title. The parser now accepts both spellings, and
  `main.py index` deletes the outdated chunk and embeds the corrected one.

**Chunk metadata.** Every chunk stores `source` (short name of the law, e.g.
*LO 11/2021 de lucha contra el dopaje en el deporte*), `location` (e.g.
*Artículo 15 (parte 2/2)*), `articles` (the articles it contains, used to
score retrieval) and `words`. The text of each chunk starts with the law's
name and, in the article design, the Título > Capítulo > article title, so the
embedding knows the context of the paragraph.

**Two chunkings** (compared in *Retrieval*):

| Design | How | Chunks | Median words |
|---|---|---|---|
| **article** | One chunk per article; articles longer than 350 words are split at paragraph ends into "parte 1/n, 2/n…" | **384** | 227 |
| **fixed** | 300-word windows over each law in order, 50 words overlap, ignoring article boundaries | **308** | 304 |

**Embedding and storage.** `gemini-embedding-2`, 768 dimensions, task type
`RETRIEVAL_DOCUMENT` for chunks and `RETRIEVAL_QUERY` for questions, stored
in ChromaDB in `index/` (one collection per design, cosine distance, 15 MB).
Each batch of 20 is stored as soon as it arrives; a chunk's id is a hash of
its design, source, location and text, so `main.py index` only embeds chunks
that don't have a saved vector yet. Rebuilding everything costs ~692
embeddings; a rerun costs 0. **A problem I hit:** passing a plain list of
strings to `gemini-embedding-2` returned **one** vector for 20 texts (it
treats the list as one multimodal input). I now send one `Content` per text
and check that the number of vectors equals the number of texts.

## Test set

I wrote the questions from the text of the laws, **before** running any
retrieval, imagining what a club manager, team delegate or federation
administrator would actually ask. For every answerable question I looked up
the article and wrote the reference answer from its text. For the
unanswerable ones I searched the three laws for the key words first, to make
sure they really are not covered, and kept them **close to the topic**.

| Kind | First set (q01–q35) | Colloquial set (q36–q44) | Total |
|---|---|---|---|
| single (one article) | 22 | 2 | 24 |
| multi (two articles, sometimes from two different laws) | 6 | 3 | 9 |
| unanswerable | 7 | 4 | 11 |
| **Total** | **35** | **9** | **44** |

By law, first set: 11 questions on the Ley del Deporte, 11 on the anti-doping
law and 8 on the violence law (multi questions counted under each law they use).

**Colloquial set (q36–q44), added after the first evaluation.** The first set
shares the law's vocabulary, because I wrote it from the articles. To test
that weakness I added 9 questions phrased the way a player or club employee
would say them (*"rajando del árbitro"*, *"no le tramitan la ficha"*,
*"le cierran el estadio"*), about contracts, image rights, agents, injuries,
security and licences. Five of them are only **partly** covered by the laws
(e.g. q43: the deadline for a licence is there, the appeal route is not), so
they also test rule 4 (answer the covered part and say what is missing).
Because they were written after the design was chosen, I report them
separately where it matters.

**Two examples:**

- **multi, q24:** *"¿Cuánto tiempo hay para sancionar una infracción
  disciplinaria muy grave y una infracción de dopaje?"* → needs the Ley del
  Deporte, art. 112 (**3 years**) **and** the anti-doping law, art. 33
  (**10 years**). An answer from one passage only would be half right.
- **unanswerable, q35:** *"¿Qué indemnización mínima cubre el seguro
  obligatorio deportivo en caso de fallecimiento?"* → the Ley del Deporte
  (art. 23) **requires** the insurance but leaves the minimum amounts to a
  future regulation, which is not in the corpus. A good assistant should say
  that the insurance is mandatory but that the amount is not in these laws,
  not invent a figure.

## Retrieval

**Metric.** For each answerable question, a hit at k means that one of
the top-k chunks comes from the expected law **and** contains the expected
article. For the multi questions I also report whether **both** expected
articles are in the top k. Question vectors are computed once and cached in
`eval/query_vectors.json`, so every design is compared on the same vectors.
Retrieval is scored on the question as the user wrote it (one search), not on
the agent's own queries.

First set (28 answerable questions; this is what I chose the design on):

| Design | Hit@1 | Hit@3 | Hit@5 | Multi, both passages @5 | Words added to the prompt @1 / @3 / @5 |
|---|---|---|---|---|---|
| Fixed 300-word windows, vector search | 82% | 96% | 100% | **83%** | 307 / 922 / 1,537 |
| **One chunk per article, vector search** | **93%** | **100%** | **100%** | 67% | **251 / 779 / 1,310** |
| One chunk per article, hybrid (vector + BM25 keywords, reciprocal rank fusion) | 64% | 79% | 82% | 67% | 253 / 801 / 1,334 |

With the colloquial set (33 answerable questions, `eval/retrieval_results.csv`):

| Design | Hit@1 | Hit@3 | Hit@5 | Multi, both passages @5 | Words @1 / @3 / @5 |
|---|---|---|---|---|---|
| Fixed 300-word windows, vector search | 79% | 94% | 97% | **78%** | 307 / 922 / 1,536 |
| **One chunk per article, vector search** | **82%** | 94% | 97% | 67% | **248 / 787 / 1,322** |
| One chunk per article, hybrid | 58% | 76% | 76% | 44% | 267 / 802 / 1,349 |

**What the numbers say.**

- **Chunking by article wins.** On the first set it puts the right article
  first 93% of the time and always within the top 3, with 15% fewer words in
  the prompt. A legal question is almost always about one article, so a chunk
  that is exactly one article is the right unit. Fixed windows cut articles in
  two and mix neighbouring articles, so the right one is more often 2nd–5th.
- **Colloquial questions are harder, as expected.** With them, hit@1 drops
  from 93% to 82% and the advantage over fixed windows shrinks to 3 points;
  at k = 3 and 5 the two designs tie. Of the 5 new answerable questions only
  q44 has its article first: q36 (image rights, art. 22) is 4th, behind
  articles about *"derechos de comercialización"*, and q42 (organiser's duties,
  Ley 39/2022 art. 86) is not in the top 5 at all, because the question talks
  about *"seguridad"* and *"control de accesos"* and the five passages about
  security in the violence law win. Article chunking is still the better or
  equal design, so I keep it, but the first set overstated retrieval quality.
- **Hybrid search made it worse**, which I didn't expect, so I checked that it
  is not a bug. In the 6 first-set questions that hybrid misses at k = 5 (q04,
  q08, q11, q17, q18, q24), the expected article is **1st or 2nd in the vector
  ranking** but only 19th–69th in the keyword ranking (q08: not at all,
  *"cerveza"* never appears in art. 4, which says *"bebidas alcohólicas"*). Reciprocal rank
  fusion scores a chunk 1/(60 + rank) in each list, so the vector's 1st place
  alone is worth 1/61 = 0.016, while a chunk that is 9th in the vector list and
  3rd by keywords gets 1/69 + 1/63 = 0.030 and pushes it out of the top 5
  (q04: art. 44 is vector 1st; the top 5 are all chunks ranked 4th–14th in
  both lists). Fusion rewards chunks that both rankings find "fairly good" over
  one that the better ranking finds best. Keyword search alone is weak here
  (hit@1 50%, hit@5 64% on the first set; 42% and 58% with the colloquial
  set) because: (1) there is no stemming, so *"¿Cuándo
  **prescribe**…?"* doesn't match *"**prescribirán**"* / *"**prescripción**"*
  in art. 112, and the keyword ranking prefers arts. 104–108, which repeat
  *"infracción muy grave"* many times; (2) legal vocabulary (*sanción,
  infracción, deportista*) appears in dozens of articles; (3) users use
  everyday words (*cerveza, estadio*) where the law uses legal ones.
- **Where article chunking fails: two multi questions** (q23, q27). Both ask
  for a sanction *and* a fine; the sanction article (21 or 22) is found but
  the fines article (24) is not in the top 5. Fixed windows do better here
  (83%) because one window can span two neighbouring articles. The agent can
  compensate by searching once per part of the question.

**Chosen design: one chunk per article, vector search, k = 5.** Best hit@1,
best or equal hit@3 and hit@5, and fewest words per result. Hit@3 was 100% on
the first set, but I kept k = 5 as a margin for differently phrased real
questions, and the colloquial set justified it: q36 is only found at rank 4.
It adds ~530 words (~700 tokens) per search.

## Tools and subagent

**MCP server (`server.py`, stdio)** with two tools. It loads `index/` once at
startup and never re-embeds the corpus.

- **`search(query)`**: *"Search Spanish national sports law: Ley 39/2022 del
  Deporte, Ley Orgánica 11/2021 de lucha contra el dopaje en el deporte, Ley
  19/2007 contra la violencia… Use it for any question about licences,
  competitions, clubs and federations, athletes' rights and duties, doping
  controls and sanctions, or security and sanctions at sports events. Write the
  query in Spanish… for a question with two parts, search once per part.
  Returns the 5 most relevant passages, each headed by [n] law — article…
  Cite the law and article of every passage you use. If none of them answers
  the question, the laws indexed don't cover it."*
- **`add_document(path)`**: *"Add one document to the searchable index: a BOE
  consolidated-text XML, a PDF, an HTML page or a text file… If exactly the
  same content is already indexed, nothing is added. If a document with the
  same name was indexed with different content, its old passages are replaced…
  Returns what happened."*

The descriptions say **when** to use each tool, **in which language** to
query, and **what comes back**, because the model only sees the description.
Saying that the results name the law and the article is what makes the model
cite them.

**One search result** (first of 5, cut), for *"¿Se puede vender cerveza en un estadio?"*:

```
[1] Ley 19/2007 contra la violencia en el deporte — Artículo 4
… CAPÍTULO I Responsabilidades y obligaciones de personas organizadoras… >
Artículo 4. Consumo y venta de bebidas alcohólicas y de otro tipo de productos.
1. Queda prohibida en las instalaciones en las que se celebren competiciones
deportivas la introducción, venta y consumo de toda clase de bebidas
alcohólicas y de drogas tóxicas, estupefacientes o sustancias psicotrópicas.
```

**Subagent** (`.claude/agents/corpus-researcher.md`): its only tool is
`mcp__corpus__search`. Its description lists the three laws and the topics to
delegate, so the editor knows when to use it. Its instructions repeat the core
rules: search in Spanish, once per part, at most 4 searches; answer only from
the passages; cite law and article; copy figures exactly; start a refusal with
"Las leyes consultadas no cubren esta pregunta."

**Transcript from my editor** (Claude Code, the main agent delegated the
question to `corpus-researcher`; the subagent used only `mcp__corpus__search`):

> **User:** Usa el subagente corpus-researcher: ¿Qué multa corresponde a una
> infracción muy grave de la ley contra la violencia en el deporte?
>
> **Tool call:** `mcp__corpus__search("multa infracción muy grave violencia en el deporte")`
>
> **corpus-researcher:** La Ley 19/2007 prevé dos regímenes distintos para las
> infracciones muy graves, cada uno con su multa:
>
> - Régimen sancionador (Título II). La sanción económica por infracciones muy
>   graves es "De 60.000,01 a 650.000 euros" (Ley 19/2007, Artículo 24). Los
>   organizadores también pueden ser sancionados con inhabilitación para
>   organizar espectáculos deportivos o con clausura temporal del recinto, en
>   ambos casos "hasta un máximo de dos años". A las personas físicas se les
>   puede prohibir el acceso a cualquier recinto deportivo "por un período entre
>   dos años y cinco años" (Ley 19/2007, Artículo 24).
> - Régimen disciplinario deportivo (Título III). Aquí la sanción pecuniaria
>   para clubes, deportistas, jueces, árbitros y directivos es "de 18.000,01 a
>   90.000 euros" en competiciones profesionales y "de 6.000,01 a 18.000 euros"
>   en el resto de competiciones (Ley 19/2007, Artículo 36). Además se pueden
>   imponer, entre otras sanciones, la inhabilitación o suspensión de licencia
>   "por un período de dos a cinco años", la clausura del recinto "desde cuatro
>   partidos o encuentros hasta una temporada", la pérdida de puntos o el
>   descenso de categoría (Ley 19/2007, Artículo 36). Las conductas que cuentan
>   como infracciones muy graves en este régimen se enumeran en (Ley 19/2007,
>   Artículo 34).
>
> La cifra aplicable depende de en qué régimen se tramite la infracción. Los
> pasajes recuperados no explican qué criterio decide entre uno y otro.

What it shows:
- **One search**, because the question has one part (rule 6).
- **Every claim is cited** and the figures are copied exactly. I checked them
  against arts. 24 and 36 in the index.
- **What isn't covered is said openly** (rule 4): which regime applies.

It gives the same figure as `agent.py` for q11, so the same rules work in both
harnesses.

## Adding a document

**Duplicate policy** (`add_document` in `server.py`). Every chunk id is a
hash of its source, location and text, so:

- **Same file again:** every id already exists → *"Already indexed: RD 958/2020
  comunicaciones comerciales del juego (62 passages), identical content.
  Nothing added."* No embedding is paid for. Tested in
  `eval/add_document_duplicate.txt`.
- **New version of an indexed document** (same source, some text changed):
  old chunks that are not in the new version are deleted and only the new
  chunks are embedded, so an amended article replaces the old one instead of
  both being searchable.
- **New document:** chunked and embedded like the corpus.

**Unanswerable question q29:** *"¿Puede un club de fútbol llevar en la camiseta
el patrocinio de una casa de apuestas?"*. None of the three sports laws
regulates gambling advertising.

**Document added:** Real Decreto 958/2020, de comunicaciones comerciales de las
actividades de juego (BOE-A-2020-13495), as BOE XML → 62 chunks. Added through
the agent: I asked it to add the file, the harness stopped and asked *"Approve?
Type 'yes'"*, and I typed `yes` (`eval/add_document_approval.txt`).

| | Answer | Evidence |
|---|---|---|
| **Before** | *"Las leyes consultadas no cubren esta pregunta. Las restricciones sobre el patrocinio de casas de apuestas en las camisetas de fútbol deben consultarse en la normativa específica de juego…"* (1 search, 3,678 tokens, 8.6 s) | `eval/add_document_before.txt` |
| **After** | *"No, no es admisible el patrocinio de operadores de juegos de azar y apuestas en las camisetas o equipaciones deportivas (RD 958/2020, Artículo 12)."* (2 searches, 7,752 tokens, 8.3 s) | `eval/add_document_after.txt` |

The refusal before was the right behaviour, and after the document is added
the same question gets a correct, cited answer, without changing any code.

## Harness and guardrails

**`AGENTS.md`** is the system prompt: 8 rules, each with its reason.
1. Search first, answer only from the results.
2. Cite every claim as *(Ley 19/2007, Artículo 4)*.
3. If not covered, start with exactly *"Las leyes consultadas no cubren esta
   pregunta."*
4. If partly covered, answer that part and say what is missing.
5. Copy figures exactly.
6. Search in Spanish, once per part, at most 4 searches.
7. Answer in Spanish, briefly.
8. Use add_document only when the user asks.

The fixed refusal sentence is a design choice: because of it, the evaluation
can detect refusals in code instead of asking a judge.

**`agent.py`** (LangChain `create_agent`, Gemini, the MCP tools):

- **Approval before `add_document`.** The tool wrapper asks the user *before*
  calling the server. Anything but "yes" returns "The user did not approve…
  Nothing was added." With no terminal to ask (evaluation, scripts), it is
  always refused, so documents are never added unattended.
- **Limits:** at most 4 searches and 8 model calls per question (middleware),
  so a confused agent can't loop and burn quota.
- **Model fallback:** if `gemini-3.5-flash-lite` is overloaded (503), the same
  request goes to `gemini-flash-lite-latest`.
- **Extra guardrail: citation check.** After the agent answers, code checks
  that a non-refusal answer cites at least one passage and that **every
  citation is a law and article that the search actually returned**. If not,
  the answer is replaced by the refusal plus *"No he podido dar una respuesta
  verificable…"*. Why this one: the worst failure in this use case is a
  confident answer with a made-up article, and that can be checked in code.

**A case where it fired (q08, beer in a stadium).** The agent's answer was
correct: *"No, queda prohibida la introducción, venta y consumo de toda clase
de bebidas alcohólicas… (Ley 19/2007, Artículo 4). Asimismo… (Ley 19/2007,
Artículos 6 y 7)."* The guardrail read *"Artículos 6 y 7"* as one unknown
article and blocked the answer, so the user got a refusal. Arts. 6 and 7 had
in fact been retrieved, so this was a **false positive**: the guardrail
failed safe (a refusal, not a wrong answer), but it cost a correct answer. I
fixed the parser to split plural citations; run offline on the saved q08
trace, the guardrail now lets the answer through. A live rerun of q08 after the
fix also answers correctly, citing (Ley 19/2007, Artículo 4)
(`eval/q08_after_fix.txt`). That run cited one article only, so the offline
trace is what tests the plural case. The table below is still the original
35-question run, so it counts q08 as a wrong refusal.

## Evaluation

The agent ran on all 44 questions (answers cached in `eval/answers.jsonl`).
The first 35 answers come from the first run; the 9 colloquial questions were
run later with the same code, and the judge regraded all 44 answers.

**Checked in code** (`evaluate.py`, `code_checks`):
- refusal: does the answer start with the fixed sentence?
- whether the guardrail fired;
- number of searches;
- whether every citation is a retrieved passage;
- whether the expected article was retrieved and cited;
- tokens and seconds.

For unanswerable questions, the code alone decides whether the refusal is
correct.

**Graded by an LLM judge** (`gemini-flash-lite-latest`, temperature 0),
only for answers that are not refusals. Rubric, in short:
- **correct = 1** if the answer gives the key facts of the reference (numbers,
  periods, who decides, yes/no) and contradicts none of them. A two-part
  question with only one part right gets 0.
- **supported = 1** if every claim about the law is in the retrieved passages.
  A claim that is true in reality but not in the passages counts as 0. Advice
  on where to look is not a claim.

The judge replies in JSON with a one-sentence reason (`eval/judged.csv`).

**A limit of this judge.** Because of the free-tier quota, the judge is a
"lite" model from the same family as the agent, and it is the same model the
agent falls back to when `gemini-3.5-flash-lite` returns 503. A judge that
shares the agent's blind spots may accept the same mistakes the agent makes,
which is one reason I graded every answer myself as well.

**Results** (`eval/summary.json`):

| Outcome | First set (q01–q35) | Colloquial set (q36–q44) | All 44 |
|---|---|---|---|
| Correct | 27 / 28 answerable (96.4%) | 4 / 5 answerable | 31 / 33 (93.9%) |
| Unsupported claim (judge) | 0 | 0 | 0 |
| Wrong answer (judge) | 0 | 1 (q36) | 1 |
| Wrong refusal | 1 (q08) | 0 | 1 |
| Correct refusals | 7 / 7 | 4 / 4 | 11 / 11 |
| Guardrail fired | q08 | q39 | 2 |
| Citations pointing to a retrieved passage | 100% | 100% | 100% |
| Expected article cited | 96.4% | 4 / 5 (q42 missing) | 93.9% |

When the judge regraded the first 35 answers, every verdict was the same as
in the first run, so at temperature 0 it is at least consistent with itself.

**What the colloquial set showed:**
- **q36 (image rights in a video game), wrong answer.** The agent found the
  right article and wrote one sentence: the athlete manages their own image
  rights against the club (Ley 39/2022, Artículo 22). It did not say that
  whether the game must pay and what the contract says are not in these laws.
  That is a half answer presented as complete, which rule 4 forbids and which
  my cost model treats like a wrong answer.
- **q42 (security at a home match), the judge said correct, I disagree.** The
  agent made two searches, both phrased with the violence law's vocabulary, so
  it never retrieved Ley 39/2022, art. 86, which lists the organiser's duties,
  including *"el control y la asistencia sanitaria"* and accident and civil
  liability insurance. It then said the laws don't cover ambulances. The
  judge accepted this because the answer was well cited and admitted a gap.
  For the user it is a wrong *"not covered"* on a point the corpus does cover.
- **q39 (a tweet against the referee), guardrail fired.** The agent answered
  with the general sanctions of Ley 39/2022 (arts. 109–110) but wrote its
  citations as *"(Artículo 110)"* without the law's name. The guardrail
  counted that as an answer without citations and replaced it with the
  refusal. The final outcome is a correct refusal, but by accident.
- **Partial coverage handled well in q41, q43 and q44.** For example, in q43
  it gave the 15 working days for a licence and the extrajudicial and
  Tribunal Administrativo del Deporte routes, citing each one.

**My grades vs the system** (`eval/human_labels.csv`, the first 35 answers):
agreement on **correct 100%** and on **supported 97.1%**. The one
disagreement is q29: the refusal names *"la Ley 13/2011 de regulación del
juego"*, which is not in any retrieved passage. I marked it unsupported, but
refusals are decided in code and never reach the judge, so the system counted
it as fine. Lesson: checking only the refusal format lets content inside a
refusal go unchecked.

I also noted small problems that don't change the grade: q15 and q21 leave out
a secondary detail, and q23 says *the club* is fined while art. 24.5 fines *its
responsible persons*. The judge marked all of these correct. With the rubric's
"key facts" wording that is defensible, but it shows the judge is lenient on
omissions.

## Failures

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 1 | q42: Ley 39/2022 art. 86 never retrieved; the agent searched only with the violence law's words (q23 and q27 missed art. 24 in a single search at the retrieval stage, but the agent searched once per part and found it) |
| Wrong answer from the right passage | 1 | q36: right article, but only half the question answered, with no "not covered" for the rest (minor omissions only: q15, q21, q23) |
| Unsupported claim | 1 | q29: names Ley 13/2011 from the model's memory inside a refusal |
| Wrong refusal | 1 | q08: guardrail parser bug on "Artículos 6 y 7" |
| Bad test question | 0 | (q39 is borderline: the laws only sanction public statements that incite violence, so a partial answer would also be acceptable) |

The judge caught q36 but not q42, so for the colloquial set I trust my own
reading over its verdict.

Two more weaknesses:
- **Outdated citation, q20.** The answer is right (Ley 39/2022, art. 120), but
  it also cites LO 11/2021, Disposición final primera. That provision amended
  the *old* Ley 10/1990 del Deporte, which has since been repealed. The corpus
  contains amending text that the model can present as current law.
- **The first test set was easier than real use.** I wrote it from the
  articles, so it shares their vocabulary. The colloquial set confirmed it:
  hit@1 fell from 93% to 82%, and 2 of its 5 answerable questions failed
  (q36, q42) against 1 of 28 in the first set. Both failures were on
  questions that cross two laws or mix covered and uncovered parts.

**What to fix first:**
1. **The citation parser** (done). It turned a correct answer into a refusal,
   and plural citations are common in legal answers.
2. **Check refusals too.** Strip or verify any law named in a refusal, or tell
   the model in AGENTS.md not to name specific laws it didn't retrieve.
3. **Mark amending provisions** (disposiciones finales that modify other
   laws) in the chunk metadata, so they are either filtered out or cited as
   "modifies…".
4. **Make partial answers say what is missing** (q36). The code could
   check that a partial answer contains a "not covered" sentence, or AGENTS.md
   could ask for one line per part of the question.
5. **Search across laws** (q42). Tell the agent to search each law that could
   apply, or add a query without law-specific words, so an organiser's duty in
   the Ley del Deporte is not hidden by the violence law.
6. **Accept citations without the law's name when only one law was
   retrieved** (q39), or ask for the full form in AGENTS.md, so the guardrail
   doesn't refuse for a formatting reason.
7. Keep adding colloquial questions (9 so far, written after the design was
   chosen).

## Decision

**Yes, as a first lookup for club and federation staff, not as legal advice.**
On my first test set it never gave a wrong answer: every non-refusal was
correct and cited an article the user can open, and it refused all 7
questions the laws don't cover. The one failure was a refusal, which costs
~€150 of legal advice in my cost model, not a fine or a ban. The colloquial
set is less clean: it still invented nothing and refused all 4 uncovered
questions, but it gave one incomplete answer (q36) and one wrong *"not
covered"* (q42). Neither contains a false statement of law, and both cite the
article they rely on, so a user who reads the citation would see the gap. But
they show that the assistant is weakest on everyday wording and on questions
that cross two laws, which is how real users ask.

**Safeguards:**
- Always show the cited articles next to the answer (the CLI already lists the
  "Pasajes consultados"), so staff check the text before acting.
- Keep the citation guardrail: an answer it can't verify becomes a refusal.
- For sanctions, deadlines and amounts, the user must read the article before
  acting. Anything that leads to a formal decision goes to a lawyer.
- `add_document` stays behind approval, and only staff who maintain the corpus
  should approve, because it changes every later answer.

**Cost and latency per question** (all 44): mean **6,008 tokens** (median
4,852) and median **5.5 s**. The colloquial questions are longer and need
more searches: 1.6 searches and 7,536 tokens on average, against 1.2 and
5,615 for the first set. The mean of 17.3 s is inflated by retries on Gemini 503
"high demand" errors (q02 took 431 s). On the free tier this costs €0, but the
quota is the real limit: the "flash" models allow only 20 requests a day,
which is why I used the "lite" models. For real use, a paid tier is needed for
both the quota and the latency.

## AI use

I used an AI coding assistant to:
- write and debug the code (`index.py`, `server.py`, `agent.py`, `evaluate.py`);
- explain errors (the Gemini batch embedding problem, quota errors);
- draft this report from my results;
- prepare a first draft of the grades in `eval/human_labels.csv`;
- classify the colloquial questions q36–q44 (which article answers them, if
  any) and draft their reference answers. The questions themselves are mine.


