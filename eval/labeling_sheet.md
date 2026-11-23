# Human labels: grade these before reading eval/verdicts.json

For each answer, write in eval/human_labels.csv: `correct` 1/0 (right against the reference, or a proper refusal for unanswerable; for multi, both parts must be right), `supported` 1/0 (every claim is in the retrieved passages), and `notes` saying why for every 0.

## q31 (unanswerable)

**Question:** What compensation do passengers get for a delayed domestic flight within the United Kingdom under UK rules after Brexit?

**Reference:** The documents do not cover this; the agent should say so and escalate to a specialist.

**Agent's searches and top hit of each:**

- call search({'query': 'compensation delayed domestic flight UK Brexit Regulation 261 2004'})
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 4.4.7 | ‘Long delays’ at arrival | relevance 0.75
- call search({'query': 'UK domestic flight compensation post brexit'})
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 4.2 | Right to reimbursement, re-routing or rebooking in the event of denied boarding or cancellation | relevance 0.75

**Answer:**

The documents I have do not cover UK domestic flight rules after Brexit. The provided documents cover EU passenger rights under Regulation (EC) No 261/2004 and its interpretative guidelines, but do not contain the specific post-Brexit UK statutory rules applicable to domestic flights within the United Kingdom.

---

## q32 (unanswerable)

**Question:** How many kilograms of hand luggage may a passenger take on board a flight within the EU?

**Reference:** The documents do not cover this; the agent should say so and escalate to a specialist.

**Agent's searches and top hit of each:**

- call search({'query': 'hand luggage baggage allowance flight EU passenger rights'})
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 10 | AIR CARRIER LIABILITY UNDER THE MONTREAL CONVENTION | relevance 0.75

**Answer:**

The documents I have do not cover this. 

The provided EU passenger-rights regulations and guidelines do not specify a weight limit or allowance for hand luggage on flights. Hand luggage policies and weight allowances are determined individually by each airline rather than by EU passenger-rights law.

---

## q33 (unanswerable)

**Question:** The hotel in a customer's package holiday was overbooked on arrival. How much compensation is she owed for the hotel?

**Reference:** The documents do not cover this; the agent should say so and escalate to a specialist.

**Agent's searches and top hit of each:**

- call search({'query': 'package holiday hotel overbooking compensation'})
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 4.3.2 | Provision of meals, refreshments and accommodation | relevance 0.71
- call search({'query': 'Package Travel Directive compensation hotel overbooking'})
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 2.2.7 | Scope of Regulation (EC) No 261/2004 in relation to Directive (EU) 2015/2302 (Package Travel Directive) | relevance 0.78

**Answer:**

The documents I have do not cover specific statutory compensation amounts for hotel overbookings under package holidays. 

The corpus only contains transport passenger rights regulations (such as EU Regulation 261/2004 for air travel, and regulations for rail, bus/coach, and sea) and notes that while Regulation 261/2004 applies to flights within a package tour, it does not apply to package tour cancellations or incidents caused by reasons other than flight disruptions (such as hotel cancellations) [Commission Guidelines on Regulation 261/2004 (2024), Section 2.2.7]. 

Rules regarding hotel overbookings or price reductions/compensation under the Package Travel Directive (Directive (EU) 2015/2302) are not present in the provided documents.

---

## q34 (unanswerable)

**Question:** What compensation do US Department of Transportation rules give for a delayed domestic flight in the United States?

**Reference:** The documents do not cover this; the agent should say so and escalate to a specialist.

**Agent's searches and top hit of each:**

- call search({'query': 'US Department of Transportation delayed domestic flight compensation'})
- [1] Regulation (EU) No 1177/2010, Recital (14) | relevance 0.73

**Answer:**

The documents I have do not cover this. The available regulations only cover EU passenger rights for air, rail, bus/coach, and sea transport (such as Regulation (EC) No 261/2004 for flights), but do not contain rules from the US Department of Transportation for domestic flights within the United States.

---

## q35 (unanswerable)

**Question:** The taxi transfer the agency booked to the airport arrived late and the customer missed her flight. What are her rights against the taxi company?

**Reference:** The documents do not cover this; the agent should say so and escalate to a specialist.

**Agent's searches and top hit of each:**

