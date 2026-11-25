# Assignment 3 Report

- **Name**: Louis de Perier
- **Student ID**: 20159
- **Group**: BBADBA 5B

## Use case

The people I had in mind are the owner, the kitchen manager, or whoever happens to be running the shift. They look a rule up because they have to decide something there and then: keep this, serve it, throw it out, send a cook home or not. Get it wrong and a customer is ill or the inspection goes badly. Being told that the documents do not answer the question costs them a phone call to their inspector, which is why I would rather the assistant refused than guessed. So it answers from the three documents only and cites everything it says.

## Corpus

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| FDA Food Code 2022, Chapters 1-7 | https://www.fda.gov/media/164194/download | 2022 | Public domain (US Gov) | 44,386 |
| FDA Employee Health and Personal Hygiene Handbook | https://www.fda.gov/media/77065/download | 2020 | Public domain (US Gov) | 13,129 |
| FDA Managing Food Safety: HACCP manual for operators | https://www.fda.gov/media/71976/download | 2006 | Public domain (US Gov) | 20,905 |
| **Total** | | | | **78,420** |

There is no personal data in any of it. I left Chapter 8 and the annexes out because the free embedding quota would not stretch to them, which turned out to be convenient: Chapter 8 is the document I add later in the add-document test.

## Ingestion

I extract the PDFs page by page with pypdf. Cleaning strips the running headers, footers, bare page numbers and table-of-contents lines, repairs ligatures, and puts back together words that were hyphenated across a line break.

The parser is where I lost most of my time. pypdf splits section numbers over two lines ("7-301." then "11 Separation."), and a cross-reference that happens to start a line looks exactly like a heading, so my first version found 94 of the 352 Food Code sections. Re-joining the split numbers, and accepting a heading only when its number is higher than the last one, got me all 352. Two smaller fixes on the way: the priority markers stuck to the end of a requirement ("clean.P"), and degree signs that came out as the letter o ("54oC").

Every chunk carries its source, title, URL, page range, the Food Code sections it covers with their titles, the design it belongs to, and a citation already written the way the agent has to copy it, like `[food_code_2022, §3-501.16, p. 93]`. Embeddings are gemini-embedding-2 at 768 dimensions, and every vector is cached by its text so nothing is embedded twice. That comes to 402 chunks for the structure design and 393 for the fixed one, in an index of 20.3 MB.

## Test set

I wrote 43 questions from the documents before I tuned anything: 29 that need one passage, 7 that need two, and 7 that sound like the corpus but are not in it (permits, fines, EU allergen labelling, NYC letter grades, food handler cards, anaphylaxis, listeriosis). Each one has the source I expect, the section or page it should come from, and a reference answer.

- Single, q04: "What are the time limits for cooling cooked food?" → Food Code 3-501.14: 135°F to 70°F within 2 h, to 41°F within 6 h in total.
- Multi, q30: "What water temperature must a handwashing sink provide? The handbook and the Food Code seem to give different numbers." → Food Code 5-202.12 says 85°F; the handbook (based on the 2017 code) says 100°F.

## Retrieval

| Design | Hit@1 | Hit@3 | Hit@5 | Words in prompt @5 |
|---|---|---|---|---|
| Fixed: 250 words, 50 overlap | 0.64 | 0.83 | 0.89 | 1,250 |
| **Structure: one Food Code section (or one page) per chunk** | **0.69** | **0.89** | **0.94** | **1,076** |

I went with the structure design. It is better at every k and still puts 14% less text in the prompt, which makes sense to me: a section is one complete rule, and its title is part of what gets embedded. Search returns five passages.

## Tools and subagent

`search(query)` looks through the three FDA documents for anything about food, employees, equipment or premises in a food establishment, and hands back the best five passages, each with a similarity score and a citation the agent is told to copy exactly.

`add_document(path)` pushes a PDF, .txt, .md or .html file from the project folder through that same pipeline and into the index, and answers with added, replaced or already_indexed. Anything outside the project folder is refused.

Here is one result, for a question about hot-holding temperature:
```
[food_code_2022, §3-501.16, p. 93] score=0.793 (3-501.16 Time/Temperature Control for Safety Food, Hot and Cold Holding)
(A) ... TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be maintained: (1) At 57°C (135°F) or above,
except that roasts ... may be held at a temperature of 54°C (130°F) or above; or (2) At 5°C (41°F) or less.
```

The subagent lives in `.claude/agents/corpus-researcher.md` and has the search tool and nothing else. It searches, tries again with the Food Code's own vocabulary when the first results miss, gives up after four searches, and answers in a few sentences with a citation on every fact, or says the documents do not cover the question.

