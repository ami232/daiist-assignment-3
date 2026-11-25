# Grading worksheet

Grade **20+** of these yourself, **before** opening `eval/judge.csv` — the whole point of the
agreement number is that your grades were formed independently of the judge's.

For each one, two binary calls:

- **correct** — does it match the reference answer? For an `unanswerable` question, a proper
  refusal (`NO CONSTA EN EL CORPUS`) *is* correct; inventing an answer is not.
- **supported** — is every claim present in the text the agent actually retrieved? A claim can
  be true in the real world and still score 0 here.

Write a reason for every **0**. Then paste your grades back to me, or fill in
`eval/human_labels.csv` directly (`id,correct,supported,notes`).

---

## q01  ·  `single`

**Question.** ¿Cuándo entra en vigor la ley orgánica de representación paritaria?

**Reference.** A los veinte días de su publicación en el «Boletín Oficial del Estado» (texto aprobado definitivamente por el Congreso).

**Agent answered:**

> En el texto aprobado definitivamente, la ley orgánica entrará en vigor a los veinte días de su publicación en el «Boletín Oficial del Estado»:
>
> > «Disposición final decimoquinta. Entrada en vigor. La presente ley orgánica entrará en vigor a los veinte días de su publicación en el «Boletín Oficial del Estado».»
> > 
> > [BOCG-15-A-1-8 · Disposición final decimoquinta · p. 35 · CVE:BOCG-15-A-1-8]

**Citations (1).** `BOCG-15-A-1-8 · Disposición final decimoquinta · p. 35 · CVE:BOCG-15-A-1-8`

`q01,correct=__,supported=__,notes=`

---

## q02  ·  `single`

**Question.** ¿A qué procesos electorales se aplica la reforma del artículo 44 bis de la LOREG?

**Reference.** A los procesos electorales que se convoquen después de la entrada en vigor de la ley orgánica.

**Agent answered:**

> Según el texto aprobado definitivamente, la reforma del artículo 44 bis de la LOREG se aplica a las candidaturas que se presenten para las elecciones de diputados y diputadas al Congreso, municipales, de miembros de los consejos insulares y de los cabildos insulares, diputados y diputadas al Parlamento Europeo y miembros de las Asambleas Legislativas de las comunidades autónomas y Juntas Generales de los Territorios Históricos vascos, así como a las listas del Senado cuando se agrupen de acuerdo con el artículo 171 [BOCG-15-A-1-8 · Artículo primero (1/2) · p. 12 · CVE:BOCG-15-A-1-8].
>
> En cuanto a su aplicación temporal, la disposición transitoria primera establece que la modificación será «de aplicación a los procesos electorales que se convoquen después de la entrada en vigor de esta ley orgánica» [BOCG-15-A-1-8 · Disposición transitoria primera (1/2) · p. 26 · CVE:BOCG-15-A-1-8].

**Citations (2).** `BOCG-15-A-1-8 · Artículo primero (1/2) · p. 12 · CVE:BOCG-15-A-1-8`; `BOCG-15-A-1-8 · Disposición transitoria primera (1/2) · p. 26 · CVE:BOCG-15-A-1-8`

`q02,correct=__,supported=__,notes=`

---

## q03  ·  `single`

**Question.** ¿Qué municipios quedan exentos de la regla de composición paritaria en las candidaturas?

**Reference.** El artículo 44 bis no es exigible en municipios con 3.000 residentes o menos; tampoco en los de entre 3.000 y 5.000, pero en estos sí se exige que las personas de cada sexo no superen el 60 % ni sean menos del 40 % en cada candidatura (apartado Dos, que modifica el art. 187.2 de la LOREG).

**Agent answered:**

> En el texto aprobado definitivamente, quedan exentos de la regla de composición paritaria (artículo 44 bis) los municipios con un número de residentes igual o inferior a 3.000 habitantes. Asimismo, la regla paritaria tampoco es exigible en los municipios que cuentan con entre 3.000 y 5.000 habitantes, si bien en estos últimos se exige una presencia equilibrada donde ningún sexo supere el 60 % ni baje del 40 %.
>
> «Lo previsto en el artículo 44 bis de esta ley no será exigible en las candidaturas que se presenten en los municipios con un número de residentes igual o inferior a 3.000 habitantes. Tampoco será exigible lo previsto en el artículo 44 bis de esta ley en aquellos municipios que cuenten con un número de residentes entre 3.000 y 5.000 habitantes. En estos casos, sí será exigible que las personas de cada sexo no superen el sesenta por ciento ni sean menos del cuarenta por ciento, en cada candidatura.» [BOCG-15-A-1-8 · Artículo primero (1/2) · p. 12 · CVE:BOCG-15-A-1-8]

**Citations (1).** `BOCG-15-A-1-8 · Artículo primero (1/2) · p. 12 · CVE:BOCG-15-A-1-8`

`q03,correct=__,supported=__,notes=`

---

## q04  ·  `single`

**Question.** ¿Pueden las comunidades autónomas establecer un sistema de elaboración de listas distinto del previsto en la ley?

**Reference.** Sí. En las elecciones a las Asambleas Legislativas de las comunidades autónomas y a las Juntas Generales de los Territorios Históricos vascos, sus leyes electorales pueden establecer otros sistemas siempre que el objetivo sea favorecer la representación paritaria y la presencia equilibrada.

