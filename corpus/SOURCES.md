# Corpus sources

All documents are publications of the **National Institute of Standards and Technology (NIST), U.S. Department of Commerce**. Credit: NIST.

All five were downloaded on **2026-11-23** from `nvlpubs.nist.gov`. All are in English.

## Licence

NIST publications are works of the U.S. Government. Under 17 U.S.C. § 105 they are not subject to copyright in the United States. Where NIST holds rights outside the U.S., it grants permission to reprint its publications worldwide. See NIST's *Copyright, Use, and Licensing Statements* (<https://www.nist.gov/oism/copyrights>), which each document links to in its front matter. This project downloads, extracts, chunks and embeds the text for a non-commercial assignment and cites every passage it returns. No document has been modified, and no endorsement by NIST is implied.

**Caveat about outside co-authors.** Section 105 covers only work by U.S. Government employees. Some of these publications list a co-author from an outside firm. Both SP 800-61r3 and SP 800-218 name Karen Scarfone of Scarfone Cybersecurity. That co-author's contribution may not be a U.S. Government work in the strict sense. This project relies on NIST publishing these documents openly, under its own copyright and licensing statements, and on its reprint permission. Confirm this against NIST's statement before redistributing the PDFs. This project does not commit them.

## Indexed documents

| # | File (`corpus/raw/`) | Document | Version / date | URL | PDF pages | Words (raw → cleaned) |
|---|---|---|---|---|---|---|
| 1 | `NIST.AI.100-1.pdf` | NIST AI 100-1, *Artificial Intelligence Risk Management Framework (AI RMF 1.0)* | 1.0, January 2023 | <https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf> (doi:10.6028/NIST.AI.100-1) | 48 | 15,911 → 14,881 |
| 2 | `NIST.AI.600-1.pdf` | NIST AI 600-1, *AI RMF: Generative Artificial Intelligence Profile* | July 2024 | <https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf> (doi:10.6028/NIST.AI.600-1) | 64 | 21,019 → 18,732 |
| 3 | `NIST.SP.800-61r3.pdf` | NIST SP 800-61 Rev. 3, *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile* | Revision 3, April 2025 | <https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-61r3.pdf> (doi:10.6028/NIST.SP.800-61r3) | 48 | 14,227 → 12,113 |
| 4 | `NIST.SP.800-218.pdf` | NIST SP 800-218, *Secure Software Development Framework (SSDF) Version 1.1: Recommendations for Mitigating the Risk of Software Vulnerabilities* | Version 1.1, February 2022 | <https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-218.pdf> (doi:10.6028/NIST.SP.800-218) | 36 | 14,282 → 12,015 |
| | | **Indexed total** | | | 196 | **65,439 → 57,741** |

## Held out (added later through the add-document tool)

| # | File (`corpus/holdout/`) | Document | Version / date | URL | PDF pages | Words (raw → cleaned) |
|---|---|---|---|---|---|---|
| 5 | `NIST.CSWP.29.pdf` | NIST CSWP 29, *The NIST Cybersecurity Framework (CSF) 2.0* | 2.0, February 26, 2024 | <https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf> (doi:10.6028/NIST.CSWP.29) | 32 | 9,468 → 8,703 |

## Pages removed in cleaning

Page numbers below are PDF page indices, starting at 1, not the printed page numbers. These pages are removed because they hold personal data (names of authors, contributors and officials, and ORCID iDs) or carry no content.

- **AI 100-1:** p1 cover, p2 title page, p4 table of contents, p5 lists of figures and tables, p48 back cover.
- **AI 600-1:** p1 cover, p2 title page, p3 "About" and acknowledgments (names staff), p4 table of contents, p58–64 Appendix B References. The named acknowledgments paragraph at the start of Appendix A (p51) is also cut out; the rest of that page is kept.
- **SP 800-61r3:** p1 cover, p2 title page (authors), p3 legal notices, p4 author ORCID iDs, p7 patent notice, p8 table of contents, p44–45 References.
- **SP 800-218:** p1 cover, p2 title page (authors and officials), p3 legal notices, p7 patent notice, p9 table of contents, p29–32 References. The Acknowledgments section on p5 is also cut out, because it names NIST staff and an individual commenter. The Audience section on that page is kept. The running header and the "available free of charge" line on each page are removed. The *References* column inside Table 1 (mappings such as `BSIMM: CP1.1`) is kept, because it is part of the practice table.
- **CSWP 29:** p1 cover, p3 acknowledgments, p4 table of contents, p32 colophon.

## Checksums (SHA-256 of the downloaded PDFs)

```
7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1  raw/NIST.AI.100-1.pdf
6e73620ab6b64e90ef2c04bf0e0d6246185a2f4b1b13cab0df494496cff89b6a  raw/NIST.AI.600-1.pdf
e5593d6bb85daecec7e8d9549400c7b3473bcc3f06e469c82218073afa7fba2d  raw/NIST.SP.800-61r3.pdf
617746e553a9e2da49bfbd4eef0dfc3094758a39b869314e4173ac36605cde22  raw/NIST.SP.800-218.pdf
3c31f46fee98cac0c4323453e5109291a213b4de7fef8c058af9bf67f717433c  holdout/NIST.CSWP.29.pdf
```
