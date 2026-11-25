# Label sheet (grade these BEFORE opening judge_verdicts.csv)

For each answer write one line in `eval/human_labels.csv`:

- `correct` = 1 if the answer is right against the reference (or, for an unanswerable question, a proper refusal), else 0.
- `supported` = 1 if EVERY claim in the answer is in the retrieved text shown, else 0.
- `notes` = why, for every 0.


---
## q01 (single)
**Question:** How many weeks does a payer have to ask their payment service provider for a refund of a payment that was initiated by the payee, such as a direct debit?

**Reference:** 8 weeks from the date the funds were debited.

**Agent answer:** A payer must request a refund from their payment service provider within **8 weeks** from the date on which the funds were debited [payment_services_regs_2017, regulation 80]. 

This applies to authorised payment transactions initiated by or through a payee, such as direct debits, provided certain conditions are met or if the transaction is a specific type of SEPA direct debit [payment_services_regs_2017, regulation 79]. Note that if the payer is not a consumer, micro-enterprise, or charity, the parties may agree that these refund rights do not apply [payment_services_regs_2017, regulation 63(5)].

<details><summary>Retrieved text (excerpt)</summary>

[payment_services_regs_2017, regulation 80]
Payment Services Regulations 2017, regulation 80 - Requests for refunds for payment transactions initiated by or through a payee
80 1 The payer must request a refund under regulation 79 from its payment service provider within 8 weeks from the date on which the funds were debited. 2 The payment service provider may require the payer to provide such information as is reasonably necessary to prove that the conditions in regulation 79(2) are satisfied. 3 The payment service provider must either— a refund the full amount of the payment transaction; or b provide justification for refusing to refund the payment transaction, indicating the bodies to which the payer may refer the matter if the payer does not accept the justification provided. 4 Any refund or justification for refusing a refund must be provided within 10 business days of receiving a request for a refund or, where applicable, within 10 business days of receiving any further information requested under paragraph (2). 5 If the payment service provider requires further information under paragraph (2), it may not refuse the refund until it has received further information from the payer.

[payment_services_regs_2017, regulation 79(6)]
Payment Services Regulations 2017, regulation 79(6) - Refunds for payment transactions initiated by or through a payee
6 The payer and payment service provider may agree in the framework contract that the right to a refund does not apply where— a the payer has given consent directly to the payment service provider for the payment transaction to be executed; and b if applicable, information on the payment transaction was provided or made available in an agreed manner to the payer for at least four weeks before the due date by the payment servic

</details>


---
## q02 (single)
**Question:** If a payment service provider refuses to refund a payee-initiated payment, what does it have to tell the payer?

**Reference:** It must give a justification for refusing and indicate the bodies the payer can refer the matter to if they do not accept it.

**Agent answer:** If a payment service provider refuses to refund a payment transaction initiated by or through a payee, it must:

*   Provide a **justification** for the refusal; and
*   Indicate the **bodies** to which the payer may refer the matter if they do not accept that justification.

This information must be provided within **10 business days** of receiving the refund request or any further information requested from the payer.

[payment_services_regs_2017, regulation 80]

<details><summary>Retrieved text (excerpt)</summary>

[payment_services_regs_2017, regulation 80]
Payment Services Regulations 2017, regulation 80 - Requests for refunds for payment transactions initiated by or through a payee
80 1 The payer must request a refund under regulation 79 from its payment service provider within 8 weeks from the date on which the funds were debited. 2 The payment service provider may require the payer to provide such information as is reasonably necessary to prove that the conditions in regulation 79(2) are satisfied. 3 The payment service provider must either— a refund the full amount of the payment transaction; or b provide justification for refusing to refund the payment transaction, indicating the bodies to which the payer may refer the matter if the payer does not accept the justification provided. 4 Any refund or justification for refusing a refund must be provided within 10 business days of receiving a request for a refund or, where applicable, within 10 business days of receiving any further information requested under paragraph (2). 5 If the payment service provider requires further information under paragraph (2), it may not refuse the refund until it has received further information from the payer.

[payment_services_regs_2017, regulation 79(6)]
Payment Services Regulations 2017, regulation 79(6) - Refunds for payment transactions initiated by or through a payee
6 The payer and payment service provider may agree in the framework contract that the right to a refund does not apply where— a the payer has given consent directly to the payment service provider for the payment transaction to be executed; and b if applicable, information on the payment transaction was provided or made available in an agreed manner to the payer for at least four weeks before the due date by the payment servic

</details>


---
## q03 (single)
**Question:** Can a customer cancel a payment order once their bank has received it?

**Reference:** In general no, after the payer's provider has received it; there are exceptions (e.g. direct debit cut-off, later revocation only by agreement).

**Agent answer:** Generally, a customer cannot revoke a payment order once it has been received by their bank [payment_services_regs_2017, regulation 83(1)]. However, there are specific rules for different types of payments:

*   **Direct Debits:** The customer cannot revoke the payment after the end of the business day preceding the day agreed for debiting the funds [payment_services_regs_2017, regulation 83(3)].
*   **Future-dated payments:** If a specific day was agreed for execution, the order cannot be revoked after the end of the business day preceding that day [payment_services_regs_2017, regulation 83(4)].
*   **PISP or Payee-initiated payments:** The payer cannot revoke the order after giving consent to the payment initiation service provider or the payee [payment_services_regs_2017, regulation 83(2)].

After these time limits, a payment order can only be revoked if the customer and the bank agree (and, for payee-initiated transactions, the payee also agrees) [payment_services_regs_2017, regulation 83(5)]. The bank may charge for such a revocation if the contract allows it [payment_services_regs_2017, regulation 83(6)].

<details><summary>Retrieved text (excerpt)</summary>

