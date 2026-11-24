# Assignment 3 Report

- **Name**: Gonzalo Angulo
- **Student ID**: 18620
- **Group**: BBADBA 5B

## Use case

**Who asks.** A track-maintenance engineer at a railway infrastructure manager (an Adif-type
organisation) or at the contractor that maintains the track on its behalf. They know the track
well, but they do not know by heart the articles of the TSI Infrastructure (Regulation 1299/2014)
or of Directives 2016/797 and 2016/798.

**What they do with the answer.** They make concrete decisions with it. The most frequent one:
after a run of the track-recording car, deciding whether a measured defect exceeds the
*immediate action limit*, and so whether to impose a speed restriction or close the section.
Others: whether a renewal needs a new authorisation from the national safety authority, and what
must go into the annual safety report (due before 31 May).

**What a wrong answer costs.** Example: the assistant gives a maximum track gauge of 1 480 mm
instead of 1 470 mm, and the section stays open with a defect that required immediate action.
Directive 2016/798 itself gives the scale of the consequence: a *significant* accident starts at
EUR 150 000 of damage, a *serious* one at EUR 2 million. I assume:

- 1 % of invented answers end in an accident of about EUR 150 000 → about EUR 1 500 per answer;
- 10 % cause rework or an audit finding of about EUR 5 000 → about EUR 500 per answer.

**Expected cost of an invented answer: about EUR 2 000.**

**What "I don't know, check Article X" costs.** 15–30 minutes of the engineer's time searching
EUR-Lex or asking a colleague: **about EUR 40**. If the assistant points to the right article,
the search is short.

**The ratio.** An invented answer is about **50× worse** than a refusal (EUR 2 000 vs EUR 40):
an order of magnitude above the 13× of Assignment 2, because here the error can lead to a
derailment. I use 50× as the central value, with a sensitivity range of 20× to 100×.

What follows from it: answering only pays if the probability that the answer is wrong is below
40 / (2 000 + 40) ≈ **2 %** (between about 5 % at 20× and 1 % at 100×). The assistant should
therefore refuse whenever the retrieved passages do not clearly contain the answer. That is why
AGENTS.md makes refusal the default, and why a code guardrail replaces any answer whose
citations were not actually retrieved.

## Corpus

Four EU acts, in English, as originally published in the Official Journal, downloaded from the
Publications Office (Cellar), the machine-access service behind EUR-Lex. EUR-Lex itself blocks
scripted downloads with a bot challenge (HTTP 202 + `x-amzn-waf-action: challenge`).

| Document | doc_id | URL | Date | Licence | Words |
|---|---|---|---|---|---|
| Directive (EU) 2016/797, interoperability of the rail system (recast) | `Dir_2016_797` | https://publications.europa.eu/resource/celex/32016L0797 | 11 May 2016 | EU reuse policy (Commission Decision 2011/833/EU), source acknowledged | 29,712 |
| Directive (EU) 2016/798, railway safety (recast) | `Dir_2016_798` | https://publications.europa.eu/resource/celex/32016L0798 | 11 May 2016 | same | 24,109 |
| Commission Regulation (EU) No 1299/2014, TSI "infrastructure" (TSI INF) | `Reg_1299_2014` | https://publications.europa.eu/resource/celex/32014R1299 | 18 Nov 2014 | same | 36,402 |
| Commission Implementing Regulation (EU) 2019/779, entities in charge of maintenance (ECM) | `Reg_2019_779` | https://publications.europa.eu/resource/celex/32019R0779 | 16 May 2019 | same | 10,159 |
| **Total** | | | | | **100,382** |

All four are public legislation with no personal data. Together they cover what the engineer
decides on:

- the track parameters and their immediate action limits (TSI INF);
- authorisations and the annual safety report (the two Directives);
- vehicle maintenance duties (ECM).

**Limitation.** These are the texts as first published, not consolidated. The TSI INF in
particular has been amended since (Regulations 2019/776 and 2023/1694), so a value may have
changed. Every answer says so, and points to the consolidated text on EUR-Lex for binding
decisions.

## Ingestion

