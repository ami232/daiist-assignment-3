# Grading sheet (eval/human_labels.csv)

Grade each answer BEFORE looking at the judge's verdicts (eval/verdicts.jsonl, eval/results.csv), as the brief asks.

For each id, fill in `eval/human_labels.csv`:

- **correct** = 1 if the answer says the same as the reference answer (or properly says the documents don't cover it when the reference says so), else 0
- **supported** = 1 if every claim in the answer is in the passages shown below it, else 0 (a plain refusal counts as supported)
- **notes** = optional, a few words on why

---

## q01 (single)

**Question:** Our client is buying a company and we need to know if the deal has an EU dimension, so what turnover thresholds does it have to meet under the main test?

**Reference answer:** Combined worldwide turnover of all undertakings concerned above EUR 5,000 million and EU-wide turnover of each of at least two of them above EUR 250 million, unless each achieves more than two-thirds of its EU turnover in one and the same Member State.

**Answer shown to the associate:**

> Under the main test (Article 1(2)), a deal has an EU dimension if it meets three turnover thresholds:
> 1. **Worldwide turnover:** The combined aggregate worldwide turnover of all undertakings concerned is more than €5,000 million [EUMR Art. 1(1)–(3)].
> 2. **EU-wide turnover:** The aggregate EU-wide turnover of each of at least two of the undertakings concerned is more than €250 million [EUMR Art. 1(1)–(3)].
> 3. **Two-thirds rule exception:** The deal does not qualify if each of the undertakings concerned achieves more than two-thirds of its aggregate EU-wide turnover within one and the same Member State [EUMR Art. 1(1)–(3)].

<details><summary>Passages the search returned</summary>

```
[EUMR Art. 1(1)–(3)] (Scope)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 1(1), Art. 1(2), Art. 1(3)
Without prejudice to Article 4(5) and Article 22, this Regulation shall apply to all concentrations with a Community dimension as defined in this Article. A concentration has a Community dimension where: (a) the combined aggregate worldwide turnover of all the undertakings concerned is more than EUR 5000 million; and (b) the aggregate Community-wide turnover of each of at least two of the undertakings concerned is more than EUR 250 million, unless each of the undertakings concerned achieves more than two-thirds of its aggregate Community-wide turnover within one and the same Member State. A concentration that does not meet the thresholds laid down in paragraph 2 has a Community dimension where: (a) the combined aggregate worldwide turnover of all the undertakings concerned is more than EUR 2500 million; (b) in each of at least three Member States, the combined aggregate turnover of all the undertakings concerned is more than EUR 100 million; (c) in each of at least three Member States included for the purpose of point (b), the aggregate turnover of each of at least two of the undertakings concerned is more than EUR 25 million; and (d) the aggregate Community-wide turnover of each of at least two of the undertakings concerned is more than EUR 100 million, unless each of the undertakings concerned achieves more than two-thirds of its aggregate Community-wide turnover within one and the same Member State.

---

[CJN para. 125] (I. THRESHOLDS)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 125
Two sets of thresholds are set out in Article 1 to establish whether the operation has a Community dimension. Article 1(2) establishes three different criteria: The worldwide turnover threshold is intended to measure the overall dimension of the undertakings concerned; the Community turnover threshold seek to determine whether the concentration involves a minimum level of activities in the Community; and the two-thirds rule aims to exclude purely domestic transactions from Community jurisdiction.

---

[CJN para. 124] (I. THRESHOLDS)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 124
A two fold test defines the operations to which the Merger Regulation applies. The first test is that the operation must be a concentration within the meaning of Article 3. The second comprises the turnover thresholds contained in Article 1, designed to identify those operations which have an impact upon the Community and can be deemed to be of ‘Community dimension’. Turnover is used as a proxy for the economic resources being combined in a concentration, and is allocated geographically in order to reflect the geographic distribution of those resources.

---

[CJN para. 127] (I. THRESHOLDS)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 127
The thresholds as such are designed to govern jurisdiction and not to assess the market position of the parties to the concentration nor the impact of the operation. In so doing they include turnover derived from, and thus the resources devoted to, all areas of activity of the parties, and not just those directly involved in the concentration. The thresholds are purely quantitative, since they are only based on turnover calculation instead of market share or other criteria. They pursue the objective to provide a simple and objective mechanism that can be easily handled by the companies involved in a merger in order to determine if their transaction has a Community dimension and is therefore notifiable.

---

[CJN para. 5] (A. INTRODUCTION)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 5
According to Article 1, the Merger Regulation only applies to operations that satisfy two conditions. First, there must be a concentration of two or more undertakings within the meaning of Article 3 of the Merger Regulation. Secondly, the turnover of the undertakings concerned, calculated in accordance with Article 5, must satisfy the thresholds set out in Article 1 of the Regulation. The notion of a concentration (including the particular requirements for joint ventures), as the first condition, is dealt with under Part B; the identification of undertakings concerned and the calculation of their turnover as relevant for the second condition are dealt with under Part C.
```
</details>

---

## q03 (single)

**Question:** The client wants to close as soon as the SPA is signed, can they close the deal before the Commission clears it?

**Reference answer:** No. A concentration with an EU dimension cannot be implemented before notification or until it has been declared compatible (or is deemed compatible under Article 10(6)).

**Answer shown to the associate:**

> No, the client cannot close the deal upon signing the SPA if it is a concentration with a Community dimension (or examined pursuant to Article 4(5)) [EUMR Art. 7(1)]. 
> 
> Under the EU Merger Regulation standstill obligation, such a concentration must not be implemented either before its notification or until it has been declared compatible with the common market by the Commission (via a clearance decision under Articles 6(1)(b), 8(1), or 8(2), or by presumption) [EUMR Art. 7(1)]. 
> 
> **Exception:** The Commission may grant a reasoned request for a derogation from this suspension obligation, which may be subject to conditions and obligations [EUMR Art. 7(3)].

<details><summary>Passages the search returned</summary>

```
[EUMR Art. 7(1)–(2)] (Suspension of concentrations)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 7(1), Art. 7(2)
A concentration with a Community dimension as defined in Article 1, or which is to be examined by the Commission pursuant to Article 4(5), shall not be implemented either before its notification or until it has been declared compatible with the common market pursuant to a decision under Articles 6(1)(b), 8(1) or 8(2), or on the basis of a presumption according to Article 10(6). Paragraph 1 shall not prevent the implementation of a public bid or of a series of transactions in securities including those convertible into other securities admitted to trading on a market such as a stock exchange, by which control within the meaning of Article 3 is acquired from various sellers, provided that: (a) the concentration is notified to the Commission pursuant to Article 4 without delay; and (b) the acquirer does not exercise the voting rights attached to the securities in question or does so only to maintain the full value of its investments based on a derogation granted by the Commission under paragraph 3.

---

[EUMR Recital 34] (Recitals)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Recital 34
To ensure effective control, undertakings should be obliged to give prior notification of concentrations with a Community dimension following the conclusion of the agreement, the announcement of the public bid or the acquisition of a controlling interest. Notification should also be possible where the undertakings concerned satisfy the Commission of their intention to enter into an agreement for a proposed concentration and demonstrate to the Commission that their plan for that proposed concentration is sufficiently concrete, for example on the basis of an agreement in principle, a memorandum of understanding, or a letter of intent signed by all undertakings concerned, or, in the case of a public bid, where they have publicly announced an intention to make such a bid, provided that the intended agreement or bid would result in a concentration with a Community dimension. The implementation of concentrations should be suspended until a final decision of the Commission has been taken. However, it should be possible to derogate from this suspension at the request of the undertakings concerned, where appropriate. In deciding whether or not to grant a derogation, the Commission should take account of all pertinent factors, such as the nature and gravity of damage to the undertakings concerned or to third parties, and the threat to competition posed by the concentration. In the interest of legal certainty, the validity of transactions must nevertheless be protected as much as necessary.

---

[EUMR Art. 7(3)–(4)] (Suspension of concentrations)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 7(3), Art. 7(4)
The Commission may, on request, grant a derogation from the obligations imposed in paragraphs 1 or 2. The request to grant a derogation must be reasoned. In deciding on the request, the Commission shall take into account inter alia the effects of the suspension on one or more undertakings concerned by the concentration or on a third party and the threat to competition posed by the concentration. Such a derogation may be made subject to conditions and obligations in order to ensure conditions of effective competition. A derogation may be applied for and granted at any time, be it before notification or after the transaction. The validity of any transaction carried out in contravention of paragraph 1 shall be dependent on a decision pursuant to Article 6(1)(b) or Article 8(1), (2) or (3) or on a presumption pursuant to Article 10(6). This Article shall, however, have no effect on the validity of transactions in securities including those convertible into other securities admitted to trading on a market such as a stock exchange, unless the buyer and seller knew or ought to have known that the transaction was carried out in contravention of paragraph 1.

---

[EUMR Art. 4(1)] (Prior notification of concentrations and pre-notification referral at the request of the notifying parties)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 4(1)
Concentrations with a Community dimension defined in this Regulation shall be notified to the Commission prior to their implementation and following the conclusion of the agreement, the announcement of the public bid, or the acquisition of a controlling interest. Notification may also be made where the undertakings concerned demonstrate to the Commission a good faith intention to conclude an agreement or, in the case of a public bid, where they have publicly announced an intention to make such a bid, provided that the intended agreement or bid would result in a concentration with a Community dimension. For the purposes of this Regulation, the term "notified concentration" shall also cover intended concentrations notified pursuant to the second subparagraph. For the purposes of paragraphs 4 and 5 of this Article, the term "concentration" includes intended concentrations within the meaning of the second subparagraph.

---

[EUMR Art. 6(1)] (Examination of the notification and initiation of proceedings)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 6(1)
The Commission shall examine the notification as soon as it is received. (a) Where it concludes that the concentration notified does not fall within the scope of this Regulation, it shall record that finding by means of a decision. (b) Where it finds that the concentration notified, although falling within the scope of this Regulation, does not raise serious doubts as to its compatibility with the common market, it shall decide not to oppose it and shall declare that it is compatible with the common market. A decision declaring a concentration compatible shall be deemed to cover restrictions directly related and necessary to the implementation of the concentration. (c) Without prejudice to paragraph 2, where the Commission finds that the concentration notified falls within the scope of this Regulation and raises serious doubts as to its compatibility with the common market, it shall decide to initiate proceedings. Without prejudice to Article 9, such proceedings shall be closed by means of a decision as provided for in Article 8(1) to (4), unless the undertakings concerned have demonstrated to the satisfaction of the Commission that they have abandoned the concentration.
```
</details>

---

## q05 (single)

**Question:** Once we notify, how long does the Commission have to take its Phase I decision?

**Reference answer:** 25 working days from the working day after receipt of a complete notification, extended to 35 working days if a Member State requests a referral or the parties offer commitments.

**Answer shown to the associate:**

> The Commission has **25 working days** from the working day following receipt of the complete notification to take its Phase I decision [EUMR Art. 10(1)–(2)]. 
> 
> This deadline is extended in the following cases:
> * To **35 working days** if the undertakings concerned offer commitments under Article 6(2), or if the Commission receives a referral request from a Member State under Article 9(2) [EUMR Art. 10(1)–(2), RN para. 78].

<details><summary>Passages the search returned</summary>

```
[RN para. 78] (1. Phase I)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 78
Parties can submit proposals for commitments to the Commission on an informal basis, even before notification. Parties have to submit commitments within not more than 20 working days from the date of the receipt of the notification. The Commission informs the parties about its serious doubts in due time before that deadline. Where the parties submit commitments, the deadline for the Commission's decision pursuant to Article 6(1) of the Merger Regulation is extended from 25 to 35 working days.

---

[RN para. 89] (2. Phase II)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 89
The question whether or not submitting remedies will extend the deadline for the Commission to take a final decision depends on the time in the procedure when the commitments are submitted. Where the parties submit commitments within less than 55 working days after the initiation of proceedings, the Commission has to take a final decision within not more than 90 working days of the date of initiation of proceedings. Where the parties submit commitments on working day 55 or afterwards (even after working day 65, if those commitments should be acceptable due to exceptional circumstances as described above in paragraph 88), the period for the Commission to take a final decision is increased to 105 working days according to Article 10(3), subparagraph 2. Where the parties submit commitments within less than 55 working days, but submit a modified version on day 55 or thereafter, the period to take a final decision will also be extended to 105 working days.

---

[EUMR Art. 10(3)] (Time limits for initiating proceedings and for decisions)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 10(3)
Without prejudice to Article 8(7), decisions pursuant to Article 8(1) to (3) concerning notified concentrations shall be taken within not more than 90 working days of the date on which the proceedings are initiated. That period shall be increased to 105 working days where the undertakings concerned offer commitments pursuant to Article 8(2), second subparagraph, with a view to rendering the concentration compatible with the common market, unless these commitments have been offered less than 55 working days after the initiation of proceedings. The periods set by the first subparagraph shall likewise be extended if the notifying parties make a request to that effect not later than 15 working days after the initiation of proceedings pursuant to Article 6(1)(c). The notifying parties may make only one such request. Likewise, at any time following the initiation of proceedings, the periods set by the first subparagraph may be extended by the Commission with the agreement of the notifying parties. The total duration of any extension or extensions effected pursuant to this subparagraph shall not exceed 20 working days.

---

[EUMR Art. 10(1)–(2)] (Time limits for initiating proceedings and for decisions)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 10(1), Art. 10(2)
Without prejudice to Article 6(4), the decisions referred to in Article 6(1) shall be taken within 25 working days at most. That period shall begin on the working day following that of the receipt of a notification or, if the information to be supplied with the notification is incomplete, on the working day following that of the receipt of the complete information. That period shall be increased to 35 working days where the Commission receives a request from a Member State in accordance with Article 9(2)or where, the undertakings concerned offer commitments pursuant to Article 6(2) with a view to rendering the concentration compatible with the common market. Decisions pursuant to Article 8(1) or (2) concerning notified concentrations shall be taken as soon as it appears that the serious doubts referred to in Article 6(1)(c) have been removed, particularly as a result of modifications made by the undertakings concerned, and at the latest by the time limit laid down in paragraph 3.

---

[RN para. 90] (2. Phase II)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 90
The Commission is available to discuss suitable commitments well in advance of the end of the 65 working day period. The parties are encouraged to submit draft proposals dealing with both substantive and implementation aspects which are necessary to ensure that the commitments are fully workable. If the parties are of the opinion that more time is needed for the investigation of the competition concerns and for the corresponding design of appropriate commitments, they may also suggest to the Commission to extend the final deadline under Article 10(3), subparagraph 1. Such a request will have to be made before the end of the 65 working day period. Indeed, the Commission will normally not extend the period for adopting a final decision according to Article 10(3), subparagraph 1 where the request for extension is presented after the deadline for submitting remedies foreseen in the Implementing Regulation, i.e. after working day 65.
```
</details>

---

## q06 (single)

**Question:** If the Commission opens a Phase II investigation, how long can it last at most?

**Reference answer:** 90 working days from the opening of proceedings, increased to 105 working days if commitments are offered (unless offered less than 55 working days after the opening), and it can be extended further at the request of the parties or with their agreement.

**Answer shown to the associate:**

> A Phase II investigation typically lasts at most **90 working days** from the initiation of proceedings [EUMR Art. 10(3)]. 
> 
> However, this period can be extended:
> * To **105 working days** if commitments are offered on or after working day 55, or if the parties request an extension of up to 15 working days within 15 working days of the initiation of proceedings [EUMR Art. 10(3)].
> * By an additional **up to 20 working days** if agreed between the Commission and the notifying parties at any time following the initiation of proceedings [EUMR Art. 10(3)].

<details><summary>Passages the search returned</summary>

```
[RN para. 90] (2. Phase II)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 90
The Commission is available to discuss suitable commitments well in advance of the end of the 65 working day period. The parties are encouraged to submit draft proposals dealing with both substantive and implementation aspects which are necessary to ensure that the commitments are fully workable. If the parties are of the opinion that more time is needed for the investigation of the competition concerns and for the corresponding design of appropriate commitments, they may also suggest to the Commission to extend the final deadline under Article 10(3), subparagraph 1. Such a request will have to be made before the end of the 65 working day period. Indeed, the Commission will normally not extend the period for adopting a final decision according to Article 10(3), subparagraph 1 where the request for extension is presented after the deadline for submitting remedies foreseen in the Implementing Regulation, i.e. after working day 65.

---

[RN para. 89] (2. Phase II)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 89
The question whether or not submitting remedies will extend the deadline for the Commission to take a final decision depends on the time in the procedure when the commitments are submitted. Where the parties submit commitments within less than 55 working days after the initiation of proceedings, the Commission has to take a final decision within not more than 90 working days of the date of initiation of proceedings. Where the parties submit commitments on working day 55 or afterwards (even after working day 65, if those commitments should be acceptable due to exceptional circumstances as described above in paragraph 88), the period for the Commission to take a final decision is increased to 105 working days according to Article 10(3), subparagraph 2. Where the parties submit commitments within less than 55 working days, but submit a modified version on day 55 or thereafter, the period to take a final decision will also be extended to 105 working days.

---

[EUMR Art. 10(3)] (Time limits for initiating proceedings and for decisions)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 10(3)
Without prejudice to Article 8(7), decisions pursuant to Article 8(1) to (3) concerning notified concentrations shall be taken within not more than 90 working days of the date on which the proceedings are initiated. That period shall be increased to 105 working days where the undertakings concerned offer commitments pursuant to Article 8(2), second subparagraph, with a view to rendering the concentration compatible with the common market, unless these commitments have been offered less than 55 working days after the initiation of proceedings. The periods set by the first subparagraph shall likewise be extended if the notifying parties make a request to that effect not later than 15 working days after the initiation of proceedings pursuant to Article 6(1)(c). The notifying parties may make only one such request. Likewise, at any time following the initiation of proceedings, the periods set by the first subparagraph may be extended by the Commission with the agreement of the notifying parties. The total duration of any extension or extensions effected pursuant to this subparagraph shall not exceed 20 working days.

---

[RN para. 78] (1. Phase I)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 78
Parties can submit proposals for commitments to the Commission on an informal basis, even before notification. Parties have to submit commitments within not more than 20 working days from the date of the receipt of the notification. The Commission informs the parties about its serious doubts in due time before that deadline. Where the parties submit commitments, the deadline for the Commission's decision pursuant to Article 6(1) of the Merger Regulation is extended from 25 to 35 working days.

---

[RN para. 94] (2. Phase II)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 94
The Merger Regulation does not impose any obligation on the Commission to accept commitments after the legal deadline for remedies, unless the Commission voluntarily undertakes to assess commitments in specific circumstances. In view of this, where parties subsequently modify the proposed commitments after the deadline of 65 working days, the Commission will only accept these modified commitments where it can clearly determine — on the basis of its assessment of information already received in the course of the investigation, including the results of prior market testing, and without the need for any other market test — that such commitments, once implemented, fully and unambiguously resolve the competition concerns identified and where there is sufficient time to allow for an adequate assessment by the Commission and for proper consultation with Member States. The Commission will normally reject modified commitments which do not fulfil those conditions.
```
</details>

---

## q08 (single)

**Question:** What happens if the Commission doesn't take a decision within the legal deadlines?

**Reference answer:** The concentration is deemed to have been declared compatible with the common market (without prejudice to Article 9).

**Answer shown to the associate:**

> If the Commission fails to take a decision within the applicable legal deadlines (Phase I or Phase II), the concentration is **deemed to have been declared compatible with the common market** [EUMR Art. 10(6)]. 
> 
> This rule is subject to Article 9 (referrals to Member States) [EUMR Art. 10(6)].

<details><summary>Passages the search returned</summary>

```
[RN para. 78] (1. Phase I)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 78
Parties can submit proposals for commitments to the Commission on an informal basis, even before notification. Parties have to submit commitments within not more than 20 working days from the date of the receipt of the notification. The Commission informs the parties about its serious doubts in due time before that deadline. Where the parties submit commitments, the deadline for the Commission's decision pursuant to Article 6(1) of the Merger Regulation is extended from 25 to 35 working days.

---

[RN para. 89] (2. Phase II)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 89
The question whether or not submitting remedies will extend the deadline for the Commission to take a final decision depends on the time in the procedure when the commitments are submitted. Where the parties submit commitments within less than 55 working days after the initiation of proceedings, the Commission has to take a final decision within not more than 90 working days of the date of initiation of proceedings. Where the parties submit commitments on working day 55 or afterwards (even after working day 65, if those commitments should be acceptable due to exceptional circumstances as described above in paragraph 88), the period for the Commission to take a final decision is increased to 105 working days according to Article 10(3), subparagraph 2. Where the parties submit commitments within less than 55 working days, but submit a modified version on day 55 or thereafter, the period to take a final decision will also be extended to 105 working days.

---

[EUMR Art. 10(1)–(2)] (Time limits for initiating proceedings and for decisions)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 10(1), Art. 10(2)
Without prejudice to Article 6(4), the decisions referred to in Article 6(1) shall be taken within 25 working days at most. That period shall begin on the working day following that of the receipt of a notification or, if the information to be supplied with the notification is incomplete, on the working day following that of the receipt of the complete information. That period shall be increased to 35 working days where the Commission receives a request from a Member State in accordance with Article 9(2)or where, the undertakings concerned offer commitments pursuant to Article 6(2) with a view to rendering the concentration compatible with the common market. Decisions pursuant to Article 8(1) or (2) concerning notified concentrations shall be taken as soon as it appears that the serious doubts referred to in Article 6(1)(c) have been removed, particularly as a result of modifications made by the undertakings concerned, and at the latest by the time limit laid down in paragraph 3.

---

[RN para. 90] (2. Phase II)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 90
The Commission is available to discuss suitable commitments well in advance of the end of the 65 working day period. The parties are encouraged to submit draft proposals dealing with both substantive and implementation aspects which are necessary to ensure that the commitments are fully workable. If the parties are of the opinion that more time is needed for the investigation of the competition concerns and for the corresponding design of appropriate commitments, they may also suggest to the Commission to extend the final deadline under Article 10(3), subparagraph 1. Such a request will have to be made before the end of the 65 working day period. Indeed, the Commission will normally not extend the period for adopting a final decision according to Article 10(3), subparagraph 1 where the request for extension is presented after the deadline for submitting remedies foreseen in the Implementing Regulation, i.e. after working day 65.

---

[EUMR Art. 10(3)] (Time limits for initiating proceedings and for decisions)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 10(3)
Without prejudice to Article 8(7), decisions pursuant to Article 8(1) to (3) concerning notified concentrations shall be taken within not more than 90 working days of the date on which the proceedings are initiated. That period shall be increased to 105 working days where the undertakings concerned offer commitments pursuant to Article 8(2), second subparagraph, with a view to rendering the concentration compatible with the common market, unless these commitments have been offered less than 55 working days after the initiation of proceedings. The periods set by the first subparagraph shall likewise be extended if the notifying parties make a request to that effect not later than 15 working days after the initiation of proceedings pursuant to Article 6(1)(c). The notifying parties may make only one such request. Likewise, at any time following the initiation of proceedings, the periods set by the first subparagraph may be extended by the Commission with the agreement of the notifying parties. The total duration of any extension or extensions effected pursuant to this subparagraph shall not exceed 20 working days.

[EUMR Art. 10(6)] (Time limits for initiating proceedings and for decisions)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 10(6)
Where the Commission has not taken a decision in accordance with Article 6(1)(b), (c), 8(1), (2) or (3) within the time limits set in paragraphs 1 and 3 respectively, the concentration shall be deemed to have been declared compatible with the common market, without prejudice to Article 9.

---

[EUMR Art. 6(1)] (Examination of the notification and initiation of proceedings)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 6(1)
The Commission shall examine the notification as soon as it is received. (a) Where it concludes that the concentration notified does not fall within the scope of this Regulation, it shall record that finding by means of a decision. (b) Where it finds that the concentration notified, although falling within the scope of this Regulation, does not raise serious doubts as to its compatibility with the common market, it shall decide not to oppose it and shall declare that it is compatible with the common market. A decision declaring a concentration compatible shall be deemed to cover restrictions directly related and necessary to the i
```
</details>

---

## q10 (single)

**Question:** Our client is a franchisor, does the franchise agreement give it control over the franchisee's business?

**Reference answer:** Normally no, because the franchisee usually exploits the entrepreneurial resources on its own account.

**Answer shown to the associate:**

> No, franchising agreements as such do not normally confer control over the franchisee's business on the franchisor [CJN para. 19]. 
> 
> The franchisee usually exploits the entrepreneurial resources on its own account, even if essential parts of the assets may belong to the franchisor [CJN para. 19].

<details><summary>Passages the search returned</summary>

```
[CJN para. 19] (1.2. Means of control)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 19
In line with these considerations, franchising agreements as such do not normally confer control over the franchisee's business on the franchisor. The franchisee usually exploits the entrepreneurial resources on its own account even if essential parts of the assets may belong to the franchisor. Furthermore, purely financial agreements, such as sale-and-lease-back transactions with arrangements for a buyback of the assets at the end of the term, do not normally constitute a concentration as they do not change control over the management and the resources.

---

[CJN para. 18] (1.2. Means of control)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 18
Control can also be acquired on a contractual basis. In order to confer control, the contract must lead to a similar control of the management and the resources of the other undertaking as in the case of acquisition of shares or assets. In addition to transferring control over the management and the resources, such contracts must be characterised by a very long duration (ordinarily without a possibility of early termination for the party granting the contractual rights). Only such contracts can result in a structural change in the market. Examples of such contracts are organisational contracts under national company law or other types of contracts, e.g. in the form of agreements for the lease of the business, giving the acquirer control over the management and the resources despite the fact that property rights or shares are not transferred. In this respect, Article 3(2)(a) specifies that control may also be constituted by a right to use the assets of an undertaking. Such contracts may also lead to a situation of joint control if both the owner of the assets as well as the undertaking controlling the management enjoy veto rights over strategic business decisions.

---

[CJN para. 70] (3.2. Veto rights)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 70
The business plan normally provides details of the aims of a company together with the measures to be taken in order to achieve those aims. A veto right over this type of business plan may be sufficient to confer joint control even in the absence of any other veto right. In contrast, where the business plan contains merely general declarations concerning the business aims of the joint venture, the existence of a veto right will be only one element in the general assessment of joint control but will not, on its own, be sufficient to confer joint control.

---

[CJN para. 63] (3. Joint control)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 63
As in the case of sole control, the acquisition of joint control can also be established on a de jure or de facto basis. There is joint control if the shareholders (the parent companies) must reach agreement on major decisions concerning the controlled undertaking (the joint venture).

---

[CJN para. 64] (3.1. Equality in voting rights or appointment to decision-making bodies)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 64
The clearest form of joint control exists where there are only two parent companies which share equally the voting rights in the joint venture. In this case, it is not necessary for a formal agreement to exist between them. However, where there is a formal agreement, it must be consistent with the principle of equality between the parent companies, by laying down, for example, that each is entitled to the same number of representatives in the management bodies and that none of the members has a casting vote. Equality may also be achieved where both parent companies have the right to appoint an equal number of members to the decision-making bodies of the joint venture.
```
</details>

---

## q11 (single)

**Question:** Our client is a minority shareholder in a joint venture, which veto rights would give it joint control?

**Reference answer:** Vetoes over strategic decisions such as the budget, the business plan, major investments or the appointment of senior management.

**Answer shown to the associate:**

> A minority shareholder acquires joint control if it holds veto rights over decisions essential for the strategic commercial behaviour of the joint venture [CJN para. 65]. 
> 
> Typically, these include decisions on:
> * The budget [CJN para. 67]
> * The business plan [CJN para. 67]
> * Major investments [CJN para. 67] (depending on the investment level and the market) [CJN para. 71]
> * The appointment of senior management [CJN para. 67]
> 
> Having all these rights is not required; one or some may suffice depending on their importance to the specific business [CJN para. 68]. 
> 
> In contrast, standard minority protection rights—such as vetoes protecting investor financial interests (e.g., changes to the statute, capital increases/decreases, liquidation, or preventing the sale or winding-up)—do not confer joint control [CJN para. 66].

<details><summary>Passages the search returned</summary>

```
[CJN para. 65] (3.2. Veto rights)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 65
Joint control may exist even where there is no equality between the two parent companies in votes or in representation in decision-making bodies or where there are more than two parent companies. This is the case where minority shareholders have additional rights which allow them to veto decisions which are essential for the strategic commercial behaviour of the joint venture. These veto rights may be set out in the statute of the joint venture or conferred by agreement between its parent companies. The veto rights themselves may operate by means of a specific quorum required for decisions taken at the shareholders' meeting or by the board of directors to the extent that the parent companies are represented on this board. It is also possible that strategic decisions are subject to approval by a body, e.g. supervisory board, where the minority shareholders are represented and form part of the quorum needed for such decisions.

---

[CJN para. 66] (3.2. Veto rights)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 66
These veto rights must be related to strategic decisions on the business policy of the joint venture. They must go beyond the veto rights normally accorded to minority shareholders in order to protect their financial interests as investors in the joint venture. This normal protection of the rights of minority shareholders is related to decisions on the essence of the joint venture, such as changes in the statute, an increase or decrease in the capital or liquidation. A veto right, for example, which prevents the sale or winding-up of the joint venture does not confer joint control on the minority shareholder concerned.

---

[CJN para. 68] (3.2. Veto rights)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 68
In order to acquire joint control, it is not necessary for a minority shareholder to have all the veto rights mentioned above. It may be sufficient that only some, or even one such right, exists. Whether or not this is the case depends upon the precise content of the veto right itself and also the importance of this right in the context of the specific business of the joint venture.

---

[CJN para. 67] (3.2. Veto rights)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 67
In contrast, veto rights which confer joint control typically include decisions on issues such as the budget, the business plan, major investments or the appointment of senior management. The acquisition of joint control, however, does not require that the acquirer has the power to exercise decisive influence on the day-to-day running of an undertaking. The crucial element is that the veto rights are sufficient to enable the parent companies to exercise such influence in relation to the strategic business behaviour of the joint venture. Moreover, it is not necessary to establish that an acquirer of joint control of the joint venture will actually make use of its decisive influence. The possibility of exercising such influence and, hence, the mere existence of the veto rights, is sufficient.

---

[CJN para. 71] (3.2. Veto rights)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 71
In the case of a veto right on investments, the importance of this right depends, first, on the level of investments which are subject to the approval of the parent companies and, secondly, on the extent to which investments constitute an essential feature of the market in which the joint venture is active. In relation to the first criterion, where the level of investments necessitating approval of the parent companies is extremely high, this veto right may be closer to the normal protection of the interests of a minority shareholder than to a right conferring a power of co-determination over the commercial policy of the joint venture. With regard to the second, the investment policy of an undertaking is normally an important element in assessing whether or not there is joint control. However, there may be some markets where investment does not play a significant role in the market behaviour of an undertaking.
```
</details>

---

## q13 (single)

**Question:** What does a joint venture need to have to count as full-function?

**Reference answer:** It must operate on a market with a management dedicated to its day-to-day operations and access to sufficient resources (finance, staff and tangible and intangible assets) to conduct its business on a lasting basis.

**Answer shown to the associate:**

> To be full-function, a joint venture must operate on a lasting basis as an autonomous economic entity [CJN para. 92]. 
> 
> The key requirements are:
> * **Sufficient resources:** It needs dedicated management for day-to-day operations and access to sufficient resources (finance, staff, and tangible/intangible assets) [CJN para. 94].
> * **Beyond a single function:** It cannot be limited to just one specific function for its parents (such as solely R&D, production, or acting merely as a sales agency) without its own market presence [CJN para. 95].
> * **Market presence and independence:** It must perform functions normally carried out by undertakings on the same market [CJN para. 94]. While it need not be autonomous in its strategic decisions, it must be operationally autonomous [CJN para. 93].
> * **Third-party sales:** If it sells to its parent companies on a lasting basis, achieving over 50% of its turnover with third parties typically indicates full-functionality; below 50%, a case-by-case analysis is required (with 20% generally serving as an indicative threshold if dealings are strictly at arm's length) [CJN para. 98].

<details><summary>Passages the search returned</summary>

```
[CJN para. 94] (1. Sufficient resources to operate independently on a market)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 94
Full function character essentially means that a joint venture must operate on a market, performing the functions normally carried out by undertakings operating on the same market. In order to do so the joint venture must have a management dedicated to its day-to-day operations and access to sufficient resources including finance, staff, and assets (tangible and intangible) in order to conduct on a lasting basis its business activities within the area provided for in the joint-venture agreement. The personnel do not necessarily need to be employed by the joint venture itself. If it is standard practice in the industry where the joint venture is operating, it may be sufficient if third parties envisage the staffing under an operational agreement or if staff is assigned by an interim employment agency. The secondment of personnel by the parent companies may also be sufficient if this is done either only for a start-up period or if the joint venture deals with the parent companies in the same way as with third parties. The latter case requires that the joint venture deals with the parents at arm's length on the basis of normal commercial conditions and that the joint venture is also free to recruit its own employees or to obtain staff via third parties.

---

[CJN para. 92] (IV. JOINT VENTURES — THE CONCEPT OF FULL-FUNCTIONALITY)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 92
Article 3(4) provides in addition that the creation of a joint venture performing on a lasting basis all the functions of an autonomous economic entity (so called full-function joint ventures) shall constitute a concentration within the meaning of the Merger Regulation. The full-functionality criterion therefore delineates the application of the Merger Regulation for the creation of joint ventures by the parties, irrespective of whether such a joint venture is created as a ‘greenfield operation’ or whether the parties contribute assets to the joint venture which they previously owned individually. In these circumstances, the joint venture must fulfil the full-functionality criterion in order to constitute a concentration.

---

[CJN para. 93] (IV. JOINT VENTURES — THE CONCEPT OF FULL-FUNCTIONALITY)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 93
The fact that a joint venture may be a full-function undertaking and therefore economically autonomous from an operational viewpoint does not mean that it enjoys autonomy as regards the adoption of its strategic decisions. Otherwise, a jointly controlled undertaking could never be considered a full-function joint venture and therefore the condition laid down in Article 3(4) would never be complied with. It is therefore sufficient for the criterion of full-functionality if the joint venture is autonomous in operational respect.

---

[CJN para. 95] (2. Activities beyond one specific function for the parents)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 95
A joint venture is not full-function if it only takes over one specific function within the parent companies' business activities without its own access to or presence on the market. This is the case, for example, for joint ventures limited to R&D or production. Such joint ventures are auxiliary to their parent companies' business activities. This is also the case where a joint venture is essentially limited to the distribution or sales of its parent companies' products and, therefore, acts principally as a sales agency. However, the fact that a joint venture makes use of the distribution network or outlet of one or more of its parent companies normally will not disqualify it as ‘full-function’ as long as the parent companies are acting only as agents of the joint venture.

---

[CJN para. 98] (3. Sale/purchase relations with the parents)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 98
Where sales from the joint venture to the parent companies are intended to be made on a lasting basis, the essential question is whether, regardless of these sales, the joint venture is geared to play an active role on the market and can be considered economically autonomous from an operational viewpoint. In this respect the relative proportion of sales made to its parents compared with the total production of the joint venture is an important factor. Due to the particularities of each individual case, it is impossible to define a specific turnover ratio which distinguishes full-function from other joint ventures. If the joint venture achieves more than 50 % of its turnover with third parties, this will typically be an indication of full-functionality. Below this indicative threshold, a case-by-case analysis is required, whereby, for the finding of operational autonomy, the relationship between the joint venture and its parents must be truly commercial in character. For this purpose, it is to be demonstrated that the joint venture will supply its goods or services to the purchaser who values them most and will pay most and that the joint venture will also deal with its parents' companies at arm's length on the basis of normal commercial conditions. Under these circumstances, i.e. if the joint venture will treat its parent companies in the same commercial way as third parties, it may be sufficient that at least 20 % of the joint venture's predicted sales will go to third parties. However, the greater the proportion of sales likely to be made to the parents, the greater will be the need for clear evidence of the commercial character of the relationship.
```
</details>

---

## q15 (single)

**Question:** Which date do we have to look at to know if the Commission has jurisdiction over the deal?

**Reference answer:** The date of the binding legal agreement, the announcement of a public bid, the acquisition of a controlling interest or the first notification (to the Commission or a Member State), whichever is earlier.

**Answer shown to the associate:**

> Answer withheld by the citation guardrail (citations not found in the search results: CJN para. 155, 156). The Deal Desk documents do not cover this. Please check with counsel or rephrase the question.

<details><summary>Passages the search returned</summary>

```
[CJN para. 156] (III. RELEVANT DATE FOR ESTABLISHING JURISDICTION)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 156
The relevant date for establishing Community jurisdiction over a concentration is therefore the date of the conclusion of the binding legal agreement, the announcement of a public bid or the acquisition of a controlling interest or the date of the first notification, whichever date is earlier. Regarding the date of notification, a notification to either the Commission or to a Member State authority is relevant. The relevant date needs in particular to be considered for the question whether acquisitions or divestitures which occur after the period covered by the relevant account, but before the relevant date, require adaptations to those accounts according to the principles set out in paragraphs 172 and 173.

---

[CJN para. 154] (III. RELEVANT DATE FOR ESTABLISHING JURISDICTION)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 154
The legal situation for establishing the Commission's jurisdiction has been changed under the recast Merger Regulation. Under the former Merger Regulation, the relevant date was the triggering event for a notification according to Article 4(1) of this Regulation — the conclusion of a final agreement or the announcement of a public bid or the acquisition of a controlling interest — or, at the latest, the time when the parties were obliged to notify (i.e. one week after a triggering event for a notification).

---

[CJN para. 155] (III. RELEVANT DATE FOR ESTABLISHING JURISDICTION)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 155
Under the recast Merger Regulation, there is no longer an obligation for the parties to notify within a certain time-frame (provided the parties do not implement the planned concentration before notification). Moreover, according to Article 4(1) second subparagraph, the undertakings concerned can already notify the transaction on the basis of a good faith intention to conclude an agreement or, in the case of a public bid, where they have publicly announced an intention to make such a bid. At the time of the notification at the latest, the Commission — as well as national competition authorities — must be able to determine their jurisdiction. Article 4(1) subparagraph 1 of the Merger Regulation provides, generally, that concentrations shall be notified following the conclusion of the agreement, the announcement of the public bid, or the acquisition of a controlling interest. The dates of these events are therefore still decisive under the recast Merger Regulation in order to determine the relevant date for establishing jurisdiction, if a notification does not occur before such events on the basis of a good faith intention or an announced intention.

---

[CJN para. 28] (1.4. Change of control on a lasting basis)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 28
Article 3(1) of the Merger Regulation defines the concept of a concentration in such a manner as to cover operations only if they bring about a lasting change in the control of the undertakings concerned and, as recital 20 adds, in the structure of the market. The Merger Regulation therefore does not deal with transactions resulting only in a temporary change of control. However, a change of control on a lasting basis is not excluded by the fact that the underlying agreements are entered into for a definite period of time, provided those agreements are renewable. A concentration may arise even in cases in which agreements envisage a definite end-date, if the period envisaged is sufficiently long to lead to a lasting change in the control of the undertakings concerned.

---

[CJN para. 31] (1.4. Change of control on a lasting basis)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 31
The Commission considers that the first transaction does not constitute a concentration, and examines the acquisitions of control by the ultimate acquirers, provided a number of conditions are met: First, the subsequent break-up must be agreed between the different purchasers in a legally binding way. Second, there must not be any uncertainty that the second step, the division of the acquired assets, will take place within a short time period after the first acquisition. The Commission considers that normally the maximum time-frame for the division of the assets should be one year.
```
</details>

---

## q16 (single)

**Question:** The deal is signed in February and the audited accounts for last year aren't ready yet, which figures do we use for the turnover?

**Reference answer:** The figures for the previous year; the Commission may exceptionally use the final draft figures if there is a major divergence due to significant and permanent changes.

**Answer shown to the associate:**

> The figures to be taken into account are those relating to the previous year [CJN para. 170]. 
> 
> The Commission is reluctant to rely on provisional or management accounts except in exceptional circumstances [CJN para. 170]. However, provisional figures for the most recent year may be used if there is a major divergence between the years due to significant, permanent changes, particularly if the final draft figures have been approved by the board of management [CJN para. 170]. Additionally, adjustments must still be made for post-account acquisitions, divestments, or closures [CJN para. 172].

<details><summary>Passages the search returned</summary>

```
[CJN para. 173] (4.2. Adjustments after the date of the last audited accounts)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 173
Second, an adjustment may also be necessary for acquisitions, divestments or closure of part of the business which have taken place during the financial year for which the audited accounts are drawn up. If acquisitions, divestments or closure of part of the business within this period are made, the changes in the economic resources may only partly be reflected in the audited accounts of the undertaking concerned. As the turnover of the businesses acquired may be included in the accounts only from the time of their acquisition, this may not reflect the full annual turnover of the acquired business. Conversely, the turnover of the businesses divested or closed may still be included in the audited accounts up to the point in time of their actual divestment or closure. In these cases, adjustments have to be made to remove the turnover generated by the divested or closed businesses from the audited accounts until the time of de-consolidation and to add the turnover which the acquired businesses have generated in the year until the time they have been consolidated in the accounts. As a result, the turnover of the businesses divested or closed must be excluded in full and the full annual turnover of the businesses acquired must be included.

---

[CJN para. 205] (VI. CONVERSION OF TURNOVER INTO EURO)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 205
When a company has sales in a range of currencies, the procedure is no different. The total turnover given in the consolidated audited accounts and in that company's reporting currency is converted into euros at the yearly average rate. Local currency sales should not be converted directly into euros since these figures are not from the consolidated audited accounts of the company.

---

[CJN para. 220] (2.3. Financial holding companies)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 220
Turnover calculation for financial holding companies as described above may in practice prove onerous. Therefore a strict and detailed application of this method will be necessary only in cases where it seems that the turnover of a financial holding company is likely to be close to the Merger Regulation thresholds; in other cases it may well be obvious that the turnover is far from the thresholds of the Merger Regulation, and therefore the published accounts are adequate for the establishment of jurisdiction.

---

[CJN para. 158] (1. The concept of turnover)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 158
In the case of services, the method of calculating turnover in general does not differ from that used in the case of products: the Commission takes into consideration the total amount of sales. However, the calculation of the amounts derived from the provision of services may be more complex as this depends on the exact service provided and the underlying legal and economic arrangements in the sector in question. Where one undertaking provides the entire service directly to the customer, the turnover of the undertaking concerned consists of the total amount of sales for the provision of services in the last financial year.

---

[CJN para. 172] (4.2. Adjustments after the date of the last audited accounts)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 172
change is not taken into account, unless the sale is a pre-condition for the notified operation. Conversely, the turnover of those businesses whose acquisition has been closed subsequent to the preparation of the most recent audited accounts, but before the relevant date for establishing jurisdiction, must be added to a company's turnover for notification purposes.

[CJN para. 173] (4.2. Adjustments after the date of the last audited accounts)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 173
Second, an adjustment may also be necessary for acquisitions, divestments or closure of part of the business which have taken place during the financial year for which the audited accounts are drawn up. If acquisitions, divestments or closure of part of the business within this period are made, the changes in the economic resources may only partly be reflected in the audited accounts of the undertaking concerned. As the turnover of the businesses acquired may be included in the accounts only from the time of their acquisition, this may not reflect the full annual turnover of the acquired business. Conversely, the turnover of the businesses divested or closed may still be included in the audited accounts up to the point in time of their actual divestment or closure. In these cases, adjustments have to be made to remove the turnover generated by the divested or closed businesses from the audited accounts until the time of de-consolidation and to add the turnover which the acquired businesses have generated in the year until the time they have been consolidated in the accounts. As a result, the turnover of the businesses divested or closed must be excluded in full and the full annual turnover of the businesses acquired must be included.

---

[CJN para. 172] (4.2. Adjustments after the date of the last audited accounts)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 172
change is not taken into account, unless the sale is a pre-condition for the notified operation. Conversely, the turnover of those businesses whose acquisition has been closed subsequent to the preparation of the most recent audited accounts, but before the relevant date for establishing jurisdiction, must be added to a company's turnover for notification purposes.

---

[CJN para. 220] (2.3. Financial holding companies)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 220
Turnover calculation for financial holding companies as described above may in practice prove onerous. Therefore a strict and detailed application of this method will be necessary only in cases where it seems that the turnover of a financial holding company is likely to be close to the Merger Regulation thresholds; in other cases it may well be obvious that the turnover is far from the thresholds of the Merger Regulation, and therefore the published accounts are adequate for the establishment of jurisdiction.

---

[CJN para. 170] (4.1. The general rule)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 170
The Commission is reluctant to rely on management or any other fo
```
</details>

---

## q17 (single)

**Question:** The target reports its turnover in dollars, how do we convert it into euro for the thresholds?

**Reference answer:** At the average exchange rate for the twelve months concerned, converting the audited annual figures as such, not quarter by quarter or month by month.

**Answer shown to the associate:**

> Answer withheld by the citation guardrail (citations not found in the search results: CJN para. 204, CJN para. 205). The Deal Desk documents do not cover this. Please check with counsel or rephrase the question.

<details><summary>Passages the search returned</summary>

```
[CJN para. 205] (VI. CONVERSION OF TURNOVER INTO EURO)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 205
When a company has sales in a range of currencies, the procedure is no different. The total turnover given in the consolidated audited accounts and in that company's reporting currency is converted into euros at the yearly average rate. Local currency sales should not be converted directly into euros since these figures are not from the consolidated audited accounts of the company.

---

[CJN para. 204] (VI. CONVERSION OF TURNOVER INTO EURO)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 204
When converting turnover figures into euro great care should be taken with the exchange rate used. The annual turnover of a company should be converted at the average rate for the twelve months concerned. This average can be obtained via DG Competition's website. The audited annual turnover figures should be converted as such and not be broken down into quarterly or monthly figures which would then be converted individually.

---

[CJN para. 158] (1. The concept of turnover)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 158
In the case of services, the method of calculating turnover in general does not differ from that used in the case of products: the Commission takes into consideration the total amount of sales. However, the calculation of the amounts derived from the provision of services may be more complex as this depends on the exact service provided and the underlying legal and economic arrangements in the sector in question. Where one undertaking provides the entire service directly to the customer, the turnover of the undertaking concerned consists of the total amount of sales for the provision of services in the last financial year.

---

[CJN para. 195] (V. GEOGRAPHIC ALLOCATION OF TURNOVER)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 195
The thresholds concerning Community-wide and Member State turnover in Article 1(2) and (3) aim to identify cases which have sufficient turnover within the Community in order to be of Community interest and which are primarily cross-border in nature. They require turnover to be allocated geographically to the Community and to individual Member States. Since audited accounts often do not provide a geographical breakdown as required by the Merger Regulation, the Commission will rely on the best figures available provided by the undertakings. The second subparagraph of Article 5(1) provides that the location of turnover is determined by the location of the customer at the time of the transaction: ‘Turnover, in the Community or in a Member State, shall comprise products sold and services provided to undertakings or consumers, in the Community or in that Member State as the case may be.’

---

[EUMR Art. 5(1)–(2)] (Calculation of turnover)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 5(1), Art. 5(2)
Aggregate turnover within the meaning of this Regulation shall comprise the amounts derived by the undertakings concerned in the preceding financial year from the sale of products and the provision of services falling within the undertakings' ordinary activities after deduction of sales rebates and of value added tax and other taxes directly related to turnover. The aggregate turnover of an undertaking concerned shall not include the sale of products or the provision of services between any of the undertakings referred to in paragraph 4. Turnover, in the Community or in a Member State, shall comprise products sold and services provided to undertakings or consumers, in the Community or in that Member State as the case may be. By way of derogation from paragraph 1, where the concentration consists of the acquisition of parts, whether or not constituted as legal entities, of one or more undertakings, only the turnover relating to the parts which are the subject of the concentration shall be taken into account with regard to the seller or sellers. However, two or more transactions within the meaning of the first subparagraph which take place within a two-year period between the same persons or undertakings shall be treated as one and the same concentration arising on the date of the last transaction.
```
</details>

---

## q19 (single)

**Question:** How long can the seller's non-compete in the share purchase agreement last?

**Reference answer:** Up to three years when goodwill and know-how are transferred; up to two years when only goodwill is transferred.

**Answer shown to the associate:**

> Answer withheld by the citation guardrail (citations not found in the search results: ARN para. 22, ARN para. 23). The Deal Desk documents do not cover this. Please check with counsel or rephrase the question.

<details><summary>Passages the search returned</summary>

```
[ARN para. 18] (A. Non-competition clauses)
Document: Commission Notice on restrictions directly related and necessary to concentrations (Ancillary Restraints Notice)
Covers: para. 18
Non-competition obligations which are imposed on the vendor in the context of the transfer of an undertaking or of part of it can be directly related and necessary to the implementation of the concentration. In order to obtain the full value of the assets transferred, the purchaser must be able to benefit from some protection against competition from the vendor in order to gain the loyalty of customers and to assimilate and exploit the know-how. Such non-competition clauses guarantee the transfer to the purchaser of the full value of the assets transferred, which in general include both physical assets and intangible assets, such as the goodwill accumulated or the know-how developed by the vendor. These are not only directly related to the concentration but are also necessary to its implementation because, without them, there would be reasonable grounds to expect that the sale of the undertaking or of part of it could not be accomplished.

---

[ARN para. 25] (A. Non-competition clauses)
Document: Commission Notice on restrictions directly related and necessary to concentrations (Ancillary Restraints Notice)
Covers: para. 25
Clauses which limit the vendor's right to purchase or hold shares in a company competing with the business transferred shall be considered directly related and necessary to the implementation of the concentration under the same conditions as outlined above for non-competition clauses, unless they prevent the vendor from purchasing or holding shares purely for financial investment purposes, without granting him/her, directly or indirectly, management functions or any material influence in the competing company.

---

[ARN para. 20] (A. Non-competition clauses)
Document: Commission Notice on restrictions directly related and necessary to concentrations (Ancillary Restraints Notice)
Covers: para. 20
Non-competition clauses are justified for periods of up to three years, when the transfer of the undertaking includes the transfer of customer loyalty in the form of both goodwill and know-how. When only goodwill is included, they are justified for periods of up to two years.

---

[ARN para. 23] (A. Non-competition clauses)
Document: Commission Notice on restrictions directly related and necessary to concentrations (Ancillary Restraints Notice)
Covers: para. 23
Similarly, non-competition clauses must remain limited to products (including improved versions or updates of products as well as successor models) and services forming the economic activity of the undertaking transferred. This can include products and services at an advanced stage of development at the time of the transaction, or products which are fully developed but not yet marketed. Protection against competition from the vendor in product or service markets in which the transferred undertaking was not active before the transfer is not considered necessary.

---

[ARN para. 22] (A. Non-competition clauses)
Document: Commission Notice on restrictions directly related and necessary to concentrations (Ancillary Restraints Notice)
Covers: para. 22
The geographical scope of a non-competition clause must be limited to the area in which the vendor has offered the relevant products or services before the transfer, since the purchaser does not need to be protected against competition from the vendor in territories not previously penetrated by the vendor. That geographical scope can be extended to territories which the vendor was planning to enter at the time of the transaction, provided that he had already invested in preparing this move.
```
</details>

---

## q20 (single)

**Question:** The buyer wants an exclusive supply agreement with the seller with no limit on quantities, does it count as an ancillary restraint?

**Reference answer:** No. Only purchase and supply obligations for fixed quantities (possibly with a variation clause) are; unlimited quantities, exclusivity or preferred-supplier status are not necessary.

**Answer shown to the associate:**

> Answer withheld by the citation guardrail (citations not found in the search results: ARN para. 33, ARN para. 34). The Deal Desk documents do not cover this. Please check with counsel or rephrase the question.

<details><summary>Passages the search returned</summary>

```
[ARN para. 34] (C. Purchase and supply obligations)
Document: Commission Notice on restrictions directly related and necessary to concentrations (Ancillary Restraints Notice)
Covers: para. 34
Both supply and purchase obligations providing for fixed quantities, possibly with a variation clause, are recognised as directly related and necessary to the implementation of the concentration. However, obligations providing for unlimited quantities, exclusivity or conferring preferred-supplier or preferred-purchaser status, are not necessary to the implementation of the concentration.

---

[ARN para. 33] (C. Purchase and supply obligations)
Document: Commission Notice on restrictions directly related and necessary to concentrations (Ancillary Restraints Notice)
Covers: para. 33
The aim of such obligations may be to ensure the continuity of supply to either of the parties of products necessary for carrying out the activities retained by the vendor or taken over by the purchaser. However, the duration of purchase and supply obligations must be limited to a period necessary for the replacement of the relationship of dependency by autonomy in the market. Thus, purchase or supply obligations aimed at guaranteeing the quantities previously supplied can be justified for a transitional period of up to five years.

---

[ARN para. 32] (C. Purchase and supply obligations)
Document: Commission Notice on restrictions directly related and necessary to concentrations (Ancillary Restraints Notice)
Covers: para. 32
In many cases, the transfer of an undertaking or of part of it can entail the disruption of traditional lines of purchase and supply which have existed as a result of the previous integration of activities within the economic unity of the vendor. In order to enable the break-up of the economic unity of the vendor and the partial transfer of the assets to the purchaser under reasonable conditions, it is often necessary to maintain, for a transitional period, the existing or similar links between the vendor and the purchaser. This objective is normally attained by purchase and supply obligations for the vendor and/or the purchaser of the undertaking or of part of it. Taking into account the particular situation resulting from the break-up of the economic unity of the vendor, such obligations can be recognised as directly related and necessary to the implementation of the concentration. They may be in favour of the vendor as well as the purchaser, depending on the particular circumstances of the case.

---

[ARN para. 35] (C. Purchase and supply obligations)
Document: Commission Notice on restrictions directly related and necessary to concentrations (Ancillary Restraints Notice)
Covers: para. 35
Service and distribution agreements are equivalent in their effect to supply arrangements; consequently the same considerations as above shall apply.

---

[ARN para. 13] (II. GENERAL PRINCIPLES)
Document: Commission Notice on restrictions directly related and necessary to concentrations (Ancillary Restraints Notice)
Covers: para. 13
Agreements must be ‘necessary to the implementation of the concentration’, which means that, in the absence of those agreements, the concentration could not be implemented or could only be implemented under considerably more uncertain conditions, at substantially higher cost, over an appreciably longer period or with considerably greater difficulty. Agreements necessary to the implementation of a concentration are typically aimed at protecting the value transferred, maintaining the continuity of supply after the break-up of a former economic entity, or enabling the start-up of a new entity. In determining whether a restriction is necessary, it is appropriate not only to take account of its nature, but also to ensure that its duration, subject matter and geographical field of application does not exceed what the implementation of the concentration reasonably requires. If equally effective alternatives are available for attaining the legitimate aim pursued, the undertakings must choose the one which is objectively the least restrictive of competition.
```
</details>

---

## q22 (single)

**Question:** If a Member State is screening a foreign investment, how long do the other Member States and the Commission have to send their comments?

**Reference answer:** No later than 35 calendar days after receiving the information, or 20 calendar days after receiving additional information if it was requested.

**Answer shown to the associate:**

> No later than 35 calendar days following receipt of the information [FDI Art. 6(7)]. 
> 
> However, other Member States and the Commission must notify their intention to provide comments or an opinion within 15 calendar days of receiving the information [FDI Art. 6(4)]. If additional information is requested, comments or opinions must be issued within 20 calendar days following receipt of the additional information [FDI Art. 6(7)].

<details><summary>Passages the search returned</summary>

```
[FDI Art. 6(4)–(6)] (Cooperation mechanism in relation to foreign direct investments undergoing screening)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 6(4), Art. 6(5), Art. 6(6)
A Member State which duly considers that a foreign direct investment in its territory is likely to affect its security or public order may request the Commission to issue an opinion or other Member States to provide comments. The comments referred to in paragraph 2 and the opinions referred to in paragraph 3 shall be duly justified. No later than 15 calendar days following the receipt of the information referred to in paragraph 1, other Member States and the Commission shall notify the Member State undertaking the screening of their intention to provide comments pursuant to paragraph 2 or an opinion pursuant to paragraph 3. The notification may include a request for additional information to the information referred to in paragraph 1. Any request for additional information shall be duly justified, limited to information necessary to provide comments pursuant to paragraph 2 or to issue an opinion pursuant to paragraph 3, proportionate to the purpose of the request and not unduly burdensome for the Member State undertaking the screening. Requests for information and replies provided by Member States shall be sent to the Commission simultaneously.

---

[FDI Art. 6(1)–(2)] (Cooperation mechanism in relation to foreign direct investments undergoing screening)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 6(1), Art. 6(2)
Member States shall notify the Commission and the other Member States of any foreign direct investment in their territory that is undergoing screening by providing the information referred to in Article 9(2) of this Regulation as soon as possible. The notification may include a list of Member States whose security or public order is deemed likely to be affected. As part of the notification, and where applicable, the Member State undertaking the screening shall endeavour to indicate whether it considers that the foreign direct investment undergoing screening is likely to fall within the scope of Regulation (EC) No 139/2004. Where a Member State considers that a foreign direct investment undergoing screening in another Member State is likely to affect its security or public order, or has information relevant for such screening, it may provide comments to the Member State undertaking the screening. The Member State providing comments shall send those comments to the Commission simultaneously. The Commission shall notify the other Member States that comments were provided.

---

[FDI Art. 7(6)–(7)] (Cooperation mechanism in relation to foreign direct investments not undergoing screening)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 7(6), Art. 7(7)
Comments pursuant to paragraph 1 or opinions pursuant to paragraph 2 shall be addressed to the Member State where the foreign direct investment is planned or has been completed and shall be sent to it within a reasonable period of time, and in any case no later than 35 calendar days following receipt of the information referred to in paragraph 5 or of the notification pursuant to Article 9(5). In cases where the opinion of the Commission follows comments from other Member States, the Commission shall have 15 additional calendar days for issuing that opinion. A Member State where a foreign direct investment is planned or has been completed shall give due consideration to the comments of the other Member States and to the opinion of the Commission.

---

[FDI Art. 6(7)] (Cooperation mechanism in relation to foreign direct investments undergoing screening)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 6(7)
Comments referred to in paragraph 2 or opinions referred to in paragraph 3 shall be addressed to the Member State undertaking the screening and shall be sent to it within a reasonable period of time, and in any case no later than 35 calendar days following receipt of the information referred to in paragraph 1. Notwithstanding the first subparagraph, if additional information was requested pursuant to paragraph 6, such comments or opinions shall be issued no later than 20 calendar days following receipt of the additional information or the notification pursuant to Article 9(5). Notwithstanding paragraph 6, the Commission may issue an opinion following comments from other Member States where possible within the deadlines referred to in this paragraph, and in any case no later than five calendar days after those deadlines have expired.

---

[FDI Art. 6(8)–(9)] (Cooperation mechanism in relation to foreign direct investments undergoing screening)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 6(8), Art. 6(9)
In the exceptional case where the Member State undertaking the screening considers that its security or public order requires immediate action, it shall notify the other Member States and the Commission of its intention to issue a screening decision before the timeframes referred to in paragraph 7 and duly justify the need for immediate action. The other Member States and the Commission shall endeavour to provide comments or to issue an opinion expeditiously. The Member State undertaking the screening shall give due consideration to the comments of the other Member States referred to in paragraph 2 and to the opinion of the Commission referred to in paragraph 3. The final screening decision shall be taken by the Member State undertaking the screening.
```
</details>

---

## q24 (single)

**Question:** A foreign investment was completed without being screened, until when can the Commission still give an opinion on it?

**Reference answer:** No later than 15 months after the foreign direct investment has been completed.

**Answer shown to the associate:**

> The Commission may issue an opinion on a foreign direct investment that has been completed without undergoing screening no later than **15 months** after the investment has been completed [FDI Art. 7(8)]. This is subject to the specific deadlines for issuing the opinion once the information is provided, and does not apply to investments completed before 10 April 2019 [FDI Art. 7(6), (8)].

<details><summary>Passages the search returned</summary>

```
[FDI Art. 6(7)] (Cooperation mechanism in relation to foreign direct investments undergoing screening)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 6(7)
Comments referred to in paragraph 2 or opinions referred to in paragraph 3 shall be addressed to the Member State undertaking the screening and shall be sent to it within a reasonable period of time, and in any case no later than 35 calendar days following receipt of the information referred to in paragraph 1. Notwithstanding the first subparagraph, if additional information was requested pursuant to paragraph 6, such comments or opinions shall be issued no later than 20 calendar days following receipt of the additional information or the notification pursuant to Article 9(5). Notwithstanding paragraph 6, the Commission may issue an opinion following comments from other Member States where possible within the deadlines referred to in this paragraph, and in any case no later than five calendar days after those deadlines have expired.

---

[FDI Art. 7(6)–(7)] (Cooperation mechanism in relation to foreign direct investments not undergoing screening)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 7(6), Art. 7(7)
Comments pursuant to paragraph 1 or opinions pursuant to paragraph 2 shall be addressed to the Member State where the foreign direct investment is planned or has been completed and shall be sent to it within a reasonable period of time, and in any case no later than 35 calendar days following receipt of the information referred to in paragraph 5 or of the notification pursuant to Article 9(5). In cases where the opinion of the Commission follows comments from other Member States, the Commission shall have 15 additional calendar days for issuing that opinion. A Member State where a foreign direct investment is planned or has been completed shall give due consideration to the comments of the other Member States and to the opinion of the Commission.

---

[FDI Art. 7(8)–(10)] (Cooperation mechanism in relation to foreign direct investments not undergoing screening)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 7(8), Art. 7(9), Art. 7(10)
Member States may provide comments pursuant to paragraph 1 and the Commission may provide an opinion pursuant to paragraph 2 no later than 15 months after the foreign direct investment has been completed. Cooperation pursuant to this Article shall take place through the contact points established in accordance with Article 11. This Article shall not apply to foreign direct investments completed before 10 April 2019.

---

[FDI Recital 21] (Recitals)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Recital 21
In order to provide greater certainty for investors, Member States should have the possibility to make comments and the Commission should have the possibility to issue an opinion in relation to completed investments not undergoing screening for a period limited to 15 months after the completion of the foreign direct investment. The cooperation mechanism should not apply to foreign direct investments completed before 10 April 2019.

---

[FDI Art. 6(4)–(6)] (Cooperation mechanism in relation to foreign direct investments undergoing screening)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 6(4), Art. 6(5), Art. 6(6)
A Member State which duly considers that a foreign direct investment in its territory is likely to affect its security or public order may request the Commission to issue an opinion or other Member States to provide comments. The comments referred to in paragraph 2 and the opinions referred to in paragraph 3 shall be duly justified. No later than 15 calendar days following the receipt of the information referred to in paragraph 1, other Member States and the Commission shall notify the Member State undertaking the screening of their intention to provide comments pursuant to paragraph 2 or an opinion pursuant to paragraph 3. The notification may include a request for additional information to the information referred to in paragraph 1. Any request for additional information shall be duly justified, limited to information necessary to provide comments pursuant to paragraph 2 or to issue an opinion pursuant to paragraph 3, proportionate to the purpose of the request and not unduly burdensome for the Member State undertaking the screening. Requests for information and replies provided by Member States shall be sent to the Commission simultaneously.
```
</details>

---

## q26 (single)

**Question:** What is an up-front buyer remedy?

**Reference answer:** The parties commit not to complete the notified deal before entering into a binding agreement with a purchaser for the divested business approved by the Commission.

**Answer shown to the associate:**

> An up-front buyer remedy is a commitment where the parties undertake not to complete the notified transaction before entering into a binding agreement with a Commission-approved purchaser for the divested business [RN para. 53]. Unlike a "fix-it-first" remedy where the purchaser's identity is known during the Commission's procedure, the identity of the up-front buyer is not known prior to the authorization decision [RN para. 50]. 
> 
> The Commission requires it in cases involving:
> * Considerable obstacles to divestiture (e.g., third-party rights or uncertainty in finding a purchaser) [RN para. 54].
> * High risks of preserving the competitiveness and saleability of the divestment business during the interim period (e.g., risk of losing key employees or where carve-out can only occur after a sales and purchase agreement is signed) [RN para. 55].

<details><summary>Passages the search returned</summary>

```
[RN para. 53] (2. Up-front buyer)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 53
There are cases where only the proposal of an up-front buyer will allow the Commission to conclude with the requisite degree of certainty that the business will be effectively divested to a suitable purchaser. The parties therefore have to undertake in the commitments that they are not going to complete the notified operation before having entered into a binding agreement with a purchaser for the divested business, approved by the Commission.

---

[RN para. 54] (2. Up-front buyer)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 54
First, this concerns cases where there are considerable obstacles for a divestiture, such as third party rights, or uncertainties as to finding a suitable purchaser. In such cases, an up-front buyer will allow the Commission to conclude with the requisite degree of certainty that the commitments will be implemented, as such a commitment creates greater incentives for the parties to close the divestiture in order to be able to complete their own concentration. In these circumstances, parties may choose between proposing an up-front buyer and an alternative divestiture commitment, as set out above in paragraph 46.

---

[RN para. 50] ((b) Identification of a suitable purchaser)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 50
In general, there are three ways to ensure that the business is transferred to a suitable purchaser. First, the business is transferred within a fixed time-limit after adoption of the decision to a purchaser which is approved by the Commission on the basis of the purchaser requirements. Second, in addition to the conditions set out for the first category, the commitments foresee that the parties may not complete the notified operation before having entered into a binding agreement with a purchaser for the business, approved by the Commission (so-called ‘up-front-buyer’). Third, the parties identify a purchaser for the business and enter into a binding agreement already during the Commission's procedure (so-called ‘fix-it-first’ remedy). The main difference between the two latter options is that in the case of an up-front buyer, the identity of the purchaser is not known to the Commission prior to the authorisation decision.

---

[RN para. 57] (3. Fix-it-first remedies)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 57
The Commission welcomes fix-it-first remedies in particular in cases where the identity of the purchaser is crucial for the effectiveness of the proposed remedy. This concerns cases where, given the circumstances, only very few potential purchasers can be considered suitable, in particular as the divested business is not a viable business in itself, but its viability will only be ensured by specific assets of the purchaser, or where the purchaser needs to have specific characteristics in order for the remedy to solve the competition concerns. If the parties choose to enter into a binding agreement with a suitable purchaser during the procedure by way of a fix-it-first solution, the Commission can in those circumstances conclude with the requisite degree of certainty that the commitments will be implemented with a sale to a suitable purchaser. In these situations, an ‘upfront buyer’ solution containing specific requirements as to the suitability of a buyer will generally be considered equivalent and acceptable.

---

[RN para. 55] (2. Up-front buyer)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 55
Second, an up-front buyer may be necessary in cases which cause considerable risks of preserving the competitiveness and saleability of the divestment business in the interim period until divestiture. This category comprises cases where the risks of a degradation of the divestment business appear to be high, in particular due to a risk of losing employees being key for the business, or where the interim risks are increased as the parties are not able to undertake the carve-out process in the interim period, but the carve-out process can only take place once a sales and purchase agreement with a purchaser is entered into. The up-front buyer provision may accelerate the transfer of the business to be divested — given the increased incentives for the parties to close the divestiture in order to be able to complete their own concentration — to such an extent that the commitments may allow the Commission to conclude with the requisite degree of certainty that those risks are limited and the divestiture will be effectively implemented.
```
</details>

---

## q28 (multi)

**Question:** Our client is buying joint control of a target together with a partner, who notifies, and how do we count the turnover between the joint venture and third parties?

**Reference answer:** The acquirers of joint control notify jointly; turnover of the joint undertaking with third parties is apportioned equally among the undertakings concerned, ignoring sales between the joint undertaking and the undertakings concerned.

**Answer shown to the associate:**

> Concentrations arising from changes in joint control must be notified jointly by the undertakings acquiring joint control (existing and new shareholders) [CJN para. 144]. 
> 
> For turnover generated with third parties, the joint venture’s turnover is apportioned equally among the undertakings exercising joint control, irrespective of their capital or voting share [EUMR Art. 5(5)(b), CJN para. 186]. Sales between the joint venture and the controlling undertakings (or connected undertakings) are excluded [EUMR Art. 5(5)(a)].

<details><summary>Passages the search returned</summary>

```
[CJN para. 87] (1. Entry of controlling shareholders)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 87
The entry of a new shareholder in a jointly controlled undertaking — either in addition to the already controlling shareholders or in replacement of one of them — also constitutes a notifiable concentration, although the undertaking is jointly controlled before and after the operation. First, also in this scenario there is a shareholder newly acquiring control of the joint venture. Second, the quality of control of the joint venture is determined by the identity of all controlling shareholders. It lies in the nature of joint control that, since each shareholder alone has a blocking right concerning strategic decisions, the jointly controlling shareholders have to take into account each others interests and are required to cooperate for the determination of the strategic behaviour of the joint venture. The nature of joint control therefore does not exhaust itself in a pure mathematical addition of the blocking rights exercised by several shareholders, but is determined by the composition of the jointly controlling shareholders. One of the most obvious scenarios leading to a decisive change in the nature of the control structure of a jointly controlled undertaking is a situation where in a joint venture, jointly controlled by a competitor of the joint venture and a financial investor, the financial investor is replaced by another competitor. In these circumstances, the control structure and the incentives of the joint venture may entirely change, not only because of the entry of the new controlling shareholder, but also due to the change in the behaviour of the remaining shareholder. The replacement of a controlling shareholder or the entry of a new shareholder in a jointly controlled undertaking therefore constitutes a change in the quality of control.

---

[CJN para. 139] (3. Acquisition of control)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 139
In the case of acquisition of joint control of a newly-created undertaking, the undertakings concerned are each of the companies acquiring control of the newly set-up joint venture (which, as it does not yet exist, cannot be considered to be an undertaking concerned and moreover, as yet, has no turnover of its own). The same rule applies where one undertaking contributes a pre-existing subsidiary or a business (over which it previously exercised sole control) to a newly created joint venture. In these circumstances, each of the jointly-controlling undertakings is considered an undertaking concerned whereas any company or business contributed to the joint venture is not an undertaking concerned, and its turnover is part of the turnover of the initial parent company.

---

[CJN para. 86] (1. Entry of controlling shareholders)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 86
A move from sole control to joint control is considered a notifiable operation as this changes the quality of control of the joint venture. First, there is a new acquisition of control for the shareholder entering the controlled undertaking. Second, only the new acquisition of control makes the controlled undertaking to a joint venture which changes decisively also the situation for the remaining controlling undertaking under the Merger Regulation: In the future, it has to take into account the interests of one or more other controlling shareholder(s) and it is required to cooperate permanently with the new shareholder(s). Before, it could either determine the strategic behaviour of the controlled undertaking alone (in the case of sole control) or was not forced to take into account the interests of specific other shareholders and was not forced to cooperate with those shareholders permanently.

---

[CJN para. 143] (3. Acquisition of control)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 143
In the case where one or more shareholders acquire control, either by entry or by substitution of one or more shareholders, in a situation of joint control both before and after the operation, the undertakings concerned are the shareholders (both existing and new) who exercise joint control and the joint venture itself. On the one hand, similar to the acquisition of joint control of an existing company, the joint venture itself can be considered as an undertaking concerned as it is an already pre-existing undertaking. On the other hand, as set out above, the entry of a new shareholder is not only in itself a new acquisition of control, but also leads to a change in the quality of control for the remaining controlling shareholders as the quality of control of the joint venture is determined by the identity and composition of the controlling shareholders and therefore also by the relationship between them. Furthermore, the Merger Regulation considers a joint venture as a combination of the economic resources of the parent companies, together with the joint venture if it already generates turnover on the market. For these reasons, the newly entering controlling shareholders are undertakings concerned alongside with the remaining controlling shareholders. Due to the change of the quality in control, all of them are considered to undertake an acquisition of control.

---

[CJN para. 144] (3. Acquisition of control)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 144
As Article 4(2) first sentence of the Merger Regulation foresees that all acquisitions of joint control shall be notified jointly by the undertakings acquiring joint control, existing and new shareholders in principle have to notify concentrations arising from such changes in joint control scenarios jointly.

[CJN para. 187] (5.2. Allocation of turnover of the undertakings identified)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 187
The principle contained in Article 5(5)(b) is followed by analogy for the allocation of turnover for joint ventures between undertakings concerned and third parties if their turnover is taken into account according to Article 5(4)(b) as set out above in paragraph 181. The Commission's practice has been to allocate to the undertaking concerned the turnover of the joint venture on a per capita basis according to the number of undertakings exercising joint control. In the example, half of the turnover of b3 is taken into account.

---

[CJN para. 186] (5.2. Allocation of turnover of the undertakings identified)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 186
However, the Merger Regulation includes specific rules for joint venture
```
</details>

---

## q30 (multi)

**Question:** The target is being bought by a subsidiary of a big group, whose turnover counts for the thresholds, only the subsidiary's or the whole group's?

**Reference answer:** The acquiring subsidiary and the target are the undertakings concerned, but the turnover of the whole group linked to the subsidiary under Article 5(4) (parents, subsidiaries and sister companies) is included.

**Answer shown to the associate:**

> Answer withheld by the citation guardrail (citations not found in the search results: CJN para. 135, CJN para. 177). The Deal Desk documents do not cover this. Please check with counsel or rephrase the question.

<details><summary>Passages the search returned</summary>

```
[CJN para. 135] (3. Acquisition of control)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 135
Where the target undertaking is acquired by a group through one of its subsidiaries, the undertakings concerned are the target undertaking and the acquiring subsidiary if this is not a mere acquisition vehicle. However, even though the subsidiary is normally the undertaking concerned for the purpose of calculating turnover, the turnover of all undertakings with which the undertaking concerned has the links as specified in Article 5(4) shall be included in the threshold calculations. In this respect, the group is considered to be a single economic unit and the different companies belonging to the same group cannot be considered as different undertakings concerned for jurisdictional purposes under the Merger Regulation. The actual notification can be made by the subsidiary concerned or by its parent company.

---

[CJN para. 177] (5.1. Identification of undertakings whose turnover is taken into account)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 177
Article 5(4) of the Merger Regulation provides the following: ‘Without prejudice to paragraph 2 [acquisitions of parts], the aggregate turnover of an undertaking concerned within the meaning of Article 1(2) and (3) shall be calculated by adding together the respective turnovers of the following: An undertaking which has in another undertaking the rights and powers mentioned in Article 5(4)(b) will be referred to as the ‘parent’ of the latter in the present section of this Notice dealing with the calculation of turnover, whereas the latter is referred to as ‘subsidiary’ of the former. In short, Article 5(4) therefore provides that the turnover of the undertaking concerned by the concentration (point (a)) should include its subsidiaries (point (b)), its parent companies (point (c)), the other subsidiaries of its parent undertakings (point (d)) and any other subsidiary jointly held by two or more of the undertakings identified under (a)-(d) (point (e)). (a) the undertaking concerned; (b) those undertakings in which the undertaking concerned directly or indirectly: (i) owns more than half the capital or business assets, or (ii) has the power to exercise more than half the voting rights, or (iii) has the power to appoint more than half the members of the supervisory board, the administrative board or bodies legally representing the undertakings, or (iv) has the right to manage the undertaking's affairs; (c) those undertakings which have in an undertaking concerned the rights or powers listed in (b); (d) those undertakings in which an undertaking as referred to in (c) has the rights or powers listed in (b); (e) those undertakings in which two or more undertakings as referred to in (a) to (d) jointly have the rights or powers listed in (b).’

---

[CJN para. 175] (5.1. Identification of undertakings whose turnover is taken into account)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 175
When an undertaking concerned by a concentration belongs to a group, not only the turnover of the undertaking concerned is considered, but the Merger Regulation requires to also take into account the turnover of those undertakings with which the undertaking concerned has links consisting in the rights or powers listed in Article 5(4) in order to determine whether the thresholds contained in Article 1 of the Merger Regulation are met. The aim is again to capture the total volume of the economic resources that are being combined through the operation irrespective of whether the economic activities are carried out directly by the undertaking concerned or whether they are undertaken indirectly via undertakings with which the undertaking concerned possesses the links described in Article 5(4).

---

[CJN para. 185] (5.2. Allocation of turnover of the undertakings identified)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 185
In general, as long as the test under Article 5(4)(b) is fulfilled, the whole turnover of the subsidiary in question will be taken into account regardless of the actual shareholding which the undertaking concerned holds in the subsidiary. In the chart, the whole turnover of the subsidiaries called b of the undertaking concerned a will be taken into account.

---

[CJN para. 220] (2.3. Financial holding companies)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 220
Turnover calculation for financial holding companies as described above may in practice prove onerous. Therefore a strict and detailed application of this method will be necessary only in cases where it seems that the turnover of a financial holding company is likely to be close to the Merger Regulation thresholds; in other cases it may well be obvious that the turnover is far from the thresholds of the Merger Regulation, and therefore the published accounts are adequate for the establishment of jurisdiction.
```
</details>

---

## q32 (multi)

**Question:** A state-owned investor from outside the EU wants to buy an EU energy network operator, which screening factors could apply?

**Reference answer:** Effects on critical infrastructure such as energy (Article 4(1)(a)) and whether the investor is directly or indirectly controlled by a third-country government (Article 4(2)(a)).

**Answer shown to the associate:**

> When assessing whether a foreign direct investment affects security or public order, Member States and the Commission may consider the investment's potential effects on **critical infrastructure**, specifically including energy infrastructure and land or real estate crucial for its use [FDI Art. 4(1)(a)]. 
> 
> Additionally, because the investor is state-owned, authorities may consider whether the foreign investor is directly or indirectly controlled by a third-country government (including via ownership structure or significant funding), whether it has been involved in activities affecting security or public order, or whether there is a serious risk of illegal or criminal activities [FDI Art. 4(2)]. They may also account for the context of whether the investor is pursuing state-led outward projects or programmes [FDI Recital 13].

<details><summary>Passages the search returned</summary>

```
[FDI Art. 4(1)] (Factors that may be taken into consideration by Member States or the Commission)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 4(1)
In determining whether a foreign direct investment is likely to affect security or public order, Member States and the Commission may consider its potential effects on, inter alia: (a) critical infrastructure, whether physical or virtual, including energy, transport, water, health, communications, media, data processing or storage, aerospace, defence, electoral or financial infrastructure, and sensitive facilities, as well as land and real estate crucial for the use of such infrastructure; (b) critical technologies and dual use items as defined in point 1 of Article 2 of Council Regulation (EC) No 428/2009, including artificial intelligence, robotics, semiconductors, cybersecurity, aerospace, defence, energy storage, quantum and nuclear technologies as well as nanotechnologies and biotechnologies; (c) supply of critical inputs, including energy or raw materials, as well as food security; (d) access to sensitive information, including personal data, or the ability to control such information; or (e) the freedom and pluralism of the media.

---

[FDI Art. 4(2)] (Factors that may be taken into consideration by Member States or the Commission)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 4(2)
In determining whether a foreign direct investment is likely to affect security or public order, Member States and the Commission may also take into account, in particular: (a) whether the foreign investor is directly or indirectly controlled by the government, including state bodies or armed forces, of a third country, including through ownership structure or significant funding; (b) whether the foreign investor has already been involved in activities affecting security or public order in a Member State; or (c) whether there is a serious risk that the foreign investor engages in illegal or criminal activities.

---

[FDI Recital 13] (Recitals)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Recital 13
In determining whether a foreign direct investment may affect security or public order, it should be possible for Member States and the Commission to consider all relevant factors, including the effects on critical infrastructure, technologies (including key enabling technologies) and inputs which are essential for security or the maintenance of public order, the disruption, failure, loss or destruction of which would have a significant impact in a Member State or in the Union. In that regard, it should also be possible for Member States and the Commission to take into account the context and circumstances of the foreign direct investment, in particular whether a foreign investor is controlled directly or indirectly, for example through significant funding, including subsidies, by the government of a third country or is pursuing State-led outward projects or programmes.

---

[FDI Art. 1(1)–(3)] (Subject matter and scope)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 1(1), Art. 1(2), Art. 1(3)
This Regulation establishes a framework for the screening by Member States of foreign direct investments into the Union on the grounds of security or public order and for a mechanism for cooperation between Member States, and between Member States and the Commission, with regard to foreign direct investments likely to affect security or public order. It includes the possibility for the Commission to issue opinions on such investments. This Regulation is without prejudice to each Member State having sole responsibility for its national security, as provided for in Article 4(2) TEU, and to the right of each Member State to protect its essential security interests in accordance with Article 346 TFEU. Nothing in this Regulation shall limit the right of each Member State to decide whether or not to screen a particular foreign direct investment within the framework of this Regulation.

---

[FDI Art. 3(1)–(4)] (Screening mechanisms of Member States)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 3(1), Art. 3(2), Art. 3(3), Art. 3(4)
In accordance with this Regulation, Member States may maintain, amend or adopt mechanisms to screen foreign direct investments in their territory on the grounds of security or public order. Rules and procedures related to screening mechanisms, including relevant timeframes, shall be transparent and not discriminate between third countries. In particular, Member States shall set out the circumstances triggering the screening, the grounds for screening and the applicable detailed procedural rules. Member States shall apply timeframes under their screening mechanisms. The screening mechanisms shall allow Member States to take into account the comments of other Member States referred to in Article 6 and 7 and the opinions of the Commission referred to in Articles 6, 7 and 8. Confidential information, including commercially-sensitive information, made available to the Member State undertaking the screening shall be protected.
```
</details>

---

## q34 (multi)

**Question:** If we offer commitments in Phase II after working day 55, what's the deadline to submit them and when does the Commission have to take the final decision?

**Reference answer:** Commitments must be submitted within 65 working days of the opening of proceedings, and because they come after day 55 the decision deadline rises from 90 to 105 working days.

**Answer shown to the associate:**

> The deadline to submit commitments in Phase II is not more than 65 working days from the initiation of proceedings [RN para. 88]. Only in exceptional circumstances may the Commission accept commitments submitted for the first time after that period [RN para. 88]. 
> 
> If commitments are submitted on working day 55 or afterwards, the Commission has to take a final decision within 105 working days of the initiation of proceedings [RN para. 89].

<details><summary>Passages the search returned</summary>

```
[RN para. 89] (2. Phase II)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 89
The question whether or not submitting remedies will extend the deadline for the Commission to take a final decision depends on the time in the procedure when the commitments are submitted. Where the parties submit commitments within less than 55 working days after the initiation of proceedings, the Commission has to take a final decision within not more than 90 working days of the date of initiation of proceedings. Where the parties submit commitments on working day 55 or afterwards (even after working day 65, if those commitments should be acceptable due to exceptional circumstances as described above in paragraph 88), the period for the Commission to take a final decision is increased to 105 working days according to Article 10(3), subparagraph 2. Where the parties submit commitments within less than 55 working days, but submit a modified version on day 55 or thereafter, the period to take a final decision will also be extended to 105 working days.

---

[RN para. 90] (2. Phase II)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 90
The Commission is available to discuss suitable commitments well in advance of the end of the 65 working day period. The parties are encouraged to submit draft proposals dealing with both substantive and implementation aspects which are necessary to ensure that the commitments are fully workable. If the parties are of the opinion that more time is needed for the investigation of the competition concerns and for the corresponding design of appropriate commitments, they may also suggest to the Commission to extend the final deadline under Article 10(3), subparagraph 1. Such a request will have to be made before the end of the 65 working day period. Indeed, the Commission will normally not extend the period for adopting a final decision according to Article 10(3), subparagraph 1 where the request for extension is presented after the deadline for submitting remedies foreseen in the Implementing Regulation, i.e. after working day 65.

---

[RN para. 88] (2. Phase II)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 88
Commitments proposed to the Commission pursuant to Article 8(2) must be submitted to the Commission within not more than 65 working days from the day on which proceedings were initiated. Where the deadlines for the final decision have been extended according to Article 10(3) of the Merger Regulation, also the deadline for remedies is automatically extended by the same number of days. Only in exceptional circumstances, the Commission may accept that commitments are submitted for the first time after the expiry of this period. The request by the parties for an extension of the deadline must be received within the period and has to set forth the exceptional circumstances which, according to the parties, justify it. In addition to the existence of exceptional circumstances, an extension is only possible where there is sufficient time to make a proper assessment of the proposal by the Commission and to allow adequate consultation with Member States and third parties.

---

[RN para. 94] (2. Phase II)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 94
The Merger Regulation does not impose any obligation on the Commission to accept commitments after the legal deadline for remedies, unless the Commission voluntarily undertakes to assess commitments in specific circumstances. In view of this, where parties subsequently modify the proposed commitments after the deadline of 65 working days, the Commission will only accept these modified commitments where it can clearly determine — on the basis of its assessment of information already received in the course of the investigation, including the results of prior market testing, and without the need for any other market test — that such commitments, once implemented, fully and unambiguously resolve the competition concerns identified and where there is sufficient time to allow for an adequate assessment by the Commission and for proper consultation with Member States. The Commission will normally reject modified commitments which do not fulfil those conditions.

---

[RN para. 78] (1. Phase I)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 78
Parties can submit proposals for commitments to the Commission on an informal basis, even before notification. Parties have to submit commitments within not more than 20 working days from the date of the receipt of the notification. The Commission informs the parties about its serious doubts in due time before that deadline. Where the parties submit commitments, the deadline for the Commission's decision pursuant to Article 6(1) of the Merger Regulation is extended from 25 to 35 working days.
```
</details>

---

## q35 (multi)

**Question:** Our client is a private equity fund set up as a limited partnership, who acquires control in its deals, and whose turnover is counted?

**Reference answer:** Control is normally exercised by the investment company that set up the fund (the limited partners normally do not control), and the investment company is treated as having the Article 5(4)(b) powers, so the turnover of the portfolio companies it controls through its funds is attributed to it.

**Answer shown to the associate:**

> Answer withheld by the citation guardrail (citations not found in the search results: CJN para. 15, 189, CJN para. 190, 191). The Deal Desk documents do not cover this. Please check with counsel or rephrase the question.

<details><summary>Passages the search returned</summary>

```
[CJN para. 190] (5.3. Allocation of turnover in case of investment funds)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 190
The same considerations, as set out above in the framework of Article 3 (paragraph 15), may also apply if an investment company sets up several investment funds with possibly different investors. Typically, on the basis of the organisational structure, in particular links between the investment company and the general partner(s) of the different funds organised as limited partnerships, or contractual arrangements, especially advisory agreements between the general partner or the investment fund and the investment company, the investment company will indirectly have the power to exercise the voting rights held by the investment fund in the portfolio companies or indirectly have one of the other powers or rights set out in Article 5(4)(b). In these circumstances, the investment company may exercise a common control structure over the different funds which it has set up and the common operation of the different funds by the investment company is often indicated by a common brand for the funds.

---

[CJN para. 15] (1.1. Person or undertaking acquiring control)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 15
Investment funds are often set up in the legal form of limited partnerships, in which the investors participate as limited partners and normally do not exercise control, either individually or collectively. The investment funds usually acquire the shares and voting rights which confer control over the portfolio companies. Depending on the circumstances, control is normally exercised by the investment company which has set up the fund as the fund itself is typically a mere investment vehicle; in more exceptional circumstances, control may be exercised by the fund itself. The investment company usually exercises control by means of the organisational structure, e.g. by controlling the general partner of fund partnerships, or by contractual arrangements, such as advisory agreements, or by a combination of both. This may be the case even if the investment company itself does not own the company acting as a general partner, but their shares are held by natural persons (who may be linked to the investment company) or by a trust. Contractual arrangements with the investment company, in particular advisory agreements, will become even more important if the general partner does not have any own resources and personnel for the management of the portfolio companies, but only constitutes a company structure whose acts are performed by persons linked to the investment company. In these circumstances, the investment company normally acquires indirect control within the meaning of Article 3(1)(b) and 3(3)(b) of the Merger Regulation, and has the power to exercise the rights which are directly held by the investment fund.

---

[CJN para. 191] (5.3. Allocation of turnover in case of investment funds)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 191
Consequently, such an organisation of the different funds by the investment company may lead to the result that the turnover of all portfolio companies held by different funds is taken into account for the purpose of assessing whether the turnover thresholds in Article 1 are met if the investment company acquires indirect control of a portfolio company via one of the funds.

---

[CJN para. 189] (5.3. Allocation of turnover in case of investment funds)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 189
The investment company, as set out above in paragraph 15, normally acquires indirect control over portfolio companies held by an investment fund. In the same way, the investment company may be considered to indirectly have the powers and rights which are set out in Article 5(4)(b), in particular to indirectly have the power to exercise the voting rights held by the investment fund in the portfolio companies.

---

[CJN para. 181] (5.1. Identification of undertakings whose turnover is taken into account)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 181
The right to manage also covers situations in which the undertaking concerned jointly has the right to manage an undertaking's affairs together with third parties. The underlying consideration is that the undertakings exercising joint control have jointly the right to manage the controlled undertakings' affairs even if each of them individually may have those rights only in a negative sense, i.e. in the form of veto rights. In the example, the undertaking (b3) which is jointly controlled by the undertaking concerned (a) and a third party (x) is taken into account as both (a) and (x) have veto rights in (b3) on the basis of their equal shareholding in (b3). Under Article 5(4)(b)(iv) the Commission only takes into account those joint ventures in which the undertaking concerned and third parties have de jure rights that give rise to a clear-cut right to manage. The inclusion of joint ventures is therefore limited to situations where the undertaking concerned and third parties have a joint right to manage on the basis of an agreement, e.g. a shareholders' agreement, or where the undertaking concerned and a third party have an equality of voting rights to the effect that they have the right to appoint an equal number of members to the decision-making bodies of the joint venture.

[CJN para. 191] (5.3. Allocation of turnover in case of investment funds)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 191
Consequently, such an organisation of the different funds by the investment company may lead to the result that the turnover of all portfolio companies held by different funds is taken into account for the purpose of assessing whether the turnover thresholds in Article 1 are met if the investment company acquires indirect control of a portfolio company via one of the funds.

---

[CJN para. 189] (5.3. Allocation of turnover in case of investment funds)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 189
The investment company, as set out above in paragraph 15, normally acquires indirect control over portfolio companies held by an investment fund. In the same way, the investment company may be considered to indirectly have the powers and rights which are set out in Article 5(4)(b), in particular to indirectly have the power to exercise the voting rights held by the investment fund in the portfolio companies.

---

[CJN para. 190] (5.3. Allocation of turnover in case of investment funds)
Document: Commission Consolidated Jurisdic
```
</details>

---

## q36 (unanswerable)

**Question:** If the deal doesn't have an EU dimension, what are the Spanish merger notification thresholds that would apply?

**Reference answer:** The corpus does not cover Spanish national merger control, so the assistant should say it does not know and suggest asking counsel or checking the CNMC rules.

**Answer shown to the associate:**

> The Deal Desk documents do not cover this. The Deal Desk library includes EU merger control rules (EUMR, CJN, Remedies Notice, Ancillary Restraints Notice) and the EU FDI Screening Regulation, but it does not contain national rules such as Spanish merger control thresholds. Please ask outside counsel for the applicable Spanish thresholds.

<details><summary>Passages the search returned</summary>

```
[EUMR Art. 1(1)–(3)] (Scope)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 1(1), Art. 1(2), Art. 1(3)
Without prejudice to Article 4(5) and Article 22, this Regulation shall apply to all concentrations with a Community dimension as defined in this Article. A concentration has a Community dimension where: (a) the combined aggregate worldwide turnover of all the undertakings concerned is more than EUR 5000 million; and (b) the aggregate Community-wide turnover of each of at least two of the undertakings concerned is more than EUR 250 million, unless each of the undertakings concerned achieves more than two-thirds of its aggregate Community-wide turnover within one and the same Member State. A concentration that does not meet the thresholds laid down in paragraph 2 has a Community dimension where: (a) the combined aggregate worldwide turnover of all the undertakings concerned is more than EUR 2500 million; (b) in each of at least three Member States, the combined aggregate turnover of all the undertakings concerned is more than EUR 100 million; (c) in each of at least three Member States included for the purpose of point (b), the aggregate turnover of each of at least two of the undertakings concerned is more than EUR 25 million; and (d) the aggregate Community-wide turnover of each of at least two of the undertakings concerned is more than EUR 100 million, unless each of the undertakings concerned achieves more than two-thirds of its aggregate Community-wide turnover within one and the same Member State.

---

[CJN para. 125] (I. THRESHOLDS)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 125
Two sets of thresholds are set out in Article 1 to establish whether the operation has a Community dimension. Article 1(2) establishes three different criteria: The worldwide turnover threshold is intended to measure the overall dimension of the undertakings concerned; the Community turnover threshold seek to determine whether the concentration involves a minimum level of activities in the Community; and the two-thirds rule aims to exclude purely domestic transactions from Community jurisdiction.

---

[CJN para. 124] (I. THRESHOLDS)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 124
A two fold test defines the operations to which the Merger Regulation applies. The first test is that the operation must be a concentration within the meaning of Article 3. The second comprises the turnover thresholds contained in Article 1, designed to identify those operations which have an impact upon the Community and can be deemed to be of ‘Community dimension’. Turnover is used as a proxy for the economic resources being combined in a concentration, and is allocated geographically in order to reflect the geographic distribution of those resources.

---

[EUMR Art. 4(1)] (Prior notification of concentrations and pre-notification referral at the request of the notifying parties)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 4(1)
Concentrations with a Community dimension defined in this Regulation shall be notified to the Commission prior to their implementation and following the conclusion of the agreement, the announcement of the public bid, or the acquisition of a controlling interest. Notification may also be made where the undertakings concerned demonstrate to the Commission a good faith intention to conclude an agreement or, in the case of a public bid, where they have publicly announced an intention to make such a bid, provided that the intended agreement or bid would result in a concentration with a Community dimension. For the purposes of this Regulation, the term "notified concentration" shall also cover intended concentrations notified pursuant to the second subparagraph. For the purposes of paragraphs 4 and 5 of this Article, the term "concentration" includes intended concentrations within the meaning of the second subparagraph.

---

[RN para. 4] (II. GENERAL PRINCIPLES)
Document: Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)
Covers: para. 4
Under the Merger Regulation, the Commission assesses the compatibility of a notified concentration with the common market on the basis of its effect on the structure of competition in the Community. The test for compatibility under Article 2(2) and (3) of the Merger Regulation is whether or not a concentration would significantly impede effective competition in the common market or a substantial part of it, in particular as a result of the creation or strengthening of a dominant position. A concentration that significantly impedes effective competition as described above is incompatible with the common market and the Commission is required to prohibit it. For the creation of a joint venture, the Commission will also examine the concentration under Article 2(4) of the Merger Regulation. The principles set out in this Notice will generally also apply to remedies submitted to eliminate competition concerns identified under Article 2(4).
```
</details>

---

## q38 (unanswerable)

**Question:** Does our deal also have to be notified to the Commission under the Foreign Subsidies Regulation?

**Reference answer:** The corpus does not include the Foreign Subsidies Regulation; the assistant should say it does not cover it.

**Answer shown to the associate:**

> The Deal Desk documents do not cover this. The library contains the EU Merger Regulation, the Jurisdictional Notice, the Remedies Notice, the Ancillary Restraints Notice, and the FDI Screening Regulation, but it does not include the Foreign Subsidies Regulation (Regulation (EU) 2022/2560). Please ask outside counsel to check whether foreign subsidies thresholds apply to the deal.

<details><summary>Passages the search returned</summary>

```
[EUMR Art. 4(1)] (Prior notification of concentrations and pre-notification referral at the request of the notifying parties)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 4(1)
Concentrations with a Community dimension defined in this Regulation shall be notified to the Commission prior to their implementation and following the conclusion of the agreement, the announcement of the public bid, or the acquisition of a controlling interest. Notification may also be made where the undertakings concerned demonstrate to the Commission a good faith intention to conclude an agreement or, in the case of a public bid, where they have publicly announced an intention to make such a bid, provided that the intended agreement or bid would result in a concentration with a Community dimension. For the purposes of this Regulation, the term "notified concentration" shall also cover intended concentrations notified pursuant to the second subparagraph. For the purposes of paragraphs 4 and 5 of this Article, the term "concentration" includes intended concentrations within the meaning of the second subparagraph.

---

[EUMR Art. 4(2)–(3)] (Prior notification of concentrations and pre-notification referral at the request of the notifying parties)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 4(2), Art. 4(3)
A concentration which consists of a merger within the meaning of Article 3(1)(a) or in the acquisition of joint control within the meaning of Article 3(1)(b) shall be notified jointly by the parties to the merger or by those acquiring joint control as the case may be. In all other cases, the notification shall be effected by the person or undertaking acquiring control of the whole or parts of one or more undertakings. Where the Commission finds that a notified concentration falls within the scope of this Regulation, it shall publish the fact of the notification, at the same time indicating the names of the undertakings concerned, their country of origin, the nature of the concentration and the economic sectors involved. The Commission shall take account of the legitimate interest of undertakings in the protection of their business secrets.

---

[EUMR Art. 4(5)] (Prior notification of concentrations and pre-notification referral at the request of the notifying parties)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 4(5)
With regard to a concentration as defined in Article 3 which does not have a Community dimension within the meaning of Article 1 and which is capable of being reviewed under the national competition laws of at least three Member States, the persons or undertakings referred to in paragraph 2 may, before any notification to the competent authorities, inform the Commission by means of a reasoned submission that the concentration should be examined by the Commission. The Commission shall transmit this submission to all Member States without delay. Any Member State competent to examine the concentration under its national competition law may, within 15 working days of receiving the reasoned submission, express its disagreement as regards the request to refer the case. Where at least one such Member State has expressed its disagreement in accordance with the third subparagraph within the period of 15 working days, the case shall not be referred. The Commission shall, without delay, inform all Member States and the persons or undertakings concerned of any such expression of disagreement. Where no Member State has expressed its disagreement in accordance with the third subparagraph within the period of 15 working days, the concentration shall be deemed to have a Community dimension and shall be notified to the Commission in accordance with paragraphs 1 and 2. In such situations, no Member State shall apply its national competition law to the concentration.

---

[FDI Art. 6(1)–(2)] (Cooperation mechanism in relation to foreign direct investments undergoing screening)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 6(1), Art. 6(2)
Member States shall notify the Commission and the other Member States of any foreign direct investment in their territory that is undergoing screening by providing the information referred to in Article 9(2) of this Regulation as soon as possible. The notification may include a list of Member States whose security or public order is deemed likely to be affected. As part of the notification, and where applicable, the Member State undertaking the screening shall endeavour to indicate whether it considers that the foreign direct investment undergoing screening is likely to fall within the scope of Regulation (EC) No 139/2004. Where a Member State considers that a foreign direct investment undergoing screening in another Member State is likely to affect its security or public order, or has information relevant for such screening, it may provide comments to the Member State undertaking the screening. The Member State providing comments shall send those comments to the Commission simultaneously. The Commission shall notify the other Member States that comments were provided.

---

[FDI Art. 6(3)] (Cooperation mechanism in relation to foreign direct investments undergoing screening)
Document: Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union
Covers: Art. 6(3)
Where the Commission considers that a foreign direct investment undergoing screening is likely to affect security or public order in more than one Member State, or has relevant information in relation to that foreign direct investment, it may issue an opinion addressed to the Member State undertaking the screening. The Commission may issue an opinion irrespective of whether other Member States have provided comments. The Commission may issue an opinion following comments from other Member States. The Commission shall issue such opinion where justified, after at least one third of Member States consider that a foreign direct investment is likely to affect their security or public order. The Commission shall notify the other Member States that an opinion was issued.
```
</details>

---

## q40 (unanswerable)

**Question:** The buyer is American, what are the US Hart-Scott-Rodino filing thresholds this year?

**Reference answer:** The corpus only covers EU rules; the assistant should say it does not know.

**Answer shown to the associate:**

> The Deal Desk documents do not cover this. The library only contains EU merger control, ancillary restraints, remedies, and EU foreign-investment screening regulations, and does not include US Hart-Scott-Rodino rules. Please ask outside counsel.

<details><summary>Passages the search returned</summary>

```
[EUMR Art. 1(1)–(3)] (Scope)
Document: Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)
Covers: Art. 1(1), Art. 1(2), Art. 1(3)
Without prejudice to Article 4(5) and Article 22, this Regulation shall apply to all concentrations with a Community dimension as defined in this Article. A concentration has a Community dimension where: (a) the combined aggregate worldwide turnover of all the undertakings concerned is more than EUR 5000 million; and (b) the aggregate Community-wide turnover of each of at least two of the undertakings concerned is more than EUR 250 million, unless each of the undertakings concerned achieves more than two-thirds of its aggregate Community-wide turnover within one and the same Member State. A concentration that does not meet the thresholds laid down in paragraph 2 has a Community dimension where: (a) the combined aggregate worldwide turnover of all the undertakings concerned is more than EUR 2500 million; (b) in each of at least three Member States, the combined aggregate turnover of all the undertakings concerned is more than EUR 100 million; (c) in each of at least three Member States included for the purpose of point (b), the aggregate turnover of each of at least two of the undertakings concerned is more than EUR 25 million; and (d) the aggregate Community-wide turnover of each of at least two of the undertakings concerned is more than EUR 100 million, unless each of the undertakings concerned achieves more than two-thirds of its aggregate Community-wide turnover within one and the same Member State.

---

[CJN para. 174] (4.2. Adjustments after the date of the last audited accounts)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 174
Other factors that may affect turnover on a temporary basis such as a decrease in orders for the product or a slow-down in the production process within the period prior to the transaction will be ignored for the purposes of calculating turnover. No adjustment to the definitive accounts will be made to incorporate them.

---

[CJN para. 137] (3. Acquisition of control)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 137
The second subparagraph of Article 5(2) includes a special provision on staggered operations or follow-up deals. The previous concentrations (within two years) involving the same parties become (re)notifiable with the most recent transaction, provided this constitutes a concentration, if the thresholds are met whether for one or more of the transactions taken in isolation or cumulatively. In this case, the undertakings concerned are the acquirer(s) and the different acquired part(s) of the target company taken as a whole.

---

[CJN para. 172] (4.2. Adjustments after the date of the last audited accounts)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 172
change is not taken into account, unless the sale is a pre-condition for the notified operation. Conversely, the turnover of those businesses whose acquisition has been closed subsequent to the preparation of the most recent audited accounts, but before the relevant date for establishing jurisdiction, must be added to a company's turnover for notification purposes.

---

[CJN para. 169] (4.1. The general rule)
Document: Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004
Covers: para. 169
The Commission seeks to base itself upon the most accurate and reliable figures available. Generally, the Commission will refer to accounts which relate to the closest financial year to the date of the transaction and which are audited under the standard applicable to the undertaking in question and compulsory for the relevant financial year. An adjustment of the audited figures should only take place if this is required by the provisions of the Merger Regulation, including the cases explained in more detail in paragraph 172.
```
</details>