[payment_services_regs_2017, regulation 83]
Payment Services Regulations 2017, regulation 83 - Revocation of a payment order
83 1 Subject to paragraphs (2) to (5), a payment service user may not revoke a payment order after it has been received by the payer's payment service provider. 2 In the case of a payment transaction initiated by a payment initiation service provider, or by or through the payee, the payer may not revoke the payment order after giving consent to the payment initiation service provider to initiate the payment transaction or giving consent to execute the payment transaction to the payee. 3 In the case of a direct debit, the payer may not revoke the payment order after the end of the business day preceding the day agreed for debiting the funds. 4 Where a day is agreed under regulation 81(5) (receipt of payment orders), the payment service user may not revoke a payment order after the end of the business day preceding the agreed day. 5 At any time after the time limits for revocation set out in paragraphs (1) to (4), the payment order may only be revoked if the revocation is— a agreed between the payment service user and the relevant payment service provider or providers; and b in the case of a payment transaction initiated by or through the payee, including in the case of a direct debit, also agreed with the payee. 6 A framework contract may provide for the relevant payment service provider to charge for revocation under this regulation.

[payment_services_regs_2017, regulation 67]
Payment Services Regulations 2017, regulation 67 - Consent and withdrawal of consent
67 1 A payment transaction is to be regarded as having been authorised by the payer for the purposes of this Part only if the payer has given its consent to— a the execution of the payment 

</details>


---
## q04 (single)
**Question:** A shop did not tell a customer about a card surcharge before they paid. Does the customer still have to pay the surcharge?

**Reference:** No. A payer is not obliged to pay a charge they were not informed of in full beforehand.

**Agent answer:** No, the customer is not obliged to pay the surcharge if they were not informed of its full amount before the initiation of the payment transaction [payment_services_regs_2017, regulation 58].

<details><summary>Retrieved text (excerpt)</summary>

[payment_services_regs_2017, regulation 58]
Payment Services Regulations 2017, regulation 58 - Information on additional charges or reductions
58 1 The payee must inform the payer of any charge requested or reduction offered by the payee for the use of a particular payment instrument before the initiation of the payment transaction. 2 The payment service provider, or any relevant other party involved in the transaction, must inform the payment service user of any charge requested by the payment service provider or other party, as the case may be, for the use of a particular payment instrument before the initiation of the payment transaction. 3 A payer or payment service user is not obliged to pay a charge of the type referred to in paragraph (1) or (2) if the payer or payment service user was not informed of the full amount of the charge in accordance with the relevant paragraph.

[payment_services_regs_2017, regulation 78]
Payment Services Regulations 2017, regulation 78 - Payment transactions where the transaction amount is not known in advance
78 Where a card-based payment transaction is initiated by or through the payee and the amount of the transaction is not known when the payer authorises the transaction— a the payer's payment service provider may not block funds on the payer's payment account unless the payer has authorised the exact amount of the funds to be blocked; and b the payer's payment service provider must release the blocked funds without undue delay after becoming aware of the amount of the payment transaction, and in any event immediately after receipt of the payment order.

[payment_services_regs_2017, regulation 61]
Payment Services Regulations 2017, regulation 61 - Information on ATM withdrawal charges
61 A provider of cash withdrawal services fal

</details>


---
## q07 (single)
**Question:** When is an e-money issuer allowed to charge a fee for redeeming electronic money?

**Reference:** Only if the fee is stated in the contract and redemption is requested before termination, or the holder ends a fixed-term contract early, or redemption is requested more than a year after termination. Fees must be proportionate to actual costs.

**Agent answer:** An electronic money issuer may only charge a fee for redemption if the fee is stated in the contract and one of the following applies:
*   Redemption is requested before the contract is terminated.
*   The holder terminates the contract before the agreed termination date.
*   Redemption is requested more than one year after the contract was terminated.

Any such fee must be "proportionate and commensurate with the costs actually incurred by the electronic money issuer" [electronic_money_regs_2011, regulation 41]. Additionally, the contract must clearly and prominently state these conditions and fees before the holder is bound by it [electronic_money_regs_2011, regulation 40].

<details><summary>Retrieved text (excerpt)</summary>

[electronic_money_regs_2011, regulation 41]
Electronic Money Regulations 2011, regulation 41 - Fees for redemption
41 1 Redemption may be subject to a fee only where the fee is stated in the contract in accordance with regulation 40(a), and— a redemption is requested before the termination of the contract; b the contract provides for a termination date and the electronic money holder terminates the contract before that date; or c redemption is requested more than one year after the date of termination of the contract. 2 Any fees for redemption must be proportionate and commensurate with the costs actually incurred by the electronic money issuer.

[electronic_money_regs_2011, regulation 42]
Electronic Money Regulations 2011, regulation 42 - Amount of redemption
42 1 Where before the termination of the contract an electronic money holder makes a request for redemption, the electronic money holder may request redemption of the monetary value of the electronic money in whole or in part, and the electronic money issuer must redeem the amount so requested subject to any fee imposed in accordance with regulation 41. 2 Where an electronic money holder makes a request for redemption on, or up to one year after, the date of the termination of the contract, the electronic money issuer must redeem— a the total monetary value of the electronic money held; or b if the electronic money issuer carries out any business activities other than the issuance of electronic money and it is not known in advance what proportion of funds received by it is to be used for electronic money, all the funds requested by the electronic money holder.

[electronic_money_regs_2011, regulation 40]
Electronic Money Regulations 2011, regulation 40 - Conditions of redemption
40 An electronic money issuer must 

</details>


---
## q09 (single)
**Question:** Which categories of payment service provider must the FCA keep on its public register?

**Reference:** Authorised payment institutions, small payment institutions, registered account information service providers, certain exclusion notifiers, registered agents, and the bodies in regulation 3(1) when providing payment services.

**Agent answer:** Under the Payment Services Regulations 2017, the FCA must maintain a register of the following categories of payment service provider (and related persons):