**Extract and clean.** `index.py` parses the Official Journal XHTML with BeautifulSoup and turns
each act into text blocks. Each block knows its section ("Article 14", "Annex, 4.2.4.1"), the
heading trail of that section, and its paragraph or point number when it has one. Removed:

- the Official Journal page header;
- table-of-contents rows (118 in the TSI INF), which repeat every heading and would match any
  query about one;
- footnotes that are only Official Journal references;
- signature blocks and the "Whereas: / HAS ADOPTED" formula lines.

Data tables are written one row per line as `cell | cell`, with row- and column-spanning cells
repeated on every row they cover.

**One extraction problem I fixed.** EUR-Lex lays out every list item ("(a) …", "(1) …") as a
two-cell table: the marker in one cell, the sentence in the other. Plain text extraction
returned a bare "(a)" followed by an orphaned sentence. Points lost their number, and so did the
location metadata. The parser rejoins marker and sentence (300 / 305 / 699 / 191 items in the
four acts). A second fix came with the added Spanish law (a PDF): the PDF path only recognised
English "Article N" headings, so the law was chunked by page, and the chunk with the key
infringement lost its heading. The fix teaches it "Artículo N." and drops the
"BOLETÍN OFICIAL DEL ESTADO" page header (320 lines). The full log is in
`index/extraction_problems.md`.

**Chunking: two designs**, one ChromaDB collection each:

- `fixed`: ~200-word windows with a 30-word overlap, ignoring structure (591 chunks).
- `article`: one chunk per Article or Annex section; a section over 400 words is split at
  paragraph boundaries, and every piece repeats the document title and heading trail
  (600 chunks).

**Metadata per chunk:** `doc_id`, `doc_title`, `celex`, `location` (e.g. "Article 14(3)",
"Annex, 4.2.8.6(1)-(2)"), `sections` (every section the chunk touches), `design`, `chunk_id`
(hash of the text), `word_count`, `source_url` and `doc_hash`.

**Embedding.** `gemini-embedding-2` at 768 dimensions (the default is 3072; 768 keeps `index/`
at 18 MB). Each batch of 20 is saved immediately. A rerun embeds only chunks without a stored
vector, and a daily-quota 429 stops cleanly. With 1,191 chunks against ~1,000 embeddings a day,
the index took two days. Query embeddings are cached in `index/query_cache.json`.

## Test set

I wrote 33 questions from the documents, phrased as the engineer would ask them, before any
tuning: **20 single, 8 multi, 5 unanswerable**. 18 of the 28 answerable questions draw on the
TSI INF, because that is what a track engineer consults most. This is a bias of the test set. The unanswerable questions are close to the corpus's topic on purpose:

- a limit the TSI delegates to EN 13848-5, which is not included (q31);
- an Adif-specific rule (q32);
- an inspection frequency the TSI does not set (q33);
- a ballast depth the TSI does not specify (q18);
- the Spanish fine for a missing safety report (q30).

Two examples:

- **q01 (single)**: *"Under the TSI INF, what are the immediate action limits for track gauge
  as an isolated defect on 1 435 mm track for a line speed of 140 km/h?"* →
  `Reg_1299_2014`, `Annex, 4.2.8.4`. Answer: minimum 1 427 mm, maximum 1 470 mm.
- **q31 (unanswerable)**: *"What immediate action limit for isolated longitudinal level defects
  (wavelength range D1) applies on a line running at 200 km/h?"* The TSI only refers to point
  8.3 of EN 13848-5, so the assistant must say it does not know, and must not quote a number.

## Retrieval

