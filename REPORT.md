# Assignment 3 Report

- **Name**: Eva Yang Garrudo Salvador
- **Student ID**: 20207
- **Group**: BBADBA 5A

All numbers below come from `eval/summary.json`, `eval/retrieval.csv` and `eval/results.csv`, written by `uv run python main.py evaluate`.

## Use case

**Who asks.** The privacy lead (or the founder who wears that hat) of a small EU company, for example a 40-person SaaS start-up with no in-house lawyer. They ask what EU data-protection law actually says: *"How fast must we report a breach?"*, *"Can we email existing customers without opt-in?"*, *"Which transfer clauses apply to our US processor?"*

**What they do with the answer.** They act on it: decide whether to notify the authority, change the cookie banner, sign or redline a contract, or decide that they need to pay a lawyer for this question.

**What a wrong answer costs compared with "I don't know".** A wrong answer is expensive and invisible: a missed 72-hour breach deadline or an unlawful marketing campaign can lead to fines of up to EUR 10-20 million or 2-4 % of turnover (GDPR Article 83), plus the damage to customers' trust. "I don't know" only costs time and money: the user reads the article or asks a lawyer (a few hundred euros). So the system must prefer refusing over guessing, and every claim must be checkable in one click. This is why the rules say *answer only from the passages, cite every claim, and say "The corpus does not cover this."* when the text is missing.

## Corpus

| Document (id in the index) | URL | Date | Licence | Words after cleaning |
|---|---|---|---|---|
| Regulation (EU) 2016/679, GDPR (`GDPR`) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679 | 27.4.2016 | EU legal texts are free to reuse with attribution (Commission Decision 2011/833/EU; © European Union, EUR-Lex) | 54,078 |
| Directive 2002/58/EC, ePrivacy Directive, consolidated text (`ePrivacy`) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219 | 19.12.2009 (consolidated) | same | 5,007 |
| Commission Implementing Decision (EU) 2021/914, standard contractual clauses for transfers to third countries (`SCC 2021/914`) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32021D0914 | 4.6.2021 | same | 15,698 |
| **Total: 3 documents** | | | | **74,783** |
| *Added later through `add_document`:* Commission Implementing Decision (EU) 2021/915, standard contractual clauses between controllers and processors, PDF (`SCC 2021/915`) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32021D0915 | 4.6.2021 | same | 7,308 |

The three documents cover the questions a small company's privacy lead actually has: general obligations (GDPR), cookies and e-mail marketing (ePrivacy) and international transfers (SCCs). They are public legislation, so there is no personal data in them; the only names (the signatures of the Presidents of the institutions) are removed during cleaning.

`index.py` downloads them from the EU Publications Office's Cellar API (`publications.europa.eu/resource/celex/...`), the official machine-readable source behind EUR-Lex. EUR-Lex's own website answers scripts with a bot challenge, and I did not try to get around it.

## Ingestion

**Extract.** HTML/XHTML with BeautifulSoup (one line per leaf block: paragraph, table cell, heading), PDF with pypdf (one line per text line, with its page number), and plain text. Everything goes through the same `extract → structure → chunk → embed` functions, so `add_document` imports the pipeline instead of rewriting it.

**Clean.** Footnotes, footnote call-outs, amendment markers (`▼M2`) and running headers are removed. Signatures are dropped. List markers that sit in their own table cell (`(a)`, `(12)`) are joined to the text that follows, so a point never loses its letter and a recital keeps its number.

**Structure.** Regular expressions recognise `CHAPTER`, `Section`, `Article N` (with its title on the next line), `ANNEX`, `Clause N`, the `MODULE ONE…FOUR` sub-headings of the SCCs, and the numbered recitals before "HAVE ADOPTED THIS REGULATION".

**Extraction problems I fixed.**
1. In the PDF, pypdf drops spaces in headings: `Clause7`, `Clause 5 - Optional`. The clause regex missed them, so Clause 7 was glued to Clause 6. Fix: `^Clause ?(\d+)` and an optional "- Optional" suffix.
2. A heading right after another heading was swallowed as its title. In the SCCs, `SECTION I` was followed by `Clause 1`, and `Clause 1` became the section's title, so Clause 1 disappeared from the index. Fix: a line that is itself a heading is never taken as a title.
3. Footnote call-outs such as "(1)" inside the text were indistinguishable from recital numbers. Fix: delete the `oj-note` / `oj-super` elements before extracting text.

