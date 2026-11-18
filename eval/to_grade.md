# Answers to grade by hand

Grade at least 20 of these **before** opening `eval/judge.jsonl` or `eval/results.csv` so the judge doesn't sway you.
For each one, add a row to `eval/human_labels.csv`: `id,correct,supported,notes` (1 = yes, 0 = no).

- **correct**: it gives the reference answer's key point (for an unanswerable question: it refuses), with no wrong statement that would mislead a tenant.
- **supported**: every claim is backed by the passages cited (open the article link to check).

Same rubric as the LLM judge (see `RUBRIC` in `evaluate.py`).

---

## q01 (single)

**Question:** ¿Cuántos meses de fianza me pueden exigir al alquilar un piso como vivienda?

**Expected:** LAU (Ley 29/1994) · Artículo 36

**Reference answer:** Una mensualidad de renta en metálico (dos para uso distinto de vivienda).

**Agent answer:**

> Al alquilar una vivienda, por ley es obligatoria una **fianza en metálico equivalente a una mensualidad de renta** [LAU (Ley 29/1994), Artículo 36. Fianza].
> 
> Adicionalmente, las partes pueden pactar **garantías adicionales** a la fianza en metálico (como un depósito extra o un aval), pero en los contratos de vivienda de hasta 5 años (o hasta 7 años si el arrendador es una persona jurídica) estas garantías adicionales **no pueden superar un máximo de dos mensualidades de renta** [LAU (Ley 29/1994), Artículo 36. Fianza].
> 
> *Confirme los detalles particulares de su contrato con un abogado o con el organismo de vivienda de su comunidad autónoma.*

*Searches: ['fianza vivienda mensualidades arrendamiento articulo']*

---

## q02 (single)

**Question:** Además de la fianza, ¿cuánto puede pedirme el casero como garantía adicional?

**Expected:** LAU (Ley 29/1994) · Artículo 36

**Reference answer:** En contratos de vivienda de hasta 5 años (7 si el arrendador es persona jurídica), la garantía adicional no puede superar dos mensualidades; en arrendamientos temporales, una.

**Agent answer:**

> En los contratos de arrendamiento de vivienda de hasta cinco años de duración (o hasta siete años si el arrendador es una persona jurídica), el valor de la garantía adicional **no puede exceder de dos mensualidades de renta** [LAU (Ley 29/1994), Artículo 36. Fianza]. En los arrendamientos temporales, esta garantía adicional no puede superar una mensualidad [LAU (Ley 29/1994), Artículo 36. Fianza]. 
> 
> Además, la ley establece que no puede exigirse al arrendatario la contratación de seguros de impago de renta u otras coberturas análogas como garantía adicional [LAU (Ley 29/1994), Artículo 36. Fianza].
> 
> *Confirme los detalles de su contrato con un abogado o con el servicio de vivienda de su comunidad autónoma.*

*Searches: ['garantia adicional arrendamiento vivienda maximo LAU articulo 36']*

---

## q03 (single)

**Question:** Si el propietario es una persona física, ¿cuál es la duración mínima de mi contrato de alquiler?

**Expected:** LAU (Ley 29/1994) · Artículo 9

**Reference answer:** Cinco años: si se pacta menos, el contrato se prorroga obligatoriamente por plazos anuales hasta cinco años, salvo que el inquilino avise con 30 días de antelación de que no renueva.

**Agent answer:**

> La duración del contrato es la que las partes pacten libremente, pero si esta es inferior a **cinco años**, el contrato se prorrogará obligatoriamente por plazos anuales hasta alcanzar esa duración mínima de **cinco años**, siempre que el arrendador sea persona física [LAU (Ley 29/1994), Artículo 9. Plazo mínimo].
> 
> * **Excepción de necesidad:** Si transcurrido el primer año se hizo constar expresamente en el contrato la necesidad del propietario de ocupar la vivienda para sí, sus familiares en primer grado de consanguinidad/adopción o su cónyuge en casos de sentencia firme de separación/divorcio/nulidad, no procederá dicha prórroga obligatoria, debiendo avisar al inquilino con al menos dos meses de antelación [LAU (Ley 29/1994), Artículo 9. Plazo mínimo].
> * **Desistimiento del inquilino:** El arrendatario puede manifestar su voluntad de no renovar el contrato avisando con al menos treinta días de antelación a la fecha de terminación del contrato o de cualquiera de sus prórrogas [LAU (Ley 29/1994), Artículo 9. Plazo mínimo].
> 
> *Nota: Esta respuesta se basa en la normativa general de alquiler de vivienda habitual; se recomienda confirmar el caso particular con un abogado o con el organismo de vivienda de su comunidad autónoma.*

*Searches: ['duracion contrato arrendamiento vivienda persona fisica plazo minimo lau']*

---

## q04 (single)

**Question:** ¿Puedo irme del piso antes de que termine el contrato? ¿Con cuánto preaviso?

**Expected:** LAU (Ley 29/1994) · Artículo 11

**Reference answer:** Sí, una vez transcurridos al menos seis meses, avisando al arrendador con 30 días de antelación; no genera indemnización para el arrendador.

**Agent answer:**

> Sí, puedes irte del piso antes de que termine el contrato, siempre que cumplas los siguientes requisitos [LAU (Ley 29/1994), Artículo 11. Desistimiento del contrato]:
> 
> * **Plazo mínimo:** Deben haber transcurrido **al menos seis meses** desde el inicio del contrato (o al menos un mes si se trata de un contrato de vivienda temporal) [LAU (Ley 29/1994), Artículo 11. Desistimiento del contrato].
> * **Preaviso:** Debes comunicárselo al arrendador con una antelación mínima de **treinta días** (o de diez días en caso de vivienda temporal) [LAU (Ley 29/1994), Artículo 11. Desistimiento del contrato].
> 
> Este desistimiento no genera derecho de indemnización a favor del arrendador, salvo que el propio contrato incluya alguna previsión al respecto (generalmente una compensación pactada para estos casos, limitada por ley) [LAU (Ley 29/1994), Artículo 11. Desistimiento del contrato].
> 
> *Nota: Para casos particulares o disputas sobre penalizaciones, se recomienda confirmar el asunto con un abogado o con el organismo de vivienda de tu comunidad autónoma.*

*Searches: ['arrendatario desistimiento contrato plazo preaviso LAU']*

---

## q05 (single)

**Question:** Can my landlord make me pay the real estate agency's fees for the rental contract?

**Expected:** LAU (Ley 29/1994) · Artículo 20