(a) Authorised payment institutions [payment_services_regs_2017, regulation 4(1)(a)];
(b) Small payment institutions [payment_services_regs_2017, regulation 4(1)(b)];
(c) Registered account information service providers [payment_services_regs_2017, regulation 4(1)(c)];
(d) Persons providing a limited network or electronic communications exclusion service who have notified the FCA under regulation 38 or 39 [payment_services_regs_2017, regulation 4(1)(d)];
(e) Agents of authorised payment institutions, small payment institutions, and registered account information service providers, registered under regulation 34 [payment_services_regs_2017, regulation 4(1)(e)]; and
(f) Certain exempt bodies specified in regulation 3(1) when they provide payment services [payment_services_regs_2017, regulation 4(1)(f)].

<details><summary>Retrieved text (excerpt)</summary>

[payment_services_regs_2017, regulation 4(5)-(6)]
Payment Services Regulations 2017, regulation 4(5)-(6) - The register of certain payment service providers
5 The FCA must— a publish the register online and make it available for public inspection; b enter in the register any cancellation of an authorisation or registration; c enter in the register a description of the service provided by a person included on the register by virtue of paragraph (1)(d); d update the register without delay; and e provide a certified copy of the register, or any part of it, to any person who asks for it— i on payment of the fee (if any) fixed by the FCA; and ii in a form (either written or electronic) in which it is legible to the person asking for it. 6 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[payment_services_regs_2017, regulation 4(1)-(4)]
Payment Services Regulations 2017, regulation 4(1)-(4) - The register of certain payment service providers
1 The FCA must maintain a register of— a authorised payment institutions ...; b small payment institutions; c registered account information service providers; d persons providing a service falling within paragraph 2(k)(i) to (iii) or (l) of Schedule 1 who have notified the FCA under regulation 38 or 39 (notification of use of limited network or electronic communications exclusion); e agents of authorised payment institutions, small payment institutions and registered account information service providers, registered under regulation 34 (use of agents); and f the persons specified in regulation 3(1) (exemption for certain bodies) where they provide payment services. 2 The FCA may include on the register any of the persons mentioned in paragraphs (f) to (i) of the definition of a payment service provider in regulation 2(1) 

</details>


---
## q11 (single)
**Question:** For safeguarding e-money funds, what minimum net assets must a credit institution outside the OECD have to count as an approved foreign credit institution?

**Reference:** Minimum net assets of 5 million pounds (plus audited accounts, a surplus for the last two years and an unqualified annual report).

**Agent answer:** Under the Electronic Money Regulations 2011, a credit institution outside the OECD must have minimum net assets of **£5 million** (or its equivalent in any other currency at the relevant time) to qualify as an approved foreign credit institution for safeguarding purposes [electronic_money_regs_2011, regulation 21(8)].

<details><summary>Retrieved text (excerpt)</summary>

[electronic_money_regs_2011, regulation 21(8)]
Electronic Money Regulations 2011, regulation 21(8) - Safeguarding option 1
8 In paragraph (7), “ approved foreign credit institution ” means— a the central bank of a State that is a member of the Organisation for Economic Co-operation and Development (“an OECD state”), b a credit institution that is supervised by the central bank or other banking regulator of an OECD state, c any credit institution that— i is subject to regulation by the banking regulator of a State that is not an OECD state, ii is required by the law of the country or territory in which it is established to provide audited accounts, iii has minimum net assets of £5 million (or its equivalent in any other currency at the relevant time), iv has a surplus of revenue over expenditure for the last two financial years, and v has an annual report which is not materially qualified.

[payment_services_regs_2017, regulation 23(19)]
Payment Services Regulations 2017, regulation 23(19) - Safeguarding requirements
19 In paragraph (18), “ approved foreign credit institution ” means— a the central bank of a State that is a member of the Organisation for Economic Co-operation and Development (“an OECD state”), b a credit institution that is supervised by the central bank or other banking regulator of an OECD state, c any credit institution that— i is subject to regulation by the banking regulator of a State that is not an OECD state, ii is required by the law of the country or territory in which it is based to provide audited accounts, iii has minimum net assets of £5 million (or its equivalent in any other currency at the relevant time), iv has a surplus of revenue over expenditure for the last two financial years, and v has an annual report which is not materially qual

</details>


---
## q13 (single)
**Question:** Which risk factors must a firm consider when carrying out its money laundering risk assessment?

**Reference:** Factors relating to its customers, the countries or areas it operates in, its products or services, its transactions and its delivery channels.

**Agent answer:** When carrying out its money laundering risk assessment, a firm must take into account information provided by its supervisory authority and consider risk factors relating to:

*   its customers;
*   the countries or geographic areas in which it operates;
*   its products or services;
*   its transactions; and
*   its delivery channels.

The firm must also take into account the size and nature of its business when deciding what steps are appropriate for this assessment [money_laundering_regs_2017, regulation 18].

<details><summary>Retrieved text (excerpt)</summary>

[money_laundering_regs_2017, regulation 18]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 18 - Risk assessment by relevant persons
18 1 A relevant person must take appropriate steps to identify and assess the risks of money laundering and terrorist financing to which its business is subject. 2 In carrying out the risk assessment required under paragraph (1), a relevant person must take into account— a information made available to them by the supervisory authority under regulations 17(9) and 47, and b risk factors including factors relating to— i its customers; ii the countries or geographic areas in which it operates; iii its products or services; iv its transactions; and v its delivery channels. 3 In deciding what steps are appropriate under paragraph (1), the relevant person must take into account the size and nature of its business. 4 A relevant person must keep an up-to-date record in writing of all the steps it has taken under paragraph (1), unless its supervisory authority notifies it in writing that such a record is not required. 5 A supervisory authority may not give the notification referred to in paragraph (4) unless it considers that the risks of money laundering and terrorist financing applicable to the sector in which the relevant person operates are clear and understood. 6 A relevant person must provide the risk assessment it has prepared under paragraph (1), the information on which that risk assessment was based and any record required to be kept under paragraph (4), to its supervisory authority on request.

