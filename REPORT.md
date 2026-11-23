# Assignment 3 Report

- **Name**: Jean Carlos
- **Student ID**: 19832
- **Group**: BBADBA 5A

## Use case

*Who asks, what they do with the answer, and what a wrong answer costs compared with "I don't know".*

WHO ASKS: a freelance drone photographer based in Madrid, before accepting a job (e.g. "Can I fly my C1 drone over this street?").

WHAT THEY DO WITH THE ANSWER: decide whether to take the job, which subcategory to fly in, and what paperwork to prepare.

COST: a WRONG ANSWER can mean a fine, a confiscated drone, or a drone flown over people where the rules forbid it. "I DON'T KNOW" only costs a check with AESA (the Spanish aviation authority) and some delay. So a wrong answer is far more expensive, and the system should refuse rather than guess.

## Corpus

*Table: document, URL, date, licence, words.*

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| Implementing Regulation (EU) 2019/947 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019R0947 | Consolidated 01.05.2025 | EUR-Lex: reuse with attribution (Commission Decision 2011/833/EU) | 19,895 |
| Delegated Regulation (EU) 2019/945 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019R0945 | Consolidated 24.06.2025 | Same | 20,924 |
| Implementing Regulation (EU) 2021/664 | https://eur-lex.europa.eu/eli/reg_impl/2021/664/2026-02-22/eng/pdf | Consolidated 22.02.2026 | Same | 5,955 |
| Recitals of 2019/947 | https://eur-lex.europa.eu/eli/reg_impl/2019/947/oj/eng | 11.6.2019 | Same | 1,620 |
| Recitals of 2019/945 | https://eur-lex.europa.eu/eli/reg_del/2019/945/oj/eng | 11.6.2019 | Same | 3,624 |
| Recitals of 2021/664 | https://eur-lex.europa.eu/eli/reg_impl/2021/664/oj/eng | 23.4.2021 | Same | 1,893 |
| Total | | | | 53,911 |

2019/947 says HOW drones may be flown, 2019/945 sets the drone CLASSES (C0 to C6), and 2021/664 covers U-space airspace. The consolidated texts leave out the recitals (the reasons for each rule), so I added them from the original Official Journal versions. All 6 documents are public EU law, reusable with attribution, and contain no personal data, so the PDFs are committed in corpus/.

## Ingestion

*How you extract, clean and chunk; one extraction problem you fixed; chunk metadata; number of chunks.*

EXTRACT: PyMuPDF reads the text of each page.

CLEAN, in 4 steps:
1. Remove the running page headers repeated on every page.
2. Remove the amendment markers (▼B, ►M1 … ◄) that EUR-Lex adds to consolidated texts.
3. Skip the front matter before the act's title (for the recitals documents, keep only the part before Article 1).
4. Rejoin words split across lines (soft hyphens and hyphenated words).

CHUNK, in 2 designs:
1. STRUCTURE: 1 chunk per article or annex point (e.g. UAS.OPEN.020), so each chunk is 1 complete rule. Its heading path (e.g. `Annex > Part A > UAS.OPEN.020`) is embedded with the text. Sections over 350 words are split into 250-word windows with a 50-word overlap.
2. FIXED: 250-word windows with a 50-word overlap, ignoring the structure.

EXTRACTION PROBLEM I FIXED: pypdf turned EUR-Lex's justified text into broken words ("a ssemblies", "sh all"), 80 of them in 2019/947 alone. PyMuPDF uses the position of each character and extracts the words whole.

CHUNK METADATA (so every search result can be cited):

| Field | Meaning |
|---|---|
| `source` | Document id, e.g. `reg-2019-947` |
| `title` | Document title |
| `section` | Heading path, e.g. `Annex > Part A > UAS.OPEN.030` |
| `sections` | Every section the chunk overlaps |
| `location` | Section and pages |
| `page_start`, `page_end` | First and last page |
| `words` | Length of the chunk |

NUMBER OF CHUNKS: 302 (structure) and 271 (fixed).

## Test set

*How you wrote it, counts by kind, two examples.*

I wrote 37 questions from the text of the indexed chunks, each phrased as the photographer would ask it, with a reference answer and the expected passage(s) taken from the text.

| Kind | Count | What it tests |
|---|---|---|
| Single | 25 | 1 passage answers it |
| Multi | 6 | It needs 2 or more passages |
| Unanswerable | 6 | Close to the topic but not in the corpus (fines, insurance amounts, exam fees) |

2 examples:
1. q27 (multi): "With a C2 drone in A2 using low-speed mode, how close can I get to uninvolved people, and how fast can the drone go in that mode?" Reference: down to 5 m (UAS.OPEN.030 of 2019/947), and 3 m/s (Annex Part 3 of 2019/945).
2. q32 (unanswerable): "Do I have to notify the Spanish Ministry of the Interior before flying over a street in Madrid?" Reference: say the documents do not cover Spanish national rules.

