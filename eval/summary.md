# Evaluation summary

## End to end

- Questions with an answer: correct 32/35 (91%); wrong refusals 1/35 (3%); answers with an unsupported claim 0/35 (0%).
- Questions without an answer: correct refusals 10/11 (91%); answered anyway (made up) 1/11 (9%).
- Valid citations in non-refusal answers: 35/35 (100%).
- Answers that cite the expected contract(s): 33/35 (94%); key numbers of the reference present: 28/35 (80%).

- single: correct 17/19 (89%)
- multi: correct 15/16 (94%)

Guardrails that fired: 1 questions (q01: call_limit)

## Cost per question (agent only)

- Tokens: 5064 in + 108 out on average (max 19861 in).
- Seconds: mean 8.0, median 7.4, max 28.7.
- Tool calls: mean 1.7. Judge adds about one call per question.

## Agreement with your grades

You graded 20 answers (20 also judged).
- correct: agreement 19/20 (95%)
- supported: agreement 20/20 (100%)
- Disagreements on `correct` (id, you, judge): q16 (0/1)

## Failures (automatic first guess; confirm each in eval/failures.csv)

- wrong answer from the right passage: 2
- retrieval miss: 1
- unsupported claim (answered, should have refused): 1

Cause list for your own classification: retrieval miss, wrong answer from the right passage, unsupported claim, wrong refusal, bad test question.

## Retrieval

| design | questions | hit@1 | hit@3 | hit@5 | avg words in top 5 |
|---|---|---|---|---|---|
| clause: all answerable | 35 | 14/35 (40%) | 31/35 (89%) | 33/35 (94%) | 598 |
| clause: single | 19 | 14/19 (74%) | 19/19 (100%) | 19/19 (100%) | 598 |
| clause: multi (all passages) | 16 | 0/16 (0%) | 12/16 (75%) | 14/16 (88%) | 598 |
| window: all answerable | 35 | 5/35 (14%) | 21/35 (60%) | 24/35 (69%) | 980 |
| window: single | 19 | 5/19 (26%) | 17/19 (89%) | 18/19 (95%) | 980 |
| window: multi (all passages) | 16 | 0/16 (0%) | 4/16 (25%) | 6/16 (38%) | 980 |

Distance of the top result (clause design): answerable questions mean 0.214, unanswerable mean 0.234 (lower is closer).

