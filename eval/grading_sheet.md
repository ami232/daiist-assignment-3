# Grading sheet (for eval/human_labels.csv)

Grade at least 20 answers **before** opening eval/judge.jsonl or eval/results.csv.
For each: `correct` 1/0 (right against the reference, or a proper refusal) and `supported` 1/0 (every claim is in the retrieved passages; open the article on the BOE link if needed). Write a note for every 0.

## q01 (single)
**Question:** ¿Cuántos días de vacaciones tiene como mínimo un trabajador y se pueden cambiar por dinero?
**Reference:** Como mínimo 30 días naturales al año; las vacaciones no son sustituibles por compensación económica.
**Agent answer:**

> El periodo mínimo de vacaciones anuales retribuidas es de **treinta días naturales**, salvo que en el convenio colectivo o en el contrato individual se pacte una duración superior [Estatuto de los Trabajadores (RDL 2/2015), Artículo 38].
> 
> **No se pueden cambiar por dinero** (compensación económica), ya que el Estatuto de los Trabajadores establece expresamente que el periodo de vacaciones anuales retribuidas no es sustituible por compensación económica, salvo en los supuestos de extinción del contrato de trabajo en los que el trabajador tenga días pendientes de disfrutar.
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 15, apdos. 1-2; Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 4-8; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 38

## q02 (single)
**Question:** ¿Cuál es la duración máxima del periodo de prueba de un técnico titulado?
**Reference:** Seis meses para técnicos titulados (dos meses para el resto; tres meses para no titulados en empresas de menos de 25 trabajadores), salvo lo que establezca el convenio.
**Agent answer:**

> La duración máxima del periodo de prueba para técnicos y técnicas tituladas es de **seis meses**, salvo que el convenio colectivo disponga otra cosa [Estatuto de los Trabajadores (RDL 2/2015), Artículo 14, apdos. 1-2]. 
> 
> Excepciones a tener en cuenta según el tipo de contrato:
> * Si se trata de un contrato de duración determinada de duración igual o superior a seis meses, el periodo de prueba no podrá exceder de un mes (reduciéndose proporcionalmente si la duración es inferior) [Estatuto de los Trabajadores (RDL 2/2015), Artículo 14, apdos. 1-2].
> * Si se trata de un contrato formativo para la obtención de práctica profesional, el periodo de prueba no podrá exceder de un mes, salvo lo dispuesto en convenio colectivo [Estatuto de los Trabajadores (RDL 2/2015), Artículo 11, apdo. 3].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 11, apdo. 3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 11, apdos. 2-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 14, apdo. 3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 14, apdos. 1-2; Estatuto de los Trabajadores (RDL 2/2015), Artículo 15, apdos. 2-4

## q03 (single)
**Question:** Vamos a firmar un contrato temporal de ocho meses: ¿cuánto puede durar como máximo el periodo de prueba?
**Reference:** En contratos de duración determinada de seis meses o más, el periodo de prueba no puede exceder de un mes.
**Agent answer:**

> En los contratos de duración determinada que se concierten por un periodo igual o superior a
>  seis meses, el periodo de prueba no podrá exceder de **un mes**, salvo que el convenio colectivo establezca otra cosa.
> 
> [Estatuto de los Trabajadores (RDL 2/2015), Artículo 14, apdos. 1-2]
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 11, apdo. 3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 14, apdo. 3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 14, apdos. 1-2; Estatuto de los Trabajadores (RDL 2/2015), Artículo 15, apdos. 1-2; Estatuto de los Trabajadores (RDL 2/2015), Artículo 15, apdos. 2-4

## q04 (single)
**Question:** ¿Qué indemnización corresponde si un despido se declara improcedente?
**Reference:** 33 días de salario por año de servicio, prorrateando por meses, con un máximo de 24 mensualidades; la empresa tiene 5 días desde la sentencia para optar entre readmisión o indemnización.
**Agent answer:**

> Si el despido se declara improcedente, el empresario dispone de un plazo de **cinco días** desde la notificación de la sentencia para optar entre la readmisión del trabajador o el abono de una indemnización [Estatuto de los Trabajadores (RDL 2/2015), Artículo 56]:
> 
> * **Contratos suscritos a partir del 12 de febrero de 2012:** La indemnización es de **33 días de salario por año de servicio**, prorrateándose por meses los periodos inferiores a un año, con un **máximo de 24
>  mensualidades** [Estatuto de los Trabajadores (RDL 2/2015), Artículo 56].
> * **Contratos formalizados con anterioridad al 12 de febrero de 2012:** Se calcula por tramos (régimen transitorio) [Estatuto de los Trabajadores (RDL 2/2015), Disposición transitoria undécima]:
>   * A razón de **45 días de salario por año de servicio** por el tiempo de prestación de servicios anterior al 12 de febrero de 2012.
>   * A razón de **33 días de salario por año de servicio** por el tiempo posterior.
>   * El importe indemnizatorio resultante no puede superar los **720 días de salario**, salvo que del cálculo del periodo anterior al 12 de febrero de 2012 resulte un número de días superior (en cuyo caso se aplicará este como límite máximo, sin que pueda superar en ningún caso las **42 mensualidades**).
> 
> En caso de que el empresario opte por la readmisión, el trabajador tendrá derecho a los salarios de tramitación [Estatuto de los Trabajadores (RDL 2/2015), Artículo 56]. Si el empresario no opta expresamente ni por la readmisión ni por la indemnización, se entiende por defecto que procede la readmisión [Estatuto de los Trabajadores (RDL 2/2015), Artículo 56].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 33, apdo. 2; Estatuto de los Trabajadores (RDL 2/2015), Artículo 53, apdo. 5; Estatuto de los Trabajadores (RDL 2/2015), Artículo 56; Estatuto de los Trabajadores (RDL 2/2015), Disposición transitoria octava; Estatuto de los Trabajadores (RDL 2/2015), Disposición transitoria undécima

