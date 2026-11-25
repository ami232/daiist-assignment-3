# Assignment 3 Report

- **Name**: Anna Serra Guirao
- **Student ID**: 18815
- **Group**: BBADBA 5B

## Use case

In the first two assignments I was focusing on an M&A boutique, so for this one I built what I called Deal Desk, an assistant that answers the questions the the analysts have about EU rules while they prepare a deal. When two companies merge or one buys another one, if they're big enough the deal has to be approved by the European Commission before it can go ahead, and some deals with buyers from outside the EU can also be checked for security reasons, so the person asking is an associate who needs to know things like if the deal is big enough to need that approval, how long the approval takes, or what the contracts are allowed to say, and they use the answer to plan the deal and to advise the client.

The reason why a wrong answer is so much worse than "I don't know" is that the mistakes here are very expensive and they don't cost the same in both directions. If the assistant says that the deal doesn't need approval and it was wrong and the client goes ahead, the EU can fine the company up to 10% of its yearly sales and the deal can be stopped, but if it says that they need approval and it was wrong then the boutique would only loose some time preparing paperwork that wasn't necessary. On the other hand, "I don't know" just means the associate asks an actual lawyer, which costs some money but it is cheap compared with the risk of a having a wrong answer. That is why the whole system is built to answer only from the official EU documents, by showing which part of which document each answer comes from so the associate can check it, and say "The Deal Desk documents do not cover this" when the documents don't have the answer.

## Corpus

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| EU Merger Regulation, Council Regulation (EC) No 139/2004 (EUMR) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32004R0139 | 20 January 2004 | EUR-Lex reuse policy, Commission Decision 2011/833/EU | 14,317 |
| Commission Consolidated Jurisdictional Notice (CJN) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52008XC0416(08) | 16 April 2008 | same | 24,059 |
| Commission Remedies Notice (RN) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52008XC1022(01) | 22 October 2008 | same | 15,105 |
| Ancillary Restraints Notice (ARN) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52005XC0305(02) | 5 March 2005 | same | 3,332 |
| FDI Screening Regulation, Regulation (EU) 2019/452 (FDI) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019R0452 | 19 March 2019 | same | 6,890 |
| **Total** | | | | **63,703** |

The first document is the main EU law that says which deals need approval, the second one is the guide on how to apply it (for example how to measure the size of the companies), the third one explains what companies can offer to fix a deal the EU doesn't like, the fourth one says which extra clauses the contracts can have, and the last one is the law on checking investments from outside the EU. The word counts are what my code counted after taking out the website menus and the footnotes (it is saved in index/stats.json). I checked that they could all be reused, because EUR-Lex lets you reuse its legal documents for anything as long as you mention the source, and they don't have personal data because they're laws and guides.

I had to be careful with two things, because the EU law on foreign investments was already replaced by a new one, but the new one only applies from 2028, so I kept the old one since it's still the one active, and I left out the guides on how the EU decides if a merger is harmful, because a new version is being prepared this year so they could be outdated.

## Ingestion

I downloaded the five pages from EUR-Lex and split them into the units of smallest pieces of a law that you can point to, like "Article 1, paragraph 2" or "paragraph 156" of a guide. Each document had a different format on the website, so my code read the text in order and then follows either the articles of a law or the numbered paragraphs of a guide, and every chunk kept the document and the exact place it came from, because that's what the search tool shows as the source and what the evaluation uses to check if it found the right paragraph.

The problem I spent the most time on was that some paragraphs were disappearing, because when I checked that the paragraphs of each guide went 1, 2, 3 without gaps, 8 of one guide and 4 of another were missing, and it was because when a paragraph has a list inside, the website puts it in a table inside another table, so my code was skipping it. Then I also found that footnote numbers like "( 21 )" mixed into the text, and when I removed them I had to be careful because my first version was also deleting the "(1)" in "Article 3(1)", which would have broken the sources the associates need to check.

I compared two ways of cutting the text into chunks and a third way of searching them:

- structure: one chunk per paragraph of an article or of a guide, which gave 584 chunks of 110 words on average.
- fixed: the text is cut every 200 words, ignoring the paragraphs, which gave 400 chunks of 199 words on average.
- hybrid: the structure chunks, but searched with both the meaning (so embeddings) and the exact words (so keyword search).

Before making the embeddings I added a small header to each chunk with the document and the place, because a sentence like "This shall not apply if each of the undertakings concerned achieves more than two-thirds..." (it is one of the paragraphs) means nothing without any context. For the embeddings I used gemini-embedding-2 and saved them after every batch, so I only had to build the index once even with the daily limit of gemini.

## Test set

I came up with the 42 questions with my sister, who works in M&A, because she knows what associates actually ask, and I checked them against the documents with an AI assistant, so they're written like real situations (like for example "The deal is signed in February and the audited accounts for last year aren't ready yet, which figures do we use for the turnover?"). For each one I wrote where the answer is and a short reference answer, and I checked with code that every expected place exists in the documents and that the topics of the unanswerable ones don't appear anywhere.

