# Assignment 3 Report

- **Name**: Niccolò Pragliola
- **Student ID**: 19873
- **Group**: BBADBA 5A

## Use case

The person asking is a school-district transportation director or a county emergency manager who reads the National Weather Service alerts at 5 am and has to decide, before the first buses leave, whether to close schools, delay buses or open warming shelters. They ask things like "what does an Ice Storm Warning actually mean", "what counts as a blizzard" or "does a Moderate on the Winter Storm Severity Index mean we have to close", and they act on the answer within minutes.

A wrong answer costs much more than "I don't know". If the assistant gets a criterion wrong, buses can end up on the road in a blizzard (or a whole district closes for nothing), while "I don't know" only costs a phone call to the local NWS office or a few minutes reading the alert text. That is why every answer has to be cited and why refusing is always allowed.

## Corpus

Six official US National Weather Service documents, 70,154 words after cleaning. All are works of the US federal government, so they are in the public domain (17 U.S.C. §105) and contain no personal data once staff names and emails are removed (see Ingestion).

| Document (source id) | URL | Date | Licence | Words |
|---|---|---|---|---|
| NWS Instruction 10-513, WFO Winter Weather Products Specification (`NWSI-10-513`) | https://www.weather.gov/media/directives/010_pdfs/pd01005013curr.pdf | Nov 6, 2024 | Public domain (US gov.) | 10,828 |
| NWS Instruction 10-514, National Winter Weather Products Specification (`NWSI-10-514`) | https://www.weather.gov/media/directives/010_pdfs/pd01005014curr.pdf | Mar 18, 2025 | Public domain (US gov.) | 3,754 |
| NWS Instruction 10-515, WFO Non-Precipitation Weather Products Specification (`NWSI-10-515`) | https://www.weather.gov/media/directives/010_pdfs/pd01005015curr.pdf | May 16, 2025 | Public domain (US gov.) | 9,232 |
| NWS Instruction 10-1605, Storm Data Preparation (`NWSI-10-1605`) | https://www.weather.gov/media/directives/010_pdfs/pd01016005curr.pdf | Jul 26, 2021 | Public domain (US gov.) | 42,120 |
| Winter Storms: The Deceptive Killers, NWS/FEMA/Red Cross preparedness guide (`WinterStorms-2008`) | https://www.weather.gov/media/safety/Winter_Storms2008.pdf | Jun 2008 | Public domain (NWS publication; only the text is used, not the Red Cross photos) | 3,021 |
| The Winter Storm Severity Index: A Guide for Users, NWS Weather Prediction Center (`WSSI-Guide-2025`) | https://origin-east-www-wpc.woc.noaa.gov/wwd/wssi/WSSI_user_guide_2025.pdf | 2025 | Public domain (US gov.) | 1,199 |

I picked these documents as they're the official NWS rules behind every winter alert (what each Watch, Warning and Advisory means and when it's issued), the official definitions of each winter event and the public safety guide, which is exactly what my user needs to read an alert correctly. I kept Storm Data (10-1605) whole even though most of it covers tornadoes, floods and hurricanes, as it holds the official definitions of Blizzard, Heavy Snow, Ice Storm and Extreme Cold, and cutting it would have meant choosing which parts to keep. The non-winter sections also make retrieval harder in a realistic way, and they take the corpus over 50,000 words.

## Ingestion

`index.py` downloads the six PDFs into `corpus/` (git-ignored), extracts the text page by page with `pypdf`, cleans it, chunks it and embeds it with `gemini-embedding-2` (768 dimensions) into ChromaDB in `index/`.

