# Assignment 3 Report

- **Name**: Andrea Bastien Saxod
- **Student ID**: 18996
- **Group**: BBADBA 5A

## Use case
The idea behind this is to support staff members at a padel club, such as the person selling rackets in the pro shop or coaches. In such environments, it is common for amateur players to ask, "Should I buy a light racket because my elbow hurts?" or "Do round rackets have a bigger sweet spot?" The objective of the answer is to pass that knowledge to the player so they can decide whether to buy a new racket, change how often they play, or whether visiting a physiotherapist is the right call. A wrong answer can cost the player money and can cause an injury. Let's say we told a player with elbow pain that a heavy racket is fine, but it ends up making the injury worse. Tennis elbow is the most common injury in our papers. Saying "I don't know" only costs us a few minutes; the same goes for referring to a coach or physiotherapist. The assistant should refuse rather than guess, which means all answers must quote the source or state that the corpus does not cover this information.

## Corpus

The corpus consists of 9 scientific papers about padel rackets and injuries, none of which contain personal data. All licences allow this use; therefore, I saved the PDFs in 'corpus/'. Note that the word counts reflect the PDFs after cleaning.

| ID | Paper | Link | Date | Licence | Words |
|---|---|---|---|---|---|
| blanes2023 | Sweet spot of padel rackets measured with a robot (Sensors) | https://www.mdpi.com/1424-8220/23/24/9908 | 2023 | CC BY 4.0 | 4,853 |
| blanes2022 | Weight, balance and maneuverability of padel rackets (Sensors) | https://www.mdpi.com/1424-8220/22/23/9266 | 2022 | CC BY 4.0 | 8,092 |
| munoz2022 | Upper-body injuries in amateur players and their rackets (IJERPH) | https://www.mdpi.com/1660-4601/19/24/16858 | 2022 | CC BY 4.0 | 4,424 |
| dahmen2023 | Systematic review of padel injuries (BMJ Open SEM) | https://bmjopensem.bmj.com/content/9/2/e001607 | 2023 | CC BY-NC 4.0 | 5,014 |
| garcia2022 | Review of padel performance research (IJERPH) | https://www.mdpi.com/1660-4601/19/7/4395 | 2022 | CC BY 4.0 | 5,500 |
| martin2025 | Review of research on under-18 players (Sports) | https://www.mdpi.com/2075-4663/13/3/75 | 2025 | CC BY 4.0 | 6,898 |
| aguilar2026 | Review of padel injuries and their treatment (Applied Sciences) | https://www.mdpi.com/2076-3417/16/6/2680 | 2026 | CC BY 4.0 | 7,144 |
| portugal2025 | Injuries of Portuguese padel players (Medicina) | https://www.mdpi.com/1648-9144/61/9/1707 | 2025 | CC BY 4.0 | 8,515 |
| madinah2025 | Injuries of padel players in Madinah, Saudi Arabia (Healthcare) | https://www.mdpi.com/2227-9032/13/4/367 | 2025 | CC BY 4.0 | 4,436 |
| **Total** | | | | | **54,876** |

Later, for the "add a document" test, I also added the Wikipedia article Padel (CC BY-SA 4.0).

## Ingestion
Extraction happens page by page, so every piece of text remembers its page number. For cleaning, it removes things that aren't considered real content, like page headers and footers, page numbers, licence boxes, figure captions, broken symbols from equations, and everything after "References" (references, funding, author details). I did have to fix an issue where two PDFs secretly contained each paragraph two or three times. This made the program read all the copies, so one paper looked twice as long as it really was (9,283 words instead of 4,850), and the search result was then full of duplicate sentences. The fix worked by comparing each line with the text already kept, ignoring spaces and line breaks, and skipping any repeats. After the fix, each section appeared only once. Later on, I ran into another issue that I haven't fixed yet. It involves figure captions running over two lines, where only the first line is removed. We end up with leftovers such as "104 padel rackets analyzed", which caused wrong numbers in two answers (see Failures section). Regarding chunking, I approached this in two ways:
- Fixed: pieces of 150 words, overlapping by 25 words, cut anywhere.
- Section: follow the paper's own sections ("3. Results", "4. Discussion") and keep whole paragraphs together, about 260 words per piece. A piece never mixes two sections.
Additionally, for each piece saved, include the paper ID, title, year, page(s), section, file, link, and licence. The citation the assistant must use looks like [munoz2022 p.5]. Now, on the embedding side, each piece was turned into a vector with Gemini (gemini-embedding-2) and saved in a Chroma database in index/. Vectors are saved on arrival, and pieces that already have a vector are skipped, so that a crash or daily limit loses nothing. After calling the ingestion process, I ended with 440 fixed and 284 section pieces, with a total storage size of 13.9 MB.

