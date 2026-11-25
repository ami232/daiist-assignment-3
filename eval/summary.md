# Evaluation summary

Model: gemini-3.1-flash-lite. The agent searches the `article` design.

## Retrieval

| design | hit@1 | hit@3 | hit@5 | words added to the prompt (k=5) |
|---|---|---|---|---|
| article | 0.68 | 0.92 | 1.00 | 1652 |
| fixed | 0.64 | 0.92 | 0.96 | 2250 |

## Results

| measure | value |
|---|---|
| correct (answerable questions) | 22 of 25 |
| unsupported (answer has a claim that is not in the passages) | 0 of 25 |
| wrong refusals (answerable questions refused) | 3 of 25 |
| correct refusals (unanswerable questions) | 5 of 5 |
| citations valid (code check) | 30 of 30 |
| guardrail fired | 5 of 30 |

## Agreement with my labels

| grade | answers I graded | judge agrees with me |
|---|---|---|
| correct | 20 | 20 |
| supported | 20 | 19 |

## Failures

| id | kind | outcome | cause | judge's reason |
|---|---|---|---|---|
| q18 | single | wrong refusal | wrong refusal | The answer incorrectly claims the corpus does not cover the question, as the retrieved passages clearly state in Article 4 that data localisation requirements are prohibited unless justified on grounds of public security. |
| q20 | single | wrong refusal | retrieval miss | The corpus contains the relevant information in the Free Flow of Non-Personal Data Regulation (EU) 2018/1807, Recital 10, which explains that the regulation applies to non-personal data and provides for a coherent set of rules with the GDPR without requiring separate storage. |
| q23 | multi | wrong refusal | wrong refusal | The answer incorrectly states that the corpus does not cover the question, even though Articles 46 and 49 of the provided GDPR text clearly outline options for international data transfers in the absence of an adequacy decision. |

## Cost per question

| per question | mean | max |
|---|---|---|
| tokens | 3797 | 4301 |
| seconds | 19.2 | 85.7 |

## Adding a document

Question q28: Which thematic categories of high-value datasets must public sector bodies make available free of charge?

- add_document, first call: Added 'open_data': 51 chunks stored, 51 newly embedded.
- add_document, second call: 'open_data' is already indexed with the same content (51 chunks). Nothing changed.

**Before:** The corpus does not cover this question.

**After:** The thematic categories of high-value datasets are [open_data | Annex I]:

1. Geospatial
2. Earth observation and environment
3. Meteorological
4. Statistics
5. Companies and company ownership
6. Mobility

The Commission adopts implementing acts to identify specific datasets within these categories that must be made available free of charge [open_data | Article 14(1)]. This requirement is subject to specific exceptions, including for libraries, museums, archives, and cases where it could cause budget-related hardship or distortions of competition [open_data | Article 14(3), (4), (5)].
