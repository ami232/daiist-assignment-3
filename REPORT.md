# Assignment 3 Report

- **Name**: Juan Carlos Chavarria
- **Student ID**: 19313
- **Group**: BBADBA 5B

## Use case

A kitchen manager or food business owner asks practical food safety questions ("What temperature must cooked chicken reach?", "How fast must cooked food be cooled?") and acts on the answer right away. A wrong answer can cause foodborne illness or a failed inspection, and many answers hinge on exact numbers (temperatures, times), so a subtly wrong figure is dangerous. A refusal ("the documents don't say, check with your local health authority") only costs the user a short delay, so the assistant must cite the exact rule and refuse when the corpus does not cover the question.

## Corpus

| Document | URL | Accessed | Licence | Words used |
|---|---|---|---|---|
| FDA Food Code 2022, Chapter 2 (Management and Personnel) and Chapter 3 (Food) | https://www.fda.gov/food/fda-food-code/food-code-2022 | 2026-11-19 | US federal government work, public domain | 21,057 |
| FDA Bad Bug Book, 2nd ed. (2012), bacterial pathogens (pp. 11-110) | https://www.fda.gov/food/foodborne-pathogens/bad-bug-book-second-edition | 2026-11-19 | US federal government work, public domain | 39,405 |
| USDA FSIS Safe Minimum Internal Temperature Chart | https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart | 2026-11-19 | US federal government work, public domain | 733 |
| **Total** | | | | **61,195** |

Word counts are raw PDF extraction, before cleaning. The rest of the Food Code (chapters 1 and 4-8, annexes) and the Bad Bug Book's parasite, virus and toxin sections were deliberately excluded, to stay within the free embedding limit and to give the test set questions the corpus cannot answer. No personal data is present.

## Ingestion
Text is extracted page by page with pypdf from selected parts of three PDFs (Food Code chapters 2-3, Bad Bug Book bacteria sections, the FSIS chart). Cleaning removes lines that repeat across many pages (running headers, footers, page numbers; numbers are normalised to "#" so "page 12" and "page 13" match), which works for any PDF, including ones added later. Cleaning dropped about 4% of the words (61,195 to 58,962). The Food Code's "Pf/P" priority markers are kept on purpose because they carry meaning for inspections.