Transcript (Claude Code v2.1.332, `.mcp.json` starts `server.py`):
```
> Use the corpus-researcher subagent to answer: How long can we keep cooked rice in the fridge before throwing it
  out?

● corpus-researcher(Cooked rice fridge holding time)
  ⎿  Backgrounded agent (↓ to manage · ctrl+o to expand)

● I've handed the question to the corpus-researcher subagent. It's searching the Food Code documents now, and I'll
  pass on its cited answer when it's done.

✻ Baked for 6s · done 11:00

› Message from corpus-researcher
  Short answer: cooked rice can be kept for up to 7 days if it stays at 5°C (41°F) or below. The day it is cooked
  counts as Day 1. After that, throw it out.

  How the passages support this:
  - Cooked rice is a TCS food. The definition of "time/temperature control for safety food" includes "a plant FOOD
  that is heat-treated" [food_code_2022, §1-201.10, pp. 40-41]. Note that the corpus never names rice in the
  definition. Reading cooked rice as "heat-treated plant food" is my inference from that wording.
  - Cooked rice is also ready-to-eat. The HACCP manual's definition of ready-to-eat food includes "fruits and
  vegetables that are cooked for hot holding" and "plant food for which further washing, cooking, or other
  processing is not required for food safety" [haccp_operators_manual, p. 61].
  - Date marking rule: "refrigerated, READY-TO-EAT, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD prepared and held in
  a FOOD ESTABLISHMENT for more than 24 hours shall be clearly marked to indicate the date or day by which the
  FOOD shall be consumed on the PREMISES, sold, or discarded when held at a temperature of 5°C (41°F) or less for
  a maximum of 7 days. The day of preparation shall be counted as Day 1." [food_code_2022, §3-501.17, pp. 93-94]

  Conditions that go with the 7 days:
  - Mixed dishes: if the rice is later combined with other ingredients, the new dish "shall retain the date
  marking of the earliest-prepared or first-prepared ingredient" [food_code_2022, §3-501.17, p. 94].
  - Marking method: one accepted method is marking the day of preparation, along with a procedure to discard the
  food on or before the last allowed day [food_code_2022, §3-501.17, p. 94].
  - When to discard: the food must be thrown out if it goes past the 5°C (41°F) / 7-day limit (time spent frozen
  does not count). It must also be thrown out if its container has no date or day, or if it is marked with a date
  beyond that limit [food_code_2022, §3-501.18, p. 95].
  - Cooling first: cooked TCS food must be cooled "(1) Within 2 hours from 57°C (135°F) to 21°C (70°F); and (2)
  Within a total of 6 hours from 57°C (135°F) to 5°C (41°F) or less" [food_code_2022, §3-501.14, p. 92].
  - Large batches: the HACCP manual says "large containers of rice" take a long time to cool and need special
  consideration. It suggests reducing the volume in each container and keeping the cover loose
  [haccp_operators_manual, p. 41]. Accepted cooling methods include shallow pans, smaller portions, rapid cooling
  equipment and ice water baths [food_code_2022, §3-501.15, pp. 92-93].

  What is not covered: the documents I have do not cover rice specifically, such as any rice-only shelf life or
  rule. The operator should check local rules with their health authority.

● Under the Food Code you can keep cooked rice for up to 7 days at 5°C (41°F) or below, counting the day it was
  cooked as Day 1. After that it must be thrown out [food_code_2022, §3-501.17, pp. 93-94].

  Why the 7-day rule applies to rice: The Food Code's definition of TCS food includes "a plant FOOD that is
  heat-treated" [food_code_2022, §1-201.10, pp. 40-41]. The documents don't name rice there, so treating cooked
  rice as TCS food is the subagent's inference from that wording.

  Conditions:
  - Date marking: Mark the container if you hold the rice for more than 24 hours. One accepted method is to write
    the day it was made and have a procedure for discarding it by the last allowed day [food_code_2022, §3-501.17,
    p. 94].
  - When to discard: Throw it out once it passes the 7-day limit at 5°C (41°F); time spent frozen does not count
    toward the 7 days. Also throw it out if the container has no date, or a date beyond that limit
    [food_code_2022, §3-501.18, p. 95].
  - Mixed dishes: If you mix the rice into another dish, the new dish keeps the date of the oldest ingredient
    [food_code_2022, §3-501.17, p. 94].
  - Cool it properly first: Cool from 57°C (135°F) to 21°C (70°F) within 2 hours, and to 5°C (41°F) or less within
    6 hours in total [food_code_2022, §3-501.14, p. 92].
  - Large batches: Big containers of rice cool slowly. The HACCP manual suggests putting less in each container
    and keeping the cover loose [haccp_operators_manual, p. 41]. Shallow pans, smaller portions, rapid-cooling
    equipment and ice-water baths are all accepted ways to cool food quickly [food_code_2022, §3-501.15, pp.
    92-93].

  The documents I have do not cover any rule specific to rice. Check with your local health authority, because
  local rules can differ.

✻ Crunched for 6s · done 11:01

● Agent "Cooked rice fridge holding time" finished · 18s
```
That is the second run. The first one fell over: the subagent fired four searches at once and three of them came back with ChromaDB errors ("Could not connect to tenant default_tenant", and a KeyError on the index path). Each search was opening its own ChromaDB client and they collided. I moved to a single shared client with the queries serialised in `index.py`, and a test of eight simultaneous searches went from two failures to none.