**Reference answer:** No. Property management and contract formalisation costs cannot be passed on to the tenant, directly or indirectly.

**Agent answer:**

> **No**, your landlord cannot make you pay the real estate agency's fees for the rental contract [LAU (Ley 29/1994), Artículo 20].
> 
> * **The general rule:** Real estate management and contract formalization fees must be borne by the landlord, and cannot be passed on to the tenant directly or indirectly under any concept or denomination [LAU (Ley 29/1994), Artículo 20.2].
> * **Exceptions:** Any other service not essential for the perfection of the contract can only be charged to the tenant if the tenant has expressly requested it in writing, having been informed beforehand of its optional nature and cost [LAU (Ley 29/1994), Artículo 20.2].
> 
> *Confirm this with a lawyer or your regional housing office if you are facing a dispute.*

*Searches: ['gastos de gestión inmobiliaria y de formalización del contrato arrendador arrendatario LAU']*

---

## q06 (single)

**Question:** ¿Quién paga las pequeñas reparaciones por el desgaste normal del piso?

**Expected:** LAU (Ley 29/1994) · Artículo 21

**Reference answer:** El arrendatario: las pequeñas reparaciones que exija el desgaste por el uso ordinario son de su cargo.

**Agent answer:**

> Las pequeñas reparaciones que exija el desgaste por el uso ordinario de la vivienda corren a cargo del **arrendatario** (inquilino) [LAU (Ley 29/1994), Artículo 21. Conservación de la vivienda]. 
> 
> *Nota: Para casos particulares o disputas, se recomienda confirmarlo con un abogado o con el servicio de vivienda de su comunidad autónoma.*

*Searches: ['reparaciones desgaste pequeño conservación vivienda arrendatario arrendador']*

---

## q07 (single)

**Question:** El casero no responde cuando le pido arreglar una avería que afecta a la habitabilidad. ¿Qué puedo hacer?

**Expected:** LAU (Ley 29/1994) · Artículo 21

**Reference answer:** Si transcurre el plazo sin respuesta o hay negativa injustificada, el inquilino puede ejecutar las obras necesarias y descontar su importe (razonable y acreditado) de las rentas futuras.

**Agent answer:**

> Si el casero no responde a una avería que afecta a la habitabilidad, puedes proceder de la siguiente manera según la Ley de Arrendamientos Urbanos (LAU):
> 
> 1. **Requerimiento formal:** Debes comunicarle la necesidad de la reparación por escrito, adjuntando un presupuesto razonable para su ejecución [LAU (Ley 29/1994), Artículo 21.5].
> 2. **Plazo de respuesta:** El arrendador dispone de un plazo de **15 días naturales** desde la recepción del requerimiento para aceptar el presupuesto, proponer una alternativa o ejecutar la obra directamente [LAU (Ley 29/1994), Artículo 21.5].
> 3. **Ejecución y descuento:** Si transcurre ese plazo sin respuesta o se niega injustificadamente, puedes **ejecutar las obras tú mismo** (siempre que el coste sea razonable, adecuado a los daños y esté documentado) y **descontar su importe de las rentas futuras** [LAU (Ley 29/1994), Artículo 21.2].
> 4. **Reparaciones urgentes:** Si se trata de una urgencia para evitar un daño inminente o una incomodidad grave, puedes realizarlas de inmediato previa comunicación al arrendador y exigirle su importe de forma inmediata [LAU (Ley 29/1994), Artículo 21.3].
> 
> *Nota: Se recomienda confirmar los pasos y la documentación con un abogado o con el servicio de vivienda de tu comunidad autónoma ante cualquier disputa.*

*Searches: ['conservación reparaciones vivienda arrendatario obras']*

---

## q08 (single)

**Question:** Si mi contrato no dice nada sobre actualizar la renta, ¿me la pueden subir cada año?

**Expected:** LAU (Ley 29/1994) · Artículo 18

**Reference answer:** No: sin pacto expreso no se aplica actualización; si se pacta, el incremento anual no puede superar la variación del IRAV.

**Agent answer:**

> **No**, no te la pueden subir: en defecto de pacto expreso en el contrato, no se aplica la actualización de la renta [LAU (Ley 29/1994), Artículo 18. Actualización de la renta].
> 
> *Condiciones y excepciones:*
> * Para que exista actualización, debe haberse incluido un pacto expreso en el contrato [LAU (Ley 29/1994), Artículo 18. Actualización de la renta].
> * Si hubiera pacto pero no detallase un índice o metodología de referencia, la subida se calcula conforme al índice legal correspondiente (IRAV) [LAU (Ley 29/1994), Artículo 18. Actualización de la renta].
> 
> *Confirma este caso particular con un abogado o con el servicio de vivienda de tu comunidad autónoma.*

*Searches: ['actualizacion renta contrato pacto expreso LAU']*

---

## q09 (single)

**Question:** ¿Cuántos meses de renta por adelantado me puede exigir el arrendador?

**Expected:** LAU (Ley 29/1994) · Artículo 17

**Reference answer:** Como máximo una mensualidad; salvo pacto, el pago es mensual en los siete primeros días del mes.

**Agent answer:**

> En cuanto al pago anticipado de la renta, el arrendador **no puede exigir en ningún caso el pago anticipado de más de una mensualidad** de renta [LAU (Ley 29/1994), Artículo 17. Determinación de la renta].
> 
> No obstante, al inicio del contrato se deben distinguir otros conceptos económicos que el arrendador puede exigir legalmente:
> * **Fianza obligatoria:** Equivalente a **1 mensualidad** de renta en el arrendamiento de vivienda (2 mensualidades si es para uso distinto del de vivienda) [LAU (Ley 29/1994), Artículo 36. Fianza].
> * **Garantías adicionales:** Las partes pueden pactar garantías adicionales a la fianza en metálico. En los contratos de vivienda de hasta 5 años de duración (o hasta 7 años si el arrendador es persona jurídica), esta garantía adicional no puede exceder de **2 mensualidades** de renta [LAU (Ley 29/1994), Artículo 36. Fianza]. En los arrendamientos temporales, no puede superar 1 mensualidad [LAU (Ley 29/1994), Artículo 36. Fianza].
> 
> *Confirme los detalles particulares de su contrato con un abogado especialista o con el servicio de vivienda de su comunidad autónoma.*

*Searches: ['fianza mensualidades pago anticipado alquiler ley 29/1994']*

---

## q10 (single)

**Question:** ¿Puedo subarrendar una habitación de mi piso alquilado?

**Expected:** LAU (Ley 29/1994) · Artículo 8