[money_laundering_regs_2017, regulation 18A]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 18A - Risk assessment by relevant persons in relation to proliferation f

</details>


---
## q15 (single)
**Question:** If someone commits an offence under the Money Laundering Regulations while outside the UK, can they still be prosecuted in the UK?

**Reference:** Yes. An offence committed wholly or partly outside the UK may be treated as committed within the jurisdiction of the court where proceedings are taken.

**Agent answer:** Yes. An offence committed wholly or partly outside the United Kingdom under the Money Laundering Regulations may, for all incidental purposes, be treated as having been committed within the jurisdiction of the court where proceedings are taken [money_laundering_regs_2017, regulation 90]. Proceedings can be taken before the appropriate court in the United Kingdom having jurisdiction where the person is for the time being, or at any appropriate UK court if they cannot be taken there [money_laundering_regs_2017, regulation 90].

<details><summary>Retrieved text (excerpt)</summary>

[money_laundering_regs_2017, regulation 90]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 90 - Proceedings: jurisdiction
90 1 Proceedings against any person for an offence under these Regulations may be taken before the appropriate court in the United Kingdom having jurisdiction in the place where that person is for the time being. 2 Proceedings against any person for an offence under these Regulations which cannot be taken under paragraph (1) may be taken at any appropriate court in the United Kingdom. 3 An offence falling under these Regulations which is committed wholly or partly outside the United Kingdom may for all incidental purposes be treated as having been committed within the jurisdiction of the court where proceedings were taken.

[money_laundering_regs_2017, regulation 89]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 89 - Proceedings: general
89 1 Proceedings for an offence under these Regulations may be instituted by— a order of the Commissioners; b a local weights and measures authority; c the Department for the Economy; d the Director of Public Prosecutions; or e the Director of Public Prosecutions for Northern Ireland. 2 Where proceedings under paragraph (1) are instituted by order of the Commissioners, the proceedings must be brought in the name of an officer of Revenue and Customs. 3 A local weights and measures authority must, whenever the FCA or (where the authority is acting pursuant to arrangements made with the Commissioners) the Commissioners require, report in such form and with such particulars as the FCA or the Commissioners require on the exercise of its functions under these Regulations. 4 Where the Commissioners investigate, or propose to investigate, an

</details>


---
## q17 (single)
**Question:** How long must the FCA keep published information about a final notice on its website?

**Reference:** At least five years, unless personal data rules require a different period.

**Agent answer:** The FCA must ensure that information about a matter to which a final notice relates remains on its official website for at least five years, unless it is personal data and data protection legislation requires a different retention period [money_laundering_regs_2017, regulation 84(9)-(11)].

<details><summary>Retrieved text (excerpt)</summary>

[money_laundering_regs_2017, regulation 84(1)-(4)]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 84(1)-(4) - Publication: the FCA
1 Where a warning notice is given by the FCA under regulation 81(2), neither the FCA nor any person to whom it is given or copied may publish the notice or any details concerning it. 2 Where the FCA gives a decision notice under regulation 81(6), the FCA must publish on their official website such information about the matter to which the notice relates as it considers appropriate, subject to paragraphs (3) to (9). 3 Where the FCA publishes information under paragraph (2) or (4) about a matter to which a decision notice relates and the person to whom the notice is given refers the matter to the Upper Tribunal (see regulation 93), the FCA must, without undue delay, publish on its official website information about the status of the appeal and its outcome. 4 Subject to paragraph (5), (6) and (9) where the FCA gives a final notice, it must, without undue delay, publish on its official website information on the type and nature of the breach and the identity of the person on whom the sanction or measure is imposed.

[money_laundering_regs_2017, regulation 84(9)-(11)]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 84(9)-(11) - Publication: the FCA
9 Information about a matter to which a final notice relates must not be published if publication in accordance with paragraph under paragraph (6) is considered by the FCA insufficient to ensure— a that the stability of the financial markets would not be put in jeopardy; or b that the publication of the information would be proportionate with regard to sanctions or measures which are considered by the FCA to be of a mino

</details>


---
## q19 (single)
**Question:** Can the FCA ask a payment institution applicant for more information after the application has been submitted?

**Reference:** Yes. Before determining the application it may require further information it reasonably considers necessary.

**Agent answer:** Yes. At any time after receiving an application and before determining it, the FCA may require the applicant to provide further information as it reasonably considers necessary to enable it to determine the application. This applies to applications for authorisation as a payment institution (as well as variations, small payment institution registrations, and account information service provider registrations).

[payment_services_regs_2017, regulation 5]
[payment_services_regs_2017, regulation 13]
[payment_services_regs_2017, regulation 17]

<details><summary>Retrieved text (excerpt)</summary>

[payment_services_regs_2017, regulation 5]
Payment Services Regulations 2017, regulation 5 - Application for authorisation as a payment institution or variation of an existing authorisation
5 1 An application for authorisation as a payment institution must contain or be accompanied by the information specified in Schedule 2 (information to be included in or with an application for authorisation). 2 An application for the variation of an authorisation as a payment institution must— a contain a statement of the proposed variation; b contain a statement of the payment services which the applicant proposes to carry on if the authorisation is varied; and c contain, or be accompanied by, such other information as the FCA may reasonably require. 3 An application under paragraph (1) or (2) must be made in such manner as the FCA may direct. 4 At any time after receiving an application and before determining it, the FCA may require the applicant to provide it with such further information as it reasonably considers necessary to enable it to determine the application. 5 Different directions may be given, and different requirements imposed, in relation to different applications or categories of application.