- **Cleaning:** Unicode normalization, then running page headers ("NWSI 10-513 NOVEMBER 6, 2024"), page numbers, table-of-contents dot leaders, slide footers and the 2008 guide's printer slugs ("Winter_Storms.indd 3 11/13/2009") are dropped, words split by a line-end hyphen are joined, and staff names (OPR, "Certified by", the digital signature block, project lead) and all email addresses are removed so the index holds no personal data.
- **Extraction problem fixed:** in the 2008 guide the "fi" and "fl" ligatures came out as a separate character followed by a space, so "office" read "oﬁ ce" and "flash flooding" read "ﬂ ash ﬂ ooding". Neither the embeddings nor a keyword search would match these words. NFKC normalisation turns "ﬁ" into "fi" and a regex removes the stray space.
- **Known limit:** the ice-accumulation criteria in NWSI 10-513 Appendix D are an image, so their numbers are not in the text.
- **Chunking:** one chunk per numbered section. Headings such as "6.3.2 Issuance Criteria" set the section, appendices become `App-D`, and Storm Data's event types become `App-A-3` (Blizzard), `App-A-26` (Ice Storm) etc. Sections longer than 300 words are cut into 300-word parts, while sections under 30 words (a heading and one line) are merged into the next. The two documents without numbered headings are chunked by page.
- **Chunk metadata:** `source`, `title`, `section`, `sections` (all sections the chunk covers), `page`, `pages`, `words`, and a ready-made `citation` such as `NWSI-10-513, section App-B, p. 35`.
- **Number of chunks:** 407 (mean 172 words, max 300). Each vector is saved as soon as it is returned, and `main.py index` only embeds chunks whose id (a hash of their text) has no saved vector, so re-running it costs nothing.

## Test set