## q05 (single)
**Question:** ¿Qué requisitos formales tiene un despido por causas objetivas?
**Reference:** Comunicación escrita con la causa, poner a disposición simultáneamente una indemnización de 20 días por año con máximo de 12 mensualidades, y preaviso de 15 días.
**Agent answer:**

> La adopción del acuerdo de extinción por causas objetivas exige la observancia de los siguientes requisitos:
> 
> 1. Comunicación escrita al trabajador expresando la causa [Estatuto de los Trabajadores (RDL 2/2015), Artículo 53, apdos. 1-4].
> 2. Poner a disposición del trabajador, simultáneamente a la entrega de la comunicación escrita, la indemnización de veinte días por año de servicio, prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades (con la salvedad de que si se funda en causa económica y la situación lo impide, se podrá hacer constar en la comunicación escrita para abonarla cuando tenga efectividad la decisión) [Estatuto de los Trabajadores (RDL 2/2015), Artículo 53, apdos. 1-4].
> 3. Concesión de un plazo de preaviso de quince días, computado desde la entrega de la comunicación personal al trabajador hasta la extinción del contrato de trabajo (dando copia del preaviso a la representación legal de los trabajadores en el supuesto de causa económica) [Estatuto de los Trabajadores (RDL 2/2015), Artículo 53, apdos. 1-4].
> 4. Durante el periodo de preaviso, el trabajador o su representante legal tendrá derecho, sin pérdida de su retribución, a una licencia de seis horas semanales con el fin de buscar nuevo empleo [Estatuto de los Trabajadores (RDL 2/2015), Artículo 53, apdos. 1-4].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 51, apdo. 1; Estatuto de los Trabajadores (RDL 2/2015), Artículo 51, apdo. 2; Estatuto de los Trabajadores (RDL 2/2015), Artículo 53, apdo. 4; Estatuto de los Trabajadores (RDL 2/2015), Artículo 53, apdo. 5; Estatuto de los Trabajadores (RDL 2/2015), Artículo 53, apdos. 1-4; Estatuto de los Trabajadores (RDL 2/2015), Artículo 55, apdos. 1-5

## q06 (single)
**Question:** ¿Cuál es la jornada ordinaria máxima semanal?
**Reference:** 40 horas semanales de trabajo efectivo de promedio en cómputo anual.
**Agent answer:**

> La duración máxima de la jornada ordinaria de trabajo es de **cuarenta horas semanales de trabajo efectivo de promedio en cómputo anual**, sin perjuicio de que los convenios colectivos o contratos de trabajo puedan pactar una duración inferior [Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 1-3].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 4-8; Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 8-9; Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdo. 5; Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdos. 1-4

## q07 (single)
**Question:** ¿Cuántas horas de descanso deben pasar como mínimo entre el final de una jornada y el comienzo de la siguiente?
**Reference:** Doce horas como mínimo.
**Agent answer:**

> Entre el final de una jornada y el comienzo de la siguiente mediarán, como mínimo, doce horas [Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 1-3].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 4-8; Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 8-9; Estatuto de los Trabajadores (RDL 2/2015), Artículo 36, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 1-3

## q08 (single)
**Question:** ¿Cuántas horas extraordinarias puede hacer un trabajador al año?
**Reference:** No más de 80 al año (con las excepciones del apartado 3, p. ej. las compensadas con descanso).
**Agent answer:**

> El número máximo de horas extraordinarias que puede realizar un trabajador es de **ochenta al año**, con las siguientes excepciones y matizaciones:
> 
> * **Contratos a tiempo parcial o de duración inferior al año:** Para los trabajadores que realicen una jornada en cómputo anual inferior a la general de la empresa, el límite máximo anual de ochenta horas se reducirá en la misma proporción que exista entre ambas jornadas [Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdos. 1-4].
> * **Compensación por descanso:** No se computarán dentro de ese límite de ochenta horas aquellas horas extraordinarias que hayan sido compensadas mediante descanso dentro de los cuatro meses siguientes a su realización [Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdos. 1-4].
> * **Siniestros y daños extraordinarios:** No se tendrán en cuenta para el cómputo máximo las horas extraordinarias trabajadas para prevenir o reparar siniestros y otros daños extraordinarios y urgentes (aunque deben ser igualmente
>  compensadas) [Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdos. 1-4].
> * **Trabajadores nocturnos:** Los trabajadores nocturnos no pueden realizar horas extraordinarias [Estatuto de los Trabajadores (RDL 2/2015), Artículo 36, apdos. 1-3].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 31; Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdo. 5; Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdos. 1-4; Estatuto de los Trabajadores (RDL 2/2015), Artículo 36, apdos. 1-3

