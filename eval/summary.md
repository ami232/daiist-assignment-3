# Evaluation summary

## Retrieval (answerable questions)

| design | chunks | hit@1 | hit@3 | hit@5 | words in prompt (top 5) |
|---|---|---|---|---|---|
| a | 482 | 0.56 | 0.64 | 0.72 | 737 |
| b | 442 | 0.56 | 0.64 | 0.80 | 886 |
- design a, single (n=18): hit@1 0.78, hit@3 0.83, hit@5 0.83
- design a, multi (n=7): hit@1 0.00, hit@3 0.14, hit@5 0.43
- design b, single (n=18): hit@1 0.78, hit@3 0.89, hit@5 1.00
- design b, multi (n=7): hit@1 0.00, hit@3 0.00, hit@5 0.29

## End to end (32 of 32 questions answered, 32 judged)

- correct and supported answers: 25 of 25 answerable
- unsupported answers (judge): 0
- correct refusals: 6 of 7 unanswerable
- wrong refusals (code check, answerable questions refused): 2
- code checks passed: 24 of 32
- guardrail flags: none

## Agreement with your grades

- no usable grades found in eval/human_labels.csv yet. Grade with eval/grading_sheet.md.

## Cost per question

- seconds: mean 19.6, median 5.7
- tokens in / out: mean 3624 / 173 (agent only; the judge adds one call per question)

## Failure candidates (check them by hand and fill final_category in eval/failures.csv)

- unsupported claim: 1

## Before / after adding a document

- question q19: How long should a shop keep its security camera recordings?
- document added: corpus/edpb_video_devices.pdf
- BEFORE: The GDPR does not specify a fixed retention period for security camera recordings. Under the principle of "storage limitation," personal data must be kept in a form that permits identification of data subjects for no longer than is necessary for the purposes for which the data are processed [gdpr, Article 5(1)(e)]. It is the responsibility of the controller to determine the appropriate retention period in accordance with these principles [edpb_breach_notification, para 124 (p.26)].
- AFTER: Personal data must not be stored longer than necessary for the purposes for which it is processed [edpb_video_devices, p.28]. For a small shop, a storage period of 24 hours is often sufficient to detect vandalism, though longer periods may be justified by factors like weekends or holidays [edpb_video_devices, p.28].

In general, data should ideally be erased automatically after a few days, and any storage period exceeding 72 hours requires stronger justification regarding its necessity and legitimacy [edpb_video_devices, p.28]. It is the controller's responsibility to define and justify the retention period based on the principles of necessity and proportionality [edpb_video_devices, p.28].
