# Casos en que saltó el validador de citas

Capturados el 2026-11-23 con el harness real (`agent.open_agent`, `add_document` denegado), modelo del agente gemini-3.5-flash-lite.
Se probaron 7 preguntas pensadas para provocarlo; saltó en 2. Las 4 que pedían artículos fuera del corpus (Ley del IVA art. 164, LGSS art. 214,
Estatuto de los Trabajadores art. 1) o varios artículos a la vez no lo activaron: el agente rechazó o citó solo lo recuperado.
Tampoco saltó al pedir el formato [Ley 20/2007, art. X]: el agente mantuvo [LETA, Artículo 38 ter].

## Caso 1

**Pregunta:** ¿Qué requisitos hay para la tarifa plana? Cita cada requisito con su apartado exacto, por ejemplo [LETA, Artículo 38 ter, apartado 1].

1. **Llamada** `search({"query": "tarifa plana reduccion cuotas inicio de actividad autonomia leta seguridad social"})`
2. **Resultado** de `search`: [LETA, Artículo 38 ter], [LETA, Artículo 38], [LETA, Artículo 38 quinquies]
3. **Respuesta del modelo**:

   > Según el texto consolidado a 2 de septiembre de 2026 de la Ley 20/2007 (Estatuto del trabajo autónomo), los requisitos y condiciones generales aplicables a la cuota reducida por inicio de actividad son los siguientes:
   >
   > * **Alta inicial o inactividad previa:** El trabajador debe causar alta inicial o no haber estado en situación de alta en los dos años inmediatamente anteriores, a contar desde la fecha de efectos del alta, en el Régimen Especial de la Seguridad Social de los Trabajadores por Cuenta Propia o Autónomos [LETA, Artículo 38 ter].
   > * **Solicitud inicial y requisitos para el segundo año:** 
   >   * La aplicación de las reducciones debe ser solicitada expresamente por los trabajadores en el momento de su alta en el régimen especial [LETA, Artículo 38 ter, apartado 3].
   >   * Para poder aplicar la cuota reducida durante los segundos doce meses naturales completos, los rendimientos económicos netos anuales del trabajador deben ser inferiores al salario mínimo interprofesional anual que corresponda a ese periodo, debiendo acompañarse la solicitud de una declaración relativa a que se prevé obtener dichos rendimientos inferiores [LETA, Artículo 38 ter, apartado 2] [LETA, Artículo 38 ter, apartado 3].
   > * **Exclusiones subjetivas:** Las reducciones en la cotización no resultarán aplicables a los familiares de trabajadores autónomos por consanguinidad o afinidad hasta el segundo grado inclusive y, en su caso, por adopción, que se incorporen al régimen especial o al grupo primero de cotización del Régimen Especial de la Seguridad Social de los Trabajadores del Mar, ni a los miembros de institutos de vida consagrada de la Iglesia Católica incluidos en el primero de dichos regímenes [LETA, Artículo 38 ter, apartado 11].
   >
   > Texto consolidado del BOE de carácter informativo; no tiene validez jurídica. Para efectos legales, consulte la publicación oficial.

4. **Validador** (mensaje añadido por el harness):

   > Revisión automática de citas: [LETA, Artículo 38 ter, apartado 3] no aparece en los resultados de search; [LETA, Artículo 38 ter, apartado 2] no aparece en los resultados de search; [LETA, Artículo 38 ter, apartado 11] no aparece en los resultados de search. Reescribe la respuesta citando solo fragmentos que devolvió search, copiando [FUENTE, Ubicación] tal cual. Quita lo que no puedas respaldar; si no queda nada, responde con la frase de rechazo.

5. **Llamada** `search({"query": "tarifa plana reduccion cuotas inicio de actividad leta articulo 38 ter"})`
6. **Resultado** de `search`: [LETA, Artículo 38 ter], [LETA, Artículo 38 quinquies], [LETA, Artículo 38 bis]
7. **Respuesta del modelo**:

   > Según el texto consolidado a 2 de septiembre de 2026 de la Ley 20/2007 (Estatuto del trabajo autónomo), para aplicar las reducciones en la cotización por inicio de actividad se deben cumplir los siguientes requisitos generales y condiciones:
   >
   > * **Alta inicial o inactividad previa:** La cotización se aplicará a los trabajadores por cuenta propia o autónomos que causen alta inicial o que no hubieran estado en situación de alta en los dos años inmediatamente anteriores, a contar desde la fecha de efectos del alta, en el Régimen Especial de la Seguridad Social de los Trabajadores por Cuenta Propia o Autónomos [LETA, Artículo 38 ter].
   > * **Rendimientos en el segundo año:** Para poder aplicar la cuota reducida durante los segundos doce meses naturales completos, los rendimientos económicos netos anuales del trabajador deben ser inferiores al salario mínimo interprofesional anual que corresponda a dicho periodo [LETA, Artículo 38 ter].
   > * **Solicitud y plazos:** La aplicación de las reducciones debe ser solicitada por los trabajadores en el momento de su alta en el régimen especial y, en su caso, antes del inicio del período del segundo año, debiendo acompañarse de una declaración relativa a que los rendimientos económicos netos previstos serán inferiores al salario mínimo interprofesional [LETA, Artículo 38 ter].
   > * **Exclusión de familiares:** Las reducciones en la cotización no resultarán aplicables a los familiares de trabajadores autónomos por consanguinidad o afinidad hasta el segundo grado inclusive y, en su caso, por adopción, que se incorporen al régimen especial o al grupo primero de cotización del Régimen Especial de la Seguridad Social de los Trabajadores del Mar, ni a los miembros de institutos de vida consagrada de la Iglesia Católica [LETA, Artículo 38 ter].
   >
   > Texto consolidado del BOE de carácter informativo; no tiene validez jurídica. Para efectos legales, consulte la publicación oficial.


## Caso 2

**Pregunta:** Hola, ¿qué puedes hacer por mí?

1. **Respuesta del modelo**:

   > Hola. Puedo ayudarte a resolver dudas sobre tus derechos y obligaciones si vas a darte de alta como autónomo en España o acabas de hacerlo, basándome exclusivamente en la legislación oficial vigente (como el Estatuto del Trabajo Autónomo, la Ley General de la Seguridad Social, el Reglamento de Facturación y el Reglamento de Gestión e Inspección Tributaria). 
   >
   > Puedes preguntarme sobre cuestiones relativas al alta, cotización, facturación y otras normativas aplicables a autónomos. 
   >
   > Texto consolidado del BOE de carácter informativo; no tiene validez jurídica. Para efectos legales, consulte la publicación oficial.

2. **Validador** (mensaje añadido por el harness):

   > Revisión automática de citas: la respuesta no cita ningún fragmento y no es la frase de rechazo. Reescribe la respuesta citando solo fragmentos que devolvió search, copiando [FUENTE, Ubicación] tal cual. Quita lo que no puedas respaldar; si no queda nada, responde con la frase de rechazo.

3. **Respuesta del modelo**:

   > No se ha encontrado contenido relacionado a tu pregunta en los documentos a los que tengo acceso. Consulte con un técnico especialista.

