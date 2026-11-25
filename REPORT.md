# Assignment 3 Report

- **Name**: Julián Consuegra
- **Student ID**: 19376
- **Group**: BBADBA 5A 

## Use case

This tool is meant to be used by startup founders that are considering applying for the EIC Accelerator (the EU's funding program for startups and SMEs under its 2027 Work Programme). Since there are many criteria that have to be taken into account in order to assess eligibility, it is of great use to develop this tool to answer questions in relation to this matter. Answers provided will help founders determine if they are eligible for funding, clarify deadlines when completing the application and understand the rules for different funding amounts. It will be a useful tool that aims to answer questions from the official EIC documents that founders can check and act upon. Sometimes the tool will not be sure about the answers to a question. There are two possible outcomes: Confidently giving a wrong answer or directly stating "I don't know". In the first scenario, a wrong answer would probably mean missing important deadlines, misleading founders into believing they are eligible for the grant when they're actually not, or wasting weeks of work in an application that was not valid in the first place. On the other hand, responding with a direct "I don't know" will most likely make the founder double check with an alternative source before taking action. This would represent less of a risk as it is a genuine response that avoids pursuing a plan under uncertain assumptions. Taking this into account, the tool should only answer when the documents support it, and otherwise say it doesn't know. 

## Corpus

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| EIC Work Programme 2027 (Commission Decision C(2026)7629) | [link](https://eic.ec.europa.eu/document/download/ed9ab103-1ffb-4d5f-a6ad-168ac3b36900_en?filename=EIC-2027-Work-Programme.pdf) | 5 Nov 2026 | Commission reuse policy (Decision 2011/833/EU), reuse allowed with source acknowledged | ~75,500 |
| EIC Accelerator Guide for Applicants, v6.0 | [link](https://eic.ec.europa.eu/document/download/9d96fbf3-4d85-4ad0-9483-c77ce348111d_en?filename=EIC%20Accelerator%20guide%20for%20applicants_WP26.pdf) | 19 Nov 2025 | Commission reuse policy (Decision 2011/833/EU), stated in the document | ~8,000 |
| EIC Fund Investment Guidelines (Horizon Europe Compartment) | [link](https://eic.ec.europa.eu/document/download/6df458e7-fa47-4ace-93fa-86099606bdb0_en?filename=EIC_Fund_Investment_2026_guidelines_f.pdf) | Aug 2026 | Commission reuse policy (Decision 2011/833/EU) | ~8,300 |
| **Total** | | | | **~91,800** |

All three are public documents from the official EIC website and contain no personal data. The Guide for Applicants was written for the 2026 Work Programme (it is the latest version available), so some details may not match the 2027 rules.


## Ingestion

Extraction is done page by page from the chosen PDFs with `pypdf`, while keeping the page number. There were certain cleaning steps in order to only maintain necessary information that is of value for the use of the tool. For example, the Guide's repeated page header was removed, lone page numbers and table of contents lines were removed, and pages that had less than 20 words were skipped (covers, blank pages). The chunks are composed of 200 words with a 40-word overlap, never crossing a page. I used a single chunk size on purpose, to stay within the 1,000-embeddings-a-day limit, and compared two search methods instead, since that needs no extra embeddings.

In the process of extraction I faced a problem that might seem simple at first glance but had to be addressed in order to capture the real meaning of words. The PDFs include some words with stray spaces such as "high -risk" and "co -investment" (38 cases in the Work Programme and 9 in the Investment Guidelines). As seen, there is an extra space just before the hyphen and it could end up being interpreted as two separate pieces. For key processes such as keyword search, this can be critical as it may miss matches due to these slight errors. I fixed this in the cleaning step by removing the space before the hyphen, so the search now sees the actual words. 

To maintain traceability and identify sources, each chunk stores its document (source), document title, page number and word count as metadata. Each chunk also gets a unique ID built from the document, page and chunk number, for example `work_programme_2027-p031-c2`. 

Following the specifications of chunk size, word overlap and no page crossing, I ended up with a total of 631 chunks within my index. They are divided into the three documents: 516 Work Programme, 59 Guide, 56 Investment Guidelines. They were then embedded with gemini-embedding-2 at 768 dimensions. 



## Test set

I began thinking on basic common questions that a startup founder could come across when evaluating if they can benefit from a grant. Evidently, the questions were formulated in a way that answers come from information available in the corpus. Also, the wording in which questions are asked was something I paid close attention to and worth noting. The documents are filled with official EIC terms that may be complex or unheard of for the common person. Due to this, I decided to generate a mix of questions in which some followed a wording that included EIC terminology but others (8 out of 37) were formulated more naturally and with everyday wording that founders could use so the search is tested with both kinds of wording.

In total there are 37 questions. There are three kinds of test questions: Single (24), multi (7) and unanswerable (6). For the single questions, there is one passage in the corpus that answers them in a simple and concise manner. This is the most basic type and usually the easiest approach the tool has to generate answers. Additionally, the multi questions require two passages for formulating an answer that can be found in different pages or documents. The tool has to find the appropriate passages and combine them, requiring more effort and increased complexity compared to single questions. This can be seen usually when a single page alone can't fully answer the question. Finally, unanswerable questions are ones that can't be answered with the information available in the corpus. These are included in order to assess the capability the tool has to deal with these situations and prevent it from giving false information instead of genuinely responding "I don't know". 

Below are examples of each type of question based on the explanations given above.

1. Single Question (Q12): “What score does my full proposal need to be considered for an interview?” 
**Answer:** 4/5 per criterion and 13/15 overall (WP p85, Guide p21).

2. Multi Question (Q25): “The guide says I need TRL 6, but what TRL level does my innovation actually need to have reached when I apply?”
**TRL: Technology Readiness Level. Scale from 1-9 of how mature a technology is.**

**Answer:** TRL 5 must be fully completed (validation in a relevant environment), which the Guide describes as TRL 6 or above.
**Sources:** Guide p6 (TRL 6 or above) + Work Programme p85 (all aspects of TRL 5 completed).

3. Unanswerable Question (Q36): “What are the EIC Accelerator cut-off dates for 2028?”
**Expected Answer:** The assistant should say it doesn’t know the 2028 dates.
**Sources**: None. The documents only give the 2027 cut-offs.

## Retrieval

For the retrieval I focused on and tested two designs: vector search and hybrid search. Vector search is the approach in which questions are turned into number embeddings that capture meaning and the search returns chunks within the corpus that have similar embeddings. Words included in the questions may differ to those used in the answers but their captured meaning is similar under this approach. On the other hand, the hybrid search uses both vector search and keyword search. Keyword search ranks chunks within the corpus depending on how many keywords used in the questions match those in the documents. Rarer words count more, so a match including "TRL" will matter more than one with "grant" which is seen everywhere. This is combined with vector search explained above, and the chunks that rank high under either method come first. Both designs use the same 631 chunks, so the comparison needed no extra embeddings. 

Before including the table with results it is important to clarify what hit@k or hit rate represent under my scenario. This metric reflects the share of answerable questions for which a chunk from an expected page appears in the top k results. 

| Design | hit@1 | hit@3 | hit@5 | Words in top 5 |
|---|---|---|---|---|
| A: vector (after fix) | 0.55 | 0.84 | 0.97 | ~790 |
| B: hybrid (after fix) | 0.45 | 0.71 | 0.84 | ~804 |
| A: vector (before fix) | 0.39 | 0.68 | 0.81 | ~790 |
| B: hybrid (before fix) | 0.39 | 0.58 | 0.68 | ~804 |


Overall, the results were positive and the pages which included answer chunks were consistently placed among the top results. Before delving into details, it is worth highlighting the fix I made to my test labels, which explains the difference between the before and after rows of the table. 

Each question has a label which is the page(s) where I initially stated the answer was. However, considering there is some repeated information throughout the different documents, one answer can appear more than once in different pages. The initial problem was that there were 6 specific cases in which the search returned a correct page number which did contain the correct answer, but it was still marked as wrong. This occurred because the page number it returned didn't coincide with the "correct" page number that was initially established without considering the fact that the same information could also be elsewhere. After identifying this problem, the labels were modified in order to take into account the correct pages that were not considered at first. By doing so, these 6 searches are now correctly marked as hits. The fix did not change the search itself, it made the measurement fair: the first numbers underestimated it. Vector search wins both before and after the fix, so the fix does not change my decision. 

The hit rate drastically improves from 1 to 5 but since the agent reads the top 5 chunks, hit@5 will be the most useful and applicable in my case. Using the top 5 chunks adds about 790 words to the prompt for each question. I accepted this cost because going from top 1 to top 5 raises the hit rate from 0.55 to 0.97. Both vector and hybrid hit@5 have high values (0.97 and 0.84) meaning that for 97% (vector) and 84% (hybrid) of the answerable questions, a correct page was among the first 5 results. The same interpretation can be used for the other hit rates. However, considering that the vector search outperformed hybrid at 1, 3 and 5, I decided to choose this approach. Hybrid search most likely did worse because words like "grant", "proposal" and "EIC" appear on almost every page, so the keyword search pulled in many off-topic pages and pushed correct ones down the ranking.

The weak spot is the multi questions. For the 7 multi questions, both needed passages were in the top 5 for only 2 of them (29%). A single search usually finds one half of the answer, so the agent may need to search more than once. 

Note: these numbers were measured before I added the NEOTEC document (see Adding a document). Re-running the retrieval comparison on the final index (742 chunks) gives exactly the same results for vector search, while hybrid search changes slightly (0.45 / 0.68 / 0.87), because keyword scores depend on all the documents in the index. The decision does not change.


## Tools and subagent

### Tool descriptions

These are the docstrings in `server.py`, which is the exact text the model reads when it decides which tool to use.

**search(query)**

```
Search the official EIC Accelerator documents: the EIC Work Programme 2027,
the EIC Accelerator Guide for Applicants and the EIC Fund Investment Guidelines.
Use it for any question about EIC Accelerator funding: eligibility, grant and
investment amounts, deadlines and cut-off dates, the application steps, evaluation
and interviews, and how the EIC Fund invests.

Returns the 5 most relevant passages, each with its document title and page number.
Answer only from these passages and cite them as (document title, p. N). If none of
them answers the question, search again with different words or say the documents
do not cover it. For a question with two parts, search once for each part.
```

**add_document(path)**

```
Add a new PDF document to the searchable collection. Give the full path to a
PDF file on this computer. The file is extracted, cleaned, cut into chunks, embedded
and stored, so the search tool can find it straight away.

If the document is already in the index (same file name, or one of the corpus
documents), nothing is added: no duplicates and no embedding cost. Returns how many
chunks were added.
```

I wrote the search description so the model knows what the documents cover, when to use the tool, and how to cite the results (document title and page). It also tells the model to search once for each part of a two-part question, because the retrieval comparison showed that one search usually only finds one half of a multi question. The add_document description says what the tool does and that a document already in the index is not added again, so there are no duplicates and no wasted embedding quota.

### One search result

Query (q13): "We've been rejected twice already. Is there a limit to how many times we can try again?" (texts shortened)

```
[1] EIC Work Programme 2027, p. 112 – ...Investment leverage: Does the proposal provide a convincing and real...
[2] EIC Work Programme 2027, p. 82 – ...the EIC Fund will re-examine the due diligence once the defined milestone has been achieved...
[3] EIC Work Programme 2027, p. 112 – ...an applicant may not apply again to the EIC STEP Scale Up or STEP Defence call under the Horizon Europe Framework Programme...
[4] EIC Accelerator Guide for Applicants v6.0, p. 49 – ...Submission limits: After three unsuccessful submissions to the EIC Accelerator, which can be at any stage...
[5] EIC Work Programme 2027, p. 31 – ...You will be informed about the outcome of the Stage 1 evaluation within 3 months...
```

The passage that answers the question (Guide p. 49) is in the results, but only at rank 4. Rank 3 is a very similar rule for a different call (STEP Scale Up), so the agent has to read carefully to pick the right one. This matches the retrieval numbers: the right page is usually somewhere in the top 5 (hit@5 = 0.97) but often not first (hit@1 = 0.55).

### Subagent instructions

The subagent is in `.claude/agents/corpus-researcher.md`. Its `tools:` line is `mcp__corpus__search`, so it can only use the search tool and cannot add documents. Its instructions:

```
You answer questions from startup founders about the EIC Accelerator, using only the
official EIC documents in the corpus (EIC Work Programme 2027, EIC Accelerator Guide
for Applicants, EIC Fund Investment Guidelines).

How to work:
1. Search the corpus with the search tool. Use only the search tool.
2. If the question has two parts (for example a rule and an amount), search once for each part.
3. If the first results do not answer the question, search once more with different words.
4. Answer only from the passages the search returned. Do not use your own knowledge.

How to reply:
- A short, direct answer (a few sentences at most).
- Cite every claim as (document title, p. N), using the title and page shown in the search results.
- If the passages do not answer the question, reply: "The EIC documents I have do not cover this." Then say briefly what they do cover, if anything related. Never guess numbers, dates or rules.
```

### Transcript from my editor (Claude Code in VS Code)

```
Use the corpus-researcher subagent to answer: We've been rejected twice already. Is there a limit to how many times we can try again?
Agent:EIC resubmission limits
IN
Answer this user question from the EIC Accelerator documents: "We've been rejected twice already. Is there a limit to how many times we can try again?" Cover resubmission rules after rejection (e.g., limits on resubmitting after failing at short proposal or full proposal/interview stage, any blocking/waiting periods, and whether rejections at different stages count differently). Cite the source documents and quote key passages. Note clearly if the corpus doesn't address something.
 Finished · type /tasks to see its transcript
2:51 PM
I've passed your question to the corpus-researcher agent. It's searching the EIC documents for the rules on resubmitting after a rejection: whether there's a cap, whether there are waiting periods, and whether a rejection counts differently depending on the stage it happened at. I'll give you the answer with citations once it finishes.


2:52 PM
Yes, there's a limit, and you have one try left. After three unsuccessful submissions to the EIC Accelerator, the same legal entity can't apply again for the rest of Horizon Europe.

Every stage counts the same. A rejection at the short proposal or the full proposal stage counts towards the three. The interview is part of the full proposal stage, so a rejection there counts too. It also doesn't matter whether you applied through Open or a Challenge, or for a grant only, blended finance or equity only (EIC Work Programme 2027, p. 88; Guide for Applicants v6.0, p. 49).
Only rejections since 1 January 2024 count. If either of your two rejections came before that date, you may have more attempts left than you think (WP 2027, p. 88).
Fast Track and Plug In entries count too (WP 2027, p. 88).
Withdrawing doesn't count. If you withdraw before you get the evaluation result, that submission isn't counted against the limit (Guide v6.0, p. 45). That could protect your last attempt if you realise mid-process that the proposal isn't ready.
You're expected to improve the proposal. Reapply only after acting on the evaluators' feedback and making significant improvements (WP 2027, p. 88).
The documents don't cover a few things:

whether you have to wait a minimum time before resubmitting
whether a rejection at the full proposal stage means starting again with a new short proposal
whether the limit resets under the next EU research programme after Horizon Europe
If you were rejected after the interview, you should also have received a Seal of Excellence (Guide v6.0, p. 55). It can help you seek other funding.
```

## Adding a document

To prevent duplicates and wasting embedding quota, when a document is already indexed it can't be added again. The 'add_document' tool responds that the document is already indexed to ensure the proper organization of information.

In order to test out the 'add_document' tool, I chose an unanswerable question that required extra information that was not originally included, and recorded the answer given by the agent before and after adding extra chunks to the index. The chosen question was Q35: “How much funding does the Spanish CDTI NEOTEC programme give to startups?”. Original documents contained information about the EU's EIC Accelerator, but this question was related to the Spanish CDTI NEOTEC programme which was not covered in the corpus. Due to this, the agent’s answer before adding the document was: "The EIC documents I have do not cover this. They do not contain information about the Spanish CDTI NEOTEC programme." I proceeded to download the NEOTEC official document (the NEOTEC 2026 call, a CDTI resolution of 6 April 2026, 43 pages, in Spanish) and saved it in the corpus folder. Then, a request was sent to the agent in order to index the information and I had to approve this action (human-in-the-loop) before it was embedded and ready to use. The document was added as 111 chunks, which took the index from 631 to 742 chunks. Once the new chunks were added, the same question was asked again and the response is now: 

"Under the CDTI NEOTEC programme, the funding consists of grants with the following limits:

* **General limit:** Up to 70% of the eligible budget can be funded, with a maximum grant amount of **€250,000** per beneficiary entity (convocatoria_neotec_2026, p. 7).
* **With PhD hire:** If the project includes hiring at least one PhD holder, up to 85% of the eligible budget can be funded, with a maximum grant amount of **€325,000** per beneficiary entity (convocatoria_neotec_2026, p. 7).
* **Additional training:** An extra amount of up to €18,300 can be added for specific international training activities at institutions like MIT or GeorgiaTech (convocatoria_neotec_2026, p. 7).
* **Project budget limits:** The minimum eligible project budget is €175,000, and the maximum is €750,000 (excluding the optional training costs) (convocatoria_neotec_2026, p. 7).

Sources:
- convocatoria_neotec_2026, p. 7"

Evidently, the agent successfully communicated with the 'add_document' tool, the approval step followed as expected, the extra chunks were added, and the answer now responds to the question that was originally unanswerable. Even though the question was in English and the document in Spanish, the search still found the right page. I checked the answer against the PDF: all the numbers are correct and on page 7, but the detail about MIT or GeorgiaTech is actually on page 32, not page 7. The citation guardrail does not catch this, because it only checks that every cited page was retrieved, not that each claim is on that exact page. Because the index now includes the NEOTEC document, q35 is no longer unanswerable; the end-to-end evaluation in the next sections was run before I added it.

## Harness and guardrails

### AGENTS.md rules

`agent.py` sends `AGENTS.md` as the system prompt, and the editor's agent reads the same file. Each rule comes with its reason:

> You help startup founders with questions about applying to the EIC Accelerator. You have a
> search tool over three official EIC documents: the EIC Work Programme 2027, the EIC Accelerator
> Guide for Applicants (v6.0) and the EIC Fund Investment Guidelines (August 2026).
>
> 1. **Search before answering, every time.** Reason: the rules change every year and you do not
>    reliably know the 2027 rules, so your memory is not a source.
> 2. **Answer only from the passages the search returned.** Do not add facts, numbers or dates from
>    your own knowledge, even if you think they are right. Reason: a founder will act on the answer
>    (apply, plan a deadline, ask for an amount), and an invented detail can cost them weeks of work.
> 3. **Cite every claim as (document title, p. N)**, using the exact title and page shown in the search
>    results, for example (EIC Work Programme 2027, p. 88). Reason: the founder must be able to check
>    the source before acting on it.
> 4. **For a question with two parts, search once for each part**, and search again with different
>    words if the first results do not answer the question. Reason: one search usually finds only one
>    side of a two-part question.
> 5. **If the passages do not answer the question, start your reply with exactly:
>    "The EIC documents I have do not cover this."** Then, in one sentence, say what related
>    information they do contain, if any. Never guess. Reason: for this use case "I don't know" is
>    cheap (the founder checks elsewhere) and a wrong answer is expensive.
> 6. **If the documents only partly answer the question, answer that part with citations and say
>    clearly which part they do not cover.** Reason: a partial answer is useful, as long as the gap
>    is visible.
> 7. **Only use the add-document tool when the user explicitly asks to add a specific file.** Reason:
>    adding a document changes what every later answer is based on, so it needs the user's approval.
> 8. **Keep answers short and in plain language**: a few sentences or a short list. Reason: founders
>    want a clear answer they can act on, not a summary of the documents.

### Approval step

The add_document tool never runs without my approval. In `agent.py`, LangChain's human-in-the-loop middleware pauses the agent right before it calls add_document and asks in the terminal. Only a "y" lets it continue; anything else rejects the call, and the agent is told the user did not approve. During the evaluation nobody can answer, so the answer is always "no". This is the real run from adding the NEOTEC document:

```
The agent wants to run add_document with {'path': '.../corpus/convocatoria_neotec_2026.pdf'}.
Approve? [y/N] y
  embedded and saved 20/111 chunks
  ...
  embedded and saved 111/111 chunks
```

The harness also has call limits: at most 4 tool calls and 6 model calls per question, so a confused agent cannot loop and use up the free quota. If Gemini is overloaded (error 503), the agent waits and retries, and then switches to a backup model. I added this after my first test kept failing with "model overloaded". The main model is `gemini-flash-lite-latest` and the backup is `gemini-flash-latest`.

### Extra guardrail: citation check

The guardrail I chose checks the citations in code after the agent answers and before the user sees it. Every (document, p. N) in the answer must be a page that the search actually returned in that run, and an answer that is not a refusal must have at least one citation. If not, the answer is withheld and replaced with "The EIC documents I have do not cover this.", plus a short note on why. I chose this because in my use case a founder must be able to check every claim against the real page, so an answer citing a page the agent never read should not reach them.

**A case where it fired (q25, the TRL question).** The agent's draft cited "EIC Work Programme 2027, p. 73", but the search had returned p. 72, not p. 73, so the guardrail blocked the answer and the founder got a refusal. The rest of the draft was actually right (TRL 5 must be completed, Guide p. 20). So this case shows the trade-off of the guardrail: it is strict, and it can turn a mostly correct answer into "I don't know". For this use case I think that is the right side to fail on, because a refusal only costs the founder a check elsewhere.

**What I learned from testing it.** At first the guardrail also fired when it should not have: it did not recognise citations whose title had brackets in it ("EIC Fund Investment Guidelines (August 2026)"), it blocked the confirmation message after adding a document (which has no citations), and it did not recognise the title of the added document because it starts with a lowercase letter (`convocatoria_neotec_2026`). I fixed all three. It also has a limit: it checks that each cited page was retrieved, not that each claim is really on that exact page. In the NEOTEC answer, the detail about MIT and GeorgiaTech was cited to p. 7 but is actually on p. 32, and the guardrail did not catch it.

## Evaluation

I ran the agent on all 37 questions with `uv run python main.py evaluate`. Each answer is saved in `eval/answers.csv`, the judge's verdicts in `eval/judge_verdicts.csv`, my grades in `eval/human_labels.csv`, and the totals in `eval/summary.csv`.

### Code checks

Some things can be checked in code, without an LLM:

- **Refusal:** does the answer start with "The EIC documents I have do not cover this."? For unanswerable questions a refusal is correct; for answerable ones it is a wrong refusal. Refusals are graded only in code, because they make no claims.
- **Valid citations:** the citation guardrail checks that every cited page was returned by the search in that run.
- **Cites an expected page:** does the answer cite at least one of the pages listed for that question in `questions.csv`?

### The judge's rubric

The answers that are not refusals (30 of them) were graded by a separate Gemini call. The judge gets the question, my reference answer, the passages the agent retrieved, and the agent's answer, and gives two grades:

1. **correct (1/0):** the answer gives the same key facts as the reference (numbers, dates, conditions) and nothing contradicts it. Extra correct detail is fine; a wrong number, a missing main point or a contradiction is 0.
2. **supported (1/0):** every factual claim in the answer is stated in the retrieved passages. A claim that is not in the passages is 0, even if it is true.

It replies in JSON with both grades and a one-sentence reason. I asked for `gemini-flash-latest` as the judge, but its daily free quota ran out, so most verdicts came from `gemini-flash-lite-latest`, the same model the agent uses.

### Agreement with the judge

I graded all 37 answers myself in `eval/human_labels.csv` (correct, supported, and a note for every 0) before looking at the judge's verdicts. I agreed with the judge on 100% of them, both for correct and for supported. This looks very good, but I don't think it proves much about the judge. Almost every answer was clearly right, so there were very few hard cases where we could disagree, and the judge never had to mark a wrong answer. It is also mostly the same model as the agent, so it may share the same blind spots. A fairer test would need more questions, including some deliberately wrong answers.

### Results

| Result | Count |
|---|---|
| Correct, all questions | 36 / 37 (97%) |
| Correct answers (answerable questions) | 30 / 31 |
| Unsupported answers (a claim not in the passages) | 0 |
| Correct refusals (unanswerable questions) | 6 / 6 |
| Wrong refusals (answerable questions) | 1 / 31 (q25, blocked by the guardrail) |
| Answers citing an expected page | 30 / 31 |
| Guardrail fired | 1 |

Cost per question, on average: 1.5 searches, about 4,400 input tokens and 170 output tokens, and 8.8 seconds.

The evaluation also found two bugs in my own system on the first run (kept in `eval/run1_buggy/`). The agent sometimes ran two searches at the same time and both wrote to the question-embedding cache, which damaged the file, so from question 31 every search failed and the "refusals" for q33–q37 only happened because search was broken. Also, the guardrail wrongly blocked four correct answers because one document title has brackets in it ("(August 2026)"). I fixed both and ran the whole evaluation again; the results above are from the second run.

## Failures

I classified every failure using the five categories from the brief: retrieval miss, wrong answer from the right passage, unsupported claim, wrong refusal, or bad test question.

| Failure | Cause | Count |
|---|---|---|
| q25 (TRL): the draft was mostly right, but it cited WP p. 73 while the search had returned p. 72, so the citation guardrail blocked it | Wrong refusal | 1 |
| Expected pages too narrow: the same answer was also on another page (usually both in the Work Programme and the Guide), so the search was marked wrong when it was right (q01, q02, q04, q09, q12, q13; found in the retrieval step and fixed) | Bad test question | 6 |
| NEOTEC demo (outside the test set): the detail about MIT and GeorgiaTech was cited to p. 7 but is actually on p. 32 | Unsupported claim (wrong page cited) | 1 |
| Retrieval misses and wrong answers from the right passage | none in the final run | 0 |

In the final run only one of the 37 questions failed, and it failed on the safe side: the founder got "I don't know" instead of a wrong answer. The bad test questions were my own mistake when labelling, not the system's, and once fixed they no longer count as failures. The two bugs found in the first run (the damaged cache and the guardrail not reading titles with brackets) were problems in my code, which I fixed before the final run.

**What to fix first:** the guardrail's all-or-nothing behaviour. Right now, if the answer cites one page that was not retrieved, the whole answer is replaced with a refusal. A better version would give the agent one more try ("you cited a page you did not retrieve; answer again using only the retrieved pages") before refusing. That would most likely have saved q25 without letting invented citations through. The second fix would be to check that each claim is really on the cited page, not only that the page was retrieved, which would have caught the MIT/GeorgiaTech case.

## Decision

After initial trial and understanding on how the tool works, I would comfortably let startup founders use this for general understanding on basic yet necessary information regarding the process of receiving grants.  The information comes from official sources and it is presented to the user in a concise manner in which it is easy to understand and proper citing is included in order to ensure credibility. The safeguards already incorporated are meant to protect the user from receiving wrong answers. However, it should not be the final word for important decisions such as submitting an application or deciding how much funding to ask for. For those, founders should confirm the information on the cited page or on the official EIC website. This decision is based on the evaluation: 36 of 37 questions were handled correctly, no answer made a claim that wasn’t in the documents, and all 6 unanswerable questions were correctly refused. Still, 37 questions is a small test, so the results should be confirmed with more questions before relying on it more widely.

 In terms of safeguards, always showing the cited page and keeping the citation guardrail with the small fix mentioned above, will allow the user to understand where the information is coming from and double-check if considered necessary. Also, it is important to note that the documents included in the corpus contain specific information from 2027, so including a reminder that information is updated every year is a necessary safeguard for future use. In relation to this, human approval for adding new documents will be maintained to ensure the integrity of information and only add documents that contain information for future years or cover a new spectrum in relation to grants that was not yet considered. 

 On average, each question uses about 4,400 input tokens and 170 output tokens and takes about 9 seconds to answer. Most of the input is the retrieved passages, which are sent to the model again each time it is called. At the published prices for gemini-flash-lite-latest ($0.30 per million input tokens and $2.50 per million output tokens), this is roughly $0.002 per question, and it was free on the free tier I used. This cost is very low compared to the weeks of work a wrong answer could waste for a founder.



## AI use

I used Claude to explain key terms, suggest relevant topics, write the code, and draft the test set and certain parts of the report. I ran and tested all the code, reviewed and edited the test set and the drafts, wrote the remaining sections, and graded all 37 answers myself. The decisions (use case, design choice, guardrail and whether to rely on the tool) are my own.