# Assignment 3 Report

- **Name**: Marta Bermejo Villaescusa
- **Student ID**: 18748
- **Group**: BBADBA 5B 

## Use case

A retail investor asks questions to check whether a broker or adviser's recommendation is appropriate, what disclosures they should receive in writing (such as Regulation Best Interest and Form CRS), and how to identify investment scams. The investor uses the answers to decide whether to trust a recommendation or what questions to ask a financial professional.

In retail investing, a wrong answer can cost the investor money, while an I don´t know answer only makes them have to check manually, always best than an incorrect one. For that reason, the system is designed to abstain rather than guess when the corpus does not support an answer, to avoid giving false security that something is a certain why. SEC sources were chosen because they are U.S. government public-domain works and provide accessible guidance without requiring legal expertise to read.

## Corpus

The corpus is made of 13 public-domain U.S. government documents totaling 60,149 words, sourced only from `sec.gov` and `investor.gov`, and not from private license materials. 

| Document (`source`) | URL | Retrieval Date | Licence | Words |
| --- | --- | --- | --- | --- |
| `form-crs-compliance-guide` | https://www.sec.gov/info/smallbus/secg/form-crs-relationship-summary | 2026-11-20 | US government work (public domain) | 2,678 |
| `form-crs-faq` | https://www.sec.gov/investment/form-crs-faq | 2026-11-20 | US government work (public domain) | 10,311 |
| `inv-common-scams` | https://www.investor.gov/additional-resources/spotlight/common-scams | 2026-11-20 | US government work (public domain) | 647 |
| `inv-crypto-assets` | https://www.investor.gov/additional-resources/spotlight/crypto-assets | 2026-11-20 | US government work (public domain) | 744 |
| `inv-five-questions` | https://www.investor.gov/introduction-investing/getting-started/five-questions-ask-you-invest | 2026-11-20 | US government work (public domain) | 437 |
| `inv-understanding-fees` | https://www.investor.gov/introduction-investing/getting-started/understanding-fees | 2026-11-20 | US government work (public domain) | 415 |
| `inv-working-with-professional` | https://www.investor.gov/introduction-investing/getting-started/working-investment-professional | 2026-11-20 | US government work (public domain) | 707 |
| `reg-bi-compliance-guide` | https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/regulation-best-interest | 2026-11-20 | US government work (public domain) | 6,020 |
| `reg-bi-faq` | https://www.sec.gov/tm/faq-regulation-best-interest | 2026-11-20 | US government work (public domain) | 8,041 |
| `staff-bulletin-account-recommendations` | https://www.sec.gov/about/divisions-offices/division-trading-markets/broker-dealers/staff-bulletin-standards-conduct-broker-dealers-investment-advisers-account-recommendations-retail | 2026-11-20 | US government work (public domain) | 4,569 |
| `staff-bulletin-care-obligations` | https://www.sec.gov/about/divisions-offices/division-trading-markets/broker-dealers/staff-bulletin-standards-conduct-broker-dealers-investment-advisers-care-obligations | 2026-11-20 | US government work (public domain) | 13,463 |
| `staff-bulletin-conflicts-of-interest` | https://www.sec.gov/about/divisions-offices/division-trading-markets/broker-dealers/staff-bulletin-standards-conduct-broker-dealers-investment-advisers-conflicts-interest | 2026-11-20 | US government work (public domain) | 8,406 |
| `staff-statement-form-crs-disclosures` | https://www.sec.gov/newsroom/speeches-statements/staff-statement-form-crs-disclosures-121721 | 2026-11-20 | US government work (public domain) | 3,711 |

The corpus mixes compliance guides, staff FAQs, staff bulletins, and investor education pages; staff bulletins and FAQs represent staff views/interpretations rather than binding law. `corpus/` is listed in `.gitignore` and is re-downloaded via `fetch_corpus.py` when running `main.py index`.

## Ingestion

Documents are converted from HTML to Markdown using `BeautifulSoup` and `markdownify` after stripping navigation menus, scripts, and footers. One extraction issue fixed in the pipeline was that `investor.gov` pages returned 0 words when looking solely for `<main>` or a populated `#main-content` container, so the extractor was updated to iterate over candidate containers and select the first one with more than 50 words.

