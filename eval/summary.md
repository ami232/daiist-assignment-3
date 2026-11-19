# Evaluation summary

Questions: 37 (30 answerable, 7 unanswerable)

## Retrieval (answerable questions)

| design | chunks | hit@1 | hit@3 | hit@5 | multi: both passages @5 | words in prompt @5 |
|---|---|---|---|---|---|---|
| fixed + dense | 276 | 0.733 | 0.867 | 0.967 | 0.75 | 1087 |
| fixed + hybrid | 276 | 0.7 | 0.933 | 0.967 | 0.625 | 1087 |
| structure + dense | 406 | 0.767 | 0.933 | 1.0 | 0.875 | 923 |
| structure + hybrid | 406 | 0.667 | 0.9 | 0.967 | 0.625 | 921 |

## End to end

| outcome | count |
|---|---|
| correct | 30 |
| wrong | 0 |
| unsupported | 0 |
| wrong refusal | 0 |
| correct refusal | 7 |
| answered unanswerable | 0 |

## Code checks

- answers with at least one citation (answerable, not refused): 30/30
- all citations valid (cited id was retrieved): 37/37
- cites the expected document (answerable, not refused): 30/30
- guardrail fired: 0 (none)

## Judge vs human

- 37 answers graded by hand. Agreement: correct 97%, supported 100%. Disagreements: m01

## Failures by cause

| cause | count | questions |
|---|---|---|
| retrieval miss | 0 |  |
| wrong answer from right passage | 0 |  |
| unsupported claim | 0 |  |
| wrong refusal | 0 |  |
| bad test question | 0 |  |

## Cost per question

- tokens: mean 4019, max 5646
- seconds: mean 38.6, max 272.0
- searches per question: mean 1.11
