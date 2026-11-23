# Assignment 3 Report

- **Name**:
- **Student ID**:
- **Group**: [BBADBA 5A | BBADBA 5B | PPLEDBA 5A]

## Use case

A sample use case would be myself, Javier Arce. Two and a half years ago I found myself in this exact situation: 20 years old and trying to take my DJ entrepreneurial project to a more serious level. At that moment I had some gigs and was making about 150–200 euros per month. However, as I started scaling my business and getting more clients, I had to formalise my business, and a tool like this would have been great to answer the many questions I had at that time. The tool would be used to decide if it was legally appropriate for me to become an autónomo, and what rights and obligations derived from this. Then, with this information, I could talk to an expert and analyse the economic viability of the operation.

In terms of the correctness of answers, users must know this is a chatbot with a RAG system behind, and that it therefore can make errors. The cost of an error will be highly dependent on what the error is about. If the question is about having to complete the 'Declaración de la Renta', and you are told you are not obliged to do so when you actually are (since 1 January 2023, anyone registered as autónomo at any point in the year must file it, first applied in the 2024 filing campaign), you can receive a fine for this. This specific question falls outside the indexed laws, so the assistant should refuse it, which is exactly the behaviour that matters when errors are costly. However, if the question is about what a mutua does or does not cover, the economic implications are less directly tied and probably less serious. Overall, I would say the cost of errors is relatively high, as it can have economic and legal implications for users if they do not make the right decisions.

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

### Subagent transcript (Claude Code, 2026-11-23)

The `corpus-researcher` subagent (`.claude/agents/corpus-researcher.md`, tools: `mcp__corpus__search` only) was called from Claude Code with a question taken from a real situation. It was not in the test set.

**Question passed to the subagent**

> Empecé a operar hace 10 días y todavía no me he dado de alta. Es esto un problema? Me puedo dar de alta de forma retrospectiva?

**Tool calls** (3 searches, under the limit of 4 set in its instructions)

| # | `search` query | Passages returned |
|---|---|---|
| 1 | `plazo solicitud de alta trabajador autónomo RETA inicio de actividad` | [LETA, Artículo 38 ter], [LGSS, Artículo 307], [LGSS, Artículo 305], [LGSS, Artículo 337] ×2 |
| 2 | `declaración censal de alta antes del inicio de actividades` | [RGAT, Artículo 9] ×3 parts, [RGAT, Artículo 13], [RGAT, Artículo 15] |
| 3 | `alta fuera de plazo efectos de las altas cotización desde el día de inicio de la actividad recargo` | [LGSS, Artículo 319], [LGSS, Artículo 307], [LETA, Artículo 38 ter], [LGSS, Artículo 313], [LETA, Artículo 25] |

Searches 1 and 2 ran in parallel. Each targets one of the two registrations: the RETA and the tax census. The third search looks for the consequences of a late registration.

**Answer returned by the subagent** (verbatim)

> Sí, puede ser un problema, tanto en Hacienda como en la Seguridad Social. Los fragmentos recuperados no dan un plazo concreto para el alta en el RETA, pero sí explican qué pasa con las cuotas de los días anteriores al alta.
>
> **Hacienda (declaración censal de alta)**
> - Quien deba figurar en el Censo de Empresarios, Profesionales y Retenedores tiene que presentar una declaración de alta en ese censo [RGAT, Artículo 9].
> - La declaración debe presentarse antes de empezar la actividad o de realizar las operaciones [RGAT, Artículo 9]. Esto es según el texto consolidado a 28 de octubre de 2026.
> - La actividad se considera empezada en cuanto se realiza cualquier entrega, prestación o adquisición de bienes o servicios, se cobra o se paga, o se contrata personal, con la finalidad de producir o distribuir bienes o servicios [RGAT, Artículo 9]. Si ya ha hecho alguna de estas cosas, el plazo para esta declaración ya ha pasado.
>
> **Seguridad Social (RETA)**
> - Las personas autónomas están obligadas a solicitar su afiliación y a comunicar su alta en el RETA "en los términos, plazos y condiciones" que fijan la ley y sus normas de desarrollo [LGSS, Artículo 307]. El fragmento no dice qué plazo es.
> - Si se cumplen los requisitos del régimen y no se pidió el alta, las cotizaciones de los periodos anteriores al alta se exigen igualmente. Esas cotizaciones cuentan para las prestaciones una vez pagadas con los recargos que correspondan [LGSS, Artículo 319].
> - Además de las sanciones administrativas por pagarlas fuera de plazo, esas cotizaciones generan intereses al tipo de interés legal del dinero, desde la fecha en que debieron pagarse [LGSS, Artículo 319]. Esto es según el texto consolidado a 11 de noviembre de 2026.
> - La cuota reducida por inicio de actividad (tarifa plana) hay que pedirla en el momento del alta en el RETA [LETA, Artículo 38 ter]. Conviene pedirla en la misma solicitud de alta.
>
> **Lo que no está cubierto**
> Sobre si se puede pedir el alta en el RETA con fecha anterior, qué plazo exacto hay, si un alta tardía afecta a la tarifa plana y cuánto serían los recargos o la sanción:
>
> > No se ha encontrado contenido relacionado a tu pregunta en los documentos a los que tengo acceso. Consulte con un técnico especialista.
>
> No he calculado cuánto tendría que pagar en cuotas atrasadas, recargos o intereses. Es mejor que un gestor o asesor lo calcule y que haga cuanto antes el alta en Hacienda y en el RETA.
>
> > Texto consolidado del BOE de carácter informativo; no tiene validez jurídica. Para efectos legales, consulte la publicación oficial.

**Check.** Every citation was checked against the indexed chunks.
- The rule "antes de iniciar la actividad" and the definition of when an activity starts are in RGAT art. 9.4. That text is in part 4/4 of the chunk, which search 2 returned.
- LGSS arts. 307 and 319 say what the answer claims.
- The consolidation dates (28-10-2026 for the RGAT, 11-11-2026 for the LGSS) match the index metadata.

The question was only partly covered, and the subagent applied rule 4. It answered what the corpus covers and used the fixed refusal phrase for what it does not: a backdated *alta* in the RETA, the exact deadline and the amount of the surcharges. It also followed rule 5: no amounts were calculated.

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
