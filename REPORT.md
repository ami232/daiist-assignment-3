# Assignment 3 Report

- **Name**: Gonzalo Ruiz Feliu
- **Student ID**: 19100
- **Group**: BBADBA 5B

## Use case

**Who asks:** customer-service staff at a travel agency. A customer calls after a flight, train, coach or ferry was cancelled, delayed or overbooked, and asks what they are owed.

**What they do with the answer:** staff repeat it to the customer, or use it to decide whether to file a claim with the carrier for them. They need the verdict (yes / no / how much), the conditions, and the article to quote to the carrier.

**Cost of a wrong answer vs "I don't know":** a confident wrong answer is the expensive one. If the assistant says "no compensation" when €400 is due, the customer gives up money they are owed. If it says €400 when nothing is due, the agency promises money the carrier will refuse, and loses the customer's trust. "I don't know, this is not covered" costs a few minutes: staff escalate to a specialist or the carrier. So the assistant should refuse whenever the documents do not cover the question, and cite every claim so staff can check it.

## Corpus

Five EU legal texts on passenger rights, one per transport mode plus the Commission's guidelines on air rights (the longest and most practical document).

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| Regulation (EC) No 261/2004 (air) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32004R0261 | 2004-02-11 | © European Union, reuse allowed with acknowledgement (Commission Decision 2011/833/EU) | 4,525 |
| Commission Guidelines on Regulation 261/2004 (2024) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52024XC05687 | 2024-07-22 | same | 19,223 |
| Regulation (EU) 2021/782 (rail) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32021R0782 | 2021-04-29 | same | 23,350 |
| Regulation (EU) No 181/2011 (bus and coach) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32011R0181 | 2011-02-16 | same | 7,250 |
| Regulation (EU) No 1177/2010 (sea and inland waterway) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32010R1177 | 2010-11-24 | same | 8,514 |
| **Total** | | | | **62,862** |

Word counts are after cleaning (footnotes and markup removed). The texts are legislation and official guidance: public, no personal data.

## Ingestion

**Download.** EUR-Lex blocks scripted downloads (it answers HTTP 202 with an empty body), so `index.py` fetches the same documents from the EU Publications Office (`publications.europa.eu/resource/celex/<CELEX>`, asking for English XHTML). The files are cached in `corpus/` (git-ignored); `main.py index` downloads them if they are missing.

**Extract and clean.** BeautifulSoup reads the XHTML. Each paragraph becomes a block tagged with its location:
- **Regulations**: "Article N" (the line after the article number becomes the heading, e.g. "Right to compensation"), "Recital (N)", "Annex I". Chapter and section labels are skipped.
- **Guidelines**: numbered sections, e.g. "Section 4.4.7" with the heading "'Long delays' at arrival".
- Footnotes (about 190 in the guidelines) and their markers are removed, because they cut sentences in half and add case-law references that pollute the chunks.
- `add_document` also accepts PDF (location "Page N") and plain text (location "Paragraph N").

**Extraction problem fixed.** The first extraction of Regulation 261/2004 gave 8,985 words, about twice its real length. The XHTML wraps the whole document in an outer `<p>` that contains all the other `<p>`, so every paragraph was read twice. The fix skips any `<p>` that contains another `<p>`: the count dropped to 4,525, and the duplicate chunks disappeared.

**Chunking: two designs.**
- **fixed**: windows of 150 words with 30 words of overlap, ignoring the structure. 525 chunks.
- **structure**: one chunk per article, recital or guideline section, split at paragraph boundaries if it exceeds 300 words; units under 30 words (e.g. a section that is only a heading) are merged into the next one. 445 chunks, median 127 words.

**Chunk metadata:** `source` (document name used in citations), `location` (e.g. "Article 7"), `locations` (every article a chunk touches, for fixed windows that cross a boundary), `heading`, `design`, `chunk` (position), `words`, `mode` (air/rail/bus/sea), `url`, `celex`.