Hit at k means at least one expected passage is in the top k. Both designs are matched at
section level (same `doc_id`, and the expected section is in the chunk's `sections`), so they
are compared on the same terms. 28 answerable questions; the same query vector is used for both
designs.

| Design | hit@1 | hit@3 | hit@5 | multi: all passages @5 | words added @5 |
|---|---|---|---|---|---|
| fixed | 0.86 | 1.00 | 1.00 | 5 / 8 | 997 |
| **article** | **1.00** | 1.00 | 1.00 | 5 / 8 | 1,101 |

**I chose `article`.** The right section is first every time, against 86 % for fixed (q02, q03,
q05 and q29 come at rank 2 or 3). It costs about 100 more words per search. Each chunk is a
whole article with its title, so the citations the engineer receives are also cleaner.

The difference is four questions at k = 1. With 28 questions this is a small-sample decision,
and section-level matching is generous to the fixed design. Both designs miss a passage on the
same multi questions (q13 Article 2, q19 Appendix R, q28), so multi-passage recall at k = 5 is
the real retrieval weakness.

## Tools and subagent

**Tools** (`server.py`; the docstrings are the descriptions the model reads):

> **search(query)**:
>
> ```
> Search four EU railway acts and return the 5 most relevant passages with their citations.
>
> The corpus is the English text, as originally published in the Official
> Journal (later amendments are NOT included), of:
>   - Dir_2016_797: Directive (EU) 2016/797, interoperability of the rail system
>   - Dir_2016_798: Directive (EU) 2016/798, railway safety
>   - Reg_1299_2014: Regulation (EU) No 1299/2014, TSI for the infrastructure subsystem (TSI INF)
>   - Reg_2019_779: Implementing Regulation (EU) 2019/779, certification of entities in charge of maintenance (ECM)
> plus any document added later with add_document.
>
> Use it for every question about EU railway safety, interoperability, track
> and infrastructure parameters (gauge, cant, gradients, platforms, tunnels...),
> safety certificates and authorisations, national safety authorities, or
> maintenance and ECM duties. Ask in plain English with the terms the acts
> use; search again with other words if the passages do not answer the question.
>
> Returns up to 5 passages, best match first. Each has a line
> "Citation: [doc_id, location]" (for example [Dir_2016_798, Article 14(3)]),
> the document title, the source URL, a cosine similarity between 0 and 1,
> and the passage text. Cite with the Citation line copied exactly. A passage
> being returned does not mean it answers the question: read the text.
> ```

> **add_document(path)**:
>
> ```
> Add ONE new document file to the search index. It changes the index and spends embedding quota.
>
> Call it only when the user explicitly asks to add a document. `path` is a
> file on this machine (.html, .xhtml, .pdf, .txt or .md), absolute or
> relative to the project folder. The file goes through the same pipeline as
> the corpus: text extraction and cleaning, chunking, embedding, storage.
>
> If the document is already indexed:
>   - same file contents (same hash): nothing is embedded, it reports "already indexed";
>   - same document name but different contents: the old version's passages are
>     deleted and the new version is indexed in their place.
>
> Returns the doc_id to use in citations, and how many passages were added
> (embedded now), skipped (already stored) and replaced (old ones deleted).
> If the embedding quota runs out it says how many passages are still
> missing; calling it again with the same path later continues from there.
> ```

**One search result** (query *"What is the European standard nominal track gauge?"*):

```
=== Result 1 of 5 ===
Citation: [Reg_1299_2014, Annex, 4.2.4.1]
Document: Commission Regulation (EU) No 1299/2014, TSI for the 'infrastructure' subsystem (TSI INF)
Source: https://publications.europa.eu/resource/celex/32014R1299
Similarity: 0.8507
Text:
Commission Regulation (EU) No 1299/2014, TSI for the 'infrastructure' subsystem (TSI INF) | Annex > 4. DESCRIPTION OF THE INFRASTRUCTURE SUBSYSTEM > 4.2. Functional and technical specifications of subsystem > 4.2.4. Track parameters > 4.2.4.1. Nominal track gauge
(1) European standard nominal track gauge shall be 1 435 mm.
(2) Instead of point (1), for the 1 520 mm track gauge system the nominal track gauge shall be 1 520 mm.
(3) Instead of point (1), for the 1 668 mm track gauge system, the nominal track gauge shall be 1 668 mm.
(4) Instead of point (1), for the 1 600 mm track gauge system the nominal track gauge shall be 1 600 mm.
```

**Subagent** (`.claude/agents/corpus-researcher.md`). It has only `mcp__corpus__search`, and its
instructions are:

1. search with the acts' wording;
2. rephrase if the results are weak (at most about four searches);
3. answer only from the passages, with `[doc_id, location]` after every claim;
4. otherwise start with "The corpus does not cover this question.";
5. end with the original-texts / not-legal-advice note.

**Transcript from Claude Code**, for the question *"What must an entity in charge of maintenance do
before a vehicle returns to service after maintenance?"* (full text in
`eval/subagent_transcript.txt`):