**Agent answered:**

> En el texto aprobado definitivamente, las leyes reguladoras de los regímenes electorales de las comunidades autónomas sí pueden establecer otros sistemas de elaboración de listas para sus asambleas legislativas, siempre que tengan por objeto favorecer la representación paritaria y la presencia equilibrada:
>
> «En las elecciones de miembros de las Asambleas Legislativas de las comunidades autónomas y Juntas Generales de los Territorios Históricos vascos, las leyes reguladoras de sus respectivos regímenes electorales podrán establecer otros sistemas de elaboración de listas siempre que su objetivo sea favorecer la representación paritaria y la presencia equilibrada de mujeres y hombres en dichas candidaturas.» [BOCG-15-A-1-8 · Artículo primero (1/2) · p. 12 · CVE:BOCG-15-A-1-8]
>
> En el proyecto inicial presentado por el Gobierno y en el informe de la ponencia, en cambio, no se contemplaba esta salvedad, exigiéndose de manera general que las candidaturas a las asambleas legislativas se integraran por personas de uno y otro sexo ordenadas de forma alternativa [BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1] [BOCG-15-A-1-4 · Artículo primero · p. 13 · CVE:BOCG-15-A-1-4].

**Citations (3).** `BOCG-15-A-1-8 · Artículo primero (1/2) · p. 12 · CVE:BOCG-15-A-1-8`; `BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1`; `BOCG-15-A-1-4 · Artículo primero · p. 13 · CVE:BOCG-15-A-1-4`

`q04,correct=__,supported=__,notes=`

---

## q05  ·  `single`

**Question.** ¿Qué porcentaje del sexo menos representado deben alcanzar las entidades de interés público y en qué fechas?

**Reference.** El 33 % a 30 de junio de 2026 y el 40 % a 30 de junio de 2029, en los consejos de administración y la alta dirección de las entidades de interés público.

**Agent answered:**

> ERROR: ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)

**Citations (0).** _none_

`q05,correct=__,supported=__,notes=`

---

## q06  ·  `single`

**Question.** ¿Desde cuándo se aplica la reforma al Tribunal Constitucional?

**Reference.** La modificación del artículo dieciséis de la LO 2/1979 no se aplica hasta la próxima renovación o nombramiento de magistrados y magistradas del Tribunal Constitucional tras la entrada en vigor de la ley.

**Agent answered:**

> Según el texto aprobado definitivamente, la modificación relativa al Tribunal Constitucional no se aplica de forma inmediata tras la entrada en vigor de la ley, sino en la siguiente renovación o nombramiento de magistrados:
>
> «La modificación del artículo dieciséis de la Ley Orgánica 2/1979, de 3 de octubre, no será de aplicación hasta que proceda la próxima renovación o nombramiento de magistrados y magistradas del Tribunal Constitucional tras la entrada en vigor de esta ley orgánica» [BOCG-15-A-1-8 · Disposición transitoria segunda · p. 26-27 · CVE:BOCG-15-A-1-8].

**Citations (1).** `BOCG-15-A-1-8 · Disposición transitoria segunda · p. 26-27 · CVE:BOCG-15-A-1-8`

`q06,correct=__,supported=__,notes=`

---

## q07  ·  `single`

**Question.** ¿Qué ocurre si el Senado rechaza los objetivos de estabilidad presupuestaria ya remitidos a las Cortes?

**Reference.** Los objetivos se someten a una nueva votación en el Pleno del Congreso y se aprueban por mayoría simple, sin necesidad de iniciar un nuevo procedimiento; la modificación se aplica de forma inmediata y directa a la tramitación en curso.

**Agent answered:**

> El corpus no contiene información sobre lo que ocurre si el Senado rechaza los objetivos de estabilidad presupuestaria, ya que el expediente se limita exclusivamente al Proyecto de Ley Orgánica de representación paritaria y presencia equilibrada de mujeres y hombres de la XV Legislatura del Congreso de los Diputados, y no cubre procedimientos presupuestarios ni la tramitación en el Senado.
>
> NO CONSTA EN EL CORPUS. Se ha buscado en todo el expediente del Proyecto de Ley Orgánica 121/000001 sobre estabilidad presupuestaria y actuaciones del Senado; el corpus necesitaría incluir el trámite del Senado o expedientes relativos a la Ley Orgánica de Estabilidad Presupuestaria y Sostenibilidad Financiera para responder a esta cuestión.

**Citations (0).** _none_

`q07,correct=__,supported=__,notes=`

---

## q08  ·  `single`

**Question.** ¿Cómo deben elaborarse las listas para la elección de diputados provinciales tras la reforma?

**Reference.** Conforme al nuevo artículo doscientos seis de la LOREG: listas avaladas al menos por un tercio de los concejales, ajustadas al principio de representación equilibrada, de modo que cada sexo no supere el 60 % ni baje del 40 %, con personas de uno y otro sexo ordenadas de forma alternativa.

**Agent answered:**