Each chunk stores metadata including `source` (file stem), `title`, `location` (section heading), `url`, `retrieved`, `design`, `chunk_index`, and `words`. Embeddings are generated with `gemini-embedding-2` (768 dimensions) using task-specific text prefixes (`title: ... > location | text: ...` for documents and `task: search result | query: ...` for queries), stored in ChromaDB (`index/`) using cosine similarity, and keyed by a content hash so identical chunks are not re-embedded.

Two chunking designs were indexed and compared:
- **`fixed150` (Design A)**: Sliding windows of 150 words with 20-word overlap — 465 chunks, mean 148 words.
- **`section300` (Design B)**: One chunk per titled section, splitting at paragraph boundaries and then sentence boundaries if a section exceeds 300 words, and dropping sections shorter than 20 words — 300 chunks, mean 195 words, max 299 words.

## Test set

`eval/questions.csv` contains 30 English questions: 20 `single`, 5 `unanswerable`, and 5 `multi` (two expected passages, with `expected_source` entries separated by `;` and `expected_location` entries separated by `;` in the same order, a convention chosen since `eval/README.md` did not specify one).

Questions were drafted with AI assistance and with some research on what are the questions that retail investors think of daily, and validated against the actual corpus sections via a script checking that each `expected_location` matched a real section and that the answer was supported by the text. An initial draft had 12 rows with non-existent locations and 7 rows (`q08`–`q11`, `q14`, `q28`, `q29`) where answers were outside or mismatched to the corpus (for example, "scarcity tactic" did not appear in `inv-common-scams`, whereas the fee figures in `q08` were present in `inv-understanding-fees`), so those rows were rewritten before tuning or running evaluation.

Examples:
- `single` (`q01`): *"How can I check whether a person promoting an investment is licensed and has a disciplinary history?"* (`inv-five-questions` | `Question 1: Is the seller licensed?`).
- `unanswerable` (`q21`): *"How are short-term versus long-term capital gains taxed for retail investors in the United States?"* (a deliberate trap because two staff bulletins mention "capital gains" in a different context, alongside refusals for SIPC coverage, MiFID II disclosures, FINRA Series 65 passing score, and Bitcoin price / buy timing).

Main limitation: 30 questions is a small set, mostly single-passage and relatively straightforward, so it does not stress-test complex or ambiguous edge cases, and is a bit easy for the model.

## Retrieval

Evaluated with `retrieval_eval.py` across the 25 answerable questions (`single` hits if any top-k chunk matches `expected_source` and `expected_location`; `multi` hits if all expected passages appear in the top-k chunks):

| Design | Hit@1 | Hit@3 | Hit@5 |
| --- | --- | --- | --- |
| `fixed150` (Design A) | 0.360 | 0.640 | 0.640 |
| `section300` (Design B) | 0.640 | 0.840 | 0.880 |

At `@5`, `fixed150` missed `q01`, `q03`, `q04`, `q06`, `q16`, `q26`, `q27`, `q28`, and `q30`, while `section300` missed `q14`, `q26`, and `q28`. For `q14`, `[reg-bi-compliance-guide | 6. What does the Conflict of Interest Obligation require?]` (0.827) ranked first ahead of `[staff-bulletin-conflicts-of-interest | Eliminating Conflicts of Interest]` (0.822), while the exact subsection `[reg-bi-compliance-guide | Are certain conflicts of interest required to be eliminated?]` was not among the top 5 results. For `q26`, `staff-statement-form-crs-disclosures` (three chunks at 0.796, 0.79, and 0.779), `inv-working-with-professional` (0.785), and `staff-bulletin-conflicts-of-interest` (0.769) filled the top 5, while both expected entries (`form-crs-compliance-guide | 4. What topics do I have to include in my relationship summary?` and `staff-bulletin-conflicts-of-interest | Identifying Conflicts of Interest`) were missing from the top 5. For `q28`, `[reg-bi-compliance-guide | Is a broker-dealer required to recommend the lowest-cost security or investment strategy?]` (0.831) was found in the top 5, whereas the `staff-bulletin-account-recommendations` results appeared under `[staff-bulletin-account-recommendations | Questions:]` (0.865 and 0.811) instead of matching the expected location label `Staff Bulletin: Standards of Conduct for Broker-Dealers and Investment Advisers Account Recommendations for Retail Investors`. These misses stem from distinct causes—overlapping documents, a two-topic query, and a label mismatch—and the exact-location hit rule makes some misses stricter than reality.

