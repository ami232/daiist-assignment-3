# Assignment 3 Report

- **Name**: Clara Zsigmond
- **Student ID**:
- **Group**: PPLEDBA 5A

## Use case

The main users are trade lawyers and trade-policy analysts, for example at a ministry of trade. They use the assistant for a first-pass reading of the WTO agreements: to understand the legal situation a client or government is in before advising on a response. Because the WTO is a system between governments, the same need exists at state level. A government can use it to understand its position before bringing (or defending) a case before a panel.
They then use the answer to decide whether a proposed measure (a tariff, an import ban, a licensing rule) is worth pursuing, whether another country's measure is worth challenging, and which articles to look at closely.

**Why a wrong answer costs more than "I don't know".**
- *A WTO-inconsistent measure.* A wrong "this is allowed" can lead a ministry to adopt a measure that breaches the agreements. The likely result is a dispute, a ruling against it, and, if it does not comply, retaliation authorized under DSU Art. 22.
- *A weak challenge.* A wrong "this is a violation" can lead a government to spend resources disputing another country's measure without a solid legal basis.
- *Credibility.* For a lawyer, citing the wrong article, or claiming something is allowed when it is not, is a serious loss of professional credibility, in front of a client or a panel.

The costs here cannot realistically be expressed as one "one-size-fits-all" monetary amount. I use authorized retaliation as a proxy for the order of magnitude when a measure is found inconsistent and not withdrawn: the US was authorized to suspend concessions worth US$191.4 million a year in *EC – Bananas III* (1999) and US$116.8 million a year in *EC – Hormones* (1999), and the EU up to US$4.04 billion in *US – FSC* (2002). These are not the cost of one wrong answer, but they show what is at stake when a government acts on a wrong reading of the agreements.

**The cost of "I don't know".** At worst, the user has to ask an expert, read the articles themselves, or look for a comparable case and ruling. That is a waste of time, not a legal or financial risk.

## Corpus

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| General Agreement on Tariffs and Trade 1947, incl. Annex I interpretive notes | https://www.wto.org/english/docs_e/legal_e/gatt47_e.htm | 30 Oct 1947, as amended | WTO legal text, "free for public use" | 25,770 |
| General Agreement on Tariffs and Trade 1994 | https://www.wto.org/english/docs_e/legal_e/gatt94_e.htm | 15 Apr 1994 (in force 1 Jan 1995) | same | 885 |
| General Agreement on Trade in Services (GATS), incl. annexes | https://www.wto.org/english/docs_e/legal_e/gats_e.htm | 15 Apr 1994 (in force 1 Jan 1995) | same | 10,960 |
| Agreement on Trade-Related Aspects of Intellectual Property Rights (TRIPS), as amended (Art. 31bis) | https://www.wto.org/english/docs_e/legal_e/trips_e.htm | 15 Apr 1994; amendment in force 23 Jan 2017 | same | 13,617 |
| Agreement on the Application of Sanitary and Phytosanitary Measures (SPS) | https://www.wto.org/english/docs_e/legal_e/sps_e.htm | 15 Apr 1994 (in force 1 Jan 1995) | same | 5,086 |
| Understanding on Rules and Procedures Governing the Settlement of Disputes (DSU) | https://www.wto.org/english/docs_e/legal_e/dsu_e.htm | 15 Apr 1994 (in force 1 Jan 1995) | same | 10,814 |
| **Total** (6 documents, downloaded 24 Nov 2026) | | | | **67,132** |

**Licence.** The WTO's [copyright page](https://www.wto.org/english/info_e/copyrights_permissions_e.htm) says: "Unrestricted official WTO documents and legal texts are free for public use." This is a non-commercial course project. The texts contain no personal data.

## Ingestion

**Extraction.** I use the HTML pages rather than the PDFs, because the HTML keeps the headings and paragraph anchors. Each page is downloaded once to `corpus/`. `parse_provisions()` reads the page from top to bottom and tracks where it is: Agreement > Part > Section > Article > paragraph. Each paragraph becomes a record that carries this full path. Footnotes are moved from the bottom of the page to the paragraph that cites them.

**Cleaning.**
- Navigation menus, scripts and the "Share" block are removed.
- Non-breaking spaces, curly quotes and extra whitespace are normalised.
- All-caps titles are re-cased ("GENERAL OBLIGATIONS AND DISCIPLINES" becomes "General Obligations and Disciplines").
- The tables of contents inside the GATS and TRIPS pages are removed. They had become chunks listing every article title, which matched almost any query.