## q09 (single)
**Question:** ¿Cuánto descanso semanal mínimo tiene un trabajador adulto?
**Reference:** Día y medio ininterrumpido, acumulable por periodos de hasta 14 días.
**Agent answer:**

> Los trabajadores adultos tienen derecho a un descanso mínimo semanal de **día y medio ininterrumpido**, que como regla general comprenderá la tarde
>  del sábado o la mañana del lunes y el día completo del domingo [Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 1-3].
> 
> Este descanso mínimo es acumulable por periodos de hasta catorce días [Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 1-3].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 4-8; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdo. 6; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 3-4

## q10 (single)
**Question:** ¿Cuántos días de permiso retribuido tiene un empleado que se casa?
**Reference:** Quince días naturales (también por registro de pareja de hecho).
**Agent answer:**

> El empleado tiene derecho a **quince días naturales** de permiso retribuido en caso de matrimonio [Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 1-3].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdo. 3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdo. 9; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 3-4; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 5-6

## q11 (single)
**Question:** ¿Cuántos días de permiso hay por el fallecimiento de un familiar de segundo grado?
**Reference:** Dos días, ampliables en dos días más si necesita desplazarse.
**Agent answer:**

> Son **dos días**, que se ampliarán en **dos días más** cuando la persona trabajadora necesite hacer un desplazamiento al efecto [Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdo. 3].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdo. 3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdo. 9; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 3-4; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 5-6

## q12 (single)
**Question:** ¿Cuántas pagas extraordinarias al año tiene derecho a cobrar un trabajador?
**Reference:** Dos al año, una en Navidad y otra en el mes que fije el convenio o acuerdo; pueden prorratearse en doce mensualidades por convenio.
**Agent answer:**

> El trabajador tiene derecho a **dos gratificaciones extraordinarias al año**: una con ocasión de las fiestas de Navidad y otra en el mes que se fije por convenio colectivo o por acuerdo entre la empresa y los representantes legales de los trabajadores [Estatuto de los Trabajadores (RDL 2/2015), Artículo 31].
> 
> No obstante, se debe tener en cuenta lo siguiente:
> * Su cuantía se fija por convenio colectivo [Estatuto de los Trabajadores (RDL 2/2015), Artículo 31].
> * Mediante convenio colectivo se puede acordar que las grat
> ificaciones extraordinarias se prorrateen en las doce mensualidades [Estatuto de los Trabajadores (RDL 2/2015), Artículo 31].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 25; Estatuto de los Trabajadores (RDL 2/2015), Artículo 31; Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdos. 1-4; Estatuto de los Trabajadores (RDL 2/2015), Artículo 38; Estatuto de los Trabajadores (RDL 2/2015), Artículo 4, apdos. 1-2

## q13 (single)
**Question:** ¿Qué indemnización cobra un trabajador cuando termina su contrato temporal?
**Reference:** 12 días de salario por año de servicio (parte proporcional), salvo en contratos formativos y de sustitución.
**Agent answer:**

> A la finalización del contrato temporal, el trabajador tiene derecho a recibir una indemnización de cuantía equivalente a la parte proporcional de la cantidad que resultaría de abonar doce días de salario
>  por cada año de servicio, o la establecida en su caso en la normativa específica de aplicación [Estatuto de los Trabajadores (RDL 2/2015), Artículo 49, apdo. 1].
> 
> Quedan excluidos de esta indemnización los contratos formativos y el contrato de duración determinada por causa de sustitución [Estatuto de los Trabajadores (RDL 2/2015), Artículo 49, apdo. 1].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 15, apdos. 5-7; Estatuto de los Trabajadores (RDL 2/2015), Artículo 33, apdo. 2; Estatuto de los Trabajadores (RDL 2/2015), Artículo 49, apdo. 1; Estatuto de los Trabajadores (RDL 2/2015), Artículo 49, apdos. 1-2; Estatuto de los Trabajadores (RDL 2/2015), Disposición transitoria octava; Estatuto de los Trabajadores (RDL 2/2015), Disposición transitoria undécima

## q14 (single)
**Question:** ¿Qué requisitos y duración tiene la excedencia voluntaria?
**Reference:** Requiere al menos un año de antigüedad; dura entre cuatro meses y cinco años; no puede repetirse hasta pasados cuatro años desde la anterior.
**Agent answer:**

> Requisitos y duración de la excedencia voluntaria:
> 
> * **Antigüedad y duración:** El trabajador con al menos una antigüedad en la empresa de un año tiene derecho a que se le reconozca la posibilidad de situarse en excedencia voluntaria por un plazo no menor a cuatro meses y no mayor a cinco años [Estatuto de los Trabajadores (RDL 2/2015), Artículo 46, apdos. 1-3].
> * **Nueva solicitud:** Este derecho solo podrá ser ejercitado otra vez por el mismo trabajador si han transcurrido cuatro años desde el final de la anterior excedencia voluntaria [Estatuto de los Trabajadores (RDL 2/2015), Artículo 46, apdos. 1-3].
> * **Derecho de reingreso:** El trabajador en excedencia voluntaria conserva solo un derecho preferente al reingreso en las vacantes de igual o similar categoría a la suya que hubiera o se produjeran en la empresa [Estatuto de los Trabajadores (RDL 2/2015), Artículo 46, apdos. 3-6].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 45; Estatuto de los Trabajadores (RDL 2/2015), Artículo 46, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 46, apdos. 3-6; Estatuto de los Trabajadores (RDL 2/2015), Artículo 48, apdos. 1-4; Estatuto de los Trabajadores (RDL 2/2015), Artículo 48, apdos. 5-7

