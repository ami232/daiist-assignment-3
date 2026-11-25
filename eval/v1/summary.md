# Evaluation summary

## Retrieval (answerable questions)

| design | chunks | hit@1 | hit@3 | hit@5 | all@5 (multi: both passages) | words in top 5 |
|---|---|---|---|---|---|---|
| fixed+dense | 429 | 0.577 | 0.885 | 0.962 | 0.885 | 1250 |
| section+dense | 475 | 0.846 | 1.0 | 1.0 | 0.962 | 1078 |
| section+bm25 | 475 | 0.462 | 0.769 | 0.846 | 0.731 | 1016 |
| fixed+hybrid | 429 | 0.577 | 0.808 | 0.923 | 0.885 | 1250 |
| section+hybrid | 475 | 0.692 | 0.923 | 1.0 | 0.962 | 1057 |

## End to end

- **questions**: 32
- **correct (judge)**: 31
- **answerable correct**: 25
- **answerable**: 26
- **unsupported (judge)**: 5
- **correct refusals**: 6
- **unanswerable**: 6
- **wrong refusals**: 0
- **invalid citations**: 0
- **citation guardrail fired**: 9
- **failures by cause (judge)**: {'unsupported claim': 5}
- **human-graded answers**: 32
- **correct (human)**: 31
- **unsupported (human)**: 12
- **failures by cause (human)**: {'unsupported claim': 12}
- **judge models**: {'gemini-3.5-flash': 13, 'gemini-flash-lite-latest': 19}
- **mean tokens per question**: 9255
- **mean input tokens**: 8893
- **mean output tokens**: 362
- **mean seconds per question**: 9.7
- **mean tool calls**: 1.38
- **judge agreement**: {'graded': 32, 'correct_agreement': 0.938, 'correct_kappa': -0.032, 'correct_disagreements': ['q05', 'q25'], 'supported_agreement': 0.719, 'supported_kappa': 0.321, 'supported_disagreements': ['q11', 'q15', 'q16', 'q20', 'q23', 'q24', 'q25', 'q30', 'q31']}

## Failures (by human labels where graded, else judge)

| id | kind | cause (human) | cause (judge) | human notes | judge reason |
|---|---|---|---|---|---|
| q03 | single | unsupported claim | unsupported claim | Closing caveat says Member States can set Article 15 geographical zones; no retrieved passage contains Article 15. | The answer correctly identifies that registration is required based on the 250 g weight threshold, but it references Article 15 and UAS geographical zones which are not present in the retrieved passages. |
| q04 | single | unsupported claim | unsupported claim | Same uncited Article 15 caveat; retrieved passages are only A2/A3 rules and AMC. | The assistant correctly identifies the 150-metre horizontal distance requirement and the condition regarding uninvolved persons, but includes an extra claim regarding Article 15 and Member State geographical zones that is not present in the retrieved passages. |
| q05 | single | unsupported claim | unsupported claim | Same uncited Article 15 caveat; no Article 15 text in retrieved passages. | The assistant missed the reference condition that the UA must never overfly uninvolved persons, and it included an unsupported claim regarding Member States defining geographical zones under Article 15 that does not appear in the retrieved passages. |
| q09 | single | unsupported claim | unsupported claim | Same uncited Article 15 caveat; no Article 15 text in retrieved passages. | The answer correctly states the mass and speed limits for a class C0 drone, but it includes an extra note regarding Article 15 of Regulation (EU) 2019/947 which is not present in the retrieved passages. |
| q11 | single | unsupported claim |  | Says Article 15 zones may restrict or prohibit night flights; passages only mention zones in general, nothing about night. | The assistant correctly states that a green flashing light must be activated when flying at night, which fully answers the question according to the reference, and all claims are supported by the provided text. |
| q15 | single | unsupported claim |  | Same uncited Article 15 caveat; no Article 15 text in retrieved passages. | The assistant correctly states the 50-metre distance for follow-up mode in subcategory A1, matching the reference answer and supported by the retrieved passages. |
| q16 | single | unsupported claim |  | Same uncited Article 15 caveat; no Article 15 text in retrieved passages. | The assistant correctly answers 'No' and provides the exact conditions and facts supported by Article 14 of Regulation (EU) 2019/947 in the retrieved passages. |
| q20 | single | unsupported claim |  | Same uncited Article 15 caveat; no Article 15 text in retrieved passages. | The assistant correctly states that a class C5 drone must be limited to not more than 5 m/s in low-speed mode (unless tethered), which matches the reference answer and is fully supported by the retrieved passages. |
| q23 | multi | unsupported claim |  | Closing warning about Article 15 zones is not in the retrieved passages. | The assistant fully answers the question, aligns with the reference answer on all points (distances, measurement method, 1:1 rule, low-speed mode exception), and every claim is supported by the retrieved passages. |
| q24 | multi | unsupported claim |  | Claims the national portal is typically run by the national aviation authority and adds an Article 15 caveat; neither is in the retrieved passages. | The assistant correctly states where to register and details the exact format and components of the registration number as specified in the reference. |
| q25 | multi | unsupported claim |  | Adds that a modified C1 could 'potentially' be re-evaluated under other open category rules such as A3; the AMC says it may only be operated in the specific category (the privately-built exception is for C4 only). Misleading and unsupported. | The assistant correctly details the conditions under which part replacements or modifications affect the C1 class status and subcategory A1 eligibility, completely supported by the provided text. |
| q30 | unanswerable |  | unsupported claim |  | The assistant correctly identifies that the corpus does not cover FAA rules, but includes external knowledge about Florida and US regulations not found in the retrieved EU drone rule passages. |
| q31 | unanswerable | unsupported claim |  | Cites Article 14 for 'not set by EU rules and falls under national law', but Article 14(2)(d) says 'if required by Union or national law'; also adds an uncited Article 15 caveat. | The assistant correctly identified that the corpus does not cover specific national insurance amounts and directed the user to national authorities, matching the reference answer. |
