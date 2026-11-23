# Assignment 3 Report

- **Name**:
- **Student ID**:
- **Group**: [BBADBA 5A | BBADBA 5B | PPLEDBA 5A]

## Use case

**Who asks:** an airline safety analyst who prepares case-study briefings for recurrent pilot training (CRM and flight-path management modules).

**What they do with the answer:** say the training team is building a session on how crews notice and respond to decaying airspeed. The analyst asks, *"What did the NTSB find about airspeed monitoring in Colgan 3407 and Asiana 214, and what did it recommend after each?"* The assistant gathers the findings, probable causes and recommendations from the reports and cites the PDF page of each claim. The analyst checks each citation and picks which lessons go onto the training slides.

**What a wrong answer costs compared with "I don't know":** a wrong answer is costly because it can end up in training material that many pilots see, and from there it is hard to correct. The errors that matter most:
- **Category errors.** Calling a contributing factor the probable cause, or the other way round. In Colgan 3407, failing to monitor airspeed was a *contributing factor*; in Asiana 214, inadequate airspeed monitoring was *part of the probable cause*.
- **Status errors.** Presenting an NTSB *recommendation* as an FAA *requirement*.
- **Changed numbers.** Altered altitudes, speeds or recommendation numbers.

"I don't know" costs only time: the analyst checks the report or another source, such as the NTSB recommendation-status records or FAA rulemaking. So the assistant must cite every claim and say plainly when the reports do not cover a question. That includes anything that happened after a report was published, which these reports cannot contain.

> This tool helps airline safety analysts prepare case-study briefings for recurrent pilot training. Analysts use it to compare findings, probable causes and safety recommendations across NTSB accident reports, and to check each claim against the original page. An unsupported answer could carry an error into training materials, so the assistant says when the reports do not contain enough evidence to answer.

**Out of scope:** what happened after a report was published (recommendation status, FAA rules, airline actions), accidents not in the corpus, and operational advice to pilots.

## Corpus

Three full NTSB aircraft accident reports. All three accidents involve airspeed or energy management, crew monitoring and emergency handling, so they support comparisons. US government works are in the public domain (17 U.S.C. §105), and the reports contain no personal data beyond the crews' professional histories, which the reports publish. `index.py` downloads them into `corpus/` (git-ignored).

| Document | Accident | URL | Date | Licence | PDF pages | Words indexed |
|---|---|---|---|---|---|---|
| NTSB/AAR-10/01 (AAR1001) | Colgan Air 3407, loss of control on approach, Buffalo, 12 Feb 2009 | https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR1001.pdf | 2 Feb 2010 | Public domain | 299 | WORDS_AAR1001 |
| NTSB/AAR-10/03 (AAR1003) | US Airways 1549, dual bird strike and Hudson River ditching, 15 Jan 2009 | https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR1003.pdf | 4 May 2010 | Public domain | 213 | WORDS_AAR1003 |
| NTSB/AAR-14/01 (AAR1401) | Asiana 214, descent below glidepath into the seawall, San Francisco, 6 Jul 2013 | https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR1401.pdf | 24 Jun 2014 | Public domain | 207 | WORDS_AAR1401 |
| **Total** | | | | | **719** | **WORDS_TOTAL** (about 261,000 before removing the contents and abbreviation pages) |

## Ingestion

- **Extract:** `pypdf`, one page at a time, so every chunk knows its PDF page.
- **Extraction problem fixed:** pypdf's default mode splits words in these PDFs, for example "th eir", "adequa te", "tim e" and "go -around". A keyword check for "go-around" on the Asiana findings page failed for that reason. Switching to `extraction_mode="layout"` keeps the words whole.
- **Clean:**
  - Remove the running header "NTSB Aircraft Accident Report" and the page-number lines, keeping the printed number as metadata, since PDF page 165 is printed page 151.
  - Rejoin words hyphenated across lines.
  - Fix ligatures.
  - Drop front matter: table-of-contents pages (detected by dot leaders), lists of figures and the abbreviation lists, about 31 pages in all.
- **Chunk (two designs, both about 350 words):**
  - **`fixed`:** sliding windows of 350 words with a 50-word overlap, ignoring the report's structure.
  - **`sections`:** detects the NTSB's numbered headings ("1.1 History of Flight", "3.1 Findings", "4.1 New Recommendations") and never crosses one. Whole paragraphs are packed up to 350 words, and a longer paragraph is split at sentence ends. Each chunk is embedded with a header line, "report title | section", so a passage from *3.2 Probable Cause* carries that label into its vector.
- **Metadata per chunk:** `doc_id`, `section`, `page_start`, `page_end` (PDF pages), `printed_start`, `printed_end`, `title`, `words`, `design`.
- **Embedding:** `gemini-embedding-2`, 768 dimensions, normalised, stored in ChromaDB (`index/chroma`, cosine). The chunk id is a hash of the embedded text, and each batch of 20 is stored as soon as it returns, so a re-run embeds only what is missing.
- **Two pitfalls handled:**
  - Passing a plain list of strings to `gemini-embedding-2` returns *one* vector for the whole list, so each text is sent as its own `Content`.
  - The free tier's daily limit made us index over two days.
- **Chunk counts:** CHUNKS_SECTIONS (`sections`) and CHUNKS_FIXED (`fixed`) for the three reports.

## Test set

- **37 questions:** 24 single, 7 multi (two reports or two passages), 6 unanswerable.
- **How they were written:** from reading the reports, mainly the findings, probable-cause and recommendation sections, which are what an analyst briefs from, with 4 from the executive summary and factual body. Each answerable question has its PDF page, checked against the extracted text.
- **The unanswerable questions** stay on topic. They ask what happened *after* a report was published (recommendation closure dates, FAA rules, airline training costs), or about an accident that is not in the corpus (Atlas Air 3591).
- **Two questions test the errors named in the use case:**
  - q31, probable cause vs contributing factor.
  - q35, which asks for an FAA rule when the report contains only an NTSB recommendation.

Examples:
- *q31 (multi):* "Was the crew's airspeed monitoring part of the probable cause or only a contributing factor in Colgan 3407, and in Asiana 214?" → AAR1001 p.169 (contributing factor) and AAR1401 p.147 (part of the probable cause).
- *q27 (unanswerable):* "On what date did the NTSB close recommendation A-10-66…?" The report states the recommendation but not its later status, so the assistant should say the reports do not cover it.

## Retrieval

*Hit rate at 1/3/5 per design, words added to the prompt, the design you chose.*

## Tools and subagent

*Your tools' descriptions, one search result, the subagent's instructions, one transcript from your editor.*

## Adding a document

*What happens when a document is already indexed. The unanswerable question, the document you added, the answer before and after.*

## Harness and guardrails

*Your AGENTS.md rules, the approval step, and your extra guardrail with one case where it fired.*

## Evaluation

*Code checks, the judge's rubric, your agreement with the judge, and results: correct, unsupported, correct refusals, wrong refusals.*

## Failures

*Failed questions by cause, with counts, and what to fix first.*

## Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

## AI use

*What you used and how, or "none".*
