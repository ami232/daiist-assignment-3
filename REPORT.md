# Assignment 3 Report: an EU drone-rules assistant you can check before you fly

- **Name**: Sergio García
- **Student ID**: 19912
- **Group**: BBADBA 5B

All numbers come from files written by the pipeline: `index/manifest.json`, `eval/retrieval_summary.json`,
`eval/results.csv`, `eval/answers.jsonl`, `eval/judge_verdicts.jsonl`, `eval/summary.json` and
`eval/add_document_demo.json`.

---

## Summary

A RAG assistant answers EU drone-law questions for the operations manager of a small drone-services
company, using the four EU drone regulations (53,714 words). The corpus is cut into one chunk per article
or annex point and searched with dense Gemini embeddings. That design won the retrieval comparison:
hit@1 0.70, hit@3 0.87 and hit@5 0.90, against 0.27 / 0.53 / 0.70 for fixed 200-word chunks.

The LangChain harness answers through the MCP `search` tool, cites chunk ids, and refuses rather than
guesses. On 36 test questions it scored as follows.

**LLM judge:**
- 30/30 answerable questions correct and supported.
- 5/6 clean refusals on the unanswerable questions.
- 1 refusal that added a claim not in the corpus.
- 100 % of citations valid.

**My own grades** (22 answers, graded before seeing the judge): I agree with the judge on 91 % for
correctness and 95 % for support. Every disagreement is the judge being more lenient. I found 4 problems:
- two incomplete multi-passage answers (m02, m06), both retrieval misses;
- two refusals that added an unsupported sentence (u04, u05).

**Cost:** about 6,000 tokens and 10 s per question (≈ $0.0017 at paid prices).

**Decision:** let users rely on it to **find and read the right article**, but not as the final go/no-go
authority. The safeguard is that the user opens the cited article before acting.

---

## Use case

**Who asks.** The operations manager (or remote pilot) of a small Spanish drone-services company
(inspections, filming, surveying), before accepting or planning a job. For example: "Can our C2 drone fly
20 m from people?", "Do we need to register?", "What does the pilot need?".

**What they do with the answer.** They decide go / no-go, choose the operational category and paperwork,
and brief the pilot.

**Wrong answer vs. "I don't know".**
- *Wrong but confident:* an illegal flight. That means an administrative sanction, insurance that does not
  cover the flight, and liability if someone is hurt. A wrong "no" also costs a lost job.
- *"I don't know":* someone spends time reading the regulation or asks a consultant, i.e. minutes to an
  hour of skilled time.

That makes refusing much cheaper than guessing. So the system is designed to refuse when evidence is
missing, to cite the exact article for every claim, and the evaluation focuses on unsupported claims.

**Volume (scenario).** Roughly 10–30 questions per week for a small operator.

The provisional version of this framing was written before choosing the corpus. The only refinement is the
volume estimate.

## Corpus

| document | source (official XHTML) | date | licence | words* |
|---|---|---|---|---:|
| Commission Implementing Regulation (EU) 2019/947, operating rules (open/specific/certified, A1–A3, competency, registration, authorisations, LUC) | https://eur-lex.europa.eu/eli/reg/2019/947/oj/eng | 2019-05-24 | © European Union, reuse authorised (Commission Decision 2011/833/EU) | 12,591 |
| Commission Delegated Regulation (EU) 2019/945, drone classes C0–C4, technical requirements, remote ID, CE marking | https://eur-lex.europa.eu/eli/reg/2019/945/oj/eng | 2019-03-12 | same | 20,710 |
| Commission Delegated Regulation (EU) 2020/1058, amends 2019/945, adds classes C5–C6 | https://eur-lex.europa.eu/eli/reg/2020/1058/oj/eng | 2020-04-27 | same | 13,275 |
| Commission Implementing Regulation (EU) 2021/664, U-space | https://eur-lex.europa.eu/eli/reg/2021/664/oj/eng | 2021-04-22 | same | 7,138 |
| **Total** | | | | **53,714** |

\*Words after cleaning (headers and footnotes removed).

The documents are public legal acts with no personal data. Regulation (EU) 2020/639 (standard scenarios)
was deliberately left out, so it could be added later with `add_document` (see "Adding a document").

## Ingestion

