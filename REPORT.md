# Assignment 3 Report

- **Name**: Daniel Teixidor
- **Student ID**: 19971
- **Group**: BBADBA 5A 

## Use case

**Who asks.** Client-facing and junior staff at an SEC-registered investment adviser (wealth-management advisors, client associates, business development, new compliance analysts) who need to know what U.S. adviser law says *before* they act: "Can we put this testimonial on the website?", "Can I charge this client a performance fee?", "Do I owe this client a Form CRS before recommending a rollover?".

**What they do with the answer.** They act on it with a real client: they send the marketing piece, sign the fee agreement, open the account. Or, if the assistant says it does not know, they ask the chief compliance officer.

**Cost of a wrong answer vs. "I don't know".** A wrong answer can turn into a violation of the Advisers Act or an SEC rule: a non-compliant advertisement, a prohibited performance fee, a missed delivery deadline. That means deficiency letters, SEC penalties (the Act's tiers go up to $100,000 per violation for a natural person and $500,000 for a firm, before inflation adjustment) and lost client trust. "I don't know" costs a few minutes of the compliance officer's time. So the system must be built to **refuse rather than guess**, and every answer must cite the exact provision so a human can check it in seconds.

## Corpus

All three documents are U.S. Government works, so public domain (17 U.S.C. §105), and contain no personal data. They are downloaded by `main.py index` and also committed in `corpus/`.

| Document | id | URL | Date / version | Licence | Words (after cleaning) |
|---|---|---|---|---|---|
| Investment Advisers Act of 1940, 15 U.S.C. 80b-1 to 80b-21 (statute text, notes removed) | `advisers-act` | https://www.govinfo.gov/content/pkg/USCODE-2023-title15/html/USCODE-2023-title15-chap2D-subchapII.htm | U.S. Code 2023 ed. | Public domain | 16,841 |
| SEC rules under the Advisers Act, 17 CFR Part 275 (39 sections) | `rules-275` | https://www.ecfr.gov/api/versioner/v1/full/2026-11-16/title-17.xml?part=275 | eCFR as of 2026-11-16 | Public domain | 30,243 |
| SEC Commission Interpretation Regarding Standard of Conduct for Investment Advisers, Rel. IA-5248, 84 FR 33669 | `fiduciary-2019` | https://www.federalregister.gov/documents/full_text/html/2019/07/12/2019-12208.html | 2019-07-12 | Public domain | 7,658 |
| **Total** | | | | | **54,742** |

Why these three: the Act sets the prohibitions and the fiduciary framework, Part 275 holds the operational rules that people break in practice (custody, marketing, books and records, codes of ethics, Form ADV/CRS delivery, pay-to-play), and the 2019 interpretation explains the fiduciary duty that the Act never defines. Many real questions need two of them at once, e.g. the performance-fee ban is in the Act (§205) and its qualified-client exemption is in Rule 205-3.

## Ingestion

**Extraction.** Each source has its own parser in `index.py`, because each has clean structure that a generic parser would throw away:

- *U.S. Code HTML* (BeautifulSoup): keeps `h3.section-head` (section), `h4.subsection-head` (subsection) and `p.statutory-body*` paragraphs. The Advisers Act section number (e.g. §205) is read from the source-credit line, so a location reads `15 U.S.C. 80b-5(a)-(b) [Advisers Act §205]`, which is how practitioners cite it.
- *eCFR XML* (ElementTree): one `<DIV8>` per rule; keeps `<P>` paragraphs and flattens tables; drops `<CITA>` (Federal Register citations). The top-level paragraph letter is tracked, with a fix for the `(i)` ambiguity: `(i)` counts as paragraph (i) only if it follows `(h)`, otherwise it is a sub-item.
- *Federal Register HTML*: keeps the body from "I. Introduction" to "List of Subjects" (drops the table of contents, the CFR amendment and the signature), removes footnote markers and the footnote list, builds section keys from the outline (`II`, `II.B`, `II.B.1`) and records the printed page of each paragraph (`84 FR 33673`).

**Cleaning.** Whitespace normalised, en dashes turned into hyphens (so `80b–5` and `80b-5` match), curly quotes straightened.

**Extraction problem I fixed.** The govinfo page of the Act is ~30,000 words, but about 11,000 of them are *editorial and statutory notes*: amendment history like "1996—Pub. L. 104–290 substituted 'regulation' for 'control'…". Indexed as-is, they would compete with the statute itself: a question about §203 registration could retrieve amendment notes about §203 instead of the rule. The notes always start at an `<h4 class="note-head">` and run to the next section heading, so the parser skips that span; the cleaned Act is 16,841 words. A second, smaller problem: footnote markers (`<sup>1</sup>`) were glued into the text ("section 79z–4 1 of this title"), so `<sup>` tags are removed before extracting text.

**Chunking: two designs** (both built by `main.py index`):

| Design | How | Chunks |
|---|---|---|
| `fixed` (baseline) | 200-word windows, 40-word overlap, ignoring structure | 343 |
| `structure` | one chunk per statute section / rule / release section, split at paragraph boundaries near 220 words (max 320); the section heading is repeated at the top of every piece; tiny tails merged | 323 (180 words on average) |

**Chunk metadata.** `id` (what the model cites, e.g. `R275:275.206(4)-2#2`), `source` (document id), `title`, `section` (key used to grade retrieval), `sections`, `section_title`, `location` (human citation), `text`, `words`, `hash` (SHA-256 of model + dimensions + embedded text).

**Embedding and storage.** `gemini-embedding-2`, 768 dimensions. That model takes the task as a text prefix rather than a `task_type`, so documents are embedded as `title: <doc — location — heading> | text: <chunk>` and queries as `task: question answering | query: <question>`. An important detail: each text is wrapped in its own `Content`; with `gemini-embedding-2` a bare list of strings is merged into *one* embedding. Vectors are appended to `index/<design>/vectors.jsonl` batch by batch (50 texts per request), keyed by the chunk hash, so a crash or the daily quota loses nothing and `main.py index` only embeds chunks without a saved vector. The first build embedded 666 chunks (343 + 323), with several automatic pauses for the per-minute rate limit. I used a JSONL + NumPy store instead of ChromaDB: with a few hundred chunks a matrix product is instant, the files diff cleanly in git, and the BM25/hybrid search needs the raw texts anyway. (ChromaDB was also removed from the dependencies, because its `onnxruntime` dependency has no wheel for my macOS 12 laptop.)

## Test set

I wrote the 42 questions in `eval/questions.csv` by reading the documents section by section, before tuning anything, phrasing them as a colleague would ask them (often as a situation, e.g. "Our firm has $105 million under management. Do we have to register with the SEC?"), and wrote a short reference answer with the exact number or condition from the text.

| Kind | Count |
|---|---|
| single (one passage) | 28 |
| multi (two passages, usually the Act + a rule, or the interpretation + a rule) | 7 |
| unanswerable (close to the topic, but not in the corpus) | 7 |

The unanswerable questions are deliberately close: Regulation Best Interest (broker-dealers, not advisers), FINRA Rule 2111, IAR continuing education, IARD fees, Series 66 passing score, wash-sale tax rules. The hardest one is q36, the dollar threshold for a "qualified client": the corpus has the rule, but the rule only says "the dollar amount specified in the most recent order", so the right answer is to say the figure is not in the corpus.

Two examples:

- **q29 (multi)**: *Can a registered adviser charge a client a performance fee based on a share of capital gains, and if so for which clients?* Sources `advisers-act;rules-275`, locations `80b-5;275.205-3`. Reference: §205(a)(1) generally prohibits it; Rule 205-3 exempts contracts with qualified clients.
- **q37 (unanswerable)**: *Under Regulation Best Interest, what does a broker-dealer's care obligation require?* Reference: the corpus does not contain Regulation Best Interest's care obligation. This is the question used for the add-document test.

## Retrieval

A hit means a retrieved chunk is from the expected document *and* covers the expected section (any of the expected passages for multi; `multi_both@5` requires all of them). 35 answerable questions; `words@5` = words added to the prompt by the top-5 chunks.

| design | method | hit@1 | hit@3 | hit@5 | multi_both@5 | words@5 |
|---|---|---|---|---|---|---|
| fixed | dense | 0.914 | 0.914 | 0.943 | 0.714 | 999 |
| fixed | bm25 | 0.829 | 0.914 | 0.943 | 0.857 | 1000 |
| fixed | hybrid | 0.914 | 0.971 | 0.971 | 0.857 | 1000 |
| structure | dense | 0.914 | 0.943 | 0.971 | 0.571 | 964 |
| structure | bm25 | 0.800 | 0.886 | 0.943 | 0.857 | 962 |
| **structure** | **hybrid** | **0.914** | **1.000** | **1.000** | **0.857** | **965** |

**Design chosen: structure + hybrid**, picked by the numbers. `evaluate.py` takes the highest hit@5, breaking ties by hit@3, then hit@1, then fewer words in the prompt, and writes the winner to `index/config.json`, which the search tool reads. It is the only combination that finds an expected passage in the top 3 for all 35 answerable questions, and it adds ~35 fewer words to the prompt than fixed chunks. Two patterns explain it:

- **Hybrid beats dense alone**, especially on two-passage questions. Dense search found both passages for only 4 of 7 multi questions (0.571 with structure), because one passage dominates the embedding of a two-part question; BM25 brings in the second passage through exact terms such as rule numbers ("205-3", "206(4)-7") and defined terms ("investment counsel"). Fusing the two rankings (reciprocal rank fusion) keeps dense search's strong hit@1 and adds BM25's coverage.
- **Structure beats fixed windows** at k = 3: a whole rule paragraph with its heading is one chunk, while 200-word windows cut a condition off from its exception and mix two rules in one chunk.

Note that all designs score high (≥ 0.94 at k = 5): legal text is very distinctive and my questions use its vocabulary. Multi-passage questions remain the weak spot (0.857 at best: one of 7 never gets both passages in the top 5).

## Tools and subagent

`server.py` (MCP, stdio, server name `corpus`) loads the committed index lazily on the first search and never re-embeds the corpus. Only the query is embedded, and query vectors are cached in `index/query_cache.jsonl`.

**`search(query, k=5)`**, description (abridged): *"Search U.S. investment adviser law: the Investment Advisers Act of 1940, the SEC rules under it (17 CFR Part 275: registration, Form ADV and Form CRS delivery, books and records, codes of ethics, performance fees and qualified clients, marketing/advertising, custody, pay-to-play, compliance programs) and the SEC's 2019 interpretation of an adviser's fiduciary duty… Use it for every factual question about these rules, before answering… Search again with other words if the passages do not answer the question; ask separately about each part of a two-part question. Returns up to k passages, each headed `=== [ID] document | location ===`. Cite a passage by its [ID]."*

**`add_document(path)`**, description (abridged): *"Add a document to the searchable corpus. Use only when the user asks to add or index a specific file… extracted, chunked and embedded with the same pipeline as the corpus… If the identical file is already indexed nothing changes; if a different version of the same document was added before, it is replaced. Returns a JSON report."* It imports `index.add_document`, which reuses `extract_document`, `chunk_blocks` and `embed_and_store`.

**One search result** (the agent's query for q11: "qualified custodian send account statements clients custody rule frequency"; first of 5 results):

```
=== [R275:275.206(4)-2#2] SEC rules under the Investment Advisers Act (17 CFR Part 275) | 17 CFR 275.206(4)-2(a) ===
17 CFR 275.206(4)-2 — Custody of funds or securities of clients by investment advisers.
(2) Notice to clients. If you open an account with a qualified custodian on your client's behalf, either under
the client's name or under your name as agent, you notify the client in writing of the qualified custodian's
name, address, and the manner in which the funds or securities are maintained, promptly when the account is
opened and following any changes to this information. [...]
(3) Account statements to clients. You have a reasonable basis, after due inquiry, for believing that the
qualified custodian sends an account statement, at least quarterly, to each of your clients for which it
maintains funds or securities, identifying the amount of funds and of each security in the account at the end
of the period and setting forth all transactions in the account during that period.
```

**Subagent** (`.claude/agents/corpus-researcher.md`, tools: `mcp__corpus__search` only, model: inherit): searches before answering, up to 4 searches, answers only from the passages, cites every claim by ID, copies numbers exactly, and starts with "The corpus does not cover this." when the passages do not answer.

**Transcript from my editor (Claude Code).** A practical problem first: my laptop runs macOS 12, and current Claude Code builds do not run on it, so I installed version 1.0.120 through npm (with Node 22). That version connects to the `corpus` MCP server without problems (`/mcp` shows `corpus ✔ connected`), but its `/agents` screen does not load project subagents: it shows "No agents found", even for the agent created with its own `/agents` wizard. So I asked Claude Code to read `.claude/agents/corpus-researcher.md` and run exactly that system prompt as a delegated subagent (the Task tool), restricted to the corpus search tool. The subagent definition is the same file; only the way it is launched differs.

```
> Read .claude/agents/corpus-researcher.md, then launch a general-purpose subagent (Task tool) whose
  instructions are that file's system prompt. The subagent must use ONLY the corpus search MCP tool,
  no other tools. Question for it: what must an adviser disclose when using a paid testimonial?

● Read(.claude/agents/corpus-researcher.md)
  └ Read 10 lines

● Task(Corpus research on testimonial disclosures)
  └ corpus - search (MCP)(query: "marketing rule testimonial endorsement required disclosures compensation", k: 8)
  [approved: "Yes, and don't ask again for corpus - search"]

Disclosures for a paid testimonial (Rule 206(4)-1)

The adviser must make these disclosures when the testimonial is disseminated. It can make them itself, or it
can reasonably believe the person giving the testimonial makes them [R275:275.206(4)-1#2].

Clear and prominent disclosures [R275:275.206(4)-1#2]:
- The testimonial was given by a current client or investor.
- Cash or non-cash compensation was provided for it, if applicable.
- A brief statement of any material conflicts of interest the person has because of their relationship with the adviser.

Additional disclosures [R275:275.206(4)-1#3]:
- The material terms of the compensation arrangement. This includes a description of the compensation provided
  or to be provided, directly or indirectly.
- A description of any material conflicts of interest from the person's relationship with the adviser or from
  the compensation arrangement.

Related conditions that are not disclosures [R275:275.206(4)-1#3]:
- The adviser needs a reasonable basis to believe the testimonial complies with the rule.
- The adviser needs a written agreement describing the scope of activities and the compensation terms.
- The adviser may not compensate a person it knows, or with reasonable care should know, is an ineligible person.

Exemptions [R275:275.206(4)-1#4], [R275:275.206(4)-1#5], [R275:275.206(4)-1#10]:
- No or de minimis compensation: The testimonial does not need to comply with paragraphs (b)(2)(ii) and (b)(3).
  The (b)(1) disclosures still apply. De minimis means $1,000 or less (or the equivalent in non-cash
  compensation) in the preceding 12 months.
- Affiliated persons: Testimonials by the adviser's partners, officers, directors or employees, or by persons
  under common control with it, are exempt from (b)(1) and (b)(2)(ii). The affiliation must be readily apparent
  or disclosed, and the adviser must document the person's status.
- Registered broker-dealers: They are exempt from (b)(1) if the testimonial is a recommendation subject to
  Regulation Best Interest. They are exempt from (b)(1)(ii) and (iii) if the recipient is not a retail customer.

Disciplined persons: If a person is subject to certain non-disqualifying Commission orders, the advertisement
must carry an extra disclosure for ten years. It must state that the person is subject to a Commission order or
opinion regarding disciplinary action(s), and it must include the order or a link to it [R275:275.206(4)-1#12].

Sources: [R275:275.206(4)-1#2], [#3], [#4], [#5], [#10], [#12], all from the SEC rules under the Advisers Act,
17 CFR 275.206(4)-1.
```

The subagent followed its rules: it searched the corpus once with the rule's own terms, answered only from the retrieved passages, cited every block by passage ID, and copied the $1,000 de minimis amount and the ten-year period exactly. Compared with the reference answer for q15, it is complete and goes further (exemptions, disciplined persons) while staying inside the evidence.

## Adding a document

**Already indexed?** `add_document` hashes the file (SHA-256). If the identical file is already indexed, nothing changes and it says so (`status: already_indexed`). If a *different* file with the same document id (file name) was added before, the new version **replaces** the old one: its old chunks are deleted before the new ones are written. A regulation that was amended must not be answered from both versions at once. Core corpus documents cannot be replaced this way; they are rebuilt with `main.py index`. Unsupported types, missing files and files over 20 MB return an error instead of crashing the server.

**Demo** (`uv run python demo_add_document.py`; it works on a temporary copy of `index/`, so the committed index and the evaluation stay as graded):

- Unanswerable question: q37, *"Under Regulation Best Interest, what does a broker-dealer's care obligation require?"*
- Document added: Regulation Best Interest, 17 CFR 240.15l-1 (eCFR, public domain), saved to `corpus/extra/reg-bi.xml`.

**Before** (from the evaluation run; the demo prints the same):

> The corpus does not cover this. The provided materials cover investment advisers and their fiduciary duty under the Investment Advisers Act of 1940, but do not contain the text of Regulation Best Interest or its broker-dealer care obligation. Please confirm with your firm's compliance officer.

**Adding it** ("Please add the document at corpus/extra/reg-bi.xml to the corpus."). The harness asked for approval at the terminal, I typed `y`, and the tool returned:

```
{"status": "added", "document": "reg-bi", "title": "§ 240.15l-1 Regulation best interest.", "words": 919,
 "chunks": {"fixed": 6, "structure": 5}, "message": "Added '§ 240.15l-1 Regulation best interest.' (919 words, 5 chunks in the structure design)."}
```

**After** (same question, 1 search, 2.6 s):

```
Under Regulation Best Interest, the care obligation requires a broker, dealer, or associated person, when making
a recommendation, to exercise reasonable diligence, care, and skill to:

* Understand risks, rewards, and costs: Understand the potential risks, rewards, and costs associated with the
  recommendation, and have a reasonable basis to believe that the recommendation could be in the best interest of
  at least some retail customers [REGBI:240.15l-1#2].
* Suitability for the particular customer: Have a reasonable basis to believe that the recommendation is in the
  best interest of a particular retail customer based on that customer's investment profile and the potential
  risks, rewards, and costs, without placing the financial or other interest of the broker, dealer, or associated
  person ahead of the customer's interest [REGBI:240.15l-1#2].
* Avoid excessive trading: Have a reasonable basis to believe that a series of recommended transactions—even if in
  the customer's best interest when viewed in isolation—is not excessive and is in the customer's best interest
  when taken together in light of the customer's investment profile [...] [REGBI:240.15l-1#3].

Sources:
  [REGBI:240.15l-1#2] § 240.15l-1 Regulation best interest. | 17 CFR 240.15l-1(a)
  [REGBI:240.15l-1#3] § 240.15l-1 Regulation best interest. | 17 CFR 240.15l-1(a)
```

The refusal turned into a correct, cited answer that matches the rule text (care obligation, 17 CFR 240.15l-1(a)(2)(ii)(A)-(C)), using only the newly added chunks.

**Adding the same file again** returned `{"status": "already_indexed", "document": "reg-bi", "message": "This exact file is already indexed as 'reg-bi'. Nothing was changed."}`: the SHA-256 matched, so nothing was re-embedded.

## Harness and guardrails

`agent.py` uses LangChain `create_agent` on Gemini (`gemini-flash-lite-latest`, set in `settings.py` and overridable with `GEMINI_CHAT_MODEL`; I first used `gemini-flash-latest`, but it kept returning 503 "high demand" errors, so the lighter model became the default). It starts `server.py` over MCP exactly as an editor does, turns its two tools into LangChain tools, and uses `AGENTS.md` as the system prompt.

**AGENTS.md rules (each with its reason in the file):** 1) search before every answer (memory may be outdated); 2) answer only from the search results (an unsupported claim looks exactly like a supported one); 3) cite every claim by passage ID (the user can verify it, the harness checks it); 4) if not covered, start with "The corpus does not cover this." and suggest compliance (a refusal costs a call, a wrong answer can cost a violation); 5) search more than once, at most 4 (answers often sit in two places); 6) copy numbers exactly, and say when the text defers to another source (thresholds are where errors hurt most); 7) short and practical, no legal advice; 8) only add documents when asked.

