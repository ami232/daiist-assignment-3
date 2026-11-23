# End-to-end evaluation

Agent: gemini-3.8-flash with retrieval design B (k=5). Judge: gemini-3.1-pro-preview. 39 questions.

Correct and supported come from the judge; refusals and the three code checks are computed in code.

| | single | multi | unanswerable | all |
|---|---|---|---|---|
| Correct (judge) | 24/25 | 6/7 | 5/7 | 35/39 |
| Supported (judge) | 24/25 | 2/7 | 6/7 | 32/39 |
| Unsupported (judge) | 1/25 | 5/7 | 1/7 | 7/39 |
| Says the documents don't cover it, anywhere (code) | 1/25 | 0/7 | 6/7 | 7/39 |
| … and leads with it, first 600 characters (code) | 0/25 | 0/7 | 2/7 | 2/39 |
| Correct refusals: unanswerable, says not covered | 0/25 | 0/7 | 6/7 | 6/39 |
| Wrong refusals: answerable, leads with not covered | 0/25 | 0/7 | 0/7 | 0/39 |
| Wrong refusals: unanswerable, never says not covered | 0/25 | 0/7 | 1/7 | 1/39 |
| Answerable with a gap caveat later in the answer | 1/25 | 0/7 | 0/7 | 1/39 |
| (a) All citations valid (code) | 22/25 | 6/7 | 7/7 | 35/39 |
| (c) Cites an expected source (code) | 23/25 | 7/7 | – | 30/32 |
| Citation guardrail fired | 20/25 | 4/7 | 2/7 | 26/39 |
| Answer flagged by the guardrail | 3/25 | 1/7 | 0/7 | 4/39 |

| Per question | single | multi | unanswerable | all |
|---|---|---|---|---|
| Tokens, average | 35,803 | 40,200 | 41,115 | 37,545 |
| Tokens, max | 154,394 | 114,720 | 128,635 | 154,394 |
| Seconds, average | 41.5 | 44.7 | 36.0 | 41.1 |
| Seconds, max | 87.7 | 79.6 | 83.1 | 87.7 |
| Model calls, average | 4.2 | 4.4 | 4.4 | 4.3 |

Agent totals for the run: 1,345,169 input + 119,104 output tokens. Seconds include the translation step in the search tool and the guardrail's retry; tokens are the agent model's only (the translation step adds ~270 tokens per search, see retrieval_results.md).

Agreement with your labels: eval/human_labels.csv has no rows yet (grade eval/to_grade.md first).

add_document demo (q33, before and after): eval/add_document_demo.md
