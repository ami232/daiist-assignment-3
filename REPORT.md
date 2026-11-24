# Assignment 3 Report

- **Name**: Brissa James
- **Student ID**: 19800
- **Group**: BBADBA 5B

## Use case

A university student who lives alone and cooks for themself asks whether food in their fridge or
freezer is still safe to eat: how long chicken lasts, whether thawed meat can be refrozen, what to
do with mold on jam. They eat, freeze or throw away the food based on the answer.

A wrong "it's fine" can cause food poisoning. A wrong "throw it out" only wastes food. So "I don't
know, when in doubt throw it out" is much cheaper than a confident wrong answer, and the assistant
must refuse when the documents don't cover the question.

## Corpus

All documents are US federal government works (public domain, 17 U.S.C. §105), with no personal
data. `main.py index` downloads them into `corpus/`.

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| FDA Bad Bug Book, 2nd ed. | https://www.fda.gov/media/83271/download | 2012 | Public domain | 106,997 |
| FDA "How to Cut Food Waste and Maintain Food Safety" + Refrigerator & Freezer Storage Chart | https://www.fda.gov/media/101389/download | 2019 | Public domain | 2,099 |
| 29 FDA consumer pages (eggs, seafood, refrigerator, power outages, Listeria, raw milk…), list in `index.py` | https://www.fda.gov/food/buy-store-serve-safe-food | 2019-2024 | Public domain | 26,043 |
| **Total: 31 documents** | | | | **135,139** |

USDA, CDC and foodsafety.gov were left out because they block automated downloads.

## Ingestion

- **Extract:** HTML with BeautifulSoup (main article only, tables kept row by row); PDFs with pypdf.
- **Clean:** whitespace, hyphenation, PDF running headers and page numbers.
- **Chunk:** by structure. HTML pages split at their headings; the Bad Bug Book at its PDF outline
  (pathogen > section); the storage chart line by line so table rows stay whole. Short sections of
  the same parent are merged, long ones split. Max 400 words per chunk (mean 257).
- **Why 400 words:** 250/300/400/500 words gave 795/682/519/427 chunks. The free tier allows about
  1,000 embeddings a day, so 400 fitted the whole corpus in one day and left quota for queries,
  while keeping one section per chunk in most cases.
- **Metadata:** `source`, `title`, `location` (section, or `p. N, pathogen > section`), `url`, `words`.
- **Embedding:** `gemini-embedding-2`, stored in ChromaDB (`index/`, 17 MB). Only chunks without a
  saved vector are embedded; vectors are saved after each batch.
- **Chunks:** 526 (Bad Bug Book 422, FDA pages 97, chart 7).
- **Extraction problem fixed:** every Bad Bug Book page repeated the header "Bad Bug Book /
  Foodborne Pathogenic Microorganisms and Natural Toxins", sometimes split over two lines, which
  ended up inside chunks. Removed with a regex. The storage chart was also being cut mid-row; it is
  now packed line by line.

## Test set

30 questions in `eval/questions.csv`: **11 single, 10 multi, 9 unanswerable**. I wrote them as the
questions I actually ask in front of my fridge (in Spanish, then translated). Half were about
storage times, which the first corpus did not cover, so the FDA storage chart was added.
The refreezing questions (q22-q27) repeat the same question for different proteins.

| id | question | kind | expected | reference answer |
|---|---|---|---|---|
| q01 | How long do eggs last in the fridge? | multi | storage chart p. 4; egg safety page, Storing | 3-5 weeks in the shell; use within 3 weeks for best quality |
| q30 | Does coffee go bad? | unanswerable | - | The corpus does not cover this |

## Retrieval

Same chunks and vectors for both designs; 21 answerable questions.

| Design | hit@1 | hit@3 | hit@5 | words added (k=5) |
|---|---|---|---|---|
| **Dense** | **0.57** | **0.67** | **0.91** | 1,354 |
| Hybrid (dense + BM25, RRF) | 0.43 | 0.52 | 0.57 | 1,341 |

**Chosen: dense.** It is better at every k for the same prompt size. Words like "chicken" or
"freeze" appear in hundreds of chunks, so BM25 added noise.

## Tools and subagent

- **`search(query)`:** "Search an index of official U.S. FDA food-safety guidance for consumers
  (storage chart, storing, thawing, leftovers, eggs, seafood… and the Bad Bug Book). Use it for any
  question about whether food is safe to eat. Returns the 5 most relevant passages, each headed by
  its citation [source | location]."
- **`add_document(path)`:** "Add one local .pdf, .html, .txt or .md file to the index with the same
  pipeline. Same file and content: nothing changes. Same name, new content: old chunks replaced."