**Reference answer:** Solo de forma parcial y con consentimiento escrito del arrendador; el precio del subarriendo no puede superar el del arrendamiento.

**Agent answer:**

> Sí, puedes subarrendar una habitación de tu piso alquilado, pero **únicamente de forma parcial y siempre que cuentes con el consentimiento previo y por escrito del arrendador** [LAU (Ley 29/1994), Artículo 8]. 
> 
> Además, debes tener en cuenta las siguientes condiciones que marca la ley:
> * **Límite en el precio:** El precio del subarriendo no puede superar, en ningún caso, el importe que tú pagas por el arrendamiento [LAU (Ley 29/1994), Artículo 8].
> * **Extinción:** El derecho del subarrendatario se extinguirá automáticamente cuando lo haga tu propio contrato como arrendatario [LAU (Ley 29/1994), Artículo 8].
> 
> *Para un caso concreto, te sugerimos confirmarlo con un abogado o con el organismo de vivienda de tu comunidad autónoma.*

*Searches: ['subarriendo parcial vivienda LAU']*

---

## q11 (single)

**Question:** Si el inquilino fallece, ¿quién puede quedarse con el contrato de alquiler?

**Expected:** LAU (Ley 29/1994) · Artículo 16

**Reference answer:** El cónyuge conviviente, la pareja con dos años de convivencia (o hijos en común), descendientes, ascendientes y hermanos convivientes, y ciertos parientes con discapacidad; debe notificarse por escrito en tres meses.

**Agent answer:**

> En caso de fallecimiento del inquilino de una vivienda, pueden subrogarse en el contrato de alquiler (quedarse con él), en un orden de preferencia determinado, las siguientes personas que hayan convivido con él:
> 
> 1. **El cónyuge** que conviviera con él en el momento del fallecimiento [LAU (Ley 29/1994), Artículo 16].
> 2. **La pareja de hecho** que hubiera convivido de forma permanente en análoga relación de afectividad durante al menos los dos años anteriores al fallecimiento, salvo que tengan descendencia en común (en cuyo basta la mera convivencia) [LAU (Ley 29/1994), Artículo 16].
> 3. **Los descendientes** (hijos, etc.) que estuvieran sujetos a su patria potestad o tutela, o hubiesen convivido habitualmente con él durante los dos años precedentes [LAU (Ley 29/1994), Artículo 16].
> 4. **Los ascendientes** (padres, etc.) que hubieran convivido habitualmente con él durante los dos años precedentes [LAU (Ley 29/1994), Artículo 16].
> 5. **Los hermanos** que hubieran convivido habitualmente con él durante los dos años precedentes [LAU (Ley 29/1994), Artículo 16].
> 6. **Personas con minusvalía igual o superior al 65%** con parentesco hasta el tercer grado colateral que hayan convivido con el inquilino durante los dos años anteriores [LAU (Ley 29/1994), Artículo 16].
> 
> **Condiciones y plazos importantes:**
> * **Extinción si no hay nadie o no se notifica:** Si no existe ninguna de estas personas o ninguna cumple los requisitos, el contrato se extingue [LAU (Ley 29/1994), Artículo 16]. Además, la subrogación debe notificarse por escrito al arrendador en un plazo máximo de **tres meses** desde el fallecimiento, adjuntando el certificado de defunción y la acreditación de los requisitos [LAU (Ley 29/1994), Artículo 16].
> * **Excepción por duración o pacto:** En contratos de duración inicial superior a 5 años (o 7 si el arrendador es persona jurídica), las partes pueden pactar que no haya derecho de subrogación transcurridos esos primeros 5 o 7 años. No obstante, **este pacto de renuncia no es válido** si las personas con derecho a subrogarse se encuentran en situación de especial vulnerabilidad (menores de edad, personas con discapacidad o mayores de 65 años) [LAU (Ley 29/1994), Artículo 16].
> 
> *Se recomienda confirmar los detalles del caso con un abogado o con el servicio de vivienda de la comunidad autónoma.*

*Searches: [None, 'subrogacion por fallecimiento del arrendatario LAU articulo 16']*

---

## q12 (single)

**Question:** El propietario quiere hacer obras de mejora en el piso. ¿Con cuánta antelación tiene que avisarme?

**Expected:** LAU (Ley 29/1994) · Artículo 22

**Reference answer:** Por escrito, al menos con tres meses de antelación, indicando naturaleza, comienzo, duración y coste; el inquilino puede desistir en el mes siguiente.

**Agent answer:**

> El propietario debe notificarlo por escrito al arrendatario **al menos con tres meses de antelación**, especificando la naturaleza, el comienzo, la duración y el coste previsible de las obras [LAU (Ley 29/1994), Artículo 22. Obras de mejora].
> 
> Además:
> * **Derecho a desistir:** Durante el plazo de un mes desde esa notificación, el inquilino puede desistir del contrato (extinguiéndose en dos meses, sin que puedan empezar las obras en ese tiempo), salvo que las obras no afecten o afecten de modo irrelevante a la vivienda [LAU (Ley 29/1994), Artículo 22. Obras de mejora].
> * **Reducción de renta e indemnización:** Si soporta las obras, el arrendatario tiene derecho a una reducción de la renta proporcional a la parte de la vivienda de la que se vea privado, así como a que le indemnicen los gastos que las obras le obliguen a efectuar [LAU (Ley 29/1994), Artículo 22. Obras de mejora].
> 
> *Para un caso concreto, se recomienda confirmarlo con un abogado o con el servicio de vivienda de su comunidad autónoma.*

*Searches: ['obras mejora antelacion notificacion arrendatario']*

---

## q13 (single)

**Question:** ¿Puedo tirar un tabique del piso alquilado sin permiso del propietario?

**Expected:** LAU (Ley 29/1994) · Artículo 23

**Reference answer:** No: las obras que modifiquen la configuración de la vivienda requieren consentimiento escrito del arrendador.

**Agent answer:**

> **No, no puedes** tirar un tabique sin permiso [LAU (Ley 29/1994), Artículo 23].
> 
> **Condiciones y consecuencias:**
> * **Consentimiento obligatorio:** Necesitas la autorización expresa y por escrito del propietario para realizar cualquier obra que modifique la configuración de la vivienda [LAU (Ley 29/1994), Artículo 23.1].
> * **Seguridad:** En ningún caso puedes realizar obras que disminuyan la estabilidad o la seguridad de la vivienda [LAU (Ley 29/1994), Artículo 23.1]. Si afectas a la seguridad, el propietario puede exigirte de inmediato que repongas las cosas al estado anterior [LAU (Ley 29/1994), Artículo 23.2].
> * **Consecuencias si lo haces sin permiso:** Al finalizar el contrato, el propietario puede optar por exigir que dejes la vivienda como estaba (a tu costa) o quedarse con la modificación sin tener que pagarte ninguna indemnización, además de poder resolver el contrato [LAU (Ley 29/1994), Artículo 23.2].
> 
> *Para un caso concreto, se recomienda confirmarlo con un abogado o con el organismo de vivienda de tu comunidad autónoma.*