> En la redacción aprobada definitivamente, el artículo doscientos seis de la Ley Orgánica del Régimen Electoral General dispone que las listas de candidatos para la elección de diputados provinciales deben elaborarse de manera que se respete el principio de representación equilibrada, exigiéndose que las personas de cada sexo no superen el sesenta por ciento ni sean menos del cuarenta por ciento, y ordenándose de forma alternativa [BOCG-15-A-1-8 · Artículo primero (2/2) · p. 12-13 · CVE:BOCG-15-A-1-8].
>
> El texto definitivo establece lo siguiente:
> «La elaboración de las mencionadas listas se ajustará al principio de representación equilibrada entre mujeres y hombres, de tal manera que las personas de cada sexo no superen el sesenta por ciento ni sean menos del cuarenta por ciento, integrándose en las listas por personas de uno y otro sexo ordenados de forma alternativa» [BOCG-15-A-1-8 · Artículo primero (2/2) · p. 12-13 · CVE:BOCG-15-A-1-8].

**Citations (2).** `BOCG-15-A-1-8 · Artículo primero (2/2) · p. 12-13 · CVE:BOCG-15-A-1-8`; `BOCG-15-A-1-8 · Artículo primero (2/2) · p. 12-13 · CVE:BOCG-15-A-1-8`

`q08,correct=__,supported=__,notes=`

---

## q09  ·  `single`

**Question.** ¿A qué elecciones se aplicaba la composición paritaria en el proyecto de ley presentado por el Gobierno?

**Reference.** A las elecciones al Congreso, municipales, de miembros de los consejos insulares y cabildos insulares, al Parlamento Europeo y a las Asambleas Legislativas de las Comunidades Autónomas (redacción del proyecto, 15/12/2023).

**Agent answered:**

> En el proyecto de ley presentado por el Gobierno, la composición paritaria se aplicaba a las elecciones de diputados al Congreso, municipales, de miembros de los consejos insulares y de los cabildos insulares, de diputados al Parlamento Europeo, de miembros de las Asambleas Legislativas de las Comunidades Autónomas y a las candidaturas para el Senado cuando se agruparan en listas.
>
> En el texto del proyecto se especificaba:
>
> «Las candidaturas que se presenten para las elecciones de diputados y diputadas al Congreso, municipales, de miembros de los consejos insulares y de los cabildos insulares, diputados y diputadas al Parlamento Europeo y miembros de las Asambleas Legislativas de las Comunidades Autónomas deberán tener una composición paritaria de mujeres y hombres, integrándose las listas por personas de uno y otro sexo ordenados de forma alternativa» [BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1].

**Citations (1).** `BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1`

`q09,correct=__,supported=__,notes=`

---

## q10  ·  `single`

**Question.** ¿Qué preveía el proyecto de ley para las listas de suplentes?

**Reference.** Que «A las listas de suplentes se aplicarán las reglas contenidas en el anterior apartado», es decir, una regla propia para las listas de suplentes (redacción del proyecto).

**Agent answered:**

> El proyecto de ley presentado por el Gobierno establecía que las reglas de composición paritaria y alternancia de mujeres y hombres se aplicarían también a las listas de suplentes, exigiendo además que las juntas electorales solo aceptasen aquellas candidaturas que cumplieran este requisito tanto para los candidatos titulares como para los suplentes [BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1].
>
> El texto original disponía lo siguiente:
>
> > «2. A las listas de suplentes se aplicarán las reglas contenidas en el anterior apartado. [...] 4. La Junta Electoral solo aceptará aquellas candidaturas que cumplan este precepto tanto para los candidatos como para los suplentes» [BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1].

**Citations (2).** `BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1`; `BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1`

`q10,correct=__,supported=__,notes=`

---

## q11  ·  `single`

**Question.** ¿Qué decía el proyecto sobre las candidaturas al Senado agrupadas en listas?

**Reference.** Que cuando las candidaturas al Senado se agrupen en listas conforme al artículo 171, esas listas deberán tener igualmente composición paritaria de mujeres y hombres (redacción del proyecto).

**Agent answered:**

> El proyecto de ley disponía que las candidaturas al Senado agrupadas en listas debían tener una composición paritaria de mujeres y hombres, ordenadas de forma alternativa, y que la Junta Electoral solo aceptaría aquellas que cumplieran este precepto tanto para los candidatos como para los suplentes.
>
> Así lo establecía el texto en su fase de `proyecto`:
>
> > «3. Cuando las candidaturas para el Senado se agrupen en listas, de acuerdo con lo dispuesto en el artículo 171, tales listas deberán tener igualmente una composición paritaria de mujeres y hombres, tal y como se establece en el apartado 1. 4. La Junta Electoral solo aceptará aquellas candidaturas que cumplan este precepto tanto para los candidatos como para los suplentes.»
> > [BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1]

**Citations (1).** `BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1`

`q11,correct=__,supported=__,notes=`

---

## q12  ·  `single`

**Question.** ¿Qué papel atribuía el proyecto a la Junta Electoral en el control de las candidaturas?

**Reference.** La Junta Electoral solo aceptará las candidaturas que cumplan el precepto, tanto para los candidatos como para los suplentes (redacción del proyecto).

**Agent answered:**

> En el trámite de proyecto, el texto presentado por el Gobierno establecía que la Junta Electoral únicamente aceptaría aquellas candidaturas que cumplieran el requisito de composición paritaria y ordenación alternativa entre mujeres y hombres, tanto para los candidatos titulares como para los suplentes.
>
> «La Junta Electoral solo aceptará aquellas candidaturas que cumplan este precepto tanto para los candidatos como para los suplentes.» [BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1]

