# Assignment 3 Report

- **Name**: Niccolò Pragliola
- **Student ID**: 19873
- **Group**: BBADBA 5A

## Use case

✍️ *Your words: who asks (school-district / county emergency manager reading NWS winter alerts before dawn), what they do with the answer (close schools, delay buses, open warming shelters), and why a wrong answer costs more than "I don't know" (buses in a blizzard vs. a call to the local NWS office).*

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

✍️ *One or two sentences: why these documents fit the use case, and why Storm Data (10-1605) is kept whole even though most of it covers non-winter events (tornadoes, floods, hurricanes).*

## Ingestion

`index.py` downloads the six PDFs into `corpus/` (git-ignored), extracts the text page by page with `pypdf`, cleans it, chunks it and embeds it with `gemini-embedding-2` (768 dimensions) into ChromaDB in `index/`.

- **Cleaning:** Unicode normalisation; running page headers ("NWSI 10-513 NOVEMBER 6, 2024"), page numbers, table-of-contents dot leaders, slide footers and the 2008 guide's printer slugs ("Winter_Storms.indd 3 11/13/2009") are dropped; words split by a line-end hyphen are joined; staff names (OPR, "Certified by", the digital signature block, project lead) and all email addresses are removed so the index holds no personal data.
- **Extraction problem fixed:** in the 2008 guide the "fi" and "fl" ligatures came out as a separate character followed by a space, so "office" read "oﬁ ce" and "flash flooding" read "ﬂ ash ﬂ ooding". Neither the embeddings nor a keyword search would match these words. NFKC normalisation turns "ﬁ" into "fi" and a regex removes the stray space.
- **Known limit:** the ice-accumulation criteria in NWSI 10-513 Appendix D are an image, so their numbers are not in the text.
- **Chunking:** one chunk per numbered section. Headings such as "6.3.2 Issuance Criteria" set the section, appendices become `App-D`, and Storm Data's event types become `App-A-3` (Blizzard), `App-A-26` (Ice Storm) etc. Sections longer than 300 words are cut into 300-word parts; sections under 30 words (a heading and one line) are merged into the next. The two documents without numbered headings are chunked by page.
- **Chunk metadata:** `source`, `title`, `section`, `sections` (all sections the chunk covers), `page`, `pages`, `words`, and a ready-made `citation` such as `NWSI-10-513, section App-B, p. 35`.
- **Number of chunks:** 407 (mean 172 words, max 300). Each vector is saved as soon as it is returned, and `main.py index` only embeds chunks whose id (a hash of their text) has no saved vector, so re-running it costs nothing.

## Test set

✍️ *How you wrote it, counts by kind (single / multi / unanswerable), two examples.*

## Retrieval

*(Filled in from `eval/summary.json` after `main.py evaluate`.)* Both designs use the same section chunks, so comparing them costs no extra embeddings:

- **A, vector:** cosine similarity between the question's embedding and each chunk's.
- **B, hybrid:** the vector ranking fused with a BM25 keyword ranking (reciprocal rank fusion), so exact terms like "Blizzard Warning" or "10-513" also count.

| Design | Hit@1 | Hit@3 | Hit@5 | Words added at k=5 |
|---|---|---|---|---|
| A, vector | 0.52 | 0.81 | 0.85 | 854 |
| B, hybrid | 0.48 | 0.63 | 0.78 | 1,048 |

Measured on the 27 answerable questions (a multi question counts as a hit only when both expected passages are in the top k). Words added to the prompt at k=1/3/5: vector 170 / 528 / 854, hybrid 219 / 610 / 1,048.

**Chosen: A, vector search** (set in `index/config.json`). ✍️ *Why, by the numbers.*

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

Transcript from Claude Code (2.1.332) in this repository, with the `corpus` server from `.mcp.json`; full version in `eval/subagent_transcript.md`. Claude Code delegated the question to `corpus-researcher`, which ran 9 searches ("snow squall warning", "snow squall criteria visibility flash freeze", "Storm Data snow squall event definition", ...) and answered:

> A Snow Squall Warning means a short, intense burst of moderate to heavy snow with gusty winds is expected, causing sudden whiteouts [NWSI-10-513, section 7, p. 19]. Snow squalls move fast and usually last less than an hour [NWSI-10-513, section App-B, p. 36]. The local office issues it when radar, satellite or reliable reports show a squall with visibility of 1/4 mile or less in snow and sub-freezing road temperatures, or temperatures dropping fast enough to cause a flash freeze with a significant drop in visibility [NWSI-10-513, section 7.2.1, p. 19]. It is valid for only 30 to 60 minutes [NWSI-10-513, section 7.2.3, p. 19]. ... What the corpus does not cover: a Snow Squall Watch or Advisory, any stated lead time for the warning, and snow-squall advice from the winter safety guide.

