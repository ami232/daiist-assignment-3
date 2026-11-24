# Extraction problems log

Written by index.py on 2026-11-24. Counts are per document.

| Problem | Status | Dir_2016_797 | Dir_2016_798 | Reg_1299_2014 | Reg_2019_779 |
|---|---|---|---|---|---|
| Official Journal page header table (date, 'EN', 'Official Journal of the European Union', page number) removed | fixed | 1 | 1 | 1 | 1 |
| table-of-contents rows removed (they repeat every section heading plus a page number and would match any query about a heading) | fixed | 0 | 0 | 118 | 0 |
| footnote markers '(1)' in running text removed, with the stray space they leave before punctuation | fixed | 17 | 17 | 13 | 11 |
| footnotes that are only Official Journal references dropped (they sit at the end of the act, far from their anchor) | fixed | 17 | 17 | 12 | 11 |
| substantive footnotes (e.g. table notes) kept: marker rewritten as '[note N]' and the note text placed right after the paragraph or table that cites it | fixed | 0 | 0 | 26 | 0 |
| signature block lines ('For the Council', 'The President', names) and 'Done at ...' removed | fixed | 7 | 7 | 4 | 4 |
| 'Whereas:' / 'HAS ADOPTED THIS ...' formula lines removed | fixed | 2 | 2 | 2 | 2 |
| list items rebuilt: EUR-Lex lays out every '(a) text' item as a two-cell table, which plain text extraction returns as a bare marker followed by an orphaned sentence | fixed | 300 | 305 | 699 | 191 |
| data tables written one row per line as 'cell | cell | cell' | fixed | 3 | 3 | 53 | 0 |
| row-spanning / column-spanning cells repeated on every row they cover, so each row is readable alone | fixed | 0 | 0 | 44 | 0 |
| table-note rows taken out of the table body (their text is attached as notes instead) | fixed | 0 | 0 | 1 | 0 |
| figures / forms that are images: the drawing is lost, replaced by an '[image not extracted]' placeholder | limitation | 0 | 0 | 16 | 7 |
| of those images, the ones with a hidden 'Text of image' transcription in the HTML: transcription kept and labelled '[text shown in the image:]' | fixed | 0 | 0 | 4 | 7 |
| formulas that exist only as images: replaced by a '[formula not extracted]' placeholder, content lost | limitation | 0 | 0 | 6 | 0 |
| sub/superscripts kept distinct ('b_qlim', 'm^2') instead of being flattened to 'b qlim', 'm 2' | fixed | 0 | 10 | 39 | 0 |
| non-breaking spaces normalised to plain spaces (e.g. '1.   Each vehicle') | fixed | 1075 | 805 | 1842 | 521 |
| numbers written with a space as thousands separator ('1 435 mm') kept as printed; they count as two words | note | 1 | 1 | 296 | 0 |
| sections that are only a heading (parents of sub-sections): no chunk of their own, the heading is kept in the title of their children | note | 17 | 3 | 48 | 3 |

## Examples

- **sub_superscripts_fixed**: `subscript 'P' -> '_P'` ;; `subscript 'F' -> '_F'` ;; `superscript '2' -> '^2'`
