# Citation guard demo

Question q07: ¿Cuánto tiempo tiene la CNMV para autorizar una OPA?

Passages search returned in this run: [CNMV-QA-OPAS, Pregunta 11], [CNMV-QA-OPAS, Pregunta 12], [CNMV-QA-OPAS, Pregunta 13], [RD1066-2007, Artículo 21]

## Real answer

Guard fired: **False**

Answer the user sees:

> El plazo es de **veinte días hábiles** a partir de la recepción de la solicitud [RD1066-2007, Artículo 21]. 
> 
> * **Cómputo:** Si se presentan documentos complementarios con posterioridad a la solicitud o si se requiere información o documentación adicional, el plazo se computa desde la fecha en que se registren dichos documentos o informaciones [RD1066-2007, Artículo 21].

## One citation changed to [RD1066-2007, Artículo 22]

Guard fired: **True** (cita pasajes que la búsqueda no devolvió: [RD1066-2007, Artículo 22])

Answer the user sees:

> El corpus no cubre esta pregunta con citas verificables: la respuesta generada cita pasajes que la búsqueda no devolvió: [RD1066-2007, Artículo 22]. Revisa la normativa directamente o consulta con el abogado del deal.

## Citations removed

Guard fired: **True** (no incluye ninguna cita)

Answer the user sees:

> El corpus no cubre esta pregunta con citas verificables: la respuesta generada no incluye ninguna cita. Revisa la normativa directamente o consulta con el abogado del deal.
