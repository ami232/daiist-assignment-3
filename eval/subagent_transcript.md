# Subagent transcript (Claude Code, corpus-researcher)

Run from Claude Code (desktop app), delegating to the `corpus-researcher` subagent, which only has the
`mcp__corpus__search` tool. Date: 2026-11-24.

**User:** cuantos dias aguanta el pollo en la refri antes de tener que congelarlo? y si lo descongelo lo puedo volver a congelar?

**corpus-researcher:**

- **Pollo crudo en la refri:** el pollo o pavo fresco, entero o en piezas, aguanta de 1 a 2 días en el refrigerador a 40 °F (4 °C). En el congelador se conserva 1 año entero o 9 meses en piezas, y esos plazos son solo por calidad, porque congelar a 0 °F (-18 °C) mantiene la comida segura indefinidamente. [fda_storage_chart | p. 4 (part 2)]
- **Volver a congelar:** los documentos de la FDA que tengo no dicen directamente si se puede volver a congelar pollo que ya se descongeló por completo en la refri. Solo dicen que la comida congelada que todavía tiene cristales de hielo o está a 40 °F o menos se puede volver a congelar o cocinar sin riesgo. [fda:refrigerator-thermometers-cold-facts-about-food-safety | Section: In Case of Disaster...; How Long Is Too Long?]
- Si lo descongelas en agua fría o en el microondas, cocínalo de inmediato. Nunca lo descongeles a temperatura ambiente. [fda:safe-food-handling | Section: SEPARATE; COOK; CHILL]
- Tira el pollo si estuvo 2 horas o más a temperatura ambiente (1 hora si hace más de 90 °F), o si no sabes cuánto tiempo estuvo a más de 40 °F. [fda:food-and-water-safety-during-power-outages-and-floods | Section: When the Power Goes Out . . .; Once Power is Restored . . .] [fda:refrigerator-thermometers-cold-facts-about-food-safety | Section: In Case of Disaster...; How Long Is Too Long?]

Citas:
- [fda_storage_chart | p. 4 (part 2)]
- [fda:refrigerator-thermometers-cold-facts-about-food-safety | Section: In Case of Disaster...; How Long Is Too Long?]
- [fda:safe-food-handling | Section: SEPARATE; COOK; CHILL]
- [fda:food-and-water-safety-during-power-outages-and-floods | Section: When the Power Goes Out . . .; Once Power is Restored . . .]

Note: a first attempt failed because Claude Code was still running the old template `server.py`
(started before the real server existed); after reconnecting the `corpus` server in `/mcp`, the
subagent answered as above.