## Adding a document

If the same file is added again with the same content, its chunk ids (hashes of the text) all exist already, so nothing is embedded and the tool says so. If a file with the same name but different content is added, the chunks that no longer exist are deleted and only the new ones are embedded, so the index never holds two versions of one document.

Unanswerable question q28: "How many inches of snow in 12 hours trigger a Winter Storm Warning in Memphis, Tennessee?" Document added through the agent, after approving the prompt: the NWS Memphis office's "Criteria for Winter Storm Watches/Warnings and Winter Weather Advisories" (`extra_documents/NWS-Memphis-Winter-Criteria.pdf`, https://www.weather.gov/media/meg/WinterStormCriteriaMEG.pdf, public domain, 3 chunks). Adding it a second time returned "Already indexed: NWS-Memphis-Winter-Criteria (3 chunks) has not changed, so nothing was embedded." Full run in `eval/add_document_demo.md`.

- **Before:** "The corpus does not cover the specific local snow criteria for Memphis, Tennessee. NWS local warning criteria are set by individual regional and local offices (with specific heavy snow criteria maintained online at www.weather.gov/snow-criteria) [NWSI-10-513, section App-D, pp. 41-42]."
- **After:** "For areas covered by the NWS Memphis office that fall under "elsewhere" (which includes Shelby County / Memphis), a Winter Storm Warning for heavy snow requires accumulations of 3 inches or more in 12 hours (or 4 inches or more in 24 hours) [NWS-Memphis-Winter-Criteria, p. 1]." The numbers are right; "which includes Shelby County / Memphis" is the agent's inference, as the document only says "elsewhere".

## Harness and guardrails

`agent.py` is a LangChain `create_agent` agent on Gemini 3.5 Flash-Lite (falls back to 3.1 Flash-Lite when the main model is overloaded or out of quota; the free tier allows only 20 requests a day on Gemini 3.5 Flash, which is kept for the judge). It starts `server.py` over MCP, uses both tools, and sends `AGENTS.md` as the system prompt.

- **AGENTS.md rules:** ✍️ *summarise your rules and their reasons.*
- **Approval step:** before `add_document` runs, the harness asks "The agent wants to add '<path>' to the index. Allow? [y/N]". Anything but "y", or no person at the keyboard, blocks the call and the model is told the user did not approve.
- **Call limits:** at most 4 tool calls and 6 model calls per question.
- **Extra guardrail, citation check:** every citation in the answer must be a passage the search tool returned in this run. If an answer has no citation or cites a passage that was never retrieved, the agent gets one retry with the rule restated; if it fails again the answer is replaced by a refusal. It fired on 6 of 32 questions, every time because the answer had no citation: 3 answers were fixed by the retry (q02, q24, q32) and 3 became refusals (q07, q11, q23). Example, q02 "What triggers an Ice Storm Warning?": the first answer had no citation, and the retry produced a cited answer ([NWSI-10-513, section App-B, p. 35], [NWSI-10-1605, section App-A-26, pp. 61-62]). In an earlier run it also caught a made-up citation: the model copied the example citation from AGENTS.md ("[NWSI-10-513, section 6.3, p. 7]") although search had returned that table as "section 6.2, pp. 6-7", so I replaced the example with a placeholder ("[source, section X, p. N]").

## Evaluation

*(Filled in after `main.py evaluate`.)*

- **Code checks:** refusal or not (the answer starts with "The corpus does not cover this"); every citation valid (it was retrieved in that run); the expected source cited.
- **Code-check fix:** the first version only recognised refusals starting exactly with "The corpus does not cover this", so q28 ("The corpus does not cover the specific local snow criteria...") counted as an answer to an unanswerable question. It now accepts any answer starting with "The corpus does not cover".
- **Judge:** Gemini 3.5 Flash with the rubric in `evaluate.py`, grading `correct` and `supported` (0/1) for every non-refusal answer, with the retrieved passages as evidence.
- ✍️ *Your rubric choices and your agreement with the judge.*

| Outcome | Count |
|---|---|
| Correct | |
| Wrong (from a retrieved passage) | |
| Unsupported | |
| Correct refusals | |
| Wrong refusals | |
| Answered an unanswerable question | |

## Failures

✍️ *Failed questions by cause (retrieval miss, wrong answer from the right passage, unsupported claim, wrong refusal, bad test question), counts, what to fix first.*

## Decision

✍️ *Would you let users rely on it, for what, with which safeguard?* Cost and latency per question: 4,711 input + 186 output tokens, 8.7 s and 1.2 tool calls on average (`eval/summary.json`); on the free tier this costs nothing, but the free tier only allows a few dozen questions a day per model.

## AI use

✍️