**Citations (1).** `BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1`

`q12,correct=__,supported=__,notes=`

---

## q13  ·  `single`

**Question.** ¿Con qué resultado aprobó el Pleno la votación de conjunto del proyecto de ley orgánica?

**Reference.** 348 votos emitidos, 177 a favor y 171 en contra, en la votación de conjunto por tener carácter de ley orgánica (sesión de 27 de junio de 2024).

**Agent answered:**

> El Pleno aprobó la votación de conjunto del proyecto de ley orgánica con 348 votos emitidos, 177 votos a favor y 171 en contra, en el trámite de debate en pleno [DSCD-15-PL-54 · La señora PRESIDENTA · p. 38 · CVE:DSCD-15-PL-54].
>
> «La señora PRESIDENTA: Pasamos ahora a la votación de conjunto del Proyecto de ley orgánica de representación paritaria y presencia equilibrada de mujeres y hombres, por tener el mismo carácter de ley orgánica. Comienza la votación. (Pausa). Efectuada la votación, dio el siguiente resultado: votos emitidos, 348; a favor, 177; en contra, 171.» [DSCD-15-PL-54 · La señora PRESIDENTA · p. 38 · CVE:DSCD-15-PL-54]

**Citations (2).** `DSCD-15-PL-54 · La señora PRESIDENTA · p. 38 · CVE:DSCD-15-PL-54`; `DSCD-15-PL-54 · La señora PRESIDENTA · p. 38 · CVE:DSCD-15-PL-54`

`q13,correct=__,supported=__,notes=`

---

## q14  ·  `single`

**Question.** ¿Qué se entiende por representación paritaria y presencia equilibrada a efectos de esta ley?

**Reference.** Aquella situación en la que las personas de cada sexo no superen el sesenta por ciento ni sean menos del cuarenta por ciento en un ámbito determinado. El criterio puede no aplicarse, en consonancia con el principio de acción positiva, cuando exista una representación de mujeres superior al sesenta por ciento, lo que deberá justificarse.

**Agent answered:**

> A efectos de esta ley, en el texto aprobado definitivamente se entiende por representación paritaria y presencia equilibrada entre mujeres y hombres:
>
> «aquella situación en la que las personas de cada sexo no superen el sesenta por ciento ni sean menos del cuarenta por ciento en un ámbito determinado» [BOCG-15-A-1-8 · Disposición adicional primera · p. 24 · CVE:BOCG-15-A-1-8].
>
> Asimismo, la norma añade que podrá no aplicarse este criterio, en consonancia con el principio de acción positiva, «cuando exista una representación de mujeres superior al sesenta por ciento que, en todo caso, deberá justificarse» [BOCG-15-A-1-8 · Disposición adicional primera · p. 24 · CVE:BOCG-15-A-1-8].

**Citations (2).** `BOCG-15-A-1-8 · Disposición adicional primera · p. 24 · CVE:BOCG-15-A-1-8`; `BOCG-15-A-1-8 · Disposición adicional primera · p. 24 · CVE:BOCG-15-A-1-8`

`q14,correct=__,supported=__,notes=`

---

## q15  ·  `single`

**Question.** ¿Cómo calificó el Grupo Popular el texto del dictamen en el debate del Pleno?

**Reference.** El señor De los Santos González dijo que el proyecto había quedado «desvirtuado por sus señorías de la izquierda».

**Agent answered:**

> En el debate del Pleno, el Grupo Popular —interviniendo a través del diputado Arsenio de los Santos González— calificó el texto del dictamen como un proyecto «desvirtuado por sus señorías de la izquierda», «destrozado» y «impúdico», señalando además que el texto incluye enmiendas que «contravienen la Constitución» y «asestan un golpe al Estado de derecho».
>
> [DSCD-15-PL-54 · El señor DE LOS SANTOS GONZÁLEZ (1/4 y 2/4) · pp. 13-14 · CVE:DSCD-15-PL-54]

**Citations (1).** `DSCD-15-PL-54 · El señor DE LOS SANTOS GONZÁLEZ (1/4 y 2/4) · pp. 13-14 · CVE:DSCD-15-PL-54`

`q15,correct=__,supported=__,notes=`

---

## q16  ·  `single`

**Question.** ¿Quién intervino en nombre del Gobierno en el debate del Pleno?

**Reference.** La Ministra de Igualdad, señora Redondo García.

**Agent answered:**

> En nombre del Gobierno intervino la ministra de Igualdad, Ana Redondo García [DSCD-15-PL-54 · La señora MINISTRA DE IGUALDAD (Redondo García) (1/2) · p. 19-20 · CVE:DSCD-15-PL-54].
>
> «La señora MINISTRA DE IGUALDAD (Redondo García): Gracias, presidenta. Intervengo muy brevemente. Simplemente, quiero agradecer el trabajo. Sé que ha sido duro, sé que han sido momentos difíciles y complicados para, finalmente, llegar a un consenso que nos permite avanzar» [DSCD-15-PL-54 · La señora MINISTRA DE IGUALDAD (Redondo García) (1/2) · p. 19-20 · CVE:DSCD-15-PL-54].

