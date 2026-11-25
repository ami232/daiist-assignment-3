# Assignment 3 Report

- **Name**: Andrés Ramírez López
- **Student ID**: 19077
- **Group**: BBADBA 5A


## Use case

A **compliance analyst at an EU bank** checks what EU banking regulation requires before the
bank acts: a capital or large-exposure limit, a deadline towards the supervisor, a governance or
remuneration rule, an investor-protection duty. The analyst reads the answer, opens the cited
article, and uses it in an internal memo, a control check or a question to the legal team.

A wrong answer can make the bank breach a limit or miss a deadline, which leads to supervisory
measures or fines (MiFID II Article 70 sets maximum fines of at least EUR 5 000 000 or up to 10 %
of annual turnover for legal persons). "I don't know" only costs the analyst a look at the
legal text or a question to legal. So the assistant must cite every claim and refuse when the
corpus does not cover the question.

I chose a compliance analyst at a bank because banking is an industry I like and know from up
close: my family works in banking, and I want to build my career in it, so anything I can work
on in or for this industry is worth it to me. If the bank breaches a rule because of a wrong
figure, the damage goes in many directions: fines and tax consequences, lost clients, harm to
the business and to its value, and financial losses.

## Corpus

The current consolidated English versions, downloaded from the Publications Office (Cellar),
because eur-lex.europa.eu answers scripts with a bot challenge. Words are counted in the
structural chunks.

| Document | URL | Consolidated version | Licence | Words | Articles |
|---|---|---|---|---|---|
| CRR, Regulation (EU) No 575/2013 (without Part Three Titles II-VI and Part Ten) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02013R0575-20260626 | 26.6.2026 | EUR-Lex reuse policy (Commission Decision 2011/833/EU): free reuse with acknowledgement of the source | 119 025 | 267 |
| CRD, Directive 2013/36/EU | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02013L0036-20260711 | 11.7.2026 | same | 86 294 | 190 |
| MiFID II, Directive 2014/65/EU | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02014L0065-20260606 | 6.6.2026 | same | 58 714 | 93 |
| **Total** | | | | **264 033** | **550** |

Legislative texts contain no personal data. The CRR's risk-weighted-asset calculation (Part
Three Titles II-VI) and its transitional provisions (Part Ten) are left out on purpose, for
three reasons. They are mostly tables and formulas that chunk badly and add noise to search,
while the analyst mainly needs limits, deadlines and obligations. At about 1 000 embeddings a
day, indexing them would have taken several more days. And leaving them out gives the test set
questions that are genuinely outside the corpus (risk weights), to check that the agent says
it does not know, which is also what the add-document demo shows. Part Three Title I (general
requirements, including the capital ratios in Article 92) is kept.

## Ingestion

`index.py` parses the EUR-Lex XHTML article by article:

- **Extraction.** Each article is a `div.eli-subdivision` (`id="art_N"`) with its number
  (`p.title-article-norm`), title (`p.stitle-article-norm`) and numbered paragraphs
  (`span.no-parag`). Division headings (PART, TITLE, CHAPTER, Section) are tracked so every
  chunk knows where it sits. Deleted articles and annexes are skipped.
- **Cleaning.** Consolidated texts carry amendment markers (`▼M8`, `►C2 … ◄`), arrows and
  footnote calls. Removing the `p.modref`, `p.arrow` and `p.footnote` elements and the
  `▼►◄` markers keeps the text exactly as it reads in force.
