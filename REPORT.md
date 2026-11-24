# Assignment 3 Report

- **Name**:
- **Student ID**:
- **Group**: [BBADBA 5A | BBADBA 5B | PPLEDBA 5A]

## Use case

*Who asks, what they do with the answer, and what a wrong answer costs compared with "I don't know".*

## Corpus

*Table: document, URL, date, licence, words.*

## Ingestion

*How you extract, clean and chunk; one extraction problem you fixed; chunk metadata; number of chunks.*

## Test set

*How you wrote it, counts by kind, two examples.*

## Retrieval

*Hit rate at 1/3/5 per design, words added to the prompt, the design you chose.*

## Tools and subagent

*Your tools' descriptions, one search result, the subagent's instructions, one transcript from your editor.*

### Transcript: Claude Code delegating to the `corpus-researcher` subagent

**User:** use the subagent corpus-researcher to answer: Is a nutrition declaration mandatory for a beer with 5% alcohol?

**Claude Code → subagent `corpus-researcher`** ("Beer nutrition declaration question"):

> Answer this question from the corpus, with citations: Is a nutrition declaration mandatory for a beer with 5% alcohol?
>
> Search the corpus, cite every claim with the label shown in the results (e.g. [REG_1169_2011, Article X]), and say clearly if any part of the question is not covered. Include in your report the queries you ran and the passage labels you relied on.

*Subagent finished (its own transcript, with the searches, is under `/tasks`).*

<details><summary>Claude Code's first reply (in Spanish)</summary>

El subagente ha terminado. Esto es lo que encontró en el corpus.

Respuesta: no, por norma general no es obligatoria
Una cerveza de 5% está por encima del umbral de 1,2% de alcohol. Por eso no tiene que llevar declaración nutricional ni lista de ingredientes [REG_1169_2011, Article 16].

Matices que da el corpus:

Otras normas. La exención se aplica "sin perjuicio" de otras disposiciones de la UE que exijan la declaración [REG_1169_2011, Article 16]. La guía de la Comisión añade que también la puede exigir una medida nacional [QA_NOTICE_2018, Section 3.6.1].
Declaraciones (claims). Si el producto lleva una declaración nutricional o de propiedades saludables, el etiquetado nutricional pasa a ser obligatorio [REG_1169_2011, Article 49].
Aplicar esto a la cerveza es una deducción del subagente, que lo avisó. Une dos pasajes, pero ninguno lo dice textualmente para bebidas alcohólicas. El equipo debería confirmarlo antes de dar por buena esa regla.
Qué declaraciones puede llevar una cerveza. Ninguna de propiedades saludables. Las únicas declaraciones nutricionales permitidas se refieren a la reducción del contenido de alcohol o de energía [REG_1924_2006, Article 4 (part 2)].
Si se pone de forma voluntaria. Debe seguir las reglas de la declaración obligatoria. En bebidas alcohólicas puede limitarse solo al valor energético [QA_NOTICE_2018, Section 3.6.1].
Lo que sí es obligatorio aunque no se haya preguntado: el grado alcohólico, con como máximo un decimal seguido de "% vol" [REG_1169_2011, Article 28]. Para cervezas de hasta 5,5% vol la tolerancia es de ±0,5% vol [REG_1169_2011, Annex XII].
Lo que el corpus no cubre
Si hoy existe una norma posterior que lo exija. El Artículo 16 pedía a la Comisión un informe para el 13 de diciembre de 2014 y, si procedía, una propuesta legislativa sobre información nutricional obligatoria para bebidas alcohólicas [REG_1169_2011, Article 16]. El corpus no recoge qué pasó después. El equipo debe consultar la normativa vigente antes de aprobar la etiqueta.
Las normas nacionales sobre declaraciones de alcohol o energía reducidos o nulos que permite el Reglamento 1924/2006.
Por qué la respuesta está construida así: sigue las reglas 3 y 4 de AGENTS.md. Responde la parte que el corpus respalda, con citas, y separa lo que no se puede determinar. Así no se da por vigente una exención que podría haber cambiado desde 2014.

</details>

**User:** pero en ingles

**Claude Code:**

> **Answer: no, as a general rule it is not mandatory**
>
> A beer at 5% is above the 1.2% alcohol threshold, so it does not have to carry a nutrition declaration or a list of ingredients [REG_1169_2011, Article 16].
>
> Caveats from the corpus:
>
> - Other rules. The exemption applies "without prejudice to" other EU provisions that require a nutrition declaration [REG_1169_2011, Article 16]. The Commission guidance adds that a national measure can also require one [QA_NOTICE_2018, Section 3.6.1].
> - Claims. If the product carries a nutrition or health claim, nutrition labelling becomes mandatory [REG_1169_2011, Article 49]. Applying this to beer is the subagent's own conclusion, and it said so. It comes from reading two passages together, and neither one says it word for word for alcoholic drinks. The team should confirm it before relying on it.
> - Which claims a beer may carry. It may not carry any health claims. The only nutrition claims allowed are about a reduction in alcohol or energy content [REG_1924_2006, Article 4 (part 2)].
> - If given voluntarily. The declaration must follow the rules for the mandatory one. For alcoholic drinks it may be limited to the energy value alone [QA_NOTICE_2018, Section 3.6.1].
> - What is mandatory, even though you didn't ask: the alcoholic strength, as a figure with no more than one decimal place followed by "% vol" [REG_1169_2011, Article 28]. For beers up to 5.5% vol the tolerance is ±0.5% vol [REG_1169_2011, Annex XII].
>
> **What the corpus does not cover**
>
> - Whether a later rule now requires it. Article 16 asked the Commission for a report by 13 December 2014 and, if appropriate, a legislative proposal on mandatory nutrition information for alcoholic drinks [REG_1169_2011, Article 16]. The corpus has nothing on what happened after that. The team needs to check the current rules before approving the label.
> - National rules on claims about reduced or zero alcohol or energy, which Regulation 1924/2006 allows.
>
> Why the answer is built this way: it follows rules 3 and 4 in AGENTS.md. It answers the part the corpus supports, with citations, and keeps apart what can't be determined from it. That way the answer doesn't present an exemption from 2014 as still current when it may have changed.

## Adding a document

*What happens when a document is already indexed. The unanswerable question, the document you added, the answer before and after.*

## Harness and guardrails

*Your AGENTS.md rules, the approval step, and your extra guardrail with one case where it fired.*

## Evaluation

*Code checks, the judge's rubric, your agreement with the judge, and results: correct, unsupported, correct refusals, wrong refusals.*

## Failures

*Failed questions by cause, with counts, and what to fix first.*

## Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

## AI use

*What you used and how, or "none".*
