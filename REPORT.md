# Assignment 3 Report

- **Name**: Marco Celati
- **Student ID**: 19219
- **Group**: BBADBA 5A

## Use case

The people asking are students who are curious about the possibility of moving to the UK for study reasons. What they do with the answer is evaluate whether or not it's worth the effort of doing it as well as start gathering the information and documents needed or asked for. A confident wrong answer will give the person asking false information which they will act on and believe unquestionably, thereby wasting both time and money, as well as breaking the actual visa conditions upon arriving in the UK. In contrast, an "I don't know" answer would simply send them to the official government source or their university's international office and would only cost a couple minutes of time in checking.

## Corpus

Eight GOV.UK pages on the Student and Graduate routes, all under the Open Government Licence v3.0, with no personal data. They were fetched on 2026-11-24 through the GOV.UK Content API, and that snapshot is committed in `corpus/` so the test set and saved vectors stay valid.

| Source name | Document | Last updated | Words |
|---|---|---|---|
| `student-visa-guide` | [Student visa](https://www.gov.uk/student-visa) | 2024-10-31 | 5,166 |
| `appendix-student` | [Immigration Rules: Appendix Student](https://www.gov.uk/guidance/immigration-rules/immigration-rules-appendix-student) | 2026-10-08 | 8,241 |
| `student-caseworker-guidance` | [Student and Child Student (caseworker guidance)](https://www.gov.uk/government/publications/student-route-caseworker-guidance/student-and-child-student) | 2026-10-16 | 27,013 |
| `graduate-visa-guide` | [Graduate visa](https://www.gov.uk/graduate-visa) | 2024-10-31 | 2,813 |
| `appendix-graduate` | [Immigration Rules Appendix Graduate](https://www.gov.uk/guidance/immigration-rules/immigration-rules-appendix-graduate) | 2026-08-03 | 1,994 |
| `graduate-caseworker-guidance` | [Graduate caseworker guidance](https://www.gov.uk/government/publications/graduate-caseworker-guidance/graduate-caseworker-guidance-accessible-version) | 2026-08-03 | 6,430 |
| `appendix-finance` | [Immigration Rules Appendix Finance](https://www.gov.uk/guidance/immigration-rules/immigration-rules-appendix-finance) | 2025-04-09 | 1,409 |
| `appendix-english-language` | [Immigration Rules Appendix English Language](https://www.gov.uk/guidance/immigration-rules/immigration-rules-appendix-english-language) | 2026-03-26 | 1,643 |
| **Total** | | | **54,709** |

Word counts are after cleaning. The set covers the same rules at three levels: the plain-English guides, the legal rules (numbered paragraphs such as ST 1.2) and the caseworker guidance that explains how officials apply them.

## Ingestion

- Extract: I get each page from the GOV.UK Content API as JSON, so I didn't need to scrape the website. My code goes through the HTML body in order and turns every paragraph, list item and table into a block. Each block remembers which headings it sits under (for example `Money you need > Course fee`) and, for the Immigration Rules, which rule number it belongs to (for example `ST 4.1`).
- Clean: I tidy up the whitespace and HTML entities. I also drop the sections that are about the guidance document itself (Contacts, Publication and Changes from last version), since they don't say anything about the visa rules.
- Extraction problems I had to fix:
  - Joining the HTML tags together left stray spaces in both the text and the headings, so I'd get things like "Confirmation of Acceptance for Studies ( CAS )". I now remove these spaces.
  - 39 blocks turned out to be pure noise. Some were "Official – sensitive: start/end of section" markers and others were stubs saying "the information in this section has been removed", so I drop all of them.
  - GOV.UK writes one rule as "ST26.1", without the space. I changed the rule pattern so it accepts that and stores it as ST 26.1, which means it can be cited like every other rule.
- Chunking (I tried two designs): in both of them, a chunk never goes across two documents.
  - "Fixed" cuts the text into 150-word windows with a 30-word overlap and ignores the structure of the page completely. This gave me 458 chunks.
  - "section" gives each heading its own chunk. If a section is longer than 300 words I split it between blocks, and if it's shorter than 40 words I merge it into the next one. This gave me 402 chunks.
- Metadata on every chunk: each chunk stores its source name, title, URL, location (the rule number or heading where it starts), heading path, every heading and rule number it covers, word count, chunk number, design, and origin (whether it came from the corpus or was added later).
- Embedding and storing: I use `gemini-embedding-2` at 768 dimensions. Before a chunk gets embedded, I add its document title and heading path to the start of it. I embed 20 chunks at a time and save them to ChromaDB (`index/chroma`, cosine distance) after every batch. Each chunk's id is a hash of its design, source and text, so if I run it again, only the new chunks get embedded. I also cache the question vectors in `index/query_vectors.json`.

## Test set

30 questions in `eval/questions.csv`: 8 single, 13 multi, 9 unanswerable. In the two expected columns, `;` separates the passages a multi question needs, and `|` lists the other places where the same fact appears; `testset.py check` verifies every source and location against the documents.

I began simply thinking of questions from the perspective of a student considering studying a master's in the UK. I got Claude to generate different areas and fields to consider, such as accommodation, the payment from the student's parents, work, or technicalities regarding the duration of the visa. Then from those general areas, I came up with much nicher ideas that I would wonder if I were in that situation myself. For instance, a multi example I was able to come up with is Q21 "My parents' savings are in Indian rupees. Which exchange rate is used to check the amount, and how long does the money need to have been in the account?", which needs FIN 1.1 in Appendix Finance for the exchange rate and the Student guide for the 28-day rule. An unanswerable example is Q16, "Does any of my time on Student and Graduate visas count toward indefinite leave to remain?": the appendices say neither route leads to settlement, which sounds like a no, but they never say whether the time counts toward settlement on another route.

## Retrieval

A hit means that a retrieved chunk covers an expected location (any one place for a single question, every needed passage for a multi one). The "words" columns are how many words the top 1, 3 or 5 chunks add to the prompt.

| design | questions | hit@1 | hit@3 | hit@5 | single hit@5 | multi hit@5 | words top1 | top3 | top5 |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 21 | 19% | 38% | 48% | 62% | 38% | 150 | 447 | 747 |
| section | 21 | 14% | 48% | 67% | 75% | 62% | 161 | 472 | 811 |

I chose "section" because although there is a small tradeoff with it performing slightly worse for 1st (14% vs. 19%), it performs much better for top3 (48% vs. 38%) and top5 (67% vs. 48%), and as our agent reads it as long as it is in the top 5, then it doesn't matter whether it is 1st or 5th.

## Tools and subagent

"server.py" exposes two MCP tools; their docstrings are the descriptions the model reads.

- "search(query)": searches the GOV.UK guidance on the Student and Graduate visas and returns the 5 most relevant passages, best first, each starting with a citation label such as "[appendix-student, ST 1.2]", followed by its section, GOV.UK link and text. It also returns the same results as structured data (label, metadata and text), which "agent.py"'s citation check and "evaluate.py" read. The text is in that copy too, because Claude Code shows the model the structured copy rather than the plain text: without it, the first subagent run saw labels but no passages and refused.
- "add_document(path)": adds one local file (.html, .json, .pdf, .md or .txt) to the corpus using "index.py"'s own pipeline ("chunk_file" and "embed_and_store"). It is only to be used when the user explicitly asks.

The subagent (`.claude/agents/corpus-researcher.md`) can use only the search tool. It must search before answering, answer only from the returned passages, cite every claim with its label, and otherwise reply with the refusal sentence.

One search result. "check.py" calling "search" with Q01, "It's been three years since my bachelor's. Will the gap count against me?" (first result, as "check.py" prints it):

```
Result 1: cite as [graduate-caseworker-guidance, Graduate: period to grant]
Graduate caseworker guidance (accessible version) > Grant or refuse > Graduate: period to grant
https://www.gov.uk/government/publications/graduate-caseworker-guidance/graduate-caseworker-guidance-accessible-version
The period of permission to be granted to an applicant is dependent on the type of course studied and the da...
```

"Subagent transcript (Claude Code, 25 November 2026):"

```
> Use the corpus-researcher subagent to answer: Can I work during my master's?

● corpus-researcher(Work rights during master's)
Backgrounded agent (↓ to manage · ctrl+o to expand)

I've asked the corpus-researcher agent to look this up in the GOV.UK documents. It's checking the weekly hour limits for a master's on a Student visa, vacation work, banned types of work, course placements, and whether you can work once the course ends. I'll pass on its cited answer when it finishes.

Waiting for 1 background agent to finish

Agent "Work rights during master's" finished · 24s

Yes, with limits. This assumes you're on a UK Student visa doing a full-time master's at a higher education provider with a track record of compliance (most universities). The answer comes from the corpus-researcher agent's search of the GOV.UK documents.

How much you can work
- During term: up to 20 hours a week [appendix-student, ST 26.1].
- During holidays: full-time, including the period before your course starts [appendix-student, ST 26.1; student-caseworker-guidance, Work conditions].
- Part-time course, or a sponsor that isn't a higher education provider with a track record of compliance: no ordinary jobs. You can only do a work placement that's part of the course, or be a Student Union Sabbatical Officer [appendix-student, ST 26.1; student-caseworker-guidance, Work conditions].

What you can't do [appendix-student, ST 26.1]
- Be self-employed or run a business. The only exception is while an endorsed Innovator Founder application is pending [ST 26.6].
- Work as a professional sportsperson or sports coach. Amateur play or coaching for your university or BUCS in return for a scholarship is allowed [student-caseworker-guidance, Professional sportsperson].
- Work as an entertainer.
- Fill a permanent full-time vacancy.

Work placements: allowed if they're an assessed, integral part of the course. On a degree-level course, a placement can't be longer than half the total course length [appendix-student, ST 26.1, ST 16.1].

After your course ends
- Any time left on your visa counts as outside term, so you can work full-time [student-caseworker-guidance, Work conditions].
- If you apply for a Graduate visa before your Student visa expires, you can start a full-time permanent job once you've completed the course, while the application is being decided [appendix-student, ST 26.6; graduate-visa-guide, When to apply].
- If you apply for a Skilled Worker visa instead, you can start up to 3 months before your course completion date [appendix-student, ST 26.6].

Where your limit is shown: your entry clearance shows "Work limit 20 hrs p/w term time". Permissions granted after 31 October 2024 come as an eVisa, which you check in your UKVI account [student-caseworker-guidance]. The documents don't say whether the work conditions appear on the eVisa itself.

Not in the documents: how a "week" is counted, or how term and vacation dates are set. Your university decides its term dates, so check with them before taking on more hours.
```

The subagent's answer was mostly right, but it got two citations wrong. It said the Innovator Founder exception was ST 26.6 when it's really ST 26.8, and at one point it cited a whole document without saying which part. Nothing caught these because the citation check only works in agent.py, not when the subagent runs in Claude Code.

## Adding a document

Current behaviour ("index.add_document"):
- An unchanged file that is already indexed is skipped, so no quota is spent.
- A changed file with the same name replaces its old chunks.
- A file named like a corpus document is refused, so the core corpus can't be overwritten.

I'm keeping all three rules. Adding the same file again doesn't re-embed anything and just tells the user nothing changed, so it's harmless. The gap is when the same page is saved under a different file name. Then it gets stored twice, and the copies can push other passages out of the top 5. Missed passages were the most common failure in my results, so I'd fix this by checking for duplicate text instead of only the file name. Replacing a changed file matters because GOV.UK pages get updated (the living-cost amounts, for example), and a student shouldn't see the old amount next to the new one. Refusing files named like a corpus document stops someone overwriting one of the eight official documents by accident, which would change what the answers and citations are based on.

Demo, q12 (`uv run python evaluate.py --demo q12 demo_page.html`, saved in `eval/demo_add_document.md`):

Question (unanswerable): My employer isn't a licensed sponsor. Can they get a licence before my Graduate visa runs out, and how long does that take?

Document added: `demo_page.html`

add_document said: Added 'demo-page': 60 chunks, 60 newly embedded, in design 'section'.

Before

> I can't find this in the documents I have.
>
> Please check GOV.UK for official guidance on sponsor licence application processing times and requirements, or speak with an immigration adviser or your employer's HR team.

Citations: none

After

> Yes, your employer can apply for a sponsor licence before your Graduate visa runs out.
>
> Most sponsor licence applications are dealt with in less than 8 weeks, though UK Visas and Immigration (UKVI) may need to visit the business [demo-page, How long it takes to get a decision]. Additionally, your employer may be able to pay an extra £750 to get a decision within 10 working days, though this faster service is limited to a small number of applications each working day on a first-come, first-served basis [demo-page, How long it takes to get a decision].

Citations: [demo-page, How long it takes to get a decision]

Before adding the page, the agent refused q12 with the refusal sentence. After adding GOV.UK's "UK visa sponsorship for employers" guide (saved as demo_page.html and split into 60 chunks), it answered with the under-8-weeks decision time, the possible UKVI visit and the £750 option for a decision within 10 working days, each cited to the new document. Its opening sentence, though, says the employer can get a licence before the Graduate visa runs out, which the page can't support, because that depends on how much time is left on the visa. Adding a document closed the coverage gap, but it didn't stop the agent overstating.

## Harness and guardrails

My agent is in `agent.py`. It's built with LangChain's `create_agent` and runs on Gemini (`gemini-3.5-flash-lite`). It gets its tools from `server.py` over MCP and uses `AGENTS.md` as its system prompt. I also give it today's date, because some of the visa rules depend on dates.

These are the limits and safety checks I set up:

- Whenever the agent tries to use `add_document`, it pauses and asks the user first (this uses LangChain's HumanInTheLoopMiddleware). The user sees which file it wants to add and types y or N in the terminal. If nobody is there to answer, like when the evaluation or `check.py` is running, the answer is automatically no.
- The agent can make at most 6 tool calls and 8 model calls for each question, so it can't keep going forever on one question.
- If `main.py ask` takes longer than 150 seconds, it stops and says why. If a single tool call takes longer than 60 seconds, it's cancelled and the model is told that it failed.
- If I hit Gemini's per-minute limit or there's a server error, it tries again. It doesn't try again if I've used up the daily quota, or if the model has no free quota at all, because retrying straight away wouldn't help.
- I always use the same fixed model version, so the evaluation can be repeated. I picked Flash-Lite because the free tier gives it 500 requests a day, while the full Flash models only get 20, and one evaluation run needs about 150. I didn't use Google's `gemini-flash-latest` alias, because on 25 November 2026 it pointed to a newer model that kept timing out on Google's end. Running `uv run python agent.py --test-models` shows which models are working.
- If the main model fails, `main.py ask` tries `gemini-3.1-flash-lite` next, and then `gemini-3.6-flash`. The last line of the output says which model gave the answer. The evaluation never switches to a backup model, so every graded answer comes from the same model. If it hits a rate limit, it just waits.
- My extra guardrail is a citation check. After the agent answers, I check that every `[source, location]` citation matches a passage that search actually returned during that run. If two citations are written in the same bracket, I check each one separately. Any answer that isn't a refusal also has to cite at least one source. If an answer fails either check, it's replaced with the refusal sentence, but I keep the blocked draft in the trace so I can see what went wrong.

These are my four rules in `AGENTS.md` and why I chose each one:

1. Search before answering. If the first search doesn't find the answer, try again with other words. Why: visa rules have exact dates and amounts, and the agent's memory could be wrong or old.
2. Only use what the search found. Don't guess. If the answer depends on something the student didn't say, tell them what it depends on. Why: the student can't tell a guess apart from a real rule.
3. Give a source for everything, using the exact label, for example [appendix-student, ST 26.1]. Why: the student can check it on GOV.UK before spending money.
4. Say so when the documents don't have the answer. Start with "I can't find this in the documents I have." and tell them where to check. If only part of the question is answered, answer that part and say the rest isn't covered. Something that's only close to the question doesn't count as an answer. Why: "I don't know" is safe, but a confident wrong answer isn't.

The citation check stopped an answer once. The first time I asked "Can I work during my master's?", the agent gave a correct answer and cited [appendix-student, ST 26.1]. But GOV.UK writes that rule as "ST26.1", with no space, so the system didn't recognise it as a rule and blocked the answer. This got fixed in the Ingestion step.

## Evaluation

`main.py evaluate` runs the agent on all 30 questions and checks in code:
- refusals, by the exact refusal sentence
- whether every citation is one that search returned
- whether the agent's own searches found the expected passage

Answers are cached, so a run stopped by the daily quota carries on where it left off; an answer whose searches all failed is not counted and runs again next time.

An LLM judge (`gemini-3.1-flash-lite`, a different model from the agent's, so it isn't grading its own answers) then grades each answer with the rubric in `eval/judge_rubric.md`, using the question, the reference answer and the retrieved text, and returns `correct`, `supported` and a reason. Agreement with my own grades (`eval/human_labels.csv`) is reported as a percentage and Cohen's kappa.

The first judge run marked three correct refusals (q12, q13, q15) wrong because the rubric didn't allow the where-to-check line that AGENTS.md asks for. I clarified the rubric and re-ran the judge. First run: 87% agreement on correct, kappa 0.63. Second run: 97% agreement on correct, kappa 0.89.

An answer counts as correct if it matches my reference answer on every part, including amounts, dates and conditions. It counts as supported if everything it says is in the passages search found. For unanswerable questions, only a refusal counts as correct.

| outcome | single | multi | unanswerable | total |
|---|---|---|---|---|
| correct | 7 | 9 | 0 | 16 |
| incorrect | 0 | 3 | 0 | 3 |
| unsupported | 0 | 1 | 0 | 1 |
| wrong refusal | 1 | 0 | 0 | 1 |
| correct refusal | 0 | 0 | 9 | 9 |

The agent got 16 of the 21 answerable questions right and refused all 9 unanswerable ones correctly. The judge agreed with my grades 97% of the time on correct (kappa: 0.89) and 93% on supported (kappa: 0.47). It was too easy on three answers I failed: q28, q09 and q23.

## Failures

Seven answers failed: five caught by both the judge and my grades, and two (q09, q28) only by my grades.

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 3 | q06, q11, q28 |
| Unsupported claim | 2 | q09, q26 |
| Wrong refusal | 1 | q01 |
| Wrong answer from the right passage | 1 | q23 |
| Bad test question | 0 | none |

Retrieval misses are the largest group, and all three follow the same pattern. The agent found the passage for the first part of a multi-part question, answered from it, and never retrieved the passage holding the second part: the timing rules for Q06, the requirement that the Student visa still be valid for Q11, and the link between application date and visa length for Q28. Its answers read as complete, so nothing signals the gap to the student. This matches the retrieval numbers: with the section design, hit@5 is 75% for single questions but 62% for multi.

Both unsupported claims add a rule the passages don't contain. In Q26 the agent filled a gap (whether delivery riders are employees) with general knowledge, turning a conditional answer into a flat no. In Q9 it invented an exception for work placements. The wrong refusal, Q1, is the other side of the agent's caution: it had the right passage but refused anyway, probably because rule 4 says related background doesn't count as an answer. The same caution got all nine unanswerable questions right. Q23 is a plain arithmetic slip.

No failure came from a bad test question, but writing the test set exposed weaknesses that I fixed or noted. I revised two references (Q02, Q07) after grading because the Student guide or caseworker guidance disagreed with Appendix Student. And q11's alternative locations for its second part weren't equivalent, since only one of them contains the rule that you must apply before your Student visa expires.

What to fix first: retrieval for multi-part questions, because it's the most common cause and the hardest for a student to spot. The simplest change is to rule 1: have the agent run a separate search for each part of the question and check that every part is covered before answering. After that, I'd loosen rule 4's related-background line and re-check q01 against the traps it currently refuses correctly.


## Decision

Yes, I'd let students rely on it but solely as a starting point. It's good at simple questions and at saying when it doesn't know, but it got 4 of the 13 multi-part questions wrong, and those wrong answers still sounded very sure of themselves and quite convincing. So students should always open the GOV.UK page it cites and check it before paying for anything or applying. Each question takes about 14 seconds, 3.1 model calls and 8,148 input + 216 output tokens, plus about 2,800 tokens for the judge.


## AI use

I used Claude to write parts of the code, as well as to brainstorm various ideas, for instance for the 30 questions, as I wrote earlier in the report, I got Claude to create the general areas that one would be concerned about if applying to do a UK master's, and used that base to come up with the question ideas myself. I also used it when selecting between different topics at the beginning of starting to work on this assignment, where it was very useful in comparing different topics and seeing how easily feasible each idea was. I also used AI in order to work on ensuring the formatting was good and that there wasn't any small grammatical mistakes.