- **Extraction problem fixed.** At first the markers ended up inside the text ("▼M8 1.
  Institutions shall…"), which broke paragraph numbering and put noise into both BM25 and the
  embeddings. A second one came from embedding: sending a plain list of strings to
  `gemini-embedding-2` returned **one** vector for a batch of 50 texts (it was read as one
  multimodal item). Each text is now wrapped in its own `Content`, and the code checks that it
  gets as many vectors as texts.
- **Chunking, two designs.**
  - *structural*: one chunk per article; articles over 400 words are split at paragraph
    boundaries. Each chunk starts with its path, e.g. `CRR > Part Four (Large exposures) >
    Article 395: Limits to large exposures [Article 395(5)]`. **983 chunks.**
  - *fixed*: 300-word windows with 50 words of overlap over each act's running text.
    **971 chunks.**
- **Metadata on every chunk:** `source`, `part`, `title`, `chapter`, `article`,
  `article_title`, `location` (e.g. `Article 395(1)-(2)`, used as the citation),
  `articles`, `paragraphs`, `file`, `words`, `hash`.
- **Embedding and storage.** `gemini-embedding-2`, 768 dimensions, `RETRIEVAL_DOCUMENT` for
  chunks and `RETRIEVAL_QUERY` for queries, in ChromaDB (`index/chroma`, cosine). Only chunks
  without a saved vector (same id, same text hash) are embedded.
- **Incident and fix.** On 18 November, adding a document pushed a collection past 1 000
  items. Chroma then tries to write its HNSW index to binary files; on Windows that write fails
  silently when the path has a non-ASCII character (the project lives under "Andrés"), and
  Chroma dropped the vectors it believed were saved: about 1 030 vectors were lost (reproduced
  in a test folder: with "é" in the path only `index_metadata.pickle` is written). Two fixes:
  the collections keep the HNSW graph in SQLite (`hnsw:sync_threshold` that is never reached),
  and every vector the API returns is also appended to `index/vectors.jsonl`, so rebuilding the
  index never spends embedding quota again. After the rebuild the retrieval numbers were
  identical to the ones before the incident.

## Test set

`eval/questions.csv`: **34 questions**, **21 single-passage**, **6 needing two passages**,
**7 the corpus cannot answer**. They are written in the plain words an analyst would type, not
in the regulation's terms. Every expected article was checked to exist in the corpus.

I wrote the questions and reference answers in `eval/questions.csv` myself, in the plain words
an analyst would use. A draft set written by an AI assistant (Claude), with the professor's
permission, was my reference for topics and expected articles; I changed them and wrote my own.
I checked every reference answer while grading: my grading tool showed it next to the agent's
answer and every retrieved passage.

Two examples:

| id | kind | question | expected | reference answer |
|---|---|---|---|---|
| q02 | single | How much money a bank can lend or have with another bank? | CRR Article 395 | Max 25% of its Tier 1 capital or 150M EUR, the bigger one. If 150M is bigger than 25%, bank put its own limit but never more than 100% of Tier 1. |
| q24 | multi | In how many company boards can sit a board member of a big investment firm? | CRD Article 91; MiFID II Article 9 | 1 executive + 2 non-executive, or 4 non-executive. Supervisor can allow 1 more non-executive. |

The unanswerable questions ask about things a compliance analyst could plausibly ask but that
sit outside the corpus: IRB default probabilities (q28), DORA incident reporting (q29), MiFIR
transaction reporting (q30), managers' transactions under MAR (q31), the anti-money-laundering
threshold for occasional transactions (q32), the length of a PRIIPs KID (q33) and the
standardised-approach risk weight of a home mortgage (q34).

## Retrieval

Hit rate over the 27 answerable questions (a hit is any expected article in the top k;
all@5 asks for every expected article of the two-passage questions). Words@5 is what the five
results add to the prompt.

| design | method | hit@1 | hit@3 | hit@5 | all@5 | words@5 |
|---|---|---|---|---|---|---|
| structural | dense | 0.74 | 0.96 | 1.00 | 0.96 | 1 365 |
| structural | hybrid (dense + BM25, RRF) | 0.41 | 0.70 | 0.93 | 0.78 | 1 511 |
| fixed | dense | 0.52 | 0.85 | 0.85 | 0.74 | 1 500 |
| fixed | hybrid | 0.41 | 0.63 | 0.70 | 0.56 | 1 500 |

For the fixed design a hit counts if any article overlapping the window matches, which is
generous to it, and it still ranks well below structural + dense.

Adding BM25 lowers hit@1 from 0.74 to 0.41: the questions use everyday words ("lend",
"cushion", "board"), not the regulation's, so exact-word matches on common terms push a less
relevant article to the top.

**Choice: structural + dense.** It has the best hit@1, finds every expected article in the top
5 for all but one two-passage question, and puts the fewest words into the prompt.

## Tools and subagent

`server.py` (MCP, stdio) exposes two tools. Their descriptions, as the model sees them:

- **search(query)**: *"Search EU banking regulation: the CRR (Regulation (EU) No 575/2013:
  own funds, capital ratios in Art. 92, large exposures, liquidity, leverage, disclosure; NOT
  the risk-weighted-asset calculation of Part Three Titles II-VI), the CRD (Directive
  2013/36/EU: authorisation of credit institutions, supervision, capital buffers, governance
  and remuneration) and MiFID II (Directive 2014/65/EU: investment firms, investor protection,
  trading venues), in their current consolidated English versions. Use it for every question
  about what these rules require; write the query in English with the regulatory terms you
  expect in the text. Returns the 5 most relevant passages, each with the citation to use,
  e.g. [CRR, Article 395(1)], followed by the passage text. If nothing relevant comes back,
  the corpus does not cover the question."*
