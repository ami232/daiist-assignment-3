# Cambios en las referencias por el texto consolidado

El índice pasó del texto original de las normas (`diario_boe/xml.php`) al texto
consolidado del BOE (API de legislación consolidada, ver `index/corpus_manifest.json`).
Estas referencias cambian porque **la norma cambió**, no porque el modelo respondiera
distinto. Cambios aprobados por la usuaria el 2026-11-15.

Las columnas `correct` y `supported` de q05, h05 y h08 se han vaciado: los valores
antiguos juzgaban respuestas dadas sobre el texto original y se rehacen tras la nueva
evaluación. Las notas (`notes`) se conservan en los archivos y se copian aquí.
Los resultados de la línea base (`answers.json`, `judge.json`, `results.csv`,
`summary.json`) no se han tocado.

## Cambios

| id | Archivo | Valor antiguo | Valor nuevo | Motivo |
|---|---|---|---|---|
| q05 | `questions.csv` | expected_source: RD 1627/1997 · expected_location: Artículo 18 · reference_answer: «Efectuar un aviso previo a la autoridad laboral competente, que además debe exponerse de forma visible en la obra.» | expected_source: RD 1627/1997 · expected_location: Artículo 19 · reference_answer: «El aviso previo del promotor (art. 18) fue derogado por el RD 337/2010. Ahora la comunicación de apertura del centro de trabajo debe ser previa al comienzo de los trabajos y la presentan solo los contratistas (art. 19).» | La norma cambió en el texto consolidado: el art. 18 del RD 1627/1997 figura como «(Derogado)» por la disposición derogatoria única.2 del RD 337/2010, y el art. 19.1 dice ahora que la comunicación de apertura «deberá ser previa al comienzo de los trabajos y se presentará únicamente por los empresarios que tengan la consideración de contratistas». |
| q05 | `human_labels.csv` | correct: 1 · supported: 1 · notes: «Prior notice, Annex III and display on site (Art. 18)» | correct: (vacío) · supported: (vacío) · notes: sin cambios | La nota juzgaba una respuesta basada en el art. 18 original, hoy derogado. |
| h08 | `heldout_labels.csv` | expected: «The corpus only holds the original 1995 table in pesetas (Art. 49, very serious up to 100 million pesetas). Current amounts are not in the corpus, so the answer should say it cannot give today's figure.» · correct: 0 · supported: 1 · notes: «Gives the 1995 pesetas amounts as 'the maximum' although the question asks for today; the note about original pesetas hedges but does not refuse. Amounts match Art. 49 (supported) but are outdated. Also cites Art. 50 for the cap, which only refers back to Art. 49.» | expected: «Correcto = decir que el art. 49 de la Ley 31/1995 está derogado por el Real Decreto Legislativo 5/2000 y que el corpus no contiene las cuantías actuales. Dar la cifra en pesetas como si fuera la actual es incorrecto.» · correct: (vacío) · supported: (vacío) · notes: sin cambios | La norma cambió en el texto consolidado: el art. 49 (y los arts. 46 a 52) de la Ley 31/1995 figura como «(Derogado)» por la disposición derogatoria única.2.c) del Real Decreto Legislativo 5/2000; la tabla en pesetas ya no está en el índice. |
| h05 | `heldout_labels.csv` | expected: «Not in the corpus: Art. 32 bis of Ley 31/1995 (preventive resource) is not in the indexed original text. Expected refusal.» · correct: 1 · supported: 1 · notes: «Correct refusal and explains that the corpus lacks the later provisions. Real gap in the corpus, not in the model.» | expected: «Debe responder, no rechazar. Los recursos preventivos son necesarios en tres casos: cuando los riesgos se agravan por la concurrencia de operaciones, en actividades o procesos peligrosos o con riesgos especiales, y cuando lo requiera la Inspección de Trabajo; en obra se aplican a cada contratista y deben ser suficientes en número y permanecer mientras dure la situación (Ley 31/1995, art. 32 bis y DA 14; RD 39/1997, art. 22 bis). Citar la DA única del RD 1627/1997 es opcional.» · correct: (vacío) · supported: (vacío) · notes: sin cambios | La norma cambió en el texto consolidado: el art. 32 bis y la disposición adicional decimocuarta de la Ley 31/1995 (añadidos por la Ley 54/2003) no estaban en el texto original indexado y sí están en el consolidado, igual que el art. 22 bis del RD 39/1997; la pregunta deja de ser un rechazo. `coverage_eval.py` la trata ya como pregunta con respuesta (solo marca «debe rechazar» si `expected` contiene «Expected refusal»), sin cambiar código. |

## Revisadas sin cambio

| id | Nota |
|---|---|
| q04 | El art. 13.4 del RD 1627/1997 consolidado ya no trae el plazo de veinticuatro horas para remitir copia de la anotación a la Inspección de Trabajo; ahora la anotación se notifica al contratista afectado y a los representantes de los trabajadores. La pregunta (quién facilita el libro de incidencias, art. 13) no depende de ese plazo: la referencia no cambia. |
| q06 | El art. 4.1.a) del RD 1627/1997 consolidado sigue diciendo «igual o superior a 75 millones de pesetas»: el BOE no lo ha pasado a euros. La referencia no cambia. |
