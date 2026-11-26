# Rúbrica del juez

Contexto: las respuestas las usa el responsable de licitaciones de una pyme para decidir si se
presenta a un concurso público y para preparar la oferta. Un dato equivocado puede suponer la
exclusión del concurso, así que la rúbrica es estricta con las cifras y con las respuestas
incompletas.

## correct (1/0)

Base: 1 si la respuesta dice lo mismo que la respuesta de referencia (o, si la pregunta no
tiene respuesta en el corpus, si lo reconoce). 0 si no.

Criterios:
- **Respuestas parciales:** si la pregunta tiene varias partes (por ejemplo, compara dos
  licitaciones) y la respuesta acierta una pero falla o se deja otra, correct = 0. Con media
  respuesta, el usuario puede tomar una mala decisión.
- **Cifras exactas:** importes, porcentajes, plazos y fechas tienen que coincidir con la
  referencia en cifra y unidad. Solo se aceptan cambios de formato (585.000 € = 585000 euros;
  36 meses = 3 años). Un redondeo, un importe con IVA cuando se pide sin IVA, o un 5 % en lugar
  de un 10 % dan correct = 0.
- **Información extra:** si la respuesta añade datos que no están en la referencia pero no la
  contradicen, no se penaliza en correct. Si esos datos no están en la evidencia, se penaliza
  en supported.
- **Otra licitación:** una cifra o un requisito tomado de una licitación distinta de la que se
  pregunta es un error: correct = 0.
- **Contradicciones:** si la referencia indica que dos documentos se contradicen, la respuesta
  solo es correcta si menciona ambos valores.

## supported (1/0)

Base: 1 si TODAS las afirmaciones de la respuesta aparecen en la evidencia recuperada; 0 si
alguna no aparece, aunque sea cierta.

Criterios:
- **Paráfrasis:** decir lo mismo con otras palabras cuenta como respaldado, siempre que no
  cambie cifras ni condiciones.
- **Cálculos:** un resultado calculado (por ejemplo, 18 + 12 + 15 + 4 = 49 puntos) cuenta como
  respaldado si cada dato de partida está en la evidencia y la operación es correcta. Si un
  dato de partida no está en la evidencia o la cuenta está mal, supported = 0.
- **Opiniones:** un párrafo marcado como «Opinión (la decisión es tuya):» no cuenta como
  afirmación, pero los datos en que se apoya sí tienen que estar en la evidencia.
- **Frases sin datos:** avisos genéricos sin ningún dato concreto («conviene revisar el pliego
  completo») no cuentan como afirmaciones.
