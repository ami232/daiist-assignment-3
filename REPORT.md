# Assignment 3 Report

- **Name**: Yan Bernard
- **Student ID**: 20202
- **Group**: BBADBA 5A

## Use case

I built this for independent artists, small-label owners or managers who don't
have legal training — people based in the US or the EU who need to figure out
which copyright right applies (composition vs sound recording, performance vs
mechanical vs neighbouring rights), who collects it, and what the law actually
says. The goal is to help them decide what to claim or when it's time to hire
a lawyer.

A wrong answer here can be expensive: unclaimed royalties, a badly signed
split, or signing away rights entirely. A confident but incorrect rule about
which party collects or which jurisdiction applies can cost real money.
So for this use case, "I don't know, ask a music lawyer" is way better than
a confident mistake.

The main failure mode I designed around is mixing up which right or which party
is involved, and confusing US vs EU/UK rules. Anything about contracts, industry
practice (typical splits, per-stream payouts) or business advice is out of scope
and should just be refused.

## Corpus

| Document | Source | Licence | Pages | ~Words |
|---|---|---|---|---|
| US Copyright Office Circular 56 — Sound Recordings | copyright.gov | US Gov't, public domain | 8 | 2 835 |
| US Copyright Office Circular 56A — Musical Compositions and Sound Recordings | copyright.gov | US Gov't, public domain | 10 | 3 492 |
| US Copyright Office Circular 58 — Group Registration of Works on an Album | copyright.gov | US Gov't, public domain | 8 | 3 234 |
| CRB Phonorecords IV Final Rule (2022-28316) — Mechanical Royalty Rates 2023-2027 | Federal Register | US Gov't, public domain | 13 | 15 267 |
| EU Directive 2019/790 (DSM) — Copyright in the Digital Single Market | EUR-Lex (CELEX 32019L0790) | Official EU legislation | 34 | 23 440 |
| UK IPO Copyright Notice 3/2014 — Performance of Live Music | gov.uk | Open Government Licence v3.0 | 4 | 2 282 |

**Total: 6 documents, 77 pages, ~50 550 words.**

## Ingestion

I used PyPDF for page-by-page text extraction. The cleaning step strips out
Copyright Office footers, standalone page numbers, and Federal Register headers.

One thing that caused me trouble: the Federal Register PDF (CRB Phonorecords IV)
has a three-column layout, and PyPDF extracts columns sequentially, which
sometimes interleaves text from adjacent columns. I handled this by removing
repeated header lines (`Federal Register / Vol. 87...`) and standalone page
numbers that show up in the middle of the text.

For chunking I compared two designs:

1. **Fixed-size:** 375 words per chunk with 50-word overlap (~500 tokens).
   Simple and uniform, but it loses section boundaries.
2. **Structure-based:** Splits on detected headings (Article X, section titles,
   FAQ headings) and prefixes each chunk with its heading. This preserves
   document structure and context. Max 600 words per section; long sections
   get split further.

Every chunk carries metadata: `source` (filename stem), `location` (page +
heading), `design` (fixed/structure), and a `content_hash` (SHA-256, used for
deduplication).

Final counts: 158 fixed + 245 structure = 403 total chunks, stored in ChromaDB
with cosine similarity in `index/chroma/` (14 MB).

## Test set

I wrote 32 questions from the documents:

| Kind | Count |
|---|---|
| `single` (one passage) | 20 |
| `multi` (two passages) | 6 |
| `unanswerable` | 6 |

I made the unanswerable questions topic-adjacent on purpose — things like
Spotify rates, trademark registration, sync licensing, HFA fees, DMCA safe
harbour, and sampling rules. They're close enough to music copyright that the
system can't just ignore them; it has to actively decide to refuse.

A few examples:

- *Single:* "What is the Copyright Act's definition of a sound recording?"
  → Expected: circ56, p.1.
- *Multi:* "How do the rights of musical composition owners differ from sound
  recording owners regarding public performance?" → Needs both circ56a and
  circ56.
- *Unanswerable:* "What is the current per-stream royalty rate on Spotify for
  independent artists?" → Out of scope; the corpus has statutory rates, not
  platform payouts.

## Retrieval

| Design | k = 1 | k = 3 | k = 5 |
|---|---|---|---|
| Fixed-size (375 words) | 92% | 96% | 100% |
| **Structure-based** | **96%** | **96%** | **100%** |

I went with **structure-based chunking**. It wins at k = 1, which is the
hardest threshold — the heading prefixes seem to help the embedding model match
questions to the right section. Both designs hit 100% at k = 5, so the corpus
does cover all the answerable questions.

Each search returns up to 5 chunks, so roughly 5 × 600 = 3 000 words of
context go into the prompt per question.