**Extraction.** `index.py` downloads the official English XHTML from the EU Publications Office (cellar).
EUR-Lex itself answers scripted downloads with a bot challenge (HTTP 202, empty body). The text is then
walked in document order, tracking the current Article (with its title) or Annex point
(e.g. `Annex, UAS.OPEN.030 …`). Headers, footnotes and the signature block are dropped.

**Two extraction problems I fixed.**
1. **List labels separated from their text.** EUR-Lex lays out list items as two-cell table rows: "(a)" in
   one cell, the sentence in the other. Paragraph-by-paragraph extraction left every "(a)" on its own line.
   Each innermost table row is now joined into one line.
2. **Text outside paragraphs.** Some rows put their text directly in the cell, with no `<p>`. Reading only
   `<p>` elements produced empty chunks; for example "UAS.STS-01.010 General provisions: (1) (2) (3) (4)" in
   2020/639. I now read every text node that belongs to the row and not to a nested table. This changed 72
   chunks; only those were re-embedded.

**Chunking (two index designs).**

| design | rule | chunks | mean words |
|---|---|---:|---:|
| structure | one chunk per article or annex point; longer than 300 words → 220-word windows with 40 overlap; each chunk starts with its citation header, e.g. "Regulation (EU) 2019/947, Annex, UAS.OPEN.030 UAS operations in subcategory A2 (part 1/2):" | 358 | 179 |
| fixed | plain text in 200-word windows with 30-word overlap, ignoring structure | 316 | 200 |

**Chunk metadata:** `source`, `doc_id` (CELEX), `location`, `covers` (all sections a chunk spans), `url`,
`design`, `origin` (`corpus` / `added`), `words`, `content_hash`.

**Embedding.** `gemini-embedding-2` at 768 dimensions, task types RETRIEVAL_DOCUMENT / RETRIEVAL_QUERY.
Vectors are stored in ChromaDB (`index/chroma`) and in `index/embedding_cache.jsonl`, keyed by text hash.

- Every vector is written as soon as it arrives, so the daily limit or a crash loses nothing.
- `main.py index` embeds only texts without a saved vector.
- The server never re-embeds the corpus.

A bug I found: `gemini-embedding-2` is multimodal. A plain list of strings is treated as *one* content and
returns a single vector. Each text must be sent as its own `Content`; the code now asserts that the number of
vectors matches. The index is 22 MB.

## Test set

I wrote 36 questions in `eval/questions.csv` from the documents, before tuning anything, and phrased them the
way the operations manager would ask.

| kind | n | description |
|---|---:|---|
| single | 24 | one passage (e.g. q07: distance from people in A2) |
| multi | 6 | two passages, e.g. m03: C1 mass/energy limit (2019/945 Annex) + A1 pilot training (2019/947 UAS.OPEN.020) |
| unanswerable | 6 | close to the topic but not in the corpus: national fines, insurance amounts, AESA night rules, fees, and two about standard scenarios (answered only by 2020/639) |

Examples:
- **q07** "In subcategory A2, how far must the drone stay from uninvolved people?" → "At least 30 m
  horizontally; down to 5 m with active low-speed mode after assessing weather, performance and segregation"
  (2019/947, UAS.OPEN.030).
- **u03** "What fine does AESA impose in Spain for flying a drone without registering?" → should refuse:
  the corpus is EU-only.

## Retrieval

Hit = the expected passage (source + article/annex point) is in the top k. For `multi`, *both* passages must
be in the top k. Thirty answerable questions; the search is exact cosine (see below).

| search design | hit@1 | hit@3 | hit@5 | multi: both in top 5 | words added to the prompt (k=5) |
|---|---:|---:|---:|---:|---:|
| fixed-dense (200-word windows) | 0.27 | 0.53 | 0.70 | 3/6 | 999 |
| **structure-dense (chosen)** | **0.70** | **0.87** | **0.90** | 3/6 | 1,059 |
| structure-hybrid (dense + BM25, reciprocal-rank fusion) | 0.70 | 0.80 | 0.87 | 3/6 | 1,051 |

**Choice: structure-dense.** It is best at every k for about 60 extra words per question.

- **Why structure helps:** the citation header puts the article and annex-point name, such as
  "UAS operations in subcategory A2", inside the embedded text, so a question naming the topic lands on the
  right chunk.
- **Why hybrid did not help:** BM25 rewards repeated legal words ("operator", "Article") that appear
  everywhere, which pushed a few right chunks down.
- **The weak spot is multi-passage questions:** only 3 of 6 have both passages in one top-5. The agent
  compensates by searching more than once (25 % of questions, 9/36, used 2 or more searches).

