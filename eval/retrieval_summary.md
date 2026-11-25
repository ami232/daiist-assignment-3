# Retrieval results

Hit@k: the expected passage is among the top k chunks (multi: all expected passages).
Any@k (multi only): at least one expected passage in the top k. MRR: mean reciprocal rank of the first hit.
Prompt words: words the top 5 chunks add to the prompt.

| Design | Questions | Hit@1 | Hit@3 | Hit@5 | MRR | Multi any@5 | Prompt words (top 5) | Top-1 score answerable | Top-1 score unanswerable |
|---|---|---|---|---|---|---|---|---|---|
| section | 43 | 0.51 | 0.77 | 0.86 | 0.73 | 0.83 | 770 | 0.819 | 0.762 |
| fixed | 43 | 0.33 | 0.65 | 0.77 | 0.58 | 1.00 | 749 | 0.821 | 0.764 |

## By kind

| Design | Kind | n | Hit@1 | Hit@3 | Hit@5 |
|---|---|---|---|---|---|
| section | single | 37 | 0.59 | 0.84 | 0.92 |
| section | multi | 6 | 0.00 | 0.33 | 0.50 |
| fixed | single | 37 | 0.38 | 0.73 | 0.84 |
| fixed | multi | 6 | 0.00 | 0.17 | 0.33 |

## Misses at k=5

- section q08 (expected ranks -): warfarin 14.3 Myocardial Infarction (0.78) | warfarin 14.3 Myocardial Infarction (0.78) | warfarin Medication Guide (0.77) | warfarin 1 Indications And Usage (0.77) | warfarin Medication Guide (0.76)
- section q17 (expected ranks -): warfarin 5.7 Use in Pregnant Women with Mechanica (0.87) | warfarin 8.1 Pregnancy (0.87) | warfarin Medication Guide (0.85) | warfarin 8.1 Pregnancy (0.84) | warfarin 8.3 Females and Males of Reproductive Po (0.83)
- section q29 (expected ranks -): amiodarone 7 Drug Interactions (0.80) | warfarin Medication Guide (0.79) | amiodarone 7 Drug Interactions (0.78) | amiodarone 12.3 Pharmacokinetics (0.78) | warfarin 7.4 Antibiotics and Antifungals (0.78)
- section q38 (expected ranks -;1): digoxin 7.2 Pharmacokinetic Drug Interactions (0.83) | digoxin 7 Drug Interactions (0.82) | digoxin 7.3 Potentially Significant Pharmacodyna (0.81) | digoxin 7.2 Pharmacokinetic Drug Interactions (0.79) | digoxin 7.3 Potentially Significant Pharmacodyna (0.79)
- section q39 (expected ranks -;-): warfarin Medication Guide (0.80) | warfarin 2.4 Monitoring to Achieve Optimal Antico (0.79) | warfarin 7.1 General Information (0.79) | warfarin 2.3 Initial and Maintenance Dosing (0.79) | warfarin 2.1 Individualized Dosing (0.79)
- section q42 (expected ranks 2;-): metoprolol 7.4 Negative Chronotropes (0.79) | amiodarone 7 Drug Interactions (0.78) | amiodarone 5.7 Bradycardia (0.78) | amiodarone 7 Drug Interactions (0.78) | amiodarone 7 Drug Interactions (0.78)
- fixed q01 (expected ranks -): warfarin Medication Guide (0.88) | warfarin 17 Patient Counseling Information (0.85) | warfarin Medication Guide (0.85) | warfarin 2.4 Monitoring to Achieve Optimal Antico (0.84) | warfarin Medication Guide (0.84)
- fixed q18 (expected ranks -): warfarin Medication Guide (0.83) | warfarin 10.1 Signs and Symptoms (0.81) | warfarin Medication Guide (0.81) | warfarin Medication Guide (0.81) | warfarin Medication Guide (0.80)
- fixed q19 (expected ranks -): warfarin Medication Guide (0.84) | warfarin Medication Guide (0.83) | warfarin 17 Patient Counseling Information (0.82) | warfarin 17 Patient Counseling Information (0.81) | warfarin Medication Guide (0.81)
- fixed q27 (expected ranks -): warfarin 5.1 Hemorrhage (0.81) | warfarin Medication Guide (0.81) | warfarin 17 Patient Counseling Information (0.81) | warfarin Medication Guide (0.81) | warfarin Medication Guide (0.80)
- fixed q29 (expected ranks -): amiodarone Medication Guide (0.79) | amiodarone 7 Drug Interactions (0.79) | amiodarone 7 Drug Interactions (0.79) | amiodarone 7 Drug Interactions (0.79) | amiodarone Medication Guide (0.78)
- fixed q31 (expected ranks -): warfarin Medication Guide (0.81) | warfarin Medication Guide (0.80) | warfarin 5.7 Use in Pregnant Women with Mechanica (0.80) | warfarin Medication Guide (0.80) | warfarin Medication Guide (0.80)
- fixed q38 (expected ranks -;1): digoxin 7.2 Pharmacokinetic Drug Interactions (0.84) | digoxin 7.2 Pharmacokinetic Drug Interactions (0.82) | digoxin 6.1 Clinical Trials Experience (0.82) | digoxin 7.3 Potentially Significant Pharmacodyna (0.82) | digoxin 1.1 Heart Failure in Adults (0.80)
- fixed q39 (expected ranks -;5): amiodarone Medication Guide (0.81) | warfarin 2.3 Initial and Maintenance Dosing (0.79) | warfarin 5.1 Hemorrhage (0.79) | warfarin Medication Guide (0.78) | warfarin 7.1 General Information (0.78)
- fixed q41 (expected ranks 1;-): apixaban 2.4 Temporary Interruption for Surgery a (0.83) | apixaban 2.5 Converting from or to ELIQUIS (0.81) | apixaban 2.3 Missed Dose (0.81) | apixaban Medication Guide (0.80) | apixaban Medication Guide (0.79)
- fixed q42 (expected ranks 3;-): amiodarone Medication Guide (0.79) | amiodarone 5.6 Thyroid Abnormalities (0.78) | amiodarone 7 Drug Interactions (0.78) | amiodarone 7 Drug Interactions (0.78) | amiodarone 7 Drug Interactions (0.78)
