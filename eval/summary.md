# Evaluation summary

## Retrieval (39 answerable questions)

| Design | hit@1 | hit@3 | hit@5 | all@5 (multi needs both) | words in top 5 |
|---|---|---|---|---|---|
| vector | 77% | 97% | 97% | 87% | 581 |
| hybrid | 64% | 85% | 90% | 80% | 581 |
| filter | 77% | 97% | 97% | 87% | 575 |

Hit@5 by kind: vector: single 97%, multi 100%; hybrid: single 94%, multi 75%; filter: single 97%, multi 100%

## End to end (46 answers)

Code checks: no search 0, answerable without citation 0, answers with invalid citation 1, answerable citing expected source 39, correct refusals 7, missed refusals 0, wrong refusals 0

Citation guardrail (agent.py), applied to the saved answers, would reject: q33 ['[bactrim, Contraindications, celebrex, Contraindications]']

Judge (46 graded): correct 45, unsupported 1, correct refusals 7, wrong refusals 0

| Kind | n | correct | unsupported |
|---|---|---|---|
| single | 31 | 31 | 1 |
| multi | 8 | 7 | 0 |
| unanswerable | 7 | 7 | 0 |

| Model | n | correct | unsupported |
|---|---|---|---|
| gemini-3.8-flash | 22 | 22 | 0 |
| gemini-3.5-flash | 10 | 10 | 1 |
| gemini-3.5-flash-lite | 14 | 13 | 0 |

Failures:
- q29 (single, gemini-3.5-flash): correct 1, supported 0; first expected passage at vector rank 1. Says the 1,250 mg daily cap applies to gout, but in the passage that cap belongs to section 2.4 (pain/dysmenorrhea), not 2.5 Acute Gout
- q34 (multi, gemini-3.5-flash-lite): correct 0, supported 1; first expected passage at vector rank 1. Does not report what the Advil label says (stomach bleeding warning with anticoagulants, ask a doctor); answers the Advil half from the Jantoven label instead

## Agreement with human labels

Graded by both: 30
- correct: 100% agreement, kappa None, disagree on none
- supported: 97% agreement, kappa 0.0, disagree on q29

## Cost per question

| Model | n | mean tokens | mean s | median s |
|---|---|---|---|---|
| gemini-3.8-flash | 22 | 2961 | 151.0 | 21.9 |
| gemini-3.5-flash | 10 | 4061 | 58.2 | 46.9 |
| gemini-3.5-flash-lite | 14 | 3352 | 4.1 | 2.8 |
| all | 46 | 3319 | 86.1 | 16.6 |
