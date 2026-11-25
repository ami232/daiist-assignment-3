# Evaluation summary

## Retrieval (answerable questions)

| design | chunks | hit@1 | hit@3 | hit@5 | all@5 (multi: both passages) | words in top 5 |
|---|---|---|---|---|---|---|
| fixed+dense | 429 | 0.577 | 0.885 | 0.962 | 0.885 | 1250 |
| section+dense | 522 | 0.846 | 1.0 | 1.0 | 0.962 | 1078 |
| section+bm25 | 522 | 0.462 | 0.769 | 0.846 | 0.731 | 975 |
| fixed+hybrid | 429 | 0.577 | 0.808 | 0.923 | 0.885 | 1250 |
| section+hybrid | 522 | 0.692 | 0.923 | 1.0 | 0.962 | 1062 |

## End to end

- **questions**: 32
- **judged answers**: 32
- **correct (judge)**: 30
- **answerable correct**: 24
- **answerable**: 26
- **unsupported (judge)**: 0
- **correct refusals**: 5
- **unanswerable**: 6
- **wrong refusals**: 0
- **invalid citations**: 0
- **citation guardrail fired**: 2
- **failures by cause (judge)**: {'wrong answer from right passage': 2}
- **human-graded answers**: 32
- **correct (human)**: 28
- **unsupported (human)**: 4
- **failures by cause (human)**: {'wrong answer from right passage': 3, 'unsupported claim': 4}
- **judge models**: {'gemini-3.6-flash': 1, 'gemini-flash-lite-latest': 31}
- **mean tokens per question**: 7218
- **mean input tokens**: 6948
- **mean output tokens**: 270
- **mean seconds per question**: 6.9
- **mean tool calls**: 1.19
- **judge agreement**: {'graded': 32, 'correct_agreement': 0.938, 'correct_kappa': 0.636, 'correct_disagreements': ['q04', 'q25'], 'supported_agreement': 0.875, 'supported_kappa': 0.0, 'supported_disagreements': ['q24', 'q25', 'q27', 'q31']}

## Failures (by human labels where graded, else judge)

| id | kind | cause (human) | cause (judge) | human notes | judge reason |
|---|---|---|---|---|---|
| q02 | single | wrong answer from right passage | wrong answer from right passage | Gives 16 as the minimum age but omits that Member States may lower it by up to 4 years in the open category (valid only in their territory), which my reference includes. | The assistant missed the reference point stating that Member States may lower the minimum age by up to 4 years for the open category (valid only in their territory). |
| q04 | single | wrong answer from right passage |  | Gives the 150 m distance but omits the condition that no uninvolved person is expected to be endangered, which my reference includes (graded strictly, consistent with q02). | The assistant correctly states the 150-metre distance requirement and includes relevant additional details from the text. |
| q22 | multi | wrong answer from right passage | wrong answer from right passage | Describes the C1 technical features (mass, speed, height limit, remote ID, geo-awareness, etc.) but never mentions the green flashing light, which my reference lists as a C1 feature (graded strictly, consistent with q02 and q04). | The assistant failed to mention the requirement for a green flashing light, which was stated in the reference answer. |
| q24 | multi | unsupported claim |  | Says registration runs through a system established by the competent national aviation authority; Article 14 says Member States establish the systems and the retrieved passages do not name the authority. | The assistant correctly identifies the registration location rules and fully describes the format of the UAS operator registration number according to the provided passages. |
| q25 | multi | unsupported claim |  | Still says a modified C1 may be operated 'unless it qualifies as a privately built UAS under subcategory A3'; the AMC says it may only be operated in the specific category (the privately built exception is for C4 only). Misleading and not in the passages. | The assistant correctly states that changing parts is allowed if done for maintenance using original or manufacturer-approved parts, and that unauthorized modifications invalidate class conformity, requiring operation in the specific category instead. |
| q27 | unanswerable | unsupported claim |  | Correct refusal, but names Regulations (EU) 2021/664, 2021/665 and 2021/666 as the U-space rules; those numbers are not in any retrieved passage. | The assistant correctly identified that the corpus does not cover the specific U-space regulations and directed the user to the national authority, matching the reference answer. |
| q31 | unanswerable | unsupported claim |  | Correct refusal, but says insurance is 'only mentioned ... if required by national law' (Article 14(2)(d) says 'Union or national law') and that minimums depend on national law; neither is in the retrieved passages. | The assistant correctly identified that the corpus does not cover specific liability insurance amounts and explained that such requirements depend on national law. |