**Chunking.** I built two designs to compare:
1. **Fixed** (baseline): 200-word windows with 40 words of overlap, ignoring structure.
2. **Structured**: one chunk per article. Articles over 350 words are split between paragraphs, never inside one. Each chunk starts with a header that gives its citation and place in the agreement, for example `[TRIPS Art. 31(a)-(f)] TRIPS > Part II > Section 5: Patents > Article 31: Other Use Without Authorization of the Right Holder`.

Chunks are embedded with `gemini-embedding-2` and stored in ChromaDB (`index/chroma`), one collection per design. A chunk's ID is a hash of its text, so re-running `main.py index` only embeds new or changed chunks.

**An extraction problem I fixed.** GATT marks articles that have an interpretive note with an asterisk ("Article III *"). The parser did not recognise these headings, so the text of these articles ended up under the previous article. The asterisk is now stripped from the heading and kept as a link to the note (Ad Article III), which is stored in the chunk metadata.

**Chunk metadata.** `agreement`, `document` (full title), `part`, `section`, `article`, `article_title`, `paragraphs`, `citation` in the agreement's own style (GATT Art. III:4, SPS Art. 2.2), `parent_id` (the whole article), `piece` (e.g. 2 of 5), `url` (links to the article), `interpretive_note` and `words`.

**Number of chunks.**

| Design | Chunks | Words per chunk (median / max) | GATT | GATT 1994 | GATS | TRIPS | SPS | DSU |
|---|---|---|---|---|---|---|---|---|
| Structured | 354 | 195 / 350 | 126 | 4 | 58 | 89 | 27 | 50 |
| Fixed | 438 | 200 / 200 | 162 | 6 | 74 | 90 | 34 | 72 |

## Test set

I am currently taking International Trade Law, so I wrote the questions I would want to ask an AI assistant if I were a trade lawyer. I knew many could be answered from the corpus. I was unsure about some, and I knew others definitely could not (such as cases we saw in class, which are not part of the agreements).

**Counts by kind** (43 questions):

| Kind | Count | Questions |
|---|---|---|
| Answered from one passage (`single`) | 22 | q01–q18, q34, q37, q38, q40 |
| Needs more than one passage (`multi`) | 10 | q19–q25, q33, q42, q43 |
| Unanswerable | 11 | q26–q32, q35, q36, q39, q41 |

Examples:

*Can be answered from one passage.* Question 40: What conditions does the introductory paragraph of GATT Article XX (the "chapeau") place on the general exceptions?
It can be answered from the GATT alone (Article XX). I first wrote it as "What is the chapeau?", but the word "chapeau" is never defined in the agreements; it appears only in an SPS footnote. So the question was not answerable from one passage, and it was missed in retrieval by every design. I rephrased it to name the passage it is about.

*Requires more than one passage.* Question 19: How does the scope of National Treatment differ between the GATT and the GATS? It needs GATT Article III and GATS Article XVII.

*Unanswerable.* Question 36: What is the Harmonized System? It is not part of these agreements.

## Retrieval

**How it is measured.** For each of the 32 answerable questions, `evaluate.py` takes the top 5 chunks of each design. A chunk is a hit when its agreement and article match the expected ones (paragraphs are ignored). **hit@k** is the share of questions with an expected passage in the top k. For the 10 multi questions, **all@k** is the share where every expected passage is in the top k. **Words added** is the number of words the top k chunks add to the prompt.

**The four designs.** Fixed and structured chunks, each ranked either by vector search (cosine similarity of embeddings) or by hybrid search (vector search combined with BM25 keyword search).

| Design | hit@1 | hit@3 | hit@5 | multi all@3 | multi all@5 | words added @5 |
|---|---|---|---|---|---|---|
| fixed + vector | 0.81 | 0.94 | 0.97 | 0.2 | 0.3 | 1,000 |
| **structured + vector** | 0.81 | 0.94 | 0.97 | **0.6** | **0.6** | 1,203 |
| fixed + hybrid | 0.53 | 0.72 | 0.84 | 0.3 | 0.3 | 1,000 |
| structured + hybrid | 0.75 | 0.88 | 0.88 | 0.3 | 0.6 | 1,208 |

(Source: `eval/retrieval_summary.csv`; per question in `eval/retrieval_per_question.csv`.)