## Retrieval

*Hit rate at 1/3/5 per design, words added to the prompt, the design you chose.*

1. HIT RATE AT k: the share of the 31 answerable questions whose expected passages ALL appear in the top k search results.
2. WORDS AT k: the average number of words those k passages add to the prompt (the cost of a larger k).

| Design | Hit@1 | Hit@3 | Hit@5 | Words@1 | Words@3 | Words@5 |
|---|---|---|---|---|---|---|
| Structure | 55% | 90% | 94% | 239 | 703 | 1,149 |
| Fixed | 52% | 87% | 94% | 250 | 746 | 1,240 |

I chose the STRUCTURE design, with k = 5:
1. Both designs reach 94% at k = 5, but structure is better at k = 1 (55% vs 52%) and k = 3 (90% vs 87%).
2. Structure adds ~90 fewer words to the prompt at k = 5 (1,149 vs 1,240).
3. k = 5 finds the expected passages for 94% of questions, against 90% at k = 3, for ~450 more words.

## Tools and subagent

*Your tools' descriptions, one search result, the subagent's instructions, one transcript from your editor.*

The descriptions below are the docstrings in `server.py`. MCP sends them to the model, which uses them to decide when to call each tool.

`search` description:
```text
Search the EU rules for flying drones (unmanned aircraft systems, UAS).

The corpus holds three EU regulations in their current consolidated versions,
plus their recitals (the reasons given for each rule):
- Implementing Regulation (EU) 2019/947: how drones may be flown. Open,
  specific and certified categories; subcategories A1, A2 and A3; distances
  from people; maximum height; remote pilot age and competency; operator
  registration; geographical zones; standard scenarios STS-01 and STS-02.
- Delegated Regulation (EU) 2019/945: drone classes C0 to C6 (mass, speed,
  low-speed mode, lights, remote identification, geo-awareness).
- Implementing Regulation (EU) 2021/664: U-space airspace and its services.
It also holds any document added with add_document (a Spanish one is in Spanish).

Use it for every question about drone rules, before answering. Search again
with other words, or once per part of a question, if the passages do not
cover everything. If no passage states the answer, the corpus does not cover it.

Returns the 5 passages closest to the query, best first. Each has a citation
[source, section] to copy into the answer, the document title, the pages,
a similarity score from 0 to 1, and the passage text.
```

`add_document` description:
```text
Add a document to the searchable corpus.

Takes the path of a PDF, .txt or .md file on this computer (absolute, or
relative to the project folder). The file goes through the same pipeline as
the corpus: text extraction, cleaning, chunking by article or section, and
embedding with Gemini. Its passages are then stored in the index, and search
finds them from the next call on.

If the identical file is already indexed, nothing changes. If a file with the
same name but different content was indexed before, its old passages are
replaced by the new ones. Files over 300 passages are refused, because each
passage counts towards the daily embedding quota.

Use it only when the user asks to add a document. Returns what happened:
added, replaced, already indexed or an error, with the document's source id
(the name to cite) and its number of passages.
```

One search result (the first of 5 for "What is the maximum height I can fly my drone at in the open category?"). Line 1 is the citation to copy, line 2 the document, location and similarity, line 3 the passage text:
```text
1. [reg-2019-947, Annex > Part A > UAS.OPEN.010]
   Commission Implementing Regulation (EU) 2019/947 (operation of unmanned aircraft) | Annex > Part A > UAS.OPEN.010, p. 24 | similarity 0.80
   ANNEX UAS OPERATIONS IN THE ‘OPEN’ AND ‘SPECIFIC’ CATEGORIES PART A UAS OPERATIONS IN THE ‘OPEN’ CATEGORY UAS.OPEN.010 General provisions (1) The category of UAS ‘open’ operations is divided into three subcategories A1, A2 and A3, on the basis of operational limitations, requirements for the remote pilot and technical requirements for UAS. (2) Where the UAS operation involves the flight of the unmanned aircraft starting from a natural elevation in the terrain or over terrain with natural elevations, the unmanned aircraft shall be maintained within 120 metres from the closest point of the surface of the earth. […]
```