- **add_document(path)**: *"Add one document to the searchable corpus. `path` is a local
  file: an EUR-Lex (X)HTML act (kept article by article), a PDF (one passage set per page) or a
  text file. It is chunked with the same pipeline as the corpus and only new or changed chunks
  are embedded. […] Only run it when the user explicitly asks to add a document."*

One search result (excerpt):

```
Result 1  cite as [CRR, Article 395(5)]  (article title: Limits to large exposures)
CRR > Part Four (Large exposures) > Article 395: Limits to large exposures [Article 395(5)]
5. The limits laid down in this Article may be exceeded for the exposures in the institution's
trading book, provided that all the following conditions are met: (a) the exposure in the
non-trading book to the client or group of connected clients in question does not exceed the
limit laid down in paragraph 1, […]
```

If the daily embedding quota runs out, search falls back to BM25 and says so in the result
instead of failing.

**Subagent** (`.claude/agents/corpus-researcher.md`, tools: `mcp__corpus__search` only):
search first with the regulation's terms and reformulate up to three times per question part;
answer only from the returned passages, copying figures exactly; cite every sentence with the
citation given; say whether the rule is in a regulation or a directive; otherwise reply
"The corpus does not cover this question." plus what was searched.

**Transcript from the editor** (Claude Code in VS Code, 2026-11-24, a question not in the test
set):

```
> Use the corpus-researcher subagent: what must an institution do when it breaches the large
  exposures limit?

corpus-researcher -> search("breach of large exposures limit report immediately competent
authority time to comply")   [1 search; returned CRR Articles 396, 392, 395(5), 395(7), 395(1)]

If, in an exceptional case, exposures exceed the limit set out in Article 395(1), the
institution shall report the value of the exposure without delay to the competent authorities.
The competent authorities may, where the circumstances warrant it, allow the institution a
limited period of time in which to comply with the limit. [CRR, Article 396]

For context, the limit in Article 395(1) is an exposure to a client or group of connected
clients whose value exceeds 25 % of the institution's Tier 1 capital. Where the client is an
institution or an investment firm, the limit is 25 % of Tier 1 capital or EUR 150 million,
whichever is higher. A G-SII's exposure to another G-SII or a non-EU G-SII must not exceed
15 % of its Tier 1 capital. [CRR, Article 395(1)]

Where the EUR 150 million amount applies, the competent authorities may allow the 100 % limit
in terms of the institution's Tier 1 capital to be exceeded on a case-by-case basis.
[CRR, Article 396]

If the competent authority allows the limit to be exceeded for a period longer than three
months, the institution must present a plan for a timely return to compliance, to the
satisfaction of the competent authority. It must then carry out that plan within the period
agreed with the authority. [CRR, Article 396] The competent authority monitors the
implementation of the plan and requires a faster return to compliance if appropriate.
[CRR, Article 396] EBA issues guidelines on how competent authorities may determine the
exceptional cases, the time appropriate for returning to compliance and the measures to ensure
a timely return. [CRR, Article 396]

Trading book excesses follow separate rules:
- The limits may be exceeded for trading book exposures only if all the conditions in
  Article 395(5) are met. [CRR, Article 395(5)]
- The institution must meet an additional own funds requirement on the part of the exposure
  that exceeds the limit. [CRR, Article 395(5)]
- Where 10 days or less have passed since the excess occurred, the trading book exposure must
  not exceed 500 % of Tier 1 capital. [CRR, Article 395(5)]
- Excesses that have persisted for more than 10 days must not, in aggregate, exceed 600 % of
  Tier 1 capital. [CRR, Article 395(5)]
- Each time the limit is exceeded, the institution must report to the competent authorities
  without delay the amount of the excess and the name of the client. Where applicable, it must
  also report the name of the group of connected clients. [CRR, Article 395(5)]

Type of act: these rules are in the CRR, which is a regulation and applies directly. There is
no national transposing law to check for them.
```

Checked against the search output: every citation was returned by that search and every figure
(25 %, EUR 150 million, 100 %, 15 %, three months, 10 days, 500 %, 600 %) is in the passages.
The context paragraph on Article 395(1) leaves out the condition attached to the EUR 150
million limit (exposures to connected clients that are not institutions must stay within 25 %),
an omission an analyst would only notice by reading the article.

## Adding a document