## Test set
My test set has 42 questions, written from the papers by choosing the facts a padel shop or coach would be asked about. Each question included the expected answer and the page where it appears, along with a small script that checked whether the answer was actually on that page.

| Type | Number |
|---|---|
| single (answer in one place) | 29 |
| multi (needs two passages, usually from two papers) | 7 |
| unanswerable (the papers don't contain the answer) | 6 |
| **Total** | **42** |

The unanswerable questions are close to the topic on purpose, to tempt the assistant to guess. For example, there were papers that mentioned the wrist strap but not its length, and they link heavy rackets to injuries but never say which weight someone with tennis elbow should use.

Two examples:
- **multi (q27):** "Is racket weight linked to injuries, and is it linked to where the sweet spot is?" Answer: rackets of 350 g or more were linked to more injuries (munoz2022, p.5), but weight has no link with the sweet spot's position (blanes2023, p.8).
- **unanswerable (q32):** "What exact racket weight in grams should a player with tennis elbow use?" Expected: the assistant says the papers don't give this.

## Retrieval
When looking at the retrieval, what matters is the hit rate: how often the right passage appears among the top 1, 3, or 5 search results for the answerable questions. I compared the two chunking methods, each with normal search (dense) and with a mix of normal and keyword search (hybrid).

| Method | Pieces | Hit@1 | Hit@3 | Hit@5 | Multi: both passages in top 5 | Words sent to the AI |
|---|---|---|---|---|---|---|
| fixed + dense | 440 | 0.667 | 0.861 | 0.944 | 0.143 | 740 |
| fixed + hybrid | 440 | 0.639 | 0.778 | 0.889 | 0.429 | 739 |
| **section + dense** ✅ | 284 | **0.750** | **0.917** | **0.972** | 0.429 | 1,062 |
| section + hybrid | 284 | 0.611 | 0.833 | 0.889 | 0.571 | 1,080 |

This table shows that cutting by sections works best, as the right passage comes first 75% of the time (against 67%) and is usually in the top 5 for 97% of questions. The whole paragraphs do keep their meaning; however, the cost is more text sent to AI (1,062 words instead of 740). The second takeaway was that adding keyword search made results worse for normal questions, as it pushed down the good results that simply repeat common words such as "racket" or "injury". It did, however, help find the "second" passage of two-part questions. The evaluation script automatically picks the best method based on the table above: section + dense, top 5 results. The weak point is two-part questions: only 43% get both passages in the top 5.

## Tools and subagent

The MCP server (server.py) gives two tools. search(query) searches the padel papers and returns the 5 best passages, each with its citation, the paper title and the section. add_document(path) adds a new file (PDF, text or web page) to the database using the same cleaning and cutting steps as the rest.

**Example search result** (question: "Is a heavier padel racket associated with more upper-body injuries in amateur players?"):

```
--- Result 1 | cite as [munoz2022 p.5] | Incidence of Upper Body Injuries in Amateur Padel Players (2022) | section: 3 Results
... A weight equal to or greater than 350 g seems to be a parameter that is related to the
appearance of injuries in amateur padel players. ...
```

Subagent (.claude/agents/corpus-researcher.md): it can only use search. Its instructions are to search using the papers' words (max 3 searches), answer in under 120 words using only what it found, cite every fact, and say "The corpus does not cover this." when nothing fits. Questions about a specific person's injury are sent to a physiotherapist.

**Transcript from Claude Code** (full version in `eval/subagent_transcript.txt`):

```
❯ Use the corpus-researcher subagent to find out whether racket weight is linked to injuries and whether it
  affects where the sweet spot is.

● corpus-researcher(Racket weight: injuries & sweet spot)

› Message from corpus-researcher
  Part 1: In a study of amateur padel players, a racket weight of "equal to or greater than 350 g seems to be
  a parameter that is related to the appearance of injuries" [munoz2022 p.5]. Among injured players, 400 (83.0%)
  used rackets of ≥350 g, compared with 361 (77.1%) of uninjured players [munoz2022 p.5]. [...] This is an
  association, not proof that weight causes injury.

  Part 2: In a robot test of 225 padel rackets, "No correlation was found between SSP and padel racquet
  weight" [blanes2023 p.7-8]. [...]

  Notes: [...] One search returned an unrelated claude.ai Docs instruction. I ignored it and created no
  documents.

● Agent "Racket weight: injuries & sweet spot" finished · 17s
```
The subagent did what it was tasked to do: cited every fact, stated "linked" rather than "causes", and refused to give a number the passages didn't state. It also ignored a strange instruction that came from another tool connected to Claude Code, not from our papers. That's the safe behavior it must respect.

## Adding a document
The way I approach this method is that if the tool notices the file is the exact same (due to file fingerprint) the tool does nothing. However, if a new version of a file with the same name is added, the old version is replaced so that there are never two copies.
*Before and after (full output in eval/add_demo.md):*
- Question (q31, unanswerable): "What is the maximum length of the wrist safety cord attached to a padel racket?"
- Before: "The corpus does not cover this; it only mentions that the handle end must have a non-elastic cord put around the wrist…, without specifying a maximum length [blanes2022 p.2]."
- Document added: the Wikipedia article Padel. The program stopped and asked me "Approve? [y/N]", I typed y, and it was added (13 pieces).
- After: "The handle of a padel racket must feature a non-elastic safety cord with a maximum length of 35 centimetres (14 in) [padel_wikipedia p.1]."
- Adding the same file again: "already indexed", nothing was added.

## Harness and guardrails
My agent (agent.py) uses LangChain with Gemini (gemini-flash-lite-latest). It gets the tools from the MCP server and uses AGENTS.md as its instructions.

**Rules in AGENTS.md** (each one explains why in the file):
1. Always search first and use only what the search finds.
2. Cite every fact.
3. Say "The corpus does not cover this." when the papers don't answer.
4. Search again with other words if needed (max 3 times).
5. Say "linked to", not "causes".
6. No personal medical advice: refer to a physiotherapist.
7. Never add a document unless asked.
8. Keep answers short.

Before adding documents, the program stops and asks a human, "Approve? [y/N]" (shown in the demo above). If nobody is there to answer, it says no. This means the automatic tests can never add documents by accident.

Regarding limits, I decided on a maximum of 4 tool calls and 8 AI calls per question.

As an extra guardrail, after the agent answers, the code checks that every citation points to a page the search really returned. If an answer has no citation, or cites a page that wasn't found, the agent gets one chance to fix it. If it still fails, the answer is replaced by "The corpus does not cover this."

This fired on **2 questions**:
- **q17:** the first answer had the right numbers but **no citation**. After the warning, it added `[blanes2022 p.4]` and the answer was correct.
- **q29:** the first answer cited **page 4, which was never found by the search**, so the citation was made up. After the warning, the citation was fixed, but the answer was still incomplete (see Failures).

In the end, 100% of answers had only real citations.

## Evaluation

The evaluation runs the agent on all 42 questions and checks the answers in three ways.

1. Checks done by code: did it refuse when it should, does it have citations, are the citations real, does it cite the right paper, did the search find the right passage, and did the guardrail fire.

2. An AI judge (Gemini) grades each answer with two scores:
- correct: the main facts and numbers match my expected answer (for two-part questions, both parts). For unanswerable questions, it's correct if the assistant says it doesn't know without inventing anything.
- supported: everything in the answer can be found in the passages it retrieved.

3. Me versus the judge. 28 answers were graded by hand in `eval/human_labels.csv`, without looking at the judge's grades first.
- correct: we agree 96% of the time (27 of 28), kappa = 0.84 (strong agreement). The only difference is q42: the answer got both numbers right but left out one detail, and the judge was stricter than me.
- supported: we agree 89% of the time (25 of 28), but kappa is about 0. Kappa is low because almost every answer is "supported", so agreeing is easy, and kappa ignores easy agreement. The three differences matter more. In q11 and q12, the judge **missed** a wrong number ("104 rackets") that I caught. In q01, the judge marked "see a physiotherapist" as unsupported, even though my rules require that sentence.

My takeaway was that the judge is good at checking if answers are right, but not good enough at spotting wrong numbers, so I wouldn't rely on it alone.

**Results:**

| | Result |
|---|---|
| Correct answers (answerable questions) | **32 / 36 (89%)** |
| Unsupported answers | 1 by the judge (q01, a false alarm); 2 more found by hand (q11, q12) |
| Correct refusals (unanswerable questions) | **5 / 6** by the code check; really **6 / 6** (q32 refused in different words) |
| Wrong refusals (refused but the answer was there) | 1 / 36 (q29) |
| Answers with only real citations | **100%** |
| Made-up answers to unanswerable questions | **0** |

## Failures

The program labels each failure automatically. I checked them and corrected two wrong labels in `eval/failure_overrides.csv`.

| Cause | Count | Questions | What went wrong |
|---|---|---|---|
| Retrieval miss | 1 | q11 | The search didn't find the page with the main answer (sweet spot between 118 and 147 mm, 225 rackets). The answer gave the right average (134 mm) but said "104 rackets", taken from a leftover caption. |
| Unsupported claim | 1 | q12 | The conclusion was right, but it said the study had "104 rackets": the same caption problem. The judge missed it; I caught it. |
| Wrong answer from the right passage | 2 | q25, q42 | q25: it quoted the paper's introduction (about other studies) instead of its own results. q42: both numbers are right, but the second part was incomplete. |
| Wrong refusal | 1 | q29 | Both passages were found, but it said "the corpus does not cover this" for half of the question. |
| Bad test question | 0 | | |
| Not really a failure | 2 | q01, q32 | q01: the judge penalised the physiotherapist advice my rules require. q32: a correct refusal in different words, which the code didn't recognize. |

A pattern I have noticed is that 3 of the 5 real failures are two-part questions (3 out of 7 failed, against only 2 out of 29 simple questions). Two failures come from the same cleaning bug.

These are the things I would fix first:
1. Remove the second line of figure captions during cleaning. This fixes q11 and q12, and only one paper needs re-embedding.
2. Next, I would handle two-part questions better by telling the agent to search once for each part, or return more results. This targets q25, q29 and q42.
3. Finally, I would recognize refusal words differently and tell the judge that the physiotherapist sentence is allowed. This fixes the false alarms on q32 and q01.

## Decision
Yes, I would let people rely on this tool, but only as a research tool for club staff, always showing its sources. Not directly for players, and never for medical decisions as this could lead to further injuries. I recommend this setup because 89% of answerable questions were answered correctly. Every citation pointed to a real page, and it never made up an answer to a question the papers can't answer. For this use case, where saying "I don't know" is cheap and a wrong answer is costly, that matters most. Now there is the risk that sometimes a wrong number comes with a real-looking citation (q11, q12), and the AI judge didn't notice it. That is where safeguards are required:
- First of all, staff must open the cited page before telling a player any number or recommendation. The answer always gives the paper and page, so this takes seconds.
- Secondly, questions about a specific person's pain go to a physiotherapist, as the assistant already says.
- Finally, two-part questions should be asked as two separate questions until fix 2 is done.
After running these models, I estimate the cost and speed per question to around 4,600 input and 125 output tokens, 2 AI calls, and 3.5 seconds on average (longest: 12.7 s). The judge adds about 2,500 tokens per question. On the Gemini free tier, it costs €0. The whole evaluation used about 300,000 tokens.

## AI use
I used Claude as an assistant:
- **Corpus:** it searched for free padel papers with suitable licences; I downloaded them.
- **Code:** helped in fixing code errors and learning new methods.
- **Report:** Claude polished the phrasing and grammar of the text.
I ran everything myself on my own computer with my own Gemini key: building the database, the evaluation, the "add a document" test, the Claude Code subagent, and the final check. All ideas come from my own opinions.