## q15 (single)
**Question:** ¿Cuánto tiempo puede durar una excedencia para cuidar a un hijo?
**Reference:** Hasta tres años desde el nacimiento (o resolución de adopción/acogimiento); durante el primer año hay reserva del puesto.
**Agent answer:**

> La excedencia para el cuidado de cada hijo tiene una duración máxima de **tres años** [Estatuto de los Trabajadores (RDL 2/2015), Artículo 46, apdos. 1-3].
> 
> Detalles clave sobre su duración y disfrute:
> * **Cómputo:** Se cuenta desde la fecha de nacimiento o, en su caso, de la resolución judicial o administrativa de adopción, guarda con fines de adopción o acogimiento permanente [Estatuto de los Trabajadores (RDL 2/2015), Artículo 46, apdos. 1-3].
> * **Derecho individual:** Constituye un derecho individual de los trabajadores y trabajadoras y puede disfrutarse de forma fraccionada [Estatuto de los Trabajadores (RDL 2/2015), Artículo 46, apdos. 1-3].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdo. 6; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 5-6; Estatuto de los Trabajadores (RDL 2/2015), Artículo 46, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 46, apdos. 3-6; Estatuto de los Trabajadores (RDL 2/2015), Artículo 48 bis

## q16 (single)
**Question:** ¿Cuántas semanas dura la suspensión del contrato por nacimiento?
**Reference:** Diecinueve semanas para cada progenitor (treinta y dos en familias monoparentales); seis semanas posteriores al parto son obligatorias.
**Agent answer:**

> La suspensión del contrato por nacimiento (que comprende el parto y el cuidado del menor) dura **diecinueve semanas** para cada uno de los progenitores (madre biológica y progenitor distinto de la madre biológica) [Estatuto de los Trabajadores (RDL 2/2015), Artículo 48, apdos. 1-4].
> 
> En los supuestos de monoparentalidad, el periodo de suspensión es de **32 semanas** [Estatuto de los Trabajadores (RDL 2/2015), Artículo 48, apdos. 1-4].
> 
> La distribución de estas diecinueve semanas para cada progenitor se organiza de la siguiente manera:
> * **6 semanas** obligatorias e ininterrumpidas a jornada completa, inmediatamente posteriores al parto (en el caso de la madre biológica, se pueden anticipar hasta cuatro semanas antes de la fecha previsible) [Estatuto de los Trabajadores (RDL 2/2015), Artículo 48, apdo. 4].
> * **11 semanas** que se pueden disfrutar en periodos semanales, de forma acumulada o interrumpida, hasta que el hijo cumpla doce meses [Estatuto de los Trabajadores (RDL 2/2015), Artículo 48, apdo. 4].
> * **2 semanas** para el cuidado del menor, que se pueden distribuir en periodos semanales de forma acumulada o interrumpida hasta que el menor cumpla ocho años [Estatuto de los Trabajadores (RDL 2/2015), Artículo 48, apdo. 4].
> 
> **Ampliaciones adicionales:**
> * **Discapacidad o parto múltiple:** Se concede una duración adicional de dos semanas (una para cada progenitor) por cada hijo a partir del segundo o en caso de discapacidad del hijo [Estatuto de los Trabajadores (RDL 2/2015), Artículo 48, apdos. 5-7].
> * **Hospitalización:** Si el neonato debe permanecer hospitalizado a continuación del parto por un periodo superior a siete días, el periodo de suspensión se amplía en tantos días como esté hospitalizado, con un máximo de trece semanas adicionales [Estatuto de los Trabajadores (RDL 2/2015), Artículo 48, apdo. 4].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 45; Estatuto de los Trabajadores (RDL 2/2015), Artículo 48, apdo. 4; Estatuto de los Trabajadores (RDL 2/2015), Artículo 48, apdos. 1-4; Estatuto de los Trabajadores (RDL 2/2015), Artículo 48, apdos. 4-5; Estatuto de los Trabajadores (RDL 2/2015), Artículo 48, apdos. 5-7

## q17 (single)
**Question:** ¿Qué plazo tiene un trabajador para reclamar contra su despido?
**Reference:** Veinte días hábiles desde el despido (plazo de caducidad), interrumpido por la papeleta de conciliación.
**Agent answer:**

> El ejercicio de la acción contra el despido caducará a los **veinte días siguientes** a aquel en que se hubiera producido [Estatuto de los Trabajadores (RDL 2/2015), Artículo 59].
> 
> A estos efectos:
> * Los días son **hábiles** [Estatuto de los Trabajadores (RDL 2/2015), Artículo 59].
> * El plazo de caducidad **queda interrumpido** por la presentación de la solicitud de conciliación ante el órgano público de mediación, arbitraje y conciliación competente [Estatuto de los Trabajadores (RDL 2/2015), Artículo 59].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 33, apdo. 11; Estatuto de los Trabajadores (RDL 2/2015), Artículo 55, apdos. 1-5; Estatuto de los Trabajadores (RDL 2/2015), Artículo 56; Estatuto de los Trabajadores (RDL 2/2015), Artículo 59; Estatuto de los Trabajadores (RDL 2/2015), Disposición transitoria undécima

