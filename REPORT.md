# Assignment 3 Report

- Name: Ana María Cea
- Student ID: 19756
- Group:  BBADBA 5B 

## Use case

Who asks. Customer-service agents at a travel agency (or a consumer helpline) who handle complaints about delayed, cancelled or overbooked journeys by plane, train, coach or ferry in the EU. They ask in English while a customer is waiting.

What they do with the answer. They tell the customer whether they are owed compensation, a refund, re-routing or care (meals, hotel), how much, and by when; then they file the claim or close the case.

Cost of a wrong answer vs "I don't know". A wrong "yes" makes the agency promise money the carrier will not pay (angry customer, lost trust, sometimes the agency pays it itself). A wrong "no" denies a customer money the law gives them (EUR 250-600 per flight passenger, 25-50 % of a rail or ferry ticket) and exposes the agency to complaints to the national enforcement body. "I don't know" costs a few minutes: the agent opens the regulation or escalates. So the system must prefer refusing to guessing. The typical dangerous error is a *correct rule from the wrong regulation* (e.g. the rail 60-minute threshold applied to a coach, where it is 120 minutes), which is why the corpus deliberately mixes four transport modes with similar but different rules.

## Corpus

| Document (source id) | URL | Date | Licence | Words (after cleaning) |
|---|---|---|---|---|
| Regulation (EC) No 261/2004, air passenger rights (`air-261-2004`) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32004R0261 | 11.2.2004 | EU legal acts, free reuse with attribution (Commission Decision 2011/833/EU; © European Union) | 4,055 |
| Commission Interpretative Guidelines on Reg. 261/2004, C/2024/5687 (`air-guidelines-2024`) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52024XC05687 | 25.9.2024 | same | 18,195 |
| Regulation (EU) 2021/782, rail passengers' rights (`rail-2021-782`) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32021R0782 | 29.4.2021 | same | 22,342 |
| Regulation (EU) No 181/2011, bus and coach passengers (`bus-181-2011`) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32011R0181 | 16.2.2011 | same | 6,822 |
| Regulation (EU) No 1177/2010, sea and inland waterway passengers (`sea-1177-2010`) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32010R1177 | 24.11.2010 | same | 8,102 |
| Total | | | | 59,516 |

All five are public EU law with no personal data. `index.py` downloads them itself from the EU Publications Office (CELLAR) by CELEX number, so `corpus/` is not committed. Added later through `add_document` (see below): Regulation (EC) No 1107/2006 on disabled passengers in air transport (`air-prm-1107-2006`, 5,515 words, committed in `extra/`).

## Ingestion

Extract. EUR-Lex's website answers scripts with an empty bot-challenge page (HTTP 202, 0 bytes), so `download()` asks CELLAR directly with content negotiation: XHTML for recent acts, HTML for 261/2004 (only available in the old format). `extract_lines()` reads the HTML in order, one line per paragraph and one line per table row, because the Official Journal lays out recitals and guideline headings as two-cell tables ("(14)" | text).

Clean. Remove footnote markers and footnote bodies (elements with class `oj-note-tag`/`oj-note`, `[1]` markers in the old format), non-breaking spaces and soft hyphens, normalise quotes and whitespace; drop the preamble, the signature block ("Done at Brussels…") and the footnote list that follows it, while keeping the annexes after it.

Chunk. `split_units()` turns the lines into legal units: `Recital N`, `Article N`, `Annex I`, and `Section 4.4.2` for the guidelines. Two chunk designs are built from the same units:

- `fixed`: 250-word windows with 50 words of overlap, blind to structure (299 chunks).
- `structure`: one chunk per unit; units longer than 300 words are split at paragraph boundaries into "part 1/2", "part 2/2"; each chunk starts with "Article 7 - Right to compensation" and is embedded with its document title in front (466 chunks).

Extraction problems fixed.
1. *Table of contents in the guidelines.* Every heading appears twice: once in the table of contents with a page number ("2.1. Territorial scope 5") and once in the body. A naive section parser created ~90 empty or duplicated sections. The parser now skips everything from "TABLE OF CONTENTS" until the first heading reappears without a page number.
2. *Annex articles colliding with real articles.* Annex I of the rail regulation reproduces the CIV international rules, which have their own Articles 1-64. Without a fix, "Article 32" of the CIV rules overwrote the regulation's Article 32 in the metadata. Articles after an "ANNEX" heading are now labelled `Annex I, Article 32`.
3. *Chapter headings glued to articles.* "CHAPTER V / GENERAL RULES ON INFORMATION AND COMPLAINTS" ended up at the end of the preceding article, and "HAVE ADOPTED THIS REGULATION: CHAPTER I" at the end of the last recital. These lines are now dropped.