**Approval before add_document.** The wrapper around the MCP tool asks at the terminal: *"The agent wants to add the document '…' to the index. Approve? [y/N]"*. Only `y` runs the tool; anything else returns "DENIED…" to the model. In a non-interactive run (the evaluation) it is refused automatically.

**Call limits.** `ModelCallLimitMiddleware(run_limit=8)` and `ToolCallLimitMiddleware(run_limit=6)` per question.

**Extra guardrail: citation check.** After the model answers, code checks that (a) every `[ID]` it cites was actually returned by a search in this turn, (b) a non-refusal cites at least one passage, and (c) it searched at all. If a check fails, the model gets one retry with the problem spelled out; if it fails again, the answer is replaced by a refusal. This turns rule 3 from a request into an enforced check. Every firing is logged in `eval/guardrail_log.jsonl`.

**It fired on 3 of 42 questions (q04, q10, q30), and each time the retry passed:**

- **q04** (private fund adviser exemption): the first answer was right in substance but cited invented IDs built from the rule's paragraph numbers, e.g. `[R275:275.203(m)-1(a)(1)]` and `[R275:275.203(m)-1(d)(5)]`. The search had returned `[R275:275.203(m)-1#1]` etc. The guardrail reported "it cites IDs that no search returned in this conversation", and the rewritten answer cites the real IDs.
- **q10**: cited `[IAA:80b-8#2]`, a chunk that was never retrieved.
- **q30**: cited `[R275:206(4)-7#2]`, a mangled ID (missing the "275." prefix, wrong chunk number).