[payment_services_regs_2017, regulation 13]
Payment Services Regulations 2017, regulation 13 - Application for registration as a small payment institution or variation of an existing registration
13 1 An application for registration as a small payment institution must contain, or be accompanied by, such information as the FCA may reasonably require. 2 An application for the variation of a registration as a small payment institution must— a contain a statement of the proposed variation; b contain a statement of the payment services which the applicant proposes to carry on if the

</details>


---
## q20 (multi)
**Question:** If a small e-money institution stops meeting the conditions to stay small, how long does it have to apply for full authorisation, and what must that application contain?

**Reference:** Within 30 days of becoming aware (if it intends to keep issuing e-money in the UK); the application must contain the information specified in Schedule 1 and be made in the manner the FCA directs.

**Agent answer:** Under the Electronic Money Regulations 2011, if a small electronic money institution ceases to comply with the conditions to remain small and intends to continue issuing electronic money in the UK, it must apply to become an authorised electronic money institution within **30 days** of becoming aware of the change in circumstances [electronic_money_regs_2011, regulation 16].

The application must:
* Contain or be accompanied by the information specified in Schedule 1 [electronic_money_regs_2011, regulation 5(1)];
* Be made in the manner directed by the Authority [electronic_money_regs_2011, regulation 5(3)]; and
* Comply with the requirements of regulation 5 and any requirements imposed under regulation 20 [electronic_money_regs_2011, regulation 6(2)]. 

The Authority may also require the applicant to provide further information that it reasonably considers necessary to determine the application [electronic_money_regs_2011, regulation 5(4)].

<details><summary>Retrieved text (excerpt)</summary>

[electronic_money_regs_2011, regulation 16]
Electronic Money Regulations 2011, regulation 16 - Application for authorisation if requirements cease to be met
16 Where a small electronic money institution ceases to comply with a condition in regulation 13(3), (4), (8) or (9) , the institution concerned must, within 30 days of becoming aware of the change in circumstances, apply to become an authorised electronic money institution under regulation 5 if it intends to continue issuing electronic money in the United Kingdom.

[payment_services_regs_2017, regulation 16]
Payment Services Regulations 2017, regulation 16 - Application for authorisation or registration if requirements cease to be met
16 If a small payment institution no longer meets a condition in regulation 14(3), (5) or (10) (conditions for registration as small payment institution) or intends to provide services other than those permitted by regulation 32 (additional activities), the institution concerned must, within 30 days of becoming aware of the change in circumstances, apply for authorisation as a payment institution under regulation 5 or registration as an account information service provider under regulation 17, as appropriate, if it intends to continue providing payment services in the United Kingdom.

[electronic_money_regs_2011, regulation 13(1)-(6)]
Electronic Money Regulations 2011, regulation 13(1)-(6) - Conditions for registration
1 The Authority may refuse to register an applicant as a small electronic money institution only if any of the conditions set out in paragraphs (2) to (10) is not met. 2 The application must comply with the requirements of, and any requirements imposed under, regulations 12 and 20 . 3 The total business activities of the applicant immediately before the time of registra

</details>


---
## q21 (multi)
**Question:** Up to what point can a payer cancel a direct debit, and if the order reaches the bank on a non-business day, when is it treated as received?

**Reference:** The payer cannot revoke after the end of the business day before the day agreed for debiting; an order received on a non-business day is deemed received on the next business day.

**Agent answer:** For a direct debit, a payer cannot revoke the payment order after the end of the business day preceding the day agreed for debiting the funds (unless agreement is reached with the provider and the payee) `[payment_services_regs_2017, regulation 83]`. 

If the time of receipt of a payment order does not fall on a business day for the payer's payment service provider, the payment order is deemed to have been received on the first business day thereafter `[payment_services_regs_2017, regulation 81]`.

<details><summary>Retrieved text (excerpt)</summary>

[payment_services_regs_2017, regulation 83]
Payment Services Regulations 2017, regulation 83 - Revocation of a payment order
83 1 Subject to paragraphs (2) to (5), a payment service user may not revoke a payment order after it has been received by the payer's payment service provider. 2 In the case of a payment transaction initiated by a payment initiation service provider, or by or through the payee, the payer may not revoke the payment order after giving consent to the payment initiation service provider to initiate the payment transaction or giving consent to execute the payment transaction to the payee. 3 In the case of a direct debit, the payer may not revoke the payment order after the end of the business day preceding the day agreed for debiting the funds. 4 Where a day is agreed under regulation 81(5) (receipt of payment orders), the payment service user may not revoke a payment order after the end of the business day preceding the agreed day. 5 At any time after the time limits for revocation set out in paragraphs (1) to (4), the payment order may only be revoked if the revocation is— a agreed between the payment service user and the relevant payment service provider or providers; and b in the case of a payment transaction initiated by or through the payee, including in the case of a direct debit, also agreed with the payee. 6 A framework contract may provide for the relevant payment service provider to charge for revocation under this regulation.

[payment_services_regs_2017, regulation 81]
Payment Services Regulations 2017, regulation 81 - Receipt of payment orders
81 1 A payer's payment service provider must not debit the payment account before receipt of a payment order. 2 Subject to paragraphs (3) to (6), for the purposes of these Regulations the time of r

</details>


---
## q22 (multi)
**Question:** What risk profiles must a supervisory authority draw up, and what must a firm hand to its supervisor on request about its own risk assessment?

**Reference:** The authority must record a risk profile for each relevant person in its sector (it may share one profile between similar firms). A firm must provide its risk assessment, the information it was based on and its written record of steps taken.

**Agent answer:** A supervisory authority must develop and record in writing risk profiles for each relevant person in its own sector (or a single risk profile for a cluster of relevant persons sharing similar characteristics where risks do not significantly differ) [money_laundering_regs_2017, regulation 17(4)-(5)]. 