Every chunk carries its document, a location (Food Code section number such as §3-401.11, Bad Bug Book organism name, or the chart's name) and the PDF page.

One extraction problem fixed: my first rule for detecting Bad Bug Book organism titles only found 12 of 24 organisms, because on the other pages the title and "For Consumers: A Snapshot" share one line, and wrapped titles (e.g. "Enteropathogenic Escherichia / coli (EPEC)") were cut. Chunks would have been cited under the wrong organism without any error. I found it by printing the metadata, and fixed it by reading the title from the top of the page and joining wrapped lines.

Two designs are indexed: A (fixed 150-word chunks, 408 chunks) and B (structure-based, new chunk at each section, at most 250 words, tiny leftovers merged, 307 chunks). Vectors (gemini-embedding-2, 3,072 numbers each) are stored in ChromaDB under index/ (19 MB), with a chunk id derived from the text so that re-running never embeds the same chunk twice.

Known limitation: the FSIS chart was saved from a web page, so its chunks also contain some website text (menu, "official website" banner, a recall alert). The temperatures are intact, but this is noise I did not clean.

## Test set

30 questions in eval/questions.csv: 15 single (one passage), 7 multi (two passages), 8 unanswerable. Phrased the way a kitchen manager would ask.

How they were written: I drafted the questions with an AI assistant (Claude), based on what the Food Code and the Bad Bug Book contain, and then checked every one against the indexed text with a script before using it. For each answerable question the script confirmed that the expected section exists in the index and that the key words or numbers of the reference answer appear in it (for multi questions, in both sections). For each unanswerable question it confirmed that the topic's key words appear nowhere in the indexed text (venison, Trichinella, aflatoxin, Cryptosporidium, footcandles, permit fees, sink compartments, dish machine rinse). The questions were written before any retrieval or agent run and were not changed afterwards. The unanswerable ones are close to the corpus topic on purpose: most are about parts of the source documents that I left out (equipment, facilities, permits, parasites, toxins).

Examples:
- q04 (single): "How quickly must cooked food be cooled from 135°F to 70°F?" Expected: FDA Food Code 2022, §3-501.14. Reference: within 2 hours (and down to 41°F within a total of 6 hours).
- q18 (unanswerable): "What is the safe minimum internal temperature for venison?" Expected: refusal. The corpus has the FSIS chart but no venison row, and the Food Code rule for commercially raised game animals is a different category.

Limits: 30 questions is small, so one question moves a rate by about 3 points. My expected locations come from design B's section labels, which favours B in the retrieval comparison. The AI-drafted questions may share the vocabulary of the documents more than real users would.

## Retrieval

Hit rate means: the expected section is among the top k retrieved chunks (for "multi" questions, both sections must be). Measured on the 22 answerable questions (15 single, 7 multi); the 8 unanswerable ones are evaluated later.

| Design | k | Hit rate single | Hit rate multi | Hit rate all | Avg words added to prompt |
|---|---|---|---|---|---|
| A: fixed 150 words (408 chunks) | 1 | 67% | 0% | 45% | 146 |
| A | 3 | 87% | 14% | 64% | 438 |
| A | 5 | 87% | 14% | 64% | 731 |
| B: by section, max 250 words (307 chunks) | 1 | 93% | 0% | 64% | 233 |
| B | 3 | 100% | 29% | 77% | 616 |
| B | 5 | 100% | 43% | 82% | 997 |

Chosen: design B with k=5. B is better at every k, and it finds the right section for every single-passage question from k=3. Going from k=3 to k=5 raises the overall hit rate from 77% to 82% (one more multi question) at the cost of about 380 more words in the prompt. In this use case a missing passage is worse than a longer prompt.

All 4 misses of design B at k=5 are multi-passage questions where one topic fills the whole top 5 (e.g. q12: five Shigella chunks, none from the handwashing rule §2-301.12). A possible fix, to be checked in the end-to-end evaluation, is for the agent to search once per part of the question.

Caveats: only 22 questions, so one question moves a rate by about 4 points. Design A labels each chunk with the section where it starts, so some of its misses may be labelling effects, and my expected locations come from design B's section labels, which favours B somewhat.

## Tools and subagent

**Tools** (server.py, MCP server "corpus", stdio):
- `search(query)`: embeds the query with Gemini (1 embedding) and returns the 5 closest passages from the index (design B). Each passage has a header with source, location, PDF page and relevance. Its description tells the model what the collection contains, when to use the tool, to search once per part of a two-part question, and that if no passage answers the question the collection does not cover it.
- `add_document(path)`: runs a .pdf/.txt/.md file through the same functions as index.py (extract, clean, chunk, embed, store). Its description states the quota cost, the already-indexed behaviour and the 300-chunk limit.

One search result (query "What temperature must chicken reach?", header lines only):

[1] source: USDA FSIS Safe Temperature Chart | location: Safe Minimum Internal Temperature Chart | page: 1 | relevance: 0.75
[3] source: FDA Food Code 2022 | location: §3-401.11 | page: 84 | relevance: 0.72
[4] source: FDA Food Code 2022 | location: §3-401.12 | page: 87 | relevance: 0.71

**Subagent** (.claude/agents/corpus-researcher.md): its tools line allows only the search tool, so it cannot call add_document. Its instructions: always search first and use no other source; search once per part of a question; a high relevance score only means a similar topic, so read the passage; answer in one or two sentences with exact numbers; cite every claim as [source | location | p.page]; if the collection does not cover the question, begin with "I don't know based on the documents".

**Transcript** (VS Code Copilot chat, custom agent corpus-researcher, model chosen by Copilot Fusion: GPT-6 Luna; 2 search calls approved, 4 steps, 16 s):

> **Question:** How fast must cooked food be cooled from 135°F to 70°F, and which bacterium is known for growing when food cools too slowly?
>
> **Answer:** Cooked food must cool from 135°F to 70°F within 2 hours. [FDA Food Code 2022 | §3-501.14 | p.92] Clostridium perfringens can multiply rapidly when cooked food is left at room temperature. [FDA Bad Bug Book (2nd ed.) | Clostridium perfringens | p.82]

Observations: both claims are correct and cited in the required format. The answer omits the second half of the cooling rule (down to 41°F within 6 hours in total). My first attempt failed: the chat answered that the search tool was not available, because the tools line used Claude Code's name (mcp__corpus__search) and Copilot did not recognise it. Changing it to corpus/search fixed it. In that failed attempt the agent refused instead of answering from memory, as its rules require.

## Adding a document
**When the document is already indexed.** The file name identifies the document and every chunk has an id (a fingerprint of its text). add_document first chunks the file, then compares its chunk ids with the ones stored under that file name. Same ids: nothing is embedded and the tool answers "Already indexed ... Nothing was embedded." Changed content: the chunks of the old version are deleted and the new ones are embedded, so the index never holds two versions of one file. Files that would make more than 300 chunks are refused before anything is embedded, to protect the free daily quota. Test: adding extra_docs/fsis_holiday_meats.pdf twice gave "Indexed fsis_holiday_meats.pdf: 16 chunks (16 newly embedded)" and then "Already indexed: ... is unchanged (16 chunks). Nothing was embedded."

**Unanswerable question and the added document.** Question q18: "What is the safe minimum internal temperature for venison?"
- Before, with the search tool: the top 5 results came from the FSIS temperature chart and Food Code §3-201.17 and §3-401.11; the word "venison" appears in none of them (top relevance 0.76).
- Document added: USDA FSIS, "Roasting Those 'Other' Holiday Meats" (US federal government work, public domain; https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/meat/roasting-those-other-holiday-meats), saved as PDF on 2026-11-24, 16 chunks. Its roasting chart (page 9) lists "Venison, round, rump, loin, or rib roast; 3 to 4 pounds, 20-25 min/lb, 160 degrees F"; it is a roasting-times chart, not a statement labelled "safe minimum internal temperature".
- After, with the same search: 4 of the 5 results come from the new document, "venison" appears in the results (top relevance 0.78).
- Agent answer before and after (agent.py, gemini-3.5-flash-lite):
  - **Before:** "What is the safe minimum internal temperature for venison?" -> "I don't know based on the documents." (1 search). The corpus had no venison figure, so this is the correct answer.
  - **Adding the document:** I asked the agent to add extra_docs/fsis_holiday_meats.pdf and approved the prompt (see the approval test in the Harness section): 16 chunks embedded, Design B grew from 307 to 323 chunks.
  - **After, same question:** still refused ("the documents cover poultry, red meat and whole game birds, but not venison"), although page 9 was among the retrieved passages. That page has the venison roast line (160 degrees F) inside a roasting-times chart, not a statement labelled "safe minimum internal temperature", so the agent followed rule 5 and refused. I checked the index directly: the 16 new chunks are stored and 7 of the top 8 search results for the question come from the new document.
  - **After, question in the chart's own words:** "At what internal temperature should a venison roast be cooked, according to the roasting chart?" The agent drafted the correct answer, "A venison round, rump, loin, or rib roast should be cooked to an internal temperature of 160 degrees F [fsis_holiday_meats.pdf | location: page 9 | p.9]". The citation check withheld it because the model wrote the label as "location: page 9" (the same false alarm as q11, see Failures); the draft is shown in the run log.
  - **Conclusion:** adding the document did make venison answerable, but the agent only answered it when the question was phrased close to the document's wording, and the final answer was blocked by my own checker. I report both results as they happened. Afterwards I removed the venison chunks again, so the submitted index (307 chunks in Design B) is the one the evaluation used and q18 stays unanswerable.

## Harness and guardrails

**AGENTS.md rules** (agent.py sends the file as the system prompt; each rule has its reason written next to it in the file):
1. Search first and answer only from the search results (the documents are the only source the user can check).
2. Cite every claim as [source | location | p.page], copied from the result header (so a person and the code can check it).
3. Copy numbers, units, conditions and rest times exactly (a subtly wrong number is the most dangerous mistake here).
4. If the corpus does not cover the question, reply "I don't know based on the documents" plus one sentence about what the documents cover, with no numbers or citations (a refusal is cheap, a number from a nearby case is not).
5. The thing asked about must be in the passage; a rule for a neighbouring category is not an answer (added after a failure, see below).
6. Search once per part of a two-part question. 7. Short answers. 8. No medical advice. 9. Add documents only when the user asks.

**Approval step.** add_document is wrapped in agent.py: before the tool runs, the agent shows the file path and waits for y/N in the terminal. If there is no terminal to ask (as in the evaluation) the answer is no and the tool is not called. Test: I asked the agent "Please add this file to the collection: extra_docs/fsis_holiday_meats.pdf". It called add_document and the code stopped it with a prompt ("Allow? [y/N]"). I answered n: nothing was embedded and the index did not change; the agent replied that it had not added the file. (The citation check then replaced that reply with the refusal wording, a false alarm because the reply contains no factual claim.) I ran the same request again and answered y: 16 new chunks were embedded and saved.

**Extra guardrails, in code and not in the prompt.**
- Citation check: every [source | location | p.N] in an answer must match a passage that a search really returned in this run; otherwise the answer is replaced by a refusal that says it was withheld.
- Refusal trim: if an answer starts with the refusal phrase, only the first paragraph (at most 2 sentences) is kept, and if it still has digits or a citation it becomes the plain refusal.
- Limits: at most 8 tool calls per question, recursion limit 30, 25 s timeout per model call.
- Model fallback: if a model returns 503/404/429/timeout the next one is tried, and a failed model is skipped for 90 s. This was needed because several Gemini models were overloaded during the project.

**One case where a guardrail fired.** Question q18 (venison). The model's draft was: "I don't know based on the documents. The provided documents cover cooking temperatures for commercially raised game animals, exotic animals like deer under a voluntary USDA inspection program, and wild game animals [FDA Food Code 2022 | §3-401.11 / §3-201.17 | p.68, 83-84]." The refusal trim replaced it with "I don't know based on the documents." The draft also merged two sections into one citation that matches no passage.

**A case the guardrails did not catch.** In an earlier run of the same question the answer was "Commercially raised or USDA-inspected game animals such as deer (venison) are cooked to 145°F ... [FDA Food Code 2022 | §3-401.11 | p.83]". The citation is real, so the citation check passed, but the passage never mentions deer or venison (checked in the index: "deer", "venison" and "elk" are absent; "game animals" and "wild" are present). That is an unsupported claim. I tightened rule 5, and the next two runs refused. The citation check verifies that the source exists, not that the sentence is supported by it; the LLM judge's "supported" grade is what measures that.

## Evaluation

**Code checks** (evaluate.py, no model involved): whether the answer is a refusal (starts with "I don't know based on the documents"); whether every citation [source | location | p.N] matches a passage that a search really returned in that run; whether the expected section was retrieved and cited. Refusals are decided by code: a refusal is correct exactly on the 8 unanswerable questions.

**LLM judge** (a Gemini Flash model, temperature 0, one call per answer that is not a refusal, given the question, the reference answer, the answer and all retrieved passages). Rubric, each 1 or 0:
- correct: same key facts as the reference answer; every key number, unit and condition matches; extra correct detail is fine; 0 if a key fact is wrong or missing.
- supported: every factual claim is stated in the retrieved passages; 0 if any claim goes beyond them (a rule for another category, general knowledge).
The judge answers in JSON with a one-sentence reason. Judge verdicts are saved in eval/judge_verdicts.jsonl.

**Human labels.** I graded all 30 answers myself in eval/human_labels.csv (correct and supported, notes for every 0) from eval/answers_for_grading.md, before seeing the judge's verdicts. Agreement with the final verdicts (code for refusals, judge for the rest): correct 29/30 (97%), supported 28/30 (93%), both 27/30 (90%). The three disagreements are all cases where I was stricter than the judge:
- q04: I gave 0 because the answer omits the required 6-hour total cooling time; the judge gave 1.
- q08: I gave supported 0 because the answer adds "contact a doctor", which no passage states (it comes from rule 8 of AGENTS.md); the judge gave 1.
- q10: I gave supported 0 because the passages shown on my sheet did not state 160°F; the judge saw all retrieved passages, so part of this is a difference in evidence, not in opinion.

**Results** (30 questions, the agent is gemini-3.5-flash-lite; add_document disabled during evaluation):

| Kind | n | Refused | Correct | Supported | Valid citations |
|---|---|---|---|---|---|
| single | 15 | 2 | 13 | 15 | 15 |
| multi | 7 | 1 | 5 | 7 | 7 |
| unanswerable | 8 | 8 | 8 | 8 | 8 |

- Answerable questions (22): 18 correct and supported (82%), 3 wrong refusals, 0 answered with unsupported claims, 1 answered wrong.
- Unanswerable questions (8): 8 correct refusals, 0 made-up answers.
- Guardrails fired: citation check 3 times (all 3 were false alarms, see Failures), refusal trim 1 time.
- Without the 3 false alarms the answerable result would have been 21 of 22 (95%); I report 82% because it is what the system really produced.

Limits: 30 questions, so one question moves a rate by about 3 points. The agent's model ignores the temperature setting, so answers are not repeatable (the venison question was answered wrongly in one earlier run and refused in the evaluation run). The judge is a model from the same vendor as the agent.
## Failures

Failed questions by cause (4 of 22 answerable questions; none of the 8 unanswerable ones failed):

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 0 | The expected section was retrieved for all 22 answerable questions |
| Wrong answer from the right passage | 1 | q13 |
| Unsupported claim | 0 | None in the final answers (one earlier venison run had one, see Harness) |
| Wrong refusal | 3 | q09, q11, q28 |
| Bad test question | 0 | None found; see below |

**The 3 wrong refusals were caused by my own citation guardrail, not by the model.** In all three the model's draft was correct and cited a retrieved page, but my string matching rejected the format:
- q09 wrote one citation with two pages ("p.103, p.106"), and my pattern accepts one page number.
- q11 copied the word "location:" into the citation.
- q28 added a "§" before the organism name.
The guardrail blocks fabricated citations, but it also withheld three good answers. Without these false alarms the result would be 21 of 22 correct and supported (95%) instead of 18 of 22 (82%). I report 82% because I did not change the checker after seeing the results.

**q13** (multi): "At what temperature must cold food be kept, and can Listeria still grow at that temperature?" The answer gave 41°F correctly and then said the documents do not state whether Listeria can still grow at that temperature, even though the Listeria chapter retrieved for the question says it can grow at refrigeration temperatures. The right chunk was in the top 5; the model did not use it. The answer is honest but incomplete, and this is the one case where the model ignored evidence it had.

**Partial citations.** q14 and q17 were judged correct but did not cite one of the two expected sections.

**Possible bad test questions.** I checked q04's reference answer ("within 2 hours, and to 41°F within a total of 6 hours") against my own grading: the agent answered only the first stage, which is what the question asks, so the question is fair, but a reader could say the reference answer asks for more than the question does. I kept it as written.

**What to fix first:**
1. Make the citation check tolerant: accept several pages ("p.103, p.106"), strip a "location:" label and a leading "§" before comparing, and compare the location only against the retrieved locations. This would have saved 3 of 4 failures. It must not make the check accept a citation to a page or section that was not retrieved.
2. Rerun the evaluation with a larger model instead of the lite one, to see whether q13 and the unstable venison behaviour are model limits.
3. Add a rule to AGENTS.md that when the question has two parts, the answer must address both or say which part is not covered.

## Decision

**Would I let users rely on it? Not yet for acting on its own; yes as a first-pass lookup that always shows its source.**

What the evidence supports:
- It never made up an answer on the 8 unanswerable questions (8 of 8 refused), including questions on nearby topics such as venison and Trichinella. That is the failure that matters most in this use case.
- Of the 19 answers it gave to answerable questions, 18 were correct and supported according to my grades and the judge's (the other one is q13, an incomplete answer) (the judge and I disagreed on 3 of 30 grades, always in the direction of me being stricter).
- Retrieval found the expected section for every answerable question with design B at k=5.

What stops me from trusting it more:
- 30 questions, written by me with AI help from the same documents, is a small and friendly test. One question moves a rate by 3 points.
- The agent's model (a lite model, chosen because the larger ones were overloaded) ignores the temperature setting, so the same question can give different answers: venison was answered wrongly once (an unsupported claim stretched from a rule about commercially raised game animals) and refused in later runs. A single passing run is not a guarantee.
- The guardrail that protects against invented citations does not check that a sentence is supported by the passage it cites; only the judge measures that.
- The corpus is partial (Food Code chapters 2-3, the bacteria in the Bad Bug Book, one chart) and US-only. A user in Spain follows EU rules, so the right use is as a lookup of the US Food Code text, not as a statement of what the law requires for them.

**Safeguards I would require before real use:** show the cited passage next to every answer so the user can check the number; keep the refusal behaviour and the citation check; fix the citation matcher so good answers are not withheld; rerun the evaluation with a larger model and a much bigger question set (at least 100 questions, including more near-miss unanswerable ones); and tell users that the assistant covers only the documents it names. For an answer that decides a temperature or a time limit, the user should confirm it in the cited passage.

**Cost and latency per question** (30 questions, search tool plus model, agent on gemini-3.5-flash-lite): on average 5,406 input tokens and 105 output tokens; median 7.2 s, mean 19.7 s, maximum 76.4 s. The long times are mostly waiting for overloaded Gemini models (the agent retries other models); 10 of 30 questions used 2 to 4 searches. Each search costs one embedding (the free tier allows about 1,000 per day); the whole evaluation used a few hundred. The judge adds about 22 more model calls per evaluation run.

## AI use

I used Claude (Anthropic's assistant, Sonnet 5.5, through Claude Code and the Claude app) throughout the project, and the Gemini API for the embeddings, the agent and the judge.

**What Claude did:** explained each coding step in plain language as I went; helped me write the code in index.py, server.py, agent.py and evaluate.py; drafted the AGENTS.md rules, the subagent file, and aided with gramatical and style corrections for the text of this report from my results. 