**The design I chose: structured + vector, top 5.** It ties with fixed + vector on hit@1/3/5 and finds all passages for twice as many multi questions (0.6 against 0.3 at k = 5), for about 20% more words. Hybrid search did worse on every measure, probably because words like "Member", "measure" and "agreement" appear in almost every chunk, so keyword matching adds noise.

## Tools and subagent

`server.py` is an MCP server named `corpus`. Claude Code (`.mcp.json`), VS Code (`.vscode/mcp.json`) and `agent.py` start it and talk to it over stdio. It loads the committed index at startup and never re-embeds the corpus.

**`search(query)` description:**
> Search the WTO legal texts: GATT 1947 (with its Annex I interpretive "Ad Article" notes), GATT 1994, GATS, TRIPS (as amended, incl. Art. 31bis), the SPS Agreement and the DSU, plus any document added with add_document. Use it for any question about what these agreements say: obligations, exceptions, definitions, time limits, dispute procedure. The corpus is the treaty text only. It has no panel or Appellate Body rulings, no tariff schedules, no other WTO agreements (e.g. Anti-Dumping, Agriculture) unless added with add_document, and no news. Search once per agreement or concept when a question spans several. Returns up to 5 passages, best first. Each has a Citation (e.g. "GATT Art. III:1-III:4", "SPS Art. 2"), the source document, a URL to the article, and the text. Cite claims with the Citation exactly as given.

**`add_document(path)` description:**
> Add one WTO legal-text web page (an .htm/.html file saved from wto.org/english/docs_e/legal_e/) to the searchable index. The file is parsed into article-level chunks with citations, embedded and stored, and becomes searchable immediately. If the same document (same file name) is already indexed with identical text, nothing is embedded and the existing chunks are kept. If it is indexed but its text has changed, the old chunks are replaced by the new ones. Returns how many chunks were added, kept and removed.

**One search result** (query q21: "How do the general exceptions for protecting human, animal, or plant life or health in GATT relate to the SPS Agreement?"):
```
[1] Citation: SPS Preamble
Source: Agreement on the Application of Sanitary and Phytosanitary Measures
URL: https://www.wto.org/english/docs_e/legal_e/sps_e.htm

[SPS Preamble] SPS > Preamble
Members,
Reaffirming that no Member should be prevented from adopting or enforcing measures necessary to
protect human, animal or plant life or health, subject to the requirement that these measures are
not applied in a manner which would constitute a means of arbitrary or unjustifiable discrimination
between Members where the same conditions prevail or a disguised restriction on international trade;
...
(results 2-5: SPS Art. 2, SPS Art. 1, SPS Annex A, SPS Art. 3)
```

**The subagent** (`.claude/agents/corpus-researcher.md`) has only one tool, `mcp__corpus__search`. Its instructions:
1. Search for the question, once per agreement or provision if it involves several (at most 4 searches).
2. Answer only with what the returned passages say.
3. Reply in at most 150 words: the direct answer first, then the supporting provisions, quoting the exact words of the key condition.
4. Cite every claim in square brackets with the citation exactly as the search shows it, and never cite anything the search did not return.
5. If the passages do not answer the question, reply "The corpus does not cover this" and say what is missing. If only part is covered, answer that part and say which part is not.

**Transcript from Claude Code:**
```
❯ Use the corpus-researcher subagent: what time limits apply to WTO panel reports?

⏺ corpus-researcher(WTO panel report time limits)

Message from @corpus-researcher

The corpus-researcher's findings on time limits for WTO panel reports, all from the DSU:

Issuing the report
- The panel's examination, "from the date that the composition and terms of reference of the panel have been agreed upon until the date the final report is issued to the parties", "shall, as a general rule, not exceed six months". In urgent cases, including perishable goods, the panel "shall aim to issue its report... within three months" [DSU Art. 12.7-12.9].
- If a panel can't meet these periods, it must tell the DSB in writing why and give an estimate. "In no case should the period from the establishment of the panel to the circulation of the report to the Members exceed nine months" [DSU Art. 12.7-12.9].
- At the complaining party's request, a panel may suspend its work for up to 12 months, and the time-frames are extended accordingly. If the suspension lasts more than 12 months, the authority for establishing the panel lapses [DSU Art. 12.10-12.12].

Adoption
- Reports "shall not be considered for adoption by the DSB until 20 days after the date they have been circulated" [DSU Art. 16].
- Objections must be circulated in writing "at least 10 days prior to the DSB meeting" [DSU Art. 16].
- "Within 60 days after the date of circulation... the report shall be adopted". The exceptions are when a party notifies an appeal or the DSB decides by consensus not to adopt it [DSU Art. 16].

Overall
- From panel establishment to the DSB's consideration for adoption, the period "shall as a general rule not exceed nine months" if the report isn't appealed. If it is appealed, the limit is 12 months. Time added under Art. 12.9 is added to these periods [DSU Art. 20].

Compliance panels
- A compliance panel "shall circulate its report within 90 days after the date of referral of the matter to it" [DSU Art. 21.4-21.6].

Agent "WTO panel report time limits" finished · 13s
```

