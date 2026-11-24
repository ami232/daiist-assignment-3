# Evaluation summary

Questions: 36; answers: 36; judged: 36.

## Retrieval

| design | k | hit rate (any source) | multi: any | multi: all | avg words in prompt |
|---|---|---|---|---|---|
| A | 1 | 80% | 64% | 0% | 243 |
| A | 3 | 93% | 82% | 0% | 695 |
| A | 5 | 97% | 91% | 27% | 1195 |
| B | 1 | 83% | 73% | 0% | 286 |
| B | 3 | 90% | 82% | 18% | 828 |
| B | 5 | 93% | 82% | 18% | 1419 |
| C | 1 | 73% | 55% | 0% | 264 |
| C | 3 | 93% | 82% | 18% | 735 |
| C | 5 | 97% | 91% | 36% | 1261 |

## Answers

| measure | count |
|---|---|
| correct (judge) | 25/36 |
| unsupported (judge) | 3/36 |
| correct refusals (code) | 3/6 unanswerable |
| wrong refusals (code) | 1/30 answerable |
| answers with all citations valid (code) | 29/30 answerable |

## Judge vs human labels

- correct: 81% agreement (17/21)
- supported: 100% agreement (21/21)

Disagreements:

- q09 correct: human=1 judge=0; judge reason: The assistant provides clear instructions on how to save and revert to a version, matching the main steps in the reference answer. However, it misses key details mentioned in the reference answer, specifically that the estimate must not be finalized and that there is a limit of 24 versions. All stated facts are fully supported by the retrieved text.
- q11 correct: human=1 judge=0; judge reason: The assistant provides clear, accurate steps for generating a SEPA payment file that align well with the reference answer and retrieved text. However, it misses the key requirement stated in the reference answer that every supplier needs an IBAN. All claims made in the response are fully supported by the retrieved text.
- q13 correct: human=1 judge=0; judge reason: The assistant provides accurate step-by-step instructions that are fully supported by the retrieved context. However, it omits key limitations mentioned in the reference answer, specifically that finalized estimates or estimates with tied purchase order/supplier invoice lines cannot be moved.
- q31 correct: human=1 judge=0; judge reason: The question is marked as unanswerable in the benchmark, but the assistant attempted to answer it instead of stating that the help centre does not cover it, so correct is 0. However, all factual claims and steps provided by the assistant are directly backed by the retrieved text, so supported is 1.

## Cost and latency

- mean tokens per question: 5668
- mean seconds per question: 4.7
