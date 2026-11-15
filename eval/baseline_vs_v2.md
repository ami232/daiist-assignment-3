# Línea base frente a v2 (30 preguntas de desarrollo)

Veredicto del juez (`correct / supported`, juez gemini-3.1-flash-lite en las dos).

- **Línea base** (`answers.json`, `judge.json`, tag `baseline-v1`): texto original del BOE, sin verificador de cobertura, agente con fallback (q01–q10 gemini-3.5-flash, q11 gemini-3.7-flash, q12–q30 gemini-3.5-flash-lite), juzgada contra las referencias de entonces.
- **v2** (`answers_v2.json`, `judge_v2.json`): texto consolidado, verificador de cobertura v4, agente y verificador gemini-3.5-flash-lite sin fallback, referencias actuales (q05 cambiada, ver `reference_changes.md`).

Rechazo = la respuesta contiene «No consta en los documentos del corpus».

| id | tipo | modelo base | base | v2 | rechazo base → v2 | cambio |
|---|---|---|---|---|---|---|
| q01 | single | gemini-3.5-flash | 1 / 1 | 1 / 1 | no → no |  |
| q02 | unanswerable | gemini-3.5-flash | 1 / 1 | 1 / 1 | sí → sí |  |
| q03 | single | gemini-3.5-flash | 1 / 1 | 1 / 1 | no → no |  |
| q04 | single | gemini-3.5-flash | 1 / 1 | 1 / 1 | no → no |  |
| q05 | single | gemini-3.5-flash | 1 / 1 | 0 / 1 | no → sí | referencia cambiada |
| q06 | single | gemini-3.5-flash | 1 / 1 | 1 / 1 | no → no |  |
| q07 | single | gemini-3.5-flash | 1 / 1 | 1 / 1 | no → no |  |
| q08 | single | gemini-3.5-flash | 1 / 1 | 1 / 1 | no → no |  |
| q09 | single | gemini-3.5-flash | 1 / 1 | 1 / 1 | no → no |  |
| q10 | single | gemini-3.5-flash | 1 / 1 | 1 / 1 | no → no |  |
| q11 | multi | gemini-3.7-flash | 1 / 1 | 1 / 1 | no → no |  |
| q12 | multi | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | no → no |  |
| q13 | unanswerable | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | sí → sí |  |
| q14 | unanswerable | gemini-3.5-flash-lite | 0 / 1 | 0 / 1 | no → no |  |
| q15 | single | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | no → no |  |
| q16 | single | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | no → no |  |
| q17 | single | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | no → no |  |
| q18 | single | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | no → no |  |
| q19 | single | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | no → no |  |
| q20 | single | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | no → no |  |
| q21 | single | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | no → no |  |
| q22 | single | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | no → no |  |
| q23 | single | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | no → no |  |
| q24 | single | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | no → no |  |
| q25 | multi | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | no → no |  |
| q26 | multi | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | no → no |  |
| q27 | multi | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | no → no |  |
| q28 | unanswerable | gemini-3.5-flash-lite | 1 / 0 | 1 / 1 | sí → sí | **sí** |
| q29 | unanswerable | gemini-3.5-flash-lite | 1 / 1 | 1 / 1 | sí → sí |  |
| q30 | unanswerable | gemini-3.5-flash-lite | 0 / 1 | 1 / 1 | no → sí | **sí** |
| **total** | | | 28 / 29 | 28 / 30 | | |

Cambian de veredicto: q05, q28, q30. El resto (27) tiene el mismo veredicto.

## Causa de cada cambio

- **q05**: **Referencia cambiada.** Línea base: con el texto original responde «aviso previo» (art. 18), correcto frente a la referencia antigua (art. 18). v2: el art. 18 está derogado y la referencia nueva es el art. 19; la búsqueda trae el art. 19 en la posición [1], pero el verificador de cobertura v4 dice NO (la pregunta habla del promotor y el art. 19 asigna la comunicación a los contratistas) y el código fuerza el rechazo. Los dos veredictos no son comparables.
- **q28**: supported 0→1. Línea base: rechazo correcto, pero añade que buscó en las cinco normas y que ninguna regula el seguro, afirmación que no está en la evidencia. v2: el verificador dice NO y el código pone el rechazo fijo, que solo enumera la consulta hecha; ya no hay afirmaciones sin apoyo. Causa: verificador de cobertura (no existía en la línea base).
- **q30**: correct 0→1. Línea base: responde con reglas generales del Anexo IV (temperatura, inclemencias, agua) como si fueran medidas contra la ola de calor. v2: el verificador dice NO y el código fuerza el rechazo. Causa: verificador de cobertura.

## Sin cambio de veredicto, pero a tener en cuenta

- **q14**: Sin cambio (0/1 en las dos). Responde con la vigilancia de la salud (Ley 31/1995, art. 22) en lugar de rechazar. En v2 el verificador dice SÍ citando la frase de excepciones del art. 22, así que no fuerza el rechazo: el verificador toma un artículo cercano por respuesta.
- q01–q11: cambia el modelo del agente (de gemini-3.5-flash / 3.7-flash a gemini-3.5-flash-lite) sin que cambie el veredicto.