**A measurement issue I fixed.** Chroma's default HNSW query is approximate: two identical runs gave hit@5 of
0.90 and 0.87. With 358 chunks, exact cosine over all vectors is instant and deterministic, so `rag.search`
now does that. Chroma remains the store.

## Tools and subagent

**MCP server (`server.py`, server name `corpus`).** It loads `index/` at startup and logs only to stderr.

- **`search(query)`** — tool description: *"Search the EU drone (UAS) regulations corpus: Implementing
  Regulation (EU) 2019/947 (operating rules …), Delegated Regulation (EU) 2019/945 and its amendment
  2020/1058 (drone classes C0–C6 …), and Implementing Regulation (EU) 2021/664 (U-space) … Returns the 5
  most relevant passages, each headed by its citation: [chunk id] regulation | article or annex point. Cite
  those ids. If nothing relevant is returned, the corpus does not cover the question."*
- **`add_document(path)`** — *"Add one document to the drone-regulation index … If the identical file is
  already indexed nothing is done; if a different version of the same document is indexed, the old chunks
  are replaced."* It imports `chunk_file`, `embed_and_store` and `add_file` from `index.py`; it does not
  rewrite them.

**One search result** (query by the agent for q07: "subcategory A2 distance uninvolved people"), first hit:

```
[32019R0947-s0049] Regulation (EU) 2019/947 | Annex, UAS.OPEN.030 UAS operations in subcategory A2 (part 1/2)
Regulation (EU) 2019/947, Annex, UAS.OPEN.030 UAS operations in subcategory A2 (part 1/2): UAS operations in
subcategory A2 shall comply with all of the following conditions: (1) be conducted in such a way that the
unmanned aircraft does not overfly uninvolved persons and the UAS operations take place at a safe horizontal
distance of at least 30 metres from them; the remote pilot may reduce the horizontal safety distance down to a
minimum of 5 metres ...
```

**Subagent (`.claude/agents/corpus-researcher.md`).** Its only tool is `mcp__corpus__search`. Its
instructions:
- search, and search again with different wording if needed;
- answer only from the returned passages, citing `[chunk id] Regulation, Article`;
- reply exactly "The corpus does not cover this question." when not covered, or name the uncovered part;
- keep to about 150 words.

**Transcript from my editor:**

Run in VS Code with GitHub Copilot (Chat, custom agent `corpus-researcher`, model auto-routed to GPT-6 Luna).
The MCP server `corpus` showed "Running | 2 tools":

> **Me:** Can a class C2 drone fly 20 m from uninvolved people in subcategory A2?
>
> *Completed 3 steps in 8s.* Auto routed task to GPT-6 Luna.
> "I'll check the corpus for the A2 horizontal-distance rule and the specific C2 condition, then answer only
> from the returned passages."
>
> **corpus-researcher:** The corpus does not cover this question. Check with the competent authority or the
> applicable national law.

**What this transcript shows.** The trace contains no `search` call. The subagent had no working search tool:
its frontmatter named the tool in Claude Code's format (`mcp__corpus__search`), and Copilot exposes MCP tools
as `corpus/search`.

- **What went right:** with no evidence, it followed its instructions and refused instead of answering from
  memory. That is the safe failure mode for this use case. The correct answer is in the corpus (UAS.OPEN.030:
  at least 30 m, or 5 m with low-speed mode), and the harness `agent.py` answers this question correctly
  (questions q07 and m01).
- **The fix:** I added the Copilot name, so the frontmatter now reads
  `tools: mcp__corpus__search, corpus/search`.
- **Not re-run:** I did not record a second transcript after the fix, so whether the subagent now retrieves
  correctly in Copilot is untested.

## Adding a document

**Already-indexed policy** (implemented in `index.add_file`):
- Documents are matched by document id (CELEX number).
- **Same content hash** → nothing is done: no embeddings spent, no duplicates.
- **Different content** (a new version of the same act) → the old chunks are deleted and the new ones stored.

Added documents are marked `origin: added`. The base evaluation hides them (`CORPUS_EXCLUDE_ADDED=1`), so
it stays reproducible.

**Demo** (`eval/add_document_demo.json`), unanswerable question **u01**: *"How long does an operational
declaration for a standard scenario remain valid?"*