- call search({'query': 'taxi transfer missed flight passenger rights Regulation (EC) No 261/2004'})
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 7 | COMPENSATION, REIMBURSEMENT, RE-ROUTING AND CARE IN THE CASE OF MULTIMODAL JOURNEYS | relevance 0.77

**Answer:**

The documents I have do not cover this. 

The available passenger-rights regulations (covering air, rail, bus/coach, and sea) and guidelines do not contain rules regarding taxi transfers or the rights of passengers against a taxi company when a late taxi causes a missed flight.

---

## q36 (unanswerable)

**Question:** What is the maximum fine in euros that Spain's enforcement body can impose on an airline that refuses to pay compensation?

**Reference:** The documents only say Member States must set effective, proportionate and dissuasive penalties; they give no amounts. The agent should say so.

**Agent's searches and top hit of each:**

- call search({'query': 'fine enforcement body Spain penalty airline refusal compensation'})
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 8.1 | Complaints to national enforcement bodies | relevance 0.74

**Answer:**

The documents I have do not cover this. 

The available texts note that Member States must lay down sanctions for infringements of Regulation (EC) No 261/2004 that are "effective, proportionate and dissuasive" [Regulation (EC) No 261/2004, Article 16], but they do not specify the maximum fine or specific monetary amounts that Spain's national enforcement body can impose.

---

## q25 (multi)

**Question:** Two customers each arrived 70 minutes late: one by train, the other on a 1,000 km flight. Who can claim compensation?

**Reference:** Only the train passenger (25% of the ticket price). Flight compensation for delay requires at least 3 hours late at arrival.

**Agent's searches and top hit of each:**

- call search({'query': 'train delay compensation 60 minutes 120 minutes passenger rights'})
- call search({'query': 'flight delay compensation 3 hours 1000 km regulation 261'})
- [1] Regulation (EU) 2021/782, Article 19 | Compensation | relevance 0.79
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 4.4.7 | ‘Long delays’ at arrival | relevance 0.77

**Answer:**

Only the train passenger can claim compensation. 

### Conditions:
* **Train passenger:** Arriving 70 minutes late entitles a rail passenger to a minimum compensation of 25% of the ticket price, as the delay falls within the 60 to 119 minutes bracket [Regulation (EU) 2021/782, Article 19].
* **Flight passenger:** A flight passenger arriving 70 minutes late is not entitled to compensation. Under EU air passenger rights, compensation for a long delay requires reaching the final destination 3 hours or more late [Commission Guidelines on Regulation 261/2004 (2024), Section 4.4.7].

---

## q26 (multi)

**Question:** A 2,000 km flight within the EU was cancelled five days before departure. The airline re-routed the customer, arriving 2.5 hours after the original arrival time. How much compensation is due?

**Reference:** EUR 200: compensation is due (informed less than 7 days before and arriving more than 2 hours late), EUR 400 for this distance, which the airline may reduce by 50% because arrival was less than 3 hours late.

**Agent's searches and top hit of each:**

- call search({'query': 'cancellation re-routing arrival time compensation 261 2004'})
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 4.4.7 | ‘Long delays’ at arrival | relevance 0.83
- call search({'query': 'Article 7 compensation amount 1500 km 3500 km Regulation 261 2004'})
- [1] Regulation (EC) No 261/2004, Article 7 | Right to compensation | relevance 0.85
- call search({'query': 'cancellation informed less than 7 days departure arrival 2 hours re-routing compensation 261 2004'})
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 4.4.13 | Re-routing and arrival more than 2 hours after the scheduled arrival time but less than 3 hours | relevance 0.84

**Answer:**