*Searches: ['obras tabique arrendatario consentimiento propietario LAU']*

---

## q14 (single)

**Question:** ¿Cuánto puede durar como máximo un alquiler de temporada (vivienda temporal)?

**Expected:** LAU (Ley 29/1994) · Artículo 9 bis

**Reference answer:** Más de 31 días y, como regla general, no más de 12 meses; si se superan sin causa o se encadenan más de dos contratos, pasa a ser vivienda habitual.

**Agent answer:**

> Como regla general, la duración máxima del alquiler de vivienda temporal es de **doce meses**, debiendo ser superior a treinta y un días y estar motivada por una causa justificada y acreditable de desplazamiento temporal [LAU (Ley 29/1994), Artículo 9 bis].
> 
> Excepciones y límites a tener en cuenta:
> * **Prórroga:** Si se pacta una duración inferior a doce meses y la causa de la temporalidad subsiste al finalizar, el contrato se puede prorrogar mediante acuerdo expreso, sin superar en conjunto esos doce meses como regla general, salvo que la causa persista posteriormente [LAU (Ley 29/1994), Artículo 9 bis].
> * **Conversión en alquiler de vivienda habitual:** Si el contrato supera los doce meses sin justificación, o si se encadenan o suceden más de dos contratos de vivienda temporal de forma consecutiva entre las mismas partes y sobre la misma vivienda, el contrato se considerará automáticamente como un arrendamiento de vivienda habitual, aplicándosele los plazos mínimos y prórrogas de este [LAU (Ley 29/1994), Artículo 9 bis].
> 
> *Para una consulta o conflicto concreto, se recomienda confirmar el caso con un abogado o con el servicio de vivienda de su comunidad autónoma.*

*Searches: [None, 'arrendamiento para uso distinto del de vivienda temporal duracion maximo']*

---

## q15 (single)

**Question:** No firmé contrato por escrito, solo de palabra. ¿Es válido mi alquiler?

**Expected:** LAU (Ley 29/1994) · Artículo 37

**Reference answer:** Sí: el contrato verbal es válido y eficaz, aunque el arrendatario puede exigir su formalización por escrito.

**Agent answer:**

> **Sí, tu alquiler es completamente válido [LAU (Ley 29/1994), Artículo 37].** 
> 
> El hecho de que no exista un documento firmado por escrito no afecta a la validez ni a la eficacia del contrato celebrado de palabra [LAU (Ley 29/1994), Artículo 37].
> 
> * **Derecho a exigir contrato por escrito:** Cualquiera de las partes puede obligar a la otra a formalizar el contrato por escrito en cualquier momento [LAU (Ley 29/1994), Artículo 37].
> * **Obligación para el casero:** Si eres el inquilino, tienes derecho a exigir que el contrato se haga por escrito, y el casero está obligado a ello [LAU (Ley 29/1994), Artículo 37].
> 
> *Para un caso concreto o disputa, se recomienda confirmarlo con un abogado o con el organismo de vivienda de tu comunidad autónoma.*

*Searches: ['contrato verbal arrendamiento vivienda valido LAU']*

---

## q16 (single)

**Question:** ¿Por qué motivos puede el casero resolver el contrato de pleno derecho?

**Expected:** LAU (Ley 29/1994) · Artículo 27

**Reference answer:** Impago de la renta o cantidades asumidas, impago de la fianza, subarriendo o cesión no consentidos, daños dolosos u obras no consentidas, actividades molestas o ilícitas, o dejar de ser vivienda habitual.

**Agent answer:**

> El arrendador puede resolver el contrato de pleno derecho por las siguientes causas de incumplimiento por parte del arrendatario [LAU (Ley 29/1994), Artículo 27]:
> 
> 1. La **falta de pago de la renta** o de cualquiera de las cantidades cuyo pago haya asumido o corresponda al arrendatario [LAU (Ley 29/1994), Artículo 27.2.a].
> 2. La **falta de pago del importe de la fianza** o de su actualización [LAU (Ley 29/1994), Artículo 27.2.b].
> 3. El **subarriendo o la cesión inconsentidos** [LAU (Ley 29/1994), Artículo 27.2.c].
> 4. La realización de **daños causados dolosamente** en la finca o de **obras no consentidas** por el arrendador cuando el consentimiento de éste sea necesario [LAU (Ley 29/1994), Artículo 27.2.d].
> 5. Cuando en la vivienda tengan lugar **actividades molestas, insalubres, nocivas, peligrosas o ilícitas** [LAU (Ley 29/1994), Artículo 27.2.e].
> 6. Cuando la vivienda **deje de estar destinada de forma primordial a satisfacer la necesidad de vivienda** del arrendatario o de quien efectivamente la viniera ocupando legalmente [LAU (Ley 29/1994), Artículo 27.2.f].
> 
> *(Nota: En los arrendamientos para uso distinto del de vivienda, como locales comerciales, también procede la resolución de pleno derecho por cesión o subarriendo incumpliendo el artículo 32) [LAU (Ley 29/1994), Artículo 35].*
> 
> Para un caso concreto, confirme siempre su situación con un abogado o con el servicio de vivienda de su comunidad autónoma.

*Searches: ['resolución de pleno derecho arrendador arrendatario LAU']*

---

## q17 (single)

**Question:** What counts as a 'gran tenedor' (large landlord) under the housing law?

**Expected:** Ley 12/2023 de vivienda · Artículo 3

**Reference answer:** A person or company owning more than 10 urban residential properties or more than 1,500 m² of residential floor area (excluding garages and storage rooms); regions may lower it to 5+ properties in stressed zones.

**Agent answer:**