- **Before:** "The corpus does not cover the validity period or expiration duration of an operational
  declaration for a standard scenario. You should check with your national competent authority…" (correct
  refusal).
- **`add_document("corpus/32020R0639.xhtml")`**, i.e. Regulation (EU) 2020/639, returned: "Added Regulation
  (EU) 2020/639: 89 chunks embedded and stored in the 'structure' index…"
- **Calling it again** returned: "Already indexed: 32020R0639 (89 chunks, same content). Nothing was added or
  re-embedded."
- **After:** "an operational declaration for a standard scenario has a limited duration of **2 years**
  [32020R0639-s0037]. The declaration is no longer considered complete if … oversight finds the operation
  is not conducted in accordance with the declaration … conditions have changed … access is not granted"
  (Annex point UAS.SPEC.085).

## Harness and guardrails

`agent.py` uses LangChain `create_agent` on `gemini-flash-lite-latest`, temperature 0. Its tools are loaded
from `server.py` over MCP (stdio), and `AGENTS.md` is the system prompt.

**AGENTS.md rules, each with its reason in the file:**
1. Search before answering.
2. Answer only from the search results.
3. Cite every claim with the returned chunk id.
4. If the corpus does not cover it, say exactly "The corpus does not cover this question." plus where to
   look.
5. With partial coverage, say what is not covered.
6. Prefer the amending text (2020/1058 over 2019/945).
7. Keep answers short and operational.
8. Never add documents on your own initiative.

**Approval step.** The `add_document` wrapper asks *"Approve? [y/N]"* in the terminal before calling the
MCP tool. In a scripted run it needs `AGENT_APPROVE=yes`; without a terminal it refuses.

Tested with `AGENT_APPROVE=no uv run python main.py ask "Please add the document corpus/32020R0639.xhtml
to the index."`:
- the harness logged `[approval] add_document('corpus/32020R0639.xhtml') denied`;
- the agent replied "The human reviewer did not approve adding the document … so it has not been added."

This test exposed a bug, now fixed: the citation guardrail first replaced that reply with a misleading "The
corpus does not cover this question." Replies that only report an `add_document` outcome are now exempt from
the citation requirement.

**Call limits.** At most 8 model calls and 6 tool calls per question (LangChain middleware).

**Extra guardrail: citation verification.**
- Every `[chunk id]` in the final answer must be one that `search` actually returned in this run.
- A non-refusal answer must cite at least one id.
- Otherwise the draft is withheld and replaced by a refusal. The reason is that for this user an
  unverifiable answer is worse than "I don't know".

**Where it fired: u02** ("maximum ground speed in STS-01"). The agent searched 6 times for "STS-01", the call
limit stopped it, and the draft ("Tool call limit reached…") had no citation. The guardrail returned "The
corpus does not cover this question. (The harness withheld a draft answer: answer without any citation…)".
That is the correct outcome. Across the 36 runs, no answer cited an id that search had not returned.

## Evaluation

**Code checks** (`evaluate.code_checks`):
- refusal detected by the fixed phrase;
- all citations returned by search: **100 %**;
- answer has a citation;
- expected passage retrieved during the run: **96.7 %** of answerable questions;
- expected document cited when answering: **96.7 %**.

**LLM judge.** The model receives the question, my reference answer, the agent's answer and the retrieved
passages as evidence, with this rubric (full text in `evaluate.JUDGE_RUBRIC`):
- **correct** = same essential facts as the reference (numbers, limits, yes/no), nothing contradicting it;
  for unanswerable questions, only a refusal is correct.
- **supported** = every factual claim is in the evidence. Something true in the real world but absent from
  the evidence is 0.

Code decides what code can: refusals on unanswerable questions are correct refusals, and refusals on
answerable ones are wrong refusals. The judge decides correctness and support.

Judge models: `gemini-3-flash-preview`, a stronger model than the agent's, for 14 answers. Its free daily
quota ran out, so `gemini-3.5-flash-lite` judged the other 22. Each verdict records its model.

**Results** (36 questions):

| outcome | n |
|---|---:|
| correct (answerable) | 30 / 30 |
| unsupported answer | 0 |
| wrong refusal | 0 |
| correct refusal (unanswerable) | 5 / 6 |
| refusal with an unsupported claim (u05) | 1 / 6 |

By kind: single 24/24, multi 6/6, unanswerable 5/6.

**My agreement with the judge.** I graded 22 answers myself (`eval/human_labels.csv`) before reading the
judge's verdicts: 10 single, all 6 multi and all 6 unanswerable.

