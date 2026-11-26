# Corpus attribution and reuse notices

This is a noncommercial academic RAG experiment. Corpus text retains its source
licensing; the software's licence does not override it. Downloaded PDFs/HTML and
cleaned Markdown live in the ignored `corpus/` directory. Saved index chunks also
contain source text, so retain this notice when sharing the index.

## Introduction to Operations Management (`operations`)

Mary Drane and Hamid Faramarzi / Seneca College; adapted and curated by LibreTexts.
Source: https://biz.libretexts.org/Bookshelves/Management/Introduction_to_Operations_Management
PDF snapshot compiled 5 May 2026. Detailed per-page licensing appears on PDF pages
135–138: CC BY-NC 4.0 on the included content. Source acknowledgements also describe
its adaptation history; retain those original credits. Licence:
https://creativecommons.org/licenses/by-nc/4.0/

Included: text from PDF pages 9–134. Excluded: front matter and undeclared-licence
contents pages, duplicated licensing lists, images and video content. Changes:
PDF text extraction, removal of recurring page/URL headers, whitespace and ligature
normalisation, and segmentation with explicit original PDF-page markers. This
licence restricts commercial reuse; the academic corpus is not cleared for a
commercial retail deployment.

## Supply Chain Resilience Guide (`fema`)

Federal Emergency Management Agency, April 2019.
Source: https://www.fema.gov/sites/default/files/2020-07/supply-chain-resilience-guide.pdf
Reuse basis: U.S. government-authored publication, generally public domain in the
United States. General explanation:
https://www.loc.gov/legal/security-copyright-and-privacy/understanding-copyright/
Third-party images, logos and linked publications are not ingested or relicensed.
Changes: text extraction, repeated-header removal, whitespace normalisation and
original PDF-page markers. The intended audience is emergency managers. No FEMA
endorsement is implied.

## Critical imports and supply chains strategy (`uk-strategy`)

Department for Business and Trade, published 17 January 2024. Crown copyright.
Source: https://www.gov.uk/government/publications/uk-critical-imports-and-supply-chains-strategy/critical-imports-and-supply-chains-strategy-html-version
The source page states Open Government Licence v3.0, except where otherwise stated:
https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
Changes: article-text extraction, removal of website navigation/images/scripts,
whitespace normalisation and hierarchical section markers. Linked publications
and third-party images are excluded. No government endorsement is implied.

## Scope and reproducibility

`prepare_corpus.py` records source URLs, snapshot SHA-256 hashes, extraction
changes, counts and scope in `corpus/SOURCES.json`. Count only the cleaned text,
not markers, duplicated overlap or attribution notices. Public bibliographic
names may remain; no private customer, employee, order or shipment data are used.
The corpus contains dated guidance, not current supplier or carrier status.

## Prepared addition: SBA overview (`sba`, not indexed in the baseline)

U.S. Small Business Administration, Business Resilience Guide, July 2025:
https://legacy.sba.gov/sites/default/files/2025-07/Business%20Resilience%20Guide.2025.pdf
Only introductory PDF page 1 is included in corpus/sba.md. Text extraction and
whitespace normalisation preserve its original page marker. The page describes
the guide's organisation. Material contributed by third-party partners elsewhere
in the guide, images and logos are excluded. Reuse basis: federal government
overview text, generally public domain in the U.S.; no endorsement implied.
This file is registered as an optional addition and is not part of the three
baseline documents or their 57,121-word count. The addition experiment awaits
its separate approval step.

Upstream attribution: the Seneca text acknowledges adaptations of Understanding Operations Management (The Open University) and Operations Management (Saylor). Original upstream notices continue to apply; this project does not relicense source text.