## q18 (single)
**Question:** ¿Cuándo prescriben las faltas muy graves cometidas por un trabajador?
**Reference:** A los sesenta días desde que la empresa tuvo conocimiento y, en todo caso, a los seis meses de cometerse.
**Agent answer:**

> Las faltas muy graves cometidas por un trabajador prescriben a los **sesenta días** a partir de la fecha en que la empresa tuvo conocimiento de su comisión y, en todo caso, a los **seis meses** de haberse cometido [Estatuto de los Trabajadores (RDL 2/2015), Artículo 60].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 54; Estatuto de los Trabajadores (RDL 2/2015), Artículo 58; Estatuto de los Trabajadores (RDL 2/2015), Artículo 59; Estatuto de los Trabajadores (RDL 2/2015), Artículo 60; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 8, apdos. 1-11

## q19 (single)
**Question:** ¿Durante cuánto tiempo debe la empresa conservar el registro de jornada?
**Reference:** Cuatro años, a disposición de trabajadores, representantes e Inspección.
**Agent answer:**

> La empresa debe conservar los registros de jornada durante **cuatro años** [Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdo. 9]. 
> 
> Además, durante dicho período, los registros deben permanecer a disposición de las personas trabajadoras, de sus representantes legales y de la Inspección de Trabajo y Seguridad Social [Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdo. 9].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdo. 9; Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 4-8; Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 8-9; Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdo. 5; Estatuto de los Trabajadores (RDL 2/2015), Artículo 59

## q20 (single)
**Question:** ¿Cuánto puede durar como máximo un contrato por circunstancias de la producción?
**Reference:** Seis meses, ampliables hasta un año por convenio colectivo sectorial.
**Agent answer:**

> La duración máxima de un contrato por circunstancias de la producción depende de la causa que lo motive:
> 
> * **Incremento ocasional e imprevisible (o oscilaciones que generan desajuste temporal):** Su duración máxima es de **seis meses**. No obstante, por convenio colectivo de ámbito sectorial se puede ampliar hasta **un año**. Si se firma por un plazo inferior al máximo, se puede prorrogar por acuerdo de las partes por una única vez, sin superar dicha duración máxima [Estatuto de los Trabajadores (RDL 2/2015), Artículo 15, apdos. 1-2].
> * **Situaciones ocasionales, previsibles y de duración reducida y delimitada:** El contrato solo se puede utilizar un máximo de **noventa días en el año natural** (excepción hecha de las empresas del sector agrario y agroalimentario, que pueden utilizar un total de 120 días), los cuales no podrán ser utilizados de manera continuada [Estatuto de los Trabajadores (RDL 2/2015), Artículo 15, apdos. 1-2].
> 
> Asimismo, se adquiere la condición de persona trabajadora fija si en un periodo de veinticuatro meses se acumulan contratos por circunstancias de la producción (directamente o mediante ETT) durante un plazo superior a **dieciocho meses** [Estatuto de los Trabajadores (RDL 2/2015), Artículo 15, apdos. 5-7].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 11, apdo. 3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 15, apdos. 1-2; Estatuto de los Trabajadores (RDL 2/2015), Artículo 15, apdos. 2-4; Estatuto de los Trabajadores (RDL 2/2015), Artículo 15, apdos. 5-7; Estatuto de los Trabajadores (RDL 2/2015), Artículo 15, apdos. 8-9

## q21 (single)
**Question:** Una empresa tiene 80 trabajadores: ¿cuántos delegados de prevención le corresponden?
**Reference:** Dos delegados de prevención (escala de 50 a 100 trabajadores).
**Agent answer:**

> A una empresa de 80 trabajadores le corresponden **2 Delegados de Prevención** [Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 35, apdos. 1-4].
> 
> Detalles a tener en cuenta:
> * **Escala legal:** La Ley de Prevención de Riesgos Laborales establece la escala de 50 a 100 trabajadores en 2 Delegados de Prevención [Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 35, apdos. 1-4].
> * **Designación:** Son designados por y entre los representantes del personal (miembros del comité de empresa o delegados de personal) [Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 35, apdos. 1-4].
> * **Cómputo de la plantilla:** Para calcular el número de trabajadores se aplican reglas específicas sobre contratos temporales (los de duración inferior a un año se computan según los días trabajados: cada 200 días o fracción equivalen a un trabajador más) [Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 35, apdos. 1-4].
> * **Convenio colectivo:** Se debe comprobar el convenio colectivo aplicable, ya que puede establecer otros sistemas de designación respetando que la facultad corresponda a los representantes o a los propios trabajadores [Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 35, apdos. 1-4].
**Passages retrieved:** Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 35, apdo. 4; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 35, apdos. 1-4; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 36, apdos. 1-2; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Disposición adicional cuarta; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Disposición adicional décima

## q22 (single)
**Question:** ¿Qué empresas deben tener Comité de Seguridad y Salud y cada cuánto se reúne?
**Reference:** Las empresas o centros con 50 o más trabajadores; se reúne trimestralmente y siempre que lo pida una de las partes.
**Agent answer:**

