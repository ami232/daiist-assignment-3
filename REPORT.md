# Assignment 3 Report

- **Name:** Eloy Sánchez Zambrano
- **Student ID:** [19367]
- **Group:** [BBADBA 5B]

## Use case

I built this assistant for a warehouse shift supervisor who needs to look something up during a shift. For example, a delivery driver arrives for the first time and asks where to go. The supervisor can use the assistant to find the relevant instructions and open the cited page before briefing the driver.

Some details depend on the warehouse. A guide can explain who the driver should report to, but the gate number comes from the site’s own arrival instructions. If that information is missing, I would want the assistant to say so. A guessed gate number sounds helpful until the driver turns up at the wrong entrance.

## Corpus

I used three guides from the UK Health and Safety Executive (HSE). I chose them because they cover different questions a supervisor might get during a shift, from cleaning up a spill to checking who can operate a lift truck. The word counts are from the text I extracted.

| Guide | Year | Words extracted | Reuse information |
|---|---:|---:|---|
| [HSG76 – Warehousing and storage](https://www.hse.gov.uk/pubns/books/hsg76.htm) | 2007 | 49,371 | Crown copyright. The PDF includes its original permission notice. |
| [HSG136 – A guide to workplace transport safety](https://www.hse.gov.uk/pubns/books/hsg136.htm) | 2014 | 17,186 | Crown copyright. The PDF refers readers to HSE’s reuse policy. |
| [L117 – Rider-operated lift trucks](https://www.hse.gov.uk/pubns/books/l117.htm) | 2013 | 12,602 | The PDF permits reuse under the Open Government Licence, excluding logos. |
| **Total** | | **79,159** | |

This project uses extracted text. It contains public sector information published by the Health and Safety Executive and licensed under the Open Government Licence. Some images and illustrations may have separate rights. [HSE copyright and reuse policy](https://www.hse.gov.uk/help/copyright.htm)

I added a fictional North Yard arrival procedure later for a separate test. The totals above cover the three original guides.

## Ingestion

I extracted the PDFs one page at a time. In `corpus/pages.csv`, I saved the cleaned text, the guide it came from and its printed page number. I extracted 219 pages and used 218. I left out page 140 of HSG76 because its reading order still needed checking.

I split the text into 519 chunks of up to 220 words each. Neighbouring chunks on the same page share 40 words so that a passage still has some context where it was split. Each chunk stays on one printed page. This makes it easy to go from a search result back to the PDF. For example, `HSG136-p026-c01` is the first chunk on printed page 26 of HSG136.

## Test set

I wrote 30 questions from the perspective of a warehouse supervisor. For each answerable question, I saved a reference answer and the expected guide and page in `eval/questions.csv`. Twenty questions needed one passage, five needed evidence from more than one page, and five asked for local details missing from the guides.

Two examples show what I wanted to test:

- **q02:** “When should we provide a refuge at a wide loading bay?” One page gives the answer. A refuge is an alternative to having two exits, one at each end of the bay [HSG136, p. 27].
- **q26:** “At our North Yard warehouse, which numbered gate should a first-time delivery driver use to report to the site operator?” The original guides explain who the driver should report to, but give no gate number for North Yard. I used this question again after adding the local arrival procedure.

## Retrieval

I compared two ways of searching the guides: dense search using Gemini embeddings and BM25 keyword search. For the 25 answerable questions, I checked the first result, then the first three and the first five. A question counted as a hit only if the results included every expected page. If a question needed two pages and the search found one, it counted as a miss.

| Search method | Hit@1 | Hit@3 | Hit@5 | Average words in the five passages |
|---|---:|---:|---:|---:|
| Dense | 10/25 (40%) | 17/25 (68%) | 20/25 (80%) | 931 |
| BM25 | 10/25 (40%) | 13/25 (52%) | 16/25 (64%) | 1,011 |

I chose dense search with five chunks. It found all the expected pages for four more questions than BM25 and added about 80 fewer words to the prompt per search. I counted the passage text only, excluding citation labels and tool instructions.

Questions that needed two pages were harder. With five results, dense search found the expected page for 18 of the 20 single-page questions, but found both pages for only two of the five multi-page questions. BM25 also scored 2/5 on that group. The methods missed different cases. For example, BM25 found both training pages for q24, while dense search missed at least one.

## Tools and subagent

I set up two tools in the MCP server:

- `search(query)` returns five passages with their guide, printed page and chunk ID. For the first-time driver question, one result was `HSG136-p026-c01`. Paragraph 125 tells visiting drivers to report to the site operator for instructions on the layout, route, parking and loading areas [HSG136, p. 26].
- `add_document(path)` adds a local text-based PDF to the index and returns its source ID and chunk count. It also checks whether the document has already been indexed.

In VS Code Copilot, I gave the `warehouse-researcher` subagent access only to `corpus/search`. I asked it to search before answering, give a short answer in plain English and cite the guide and printed page for each claim. If a search covered only part of a question, it should search for the other part and say what was still missing. I also asked it to preserve the guide’s wording when a distinction like “should” or “must” matters.

### Example from VS Code Copilot

**Question:** What information should I give a driver who is visiting our warehouse for the first time?

**Subagent response:**

> Give the driver:
>
> - **Before arrival:** A map and directions, vehicle restrictions, route hazards, where and when to report, and—if needed—pictograms or information in multiple languages. (HSG76, printed p. 80)
> - **On arrival:** The site layout and safe route, where to park and load or unload, who is in charge, and the driver’s responsibilities. (HSG136, printed p. 26; HSG76, printed p. 80)
> - **For safety:** Site rules, required PPE, and what to do in an incident or accident; tell them that high-visibility clothing must be worn at all times. (HSG76, printed p. 80; HSG136, printed p. 26)

I checked the answer against page 26 of HSG136. Paragraph 125 supports the instructions about reporting to the operator and finding the right route. The high-visibility wording, however, appears on an example sign. The response turned one site’s sign into a rule for every warehouse.

## Adding a document

I asked q26 twice with the same model to see whether adding one document would change the answer.

**Before adding the PDF**, the agent explained that drivers should report to the site operator and said it could not determine the gate number. That was the expected answer with the original three guides. The saved response is in `eval/baseline_gemini_3_1_flash_lite/q26.json`.

**After adding the PDF**, I asked the same question again. The new file, `corpus/north_yard_arrivals.pdf`, was a one-page fictional procedure written for this test. This time the agent answered:

> At the North Yard warehouse, first-time delivery drivers must report to the site operator at Gate 3 [north_yard_arrivals-d9d657a3, p. 1].

I saved this response in `eval/q26_after.txt`. I kept the original response in the 30-question evaluation because the gate number was missing when I ran that test.

I also tried adding `hsg136.pdf` a second time. The tool returned `Already indexed: HSG136 (original corpus).` It recognised the file by its hash and skipped embedding it again.

## Harness and guardrails

The agent reads its rules from `AGENTS.md`. It should search before answering, cite a printed page for each factual claim and keep the distinction between “must”, “should” and “may”. For a two-part question, it should check both parts. If the search itself fails, it should tell the user what happened. A failed search is different from a successful search that finds no answer.

Adding a document changes what the assistant can use in future answers, so I included an approval step. The agent checks that the selected file is an existing PDF inside `corpus/`, displays the full path and asks the user to type `yes`. The user has to approve it in an interactive terminal.

I also limited the agent to four tool calls per question. I saw this limit in q03, about a loading bay where guardrails would not fit. When the agent tried another search, the trace recorded `Tool-call limit reached. Use existing evidence.` It then answered using the passages it already had, including HSG136, p. 27.

## Evaluation

I looked at two things separately. **Correctness** asks whether the answer covers every essential point in the reference answer. For an unanswerable question, that means recognising what is missing without guessing. **Support** asks whether the retrieved passages back up every factual claim, including extra examples. An answer can get the main point right and still overstate what the guide says.

Gemini 3.8 Flash answered the first eight questions and Gemini 3.1 Flash Lite answered the remaining 22. I then used Flash Lite as the judge for all 30. It received the question, reference answer, agent answer and retrieved passages. The script compared its grades with the AI-assisted review labels in `eval/human_labels.csv`.

| Criterion | Judge marked yes | Review marked yes | Agreement |
|---|---:|---:|---:|
| Correct answer | 29/30 | 27/30 | 28/30 (93.3%) |
| Every factual claim supported | 30/30 | 21/30 | 21/30 (70.0%) |

For correctness, both the judge and the review flagged q22. They disagreed on q11 and q21, where the judge accepted answers that missed part of the question.

The biggest difference was in support. The judge accepted all 30 answers, while the review flagged nine. For example, in q14 the agent got the pallet inspection timing and the decision to remove a damaged pallet right. The guide used “should”, but the agent described both actions as mandatory. The judge missed that difference.

The citation check found that every cited page appeared in the search results for that question. The refusal detector flagged the five unanswerable questions and one extra case, q09. When I read q09, the agent had answered the pothole question and only said that it lacked details about local procedures. After checking that case, the final count was **five correct refusals and zero wrong refusals**.

## Failures

The review found problems in 11 of the 30 original answers. Three were incomplete (q11, q21 and q22). Nine included a claim the evidence did not fully support (q03, q09, q14, q17, q19, q21, q24, q25 and q29). Since q21 had both problems, it appears in both groups.

In q11, the search returned pages 53 and 54 of HSG76 and missed page 55. The answer listed risk factors but left out three practical steps: watching the work, talking to employees and checking the injury history. I classified this as a retrieval miss.

In q21, the search found the arrival instructions on HSG136, p. 26, but missed the training guidance on L117, p. 16. This explains why the answer left out assessment and any necessary training and reassessment. I counted this as a retrieval miss as well as an unsupported claim about high-visibility clothing.

**q22 showed what happens when the search misses half a question.** The agent explained how to take a damaged pallet out of use. It missed two checks before dispatch: whether the replacement pallet was rated for the load and whether it was secured to the vehicle. The search found passages about damaged pallets and pallet inverters, but missed the checklist on HSG136, p. 30. I would search separately for each part and check that the final answer covers both.

**q21 showed what can go wrong even when the search finds the right page.** The agent treated the high-visibility instruction on an example sign as a general rule. I saw the same mistake when I ran `check.py` after adding the North Yard document. All checks passed, but the answer still overstated what HSG136, p. 26 said. That later run is separate from the original 30 answers.

My first fix would be to check claims containing words like “must”, “always” or “will be denied”. For each one, I would ask: who does this instruction apply to, and does the cited page actually use wording that strong?

## Decision

I would use this assistant to find the right page during a shift. Before briefing a driver, I would read the passage and check who it applies to. The high-visibility example in q21 is why: the agent found the right page and still gave a broader instruction than the guide supported.

| Agent model | Questions | Mean tokens per question | Mean time | Median time |
|---|---:|---:|---:|---:|
| Gemini 3.8 Flash | 8 | 5,719 | 1,229.4 s | 919.7 s |
| Gemini 3.1 Flash Lite | 22 | 2,486 | 8.2 s | 7.6 s |
| Overall | 30 | 3,348 | 333.8 s | 8.3 s |

I used tokens as a rough measure of cost because the logs recorded usage and time, but no price per request. The table covers completed agent answers. It excludes judge calls and failed attempts.

The two models answered different questions, so these runs cannot tell me how much of the time difference came from the model itself. For the supervisor, the practical issue is the wait. Half of the first eight answers took around 15 minutes or longer. If a driver is already at the loading bay, the supervisor needs a way to open the guides directly.

## AI use

I used ChatGPT/Codex to help write and debug the evaluation code, work through Gemini quota errors, and draft and revise this report. It also helped compare saved answers with the retrieved passages and suggested labels for `human_labels.csv`. The agreement figures therefore compare Gemini’s grades with an AI-assisted review.

I used GitHub Copilot in VS Code to test the `warehouse-researcher` subagent. Gemini 3.8 Flash generated the first eight baseline answers. Gemini 3.1 Flash Lite generated the remaining 22 and graded all 30 saved answers.