On request, a firm must provide its supervisor with:
* Its money laundering and terrorist financing risk assessment, the information on which it was based, and its written record of steps taken [money_laundering_regs_2017, regulation 18(6)]; and
* Its proliferation financing risk assessment, the information on which it was based, and its written record of steps taken [money_laundering_regs_2017, regulation 18A(5)].

<details><summary>Retrieved text (excerpt)</summary>

[money_laundering_regs_2017, regulation 17(1)-(5)]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 17(1)-(5) - Risk assessment by supervisory authorities
1 Each supervisory authority must identify and assess the international and domestic risks of money laundering and terrorist financing to which those relevant persons for which it is the supervisory authority (“its own sector”) are subject. 2 In carrying out the risk assessment required under paragraph (1), the supervisory authority must take into account— a . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . b . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . c the report prepared by the Treasury and the Home Office under regulation 16(6); and d information made available by the Treasury and the Home Office under regulation 16(8). 3 A supervisory authority must keep an up-to-date record in writing of all the steps it has taken under paragraph (1). 4 Each supervisory authority must develop and record in writing risk profiles for each relevant person in its own sector. 5 A supervisory authority may prepare a single risk profile under paragraph (4) in relation to two or more relevant persons in its sector, if— a the relevant persons share similar characteristics; and b the risks of money laundering and terrorist financing affecting those relevant persons do not differ significantly.

[money_laundering_regs_2017, regulation 17(6)-(9)]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 17(6)-(9) - Risk assessment by supervisory authorities
6 Where a supervisory authority has prepared a single risk profile for two or more relevant persons in its sector (a “cluster”), the supervisory authority must keep under review wheth

</details>


---
## q23 (multi)
**Question:** Who is responsible for the national proliferation financing risk assessment, and what must a firm do about its own proliferation financing controls?

**Reference:** The Treasury arranges the national assessment. A firm must establish and maintain proportionate policies, controls and procedures approved by senior management, review and update them, and keep a written record.

**Agent answer:** The Treasury is responsible for making arrangements for the national proliferation financing risk assessment and preparing a report on its findings [money_laundering_regs_2017, regulation 16A(1)-(4)].

Regarding its own proliferation financing controls, a firm must:
* Take appropriate steps (taking into account its size and nature) to identify and assess its proliferation financing risks, using the Treasury's report and specific risk factors (such as customers, countries, products, transactions, and delivery channels), keep a written record of these steps, and provide them to its supervisory authority on request [money_laundering_regs_2017, regulation 18A].
* Establish, maintain, regularly review, and update proportionate policies, controls, and procedures—approved by senior management—to effectively mitigate and manage those risks, including risk management practices, internal controls, monitoring, and specific measures for complex transactions, anonymity risks, and new products or technologies [money_laundering_regs_2017, regulation 19A(1)-(4)].
* Maintain written records of these policies, controls, procedures, changes, and internal communications, and communicate them to relevant foreign branches and subsidiaries [money_laundering_regs_2017, regulation 19A(1), (5)].

<details><summary>Retrieved text (excerpt)</summary>

[money_laundering_regs_2017, regulation 18A]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 18A - Risk assessment by relevant persons in relation to proliferation financing
18A 1 A relevant person must take appropriate steps to identify and assess the risks of proliferation financing to which its business is subject. 2 In carrying out the risk assessment required under paragraph (1), a relevant person must take into account— a information in the report referred to in regulation 16A (risk assessment by the Treasury); and b risk factors including factors relating to— i its customers; ii the countries or geographic areas in which it operates; iii its products or services; iv its transactions; and v its delivery channels. 3 In deciding what steps are appropriate under paragraph (1), the relevant person must take into account the size and nature of its business. 4 A relevant person must keep an up-to-date record in writing of all the steps it has taken under paragraph (1), unless its supervisory authority notifies it in writing that such a record is not required. 5 A relevant person must provide the risk assessment it has prepared under paragraph (1), the information on which that risk assessment was based and any record required to be kept under paragraph (4), to its supervisory authority on request.

[money_laundering_regs_2017, regulation 16A(1)-(8)]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 16A(1)-(8) - Risk assessment by the Treasury
1 The Treasury must make arrangements for a risk assessment to be undertaken to identify, assess, understand and mitigate the risks of proliferation financing affecting the United Kingdom (“the proliferation financing risk assessment”). 2 The proliferat

</details>


---
## q24 (multi)
**Question:** Which authority supervises authorised e-money institutions for the transfer-of-funds rules, and what does the register of authorised e-money institutions have to cover?

**Reference:** The FCA is their transfer of funds supervisory authority. The register covers authorised and small e-money institutions, notified persons, registered agents and the National Savings Bank when it issues e-money.

**Agent answer:** The FCA is the transfer of funds supervisory authority for authorised electronic money institutions [money_laundering_regs_2017, regulation 62]. 

The Authority must maintain a register of authorised electronic money institutions (among others), and may include on it any information it considers appropriate, provided the register identifies the electronic money issuance for which the institution is authorised or registered [electronic_money_regs_2011, regulation 4(1)-(5)].

<details><summary>Retrieved text (excerpt)</summary>

[money_laundering_regs_2017, regulation 62]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 62 - Transfer of funds supervisory authorities
62 1 The FCA is the transfer of funds supervisory authority for payment service providers, who are— a authorised persons; b authorised payment institutions under the Payment Services Regulations 2017 which are not included in the register maintained by the Commissioners under regulation 54(2); c registered small payment institutions under the Payment Services Regulations 2017 which are not included in the register maintained by the Commissioners under regulation 54(2); d authorised electronic money institutions under the Electronic Money Regulations 2011 ; or e registered small electronic money institutions under the Electronic Money Regulations 2011. 2 The Commissioners are the transfer of funds supervisory authority for payment service providers who do not come within paragraph (1).

