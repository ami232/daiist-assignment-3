# Evaluation summary

Written by `main.py evaluate` (stage 6) and rewritten on every run: do not edit it by hand.

- Questions answered and judged: 33 (28 answerable, 5 unanswerable)
- Design searched by the agent: article; model: gemini-3.6-flash (also the judge)
- Correct (judge): 27 of 33 (82%)
- Correct among answerable questions (judge): 23 of 28
- Unsupported answers (judge, supported = 0): 4 of 33 (12%)
- Correct refusals (unanswerable and refused): 3 of 5
- Wrong refusals (answerable but refused): 0 of 28
- Answered an unanswerable question: 2 of 5
- Answers with a citation that was not retrieved (before the guardrail): 0
- Mean tokens per question: 9,750 input, 1,127 output
- Mean seconds per question: 20.6

## Retrieval (stage 1)

| design | questions | hit@1 | hit@3 | hit@5 | multi_questions | multi_all@5 | words@5 |
|---|---|---|---|---|---|---|---|
| fixed | 28 | 0.857 | 1.0 | 1.0 | 8 | 0.625 | 997 |
| article | 28 | 1.0 | 1.0 | 1.0 | 8 | 0.625 | 1101 |

## Failures to classify

Every answer the judge marked not correct or not supported, or that code flagged.
Classes: retrieval miss, wrong answer from the right passage, unsupported claim, wrong refusal, bad test question.

| id | kind | correct | supported | code checks | question-only retrieval hit@5 | judge's reason |
|---|---|---|---|---|---|---|
| q08 | single | 0 | 1 |  | 1 | The answer misses the specific twist limit values (16 mm or 20 mm depending on line speed for 1 520 mm gauge) included in the reference answer. However, all claims made are fully supported by the retrieved passages. |
| q13 | multi | 0 | 1 |  | 1 | The answer is supported by the passages, but it is incomplete according to the reference answer because it omits the key detail that line layout, track parameters, switches and crossings, track resistance, structures, and platforms should be adapted together to move towards interoperability. |
| q17 | single | 0 | 1 |  | 1 | The answer is partial because it misses key details from the reference answer regarding the joint investigation with the railway undertaking to localise the section and determine the cause of instability if limits are met. However, all claims made in the answer are fully supported by the retrieved passages. |
| q18 | unanswerable | 1 | 1 | answered_unanswerable |  | The assistant correctly states that the TSI INF does not specify a numerical minimum ballast depth and accurately summarizes what the retrieved text does require regarding track design and ballast thickness without inventing any rules or values. |
| q24 | single | 0 | 1 |  | 1 | The answer is fully supported by the retrieved passages, but it fails to mention that the national safety authority must decide on an application within 4 months of receiving all information. |
| q28 | multi | 0 | 1 |  | 1 | The answer is incorrect because it missing a key fact from the reference answer (surveillance site visits at least once every 12 months). However, it is fully supported by the retrieved passages. |
| q30 | unanswerable | 1 | 0 |  |  | The assistant correctly states that the corpus does not cover the question and does not invent any rules or fine amounts. However, it fails on support because it explicitly names a law (Ley 38/2015 del Sector Ferroviario) and an authority (AESF) that are not present in the retrieved passages. |
| q31 | unanswerable | 0 | 0 | answered_unanswerable |  | The answer fails to explicitly state that the provided corpus does not contain the answer. Additionally, the mention of 'national track standards implementing it' is a claim not supported by the retrieved passages. |
| q32 | unanswerable | 1 | 0 |  |  | The assistant correctly identifies that the corpus does not contain the answer and does not invent rules. However, it mentions external directives and authorities not present in the retrieved passages (e.g., Directive (EU) 2016/797, AESF, ERA), making it unsupported. |
| q33 | unanswerable | 1 | 0 |  |  | The assistant correctly states that the corpus does not cover the question. However, it mentions 'national safety rules', which are not mentioned in the retrieved passages, making that claim/pointer unsupported. |
