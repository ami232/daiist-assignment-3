# Assignment 3 Report

- **Name**: Ainhoa Olaechea
- **Student ID**: 18680
- **Group**: BBADBA 5A

## Use case

**Who asks:** a compliance analyst at a UCITS management company. Before a portfolio manager executes a trade
or the firm changes a process, the analyst checks whether it complies with the EU UCITS rules (investment and
diversification limits, eligible assets, derivatives, borrowing, organisation and conflicts of interest, key
investor information).

**What they do with the answer:** approve, block or escalate the decision, citing the article.

**Cost of a wrong answer vs "I don't know":** a wrong answer (e.g. a 10% limit stated as 20%) can lead to a
limit breach, a forced sale at a loss, a regulatory sanction and harm to investors. "I don't know" only means
the question goes to the legal team, a delay of hours. So the assistant must prefer refusing to guessing, and
every answer must carry a citation the analyst can check.

## Corpus

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| Directive 2009/65/EC (UCITS Directive) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32009L0065 | 13 Jul 2009 | EU legal texts, reuse allowed with source (Commission Decision 2011/833/EU) | 39,353 |
| Commission Directive 2007/16/EC (eligible assets) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32007L0016 | 19 Mar 2007 | same | 5,340 |
| Commission Directive 2010/43/EU (organisation, conflicts of interest, risk management) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32010L0043 | 1 Jul 2010 | same | 13,875 |
| Commission Regulation (EU) 583/2010 (key investor information) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32010R0583 | 1 Jul 2010 | same | 8,369 |
| **Total** | | | | **66,937** |
| *Added later with add_document:* Directive 2014/91/EU (UCITS V) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32014L0091 | 23 Jul 2014 | same | – |

All documents are public EU law and contain no personal data. The corpus holds the original texts, not the
consolidated versions, so later amendments are deliberately left out (this is what makes some test questions
unanswerable).

## Ingestion

**Extraction:** `index.py` downloads each act as HTML from the EU Publications Office (Cellar), the same text
EUR-Lex shows, into `corpus/` (git-ignored). Text is extracted with BeautifulSoup and cleaned (whitespace and
non-breaking spaces normalised, list markers like "(a)" joined to their text).

**Structure:** the text is split into Recitals, Article N and Annex N sections, each with its chapter. The
correlation table annex (old vs new article numbers) is dropped as noise.

**Extraction problems fixed:**
1. EUR-Lex answers scripts with a bot check (HTTP 202), so the code downloads from the Publications Office
   instead, joins long acts delivered in several parts, and re-downloads any act below a minimum word count.
2. The first parse of the UCITS Directive found only 11 sections and 9,668 of its ~40,000 words. Article
   references inside sentences ("…referred to in Article 5…") were read as headings, and a short list of
   annexes before Article 1 made the parser think the annexes had started, so all 119 articles ended up in the
   correlation-table annex and were dropped. Fix: real headings are recognised by their HTML class (`ti-art`),
   and "ANNEX" only counts after the first article. Result: 122 sections and 39,353 words.

**Chunk metadata:** `doc_id`, `source` (act title), `location` (e.g. "Article 52"), `locations` (all articles a
chunk spans), `chapter`, `page` (for PDFs), `part`, `design`, `words`. Chunk ids are a hash of location and
text, so only new or changed chunks are embedded; each vector is saved in ChromaDB (`index/chroma`) as soon as
it arrives, which mattered with the free-tier limit of about 1,000 embeddings a day.

**Embedding:** `gemini-embedding-2`, 768 dimensions, one text per call, with the recommended prefixes
(`title: … | text: …` for chunks, `task: question answering | query: …` for queries). Query vectors are cached.

