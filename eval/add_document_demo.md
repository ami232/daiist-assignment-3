# Demo de add_document

Pregunta q31 antes y después de añadir `corpus/BOE-A-2026-7296.xml` con `add_document`, en una sola sesión del agente (agent.py). Generado por `demo_add_document.py`.

## 1. Antes de añadir el documento

**Mensaje:** Actualmente facturo entorno a 600 euros al mes. ¿Qué tramo de cotización me corresponde?

**Herramientas:**

- llamada `search({"query": "tramos cotizacion ingresos autonomos seguridad social"})`
- resultado `search`: [LGSS, Artículo 308], [LETA, Artículo 38 ter], [LETA, Artículo 25]

**Respuesta:**

> Las personas trabajadoras autónomas deben cotizar en función de los rendimientos netos anuales obtenidos en el ejercicio de sus actividades económicas, empresariales o profesionales [LGSS, Artículo 308]. Para ello, la Ley de Presupuestos Generales del Estado establece anualmente una tabla general y una tabla reducida de bases de cotización divididas en tramos consecutivos de importes de rendimientos netos mensuales [LGSS, Artículo 308]. Cada trabajador debe elegir la base de cotización mensual que corresponda según su previsión del promedio mensual de sus rendimientos netos anuales [LGSS, Artículo 308].
>
> Dado que los documentos consultados no detallan las cuantías específicas de los tramos ni los importes exactos de las bases asignadas a cada nivel de ingresos, no es posible indicar el tramo exacto que le corresponde para su facturación de 600 euros mensuales. Se recomienda confirmar este cálculo y la tabla aplicable con un profesional especialista.
>
> Texto consolidado del BOE de carácter informativo; no tiene validez jurídica. Para efectos legales, consulte la publicación oficial.

_Citas: [LGSS, Artículo 308] · búsquedas: 1 · tokens: 6635 · 4.1 s_

## 2. Petición de añadir el documento

**Mensaje:** Añade al índice el documento corpus/BOE-A-2026-7296.xml.

**Herramientas:**

- llamada `add_center({"path": "corpus/BOE-A-2026-7296.xml"})`
- resultado `add_center` (error): Error: add_center is not a valid tool, try one of [search, add_document].
- llamada `add_document({"path": "corpus/BOE-A-2026-7296.xml"})`
- resultado `add_document` (success): Añadido: COT2026 (BOE-A-2026-7296, consolidado a 16 de julio de 2026). 8 fragmentos nuevos, 0 omitidos (ya estaban).

**Respuesta:**

> Se ha añadido correctamente al índice el documento `corpus/BOE-A-2026-7296.xml` (COT2026, consolidado a 16 de julio de 2026).

_Citas: ninguna · búsquedas: 0 · tokens: 5373 · 41.39 s_

## 3. Después de añadir el documento

**Mensaje:** Actualmente facturo entorno a 600 euros al mes. ¿Qué tramo de cotización me corresponde?

**Herramientas:**

- llamada `search({"query": "tramos cotizacion ingresos autonomos seguridad social"})`
- resultado `search`: [COT2026, Artículo 18], [LGSS, Artículo 308], [LETA, Artículo 38 ter]

**Respuesta:**

> Según el texto consolidado a 16 de julio de 2026 de la norma de cotización, los trabajadores autónomos cotizan en función de sus rendimientos netos mensuales estimados mediante una tabla general y una tabla reducida [COT2026, Artículo 18] [LGSS, Artículo 308]. 
>
> Para unos rendimientos netos de 600 euros al mes, el tramo aplicable se encuentra en la **tabla reducida**, concretamente:
>
> * **Tramo 1** (rendimientos iguales o inferiores a 670 euros mensuales): con una base mínima de 653,59 euros y una base máxima de 718,94 euros [COT2026, Artículo 18].
> * **Tramo 2** (rendimientos superiores a 670 euros y hasta 900 euros mensuales): con una base mínima de 718,95 euros y una base máxima de 900,00 euros [COT2026, Artículo 18].
>
> Debe elegir la base de cotización mensual que mejor se ajuste a su previsión dentro del tramo que le corresponda según sus rendimientos netos reales [LGSS, Artículo 308]. Tenga en cuenta que posteriormente la Seguridad Social realiza una regularización anual comparando estos datos con los rendimientos netos fiscales declarados.
>
> Se recomienda confirmar el cálculo y la elección del tramo con un profesional especialista, ya que la cotización depende de la cifra exacta de rendimientos netos y de posibles bonificaciones aplicables.
>
> Texto consolidado del BOE de carácter informativo; no tiene validez jurídica. Para efectos legales, consulte la publicación oficial.

_Citas: [COT2026, Artículo 18], [LGSS, Artículo 308] · búsquedas: 1 · tokens: 7474 · 2.36 s_