Metadata per chunk. `source` (document id), `location` (unit, used for citations), `units` (all units a fixed window touches, used to score hits), `mode` (air/rail/bus/sea), `title`, `hash` of the embedded text, `added` (true for documents added later).

Embeddings. `gemini-embedding-2`, `RETRIEVAL_DOCUMENT` task type, truncated to 768 dimensions and L2-normalised (4× smaller index than 3,072; under 90 MB with room to spare). Each batch of 50 vectors is appended to `index/vectors.jsonl` as soon as it arrives, keyed by a hash of model + text, so a re-run embeds only chunks without a vector and the daily free-tier limit loses nothing. Both designs together cost 765 embeddings, under the ~1,000/day limit. Query embeddings are cached in `index/queries.jsonl`, so re-running the evaluation costs no quota.

## Test set

I wrote 42 questions from the documents before tuning anything, phrased the way an agent would ask while a customer is on the phone, covering all four transport modes and both the regulations and the guidelines.

| kind | count |
|---|---|
| single | 28 |
| multi (two passages) | 7 |
| unanswerable | 7 |

The multi questions mostly compare two modes (train vs ferry compensation, rail vs coach notice periods for assistance) or need two articles of the same regulation (5-hour flight delay → Article 6 gives the right, Article 8 the 7-day refund). The unanswerable questions stay close to the corpus: airline fees, national limitation periods, the 2025 reform negotiations, Renfe's own policy.

