# Resumen de la evaluación

Agente: `gemini-3.5-flash-lite` · juez: `gemini-3.1-flash-lite` · diseño: `struct / dense / filtro=True / k=5`

## Resultados (37 de 37 preguntas puntuadas)

- **Correctas:** 34/37 (92 %)  multi: 5/6 (83 %) · single: 23/25 (92 %) · unanswerable: 6/6 (100 %)
- **Respuestas con afirmaciones no respaldadas:** 1/31 (3 %) de las respuestas que no son rechazo
- **Rechazos correctos:** 6/6 (100 %) de las preguntas sin respuesta
- **Rechazos indebidos (wrong refusals):** 0/31 (0 %) de las preguntas con respuesta
- **Rechazos que faltaron** (contestó una pregunta sin respuesta): 0
- **Citas inválidas:** 0 respuestas · guardarraíl de citas: saltó 0 veces, bloqueó 0

## Coste por pregunta

- Tokens del agente: media 7196, mediana 5677
- Segundos: media 7.5, mediana 3.8, máximo 36.45
- Llamadas a herramientas: media 1.32

## Acuerdo con tus notas (human_labels.csv)

- correct: acuerdo 0.973 en 37 respuestas (kappa de Cohen 0.786)
- supported: acuerdo 0.946 en 37 respuestas (kappa de Cohen 0.479)

Desacuerdos (humano vs. sistema, correct/supported):

| id | human | sistema | graded_by | judge_reason |
|---|---|---|---|---|
| q06 | 1/0 | 1/1 | juez | La respuesta es correcta y está totalmente respaldada por la evidencia, identificando correctamente el requisito de solvencia y calculando el importe anual basándose en los datos del presupuesto proporcionados. |
| q09 | 1/0 | 1/1 | juez | La respuesta proporciona la cifra exacta y las condiciones temporales requeridas, respaldándose correctamente en la evidencia citada. |
| q11 | 1/1 | 0/1 | juez | La respuesta es incorrecta porque omite la información sobre el teléfono de guardia 24x7 para incidentes críticos o altos, que es parte esencial de la respuesta de referencia. |


## Fallos por causa sugerida (revísalos en failures.csv)

| causa | n |
|---|---|
| wrong answer from right passage | 2 |
| retrieval miss | 1 |


## Retrieval

| design | method | tender_filter | hit@1 | hit@3 | hit@5 | multi_all@5 | words_in_prompt@5 | chunks |
|---|---|---|---|---|---|---|---|---|
| fixed300 | dense | no | 0.581 | 0.839 | 0.903 | 0.167 | 1413 | 320 |
| fixed300 | dense | sí | 0.581 | 0.839 | 0.903 | 0.167 | 1413 | 320 |
| fixed300 | bm25 | no | 0.484 | 0.71 | 0.839 | 0.5 | 1445 | 320 |
| fixed300 | bm25 | sí | 0.548 | 0.839 | 0.935 | 0.5 | 1467 | 320 |
| fixed300 | hybrid | no | 0.613 | 0.839 | 0.935 | 0.333 | 1455 | 320 |
| fixed300 | hybrid | sí | 0.613 | 0.839 | 0.935 | 0.333 | 1450 | 320 |
| struct | dense | no | 0.71 | 0.935 | 1.0 | 0.5 | 876 | 405 |
| struct | dense | sí | 0.71 | 0.935 | 1.0 | 0.5 | 869 | 405 |
| struct | bm25 | no | 0.419 | 0.774 | 0.806 | 0.5 | 976 | 405 |
| struct | bm25 | sí | 0.581 | 0.806 | 0.871 | 0.5 | 944 | 405 |
| struct | hybrid | no | 0.645 | 0.871 | 0.935 | 0.5 | 911 | 405 |
| struct | hybrid | sí | 0.645 | 0.871 | 0.935 | 0.5 | 907 | 405 |