Subagent instructions (`.claude/agents/corpus-researcher.md`). Its only tool is `mcp__corpus__search`, so it can search but never add documents:
```text
You answer questions about the EU drone rules using only the `search` tool of the `corpus` server. A wrong answer can cost the user a fine or an unsafe flight, so accuracy comes before completeness.

1. Search before answering, every time. Search once per part of a multi-part question, with up to 4 searches. If the results miss something, search again with different words.
2. Answer only from the passages the search returned. Add no general knowledge, national rules or advice that they do not state.
3. After each sentence that states a fact, copy the citation exactly as the result shows it, for example `[reg-2019-947, Annex > Part A > UAS.OPEN.030]`.
4. Copy numbers and units exactly, with their conditions and exceptions.
5. If no passage states the answer, reply with exactly `The documents do not cover this.` Never guess. If only part is covered, answer that part and write `The documents do not cover` followed by the missing part.
6. Reply with a short answer first (one to three sentences), then any details, and nothing else.
```

Transcript from Claude Code in VS Code. The main agent delegated the question, and the subagent searched once and answered with citations:
```text
User: Use the corpus-researcher subagent to answer: What is the maximum take-off mass of a class C2 drone?

Agent: C2 drone max take-off mass
  IN: What is the maximum take-off mass (MTOM) of a class C2 drone under the EU rules? Search the corpus
      (Regulation 2019/945 class requirements for C2) and answer only from the returned passages, with the
      exact value and unit, any conditions attached, and the citation exactly as the search result shows it.
      If the passages don't state it, reply "The documents do not cover this."
  Finished

Claude Code: A class C2 drone must have an MTOM of less than 4 kg, including payload [reg-2019-945, Annex > Part 3].
* The limit is strictly "less than" 4 kg, and the payload counts toward it [reg-2019-945, Annex > Part 3].
* A C2 drone must also limit its maximum attainable height above the take-off point to 120 m. Alternatively,
  it can have a system that limits the height above the surface or above the take-off point to 120 m or to a
  value the remote pilot selects [reg-2019-945, Annex > Part 3].
* If the drone is tethered, the tether's tensile length must be less than 50 m [reg-2019-945, Annex > Part 3].
The subagent ran one corpus search. The answer comes from Regulation (EU) 2019/945, Annex, Part 3
("Requirements for a class C2 Unmanned aircraft system").
```

## Adding a document

*What happens when a document is already indexed. The unanswerable question, the document you added, the answer before and after.*

WHEN A DOCUMENT IS ALREADY INDEXED:
1. Same content (same SHA-256 fingerprint): nothing changes, and the tool says it is already indexed.
2. Same file name, new content (e.g. a new version of the rules): its old passages are replaced by the new ones.

THE TEST:
1. Unanswerable question: q32, "Do I have to notify the Spanish Ministry of the Interior before flying over a street in Madrid?"
2. Document added: Real Decreto 517/2024 (Spain), https://boe.es/buscar/pdf/2024/BOE-A-2024-11377-consolidado.pdf (BOE, reuse allowed citing the source), 38,467 words in 209 passages.
3. Result: BEFORE, the agent refused and pointed to the nearest EU rule (its saved q32 answer in `eval/answers.jsonl`, from the evaluation run before the decree was added). AFTER, it answered from Article 40 of the decree.

Before:
```text
The documents do not cover this.

Member States may define UAS geographical zones for safety, security, privacy, or environmental reasons, which can include prohibiting operations, requesting particular conditions, or requiring prior flight authorisation `[reg-2019-947, Article 15]`.
```

After:
```text
Yes, for operations in urban environments or over assemblies of people, operators subject to the registration obligation who intend to carry out UAS operations must communicate it previously to the Ministry of the Interior at least five natural days in advance of the planned start date of the operation [rd-517-2024, Capítulo V > Sección 2.a > Artículo 40].
```

## Harness and guardrails

*Your AGENTS.md rules, the approval step, and your extra guardrail with one case where it fired.*