> As a general rule under Spanish housing law, a *gran tenedor* (large landlord) is any individual or corporate entity that owns **more than 10 residential urban properties** (excluding garages and storage rooms), or a total residential constructed floor area of **more than 1,500 m²** [Ley 12/2023 de vivienda, Artículo 3]. 
> 
> **Key condition and exception:**
> * **Stressed-market areas (*zonas tensionadas*):** The threshold can be lowered in specific regional declarations down to owners of **5 or more** residential properties if justified by the autonomous community [Ley 12/2023 de vivienda, Artículo 3].
> * **Calculation rule:** If a single property title (*finca registral*) comprises a building with multiple residential units, each unit counts as an independent property regardless of whether a horizontal property division is formally registered [Ley 12/2023 de vivienda, Artículo 3].
> * **Proof:** This status must be certified via the Land Registry (*Registro de la Propiedad*) [Ley 12/2023 de vivienda, Artículo 3].
> 
> *For a concrete dispute or legal assessment, confirm with a lawyer or your regional housing office.*

*Searches: ['gran tenedor definicion ley vivienda articulo']*

---

## q18 (single)

**Question:** ¿Cuánto tiempo dura la declaración de una zona de mercado residencial tensionado?

**Expected:** Ley 12/2023 de vivienda · Artículo 18

**Reference answer:** Tres años, prorrogable anualmente si persisten las circunstancias.

**Agent answer:**

> La vigencia de la declaración de una zona de mercado residencial tensionado es de **tres años**, pudiendo **prorrogarse anualmente** siguiendo el mismo procedimiento si subsisten las circunstancias que motivaron dicha declaración y se justifica adecuadamente [Ley 12/2023 de vivienda, Artículo 18].
> 
> *Para cualquier duda concreta sobre su caso, consulte con un abogado o con el servicio de vivienda de su comunidad autónoma.*

*Searches: ['zona de mercado residencial tensionado duracion vigencia prorroga Ley 12 2023']*

---

## q19 (single)

**Question:** Si el piso está en zona tensionada, ¿qué información tiene que darme el propietario antes de firmar?

**Expected:** Ley 12/2023 de vivienda · Artículo 31

**Reference answer:** Que está en zona tensionada, la última renta del contrato de vivienda habitual de los últimos cinco años y el valor del índice de referencia de precios aplicable.

**Agent answer:**

> Cuando una vivienda se encuentra en una zona de mercado residencial tensionado, el propietario (o la persona que intervenga en la intermediación) tiene la obligación de indicarlo y de facilitarle la siguiente información **con anterioridad a la formalización del contrato y por escrito en el propio documento del contrato** [Ley 12/2023 de vivienda, Artículo 31. Información mínima en las operaciones de compra y arrendamiento de vivienda]:
> 
> 1. **La cuantía de la última renta** del contrato de arrendamiento de vivienda habitual que haya estado vigente en los últimos cinco años en esa misma vivienda [Ley 12/2023 de vivienda, Artículo 31].
> 2. **El valor que le corresponda** a la vivienda atendiendo al índice de referencia de precios de alquiler que resulte de aplicación [Ley 12/2023 de vivienda, Artículo 31].
> 
> *Nota: Para casos particulares o disputas concretas, se recomienda contrastar la situación con un abogado o con el servicio de vivienda de su comunidad autónoma.*

*Searches: ['zona tensionada informacion contrato arrendamiento renta anterior ley vivienda', 'información que debe suministrarse arrendatario zona tensionada alquiler ley vivienda transparencia']*

---

## q20 (single)

**Question:** ¿Qué cambia en la prórroga de los contratos de alquiler a partir del 15 de noviembre de 2026?

**Expected:** LAU (Ley 29/1994) · Artículo 10

**Reference answer:** Según la redacción futura (RDL 28/2026), a falta de preaviso el contrato se prorroga tácita y obligatoriamente por plazos de cinco años (siete si el arrendador es persona jurídica), y si el arrendador no prorroga debe indemnizar al inquilino salvo excepciones.

**Agent answer:**

> El corpus no cubre esta pregunta de manera detallada respecto a la norma de esa fecha concreta (ya que los extractos disponibles de la redacción futura del artículo 10 de la LAU mencionan efectos a partir del 15 de noviembre de 2026, pero el corpus no detalla todos los cambios introducidos por dicho Real Decreto-ley más allá de la prórroga tácita y las indemnizaciones).
> 
> *Consulte con un abogado o con el servicio de vivienda de su comunidad autónoma para verificar el texto exacto aplicable.*

*Searches: ['prórroga noviembre 2026 arrendamientos urbanos vivienda']*

---

## q21 (single)

**Question:** ¿Cuánto podía subir como máximo la renta en la actualización anual de 2024?

**Expected:** Ley 12/2023 de vivienda · Disposición final sexta

**Reference answer:** Un 3 % (con gran tenedor, el pacto no podía superar el 3 %; sin gran tenedor, a falta de pacto, tampoco más del 3 %).

**Agent answer:**

> Durante el año 2024, el límite máximo de actualización anual de la renta de los contratos de alquiler de vivienda sujeta a la LAU fue del **3%**, tanto si el arrendador era un gran tenedor como si no lo era, a falta de un nuevo pacto inferior entre las partes [Ley 12/2023 de vivienda, Disposición final sexta].
> 
> *Excepciones y condiciones:*
> * Si no existía un pacto previo entre las partes sobre el mecanismo de actualización, no se aplicaba incremento alguno [LAU (Ley 29/1994), Artículo 18].
> * Si las partes alcanzaban un pacto diferente, este se aplicaba siempre que no superara el límite extraordinario del 3% establecido para todo el año 2024 [Ley 12/2023 de vivienda, Disposición final sexta].
> 
> *Confirme los detalles particulares de su contrato con un abogado o con el servicio de vivienda de su comunidad autónoma.*

*Searches: ['actualizacion renta 2024 limite porcentaje 2 por ciento 3 por ciento indice lau vivienda']*

---

## q22 (single)

**Question:** ¿Se aplica la Ley de Arrendamientos Urbanos a una residencia universitaria asignada por la universidad?

**Expected:** LAU (Ley 29/1994) · Artículo 5

**Reference answer:** No: las viviendas universitarias calificadas como tales y asignadas a alumnos matriculados están excluidas de la LAU.

**Agent answer:**

> No, no se aplica la Ley de Arrendamientos Urbanos (LAU).
> 
> Quedan expresamente excluidas del ámbito de aplicación de la LAU:
> * El uso de las viviendas universitarias que hayan sido calificadas expresamente como tales por la propia Universidad propietaria o responsable.
> * Que sean asignadas a alumnos matriculados, así como al personal docente y de administración y servicios, por razón del vínculo con la Universidad.
> * Su uso se someterá a las normas específicas establecidas por la propia Universidad [LAU (Ley 29/1994), Artículo 5].
> 
> *Nota: Se recomienda confirmar los detalles específicos en la normativa propia de la universidad correspondiente o con un servicio especializado en vivienda.*

