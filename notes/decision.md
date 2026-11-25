## Cost and latency

Prices from the Google AI Studio pricing page (aistudio.google.com/docs/pricing), paid tier, checked on 23 November 2026:
- gemini-3.5-flash-lite: $0.30 per 1M input tokens, $2.50 per 1M output tokens.
- gemini-embedding-2: $0.20 per 1M text input tokens.

Average per question in my 30-question run: 3,805 input tokens, 278 output tokens, 1.1 searches.

- Input: 3,805 x $0.30 / 1,000,000 = $0.00114
- Output: 278 x $2.50 / 1,000,000 = $0.00070
- Total: about $0.0018 per question.
- Embedding the question is negligible (assumed about 30 tokens, about $0.000006).
- At an example volume of 500 questions a month: about $0.92 a month.
- One-off indexing of the 536 chunks: roughly $0.04 (my estimate, at most about 190,000 tokens).

I ran everything on the free tier, so I actually paid $0. These are the costs at paid rates.

Latency: median 3.5 seconds, 90th percentile 13.2 seconds.

Free tier limit: gemini-3.5-flash-lite allows 15 requests per minute and 500 per day. I hit 19 against 15 per minute during testing, so the free tier would not support several users at once.

## What the evaluation showed

- Human grades on 30 questions: correct 29/30, supported 23/30.
- The 5 unanswerable questions were all refused (original run).
- Fabricated citations: 0, though one cited article (q01) was not among the retrieved passages.
- 7 of the 30 original answers were graded unsupported (q01, q04, q09, q10, q16, q22, q27); in the classification, 6 of them are unsupported claims and q09 is a misreading. q14, graded after the document was added, is a further case.
- Other failures I classified (notes/failure_classification.md): 1 bad test question (q19), 2 retrieval misses with little or no harm to the answer (q07, q08), 0 wrong refusals.
- Limit of the test: 30 questions on 3 documents, written and graded by me.

## Decision

Ship with limits

It did well on my test: 29 of 30 answers correct, all 5 unanswerable questions refused, no fabricated citations (though one cited article, in q01, was not among the retrieved passages), and about $0.0018 a question at paid rates (I ran on the free tier). The problem is that 7 of the 30 answers had something I couldn't find in the passages the agent retrieved. Mostly it was true extra detail, but q16 added a legal condition that isn't in the retrieved passage, and q09 misread the passage it cited. A user can't see the difference without checking. q14 showed the same weakness from another side. Even with the new document, the agent answered as if a 2023 decision still applies, so for anything that changes over time, like adequacy decisions or fines, the answer is only a pointer to a dated source. It's 30 questions on 3 documents that I wrote and graded myself, so I'd give it to a small group but not rely on it for a legal decision.

Limits:
- Use it to find the right article, not as legal advice. Before acting on a deadline, fine or condition, open the cited article and check it says what the answer says.
- It only covers the GDPR and two EDPB guidelines. It has no Spanish or US state law, so for those ask the AEPD or an adviser.
- For anything that can change, check the date of the source and whether it's still current.
- The free tier allows 15 requests a minute, so use the paid tier for more than one user.
- Before a wider release, get someone else to grade the answers and mark the core points in each reference answer.
