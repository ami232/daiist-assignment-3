# Evaluation summary

## Retrieval (answerable questions)

| design | hit@1 | hit@3 | hit@5 | multi, both passages @1/@3/@5 | words added @1/@3/@5 |
|---|---|---|---|---|---|
| structure | 88% | 97% | 100% | 0% / 33% / 67% | 242 / 720 / 1169 |
| fixed | 82% | 91% | 97% | 17% / 17% / 17% | 200 / 598 / 988 |

Hit = an expected passage is among the top k (for multi: at least one). Precise = expected location has at most 2 chunks; broad = more (any chunk counts).

| design | precise hit@1/@3/@5 | broad hit@1/@3/@5 |
|---|---|---|
| structure | 78% / 94% / 100% (n=18) | 100% / 100% / 100% (n=16) |
| fixed | 67% / 83% / 94% (n=18) | 100% / 100% / 100% (n=16) |

## End to end (agent)

- Answerable answered: 94% (32/34) (of which say part is not covered: []); wrong refusals: 2 ['q20', 'q31']
- Unanswerable: refused ['q06', 'q29', 'q30']; partial answer that says what is not covered ['q14', 'q23', 'q26']; answered anyway []
- Citations valid (code check, model's own answer): 98% (39/40)
- Answers that cite an expected passage: 97% (31/32)
- Guardrail fired: 2 {'q20': 'cited but not retrieved: [ALLERGEN_NOTICE_2017, Section 3.6]', 'q31': 'the answer cites no source'}
- Judge: correct 92% (37/40), supported 100% (40/40)
- Agreement with your grades: correct 100% (20/20) (kappa 1.00), supported 90% (18/20) (kappa 0.00); disagreements: ['q14', 'q26']

## Failures (automatic first guess; review them and spot bad test questions)

- unsupported claim (answered an unanswerable question): 1 ['q26']
- wrong refusal (guardrail blocked): 2 ['q20', 'q31']

## Cost and latency per question

- tokens: mean 6802, median 4542
- seconds: mean 24.2, median 15.0
- searches (one embedding each): 55 in total; models: {'gemini-3.5-flash-lite': 27, 'gemini-3.5-flash-lite, gemini-3.6-flash': 13}