## Adding a document

**How it works.** `add_document` imports `index.py` and uses the same functions as `main.py index`. It checks the file (it must exist, be `.htm`/`.html` and be under 5 MB), chunks it with `chunk_file()`, removes outdated chunks of the same document with `prune()`, and embeds and stores new chunks with `embed_and_store()`.

**When the document is already indexed.** Chunk IDs are hashes of the text, so an identical file produces IDs that are already stored. Nothing is embedded and the tool says so. If a file with the same name has changed, its old chunks are removed and only the new ones are embedded. This way a re-added document never creates duplicate results or uses embedding quota, and an updated text replaces the old one.

**The unanswerable question.** q29: "Under the TBT Agreement, what are the specific rules for technical regulations and conformity assessment procedures?" The TBT Agreement is not in the corpus.

**The document I added.** The TBT Agreement from wto.org (`17-tbt_e.htm`, saved in `corpus/`). It produced 35 chunks.

**Answer before** (searches, finds only SPS and GATS passages, and refuses):
```
$ uv run python main.py ask "Under the TBT Agreement, what are the specific rules for technical regulations and conformity assessment procedures?"
search 'TBT Agreement technical regulations conformity assessment procedures': ['SPS Art. 8', 'SPS Annex B, para. 5-8', 'SPS Art. 7', 'SPS Annex C, para. (g)-3', 'GATS Art. VI:1-VI:4(c)']
The corpus does not cover this; it does not contain the TBT Agreement, as the WTO agreements included in the corpus are GATT 1947, GATT 1994, GATS, TRIPS, the SPS Agreement, and the DSU.

[1 tool calls, 4143 tokens, 8.79s]
```

**Adding it** (approved with `y`):
```
$ uv run python main.py ask "Please add the document corpus/17-tbt_e.htm to the index"
The agent wants to run add_document({'path': 'corpus/17-tbt_e.htm'}). This changes the shared index. Approve? [y/N] y
[structured] 35 chunks, 0 already embedded, 35 to embed
[structured] stored 35/35
The document `corpus/17-tbt_e.htm` has been added to the index: 35 chunks were added, 0 unchanged, and 0 outdated chunks removed.

[1 tool calls, 2810 tokens, 9.59s]
```

