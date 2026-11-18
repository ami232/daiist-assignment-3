# Adding a document: before and after

**Question (q34, unanswerable in the initial corpus):** ¿Puede votar en la junta de propietarios un propietario que debe cuotas de comunidad?

**Document added:** LPH (Ley 49/1960) — `corpus/BOE-A-1960-10906.xml`
(https://www.boe.es/buscar/act.php?id=BOE-A-1960-10906), through the same pipeline as `add_document`.

- First add: 54 chunks, 54 embedded (22s incl. second call).
- Adding it again: 0 embedded, 0 removed — already indexed and unchanged, so nothing is re-embedded.

## Before

El corpus no cubre esta pregunta (la regulación sobre la junta de propietarios y la suspensión del derecho de voto por deudas se encuentra en la Ley sobre Propiedad Horizontal, que no está indexada en el corpus; este solo incluye la LAU, la Ley de Vivienda y las reformas del RDL 7/2019 relativas al alquiler y determinados aspectos accesorios). 

*Confirme este extremo con un abogado o con la normativa aplicable en materia de propiedad horizontal.*

*Tool calls: 2; citation guard: ok*

## After

**No** si las deudas están vencidas al iniciarse la junta [LPH (Ley 49/1960), Artículo quince].

Condiciones y excepciones:
* **Excepción:** Sí puede votar si ha impugnado judicialmente dichas deudas o si ha procedido a su consignación judicial o notarial [LPH (Ley 49/1960), Artículo quince].
* **Participación:** Aunque no tenga derecho a voto, puede asistir a la junta y participar en las deliberaciones [LPH (Ley 49/1960), Artículo quince]. Su persona y cuota no se computarán para calcular las mayorías necesarias para los acuerdos [LPH (Ley 49/1960), Artículo quince].

*Para un conflicto concreto, confirme los detalles con un abogado o profesional especializado en la Ley de Propiedad Horizontal.*

*Tool calls: 1; citation guard: ok; valid citations: ['LPH (Ley 49/1960), Artículo quince', 'LPH (Ley 49/1960), Artículo quince', 'LPH (Ley 49/1960), Artículo quince', 'LPH (Ley 49/1960), Artículo quince']*