**Chunking: two designs, both indexed.**
- **structured**: one chunk per article, clause or annex. Articles longer than 350 words are split at paragraph boundaries ("part 2 of 3"). The SCCs always split where a new MODULE starts. Consecutive recitals are grouped up to 300 words. Result: 378 chunks, average 195 words.
- **fixed** (baseline): 400-word windows with 50 words of overlap, ignoring structure. Result: 211 chunks, average 397 words.

**Metadata on every chunk.** `doc_id`, `doc_title`, `file`, `location` (e.g. `Article 33`, `Recitals 26-28`, `Annex, Clause 9`), `locations` (every unit it covers), `header` (document | chapter | section | article and title | module), `cite` (the ready-made citation, e.g. `GDPR, Article 33`, plus `p. 8` for PDFs), `page`, `part`, `words` and `file_sha` (to detect duplicates).

**Embedding and storage.** `gemini-embedding-2` with 768 dimensions, using `RETRIEVAL_DOCUMENT` for chunks and `RETRIEVAL_QUERY` for questions. The text embedded is header + chunk, so "Article 33: Notification of a personal data breach" is part of the vector. Vectors go to ChromaDB in `index/chroma/` (14 MB in total), saved after every batch of 50. A chunk's id is a hash of its content, so `main.py index` embeds only chunks without a saved vector; a second run embeds 0. Question vectors are cached in `index/query_cache.json` (85 questions so far), so evaluation re-runs and the server never pay for the same question twice. One problem appeared here: `gemini-embedding-2` turns a plain list of strings into one multimodal input and returns one vector. Each text has to be sent as its own `Content`; the code now checks that it gets back as many vectors as texts.

Embedding cost: 378 + 211 corpus chunks, 34 for the added PDF and 85 questions, about 710 embeddings, within one day's free tier.

## Test set

I wrote 38 questions in `eval/questions.csv` from the documents before tuning anything: **26 single, 6 multi (two passages), 6 unanswerable**. Each one was checked against the extracted text. They are phrased the way the privacy lead would ask, not with the law's words (*"We have 40 employees. Do we have to keep records of processing activities?"* rather than "Article 30(5)"). Some are deliberately tricky. q21 asks for a period the SCCs leave blank ("[Specify time period]"), so the right answer is "the parties fill it in". q19 asks for a number of hours that the ePrivacy Directive does not give. The unanswerable questions stay close to the topic: Decision 2021/915 (not in the corpus until I add it), the AI Act, the EU-US Data Privacy Framework, Spain's age of digital consent (the GDPR gives 16 and a 13 floor but not the Spanish number), how long cookie consent lasts, and the NIS2 deadline. The format is documented in `eval/README.md`.

Two examples:

| id | question | kind | expected | reference answer |
|---|---|---|---|---|
| q18 | Can we send marketing emails to existing customers who never opted in? | single | ePrivacy, Article 13 | Yes, if the e-mail was obtained in a sale, is used for our own similar products or services, and customers can object free and easily at collection and in every message. |
| m02 | What is the maximum fine for failing to notify a personal data breach to the supervisory authority? | multi | GDPR Article 33 + Article 83 | Article 33 is within "Articles 25 to 39" in Article 83(4)(a): up to EUR 10 000 000 or 2 % of worldwide turnover, whichever is higher. |

## Retrieval

Hit rate on the 32 answerable questions: a hit at k means one of the top-k chunks covers the expected article, recital or clause. "Both@5" counts multi questions where both passages were in the top 5. "Words in prompt" is what k = 5 adds to the model's context.

| design | search | chunks | hit@1 | hit@3 | hit@5 | both passages@5 (multi) | words in prompt (k=5) |
|---|---|---|---|---|---|---|---|
| **structured** | **dense** | 378 | **81%** | **100%** | **100%** | **67%** | **1,196** |
| structured | BM25 keywords | 378 | 47% | 59% | 66% | 0% | 1,253 |
| structured | hybrid (RRF) | 378 | 53% | 75% | 88% | 33% | 1,244 |
| fixed 400 w | dense | 211 | 66% | 97% | 97% | 50% | 1,989 |
| fixed 400 w | BM25 keywords | 211 | 38% | 59% | 69% | 0% | 1,981 |
| fixed 400 w | hybrid (RRF) | 211 | 56% | 88% | 91% | 33% | 1,982 |

