# Test-set worksheet

Working aid, not a submission artefact — delete it and `eval/sections.csv` before the PR if
you'd rather they weren't graded.

**It inventories the corpus. It does not contain questions.** The 30+ questions, their
`kind`, and the `reference_answer` for each are yours to write: the brief requires it, and
they are what the comprehension check will probe.

## How to use it

`expected_source` is the **doc_id** column. `expected_location` is the **seccion** column,
copied exactly — `evaluate.py` scores a hit when the doc_id matches and `seccion` appears in
the chunk's `location_label`. Separate several with `;`, in the same order in both columns.

Hard rules `check.py` enforces: 30+ questions; 5+ `unanswerable`; 5+ `multi`; unique `id`;
`unanswerable` rows must leave `expected_source` **empty**; every other row must have one.
The first non-unanswerable row is the question `check.py` puts through the server and the
agent, so make `q01` something clean and clearly answerable.

> **Note on the counts below.** The per-document word counts in this worksheet come from an
> earlier extraction pass and total 70,574. The authoritative figures are in
> `index/manifest.json` and REPORT.md: **63,434 words across four documents**. The difference is
> front matter that the final page filter excludes. The section names and `doc_id` values below
> are still correct and are what `expected_location` was copied from.

## The corpus

| doc_id | trámite | date | sections | words |
|---|---|---|---|---|
| `BOCG-15-A-1-1` | `proyecto` | 2023-12-15 | 22 | 14,024 |
| `BOCG-15-A-1-4` | `informe_ponencia` | 2024-06-25 | 25 | 16,641 |
| `BOCG-15-A-1-8` | `aprobacion_definitiva` | 2024-07-31 | 45 | 21,314 |
| `DSCD-15-PL-54` | `debate_pleno` | 2024-06-27 | 15 | 18,595 |

## Where the version drift is

The same article exists in up to three stages and the text differs. These are the questions
a retriever without a `tramite` filter gets wrong, so they are worth over-sampling.

| section | proyecto | ponencia | definitiva |
|---|:--:|:--:|:--:|
| `Artículo cuarto` | x | x | x |
| `Artículo decimoctavo` | · | · | x |
| `Artículo decimocuarto` | · | · | x |
| `Artículo decimoquinto` | · | · | x |
| `Artículo decimosexto` | · | · | x |
| `Artículo decimoséptimo` | · | · | x |
| `Artículo decimotercero` | · | · | x |
| `Artículo duodécimo` | · | x | x |
| `Artículo décimo` | x | x | x |
| `Artículo noveno` | x | x | x |
| `Artículo octavo` | x | x | x |
| `Artículo primero` | x | x | x |
| `Artículo quinto` | x | x | x |
| `Artículo segundo` | x | x | x |
| `Artículo sexto` | x | x | x |
| `Artículo séptimo` | x | x | x |
| `Artículo tercero` | x | x | x |
| `Artículo undécimo` | x | x | x |
| `Disposición adicional (nueva)` | · | x | · |
| `Disposición adicional cuarta` | · | · | x |
| `Disposición adicional primera` | x | x | x |
| `Disposición adicional quinta` | · | · | x |
| `Disposición adicional segunda` | x | x | x |
| `Disposición adicional sexta` | · | · | x |
| `Disposición adicional tercera` | x | x | x |
| `Disposición final (cuarta)` | · | x | · |
| `Disposición final (nueva)` | · | x | · |
| `Disposición final (primera)` | · | x | · |
| `Disposición final (segunda)` | · | x | · |
| `Disposición final (tercera)` | · | x | · |
| `Disposición final cuarta` | x | · | x |
| `Disposición final decimocuarta` | · | · | x |
| `Disposición final decimoquinta` | · | · | x |
| `Disposición final decimotercera` | · | · | x |
| `Disposición final duodécima` | · | · | x |
| `Disposición final décima` | · | · | x |
| `Disposición final novena` | · | · | x |
| `Disposición final octava` | · | · | x |
| `Disposición final primera` | x | · | x |
| `Disposición final quinta` | · | · | x |
| `Disposición final segunda` | x | · | x |
| `Disposición final sexta` | · | · | x |
| `Disposición final séptima` | · | · | x |
| `Disposición final tercera` | x | · | x |
| `Disposición final undécima` | · | · | x |
| `Disposición transitoria primera` | x | x | x |
| `Disposición transitoria segunda` | x | x | x |
| `Disposición transitoria tercera` | · | · | x |