Without the guardrail, three answers would have shown the user citations that lead nowhere. After it, **42/42 answers have only valid citations**.

## Evaluation

`main.py evaluate` ran the agent on all 42 questions (answers in `eval/answers.jsonl`). The judge first stopped at q05 on a Google 503 error; the stage is resumable and finished on the second run.

**Code checks** (no LLM): searched before answering; has at least one citation; all citations are IDs that were really retrieved; refusal (answer starts with "The corpus does not cover this"); for answerable questions, whether the expected passage was among what the agent retrieved; whether the guardrail fired. Refusals are graded by code: right for unanswerable questions, a *wrong refusal* for answerable ones.

**LLM judge** (`gemini-flash-lite-latest`, JSON output). It sees the question, the kind, the reference answer, the full text of every passage the agent retrieved (the evidence) and the answer. Rubric:
- `correct` = 1 if the answer has the same substance as the reference (the key rule, number, condition or exception; extra correct detail is fine). For unanswerable questions, 1 only if it clearly says the information is not in the corpus and does not supply the missing fact.
- `supported` = 1 if every factual claim is in, or follows directly from, the evidence, even if a claim is true in the real world but not in the evidence.

**Results:**

| | Code checks + LLM judge | After my review |
|---|---|---|
| Correct (all 42) | 42/42 (100%) | **40/42 (95%)** |
| Correct on answerable (35) | 35/35 (100%) | 33/35 (94%) |
| Supported | 42/42 (100%) | 42/42 (100%) |
| Unanswerable handled correctly (7) | 7/7 (6 formal refusals + q36) | 7/7 |
| Wrong refusals (35 answerable) | 0/35 | 0/35 |
| Searched before answering | 42/42 | |
| All citations valid (code check) | 42/42 (3 after the guardrail's retry) | |
| Expected passage among the agent's retrieved | 35/35 | |

q36 (qualified-client threshold) is counted as a correct non-refusal: the code check sees no "The corpus does not cover this" opener, but the answer does exactly what the reference asks: it says the figure is set by the SEC's most recent order, does not invent a number, and refers to compliance.

**Agreement with my own grades.** I graded 22 answers in `eval/human_labels.csv` from `eval/to_grade.csv` (answers without the judge's verdicts), choosing q01–q12, q20, all 7 multi questions, q36 and q39 so that every kind is represented:

| field | n | agreement | Cohen's κ |
|---|---|---|---|
| correct | 22 | 91% (20/22) | 0.0 |
| supported | 22 | 100% | n/a (no variance) |

The 91% raw agreement hides the real finding: **the judge never gave a 0**, so κ is 0. It agrees only because most answers are good. The two disagreements are both multi questions the judge passed and I failed (q29, q34, below). This lite judge is too lenient with *incomplete* answers: its rubric says "nothing important missing", but it rewarded answers that were correct as far as they went. Before relying on its numbers I would use a stronger judge model and add to the rubric "for a two-part question, check each part separately".

## Failures

The automatic classification (`eval/failures.csv`) is empty because the judge passed everything; these are the failures from my review:

| Question | Cause | What happened |
|---|---|---|
| q29 (multi: performance fees) | **Wrong answer from the right passage** | The agent retrieved both the Act (`IAA:80b-5#1`) and Rule 205-3, but answered "Yes, … provided the client is a qualified client" without saying that §205(a)(1) *generally prohibits* performance fees. A user could read it as "performance fees are allowed" and miss that the default is a ban. |
| q34 (multi: "reviewed by the SEC" / "SEC approved us") | **Retrieval miss** (agent level) | The agent searched once; all 5 results were marketing-rule chunks, so §208 (`IAA:80b-8`) never reached it. It answered only the performance-review half and ignored "the SEC approved us" and the right to state registration. The agent's own query wording ("advertisement SEC approved reviewed performance figures") pulled everything toward the marketing rule.  |

Smaller issues that I did not count as failures: q12 cites `[R275:275.204-4#1]` for a claim that is really in `206(4)-2#4`. The citation is "valid" (it was retrieved), so the code check cannot catch a citation to the *wrong* retrieved passage. q05 is correct but muddled about the thresholds.

**What to fix first:** both failures are two-part questions answered with one search. AGENTS.md rule 5 already says "for a question with two parts, search for each part", but the lite model ignored it (q29 and q34 each used 1 search; the average was 1.2). The fix is to enforce it in the harness like the citation check: if the question contains "and" / "or" joining two asks and only one search ran, return a nudge to search the other part. Second, upgrade the judge (above).

## Decision

**Would I let users rely on it?** Not as the final word, but yes as a **first stop that always shows the source**. On this test set it answered 40 of 42 correctly, never refused an answerable question, handled all 7 out-of-corpus questions without inventing anything, and every citation it showed points to a real retrieved passage (the guardrail enforced that 3 times). The two failures are the dangerous kind for compliance: answers that are *correct but incomplete* and read as permission ("Yes, you can charge a performance fee…"). The judge missed both, so I would not trust automated grading alone either.

Safeguards for use: (1) anything that leads to a client-facing action (an ad, a fee agreement, a custody arrangement) still goes to the CCO, with the cited passages attached; (2) the citation guardrail stays on, plus the proposed "search each part" check; (3) the UI states that the corpus excludes SEC orders (e.g. current qualified-client thresholds), FINRA rules, Regulation BI and state law; (4) re-run the evaluation with a stronger judge and more multi-part questions before wider use, since 42 questions is a small sample.

**Cost and latency per question** (from `eval/summary.md`, free tier, so $0):

| | mean | median | max |
|---|---|---|---|
| Agent tokens (input + output) | 5,884 | 4,388 | 21,647 |
| Agent seconds | 16.5 | 5.2 | 250.8 |
| Searches | 1.2 | | 3 |
| Judge tokens per judged answer | 2,373 | | |

The median (about 4,400 tokens and 5 seconds) is the typical cost. The mean and the maxima are inflated by API waits: q10's 250 s and 21,647 tokens include rate-limit/503 retries and a guardrail retry with 3 searches. Most tokens are input: the system prompt plus ~965 words of retrieved passages per search.

## AI use

I used Claude (Anthropic) as a coding assistant for the whole pipeline: choosing the corpus, reading the documents to draft the test questions, writing `index.py`, `retrieval.py`, `server.py`, `agent.py`, `evaluate.py`, the subagent and `AGENTS.md`, and drafting this report from my own evaluation results.