> Deben constituir un Comité de Seguridad y Salud todas las empresas o centros de trabajo que cuenten con 50 o más trabajadores [Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 38]. 
> 
> El Comité se reunirá trimestralmente y siempre que lo solicite alguna de las representaciones en el mismo [Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 38].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 66; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 34, apdo. 3; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 38; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 39, apdo. 3; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 39, apdos. 1-2

## q23 (single)
**Question:** ¿Cuándo prescriben las infracciones en materia de prevención de riesgos laborales?
**Reference:** Leves al año, graves a los tres años y muy graves a los cinco años desde la infracción.
**Agent answer:**

> En materia de prevención de riesgos laborales, el plazo de prescripción de las infracciones se cuenta desde la fecha de la infracción y varía según su gravedad:
> 
> * **Infracciones leves:** prescriben al **año**.
> * **Infracciones graves:** prescriben a los **tres años**.
> * **Infracciones muy graves:** prescriben a los **cinco años**.
> 
> [Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 4]
**Passages retrieved:** Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 11; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 12, apdos. 1-5; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 4; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 40, apdos. 1-2; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 42, apdos. 5-6

## q24 (single)
**Question:** ¿Cuál es la multa máxima por una infracción muy grave en prevención de riesgos laborales?
**Reference:** Hasta 983.736 euros (grado máximo: 491.866 a 983.736 euros).
**Agent answer:**

> La multa máxima por una infracción muy grave en prevención de riesgos laborales es de **983.736 euros** (en su grado máximo) [Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 40, apdos. 1-2]. 
> 
> Las cuantías para las infracciones muy graves en materia de prevención de riesgos laborales se distribuyen de la siguiente manera:
> * **Grado mínimo:** de 49.181 a 196.745 euros [Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 40, apdos. 1-2].
> * **Grado medio:** de 196.746 a 491.865 euros [Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 40, apdos. 1-2].
> * **Grado máximo:** de 491.866 a 983.736 euros [Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 40, apdos. 1-2].
**Passages retrieved:** Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 12, apdos. 1-5; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 13, apdos. 1-7; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 13, apdos. 8-11; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 40, apdo. 1; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 40, apdos. 1-2

## m01 (multi)
**Question:** ¿En qué se diferencia la indemnización de un despido objetivo de la de un despido improcedente?
**Reference:** Objetivo: 20 días por año con máximo de 12 mensualidades. Improcedente: 33 días por año con máximo de 24 mensualidades.
**Agent answer:**

> Las principales diferencias entre la indemnización por despido objetivo y la de despido improcedente son las siguientes:
> 
> * **Despido objetivo (causas económicas, técnicas, organizativas, de producción, etc.):** 
>   * La cuantía es de **20 días de salario por año de servicio**, prorrateándose por meses los períodos inferiores a un año, con un **máximo de 12 mensualidades** [Estatuto de los Trabajadores (RDL 2/2015), Artículo 53, apdos. 1-4].
>   * Debe ponerse a disposición del trabajador simultáneamente a la entrega de la comunicación escrita (salvo en caso de causa económica si se justifica la imposibilidad en el momento) [Estatuto de los Trabajadores (RDL 2/2015), Artículo 53, apdos. 1-4].
> 
> * **Despido improcedente:**
>   * Para contratos suscritos a partir del 12 de febrero de 2012, la indemnización es de **33 días de salario por año de servicio**, prorrateándose por meses los períodos inferiores a un año, con un **máximo de 24 mensualidades** [Estatuto de los Trabajadores (RDL 2/2015), Artículo 56]. *(Nota: Para contratos anteriores
>  a dicha fecha existen reglas de cálculo específicas por tramos temporales y topes indemnizatorios mayores previstos en la Disposición transitoria undécima).*
>   * Se abona si el empresario opta por la indemnización frente a la readmisión tras ser declarado improcedente el despido [Estatuto de los Trabajadores (RDL 2/2015), Artículo 56]. Si el despido objetivo inicial se declara improcedente y se opta por la indemnización o la readmisión, se aplican las reglas específicas de deducción o reintegro de la cantidad ya entregada en el despido objetivo [Estatuto de los Trabajadores (RDL 2/2015), Artículo 53, apdo. 5].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 33, apdo. 2; Estatuto de los Trabajadores (RDL 2/2015), Artículo 53, apdo. 5; Estatuto de los Trabajadores (RDL 2/2015), Artículo 53, apdos. 1-4; Estatuto de los Trabajadores (RDL 2/2015), Artículo 56; Estatuto de los Trabajadores (RDL 2/2015), Disposición transitoria undécima

## m02 (multi)
**Question:** Tenemos un empleado de 17 años: ¿puede hacer horas extra y cuántas horas puede trabajar al día?
**Reference:** No puede hacer horas extraordinarias (ni trabajo nocturno) y no puede trabajar más de 8 horas diarias de trabajo efectivo, incluida la formación.
**Agent answer:**

> * **Horas extraordinarias:** **
> No**, los menores de 18 años tienen prohibido realizar horas extraordinarias [Estatuto de los Trabajadores (RDL 2/2015), Artículo 6].
> * **Jornada diaria:** Como máximo podrán trabajar **ocho horas diarias** de trabajo efectivo, incluyendo, en su caso, el tiempo dedicado a la formación y las horas realizadas con otros empleadores si trabajasen para varios [Estatuto de los Trabajadores (RDL 2/2015), Artículo 34].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 4-8; Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdo. 5; Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdos. 1-4; Estatuto de los Trabajadores (RDL 2/2015), Artículo 6