**Chosen: structured chunks + dense search, k = 5** (written to `index/config.json`, which `server.py` reads). It wins on every hit rate and puts 40 % fewer words in the prompt than fixed windows, because an article-sized chunk is exactly the unit a legal question is about. Hit@1 rises from 66 % to 81 % because a fixed window that starts in the middle of Article 32 and ends in Article 34 is a blurry match for "breach notification". Hybrid search *hurt*: my users ask in everyday words ("hire another processor", "opted in"), while the law says "engage another processor" and "prior consent". BM25 rewards exact word overlap and pulls in chunks that merely repeat common words, and fusing it with the dense ranking lowered the dense ranking's quality. A metadata filter (the optional `document` argument of `search`) is available to the agent, but I did not make it part of the evaluated design.

## Tools and subagent

**`search(query, document="")`**. Its description, which the model reads: *"Search the EU data-protection corpus: the GDPR (Regulation (EU) 2016/679, recitals and articles), the ePrivacy Directive 2002/58/EC (consolidated 2009, cookies, direct marketing, traffic and location data) and the Commission's standard contractual clauses for transfers to third countries (Decision (EU) 2021/914), plus any document added later. Use it for any question about what these legal texts say. Ask in plain words; quote legal terms when you know them. Call it again with different words if the first results do not contain the answer. Optional `document` limits results to one document id… Returns the 5 most relevant passages, each with a line `CITE AS: [document, location]`. Copy that citation exactly after every claim that relies on the passage."*

**`add_document(path)`**: *"Add one document to the corpus index: a local file path to an .html/.xhtml, .pdf or .txt file. The file is extracted, cleaned, chunked with the same pipeline as the corpus, embedded with Gemini and stored, and becomes searchable at once. If the same file content is already indexed nothing is re-embedded; if a document with the same name but different content is indexed, its old chunks are replaced… Only use it when the user asks to add a document."* The server also refuses other file types and files over 20 MB.

The server loads the committed index at startup and never re-embeds the corpus. It prints nothing to stdout.

