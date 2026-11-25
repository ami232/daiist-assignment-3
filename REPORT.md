# Assignment 3 Report

- **Name**: Moritz Hanbuch
- **Student ID**: 19140
- **Group**: BBADBA 5A

## Use case

For this assignment I chose a use case from the property management sector in Germany. My father works in this sector, and hence I had often heard from him that general AI is not very good at niche questions in his field. When he has a question about service charges that he cannot answer himself, he first searches online, then asks a general AI, and only if that does not help does he ask a lawyer or another expert. In his experience the AI often gave wrong answers, and since it gives no sources, he cannot tell which answers are right. This is the step my system is built for. The user is a property manager or landlord who wants to know if a cost can be passed on to the tenants in the service charge statement (Nebenkostenabrechnung).

A wrong answer can cost money in three ways:
- a single cost cannot be recovered from the tenant
- the whole statement can be invalid
- the back payment is lost if the deadline is missed

Saying "I don't know" only costs the fee for a lawyer, so I decided the assistant should say so rather than guess.

## Corpus

For the corpus I combined the German laws on service charges with court decisions from the Federal Court of Justice (BGH). I did this because the laws only list which costs exist, while the court decisions decide the difficult cases, which is where a general AI usually goes wrong. All texts are official works under § 5 UrhG, so I am allowed to reuse them, and they contain no personal data. I held back one decision so I could use it later for the add-document demo.

