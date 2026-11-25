# Retrieval results

Hit@k: the expected passage is among the top k chunks (multi: all expected passages).
Any@k (multi only): at least one expected passage in the top k. MRR: mean reciprocal rank of the first hit.
Prompt words: words the top 5 chunks add to the prompt.

| Design | Questions | Hit@1 | Hit@3 | Hit@5 | MRR | Multi any@5 | Prompt words (top 5) | Top-1 score answerable | Top-1 score unanswerable |
|---|---|---|---|---|---|---|---|---|---|
| section | 37 | 0.59 | 0.84 | 0.92 | 0.72 | n/a | 780 | 0.819 | n/a |
| fixed | 37 | 0.38 | 0.73 | 0.84 | 0.56 | n/a | 750 | 0.821 | n/a |

## By kind

| Design | Kind | n | Hit@1 | Hit@3 | Hit@5 |
|---|---|---|---|---|---|
| section | single | 37 | 0.59 | 0.84 | 0.92 |
| fixed | single | 37 | 0.38 | 0.73 | 0.84 |

## Misses at k=5

- section q08 (expected ranks -): warfarin 14.3 Myocardial Infarction (0.78) | warfarin 14.3 Myocardial Infarction (0.78) | warfarin Medication Guide (0.77) | warfarin 1 Indications And Usage (0.77) | warfarin Medication Guide (0.76)
- section q17 (expected ranks -): warfarin 5.7 Use in Pregnant Women with Mechanica (0.87) | warfarin 8.1 Pregnancy (0.87) | warfarin Medication Guide (0.85) | warfarin 8.1 Pregnancy (0.84) | warfarin 8.3 Females and Males of Reproductive Po (0.83)
- section q29 (expected ranks -): amiodarone 7 Drug Interactions (0.80) | warfarin Medication Guide (0.79) | amiodarone 7 Drug Interactions (0.78) | amiodarone 12.3 Pharmacokinetics (0.78) | warfarin 7.4 Antibiotics and Antifungals (0.78)
- fixed q01 (expected ranks -): warfarin Medication Guide (0.88) | warfarin 17 Patient Counseling Information (0.85) | warfarin Medication Guide (0.85) | warfarin 2.4 Monitoring to Achieve Optimal Antico (0.84) | warfarin Medication Guide (0.84)
- fixed q18 (expected ranks -): warfarin Medication Guide (0.83) | warfarin 10.1 Signs and Symptoms (0.81) | warfarin Medication Guide (0.81) | warfarin Medication Guide (0.81) | warfarin Medication Guide (0.80)
- fixed q19 (expected ranks -): warfarin Medication Guide (0.84) | warfarin Medication Guide (0.83) | warfarin 17 Patient Counseling Information (0.82) | warfarin 17 Patient Counseling Information (0.81) | warfarin Medication Guide (0.81)
- fixed q27 (expected ranks -): warfarin 5.1 Hemorrhage (0.81) | warfarin Medication Guide (0.81) | warfarin 17 Patient Counseling Information (0.81) | warfarin Medication Guide (0.81) | warfarin Medication Guide (0.80)
- fixed q29 (expected ranks -): amiodarone Medication Guide (0.79) | amiodarone 7 Drug Interactions (0.79) | amiodarone 7 Drug Interactions (0.79) | amiodarone 7 Drug Interactions (0.79) | amiodarone Medication Guide (0.78)
- fixed q31 (expected ranks -): warfarin Medication Guide (0.81) | warfarin Medication Guide (0.80) | warfarin 5.7 Use in Pregnant Women with Mechanica (0.80) | warfarin Medication Guide (0.80) | warfarin Medication Guide (0.80)