[electronic_money_regs_2011, regulation 4(1)-(5)]
Electronic Money Regulations 2011, regulation 4(1)-(5) - The register of certain electronic money issuers
1 The Authority must maintain a register of— a authorised electronic money institutions ... b small electronic money institutions; ba persons who have notified the Authority in accordance with regulation 3A or 3B; c agents of electronic money institutions required to be registered under regulation 34; and d the National Savings Bank where it issues electronic money. 2 The Authority may include on the register any of the persons mentioned in paragraphs ... (e), (f) and (g) of the definition of electronic money issuer in regulation 2(1) where such persons issue electronic money. 3 Where a person mentioned in paragraph (e), (f), (g) or (j) of the definition of a

</details>


---
## q26 (unanswerable)
**Question:** What is the maximum amount allowed for a single contactless card payment in the UK without entering a PIN?

**Reference:** The corpus does not cover this; the assistant should say it does not know and not guess.

**Agent answer:** The corpus does not cover this.

<details><summary>Retrieved text (excerpt)</summary>

[money_laundering_regs_2017, regulation 38(1)-(4)]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 38(1)-(4) - Electronic money
1 Subject to paragraph (3), a relevant person is not required to apply customer due diligence measures in relation to electronic money, and regulations 27, 28, 30 and 33 to 37 do not apply provided that— a the maximum amount which can be stored electronically is £150 ; b the payment instrument used in connection with the electronic money (“the relevant payment instrument”) is— i not reloadable; or ii is subject to a maximum limit on monthly payment transactions of £150 which can only be used in the United Kingdom; c the relevant payment instrument is used exclusively to purchase goods or services; d anonymous electronic money cannot be used to fund the relevant payment instrument. 2 Paragraph (1) does not apply to any transaction which consists of the redemption in cash, or a cash withdrawal, of the monetary value of the electronic money, where— a the amount redeemed exceeds £50 ; or b in the case of remote payment transactions, the amount redeemed exceeds £50 per transaction. 3 The issuer of the relevant payment instrument must carry out sufficient monitoring of its business relationship with the users of electronic money and of transactions made using the relevant payment instrument to enable it to detect any unusual or suspicious transactions. 4 A relevant person is not prevented from applying simplified customer due diligence measures in relation to electronic money because the conditions set out in paragraph (1) are not satisfied, provided that such measures are permitted under regulation 37.

[payment_services_regs_2017, regulation 68(1)-(5)]
Payment Services Regulations 2017, regulation 68(1)-(5) 

</details>


---
## q27 (unanswerable)
**Question:** What is the current fee the FCA charges to apply for authorisation as a payment institution?

**Reference:** The corpus does not cover this; the assistant should say it does not know and not guess.

**Agent answer:** The corpus does not cover this. The search results discuss the application requirements and conditions for authorisation as a payment institution under the Payment Services Regulations 2017, but do not specify any FCA application fees.

<details><summary>Retrieved text (excerpt)</summary>

[payment_services_regs_2017, regulation 5]
Payment Services Regulations 2017, regulation 5 - Application for authorisation as a payment institution or variation of an existing authorisation
5 1 An application for authorisation as a payment institution must contain or be accompanied by the information specified in Schedule 2 (information to be included in or with an application for authorisation). 2 An application for the variation of an authorisation as a payment institution must— a contain a statement of the proposed variation; b contain a statement of the payment services which the applicant proposes to carry on if the authorisation is varied; and c contain, or be accompanied by, such other information as the FCA may reasonably require. 3 An application under paragraph (1) or (2) must be made in such manner as the FCA may direct. 4 At any time after receiving an application and before determining it, the FCA may require the applicant to provide it with such further information as it reasonably considers necessary to enable it to determine the application. 5 Different directions may be given, and different requirements imposed, in relation to different applications or categories of application.

[payment_services_regs_2017, regulation 6(1)-(6)]
Payment Services Regulations 2017, regulation 6(1)-(6) - Conditions for authorisation as a payment institution
1 The FCA may refuse to grant all or part of an application for authorisation as a payment institution only if any of the conditions set out in paragraphs (2) to (9) is not met. 2 The application must comply with the requirements of, and any requirements imposed under, regulations 5 (application for authorisation) and 20 (duty to notify changes). 3 The applicant must immediately before the time of authorisation hold the

</details>


---
## q28 (unanswerable)
**Question:** What is the Financial Ombudsman Service's compensation limit for a complaint about a payment services provider?

**Reference:** The corpus does not cover this; the assistant should say it does not know and not guess.

**Agent answer:** The corpus does not cover this. The regulations mention the ombudsman scheme established under Part 16 of the 2000 Act in relation to complaints [payment_services_regs_2017, regulation 117] and cryptoasset business disclosures [money_laundering_regs_2017, regulation 60A], but they do not state the Financial Ombudsman Service's compensation limit.

<details><summary>Retrieved text (excerpt)</summary>

[payment_services_regs_2017, regulation 117]
Payment Services Regulations 2017, regulation 117 - Complaints
117 1 The FCA must maintain arrangements designed to enable payment service users and other interested parties to submit complaints to it that— a a requirement imposed by or under Parts 2 to 7 of these Regulations has been breached by a payment service provider, or b a requirement imposed by or under section 312R of the 2000 Act has been breached by an authorised payment institution, small payment institution, or registered account information services provider. 2 Where it considers it appropriate, the FCA must include in any reply to a complaint under paragraph (1) details of the ombudsman scheme established under Part 16 of the 2000 Act (the ombudsman scheme).

[payment_services_regs_2017, regulation 101(1)-(7)]
Payment Services Regulations 2017, regulation 101(1)-(7) - Dispute resolution
1 This regulation applies in relation to complaints from payment service users who are not eligible within the meaning of section 226(6) of the 2000 Act (the ombudsman scheme – compulsory jurisdiction). 2 A payment service provider must put in place and apply adequate and effective complaint resolution procedures for the settlement of complaints from payment service users about the rights and obligations arising under Parts 6 and 7. 3 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4 When a payment service provider receives a complaint from a payment service user, the payment service provider must make every possible effort to address all points raised in a reply to the complaint on paper or, if agreed between payment service provider and payment service user, in another durable medium. 5 Subject to paragraph (6), the reply must be provided to the complainant wi