| Document | Source | Date / version | Words | Chunks | Licence |
|---|---|---|---|---|---|
| BGB §§ 535–580a | [gesetze-im-internet.de/bgb](https://www.gesetze-im-internet.de/bgb/) | last changed 23.7.2026 | 13,116 | 40 | § 5 UrhG, public domain |
| BetrKV | [gesetze-im-internet.de/betrkv](https://www.gesetze-im-internet.de/betrkv/) | last changed 16.10.2023 | 1,251 | 4 | § 5 UrhG, public domain |
| HeizkostenV | [gesetze-im-internet.de/heizkostenv](https://www.gesetze-im-internet.de/heizkostenv/) | last changed 16.10.2023 | 4,342 | 13 | § 5 UrhG, public domain |
| CO2KostAufG | [gesetze-im-internet.de/co2kostaufg](https://www.gesetze-im-internet.de/co2kostaufg/) | last changed 23.7.2026 | 4,194 | 16 | § 5 UrhG, public domain |
| 17 BGH VIII ZR judgments ([list with one-line topics](ingest.py)) | rechtsprechung-im-internet.de | 2014-07-09 to 2026-05-20 | 53,500 | 128 | § 5 UrhG, public domain |
| **Total** | | | **76,403** | **201** | |
| *Holdout: BGH VIII ZR 6/24* | rechtsprechung-im-internet.de | 2026-05-20 | 8,311 | 21 when added | § 5 UrhG, public domain |

## Ingestion

I downloaded the laws and the court decisions as XML files from the official government websites and read them with Python. Then I split the texts the same way lawyers cite them, so by paragraph (§) for the laws and by margin number (Rn.) for the court decisions. After that I merged these into chunks of about 200 to 400 words, which gave me 201 chunks. Every chunk has its source, location, date or version, and URL, so a property manager can look it up. I also removed parts of the court decisions that are not useful for my user, like the facts of the specific case and the opinion of the lower court, which can be wrong. One problem I had to fix was a formula in the heating cost law that only existed as an image, so I typed it in by hand. I embedded the chunks with Gemini and stored them in ChromaDB in the index folder, as the assignment asked.

## Test set

For the test set I wrote 39 questions from the documents, 25 that need one passage, 7 that need two, and 7 that the documents cannot answer. I wrote them the way a property manager would ask and wrote a reference answer for each. Two examples are:
- "We had to remove a rotten tree from the garden because it was no longer stable. Can I include the cost in the tenants' service charge statement?" The answer is yes, as garden maintenance, if the lease covers it.
- "Do I have to get comparison quotes before hiring a cleaning company?" The documents do not answer this, so the assistant should say so and refer to a lawyer.

Files: [`eval/questions.csv`](eval/questions.csv) · [`eval/review.md`](eval/review.md)

## Retrieval

Since the documents are German and the questions English, I compared four designs, and these are the three main ones:
- A, searching with the English question
- B, translating the question into German legal terms first
- C, the translation plus keyword search

A hit means the right passage, or the summary of the right court decision, is in the results. I chose B with the top 5 results, because it found the right passage most often (91%) and added fewer words to the prompt than C.

| Design | Hit rate k=1 | k=3 | k=5 | Words added (k=5) |
|---|---|---|---|---|
| A: English question | 59% | 78% | 81% | 1,242 |
| **B: German translation** | 59% | 81% | **91%** | 1,344 |
| C: translation + keyword search | 50% | 66% | 72% | 1,564 |

The fourth design was C with at most two passages per document, which did no better than C, so I left it out of the table.

Files: [`eval/retrieval_results.md`](eval/retrieval_results.md)

## Tools and subagent

The MCP server has two tools:
- search(query), which searches the documents and returns the 5 best passages with their citations
- add_document(path), which adds a new court decision or law to the index

The subagent can only use the search tool. Its instructions say to search once for each part of the question, answer in English with citations, and say when the documents do not cover something. In the transcript below, it answers the tree question correctly, but it says the playground question is not covered, because the search did not find the right passage.

**Search result** (top 2 hits for q01):

1. BGH VIII ZR 107/20, Leitsatz
2. BGH VIII ZR 107/20, Rn. 23–25

**Transcript** (trimmed, cuts marked […]; full version in [`eval/subagent_transcript.md`](eval/subagent_transcript.md)):

```text
❯ Use the corpus-researcher subagent to answer: We had a rotten tree removed
  from the garden and we pay someone to replace the sand in the playground. Can
  I bill the tenants for both?

⏺ corpus-researcher(Tree removal and playground sand)
[…]
› Message from corpus-researcher
[…]
  Four searches were run: tree felling, playground sand, a second try for the
  wording of § 2 Nr. 10 BetrKV, and the "recurring" requirement together with
  the lease agreement. None of them returned the text of § 2 Nr. 10 BetrKV
  itself, so I can only quote it as the BGH reproduces it.
[…]
  - The BGH held that the costs of felling a rotten tree that is no longer
  stable (morsch, nicht mehr standsicher) are, in principle, billable garden
  maintenance costs (Gartenpflege) under § 2 Nr. 10 BetrKV (BGH VIII ZR 107/20,
  Leitsatz, decided 2021-11-10).
[…]
  **2. Replacing playground sand (Spielsand-Erneuerung): not covered by the
  results**
  - Two separate searches returned no passage that mentions playgrounds
  (Spielplätze) or renewing sand (Erneuerung von Sand). Neither returned the
  text of § 2 BetrKV.
[…]
⏺ Tree: yes, in principle, if your lease passes on service charges. Playground
  sand: the corpus doesn't answer that one, so ask a tenancy lawyer before you
  bill it.
[…]
```

Files: [`server.py`](server.py) · [`.claude/agents/corpus-researcher.md`](.claude/agents/corpus-researcher.md)

## Adding a document

If a document is already in the index and has not changed, it is skipped, and if it has changed, the old version is replaced. For the demo I used the question about comparison quotes and added the held-back court decision BGH VIII ZR 6/24. Before, the agent found no passage about it, but still concluded that there is no duty. After adding the decision, it found it in the first search and gave a correct answer with a citation.

Files: [`eval/add_document_demo.md`](eval/add_document_demo.md)

## Harness and guardrails

My AGENTS.md has these rules:
1. Only answer from the search results
2. Cite every claim
3. If the documents do not answer it, say so and name who to ask
4. Say what the answer depends on, for example the lease
5. If a law and an older court decision differ, the law wins
6. Search once for each part of the question
7. Answer in English and keep the German term in brackets
8. Only add documents when the user asks

The first guardrail is the approval step. Before add_document runs, the program asks me to confirm with y or n. The second guardrail checks after each answer that every citation was really returned by the search. If not, the agent has to fix the answer once, and otherwise the answer gets a warning. It fired on 26 of 39 answers and fixed 22 of them, while 4 stayed flagged. For example, in the question about the caretaker's on-call fee, it cited three law sections the search never returned, and the retry removed them. I also tried adding a rule to AGENTS.md for this, but in a rerun it did not change anything, while the code check did.

Files: [`agent.py`](agent.py) · [`AGENTS.md`](AGENTS.md) · [`eval/guardrail_log.jsonl`](eval/guardrail_log.jsonl)

## Evaluation

I ran the agent on all 39 questions. With code (simple Python, no AI) I checked whether the citations were retrieved and whether the answer says the documents do not cover the question. Then a larger Gemini model graded each answer as the judge, with two criteria:
- correct, meaning it matches my reference answer
- supported, meaning every claim is in the retrieved text

I also graded all 39 answers myself before looking at the judge. I agree with the judge on 95% for correct and 82% for supported. The main difference is that the judge passed one answer that should have said "not covered" and one that missed an exception, so it is too lenient where it matters most for my use case.

| My grades | single | multi | unanswerable | all |
|---|---|---|---|---|
| Correct (same conclusion as my reference answer) | 23/25 | 6/7 | 4/7 | 33/39 |
| Supported (everything it says is in the passages it found) | 23/25 | 7/7 | 5/7 | 35/39 |

That means 4 correct refusals and 3 wrong ones (unanswerable questions it answered anyway), and it never refused a question the documents can answer.

As an extra, I wanted to test if a RAG system is actually better than a general AI, which was my father's original problem. So I compared my agent with plain Gemini Flash without my documents, in two steps. First with only the questions, where it got 9 of 39 right, but 17 answers never mentioned German law and about half of those used UK or US rules, because the questions do not name a country. Then I added "(Germany, residential lease)" to each question, and it got 24 of 39 right. However, it never said "I don't know" on the 7 unanswerable questions, while my agent got 35 of 39 right by the same judge (33 by my own grades) and said "not covered" on 4 of the 7. This shows why the RAG system was the right step. A general AI is not bad on simple questions, but it always gives an answer, even when it should not, and without sources a property manager cannot tell when it is wrong.

Files: [`evaluate.py`](evaluate.py) · [`eval/baseline.md`](eval/baseline.md)

## Failures

By my grades, 9 answers failed:

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 3 | q07, q25, q28 |
| Wrong answer from the right passage | 0 | |
| Unsupported claim | 3 | q04, q21, q36 |
| Wrong refusal (answered when it should not) | 3 | q33, q34, q38 |
| Bad test question | 0 | |

The most important problem is that it sometimes answers questions the documents cannot answer, instead of saying so. I would fix this first, with a second check after the answer that tests whether a passage actually states the conclusion. The second problem is that it sometimes misses an exception because that passage is not found, so I would improve the search next.

Files: [`eval/failures.md`](eval/failures.md)

## Decision

I would let my father use it as a replacement for googling and asking a general AI, but not instead of the lawyer. It cites a source for every answer, and the code checks that each source was really found, so he can check it quickly, and it says "not covered" much more often than a general AI. However, it still answered 3 of 7 questions it should not have answered, so for anything important or unclear he should still ask an expert.

| | Agent answers | Agent says "not covered" |
|---|---|---|
| **Documents can answer** | 32 (29 correct, 3 wrong) | 0 |
| **Documents cannot answer** | 3 | 4 |

I also thought about putting money values on each cell, but without real data these would have been made up. From talking to people in property management, the worst case is clearly an AI that answers confidently but wrong. In my table these are the 3 unanswerable questions it answered and the 3 wrong answers. A wrong "not covered" would cost time and an expert's fee, which is still cheaper than acting on a wrong answer, and in my test this did not happen once.

Each question costs about 37,500 tokens and 41 seconds.

## AI use

I used Claude Code to build the pipeline and write the code, and after I decided which types of documents I wanted, it also found and downloaded the right ones for the corpus. I used Claude to help with the formatting, wording and grammar of this report, and as a second opinion, for example to check my assumptions when I investigated why answers failed. All the decisions (use case, chunking, design choice, refusals, judge rubric, ship decision, questions) are mine, and so are the grades and the analysis.