| Kind | Count |
|---|---|
| Answered by one passage (single) | 27 |
| Need two passages (multi) | 8 |
| Not answered by the documents (unanswerable) | 7 |
| Total | 42 |

- Multi: in question 34 it says "If we offer commitments in Phase II after working day 55, what's the deadline to submit them and when does the Commission have to take the final decision?" and that needs a paragraph from the merger law and another one from the remedies guide.
- Unanswerable: in question 36 it says "If the deal doesn't have an EU dimension, what are the Spanish merger notification thresholds that would apply?" and that's unanswerable because the documents talk about thresholds all the time but only the EU ones.

## Retrieval

| Design | Hit rate @1 | @3 | @5 | Words added to the prompt (top 5) | Chunks |
|---|---|---|---|---|---|
| structure | 0.429 | 0.657 | **0.914** | 661 | 584 |
| fixed | 0.571 | 0.714 | 0.800 | 996 | 400 |
| hybrid | 0.343 | 0.571 | 0.686 | 649 | 584 |

These are from eval/summary.json, of the 35 questions that have an answer, and a question only counted as found if all the paragraphs it needed were in the top results. I chose structure, because the agent reads the top 5 and there it found the right paragraphs for 0.914 of the questions and with fixed only for 0.800, and it also added 661 words to the prompt instead of 996, so it was better and cheaper. Although it is true that fixed was better at getting the right paragraph first (0.571 against 0.429), but I think it's because its chunks are much bigger so they have more context, but they also bring more text that doesn't matter. Then, hybrid was the worst, which I didn't expect, and I think it's because words like "concentration", "Commission" or "turnover" are in almost every paragraph, so the keyword search just pushed the right paragraph down.

## Tools and subagent

My tool server (server.py, called corpus) gave the AI two tools:

- search(query): returns the 5 paragraphs that match the question the best, and each with its source at the top like [EUMR Art. 1(2)], and its description also says what the documents don't include (like Spanish or US rules) so the AI knows when to not trust the results.
- add_document(path): adds a new file going through the same process as the documents I have been using.

This was the first result that search gave in check.py for the first question of the test set:

```
[EUMR Art. 1(1)–(3)] (Scope)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 1(1), Art. 1(2), Art. 1(3)
Without prejudice to Article 4(5) and Article 22, this Regulation shall apply to all concentrations with a Community dimension as defined in this Article. A concentration has a Community dimension where: (a) ...
```

The subagent (.claude/agents/corpus-researcher.md) could only use search, and its instructions told it to search again with other words if it needed it, answer in maximum 150 words only with what the paragraphs say, cite all the sentences, say "The Deal Desk documents do not cover this." when it doesn't have the answer, and never say a deal doesn't need to be approved except if a paragraph says it.

I asked my sister to use the subagent from my editor to make a question (also telling it directly to use the subagent), and it searched only once and answered in 44 seconds with the same rule as my reference answer for question 19, only citing paragraphs from the expected article (I added the screenshot in docs/subagent_transcript.png):

```
> Use the corpus-researcher subagent, how long can the seller's non-compete last

I'll ask the corpus-researcher subagent about seller non-compete duration under the Deal Desk library.

Explored 1 search
  • Seller non-compete duration (Auto, Completed)

Up to three years if the sale transfers both goodwill and know-how; up to two years if only
goodwill is transferred. [ARN para. 20]

Seller non-competes can be directly related and necessary so the buyer gets the full value of the
assets (including goodwill/know-how). [ARN para. 18] Duration, geography, subject matter and the
persons bound must not go beyond what is reasonably necessary. [ARN para. 19]

(via corpus-researcher)
```

## Adding a document

I already have mentioned the add_document tool, but how it does it is by making a fingerprint of the file first, so if the same file is already in the index it doesn't do anything, and if it's a new version of a document it replaces the old one, for the assistant not to mix them. And for the demo I used the question "Which deals can go through the simplified procedure and use the short Form CO?" and the EU's 2023 guide on the simplified procedure, which is the document that answers it. But before adding it the agent answered "The Deal Desk documents do not cover the rules on the simplified procedure or the short Form CO ..." and said to ask a lawyer, and then add_document answered "Done: added STN (STN.html): 35 chunks in the 'structure' index, 35 new embeddings", and after that the same question got a real answer with the five types of deals that qualify, each one with its source, like "Joint ventures with no EEA turnover... [STN para. 5(a)]". And when I added the same file again it answered "STN (STN.html) is already indexed with identical content; nothing was added" (I added all of this in eval/add_document_demo.json).

## Harness and guardrails