**Answer after**:
```
search 'TBT Agreement technical regulations conformity assessment procedures': ['TBT Art. 5.2(8)-5.6(1)', 'TBT Art. 5.6(2)-5.8', 'TBT Art. 5.1-5.2(1)', 'TBT Art. 5.2(2)-5.2(7)', 'TBT Art. 6']
search 'TBT Agreement technical regulations Article 2': ['TBT Art. 2.1-2.5', 'TBT Art. 2.6-2.9(4)', 'TBT Art. 2.10-2.12', 'TBT Art. 3', 'TBT Art. 5.1-5.2(1)']
Under the WTO Agreement on Technical Barriers to Trade (TBT Agreement), specific disciplines govern the preparation, adoption, and application of both **technical regulations** and **conformity assessment procedures** by central government bodies.

---

### I. Rules for Technical Regulations (Article 2)

* **Non-Discrimination:** Imported products from any Member must be accorded treatment "no less favourable than that accorded to like products of national origin and to like products originating in any other country" [TBT Art. 2.1].
* **Avoidance of Unnecessary Obstacles:** Technical regulations shall not be prepared, adopted or applied with a view to or with the effect of creating unnecessary obstacles to international trade. Specifically, they **"shall not be more trade-restrictive than necessary to fulfil a legitimate objective, taking account of the risks non-fulfilment would create"** [TBT Art. 2.2].
  * Recognized legitimate objectives include, *inter alia*: national security requirements; the prevention of deceptive practices; protection of human health or safety, animal or plant life or health, or the environment [TBT Art. 2.2].
* **Use of International Standards:** Where technical regulations are required and relevant international standards exist or their completion is imminent, Members **"shall use them, or the relevant parts of them, as a basis for their technical regulations except when such international standards or relevant parts would be an ineffective or inappropriate means for the fulfilment of the legitimate objectives pursued"** [TBT Art. 2.4].
* **Performance-Based Requirements:** Members shall specify technical regulations based on product requirements in terms of performance rather than design or descriptive characteristics, wherever appropriate [TBT Art. 2.7].
* **Equivalence:** Members shall give positive consideration to accepting as equivalent technical regulations of other Members, even if they differ from their own, provided they are satisfied that those regulations adequately fulfil the objectives of their own regulations [TBT Art. 2.7].
* **Transparency, Notification, and Comment Procedures:** When no international standard exists or a proposed technical regulation deviates from an international standard, and it may have a significant effect on trade, Members must publish a notice at an early stage, notify other Members via the Secretariat, provide particulars or copies upon request, and allow a reasonable time for written comments [TBT Art. 2.9]. Except in urgent circumstances (such as safety, health, environmental protection, or national security), Members must also allow a reasonable interval between publication and entry into force [TBT Art. 2.10-2.12].

---

### II. Rules for Conformity Assessment Procedures (Article 5)

* **National Treatment and Non-Discrimination:** Suppliers of like products from other Members must be granted access to conformity assessment procedures under conditions "no less favourable than those accorded to suppliers of like products of national origin or originating in any other country, in a comparable situation" [TBT Art. 5.1.1].
* **No Unnecessary Obstacles:** Procedures must not be prepared, adopted, or applied with a view to or with the effect of creating unnecessary obstacles to international trade. They **"shall not be more strict or be applied more strictly than is necessary to give the importing Member adequate confidence that products conform with the applicable technical regulations or standards, taking account of the risks non-conformity would create"** [TBT Art. 5.1.2].
* **Operational and Processing Rules:** Members must ensure that:
  * Procedures are undertaken and completed as expeditiously as possible and in a no less favourable order for imported products than for domestic products [TBT Art. 5.2.1].
  * Standard processing periods are published or communicated upon request, complete documentation requirements are promptly assessed, and results are transmitted precisely without undue delay [TBT Art. 5.2.2].
  * Information requirements are limited to what is necessary to assess conformity and determine fees [TBT Art. 5.2.3].
  * Confidentiality of information is respected in the same way as for domestic products [TBT Art. 5.2.4].
  * Fees are equitable compared to those charged for like domestic products [TBT Art. 5.2.5].
  * Siting of facilities and sample selection do not cause unnecessary inconvenience [TBT Art. 5.2.6].
* **Use of International Guides/Recommendations:** Where a positive assurance of conformity is required, central government bodies shall use relevant guides or recommendations issued by international standardizing bodies as a basis for their conformity assessment procedures, except where inappropriate for reasons such as national security, health or safety, or fundamental geographical/technological factors [TBT Art. 5.4].
* **Transparency and Notification:** Similar to technical regulations, when proposed conformity assessment procedures do not conform to international guides/recommendations and may significantly affect trade, Members must publish a notice, notify other Members through the Secretariat, and allow a reasonable time for written comments [TBT Art. 5.6].
* **Recognition of Conformity Assessment (Article 6):** Members shall ensure, whenever possible, that the results of conformity assessment procedures in other Members are accepted—even if those procedures differ from their own—provided they are satisfied that those procedures offer an equivalent assurance of conformity [TBT Art. 6.1].

Sources:
  - TBT Art. 2.10-2.12: https://www.wto.org/english/docs_e/legal_e/17-tbt_e.htm#articleII
[2 tool calls, 11648 tokens, 12.94s]
```
The `search …` lines at the top of the before and after outputs are the server's log of each search the agent made and which passages it returned.

**Adding it again** (nothing is embedded):
```
[structured] 35 chunks, 35 already embedded, 0 to embed
The document `corpus/17-tbt_e.htm` is already indexed with identical text (35 chunks); nothing was embedded.
```

