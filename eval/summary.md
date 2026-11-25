# Evaluation summary

## Retrieval (answerable questions)

| design | hit@1 | hit@3 | hit@5 | words in prompt (k=5) |
|---|---|---|---|---|
| dense | 72% | 96% | 96% | 1061 |
| bm25 | 24% | 80% | 84% | 1173 |
| hybrid | 72% | 92% | 100% | 1130 |

Best by hit@5 (ties broken by hit@3, hit@1): **hybrid** (retrieval.DEFAULT_MODE is `hybrid`; change it if they differ).

## End to end (judge + code checks)

- Questions: 32 (25 answerable, 7 unanswerable)
- Judged correct: 32/32 (100%)
- Judged supported (no unsupported claims): 32/32 (100%)
- Valid citations (code check): 32/32
- Answerable questions citing the expected regulation(s) (code check): 25/25
- Correct refusals on unanswerable: 7/7
- Wrong refusals on answerable: 0/25
- Unanswerable questions that were answered anyway: 0/7
- Guardrail fired: 0 times
- Cost per question: 3127 input + 198 output tokens, 18.7s on average

## Failures by cause

- none

See eval/failures.csv. The causes are automatic guesses: check each one by hand (a failure can also be a bad test question).

## Agreement between you and the judge

- `correct`: agree on 22/22 (100%)
- `supported`: agree on 22/22 (100%)
- Disagreements on `correct`: none