Two examples:
- q26 (single): "A ferry crossing scheduled for 6 hours arrives 2.5 hours late. What compensation is due?" → `sea-1177-2010`, `Article 19` → 25 % of the ticket price (journeys of 4-8 hours: at least 2 hours' delay; 50 % only beyond 4 hours).
- q36 (unanswerable): "How far in advance must a wheelchair user notify the airline to get assistance at the airport?" The corpus has the rule for trains (24 h), coaches (36 h) and ferries (48 h) but not for planes, so this is a trap: the right answer is "not covered", not another mode's number.

## Retrieval

Hit = the expected source and location appear among the top k results (for multi questions, at least one of the two; the "both" column requires both). 35 answerable questions.

| design | hit@1 | hit@3 | hit@5 | MRR@5 | multi: both in top 5 | words added at k=5 |
|---|---|---|---|---|---|---|
| fixed (250-word windows, dense) | 69% | 91% | 97% | 0.81 | 71% | 1,250 |
| structure (legal units, dense) | 91% | 94% | 94% | 0.93 | 71% | 976 |
| structure-hybrid (dense + BM25, RRF) | 66% | 83% | 86% | 0.74 | 57% | 1,001 |
| structure-hybrid-mode (+ transport-mode filter) | 60% | 83% | 89% | 0.72 | 57% | 1,008 |

![hit rate](eval/hit_rate.png)

Choice: `structure`. It puts the right article first in 91% of questions (69% for fixed windows) and has the best hit@3, which is what matters because the agent mostly uses the first results. Each chunk starts with the document title and the article heading ("Article 19 - Compensation for the ticket price"), so the embedding points straight at the right article. Fixed windows only win at k=5 (97% vs 94%) because each 250-word window touches several articles, at the price of 28% more text in the prompt and citations that are less precise.

What did not work. Adding BM25 made retrieval *worse* (hit@1 from 91% to 66%). Words like "delay", "compensation" and "passenger" appear in all four regulations, so the keyword ranking is weak and noisy, and reciprocal rank fusion gives it the same weight as the dense ranking, which pushes the correct article down. The transport-mode filter did not help either: dense search already picks the right mode thanks to the document title in each chunk. Both variants cost no extra embeddings, so trying them was cheap, but the simplest design won.

## Tools and subagent

search(query) (docstring = description the model reads):
> Search EU passenger rights law: Regulation 261/2004 on air passenger rights (denied boarding, cancellation, long delay) with the Commission's 2024 interpretative guidelines, Regulation 2021/782 on rail passengers, Regulation 181/2011 on bus and coach passengers and Regulation 1177/2010 on sea and inland waterway passengers, plus any document added later. Use it for every question about compensation, refunds, re-routing, care (meals, hotels), delays, cancellations, disabled passengers or complaints in EU transport. Write the query in English legal terms and name the transport mode […]. Returns the 5 most relevant passages, each headed by "cite as [source, location]" […].

add_document(path):
> Add a document to the passenger-rights index so search can find it. `path` is a local file (EU legal act as HTML/XHTML from EUR-Lex, PDF, TXT or Markdown). The file goes through the same pipeline as the corpus […]. If the identical file is already indexed nothing changes; if another version of a file with the same name is indexed, its chunks are replaced. […] Only call it when the user asks to add a document; it needs their approval.

One search result (first of five for q01):

```
--- Result 1 | cite as [air-261-2004, Article 7]
Document: Regulation (EC) No 261/2004 - air passenger rights (denied boarding, cancellation, delay)
Mode: air

Article 7 - Right to compensation
1. Where reference is made to this Article, passengers shall receive compensation amounting to:
(a) EUR 250 for all flights of 1500 kilometres or less;
(b) EUR 400 for all intra-Community flights of more than 1500 kilometres, and for all other flights between 1500 and 3500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b). […]
```

Subagent (`.claude/agents/corpus-researcher.md`, tools: `mcpcorpussearch` only): searches before answering, at most four searches, answers only from the passages, keeps transport modes apart, cites every claim as `[source, location]`, starts with "The documents I have do not cover this." when the corpus does not answer, and replies in at most ~150 words with a Sources line.

Transcript from Claude Code in VS Code (Opus 5.5), with the project folder open and the `corpus` MCP server connected:

```
> Use the corpus-researcher subagent to answer: how much compensation is a rail
  passenger owed for a 90-minute delay?

  Message from @corpus-researcher: [Subagent hand-back] ...
  (the subagent's search calls to mcp__corpus__search are folded in this panel)

  The passenger is owed at least 25% of the ticket price. Under Regulation (EU)
  2021/782, the minimum is 25% for a delay of 60-119 minutes and 50% for 120
  minutes or more [rail-2021-782, Article 19(1)].

  Conditions and exceptions:
  - Price used: the full price the passenger actually paid. For a return ticket,
    it's the price of the delayed leg, or half the ticket if the legs aren't
    priced separately [rail-2021-782, Article 19(3)].
  - No compensation if:
    - the ticket was already refunded under Article 18 [rail-2021-782, Article 19(1)];
    - the passenger knew about the delay before buying [rail-2021-782, Article 19(9)];
    - re-routing cut the delay to under 60 minutes [rail-2021-782, Article 19(9)].
  - Exemptions: the railway doesn't have to pay if it proves the cause was
    extraordinary circumstances, the passenger's own fault, or unavoidable
    third-party behaviour. Strikes by its own staff and failures of the
    infrastructure manager don't count [rail-2021-782, Article 19(10)]. Whether
    one of these applies depends on what caused the delay.
  - Payment: due within one month of the request. The railway can pay in
    vouchers, but must pay money if the passenger asks. It can set a minimum
    payout of up to EUR 4, and it can't deduct fees [rail-2021-782, Article 19(7)-(8)].
```

Every claim cites Article 19 of the rail regulation, the passage the expected answer for q17 points to, and the subagent kept to the rail regulation without mixing in the bus or ferry rules.

## Adding a document

Already indexed? `add_file()` hashes the file (SHA-256). Same name and same hash → nothing is embedded and the tool says "already indexed with identical content; nothing changed". Same name, different hash → treated as a new version: the new chunks are embedded first and only then replace the old ones, so if the quota runs out half-way the old version stays searchable. A new name → added. Added documents are stored with `added: true`, only in the chunk design the server searches, so no quota is wasted on the other one.

Before and after (`eval/before_after.md`): q36, "How far in advance must a wheelchair user notify the airline to get assistance at the airport?". The corpus has this rule for trains, coaches and ferries, but not for planes. Document added: `extra/air-prm-1107-2006.html` (Regulation (EC) No 1107/2006), through `index.add_file`, the function behind the `add_document` tool.

- Before: "The documents I have do not cover the specific notification time for air travel. The provided regulations cover passenger rights for rail, bus/coach, and sea travel, but not air travel. You may wish to consult the specific airline's conditions of carriage or the relevant national enforcement body for air passenger rights." (Retrieved: bus Art. 14, sea Art. 11, rail Art. 24, rail Recital 30. It correctly did not reuse another mode's number.)
- After: "To ensure assistance at the airport, a passenger with reduced mobility should notify the air carrier, their agent, or the tour operator at least 48 hours before the published departure time of the flight [air-prm-1107-2006, Article 7(1)]. [...] If notification is not made at least 48 hours in advance, the airport managing body is still required to make 'all reasonable efforts' to provide the necessary assistance [air-prm-1107-2006, Article 7(3)]." (Retrieved: 1107/2006 Art. 7, Annex I, Art. 6, Annex II.)

## Harness and guardrails

AGENTS.md (system prompt of `agent.py`, also read by the editor's agent): 9 rules, each with its reason: search before every answer; answer only from the results; cite every claim as `[source, location]` and never cite what was not retrieved; keep transport modes apart; start with "The documents I have do not cover this." when not covered (partial answers say which part is missing); search again with other words, at most four times; be short (≤150 words, direct answer first); never add documents unasked; no predictions about how a court or airline will decide.

Approval step. `HumanInTheLoopMiddleware(interrupt_on={"add_document": …})` with a LangGraph checkpointer: when the model calls `add_document`, the run pauses, the harness prints the tool call and asks `Approve? [y/N]`, and resumes with `approve` or `reject`. Without a terminal (evaluation, CI) the answer is always reject. Call limits: 8 model calls and 4 searches per run (`ModelCallLimitMiddleware`, `ToolCallLimitMiddleware`).

Extra guardrail: citation check. After the agent answers, code parses every `[source, location]` in the answer and checks that (a) a non-refusal answer has at least one citation and (b) every citation matches a passage the search tool returned in this run (a paragraph like "Article 7(1)" matches a retrieved "Article 7"). If the check fails, the agent gets one correction message listing the bad citations; if it fails again, the answer is replaced by a refusal. Why this one: in this use case the agent shows the citation to the customer, so an invented article number is worse than no answer. 
Case where it fired (q23, "Does the bus and coach passenger rights regulation fully apply to a 150 km regular coach service?"). The first answer was right in substance, but it cited `[bus-181-2011, Article 4(2)]`, `[bus-181-2011, Article 9]`, `[..., Article 10(1), Article 16(1)(b) ...]` and `[..., Articles 24 to 28]`, and the search tool had only returned Article 2. The model had copied the article numbers *listed inside* Article 2(2) and cited them as if it had read them. The check rejected all four citations; the corrected answer cites only `[bus-181-2011, Article 2(1)]` and `[bus-181-2011, Article 2(2)]` and names the other articles as what Article 2(2) lists. This is exactly the error the guardrail is for: a customer-service agent would have opened Article 9 expecting to find what the answer claimed.

A bug the evaluation found in the guardrail itself. In the first run (`eval/run1/`) the guardrail fired on 4 questions, and 3 of them were correct refusals (q36, q38, q42). The refusal check looked for the exact phrase "The documents I have do not cover this", but the model wrote variants such as "The documents I have do not cover the specific notification time...". So the code treated these refusals as answers without citations and forced the agent to add some, and in q38 (cabin-bag fees) it cited Article 7 of 261/2004, which has nothing to do with baggage. The same bug made the code count 4 correct refusals as "answered an unanswerable question" (run 1: 3/7 correct refusals). We changed the check to match the stem "The documents I have do not cover" and re-ran: 7/7 correct refusals and the guardrail fired only on q23, a real case.

## Evaluation

Models. Agent: `gemini-3.1-flash-lite`. Judge: `gemini-3.5-flash-lite`, a different model from the agent, so the judge is not grading its own answers. Embeddings: `gemini-embedding-2`. We first tried `gemini-2.5-flash` (no longer available to new keys), `gemini-3.8-flash` (requests hung, 503 "high demand") and `gemini-3.5-flash` (the free-tier daily quota ran out after 10 questions), so we moved to the "lite" models, which have a larger free quota.

Code checks (`evaluate.py`, `code_checks`): refusal (answer opens with "The documents I have do not cover"), citation present, every citation valid (returned by the tool), expected passage retrieved, expected passage cited, number of searches. Code decides what code can: an answerable question that was refused is wrong; an unanswerable one that was refused is right; an unanswerable one that was answered is wrong; an answer with an invalid citation is unsupported.

Judge. Temperature 0, JSON output, given the question, its kind, the reference answer, the retrieved passages and the answer. Rubric (full text in `evaluate.py`): `correct` = the key facts of the reference (amounts, thresholds, deadlines, yes/no) for the right transport mode, nothing contradicting it, no missing condition that changes the outcome, both parts for multi questions, and for unanswerable questions a clear "not covered" without presenting an answer; `supported` = every factual claim is in the passages (true but not retrieved counts as unsupported). Instruction: be strict, a confident wrong number is worse than "I don't know".

Agreement with my grades. I graded 26 answers with `grade.py`, which shows the question, the reference, the answer and (on request) the passages, but not the judge's verdict.

| grade | n | agreement | Cohen's kappa |
|---|---|---|---|
| correct | 26 | 100% | 1.0 |
| supported | 26 | 100% | 1.0 |

My first pass gave 1 to all 26 answers, which produced 96% agreement but a kappa of 0.0: when one rater never gives a 0, kappa is zero by definition, because all the agreement could be chance. The one disagreement was q27 (do cruise passengers get delay compensation?). The judge was right and I was wrong: the agent answered "yes, 25%", but Article 2 of 1177/2010 excludes cruise passengers from Article 19. I had read it too quickly. I corrected that grade (noted in `human_labels.csv`). Limitations: my grades are not fully blind, because I already knew that q27 and q29 were the two answers the code had flagged, and my 26 contain only one wrong answer, so the kappa of 1.0 rests on very few negatives. With more failures in the sample the agreement would be a stronger test of the judge.

Results (42 questions):

| | run 1 | final run |
|---|---|---|
| correct (all) | 36 / 42 | 40 / 42 |
| correct (answerable) | 33 / 35 | 33 / 35 |
| unsupported answers | 2 | 2 |
| correct refusals | 3 / 7 | 7 / 7 |
| answered an unanswerable question | 4 | 0 |
| wrong refusals | 0 / 35 | 0 / 35 |
| answers with valid citations (code) | 42 / 42 | 42 / 42 |
| citation guardrail fired | q23, q36, q38, q42 | q23 |

The change between runs is the refusal-check fix described under *Harness and guardrails*; the agent's answers to the answerable questions are equally good in both runs.

## Failures

From `eval/failures.csv` (cause suggested by code, checked by me):

| cause | count | example |
|---|---|---|
| retrieval miss | 1 | q27: "Do cruise passengers have a right to compensation for delay in arrival?" The agent found Article 19 (delay compensation) but not Article 2, which excludes cruise passengers, and answered "yes, 25%". |
| wrong answer from right passage | 1 | q29: train and ferry, 3-hour journey, 2.5 hours late. Train right (50%). Ferry wrong: it said 25%, but for journeys up to 4 hours a delay of more than twice the 1-hour threshold gives 50% (Article 19(1)). |
| unsupported claim | 0 | |
| wrong refusal | 0 | |
| bad test question | 0 | |

Both failures are about exceptions and thresholds: the general rule was found, the exception or the second threshold was not applied. That is the dangerous kind of error in this use case, because the answer sounds confident and comes with a valid citation.

What to fix first. The retrieval miss, because it is invisible to the agent. Scope and exclusion articles (Article 2 of each regulation: who is covered, who is not) should be retrieved together with any rights article of the same regulation, for example by always adding the regulation's scope article to the results, or by a rule in AGENTS.md: "before saying someone is entitled, search the scope article of that regulation". For q29, a rule asking the agent to state the threshold and the delay before giving the percentage would make the arithmetic visible and checkable.

## Decision


I would let customer-service agents use it for the amounts, thresholds and deadlines in the four regulations, as a first answer that always shows the article it comes from, but not as the final word. It answered 33 of 35 answerable questions correctly with valid citations and refused all 7 questions the documents do not cover, without ever answering one of them. Its two mistakes were confident, cited answers that missed an exception (cruise passengers) or a second threshold (ferry 50%), so I would not let it be used for who is covered or for edge cases without a check. Safeguards: the citation is always shown and the agent opens it before promising money; refusals and any claim above EUR 250 are escalated to a supervisor; and the scope-article fix above is made first.

Cost and latency: about 4,539 input and 225 output tokens, 2.05 model calls and 1.14 searches per question; 6.3 s per question. On the free tier this costs $0. At an assumed price of $0.30 per million input and $2.50 per million output tokens (an assumption, not the published price of `gemini-3.1-flash-lite`), it would be about $0.002 per question, so cost is not the constraint; the free-tier daily quota is.

## AI use

I used Claude (Anthropic) to:

- Code: it wrote most of `index.py`, `retrieval.py`, `server.py`, `agent.py`, `evaluate.py`, `settings.py` and `grade.py`, tested them offline before I ran them, and fixed the problems we found when running them (Gemini model names and quotas, a timeout, and the refusal-check bug).
- Studying: it wrote study notes explaining each part, which I used to prepare for the written comprehension check.