**What I had to change for this.**
- *The parser.* In the six original pages, an article heading is just "Article 2" and the title is on the next line. In the TBT page, both are on one line: "Article 2: Preparation, Adoption …". The parser did not recognise this as an article heading, so the first TBT chunks had no article number (`TBT, para. 1-5` instead of `TBT Art. 2.1-2.5`). I changed `index.py` to also accept "Article 2: Title" (and "Annex 1: Title"). The six original documents still produce exactly the same chunks, so nothing had to be re-embedded.
- *The citation guardrail.* It requires every answer to cite a passage. The reply to "please add this document" only reports what the tool did, so it has nothing to cite, and the guardrail made the agent answer "The corpus does not cover this" instead. A reply that only reports an approved `add_document` no longer needs a citation.

## Harness and guardrails

**The harness.** `agent.py` builds a LangChain agent on `gemini-3.5-flash-lite`, with `AGENTS.md` as the system prompt and the two MCP tools from `server.py`. Every tool call is recorded in a trace (query, retrieved citations, tokens, time), which `evaluate.py` uses.

**AGENTS.md rules** (each has its reason in the file):
1. Answer only from passages `search` returned in this conversation, never from outside knowledge.
2. Search before answering, once per agreement or concept when the question spans several (at most 4 searches).
3. Cite every claim with the citation exactly as the search gives it, in square brackets.
4. If the passages do not answer the question, start with "The corpus does not cover this" and say what is missing. If only part is covered, answer that part.
5. The corpus never contains rulings, tariff schedules, other WTO agreements or current events (unless a document was added later).
6. Quote the treaty's own words for the key condition and keep the answer short.
7. Never call `add_document` unless the user asks to add a specific file.

**Approval step.** Before `add_document` runs, the harness asks in the terminal: *"The agent wants to run add_document({'path': …}). This changes the shared index. Approve? [y/N]"*. Anything other than `y` or `yes` is a refusal. With no terminal (as in evaluation) it is refused automatically. On a refusal the tool does not run and the model is told not to retry. In the demo, a stray key press went into the first prompt, and the add was correctly refused.

The harness also limits each question to 4 tool calls and 6 model calls, so the agent cannot loop.

**Extra guardrail: citation check.** After the agent answers, code checks every `[citation]` in the answer against the passages search actually returned in that run, at article level (`GATT Art. III:2` counts as GATT Art. III). An answer that is not a refusal and has no citation also fails. If the check fails, the agent gets one retry with the list of bad citations. If the retry also fails, the answer is replaced by a refusal. I chose this because the worst failure for a lawyer is a confident answer that cites an article the system never read.

**A case where it fired: q20** ("Compare how MFN exemptions work under the GATT versus the GATS"). The first draft cited `[GATS Annex on Art. II Exemptions, para. 1]` and similar. Search had returned `GATS Annex on Art. II Exemptions`, but my citation matcher read ", para. 1" as part of the annex name, so the citations did not match. The agent rewrote them in the retrieved form and the answer was shown. In the full evaluation the guardrail fired on 2 of 43 questions (q06, q20), and both answers were fixed on retry. I then fixed the matcher.

## Evaluation

`main.py evaluate` asks the agent all 43 questions and saves answers to `eval/answers.jsonl`, verdicts to `eval/judged.csv` and totals to `eval/summary.json`. Approval is always refused, so evaluation never changes the index.

**Code checks** (no LLM):
- **Refusal:** does the answer contain "The corpus does not cover this"? Unanswerable questions must be refused and answerable ones must not. Refusals are graded by code only.
- **Valid citations:** every citation matches a retrieved passage (same rule as the guardrail).
- **Expected article cited:** at least one citation matches the expected agreement and article.
- **Expected passage retrieved:** any search returned the expected article. This separates retrieval misses from answer mistakes.

**The judge's rubric.** `gemini-3.1-flash-lite`, a different model from the agent, grades every answered question that is answerable. It sees the question, my reference answer, the retrieved passages and the answer.
- **correct = 1** if the answer reaches the same legal outcome as the reference and leaves out no essential condition, time limit or exception. A wrong number, a wrong article, the opposite conclusion or only half of a two-part question gives 0.
- **supported = 1** if every legal claim is stated in, or follows directly from, the retrieved passages. Case law, outside knowledge or a citation to the wrong passage gives 0, even if true.

**Agreement with the judge.** I graded 22 answers myself in `eval/human_labels.csv` (15 answerable, 7 unanswerable), using `grade.py`, which hides the judge's verdict.

| | Answers | Agreement |
|---|---|---|
| correct | 22 | 95.5% (21 of 22) |
| supported | 22 | 100% (22 of 22) |

