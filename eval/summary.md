# Evaluation summary

2026-11-24 · agent `gemini-3.5-flash-lite` · judge `gemini-3.5-flash-lite` · search design `article`

## Retrieval

Answerable questions: 27. A hit means an expected article is among the top k results.

| Design | hit@1 | hit@3 | hit@5 | multi: both passages in top 5 | words added (top 5) |
|---|---|---|---|---|---|
| article | 0.74 | 0.96 | 1.00 | 0.833 | 835 |
| fixed | 0.63 | 0.78 | 0.85 | 0.833 | 745 |

Highest hit@5 (ties broken by hit@3, hit@1, fewer words): **article**.

## End to end

Questions answered: 32 of 32.

| Result | Count |
|---|---|
| Correct (all questions) | 29/32 (91%) |
| Supported (all questions) | 31/32 (97%) |
| Correct answers to answerable questions | 24/27 (89%) |
| Unsupported answers | 1 |
| Correct refusals (unanswerable) | 5/5 (100%) |
| Wrong refusals (answerable) | 0 |
| Blocked by the citation check | 0 |
| Citation check fired (incl. fixed on retry) | 0 |

| Kind | n | Correct | Supported |
|---|---|---|---|
| single | 21 | 18 | 20 |
| multi | 6 | 6 | 6 |
| unanswerable | 5 | 5 | 5 |

## Cost per question

| | Mean | Median | Max |
|---|---|---|---|
| Agent tokens | 5,364 | 4,420 | 10,492 |
| Agent model calls | 2.3 | 2 | 3 |
| Seconds | 16.5 | 4.7 | 161.7 |
| Judge tokens (judged answers) | 2,750 | 2,416 | 4,506 |

## Agreement with your grades

You graded 27 answers; 27 of them were graded by the judge.

| | All your grades | Judge-graded only |
|---|---|---|
| Correct | 89% | 89% |
| Supported | 78% | 78% |

- q03 supported: you 0, judge 1. It gets the coin right, but 'all archaeological items' is too broad. Article 44(5) makes an exception for parts of a registered historic building.
- q04 supported: you 0, judge 1. Article 45 says who chooses the museum. The details about distance and conservation are in Article 42(2), which the answer didn't cite.
- q05 supported: you 0, judge 1. The fine is right. Article 76 only treats the excavation as an administrative offence if it isn't a crime.
- q14 supported: you 0, judge 1. Rule 1 allows a lift that fits with protection and significantly improves protection, knowledge or appreciation. It doesn't say a lift must be necessary for research or permanent protection.
- q20 correct: you 0, judge 1. It covers humanity and the states of cultural, historical or archaeological origin. It leaves out the country of origin as a separate basis for a claim.
- q22 supported: you 0, judge 1. Article 42 covers permission. The definition that makes mapping without disturbing the seabed a survey comes from Article 41, which the answer didn't cite.
- q23 supported: you 0, judge 1. The timing is right for this private boat, but the answer says 'any shipwreck'. Article 374 excludes state vessels.
- q25 correct: you 0, judge 1. It gives the right distance and says approval can be required. It leaves out the duty to apply the annex rules when the country regulates the work.
- q27 correct: you 0, judge 1. It says Spain can decline to lead but leaves out who then chooses the coordinator: the other states parties that declared an interest.

## Failures by suggested cause (check each one yourself)

- retrieval miss: 1 (q21)
- wrong answer from the right passage: 2 (q02, q14)

## Citation check firings

None.