*Searches: ['residencia universitaria exclusion LAU arrendamientos urbanos']*

---

## q23 (multi)

**Question:** Si el arrendador es una empresa, ¿cuánto dura como mínimo el contrato y durante cuánto tiempo no se actualiza la fianza?

**Expected:** LAU (Ley 29/1994);LAU (Ley 29/1994) · Artículo 9;Artículo 36

**Reference answer:** Siete años en ambos casos: duración mínima de siete años y la fianza no se actualiza durante los siete primeros años.

**Agent answer:**

> Si el arrendador es una persona jurídica (una empresa):
> 
> * **Duración mínima:** El contrato tiene una duración mínima de **7 años** (prorrogándose obligatoriamente por plazos anuales hasta alcanzar ese plazo si se pactó un periodo inferior), salvo que el inquilino manifieste su voluntad de no renovarlo con al menos 30 días de antelación a la fecha de terminación [LAU (Ley 29/1994), Artículo 9.1].
> * **Actualización de la fianza:** La fianza no estará sujeta a actualización durante los **primeros 7 años** de duración del contrato [LAU (Ley 29/1994), Artículo 36.2].
> 
> *Confirme los detalles particulares de su contrato con un abogado especializado o con el servicio de vivienda de su comunidad autónoma.*

*Searches: ['plazo minimo contrato arrendamiento persona juridica LAU duracion', 'actualizacion fianza LAU articulo 36 fianza alquiler vivienda']*

---

## q24 (multi)

**Question:** ¿Puede un gran tenedor fijar libremente la renta de un nuevo contrato en zona tensionada? ¿Quién es gran tenedor?

**Expected:** LAU (Ley 29/1994);Ley 12/2023 de vivienda · Artículo 17;Artículo 3

**Reference answer:** No: la renta no puede superar el límite del sistema de índices de referencia; gran tenedor es quien tiene más de 10 inmuebles residenciales o más de 1.500 m² (o 5+ si la comunidad lo fija).

**Agent answer:**

> **No**, un gran tenedor no puede fijar libremente la renta de un nuevo contrato si la vivienda se encuentra en una zona de mercado residencial tensionado [Ley 12/2023 de vivienda, Disposición final primera; LAU (Ley 29/1994), Artículo 17.7]. 
> 
> En este caso, la renta pactada al inicio del nuevo contrato **no podrá exceder del límite máximo del precio aplicable conforme al sistema de índices de precios de referencia**, y tampoco se pueden repercutir al arrendatario nuevos gastos o cuotas que superen dicho límite [Ley 12/2023 de vivienda, Disposición final primera; LAU (Ley 29/1994), Artículo 17.7].
> 
> ### ¿Quién es gran tenedor?
> Según la Ley 12/2023, es la **persona física o jurídica titular de más de diez inmuebles urbanos de uso residencial** (o una superficie construida de más de **1.500 m² de uso residencial**, excluyendo en todo caso garajes y trasteros) [Ley 12/2023 de vivienda, Artículo 3.k]. 
> 
> Además, esta definición general puede ser particularizada en la declaración de la zona de mercado residencial tensionado para incluir a los titulares de **cinco o más inmuebles urbanos de uso residencial** ubicados en dicho ámbito, si así lo motiva la comunidad autónoma en su memoria justificativa [Ley 12/2023 de vivienda, Artículo 3.k]. La condición debe acreditarse mediante certificación del Registro de la Propiedad [Ley 12/2023 de vivienda, Artículo 3.k].
> 
> *Confirme los detalles particulares de su contrato y zona con un abogado o con el servicio de vivienda de su comunidad autónoma.*

*Searches: ['gran tenedor zona tensionada renta contrato alquiler Ley 12 2023', 'gran tenedor definicion articulo 3 Ley 12 2023']*

---

## q25 (multi)

**Question:** Si me voy del piso a los 8 meses, ¿con cuánto preaviso, y desde cuándo genera intereses la fianza si no me la devuelven?

**Expected:** LAU (Ley 29/1994);LAU (Ley 29/1994) · Artículo 11;Artículo 36

**Reference answer:** Puede desistir con 30 días de preaviso (ya pasaron seis meses); la fianza no devuelta devenga el interés legal un mes después de entregar las llaves.

**Agent answer:**

> Para desistir del contrato de vivienda a los 8 meses, debes comunicárselo al arrendador con un **preaviso mínimo de treinta días** [LAU (Ley 29/1994), Artículo 11]. Como el desistimiento solo se puede ejercer una vez que han transcurrido al menos seis meses desde la firma, a los 8 meses estás en plenas condiciones legales de hacerlo sin generar derecho de indemnización para el arrendador (salvo que el contrato prevea expresamente alguna penalización por desistimiento anticipado, si así se pactó) [LAU (Ley 29/1994), Artículo 11].
> 
> En cuanto a la fianza, si no te la devuelven, **empieza a devengar el interés legal transcurrido un mes desde la entrega de las llaves** sin que se te haya hecho efectiva la restitución [LAU (Ley 29/1994), Artículo 36].
> 
> *Nota: Para un conflicto concreto, confirma los detalles de tu contrato con un abogado o con el servicio de vivienda de tu comunidad autónoma.*

*Searches: ['arrendatario desistimiento plazo preaviso meses LAU', 'fianza intereses devolucion plazo LAU Artículo 36']*

---

## q26 (multi)

**Question:** ¿Cuánto dura una zona tensionada y qué prórroga extraordinaria puede pedir un inquilino de esa zona al acabar su contrato?

**Expected:** Ley 12/2023 de vivienda;LAU (Ley 29/1994) · Artículo 18;Artículo 10

**Reference answer:** La declaración dura tres años (prorrogable anualmente); el inquilino puede pedir una prórroga extraordinaria por plazos anuales de hasta tres años, que el arrendador debe aceptar salvo excepciones.

**Agent answer:**

> La vigencia de la declaración de una zona de mercado residencial tensionado es de **tres años**, pudiendo prorrogarse anualmente siguiendo el mismo procedimiento si subsisten las circunstancias que la motivaron [Ley 12/2023 de vivienda, Artículo 18].
> 
> Al finalizar el contrato o sus prórrogas dentro de una zona tensionada, el inquilino puede pedir una **prórroga extraordinaria por plazos anuales hasta un máximo de tres años**, manteniendo las mismas condiciones del contrato en vigor [LAU (Ley 29/1994), Artículo 10.3].
> 
> **Excepciones:** El arrendador solo puede rechazar esta prórroga obligatoria si:
> * Se ha pactado otro acuerdo entre las partes.
> * Se ha firmado un nuevo contrato con las limitaciones de renta que correspondan.
> * El arrendador ha comunicado debidamente la necesidad de ocupar la vivienda para destinarla a vivienda permanente para sí mismo, sus familiares en primer grado (consanguinidad o adopción) o para su cónyuge en casos de sentencia firme de separación, divorcio o nulidad matrimonial [LAU (Ley 29/1994), Artículo 10.3].
> 
> *Confirme siempre su caso particular con un abogado o con el servicio de vivienda de su comunidad autónoma.*

