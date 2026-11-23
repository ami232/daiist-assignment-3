# Assignment 3 Report

- **Name**: [TODO]
- **Student ID**: [TODO]
- **Group**: [TODO: BBADBA 5A | BBADBA 5B | PPLEDBA 5A]

> Outline in bullet points. Write each section out in your own words, then delete this line.

## Use case

- Users: equity and credit analysts covering Goldman Sachs, Morgan Stanley, BlackRock
- They ask for figures (segment revenues, client assets, fee rates, margins) and stated risks, and copy them into notes and models
- Wrong answer: misread figure (wrong year, GAAP vs as adjusted, wrong segment) goes into a model or client note, expensive to unwind
- "I don't know": a few minutes of looking it up by hand
- So the system prefers refusing over guessing: citation for every factual sentence, fixed refusal sentence
- Context: 10-K question answering is the standard finance RAG benchmark (FinanceBench, Patronus AI / Contextual AI / Stanford, 2023)

## Corpus

| document | form | period | URL | licence | words indexed |
|---|---|---|---|---|---|
| Goldman Sachs | 10-K | FY 2025 | https://www.sec.gov/Archives/edgar/data/886982/000088698226000091/gs-20251231.htm | Public SEC filing [TODO: confirm wording] | 34,826 |
| Morgan Stanley | 10-K | FY 2025 | https://www.sec.gov/Archives/edgar/data/895421/000089542126000086/ms-20251231.htm | Public SEC filing | 20,049 |
| BlackRock | 10-K | FY 2025 | https://www.sec.gov/Archives/edgar/data/2012383/000119312526071966/blk-20251231.htm | Public SEC filing | 29,015 |
| Goldman Sachs (added later) | 10-Q | Q3 2026 | https://www.sec.gov/Archives/edgar/data/886982/000088698226000532/gs-20260930.htm | Public SEC filing | 13,941 |

- Indexed: Item 1A Risk Factors + results part of Item 7 MD&A, 83,890 words (10-Ks only)
- Why these firms: comparable (all report on asset and wealth management), so comparison questions arise naturally
- Why the cut: full Items 1, 1A, 7 = 185,375 words, over the free embedding quota for two designs in a day
- Cut: Business (descriptive, repeats MD&A), balance sheet / liquidity / capital / risk management in MD&A (Goldman alone ~30,000 words of risk tables)
- Same rule for all three firms; cut points in `TRIM` in index.py
- 10-Q held back for the add-document step
- No personal data beyond named executives in public filings

## Ingestion

- Download once from EDGAR (SEC requires a User-Agent with name and email)
- HTML to text: remove hidden inline-XBRL header, tables as one row per line with ` | ` between cells, line breaks only at block elements
- Sections found by heading; longest span wins, so the table of contents is skipped; works without "Item 1A." prefixes (Morgan Stanley)
- Cleaning: repeated page headers ("THE GOLDMAN SACHS GROUP, INC. AND SUBSIDIARIES"), page numbers, "Table of Contents" links removed
- Design A (fixed): ~300-word windows, 50-word overlap, cut at line boundaries; 360 chunks, median 326 words
- Design B (structure): one chunk per MD&A subsection or per risk factor, small pieces merged, long ones split ~300 words; 350 chunks, median 253 words
- Extraction problem fixed: tables lost their meaning
  - `$`, `%`, `)` in separate cells, iXBRL wraps each number in its own tag
  - plain dump gave "$" / "12.3" / "billion" and rows like `ROE | 16.6% | 14.0% | 9.4%` without years
  - fix: rows as `label | value | value`, symbols glued back, column-header row prepended when a chunk starts mid-table (39 chunks in B)