## m03 (multi)
**Question:** Si una empresa no lleva el registro diario de jornada: ¿qué obligación incumple y qué tipo de infracción comete?
**Reference:** Incumple la obligación de garantizar el registro diario de jornada con hora de inicio y fin (ET art. 34.9); es una infracción grave (LISOS art. 7.5).
**Agent answer:**

> Incumple la obligación de garantizar el registro diario de jornada, que deberá incluir el horario concreto de inicio y finalización de la jornada de trabajo de cada persona trabajadora [Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdo. 9].
> 
> Comete una infracción grave tipificada como la transgresión de las normas y los límites legales o pactados en materia de jornada, trabajo nocturno, horas extraordinarias, horas complementarias, descansos, vacaciones, permisos, registro de jornada y, en general, el tiempo de trabajo [Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 7, apdos. 1-9].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdo. 9; Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 8-9; Estatuto de los Trabajadores (RDL 2/2015), Artículo 35, apdo. 5; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 12, apdos. 1-5; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 15, apdos. 1-6; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 22, apdos. 6-10; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 7, apdos. 1-9; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 7, apdos. 10-16

## m04 (multi)
**Question:** ¿Está obligada la empresa a formar a los trabajadores en prevención de riesgos y qué infracción comete si no lo hace?
**Reference:** Sí: formación teórica y práctica suficiente al contratar y al cambiar funciones o tecnologías, dentro de la jornada y sin coste para el trabajador; incumplirlo es una infracción grave (LISOS art. 12.8).
**Agent answer:**