The one disagreement is q06 ("Are government-provided services covered by the GATS?"). The agent said they are covered unless "supplied in the exercise of governmental authority" (GATS Art. I:3). The judge marked it correct. I marked it incorrect: the quote is right, but the answer suggests government services are normally covered, when most of them fall under that exception. The judge checked the wording, not the legal outcome.

**Results** (43 questions):

| Outcome | Count |
|---|---|
| Correct (correct and supported) | 28 of 32 answerable |
| Incorrect | 2 |
| Unsupported | 0 |
| Wrong refusals (answerable, but refused) | 2 |
| Correct refusals (unanswerable, refused) | 11 of 11 |
| Answered an unanswerable question | 0 |

Code checks: valid citations in 43 of 43 answers, correct refusal behaviour in 41 of 43, expected article cited in 29 of 32.

## Failures

`evaluate.py` suggests a cause for each failure (in `eval/judged.csv`), which I then checked by reading the answer.

| Question | Cause | What happened |
|---|---|---|
| q20 (multi): MFN exemptions, GATT vs GATS | Wrong answer from the right passage | It retrieved GATT Art. I and GATS Art. II but said the corpus did not cover the GATT side. |
| q43 (multi): can IP rights be suspended? | Wrong answer from the right passage (really a partial retrieval miss) | Both searches stayed in TRIPS. It never searched the DSU, so Art. 22.3 (suspending TRIPS obligations as retaliation) was never found. |
| q21 (multi): GATT XX(b) and SPS | Wrong refusal | It opened with "The corpus does not cover this", then answered correctly from SPS Art. 2. Code counts the phrase as a refusal. |
| q38 (single): do SPS and TBT serve the same purpose? | Wrong refusal | It correctly said the TBT is not in the corpus and described the SPS side, which is the partial answer rule 4 asks for. It missed SPS Art. 1.4. |
| q06 (single): government services under the GATS | Wrong answer from the right passage (my grade only) | Right article, wrong legal reading (see Evaluation). |

**Counts:** 3 wrong answers from the right passage (including q06), 2 wrong refusals, 0 retrieval misses, 0 unsupported claims, 0 bad test questions. Three of the five failures are multi questions.

**Patterns I would work on fixing first:**
1. **Questions that involve two agreements.** In code, check that the agent searched and cited every agreement the question names, and if not, send it back once (like the citation check). This targets q20 and q43.
2. **Partial answers counted as refusals.** Count an answer as a refusal only if it starts with "The corpus does not cover this" and has no citations. This would fix how q21 and q38 are graded.

**Smaller known issues.**
- The citation check works at article level, so a wrong paragraph number passes. In the TBT demo, the performance-based rule (Art. 2.8) was cited as Art. 2.7.
- `gemini-3.5-flash-lite` ignores the temperature setting, so the same question can give a slightly different answer each time.

## Decision
First, the facts: It answered 28 of 32 answerable questions correctly, every citation pointed to a passage it actually retrieved, and it refused all 11 unanswerable questions without making anything up. Since a made-up answer is the expensive mistake for this user, this is super important!! But q06 shows that a correct quote can still come with a wrong legal reading, and the corpus has no rulings to show how panels read the text.

**So: would I let users rely on it?** Yes, for finding and quoting the provisions that apply to a question, as a first step before the lawyer reads them. But not for interpreting a provision or predicting how a panel would rule! Although the tool is helpful, it is limited in scope and application. It doesn't take precedent into account or have very good interpretation skills, it is just a faithful repeater of what the documents say.

**Safeguards.**
1. Read the linked article before relying on an answer (every citation comes with a link to wto.org).
2. Keep the citation check on, so every cited article was actually retrieved.
3. For questions that compare two agreements, check that both are cited.
4. Treat "The corpus does not cover this" as a reason to look at case law or the missing agreement.

**Cost and latency per question** (`eval/summary.json`):

| | Mean per question |
|---|---|
| Agent tokens (input + output) | 5,097 |
| Judge tokens (evaluation only) | 1,669 |
| Time | 7.0 s |
| Tool calls | 1.12 |

On the Gemini free tier this costs nothing. The limit is quota: `gemini-3.5-flash` allows only 20 requests a day, which is why the agent uses the lite model (it was also faster: about 7 s per question against 30 to 45 s).

## AI use

I used AI to help me write the code, but made the decisions myself. We worked through the problem solving together and each part of the assignment at a time, and I wrote the report which it then helped me with tightening the wording.