**Citations (2).** `DSCD-15-PL-54 · La señora MINISTRA DE IGUALDAD (Redondo García) (1/2) · p. 19-20 · CVE:DSCD-15-PL-54`; `DSCD-15-PL-54 · La señora MINISTRA DE IGUALDAD (Redondo García) (1/2) · p. 19-20 · CVE:DSCD-15-PL-54`

`q16,correct=__,supported=__,notes=`

---

## q17  ·  `single`

**Question.** ¿Qué norma de la Unión Europea incorpora esta ley al derecho español?

**Reference.** La Directiva (UE) 2022/2381 del Parlamento Europeo y del Consejo, de 23 de noviembre de 2022, relativa a un mejor equilibrio de género entre los administradores de las sociedades cotizadas y a medidas conexas.

**Agent answered:**

> La ley incorpora al derecho español la Directiva (UE) 2022/2381, del Parlamento Europeo y del Consejo, de 23 de noviembre de 2022, relativa a un mejor equilibrio de género entre los administradores de las sociedades cotizadas y a medidas conexas.
>
> Así figura en el texto presentado por el Gobierno y en el informe de la ponencia:
>
> > «Disposición final tercera. Incorporación de derecho de la Unión Europea. Mediante esta ley orgánica se incorpora al derecho español la Directiva (UE) 2022/2381, del Parlamento Europeo y del Consejo, de 23 de noviembre de 2022, relativa a un mejor equilibrio de género entre los administradores de las sociedades cotizadas y a medidas conexas.» [BOCG-15-A-1-1 · Disposición final tercera · p. 22 · CVE:BOCG-15-A-1-1]  
> > [BOCG-15-A-1-4 · Disposición final (tercera) · p. 27 · CVE:BOCG-15-A-1-4]
>
> Y en el texto aprobado definitivamente, tras la reordenación del articulado, se recoge en la disposición final decimocuarta:
>
> > «Disposición final decimocuarta. Incorporación de derecho de la Unión Europea. Mediante esta ley orgánica se incorpora al derecho español la Directiva (UE) 2022/2381, del Parlamento Europeo y del Consejo, de 23 de noviembre de 2022, relativa a un mejor equilibrio de género entre los administradores de las sociedades cotizadas y a medidas conexas.» [BOCG-15-A-1-8 · Disposición final decimocuarta · p. 35 · CVE:BOCG-15-A-1-8]

**Citations (3).** `BOCG-15-A-1-1 · Disposición final tercera · p. 22 · CVE:BOCG-15-A-1-1`; `BOCG-15-A-1-4 · Disposición final (tercera) · p. 27 · CVE:BOCG-15-A-1-4`; `BOCG-15-A-1-8 · Disposición final decimocuarta · p. 35 · CVE:BOCG-15-A-1-8`

`q17,correct=__,supported=__,notes=`

---

## q18  ·  `single`

**Question.** ¿Qué obligaciones impone la ley a los partidos políticos en materia de igualdad interna?

**Reference.** Deben tener un plan de igualdad interno que incluya medidas para prevenir y detectar la violencia machista, y establecer un protocolo de actuación ante la violencia machista ejercida, dentro o fuera de la organización, por afiliados o por personas no afiliadas con cargo de representación o función específica, con independencia del nivel jerárquico o del cargo público que ocupen.

**Agent answered:**

> En el texto aprobado definitivamente, la ley impone a los partidos políticos la obligación de contar con un plan de igualdad interno y un protocolo de actuación frente a la violencia machista [BOCG-15-A-1-8 · Disposición final quinta · p. 30 · CVE:BOCG-15-A-1-8].
>
> Según el texto aprobado definitivamente:
>
> «Los partidos políticos deben tener un plan de igualdad interno que incluirá medidas para prevenir y detectar la violencia machista. Asimismo, deben establecer un protocolo de actuación ante la violencia machista que ejerzan, dentro o fuera de la organización, afiliados o bien personas que sin estar afiliadas tengan un cargo de representación o hayan sido designadas para una función específica, con independencia del nivel jerárquico o del cargo público que ocupen.» [BOCG-15-A-1-8 · Disposición final quinta · p. 30 · CVE:BOCG-15-A-1-8]

**Citations (2).** `BOCG-15-A-1-8 · Disposición final quinta · p. 30 · CVE:BOCG-15-A-1-8`; `BOCG-15-A-1-8 · Disposición final quinta · p. 30 · CVE:BOCG-15-A-1-8`

`q18,correct=__,supported=__,notes=`

---

## q19  ·  `single`

**Question.** ¿Qué partes de la ley tienen carácter de ley orgánica?

**Reference.** Toda la ley, salvo los artículos cuarto, séptimo a duodécimo, decimocuarto y decimosexto a decimoctavo, las disposiciones adicionales, los apartados 2 a 6 de la disposición transitoria primera, el apartado 3 de la disposición transitoria segunda y las disposiciones finales primera a tercera y séptima a décima. La modificación del Real Decreto 1006/1985 mantiene rango reglamentario.

**Agent answered:**

