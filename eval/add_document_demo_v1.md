# Demo de add_document

Pregunta q31 antes y después de añadir `corpus/BOE-A-2026-7296.xml` con `add_document`, en una sola sesión del agente (agent.py). Generado por `demo_add_document.py`. **v1: antes de corregir el validador de citas; el paso 2 acaba en la frase de rechazo aunque el documento se añadió.**

## 1. Antes de añadir el documento

**Mensaje:** Actualmente facturo entorno a 600 euros al mes. ¿Qué tramo de cotización me corresponde?

**Herramientas:**

- llamada `search({"query": "cotizacion autonomos ingresos rendimientos netos tramos"})`
- resultado `search`: [LGSS, Artículo 308], [LETA, Artículo 38 ter]

**Respuesta:**

> Las personas trabajadoras autónomas deben cotizar en función de los rendimientos netos anuales que obtengan en el ejercicio de sus actividades [LGSS, Artículo 308]. Para ello, la Ley de Presupuestos Generales del Estado establece anualmente una tabla general y una tabla reducida de bases de cotización divididas en tramos consecutivos de importes de rendimientos netos mensuales, a los que se asigna una base de cotización mínima y máxima [LGSS, Artículo 308]. Los trabajadores deben elegir la base mensual que corresponda según su previsión del promedio mensual de rendimientos netos anuales dentro de dichas tablas [LGSS, Artículo 308].
>
> No se ha encontrado contenido relacionado a tu pregunta en los documentos a los que tengo acceso. Consulte con un técnico especialista.
>
> Texto consolidado del BOE de carácter informativo; no tiene validez jurídica. Para efectos legales, consulte la publicación oficial.

_Citas: [LGSS, Artículo 308] · búsquedas: 1 · tokens: 7054 · 3.72 s_

## 2. Petición de añadir el documento

**Mensaje:** Añade al índice el documento corpus/BOE-A-2026-7296.xml.

**Herramientas:**

- llamada `add_document({"path": "corpus/BOE-A-2026-7296.xml"})`
- resultado `add_document` (success): Añadido: COT2026 (BOE-A-2026-7296, consolidado a 16 de julio de 2026). 8 fragmentos nuevos, 0 omitidos (ya estaban).
- llamada `search({"query": "BOE-A-2026-7296"})`
- resultado `search`: [COT2026, Artículo 18], [COT2026, Artículo 19], [RGAT, Artículo 19], [RGAT, Artículo 20]

**Respuesta:**

> No se ha encontrado contenido relacionado a tu pregunta en los documentos a los que tengo acceso. Consulte con un técnico especialista.
>
> Texto consolidado del BOE de carácter informativo; no tiene validez jurídica. Para efectos legales, consulte la publicación oficial.

_Citas: ninguna · búsquedas: 1 · tokens: 10488 · 78.96 s_

## 3. Después de añadir el documento

**Mensaje:** Actualmente facturo entorno a 600 euros al mes. ¿Qué tramo de cotización me corresponde?

**Herramientas:**

- llamada `search({"query": "tramos cotizacion ingresos autonomos reregimen especial seguridad social"})`
- resultado `search`: [COT2026, Artículo 18], [LGSS, Artículo 308], [LETA, Artículo 38 ter]

**Respuesta:**

> Según el texto consolidado de la normativa a 16 de julio de 2026, los trabajadores autónomos cotizan en función de sus rendimientos netos anuales divididos en tramos mensuales, disponiendo de una tabla general y una tabla reducida de bases de cotización [COT2026, Artículo 18] [LGSS, Artículo 308]. 
>
> Para unos rendimientos netos de 600 euros al mes, al encontrarse en el tramo igual o inferior a 670 euros mensuales, le correspondería el **Tramo 1 de la tabla reducida**, que establece una base mínima de 653,59 euros y una base máxima de 718,94 euros mensuales [COT2026, Artículo 18].
>
> Debe tener en cuenta que la base elegida inicialmente tiene carácter provisional hasta que se realice la regularización definitiva en función de los rendimientos netos anuales comunicados por la Administración tributaria [LGSS, Artículo 308]. Se recomienda confirmar el cálculo y la base aplicable con un profesional especializado.
>
> Texto consolidado del BOE de carácter informativo; no tiene validez jurídica. Para efectos legales, consulte la publicación oficial.

_Citas: [COT2026, Artículo 18], [LGSS, Artículo 308] · búsquedas: 1 · tokens: 7401 · 3.75 s_
