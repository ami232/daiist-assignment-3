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
| single | 24/24 (100%) |
| multi | 6/6 (100%) |
| unanswerable | 6/6 (100%) |

- Correct overall: 36/36
- Supported by retrieved text: 36/36
- Answered with an unsupported claim (made something up): 0/36
- Rightly refused (unanswerable): 6/6
- Wrongly refused (answerable): 0/30
- Answers with an invalid citation (before the guardrail): 1
- Answers changed by the guardrail: 1

## Cost per question

- Tokens: mean 5,558, median 3,745, max 32,168
- Seconds: mean 7.3, median 5.7, max 31.7
- Tool calls: mean 1.5

## Judge vs human (20 answers)

- correct: agreement 0.95, Cohen's kappa 0.0, disagreements ['m06']
- supported: agreement 0.95, Cohen's kappa 0.0, disagreements ['u04']