A single 5-chunk search passes roughly 740 words into the prompt under `fixed150` versus roughly 975 words under `section300` (~230 more words), and the agent averaged ~3,781 input tokens per question overall. I selected `section300` (`ACTIVE_DESIGN = "section300"` in `index.py`) because it outperforms `fixed150` at `@1`, `@3`, and `@5` (lifting `@1` from 9/25 to 16/25) and preserves section context rather than cutting every 150 words, while noting both the higher word count per retrieval and the small sample size (a 6-question gain at `@5`, 16 → 22 of 25). One nuance in `section300` is that headings like `Questions:` recur across multiple chunks in staff bulletins, creating location ambiguity (seen in `q28`).

## Tools and subagent

In `server.py`, the MCP tools are:

- `search`: "Search the investor-protection corpus and return the 5 closest passages, each with a citation. The corpus is public text from the U.S. Securities and Exchange Commission about how brokers and advisers must treat retail investors: the Regulation Best Interest and Form CRS compliance guides and FAQs, three SEC staff bulletins (care obligations, conflicts of interest, account recommendations), a staff statement on Form CRS disclosures, and Investor.gov pages on fees, questions to ask before investing, working with an investment professional, common scams and crypto assets. Documents added with add_document are searched too. Use it for any question about those topics, and before answering from your own knowledge. Each result has a Citation like [source | section], a similarity score (higher is closer), the document title, its URL and the passage text. Answer only from the passages and cite the Citation of every passage you use. If no passage answers the question, say you do not know. Pass the question in natural language, for example "What does the care obligation require?"." It returns the top 5 matching chunks with `Citation: [source | location]`, similarity score, title, URL and text.
- `add_document`: "Add one document to the searchable index: read it, split it into chunks, embed and store them. path is a file path (absolute, or relative to the project folder); .md, .txt, .html and .pdf are supported. Every chunk keeps the file name as its source and its section (or page) as location. If the document is already indexed unchanged, nothing is embedded and nothing is duplicated. If it changed, its old chunks are replaced by the new ones. A file that would need more than 60 new embeddings is refused, to protect the free daily quota. Returns a one-line summary." It reads, chunks, embeds and indexes a supported file.

Example of one `search` result (query: "Regulation Best Interest disclosure obligation in writing"). Each result carries its citation, similarity, title, URL and text:

```text
### Result 1 (similarity 0.871)
Citation: [reg-bi-faq | Disclosure Obligation]
Document: Regulation Best Interest: Frequently Asked Questions
URL: https://www.sec.gov/tm/faq-regulation-best-interest
Text: Q: I am an associated person of a broker-dealer; are there circumstances where I can provide
oral disclosures, or provide written disclosures after a recommendation is made [...]
A: Only in limited circumstances. [...]
```

The `corpus-researcher` subagent (`.claude/agents/corpus-researcher.md`) is restricted to `mcp__corpus__search` and must answer in at most 5 sentences with citations, or reply "The corpus does not cover this."

When launching the MCP server from the editor, SSL failed with `CERTIFICATE_VERIFY_FAILED` against the Windows certificate store. Injecting `truststore` inside a `try/except` block in `server.py` resolved it (running `main.py ask` from the terminal did not hit the issue). One nuance in the subagent's answer on written disclosures: saying a standalone broker can meet the disclosure with the Relationship Summary is accurate only for the capacity disclosure (acting as a broker-dealer). Per the FAQ, Form CRS alone generally does not satisfy the whole Disclosure Obligation.

Transcript (Claude Code in VS Code, trimmed to the essentials). The first run failed because the MCP server launched from the editor could not verify Google's SSL certificate. After adding `truststore` to `server.py` and reconnecting the `corpus` server, both questions below worked.