| dimension | agreement | Cohen's κ | disagreements |
|---|---:|---:|---|
| correct | 20/22 = **91 %** | 0.00 | m02, m06: I marked both incomplete, the judge marked them correct |
| supported | 21/22 = **95 %** | 0.65 | u04: I marked an unsupported claim, the judge did not |

- **Why κ is 0 for correctness despite 91 % agreement:** the judge said "correct" for every one of the 22, so
  agreement is no better than chance by construction. That is the useful finding: **the judge never failed an
  answer on completeness**, while I failed two.
- **The pattern:** every disagreement goes the same way, with the judge more lenient than me. So the judge's
  scores are an upper bound.

**Reading the 30/30 with care.** A perfect judge score on 30 questions does not mean the error rate is zero:
with 0 errors in 30, the 95 % upper bound is about 11 %. My own grades found 4 problems in the 22 answers I
graded (m02, m06, u04, u05). The judge accepted 3 of them; it caught only u05.

## Failures

| question | judge said | what actually happened (my grade) | cause |
|---|---|---|---|
| m02 (open requirements not met → what do we need?) | correct, supported | **Incomplete:** presents the operational authorisation as the only route and omits the standard-scenario declaration and the LUC alternative. Article 5 is split into two chunks; the agent retrieved part 1 (s0017) but not part 2 (s0018), where those alternatives are. The hit-rate metric counted it as a hit, because "Article 5" was found. | retrieval miss (second part of the article) |
| m06 (1.5 kg drone without class label) | correct, supported | **Incomplete:** cites Article 20 (A3 allowed if placed on the market before 1 July 2022) but omits the A3 conditions: no uninvolved person endangered, 150 m from residential/commercial/industrial/recreational areas. One search; UAS.OPEN.040 was not retrieved. | retrieval miss (second passage) |
| u04 (minimum insurance for a 20 kg drone) | correct refusal, supported | Refused correctly, but adds that insurance "is typically set at the national level", which is not in the corpus. | unsupported claim |
| u05 (AESA night flights) | correct refusal, **unsupported** | Refused correctly, then added an AESA street address that is not in the corpus. It appears to be an outdated address, exactly the kind of confident detail this user cannot afford. | unsupported claim |
| m04 (remote ID data) | correct, supported | Correct, but my reference answer was outdated: 2020/1058 adds the time-stamp and emergency status to C1 direct remote ID, which I had attributed only to the U-space network service. The agent followed the amended text (rule 6). | bad test question |
| u02 (STS-01 speed) | correct refusal | Correct, but only thanks to the call limit plus the citation guardrail after 6 fruitless searches (27.9 s). | guardrail working, not a failure |

**Counts:**

| cause | n |
|---|---:|
| retrieval miss | 2 (m02, m06) |
| unsupported claim | 2 (u04, u05) |
| bad test question | 1 (m04) |
| wrong answer from the right passage | 0 |
| wrong refusal | 0 |

Both retrieval misses are **multi-passage questions where the agent searched only once**. Both unsupported
claims are **extra "helpful" sentences added after a correct refusal**.

**Fix first:**
1. **Multi-passage retrieval.** Only 3/6 questions get both passages in one search, and m02/m06 failed exactly
   there. Let the agent decompose compound questions into one search per sub-question (rule in AGENTS.md).
   Also return the sibling parts of a split article together, so retrieving "Article 5 (part 1/2)" brings
   part 2 with it.
2. **Strip uncited sentences from refusals** (u04, u05). Extend the guardrail so any sentence after the refusal
   phrase is removed unless it is a fixed pointer such as "ask the competent authority".
3. **Judge completeness.** Add "omits a condition that the reference lists" to the rubric (all three
   disagreements with my grades were about completeness), and use the same strong judge model for every
   answer.

## Decision

**Would I let users rely on it?** Yes, as a **research assistant that finds and quotes the right article**.
No, as the final authority for a go / no-go decision.

**Why, with numbers.** Two scenario costs per question:
- **Human research** (the "I don't know" path): about 15 min of the operations manager at about EUR 40/h
  (Eurostat 2024 euro-area average hourly labour cost EUR 37.3, rounded up) ≈ **EUR 10**.
- **Acting on a wrong answer:** illegal flight, sanction, insurance problem; assumed **EUR 2,000** as an
  expected value. This is a scenario figure, not a measured one.