**Already indexed:** "update if changed". Chunks are matched by id and text hash: unchanged
chunks are kept, changed ones re-embedded, chunks no longer in the file deleted. Adding the
same unchanged file again returns "Already indexed … nothing changed" and spends no quota.
Vectors are also kept in `index/vectors.jsonl`, so re-adding a removed document is free.

**Unanswerable question:** the topic of q34 (home mortgage risk weights), asked in the
regulation's terms: *"What risk weight applies under the standardised approach to retail
exposures fully secured by residential property?"*

**Document added:** `docs/CRR_risk_weights_standardised_approach.xhtml`: CRR Articles 114-134
(Part Three, Title II, Chapter 2, Section 2), from the same consolidated version, 64 chunks.

- **Before:** "The corpus does not cover this question. I searched for the risk weight
  applicable under the standardised approach to retail exposures fully secured by residential
  property." (2 searches)
- **Approval:** the agent asked to run `add_document`; the human typed `y`.
- **After:** a cited answer: 20 % for the part of the exposure up to 55 % of the property value
  [CRR, Article 125(1)], and the exposure-to-value buckets 30 / 35 / 45 / 60 / 75 / 105 %
  [CRR, Article 125(2)], checked against the document.

Full outputs in `eval/add_document_demo.md`.

After the demo the document was removed from the index (983 chunks again), so q34 stays a
question the corpus cannot answer in the evaluation. Its vectors stay in `index/vectors.jsonl`,
so adding it again spends no quota.

## Harness and guardrails

`agent.py`: LangChain `create_agent` with `gemini-3.8-flash` (temperature 0), the MCP tools
over stdio, and `AGENTS.md` as system prompt. When the model is overloaded (503/504) after
retries, it falls back to `gemini-3.5-flash-lite` and records which model answered.

**AGENTS.md rules** (each with its reason in the file): answer only from search results; cite
every claim with the citation given; reply exactly "The corpus does not cover this question."
when the results do not answer; search before answering and reformulate (at most three searches
per question part); copy figures literally; say whether the rule comes from a regulation or a
directive; never add documents unless asked.

**Approval step:** `HumanInTheLoopMiddleware` interrupts before `add_document`; it runs only if
the human types `y`. Without an interactive terminal (evaluation) it is rejected.

**Tool-call limit:** at most 6 tool calls per question (`ToolCallLimitMiddleware`).

**Extra guardrail: citation validator.** After the answer, code checks that every
`[Source, Article …]` citation was returned by a search in this run (at article level), and
that an answer that is not a refusal cites something. If not, the agent is told what is wrong
and gets one chance to rewrite; if it still fails, the answer is shown with a warning.

**Where it fired during development:**
- An answer cited `[MiFID II, Article 5(4)(a)]`, but the check's pattern accepted only one
  level of parentheses (`5(4)`), so it saw "no citations", asked for a rewrite and added a
  warning to a correct answer. A false positive; the pattern now accepts `5(4)(a)`.
- *add_document demo, first run:* after a successful add, the check saw an answer with no
  citations and pushed the agent into the refusal phrase. A turn that only adds a document is
  now exempt.

Neither was a made-up citation. In the final evaluation it did not fire: all 34 answers passed
the check the first time.

I keep it as a safety net. So far its real cost came from its own bugs, now fixed, not from
blocking good answers by design. It stays because a single made-up citation would be the most
dangerous error for the analyst, who opens the cited article to verify the answer, even if such
citations are rare. The lesson: a guardrail has to be tried on real answers before it is
trusted, and it should log what it rejects; the saved traces keep only the final answer, so a
rejected first attempt cannot be inspected afterwards.

## Evaluation

Agent run on all 34 questions (`eval/answers.jsonl`), structural design + dense search.

**Code checks:** at least one search per answer; refusal phrase present; citations in the
answer; citations not returned by search (0 invalid); whether the expected article is cited;
correct refusal (unanswerable and refused); wrong refusal (answerable and refused); guardrail
fired.

**Judge rubric (binary):** `correct` = 1 if the answer gives the reference answer's key facts
(figures, conditions) without contradicting it, or properly refuses an unanswerable question;
`supported` = 1 if every factual claim is backed by the retrieved passages. JSON output with a
one-sentence reason.

**Judge models.** The judge must be a different model from the agent's (`gemini-3.8-flash`,
fallback `gemini-3.5-flash-lite`). The free tier allows about 20 judge calls per model per day,
so when one model's daily quota ran out the next one took over: `gemini-3.5-flash` gave 19
verdicts, `gemini-3.6-flash` 3 and `gemini-3-flash-preview` 12. Each verdict records its model
in `eval/judge.csv`.