*Searches: ['declaracion zona tensionada duracion prorroga extraordinaria inquilino']*

---

## q27 (multi)

**Question:** Si el propietario vende el piso, ¿el comprador tiene que respetar mi contrato y tengo derecho a comprarlo yo primero?

**Expected:** LAU (Ley 29/1994);LAU (Ley 29/1994) · Artículo 14;Artículo 25

**Reference answer:** Sí: el adquirente se subroga al menos durante los cinco (siete) primeros años; y el inquilino tiene derecho de tanteo en 30 días naturales desde la notificación y, si no se notifica, de retracto.

**Agent answer:**

> Sí, por norma general **el comprador debe respetar tu contrato**, y **tienes derecho de adquisición preferente** (tanteo y retracto) para comprar la vivienda antes que nadie [LAU (Ley 29/1994), Artículo 14, Artículo 25].
> 
> ### 1. ¿Tiene el comprador que respetar tu contrato?
> * **Durante los primeros 5 o 7 años:** El comprador queda subrogado en los derechos y obligaciones del propietario anterior durante los primeros **5 años** de vigencia del contrato (o **7 años** si el anterior propietario era una persona jurídica), incluso aunque esté inscrito o cumpla los requisitos de protección de terceros de la Ley Hipotecaria [LAU (Ley 29/1994), Artículo 14].
> * **Si el contrato es de mayor duración:** Si pactasteis una duración superior, el comprador deberá respetarla por todo el plazo acordado, salvo que cumpla ciertos requisitos legales específicos de buena fe registral (en cuyo caso el contrato se acortaría a esos 5 o 7 años, generando una indemnización al inquilino) [LAU (Ley 29/1994), Artículo 14].
> * **Pacto de extinción:** Salvo que en el contrato se incluyera expresamente una cláusula que estipule que la venta de la vivienda extingue el arrendamiento (lo que acortaría el plazo a esos 5 o 7 años máximos de protección) [LAU (Ley 29/1994), Artículo 14].
> 
> ### 2. ¿Tienes derecho a comprarlo tú primero?
> Sí. Tienes **derecho de adquisición preferente**, que incluye dos vías [LAU (Ley 29/1994), Artículo 25]:
> * **Derecho de tanteo:** El propietario debe notificarte de forma fehaciente su decisión de vender, el precio y las condiciones esenciales. Tienes un plazo de **30 días naturales** desde esa notificación para ejercer tu derecho y comprar la vivienda en las mismas condiciones [LAU (Ley 29/1994), Artículo 25].
> * **Derecho de retracto:** Si no se te hizo la notificación, si se omitieron datos obligatorios en ella (como el precio) o si el precio final de la venta fue inferior o las condiciones más ventajosas, puedes ejercitar el retracto [LAU (Ley 29/1994), Artículo 25]. Esto te permite adquirir la vivienda pagando el precio de la compraventa en un plazo de **30 días naturales** desde que el nuevo comprador te notifique fehacientemente cómo se efectuó la operación (entregándote copia de la escritura) [LAU (Ley 29/1994), Artículo 25].
> * *Nota:* Este derecho no se puede renunciar contractualmente, ya que la ley prohíbe pactar la renuncia del inquilino al tanteo y retracto [LAU (Ley 29/1994), Artículo 25].
> 
> *Confirme los detalles particulares de su situación con un abogado o con el servicio de vivienda de su comunidad autónoma.*

*Searches: ['venta de vivienda arrendada comprador derecho adquisicion preferente LAU']*

---

## q28 (multi)

**Question:** ¿Quién paga la reparación de una caldera estropeada y quién paga los honorarios de la inmobiliaria?

**Expected:** LAU (Ley 29/1994);LAU (Ley 29/1994) · Artículo 21;Artículo 20

**Reference answer:** La reparación necesaria para la habitabilidad la paga el arrendador (salvo deterioro imputable al inquilino o pequeñas reparaciones de uso); los gastos de gestión inmobiliaria y formalización son del arrendador.

**Agent answer:**

> * **Reparación de la caldera:** La paga por regla general el **arrendador** (propietario), ya que está obligado a realizar las reparaciones necesarias para conservar la vivienda en condiciones de habitabilidad [LAU (Ley 29/1994), Artículo 21].
>   * *Excepción:* Si la avería se debe a un mal uso imputable al inquilino o a una pequeña reparación derivada del desgaste diario ordinario, correrá a cargo del **arrendatario** [LAU (Ley 29/1994), Artículo 21].
> 
> * **Honorarios de la inmobiliaria:** Los paga siempre el **arrendador** (propietario) [LAU (Ley 29/1994), Artículo 20]. La ley prohíbe repercutir los gastos de gestión inmobiliaria y de formalización del contrato al inquilino, bajo ningún concepto o denominación [LAU (Ley 29/1994), Artículo 20].
> 
> *Para conflictos concretos, se recomienda confirmarlo con un abogado o con el servicio de vivienda de su comunidad autónoma.*

*Searches: ['reparacion caldera conservacion vivienda arrendamiento', 'honorarios inmobiliaria gastos gestion inmobiliaria arrendador arrendatario ley vivienda']*

---

## q29 (multi)

**Question:** ¿Qué sistema creó el RDL 7/2019 para conocer el precio del alquiler y cómo afecta hoy a la renta de grandes tenedores en zonas tensionadas?

**Expected:** RDL 7/2019;LAU (Ley 29/1994) · Disposición adicional segunda;Artículo 17

**Reference answer:** Creó el sistema estatal de índices de referencia del precio del alquiler; hoy la renta inicial de un gran tenedor en zona tensionada no puede superar el límite de ese sistema de índices.

**Agent answer:**

