# Assignment 3 Report

- **Name**: Aitana Damotte Huedo
- **Student ID**: 18654
- **Group**: [BBADBA 5A | BBADBA 5B | PPLEDBA 5A]

## Use case
The user is the bid manager of a Spanish SME that sells managed cybersecurity services (SOC/MDR). They decide which public tenders on PLACSP and TED to bid for.

They use the answers twice:
- **Go/no-go:** solvency thresholds, required certifications (ISO/IEC 27001, ENS) and business classification. This comes before spending days on a proposal.
- **Preparing the bid:** deadline, guarantees, award criteria and their weights, service levels and penalties.

A wrong answer is expensive. Missing the deadline, not lodging the 5 % guarantee or misreading a solvency threshold gets the bid excluded. A misread service level or penalty becomes a binding commitment on a contract worth €295,200 (ENISA) to €22.9 million (GISS) in estimated value.

"I don't know" is cheap. Every answer cites [document, page], so the user opens that page of the tender documents, which are the legally binding text anyway. So the assistant should refuse whenever it does not retrieve the passage.

## Corpus

Nine public documents from three real Spanish cybersecurity tenders (SOC/MDR), all from 2026. For each tender:
- **PCAP** (administrative clauses: solvency, guarantees, award criteria, penalties), from PLACSP.
- **PPT** (technical specifications: service levels, staff, tools), from PLACSP.
- **TED notice**, downloaded as JSON from the TED Search API. It is the official summary (value, duration, deadline). It is also where one contradiction with the PCAP shows up (q28).