**Embedding and storage.** `gemini-embedding-2` with `output_dimensionality=768` (a quarter of the full size, keeps `index/` at 15 MB), `RETRIEVAL_DOCUMENT` for chunks and `RETRIEVAL_QUERY` for questions. Stored in ChromaDB (`index/chroma`, cosine distance), one collection per design. Chunk ids are a hash of design, source, location and text, so `main.py index` embeds only chunks without a saved vector, and saves each batch of 50 as soon as it is embedded (the free tier allows about 1,000 embeddings a day).

## Test set

36 questions in `eval/questions.csv`: **24 single, 6 multi, 6 unanswerable**. Each question has its expected source, location and a short reference answer, and every one was read and approved before running anything. Every expected source and location was checked against the index metadata. The questions are worded as a travel-agency employee would ask them, with concrete numbers (distances, delay lengths) so that the answer depends on applying the rule, not just finding it. The unanswerable ones are close to the topic on purpose (UK rules after Brexit, hand-luggage weight, hotel overbooking in a package holiday, US DOT rules, a late taxi transfer, Spain's maximum fine).

Two examples:

| id | kind | question | expected | reference answer |
|---|---|---|---|---|
| q26 | multi | A 2,000 km flight within the EU was cancelled five days before departure. The airline re-routed the customer, arriving 2.5 hours after the original arrival time. How much compensation is due? | Regulation (EC) No 261/2004, Article 5; Article 7 | EUR 200: compensation is due (informed less than 7 days before and arriving more than 2 hours late), EUR 400 for this distance, which the airline may reduce by 50% because arrival was less than 3 hours late. |
| q36 | unanswerable | What is the maximum fine in euros that Spain's enforcement body can impose on an airline that refuses to pay compensation? | (none) | The documents only say Member States must set effective, proportionate and dissuasive penalties; they give no amounts. |

## Retrieval

Hit rate on the 30 answerable questions: a hit is a retrieved chunk from the expected source that touches the expected location. For multi questions, "all passages" means both expected passages are in the top k. One embedding per question, reused for both designs (`eval/query_vectors.json`).

| Design | k | Hit rate | Multi: all passages | Words added to the prompt |
|---|---|---|---|---|
| fixed | 1 | **0.800** | 0.000 | 150 |
| fixed | 3 | 0.867 | 0.333 | 450 |
| fixed | 5 | 0.967 | 0.500 | 750 |
| structure | 1 | 0.700 | 0.000 | 207 |
| structure | 3 | **0.933** | 0.500 | 584 |
| structure | 5 | 0.967 | **0.667** | 930 |

**Choice: structure, with k = 5.** The small fixed windows win at k = 1 (the exact sentence ranks first), but the agent reads five chunks, and at k = 5 both designs miss one question each. What decides it is the multi questions: structure finds both passages in 4 of 6 against 3 of 6, because a whole article keeps the rule and its conditions together. It also gives clean citations ("Article 7") instead of "Article 6 – Article 7". The cost is about 180 more words per question (+24%), which is small next to a wrong answer. In the end-to-end run the agent's own searches (often two or three per question) retrieved the expected passage for 30 of 30 answerable questions.

## Tools and subagent

`server.py` (MCP, stdio) serves the structure design. It opens the saved index at startup and never re-embeds the corpus; it logs to stderr only, because stdout carries the protocol.

**search(query)**, description as the model reads it (shortened):
> Search EU passenger-rights law for passages relevant to a question. The corpus holds: Regulation (EC) No 261/2004 …, the Commission's 2024 interpretative Guidelines …, Regulation (EU) 2021/782 (rail), Regulation (EU) No 181/2011 (bus and coach), Regulation (EU) No 1177/2010 (sea …), plus any document added with add_document. Use it before answering any question about passenger rights, and again with different wording (or once per transport mode) when a question needs several rules. … Returns the 5 most similar passages, best first. Each one starts with a line "[n] \<source\>, \<location\> | \<heading\> | relevance \<0-1\>", then the passage text. Cite a passage as [\<source\>, \<location\>], copied exactly from that line. Low relevance (under about 0.5) or passages on another topic mean the corpus probably does not cover the question.

**add_document(path)**:
> Add a local file (HTML, PDF, TXT or MD) to the passenger-rights index. The file is split into chunks the same way as the original corpus, embedded and saved, so later searches can find it. Its file name (without extension) becomes the source name used in citations. Same content already indexed: nothing is done. A file with the same name but new content: its old chunks are replaced. Returns a short report … Only call it when the user asks to add a document.

**One search result** (first of five) for "compensation for a cancelled flight of 1,200 km":
```
[1] Regulation (EC) No 261/2004, Article 7 | Right to compensation | relevance 0.81
Link: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32004R0261
Article 7 Right to compensation 1. Where reference is made to this Article, passengers shall
receive compensation amounting to: (a) EUR 250 for all flights of 1500 kilometres or less; ...
```

**Subagent** (`.claude/agents/corpus-researcher.md`, tool: `mcp__corpus__search` only). Its description tells the editor to delegate any question about compensation, refunds, rerouting, assistance, delays, cancellations or denied boarding in the five documents. Its instructions: search before answering (once per part for mixed questions), answer only from the passages, cite every claim as [source, location], say "The corpus does not cover this." when it doesn't, state assumptions, and reply as **Answer / Conditions / Sources**.

**Transcript from my editor** (Claude Code desktop, session opened in the repo folder; the "corpus" server from `.mcp.json` connected, and the main agent delegated to the subagent, which called `mcp__corpus__search` three times, 3 tool uses, about 15 s):

```
User: Use the corpus-researcher subagent to answer: "A ferry crossing scheduled for 3 hours
      arrived 1 hour 20 minutes late. What can the passenger claim?"

Claude Code: The corpus MCP server is connected. Handing the question to the
             corpus-researcher subagent.
  [Agent: corpus-researcher]
    mcp__corpus__search (x3)

corpus-researcher:
**Answer:** Yes. The passenger can claim at least 25% of the ticket price as compensation
for the late arrival, and keeps the right to be carried [Regulation (EU) No 1177/2010, Article 19].

**Conditions:**
- **Threshold:** for a scheduled journey of up to 4 hours, compensation is due for an arrival
  delay of at least 1 hour. The rate is 25%, or 50% if the delay is more than double that
  threshold [Regulation (EU) No 1177/2010, Article 19]. Here the journey is 3 hours and the
  delay is 1h20, so 25% applies. The delay would need to be over 2 hours for 50%.
- **Price used:** compensation is based on the price actually paid for the delayed service.
  On a return ticket, it is based on half the price paid [Regulation (EU) No 1177/2010, Article 19].
- **Payment:** within 1 month of the request. The carrier may pay in vouchers, but must pay
  money if the passenger asks. Fees cannot be deducted. Carriers may refuse claims below a
  threshold of up to EUR 6 [Regulation (EU) No 1177/2010, Article 19].
- **Exceptions (no compensation):**
  - The carrier proves the delay was caused by weather endangering the safe operation of the
    ship, or by extraordinary circumstances that could not have been avoided even with all
    reasonable measures [Regulation (EU) No 1177/2010, Article 20]. The carrier bears the
    burden of proof. Examples of such weather are strong winds, heavy seas and storms
    [Regulation (EU) No 1177/2010, Recital (16)].
  - The passenger was told about the delay before buying the ticket, or the passenger caused
    the delay [Regulation (EU) No 1177/2010, Article 20].
  - The passenger holds an open ticket with no departure time set, unless it is a travel pass
    or season ticket [Regulation (EU) No 1177/2010, Article 20].
- **Assistance, re-routing or refund:** these depend on a delay in *departure* of more than
  90 minutes [Regulation (EU) No 1177/2010, Article 17] [Regulation (EU) No 1177/2010,
  Article 18]. With a 1h20 arrival delay this probably does not apply. Confirm the actual
  departure delay with the customer.

**Assumptions:** the 3 hours is the scheduled journey time in the transport contract. The
cause of the delay is unknown, so I assumed it was not weather or extraordinary
circumstances. Confirm the cause with the carrier.

**Sources:** [Regulation (EU) No 1177/2010, Article 19], [Regulation (EU) No 1177/2010,
Article 20], [Regulation (EU) No 1177/2010, Recital (16)], [Regulation (EU) No 1177/2010,
Article 17], [Regulation (EU) No 1177/2010, Article 18]
```

The answer matches the reference for q22 (25% of the ticket price, Article 19), cites only the sea regulation, states its assumptions, and correctly separates the arrival delay (compensation) from the departure delay (assistance, re-routing).

## Adding a document

**Already indexed?** `add_document` hashes the file's bytes. If chunks with the same content hash exist, it does nothing and says "already indexed as '…'". If a document with the same name but different content exists, its old chunks are deleted and the new version is added (an updated version replaces the old one instead of both being searchable). Otherwise it is added. Only the new chunks are embedded. Tested: adding the same file twice gives "Not added: this content is already indexed"; a missing path gives a clear error.

**Before and after** (stage 6 of `evaluate.py`, saved in `eval/before_after.json`).

**Question q33 (unanswerable):** "The hotel in a customer's package holiday was overbooked on arrival. How much compensation is she owed for the hotel?"

**Before:**
> The documents I have do not cover specific statutory compensation amounts for hotel overbookings under package holidays. … Regulation 261/2004 applies to flights within a package tour, [but] it does not apply to package tour cancellations or incidents caused by reasons other than flight disruptions (such as hotel cancellations) [Commission Guidelines on Regulation 261/2004 (2024), Section 2.2.7]. Rules regarding hotel overbookings or price reductions/compensation under the Package Travel Directive (Directive (EU) 2015/2302) are not present in the provided documents.

**Document added:** Directive (EU) 2015/2302 on package travel (CELEX 32015L2302, same source and licence as the corpus): "Added 'Directive (EU) 2015-2302 (Package Travel)': 109 chunks, 16618 words."

**After** (two searches, both returning Articles 13 and 14 of the Directive):
> Yes, the customer is entitled to an appropriate price reduction for any period of lack of conformity, and appropriate compensation from the organiser for any damage sustained as a result [Directive (EU) 2015-2302 (Package Travel), Article 14]. Conditions: the organiser must offer, at no extra cost, suitable alternative arrangements of equivalent or higher quality where possible, or of lower quality with an appropriate price reduction [… Article 13]. … The traveller is not entitled to compensation for damages if the organiser proves the lack of conformity is attributable to the traveller, an unforeseeable or unavoidable third party, or unavoidable and extraordinary circumstances [… Article 14].

The stage then deletes the Directive's chunks, so the 36 questions keep measuring the original corpus and `main.py evaluate` can be re-run with the same result.

## Harness and guardrails

`agent.py` is session 10's harness adapted: LangChain `create_agent` with `gemini-3.5-flash-lite`, the two MCP tools loaded from `server.py` with `MCPAdapter`, and `AGENTS.md` as system prompt.

**AGENTS.md rules** (each has its reason in the file):
1. Search before every answer and answer only from the results, never from own knowledge.
2. Cite every claim as [source, location], copied exactly from the result line.
3. If the passages do not cover the question, say "The documents I have do not cover this", say what is missing, and don't guess.
4. Search once for each part of a question that mixes transport modes or rules.
5. State the assumption when a fact the answer depends on is missing.
6. Answer first (yes / no / amount), then conditions, then citations.
7. Only call add_document when the user asks for it.

**Approval step.** A `wrap_tool_call` middleware stops every `add_document` call and asks the person at the keyboard `Allow add_document(...)? [y/N]`. Anything but "y" returns an error to the model ("The user refused this tool call. Do not add the document another way."). With nobody at the keyboard (stdin is not a terminal, e.g. during evaluation) it refuses rather than adding silently. Tested: `main.py ask "Please add the document README.md to the index."` with no terminal → refused, index unchanged at 445 chunks.

**Call limit.** `ModelCallLimitMiddleware(run_limit=8)` stops runaway loops.

**Extra guardrail: citation check.** After the agent answers, the harness collects every "[source, location]" that appeared in a search result during this question, and checks every bracketed citation in the answer against them. A citation may narrow a retrieved one to a paragraph ("Article 7(1)(b)" when "Article 7" was retrieved) but nothing else ("Article 70", or a source that was never retrieved, fails). If any citation is unsupported, the agent gets one chance to rewrite its answer citing only retrieved passages; if it still fails, the answer is printed with a WARNING listing the unverified citations. The model cannot skip it: the harness runs it, not the model.

**A case where it fired** (q29, rail delay from extreme weather): the first answer cited `[Regulation (EU) 2021/782, Article 19, Article 19(10)]`, two locations jammed into one bracket, which matches no retrieved passage. The guardrail sent it back; the second answer cited `[Regulation (EU) 2021/782, Article 19]` and `[Regulation (EU) 2021/782, Article 20]`, both verified. In the full run it fired on 3 of 36 questions (q11, q27, q29) and all three were repaired; no answer ended with a warning.

## Evaluation

`main.py evaluate` runs six stages and writes everything to `eval/`: retrieval (above), the agent's answers to all 36 questions (`answers.json`), code checks, the LLM judge (`verdicts.json`), outcomes and agreement (`results.csv`, `summary.json`), and the before/after (`before_after.json`). Answers and verdicts are cached and redone only if the agent (model, AGENTS.md, server) or the judge changes.

**Code checks** (exact, no model):

| Check | Result |
|---|---|
| Called search | 36 / 36 |
| All citations valid (guardrail) | 36 / 36 (3 after one retry) |
| Answerable questions with at least one citation | 30 / 30 |
| Expected passage among the agent's search results | 30 / 30 |
| Refusal phrase ("do not cover"…) agrees with the judge's "refused" | 35 / 36 (q13 says "not covered by the Regulation", a correct answer, not a refusal) |

**Judge.** `gemini-3.1-flash-lite`, temperature 0, structured output with the reasoning first, then three booleans. It sees the question, its kind, the reference answer, the full tool trace (the passages the agent saw) and the answer. Rubric:
- **refused**: the answer says the documents do not cover the question.
- **correct**: answerable → the verdict and its key amount, time limit or condition match the reference; extra details are fine if they don't contradict it; for multi questions both parts must be right (one part missing or wrong = incorrect). Unanswerable → correct only if it refuses without inventing the missing answer.
- **supported**: every factual claim is stated in the retrieved passages; a citation is not enough, the passage must say it; general knowledge fails.

The planned judge was `gemini-3.5-flash` (stronger than the agent), but its free tier allows only 20 requests a day; after 12 verdicts it ran out, so all 36 were judged again with `gemini-3.1-flash-lite`. This judge is not stronger than the agent, which matters below.

Outcomes are assigned in code from the verdict: answerable → *correct* (correct and supported), *unsupported* (not supported), *incorrect* (supported but wrong), *wrong refusal* (refused); unanswerable → *correct refusal* (refused) or *unsupported* (answered).

**Results according to the judge:**

| Kind | Correct | Unsupported | Incorrect | Correct refusal | Wrong refusal |
|---|---|---|---|---|---|
| single (24) | 24 | 0 | 0 | – | 0 |
| multi (6) | 6 | 0 | 0 | – | 0 |
| unanswerable (6) | – | 0 | – | 6 | – |

**Agreement with the labels** (`eval/human_labels.csv`, 20 answers: all 6 unanswerable, all 6 multi, 8 single across the five documents;

| | Agreement | Disagreements |
|---|---|---|
| correct | 0.90 | q26, q32 |
| supported | 0.90 | q26, q20 |
| both | 0.85 | |

All three disagreements go the same way: **the judge passes what the labels fail.** On q26 it noticed the confused "7–14 day window" explanation but called it minor and accepted an answer whose headline is EUR 400 (reference: EUR 200). On q20 it did not notice that the descriptions of the articles are not in the passage. On q32 it caught the added general-knowledge claim (supported = false) but also marked the refusal incorrect. So the judge's 100% overstates quality: on the labelled sample, 18/20 answers are correct and 17/20 supported.

## Failures

Using the brief's categories, over the 20 labelled answers (the 16 others were read and showed no content errors):

| Cause | Count | Questions | What happened |
|---|---|---|---|
| Retrieval miss | 0 | – | The agent's own searches found the expected passage for 30/30 answerable questions; on q26 it searched three times. |
| Wrong answer from the right passage | 1 | q26 | Had Articles 5 and 7 but misapplied them: led with EUR 400 instead of EUR 200 and said 5 days' notice falls in the "7 to 14 days" window. A two-condition calculation. |
| Unsupported claim | 2 | q20, q32 | Right verdict plus details from the model's own knowledge: the topics of the bus articles that apply under 250 km (one wrong: "accident compensation" for Article 17, which is about mobility equipment); "hand-luggage limits are set by each airline" inside a correct refusal. No citation was invented, so the citation guardrail cannot see this. |
| Wrong refusal | 0 | – | |
| Bad test question | 0 | – | q13's reference ("not covered by the Regulation") makes the refusal regex fire on a correct answer; that is a limit of the code check, not of the question. |

Not failures of the answers, but worth noting: 3 citation-format slips (q11, q27, q29), all caught and repaired by the guardrail; about six answers list their citations at the end instead of after each claim (rule 2 asks for each claim); and the judge's leniency.

**What to fix first:**
1. **Calculations with several conditions (q26).** Add a rule to AGENTS.md: for amounts, list each condition from the passage, check the facts against it, then compute. This is the only failure that would cost money.
2. **Unsupported elaboration (q20, q32).** Tighten rule 1 ("do not describe what a cited article says unless the passage says it; refusals contain nothing else") and add an LLM check of support at answer time, since code cannot catch it.
3. **The judge.** Re-run with a judge stronger than the agent (gemini-3.5-flash over two days of quota, or a paid key) and grade more answers by hand before trusting any pass rate.

## Decision

**Yes, for travel-agency staff, not for customers directly, with safeguards.**

**For what:** first answers to customers' questions on EU passenger rights in the five documents (plus the Package Travel Directive, which should be added permanently given the agency sells packages). On the labelled sample 18/20 answers were right, no citation was invented (checked in code on all 36), and all six questions outside the corpus got an honest "not covered".

**Safeguards:**
- Staff always see the citations and the link to EUR-Lex; the citation guardrail stays on.
- When the answer is an **amount that depends on more than one condition** (notice period, distance, rerouting time), staff confirm it against the cited articles before promising it to the customer: that is the failure seen on q26.
- "Not covered" answers go to a specialist, as designed.
- Re-evaluate with a stronger judge and more human labels before trusting the numbers further, and after any change to the rules or the corpus.

**Cost and latency per question** (averages over the 36 questions; prices from the Gemini API paid tier, USD per 1M tokens; the whole project ran on the free tier, so the real cost was zero):

| | Tokens | Price | Cost |
|---|---|---|---|
| Agent (gemini-3.5-flash-lite, 2.3 model calls) | 5,782 in + 251 out | $0.30 in / $2.50 out | $0.0024 |
| Query embeddings (about 1.6 searches) | ~40 | $0.20 | ≈ $0 |
| **Per question in use** | | | **≈ $0.0024 (about $2.40 per 1,000 questions)** |
| Judge, evaluation only (gemini-3.1-flash-lite) | 2,682 in + 92 out | $0.25 / $1.50 | $0.0008 |

Latency: median 6.0 s per question (mean 8.5 s, maximum 41.8 s when Gemini answered 503 "high demand" and the call was retried). Indexing both designs once embedded about 190k tokens, about $0.04.

## AI use

I used Claude in different stages, working step by step and explaining each step.

- **Code:** Claude helped me write the technical aspects of the code
- **Report:** Claude helped me structure the report, which I wrote myself previously.