> En el texto aprobado definitivamente, la ley tiene carácter de ley orgánica salvo excepciones relativas a determinados artículos, disposiciones adicionales, transitorias y finales, indicando además que la modificación de un real decreto mantiene su rango reglamentario:
>
> «La presente ley tiene el carácter de ley orgánica, a excepción de los artículos cuarto, séptimo a duodécimo, decimocuarto y decimosexto a decimoctavo, de las disposiciones adicionales, de los apartados 2 a 6 de la disposición transitoria primera, del apartado 3 de la disposición transitoria segunda y de las disposiciones finales primera a tercera y séptima a décima. La modificación del Real Decreto 1006/1985 mantiene su rango reglamentario.» [BOCG-15-A-1-8 · Disposición final duodécima · p. 34 · CVE:BOCG-15-A-1-8]
>
> En el trámite de proyecto presentado por el Gobierno, las excepciones abarcaban un conjunto diferente de preceptos:
>
> «La presente ley tiene el carácter de ley orgánica, a excepción de los artículos cuarto, séptimo a undécimo, de las disposiciones adicionales, de los apartados 2 a 6 de la disposición transitoria primera y del apartado 3 de la disposición transitoria segunda.» [BOCG-15-A-1-1 · Disposición final primera · p. 22 · CVE:BOCG-15-A-1-1]

**Citations (2).** `BOCG-15-A-1-8 · Disposición final duodécima · p. 34 · CVE:BOCG-15-A-1-8`; `BOCG-15-A-1-1 · Disposición final primera · p. 22 · CVE:BOCG-15-A-1-1`

`q19,correct=__,supported=__,notes=`

---

## q20  ·  `single`

**Question.** ¿Qué plazo tiene el Consejo General del Poder Judicial para adaptar sus reglamentos y con qué objetivo?

**Reference.** Un año desde la entrada en vigor de la ley orgánica, para adaptar el Reglamento 1/2000 sobre provisión de plazas de nombramiento discrecional, garantizando la presencia equilibrada y permitiendo alcanzar al menos un cuarenta por ciento de mujeres en dichos órganos.

**Agent answered:**

> Según el texto aprobado definitivamente, el Consejo General del Poder Judicial dispone de un plazo de un año desde la entrada en vigor de la ley orgánica para adaptar sus reglamentos, con el fin de garantizar el cumplimiento del principio de presencia equilibrada en los nombramientos discrecionales.
>
> > «Disposición adicional sexta. Adaptación de reglamentos judiciales. En el plazo de un año desde la entrada en vigor de esta ley orgánica, el Consejo General del Poder Judicial deberá adaptar el Acuerdo de 26 de julio de 2000, del Pleno del Consejo General del Poder Judicial, por el que se aprueba el Reglamento 1/2000, de 25 de febrero de 2010, que regula la provisión de plazas de nombramiento discrecional en los órganos judiciales, a lo dispuesto en esta ley orgánica, garantizando el cumplimiento del principio de presencia equilibrada de mujeres y hombres en los nombramientos judiciales de carácter discrecional que permitan alcanzar al menos un cuarenta por ciento de mujeres en dichos órganos.» [BOCG-15-A-1-8 · Disposición adicional sexta · p. 25-26 · CVE:BOCG-15-A-1-8]

**Citations (1).** `BOCG-15-A-1-8 · Disposición adicional sexta · p. 25-26 · CVE:BOCG-15-A-1-8`

`q20,correct=__,supported=__,notes=`

---

## q21  ·  `multi`

**Question.** ¿Cambió la regla sobre las listas de suplentes entre el proyecto de ley y el texto finalmente aprobado?

**Reference.** Sí. El proyecto (15/12/2023) daba a los suplentes una regla propia: «A las listas de suplentes se aplicarán las reglas contenidas en el anterior apartado». El texto aprobado definitivamente (31/07/2024) la sustituye por «La regla anterior se aplicará en el conjunto de las listas, sin separar titulares y suplentes».

**Agent answered:**

> Sí, la regla sobre las listas de suplentes cambió entre el proyecto y el texto definitivamente aprobado. 
>
> En el **proyecto**, se disponía:
> > «2. A las listas de suplentes se aplicarán las reglas contenidas en el anterior apartado.» [BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1]
>
> En cambio, en el texto de **aprobación definitiva**, la redacción del artículo 44.2 bis pasó a ser la siguiente:
> > «2. La regla anterior se aplicará en el conjunto de las listas, sin separar titulares y suplentes.» [BOCG-15-A-1-8 · Artículo primero (1/2) · p. 12 · CVE:BOCG-15-A-1-8]

**Citations (2).** `BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1`; `BOCG-15-A-1-8 · Artículo primero (1/2) · p. 12 · CVE:BOCG-15-A-1-8`

`q21,correct=__,supported=__,notes=`

---

## q22  ·  `multi`

**Question.** ¿En qué fase de la tramitación se introdujo la redacción «sin separar titulares y suplentes»?

**Reference.** Después del Informe de la Ponencia. El informe de 25/06/2024 mantenía todavía la redacción del proyecto («A las listas de suplentes se aplicarán las reglas contenidas en el anterior apartado»); la fórmula «sin separar titulares y suplentes» aparece en el texto aprobado definitivamente de 31/07/2024.

**Agent answered:**

> NO CONSTA EN EL CORPUS
>
> He buscado la expresión «sin separar titulares y suplentes» en todos los documentos del expediente (proyecto, informe de ponencia, debate en pleno y aprobación definitiva) y no aparece en ninguno de ellos.