```text
You: Use the corpus-researcher subagent to answer: What must a broker give a retail investor in
writing under Regulation Best Interest?

Agent (corpus-researcher), tool used: mcp__corpus__search

Answer (from the subagent):
- Before or at the time of a recommendation, the broker-dealer must give the retail customer full
  and fair disclosure in writing. It must cover all material facts about the scope and terms of the
  relationship, and all material facts about conflicts of interest tied to the recommendation
  [reg-bi-compliance-guide | 4. What does the Disclosure Obligation require?].
- Those relationship facts include that the firm or its associated person is acting as a
  broker-dealer. A standalone broker-dealer can generally meet this by delivering the Relationship
  Summary [reg-bi-faq | Disclosure Obligation].
- There is limited flexibility: written disclosures can be updated orally for facts not reasonably
  known when they were written, and where existing rules allow disclosure after the recommendation
  (for example a trade confirmation or prospectus), that document can come afterward
  [reg-bi-faq | Disclosure Obligation].

You: Run the corpus-researcher subagent again with a question about capital gains taxes.

Answer (from the subagent): "The corpus does not cover this." The corpus covers what brokers and
advisers must do under Reg BI, Form CRS and the SEC staff bulletins, plus Investor.gov pages on
fees, questions to ask before investing and scams.
Why it refused: two passages mention taxes, but neither says how capital gains are taxed, so under
rule 5 they do not count as an answer:
- the care-obligations bulletin lists "limiting capital gains" as a tax goal a firm should consider
  [staff-bulletin-care-obligations | Understanding the Retail Investor's Investment Profile];
- the Reg BI FAQ says selling class A mutual fund shares "could generate a taxable event"
  [reg-bi-faq | Care Obligation].
Best similarity for the tax question: about 0.65 (for the Reg BI question: 0.871).
```

## Adding a document

Index update policy: if a document is already indexed and unchanged (matched via content-hash chunk IDs), no chunks are re-embedded or duplicated; if a document is modified, its prior chunks are removed and replaced with new chunks; if indexing would require more than 60 new embeddings, the operation is rejected to protect the daily free quota. `add_document` writes only to the active design (`section300`).

Demo on `q21` (U.S. capital gains tax):
- **Before**: Refused with *"The corpus does not cover this..."* and noted what the corpus covers.
- **Added document**: `extra_docs/irs-capital-gains.md` (IRS Topic No. 409, *Capital gains and losses*, public-domain U.S. government content, ~900 words, 8 chunks including `"Short-term or long-term"` and `"Capital gains tax rates"`).
- **After**: Answered using 0%, 15%, or 20% income-based rates and cited `[irs-capital-gains | Short-term or long-term, irs-capital-gains | Capital gains tax rates]`, with the added document appearing in the top 3 results (similarities 0.775, 0.752, 0.695).
- **Second call**: Reported that the document *"was already indexed unchanged"*.

On the first attempt, `q21` still refused; that download had broken encoding characters (`Â`, `â€œ`), and after fixing the encoding and re-adding it answered (though encoding was not proven to be the sole cause). Also, in the demo answer, 25% and 28% were grouped together with collectibles and qualified small business stock, whereas 28% applies to collectibles and qualified small business stock and 25% applies to unrecaptured Section 1250 gain—making this a real wrong answer from a right passage that occurred only during the demo before the extra document was removed. Afterwards, `remove_extra.py` removed the extra document so the index returned to 300 chunks for evaluation and submission.

## Harness and guardrails

`AGENTS.md` enforces rules including: always search before answering; rely only on retrieved passages; cite every claim as `[source | location]`; if uncovered, say *"The corpus does not cover this."* plus one line on what the corpus covers; do not treat a topically related passage as an answer; give no personal financial advice; search again if two passages are needed; call `add_document` only when requested by the user; and respond in English in at most 6 sentences.

Human approval gates `add_document` in the terminal (`Allow it? [y/N]`), returning `"The human refused: the document was NOT added"` on `n`. A `ModelCallLimitMiddleware` caps model calls at 6 per question.

My extra citation guardrail checks that every `[source | location]` citation in the output matches a passage returned by `search` in that run, replacing the answer with a refusal if not. It triggered on two false positives that helped refine it: (1) Gemini grouped multiple citations inside one bracket like `[a | x, b | y]`, which the parser now splits, and (2) a run that only called `add_document` was replaced despite having no search citations to check, so that case is now skipped. In the final 30-question evaluation, `guardrail_replaced` was `False` on all 30 rows (no real fabricated citation was caught during that run). Both agent and judge used `gemini-3.5-flash-lite`.

## Evaluation

Automated code checks passed 27/30 questions (`single`: 19/20, `multi`: 3/5, `unanswerable`: 5/5), checking refusal phrasing (`does not cover`), valid citations, and expected sources.

My grading rubric:
- `correct` (answerable): captures the main point of the reference answer without needing every detail.
- `correct` (unanswerable): refuses / states the corpus does not cover it (including a refusal that notes a related topic with a valid citation).
- `supported`: every claim is backed by a cited passage, without requiring verbatim wording.