One search result:
```
### Result 1  [fda:what-you-need-know-about-egg-safety | Section: Storing; Preparing]
Document: What You Need to Know About Egg Safety
• Store eggs in their original carton and use them within 3 weeks for best quality.
```

**Subagent** (`.claude/agents/corpus-researcher.md`, only the search tool): search first, answer
only from the passages, cite every claim, say when the documents don't cover it, never guess a
number of days.

**Transcript (Claude Code):**
> **Me:** cuantos dias aguanta el pollo en la refri antes de tener que congelarlo? y si lo
> descongelo lo puedo volver a congelar?
>
> **corpus-researcher:** El pollo fresco aguanta de 1 a 2 días en el refrigerador… [fda_storage_chart
> | p. 4 (part 2)]. Los documentos no dicen directamente si se puede volver a congelar pollo ya
> descongelado; solo que la comida que todavía tiene cristales de hielo o está a 40 °F o menos se
> puede volver a congelar [fda:refrigerator-thermometers-cold-facts-about-food-safety | Section: In
> Case of Disaster...; How Long Is Too Long?]…

Full transcript: `eval/subagent_transcript.md`.

## Adding a document

- **Already indexed:** same content → "Already indexed… Nothing changed"; changed content → replaced.
- **Question:** q02 "If I scrape off the moldy part of my jam, can I eat the rest?"
- **Document:** USDA FSIS "Molds on Food: Are They Dangerous?" (public domain, 6 chunks), added
  through the agent with approval.
- **Before:** "The FDA documents I have don't cover this."
- **After:** "No, you should discard the jam [usda_molds_on_food | Section: How Should You Handle
  Food with Mold on It? (part 2)]. Microbiologists recommend against scooping out the mold…"

## Harness and guardrails

`agent.py`: LangChain `create_agent` on `gemini-3.5-flash-lite`, tools from `server.py` over MCP,
`AGENTS.md` as system prompt, max 6 tool calls and 8 model calls per question.

- **AGENTS.md rules:** (1) answer only from search results, because only the FDA text is checked;
  (2) cite every claim, so each claim can be verified; (3) say when the corpus doesn't cover the
  question, because a wrong "it's fine" can make someone sick.
- **Approval:** `add_document` only runs after a human types `y`; without a terminal it is denied.
- **Extra guardrail, verified citations:** every citation must match a passage `search` returned in
  that run; an answer without citations is only accepted if it is a refusal. If it fails, one retry;
  if it fails again, the answer is withheld.
- **Case where it fired:** q18 "Why does my fridge smell bad?": both attempts failed, so the user got
  "I couldn't produce an answer backed by valid citations… so I won't guess. When in doubt, throw it
  out." It fired on 5 of 30 questions.

## Evaluation

- **Code checks:** citations valid, expected source cited, refusals (right and wrong).
- **Judge:** `gemini-3.1-flash-lite` (different from the agent), with the retrieved passages as
  evidence. Rubric: *correct* = key facts of the reference (both parts for multi), or a clear refusal
  for unanswerable; *supported* = every claim is in the evidence.
- **Agreement with my 30 grades:** correct 29/30 (97%, kappa 0.87), supported 30/30. The only
  disagreement is q26: I gave 0 because it started with "the documents don't cover this"; the judge
  gave 1 because it then quoted the general refreezing rule.

| Result | |
|---|---|
| Correct | 26/30 (87%) |
| Unsupported | 0/30 |
| Correct refusals | 9/9 |
| Wrong refusals | 5/21 |

## Failures

| id | question | cause |
|---|---|---|
| q16 | cooked lentils in the fridge | bad test question (the chart only says "soups & stews") |
| q24, q25, q26 | refreeze thawed burger / salmon / tuna | wrong refusal (right passage retrieved) |
| q27 | refreeze thawed white fish | retrieval miss |

Counts: 3 wrong refusals, 1 retrieval miss, 1 bad test question, 0 unsupported claims.
**Fix first:** the wrong refusals. The model is too cautious when the passage gives a general rule
instead of naming the food; a rule in AGENTS.md to apply general rules (with citation) would help.

## Decision

Yes, for simple storage questions (how many days, fridge vs freezer), as long as the citations are
shown and it keeps refusing when unsure. It never made an unsupported claim and refused all 9
unanswerable questions; its errors are refusals, which for food safety is the cheap error.
Safeguard: show sources and keep "when in doubt, throw it out". Limits: US guidance (°F), and the
free-tier quota.

**Cost:** ~8,400 tokens and ~9.7 s per question, 1.6 searches on average.

## AI use

Claude Code (Claude Opus) wrote the code, found the public-domain sources, translated my test
questions and filled their expected sources, drafted the judge rubric and wrote this report (our
professor allowed AI for the report). I chose the use case, corpus, chunk size and guardrail, wrote
the test questions and graded the 30 answers myself before seeing the judge's verdicts.