**Results.** The headline numbers are my labels (graded before seeing the judge); the judge's
are a cross-check.

| | my labels | judge |
|---|---|---|
| correct | **33/34** | 34/34 |
| supported | **34/34** | 34/34 |
| correct refusals | **7/7** | 7/7 |
| wrong refusals | **0** | 0 |
| invalid citations (code) | 0 | |
| citation guardrail fired | 0 | |
| answered by the fallback model | 34/34 | |

`gemini-3.8-flash` was overloaded (503) during the run, so every answer came from
`gemini-3.5-flash-lite`.

**Agreement with my labels (34 answers):**

| | agreement | Cohen's kappa | disagreements |
|---|---|---|---|
| correct | 0.97 | 0.00 | q23: judge 1, me 0 |
| supported | 1.00 | undefined | none |

Kappa is 0 or undefined because the judge gave 1 to all 34 answers on both criteria: with no
variation in one rater, kappa cannot measure agreement even at 33/34. The one disagreement is
an answer that is right in what it says but misses part of the reference answer, which the
judge did not penalise.

## Failures

By my labels, 1 of 34 answers failed:

| cause | count | questions |
|---|---|---|
| retrieval miss | 1 | q23 |
| wrong answer from the right passage | 0 | |
| unsupported claim | 0 | |
| wrong refusal | 0 | |
| bad test question | 0 | |

**q23** (two passages: *"Apart from the minimum capital, what extra safety cushion a bank
need?"*; reference: 4.5 % minimum plus a 2.5 % cushion). The agent made one search, "capital
buffer requirements combined buffer requirement CRD", which returned only CRD articles (128,
129, 133, 136, 141a). It gave the 2.5 % capital conservation buffer [CRD, Article 129(1)] and
the other buffers, but CRR Article 92, with the 4.5 % Common Equity Tier 1 minimum, never came
back, so the answer leaves it out. AGENTS.md rule 4 already says "for questions that combine
two topics, search each one"; the agent searched only one.

**What to fix first: search each topic.** Enforce rule 4 in code instead of leaving it to the
prompt: for a question with two parts, require one search per part before the agent answers.
Any change means running all 34 questions again and grading them again.

## Decision

Cost per question: **5 560 input + 245 output tokens, 22.9 s** on average, all from the
fallback model. The add-document demo answers took 143-206 s when the primary model was
overloaded.

**Would I let analysts rely on it?** Yes, but as a search tool and a first reading, not as the
final source. The results are good: 33 of 34 answers correct, all of them supported by the
passages, no made-up citations and no wrong refusals. The seven questions outside the corpus
were all refused correctly, even when the retrieved passages contained figures that looked like
an answer (for q34, the 55 % and 20 % of CRR Article 402 on exposures secured by residential
property). But the one failure worries me more than the number suggests. It is not an obvious
error but an incomplete answer that sounds complete: q23 gives the 2.5 % buffer and leaves out
the 4.5 % CET1 minimum. An analyst who trusts it without checking would not notice what is
missing. The agent searched only the CRD, so the CRR article with the 4.5 % never came back.
And 34 questions are a small sample to take the 97 % at face value.

**For which questions.** Yes for finding the applicable article and the main figure: a ratio, a
deadline, an amount or a limit. There it was almost always right and cites the exact article,
so it can be checked quickly. Not for deciding whether the bank complies. That decision depends
precisely on the conditions, exceptions and special cases, which is where a missing piece does
the most harm. It also depends not only on the EU text but on national law and the bank's own
data, which the assistant does not have. With questions that combine several articles or acts I
would be more careful: it got most of them right, but that is where a piece is most easily
missing, as in q23.

**Safeguards.**
- The analyst always opens the cited article before using the answer, reads all of it, and
  checks whether another article or act is also needed, because in q23 what was missing was in
  a different act.
- If the rule comes from a directive (CRD or MiFID II), the analyst checks the national
  transposing law, which the corpus does not include.
- Any conclusion about compliance, or anything going to a client or the supervisor, goes
  through the legal or compliance team.
- The system keeps being evaluated with more questions, especially combined ones and ones with
  exceptions, before its use is extended.

## AI use

I used Claude Code to write the code (`index.py`, `retrieval.py`,
`server.py`, `agent.py`, `evaluate.py`, `grade.py`), the subagent file and `AGENTS.md` from rules I chose. 

It asked me before every
design decision (corpus, user, chunking designs, rules, guardrail, models, rubric, fallback,
duplicate policy) and I chose the ones that I thought were more suitable for this assignment.
