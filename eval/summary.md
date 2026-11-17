# Evaluation summary

## Retrieval (answerable questions, original corpus)

| design | chunks | hit@1 | hit@3 | hit@5 | multi: both passages @5 | words in prompt @5 |
|---|---|---|---|---|---|---|
| fixed+dense | 440 | 0.667 | 0.861 | 0.944 | 0.143 | 740 |
| fixed+hybrid | 440 | 0.639 | 0.778 | 0.889 | 0.429 | 739 |
| section+dense | 284 | 0.75 | 0.917 | 0.972 | 0.429 | 1062 |
| section+hybrid | 284 | 0.611 | 0.833 | 0.889 | 0.571 | 1080 |

## End to end

- Correct answers (judge): 32/36 answerable
- Unsupported answers (judge): 1
- Correct refusals: 5/6 unanswerable
- Wrong refusals: 1/36 answerable
- Valid citations (code check): 100% of answers
- Citation guardrail fired on 2 questions
- Cost per question: 4606 input + 125 output tokens, 2.12 model calls, 3.5 s on average (max 12.65 s)

## Failures by cause

- unsupported claim: 2
- wrong answer from right passage: 2
- retrieval miss: 1
- wrong refusal: 1

## Judge vs human

- correct: 96% agreement, Cohen's kappa 0.837 (n=28; disagreements: q42)
- supported: 89% agreement, Cohen's kappa -0.05 (n=28; disagreements: q01, q11, q12)