- **In all three stages (16):** `Artículo cuarto`, `Artículo décimo`, `Artículo noveno`, `Artículo octavo`, `Artículo primero`, `Artículo quinto`, `Artículo segundo`, `Artículo sexto`, `Artículo séptimo`, `Artículo tercero`, `Artículo undécimo`, `Disposición adicional primera`… — the natural home for version-trap and `multi` questions.
- **Only in the final text (21):** `Artículo decimoctavo`, `Artículo decimocuarto`, `Artículo decimoquinto`, `Artículo decimosexto`, `Artículo decimoséptimo`, `Artículo decimotercero`, `Disposición adicional cuarta`, `Disposición adicional quinta`, `Disposición adicional sexta`, `Disposición final decimocuarta`, `Disposición final decimoquinta`, `Disposición final decimotercera`, `Disposición final duodécima`, `Disposición final décima`… — these entered the law after the Government's bill.

**A labelling quirk that matters for `multi` questions.** The Informe de la Ponencia names
provisions it proposes to add as `Disposición adicional (nueva)`, `Disposición final (primera)`
and so on, in parentheses — so its labels do **not** line up with the other two stages. Write
stage-comparison questions across **proyecto ↔ aprobación definitiva**, where the labels match
exactly, and treat the ponencia as a third point whose `expected_location` you copy from the
`seccion` column rather than assuming.

### Which sections changed most, bill -> enacted text

Word counts for the same `seccion` in `BOCG-15-A-1-1` and `BOCG-15-A-1-8`. The biggest movers
are where a retriever with no `tramite` filter will be most confidently wrong, so they make the
sharpest version traps and the most interesting `multi` questions.

| section | proyecto | definitiva | change |
|---|--:|--:|--:|
| `Disposición final primera` | 49 | 601 | +552 |
| `Artículo primero` | 207 | 664 | +457 |
| `Disposición final tercera` | 53 | 508 | +455 |
| `Artículo undécimo` | 723 | 890 | +167 |
| `Artículo sexto` | 172 | 324 | +152 |
| `Disposición final cuarta` | 57 | 185 | +128 |
| `Disposición final segunda` | 159 | 268 | +109 |
| `Artículo noveno` | 1,885 | 1,964 | +79 |
| `Disposición transitoria primera` | 652 | 608 | -44 |
| `Disposición adicional tercera` | 155 | 116 | -39 |
| `Disposición adicional primera` | 128 | 99 | -29 |
| `Artículo cuarto` | 171 | 189 | +18 |

### What each article amends

Useful for writing questions that sound like a journalist's, not like a database query.

| section | in the final text it modifies |
|---|---|
| `Artículo cuarto` | Modificación de la Ley 50/1981, de 30 de diciembre, por la que se regula |
| `Artículo decimoctavo` | Modificación de la Ley 5/2011, de 29 de marzo, de Economía Social |
| `Artículo decimocuarto` | Modificación del Real Decreto Legislativo 2/2015, de 23 de octubre, |
| `Artículo decimoquinto` | Modificación de la Ley Orgánica 2/2023, de 22 de marzo, del Sistema |
| `Artículo decimosexto` | Modificación de la Ley 50/2002, de 26 de diciembre, de Fundaciones |
| `Artículo decimoséptimo` | Modificación de la Ley 43/2015, de 9 de octubre, del Tercer Sector |
| `Artículo decimotercero` | Modificación de la Ley Orgánica 11/1985, de 2 de agosto, de Libert |
| `Artículo duodécimo` | Modificación de la Ley 17/2006, de 5 de junio, de la radio y la televi |
| `Artículo décimo` | Modificación de la Ley 6/2023, de 17 de marzo, de los Mercados de Valores |
| `Artículo noveno` | Modificación del Texto Refundido de la Ley de Sociedades de Capital, apro |
| `Artículo octavo` | Modificación de la Ley 40/2015, de 1 de octubre, de Régimen Jurídico del |
| `Artículo primero` | Modificación de la Ley Orgánica 5/1985, de 19 de junio, del Régimen Elec |
| `Artículo quinto` | Modificación de la Ley Orgánica 2/1982, de 12 de mayo, del Tribunal de Cu |
| `Artículo segundo` | Modificación de la Ley Orgánica 2/1979, de 3 de octubre, del Tribunal Co |
| `Artículo sexto` | Modificación de la Ley Orgánica 6/1985, de 1 de julio, del Poder Judicial |
| `Artículo séptimo` | Modificación de la Ley 50/1997, de 27 de noviembre, del Gobierno |
| `Artículo tercero` | Modificación de la Ley Orgánica 3/1980, de 22 de abril, del Consejo de E |
| `Artículo undécimo` | Modificación de la Ley 2/1974, de 13 de febrero, sobre Colegios Profesi |

