# Blind grading sheet

Grade each answer before opening eval/results.json or eval/verdicts.jsonl (they hold the judge's verdicts).
Write your grades in eval/human_labels.csv as `id,correct,supported,notes` with 1/0, and a note for every 0.
`correct`: right against the reference, or a proper refusal. `supported`: every claim is in the passages below.

## q01 (single)

**Question:** How much compensation does EU law give for a cancelled flight of 1,500 km or less?

**Reference:** EUR 250 per passenger (Art. 7(1)(a)); it may be cut by 50% if re-routing arrives within 2 hours of the original arrival time, and it is not owed where the cancellation exceptions in Art. 5 apply.

**Answer shown to the user:**

> For a cancelled flight of 1,500 kilometres or less, EU law provides standard compensation of **EUR 250** [32004R0261:A:w016:1].
> 
> However, this amount is subject to specific conditions, reductions, and exceptions:
> 
> * **Notice period:** You are not entitled to compensation if you are informed of the cancellation at least two weeks before the scheduled time of departure, or within specific shorter notice windows if you are offered alternative re-routing that meets strict timing criteria [32004R0261:A:w014:1].
> * **Re-routing arrival time:** The operating air carrier may reduce the compensation by 50% (to EUR 125) if you are offered re-routing to your final destination on an alternative flight whose arrival time does not exceed the scheduled arrival time of the original flight by more than two hours [32004R0261:A:w017:1].
> * **Extraordinary circumstances:** The carrier is not obliged to pay compensation if it can prove that the cancellation is caused by extraordinary circumstances that could not have been avoided even if all reasonable measures had been taken [32004R0261:A:w015:1].
> 
> *Note: This information is based on Regulation (EC) No 261/2004 [32004R0261:A:w017:1] and is provided for informational purposes rather than as legal advice.*

<details><summary>Passages the agent retrieved</summary>

```text
[32004R0261:A:w017:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 7, PDF p. 5 | similarity 0.795
(b) EUR 400 for all intra-Community flights of more than
1 500 kilometres, and for all other flights between 1 500
and 3 500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the distance, the basis shall be the last destination
at which the denial of boarding or cancellation will delay
the passenger's arrival after the scheduled time.
2. When passengers are offered re-routing to their final
destination on an alternative flight pursuant to Article 8, the
arrival time of which does not exceed the scheduled arrival
time of the flight originally booked
(a) by two hours, in respect of all flights of 1 500 kilometres
or less; or
(b) by three hours, in respect of all intra-Community flights of
more than 1 500 kilometres and for all other flights
between 1 500 and 3 500 kilometres; or
(c) by four hours, in respect of all flights not falling under (a)
or (b),
the operating air carrier may reduce the compensation
provided for in paragraph 1 by 50 %.
3. The compensation referred to in paragraph 1 shall be
paid in cash, by electronic bank transfer, bank orders or bank
cheques or, with
```
```text
[32004R0261:A:w014:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 5, PDF p. 4 | similarity 0.769
in event of re-routing
when the reasonably expected time of departure of
the new flight is at least the day after the departure as it
was planned for the cancelled flight, the assistance specified
in Article 9(1)(b) and 9(1)(c); and
(c) have the right to compensation by the operating air carrier
in accordance with Article 7, unless:
(i) they are informed of the cancellation at least two
weeks before the scheduled time of departure; or
(ii) they are informed of the cancellation between two
weeks and seven days before the scheduled time of
departure and are offered re-routing, allowing them to
depart no more than two hours before the scheduled
time of departure and to reach their final destination
less than four hours after the scheduled time of arrival;
or
(iii) they are informed of the cancellation less than seven
days before the scheduled time of departure and are
offered re-routing, allowing them to depart no more
than one hour before the scheduled time of departure
and to reach their final destination less than two hours
after the scheduled time of arrival.
2. When passengers are informed of the cancellation, an
explanation shall be given concerning possible alternative transport
.
```
```text
[32004R0261:A:w015:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 5 to Article 6, PDF p. 4 | similarity 0.761
before the scheduled time of departure
and to reach their final destination less than two hours
after the scheduled time of arrival.
2. When passengers are informed of the cancellation, an
explanation shall be given concerning possible alternative transport
.
3. An operating air carrier shall not be obliged to pay
compensation in accordance with Article 7, if it can prove that
the cancellation is caused by extraordinary circumstances
which could not have been avoided even if all reasonable
measures had been taken.
4. The burden of proof concerning the questions as to
whether and when the passenger has been informed of the
cancellation of the flight shall rest with the operating air
carrier.
Article 6
Delay
1. When an operating air carrier reasonably expects a flight
to be delayed beyond its scheduled time of departure:
(a) for two hours or more in the case of flights of 1 500 kilometres
or less; or
(b) for three hours or more in the case of all intra-Community
flights of more than 1 500 kilometres and of all other
flights between 1 500 and 3 500 kilometres; or
(c) for four hours or more in the case of all flights not falling
```
```text
[52024XC05687:A:w095:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 6.4, PDF p. 30 | similarity 0.751
The right to compensation for cancellation pursuant to Article 5(1) and Article 7 of Regulation (EC) No 261/2004 does not
apply in the case of cancellations made more than 14 days in advance or if the cancellation is caused by extraordinary
circumstances that could not have been avoided even if all reasonable measures had been taken by the air carrier.
The Commission considers that, if public authorities take measures intended to contain the effects of a crisis situation
leading to massive travel disruptions, such measures are by their nature and origin not inherent in the normal exercise of
the activity of air carriers and are outside their actual control.
Article 5(3) waives the right to compensation on condition that the cancellation in question ‘is caused’ by extraordinary
circumstances that could not have been avoided even if all reasonable measures had been taken.
This condition should be considered fulfilled if public authorities either prohibit certain flights or restrict the movement of
people in a manner that de facto excludes the operation of the flight in question.
This condition may also be fulfilled if the flight cancellation occurs in circumstances in which the corresponding movement
of people is not entirely prohibited but
```
```text
[32004R0261:A:w016:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 6 to Article 7, PDF pp. 4-5 | similarity 0.748
in the case of all intra-Community
flights of more than 1 500 kilometres and of all other
flights between 1 500 and 3 500 kilometres; or
(c) for four hours or more in the case of all flights not falling
under (a) or (b),
passengers shall be offered by the operating air carrier:
(i) the assistance specified in Article 9(1)(a) and 9(2); and
(ii) when the reasonably expected time of departure is at least
the day after the time of departure previously announced,
the assistance specified in Article 9(1)(b) and 9(1)(c); and
(iii) when the delay is at least five hours, the assistance specified
in Article 8(1)(a).
2. In any event, the assistance shall be offered within the
time limits set out above with respect to each distance bracket.
Article 7
Right to compensation
1. Where reference is made to this Article, passengers shall
receive compensation amounting to:
(a) EUR 250 for all flights of 1 500 kilometres or less;
(b) EUR 400 for all intra-Community flights of more than
1 500 kilometres, and for all other flights between 1 500
and 3 500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the
```

</details>

## q02 (single)

**Question:** My flight is delayed at departure by more than five hours and I no longer want to travel. Can I get my ticket refunded?

**Reference:** Yes. For a delay of at least five hours the airline must offer the assistance in Art. 8(1)(a): reimbursement of the ticket (and a return flight where relevant) (Art. 6(1)(iii)).

**Answer shown to the user:**

> Yes. Under EU air passenger rights texts, if your flight is delayed at departure by **at least five hours**, you are entitled to be offered reimbursement of your ticket [32004R0261:A:w016:1, 32004R0261:A:w018:1].
> 
> ### What the rules say
> * **Reimbursement (Refund):** When the departure delay reaches at least five hours, the carrier must offer you the assistance specified in Article 8(1)(a) [32004R0261:A:w016:1]. This gives you the choice of getting a refund of the full cost of your ticket at the price it was bought [32004R0261:A:w018:1]:
>   * for the part or parts of the journey not made, and
>   * for the part or parts already made, if the flight is no longer serving any purpose in relation to your original travel plan (plus, if relevant, a return flight to your first point of departure at the earliest opportunity) [32004R0261:A:w018:1].
> * **Timeframe:** If you choose reimbursement, the carrier must pay it within seven days, by cash, electronic bank transfer, bank order, or bank cheque (or in travel vouchers/services, but only with your signed agreement) [32004R0261:A:w018:1].
> * **Care:** While waiting for the departure of a delayed flight, you also have the right to care (such as meals and refreshments in a reasonable relation to waiting time) depending on the distance bracket of your flight [32004R0261:A:w016:1, 32004R0261:A:w019:1].
> 
> *Note: This information is based on Regulation (EC) No 261/2004 and the Commission interpretative guidelines, not legal advice for your specific case.*

<details><summary>Passages the agent retrieved</summary>

```text
[32004R0261:A:w015:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 5 to Article 6, PDF p. 4 | similarity 0.751
before the scheduled time of departure
and to reach their final destination less than two hours
after the scheduled time of arrival.
2. When passengers are informed of the cancellation, an
explanation shall be given concerning possible alternative transport
.
3. An operating air carrier shall not be obliged to pay
compensation in accordance with Article 7, if it can prove that
the cancellation is caused by extraordinary circumstances
which could not have been avoided even if all reasonable
measures had been taken.
4. The burden of proof concerning the questions as to
whether and when the passenger has been informed of the
cancellation of the flight shall rest with the operating air
carrier.
Article 6
Delay
1. When an operating air carrier reasonably expects a flight
to be delayed beyond its scheduled time of departure:
(a) for two hours or more in the case of flights of 1 500 kilometres
or less; or
(b) for three hours or more in the case of all intra-Community
flights of more than 1 500 kilometres and of all other
flights between 1 500 and 3 500 kilometres; or
(c) for four hours or more in the case of all flights not falling
```
```text
[32004R0261:A:w016:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 6 to Article 7, PDF pp. 4-5 | similarity 0.770
in the case of all intra-Community
flights of more than 1 500 kilometres and of all other
flights between 1 500 and 3 500 kilometres; or
(c) for four hours or more in the case of all flights not falling
under (a) or (b),
passengers shall be offered by the operating air carrier:
(i) the assistance specified in Article 9(1)(a) and 9(2); and
(ii) when the reasonably expected time of departure is at least
the day after the time of departure previously announced,
the assistance specified in Article 9(1)(b) and 9(1)(c); and
(iii) when the delay is at least five hours, the assistance specified
in Article 8(1)(a).
2. In any event, the assistance shall be offered within the
time limits set out above with respect to each distance bracket.
Article 7
Right to compensation
1. Where reference is made to this Article, passengers shall
receive compensation amounting to:
(a) EUR 250 for all flights of 1 500 kilometres or less;
(b) EUR 400 for all intra-Community flights of more than
1 500 kilometres, and for all other flights between 1 500
and 3 500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the
```
```text
[32004R0261:A:w014:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 5, PDF p. 4 | similarity 0.746
in event of re-routing
when the reasonably expected time of departure of
the new flight is at least the day after the departure as it
was planned for the cancelled flight, the assistance specified
in Article 9(1)(b) and 9(1)(c); and
(c) have the right to compensation by the operating air carrier
in accordance with Article 7, unless:
(i) they are informed of the cancellation at least two
weeks before the scheduled time of departure; or
(ii) they are informed of the cancellation between two
weeks and seven days before the scheduled time of
departure and are offered re-routing, allowing them to
depart no more than two hours before the scheduled
time of departure and to reach their final destination
less than four hours after the scheduled time of arrival;
or
(iii) they are informed of the cancellation less than seven
days before the scheduled time of departure and are
offered re-routing, allowing them to depart no more
than one hour before the scheduled time of departure
and to reach their final destination less than two hours
after the scheduled time of arrival.
2. When passengers are informed of the cancellation, an
explanation shall be given concerning possible alternative transport
.
```
```text
[52024XC05687:A:w034:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 3.2.6 to Section 3.3.2, PDF p. 13 | similarity 0.733
to be paid if the air carrier can prove, in accordance with Article 5(3), that the
cancellation is caused by extraordinary circumstances that could not have been avoided even if all reasonable measures had
been taken (63).
3.3. Delay
3.3.1. Delay at departure
Under Article 6(1) of Regulation (EC) No 261/2004, if the departure of a flight is delayed, passengers affected by this delay
have the right to ‘care’ according to Article 9, and to reimbursement and a return flight according to Article 8(1), point (a).
The underlying principle of Article 6(1) is that the rights depend on the duration of the delay and the distance of the flight.
In this regard, it should be noted that the right to re-routing as laid down in Article 8(1), point (b), is not covered under
Article 6(1) as it can be considered that the air carrier is trying, in the first place, to address the cause of the delay in order
to minimise the inconvenience to the passengers.
3.3.2. ‘Long delay’ at arrival
The Court has ruled that a delay at arrival of at least 3 hours gives the same rights in terms of compensation as a
cancellation (64) (for more details,
Notes: (63) See Section 5 on extraordinary circumstances. (64) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 69. See also Joined Cases C-581/10 and C-629/10, ECLI:EU:C:2012:657, paragraph 40, and Case C-413/11, ECLI:EU:C:2013:246, paragraph 19.
```
```text
[32004R0261:A:w019:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 8 to Article 9, PDF p. 5 | similarity 0.780
— a return flight to the first point of departure, at the
earliest opportunity;
(b) re-routing, under comparable transport conditions, to their
final destination at the earliest opportunity; or
(c) re-routing, under comparable transport conditions, to their
final destination at a later date at the passenger's convenience
, subject to availability of seats.
2. Paragraph 1(a) shall also apply to passengers whose
flights form part of a package, except for the right to reimbursement
where such right arises under Directive 90/314/EEC.
3. When, in the case where a town, city or region is served
by several airports, an operating air carrier offers a passenger a
flight to an airport alternative to that for which the booking
was made, the operating air carrier shall bear the cost of transferring
the passenger from that alternative airport either to that
for which the booking was made, or to another close-by destination
agreed with the passenger.
Article 9
Right to care
1. Where reference is made to this Article, passengers shall
be offered free of charge:
(a) meals and refreshments in a reasonable relation to the
waiting time;
(b) hotel accommodation in cases
— where a stay of one or more nights becomes necessary,
```
```text
[32004R0261:A:w018:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 7 to Article 8, PDF p. 5 | similarity 0.781
the operating air carrier may reduce the compensation
provided for in paragraph 1 by 50 %.
3. The compensation referred to in paragraph 1 shall be
paid in cash, by electronic bank transfer, bank orders or bank
cheques or, with the signed agreement of the passenger, in
travel vouchers and/or other services.
4. The distances given in paragraphs 1 and 2 shall be
measured by the great circle route method.
Article 8
Right to reimbursement or re-routing
1. Where reference is made to this Article, passengers shall
be offered the choice between:
(a) — reimbursement within seven days, by the means
provided for in Article 7(3), of the full cost of the ticket
at the price at which it was bought, for the part or
parts of the journey not made, and for the part or parts
already made if the flight is no longer serving any
purpose in relation to the passenger's original travel
plan, together with, when relevant,
— a return flight to the first point of departure, at the
earliest opportunity;
(b) re-routing, under comparable transport conditions, to their
final destination at the earliest opportunity; or
(c) re-routing, under comparable transport conditions, to their
final destination at
```

</details>

## q03 (single)

**Question:** What care must the airline give me free of charge while I wait for a delayed or cancelled flight?

**Reference:** Meals and refreshments in reasonable relation to the waiting time, hotel accommodation when a stay of one or more nights (or an extra stay) becomes necessary, transport between airport and accommodation, and two telephone calls, emails, telexes or faxes (Art. 9).

**Answer shown to the user:**

> WITHHELD: the harness blocked this answer because it cites passages that search did not return: 32004R0261:A:w020:2.

<details><summary>Passages the agent retrieved</summary>

```text
[32004R0261:A:w020:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 9 to Article 10, PDF p. 5 | similarity 0.777
is made to this Article, passengers shall
be offered free of charge:
(a) meals and refreshments in a reasonable relation to the
waiting time;
(b) hotel accommodation in cases
— where a stay of one or more nights becomes necessary,
or
— where a stay additional to that intended by the
passenger becomes necessary;
(c) transport between the airport and place of accommodation
(hotel or other).
2. In addition, passengers shall be offered free of charge two
telephone calls, telex or fax messages, or e-mails.
3. In applying this Article, the operating air carrier shall pay
particular attention to the needs of persons with reduced mobility
and any persons accompanying them, as well as to the
needs of unaccompanied children.
Article 10
Upgrading and downgrading
1. If an operating air carrier places a passenger in a class
higher than that for which the ticket was purchased, it may not
request any supplementary payment.
2. If an operating air carrier places a passenger in a class
lower than that for which the ticket was purchased, it shall
within seven days, by the means provided for in Article 7(3),
reimburse
(a) 30 % of the price of the ticket for all flights
```
```text
[52024XC05687:A:w055:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.3.2, PDF pp. 18-19 | similarity 0.781
and the time of day (or night) at which it occurs, including at the
transfer airport in the case of connecting flights, in order to reduce the inconvenience suffered by the passengers as much
as possible, while bearing in mind the principle of proportionality. Particular attention has to be given to the needs of
people with a disability or reduced mobility and unaccompanied children.
Furthermore, passengers should be offered care free of charge in a clear and accessible way, including, where possible, via
electronic means of communication. This means that passengers should not be left to make arrangements themselves, e.g.
finding and paying for accommodation or food. Instead, operating air carriers are obliged to actively offer care. Operating
air carriers should also ensure, where available, that accommodation is accessible for people with a disability and their
service dogs.
If care has not been offered even though it should have been, passengers who have had to pay for meals and refreshments,
hotel accommodation, transport between the airport and the place of accommodation and/or telecommunication services
can obtain reimbursement of the expenses incurred from the air carrier, if these were necessary, reasonable and
appropriate (89).
If passengers reject the air carrier’s reasonable
Notes: (89) Case C-12/11, ECLI:EU:C:2013:43, paragraph 66.
```
```text
[52024XC05687:A:w059:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.3.2 to Section 4.3.3, PDF pp. 19-20 | similarity 0.754
a much longer delay, the air carrier should be allowed to
decline to provide hotel accommodation and corresponding transfers. Similarly, if an air carrier is about to give vouchers
for food and drinks but is informed that the flight is ready for boarding, it should be allowed to decline to provide this
care. Apart from these cases, the Commission is of the opinion that this limitation is to be applied only in very exceptional
cases, as every effort should be made to reduce the inconvenience suffered by passengers.
The right to care under Regulation (EC) No 261/2004 has no bearing on the obligations of organisers of packages under
Directive (EU) 2015/2302.
4.3.3. Care in extraordinary circumstances or exceptional events
According to Regulation (EC) No 261/2004, the air carrier is obliged to fulfil the obligation of care even if the cancellation
of a flight is caused by extraordinary circumstances, that is to say circumstances that could not have been avoided even if all
reasonable measures had been taken. Regulation (EC) No 261/2004 contains nothing that would allow the conclusion to be
drawn that it recognises a separate category of ‘particularly extraordinary’ events – beyond the extraordinary circumstances
referred to in Article
```
```text
[52024XC05687:A:w058:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.3.2, PDF p. 19 | similarity 0.750
to take care of the accommodation arrangements as such (90), for
instance by booking a specific room in the name of the passenger.
On a similar line, the Court has stated that in the case of an incident at the hotel, the air carrier cannot be required, on the
basis of Regulation (EC) No 261/2004 alone, to compensate a passenger for damage caused by fault on the part of
employees of the hotel in which the accommodation is provided (91).
It should be borne in mind that according to recital 18 of Regulation (EC) No 261/2004, care may be limited or declined if
its provision would itself cause further delay to passengers awaiting an alternative or a delayed flight. If a flight is delayed
late in the evening but can be expected to depart within a few hours and if dispatching passengers to hotels and bringing
them back to the airport in the middle of the night could lead to a much longer delay, the air carrier should be allowed to
decline to provide hotel accommodation and corresponding transfers. Similarly, if an air carrier is about to give vouchers
for food and drinks but is informed that the flight is
Notes: (90) Case C-530/19, ECLI:EU:C:2020:635, paragraph 24. (91) Case C-530/19, ECLI:EU:C:2020:635, paragraph 40.
```
```text
[32004R0261:A:w019:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 8 to Article 9, PDF p. 5 | similarity 0.740
— a return flight to the first point of departure, at the
earliest opportunity;
(b) re-routing, under comparable transport conditions, to their
final destination at the earliest opportunity; or
(c) re-routing, under comparable transport conditions, to their
final destination at a later date at the passenger's convenience
, subject to availability of seats.
2. Paragraph 1(a) shall also apply to passengers whose
flights form part of a package, except for the right to reimbursement
where such right arises under Directive 90/314/EEC.
3. When, in the case where a town, city or region is served
by several airports, an operating air carrier offers a passenger a
flight to an airport alternative to that for which the booking
was made, the operating air carrier shall bear the cost of transferring
the passenger from that alternative airport either to that
for which the booking was made, or to another close-by destination
agreed with the passenger.
Article 9
Right to care
1. Where reference is made to this Article, passengers shall
be offered free of charge:
(a) meals and refreshments in a reasonable relation to the
waiting time;
(b) hotel accommodation in cases
— where a stay of one or more nights becomes necessary,
```
```text
[32004R0261:A:w016:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 6 to Article 7, PDF pp. 4-5 | similarity 0.803
in the case of all intra-Community
flights of more than 1 500 kilometres and of all other
flights between 1 500 and 3 500 kilometres; or
(c) for four hours or more in the case of all flights not falling
under (a) or (b),
passengers shall be offered by the operating air carrier:
(i) the assistance specified in Article 9(1)(a) and 9(2); and
(ii) when the reasonably expected time of departure is at least
the day after the time of departure previously announced,
the assistance specified in Article 9(1)(b) and 9(1)(c); and
(iii) when the delay is at least five hours, the assistance specified
in Article 8(1)(a).
2. In any event, the assistance shall be offered within the
time limits set out above with respect to each distance bracket.
Article 7
Right to compensation
1. Where reference is made to this Article, passengers shall
receive compensation amounting to:
(a) EUR 250 for all flights of 1 500 kilometres or less;
(b) EUR 400 for all intra-Community flights of more than
1 500 kilometres, and for all other flights between 1 500
and 3 500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the
```
```text
[52024XC05687:A:w034:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 3.2.6 to Section 3.3.2, PDF p. 13 | similarity 0.788
to be paid if the air carrier can prove, in accordance with Article 5(3), that the
cancellation is caused by extraordinary circumstances that could not have been avoided even if all reasonable measures had
been taken (63).
3.3. Delay
3.3.1. Delay at departure
Under Article 6(1) of Regulation (EC) No 261/2004, if the departure of a flight is delayed, passengers affected by this delay
have the right to ‘care’ according to Article 9, and to reimbursement and a return flight according to Article 8(1), point (a).
The underlying principle of Article 6(1) is that the rights depend on the duration of the delay and the distance of the flight.
In this regard, it should be noted that the right to re-routing as laid down in Article 8(1), point (b), is not covered under
Article 6(1) as it can be considered that the air carrier is trying, in the first place, to address the cause of the delay in order
to minimise the inconvenience to the passengers.
3.3.2. ‘Long delay’ at arrival
The Court has ruled that a delay at arrival of at least 3 hours gives the same rights in terms of compensation as a
cancellation (64) (for more details,
Notes: (63) See Section 5 on extraordinary circumstances. (64) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 69. See also Joined Cases C-581/10 and C-629/10, ECLI:EU:C:2012:657, paragraph 40, and Case C-413/11, ECLI:EU:C:2013:246, paragraph 19.
```
```text
[32004R0261:A:w015:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 5 to Article 6, PDF p. 4 | similarity 0.760
before the scheduled time of departure
and to reach their final destination less than two hours
after the scheduled time of arrival.
2. When passengers are informed of the cancellation, an
explanation shall be given concerning possible alternative transport
.
3. An operating air carrier shall not be obliged to pay
compensation in accordance with Article 7, if it can prove that
the cancellation is caused by extraordinary circumstances
which could not have been avoided even if all reasonable
measures had been taken.
4. The burden of proof concerning the questions as to
whether and when the passenger has been informed of the
cancellation of the flight shall rest with the operating air
carrier.
Article 6
Delay
1. When an operating air carrier reasonably expects a flight
to be delayed beyond its scheduled time of departure:
(a) for two hours or more in the case of flights of 1 500 kilometres
or less; or
(b) for three hours or more in the case of all intra-Community
flights of more than 1 500 kilometres and of all other
flights between 1 500 and 3 500 kilometres; or
(c) for four hours or more in the case of all flights not falling
```
```text
[52024XC05687:A:w054:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.3.1 to Section 4.3.2, PDF p. 18 | similarity 0.759
conditions, to their final
destination at the earliest opportunity (Article 8(1), point (b)), or a return flight (Article 8(1), point (a), second indent).
4.3.2. Provision of meals, refreshments and accommodation
The intention of Regulation (EC) No 261/2004 is to ensure that the needs of passengers waiting for their return flight or
re-routing are appropriately taken care of. The extent of appropriate care will have to be assessed on a case-by-case basis,
with due regard to the needs of passengers in the relevant circumstances and the principle of proportionality (i.e.
according to the waiting time). The price paid for the ticket or the temporary nature of the inconvenience suffered should
not interfere with the right to care.
With regard to Article 9(1), point (a), on meals and refreshments, the Commission considers the expression ‘in a reasonable
relation to the waiting time’ to mean that operating air carriers should provide passengers with appropriate care
corresponding to the expected length of the delay and the time of day (or night) at which it occurs, including at the
transfer airport in the case of connecting flights, in order to reduce the inconvenience suffered by the passengers as much
as possible, while bearing in mind
```

</details>

## q04 (single)

**Question:** I was downgraded from business to economy on a 2,000 km flight inside the EU. How much of the ticket price must be reimbursed?

**Reference:** 50% of the ticket price, within seven days (Art. 10(2)(b)); 30% applies to flights of 1,500 km or less and 75% to longer flights not under (a) or (b).

**Answer shown to the user:**

> For an intra-Community flight of more than 1,500 kilometres where you are downgraded from business to economy, the operating air carrier must reimburse **50%** of the price of the ticket within seven days [32004R0261:A:w021:1]. 
> 
> According to Regulation (EC) No 261/2004, the reimbursement percentages for downgrading are:
> * **30%** for flights of 1,500 km or less [32004R0261:A:w021:1].
> * **50%** for all intra-Community flights of more than 1,500 km, and for other flights between 1,500 km and 3,500 km [32004R0261:A:w021:1].
> * **75%** for all other flights [32004R0261:A:w021:1].
> 
> ### What to check next:
> * **Ticket price basis:** The reimbursement is calculated based on the price of the specific flight on which you were downgraded [52024XC05687:A:w038:1]. Taxes and charges are generally excluded from this calculation if their amount does not depend on the travel class [52024XC05687:A:w039:1].
> * **Payment method:** The carrier must pay the reimbursement within seven days, in cash, by electronic bank transfer, bank order, or bank cheque (or in travel vouchers, but only with your signed agreement) [32004R0261:A:w021:1, 32004R0261:A:w018:1].
> 
> *(Note: This information is drawn directly from EU passenger rights legislation and interpretative guidelines, not legal advice for your specific case.)*

<details><summary>Passages the agent retrieved</summary>

```text
[32004R0261:A:w021:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 10 to Article 11, PDF pp. 5-6 | similarity 0.798
a passenger in a class
lower than that for which the ticket was purchased, it shall
within seven days, by the means provided for in Article 7(3),
reimburse
(a) 30 % of the price of the ticket for all flights of 1 500 kilometres
or less, or
(b) 50 % of the price of the ticket for all intra-Community
flights of more than 1 500 kilometres, except flights
between the European territory of the Member States and
the French overseas departments, and for all other flights
between 1 500 and 3 500 kilometres, or
(c) 75 % of the price of the ticket for all flights not falling
under (a) or (b), including flights between the European
territory of the Member States and the French overseas
departments.
Article 11
Persons with reduced mobility or special needs
1. Operating air carriers shall give priority to carrying
persons with reduced mobility and any persons or certified
service dogs accompanying them, as well as unaccompanied
children.
2. In cases of denied boarding, cancellation and delays of
any length, persons with reduced mobility and any persons
accompanying them, as well as unaccompanied children, shall
have the right to care in accordance with Article 9
```
```text
[52024XC05687:A:w038:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 3.4.1 to Section 3.4.2, PDF p. 14 | similarity 0.767
treatment commensurate to their booking (e.g. as
regards seating or catering), but still travelling in the same class, are not being downgraded. However, they might be
eligible for a reimbursement of the amount paid for a service but not received under the air carrier’s terms and conditions
and/or under national law.
The definition of downgrading (or upgrading) applies to the class of service for which the ticket was purchased and not to
any advantages offered through a frequent flyer programme or other commercial programme provided by an air carrier or
tour operator.
3.4.2. Rights associated with upgrading and downgrading
In the case of upgrading, an air carrier cannot request any supplementary payment. In the case of downgrading,
compensation in the form of reimbursement of a percentage of the price of the ticket is provided for in Article 10(2),
points (a), (b) and (c), of Regulation (EC) No 261/2004.
The price to be taken into account in determining the reimbursement for the passengers affected is the price of the flight on
which they were downgraded unless this price is not indicated on the ticket entitling the passenger to transport on this
flight. In this case, it must be based on the
```
```text
[52024XC05687:A:w039:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 3.4.2 to Section 4.1.1, PDF pp. 14-15 | similarity 0.764
the passengers affected is the price of the flight on
which they were downgraded unless this price is not indicated on the ticket entitling the passenger to transport on this
flight. In this case, it must be based on the part of the price of the ticket corresponding to the quotient of the distance of
this flight divided by the total distance that the passenger is entitled to travel. This price does not include taxes and charges
indicated on the ticket as long as neither the requirement to pay these taxes and charges nor their amount depends on the
class for which the ticket was purchased (70).
4. PASSENGERS’ RIGHTS
4.1. Right to information
4.1.1. General right to information
Article 14(1) of Regulation (EC) No 261/2004 specifies the text of a notice that must be legible and displa yed at check-in in
a manner clearly visible to passengers. This notice should be displa yed physically or electronically in as many relevant
languages as possible. This has to be done not only at the airport check-in desk, but also on kiosks at the airport, online
and ideally also at the boarding gate.
In addition, whenever an air carrier gives partial, misleading
Notes: (70) Case C-255/15, ECLI:EU:C:2016:472, paragraphs 32 and 43.
```
```text
[32004R0261:A:w017:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 7, PDF p. 5 | similarity 0.763
(b) EUR 400 for all intra-Community flights of more than
1 500 kilometres, and for all other flights between 1 500
and 3 500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the distance, the basis shall be the last destination
at which the denial of boarding or cancellation will delay
the passenger's arrival after the scheduled time.
2. When passengers are offered re-routing to their final
destination on an alternative flight pursuant to Article 8, the
arrival time of which does not exceed the scheduled arrival
time of the flight originally booked
(a) by two hours, in respect of all flights of 1 500 kilometres
or less; or
(b) by three hours, in respect of all intra-Community flights of
more than 1 500 kilometres and for all other flights
between 1 500 and 3 500 kilometres; or
(c) by four hours, in respect of all flights not falling under (a)
or (b),
the operating air carrier may reduce the compensation
provided for in paragraph 1 by 50 %.
3. The compensation referred to in paragraph 1 shall be
paid in cash, by electronic bank transfer, bank orders or bank
cheques or, with
```
```text
[32004R0261:A:w018:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 7 to Article 8, PDF p. 5 | similarity 0.751
the operating air carrier may reduce the compensation
provided for in paragraph 1 by 50 %.
3. The compensation referred to in paragraph 1 shall be
paid in cash, by electronic bank transfer, bank orders or bank
cheques or, with the signed agreement of the passenger, in
travel vouchers and/or other services.
4. The distances given in paragraphs 1 and 2 shall be
measured by the great circle route method.
Article 8
Right to reimbursement or re-routing
1. Where reference is made to this Article, passengers shall
be offered the choice between:
(a) — reimbursement within seven days, by the means
provided for in Article 7(3), of the full cost of the ticket
at the price at which it was bought, for the part or
parts of the journey not made, and for the part or parts
already made if the flight is no longer serving any
purpose in relation to the passenger's original travel
plan, together with, when relevant,
— a return flight to the first point of departure, at the
earliest opportunity;
(b) re-routing, under comparable transport conditions, to their
final destination at the earliest opportunity; or
(c) re-routing, under comparable transport conditions, to their
final destination at
```

</details>

## q05 (single)

**Question:** Within how many days must an airline pay my ticket refund after a cancellation?

**Reference:** Within seven days, by cash, bank transfer, bank order or cheque, or vouchers only with the passenger's signed agreement (Art. 8(1)(a) with Art. 7(3)).

**Answer shown to the user:**

> Under EU air passenger rights regulations, when a flight is cancelled and you choose reimbursement, the airline must pay the full cost of the ticket **within seven days** [32004R0261:A:w018:1].
> 
> ### Key Conditions:
> * **Form of payment:** The reimbursement must be paid in cash, by electronic bank transfer, bank order, or bank cheque, unless you give your signed agreement to accept travel vouchers or other services [32004R0261:A:w018:1, 52024XC05687:A:w046:1].
> * **Scope of refund:** The refund covers the full price at which the ticket was bought for the parts of the journey not made, and also for parts already made if the flight no longer serves any purpose in relation to your original travel plan (along with a return flight to your first point of departure at the earliest opportunity, if relevant) [32004R0261:A:w018:1].
> 
> *(Note: This information is based directly on EU Regulation (EC) No 261/2004 and does not constitute formal legal advice.)*

<details><summary>Passages the agent retrieved</summary>

```text
[52024XC05687:A:w043:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.2, PDF p. 16 | similarity 0.748
Right to reimbursement, re-routing or rebooking in the event of denied boarding or cancellation
Article 8(1) of Regulation (EC) No 261/2004 imposes on air carriers the obligation to offer passengers a triple choice,
between the following:
— reimbursement of the ticket price (76) (77) and, in the case of connections, a return flight to the airport of departure at
the earliest opportunity;
— re-routing to their final destination either at the earliest opportunity; or
— re-routing at a later date at the passenger’s convenience under comparable transport conditions, subject to availability
of seats.
If an operating air carrier has to offer the choice between reimbursement and re-routing, the air carrier must present the
passengers concerned with comprehensive information on all the options concerning reimbursement and re-routing.
Pursuant to Article 5(2) of Regulation (EC) No 261/2004, passengers must receive information on re-routing from the
operating air carrier when informed of the cancellation. The passengers concerned are under no obligation to actively
contribute to seeking the relevant information themselves (78).
As a general principle, if the passenger is denied boarding or is informed about the cancellation of the flight and is correctly
informed of the available options, the choice offered to passengers
Notes: (76) The ticket price is reimbursed for the part or parts of the journey not made, and for the part or parts already made if the flight is no longer serving any purpose in relation to the passenger’s original travel plan. In principle, if the passengers choose to return to their airport of departure, the part or parts of the journey already made no longer serve any purpose in relation to the original travel plan. (77) The price of the ticket to be taken into consideration for the purposes of determining the reimbursement owed by the air carrier to a passenger in the event of cancellation of a flight includes the difference between the amount paid by that passenger and the amount received by the air carrier, which corresponds to a commission collected by a person acting as an intermediary between those two parties, unless that commission was set without the knowledge of the air carrier (Case C-601/17, ECLI:EU:C:2018:702, paragraph 20). (78) Case C-354/18, ECLI:EU:C:2019:637, paragraph 56.
```
```text
[32004R0261:A:w014:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 5, PDF p. 4 | similarity 0.701
in event of re-routing
when the reasonably expected time of departure of
the new flight is at least the day after the departure as it
was planned for the cancelled flight, the assistance specified
in Article 9(1)(b) and 9(1)(c); and
(c) have the right to compensation by the operating air carrier
in accordance with Article 7, unless:
(i) they are informed of the cancellation at least two
weeks before the scheduled time of departure; or
(ii) they are informed of the cancellation between two
weeks and seven days before the scheduled time of
departure and are offered re-routing, allowing them to
depart no more than two hours before the scheduled
time of departure and to reach their final destination
less than four hours after the scheduled time of arrival;
or
(iii) they are informed of the cancellation less than seven
days before the scheduled time of departure and are
offered re-routing, allowing them to depart no more
than one hour before the scheduled time of departure
and to reach their final destination less than two hours
after the scheduled time of arrival.
2. When passengers are informed of the cancellation, an
explanation shall be given concerning possible alternative transport
.
```
```text
[52024XC05687:A:w093:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 6.2, PDF pp. 29-30 | similarity 0.700
interfere with the right to choose re-routing at
the ‘earliest opportunity’. Air carriers may find it impossible to re-route the passenger to the intended destination within a
short period of time. Moreover, it may not be clear for some time when re-routing will become possible. This situation
may, for example, arise if a Member State suspends flights departing to or arriving from certain countries. Therefore,
depending on the case, the earliest opportunity for re-routing may be considerably delayed or subject to considerable
uncertainty. As a result, reimbursement of the ticket price or a re-routing at a later date ‘at the passenger’s convenience’
might be preferable for the passenger.
Regarding reimbursement, in cases where the passenger books the outbound flight and the return flight separately and the
outbound flight is cancelled, the passenger is only entitled to reimbursement of the cancelled flight, that is to say, here, the
outbound flight.
However, if the outbound flight and the return flight are part of the same booking, even if operated by different air carriers,
passengers should be offered two options if the outbound flight is cancelled: to be reimbursed for the whole ticket (i.e. both
flights) or to be re-routed on another flight
```
```text
[52024XC05687:A:w094:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 6.2 to Section 6.4, PDF p. 30 | similarity 0.699
of the same booking, even if operated by different air carriers,
passengers should be offered two options if the outbound flight is cancelled: to be reimbursed for the whole ticket (i.e. both
flights) or to be re-routed on another flight for the outbound flight.
6.3. Right to care
Regulation (EC) No 261/2004 does not contain any provisions that recognise a separate category of ‘particularly
extraordinary’ events beyond the extraordinary circumstances referred to in its Article 5(3). Therefore, the air carrier is
required to fulfil its obligations, including those under Article 9 of Regulation (EC) No 261/2004, even if the situation
giving rise to these obligations lasts for a long period. In such circumstances and events, passengers are especially
vulnerable (153). If exceptional events occur, the intention of Regulation (EC) No 261/2004 is to ensure that appropriate
care is provided in particular to passengers waiting for re-routing under Article 8(1), point (b), of Regulation (EC)
No 261/2004.
6.4. Right to compensation
The right to compensation for cancellation pursuant to Article 5(1) and Article 7 of Regulation (EC) No 261/2004 does not
apply in the case of cancellations made more than 14 days in advance or if the cancellation is caused by
Notes: (153) Case C-12/11, ECLI:EU:C:2013:43, paragraph 30, and Point 4.3.3 of the Interpretative Guidelines.
```
```text
[32015L2302:A:w061:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 12 to Article 13, PDF p. 17 | similarity 0.697
in the case of trips lasting less than two days;
or
(b) the organiser is prevented from performing the contract because of unavoidable and extraordinary circumstances
and notifies the traveller of the termination of the contract without undue delay before the start of the package.
4. The organiser shall provide any refunds required under paragraphs 2 and 3 or, with respect to paragraph 1,
reimburse any payments made by or on behalf of the traveller for the package minus the appropriate termination fee.
Such refunds or reimbursements shall be made to the traveller without undue delay and in any event not later than 14
days after the package travel contract is terminated.
5. With respect to off-premises contracts, Member States may provide in their national law that the traveller has the
right to withdraw from the package travel contract within a period of 14 days without giving any reason.
Article 13
Responsibility for the performance of the package
1. Member States shall ensure that the organiser is responsible for the performance of the travel services included in
the package travel contract, irrespective of whether those services are to be performed by the organiser or by other
travel service providers.
Member
```
```text
[32004R0261:A:w018:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 7 to Article 8, PDF p. 5 | similarity 0.777
the operating air carrier may reduce the compensation
provided for in paragraph 1 by 50 %.
3. The compensation referred to in paragraph 1 shall be
paid in cash, by electronic bank transfer, bank orders or bank
cheques or, with the signed agreement of the passenger, in
travel vouchers and/or other services.
4. The distances given in paragraphs 1 and 2 shall be
measured by the great circle route method.
Article 8
Right to reimbursement or re-routing
1. Where reference is made to this Article, passengers shall
be offered the choice between:
(a) — reimbursement within seven days, by the means
provided for in Article 7(3), of the full cost of the ticket
at the price at which it was bought, for the part or
parts of the journey not made, and for the part or parts
already made if the flight is no longer serving any
purpose in relation to the passenger's original travel
plan, together with, when relevant,
— a return flight to the first point of departure, at the
earliest opportunity;
(b) re-routing, under comparable transport conditions, to their
final destination at the earliest opportunity; or
(c) re-routing, under comparable transport conditions, to their
final destination at
```
```text
[32004R0261:A:w017:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 7, PDF p. 5 | similarity 0.763
(b) EUR 400 for all intra-Community flights of more than
1 500 kilometres, and for all other flights between 1 500
and 3 500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the distance, the basis shall be the last destination
at which the denial of boarding or cancellation will delay
the passenger's arrival after the scheduled time.
2. When passengers are offered re-routing to their final
destination on an alternative flight pursuant to Article 8, the
arrival time of which does not exceed the scheduled arrival
time of the flight originally booked
(a) by two hours, in respect of all flights of 1 500 kilometres
or less; or
(b) by three hours, in respect of all intra-Community flights of
more than 1 500 kilometres and for all other flights
between 1 500 and 3 500 kilometres; or
(c) by four hours, in respect of all flights not falling under (a)
or (b),
the operating air carrier may reduce the compensation
provided for in paragraph 1 by 50 %.
3. The compensation referred to in paragraph 1 shall be
paid in cash, by electronic bank transfer, bank orders or bank
cheques or, with
```
```text
[52024XC05687:A:w046:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.2, PDF pp. 16-17 | similarity 0.754
cancellation of a flight, to offer assistance to the passengers concerned such as offering them reimbursement of the ticket,
at the price at which it was bought, and, where necessary, a return flight to the first point of departure (80).
However, if an air carrier can demonstrate that it has contacted the passengers who have accepted to give their personal
contact details, and that it has sought to provide the assistance required by Article 8, but the passengers have nonetheless
made their own assistance or re-routing arrangements, then the air carrier may conclude that it is not responsible for any
additional costs the passengers have incurred and may decide not to reimburse them.
As regards the form in which the reimbursement is to be made, the structure of Article 7(3) shows that the reimbursement
of the cost of the ticket is made, primarily, by a sum of money. By contrast, reimbursement in travel vouchers and/or other
services is presented as a subsidiary means of reimbursement, since it is subject to the supplementary condition of the
‘signed agreement of the passenger’ (81).
In this connection, the Court has clarified that the concept of ‘agreement’ is to be understood, in accordance with
Notes: (80) Case C-601/17, ECLI:EU:C:2018:702, paragraph 12. (81) Case C-76/23, ECLI:EU:C:2024:253, paragraph 20.
```
```text
[52024XC05687:A:w075:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.4.13 to Section 4.4.14, PDF p. 24 | similarity 0.747
at its destination with a long delay, they are not eligible for compensation if they reach their final destination
(with the new flight) with a delay of less than 3 hours after the scheduled arrival time of their originally booked flight (114).
F. Reimbursement in the event of downgrading
4.4.14. Calculation of the amount
In accordance with Article 10 of Regulation (EC) No 261/2004, reimbursement is payable only for the flight on which the
passenger has been downgraded and not for the whole journey included in a single ticket, which may include two or more
connecting flights. The aforementioned reimbursement should be paid within 7 days.
G. Further compensation
Article 7 of Regulation (EC) No 261/2004 provides for standardised fixed compensation. Article 12 underlines that the
provisions of Regulation (EC) No 261/2004 do not rule out a passenger’s right to additional compensation. The Court has
ruled that the concept of ‘further compensation’ allows a national court to award compensation, under the conditions
provided for by the Montreal Convention or national law, for damage, including non-material damage, arising from breach
of a contract of carriage by air (115). A national court may deduct the compensation granted under Regulation (EC)
No 261/2004
Notes: (114) Case C-54/23, ECLI:EU:C:2024:74, paragraph 24. (115) Case C-83/10, ECLI:EU:C:2011:652, paragraph 46.
```

</details>

## q06 (single)

**Question:** Does the air passenger rights regulation protect me if I travel on a frequent flyer award ticket?

**Reference:** Yes. The regulation does not apply to free or reduced fares not available to the public, but it does apply to tickets issued under a frequent flyer or other commercial programme (Art. 3(3)).

**Answer shown to the user:**

> WITHHELD: the harness blocked this answer because it makes claims without citing any retrieved passage.

<details><summary>Passages the agent retrieved</summary>

```text
[32004R0261:A:w012:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 3 to Article 4, PDF pp. 3-4 | similarity 0.807
a reduced fare not available directly or
indirectly to the public. However, it shall apply to passengers
having tickets issued under a frequent flyer programme or
other commercial programme by an air carrier or tour
operator.
4. This Regulation shall only apply to passengers transported
by motorised fixed wing aircraft.
5. This Regulation shall apply to any operating air carrier
providing transport to passengers covered by paragraphs 1 and
2. Where an operating air carrier which has no contract with
the passenger performs obligations under this Regulation, it
shall be regarded as doing so on behalf of the person having a
contract with that passenger.
6. This Regulation shall not affect the rights of passengers
under Directive 90/314/EEC. This Regulation shall not apply in
cases where a package tour is cancelled for reasons other than
cancellation of the flight.
Article 4
Denied boarding
1. When an operating air carrier reasonably expects to deny
boarding on a flight, it shall first call for volunteers to
surrender their reservations in exchange for benefits under
conditions to be agreed between the passenger concerned and
the operating air carrier. Volunteers shall be assisted in accordance
with Article 8, such assistance being additional to the
```
```text
[32004R0261:A:w011:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 3, PDF pp. 3-4 | similarity 0.804
territory of a Member
State to which the Treaty applies, unless they received
benefits or compensation and were given assistance in that
third country, if the operating air carrier of the flight
concerned is a Community carrier.
2. Paragraph 1 shall apply on the condition that passengers:
(a) have a confirmed reservation on the flight concerned and,
except in the case of cancellation referred to in Article 5,
present themselves for check-in,
— as stipulated and at the time indicated in advance and
in writing (including by electronic means) by the air
carrier, the tour operator or an authorised travel agent,
or, if no time is indicated,
— not later than 45 minutes before the published departure
time; or
(b) have been transferred by an air carrier or tour operator
from the flight for which they held a reservation to another
flight, irrespective of the reason.
3. This Regulation shall not apply to passengers travelling
free of charge or at a reduced fare not available directly or
indirectly to the public. However, it shall apply to passengers
having tickets issued under a frequent flyer programme or
other commercial programme by an air carrier or tour
operator.
4. This Regulation shall
```
```text
[52024XC05687:A:w016:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 2.2.2 to Section 2.2.3, PDF p. 8 | similarity 0.779
event
sponsorship operation, the benefit of which is restricted to certain specified people and the issue of which requires prior
and individual authorisation from that air carrier (34).
By contrast, Article 3(3) stipulates that the Regulation does apply to passengers having tickets issued under a frequent flyer
programme or other commercial programme by an air carrier or tour operator.
As regards infants, the Court has held that passengers who travel free of charge on account of their young age, but who do
not have an allocated seat or a boarding pass and whose names do not appear on the reservation booked by their parents,
are excluded from the scope of Regulation (EC) No 261/2004 (35).
2.2.3. Requirement for passengers to be present for check-in
It follows from Article 3(2) of Regulation (EC) No 261/2004 that in order to be covered by the Regulation, passengers: (i)
have to hold a confirmed reservation; and (ii) must present themselves for check-in in good time. The second requirement
does not apply in the case of a flight cancellation.
These two conditions are cumulative: the passenger’s presence for check-in cannot be presumed by virtue of the fact that
the passenger has a confirmed reservation on
Notes: (34) Case C-316/20, ECLI:EU:C:2020:966, paragraph 19. (35) Case C-686/20, ECLI:EU:C:2021:859, paragraph 31.
```
```text
[32004R0261:A:w000:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Preamble to Recital (2), PDF p. 1 | similarity 0.778
I
(Acts whose publication is obligatory)
REGULATION (EC) No 261/2004 OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL
of 11 February 2004
establishing common rules on compensation and assistance to passengers in the event of denied
boarding and of cancellation or long delay of flights, and repealing Regulation (EEC) No 295/91
(Text with EEA relevance)
THE EUROPEAN PARLIAMENT AND THE COUNCIL OF THE
EUROPEAN UNION,
Having regard to the Treaty establishing the European
Community, and in particular Article 80(2) thereof,
Having regard to the proposal from the Commission ( 1),
Having regard to the opinion of the European Economic and
Social Committee ( 2),
After consulting the Committee of the Regions,
Acting in accordance with the procedure laid down in Article
251 of the Treaty ( 3), in the light of the joint text approved by
the Conciliation Committee on 1 December 2003,
Whereas:
(1) Action by the Community in the field of air transport
should aim, among other things, at ensuring a high level
of protection for passengers. Moreover, full account
should be taken of the requirements of consumer protection
in general.
(2) Denied boarding and cancellation or long delay of flights
cause serious trouble and inconvenience to passengers.
```
```text
[52024XC05687:A:w015:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 2.2.2, PDF p. 8 | similarity 0.777
of charge’ means that a passenger is transported by the air carrier without any pecuniary obligation on the
part of the passenger. Cases where the air fare is reduced to zero but passengers still have to pay for taxes and other
charges in order to receive their tickets, would not fall under this term.
If a ticket was obtained at a reduced rate, the determining factor is whether this reduction is reserved to a specific group of
people or if it is open to anyone who wishes to book, even if they might have to fulfil certain conditions or requirements.
Such tickets would still be considered as ‘publicly available’ and their holders would be covered by the Regulation.
However, special fares offered by air carriers to their staff do fall under this provision. Regulation (EC) No 261/2004 does
not apply, either, to a passenger who travels on a preferential fare ticket issued by an air carrier as part of an event
sponsorship operation, the benefit of which is restricted to certain specified people and the issue of which requires prior
and individual authorisation from that air carrier (34).
By contrast, Article 3(3) stipulates that the Regulation does apply to passengers
Notes: (34) Case C-316/20, ECLI:EU:C:2020:966, paragraph 19.
```

</details>

## q07 (single)

**Question:** At what moment does a flight count as having arrived when calculating the length of a delay?

**Reference:** When at least one of the aircraft doors is opened, on the assumption that passengers may then leave the aircraft (guidelines, section 3.3.3).

**Answer shown to the user:**

> When calculating the length of a delay at arrival, the EU Court of Justice has concluded that the "time of arrival" corresponds to the moment when **at least one of the doors of the aircraft is opened**, under the assumption that passengers are permitted to leave the aircraft at that time [52024XC05687:A:w035:1]. 
> 
> *Note: This point comes from the European Commission’s 2024 interpretative guidelines on Regulation (EC) No 261/2004, reflecting case law, which serve as guidance rather than binding legislation [52024XC05687:A:w035:1].*

<details><summary>Passages the agent retrieved</summary>

```text
[52024XC05687:A:w035:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 3.3.1 to Section 3.3.3, PDF pp. 13-14 | similarity 0.729
minimise the inconvenience to the passengers.
3.3.2. ‘Long delay’ at arrival
The Court has ruled that a delay at arrival of at least 3 hours gives the same rights in terms of compensation as a
cancellation (64) (for more details, see Section 4.4.5 on compensation).
3.3.3. Measuring the delay at arrival and concept of time of arrival
The Court has concluded that the concept of ‘time of arrival’, which is used to determine the length of the delay to which
passengers on a flight have been subject if arrival is delayed, corresponds to the time at which at least one of the doors of
the aircraft is opened, the assumption being that, at that moment, the passengers are permitted to leave the aircraft (65).The
Commission considers that the operating air carrier should register the time of arrival on the basis of, for instance, a signed
declaration by the flight crew or handling agent. The time of arrival should be provided free of charge upon request to the
national enforcement body and the passengers as evidence of compliance with Regulation (EC) No 261/2004.
The ‘scheduled arrival time’ used as the starting point for calculating a delay is the time that is
Notes: (64) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 69. See also Joined Cases C-581/10 and C-629/10, ECLI:EU:C:2012:657, paragraph 40, and Case C-413/11, ECLI:EU:C:2013:246, paragraph 19. (65) Case C-452/13, ECLI:EU:C:2014:2141, paragraph 27.
```
```text
[52024XC05687:A:w036:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 3.3.3, PDF pp. 13-14 | similarity 0.705
free of charge upon request to the
national enforcement body and the passengers as evidence of compliance with Regulation (EC) No 261/2004.
The ‘scheduled arrival time’ used as the starting point for calculating a delay is the time that is fixed in the flight schedule
and indicated on the reservation (ticket or other proof (66)) held by the passenger concerned (67).
To determine the extent of the delay in arrival suffered by a passenger on a diverted flight that landed at an airport that is
different from the one for which the booking was made but that serves the same town, city or region, it is necessary to
take as a reference the time at which the passenger actually reaches, at the end of the transfer, either the airport for which
the booking was made or, as the case may be, another close-by destination agreed with the operating air carrier (68).
If a flight was delayed at arrival by 3 hours or more and if this delay was partly due to an event that qualifies as an
extraordinary circumstance and partly due to another cause, the delay attributable to the extraordinary circumstance must
be deducted from the total delay of
Notes: (66) Joined Cases C-146/20, C-188/20, C-196/20 and C-270/20, ECLI:EU:C:2021:1038, paragraph 68. (67) Case C-654/19, ECLI:EU:C:2020:770, paragraph 25. (68) Case C-826/19, ECLI:EU:C:2021:318, paragraph 49.
```
```text
[52024XC05687:A:w067:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.4.7 to Section 4.4.8, PDF p. 22 | similarity 0.675
in which passengers concerned by a flight cancellation are not offered re-routing allowing them to depart no
more than 1 hour before the scheduled time of departure and to reach their final destination less than 2 hours after the
scheduled time of arrival. The Court deduced from this that the right to compensation laid down in Article 7 of Regulation
(EC) No 261/2004 aims to repair a loss of time of at least 3 hours. However, such a delay does not entitle passengers to
compensation if the air carrier can prove that the long delay was caused by extraordinary circumstances that could not
have been avoided even if all reasonable measures had been taken (100) (see Section 5 on extraordinary circumstances).
4.4.8. Compensation for long delay at arrival in the case of connecting flights
The Court (101) takes the view that for the purposes of the compensation provided for in Article 7 of Regulation (EC)
No 261/2004, a delay must be assessed in relation to the scheduled time of arrival at the passenger’s final destination as
defined in Article 2, point (h), of Regulation (EC) No 261/2004, which in the case of directly connecting flights must be
understood as the
Notes: (100) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 69. (101) Case C-11/11, ECLI:EU:C:2013:106, paragraph 47.
```
```text
[32004R0261:A:w016:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 6 to Article 7, PDF pp. 4-5 | similarity 0.669
in the case of all intra-Community
flights of more than 1 500 kilometres and of all other
flights between 1 500 and 3 500 kilometres; or
(c) for four hours or more in the case of all flights not falling
under (a) or (b),
passengers shall be offered by the operating air carrier:
(i) the assistance specified in Article 9(1)(a) and 9(2); and
(ii) when the reasonably expected time of departure is at least
the day after the time of departure previously announced,
the assistance specified in Article 9(1)(b) and 9(1)(c); and
(iii) when the delay is at least five hours, the assistance specified
in Article 8(1)(a).
2. In any event, the assistance shall be offered within the
time limits set out above with respect to each distance bracket.
Article 7
Right to compensation
1. Where reference is made to this Article, passengers shall
receive compensation amounting to:
(a) EUR 250 for all flights of 1 500 kilometres or less;
(b) EUR 400 for all intra-Community flights of more than
1 500 kilometres, and for all other flights between 1 500
and 3 500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the
```
```text
[52024XC05687:A:w034:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 3.2.6 to Section 3.3.2, PDF p. 13 | similarity 0.665
to be paid if the air carrier can prove, in accordance with Article 5(3), that the
cancellation is caused by extraordinary circumstances that could not have been avoided even if all reasonable measures had
been taken (63).
3.3. Delay
3.3.1. Delay at departure
Under Article 6(1) of Regulation (EC) No 261/2004, if the departure of a flight is delayed, passengers affected by this delay
have the right to ‘care’ according to Article 9, and to reimbursement and a return flight according to Article 8(1), point (a).
The underlying principle of Article 6(1) is that the rights depend on the duration of the delay and the distance of the flight.
In this regard, it should be noted that the right to re-routing as laid down in Article 8(1), point (b), is not covered under
Article 6(1) as it can be considered that the air carrier is trying, in the first place, to address the cause of the delay in order
to minimise the inconvenience to the passengers.
3.3.2. ‘Long delay’ at arrival
The Court has ruled that a delay at arrival of at least 3 hours gives the same rights in terms of compensation as a
cancellation (64) (for more details,
Notes: (63) See Section 5 on extraordinary circumstances. (64) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 69. See also Joined Cases C-581/10 and C-629/10, ECLI:EU:C:2012:657, paragraph 40, and Case C-413/11, ECLI:EU:C:2013:246, paragraph 19.
```

</details>

## q08 (single)

**Question:** Is a strike by the airline's own staff an extraordinary circumstance that cancels my right to compensation?

**Reference:** No. According to the guidelines, the Court held that a strike by the operating carrier's staff linked to employment demands (e.g. pay) is not an extraordinary circumstance; this includes union and 'wildcat' strikes (section 5.2.2).

**Answer shown to the user:**

> No. According to the interpretative guidelines (which reflect EU case law), strikes by the staff of an operating air carrier **cannot** be qualified as extraordinary circumstances if the strike is connected to employment demands, such as pay negotiations, union-organized strikes, wildcat strikes over restructuring, or solidarity strikes [52024XC05687:A:w082:1, 52024XC05687:A:w083:1]. Because these issues stem from the normal exercise of the carrier's activity and are under its actual control, they do not cancel your right to compensation [52024XC05687:A:w082:1, 52024XC05687:A:w083:1].
> 
> An exception exists only if the strike originates from demands that **only public authorities can satisfy** and that are therefore beyond the air carrier's actual control [52024XC05687:A:w083:1]. 
> 
> *(Note: This information is based on EU interpretive guidelines and case law texts, not legal advice for your specific case.)*

<details><summary>Passages the agent retrieved</summary>

```text
[52024XC05687:A:w088:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.2.3 to Section 5.3, PDF p. 28 | similarity 0.805
a flight at a congested airport due to bad weather conditions, including if these conditions result in capacity
shortages, would stem from extraordinary circumstances.
i) External strikes
Strikes that are external to the activity of an air carrier, such as strike action taken by air traffic controllers or airport staff,
may constitute extraordinary circumstances given that such external strike action does not fall within the exercise of the air
carrier’s activity and is thus beyond its actual control (145).
j) Shortage of staff providing baggage loading services
A situation where there is an insufficient number of staff of the airport operator responsible for the operations of loading
baggage onto planes may constitute an extraordinary circumstance (146).
5.3. Reasonable measures an air carrier can be expected to take in extraordinary circumstances
Whenever extraordinary circumstances arise, an air carrier must, in order to be released from the obligation to pay
compensation, show that it could not have avoided them even if it had taken all reasonable measures to this effect.
In other words, if such circumstances do arise, it is incumbent on the operating air carrier to demonstrate that it adopted
measures appropriate to the situation, deploying all its resources in terms
Notes: (145) Case C-28/20, ECLI:EU:C:2021:226, paragraphs 42 and 43. (146) Case C-405/23, ECLI:EU:C:2024:408, paragraph 30.
```
```text
[52024XC05687:A:w082:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.2.2, PDF p. 26 | similarity 0.791
carriers are regularly faced with situations arising from the use of such equipment. A collision between an aircraft and a
set of mobile boarding stairs is, hence, an internal event, inherent in the normal exercise of the activity of the air carrier.
Extraordinary circumstances would apply, for example, when damage to the aircraft is due to an act external to the
airport’s normal services, such as an act of terrorism or sabotage.
— Unexpected absence of crew members
If a crew member whose presence is essential to the operation of a flight is unexpectedly absent shortly before the
scheduled departure of this flight due to illness or even unexpected death, this does not fall within the concept of
extraordinary circumstances within the meaning of Article 5(3) of Regulation (EC) No 261/2004 (128).
— Strikes by airline staff
The Court has ruled that strikes by the staff of an operating air carrier cannot be qualified as an extraordinary circumstance
if this strike is connected to demands relating to the employment relationship between the air carrier and its staff, such as in
the case of pay negotiations (129).
This finding also applies to strikes organised by trade unions (130) and ‘wildcat strikes’
Notes: (128) Joined Cases C-156/22, C-157/22 and C-158/22, ECLI:EU:C:2023:393, paragraph 26. (129) Case C-28/20, ECLI:EU:C:2021:226, paragraph 37. (130) Case C-28/20, ECLI:EU:C:2021:226, paragraph 44.
```
```text
[52024XC05687:A:w083:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.2.2 to Section 5.2.3, PDF pp. 26-27 | similarity 0.787
strike is connected to demands relating to the employment relationship between the air carrier and its staff, such as in
the case of pay negotiations (129).
This finding also applies to strikes organised by trade unions (130) and ‘wildcat strikes’ called by airline staff following the
surprise announcement of a restructuring of an air carrier (131). A strike by the staff of an operating air carrier in solidarity
with strike action launched against the parent company of this air carrier is also not covered by the concept of
extraordinary circumstances (132).
Strike measures taken to enforce the claims of these workers at the parent company do not fall within the concept of
extraordinary circumstances within the meaning of Article 5(3) of Regulation (EC) No 261/2004; whether there were
prior negotiations with emplo yees’ representatives is irrelevant in this regar d (133).
If, however, such a strike originates from demands that only the public authorities can satisfy and that, accordingly, are
beyond the actual control of the air carrier concerned, it is capable of constituting an extraordinary circumstance (134).
5.2.3. ‘External’ events
In various cases, the Court has assessed situations arising from natural events or acts of third parties. These events
Notes: (129) Case C-28/20, ECLI:EU:C:2021:226, paragraph 37. (130) Case C-28/20, ECLI:EU:C:2021:226, paragraph 44. (131) Case C-195/17, ECLI:EU:C:2018:258, paragraph 48. (132) Case C-613/20, ECLI:EU:C:2021:820, paragraph 34. (133) Case C-287/20, ECLI:EU:C:2022:1, paragraph 33. (134) Case C-28/20, ECLI:EU:C:2021:226, paragraph 45.
```
```text
[52024XC05687:A:w077:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.1, PDF pp. 24-25 | similarity 0.778
(a) the existence of extraordinary circumstances and the link between these circumstances and the delay or the
cancellation; and
(b) the fact that this delay or cancellation could not have been avoided even though the air carrier took all reasonable
measures (see Section 5.3).
A given extraordinary circumstance can produce more than one cancellation or delay at final destination, such as in the case
of an air traffic management decision as referred to in recital 15 of Regulation (EC) No 261/2004.
As a derogation from the main rule – i.e. the payment of compensation, which reflects the objective of consumer
protection – the exemption in Article 5(3) must be interpreted strictly (118). Therefore, all extraordinary circumstances
surrounding events such as those listed in recital 14 of Regulation (EC) No 261/2004 – i.e. political instability,
meteorological conditions incompatible with the operation of the flight concerned, security risks, unexpected flight safety
shortcomings and strikes that affect the operation of an operating air carrier – are not necessarily grounds for an
exemption from the obligation to pay compensation, but require a case-by-case assessment (119).
The Court has developed two cumulative conditions for the classification of events as extraordinary circumstances, which
have been consistently
Notes: (118) Case C-549/07, ECLI:EU:C:2008:771, paragraph 17, and the case-law cited. (119) Case C-549/07, ECLI:EU:C:2008:771, paragraph 22.
```
```text
[52024XC05687:A:w095:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 6.4, PDF p. 30 | similarity 0.767
The right to compensation for cancellation pursuant to Article 5(1) and Article 7 of Regulation (EC) No 261/2004 does not
apply in the case of cancellations made more than 14 days in advance or if the cancellation is caused by extraordinary
circumstances that could not have been avoided even if all reasonable measures had been taken by the air carrier.
The Commission considers that, if public authorities take measures intended to contain the effects of a crisis situation
leading to massive travel disruptions, such measures are by their nature and origin not inherent in the normal exercise of
the activity of air carriers and are outside their actual control.
Article 5(3) waives the right to compensation on condition that the cancellation in question ‘is caused’ by extraordinary
circumstances that could not have been avoided even if all reasonable measures had been taken.
This condition should be considered fulfilled if public authorities either prohibit certain flights or restrict the movement of
people in a manner that de facto excludes the operation of the flight in question.
This condition may also be fulfilled if the flight cancellation occurs in circumstances in which the corresponding movement
of people is not entirely prohibited but
```

</details>

## q09 (single)

**Question:** Does a bird strike count as an extraordinary circumstance for flight compensation?

**Reference:** Yes, a collision with a bird can be an extraordinary circumstance, and it is irrelevant whether it actually damaged the aircraft (guidelines, section 5.2.3).

**Answer shown to the user:**

> Yes. According to the European Commission's interpretative guidelines (which summarize EU case-law), a collision between an aircraft and a bird, as well as any resulting damage or incidents (such as an aborted take-off or emergency braking), are not inherent in the normal exercise of an airline's activity and are outside its actual control [52024XC05687:A:w084:1, 52024XC05687:A:w085:1]. Therefore, such a collision **may be classified as an extraordinary circumstance** [52024XC05687:A:w084:1].
> 
> However, even if a bird strike occurred, the airline must still prove that the resulting cancellation or delay could not have been avoided even if it had taken all "reasonable measures" (deploying appropriate resources and measures suitable to the situation) [52024XC05687:A:w077:1, 52024XC05687:A:w088:1]. 
> 
> *Note: This information is based on the published EU texts and Commission guidelines, not legal advice for a specific case.*

<details><summary>Passages the agent retrieved</summary>

```text
[52024XC05687:A:w084:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.2.2 to Section 5.2.3, PDF p. 27 | similarity 0.786
beyond the actual control of the air carrier concerned, it is capable of constituting an extraordinary circumstance (134).
5.2.3. ‘External’ events
In various cases, the Court has assessed situations arising from natural events or acts of third parties. These events can
generally be qualified as extraordinary circumstances.
Some examples are set out below.
a) Bird strike
A collision between an aircraft and a bird as well as any damage caused by such a collision are not intrinsically linked to the
operation of the aircraft. They are not by their nature or origin inherent in the normal exercise of the activity of the air
carrier concerned and are therefore outside its actual control. Accordingly, such a collision may be classified as an
extraordinary circumstance (135).
The Court has also clarified that it is irrelevant whether the collision actually caused damage to the aircraft concerned. The
objective of ensuring a high level of protection for air passengers pursued by Regulation (EC) No 261/2004, as specified in
its recital 1, means that air carriers must not be encouraged to refrain from taking the measures necessitated by such an
incident by prioritising the maintaining and punctuality of their flights over the objective of safety
Notes: (134) Case C-28/20, ECLI:EU:C:2021:226, paragraph 45. (135) Case C-315/15, ECLI:EU:C:2017:342, paragraph 24.
```
```text
[52024XC05687:A:w085:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.2.3, PDF p. 27 | similarity 0.752
261/2004, as specified in
its recital 1, means that air carriers must not be encouraged to refrain from taking the measures necessitated by such an
incident by prioritising the maintaining and punctuality of their flights over the objective of safety (136).
In another case, the Court has found that the interruption of the take-off phase of an aircraft caused by a bird strike and
resulting in an emergency braking manoeuvre damaging the aircraft’s tyres falls within the concept of extraordinary
circumstances within the meaning of Article 5(3) of Regulation (EC) No 261/2004 (137).
b) Collision with other aircrafts or airport vehicles
A collision of an aircraft in a parking position with an aircraft of another airline caused by the movement of the aircraft of
the other airline falls within the concept of extraordinary circumstances (138).
A technical failure of an aircraft parked at the airport caused by a collision of a catering vehicle belonging to a third party
with the aircraft is also capable of falling within the concept of extraordinary circumstances (139).
c) Damage to the aircraft caused by a foreign object
Damage to an aircraft caused by a foreign object, such as loose debris, lying on an airport
Notes: (136) Case C-315/15, ECLI:EU:C:2017:342, paragraph 25. (137) Case C-302/22, ECLI:EU:C:2022:748, paragraph 23. (138) Case C-264/20, ECLI:EU:C:2021:26, paragraph 26. (139) Case C-659/21, ECLI:EU:C:2022:254, paragraph 27.
```
```text
[52024XC05687:A:w088:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.2.3 to Section 5.3, PDF p. 28 | similarity 0.749
a flight at a congested airport due to bad weather conditions, including if these conditions result in capacity
shortages, would stem from extraordinary circumstances.
i) External strikes
Strikes that are external to the activity of an air carrier, such as strike action taken by air traffic controllers or airport staff,
may constitute extraordinary circumstances given that such external strike action does not fall within the exercise of the air
carrier’s activity and is thus beyond its actual control (145).
j) Shortage of staff providing baggage loading services
A situation where there is an insufficient number of staff of the airport operator responsible for the operations of loading
baggage onto planes may constitute an extraordinary circumstance (146).
5.3. Reasonable measures an air carrier can be expected to take in extraordinary circumstances
Whenever extraordinary circumstances arise, an air carrier must, in order to be released from the obligation to pay
compensation, show that it could not have avoided them even if it had taken all reasonable measures to this effect.
In other words, if such circumstances do arise, it is incumbent on the operating air carrier to demonstrate that it adopted
measures appropriate to the situation, deploying all its resources in terms
Notes: (145) Case C-28/20, ECLI:EU:C:2021:226, paragraphs 42 and 43. (146) Case C-405/23, ECLI:EU:C:2024:408, paragraph 30.
```
```text
[52024XC05687:A:w077:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.1, PDF pp. 24-25 | similarity 0.740
(a) the existence of extraordinary circumstances and the link between these circumstances and the delay or the
cancellation; and
(b) the fact that this delay or cancellation could not have been avoided even though the air carrier took all reasonable
measures (see Section 5.3).
A given extraordinary circumstance can produce more than one cancellation or delay at final destination, such as in the case
of an air traffic management decision as referred to in recital 15 of Regulation (EC) No 261/2004.
As a derogation from the main rule – i.e. the payment of compensation, which reflects the objective of consumer
protection – the exemption in Article 5(3) must be interpreted strictly (118). Therefore, all extraordinary circumstances
surrounding events such as those listed in recital 14 of Regulation (EC) No 261/2004 – i.e. political instability,
meteorological conditions incompatible with the operation of the flight concerned, security risks, unexpected flight safety
shortcomings and strikes that affect the operation of an operating air carrier – are not necessarily grounds for an
exemption from the obligation to pay compensation, but require a case-by-case assessment (119).
The Court has developed two cumulative conditions for the classification of events as extraordinary circumstances, which
have been consistently
Notes: (118) Case C-549/07, ECLI:EU:C:2008:771, paragraph 17, and the case-law cited. (119) Case C-549/07, ECLI:EU:C:2008:771, paragraph 22.
```
```text
[32004R0261:A:w015:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 5 to Article 6, PDF p. 4 | similarity 0.738
before the scheduled time of departure
and to reach their final destination less than two hours
after the scheduled time of arrival.
2. When passengers are informed of the cancellation, an
explanation shall be given concerning possible alternative transport
.
3. An operating air carrier shall not be obliged to pay
compensation in accordance with Article 7, if it can prove that
the cancellation is caused by extraordinary circumstances
which could not have been avoided even if all reasonable
measures had been taken.
4. The burden of proof concerning the questions as to
whether and when the passenger has been informed of the
cancellation of the flight shall rest with the operating air
carrier.
Article 6
Delay
1. When an operating air carrier reasonably expects a flight
to be delayed beyond its scheduled time of departure:
(a) for two hours or more in the case of flights of 1 500 kilometres
or less; or
(b) for three hours or more in the case of all intra-Community
flights of more than 1 500 kilometres and of all other
flights between 1 500 and 3 500 kilometres; or
(c) for four hours or more in the case of all flights not falling
```

</details>

## q10 (single)

**Question:** Is there an EU-wide deadline for taking an airline to court over flight compensation?

**Reference:** No. Regulation 261/2004 sets no time limit; national limitation rules apply, so deadlines differ between Member States, and the Montreal Convention's 2-year limit is not relevant (section 9.2).

**Answer shown to the user:**

> No, there is no EU-wide deadline. 
> 
> Regulation (EC) No 261/2004 does not set time limits for bringing an action before national courts, and deadlines may differ between Member States [52024XC05687:A:w109:1]. This issue is subject to each individual Member State's national legislation on the limitation of actions [52024XC05687:A:w109:1]. Additionally, the 2-year limitation period under the Montreal Convention does not apply to claims brought under Regulation (EC) No 261/2004 [52024XC05687:A:w109:1].
> 
> *Note: This information is based on the EU passenger-rights texts and Commission interpretative guidelines, not legal advice for a specific case.*

<details><summary>Passages the agent retrieved</summary>

```text
[52024XC05687:A:w109:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 9.1 to Section 10, PDF p. 34 | similarity 0.802
operating air carrier, even if no contract was concluded between the passenger and the air
carrier (173).
As regards jurisdiction for claims under the Montreal Convention, the Court has clarified the following: while the territorial
jurisdiction for a claim for compensation under Regulation (EC) No 261/2004 should be assessed under Regulation (EU)
No 1215/2012, jurisdiction for a supplementary claim for further damage falling within the scope of the Montreal
Convention should be assessed under this Convention (174).
9.2. Time limit for bringing an action under Regulation (EC) No 261/2004
Regulation (EC) No 261/2004 does not set time limits for bringing an action before the national courts. This issue is subject
to the national legislation of each Member State on the limitation of action. The 2-year limitation of action under the
Montreal Convention is not relevant to claims brought under Regulation (EC) No 261/2004 and does not affect Member
States’ national legislation because the compensation measures laid down by Regulation (EC) No 261/2004 fall outside the
Convention’s scope as they aim to address an inconvenience suffered by passengers, while remaining additional to the
system for damages laid down by the Convention. Hence, the deadlines may differ between Member States (175).
10.
Notes: (173) Case C-215/18, ECLI:EU:C:2020:235, paragraph 38. (174) Case C-213/18, ECLI:EU:C:2019:927, paragraph 44. (175) Case C-139/11, ECLI:EU:C:2012:741, paragraph 33.
```
```text
[52024XC05687:A:w099:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 8.1, PDF p. 31 | similarity 0.750
Regulation (EC) No 261/2004 at any EU airport or concerning any flight from a non-EU country to such an airport (158).
To ensure that complaint procedures are dealt with efficiently and to provide a secure legal environment for air carriers and
other businesses potentially involved, the Commission recommends that passengers be advised to make complaints to:
— the national enforcement body of the country of departure in the case of EU flights and flights from the EU to a
non-EU country; and
— the national enforcement body of the country of ar rival in the case of flights from outside the EU.
Passengers who consider that an air carrier has infringed their rights should make their complaints within a reasonable time
and according to the time frames set by national la w (159).
Passengers should first complain to the air carrier. Only if they disagree with the air carrier’s answer or in the absence of any
satisfactory reply from the air carrier, passengers should lodge a complaint with a national enforcement body. The
Commission recommends that the air carrier should reply within 2 months and that no restrictions are imposed regarding
the use of one of the official languages of
Notes: (158) Article 16(2) of Regulation (EC) No 261/2004. (159) Case C-139/11, ECLI:EU:C:2012:741, paragraph 33.
```
```text
[52024XC05687:A:w110:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 9.2 to Section 10, PDF p. 34 | similarity 0.748
No 261/2004 fall outside the
Convention’s scope as they aim to address an inconvenience suffered by passengers, while remaining additional to the
system for damages laid down by the Convention. Hence, the deadlines may differ between Member States (175).
10. AIR CARRIER LIABILITY UNDER THE MONTREAL CONVENTION
The Convention for the Unification of Certain Rules for International Carriage by Air, commonly known as the ‘Montreal
Convention’, was agreed in Montreal on 28 May 1999. The EU is a contracting party to this Convention and some of the
Convention’s provisions have been incorporated into EU law by Regulation (EC) No 2027/97, which aims to protect air
passengers’ rights in the EU along with Regulation (EC) No 261/2004.
(a) Compatibility of Regulation (EC) No 261/2004 with the Montreal Convention:
The Court (176) has confirmed that the requirements to provide compensation for delay at arrival and to provide
assistance in the event of delay at departure are compatible with the Montreal Convention. In this connection, the
Court has considered that the loss of time inherent in a flight delay constitutes an ‘inconvenience’ rather than
‘damage’, which the Montreal Convention aims to address. This reasoning was based on the finding that excessive
delay will
Notes: (175) Case C-139/11, ECLI:EU:C:2012:741, paragraph 33. (176) Case C-344/04, ECLI:EU:C:2006:10, paragraphs 43, 45, 46 and 47; Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 51.
```
```text
[52024XC05687:A:w067:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.4.7 to Section 4.4.8, PDF p. 22 | similarity 0.746
in which passengers concerned by a flight cancellation are not offered re-routing allowing them to depart no
more than 1 hour before the scheduled time of departure and to reach their final destination less than 2 hours after the
scheduled time of arrival. The Court deduced from this that the right to compensation laid down in Article 7 of Regulation
(EC) No 261/2004 aims to repair a loss of time of at least 3 hours. However, such a delay does not entitle passengers to
compensation if the air carrier can prove that the long delay was caused by extraordinary circumstances that could not
have been avoided even if all reasonable measures had been taken (100) (see Section 5 on extraordinary circumstances).
4.4.8. Compensation for long delay at arrival in the case of connecting flights
The Court (101) takes the view that for the purposes of the compensation provided for in Article 7 of Regulation (EC)
No 261/2004, a delay must be assessed in relation to the scheduled time of arrival at the passenger’s final destination as
defined in Article 2, point (h), of Regulation (EC) No 261/2004, which in the case of directly connecting flights must be
understood as the
Notes: (100) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 69. (101) Case C-11/11, ECLI:EU:C:2013:106, paragraph 47.
```
```text
[32004R0261:A:w017:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 7, PDF p. 5 | similarity 0.746
(b) EUR 400 for all intra-Community flights of more than
1 500 kilometres, and for all other flights between 1 500
and 3 500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the distance, the basis shall be the last destination
at which the denial of boarding or cancellation will delay
the passenger's arrival after the scheduled time.
2. When passengers are offered re-routing to their final
destination on an alternative flight pursuant to Article 8, the
arrival time of which does not exceed the scheduled arrival
time of the flight originally booked
(a) by two hours, in respect of all flights of 1 500 kilometres
or less; or
(b) by three hours, in respect of all intra-Community flights of
more than 1 500 kilometres and for all other flights
between 1 500 and 3 500 kilometres; or
(c) by four hours, in respect of all flights not falling under (a)
or (b),
the operating air carrier may reduce the compensation
provided for in paragraph 1 by 50 %.
3. The compensation referred to in paragraph 1 shall be
paid in cash, by electronic bank transfer, bank orders or bank
cheques or, with
```

</details>

## q11 (single)

**Question:** The airline moved my flight's departure more than one hour earlier. Is that treated as a cancellation?

**Reference:** Yes. The guidelines say a flight must be regarded as cancelled if the departure is brought forward by more than 1 hour, whereas postponing by less than 3 hours without other changes is not a cancellation (section 3.2.2).

**Answer shown to the user:**

> Yes, according to the European Commission's interpretative guidelines on Regulation (EC) No 261/2004, bringing the departure time of a flight forward by more than 1 hour must be regarded as a cancellation [52024XC05687:A:w031:1]. 
> 
> *(Note: These guidelines are interpretative guidance rather than binding legislation itself, but they reflect settled EU case law on this point [52024XC05687:A:w031:1].)*
> 
> ### What this means for your rights
> Because a schedule change of this type is treated as a cancellation, you are generally entitled to:
> 1. **Reimbursement (refund), re-routing, or return** under Article 8 of Regulation (EC) No 261/2004 [32004R0261:A:article-8] [52024XC05687:A:w033:1].
> 2. **Care** (meals, refreshments, and hotel accommodation if necessary) under Article 9 [32004R0261:A:article-9] [52024XC05687:A:w033:1].
> 3. **Compensation** under Article 7, unless you were informed of the change sufficiently far in advance or the change was caused by extraordinary circumstances that could not have been avoided [32004R0261:A:article-5] [52024XC05687:A:w033:1].
> 
> ### What to check next
> * Check **how many days in advance** the airline notified you of this earlier departure, as the notice period affects your right to compensation [52024XC05687:A:w033:1].
> * Contact the airline to choose between a refund or alternative re-routing that suits your plans. 
> 
> *(This is information from the EU passenger-rights texts, not formal legal advice for your specific case.)*

<details><summary>Passages the agent retrieved</summary>

```text
[52024XC05687:A:w031:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 3.2.2 to Section 3.2.3, PDF p. 12 | similarity 0.851
is given an annotated flight number (e.g. XX 1234a instead of XX 1234) to distinguish it from the
flight on this subsequent day that has the same number. However, in this case, it could still be considered as a delayed flight
and not a cancelled flight. This should be assessed on a case-by-case basis.
By way of example, a flight is not regarded as having been ‘cancelled’ if the operating air carrier postpones the time of
departure of the flight by less than 3 hours, without making any other changes to this flight (58).
However, a flight must be regarded as having been ‘cancelled’ if the operating air carrier brings the departure time of the
flight forward by more than 1 hour (59).
3.2.3. Case of an aircraft that returns to its point of departure
The concept of ‘cancellation’ as stipulated in Article 2, point (l), of Regulation (EC) No 261/2004 also covers the case of an
aircraft taking off but, for whatever reason, being subsequently forced to return to the airport of departure, where the
passengers of the said aircraft are transferred onto other flights. Indeed, the fact that take-off occurred but that the aircraft
then returned to the
Notes: (58) Joined Cases C-146/20, C-188/20, C-196/20 and C-270/20, ECLI:EU:C:2021:1038, paragraph 87. (59) Case C-263/20, ECLI:EU:C:2021:1039, paragraph 35; Case C-395/20, ECLI:EU:C:2021:1041, paragraph 23.
```
```text
[52024XC05687:A:w030:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 3.2.1 to Section 3.2.2, PDF p. 12 | similarity 0.832
flight as such and may arise from different factors. In particular, the Court highlighted that these circumstances (i.e. the
announcement of a flight as being ‘delayed’ or ‘cancelled’) can ‘be attributable to inaccurate classifications or to factors
obtaining in the airport concerned or, yet again, they may be unavoidable given the waiting time and the fact that it is
necessary for the passengers concerned to spend the night in a hotel’.
3.2.2. Change of departure time
Without prejudice to Section 3.3.1 and in order to avoid a situation where air carriers present a flight as continuously
‘delayed’ instead of ‘cancelled’, it was considered useful to highlight the distinction between a ‘cancellation’ and a ‘delay’. A
flight may generally tend to be considered as cancelled when its flight number changes, but in practice, this might not
always be a determining criterion. Indeed, a flight may experience such a long delay that it departs the day after it was
scheduled and therefore is given an annotated flight number (e.g. XX 1234a instead of XX 1234) to distinguish it from the
flight on this subsequent day that has the same number. However, in this case, it could still be considered as a delayed
```
```text
[52024XC05687:A:w074:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.4.12 to Section 4.4.13, PDF pp. 23-24 | similarity 0.830
of arrival;
— if passengers are informed less than 7 days before the scheduled departure, re-routing must allow them to depart no
more than 1 hour before the original scheduled time of departure and to reach their final destination less than 2 hours
after the original scheduled time of arrival (112).
4.4.13. Re-routing and arrival more than 2 hours after the scheduled arrival time but less than 3 hours
The Court has confirmed that passengers who are informed of the cancellation of their flight less than 7 days before the
scheduled time of departure are entitled to the compensation referred to in Article 5(1), point (c), if the re-routing offered
by the air carrier enabled them to reach the final destination more than 2 hours but less than 3 hours after the scheduled
time of arrival of the cancelled flight (113).
However, if passengers re-route themselves, because they have been informed or have sufficient evidence that their flight
will arrive at its destination with a long delay, they are not eligible for compensation if they reach their final destination
(with the new flight) with a delay of less than 3 hours after the scheduled arrival time of their originally booked
Notes: (112) Case C-130/18, ECLI:EU:C:2018:496, paragraph 23. (113) Case C-130/18, ECLI:EU:C:2018:496, paragraph 23.
```
```text
[52024XC05687:A:w029:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 3.2.1, PDF p. 12 | similarity 0.818
the original flight is abandoned and passengers of this flight join
passengers on a flight that was also planned, but independently of the original flight. Article 2, point (l), does not require
an express decision of cancellation by the air carrier (55).
A flight that was carried out between the places of departure and arrival in accordance with the planned schedule but
during which an unscheduled stopover took place cannot be regarded as cancelled (56).
By contrast, the Court (57) considers that it cannot, as a rule, be concluded that there is a flight delay or cancellation on the
basis of a ‘delay’ or a ‘cancellation’ being shown on the airport departures board or announced by the air carrier’s staff.
Similarly, the fact that passengers recover their luggage or obtain new boarding cards is not, as a rule, a deciding factor to
ascertain that a flight has been cancelled. These circumstances are not connected with the objective characteristics of the
flight as such and may arise from different factors. In particular, the Court highlighted that these circumstances (i.e. the
announcement of a flight as being ‘delayed’ or ‘cancelled’) can ‘be attributable to inaccurate classifications or to factors
obtaining in the
Notes: (55) Case C-83/10, ECLI:EU:C:2011:652, paragraph 29. (56) Case C-32/16, ECLI:EU:C:2016:753, paragraph 27. (57) Joined Cases C-402/07 and C-432/07, ECLI:EU:2009:716, paragraphs 37 and 38.
```
```text
[52024XC05687:A:w033:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 3.2.4 to Section 3.3.1, PDF p. 13 | similarity 0.810
not serve the same town,
city or region, passengers are entitled to compensation for cancellation of a flight (62).
3.2.5. Burden of proof in the event of cancellation
Article 5(4) of Regulation (EC) No 261/2004 imposes on air carriers the burden of proof as regards whether and when the
passengers have been individually informed of the cancellation of their flight.
On the obligation to inform passengers of a cancellation, see also Section 4.4.6.
3.2.6. Rights associated with cancellation
Cancellation of a flight gives: (i) a right to reimbursement, re-routing or return as defined in Article 8 of Regulation (EC)
No 261/2004; (ii) a right to ‘care’ as defined in Article 9; and (iii) under Article 5(1), point (c), a right to ‘compensation’ as
defined in Article 7. The underlying principle of Article 5(1), point (c), is that compensation is to be paid if the passenger
has not been informed of the cancellation sufficiently in advance.
However, compensation does not have to be paid if the air carrier can prove, in accordance with Article 5(3), that the
cancellation is caused by extraordinary circumstances that could not have been avoided even if all reasonable measures had
been taken (63).
3.3. Delay
3.3.1.
Notes: (62) Case C-253/21, ECLI:EU:C:2021:840, paragraph 27. (63) See Section 5 on extraordinary circumstances.
```

</details>

## q12 (single)

**Question:** My train arrived 75 minutes late. What compensation can I claim?

**Reference:** At least 25% of the ticket price for a delay of 60 to 119 minutes (50% for 120 minutes or more), unless the ticket was reimbursed under Art. 18 or an exemption applies (Art. 19(1)).

**Answer shown to the user:**

> For a train delay of 75 minutes, you are entitled to compensation equal to **25% of the ticket price** [32021R0782:A:w054:1]. 
> 
> ### Conditions and Exceptions to Check:
> * **Delay Threshold:** The EU rail regulations set the minimum compensation at 25% for delays between 60 and 119 minutes, and 50% for delays of 120 minutes or more [32021R0782:A:w054:1].
> * **Knowledge before purchase:** You do not have a right to compensation if you were informed of the delay before buying your ticket [32021R0782:A:w058:1].
> * **Re-routing:** If you were re-routed and the resulting delay on arrival was under 60 minutes, compensation does not apply [32021R0782:A:w058:1].
> * **Extraordinary circumstances:** A railway undertaking is not obliged to pay compensation if it proves the delay was caused directly by extraordinary circumstances not connected with railway operations (such as extreme weather conditions, major natural disasters, or major public health crises), fault on the part of the passenger, or certain third-party behaviours that could not be avoided [32021R0782:A:w058:1].
> * **Minimum payout threshold:** Railway undertakings may set a minimum threshold under which compensation payments will not be paid, but this cannot exceed €4 per ticket [32021R0782:A:w057:1].
> 
> ### What to do next:
> You can request compensation from the railway undertaking. While they may offer vouchers, you have the right to request that compensation be paid in money [32021R0782:A:w057:1]. The payment must be made within one month after submitting your request [32021R0782:A:w057:1]. 
> 
> *(Note: This information is based on Regulation (EU) 2021/782 on rail passenger rights and serves as general guidance, not formal legal advice.)*

<details><summary>Passages the agent retrieved</summary>

```text
[32021R0782:A:w054:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 18 to Article 19, PDF p. 19 | similarity 0.773
common form referred to in paragraph 6. Railway
undertakings shall not reject a request for reimbursement solely on the grounds that the passenger has not used that
form. If a request is not sufficiently precise, the railway undertaking shall ask the passenger to clarify the request and shal l
assist the passenger to do so.
Article 19
Compensation
1. Without losing the right of transport, a passenger is entitled to compensation for delays from the railway undertaking
if he or she is facing a delay between the places of departure and final destination stated in the ticket or through-ticket
for which the cost has not been reimbursed in accordance with Article 18. The minimum compensation for delays
shall be as follows:
(a) 25 % of the ticket price for a delay of 60 to 119 minutes;
(b) 50 % of the ticket price for a delay of 120 minutes or more.
2. Paragraph 1 shall also apply to passengers who hold a travel pass or season ticket. If those passengers encounter
recurrent delays or cancellations during the period of validity of the travel pass or season ticket, they shall be entitled to
adequate compensation in accordance with the railway undertaking’s
```
```text
[32021R0782:A:w055:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19, PDF p. 19 | similarity 0.752
hold a travel pass or season ticket. If those passengers encounter
recurrent delays or cancellations during the period of validity of the travel pass or season ticket, they shall be entitled to
adequate compensation in accordance with the railway undertaking’s compensation arrangements. These arrangements
shall state the criteria for determining delay and for the calculation of the compensation. Where delays of less than
60 minutes occur repeatedly during the period of validity of the travel pass or season ticket, the delays may be counted
cumulatively and passengers may be compensated in accordance with the railway undertaking’s compensation arrangements
.
3. Without prejudice to paragraph 2, compensation for delay shall be calculated in relation to the full price which the
passenger actually paid for the delayed service. Where the transport contract is for a return journey, compensation for
delay on either the outward or the return leg shall be calculated in relation to the price indicated for that leg of the
journey on the ticket. Where there is no such indication of the price of the individual legs of the journey, the
compensation shall be calculated in relation to half of the price paid for the ticket. In the same way,
```
```text
[32021R0782:A:w059:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19 to Article 20, PDF pp. 20-21 | similarity 0.748
prevent;
(b) fault on the part of the passenger; or
(c) the behaviour of a third party which the railway undertaking, in spite of having taken the care required in the
particular circumstances of the case, was unable to avoid and the consequences of which it was unable to prevent,
such as persons on the track, cable theft, on-board emergencies, law enforcement activities, sabotage or terrorism.
Strikes by the personnel of the railway undertaking, acts or omissions by another undertaking using the same railway
infrastructure and acts or omissions of the infrastructure and station managers are not covered by the exemption referred
to in point (c) of the first subparagraph.
Article 20
Assistance
1. In the case of a delay in arrival or departure, or cancellation of a service, passengers shall be kept informed of the
situation and of the estimated departure time and estimated arrival time of the service or the replacement service by the
railway undertaking or by the station manager as soon as such information is available. Where ticket vendors and tour
operators have such information, they shall also provide it to the passenger.
2. Where the delay referred to in paragraph 1 amounts to 60 minutes
```
```text
[32021R0782:A:w058:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19, PDF p. 20 | similarity 0.746
by financial transaction costs such as fees, telephone costs
or stamps. Railway undertakings may introduce a minimum threshold under which payments for compensation will not
be paid. This threshold shall not exceed EUR 4 per ticket.
9. Passengers shall not have any right to compensation if they are informed of a delay before buying a ticket, or if a
delay due to continuation on a different service or re-routing remains below 60 minutes.
10. A railway undertaking shall not be obliged to pay compensation if it can prove that the delay, missed connection
or cancellation was caused directly by, or was inherently linked with:
(a) extraordinary circumstances not connected with the operation of the railway, such as extreme weather conditions,
major natural disasters or major public health crises, which the railway undertaking, in spite of having taken the care
required in the particular circumstances of the case, was unable to avoid and the consequences of which it was unable
to prevent;
(b) fault on the part of the passenger; or
(c) the behaviour of a third party which the railway undertaking, in spite of having taken the care required in the
particular circumstances of the case, was unable to avoid
```
```text
[32021R0782:A:w057:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19, PDF p. 20 | similarity 0.741
38(2).
6. Member States may require railway undertakings to accept requests for compensation by particular means of
communication, provided that the request does not create discriminatory effects. Passengers shall have the right to
submit their requests using the common form referred to in paragraph 5. Railway undertakings shall not reject a
request for compensation solely on the grounds that the passenger has not used that form. If a request is not sufficiently
precise, the railway undertaking shall ask the passenger to clarify the request and shall assist the passenger to do so.
7. The compensation of the ticket price shall be paid within one month after the submission of the request for
compensation. The compensation may be paid in vouchers and/or other services if the terms are flexible, in particular
regarding the validity period and destination. The compensation shall be paid in money at the request of the passenger.
8. The compensation of the ticket price shall not be reduced by financial transaction costs such as fees, telephone costs
or stamps. Railway undertakings may introduce a minimum threshold under which payments for compensation will not
be paid. This threshold shall not exceed EUR 4 per ticket.
9. Passengers shall not
```

</details>

## q13 (single)

**Question:** How quickly must a railway pay delay compensation, and can it pay me in vouchers?

**Reference:** Within one month of the request; vouchers or other services are allowed only if their terms are flexible, and the passenger can ask for money (Art. 19(7)).

**Answer shown to the user:**

> Under EU rail passenger rights rules (Regulation (EU) 2021/782), compensation must be paid within **one month** after you submit your request [32021R0782:A:w057:1].
> 
> As for vouchers:
> * **Can they pay you in vouchers?** Yes, the compensation may be paid in vouchers and/or other services, but **only if the terms are flexible** (specifically regarding their validity period and destination) [32021R0782:A:w057:1].
> * **Your right to money:** You have the right to request payment in money instead, and the railway must pay you in cash/money if you ask for it [32021R0782:A:w057:1].
> 
> *(Note: This information is based on Regulation (EU) 2021/782 on rail passenger rights and does not constitute legal advice.)*

<details><summary>Passages the agent retrieved</summary>

```text
[32021R0782:A:w057:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19, PDF p. 20 | similarity 0.745
38(2).
6. Member States may require railway undertakings to accept requests for compensation by particular means of
communication, provided that the request does not create discriminatory effects. Passengers shall have the right to
submit their requests using the common form referred to in paragraph 5. Railway undertakings shall not reject a
request for compensation solely on the grounds that the passenger has not used that form. If a request is not sufficiently
precise, the railway undertaking shall ask the passenger to clarify the request and shall assist the passenger to do so.
7. The compensation of the ticket price shall be paid within one month after the submission of the request for
compensation. The compensation may be paid in vouchers and/or other services if the terms are flexible, in particular
regarding the validity period and destination. The compensation shall be paid in money at the request of the passenger.
8. The compensation of the ticket price shall not be reduced by financial transaction costs such as fees, telephone costs
or stamps. Railway undertakings may introduce a minimum threshold under which payments for compensation will not
be paid. This threshold shall not exceed EUR 4 per ticket.
9. Passengers shall not
```
```text
[32021R0782:A:w054:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 18 to Article 19, PDF p. 19 | similarity 0.733
common form referred to in paragraph 6. Railway
undertakings shall not reject a request for reimbursement solely on the grounds that the passenger has not used that
form. If a request is not sufficiently precise, the railway undertaking shall ask the passenger to clarify the request and shal l
assist the passenger to do so.
Article 19
Compensation
1. Without losing the right of transport, a passenger is entitled to compensation for delays from the railway undertaking
if he or she is facing a delay between the places of departure and final destination stated in the ticket or through-ticket
for which the cost has not been reimbursed in accordance with Article 18. The minimum compensation for delays
shall be as follows:
(a) 25 % of the ticket price for a delay of 60 to 119 minutes;
(b) 50 % of the ticket price for a delay of 120 minutes or more.
2. Paragraph 1 shall also apply to passengers who hold a travel pass or season ticket. If those passengers encounter
recurrent delays or cancellations during the period of validity of the travel pass or season ticket, they shall be entitled to
adequate compensation in accordance with the railway undertaking’s
```
```text
[32021R0782:A:w055:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19, PDF p. 19 | similarity 0.717
hold a travel pass or season ticket. If those passengers encounter
recurrent delays or cancellations during the period of validity of the travel pass or season ticket, they shall be entitled to
adequate compensation in accordance with the railway undertaking’s compensation arrangements. These arrangements
shall state the criteria for determining delay and for the calculation of the compensation. Where delays of less than
60 minutes occur repeatedly during the period of validity of the travel pass or season ticket, the delays may be counted
cumulatively and passengers may be compensated in accordance with the railway undertaking’s compensation arrangements
.
3. Without prejudice to paragraph 2, compensation for delay shall be calculated in relation to the full price which the
passenger actually paid for the delayed service. Where the transport contract is for a return journey, compensation for
delay on either the outward or the return leg shall be calculated in relation to the price indicated for that leg of the
journey on the ticket. Where there is no such indication of the price of the individual legs of the journey, the
compensation shall be calculated in relation to half of the price paid for the ticket. In the same way,
```
```text
[32021R0782:A:w049:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 15 to Article 18, PDF pp. 17-18 | similarity 0.717
except where damage was caused by the negligence or fault of
the passenger or where the person who received the advance payment was not the person entitled to compensation.
Article 16
Contestation of liability
Even if the railway undertaking contests its responsibility for physical injury to a passenger whom it conveys, it shall
make every reasonable effort to assist the passenger with his or her claim for compensation for damage from third
parties.
Article 17
Liability for delays, missed connections and cancellations
Subject to the provisions of this Chapter, the liability of railway undertakings in respect of delays, missed connections and
cancellations shall be governed by Chapter II of Title IV of Annex I.
Article 18
Reimbursement and re-routing
1. Where it is reasonably to be expected, either at departure or in the event of a missed connection or a cancellation,
that arrival at the final destination under the transport contract will be subject to a delay of 60 minutes or more, the
railway undertaking operating the delayed or cancelled service shall immediately offer the passenger the choice between
one of the following options, and shall make the necessary arrangements:
(a) reimbursement of the full cost of the ticket, under
```
```text
[32021R0782:A:w056:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19, PDF pp. 19-20 | similarity 0.707
journey on the ticket. Where there is no such indication of the price of the individual legs of the journey, the
compensation shall be calculated in relation to half of the price paid for the ticket. In the same way, the price for a
delayed service provided under any other form of transport contract entitling the passenger to travel for two or more
subsequent legs shall be calculated in proportion to the full price.
4. The calculation of the period of delay shall not take into account any delay that the railway undertaking can
demonstrate as having occurred outside the Union.
5. The Commission shall adopt an implementing act establishing a common form for compensation requests under
this Regulation by 7 June 2023. That common form shall be established in a format which is accessible to persons with
disabilities and persons with reduced mobility. That implementing act shall be adopted in accordance with the examination
procedure referred to in Article 38(2).
6. Member States may require railway undertakings to accept requests for compensation by particular means of
communication, provided that the request does not create discriminatory effects. Passengers shall have the right to
submit their requests using the common form
```

</details>

## q14 (single)

**Question:** My train has been cancelled. What choices must the railway undertaking offer me?

**Reference:** Where a delay of 60 minutes or more at the final destination is expected, or on cancellation: reimbursement (with a return service where relevant), continuation or re-routing at the earliest opportunity, or re-routing at a later date at the passenger's convenience (Art. 18(1)).

**Answer shown to the user:**

> NEED DETAILS: When a train is cancelled (or reasonably expected to cause a delay of 60 minutes or more to your final destination), the railway undertaking must immediately offer you a choice of three options [32021R0782:A:w049:1, 32021R0782:A:w050:1]:
> 
> 1. **Reimbursement** of the full cost of the ticket (under the conditions it was paid for) for the parts of the journey not made, and also for parts already made if your journey no longer serves any purpose in relation to your original travel plan. When relevant, this includes a return service to your first point of departure at the earliest opportunity [32021R0782:A:w050:1].
> 2. **Continuation or re-routing** to your final destination under comparable transport conditions at the earliest opportunity [32021R0782:A:w050:1].
> 3. **Continuation or re-routing** to your final destination under comparable transport conditions at a later date at your convenience [32021R0782:A:w050:1].
> 
> To confirm which specific conditions or additional assistance apply to your situation, please provide:
> * Whether your arrival at your final destination is expected to be delayed by 60 minutes or more [32021R0782:A:w049:1].
> * Whether you are requesting re-routing or reimbursement [32021R0782:A:w050:1].
> 
> *(This information is based on EU Regulation 2021/782 on rail passenger rights and does not constitute formal legal advice.)*

<details><summary>Passages the agent retrieved</summary>

```text
[32021R0782:A:w050:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 18, PDF p. 18 | similarity 0.843
or more, the
railway undertaking operating the delayed or cancelled service shall immediately offer the passenger the choice between
one of the following options, and shall make the necessary arrangements:
(a) reimbursement of the full cost of the ticket, under the conditions by which it was paid, for the part or parts of his or
her journey not made and for the part or parts already made if the journey is no longer serving any purpose in
relation to the passenger’s original travel plan, together with, when relevant, a return service to the first point of
departure at the earliest opportunity;
(b) continuation or re-routing, under comparable transport conditions, to the final destination at the earliest opportunity;
(c) continuation or re-routing, under comparable transport conditions, to the final destination at a later date at the
passenger’s convenience.
2. Where, for the purposes of points (b) and (c) of paragraph 1, comparable re-routing is operated by the same railway
undertaking or another undertaking is commissioned to perform the re-routing, this shall not generate additional costs to
the passenger. This requirement also applies where the re-routing involves the use of transport of a higher service class
and alternative modes of transport. Railway
```
```text
[32021R0782:A:w049:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 15 to Article 18, PDF pp. 17-18 | similarity 0.810
except where damage was caused by the negligence or fault of
the passenger or where the person who received the advance payment was not the person entitled to compensation.
Article 16
Contestation of liability
Even if the railway undertaking contests its responsibility for physical injury to a passenger whom it conveys, it shall
make every reasonable effort to assist the passenger with his or her claim for compensation for damage from third
parties.
Article 17
Liability for delays, missed connections and cancellations
Subject to the provisions of this Chapter, the liability of railway undertakings in respect of delays, missed connections and
cancellations shall be governed by Chapter II of Title IV of Annex I.
Article 18
Reimbursement and re-routing
1. Where it is reasonably to be expected, either at departure or in the event of a missed connection or a cancellation,
that arrival at the final destination under the transport contract will be subject to a delay of 60 minutes or more, the
railway undertaking operating the delayed or cancelled service shall immediately offer the passenger the choice between
one of the following options, and shall make the necessary arrangements:
(a) reimbursement of the full cost of the ticket, under
```
```text
[32021R0782:A:w052:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 18, PDF pp. 18-19 | similarity 0.805
time of the delayed or cancelled service or the missed connection, the passenger shall be entitled to conclude
such a contract with other providers of public transport services by rail, coach or bus. The railway undertaking shall
reimburse the passenger for the necessary, appropriate and reasonable costs that he or she incurs.
This paragraph shall not affect national laws, regulations or administrative provisions which grant more favourable re-routing
conditions to passengers.
4. Re-routing transport service providers shall provide persons with disabilities and persons with reduced mobility with
a comparable level of assistance and accessibility when offering an alternative service. Re-routing transport service
providers may provide persons with disabilities and persons with reduced mobility with alternative services which are
appropriate to their needs and which differ from those offered to other passengers.
5. The reimbursements referred to in point (a) of paragraph 1 and in paragraph 3 shall be paid within 30 days after
the receipt of the request. Member States may require railway undertakings to accept such requests by particular means of
communication, provided that the request does not create discriminatory effects. The reimbursement may take the form
of vouchers and/or the provision of other services provided that the terms
```
```text
[32021R0782:A:w051:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 18, PDF p. 18 | similarity 0.805
another undertaking is commissioned to perform the re-routing, this shall not generate additional costs to
the passenger. This requirement also applies where the re-routing involves the use of transport of a higher service class
and alternative modes of transport. Railway undertakings shall make reasonable efforts to avoid additional connections
and to ensure that delay in the total travel time is as short as possible. Passengers shall not be downgraded to transport
facilities of a lower class unless such facilities are the only re-routing means available.
3. Without prejudice to paragraph 2, the railway undertaking may allow the passenger, at his or her request, to
conclude contracts with other providers of transport services which enable the passenger to reach the final destination
under comparable conditions, in which case the railway undertaking shall reimburse the passenger for the costs that he or
she incurs.
Where the available re-routing options are not communicated to the passenger within 100 minutes from the scheduled
departure time of the delayed or cancelled service or the missed connection, the passenger shall be entitled to conclude
such a contract with other providers of public transport services by rail, coach or bus. The railway undertaking shall
reimburse the passenger
```
```text
[32021R0782:A:w054:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 18 to Article 19, PDF p. 19 | similarity 0.788
common form referred to in paragraph 6. Railway
undertakings shall not reject a request for reimbursement solely on the grounds that the passenger has not used that
form. If a request is not sufficiently precise, the railway undertaking shall ask the passenger to clarify the request and shal l
assist the passenger to do so.
Article 19
Compensation
1. Without losing the right of transport, a passenger is entitled to compensation for delays from the railway undertaking
if he or she is facing a delay between the places of departure and final destination stated in the ticket or through-ticket
for which the cost has not been reimbursed in accordance with Article 18. The minimum compensation for delays
shall be as follows:
(a) 25 % of the ticket price for a delay of 60 to 119 minutes;
(b) 50 % of the ticket price for a delay of 120 minutes or more.
2. Paragraph 1 shall also apply to passengers who hold a travel pass or season ticket. If those passengers encounter
recurrent delays or cancellations during the period of validity of the travel pass or season ticket, they shall be entitled to
adequate compensation in accordance with the railway undertaking’s
```

</details>

## q15 (single)

**Question:** Am I allowed to take my bicycle on a train under the EU rail passenger rights regulation?

**Reference:** Yes, where appropriate for a reasonable fee, but railway undertakings may restrict it for safety or operational reasons such as peak-hour capacity, rolling stock or bicycle size (Art. 6(1),(3)).

**Answer shown to the user:**

> Yes, under Regulation (EU) 2021/782 on rail passenger rights, passengers are generally entitled to take bicycles on board trains, subject to certain conditions and limitations [32021R0782:A:w035:1]. 
> 
> ### Key Rules and Conditions:
> * **Fees and Reservations:** Carriage is subject to a reasonable fee where appropriate [32021R0782:A:w035:1]. If a train requires a reservation, it must be possible to make one for your bicycle [32021R0782:A:w035:1]. If you have a valid bicycle reservation and your bicycle is refused without a duly justified reason, you are entitled to re-routing or reimbursement, compensation, and assistance [32021R0782:A:w035:1].
> * **Stowage and Conduct:** If designated bicycle spaces are available on board, you must stow your bicycle in those places [32021R0782:A:w036:1]. If they are not available, you must keep your bicycle under supervision and make all reasonable efforts to ensure it causes no harm or damage to other passengers, luggage, mobility equipment, or rail operations [32021R0782:A:w036:1].
> * **Scope:** These rights apply to bicycles that can be readily ridden before and after the rail journey (bicycles in packages or bags fall under rules for regular luggage) [32021R0782:A:w010:1].
> 
> ### Limitations and Restrictions:
> * **Operational and Safety Limits:** Railway undertakings may restrict the right to take bicycles on board for safety or operational reasons, such as capacity limits during peak hours, rolling stock limitations, or based on the weight and dimensions of the bicycles [32021R0782:A:w036:1]. 
> * **Undertaking Obligations:** Railway undertakings must publish their transport conditions for bicycles and up-to-date capacity information on their official websites [32021R0782:A:w036:1].
> 
> *Note: This information is drawn directly from EU rail passenger rights texts and does not constitute legal advice.*

<details><summary>Passages the agent retrieved</summary>

```text
[32021R0782:A:w036:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 6, PDF p. 13 | similarity 0.790
accordance with Article 18, compensation in
accordance with Article 19 and assistance in accordance with Article 20(2).
2. Where designated places for bicycles are available on board the train, passengers shall stow their bicycles in such
places. Where such places are not available, passengers shall keep their bicycles under supervision, and shall make all
reasonable efforts to ensure that their bicycles cause no harm or damage to other passengers, mobility equipment, luggage
or rail operations.
3. Railway undertakings may restrict the right of passengers to take bicycles on board the train for safety or operational
reasons, in particular as a result of capacity limits applicable during peak hours, or where rolling stock does not
permit it. Railway undertakings may also restrict the carriage of bicycles based on the weights and dimensions of the
bicycles concerned. They shall publish their conditions for the transport of bicycles, including up-to-date information on
the availability of capacity, by using the telematics applications referred to in Regulation (EU) No 454/2011 on their
official websites.
4. When initiating procurement procedures for new rolling stock, or when performing a major upgrade of existing
rolling stock resulting in the need for a new vehicle authorisation for placing on
```
```text
[32021R0782:A:w035:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 5 to Article 6, PDF pp. 12-13 | similarity 0.783
to social tariffs, railway undertakings, ticket vendors or tour operators shall offer contract conditions
and tariffs to the general public without direct or indirect discrimination on the basis of the passenger’s nationality or of
the place of establishment within the Union of the railway undertaking, ticket vendor or tour operator.
The first paragraph of this Article also applies to railway undertakings and ticket vendors when accepting reservations
from passengers in accordance with Article 11.
Article 6
Bicycles
1. Subject to the limitations set out in paragraph 3, and where appropriate for a reasonable fee, passengers shall be
entitled to take bicycles on board the train.
On trains for which a reservation is required, it shall be possible to make a reservation for the carriage of a bicycle.
Where a passenger has made a reservation for a bicycle and the carriage of that bicycle is refused without a duly justified
reason, the passenger shall be entitled to re-routing or reimbursement in accordance with Article 18, compensation in
accordance with Article 19 and assistance in accordance with Article 20(2).
2. Where designated places for bicycles are available on board the train, passengers shall stow their bicycles in such
places. Where such places
```
```text
[32021R0782:A:w038:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 6 to Article 7, PDF pp. 13-14 | similarity 0.775
each train composition shall have at least four places for bicycles.
Member States may set a number higher than four as the minimum adequate number for certain types of services, in
which case that number shall apply instead of the number identified in accordance with the second subparagraph.
5. Railway undertakings may establish, and keep up-to-date, plans on how to increase and improve the transport of
bicycles, and on other solutions encouraging combined use of railways and bicycles.
The competent authorities, as defined in point (b) of Article 2 of Regulation (EC) No 1370/2007 of the European
Parliament and of the Council (13), may establish such plans for services provided under public service contracts.
Member States may require that such plans are established by those competent authorities or by railway undertakings
operating on their territory.
6. The plans referred to in paragraph 5 shall be established following consultation of the public and relevant
representative organisations. Those plans shall be published on the website of the railway undertaking or the
competent authority, as appropriate.
Article 7
Exclusion of waiver and stipulation of limits
1. Obligations towards passengers pursuant to this Regulation may not be limited or waived, notably by a derogation
Notes: (13) Regulation (EC) No 1370/2007 of the European Parliament and of the Council of 23 October 2007 on public passenger transport services by rail and by road and repealing Council Regulations (EEC) Nos 1191/69 and 1107/70 (OJ L 315, 3.12.2007, p. 1).
```
```text
[32021R0782:A:w009:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Recital (17), PDF p. 4 | similarity 0.772
adequate number of bicycle places for a train composition should be determined taking into consideration the
size of train composition, the type of service and the demand for transport of bicycles. Railway undertakings
should have the possibility to establish plans with concrete numbers of bicycle places for their services, after
consulting the public. Where railway undertakings choose not to establish plans, a statutory number should apply.
That statutory number should also serve as guidance by railway undertakings when establishing their plans. A
number which is below the statutory number should be considered adequate only where it is justified by special
circumstances such as operation of rail services in winter time where there is clearly no or low demand for the
transport of bicycles. Furthermore, in some Member States demand for the transport of bicycles is particularly high
as regards certain types of services. Therefore, Member States should have the possibility to determine the
minimum adequate numbers of bicycle places for certain types of services. These numbers should prevail over
the concrete numbers as mentioned in any plans of the railway undertakings. This should not impede the free
movement of railway rolling stock within the Union. Passengers should be informed of
```
```text
[32021R0782:A:w010:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Recital (17) to Recital (20), PDF p. 4 | similarity 0.761
certain types of services. These numbers should prevail over
the concrete numbers as mentioned in any plans of the railway undertakings. This should not impede the free
movement of railway rolling stock within the Union. Passengers should be informed of the space available for
bicycles.
(18) The rights and obligations regarding carriage of bicycles on trains should apply to bicycles that can be readily
ridden prior to and after the rail journey. Carriage of bicycles in packages and bags, as applicable, is covered by the
provisions of this Regulation relating to luggage.
(19) Rail passengers’ rights to rail services include the receipt of information regarding the service both before and
during the journey. Railway undertakings, ticket vendors and tour operators should provide general information on
the rail service in advance of travel. That information should be provided in accessible formats for persons with
disabilities or persons with reduced mobility. Railway undertakings and, where possible, ticket vendors and tour
operators should provide the passenger during the journey with further information required by this Regulation.
Where a station manager has such information, he or she should also provide the information to the passengers.
(20) The size of ticket vendors varies substantially from
```

</details>

## q16 (single)

**Question:** Can a railway refuse delay compensation because its own staff were on strike?

**Reference:** No. Strikes by the railway undertaking's personnel are expressly not covered by the third-party exemption in Art. 19(10)(c).

**Answer shown to the user:**

> No. Under EU rail passenger rights legislation (Regulation (EU) 2021/782), a railway undertaking cannot refuse delay compensation on the grounds of strikes by its own personnel `[32021R0782:A:w059:1]`.
> 
> The regulation explicitly states that strikes by the personnel of the railway undertaking are not covered by the exemptions that would otherwise relieve the railway from paying compensation `[32021R0782:A:w059:1]`, nor should such strikes affect its liability for delays `[32021R0782:A:w020:1]`. 
> 
> *(Note: This is information from the texts, not legal advice for your case.)*

<details><summary>Passages the agent retrieved</summary>

```text
[32021R0782:A:w059:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19 to Article 20, PDF pp. 20-21 | similarity 0.767
prevent;
(b) fault on the part of the passenger; or
(c) the behaviour of a third party which the railway undertaking, in spite of having taken the care required in the
particular circumstances of the case, was unable to avoid and the consequences of which it was unable to prevent,
such as persons on the track, cable theft, on-board emergencies, law enforcement activities, sabotage or terrorism.
Strikes by the personnel of the railway undertaking, acts or omissions by another undertaking using the same railway
infrastructure and acts or omissions of the infrastructure and station managers are not covered by the exemption referred
to in point (c) of the first subparagraph.
Article 20
Assistance
1. In the case of a delay in arrival or departure, or cancellation of a service, passengers shall be kept informed of the
situation and of the estimated departure time and estimated arrival time of the service or the replacement service by the
railway undertaking or by the station manager as soon as such information is available. Where ticket vendors and tour
operators have such information, they shall also provide it to the passenger.
2. Where the delay referred to in paragraph 1 amounts to 60 minutes
```
```text
[32021R0782:A:w020:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Recital (37) to Recital (38), PDF pp. 6-7 | similarity 0.743
third parties, the railway undertaking should not
be obliged to provide compensation for the delay. Railway undertakings should prove that they could neither
foresee nor avoid such events, nor could they prevent the delay, even if all reasonable measures had been taken,
including appropriate preventive maintenance of their rolling stock. Strikes by the personnel of the railway undertaking
, and actions or omissions by other railway operators using the same infrastructure, infrastructure manager
or station manager, should not affect the liability for delays. The circumstances in which railway undertakings are
not obliged to pay compensation should be objectively justified. Where a communication or a document of the
railway infrastructure manager, a public authority or other body independent from the railway undertakings,
indicating the circumstances on which the railway undertaking relies in order to be exempt from the obligation
to pay compensation, is available to railway undertakings, they should bring such communications or documents
to the attention of passengers and, where relevant, to that of the authorities concerned.
(38) Railway undertakings should be encouraged to simplify the procedure for passengers to apply for compensation or
reimbursement. In particular, Member States should have the possibility to require that railway undertakings accept
applications
```
```text
[32021R0782:A:w058:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19, PDF p. 20 | similarity 0.740
by financial transaction costs such as fees, telephone costs
or stamps. Railway undertakings may introduce a minimum threshold under which payments for compensation will not
be paid. This threshold shall not exceed EUR 4 per ticket.
9. Passengers shall not have any right to compensation if they are informed of a delay before buying a ticket, or if a
delay due to continuation on a different service or re-routing remains below 60 minutes.
10. A railway undertaking shall not be obliged to pay compensation if it can prove that the delay, missed connection
or cancellation was caused directly by, or was inherently linked with:
(a) extraordinary circumstances not connected with the operation of the railway, such as extreme weather conditions,
major natural disasters or major public health crises, which the railway undertaking, in spite of having taken the care
required in the particular circumstances of the case, was unable to avoid and the consequences of which it was unable
to prevent;
(b) fault on the part of the passenger; or
(c) the behaviour of a third party which the railway undertaking, in spite of having taken the care required in the
particular circumstances of the case, was unable to avoid
```
```text
[52024XC05687:A:w077:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.1, PDF pp. 24-25 | similarity 0.726
(a) the existence of extraordinary circumstances and the link between these circumstances and the delay or the
cancellation; and
(b) the fact that this delay or cancellation could not have been avoided even though the air carrier took all reasonable
measures (see Section 5.3).
A given extraordinary circumstance can produce more than one cancellation or delay at final destination, such as in the case
of an air traffic management decision as referred to in recital 15 of Regulation (EC) No 261/2004.
As a derogation from the main rule – i.e. the payment of compensation, which reflects the objective of consumer
protection – the exemption in Article 5(3) must be interpreted strictly (118). Therefore, all extraordinary circumstances
surrounding events such as those listed in recital 14 of Regulation (EC) No 261/2004 – i.e. political instability,
meteorological conditions incompatible with the operation of the flight concerned, security risks, unexpected flight safety
shortcomings and strikes that affect the operation of an operating air carrier – are not necessarily grounds for an
exemption from the obligation to pay compensation, but require a case-by-case assessment (119).
The Court has developed two cumulative conditions for the classification of events as extraordinary circumstances, which
have been consistently
Notes: (118) Case C-549/07, ECLI:EU:C:2008:771, paragraph 17, and the case-law cited. (119) Case C-549/07, ECLI:EU:C:2008:771, paragraph 22.
```
```text
[52024XC05687:A:w088:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.2.3 to Section 5.3, PDF p. 28 | similarity 0.724
a flight at a congested airport due to bad weather conditions, including if these conditions result in capacity
shortages, would stem from extraordinary circumstances.
i) External strikes
Strikes that are external to the activity of an air carrier, such as strike action taken by air traffic controllers or airport staff,
may constitute extraordinary circumstances given that such external strike action does not fall within the exercise of the air
carrier’s activity and is thus beyond its actual control (145).
j) Shortage of staff providing baggage loading services
A situation where there is an insufficient number of staff of the airport operator responsible for the operations of loading
baggage onto planes may constitute an extraordinary circumstance (146).
5.3. Reasonable measures an air carrier can be expected to take in extraordinary circumstances
Whenever extraordinary circumstances arise, an air carrier must, in order to be released from the obligation to pay
compensation, show that it could not have avoided them even if it had taken all reasonable measures to this effect.
In other words, if such circumstances do arise, it is incumbent on the operating air carrier to demonstrate that it adopted
measures appropriate to the situation, deploying all its resources in terms
Notes: (145) Case C-28/20, ECLI:EU:C:2021:226, paragraphs 42 and 43. (146) Case C-405/23, ECLI:EU:C:2024:408, paragraph 30.
```

</details>

## q17 (single)

**Question:** Can I cancel my package holiday before it starts, and will I have to pay a fee?

**Reference:** Yes, at any time before the start, but the organiser may charge an appropriate and justifiable termination fee; no fee is due if unavoidable and extraordinary circumstances at or near the destination significantly affect the package or the travel there (Art. 12(1)-(2)).

**Answer shown to the user:**

> Yes, you can cancel (terminate) your package holiday at any time before it starts [32015L2302:A:w059:1]. Whether you will have to pay a fee depends on the reason for your cancellation:
> 
> * **Standard cancellation:** If you cancel for personal reasons, the organiser may require you to pay an appropriate and justifiable termination fee [32015L2302:A:w059:1]. The contract may specify reasonable standardised termination fees based on when you cancel and expected cost savings or alternative use of the services [32015L2302:A:w059:1]. If there are no standardised fees, the fee equals the package price minus cost savings and income from alternative deployment [32015L2302:A:w059:1]. You can also ask the organiser to justify the fee amount [32015L2302:A:w059:1].
> * **Cancellation without a fee:** You can terminate the contract before it starts **without paying any termination fee** if "unavoidable and extraordinary circumstances" occur at your destination or its immediate vicinity that significantly affect the performance of the package or the carriage of passengers to the destination [32015L2302:A:w059:1]. This can include things like serious security problems, warfare, significant health risks (such as a serious disease outbreak), or natural disasters [32015L2302:A:w020:1]. In this case, you are entitled to a full refund of payments made for the package, but no additional compensation [32015L2302:A:w059:1].
> 
> *(Note: This information is based on EU Directive (EU) 2015/2302 on package travel and is provided for informational purposes, not as legal advice.)*

<details><summary>Passages the agent retrieved</summary>

```text
[32015L2302:A:w059:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 12, PDF pp. 16-17 | similarity 0.834
termination fee to the organiser. The package travel contract may specify
reasonable standardised termination fees based on the time of the termination of the contract before the start of the
package and the expected cost savings and income from alternative deployment of the travel services. In the absence of
standardised termination fees, the amount of the termination fee shall correspond to the price of the package minus the
cost savings and income from alternative deployment of the travel services. At the traveller's request the organiser shall
provide a justification for the amount of the termination fees.
2. Notwithstanding paragraph 1, the traveller shall have the right to terminate the package travel contract before the
start of the package without paying any termination fee in the event of unavoidable and extraordinary circumstances
occurring at the place of destination or its immediate vicinity and significantly affecting the performance of the package,
or which significantly affect the carriage of passengers to the destination. In the event of termination of the package
travel contract under this paragraph, the traveller shall be entitled to a full refund of any payments made for the
package, but shall not be entitled to additional compensation.
3. The organiser
```
```text
[32015L2302:A:w060:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 12, PDF p. 17 | similarity 0.814
In the event of termination of the package
travel contract under this paragraph, the traveller shall be entitled to a full refund of any payments made for the
package, but shall not be entitled to additional compensation.
3. The organiser may terminate the package travel contract and provide the traveller with a full refund of any
payments made for the package, but shall not be liable for additional compensation, if:
(a) the number of persons enrolled for the package is smaller than the minimum number stated in the contract and the
organiser notifies the traveller of the termination of the contract within the period fixed in the contract, but not
later than:
(i) 20 days before the start of the package in the case of trips lasting more than six days;
(ii) seven days before the start of the package in the case of trips lasting between two and six days;
(iii) 48 hours before the start of the package in the case of trips lasting less than two days;
or
(b) the organiser is prevented from performing the contract because of unavoidable and extraordinary circumstances
and notifies the traveller of the termination of the contract without undue delay before
```
```text
[32015L2302:A:w061:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 12 to Article 13, PDF p. 17 | similarity 0.804
in the case of trips lasting less than two days;
or
(b) the organiser is prevented from performing the contract because of unavoidable and extraordinary circumstances
and notifies the traveller of the termination of the contract without undue delay before the start of the package.
4. The organiser shall provide any refunds required under paragraphs 2 and 3 or, with respect to paragraph 1,
reimburse any payments made by or on behalf of the traveller for the package minus the appropriate termination fee.
Such refunds or reimbursements shall be made to the traveller without undue delay and in any event not later than 14
days after the package travel contract is terminated.
5. With respect to off-premises contracts, Member States may provide in their national law that the traveller has the
right to withdraw from the package travel contract within a period of 14 days without giving any reason.
Article 13
Responsibility for the performance of the package
1. Member States shall ensure that the organiser is responsible for the performance of the travel services included in
the package travel contract, irrespective of whether those services are to be performed by the organiser or by other
travel service providers.
Member
```
```text
[32015L2302:A:w020:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Recital (31) to Recital (33), PDF p. 5 | similarity 0.793
have the right to terminate the
package travel contract without paying any termination fee where unavoidable and extraordinary circumstances
will significantly affect the performance of the package. This may cover for example warfare, other serious
security problems such as terrorism, significant risks to human health such as the outbreak of a serious disease at
the travel destination, or natural disasters such as floods, earthquakes or weather conditions which make it
impossible to travel safely to the destination as agreed in the package travel contract.
(32) In specific situations, the organiser should also be entitled to terminate the package travel contract before the
start of the package without paying compensation, for instance if the minimum number of participants is not
reached and where that possibility has been reserved in the contract. In that event, the organiser should refund all
payments made in respect of the package.
(33) In certain cases organisers should be allowed to make unilateral changes to the package travel contract. However,
travellers should have the right to terminate the package travel contract if the changes alter significantly any of
the main characteristics of the travel services. This may for instance be the case if the quality or the
```
```text
[32015L2302:A:w058:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 11 to Article 12, PDF p. 16 | similarity 0.790
subparagraph of paragraph 2 result in a package of lower quality or cost,
the traveller shall be entitled to an appropriate price reduction.
5. If the package travel contract is terminated pursuant to point (b) of the first subparagraph of paragraph 2 of this
Article, and the traveller does not accept a substitute package, the organiser shall refund all payments made by or on
behalf of the traveller without undue delay and in any event not later than 14 days after the contract is terminated.
Article 14(2), (3), (4), (5) and (6) shall apply mutatis mutandis.
Article 12
Termination of the package travel contract and the right of withdrawal before the start of the package
1. Member States shall ensure that the traveller may terminate the package travel contract at any time before the start
of the package. Where the traveller terminates the package travel contract under this paragraph, the traveller may be
required to pay an appropriate and justifiable termination fee to the organiser. The package travel contract may specify
reasonable standardised termination fees based on the time of the termination of the contract before the start of the
package and the expected cost savings and income from alternative
```

</details>

## q18 (single)

**Question:** What is the minimum limitation period for claiming compensation under the package travel directive?

**Reference:** Not less than two years (Art. 14(6)).

**Answer shown to the user:**

> Under Directive (EU) 2015/2302 on package travel, the limitation period for introducing claims for compensation or price reduction shall not be less than **two years** [32015L2302:A:w068:1]. 
> 
> This information is based on the provisions of the package travel directive text (legislation, original text) and is provided for informational purposes, not as legal advice [32015L2302:A:w068:1].

<details><summary>Passages the agent retrieved</summary>

```text
[32015L2302:A:w068:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 14 to Article 15, PDF p. 19 | similarity 0.821
In other cases, the
package travel contract may limit compensation to be paid by the organiser as long as that limitation does not apply to
personal injury or damage caused intentionally or with negligence and does not amount to less than three times the
total price of the package.
5. Any right to compensation or price reduction under this Directive shall not affect the rights of travellers under
Regulation (EC) No 261/2004, Regulation (EC) No 1371/2007, Regulation (EC) No 392/2009 of the European
Parliament and of the Council (1), Regulation (EU) No 1177/2010 and Regulation (EU) No 181/2011, and under international
conventions. Travellers shall be entitled to present claims under this Directive and under those Regulations and
international conventions. Compensation or price reduction granted under this Directive and the compensation or price
reduction granted under those Regulations and international conventions shall be deducted from each other in order to
avoid overcompensation.
6. The limitation period for introducing claims under this Article shall not be less than two years.
Article 15
Possibility to contact the organiser via the retailer
Without prejudice to the second subparagraph of Article 13(1), Member States shall ensure that the traveller may
address messages, requests or complaints
Notes: (1) Regulation (EC) No 392/2009 of the European Parliament and of the Council of 23 April 2009 on the liability of carriers of passengers by sea in the event of accidents (OJ L 131, 28.5.2009, p. 24).
```
```text
[32015L2302:A:w069:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 14 to Article 16, PDF p. 19 | similarity 0.785
Article shall not be less than two years.
Article 15
Possibility to contact the organiser via the retailer
Without prejudice to the second subparagraph of Article 13(1), Member States shall ensure that the traveller may
address messages, requests or complaints in relation to the performance of the package directly to the retailer through
which it was purchased. The retailer shall forward those messages, requests or complaints to the organiser without
undue delay.
For the purpose of compliance with time-limits or limitation periods, receipt of the messages, requests or complaints
referred to in the first subparagraph by the retailer shall be considered as receipt by the organiser.
Article 16
Obligation to provide assistance
Member States shall ensure that the organiser gives appropriate assistance without undue delay to the traveller in
difficulty, including in the circumstances referred to in Article 13(7), in particular by:
(a) providing appropriate information on health services, local authorities and consular assistance; and
(b) assisting the traveller to make distance communications and helping the traveller to find alternative travel
arrangements.
The organiser shall be able to charge a reasonable fee for such assistance if the difficulty is caused intentionally by the
traveller or through the traveller's negligence. That
```
```text
[32015L2302:A:w067:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 14, PDF pp. 18-19 | similarity 0.774
receive appropriate compensation from the organiser for any damage which the
traveller sustains as a result of any lack of conformity. Compensation shall be made without undue delay.
3. The traveller shall not be entitled to compensation for damages if the organiser proves that the lack of conformity
is:
(a) attributable to the traveller;
(b) attributable to a third party unconnected with the provision of the travel services included in the package travel
contract and is unforeseeable or unavoidable; or
(c) due to unavoidable and extraordinary circumstances.
4. Insofar as international conventions binding the Union limit the extent of or the conditions under which
compensation is to be paid by a provider carrying out a travel service which is part of a package, the same limitations
shall apply to the organiser. Insofar as international conventions not binding the Union limit compensation to be paid
by a service provider, Member States may limit compensation to be paid by the organiser accordingly. In other cases, the
package travel contract may limit compensation to be paid by the organiser as long as that limitation does not apply to
personal injury or damage caused intentionally or with negligence and does not amount to less
```
```text
[32015L2302:A:w066:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 13 to Article 14, PDF pp. 18-19 | similarity 0.767
of costs referred to in paragraph 7 of this Article shall not apply to persons with reduced mobility,
as defined in point (a) of Article 2 of Regulation (EC) No 1107/2006, and any person accompanying them, pregnant
women and unaccompanied minors, as well as persons in need of specific medical assistance, provided that the
organiser has been notified of their particular needs at least 48 hours before the start of the package. The organiser may
not invoke unavoidable and extraordinary circumstances to limit the liability under paragraph 7 of this Article if the
relevant transport provider may not rely on such circumstances under applicable Union legislation.
Article 14
Price reduction and compensation for damages
1. Member States shall ensure that the traveller is entitled to an appropriate price reduction for any period during
which there was lack of conformity, unless the organiser proves that the lack of conformity is attributable to the
traveller.
2. The traveller shall be entitled to receive appropriate compensation from the organiser for any damage which the
traveller sustains as a result of any lack of conformity. Compensation shall be made without undue delay.
3. The traveller shall not be entitled to compensation for damages if
```
```text
[32015L2302:A:w023:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Recital (34) to Recital (35), PDF p. 6 | similarity 0.760
This would apply, for instance, when, due to the delay of a bus provided by the
organiser, the traveller has to take a taxi to catch his flight on time. Travellers should also be entitled to a price
reduction, termination of the package travel contract and/or compensation for damages. Compensation should
also cover non-material damage, such as compensation for loss of enjoyment of the trip or holiday because of
substantial problems in the performance of the relevant travel services. The traveller should be required to inform
the organiser without undue delay, taking into account the circumstances of the case, of any lack of conformity
he perceives during the performance of a travel service included in the package travel contract. Failure to do so
may be taken into account when determining the appropriate price reduction or compensation for damages
where such notice would have avoided or reduced the damage.
(35) In order to ensure consistency, it is appropriate to align the provisions of this Directive with international
conventions regulating travel services and with the Union passenger rights legislation. Where the organiser is
liable for failure to perform or improper performance of the travel services included in the package travel
contract, the
```

</details>

## q19 (single)

**Question:** What help must the package organiser give me if I get into difficulty during the trip?

**Reference:** Appropriate assistance without undue delay, in particular information on health services, local authorities and consular assistance, and help with distance communications and alternative travel arrangements; a reasonable fee (not above actual costs) may be charged if the traveller caused the difficulty intentionally or negligently (Art. 16).

**Answer shown to the user:**

> Under EU package travel rules (Directive (EU) 2015/2302), if you get into difficulty during your trip, the package organiser must give you **appropriate assistance without undue delay** [32015L2302:A:w069:1]. 
> 
> ### What the assistance includes:
> * **Information:** Providing appropriate information on health services, local authorities, and consular assistance [32015L2302:A:w069:1].
> * **Communications and travel:** Assisting you to make distance communications and helping you find alternative travel arrangements [32015L2302:A:w069:1].
> 
> ### Conditions and Exceptions:
> * **Cost of assistance:** The organiser is allowed to charge a reasonable fee for this assistance *only* if the difficulty was caused intentionally by you or through your negligence; even then, the fee cannot exceed the actual costs the organiser incurred [32015L2302:A:w070:1].
> * **Extraordinary circumstances and accommodation:** If you are stuck and your return cannot be ensured as agreed because of "unavoidable and extraordinary circumstances," the organiser must bear the cost of necessary accommodation (if possible of an equivalent category) for up to **three nights** per traveller, unless longer periods apply under EU passenger-rights transport legislation [32015L2302:A:w065:1]. This three-night limit does not apply to persons with reduced mobility, pregnant women, unaccompanied minors, or persons needing specific medical assistance [32015L2302:A:w065:1].
> 
> *Note: This is information from the EU texts, not legal advice for your specific case.*

<details><summary>Passages the agent retrieved</summary>

```text
[32015L2302:A:w070:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 16 to Article 17, PDF pp. 19-20 | similarity 0.776
make distance communications and helping the traveller to find alternative travel
arrangements.
The organiser shall be able to charge a reasonable fee for such assistance if the difficulty is caused intentionally by the
traveller or through the traveller's negligence. That fee shall not in any event exceed the actual costs incurred by the
organiser.
Article 17
Effectiveness and scope of insolvency protection
1. Member States shall ensure that organisers established in their territory provide security for the refund of all
payments made by or on behalf of travellers insofar as the relevant services are not performed as a consequence of the
organiser's insolvency. If the carriage of passengers is included in the package travel contract, organisers shall also
provide security for the travellers' repatriation. Continuation of the package may be offered.
Organisers not established in a Member State which sell or offer for sale packages in a Member State, or which by any
means direct such activities to a Member State, shall be obliged to provide the security in accordance with the law of
that Member State.
2. The security referred to in paragraph 1 shall be effective and shall cover reasonably foreseeable costs. It shall cover
the amounts of
```
```text
[32015L2302:A:w069:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 14 to Article 16, PDF p. 19 | similarity 0.748
Article shall not be less than two years.
Article 15
Possibility to contact the organiser via the retailer
Without prejudice to the second subparagraph of Article 13(1), Member States shall ensure that the traveller may
address messages, requests or complaints in relation to the performance of the package directly to the retailer through
which it was purchased. The retailer shall forward those messages, requests or complaints to the organiser without
undue delay.
For the purpose of compliance with time-limits or limitation periods, receipt of the messages, requests or complaints
referred to in the first subparagraph by the retailer shall be considered as receipt by the organiser.
Article 16
Obligation to provide assistance
Member States shall ensure that the organiser gives appropriate assistance without undue delay to the traveller in
difficulty, including in the circumstances referred to in Article 13(7), in particular by:
(a) providing appropriate information on health services, local authorities and consular assistance; and
(b) assisting the traveller to make distance communications and helping the traveller to find alternative travel
arrangements.
The organiser shall be able to charge a reasonable fee for such assistance if the difficulty is caused intentionally by the
traveller or through the traveller's negligence. That
```
```text
[32015L2302:A:w065:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 13, PDF p. 18 | similarity 0.744
the proposed alternative arrangements in
accordance with the third subparagraph of paragraph 5 of this Article, the traveller is, where appropriate, entitled to
price reduction and/or compensation for damages in accordance with Article 14 without terminating the package travel
contract.
If the package includes the carriage of passengers, the organiser shall, in the cases referred to in the first and second subparagraphs
, also provide repatriation of the traveller with equivalent transport without undue delay and at no extra cost
to the traveller.
7. As long as it is impossible to ensure the traveller's return as agreed in the package travel contract because of
unavoidable and extraordinary circumstances, the organiser shall bear the cost of necessary accommodation, if possible
of equivalent category, for a period not exceeding three nights per traveller. Where longer periods are provided for in
Union passenger rights legislation applicable to the relevant means of transport for the traveller's return, those periods
shall apply.
8. The limitation of costs referred to in paragraph 7 of this Article shall not apply to persons with reduced mobility,
as defined in point (a) of Article 2 of Regulation (EC) No 1107/2006, and any person accompanying them, pregnant
women and unaccompanied
```
```text
[32015L2302:A:w062:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 13, PDF pp. 17-18 | similarity 0.738
States shall ensure that the organiser is responsible for the performance of the travel services included in
the package travel contract, irrespective of whether those services are to be performed by the organiser or by other
travel service providers.
Member States may maintain or introduce in their national law provisions under which the retailer is also responsible
for the performance of the package. In that case the provisions of Article 7 and Chapter III, this Chapter and Chapter V
which are applicable to the organiser shall also apply mutatis mutandis to the retailer.
2. The traveller shall inform the organiser without undue delay, taking into account the circumstances of the case, of
any lack of conformity which he perceives during the performance of a travel service included in the package travel
contract.
3. If any of the travel services are not performed in accordance with the package travel contract, the organiser shall
remedy the lack of conformity, unless that:
(a) is impossible; or
(b) entails disproportionate costs, taking into account the extent of the lack of conformity and the value of the travel
services affected.
If the organiser, in accordance with point (a) or point (b) of the first subparagraph
```
```text
[32015L2302:A:w063:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 13, PDF pp. 17-18 | similarity 0.737
is impossible; or
(b) entails disproportionate costs, taking into account the extent of the lack of conformity and the value of the travel
services affected.
If the organiser, in accordance with point (a) or point (b) of the first subparagraph of this paragraph, does not remedy
the lack of conformity, Article 14 shall apply.
4. Without prejudice to the exceptions laid down in paragraph 3, if the organiser does not remedy the lack of
conformity within a reasonable period set by the traveller, the traveller may do so himself and request reimbursement of
the necessary expenses. It shall not be necessary for the traveller to specify a time-limit if the organiser refuses to
remedy the lack of conformity or if immediate remedy is required.
5. Where a significant proportion of the travel services cannot be provided as agreed in the package travel contract,
the organiser shall offer, at no extra cost to the traveller, suitable alternative arrangements of, where possible, equivalent
or higher quality than those specified in the contract, for the continuation of the package, including where the traveller's
return to the place of departure is not provided as agreed.
Where the proposed alternative arrangements result in a package
```

</details>

## q20 (multi)

**Question:** My 1,200 km flight was cancelled because a technical defect was found just before departure. Am I owed compensation, and how much?

**Reference:** Probably yes: according to the guidelines a technical problem inherent in the normal operation of the aircraft is not an extraordinary circumstance (section 5.2.2), so EUR 250 for a flight of 1,500 km or less (Art. 7(1)(a)), subject to the notice and re-routing conditions of Art. 5.

**Answer shown to the user:**

> Yes, under EU rules you may be owed **€250** in compensation, provided you were not informed of the cancellation at least two weeks before departure [32004R0261:A:w014:1, 32004R0261:A:w16:1]. 
> 
> * **Distance bracket:** For flights of 1,500 km or less, the standard compensation amount is **€250** [32004R0261:A:w016:1].
> * **Technical defects:** Under EU passenger-rights texts and interpretive guidelines, an unexpected technical defect discovered just before departure is generally considered "internal" and **inherent in the normal exercise of an air carrier's activity**. It does not qualify as an "extraordinary circumstance" that would exempt the airline from paying compensation [52024XC05687:A:w080:1].
> 
> ### What else to check
> * **Notice period:** You are not owed compensation if the airline informed you of the cancellation at least 14 days before the scheduled departure, or within specific shorter windows if they offered you qualifying alternative re-routing [32004R0261:A:w014:1].
> * **Re-routing impact:** If the airline offered you an alternative flight that got you to your destination with only a minimal delay (less than two hours past your original scheduled arrival), the airline is permitted to reduce your compensation by 50% (to €125) [32004R0261:A:w017:1].
> * **Separate rights:** Compensation is separate from your right to a full ticket refund or re-routing under Article 8, and separate from your right to care (meals, refreshments, and hotel accommodation if necessary) while waiting [32004R0261:A:w018:1].
> 
> *This is information from the EU passenger-rights texts, not legal advice for your specific case.*

<details><summary>Passages the agent retrieved</summary>

```text
[32004R0261:A:w017:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 7, PDF p. 5 | similarity 0.782
(b) EUR 400 for all intra-Community flights of more than
1 500 kilometres, and for all other flights between 1 500
and 3 500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the distance, the basis shall be the last destination
at which the denial of boarding or cancellation will delay
the passenger's arrival after the scheduled time.
2. When passengers are offered re-routing to their final
destination on an alternative flight pursuant to Article 8, the
arrival time of which does not exceed the scheduled arrival
time of the flight originally booked
(a) by two hours, in respect of all flights of 1 500 kilometres
or less; or
(b) by three hours, in respect of all intra-Community flights of
more than 1 500 kilometres and for all other flights
between 1 500 and 3 500 kilometres; or
(c) by four hours, in respect of all flights not falling under (a)
or (b),
the operating air carrier may reduce the compensation
provided for in paragraph 1 by 50 %.
3. The compensation referred to in paragraph 1 shall be
paid in cash, by electronic bank transfer, bank orders or bank
cheques or, with
```
```text
[32004R0261:A:w014:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 5, PDF p. 4 | similarity 0.760
in event of re-routing
when the reasonably expected time of departure of
the new flight is at least the day after the departure as it
was planned for the cancelled flight, the assistance specified
in Article 9(1)(b) and 9(1)(c); and
(c) have the right to compensation by the operating air carrier
in accordance with Article 7, unless:
(i) they are informed of the cancellation at least two
weeks before the scheduled time of departure; or
(ii) they are informed of the cancellation between two
weeks and seven days before the scheduled time of
departure and are offered re-routing, allowing them to
depart no more than two hours before the scheduled
time of departure and to reach their final destination
less than four hours after the scheduled time of arrival;
or
(iii) they are informed of the cancellation less than seven
days before the scheduled time of departure and are
offered re-routing, allowing them to depart no more
than one hour before the scheduled time of departure
and to reach their final destination less than two hours
after the scheduled time of arrival.
2. When passengers are informed of the cancellation, an
explanation shall be given concerning possible alternative transport
.
```
```text
[32004R0261:A:w015:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 5 to Article 6, PDF p. 4 | similarity 0.760
before the scheduled time of departure
and to reach their final destination less than two hours
after the scheduled time of arrival.
2. When passengers are informed of the cancellation, an
explanation shall be given concerning possible alternative transport
.
3. An operating air carrier shall not be obliged to pay
compensation in accordance with Article 7, if it can prove that
the cancellation is caused by extraordinary circumstances
which could not have been avoided even if all reasonable
measures had been taken.
4. The burden of proof concerning the questions as to
whether and when the passenger has been informed of the
cancellation of the flight shall rest with the operating air
carrier.
Article 6
Delay
1. When an operating air carrier reasonably expects a flight
to be delayed beyond its scheduled time of departure:
(a) for two hours or more in the case of flights of 1 500 kilometres
or less; or
(b) for three hours or more in the case of all intra-Community
flights of more than 1 500 kilometres and of all other
flights between 1 500 and 3 500 kilometres; or
(c) for four hours or more in the case of all flights not falling
```
```text
[32004R0261:A:w016:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 6 to Article 7, PDF pp. 4-5 | similarity 0.743
in the case of all intra-Community
flights of more than 1 500 kilometres and of all other
flights between 1 500 and 3 500 kilometres; or
(c) for four hours or more in the case of all flights not falling
under (a) or (b),
passengers shall be offered by the operating air carrier:
(i) the assistance specified in Article 9(1)(a) and 9(2); and
(ii) when the reasonably expected time of departure is at least
the day after the time of departure previously announced,
the assistance specified in Article 9(1)(b) and 9(1)(c); and
(iii) when the delay is at least five hours, the assistance specified
in Article 8(1)(a).
2. In any event, the assistance shall be offered within the
time limits set out above with respect to each distance bracket.
Article 7
Right to compensation
1. Where reference is made to this Article, passengers shall
receive compensation amounting to:
(a) EUR 250 for all flights of 1 500 kilometres or less;
(b) EUR 400 for all intra-Community flights of more than
1 500 kilometres, and for all other flights between 1 500
and 3 500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the
```
```text
[52024XC05687:A:w095:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 6.4, PDF p. 30 | similarity 0.745
The right to compensation for cancellation pursuant to Article 5(1) and Article 7 of Regulation (EC) No 261/2004 does not
apply in the case of cancellations made more than 14 days in advance or if the cancellation is caused by extraordinary
circumstances that could not have been avoided even if all reasonable measures had been taken by the air carrier.
The Commission considers that, if public authorities take measures intended to contain the effects of a crisis situation
leading to massive travel disruptions, such measures are by their nature and origin not inherent in the normal exercise of
the activity of air carriers and are outside their actual control.
Article 5(3) waives the right to compensation on condition that the cancellation in question ‘is caused’ by extraordinary
circumstances that could not have been avoided even if all reasonable measures had been taken.
This condition should be considered fulfilled if public authorities either prohibit certain flights or restrict the movement of
people in a manner that de facto excludes the operation of the flight in question.
This condition may also be fulfilled if the flight cancellation occurs in circumstances in which the corresponding movement
of people is not entirely prohibited but
```
```text
[52024XC05687:A:w080:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.2.2, PDF pp. 25-26 | similarity 0.850
Court (123) has clarified further that a technical problem that comes to light during aircraft maintenance or is caused by
failure to maintain an aircraft cannot be regarded as extraordinary circumstances. The Court takes the view that even if a
technical problem that has occurred unexpectedly is not attributable to poor maintenance and is not detected during
routine maintenance checks, it does not fall within the definition of extraordinary circumstances if it is inherent in the
normal exercise of the activity of the air carrier.
For instance, a breakdown caused by the premature malfunction of certain components of an aircraft may constitute an
unexpected event. Nevertheless, such a breakdown remains intrinsically linked to the very complex operating system of an
aircraft, which is operated by the air carrier in conditions – particularly meteorological conditions – that are often difficult
or even extreme, it being understood, moreover, that no component of an aircraft lasts forever. Therefore, it must be held
that such an unexpected event is inherent in the normal exercise of the air carrier’s activity (124).
The same holds true, in principle, for the failure of a part that is only replaced by a new part when it becomes defective
Notes: (123) Case C-549/07, ECLI:EU:C:2008:771, paragraph 25. (124) Case C-257/14, ECLI:EU:C:2015:618, paragraphs 40, 41 and 42.
```
```text
[52024XC05687:A:w079:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.1 to Section 5.2.2, PDF p. 25 | similarity 0.825
enforcement body and the passengers in line with national
provisions on access to documents.
5.2. ‘Internal’ and ‘external’ events
5.2.1. Concept
The Court has consistently held in its case-law relating to the concept of extraordinary circumstances within the meaning of
Article 5(3) of Regulation (EC) No 261/2004 that events whose origin is ‘internal’ must be distinguished from those whose
origin is ‘external’ to the operating air carrier (121).
‘External’ events result from external circumstances that are more or less frequent in practice but which the air carrier does
not control because they arise from a natural event or an act of a third party, such as another air carrier or a public or
private operator interfering with flight or airport activity (122). ‘External’ events generally qualify as extraordinary
circumstances.
Events that are not ‘external’ should be qualified as ‘internal’ to the operating air carrier and thus are not extraordinary
circumstances.
5.2.2. ‘Internal’ events
— Technical defects of the aircraft
The Court (123) has clarified further that a technical problem that comes to light during aircraft maintenance or is caused by
failure to maintain an aircraft cannot be regarded as extraordinary circumstances. The Court takes the view that even if a
Notes: (121) The Court made this distinction for the first time in Case C-28/20, ECLI:EU:C:2021:226, paragraph 39. (122) Case C-28/20, ECLI:EU:C:2021:226, paragraph 41. (123) Case C-549/07, ECLI:EU:C:2008:771, paragraph 25.
```
```text
[52024XC05687:A:w091:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.3 to Section 5.4, PDF p. 29 | similarity 0.824
of its undertaking at the relevant time (149).
As regards technical defects, the fact that an air carrier has complied with the minimum rules on maintenance of an aircraft
cannot in itself suffice to establish that this air carrier has taken all reasonable measures to relieve it of its obligation to pay
compensation (150).
5.4. Extraordinary circumstances on a previous flight with the same aircraft
In order to be exempted from its obligation to compensate passengers in the event of a long delay or cancellation of a flight,
an operating air carrier may rely on an extraordinary circumstance that affected a previous flight which it operated using
the same aircraft, if there is a direct causal link between the occurrence of this circumstance and the delay or cancellation
of the subsequent flight (151).
In another case, the Court has specified that in case of a long delay at arrival, an operating air carrier may rely on an
extraordinary circumstance that affected not this delayed flight but a previous flight operated by this air carrier using the
same aircraft at aircraft turnaround three flights back in the rotation sequence of the aircraft, if there is a direct causal link
between the
Notes: (149) Case C-264/20, ECLI:EU:C:2021:26, paragraph 33. (150) Case C-549/07, ECLI:EU:C:2008:771, paragraph 43. (151) Case C-74/19, EU:C:2020:460, paragraph 55.
```
```text
[52024XC05687:A:w081:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.2.2, PDF p. 26 | similarity 0.812
such an unexpected event is inherent in the normal exercise of the air carrier’s activity (124).
The same holds true, in principle, for the failure of a part that is only replaced by a new part when it becomes defective (an
‘on condition’ part) (125).
However, a hidden manufacturing defect revealed by the manufacturer of the aircraft or by a competent authority, or
damage to the aircraft caused by acts of sabotage or terrorism would qualify as extraordinary circumstances. This holds
true even if the manufacturer has informed the air carrier of the existence of the defect several months before the flight (126).
— Mobile boarding stairs
The Court (127) has clarified that the collision of mobile boarding stairs with an aircraft cannot be considered as
extraordinary circumstances exempting the air carrier from payment of compensation under Article 5(3) of Regulation
(EC) No 261/2004. Mobile stairs or gangways can be regarded as indispensable to air passenger transport, and therefore
air carriers are regularly faced with situations arising from the use of such equipment. A collision between an aircraft and a
set of mobile boarding stairs is, hence, an internal event, inherent in the normal exercise of the activity of the
Notes: (124) Case C-257/14, ECLI:EU:C:2015:618, paragraphs 40, 41 and 42. (125) Case C-832/18, ECLI:EU:C:2020:204, paragraph 43. (126) Case C-411/23, ECLI:EU:C:2024:498, paragraph 42; see also case C-385/23, Finnair, ECLI:EU:C:2024:497, paragraphs 37 and 39. (127) Case C-394/14, ECLI:EU:C:2014:2377, paragraphs 19 and 20.
```
```text
[52024XC05687:A:w090:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 5.3, PDF p. 29 | similarity 0.812
to operate the flight in its entirety once the
extraordinary circumstances have come to an end. Such buffer time is assessed on a case-by-case basis.
However, Article 5(3) cannot be interpreted as requiring, as a ‘reasonable measure’, provision to be made, generally and
without distinction, for a minimum buffer time applicable in the same way to all air carriers in all situations if
extraordinary circumstances arise. In this regard, air carriers will generally have more resources available at their home
base compared to outbound destinations, giving them more possibilities to limit the impact of extraordinary
circumstances. The assessment of the air carrier’s ability to operate the programmed flight in its entirety in the new
conditions resulting from the occurrence of extraordinary circumstances must be carried out in such a way as to ensure
that the length of the required buffer time does not result in the air carrier being led to make intolerable sacrifices in the
light of the capacities of its undertaking at the relevant time (149).
As regards technical defects, the fact that an air carrier has complied with the minimum rules on maintenance of an aircraft
cannot in itself suffice to establish that this air carrier has
Notes: (149) Case C-264/20, ECLI:EU:C:2021:26, paragraph 33.
```
```text
[32004R0261:A:w018:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 7 to Article 8, PDF p. 5 | similarity 0.742
the operating air carrier may reduce the compensation
provided for in paragraph 1 by 50 %.
3. The compensation referred to in paragraph 1 shall be
paid in cash, by electronic bank transfer, bank orders or bank
cheques or, with the signed agreement of the passenger, in
travel vouchers and/or other services.
4. The distances given in paragraphs 1 and 2 shall be
measured by the great circle route method.
Article 8
Right to reimbursement or re-routing
1. Where reference is made to this Article, passengers shall
be offered the choice between:
(a) — reimbursement within seven days, by the means
provided for in Article 7(3), of the full cost of the ticket
at the price at which it was bought, for the part or
parts of the journey not made, and for the part or parts
already made if the flight is no longer serving any
purpose in relation to the passenger's original travel
plan, together with, when relevant,
— a return flight to the first point of departure, at the
earliest opportunity;
(b) re-routing, under comparable transport conditions, to their
final destination at the earliest opportunity; or
(c) re-routing, under comparable transport conditions, to their
final destination at
```
```text
[52024XC05687:A:w071:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.4.10 to Section 4.4.11, PDF p. 23 | similarity 0.740
hours of more (106).
It follows that the compensation payable to a passenger whose flight is delayed by 3 hours or more, who reaches their final
destination 3 hours or more after the arrival time originally scheduled, may be reduced by 50 %, if the delay is less than
4 hours (107).
In other words, if the delay at arrival is more than 3 and less than 4 hours for a journey of more than 3 500 km, the
compensation can be reduced by 50 % and therefore amounts to EUR 300 in accordance with Article 7(2) of Regulation
(EC) No 261/2004.
However, if a flight has been brought forward an amount of time that gives rise to a right to compensation pursuant to
Article 7, the operating air carrier is still required to pay the full amount. It does not have the possibility to reduce any
compensation to be paid by 50 % on the ground that it has offered the passengers re-routing, allowing them to arrive
without delay at their final destination (108).
4.4.11. Calculation of the distance on the basis of the ‘journey’ to determine the compensation in the event of long delay at the final
destination
Notes: (106) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 63. (107) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 63. (108) Joined Cases C-146/20, C-188/20, C-196/20 and C-270/20, ECLI:EU:C:2021:1038, paragraph 94.
```
```text
[52024XC05687:A:w063:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.4.2 to Section 4.4.4, PDF pp. 20-21 | similarity 0.722
flight included in their reservation has been subject to a delay attributable to this air carrier, who mistakenly
expected these passengers not to arrive in time to board the second flight (96). In contrast, if passengers have two separate
tickets for two consecutive flights and delay of the first flight means that they are unable to check in on time for the
following flight, air carriers are not obliged to pay compensation. However, if the delay of the first flight is over 3 hours,
the passenger can be entitled to compensation from the air carrier operating this flight.
4.4.3. Amount of compensation
The compensation is calculated in accordance with Article 7(1) of Regulation (EC) No 261/2004. It can be reduced by 50 %
if the conditions of Article 7(2) are fulfilled.
C. Compensation in the event of cancellation
4.4.4. General case
Compensation is due in the event of cancellation:
— if passengers are not informed sufficiently in advance, i.e. at least 2 weeks before the scheduled departure, and
— if they are not re-routed within the time limits set out in Article 5(1), point (c), of Regulation (EC) No 261/2004 (see
Section E),
— unless the cancellation is caused by
Notes: (96) Case C-321/11, ECLI:EU:C:2012:609, paragraph 36.
```

</details>

## q21 (multi)

**Question:** My flight arrived three and a half hours late. Can I get compensation even though the regulation only mentions compensation for cancellations?

**Reference:** Yes. Per the guidelines, the Court held that passengers arriving 3 hours or more late are entitled to the same Art. 7 compensation as for cancellation, unless extraordinary circumstances (section 4.4.7); the amount depends on distance (EUR 250/400/600, Art. 7).

**Answer shown to the user:**

> Yes, under EU case law reflected in the Commission’s guidelines, passengers reaching their final destination with a delay of **3 hours or more** are entitled to the same compensation under Article 7 as passengers whose flight is cancelled, because they suffer a comparable loss of time [52024XC05687:A:w066:1]. 
> 
> The text of Regulation (EC) No 261/2004 itself sets compensation amounts based on distance [32004R0261:A:w016:1]:
> * **€250** for flights of 1,500 km or less [32004R0261:A:w016:1];
> * **€400** for all intra-Community flights of more than 1,500 km, and all other flights between 1,500 km and 3,500 km [32004R0261:A:w016:1];
> * **€600** for all other flights [32004R0261:A:w016:1].
> 
> ### Conditions and Exceptions
> * **Extraordinary circumstances:** Compensation is not due if the air carrier can prove that the long delay was caused by extraordinary circumstances that could not have been avoided even if all reasonable measures had been taken [52024XC05687:A:w067:1].
> * **Guidance status:** Note that the extension of compensation to delayed arrivals is established through court interpretations incorporated in the Commission's interpretative guidelines rather than being explicitly written into the original text of Regulation (EC) No 261/2004 [52024XC05687:A:w066:1].
> 
> *This is information from the texts, not legal advice for your case.*

<details><summary>Passages the agent retrieved</summary>

```text
[32004R0261:A:w017:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 7, PDF p. 5 | similarity 0.814
(b) EUR 400 for all intra-Community flights of more than
1 500 kilometres, and for all other flights between 1 500
and 3 500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the distance, the basis shall be the last destination
at which the denial of boarding or cancellation will delay
the passenger's arrival after the scheduled time.
2. When passengers are offered re-routing to their final
destination on an alternative flight pursuant to Article 8, the
arrival time of which does not exceed the scheduled arrival
time of the flight originally booked
(a) by two hours, in respect of all flights of 1 500 kilometres
or less; or
(b) by three hours, in respect of all intra-Community flights of
more than 1 500 kilometres and for all other flights
between 1 500 and 3 500 kilometres; or
(c) by four hours, in respect of all flights not falling under (a)
or (b),
the operating air carrier may reduce the compensation
provided for in paragraph 1 by 50 %.
3. The compensation referred to in paragraph 1 shall be
paid in cash, by electronic bank transfer, bank orders or bank
cheques or, with
```
```text
[32004R0261:A:w016:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 6 to Article 7, PDF pp. 4-5 | similarity 0.814
in the case of all intra-Community
flights of more than 1 500 kilometres and of all other
flights between 1 500 and 3 500 kilometres; or
(c) for four hours or more in the case of all flights not falling
under (a) or (b),
passengers shall be offered by the operating air carrier:
(i) the assistance specified in Article 9(1)(a) and 9(2); and
(ii) when the reasonably expected time of departure is at least
the day after the time of departure previously announced,
the assistance specified in Article 9(1)(b) and 9(1)(c); and
(iii) when the delay is at least five hours, the assistance specified
in Article 8(1)(a).
2. In any event, the assistance shall be offered within the
time limits set out above with respect to each distance bracket.
Article 7
Right to compensation
1. Where reference is made to this Article, passengers shall
receive compensation amounting to:
(a) EUR 250 for all flights of 1 500 kilometres or less;
(b) EUR 400 for all intra-Community flights of more than
1 500 kilometres, and for all other flights between 1 500
and 3 500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the
```
```text
[52024XC05687:A:w067:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.4.7 to Section 4.4.8, PDF p. 22 | similarity 0.805
in which passengers concerned by a flight cancellation are not offered re-routing allowing them to depart no
more than 1 hour before the scheduled time of departure and to reach their final destination less than 2 hours after the
scheduled time of arrival. The Court deduced from this that the right to compensation laid down in Article 7 of Regulation
(EC) No 261/2004 aims to repair a loss of time of at least 3 hours. However, such a delay does not entitle passengers to
compensation if the air carrier can prove that the long delay was caused by extraordinary circumstances that could not
have been avoided even if all reasonable measures had been taken (100) (see Section 5 on extraordinary circumstances).
4.4.8. Compensation for long delay at arrival in the case of connecting flights
The Court (101) takes the view that for the purposes of the compensation provided for in Article 7 of Regulation (EC)
No 261/2004, a delay must be assessed in relation to the scheduled time of arrival at the passenger’s final destination as
defined in Article 2, point (h), of Regulation (EC) No 261/2004, which in the case of directly connecting flights must be
understood as the
Notes: (100) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 69. (101) Case C-11/11, ECLI:EU:C:2013:106, paragraph 47.
```
```text
[52024XC05687:A:w066:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.4.6 to Section 4.4.7, PDF pp. 21-22 | similarity 0.804
could only be
used to contact the travel agent through which the reservation had been made, and not the passenger directly, and that this
travel agent did not send the information to the passenger in good time (98), meaning at least 2 weeks before the scheduled
time of departure.
D. Compensation in the event of long delay at arrival
4.4.7. ‘Long delays’ at arrival
As regards ‘long delays’, the Court has ruled that delayed passengers may suffer from a similar inconvenience as passengers
whose flight is cancelled, consisting in a certain loss of time (99). Based on the principle of equal treatment, passengers
reaching their final destination with a delay of 3 hours or more are entitled to the same compensation (Article 7) as
passengers whose flight is cancelled. The Court predominantly based its ruling on Article 5(1), point (c)(iii), of Regulation
(EC) No 261/2004, in which the EU legislature attaches legal consequences, including the right to compensation, to
situations in which passengers concerned by a flight cancellation are not offered re-routing allowing them to depart no
more than 1 hour before the scheduled time of departure and to reach their final destination less than 2 hours after the
scheduled
Notes: (98) Case C-307/21, ECLI:EU:C:2022:729, paragraph 30. (99) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 54.
```
```text
[52024XC05687:A:w034:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 3.2.6 to Section 3.3.2, PDF p. 13 | similarity 0.800
to be paid if the air carrier can prove, in accordance with Article 5(3), that the
cancellation is caused by extraordinary circumstances that could not have been avoided even if all reasonable measures had
been taken (63).
3.3. Delay
3.3.1. Delay at departure
Under Article 6(1) of Regulation (EC) No 261/2004, if the departure of a flight is delayed, passengers affected by this delay
have the right to ‘care’ according to Article 9, and to reimbursement and a return flight according to Article 8(1), point (a).
The underlying principle of Article 6(1) is that the rights depend on the duration of the delay and the distance of the flight.
In this regard, it should be noted that the right to re-routing as laid down in Article 8(1), point (b), is not covered under
Article 6(1) as it can be considered that the air carrier is trying, in the first place, to address the cause of the delay in order
to minimise the inconvenience to the passengers.
3.3.2. ‘Long delay’ at arrival
The Court has ruled that a delay at arrival of at least 3 hours gives the same rights in terms of compensation as a
cancellation (64) (for more details,
Notes: (63) See Section 5 on extraordinary circumstances. (64) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 69. See also Joined Cases C-581/10 and C-629/10, ECLI:EU:C:2012:657, paragraph 40, and Case C-413/11, ECLI:EU:C:2013:246, paragraph 19.
```

</details>

## q22 (multi)

**Question:** If my flight is cancelled because of extraordinary circumstances, does the airline still have to provide meals and a hotel?

**Reference:** Yes. Extraordinary circumstances remove only the duty to pay compensation (Art. 5(3)); the duty of care still applies, even when such circumstances last a long time (guidelines, section 4.3.3).

**Answer shown to the user:**

> Yes. Even if a flight is cancelled because of extraordinary circumstances, the operating air carrier still has an obligation to provide care [52024XC05687:A:w059:1]. 
> 
> According to the European Commission's interpretative guidelines and Regulation (EC) No 261/2004, the right to care is not exempted by extraordinary circumstances [52024XC05687:A:w059:1]. Passengers facing a cancellation must be offered free of charge:
> * Meals and refreshments in a reasonable relation to the waiting time [32004R0261:A:w020:1].
> * Hotel accommodation where a stay of one or more nights becomes necessary, or where a stay additional to that intended by the passenger becomes necessary [32004R0261:A:w020:1].
> * Transport between the airport and the place of accommodation [32004R0261:A:w020:1].
> * Two free telephone calls, fax messages, or e-mails [32004R0261:A:w020:1].
> 
> The guidelines state that carriers must actively offer care rather than leaving passengers to make and pay for arrangements themselves [52024XC05687:A:w055:1]. If the airline fails to offer care and you have to pay for meals or a hotel yourself, you can obtain reimbursement for expenses that were necessary, reasonable, and appropriate [52024XC05687:A:w055:1]. 
> 
> *(Note: While extraordinary circumstances relieve the airline of paying financial **compensation** under Article 7 [32004R0261:A:w015:1], they do not remove the duty of **care** under Article 9 [32004R0261:A:w020:1], [52024XC05687:A:w059:1]. This information is drawn from EU passenger-rights texts and guidance, not legal advice for a specific case.)*

<details><summary>Passages the agent retrieved</summary>

```text
[52024XC05687:A:w059:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.3.2 to Section 4.3.3, PDF pp. 19-20 | similarity 0.808
a much longer delay, the air carrier should be allowed to
decline to provide hotel accommodation and corresponding transfers. Similarly, if an air carrier is about to give vouchers
for food and drinks but is informed that the flight is ready for boarding, it should be allowed to decline to provide this
care. Apart from these cases, the Commission is of the opinion that this limitation is to be applied only in very exceptional
cases, as every effort should be made to reduce the inconvenience suffered by passengers.
The right to care under Regulation (EC) No 261/2004 has no bearing on the obligations of organisers of packages under
Directive (EU) 2015/2302.
4.3.3. Care in extraordinary circumstances or exceptional events
According to Regulation (EC) No 261/2004, the air carrier is obliged to fulfil the obligation of care even if the cancellation
of a flight is caused by extraordinary circumstances, that is to say circumstances that could not have been avoided even if all
reasonable measures had been taken. Regulation (EC) No 261/2004 contains nothing that would allow the conclusion to be
drawn that it recognises a separate category of ‘particularly extraordinary’ events – beyond the extraordinary circumstances
referred to in Article
```
```text
[32004R0261:A:w020:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 9 to Article 10, PDF p. 5 | similarity 0.788
is made to this Article, passengers shall
be offered free of charge:
(a) meals and refreshments in a reasonable relation to the
waiting time;
(b) hotel accommodation in cases
— where a stay of one or more nights becomes necessary,
or
— where a stay additional to that intended by the
passenger becomes necessary;
(c) transport between the airport and place of accommodation
(hotel or other).
2. In addition, passengers shall be offered free of charge two
telephone calls, telex or fax messages, or e-mails.
3. In applying this Article, the operating air carrier shall pay
particular attention to the needs of persons with reduced mobility
and any persons accompanying them, as well as to the
needs of unaccompanied children.
Article 10
Upgrading and downgrading
1. If an operating air carrier places a passenger in a class
higher than that for which the ticket was purchased, it may not
request any supplementary payment.
2. If an operating air carrier places a passenger in a class
lower than that for which the ticket was purchased, it shall
within seven days, by the means provided for in Article 7(3),
reimburse
(a) 30 % of the price of the ticket for all flights
```
```text
[52024XC05687:A:w055:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.3.2, PDF pp. 18-19 | similarity 0.776
and the time of day (or night) at which it occurs, including at the
transfer airport in the case of connecting flights, in order to reduce the inconvenience suffered by the passengers as much
as possible, while bearing in mind the principle of proportionality. Particular attention has to be given to the needs of
people with a disability or reduced mobility and unaccompanied children.
Furthermore, passengers should be offered care free of charge in a clear and accessible way, including, where possible, via
electronic means of communication. This means that passengers should not be left to make arrangements themselves, e.g.
finding and paying for accommodation or food. Instead, operating air carriers are obliged to actively offer care. Operating
air carriers should also ensure, where available, that accommodation is accessible for people with a disability and their
service dogs.
If care has not been offered even though it should have been, passengers who have had to pay for meals and refreshments,
hotel accommodation, transport between the airport and the place of accommodation and/or telecommunication services
can obtain reimbursement of the expenses incurred from the air carrier, if these were necessary, reasonable and
appropriate (89).
If passengers reject the air carrier’s reasonable
Notes: (89) Case C-12/11, ECLI:EU:C:2013:43, paragraph 66.
```
```text
[32004R0261:A:w004:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Recital (12) to Recital (16), PDF p. 2 | similarity 0.762
reasonable measures had been taken.
(13) Passengers whose flights are cancelled should be able
either to obtain reimbursement of their tickets or to
obtain re-routing under satisfactory conditions, and
should be adequately cared for while awaiting a later
flight.
(14) As under the Montreal Convention, obligations on operating
air carriers should be limited or excluded in cases
where an event has been caused by extraordinary
circumstances which could not have been avoided even
if all reasonable measures had been taken. Such circumstances
may, in particular, occur in cases of political
instability, meteorological conditions incompatible with
the operation of the flight concerned, security risks,
unexpected flight safety shortcomings and strikes that
affect the operation of an operating air carrier.
(15) Extraordinary circumstances should be deemed to exist
where the impact of an air traffic management decision
in relation to a particular aircraft on a particular day
gives rise to a long delay, an overnight delay, or the
cancellation of one or more flights by that aircraft, even
though all reasonable measures had been taken by the
air carrier concerned to avoid the delays or cancellations
.
(16) In cases where a package tour is cancelled for reasons
other than the flight
```
```text
[32004R0261:A:w015:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 5 to Article 6, PDF p. 4 | similarity 0.758
before the scheduled time of departure
and to reach their final destination less than two hours
after the scheduled time of arrival.
2. When passengers are informed of the cancellation, an
explanation shall be given concerning possible alternative transport
.
3. An operating air carrier shall not be obliged to pay
compensation in accordance with Article 7, if it can prove that
the cancellation is caused by extraordinary circumstances
which could not have been avoided even if all reasonable
measures had been taken.
4. The burden of proof concerning the questions as to
whether and when the passenger has been informed of the
cancellation of the flight shall rest with the operating air
carrier.
Article 6
Delay
1. When an operating air carrier reasonably expects a flight
to be delayed beyond its scheduled time of departure:
(a) for two hours or more in the case of flights of 1 500 kilometres
or less; or
(b) for three hours or more in the case of all intra-Community
flights of more than 1 500 kilometres and of all other
flights between 1 500 and 3 500 kilometres; or
(c) for four hours or more in the case of all flights not falling
```

</details>

## q23 (multi)

**Question:** My train was cancelled and nobody told me about re-routing options for two hours. Can I book a coach myself, and do I get meals while I wait?

**Reference:** Yes: if re-routing options are not communicated within 100 minutes of the scheduled departure, the passenger may contract other rail, coach or bus services and be reimbursed (Art. 18(3)); for a cancellation the railway must also offer meals and refreshments in reasonable relation to the waiting time (Art. 20(2)(a)).

**Answer shown to the user:**

> Under EU rail passenger rights (Regulation (EU) 2021/782), here is what the texts establish regarding your situation:
> 
> ### Booking a coach yourself (Re-routing)
> * **The 100-minute rule:** If the railway undertaking fails to communicate available re-routing options to you within **100 minutes** from the scheduled departure time of the cancelled service, you are legally entitled to conclude a contract yourself with other public transport providers by rail, coach, or bus to reach your final destination under comparable conditions `[32021R0782:A:w051:1]`.
> * **Reimbursement:** Since you waited for two hours (120 minutes), which exceeds the 100-minute threshold without communication of options, you may book a coach and the railway undertaking must reimburse you for the **necessary, appropriate, and reasonable costs** incurred `[32021R0782:A:w052:1]`.
> 
> ### Meals and refreshments (Assistance)
> * **Conditions:** In the event of a cancellation or a delay of 60 minutes or more, the railway undertaking must offer passengers meals and refreshments free of charge, in reasonable relation to the waiting time, provided they are available on the train or in the station, or can reasonably be supplied `[32021R0782:A:w060:1]`.
> * **Note:** This assistance is supposed to be provided by the railway undertaking directly `[32021R0782:A:w060:1]`. 
> 
> *(Note: This is information from the EU rail passenger rights text, not legal advice for your specific case.)*

<details><summary>Passages the agent retrieved</summary>

```text
[32021R0782:A:w050:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 18, PDF p. 18 | similarity 0.748
or more, the
railway undertaking operating the delayed or cancelled service shall immediately offer the passenger the choice between
one of the following options, and shall make the necessary arrangements:
(a) reimbursement of the full cost of the ticket, under the conditions by which it was paid, for the part or parts of his or
her journey not made and for the part or parts already made if the journey is no longer serving any purpose in
relation to the passenger’s original travel plan, together with, when relevant, a return service to the first point of
departure at the earliest opportunity;
(b) continuation or re-routing, under comparable transport conditions, to the final destination at the earliest opportunity;
(c) continuation or re-routing, under comparable transport conditions, to the final destination at a later date at the
passenger’s convenience.
2. Where, for the purposes of points (b) and (c) of paragraph 1, comparable re-routing is operated by the same railway
undertaking or another undertaking is commissioned to perform the re-routing, this shall not generate additional costs to
the passenger. This requirement also applies where the re-routing involves the use of transport of a higher service class
and alternative modes of transport. Railway
```
```text
[32021R0782:A:w051:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 18, PDF p. 18 | similarity 0.763
another undertaking is commissioned to perform the re-routing, this shall not generate additional costs to
the passenger. This requirement also applies where the re-routing involves the use of transport of a higher service class
and alternative modes of transport. Railway undertakings shall make reasonable efforts to avoid additional connections
and to ensure that delay in the total travel time is as short as possible. Passengers shall not be downgraded to transport
facilities of a lower class unless such facilities are the only re-routing means available.
3. Without prejudice to paragraph 2, the railway undertaking may allow the passenger, at his or her request, to
conclude contracts with other providers of transport services which enable the passenger to reach the final destination
under comparable conditions, in which case the railway undertaking shall reimburse the passenger for the costs that he or
she incurs.
Where the available re-routing options are not communicated to the passenger within 100 minutes from the scheduled
departure time of the delayed or cancelled service or the missed connection, the passenger shall be entitled to conclude
such a contract with other providers of public transport services by rail, coach or bus. The railway undertaking shall
reimburse the passenger
```
```text
[32021R0782:A:w060:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 20, PDF p. 21 | similarity 0.809
the station manager as soon as such information is available. Where ticket vendors and tour
operators have such information, they shall also provide it to the passenger.
2. Where the delay referred to in paragraph 1 amounts to 60 minutes or more, or the service is cancelled, the railway
undertaking operating the delayed or cancelled service shall offer the passengers the following, free of charge:
(a) meals and refreshments in reasonable relation to the waiting time, if they are available on the train or in the station,
or can reasonably be supplied, taking into account criteria such as the distance from the supplier, the time required
for delivery and the cost;
(b) hotel or other accommodation, and transport between the railway station and place of accommodation, in cases
where a stay of one or more nights becomes necessary or an additional stay becomes necessary, where and when
physically possible. In cases where such a stay becomes necessary due to the circumstances referred to in
Article 19(10), the railway undertaking may limit the duration of accommodation to a maximum of three nights.
The access requirements of persons with disabilities and persons with reduced mobility and the needs of assistance
dogs shall
```
```text
[32021R0782:A:w052:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 18, PDF pp. 18-19 | similarity 0.753
time of the delayed or cancelled service or the missed connection, the passenger shall be entitled to conclude
such a contract with other providers of public transport services by rail, coach or bus. The railway undertaking shall
reimburse the passenger for the necessary, appropriate and reasonable costs that he or she incurs.
This paragraph shall not affect national laws, regulations or administrative provisions which grant more favourable re-routing
conditions to passengers.
4. Re-routing transport service providers shall provide persons with disabilities and persons with reduced mobility with
a comparable level of assistance and accessibility when offering an alternative service. Re-routing transport service
providers may provide persons with disabilities and persons with reduced mobility with alternative services which are
appropriate to their needs and which differ from those offered to other passengers.
5. The reimbursements referred to in point (a) of paragraph 1 and in paragraph 3 shall be paid within 30 days after
the receipt of the request. Member States may require railway undertakings to accept such requests by particular means of
communication, provided that the request does not create discriminatory effects. The reimbursement may take the form
of vouchers and/or the provision of other services provided that the terms
```
```text
[52024XC05687:A:w056:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.3.2, PDF p. 19 | similarity 0.750
hotel accommodation, transport between the airport and the place of accommodation and/or telecommunication services
can obtain reimbursement of the expenses incurred from the air carrier, if these were necessary, reasonable and
appropriate (89).
If passengers reject the air carrier’s reasonable care that has to be offered under Article 9 and make their own arrangements,
the air carrier is not obliged to reimburse the expenses incurred by the passenger, unless provided otherwise under national
law or agreed beforehand by the air carrier. In order to provide equal treatment between passengers, such reimbursement
can never exceed the value of the aforementioned ‘reasonable offer’ of the air carrier. Passengers should also retain all
receipts for the expenses incurred.
In any event, passengers who feel that they are entitled to have more of their expenses reimbursed or to obtain
compensation for damage suffered as a result of a delay, including expenses, retain the right to base their claims on the
provisions of the Montreal Convention as well as Article 3 of Regulation (EC) No 2027/97, and to take the air carrier to a
national court or address themselves to the competent national enforcement body. In some Member States, passengers
may have to turn to
Notes: (89) Case C-12/11, ECLI:EU:C:2013:43, paragraph 66.
```
```text
[52024XC05687:A:w055:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.3.2, PDF pp. 18-19 | similarity 0.756
and the time of day (or night) at which it occurs, including at the
transfer airport in the case of connecting flights, in order to reduce the inconvenience suffered by the passengers as much
as possible, while bearing in mind the principle of proportionality. Particular attention has to be given to the needs of
people with a disability or reduced mobility and unaccompanied children.
Furthermore, passengers should be offered care free of charge in a clear and accessible way, including, where possible, via
electronic means of communication. This means that passengers should not be left to make arrangements themselves, e.g.
finding and paying for accommodation or food. Instead, operating air carriers are obliged to actively offer care. Operating
air carriers should also ensure, where available, that accommodation is accessible for people with a disability and their
service dogs.
If care has not been offered even though it should have been, passengers who have had to pay for meals and refreshments,
hotel accommodation, transport between the airport and the place of accommodation and/or telecommunication services
can obtain reimbursement of the expenses incurred from the air carrier, if these were necessary, reasonable and
appropriate (89).
If passengers reject the air carrier’s reasonable
Notes: (89) Case C-12/11, ECLI:EU:C:2013:43, paragraph 66.
```
```text
[32021R0782:A:w059:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19 to Article 20, PDF pp. 20-21 | similarity 0.754
prevent;
(b) fault on the part of the passenger; or
(c) the behaviour of a third party which the railway undertaking, in spite of having taken the care required in the
particular circumstances of the case, was unable to avoid and the consequences of which it was unable to prevent,
such as persons on the track, cable theft, on-board emergencies, law enforcement activities, sabotage or terrorism.
Strikes by the personnel of the railway undertaking, acts or omissions by another undertaking using the same railway
infrastructure and acts or omissions of the infrastructure and station managers are not covered by the exemption referred
to in point (c) of the first subparagraph.
Article 20
Assistance
1. In the case of a delay in arrival or departure, or cancellation of a service, passengers shall be kept informed of the
situation and of the estimated departure time and estimated arrival time of the service or the replacement service by the
railway undertaking or by the station manager as soon as such information is available. Where ticket vendors and tour
operators have such information, they shall also provide it to the passenger.
2. Where the delay referred to in paragraph 1 amounts to 60 minutes
```
```text
[32021R0782:A:w049:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 15 to Article 18, PDF pp. 17-18 | similarity 0.749
except where damage was caused by the negligence or fault of
the passenger or where the person who received the advance payment was not the person entitled to compensation.
Article 16
Contestation of liability
Even if the railway undertaking contests its responsibility for physical injury to a passenger whom it conveys, it shall
make every reasonable effort to assist the passenger with his or her claim for compensation for damage from third
parties.
Article 17
Liability for delays, missed connections and cancellations
Subject to the provisions of this Chapter, the liability of railway undertakings in respect of delays, missed connections and
cancellations shall be governed by Chapter II of Title IV of Annex I.
Article 18
Reimbursement and re-routing
1. Where it is reasonably to be expected, either at departure or in the event of a missed connection or a cancellation,
that arrival at the final destination under the transport contract will be subject to a delay of 60 minutes or more, the
railway undertaking operating the delayed or cancelled service shall immediately offer the passenger the choice between
one of the following options, and shall make the necessary arrangements:
(a) reimbursement of the full cost of the ticket, under
```

</details>

## q24 (multi)

**Question:** A flight in my package holiday was cancelled. Can I claim compensation both from the package organiser and from the airline?

**Reference:** Yes, travellers may claim under both the directive and Regulation 261/2004, including directly from the airline even without a contract with it, but amounts granted under each are deducted from each other to avoid overcompensation (Art. 14(5); guidelines section 2.2.7).

**Answer shown to the user:**

> Yes, you are entitled to present claims under both the Package Travel Directive and EU air passenger rights regulations [32015L2302:A:w068:1]. You may seek compensation directly from the operating air carrier for a cancelled flight even though your flight is part of a package [52024XC05687:A:w023:1]. 
> 
> However, there is an anti-double-dipping rule: any compensation or price reduction granted under the Package Travel Directive and under passenger rights regulations must be deducted from each other to avoid overcompensation [52024XC05687:A:w021:1, 32015L2302:A:w068:1]. Furthermore, note that while you can seek compensation from the airline, you cannot seek a ticket *reimbursement* from the airline if you are entitled to seek that reimbursement from your package organiser under the Package Travel Directive [52024XC05687:A:w022:1].
> 
> *Note: This information is drawn directly from EU texts and guidelines; it is not legal advice for your specific case.*

<details><summary>Passages the agent retrieved</summary>

```text
[32015L2302:A:w093:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Annex I, PDF p. 28 | similarity 0.728
as agreed, suitable
alternative arrangements will have to be offered to the traveller at no extra cost. Travellers may terminate the
contract without paying any termination fee, where services are not performed in accordance with the contract and
this substantially affects the performance of the package and the organiser fails to remedy the problem.
— Travellers are also entitled to a price reduction and/or compensation for damages where the travel services are not
performed or are improperly performed.
— The organiser has to provide assistance if the traveller is in difficulty.
— If the organiser or, in some Member States, the retailer becomes insolvent, payments will be refunded. If the
organiser or, where applicable, the retailer becomes insolvent after the start of the package and if transport is
included in the package, repatriation of the travellers is secured. XY has taken out insolvency protection with YZ
[the entity in charge of the insolvency protection, e.g. a guarantee fund or an insurance company). Travellers may
contact this entity or, where applicable, the competent authority (contact details, including name, geographical
address, email and telephone number) if services are denied because of XY's insolvency.
Directive (EU) 2015/2302 as transposed into national law (hyperlink)
```
```text
[32015L2302:A:w060:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 12, PDF p. 17 | similarity 0.725
In the event of termination of the package
travel contract under this paragraph, the traveller shall be entitled to a full refund of any payments made for the
package, but shall not be entitled to additional compensation.
3. The organiser may terminate the package travel contract and provide the traveller with a full refund of any
payments made for the package, but shall not be liable for additional compensation, if:
(a) the number of persons enrolled for the package is smaller than the minimum number stated in the contract and the
organiser notifies the traveller of the termination of the contract within the period fixed in the contract, but not
later than:
(i) 20 days before the start of the package in the case of trips lasting more than six days;
(ii) seven days before the start of the package in the case of trips lasting between two and six days;
(iii) 48 hours before the start of the package in the case of trips lasting less than two days;
or
(b) the organiser is prevented from performing the contract because of unavoidable and extraordinary circumstances
and notifies the traveller of the termination of the contract without undue delay before
```
```text
[32015L2302:A:w085:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Annex I, PDF pp. 25-26 | similarity 0.719
termination fee, where services are not performed in accordance with the contract and
this substantially affects the performance of the package and the organiser fails to remedy the problem.
— Travellers are also entitled to a price reduction and/or compensation for damages where the travel services are not
performed or are improperly performed.
— The organiser has to provide assistance if the traveller is in difficulty.
— If the organiser or, in some Member States, the retailer becomes insolvent, payments will be refunded. If the
organiser or, where applicable, the retailer becomes insolvent after the start of the package and if transport is
included in the package, repatriation of the travellers is secured. XY has taken out insolvency protection with YZ (the
entity in charge of the insolvency protection, e.g. a guarantee fund or an insurance company). Travellers may contact
this entity or, where applicable, the competent authority (contact details, including name, geographical address, email
and telephone number) if services are denied because of XY's insolvency.
Directive (EU) 2015/2302 as transposed into national law (hyperlink)
Part B
Standard information form for package travel contracts in situations other than those covered by Part A
The combination of travel services offered to
```
```text
[32015L2302:A:w065:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 13, PDF p. 18 | similarity 0.719
the proposed alternative arrangements in
accordance with the third subparagraph of paragraph 5 of this Article, the traveller is, where appropriate, entitled to
price reduction and/or compensation for damages in accordance with Article 14 without terminating the package travel
contract.
If the package includes the carriage of passengers, the organiser shall, in the cases referred to in the first and second subparagraphs
, also provide repatriation of the traveller with equivalent transport without undue delay and at no extra cost
to the traveller.
7. As long as it is impossible to ensure the traveller's return as agreed in the package travel contract because of
unavoidable and extraordinary circumstances, the organiser shall bear the cost of necessary accommodation, if possible
of equivalent category, for a period not exceeding three nights per traveller. Where longer periods are provided for in
Union passenger rights legislation applicable to the relevant means of transport for the traveller's return, those periods
shall apply.
8. The limitation of costs referred to in paragraph 7 of this Article shall not apply to persons with reduced mobility,
as defined in point (a) of Article 2 of Regulation (EC) No 1107/2006, and any person accompanying them, pregnant
women and unaccompanied
```
```text
[52024XC05687:A:w023:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 2.2.7 to Section 3.1.1, PDF p. 10 | similarity 0.788
of the ticket and has not taken any measures to
guarantee such reimbursement (45). In other words, passengers who are entitled to seek reimbursement from their travel
organiser under Directive (EU) 2015/2302 are not able to seek reimbursement from the air carrier under Regulation (EC)
No 261/2004.
However, a traveller may seek compensation directly from the air carrier for flights delayed for 3 hours or more or
cancelled, even if there is no contract between this traveller and the respective air carrier and the flight is part of a
package (46).
3. EVENTS GIVING RIGHTS UNDER REGULATION (EC) No 261/2004
3.1. Denied boarding
3.1.1. Concept of ‘denied boarding’
The concept of ‘denied boarding’ relates not only to cases of overbooking but also to those cases where boarding is denied
on other grounds, such as operational reasons (47). In accordance with Article 2, point (j), of Regulation (EC) No 261/2004,
‘denied boarding’ does not cover a situation where there are reasonable grounds for refusing to carry passengers on a flight
even though they presented themselves on time for the flight, such as reasons of health, safety or security, or inadequate
travel documentation.
If the original flight of a passenger who holds
Notes: (45) Case C-163/18, ECLI:EU:C:2019:585, paragraph 44. (46) Case C-215/18, ECLI:EU:C:2020:235, paragraph 38. (47) Case C-22/11, ECLI:EU:C:2012:604, paragraph 26.
```
```text
[52024XC05687:A:w021:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 2.2.7, PDF pp. 9-10 | similarity 0.845
cancelled for reasons other than cancellation of the flight (for example, in the
event of a hotel cancellation). It is also stated that the rights granted under Regulation (EC) No 261/2004 do not affect the
rights granted to travellers under Directive (EU) 2015/2302 of the European Parliament and of the Council (43). Travellers
thus have, in principle, rights in relation to both the package organiser under Directive (EU) 2015/2302 and the operating
air carrier under Regulation (EC) No 261/2004. Article 14(5) of Directive (EU) 2015/2302 also provides that any right to
compensation or price reduction under this Directive does not affect the rights of travellers under Regulation (EC)
No 261/2004, but specifies that compensation or price reduction granted under passenger rights regulations and under
this Directive must be deducted from each other in order to avoid overcompensation.
However, neither Regulation (EC) No 261/2004 nor Directive (EU) 2015/2302 deals with the question of whether it is the
package organiser or the operating air carrier that ultimately has to bear the cost of their overlapping obligations (44).
Resolving such a matter will thus depend on the contractual provisions between organisers and air carriers and the
applicable national law. Any arrangements made in
Notes: (43) Directive (EU) 2015/2302 of the European Parliament and of the Council of 25 November 2015 on package travel and linked travel arrangements, amending Regulation (EC) No 2006/2004 and Directive 2011/83/EU of the European Parliament and of the Council and repealing Council Directive 90/314/EEC (OJ L 326, 11.12.2015, p. 1, ELI: http://data.europa.eu/eli/dir/2015/2302/oj). According to Article 29 of Directive (EU) 2015/2302, references to Directive 90/314/EEC in the Regulation are to be read as references to Directive (EU) 2015/2302. (44) However, regarding the ‘right of redress’, see Article 13 of Regulation (EC) No 261/2004 and Article 22 of Directive (EU) 2015/2302.
```
```text
[32015L2302:A:w068:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 14 to Article 15, PDF p. 19 | similarity 0.816
In other cases, the
package travel contract may limit compensation to be paid by the organiser as long as that limitation does not apply to
personal injury or damage caused intentionally or with negligence and does not amount to less than three times the
total price of the package.
5. Any right to compensation or price reduction under this Directive shall not affect the rights of travellers under
Regulation (EC) No 261/2004, Regulation (EC) No 1371/2007, Regulation (EC) No 392/2009 of the European
Parliament and of the Council (1), Regulation (EU) No 1177/2010 and Regulation (EU) No 181/2011, and under international
conventions. Travellers shall be entitled to present claims under this Directive and under those Regulations and
international conventions. Compensation or price reduction granted under this Directive and the compensation or price
reduction granted under those Regulations and international conventions shall be deducted from each other in order to
avoid overcompensation.
6. The limitation period for introducing claims under this Article shall not be less than two years.
Article 15
Possibility to contact the organiser via the retailer
Without prejudice to the second subparagraph of Article 13(1), Member States shall ensure that the traveller may
address messages, requests or complaints
Notes: (1) Regulation (EC) No 392/2009 of the European Parliament and of the Council of 23 April 2009 on the liability of carriers of passengers by sea in the event of accidents (OJ L 131, 28.5.2009, p. 24).
```
```text
[52024XC05687:A:w022:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 2.2.7, PDF p. 10 | similarity 0.812
operating air carrier that ultimately has to bear the cost of their overlapping obligations (44).
Resolving such a matter will thus depend on the contractual provisions between organisers and air carriers and the
applicable national law. Any arrangements made in this regard (including practical arrangements to avoid
overcompensation) must not impact negatively on the passengers’ ability to address their claims to either the package
organiser or the air carrier and to obtain the appropriate entitlements under the rights that do not arise under Directive
(EU) 2015/2302.
In this regard, the Court has ruled that pursuant to Article 8(2) of Regulation (EC) No 261/2004, passengers who have the
right to hold the travel organiser liable for reimbursement of the cost of their air ticket under the Package Travel Directive,
can no longer claim reimbursement of the cost of this ticket from the air carrier under Regulation (EC) No 261/2004, even
if the tour organiser is financially incapable of reimbursing the cost of the ticket and has not taken any measures to
guarantee such reimbursement (45). In other words, passengers who are entitled to seek reimbursement from their travel
organiser under Directive (EU) 2015/2302 are not able to seek reimbursement from the
Notes: (44) However, regarding the ‘right of redress’, see Article 13 of Regulation (EC) No 261/2004 and Article 22 of Directive (EU) 2015/2302. (45) Case C-163/18, ECLI:EU:C:2019:585, paragraph 44.
```
```text
[32015L2302:A:w025:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Recital (35) to Recital (38), PDF pp. 6-7 | similarity 0.804
rights
legislation.
(36) This Directive should not affect the rights of travellers to present claims both under this Directive and under
other relevant Union legislation or international conventions, so that travellers continue to have the possibility to
address claims to the organiser, the carrier or any other liable party, or, as the case may be, to more than one
party. It should be clarified that, in order to avoid overcompensation, compensation or price reduction granted
under this Directive and the compensation or price reduction granted under other relevant Union legislation or
international conventions should be deducted from each other. The organiser's liability should be without
prejudice to the right to seek redress from third parties, including service providers.
(37) If the traveller is in difficulty during the trip or holiday, the organiser should be obliged to give appropriate
assistance without undue delay. Such assistance should consist mainly of providing, where appropriate,
information on aspects such as health services, local authorities and consular assistance, as well as practical help,
for instance with regard to distance communications and alternative travel arrangements.
(38) In its Communication of 18 March 2013 entitled ‘Passenger protection in the event of airline insolvency’, the
Commission set out
```

</details>

## q25 (multi)

**Question:** The organiser of my package raised the price by 10% three weeks before departure. Is that allowed and what are my options?

**Reference:** An increase is allowed only if the contract reserves it, for fuel, taxes/fees or exchange rates, notified at least 20 days before the start (Art. 10(1),(3)); because it exceeds 8%, the traveller may accept it or terminate without a termination fee, with a refund within 14 days if no substitute is accepted (Art. 10(2), Art. 11(2),(5)).

**Answer shown to the user:**

> Under EU package travel rules, a price increase three weeks (21 days) before departure is allowed *only if* specific strict conditions are met [32015L2302:A:w054:1, 32015L2302:A:w055:1]. 
> 
> *This is information from the EU texts, not legal advice for your specific case.*
> 
> ### When a price increase is allowed
> An organiser may increase the price after booking only if:
> 1. **The contract expressly reserves that possibility** and explains how price revisions are calculated [32015L2302:A:w054:1].
> 2. **The increase is a direct consequence of changes in:**
>    - The price of passenger carriage resulting from fuel or other power costs [32015L2302:A:w054:1];
>    - Taxes or fees on the travel services imposed by third parties not directly involved in the package (such as tourist taxes, landing taxes, or embarkation/disembarkation fees) [32015L2302:A:w054:1]; or
>    - Exchange rates relevant to the package [32015L2302:A:w054:1].
> 3. **Notice and justification:** The organiser must notify you clearly and comprehensibly on a durable medium, providing a justification and a calculation for the increase, at the latest 20 days before the start of the package [32015L2302:A:w055:1].
> 
> ### Your options because the increase exceeds 8%
> Because the proposed price increase is **10%** (which is more than 8%), it crosses the threshold where you have distinct rights under Article 11(2):
> 1. **Accept the proposed increase** [32015L2302:A:w056:1].
> 2. **Terminate the contract without paying a termination fee** [32015L2302:A:w056:1]. If you choose to terminate, you can also accept a substitute package if the organiser offers one (ideally of equivalent or higher quality) [32015L2302:A:w056:1]. If you do not accept a substitute package, the organiser must refund all payments made without undue delay and at the latest within 14 days of the contract termination [32015L2302:A:w058:1].
> 
> ### What to check next
> - Check your contract to see if price increases were explicitly reserved and if the stated cost categories (fuel, taxes, or exchange rates) match the organiser's justification.
> - Look at the calculation provided by the organiser to ensure the 10% hike stems strictly from those allowed cost factors.

<details><summary>Passages the agent retrieved</summary>

```text
[32015L2302:A:w054:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 10, PDF p. 15 | similarity 0.832
the price
1. Member States shall ensure that after the conclusion of the package travel contract, prices may be increased only if
the contract expressly reserves that possibility and states that the traveller is entitled to price reduction under
paragraph 4. In that event the package travel contract shall state how price revisions are to be calculated. Price increases
shall be possible exclusively as a direct consequence of changes in:
(a) the price of the carriage of passengers resulting from the cost of fuel or other power sources;
(b) the level of taxes or fees on the travel services included in the contract imposed by third parties not directly involved
in the performance of the package, including tourist taxes, landing taxes or embarkation or disembarkation fees at
ports and airports; or
(c) the exchange rates relevant to the package.
2. If the price increase referred to in paragraph 1 of this Article exceeds 8 % of the total price of the package,
Article 11(2) to (5) shall apply.
3. Irrespective of its extent, a price increase shall be possible only if the organiser notifies the traveller clearly and
comprehensibly of it with a justification for that increase and a calculation,
```
```text
[32015L2302:A:w055:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 10 to Article 11, PDF pp. 15-16 | similarity 0.838
the package,
Article 11(2) to (5) shall apply.
3. Irrespective of its extent, a price increase shall be possible only if the organiser notifies the traveller clearly and
comprehensibly of it with a justification for that increase and a calculation, on a durable medium at the latest 20 days
before the start of the package.
4. If the package travel contract stipulates the possibility of price increases, the traveller shall have the right to a price
reduction corresponding to any decrease in the costs referred to in points (a), (b) and (c) of paragraph 1 that occurs after
the conclusion of the contract before the start of the package.
5. In the event of a price decrease, the organiser shall have the right to deduct actual administrative expenses from
the refund owed to the traveller. At the traveller's request, the organiser shall provide proof of those administrative
expenses.
Article 11
Alteration of other package travel contract terms
1. Member States shall ensure that, before the start of the package, the organiser may not unilaterally change package
travel contract terms other than the price in accordance with Article 10, unless:
(a) the organiser has reserved that right in the contract;
(b)
```
```text
[32015L2302:A:w021:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Recital (33), PDF pp. 5-6 | similarity 0.839
travel contract. However,
travellers should have the right to terminate the package travel contract if the changes alter significantly any of
the main characteristics of the travel services. This may for instance be the case if the quality or the value of the
travel services diminishes. Changes of departure or arrival times indicated in the package travel contract should
be considered significant, for instance, where they would impose on the traveller considerable inconvenience or
additional costs, for instance rearrangement of transport or accommodation. Price increases should be possible
only if there has been a change in the cost of fuel or other power sources for the carriage of passengers, in taxes
or fees imposed by a third party not directly involved in the performance of the travel services included in the
package travel contract or in the exchange rates relevant to the package and only if the contract expressly
reserves the possibility of such a price increase and states that the traveller is entitled to a price reduction
corresponding to a decrease in those costs. If the organiser proposes a price increase of more than 8 % of the
total price, the traveller should be entitled to terminate the package
```
```text
[32015L2302:A:w087:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Annex I, PDF p. 26 | similarity 0.795
contract.
— Travellers are given an emergency telephone number or details of a contact point where they can get in touch with
the organiser or the travel agent.
— Travellers may transfer the package to another person, on reasonable notice and possibly subject to additional costs.
— The price of the package may only be increased if specific costs rise (for instance fuel prices), and if expressly
provided for in the contract, and in any event not later than 20 days before the start of the package. If the price
increase exceeds 8 % of the price of the package, the traveller may terminate the contract. If the organiser reserves
the right to a price increase, the traveller has a right to a price reduction if there is a decrease in the relevant costs.
— Travellers may terminate the contract without paying any termination fee and get a full refund of any payments if
any of the essential elements of the package, other than the price, are changed significantly. If before the start of the
package the trader responsible for the package cancels the package, travellers are entitled to a refund and
compensation where appropriate.
— Travellers may terminate the
```
```text
[32015L2302:A:w022:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Recital (33) to Recital (34), PDF p. 6 | similarity 0.793
the traveller is entitled to a price reduction
corresponding to a decrease in those costs. If the organiser proposes a price increase of more than 8 % of the
total price, the traveller should be entitled to terminate the package travel contract without paying a termination
fee.
(34) It is appropriate to set out specific rules on remedies as regards the lack of conformity in the performance of the
package travel contract. The traveller should be entitled to have problems resolved and, where a significant
proportion of travel services included in the package travel contract cannot be provided, the traveller should be
offered suitable alternative arrangements. If the organiser does not remedy the lack of conformity within a
reasonable period set by the traveller, the traveller should be able to do so himself and request reimbursement of
the necessary expenses. In certain cases there should not be a need to specify a time-limit, in particular if
immediate remedy is required. This would apply, for instance, when, due to the delay of a bus provided by the
organiser, the traveller has to take a taxi to catch his flight on time. Travellers should also be entitled to a price
reduction, termination
```
```text
[32015L2302:A:w056:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 11, PDF p. 16 | similarity 0.841
shall ensure that, before the start of the package, the organiser may not unilaterally change package
travel contract terms other than the price in accordance with Article 10, unless:
(a) the organiser has reserved that right in the contract;
(b) the change is insignificant; and
(c) the organiser informs the traveller of the change in a clear, comprehensible and prominent manner on a durable
medium.
2. If, before the start of the package, the organiser is constrained to alter significantly any of the main characteristics
of the travel services as referred to in point (a) of the first subparagraph of Article 5(1) or cannot fulfil the special
requirements as referred to in point (a) of Article 7(2), or proposes to increase the price of the package by more than
8 % in accordance with Article 10(2), the traveller may within a reasonable period specified by the organiser:
(a) accept the proposed change; or
(b) terminate the contract without paying a termination fee.
If the traveller terminates the package travel contract, the traveller may accept a substitute package where this is offered
by the organiser, if possible of an equivalent or a higher quality.
3. The organiser shall without undue delay
```
```text
[32015L2302:A:w058:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 11 to Article 12, PDF p. 16 | similarity 0.827
subparagraph of paragraph 2 result in a package of lower quality or cost,
the traveller shall be entitled to an appropriate price reduction.
5. If the package travel contract is terminated pursuant to point (b) of the first subparagraph of paragraph 2 of this
Article, and the traveller does not accept a substitute package, the organiser shall refund all payments made by or on
behalf of the traveller without undue delay and in any event not later than 14 days after the contract is terminated.
Article 14(2), (3), (4), (5) and (6) shall apply mutatis mutandis.
Article 12
Termination of the package travel contract and the right of withdrawal before the start of the package
1. Member States shall ensure that the traveller may terminate the package travel contract at any time before the start
of the package. Where the traveller terminates the package travel contract under this paragraph, the traveller may be
required to pay an appropriate and justifiable termination fee to the organiser. The package travel contract may specify
reasonable standardised termination fees based on the time of the termination of the contract before the start of the
package and the expected cost savings and income from alternative
```

</details>

## q26 (multi)

**Question:** My train arrives two hours late. If I take a refund of my ticket, can I also get delay compensation?

**Reference:** No: compensation is due for delays on tickets whose cost has not been reimbursed under Art. 18 (Art. 19(1)). Without a refund, a delay of 120 minutes or more gives at least 50% of the ticket price (Art. 19(1)(b)).

**Answer shown to the user:**

> No, under EU rail passenger rights (Regulation (EU) 2021/782), you cannot get delay compensation if the cost of the ticket has been reimbursed [32021R0782:A:w054:1]. 
> 
> ### The Rules
> * **Reimbursement (Refund):** If you face a projected delay of 60 minutes or more at your final destination, you can choose to stop travelling and request reimbursement of the full cost of the ticket (or for the parts not made, and parts already made if your journey no longer serves its original purpose) [32021R0782:A:w050:1].
> * **Delay Compensation:** Passengers are entitled to compensation for delays if the cost of the ticket **has not been reimbursed** [32021R0782:A:w054:1]. For a delay of 120 minutes or more, the minimum compensation is 50% of the ticket price [32021R0782:A:w054:1]. 
> 
> Therefore, you must choose between taking a full refund (and abandoning/reversing your trip) or continuing your journey (or accepting re-routing) and claiming delay compensation. You cannot combine a full ticket refund with delay compensation for that same ticket.
> 
> *Note: This information is based on the published text of Regulation (EU) 2021/782 and does not constitute formal legal advice.*

<details><summary>Passages the agent retrieved</summary>

```text
[32021R0782:A:w054:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 18 to Article 19, PDF p. 19 | similarity 0.777
common form referred to in paragraph 6. Railway
undertakings shall not reject a request for reimbursement solely on the grounds that the passenger has not used that
form. If a request is not sufficiently precise, the railway undertaking shall ask the passenger to clarify the request and shal l
assist the passenger to do so.
Article 19
Compensation
1. Without losing the right of transport, a passenger is entitled to compensation for delays from the railway undertaking
if he or she is facing a delay between the places of departure and final destination stated in the ticket or through-ticket
for which the cost has not been reimbursed in accordance with Article 18. The minimum compensation for delays
shall be as follows:
(a) 25 % of the ticket price for a delay of 60 to 119 minutes;
(b) 50 % of the ticket price for a delay of 120 minutes or more.
2. Paragraph 1 shall also apply to passengers who hold a travel pass or season ticket. If those passengers encounter
recurrent delays or cancellations during the period of validity of the travel pass or season ticket, they shall be entitled to
adequate compensation in accordance with the railway undertaking’s
```
```text
[32021R0782:A:w055:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19, PDF p. 19 | similarity 0.738
hold a travel pass or season ticket. If those passengers encounter
recurrent delays or cancellations during the period of validity of the travel pass or season ticket, they shall be entitled to
adequate compensation in accordance with the railway undertaking’s compensation arrangements. These arrangements
shall state the criteria for determining delay and for the calculation of the compensation. Where delays of less than
60 minutes occur repeatedly during the period of validity of the travel pass or season ticket, the delays may be counted
cumulatively and passengers may be compensated in accordance with the railway undertaking’s compensation arrangements
.
3. Without prejudice to paragraph 2, compensation for delay shall be calculated in relation to the full price which the
passenger actually paid for the delayed service. Where the transport contract is for a return journey, compensation for
delay on either the outward or the return leg shall be calculated in relation to the price indicated for that leg of the
journey on the ticket. Where there is no such indication of the price of the individual legs of the journey, the
compensation shall be calculated in relation to half of the price paid for the ticket. In the same way,
```
```text
[32021R0782:A:w050:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 18, PDF p. 18 | similarity 0.735
or more, the
railway undertaking operating the delayed or cancelled service shall immediately offer the passenger the choice between
one of the following options, and shall make the necessary arrangements:
(a) reimbursement of the full cost of the ticket, under the conditions by which it was paid, for the part or parts of his or
her journey not made and for the part or parts already made if the journey is no longer serving any purpose in
relation to the passenger’s original travel plan, together with, when relevant, a return service to the first point of
departure at the earliest opportunity;
(b) continuation or re-routing, under comparable transport conditions, to the final destination at the earliest opportunity;
(c) continuation or re-routing, under comparable transport conditions, to the final destination at a later date at the
passenger’s convenience.
2. Where, for the purposes of points (b) and (c) of paragraph 1, comparable re-routing is operated by the same railway
undertaking or another undertaking is commissioned to perform the re-routing, this shall not generate additional costs to
the passenger. This requirement also applies where the re-routing involves the use of transport of a higher service class
and alternative modes of transport. Railway
```
```text
[32021R0782:A:w059:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19 to Article 20, PDF pp. 20-21 | similarity 0.721
prevent;
(b) fault on the part of the passenger; or
(c) the behaviour of a third party which the railway undertaking, in spite of having taken the care required in the
particular circumstances of the case, was unable to avoid and the consequences of which it was unable to prevent,
such as persons on the track, cable theft, on-board emergencies, law enforcement activities, sabotage or terrorism.
Strikes by the personnel of the railway undertaking, acts or omissions by another undertaking using the same railway
infrastructure and acts or omissions of the infrastructure and station managers are not covered by the exemption referred
to in point (c) of the first subparagraph.
Article 20
Assistance
1. In the case of a delay in arrival or departure, or cancellation of a service, passengers shall be kept informed of the
situation and of the estimated departure time and estimated arrival time of the service or the replacement service by the
railway undertaking or by the station manager as soon as such information is available. Where ticket vendors and tour
operators have such information, they shall also provide it to the passenger.
2. Where the delay referred to in paragraph 1 amounts to 60 minutes
```
```text
[32021R0782:A:w056:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19, PDF pp. 19-20 | similarity 0.720
journey on the ticket. Where there is no such indication of the price of the individual legs of the journey, the
compensation shall be calculated in relation to half of the price paid for the ticket. In the same way, the price for a
delayed service provided under any other form of transport contract entitling the passenger to travel for two or more
subsequent legs shall be calculated in proportion to the full price.
4. The calculation of the period of delay shall not take into account any delay that the railway undertaking can
demonstrate as having occurred outside the Union.
5. The Commission shall adopt an implementing act establishing a common form for compensation requests under
this Regulation by 7 June 2023. That common form shall be established in a format which is accessible to persons with
disabilities and persons with reduced mobility. That implementing act shall be adopted in accordance with the examination
procedure referred to in Article 38(2).
6. Member States may require railway undertakings to accept requests for compensation by particular means of
communication, provided that the request does not create discriminatory effects. Passengers shall have the right to
submit their requests using the common form
```

</details>

## q27 (unanswerable)

**Question:** What compensation do I get if my ferry crossing is delayed by three hours?

**Reference:** The corpus does not cover sea or inland waterway passenger rights; the assistant should say so and not apply air or rail rules.

**Answer shown to the user:**

> NOT IN CORPUS: The corpus covers air passenger rights [32004R0261:A:w016:1], rail passenger rights [32021R0782:A:w054:1], and package travel [32015R2302], but does not contain provisions for ferry or bus and coach passenger rights. To check rights for ferry crossings, you would need to consult EU or national legislation specifically governing maritime passenger rights (such as Regulation (EU) No 1177/2010), or the carrier's terms and conditions.

<details><summary>Passages the agent retrieved</summary>

```text
[32004R0261:A:w016:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 6 to Article 7, PDF pp. 4-5 | similarity 0.700
in the case of all intra-Community
flights of more than 1 500 kilometres and of all other
flights between 1 500 and 3 500 kilometres; or
(c) for four hours or more in the case of all flights not falling
under (a) or (b),
passengers shall be offered by the operating air carrier:
(i) the assistance specified in Article 9(1)(a) and 9(2); and
(ii) when the reasonably expected time of departure is at least
the day after the time of departure previously announced,
the assistance specified in Article 9(1)(b) and 9(1)(c); and
(iii) when the delay is at least five hours, the assistance specified
in Article 8(1)(a).
2. In any event, the assistance shall be offered within the
time limits set out above with respect to each distance bracket.
Article 7
Right to compensation
1. Where reference is made to this Article, passengers shall
receive compensation amounting to:
(a) EUR 250 for all flights of 1 500 kilometres or less;
(b) EUR 400 for all intra-Community flights of more than
1 500 kilometres, and for all other flights between 1 500
and 3 500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the
```
```text
[32021R0782:A:w055:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19, PDF p. 19 | similarity 0.697
hold a travel pass or season ticket. If those passengers encounter
recurrent delays or cancellations during the period of validity of the travel pass or season ticket, they shall be entitled to
adequate compensation in accordance with the railway undertaking’s compensation arrangements. These arrangements
shall state the criteria for determining delay and for the calculation of the compensation. Where delays of less than
60 minutes occur repeatedly during the period of validity of the travel pass or season ticket, the delays may be counted
cumulatively and passengers may be compensated in accordance with the railway undertaking’s compensation arrangements
.
3. Without prejudice to paragraph 2, compensation for delay shall be calculated in relation to the full price which the
passenger actually paid for the delayed service. Where the transport contract is for a return journey, compensation for
delay on either the outward or the return leg shall be calculated in relation to the price indicated for that leg of the
journey on the ticket. Where there is no such indication of the price of the individual legs of the journey, the
compensation shall be calculated in relation to half of the price paid for the ticket. In the same way,
```
```text
[32021R0782:A:w054:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 18 to Article 19, PDF p. 19 | similarity 0.692
common form referred to in paragraph 6. Railway
undertakings shall not reject a request for reimbursement solely on the grounds that the passenger has not used that
form. If a request is not sufficiently precise, the railway undertaking shall ask the passenger to clarify the request and shal l
assist the passenger to do so.
Article 19
Compensation
1. Without losing the right of transport, a passenger is entitled to compensation for delays from the railway undertaking
if he or she is facing a delay between the places of departure and final destination stated in the ticket or through-ticket
for which the cost has not been reimbursed in accordance with Article 18. The minimum compensation for delays
shall be as follows:
(a) 25 % of the ticket price for a delay of 60 to 119 minutes;
(b) 50 % of the ticket price for a delay of 120 minutes or more.
2. Paragraph 1 shall also apply to passengers who hold a travel pass or season ticket. If those passengers encounter
recurrent delays or cancellations during the period of validity of the travel pass or season ticket, they shall be entitled to
adequate compensation in accordance with the railway undertaking’s
```
```text
[32021R0782:A:w058:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 19, PDF p. 20 | similarity 0.689
by financial transaction costs such as fees, telephone costs
or stamps. Railway undertakings may introduce a minimum threshold under which payments for compensation will not
be paid. This threshold shall not exceed EUR 4 per ticket.
9. Passengers shall not have any right to compensation if they are informed of a delay before buying a ticket, or if a
delay due to continuation on a different service or re-routing remains below 60 minutes.
10. A railway undertaking shall not be obliged to pay compensation if it can prove that the delay, missed connection
or cancellation was caused directly by, or was inherently linked with:
(a) extraordinary circumstances not connected with the operation of the railway, such as extreme weather conditions,
major natural disasters or major public health crises, which the railway undertaking, in spite of having taken the care
required in the particular circumstances of the case, was unable to avoid and the consequences of which it was unable
to prevent;
(b) fault on the part of the passenger; or
(c) the behaviour of a third party which the railway undertaking, in spite of having taken the care required in the
particular circumstances of the case, was unable to avoid
```
```text
[32021R0782:A:w123:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Annex I, Article 44 to Annex I, Article 46, PDF p. 41 | similarity 0.686
or delay in delivery of a vehicle, the carrier must, if
the person entitled proves that loss or damage has been suffered thereby, pay compensation not exceeding the amount of
the carriage charge.
2. If, in case of delay in loading for a reason attributable to the carrier, the person entitled elects not to proceed with
the contract of carriage, the carriage charge shall be refunded to him. In addition the person entitled may, if he proves
that loss or damage has been suffered as a result of the delay, claim compensation not exceeding the carriage charge.
Article 45
Compensation for loss
In case of total or partial loss of a vehicle the compensation payable to the person entitled for the loss or damage proved
shall be calculated on the basis of the usual value of the vehicle. It shall not exceed 8 000 units of account. A loaded or
unloaded trailer shall be considered as a separate vehicle.
Article 46
Liability in respect of other articles
1. In respect of articles left inside the vehicle or situated in boxes (e.g. luggage or ski boxes) fixed to the vehicle, the
carrier shall be liable only for loss or damage caused
```

</details>

## q28 (unanswerable)

**Question:** My long-distance coach was cancelled at the bus terminal. What must the bus company offer me?

**Reference:** The core corpus does not contain bus and coach passenger rights (Regulation 181/2011 is only mentioned by name); the assistant should say it cannot answer from the corpus.

**Answer shown to the user:**

> NOT IN CORPUS: I searched for rules regarding cancelled long-distance coach services, but the EU texts in this corpus cover only air passenger rights (Regulation (EC) No 261/2004), rail passenger rights (Regulation (EU) 2021/782), package travel (Directive (EU) 2015/2302), and bus/coach rights are not included. 
> 
> To find out what the bus company must offer you, you would need to consult EU bus and coach passenger rights legislation (Regulation (EU) No 181/2011) or the carrier's own terms and conditions, which are outside this corpus.

<details><summary>Passages the agent retrieved</summary>

```text
[32004R0261:A:w019:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 8 to Article 9, PDF p. 5 | similarity 0.640
— a return flight to the first point of departure, at the
earliest opportunity;
(b) re-routing, under comparable transport conditions, to their
final destination at the earliest opportunity; or
(c) re-routing, under comparable transport conditions, to their
final destination at a later date at the passenger's convenience
, subject to availability of seats.
2. Paragraph 1(a) shall also apply to passengers whose
flights form part of a package, except for the right to reimbursement
where such right arises under Directive 90/314/EEC.
3. When, in the case where a town, city or region is served
by several airports, an operating air carrier offers a passenger a
flight to an airport alternative to that for which the booking
was made, the operating air carrier shall bear the cost of transferring
the passenger from that alternative airport either to that
for which the booking was made, or to another close-by destination
agreed with the passenger.
Article 9
Right to care
1. Where reference is made to this Article, passengers shall
be offered free of charge:
(a) meals and refreshments in a reasonable relation to the
waiting time;
(b) hotel accommodation in cases
— where a stay of one or more nights becomes necessary,
```
```text
[32021R0782:A:w050:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 18, PDF p. 18 | similarity 0.639
or more, the
railway undertaking operating the delayed or cancelled service shall immediately offer the passenger the choice between
one of the following options, and shall make the necessary arrangements:
(a) reimbursement of the full cost of the ticket, under the conditions by which it was paid, for the part or parts of his or
her journey not made and for the part or parts already made if the journey is no longer serving any purpose in
relation to the passenger’s original travel plan, together with, when relevant, a return service to the first point of
departure at the earliest opportunity;
(b) continuation or re-routing, under comparable transport conditions, to the final destination at the earliest opportunity;
(c) continuation or re-routing, under comparable transport conditions, to the final destination at a later date at the
passenger’s convenience.
2. Where, for the purposes of points (b) and (c) of paragraph 1, comparable re-routing is operated by the same railway
undertaking or another undertaking is commissioned to perform the re-routing, this shall not generate additional costs to
the passenger. This requirement also applies where the re-routing involves the use of transport of a higher service class
and alternative modes of transport. Railway
```
```text
[32004R0261:A:w014:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 5, PDF p. 4 | similarity 0.639
in event of re-routing
when the reasonably expected time of departure of
the new flight is at least the day after the departure as it
was planned for the cancelled flight, the assistance specified
in Article 9(1)(b) and 9(1)(c); and
(c) have the right to compensation by the operating air carrier
in accordance with Article 7, unless:
(i) they are informed of the cancellation at least two
weeks before the scheduled time of departure; or
(ii) they are informed of the cancellation between two
weeks and seven days before the scheduled time of
departure and are offered re-routing, allowing them to
depart no more than two hours before the scheduled
time of departure and to reach their final destination
less than four hours after the scheduled time of arrival;
or
(iii) they are informed of the cancellation less than seven
days before the scheduled time of departure and are
offered re-routing, allowing them to depart no more
than one hour before the scheduled time of departure
and to reach their final destination less than two hours
after the scheduled time of arrival.
2. When passengers are informed of the cancellation, an
explanation shall be given concerning possible alternative transport
.
```
```text
[52024XC05687:A:w043:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.2, PDF p. 16 | similarity 0.630
Right to reimbursement, re-routing or rebooking in the event of denied boarding or cancellation
Article 8(1) of Regulation (EC) No 261/2004 imposes on air carriers the obligation to offer passengers a triple choice,
between the following:
— reimbursement of the ticket price (76) (77) and, in the case of connections, a return flight to the airport of departure at
the earliest opportunity;
— re-routing to their final destination either at the earliest opportunity; or
— re-routing at a later date at the passenger’s convenience under comparable transport conditions, subject to availability
of seats.
If an operating air carrier has to offer the choice between reimbursement and re-routing, the air carrier must present the
passengers concerned with comprehensive information on all the options concerning reimbursement and re-routing.
Pursuant to Article 5(2) of Regulation (EC) No 261/2004, passengers must receive information on re-routing from the
operating air carrier when informed of the cancellation. The passengers concerned are under no obligation to actively
contribute to seeking the relevant information themselves (78).
As a general principle, if the passenger is denied boarding or is informed about the cancellation of the flight and is correctly
informed of the available options, the choice offered to passengers
Notes: (76) The ticket price is reimbursed for the part or parts of the journey not made, and for the part or parts already made if the flight is no longer serving any purpose in relation to the passenger’s original travel plan. In principle, if the passengers choose to return to their airport of departure, the part or parts of the journey already made no longer serve any purpose in relation to the original travel plan. (77) The price of the ticket to be taken into consideration for the purposes of determining the reimbursement owed by the air carrier to a passenger in the event of cancellation of a flight includes the difference between the amount paid by that passenger and the amount received by the air carrier, which corresponds to a commission collected by a person acting as an intermediary between those two parties, unless that commission was set without the knowledge of the air carrier (Case C-601/17, ECLI:EU:C:2018:702, paragraph 20). (78) Case C-354/18, ECLI:EU:C:2019:637, paragraph 56.
```
```text
[32015L2302:A:w060:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Article 12, PDF p. 17 | similarity 0.625
In the event of termination of the package
travel contract under this paragraph, the traveller shall be entitled to a full refund of any payments made for the
package, but shall not be entitled to additional compensation.
3. The organiser may terminate the package travel contract and provide the traveller with a full refund of any
payments made for the package, but shall not be liable for additional compensation, if:
(a) the number of persons enrolled for the package is smaller than the minimum number stated in the contract and the
organiser notifies the traveller of the termination of the contract within the period fixed in the contract, but not
later than:
(i) 20 days before the start of the package in the case of trips lasting more than six days;
(ii) seven days before the start of the package in the case of trips lasting between two and six days;
(iii) 48 hours before the start of the package in the case of trips lasting less than two days;
or
(b) the organiser is prevented from performing the contract because of unavoidable and extraordinary circumstances
and notifies the traveller of the termination of the contract without undue delay before
```

</details>

## q29 (unanswerable)

**Question:** Will my travel insurance reimburse the hotel I paid for after my flight was cancelled?

**Reference:** Insurance cover is not in the corpus; the assistant should say so, and may point out that the airline's duty of care (hotel) is a separate question.

**Answer shown to the user:**

> NOT IN CORPUS: I searched for provisions on travel insurance reimbursement for privately booked hotels following a flight cancellation, but the available EU passenger-rights texts (such as Regulation (EC) No 261/2004, Regulation (EU) 2021/782, and Directive (EU) 2015/2302) do not cover private travel insurance policies. 
> 
> Whether your travel insurance reimburses your hotel depends entirely on the specific terms and conditions of your private insurance policy. (Under EU air passenger rights, operating air carriers have obligations regarding care such as hotel accommodation only when passengers are delayed or re-routed under specific conditions, but privately purchased insurance coverage is separate.) To answer this, you would need to consult your insurance policy documents or provider.

<details><summary>Passages the agent retrieved</summary>

```text
[52024XC05687:A:w095:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 6.4, PDF p. 30 | similarity 0.677
The right to compensation for cancellation pursuant to Article 5(1) and Article 7 of Regulation (EC) No 261/2004 does not
apply in the case of cancellations made more than 14 days in advance or if the cancellation is caused by extraordinary
circumstances that could not have been avoided even if all reasonable measures had been taken by the air carrier.
The Commission considers that, if public authorities take measures intended to contain the effects of a crisis situation
leading to massive travel disruptions, such measures are by their nature and origin not inherent in the normal exercise of
the activity of air carriers and are outside their actual control.
Article 5(3) waives the right to compensation on condition that the cancellation in question ‘is caused’ by extraordinary
circumstances that could not have been avoided even if all reasonable measures had been taken.
This condition should be considered fulfilled if public authorities either prohibit certain flights or restrict the movement of
people in a manner that de facto excludes the operation of the flight in question.
This condition may also be fulfilled if the flight cancellation occurs in circumstances in which the corresponding movement
of people is not entirely prohibited but
```
```text
[32015L2302:A:w093:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Annex I, PDF p. 28 | similarity 0.668
as agreed, suitable
alternative arrangements will have to be offered to the traveller at no extra cost. Travellers may terminate the
contract without paying any termination fee, where services are not performed in accordance with the contract and
this substantially affects the performance of the package and the organiser fails to remedy the problem.
— Travellers are also entitled to a price reduction and/or compensation for damages where the travel services are not
performed or are improperly performed.
— The organiser has to provide assistance if the traveller is in difficulty.
— If the organiser or, in some Member States, the retailer becomes insolvent, payments will be refunded. If the
organiser or, where applicable, the retailer becomes insolvent after the start of the package and if transport is
included in the package, repatriation of the travellers is secured. XY has taken out insolvency protection with YZ
[the entity in charge of the insolvency protection, e.g. a guarantee fund or an insurance company). Travellers may
contact this entity or, where applicable, the competent authority (contact details, including name, geographical
address, email and telephone number) if services are denied because of XY's insolvency.
Directive (EU) 2015/2302 as transposed into national law (hyperlink)
```
```text
[32015L2302:A:w102:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Annex II, PDF p. 31 | similarity 0.665
those travel services will become part of a linked travel arrangement.
In that case XY has, as required by EU law, protection in place to refund your payments to XY for services not performed
because of XY's insolvency. Please note that this does not provide a refund in the event of the insolvency of
the relevant service provider.
More information on insolvency protection (to be provided in the form of a hyperlink)
Following the hyperlink the traveller will receive the following information:
XY has taken out insolvency protection with YZ (the entity in charge of the insolvency protection, e.g. a guarantee
fund or an insurance company).
Travellers may contact this entity or, where applicable, the competent authority (contact details, including name, geographical
address, email and telephone number) if the services are denied because of XY's insolvency.
Note: This insolvency protection does not cover contracts with parties other than XY, which can be performed despite
XY's insolvency.
Directive (EU) 2015/2302 as transposed into the national law (hyperlink)
```
```text
[32015L2302:A:w020:1] Directive (EU) 2015/2302 (package travel) (legislation; Original text, OJ L 326, 11.12.2015 (not consolidated))
Location: Recital (31) to Recital (33), PDF p. 5 | similarity 0.662
have the right to terminate the
package travel contract without paying any termination fee where unavoidable and extraordinary circumstances
will significantly affect the performance of the package. This may cover for example warfare, other serious
security problems such as terrorism, significant risks to human health such as the outbreak of a serious disease at
the travel destination, or natural disasters such as floods, earthquakes or weather conditions which make it
impossible to travel safely to the destination as agreed in the package travel contract.
(32) In specific situations, the organiser should also be entitled to terminate the package travel contract before the
start of the package without paying compensation, for instance if the minimum number of participants is not
reached and where that possibility has been reserved in the contract. In that event, the organiser should refund all
payments made in respect of the package.
(33) In certain cases organisers should be allowed to make unilateral changes to the package travel contract. However,
travellers should have the right to terminate the package travel contract if the changes alter significantly any of
the main characteristics of the travel services. This may for instance be the case if the quality or the
```
```text
[32004R0261:A:w014:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 5, PDF p. 4 | similarity 0.662
in event of re-routing
when the reasonably expected time of departure of
the new flight is at least the day after the departure as it
was planned for the cancelled flight, the assistance specified
in Article 9(1)(b) and 9(1)(c); and
(c) have the right to compensation by the operating air carrier
in accordance with Article 7, unless:
(i) they are informed of the cancellation at least two
weeks before the scheduled time of departure; or
(ii) they are informed of the cancellation between two
weeks and seven days before the scheduled time of
departure and are offered re-routing, allowing them to
depart no more than two hours before the scheduled
time of departure and to reach their final destination
less than four hours after the scheduled time of arrival;
or
(iii) they are informed of the cancellation less than seven
days before the scheduled time of departure and are
offered re-routing, allowing them to depart no more
than one hour before the scheduled time of departure
and to reach their final destination less than two hours
after the scheduled time of arrival.
2. When passengers are informed of the cancellation, an
explanation shall be given concerning possible alternative transport
.
```

</details>

## q30 (unanswerable)

**Question:** Does Ryanair's own policy let me choose a voucher worth more than the cash refund?

**Reference:** Airline-specific policies are not in the corpus; the assistant should say so without inventing the policy.

**Answer shown to the user:**

> NOT IN CORPUS: I searched the corpus for Ryanair's policies and airline-specific voucher terms, but the corpus contains EU legislative texts (such as Regulation (EC) No 261/2004 and Regulation (EU) 2021/782) rather than individual airline policies or commercial offers. 
> 
> To find out if Ryanair offers a voucher worth more than a cash refund, you will need to check Ryanair's own website, their terms and conditions, or contact their customer service directly. 
> 
> *Note: This is information based on the available texts, not legal advice for your case.*

<details><summary>Passages the agent retrieved</summary>

(none)

</details>

## q31 (unanswerable)

**Question:** What did the 2025 amendment to Regulation 261/2004 change about the delay threshold for compensation?

**Reference:** The corpus holds the 2004 original text and the 2024 guidelines only; it cannot say what any later amendment changed, and the assistant must not invent one.

**Answer shown to the user:**

> NOT IN CORPUS: The corpus does not contain any texts or amendments from 2025. It includes the original 2004 text of Regulation (EC) No 261/2004 and the 2024 Commission interpretative guidelines, neither of which mentions a 2025 amendment [32004R0261:A:w016:1, 52024XC05687:A:w067:1]. 
> 
> To check for recent legislative changes or amendments from 2025 onwards, you would need to consult official publications like the Official Journal of the European Union or current consolidated legislative databases.

<details><summary>Passages the agent retrieved</summary>

```text
[32004R0261:A:w016:1] Regulation (EC) No 261/2004 (air passenger rights) (legislation; Original text, OJ L 46, 17.2.2004 (not consolidated))
Location: Article 6 to Article 7, PDF pp. 4-5 | similarity 0.768
in the case of all intra-Community
flights of more than 1 500 kilometres and of all other
flights between 1 500 and 3 500 kilometres; or
(c) for four hours or more in the case of all flights not falling
under (a) or (b),
passengers shall be offered by the operating air carrier:
(i) the assistance specified in Article 9(1)(a) and 9(2); and
(ii) when the reasonably expected time of departure is at least
the day after the time of departure previously announced,
the assistance specified in Article 9(1)(b) and 9(1)(c); and
(iii) when the delay is at least five hours, the assistance specified
in Article 8(1)(a).
2. In any event, the assistance shall be offered within the
time limits set out above with respect to each distance bracket.
Article 7
Right to compensation
1. Where reference is made to this Article, passengers shall
receive compensation amounting to:
(a) EUR 250 for all flights of 1 500 kilometres or less;
(b) EUR 400 for all intra-Community flights of more than
1 500 kilometres, and for all other flights between 1 500
and 3 500 kilometres;
(c) EUR 600 for all flights not falling under (a) or (b).
In determining the
```
```text
[52024XC05687:A:w067:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.4.7 to Section 4.4.8, PDF p. 22 | similarity 0.766
in which passengers concerned by a flight cancellation are not offered re-routing allowing them to depart no
more than 1 hour before the scheduled time of departure and to reach their final destination less than 2 hours after the
scheduled time of arrival. The Court deduced from this that the right to compensation laid down in Article 7 of Regulation
(EC) No 261/2004 aims to repair a loss of time of at least 3 hours. However, such a delay does not entitle passengers to
compensation if the air carrier can prove that the long delay was caused by extraordinary circumstances that could not
have been avoided even if all reasonable measures had been taken (100) (see Section 5 on extraordinary circumstances).
4.4.8. Compensation for long delay at arrival in the case of connecting flights
The Court (101) takes the view that for the purposes of the compensation provided for in Article 7 of Regulation (EC)
No 261/2004, a delay must be assessed in relation to the scheduled time of arrival at the passenger’s final destination as
defined in Article 2, point (h), of Regulation (EC) No 261/2004, which in the case of directly connecting flights must be
understood as the
Notes: (100) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 69. (101) Case C-11/11, ECLI:EU:C:2013:106, paragraph 47.
```
```text
[52024XC05687:A:w071:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.4.10 to Section 4.4.11, PDF p. 23 | similarity 0.754
hours of more (106).
It follows that the compensation payable to a passenger whose flight is delayed by 3 hours or more, who reaches their final
destination 3 hours or more after the arrival time originally scheduled, may be reduced by 50 %, if the delay is less than
4 hours (107).
In other words, if the delay at arrival is more than 3 and less than 4 hours for a journey of more than 3 500 km, the
compensation can be reduced by 50 % and therefore amounts to EUR 300 in accordance with Article 7(2) of Regulation
(EC) No 261/2004.
However, if a flight has been brought forward an amount of time that gives rise to a right to compensation pursuant to
Article 7, the operating air carrier is still required to pay the full amount. It does not have the possibility to reduce any
compensation to be paid by 50 % on the ground that it has offered the passengers re-routing, allowing them to arrive
without delay at their final destination (108).
4.4.11. Calculation of the distance on the basis of the ‘journey’ to determine the compensation in the event of long delay at the final
destination
Notes: (106) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 63. (107) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 63. (108) Joined Cases C-146/20, C-188/20, C-196/20 and C-270/20, ECLI:EU:C:2021:1038, paragraph 94.
```
```text
[52024XC05687:A:w066:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 4.4.6 to Section 4.4.7, PDF pp. 21-22 | similarity 0.754
could only be
used to contact the travel agent through which the reservation had been made, and not the passenger directly, and that this
travel agent did not send the information to the passenger in good time (98), meaning at least 2 weeks before the scheduled
time of departure.
D. Compensation in the event of long delay at arrival
4.4.7. ‘Long delays’ at arrival
As regards ‘long delays’, the Court has ruled that delayed passengers may suffer from a similar inconvenience as passengers
whose flight is cancelled, consisting in a certain loss of time (99). Based on the principle of equal treatment, passengers
reaching their final destination with a delay of 3 hours or more are entitled to the same compensation (Article 7) as
passengers whose flight is cancelled. The Court predominantly based its ruling on Article 5(1), point (c)(iii), of Regulation
(EC) No 261/2004, in which the EU legislature attaches legal consequences, including the right to compensation, to
situations in which passengers concerned by a flight cancellation are not offered re-routing allowing them to depart no
more than 1 hour before the scheduled time of departure and to reach their final destination less than 2 hours after the
scheduled
Notes: (98) Case C-307/21, ECLI:EU:C:2022:729, paragraph 30. (99) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 54.
```
```text
[52024XC05687:A:w034:1] Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024) (guidance; Commission Notice C/2024/5687, OJ C, 25.9.2024)
Location: Section 3.2.6 to Section 3.3.2, PDF p. 13 | similarity 0.749
to be paid if the air carrier can prove, in accordance with Article 5(3), that the
cancellation is caused by extraordinary circumstances that could not have been avoided even if all reasonable measures had
been taken (63).
3.3. Delay
3.3.1. Delay at departure
Under Article 6(1) of Regulation (EC) No 261/2004, if the departure of a flight is delayed, passengers affected by this delay
have the right to ‘care’ according to Article 9, and to reimbursement and a return flight according to Article 8(1), point (a).
The underlying principle of Article 6(1) is that the rights depend on the duration of the delay and the distance of the flight.
In this regard, it should be noted that the right to re-routing as laid down in Article 8(1), point (b), is not covered under
Article 6(1) as it can be considered that the air carrier is trying, in the first place, to address the cause of the delay in order
to minimise the inconvenience to the passengers.
3.3.2. ‘Long delay’ at arrival
The Court has ruled that a delay at arrival of at least 3 hours gives the same rights in terms of compensation as a
cancellation (64) (for more details,
Notes: (63) See Section 5 on extraordinary circumstances. (64) Joined Cases C-402/07 and C-432/07, ECLI:EU:C:2009:716, paragraph 69. See also Joined Cases C-581/10 and C-629/10, ECLI:EU:C:2012:657, paragraph 40, and Case C-413/11, ECLI:EU:C:2013:246, paragraph 19.
```

</details>

## q32 (unanswerable)

**Question:** What is the email address of Portugal's national enforcement body for rail passenger complaints?

**Reference:** The rail regulation requires Member States to designate enforcement bodies but the corpus does not name Portugal's body or its contact details.

**Answer shown to the user:**

> NOT IN CORPUS: I searched the corpus for Portugal's national enforcement body for rail passenger complaints and its contact details, but the texts (including Regulation (EU) 2021/782 on rail passenger rights) establish the rules and procedures for complaints to national enforcement bodies [32021R0782:A:w081:1] but do not list specific email addresses or contact details for individual Member States' authorities. 
> 
> To find the official email address, you would need to check the official website of Portugal's designated national enforcement body for rail passenger rights (such as the national transport authority or regulator) or consult the European Union Agency for Railways' lists of national enforcement bodies.

<details><summary>Passages the agent retrieved</summary>

```text
[32021R0782:A:w081:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 32 to Article 33, PDF pp. 27-28 | similarity 0.752
Union Agency for Railways.
4. Railway undertakings shall give their contact details to the national enforcement body or bodies of the Member
States in which they operate.
Article 33
Complaint handling by national enforcement bodies and other bodies
1. Without prejudice to the rights of consumers to seek alternative redress pursuant to Directive 2013/11/EU of the
European Parliament and of the Council (15), after having complained unsuccessfully to the railway undertaking or station
manager pursuant to Article 28 the passenger may complain to the national enforcement body or any other body
designated under paragraph 2 of this Article within three months from receiving information on the rejection of the
original complaint. Where no reply is received within three months from making the original complaint, the passenger
shall have the right to complain to the national enforcement body or any other body designated under paragraph 2.
Where necessary, that body shall inform the complainant about his or her right to complain to alternative dispute
resolution bodies to seek individual redress.
2. Any passenger may complain about an alleged infringement of this Regulation either to the national enforcement
body, or to any other body designated by a Member State for that purpose.
Notes: (15) Directive 2013/11/EU of the European Parliament and of the Council of 21 May 2013 on alternative dispute resolution for consumer disputes and amending Regulation (EC) No 2006/2004 and Directive 2009/22/EC (OJ L 165, 18.6.2013, p. 63).
```
```text
[32021R0782:A:w082:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 33, PDF pp. 27-28 | similarity 0.744
to alternative dispute
resolution bodies to seek individual redress.
2. Any passenger may complain about an alleged infringement of this Regulation either to the national enforcement
body, or to any other body designated by a Member State for that purpose.
3. The national enforcement body or any other body designated under paragraph 2 shall acknowledge receipt of the
complaint within two weeks of receiving it. The complaint-handling procedure shall take a maximum of three months
from the date of the establishment of the complaint file. For complex cases, that body may extend that period to six
months. In such a case, it shall inform the passenger of the reasons for the extension and of the expected time needed to
conclude the procedure. Only those cases that involve legal proceedings may take longer than six months. Where that
body is also an alternative dispute resolution body within the meaning of Directive 2013/11/EU, the time limits laid
down in that Directive shall prevail.
The complaint-handling procedure shall be made accessible to persons with disabilities and to persons with reduced
mobility.
4. Passenger complaints about an incident involving a railway undertaking shall be handled by the national
enforcement body or any other body
```
```text
[32021R0782:A:w075:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 28, PDF pp. 25-26 | similarity 0.741
and obligations covered by this Regulation in
their respective fields of responsibility. They shall make their contact details and working language, or languages, widely
known to passengers. This mechanism shall not apply for the purposes of Chapter III.
2. Passengers may submit a complaint to any railway undertaking or station manager regarding their respective fields
of responsibility via the mechanisms referred to in paragraph 1. Such a complaint shall be submitted within three months
of the incident that it concerns. Within one month of receiving the complaint, the addressee shall either give a reasoned
reply or, in justified cases, inform the passenger that he or she will receive a reply within a period of less than three
months from the date of receipt of the complaint. Railway undertakings and station managers shall keep the data
necessary to assess the complaint for the duration of the entire complaint-handling procedure, including the
complaint-handling procedures referred to in Articles 33 and 34, and shall make that data available to national
enforcement bodies upon request.
3. Details of the complaint-handling procedure shall be accessible to the public, including to persons with disabilities
and to persons with reduced mobility. This information shall be available upon
```
```text
[32021R0782:A:w080:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 32 to Article 33, PDF p. 27 | similarity 0.738
For the purpose of paragraph 1, railway undertakings, station managers, infrastructure managers, ticket vendors and
tour operators shall provide the national enforcement bodies with relevant documents and information at their request
without undue delay and, in any event, within one month from the receipt of the request. In complex cases, the national
enforcement body may extend this period to a maximum of three months from the receipt of the request. In carrying out
their functions, the national enforcement bodies shall take account of the information submitted to them by the body
designated under Article 33 to handle complaints, if this is a different body. They may also decide on enforcement actions
based on individual complaints transmitted by such a body.
3. Every two years, the national enforcement bodies shall publish reports with statistics on their activity, including on
penalties applied by 30 June of the following calendar year. Those reports shall be made available on the website of the
European Union Agency for Railways.
4. Railway undertakings shall give their contact details to the national enforcement body or bodies of the Member
States in which they operate.
Article 33
Complaint handling by national enforcement bodies and other bodies
1. Without
```
```text
[32021R0782:A:w083:1] Regulation (EU) 2021/782 (rail passenger rights) (legislation; Original text, OJ L 172, 17.5.2021 (not consolidated))
Location: Article 33 to Article 34, PDF p. 28 | similarity 0.731
prevail.
The complaint-handling procedure shall be made accessible to persons with disabilities and to persons with reduced
mobility.
4. Passenger complaints about an incident involving a railway undertaking shall be handled by the national
enforcement body or any other body designated under paragraph 2 of the Member State that granted that undertaking’s
licence.
5. Where a complaint relates to alleged infringements by station or infrastructure managers, the complaint shall be
handled by the national enforcement body or any other body designated under paragraph 2 of the Member State on
whose territory the incident occurred.
6. In the framework of cooperation pursuant to Article 34, the national enforcement bodies may derogate from
paragraphs 4 or 5 of this Article, or both of them, where for justified reasons, in particular those related to language
or place of residence, this is in the passenger’s interest.
Article 34
Exchange of information and cross-border cooperation between national enforcement bodies
1. Where different bodies are designated under Articles 31 and 33, reporting mechanisms shall be set up to ensure the
exchange of information between them, in accordance with Regulation (EU) 2016/679, in order to help the national
enforcement body to carry out its tasks of supervision
```

</details>