AGENTS.md rules (the agent's system prompt):
1. Search before answering, because the rules were amended several times and the model's memory may be outdated.
2. Answer only from the search results, because an unsupported claim looks as trustworthy as a supported one.
3. Cite every claim exactly as the result shows it, so the user can check it.
4. Search once per part of a question, because 1 query usually does not retrieve 2 different passages.
5. If no passage states the answer, reply exactly "The documents do not cover this.", because a refusal is cheap here and the fixed wording lets code count refusals.
6. Keep numbers and units exact, because a slightly wrong limit changes whether a flight is legal.
7. Be short and answer in the user's language, because the user often reads the answer on site.
8. Never call add_document unless the user asks, because it changes the corpus and spends quota.

APPROVAL: add_document changes the corpus for every later answer, so a `wrap_tool_call` middleware stops every `add_document` call and asks `Allow add_document({...})? [y/N]` in the terminal. Anything but `y` refuses the call. With no terminal (evaluation, check.py), it refuses automatically.

EXTRA GUARDRAIL, GROUNDING: after the model answers, code checks 2 things:
1. Every citation names a passage that search returned in that run.
2. Any answer that is not a refusal cites something.

If either check fails, the model gets 1 retry with the reason. If it fails again, the answer is replaced by a refusal.

Case where it fired: in q05, the model merged 2 passages into 1 citation, `[reg-2019-947, Annex > Part A > UAS.OPEN.030, reg-2019-947, Annex > Part A > UAS.OPEN.040]`, which matches no retrieved passage. After the retry, it cited each passage separately and the answer was correct.

CALL LIMIT: at most 8 model calls per question (`ModelCallLimitMiddleware`), so a loop cannot run up cost.

## Evaluation

*Code checks, the judge's rubric, your agreement with the judge, and results: correct, unsupported, correct refusals, wrong refusals.*

I ran the agent on all 37 questions and graded the answers in 3 ways: code, an LLM judge, and my own grades.

CODE CHECKS (what code can check exactly):
1. Every answer searched first (37/37).
2. Every citation names a passage retrieved in that run (37/37).
3. Every answer either cites a passage or is a refusal (37/37).
4. Refusals are detected by the fixed sentence and graded in code: correct when the question is unanswerable.

THE JUDGE'S RUBRIC (`gemini-3.5-flash`, given the question, the reference answer, every retrieved passage and the answer):
- Correct: gives the key facts of the reference and contradicts none. Missing minor detail is fine, but declining an answerable question is not. For an unanswerable question, correct only if it says the documents do not cover it.
- Supported: every factual claim is stated in the retrieved passages, judged only against them.

AGREEMENT between my grades and the judge's, on 23 answers (q01–q14 and q26–q34):

| | Agreement | Same grade |
|---|---|---|
| Correct | 91% | 21 of 23 |
| Supported | 91% | 21 of 23 |
| Both | 87% | 20 of 23 |

We disagreed on q02, q12 and q30 (see Failures).

RESULTS, the judge's verdicts (refusals graded in code), 37 questions:

| Outcome | Count |
|---|---|
| Correct | 30 |
| Unsupported | 1 |
| Correct refusals | 6 |
| Wrong refusals | 0 |

After my review, 3 answerable answers are wrong (q02, q12 and q30), so 28 of 31 are correct. The Failures section uses these final grades, and counts the judge's 1 unsupported answer (q02) under its root cause.

## Failures

*Failed questions by cause, with counts, and what to fix first.*

3 answers failed. Each is counted once, under its ROOT cause:

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 1 | q12: UAS.OPEN.050(7) (involved persons must be informed of the risks and explicitly agree) was never retrieved. The agent searched with its own shorter queries ("A2 A3 people involved staff consent", "uninvolved persons definition"), while the question's own wording finds UAS.OPEN.050 in the top 5 (`eval/retrieval.json`). |
| Wrong answer from the right passage | 2 | q02: applied the rule for C0 and sub-250 g drones (may overfly uninvolved persons) to a C1 drone, which must NOT overfly them. q30: recital 16 (privacy risk) was retrieved, but the answer gave the conditions for registering instead of the reason. |
| Unsupported claim | 0 | |
| Wrong refusal | 0 | |
| Bad test question | 0 | |

How they were found:
1. q12 and q30: the judge accepted them; my grades rejected them.
2. q02: the judge found it unsupported. I had graded it correct because my reference answer made the same mistake, and re-reading UAS.OPEN.020 showed the judge was right. I left my grade unchanged so the agreement figures stay honest.

What to fix first:
1. The q02 kind, the most EXPENSIVE error for this user. Correct q02's reference answer and add an AGENTS.md rule: state which drone class or condition each quoted clause applies to, and match it to the user's case.
2. The q12 kind: add an AGENTS.md rule to run the first search with the user's own wording, because the agent's shorter rewrites missed a passage that the original question finds.

## Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

YES, for finding and quoting the EU rule that applies, with its citation, as a first check before accepting a job:
1. No final answer cited a passage that search did not return (the guardrail caught 2 attempts, in q05 and q20).
2. It refused all 6 unanswerable questions.
3. BUT 3 of 31 answerable answers were wrong in a way that reads as confident.

SAFEGUARD: the user opens the cited article before flying, and treats "The documents do not cover this" and anything national (fines, notifications, local zones) as a prompt to check with AESA.

| Per question | |
|---|---|
| Tokens | 7,284 (7,101 in, 184 out) |
| Seconds | 7.5 |

## AI use

*What you used and how, or "none".*

I looked for relevant corpuses on Google, and then used Claude to write the code, instructing it what to do using the assignment instructions, verifying the results, and ensuring they were what was expected; if not, I prompted Claude to adjust the index, agent, and evaluate files accordingly. I also graded the 23 answers myself, and then wrote the report.