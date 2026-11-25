TRIPRESCUE — ASSIGNMENT CORPUS

Core: 4 English official EU documents, 75,678 extracted words.
Holdout: bus/coach passenger rights, Regulation 181/2011. Do not index until the add-document demonstration.

FILES
core/*.pdf: official original publications.
holdout/: official English HTML for the extension.
(The preliminary text extractions originally shipped here were removed: index.py extracts from the PDFs and HTML itself.)
manifest.json: sources, word counts, checksums and editions.

WORD COUNT
Whitespace-separated tokens after basic header/blank-line removal. Includes footnotes, references and front matter. This is a preliminary extraction count, not a final fully cleaned count. Recount after ingestion cleanup; there is about 25,000 words of margin above the assignment threshold.

USE AND ATTRIBUTION
Source: European Union, Official Journal, via the Publications Office.
EUR-Lex allows reuse of legal documents for commercial and noncommercial purposes unless otherwise specified. Preserve source attribution and identify extraction changes.
Terms: https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en

EDITION SCOPE
These are the identified original published texts, not a comprehensive current consolidated legal library. The 2024 guidelines interpret the older flight regulation. Store document dates and type (legislation versus guidance). Do not label this prototype as up-to-date legal advice. Package-travel implementation and rail exemptions may require additional national sources.

INGESTION WORK STILL NEEDED
Check PDF column reading order and tables; repair hyphenation and remove recurring headers. Keep article/section identifiers alongside PDF pages. Raw publications include names in signatories and case references: remove unnecessary personal names from indexed text to satisfy the brief's no-personal-data constraint, retaining CELEX/ECLI identifiers for citations. These files are source material, not certified anonymized text.

ASSIGNMENT WORKFLOW
Choose a narrow user scenario within travel disruption. Read the sources and write your own 30+ questions before tuning retrieval, including 5+ multi-passage and 5+ unanswerable questions. Reserve one bus-specific question whose answer is absent from the core and demonstrably present in the holdout. Check this absence rather than assuming all bus questions are unanswerable: the package directive also discusses transport.
Compare two retrieval designs, record hit rates, and select based on results. Then build the required MCP tools and harness, run evaluation, and complete your own human grading and analysis. No test questions, evaluation scores or report conclusions are supplied here.
