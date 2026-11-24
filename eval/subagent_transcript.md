# Subagent transcript (Claude Code)

Subagent: `.claude/agents/corpus-researcher.md` (tools: `mcp__corpus__search` only), invoked from Claude Code in this repository; 2 search calls, ~9.7k tokens, 13.5 s.

**User:** Mi casero quiere subirme el alquiler este año aunque el contrato no dice nada de actualizaciones. ¿Puede hacerlo? Responde citando los artículos.

**corpus-researcher:**

No. Si el contrato no incluye ninguna cláusula de actualización, el casero no puede subir la renta cada año.

- **No hay subida sin un pacto expreso.** Durante el contrato, la renta solo puede actualizarse en la fecha en que se cumple cada año de vigencia, y "en los términos pactados por las partes". La ley dice: "En defecto de pacto expreso, no se aplicará actualización de rentas a los contratos" [LAU (Ley 29/1994), Artículo 18.1]. Esta regla viene de la reforma del RDL 7/2019 [RDL 7/2019, Artículo primero, apartado Nueve].
- **Si hubiera pacto, la subida tiene un tope.** Cuando la cláusula no indica qué índice se usa, se aplica el IRAV. Aunque lo indique, la subida anual nunca puede superar la variación del IRAV [LAU (Ley 29/1994), Artículo 18.1; Disposición adicional undécima].
- **Hace falta avisar por escrito.** La renta actualizada solo se puede cobrar a partir del mes siguiente a que una parte se lo notifique a la otra por escrito, indicando el porcentaje aplicado. Basta una nota en el recibo del mes anterior [LAU (Ley 29/1994), Artículo 18.2].
- **Hay una excepción: las obras de mejora.** Si el casero hace obras de mejora después de los primeros cinco años de contrato (siete si el casero es una empresa o persona jurídica), puede subir la renta, salvo que el contrato diga lo contrario. La subida se calcula con el interés legal del dinero más tres puntos sobre lo invertido. Tiene un máximo del 20 % de la renta vigente y debe notificarse por escrito con el desglose de costes [RDL 7/2019, Artículo primero, apartado Diez, que da nueva redacción al art. 19 LAU]. Este texto procede de la versión del RDL que modifica la LAU; no he recuperado el artículo 19 en la versión consolidada.

URLs: https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003 ; https://www.boe.es/buscar/act.php?id=BOE-A-2019-3108

> Observation: for the improvement-works exception the subagent cited the *amending* text in RDL 7/2019 rather than the consolidated LAU Article 19 — the duplicate-text risk of including RDL 7/2019 in the corpus. The content matches LAU art. 19 here, but an amending text can be outdated if the article was changed again later.