| Document | Tender | Type | URL | Date | Licence | Words |
|---|---|---|---|---|---|---|
| `cartagena_pcap` | Ayuntamiento de Cartagena (SE2026/44) | PCAP | [PLACSP](https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=3RvTg%2BqJGplpqK%2BNayOJdmu3brxMJj85yHdub21Tk8IRUVsFr1wAigfAsquMfDh9lBaZNGbs4SxQbAtLZnFB2c83c%2Bb8gBCF4jisIX8LfHOHAj0WEJrB5sP7amrh2jBD) | 2026-09-09 | Ley 37/2007 (PLACSP) | 13,106 |
| `cartagena_ppt` | Ayuntamiento de Cartagena (SE2026/44) | PPT | [PLACSP](https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=4LNw9X8Oth%2BSn9NbTkZ4FS6sIE23mzU7WXFZ56WAvbF1G%2BlP4OQLs1MxqFW16iI7xeK%2BjNty6lM6gGPDyy6wJX7drdkgQxKh8ayOdg%2BOlwGHAj0WEJrB5sP7amrh2jBD) | 2026-07-28 | Ley 37/2007 (PLACSP) | 6,657 |
| `cartagena_ted` | Ayuntamiento de Cartagena (SE2026/44) | TED notice | [TED 649174-2026](https://ted.europa.eu/es/notice/-/detail/649174-2026) | 2026-09-21 | Decision 2011/833/EU (TED) | 315 |
| `enisa_pcap` | ENISA (56/2026) | PCAP | [PLACSP](https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=9ETPlYBON0QDBMg/Qhi65LuaWFeo/yh0sxRjsJQIi9I23eR5bxfQbFmYrhtwrA6xiOf5PEsipiU7Qc1eWPlT2bG9QfRLddT5kTx4EkNbrTqCx2e6p7hqtlp2aFupgHMr) | 2026-07-27 | Ley 37/2007 (PLACSP) | 13,660 |
| `enisa_ppt` | ENISA (56/2026) | PPT | [PLACSP](https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=47dHKqAqtfJ1wQ0TG75owUHSgz94ch%2BQdgK4Ni1EKa/Fn5t09e5eP/7%2BHUMzKwCqXx5FiJeMlcwnb6%2BXDhu8vvAFA9Kll/3leo9p7zi5FHht/o8fNevwsujgRzaBbugn) | 2026-07-27 | Ley 37/2007 (PLACSP) | 6,920 |
| `enisa_ted` | ENISA (56/2026) | TED notice | [TED 530695-2026](https://ted.europa.eu/es/notice/-/detail/530695-2026) | 2026-07-31 | Decision 2011/833/EU (TED) | 336 |
| `giss_pcap` | GISS (2026/7028) | PCAP | [PLACSP](https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=utdJKrcIIi8TnaqXvWAbH6rIIccFdesQyEoNK3OwOZWh6ayu5tQXrTM7Ellxz2qtMvT/tGixw9fore9Gnhnf402jEM6FdBnnUZRaT5ybWWjfdyQgZAdTm3EfcUAC7CJ6) | 2026-11-19 | Ley 37/2007 (PLACSP) | 22,717 |
| `giss_ppt` | GISS (2026/7028) | PPT | [PLACSP](https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=4Olo7kYgFvEES5uZIJmlCdK2/Qrpoei5GZTfHej2T75bfV%2BsuxKUo7kvgBuuBPt6bwuwEw2f9qdtYb4ExfoogqlYTMRd9VRC8R9/oCOZn6Q//q7NB2iMZvNyf0xrJmjt) | 2026-11-19 | Ley 37/2007 (PLACSP) | 20,873 |
| `giss_ted` | GISS (2026/7028) | TED notice | [TED 809807-2026](https://ted.europa.eu/es/notice/-/detail/809807-2026) | 2026-11-20 | Decision 2011/833/EU (TED) | 477 |
| **Total** | 3 tenders | 9 documents | | | | **85,061** |

- **Date:** for PDFs, the date of the final version in the file metadata. For TED notices, the publication date.
- **Words:** counted after cleaning and redaction (`index/corpus_stats.csv`). 293 pages in total.
- **Licence:** PLACSP documents are public sector information, and Ley 37/2007 allows their reuse if the source is cited. TED notices can be reused under the European Commission's reuse policy (Decision 2011/833/EU).
- **Personal data:** the PDFs are electronically signed, so they contain the signers' names and some emails. `index.py` replaces them with tags before chunking: 70 signature blocks, 4 emails and 1 name. From TED I request only the fields I need, with no contact-person fields.
- The original PDFs are not committed (`corpus/` is in `.gitignore`). `main.py index` downloads them again from the URLs above.


## Ingestion

`index.py` runs one pipeline for every document. `server.py` imports it for `add_document`.

1. **Extract.** PDFs are read with `pypdf`, page by page, so each chunk keeps its page number. TED notices arrive as JSON from the TED API; `index.py` turns them into one page of text with Spanish labels («Valor estimado total (sin IVA): 585000 Moneda: EUR»).
2. **Redact personal data**, once before cleaning and once after.
3. **Clean.**
   - Remove lines that repeat on 40 % or more of a document's pages (headers, footers, signature blocks).
   - Remove table-of-contents lines and page numbers.
   - Join words split by a hyphen at the end of a line (81 cases in `giss_ppt`).
   - Fix small capitals that pypdf splits: «D ESCRIPCIÓN» → «DESCRIPCIÓN» (31 cases in `giss_ppt`).
4. **Chunk.** There are two designs (see *Retrieval*). The structural one finds clause headings («CLÁUSULA 12», «TERCERA.-», «4.1. PRESUPUESTO», lines in capitals) and makes one chunk per clause. Clauses under 60 words are merged with the next one. Clauses over 350 words are split into equal parts, and each part after the first starts with `[heading] (continuación)`.
5. **Embed and store.** gemini-embedding-2 (768 dimensions), in batches of 20, into ChromaDB (`index/chroma`, cosine distance), one collection per design. The chunk id is a hash of its text, so running `main.py index` again only embeds chunks that have no saved vector.

**Extraction problem I fixed: the Cartagena signature footer.**
- Every page of the two Cartagena PDFs ends with an e-signature footer. pypdf extracts it as eight lines: «La comprobación de la autenticidad de este documento…», «Código Seguro de Verificación: …», «AYUNTAMIENTO DE CARTAGENA», «FIRMADO POR», the signer's name, the job title, the date and «Pág. 10 de 31».
- It caused three problems. It cut in two every clause that crosses a page. It repeated the same noise on all 69 pages of the two documents. And it put a person's name in the index.
- The fix has three parts:
  1. A redaction pattern for this format, because the name is on the line after «FIRMADO POR».
  2. The header/footer filter replaces digits with `#` before counting lines, so «Pág. 10 de 31» and «Pág. 11 de 31» count as the same line.
  3. A second redaction pass after cleaning, for emails that only become whole once hyphenated words are joined.
- Result: no chunk in `index/chunks_struct.csv` contains «Código Seguro», «FIRMADO POR» or a page footer.
- I accepted one side effect. The small-capitals fix also joins a few real one-letter words, for example «anexo X lo» → «anexo Xlo» (about 7 cases). This does not hurt retrieval.

**Another fix: headings.** Numbered paragraphs like «2.5. El desconocimiento del contrato…» looked like headings and produced tiny chunks. Now a numbered line counts as a heading only if the next line does not start in lower case.

**Chunk metadata:** `doc_id`, `doc_type` (pcap, ppt, ted), `title`, `tender_key`, `tender_id`, `buyer`, `aliases`, `url`, `section` (the clause heading), `page_start`, `page_end`, `words`, `design`, `file_sha256` and `origin`. Citations are `[doc_id, p. page_start]`. The tender filter uses `tender_key`.

**Number of chunks:**
- **struct:** 405 (Cartagena 65 PCAP + 42 PPT + 3 TED; ENISA 66 + 38 + 3; GISS 100 + 85 + 3). They have 60–356 words, median 211.
- **fixed300:** 320.

## Test set

There are 37 questions in `eval/questions.csv`, written from the indexed documents. Claude helped me draft them, and I checked each one against the PDF page.

- **25 single:** one passage answers them. Example: «¿Cuál es el valor estimado del contrato de SOC/MDR del Ayuntamiento de Cartagena?» (585.000 € sin IVA).
- **6 multi:** they need two passages, from two tenders or from two documents of the same tender. Example: «¿Exigen Cartagena y ENISA la misma garantía definitiva?». In q28 («¿Coinciden la duración del contrato de Cartagena en el pliego y en el anuncio de TED?») the two documents disagree: the PCAP says «tres años y tres meses» and TED says 455 días.
- **6 unanswerable**, all on topic:
  - tenders that are not in the corpus: «¿Qué garantía definitiva exige la EMVS de Madrid en su licitación de SOC?», and one from the Ayuntamiento de Murcia;
  - facts that tender documents do not contain: the winner, the number of bids, the signature date;
  - a threshold set by another regulation: «¿Cuál es el umbral de regulación armonizada para contratos de servicios en 2027?».

The questions cover what a bid manager checks before bidding: eligibility (solvency, certifications, classification), money (budget, estimated value, guarantees, penalties), timing (deadline, duration, extensions), scoring (criteria and weights) and service levels.

## Retrieval
I compared two chunking designs. Each one has its own full set of embeddings (gemini-embedding-2, 768 dimensions).
- **fixed300:** 300-word windows with a 30-word overlap. Ignores the document structure. 320 chunks.
- **struct:** one chunk per clause, with its heading. 60–350 words. 405 chunks.

On each design I tested three search methods:
- **dense:** cosine similarity of the embeddings;
- **BM25:** keyword search;
- **hybrid:** both rankings fused with Reciprocal Rank Fusion.

I ran each one with and without a filter that only searches the tender named in the question. A hit is a chunk from the expected document that overlaps the expected page. Results on the 31 answerable questions, with the filter on:

| Design | Method | hit@1 | hit@3 | hit@5 | multi_all@5 | Words added to the prompt |
|---|---|---|---|---|---|---|
| fixed300 | dense | 0.58 | 0.84 | 0.90 | 0.17 | 1,413 |
| fixed300 | hybrid | 0.61 | 0.84 | 0.94 | 0.33 | 1,450 |
| struct | bm25 | 0.58 | 0.81 | 0.87 | 0.50 | 944 |
| struct | hybrid | 0.65 | 0.87 | 0.94 | 0.50 | 907 |
| **struct** | **dense** | **0.71** | **0.94** | **1.00** | **0.50** | **869** |

All 12 combinations are in `eval/retrieval.md`.

**I chose struct + dense, with the tender filter on and 5 chunks per search.**
1. **Best hit rate at every k.** With 5 chunks, the right passage is retrieved for all 31 questions, and for 22 of them it comes first. Chunking matters more than the search method: fixed windows cut clauses in half, so the heading «garantía definitiva» can land in one chunk and the percentage in the next.
2. **Cheapest.** It adds 869 words to the prompt per search, against 1,413 for fixed300 (38 % less).
3. **Hybrid did not help.** Legal boilerplate repeats the same words (garantía, plazo, contrato) in many clauses, so BM25 is weak here. Fusing it pulls those clauses up: hit@1 is 0.65, against 0.71 for dense alone.
4. **The filter changes nothing for dense** (0.71 with and without it), but I keep it. It costs nothing, and it protects against the most expensive error in my use case: a figure from the wrong tender.

**Limitation:** one search finds both passages for only 3 of the 6 multi questions (multi_all@5 = 0.50). That is why `AGENTS.md` tells the agent to run one search per tender when comparing.

## Tools and subagent
`server.py` is an MCP server with two tools. The model reads their descriptions, so they say what the corpus contains, when to use each tool, what the arguments mean and how to cite. They are in Spanish, like the corpus.

**`search(query, licitacion="")`**

```text
Busca en un corpus de pliegos REALES de licitaciones públicas españolas de
ciberseguridad (servicios SOC/MDR), descargados de la Plataforma de Contratación del Sector
Público (PCAP = cláusulas administrativas: plazos, solvencia, garantías, criterios de
adjudicación, penalidades...; PPT = prescripciones técnicas: servicios, perfiles, SLAs,
herramientas) y de sus anuncios en TED (DOUE).

Licitaciones disponibles: «cartagena» = Ayuntamiento de Cartagena, expte. SE2026/44; «enisa» = Empresa Nacional de Innovación, S.M.E., S.A. (ENISA), expte. 56/2026; «giss» = Gerencia de Informática de la Seguridad Social (GISS), expte. 2026/7028.

Úsala SIEMPRE antes de responder cualquier pregunta sobre estas licitaciones; puedes
llamarla varias veces con consultas distintas (p. ej. una por licitación al comparar).
Argumentos:
  - query: la consulta en español, con las palabras que esperas encontrar en el pliego.
  - licitacion (opcional): clave de la licitación para buscar SOLO en ella
    (p. ej. "cartagena"). Si la omites y la consulta nombra una, se filtra sola.
Devuelve hasta 5 fragmentos; cada uno trae la cita exacta que debes usar,
con el formato [doc_id, p. N], el documento, el apartado y las páginas.
```

**`add_document(path)`**

```text
Añade un documento nuevo al índice del corpus: lo extrae, lo limpia, borra los
datos personales, lo trocea, calcula sus embeddings con Gemini y lo guarda, de modo que
search ya lo encuentre. Úsala solo cuando el usuario pida explícitamente añadir un
fichero. Argumento: path, ruta a un fichero .htm, .html, .json, .md, .pdf, .txt dentro de
la carpeta del proyecto. Si el mismo contenido ya está indexado no hace nada (no gasta
cuota); si es una versión nueva de un documento con el mismo nombre, sustituye la
anterior. Devuelve el doc_id que debes usar en las citas y cuántos fragmentos se añadieron.
```

**One search result** (trimmed: the full result returns the whole text of all 5 chunks):

```text
5 fragmentos para «garantia definitiva» (filtrados por la licitación «cartagena»)
---
[1] Cita: [cartagena_pcap, p. 21]
Documento: Pliego de Cláusulas Administrativas Particulares (PCAP) — Servicio de SOC/MDR y herramientas de ciberseguridad (Ayuntamiento de Cartagena, expte. SE2026/44)
Apartado: B) DOCUMENTACIÓN JUSTIFICATIVA DE HALLARSE AL CORRIENTE EN EL CUMPLIMIENTO DE SUS | Páginas: 21-22
Texto: … B.1) Garantía definitiva . El adjudicatario deberá constituir a disposición del Órgano de Contratación, en la Tesorería Municipal, una garantía definitiva del 5% del precio final ofertado , excluido el Impuesto sobre el Valor añadido, de conformidad con lo establecido en el artículo 107 de la LCSP. …
---
[2] Cita: [cartagena_pcap, p. 30]  Apartado: 17.1. Plazo y devolución de la garantía.
[3] Cita: [cartagena_pcap, p. 29]  Apartado: 16.- RECEPCIÓN DEL CONTRATO.
[4] Cita: [cartagena_pcap, p. 29]  Apartado: V.- EXTINCIÓN Y LIQUIDACIÓN DEL CONTRATO.
[5] Cita: [cartagena_pcap, p. 18]  Apartado: 5 PUNTOS
```

The answer is the first result. Results 2–4 are about returning the guarantee. Result 5 is noise: it is an award criterion, and its heading «5 PUNTOS» is a chunking mistake (a score line taken as a heading), the same weakness behind q08 and q09 (see *Failures*).

**Subagent** (`.claude/agents/corpus-researcher.md`). It can only use `mcp__corpus__search`. Its instructions (in Spanish) say:
- search before answering; when comparing tenders, search each tender separately with `licitacion`;
- if the results are not enough, rephrase with the words a tender document would use, with at most 4 searches;
- answer in Spanish, briefly, with the exact citation `[doc_id, p. N]` after each claim;
- if the chunks do not answer the question, start with «El corpus no cubre esta pregunta» and say what it searched for.

**Transcript from Claude Code.** Claude Code was in auto permission mode, so it approved the read-only `search` calls without asking me. The full export is in `eval/subagent_transcript.txt`.

```text
❯ Usa el subagente corpus-researcher para responder: ¿Qué solvencia económica
  exigen Cartagena y ENISA a los licitadores?

⏺ corpus-researcher(Solvencia económica Cartagena y ENISA)
  ⎿  Backgrounded agent (↓ to manage · ctrl+o to expand)

⏺ He lanzado el subagente corpus-researcher para buscar la solvencia económica
  que piden Cartagena y ENISA. Hace una búsqueda por cada licitación, en los
  pliegos y en los anuncios de TED. Cuando termine te paso la respuesta con sus
  citas.

› Message from corpus-researcher
  En las dos licitaciones el único requisito de solvencia económica y financiera
  es el volumen anual de negocios. Ni el PCAP ni el anuncio de TED piden seguro
  de responsabilidad civil ni patrimonio neto. ENISA da una cifra exacta.
  Cartagena solo la da como fórmula, sin importe.

  **Cartagena (expte. SE2026/44)**
  - **Criterio:** volumen de negocios anual general. Cuenta el mejor de los tres
  últimos ejercicios, según la fecha de constitución o de inicio de actividades
  y la de presentación de ofertas [cartagena_pcap, p. 7].
  - **Cifra:** el pliego no da un importe. Dice que el volumen debe ser «de
  importe igual o superior al precio de licitación anual del contrato»
  [cartagena_pcap, p. 7]. En los fragmentos que encontré no sale el precio de
  licitación anual. El anuncio de TED solo da el «Valor estimado total (sin
  IVA): 585000 Moneda: EUR» y una «Duración del contrato por lote: 455 días»
  [cartagena_ted, p. 1]. No he calculado el umbral a partir de esos datos.
  - **Cómo se acredita:** con el medio del artículo 87.1a) de la LCSP, es decir,
  el volumen anual de negocios del mejor de los tres últimos ejercicios
  disponibles, «por importe igual o superior al exigido en el anuncio de
  licitación y en los pliegos del contrato» [cartagena_pcap, p. 20]. El
  fragmento no dice qué documento hay que presentar (cuentas anuales u otro).
  - **Anuncio de TED:** como criterio de selección económica figura solo «Cifra
  anual de negocio» (código slc-stand-to-gen) [cartagena_ted, p. 1]. Coincide
  con el PCAP.
  - **Seguro:** la póliza de seguro no es un requisito de solvencia. Es un
  criterio de adjudicación que da 3 puntos [cartagena_ted, p. 1]. Se valora que
  el licitador incluya, «sin coste adicional para el Ayuntamiento de Cartagena,
  una póliza de seguro específica con un capital asegurado mínimo de 1.000.000
  de euros por siniestro y anualidad», vigente durante todo el contrato
  [cartagena_pcap, p. 15].

  **ENISA (expte. 56/2026)**
  - **Criterio:** importe neto de la cifra de negocios, referido al mejor de los
  tres últimos ejercicios disponibles (art. 87 LCSP) [enisa_pcap, p. 23].
  - **Cifra:** «al menos, una vez y media el valor anual medio del contrato,
  esto es: 123.000,00 €» [enisa_pcap, p. 23].
  - **Cómo se acredita:** con las cuentas anuales aprobadas y depositadas en el
  Registro Mercantil o, si la empresa no está inscrita en él, en el registro
  oficial que le corresponda. Los empresarios individuales no inscritos lo
  acreditan con sus libros de inventarios y cuentas anuales legalizados por el
  Registro Mercantil [enisa_pcap, p. 24].
  - **Alternativa por clasificación:** se puede acreditar la solvencia con la
  clasificación Grupo V, Subgrupo 5, Categoría 1. Hay que aportar el certificado
  de clasificación, original o copia autenticada, y una declaración responsable
  de que sigue vigente [enisa_pcap, p. 23].
  - **Registro de licitadores:** la inscripción en el Registro Oficial de
  Licitadores y Empresas Clasificadas del Sector Público acredita la solvencia
  económica y financiera, salvo prueba en contrario [enisa_pcap, p. 22].
  - **Anuncio de TED:** como criterio económico figura solo «Cifra anual de
  negocio» [enisa_ted, p. 1]. Coincide con el PCAP. El anuncio no repite la
  cifra de 123.000,00 €.

  **Contradicciones:** no he encontrado ninguna entre el PCAP y el anuncio de
  TED en ninguna de las dos licitaciones.

  Lo que el corpus no cubre: no encontré ningún requisito de seguro de
  responsabilidad civil ni de patrimonio neto como solvencia en ninguna de las
  dos licitaciones. En Cartagena tampoco sale el importe en euros del «precio de
  licitación anual», que es lo que fija el umbral, ni el documento concreto con
  el que se acredita el volumen de negocios. Busqué «solvencia económica y
  financiera volumen anual de negocios» y «anuncio TED criterios de selección
  situación económica y financiera seguro de responsabilidad civil (patrimonio
  neto)», una vez en cada licitación, y llegué al máximo de 4 búsquedas.

⏺ Las dos licitaciones piden como solvencia económica y financiera solo el
  volumen anual de negocios. ENISA fija una cifra concreta. Cartagena solo da la
  fórmula, sin el importe en euros.

  [Claude Code then repeats the same answer for the user; full text in
  eval/subagent_transcript.txt]

  Lo que el corpus no cubre: ninguna de las dos pide seguro de responsabilidad
  civil ni patrimonio neto como solvencia. En Cartagena tampoco aparece el
  importe del «precio de licitación anual» ni el documento con el que se
  acredita el volumen de negocios. El subagente llegó al límite de 4 búsquedas,
  así que quizá haya páginas del PCAP de Cartagena que no ha revisado.

⏺ Agent "Solvencia económica Cartagena y ENISA" finished · 23s
```

What it shows:
- It ran two searches per tender (one with the words of the tender document, one for the TED notice), checked both sources against each other and cited every claim.
- **ENISA:** it gave the exact threshold, 123.000,00 € [enisa_pcap, p. 23].
- **Cartagena:** the PCAP only gives a rule («de importe igual o superior al precio de licitación anual del contrato»). The subagent did not calculate the amount from the TED value, and it said so.
- It used its 4 searches and warned that it might have missed pages. The warning was right: the annual amount is in the PPT (p. 37: 195.000 € a year without VAT, 235.950 € with VAT), which it never searched.
- So the answer was honest but incomplete. The user still has to open the cited pages. Compare q06: my main agent did find PPT p. 37, but then stated the threshold as 195.000 € sin IVA without being asked (see *Failures*).

## Adding a document

**What happens if the document is already indexed.** `add_document` computes the SHA-256 hash of the file and looks for it in the index.
- **Same content already indexed:** it answers «YA INDEXADO» and does nothing. No embeddings are made, so no quota is spent.
- **Same name (same `doc_id`) but new content:** it embeds and stores the new version first, and only then deletes the old chunks. There are no duplicates, and if the API fails halfway (quota, network) the old version stays in the index.

Before indexing, it also checks that the file exists, is inside the project folder, has an allowed type and is 25 MB or less. Then it runs the same pipeline as `index.py` (imported, not rewritten), redaction of personal data included.

**Demo** (`demo_add_document.py`, output saved in `eval/add_document_demo.md`). It works on a temporary copy of `index/`, so the index I submit and my evaluation do not change.
- **Unanswerable question (q32):** «¿Qué garantía definitiva exige la EMVS de Madrid en su licitación de SOC?»
- **Document added:** `nuevos/emvs_madrid_pcap.pdf`, the PCAP of the EMVS Madrid SOC tender, from PLACSP.

**Before:**

```text
El corpus no cubre esta pregunta.
Buscé información sobre la garantía definitiva en las licitaciones disponibles en el corpus (Ayuntamiento de Cartagena, ENISA y Gerencia de Informática de la Seguridad Social), pero ninguna corresponde a la EMVS de Madrid. […]
```

**add_document:**

```text
AÑADIDO: «emvs_madrid_pcap.pdf» como doc_id «emvs_madrid_pcap»: 169 fragmentos nuevos. Datos personales tachados: {'firma': 208, 'email': 6, 'telefono': 1}. Cítalo como [emvs_madrid_pcap, p. N].
```

**After:**

```text
La EMVS de Madrid exige una garantía definitiva cuya cuantía es igual al 5 por 100 del importe del precio final ofertado por el licitador, excluido el Impuesto sobre el Valor Añadido, o, en su caso, del presupuesto base de licitación, excluido el Impuesto sobre el Valor Añadido, según lo previsto en el apartado 15 del Anexo I del pliego [emvs_madrid_pcap, p. 15].

Debe acreditarse en el plazo de diez días hábiles a contar desde el siguiente a aquel en que se reciba el requerimiento del artículo 150.2 de la LCSP [emvs_madrid_pcap, p. 15].
```

- The refusal became a cited answer from the new document.
- Cost: before, 5,913 tokens and 2.96 s; after, 5,556 tokens and 2.03 s.
- Redaction also worked on a document it had never seen: 208 signatures, 6 emails and 1 phone number removed.

## Harness and guardrails
**System prompt.** `agent.py` (LangChain `create_agent`, model gemini-3.5-flash-lite) uses `AGENTS.md` as the system prompt, unchanged. Each rule has its reason written in the file.

Required rules:
1. «Responde solo con lo que devuelve `search`.»
2. «Cita cada afirmación con el formato exacto `[doc_id, p. N]`.»
3. «Si el corpus no cubre la pregunta, dilo.» The answer must start with «El corpus no cubre esta pregunta».

My rules:

4. «Si el corpus solo cubre una parte de la pregunta, responde esa parte y avisa de lo que falta.» The answer ends with «Lo que el corpus no cubre:».
5. «Si dos documentos se contradicen, da los dos valores y avisa.»
6. «Copia las cifras tal como salen en el pliego.» It calculates only if the user asks, showing the operation.
7. «Puedes dar una opinión, pero la decisión es del usuario.» The opinion goes in a paragraph that starts with «Opinión (la decisión es tuya):».

**Limits:** at most 6 tool calls and 10 model calls per question (LangChain middleware). A confused agent cannot loop and use up the quota.

**Approval step.**
- The MCP tools are wrapped as LangChain tools.
- Before `add_document` runs, the wrapper shows the path and asks `[s/N]`.
- Any answer except «s» denies it. The tool is not called, and the agent receives: «DENEGADO: el usuario no ha aprobado añadir este documento. No lo vuelvas a intentar; explica que hace falta su aprobación.»
- When there is no terminal (for example inside `main.py evaluate`), it denies automatically.

Example:

```text
$ uv run python main.py ask "Añade al índice el documento nuevos/emvs_madrid_pcap.pdf"

[APROBACIÓN] El agente quiere AÑADIR al índice el fichero:
    nuevos/emvs_madrid_pcap.pdf
Esto gasta cuota de embeddings y cambia el índice. ¿Lo apruebas? [s/N] N
El corpus no cubre esta pregunta. Tras buscar en el corpus los expedientes disponibles (Cartagena, ENISA y GISS), no se encuentra el documento `nuevos/emvs_madrid_pcap.pdf` ni información relativa a la EMVS de Madrid, ya que el sistema requiere la aprobación expresa del usuario para añadir nuevos documentos al índice (véase, por ejemplo, [enisa_pcap, p. 1]).

[guardarraíl de citas] corregida: la respuesta no tiene ninguna cita [doc_id, p. N]

--- Primera respuesta del agente (la que paró el guardarraíl) ---
El corpus no cubre esta acción porque el usuario no ha aprobado añadir el documento. Para poder añadir `nuevos/emvs_madrid_pcap.pdf` al índice, se requiere su aprobación expresa.
--- Fin de la primera respuesta ---

[2 llamadas a herramientas · 8862 tokens · 23.93 s]
```

The document was not added, and the index did not change.

**Extra guardrail: citation check.** After each answer, code checks two things:
- an answer that is not a refusal has at least one citation;
- each cited `[doc_id, p. N]` falls inside a chunk that `search` returned for that question.

If a check fails, the harness tells the agent what is wrong and asks for one rewrite. If the rewrite also fails, the harness replaces it with «El corpus no cubre esta pregunta con fuentes verificables» plus the reason. Both answers are saved in the trace.

Why this guardrail: in my use case, an answer is only useful if the user can open the cited page. A model can write a citation that looks right but points to a page it never retrieved.

**Where it fired:**
- **The approval run above.** The first answer was correct, but it started with «El corpus no cubre esta acción» instead of the exact phrase, so the code saw an answer without citations. In the rewrite, the agent added `[enisa_pcap, p. 1]`, a page that says nothing about approvals. The guardrail let it through because that page had been retrieved. **This is its limit:** it checks that a citation points to retrieved text, not that the text supports the sentence. Only the judge's *supported* grade checks that, and only during evaluation. Here the guardrail made a correct answer worse.
- **q26 in the first evaluation run** («¿Exigen Cartagena y ENISA la misma garantía definitiva?»). It blocked a correct answer. The blocked text was not saved at the time. The most likely cause is two citations in one bracket, as in the re-run (`[cartagena_pcap, p. 21, enisa_pcap, p. 31]`), which my first parser could not read. I fixed the parser, made the harness save the original answer and re-ran q26, which passed. In the final run of all 37 questions, the guardrail fired 0 times.
- **A test where it did not fire.** I asked the agent to answer from memory and cite `[cartagena_pcap, p. 99]`. It refused by itself, quoting rules 1 and 2, without calling any tool. Refusals are not checked, so the guardrail had nothing to do.

**What I would fix first:** skip the check when the turn ended with a denied `add_document`, since there is nothing to cite. Then check that the cited chunk contains the key figure or term of the sentence it supports.

## Evaluation

**Code checks** (`evaluate.py`, no LLM):
- **Refusal:** the answer contains «El corpus no cubre esta pregunta» in its first 300 characters.
- **Citations:** every `[doc_id, p. N]` must point to a chunk that `search` returned for that question.
- **Refusal questions are graded by code:** a refusal on an unanswerable question is correct; a refusal on an answerable one is a wrong refusal; an answer to an unanswerable one is a missed refusal.
- **Retrieval:** did the agent retrieve the expected passage(s)? For multi questions, all of them.

**LLM judge** for the 31 answers that are not refusals. It sees the question, my reference answer, the evidence the agent retrieved and the agent's answer. It returns JSON: `correct` (1/0), `supported` (1/0) and a reason. Temperature 0. My rubric (`eval/rubric.md`) is strict, because the user decides whether to bid with these answers:
- a multi answer with one part missing is wrong;
- figures must match in number and unit (only format changes are allowed);
- extra information is fine in *correct*, but it must be in the evidence for *supported*;
- a figure from another tender is wrong;
- a contradiction counts only if both values are given;
- a calculation is supported only if every input is in the evidence and the arithmetic is right.

**Judge model.** I started with gemini-3.6-flash. Its free tier allows 20 requests a day, and it ran out after 18 answers. I switched to gemini-3.1-flash-lite (500 a day) and re-graded all 31 with it, so one judge grades everything. It is not the agent's model, so the agent does not grade itself. On the 18 answers both judges graded, they agreed 17/18 on *correct* and 18/18 on *supported* (`eval/judges_comparison.md`).

**Agreement with my labels** (all 37 answers, `eval/human_labels.csv`):

| | Agreement | Cohen's kappa |
|---|---|---|
| correct | 36/37 (0.973) | 0.786 |
| supported | 35/37 (0.946) | 0.479 |

The three disagreements:
- **q06 and q09:** the judge said *supported*; I said no. In both, the error comes from the evidence itself (q09: a chunk with a wrong heading) or from linking two retrieved facts (q06). The judge accepts those; only checking the PDF catches them.
- **q11:** the judge said wrong; I said right. My reference answer had more than the question asked (see *Failures*).

Kappa is low for *supported* because almost every answer is supported, so two disagreements weigh a lot. Caveat: Claude proposed my labels and I reviewed them (see *AI use*), so they are not fully independent.

**Results** (37 questions):

| | Judge + code | My labels |
|---|---|---|
| Correct | 34/37 (92 %) | 35/37 (95 %) |
| · single | 23/25 | 24/25 |
| · multi | 5/6 | 5/6 |
| · unanswerable | 6/6 | 6/6 |
| Unsupported (of 31 answers) | 1/31 (3 %) | 3/31 (10 %) |
| Correct refusals | 6/6 | 6/6 |
| Wrong refusals | 0/31 | 0/31 |
| Missed refusals | 0 | 0 |
| Answers with invalid citations | 0 | — |

The agent never refused an answerable question and never answered an unanswerable one. Every citation pointed to a retrieved chunk.

## Failures

Five answers have a 0 in my labels or in the judge's grades:

| Question | Cause | What happened |
|---|---|---|
| q08 «¿Cuántos puntos reparte Cartagena en los criterios de juicio de valor?» | wrong answer from the right passage | Said 53 points instead of 49. It added two objective criteria (póliza, personal indefinido) because they sat in a chunk titled «CRITERIOS JUICIOS DE VALOR SUBJETIVOS PUNTOS». |
| q09 «¿Qué capital mínimo debe cubrir la póliza de seguro en el contrato de Cartagena?» | unsupported claim | The amount is right (1.000.000 €), but it says the policy is a «juicio de valor» criterion. The chunk's text says «Se establecen como criterios objetivos los siguientes: a.-Póliza de seguro (3 puntos)». It trusted the heading. |
| q30 «¿Cuánto duran los contratos de ENISA y de la Seguridad Social?» | retrieval miss | ENISA is right (36 meses). The GISS duration (24 months per lot) is in `giss_ted`, p. 1. The agent searched the GISS tender three times and only got the PCAP clause that points to the «Hoja Resumen». It said so with «Lo que el corpus no cubre:», but half a multi answer counts as wrong. |
| q06 «¿Qué volumen de negocios se exige como solvencia económica en la licitación de Cartagena?» | unsupported claim | The rule is right. But it added, unasked, that the minimum is 195.000 € sin IVA. The PCAP does not say if the «precio de licitación anual» includes VAT (with VAT it is 235.950 €). This breaks rule 6. |
| q11 «¿Con qué frecuencia hay reuniones de seguimiento en el servicio de Cartagena?» | bad test question | The answer (weekly) is right. My reference also had the 24x7 phone, which the question does not ask for, and the judge marked it wrong. |

**Counts:** unsupported claim 2 · wrong answer from the right passage 1 · retrieval miss 1 · bad test question 1 · wrong refusal 0.

**q08 and q09 have the same root cause: chunking.** The award-criteria clause of `cartagena_pcap` is longer than 350 words, so the chunker split it and repeated its first heading on three continuation chunks (pp. 15–18). Those chunks actually contain the price formula and the objective criteria. The objective criteria start with a sentence, not a heading line, so the chunker did not see the new section.

**What to fix first: the chunking.**
1. Treat sentences that open a new block of criteria («Se establecen como criterios objetivos…») as headings, and do not repeat a heading on a chunk that starts a different block.
2. Re-index (only changed chunks get new embeddings), re-run the evaluation and re-label q08 and q09.

Why first: it explains 2 of the 4 real failures, and it is the most dangerous kind. The wrong label sits inside the evidence, so the answer cites a real page, the guardrail passes it and the judge accepts it (q09).

Next fixes:
- **q30:** for durations and values, tell the agent to also search the TED notice.
- **q06:** a code check that flags figures in the answer that do not appear in the cited chunk.
- **q11:** reference answers should contain only what the question asks.

I also fixed the evaluation script: it counted a multi question as "passage retrieved" when only one of its passages was retrieved, so q30 was first suggested as "wrong answer from the right passage".

## Decision

**Not yet.** The results are good: 92–95 % correct, every refusal right and every citation valid. But the two chunking errors are the kind a bid manager cannot afford. A wrong point total or a criterion of the wrong type, with a real citation, changes how the proposal is written, and neither my guardrail nor the judge caught them.

First I would fix the chunking, re-run the evaluation and check my labels again. If q08 and q09 pass and nothing else breaks, I would let the bid manager use it for go/no-go and to find the right page fast. **Safeguard:** before committing money or signing, open the cited page and check the figure there. The citation makes that a few seconds.

**Cost per question** (37 questions, gemini-3.5-flash-lite):
- **Tokens:** 7,196 on average (median 5,677).
- **Time:** 7.5 s on average (median 3.8 s, max 36.45 s).
- **Searches:** 1.32 tool calls on average.

## AI use

- I used Claude throughout to undertand everyhtgn i was doing.
- Claude wrote all the code (`index.py`, `retrieval.py`, `server.py`, `agent.py`, `evaluate.py`, `.claude/agents/corpus-researcher.md` and the helper scripts `buscar_licitaciones.py`, `etiquetar.py`, `ver_respuesta.py`, `demo_add_document.py`, `comparar_jueces.py`) and explained it to me step by step. I ran everything on my computer in my terminal, checked the outputs and reported errors, which Claude fixed (for example, a race condition in the query cache, the parser for grouped citations and, in a final review, the order of operations in `add_document`).

  What i decided: 
  - the use case;
  - the corpus: real PLACSP/TED tenders, with personal data removed and licences checked;
  - the four extra rules in `AGENTS.md` and the judge rubric. Claude asked me multiple-choice questions and wrote the text from my answers
  - the retrieval design, chosen by the numbers in `eval/retrieval.md`;
  - the judge model there was a point  when gemini-3.6-flash ran out of free quota so Claude proposed the options and I chose gemini-3.1-flash-lite
  - the ship decision: not yet, fix the chunking first.
- **Test set:** drafted with Claude. I checked each question and reference answer against the PDF page.
- **Human labels:** Claude proposed a grade for each of the 37 answers using my rubric. I decided the doubtful ones (q06, q09, q11) and confirmed all of them. So my labels are not fully independent of an LLM, which matters when reading the agreement with the judge.
- **Failure causes:** Claude proposed a cause for each failure from the agent's traces; I checked and confirmed them.
- **Report:** Claude drafted the text from my decisions and my results. I reviewed and edited it.
- **Claude Code:** used only to run the subagent.
- The Gemini models (embeddings, agent and judge) are part of the system I evaluate, not help with the assignment.
