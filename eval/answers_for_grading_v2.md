# Answers to grade, v2 (no judge verdicts here)

Consolidated corpus; agent and coverage check (v4): gemini-3.5-flash-lite. 45 questions: dev (30), heldout (9), fresh (6).

For each: correct = right against the reference (or a proper refusal); supported = every claim is in the retrieved text.

When the coverage check says NO for every search, the code replaces the agent's text with the fixed refusal (marked below as *forced refusal*); the model's own text is not kept.


---
## q01 (single, dev)
**Question:** ¿Quién designa al coordinador de seguridad y salud durante la ejecución de la obra?
**Reference:** El promotor, antes del inicio de los trabajos o tan pronto como intervenga más de una empresa o autónomos.
**Answer:**

El **promotor** es quien designa al coordinador de seguridad y salud durante la ejecución de la obra, antes del inicio de los trabajos o tan pronto como se constate que interviene más de una empresa, una empresa y trabajadores autónomos, o diversos trabajadores autónomos.

Fuentes:
- RD 1627/1997, Artículo 3 (apartados 2 y 4).
- Ley 32/2006, Artículo 3.

**Citations:** RD 1627/1997, Artículo 3; Ley 32/2006, Artículo 3 — all in retrieved text

**Coverage check:**

- Search 1 «quien designa al coordinador de seguridad y salud durante la ejecucion de la obra»: **SÍ**, passage [1], quote: «2. Cuando en la ejecución de la obra intervenga más de una empresa, o una empresa y trabajadores autónomos o diversos trabajadores autónomos, el promotor, antes del inicio de los trabajos o tan pronto como se constate dicha circunstancia, designará un coordinador en materia de seguridad y salud durante la ejecución de la obra.». Need: quién designa al coordinador de seguridad y salud durante la ejecución de la obra

**Retrieved passages:**

[1] RD 1627/1997, Artículo 3 (score 0.807)
RD 1627/1997, Artículo 3
Artículo 3. Designación de los coordinadores en materia de seguridad y salud.
1. En las obras incluidas en el ámbito de aplicación del presente Real Decreto, cuando en la elaboración del proyecto de obra intervengan varios proyectistas, el promotor designará un coordinador en materia de seguridad y de salud durante la elaboración del proyecto de obra.
2. Cuando en la ejecución de la obra intervenga más de una empresa, o una empresa y trabajadores autónomos o diversos trabajadores autónomos, el promotor, antes del inicio de los trabajos o tan pronto como se constate dicha circunstancia, designará un coordinador en materia de seguridad y salud durante la ejecución de la obra.
3. La designación de los coordinadores en materia de seguridad y salud durante la elaboración del proyecto de obra y durante la ejecución de la obra podrá recaer en la misma persona.
4. La designación de los coordinadores no eximirá al promotor de sus responsabilidades.

[2] RD 1627/1997, Artículo 9 (score 0.788)
RD 1627/1997, Artículo 9
Artículo 9. Obligaciones del coordinador en materia de seguridad y de salud durante la ejecución de la obra.
El coordinador en materia de seguridad y salud durante la ejecución de la obra deberá desarrollar las siguientes funciones:
a) Coordinar la aplicación de los principios generales de prevención y de seguridad:
1.º Al tomar las decisiones técnicas y de organización con el fin de planificar los distintos trabajos o fases de trabajo que vayan a desarrollarse simultánea o sucesivamente.
2.º Al estimar la duración requerida para la ejecución de estos distintos trabajos o fases de trabajo.
b) Coordinar las actividades de la obra para garantizar que los contratistas y, en su caso, los subcontratistas y los trabajadores autónomos apliquen de manera coherente y responsable los principios de la acción preventiva que se recogen en el artículo 15 de la Ley de Prevención de Riesgos Laborales durante la ejecución de la obra y, en particular, en las tareas o actividades a que se refiere el artículo 10 de este Real Decreto.
c) Aprobar el plan de seguridad y salud elaborado por el contratista y, en su caso, las modificaciones introducidas en el mismo. Conforme a lo dispuesto en el último párrafo del apartado 2 del artículo 7, la dirección facultativa asumirá esta función cuando no fuera necesaria la designación de coordinador.
d) Organizar la coordinación de actividades empresariales prevista en el artículo 24 de la Ley de Prevención de Riesgos Laborales.
e) Coordinar las acciones y funciones de control de la aplicación correcta de los métodos de trabajo.
f) Adoptar las medidas necesarias para que sólo las personas autorizadas puedan acceder a la obra. La dirección facultativa asumirá esta función cuando no fuera necesaria la designación de coordinador.

[3] RD 1627/1997, Artículo 2 (score 0.764)
RD 1627/1997, Artículo 2
Artículo 2. Definiciones.
1. A efectos del presente Real Decreto, se entenderá por:
a) Obra de construcción u obra: cualquier obra, pública o privada, en la que se efectúen trabajos de construcción o ingeniería civil cuya relación no exhaustiva figura en el anexo I.
b) Trabajos con riesgos especiales: trabajos cuya realización exponga a los trabajadores a riesgos de especial gravedad para su seguridad y salud, comprendidos los indicados en la relación no exhaustiva que figura en el anexo II.
c) Promotor: cualquier persona física o jurídica por cuenta de la cual se realice una obra.
d) Proyectista: el autor o autores, por encargo del promotor, de la totalidad o parte del proyecto de obra.
e) Coordinador en materia de seguridad y de salud durante la elaboración del proyecto de obra: el técnico competente designado por el promotor para coordinar, durante la fase del proyecto de obra, la aplicación de los principios que se mencionan en el artículo 8.
f) Coordinador en materia de seguridad y de salud durante la ejecución de la obra: el técnico competente integrado en la dirección facultativa, designado por el promotor para llevar a cabo las tareas que se mencionan en el artículo 9.
g) Dirección facultativa: el técnico o técnicos competentes designados por el promotor, encargados de la dirección y del control de la ejecución de la obra.
h) Contratista: la persona física o jurídica que asume contractualmente ante el promotor, con medios humanos y materiales, propios o ajenos, el compromiso de ejecutar la totalidad o parte de las obras con sujeción al proyecto y al contrato.
i) Subcontratista: la persona física o jurídica que asume contractualmente ante el contratista, empresario principal, el compromiso de realizar determinadas partes o instalaciones de la obra, con sujeción al proyecto por el que se rige su ejecución.

[4] Ley 32/2006, Artículo 3 (score 0.761)
Ley 32/2006, Artículo 3
Artículo 3. Definiciones.
A efectos de esta Ley se entenderá por:
a) Obra de construcción u obra: cualquier obra, pública o privada, en la que se efectúen trabajos de construcción o de ingeniería civil.
b) Promotor: cualquier persona física o jurídica por cuenta de la cual se realice la obra.
c) Dirección facultativa: el técnico o técnicos competentes designados por el promotor, encargados de la dirección y del control de la ejecución de la obra.
d) Coordinador en materia de seguridad y de salud durante la ejecución de la obra: el técnico competente integrado en la dirección facultativa, designado por el promotor para llevar a cabo las tareas establecidas para este coordinador en la reglamentación de seguridad y salud en las obras de construcción.
e) Contratista o empresario principal: la persona física o jurídica, que asume contractualmente ante el promotor, con medios humanos y materiales, propios o ajenos, el compromiso de ejecutar la totalidad o parte de las obras con sujeción al proyecto y al contrato.
Cuando el promotor realice directamente con medios humanos y materiales propios la totalidad o determinadas partes de la obra, tendrá también la consideración de contratista a los efectos de la presente Ley; asimismo, cuando la contrata se haga con una Unión Temporal de Empresas, que no ejecute directamente la obra, cada una de sus empresas miembro tendrá la consideración de empresa contratista en la parte de obra que ejecute.
f) Subcontratista: la persona física o jurídica que asume contractualmente ante el contratista u otro subcontratista comitente el compromiso de realizar determinadas partes o unidades de obra, con sujeción al proyecto por el que se rige su ejecución. Las variantes de esta figura pueden ser las del primer subcontratista (subcontratista cuyo comitente es el contratista), segundo subcontratista (subcontratista cuyo comitente es el primer subcontratista), y así sucesivamente.

[5] RD 1627/1997, Artículo 14 (score 0.759)
RD 1627/1997, Artículo 14
Artículo 14. Paralización de los trabajos.
1. Sin perjuicio de lo previsto en los apartados 2 y 3 del artículo 21 y en el artículo 44 de la Ley de Prevención de Riesgos Laborales, cuando el coordinador en materia de seguridad y salud durante la ejecución de la obra o cualquier otra persona integrada en la dirección facultativa observase incumplimiento de las medidas de seguridad y salud, advertirá al contratista de ello, dejando constancia de tal incumplimiento en el libro de incidencias, cuando éste exista de acuerdo con lo dispuesto en el apartado 1 del artículo 13, y quedando facultado para, en circunstancias de riesgo grave e inminente para la seguridad y la salud de los trabajadores, disponer la paralización de los tajos o, en su caso, de la totalidad de la obra.
2. En el supuesto previsto en el apartado anterior, la persona que hubiera ordenado la paralización deberá dar cuenta a los efectos oportunos a la Inspección de Trabajo y Seguridad Social correspondiente, a los contratistas y, en su caso, a los subcontratistas afectados por la paralización, así como a los representantes de los trabajadores de éstos.
3. Asimismo, lo dispuesto en este artículo se entiende sin perjuicio de la normativa sobre contratos de las Administraciones públicas relativa al cumplimiento de plazos y suspensión de obras.

---
## q02 (unanswerable, dev)
**Question:** ¿Cuántos días de vacaciones tiene un albañil según el convenio colectivo?
**Reference:** El corpus no lo cubre; debe decir que no consta en los documentos.
**Answer:** *(forced refusal)*

No consta en los documentos del corpus.

Se buscó en el corpus: «vacaciones albañil convenio colectivo».

**Citations:** (none)

**Coverage check:**

- Search 1 «vacaciones albañil convenio colectivo»: **NO**. Need: el número de días de vacaciones que tiene un albañil según el convenio colectivo

**Retrieved passages:**

[1] Ley 32/2006, Disposición adicional tercera (score 0.681)
Ley 32/2006, Disposición adicional tercera
c) La inexistencia en la provincia en la que esté contratada la persona trabajadora de obras de la empresa acordes a su cualificación profesional, nivel, función y grupo profesional una vez analizada su cualificación o posible recualificación.
En el supuesto a) anterior, la persona trabajadora deberá notificar por escrito a la empresa la aceptación o rechazo de la propuesta en el plazo de siete días desde que tenga conocimiento de la comunicación empresarial. Transcurrido dicho plazo sin contestación se entenderá que la persona trabajadora rechaza la propuesta de recolocación.
En los supuestos recogidos en los apartados b) y c) precedentes, la empresa deberá notificar la extinción del contrato a la persona trabajadora afectada con una antelación de quince días a su efectividad.
6. La extinción del contrato indefinido por motivos inherentes a la persona trabajadora deberá ser puesta en conocimiento de la representación legal de las personas trabajadoras con una antelación de siete días a su efectividad y dará lugar a una indemnización del siete por ciento calculada sobre los conceptos salariales establecidos en las tablas del convenio colectivo que resulte de aplicación y que hayan sido devengados durante toda la vigencia del contrato, o la superior establecida por el Convenio General del Sector de la Construcción.

[2] Ley 32/2006, Artículo 2 (score 0.669)
Ley 32/2006, Artículo 2
Artículo 2. Ámbito de aplicación.
La presente Ley será de aplicación a los contratos que se celebren, en régimen de subcontratación, para la ejecución de los siguientes trabajos realizados en obras de construcción:
Excavación; movimiento de tierras; construcción; montaje y desmontaje de elementos prefabricados; acondicionamientos o instalaciones; transformación; rehabilitación; reparación; desmantelamiento; derribo; mantenimiento; conservación y trabajos de pintura y limpieza; saneamiento.

[3] Ley 32/2006, Artículo 4 (score 0.668)
Ley 32/2006, Artículo 4
4. Las empresas cuya actividad consista en ser contratadas o subcontratadas habitualmente para la realización de trabajos en obras del sector de la construcción deberán contar, en los términos que se determine reglamentariamente, con un número de trabajadores contratados con carácter indefinido que no será inferior al 10 por ciento durante los dieciocho primeros meses de vigencia de esta Ley, ni al 20 por ciento durante los meses del decimonoveno al trigésimo sexto, ni al 30 por ciento a partir del mes trigésimo séptimo, inclusive.
A estos efectos, en las cooperativas de trabajo asociado los socios trabajadores serán computados de manera análoga a los trabajadores por cuenta ajena en los términos que se determine reglamentariamente.

[4] Ley 32/2006, Disposición adicional tercera (score 0.665)
Ley 32/2006, Disposición adicional tercera
Disposición adicional tercera. Extinción del contrato indefinido por motivos inherentes a la persona trabajadora en el sector de la construcción.
1. Sin perjuicio de lo previsto en la sección 4.ª del capítulo III del título I del Estatuto de los Trabajadores, los contratos de trabajo indefinidos adscritos a obra celebrados en el ámbito de las empresas del sector de la construcción, podrán extinguirse por motivos inherentes a la persona trabajadora conforme a lo dispuesto en la presente disposición, que resultará aplicable con independencia del número de personas trabajadoras afectadas.
Tendrán la consideración de contratos indefinidos adscritos a obra aquellos que tengan por objeto tareas o servicios cuya finalidad y resultado estén vinculados a obras de construcción, teniendo en cuenta las actividades establecidas en el ámbito funcional del Convenio General del Sector de la Construcción.
La extinción regulada en este artículo no resultará aplicable a las personas trabajadoras que formen parte del personal de estructura.
2. La finalización de la obra en la que presta servicios la persona trabajadora determinará la obligación para la empresa de efectuarle una propuesta de recolocación, previo desarrollo, de ser preciso, de un proceso de formación.
Este proceso, que será siempre a cargo de la empresa, podrá realizarse directamente o a través de una entidad especializada, siendo preferente la formación que imparta la Fundación Laboral de la Construcción con cargo a las cuotas empresariales.
La negociación colectiva de ámbito estatal del sector de la construcción determinará los requisitos de acceso, duración y modalidades de formación adecuadas según las cualificaciones requeridas para cada puesto, nivel, función y grupo profesional.
El indicado proceso de formación podrá desarrollarse con antelación a la finalización de la obra.
3. A efectos de lo previsto en esta disposición, se entenderá por finalización de las obras y servicios la terminación real, verificable y efectiva de los trabajos desarrollados por esta.

[5] Ley 32/2006, Disposición adicional tercera (score 0.657)
Ley 32/2006, Disposición adicional tercera
Asimismo, tendrán la consideración de finalización de obra la disminución real del volumen de obra por la realización paulatina de las correspondientes unidades de ejecución debidamente acreditada, así como la paralización, definitiva o temporal, de entidad suficiente, de una obra, por causa imprevisible para la empresa y ajena a su voluntad.
La finalización de la obra deberá ser puesta en conocimiento de la representación legal de las personas trabajadoras, en su caso, así como de las comisiones paritarias de los convenios de ámbito correspondiente o, en su defecto, de los sindicatos representativos del sector, con cinco días de antelación a su efectividad y dará lugar a la propuesta de recolocación prevista en esta disposición.
4. La propuesta de recolocación prevista en esta disposición será formalizada por escrito mediante una cláusula que se anexará al contrato de trabajo.
Esta cláusula, que deberá precisar las condiciones esenciales, ubicación de la obra y fecha de incorporación a la misma, así como las acciones formativas exigibles para ocupar el nuevo puesto, será sometida a aceptación por parte de la persona trabajadora con quince días de antelación a la finalización de su trabajo en la obra en la que se encuentre prestando servicios.
5. Una vez efectuada la propuesta de recolocación, el contrato indefinido adscrito a obra podrá extinguirse por motivos inherentes a la persona trabajadora cuando se dé alguna de las siguientes circunstancias:
a) La persona trabajadora afectada rechaza la recolocación.
b) La cualificación de la persona afectada, incluso tras un proceso de formación o recualificación, no resulta adecuada a las nuevas obras que tenga la empresa en la misma provincia, o no permite su integración en estas, por existir un exceso de personas con la cualificación necesaria para desarrollar sus mismas funciones.
La negociación colectiva de ámbito estatal del sector correspondiente precisará los criterios de prioridad o permanencia que deben operar en caso de concurrir estos motivos en varias personas trabajadoras de forma simultánea en relación con la misma obra.

---
## q03 (single, dev)
**Question:** ¿A partir de cuántos trabajadores es obligatorio constituir un Comité de Seguridad y Salud?
**Reference:** En las empresas o centros de trabajo con 50 o más trabajadores.
**Answer:**

Es obligatorio constituir un Comité de Seguridad y Salud en todas las empresas o centros de trabajo que cuenten con **50 o más trabajadores** (Ley 31/1995, Artículo 38).

Fuentes utilizadas:
- Ley 31/1995 (Prevención de Riesgos Laborales), Artículo 38.

**Citations:** Ley 31/1995, Artículo 38 — all in retrieved text

**Coverage check:**

- Search 1 «Comite de Seguridad y Salud numero de trabajadores»: **SÍ**, passage [1], quote: «2. Se constituirá un Comité de Seguridad y Salud en todas las empresas o centros de trabajo que cuenten con 50 o más trabajadores.». Need: a partir de qué número de trabajadores es obligatorio constituir un Comité de Seguridad y Salud

**Retrieved passages:**

[1] Ley 31/1995, Artículo 38 (score 0.781)
Ley 31/1995, Artículo 38
Artículo 38. Comité de Seguridad y Salud.
1. El Comité de Seguridad y Salud es el órgano paritario y colegiado de participación destinado a la consulta regular y periódica de las actuaciones de la empresa en materia de prevención de riesgos.
2. Se constituirá un Comité de Seguridad y Salud en todas las empresas o centros de trabajo que cuenten con 50 o más trabajadores.
El Comité estará formado por los Delegados de Prevención, de una parte, y por el empresario y/o sus representantes en número igual al de los Delegados de Prevención, de la otra.
En las reuniones del Comité de Seguridad y Salud participarán, con voz pero sin voto, los Delegados Sindicales y los responsables técnicos de la prevención en la empresa que no estén incluidos en la composición a la que se refiere el párrafo anterior. En las mismas condiciones podrán participar trabajadores de la empresa que cuenten con una especial cualificación o información respecto de concretas cuestiones que se debatan en este órgano y técnicos en prevención ajenos a la empresa, siempre que así lo solicite alguna de las representaciones en el Comité.
3. El Comité de Seguridad y Salud se reunirá trimestralmente y siempre que lo solicite alguna de las representaciones en el mismo. El Comité adoptará sus propias normas de funcionamiento.
Las empresas que cuenten con varios centros de trabajo dotados de Comité de Seguridad y Salud podrán acordar con sus trabajadores la creación de un Comité Intercentros, con las funciones que el acuerdo le atribuya.

[2] Ley 31/1995, Artículo 35 (score 0.747)
Ley 31/1995, Artículo 35
Artículo 35. Delegados de Prevención.
1. Los Delegados de Prevención son los representantes de los trabajadores con funciones específicas en materia de prevención de riesgos en el trabajo.
2. Los Delegados de Prevención serán designados por y entre los representantes del personal, en el ámbito de los órganos de representación previstos en las normas a que se refiere el artículo anterior, con arreglo a la siguiente escala:
De 50 a 100 trabajadores: 2 Delegados de Prevención.
De 101 a 500 trabajadores: 3 Delegados de Prevención.
De 501 a 1.000 trabajadores: 4 Delegados de Prevención.
De 1.001 a 2.000 trabajadores: 5 Delegados de Prevención.
De 2.001 a 3.000 trabajadores: 6 Delegados de Prevención.
De 3.001 a 4.000 trabajadores: 7 Delegados de Prevención.
De 4.001 en adelante: 8 Delegados de Prevención.
En las empresas de hasta treinta trabajadores el Delegado de Prevención será el Delegado de Personal. En las empresas de treinta y uno a cuarenta y nueve trabajadores habrá un Delegado de Prevención que será elegido por y entre los Delegados de Personal.
3. A efectos de determinar el número de Delegados de Prevención se tendrán en cuenta los siguientes criterios:
a) Los trabajadores vinculados por contratos de duración determinada superior a un año se computarán como trabajadores fijos de plantilla.
b) Los contratados por término de hasta un año se computarán según el número de días trabajados en el período de un año anterior a la designación. Cada doscientos días trabajados o fracción se computarán como un trabajador más.
4. No obstante lo dispuesto en el presente artículo, en los convenios colectivos podrán establecerse otros sistemas de designación de los Delegados de Prevención, siempre que se garantice que la facultad de designación corresponde a los representantes del personal o a los propios trabajadores.

[3] Ley 31/1995, Artículo 39 (score 0.744)
Ley 31/1995, Artículo 39
Artículo 39. Competencias y facultades del Comité de Seguridad y Salud.
1. El Comité de Seguridad y Salud tendrá las siguientes competencias:
a) Participar en la elaboración, puesta en práctica y evaluación de los planes y programas de prevención de riesgos de la empresa. A tal efecto, en su seno se debatirán, antes de su puesta en práctica y en lo referente a su incidencia en la prevención de riesgos, la elección de la modalidad organizativa de la empresa y, en su caso, la gestión realizada por las entidades especializadas con las que la empresa hubiera concertado la realización de actividades preventivas; los proyectos en materia de planificación, organización del trabajo e introducción de nuevas tecnologías, organización y desarrollo de las actividades de protección y prevención a que se refiere el artículo 16 de esta Ley y proyecto y organización de la formación en materia preventiva.
b) Promover iniciativas sobre métodos y procedimientos para la efectiva prevención de los riesgos, proponiendo a la empresa la mejora de las condiciones o la corrección de las deficiencias existentes.
2. En el ejercicio de sus competencias, el Comité de Seguridad y Salud estará facultado para:
a) Conocer directamente la situación relativa a la prevención de riesgos en el centro de trabajo, realizando a tal efecto las visitas que estime oportunas.
b) Conocer cuantos documentos e informes relativos a las condiciones de trabajo sean necesarios para el cumplimiento de sus funciones, así como los procedentes de la actividad del servicio de prevención, en su caso.
c) Conocer y analizar los daños producidos en la salud o en la integridad física de los trabajadores, al objeto de valorar sus causas y proponer las medidas preventivas oportunas.
d) Conocer e informar la memoria y programación anual de servicios de prevención.

[4] Ley 31/1995, Artículo 34 (score 0.739)
Ley 31/1995, Artículo 34
b) Se deberá establecer el ámbito específico que resulte adecuado en cada caso para el ejercicio de la función de participación en materia preventiva dentro de la estructura organizativa de la Administración. Con carácter general, dicho ámbito será el de los órganos de representación del personal al servicio de las Administraciones públicas, si bien podrán establecerse otros distintos en función de las características de la actividad y frecuencia de los riesgos a que puedan encontrarse expuestos los trabajadores.
c) Cuando en el indicado ámbito existan diferentes órganos de representación del personal, se deberá garantizar una actuación coordinada de todos ellos en materia de prevención y protección de la seguridad y la salud en el trabajo, posibilitando que la participación se realice de forma conjunta entre unos y otros, en el ámbito específico establecido al efecto.
d) Con carácter general, se constituirá un único Comité de Seguridad y Salud en el ámbito de los órganos de representación previstos en la Ley de Organos de Representación del Personal al Servicio de las Administraciones Públicas, que estará integrado por los Delegados de Prevención designados en dicho ámbito, tanto para el personal con relación de carácter administrativo o estatutario como para el personal laboral, y por representantes de la Administración en número no superior al de Delegados. Ello no obstante, podrán constituirse Comités de Seguridad y Salud en otros ámbitos cuando las razones de la actividad y el tipo y frecuencia de los riesgos así lo aconsejen.

[5] Ley 31/1995, Artículo 34 (score 0.73)
Ley 31/1995, Artículo 34
Artículo 34. Derechos de participación y representación.
1. Los trabajadores tienen derecho a participar en la empresa en las cuestiones relacionadas con la prevención de riesgos en el trabajo.
En las empresas o centros de trabajo que cuenten con seis o más trabajadores, la participación de éstos se canalizará a través de sus representantes y de la representación especializada que se regula en este capítulo.
2. A los Comités de Empresa, a los Delegados de Personal y a los representantes sindicales les corresponde, en los términos que, respectivamente, les reconocen el Estatuto de los Trabajadores, la Ley de Organos de Representación del Personal al Servicio de las Administraciones Públicas y la Ley Orgánica de Libertad Sindical, la defensa de los intereses de los trabajadores en materia de prevención de riesgos en el trabajo. Para ello, los representantes del personal ejercerán las competencias que dichas normas establecen en materia de información, consulta y negociación, vigilancia y control y ejercicio de acciones ante las empresas y los órganos y tribunales competentes.
3. El derecho de participación que se regula en este capítulo se ejercerá en el ámbito de las Administraciones públicas con las adaptaciones que procedan en atención a la diversidad de las actividades que desarrollan y las diferentes condiciones en que éstas se realizan, la complejidad y dispersión de su estructura organizativa y sus peculiaridades en materia de representación colectiva, en los términos previstos en la Ley 7/1990, de 19 de julio, sobre negociación colectiva y participación en la determinación de las condiciones de trabajo de los empleados públicos, pudiéndose establecer ámbitos sectoriales y descentralizados en función del número de efectivos y centros.
Para llevar a cabo la indicada adaptación en el ámbito de la Administración General del Estado, el Gobierno tendrá en cuenta los siguientes cr

---
## q04 (single, dev)
**Question:** ¿Quién facilita el libro de incidencias en una obra de construcción privada?
**Reference:** El Colegio profesional al que pertenezca el técnico que haya aprobado el plan de seguridad y salud.
**Answer:**

En una obra de construcción privada, el libro de incidencias será facilitado por **el Colegio profesional al que pertenezca el técnico que haya aprobado el plan de seguridad y salud** (RD 1627/1997, Artículo 13).

Fuentes:
- RD 1627/1997, Artículo 13.

*Nota: Esta información es meramente divulgativa y se basa en la normativa citada.*

**Citations:** RD 1627/1997, Artículo 13 — all in retrieved text

**Coverage check:**

- Search 1 «libro de incidencias facilita obra privada»: **SÍ**, passage [1], quote: «a) El Colegio profesional al que pertenezca el técnico que haya aprobado el plan de seguridad y salud.». Need: Quién facilita el libro de incidencias en una obra de construcción privada.

**Retrieved passages:**

[1] RD 1627/1997, Artículo 13 (score 0.75)
RD 1627/1997, Artículo 13
Artículo 13. Libro de incidencias.
1. En cada centro de trabajo existirá con fines de control y seguimiento del plan de seguridad y salud un libro de incidencias que constará de hojas por duplicado, habilitado al efecto.
2. El libro de incidencias será facilitado por:
a) El Colegio profesional al que pertenezca el técnico que haya aprobado el plan de seguridad y salud.
b) La Oficina de Supervisión de Proyectos u órgano equivalente cuando se trate de obras de las Administraciones públicas.
3. El libro de incidencias, que deberá mantenerse siempre en la obra, estará en poder del coordinador en materia de seguridad y salud durante la ejecución de la obra o, cuando no fuera necesaria la designación de coordinador, en poder de la dirección facultativa. A dicho libro tendrán acceso la dirección facultativa de la obra, los contratistas y subcontratistas y los trabajadores autónomos, así como las personas u órganos con responsabilidades en materia de prevención en las empresas intervinientes en la obra, los representantes de los trabajadores y los técnicos de los órganos especializados en materia de seguridad y salud en el trabajo de las Administraciones públicas competentes, quienes podrán hacer anotaciones en el mismo, relacionadas con los fines que al libro se le reconocen en el apartado 1.
4. Efectuada una anotación en el libro de incidencias, el coordinador en materia de seguridad y salud durante la ejecución de la obra o, cuando no sea necesaria la designación de coordinador, la dirección facultativa, deberán notificarla al contratista afectado y a los representantes de los trabajadores de éste. En el caso de que la anotación se refiera a cualquier incumplimiento de las advertencias u observaciones previamente anotadas en dicho libro por las personas facultadas para ello, así como en el supuesto a que se refiere el artículo siguiente, deberá remitirse una copia a la Inspección de Trabajo y Seguridad Social en el plazo de veinticuatro horas. En todo caso, deberá especificarse si la anotación efectuada supone una reiteración de una advertencia u observación anterior o si, por el contrario, se trata de una nueva observación.

[2] Ley 32/2006, Anexo (score 0.718)
Ley 32/2006, Anexo
ANEXO
A) DATOS IDENTIFICATIVOS DE LA OBRA
Promotor
NIF
Contratista
NIF
Dirección Facultativa
NIF
Coordinador de seg. y salud en fase de ejecución
NIF
Domicilio de la obra
Localidad
B) REGISTRO DE SUBCONTRATACIONES
N.º orden
Empresa subcontratista o trabajador autónomo/NIF
Nivel de subcontratación
N.º orden del comitente (1)
Fecha comienzo trabajos
Objeto del contrato
Responsable de dirección trabajos/Representantes de los trabajadores
Fecha entrega plan de seg. y salud
Referencia de instrucciones del coordinador (2)
Firma del subcontratista o trabajador autónomo
Aprobación de la Dirección Facultativa (3)
(1) En esta columna se anotará el N.º de orden correspondiente al asiento de la empresa que ha subcontratado los trabajos a la subcontratista de este asiento, dejándose en blanco en caso de que la comitente sea la empresa contratista.
(2) En esta columna se hará constar, en su caso, la referencia de las hojas del Libro de incidencias al plan de seguridad y salud del contratista en las que el Coordinador de seguridad y salud en fase de ejecución haya efectuado anotaciones sobre las instrucciones sobre el desarrollo del procedimiento de coordinación establecido.
(3) Cuando proceda, se hará constar en esta columna la aprobación de la subcontratación a que se refiere el asiento por parte de la Dirección Facultativa, mediante la firma del mismo en esta casilla y la indicación de su fecha.

[3] RD 1627/1997, Artículo 14 (score 0.692)
RD 1627/1997, Artículo 14
Artículo 14. Paralización de los trabajos.
1. Sin perjuicio de lo previsto en los apartados 2 y 3 del artículo 21 y en el artículo 44 de la Ley de Prevención de Riesgos Laborales, cuando el coordinador en materia de seguridad y salud durante la ejecución de la obra o cualquier otra persona integrada en la dirección facultativa observase incumplimiento de las medidas de seguridad y salud, advertirá al contratista de ello, dejando constancia de tal incumplimiento en el libro de incidencias, cuando éste exista de acuerdo con lo dispuesto en el apartado 1 del artículo 13, y quedando facultado para, en circunstancias de riesgo grave e inminente para la seguridad y la salud de los trabajadores, disponer la paralización de los tajos o, en su caso, de la totalidad de la obra.
2. En el supuesto previsto en el apartado anterior, la persona que hubiera ordenado la paralización deberá dar cuenta a los efectos oportunos a la Inspección de Trabajo y Seguridad Social correspondiente, a los contratistas y, en su caso, a los subcontratistas afectados por la paralización, así como a los representantes de los trabajadores de éstos.
3. Asimismo, lo dispuesto en este artículo se entiende sin perjuicio de la normativa sobre contratos de las Administraciones públicas relativa al cumplimiento de plazos y suspensión de obras.

[4] Ley 32/2006, Artículo 8 (score 0.681)
Ley 32/2006, Artículo 8
Artículo 8. Documentación de la subcontratación.
1. En toda obra de construcción, incluida en el ámbito de aplicación de esta Ley, cada contratista deberá disponer de un Libro de Subcontratación.
En dicho libro, que deberá permanecer en todo momento en la obra, se deberán reflejar, por orden cronológico desde el comienzo de los trabajos, todas y cada una de las subcontrataciones realizadas en una determinada obra con empresas subcontratistas y trabajadores autónomos, su nivel de subcontratación y empresa comitente, el objeto de su contrato, la identificación de la persona que ejerce las facultades de organización y dirección de cada subcontratista y, en su caso, de los representantes legales de los trabajadores de la misma, las respectivas fechas de entrega de la parte del plan de seguridad y salud que afecte a cada empresa subcontratista y trabajador autónomo, así como las instrucciones elaboradas por el coordinador de seguridad y salud para marcar la dinámica y desarrollo del procedimiento de coordinación establecido, y las anotaciones efectuadas por la dirección facultativa sobre su aprobación de cada subcontratación excepcional de las previstas en el artículo 5.3 de esta Ley.
Al Libro de Subcontratación tendrán acceso el promotor, la dirección facultativa, el coordinador de seguridad y salud en fase de ejecución de la obra, las empresas y trabajadores autónomos intervinientes en la obra, los técnicos de prevención, los delegados de prevención, la autoridad laboral y los representantes de los trabajadores de las diferentes empresas que intervengan en la ejecución de la obra.
2. Asimismo, cada empresa deberá disponer de la documentación o título que acredite la posesión de la maquinaria que utiliza, y de cuanta documentación sea exigida por las disposiciones legales vigentes.
3. Reglamentariamente se determinarán las condiciones del Libro de Subcontratación al que se refiere el apartado 1, en cuanto a su régimen de habilitación, por la autoridad laboral autonómica competente, así como el contenido y obligaciones y derechos derivados del mismo, al tiempo que se procederá a una revisión de las distintas obligaciones documentales aplicables a las obras de construcción con objeto de lograr su unificación y simplificación.

[5] Ley 32/2006, Disposición transitoria segunda (score 0.665)
Ley 32/2006, Disposición transitoria segunda
Disposición transitoria segunda. Aplicación transitoria de la documentación del régimen de subcontratación.
En tanto no se determinen las condiciones y el modo de habilitación del Libro de Subcontratación regulado en el artículo 8, el régimen de subcontratación previsto en el artículo 5 se documentará mediante la cumplimentación de la ficha que se inserta como Anexo de esta Ley. La forma de utilización de las fichas y el acceso a las mismas se llevará a cabo en los mismos supuestos y condiciones previstos para el Libro de Subcontratación en esta Ley.

---
## q05 (single, dev)
**Question:** ¿Qué debe hacer el promotor ante la autoridad laboral antes de empezar los trabajos de una obra?
**Reference:** El aviso previo del promotor (art. 18) fue derogado por el RD 337/2010. Ahora la comunicación de apertura del centro de trabajo debe ser previa al comienzo de los trabajos y la presentan solo los contratistas (art. 19).
**Answer:** *(forced refusal)*

No consta en los documentos del corpus.

Se buscó en el corpus: «promotor autoridad laboral antes de empezar los trabajos obra».

**Citations:** (none)

**Coverage check:**

- Search 1 «promotor autoridad laboral antes de empezar los trabajos obra»: **NO**. Need: qué debe hacer el promotor ante la autoridad laboral antes de empezar los trabajos de una obra

**Retrieved passages:**

[1] RD 1627/1997, Artículo 19 (score 0.776)
RD 1627/1997, Artículo 19
Artículo 19. Información a la autoridad laboral.
1. La comunicación de apertura del centro de trabajo a la autoridad laboral competente deberá ser previa al comienzo de los trabajos y se presentará únicamente por los empresarios que tengan la consideración de contratistas de acuerdo con lo dispuesto en este real decreto.
La comunicación de apertura incluirá el plan de seguridad y salud al que se refiere el artículo 7 del presente real decreto.
2. El plan de seguridad y salud estará a disposición permanente de la Inspección de Trabajo y Seguridad Social y de los técnicos de los órganos especializados en materia de seguridad y salud en las Administraciones públicas competentes.

[2] Ley 32/2006, Artículo 3 (score 0.772)
Ley 32/2006, Artículo 3
Artículo 3. Definiciones.
A efectos de esta Ley se entenderá por:
a) Obra de construcción u obra: cualquier obra, pública o privada, en la que se efectúen trabajos de construcción o de ingeniería civil.
b) Promotor: cualquier persona física o jurídica por cuenta de la cual se realice la obra.
c) Dirección facultativa: el técnico o técnicos competentes designados por el promotor, encargados de la dirección y del control de la ejecución de la obra.
d) Coordinador en materia de seguridad y de salud durante la ejecución de la obra: el técnico competente integrado en la dirección facultativa, designado por el promotor para llevar a cabo las tareas establecidas para este coordinador en la reglamentación de seguridad y salud en las obras de construcción.
e) Contratista o empresario principal: la persona física o jurídica, que asume contractualmente ante el promotor, con medios humanos y materiales, propios o ajenos, el compromiso de ejecutar la totalidad o parte de las obras con sujeción al proyecto y al contrato.
Cuando el promotor realice directamente con medios humanos y materiales propios la totalidad o determinadas partes de la obra, tendrá también la consideración de contratista a los efectos de la presente Ley; asimismo, cuando la contrata se haga con una Unión Temporal de Empresas, que no ejecute directamente la obra, cada una de sus empresas miembro tendrá la consideración de empresa contratista en la parte de obra que ejecute.
f) Subcontratista: la persona física o jurídica que asume contractualmente ante el contratista u otro subcontratista comitente el compromiso de realizar determinadas partes o unidades de obra, con sujeción al proyecto por el que se rige su ejecución. Las variantes de esta figura pueden ser las del primer subcontratista (subcontratista cuyo comitente es el contratista), segundo subcontratista (subcontratista cuyo comitente es el primer subcontratista), y así sucesivamente.

[3] RD 1627/1997, Artículo 3 (score 0.756)
RD 1627/1997, Artículo 3
Artículo 3. Designación de los coordinadores en materia de seguridad y salud.
1. En las obras incluidas en el ámbito de aplicación del presente Real Decreto, cuando en la elaboración del proyecto de obra intervengan varios proyectistas, el promotor designará un coordinador en materia de seguridad y de salud durante la elaboración del proyecto de obra.
2. Cuando en la ejecución de la obra intervenga más de una empresa, o una empresa y trabajadores autónomos o diversos trabajadores autónomos, el promotor, antes del inicio de los trabajos o tan pronto como se constate dicha circunstancia, designará un coordinador en materia de seguridad y salud durante la ejecución de la obra.
3. La designación de los coordinadores en materia de seguridad y salud durante la elaboración del proyecto de obra y durante la ejecución de la obra podrá recaer en la misma persona.
4. La designación de los coordinadores no eximirá al promotor de sus responsabilidades.

[4] RD 1627/1997, Artículo 4 (score 0.754)
RD 1627/1997, Artículo 4
Artículo 4. Obligatoriedad del estudio de seguridad y salud o del estudio básico de seguridad y salud en las obras.
1. El promotor estará obligado a que en la fase de redacción del proyecto se elabore un estudio de seguridad y salud en los proyectos de obras en que se den alguno de los supuestos siguientes:
a) Que el presupuesto de ejecución por contrata incluido en el proyecto sea igual o superior a 75 millones de pesetas.
b) Que la duración estimada sea superior a 30 días laborables, empleándose en algún momento a más de 20 trabajadores simultáneamente.
c) Que el volumen de mano de obra estimada, entendiendo por tal la suma de los días de trabajo del total de los trabajadores en la obra, sea superior a 500.
d) Las obras de túneles, galerías, conducciones subterráneas y presas.
2. En los proyectos de obras no incluidos en ninguno de los supuestos previstos en el apartado anterior, el promotor estará obligado a que en la fase de redacción del proyecto se elabore un estudio básico de seguridad y salud.

[5] RD 1627/1997, Artículo 2 (score 0.749)
RD 1627/1997, Artículo 2
Artículo 2. Definiciones.
1. A efectos del presente Real Decreto, se entenderá por:
a) Obra de construcción u obra: cualquier obra, pública o privada, en la que se efectúen trabajos de construcción o ingeniería civil cuya relación no exhaustiva figura en el anexo I.
b) Trabajos con riesgos especiales: trabajos cuya realización exponga a los trabajadores a riesgos de especial gravedad para su seguridad y salud, comprendidos los indicados en la relación no exhaustiva que figura en el anexo II.
c) Promotor: cualquier persona física o jurídica por cuenta de la cual se realice una obra.
d) Proyectista: el autor o autores, por encargo del promotor, de la totalidad o parte del proyecto de obra.
e) Coordinador en materia de seguridad y de salud durante la elaboración del proyecto de obra: el técnico competente designado por el promotor para coordinar, durante la fase del proyecto de obra, la aplicación de los principios que se mencionan en el artículo 8.
f) Coordinador en materia de seguridad y de salud durante la ejecución de la obra: el técnico competente integrado en la dirección facultativa, designado por el promotor para llevar a cabo las tareas que se mencionan en el artículo 9.
g) Dirección facultativa: el técnico o técnicos competentes designados por el promotor, encargados de la dirección y del control de la ejecución de la obra.
h) Contratista: la persona física o jurídica que asume contractualmente ante el promotor, con medios humanos y materiales, propios o ajenos, el compromiso de ejecutar la totalidad o parte de las obras con sujeción al proyecto y al contrato.
i) Subcontratista: la persona física o jurídica que asume contractualmente ante el contratista, empresario principal, el compromiso de realizar determinadas partes o instalaciones de la obra, con sujeción al proyecto por el que se rige su ejecución.

---
## q06 (single, dev)
**Question:** ¿A partir de qué presupuesto de ejecución por contrata es obligatorio elaborar un estudio de seguridad y salud?
**Reference:** Cuando el presupuesto de ejecución por contrata sea igual o superior a 75 millones de pesetas (además de otros supuestos de duración y mano de obra).
**Answer:**

El promotor está obligado a que se elabore un estudio de seguridad y salud cuando el presupuesto de ejecución por contrata incluido en el proyecto sea **igual o superior a 75 millones de pesetas** (RD 1627/1997, Artículo 4). 

*(Nota: Los pasajes del corpus recogen la cifra original de la norma, sin que conste una actualización a euros en el texto consultado).*

Fuentes utilizadas:
- RD 1627/1997, Artículo 4.

**Citations:** RD 1627/1997, Artículo 4 — all in retrieved text

**Coverage check:**

- Search 1 «estudio de seguridad y salud presupuesto ejecucion por contrata obligatorio»: **PARCIAL**, passage [1], quote: «a) Que el presupuesto de ejecución por contrata incluido en el proyecto sea igual o superior a 75 millones de pesetas.». Need: a partir de qué presupuesto de ejecución por contrata incluido en el proyecto es obligatorio elaborar un estudio de seguridad y salud

**Retrieved passages:**

[1] RD 1627/1997, Artículo 4 (score 0.755)
RD 1627/1997, Artículo 4
Artículo 4. Obligatoriedad del estudio de seguridad y salud o del estudio básico de seguridad y salud en las obras.
1. El promotor estará obligado a que en la fase de redacción del proyecto se elabore un estudio de seguridad y salud en los proyectos de obras en que se den alguno de los supuestos siguientes:
a) Que el presupuesto de ejecución por contrata incluido en el proyecto sea igual o superior a 75 millones de pesetas.
b) Que la duración estimada sea superior a 30 días laborables, empleándose en algún momento a más de 20 trabajadores simultáneamente.
c) Que el volumen de mano de obra estimada, entendiendo por tal la suma de los días de trabajo del total de los trabajadores en la obra, sea superior a 500.
d) Las obras de túneles, galerías, conducciones subterráneas y presas.
2. En los proyectos de obras no incluidos en ninguno de los supuestos previstos en el apartado anterior, el promotor estará obligado a que en la fase de redacción del proyecto se elabore un estudio básico de seguridad y salud.

[2] RD 1627/1997, Artículo 5 (score 0.734)
RD 1627/1997, Artículo 5
e) Presupuesto que cuantifique el conjunto de gastos previstos para la aplicación y ejecución del estudio de seguridad y salud.
3. Dicho estudio deberá formar parte del proyecto de ejecución de obra o, en su caso, del proyecto de obra, ser coherente con el contenido del mismo y recoger las medidas preventivas adecuadas a los riesgos que conlleve la realización de la obra.
4. El presupuesto para la aplicación y ejecución del estudio de seguridad y salud deberá cuantificar el conjunto de gastos previstos, tanto por lo que se refiere a la suma total como a la valoración unitaria de elementos, con referencia al cuadro de precios sobre el que se calcula. Sólo podrán figurar partidas alzadas en los casos de elementos u operaciones de difícil previsión.
Las mediciones, calidades y valoración recogidas en el presupuesto del estudio de seguridad y salud podrán ser modificadas o sustituidas por alternativas propuestas por el contratista en el plan de seguridad y salud a que se refiere el artículo 7, previa justificación técnica debidamente motivada, siempre que ello no suponga disminución del importe total, ni de los niveles de protección contenidos en el estudio. A estos efectos, el presupuesto del estudio de seguridad y salud deberá ir incorporado al presupuesto general de la obra como un capítulo más del mismo.
No se incluirán en el presupuesto del estudio de seguridad y salud los costes exigidos por la correcta ejecución profesional de los trabajos, conforme a las normas reglamentarias en vigor y los criterios técnicos generalmente admitidos, emanados de organismos especializados.
5. El estudio de seguridad y salud a que se refieren los apartados anteriores deberá tener en cuenta, en su caso, cualquier tipo de actividad que se lleve a cabo en la obra, debiendo estar localizadas e identificadas las zonas en las que se presten trabajos incluidos en uno o varios de los apartados del anexo II, así como sus correspondientes medidas específicas.

[3] RD 1627/1997, Artículo 5 (score 0.726)
RD 1627/1997, Artículo 5
Artículo 5. Estudio de seguridad y salud.
El estudio de seguridad y salud a que se refiere el apartado 1 del artículo 4 será elaborado por el técnico competente designado por el promotor. Cuando deba existir un coordinador en materia de seguridad y salud durante la elaboración del proyecto de obra, le corresponderá a éste elaborar o hacer que se elabore, bajo su responsabilidad, dicho estudio.
2. El estudio contendrá, como mínimo, los siguientes documentos:
a) Memoria descriptiva de los procedimientos, equipos técnicos y medios auxiliares que hayan de utilizarse o cuya utilización pueda preverse; identificación de los riesgos laborales que puedan ser evitados, indicando a tal efecto las medidas técnicas necesarias para ello; relación de los riesgos laborales que no puedan eliminarse conforme a lo señalado anteriormente, especificando las medidas preventivas y protecciones técnicas tendentes a controlar y reducir dichos riesgos y valorando su eficacia, en especial cuando se propongan medidas alternativas.
Asimismo, se incluirá la descripción de los servicios sanitarios y comunes de que deberá estar dotado el centro de trabajo de la obra, en función del número de trabajadores que vayan a utilizarlos.
En la elaboración de la memoria habrán de tenerse en cuenta las condiciones del entorno en que se realice la obra, así como la tipología y características de los materiales y elementos que hayan de utilizarse, determinación del proceso constructivo y orden de ejecución de los trabajos.
b) Pliego de condiciones particulares en el que se tendrán en cuenta las normas legales y reglamentarias aplicables a las especificaciones técnicas propias de la obra de que se trate, así como las prescripciones que se habrán de cumplir en relación con las características, la utilización y la conservación de las máquinas, útiles, herramientas, sistemas y equipos preventivos.
c) Planos en los que se desarrollarán los gráficos y esquemas necesarios para la mejor definición y comprensión de las medidas preventivas definidas en la memoria, con expresión de las especificaciones técnicas necesarias.
d) Mediciones de todas aquellas unidades o elementos de seguridad y salud en el trabajo que hayan sido definidos o proyectados.

[4] RD 1627/1997, Artículo 17 (score 0.724)
RD 1627/1997, Artículo 17
Artículo 17. Visado de proyectos.
1. La inclusión en el proyecto de ejecución de obra del estudio de seguridad y salud o, en su caso, del estudio básico será requisito necesario para el visado de aquél por el Colegio profesional correspondiente, expedición de la licencia municipal y demás autorizaciones y trámites por parte de las distintas Administraciones públicas.
2. En la tramitación para la aprobación de los proyectos de obras de las Administraciones públicas se hará declaración expresa por la Oficina de Supervisión de Proyectos u órgano equivalente sobre la inclusión del correspondiente estudio de seguridad y salud o, en su caso, del estudio básico.

[5] RD 1627/1997, Artículo 6 (score 0.724)
RD 1627/1997, Artículo 6
Artículo 6. Estudio básico de seguridad y salud.
1. El estudio básico de seguridad y salud a que se refiere el apartado 2 del artículo 4 será elaborado por el técnico competente designado por el promotor. Cuando deba existir un coordinador en materia de seguridad y salud durante la elaboración del proyecto de obra, le corresponderá a éste elaborar o hacer que se elabore, bajo su responsabilidad, dicho estudio.
2. El estudio básico deberá precisar las normas de seguridad y salud aplicables a la obra. A tal efecto, deberá contemplar la identificación de los riesgos laborales que puedan ser evitados, indicando las medidas técnicas necesarias para ello; relación de los riesgos laborales que no puedan eliminarse conforme a lo señalado anteriormente, especificando las medidas preventivas y protecciones técnicas tendentes a controlar y reducir dichos riesgos y valorando su eficacia, en especial cuando se propongan medidas alternativas. En su caso, tendrá en cuenta cualquier otro tipo de actividad que se lleve a cabo en la misma, y contendrá medidas específicas relativas a los trabajos incluidos en uno o varios de los apartados del anexo II.
3. En el estudio básico se contemplarán también las previsiones y las informaciones útiles para efectuar en su día, en las debidas condiciones de seguridad y salud, los previsibles trabajos posteriores.

---
## q07 (single, dev)
**Question:** ¿Cuándo está obligada una empresa a constituir un servicio de prevención propio por su número de trabajadores?
**Reference:** Cuando tenga más de 500 trabajadores; entre 250 y 500 si desarrolla actividades del anexo I; o si lo decide la autoridad laboral.
**Answer:**

El empresario está obligado a constituir un servicio de prevención propio cuando concurra alguno de los siguientes supuestos según su número de trabajadores y actividad:

1. Empresas que cuenten con **más de 500 trabajadores** (RD 39/1997, Artículo 14.a).
2. Empresas de **entre 250 y 500 trabajadores**, siempre que desarrollen alguna de las actividades incluidas en el anexo I (RD 39/1997, Artículo 14.b).
3. Empresas no incluidas en los supuestos anteriores cuando así lo decida la **autoridad laboral**, previo informe de la Inspección de Trabajo y Seguridad Social y de los órganos técnicos de las Comunidades Autónomas, en función de la peligrosidad de la actividad o de la siniestralidad (RD 39/1997, Artículo 14.c).

*Fuentes utilizadas:* RD 39/1997, Artículo 14. 
*Nota: Esta información es meramente divulgativa y no constituye asesoramiento legal.*

**Citations:** RD 39/1997, Artículo 14 — all in retrieved text

**Coverage check:**

- Search 1 «servicio de prevención propio número de trabajadores obligación»: **SÍ**, passage [1], quote: «El empresario deberá constituir un servicio de prevención propio cuando concurra alguno de los siguientes supuestos:». Need: el número de trabajadores y las condiciones a partir de los cuales una empresa está obligada a constituir un servicio de prevención propio

**Retrieved passages:**

[1] RD 39/1997, Artículo 14 (score 0.776)
RD 39/1997, Artículo 14
Artículo 14. Servicio de prevención propio.
El empresario deberá constituir un servicio de prevención propio cuando concurra alguno de los siguientes supuestos:
a) Que se trate de empresas que cuenten con más de 500 trabajadores.
b) Que, tratándose de empresas de entre 250 y 500 trabajadores, desarrollen alguna de las actividades incluidas en el anexo I.
c) Que, tratándose de empresas no incluidas en los apartados anteriores, así lo decida la autoridad laboral, previo informe de la Inspección de Trabajo y Seguridad Social y, en su caso, de los órganos técnicos en materia preventiva de las Comunidades Autónomas, en función de la peligrosidad de la actividad desarrollada o de la frecuencia o gravedad de la siniestralidad en la empresa, salvo que se opte por el concierto con una entidad especializada ajena a la empresa de conformidad con lo dispuesto en el artículo 16 de esta disposición.
Teniendo en cuenta las circunstancias existentes, la resolución de la autoridad laboral fijará un plazo, no superior a un año, para que, en el caso de que se optase por un servicio de prevención propio, la empresa lo constituya en dicho plazo. Hasta la fecha señalada en la resolución, las actividades preventivas en la empresa deberán ser concertadas con una entidad especializada ajena a la empresa, salvo de aquellas que vayan siendo asumidas progresivamente por la empresa mediante la designación de trabajadores, hasta su plena integración en el servicio de prevención que se constituya.

[2] Ley 31/1995, Artículo 31 (score 0.759)
Ley 31/1995, Artículo 31
Artículo 31. Servicios de prevención.
1. Si la designación de uno o varios trabajadores fuera insuficiente para la realización de las actividades de prevención, en función del tamaño de la empresa, de los riesgos a que están expuestos los trabajadores o de la peligrosidad de las actividades desarrolladas, con el alcance que se establezca en las disposiciones a que se refiere la letra e) del apartado 1 del artículo 6 de la presente Ley, el empresario deberá recurrir a uno o varios servicios de prevención propios o ajenos a la empresa, que colaborarán cuando sea necesario.
Para el establecimiento de estos servicios en las Administraciones públicas se tendrá en cuenta su estructura organizativa y la existencia, en su caso, de ámbitos sectoriales y descentralizados.
2. Se entenderá como servicio de prevención el conjunto de medios humanos y materiales necesarios para realizar las actividades preventivas a fin de garantizar la adecuada protección de la seguridad y la salud de los trabajadores, asesorando y asistiendo para ello al empresario, a los trabajadores y a sus representantes y a los órganos de representación especializados. Para el ejercicio de sus funciones, el empresario deberá facilitar a dicho servicio el acceso a la información y documentación a que se refiere el apartado 3 del artículo anterior.
3. Los servicios de prevención deberán estar en condiciones de proporcionar a la empresa el asesoramiento y apoyo que precise en función de los tipos de riesgo en ella existentes y en lo referente a:
a) El diseño, implantación y aplicación de un plan de prevención de riesgos laborales que permita la integración de la prevención en la empresa.
b) La evaluación de los factores de riesgo que puedan afectar a la seguridad y la salud de los trabajadores en los términos previstos en el artículo 16 de esta Ley.
c) La planificación de la actividad preventiva y la determinación de las prioridades en la adopción de las medidas preventivas y la vigilancia de su eficacia.
d) La información y formación de los trabajadores, en los términos previstos en los artículos 18 y 19 de esta Ley.

[3] Ley 31/1995, Artículo 30 (score 0.757)
Ley 31/1995, Artículo 30
5. En las empresas de hasta diez trabajadores, el empresario podrá asumir personalmente las funciones señaladas en el apartado 1, siempre que desarrolle de forma habitual su actividad en el centro de trabajo y tenga la capacidad necesaria, en función de los riesgos a que estén expuestos los trabajadores y la peligrosidad de las actividades, con el alcance que se determine en las disposiciones a que se refiere el artículo 6.1.e) de esta Ley. La misma posibilidad se reconoce al empresario que, cumpliendo tales requisitos, ocupe hasta 25 trabajadores, siempre y cuando la empresa disponga de un único centro de trabajo.
6. El empresario que no hubiere concertado el Servicio de prevención con una entidad especializada ajena a la empresa deberá someter su sistema de prevención al control de una auditoría o evaluación externa, en los términos que reglamentariamente se determinen.
7. Las personas o entidades especializadas que pretendan desarrollar la actividad de auditoría del sistema de prevención habrán de contar con una única autorización de la autoridad laboral, que tendrá validez en todo el territorio español. El vencimiento del plazo máximo del procedimiento de autorización sin haberse notificado resolución expresa al interesado permitirá entender desestimada la solicitud por silencio administrativo, con el objeto de garantizar una adecuada protección de los trabajadores.

[4] Ley 31/1995, Artículo 35 (score 0.751)
Ley 31/1995, Artículo 35
Artículo 35. Delegados de Prevención.
1. Los Delegados de Prevención son los representantes de los trabajadores con funciones específicas en materia de prevención de riesgos en el trabajo.
2. Los Delegados de Prevención serán designados por y entre los representantes del personal, en el ámbito de los órganos de representación previstos en las normas a que se refiere el artículo anterior, con arreglo a la siguiente escala:
De 50 a 100 trabajadores: 2 Delegados de Prevención.
De 101 a 500 trabajadores: 3 Delegados de Prevención.
De 501 a 1.000 trabajadores: 4 Delegados de Prevención.
De 1.001 a 2.000 trabajadores: 5 Delegados de Prevención.
De 2.001 a 3.000 trabajadores: 6 Delegados de Prevención.
De 3.001 a 4.000 trabajadores: 7 Delegados de Prevención.
De 4.001 en adelante: 8 Delegados de Prevención.
En las empresas de hasta treinta trabajadores el Delegado de Prevención será el Delegado de Personal. En las empresas de treinta y uno a cuarenta y nueve trabajadores habrá un Delegado de Prevención que será elegido por y entre los Delegados de Personal.
3. A efectos de determinar el número de Delegados de Prevención se tendrán en cuenta los siguientes criterios:
a) Los trabajadores vinculados por contratos de duración determinada superior a un año se computarán como trabajadores fijos de plantilla.
b) Los contratados por término de hasta un año se computarán según el número de días trabajados en el período de un año anterior a la designación. Cada doscientos días trabajados o fracción se computarán como un trabajador más.
4. No obstante lo dispuesto en el presente artículo, en los convenios colectivos podrán establecerse otros sistemas de designación de los Delegados de Prevención, siempre que se garantice que la facultad de designación corresponde a los representantes del personal o a los propios trabajadores.

[5] RD 39/1997, Artículo 16 (score 0.749)
RD 39/1997, Artículo 16
Artículo 16. Servicios de prevención ajenos.
1. El empresario deberá recurrir a uno o varios servicios de prevención ajenos, que colaborarán entre sí cuando sea necesario, cuando concurra alguna de las siguientes circunstancias:
a) Que la designación de uno o varios trabajadores sea insuficiente para la realización de la actividad de prevención y no concurran las circunstancias que determinan la obligación de constituir un servicio de prevención propio.
b) Que en el supuesto a que se refiere el párrafo c) del artículo 14 no se haya optado por la constitución de un servicio de prevención propio.
c) Que se haya producido una asunción parcial de la actividad preventiva en los términos previstos en el apartado 2 del artículo 11 y en el apartado 4 del artículo 15 de la presente disposición.
2. De conformidad con lo dispuesto en el artículo 33.1 de la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales, los representantes de los trabajadores deberán ser consultados por el empresario con carácter previo a la adopción de la decisión de concertar la actividad preventiva con uno o varios servicios de prevención ajenos.
Por otra parte, de conformidad con lo dispuesto en el artículo 39.1.a) de la indicada Ley, los criterios a tener en cuenta para la selección de la entidad con la que se vaya a concertar dicho servicio, así como las características técnicas del concierto, se debatirán, y en su caso se acordarán, en el seno del Comité de Seguridad y Salud de la empresa.

---
## q08 (single, dev)
**Question:** ¿Es obligatoria para el trabajador la vigilancia periódica de su salud?
**Reference:** En general es voluntaria y requiere su consentimiento, salvo excepciones previo informe de los representantes de los trabajadores (por ejemplo si es imprescindible para evaluar los efectos de las condiciones de trabajo o si el estado de salud puede ser un peligro para él o para otros).
**Answer:**

Por regla general, la vigilancia periódica de la salud tiene carácter **voluntario** para el trabajador y solo podrá llevarse a cabo cuando este preste su consentimiento (Ley 31/1995, Artículo 22).

No obstante, **de carácter voluntario solo se exceptuarán** (es decir, serán obligatorios), previo informe de los representantes de los trabajadores, los siguientes supuestos:
1. Cuando la realización de los reconocimientos sea imprescindible para **evaluar los efectos de las condiciones de trabajo sobre la salud** de los trabajadores.
2. Para verificar si el estado de salud del trabajador puede constituir un **peligro para el mismo, para los demás trabajadores o para otras personas** relacionadas con la empresa.
3. Cuando así esté establecido en una **disposición legal** en relación con la protección de riesgos específicos y actividades de especial peligrosidad.

En todo caso, se deberá optar por las pruebas que causen las menores molestias y que sean proporcionales al riesgo, respetando el derecho a la intimidad, a la dignidad y a la confidencialidad (Ley 31/1995, Artículo 22).

Fuentes utilizadas:
- Ley 31/1995 (Ley de Prevención de Riesgos Laborales), Artículo 22.

*Nota: Esta información es divulgativa y no constituye asesoramiento jurídico.*

**Citations:** Ley 31/1995, Artículo 22 — all in retrieved text

**Coverage check:**

- Search 1 «vigilancia periodica salud obligatoria trabajador»: **SÍ**, passage [1], quote: «De este carácter voluntario sólo se exceptuarán, previo informe de los representantes de los trabajadores, los supuestos en los que la realización de los reconocimientos sea imprescindible para evaluar los efectos de las condiciones de trabajo sobre la salud de los trabajadores o para verificar si el estado de salud del trabajador puede constituir un peligro para el mismo, para los demás trabajadores o para otras personas relacionadas con la empresa o cuando así esté establecido en una disposición legal en relación con la protección de riesgos específicos y actividades de especial peligrosidad.». Need: si la vigilancia periódica de la salud es obligatoria para el trabajador

**Retrieved passages:**

[1] Ley 31/1995, Artículo 22 (score 0.77)
Ley 31/1995, Artículo 22
Artículo 22. Vigilancia de la salud.
1. El empresario garantizará a los trabajadores a su servicio la vigilancia periódica de su estado de salud en función de los riesgos inherentes al trabajo.
Esta vigilancia sólo podrá llevarse a cabo cuando el trabajador preste su consentimiento. De este carácter voluntario sólo se exceptuarán, previo informe de los representantes de los trabajadores, los supuestos en los que la realización de los reconocimientos sea imprescindible para evaluar los efectos de las condiciones de trabajo sobre la salud de los trabajadores o para verificar si el estado de salud del trabajador puede constituir un peligro para el mismo, para los demás trabajadores o para otras personas relacionadas con la empresa o cuando así esté establecido en una disposición legal en relación con la protección de riesgos específicos y actividades de especial peligrosidad.
En todo caso se deberá optar por la realización de aquellos reconocimientos o pruebas que causen las menores molestias al trabajador y que sean proporcionales al riesgo.
2. Las medidas de vigilancia y control de la salud de los trabajadores se llevarán a cabo respetando siempre el derecho a la intimidad y a la dignidad de la persona del trabajador y la confidencialidad de toda la información relacionada con su estado de salud.
3. Los resultados de la vigilancia a que se refiere el apartado anterior serán comunicados a los trabajadores afectados.
4. Los datos relativos a la vigilancia de la salud de los trabajadores no podrán ser usados con fines discriminatorios ni en perjuicio del trabajador.
El acceso a la información médica de carácter personal se limitará al personal médico y a las autoridades sanitarias que lleven a cabo la vigilancia de la salud de los trabajadores, sin que pueda facilitarse al empresario o a otras personas sin consentimiento expreso del trabajador.

[2] Ley 31/1995, Artículo 22 (score 0.748)
Ley 31/1995, Artículo 22
No obstante lo anterior, el empresario y las personas u órganos con responsabilidades en materia de prevención serán informados de las conclusiones que se deriven de los reconocimientos efectuados en relación con la aptitud del trabajador para el desempeño del puesto de trabajo o con la necesidad de introducir o mejorar las medidas de protección y prevención, a fin de que puedan desarrollar correctamente sus funciones en materia preventiva.
5. En los supuestos en que la naturaleza de los riesgos inherentes al trabajo lo haga necesario, el derecho de los trabajadores a la vigilancia periódica de su estado de salud deberá ser prolongado más allá de la finalización de la relación laboral, en los términos que reglamentariamente se determinen.
6. Las medidas de vigilancia y control de la salud de los trabajadores se llevarán a cabo por personal sanitario con competencia técnica, formación y capacidad acreditada.

[3] RD 39/1997, Artículo 37 (score 0.729)
RD 39/1997, Artículo 37
b) En materia de vigilancia de la salud, la actividad sanitaria deberá abarcar, en las condiciones fijadas por el artículo 22 de la Ley 31/1995, de Prevención de Riesgos Laborales:
1.º Una evaluación de la salud de los trabajadores inicial después de la incorporación al trabajo o después de la asignación de tareas específicas con nuevos riesgos para la salud.
2.º Una evaluación de la salud de los trabajadores que reanuden el trabajo tras una ausencia prolongada por motivos de salud, con la finalidad de descubrir sus eventuales orígenes profesionales y recomendar una acción apropiada para proteger a los trabajadores.
3.º Una vigilancia de la salud a intervalos periódicos.
c) La vigilancia de la salud estará sometida a protocolos específicos u otros medios existentes con respecto a los factores de riesgo a los que esté expuesto el trabajador. El Ministerio de Sanidad y Consumo y las Comunidades Autónomas, oídas las sociedades científicas competentes, y de acuerdo con lo establecido en la Ley General de Sanidad en materia de participación de los agentes sociales, establecerán la periodicidad y contenidos específicos de cada caso.
Los exámenes de salud incluirán, en todo caso, una historia clínico-laboral, en la que además de los datos de anamnesis, exploración clínica y control biológico y estudios complementarios en función de los riesgos inherentes al trabajo, se hará constar una descripción detallada del puesto de trabajo, el tiempo de permanencia en el mismo, los riesgos detectados en el análisis de las condiciones de trabajo, y las medidas de prevención adoptadas.
Deberá constar igualmente, en caso de disponerse de ello, una descripción de los anteriores puestos de trabajo, riesgos presentes en los mismos, y tiempo de permanencia para cada uno de ellos.
d) El personal sanitario del servicio de prevención deberá conocer las enfermedades que se produzcan entre los trabajadores y las ausencias del trabajo por motivos de salud, a los solos efectos de poder identificar cualquier relación entre la causa de enfermedad o de ausencia y los riesgos para la salud que puedan presentarse en los lugares de trabajo.

[4] RD 39/1997, Artículo 37 (score 0.724)
RD 39/1997, Artículo 37
e) En los supuestos en que la naturaleza de los riesgos inherentes al trabajo lo haga necesario, el derecho de los trabajadores a la vigilancia periódica de su estado de salud deberá ser prolongado más allá de la finalización de la relación laboral a través del Sistema Nacional de Salud.
f) El personal sanitario del servicio deberá analizar los resultados de la vigilancia de la salud de los trabajadores y de la evaluación de los riesgos, con criterios epidemiológicos y colaborará con el resto de los componentes del servicio, a fin de investigar y analizar las posibles relaciones entre la exposición a los riesgos profesionales y los perjuicios para la salud y proponer medidas encaminadas a mejorar las condiciones y medio ambiente de trabajo.
g) El personal sanitario del servicio de prevención estudiará y valorará, especialmente, los riesgos que puedan afectar a las trabajadoras en situación de embarazo o parto reciente, a los menores y a los trabajadores especialmente sensibles a determinados riesgos, y propondrá las medidas preventivas adecuadas.
h) El personal sanitario del servicio de prevención que, en su caso, exista en el centro de trabajo deberá proporcionar los primeros auxilios y la atención de urgencia a los trabajadores víctimas de accidentes o alteraciones en el lugar de trabajo.

[5] RD 39/1997, Anexo I (score 0.699)
RD 39/1997, Anexo I
ANEXO I
a) Trabajos con exposición a radiaciones ionizantes en zonas controladas según Real Decreto 53/1992, de 24 de enero, sobre protección sanitaria contra radiaciones ionizantes.
b) Trabajos con exposición a sustancias o mezclas causantes de toxicidad aguda de categoría 1, 2 y 3, y en particular a agentes cancerígenos, mutagénicos o tóxicos para la reproducción, de categoría 1A y 1B, según el Reglamento (CE) n.º 1272/2008, de 16 de diciembre de 2008, sobre clasificación, etiquetado y envasado de sustancias y mezclas.
c) Actividades en que intervienen productos químicos de alto riesgo y son objeto de la aplicación del Real Decreto 886/1988, de 15 de julio, y sus modificaciones, sobre prevención de accidentes mayores en determinadas actividades industriales.
d) Trabajos con exposición a agentes biológicos de los grupos 3 y 4, según la Directiva 90/679/CEE y sus modificaciones, sobre protección de los trabajadores contra los riesgos relacionados a agentes biológicos durante el trabajo.
e) Actividades de fabricación, manipulación y utilización de explosivos, incluidos los artículos pirotécnicos y otros objetos o instrumentos que contengan explosivos.
f) Trabajos propios de minería a cielo abierto y de interior, y sondeos en superficie terrestre o en plataformas marinas.
g) Actividades en inmersión bajo el agua.
h) Actividades en obras de construcción, excavación, movimientos de tierras y túneles, con riesgo de caída de altura o sepultamiento.
i) Actividades en la industria siderúrgica y en la construcción naval.
j) Producción de gases comprimidos, licuados o disueltos o utilización significativa de los mismos.
k) Trabajos que produzcan concentraciones elevadas de polvo silíceo.
l) Trabajos con riesgos eléctricos en alta tensión.

---
## q09 (single, dev)
**Question:** ¿Qué documento debe tener cada contratista en la obra para reflejar las subcontrataciones realizadas?
**Reference:** El Libro de Subcontratación, que debe permanecer en todo momento en la obra.
**Answer:**

Cada contratista debe disponer en la obra de un **Libro de Subcontratación**.

En dicho libro, que debe permanecer en todo momento en la obra y reflejar los datos por orden cronológico desde el comienzo de los trabajos, se deben consignar:
- Todas y cada una de las subcontrataciones realizadas con empresas subcontratistas y trabajadores autónomos.
- El nivel de subcontratación y la empresa comitente.
- El objeto del contrato.
- La identificación de la persona que ejerce las facultades de organización y dirección de cada subcontratista y, en su caso, de los representantes legales de los trabajadores de la misma.
- Las respectivas fechas de entrega de la parte del plan de seguridad y salud que afecte a cada subcontratista y trabajador autónomo.
- Las instrucciones elaboradas por el coordinador de seguridad y salud para marcar la dinámica y desarrollo del procedimiento de coordinación.
- Las anotaciones efectuadas por la dirección facultativa sobre su aprobación de cada subcontratación excepcional.

*(Nota: Esta información es meramente informativa y no constituye asesoramiento jurídico).*

**Fuentes:**
- Ley 32/2006, Artículo 8 y Anexo.

**Citations:** Ley 32/2006, Artículo 8 — all in retrieved text

**Coverage check:**

- Search 1 «libro de subcontratación contratista obra»: **SÍ**, passage [2], quote: «1. En toda obra de construcción, incluida en el ámbito de aplicación de esta Ley, cada contratista deberá disponer de un Libro de Subcontratación.». Need: qué documento debe tener cada contratista en la obra para reflejar las subcontrataciones realizadas

**Retrieved passages:**

[1] Ley 32/2006, Anexo (score 0.771)
Ley 32/2006, Anexo
ANEXO
A) DATOS IDENTIFICATIVOS DE LA OBRA
Promotor
NIF
Contratista
NIF
Dirección Facultativa
NIF
Coordinador de seg. y salud en fase de ejecución
NIF
Domicilio de la obra
Localidad
B) REGISTRO DE SUBCONTRATACIONES
N.º orden
Empresa subcontratista o trabajador autónomo/NIF
Nivel de subcontratación
N.º orden del comitente (1)
Fecha comienzo trabajos
Objeto del contrato
Responsable de dirección trabajos/Representantes de los trabajadores
Fecha entrega plan de seg. y salud
Referencia de instrucciones del coordinador (2)
Firma del subcontratista o trabajador autónomo
Aprobación de la Dirección Facultativa (3)
(1) En esta columna se anotará el N.º de orden correspondiente al asiento de la empresa que ha subcontratado los trabajos a la subcontratista de este asiento, dejándose en blanco en caso de que la comitente sea la empresa contratista.
(2) En esta columna se hará constar, en su caso, la referencia de las hojas del Libro de incidencias al plan de seguridad y salud del contratista en las que el Coordinador de seguridad y salud en fase de ejecución haya efectuado anotaciones sobre las instrucciones sobre el desarrollo del procedimiento de coordinación establecido.
(3) Cuando proceda, se hará constar en esta columna la aprobación de la subcontratación a que se refiere el asiento por parte de la Dirección Facultativa, mediante la firma del mismo en esta casilla y la indicación de su fecha.

[2] Ley 32/2006, Artículo 8 (score 0.768)
Ley 32/2006, Artículo 8
Artículo 8. Documentación de la subcontratación.
1. En toda obra de construcción, incluida en el ámbito de aplicación de esta Ley, cada contratista deberá disponer de un Libro de Subcontratación.
En dicho libro, que deberá permanecer en todo momento en la obra, se deberán reflejar, por orden cronológico desde el comienzo de los trabajos, todas y cada una de las subcontrataciones realizadas en una determinada obra con empresas subcontratistas y trabajadores autónomos, su nivel de subcontratación y empresa comitente, el objeto de su contrato, la identificación de la persona que ejerce las facultades de organización y dirección de cada subcontratista y, en su caso, de los representantes legales de los trabajadores de la misma, las respectivas fechas de entrega de la parte del plan de seguridad y salud que afecte a cada empresa subcontratista y trabajador autónomo, así como las instrucciones elaboradas por el coordinador de seguridad y salud para marcar la dinámica y desarrollo del procedimiento de coordinación establecido, y las anotaciones efectuadas por la dirección facultativa sobre su aprobación de cada subcontratación excepcional de las previstas en el artículo 5.3 de esta Ley.
Al Libro de Subcontratación tendrán acceso el promotor, la dirección facultativa, el coordinador de seguridad y salud en fase de ejecución de la obra, las empresas y trabajadores autónomos intervinientes en la obra, los técnicos de prevención, los delegados de prevención, la autoridad laboral y los representantes de los trabajadores de las diferentes empresas que intervengan en la ejecución de la obra.
2. Asimismo, cada empresa deberá disponer de la documentación o título que acredite la posesión de la maquinaria que utiliza, y de cuanta documentación sea exigida por las disposiciones legales vigentes.
3. Reglamentariamente se determinarán las condiciones del Libro de Subcontratación al que se refiere el apartado 1, en cuanto a su régimen de habilitación, por la autoridad laboral autonómica competente, así como el contenido y obligaciones y derechos derivados del mismo, al tiempo que se procederá a una revisión de las distintas obligaciones documentales aplicables a las obras de construcción con objeto de lograr su unificación y simplificación.

[3] Ley 32/2006, Artículo 5 (score 0.74)
Ley 32/2006, Artículo 5
Artículo 5. Régimen de la subcontratación.
1. La subcontratación, como forma de organización productiva, no podrá ser limitada, salvo en las condiciones y en los supuestos previstos en esta Ley.
2. Con carácter general, el régimen de la subcontratación en el sector de la construcción será el siguiente:
a) El promotor podrá contratar directamente con cuantos contratistas estime oportuno ya sean personas físicas o jurídicas.
b) El contratista podrá contratar con las empresas subcontratistas o trabajadores autónomos la ejecución de los trabajos que hubiera contratado con el promotor.
c) El primer y segundo subcontratistas podrán subcontratar la ejecución de los trabajos que, respectivamente, tengan contratados, salvo en los supuestos previstos en la letra f) del presente apartado.
d) El tercer subcontratista no podrá subcontratar los trabajos que hubiera contratado con otro subcontratista o trabajador autónomo.
e) El trabajador autónomo no podrá subcontratar los trabajos a él encomendados ni a otras empresas subcontratistas ni a otros trabajadores autónomos.
f) Asimismo, tampoco podrán subcontratar los subcontratistas, cuya organización productiva puesta en uso en la obra consista fundamentalmente en la aportación de mano de obra, entendiéndose por tal la que para la realización de la actividad contratada no utiliza más equipos de trabajo propios que las herramientas manuales, incluidas las motorizadas portátiles, aunque cuenten con el apoyo de otros equipos de trabajo distintos de los señalados, siempre que éstos pertenezcan a otras empresas, contratistas o subcontratistas, de la obra.
3. No obstante lo dispuesto en el apartado anterior, cuando en casos fortuitos debidamente justificados, por exigencias de especialización de los trabajos, complicaciones técnicas de la producción o circunstancias de fuerza mayor por las que puedan atravesar los agentes que intervienen en la obra, fuera necesario, a juicio de la dirección facultativa, la contratación de alguna parte de la obra con terceros, excepcionalmente se podrá extender la subcontratación establecida en el apartado anterior en un nivel adicional, siempre que se haga constar por la dirección facultativa su aprobación previa y la causa o causas motivadoras de la misma en el Libro de Subcontratación al que se refiere el artículo 7 de esta Ley.

[4] Ley 32/2006, Disposición adicional primera (score 0.731)
Ley 32/2006, Disposición adicional primera
c) Proceder a subcontratar con otro u otros subcontratistas o trabajadores autónomos superando los niveles de subcontratación permitidos legalmente, sin disponer de la expresa aprobación de la dirección facultativa, o permitir que en el ámbito de ejecución de su subcontrato otros subcontratistas o trabajadores autónomos incurran en el supuesto anterior y sin que concurran en este caso las circunstancias previstas en la letra c) del apartado 15 del artículo siguiente, salvo que proceda su calificación como infracción muy grave, de acuerdo con el mismo artículo siguiente.
28. Se consideran infracciones graves del contratista, de conformidad con lo previsto en la Ley Reguladora de la subcontratación en el sector de la construcción:
a) No llevar en orden y al día el Libro de Subcontratación exigido, o no hacerlo en los términos establecidos reglamentariamente.
b) Permitir que, en el ámbito de ejecución de su contrato, intervengan empresas subcontratistas o trabajadores autónomos superando los niveles de subcontratación permitidos legalmente, sin disponer de la expresa aprobación de la dirección facultativa, y sin que concurran las circunstancias previstas en la letra c) del apartado 15 del artículo siguiente, salvo que proceda su calificación como infracción muy grave, de acuerdo con el mismo artículo siguiente.
c) El incumplimiento del deber de acreditar, en la forma establecida legal o reglamentariamente, que dispone de recursos humanos, tanto en su nivel directivo como productivo, que cuentan con la formación necesaria en prevención de riesgos laborales, y que dispone de una organización preventiva adecuada, y la inscripción en el registro correspondiente, o del deber de verificar dicha acreditación y registro por los subcontratistas con los que contrate, y salvo que proceda su calificación como infracción muy grave, de acuerdo con el artículo siguiente.
d) La vulneración de los derechos de información de los representantes de los trabajadores sobre las contrataciones y subcontrataciones que se realicen en la obra, y de acceso al Libro de Subcontratación, en los términos establecidos en la Ley Reguladora de la subcontratación en el sector de la construcción.

[5] Ley 32/2006, Artículo 3 (score 0.729)
Ley 32/2006, Artículo 3
Artículo 3. Definiciones.
A efectos de esta Ley se entenderá por:
a) Obra de construcción u obra: cualquier obra, pública o privada, en la que se efectúen trabajos de construcción o de ingeniería civil.
b) Promotor: cualquier persona física o jurídica por cuenta de la cual se realice la obra.
c) Dirección facultativa: el técnico o técnicos competentes designados por el promotor, encargados de la dirección y del control de la ejecución de l

---
## q10 (single, dev)
**Question:** ¿Cuántos delegados de prevención corresponden a una empresa de 300 trabajadores?
**Reference:** 3 delegados de prevención (escala de 101 a 500 trabajadores).
**Answer:**

A una empresa de 300 trabajadores corresponden **3 Delegados de Prevención** (Ley 31/1995, Artículo 35).

* Fuentes utilizadas: Ley 31/1995, Artículo 35.

*Nota: Esta información es meramente informativa y no constituye asesoramiento jurídico.*

**Citations:** Ley 31/1995, Artículo 35 — all in retrieved text

**Coverage check:**

- Search 1 «delegados de prevención número de trabajadores empresa 300»: **SÍ**, passage [1], quote: «3 Delegados de Prevención.». Need: el número de delegados de prevención que corresponden a una empresa de 300 trabajadores

**Retrieved passages:**

[1] Ley 31/1995, Artículo 35 (score 0.819)
Ley 31/1995, Artículo 35
Artículo 35. Delegados de Prevención.
1. Los Delegados de Prevención son los representantes de los trabajadores con funciones específicas en materia de prevención de riesgos en el trabajo.
2. Los Delegados de Prevención serán designados por y entre los representantes del personal, en el ámbito de los órganos de representación previstos en las normas a que se refiere el artículo anterior, con arreglo a la siguiente escala:
De 50 a 100 trabajadores: 2 Delegados de Prevención.
De 101 a 500 trabajadores: 3 Delegados de Prevención.
De 501 a 1.000 trabajadores: 4 Delegados de Prevención.
De 1.001 a 2.000 trabajadores: 5 Delegados de Prevención.
De 2.001 a 3.000 trabajadores: 6 Delegados de Prevención.
De 3.001 a 4.000 trabajadores: 7 Delegados de Prevención.
De 4.001 en adelante: 8 Delegados de Prevención.
En las empresas de hasta treinta trabajadores el Delegado de Prevención será el Delegado de Personal. En las empresas de treinta y uno a cuarenta y nueve trabajadores habrá un Delegado de Prevención que será elegido por y entre los Delegados de Personal.
3. A efectos de determinar el número de Delegados de Prevención se tendrán en cuenta los siguientes criterios:
a) Los trabajadores vinculados por contratos de duración determinada superior a un año se computarán como trabajadores fijos de plantilla.
b) Los contratados por término de hasta un año se computarán según el número de días trabajados en el período de un año anterior a la designación. Cada doscientos días trabajados o fracción se computarán como un trabajador más.
4. No obstante lo dispuesto en el presente artículo, en los convenios colectivos podrán establecerse otros sistemas de designación de los Delegados de Prevención, siempre que se garantice que la facultad de designación corresponde a los representantes del personal o a los propios trabajadores.

[2] Ley 31/1995, Artículo 34 (score 0.777)
Ley 31/1995, Artículo 34
Artículo 34. Derechos de participación y representación.
1. Los trabajadores tienen derecho a participar en la empresa en las cuestiones relacionadas con la prevención de riesgos en el trabajo.
En las empresas o centros de trabajo que cuenten con seis o más trabajadores, la participación de éstos se canalizará a través de sus representantes y de la representación especializada que se regula en este capítulo.
2. A los Comités de Empresa, a los Delegados de Personal y a los representantes sindicales les corresponde, en los términos que, respectivamente, les reconocen el Estatuto de los Trabajadores, la Ley de Organos de Representación del Personal al Servicio de las Administraciones Públicas y la Ley Orgánica de Libertad Sindical, la defensa de los intereses de los trabajadores en materia de prevención de riesgos en el trabajo. Para ello, los representantes del personal ejercerán las competencias que dichas normas establecen en materia de información, consulta y negociación, vigilancia y control y ejercicio de acciones ante las empresas y los órganos y tribunales competentes.
3. El derecho de participación que se regula en este capítulo se ejercerá en el ámbito de las Administraciones públicas con las adaptaciones que procedan en atención a la diversidad de las actividades que desarrollan y las diferentes condiciones en que éstas se realizan, la complejidad y dispersión de su estructura organizativa y sus peculiaridades en materia de representación colectiva, en los términos previstos en la Ley 7/1990, de 19 de julio, sobre negociación colectiva y participación en la determinación de las condiciones de trabajo de los empleados públicos, pudiéndose establecer ámbitos sectoriales y descentralizados en función del número de efectivos y centros.
Para llevar a cabo la indicada adaptación en el ámbito de la Administración General del Estado, el Gobierno tendrá en cuenta los siguientes criterios:
a) En ningún caso dicha adaptación podrá afectar a las competencias, facultades y garantías que se reconocen en esta Ley a los Delegados de Prevención y a los Comités de Seguridad y Salud.

[3] Ley 31/1995, Disposición adicional décima (score 0.769)
Ley 31/1995, Disposición adicional décima
Disposición adicional décima. Sociedades cooperativas.
El procedimiento para la designación de los Delegados de Prevención regulados en el artículo 35 de esta Ley en las sociedades cooperativas que no cuenten con asalariados deberá estar previsto en sus Estatutos o ser objeto de acuerdo en Asamblea General.
Cuando, además de los socios que prestan su trabajo personal, existan asalariados se computarán ambos colectivos a efectos de lo dispuesto en el número 2 del artículo 35. En este caso, la designación de los Delegados de Prevención se realizará conjuntamente por los socios que prestan trabajo y los trabajadores asalariados o, en su caso, los representantes de éstos.

[4] Ley 31/1995, Artículo 36 (score 0.766)
Ley 31/1995, Artículo 36
Artículo 36. Competencias y facultades de los Delegados de Prevención.
1. Son competencias de los Delegados de Prevención:
a) Colaborar con la dirección de la empresa en la mejora de la acción preventiva.
b) Promover y fomentar la cooperación de los trabajadores en la ejecución de la normativa sobre prevención de riesgos laborales.
c) Ser consultados por el empresario, con carácter previo a su ejecución, acerca de las decisiones a que se refiere el artículo 33 de la presente Ley.
d) Ejercer una labor de vigilancia y control sobre el cumplimiento de la normativa de prevención de riesgos laborales.
En las empresas que, de acuerdo con lo dispuesto en el apartado 2 del artículo 38 de esta Ley, no cuenten con Comité de Seguridad y Salud por no alcanzar el número mínimo de trabajadores establecido al efecto, las competencias atribuidas a aquél en la presente Ley serán ejercidas por los Delegados de Prevención.
2. En el ejercicio de las competencias atribuidas a los Delegados de Prevención, éstos estarán facultados para:
a) Acompañar a los técnicos en las evaluaciones de carácter preventivo del medio ambiente de trabajo, así como, en los términos previstos en el artículo 40 de esta Ley, a los Inspectores de Trabajo y Seguridad Social en las visitas y verificaciones que realicen en los centros de trabajo para comprobar el cumplimiento de la normativa sobre prevención de riesgos laborales, pudiendo formular ante ellos las observaciones que estimen oportunas.
b) Tener acceso, con las limitaciones previstas en el apartado 4 del artículo 22 de esta Ley, a la información y documentación relativa a las condiciones de trabajo que sean necesarias para el ejercicio de sus funciones y, en particular, a la prevista en los artículos 18 y 23 de esta Ley. Cuando la información esté sujeta a las limitaciones reseñadas, sólo podrá ser suministrada de manera que se garantice el respeto de la confidencialidad.

[5] Ley 31/1995, Artículo 38 (score 0.761)
Ley 31/1995, Artículo 38
Artículo 38. Comité de Seguridad y Salud.
1. El Comité de Seguridad y Salud es el órgano paritario y colegiado de participación destinado a la consulta regular y periódica de las actuaciones de la empresa en materia de prevención de riesgos.
2. Se constituirá un Comité de Seguridad y Salud en todas las empresas o centros de trabajo que cuenten con 50 o más trabajadores.
El Comité estará formado por los Delegados de Prevención, de una parte, y por el empresario y/o sus representantes en número igual al de los Delegados de Prevención, de la otra.
En las reuniones del Comité de Seguridad y Salud participarán, con voz pero sin voto, los Delegados Sindicales y los responsables técnicos de la prevención en la empresa que no estén incluidos en la composición a la que se refiere el párrafo anterior. En las mismas condiciones podrán participar trabajadores de la empresa que cuenten con una especial cualificación o información respecto de concretas cuestiones que se debatan en este órgano y técnicos en prevención ajenos a la empresa, siempre que así lo solicite alguna de las representaciones en el Comité.
3. El Comité de Seguridad y Salud se reunirá trimestralmente y siempre que lo solicite alguna de las representaciones en el mismo. El Comité adoptará sus propias normas de funcionamiento.
Las empresas que cuenten con varios centros de trabajo dotados de Comité de Seguridad y Salud podrán acordar con sus trabajadores la creación de un Comité Intercentros, con las funciones que el acuerdo le atribuya.

---
## q11 (multi, dev)
**Question:** ¿Qué principios de la acción preventiva deben aplicar los trabajadores autónomos en una obra y dónde se enumeran?
**Reference:** El RD 1627/1997 les obliga a aplicar los principios del artículo 15 de la Ley 31/1995, como evitar los riesgos, evaluar los que no se puedan evitar y combatir los riesgos en su origen.
**Answer:**

Los trabajadores autónomos en una obra están obligados a aplicar los **principios de la acción preventiva** que se recogen en el **artículo 15 de la Ley de Prevención de Riesgos Laborales (Ley 31/1995)**, en particular al desarrollar las tareas o actividades indicadas en el artículo 10 del Real Decreto 1627/1997 (RD 1627/1997, Artículo 12.1.a).

Dichos principios se enumeran en el **artículo 15 de la Ley 31/1995** y son los siguientes:
a) Evitar los riesgos.
b) Evaluar los riesgos que no se puedan evitar.
c) Combatir los riesgos en su origen.
d) Adaptar el trabajo a la persona, en particular en lo que respecta a la concepción de los puestos de trabajo, así como a la elección de los equipos y los métodos de trabajo y de producción, con miras, en particular, a atenuar el trabajo monótono y repetitivo y a reducir los efectos del mismo en la salud.
e) Tener en cuenta la evolución de la técnica.
f) Sustituir lo peligroso por lo que entrañe poco o ningún peligro.
g) Planificar la prevención, buscando un conjunto coherente que integre en ella la técnica, la organización del trabajo, las condiciones de trabajo, las relaciones sociales y la influencia de los factores ambientales en el trabajo.
h) Adoptar medidas que antepongan la protección colectiva a la individual.
i) Dar las debidas instrucciones a los trabajadores.

*(Nota: Esta información es meramente informativa y se basa exclusivamente en los documentos del corpus).*

**Fuentes utilizadas:**
* RD 1627/1997, Artículo 12.
* Ley 31/1995, Artículo 15.

**Citations:** RD 1627/1997, Artículo 12; Ley 31/1995, Artículo 15 — all in retrieved text

**Coverage check:**

- Search 1 «trabajadores autonomos principios de la accion preventiva obra»: **SÍ**, passage [2], quote: «a) Aplicar los principios de la acción preventiva que se recogen en el artículo 15 de la Ley de Prevención de Riesgos Laborales, en particular al desarrollar las tareas o actividades indicadas en el artículo 10 del presente Real Decreto.». Need: qué principios de la acción preventiva deben aplicar los trabajadores autónomos en una obra y dónde se enumeran

**Retrieved passages:**

[1] RD 1627/1997, Artículo 2 (score 0.772)
RD 1627/1997, Artículo 2
j) Trabajador autónomo: la persona física distinta del contratista y del subcontratista, que realiza de forma personal y directa una actividad profesional, sin sujeción a un contrato de trabajo, y que asume contractualmente ante el promotor, el contratista o el subcontratista el compromiso de realizar determinadas partes o instalaciones de la obra.
Cuando el trabajador autónomo emplee en la obra a trabajadores por cuenta ajena tendrá la consideración de contratista o subcontratista a efectos del presente Real Decreto.
2. El contratista y el subcontratista a los que se refiere el presente Real Decreto tendrán la consideración de empresario a los efectos previstos en la normativa sobre prevención de riesgos laborales.
3. Cuando el promotor contrate directamente trabajadores autónomos para la realización de la obra o de determinados trabajos de la misma, tendrá la consideración de contratista respecto de aquéllos a efectos de lo dispuesto en el presente Real Decreto.
Lo dispuesto en el párrafo anterior no será de aplicación cuando la actividad contratada se refiera exclusivamente a la construcción o reparación que pueda contratar un cabeza de familia respecto de su vivienda.

[2] RD 1627/1997, Artículo 12 (score 0.768)
RD 1627/1997, Artículo 12
Artículo 12. Obligaciones de los trabajadores autónomos.
1. Los trabajadores autónomos estarán obligados a:
a) Aplicar los principios de la acción preventiva que se recogen en el artículo 15 de la Ley de Prevención de Riesgos Laborales, en particular al desarrollar las tareas o actividades indicadas en el artículo 10 del presente Real Decreto.
b) Cumplir las disposiciones mínimas de seguridad y salud establecidas en el anexo IV del presente Real Decreto, durante la ejecución de la obra.
c) Cumplir las obligaciones en materia de prevención de riesgos que establece para los trabajadores el artículo 29, apartados 1 y 2, de la Ley de Prevención de Riesgos Laborales.
d) Ajustar su actuación en la obra conforme a los deberes de coordinación de actividades empresariales establecidos en el artículo 24 de la Ley de Prevención de Riesgos Laborales, participando en particular en cualquier medida de actuación coordinada que se hubiera establecido.
e) Utilizar equipos de trabajo que se ajusten a lo dispuesto en el Real Decreto 1215/1997, de 18 de julio, por el que se establecen las disposiciones mínimas de seguridad y salud para la utilización por los trabajadores de los equipos de trabajo.
f) Elegir y utilizar equipos de protección individual en los términos previstos en el Real Decreto 773/1997, de 30 de mayo, sobre disposiciones mínimas de seguridad y salud relativas a la utilización por los trabajadores de equipos de protección individual.
g) Atender las indicaciones y cumplir las instrucciones del coordinador en materia de seguridad y de salud durante la ejecución de la obra o, en su caso, de la dirección facultativa.
2. Los trabajadores autónomos deberán cumplir lo establecido en el plan de seguridad y salud.

[3] Ley 31/1995, Artículo 15 (score 0.754)
Ley 31/1995, Artículo 15
Artículo 15. Principios de la acción preventiva.
1. El empresario aplicará las medidas que integran el deber general de prevención previsto en el artículo anterior, con arreglo a los siguientes principios generales:
a) Evitar los riesgos.
b) Evaluar los riesgos que no se puedan evitar.
c) Combatir los riesgos en su origen.
d) Adaptar el trabajo a la persona, en particular en lo que respecta a la concepción de los puestos de trabajo, así como a la elección de los equipos y los métodos de trabajo y de producción, con miras, en particular, a atenuar el trabajo monótono y repetitivo y a reducir los efectos del mismo en la salud.
e) Tener en cuenta la evolución de la técnica.
f) Sustituir lo peligroso por lo que entrañe poco o ningún peligro.
g) Planificar la prevención, buscando un conjunto coherente que integre en ella la técnica, la organización del trabajo, las condiciones de trabajo, las relaciones sociales y la influencia de los factores ambientales en el trabajo.
h) Adoptar medidas que antepongan la protección colectiva a la individual.
i) Dar las debidas instrucciones a los trabajadores.
2. El empresario tomará en consideración las capacidades profesionales de los trabajadores en materia de seguridad y de salud en el momento de encomendarles las tareas.
3. El empresario adoptará las medidas necesarias a fin de garantizar que sólo los trabajadores que hayan recibido información suficiente y adecuada puedan acceder a las zonas de riesgo grave y específico.
4. La efectividad de las medidas preventivas deberá prever las distracciones o imprudencias no temerarias que pudiera cometer el trabajador. Para su adopción se tendrán en cuenta los riesgos adicionales que pudieran implicar determinadas medidas preventivas, las cuales sólo podrán adoptarse cuando la magnitud de dichos riesgos sea sustancialmente inferior a la de los que se pretende controlar y no existan alternativas más seguras.

[4] Ley 32/2006, Artículo 3 (score 0.741)
Ley 32/2006, Artículo 3
g) Trabajador autónomo: la persona física distinta del contratista y del subcontratista, que realiza de forma personal y directa una actividad profesional, sin sujeción a un contrato de trabajo, y que asume contractualmente ante el promotor, el contratista o el subcontratista el compromiso de realizar determinadas partes o instalaciones de la obra. Cuando el trabajador autónomo emplee en la obra a trabajadores por cuenta ajena, tendrá la consideración de contratista o subcontratista a los efectos de la presente Ley.
h) Subcontratación: la práctica mercantil de organización productiva en virtud de la cual el contratista o subcontratista encarga a otro subcontratista o trabajador autónomo parte de lo que a él se le ha encomendado.
i) Nivel de subcontratación: cada uno de los escalones en que se estructura el proceso de subcontratación que se desarrolla para la ejecución de la totalidad o parte de la obra asumida contractualmente por el contratista con el promotor.

[5] Ley 31/1995, Artículo 15 (score 0.731)
Ley 31/1995, Artículo 15
5. Podrán concertar operaciones de seguro que tengan como fin garantizar como ámbito de cobertura la previsión de riesgos derivados del trabajo, la empresa respecto de sus trabajadores, los trabajadores autónomos respecto a ellos mismos y las sociedades cooperativas respecto a sus socios cuya actividad consista en la prestación de su trabajo personal.

---
## q12 (multi, dev)
**Question:** ¿Qué formación en prevención deben garantizar las empresas a los trabajadores de una obra y en qué momentos debe darse?
**Reference:** Una formación necesaria y adecuada a su puesto o función (Ley 32/2006); teórica y práctica, al contratarse, cuando cambien sus funciones o se introduzcan nuevas tecnologías o equipos, y repetirse periódicamente si es necesario (Ley 31/1995).
**Answer:**

Según la normativa, las empresas deben garantizar que los trabajadores reciban una formación teórica y práctica, suficiente y adecuada, centrada específicamente en su puesto de trabajo o función, de forma que conozcan los riesgos y las medidas para prevenirlos (Ley 31/1995, Artículo 19; Ley 32/2006, Artículo 10). 

Los momentos en los que debe impartirse u otorgarse dicha formación son:
1. En el **momento de la contratación**, cualquiera que sea la modalidad o duración de ésta (Ley 31/1995, Artículo 19).
2. Cuando se produzcan **cambios en las funciones** que desempeñe el trabajador (Ley 31/1995, Artículo 19).
3. Cuando se introduzcan **nuevas tecnologías** o **cambios en los equipos de trabajo** (Ley 31/1995, Artículo 19).
4. **Periódicamente**, si fuera necesario, adaptándose a la evolución de los riesgos y a la aparición de otros nuevos (Ley 31/1995, Artículo 19).

Además, las empresas deben velar por que todos los trabajadores que presten servicios en las obras cuenten con dicha formación adecuada (Ley 32/2006, Artículo 10).

*(Información orientativa no vinculante basada en la Ley 31/1995 y la Ley 32/2006).*

**Fuentes utilizadas:**
- Ley 31/1995, Artículo 19
- Ley 32/2006, Artículo 10

**Citations:** Ley 31/1995, Artículo 19; Ley 32/2006, Artículo 10 — all in retrieved text

**Coverage check:**

- Search 1 «formacion prevención trabajadores obra momentos garantizar»: **SÍ**, passage [2], quote: «1. Las empresas velarán por que todos los trabajadores que presten servicios en las obras tengan la formación necesaria y adecuada a su puesto de trabajo o función en materia de prevención de riesgos laborales, de forma que conozcan los riesgos y las medidas para prevenirlos.». Need: Qué formación en prevención deben garantizar las empresas a los trabajadores de una obra y en qué momentos debe darse.

**Retrieved passages:**

[1] Ley 31/1995, Artículo 19 (score 0.769)
Ley 31/1995, Artículo 19
Artículo 19. Formación de los trabajadores.
1. En cumplimiento del deber de protección, el empresario deberá garantizar que cada trabajador reciba una formación teórica y práctica, suficiente y adecuada, en materia preventiva, tanto en el momento de su contratación, cualquiera que sea la modalidad o duración de ésta, como cuando se produzcan cambios en las funciones que desempeñe o se introduzcan nuevas tecnologías o cambios en los equipos de trabajo.
La formación deberá estar centrada específicamente en el puesto de trabajo o función de cada trabajador, adaptarse a la evolución de los riesgos y a la aparición de otros nuevos y repetirse periódicamente, si fuera necesario.
2. La formación a que se refiere el apartado anterior deberá impartirse, siempre que sea posible, dentro de la jornada de trabajo o, en su defecto, en otras horas pero con el descuento en aquélla del tiempo invertido en la misma. La formación se podrá impartir por la empresa mediante medios propios o concertándola con servicios ajenos, y su coste no recaerá en ningún caso sobre los trabajadores.

[2] Ley 32/2006, Artículo 10 (score 0.761)
Ley 32/2006, Artículo 10
Artículo 10. Acreditación de la formación preventiva de los trabajadores.
1. Las empresas velarán por que todos los trabajadores que presten servicios en las obras tengan la formación necesaria y adecuada a su puesto de trabajo o función en materia de prevención de riesgos laborales, de forma que conozcan los riesgos y las medidas para prevenirlos.
2. Sin perjuicio de la obligación legal del empresario de garantizar la formación a que se refiere el apartado anterior, en la negociación colectiva estatal del sector se podrán establecer programas formativos y contenidos específicos de carácter sectorial y para los trabajos de cada especialidad.
3. Dadas las características que concurren en el sector de la construcción, reglamentariamente o a través de la negociación colectiva sectorial de ámbito estatal, se regulará la forma de acreditar la formación específica recibida por el trabajador referida a la prevención de riesgos laborales en el sector de la construcción.
El sistema de acreditación que se establezca, que podrá consistir en la expedición de una cartilla o carné profesional para cada trabajador, será único y tendrá validez en el conjunto del sector, pudiendo atribuirse su diseño, ejecución y expedición a organismos paritarios creados en el ámbito de la negociación colectiva sectorial de ámbito estatal, en coordinación con la Fundación adscrita a la Comisión Nacional de Seguridad y Salud en el Trabajo.

[3] RD 1627/1997, Artículo 15 (score 0.724)
RD 1627/1997, Artículo 15
Artículo 15. Información a los trabajadores.
1. De conformidad con el artículo 18 de la Ley de Prevención de Riesgos Laborales, los contratistas y subcontratistas deberán garantizar que los trabajadores reciban una información adecuada de todas las medidas que hayan de adoptarse en lo que se refiere a su seguridad y su salud en la obra.
2. La información deberá ser comprensible para los trabajadores afectados.

[4] Ley 32/2006, Preámbulo (score 0.724)
Ley 32/2006, Preámbulo
A todos los que la presente vieren y entendieren.
Sabed: Que las Cortes Generales han aprobado y Yo vengo en sancionar la siguiente ley.
Tras diez años de promulgación de la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales, y después su desarrollo reglamentario, es un hecho incontestable que, pese a todo, y a los ingentes esfuerzos realizados por los distintos actores implicados en la prevención de riesgos laborales (Estado, Comunidades Autónomas, Agentes Sociales, Entidades especializadas, etcétera), existe un sector como el de la construcción que, constituyendo uno de los ejes del crecimiento económico de nuestro país, está sometido a unos riesgos especiales y continúa registrando una siniestralidad laboral muy notoria por sus cifras y gravedad.
Son numerosos los estudios y análisis desarrollados para evaluar las causas de tales índices de siniestralidad en este sector, sin que resulte posible atribuir el origen de esta situación a una causa única, dada su complejidad.
Uno de esos factores puede estar relacionado con la utilización de una forma de organización productiva, que tiene una importante tradición en el sector, pero que ha adquirido en las últimas décadas un especial desarrollo en el mismo, también como reflejo de la externalización productiva que se da en otros sectores, aunque en éste con especial intensidad. Esta forma de organización no es otra que la denominada «subcontratación».

[5] Ley 31/1995, Artículo 14 (score 0.723)
Ley 31/1995, Artículo 14
Artículo 14. Derecho a la protección frente a los riesgos laborales.
1. Los trabajadores tienen derecho a una protección eficaz en materia de seguridad y salud en el trabajo.
El citado derecho supone la existencia de un correlativo deber del empresario de protección de los trabajadores frente a los riesgos laborales.
Este deber de protección constituye, igualmente, un deber de las Administraciones públicas respecto del personal a su servicio.
Los derechos de información, consulta y participación, formación en materia preventiva, paralización de la actividad en caso de riesgo grave e inminente y vigilancia de su estado de salud, en los términos previstos en la presente Ley, forman parte del derecho de los trabajadores a una protección eficaz en materia de seguridad y salud en el trabajo.
2. En cumplimiento del deber de protección, el empresario deberá garantizar la seguridad y la salud de los trabajadores a su servicio en todos los aspectos relacionados con el trabajo. A estos efectos, en el marco de sus responsabilidades, el empresario realizará la prevención de los riesgos laborales mediante la integración de la actividad preventiva en la empresa y la adopción de cuantas medidas sean necesarias para la protección de la seguridad y la salud de los trabajadores, con las especialidades que se recogen en los artículos siguientes en materia de plan de prevención de riesgos laborales, evaluación de riesgos, información, consulta y participación y formación de los trabajadores, actuación en casos de emergencia y de riesgo grave e inminente, vigilancia de la salud, y mediante la constitución de una organización y de los medios necesarios en los términos establecidos en el capítulo IV de esta ley.
El empresario desarrollará una acción permanente de seguimiento de la actividad preventiva con el fin de perfeccionar de manera continua las actividades de identificación, evaluación y control de los riesgos que no se hayan podido evitar y los niveles de protección existentes y dispondrá lo necesario para la adaptación de las medidas de prevención señaladas en el párrafo anterior a las modificaciones que puedan experimentar las circunstancias que incidan en la realización del trabajo.

---
## q13 (unanswerable, dev)
**Question:** ¿Qué carnet o formación específica necesita un operador de grúa torre?
**Reference:** El corpus no lo cubre; debe decir que no consta en los documentos.
**Answer:** *(forced refusal)*

No consta en los documentos del corpus.

Se buscó en el corpus: «operador de grua torre carnet formacion».

**Citations:** (none)

**Coverage check:**

- Search 1 «operador de grua torre carnet formacion»: **NO**. Need: qué carnet o formación específica necesita un operador de grúa torre

**Retrieved passages:**

[1] Ley 32/2006, Artículo 10 (score 0.639)
Ley 32/2006, Artículo 10
Artículo 10. Acreditación de la formación preventiva de los trabajadores.
1. Las empresas velarán por que todos los trabajadores que presten servicios en las obras tengan la formación necesaria y adecuada a su puesto de trabajo o función en materia de prevención de riesgos laborales, de forma que conozcan los riesgos y las medidas para prevenirlos.
2. Sin perjuicio de la obligación legal del empresario de garantizar la formación a que se refiere el apartado anterior, en la negociación colectiva estatal del sector se podrán establecer programas formativos y contenidos específicos de carácter sectorial y para los trabajos de cada especialidad.
3. Dadas las características que concurren en el sector de la construcción, reglamentariamente o a través de la negociación colectiva sectorial de ámbito estatal, se regulará la forma de acreditar la formación específica recibida por el trabajador referida a la prevención de riesgos laborales en el sector de la construcción.
El sistema de acreditación que se establezca, que podrá consistir en la expedición de una cartilla o carné profesional para cada trabajador, será único y tendrá validez en el conjunto del sector, pudiendo atribuirse su diseño, ejecución y expedición a organismos paritarios creados en el ámbito de la negociación colectiva sectorial de ámbito estatal, en coordinación con la Fundación adscrita a la Comisión Nacional de Seguridad y Salud en el Trabajo.

[2] RD 1215/1997, Anexo II (score 0.626)
RD 1215/1997, Anexo II
2. Equipos de trabajo para la elevación de cargas no guiadas.
a) Si dos o más equipos de trabajo para la elevación de cargas no guiadas se instalan o se montan en un lugar de trabajo de manera que sus campos de acción se solapen, deberán adoptarse medidas adecuadas para evitar las colisiones entre las cargas o los elementos de los propios equipos.
b) Durante el empleo de un equipo de trabajo móvil para la elevación de cargas no guiadas deberán adoptarse medidas para evitar su balanceo, vuelco y, en su caso, desplazamiento y deslizamiento. Deberá comprobarse la correcta realización de estas medidas.
c) Si el operador de un equipo de trabajo para la elevación de cargas no guiadas no puede observar el trayecto completo de la carga ni directamente ni mediante los dispositivos auxiliares que faciliten las informaciones útiles, deberá designarse un encargado de señales en comunicación con el operador para guiarle y deberán adoptarse medidas de organización para evitar colisiones de la carga que puedan poner en peligro a los trabajadores.
d) Los trabajos deberán organizarse de forma que, mientras un trabajador esté colgando o descolgando una carga a mano, pueda realizar con toda seguridad esas operaciones, garantizando en particular que dicho trabajador conserve el control, directo o indirecto, de las mismas.
e) Todas las operaciones de levantamiento deberán estar correctamente planificadas, vigiladas adecuadamente y efectuadas con miras a proteger la seguridad de los trabajadores.
En particular, cuando dos o más equipos de trabajo para la elevación de cargas no guiadas deban elevar simultáneamente una carga, deberá elaborarse y aplicarse un procedimiento con el fin de garantizar una buena coordinación de los operadores.
f) Si algún equipo de trabajo para la elevación de cargas no guiadas no puede mantener las cargas en caso de avería parcial o total de la alimentación de energía, deberán adoptarse medidas apropiadas para evitar que los trabajadores se expongan a los riesgos correspondientes.

[3] RD 1215/1997, Anexo II (score 0.621)
RD 1215/1997, Anexo II
Las cargas suspendidas no deberán quedar sin vigilancia, salvo si es imposible el acceso a la zona de peligro y si la carga se ha colgado con toda seguridad y se mantiene de forma completamente segura.
g) El empleo al aire libre de equipos de trabajo para la elevación de cargas no guiadas deberá cesar cuando las condiciones meteorológicas se degraden hasta el punto de causar perjuicio a la seguridad de funcio namiento y provocar de esa manera que los trabajadores corran riesgos. Deberán adoptarse medidas adecuadas de protección, destinadas especialmente a impedir el vuelco del equipo de trabajo, para evitar riesgos a los trabajadores.
4. Disposiciones relativas a la utilización de los equipos de trabajo para la realización de trabajos temporales en altura.
4.1 Disposiciones generales.
4.1.1 Si, en aplicación de lo dispuesto en la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales, en concreto, en sus artículos 15, 16 y 17, y en el artículo 3 de este real decreto, no pueden efectuarse trabajos temporales en altura de manera segura y en condiciones ergonómicas aceptables desde una superficie adecuada, se elegirán los equipos de trabajo más apropiados para garantizar y mantener unas condiciones de trabajo seguras, teniendo en cuenta, en particular, que deberá darse prioridad a las medidas de protección colectiva frente a las medidas de protección individual y que la elección no podrá subordinarse a criterios económicos. Las dimensiones de los equipos de trabajo deberán estar adaptadas a la naturaleza del trabajo y a las dificultades previsibles y deberán permitir una circulación sin peligro.
La elección del tipo más conveniente de medio de acceso a los puestos de trabajo temporal en altura deberá efectuarse en función de la frecuencia de circulación, la altura a la que se deba subir y la duración de la utilización. La elección efectuada deberá permitir la evacuación en caso de peligro inminente. El paso en ambas direcciones entre el medio de acceso y las plataformas, tableros o pasarelas no deberá aumentar el riesgo de caída.

[4] RD 1215/1997, Anexo I (score 0.616)
RD 1215/1997, Anexo I
b) En las máquinas para elevación de cargas deberá figurar una indicación claramente visible de su carga nominal y, en su caso, una placa de carga que estipule la carga nominal de cada configuración de la máquina.
Los accesorios de elevación deberán estar marcados de tal forma que se puedan identificar las características esenciales para un uso seguro.
Si el equipo de trabajo no está destinado a la elevación de trabajadores y existe posibilidad de confusión, deberá fijarse una señalización adecuada de manera visible.
c) Los equipos de trabajo instalados de forma permanente deberán instalarse de modo que se reduzca el riesgo de que la carga caiga en picado, se suelte o se desvíe involuntariamente de forma peligrosa o, por cualquier otro motivo, golpee a los trabajadores. d) Las máquinas para elevación o desplazamiento de trabajadores deberán poseer las características apropiadas para:
1.º Evitar, por medio de dispositivos apropiados, los riesgos de caída del habitáculo, cuando existan tales riesgos.
2.º Evitar los riesgos de caída del usuario fuera del habitáculo, cuando existan tales riesgos.
3.º Evitar los riesgos de aplastamiento, aprisio namiento o choque del usuario, en especial los debidos a un contacto fortuito con objetos.
4.º Garantizar la seguridad de los trabajadores que en caso de accidente queden bloqueados en el habitáculo y permitir su liberación.
Si por razones inherentes al lugar y al desnivel, los riesgos previstos en el párrafo 1.º anterior no pueden evitarse por medio de ningún dispositivo de seguridad, deberá instalarse un cable con coeficiente de seguridad reforzado cuyo buen estado se comprobará todos los días de trabajo.

[5] Ley 31/1995, Artículo 19 (score 0.614)
Ley 31/1995, Artículo 19
Artículo 19. Formación de los trabajadores.
1. En cumplimiento del deber de protección, el empresario deberá garantizar que cada trabajador reciba una formación teórica y práctica, suficiente y adecuada, en materia preventiva, tanto en el momento de su contratación, cualquiera que sea la modalidad o duración de ésta, como cuando se produzcan cambios en las funciones que desempeñe o se introduzcan nuevas tecnologías o cambios en los equipos de trabajo.
La formación deberá estar centrada específicamente en el puesto de trabajo o función de cada trabajador, adaptarse a la evolución de los riesgos y a la aparición de otros nuevos y repetirse periódicamente, si fuera necesario.
2. La formación a que se refiere el apartado anterior deberá impartirse, siempre que sea posible, dentro de la jornada de trabajo o, en su defecto, en otras horas pero con el descuento en aquélla del tiempo invertido en la misma. La formación se podrá impartir por la empresa mediante medios propios o concertándola con servicios ajenos, y su coste no recaerá en ningún caso sobre los trabajadores.

---
## q14 (unanswerable, dev)
**Question:** ¿Está permitido hacer controles de alcoholemia a los trabajadores de la obra?
**Reference:** El corpus no lo cubre; debe decir que no consta en los documentos.
**Answer:**

En los documentos del corpus no se menciona específicamente el término "alcoholemia", pero la Ley 31/1995 de Prevención de Riesgos Laborales regula la vigilancia de la salud (Ley 31/1995, Artículo 22). 

En relación con esta materia, la norma establece que la vigilancia periódica de la salud del trabajador será voluntaria y solo podrá llevarse a cabo cuando este preste su consentimiento (Ley 31/1995, Artículo 22.1). De este carácter voluntario solo se exceptuarán, previo informe de los representantes de los trabajadores:
1. Los supuestos en los que la realización de los reconocimientos sea imprescindible para evaluar los efectos de las condiciones de trabajo sobre la salud de los trabajadores.
2. Los supuestos para verificar si el estado de salud del trabajador puede constituir un peligro para el mismo, para los demás trabajadores o para otras personas relacionadas con la empresa.
3. Los supuestos en los que así esté establecido en una disposición legal en relación con la protección de riesgos específicos y actividades de especial peligrosidad.

En todo caso, las medidas de control de la salud deben realizarse respetando el derecho a la intimidad y a la dignidad de la persona trabajadora, así como la confidencialidad de la información médica (Ley 31/1995, Artículo 22.2).

Fuentes utilizadas:
- Ley 31/1995 (Prevención de Riesgos Laborales), Artículo 22.

*Nota: Esta información es meramente divulgativa y no constituye asesoramiento legal.*

**Citations:** Ley 31/1995, Artículo 22 — all in retrieved text

**Coverage check:**

- Search 1 «alcohol alcoholemia controles trabajadores construcción»: **SÍ**, passage [2], quote: «De este carácter voluntario sólo se exceptuarán, previo informe de los representantes de los trabajadores, los supuestos en los que la realización de los reconocimientos sea imprescindible para evaluar los efectos de las condiciones de trabajo sobre la salud de los trabajadores o para verificar si el estado de salud del trabajador puede constituir un peligro para el mismo, para los demás trabajadores o para otras personas relacionadas con la empresa o cuando así esté establecido en una disposición legal en relación con la protección de riesgos específicos y actividades de especial peligrosidad.». Need: si está permitido hacer controles de alcoholemia a los trabajadores de la obra

**Retrieved passages:**

[1] Ley 32/2006, Artículo 4 (score 0.634)
Ley 32/2006, Artículo 4
4. Las empresas cuya actividad consista en ser contratadas o subcontratadas habitualmente para la realización de trabajos en obras del sector de la construcción deberán contar, en los términos que se determine reglamentariamente, con un número de trabajadores contratados con carácter indefinido que no será inferior al 10 por ciento durante los dieciocho primeros meses de vigencia de esta Ley, ni al 20 por ciento durante los meses del decimonoveno al trigésimo sexto, ni al 30 por ciento a partir del mes trigésimo séptimo, inclusive.
A estos efectos, en las cooperativas de trabajo asociado los socios trabajadores serán computados de manera análoga a los trabajadores por cuenta ajena en los términos que se determine reglamentariamente.

[2] Ley 31/1995, Artículo 22 (score 0.626)
Ley 31/1995, Artículo 22
Artículo 22. Vigilancia de la salud.
1. El empresario garantizará a los trabajadores a su servicio la vigilancia periódica de su estado de salud en función de los riesgos inherentes al trabajo.
Esta vigilancia sólo podrá llevarse a cabo cuando el trabajador preste su consentimiento. De este carácter voluntario sólo se exceptuarán, previo informe de los representantes de los trabajadores, los supuestos en los que la realización de los reconocimientos sea imprescindible para evaluar los efectos de las condiciones de trabajo sobre la salud de los trabajadores o para verificar si el estado de salud del trabajador puede constituir un peligro para el mismo, para los demás trabajadores o para otras personas relacionadas con la empresa o cuando así esté establecido en una disposición legal en relación con la protección de riesgos específicos y actividades de especial peligrosidad.
En todo caso se deberá optar por la realización de aquellos reconocimientos o pruebas que causen las menores molestias al trabajador y que sean proporcionales al riesgo.
2. Las medidas de vigilancia y control de la salud de los trabajadores se llevarán a cabo respetando siempre el derecho a la intimidad y a la dignidad de la persona del trabajador y la confidencialidad de toda la información relacionada con su estado de salud.
3. Los resultados de la vigilancia a que se refiere el apartado anterior serán comunicados a los trabajadores afectados.
4. Los datos relativos a la vigilancia de la salud de los trabajadores no podrán ser usados con fines discriminatorios ni en perjuicio del trabajador.
El acceso a la información médica de carácter personal se limitará al personal médico y a las autoridades sanitarias que lleven a cabo la vigilancia de la salud de los trabajadores, sin que pueda facilitarse al empresario o a otras personas sin consentimiento expreso del trabajador.

[3] RD 1627/1997, Artículo 19 (score 0.624)
RD 1627/1997, Artículo 19
Artículo 19. Información a la autoridad laboral.
1. La comunicación de apertura del centro de trabajo a la autoridad laboral competente deberá ser previa al comienzo de los trabajos y se presentará únicamente por los empresarios que tengan la consideración de contratistas de acuerdo con lo dispuesto en este real decreto.
La comunicación de apertura incluirá el plan de seguridad y salud al que se refiere el artículo 7 del presente real decreto.
2. El plan de seguridad y salud estará a disposición permanente de la Inspección de Trabajo y Seguridad Social y de los técnicos de los órganos especializados en materia de seguridad y salud en las Administraciones públicas competentes.

[4] Ley 32/2006, Artículo 2 (score 0.621)
Ley 32/2006, Artículo 2
Artículo 2. Ámbito de aplicación.
La presente Ley será de aplicación a los contratos que se celebren, en régimen de subcontratación, para la ejecución de los siguientes trabajos realizados en obras de construcción:
Excavación; movimiento de tierras; construcción; montaje y desmontaje de elementos prefabricados; acondicionamientos o instalaciones; transformación; rehabilitación; reparación; desmantelamiento; derribo; mantenimiento; conservación y trabajos de pintura y limpieza; saneamiento.

[5] Ley 32/2006, Anexo (score 0.618)
Ley 32/2006, Anexo
ANEXO
A) DATOS IDENTIFICATIVOS DE LA OBRA
Promotor
NIF
Contratista
NIF
Dirección Facultativa
NIF
Coordinador de seg. y salud en fase de ejecución
NIF
Domicilio de la obra
Localidad
B) REGISTRO DE SUBCONTRATACIONES
N.º orden
Empresa subcontratista o trabajador autónomo/NIF
Nivel de subcontratación
N.º orden del comitente (1)
Fecha comienzo trabajos
Objeto del contrato
Responsable de dirección trabajos/Representantes de los trabajadores
Fecha entrega plan de seg. y salud
Referencia de instrucciones del coordinador (2)
Firma del subcontratista o trabajador autónomo
Aprobación de la Dirección Facultativa (3)
(1) En esta columna se anotará el N.º de orden correspondiente al asiento de la empresa que ha subcontratado los trabajos a la subcontratista de este asiento, dejándose en blanco en caso de que la comitente sea la empresa contratista.
(2) En esta columna se hará constar, en su caso, la referencia de las hojas del Libro de incidencias al plan de seguridad y salud del contratista en las que el Coordinador de seguridad y salud en fase de ejecución haya efectuado anotaciones sobre las instrucciones sobre el desarrollo del procedimiento de coordinación establecido.
(3) Cuando proceda, se hará constar en esta columna la aprobación de la subcontratación a que se refiere el asiento por parte de la Dirección Facultativa, mediante la firma del mismo en esta casilla y la indicación de su fecha.

---
## q15 (single, dev)
**Question:** ¿Cuándo hay que hacer una comprobación inicial de un equipo de trabajo cuya seguridad depende de sus condiciones de instalación?
**Reference:** Tras su instalación y antes de la puesta en marcha por primera vez, y de nuevo después de cada montaje en un nuevo lugar o emplazamiento.
**Answer:**

Los equipos de trabajo cuya seguridad depende de sus condiciones de instalación deben someterse a una comprobación inicial en los siguientes momentos:

1. **Tras su instalación y antes de la puesta en marcha por primera vez.**
2. **Después de cada montaje en un nuevo lugar o emplazamiento**, con objeto de asegurar la correcta instalación y el buen funcionamiento de los equipos.

Esta comprobación debe ser efectuada por personal competente (RD 1215/1997, Artículo 4).

Fuentes:
- RD 1215/1997, Artículo 4.

*Nota: Esta información es de carácter orientativo e informativo; se debe consultar la normativa oficial para la aplicación estricta de las obligaciones preventivas.*

**Citations:** RD 1215/1997, Artículo 4 — all in retrieved text

**Coverage check:**

- Search 1 «comprobacion inicial equipo de trabajo condiciones de instalacion»: **SÍ**, passage [1], quote: «1. El empresario adoptará las medidas necesarias para que aquellos equipos de trabajo cuya seguridad dependa de sus condiciones de instalación se sometan a una comprobación inicial, tras su instalación y antes de la puesta en marcha por primera vez, y a una nueva comprobación después de cada montaje en un nuevo lugar o emplazamiento, con objeto de asegurar la correcta instalación y el buen funcionamiento de los equipos.». Need: cuándo hay que hacer una comprobación inicial de un equipo de trabajo cuya seguridad depende de sus condiciones de instalación

**Retrieved passages:**

[1] RD 1215/1997, Artículo 4 (score 0.789)
RD 1215/1997, Artículo 4
Artículo 4. Comprobación de los equipos de trabajo.
1. El empresario adoptará las medidas necesarias para que aquellos equipos de trabajo cuya seguridad dependa de sus condiciones de instalación se sometan a una comprobación inicial, tras su instalación y antes de la puesta en marcha por primera vez, y a una nueva comprobación después de cada montaje en un nuevo lugar o emplazamiento, con objeto de asegurar la correcta instalación y el buen funcionamiento de los equipos.
2. El empresario adoptará las medidas necesarias para que aquellos equipos de trabajo sometidos a influencias susceptibles de ocasionar deterioros que puedan generar situaciones peligrosas estén sujetos a comprobaciones y, en su caso, pruebas de carácter periódico, con objeto de asegurar el cumplimiento de las disposiciones de seguridad y de salud y de remediar a tiempo dichos deterioros.
Igualmente, se deberán realizar comprobaciones adicionales de tales equipos cada vez que se produzcan acontecimientos excepcionales, tales como transformaciones, accidentes, fenómenos naturales o falta prolongada de uso, que puedan tener consecuencias perjudiciales para la seguridad.
3. Las comprobaciones serán efectuadas por personal competente.
4. Los resultados de las comprobaciones deberán documentarse y estar a disposición de la autoridad laboral. Dichos resultados deberán conservarse durante toda la vida útil de los equipos.
Cuando los equipos de trabajo se empleen fuera de la empresa, deberán ir acompañados de una prueba material de la realización de la última comprobación.
5. Los requisitos y condiciones de las comprobaciones de los equipos de trabajo se ajustarán a lo dispuesto en la normativa específica que les sea de aplicación.

[2] RD 1215/1997, Artículo 3 (score 0.712)
RD 1215/1997, Artículo 3
Artículo 3. Obligaciones generales del empresario.
1. El empresario adoptará las medidas necesarias para que los equipos de trabajo que se pongan a disposición de los trabajadores sean adecuados al trabajo que deba realizarse y convenientemente adaptados al mismo, de forma que garanticen la seguridad y la salud de los trabajadores al utilizar dichos equipos de trabajo.
Cuando no sea posible garantizar de este modo totalmente la seguridad y la salud de los trabajadores durante la utilización de los equipos de trabajo, el empresario tomará las medidas adecuadas para reducir tales riesgos al mínimo.
En cualquier caso, el empresario deberá utilizar únicamente equipos que satisfagan:
a) Cualquier disposición legal o reglamentaria que les sea de aplicación.
b) Las condiciones generales previstas en el anexo I de este Real Decreto.
2. Para la elección de los equipos de trabajo el empresario deberá tener en cuenta los siguientes factores:
a) Las condiciones y características específicas del trabajo a desarrollar.
b) Los riesgos existentes para la seguridad y salud de los trabajadores en el lugar de trabajo y, en particular, en los puestos de trabajo, así como los riesgos que puedan derivarse de la presencia o utilización de dichos equipos o agravarse por ellos.
c) En su caso, las adaptaciones necesarias para su utilización por trabajadores discapacitados.
3. Para la aplicación de las disposiciones mínimas de seguridad y salud previstas en el presente Real Decreto, el empresario tendrá en cuenta los principios ergonómicos, especialmente en cuanto al diseño del puesto de trabajo y la posición de los trabajadores durante la utilización del equipo de trabajo.
4. La utilización de los equipos de trabajo deberá cumplir las condiciones generales establecidas en el anexo II del presente Real Decreto.
Cuando, a fin de evitar o controlar un riesgo específico para la seguridad o salud de los trabajadores, la utilización de un equipo de trabajo deba realizarse en condiciones o formas determinadas, que requieran un particular conocimiento por parte de aquéllos, el empresario adoptará las medidas necesarias para que la utilización de dicho equipo quede reservada a los trabajadores designados para ello.

[3] RD 1215/1997, Anexo II (score 0.711)
RD 1215/1997, Anexo II
ANEXO II
Disposiciones relativas a la utilización de los equipos de trabajo
Las disposiciones del presente anexo se aplicarán cuando exista el riesgo correspondiente para el equipo de trabajo considerado.
1. Condiciones generales de utilización de los equipos de trabajo
1. Los equipos de trabajo se instalarán, dispondrán y utilizarán de modo que se reduzcan los riesgos para los usuarios del equipo y para los demás trabajadores.
En su montaje se tendrá en cuenta la necesidad de suficiente espacio libre entre los elementos móviles de los equipos de trabajo y los elementos fijos o móviles de su entorno y de que puedan suministrarse o retirarse de manera segura las energías y sustancias utilizadas o producidas por el equipo.
2. Los trabajadores deberán poder acceder y permanecer en condiciones de seguridad en todos los lugares necesarios para utilizar, ajustar o mantener los equipos de trabajo.
3. Los equipos de trabajo no deberán utilizarse de forma o en operaciones o en condiciones contraindicadas por el fabricante. Tampoco podrán utilizarse sin los elementos de protección previstos para la realización de la operación de que se trate.
Los equipos de trabajo sólo podrán utilizarse de forma o en operaciones o en condiciones no consideradas por el fabricante si previamente se ha realizado una evaluación de los riesgos que ello conllevaría y se han tomado las medidas pertinentes para su eliminación o control.
4. Antes de utilizar un equipo de trabajo se comprobará que sus protecciones y condiciones de uso son las adecuadas y que su conexión o puesta en marcha no representa un peligro para terceros.
Los equipos de trabajo dejarán de utilizarse si se producen deterioros, averías u otras circunstancias que comprometan la seguridad de su funcionamiento.
5. Cuando se empleen equipos de trabajo con elementos peligrosos accesibles que no puedan ser totalmente protegidos, deberán adoptarse las precauciones y utilizarse las protecciones individuales apropiadas para reducir los riesgos al mínimo posible.
En particular, deberán tomarse las medidas necesarias para evitar, en su caso, el atrapamiento de cabello, ropas de trabajo u otros objetos que pudiera llevar el trabajador.

[4] RD 1215/1997, Artículo 3 (score 0.706)
RD 1215/1997, Artículo 3
5. El empresario adoptará las medidas necesarias para que, mediante un mantenimiento adecuado, los equipos de trabajo se conserven durante todo el tiempo de utilización en unas condiciones tales que satisfagan las disposiciones del segundo párrafo del apartado 1. Dicho mantenimiento se realizará teniendo en cuenta las instrucciones del fabricante o, en su defecto, las características de estos equipos, sus condiciones de utilización y cualquier otra circunstancia normal o excepcional que pueda influir en su deterioro o desajuste.
Las operaciones de mantenimiento, reparación o transformación de los equipos de trabajo cuya realización suponga un riesgo específico para los trabajadores sólo podrán ser encomendadas al personal especialmente capacitado para ello.

[5] RD 1215/1997, Artículo 2 (score 0.705)
RD 1215/1997, Artículo 2
Artículo 2. Definiciones.
A efectos del presente Real Decreto se entenderá por:
a) Equipo de trabajo: cualquier máquina, aparato, instrumento o instalación utilizado en el trabajo.
b) Utilización de un equipo de trabajo: cualquier actividad referida a un equipo de trabajo, tal como la puesta en marcha o la detención, el empleo, el transporte, la reparación, la transformación, el mantenimiento y la conservación, incluida, en particular, la limpieza.
c) Zona peligrosa: cualquier zona situada en el interior o alrededor de un equipo de trabajo en la que la presencia de un trabajador expuesto entrañe un riesgo para su seguridad o para su salud.
d) Trabajador expuesto: cualquier trabajador que se encuentre total o parcialmente en una zona peligrosa.
e) Operador del equipo: el trabajador encargado de la utilización de un equipo de trabajo.

---
## q16 (single, dev)
**Question:** ¿Qué medidas de emergencia debe adoptar el empresario?
**Reference:** Analizar las posibles situaciones de emergencia y adoptar medidas de primeros auxilios, lucha contra incendios y evacuación, designando personal encargado con formación suficiente, en número suficiente y con material adecuado.
**Answer:**

De acuerdo con la Ley 31/1995 (Artículo 20), el empresario, teniendo en cuenta el tamaño y la actividad de la empresa, así como la posible presencia de personas ajenas a la misma, debe adoptar las siguientes medidas en materia de emergencia:

1. **Analizar las posibles situaciones de emergencia.**
2. **Adoptar las medidas necesarias** en materia de:
   - Primeros auxilios.
   - Lucha contra incendios.
   - Evacuación de los trabajadores.
3. **Designar al personal** encargado de poner en práctica estas medidas. Dicho personal debe poseer la formación necesaria, ser suficiente en número y disponer del material adecuado.
4. **Comprobar periódicamente**, en su caso, el correcto funcionamiento de las medidas y del personal designado.
5. **Organizar las relaciones necesarias con servicios externos** a la empresa (en particular en materia de primeros auxilios, asistencia médica de urgencia, salvamento y lucha contra incendios) para garantizar la rapidez y eficacia de las actuaciones.

*(Fuentes utilizadas: Ley 31/1995, Artículo 20)*. 

*Nota: Esta información es meramente divulgativa y no constituye asesoramiento legal.*

**Citations:** Ley 31/1995, Artículo 20 — all in retrieved text

**Coverage check:**

- Search 1 «medidas de emergencia trabajador empresario»: **SÍ**, passage [1], quote: «El empresario, teniendo en cuenta el tamaño y la actividad de la empresa, así como la posible presencia de personas ajenas a la misma, deberá analizar las posibles situaciones de emergencia y adoptar las medidas necesarias en materia de primeros auxilios, lucha contra incendios y evacuación de los trabajadores, designando para ello al personal encargado de poner en práctica estas medidas y comprobando periódicamente, en su caso, su correcto funcionamiento.». Need: qué medidas de emergencia debe adoptar el empresario

**Retrieved passages:**

[1] Ley 31/1995, Artículo 20 (score 0.751)
Ley 31/1995, Artículo 20
Artículo 20. Medidas de emergencia.
El empresario, teniendo en cuenta el tamaño y la actividad de la empresa, así como la posible presencia de personas ajenas a la misma, deberá analizar las posibles situaciones de emergencia y adoptar las medidas necesarias en materia de primeros auxilios, lucha contra incendios y evacuación de los trabajadores, designando para ello al personal encargado de poner en práctica estas medidas y comprobando periódicamente, en su caso, su correcto funcionamiento. El citado personal deberá poseer la formación necesaria, ser suficiente en número y disponer del material adecuado, en función de las circunstancias antes señaladas.
Para la aplicación de las medidas adoptadas, el empresario deberá organizar las relaciones que sean necesarias con servicios externos a la empresa, en particular en materia de primeros auxilios, asistencia médica de urgencia, salvamento y lucha contra incendios, de forma que quede garantizada la rapidez y eficacia de las mismas.

[2] Ley 31/1995, Artículo 21 (score 0.692)
Ley 31/1995, Artículo 21
Artículo 21. Riesgo grave e inminente.
1. Cuando los trabajadores estén o puedan estar expuestos a un riesgo grave e inminente con ocasión de su trabajo, el empresario estará obligado a:
a) Informar lo antes posible a todos los trabajadores afectados acerca de la existencia de dicho riesgo y de las medidas adoptadas o que, en su caso, deban adoptarse en materia de protección.
b) Adoptar las medidas y dar las instrucciones necesarias para que, en caso de peligro grave, inminente e inevitable, los trabajadores puedan interrumpir su actividad y, si fuera necesario, abandonar de inmediato el lugar de trabajo. En este supuesto no podrá exigirse a los trabajadores que reanuden su actividad mientras persista el peligro, salvo excepción debidamente justificada por razones de seguridad y determinada reglamentariamente.
c) Disponer lo necesario para que el trabajador que no pudiera ponerse en contacto con su superior jerárquico, ante una situación de peligro grave e inminente para su seguridad, la de otros trabajadores o la de terceros a la empresa, esté en condiciones, habida cuenta de sus conocimientos y de los medios técnicos puestos a su disposición, de adoptar las medidas necesarias para evitar las consecuencias de dicho peligro.
2. De acuerdo con lo previsto en el apartado 1 del artículo 14 de la presente Ley, el trabajador tendrá derecho a interrumpir su actividad y abandonar el lugar de trabajo, en caso necesario, cuando considere que dicha actividad entraña un riesgo grave e inminente para su vida o su salud.
3. Cuando en el caso a que se refiere el apartado 1 de este artículo el empresario no adopte o no permita la adopción de las medidas necesarias para garantizar la seguridad y la salud de los trabajadores, los representantes legales de éstos podrán acordar, por mayoría de sus miembros, la paralización de la actividad de los trabajadores afectados por dicho riesgo. Tal acuerdo será comunicado de inmediato a la empresa y a la autoridad laboral, la cual, en el plazo de veinticuatro horas, anulará o ratificará la paralización acordada.

[3] Ley 31/1995, Artículo 21 (score 0.686)
Ley 31/1995, Artículo 21
El acuerdo a que se refiere el párrafo anterior podrá ser adoptado por decisión mayoritaria de los Delegados de Prevención cuando no resulte posible reunir con la urgencia requerida al órgano de representación del personal.
4. Los trabajadores o sus representantes no podrán sufrir perjuicio alguno derivado de la adopción de las medidas a que se refieren los apartados anteriores, a menos que hubieran obrado de mala fe o cometido negligencia grave.

[4] Ley 31/1995, Artículo 53 (score 0.68)
Ley 31/1995, Artículo 53
Artículo 53. Suspensión o cierre del centro de trabajo.
El Gobierno o, en su caso, los órganos de gobierno de las Comunidades Autónomas con competencias en la materia, cuando concurran circunstancias de excepcional gravedad en las infracciones en materia de seguridad y salud en el trabajo, podrán acordar la suspensión de las actividades laborales por un tiempo determinado o, en caso extremo, el cierre del centro de trabajo correspondiente, sin perjuicio, en todo caso, del pago del salario o de las indemnizaciones que procedan y de las medidas que puedan arbitrarse para su garantía.

[5] RD 39/1997, Artículo 12 (score 0.677)
RD 39/1997, Artículo 12
Artículo 12. Designación de trabajadores.
1. El empresario designará a uno o varios trabajadores para ocuparse de la actividad preventiva en la empresa.
Las actividades preventivas para cuya realización no resulte suficiente la designación de uno o varios trabajadores deberán ser desarrolladas a través de uno o más servicios de prevención propios o ajenos.
2. No obstante lo dispuesto en el apartado anterior, no será obligatoria la designación de trabajadores cuando el empresario:
a) Haya asumido personalmente la actividad preventiva de acuerdo con lo señalado en el artículo 11.
b) Haya recurrido a un servicio de prevención propio.
c) Haya recurrido a un servicio de prevención ajeno.

---
## q17 (single, dev)
**Question:** ¿Cuándo deben utilizarse los equipos de protección individual?
**Reference:** Cuando los riesgos no se puedan evitar o limitar suficientemente por medios técnicos de protección colectiva o mediante medidas, métodos o procedimientos de organización del trabajo.
**Answer:**

Los equipos de protección individual deben utilizarse **cuando los riesgos no se puedan evitar o no puedan limitarse suficientemente por medios técnicos de protección colectiva o mediante medidas, métodos o procedimientos de organización del trabajo** (Ley 31/1995, Artículo 17).

Fuentes:
* Ley 31/1995 (Prevención de Riesgos Laborales), Artículo 17.

*Nota: Esta información es de carácter divulgativo y no constituye asesoramiento legal.*

**Citations:** Ley 31/1995, Artículo 17 — all in retrieved text

**Coverage check:**

- Search 1 «utilizacion equipos de proteccion individual cuando»: **SÍ**, passage [1], quote: «Los equipos de protección individual deberán utilizarse cuando los riesgos no se puedan evitar o no puedan limitarse suficientemente por medios técnicos de protección colectiva o mediante medidas, métodos o procedimientos de organización del trabajo.». Need: cuándo deben utilizarse los equipos de protección individual

**Retrieved passages:**

[1] Ley 31/1995, Artículo 17 (score 0.775)
Ley 31/1995, Artículo 17
Artículo 17. Equipos de trabajo y medios de protección.
1. El empresario adoptará las medidas necesarias con el fin de que los equipos de trabajo sean adecuados para el trabajo que deba realizarse y convenientemente adaptados a tal efecto, de forma que garanticen la seguridad y la salud de los trabajadores al utilizarlos.
Cuando la utilización de un equipo de trabajo pueda presentar un riesgo específico para la seguridad y la salud de los trabajadores, el empresario adoptará las medidas necesarias con el fin de que:
a) La utilización del equipo de trabajo quede reservada a los encargados de dicha utilización.
b) Los trabajos de reparación, transformación, mantenimiento o conservación sean realizados por los trabajadores específicamente capacitados para ello.
2. El empresario deberá proporcionar a sus trabajadores equipos de protección individual adecuados para el desempeño de sus funciones y velar por el uso efectivo de los mismos cuando, por la naturaleza de los trabajos realizados, sean necesarios.
Los equipos de protección individual deberán utilizarse cuando los riesgos no se puedan evitar o no puedan limitarse suficientemente por medios técnicos de protección colectiva o mediante medidas, métodos o procedimientos de organización del trabajo.

[2] Ley 31/1995, Artículo 4 (score 0.742)
Ley 31/1995, Artículo 4
c) Los procedimientos para la utilización de los agentes citados anteriormente que influyan en la generación de los riesgos mencionados.
d) Todas aquellas otras características del trabajo, incluidas las relativas a su organización y ordenación, que influyan en la magnitud de los riesgos a que esté expuesto el trabajador.
8.º Se entenderá por «equipo de protección individual» cualquier equipo destinado a ser llevado o sujetado por el trabajador para que le proteja de uno o varios riesgos que puedan amenazar su seguridad o su salud en el trabajo, así como cualquier complemento o accesorio destinado a tal fin.

[3] Ley 31/1995, Artículo 29 (score 0.716)
Ley 31/1995, Artículo 29
Artículo 29. Obligaciones de los trabajadores en materia de prevención de riesgos.
1. Corresponde a cada trabajador velar, según sus posibilidades y mediante el cumplimiento de las medidas de prevención que en cada caso sean adoptadas, por su propia seguridad y salud en el trabajo y por la de aquellas otras personas a las que pueda afectar su actividad profesional, a causa de sus actos y omisiones en el trabajo, de conformidad con su formación y las instrucciones del empresario.
2. Los trabajadores, con arreglo a su formación y siguiendo las instrucciones del empresario, deberán en particular:
1.º Usar adecuadamente, de acuerdo con su naturaleza y los riesgos previsibles, las máquinas, aparatos, herramientas, sustancias peligrosas, equipos de transporte y, en general, cualesquiera otros medios con los que desarrollen su actividad.
2.º Utilizar correctamente los medios y equipos de protección facilitados por el empresario, de acuerdo con las instrucciones recibidas de éste.
3.º No poner fuera de funcionamiento y utilizar correctamente los dispositivos de seguridad existentes o que se instalen en los medios relacionados con su actividad o en los lugares de trabajo en los que ésta tenga lugar.
4.º Informar de inmediato a su superior jerárquico directo, y a los trabajadores designados para realizar actividades de protección y de prevención o, en su caso, al servicio de prevención, acerca de cualquier situación que, a su juicio, entrañe, por motivos razonables, un riesgo para la seguridad y la salud de los trabajadores.
5.º Contribuir al cumplimiento de las obligaciones establecidas por la autoridad competente con el fin de proteger la seguridad y la salud de los trabajadores en el trabajo.
6.º Cooperar con el empresario para que éste pueda garantizar unas condiciones de trabajo que sean seguras y no entrañen riesgos para la seguridad y la salud de los trabajadores.

[4] RD 1215/1997, Anexo II (score 0.709)
RD 1215/1997, Anexo II
ANEXO II
Disposiciones relativas a la utilización de los equipos de trabajo
Las disposiciones del presente anexo se aplicarán cuando exista el riesgo correspondiente para el equipo de trabajo considerado.
1. Condiciones generales de utilización de los equipos de trabajo
1. Los equipos de trabajo se instalarán, dispondrán y utilizarán de modo que se reduzcan los riesgos para los usuarios del equipo y para los demás trabajadores.
En su montaje se tendrá en cuenta la necesidad de suficiente espacio libre entre los elementos móviles de los equipos de trabajo y los elementos fijos o móviles de su entorno y de que puedan suministrarse o retirarse de manera segura las energías y sustancias utilizadas o producidas por el equipo.
2. Los trabajadores deberán poder acceder y permanecer en condiciones de seguridad en todos los lugares necesarios para utilizar, ajustar o mantener los equipos de trabajo.
3. Los equipos de trabajo no deberán utilizarse de forma o en operaciones o en condiciones contraindicadas por el fabricante. Tampoco podrán utilizarse sin los elementos de protección previstos para la realización de la operación de que se trate.
Los equipos de trabajo sólo podrán utilizarse de forma o en operaciones o en condiciones no consideradas por el fabricante si previamente se ha realizado una evaluación de los riesgos que ello conllevaría y se han tomado las medidas pertinentes para su eliminación o control.
4. Antes de utilizar un equipo de trabajo se comprobará que sus protecciones y condiciones de uso son las adecuadas y que su conexión o puesta en marcha no representa un peligro para terceros.
Los equipos de trabajo dejarán de utilizarse si se producen deterioros, averías u otras circunstancias que comprometan la seguridad de su funcionamiento.
5. Cuando se empleen equipos de trabajo con elementos peligrosos accesibles que no puedan ser totalmente protegidos, deberán adoptarse las precauciones y utilizarse las protecciones individuales apropiadas para reducir los riesgos al mínimo posible.
En particular, deberán tomarse las medidas necesarias para evitar, en su caso, el atrapamiento de cabello, ropas de trabajo u otros objetos que pudiera llevar el trabajador.

[5] Ley 31/1995, Artículo 15 (score 0.705)
Ley 31/1995, Artículo 15
Artículo 15. Principios de la acción preventiva.
1. El empresario aplicará las medidas que integran el deber general de prevención previsto en el artículo anterior, con arreglo a los siguientes principios generales:
a) Evitar los riesgos.
b) Evaluar los riesgos que no se puedan evitar.
c) Combatir los riesgos en su origen.
d) Adaptar el trabajo a la persona, en particular en lo que respecta a la concepción de los puestos de trabajo, así como a la elección de los equipos y los métodos de trabajo y de producción, con miras, en particular, a atenuar el trabajo monótono y repetitivo y a reducir los efectos del mismo en la salud.
e) Tener en cuenta la evolución de la técnica.
f) Sustituir lo peligroso por lo que entrañe poco o ningún peligro.
g) Planificar la prevención, buscando un conjunto coherente que integre en ella la técnica, la organización del trabajo, las condiciones de trabajo, las relaciones sociales y la influencia de los factores ambientales en el trabajo.
h) Adoptar medidas que antepongan la protección colectiva a la individual.
i) Dar las debidas instrucciones a los trabajadores.
2. El empresario tomará en consideración las capacidades profesionales de los trabajadores en materia de seguridad y de salud en el momento de encomendarles las tareas.
3. El empresario adoptará las medidas necesarias a fin de garantizar que sólo los trabajadores que hayan recibido información suficiente y adecuada puedan acceder a las zonas de riesgo grave y específico.
4. La efectividad de las medidas preventivas deberá prever las distracciones o imprudencias no temerarias que pudiera cometer el trabajador. Para su adopción se tendrán en cuenta los riesgos adicionales que pudieran implicar determinadas medidas preventivas, las cuales sólo podrán adoptarse cuando la magnitud de dichos riesgos sea sustancialmente inferior a la de los que se pretende controlar y no existan alternativas más seguras.

---
## q18 (single, dev)
**Question:** ¿Quién aprueba el plan de seguridad y salud de una obra y cuándo?
**Reference:** El coordinador en materia de seguridad y salud durante la ejecución de la obra, antes del inicio de la obra; en obras de las Administraciones públicas lo aprueba la Administración que adjudicó la obra, con informe del coordinador.
**Answer:**

El plan de seguridad y salud de una obra debe aprobarse **antes del inicio de la obra** (RD 1627/1997, Artículo 7).

¿Quién lo aprueba depende del tipo de obra?
1. **Regla general:** Debe ser aprobado por el **coordinador en materia de seguridad y de salud durante la ejecución de la obra** (RD 1627/1997, Artículo 7 y Artículo 9).
2. **Obras de las Administraciones públicas:** El plan, con el correspondiente informe del coordinador, se elevará para su aprobación a la **Administración pública que haya adjudicado la obra** (RD 1627/1997, Artículo 7).
3. **Obras donde no sea necesaria la designación de coordinador:** Las funciones de aprobación serán asumidas por la **dirección facultativa** (RD 1627/1997, Artículo 7 y Artículo 9).

Fuentes utilizadas:
- RD 1627/1997, Artículo 7 y Artículo 9.

*Nota: Esta información es de carácter orientativo y no constituye asesoramiento legal.*

**Citations:** RD 1627/1997, Artículo 7 — all in retrieved text

**Coverage check:**

- Search 1 «aprobacion plan de seguridad y salud en obras»: **SÍ**, passage [1], quote: «2. El plan de seguridad y salud deberá ser aprobado, antes del inicio de la obra, por el coordinador en materia de seguridad y de salud durante la ejecución de la obra.». Need: Quién aprueba el plan de seguridad y salud de una obra y cuándo

**Retrieved passages:**

[1] RD 1627/1997, Artículo 7 (score 0.777)
RD 1627/1997, Artículo 7
Artículo 7. Plan de seguridad y salud en el trabajo.
1. En aplicación del estudio de seguridad y salud o, en su caso, del estudio básico, cada contratista elaborará un plan de seguridad y salud en el trabajo en el que se analicen, estudien, desarrollen y complementen las previsiones contenidas en el estudio o estudio básico, en función de su propio sistema de ejecución de la obra. En dicho plan se incluirán, en su caso, las propuestas de medidas alternativas de prevención que el contratista proponga con la correspondiente justificación técnica, que no podrán implicar disminución de los niveles de protección previstos en el estudio o estudio básico.
En el caso de planes de seguridad y salud elaborados en aplicación del estudio de seguridad y salud las propuestas de medidas alternativas de prevención incluirán la valoración económica de las mismas, que no podrá implicar disminución del importe total, de acuerdo con el segundo párrafo del apartado 4 del artículo 5.
2. El plan de seguridad y salud deberá ser aprobado, antes del inicio de la obra, por el coordinador en materia de seguridad y de salud durante la ejecución de la obra.
En el caso de obras de las Administraciones públicas, el plan, con el correspondiente informe del coordinador en materia de seguridad y de salud durante la ejecución de la obra, se elevará para su aprobación a la Administración pública que haya adjudicado la obra.
Cuando no sea necesaria la designación de coordinador, las funciones que se le atribuyen en los párrafos anteriores serán asumidas por la dirección facultativa.
3. En relación con los puestos de trabajo en la obra, el plan de seguridad y salud en el trabajo a que se refiere este artículo constituye el instrumento básico de ordenación de las actividades de identificación y, en su caso, evaluación de los riesgos y planificación de la actividad preventiva a las que se refiere el capítulo II del Real Decreto por el que se aprueba el Reglamento de los Servicios de Prevención.

[2] RD 1627/1997, Artículo 7 (score 0.749)
RD 1627/1997, Artículo 7
4. El plan de seguridad y salud podrá ser modificado por el contratista en función del proceso de ejecución de la obra, de la evolución de los trabajos y de las posibles incidencias o modificaciones que puedan surgir a lo largo de la obra, pero siempre con la aprobación expresa en los términos del apartado 2. Quienes intervengan en la ejecución de la obra, así como las personas u órganos con responsabilidades en materia de prevención en las empresas intervinientes en la misma y los representantes de los trabajadores, podrán presentar, por escrito y de forma razonada, las sugerencias y alternativas que estimen oportunas. A tal efecto, el plan de seguridad y salud estará en la obra a disposición permanente de los mismos.
5. Asimismo, el plan de seguridad y salud estará en la obra a disposición permanente de la dirección facultativa.

[3] RD 1627/1997, Artículo 17 (score 0.744)
RD 1627/1997, Artículo 17
Artículo 17. Visado de proyectos.
1. La inclusión en el proyecto de ejecución de obra del estudio de seguridad y salud o, en su caso, del estudio básico será requisito necesario para el visado de aquél por el Colegio profesional correspondiente, expedición de la licencia municipal y demás autorizaciones y trámites por parte de las distintas Administraciones públicas.
2. En la tramitación para la aprobación de los proyectos de obras de las Administraciones públicas se hará declaración expresa por la Oficina de Supervisión de Proyectos u órgano equivalente sobre la inclusión del correspondiente estudio de seguridad y salud o, en su caso, del estudio básico.

[4] RD 1627/1997, Artículo 9 (score 0.742)
RD 1627/1997, Artículo 9
Artículo 9. Obligaciones del coordinador en materia de seguridad y de salud durante la ejecución de la obra.
El coordinador en materia de seguridad y salud durante la ejecución de la obra deberá desarrollar las siguientes funciones:
a) Coordinar la aplicación de los principios generales de prevención y de seguridad:
1.º Al tomar las decisiones técnicas y de organización con el fin de planificar los distintos trabajos o fases de trabajo que vayan a desarrollarse simultánea o sucesivamente.
2.º Al estimar la duración requerida para la ejecución de estos distintos trabajos o fases de trabajo.
b) Coordinar las actividades de la obra para garantizar que los contratistas y, en su caso, los subcontratistas y los trabajadores autónomos apliquen de manera coherente y responsable los principios de la acción preventiva que se recogen en el artículo 15 de la Ley de Prevención de Riesgos Laborales durante la ejecución de la obra y, en particular, en las tareas o actividades a que se refiere el artículo 10 de este Real Decreto.
c) Aprobar el plan de seguridad y salud elaborado por el contratista y, en su caso, las modificaciones introducidas en el mismo. Conforme a lo dispuesto en el último párrafo del apartado 2 del artículo 7, la dirección facultativa asumirá esta función cuando no fuera necesaria la designación de coordinador.
d) Organizar la coordinación de actividades empresariales prevista en el artículo 24 de la Ley de Prevención de Riesgos Laborales.
e) Coordinar las acciones y funciones de control de la aplicación correcta de los métodos de trabajo.
f) Adoptar las medidas necesarias para que sólo las personas autorizadas puedan acceder a la obra. La dirección facultativa asumirá esta función cuando no fuera necesaria la designación de coordinador.

[5] RD 1627/1997, Artículo 19 (score 0.739)
RD 1627/1997, Artículo 19
Artículo 19. Información a la autoridad laboral.
1. La comunicación de apertura del centro de trabajo a la autoridad laboral competente deberá ser previa al comienzo de los trabajos y se presentará únicamente por los empresarios que tengan la consideración de contratistas de acuerdo con lo dispuesto en este real decreto.
La comunicación de apertura incluirá el plan de seguridad y salud al que se refiere el artículo 7 del presente real decreto.
2. El plan de seguridad y salud estará a disposición permanente de la Inspección de Trabajo y Seguridad Social y de los técnicos de los órganos especializados en materia de seguridad y salud en las Administraciones públicas competentes.

---
## q19 (single, dev)
**Question:** ¿Quién puede paralizar los trabajos en una obra y en qué circunstancias?
**Reference:** El coordinador de seguridad y salud en ejecución o cualquier otra persona de la dirección facultativa, en circunstancias de riesgo grave e inminente, tras advertir al contratista y dejar constancia en el libro de incidencias.
**Answer:**

Según la normativa de seguridad y salud en las obras de construcción, los trabajos pueden ser paralizados por los siguientes sujetos y circunstancias:

1. **El coordinador en materia de seguridad y salud durante la ejecución de la obra o cualquier persona integrada en la dirección facultativa**:
   - **Circunstancias**: Cuando observen incumplimientos de las medidas de seguridad y salud y se den **circunstancias de riesgo grave e inminente** para la seguridad y la salud de los trabajadores (RD 1627/1997, Artículo 14). Previamente deben advertir al contratista y dejar constancia en el libro de incidencias (cuando este exista).

2. **El Inspector de Trabajo y Seguridad Social**:
   - **Circunstancias**: Cuando compruebe que la inobservancia de la normativa sobre prevención de riesgos laborales implica, a su juicio, un **riesgo grave e inminente** para la seguridad y la salud de los trabajadores, pudiendo ordenar la paralización inmediata de tales trabajos o tareas (Ley 31/1995, Artículo 44).

Asimismo, se contemplan otros supuestos generales de paralización o suspensión en la Ley de Prevención de Riesgos Laborales (artículos 21 y 44) y medidas gubernativas de suspensión o cierre en casos de excepcional gravedad (Ley 31/1995, Artículo 53).

**Fuentes utilizadas:**
- RD 1627/1997, Artículo 14.
- Ley 31/1995 (Ley de Prevención de Riesgos Laborales), Artículos 44 y 53.

*(Nota: Esta información es de carácter divulgativo y no constituye asesoramiento jurídico).*

**Citations:** RD 1627/1997, Artículo 14; Ley 31/1995, Artículo 44; Ley 31/1995, Artículo 53 — all in retrieved text

**Coverage check:**

- Search 1 «paralización trabajos obra circunstancias»: **SÍ**, passage [1], quote: «1. Sin perjuicio de lo previsto en los apartados 2 y 3 del artículo 21 y en el artículo 44 de la Ley de Prevención de Riesgos Laborales, cuando el coordinador en materia de seguridad y salud durante la ejecución de la obra o cualquier otra persona integrada en la dirección facultativa observase incumplimiento de las medidas de seguridad y salud, advertirá al contratista de ello, dejando constancia de tal incumplimiento en el libro de incidencias, cuando éste exista de acuerdo con lo dispuesto en el apartado 1 del artículo 13, y quedando facultado para, en circunstancias de riesgo grave e inminente para la seguridad y la salud de los trabajadores, disponer la paralización de los tajos o, en su caso, de la totalidad de la obra.». Need: quién puede paralizar los trabajos en una obra y en qué circunstancias

**Retrieved passages:**

[1] RD 1627/1997, Artículo 14 (score 0.755)
RD 1627/1997, Artículo 14
Artículo 14. Paralización de los trabajos.
1. Sin perjuicio de lo previsto en los apartados 2 y 3 del artículo 21 y en el artículo 44 de la Ley de Prevención de Riesgos Laborales, cuando el coordinador en materia de seguridad y salud durante la ejecución de la obra o cualquier otra persona integrada en la dirección facultativa observase incumplimiento de las medidas de seguridad y salud, advertirá al contratista de ello, dejando constancia de tal incumplimiento en el libro de incidencias, cuando éste exista de acuerdo con lo dispuesto en el apartado 1 del artículo 13, y quedando facultado para, en circunstancias de riesgo grave e inminente para la seguridad y la salud de los trabajadores, disponer la paralización de los tajos o, en su caso, de la totalidad de la obra.
2. En el supuesto previsto en el apartado anterior, la persona que hubiera ordenado la paralización deberá dar cuenta a los efectos oportunos a la Inspección de Trabajo y Seguridad Social correspondiente, a los contratistas y, en su caso, a los subcontratistas afectados por la paralización, así como a los representantes de los trabajadores de éstos.
3. Asimismo, lo dispuesto en este artículo se entiende sin perjuicio de la normativa sobre contratos de las Administraciones públicas relativa al cumplimiento de plazos y suspensión de obras.

[2] Ley 31/1995, Artículo 44 (score 0.738)
Ley 31/1995, Artículo 44
Artículo 44. Paralización de trabajos.
1. Cuando el Inspector de Trabajo y Seguridad Social compruebe que la inobservancia de la normativa sobre prevención de riesgos laborales implica, a su juicio, un riesgo grave e inminente para la seguridad y la salud de los trabajadores podrá ordenar la paralización inmediata de tales trabajos o tareas. Dicha medida será comunicada a la empresa responsable, que la pondrá en conocimiento inmediato de los trabajadores afectados, del Comité de Seguridad y Salud, del Delegado de Prevención o, en su ausencia, de los representantes del personal. La empresa responsable dará cuenta al Inspector de Trabajo y Seguridad Social del cumplimiento de esta notificación.
El Inspector de Trabajo y Seguridad Social dará traslado de su decisión de forma inmediata a la autoridad laboral. La empresa, sin perjuicio del cumplimiento inmediato de tal decisión, podrá impugnarla ante la autoridad laboral en el plazo de tres días hábiles, debiendo resolverse tal impugnación en el plazo máximo de veinticuatro horas. Tal resolución será ejecutiva, sin perjuicio de los recursos que procedan.
La paralización de los trabajos se levantará por la Inspección de Trabajo y Seguridad Social que la hubiera decretado, o por el empresario tan pronto como se subsanen las causas que la motivaron, debiendo, en este último caso, comunicarlo inmediatamente a la Inspección de Trabajo y Seguridad Social.
2. Los supuestos de paralización regulados en este artículo, así como los que se contemplen en la normativa reguladora de las actividades previstas en el apartado 2 del artículo 7 de la presente Ley, se entenderán, en todo caso, sin perjuicio del pago del salario o de las indemnizaciones que procedan y de las medidas que puedan arbitrarse para su garantía.

[3] Ley 32/2006, Disposición adicional tercera (score 0.715)
Ley 32/2006, Disposición adicional tercera
Asimismo, tendrán la consideración de finalización de obra la disminución real del volumen de obra por la realización paulatina de las correspondientes unidades de ejecución debidamente acreditada, así como la paralización, definitiva o temporal, de entidad suficiente, de una obra, por causa imprevisible para la empresa y ajena a su voluntad.
La finalización de la obra deberá ser puesta en conocimiento de la representación legal de las personas trabajadoras, en su caso, así como de las comisiones paritarias de los convenios de ámbito correspondiente o, en su defecto, de los sindicatos representativos del sector, con cinco días de antelación a su efectividad y dará lugar a la propuesta de recolocación prevista en esta disposición.
4. La propuesta de recolocación prevista en esta disposición será formalizada por escrito mediante una cláusula que se anexará al contrato de trabajo.
Esta cláusula, que deberá precisar las condiciones esenciales, ubicación de la obra y fecha de incorporación a la misma, así como las acciones formativas exigibles para ocupar el nuevo puesto, será sometida a aceptación por parte de la persona trabajadora con quince días de antelación a la finalización de su trabajo en la obra en la que se encuentre prestando servicios.
5. Una vez efectuada la propuesta de recolocación, el contrato indefinido adscrito a obra podrá extinguirse por motivos inherentes a la persona trabajadora cuando se dé alguna de las siguientes circunstancias:
a) La persona trabajadora afectada rechaza la recolocación.
b) La cualificación de la persona afectada, incluso tras un proceso de formación o recualificación, no resulta adecuada a las nuevas obras que tenga la empresa en la misma provincia, o no permite su integración en estas, por existir un exceso de personas con la cualificación necesaria para desarrollar sus mismas funciones.
La negociación colectiva de ámbito estatal del sector correspondiente precisará los criterios de prioridad o permanencia que deben operar en caso de concurrir estos motivos en varias personas trabajadoras de forma simultánea en relación con la misma obra.

[4] Ley 32/2006, Disposición adicional tercera (score 0.679)
Ley 32/2006, Disposición adicional tercera
Disposición adicional tercera. Extinción del contrato indefinido por motivos inherentes a la persona trabajadora en el sector de la construcción.
1. Sin perjuicio de lo previsto en la sección 4.ª del capítulo III del título I del Estatuto de los Trabajadores, los contratos de trabajo indefinidos adscritos a obra celebrados en el ámbito de las empresas del sector de la construcción, podrán extinguirse por motivos inherentes a la persona trabajadora conforme a lo dispuesto en la presente disposición, que resultará aplicable con independencia del número de personas trabajadoras afectadas.
Tendrán la consideración de contratos indefinidos adscritos a obra aquellos que tengan por objeto tareas o servicios cuya finalidad y resultado estén vinculados a obras de construcción, teniendo en cuenta las actividades establecidas en el ámbito funcional del Convenio General del Sector de la Construcción.
La extinción regulada en este artículo no resultará aplicable a las personas trabajadoras que formen parte del personal de estructura.
2. La finalización de la obra en la que presta servicios la persona trabajadora determinará la obligación para la empresa de efectuarle una propuesta de recolocación, previo desarrollo, de ser preciso, de un proceso de formación.
Este proceso, que será siempre a cargo de la empresa, podrá realizarse directamente o a través de una entidad especializada, siendo preferente la formación que imparta la Fundación Laboral de la Construcción con cargo a las cuotas empresariales.
La negociación colectiva de ámbito estatal del sector de la construcción determinará los requisitos de acceso, duración y modalidades de formación adecuadas según las cualificaciones requeridas para cada puesto, nivel, función y grupo profesional.
El indicado proceso de formación podrá desarrollarse con antelación a la finalización de la obra.
3. A efectos de lo previsto en esta disposición, se entenderá por finalización de las obras y servicios la terminación real, verificable y efectiva de los trabajos desarrollados por esta.

[5] Ley 31/1995, Artículo 53 (score 0.675)
Ley 31/1995, Artículo 53
Artículo 53. Suspensión o cierre del centro de trabajo.
El Gobierno o, en su caso, los órganos de gobierno de las Comunidades Autónomas con competencias en la materia, cuando concurran circunstancias de excepcional gravedad en las infracciones en materia de seguridad y salud en el trabajo, podrán acordar la suspensión de las actividades laborales por un tiempo determinado o, en caso extremo, el cierre del centro de trabajo correspondiente, sin perjuicio, en todo caso, del pago del salario o de las indemnizaciones que procedan y de las medidas que puedan arbitrarse para su garantía.

---
## q20 (single, dev)
**Question:** ¿Puede un tercer subcontratista subcontratar a su vez los trabajos que tiene contratados?
**Reference:** No, el tercer subcontratista no puede subcontratar los trabajos que haya contratado con otro subcontratista o trabajador autónomo.
**Answer:**

**No**, con carácter general **el tercer subcontratista no podrá subcontratar** los trabajos que hubiera contratado con otro subcontratista o trabajador autónomo (Ley 32/2006, Artículo 5).

No obstante, la ley prevé una excepción: se podrá extender la subcontratación en un nivel adicional de forma excepcional cuando, en casos fortuitos debidamente justificados por exigencias de especialización, complicaciones técnicas o fuerza mayor, sea necesario a juicio de la dirección facultativa. Para ello, será obligatorio que la dirección facultativa apruebe previamente dicha contratación y haga constar la causa o causas motivadoras en el Libro de Subcontratación (Ley 32/2006, Artículo 5).

Fuentes utilizadas:
- Ley 32/2006, Artículo 5.

*(Nota: Esta información es de carácter divulgativo y no constituye asesoramiento jurídico).*

**Citations:** Ley 32/2006, Artículo 5 — all in retrieved text

**Coverage check:**

- Search 1 «subcontratacion tercer subcontratista sector construccion»: **SÍ**, passage [1], quote: «d) El tercer subcontratista no podrá subcontratar los trabajos que hubiera contratado con otro subcontratista o trabajador autónomo.». Need: si un tercer subcontratista puede subcontratar a su vez los trabajos que tiene contratados

**Retrieved passages:**

[1] Ley 32/2006, Artículo 5 (score 0.795)
Ley 32/2006, Artículo 5
Artículo 5. Régimen de la subcontratación.
1. La subcontratación, como forma de organización productiva, no podrá ser limitada, salvo en las condiciones y en los supuestos previstos en esta Ley.
2. Con carácter general, el régimen de la subcontratación en el sector de la construcción será el siguiente:
a) El promotor podrá contratar directamente con cuantos contratistas estime oportuno ya sean personas físicas o jurídicas.
b) El contratista podrá contratar con las empresas subcontratistas o trabajadores autónomos la ejecución de los trabajos que hubiera contratado con el promotor.
c) El primer y segundo subcontratistas podrán subcontratar la ejecución de los trabajos que, respectivamente, tengan contratados, salvo en los supuestos previstos en la letra f) del presente apartado.
d) El tercer subcontratista no podrá subcontratar los trabajos que hubiera contratado con otro subcontratista o trabajador autónomo.
e) El trabajador autónomo no podrá subcontratar los trabajos a él encomendados ni a otras empresas subcontratistas ni a otros trabajadores autónomos.
f) Asimismo, tampoco podrán subcontratar los subcontratistas, cuya organización productiva puesta en uso en la obra consista fundamentalmente en la aportación de mano de obra, entendiéndose por tal la que para la realización de la actividad contratada no utiliza más equipos de trabajo propios que las herramientas manuales, incluidas las motorizadas portátiles, aunque cuenten con el apoyo de otros equipos de trabajo distintos de los señalados, siempre que éstos pertenezcan a otras empresas, contratistas o subcontratistas, de la obra.
3. No obstante lo dispuesto en el apartado anterior, cuando en casos fortuitos debidamente justificados, por exigencias de especialización de los trabajos, complicaciones técnicas de la producción o circunstancias de fuerza mayor por las que puedan atravesar los agentes que intervienen en la obra, fuera necesario, a juicio de la dirección facultativa, la contratación de alguna parte de la obra con terceros, excepcionalmente se podrá extender la subcontratación establecida en el apartado anterior en un nivel adicional, siempre que se haga constar por la dirección facultativa su aprobación previa y la causa o causas motivadoras de la misma en el Libro de Subcontratación al que se refiere el artículo 7 de esta Ley.

[2] Ley 32/2006, Artículo 3 (score 0.777)
Ley 32/2006, Artículo 3
g) Trabajador autónomo: la persona física distinta del contratista y del subcontratista, que realiza de forma personal y directa una actividad profesional, sin sujeción a un contrato de trabajo, y que asume contractualmente ante el promotor, el contratista o el subcontratista el compromiso de realizar determinadas partes o instalaciones de la obra. Cuando el trabajador autónomo emplee en la obra a trabajadores por cuenta ajena, tendrá la consideración de contratista o subcontratista a los efectos de la presente Ley.
h) Subcontratación: la práctica mercantil de organización productiva en virtud de la cual el contratista o subcontratista encarga a otro subcontratista o trabajador autónomo parte de lo que a él se le ha encomendado.
i) Nivel de subcontratación: cada uno de los escalones en que se estructura el proceso de subcontratación que se desarrolla para la ejecución de la totalidad o parte de la obra asumida contractualmente por el contratista con el promotor.

[3] Ley 32/2006, Preámbulo (score 0.768)
Ley 32/2006, Preámbulo
Hay que tener en cuenta que la contratación y subcontratación de obras o servicios es una expresión de la libertad de empresa que reconoce la Constitución Española en su artículo 38 y que, en el marco de una economía de mercado, cualquier forma de organización empresarial es lícita, siempre que no contraríe el ordenamiento jurídico. La subcontratación permite en muchos casos un mayor grado de especialización, de cualificación de los trabajadores y una más frecuente utilización de los medios técnicos que se emplean, lo que influye positivamente en la inversión en nueva tecnología. Además, esta forma de organización facilita la participación de las pequeñas y medianas empresas en la actividad de la construcción, lo que contribuye a la creación de empleo. Estos aspectos determinan una mayor eficiencia empresarial.
Sin embargo, el exceso en las cadenas de subcontratación, especialmente en este sector, además de no aportar ninguno de los elementos positivos desde el punto de vista de la eficiencia empresarial que se deriva de la mayor especialización y cualificación de los trabajadores, ocasiona, en no pocos casos, la participación de empresas sin una mínima estructura organizativa que permita garantizar que se hallan en condiciones de hacer frente a sus obligaciones de protección de la salud y la seguridad de los trabajadores, de tal forma que su participación en el encadenamiento sucesivo e injustificado de subcontrataciones opera en menoscabo de los márgenes empresariales y de la calidad de los servicios proporcionados de forma progresiva hasta el punto de que, en los últimos eslabones de la cadena, tales márgenes son prácticamente inexistentes, favoreciendo el trabajo sumergido, justo en el elemento final que ha de responder de las condiciones de seguridad y salud de los trabajadores que realizan las obras. Es por ello por lo que los indicados excesos de subcontratación pueden facilitar la aparición de prácticas incompatibles con la seguridad y salud en el trabajo.

[4] Ley 32/2006, Artículo 2 (score 0.766)
Ley 32/2006, Artículo 2
Artículo 2. Ámbito de aplicación.
La presente Ley será de aplicación a los contratos que se celebren, en régimen de subcontratación, para la ejecución de los siguientes trabajos realizados en obras de construcción:
Excavación; movimiento de tierras; construcción; montaje y desmontaje de elementos prefabricados; acondicionamientos o instalaciones; transformación; rehabilitación; reparación; desmantelamiento; derribo; mantenimiento; conservación y trabajos de pintura y limpieza; saneamiento.

[5] Ley 32/2006, Artículo 3 (score 0.763)
Ley 32/2006, Artículo 3
Artículo 3. Definiciones.
A efectos de esta Ley se entenderá por:
a) Obra de construcción u obra: cualquier obra, pública o privada, en la que se efectúen trabajos de construcción o de ingeniería civil.
b) Promotor: cualquier persona física o jurídica por cuenta de la cual se realice la obra.
c) Dirección facultativa: el técnico o técnicos competentes designados por el promotor, encargados de la dirección y del control de la ejecución de la obra.
d) Coordinador en materia de seguridad y de salud durante la ejecución de la obra: el técnico competente integrado en la dirección facultativa, designado por el promotor para llevar a cabo las tareas establecidas para este coordinador en la reglamentación de seguridad y salud en las obras de construcción.
e) Contratista o empresario principal: la persona física o jurídica, que asume contractualmente ante el promotor, con medios humanos y materiales, propios o ajenos, el compromiso de ejecutar la totalidad o parte de las obras con sujeción al proyecto y al contrato.
Cuando el promotor realice directamente con medios humanos y materiales propios la totalidad o determinadas partes de la obra, tendrá también la consideración de contratista a los efectos de la presente Ley; asimismo, cuando la contrata se haga con una Unión Temporal de Empresas, que no ejecute directamente la obra, cada una de sus empresas miembro tendrá la consideración de empresa contratista en la parte de obra que ejecute.
f) Subcontratista: la persona física o jurídica que asume contractualmente ante el contratista u otro subcontratista comitente el compromiso de realizar determinadas partes o unidades de obra, con sujeción al proyecto por el que se rige su ejecución. Las variantes de esta figura pueden ser las del primer subcontratista (subcontratista cuyo comitente es el contratista), segundo subcontratista (subcontratista cuyo comitente es el primer subcontratista), y así sucesivamente.

---
## q21 (single, dev)
**Question:** ¿De qué autoridad depende el Registro de Empresas Acreditadas y qué validez tiene la inscripción?
**Reference:** Depende de la autoridad laboral de la Comunidad Autónoma donde radique el domicilio social de la empresa, y la inscripción tiene validez en todo el territorio nacional.
**Answer:**

El Registro de Empresas Acreditadas depende de la **autoridad laboral competente**, entendiéndose por tal la correspondiente al territorio de la Comunidad Autónoma donde radique el domicilio social de la empresa contratista o subcontratista (Ley 32/2006, Artículo 6).

La inscripción en dicho registro tendrá **validez para todo el territorio nacional** (Ley 32/2006, Artículo 6).

Fuentes:
- Ley 32/2006, Artículo 6

*Nota: Esta información es de carácter divulgativo y no constituye asesoramiento legal.*

**Citations:** Ley 32/2006, Artículo 6 — all in retrieved text

**Coverage check:**

- Search 1 «Registro de Empresas Acreditadas autoridad validez inscripción»: **SÍ**, passage [1], quote: «1. A efectos de lo dispuesto en el artículo anterior, se creará el Registro de Empresas Acreditadas, que dependerá de la autoridad laboral competente, entendiéndose por tal la correspondiente al territorio de la Comunidad Autónoma donde radique el domicilio social de la empresa contratista o subcontratista.». Need: De qué autoridad depende el Registro de Empresas Acreditadas y qué validez tiene su inscripción

**Retrieved passages:**

[1] Ley 32/2006, Artículo 6 (score 0.826)
Ley 32/2006, Artículo 6
Artículo 6. Registro de Empresas Acreditadas.
1. A efectos de lo dispuesto en el artículo anterior, se creará el Registro de Empresas Acreditadas, que dependerá de la autoridad laboral competente, entendiéndose por tal la correspondiente al territorio de la Comunidad Autónoma donde radique el domicilio social de la empresa contratista o subcontratista.
2. La inscripción en el Registro de Empresas Acreditadas tendrá validez para todo el territorio nacional, siendo sus datos de acceso público con la salvedad de los referentes a la intimidad de las personas.
3. Reglamentariamente se establecerán el contenido, la forma y los efectos de la inscripción en dicho registro, así como los sistemas de coordinación de los distintos registros dependientes de las autoridades laborales autonómicas.

[2] Ley 32/2006, Artículo 4 (score 0.745)
Ley 32/2006, Artículo 4
Artículo 4. Requisitos exigibles a los contratistas y subcontratistas.
1. Para que una empresa pueda intervenir en el proceso de subcontratación en el sector de la construcción, como contratista o subcontratista, deberá:
a) Poseer una organización productiva propia, contar con los medios materiales y personales necesarios, y utilizarlos para el desarrollo de la actividad contratada.
b) Asumir los riesgos, obligaciones y responsabilidades propias del desarrollo de la actividad empresarial.
c) Ejercer directamente las facultades de organización y dirección sobre el trabajo desarrollado por sus trabajadores en la obra y, en el caso de los trabajadores autónomos, ejecutar el trabajo con autonomía y responsabilidad propia y fuera del ámbito de organización y dirección de la empresa que le haya contratado.
2. Además de los anteriores requisitos, las empresas que pretendan ser contratadas o subcontratadas para trabajos de una obra de construcción deberán también:
a) Acreditar que disponen de recursos humanos, en su nivel directivo y productivo, que cuentan con la formación necesaria en prevención de riesgos laborales, así como de una organización preventiva adecuada a la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales.
b) Estar inscritas en el Registro de Empresas Acreditadas al que se refiere el artículo 6 de esta Ley. La inscripción se realizará de oficio por la autoridad laboral competente, sobre la base de la declaración del empresario a que se refiere el apartado siguiente.
3. Las empresas contratistas o subcontratistas acreditarán el cumplimiento de los requisitos a que se refieren los apartados 1 y 2.a) de este artículo mediante una declaración suscrita por su representante legal formulada ante el Registro de Empresas Acreditadas.

[3] RD 39/1997, Artículo 24 (score 0.735)
RD 39/1997, Artículo 24
Artículo 24. Autoridad competente.
1. Será autoridad laboral competente para conocer de las solicitudes de acreditación formuladas por las entidades especializadas que pretendan actuar como servicios de prevención el órgano competente de la comunidad autónoma o de la Ciudad con Estatuto de Autonomía donde radiquen sus instalaciones principales. Esa misma autoridad laboral será competente para conocer, en su caso, de la revocación de la acreditación.
2. La acreditación otorgada será única y tendrá validez en todo el territorio español, conforme al procedimiento regulado a continuación.

[4] RD 39/1997, Artículo 28 (score 0.731)
RD 39/1997, Artículo 28
Artículo 28. Registro.
1. En los órganos competentes de las comunidades autónomas o de la Administración General del Estado, en el caso de las ciudades de Ceuta y de Melilla, se creará un registro en el que serán inscritas las entidades especializadas que hayan sido acreditadas como servicios de prevención, así como las personas o entidades especializadas a las que se haya concedido autorización para efectuar auditorías o evaluaciones de los sistemas de prevención de conformidad con lo establecido en el capítulo V.
2. La configuración de los registros deberá permitir que, con independencia de la autoridad laboral competente que haya expedido la acreditación:
a) Los ciudadanos puedan consultar las entidades especializadas acreditadas como servicios de prevención ajenos o entidades auditoras.
b) Las entidades especializadas puedan cumplir sus obligaciones de comunicación de datos relativos al cumplimiento de los requisitos de funcionamiento con las autoridades laborales competentes.
c) Las autoridades laborales, las autoridades sanitarias, la Inspección de Trabajo y Seguridad Social, el Instituto Nacional de Seguridad e Higiene en el Trabajo así como los órganos técnicos territoriales en materia de seguridad y salud en el trabajo puedan tener acceso a toda la información disponible sobre las entidades especializadas acreditadas como servicios de prevención ajenos o entidades auditoras, al margen de la autoridad que haya expedido la acreditación.
3. Los datos que obren en los Registros de las autoridades competentes, incluyendo las comunicaciones de datos relativos al cumplimiento de los requisitos de funcionamiento a que se refiere el artículo 26, se incorporarán a una base de datos general cuya gestión corresponderá a la Dirección General de Empleo del Ministerio de Empleo y Seguridad Social.
La configuración de esta base de datos deberá permitir a las comunidades autónomas que sus respectivos registros cumplan las funciones que se les atribuyen en el apartado 2.

[5] Ley 32/2006, Artículo 2 (score 0.715)
Ley 32/2006, Artículo 2
Artículo 2. Ámbito de aplicación.
La presente Ley será de aplicación a los contratos que se celebren, en régimen de subcontratación, para la ejecución de los siguientes trabajos realizados en obras de construcción:
Excavación; movimiento de tierras; construcción; montaje y desmontaje de elementos prefabricados; acondicionamientos o instalaciones; transformación; rehabilitación; reparación; desmantelamiento; derribo; mantenimiento; conservación y trabajos de pintura y limpieza; saneamiento.

---
## q22 (single, dev)
**Question:** ¿Cuándo debe revisarse la evaluación inicial de riesgos?
**Reference:** Cuando lo establezca una disposición específica; cuando se detecten daños a la salud o las actividades de prevención resulten inadecuadas o insuficientes; y con la periodicidad acordada entre la empresa y los representantes de los trabajadores.
**Answer:**

La evaluación inicial de riesgos deberá revisarse en los siguientes casos:

1. Cuando así lo establezca una disposición específica (RD 39/1997, Artículo 6).
2. En todo caso, respecto a los puestos de trabajo afectados, cuando se hayan detectado daños a la salud de los trabajadores o se haya apreciado —a través de los controles periódicos y la vigilancia de la salud— que las actividades de prevención son inadecuadas o insuficientes (RD 39/1997, Artículo 6).
3. Con la periodicidad que se acuerde entre la empresa y los representantes de los trabajadores, teniendo en cuenta el deterioro por el transcurso del tiempo de los elementos del proceso productivo (RD 39/1997, Artículo 6).
4. Asimismo, deberán volver a evaluarse los puestos que puedan verse afectados por:
   - La elección de equipos de trabajo, sustancias o preparados químicos, la introducción de nuevas tecnologías o la modificación en el acondicionamiento de los lugares de trabajo (RD 39/1997, Artículo 4).
   - Un cambio en las condiciones de trabajo (RD 39/1997, Artículo 4).
   - La incorporación de un trabajador cuyas características personales o estado biológico conocido lo hagan especialmente sensible a las condiciones del puesto (RD 39/1997, Artículo 4).

Fuentes utilizadas:
- RD 39/1997, Artículo 4 y Artículo 6.

**Citations:** RD 39/1997, Artículo 6; RD 39/1997, Artículo 4 — all in retrieved text

**Coverage check:**

- Search 1 «revision de la evaluacion inicial de riesgos»: **SÍ**, passage [1], quote: «1. La evaluación inicial a que se refiere el artículo 4 deberá revisarse cuando así lo establezca una disposición específica.». Need: cuándo debe revisarse la evaluación inicial de riesgos

**Retrieved passages:**

[1] RD 39/1997, Artículo 6 (score 0.787)
RD 39/1997, Artículo 6
Artículo 6. Revisión.
1. La evaluación inicial a que se refiere el artículo 4 deberá revisarse cuando así lo establezca una disposición específica.
En todo caso, se deberá revisar la evaluación correspondiente a aquellos puestos de trabajo afectados cuando se hayan detectado daños a la salud de los trabajadores o se haya apreciado a través de los controles periódicos, incluidos los relativos a la vigilancia de la salud, que las actividades de prevención pueden ser inadecuadas o insuficientes. Para ello se tendrán en cuenta los resultados de:
a) La investigación sobre las causas de los daños para la salud que se hayan producido.
b) Las actividades para la reducción de los riesgos a que se hace referencia en el apartado 1.a) del artículo 3.
c) Las actividades para el control de los riesgos a que se hace referencia en el apartado 1.b) del artículo 3.
d) El análisis de la situación epidemiológica según los datos aportados por el sistema de información sanitaria u otras fuentes disponibles.
2. Sin perjuicio de lo señalado en el apartado anterior, deberá revisarse igualmente la evaluación inicial con la periodicidad que se acuerde entre la empresa y los representantes de los trabajadores, teniendo en cuenta, en particular, el deterioro por el transcurso del tiempo de los elementos que integran el proceso productivo.

[2] RD 39/1997, Artículo 4 (score 0.742)
RD 39/1997, Artículo 4
Artículo 4. Contenido general de la evaluación.
1. La evaluación inicial de los riesgos que no hayan podido evitarse deberá extenderse a cada uno de los puestos de trabajo de la empresa en que concurran dichos riesgos.
Para ello, se tendrán en cuenta:
a) Las condiciones de trabajo existentes o previstas, tal como quedan definidas en el apartado 7 del artículo 4 de la Ley de Prevención de Riesgos Laborales.
b) La posibilidad de que el trabajador que lo ocupe o vaya a ocuparlo sea especialmente sensible, por sus características personales o estado biológico conocido, a alguna de dichas condiciones.
En particular, a efectos de lo dispuesto sobre la evaluación de riesgos en el artículo 26.1 de la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales, el anexo VII de este real decreto incluye una lista no exhaustiva de agentes, procedimientos y condiciones de trabajo que pueden influir negativamente en la salud de las trabajadoras embarazadas o en período de lactancia natural, del feto o del niño durante el período de lactancia natural, en cualquier actividad susceptible de presentar un riesgo específico de exposición.

[3] RD 39/1997, Artículo 4 (score 0.741)
RD 39/1997, Artículo 4
En todo caso la trabajadora embarazada no podrá realizar actividades que supongan riesgo de exposición a los agentes o condiciones de trabajo incluidos en la lista no exhaustiva de la parte A del anexo VIII, cuando, de acuerdo con las conclusiones obtenidas de la evaluación de riesgos, ello pueda poner en peligro su seguridad o su salud o la del feto. Igualmente la trabajadora en período de lactancia no podrá realizar actividades que supongan el riesgo de una exposición a los agentes o condiciones de trabajo enumerados en la lista no exhaustiva del anexo VIII, parte B, cuando de la evaluación se desprenda que ello pueda poner en peligro su seguridad o su salud o la del niño durante el período de lactancia natural. En los casos previstos en este párrafo, se adoptarán las medidas previstas en el artículo 26 de la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales, con el fin de evitar la exposición a los riesgos indicados.
2. A partir de dicha evaluación inicial, deberán volver a evaluarse los puestos de trabajo que puedan verse afectados por:
a) La elección de equipos de trabajo, sustancias o preparados químicos, la introducción de nuevas tecnologías o la modificación en el acondicionamiento de los lugares de trabajo.
b) El cambio en las condiciones de trabajo.
c) La incorporación de un trabajador cuyas características personales o estado biológico conocido lo hagan especialmente sensible a las condiciones del puesto.
3. La evaluación de los riesgos se realizará mediante la intervención de personal competente, de acuerdo con lo dispuesto en el capítulo VI de esta norma.

[4] RD 39/1997, Artículo 3 (score 0.74)
RD 39/1997, Artículo 3
Artículo 3. Definición.
1. La evaluación de los riesgos laborales es el proceso dirigido a estimar la magnitud de aquellos riesgos que no hayan podido evitarse, obteniendo la información necesaria para que el empresario esté en condiciones de tomar una decisión apropiada sobre la necesidad de adoptar medidas preventivas y, en tal caso, sobre el tipo de medidas que deben adoptarse.
Cuando de la evaluación realizada resulte necesaria la adopción de medidas preventivas, deberán ponerse claramente de manifiesto las situaciones en que sea necesario:
a) Eliminar o reducir el riesgo, mediante medidas de prevención en el origen, organizativas, de protección colectiva, de protección individual, o de formación e información a los trabajadores.
b) Controlar periódicamente las condiciones, la organización y los métodos de trabajo y el estado de salud de los trabajadores.
2. De acuerdo con lo previsto en el artículo 33 de la Ley de Prevención de Riesgos Laborales, el empresario deberá consultar a los representantes de los trabajadores, o a los propios trabajadores en ausencia de representantes, acerca del procedimiento de evaluación a utilizar en la empresa o centro de trabajo.

[5] Ley 31/1995, Artículo 16 (score 0.74)
Ley 31/1995, Artículo 16
Artículo 16. Plan de prevención de riesgos laborales, evaluación de los riesgos y planificación de la actividad preventiva
1. La prevención de riesgos laborales deberá integrarse en el sistema general de gestión de la empresa, tanto en el conjunto de sus actividades como en todos los niveles jerárquicos de ésta, a través de la implantación y aplicación de un plan de prevención de riesgos laborales a que se refiere el párrafo siguiente.
Este plan de prevención de riesgos laborales deberá incluir la estructura organizativa, las responsabilidades, las funciones, las prácticas, los procedimientos, los procesos y los recursos necesarios para realizar la acción de prevención de riesgos en la empresa, en los términos que reglamentariamente se establezcan.
2. Los instrumentos esenciales para la gestión y aplicación del plan de prevención de riesgos, que podrán ser llevados a cabo por fases de forma programada, son la evaluación de riesgos laborales y la planificación de la actividad preventiva a que se refieren los párrafos siguientes:
a) El empresario deberá realizar una evaluación inicial de los riesgos para la seguridad y salud de los trabajadores, teniendo en cuenta, con carácter general, la naturaleza de la actividad, las características de los puestos de trabajo existentes y de los trabajadores que deban desempeñarlos. Igual evaluación deberá hacerse con ocasión de la elección de los equipos de trabajo, de las sustancias o preparados químicos y del acondicionamiento de los lugares de trabajo. La evaluación inicial tendrá en cuenta aquellas otras actuaciones que deban desarrollarse de conformidad con lo dispuesto en la normativa sobre protección de riesgos específicos y actividades de especial peligrosidad. La evaluación será actualizada cuando cambien las condiciones de trabajo y, en todo caso, se someterá a consideración y se revisará, si fuera necesario, con ocasión de los daños para la salud que se hayan producido.
Cuando el resultado de la evaluación lo hiciera necesario, el empresario realizará controles periódicos de las condiciones de trabajo y de la actividad de los trabajadores en la prestación de sus servicios, para detectar situaciones potencialmente peligrosas.

---
## q23 (single, dev)
**Question:** ¿Qué datos deben reflejarse en la documentación de la evaluación de riesgos para cada puesto de trabajo?
**Reference:** La identificación del puesto, los riesgos existentes y los trabajadores afectados, el resultado de la evaluación y las medidas preventivas, y los criterios y métodos de evaluación utilizados cuando proceda.
**Answer:**

En la documentación de la evaluación de riesgos, para cada puesto de trabajo cuya evaluación ponga de manifiesto la necesidad de tomar alguna medida preventiva, deben reflejarse los siguientes datos (RD 39/1997, Artículo 7):

a) La identificación del puesto de trabajo.
b) El riesgo o riesgos existentes y la relación de trabajadores afectados.
c) El resultado de la evaluación y las medidas preventivas procedentes (teniendo en cuenta lo establecido en el artículo 3 del mismo real decreto).
d) La referencia de los criterios y procedimientos de evaluación y de los métodos de medición, análisis o ensayo utilizados, en los casos en que sea de aplicación lo dispuesto en el artículo 5.3 del mismo real decreto.

Fuentes utilizadas:
- RD 39/1997, Artículo 7.

*Nota: Esta información es de carácter divulgativo y no constituye asesoramiento jurídico.*

**Citations:** RD 39/1997, Artículo 7 — all in retrieved text

**Coverage check:**

- Search 1 «datos evaluación de riesgos puesto de trabajo»: **SÍ**, passage [1], quote: «En la documentación a que hacen referencia los párrafos b) y c) del artículo 23.1 de la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales, deberán reflejarse, para cada puesto de trabajo cuya evaluación ponga de manifiesto la necesidad de tomar alguna medida preventiva, los siguientes datos:». Need: los datos específicos que deben reflejarse en la documentación de la evaluación de riesgos para cada puesto de trabajo

**Retrieved passages:**

[1] RD 39/1997, Artículo 7 (score 0.744)
RD 39/1997, Artículo 7
Artículo 7. Documentación.
En la documentación a que hacen referencia los párrafos b) y c) del artículo 23.1 de la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales, deberán reflejarse, para cada puesto de trabajo cuya evaluación ponga de manifiesto la necesidad de tomar alguna medida preventiva, los siguientes datos:
a) La identificación del puesto de trabajo.
b) El riesgo o riesgos existentes y la relación de trabajadores afectados.
c) El resultado de la evaluación y las medidas preventivas procedentes, teniendo en cuenta lo establecido en el artículo 3.
d) La referencia de los criterios y procedimientos de evaluación y de los métodos de medición, análisis o ensayo utilizados, en los casos en que sea de aplicación lo dispuesto en el apartado 3 del artículo 5.

[2] RD 39/1997, Artículo 5 (score 0.731)
RD 39/1997, Artículo 5
Artículo 5. Procedimiento.
1. A partir de la información obtenida sobre la organización, características y complejidad del trabajo, sobre las materias primas y los equipos de trabajo existentes en la empresa y sobre el estado de salud de los trabajadores, se procederá a la determinación de los elementos peligrosos y a la identificación de los trabajadores expuestos a los mismos, valorando a continuación el riesgo existente en función de criterios objetivos de valoración, según los conocimientos técnicos existentes, o consensuados con los trabajadores, de manera que se pueda llegar a una conclusión sobre la necesidad de evitar o de controlar y reducir el riesgo.
A los efectos previstos en el párrafo anterior se tendrá en cuenta la información recibida de los trabajadores sobre los aspectos señalados.
2. El procedimiento de evaluación utilizado deberá proporcionar confianza sobre su resultado. En caso de duda deberán adoptarse las medidas preventivas más favorables, desde el punto de vista de la prevención.
La evaluación incluirá la realización de las mediciones, análisis o ensayos que se consideren necesarios, salvo que se trate de operaciones, actividades o procesos en los que la directa apreciación profesional acreditada permita llegar a una conclusión sin necesidad de recurrir a aquéllos, siempre que se cumpla lo dispuesto en el párrafo anterior.
En cualquier caso, si existiera normativa específica de aplicación, el procedimiento de evaluación deberá ajustarse a las condiciones concretas establecidas en la misma.
3. Cuando la evaluación exija la realización de mediciones, análisis o ensayos y la normativa no indique o concrete los métodos que deben emplearse, o cuando los criterios de evaluación contemplados en dicha normativa deban ser interpretados o precisados a la luz de otros criterios de carácter técnico, se podrán utilizar, si existen, los métodos o criterios recogidos en:
a) Normas UNE.
b) Guías del Instituto Nacional de Seguridad e Higiene en el Trabajo, del Instituto Nacional de Silicosis y protocolos y guías del Ministerio de Sanidad y Consumo, así como de Instituciones competentes de las Comunidades Autónomas.
c) Normas internacionales.

[3] RD 39/1997, Artículo 4 (score 0.73)
RD 39/1997, Artículo 4
Artículo 4. Contenido general de la evaluación.
1. La evaluación inicial de los riesgos que no hayan podido evitarse deberá extenderse a cada uno de los puestos de trabajo de la empresa en que concurran dichos riesgos.
Para ello, se tendrán en cuenta:
a) Las condiciones de trabajo existentes o previstas, tal como quedan definidas en el apartado 7 del artículo 4 de la Ley de Prevención de Riesgos Laborales.
b) La posibilidad de que el trabajador que lo ocupe o vaya a ocuparlo sea especialmente sensible, por sus características personales o estado biológico conocido, a alguna de dichas condiciones.
En particular, a efectos de lo dispuesto sobre la evaluación de riesgos en el artículo 26.1 de la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales, el anexo VII de este real decreto incluye una lista no exhaustiva de agentes, procedimientos y condiciones de trabajo que pueden influir negativamente en la salud de las trabajadoras embarazadas o en período de lactancia natural, del feto o del niño durante el período de lactancia natural, en cualquier actividad susceptible de presentar un riesgo específico de exposición.

[4] Ley 31/1995, Artículo 16 (score 0.729)
Ley 31/1995, Artículo 16
Artículo 16. Plan de prevención de riesgos laborales, evaluación de los riesgos y planificación de la actividad preventiva
1. La prevención de riesgos laborales deberá integrarse en el sistema general de gestión de la empresa, tanto en el conjunto de sus actividades como en todos los niveles jerárquicos de ésta, a través de la implantación y aplicación de un plan de prevención de riesgos laborales a que se refiere el párrafo siguiente.
Este plan de prevención de riesgos laborales deberá incluir la estructura organizativa, las responsabilidades, las funciones, las prácticas, los procedimientos, los procesos y los recursos necesarios para realizar la acción de prevención de riesgos en la empresa, en los términos que reglamentariamente se establezcan.
2. Los instrumentos esenciales para la gestión y aplicación del plan de prevención de riesgos, que podrán ser llevados a cabo por fases de forma programada, son la evaluación de riesgos laborales y la planificación de la actividad preventiva a que se refieren los párrafos siguientes:
a) El empresario deberá realizar una evaluación inicial de los riesgos para la seguridad y salud de los trabajadores, teniendo en cuenta, con carácter general, la naturaleza de la actividad, las características de los puestos de trabajo existentes y de los trabajadores que deban desempeñarlos. Igual evaluación deberá hacerse con ocasión de la elección de los equipos de trabajo, de las sustancias o preparados químicos y del acondicionamiento de los lugares de trabajo. La evaluación inicial tendrá en cuenta aquellas otras actuaciones que deban desarrollarse de conformidad con lo dispuesto en la normativa sobre protección de riesgos específicos y actividades de especial peligrosidad. La evaluación será actualizada cuando cambien las condiciones de trabajo y, en todo caso, se someterá a consideración y se revisará, si fuera necesario, con ocasión de los daños para la salud que se hayan producido.
Cuando el resultado de la evaluación lo hiciera necesario, el empresario realizará controles periódicos de las condiciones de trabajo y de la actividad de los trabajadores en la prestación de sus servicios, para detectar situaciones potencialmente peligrosas.

[5] RD 39/1997, Artículo 3 (score 0.729)
RD 39/1997, Artículo 3
Artículo 3. Definición.
1. La evaluación de los riesgos laborales es el proceso dirigido a estimar la magnitud de aquellos riesgos que no hayan podido evitarse, obteniendo la información necesaria para que el empresario esté en condiciones de tomar una decisión apropiada sobre la necesidad de adoptar medidas preventivas y, en tal caso, sobre el tipo de medidas que deben adoptarse.
Cuando de la evaluación realizada resulte necesaria la adopción de medidas preventivas, deberán ponerse claramente de manifiesto las situaciones en que sea necesario:
a) Eliminar o reducir el riesgo, mediante medidas de prevención en el origen, organizativas, de protección colectiva, de protección individual, o de formación e información a los trabajadores.
b) Controlar periódicamente las condiciones, la organización y los métodos de trabajo y el estado de salud de los trabajadores.
2. De acuerdo con lo previsto en el artículo 33 de la Ley de Prevención de Riesgos Laborales, el empresario deberá consultar a los representantes de los trabajadores, o a los propios trabajadores en ausencia de representantes, acerca del procedimiento de evaluación a utilizar en la empresa o centro de trabajo.

---
## q24 (single, dev)
**Question:** ¿Quién debe facilitar una copia del plan de seguridad y salud a los representantes de los trabajadores?
**Reference:** El contratista, a los representantes de los trabajadores en el centro de trabajo.
**Answer:**

El **contratista** debe facilitar una copia del plan de seguridad y salud (y de sus posibles modificaciones) a los representantes de los trabajadores en el centro de trabajo, a efectos de su conocimiento y seguimiento (RD 1627/1997, Artículo 16).

Fuentes utilizadas:
- RD 1627/1997, Artículo 16.

*(Esta información es de carácter orientativo e informativo y no constituye asesoramiento jurídico).*

**Citations:** RD 1627/1997, Artículo 16 — all in retrieved text

**Coverage check:**

- Search 1 «copia plan de seguridad y salud representantes de los trabajadores»: **SÍ**, passage [1], quote: «3. Una copia del plan de seguridad y salud y de sus posibles modificaciones, en los términos previstos en el apartado 4 del artículo 7, a efectos de su conocimiento y seguimiento, será facilitada por el contratista a los representantes de los trabajadores en el centro de trabajo.». Need: Quién debe facilitar una copia del plan de seguridad y salud a los representantes de los trabajadores

**Retrieved passages:**

[1] RD 1627/1997, Artículo 16 (score 0.769)
RD 1627/1997, Artículo 16
Artículo 16. Consulta y participación de los trabaja dores.
1. La consulta y participación de los trabajadores o sus representantes se realizarán, de conformidad con lo dispuesto en el apartado 2 del artículo 18 de la Ley de Prevención de Riesgos Laborales, sobre las cuestiones a las que se refiere el presente Real Decreto.
2. Cuando sea necesario, teniendo en cuenta el nivel de riesgo y la importancia de la obra, la consulta y participación de los trabajadores o sus representantes en las empresas que ejerzan sus actividades en el lugar de trabajo deberá desarrollarse con la adecuada coordinación de conformidad con el apartado 3 del ar tículo 39 de la Ley de Prevención de Riesgos Laborales.
3. Una copia del plan de seguridad y salud y de sus posibles modificaciones, en los términos previstos en el apartado 4 del artículo 7, a efectos de su conocimiento y seguimiento, será facilitada por el contratista a los representantes de los trabajadores en el centro de trabajo.

[2] Ley 31/1995, Artículo 39 (score 0.757)
Ley 31/1995, Artículo 39
Artículo 39. Competencias y facultades del Comité de Seguridad y Salud.
1. El Comité de Seguridad y Salud tendrá las siguientes competencias:
a) Participar en la elaboración, puesta en práctica y evaluación de los planes y programas de prevención de riesgos de la empresa. A tal efecto, en su seno se debatirán, antes de su puesta en práctica y en lo referente a su incidencia en la prevención de riesgos, la elección de la modalidad organizativa de la empresa y, en su caso, la gestión realizada por las entidades especializadas con las que la empresa hubiera concertado la realización de actividades preventivas; los proyectos en materia de planificación, organización del trabajo e introducción de nuevas tecnologías, organización y desarrollo de las actividades de protección y prevención a que se refiere el artículo 16 de esta Ley y proyecto y organización de la formación en materia preventiva.
b) Promover iniciativas sobre métodos y procedimientos para la efectiva prevención de los riesgos, proponiendo a la empresa la mejora de las condiciones o la corrección de las deficiencias existentes.
2. En el ejercicio de sus competencias, el Comité de Seguridad y Salud estará facultado para:
a) Conocer directamente la situación relativa a la prevención de riesgos en el centro de trabajo, realizando a tal efecto las visitas que estime oportunas.
b) Conocer cuantos documentos e informes relativos a las condiciones de trabajo sean necesarios para el cumplimiento de sus funciones, así como los procedentes de la actividad del servicio de prevención, en su caso.
c) Conocer y analizar los daños producidos en la salud o en la integridad física de los trabajadores, al objeto de valorar sus causas y proponer las medidas preventivas oportunas.
d) Conocer e informar la memoria y programación anual de servicios de prevención.

[3] Ley 31/1995, Artículo 34 (score 0.751)
Ley 31/1995, Artículo 34
Artículo 34. Derechos de participación y representación.
1. Los trabajadores tienen derecho a participar en la empresa en las cuestiones relacionadas con la prevención de riesgos en el trabajo.
En las empresas o centros de trabajo que cuenten con seis o más trabajadores, la participación de éstos se canalizará a través de sus representantes y de la representación especializada que se regula en este capítulo.
2. A los Comités de Empresa, a los Delegados de Personal y a los representantes sindicales les corresponde, en los términos que, respectivamente, les reconocen el Estatuto de los Trabajadores, la Ley de Organos de Representación del Personal al Servicio de las Administraciones Públicas y la Ley Orgánica de Libertad Sindical, la defensa de los intereses de los trabajadores en materia de prevención de riesgos en el trabajo. Para ello, los representantes del personal ejercerán las competencias que dichas normas establecen en materia de información, consulta y negociación, vigilancia y control y ejercicio de acciones ante las empresas y los órganos y tribunales competentes.
3. El derecho de participación que se regula en este capítulo se ejercerá en el ámbito de las Administraciones públicas con las adaptaciones que procedan en atención a la diversidad de las actividades que desarrollan y las diferentes condiciones en que éstas se realizan, la complejidad y dispersión de su estructura organizativa y sus peculiaridades en materia de representación colectiva, en los términos previstos en la Ley 7/1990, de 19 de julio, sobre negociación colectiva y participación en la determinación de las condiciones de trabajo de los empleados públicos, pudiéndose establecer ámbitos sectoriales y descentralizados en función del número de efectivos y centros.
Para llevar a cabo la indicada adaptación en el ámbito de la Administración General del Estado, el Gobierno tendrá en cuenta los siguientes criterios:
a) En ningún caso dicha adaptación podrá afectar a las competencias, facultades y garantías que se reconocen en esta Ley a los Delegados de Prevención y a los Comités de Seguridad y Salud.

[4] Ley 31/1995, Artículo 38 (score 0.749)
Ley 31/1995, Artículo 38
Artículo 38. Comité de Seguridad y Salud.
1. El Comité de Seguridad y Salud es el órgano paritario y colegiado de participación destinado a la consulta regular y periódica de las actuaciones de la empresa en materia de prevención de riesgos.
2. Se constituirá un Comité de Seguridad y Salud en todas las empresas o centros de trabajo que cuenten con 50 o más trabajadores.
El Comité estará formado por los Delegados de Prevención, de una parte, y por el empresario y/o sus representantes en número igual al de los Delegados de Prevención, de la otra.
En las reuniones del Comité de Seguridad y Salud participarán, con voz pero sin voto, los Delegados Sindicales y los responsables técnicos de la prevención en la empresa que no estén incluidos en la composición a la que se refiere el párrafo anterior. En las mismas condiciones podrán participar trabajadores de la empresa que cuenten con una especial cualificación o información respecto de concretas cuestiones que se debatan en este órgano y técnicos en prevención ajenos a la empresa, siempre que así lo solicite alguna de las representaciones en el Comité.
3. El Comité de Seguridad y Salud se reunirá trimestralmente y siempre que lo solicite alguna de las representaciones en el mismo. El Comité adoptará sus propias normas de funcionamiento.
Las empresas que cuenten con varios centros de trabajo dotados de Comité de Seguridad y Salud podrán acordar con sus trabajadores la creación de un Comité Intercentros, con las funciones que el acuerdo le atribuya.

[5] RD 1627/1997, Artículo 7 (score 0.748)
RD 1627/1997, Artículo 7
4. El plan de seguridad y salud podrá ser modificado por el contratista en función del proceso de ejecución de la obra, de la evolución de los trabajos y de las posibles incidencias o modificaciones que puedan surgir a lo largo de la obra, pero siempre con la aprobación expresa en los términos del apartado 2. Quienes intervengan en la ejecución de la obra, así como las personas u órganos con responsabilidades en materia de prevención en las empresas intervinientes en la misma y los representantes de los trabajadores, podrán presentar, por escrito y de forma razonada, las sugerencias y alternativas que estimen oportunas. A tal efecto, el plan de seguridad y salud estará en la obra a disposición permanente de los mismos.
5. Asimismo, el plan de seguridad y salud estará en la obra a disposición permanente de la dirección facultativa.

---
## q25 (multi, dev)
**Question:** ¿Qué obligación tienen los contratistas de una obra sobre coordinación de actividades empresariales y en qué consiste esa coordinación?
**Reference:** Deben cumplir la normativa preventiva teniendo en cuenta la coordinación de actividades del artículo 24 de la Ley 31/1995; las empresas que coinciden en un mismo centro de trabajo deben cooperar y establecer los medios de coordinación necesarios.
**Answer:**

En relación con las obras de construcción, los contratistas tienen la obligación de cumplir la normativa de prevención de riesgos laborales teniendo en cuenta las obligaciones sobre **coordinación de actividades empresariales (CAE)** previstas en el artículo 24 de la Ley 31/1995 de Prevención de Riesgos Laborales (RD 1627/1997, Artículo 11).

Asimismo, entre las funciones del coordinador en materia de seguridad y salud durante la ejecución de la obra figura **organizar la coordinación de actividades empresariales** prevista en dicho artículo 24 (RD 1627/1997, Artículo 9), y los contratistas y subcontratistas están obligados a atender las indicaciones y cumplir las instrucciones de dicho coordinador o de la dirección facultativa (RD 1627/1997, Artículo 11).

En cuanto a **en qué consiste** dicha coordinación (según el artículo 24 de la Ley 31/1995), comprende:

1. **Cooperación:** Cuando en un mismo centro de trabajo desarrollen actividades trabajadores de dos o más empresas, éstas deben cooperar en la aplicación de la normativa de prevención de riesgos laborales, estableciendo para ello los medios de coordinación necesarios en cuanto a la protección y prevención de riesgos laborales y la información sobre los mismos a sus respectivos trabajadores (Ley 31/1995, Artículo 24).
2. **Información, instrucciones y vigilancia (si procede):** Las empresas contratistas o subcontratistas que contraten la realización de obras o servicios correspondientes a su propia actividad en sus propios centros de trabajo deben vigilar el cumplimiento de la normativa de prevención por parte de las contratas y subcontratas (Ley 31/1995, Artículo 24).
3. **Aplicación a autónomos:** Los deberes de cooperación, información e instrucción también son de aplicación respecto de los trabajadores autónomos que desarrollen actividades en el centro de trabajo (Ley 31/1995, Artículo 24), debiendo además los contratistas informar y proporcionar las instrucciones adecuadas a los trabajadores autónomos sobre las medidas que hayan de adoptarse en cuanto a su seguridad y salud en la obra (RD 1627/1997, Artículo 11).

*Nota: Esta información es meramente divulgativa y se basa estrictamente en los textos legales del corpus.*

Fuentes utilizadas:
- Ley 31/1995, Artículo 24.
- RD 1627/1997, Artículo 9 y Artículo 11.

**Citations:** RD 1627/1997, Artículo 11; RD 1627/1997, Artículo 9; Ley 31/1995, Artículo 24 — all in retrieved text

**Coverage check:**

- Search 1 «contratistas coordinacion de actividades empresariales obra»: **SÍ**, passage [5], quote: «c) Cumplir la normativa en materia de prevención de riesgos laborales, teniendo en cuenta, en su caso, las obligaciones sobre coordinación de actividades empresariales previstas en el artículo 24 de la Ley de Prevención de Riesgos Laborales, así como cumplir las disposiciones mínimas establecidas en el anexo IV del presente Real Decreto, durante la ejecución de la obra.». Need: qué obligación tienen los contratistas de una obra sobre coordinación de actividades empresariales y en qué consiste esa coordinación
- Search 2 «RD 1627 1997 contratistas obligaciones coordinacion actividades empresariales»: **SÍ**, passage [2], quote: «c) Cumplir la normativa en materia de prevención de riesgos laborales, teniendo en cuenta, en su caso, las obligaciones sobre coordinación de actividades empresariales previstas en el artículo 24 de la Ley de Prevención de Riesgos Laborales, así como cumplir las disposiciones mínimas establecidas en el anexo IV del presente Real Decreto, durante la ejecución de la obra.». Need: qué obligación tienen los contratistas de una obra sobre coordinación de actividades empresariales y en qué consiste esa coordinación

**Retrieved passages:**

[1] Ley 31/1995, Artículo 24 (score 0.771)
Ley 31/1995, Artículo 24
Artículo 24. Coordinación de actividades empresariales.
1. Cuando en un mismo centro de trabajo desarrollen actividades trabajadores de dos o más empresas, éstas deberán cooperar en la aplicación de la normativa sobre prevención de riesgos laborales. A tal fin, establecerán los medios de coordinación que sean necesarios en cuanto a la protección y prevención de riesgos laborales y la información sobre los mismos a sus respectivos trabajadores, en los términos previstos en el apartado 1 del artículo 18 de esta Ley.
2. El empresario titular del centro de trabajo adoptará las medidas necesarias para que aquellos otros empresarios que desarrollen actividades en su centro de trabajo reciban la información y las instrucciones adecuadas, en relación con los riesgos existentes en el centro de trabajo y con las medidas de protección y prevención correspondientes, así como sobre las medidas de emergencia a aplicar, para su traslado a sus respectivos trabajadores.
3. Las empresas que contraten o subcontraten con otras la realización de obras o servicios correspondientes a la propia actividad de aquéllas y que se desarrollen en sus propios centros de trabajo deberán vigilar el cumplimiento por dichos contratistas y subcontratistas de la normativa de prevención de riesgos laborales.
4. Las obligaciones consignadas en el último párrafo del apartado 1 del artículo 41 de esta Ley serán también de aplicación, respecto de las operaciones contratadas, en los supuestos en que los trabajadores de la empresa contratista o subcontratista no presten servicios en los centros de trabajo de la empresa principal, siempre que tales trabajadores deban operar con maquinaria, equipos, productos, materias primas o útiles proporcionados por la empresa principal.
5. Los deberes de cooperación y de información e instrucción recogidos en los apartados 1 y 2 serán de aplicación respecto de los trabajadores autónomos que desarrollen actividades en dichos centros de trabajo.
6. Las obligaciones previstas en este artículo serán desarrolladas reglamentariamente.

[2] Ley 32/2006, Artículo 3 (score 0.745)
Ley 32/2006, Artículo 3
Artículo 3. Definiciones.
A efectos de esta Ley se entenderá por:
a) Obra de construcción u obra: cualquier obra, pública o privada, en la que se efectúen trabajos de construcción o de ingeniería civil.
b) Promotor: cualquier persona física o jurídica por cuenta de la cual se realice la obra.
c) Dirección facultativa: el técnico o técnicos competentes designados por el promotor, encargados de la dirección y del control de la ejecución de la obra.
d) Coordinador en materia de seguridad y de salud durante la ejecución de la obra: el técnico competente integrado en la dirección facultativa, designado por el promotor para llevar a cabo las tareas establecidas para este coordinador en la reglamentación de seguridad y salud en las obras de construcción.
e) Contratista o empresario principal: la persona física o jurídica, que asume contractualmente ante el promotor, con medios humanos y materiales, propios o ajenos, el compromiso de ejecutar la totalidad o parte de las obras con sujeción al proyecto y al contrato.
Cuando el promotor realice directamente con medios humanos y materiales propios la totalidad o determinadas partes de la obra, tendrá también la consideración de contratista a los efectos de la presente Ley; asimismo, cuando la contrata se haga con una Unión Temporal de Empresas, que no ejecute directamente la obra, cada una de sus empresas miembro tendrá la consideración de empresa contratista en la parte de obra que ejecute.
f) Subcontratista: la persona física o jurídica que asume contractualmente ante el contratista u otro subcontratista comitente el compromiso de realizar determinadas partes o unidades de obra, con sujeción al proyecto por el que se rige su ejecución. Las variantes de esta figura pueden ser las del primer subcontratista (subcontratista cuyo comitente es el contratista), segundo subcontratista (subcontratista cuyo comitente es el primer subcontratista), y así sucesivamente.

[3] Ley 32/2006, Artículo 2 (score 0.744)
Ley 32/2006, Artículo 2
Artículo 2. Ámbito de aplicación.
La presente Ley será de aplicación a los contratos que se celebren, en régimen de subcontratación, para la ejecución de los siguientes trabajos realizados en obras de construcción:
Excavación; movimiento de tierras; construcción; montaje y desmontaje de elementos prefabricados; acondicionamientos o instalaciones; transformación; rehabilitación; reparación; desmantelamiento; derribo; mantenimiento; conservación y trabajos de pintura y limpieza; saneamiento.

[4] RD 1627/1997, Artículo 3 (score 0.743)
RD 1627/1997, Artículo 3
Artículo 3. Designación de los coordinadores en materia de seguridad y salud.
1. En las obras incluidas en el ámbito de aplicación del presente Real Decreto, cuando en la elaboración del proyecto de obra intervengan varios proyectistas, el promotor designará un coordinador en materia de seguridad y de salud durante la elaboración del proyecto de obra.
2. Cuando en la ejecución de la obra intervenga más de una empresa, o una empresa y trabajadores autónomos o diversos trabajadores autónomos, el promotor, antes del inicio de los trabajos o tan pronto como se constate dicha circunstancia, designará un coordinador en materia de seguridad y salud durante la ejecución de la obra.
3. La designación de los coordinadores en materia de seguridad y salud durante la elaboración del proyecto de obra y durante la ejecución de la obra podrá recaer en la misma persona.
4. La designación de los coordinadores no eximirá al promotor de sus responsabilidades.

[5] RD 1627/1997, Artículo 11 (score 0.734)
RD 1627/1997, Artículo 11
Artículo 11. Obligaciones de los contratistas y subcontratistas.
1. Los contratistas y subcontratistas estarán obligados a:
a) Aplicar los principios de la acción preventiva que se recogen en el artículo 15 de la Ley de Prevención de Riesgos Laborales, en particular al desarrollar las tareas o actividades indicadas en el artículo 10 del presente Real Decreto.
b) Cumplir y hacer cumplir a su personal lo establecido en el plan de seguridad y salud al que se refiere el artículo 7.
c) Cumplir la normativa en materia de prevención de riesgos laborales, teniendo en cuenta, en su caso, las obligaciones sobre coordinación de actividades empresariales previstas en el artículo 24 de la Ley de Prevención de Riesgos Laborales, así como cumplir las disposiciones mínimas establecidas en el anexo IV del presente Real Decreto, durante la ejecución de la obra.
d) Informar y proporcionar las instrucciones adecuadas a los trabajadores autónomos sobre todas las medidas que hayan de adoptarse en lo que se refiere a su seguridad y salud en la obra.
e) Atender las indicaciones y cumplir las instrucciones del coordinador en materia de seguridad y de salud durante la ejecución de la obra o, en su caso, de la dirección facultativa.
2. Los contratistas y los subcontratistas serán responsables de la ejecución correcta de las medidas preventivas fijadas en el plan de seguridad y salud en lo relativo a las obligaciones que les correspondan a ellos directamente o, en su caso, a los trabajadores autónomos por ellos contratados.
Además, los contratistas y los subcontratistas responderán solidariamente de las consecuencias que se deriven del incumplimiento de las medidas previstas en el plan, en los términos del apartado 2 del artículo 42 de la Ley de Prevención de Riesgos Laborales.
3. Las responsabilidades de los coordinadores, de la dirección facultativa y del promotor no eximirán de sus responsabilidades a los contratistas y a los subcontratistas.

[1] RD 1627/1997, Artículo 3 (score 0.796)
RD 1627/1997, Artículo 3
Artículo 3. Designación de los coordinadores en materia de seguridad y salud.
1. En las obras incluidas en el ámbito de aplicación del presente Real Decreto, cuando en la elaboración del proyecto de obra intervengan varios proyectistas, el promotor designará un coordinador en materia de seguridad y de salud durante la elaboración del proyecto de obra.
2. Cuando en la ejecución de la obra intervenga más de una empresa, o una empresa y trabajadores autónomos o diversos trabajadores autónomos, el promotor, antes del inicio de los trabajos o tan pronto como se constate dicha circunstancia, designará un coordinador en materia de seguridad y salud durante la ejecución de la obra.
3. La designación de los coordinadores en materia de seguridad y salud durante la elaboración del proyecto de obra y durante la ejecución de la obra podrá recaer en la misma persona.
4. La designación de los coordinadores no eximirá al promotor de sus responsabilidades.

[2] RD 1627/1997, Artículo 11 (score 0.79)
RD 1627/1997, Artículo 11
Artículo 11. Obligaciones de los contratistas y subcontratistas.
1. Los contratistas y subcontratistas estarán obligados a:
a) Aplicar los principios de la acción preventiva qu

---
## q26 (multi, dev)
**Question:** ¿Qué información sobre seguridad y salud deben recibir los trabajadores de una obra y quién debe garantizarla?
**Reference:** Contratistas y subcontratistas deben garantizar una información adecuada y comprensible sobre las medidas de seguridad y salud en la obra; el empresario debe informar de los riesgos y medidas de prevención, y directamente a cada trabajador de los riesgos específicos de su puesto.
**Answer:**

Según la normativa aplicable en las obras de construcción:

* **Quién debe garantizarla:** Los **contratistas y subcontratistas** deberán garantizar que los trabajadores reciban la información adecuada (RD 1627/1997, Artículo 15).
* **Qué información deben recibir:** Los trabajadores deben recibir una información adecuada de **todas las medidas que hayan de adoptarse en lo que se refiere a su seguridad y su salud en la obra** (RD 1627/1997, Artículo 15). Dicha información deberá ser **comprensible** para los trabajadores afectados (RD 1627/1997, Artículo 15) y se ajustará a lo dispuesto en el artículo 18 de la Ley de Prevención de Riesgos Laborales (Ley 31/1995, Artículo 18), que incluye los riesgos para la seguridad y la salud en el trabajo (tanto generales de la empresa como específicos del puesto o función) y las medidas y actividades de protección y prevención aplicables.

*Nota: Esta información se proporciona a título informativo y no constituye asesoramiento legal.*

**Fuentes utilizadas:**
* RD 1627/1997, Artículo 15.
* Ley 31/1995, Artículo 18.

**Citations:** RD 1627/1997, Artículo 15; Ley 31/1995, Artículo 18 — all in retrieved text

**Coverage check:**

- Search 1 «informacion trabajadores seguridad y salud obra»: **SÍ**, passage [1], quote: «1. De conformidad con el artículo 18 de la Ley de Prevención de Riesgos Laborales, los contratistas y subcontratistas deberán garantizar que los trabajadores reciban una información adecuada de todas las medidas que hayan de adoptarse en lo que se refiere a su seguridad y su salud en la obra.». Need: qué información sobre seguridad y salud deben recibir los trabajadores de una obra y quién debe garantizarla

**Retrieved passages:**

[1] RD 1627/1997, Artículo 15 (score 0.756)
RD 1627/1997, Artículo 15
Artículo 15. Información a los trabajadores.
1. De conformidad con el artículo 18 de la Ley de Prevención de Riesgos Laborales, los contratistas y subcontratistas deberán garantizar que los trabajadores reciban una información adecuada de todas las medidas que hayan de adoptarse en lo que se refiere a su seguridad y su salud en la obra.
2. La información deberá ser comprensible para los trabajadores afectados.

[2] RD 1627/1997, Artículo 19 (score 0.739)
RD 1627/1997, Artículo 19
Artículo 19. Información a la autoridad laboral.
1. La comunicación de apertura del centro de trabajo a la autoridad laboral competente deberá ser previa al comienzo de los trabajos y se presentará únicamente por los empresarios que tengan la consideración de contratistas de acuerdo con lo dispuesto en este real decreto.
La comunicación de apertura incluirá el plan de seguridad y salud al que se refiere el artículo 7 del presente real decreto.
2. El plan de seguridad y salud estará a disposición permanente de la Inspección de Trabajo y Seguridad Social y de los técnicos de los órganos especializados en materia de seguridad y salud en las Administraciones públicas competentes.

[3] Ley 31/1995, Artículo 18 (score 0.729)
Ley 31/1995, Artículo 18
Artículo 18. Información, consulta y participación de los trabajadores.
1. A fin de dar cumplimiento al deber de protección establecido en la presente Ley, el empresario adoptará las medidas adecuadas para que los trabajadores reciban todas las informaciones necesarias en relación con:
a) Los riesgos para la seguridad y la salud de los trabajadores en el trabajo, tanto aquellos que afecten a la empresa en su conjunto como a cada tipo de puesto de trabajo o función.
b) Las medidas y actividades de protección y prevención aplicables a los riesgos señalados en el apartado anterior.
c) Las medidas adoptadas de conformidad con lo dispuesto en el artículo 20 de la presente Ley.
En las empresas que cuenten con representantes de los trabajadores, la información a que se refiere el presente apartado se facilitará por el empresario a los trabajadores a través de dichos representantes; no obstante, deberá informarse directamente a cada trabajador de los riesgos específicos que afecten a su puesto de trabajo o función y de las medidas de protección y prevención aplicables a dichos riesgos.
2. El empresario deberá consultar a los trabajadores, y permitir su participación, en el marco de todas las cuestiones que afecten a la seguridad y a la salud en el trabajo, de conformidad con lo dispuesto en el capítulo V de la presente Ley.
Los trabajadores tendrán derecho a efectuar propuestas al empresario, así como a los órganos de participación y representación previstos en el capítulo V de esta Ley, dirigidas a la mejora de los niveles de protección de la seguridad y la salud en la empresa.

[4] Ley 32/2006, Artículo 9 (score 0.728)
Ley 32/2006, Artículo 9
Artículo 9. Representantes de los trabajadores.
1. Los representantes de los trabajadores de las diferentes empresas que intervengan en la ejecución de la obra deberán ser informados de las contrataciones y subcontrataciones que se hagan en la misma.
2. Por convenio colectivo sectorial de ámbito estatal podrán establecerse sistemas o procedimientos de representación de los trabajadores a través de representantes sindicales o de carácter bipartito entre organizaciones empresariales y sindicales, con el fin de promover el cumplimiento de la normativa de prevención de riesgos laborales en las obras de construcción del correspondiente territorio.

[5] RD 1627/1997, Artículo 16 (score 0.725)
RD 1627/1997, Artículo 16
Artículo 16. Consulta y participación de los trabaja dores.
1. La consulta y participación de los trabajadores o sus representantes se realizarán, de conformidad con lo dispuesto en el apartado 2 del artículo 18 de la Ley de Prevención de Riesgos Laborales, sobre las cuestiones a las que se refiere el presente Real Decreto.
2. Cuando sea necesario, teniendo en cuenta el nivel de riesgo y la importancia de la obra, la consulta y participación de los trabajadores o sus representantes en las empresas que ejerzan sus actividades en el lugar de trabajo deberá desarrollarse con la adecuada coordinación de conformidad con el apartado 3 del ar tículo 39 de la Ley de Prevención de Riesgos Laborales.
3. Una copia del plan de seguridad y salud y de sus posibles modificaciones, en los términos previstos en el apartado 4 del artículo 7, a efectos de su conocimiento y seguimiento, será facilitada por el contratista a los representantes de los trabajadores en el centro de trabajo.

---
## q27 (multi, dev)
**Question:** ¿Qué debe acreditar una empresa para ser subcontratada en una obra y qué registro está relacionado con ello?
**Reference:** Debe acreditar recursos humanos con formación en prevención y una organización preventiva adecuada, y estar inscrita en el Registro de Empresas Acreditadas, que depende de la autoridad laboral autonómica y tiene validez nacional.
**Answer:**

Para que una empresa pueda ser contratada o subcontratada en una obra de construcción, debe cumplir y acreditar los siguientes requisitos establecidos en la Ley 32/2006, Artículo 4:

1. **Requisitos generales de organización y actividad** ((Ley 32/2006, Artículo 4.1)):
   - Poseer una organización productiva propia, contar con los medios materiales y personales necesarios, y utilizarlos para el desarrollo de la actividad contratada.
   - Asumir los riesgos, obligaciones y responsabilidades propias del desarrollo de la actividad empresarial.
   - Ejercer directamente las facultades de organización y dirección sobre el trabajo desarrollado por sus trabajadores en la obra.

2. **Requisitos de prevención y registro** ((Ley 32/2006, Artículo 4.2)):
   - Acreditar que disponen de recursos humanos, en su nivel directivo y productivo, con la formación necesaria en prevención de riesgos laborales, y de una organización preventiva adecuada a la Ley 31/1995.
   - **Estar inscritas en el Registro de Empresas Acreditadas**, regulado en el artículo 6 de la misma ley. La inscripción se realiza de oficio por la autoridad laboral competente sobre la base de la declaración del empresario.

El cumplimiento de los requisitos de organización y de formación preventiva se acredita mediante una **declaración suscrita por su representante legal formulada ante el Registro de Empresas Acreditadas** ((Ley 32/2006, Artículo 4.3)).

**Fuentes utilizadas:**
- Ley 32/2006, Artículos 4 y 7.

*Nota: Esta información es divulgativa y no constituye asesoramiento jurídico.*

**Citations:** Ley 32/2006, Artículo 4; Ley 32/2006, Artículos 4 — all in retrieved text

**Coverage check:**

- Search 1 «requisitos subcontratación acreditar registro obra Ley 32 2006»: **SÍ**, passage [1], quote: «2. Además de los anteriores requisitos, las empresas que pretendan ser contratadas o subcontratadas para trabajos de una obra de construcción deberán también:». Need: qué debe acreditar una empresa para ser subcontratada en una obra y qué registro está relacionado con ello

**Retrieved passages:**

[1] Ley 32/2006, Artículo 4 (score 0.81)
Ley 32/2006, Artículo 4
Artículo 4. Requisitos exigibles a los contratistas y subcontratistas.
1. Para que una empresa pueda intervenir en el proceso de subcontratación en el sector de la construcción, como contratista o subcontratista, deberá:
a) Poseer una organización productiva propia, contar con los medios materiales y personales necesarios, y utilizarlos para el desarrollo de la actividad contratada.
b) Asumir los riesgos, obligaciones y responsabilidades propias del desarrollo de la actividad empresarial.
c) Ejercer directamente las facultades de organización y dirección sobre el trabajo desarrollado por sus trabajadores en la obra y, en el caso de los trabajadores autónomos, ejecutar el trabajo con autonomía y responsabilidad propia y fuera del ámbito de organización y dirección de la empresa que le haya contratado.
2. Además de los anteriores requisitos, las empresas que pretendan ser contratadas o subcontratadas para trabajos de una obra de construcción deberán también:
a) Acreditar que disponen de recursos humanos, en su nivel directivo y productivo, que cuentan con la formación necesaria en prevención de riesgos laborales, así como de una organización preventiva adecuada a la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales.
b) Estar inscritas en el Registro de Empresas Acreditadas al que se refiere el artículo 6 de esta Ley. La inscripción se realizará de oficio por la autoridad laboral competente, sobre la base de la declaración del empresario a que se refiere el apartado siguiente.
3. Las empresas contratistas o subcontratistas acreditarán el cumplimiento de los requisitos a que se refieren los apartados 1 y 2.a) de este artículo mediante una declaración suscrita por su representante legal formulada ante el Registro de Empresas Acreditadas.

[2] Ley 32/2006, Artículo 8 (score 0.803)
Ley 32/2006, Artículo 8
Artículo 8. Documentación de la subcontratación.
1. En toda obra de construcción, incluida en el ámbito de aplicación de esta Ley, cada contratista deberá disponer de un Libro de Subcontratación.
En dicho libro, que deberá permanecer en todo momento en la obra, se deberán reflejar, por orden cronológico desde el comienzo de los trabajos, todas y cada una de las subcontrataciones realizadas en una determinada obra con empresas subcontratistas y trabajadores autónomos, su nivel de subcontratación y empresa comitente, el objeto de su contrato, la identificación de la persona que ejerce las facultades de organización y dirección de cada subcontratista y, en su caso, de los representantes legales de los trabajadores de la misma, las respectivas fechas de entrega de la parte del plan de seguridad y salud que afecte a cada empresa subcontratista y trabajador autónomo, así como las instrucciones elaboradas por el coordinador de seguridad y salud para marcar la dinámica y desarrollo del procedimiento de coordinación establecido, y las anotaciones efectuadas por la dirección facultativa sobre su aprobación de cada subcontratación excepcional de las previstas en el artículo 5.3 de esta Ley.
Al Libro de Subcontratación tendrán acceso el promotor, la dirección facultativa, el coordinador de seguridad y salud en fase de ejecución de la obra, las empresas y trabajadores autónomos intervinientes en la obra, los técnicos de prevención, los delegados de prevención, la autoridad laboral y los representantes de los trabajadores de las diferentes empresas que intervengan en la ejecución de la obra.
2. Asimismo, cada empresa deberá disponer de la documentación o título que acredite la posesión de la maquinaria que utiliza, y de cuanta documentación sea exigida por las disposiciones legales vigentes.
3. Reglamentariamente se determinarán las condiciones del Libro de Subcontratación al que se refiere el apartado 1, en cuanto a su régimen de habilitación, por la autoridad laboral autonómica competente, así como el contenido y obligaciones y derechos derivados del mismo, al tiempo que se procederá a una revisión de las distintas obligaciones documentales aplicables a las obras de construcción con objeto de lograr su unificación y simplificación.

[3] Ley 32/2006, Anexo (score 0.802)
Ley 32/2006, Anexo
ANEXO
A) DATOS IDENTIFICATIVOS DE LA OBRA
Promotor
NIF
Contratista
NIF
Dirección Facultativa
NIF
Coordinador de seg. y salud en fase de ejecución
NIF
Domicilio de la obra
Localidad
B) REGISTRO DE SUBCONTRATACIONES
N.º orden
Empresa subcontratista o trabajador autónomo/NIF
Nivel de subcontratación
N.º orden del comitente (1)
Fecha comienzo trabajos
Objeto del contrato
Responsable de dirección trabajos/Representantes de los trabajadores
Fecha entrega plan de seg. y salud
Referencia de instrucciones del coordinador (2)
Firma del subcontratista o trabajador autónomo
Aprobación de la Dirección Facultativa (3)
(1) En esta columna se anotará el N.º de orden correspondiente al asiento de la empresa que ha subcontratado los trabajos a la subcontratista de este asiento, dejándose en blanco en caso de que la comitente sea la empresa contratista.
(2) En esta columna se hará constar, en su caso, la referencia de las hojas del Libro de incidencias al plan de seguridad y salud del contratista en las que el Coordinador de seguridad y salud en fase de ejecución haya efectuado anotaciones sobre las instrucciones sobre el desarrollo del procedimiento de coordinación establecido.
(3) Cuando proceda, se hará constar en esta columna la aprobación de la subcontratación a que se refiere el asiento por parte de la Dirección Facultativa, mediante la firma del mismo en esta casilla y la indicación de su fecha.

[4] Ley 32/2006, Artículo 2 (score 0.798)
Ley 32/2006, Artículo 2
Artículo 2. Ámbito de aplicación.
La presente Ley será de aplicación a los contratos que se celebren, en régimen de subcontratación, para la ejecución de los siguientes trabajos realizados en obras de construcción:
Excavación; movimiento de tierras; construcción; montaje y desmontaje de elementos prefabricados; acondicionamientos o instalaciones; transformación; rehabilitación; reparación; desmantelamiento; derribo; mantenimiento; conservación y trabajos de pintura y limpieza; saneamiento.

[5] Ley 32/2006, Artículo 7 (score 0.794)
Ley 32/2006, Artículo 7
Artículo 7. Deber de vigilancia y responsabilidades derivadas de su incumplimiento.
1. Las empresas contratistas y subcontratistas que intervengan en las obras de construcción incluidas en el ámbito de aplicación de esta Ley deberán vigilar el cumplimiento de lo dispuesto en la misma por las empresas subcontratistas y trabajadores autónomos con que contraten; en particular, en lo que se refiere a las obligaciones de acreditación y registro reguladas en el artículo 4.2 y al régimen de la subcontratación que se regula en el artículo 5.
A efectos de lo dispuesto en el párrafo anterior, las empresas subcontratistas deberán comunicar o trasladar al contratista, a través de sus respectivas empresas comitentes en caso de ser distintas de aquél, toda información o documentación que afecte al contenido de este capítulo.
2. Sin perjuicio de otras responsabilidades establecidas en la legislación social, el incumplimiento de las obligaciones de acreditación y registro exigidas en el artículo 4.2, o del régimen de subcontratación establecido en el artículo 5, determinará la responsabilidad solidaria del subcontratista que hubiera contratado incurriendo en dichos incumplimientos y del correspondiente contratista respecto de las obligaciones laborales y de Seguridad Social derivadas de la ejecución del contrato acordado que correspondan al subcontratista responsable del incumplimiento en el ámbito de ejecución de su contrato, cualquiera que fuera la actividad de dichas empresas.
3. En todo caso será exigible la responsabilidad establecida en el artículo 43 del Estatuto de los Trabajadores cuando se den los supuestos previstos en el mismo.

---
## q28 (unanswerable, dev)
**Question:** ¿Qué seguro de responsabilidad civil debe contratar el promotor de una obra?
**Reference:** El corpus no lo cubre; debe decir que no consta en los documentos.
**Answer:** *(forced refusal)*

No consta en los documentos del corpus.

Se buscó en el corpus: «seguro de responsabilidad civil promotor obra».

**Citations:** (none)

**Coverage check:**

- Search 1 «seguro de responsabilidad civil promotor obra»: **NO**. Need: qué seguro de responsabilidad civil debe contratar el promotor de una obra

**Retrieved passages:**

[1] Ley 32/2006, Artículo 3 (score 0.678)
Ley 32/2006, Artículo 3
Artículo 3. Definiciones.
A efectos de esta Ley se entenderá por:
a) Obra de construcción u obra: cualquier obra, pública o privada, en la que se efectúen trabajos de construcción o de ingeniería civil.
b) Promotor: cualquier persona física o jurídica por cuenta de la cual se realice la obra.
c) Dirección facultativa: el técnico o técnicos competentes designados por el promotor, encargados de la dirección y del control de la ejecución de la obra.
d) Coordinador en materia de seguridad y de salud durante la ejecución de la obra: el técnico competente integrado en la dirección facultativa, designado por el promotor para llevar a cabo las tareas establecidas para este coordinador en la reglamentación de seguridad y salud en las obras de construcción.
e) Contratista o empresario principal: la persona física o jurídica, que asume contractualmente ante el promotor, con medios humanos y materiales, propios o ajenos, el compromiso de ejecutar la totalidad o parte de las obras con sujeción al proyecto y al contrato.
Cuando el promotor realice directamente con medios humanos y materiales propios la totalidad o determinadas partes de la obra, tendrá también la consideración de contratista a los efectos de la presente Ley; asimismo, cuando la contrata se haga con una Unión Temporal de Empresas, que no ejecute directamente la obra, cada una de sus empresas miembro tendrá la consideración de empresa contratista en la parte de obra que ejecute.
f) Subcontratista: la persona física o jurídica que asume contractualmente ante el contratista u otro subcontratista comitente el compromiso de realizar determinadas partes o unidades de obra, con sujeción al proyecto por el que se rige su ejecución. Las variantes de esta figura pueden ser las del primer subcontratista (subcontratista cuyo comitente es el contratista), segundo subcontratista (subcontratista cuyo comitente es el primer subcontratista), y así sucesivamente.

[2] RD 1627/1997, Artículo 3 (score 0.662)
RD 1627/1997, Artículo 3
Artículo 3. Designación de los coordinadores en materia de seguridad y salud.
1. En las obras incluidas en el ámbito de aplicación del presente Real Decreto, cuando en la elaboración del proyecto de obra intervengan varios proyectistas, el promotor designará un coordinador en materia de seguridad y de salud durante la elaboración del proyecto de obra.
2. Cuando en la ejecución de la obra intervenga más de una empresa, o una empresa y trabajadores autónomos o diversos trabajadores autónomos, el promotor, antes del inicio de los trabajos o tan pronto como se constate dicha circunstancia, designará un coordinador en materia de seguridad y salud durante la ejecución de la obra.
3. La designación de los coordinadores en materia de seguridad y salud durante la elaboración del proyecto de obra y durante la ejecución de la obra podrá recaer en la misma persona.
4. La designación de los coordinadores no eximirá al promotor de sus responsabilidades.

[3] RD 1627/1997, Artículo 4 (score 0.656)
RD 1627/1997, Artículo 4
Artículo 4. Obligatoriedad del estudio de seguridad y salud o del estudio básico de seguridad y salud en las obras.
1. El promotor estará obligado a que en la fase de redacción del proyecto se elabore un estudio de seguridad y salud en los proyectos de obras en que se den alguno de los supuestos siguientes:
a) Que el presupuesto de ejecución por contrata incluido en el proyecto sea igual o superior a 75 millones de pesetas.
b) Que la duración estimada sea superior a 30 días laborables, empleándose en algún momento a más de 20 trabajadores simultáneamente.
c) Que el volumen de mano de obra estimada, entendiendo por tal la suma de los días de trabajo del total de los trabajadores en la obra, sea superior a 500.
d) Las obras de túneles, galerías, conducciones subterráneas y presas.
2. En los proyectos de obras no incluidos en ninguno de los supuestos previstos en el apartado anterior, el promotor estará obligado a que en la fase de redacción del proyecto se elabore un estudio básico de seguridad y salud.

[4] Ley 32/2006, Artículo 2 (score 0.654)
Ley 32/2006, Artículo 2
Artículo 2. Ámbito de aplicación.
La presente Ley será de aplicación a los contratos que se celebren, en régimen de subcontratación, para la ejecución de los siguientes trabajos realizados en obras de construcción:
Excavación; movimiento de tierras; construcción; montaje y desmontaje de elementos prefabricados; acondicionamientos o instalaciones; transformación; rehabilitación; reparación; desmantelamiento; derribo; mantenimiento; conservación y trabajos de pintura y limpieza; saneamiento.

[5] Ley 32/2006, Artículo 7 (score 0.653)
Ley 32/2006, Artículo 7
Artículo 7. Deber de vigilancia y responsabilidades derivadas de su incumplimiento.
1. Las empresas contratistas y subcontratistas que intervengan en las obras de construcción incluidas en el ámbito de aplicación de esta Ley deberán vigilar el cumplimiento de lo dispuesto en la misma por las empresas subcontratistas y trabajadores autónomos con que contraten; en particular, en lo que se refiere a las obligaciones de acreditación y registro reguladas en el artículo 4.2 y al régimen de la subcontratación que se regula en el artículo 5.
A efectos de lo dispuesto en el párrafo anterior, las empresas subcontratistas deberán comunicar o trasladar al contratista, a través de sus respectivas empresas comitentes en caso de ser distintas de aquél, toda información o documentación que afecte al contenido de este capítulo.
2. Sin perjuicio de otras responsabilidades establecidas en la legislación social, el incumplimiento de las obligaciones de acreditación y registro exigidas en el artículo 4.2, o del régimen de subcontratación establecido en el artículo 5, determinará la responsabilidad solidaria del subcontratista que hubiera contratado incurriendo en dichos incumplimientos y del correspondiente contratista respecto de las obligaciones laborales y de Seguridad Social derivadas de la ejecución del contrato acordado que correspondan al subcontratista responsable del incumplimiento en el ámbito de ejecución de su contrato, cualquiera que fuera la actividad de dichas empresas.
3. En todo caso será exigible la responsabilidad establecida en el artículo 43 del Estatuto de los Trabajadores cuando se den los supuestos previstos en el mismo.

---
## q29 (unanswerable, dev)
**Question:** ¿Cuántos extintores debe haber por planta en una obra?
**Reference:** El corpus no lo cubre; debe decir que no consta en los documentos.
**Answer:** *(forced refusal)*

No consta en los documentos del corpus.

Se buscó en el corpus: «extintores planta obra construccion».

**Citations:** (none)

**Coverage check:**

- Search 1 «extintores planta obra construccion»: **NO**. Need: el número exacto de extintores que debe haber por planta en una obra

**Retrieved passages:**

[1] RD 1627/1997, Anexo I (score 0.638)
RD 1627/1997, Anexo I
ANEXO I
Relación no exhaustiva de las obras de construcción o de ingeniería civil
a) Excavación.
b) Movimiento de tierras.
c) Construcción.
d) Montaje y desmontaje de elementos prefabricados.
e) Acondicionamiento o instalaciones.
f) Transformación.
g) Rehabilitación.
h) Reparación.
i) Desmantelamiento.
j) Derribo.
k) Mantenimiento.
l) Conservación-Trabajos de pintura y de limpieza.
m) Saneamiento.

[2] Ley 31/1995, Artículo 20 (score 0.633)
Ley 31/1995, Artículo 20
Artículo 20. Medidas de emergencia.
El empresario, teniendo en cuenta el tamaño y la actividad de la empresa, así como la posible presencia de personas ajenas a la misma, deberá analizar las posibles situaciones de emergencia y adoptar las medidas necesarias en materia de primeros auxilios, lucha contra incendios y evacuación de los trabajadores, designando para ello al personal encargado de poner en práctica estas medidas y comprobando periódicamente, en su caso, su correcto funcionamiento. El citado personal deberá poseer la formación necesaria, ser suficiente en número y disponer del material adecuado, en función de las circunstancias antes señaladas.
Para la aplicación de las medidas adoptadas, el empresario deberá organizar las relaciones que sean necesarias con servicios externos a la empresa, en particular en materia de primeros auxilios, asistencia médica de urgencia, salvamento y lucha contra incendios, de forma que quede garantizada la rapidez y eficacia de las mismas.

[3] RD 1627/1997, Anexo IV (score 0.631)
RD 1627/1997, Anexo IV
b) En caso de peligro, todos los lugares de trabajo deberán poder evacuarse rápidamente y en condiciones de máxima seguridad para los trabajadores.
c) El número, la distribución y las dimensiones de las vías y salidas de emergencia dependerán del uso, de los equipos y de las dimensiones de la obra y de los locales, así como del número máximo de personas que puedan estar presente en ellos.
d) Las vías y salidas específicas de emergencia deberán señalizarse conforme al Real Decreto 485/1997, de 14 de abril, sobre disposiciones mínimas en materia de señalización de seguridad y salud en el trabajo. Dicha señalización deberá fijarse en los lugares adecuados y tener la resistencia suficiente.
e) Las vías y salidas de emergencia, así como las vías de circulación y las puertas que den acceso a ellas, no deberán estar obstruidas por ningún objeto, de modo que puedan utilizarse sin trabas en cualquier momento.
f) En caso de avería del sistema de alumbrado, las vías y salidas de emergencia que requieran iluminación deberán estar equipadas con iluminación de seguridad de suficiente intensidad.
5. Detección y lucha contra incendios:
a) Según las características de la obra y según las dimensiones y el uso de los locales, los equipos presentes, las características físicas y químicas de las sustancias o materiales que se hallen presentes así como el número máximo de personas que puedan hallarse en ellos, se deberá prever un número suficiente de dispositivos apropiados de lucha contra incendios y, si fuere necesario, de detectores de incendios y de sistemas de alarma.
b) Dichos dispositivos de lucha contra incendios y sistemas de alarma deberán verificarse y mantenerse con regularidad. Deberán realizarse, a intervalos regulares, pruebas y ejercicios adecuados.
c) Los dispositivos no automáticos de lucha contra incendios deberán ser de fácil acceso y manipulación.
Deberán estar señalizados conforme al Real Decreto sobre señalización de seguridad y salud en el trabajo. Dicha señalización deberá fijarse en los lugares adecuados y tener la resistencia suficiente.
6. Ventilación:

[4] Ley 32/2006, Artículo 2 (score 0.629)
Ley 32/2006, Artículo 2
Artículo 2. Ámbito de aplicación.
La presente Ley será de aplicación a los contratos que se celebren, en régimen de subcontratación, para la ejecución de los siguientes trabajos realizados en obras de construcción:
Excavación; movimiento de tierras; construcción; montaje y desmontaje de elementos prefabricados; acondicionamientos o instalaciones; transformación; rehabilitación; reparación; desmantelamiento; derribo; mantenimiento; conservación y trabajos de pintura y limpieza; saneamiento.

[5] RD 1627/1997, Artículo 4 (score 0.617)
RD 1627/1997, Artículo 4
Artículo 4. Obligatoriedad del estudio de seguridad y salud o del estudio básico de seguridad y salud en las obras.
1. El promotor estará obligado a que en la fase de redacción del proyecto se elabore un estudio de seguridad y salud en los proyectos de obras en que se den alguno de los supuestos siguientes:
a) Que el presupuesto de ejecución por contrata incluido en el proyecto sea igual o superior a 75 millones de pesetas.
b) Que la duración estimada sea superior a 30 días laborables, empleándose en algún momento a más de 20 trabajadores simultáneamente.
c) Que el volumen de mano de obra estimada, entendiendo por tal la suma de los días de trabajo del total de los trabajadores en la obra, sea superior a 500.
d) Las obras de túneles, galerías, conducciones subterráneas y presas.
2. En los proyectos de obras no incluidos en ninguno de los supuestos previstos en el apartado anterior, el promotor estará obligado a que en la fase de redacción del proyecto se elabore un estudio básico de seguridad y salud.

---
## q30 (unanswerable, dev)
**Question:** ¿Qué medidas deben tomarse en las obras durante una ola de calor?
**Reference:** El corpus no lo cubre; debe decir que no consta en los documentos.
**Answer:** *(forced refusal)*

No consta en los documentos del corpus.

Se buscó en el corpus: «ola de calor temperaturas meteorológicas obras de construcción».

**Citations:** (none)

**Coverage check:**

- Search 1 «ola de calor temperaturas meteorológicas obras de construcción»: **NO**. Need: qué medidas específicas deben tomarse en las obras durante una ola de calor

**Retrieved passages:**

[1] RD 1627/1997, Anexo IV (score 0.639)
RD 1627/1997, Anexo IV
a) Teniendo en cuenta los métodos de trabajo y las cargas físicas impuestas a los trabajadores, éstos deberán disponer de aire limpio en cantidad suficiente.
b) En caso de que se utilice una instalación de ventilación, deberá mantenerse en buen estado de funcionamiento y los trabajadores no deberán estar expuestos a corrientes de aire que perjudiquen su salud. Siempre que sea necesario para la salud de los trabajadores, deberá haber un sistema de control que indique cualquier avería.
7. Exposición a riesgos particulares:
a) Los trabajadores no deberán estar expuestos a niveles sonoros nocivos ni a factores externos nocivos (por ejemplo, gases, vapores, polvo).
b) En caso de que algunos trabajadores deban penetrar en una zona cuya atmósfera pudiera contener sustancias tóxicas o nocivas, o no tener oxígeno en cantidad suficiente o ser inflamable, la atmósfera confinada deberá ser controlada y se deberán adoptar medidas adecuadas para prevenir cualquier peligro.
c) En ningún caso podrá exponerse a un trabajador a una atmósfera confinada de alto riesgo. Deberá, al menos, quedar bajo vigilancia permanente desde el exterior y deberán tomarse todas las debidas precauciones para que se le pueda prestar auxilio eficaz e inmediato.
8. Temperatura: La temperatura debe ser la adecuada para el organismo humano durante el tiempo de trabajo, cuando las circunstancias lo permitan, teniendo en cuenta los métodos de trabajo que se apliquen y las cargas físicas impuestas a los trabajadores.
9. Iluminación:
a) Los lugares de trabajo, los locales y las vías de circulación en la obra deberán disponer, en la medida de lo posible, de suficiente luz natural y tener una iluminación artificial adecuada y suficiente durante la noche y cuando no sea suficiente la luz natural. En su caso, se utilizarán puntos de iluminación portátiles con protección antichoques. El color utilizado para la iluminación artificial no podrá alterar o influir en la percepción de las señales o paneles de señalización.

[2] Ley 32/2006, Artículo 2 (score 0.606)
Ley 32/2006, Artículo 2
Artículo 2. Ámbito de aplicación.
La presente Ley será de aplicación a los contratos que se celebren, en régimen de subcontratación, para la ejecución de los siguientes trabajos realizados en obras de construcción:
Excavación; movimiento de tierras; construcción; montaje y desmontaje de elementos prefabricados; acondicionamientos o instalaciones; transformación; rehabilitación; reparación; desmantelamiento; derribo; mantenimiento; conservación y trabajos de pintura y limpieza; saneamiento.

[3] RD 1627/1997, Anexo I (score 0.6)
RD 1627/1997, Anexo I
ANEXO I
Relación no exhaustiva de las obras de construcción o de ingeniería civil
a) Excavación.
b) Movimiento de tierras.
c) Construcción.
d) Montaje y desmontaje de elementos prefabricados.
e) Acondicionamiento o instalaciones.
f) Transformación.
g) Rehabilitación.
h) Reparación.
i) Desmantelamiento.
j) Derribo.
k) Mantenimiento.
l) Conservación-Trabajos de pintura y de limpieza.
m) Saneamiento.

[4] Ley 32/2006, Artículo 4 (score 0.6)
Ley 32/2006, Artículo 4
4. Las empresas cuya actividad consista en ser contratadas o subcontratadas habitualmente para la realización de trabajos en obras del sector de la construcción deberán contar, en los términos que se determine reglamentariamente, con un número de trabajadores contratados con carácter indefinido que no será inferior al 10 por ciento durante los dieciocho primeros meses de vigencia de esta Ley, ni al 20 por ciento durante los meses del decimonoveno al trigésimo sexto, ni al 30 por ciento a partir del mes trigésimo séptimo, inclusive.
A estos efectos, en las cooperativas de trabajo asociado los socios trabajadores serán computados de manera análoga a los trabajadores por cuenta ajena en los términos que se determine reglamentariamente.

[5] RD 1215/1997, Anexo II (score 0.594)
RD 1215/1997, Anexo II
4.1.6 Los trabajos temporales en altura sólo podrán efectuarse cuando las condiciones meteorológicas no pongan en peligro la salud y la seguridad de los trabajadores.
4.2 Disposiciones específicas sobre la utilización de escaleras de mano.
4.2.1 Las escaleras de mano se colocarán de forma que su estabilidad durante su utilización esté asegurada. Los puntos de apoyo de las escaleras de mano deberán asentarse sólidamente sobre un soporte de dimensiones adecuadas y estable, resistente e inmóvil, de forma que los travesaños queden en posición horizontal. Las escaleras suspendidas se fijarán de forma segura y, excepto las de cuerda, de manera que no puedan desplazarse y se eviten los movimientos de balanceo.
4.2.2 Se impedirá el deslizamiento de los pies de las escaleras de mano durante su utilización ya sea mediante la fijación de la parte superior o inferior de los largueros, ya sea mediante cualquier dispositivo antideslizante o cualquier otra solución de eficacia equivalente. Las escaleras de mano para fines de acceso deberán tener la longitud necesaria para sobresalir al menos un metro del plano de trabajo al que se accede. Las escaleras compuestas de varios elementos adaptables o extensibles deberán utilizarse de forma que la inmovilización recíproca de los distintos elementos esté asegurada. Las escaleras con ruedas deberán haberse inmovilizado antes de acceder a ellas. Las escaleras de mano simples se colocarán, en la medida de lo posible, formando un ángulo aproximado de 75 grados con la horizontal.

---
## h01 (multi, heldout)
**Question:** Oye, tengo a un tío de una subcontrata que lleva dos días currando en la obra y no sé si le han dado formación ni nada de eso. ¿Eso me lo tengo que mirar yo o es cosa de su empresa?
**Reference:** Employer must give the training (Ley 31/1995 Art. 19; Ley 32/2006 Art. 10.1) but the contractor must monitor its subcontractors, including accreditation of trained staff (Ley 32/2006 Art. 7.1 and 4.2.a).
**Answer:**

Según los documentos del corpus, la obligación de garantizar que el trabajador tenga la formación necesaria en prevención de riesgos laborales recae en su propia empresa (su empleador), que debe velar por que cuente con la formación adecuada a su puesto de trabajo o función (Ley 32/2006, Artículo 10).

Fuentes utilizadas:
- Ley 32/2006 (subcontratación en el sector de la construcción), Artículo 10.

*Nota: Esta información es divulgativa y no constituye asesoramiento legal.*

**Citations:** Ley 32/2006, Artículo 10 — all in retrieved text

**Coverage check:**

- Search 1 «formacion trabajadores subcontrata construccion»: **SÍ**, passage [3], quote: «1. Las empresas velarán por que todos los trabajadores que presten servicios en las obras tengan la formación necesaria y adecuada a su puesto de trabajo o función en materia de prevención de riesgos laborales, de forma que conozcan los riesgos y las medidas para prevenirlos.». Need: si la obligación de que el trabajador de una subcontrata tenga formación en prevención de riesgos laborales recae sobre su propia empresa o sobre la empresa principal de la obra

**Retrieved passages:**

[1] Ley 32/2006, Artículo 2 (score 0.747)
Ley 32/2006, Artículo 2
Artículo 2. Ámbito de aplicación.
La presente Ley será de aplicación a los contratos que se celebren, en régimen de subcontratación, para la ejecución de los siguientes trabajos realizados en obras de construcción:
Excavación; movimiento de tierras; construcción; montaje y desmontaje de elementos prefabricados; acondicionamientos o instalaciones; transformación; rehabilitación; reparación; desmantelamiento; derribo; mantenimiento; conservación y trabajos de pintura y limpieza; saneamiento.

[2] Ley 32/2006, Artículo 1 (score 0.742)
Ley 32/2006, Artículo 1
Artículo 1. Objeto de la Ley.
1. La presente Ley regula la subcontratación en el sector de la construcción y tiene por objeto mejorar las condiciones de trabajo del sector, en general, y las condiciones de seguridad y salud de los trabajadores del mismo, en particular.
2. Lo previsto en esta Ley se entiende sin perjuicio de la aplicación a las subcontrataciones que se realicen en el sector de la construcción de lo dispuesto en el artículo 42 del Texto Refundido de la Ley del Estatuto de los Trabajadores, aprobado por Real Decreto Legislativo 1/1995, de 24 de marzo, y en el resto de la legislación social.

[3] Ley 32/2006, Artículo 10 (score 0.741)
Ley 32/2006, Artículo 10
Artículo 10. Acreditación de la formación preventiva de los trabajadores.
1. Las empresas velarán por que todos los trabajadores que presten servicios en las obras tengan la formación necesaria y adecuada a su puesto de trabajo o función en materia de prevención de riesgos laborales, de forma que conozcan los riesgos y las medidas para prevenirlos.
2. Sin perjuicio de la obligación legal del empresario de garantizar la formación a que se refiere el apartado anterior, en la negociación colectiva estatal del sector se podrán establecer programas formativos y contenidos específicos de carácter sectorial y para los trabajos de cada especialidad.
3. Dadas las características que concurren en el sector de la construcción, reglamentariamente o a través de la negociación colectiva sectorial de ámbito estatal, se regulará la forma de acreditar la formación específica recibida por el trabajador referida a la prevención de riesgos laborales en el sector de la construcción.
El sistema de acreditación que se establezca, que podrá consistir en la expedición de una cartilla o carné profesional para cada trabajador, será único y tendrá validez en el conjunto del sector, pudiendo atribuirse su diseño, ejecución y expedición a organismos paritarios creados en el ámbito de la negociación colectiva sectorial de ámbito estatal, en coordinación con la Fundación adscrita a la Comisión Nacional de Seguridad y Salud en el Trabajo.

[4] Ley 32/2006, Artículo 4 (score 0.738)
Ley 32/2006, Artículo 4
4. Las empresas cuya actividad consista en ser contratadas o subcontratadas habitualmente para la realización de trabajos en obras del sector de la construcción deberán contar, en los términos que se determine reglamentariamente, con un número de trabajadores contratados con carácter indefinido que no será inferior al 10 por ciento durante los dieciocho primeros meses de vigencia de esta Ley, ni al 20 por ciento durante los meses del decimonoveno al trigésimo sexto, ni al 30 por ciento a partir del mes trigésimo séptimo, inclusive.
A estos efectos, en las cooperativas de trabajo asociado los socios trabajadores serán computados de manera análoga a los trabajadores por cuenta ajena en los términos que se determine reglamentariamente.

[5] Ley 32/2006, Artículo 4 (score 0.737)
Ley 32/2006, Artículo 4
Artículo 4. Requisitos exigibles a los contratistas y subcontratistas.
1. Para que una empresa pueda intervenir en el proceso de subcontratación en el sector de la construcción, como contratista o subcontratista, deberá:
a) Poseer una organización productiva propia, contar con los medios materiales y personales necesarios, y utilizarlos para el desarrollo de la actividad contratada.
b) Asumir los riesgos, obligaciones y responsabilidades propias del desarrollo de la actividad empresarial.
c) Ejercer directamente las facultades de organización y dirección sobre el trabajo desarrollado por sus trabajadores en la obra y, en el caso de los trabajadores autónomos, ejecutar el trabajo con autonomía y responsabilidad propia y fuera del ámbito de organización y dirección de la empresa que le haya contratado.
2. Además de los anteriores requisitos, las empresas que pretendan ser contratadas o subcontratadas para trabajos de una obra de construcción deberán también:
a) Acreditar que disponen de recursos humanos, en su nivel directivo y productivo, que cuentan con la formación necesaria en prevención de riesgos laborales, así como de una organización preventiva adecuada a la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales.
b) Estar inscritas en el Registro de Empresas Acreditadas al que se refiere el artículo 6 de esta Ley. La inscripción se realizará de oficio por la autoridad laboral competente, sobre la base de la declaración del empresario a que se refiere el apartado siguiente.
3. Las empresas contratistas o subcontratistas acreditarán el cumplimiento de los requisitos a que se refieren los apartados 1 y 2.a) de este artículo mediante una declaración suscrita por su representante legal formulada ante el Registro de Empresas Acreditadas.

---
## h02 (single, heldout)
**Question:** Hemos cogido a dos chavales de una ETT para una obra que llevamos nosotros. ¿Quién les tiene que dar la formación y quién les da los equipos de protección: la ETT o nosotros?
**Reference:** ETT is responsible for training and health surveillance; the user company is responsible for working conditions and for informing the ETT about the job (Ley 31/1995 Art. 28.5, 28.2). The text does not say literally who supplies PPE.
**Answer:**

Según los documentos consultados:

* **Formación:** La Empresa de Trabajo Temporal (ETT) es la responsable del cumplimiento de las obligaciones en materia de formación (Ley 31/1995, Artículo 28.5). Para ello, vuestra empresa usuaria debe informar previamente a la ETT (y esta a los trabajadores) sobre las características del puesto y las cualificaciones requeridas antes de su adscripción (Ley 31/1995, Artículo 28.5).
* **Equipos de protección y condiciones de ejecución:** La empresa usuaria (vosotros) es la responsable de las condiciones de ejecución del trabajo en todo lo relacionado con la protección de la seguridad y la salud de los trabajadores (Ley 31/1995, Artículo 28.5). *(Nota: Los pasajes del corpus no especifican de forma literal quién debe entregar físicamente los equipos de protección individual en el caso particular de una ETT, ya que el artículo genérico 17.2 establece que el empresario debe proporcionarlos, sin desarrollar en este apartado la distinción exacta entre ETT y empresa usuaria sobre los EPI).*

Fuentes utilizadas:
* Ley 31/1995 (Ley de Prevención de Riesgos Laborales), Artículos 17, 19 y 28.

*Esta información es divulgativa y no constituye asesoramiento legal.*

**Citations:** Ley 31/1995, Artículo 28 — all in retrieved text

**Coverage check:**

- Search 1 «ETT formación equipos protección obra construcción»: **PARCIAL**, passage [5], quote: «La empresa de trabajo temporal será responsable del cumplimiento de las obligaciones en materia de formación y vigilancia de la salud que se establecen en los apartados 2 y 3 de este artículo.». Need: quién debe dar la formación y quién los equipos de protección a los trabajadores de una ETT en una obra
- Search 2 «Ley 31 1995 articulo 28 equipos de protección ETT empresa usuaria»: **PARCIAL**, passage [1], quote: «La empresa de trabajo temporal será responsable del cumplimiento de las obligaciones en materia de formación y vigilancia de la salud que se establecen en los apartados 2 y 3 de este artículo.». Need: quién debe dar la formación a los trabajadores de una ETT y quién les debe proporcionar los equipos de protección

**Retrieved passages:**

[1] Ley 31/1995, Artículo 19 (score 0.71)
Ley 31/1995, Artículo 19
Artículo 19. Formación de los trabajadores.
1. En cumplimiento del deber de protección, el empresario deberá garantizar que cada trabajador reciba una formación teórica y práctica, suficiente y adecuada, en materia preventiva, tanto en el momento de su contratación, cualquiera que sea la modalidad o duración de ésta, como cuando se produzcan cambios en las funciones que desempeñe o se introduzcan nuevas tecnologías o cambios en los equipos de trabajo.
La formación deberá estar centrada específicamente en el puesto de trabajo o función de cada trabajador, adaptarse a la evolución de los riesgos y a la aparición de otros nuevos y repetirse periódicamente, si fuera necesario.
2. La formación a que se refiere el apartado anterior deberá impartirse, siempre que sea posible, dentro de la jornada de trabajo o, en su defecto, en otras horas pero con el descuento en aquélla del tiempo invertido en la misma. La formación se podrá impartir por la empresa mediante medios propios o concertándola con servicios ajenos, y su coste no recaerá en ningún caso sobre los trabajadores.

[2] Ley 31/1995, Artículo 17 (score 0.699)
Ley 31/1995, Artículo 17
Artículo 17. Equipos de trabajo y medios de protección.
1. El empresario adoptará las medidas necesarias con el fin de que los equipos de trabajo sean adecuados para el trabajo que deba realizarse y convenientemente adaptados a tal efecto, de forma que garanticen la seguridad y la salud de los trabajadores al utilizarlos.
Cuando la utilización de un equipo de trabajo pueda presentar un riesgo específico para la seguridad y la salud de los trabajadores, el empresario adoptará las medidas necesarias con el fin de que:
a) La utilización del equipo de trabajo quede reservada a los encargados de dicha utilización.
b) Los trabajos de reparación, transformación, mantenimiento o conservación sean realizados por los trabajadores específicamente capacitados para ello.
2. El empresario deberá proporcionar a sus trabajadores equipos de protección individual adecuados para el desempeño de sus funciones y velar por el uso efectivo de los mismos cuando, por la naturaleza de los trabajos realizados, sean necesarios.
Los equipos de protección individual deberán utilizarse cuando los riesgos no se puedan evitar o no puedan limitarse suficientemente por medios técnicos de protección colectiva o mediante medidas, métodos o procedimientos de organización del trabajo.

[3] Ley 31/1995, Artículo 28 (score 0.686)
Ley 31/1995, Artículo 28
Artículo 28. Relaciones de trabajo temporales, de duración determinada y en empresas de trabajo temporal.
1. Los trabajadores con relaciones de trabajo temporales o de duración determinada, así como los contratados por empresas de trabajo temporal, deberán disfrutar del mismo nivel de protección en materia de seguridad y salud que los restantes trabajadores de la empresa en la que prestan sus servicios.
La existencia de una relación de trabajo de las señaladas en el párrafo anterior no justificará en ningún caso una diferencia de trato por lo que respecta a las condiciones de trabajo, en lo relativo a cualquiera de los aspectos de la protección de la seguridad y la salud de los trabajadores.
La presente Ley y sus disposiciones de desarrollo se aplicarán plenamente a las relaciones de trabajo señaladas en los párrafos anteriores.
2. El empresario adoptará las medidas necesarias para garantizar que, con carácter previo al inicio de su actividad, los trabajadores a que se refiere el apartado anterior reciban información acerca de los riesgos a los que vayan a estar expuestos, en particular en lo relativo a la necesidad de cualificaciones o aptitudes profesionales determinadas, la exigencia de controles médicos especiales o la existencia de riesgos específicos del puesto de trabajo a cubrir, así como sobre las medidas de protección y prevención frente a los mismos.
Dichos trabajadores recibirán, en todo caso, una formación suficiente y adecuada a las características del puesto de trabajo a cubrir, teniendo en cuenta su cualificación y experiencia profesional y los riesgos a los que vayan a estar expuestos.
3. Los trabajadores a que se refiere el presente artículo tendrán derecho a una vigilancia periódica de su estado de salud, en los términos establecidos en el artículo 22 de esta Ley y en sus normas de desarrollo.

[4] Ley 32/2006, Artículo 2 (score 0.684)
Ley 32/2006, Artículo 2
Artículo 2. Ámbito de aplicación.
La presente Ley será de aplicación a los contratos que se celebren, en régimen de subcontratación, para la ejecución de los siguientes trabajos realizados en obras de construcción:
Excavación; movimiento de tierras; construcción; montaje y desmontaje de elementos prefabricados; acondicionamientos o instalaciones; transformación; rehabilitación; reparación; desmantelamiento; derribo; mantenimiento; conservación y trabajos de pintura y limpieza; saneamiento.

[5] Ley 31/1995, Artículo 28 (score 0.682)
Ley 31/1995, Artículo 28
4. El empresario deberá informar a los trabajadores designados para ocuparse de las actividades de protección y prevención o, en su caso, al servicio de prevención previsto en el artículo 31 de esta Ley de la incorporación de los trabajadores a que se refiere el presente artículo, en la medida necesaria para que puedan desarrollar de forma adecuada sus funciones respecto de todos los trabajadores de la empresa.
5. En las relaciones de trabajo a través de empresas de trabajo temporal, la empresa usuaria será responsable de las condiciones de ejecución del trabajo en todo lo relacionado con la protección de la seguridad y la salud de los trabajadores. Corresponderá, además, a la empresa usuaria el cumplimiento de las obligaciones en materia de información previstas en los apartados 2 y 4 del presente artículo.
La empresa de trabajo temporal será responsable del cumplimiento de las obligaciones en materia de formación y vigilancia de la salud que se establecen en los apartados 2 y 3 de este artículo. A tal fin, y sin perjuicio de lo dispuesto en el párrafo anterior, la empresa usuaria deberá informar a la empresa de trabajo temporal, y ésta a los trabajadores afectados, antes de la adscripción de los mismos, acerca de las características propias de los puestos de trabajo a desempeñar y de las cualificaciones requeridas.
La empresa usuaria deberá informar a los representantes de los trabajadores en la misma de la adscripción de los trabajadores puestos a disposición por la empresa de trabajo temporal. Dichos trabajadores podrán dirigirse a estos representantes en el ejercicio de los derechos reconocidos en la presente Ley.

[1] Ley 31/1995, Artículo 28 (score 0.822)
Ley 31/1995, Artículo 28
4. El empresario deberá informar a los trabajadores designados para ocuparse de las actividades de protección y prevención o, en su caso, al servicio de prevención previsto en el artículo 31 de esta Ley de la incorporación de los trabajadores a que se refiere el presente artículo, en la medida necesaria para que puedan desarrollar de forma adecuada sus funciones respecto de todos los trabajadores de la empresa.
5. En las relaciones de trabajo a través de empresas de trabajo temporal, la empresa usuaria será responsable de las condiciones de ejecución del trabajo en todo lo relacionado con la protección de la seguridad y la salud de los trabajadores. Corresponderá, además, a la empresa usuaria el cumplimiento de las obligaciones en materia de información previstas en los apartados 2 y 4 del presente artículo.
La empresa de trabajo temporal será responsable del cumplimiento de las obligaciones en materia de formación y vigilancia de la salud que se establecen en los apartados 2 y 3 de este artículo. A tal fin, y sin perjuicio de lo dispuesto en el párrafo anterior, la empresa usuaria deberá informar a la empresa de trabajo temporal, y ésta a los trabajadores afectados, antes de la adscripción de los mismos, acerca de las características propias de los puestos de trabajo a desempeñar y de las cualificaciones requeridas.
La empresa usuaria deberá informar a los representantes de los trabajadores en la misma de la adscripción de los trabajadores puestos a disposición por la empresa de trabajo temporal. Dichos trabajadores podrán dirigirse a estos representantes en el ejercicio de los derechos reconocidos en la presente Ley.

[2] Ley 31/1995, Artículo 17 (score 0.815)
Ley 31/1995, Artículo 17
Artículo 17. Equipos de trabajo y medios de protección.
1. El empresario adoptará las medidas necesarias con el fin de que los equipos de trabajo sean adecuados para el trabajo que deba realizarse y convenientemente adaptados a tal efecto, de forma que garanticen la seguridad y la salud de los trabajadores al utilizarlos.
Cuando la utilización de un equipo de trabajo pueda presentar un riesgo específico para la seguridad y la salud de los trabajadores, el empresario adoptará las medidas necesarias con el fin de que:
a) La utilización 

---
## h03 (multi, heldout)
**Question:** Somos 47 en plantilla repartidos entre la oficina y dos obras. ¿Estamos obligados a montar un comité de seguridad y salud o todavía no?
**Reference:** No: 47 is below 50 (Art. 38.2). One prevention delegate elected among staff delegates (Art. 35.2, 31-49 workers).
**Answer:**

No, con una plantilla de 47 trabajadores todavía no están obligados a constituir un comité de seguridad y salud. 

Según la normativa, se debe constituir un Comité de Seguridad y Salud en todas las empresas o centros de trabajo que cuenten con 50 o más trabajadores ((Ley 31/1995, Artículo 38)).

Fuentes utilizadas:
- Ley 31/1995 (Prevención de Riesgos Laborales), Artículo 38.

**Citations:** Ley 31/1995, Artículo 38 — all in retrieved text

**Coverage check:**

- Search 1 «comite de seguridad y salud numero de trabajadores plantilla empresa»: **SÍ**, passage [1], quote: «2. Se constituirá un Comité de Seguridad y Salud en todas las empresas o centros de trabajo que cuenten con 50 o más trabajadores.». Need: a partir de qué número de trabajadores en plantilla se está obligado a montar un comité de seguridad y salud

**Retrieved passages:**

[1] Ley 31/1995, Artículo 38 (score 0.743)
Ley 31/1995, Artículo 38
Artículo 38. Comité de Seguridad y Salud.
1. El Comité de Seguridad y Salud es el órgano paritario y colegiado de participación destinado a la consulta regular y periódica de las actuaciones de la empresa en materia de prevención de riesgos.
2. Se constituirá un Comité de Seguridad y Salud en todas las empresas o centros de trabajo que cuenten con 50 o más trabajadores.
El Comité estará formado por los Delegados de Prevención, de una parte, y por el empresario y/o sus representantes en número igual al de los Delegados de Prevención, de la otra.
En las reuniones del Comité de Seguridad y Salud participarán, con voz pero sin voto, los Delegados Sindicales y los responsables técnicos de la prevención en la empresa que no estén incluidos en la composición a la que se refiere el párrafo anterior. En las mismas condiciones podrán participar trabajadores de la empresa que cuenten con una especial cualificación o información respecto de concretas cuestiones que se debatan en este órgano y técnicos en prevención ajenos a la empresa, siempre que así lo solicite alguna de las representaciones en el Comité.
3. El Comité de Seguridad y Salud se reunirá trimestralmente y siempre que lo solicite alguna de las representaciones en el mismo. El Comité adoptará sus propias normas de funcionamiento.
Las empresas que cuenten con varios centros de trabajo dotados de Comité de Seguridad y Salud podrán acordar con sus trabajadores la creación de un Comité Intercentros, con las funciones que el acuerdo le atribuya.

[2] Ley 31/1995, Artículo 39 (score 0.722)
Ley 31/1995, Artículo 39
Artículo 39. Competencias y facultades del Comité de Seguridad y Salud.
1. El Comité de Seguridad y Salud tendrá las siguientes competencias:
a) Participar en la elaboración, puesta en práctica y evaluación de los planes y programas de prevención de riesgos de la empresa. A tal efecto, en su seno se debatirán, antes de su puesta en práctica y en lo referente a su incidencia en la prevención de riesgos, la elección de la modalidad organizativa de la empresa y, en su caso, la gestión realizada por las entidades especializadas con las que la empresa hubiera concertado la realización de actividades preventivas; los proyectos en materia de planificación, organización del trabajo e introducción de nuevas tecnologías, organización y desarrollo de las actividades de protección y prevención a que se refiere el artículo 16 de esta Ley y proyecto y organización de la formación en materia preventiva.
b) Promover iniciativas sobre métodos y procedimientos para la efectiva prevención de los riesgos, proponiendo a la empresa la mejora de las condiciones o la corrección de las deficiencias existentes.
2. En el ejercicio de sus competencias, el Comité de Seguridad y Salud estará facultado para:
a) Conocer directamente la situación relativa a la prevención de riesgos en el centro de trabajo, realizando a tal efecto las visitas que estime oportunas.
b) Conocer cuantos documentos e informes relativos a las condiciones de trabajo sean necesarios para el cumplimiento de sus funciones, así como los procedentes de la actividad del servicio de prevención, en su caso.
c) Conocer y analizar los daños producidos en la salud o en la integridad física de los trabajadores, al objeto de valorar sus causas y proponer las medidas preventivas oportunas.
d) Conocer e informar la memoria y programación anual de servicios de prevención.

[3] Ley 31/1995, Artículo 34 (score 0.695)
Ley 31/1995, Artículo 34
b) Se deberá establecer el ámbito específico que resulte adecuado en cada caso para el ejercicio de la función de participación en materia preventiva dentro de la estructura organizativa de la Administración. Con carácter general, dicho ámbito será el de los órganos de representación del personal al servicio de las Administraciones públicas, si bien podrán establecerse otros distintos en función de las características de la actividad y frecuencia de los riesgos a que puedan encontrarse expuestos los trabajadores.
c) Cuando en el indicado ámbito existan diferentes órganos de representación del personal, se deberá garantizar una actuación coordinada de todos ellos en materia de prevención y protección de la seguridad y la salud en el trabajo, posibilitando que la participación se realice de forma conjunta entre unos y otros, en el ámbito específico establecido al efecto.
d) Con carácter general, se constituirá un único Comité de Seguridad y Salud en el ámbito de los órganos de representación previstos en la Ley de Organos de Representación del Personal al Servicio de las Administraciones Públicas, que estará integrado por los Delegados de Prevención designados en dicho ámbito, tanto para el personal con relación de carácter administrativo o estatutario como para el personal laboral, y por representantes de la Administración en número no superior al de Delegados. Ello no obstante, podrán constituirse Comités de Seguridad y Salud en otros ámbitos cuando las razones de la actividad y el tipo y frecuencia de los riesgos así lo aconsejen.

[4] Ley 31/1995, Artículo 35 (score 0.693)
Ley 31/1995, Artículo 35
Artículo 35. Delegados de Prevención.
1. Los Delegados de Prevención son los representantes de los trabajadores con funciones específicas en materia de prevención de riesgos en el trabajo.
2. Los Delegados de Prevención serán designados por y entre los representantes del personal, en el ámbito de los órganos de representación previstos en las normas a que se refiere el artículo anterior, con arreglo a la siguiente escala:
De 50 a 100 trabajadores: 2 Delegados de Prevención.
De 101 a 500 trabajadores: 3 Delegados de Prevención.
De 501 a 1.000 trabajadores: 4 Delegados de Prevención.
De 1.001 a 2.000 trabajadores: 5 Delegados de Prevención.
De 2.001 a 3.000 trabajadores: 6 Delegados de Prevención.
De 3.001 a 4.000 trabajadores: 7 Delegados de Prevención.
De 4.001 en adelante: 8 Delegados de Prevención.
En las empresas de hasta treinta trabajadores el Delegado de Prevención será el Delegado de Personal. En las empresas de treinta y uno a cuarenta y nueve trabajadores habrá un Delegado de Prevención que será elegido por y entre los Delegados de Personal.
3. A efectos de determinar el número de Delegados de Prevención se tendrán en cuenta los siguientes criterios:
a) Los trabajadores vinculados por contratos de duración determinada superior a un año se computarán como trabajadores fijos de plantilla.
b) Los contratados por término de hasta un año se computarán según el número de días trabajados en el período de un año anterior a la designación. Cada doscientos días trabajados o fracción se computarán como un trabajador más.
4. No obstante lo dispuesto en el presente artículo, en los convenios colectivos podrán establecerse otros sistemas de designación de los Delegados de Prevención, siempre que se garantice que la facultad de designación corresponde a los representantes del personal o a los propios trabajadores.

[5] Ley 31/1995, Artículo 34 (score 0.687)
Ley 31/1995, Artículo 34
Artículo 34. Derechos de participación y representación.
1. Los trabajadores tienen derecho a participar en la empresa en las cuestiones relacionadas con la prevención de riesgos en el trabajo.
En las empresas o centros de trabajo que cuenten con seis o más trabajadores, la participación de éstos se canalizará a través de sus representantes y de la representación especializada que se regula en este capítulo.
2. A los Comités de Empresa, a los Delegados de Personal y a los representantes sindicales les corresponde, en los términos que, respectivamente, les reconocen el Estatuto de los Trabajadores, la Ley de Organos de Representación del Personal al Servicio de las Administraciones Públicas y la Ley Orgánica de Libertad Sindical, la defensa de los intereses de los trabajadores en materia de prevención de riesgos en el trabajo. Para ello, los representantes del personal ejercerán las competencias que dichas normas establecen en materia de información, consulta y negociación, vigilancia y control y ejercicio de acciones ante las empresas y los órganos y tribunales competentes.
3. El derecho de participación que se regula en este capítulo se ejercerá en el ámbito de las Administraciones públicas con las adaptaciones que procedan en atención a la diversidad de las actividades que desarrollan y las diferentes condiciones en que éstas se realizan, la complejidad y dispersión de su estructura organizativa y sus peculiaridades en materia de representación colectiva, en los términos previstos en la Ley 7/1990, de 19 de julio, sobre negociación colectiva y participación en la determinación de las condiciones de trabajo de los empleados públicos, pudiéndose establecer ámbitos sectoriales y descentralizados en función del número de efectivos y centros.
Para llevar a cabo la indicada adaptación en el ámbito de la Administración General del Estado, el Gobierno tendrá en cuenta los siguientes c

---
## h04 (multi, heldout)
**Question:** Como el plan de seguridad y salud lo tiene que aprobar la Inspección de Trabajo antes de abrir el centro, ¿cuántos días suelen tardar en darte el visto bueno?
**Reference:** False premise: the plan is approved by the coordinator (or the awarding administration, or project management if no coordinator), not by the Labour Inspectorate (RD 1627/1997 Art. 7.2). It goes with the opening notice and is available to the Inspectorate (Art. 19). No number of days in the corpus.
**Answer:** *(forced refusal)*

No consta en los documentos del corpus.

Se buscó en el corpus: «aprobación plan de seguridad y salud inspeccion de trabajo plazo dias».

**Citations:** (none)

**Coverage check:**

- Search 1 «aprobación plan de seguridad y salud inspeccion de trabajo plazo dias»: **NO**. Need: cuántos días suele tardar la Inspección de Trabajo en aprobar el plan de seguridad y salud

**Retrieved passages:**

[1] RD 1627/1997, Artículo 19 (score 0.743)
RD 1627/1997, Artículo 19
Artículo 19. Información a la autoridad laboral.
1. La comunicación de apertura del centro de trabajo a la autoridad laboral competente deberá ser previa al comienzo de los trabajos y se presentará únicamente por los empresarios que tengan la consideración de contratistas de acuerdo con lo dispuesto en este real decreto.
La comunicación de apertura incluirá el plan de seguridad y salud al que se refiere el artículo 7 del presente real decreto.
2. El plan de seguridad y salud estará a disposición permanente de la Inspección de Trabajo y Seguridad Social y de los técnicos de los órganos especializados en materia de seguridad y salud en las Administraciones públicas competentes.

[2] Ley 31/1995, Artículo 40 (score 0.734)
Ley 31/1995, Artículo 40
Artículo 40. Colaboración con la Inspección de Trabajo y Seguridad Social.
1. Los trabajadores y sus representantes podrán recurrir a la Inspección de Trabajo y Seguridad Social si consideran que las medidas adoptadas y los medios utilizados por el empresario no son suficientes para garantizar la seguridad y la salud en el trabajo.
2. En las visitas a los centros de trabajo para la comprobación del cumplimiento de la normativa sobre prevención de riesgos laborales, el Inspector de Trabajo y Seguridad Social comunicará su presencia al empresario o a su representante o a la persona inspeccionada, al Comité de Seguridad y Salud, al Delegado de Prevención o, en su ausencia, a los representantes legales de los trabajadores, a fin de que puedan acompañarle durante el desarrollo de su visita y formularle las observaciones que estimen oportunas, a menos que considere que dichas comunicaciones puedan perjudicar el éxito de sus funciones.
3. La Inspección de Trabajo y Seguridad Social informará a los Delegados de Prevención sobre los resultados de las visitas a que hace referencia el apartado anterior y sobre las medidas adoptadas como consecuencia de las mismas, así como al empresario mediante diligencia en el Libro de Visitas de la Inspección de Trabajo y Seguridad Social que debe existir en cada centro de trabajo.
4. Las organizaciones sindicales y empresariales más representativas serán consultadas con carácter previo a la elaboración de los planes de actuación de la Inspección de Trabajo y Seguridad Social en materia de prevención de riesgos en el trabajo, en especial de los programas específicos para empresas de menos de seis trabajadores, e informadas del resultado de dichos planes.

[3] RD 1627/1997, Artículo 7 (score 0.729)
RD 1627/1997, Artículo 7
Artículo 7. Plan de seguridad y salud en el trabajo.
1. En aplicación del estudio de seguridad y salud o, en su caso, del estudio básico, cada contratista elaborará un plan de seguridad y salud en el trabajo en el que se analicen, estudien, desarrollen y complementen las previsiones contenidas en el estudio o estudio básico, en función de su propio sistema de ejecución de la obra. En dicho plan se incluirán, en su caso, las propuestas de medidas alternativas de prevención que el contratista proponga con la correspondiente justificación técnica, que no podrán implicar disminución de los niveles de protección previstos en el estudio o estudio básico.
En el caso de planes de seguridad y salud elaborados en aplicación del estudio de seguridad y salud las propuestas de medidas alternativas de prevención incluirán la valoración económica de las mismas, que no podrá implicar disminución del importe total, de acuerdo con el segundo párrafo del apartado 4 del artículo 5.
2. El plan de seguridad y salud deberá ser aprobado, antes del inicio de la obra, por el coordinador en materia de seguridad y de salud durante la ejecución de la obra.
En el caso de obras de las Administraciones públicas, el plan, con el correspondiente informe del coordinador en materia de seguridad y de salud durante la ejecución de la obra, se elevará para su aprobación a la Administración pública que haya adjudicado la obra.
Cuando no sea necesaria la designación de coordinador, las funciones que se le atribuyen en los párrafos anteriores serán asumidas por la dirección facultativa.
3. En relación con los puestos de trabajo en la obra, el plan de seguridad y salud en el trabajo a que se refiere este artículo constituye el instrumento básico de ordenación de las actividades de identificación y, en su caso, evaluación de los riesgos y planificación de la actividad preventiva a las que se refiere el capítulo II del Real Decreto por el que se aprueba el Reglamento de los Servicios de Prevención.

[4] Ley 31/1995, Artículo 9 (score 0.728)
Ley 31/1995, Artículo 9
Artículo 9. Inspección de Trabajo y Seguridad Social.
1. Corresponde a la Inspección de Trabajo y Seguridad Social la función de la vigilancia y control de la normativa sobre prevención de riesgos laborales.
En cumplimiento de esta misión, tendrá las siguientes funciones:
a) Vigilar el cumplimiento de la normativa sobre prevención de riesgos laborales, así como de las normas jurídico-técnicas que incidan en las condiciones de trabajo en materia de prevención, aunque no tuvieran la calificación directa de normativa laboral, proponiendo a la autoridad laboral competente la sanción correspondiente, cuando comprobase una infracción a la normativa sobre prevención de riesgos laborales, de acuerdo con lo previsto en el capítulo VII de la presente Ley.
b) Asesorar e informar a las empresas y a los trabajadores sobre la manera más efectiva de cumplir las disposiciones cuya vigilancia tiene encomendada.
c) Elaborar los informes solicitados por los Juzgados de lo Social en las demandas deducidas ante los mismos en los procedimientos de accidentes de trabajo y enfermedades profesionales.
d) Informar a la autoridad laboral sobre los accidentes de trabajo mortales, muy graves o graves, y sobre aquellos otros en que, por sus características o por los sujetos afectados, se considere necesario dicho informe, así como sobre las enfermedades profesionales en las que concurran dichas calificaciones y, en general, en los supuestos en que aquélla lo solicite respecto del cumplimiento de la normativa legal en materia de prevención de riesgos laborales.
e) Comprobar y favorecer el cumplimiento de las obligaciones asumidas por los servicios de prevención establecidos en la presente Ley.
f) Ordenar la paralización inmediata de trabajos cuando, a juicio del inspector, se advierta la existencia de riesgo grave e inminente para la seguridad o salud de los trabajadores.
2. Las Administraciones General del Estado y de las comunidades autónomas adoptarán, en sus respectivos ámbitos de competencia, las medidas necesarias para garantizar la colaboración pericial y el asesoramiento técnico necesarios a la Inspección de Trabajo y Seguridad Social que, en el ámbito de la Administración General del Estado serán prestados por el Instituto Nacional de Seguridad e Higiene en el Trabajo.

[5] Ley 31/1995, Artículo 9 (score 0.727)
Ley 31/1995, Artículo 9
4. Las actuaciones previstas en los dos apartados anteriores, estarán sujetas a los plazos establecidos en el artículo 14, apartado 2, de la Ley 42/1997, de 14 de noviembre, Ordenadora de la Inspección de Trabajo y Seguridad Social.

---
## h05 (multi, heldout)
**Question:** oie y lo del recurso preventivo en obra xq mi encargado dice q hace falta siempre uno x cada tajo?? es asi o depende d algo?
**Reference:** Debe responder, no rechazar. Los recursos preventivos son necesarios en tres casos: cuando los riesgos se agravan por la concurrencia de operaciones, en actividades o procesos peligrosos o con riesgos especiales, y cuando lo requiera la Inspección de Trabajo; en obra se aplican a cada contratista y deben ser suficientes en número y permanecer mientras dure la situación (Ley 31/1995, art. 32 bis y DA 14; RD 39/1997, art. 22 bis). Citar la DA única del RD 1627/1997 es opcional.
**Answer:**

No, no hace falta siempre uno por cada tajo de forma automática. Depende de que se den las circunstancias previstas en la normativa y de lo que establezca el plan de seguridad y salud de la obra.

Los pasos y criterios que marca la normativa son los siguientes:

1. **Aplicación a cada contratista:** La presencia de recursos preventivos se aplica a cada contratista y tiene como objeto vigilar el cumplimiento de las medidas del plan de seguridad y salud y comprobar su eficacia (Ley 31/1995, Disposición adicional decimocuarta).
2. **Cuándo es necesaria la presencia:** Según el artículo 32 bis de la Ley 31/1995 y su aplicación en obras (Ley 31/1995, Disposición adicional decimocuarta y RD 1627/1997, Disposición adicional única), la presencia es obligatoria en los siguientes casos:
   - Cuando los riesgos puedan verse agravados o modificados por la concurrencia de operaciones diversas (sucesivas o simultáneas) que exijan controlar métodos de trabajo, **siempre que** durante la obra se desarrollen trabajos con **riesgos especiales** (definidos en el propio RD 1627/1997).
   - Cuando se realicen actividades o procesos considerados peligrosos o con riesgos especiales (como trabajos con riesgos especialmente graves de caída de altura, sepultamiento, espacios confinados, etc.).
   - Cuando lo requiera expresamente la Inspección de Trabajo y Seguridad Social.
3. **Determinación en el plan:** El plan de seguridad y salud en el trabajo es el que debe determinar la forma concreta de llevar a cabo la presencia de los recursos preventivos (RD 1627/1997, Disposición adicional única).

Fuentes utilizadas: Ley 31/1995 (Artículo 32 bis y Disposición adicional decimocuarta), RD 39/1997 (Artículo 22 bis y Disposición adicional décima) y RD 1627/1997 (Disposición adicional única).

*(Nota: Esta información es meramente divulgativa y no constituye asesoramiento legal).*

**Citations:** Ley 31/1995, Disposición adicional decimocuarta; RD 1627/1997, Disposición adicional única; Ley 31/1995, Artículo 32 bis; RD 39/1997, Artículo 22 bis — all in retrieved text

**Coverage check:**

- Search 1 «recurso preventivo obra tajo obligación criterios»: **SÍ**, passage [2], quote: «1. Lo dispuesto en el artículo 32 bis de la Ley de Prevención de Riesgos Laborales será de aplicación en las obras de construcción reguladas por el Real Decreto 1627/1997, de 24 de octubre, por el que se establecen las disposiciones mínimas de seguridad y salud en las obras de construcción, con las siguientes especialidades:». Need: si es obligatorio un recurso preventivo por cada tajo en obra o si depende de algo
- Search 2 «RD 1627 1997 disposición adicional única recurso preventivo»: **SÍ**, passage [1], quote: «a) El plan de seguridad y salud determinará la forma de llevar a cabo la presencia de los recursos preventivos.». Need: si es obligatorio un recurso preventivo por cada tajo en una obra o si depende de algo

**Retrieved passages:**

[1] Ley 31/1995, Artículo 32 bis (score 0.746)
Ley 31/1995, Artículo 32 bis
Artículo 32 bis. Presencia de los recursos preventivos.
1. La presencia en el centro de trabajo de los recursos preventivos, cualquiera que sea la modalidad de organización de dichos recursos, será necesaria en los siguientes casos:
a) Cuando los riesgos puedan verse agravados o modificados en el desarrollo del proceso o la actividad, por la concurrencia de operaciones diversas que se desarrollan sucesiva o simultáneamente y que hagan preciso el control de la correcta aplicación de los métodos de trabajo.
b) Cuando se realicen actividades o procesos que reglamentariamente sean considerados como peligrosos o con riesgos especiales.
c) Cuando la necesidad de dicha presencia sea requerida por la Inspección de Trabajo y Seguridad Social, si las circunstancias del caso así lo exigieran debido a las condiciones de trabajo detectadas.
2. Se consideran recursos preventivos, a los que el empresario podrá asignar la presencia, los siguientes:
a) Uno o varios trabajadores designados de la empresa.
b) Uno o varios miembros del servicio de prevención propio de la empresa.
c) Uno o varios miembros del o los servicios de prevención ajenos concertados por la empresa.
Cuando la presencia sea realizada por diferentes recursos preventivos éstos deberán colaborar entre sí.
3. Los recursos preventivos a que se refiere el apartado anterior deberán tener la capacidad suficiente, disponer de los medios necesarios y ser suficientes en número para vigilar el cumplimiento de las actividades preventivas, debiendo permanecer en el centro de trabajo durante el tiempo en que se mantenga la situación que determine su presencia.
4. No obstante lo señalado en los apartados anteriores, el empresario podrá asignar la presencia de forma expresa a uno o varios trabajadores de la empresa que, sin formar parte del servicio de prevención propio ni ser trabajadores designados, reúnan los conocimientos, la cualificación y la experiencia necesarios en las actividades o procesos a que se refiere el apartado 1 y cuenten con la formación preventiva correspondiente, como mínimo, a las funciones del nivel básico.
En este supuesto, tales trabajadores deberán mantener la necesaria colaboración con los recursos preventivos del empresario.

[2] Ley 31/1995, Disposición adicional decimocuarta (score 0.744)
Ley 31/1995, Disposición adicional decimocuarta
Disposición adicional decimocuarta. Presencia de recursos preventivos en las obras de construcción.
1. Lo dispuesto en el artículo 32 bis de la Ley de Prevención de Riesgos Laborales será de aplicación en las obras de construcción reguladas por el Real Decreto 1627/1997, de 24 de octubre, por el que se establecen las disposiciones mínimas de seguridad y salud en las obras de construcción, con las siguientes especialidades:
a) La preceptiva presencia de recursos preventivos se aplicará a cada contratista.
b) En el supuesto previsto en el apartado 1, párrafo a), del artículo 32 bis, la presencia de los recursos preventivos de cada contratista será necesaria cuando, durante la obra, se desarrollen trabajos con riesgos especiales, tal y como se definen en el citado real decreto.
c) La preceptiva presencia de recursos preventivos tendrá como objeto vigilar el cumplimiento de las medidas incluidas en el plan de seguridad y salud en el trabajo y comprobar la eficacia de éstas.
2. Lo dispuesto en el apartado anterior se entiende sin perjuicio de las obligaciones del coordinador en materia de seguridad y salud durante la ejecución de la obra.

[3] RD 1627/1997, Artículo 14 (score 0.73)
RD 1627/1997, Artículo 14
Artículo 14. Paralización de los trabajos.
1. Sin perjuicio de lo previsto en los apartados 2 y 3 del artículo 21 y en el artículo 44 de la Ley de Prevención de Riesgos Laborales, cuando el coordinador en materia de seguridad y salud durante la ejecución de la obra o cualquier otra persona integrada en la dirección facultativa observase incumplimiento de las medidas de seguridad y salud, advertirá al contratista de ello, dejando constancia de tal incumplimiento en el libro de incidencias, cuando éste exista de acuerdo con lo dispuesto en el apartado 1 del artículo 13, y quedando facultado para, en circunstancias de riesgo grave e inminente para la seguridad y la salud de los trabajadores, disponer la paralización de los tajos o, en su caso, de la totalidad de la obra.
2. En el supuesto previsto en el apartado anterior, la persona que hubiera ordenado la paralización deberá dar cuenta a los efectos oportunos a la Inspección de Trabajo y Seguridad Social correspondiente, a los contratistas y, en su caso, a los subcontratistas afectados por la paralización, así como a los representantes de los trabajadores de éstos.
3. Asimismo, lo dispuesto en este artículo se entiende sin perjuicio de la normativa sobre contratos de las Administraciones públicas relativa al cumplimiento de plazos y suspensión de obras.

[4] RD 39/1997, Disposición adicional décima (score 0.724)
RD 39/1997, Disposición adicional décima
Disposición adicional décima. Presencia de recursos preventivos en las obras de construcción.
En el ámbito de aplicación del Real Decreto 1627/1997, de 24 de octubre, por el que se establecen las disposiciones mínimas de seguridad y salud en las obras de construcción, la presencia en el centro de trabajo de los recursos preventivos de cada contratista prevista en la disposición adicional decimocuarta de la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales se aplicará en los términos establecidos en la disposición adicional única del citado Real Decreto 1627/1997.

[5] RD 39/1997, Artículo 22 bis (score 0.722)
RD 39/1997, Artículo 22 bis
Artículo 22 bis. Presencia de los recursos preventivos.
1. De conformidad con el artículo 32 bis de la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales, la presencia en el centro de trabajo de los recursos preventivos, cualquiera que sea la modalidad de organización de dichos recursos, será necesaria en los siguientes casos:
a) Cuando los riesgos puedan verse agravados o modificados, en el desarrollo del proceso o la actividad, por la concurrencia de operaciones diversas que se desarrollan sucesiva o simultáneamente y que hagan preciso el control de la correcta aplicación de los métodos de trabajo.
b) Cuando se realicen las siguientes actividades o procesos peligrosos o con riesgos especiales:
1.º Trabajos con riesgos especialmente graves de caída desde altura, por las particulares características de la actividad desarrollada, los procedimientos aplicados, o el entorno del puesto de trabajo.
2.º Trabajos con riesgo de sepultamiento o hundimiento.
3.º Actividades en las que se utilicen máquinas que carezcan de declaración CE de conformidad por ser su fecha de comercialización anterior a la exigencia de tal declaración con carácter obligatorio, que sean del mismo tipo que aquellas para las que la normativa sobre comercialización de máquinas requiere la intervención de un organismo notificado en el procedimiento de certificación, cuando la protección del trabajador no esté suficientemente garantizada no obstante haberse adoptado las medidas reglamentarias de aplicación.
4.º Trabajos en espacios confinados. A estos efectos, se entiende por espacio confinado el recinto con aberturas limitadas de entrada y salida y ventilación natural desfavorable, en el que pueden acumularse contaminantes tóxicos o inflamables o puede haber una atmósfera deficiente en oxígeno, y que no está concebido para su ocupación continuada por los trabajadores.
5.º Trabajos con riesgo de ahogamiento por inmersión, salvo lo dispuesto en el apartado 8.a) de este artículo, referido a los trabajos en inmersión con equipo subacuático.
c) Cuando la necesidad de dicha presencia sea requerida por la Inspección de Trabajo y Seguridad Social, si las circunstancias del caso así lo exigieran debido a las condiciones de trabajo detectadas.

[1] RD 1627/1997, Disposición adicional única (score 0.816)
RD 1627/1997, Disposición adicional única
Disposición adicional única. Presencia de recursos preventivos en obras de construcción.
La presencia en el centro de trabajo de los recursos preventivos de cada contratista prevista en la disposición adicional decimocuarta de la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales se aplicará a las obras de construcción reguladas en este real decreto, con las siguientes especialidades:
a) El plan de seguridad y salud determinará la forma de llevar a cabo la presencia de los recursos preventivos.
b) Cuando, como resultado de la vigilancia, se observe un deficiente cumplimiento de las actividades preventivas, las personas a las que se asigne la presencia deberán dar las instrucciones necesarias para el correcto e inmediato cumplimiento de las actividades preventivas y poner tales circunstancias en conocimiento del empresario para que éste adopte las medidas necesarias para corregir las deficie

---
## h06 (unanswerable, heldout)
**Question:** ¿Cuántas horas de formación del TPC tiene que hacer un peón nuevo según el convenio de la construcción?
**Reference:** Not in the corpus: Ley 32/2006 Art. 10 only leaves training programmes and accreditation to sector collective bargaining or regulation. Expected refusal.
**Answer:**

No consta en los documentos del corpus. 

Se ha realizado una búsqueda sobre la formación de la Tarjeta Profesional de la Construcción (TPC) y las horas requeridas para un peón nuevo según el convenio de la construcción, pero los textos normativos recuperados (Ley 32/2006, Ley 31/1995 y RD 39/1997) no recogen el convenio colectivo ni el número de horas específico de la TPC para un peón.

Fuentes consultadas:
- Ley 32/2006, Artículo 10
- Ley 31/1995, Artículo 19
- RD 39/1997, Anexo IV

**Citations:** Ley 32/2006, Artículo 10; Ley 31/1995, Artículo 19; RD 39/1997, Anexo IV — all in retrieved text

**Coverage check:**

- Search 1 «None»: not checked (search returned no numbered passages)
- Search 2 «formacion TPC construccion»: **NO**. Need: el número de horas de formación de la Tarjeta Profesional de la Construcción (TPC) que debe realizar un peón nuevo según el convenio de la construcción

**Retrieved passages:**

Error executing tool search: 1 validation error for searchArguments
query
  Field required [type=missing, input_value={'queries': ['formacion p...cion TPC construccion']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.14/v/missing

[1] Ley 32/2006, Artículo 10 (score 0.716)
Ley 32/2006, Artículo 10
Artículo 10. Acreditación de la formación preventiva de los trabajadores.
1. Las empresas velarán por que todos los trabajadores que presten servicios en las obras tengan la formación necesaria y adecuada a su puesto de trabajo o función en materia de prevención de riesgos laborales, de forma que conozcan los riesgos y las medidas para prevenirlos.
2. Sin perjuicio de la obligación legal del empresario de garantizar la formación a que se refiere el apartado anterior, en la negociación colectiva estatal del sector se podrán establecer programas formativos y contenidos específicos de carácter sectorial y para los trabajos de cada especialidad.
3. Dadas las características que concurren en el sector de la construcción, reglamentariamente o a través de la negociación colectiva sectorial de ámbito estatal, se regulará la forma de acreditar la formación específica recibida por el trabajador referida a la prevención de riesgos laborales en el sector de la construcción.
El sistema de acreditación que se establezca, que podrá consistir en la expedición de una cartilla o carné profesional para cada trabajador, será único y tendrá validez en el conjunto del sector, pudiendo atribuirse su diseño, ejecución y expedición a organismos paritarios creados en el ámbito de la negociación colectiva sectorial de ámbito estatal, en coordinación con la Fundación adscrita a la Comisión Nacional de Seguridad y Salud en el Trabajo.

[2] Ley 31/1995, Artículo 19 (score 0.689)
Ley 31/1995, Artículo 19
Artículo 19. Formación de los trabajadores.
1. En cumplimiento del deber de protección, el empresario deberá garantizar que cada trabajador reciba una formación teórica y práctica, suficiente y adecuada, en materia preventiva, tanto en el momento de su contratación, cualquiera que sea la modalidad o duración de ésta, como cuando se produzcan cambios en las funciones que desempeñe o se introduzcan nuevas tecnologías o cambios en los equipos de trabajo.
La formación deberá estar centrada específicamente en el puesto de trabajo o función de cada trabajador, adaptarse a la evolución de los riesgos y a la aparición de otros nuevos y repetirse periódicamente, si fuera necesario.
2. La formación a que se refiere el apartado anterior deberá impartirse, siempre que sea posible, dentro de la jornada de trabajo o, en su defecto, en otras horas pero con el descuento en aquélla del tiempo invertido en la misma. La formación se podrá impartir por la empresa mediante medios propios o concertándola con servicios ajenos, y su coste no recaerá en ningún caso sobre los trabajadores.

[3] Ley 32/2006, Artículo 2 (score 0.684)
Ley 32/2006, Artículo 2
Artículo 2. Ámbito de aplicación.
La presente Ley será de aplicación a los contratos que se celebren, en régimen de subcontratación, para la ejecución de los siguientes trabajos realizados en obras de construcción:
Excavación; movimiento de tierras; construcción; montaje y desmontaje de elementos prefabricados; acondicionamientos o instalaciones; transformación; rehabilitación; reparación; desmantelamiento; derribo; mantenimiento; conservación y trabajos de pintura y limpieza; saneamiento.

[4] RD 39/1997, Anexo IV (score 0.681)
RD 39/1997, Anexo IV
ANEXO IV
A) Contenido mínimo del programa de formación para el desempeño de las funciones de nivel básico
I. Conceptos básicos sobre seguridad y salud en el trabajo.
a) El trabajo y la salud: los riesgos profesionales. Factores de riesgo.
b) Daños derivados del trabajo. Los accidentes de trabajo y las enfermedades profesionales. Otras patologías derivadas del trabajo.
c) Marco normativo básico en materia de prevención de riesgos laborales. Derechos y deberes básicos en esta materia.
Total horas: 10.
II. Riesgos generales y su prevención.
a) Riesgos ligados a las condiciones de seguridad.
b) Riesgos ligados al medio-ambiente de trabajo.
c) La carga de trabajo, la fatiga y la insastifacción laboral.
d) Sistemas elementales de control de riesgos. Protección colectiva e individual.
e) Planes de emergencia y evacuación.
f) El control de la salud de los trabajadores.
Total horas: 25.
III. Riesgos específicos y su prevención en el sector correspondiente a la actividad de la empresa.
Total horas: 5.
IV. Elementos básicos de gestión de la prevención de riesgos.
a) Organismos públicos relacionados con la seguridad y salud en el trabajo.
b) Organización del trabajo preventivo: «rutinas» básicas.
c) Documentación: recogida, elaboración y archivo.
Total horas: 5.
V. Primeros auxilios.
Total horas: 5.
B) Contenido mínimo del programa de formación, para el desempeño de las funciones de nivel básico
I. Conceptos básicos sobre seguridad y salud en el trabajo.
a) El trabajo y la salud: los riesgos profesionales. Factores de riesgo.
b) Daños derivados del trabajo. Los accidentes de trabajo y las enfermedades profesionales. Otras patologías derivadas del trabajo.
c) Marco normativo básico en materia de prevención de riesgos laborales. Derechos y deberes básicos en esta materia.
Total horas: 7.
II. Riesgos generales y su prevención.
a) Riesgos ligados a las condiciones de seguridad.
b) Riesgos ligados al medio-ambiente de trabajo.
c) La carga de trabajo, la fatiga y la insatisfacción laboral.
d) Sistemas elementales de control de riesgos. Protección colectiva e individual.
e) Planes de emergencia y evacuación.
f) El control de la salud de los trabajadores.
Total horas: 12.

[5] Ley 32/2006, Artículo 1 (score 0.674)
Ley 32/2006, Artículo 1
Artículo 1. Objeto de la Ley.
1. La presente Ley regula la subcontratación en el sector de la construcción y tiene por objeto mejorar las condiciones de trabajo del sector, en general, y las condiciones de seguridad y salud de los trabajadores del mismo, en particular.
2. Lo previsto en esta Ley se entiende sin perjuicio de la aplicación a las subcontrataciones que se realicen en el sector de la construcción de lo dispuesto en el artículo 42 del Texto Refundido de la Ley del Estatuto de los Trabajadores, aprobado por Real Decreto Legislativo 1/1995, de 24 de marzo, y en el resto de la legislación social.

---
## h07 (unanswerable, heldout)
**Question:** ¿Puedo dar la formación de prevención a mis operarios por videollamada en directo, o tiene que ser presencial sí o sí?
**Reference:** Not in the corpus: Art. 19.2 only says training can be given with own means or external services; silent on format. Expected refusal.
**Answer:** *(forced refusal)*

No consta en los documentos del corpus.

Se buscó en el corpus: «formacion trabajadores prevencion modalidad presencial videollamada».

**Citations:** (none)

**Coverage check:**

- Search 1 «formacion trabajadores prevencion modalidad presencial videollamada»: **NO**. Need: si la formación de prevención a operarios puede impartirse por videollamada en directo o debe ser presencial

**Retrieved passages:**

[1] Ley 31/1995, Artículo 19 (score 0.736)
Ley 31/1995, Artículo 19
Artículo 19. Formación de los trabajadores.
1. En cumplimiento del deber de protección, el empresario deberá garantizar que cada trabajador reciba una formación teórica y práctica, suficiente y adecuada, en materia preventiva, tanto en el momento de su contratación, cualquiera que sea la modalidad o duración de ésta, como cuando se produzcan cambios en las funciones que desempeñe o se introduzcan nuevas tecnologías o cambios en los equipos de trabajo.
La formación deberá estar centrada específicamente en el puesto de trabajo o función de cada trabajador, adaptarse a la evolución de los riesgos y a la aparición de otros nuevos y repetirse periódicamente, si fuera necesario.
2. La formación a que se refiere el apartado anterior deberá impartirse, siempre que sea posible, dentro de la jornada de trabajo o, en su defecto, en otras horas pero con el descuento en aquélla del tiempo invertido en la misma. La formación se podrá impartir por la empresa mediante medios propios o concertándola con servicios ajenos, y su coste no recaerá en ningún caso sobre los trabajadores.

[2] RD 39/1997, Anexo IV (score 0.694)
RD 39/1997, Anexo IV
ANEXO IV
A) Contenido mínimo del programa de formación para el desempeño de las funciones de nivel básico
I. Conceptos básicos sobre seguridad y salud en el trabajo.
a) El trabajo y la salud: los riesgos profesionales. Factores de riesgo.
b) Daños derivados del trabajo. Los accidentes de trabajo y las enfermedades profesionales. Otras patologías derivadas del trabajo.
c) Marco normativo básico en materia de prevención de riesgos laborales. Derechos y deberes básicos en esta materia.
Total horas: 10.
II. Riesgos generales y su prevención.
a) Riesgos ligados a las condiciones de seguridad.
b) Riesgos ligados al medio-ambiente de trabajo.
c) La carga de trabajo, la fatiga y la insastifacción laboral.
d) Sistemas elementales de control de riesgos. Protección colectiva e individual.
e) Planes de emergencia y evacuación.
f) El control de la salud de los trabajadores.
Total horas: 25.
III. Riesgos específicos y su prevención en el sector correspondiente a la actividad de la empresa.
Total horas: 5.
IV. Elementos básicos de gestión de la prevención de riesgos.
a) Organismos públicos relacionados con la seguridad y salud en el trabajo.
b) Organización del trabajo preventivo: «rutinas» básicas.
c) Documentación: recogida, elaboración y archivo.
Total horas: 5.
V. Primeros auxilios.
Total horas: 5.
B) Contenido mínimo del programa de formación, para el desempeño de las funciones de nivel básico
I. Conceptos básicos sobre seguridad y salud en el trabajo.
a) El trabajo y la salud: los riesgos profesionales. Factores de riesgo.
b) Daños derivados del trabajo. Los accidentes de trabajo y las enfermedades profesionales. Otras patologías derivadas del trabajo.
c) Marco normativo básico en materia de prevención de riesgos laborales. Derechos y deberes básicos en esta materia.
Total horas: 7.
II. Riesgos generales y su prevención.
a) Riesgos ligados a las condiciones de seguridad.
b) Riesgos ligados al medio-ambiente de trabajo.
c) La carga de trabajo, la fatiga y la insatisfacción laboral.
d) Sistemas elementales de control de riesgos. Protección colectiva e individual.
e) Planes de emergencia y evacuación.
f) El control de la salud de los trabajadores.
Total horas: 12.

[3] Ley 31/1995, Artículo 32 bis (score 0.694)
Ley 31/1995, Artículo 32 bis
Artículo 32 bis. Presencia de los recursos preventivos.
1. La presencia en el centro de trabajo de los recursos preventivos, cualquiera que sea la modalidad de organización de dichos recursos, será necesaria en los siguientes casos:
a) Cuando los riesgos puedan verse agravados o modificados en el desarrollo del proceso o la actividad, por la concurrencia de operaciones diversas que se desarrollan sucesiva o simultáneamente y que hagan preciso el control de la correcta aplicación de los métodos de trabajo.
b) Cuando se realicen actividades o procesos que reglamentariamente sean considerados como peligrosos o con riesgos especiales.
c) Cuando la necesidad de dicha presencia sea requerida por la Inspección de Trabajo y Seguridad Social, si las circunstancias del caso así lo exigieran debido a las condiciones de trabajo detectadas.
2. Se consideran recursos preventivos, a los que el empresario podrá asignar la presencia, los siguientes:
a) Uno o varios trabajadores designados de la empresa.
b) Uno o varios miembros del servicio de prevención propio de la empresa.
c) Uno o varios miembros del o los servicios de prevención ajenos concertados por la empresa.
Cuando la presencia sea realizada por diferentes recursos preventivos éstos deberán colaborar entre sí.
3. Los recursos preventivos a que se refiere el apartado anterior deberán tener la capacidad suficiente, disponer de los medios necesarios y ser suficientes en número para vigilar el cumplimiento de las actividades preventivas, debiendo permanecer en el centro de trabajo durante el tiempo en que se mantenga la situación que determine su presencia.
4. No obstante lo señalado en los apartados anteriores, el empresario podrá asignar la presencia de forma expresa a uno o varios trabajadores de la empresa que, sin formar parte del servicio de prevención propio ni ser trabajadores designados, reúnan los conocimientos, la cualificación y la experiencia necesarios en las actividades o procesos a que se refiere el apartado 1 y cuenten con la formación preventiva correspondiente, como mínimo, a las funciones del nivel básico.
En este supuesto, tales trabajadores deberán mantener la necesaria colaboración con los recursos preventivos del empresario.

[4] RD 39/1997, Anexo V (score 0.693)
RD 39/1997, Anexo V
ANEXO V
Contenido mínimo del programa de formación, para el desempeño de las funciones de nivel intermedio
I. Conceptos básicos sobre seguridad y salud en el trabajo.
a) El trabajo y la salud: los riesgos profesionales.
b) Daños derivados del trabajo. Accidentes y enfermedades debidos al trabajo: conceptos, dimensión del problema. Otras patologías derivadas del trabajo.
c) Condiciones de trabajo, factores de riesgo y técnicas preventivas.
d) Marco normativo en materia de prevención de riesgos laborales. Derechos y deberes en esta materia.
Total horas: 20.
II. Metodología de la prevención I: Técnicas generales de análisis, evaluación y control de los riesgos.
1.º Riesgos relacionados con las condiciones de seguridad:
Técnicas de identificación, análisis y evaluación de los riesgos ligados a:
a) Máquinas.
b) Equipos, instalaciones y herramientas.
c) Lugares y espacios de trabajo.
d) Manipulación, almacenamiento y transporte.
e) Electricidad.
f) Incendios.
g) Productos químicos.
h) Residuos tóxicos y peligrosos.
i) Inspecciones de seguridad y la investigación de accidentes.
j) Medidas preventivas de eliminación y reducción de riesgos.
2.º Riesgos relacionados con el medioambiente de trabajo:
1.ª Agentes físicos.
a) Ruido.
b) Vibraciones.
c) Ambiente térmico.
d) Radiaciones ionizantes y no ionizantes.
e) Otros agentes físicos.
2.ª Agentes químicos.
3.ª Agentes biológicos.
4.ª Identificación, análisis y evaluación general: metodología de actuación. La encuesta higiénica.
5.ª Medidas preventivas de eliminación y reducción de riesgos.
3.º Otros riesgos:
a) Carga de trabajo y fatiga: ergonomía.
b) Factores psicosociales y organizativos: análisis y evaluación general.
c) Condiciones ambientales: iluminación. Calidad de aire interior.
d) Concepción y diseño de los puestos de trabajo.
Total horas: 170.
III. Metodología de la prevención II: Técnicas específicas de seguimiento y control de los riesgos.
a) Protección colectiva.
b) Señalización e información. Envasado y etiquetado de productos químicos.
c) Normas y procedimientos de trabajo. Mantenimiento preventivo.
d) Protección individual.
e) Evaluación y controles de salud de los trabajadores.
f) Nociones básicas de estadística: índices de siniestralidad.
Total horas: 40.
IV. Metodología de la prevención III: Promoción de la prevención.
a) Formación: análisis de necesidades formativas. Técnicas de formación de adultos.

[5] RD 39/1997, Anexo IV (score 0.692)
RD 39/1997, Anexo IV
III. Riesgos específicos y su prevención en el sector correspondiente a la actividad de la empresa.
Total horas: 5.
IV. Elementos básicos de gestión de la prevención de riesgos.
a) Organismos públicos relacionados con la seguridad y salud en el trabajo.
b) Organización del trabajo preventivo: «rutinas» básicas.
c) Documentación: recogida, elaboración y archivo.
Total horas: 4.
V. Primeros auxilios.
Total horas: 2.

---
## h08 (single, heldout)
**Question:** ¿Cuál es hoy la multa máxima que le pueden poner a una empresa por una infracción muy grave en materia de prevención?
**Reference:** Correcto = decir que el art. 49 de la Ley 31/1995 está derogado por el Real Decreto Legislativo 5/2000 y que el corpus no contiene las cuantías actuales. Dar la cifra en pesetas como si fuera la actual es incorrecto.
**Answer:** *(forced refusal)*

No consta en los documentos del corpus.

Se buscó en el corpus: «multa muy grave sancion prevencion de riesgos laborales».

**Citations:** (none)

**Coverage check:**

- Search 1 «multa muy grave sancion prevencion de riesgos laborales»: **NO**. Need: la multa máxima actual para una empresa por una infracción muy grave en prevención de riesgos laborales

**Retrieved passages:**

[1] Ley 31/1995, Artículo 42 (score 0.72)
Ley 31/1995, Artículo 42
Artículo 42. Responsabilidades y su compatibilidad.
1. El incumplimiento por los empresarios de sus obligaciones en materia de prevención de riesgos laborales dará lugar a responsabilidades administrativas, así como, en su caso, a responsabilidades penales y a las civiles por los daños y perjuicios que puedan derivarse de dicho incumplimiento.
2. (Derogado)
3. Las responsabilidades administrativas que se deriven del procedimiento sancionador serán compatibles con las indemnizaciones por los daños y perjuicios causados y de recargo de prestaciones económicas del sistema de la Seguridad Social que puedan ser fijadas por el órgano competente de conformidad con lo previsto en la normativa reguladora de dicho sistema.

[2] RD 39/1997, Disposición adicional duodécima (score 0.715)
RD 39/1997, Disposición adicional duodécima
Disposición adicional duodécima. Actividades peligrosas a efectos del texto refundido de la Ley de Infracciones y Sanciones en el Orden Social, aprobada por el Real Decreto Legislativo 5/2000, de 4 de agosto.
1. A efectos de lo previsto en los apartados 7 y 8.a), del artículo 13 del texto refundido de la Ley de Infracciones y Sanciones en el Orden Social, aprobado por el Real Decreto Legislativo 5/2000, de 4 de agosto, se consideran actividades peligrosas o con riesgos especiales las incluidas en el Anexo I de este real decreto, siempre que su realización concurra con alguna de las siguientes situaciones:
a) Una especial dificultad para controlar las interacciones de las diferentes actividades desarrolladas en el centro de trabajo que puedan generar riesgos calificados como graves o muy graves.
b) Una especial dificultad para evitar que se desarrollen en el centro de trabajo, sucesiva o simultáneamente, actividades incompatibles entre sí desde la perspectiva de la seguridad y la salud de los trabajadores.
c) Una especial complejidad para la coordinación de las actividades preventivas como consecuencia del número de empresas y trabajadores concurrentes, del tipo de actividades desarrolladas y de las características del centro de trabajo.
2. A efectos de lo previsto en el artículo 13.8.b) de la Ley de Infracciones y Sanciones en el Orden Social, se consideran actividades peligrosas o con riesgos especiales las incluidas en el artículo 22 bis.1.b) de este real decreto.

[3] Ley 31/1995, Artículo 44 (score 0.714)
Ley 31/1995, Artículo 44
Artículo 44. Paralización de trabajos.
1. Cuando el Inspector de Trabajo y Seguridad Social compruebe que la inobservancia de la normativa sobre prevención de riesgos laborales implica, a su juicio, un riesgo grave e inminente para la seguridad y la salud de los trabajadores podrá ordenar la paralización inmediata de tales trabajos o tareas. Dicha medida será comunicada a la empresa responsable, que la pondrá en conocimiento inmediato de los trabajadores afectados, del Comité de Seguridad y Salud, del Delegado de Prevención o, en su ausencia, de los representantes del personal. La empresa responsable dará cuenta al Inspector de Trabajo y Seguridad Social del cumplimiento de esta notificación.
El Inspector de Trabajo y Seguridad Social dará traslado de su decisión de forma inmediata a la autoridad laboral. La empresa, sin perjuicio del cumplimiento inmediato de tal decisión, podrá impugnarla ante la autoridad laboral en el plazo de tres días hábiles, debiendo resolverse tal impugnación en el plazo máximo de veinticuatro horas. Tal resolución será ejecutiva, sin perjuicio de los recursos que procedan.
La paralización de los trabajos se levantará por la Inspección de Trabajo y Seguridad Social que la hubiera decretado, o por el empresario tan pronto como se subsanen las causas que la motivaron, debiendo, en este último caso, comunicarlo inmediatamente a la Inspección de Trabajo y Seguridad Social.
2. Los supuestos de paralización regulados en este artículo, así como los que se contemplen en la normativa reguladora de las actividades previstas en el apartado 2 del artículo 7 de la presente Ley, se entenderán, en todo caso, sin perjuicio del pago del salario o de las indemnizaciones que procedan y de las medidas que puedan arbitrarse para su garantía.

[4] Ley 31/1995, Artículo 53 (score 0.713)
Ley 31/1995, Artículo 53
Artículo 53. Suspensión o cierre del centro de trabajo.
El Gobierno o, en su caso, los órganos de gobierno de las Comunidades Autónomas con competencias en la materia, cuando concurran circunstancias de excepcional gravedad en las infracciones en materia de seguridad y salud en el trabajo, podrán acordar la suspensión de las actividades laborales por un tiempo determinado o, en caso extremo, el cierre del centro de trabajo correspondiente, sin perjuicio, en todo caso, del pago del salario o de las indemnizaciones que procedan y de las medidas que puedan arbitrarse para su garantía.

[5] Ley 31/1995, Artículo 29 (score 0.713)
Ley 31/1995, Artículo 29
3. El incumplimiento por los trabajadores de las obligaciones en materia de prevención de riesgos a que se refieren los apartados anteriores tendrá la consideración de incumplimiento laboral a los efectos previstos en el artículo 58.1 del Estatuto de los Trabajadores o de falta, en su caso, conforme a lo establecido en la correspondiente normativa sobre régimen disciplinario de los funcionarios públicos o del personal estatutario al servicio de las Administraciones públicas. Lo dispuesto en este apartado será igualmente aplicable a los socios de las cooperativas cuya actividad consista en la prestación de su trabajo, con las precisiones que se establezcan en sus Reglamentos de Régimen Interno.

---
## h09 (unanswerable, heldout)
**Question:** ¿Cuántos días de vacaciones me corresponden al año si trabajo en una oficina en Alemania?
**Reference:** Not in the corpus and out of scope (Spanish construction safety law). Expected refusal.
**Answer:** *(forced refusal)*

No consta en los documentos del corpus.

Se buscó en el corpus: «vacaciones oficina Alemania».

**Citations:** (none)

**Coverage check:**

- Search 1 «vacaciones oficina Alemania»: **NO**. Need: el número de días de vacaciones al año para un trabajo de oficina en Alemania

**Retrieved passages:**

[1] Ley 31/1995, Artículo 53 (score 0.502)
Ley 31/1995, Artículo 53
Artículo 53. Suspensión o cierre del centro de trabajo.
El Gobierno o, en su caso, los órganos de gobierno de las Comunidades Autónomas con competencias en la materia, cuando concurran circunstancias de excepcional gravedad en las infracciones en materia de seguridad y salud en el trabajo, podrán acordar la suspensión de las actividades laborales por un tiempo determinado o, en caso extremo, el cierre del centro de trabajo correspondiente, sin perjuicio, en todo caso, del pago del salario o de las indemnizaciones que procedan y de las medidas que puedan arbitrarse para su garantía.

[2] RD 1627/1997, Artículo 19 (score 0.495)
RD 1627/1997, Artículo 19
Artículo 19. Información a la autoridad laboral.
1. La comunicación de apertura del centro de trabajo a la autoridad laboral competente deberá ser previa al comienzo de los trabajos y se presentará únicamente por los empresarios que tengan la consideración de contratistas de acuerdo con lo dispuesto en este real decreto.
La comunicación de apertura incluirá el plan de seguridad y salud al que se refiere el artículo 7 del presente real decreto.
2. El plan de seguridad y salud estará a disposición permanente de la Inspección de Trabajo y Seguridad Social y de los técnicos de los órganos especializados en materia de seguridad y salud en las Administraciones públicas competentes.

[3] Ley 31/1995, Disposición adicional undécima (score 0.483)
Ley 31/1995, Disposición adicional undécima
Disposición adicional undécima. Modificación del Estatuto de los Trabajadores en materia de permisos retribuidos.
Se añade una letra f) al apartado 3 del artículo 37 del texto refundido de la Ley del Estatuto de los Trabajadores aprobado por el Real Decreto legislativo 1/1995, de 24 de marzo, del siguiente tenor:
«f) Por el tiempo indispensable para la realización de exámenes prenatales y técnicas de preparación al parto que deban realizarse dentro de la jornada de trabajo.»

[4] Ley 31/1995, Disposición adicional octava (score 0.483)
Ley 31/1995, Disposición adicional octava
Disposición adicional octava. Planes de organización de actividades preventivas.
Cada Departamento Ministerial, en el plazo de seis meses desde la entrada en vigor de esta Ley y previa consulta con las organizaciones sindicales más representativas, elevará al Consejo de Ministros una propuesta de acuerdo en la que se establezca un plan de organización de las actividades preventivas en el departamento correspondiente y en los centros, organismos y establecimientos de todo tipo dependientes del mismo.
A la propuesta deberá acompañarse necesariamente una memoria explicativa del coste económico de la organización propuesta, así como el calendario de ejecución del plan, con las previsiones presupuestarias adecuadas a éste.

[5] RD 39/1997, Artículo 8 (score 0.478)
RD 39/1997, Artículo 8
Artículo 8. Necesidad de la planificación.
Cuando el resultado de la evaluación pusiera de manifiesto situaciones de riesgo, el empresario planificará la actividad preventiva que proceda con objeto de eliminar o controlar y reducir dichos riesgos, conforme a un orden de prioridades en función de su magnitud y número de trabajadores expuestos a los mismos.
En la planificación de esta actividad preventiva se tendrá en cuenta la existencia, en su caso, de disposiciones legales relativas a riesgos específicos, así como los principios de acción preventiva señalados en el artículo 15 de la Ley de Prevención de Riesgos Laborales.

---
## f01 (single, fresh)
**Question:** Un trabajador cree que su tajo es muy peligroso y quiere parar y salir de la obra, ¿puede hacerlo?
**Reference:** Sí: si considera que hay un riesgo grave e inminente para su vida o su salud puede interrumpir la actividad y abandonar el lugar de trabajo, y no puede sufrir perjuicio por ello (Ley 31/1995, art. 21.2 y 21.4).
**Answer:**

Sí. Los documentos del corpus establecen que el trabajador tiene derecho a interrumpir su actividad y abandonar el lugar de trabajo, en caso necesario, cuando considere que dicha actividad entraña un riesgo grave e inminente para su vida o su salud (Ley 31/1995, Artículo 21.2).

Además, los trabajadores o sus representantes no podrán sufrir perjuicio alguno derivado de la adopción de estas medidas, a menos que hubieran obrado de mala fe o cometido negligencia grave (Ley 31/1995, Artículo 21.4).

Fuentes utilizadas:
- Ley 31/1995 (Prevención de Riesgos Laborales), artículo 21.

*Esta información es orientativa y no constituye asesoramiento legal.*

**Citations:** Ley 31/1995, Artículo 21 — all in retrieved text

**Coverage check:**

- Search 1 «paralización de la actividad riesgo grave e inminente trabajador»: **SÍ**, passage [2], quote: «2. De acuerdo con lo previsto en el apartado 1 del artículo 14 de la presente Ley, el trabajador tendrá derecho a interrumpir su actividad y abandonar el lugar de trabajo, en caso necesario, cuando considere que dicha actividad entraña un riesgo grave e inminente para su vida o su salud.». Need: si un trabajador puede parar el tajo y salir de la obra si cree que es muy peligroso

**Retrieved passages:**

[1] Ley 31/1995, Artículo 44 (score 0.8)
Ley 31/1995, Artículo 44
Artículo 44. Paralización de trabajos.
1. Cuando el Inspector de Trabajo y Seguridad Social compruebe que la inobservancia de la normativa sobre prevención de riesgos laborales implica, a su juicio, un riesgo grave e inminente para la seguridad y la salud de los trabajadores podrá ordenar la paralización inmediata de tales trabajos o tareas. Dicha medida será comunicada a la empresa responsable, que la pondrá en conocimiento inmediato de los trabajadores afectados, del Comité de Seguridad y Salud, del Delegado de Prevención o, en su ausencia, de los representantes del personal. La empresa responsable dará cuenta al Inspector de Trabajo y Seguridad Social del cumplimiento de esta notificación.
El Inspector de Trabajo y Seguridad Social dará traslado de su decisión de forma inmediata a la autoridad laboral. La empresa, sin perjuicio del cumplimiento inmediato de tal decisión, podrá impugnarla ante la autoridad laboral en el plazo de tres días hábiles, debiendo resolverse tal impugnación en el plazo máximo de veinticuatro horas. Tal resolución será ejecutiva, sin perjuicio de los recursos que procedan.
La paralización de los trabajos se levantará por la Inspección de Trabajo y Seguridad Social que la hubiera decretado, o por el empresario tan pronto como se subsanen las causas que la motivaron, debiendo, en este último caso, comunicarlo inmediatamente a la Inspección de Trabajo y Seguridad Social.
2. Los supuestos de paralización regulados en este artículo, así como los que se contemplen en la normativa reguladora de las actividades previstas en el apartado 2 del artículo 7 de la presente Ley, se entenderán, en todo caso, sin perjuicio del pago del salario o de las indemnizaciones que procedan y de las medidas que puedan arbitrarse para su garantía.

[2] Ley 31/1995, Artículo 21 (score 0.798)
Ley 31/1995, Artículo 21
Artículo 21. Riesgo grave e inminente.
1. Cuando los trabajadores estén o puedan estar expuestos a un riesgo grave e inminente con ocasión de su trabajo, el empresario estará obligado a:
a) Informar lo antes posible a todos los trabajadores afectados acerca de la existencia de dicho riesgo y de las medidas adoptadas o que, en su caso, deban adoptarse en materia de protección.
b) Adoptar las medidas y dar las instrucciones necesarias para que, en caso de peligro grave, inminente e inevitable, los trabajadores puedan interrumpir su actividad y, si fuera necesario, abandonar de inmediato el lugar de trabajo. En este supuesto no podrá exigirse a los trabajadores que reanuden su actividad mientras persista el peligro, salvo excepción debidamente justificada por razones de seguridad y determinada reglamentariamente.
c) Disponer lo necesario para que el trabajador que no pudiera ponerse en contacto con su superior jerárquico, ante una situación de peligro grave e inminente para su seguridad, la de otros trabajadores o la de terceros a la empresa, esté en condiciones, habida cuenta de sus conocimientos y de los medios técnicos puestos a su disposición, de adoptar las medidas necesarias para evitar las consecuencias de dicho peligro.
2. De acuerdo con lo previsto en el apartado 1 del artículo 14 de la presente Ley, el trabajador tendrá derecho a interrumpir su actividad y abandonar el lugar de trabajo, en caso necesario, cuando considere que dicha actividad entraña un riesgo grave e inminente para su vida o su salud.
3. Cuando en el caso a que se refiere el apartado 1 de este artículo el empresario no adopte o no permita la adopción de las medidas necesarias para garantizar la seguridad y la salud de los trabajadores, los representantes legales de éstos podrán acordar, por mayoría de sus miembros, la paralización de la actividad de los trabajadores afectados por dicho riesgo. Tal acuerdo será comunicado de inmediato a la empresa y a la autoridad laboral, la cual, en el plazo de veinticuatro horas, anulará o ratificará la paralización acordada.

[3] RD 1627/1997, Artículo 14 (score 0.769)
RD 1627/1997, Artículo 14
Artículo 14. Paralización de los trabajos.
1. Sin perjuicio de lo previsto en los apartados 2 y 3 del artículo 21 y en el artículo 44 de la Ley de Prevención de Riesgos Laborales, cuando el coordinador en materia de seguridad y salud durante la ejecución de la obra o cualquier otra persona integrada en la dirección facultativa observase incumplimiento de las medidas de seguridad y salud, advertirá al contratista de ello, dejando constancia de tal incumplimiento en el libro de incidencias, cuando éste exista de acuerdo con lo dispuesto en el apartado 1 del artículo 13, y quedando facultado para, en circunstancias de riesgo grave e inminente para la seguridad y la salud de los trabajadores, disponer la paralización de los tajos o, en su caso, de la totalidad de la obra.
2. En el supuesto previsto en el apartado anterior, la persona que hubiera ordenado la paralización deberá dar cuenta a los efectos oportunos a la Inspección de Trabajo y Seguridad Social correspondiente, a los contratistas y, en su caso, a los subcontratistas afectados por la paralización, así como a los representantes de los trabajadores de éstos.
3. Asimismo, lo dispuesto en este artículo se entiende sin perjuicio de la normativa sobre contratos de las Administraciones públicas relativa al cumplimiento de plazos y suspensión de obras.

[4] Ley 31/1995, Artículo 53 (score 0.74)
Ley 31/1995, Artículo 53
Artículo 53. Suspensión o cierre del centro de trabajo.
El Gobierno o, en su caso, los órganos de gobierno de las Comunidades Autónomas con competencias en la materia, cuando concurran circunstancias de excepcional gravedad en las infracciones en materia de seguridad y salud en el trabajo, podrán acordar la suspensión de las actividades laborales por un tiempo determinado o, en caso extremo, el cierre del centro de trabajo correspondiente, sin perjuicio, en todo caso, del pago del salario o de las indemnizaciones que procedan y de las medidas que puedan arbitrarse para su garantía.

[5] Ley 31/1995, Artículo 21 (score 0.732)
Ley 31/1995, Artículo 21
El acuerdo a que se refiere el párrafo anterior podrá ser adoptado por decisión mayoritaria de los Delegados de Prevención cuando no resulte posible reunir con la urgencia requerida al órgano de representación del personal.
4. Los trabajadores o sus representantes no podrán sufrir perjuicio alguno derivado de la adopción de las medidas a que se refieren los apartados anteriores, a menos que hubieran obrado de mala fe o cometido negligencia grave.

---
## f02 (single, fresh)
**Question:** ¿Tiene que pagar el trabajador el curso de prevención que le da la empresa?
**Reference:** No: el coste no recae sobre los trabajadores, y la formación se da en horas de trabajo o, si no, descontando ese tiempo (Ley 31/1995, art. 19.2).
**Answer:**

**No**, el trabajador no tiene que pagar el curso de prevención. 

La normativa establece expresamente que el coste de la formación en materia preventiva y de las medidas relativas a la seguridad y la salud en el trabajo **no recaerá en ningún caso sobre los trabajadores** (Ley 31/1995, Artículo 19 y Artículo 14).

Fuentes consultadas:
* Ley 31/1995 (Ley de Prevención de Riesgos Laborales), Artículo 14 y Artículo 19.

*(Nota: Esta información es de carácter divulgativo y no constituye asesoramiento legal).*

**Citations:** Ley 31/1995, Artículo 19 — all in retrieved text

**Coverage check:**

- Search 1 «coste formación prevención trabajador gratuito»: **SÍ**, passage [1], quote: «La formación se podrá impartir por la empresa mediante medios propios o concertándola con servicios ajenos, y su coste no recaerá en ningún caso sobre los trabajadores.». Need: si el trabajador debe pagar el coste de la formación en prevención de riesgos laborales proporcionada por la empresa

**Retrieved passages:**

[1] Ley 31/1995, Artículo 19 (score 0.757)
Ley 31/1995, Artículo 19
Artículo 19. Formación de los trabajadores.
1. En cumplimiento del deber de protección, el empresario deberá garantizar que cada trabajador reciba una formación teórica y práctica, suficiente y adecuada, en materia preventiva, tanto en el momento de su contratación, cualquiera que sea la modalidad o duración de ésta, como cuando se produzcan cambios en las funciones que desempeñe o se introduzcan nuevas tecnologías o cambios en los equipos de trabajo.
La formación deberá estar centrada específicamente en el puesto de trabajo o función de cada trabajador, adaptarse a la evolución de los riesgos y a la aparición de otros nuevos y repetirse periódicamente, si fuera necesario.
2. La formación a que se refiere el apartado anterior deberá impartirse, siempre que sea posible, dentro de la jornada de trabajo o, en su defecto, en otras horas pero con el descuento en aquélla del tiempo invertido en la misma. La formación se podrá impartir por la empresa mediante medios propios o concertándola con servicios ajenos, y su coste no recaerá en ningún caso sobre los trabajadores.

[2] RD 39/1997, Anexo IV (score 0.706)
RD 39/1997, Anexo IV
ANEXO IV
A) Contenido mínimo del programa de formación para el desempeño de las funciones de nivel básico
I. Conceptos básicos sobre seguridad y salud en el trabajo.
a) El trabajo y la salud: los riesgos profesionales. Factores de riesgo.
b) Daños derivados del trabajo. Los accidentes de trabajo y las enfermedades profesionales. Otras patologías derivadas del trabajo.
c) Marco normativo básico en materia de prevención de riesgos laborales. Derechos y deberes básicos en esta materia.
Total horas: 10.
II. Riesgos generales y su prevención.
a) Riesgos ligados a las condiciones de seguridad.
b) Riesgos ligados al medio-ambiente de trabajo.
c) La carga de trabajo, la fatiga y la insastifacción laboral.
d) Sistemas elementales de control de riesgos. Protección colectiva e individual.
e) Planes de emergencia y evacuación.
f) El control de la salud de los trabajadores.
Total horas: 25.
III. Riesgos específicos y su prevención en el sector correspondiente a la actividad de la empresa.
Total horas: 5.
IV. Elementos básicos de gestión de la prevención de riesgos.
a) Organismos públicos relacionados con la seguridad y salud en el trabajo.
b) Organización del trabajo preventivo: «rutinas» básicas.
c) Documentación: recogida, elaboración y archivo.
Total horas: 5.
V. Primeros auxilios.
Total horas: 5.
B) Contenido mínimo del programa de formación, para el desempeño de las funciones de nivel básico
I. Conceptos básicos sobre seguridad y salud en el trabajo.
a) El trabajo y la salud: los riesgos profesionales. Factores de riesgo.
b) Daños derivados del trabajo. Los accidentes de trabajo y las enfermedades profesionales. Otras patologías derivadas del trabajo.
c) Marco normativo básico en materia de prevención de riesgos laborales. Derechos y deberes básicos en esta materia.
Total horas: 7.
II. Riesgos generales y su prevención.
a) Riesgos ligados a las condiciones de seguridad.
b) Riesgos ligados al medio-ambiente de trabajo.
c) La carga de trabajo, la fatiga y la insatisfacción laboral.
d) Sistemas elementales de control de riesgos. Protección colectiva e individual.
e) Planes de emergencia y evacuación.
f) El control de la salud de los trabajadores.
Total horas: 12.

[3] Ley 32/2006, Artículo 10 (score 0.705)
Ley 32/2006, Artículo 10
Artículo 10. Acreditación de la formación preventiva de los trabajadores.
1. Las empresas velarán por que todos los trabajadores que presten servicios en las obras tengan la formación necesaria y adecuada a su puesto de trabajo o función en materia de prevención de riesgos laborales, de forma que conozcan los riesgos y las medidas para prevenirlos.
2. Sin perjuicio de la obligación legal del empresario de garantizar la formación a que se refiere el apartado anterior, en la negociación colectiva estatal del sector se podrán establecer programas formativos y contenidos específicos de carácter sectorial y para los trabajos de cada especialidad.
3. Dadas las características que concurren en el sector de la construcción, reglamentariamente o a través de la negociación colectiva sectorial de ámbito estatal, se regulará la forma de acreditar la formación específica recibida por el trabajador referida a la prevención de riesgos laborales en el sector de la construcción.
El sistema de acreditación que se establezca, que podrá consistir en la expedición de una cartilla o carné profesional para cada trabajador, será único y tendrá validez en el conjunto del sector, pudiendo atribuirse su diseño, ejecución y expedición a organismos paritarios creados en el ámbito de la negociación colectiva sectorial de ámbito estatal, en coordinación con la Fundación adscrita a la Comisión Nacional de Seguridad y Salud en el Trabajo.

[4] RD 39/1997, Artículo 35 (score 0.697)
RD 39/1997, Artículo 35
Artículo 35. Funciones de nivel básico.
1. Integran el nivel básico de la actividad preventiva las funciones siguientes:
a) Promover los comportamientos seguros y la correcta utilización de los equipos de trabajo y protección, y fomentar el interés y cooperación de los trabajadores en una acción preventiva integrada.
b) Promover, en particular, las actuaciones preventivas básicas, tales como el orden, la limpieza, la señalización y el mantenimiento general, y efectuar su seguimiento y control.
c) Realizar evaluaciones elementales de riesgos y, en su caso, establecer medidas preventivas del mismo carácter compatibles con su grado de formación.
d) Colaborar en la evaluación y el control de los riesgos generales y específicos de la empresa, efectuando visitas al efecto, atención a quejas y sugerencias, registro de datos, y cuantas funciones análogas sean necesarias.
e) Actuar en caso de emergencia y primeros auxilios gestionando las primeras intervenciones al efecto.
f) Cooperar con los servicios de prevención, en su caso.
2. Para desempeñar las funciones referidas en el apartado anterior, será preciso:
a) Poseer una formación mínima con el contenido especificado en el programa a que se refiere el anexo IV y cuyo desarrollo tendrá una duración no inferior a 50 horas, en el caso de empresas que desarrollen alguna de las actividades incluidas en el anexo I, o de 30 horas en los demás casos, y una distribución horaria adecuada a cada proyecto formativo, respetando la establecida en los apartados 1 y 2, respectivamente, del anexo IV citado, o
b) Poseer una formación profesional o académica que capacite para llevar a cabo responsabilidades profesionales equivalentes o similares a las que precisan las actividades señaladas en el apartado anterior, o
c) Acreditar una experiencia no inferior a dos años en una empresa, institución o Administración pública que lleve consigo el desempeño de niveles profesionales de responsabilidad equivalentes o similares a los que precisan las actividades señaladas en el apartado anterior.

[5] Ley 31/1995, Artículo 14 (score 0.694)
Ley 31/1995, Artículo 14
3. El empresario deberá cumplir las obligaciones establecidas en la normativa sobre prevención de riesgos laborales.
4. Las obligaciones de los trabajadores establecidas en esta Ley, la atribución de funciones en materia de protección y prevención a trabajadores o servicios de la empresa y el recurso al concierto con entidades especializadas para el desarrollo de actividades de prevención complementarán las acciones del empresario, sin que por ello le eximan del cumplimiento de su deber en esta materia, sin perjuicio de las acciones que pueda ejercitar, en su caso, contra cualquier otra persona.
5. El coste de las medidas relativas a la seguridad y la salud en el trabajo no deberá recaer en modo alguno sobre los trabajadores.

---
## f03 (single, fresh)
**Question:** Tenemos a una operaria embarazada en la obra, ¿qué tenemos que hacer?
**Reference:** Evaluar los riesgos para el embarazo y la lactancia; si hay riesgo, adaptar sus condiciones o su tiempo de trabajo y, si hace falta, cambiarla de puesto (Ley 31/1995, art. 26).
**Answer:**

Ante la presencia de una operaria embarazada en la obra, se deben seguir los siguientes pasos según la normativa:

1. **Evaluación de riesgos específica:** La evaluación de riesgos de la empresa debe comprender la determinación de la naturaleza, el grado y la duración de la exposición a agentes, procedimientos o condiciones de trabajo que puedan influir negativamente en la salud de la trabajadora o del feto (Ley 31/1995, Artículo 26). En todo caso, la trabajadora no podrá realizar actividades que supongan riesgo de exposición a los agentes o condiciones de trabajo de la lista del Anexo VIII del RD 39/1997 (RD 39/1997, Artículo 4).
2. **Adaptación de condiciones o tiempo de trabajo:** Si los resultados revelan un riesgo, el empresario adoptará las medidas necesarias para evitar la exposición mediante la adaptación de las condiciones o del tiempo de trabajo, lo que incluirá, cuando sea necesario, la supresión del trabajo nocturno o a turnos (Ley 31/1995, Artículo 26).
3. **Cambio de puesto:** Si la adaptación no es posible o el puesto sigue influyendo negativamente (certificado por los Servicios Médicos del INSS o de las Mutuas, con informe del médico del Servicio Nacional de Salud), la trabajadora deberá desempeñar un puesto de trabajo o función diferente y compatible, exento de riesgos, previa consulta a los representantes de los trabajadores. Si no existe un puesto de su grupo o categoría, podrá ser destinada a uno de otro grupo conservando el derecho al conjunto de sus retribuciones (Ley 31/1995, Artículo 26).
4. **Suspensión del contrato por riesgo:** Si dicho cambio de puesto no resulta técnica u objetivamente posible, o no puede razonablemente exigirse por motivos justificados, procederá la suspensión del contrato por riesgo durante el embarazo (Ley 31/1995, Artículo 26).
5. **Exámenes prenatales:** La trabajadora tendrá derecho a ausentarse del trabajo, con derecho a remuneración, para la realización de exámenes prenatales y técnicas de preparación al parto, previo aviso y justificación (Ley 31/1995, Artículo 26).

Fuentes utilizadas:
- Ley 31/1995, Artículo 26.
- RD 39/1997, Artículo 4, Anexo VII y Anexo VIII.

*Nota: Esta información es divulgativa y no constituye asesoramiento legal.*

**Citations:** Ley 31/1995, Artículo 26; RD 39/1997, Artículo 4 — all in retrieved text

**Coverage check:**

- Search 1 «trabajadora embarazada maternidad lactancia obra seguridad salud»: **SÍ**, passage [1], quote: «Si los resultados de la evaluación revelasen un riesgo para la seguridad y la salud o una posible repercusión sobre el embarazo o la lactancia de las citadas trabajadoras, el empresario adoptará las medidas necesarias para evitar la exposición a dicho riesgo, a través de una adaptación de las condiciones o del tiempo de trabajo de la trabajadora afectada.». Need: qué medidas o actuaciones se deben llevar a cabo con una operaria embarazada en la obra

**Retrieved passages:**

[1] Ley 31/1995, Artículo 26 (score 0.762)
Ley 31/1995, Artículo 26
Artículo 26. Protección de la maternidad.
1. La evaluación de los riesgos a que se refiere el artículo 16 de la presente Ley deberá comprender la determinación de la naturaleza, el grado y la duración de la exposición de las trabajadoras en situación de embarazo o parto reciente a agentes, procedimientos o condiciones de trabajo que puedan influir negativamente en la salud de las trabajadoras o del feto, en cualquier actividad susceptible de presentar un riesgo específico. Si los resultados de la evaluación revelasen un riesgo para la seguridad y la salud o una posible repercusión sobre el embarazo o la lactancia de las citadas trabajadoras, el empresario adoptará las medidas necesarias para evitar la exposición a dicho riesgo, a través de una adaptación de las condiciones o del tiempo de trabajo de la trabajadora afectada. Dichas medidas incluirán, cuando resulte necesario, la no realización de trabajo nocturno o de trabajo a turnos.
2. Cuando la adaptación de las condiciones o del tiempo de trabajo no resultase posible o, a pesar de tal adaptación, las condiciones de un puesto de trabajo pudieran influir negativamente en la salud de la trabajadora embarazada o del feto, y así lo certifiquen los Servicios Médicos del Instituto Nacional de la Seguridad Social o de las Mutuas, en función de la Entidad con la que la empresa tenga concertada la cobertura de los riesgos profesionales, con el informe del médico del Servicio Nacional de Salud que asista facultativamente a la trabajadora, ésta deberá desempeñar un puesto de trabajo o función diferente y compatible con su estado. El empresario deberá determinar, previa consulta con los representantes de los trabajadores, la relación de los puestos de trabajo exentos de riesgos a estos efectos.
El cambio de puesto o función se llevará a cabo de conformidad con las reglas y criterios que se apliquen en los supuestos de movilidad funcional y tendrá efectos hasta el momento en que el estado de salud de la trabajadora permita su reincorporación al anterior puesto.

[2] Ley 31/1995, Artículo 26 (score 0.756)
Ley 31/1995, Artículo 26
En el supuesto de que, aun aplicando las reglas señaladas en el párrafo anterior, no existiese puesto de trabajo o función compatible, la trabajadora podrá ser destinada a un puesto no correspondiente a su grupo o categoría equivalente, si bien conservará el derecho al conjunto de retribuciones de su puesto de origen.
3. Si dicho cambio de puesto no resultara técnica u objetivamente posible, o no pueda razonablemente exigirse por motivos justificados, podrá declararse el paso de la trabajadora afectada a la situación de suspensión del contrato por riesgo durante el embarazo, contemplada en el artículo 45.1.d) del Estatuto de los Trabajadores, durante el período necesario para la protección de su seguridad o de su salud y mientras persista la imposibilidad de reincorporarse a su puesto anterior o a otro puesto compatible con su estado.
4. Lo dispuesto en los números 1 y 2 de este artículo será también de aplicación durante el período de lactancia natural, si las condiciones de trabajo pudieran influir negativamente en la salud de la mujer o del hijo y así lo certifiquen los Servicios Médicos del Instituto Nacional de la Seguridad Social o de las Mutuas, en función de la Entidad con la que la empresa tenga concertada la cobertura de los riesgos profesionales, con el informe del médico del Servicio Nacional de Salud que asista facultativamente a la trabajadora o a su hijo. Podrá, asimismo, declararse el pase de la trabajadora afectada a la situación de suspensión del contrato por riesgo durante la lactancia natural de hijos menores de nueve meses contemplada en el artículo 45.1.d) del Estatuto de los Trabajadores, si se dan las circunstancias previstas en el número 3 de este artículo.
5. Las trabajadoras embarazadas tendrán derecho a ausentarse del trabajo, con derecho a remuneración, para la realización de exámenes prenatales y técnicas de preparación al parto, previo aviso al empresario y justificación de la necesidad de su realización dentro de la jornada de trabajo.

[3] RD 39/1997, Anexo VII (score 0.733)
RD 39/1997, Anexo VII
ANEXO VII
Lista no exhaustiva de agentes, procedimientos y condiciones de trabajo que pueden influir negativamente en la salud de las trabajadoras embarazadas o en período de lactancia natural, del feto o del niño durante el período de lactancia natural
A. Agentes.
1. Agentes físicos, cuando se considere que puedan implicar lesiones fetales o provocar un desprendimiento de la placenta, en particular:
a) Choques, vibraciones o movimientos.
b) Manipulación manual de cargas pesadas que supongan riesgos, en particular dorsolumbares.
c) Ruido.
d) Radiaciones no ionizantes.
e) Frío y calor extremos.
f) Movimientos y posturas, desplazamientos, tanto en el interior como en el exterior del centro de trabajo, fatiga mental y física y otras cargas físicas vinculadas a la actividad de la trabajadora embarazada, que haya dado a luz o en período de lactancia.
2. Agentes biológicos.–Agentes biológicos de los grupos de riesgo 2, 3 y 4, según la clasificación de los agentes biológicos establecida en el Real Decreto 664/1997, de 12 de mayo, sobre la protección de los trabajadores contra los riesgos relacionados con la exposición a agentes biológicos durante el trabajo, en la medida en que se sepa que dichos agentes o las medidas terapéuticas que necesariamente traen consigo ponen en peligro la salud de las trabajadoras embarazadas o del feto y siempre que no figuren en el anexo VIII.
3. Agentes químicos.–Los siguientes agentes químicos, en la medida en que se sepa que ponen en peligro la salud de las trabajadoras embarazadas o en período de lactancia, del feto o del niño durante el período de lactancia natural y siempre que no figuren en el anexo VIII:
a) Las sustancias etiquetadas como H340, H341, H350, H351, H361, H371, H361d, H361f, H350i y H361fd por el Reglamento (CE) n.º 1272/2008 del Parlamento Europeo y del Consejo, de 16 de diciembre de 2008, sobre clasificación, etiquetado y envasado de sustancias y mezclas.

[4] RD 39/1997, Anexo VIII (score 0.733)
RD 39/1997, Anexo VIII
ANEXO VIII
Lista no exhaustiva de agentes y condiciones de trabajo a los cuales no podrá haber riesgo de exposición por parte de trabajadoras embarazadas o en período de lactancia natural
A. Trabajadoras embarazadas.
1. Agentes.
a) Agentes físicos:
Radiaciones ionizantes.
Trabajos en atmósferas de sobrepresión elevada, por ejemplo, en locales a presión, submarinismo.
b) Agentes biológicos:
Toxoplasma.
Virus de la rubeola.
Salvo si existen pruebas de que la trabajadora embarazada está suficientemente protegida contra estos agentes por su estado de inmunización.
c) Agentes químicos:
Las sustancias etiquetadas como H360, H360D, H360F, H360FD, H360Fd, H360Df y H370 por el Reglamento (CE) n.º 1272/2008 del Parlamento Europeo y del Consejo, de 16 de diciembre de 2008, sobre clasificación, etiquetado y envasado de sustancias y mezclas.
Las sustancias cancerígenas y mutágenas, de categoría 1A y 1B incluidas en la parte 3 del Anexo VI del Reglamento (CE) n.º 1272/2008, de 16 de diciembre de 2008, sobre clasificación, etiquetado y envasado de sustancias y mezclas.
Plomo y derivados, en la medida en que estos agentes sean susceptibles de ser absorbidos por el organismo humano.
2. Condiciones de trabajo.–Trabajos de minería subterráneos.
B. Trabajadoras en período de lactancia.
1. Agentes químicos:
Las sustancias etiquetadas como H362 por el Reglamento (CE) n.º 1272/2008 del Parlamento Europeo y del Consejo, de 16 de diciembre de 2008, sobre clasificación, etiquetado y envasado de sustancias y mezclas.
Las sustancias cancerígenas y mutágenas, de categoría 1A y 1B incluidas en la parte 3 del Anexo VI del Reglamento (CE) n.º 1272/2008, de 16 de diciembre de 2008, sobre clasificación, etiquetado y envasado de sustancias y mezclas.
Plomo y derivados, en la medida en que estos agentes sean susceptibles de ser absorbidos por el organismo humano.
2. Condiciones de trabajo.–Trabajos de minería subterráneos.

[5] RD 39/1997, Artículo 4 (score 0.727)
RD 39/1997, Artículo 4
En todo caso la trabajadora embarazada no podrá realizar actividades que supongan riesgo de exposición a los agentes o condiciones de trabajo incluidos en la lista no exhaustiva de la parte A del anexo VIII, cuando, de acuerdo con las conclusiones obtenidas de la evaluación de riesgos, ello pueda poner en peligro su seguridad o su salud o la del feto. Igualmente la trabajadora en período de lactancia no podrá realizar actividades que supongan el riesgo de una exposición a los agentes o condiciones de trabajo enumerados en la lista no exhaustiva del anexo VIII, parte B, cuando de la evaluación se desprenda que ello pueda poner en peligro su seguridad o su salud o la del niño durante el período de lactancia natural. En los casos previstos en este párrafo, se adoptarán

---
## f04 (single, fresh)
**Question:** Somos 40 en plantilla, ¿cuántos delegados de prevención nos tocan?
**Reference:** Uno, elegido por y entre los delegados de personal (empresas de 31 a 49 trabajadores, Ley 31/1995, art. 35.2).
**Answer:**

Con una plantilla de 40 trabajadores, corresponde **un Delegado de Prevención**, que será elegido por y entre los Delegados de Personal.

Fuentes utilizadas:
- Ley 31/1995, Artículo 35, apartado 2.

*Nota: Esta información es divulgativa y no constituye asesoramiento legal.*

**Citations:** Ley 31/1995, Artículo 35 — all in retrieved text

**Coverage check:**

- Search 1 «numero delegados de prevencion plantilla trabajadores ley 31 1995»: **SÍ**, passage [1], quote: «En las empresas de treinta y uno a cuarenta y nueve trabajadores habrá un Delegado de Prevención que será elegido por y entre los Delegados de Personal.». Need: el número de delegados de prevención que corresponden a una plantilla de 40 trabajadores

**Retrieved passages:**

[1] Ley 31/1995, Artículo 35 (score 0.814)
Ley 31/1995, Artículo 35
Artículo 35. Delegados de Prevención.
1. Los Delegados de Prevención son los representantes de los trabajadores con funciones específicas en materia de prevención de riesgos en el trabajo.
2. Los Delegados de Prevención serán designados por y entre los representantes del personal, en el ámbito de los órganos de representación previstos en las normas a que se refiere el artículo anterior, con arreglo a la siguiente escala:
De 50 a 100 trabajadores: 2 Delegados de Prevención.
De 101 a 500 trabajadores: 3 Delegados de Prevención.
De 501 a 1.000 trabajadores: 4 Delegados de Prevención.
De 1.001 a 2.000 trabajadores: 5 Delegados de Prevención.
De 2.001 a 3.000 trabajadores: 6 Delegados de Prevención.
De 3.001 a 4.000 trabajadores: 7 Delegados de Prevención.
De 4.001 en adelante: 8 Delegados de Prevención.
En las empresas de hasta treinta trabajadores el Delegado de Prevención será el Delegado de Personal. En las empresas de treinta y uno a cuarenta y nueve trabajadores habrá un Delegado de Prevención que será elegido por y entre los Delegados de Personal.
3. A efectos de determinar el número de Delegados de Prevención se tendrán en cuenta los siguientes criterios:
a) Los trabajadores vinculados por contratos de duración determinada superior a un año se computarán como trabajadores fijos de plantilla.
b) Los contratados por término de hasta un año se computarán según el número de días trabajados en el período de un año anterior a la designación. Cada doscientos días trabajados o fracción se computarán como un trabajador más.
4. No obstante lo dispuesto en el presente artículo, en los convenios colectivos podrán establecerse otros sistemas de designación de los Delegados de Prevención, siempre que se garantice que la facultad de designación corresponde a los representantes del personal o a los propios trabajadores.

[2] Ley 31/1995, Disposición adicional décima (score 0.781)
Ley 31/1995, Disposición adicional décima
Disposición adicional décima. Sociedades cooperativas.
El procedimiento para la designación de los Delegados de Prevención regulados en el artículo 35 de esta Ley en las sociedades cooperativas que no cuenten con asalariados deberá estar previsto en sus Estatutos o ser objeto de acuerdo en Asamblea General.
Cuando, además de los socios que prestan su trabajo personal, existan asalariados se computarán ambos colectivos a efectos de lo dispuesto en el número 2 del artículo 35. En este caso, la designación de los Delegados de Prevención se realizará conjuntamente por los socios que prestan trabajo y los trabajadores asalariados o, en su caso, los representantes de éstos.

[3] Ley 31/1995, Artículo 34 (score 0.774)
Ley 31/1995, Artículo 34
Artículo 34. Derechos de participación y representación.
1. Los trabajadores tienen derecho a participar en la empresa en las cuestiones relacionadas con la prevención de riesgos en el trabajo.
En las empresas o centros de trabajo que cuenten con seis o más trabajadores, la participación de éstos se canalizará a través de sus representantes y de la representación especializada que se regula en este capítulo.
2. A los Comités de Empresa, a los Delegados de Personal y a los representantes sindicales les corresponde, en los términos que, respectivamente, les reconocen el Estatuto de los Trabajadores, la Ley de Organos de Representación del Personal al Servicio de las Administraciones Públicas y la Ley Orgánica de Libertad Sindical, la defensa de los intereses de los trabajadores en materia de prevención de riesgos en el trabajo. Para ello, los representantes del personal ejercerán las competencias que dichas normas establecen en materia de información, consulta y negociación, vigilancia y control y ejercicio de acciones ante las empresas y los órganos y tribunales competentes.
3. El derecho de participación que se regula en este capítulo se ejercerá en el ámbito de las Administraciones públicas con las adaptaciones que procedan en atención a la diversidad de las actividades que desarrollan y las diferentes condiciones en que éstas se realizan, la complejidad y dispersión de su estructura organizativa y sus peculiaridades en materia de representación colectiva, en los términos previstos en la Ley 7/1990, de 19 de julio, sobre negociación colectiva y participación en la determinación de las condiciones de trabajo de los empleados públicos, pudiéndose establecer ámbitos sectoriales y descentralizados en función del número de efectivos y centros.
Para llevar a cabo la indicada adaptación en el ámbito de la Administración General del Estado, el Gobierno tendrá en cuenta los siguientes criterios:
a) En ningún caso dicha adaptación podrá afectar a las competencias, facultades y garantías que se reconocen en esta Ley a los Delegados de Prevención y a los Comités de Seguridad y Salud.

[4] Ley 31/1995, Artículo 36 (score 0.765)
Ley 31/1995, Artículo 36
Artículo 36. Competencias y facultades de los Delegados de Prevención.
1. Son competencias de los Delegados de Prevención:
a) Colaborar con la dirección de la empresa en la mejora de la acción preventiva.
b) Promover y fomentar la cooperación de los trabajadores en la ejecución de la normativa sobre prevención de riesgos laborales.
c) Ser consultados por el empresario, con carácter previo a su ejecución, acerca de las decisiones a que se refiere el artículo 33 de la presente Ley.
d) Ejercer una labor de vigilancia y control sobre el cumplimiento de la normativa de prevención de riesgos laborales.
En las empresas que, de acuerdo con lo dispuesto en el apartado 2 del artículo 38 de esta Ley, no cuenten con Comité de Seguridad y Salud por no alcanzar el número mínimo de trabajadores establecido al efecto, las competencias atribuidas a aquél en la presente Ley serán ejercidas por los Delegados de Prevención.
2. En el ejercicio de las competencias atribuidas a los Delegados de Prevención, éstos estarán facultados para:
a) Acompañar a los técnicos en las evaluaciones de carácter preventivo del medio ambiente de trabajo, así como, en los términos previstos en el artículo 40 de esta Ley, a los Inspectores de Trabajo y Seguridad Social en las visitas y verificaciones que realicen en los centros de trabajo para comprobar el cumplimiento de la normativa sobre prevención de riesgos laborales, pudiendo formular ante ellos las observaciones que estimen oportunas.
b) Tener acceso, con las limitaciones previstas en el apartado 4 del artículo 22 de esta Ley, a la información y documentación relativa a las condiciones de trabajo que sean necesarias para el ejercicio de sus funciones y, en particular, a la prevista en los artículos 18 y 23 de esta Ley. Cuando la información esté sujeta a las limitaciones reseñadas, sólo podrá ser suministrada de manera que se garantice el respeto de la confidencialidad.

[5] Ley 31/1995, Disposición adicional cuarta (score 0.763)
Ley 31/1995, Disposición adicional cuarta
Disposición adicional cuarta. Designación de Delegados de Prevención en supuestos especiales.
En los centros de trabajo que carezcan de representantes de los trabajadores por no existir trabajadores con la antigüedad suficiente para ser electores o elegibles en las elecciones para representantes del personal, los trabajadores podrán elegir por mayoría a un trabajador que ejerza las competencias del Delegado de Prevención, quién tendrá las facultades, garantías y obligaciones de sigilo profesional de tales Delegados. La actuación de éstos cesará en el momento en que se reúnan los requisitos de antigüedad necesarios para poder celebrar la elección de representantes del personal, prorrogándose por el tiempo indispensable para la efectiva celebración de la elección.

---
## f05 (unanswerable, fresh)
**Question:** ¿Qué equipo de protección tiene que llevar un soldador?
**Reference:** Debe rechazar: el corpus no habla de soldadura ni de EPI específicos por oficio.
**Answer:** *(forced refusal)*

No consta en los documentos del corpus.

Se buscó en el corpus: «equipos de protección individual soldadura construcción».

**Citations:** (none)

**Coverage check:**

- Search 1 «equipos de protección individual soldadura construcción»: **NO**. Need: el equipo de protección específico que tiene que llevar un soldador

**Retrieved passages:**

[1] Ley 31/1995, Artículo 17 (score 0.703)
Ley 31/1995, Artículo 17
Artículo 17. Equipos de trabajo y medios de protección.
1. El empresario adoptará las medidas necesarias con el fin de que los equipos de trabajo sean adecuados para el trabajo que deba realizarse y convenientemente adaptados a tal efecto, de forma que garanticen la seguridad y la salud de los trabajadores al utilizarlos.
Cuando la utilización de un equipo de trabajo pueda presentar un riesgo específico para la seguridad y la salud de los trabajadores, el empresario adoptará las medidas necesarias con el fin de que:
a) La utilización del equipo de trabajo quede reservada a los encargados de dicha utilización.
b) Los trabajos de reparación, transformación, mantenimiento o conservación sean realizados por los trabajadores específicamente capacitados para ello.
2. El empresario deberá proporcionar a sus trabajadores equipos de protección individual adecuados para el desempeño de sus funciones y velar por el uso efectivo de los mismos cuando, por la naturaleza de los trabajos realizados, sean necesarios.
Los equipos de protección individual deberán utilizarse cuando los riesgos no se puedan evitar o no puedan limitarse suficientemente por medios técnicos de protección colectiva o mediante medidas, métodos o procedimientos de organización del trabajo.

[2] Ley 31/1995, Artículo 4 (score 0.678)
Ley 31/1995, Artículo 4
c) Los procedimientos para la utilización de los agentes citados anteriormente que influyan en la generación de los riesgos mencionados.
d) Todas aquellas otras características del trabajo, incluidas las relativas a su organización y ordenación, que influyan en la magnitud de los riesgos a que esté expuesto el trabajador.
8.º Se entenderá por «equipo de protección individual» cualquier equipo destinado a ser llevado o sujetado por el trabajador para que le proteja de uno o varios riesgos que puedan amenazar su seguridad o su salud en el trabajo, así como cualquier complemento o accesorio destinado a tal fin.

[3] RD 1627/1997, Anexo I (score 0.671)
RD 1627/1997, Anexo I
ANEXO I
Relación no exhaustiva de las obras de construcción o de ingeniería civil
a) Excavación.
b) Movimiento de tierras.
c) Construcción.
d) Montaje y desmontaje de elementos prefabricados.
e) Acondicionamiento o instalaciones.
f) Transformación.
g) Rehabilitación.
h) Reparación.
i) Desmantelamiento.
j) Derribo.
k) Mantenimiento.
l) Conservación-Trabajos de pintura y de limpieza.
m) Saneamiento.

[4] RD 1627/1997, Anexo II (score 0.666)
RD 1627/1997, Anexo II
ANEXO II
Relación no exhaustiva de los trabajos que implican riesgos especiales para la seguridad y la salud de los trabajadores
1. Trabajos con riesgos especialmente graves de sepultamiento, hundimiento o caída de altura, por las particulares características de la actividad desarrollada, los procedimientos aplicados, o el entorno del puesto de trabajo.
2. Trabajos en los que la exposición a agentes químicos o biológicos suponga un riesgo de especial gravedad, o para los que la vigilancia específica de la salud de los trabajadores sea legalmente exigible.
3. Trabajos con exposición a radiaciones ionizantes para los que la normativa específica obliga a la delimitación de zonas controladas o vigiladas.
4. Trabajos en la proximidad de líneas eléctricas de alta tensión.
5. Trabajos que expongan a riesgo de ahogamiento por inmersión.
6. Obras de excavación de túneles, pozos y otros trabajos que supongan movimientos de tierra subterráneos.
7. Trabajos realizados en inmersión con equipo subacuático.
8. Trabajos realizados en cajones de aire comprimido.
9. Trabajos que impliquen el uso de explosivos.
10. Trabajos que requieran montar o desmontar elementos prefabricados pesados.

[5] Ley 32/2006, Artículo 2 (score 0.664)
Ley 32/2006, Artículo 2
Artículo 2. Ámbito de aplicación.
La presente Ley será de aplicación a los contratos que se celebren, en régimen de subcontratación, para la ejecución de los siguientes trabajos realizados en obras de construcción:
Excavación; movimiento de tierras; construcción; montaje y desmontaje de elementos prefabricados; acondicionamientos o instalaciones; transformación; rehabilitación; reparación; desmantelamiento; derribo; mantenimiento; conservación y trabajos de pintura y limpieza; saneamiento.

---
## f06 (unanswerable, fresh)
**Question:** ¿En cuántos días tengo que pagar a un subcontratista?
**Reference:** Debe rechazar: los plazos de pago no están en estas normas.
**Answer:** *(forced refusal)*

No consta en los documentos del corpus.

Se buscó en el corpus: «plazo pago subcontratista Ley 32/2006».

**Citations:** (none)

**Coverage check:**

- Search 1 «plazo pago subcontratista Ley 32/2006»: **NO**. Need: el plazo en días para pagar a un subcontratista

**Retrieved passages:**

[1] Ley 32/2006, Artículo 2 (score 0.762)
Ley 32/2006, Artículo 2
Artículo 2. Ámbito de aplicación.
La presente Ley será de aplicación a los contratos que se celebren, en régimen de subcontratación, para la ejecución de los siguientes trabajos realizados en obras de construcción:
Excavación; movimiento de tierras; construcción; montaje y desmontaje de elementos prefabricados; acondicionamientos o instalaciones; transformación; rehabilitación; reparación; desmantelamiento; derribo; mantenimiento; conservación y trabajos de pintura y limpieza; saneamiento.

[2] Ley 32/2006, Artículo 5 (score 0.76)
Ley 32/2006, Artículo 5
Artículo 5. Régimen de la subcontratación.
1. La subcontratación, como forma de organización productiva, no podrá ser limitada, salvo en las condiciones y en los supuestos previstos en esta Ley.
2. Con carácter general, el régimen de la subcontratación en el sector de la construcción será el siguiente:
a) El promotor podrá contratar directamente con cuantos contratistas estime oportuno ya sean personas físicas o jurídicas.
b) El contratista podrá contratar con las empresas subcontratistas o trabajadores autónomos la ejecución de los trabajos que hubiera contratado con el promotor.
c) El primer y segundo subcontratistas podrán subcontratar la ejecución de los trabajos que, respectivamente, tengan contratados, salvo en los supuestos previstos en la letra f) del presente apartado.
d) El tercer subcontratista no podrá subcontratar los trabajos que hubiera contratado con otro subcontratista o trabajador autónomo.
e) El trabajador autónomo no podrá subcontratar los trabajos a él encomendados ni a otras empresas subcontratistas ni a otros trabajadores autónomos.
f) Asimismo, tampoco podrán subcontratar los subcontratistas, cuya organización productiva puesta en uso en la obra consista fundamentalmente en la aportación de mano de obra, entendiéndose por tal la que para la realización de la actividad contratada no utiliza más equipos de trabajo propios que las herramientas manuales, incluidas las motorizadas portátiles, aunque cuenten con el apoyo de otros equipos de trabajo distintos de los señalados, siempre que éstos pertenezcan a otras empresas, contratistas o subcontratistas, de la obra.
3. No obstante lo dispuesto en el apartado anterior, cuando en casos fortuitos debidamente justificados, por exigencias de especialización de los trabajos, complicaciones técnicas de la producción o circunstancias de fuerza mayor por las que puedan atravesar los agentes que intervienen en la obra, fuera necesario, a juicio de la dirección facultativa, la contratación de alguna parte de la obra con terceros, excepcionalmente se podrá extender la subcontratación establecida en el apartado anterior en un nivel adicional, siempre que se haga constar por la dirección facultativa su aprobación previa y la causa o causas motivadoras de la misma en el Libro de Subcontratación al que se refiere el artículo 7 de esta Ley.

[3] Ley 32/2006, Artículo 7 (score 0.756)
Ley 32/2006, Artículo 7
Artículo 7. Deber de vigilancia y responsabilidades derivadas de su incumplimiento.
1. Las empresas contratistas y subcontratistas que intervengan en las obras de construcción incluidas en el ámbito de aplicación de esta Ley deberán vigilar el cumplimiento de lo dispuesto en la misma por las empresas subcontratistas y trabajadores autónomos con que contraten; en particular, en lo que se refiere a las obligaciones de acreditación y registro reguladas en el artículo 4.2 y al régimen de la subcontratación que se regula en el artículo 5.
A efectos de lo dispuesto en el párrafo anterior, las empresas subcontratistas deberán comunicar o trasladar al contratista, a través de sus respectivas empresas comitentes en caso de ser distintas de aquél, toda información o documentación que afecte al contenido de este capítulo.
2. Sin perjuicio de otras responsabilidades establecidas en la legislación social, el incumplimiento de las obligaciones de acreditación y registro exigidas en el artículo 4.2, o del régimen de subcontratación establecido en el artículo 5, determinará la responsabilidad solidaria del subcontratista que hubiera contratado incurriendo en dichos incumplimientos y del correspondiente contratista respecto de las obligaciones laborales y de Seguridad Social derivadas de la ejecución del contrato acordado que correspondan al subcontratista responsable del incumplimiento en el ámbito de ejecución de su contrato, cualquiera que fuera la actividad de dichas empresas.
3. En todo caso será exigible la responsabilidad establecida en el artículo 43 del Estatuto de los Trabajadores cuando se den los supuestos previstos en el mismo.

[4] Ley 32/2006, Artículo 1 (score 0.755)
Ley 32/2006, Artículo 1
Artículo 1. Objeto de la Ley.
1. La presente Ley regula la subcontratación en el sector de la construcción y tiene por objeto mejorar las condiciones de trabajo del sector, en general, y las condiciones de seguridad y salud de los trabajadores del mismo, en particular.
2. Lo previsto en esta Ley se entiende sin perjuicio de la aplicación a las subcontrataciones que se realicen en el sector de la construcción de lo dispuesto en el artículo 42 del Texto Refundido de la Ley del Estatuto de los Trabajadores, aprobado por Real Decreto Legislativo 1/1995, de 24 de marzo, y en el resto de la legislación social.

[5] Ley 32/2006, Preámbulo (score 0.751)
Ley 32/2006, Preámbulo
A todos los que la presente vieren y entendieren.
Sabed: Que las Cortes Generales han aprobado y Yo vengo en sancionar la siguiente ley.
Tras diez años de promulgación de la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales, y después su desarrollo reglamentario, es un hecho incontestable que, pese a todo, y a los ingentes esfuerzos realizados por los distintos actores implicados en la prevención de riesgos laborales (Estado, Comunidades Autónomas, Agentes Sociales, Entidades especializadas, etcétera), existe un sector como el de la construcción que, constituyendo uno de los ejes del crecimiento económico de nuestro país, está sometido a unos riesgos especiales y continúa registrando una siniestralidad laboral muy notoria por sus cifras y gravedad.
Son numerosos los estudios y análisis desarrollados para evaluar las causas de tales índices de siniestralidad en este sector, sin que resulte posible atribuir el origen de esta situación a una causa única, dada su complejidad.
Uno de esos factores puede estar relacionado con la utilización de una forma de organización productiva, que tiene una importante tradición en el sector, pero que ha adquirido en las últimas décadas un especial desarrollo en el mismo, también como reflejo de la externalización productiva que se da en otros sectores, aunque en éste con especial intensidad. Esta forma de organización no es otra que la denominada «subcontratación».