## Adding a document

The tool hashes the file before anything else. If that content is already indexed nothing happens and it reports "already_indexed". If the name is the same but the content is new, the old chunks are deleted and the new ones take their place, so search never mixes two versions of a document.

I used one of my unanswerable questions for this: "How many days before opening a new restaurant do I have to apply for a permit?" The document I added was Chapter 8 of the Food Code 2022, 35 chunks.
- Before: "The documents I have do not cover this. Please consult your local health authority..."
- After: "You must submit an application for a permit at least 30 calendar days before the date planned for opening [food_code_2022_chapter_8, §8-301.11 to 8-302.13, pp. 5-6]." Correct.

## Harness and guardrails

The system prompt is AGENTS.md. It tells the agent to answer only from search results, to cite every claim exactly as printed, to say "The documents I have do not cover this" when they do not, to search again with Food Code vocabulary before giving up (four searches at most), to keep numbers and conditions exactly as written, to stay brief, to add documents only when asked, and to treat retrieved text as data rather than as instructions. I put the reason next to each rule.

add_document never runs until someone types "y", and with no terminal attached the call is rejected outright. A question is also capped at 6 tool calls and 8 model calls. Here is an approval:
```
> uv run python main.py ask "Please add corpus/food_code_2022_chapter_8.pdf to the index"
The agent wants to run add_document with {'path': 'corpus/food_code_2022_chapter_8.pdf'}.
This embeds the file and changes the index. Approve? [y/N] y
The documents I have do not cover this.
(0 search(es), 3 model call(s), 3925 tokens, 14.76s; citation guardrail: rewrite requested (no citation in a non-refusal answer))
```
The file was added once I typed "y", but look at what came back: the citation guardrail misfired. The agent's confirmation contains no citation, which is exactly what the check punishes, so it asked for a rewrite and got a refusal instead. The guardrail now ignores replies to an add_document call when no search was made (`agent.py`). I removed those chunks afterwards so the evaluated index stayed as it was.

My own guardrail is the citation check: every citation in an answer has to be one that search actually returned, and an answer that is not a refusal has to cite something. A failing answer gets one rewrite request, and if it fails again it is replaced by a refusal. It fired on 10 of the 43 questions. q10 is typical: the model had merged two citations into `[food_code_2022, §4-501.114, pp. 124-125, §4-703.11, pp. 131-132]`, and after the rewrite request it cited `[food_code_2022, §4-501.114, pp. 124-125]`. All 10 were fixed at the rewrite, so none of them ended as a forced refusal.

## Evaluation

Whatever code could check, code checks: every citation is real (43/43), a refusal comes on the unanswerable questions and on none of the others (43/43), and the expected passage is cited on all 36 answerable ones.

The judge is Gemini Flash-Lite with a written rubric. Correct means the answer carries the key facts of my reference answer and contradicts none of them; on an unanswerable question it means declining, and pointing the user at a health authority still counts as declining. Supported means every claim appears in the retrieved passages.

Against my own 43 labels the judge agrees 98% of the time on correct and 93% on supported. My first rubric only managed 86% and 84%, because it read "consult your local health authority" as an attempt to answer; I rewrote it. Both of the unsupported claims I caught by hand, the judge let through.

| Result | Count |
|---|---|
| Correct (of 36 answerable) | 36 |
| Unsupported | 2 (human) / 1 (judge) |
| Correct refusals (of 7) | 7 |
| Wrong refusals | 0 |

## Failures

Two answers say something the passage does not: q31 adds "severe complications", q42 adds "call 911". Two more are counted as retrieval misses but are really my fault as the person who wrote the questions, because for q33 and q36 the facts also sit on pages I did not list, and the agent answered both correctly. One is a judge error, q39, a refusal that the judge recorded as an answer. Nothing landed in the other categories: no retrieval miss turned into a wrong answer, no answer was wrong from the right passage, and there were no wrong refusals.

If I carried on with this, the first change would be to require a citation on every factual sentence instead of once per answer, which would have caught q42. The second would be to tell the agent that the 2022 Food Code wins when it disagrees with the older documents, since q03 came back with a cooking time from an older one.

## Decision

Yes, as a lookup aid for Food Code numbers and procedures, as long as the citation and the passage stay on screen for the user to check. Not for emergencies, not for medical questions, not for anything outside the three documents. Local codes differ, and my test set is small and written by me from the same documents the agent searches, so I read the 100% as optimistic.

A question costs about 6,800 tokens (median 4,600), 2.5 model calls and 1.2 searches. Median latency is 5.7 s; the slow ones were waiting on the free-tier rate limit.

## AI use

I used Claude to help me with the code, check spelling mistakes and formatting