## Tools and subagent

### MCP tools (server.py)

- **search(query):** Embeds the query with `gemini-embedding-2`, searches the
  structure-based ChromaDB collection (cosine similarity, top 5), and returns
  each chunk with its `chunk_id`, `source`, `location`, `score` and full text.

- **add_document(path):** Takes a PDF path. It checks the content hash first —
  if the exact same content is already indexed it skips; if the same filename
  exists with different content it replaces the old chunks. Otherwise it runs
  the chunking pipeline and embeds the new chunks.

Here's what a search result looks like for "What is a sound recording?":

```
[chunk_id: circ56__struct__002]
[source: circ56, location: p.1, What is a Sound Recording?, score: 0.848]
The Copyright Act defines sound recordings as "works that result from the
fixation of a series of musical, spoken, or other sounds but not including
sounds accompanying a motion picture or other audiovisual work."...
```

### Subagent (.claude/agents/corpus-researcher.md)

The subagent is set up with `tools: mcp__corpus__search` and told to use the
search tool for every question, cite every claim, name the jurisdiction and
right type, never give legal advice, and refuse when the corpus doesn't cover
the question.

**Transcript** (Claude Code, using the `corpus-researcher` subagent via MCP
`corpus` server):

> **User:** What is the Copyright Act's definition of a sound recording?
>
> **corpus-researcher:** *(calls `mcp__corpus__search` with query "Copyright Act
> definition of a sound recording")*
>
> Under US federal law (specifically the Copyright Act), sound recordings are
> defined as "works that result from the fixation of a series of musical, spoken,
> or other sounds but not including sounds accompanying a motion picture or other
> audiovisual work" [circ56, p.1, "What is a Sound Recording?"].
>
> This definition relates to copyright in a sound recording (a neighbouring or
> related right), which is distinct from copyright in the underlying musical
> composition [circ56, p.2, "Sound Recordings Distinguished from Underlying
> Creative Works"].

## Adding a document

The dedup logic works like this: if the file's content hash already exists in
the index, it skips. If the same source name exists but the content changed,
it replaces the old chunks. Otherwise it just chunks, embeds, and stores.

### Before/after demo

I used q32 — "What are the copyright rules for sampling pre-existing
recordings in hip-hop music?"

I added `sampling_rules.pdf`, a one-page summary of US sampling law covering
the dual-licence requirement, the Bridgeport v. VMG Salsoul circuit split,
fair use, and clearance practice. Running
`add_document("docs/sampling_rules.pdf")` created 5 new structure-based chunks.

**Before (no sampling document in corpus):**

> The retrieved corpus contains limited references to sampling, specifically
> noting that under US federal law, a derivative sound recording is an audio
> recording that incorporates preexisting sounds (such as those previously
> registered, published, or fixed before February 15, 1972) provided that the
> preexisting recorded sounds are rearranged, remixed, or otherwise altered in
> sequence [circ56, p.2, Derivative Sound Recordings].
>
> The corpus does not contain detailed rules concerning the specific legal
> requirements for clearing samples in hip-hop music.
>
> The corpus does not cover this question. Please consult a music lawyer or your
> collecting society.

**After (`sampling_rules.pdf` added):**

> Under US federal law, sampling a pre-existing sound recording in a new work
> such as hip-hop music requires two separate licences:
> 1. Permission from the owner of the copyright in the **sound recording**
>    (typically the record label).
> 2. Permission from the owner of the copyright in the underlying **musical
>    composition** (typically the music publisher or songwriter).
> Failure to obtain both licences constitutes copyright infringement
> [sampling_rules, p.1, "Section 1: Legal Framework for Sampling"].
>
> Additional legal rules and considerations:
> - In the Sixth Circuit (*Bridgeport Music, Inc. v. Dimension Films*, 2005),
>   any unauthorised copying of a sound recording constitutes infringement ("Get
>   a license or do not sample") [sampling_rules, p.1, "Section 2: Key Case
>   Law"].
> - In the Ninth Circuit (*VMG Salsoul, LLC v. Ciccone*, 2016), the de minimis
>   defence does apply — a sample too small to be recognised is not actionable
>   [sampling_rules, p.1, "Section 2: Key Case Law"].
> - Fair use defences in sampling cases have generally been unsuccessful
>   [sampling_rules, p.1, "Section 4: Fair Use Considerations"].
> - To legally clear a sample: identify both copyright owners, negotiate
>   clearance licences, and obtain written permission before release
>   [sampling_rules, p.1, "Section 3: Practical Requirements for Clearing
>   Samples"].

So it went from a clean refusal to a fully cited answer just by adding the
right document — exactly what the add_document tool is for.

## Harness and guardrails

The AGENTS.md system prompt has 8 rules: answer only from retrieved passages,
cite every claim, name the jurisdiction, name the type of right, say "I don't
know" when the passages aren't enough, never give legal advice, refuse
out-of-scope questions, and keep answers concise.

### Approval step
The `add_document` tool asks for explicit human approval (`y/n` prompt) before
it runs. In non-interactive mode (e.g. during evaluation), it defaults to
denied.

### Extra guardrail: score-threshold pre-filter
Before even calling the LLM, the agent checks the top retrieval score. If the
best cosine-similarity is below 0.25, it refuses right away without spending
tokens — this prevents hallucination on clearly out-of-scope questions.

For example, q27 ("What is the current per-stream royalty rate on Spotify?")
scored below threshold, so the agent returned "I don't have enough relevant
information" in 2.6 seconds without touching the LLM.

## Evaluation

### Code checks (automated)

| Check | Count |
|---|---|
| Citation present (answerable) | 22/22 (100%) |
| Citation missing | 0 |
| Correct refusal (unanswerable) | 4/6 |
| Wrong refusal (answerable refused) | 4 |
| Missed refusal (unanswerable not refused) | 2 |

Every answerable question that got an answer included citations, which is good.
The 4 wrong refusals are from the score threshold being a bit too aggressive
(more on that below).

### LLM judge rubric

I used Gemini as an LLM judge. It grades each answer as `correct`,
`partially_correct`, `incorrect`, `correct_refusal`, `wrong_refusal`, or
`unsupported_claim`, and also checks whether citations are present and the
jurisdiction is correct.

### Judge verdicts

| Verdict | Count | % |
|---|---|---|
| Correct | 18 | 56% |
| Partially correct | 7 | 22% |
| Unsupported claim | 3 | 9% |
| Correct refusal | 3 | 9% |
| Wrong refusal | 1 | 3% |

### Human-judge agreement

I got **66% agreement (21/32)** with the LLM judge. Most disagreements were
borderline — the judge called some answers `partially_correct` where I thought
they were `correct`, and vice versa. The other mismatches were on q31/q32,
where the agent added tangential info instead of cleanly refusing and we graded
that differently.

## Failures

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 0 | — |
| Wrong answer from right passage | 3 | q14 (wrong Article cited), q18 (missed settling parties), q22 (incomplete synthesis) |
| Unsupported claim | 3 | q07, q09, q13 (agent added details beyond retrieved text) |
| Wrong refusal | 4 | Answerable questions where the guardrail or agent refused unnecessarily |
| Missed refusal | 2 | q31, q32 (unanswerable but agent added tangential info instead of cleanly refusing) |

No retrieval misses at all, which is nice — the index is doing its job. The
problems are all on the generation side.

**What I'd fix first:**

1. **Lower the score threshold** — 4 wrong refusals means 0.25 is too
   aggressive for some valid questions. Something around 0.20 would probably
   fix most of these without letting junk through.
2. **Tighten refusal behavior** — q31 and q32 show the agent sometimes hedges
   with tangential info instead of cleanly refusing. I'd add a stronger rule
   in AGENTS.md: "if the question isn't directly answered by the passages,
   refuse entirely — don't add tangential information."
3. **Better multi-passage synthesis** — q22 and q24 show the agent struggles
   when it needs to combine info from two different documents. A prompt
   instruction to explicitly synthesize across passages could help.

## Decision

**Would I let users rely on it?** Yes, but with guardrails — specifically for
**looking up specific legal rules** like definitions, registration
requirements, and rights tables. It's accurate on single-passage factual
questions (high retrieval hit rate, 100% citation rate on answered questions)
and it correctly refuses most out-of-scope questions.

It's **not good enough for** multi-step legal reasoning, cross-jurisdiction
comparisons, or anything that requires judgment beyond what the statute says.
Every answer should carry a disclaimer that this is not legal advice.

**Safeguards I'd keep:**
- The score-threshold guardrail (tuned a bit lower).
- Always showing source citations so users can check.
- A standing "this is not legal advice" disclaimer.

**Cost per question:**
- Average latency: **8.4 seconds** (with gemini-3.5-flash-lite).
- Embedding: 1 API call per question.
- LLM: 1-2 API calls per question (tool calling + answer generation).
- On the free tier you get about 20 generate requests per model per day; a
  paid key removes that bottleneck.

## AI use

I used Claude Code to write the code for `index.py`, `server.py`,
`agent.py`, `evaluate.py`, `AGENTS.md` and I
reviewed and tested all of it, I made the question using claudes gudance because I am not expert in the matter but I verified the reference answers against
the actual documents. the use-case decision, corpus selection,
chunking-design choice, the ship decision, failure analysis, the human grades
in `eval/human_labels.csv`, and the analysis in this report are all mine.