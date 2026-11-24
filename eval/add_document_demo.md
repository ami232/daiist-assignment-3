# add_document demo: q30 before and after

**Question (q30):** What fine does Spain impose on an infrastructure manager that fails to submit its annual safety report on time?

## Before

Answer from stage 2 of `main.py evaluate` (design `article`, model `gemini-3.6-flash`), with only the four EU acts in the index.

```text
The corpus does not cover this question.

Directive (EU) 2016/798 requires infrastructure managers to submit an annual safety report to their national safety authority before 31 May of each year [Dir_2016_798, Article 9(6)-(7)] and mandates that Member States lay down rules on effective, proportionate, and dissuasive penalties for infringements [Dir_2016_798, Article 30]. However, the specific fine amounts established under Spanish national law are not contained in the corpus.

To determine the specific fine imposed in Spain, check Spanish national railway law (such as the *Ley 38/2015 del Sector Ferroviario*) or consult Spain's national safety authority (*Agencia Estatal de Seguridad Ferroviaria* — AESF).

Note: based on the acts as originally published (later amendments not included). Not legal advice; for binding decisions check the consolidated text on EUR-Lex.
```

- Searches: 'annual safety report fine penalty Spain'
- Retrieved passages: [Dir_2016_798, Article 19], [Dir_2016_798, Article 9(6)-(7)], [Dir_2016_798, Annex I], [Dir_2016_798, Article 30], [Dir_2016_798, Annex I, 5]
- Citations in the answer: [Dir_2016_798, Article 9(6)-(7)], [Dir_2016_798, Article 30]
- Guardrails fired: none
- Tokens: 4,531 input, 1,073 output; 8.5 s

## Adding the document

The consolidated Ley 38/2015 del Sector Ferroviario was added through the agent, with the approval guardrail asking first.

- File: `corpus_extra/BOE-A-2015-10440-consolidado.pdf` (source: https://www.boe.es/buscar/pdf/2015/BOE-A-2015-10440-consolidado.pdf)
- `add_document` was approved at the terminal prompt and ran once.
- Result: doc_id `BOE_A_2015_10440_consolidado`, 284 chunks added to the `article` collection.
- Checked in the index afterwards: the `article` collection holds 884 vectors (600 corpus + 284 new), all 284 with the same `doc_hash`; the `fixed` collection is unchanged (591).

## After

Same question, same agent, same model, with the law in the index.

- The agent answered that failing to submit the annual safety report on time is a **minor infringement** ("infracción leve"), fined **up to 7,500 euros**.
- Citations: `[BOE_A_2015_10440_consolidado, Artículo 108 (part 3/3)]` and `[BOE_A_2015_10440_consolidado, Artículo 109 (part 2/4)]`.
- Searches: 'fine penalty annual safety report Spain'; 'informe anual de seguridad sancion infraccion Ley 38/2015'; 'Artículo 109. Sanciones infracciones leves multa'.
- The citation guardrail did not fire: both cited passages were retrieved in this run.

## Verdict

**The "after" answer is wrong.** Checked against the stored chunk texts, with no model call.

What the law says:

- `Artículo 107 (part 3/7)`, under the heading "Artículo 107. Infracciones graves", point 1.15: "El incumplimiento de la obligación de los administradores de infraestructuras ferroviarias y de las empresas ferroviarias de presentar ante la autoridad nacional de seguridad el informe anual de seguridad." This is the **annual safety report** of the question, and not submitting it is a **serious** infringement.
- `Artículo 109 (part 1/4)`, point 1(b): "Las graves con multa de 7.501 hasta 38.000 euros." The lower range in the same sentence (751 to 6.300 euros) is for rail-transport infringements, which point 1.15 is not: it is listed before "2. Infracciones en materia de transporte ferroviario" begins.
- So the correct answer is: serious infringement, **7,501 to 38,000 euros**.

What the agent cited instead:

- `Artículo 108 (part 3/3)`, letter h): "El incumplimiento de la obligación de remitir a las autoridades competentes el informe anual o los partes de accidente fuera de los plazos reglamentariamente establecidos." This "informe anual" is the **dangerous-goods annual report**, not the annual safety report. Letter h) belongs to the group "3. Infracciones en materia de transporte de mercancías peligrosas", and the same chunk assigns responsibility for letters e) to h) to "la empresa obligada a tener consejero de seguridad" (the dangerous-goods safety adviser).
- `Artículo 109 (part 2/4)`, point 1(c): "Las leves con multa de hasta 7.500 euros." Quoted correctly, but it is the fine for the wrong infringement.

Why it happened:

| Search | Top 5 | Rank of `Artículo 107 (part 3/7)` |
|---|---|---|
| 'fine penalty annual safety report Spain' | Dir_2016_798 Article 19; Article 9(6)-(7); Article 30; Annex I; BOE Artículo 109 (part 4/4) | 24 |
| 'informe anual de seguridad sancion infraccion Ley 38/2015' | BOE Artículo 108 (part 3/3); Artículo 110; Artículo 109 (part 1/4); Artículo 109 (part 4/4); Artículo 112 | 7 |
| 'Artículo 109. Sanciones infracciones leves multa' | BOE Artículo 109 (part 2/4); Artículo 109 (part 1/4); Artículo 108 (part 1/3); Artículo 108 (part 3/3); Artículo 109 (part 3/4) | 13 |

- `Artículo 107 (part 3/7)`, the only passage that classifies the infringement, **was in none of the three top-5 lists** (ranks 24, 7 and 13, re-run from the cached query embeddings).
- `Artículo 109 (part 1/4)`, with the correct 7,501 to 38,000 euro range, **was retrieved** (rank 3 in the second search, rank 2 in the third), but nothing retrieved said the infringement was serious.
- The passage that was retrieved first for the Spanish query matches the question's words more closely than the right one: it says "informe anual" and "fuera de los plazos" (late), while point 1.15 speaks of not submitting the report and has no separate rule for lateness.
- The cited chunk does not show its group heading. "3. Infracciones en materia de transporte de mercancías peligrosas" is in `Artículo 108 (part 2/3)`; part 3/3 keeps only the article title "Infracciones leves", so the dangerous-goods context is visible there only through the safety-adviser sentence.

**Classification:** retrieval miss, leading to a confident wrong answer that passes the citation guardrail. The guardrail checks that the cited passages were retrieved, not that they are about the right thing, so it cannot catch this.

Compared with "Before": the agent went from a correct refusal to a wrong, cited answer.
