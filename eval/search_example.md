# Search tool: descriptions and one real result

Called over MCP (stdio) against `server.py` on 2026-11-25, query: `flight cancelled less than 7 days before departure compensation`. For the report, the first passage in full and the other four by header is enough.

```text
### tool: search
Search the EU air passenger rights corpus and return the 5 most relevant passages.

    The corpus holds EU law for air passengers: Regulation (EC) 261/2004 (denied boarding,
    cancellations, long delays, upgrading/downgrading: compensation, refunds, re-routing,
    meals and hotels) and the Commission's 2024 interpretative guidelines on it;
    Regulation (EC) 2027/97 (airline liability for accidents and for lost, damaged or
    delayed baggage, Montreal Convention limits); Regulation (EC) 1107/2006 (rights of
    disabled passengers and passengers with reduced mobility) and its 2024 guidelines;
    plus any document added later with add_document.

    Use it for any question about what an air passenger is entitled to in the EU. Write the
    query in English, describing the passenger's situation or the legal concept. Call it
    again with a different query if the passages do not answer the question.

    Returns numbered passages, each with source_id, location (e.g. "Article 7",
    "Section 4.4.7", "Annex I"), a cosine similarity score (higher is closer), the document
    title, its URL and the passage text with its footnotes. Cite answers as source_id + location. If no passage covers the question,
    the corpus does not answer it.
    

### tool: add_document
Add one EUR-Lex HTML document to the corpus so that search can find it.

    `path` is a local .html file (absolute, or relative to the project folder), for
    example a regulation downloaded from EUR-Lex into corpus/. The file is parsed into
    articles, recitals, sections and annexes, cut into chunks the same way as the rest of
    the corpus, embedded and stored permanently in the index.

    Adding the same file again is safe: chunks already in the index are not embedded twice.
    Returns the new source_id, how many chunks were added and which sections they cover,
    or an error message if the file is missing, not HTML, or the embedding quota is spent.
    

### search result
[1] source_id: reg_261_2004 | location: Article 5 (part 1/2) | similarity: 0.780
sections: Article 5
document: Regulation (EC) No 261/2004 on compensation and assistance to air passengers (denied boarding, cancellation, long delay)
url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32004R0261
Article 5 – Cancellation
1. In case of cancellation of a flight, the passengers concerned shall:
(a) be offered assistance by the operating air carrier in accordance with Article 8; and
(b) be offered assistance by the operating air carrier in accordance with Article 9(1)(a) and 9(2), as well as, in event of re-routing when the reasonably expected time of departure of the new flight is at least the day after the departure as it was planned for the cancelled flight, the assistance specified in Article 9(1)(b) and 9(1)(c); and
(c) have the right to compensation by the operating air carrier in accordance with Article 7, unless:
(i) they are informed of the cancellation at least two weeks before the scheduled time of departure; or
(ii) they are informed of the cancellation between two weeks and seven days before the scheduled time of departure and are offered re-routing, allowing them to depart no more than two hours before the scheduled time of departure and to reach their final destination less than four hours after the scheduled time of arrival; or
(iii) they are informed of the cancellation less than seven days before the scheduled time of departure and are offered re-routing, allowing them to depart no more than one hour before the scheduled time of departure and to reach their final destination less than two hours after the scheduled time of arrival.
2. When passengers are informed of the cancellation, an explanation shall be given concerning possible alternative transport.
3. An operating air carrier shall not be obliged to pay compensation in accordance with Article 7, if it can prove that the cancellation is caused by extraordinary circumstances which could not have been avoided even if all reasonable measures had been taken.

---

[2] source_id: reg_261_2004 | location: Article 7 | similarity: 0.770
sections: Article 7
document: Regulation (EC) No 261/2004 on compensation and assistance to air passengers (denied boarding, cancellation, long delay)
url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32004R0261
Article 7 – Right to compensation
1. Where reference is made to this Article, passengers shall receive compensation amounting to:
(a) EUR 250 for all flights of 1500 kilometres or less;
(b) EUR 400 for all intra-Community flights of more than 1500 kilometres, and for all other flights between 1500 and 3500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the distance, the basis shall be the last destination at which the denial of boarding or cancellation will delay the passenger's arrival after the scheduled time.
2. When passengers are offered re-routing to their final destination on an alternative flight pursuant to Article 8, the arrival time of which does not exceed the scheduled arrival time of the flight originally booked
(a) by two hours, in respect of all flights of 1500 kilometres or less; or
(b) by three hours, in respect of all intra-Community flights of more than 1500 kilometres and for all other flights between 1500 and 3500 kilometres; or
(c) by four hours, in respect of all flights not falling under (a) or (b),
the operating air carrier may reduce the compensation provided for in paragraph 1 by 50 %.
3. The compensation referred to in paragraph 1 shall be paid in cash, by electronic bank transfer, bank orders or bank cheques or, with the signed agreement of the passenger, in travel vouchers and/or other services.
4. The distances given in paragraphs 1 and 2 shall be measured by the great circle route method.

---

[3] source_id: guidelines_261_2004 | location: Section 4.4.3 to Section 4.4.4 | similarity: 0.762
sections: Section 4.4.3; Section 4.4.4
document: Commission Interpretative Guidelines (2024) on Regulation 261/2004 and Regulation 2027/97
url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52024XC05687
Section 4.4.3 – Amount of compensation
The compensation is calculated in accordance with Article 7(1) of Regulation (EC) No 261/2004. It can be reduced by 50 % if the conditions of Article 7(2) are fulfilled.
C. Compensation in the event of cancellation
Section 4.4.4 – General case
Compensation is due in the event of cancellation:
— if passengers are not informed sufficiently in advance, i.e. at least 2 weeks before the scheduled departure, and
— if they are not re-routed within the time limits set out in Article 5(1), point (c), of Regulation (EC) No 261/2004 (see Section E),
— unless the cancellation is caused by extraordinary circumstances that could not have been avoided even if all reasonable measures had been taken, in accordance with Article 5(3) (see Section 5 on extraordinary circumstances).
It is important to note that this compensation is to be distinguished from the compensation for long delay at arrival.

---

[4] source_id: guidelines_261_2004 | location: Section 3.2.6 | similarity: 0.755
sections: Section 3.2.6
document: Commission Interpretative Guidelines (2024) on Regulation 261/2004 and Regulation 2027/97
url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52024XC05687
Section 3.2.6 – Rights associated with cancellation
Cancellation of a flight gives: (i) a right to reimbursement, re-routing or return as defined in Article 8 of Regulation (EC) No 261/2004; (ii) a right to ‘care’ as defined in Article 9; and (iii) under Article 5(1), point (c), a right to ‘compensation’ as defined in Article 7. The underlying principle of Article 5(1), point (c), is that compensation is to be paid if the passenger has not been informed of the cancellation sufficiently in advance.
However, compensation does not have to be paid if the air carrier can prove, in accordance with Article 5(3), that the cancellation is caused by extraordinary circumstances that could not have been avoided even if all reasonable measures had been taken [63] .

Footnotes:
[63] See Section 5 on extraordinary circumstances.

---

[5] source_id: guidelines_261_2004 | location: Section 6.4 (part 1/2) | similarity: 0.753
sections: Section 6.4
document: Commission Interpretative Guidelines (2024) on Regulation 261/2004 and Regulation 2027/97
url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52024XC05687
Section 6.4 – Right to compensation
The right to compensation for cancellation pursuant to Article 5(1) and Article 7 of Regulation (EC) No 261/2004 does not apply in the case of cancellations made more than 14 days in advance or if the cancellation is caused by extraordinary circumstances that could not have been avoided even if all reasonable measures had been taken by the air carrier.
The Commission considers that, if public authorities take measures intended to contain the effects of a crisis situation leading to massive travel disruptions, such measures are by their nature and origin not inherent in the normal exercise of the activity of air carriers and are outside their actual control.
Article 5(3) waives the right to compensation on condition that the cancellation in question ‘is caused’ by extraordinary circumstances that could not have been avoided even if all reasonable measures had been taken.
This condition should be considered fulfilled if public authorities either prohibit certain flights or restrict the movement of people in a manner that de facto excludes the operation of the flight in question.
This condition may also be fulfilled if the flight cancellation occurs in circumstances in which the corresponding movement of people is not entirely prohibited but limited to people benefiting from derogations (for example nationals or residents of the state concerned).
```