**Number of chunks:** article design 316, fixed design 420 (+93 after adding UCITS V). `index/ 18 MB.

## Test set

40 questions in `eval/questions.csv`, written from the corpus texts as a compliance analyst would ask them:

| Kind | Count |
|---|---|
| single | 27 |
| multi (needs two passages) | 7 |
| unanswerable | 6 |

Unanswerable questions stay close to the topic: UCITS V remuneration rules, AIFMD leverage, money market fund
maturity, Spanish withholding tax, the PRIIPs KID and SFDR disclosures.

A checker (`eval/check_questions.py`) verifies every expected source and location against the index and that
each number in the reference answer appears in that article. It found two errors in the first draft (q19 used
"five years" but the law says "5 years"; q31's reference used words not in Article 78), which were fixed.

**Examples:**
- q01 (single): *What is the maximum share of a UCITS's assets that can be invested in transferable securities
  issued by a single body?* → 5%; can be raised to 10% if holdings above 5% total no more than 40%
  (ucits_directive, Article 52).
- q34 (multi): *Can a UCITS hold 15% of the bonds issued by one company if that holding is only 3% of the fund's
  assets?* → No: the 3% respects the 5% issuer limit (Article 52), but a UCITS may acquire no more than 10% of
  one issuer's debt securities (Article 56).

## Retrieval

Hit rate on the 34 answerable questions (a hit = an expected source and location in the top k):

| Design | hit@1 | hit@3 | hit@5 | multi: both passages @1 | @3 | @5 |
|---|---|---|---|---|---|---|
| article (one chunk per article, long ones split at ~350 words) | 88% | 100% | 100% | 0% | 43% | 57% |
| fixed (200 words, 40-word overlap) | 88% | 100% | 100% | 0% | 57% | 71% |

**Words added to the prompt:** with k = 5, about 1,000 words per search for both designs (fixed chunks are 200
words; article chunks average about 210 words).

**Choice:** both designs tie on hit@1/3/5. Fixed retrieves both needed passages more often for multi questions
(71% vs 57% at k = 5), so I chose **fixed with k = 5** (`index/active_design.txt`). Trade-off accepted: fixed
chunks can cut a rule in the middle and their citations can span two articles (e.g. "Article 55 to Article 56").
This later caused some imprecise article numbers (see Failures).

Limitation: hit rates are high partly because questions were written while reading the same articles and use
similar wording; real users would phrase things differently.

## Tools and subagent

**`search(query)`** (server.py): "Search the EU UCITS rulebook: Directive 2009/65/EC (UCITS Directive),
Commission Directive 2007/16/EC (eligible assets), Commission Directive 2010/43/EU (organisation, conflicts of
interest, risk management) and Commission Regulation 583/2010 (key investor information), plus any document
added with add_document. Use it for every question about UCITS funds and their management companies […].
Returns the 5 most relevant passages. Each starts with its citation in the form [doc_id, Article N] […],
followed by the act's title, a relevance score between 0 and 1, and the text."

**`add_document(path)`**: "Add one document (.html, .pdf, .txt or .md) to the UCITS search index. The file is
extracted, cleaned, split into chunks with source and location metadata, embedded and stored […]. If a file
with identical content is already indexed, nothing is embedded; if a file with the same name but different
content exists, its old chunks are replaced."

**One search result** (from `check.py`, query = q01):

~~~
[ucits_directive, Article 55 to Article 56] Directive 2009/65/EC (UCITS Directive) (relevance 0.77)
UCITS itself and to the other UCITS or collective investment undertaking in which it invests. 1. An
investment company or a management company acting in connection with all of the common funds which it
manages … shall not acquire any shares carrying voting rights …
~~~

**Subagent** (`.claude/agents/corpus-researcher.md`, tools: `mcp__corpus__search` only): a UCITS researcher
for a compliance analyst that must search before answering (once per rule for two-rule questions), answer only
from the passages, cite every claim exactly, quote numbers exactly, start with "I don't know" when the passages
don't answer, and keep answers short.

**Transcript from Claude Code** (full file: `eval/subagent_transcript.txt`):

~~~
❯ Use the corpus-researcher subagent to answer: Can a UCITS hold 15% of the bonds issued by one company if
  that holding is only 3% of the fund's assets?

● corpus-researcher(UCITS 15% bonds one issuer)
  ⎿  Backgrounded agent

› Message from corpus-researcher
  Answer: No, not as a rule. The 3% weight passes the asset-spreading test, but buying 15% of one issuer's
  debt securities breaks the 10% cap on how much of one issuer's debt a fund may acquire.
  - Debt ownership cap: "A UCITS may acquire no more than ... (b) 10 % of the debt securities of a single
    issuing body" [ucits_directive, Article 56(2)]. […]
  - Asset-spreading limit: […] A 3% position is below the 5% figure, so Article 52 is not the problem.
    The opening sentence of Article 52(1) did not come back in the search results. […]
  Note: this answer reflects only the original Directive 2009/65/EC text that is indexed. Later amendments
  (e.g. UCITS V) and national law may matter.
~~~

The subagent's remark that "the opening sentence of Article 52(1) did not come back" is a direct effect of the
fixed chunking: the sentence with the 5% limit sat in a chunk that was not in the top 5.

## Adding a document

**Already indexed:** `add_document` computes a SHA-256 hash of the file. Identical content → nothing is
embedded ("Already indexed … nothing was embedded"). Same file name with different content → the old chunks are
replaced. Only the active design (fixed) is embedded, and the corpus is never re-embedded.

**Unanswerable question:** q35, *What rules apply to the remuneration policy for staff of a UCITS management
company?* (remuneration rules were added by UCITS V in 2014).

**Document added:** Directive 2014/91/EU (UCITS V), added through the agent's `add_document` tool after I
approved it (93 chunks embedded).

**Before:** "I don't know. The indexed documents do not contain specific rules regarding the remuneration
policy for staff of a UCITS management company. […] later amendments (such as those introduced by UCITS V
regarding remuneration) are not included in the current search index."

**After:** "UCITS management companies must establish and apply remuneration policies and practices that are
consistent with and promote sound and effective risk management, align with the business strategy and
investors' interests, and include measures to avoid conflicts of interest [ucits_v_directive, Article 14b].
These policies must cover both fixed and variable components of salaries and discretionary pension benefits
[…]. They apply to senior management, risk takers, control functions, and any employee whose professional
activities have a material impact on the risk profiles […]. Additionally, significant management companies
must establish a remuneration committee [ucits_v_directive, Article 14b]."

Full record: `eval/before_after.json`.

## Harness and guardrails

**AGENTS.md (system prompt), each rule with its reason:** always search first, once per rule for two-rule
questions (the answer must come from the law); answer only from the returned passages (anything else can't be
verified); cite every claim exactly as the passage citation (the analyst must verify, and the harness rejects
other citations); quote numbers exactly (in compliance a wrong number is a wrong answer); start with "I don't
know" when the passages don't answer (a guess can cause a breach; the fixed phrase also lets code detect
refusals); keep it short, rule first then exceptions; say that later amendments may apply; use `add_document`
only when asked and never retry a denied approval.

**Harness (`agent.py`):** LangChain `create_agent` on Gemini with the two MCP tools from `server.py`.
- **Approval:** `add_document` only runs after a human types `y`. Without a person at the keyboard
  (evaluation, `check.py`) it is denied. In the before/after run it asked "The agent wants to add
  'corpus/ucits_v_directive.html' to the index (uses embeddings). Approve? [y/N]" and ran only after `y`.
- **Call limit:** at most 6 tool calls per question plus a graph recursion limit.
- **Model fallback:** if a Gemini model is overloaded (503), out of free quota (429) or retired (404), the
  agent moves to the next one. During the evaluation the Flash models ran out of free quota, so answers came
  from Flash-Lite.

**Extra guardrail: citation check.** Every citation in the answer must match a passage that `search` returned
in that run, and an answer must have at least one citation (or be a refusal). Otherwise the answer is replaced
by "I don't know … please check with the legal or compliance team." For a compliance analyst an unsupported
answer is worse than no answer.

**Where it fired:** in 2 of 40 evaluation questions (5%), e.g. q31 (KIID content and length), where the draft
answer was replaced by a refusal, which became a wrong refusal. It also fired after the approved
`add_document` call: the agent's confirmation had no citation, so it was shown as "I don't know" even though
the document had been added. Both show the guardrail is strict; the next version should allow
citation-free replies to non-question requests.

The call limit also fired during the final check: with gemini-3.5-flash-lite the agent kept searching (8 tool calls) without answering, and the harness stopped it and returned "I don't know". With gemini-3.1-flash-lite the same question was answered correctly with one search.

## Evaluation

**Code checks:** citation validity (the guardrail above), refusal detection (regex on "I don't know" and
similar phrases), and whether the expected passage was among the retrieved ones. Refusals are labelled by code:
a refusal on an unanswerable question is correct; on an answerable one it is a wrong refusal.

**LLM judge** (Gemini, strict on numbers), for every non-refusal answer:

> correct (1/0): 1 if the answer gives the same rule as the reference answer AND every number, threshold and
> condition of the reference that matters for the decision is present and matches. Extra details are fine if
> the passages do not contradict them. A wrong or missing key number, limit or condition, or a different
> conclusion, is 0.
> supported (1/0): 1 if every factual claim in the answer can be found in the retrieved passages (paraphrase is
> fine). 0 if any claim, number or condition is not in the passages.

**Agreement with the judge:** I graded 22 answers (all 7 multi, all 6 unanswerable and 9 single) in
`eval/human_labels.csv` before reading the judge's verdicts. Agreement on *correct*: **86%** (80% on the
answers the judge graded); on *supported*: **95%** (93%). All three disagreements (q32, q33, q34) are multi
questions where I graded the answer wrong and the judge graded it correct: the answers had the right conclusion
but missed a key limit (q32: the 10% limit on target funds; q33: the 5%/10% issuer limit; q34: the 10% cap on
one issuer's debt). Even with a strict rubric the judge is lenient on partial answers.

**Results (40 questions, code + judge):**

| Measure | Result |
|---|---|
| Answerable questions correct | 30/34 (88%) |
| Unsupported / made-up answers | 1/30 answered (3%) |
| Correct refusals (unanswerable) | 6/6 (100%) |
| Wrong refusals (answerable) | 4/34 (12%) |
| Overall correct | 36/40 (90%) |

Using my grades instead of the judge's for q32–q34, answerable accuracy is **27/34 (79%)** and only **3 of the
7 multi questions** are answered correctly. Detailed outputs: `eval/results.csv`, `eval/failures.csv`,
`eval/summary.json`.

## Failures

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 0 | – (the expected passage was retrieved for every failed question) |
| Wrong answer from the right passage | 1 | q32 (misses the 10% target-fund limit, misapplies the 30% rule) |
| Unsupported claim | 2 | q33 ("not an unlawful breach" is not in the text), q34 (reasoning that only the % of fund assets matters) |
| Wrong refusal | 4 | q13, q21, q26, q31 (2 of them caused by the citation guardrail) |
| Bad test question | 0 | – |

Also found while grading (answer still correct): wrong article numbers in citations, e.g. q08 cites Article 57
instead of 58 and q09 cites Article 82 instead of 83, because fixed chunks span two articles.

**What to fix first:**
1. **Multi-rule questions** (3 of 7 wrong): make the agent search once per condition and check every limit
   before concluding, and switch back to article chunking so each rule arrives complete with an exact citation.
2. **Wrong refusals**: let the guardrail keep answers whose citations name a retrieved article at paragraph
   level, instead of replacing the whole answer.
3. **Judge**: add "missing any reference limit = 0" examples to the rubric, since it was lenient on partial
   answers.

## Decision

**Not for unsupervised use.** For single-rule lookups (limits, deadlines, document requirements) it is reliable:
answers are correct and cited, and it never invented an answer to an out-of-scope question. But a compliance
analyst's hardest questions combine two or more rules, and there it was wrong or incomplete in 4 of 7 cases,
sometimes with a confident "No/Yes". A wrong limit in compliance can cause a breach.

**I would let analysts use it as a research assistant** to find and quote the relevant articles, with these
safeguards: (1) every answer shows its citations and the analyst reads the cited article before acting;
(2) questions combining several conditions are always confirmed by legal; (3) a banner states that only the
original 2007–2010 texts (plus UCITS V) are indexed and later amendments or national law may apply.

**Cost and latency per question** (evaluation run, Gemini Flash-Lite): about **5,240 input + 230 output
tokens**, **1.2 searches** (one query embedding each) and **12.9 seconds** on average. With the free tier this
cost nothing; the real constraint was the free daily quota, which forced the switch from Flash to Flash-Lite.

## AI use

I used **Claude (Anthropic)** for: 
- **Code and debugging:** I used Claude to assist with the development of `index.py`, `server.py`, `agent.py`, `evaluate.py`, `eval/check_questions.py` and `eval/grade.py`. It helped me work through implementation issues and debug errors as they arose, including the EUR-Lex bot check, document splitting, article parsing, model quota limitations and fallback mechanisms.
- **Design decisions:** I used Claude to explore possible approaches and understand their trade-offs. I made the final decisions regarding the use case (compliance analyst), corpus (UCITS acts), chunking strategies (fixed vs. article-based), retrieval configuration (fixed chunking, k = 5, based on retrieval results), duplicate handling (skip-if-identical), evaluation judge criteria (strict on numerical accuracy) and the addition of UCITS V.
- **Test set, AGENTS.md and subagent:** I used Claude to help structure and prepare these components. I reviewed the outputs and verified the test set against the index using the checker.
- **Human evaluation:** I personally graded the 22 answers using the `grade.py` helper. Claude provided suggestions for grades and evaluation notes, which I reviewed and adjusted before entering the final grades.
- **Report:** I used Claude to help structure and refine the report based on my analysis of the results.
- **Claude Code:** I also used Claude Code to assist with running the subagent.