**Citations (0).** _none_

`q22,correct=__,supported=__,notes=`

---

## q23  ·  `multi`

**Question.** ¿Incluía el proyecto de ley a las Juntas Generales de los Territorios Históricos vascos?

**Reference.** No. El artículo primero del proyecto no las mencionaba; el texto aprobado definitivamente las añade tanto en el apartado 1 como en el apartado 3 del nuevo artículo 44 bis.

**Agent answered:**

> NO CONSTA EN EL CORPUS
>
> Se buscó «Juntas Generales» en el trámite `proyecto` (`BOCG-15-A-1-1`), y el corpus no contiene menciones a ellas en esa fase. Para responder sobre el contenido del proyecto respecto a las Juntas Generales, el corpus debería incluir los textos de enmiendas o documentación previa no incorporada al expediente parlamentario digitalizado del Congreso.

**Citations (0).** _none_

`q23,correct=__,supported=__,notes=`

---

## q24  ·  `multi`

**Question.** ¿Preveía el proyecto de ley excepciones para los municipios pequeños?

**Reference.** No. El artículo primero del proyecto no contenía excepción alguna por tamaño de municipio; el texto aprobado definitivamente añade, al modificar el artículo 187.2 de la LOREG, la exención para municipios de 3.000 residentes o menos y la regla del 60/40 para los de entre 3.000 y 5.000.

**Agent answered:**

> El proyecto de ley presentado por el Gobierno no preveía excepciones para los municipios pequeños en cuanto a la composición de las candidaturas electorales, exigiendo el formato de lista paritaria y alternativa («cremallera») para todas las elecciones municipales sin distinción por tamaño de población [BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1].
>
> Texto del proyecto de ley (*trámite: proyecto*):
> «Las candidaturas que se presenten para las elecciones de diputados y diputadas al Congreso, municipales, de miembros de los consejos insulares y de los cabildos insulares, diputados y diputadas al Parlamento Europeo y miembros de las Asambleas Legislativas de las Comunidades Autónomas deberán tener una composición paritaria de mujeres y hombres, integrándose las listas por personas de uno y otro sexo ordenados de forma alternativa.»
> [BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1]

**Citations (2).** `BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1`; `BOCG-15-A-1-1 · Artículo primero · p. 11-12 · CVE:BOCG-15-A-1-1`

`q24,correct=__,supported=__,notes=`

---

## q25  ·  `multi`

**Question.** ¿Cuándo entra en vigor la ley y a partir de qué elecciones se aplica la reforma del artículo 44 bis?

**Reference.** Entra en vigor a los veinte días de su publicación en el BOE, y la modificación del artículo 44 bis se aplica a los procesos electorales que se convoquen después de esa entrada en vigor.

**Agent answered:**

> En el trámite de aprobación definitiva, la ley establece que su entrada en vigor se producirá a los veinte días de su publicación en el «Boletín Oficial del Estado», y la reforma del artículo 44 bis se aplicará a los procesos electorales convocados tras dicha entrada en vigor:
>
> «La presente ley orgánica entrará en vigor a los veinte días de su publicación en el «Boletín Oficial del Estado» [BOCG-15-A-1-8 · Disposición final decimoquinta · p. 35 · CVE:BOCG-15-A-1-8].»
>
> «La modificación del artículo cuarenta y cuatro bis de la Ley Orgánica 5/1985, de 19 de junio, será de aplicación a los procesos electorales que se convoquen después de la entrada en vigor de esta ley orgánica [BOCG-15-A-1-8 · Disposición transitoria primera · p. 26 · CVE:BOCG-15-A-1-8].»

**Citations (2).** `BOCG-15-A-1-8 · Disposición final decimoquinta · p. 35 · CVE:BOCG-15-A-1-8`; `BOCG-15-A-1-8 · Disposición transitoria primera · p. 26 · CVE:BOCG-15-A-1-8`

`q25,correct=__,supported=__,notes=`

---

## q26  ·  `multi`

**Question.** ¿Qué establece el texto aprobado sobre la composición de las listas y qué objetó VOX en el debate?

**Reference.** El texto aprobado exige candidaturas de composición paritaria con personas de uno y otro sexo ordenadas de forma alternativa, aplicándose la regla al conjunto de las listas. En el debate, la señora Aguirre Gil de Biedma (VOX) dijo que el proyecto «quiere imponer por la fuerza» tanto la composición paritaria de las listas como el 40 % del sexo menos representado en otros órganos.

**Agent answered:**

> Sobre la composición de las listas, el texto aprobado definitivamente en el Congreso (31/07/2024) establece el modelo de **«listas cremallera»**, en el que las candidaturas presentadas por los partidos políticos, federaciones, coaliciones o agrupaciones de electores deben alternar mujeres y hombres de forma rigurosa, de modo que los de un sexo ocupen los puestos pares y los del otro los impares [BOCG-15-A-1-8 · preámbulo (8/21) · p. 5 · CVE:BOCG-15-A-1-8].
>
> Por su parte, durante el debate del Pleno (27/06/2024), la diputada de VOX Blanca Aguirre Gil de Biedma objetó que la ley no iba a aportar ningún beneficio, sino que supondría «primero, la vulneración de la igualdad; segundo, el menoscabo de los principios del mérito y capacidad; tercero, una creciente inseguridad jurídica; cuarto, un ataque frontal a la libertad de empresa; quinto, nefastas consecuencias para la economía y el empleo, y sexto y último, pero no por ello menos importante, paradójicamente, ya que se supone que esta ley está hecha para proteger a las mujeres, va a suponer la degradación de la valía personal y profesional de la mujer» [DSCD-15-PL-54 · La señora AGUIRRE GIL DE BIEDMA (4/4) · p. 18 · CVE:DSCD-15-PL-54].

