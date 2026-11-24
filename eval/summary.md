# Evaluation summary

## Retrieval (answerable questions)

| design | mode | chunks | hit@1 | hit@3 | hit@5 | both passages@5 (multi) | words in prompt (k=5) |
|---|---|---|---|---|---|---|---|
| structured | dense | 378 | 81% | 100% | 100% | 67% | 1196 |
| structured | bm25 | 378 | 47% | 59% | 66% | 0% | 1253 |
| structured | hybrid | 378 | 53% | 75% | 88% | 33% | 1244 |
| fixed | dense | 211 | 66% | 97% | 97% | 50% | 1989 |
| fixed | bm25 | 211 | 38% | 59% | 69% | 0% | 1981 |
| fixed | hybrid | 211 | 56% | 88% | 91% | 33% | 1982 |

Chosen: **structured + dense**, k = 5.

## End to end

| outcome | count |
|---|---|
| correct | 32 |
| incorrect | 0 |
| unsupported | 0 |
| wrong refusal | 0 |
| correct refusal | 6 |
| answered unanswerable | 0 |

## Code checks

```
{
  "citations_valid": 38,
  "uncited_non_refusals": 0,
  "expected_article_cited": 32,
  "answerable": 32,
  "unanswerable": 6,
  "guardrail": {
    "passed": 37,
    "repaired": 1,
    "blocked": 0
  }
}
```

## Judge agreement with human grades

```
{
  "graded": 0
}
```

## Failures

| cause | count | questions |
|---|---|---|

## Cost per question

```
{
  "avg_tokens": 4897,
  "avg_seconds": 13.1,
  "avg_tool_calls": 1.18,
  "avg_judge_tokens": 2466
}
```

## Every answer

| id | kind | result | cause | judge reason |
|---|---|---|---|---|
| q01 | single | correct |  | The answer accurately reflects the requirements of Article 33 of the GDPR regarding the notification timeline and the exception for low-risk breaches. |
| q02 | single | correct |  | The answer accurately states the maximum fine amounts and conditions as specified in the provided text. |
| q03 | single | correct |  | The answer accurately reflects the age requirements for parental consent as stated in Article 8 of the GDPR. |
| q04 | single | correct |  | The answer accurately reflects the deadlines and conditions for responding to data subject requests as provided in the retrieved passages. |
| q05 | single | correct |  | The answer accurately reflects the requirements for designating a data protection officer as outlined in the provided GDPR articles. |
| q06 | single | correct |  | The answer accurately lists all six legal grounds for processing as defined in Article 6 of the GDPR and includes the necessary condition regarding public authorities. |
| q07 | single | correct |  | The answer accurately identifies the general requirement for a DPIA and the specific examples listed in Article 35, while also noting the role of supervisory authorities. |
| q08 | single | correct |  | The answer accurately reflects the requirements of GDPR Article 28 regarding sub-processor authorization and the controller's right to object. |
| q09 | single | correct |  | The answer accurately reflects the conditions for extraterritorial application of the GDPR as stated in Article 3 of the provided text. |
| q10 | single | correct |  | The answer accurately defines pseudonymisation according to Article 4(5) and includes relevant context from the provided passages. |
| q11 | single | correct |  | The answer correctly addresses all parts of the question and reference answer, including the right to withdraw, the effect on prior processing, the ease of withdrawal, and the requirement to inform the user beforehand. |
| q12 | single | correct |  | The answer accurately identifies the conditions for the right to data portability and the exceptions as provided in the retrieved passages. |
| q13 | single | correct |  | The answer accurately reflects the provided text and correctly states that the GDPR does not apply to anonymous information. |
| q14 | single | correct |  | The answer accurately reflects the GDPR's position on deceased persons as stated in the provided recitals. |
| q15 | single | correct |  | The answer accurately reflects the criteria for the record-keeping exemption under Article 30 of the GDPR. |
| q16 | single | correct |  | The assistant accurately and comprehensively lists the information requirements set out in Article 13 of the GDPR, which is the correct source for data collected directly from the data subject. |
| q17 | single | correct |  | The answer accurately reflects the requirements for consent and the exceptions provided in the retrieved text. |
| q18 | single | correct |  | The answer accurately reflects the conditions for the 'soft opt-in' exception as described in Article 13 of the ePrivacy Directive. |
| q19 | single | correct |  | The assistant correctly identified the 'without undue delay' requirement and supported it with the provided text. |
| q20 | single | correct |  | The answer accurately reflects the requirements of Article 6 of the ePrivacy Directive and correctly identifies the relevant exceptions. |
| q21 | single | correct |  | The answer accurately explains that the time period is not fixed by the clauses but is a placeholder to be filled in by the parties, consistent with the reference answer and retrieved passages. |
| q22 | single | correct |  | The answer accurately reflects the deadline and conditions specified in the retrieved passages. |
| q23 | single | correct |  | The answer accurately summarizes the obligations of the data importer regarding public authority access as outlined in the provided SCCs. |
| q24 | single | correct |  | The answer accurately summarizes the governing law requirements for the different modules as provided in the retrieved passages. |
| q25 | single | correct |  | The answer accurately reflects the requirements for accession as described in the provided source text. |
| q26 | single | correct |  | The answer accurately summarizes the tasks of the data protection officer as defined in Article 39 of the GDPR and is fully supported by the provided text. |
| m01 | multi | correct |  | The answer correctly identifies the requirement to inform data subjects in cases of high risk and provides the correct 72-hour deadline for notifying the supervisory authority, citing the appropriate articles. |
| m02 | multi | correct |  | The answer correctly identifies the fine amount and cites the relevant article from the provided passages. |
| m03 | multi | correct |  | The answer accurately reflects the requirements for notifying recipients and handling public data as outlined in the provided GDPR articles. |
| m04 | multi | correct |  | The answer accurately addresses both parts of the question using the provided source material. |
| m05 | multi | correct |  | The answer correctly identifies that consent is required under the ePrivacy Directive for storing information on a user's device, correctly identifies the limited exceptions, and correctly concludes that legitimate interests cannot be used as a substitute. |
| m06 | multi | correct |  | The answer accurately reflects the GDPR requirements and the specific options provided in the 2021 SCCs for sub-processor authorization. |
| u01 | unanswerable | correct refusal |  | The assistant correctly identified that the provided corpus does not contain the requested Decision 2021/915. |
| u02 | unanswerable | correct refusal |  | The assistant correctly identified that the corpus does not contain the EU AI Act. |
| u03 | unanswerable | correct refusal |  | The assistant correctly identified that the provided corpus does not contain information regarding the EU-US Data Privacy Framework. |
| u04 | unanswerable | correct refusal |  | The assistant correctly identified that the corpus does not contain the specific national law for Spain and explained why. |
| u05 | unanswerable | correct refusal |  | The assistant correctly identified that the provided corpus does not contain information on the validity period of cookie consent. |
| u06 | unanswerable | correct refusal |  | The assistant correctly identified that the corpus does not contain the NIS2 Directive. |