> Sí, el empresario está obligado a garantizar que cada trabajador reciba una formación teórica y práctica, suficiente y adecuada, en materia preventiva, tanto en el momento de su contratación como cuando se produzcan cambios en las funciones que desempeñe o se introduzcan nuevas tecnologías o cambios en los equipos de trabajo [CITE AS: [Ley de Prevención de Riesgos Laborales (Ley 
> 31/1995), Artículo 19] | en vigor desde 1996-02-10 | https://www.boe.es/buscar/act.php?id=BOE-A-1995-24292].
> 
> Si la empresa incumple las obligaciones en materia de formación e información suficiente y adecuada a los trabajadores acerca de los riesgos del puesto de trabajo y sobre las medidas preventivas aplicables, comete una infracción grave, salvo que se trate de una infracción muy grave conforme al artículo siguiente [CITE AS: [Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 12, apdos. 6-12] | en vigor desde 2007-04-19 | https://www.boe.es/buscar/act.php?id=BOE-A-2000-15060].
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 19; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 14, apdos. 1-2; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 18; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 19; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 29, apdos. 1-2; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 11; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 12, apdos. 1-5; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 12, apdos. 13-16; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 12, apdos. 6-12

## m05 (multi)
**Question:** Ante un riesgo grave e inminente ¿puede el trabajador dejar su puesto y qué pasa si la empresa se lo impide?
**Reference:** Sí, puede interrumpir su actividad y abandonar el lugar de trabajo sin sufrir perjuicio salvo mala fe o negligencia grave; impedir ese derecho es infracción muy grave (LISOS art. 13.9).
**Agent answer:**

> Sí, el trabajador tiene derecho a interrumpir su actividad y abandonar el lugar de trabajo cuando considere que dicha actividad entraña un riesgo grave e inminente para su vida o su salud [Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 21, apdos. 1-3]. 
> 
> Además, los trabajadores o sus representantes no pueden sufrir ningún perjuicio derivado de la adopción de esta medida, a menos que hubieran obrado de mala fe o cometido negligencia grave [Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 21, apdo. 4].
**Passages retrieved:** Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 14, apdos. 1-2; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 21, apdo. 4; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 21, apdos. 1-3; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 44; Ley de Prevención de Riesgos Laborales (Ley 31/1995), Artículo 53

## m06 (multi)
**Question:** ¿Qué infracción comete la empresa que no da de alta en la Seguridad Social a un trabajador y con qué multa se sanciona?
**Reference:** Infracción grave (art. 22.2), una por trabajador afectado; multa de 3.750 a 12.000 euros según grado (art. 40.1.e).
**Agent answer:**

> La empresa que no solicita la afiliación inicial o el alta de los trabajadores que ingresan a su servicio, o la solicita fuera de plazo como consecuencia de actuación inspectora, comete una infracción grave, considerándose una infracción por cada uno de los trabajadores afectados [Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 22, apdos. 1-5].
> 
> Las sanciones correspondientes se recogen en el artículo 40 de la LISOS [Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 40, apdo. 1].
**Passages retrieved:** Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 22, apdos. 1-5; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 22, apdos. 11-15; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 22, apdos. 15-16; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 22, apdos. 6-10; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 40, apdo. 1; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 40, apdos. 1-2

## u01 (unanswerable)
**Question:** ¿Cuál es la cuantía del salario mínimo interprofesional este año?
**Reference:** El corpus no lo cubre: el ET solo dice que el Gobierno fija el SMI anualmente; la cuantía está en el real decreto anual, no indexado.
**Agent answer:**

> El corpus no cubre esta pregunta. El texto consolidado del Estatuto de los Trabajadores establece que el Gobierno fija anualmente el salario mínimo interprofesional [Estatuto de los Trabajadores (RDL 2/2015), Artículo 27], pero no especifica la cuantía concreta vigente para el año en curso.
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 26; Estatuto de los Trabajadores (RDL 2/2015), Artículo 27; Estatuto de los Trabajadores (RDL 2/2015), Artículo 32; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 40, apdo. 1; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 40, apdos. 1-2

## u02 (unanswerable)
**Question:** ¿Tiene la empresa que pagar los gastos de internet y equipos de un trabajador en teletrabajo?
**Reference:** El corpus base no lo cubre: el ET remite a la Ley 10/2021 de trabajo a distancia, que no está indexada (se añade después con add_document).
**Agent answer:**

> El corpus no cubre esta pregunta porque el régimen detallado de compensación de gastos e internet en el teletrabajo se remite a la Ley 10/2021 de trabajo a distancia, la cual no se encuentra indexada en la base de datos actual. 
> 
> No obstante, el Estatuto de los Trabajadores establece expresamente que la empresa tiene la obligación de suministrar los medios, equipos y herramientas adecuados para el trabajo a distancia [Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 3-4]. Para los gastos específicos de internet y otros detalles de compensación, debe consultarse la normativa específica de trabajo a distancia y el convenio colectivo aplicable.
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 13; Estatuto de los Trabajadores (RDL 2/2015), Artículo 20 bis; Estatuto de los Trabajadores (RDL 2/2015), Artículo 21; Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 4-8; Estatuto de los Trabajadores (RDL 2/2015), Artículo 34, apdos. 8-9; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 3-4; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 7-8; Estatuto de los Trabajadores (RDL 2/2015), Artículo 40, apdo. 1; Estatuto de los Trabajadores (RDL 2/2015), Artículo 40, apdos. 6-7

## u03 (unanswerable)
**Question:** ¿Qué porcentaje del salario cobra un trabajador de baja por enfermedad común a partir del cuarto día?
**Reference:** El corpus no lo cubre: la prestación por incapacidad temporal está en la Ley General de la Seguridad Social, no indexada.
**Agent answer:**

> El corpus no cubre esta pregunta. La información sobre los porcentajes del subsidio por incapacidad temporal y sus tramos se encuentra en la Ley General de la Seguridad Social, la cual no está indexada en el corpus actual.
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 14, apdo. 3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 29; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdo. 9; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 5-6; Estatuto de los Trabajadores (RDL 2/2015), Artículo 47, apdo. 7; Estatuto de los Trabajadores (RDL 2/2015), Artículo 47, apdos. 5-7; Estatuto de los Trabajadores (RDL 2/2015), Disposición transitoria octava; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 40, apdo. 1

## u04 (unanswerable)
**Question:** ¿Cuánto tiempo puede cobrar el paro un trabajador despedido?
**Reference:** El corpus no lo cubre: la prestación por desempleo está en la Ley General de la Seguridad Social, no indexada.
**Agent answer:**

> El corpus no cubre esta pregunta. La duración de la prestación por
>  desempleo contributiva según los días cotizados se regula en la Ley General de la Seguridad Social, una norma que no se encuentra indexada en el corpus actual.
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 47, apdo. 7; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Articulo 47, apdo. 1; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Articulo 47, apdos. 1-2; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 24, apdo. 4; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 24, apdos. 1-3; Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000), Artículo 25

## u05 (unanswerable)
**Question:** ¿Cuántos días de vacaciones fija el convenio colectivo de hostelería?
**Reference:** El corpus no lo cubre: los convenios colectivos no están indexados; el ET solo fija el mínimo de 30 días naturales.
**Agent answer:**

> El corpus no cubre esta pregunta. El texto legal disponible no contiene los convenios colectivos específicos del sector de hostelería, por lo que debe consultarse el convenio colectivo de hostelería aplicable en su territorio o sector para conocer los días exactos de vacaciones que fija.
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 31; Estatuto de los Trabajadores (RDL 2/2015), Artículo 37, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 38; Estatuto de los Trabajadores (RDL 2/2015), Artículo 84, apdos. 1-2; Estatuto de los Trabajadores (RDL 2/2015), Artículo 86, apdos. 1-4

## u06 (unanswerable)
**Question:** ¿Qué tipo de cotización a la Seguridad Social por contingencias comunes paga la empresa?
**Reference:** El corpus no lo cubre: los tipos de cotización se fijan en la normativa de Seguridad Social y la orden anual de cotización, no indexadas.
**Agent answer:**

> El corpus no cubre esta pregunta. (La cuantía y los tipos específicos de cotización empresarial a la Seguridad Social por contingencias comunes no están regulados en el Estatuto de los Trabajadores ni en las demás normas indexadas en el corpus, sino en la Ley de Presupuestos Generales del Estado y en la normativa específica de la Seguridad Social).
**Passages retrieved:** Estatuto de los Trabajadores (RDL 2/2015), Artículo 33, apdos. 4-8; Estatuto de los Trabajadores (RDL 2/2015), Artículo 42, apdos. 1-3; Estatuto de los Trabajadores (RDL 2/2015), Artículo 44, apdos. 1-5; Estatuto de los Trabajadores (RDL 2/2015), Disposición adicional vigésima; Estatuto de los Trabajadores (RDL 2/2015), Disposición final primera