**Amount due:** €400 (which may be reduced by 50% to **€200** if the re-routed flight's departure time met specific timing criteria—see conditions below).

**Conditions:**
* **Compensation amount:** For an intra-Community flight of more than 1,500 km, the standard compensation under Article 7 is €400 [Regulation (EC) No 261/2004, Article 7].
* **Why compensation is due:** Because the customer was notified of the cancellation 5 days before departure (which is less than 2 weeks) and arrived 2.5 hours late (which is 2 hours or more after the scheduled arrival time), the re-routing does not exempt the airline from paying compensation [Commission Guidelines on Regulation 261/2004 (2024), Section 4.4.13, Regulation (EC) No 261/2004, Article 5].
* **Potential 50% reduction:** The airline may reduce the compensation by 50% (paying €200 instead of €400) if the alternative flight allowed the passenger to reach their final destination less than 3 hours after the scheduled arrival time [Regulation (EC) No 261/2004, Article 7]. 
* **Departure time check:** For the cancellation to be exempt from compensation entirely when notified between 7 and 14 days in advance, the re-routing must also have allowed the customer to depart no more than 2 hours before the original scheduled time of departure [Regulation (EC) No 261/2004, Article 5]. (Since the prompt specifies notification 5 days before—which falls into the 7-to-14-day window under Article 5(1)(c)(ii)—this departure condition applies; if the airline gave less than 7 days' notice, the stricter 1-hour departure limit applies [Regulation (EC) No 261/2004, Article 5]).
* **Extraordinary circumstances:** No compensation is due if the cancellation was caused by extraordinary circumstances that could not have been avoided even if all reasonable measures had been taken [Regulation (EC) No 261/2004, Article 5].

[Regulation (EC) No 261/2004, Article 5]
[Regulation (EC) No 261/2004, Article 7]
[Commission Guidelines on Regulation 261/2004 (2024), Section 4.4.13]

---

## q27 (multi)

**Question:** Passengers are stranded overnight after a cancelled departure. How many hotel nights must the carrier pay, and up to what cost, for a long-distance coach compared with a ferry?

**Reference:** Coach: up to EUR 80 per night for a maximum of 2 nights. Ferry: up to EUR 80 per night for a maximum of 3 nights.

**Agent's searches and top hit of each:**

- call search({'query': 'bus coach accommodation hotel cancellation overnight passenger rights'})
- call search({'query': 'sea inland waterway accommodation hotel cancellation overnight passenger rights'})
- [1] Regulation (EU) No 181/2011, Article 21 | Assistance in case of cancelled or delayed departures | relevance 0.79
- [1] Regulation (EU) No 1177/2010, Recital (13) | relevance 0.78
- call search({'query': 'Regulation (EU) No 1177/2010 Article 17 assistance accommodation ashore'})
- [1] Regulation (EU) No 1177/2010, Article 17 | Assistance in the event of cancelled or delayed departures | relevance 0.86

**Answer:**

For passengers stranded overnight due to a cancelled departure:

### **Long-Distance Coach**
* **Number of nights:** Maximum of **2 nights** [Regulation (EU) No 181/2011, Article 21].
* **Cost limit:** Up to **EUR 80 per night** per passenger, excluding transport to and from the terminal and place of accommodation [Regulation (EU) No 181/2011, Article 21].
* **Conditions:** Applies to scheduled journeys with a scheduled duration of more than 3 hours where departure from a terminal is cancelled (or delayed by more than 90 minutes) and a stay of 1 or more nights becomes necessary [Regulation (EU) No 181/2011, Article 21].

### **Ferry (Sea and Inland Waterway)**
* **Number of nights:** Maximum of **3 nights** [Regulation (EU) No 1177/2010, Article 17].
* **Cost limit:** Up to **EUR 80 per night** per passenger for accommodation ashore, not including transport to and from the port terminal and place of accommodation [Regulation (EU) No 1177/2010, Article 17]. Alternatively, adequate accommodation may be offered on board where and when physically possible [Regulation (EU) No 1177/2010, Article 17].
* **Conditions:** Applies where departure from a port terminal is cancelled (or delayed for more than 90 minutes) and a stay of one or more nights (or a stay additional to that intended) becomes necessary [Regulation (EU) No 1177/2010, Article 17].

### **Citations**
* Coach: [Regulation (EU) No 181/2011, Article 21]
* Ferry: [Regulation (EU) No 1177/2010, Article 17]

---

## q28 (multi)

**Question:** A customer's flight is delayed by more than five hours at departure and he no longer wants to travel. What can he get?

**Reference:** Reimbursement of the ticket within seven days, plus a return flight to the first point of departure when relevant.

**Agent's searches and top hit of each:**

- call search({'query': 'flight delayed departure five hours reimbursement right to care'})
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 4.3.2 | Provision of meals, refreshments and accommodation | relevance 0.77
- call search({'query': 'Article 6 delay at departure five hours reimbursement Article 8'})
- [1] Regulation (EC) No 261/2004, Article 6 | Delay | relevance 0.82

**Answer:**

If a flight is delayed at departure by at least five hours and the customer no longer wants to travel, they can get:

* **Reimbursement** within seven days of the full cost of the ticket at the price it was bought, for the part(s) of the journey not made, and also for the part(s) already made if the flight is no longer serving any purpose in relation to the original travel plan [Regulation (EC) No 261/2004, Article 8].
* **A return flight** to the first point of departure at the earliest opportunity, if applicable [Regulation (EC) No 261/2004, Article 8].
* **Care** while waiting, which includes meals and refreshments in a reasonable relation to the waiting time, plus two telephone calls, fax messages, or emails [Regulation (EC) No 261/2004, Article 6, Regulation (EC) No 261/2004, Article 9]. If a stay of one or more nights becomes necessary, hotel accommodation and transport between the airport and the place of accommodation must also be offered [Regulation (EC) No 261/2004, Article 6, Regulation (EC) No 261/2004, Article 9].

---

## q29 (multi)

**Question:** A train arrives 2.5 hours late because of extreme weather. Does the passenger get delay compensation, and how many hotel nights can the railway limit him to if he must stay over?

**Reference:** No compensation (extreme weather is an exemption), but he still gets assistance; the railway may limit accommodation to a maximum of three nights.

**Agent's searches and top hit of each:**

- call search({'query': 'rail delay compensation 2 hours extreme weather force majeure'})
- call search({'query': 'rail accommodation hotel nights limit overnight stay'})
- [1] Regulation (EU) 2021/782, Recital (37) | relevance 0.76
- [1] Regulation (EU) No 181/2011, Article 21 | Assistance in case of cancelled or delayed departures | relevance 0.70
- call search({'query': 'Regulation (EU) 2021/782 Recital 37'})
- call search({'query': 'Regulation (EU) 2021/782 Article 19'})
- [1] Regulation (EU) 2021/782, Preamble | relevance 0.82
- [1] Regulation (EU) No 1177/2010, Article 19 | Compensation of the ticket price in the event of delay in arrival | relevance 0.82

**Answer:**

**No, the passenger does not get delay compensation**, but **they are entitled to hotel accommodation**, which the railway can limit to a **maximum of three nights**.

### Conditions:
* **Compensation:** Passengers are normally entitled to compensation of 50% of the ticket price for a delay of 120 minutes or more [Regulation (EU) 2021/782, Article 19]. However, the railway undertaking is not obliged to pay compensation if it can prove that the delay was caused by extraordinary circumstances, such as extreme weather conditions, which it was unable to avoid or prevent [Regulation (EU) 2021/782, Article 19].
* **Accommodation:** In cases where a stay of one or more nights becomes necessary due to those extraordinary circumstances, the railway undertaking may limit the duration of hotel or other accommodation to a maximum of three nights [Regulation (EU) 2021/782, Article 20].

### Citations:
* [Regulation (EU) 2021/782, Article 19]
* [Regulation (EU) 2021/782, Article 20]

---

## q30 (multi)

**Question:** A flight from Madrid to Paris (about 1,050 km) was diverted and landed in Lyon, which does not serve Paris. What compensation can the customer claim?

**Reference:** It is treated as a cancellation, so EUR 250 (flight of 1,500 km or less), unless extraordinary circumstances apply.

**Agent's searches and top hit of each:**

- call search({'query': 'flight cancellation diversion compensation Regulation 261 2004'})
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 3.2.4 | Diverted flight | relevance 0.84
- call search({'query': 'Regulation 261 2004 Article 7 compensation amount 1500 km'})
- [1] Regulation (EC) No 261/2004, Article 7 | Right to compensation | relevance 0.86

**Answer:**

Yes, the customer can claim compensation. 

### Conditions and Amount
* **Treatment as a Cancellation:** Because the flight was diverted to an airport (Lyon) that does not serve the original final destination (Paris), the diversion must be treated in the same way as a flight cancellation [Commission Guidelines on Regulation 261/2004 (2024), Section 3.2.4].
* **Compensation Amount:** For flights of 1,500 kilometres or less, the standard compensation is **EUR 250** [Regulation (EC) No 261/2004, Article 7].
* **Exceptions:** Compensation is not owed if the passenger was informed of the cancellation/diversion sufficiently in advance under the rules of Article 5(1), or if the diversion was caused by extraordinary circumstances that could not have been avoided even if all reasonable measures had been taken [Commission Guidelines on Regulation 261/2004 (2024), Section 3.2.6, Regulation (EC) No 261/2004, Article 5]. (This assumes no extraordinary circumstances apply.)

### Citations
* [Commission Guidelines on Regulation 261/2004 (2024), Section 3.2.4]
* [Regulation (EC) No 261/2004, Article 5]
* [Regulation (EC) No 261/2004, Article 7]

---

## q01 (single)

**Question:** A customer's flight of 1,200 km was cancelled and he is entitled to compensation. How much should he receive?

**Reference:** EUR 250 (flights of 1,500 km or less).

**Agent's searches and top hit of each:**

- call search({'query': 'compensation amount flight distance 1500 km or less'})
- [1] Regulation (EC) No 261/2004, Article 7 | Right to compensation | relevance 0.81

**Answer:**

He should receive **EUR 250**.

**Conditions:**
- For flights of 1,500 kilometres or less, the standard compensation is EUR 250 [Regulation (EC) No 261/2004, Article 7].
- This amount may be reduced by 50% (to EUR 125) if the passenger is offered re-routing to their final destination on an alternative flight whose arrival time does not exceed the scheduled arrival time of the originally booked flight by more than two hours [Regulation (EC) No 261/2004, Article 7]. *(Assuming the customer was not re-routed within this two-hour window, the full EUR 250 applies).*

[Regulation (EC) No 261/2004, Article 7]

---

## q05 (single)

**Question:** The airline wants to pay a customer's compensation in travel vouchers. Is it allowed to?

**Reference:** Only with the passenger's signed agreement; otherwise it must pay in cash, by bank transfer, bank order or cheque.

**Agent's searches and top hit of each:**

- call search({'query': 'compensation in travel vouchers air Regulation 261/2004'})
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 2.2.7 | Scope of Regulation (EC) No 261/2004 in relation to Directive (EU) 2015/2302 (Package Travel Directive) | relevance 0.81

**Answer:**

Yes, but only with the signed agreement of the passenger. Otherwise, it must be paid in cash, by electronic bank transfer, bank orders, or bank cheques.

[Regulation (EC) No 261/2004, Article 7]

---

## q08 (single)

**Question:** A customer's flight reached its destination 3 hours and 15 minutes late. Does he have a right to compensation?

**Reference:** Yes. A delay at arrival of at least 3 hours gives the same right to compensation as a cancellation (unless extraordinary circumstances apply).

**Agent's searches and top hit of each:**

- call search({'query': 'compensation flight delay 3 hours 15 minutes Regulation EC 261 2004'})
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 4.4.7 | ‘Long delays’ at arrival | relevance 0.81

**Answer:**

Yes, the customer has a right to compensation.

**Conditions:**
- The flight reached its final destination 3 hours or more late (3 hours and 15 minutes).
- The air carrier is not able to prove that the long delay was caused by extraordinary circumstances that could not have been avoided even if all reasonable measures had been taken.

**Citations:**
- [Commission Guidelines on Regulation 261/2004 (2024), Section 4.4.7]
- [Commission Guidelines on Regulation 261/2004 (2024), Section 3.3.2]

---

## q13 (single)

**Question:** A customer flew New York to Istanbul on one booking with an EU airline, changing planes in Frankfurt. Is the trip covered by Regulation 261/2004?

**Reference:** No. If both the first departure airport and the final destination are outside the EU, the Regulation does not apply, even with a stopover in the EU.

**Agent's searches and top hit of each:**

- call search({'query': 'flight from third country to third country community carrier Regulation 261/2004 scope'})
- [1] Commission Guidelines on Regulation 261/2004 (2024), Section 2.1.4 | Flights outside the scope of Regulation (EC) No 261/2004 | relevance 0.85

**Answer:**

**No**, the trip is not covered by Regulation 261/2004.

**Conditions:**
Even though the trip involves an EU airline and a connection in an EU airport (Frankfurt), Regulation 261/2004 does not apply to connecting flights under a single booking when both the departure airport (New York) and the final destination airport (Istanbul) are located outside the EU [Commission Guidelines on Regulation 261/2004 (2024), Section 2.1.4]. 

**Citations:**
- [Commission Guidelines on Regulation 261/2004 (2024), Section 2.1.4]

---

## q16 (single)

**Question:** A customer's train arrived 75 minutes late. What minimum compensation can he claim?

**Reference:** 25% of the ticket price (delay of 60 to 119 minutes).

**Agent's searches and top hit of each:**

- call search({'query': 'train delay compensation 75 minutes minimum compensation Regulation (EU) 2021/782'})
- [1] Regulation (EU) 2021/782, Article 19 | Compensation | relevance 0.85

**Answer:**

25% of the ticket price.

**Conditions:**
- The customer must be facing a delay between the places of departure and final destination stated in the ticket or through-ticket.
- The cost of the ticket has not been reimbursed under Article 18.
- For a delay of 60 to 119 minutes, the minimum compensation is 25% of the ticket price [Regulation (EU) 2021/782, Article 19].

---

## q20 (single)

**Question:** A customer took a regular coach service of 180 km that was badly delayed. Does the full EU bus passenger regulation apply?

**Reference:** No. Full rights apply to regular services of 250 km or more; shorter services get only some articles.

**Agent's searches and top hit of each:**

- call search({'query': 'bus passenger regulation scope distance 250 km regular service'})
- [1] Regulation (EU) No 181/2011, Article 2 | Scope | relevance 0.77

**Answer:**

No, the full EU bus passenger regulation does not apply because the scheduled distance is under 250 km. 

### Conditions:
- For regular services with a scheduled distance of **250 km or more**, the **full** Regulation (EU) No 181/2011 applies [Regulation (EU) No 181/2011, Article 2].
- For regular services with a scheduled distance **shorter than 250 km** (such as 180 km), only specific provisions apply (including certain rules on non-discrimination, accident compensation for passengers, disability rights, basic information, and complaint handling), but the general cancellation and delay rights provisions do not apply in full [Regulation (EU) No 181/2011, Article 2].

### Citations:
- [Regulation (EU) No 181/2011, Article 2]

---

## q22 (single)

**Question:** A ferry crossing scheduled to last 3 hours arrived 1 hour and 20 minutes late. What compensation can the passenger request?

**Reference:** 25% of the ticket price (delay of at least 1 hour on a journey of up to 4 hours).

**Agent's searches and top hit of each:**

- call search({'query': 'sea inland waterway passenger rights compensation delay'})
- [1] Regulation (EU) No 1177/2010, Article 18 | Re-routing and reimbursement in the event of cancelled or delayed departures | relevance 0.79

**Answer:**

The passenger can request compensation of **25% of the ticket price**.

### Conditions:
* The scheduled journey lasted up to 4 hours (3 hours), and the arrival delay was at least 1 hour (the passenger arrived 1 hour and 20 minutes late) [Regulation (EU) No 1177/2010, Article 19].
* This compensation is without prejudice to the passenger's right to transport [Regulation (EU) No 1177/2010, Article 19].
* Compensation may not apply if the delay was caused by weather conditions endangering the safe operation of the ship or by unavoidable extraordinary circumstances [Regulation (EU) No 1177/2010, Recital (14)].

### Citations:
* [Regulation (EU) No 1177/2010, Article 19]
* [Regulation (EU) No 1177/2010, Recital (14)]

---

## q24 (single)

**Question:** A passenger had a reservation for his bicycle on a train, but the railway refused to carry it without a valid reason. What is he entitled to?

**Reference:** Re-routing or reimbursement (Article 18), compensation (Article 19) and assistance (Article 20(2)).

**Agent's searches and top hit of each:**

- call search({'query': 'railway bicycle reservation refused carriage entitled'})
- [1] Regulation (EU) 2021/782, Article 6 | Bicycles | relevance 0.74

**Answer:**

Yes, the passenger is entitled to:
- Re-routing or reimbursement in accordance with Article 18,
- Compensation in accordance with Article 19, and
- Assistance in accordance with Article 20(2).

**Conditions:**
- The passenger must have made a valid reservation for the carriage of the bicycle.
- The carriage of the bicycle must have been refused without a duly justified reason.

[Regulation (EU) 2021/782, Article 6]

---
