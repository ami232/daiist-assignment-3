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