## The debate: who spoke, for which group

`grupo` is now a chunk metadata field and a `search` filter, parsed by `index.py` from the
session's own sumario (pp. 2-3), which the index otherwise skips.

| speaker (`seccion`) | group | turns | pages | words |
|---|---|--:|---|--:|
| `La señora PRESIDENTA` | (presidencia) | 78 | 4-39 | 3,313 |
| `La señora CALVO GÓMEZ` | Junts per Catalunya | 7 | 8-10 | 2,483 |
| `La señora VALLUGERA BALAÑÀ` | Republicano | 4 | 10-12 | 1,568 |
| `El señor DE LOS SANTOS GONZÁLEZ` | Popular en el Congreso | 5 | 13-15 | 1,453 |
| `La señora POZUETA FERNÁNDEZ` | Euskal Herria Bildu | 4 | 15-16 | 1,382 |
| `La señora AGUIRRE GIL DE BIEDMA` | VOX | 4 | 17-18 | 1,329 |
| `El señor AGIRRETXEA URRESTI` | Vasco (EAJ-PNV) | 4 | 7-8 | 1,319 |
| `La señora FERNÁNDEZ BENÉITEZ` | Socialista | 4 | 18-19 | 1,195 |
| `La señora GIL DE REBOLEÑO LASTORTRES` | Plurinacional SUMAR | 3 | 12-13 | 1,177 |
| `La señora VALIDO GARCÍA` | Mixto | 3 | 5-32 | 929 |
| `El señor REGO CANDAMIL` | Mixto | 2 | 5-6 | 737 |
| `La señora MINISTRA DE IGUALDAD (Redondo García)` | (Gobierno, sin grupo) | 2 | 19-20 | 671 |
| `La señora BELARRA URTEAGA` | Mixto | 2 | 6 | 620 |
| `El señor CATALÁN HIGUERAS` | Mixto | 1 | 4 | 297 |

## A shape for 36 questions

Counts, not questions. Adjust freely — but keep `multi` and `unanswerable` above the floor.

| n | kind | what it tests | where to look |
|--:|---|---|---|
| 6 | `single` | what the enacted text says | `BOCG-15-A-1-8`, any article |
| 5 | `single` | **version trap** — what the *Government's* text said | `BOCG-15-A-1-1` only |
| 4 | `single` | what a deputy argued | `DSCD-15-PL-54`, one speaker |
| 3 | `single` | the vote and its result | `DSCD-15-PL-54`, pp. 32-39 |
| 2 | `single` | a disposición (transitoria/final) | any stage |
| 6 | `multi` | did this article change between two stages? | two BOCG docs |
| 4 | `multi` | a provision **and** what was said about it | one BOCG + the DS |
| 6 | `unanswerable` | near-miss, not off-topic | see below |

**The six unanswerable ones carry the most weight in the report.** Keep them *adjacent* to
the corpus, never obviously off-topic. Four natural sources: the **enmiendas**
(`BOCG-15-A-1-2`, deliberately held back — reserve at least one for the add-document demo,
and set `DEMO_QUESTION_ID` in `evaluate.py` to its id); the **Senado**, which amended this
bill but is not indexed; **another bill** of the same legislature; and anything **after July
2024**. Two more should target the scope guard rather than retrieval — a prediction and a
value judgement — since they are unanswerable because no passage *could* answer them.

## Before you tune anything

Write all 36 now, from the documents, before the index is embedded and before you see a
single hit rate. It is the only way the retrieval numbers mean anything, and you will be
asked to defend them without your code.