> El Real Decreto-Ley 7/2019 creó el **sistema estatal de índices de referencia del precio del alquiler de vivienda**, un sistema basado en datos fiscales, catastrales, registrales y de depósitos de fianza para ofrecer anualmente valores medios de la renta mensual por metro cuadrado según secciones censales, barrios y municipios [RDL 7/2019, Disposición adicional segunda].
> 
> En cuanto a su aplicación actual, en los contratos de arrendamiento situados en **zonas de mercado residencial tensionado** en los que el arrendador sea un **gran tenedor**, la renta inicial pactada al inicio del nuevo contrato **no puede exceder el límite máximo del precio aplicable conforme a dicho sistema de índices de referencia** (además de aplicarse los límites generales respecto al contrato anterior, si los hubiera) [Ley 12/2023 de vivienda, Disposición final primera].
> 
> *Nota: Para casos particulares o conflictos sobre la aplicación de estos límites, se recomienda confirmar la situación con un abogado o con el servicio de vivienda de la comunidad autónoma.*

*Searches: ['RDL 7 2019 sistema precio alquiler referencia indice', 'Ley 12 2023 renta grandes tenedores zonas tensionadas indice referencia']*

---

## q30 (unanswerable)

**Question:** ¿Cuál es el valor del IRAV publicado para octubre de 2026?

**Expected:** — · —

**Reference answer:** El corpus no da valores publicados del IRAV; solo regula que la actualización no puede superarlo.

**Agent answer:**

> El corpus no cubre esta pregunta (no contiene los valores mensuales publicados del Índice de Referencia para la Actualización Anual de los Contratos de Arrendamiento de Vivienda, IRAV). 
> 
> El corpus únicamente recoge la previsión legal de su existencia y su utilización como límite o referencia para la actualización anual de la renta [LAU (Ley 29/1994), Artículo 18. Actualización de la renta] y para limitar el incremento en contratos de arrendamiento de vivienda temporal sucesivos [LAU (Ley 29/1994), Artículo 17. Determinación de la renta], pero no los datos estadísticos publicados por el Instituto Nacional de Estadística.
> 
> *Para un caso concreto, se recomienda consultar directamente con el Instituto Nacional de Estadística (INE), un abogado especialista o la oficina de vivienda de su comunidad autónoma.*

*Searches: ['IRAV octubre 2026']*

---

## q31 (unanswerable)

**Question:** ¿Qué barrios de Barcelona están declarados zona de mercado residencial tensionado?

**Expected:** — · —

**Reference answer:** El corpus regula cómo se declaran las zonas tensionadas pero no incluye ninguna declaración concreta.

**Agent answer:**

> El corpus no cubre esta pregunta (no contiene la relación de barrios específicos de Barcelona declarados zona de mercado residencial tensionado, ya que el texto legal estatal solo regula los requisitos y el procedimiento general para dicha declaración) [Ley 12/2023 de vivienda, Artículo 18]. 
> 
> *Para un caso concreto, se recomienda consultar con un abogado o con la oficina de vivienda de la administración autonómica o local.*

*Searches: ['zona de mercado residencial tensionado Barcelona barrios']*

---

## q32 (unanswerable)

**Question:** ¿Cuánto dinero da el Bono Alquiler Joven y quién puede pedirlo?

**Expected:** — · —

**Reference answer:** El corpus no regula el Bono Alquiler Joven.

**Agent answer:**

> El corpus no cubre esta pregunta. Las leyes de arrendamientos urbanos y vivienda indexadas (LAU, Ley 12/2023 y RDL 7/2019) no contienen los detalles, cuantías ni requisitos específicos del Bono Alquiler Joven, ya que esta ayuda se regula mediante reales decretos y convocatorias de las comunidades autónomas ajenos a los textos legales consolidados del BOE aquí indexados. 
> 
> Para confirmar los importes y requisitos exactos aplicables en su comunidad autónoma, se recomienda consultarlo directamente con el organismo de vivienda de la región o con un profesional especializado.

*Searches: ['Bono Alquiler Joven cuantia requisitos', '"Bono Alquiler Joven"']*

---

## q33 (unanswerable)

**Question:** ¿Cuánto tarda de media un juicio de desahucio por impago en Madrid?

**Expected:** — · —

**Reference answer:** El corpus no contiene datos sobre la duración de los procedimientos judiciales.

**Agent answer:**

> El corpus no cubre esta pregunta (no contiene datos estadísticos sobre la duración media de los juicios de desahucio en Madrid). 
> 
> La normativa procesal aplicable sí regula los plazos de los trámites esenciales (como el requerimiento de pago de diez días y los trámites de suspensión por vulnerabilidad de hasta dos o cuatro meses según el demandante) [RDL 7/2019, Artículo tercero; Ley 12/2023 de vivienda, Disposición final quinta], pero no especifica la duración total acumulada en la práctica judicial.
> 
> *Confirme los plazos estimados actuales con un abogado o con los servicios de información de la vivienda de la Comunidad de Madrid.*

*Searches: ['juicio de desahucio por impago plazo duración Madrid', 'duración media juicio desahucio Madrid LEC']*

---

## q34 (unanswerable)

**Question:** ¿Puede votar en la junta de propietarios un propietario que debe cuotas de comunidad?

**Expected:** — · —

**Reference answer:** Las leyes indexadas no lo regulan (está en la Ley de Propiedad Horizontal, art. 15.2: puede asistir y deliberar pero no votar, salvo que haya impugnado judicialmente la deuda o consignado la suma).

**Agent answer:**

> El corpus no cubre esta pregunta (la regulación sobre la junta de propietarios y la suspensión del derecho de voto por deudas se encuentra en la Ley sobre Propiedad Horizontal, que no está indexada en el corpus; este solo incluye la LAU, la Ley de Vivienda y las reformas del RDL 7/2019 relativas al alquiler y determinados aspectos accesorios). 
> 
> *Confirme este extremo con un abogado o con la normativa aplicable en materia de propiedad horizontal.*

*Searches: ['propietario deudas voto junta de propietarios', 'derecho a voto propietarios morosos ley propiedad horizontal asistencia voto cuotas']*

---

## q35 (unanswerable)

**Question:** ¿Cuál es el tipo de interés legal del dinero en 2026?

**Expected:** — · —

**Reference answer:** El corpus remite al interés legal (p. ej. para la fianza) pero no fija su valor.

**Agent answer:**

> El corpus no cubre esta pregunta. Las leyes de arrendamientos urbanos (como la LAU o la Ley 12/2023) solo mencionan que el interés legal del dinero se aplica a la devolución de la fianza si transcurre más de un mes desde la entrega de llaves sin haberse restituido [LAU (Ley 29/1994), Artículo 36. Fianza], pero no recogen la cifra concreta del tipo de interés legal del dinero para cada año.

*Searches: ['interes legal del dinero 2026']*