```
corpus-researcher(ECM return to service duties)
Backgrounded agent (↓ to manage · ctrl+o to expand)

⏺ Waited for background work

Message from @corpus-researcher (ctrl+o to expand)

Before a vehicle returns to service, two steps must be completed: the workshop's release to service, then the ECM's return to operation notice to the user, which takes the release into account [Reg_2019_779, Article 2].

1. Release to service (maintenance delivery function)
   - This is the justified and recorded assurance that maintenance was delivered according to the maintenance orders [Reg_2019_779, Article 2].
   - The function must have procedures to check completed tasks against the orders and to issue the release notice, including all information useful to define restrictions of use [Reg_2019_779, Annex II, IV(6)-(9)].
   - It must pass on the works performed and any safety fault or defect identified [Reg_2019_779, Annex II, IV(6)-(9)].
   - For safety-related activities, it must record the works performed, the control measures required by the orders, the release to service, and calibration and verification results [Reg_2019_779, Annex II, IV(10)].
2. Return to operation (fleet maintenance management function)
   - This function manages the vehicle's removal for maintenance and its return to operation [Dir_2016_798, Article 14(3)].
   - It must have procedures to define the necessary verification measures for the maintenance delivered and the release, and to issue the return to operation notice with any restrictions of use needed for safe running [Reg_2019_779, Annex II, III(1)-(8)].
   - It must inform interested parties of the return and any restrictions relevant to users, and record the maintenance orders and the return with its restrictions [Reg_2019_779, Annex II, III(9)-(10)].
3. ECM's overall responsibility
   - The return to operation notice is the ECM's assurance that all appropriate works are complete and the vehicle can be used safely, possibly with restrictions [Reg_2019_779, Article 2].
   - The ECM must ensure its vehicles are in a safe state of running. Its maintenance system must ensure maintenance follows the maintenance file and requirements in force, and that activities are traceable [Dir_2016_798, Article 14(1)-(2)].
   - It must perform the management function itself. It may outsource the other functions, but must ensure they all comply with Annex III of the Directive [Dir_2016_798, Article 14(3)].

Not covered by the passages found: the text of Annex III to Directive 2016/798, time limits, notice templates and specific acceptance tests. They also do not spell out whether a contractor may sign the return to operation notice. Check the full acts on EUR-Lex, and the maintenance file and orders for vehicle-specific tests.

Note: based on the acts as originally published (later amendments not included). Not legal advice; for binding decisions check the consolidated text on EUR-Lex.
```

The subagent cited every claim and named what it did not find (the text of Annex III to the
Directive), instead of filling the gap.

## Adding a document

**Already indexed.** `add_document` hashes the file contents:

- same hash → "already indexed, nothing embedded";
- same `doc_id` but a different hash → the old version's chunks are deleted and the new ones
  are indexed. Chunks whose text is unchanged keep their vector, which saves quota.

I tested it on Ley 38/2015: the second call returned *"already indexed (284 chunks)"* with zero
embeddings.

**The unanswerable question: q30**, *"What fine does Spain impose on an infrastructure manager
that fails to submit its annual safety report on time?"*