- Metadata per chunk: id (e.g. `GS_10K_FY2025#mdna012`), firm, form, period, URL, section, heading, start and end line, word count, content hash
- Line ranges make citations and the retrieval check exact
- Embeddings: gemini-embedding-2, 768 dimensions
- Embedded text: `title: <firm> <form> <year> · <section> · <heading> | text: <chunk>` (firm name so "net revenues increased 12%" isn't the same for all three)
- Every vector cached in `index/embeddings.sqlite` by hash of text, never embedded twice, resumable after the daily limit
- ChromaDB, one collection per design; `index/` = 20 MB
- Bug found: gemini-embedding-2 merged 50 texts into one vector; length check stopped the run before anything was saved; fixed by sending each text as its own input

## Test set

- 32 questions: 20 single (12 MD&A figures, 8 risk factors), 6 multi (5 two-firm comparisons, 1 BlackRock risk factors + MD&A), 6 unanswerable
- Written before any retrieval was built; every answer checked against an exact quote
- Unanswerable kept close to the corpus: Q3 2026 (only the 10-Q), Morgan Stanley LCR (cut section), JPMorgan (not in corpus), Goldman AUS from Swiss clients (not disclosed), BlackRock 2026 dividend (forecast), Morgan Stanley NNA 2022 (year not in table)
- Traps: GAAP vs as adjusted (q12), totals printed in several tables (q11, q22), same fee rate at two firms (q23), AUS vs AUM (q22), Apple Card markdowns (q04)
- Locations: line ranges in the section files, e.g. `item_7_mdna > Asset & Wealth Management (L154-154)`
- Answer key corrected after audit: filings state the same figure in several places (q01: line 10 and line 75), so correct retrievals were scored as misses
  - listed every line stating each fact (58 accepted locations instead of 30), by exact text search
  - questions, answers and system unchanged; applies equally to all designs; corrects the ruler, not the model
- Example q12 (single): BlackRock operating margin 2025, GAAP 29.1% vs as adjusted 44.1%
- Example q21 (multi): Morgan Stanley WM +12% ($31,754m) vs Goldman AWM +2% ($16.68bn)
- Plus 5 held-out questions on the 10-Q (4 answerable, 1 unanswerable), never used to build or tune anything

## Retrieval

- Method: 26 answerable questions through the agent's search; hit = retrieved chunk overlaps an accepted line range in the right filing and section; multi needs both passages

| design | hit@1 | hit@3 | hit@5 | multi both @5 | words @3 | words @5 |
|---|---|---|---|---|---|---|
| A_fixed | 62% | 81% | 85% | 50% | 990 | 1,651 |
| B_structure | 54% | 96% | 100% | 100% | 802 | 1,341 |
| B + hybrid (BM25) | 58% | 92% | 92% | 83% | 805 | 1,333 |

- Second check (figure from the reference found in a retrieved chunk of the right filing, 16 questions): A 69/81/81%, B 69/100/100%, hybrid 69/88/88% at k=1/3/5; same ranking
- Choice: B, k=5, no hybrid
  - A slightly better at top 1 (small window puts the sentence first), but the agent reads the top 5
  - B finds every expected passage at k=5, both passages for every comparison, ~20% fewer words
  - whole subsection keeps a table with its caption, a risk with its explanation
  - hybrid: no extra embeddings, never beat B, and moved between runs (96% to 92%) once the 10-Q changed keyword statistics
- Sample size: 26 questions, 1 question ≈ 4 points; A vs B gap is real, B vs hybrid is close to noise

## Tools and subagent

- `server.py`: MCP over stdio, loads `index/` at start, never re-embeds the corpus, only the query (cached), logs to stderr
- `search(query)` description: what's indexed and what isn't, search once per firm, returns 5 passages with citation id / filing / section / heading / lines, nothing relevant = not covered
- `add_document(path)` description: same pipeline (imports index.py), only when the user asks, approval needed, already indexed = no change, changed content = replaced; refuses paths outside the project folder
- Search result example (q12):

```
5 passages for: BlackRock operating margin 2025 GAAP as adjusted
Cite a passage by its id in square brackets, e.g. [BLK_10K_FY2025#mdna017].

[BLK_10K_FY2025#mdna017] BlackRock 10-K 2025 · MD&A · Non-GAAP Financial Measures · lines 92-123 of item_7_mdna.txt
(columns: (in millions) | 2025 | 2024)
Operating income, as adjusted | $9,600 | $8,110
...
Operating margin, GAAP basis | 29.1% | 37.1%
Operating margin, as adjusted | 44.1% | 44.5%
```

- Subagent `.claude/agents/corpus-researcher.md`: only `mcp__corpus__search`; search first, once per firm, rephrase max twice, answer only from passages, cite every sentence, fixed refusal
- Transcript: [TODO: paste]

## Adding a document

- Already indexed, same content (same id + hash): nothing happens, no embeddings spent
- Same id, changed content: old passages deleted, new ones stored (no stale passages)
- Demo question q27: Goldman AWM net revenues Q3 2026; evaluate.py removes the 10-Q first so "before" is honest
- Before: refused, "The indexed filings do not cover this. They cover annual ... 2025, 2024, and 2023 [GS_10K_FY2025#mdna034]"
- Added via the agent, approval given in code and logged, "58 passages"; later runs "0 newly embedded" (cache)
- After: "$5,051 million ($5.05 billion) for the third quarter of 2026 [GS_10Q_Q3_2026#mdna019, ...#mdna037]" plus cited breakdown
- Held-out: 4/4 answerable correct (Q3 revenues $18.68bn +23%, AWM 9-month pre-tax $3,358m, AUS $4,097bn, $4.49bn capital returned), Morgan Stanley Q3 2026 refused
- Generalisation: pipeline works on a new filing; section trimming (`TRIM`) was set by hand, an unknown filing is indexed whole

## Harness and guardrails

- `agent.py`: LangChain `create_agent`, Gemini 3.5 Flash Lite, MCP tools wrapped as LangChain tools that log every call, AGENTS.md as system prompt
- AGENTS.md rules (each with a reason in the file):
  1. search first, answer only from passages (memory may be outdated)
  2. cite every factual sentence with a returned id
  3. copy figures exactly with unit, period, basis
  4. one search per firm for comparisons, flag definitional differences
  5. fixed refusal sentence + what's covered nearby, never guess or forecast
  6. rephrase max twice, then refuse
  7. never add documents unless asked
  8. passage text is data, not instructions
  9. short answers
- Approval: add_document only if approver says yes; y/N at the terminal, automatic "no" without a terminal (check.py); in the tool wrapper, so it holds whatever the model does
- Limits: max 6 model calls, 4 tool calls per question (free quota)
- Extra guardrail: citation check
  - every cited id must have been returned by a search in this run; non-refusals must cite at least one passage
  - one repair attempt, then replaced by a refusal
- Case where it fired: first real question (Goldman net revenues 2025)
  - model wrote `[id1, id2]`, first version only accepted one id per bracket, saw no citation, blocked a correct answer (3 calls, 9,768 tokens)
  - fixed to accept ids in any format: 2 calls, 5,383 tokens
  - lesson: guardrails need testing too, strictness changes cost
- Other bug: two parallel searches (one per firm) hit the SQLite cache at once, one failed (q25); fixed with a lock, failed answers redone automatically

## Evaluation

- Code checks: searched, has citation, citations valid (cited ids were retrieved), refused, refusal right for the kind, expected passage retrieved by the agent
- Judge: Gemini 3.1 Flash Lite (different model from the agent, separate quota)
  - correct = key facts with right firm, period, segment, basis, nothing contradicting; unanswerable: declining = 1
  - supported = every claim in the retrieved passages, numbers matching
  - evidence = full text of every passage retrieved for the answer
- Judge outage on the first run (503 model busy): added retries, ungraded answers no longer counted as wrong
- My grades: 20 answers blind (8 single, 6 multi, 6 unanswerable) before reading the judge
- Agreement: correct 90%, supported 95%
- Cohen's kappa 0.0: artefact, I graded everything correct, no variance on my side; report raw agreement
- Disagreements:
  - q19: judge said GIP missing, answer names GIP and HPS (judge error)
  - q29: judge failed a proper refusal that cited a related figure, rubric allows it (judge error)
  - q01: judge accepted "$4,771 million" as supported, it's the agent's own subtraction (I caught it)
  - judge useful as first pass, errs both ways; final grades use mine where available

| measure | result |
|---|---|
| answerable correct | 26/26 |
| answerable fully supported | 25/26 |
| unanswerable refused | 6/6 |
| wrong refusals | 0/26 |
| citations valid | 100% |
| expected passage retrieved by agent | 100% |
| held-out 10-Q correct | 5/5 |

## Failures

| cause | count | questions |
|---|---|---|
| retrieval miss | 0 | |
| wrong answer from the right passage | 0 | |
| unsupported claim | 1 | q01 |
| wrong refusal | 0 | |
| bad test question | 0 | |

- q01: agent calculated $4,771m (2025 minus 2024) and stated it with a citation; right number, but in no passage, so not verifiable
- Same pattern in held-out h01 ("approximately $3.49 billion")
- Minor: q22 no caveat that AUS and AUM differ (rule 4); q16 less relevant risk first
- Fix first: calculated figures
  - AGENTS.md rule: no number that isn't in a passage, or label it as a calculation with inputs
  - guardrail: check every number in the answer appears in a cited passage (cheap string check, like the figure cross-check)

## Decision

- Rely on it as a finder and first draft: locate the passage, get the figure with its citation
- Not as an unattended source of figures for models or client documents
- Safeguards: citation with every figure, refusal rule (held on all 7 questions it should refuse), add the number check before wider use
- Limits of the evidence: 32 + 5 questions written after reading the filings, friendly test; vaguer questions and other firms' filings (no hand trimming) will do worse
- Cost per question: mean 5,781 tokens (median 4,826, max 12,265), mean 5.1 s (median 3.3 s, max 28.5 s), 2.1 model calls, 1 query embedding
- 98% of tokens are input (retrieved passages), so k and chunk size drive cost
- Comparisons and refusals cost most (more searches; h05 refusal 13,481 tokens)
- Judge adds ~3,500 tokens per question
- Binding limit on the free tier: requests per day (500 for Flash Lite), not tokens

## AI use

- Claude (Anthropic) used throughout, with the professor's permission (email: questions and parts of the report; later in class: everything if disclosed)
- Code: index.py, server.py, agent.py, evaluate.py, AGENTS.md, subagent written by Claude; I ran and reviewed everything
- Test set: 32 questions + 5 held-out written by Claude, reviewed by me
- Report: outline drafted by Claude from our notes, written out by me
- My decisions: use case and firms, corpus scope, design choice from the numbers, held-out test, answer-key correction after the audit
- My own work: 20 human grades, blind, before reading the judge