**One search result** (the agent's query for q01; the first of 5 passages, shortened):

```
[1] CITE AS: [GDPR, Recital 85]
    source: Regulation (EU) 2016/679 (General Data Protection Regulation)
    location: GDPR | Recital 85
    document: GDPR | covers: Recital 85
(85) A personal data breach may, if not addressed in an appropriate and timely manner, result in physical,
material or non-material damage ... the controller should notify the personal data breach to the supervisory
authority without undue delay and, where feasible, not later than 72 hours after having become aware of it ...

[2] CITE AS: [GDPR, Article 33]
    location: GDPR | Chapter IV – Controller and processor | Section 2 – Security of personal data |
              Article 33: Notification of a personal data breach to the supervisory authority
...
```

**Subagent** (`.claude/agents/corpus-researcher.md`, tools: `mcp__corpus__search` only). Its instructions:

> You are a research assistant for the privacy lead of a small EU company. You can only use the `search` tool of the `corpus` MCP server; you have no other source.
> 1. Search the corpus with the user's question. If the passages do not contain the answer, search once or twice more with other words (legal terms, the article you expect, the document name in `document`).
> 2. Answer in at most 150 words, using only what the passages say. Quote numbers and deadlines exactly.
> 3. After every claim, put the citation exactly as the passage gives it after `CITE AS:`, for example `[GDPR, Article 33]`. Never invent or alter a citation.
> 4. If the passages do not answer the question, reply `The corpus does not cover this.` and one sentence on what is missing. Do not answer from memory, even if you know the answer.
> 5. If only part is covered, answer that part with citations and say which part is not covered.

**Transcript from Claude Code** (desktop app, run in this repo on 24.11.2026; full version with every search result in `eval/subagent_transcript.md`):

> **Prompt to the subagent:** Can we send marketing emails to our existing customers if they never opted in?
>
> **Tool call 1:** `mcp__corpus__search {"query": "electronic mail direct marketing existing customers similar products opt-out", "document": "ePrivacy"}` returned `[1] CITE AS: [ePrivacy, Article 13]` … "Notwithstanding paragraph 1, where a natural or legal person obtains from its customers their electronic contact details for electronic mail, in the context of the sale of a product or a service … may use these electronic contact details for direct marketing of its own similar products or services provided that customers clearly and distinctly are given the opportunity to object …" (+ 4 more passages)
>
> **Tool call 2:** `mcp__corpus__search {"query": "right to object to direct marketing processing", "document": "GDPR"}` returned `[1] CITE AS: [GDPR, Article 21]` … (+ 4 more passages)
>
> **Final answer:** Yes, under limited conditions. Without consent, email marketing is not allowed: it "may be allowed only in respect of subscribers or users who have given their prior consent" [ePrivacy, Article 13]. There is one exception for existing customers. If you got a customer's email address "in the context of the sale of a product or a service", you may use it for direct marketing of "its own similar products or services". This applies only if customers "clearly and distinctly are given the opportunity to object, free of charge and in an easy manner", both "at the time of their collection and on the occasion of each message" [ePrivacy, Article 13]. You may not hide the sender's identity, and every email needs "a valid address" where the recipient can ask you to stop [ePrivacy, Article 13].
>
> Under the GDPR, customers can object to direct marketing "at any time". After they object, their data "shall no longer be processed for such purposes" [GDPR, Article 21]. You must tell them about this right "at the latest at the time of the first communication" [GDPR, Article 21].
>
> The corpus does not say how each Member State has written these rules into its national law.

The subagent used the `document` filter on its own and combined two documents correctly.

## Adding a document

**Already indexed.** I decided that `add_document` compares the file's SHA-256 hash with the hash stored on the chunks:
- **Same content already indexed:** nothing happens and nothing is re-embedded, so no quota is spent.
- **Same document name, different content** (a new version): its old chunks are deleted and the new ones embedded, so the index never holds two contradictory versions.
- **New document:** chunk, embed, store.

The server reloads its in-memory index straight away.

**The demo** (`eval/add_document_demo.json`, run by `main.py evaluate` through the MCP tool):

- **Unanswerable question u01:** *"Under the Commission's standard contractual clauses for controller-processor contracts within the EU (Decision 2021/915), what must a processor's breach notification to the controller contain?"*
- **Before:** "The corpus does not cover this. Commission Implementing Decision (EU) 2021/915 is not included in the corpus."
- **`add_document("docs_to_add/SCC_2021_915.pdf")`:** "Added new document 'SCC 2021/915'. 34 chunks, 34 embedded and stored."
- **The same call again:** "Already indexed: 'SCC 2021/915' (34 chunks) with identical content. Nothing was re-embedded."
- **After:** "For a personal data breach concerning data processed by the processor, the notification must contain at least: a description of the nature of the breach, including (where possible) the categories and approximate number of data subjects and data records concerned [SCC 2021/915, Annex, Clause 9, p. 8]; the details of a contact point where more information can be obtained [SCC 2021/915, Annex, Clause 9, p. 8]; the likely consequences of the breach and the measures taken or proposed … [SCC 2021/915, Annex, Clause 9, p. 8]. If it is not possible to provide all information at the same time, the initial notification must contain the information then available … [SCC 2021/915, Annex, Clause 9, p. 8]."

This matches Clause 9.2 of the Decision, and the citation carries the PDF page number. (The main evaluation runs with `CORPUS_EXCLUDE="SCC 2021/915"` so that u01 is measured on the base corpus.)

## Harness and guardrails

`agent.py` is LangChain `create_agent` on `gemini-3.5-flash-lite`. It reaches `server.py`'s two tools over MCP (stdio), exactly as an editor does, with `AGENTS.md` as the system prompt.

**AGENTS.md rules (each with its reason in the file):**
1. Search before every answer; search again with other words if needed. *(Memory may be outdated or mix up laws.)*
2. Answer only from the results. *(An unsupported claim looks as confident as a supported one.)*
3. Cite every claim exactly as `CITE AS:` gives it. *(The user must be able to check it; code verifies it.)*
4. If not covered, say exactly "The corpus does not cover this." plus what is missing; answer only the covered part. *(A wrong legal answer costs far more than "I don't know".)*
5. Quote numbers and deadlines exactly. *(Paraphrased time limits are where errors get expensive.)*
6. At most about 150 words. *(The one sentence that matters must not get lost.)*
7. Only add documents on explicit request. *(Adding a document changes every later answer.)*

**Approval before `add_document`.** The tool wrapper stops and asks the person at the terminal. If nobody is there (no TTY, as in `check.py` or evaluation), the answer is "no". From `eval/approval_transcript.txt`:

```
$ python agent.py "Please add the file docs_to_add/SCC_2021_915.pdf to the corpus."
The agent wants to add 'docs_to_add/SCC_2021_915.pdf' to the index (this embeds it and changes later answers).
Approve? [yes/no] yes
The document `docs_to_add/SCC_2021_915.pdf` has already been indexed as "SCC 2021/915" and is available in the corpus.

$ python agent.py "Add docs_to_add/SCC_2021_915.pdf to the index please."
Approve? [yes/no] no
The user did not approve adding this document. Nothing was added.
```

**Limits.** At most 6 tool calls and 8 model calls per question (`ToolCallLimitMiddleware`, `ModelCallLimitMiddleware`).

**My extra guardrail: the citation check.** After the agent answers, code extracts every `[...]` citation and checks it against the `CITE AS:` lines the search tool actually returned in this run. A non-refusal answer must cite at least one. If a citation is unknown or the answer has none, the model gets one repair round that lists the allowed citations. If it still fails, the answer is **withheld** and replaced by a refusal. An answer the user cannot check never reaches them.

**Where it fired.** In the evaluation, it fired once, on m02 (*maximum fine for not notifying a breach*): the first draft failed the check, the repair round produced an answer citing `[GDPR, Article 83]`, and that answer is correct. (The first version of the harness did not save the rejected draft; it does now.) When I re-ran the same question on its own (`eval/guardrail_cases_first_version.json`), the draft was *"…up to 10 000 000 EUR, or … 2 % of the total worldwide annual turnover … [GDPR, Article 83, paragraph 4]"*. That is a **correct** answer: Article 83 was retrieved, and "paragraph 4" only points inside it. The first version of the check did not accept the extra words, the repair failed again, and the guardrail **blocked a correct answer**, which turned into a wrong refusal. I changed the check to accept paragraph references inside a retrieved article (`Article 33(1)`, `Article 83, paragraph 4`) while still rejecting any article that was not retrieved. Over-blocking is the price of this guardrail: it turns a possible unsupported claim into a refusal, which for my use case is the cheaper error.

## Evaluation

`main.py evaluate` runs the agent on all 38 questions through `server.py`. Answers, traces and costs are saved to `eval/answers.jsonl` as they come, and re-runs only ask what is missing, so the stage can be repeated on the free tier.

**Code checks (no LLM):**
- **Citations valid:** every cited source was returned by search: **38 / 38**.
- **Uncited answers that were not refusals: 0.**
- **Refusal detection** (the exact sentence): refused **6 / 6** unanswerable questions and **0 / 32** answerable ones.
- **Expected article cited:** for answerable questions, the article in `questions.csv` is among the citations: **32 / 32**.
- **Expected passages retrieved:** all expected passages were in the search results for 31 / 32. The exception was m05, where GDPR Article 95 never came back.
- **Guardrail:** 37 passed, 1 repaired (m02), 0 blocked.

**LLM judge.** `gemini-3.1-flash-lite`, a different model version from the agent. I couldn't use a bigger judge: the free tier allows only 20 requests a day for the Flash models. The judge gets the question, the reference answer, every passage the agent retrieved (as evidence) and the answer. Its rubric (`RUBRIC` in `evaluate.py`), in short:
- **correct = 1** when the key facts of the reference (numbers, deadlines, conditions) are there and not contradicted. A missing *minor* detail is fine; a missing *key* condition is 0. For an unanswerable question, 1 only if the answer says the corpus does not cover it. A refusal of an answerable question is 0.
- **supported = 1** when every claim is stated in the retrieved passages, even if the claim is true in reality but missing from them. A pure refusal is supported.

The final outcome combines both. Refusal and citation validity come from code; correct and supported come from the judge.

| outcome | count |
|---|---|
| correct (answerable, judge correct and supported) | **32 / 32** |
| incorrect (supported but wrong) | 0 |
| unsupported (made something up) | 0 |
| wrong refusal | 0 |
| correct refusal | **6 / 6** |
| answered an unanswerable question | 0 |

**Agreement with my own grades.** <<AGREEMENT>>

## Failures

The automatic classification in `eval/results.csv` finds **no failed question** in the main run. By the definitions in the brief:

| cause | count |
|---|---|
| retrieval miss | 0 |
| wrong answer from the right passage | 0 |
| unsupported claim | 0 |
| wrong refusal | 0 (1 in the guardrail stress test, now fixed) |
| bad test question | 0 |

<<HUMAN_FAILURES>>

Because a perfect score on 38 questions mostly says the test is too easy for this system, these are the weak spots I found by reading the answers and the traces:

1. **Partial retrieval miss, m05** (*legitimate interests for analytics cookies?*). The answer is right ("No: ePrivacy Article 5(3) requires consent unless strictly necessary") but rests on one passage only: GDPR Article 95, the article that explains *why* the ePrivacy rule wins over the GDPR's legitimate interests, was never retrieved. On a harder variant of the question this would become an unsupported claim.
2. **Wrong refusal caused by my own guardrail** (stress test, described above). Fixed by accepting paragraph references.
3. **Incomplete but "correct" answers.**
   - q19 (*how fast must a telecom provider notify a breach under ePrivacy?*) answers "without undue delay" but leaves out that subscribers must also be told when they are adversely affected.
   - q24 (*which law governs the SCCs?*) blurs the difference between Modules 1-3 (an EU Member State's law) and Module 4 (any country that allows third-party beneficiary rights).

   The lenient judge counted both as correct; a strict lawyer would not.
4. **Latency outliers.** q23 took 101 s and q21 54 s. The time went to waiting on Gemini's free-tier rate limits and "high demand" 503 errors, not to thinking.

**What to fix first:** retrieval for multi-passage questions. Only 67 % of multi questions get *both* passages in the top 5. A second search per sub-question (the agent already does this sometimes), or retrieving the articles a passage cross-references (Article 83 names "Articles 25 to 39"), would address m05 and m02. Next comes a stronger judge, or a second judge, on the borderline answers.

## Decision

**Would I let users rely on it?** Yes, for one job: finding and quoting what the GDPR, the ePrivacy Directive and the 2021 transfer clauses say, as the first step before a decision. Every answer carries citations that code has verified against the retrieved text, and the system refused all 6 out-of-scope questions instead of guessing. **No** for the decision itself: the corpus has no national law, no EDPB guidelines, no case law and no later acts (AI Act, Data Act, Data Privacy Framework), and many real questions depend on those.

**Safeguards:**
- Keep the citation guardrail and the exact refusal sentence.
- Show the cited article text next to the answer, so the user reads the source and not only the summary.
- Treat any answer about a deadline, a fine or an international transfer as "check the cited article before acting".
- Keep `add_document` behind human approval, so the corpus only changes on purpose.

**Cost and latency per question** (38 questions, `gemini-3.5-flash-lite`):
- **4,897 tokens on average**: 4,749 input (mostly the 5 retrieved passages, about 1,200 words, plus AGENTS.md) and 148 output.
- **1.2 search calls**, so about 1.2 query embeddings when the question is new.
- **Median 7.9 s**, mean 13.1 s; the mean is pushed up by rate-limit retries on the free tier.
- **Judging:** about 2,500 extra tokens per answer.

On the free tier the money cost is zero. The real limits are the free-tier quotas: about 1,000 embeddings a day and 20 requests a day for the larger Flash models, which is why the agent and the judge use Flash-Lite models.

## AI use

I used **Claude Code** (Claude Opus 5.5, by Anthropic) for most of the work, and I disclose it in full:
- **Code:** it wrote all of it: `index.py`, `rag.py`, `server.py`, `agent.py`, `evaluate.py` and `grade.py`.
- **Content:** it proposed the use case and the corpus, the two chunking designs, the 38 test questions with their reference answers, the rules in `AGENTS.md` and the subagent, and the judge's rubric. It checked every question against the extracted text.
- **Report:** it drafted this report from the evaluation output.

What I did myself:
- accepted the use case, the corpus and the ship decision as mine, after reading them;
- created my Gemini key and put it in `.env`;
- forked the repository;
- ran the subagent in Claude Code (the transcript above);
- graded the answers in `eval/human_labels.csv` with `grade.py`, without seeing the judge's verdicts;
- read and checked this report.

Gemini (`gemini-embedding-2`, `gemini-3.5-flash-lite` as the agent, `gemini-3.1-flash-lite` as the judge) is part of the system itself, not a writing aid.