Across all 30 questions:
- **Judge (`gemini-3.5-flash-lite`)**: 30/30 `correct`, 30/30 `supported`.
- **My labels (`human_labels.csv`)**: 30/30 `correct` (`yes`), 29/30 `supported` (`yes`, with `q20` marked `no`), 5/5 correct refusals, 0 wrong refusals, and 1 unsupported claim (`q20`).
- **Agreement**: 30/30 (100%) on `correct` and 29/30 (97%) on `supported`, disagreeing only on `q20`.

High agreement here does not prove the judge is reliable because nearly all my labels were `yes`, so an always-`yes` baseline would match closely. The informative case is `q20`, where the judge missed a real citation error—likely because the judge saw all retrieved chunks rather than only cited ones, and used the same model family as the agent.

Cost and latency per question averaged ~3,781 input tokens, ~145 output tokens and 8.6 seconds, which is about $0.0015 for the agent at $0.30 per 1M input tokens and $2.50 per 1M output tokens per Google´s published pricing. The judge adds about 2,000 tokens per question. Questions that need two searches cost roughly double (for example `q20` at 8,841 input tokens and `q30` at 8,486).

## Failures

- **Over-strict `expected_source` in code checks (3 questions: `q14`, `q26`, `q29`)**: The agent answered accurately with valid citations, just from other corpus documents that also contain the answer (`staff-bulletin-conflicts-of-interest` for `q14`, `staff-statement-form-crs-disclosures` for `q26`, and `inv-crypto-assets` for `q29`). These are test-set labeling issues rather than agent errors, and `questions.csv` was left unchanged instead of adjusting the test to pass.
- **Misattributed citation (1 question: `q20`)**: The opening claim—that firms must eliminate or mitigate conflicts rather than only disclose them—is accurate, but was cited to the third-party compensation disclosure section instead of the eliminating/mitigating sections (`supported = no`).
- **Wrong answer from right passage (1 demo case: `extra_docs/irs-capital-gains.md` on `q21`)**: The demo answer grouped the 25% and 28% tax rates together under collectibles and qualified small business stock, whereas 28% applies to those assets and 25% applies to unrecaptured Section 1250 gain. This happened only during the demo, and the extra document was removed afterward.
- **Retrieval misses (`@5`)**: `section300` missed `q14`, `q26`, and `q28`, while `fixed150` missed 9 questions (`q01`, `q03`, `q04`, `q06`, `q16`, `q26`, `q27`, `q28`, `q30`). In `section300`, `q14` and `q26` are real misses under the exact-location rule (caused by overlapping documents and a two-topic query, respectively), while `q28` is just a heading mismatch (`Questions:` vs. the full bulletin title); wrong refusals: 0.

What to fix first: (1) allow alternative valid sources in `expected_source`, (2) pass only cited passages—not all retrieved chunks—to the LLM judge, and (3) add harder questions that test nuance and ambiguity.


## Decision

I would release this assistant to real users, but only under clear conditions. In the 30-question test, the agent got 5/5 refusals right and had 0/25 wrong refusals, and the only real error was in `q20`, where it gave the right idea about eliminating or mitigating conflicts but pointed to the third-party compensation disclosure section instead of the right place.

Still, I would not trust these results blindly because of three main limits. First, the test set is small and fairly straightforward, so passing 30 questions does not prove it handles tricky or ambiguous cases well. Second, the LLM judge was not validated and missed the `q20` citation mistake, so automated scores cannot be taken at face value. Third, the corpus is a point-in-time snapshot from `2026-11-20` in English and includes staff bulletins and FAQs that are staff views rather than binding law, so it can go out of date or miss legal detail.

For those reasons, I would only let users rely on it to locate and cite what these SEC documents say—never as personalized financial or legal advice—and with three safeguards in place: always showing the citations, refusing when the corpus does not cover a question, and reminding users to check the primary source before making money decisions. At roughly $0.0015 and 8.6 seconds per question, the cost and speed are acceptable for that kind of lookup use.

## AI use

I used Claude to generate many of the code scripts, and to solve any issues that appeared from not using correctly the libraries and syntax. I also used Claude Code inside of VS. I also used Claude to ideate the 30 questions, and to check that the ones I came up with were relevant and made sense. 
I was te one to come up with the use case, did most of the corpus selection, interpretation, human labels, and final decisions. 