**Citations (2).** `BOCG-15-A-1-8 · preámbulo (8/21) · p. 5 · CVE:BOCG-15-A-1-8`; `DSCD-15-PL-54 · La señora AGUIRRE GIL DE BIEDMA (4/4) · p. 18 · CVE:DSCD-15-PL-54`

`q26,correct=__,supported=__,notes=`

---

## q27  ·  `unanswerable`

**Question.** ¿Qué texto proponía la enmienda número 24 del Grupo Parlamentario Vasco (EAJ-PNV)?

**Reference.** NO CONSTA EN EL CORPUS. El Diario de Sesiones recoge la votación de la enmienda 24, pero el texto de las enmiendas (BOCG-15-A-1-2) no forma parte del corpus.

**Agent answered:**

> NO CONSTA EN EL CORPUS. 
>
> Buscaba la enmienda número 24 del Grupo Parlamentario Vasco (EAJ-PNV). El corpus únicamente contiene el proyecto del Gobierno, el informe de la ponencia, el texto aprobado definitivamente y el debate del Pleno, pero no incluye las enmiendas presentadas por los grupos parlamentarios.

**Citations (0).** _none_

`q27,correct=__,supported=__,notes=`

---

## q28  ·  `unanswerable`

**Question.** ¿Introdujo el Senado alguna modificación en el proyecto de ley?

**Reference.** NO CONSTA EN EL CORPUS. El corpus cubre solo la tramitación en el Congreso de los Diputados; no incluye el trámite en el Senado.

**Agent answered:**

> NO CONSTA EN EL CORPUS. 
>
> El corpus abarca únicamente la tramitación en el Congreso de los Diputados (proyecto inicial, informe de la ponencia, debate en pleno y aprobación definitiva de julio de 2024), por lo que no contiene la fase del Senado ni las posibles modificaciones introducidas en dicha cámara.

**Citations (0).** _none_

`q28,correct=__,supported=__,notes=`

---

## q29  ·  `unanswerable`

**Question.** ¿Con qué número se publicó finalmente la ley en el Boletín Oficial del Estado?

**Reference.** NO CONSTA EN EL CORPUS. El documento más reciente del corpus es la aprobación definitiva por el Congreso, de 31 de julio de 2024, anterior a la publicación en el BOE.

**Agent answered:**

> NO CONSTA EN EL CORPUS. 
>
> Se buscó el número con el que se publicó la ley en el Boletín Oficial del Estado (BOE), pero el corpus solo contiene la tramitación en el Congreso de los Diputados hasta julio de 2024 (aprobación definitiva en el BOCG), por lo que no incluye la posterior publicación oficial con el número definitivo de ley del BOE.

**Citations (0).** _none_

`q29,correct=__,supported=__,notes=`

---

## q30  ·  `unanswerable`

**Question.** ¿Se interpuso algún recurso de inconstitucionalidad contra la ley?

**Reference.** NO CONSTA EN EL CORPUS. El corpus no contiene nada posterior a julio de 2024.

**Agent answered:**

> NO CONSTA EN EL CORPUS. 
>
> Se buscó información sobre recursos de inconstitucionalidad interpuestos contra la ley, pero el corpus se limita a la tramitación en el Congreso de los Diputados hasta julio de 2024 y no incluye actuaciones posteriores ante el Tribunal Constitucional.

**Citations (0).** _none_

`q30,correct=__,supported=__,notes=`

---

## q31  ·  `unanswerable`

**Question.** ¿Ha adaptado el Parlament de Catalunya su ley electoral a esta norma?

**Reference.** NO CONSTA EN EL CORPUS. El corpus no cubre los parlamentos autonómicos.

**Agent answered:**

> El corpus no cubre los parlamentos autonómicos, por lo que esta cuestión queda fuera del ámbito de los documentos disponibles [Proyecto de Ley Orgánica 121/000001].

**Citations (1).** `Proyecto de Ley Orgánica 121/000001`

`q31,correct=__,supported=__,notes=`

---

## q32  ·  `unanswerable`

**Question.** ¿Qué se debatió en la Comisión de Igualdad sobre el artículo 44 bis?

**Reference.** NO CONSTA EN EL CORPUS. El corpus incluye el informe de la Ponencia y el debate del Pleno, pero no el debate de la Comisión.

**Agent answered:**

> NO CONSTA EN EL CORPUS. 
>
> Se buscó la mención a la Comisión de Igualdad y el artículo 44 bis, pero el corpus no contiene los debates ni los trabajos de las comisiones parlamentarias, limitándose al texto del proyecto, el informe de la ponencia, el debate en Pleno y el texto aprobado definitivamente en el Congreso.

**Citations (0).** _none_

`q32,correct=__,supported=__,notes=`

---