I chose the topics from the documents (each alert type, Watch vs Warning, the Alaska and Hawaii criteria, the Severity Index, frostbite and hypothermia, the same term in two documents, old vs new product names, and questions close to the topic that the corpus can't answer), and the questions were drafted from those topics with Claude. Every reference answer and location was checked against the document text before running anything, and nothing was tuned on the test set. There are 32 questions: 21 single (one passage), 6 multi (two passages) and 5 unanswerable.

Two examples:

1. **Multi:** "Do the winter instruction and Storm Data define a blizzard the same way?" Expected: NWSI-10-513 App-B and NWSI-10-1605 App-A-3. Reference: yes, both require sustained wind or frequent gusts of 35 mph (30 knots) or more and falling or blowing snow reducing visibility below 1/4 mile for 3 consecutive hours or longer.
2. **Unanswerable:** "How many inches of snow in 12 hours trigger a Winter Storm Warning in Memphis, Tennessee?" It sounds answerable, but 10-513 only lists criteria for Alaska and Hawaii and links to a map for the rest of the country, so the right answer is that the corpus does not cover it (this is the question I later answered by adding a document).

## Retrieval

Both designs use the same section chunks, so comparing them costs no extra embeddings:

- **A, vector:** cosine similarity between the question's embedding and each chunk's.
- **B, hybrid:** the vector ranking fused with a BM25 keyword ranking (reciprocal rank fusion), so exact terms like "Blizzard Warning" or "10-513" also count.

| Design | Hit@1 | Hit@3 | Hit@5 | Words added at k=5 |
|---|---|---|---|---|
| A, vector | 0.52 | 0.81 | 0.85 | 854 |
| B, hybrid | 0.48 | 0.63 | 0.78 | 1,048 |

Measured on the 27 answerable questions (a multi question counts as a hit only when both expected passages are in the top k). Words added to the prompt at k=1/3/5: vector 170 / 528 / 854, hybrid 219 / 610 / 1,048.

**Chosen: A, vector search** (set in `index/config.json`). Vector search wins at every k (0.85 vs 0.78 at k=5 and 0.81 vs 0.63 at k=3) while adding fewer words to the prompt (854 vs 1,048 at k=5), so it's both more accurate and cheaper. I expected hybrid to help with exact terms like "Blizzard Warning", but those words appear in so many chunks (examples, tables, Storm Data) that the keyword ranking probably pushed the right section down instead of up. I kept k=5, as going from 3 to 5 still finds the right passage for one more question (23 of 27 instead of 22) for about 330 more words.

## Tools and subagent

`server.py` exposes two MCP tools.

**search(query)**: "Search official US National Weather Service (NWS) documents on winter weather: what Winter Storm, Blizzard, Ice Storm, Winter Weather, Extreme Cold and Snow Squall watches, warnings and advisories mean and when they are issued (NWS Instructions 10-513, 10-514, 10-515), the official Storm Data event definitions (NWSI 10-1605), the Winter Storm Severity Index guide, and the NWS winter safety guide (frostbite, hypothermia, preparedness). Use it for any question about winter weather alerts, their criteria, or winter safety, and search again with other words if the first results do not answer it. Returns the 5 most relevant passages, numbered, each with a citation in the form (source, section, page). Cite these exactly; if no passage answers the question, the corpus does not cover it."

**add_document(path)**: "Add one document (a .pdf, .txt or .md file on this computer) to the winter weather corpus so that later searches can find it. The file is extracted, cleaned, chunked by section and embedded with the same pipeline as the corpus. The document is identified by its file name. If the same file was already indexed with the same content, nothing is embedded again; if a file with that name was indexed with different content, its old chunks are replaced. Returns how many chunks were added and how many were already there."

One search result (first of five) for "Blizzard Warning wind visibility criteria":

```
[1] (NWSI-10-513, section App-B, p. 35)
APPENDIX B. Winter Weather Definitions ... ● Blizzard: A blizzard means that the following
conditions are expected to prevail for a period of 3 consecutive hours or longer: o Sustained
wind or frequent gusts to 35 miles an hour or greater and o Considerable falling and/or blowing
snow, i.e., frequently reducing visibility below 1/4 mile. ...
```

The subagent (`.claude/agents/corpus-researcher.md`) may only use `mcp__corpus__search`. It searches before answering, searches again with other words when needed, cites each claim exactly as the tool shows it, starts with "The corpus does not cover this" when no passage answers, never presents a local threshold as national, and prefers the newest document when sources disagree.

Transcript from Claude Code (2.1.332) in this repository, with the `corpus` server from `.mcp.json` (full version in `eval/subagent_transcript.md`). Claude Code delegated the question to `corpus-researcher`, which ran 9 searches ("snow squall warning", "snow squall criteria visibility flash freeze", "Storm Data snow squall event definition", ...) and answered:

> A Snow Squall Warning means a short, intense burst of moderate to heavy snow with gusty winds is expected, causing sudden whiteouts [NWSI-10-513, section 7, p. 19]. Snow squalls move fast and usually last less than an hour [NWSI-10-513, section App-B, p. 36]. The local office issues it when radar, satellite or reliable reports show a squall with visibility of 1/4 mile or less in snow and sub-freezing road temperatures, or temperatures dropping fast enough to cause a flash freeze with a significant drop in visibility [NWSI-10-513, section 7.2.1, p. 19]. It is valid for only 30 to 60 minutes [NWSI-10-513, section 7.2.3, p. 19]. ... What the corpus does not cover: a Snow Squall Watch or Advisory, any stated lead time for the warning, and snow-squall advice from the winter safety guide.

## Adding a document

If the same file is added again with the same content, its chunk ids (hashes of the text) all exist already, so nothing is embedded and the tool says so. If a file with the same name but different content is added, the chunks that no longer exist are deleted and only the new ones are embedded, so the index never holds two versions of one document.

Unanswerable question q28: "How many inches of snow in 12 hours trigger a Winter Storm Warning in Memphis, Tennessee?" Document added through the agent, after approving the prompt: the NWS Memphis office's "Criteria for Winter Storm Watches/Warnings and Winter Weather Advisories" (`extra_documents/NWS-Memphis-Winter-Criteria.pdf`, https://www.weather.gov/media/meg/WinterStormCriteriaMEG.pdf, public domain, 3 chunks). Adding it a second time returned "Already indexed: NWS-Memphis-Winter-Criteria (3 chunks) has not changed, so nothing was embedded." Full run in `eval/add_document_demo.md`.

- **Before:** "The corpus does not cover the specific local snow criteria for Memphis, Tennessee. NWS local warning criteria are set by individual regional and local offices (with specific heavy snow criteria maintained online at www.weather.gov/snow-criteria) [NWSI-10-513, section App-D, pp. 41-42]."
- **After:** "For areas covered by the NWS Memphis office that fall under "elsewhere" (which includes Shelby County / Memphis), a Winter Storm Warning for heavy snow requires accumulations of 3 inches or more in 12 hours (or 4 inches or more in 24 hours) [NWS-Memphis-Winter-Criteria, p. 1]." The numbers are right, while "which includes Shelby County / Memphis" is the agent's inference, as the document only says "elsewhere".

## Harness and guardrails

`agent.py` is a LangChain `create_agent` agent on Gemini 3.5 Flash-Lite (falls back to 3.1 Flash-Lite when the main model is overloaded or out of quota, as the free tier allows only 20 requests a day on Gemini 3.5 Flash, which is kept for the judge). It starts `server.py` over MCP, uses both tools, and sends `AGENTS.md` as the system prompt.

- **AGENTS.md rules:** answer only from the search results (users act on the answer, so it has to come from the NWS documents), cite every claim with the exact citation the tool returned (so the user can check it before acting), start with "The corpus does not cover this" when the passages don't answer (a confident wrong answer costs more than a refusal), never present a local threshold as national (an Alaska number applied in Colorado would be wrong), prefer the newest document when sources disagree and say so (the 2008 guide still talks about wind chill alerts that 10-513 replaced in 2024), never make the closing decision (the WSSI guide itself says Moderate does not mean schools must close), keep answers short (users read them under time pressure) and only add documents the user asks for, with approval.
- **Approval step:** before `add_document` runs, the harness asks "The agent wants to add '<path>' to the index. Allow? [y/N]". Anything but "y", or no person at the keyboard, blocks the call and the model is told the user did not approve.
- **Call limits:** at most 4 tool calls and 6 model calls per question.
- **Extra guardrail, citation check:** every citation in the answer must be a passage the search tool returned in this run. If an answer has no citation or cites a passage that was never retrieved, the agent gets one retry with the rule restated, and if it fails again the answer is replaced by a refusal. It fired on 6 of 32 questions, every time because the answer had no citation: 3 answers were fixed by the retry (q02, q24, q32) and 3 became refusals (q07, q11, q23). Example, q02 "What triggers an Ice Storm Warning?": the first answer had no citation, and the retry produced a cited answer ([NWSI-10-513, section App-B, p. 35], [NWSI-10-1605, section App-A-26, pp. 61-62]). In an earlier run it also caught a made-up citation: the model copied the example citation from AGENTS.md ("[NWSI-10-513, section 6.3, p. 7]") although search had returned that table as "section 6.2, pp. 6-7", so I replaced the example with a placeholder ("[source, section X, p. N]").

## Evaluation

- **Code checks:** refusal or not (the answer starts with "The corpus does not cover"), every citation valid (it was retrieved in that run) and the expected source cited.
- **Code-check fix:** the first version only recognised refusals starting exactly with "The corpus does not cover this", so q28 ("The corpus does not cover the specific local snow criteria...") counted as an answer to an unanswerable question. It now accepts any answer starting with "The corpus does not cover".
- **Judge:** Gemini 3.5 Flash with the rubric in `evaluate.py`, grading `correct` and `supported` (0/1) for every non-refusal answer, with the retrieved passages as evidence.
- **Rubric choices:** the judge grades "correct" (same facts as my reference answer) and "supported" (every claim is in the retrieved passages) separately, as they're different failures with different fixes. A correct but unsupported answer is the dangerous one for my user, as it looks trustworthy while the citation doesn't back it, and a supported but wrong answer usually means retrieval found the wrong passage. Refusals are graded by code, not by the judge, as a refusal makes no claim.

| Outcome | Count |
|---|---|
| Correct | 20 |
| Wrong (from a retrieved passage) | 1 |
| Unsupported | 3 |
| Correct refusals | 4 of 5 unanswerable |
| Wrong refusals | 3 |
| Answered an unanswerable question | 1 |

Code checks: every citation in every answer was one the search returned (100% valid), and the citation guardrail fired on 6 of 32 questions. All 24 verdicts come from Gemini 3.5 Flash.

**Agreement with my grades (20 answers):** 85% on correct, 90% on supported. We disagreed on 4: q22 (the judge found "imminent or occurring" not in the passages while I accepted it), q24 (the judge marked the answer wrong because it never says "no" and leaves out the typical amounts, while I accepted it), and q23 and q30, which the code grades rather than the judge (q23 is a refusal of an answerable question, q30 answers an unanswerable one without the refusal phrase, and I graded both as fine).

## Failures

| Question | Outcome | Cause | Evidence |
|---|---|---|---|
| q07 Extreme Cold Warning | wrong refusal | retrieval miss | expected passage (NWSI-10-515 6.2.3) not in the top 5; the answer had no citation and the guardrail turned it into a refusal |
| q11 Juneau criteria | wrong refusal | wrong refusal | right passage ranked 1st, but the answer had no citation and the retry failed |
| q23 Blizzard in two documents | wrong refusal | wrong refusal | both passages retrieved, answer had no citation, retry failed |
| q24 One national snowfall amount? | wrong | retrieval miss | neither expected passage in the top 5; the agent quoted a side detail of App-D instead of answering "no" |
| q04 Winter Weather Advisory | unsupported | unsupported claim | "significant inconveniences" is not in the passages |
| q15 WSSI levels | unsupported | unsupported claim | added a note about closing decisions not in the passages |
| q22 Watch vs Warning | unsupported | unsupported claim | "imminent or occurring" is not in the retrieved passages |
| q30 School-closing snowfall | answered unanswerable | unsupported claim / bad test question | answered from the WSSI note instead of refusing |

Counts: wrong refusal 2, retrieval miss 2, unsupported claim 4 (counting q30).

I'd fix the unsupported claims first. They're the most common failure (4 of 32) and the most dangerous one, as each of these answers carried valid citations while adding words the passages don't say ("imminent or occurring", "significant inconveniences", a closing-decision note), so a user who trusts the citation would never notice. The fix is to make the guardrail check claims and not only citations (for example asking a second model whether each sentence is in the cited passage) and to tell the model in AGENTS.md not to add explanations of its own. Wrong refusals come second, as they cost a phone call rather than a wrong decision, and the two retrieval misses third (splitting the large Table 1 chunk and labelling chunks with every section they cover).

## Decision

Yes, but only for limited use. I'd let emergency managers rely on it to explain what an alert, a definition or a Severity Index level means, always with the cited passage open next to the answer, while not relying on it for local thresholds (the corpus only has Alaska, Hawaii and now Memphis) or for the closing decision itself, which stays with them. With 20 of 27 answerable questions correct, 4 of 5 unanswerable ones refused and every citation pointing to a real passage, it's useful for reading alerts faster, but 4 unsupported claims mean the citation has to be checked every time, which is the safeguard. Cost and latency per question: 4,711 input + 186 output tokens, 8.7 s and 1.2 tool calls on average (`eval/summary.json`). On the free tier this costs nothing, but the free tier only allows a few dozen questions a day per model, so real use would need a paid key (a few cents a day at this volume).

## AI use

I used Claude (Claude Code) to write the code (index, search, MCP server, agent and evaluation), run the indexing and the evaluation, draft the test questions in good English from the topics I chose and draft the report text from my decisions (the use case, vector search, what to fix first and the decision to allow limited use). I graded the 20 answers in `eval/human_labels.csv` myself before seeing the judge's verdicts. The agent and the judge use Gemini 3.5 Flash-Lite and Gemini 3.5 Flash.