</details>


---
## q29 (unanswerable)
**Question:** What minimum prison sentence does the EU's sixth Anti-Money Laundering Directive require for money laundering offences?

**Reference:** The corpus does not cover this; the assistant should say it does not know and not guess.

**Agent answer:** The corpus does not cover this. The available documents cover the Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, the Payment Services Regulations 2017, and the Electronic Money Regulations 2011, but do not contain information on the EU's sixth Anti-Money Laundering Directive or its required minimum prison sentences for money laundering offences.

<details><summary>Retrieved text (excerpt)</summary>

[money_laundering_regs_2017, regulation 3(1)]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 3(1) - General interpretation
financial system for the purposes of money laundering or terrorist financing , as amended by Directive 2018/843 of the European Parliament and of the Council of 30th May 2018 ; “ FSMA ” means the Financial Services and Markets Act 2000 ; “ funds transfer regulation ” means Regulation 2015/847/EU of the European Parliament and of the Council of 20th May 2015 on information accompanying transfers of funds ; ... “ group ” has the meaning given by section 421 (group) of FSMA ; “ high value dealer ” has the meaning given by regulation 14(1)(a); “ independent legal professional ” has the meaning given by regulation 12(1); “ insolvency practitioner ” has the meaning given by regulation 11(b); “ law enforcement authority ” has the meaning given by regulation 44(10); “ letting agent ” has the meaning given by regulation 13(3); “ local weights and measures authority ” has the meaning given by section 69 of the Weights and Measures Act 1985 (local weights and measures authorities) ; “ manager ”, in relation to a firm, means a person who has control, authority or responsibility for managing the business of that firm, and includes a nominated officer; “ markets in financial instruments directive ” means Directive 2014/65/EU of the European Parliament and of the Council of 15th May 2014 on markets in financial instruments ; “ markets in financial instruments regulation ” means Regulation (EU) 600/2014 of the European Parliament and of the Council of 15 May 2014 on markets in financial instruments (as that Regulation forms part of domestic law under section 3 of the European Union (Withdrawal) Act 2018); “ money laundering

</details>


---
## q30 (unanswerable)
**Question:** For how many days must a bank freeze funds after receiving a designation under the Sanctions and Anti-Money Laundering Act 2018?

**Reference:** The corpus does not cover this; the assistant should say it does not know and not guess.

**Agent answer:** The corpus does not cover this.

<details><summary>Retrieved text (excerpt)</summary>

[money_laundering_regs_2017, regulation 45A]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 45A - Duty to establish mechanism for requests
45A . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[money_laundering_regs_2017, regulation 16A(10)]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 16A(10) - Risk assessment by the Treasury
means an obligation that the UK has by virtue of a resolution adopted by the Security Council of the United Nations which relates to the prevention, suppression and disruption of the proliferation of weapons of mass destruction and the financing of such; “ technology ” has the meaning given by paragraph 37 of Schedule 1 to the Sanctions and Anti-Money Laundering Act 2018.

[money_laundering_regs_2017, regulation 45D]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 45D - Requests for information about safe-deposit boxes
45D . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[money_laundering_regs_2017, regulation 16A(10)]
Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017, regulation 16A(10) - Risk assessment by the Treasury
10 In this regulation— “ biological weapon ” means a biological agent or toxin (within the meaning of section 1(1)(a) of the Biological Weapons Act 1974 ) in a form capable of use for hostile purposes or anything to which section 1(1)(b) of that Act applies; “ chemical weapon ” has the meaning given by section 1 of the Chemical Weapons Act 1996 ; “ CBRN-related goods and technology ” means technology (including dual-use technology) and dual-use goods used for non-legitimate purposes in connection with the matters referred to in paragraph (9); “ dual

</details>


---
## q31 (unanswerable)
**Question:** What capital must a bank hold against operational risk under the Basel III framework?

**Reference:** The corpus does not cover this; the assistant should say it does not know and not guess.

**Agent answer:** The corpus does not cover this. The corpus covers the Money Laundering Regulations 2017, the Payment Services Regulations 2017, and the Electronic Money Regulations 2011, none of which detail Basel III capital requirements for banks against operational risk.

<details><summary>Retrieved text (excerpt)</summary>

[payment_services_regs_2017, regulation 98]
Payment Services Regulations 2017, regulation 98 - Management of operational and security risks
98 1 Each payment service provider must establish a framework with appropriate mitigation measures and control mechanisms to manage the operational and security risks, relating to the payment services it provides. As part of that framework, the payment service provider must establish and maintain effective incident management procedures, including for the detection and classification of major operational and security incidents. 2 Each payment service provider must provide to the FCA an updated and comprehensive assessment of the operational and security risks relating to the payment services it provides and on the adequacy of the mitigation measures and control mechanisms implemented in response to those risks. 3 Such assessment must— a be provided on an annual basis, or at such shorter intervals as the FCA may direct; and b be provided in such form and manner, and contain such information, as the FCA may direct.

[payment_services_regs_2017, regulation 22]
Payment Services Regulations 2017, regulation 22 - Capital requirements
22 1 An authorised payment institution must maintain at all times own funds equal to or in excess of the greater of— a the amount of initial capital specified in Part 1 of Schedule 3 (capital requirements), or b in the case of an authorised payment institution which does not fall within paragraph (2), the amount of own funds calculated in accordance with Part 2 of Schedule 3. 2 An authorised payment institution falls within this paragraph if— a it does not offer payment services specified in paragraph 1(a) to (f) of Schedule 1 (payment services other than payment initiation services or account information ser

</details>