**The document added:** Ley 38/2015, de 29 de septiembre, del sector ferroviario, consolidated
text from the BOE (https://www.boe.es/buscar/pdf/2015/BOE-A-2015-10440-consolidado.pdf). It is in
Spanish and adds 284 chunks. I approved it at the terminal prompt.

- **Before:** "The corpus does not cover this question." A correct refusal.
- **After:** *"Failing to submit the annual report within the established deadlines is
  classified as a minor infringement (infracción leve) … Minor infringements carry a fine of up
  to €7,500"*, citing `[BOE_A_2015_10440_consolidado, Artículo 108 (part 3/3)]` and
  `Artículo 109 (part 2/4)`.

**The "after" answer is wrong.** Not submitting the safety report is a *serious* infringement
(Artículo 107.Uno, point 1.15), fined EUR 7,501 – 38,000 (Artículo 109.1(b)). The "informe anual"
in Artículo 108 is the dangerous-goods report. The chunk with point 1.15 ranked 24th, 7th and
13th in the agent's three searches, so it was never in a top 5. The citation guardrail could not
stop the answer, because both citations were genuinely retrieved. Details are in
`eval/add_document_demo.md`. This is the most important result of the evaluation: adding a
document turned a correct refusal into a confident, cited, wrong answer.

## Harness and guardrails

**AGENTS.md** (the system prompt) has six rules, each with its reason:

1. Answer only from search results (general knowledge of safety rules may be wrong or
   outdated).
2. Cite every claim as `[doc_id, location]` (the engineer must be able to check the article).
3. If the results do not cover the question, say "The corpus does not cover this question." and
   never guess (a wrong answer costs ~50× a refusal).
4. Say that answers are based on the texts as originally published (a corpus limitation).
5. Never call `add_document` unless the user explicitly asks (it changes the index).
6. Not legal advice; check the consolidated text for binding decisions.

**Approval.** `agent.py` intercepts every `add_document` call and asks
`Allow it? [y/N]` on the terminal. With no terminal (for example during evaluation) it denies
automatically.

**Call limit.** At most 6 tool calls per question (LangChain `ToolCallLimitMiddleware`). It never
fired in the evaluation: 51 searches for 33 questions.

**My extra guardrail: citation check.** After the answer, code checks that every
`[doc_id, location]` it cites was returned by a search in the same run. If one was not, the
answer is replaced with a refusal.

- **v1 required an exact match.** It fired on 6 of 33 answers, and every time the model had
  cited a sub-paragraph of a retrieved section (`Article 12(2)` when the chunk is labelled
  `Article 12`). Five of these were answerable questions (q12, q17, q24, q26, q28), so the
  guardrail itself caused 5 wrong refusals.
- **v2 accepts the same document and section** after dropping paragraph references. I
  re-applied it offline to the saved drafts, without new model calls. A forged citation
  (`Article 99(4)`) still fires, as the unit test shows. Its limitation is that it can accept a
  paragraph outside the retrieved range.

| | v1 exact | v2 same section |
|---|---|---|
| Guardrail fired | 6 | 0 |
| Wrong refusals | 5 | 0 |
| Correct refusals | 3 | 3 |
| Answered an unanswerable question | 2 | 2 |

## Evaluation

**Code checks** (`evaluate.py`, stage 3):

- every citation is among the passages retrieved in that run;
- refusal is detected by the fixed sentence of AGENTS.md rule 3;
- unanswerable + refused = correct refusal; answerable + refused = wrong refusal;
- whether the expected source was cited.

**Judge** (stage 4): `gemini-3.6-flash`, the same model that answers, with the question, the
reference answer, the retrieved passages and the answer. My rubric is **strict**:

- `correct = 1` only if every key fact and number of the reference is present and none is
  wrong; a partial answer is 0;
- for an unanswerable question, 1 only if it declines without inventing values;
- `supported = 1` only if every claim is in the retrieved passages; naming a law or authority
  that is not in the passages counts as unsupported, even as a "where to look" pointer.

**Agreement with my blind grades** (33 answers, graded before the judge ran): **79 % on correct**
(26 / 33) and **94 % on supported** (31 / 33).

- In 6 of the 7 `correct` disagreements the judge was stricter than me (q08, q13, q17, q24,
  q28, q31). It flagged omitted details that I had accepted. My grades were more lenient than my
  own rubric.
- In the opposite case (q23), I caught a substantive error the judge missed. The answer presents
  the investigation of a serious accident as discretionary, when Article 20 makes it mandatory.

**Results** (article design, guardrail v2, judge verdicts):

| | Count |
|---|---|
| Correct | 27 / 33 (82 %); 23 / 28 answerable |
| Unsupported | 4 / 33 (12 %) |
| Correct refusals | 3 / 5 by code (q30, q32, q33); 4 / 5 by the judge, which also accepts q18 |
| Wrong refusals | 0 / 28 |
| Answered an unanswerable question (code) | 2 / 5 (q18, q31): neither invents a value, but neither uses the refusal sentence |

## Failures

Each answer flagged by the judge, the code or me, classified by me:

| Cause | Count | Questions |
|---|---|---|
| Bad test question (the reference asks for more than the question) | 4 | q08, q17, q24, q28 |
| Wrong answer from the right passage | 2 | q13 (omits adapting the elements together), q23 (mandatory investigation presented as optional) |
| Unsupported claim | 2 | q30, q32 (refuse correctly, but name Ley 38/2015, AESF or Adif rules from the model's own knowledge) |
| Retrieval miss | 1 | q30 after adding Ley 38/2015 (a confident wrong answer) |
| Wrong refusal | 0 (v2); 5 under guardrail v1 | q12, q17, q24, q26, q28 under v1 |
| No failure on review | 2 | q31, q33 (decline in substance; "national rules" and the NSA are in the corpus) |

q28 is also a partial retrieval miss: Article 8 of Regulation 2019/779 was not in its top 5.

**What to fix first:**

1. **Retrieval over added documents.** The one expensive failure is q30-after: a near-duplicate
   passage outranked the right one, and the citation check cannot catch that. Next steps: hybrid
   (keyword + vector) search, a larger k for documents in another language, and a check that a
   sanction answer cites the article that *classifies* the infringement.
2. **The reference answers.** Four of the judge's failures come from references that ask for
   more than the question does. With a strict judge, the references must be trimmed to the
   question before the scores mean anything.
3. **Refusal detection.** q18 and q31 decline in substance but not with the fixed sentence, so
   code and judge disagree. Either the agent should always use the sentence, or the check should
   recognise a substantive refusal.

## Decision

**Would I let users rely on it? Yes, as a lookup aid only.** Engineers can use it to find the
right article and value fast, but they must **open the cited article and confirm the value
before any safety decision** (a speed restriction, closing a section). In the interface, every
citation would be a link to the source.

- **Why not more.** The threshold from the use case is a wrong-answer rate under ~2 %. On the
  answerable questions the judge marks 5 of 28 not correct; 4 of those are test-question
  problems, which leaves 2 real content errors (q13, q23), about 7 %. And adding one document
  produced a confident wrong answer. That is well above 2 %, so the answer cannot be the
  decision.
- **Why not less.** The safeguard costs 1–2 minutes per question, far below the EUR 40 of an
  unaided search. Retrieval puts the right article first in 100 % of answerable questions. Zero
  wrong refusals and zero fabricated citations got through.
- **Not for:** sanction amounts or national law added later (see q30), nor anything after the
  original publication dates.

**Cost and latency per question** (33 questions, article design): **9,750 input + 1,127 output
tokens**. At gemini-3.6-flash's standard price of $1.50 / $7.50 per million tokens, that is about
**$0.023 per question**, or about half that at the introductory price of $0.75 / $3.75 that runs
until 31 Dec 2026. The judge adds about 3,000 input + 700 output tokens per question.
**Latency is 20.6 s on average**: 10.1 s on the paid tier, 53.6 s on the free tier. Search
itself takes under 2 s; the rest is model time. The free tier allows only 20 model calls a day
for this model, so I enabled billing to finish the run.

## AI use

I used Claude (Anthropic): Claude Code wrote the code in `index.py`, `server.py`, `agent.py`,
`evaluate.py` and the tests, and Claude in chat helped me plan, explained the results, and drafted
this report in English from my notes and numbers. The following are mine:

- the use case and its costs (EUR 2 000 vs EUR 40, 50×) and the choice of corpus;
- the two designs to compare and the choice of `article` from the numbers;
- the duplicate-document policy and the citation guardrail, including relaxing it to v2;
- the strict judge rubric, including counting outside laws as unsupported;
- the 33 test questions, written by me from the documents;
- my 33 blind grades;
- the failure classification and the decision.