**Without a safeguard.** Expected cost = p_wrong × 2,000 + p_refuse × 10 + run cost, where
p_refuse ≈ 6/36 ≈ 0.17. It beats doing all research by hand (EUR 10) only if p_wrong is below about
**0.4 %**. Even my optimistic estimate is above that:
- 4 problems in the 22 answers I graded myself (≈ 18 %; 2 incomplete, 2 with an unsupported extra sentence),
  or 0/30 by the judge with an upper bound of ≈ 11 %.
- Blind reliance is therefore not justified.

**With the safeguard.** The user opens the cited article (one click; ~3 min ≈ EUR 2) before acting. Most
errors become visible and the expected cost is ≈ EUR 2 + 0.17 × 10 ≈ **EUR 3.7 per question**, against
EUR 10 for manual research. Citations are always real ids (100 % valid; enforced by the guardrail), so
checking is cheap. Refusals ("the corpus does not cover…") send the user to the authority, which is the
right behaviour.

**Scope limits to state to users:**
- EU rules only (no Spanish national rules, fines, insurance amounts or fees).
- The corpus contains original texts plus amendments, not consolidated versions.
- Standard scenarios are only covered after adding 2020/639.

**Cost and latency per question** (agent only, 36 questions):

| metric | value |
|---|---|
| model calls / searches | mean 2.6 / 1.5 |
| tokens | mean 5,964 (5,790 in, 174 out), max 40,016 |
| latency | mean 10.5 s, median 8.4 s, max 29.9 s |
| money | free tier here; ≈ $0.0017 per question at the paid list price of Gemini 3.1 Flash-Lite ($0.25 in / $1.50 out per 1M tokens) |

The judge adds about 2,400 tokens per graded answer. Note that on the free tier Google may use the prompts to
improve its products, so a paid key is advisable if questions include client details.

## Key decisions and trade-offs (for the comprehension check)

1. **Use case with an asymmetric error cost.** A refusal costs ~EUR 10 of reading; a wrong answer can cost
   thousands. So the whole design favours refusing and citing.
2. **Structure-based chunks with a citation header.** They won by the numbers (hit@1 0.70 vs 0.27), because
   the header puts the article topic into the embedding.
3. **Dense over hybrid.** BM25 did not help on legal text full of repeated words (hit@5 0.87 vs 0.90).
4. **Exact search instead of approximate HNSW.** It is reproducible and instant at this size.
5. **Citation guardrail.** It is code-checkable, it fired correctly on u02, and it guarantees that every
   citation can be opened.
6. **Already-indexed policy.** Same file → no-op; new version → replace.
7. **Evaluation honesty.** The judge's 30/30 overstates quality. My own grades agree 91 % on correctness, but
   every disagreement is the judge being too lenient on completeness. Failures: 2 retrieval misses, 2
   unsupported claims, 1 bad test question.

## Reproduction

```bash
uv sync
cp .env.example .env            # GEMINI_API_KEY=...
uv run python main.py index     # downloads the corpus to corpus/, embeds only chunks without a saved vector
uv run python main.py ask "Can a class C2 drone fly 20 m from people in A2?"
uv run python main.py evaluate  # retrieval + agent + judge + agreement + demo; resumes from eval/ caches
uv run python check.py
```

- **Models:** `gemini-embedding-2` (768 dims), agent `gemini-flash-lite-latest`, judge
  `gemini-3-flash-preview` with `gemini-3.5-flash-lite` as fallback.
- **Code layout:**
  - `rag.py`: shared retrieval;
  - `index.py`: ingestion and the add-document pipeline;
  - `server.py`: MCP;
  - `agent.py`: harness;
  - `evaluate.py`: evaluation.

## AI use

I used Claude (Anthropic, Cowork mode) for most of this assignment. It:
- proposed the use case (EU drone rules) and the corpus after I asked it to pick an original one;
- wrote the code (`rag.py`, `index.py`, `server.py`, `agent.py`, `evaluate.py`, AGENTS.md, the subagent);
- drafted the 36 test questions and their reference answers from the documents;
- ran the indexing and the evaluation;
- reviewed the answers and drafted this report.

My part:
- created the Gemini key and the folder;
- graded 22 answers myself in `eval/human_labels.csv`, with my notes on the four I failed, before seeing the
  judge;
- ran the subagent in my editor;
- am responsible for being able to explain and defend every decision above.

