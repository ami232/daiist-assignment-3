# Evaluation summary

36 questions; model `gemini-3.5-flash-lite`.

## Retrieval (hit rate)

| design | hit@1 | hit@3 | hit@5 |
|---|---|---|---|
| section-bm25 | 0.43 | 0.67 | 0.77 |
| section-vector | 0.63 | 0.87 | 0.93 |
| section-hybrid | 0.60 | 0.83 | 0.93 |

Best by hit@3: **section-vector**.

## End to end (LLM judge)

| kind | correct |
|---|---|
| single | 23/24 (96%) |
| multi | 5/6 (83%) |
| unanswerable | 6/6 (100%) |

- Correct overall: 34/36
- Supported by retrieved text: 35/36
- Answered with an unsupported claim (made something up): 0/36
- Rightly refused (unanswerable): 6/6
- Wrongly refused (answerable): 2/30
- Answers with an invalid citation (before the guardrail): 7
- Answers changed by the guardrail: 7

## Failures (automatic first pass; review in failures.csv)

- wrong refusal: 2

## Cost per question

- Tokens: mean 5,450, median 3,681, max 25,020
- Seconds: mean 6.2, median 5.9, max 14.3
- Tool calls: mean 1.5
