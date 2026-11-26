# Evaluation summary

Written by `evaluate.py`; every number below is computed from the files next to this one.

## Set-up

- questions: 45 (20 single, 12 multi, 13 unanswerable)
- retrieval the agent used (design + mode @ passages per search): structure+dense@k5
- agent model: gemini-3.5-flash-lite; judge model: gemini-3.1-flash-lite
- written: 2026-11-25 22:33

## Retrieval (hit rate: an expected passage is in the top k; multi questions need all their passages)

| design + mode | hit@1 | hit@3 | hit@5 | words added to the prompt (top 5, mean) |
|---|---|---|---|---|
| fixed+dense | 53% | 78% | 91% | 1249 |
| fixed+bm25 | 41% | 69% | 78% | 1250 |
| fixed+hybrid | 53% | 81% | 91% | 1249 |
| structure+dense | 56% | 91% | 94% | 1055 |
| structure+bm25 | 38% | 75% | 78% | 1030 |
| structure+hybrid | 50% | 88% | 91% | 1047 |

Best by hit@5, then hit@3, then hit@1: **structure + dense**. The server serves: structure + dense, k=5.

## Agent answers, code checks

| kind | questions | code checks pass | valid citations | expected passage retrieved |
|---|---|---|---|---|
| single | 20 | 95% | 95% | 100% |
| multi | 12 | 83% | 100% | 83% |
| unanswerable | 13 | 92% | 100% | - |

## LLM judge

| measure | result | bar | met |
|---|---|---|---|
| correct_answerable | 84% | 85% | NO |
| refusal_unanswerable | 69% | 90% | NO |
| supported | 93% | 90% | yes |
| citations_valid | 98% | 95% | yes |

## Your grades (24 answers)

correct: 83%, supported: 75%.

## Agreement, judge versus you

| field | agreement | Cohen's kappa | judge too lenient | judge too strict |
|---|---|---|---|---|
| correct | 67% | -0.2 | 4 | 4 |
| supported | 71% | -0.077 | 6 | 1 |

Compared on 24 answers that you graded. "Too lenient" = the judge said 1 where you said 0.

## Failures

| category | count |
|---|---|
| retrieval miss | 6 |
| wrong answer from the right passage | 1 |
| unsupported claim | 4 |
| wrong refusal | 0 |
| bad test question | 0 |

| id | kind | category | graded by | why |
|---|---|---|---|---|
| q07 | single | retrieval miss | you | 1 |
| q10 | single | unsupported claim | judge | The answer misses the key fact that a declaration is sufficient for operations that fit a standard scenario, as mentioned in the reference answer. |
| q12 | single | retrieval miss | you | 1 |
| q18 | single | retrieval miss | you | 1 |
| q19 | single | retrieval miss | you | 1 |
| q22 | multi | wrong answer from the right passage | judge | The answer fails to mention that a class C3 drone must have a maximum characteristic dimension below 3 m, which is a key fact defined in the reference. |
| q34 | unanswerable | unsupported claim | judge | The answer provides information about national fees that is not present in the provided evidence, violating the requirement for the answer to be supported by th |
| q37 | unanswerable | retrieval miss | you | 1 |
| q43 | multi | retrieval miss | you | 1 |
| q48 | unanswerable | unsupported claim | judge | The answer provides external information about Member States setting their own fees, which is not stated in the provided evidence. |
| q49 | unanswerable | unsupported claim | judge | The assistant failed to explicitly state that the requirement is 'not covered' as requested for an unanswerable question, instead providing an answer that impli |

## Adding a document

Question q30: Which Spanish authority is responsible for running the national register of drone operators?

- before: NOT COVERED: The provided EU drone regulations require Member States to establish and maintain registration systems for drone operators [Reg. 2019/947, Article 14], but they do not name the specific national authority (such as Spain's *Agencia Estatal de Seguridad Aérea* - AESA) responsible for running Spain's national register.
- add_document, user declines: The file was not added. Please let me know how I can help you with the existing drone regulations!
- add_document, user approves: Indexed 'RD-517-2024': 194 chunks (0 newly embedded, 194 reused). It is searchable now.
- same file again: 'RD-517-2024' is already indexed (194 chunks); nothing to do.
- after: The authority responsible for establishing and managing the national register of drone operators (*Registro de operadores de UAS*) in Spain is the **Dirección de Seguridad de Aeronaves de la Agencia Estatal de Seguridad Aérea** (the Aircraft Safety Directorate of the State Aviation Safety Agency) [RD-517-2024, Artículo 48].
- the question flipped from NOT COVERED to an answer citing the added file: True (cites the expected article RD-517-2024, Artículo 48: True)
- controls q31, q32 still refused: True


## Cost per question (agent)

| measure | mean | median | p90 | max |
|---|---|---|---|---|
| tokens | 5719.4 | 4511 | 9757 | 14075 |
| input tokens | 5506.6 | 4314 | 9497 | 13784 |
| output tokens | 212.9 | 173 | 461 | 545 |
| seconds | 11.6 | 7.7 | 26.7 | 46.9 |
| model calls | 2.3 | 2 | 3 | 4 |
| searches (= embeddings) | 1.2 | 1 | 2 | 2 |

Citation-verifier retries over all questions: 5. Judge, per question: 2568.8 tokens, 5.8 s.