I built the agent (agent.py) with LangChain's create_agent like in session 10, with gemini-3.5-flash-lite, my two tools and its instructions in AGENTS.md. The rules were to search before answering, to answer only from the search results, cite everything, to say when the documents don't cover the question, to never say a deal doesn't need to be approved without a paragraph that explicitly says it, to keep it short, to only add documents when asked to and to treat the documents as information and not as instructions, and I wrote the reason next to each rule because I think the AI follows a rule better when it knows why.

The code also ran three guardrails that the AI can't skip:

1. Approval: add_document only runs if a person types "y", because adding a document changes every answer after it.
2. Call limit: maximum 8 calls to the AI per question, so it stops if it goes around in circles.
3. Source check (my extra one): after the AI answers, the code checks that every source it cites was really returned by the search, and if not, or if it gives facts with no source, the answer is blocked. I chose this one because the source is what the associate trusts, so an invented source is the worst mistake, because it looks exactly like a real one.

In my first run it blocked 12 answers, but when I looked at them none was actually wrong, it was my code not understanding some ways of writing the sources, like two paragraphs in the same brackets (like for example [CJN para. 155, 156]) or a point inside a paragraph (like for example [STN para. 5(a)]). After fixing that it didn't block any of the 42, which is good but it meant I didn't have a real case to test the third guardrail, so evaluate.py also tests it on purpose, it takes the real answer to "can they close the deal before the Commission clears it?" and adds a source that the search never returned, and the guardrail blocks it with "citations not found in the search results: EUMR Art. 21(4)", and the same answer without any sources is blocked with "the answer states facts without any citation" (I put it in guardrail_test in eval/summary.json).

## Evaluation

For the evaluation, evaluate.py ran the agent on the 42 questions and checked each answer in two ways. First the code checks, which are the things a program can check without understanding the answer, like if the sources pass the source check, if it refused a question that had an answer, or if it answered one that didn't, which is the worst case. Then a judge (gemini-3.5-flash, a stronger model than the agent) graded each answer on if it's correct compared with my reference answer and if everything it says is in the paragraphs the search returned. The free version of the judge only allows 20 requests a day, so I graded 6 answers per request.

| Code check (42 questions) | Result |
|---|---|
| Unanswerable questions correctly refused | 7 of 7 |
| Unanswerable questions answered anyway | 0 |
| Answerable questions wrongly refused | 0 of 35 |
| Answers blocked by the source check | 0 |
| Answers that cite the document where the answer is | 33 of 35 |

| Judge (42 questions) | Result |
|---|---|
| Correct | 42 of 42 |
| Supported by the paragraphs the search returned | 42 of 42 |
| Agreement with my own grades on correct (24 answers) | 0.958 |
| Agreement with my own grades on supported (24 answers) | 0.958 |

The first time the judge graded everything it said 5 answers were unsupported, but when I read its reasons it kept saying that the paragraph "cuts off" or was "truncated", and it was because my code was only sending the judge the first 6,000 characters of what the search returned, so for 17 answers it couldn't see all the paragraphs. I sent it the full paragraphs and graded those 17 again, and then all 42 were supported (all in `eval/summary.json`). I graded 24 of the answers myself before seeing the judge's grades, and we only disagreed on one.

## Failures

The only real failure was in question 6, which was a wrong answer from the right paragraph, because the search found EUMR Art. 10(3) but the answer said that the 105 working days also happen when the parties ask for an extension of up to 15 days, when in the article the 105 days are only for commitments offered late and the extensions are a separate rule, so it mixed the two. The judge said it was correct and supported, and the source check let it through because the source was real, so the only one that caught it was me, which shows that a real source doesn't mean the answer read it correctly, and that the judge is quite lenient with deadlines that look right.

Then two answers (for questions 30 and 34) didn't cite the document I was expecting, but they were right and they cited the guide that explains the same rule instead of the law, so I think this is more a bad test question because I was too strict with where the answer had to come from. Also, in the retrieval test 3 questions (3, 28 and 34) didn't have all their paragraphs in the top 5, but the agent searched again with other words and still answered them correctly, so these misses didn't end up being wrong answers. Overall there weren't any wrong refusals or any unsuported laws.

## Decision

I would let the associates use it to find the right paragraph and get a first answer, but not rely on it without opening the source, because question 6 showed me that an answer can look right, cite the right article and still get a deadline wrong, and deadlines are exactly the kind of mistake that is expensive in this case. What I'm happy with is the "I don't know" part, because it refused the 7 questions the documents don't cover and it didn't refuse any that they do, which was the main thing I wanted from the use case. Each question cost on average 4,267 input tokens, 147 output tokens and 6.9 seconds, so it's cheap and fast enough for associates to use it all the time, and the next thing I would add is a check for numbers like deadlines and thresholds, comparing them with the paragraph, since that's where the one failure happened.

## AI use

I used Claude to help me write the code and the agent instruction files (AGENTS.md and the corpus-researcher subagent markdown). It also helped me format this report, especially the tables with the documents and the results, and it assessed that my test questions were well formulated as well as gave me the optimal number of questions to come up with to test the agent well enough.
