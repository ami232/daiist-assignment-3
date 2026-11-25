# Traza del subagente `corpus-researcher`

Ejecutado el 24/11/2026 desde una sesión de Claude Code, contra el índice posterior a la
demostración de `add_document` (5 documentos, 121.580 palabras). El subagente sólo dispone de
la herramienta `mcp__corpus__search`; no puede leer el sistema de ficheros ni llamar a
`add_document`. Sus instrucciones son las reglas de `AGENTS.md`.

## Pregunta

> ¿Qué cambió en el artículo cuarenta y cuatro bis de la LOREG entre el Informe de la Ponencia
> y el texto aprobado definitivamente?

## Llamadas a la herramienta (2)

| # | `query` | `tramite` | `k` | resultados |
|---|---|---|---|---|
| 1 | `artículo 44 bis LOREG candidaturas composición equilibrada proporción mujeres hombres` | `informe_ponencia` | 6 | 6 |
| 2 | `artículo 44 bis LOREG candidaturas composición equilibrada proporción mujeres hombres` | `aprobacion_definitiva` | 6 | 6 |

Sin filtros `genero` ni `grupo`. El subagente usó el filtro `tramite` por su cuenta, una vez por
cada versión del texto: es el patrón que el diseño C (`structured+filtro`) pretendía favorecer.

## Respuesta del subagente

> Entre el Informe de la Ponencia y el texto aprobado definitivamente, el artículo cuarenta y
> cuatro bis pasó de cuatro a cinco apartados: se añadieron las Juntas Generales de los
> Territorios Históricos vascos al ámbito del apartado 1, se reformuló la regla sobre suplentes,
> se incorporó un nuevo apartado 3 que permite a las comunidades autónomas y Juntas Generales
> establecer otros sistemas de elaboración de listas, y se renumeraron los apartados sobre el
> Senado y la Junta Electoral.
>
> En el **informe de ponencia** (25/06/2024) el precepto decía: «Artículo cuarenta y cuatro bis.
> 1. Las candidaturas que se presenten para las elecciones de diputados y diputadas al Congreso,
> municipales, de miembros de los consejos insulares y de los cabildos insulares, diputados y
> diputadas al Parlamento Europeo y miembros de las Asambleas Legislativas de las Comunidades
> Autónomas deberán tener una composición paritaria de mujeres y hombres, integrándose las listas
> por personas de uno y otro sexo ordenados de forma alternativa. 2. A las listas de suplentes se
> aplicarán las reglas contenidas en el anterior apartado. 3. Cuando las candidaturas para el
> Senado se agrupen en listas, de acuerdo con lo dispuesto en el artículo 171, tales listas
> deberán tener igualmente una composición paritaria de mujeres y hombres, tal y como se establece
> en el apartado 1. 4. La Junta Electoral solo aceptará aquellas candidaturas que cumplan este
> precepto tanto para los candidatos como para los suplentes.»
> [BOCG-15-A-1-4 · Artículo primero · p. 13 · CVE:BOCG-15-A-1-4]
>
> En el texto de **aprobación definitiva** (31/07/2024) la redacción es: «Artículo cuarenta y
> cuatro bis. 1. Las candidaturas que se presenten para las elecciones de diputados y diputadas al
> Congreso, municipales, de miembros de los consejos insulares y de los cabildos insulares,
> diputados y diputadas al Parlamento Europeo y miembros de las Asambleas Legislativas de las
> comunidades autónomas y Juntas Generales de los Territorios Históricos vascos deberán tener una
> composición paritaria de mujeres y hombres, integrándose las listas por personas de uno y otro
> sexo ordenados de forma alternativa. 2. La regla anterior se aplicará en el conjunto de las
> listas, sin separar titulares y suplentes. 3. En las elecciones de miembros de las Asambleas
> Legislativas de las comunidades autónomas y Juntas Generales de los Territorios Históricos
> vascos, las leyes reguladoras de sus respectivos regímenes electorales podrán establecer otros
> sistemas de elaboración de listas siempre que su objetivo sea favorecer la representación
> paritaria y la presencia equilibrada de mujeres y hombres en dichas candidaturas. 4. Cuando las
> candidaturas para el Senado se agrupen en listas, de acuerdo con lo dispuesto en el artículo
> 171, tales listas deberán tener igualmente una composición paritaria de mujeres y hombres, tal y
> como se establece en el apartado 1. 5. La Junta Electoral solo aceptará aquellas candidaturas
> que cumplan este precepto tanto para las personas candidatas como para las suplentes.»
> [BOCG-15-A-1-8 · Artículo primero (1/2) · p. 12 · CVE:BOCG-15-A-1-8]
>
> Nota adicional de encuadre: en la aprobación definitiva el Artículo primero aparece además
> dividido en apartados «Uno», «Dos» y «Tres», incluyendo modificaciones del artículo 187.2 y del
> artículo doscientos seis de la LOREG. No he verificado en esta consulta si esas dos
> modificaciones adicionales ya figuraban en el informe de ponencia; haría falta una búsqueda
> específica sobre los artículos 187 y 206 en el trámite `informe_ponencia`.

## Verificación manual de la traza

Comprobado fragmento a fragmento contra `index/chunks.jsonl`:

- Las dos citas textuales son **literales**: cada fragmento entrecomillado aparece palabra por
  palabra en el documento que se cita.
- Las dos etiquetas de localización **resuelven** a `location_label` reales del índice
  (`BOCG-15-A-1-4 · Artículo primero · p. 13` y `BOCG-15-A-1-8 · Artículo primero (1/2) · p. 12`).
- Los cuatro cambios que enumera en la primera frase se corresponden con diferencias reales entre
  ambas redacciones.
- No añade ningún nombre propio, ninguna cifra ni ningún juicio que no esté en el texto
  recuperado, y marca explícitamente el límite de lo que no ha comprobado (artículos 187 y 206).

Es decir: en esta consulta el subagente cumple las ocho reglas. El contraste con los fallos
medidos en la evaluación —la fabricación de nombres de pila y la fusión de dos etiquetas de cita
en una inexistente— sugiere que el riesgo no está repartido por igual entre tipos de pregunta,
sino concentrado en las que piden **quién** dijo algo. Véase la sección de fallos.
