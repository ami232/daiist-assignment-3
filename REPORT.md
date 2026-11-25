# Assignment 3 Report

- Name: Clementine Mathieu
- Student ID: 19311
- Group: [BBADBA 5A]

## Use case

Who asks, what they do with the answer, and what a wrong answer costs compared with "I don't know".

Who asks: Small food business owners and managers who need quick answers about food safety but do not have a specialist in their staff. They ask practical questions about cooking temperatures, food cooling, sick employees or HACCP requirements. The answers are spread across more than 1,200 pages of FDA guidance, making them difficult to find.

What they do with the answer: They use it immediately to make decisions, such as whether food is safe to serve, whether an employee can work or what rules to include in a HACCP plan. Every answer must include a section and page reference so it can be checked.

What a wrong answer costs: A wrong answer can cause food poisoning or a serious illness. It can also lead to failed inspections and legal problems. Giving no answer is much safer than giving incorrect advice, as the user can check the official guidelines or contact the health department. Therefore, the system should only answer when the sources clearly support it.

## Corpus

Table: document, URL, date, licence, words.

| Document | URL | Date | Licence | Pages | Words |
|---|---|---|---|---|---|
| FDA Food Code 2026 | [fda.gov/media/194741/download](https://www.fda.gov/media/194741/download) | September 2026 | Public domain (US government work) | 732 | 262,535 |
| Managing Food Safety: A Manual for the Voluntary Use of HACCP Principles for Operators of Food Service and Retail Establishments | [fda.gov/media/71976/download](https://www.fda.gov/media/71976/download) | April 2006 | Public domain (US government work) | 86 | 21,701 |
| Managing Food Safety: A Regulator's Manual for Applying HACCP Principles to Risk-based Retail and Food Service Inspections | [fda.gov/media/72067/download](https://www.fda.gov/media/72067/download) | April 2006 | Public domain (US government work) | 85 | 22,357 |
| Total | | | | 903 | 306,593 |

## Ingestion

How you extract, clean and chunk; one extraction problem you fixed; chunk metadata; number of chunks.

Extract. `index.py` downloads the three PDFs from fda.gov into `corpus/` and extracts the text of each page with pypdf. Each page is handled separately so that every line keeps its page number.

Clean.
- Remove the running header ("FDA Food Code 2026  Chapter 3. Food") and the page number at the top of each page. The header gives the part name, which is kept as metadata.
- Skip the parts of the Food Code that only add noise: the table of contents, the index, Annex 2 (references), the Summary of Changes and the list of previous editions. In the HACCP manuals, skip the cover, the table of contents and the Paperwork Reduction Act annex. Table-of-contents lines with dot leaders are also removed.
- Fix degree signs that pypdf reads as the letter "o": "68oC (155oF)" becomes "68°C (155°F)".
- Remove the asterisks the Food Code puts on defined terms and lowercase them ("*FOOD" becomes "food"), keeping acronyms such as HACCP and USDA in capitals.
- Remove the small P and Pf priority markers at the end of clauses.
- Join section numbers and words broken at the end of a line ("3-" + "401.13").
- Remove lines of blanks (`________`) from the fill-in forms in Food Code Annex 7 and the manuals, and replace bullet symbols that pypdf reads as an unreadable private-use character with "•".

Chunk. Chunks follow the structure of the documents. In the Food Code, each section starts a new chunk, while in the manuals, each chapter, annex or capital-letter heading does. Short sections from the same part are merged until they reach around 350 words. Longer sections are split at the end of a sentence after 350 words, or at a line after 455 words if needed. Any remaining text under 40 words is added to the previous chunk. This reduced the number of very short chunks (under 40 words) from 253 to 12.

I chose 350 words as a balance between keeping sections together and staying within the free daily embedding limit of about 1,000 texts. It produces 790 chunks, compared with 891 at 300 words and 705 at 400 words. This allows the full index to be embedded in one day.

Extraction problem I fixed: words split in two. pypdf sometimes inserts spaces inside words, especially in the HACCP manuals (e.g. "restri cting" instead of "restricting"). This makes searches less accurate. I fixed this by joining neighbouring words when their combined form appears at least twice in the document and the second word is not valid on its own. Earlier versions were too aggressive, incorrectly joining phrases like "a symptomatic employee" into "asymptomatic employee", which changes the meaning. The final rule made 130 repairs (40 in the Food Code and 48 and 42 in the manuals). I checked every repair manually and found no incorrect joins.

Chunk metadata. Each chunk stores where it comes from, so the agent can cite it:

```json
{
  "id": "food-code-2026:9ff161007882",
  "doc_id": "food-code-2026",
  "title": "FDA Food Code 2026",
  "part": "Chapter 3. Food",
  "section": "3-401.11 Raw Animal Foods",
  "page_start": 91,
  "page_end": 92,
  "page_label": "63",
  "words": 393,
  "text": "[FDA Food Code 2026 > Chapter 3. Food > 3-401.11 Raw Animal Foods]\n3-401.11 Raw Animal Foods. (A) Except as specified ..."
}
```

`page_start` and `page_end` are PDF pages, and `page_label` is the number printed on the page. The text starts with the document, part and section, so the embedding also captures where the passage comes from. The id is a hash of the text. If the chunking changes, only the changed chunks need new embeddings.

Number of chunks. 790 chunks and 249,610 words: 648 from the Food Code, 72 from the operators' manual and 70 from the regulators' manual. The median chunk is 354 words and the longest is 474.

Embedding. Each chunk is embedded with `gemini-embedding-2` at 768 dimensions and stored in ChromaDB (`index/chroma/`, cosine distance) with its text and metadata. This model does not accept a `task_type`, so the task is written into the text, as Google's documentation recommends: `title: … | text: …` for chunks and `task: search result | query: …` for questions. Each text is sent as its own `Content` object. A plain list of strings would come back as one combined vector.

Problem I faced: the per-minute rate limit. Each batch of 20 vectors is saved as soon as Gemini returns it, and chunks already stored are skipped, so a crash or a quota error loses nothing. On the first run, requests started failing with 429 after about 100 chunks. The limit was not the daily quota but a per-minute limit on tokens (embed_content_free_tier_tokens). The script now sends at most 90 texts a minute and, on a 429, waits as long as Gemini's retryDelay asks before retrying. It stops cleanly if the daily quota is used up, and the next run continues from there. The second run embedded the remaining 690 chunks. Since the limit counts tokens, a cap on words per minute would match it better than a cap on texts.

## Test set

How you wrote it, counts by kind, two examples.

`eval/questions.csv` has 36 questions: 22 single, 7 multi and 7 unanswerable. They were written before any tuning of retrieval. Each answerable question started from a rule in the documents. I read the passage and wrote the question the way a restaurant manager would ask it, not in the code's words: "hamburger patties", not "comminuted meat"; "looks yellow", not "jaundiced". The reference answer copies the numbers and conditions from the passage. The questions cover the topics in the use case like cooking, cooling, or sick employeesfor example.

- Matching. expected_location gives the section and PDF pages, e.g. § 3-501.14 Cooling, PDF pages 98-99. A retrieved chunk is a hit if it comes from the same document and its pages overlap that range. Multi questions list both passages, separated by ;.
- Multi questions need two rules, usually two steps of one food flow (cook then hold, cool then reheat, freeze then keep records). q29 crosses documents.
- Unanswerable questions are on topic and were checked with a text search over all chunks. Two (onset of Staphylococcus aureus and Bacillus cereus illness) are answered by the Bad Bug Book, which I added later. The others sit next to real rules: grease-trap pumping, training hours, pay during exclusion, ceiling height, EU law.

Two examples:

| id | kind | question | expected location | reference answer |
|---|---|---|---|---|
| q10 | single | One of my cooks looks yellow and says it started three days ago. Can he keep working? | § 2-201.12 Exclusions and Restrictions, PDF pages 59-60 | No: exclude a food employee who is jaundiced with onset within the last 7 calendar days, unless a health practitioner documents that it is not caused by hepatitis A or another fecal-orally transmitted infection. |
| q28 | multi | We want to serve salmon sashimi. How must the fish be frozen, and what records do we keep? | § 3-402.11 Parasite Destruction, PDF page 95; § 3-402.12 Records Creation and Retention, PDF page 96 | Freeze at -20°C (-4°F) or below for 168 hours (7 days), or at -35°C (-31°F) until solid and stored at -35°C for 15 hours, or solid at -35°C then stored at -20°C for 24 hours. Record freezing temperature and time and keep records 90 calendar days beyond service (or a supplier's written statement). |

## Retrieval

Hit rate at 1/3/5 per design, words added to the prompt, the design you chose.

`evaluate.py` measures retrieval on the 29 answerable questions. A question is a hit at k if at least one expected passage is in the top k. For the 7 multi questions, I also report how often both passages are in the top 5. All designs search the same 790 chunks. Changing chunk size would have cost a full re-embedding (705 to 891 texts), close to the free daily quota of about 1,000, so I compared search methods on the same chunks instead. Question vectors are cached in `eval/query_vectors.json`, so a re-run costs no embeddings.

| Design | hit@1 | hit@3 | hit@5 | multi: both passages @5 | words in top 5 |
|---|---|---|---|---|---|
| Dense (Gemini embeddings, cosine) | 59% | 90% | 97% | 57% | 1,662 |
| BM25 (keyword) | 14% | 38% | 48% | 29% | 1,792 |
| Hybrid (dense + BM25, reciprocal rank fusion) | 34% | 69% | 72% | 43% | 1,780 |
| Dense, rules first (Annex 3 pushed down) | 72% | 97% | 97% | 71% | 1,631 |

Keyword search fails on how users talk. BM25 missed 15 of 29 questions at k = 5. Users write "hamburger patties", "looks yellow" and "the cold well"; the code writes "comminuted", "jaundiced" and "cold holding". Adding BM25 to dense search made it worse (72% against 97%). With 790 chunks and conversational questions, the keyword ranking mostly adds noise to the fusion.

Annex 3 pushes the rules out of first place. Dense search almost always found the right passage in the top 5, but put it first only 59% of the time. In half of the 12 misses at first place, the top result was the Food Code's Annex 3 ("Public Health Reasons"). Annex 3 explains why each rule exists and repeats its heading, so it looks very similar to a question about the rule, but it often leaves out the number the user needs. It is also large: 290 of the Food Code's 648 chunks. (The other 6 misses were the HACCP manual's version of the rule (3), Annex 4 on HACCP (2) and Annex 7's cooking chart (1).)

The fix: a small handicap for Annex 3. The "rules first" design takes the 30 closest chunks, lowers the score of each Annex 3 chunk by 0.05, and sorts again. If an Annex 3 chunk matches much better, it still comes first. That matters for the few questions only Annex 3 answers. I tried handicaps from 0.01 to 0.05, and also removing Annex 3 completely. A handicap of 0.05 gave the same results as removing it (72% / 97% / 97%, and 71% for both passages), while keeping Annex 3 searchable.

Chosen design: dense, rules first, k = 5. It puts the right passage in the top 3 for 97% of the questions, and puts the rule itself in first place more often than plain dense search. That matters because the agent mostly cites what it reads first. The live server (server.py) uses exactly the same search function that evaluate.py tests (index.ranked_search). Returning 5 passages adds about 1,630 words to the prompt per search.
Only one question, q29, misses at k = 5. It needs the definition of "critical limit" from a HACCP manual's glossary. The search returns the Food Code's Annex 4 instead, which explains critical limits at much greater length and so looks like a better match.

## Tools and subagent

Your tools' descriptions, one search result, the subagent's instructions, one transcript from your editor.

`server.py` is an MCP server with two tools. At startup it opens the saved ChromaDB index and does not embed anything. Only the question is embedded when `search` is called.

`search(query, k=5)`. The query is embedded with the `task: search result | query: …` prefix, and the k closest chunks (5 by default, at most 10) are returned by cosine similarity. Its description, which is what the model reads:

> Search US FDA food-safety guidance for retail and food service: the FDA Food Code 2026 (cooking, cooling, hot and cold holding, date marking, employee health and exclusion, handwashing, allergens, equipment, plumbing, facilities, inspections) and FDA's two HACCP manuals for operators and regulators (hazard analysis, critical control points, critical limits, monitoring, risk control plans), plus any document added later with add_document.
>
> Use it for every factual question about food-safety rules or HACCP, and phrase the query the way the rule would be written (e.g. "cooling cooked food time and temperature limits"). Search again with different words if the first results do not answer the question.
>
> Returns the k most similar passages (default 5, at most 10), best first. Each starts with a numbered citation line: document | part | section | PDF page (printed page), and a relevance score from 0 to 1. Cite those lines in the answer. If no passage states the answer, say the corpus does not cover it.

The description lists the topics the corpus covers, so the model knows when to use the tool. It says how to phrase a query, and it asks the model to cite the location lines and to say when the corpus does not answer the question. That last instruction matters for this use case, where a wrong answer costs more than "I don't know".

`add_document(path)`. Its description:

> Add a PDF to the searchable food-safety corpus: extracts, cleans and chunks it with the same pipeline as the corpus, embeds the chunks with Gemini and stores them, so search finds them from then on.
>
> `path` is the PDF's file path, absolute or relative to the project folder. If the same file is already indexed, nothing is done and no embeddings are spent. If a different version of a document with the same file name is indexed, its old chunks are replaced. Embedding uses the daily Gemini quota (about one text per 350 words of PDF); if it runs out, the chunks embedded so far are kept and calling again later finishes the job.
>
> Returns what happened: the document id, title and number of chunks stored.

The tool imports `chunk_file` and `embed_and_store` from `index.py`, so an added document goes through exactly the same extraction, cleaning, chunking and embedding as the corpus.

One search result. Query: "What temperature do I cook hamburger patties to?" (k = 3). The rule that answers it came second, shortened:

[2] FDA Food Code 2026 | Chapter 3. Food | 3-401.11 Raw Animal Foods | PDF pages 91-92 (printed page 63) (score 0.70)
3-401.11 Raw Animal Foods. (A) ... raw animal foods such as eggs, fish, meat, poultry ... shall be
cooked to heat all parts of the food to a temperature and for a time that complies with one of the
following methods ... (2) 68°C (155°F) for 17 seconds or the temperature specified in the following
chart ... for ratites, and nonintact MEATS; the following if they are comminuted: fish and game animals ...

The three results:
- The HACCP operators' manual (score 0.72): a general passage on cooking. It mentions hamburgers and gives "155°F for 15 seconds" for ground beef.
- The Food Code rule, § 3-401.11 (score 0.70): 68°C (155°F) for 17 seconds for comminuted (ground) meat. This is the rule that answers the question.
- Annex 3 on the same section (score 0.75): it explains why 155°F is enough.

The Annex 3 passage had the highest similarity but came last, because the rules-first ranking takes 0.05 off Annex 3 scores (0.75 − 0.05 = 0.70). The example also shows why citations matter. The 2006 manual says 15 seconds and the 2026 Food Code says 17, so the answer has to cite the Food Code rule.

Subagent. `.claude/agents/corpus-researcher.md` defines a Claude Code subagent whose only tool is `mcp__corpus__search`. It cannot add documents, read files or browse the web, so everything it says has to come from the corpus. Its description tells the main agent when to delegate: "any question about cooking, cooling, holding or reheating temperatures and times, date marking, employee illness and exclusion, handwashing, allergens, equipment, facilities, inspections, or HACCP plans". Its instructions are the same rules as `AGENTS.md`, shortened:
1. Search before every answer, phrasing the query like the rule.
2. Search again with other words, up to 3 searches, and once for each part of a two-part question.
3. Answer only from returned passages.
4. Cite every claim with the location line as the tool printed it.
5. Say "The corpus does not cover this." rather than guess, and name the part that is missing.
6. Keep numbers, °C and °F, times and exceptions.

The reply format is Answer: plus Sources:.

Transcript from the editor. The question is not in the test set. I asked the subagent to also list its search queries.

> Main agent → corpus-researcher: A deli supervisor asks: "We just started selling a house-made peanut sauce. Do we have to tell customers which major food allergens are in unpackaged food we serve, and does my staff need any allergen training?"
>
> Searches (3): `notification of consumers major food allergens unpackaged food written notification` · `person in charge demonstration of knowledge food allergy awareness employees trained` · `definition major food allergen milk egg fish crustacean shellfish tree nuts wheat peanuts soybeans sesame`
>
> corpus-researcher: Answer: Yes to both, and peanut sauce is covered. Under the Food Code, peanuts are a "major food allergen" (FDA Food Code 2026, § 1-201.10 Statement of Application and Listing of Terms, PDF pages 38-39 (printed page 10)). "The permit holder shall notify consumers by written notification of the presence of major food allergens as an ingredient in unpackaged food items that are served or sold to the consumer" (FDA Food Code 2026, § 3-602.12 Other Forms of Information, PDF pages 109-111 (printed page 81)). The written notice can take many forms, physical or electronic, "including, but not limited to, brochures, deli case or menu notifications, label statements, table tents, placards, or other effective written means" (FDA Food Code 2026, Annex 3, § 3-602.12 Other Forms of Information, PDF pages 494-495). On training, the person in charge must make sure "employees are properly trained in food safety, including food allergy awareness, as it relates to their assigned duties." Food allergy awareness "includes describing foods identified as major food allergens and the symptoms that a major food allergen could cause in a sensitive individual who has an allergic reaction" (FDA Food Code 2026, § 2-103.11 Person in Charge ¶ (O), PDF pages 55-56 (printed page 27)). For an allergen training program, the guidance suggests (but does not require) topics such as identifying the major food allergens, recognizing the symptoms of an allergic reaction and how to respond, and "principles of allergen cross-contact prevention" (FDA Food Code 2026, Annex 3, § 2-103.11 Person in Charge, PDF pages 362-363).
>
> Note: the FDA Food Code is a model code. Each state or county adopts it with its own changes, so check with your local regulatory authority which version and wording apply to you.
>
> Sources: five citation lines, from § 1-201.10, § 3-602.12, § 2-103.11 and the matching Annex 3 sections.

## Adding a document

What happens when a document is already indexed. The unanswerable question, the document you added, the answer before and after.

When a document is already indexed. `index/documents.json` records every indexed document with the SHA-256 hash of its file. `add_document` hashes the new file before doing anything else:
- Same file already indexed: nothing is changed and no embeddings are spent, even if the file has a different name. Tested by adding my local copy of the Food Code, which has a different path from the one in `corpus/`: "Already indexed: fda-food-code-2026.pdf is the same file as 'FDA Food Code 2026' (id food-code-2026, 648 chunks). Nothing was changed."
- New version of a known document (same file name, different content): its old chunks are deleted and the new version is indexed, so search never returns two conflicting versions of the same rule. For food-safety rules this matters, because an older edition can give a different temperature or time.
- New document: it is chunked, embedded and registered.

Preparing the document to add. The document I will add is the Bad Bug Book. A dry run of `chunk_file` on it, with no embedding, produced 0 chunks. Its pages have no "Chapter 1 – …" headings like the manuals, so the pipeline treated the whole book as a cover page and skipped it. The tool would have reported success while indexing nothing. In the Bad Bug Book, each chapter starts with the pathogen's name followed by numbered headings ("1. Organism", "2. Disease", … "9. Other Resources"). I added a rule for documents without Chapter/Annex headings: a "1." heading starts a new chapter, named by the line before it. The Bad Bug Book now gives 384 chunks across 58 pathogen chapters, for example `Bad Bug Book > Salmonella species > 2. Disease`. The rule only applies to documents without Chapter/Annex headings, so none of the corpus chunks changed.

The unanswerable question, before and after. Question q30: "How long after eating food contaminated with Staphylococcus aureus toxin do symptoms usually start?" The Food Code mentions S. aureus several times (infected wounds on hands, heat-stable toxins), but never says when symptoms start.

Before (evaluation run, search `Staphylococcus aureus toxin symptoms onset time duration`):

> The corpus does not cover this.

Adding it (called from Claude Code, which asked me to approve the `add_document` call first):

```
Added 'Bad Bug Book' (id bad-bug-book-2nd-edition-pdf): 292 pages, 384 chunks, 384 newly embedded. It is now searchable.
```

The index now holds 1,174 chunks (28 MB). The evaluation stays comparable: `evaluate.py` filters retrieval to the three corpus documents, and the agent's answers were recorded before the document was added.

After (`main.py ask`, same question, 1 search, 4.5 s):

> The onset of symptoms after eating food contaminated with Staphylococcus aureus enterotoxin usually ranges from 1 to 7 hours, with a mean of 2 to 4 hours (Bad Bug Book | Staphylococcus aureus | 2. Illness, PDF page 88; Bad Bug Book | Phytohaemagglutinin (kidney bean lectin) | Appendix 5, PDF page 267). This onset time depends on individual susceptibility to the toxin, the amount of toxin ingested, and general health (Bad Bug Book | Staphylococcus aureus | 2. Illness, PDF page 88).

Both facts are in the retrieved chunks: page 88 says symptoms start "usually … rapid (1 to 7 hours)", and the Appendix 5 table on page 267 gives "1‐7 h, mean 2‐4 h". The second citation shows a chunking flaw. The appendices have no "1." heading, so they were labelled as part of the last chapter before them (Phytohaemagglutinin). The page is still right. The fix is to start a new part at each "Appendix N." line.

## Harness and guardrails

Your AGENTS.md rules, the approval step, and your extra guardrail with one case where it fired.

`agent.py` is a LangChain `create_agent` on Gemini (`gemini-3.5-flash-lite`, which answers in about 5 to 20 s; `gemini-3.5-flash` took about 50 s per call on the free tier). It runs `server.py` over MCP and records every tool call in a trace, which the guardrail and the evaluation use.

AGENTS.md rules. `AGENTS.md` is the system prompt, and each rule gives its reason in the file:
1. Search before every answer, phrasing the query like the rule, up to 3 searches.
2. Answer only from the search results.
3. Cite every claim with the location as the tool printed it.
4. Say "The corpus does not cover this." instead of guessing.
5. Keep exact numbers, °C and °F, times and exceptions.
6. Say the Food Code is a model code, on its own line, without a citation.
7. No medical advice: say what the business must do (exclude, restrict, report).
8. Call `add_document` only when the user explicitly asks.

Rule 6 changed after a test. The agent had cited § 3-501.14 for "the Food Code is a model code", which that section does not say.

Approval step and limits. `HumanInTheLoopMiddleware` pauses before `add_document` and asks "Allow it? [y/N]". Only "y" lets it run, and with no one at the keyboard the call is rejected. Tested with no terminal: the call was rejected and the index still held 790 chunks. At most 4 tool calls and 8 model calls are allowed per question, so a looping agent cannot use up the free quota.

Extra guardrail: citation check. After the agent answers, code checks two things. Every citation must match a passage the search returned in this run (same page, and same § if one is given). An answer with no citation must be a refusal. If the check fails, the agent gets one rewrite; if it fails again, the answer becomes a refusal. Blocking a correct answer is better here than passing a claim the user cannot check. I tested it on made-up answers against a result for § 3-501.14, PDF page 98. The right citation passed; a wrong page, a wrong section and a missing citation were blocked.

Where it fired. It fired on 6 of 36 evaluation questions. In q23 (chili cooled and reheated), the first answer cited "HACCP Manual for Operators, PDF page 37", a page no search had returned. The rewrite cited only retrieved pages and passed. The check also has a cost. In q12 the agent cited the right rule by its printed page ("printed page 52"), the check rejected it twice, and a correct answer became a refusal. The check now also accepts printed pages (see Failures). An early false alarm, on the agent's reply to a rejected `add_document`, was fixed by skipping replies where no search was made and approval was requested.

## Evaluation

Code checks, the judge's rubric, your agreement with the judge, and results: correct, unsupported, correct refusals, wrong refusals.

`main.py evaluate` runs the agent (the same `agent.ask` as `main.py ask`) on all 36 questions, with `add_document` always rejected, and caches each answer in `eval/answers.jsonl`. As in session 10's `07-own-harness/evaluate.py`, what code can check is checked in code, and the rest goes to a judge.

Code checks (all 36 answers, no model):

| Check | Result |
|---|---|
| Every citation matches a passage the search returned | 36/36 |
| An expected passage was among the search results (answerable) | 29/29 |
| The answer cites an expected passage (answerable) | 25/29 |
| Unanswerable questions refused, fully or partly | 7/7 |
| Answerable questions refused | 1/29 (q12) |
| Citation guardrail fired | 6/36 |

A refusal counts if the answer says "the corpus does not cover / specify / state…". This also catches partial refusals such as q33 and q35, where the agent named what was missing and cited the nearest rule, as rule 4 asks. Of the 4 answers that did not cite an expected passage, one is the q12 refusal. The other 3 (q18, q21, q29) cited an equivalent passage, e.g. the Food Code's Annex 4 for the seven HACCP principles instead of the operators' manual.

LLM judge. `gemini-3.6-flash`, a stronger model than the agent's, so the agent does not grade itself. It sees the question, the reference answer, the agent's answer and all the retrieved text, and returns a structured verdict, reasoning first:
- correct: gives the reference's key facts (numbers, units, times, main conditions) and nothing that contradicts it. For an unanswerable question: says the corpus does not cover it, without supplying the fact from elsewhere.
- supported: every factual claim is in the retrieved text (the model-code note is not checked).

Its free quota is 20 requests a day, so judging took two days. `evaluate.py` saves each verdict and stops cleanly when the quota runs out.

Results:

| | Judge | My grades |
|---|---|---|
| Answerable, correct and supported | 28 / 29 | 27 / 29 |
| Answerable, incorrect | 0 | 0 |
| Answerable, unsupported claim | 0 | 1 (q15) |
| Wrong refusals | 1 / 29 | 1 / 29 (q12) |
| Unanswerable, correct refusals | 7 / 7 | 7 / 7 |
| Unanswerable, answered anyway | 0 | 0 |

Agreement with my grades. I graded all 36 answers in `eval/human_labels.csv` before reading the judge's verdicts.

| Criterion | Agreement | Cohen's kappa | Disagreements |
|---|---|---|---|
| correct | 36/36 (100%) | 1.0 | none |
| supported | 35/36 (97%) | 0.0 | q15 |

The kappa of 0.0 on supported does not mean the judge is random. It rated all 36 answers supported, so chance alone predicts 97% agreement, and kappa cannot measure anything.

The one disagreement is a real miss by the judge. For q15, the agent wrote that milk may be received at the temperature in its law, "such as Grade A milk standards". The retrieved rule, § 3-202.11 ¶ (B), only says "laws governing milk and molluscan shellfish". The numbers are right, so the answer is correct, but "Grade A" came from the model's own knowledge. The judge checked the numbers and missed the added detail. It is reliable for correctness here, but not on its own for support.

## Failures

Failed questions by cause, with counts, and what to fix first.

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 0 | |
| Wrong answer from the right passage | 0 | |
| Unsupported claim | 1 | q15 (found by my grading; the judge missed it) |
| Wrong refusal | 1 | q12 |
| Bad test question | 0 | |

q12 (wrong refusal, caused by my own guardrail). "Can my staff make salads with their bare hands if they washed them?" The search found the right rule, § 3-301.11, but the agent cited it by its printed page ("printed page 52") instead of the PDF page. The citation check only compared PDF pages, so it rejected the answer twice and replaced it with a refusal. This is the safe direction (the user loses minutes, not safety), but it is still a failure.

Fixed first: the check now also accepts a printed page that matches a retrieved passage. On q12's recorded results, the printed-page citation passes, while wrong pages, wrong sections and missing citations are still blocked. The evaluation numbers are from before the fix.

q15 (unsupported claim). The agent added "such as Grade A milk standards" to a correct, cited answer; the retrieved rule only says "laws governing milk". The citation guardrail cannot catch this, because it checks that the cited page was retrieved, not that the page says what the sentence claims. The judge missed it too. To fix next: a check that compares each cited sentence with its passage, plus human spot checks.

Weak spots that did not cause a failure:
- Multi questions depend on searching twice. One search put both passages in the top 5 for only 71% of multi questions, and the agent searched more than once on only 4 of 36 questions.
- Definitions. q29 is the only retrieval miss at k = 5: the manual's glossary definition of "critical limit" loses to the Food Code's longer Annex 4 explanation. The agent answered correctly from those other passages.
- Latency. Median 8 s, but 5 of 36 answers took 115–160 s because of free-tier queuing and the guardrail's retry.

Also to fix: start a new part at "Appendix N." headings in the Bad Bug Book, and add multi questions whose two parts use different words.

## Decision

Would you let users rely on it, for what, with which safeguard? Cost and latency per question.

Yes, as a lookup tool that shows where the rule is, not as the final authority. On 36 questions it gave no incorrect answers, refused all 7 it could not answer, and every citation pointed to a passage it really retrieved, which the guardrail checks in code. Its two failures were a wrong refusal (q12), the safe direction, and one unsupported detail in a correct answer (q15). A restaurant manager can use it to find the right rule and its numbers quickly, then check the cited page.

Limits and safeguards:
- Small sample. 0 wrong answers out of 29 still allows an error rate of several percent. The user should read the cited rule before acting on a number.
- A valid citation does not prove the sentence (q15). A check that compares each sentence with its passage is the next safeguard to build.
- Model code. The answer must keep saying local rules can differ. The corpus has nothing on EU law, pay or building dimensions.
- No diagnosis. Bad Bug Book answers about symptoms must stay information, not medical advice (rule 7).
- Keep the citation guardrail and the approval for `add_document`, which changes every later answer and cost 384 of about 1,000 free daily embeddings.

Cost and latency per question (mean of 36 runs): 7,010 input and 299 output tokens and 1.14 searches, mostly the system prompt plus about 1,600 words of passages per search. That is free within the free-tier limits. Latency is 8 s median but 131 s at the 90th percentile because of free-tier queuing: fine for checking a rule, but daily use would need a paid tier.

## AI use

What you used and how, or "none".

I used Claude Code (Claude Opus 5.5) in VS Code as a coding assistant. For the test set and evaluation stage, it:
- helped draft test questions and reference answers from the corpus, which I then checked;
- helped confirm that the unanswerable questions are not covered by the corpus;
- helped write the evaluation code, following the structure used in class;
- ran comparisons that informed design choices such as the ranking;
- helped find and fix bugs;
- helped draft parts of this report from the evaluation results;
- helped review cases where my grades and the judge's disagreed.

I graded the answers in `eval/human_labels.csv` myself, before reading the judge's verdicts. Gemini is used at run time: `gemini-embedding-2` for the embeddings, `gemini-3.5-flash-lite` for the agent and `gemini-3.6-flash` as the judge.
