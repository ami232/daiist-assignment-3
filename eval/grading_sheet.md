# Grading sheet

Grade at least 20 answers in `eval/human_labels.csv` (columns id, correct, supported, notes) BEFORE the judge runs.

- **correct** = 1 if the answer is right against the reference (or a proper refusal for an unanswerable question).
- **supported** = 1 if every claim in the answer is in the retrieved passages shown here.


---

## q01 (single)

**Question:** How quickly do we have to report a personal data breach to the data protection authority?

**Reference answer:** Without undue delay and, where feasible, within 72 hours of becoming aware of it, unless the breach is unlikely to result in a risk to individuals. If later than 72 hours, the notification must give reasons for the delay.

**Agent answer:**

In the case of a personal data breach, the controller shall notify the personal data protection authority without undue delay and, where feasible, not later than 72 hours after having become aware of it, unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. If the notification is not made within 72 hours, it must be accompanied by reasons for the delay.

(GDPR, Article 33)

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 33 - Notification of a personal data breach to the supervisory authority  (distance 0.223)
GDPR, Article 33: Notification of a personal data breach to the supervisory authority
1. In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority competent in accordance with Article 55, unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where the notification to the supervisory authority is not made within 72 hours, it shall be accompanied by reasons for the delay.
2. The processor shall notify the controller without undue delay after becoming aware of a personal data breach.
3. The notification referred to in paragraph 1 shall at least:
(a) describe the nature of the personal data breach including where possible, the categories and approximate number of data subjects concerned and the categories and approximate number of personal data records concerned;
(b) communicate the name and contact details of the data protection officer or other contact point where more information can be obtained;
(c) describe the likely consequences of the personal data breach;
(d) describe the measures taken or proposed to be taken by the controller to address the personal data breach, including, where appropriate, measures to mitigate its possible adverse effects.
4. Where, and in so far as, it is not possible to provide the information at the same time, the information may be provided in phases without undue further delay.
5. The controller shall document any personal data breaches, comprising the facts relating to the personal data breach, its effects and the remedial action taken. That documentation shall enable the supervisory authority to verify compliance with this Article.

---

[2] GDPR, Article 34 - Communication of a personal data breach to the data subject  (distance 0.277)
GDPR, Article 34: Communication of a personal data breach to the data subject
1. When the personal data breach is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall communicate the personal data breach to the data subject without undue delay.
2. The communication to the data subject referred to in paragraph 1 of this Article shall describe in clear and plain language the nature of the personal data breach and contain at least the information and measures referred to in points (b), (c) and (d) of Article 33(3).
3. The communication to the data subject referred to in paragraph 1 shall not be required if any of the following conditions are met:
(a) the controller has implemented appropriate technical and organisational protection measures, and those measures were applied to the personal data affected by the personal data breach, in particular those that render the personal data unintelligible to any person who is not authorised to access it, such as encryption;
(b) the controller has taken subsequent measures which ensure that the high risk to the rights and freedoms of data subjects referred to in paragraph 1 is no longer likely to materialise;
(c) it would involve disproportionate effort. In such a case, there shall instead be a public communication or similar measure whereby the data subjects are informed in an equally effective manner.
4. If the controller has not already communicated the personal data breach to the data subject, the supervisory authority, having considered the likelihood of the personal data breach resulting in a high risk, may require it to do so or may decide that any of the conditions referred to in paragraph 3 are met.

---

[3] GDPR, Article 66 - Urgency procedure  (distance 0.284)
GDPR, Article 66: Urgency procedure
1. In exceptional circumstances, where a supervisory authority concerned considers that there is an urgent need to act in order to protect the rights and freedoms of data subjects, it may, by way of derogation from the consistency mechanism referred to in Articles 63, 64 and 65 or the procedure referred to in Article 60, immediately adopt provisional measures intended to produce legal effects on its own territory with a specified period of validity which shall not exceed three months. The supervisory authority shall, without delay, communicate those measures and the reasons for adopting them to the other supervisory authorities concerned, to the Board and to the Commission.
2. Where a supervisory authority has taken a measure pursuant to paragraph 1 and considers that final measures need urgently be adopted, it may request an urgent opinion or an urgent binding decision from the Board, giving reasons for requesting such opinion or decision.
3. Any supervisory authority may request an urgent opinion or an urgent binding decision, as the case may be, from the Board where a competent supervisory authority has not taken an appropriate measure in a situation where there is an urgent need to act, in order to protect the rights and freedoms of data subjects, giving reasons for requesting such opinion or decision, including for the urgent need to act.
4. By derogation from Article 64(3) and Article 65(2), an urgent opinion or an urgent binding decision referred to in paragraphs 2 and 3 of this Article shall be adopted within two weeks by simple majority of the members of the Board.

---

[4] Data Act, Article 40 - Penalties  (distance 0.298)
Data Act, Article 40: Penalties
1. Member States shall lay down the rules on penalties applicable to infringements of this Regulation and shall take all measures necessary to ensure that they are implemented. The penalties provided for shall be effective, proportionate and dissuasive.
2. Member States shall by 12 September 2025 notify the Commission of those rules and measures and shall notify it without delay of any subsequent amendment affecting them. The Commission shall regularly update and maintain an easily accessible public register of those measures.
3. Member States shall take into account the recommendations of the EDIB and the following non-exhaustive criteria for the imposition of penalties for infringements of this Regulation:
(a) the nature, gravity, scale and duration of the infringement;
(b) any action taken by the infringing party to mitigate or remedy the damage caused by the infringement;
(c) any previous infringements by the infringing party;
(d) the financial benefits gained or losses avoided by the infringing party due to the infringement, insofar as such benefits or losses can be reliably established;
(e) any other aggravating or mitigating factor applicable to the circumstances of the case;
(f) infringing party’s annual turnover in the preceding financial year in the Union.
4. For infringements of the obligations laid down in Chapter II, III and V of this Regulation, the supervisory authorities responsible for monitoring the application of Regulation (EU) 2016/679 may within their scope of competence impose administrative fines in accordance with Article 83 of Regulation (EU) 2016/679 and up to the amount referred to in Article 83(5) of that Regulation.
5. For infringements of the obligations laid down in Chapter V of this Regulation, the European Data Protection Supervisor may impose within its scope of competence administrative fines in accordance with Article 66 of Regulation (EU) 2018/1725 up to the amount referred to in Article 66(3) of that Regulation.

---

[5] GDPR, Article 37 - Designation of the data protection officer  (distance 0.302)
GDPR, Article 37: Designation of the data protection officer
1. The controller and the processor shall designate a data protection officer in any case where:
(a) the processing is carried out by a public authority or body, except for courts acting in their judicial capacity;
(b) the core activities of the controller or the processor consist of processing operations which, by virtue of their nature, their scope and/or their purposes, require regular and systematic monitoring of data subjects on a large scale; or
(c) the core activities of the controller or the processor consist of processing on a large scale of special categories of data pursuant to Article 9 and personal data relating to criminal convictions and offences referred to in Article 10.
2. A group of undertakings may appoint a single data protection officer provided that a data protection officer is easily accessible from each establishment.
3. Where the controller or the processor is a public authority or body, a single data protection officer may be designated for several such authorities or bodies, taking account of their organisational structure and size.
4. In cases other than those referred to in paragraph 1, the controller or processor or associations and other bodies representing categories of controllers or processors may or, where required by Union or Member State law shall, designate a data protection officer. The data protection officer may act for such associations and other bodies representing controllers or processors.
5. The data protection officer shall be designated on the basis of professional qualities and, in particular, expert knowledge of data protection law and practices and the ability to fulfil the tasks referred to in Article 39.
6. The data protection officer may be a staff member of the controller or processor, or fulfil the tasks on the basis of a service contract.
7. The controller or the processor shall publish the contact details of the data protection officer and communicate them to the supervisory authority.
```
</details>


---

## q02 (single)

**Question:** At what age can a child give valid consent to an online service on their own?

**Reference answer:** At 16. Below 16 the consent must be given or authorised by the holder of parental responsibility. Member States may lower the age, but not below 13.

**Agent answer:**

In relation to the offer of information society services directly to a child, the processing of a child's personal data is lawful where the child is at least 16 years old. If the child is below the age of 16 years, the processing is lawful only if and to the extent that consent is given or authorised by the holder of parental responsibility over the child. 

However, Member States may provide by law for a lower age for those purposes, provided that such lower age is not below 13 years.

(GDPR, Article 8)

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 8 - Conditions applicable to child's consent in relation to information society services  (distance 0.224)
GDPR, Article 8: Conditions applicable to child's consent in relation to information society services
1. Where point (a) of Article 6(1) applies, in relation to the offer of information society services directly to a child, the processing of the personal data of a child shall be lawful where the child is at least 16 years old. Where the child is below the age of 16 years, such processing shall be lawful only if and to the extent that consent is given or authorised by the holder of parental responsibility over the child.
Member States may provide by law for a lower age for those purposes provided that such lower age is not below 13 years.
2. The controller shall make reasonable efforts to verify in such cases that consent is given or authorised by the holder of parental responsibility over the child, taking into consideration available technology.
3. Paragraph 1 shall not affect the general contract law of Member States such as the rules on the validity, formation or effect of a contract in relation to a child.

---

[2] GDPR, Article 7 - Conditions for consent  (distance 0.350)
GDPR, Article 7: Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data.
2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding.
3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.
4. When assessing whether consent is freely given, utmost account shall be taken of whether, inter alia , the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

---

[3] Data Governance Act, Article 25 - European data altruism consent form  (distance 0.361)
Data Governance Act, Article 25: European data altruism consent form
1. In order to facilitate the collection of data based on data altruism, the Commission shall adopt implementing acts establishing and developing a European data altruism consent form, after consulting the European Data Protection Board, taking into account the advice of the European Data Innovation Board and duly involving relevant stakeholders. The form shall allow the collection of consent or permission across Member States in a uniform format. Those implementing acts shall be adopted in accordance with the advisory procedure referred to in Article 33(2).
2. The European data altruism consent form shall use a modular approach allowing customisation for specific sectors and for different purposes.
3. Where personal data are provided, the European data altruism consent form shall ensure that data subjects are able to give consent to and withdraw consent from a specific data processing operation in compliance with the requirements of Regulation (EU) 2016/679.
4. The form shall be available in a manner that can be printed on paper and is easily understandable as well as in an electronic, machine-readable form.

---

[4] Data Governance Act, Article 21 - Specific requirements to safeguard rights and interests of data subjects and data holders with regard to their data  (distance 0.379)
Data Governance Act, Article 21: Specific requirements to safeguard rights and interests of data subjects and data holders with regard to their data
1. A recognised data altruism organisation shall inform data subjects or data holders prior to any processing of their data in a clear and easily comprehensible manner of:
(a) the objectives of general interest and, if applicable, the specified, explicit and legitimate purpose for which personal data is to be processed, and for which it permits the processing of their data by a data user;
(b) the location of and the objectives of general interest for which it permits any processing carried out in a third country, where the processing is carried out by the recognised data altruism organisation.
2. The recognised data altruism organisation shall not use the data for other objectives than those of general interest for which the data subject or data holder allows the processing. The recognised data altruism organisation shall not use misleading marketing practices to solicit the provision of data.
3. The recognised data altruism organisation shall provide tools for obtaining consent from data subjects or permissions to process data made available by data holders. The recognised data altruism organisation shall also provide tools for easy withdrawal of such consent or permission.
4. The recognised data altruism organisation shall take measures to ensure an appropriate level of security for the storage and processing of non-personal data that it has collected based on data altruism.
5. The recognised data altruism organisation shall, without delay, inform data holders in the event of any unauthorised transfer, access or use of the non-personal data that it has shared.
6. Where the recognised data altruism organisation facilitates data processing by third parties, including by providing tools for obtaining consent from data subjects or permissions to process data made available by data holders, it shall, where relevant, specify the third-country jurisdiction in which the data use is intended to take place.

---

[5] Data Governance Act, Article 7 - Competent bodies, part 2/2  (distance 0.382)
Data Governance Act, Article 7: Competent bodies
(d) assisting the public sector bodies, where relevant, to provide support to re-users in requesting consent for re-use from data subjects or permission from data holders in line with their specific decisions, including on the jurisdiction in which the data processing is intended to take place and assisting the public sector bodies in establishing technical mechanisms that allow the transmission of requests for consent or permission from re-users, where practically feasible;
(e) providing public sector bodies with assistance in assessing the adequacy of contractual commitments made by a re-user pursuant to Article 5(10).
5. Each Member State shall notify the Commission of the identity of the competent bodies designated pursuant to paragraph 1 by 24 September 2023. Each Member State shall also notify the Commission of any subsequent change to the identity of those competent bodies.
```
</details>


---

## q03 (single)

**Question:** Can a user withdraw their consent, and how easy does it have to be?

**Reference answer:** Yes, at any time. Withdrawal must be as easy as giving consent, and it does not affect the lawfulness of processing done before the withdrawal.

**Agent answer:**

Yes, a data subject has the right to withdraw their consent at any time. The withdrawal does not affect the lawfulness of processing that was based on consent before its withdrawal. 

Regarding how easy it has to be:
* It must be as easy to withdraw as to give consent.
* The data subject must be informed of this right prior to giving consent.

(GDPR, Article 7)

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 7 - Conditions for consent  (distance 0.215)
GDPR, Article 7: Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data.
2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding.
3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.
4. When assessing whether consent is freely given, utmost account shall be taken of whether, inter alia , the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

---

[2] Data Governance Act, Article 25 - European data altruism consent form  (distance 0.307)
Data Governance Act, Article 25: European data altruism consent form
1. In order to facilitate the collection of data based on data altruism, the Commission shall adopt implementing acts establishing and developing a European data altruism consent form, after consulting the European Data Protection Board, taking into account the advice of the European Data Innovation Board and duly involving relevant stakeholders. The form shall allow the collection of consent or permission across Member States in a uniform format. Those implementing acts shall be adopted in accordance with the advisory procedure referred to in Article 33(2).
2. The European data altruism consent form shall use a modular approach allowing customisation for specific sectors and for different purposes.
3. Where personal data are provided, the European data altruism consent form shall ensure that data subjects are able to give consent to and withdraw consent from a specific data processing operation in compliance with the requirements of Regulation (EU) 2016/679.
4. The form shall be available in a manner that can be printed on paper and is easily understandable as well as in an electronic, machine-readable form.

---

[3] GDPR, Article 8 - Conditions applicable to child's consent in relation to information society services  (distance 0.311)
GDPR, Article 8: Conditions applicable to child's consent in relation to information society services
1. Where point (a) of Article 6(1) applies, in relation to the offer of information society services directly to a child, the processing of the personal data of a child shall be lawful where the child is at least 16 years old. Where the child is below the age of 16 years, such processing shall be lawful only if and to the extent that consent is given or authorised by the holder of parental responsibility over the child.
Member States may provide by law for a lower age for those purposes provided that such lower age is not below 13 years.
2. The controller shall make reasonable efforts to verify in such cases that consent is given or authorised by the holder of parental responsibility over the child, taking into consideration available technology.
3. Paragraph 1 shall not affect the general contract law of Member States such as the rules on the validity, formation or effect of a contract in relation to a child.

---

[4] GDPR, Article 17 - Right to erasure (‘right to be forgotten’), part 1/2  (distance 0.315)
GDPR, Article 17: Right to erasure (‘right to be forgotten’)
1. The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay and the controller shall have the obligation to erase personal data without undue delay where one of the following grounds applies:
(a) the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed;
(b) the data subject withdraws consent on which the processing is based according to point (a) of Article 6(1), or point (a) of Article 9(2), and where there is no other legal ground for the processing;
(c) the data subject objects to the processing pursuant to Article 21(1) and there are no overriding legitimate grounds for the processing, or the data subject objects to the processing pursuant to Article 21(2);
(d) the personal data have been unlawfully processed;
(e) the personal data have to be erased for compliance with a legal obligation in Union or Member State law to which the controller is subject;
(f) the personal data have been collected in relation to the offer of information society services referred to in Article 8(1).
2. Where the controller has made the personal data public and is obliged pursuant to paragraph 1 to erase the personal data, the controller, taking account of available technology and the cost of implementation, shall take reasonable steps, including technical measures, to inform controllers which are processing the personal data that the data subject has requested the erasure by such controllers of any links to, or copy or replication of, those personal data.
3. Paragraphs 1 and 2 shall not apply to the extent that processing is necessary:
(a) for exercising the right of freedom of expression and information;
(b) for compliance with a legal obligation which requires processing by Union or Member State law to which the controller is subject or for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller;

---

[5] GDPR, Article 13 - Information to be provided where personal data are collected from the data subject, part 1/2  (distance 0.335)
GDPR, Article 13: Information to be provided where personal data are collected from the data subject
1. Where personal data relating to a data subject are collected from the data subject, the controller shall, at the time when personal data are obtained, provide the data subject with all of the following information:
(a) the identity and the contact details of the controller and, where applicable, of the controller's representative;
(b) the contact details of the data protection officer, where applicable;
(c) the purposes of the processing for which the personal data are intended as well as the legal basis for the processing;
(d) where the processing is based on point (f) of Article 6(1), the legitimate interests pursued by the controller or by a third party;
(e) the recipients or categories of recipients of the personal data, if any;
(f) where applicable, the fact that the controller intends to transfer personal data to a third country or international organisation and the existence or absence of an adequacy decision by the Commission, or in the case of transfers referred to in Article 46 or 47, or the second subparagraph of Article 49(1), reference to the appropriate or suitable safeguards and the means by which to obtain a copy of them or where they have been made available.
2. In addition to the information referred to in paragraph 1, the controller shall, at the time when personal data are obtained, provide the data subject with the following further information necessary to ensure fair and transparent processing:
(a) the period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period;
(b) the existence of the right to request from the controller access to and rectification or erasure of personal data or restriction of processing concerning the data subject or to object to processing as well as the right to data portability;
(c) where the processing is based on point (a) of Article 6(1) or point (a) of Article 9(2), the existence of the right to withdraw consent at any time, without affecting the lawfulness of processing based on consent before its withdrawal;
```
</details>


---

## q04 (single)

**Question:** How long do we have to answer a customer's request to access their data?

**Reference answer:** Without undue delay and in any event within one month of receiving the request. It can be extended by two further months for complex or numerous requests, and the person must be told of the extension and reasons within the first month.

**Agent answer:**

The controller shall provide information on action taken on a request to access personal data (under Article 15) without undue delay and in any event within one month of receipt of the request. 

That period may be extended by two further months where necessary, taking into account the complexity and number of the requests. The controller shall inform the data subject of any such extension within one month of receipt of the request, together with the reasons for the delay.

(GDPR, Article 12)

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 12 - Transparent information, communication and modalities for the exercise of the rights of the data subject, part 1/2  (distance 0.248)
GDPR, Article 12: Transparent information, communication and modalities for the exercise of the rights of the data subject
1. The controller shall take appropriate measures to provide any information referred to in Articles 13 and 14 and any communication under Articles 15 to 22 and 34 relating to processing to the data subject in a concise, transparent, intelligible and easily accessible form, using clear and plain language, in particular for any information addressed specifically to a child. The information shall be provided in writing, or by other means, including, where appropriate, by electronic means. When requested by the data subject, the information may be provided orally, provided that the identity of the data subject is proven by other means.
2. The controller shall facilitate the exercise of data subject rights under Articles 15 to 22. In the cases referred to in Article 11(2), the controller shall not refuse to act on the request of the data subject for exercising his or her rights under Articles 15 to 22, unless the controller demonstrates that it is not in a position to identify the data subject.
3. The controller shall provide information on action taken on a request under Articles 15 to 22 to the data subject without undue delay and in any event within one month of receipt of the request. That period may be extended by two further months where necessary, taking into account the complexity and number of the requests. The controller shall inform the data subject of any such extension within one month of receipt of the request, together with the reasons for the delay. Where the data subject makes the request by electronic form means, the information shall be provided by electronic means where possible, unless otherwise requested by the data subject.
4. If the controller does not take action on the request of the data subject, the controller shall inform the data subject without delay and at the latest within one month of receipt of the request of the reasons for not taking action and on the possibility of lodging a complaint with a supervisory authority and seeking a judicial remedy.

---

[2] GDPR, Article 15 - Right of access by the data subject  (distance 0.259)
GDPR, Article 15: Right of access by the data subject
1. The data subject shall have the right to obtain from the controller confirmation as to whether or not personal data concerning him or her are being processed, and, where that is the case, access to the personal data and the following information:
(a) the purposes of the processing;
(b) the categories of personal data concerned;
(c) the recipients or categories of recipient to whom the personal data have been or will be disclosed, in particular recipients in third countries or international organisations;
(d) where possible, the envisaged period for which the personal data will be stored, or, if not possible, the criteria used to determine that period;
(e) the existence of the right to request from the controller rectification or erasure of personal data or restriction of processing of personal data concerning the data subject or to object to such processing;
(f) the right to lodge a complaint with a supervisory authority;
(g) where the personal data are not collected from the data subject, any available information as to their source;
(h) the existence of automated decision-making, including profiling, referred to in Article 22(1) and (4) and, at least in those cases, meaningful information about the logic involved, as well as the significance and the envisaged consequences of such processing for the data subject.
2. Where personal data are transferred to a third country or to an international organisation, the data subject shall have the right to be informed of the appropriate safeguards pursuant to Article 46 relating to the transfer.
3. The controller shall provide a copy of the personal data undergoing processing. For any further copies requested by the data subject, the controller may charge a reasonable fee based on administrative costs. Where the data subject makes the request by electronic means, and unless otherwise requested by the data subject, the information shall be provided in a commonly used electronic form.
4. The right to obtain a copy referred to in paragraph 3 shall not adversely affect the rights and freedoms of others.

---

[3] Data Governance Act, Article 9 - Procedure for requests for re-use  (distance 0.273)
Data Governance Act, Article 9: Procedure for requests for re-use
1. Unless shorter time limits have been established in accordance with national law, the competent public sector bodies or the competent bodies referred to in Article 7(1) shall adopt a decision on the request for the re-use of the categories of data referred to in Article 3(1) within two months of the date of receipt of the request.
In the case of exceptionally extensive and complex requests for re-use, that two-month period may be extended by up to 30 days. In such cases the competent public sector bodies or the competent bodies referred to in Article 7(1) shall notify the applicant as soon as possible that more time is needed for conducting the procedure, together with the reasons for the delay.
2. Any natural or legal person directly affected by a decision as referred to in paragraph 1 shall have an effective right of redress in the Member State where the relevant body is located. Such a right of redress shall be laid down in national law and shall include the possibility of review by an impartial body with the appropriate expertise, such as the national competition authority, the relevant access-to-documents authority, the supervisory authority established in accordance with Regulation (EU) 2016/679 or a national judicial authority, whose decisions are binding upon the public sector body or the competent body concerned.

---

[4] Data Act, Article 18 - Compliance with requests for data, part 1/2  (distance 0.283)
Data Act, Article 18: Compliance with requests for data
1. A data holder receiving a request to make data available under this Chapter shall make the data available to the requesting public sector body, the Commission, the European Central Bank or a Union body without undue delay, taking into account necessary technical, organisational and legal measures.
2. Without prejudice to specific needs regarding the availability of data defined in Union or national law, a data holder may decline or seek the modification of a request to make data available under this Chapter without undue delay and, in any event, no later than five working days after the receipt of a request for the data necessary to respond to a public emergency and without undue delay and, in any event, no later than 30 working days after the receipt of such a request in other cases of an exceptional need, on any of the following grounds:
(a) the data holder does not have control over the data requested;
(b) a similar request for the same purpose has been previously submitted by another public sector body or the Commission, the European Central Bank or a Union body and the data holder has not been notified of the erasure of the data pursuant to Article 19(1), point (c);
(c) the request does not meet the conditions laid down in Article 17(1) and (2).
3. If the data holder decides to decline the request or to seek its modification in accordance with paragraph 2, point (b), it shall indicate the identity of the public sector body or the Commission, the European Central Bank or the Union body that previously submitted a request for the same purpose.
4. Where the data requested includes personal data, the data holder shall properly anonymise the data, unless the compliance with the request to make data available to a public sector body, the Commission, the European Central Bank or a Union body requires the disclosure of personal data. In such cases, the data holder shall pseudonymise the data.

---

[5] GDPR, Article 13 - Information to be provided where personal data are collected from the data subject, part 1/2  (distance 0.289)
GDPR, Article 13: Information to be provided where personal data are collected from the data subject
1. Where personal data relating to a data subject are collected from the data subject, the controller shall, at the time when personal data are obtained, provide the data subject with all of the following information:
(a) the identity and the contact details of the controller and, where applicable, of the controller's representative;
(b) the contact details of the data protection officer, where applicable;
(c) the purposes of the processing for which the personal data are intended as well as the legal basis for the processing;
(d) where the processing is based on point (f) of Article 6(1), the legitimate interests pursued by the controller or by a third party;
(e) the recipients or categories of recipients of the personal data, if any;
(f) where applicable, the fact that the controller intends to transfer personal data to a third country or international organisation and the existence or absence of an adequacy decision by the Commission, or in the case of transfers referred to in Article 46 or 47, or the second subparagraph of Article 49(1), reference to the appropriate or suitable safeguards and the means by which to obtain a copy of them or where they have been made available.
2. In addition to the information referred to in paragraph 1, the controller shall, at the time when personal data are obtained, provide the data subject with the following further information necessary to ensure fair and transparent processing:
(a) the period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period;
(b) the existence of the right to request from the controller access to and rectification or erasure of personal data or restriction of processing concerning the data subject or to object to processing as well as the right to data portability;
(c) where the processing is based on point (a) of Article 6(1) or point (a) of Article 9(2), the existence of the right to withdraw consent at any time, without affecting the lawfulness of processing based on consent before its withdrawal;
```
</details>


---

## q05 (single)

**Question:** When is a company required to appoint a data protection officer?

**Reference answer:** When it is a public authority (except courts), or its core activities require regular and systematic large-scale monitoring of individuals, or its core activities involve large-scale processing of special categories of data or criminal-conviction data.

**Agent answer:**

A controller or a processor is required to designate a data protection officer in any case where:
(a) the processing is carried out by a public authority or body, except for courts acting in their judicial capacity;
(b) the core activities of the controller or the processor consist of processing operations which, by virtue of their nature, their scope and/or their purposes, require regular and systematic monitoring of data subjects on a large scale; or
(c) the core activities of the controller or the processor consist of processing on a large scale of special categories of data pursuant to Article 9 and personal data relating to criminal convictions and offences referred to in Article 10.

In cases other than these, a controller, processor, or representative associations and other bodies may designate a data protection officer, or are required to do so where mandated by Union or Member State law.

(GDPR, Article 37)

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 37 - Designation of the data protection officer  (distance 0.187)
GDPR, Article 37: Designation of the data protection officer
1. The controller and the processor shall designate a data protection officer in any case where:
(a) the processing is carried out by a public authority or body, except for courts acting in their judicial capacity;
(b) the core activities of the controller or the processor consist of processing operations which, by virtue of their nature, their scope and/or their purposes, require regular and systematic monitoring of data subjects on a large scale; or
(c) the core activities of the controller or the processor consist of processing on a large scale of special categories of data pursuant to Article 9 and personal data relating to criminal convictions and offences referred to in Article 10.
2. A group of undertakings may appoint a single data protection officer provided that a data protection officer is easily accessible from each establishment.
3. Where the controller or the processor is a public authority or body, a single data protection officer may be designated for several such authorities or bodies, taking account of their organisational structure and size.
4. In cases other than those referred to in paragraph 1, the controller or processor or associations and other bodies representing categories of controllers or processors may or, where required by Union or Member State law shall, designate a data protection officer. The data protection officer may act for such associations and other bodies representing controllers or processors.
5. The data protection officer shall be designated on the basis of professional qualities and, in particular, expert knowledge of data protection law and practices and the ability to fulfil the tasks referred to in Article 39.
6. The data protection officer may be a staff member of the controller or processor, or fulfil the tasks on the basis of a service contract.
7. The controller or the processor shall publish the contact details of the data protection officer and communicate them to the supervisory authority.

---

[2] GDPR, Article 39 - Tasks of the data protection officer  (distance 0.250)
GDPR, Article 39: Tasks of the data protection officer
1. The data protection officer shall have at least the following tasks:
(a) to inform and advise the controller or the processor and the employees who carry out processing of their obligations pursuant to this Regulation and to other Union or Member State data protection provisions;
(b) to monitor compliance with this Regulation, with other Union or Member State data protection provisions and with the policies of the controller or processor in relation to the protection of personal data, including the assignment of responsibilities, awareness-raising and training of staff involved in processing operations, and the related audits;
(c) to provide advice where requested as regards the data protection impact assessment and monitor its performance pursuant to Article 35;
(d) to cooperate with the supervisory authority;
(e) to act as the contact point for the supervisory authority on issues relating to processing, including the prior consultation referred to in Article 36, and to consult, where appropriate, with regard to any other matter.
2. The data protection officer shall in the performance of his or her tasks have due regard to the risk associated with processing operations, taking into account the nature, scope, context and purposes of processing.

---

[3] GDPR, Article 38 - Position of the data protection officer  (distance 0.254)
GDPR, Article 38: Position of the data protection officer
1. The controller and the processor shall ensure that the data protection officer is involved, properly and in a timely manner, in all issues which relate to the protection of personal data.
2. The controller and processor shall support the data protection officer in performing the tasks referred to in Article 39 by providing resources necessary to carry out those tasks and access to personal data and processing operations, and to maintain his or her expert knowledge.
3. The controller and processor shall ensure that the data protection officer does not receive any instructions regarding the exercise of those tasks. He or she shall not be dismissed or penalised by the controller or the processor for performing his tasks. The data protection officer shall directly report to the highest management level of the controller or the processor.
4. Data subjects may contact the data protection officer with regard to all issues related to processing of their personal data and to the exercise of their rights under this Regulation.
5. The data protection officer shall be bound by secrecy or confidentiality concerning the performance of his or her tasks, in accordance with Union or Member State law.
6. The data protection officer may fulfil other tasks and duties. The controller or processor shall ensure that any such tasks and duties do not result in a conflict of interests.

---

[4] GDPR, Article 53 - General conditions for the members of the supervisory authority  (distance 0.285)
GDPR, Article 53: General conditions for the members of the supervisory authority
1. Member States shall provide for each member of their supervisory authorities to be appointed by means of a transparent procedure by:
— their parliament;
— their government;
— their head of State; or
— an independent body entrusted with the appointment under Member State law.
2. Each member shall have the qualifications, experience and skills, in particular in the area of the protection of personal data, required to perform its duties and exercise its powers.
3. The duties of a member shall end in the event of the expiry of the term of office, resignation or compulsory retirement, in accordance with the law of the Member State concerned.
4. A member shall be dismissed only in cases of serious misconduct or if the member no longer fulfils the conditions required for the performance of the duties.

---

[5] GDPR, Article 54 - Rules on the establishment of the supervisory authority  (distance 0.288)
GDPR, Article 54: Rules on the establishment of the supervisory authority
1. Each Member State shall provide by law for all of the following:
(a) the establishment of each supervisory authority;
(b) the qualifications and eligibility conditions required to be appointed as member of each supervisory authority;
(c) the rules and procedures for the appointment of the member or members of each supervisory authority;
(d) the duration of the term of the member or members of each supervisory authority of no less than four years, except for the first appointment after 24 May 2016, part of which may take place for a shorter period where that is necessary to protect the independence of the supervisory authority by means of a staggered appointment procedure;
(e) whether and, if so, for how many terms the member or members of each supervisory authority is eligible for reappointment;
(f) the conditions governing the obligations of the member or members and staff of each supervisory authority, prohibitions on actions, occupations and benefits incompatible therewith during and after the term of office and rules governing the cessation of employment.
2. The member or members and the staff of each supervisory authority shall, in accordance with Union or Member State law, be subject to a duty of professional secrecy both during and after their term of office, with regard to any confidential information which has come to their knowledge in the course of the performance of their tasks or exercise of their powers. During their term of office, that duty of professional secrecy shall in particular apply to reporting by natural persons of infringements of this Regulation.
```
</details>


---

## q06 (single)

**Question:** What is the maximum fine for breaching the basic principles of processing or the rules on consent?

**Reference answer:** Up to EUR 20 million or, for an undertaking, up to 4% of total worldwide annual turnover of the preceding financial year, whichever is higher.

**Agent answer:**

Infringements of the basic principles for processing, including conditions for consent pursuant to Articles 5, 6, 7, and 9, shall be subject to administrative fines up to 20 000 000 EUR, or in the case of an undertaking, up to 4 % of the total worldwide annual turnover of the preceding financial year, whichever is higher.

(GDPR, Article 83(5))

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 83 - General conditions for imposing administrative fines, part 2/3  (distance 0.170)
GDPR, Article 83: General conditions for imposing administrative fines
3. If a controller or processor intentionally or negligently, for the same or linked processing operations, infringes several provisions of this Regulation, the total amount of the administrative fine shall not exceed the amount specified for the gravest infringement.
4. Infringements of the following provisions shall, in accordance with paragraph 2, be subject to administrative fines up to 10 000 000 EUR, or in the case of an undertaking, up to 2 % of the total worldwide annual turnover of the preceding financial year, whichever is higher:
(a) the obligations of the controller and the processor pursuant to Articles 8, 11, 25 to 39 and 42 and 43;
(b) the obligations of the certification body pursuant to Articles 42 and 43;
(c) the obligations of the monitoring body pursuant to Article 41(4).
5. Infringements of the following provisions shall, in accordance with paragraph 2, be subject to administrative fines up to 20 000 000 EUR, or in the case of an undertaking, up to 4 % of the total worldwide annual turnover of the preceding financial year, whichever is higher:
(a) the basic principles for processing, including conditions for consent, pursuant to Articles 5, 6, 7 and 9;
(b) the data subjects' rights pursuant to Articles 12 to 22;
(c) the transfers of personal data to a recipient in a third country or an international organisation pursuant to Articles 44 to 49;
(d) any obligations pursuant to Member State law adopted under Chapter IX;
(e) non-compliance with an order or a temporary or definitive limitation on processing or the suspension of data flows by the supervisory authority pursuant to Article 58(2) or failure to provide access in violation of Article 58(1).
6. Non-compliance with an order by the supervisory authority as referred to in Article 58(2) shall, in accordance with paragraph 2 of this Article, be subject to administrative fines up to 20 000 000 EUR, or in the case of an undertaking, up to 4 % of the total worldwide annual turnover of the preceding financial year, whichever is higher.

---

[2] GDPR, Article 83 - General conditions for imposing administrative fines, part 1/3  (distance 0.186)
GDPR, Article 83: General conditions for imposing administrative fines
1. Each supervisory authority shall ensure that the imposition of administrative fines pursuant to this Article in respect of infringements of this Regulation referred to in paragraphs 4, 5 and 6 shall in each individual case be effective, proportionate and dissuasive.
2. Administrative fines shall, depending on the circumstances of each individual case, be imposed in addition to, or instead of, measures referred to in points (a) to (h) and (j) of Article 58(2). When deciding whether to impose an administrative fine and deciding on the amount of the administrative fine in each individual case due regard shall be given to the following:
(a) the nature, gravity and duration of the infringement taking into account the nature scope or purpose of the processing concerned as well as the number of data subjects affected and the level of damage suffered by them;
(b) the intentional or negligent character of the infringement;
(c) any action taken by the controller or processor to mitigate the damage suffered by data subjects;
(d) the degree of responsibility of the controller or processor taking into account technical and organisational measures implemented by them pursuant to Articles 25 and 32;
(e) any relevant previous infringements by the controller or processor;
(f) the degree of cooperation with the supervisory authority, in order to remedy the infringement and mitigate the possible adverse effects of the infringement;
(g) the categories of personal data affected by the infringement;
(h) the manner in which the infringement became known to the supervisory authority, in particular whether, and if so to what extent, the controller or processor notified the infringement;
(i) where measures referred to in Article 58(2) have previously been ordered against the controller or processor concerned with regard to the same subject-matter, compliance with those measures;
(j) adherence to approved codes of conduct pursuant to Article 40 or approved certification mechanisms pursuant to Article 42; and
(k) any other aggravating or mitigating factor applicable to the circumstances of the case, such as financial benefits gained, or losses avoided, directly or indirectly, from the infringement.

---

[3] GDPR, Article 83 - General conditions for imposing administrative fines, part 3/3  (distance 0.235)
GDPR, Article 83: General conditions for imposing administrative fines
7. Without prejudice to the corrective powers of supervisory authorities pursuant to Article 58(2), each Member State may lay down the rules on whether and to what extent administrative fines may be imposed on public authorities and bodies established in that Member State.
8. The exercise by the supervisory authority of its powers under this Article shall be subject to appropriate procedural safeguards in accordance with Union and Member State law, including effective judicial remedy and due process.
9. Where the legal system of the Member State does not provide for administrative fines, this Article may be applied in such a manner that the fine is initiated by the competent supervisory authority and imposed by competent national courts, while ensuring that those legal remedies are effective and have an equivalent effect to the administrative fines imposed by supervisory authorities. In any event, the fines imposed shall be effective, proportionate and dissuasive. Those Member States shall notify to the Commission the provisions of their laws which they adopt pursuant to this paragraph by 25 May 2018 and, without delay, any subsequent amendment law or amendment affecting them.

---

[4] GDPR, Article 84 - Penalties  (distance 0.258)
GDPR, Article 84: Penalties
1. Member States shall lay down the rules on other penalties applicable to infringements of this Regulation in particular for infringements which are not subject to administrative fines pursuant to Article 83, and shall take all measures necessary to ensure that they are implemented. Such penalties shall be effective, proportionate and dissuasive.
2. Each Member State shall notify to the Commission the provisions of its law which it adopts pursuant to paragraph 1, by 25 May 2018 and, without delay, any subsequent amendment affecting them.

---

[5] GDPR, Article 82 - Right to compensation and liability  (distance 0.262)
GDPR, Article 82: Right to compensation and liability
1. Any person who has suffered material or non-material damage as a result of an infringement of this Regulation shall have the right to receive compensation from the controller or processor for the damage suffered.
2. Any controller involved in processing shall be liable for the damage caused by processing which infringes this Regulation. A processor shall be liable for the damage caused by processing only where it has not complied with obligations of this Regulation specifically directed to processors or where it has acted outside or contrary to lawful instructions of the controller.
3. A controller or processor shall be exempt from liability under paragraph 2 if it proves that it is not in any way responsible for the event giving rise to the damage.
4. Where more than one controller or processor, or both a controller and a processor, are involved in the same processing and where they are, under paragraphs 2 and 3, responsible for any damage caused by processing, each controller or processor shall be held liable for the entire damage in order to ensure effective compensation of the data subject.
5. Where a controller or processor has, in accordance with paragraph 4, paid full compensation for the damage suffered, that controller or processor shall be entitled to claim back from the other controllers or processors involved in the same processing that part of the compensation corresponding to their part of responsibility for the damage, in accordance with the conditions set out in paragraph 2.
6. Court proceedings for exercising the right to receive compensation shall be brought before the courts competent under the law of the Member State referred to in Article 79(2).
```
</details>


---

## q07 (single)

**Question:** In which cases is a data protection impact assessment mandatory?

**Reference answer:** In particular for systematic and extensive profiling-based evaluation that produces legal or similarly significant effects, large-scale processing of special categories or criminal-offence data, and large-scale systematic monitoring of a publicly accessible area.

**Agent answer:**

A data protection impact assessment is mandatory prior to processing where a type of processing—in particular using new technologies, and taking into account the nature, scope, context, and purposes of the processing—is likely to result in a high risk to the rights and freedoms of natural persons (GDPR, Article 35(1)). 

Specifically, it is required in the case of:
(a) a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person;
(b) processing on a large scale of special categories of data referred to in Article 9(1), or of personal data relating to criminal convictions and offences referred to in Article 10; or
(c) a systematic monitoring of a publicly accessible area on a large scale (GDPR, Article 35(3)).

Supervisory authorities also establish, make public, and communicate lists of the kinds of processing operations that are subject to the requirement for a data protection impact assessment (GDPR, Article 35(4)).

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 35 - Data protection impact assessment, part 1/3  (distance 0.194)
GDPR, Article 35: Data protection impact assessment
1. Where a type of processing in particular using new technologies, and taking into account the nature, scope, context and purposes of the processing, is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall, prior to the processing, carry out an assessment of the impact of the envisaged processing operations on the protection of personal data. A single assessment may address a set of similar processing operations that present similar high risks.
2. The controller shall seek the advice of the data protection officer, where designated, when carrying out a data protection impact assessment.
3. A data protection impact assessment referred to in paragraph 1 shall in particular be required in the case of:
(a) a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person;
(b) processing on a large scale of special categories of data referred to in Article 9(1), or of personal data relating to criminal convictions and offences referred to in Article 10; or
(c) a systematic monitoring of a publicly accessible area on a large scale.
4. The supervisory authority shall establish and make public a list of the kind of processing operations which are subject to the requirement for a data protection impact assessment pursuant to paragraph 1. The supervisory authority shall communicate those lists to the Board referred to in Article 68.
5. The supervisory authority may also establish and make public a list of the kind of processing operations for which no data protection impact assessment is required. The supervisory authority shall communicate those lists to the Board.

---

[2] GDPR, Article 35 - Data protection impact assessment, part 2/3  (distance 0.228)
GDPR, Article 35: Data protection impact assessment
6. Prior to the adoption of the lists referred to in paragraphs 4 and 5, the competent supervisory authority shall apply the consistency mechanism referred to in Article 63 where such lists involve processing activities which are related to the offering of goods or services to data subjects or to the monitoring of their behaviour in several Member States, or may substantially affect the free movement of personal data within the Union.
7. The assessment shall contain at least:
(a) a systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitimate interest pursued by the controller;
(b) an assessment of the necessity and proportionality of the processing operations in relation to the purposes;
(c) an assessment of the risks to the rights and freedoms of data subjects referred to in paragraph 1; and
(d) the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned.
8. Compliance with approved codes of conduct referred to in Article 40 by the relevant controllers or processors shall be taken into due account in assessing the impact of the processing operations performed by such controllers or processors, in particular for the purposes of a data protection impact assessment.
9. Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to the protection of commercial or public interests or the security of processing operations.

---

[3] GDPR, Article 35 - Data protection impact assessment, part 3/3  (distance 0.242)
GDPR, Article 35: Data protection impact assessment
10. Where processing pursuant to point (c) or (e) of Article 6(1) has a legal basis in Union law or in the law of the Member State to which the controller is subject, that law regulates the specific processing operation or set of operations in question, and a data protection impact assessment has already been carried out as part of a general impact assessment in the context of the adoption of that legal basis, paragraphs 1 to 7 shall not apply unless Member States deem it to be necessary to carry out such an assessment prior to processing activities.
11. Where necessary, the controller shall carry out a review to assess if processing is performed in accordance with the data protection impact assessment at least when there is a change of the risk represented by processing operations.

---

[4] GDPR, Article 36 - Prior consultation, part 1/2  (distance 0.255)
GDPR, Article 36: Prior consultation
1. The controller shall consult the supervisory authority prior to processing where a data protection impact assessment under Article 35 indicates that the processing would result in a high risk in the absence of measures taken by the controller to mitigate the risk.
2. Where the supervisory authority is of the opinion that the intended processing referred to in paragraph 1 would infringe this Regulation, in particular where the controller has insufficiently identified or mitigated the risk, the supervisory authority shall, within period of up to eight weeks of receipt of the request for consultation, provide written advice to the controller and, where applicable to the processor, and may use any of its powers referred to in Article 58. That period may be extended by six weeks, taking into account the complexity of the intended processing. The supervisory authority shall inform the controller and, where applicable, the processor, of any such extension within one month of receipt of the request for consultation together with the reasons for the delay. Those periods may be suspended until the supervisory authority has obtained information it has requested for the purposes of the consultation.
3. When consulting the supervisory authority pursuant to paragraph 1, the controller shall provide the supervisory authority with:
(a) where applicable, the respective responsibilities of the controller, joint controllers and processors involved in the processing, in particular for processing within a group of undertakings;
(b) the purposes and means of the intended processing;
(c) the measures and safeguards provided to protect the rights and freedoms of data subjects pursuant to this Regulation;
(d) where applicable, the contact details of the data protection officer;
(e) the data protection impact assessment provided for in Article 35; and
(f) any other information requested by the supervisory authority.
4. Member States shall consult the supervisory authority during the preparation of a proposal for a legislative measure to be adopted by a national parliament, or of a regulatory measure based on such a legislative measure, which relates to processing.

---

[5] GDPR, Article 37 - Designation of the data protection officer  (distance 0.267)
GDPR, Article 37: Designation of the data protection officer
1. The controller and the processor shall designate a data protection officer in any case where:
(a) the processing is carried out by a public authority or body, except for courts acting in their judicial capacity;
(b) the core activities of the controller or the processor consist of processing operations which, by virtue of their nature, their scope and/or their purposes, require regular and systematic monitoring of data subjects on a large scale; or
(c) the core activities of the controller or the processor consist of processing on a large scale of special categories of data pursuant to Article 9 and personal data relating to criminal convictions and offences referred to in Article 10.
2. A group of undertakings may appoint a single data protection officer provided that a data protection officer is easily accessible from each establishment.
3. Where the controller or the processor is a public authority or body, a single data protection officer may be designated for several such authorities or bodies, taking account of their organisational structure and size.
4. In cases other than those referred to in paragraph 1, the controller or processor or associations and other bodies representing categories of controllers or processors may or, where required by Union or Member State law shall, designate a data protection officer. The data protection officer may act for such associations and other bodies representing controllers or processors.
5. The data protection officer shall be designated on the basis of professional qualities and, in particular, expert knowledge of data protection law and practices and the ability to fulfil the tasks referred to in Article 39.
6. The data protection officer may be a staff member of the controller or processor, or fulfil the tasks on the basis of a service contract.
7. The controller or the processor shall publish the contact details of the data protection officer and communicate them to the supervisory authority.
```
</details>


---

## q08 (single)

**Question:** When can a person demand that their personal data be erased?

**Reference answer:** When the data are no longer necessary for their purposes, consent is withdrawn and there is no other legal ground, the person objects and there are no overriding grounds, the data were unlawfully processed, erasure is required by law, or the data were collected from a child for online services.

**Agent answer:**

A data subject has the right to obtain from the controller the erasure of personal data concerning them without undue delay where one of the following grounds applies:

(a) the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed;
(b) the data subject withdraws consent on which the processing is based according to point (a) of Article 6(1), or point (a) of Article 9(2), and where there is no other legal ground for the processing;
(c) the data subject objects to the processing pursuant to Article 21(1) and there are no overriding legitimate grounds for the processing, or the data subject objects to the processing pursuant to Article 21(2);
(d) the personal data have been unlawfully processed;
(e) the personal data have to be erased for compliance with a legal obligation in Union or Member State law to which the controller is subject;
(f) the personal data have been collected in relation to the offer of information society services referred to in Article 8(1).

These rights to erasure do not apply to the extent that processing is necessary for exercising freedom of expression and information; for compliance with a legal obligation, public interest tasks, or official authority; for public health reasons in the area of public health; for archiving purposes in the public interest, scientific or historical research, or statistical purposes; or for the establishment, exercise, or defence of legal claims.

(GDPR, Article 17)

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 17 - Right to erasure (‘right to be forgotten’), part 1/2  (distance 0.212)
GDPR, Article 17: Right to erasure (‘right to be forgotten’)
1. The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay and the controller shall have the obligation to erase personal data without undue delay where one of the following grounds applies:
(a) the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed;
(b) the data subject withdraws consent on which the processing is based according to point (a) of Article 6(1), or point (a) of Article 9(2), and where there is no other legal ground for the processing;
(c) the data subject objects to the processing pursuant to Article 21(1) and there are no overriding legitimate grounds for the processing, or the data subject objects to the processing pursuant to Article 21(2);
(d) the personal data have been unlawfully processed;
(e) the personal data have to be erased for compliance with a legal obligation in Union or Member State law to which the controller is subject;
(f) the personal data have been collected in relation to the offer of information society services referred to in Article 8(1).
2. Where the controller has made the personal data public and is obliged pursuant to paragraph 1 to erase the personal data, the controller, taking account of available technology and the cost of implementation, shall take reasonable steps, including technical measures, to inform controllers which are processing the personal data that the data subject has requested the erasure by such controllers of any links to, or copy or replication of, those personal data.
3. Paragraphs 1 and 2 shall not apply to the extent that processing is necessary:
(a) for exercising the right of freedom of expression and information;
(b) for compliance with a legal obligation which requires processing by Union or Member State law to which the controller is subject or for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller;

---

[2] GDPR, Article 17 - Right to erasure (‘right to be forgotten’), part 2/2  (distance 0.254)
GDPR, Article 17: Right to erasure (‘right to be forgotten’)
(c) for reasons of public interest in the area of public health in accordance with points (h) and (i) of Article 9(2) as well as Article 9(3);
(d) for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) in so far as the right referred to in paragraph 1 is likely to render impossible or seriously impair the achievement of the objectives of that processing; or
(e) for the establishment, exercise or defence of legal claims.

---

[3] GDPR, Article 21 - Right to object  (distance 0.302)
GDPR, Article 21: Right to object
1. The data subject shall have the right to object, on grounds relating to his or her particular situation, at any time to processing of personal data concerning him or her which is based on point (e) or (f) of Article 6(1), including profiling based on those provisions. The controller shall no longer process the personal data unless the controller demonstrates compelling legitimate grounds for the processing which override the interests, rights and freedoms of the data subject or for the establishment, exercise or defence of legal claims.
2. Where personal data are processed for direct marketing purposes, the data subject shall have the right to object at any time to processing of personal data concerning him or her for such marketing, which includes profiling to the extent that it is related to such direct marketing.
3. Where the data subject objects to processing for direct marketing purposes, the personal data shall no longer be processed for such purposes.
4. At the latest at the time of the first communication with the data subject, the right referred to in paragraphs 1 and 2 shall be explicitly brought to the attention of the data subject and shall be presented clearly and separately from any other information.
5. In the context of the use of information society services, and notwithstanding Directive 2002/58/EC, the data subject may exercise his or her right to object by automated means using technical specifications.
6. Where personal data are processed for scientific or historical research purposes or statistical purposes pursuant to Article 89(1), the data subject, on grounds relating to his or her particular situation, shall have the right to object to processing of personal data concerning him or her, unless the processing is necessary for the performance of a task carried out for reasons of public interest.

---

[4] Data Act, Article 19 - Obligations of public sector bodies, the Commission, the European Central Bank and Union bodies, part 1/2  (distance 0.303)
Data Act, Article 19: Obligations of public sector bodies, the Commission, the European Central Bank and Union bodies
1. A public sector body, the Commission, the European Central Bank or a Union body receiving data pursuant to a request made under Article 14 shall:
(a) not use the data in a manner incompatible with the purpose for which they were requested;
(b) have implemented technical and organisational measures that preserve the confidentiality and integrity of the requested data and the security of the data transfers, in particular personal data, and safeguard the rights and freedoms of data subjects;
(c) erase the data as soon as they are no longer necessary for the stated purpose and inform the data holder and individuals or organisations that received the data pursuant to Article 21(1) without undue delay that the data have been erased, unless archiving of the data is required in accordance with Union or national law on public access to documents in the context of transparency obligations.
2. A public sector body, the Commission, the European Central Bank, a Union body or a third party receiving data under this Chapter shall not:
(a) use the data or insights about the economic situation, assets and production or operation methods of the data holder to develop or enhance a connected product or related service that competes with the connected product or related service of the data holder;
(b) share the data with another third party for any of the purposes referred to in point (a).

---

[5] GDPR, Article 15 - Right of access by the data subject  (distance 0.304)
GDPR, Article 15: Right of access by the data subject
1. The data subject shall have the right to obtain from the controller confirmation as to whether or not personal data concerning him or her are being processed, and, where that is the case, access to the personal data and the following information:
(a) the purposes of the processing;
(b) the categories of personal data concerned;
(c) the recipients or categories of recipient to whom the personal data have been or will be disclosed, in particular recipients in third countries or international organisations;
(d) where possible, the envisaged period for which the personal data will be stored, or, if not possible, the criteria used to determine that period;
(e) the existence of the right to request from the controller rectification or erasure of personal data or restriction of processing of personal data concerning the data subject or to object to such processing;
(f) the right to lodge a complaint with a supervisory authority;
(g) where the personal data are not collected from the data subject, any available information as to their source;
(h) the existence of automated decision-making, including profiling, referred to in Article 22(1) and (4) and, at least in those cases, meaningful information about the logic involved, as well as the significance and the envisaged consequences of such processing for the data subject.
2. Where personal data are transferred to a third country or to an international organisation, the data subject shall have the right to be informed of the appropriate safeguards pursuant to Article 46 relating to the transfer.
3. The controller shall provide a copy of the personal data undergoing processing. For any further copies requested by the data subject, the controller may charge a reasonable fee based on administrative costs. Where the data subject makes the request by electronic means, and unless otherwise requested by the data subject, the information shall be provided in a commonly used electronic form.
4. The right to obtain a copy referred to in paragraph 3 shall not adversely affect the rights and freedoms of others.
```
</details>


---

## q09 (single)

**Question:** Do we always have to tell the affected individuals about a data breach?

**Reference answer:** Only if the breach is likely to result in a high risk to them. It is not required if the data were protected (e.g. encrypted), later measures removed the high risk, or it would take disproportionate effort (then a public communication is needed instead).

**Agent answer:**

No. Communication to the data subject is required when the personal data breach is likely to result in a high risk to the rights and freedoms of natural persons, and it must be done without undue delay. 

However, the communication is not required if any of the following conditions are met:
(a) the controller has implemented appropriate technical and organisational protection measures, and those measures were applied to the personal data affected by the breach, in particular those that render the personal data unintelligible to any person who is not authorised to access it, such as encryption;
(b) the controller has taken subsequent measures which ensure that the high risk to the rights and freedoms of data subjects is no longer likely to materialise;
(c) it would involve disproportionate effort, in which case there shall instead be a public communication or similar measure whereby the data subjects are informed in an equally effective manner.

Additionally, the supervisory authority may require the controller to communicate the breach to the data subject, or decide that one of the above conditions is met, having considered the likelihood of the breach resulting in a high risk.

(GDPR, Article 34)

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 34 - Communication of a personal data breach to the data subject  (distance 0.190)
GDPR, Article 34: Communication of a personal data breach to the data subject
1. When the personal data breach is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall communicate the personal data breach to the data subject without undue delay.
2. The communication to the data subject referred to in paragraph 1 of this Article shall describe in clear and plain language the nature of the personal data breach and contain at least the information and measures referred to in points (b), (c) and (d) of Article 33(3).
3. The communication to the data subject referred to in paragraph 1 shall not be required if any of the following conditions are met:
(a) the controller has implemented appropriate technical and organisational protection measures, and those measures were applied to the personal data affected by the personal data breach, in particular those that render the personal data unintelligible to any person who is not authorised to access it, such as encryption;
(b) the controller has taken subsequent measures which ensure that the high risk to the rights and freedoms of data subjects referred to in paragraph 1 is no longer likely to materialise;
(c) it would involve disproportionate effort. In such a case, there shall instead be a public communication or similar measure whereby the data subjects are informed in an equally effective manner.
4. If the controller has not already communicated the personal data breach to the data subject, the supervisory authority, having considered the likelihood of the personal data breach resulting in a high risk, may require it to do so or may decide that any of the conditions referred to in paragraph 3 are met.

---

[2] GDPR, Article 33 - Notification of a personal data breach to the supervisory authority  (distance 0.222)
GDPR, Article 33: Notification of a personal data breach to the supervisory authority
1. In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority competent in accordance with Article 55, unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where the notification to the supervisory authority is not made within 72 hours, it shall be accompanied by reasons for the delay.
2. The processor shall notify the controller without undue delay after becoming aware of a personal data breach.
3. The notification referred to in paragraph 1 shall at least:
(a) describe the nature of the personal data breach including where possible, the categories and approximate number of data subjects concerned and the categories and approximate number of personal data records concerned;
(b) communicate the name and contact details of the data protection officer or other contact point where more information can be obtained;
(c) describe the likely consequences of the personal data breach;
(d) describe the measures taken or proposed to be taken by the controller to address the personal data breach, including, where appropriate, measures to mitigate its possible adverse effects.
4. Where, and in so far as, it is not possible to provide the information at the same time, the information may be provided in phases without undue further delay.
5. The controller shall document any personal data breaches, comprising the facts relating to the personal data breach, its effects and the remedial action taken. That documentation shall enable the supervisory authority to verify compliance with this Article.

---

[3] GDPR, Article 77 - Right to lodge a complaint with a supervisory authority  (distance 0.285)
GDPR, Article 77: Right to lodge a complaint with a supervisory authority
1. Without prejudice to any other administrative or judicial remedy, every data subject shall have the right to lodge a complaint with a supervisory authority, in particular in the Member State of his or her habitual residence, place of work or place of the alleged infringement if the data subject considers that the processing of personal data relating to him or her infringes this Regulation.
2. The supervisory authority with which the complaint has been lodged shall inform the complainant on the progress and the outcome of the complaint including the possibility of a judicial remedy pursuant to Article 78.

---

[4] GDPR, Article 82 - Right to compensation and liability  (distance 0.292)
GDPR, Article 82: Right to compensation and liability
1. Any person who has suffered material or non-material damage as a result of an infringement of this Regulation shall have the right to receive compensation from the controller or processor for the damage suffered.
2. Any controller involved in processing shall be liable for the damage caused by processing which infringes this Regulation. A processor shall be liable for the damage caused by processing only where it has not complied with obligations of this Regulation specifically directed to processors or where it has acted outside or contrary to lawful instructions of the controller.
3. A controller or processor shall be exempt from liability under paragraph 2 if it proves that it is not in any way responsible for the event giving rise to the damage.
4. Where more than one controller or processor, or both a controller and a processor, are involved in the same processing and where they are, under paragraphs 2 and 3, responsible for any damage caused by processing, each controller or processor shall be held liable for the entire damage in order to ensure effective compensation of the data subject.
5. Where a controller or processor has, in accordance with paragraph 4, paid full compensation for the damage suffered, that controller or processor shall be entitled to claim back from the other controllers or processors involved in the same processing that part of the compensation corresponding to their part of responsibility for the damage, in accordance with the conditions set out in paragraph 2.
6. Court proceedings for exercising the right to receive compensation shall be brought before the courts competent under the law of the Member State referred to in Article 79(2).

---

[5] GDPR, Article 32 - Security of processing  (distance 0.298)
GDPR, Article 32: Security of processing
1. Taking into account the state of the art, the costs of implementation and the nature, scope, context and purposes of processing as well as the risk of varying likelihood and severity for the rights and freedoms of natural persons, the controller and the processor shall implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk, including inter alia as appropriate:
(a) the pseudonymisation and encryption of personal data;
(b) the ability to ensure the ongoing confidentiality, integrity, availability and resilience of processing systems and services;
(c) the ability to restore the availability and access to personal data in a timely manner in the event of a physical or technical incident;
(d) a process for regularly testing, assessing and evaluating the effectiveness of technical and organisational measures for ensuring the security of the processing.
2. In assessing the appropriate level of security account shall be taken in particular of the risks that are presented by processing, in particular from accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to personal data transmitted, stored or otherwise processed.
3. Adherence to an approved code of conduct as referred to in Article 40 or an approved certification mechanism as referred to in Article 42 may be used as an element by which to demonstrate compliance with the requirements set out in paragraph 1 of this Article.
4. The controller and processor shall take steps to ensure that any natural person acting under the authority of the controller or the processor who has access to personal data does not process them except on instructions from the controller, unless he or she is required to do so by Union or Member State law.
```
</details>


---

## q10 (single)

**Question:** Does the GDPR apply to a company based outside the EU?

**Reference answer:** Yes, if it offers goods or services to people in the Union (paid or free) or monitors their behaviour taking place in the Union. It also applies where Member State law applies by virtue of public international law.

**Agent answer:**

Yes, the GDPR applies to a controller or processor not established in the Union with respect to the processing of personal data of data subjects who are in the Union, where the processing activities are related to:
(a) the offering of goods or services, irrespective of whether a payment of the data subject is required, to such data subjects in the Union; or
(b) the monitoring of their behaviour as far as their behaviour takes place within the Union.

Additionally, the GDPR applies to the processing of personal data by a controller not established in the Union, but in a place where Member State law applies by virtue of public international law.

(GDPR, Article 3)

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 3 - Territorial scope  (distance 0.160)
GDPR, Article 3: Territorial scope
1. This Regulation applies to the processing of personal data in the context of the activities of an establishment of a controller or a processor in the Union, regardless of whether the processing takes place in the Union or not.
2. This Regulation applies to the processing of personal data of data subjects who are in the Union by a controller or processor not established in the Union, where the processing activities are related to:
(a) the offering of goods or services, irrespective of whether a payment of the data subject is required, to such data subjects in the Union; or
(b) the monitoring of their behaviour as far as their behaviour takes place within the Union.
3. This Regulation applies to the processing of personal data by a controller not established in the Union, but in a place where Member State law applies by virtue of public international law.

---

[2] GDPR, Article 2 - Material scope  (distance 0.207)
GDPR, Article 2: Material scope
1. This Regulation applies to the processing of personal data wholly or partly by automated means and to the processing other than by automated means of personal data which form part of a filing system or are intended to form part of a filing system.
2. This Regulation does not apply to the processing of personal data:
(a) in the course of an activity which falls outside the scope of Union law;
(b) by the Member States when carrying out activities which fall within the scope of Chapter 2 of Title V of the TEU;
(c) by a natural person in the course of a purely personal or household activity;
(d) by competent authorities for the purposes of the prevention, investigation, detection or prosecution of criminal offences or the execution of criminal penalties, including the safeguarding against and the prevention of threats to public security.
3. For the processing of personal data by the Union institutions, bodies, offices and agencies, Regulation (EC) No 45/2001 applies. Regulation (EC) No 45/2001 and other Union legal acts applicable to such processing of personal data shall be adapted to the principles and rules of this Regulation in accordance with Article 98.
4. This Regulation shall be without prejudice to the application of Directive 2000/31/EC, in particular of the liability rules of intermediary service providers in Articles 12 to 15 of that Directive.

---

[3] GDPR, Article 27 - Representatives of controllers or processors not established in the Union  (distance 0.235)
GDPR, Article 27: Representatives of controllers or processors not established in the Union
1. Where Article 3(2) applies, the controller or the processor shall designate in writing a representative in the Union.
2. The obligation laid down in paragraph 1 of this Article shall not apply to:
(a) processing which is occasional, does not include, on a large scale, processing of special categories of data as referred to in Article 9(1) or processing of personal data relating to criminal convictions and offences referred to in Article 10, and is unlikely to result in a risk to the rights and freedoms of natural persons, taking into account the nature, context, scope and purposes of the processing; or
(b) a public authority or body.
3. The representative shall be established in one of the Member States where the data subjects, whose personal data are processed in relation to the offering of goods or services to them, or whose behaviour is monitored, are.
4. The representative shall be mandated by the controller or processor to be addressed in addition to or instead of the controller or the processor by, in particular, supervisory authorities and data subjects, on all issues related to processing, for the purposes of ensuring compliance with this Regulation.
5. The designation of a representative by the controller or processor shall be without prejudice to legal actions which could be initiated against the controller or the processor themselves.

---

[4] GDPR, Article 1 - Subject-matter and objectives  (distance 0.240)
GDPR, Article 1: Subject-matter and objectives
1. This Regulation lays down rules relating to the protection of natural persons with regard to the processing of personal data and rules relating to the free movement of personal data.
2. This Regulation protects fundamental rights and freedoms of natural persons and in particular their right to the protection of personal data.
3. The free movement of personal data within the Union shall be neither restricted nor prohibited for reasons connected with the protection of natural persons with regard to the processing of personal data.

---

[5] Data Act, Article 1 - Subject matter and scope, part 1/3  (distance 0.243)
Data Act, Article 1: Subject matter and scope
1. This Regulation lays down harmonised rules, inter alia, on:
(a) the making available of product data and related service data to the user of the connected product or related service;
(b) the making available of data by data holders to data recipients;
(c) the making available of data by data holders to public sector bodies, the Commission, the European Central Bank and Union bodies, where there is an exceptional need for those data for the performance of a specific task carried out in the public interest;
(d) facilitating switching between data processing services;
(e) introducing safeguards against unlawful third-party access to non-personal data; and
(f) the development of interoperability standards for data to be accessed, transferred and used.
2. This Regulation covers personal and non-personal data, including the following types of data, in the following contexts:
(a) Chapter II applies to data, with the exception of content, concerning the performance, use and environment of connected products and related services;
(b) Chapter III applies to any private sector data that is subject to statutory data sharing obligations;
(c) Chapter IV applies to any private sector data accessed and used on the basis of contract between enterprises;
(d) Chapter V applies to any private sector data with a focus on non-personal data;
(e) Chapter VI applies to any data and services processed by providers of data processing services;
(f) Chapter VII applies to any non-personal data held in the Union by providers of data processing services.
3. This Regulation applies to:
(a) manufacturers of connected products placed on the market in the Union and providers of related services, irrespective of the place of establishment of those manufacturers and providers;
(b) users in the Union of connected products or related services as referred to in point (a);
(c) data holders, irrespective of their place of establishment, that make data available to data recipients in the Union;
(d) data recipients in the Union to whom data are made available;
```
</details>


---

## q11 (single)

**Question:** What information must a seller give a customer before they buy a connected product?

**Reference answer:** The type, format and estimated volume of data the product can generate, whether it generates data continuously and in real time, whether data are stored on the device or a remote server (and retention), and how the user can access, retrieve or erase the data.

**Agent answer:**

Before concluding a contract for the purchase, rent, or lease of a connected product, the seller, rentor, or lessor must provide at least the following information to the user in a clear and comprehensible manner:

(a) the type, format, and estimated volume of product data the connected product is capable of generating;
(b) whether the connected product is capable of generating data continuously and in real-time;
(c) whether the connected product is capable of storing data on-device or on a remote server, including the intended duration of retention, where applicable;
(d) how the user may access, retrieve, or, where relevant, erase the data, including the technical means to do so, as well as their terms of use and quality of service.

(Data Act, Article 3)

<details><summary>Retrieved passages</summary>

```
[1] Data Act, Article 3 - Obligation to make product data and related service data accessible to the user, part 1/2  (distance 0.185)
Data Act, Article 3: Obligation to make product data and related service data accessible to the user
1. Connected products shall be designed and manufactured, and related services shall be designed and provided, in such a manner that product data and related service data, including the relevant metadata necessary to interpret and use those data, are, by default, easily, securely, free of charge, in a comprehensive, structured, commonly used and machine-readable format, and, where relevant and technically feasible, directly accessible to the user.
2. Before concluding a contract for the purchase, rent or lease of a connected product, the seller, rentor or lessor, which may be the manufacturer, shall provide at least the following information to the user, in a clear and comprehensible manner:
(a) the type, format and estimated volume of product data which the connected product is capable of generating;
(b) whether the connected product is capable of generating data continuously and in real-time;
(c) whether the connected product is capable of storing data on-device or on a remote server, including, where applicable, the intended duration of retention;
(d) how the user may access, retrieve or, where relevant, erase the data, including the technical means to do so, as well as their terms of use and quality of service.
3. Before concluding a contract for the provision of a related service, the provider of such related service shall provide at least the following information to the user, in a clear and comprehensible manner:
(a) the nature, estimated volume and collection frequency of product data that the prospective data holder is expected to obtain and, where relevant, the arrangements for the user to access or retrieve such data, including the prospective data holder’s data storage arrangements and the duration of retention;
(b) the nature and estimated volume of related service data to be generated, as well as the arrangements for the user to access or retrieve such data, including the prospective data holder’s data storage arrangements and the duration of retention;

---

[2] Data Act, Article 3 - Obligation to make product data and related service data accessible to the user, part 2/2  (distance 0.221)
Data Act, Article 3: Obligation to make product data and related service data accessible to the user
(c) whether the prospective data holder expects to use readily available data itself and the purposes for which those data are to be used, and whether it intends to allow one or more third parties to use the data for purposes agreed upon with the user;
(d) the identity of the prospective data holder, such as its trading name and the geographical address at which it is established and, where applicable, of other data processing parties;
(e) the means of communication which make it possible to contact the prospective data holder quickly and communicate with that data holder efficiently;
(f) how the user can request that the data are shared with a third party and, where applicable, end the data sharing;
(g) the user’s right to lodge a complaint alleging an infringement of any of the provisions of this Chapter with the competent authority designated pursuant to Article 37;
(h) whether a prospective data holder is the holder of trade secrets contained in the data that is accessible from the connected product or generated during the provision of a related service, and, where the prospective data holder is not the trade secret holder, the identity of the trade secret holder;
(i) the duration of the contract between the user and the prospective data holder, as well as the arrangements for terminating such a contract.

---

[3] Data Act, Article 4 - The rights and obligations of users and data holders with regard to access, use and making available product data and related service data, part 1/4  (distance 0.223)
Data Act, Article 4: The rights and obligations of users and data holders with regard to access, use and making available product data and related service data
1. Where data cannot be directly accessed by the user from the connected product or related service, data holders shall make readily available data, as well as the relevant metadata necessary to interpret and use those data, accessible to the user without undue delay, of the same quality as is available to the data holder, easily, securely, free of charge, in a comprehensive, structured, commonly used and machine-readable format and, where relevant and technically feasible, continuously and in real-time. This shall be done on the basis of a simple request through electronic means where technically feasible.
2. Users and data holders may contractually restrict or prohibit accessing, using or further sharing data, if such processing could undermine security requirements of the connected product, as laid down by Union or national law, resulting in a serious adverse effect on the health, safety or security of natural persons. Sectoral authorities may provide users and data holders with technical expertise in that context. Where the data holder refuses to share data pursuant to this Article, it shall notify the competent authority designated pursuant to Article 37.
3. Without prejudice to the user’s right to seek redress at any stage before a court or tribunal of a Member State, the user may, in relation to any dispute with the data holder concerning the contractual restrictions or prohibitions referred to in paragraph 2:
(a) lodge, in accordance with Article 37(5), point (b), a complaint with the competent authority; or
(b) agree with the data holder to refer the matter to a dispute settlement body in accordance with Article 10(1).
4. Data holders shall not make the exercise of choices or rights under this Article by the user unduly difficult, including by offering choices to the user in a non-neutral manner or by subverting or impairing the autonomy, decision-making or choices of the user via the structure, design, function or manner of operation of a user digital interface or a part thereof.

---

[4] Data Act, Article 1 - Subject matter and scope, part 1/3  (distance 0.226)
Data Act, Article 1: Subject matter and scope
1. This Regulation lays down harmonised rules, inter alia, on:
(a) the making available of product data and related service data to the user of the connected product or related service;
(b) the making available of data by data holders to data recipients;
(c) the making available of data by data holders to public sector bodies, the Commission, the European Central Bank and Union bodies, where there is an exceptional need for those data for the performance of a specific task carried out in the public interest;
(d) facilitating switching between data processing services;
(e) introducing safeguards against unlawful third-party access to non-personal data; and
(f) the development of interoperability standards for data to be accessed, transferred and used.
2. This Regulation covers personal and non-personal data, including the following types of data, in the following contexts:
(a) Chapter II applies to data, with the exception of content, concerning the performance, use and environment of connected products and related services;
(b) Chapter III applies to any private sector data that is subject to statutory data sharing obligations;
(c) Chapter IV applies to any private sector data accessed and used on the basis of contract between enterprises;
(d) Chapter V applies to any private sector data with a focus on non-personal data;
(e) Chapter VI applies to any data and services processed by providers of data processing services;
(f) Chapter VII applies to any non-personal data held in the Union by providers of data processing services.
3. This Regulation applies to:
(a) manufacturers of connected products placed on the market in the Union and providers of related services, irrespective of the place of establishment of those manufacturers and providers;
(b) users in the Union of connected products or related services as referred to in point (a);
(c) data holders, irrespective of their place of establishment, that make data available to data recipients in the Union;
(d) data recipients in the Union to whom data are made available;

---

[5] Data Act, Article 2 - Definitions, part 1/6  (distance 0.236)
Data Act, Article 2: Definitions
For the purposes of this Regulation, the following definitions apply:
(1) ‘data’ means any digital representation of acts, facts or information and any compilation of such acts, facts or information, including in the form of sound, visual or audio-visual recording;
(2) ‘metadata’ means a structured description of the contents or the use of data facilitating the discovery or use of that data;
(3) ‘personal data’ means personal data as defined in Article 4, point (1), of Regulation (EU) 2016/679;
(4) ‘non-personal data’ means data other than personal data;
(5) ‘connected product’ means an item that obtains, generates or collects data concerning its use or environment and that is able to communicate product data via an electronic communications service, physical connection or on-device access, and whose primary function is not the storing, processing or transmission of data on behalf of any party other than the user;
(6) ‘related service’ means a digital service, other than an electronic communications service, including software, which is connected with the product at the time of the purchase, rent or lease in such a way that its absence would prevent the connected product from performing one or more of its functions, or which is subsequently connected to the product by the manufacturer or a third party to add to, update or adapt the functions of the connected product;
(7) ‘processing’ means any operation or set of operations which is performed on data or on sets of data, whether or not by automated means, such as collection, recording, organisation, structuring, storage, adaptation or alteration, retrieval, consultation, use, disclosure by transmission, dissemination, or other means of making them available, alignment or combination, restriction, erasure or destruction;
(8) ‘data processing service’ means a digital service that is provided to a customer and that enables ubiquitous and on-demand network access to a shared pool of configurable, scalable and elastic computing resources of a centralised, distributed or highly distributed nature that can be rapidly provisioned and released with minimal management effort or service provider interaction;
```
</details>


---

## q12 (single)

**Question:** From when can cloud providers no longer charge customers for switching to another provider?

**Reference answer:** From 12 January 2027 no switching charges may be imposed. From 11 January 2024 to 12 January 2027 only reduced charges are allowed, not exceeding the provider's direct switching costs.

**Agent answer:**

From 12 January 2027, providers of data processing services shall not impose any switching charges on the customer for the switching process.

(Data Act, Article 29)

<details><summary>Retrieved passages</summary>

```
[1] Data Act, Article 29 - Gradual withdrawal of switching charges  (distance 0.155)
Data Act, Article 29: Gradual withdrawal of switching charges
1. From 12 January 2027, providers of data processing services shall not impose any switching charges on the customer for the switching process.
2. From 11 January 2024 to 12 January 2027, providers of data processing services may impose reduced switching charges on the customer for the switching process.
3. The reduced switching charges referred to in paragraph 2 shall not exceed the costs incurred by the provider of data processing services that are directly linked to the switching process concerned.
4. Before entering into a contract with a customer, providers of data processing services shall provide the prospective customer with clear information on the standard service fees and early termination penalties that might be imposed, as well as on the reduced switching charges that might be imposed during the timeframe referred to in paragraph 2.
5. Where relevant, providers of data processing services shall provide information to a customer on data processing services that involve highly complex or costly switching or for which it is impossible to switch without significant interference in the data, digital assets or service architecture.
6. Where applicable, providers of data processing services shall make the information referred to in paragraphs 4 and 5 publicly available to customers via a dedicated section of their website or in any other easily accessible way.
7. The Commission is empowered to adopt delegated acts in accordance with Article 45 to supplement this Regulation by establishing a monitoring mechanism for the Commission to monitor switching charges, imposed by providers of data processing services on the market to ensure that the withdrawal and reduction of switching charges, pursuant to paragraphs 1 and 2 of this Article are to be attained in accordance with the deadlines laid down in those paragraphs.

---

[2] Data Act, Article 23 - Removing obstacles to effective switching  (distance 0.168)
Data Act, Article 23: Removing obstacles to effective switching
Providers of data processing services shall take the measures provided for in Articles 25, 26, 27, 29 and 30 to enable customers to switch to a data processing service, covering the same service type, which is provided by a different provider of data processing services, or to on-premises ICT infrastructure, or, where relevant, to use several providers of data processing services at the same time. In particular, providers of data processing services shall not impose and shall remove pre-commercial, commercial, technical, contractual and organisational obstacles, which inhibit customers from:
(a) terminating, after the maximum notice period and the successful completion of the switching process, in accordance with Article 25, the contract of the data processing service;
(b) concluding new contracts with a different provider of data processing services covering the same service type;
(c) porting the customer’s exportable data and digital assets, to a different provider of data processing services or to an on-premises ICT infrastructure, including after having benefited from a free-tier offering;
(d) in accordance with Article 24, achieving functional equivalence in the use of the new data processing service in the ICT environment of a different provider of data processing services covering the same service type;
(e) unbundling, where technically feasible, data processing services referred to in Article 30(1) from other data processing services provided by the provider of data processing services.

---

[3] Data Act, Article 25 - Contractual terms concerning switching, part 2/5  (distance 0.169)
Data Act, Article 25: Contractual terms concerning switching
(a) clauses allowing the customer, upon request, to switch to a data processing service offered by a different provider of data processing services or to port all exportable data and digital assets to an on-premises ICT infrastructure, without undue delay and in any event not after the mandatory maximum transitional period of 30 calendar days, to be initiated after the maximum notice period referred to in point (d), during which the service contract remains applicable and during which the provider of data processing services shall: (i) provide reasonable assistance to the customer and third parties authorised by the customer in the switching process; (ii) act with due care to maintain business continuity, and continue the provision of the functions or services under the contract; (iii) provide clear information concerning known risks to continuity in the provision of the functions or services on the part of the source provider of data processing services; (iv) ensure that a high level of security is maintained throughout the switching process, in particular the security of the data during their transfer and the continued security of the data during the retrieval period specified in point (g), in accordance with applicable Union or national law; (i) provide reasonable assistance to the customer and third parties authorised by the customer in the switching process; (ii) act with due care to maintain business continuity, and continue the provision of the functions or services under the contract; (iii) provide clear information concerning known risks to continuity in the provision of the functions or services on the part of the source provider of data processing services; (iv) ensure that a high level of security is maintained throughout the switching process, in particular the security of the data during their transfer and the continued security of the data during the retrieval period specified in point (g), in accordance with applicable Union or national law;
(i) provide reasonable assistance to the customer and third parties authorised by the customer in the switching process;

---

[4] Data Act, Article 30 - Technical aspects of switching, part 1/2  (distance 0.173)
Data Act, Article 30: Technical aspects of switching
1. Providers of data processing services that concern scalable and elastic computing resources limited to infrastructural elements such as servers, networks and the virtual resources necessary for operating the infrastructure, but that do not provide access to the operating services, software and applications that are stored, otherwise processed, or deployed on those infrastructural elements, shall, in accordance with Article 27, take all reasonable measures in their power to facilitate that the customer, after switching to a service covering the same service type, achieves functional equivalence in the use of the destination data processing service. The source provider of data processing services shall facilitate the switching process by providing capabilities, adequate information, documentation, technical support and, where appropriate, the necessary tools.
2. Providers of data processing services, other than those referred to in paragraph 1, shall make open interfaces available to an equal extent to all their customers and the concerned destination providers of data processing services free of charge to facilitate the switching process. Those interfaces shall include sufficient information on the service concerned to enable the development of software to communicate with the services, for the purposes of data portability and interoperability.
3. For data processing services other than those referred to in paragraph 1 of this Article, providers of data processing services shall ensure compatibility with common specifications based on open interoperability specifications or harmonised standards for interoperability at least 12 months after the references to those common specifications or harmonised standards for interoperability of data processing services were published in the central Union standards repository for the interoperability of data processing services following the publication of the underlying implementing acts in the Official Journal of the European Union in accordance with Article 35(8).
4. Providers of data processing services other than those referred to in paragraph 1 of this Article shall update the online register referred to in Article 26, point (b) in accordance with their obligations under paragraph 3 of this Article.

---

[5] Data Act, Article 25 - Contractual terms concerning switching, part 4/5  (distance 0.186)
Data Act, Article 25: Contractual terms concerning switching
(f) an exhaustive specification of categories of data specific to the internal functioning of the provider’s data processing service that are to be exempted from the exportable data under point (e) of this paragraph where a risk of breach of trade secrets of the provider exists, provided that such exemptions do not impede or delay the switching process provided for in Article 23;
(g) a minimum period for data retrieval of at least 30 calendar days, starting after the termination of the transitional period that was agreed between the customer and the provider of data processing services, in accordance with point (a) of this paragraph and paragraph 4;
(h) a clause guaranteeing full erasure of all exportable data and digital assets generated directly by the customer, or relating to the customer directly, after the expiry of the retrieval period referred to in point (g) or after the expiry of an alternative agreed period at a date later than the date of expiry of the retrieval period referred to in point (g), provided that the switching process has been completed successfully;
(i) switching charges, that may be imposed by providers of data processing services in accordance with Article 29.
3. The contract referred to in paragraph 1 shall include clauses providing that the customer may notify the provider of data processing services of its decision to perform one or more of the following actions upon termination of the maximum notice period referred to in paragraph 2, point (d):
(a) switch to a different provider of data processing services, in which case the customer shall provide the necessary details of that provider;
(b) switch to an on-premises ICT infrastructure;
(c) erase its exportable data and digital assets.
```
</details>


---

## q13 (single)

**Question:** Which data processing services are exempt from the Data Act's switching obligations?

**Reference answer:** Services whose main features are custom-built for an individual customer and not offered at broad commercial scale, and non-production versions provided for testing and evaluation for a limited time. Customers must be told in advance which obligations do not apply.

**Agent answer:**

The indexed documents do not cover this. I searched for exemptions to the switching obligations for data processing services under the Data Act.

<details><summary>Retrieved passages</summary>

```
[1] Data Act, Article 23 - Removing obstacles to effective switching  (distance 0.208)
Data Act, Article 23: Removing obstacles to effective switching
Providers of data processing services shall take the measures provided for in Articles 25, 26, 27, 29 and 30 to enable customers to switch to a data processing service, covering the same service type, which is provided by a different provider of data processing services, or to on-premises ICT infrastructure, or, where relevant, to use several providers of data processing services at the same time. In particular, providers of data processing services shall not impose and shall remove pre-commercial, commercial, technical, contractual and organisational obstacles, which inhibit customers from:
(a) terminating, after the maximum notice period and the successful completion of the switching process, in accordance with Article 25, the contract of the data processing service;
(b) concluding new contracts with a different provider of data processing services covering the same service type;
(c) porting the customer’s exportable data and digital assets, to a different provider of data processing services or to an on-premises ICT infrastructure, including after having benefited from a free-tier offering;
(d) in accordance with Article 24, achieving functional equivalence in the use of the new data processing service in the ICT environment of a different provider of data processing services covering the same service type;
(e) unbundling, where technically feasible, data processing services referred to in Article 30(1) from other data processing services provided by the provider of data processing services.

---

[2] Data Act, Article 25 - Contractual terms concerning switching, part 2/5  (distance 0.214)
Data Act, Article 25: Contractual terms concerning switching
(a) clauses allowing the customer, upon request, to switch to a data processing service offered by a different provider of data processing services or to port all exportable data and digital assets to an on-premises ICT infrastructure, without undue delay and in any event not after the mandatory maximum transitional period of 30 calendar days, to be initiated after the maximum notice period referred to in point (d), during which the service contract remains applicable and during which the provider of data processing services shall: (i) provide reasonable assistance to the customer and third parties authorised by the customer in the switching process; (ii) act with due care to maintain business continuity, and continue the provision of the functions or services under the contract; (iii) provide clear information concerning known risks to continuity in the provision of the functions or services on the part of the source provider of data processing services; (iv) ensure that a high level of security is maintained throughout the switching process, in particular the security of the data during their transfer and the continued security of the data during the retrieval period specified in point (g), in accordance with applicable Union or national law; (i) provide reasonable assistance to the customer and third parties authorised by the customer in the switching process; (ii) act with due care to maintain business continuity, and continue the provision of the functions or services under the contract; (iii) provide clear information concerning known risks to continuity in the provision of the functions or services on the part of the source provider of data processing services; (iv) ensure that a high level of security is maintained throughout the switching process, in particular the security of the data during their transfer and the continued security of the data during the retrieval period specified in point (g), in accordance with applicable Union or national law;
(i) provide reasonable assistance to the customer and third parties authorised by the customer in the switching process;

---

[3] Data Act, Article 25 - Contractual terms concerning switching, part 4/5  (distance 0.215)
Data Act, Article 25: Contractual terms concerning switching
(f) an exhaustive specification of categories of data specific to the internal functioning of the provider’s data processing service that are to be exempted from the exportable data under point (e) of this paragraph where a risk of breach of trade secrets of the provider exists, provided that such exemptions do not impede or delay the switching process provided for in Article 23;
(g) a minimum period for data retrieval of at least 30 calendar days, starting after the termination of the transitional period that was agreed between the customer and the provider of data processing services, in accordance with point (a) of this paragraph and paragraph 4;
(h) a clause guaranteeing full erasure of all exportable data and digital assets generated directly by the customer, or relating to the customer directly, after the expiry of the retrieval period referred to in point (g) or after the expiry of an alternative agreed period at a date later than the date of expiry of the retrieval period referred to in point (g), provided that the switching process has been completed successfully;
(i) switching charges, that may be imposed by providers of data processing services in accordance with Article 29.
3. The contract referred to in paragraph 1 shall include clauses providing that the customer may notify the provider of data processing services of its decision to perform one or more of the following actions upon termination of the maximum notice period referred to in paragraph 2, point (d):
(a) switch to a different provider of data processing services, in which case the customer shall provide the necessary details of that provider;
(b) switch to an on-premises ICT infrastructure;
(c) erase its exportable data and digital assets.

---

[4] Data Act, Article 30 - Technical aspects of switching, part 1/2  (distance 0.216)
Data Act, Article 30: Technical aspects of switching
1. Providers of data processing services that concern scalable and elastic computing resources limited to infrastructural elements such as servers, networks and the virtual resources necessary for operating the infrastructure, but that do not provide access to the operating services, software and applications that are stored, otherwise processed, or deployed on those infrastructural elements, shall, in accordance with Article 27, take all reasonable measures in their power to facilitate that the customer, after switching to a service covering the same service type, achieves functional equivalence in the use of the destination data processing service. The source provider of data processing services shall facilitate the switching process by providing capabilities, adequate information, documentation, technical support and, where appropriate, the necessary tools.
2. Providers of data processing services, other than those referred to in paragraph 1, shall make open interfaces available to an equal extent to all their customers and the concerned destination providers of data processing services free of charge to facilitate the switching process. Those interfaces shall include sufficient information on the service concerned to enable the development of software to communicate with the services, for the purposes of data portability and interoperability.
3. For data processing services other than those referred to in paragraph 1 of this Article, providers of data processing services shall ensure compatibility with common specifications based on open interoperability specifications or harmonised standards for interoperability at least 12 months after the references to those common specifications or harmonised standards for interoperability of data processing services were published in the central Union standards repository for the interoperability of data processing services following the publication of the underlying implementing acts in the Official Journal of the European Union in accordance with Article 35(8).
4. Providers of data processing services other than those referred to in paragraph 1 of this Article shall update the online register referred to in Article 26, point (b) in accordance with their obligations under paragraph 3 of this Article.

---

[5] Data Act, Article 25 - Contractual terms concerning switching, part 3/5  (distance 0.217)
Data Act, Article 25: Contractual terms concerning switching
(ii) act with due care to maintain business continuity, and continue the provision of the functions or services under the contract;
(iii) provide clear information concerning known risks to continuity in the provision of the functions or services on the part of the source provider of data processing services;
(iv) ensure that a high level of security is maintained throughout the switching process, in particular the security of the data during their transfer and the continued security of the data during the retrieval period specified in point (g), in accordance with applicable Union or national law;
(b) an obligation of the provider of data processing services to support the customer’s exit strategy relevant to the contracted services, including by providing all relevant information;
(c) a clause specifying that the contract shall be considered to be terminated and the customer shall be notified of the termination, in one of the following cases: (i) where applicable, upon the successful completion of the switching process; (ii) at the end of the maximum notice period referred to in paragraph (d), where the customer does not wish to switch but to erase its exportable data and digital assets upon service termination; (i) where applicable, upon the successful completion of the switching process; (ii) at the end of the maximum notice period referred to in paragraph (d), where the customer does not wish to switch but to erase its exportable data and digital assets upon service termination;
(i) where applicable, upon the successful completion of the switching process;
(ii) at the end of the maximum notice period referred to in paragraph (d), where the customer does not wish to switch but to erase its exportable data and digital assets upon service termination;
(d) a maximum notice period for initiation of the switching process, which shall not exceed two months;
(e) an exhaustive specification of all categories of data and digital assets that can be ported during the switching process, including, at a minimum, all exportable data;
```
</details>


---

## q14 (single)

**Question:** How many working days does a data holder have to decline or modify a public body's data request in a public emergency?

**Reference answer:** No later than five working days after receiving the request.

**Agent answer:**

A data holder has no later than five working days after the receipt of a request to decline or seek the modification of a request for data necessary to respond to a public emergency.

(Data Act, Article 18(2))

<details><summary>Retrieved passages</summary>

```
[1] Data Act, Article 18 - Compliance with requests for data, part 1/2  (distance 0.249)
Data Act, Article 18: Compliance with requests for data
1. A data holder receiving a request to make data available under this Chapter shall make the data available to the requesting public sector body, the Commission, the European Central Bank or a Union body without undue delay, taking into account necessary technical, organisational and legal measures.
2. Without prejudice to specific needs regarding the availability of data defined in Union or national law, a data holder may decline or seek the modification of a request to make data available under this Chapter without undue delay and, in any event, no later than five working days after the receipt of a request for the data necessary to respond to a public emergency and without undue delay and, in any event, no later than 30 working days after the receipt of such a request in other cases of an exceptional need, on any of the following grounds:
(a) the data holder does not have control over the data requested;
(b) a similar request for the same purpose has been previously submitted by another public sector body or the Commission, the European Central Bank or a Union body and the data holder has not been notified of the erasure of the data pursuant to Article 19(1), point (c);
(c) the request does not meet the conditions laid down in Article 17(1) and (2).
3. If the data holder decides to decline the request or to seek its modification in accordance with paragraph 2, point (b), it shall indicate the identity of the public sector body or the Commission, the European Central Bank or the Union body that previously submitted a request for the same purpose.
4. Where the data requested includes personal data, the data holder shall properly anonymise the data, unless the compliance with the request to make data available to a public sector body, the Commission, the European Central Bank or a Union body requires the disclosure of personal data. In such cases, the data holder shall pseudonymise the data.

---

[2] Data Act, Article 15 - Exceptional need to use data, part 1/3  (distance 0.281)
Data Act, Article 15: Exceptional need to use data
1. An exceptional need to use certain data within the meaning of this Chapter shall be limited in time and scope and shall be considered to exist only in any of the following circumstances:
(a) where the data requested is necessary to respond to a public emergency and the public sector body, the Commission, the European Central Bank or the Union body is unable to obtain such data by alternative means in a timely and effective manner under equivalent conditions;

---

[3] Data Act, Article 17 - Requests for data to be made available, part 1/3  (distance 0.296)
Data Act, Article 17: Requests for data to be made available
1. When requesting data pursuant to Article 14, a public sector body, the Commission, the European Central Bank or a Union body shall:
(a) specify the data required, including the relevant metadata necessary to interpret and use those data;
(b) demonstrate that the conditions necessary for the existence of an exceptional need as referred to in Article 15 for the purpose of which the data are requested are met;
(c) explain the purpose of the request, the intended use of the data requested, including, where applicable, by a third party in accordance with paragraph 4 of this Article, the duration of that use, and, where relevant, how the processing of personal data is to address the exceptional need;
(d) specify, if possible, when the data are expected to be erased by all parties that have access to them;
(e) justify the choice of data holder to which the request is addressed;
(f) specify any other public sector bodies or the Commission, European Central Bank or Union bodies and the third parties with which the data requested is expected to be shared with;
(g) where personal data are requested, specify any technical and organisational measures necessary and proportionate to implement data protection principles and necessary safeguards, such as pseudonymisation, and whether anonymisation can be applied by the data holder before making the data available;
(h) state the legal provision allocating to the requesting public sector body, the Commission, the European Central Bank or the Union body the specific task carried out in the public interest relevant for requesting the data;
(i) specify the deadline by which the data are to be made available and the deadline referred to in Article 18(2) by which the data holder may decline or seek modification of the request;
(j) make its best efforts to avoid compliance with the data request resulting in the data holders’ liability for infringement of Union or national law.
2. A request for data made pursuant to paragraph 1 of this Article shall:
(a) be made in writing and expressed in clear, concise and plain language understandable to the data holder;

---

[4] Data Act, Article 15 - Exceptional need to use data, part 3/3  (distance 0.307)
Data Act, Article 15: Exceptional need to use data
(i) a public sector body, the Commission, the European Central Bank or a Union body is acting on the basis of Union or national law and has identified specific data, the lack of which prevents it from fulfilling a specific task carried out in the public interest, that has been explicitly provided for by law, such as the production of official statistics or the mitigation of or recovery from a public emergency; and
(ii) the public sector body, the Commission, the European Central Bank or the Union body has exhausted all other means at its disposal to obtain such data, including purchase of non-personal data on the market by offering market rates, or by relying on existing obligations to make data available or the adoption of new legislative measures which could guarantee the timely availability of the data.
2. Paragraph 1, point (b), shall not apply to microenterprises and small enterprises.
3. The obligation to demonstrate that the public sector body was unable to obtain non-personal data by purchasing them on the market shall not apply where the specific task carried out in the public interest is the production of official statistics and where the purchase of such data is not allowed by national law.

---

[5] Data Governance Act, Article 9 - Procedure for requests for re-use  (distance 0.315)
Data Governance Act, Article 9: Procedure for requests for re-use
1. Unless shorter time limits have been established in accordance with national law, the competent public sector bodies or the competent bodies referred to in Article 7(1) shall adopt a decision on the request for the re-use of the categories of data referred to in Article 3(1) within two months of the date of receipt of the request.
In the case of exceptionally extensive and complex requests for re-use, that two-month period may be extended by up to 30 days. In such cases the competent public sector bodies or the competent bodies referred to in Article 7(1) shall notify the applicant as soon as possible that more time is needed for conducting the procedure, together with the reasons for the delay.
2. Any natural or legal person directly affected by a decision as referred to in paragraph 1 shall have an effective right of redress in the Member State where the relevant body is located. Such a right of redress shall be laid down in national law and shall include the possibility of review by an impartial body with the appropriate expertise, such as the national competition authority, the relevant access-to-documents authority, the supervisory authority established in accordance with Regulation (EU) 2016/679 or a national judicial authority, whose decisions are binding upon the public sector body or the competent body concerned.
```
</details>


---

## q15 (single)

**Question:** Can a data holder charge another business for making data available, and how?

**Reference answer:** Yes. Compensation agreed in business-to-business relations must be non-discriminatory and reasonable and may include a margin, taking into account costs of making data available and investment in data collection, among other factors.

**Agent answer:**

Yes, a data holder can charge another business (a data recipient) for making data available in business-to-business relations, provided that the compensation agreed upon is non-discriminatory and reasonable, and it may include a margin (Data Act, Article 9).

When agreeing on the compensation, the data holder and the data recipient must take into account:
- Costs incurred in making the data available, specifically including costs for formatting data, dissemination via electronic means, and storage (Data Act, Article 9).
- Investments in the collection and production of the data, where applicable, taking into account whether other parties contributed to obtaining, generating, or collecting the data (Data Act, Article 9).

Additionally:
- The compensation may depend on the volume, format, and nature of the data (Data Act, Article 9).
- If the data recipient is an SME or a not-for-profit research organisation without partner or linked enterprises that do not qualify as SMEs, the compensation must not exceed the costs incurred in making the data available (Data Act, Article 9).
- The data holder must provide the data recipient with sufficient detail regarding the basis for calculating the compensation so the recipient can assess whether these requirements are met (Data Act, Article 9).

<details><summary>Retrieved passages</summary>

```
[1] Data Act, Article 9 - Compensation for making data available  (distance 0.190)
Data Act, Article 9: Compensation for making data available
1. Any compensation agreed upon between a data holder and a data recipient for making data available in business-to-business relations shall be non- discriminatory and reasonable and may include a margin.
2. When agreeing on any compensation, the data holder and the data recipient shall take into account in particular:
(a) costs incurred in making the data available, including, in particular, the costs necessary for the formatting of data, dissemination via electronic means and storage;
(b) investments in the collection and production of data, where applicable, taking into account whether other parties contributed to obtaining, generating or collecting the data in question.
3. The compensation referred to in paragraph 1 may also depend on the volume, format and nature of the data.
4. Where the data recipient is an SME or a not-for-profit research organisation and where such a data recipient does not have partner enterprises or linked enterprises that do not qualify as SMEs, any compensation agreed shall not exceed the costs referred to in paragraph 2, point (a).
5. The Commission shall adopt guidelines on the calculation of reasonable compensation, taking into account the advice of the European Data Innovation Board (EDIB) referred to in Article 42.
6. This Article shall not preclude other Union law or national legislation adopted in accordance with Union law from excluding compensation for making data available or providing for lower compensation.
7. The data holder shall provide the data recipient with information setting out the basis for the calculation of the compensation in sufficient detail so that the data recipient can assess whether the requirements of paragraphs 1 to 4 are met.

---

[2] Data Act, Article 20 - Compensation in cases of an exceptional need  (distance 0.234)
Data Act, Article 20: Compensation in cases of an exceptional need
1. Data holders other than microenterprises and small enterprises shall make available data necessary to respond to a public emergency pursuant to Article 15(1), point (a), free of charge. The public sector body, the Commission, the European Central Bank or the Union body that has received data shall provide public acknowledgement to the data holder if requested by the data holder.
2. The data holder shall be entitled to fair compensation for making data available in compliance with a request made pursuant to Article 15(1), point (b). Such compensation shall cover the technical and organisational costs incurred to comply with the request including, where applicable, the costs of anonymisation, pseudonymisation, aggregation and of technical adaptation, and a reasonable margin. Upon request of the public sector body, the Commission, the European Central Bank or the Union body, the data holder shall provide information on the basis for the calculation of the costs and the reasonable margin.
3. Paragraph 2 shall also apply where a microenterprise and small enterprise claims compensation for making data available.
4. Data holders shall not be entitled to compensation for making data available in compliance with a request made pursuant to Article 15(1), point (b), where the specific task carried out in the public interest is the production of official statistics and where the purchase of data is not allowed by national law. Member States shall notify the Commission where the purchase of data for the production of official statistics is not allowed by national law.
5. Where the public sector body, the Commission, the European Central Bank or the Union body disagrees with the level of compensation requested by the data holder, they may lodge a complaint with the competent authority designated pursuant to Article 37 of the Member State where the data holder is established.

---

[3] Data Act, Article 8 - Conditions under which data holders make data available to data recipients  (distance 0.237)
Data Act, Article 8: Conditions under which data holders make data available to data recipients
1. Where, in business-to-business relations, a data holder is obliged to make data available to a data recipient under Article 5 or under other applicable Union law or national legislation adopted in accordance with Union law, it shall agree with a data recipient the arrangements for making the data available and shall do so under fair, reasonable and non-discriminatory terms and conditions and in a transparent manner in accordance with this Chapter and Chapter IV.
2. A contractual term concerning access to and the use of data, or liability and remedies for the breach or termination of data-related obligations, shall not be binding if it constitutes an unfair contractual term within the meaning of Article 13 or if, to the detriment of the user, it excludes the application of, derogates from or varies the effect of the user’s rights under Chapter II.
3. A data holder shall not discriminate regarding the arrangements for making data available between comparable categories of data recipients, including partner enterprises or linked enterprises of the data holder when making data available. Where a data recipient considers that the conditions under which data has been made available to it are discriminatory, the data holder shall without undue delay provide the data recipient, upon its reasoned request, with information showing that there has been no discrimination.
4. A data holder shall not make data available to a data recipient, including on an exclusive basis, unless requested to do so by the user under Chapter II.
5. Data holders and data recipients shall not be required to provide any information beyond what is necessary to verify compliance with the contractual terms agreed for making data available or with their obligations under this Regulation or other applicable Union law or national legislation adopted in accordance with Union law.
6. Unless otherwise provided for in Union law, including Article 4(6) and Article 5(9) of this Regulation, or by national legislation adopted in accordance with Union law, an obligation to make data available to a data recipient shall not oblige the disclosure of trade secrets.

---

[4] Data Act, Article 5 - Right of the user to share data with third parties, part 1/4  (distance 0.254)
Data Act, Article 5: Right of the user to share data with third parties
1. Upon request by a user, or by a party acting on behalf of a user, the data holder shall make available readily available data, as well as the relevant metadata necessary to interpret and use those data, to a third party without undue delay, of the same quality as is available to the data holder, easily, securely, free of charge to the user, in a comprehensive, structured, commonly used and machine-readable format and, where relevant and technically feasible, continuously and in real-time. The data shall be made available by the data holder to the third party in accordance with Articles 8 and 9.
2. Paragraph 1 shall not apply to readily available data in the context of the testing of new connected products, substances or processes that are not yet placed on the market unless their use by a third party is contractually permitted.
3. Any undertaking designated as a gatekeeper, pursuant to Article 3 of Regulation (EU) 2022/1925, shall not be an eligible third party under this Article and therefore shall not:
(a) solicit or commercially incentivise a user in any manner, including by providing monetary or any other compensation, to make data available to one of its services that the user has obtained pursuant to a request under Article 4(1);
(b) solicit or commercially incentivise a user to request the data holder to make data available to one of its services pursuant to paragraph 1 of this Article;
(c) receive data from a user that the user has obtained pursuant to a request under Article 4(1).
4. For the purpose of verifying whether a natural or legal person qualifies as a user or as a third party for the purposes of paragraph 1, the user or the third party shall not be required to provide any information beyond what is necessary. Data holders shall not keep any information on the third party’s access to the data requested beyond what is necessary for the sound execution of the third party’s access request and for the security and maintenance of the data infrastructure.

---

[5] Data Act, Article 4 - The rights and obligations of users and data holders with regard to access, use and making available product data and related service data, part 1/4  (distance 0.258)
Data Act, Article 4: The rights and obligations of users and data holders with regard to access, use and making available product data and related service data
1. Where data cannot be directly accessed by the user from the connected product or related service, data holders shall make readily available data, as well as the relevant metadata necessary to interpret and use those data, accessible to the user without undue delay, of the same quality as is available to the data holder, easily, securely, free of charge, in a comprehensive, structured, commonly used and machine-readable format and, where relevant and technically feasible, continuously and in real-time. This shall be done on the basis of a simple request through electronic means where technically feasible.
2. Users and data holders may contractually restrict or prohibit accessing, using or further sharing data, if such processing could undermine security requirements of the connected product, as laid down by Union or national law, resulting in a serious adverse effect on the health, safety or security of natural persons. Sectoral authorities may provide users and data holders with technical expertise in that context. Where the data holder refuses to share data pursuant to this Article, it shall notify the competent authority designated pursuant to Article 37.
3. Without prejudice to the user’s right to seek redress at any stage before a court or tribunal of a Member State, the user may, in relation to any dispute with the data holder concerning the contractual restrictions or prohibitions referred to in paragraph 2:
(a) lodge, in accordance with Article 37(5), point (b), a complaint with the competent authority; or
(b) agree with the data holder to refer the matter to a dispute settlement body in accordance with Article 10(1).
4. Data holders shall not make the exercise of choices or rights under this Article by the user unduly difficult, including by offering choices to the user in a non-neutral manner or by subverting or impairing the autonomy, decision-making or choices of the user via the structure, design, function or manner of operation of a user digital interface or a part thereof.
```
</details>


---

## q16 (single)

**Question:** How long does a public body have to decide on a request to re-use its data?

**Reference answer:** Within two months of receipt, unless national law sets shorter limits. For exceptionally extensive and complex requests it can be extended by up to 30 days, with the applicant notified.

**Agent answer:**

A competent public sector body or competent body must adopt a decision on a request for the re-use of certain categories of data within two months of the date of receipt of the request, unless shorter time limits have been established in accordance with national law (Data Governance Act, Article 9(1)). 

For exceptionally extensive and complex requests, that two-month period may be extended by up to 30 days, in which case the body must notify the applicant as soon as possible that more time is needed, along with the reasons for the delay (Data Governance Act, Article 9(1)).

(Data Governance Act, Article 9(1))

<details><summary>Retrieved passages</summary>

```
[1] Data Governance Act, Article 9 - Procedure for requests for re-use  (distance 0.231)
Data Governance Act, Article 9: Procedure for requests for re-use
1. Unless shorter time limits have been established in accordance with national law, the competent public sector bodies or the competent bodies referred to in Article 7(1) shall adopt a decision on the request for the re-use of the categories of data referred to in Article 3(1) within two months of the date of receipt of the request.
In the case of exceptionally extensive and complex requests for re-use, that two-month period may be extended by up to 30 days. In such cases the competent public sector bodies or the competent bodies referred to in Article 7(1) shall notify the applicant as soon as possible that more time is needed for conducting the procedure, together with the reasons for the delay.
2. Any natural or legal person directly affected by a decision as referred to in paragraph 1 shall have an effective right of redress in the Member State where the relevant body is located. Such a right of redress shall be laid down in national law and shall include the possibility of review by an impartial body with the appropriate expertise, such as the national competition authority, the relevant access-to-documents authority, the supervisory authority established in accordance with Regulation (EU) 2016/679 or a national judicial authority, whose decisions are binding upon the public sector body or the competent body concerned.

---

[2] Data Act, Article 18 - Compliance with requests for data, part 1/2  (distance 0.268)
Data Act, Article 18: Compliance with requests for data
1. A data holder receiving a request to make data available under this Chapter shall make the data available to the requesting public sector body, the Commission, the European Central Bank or a Union body without undue delay, taking into account necessary technical, organisational and legal measures.
2. Without prejudice to specific needs regarding the availability of data defined in Union or national law, a data holder may decline or seek the modification of a request to make data available under this Chapter without undue delay and, in any event, no later than five working days after the receipt of a request for the data necessary to respond to a public emergency and without undue delay and, in any event, no later than 30 working days after the receipt of such a request in other cases of an exceptional need, on any of the following grounds:
(a) the data holder does not have control over the data requested;
(b) a similar request for the same purpose has been previously submitted by another public sector body or the Commission, the European Central Bank or a Union body and the data holder has not been notified of the erasure of the data pursuant to Article 19(1), point (c);
(c) the request does not meet the conditions laid down in Article 17(1) and (2).
3. If the data holder decides to decline the request or to seek its modification in accordance with paragraph 2, point (b), it shall indicate the identity of the public sector body or the Commission, the European Central Bank or the Union body that previously submitted a request for the same purpose.
4. Where the data requested includes personal data, the data holder shall properly anonymise the data, unless the compliance with the request to make data available to a public sector body, the Commission, the European Central Bank or a Union body requires the disclosure of personal data. In such cases, the data holder shall pseudonymise the data.

---

[3] Data Governance Act, Article 5 - Conditions for re-use, part 1/5  (distance 0.274)
Data Governance Act, Article 5: Conditions for re-use
1. Public sector bodies which are competent under national law to grant or refuse access for the re-use of one or more of the categories of data referred to in Article 3(1) shall make publicly available the conditions for allowing such re-use and the procedure to request the re-use via the single information point referred to in Article 8. Where they grant or refuse access for re-use, they may be assisted by the competent bodies referred to in Article 7(1).
Member States shall ensure that public sector bodies are equipped with the necessary resources to comply with this Article.
2. Conditions for re-use shall be non-discriminatory, transparent, proportionate and objectively justified with regard to the categories of data and the purposes of re-use and the nature of the data for which re-use is allowed. Those conditions shall not be used to restrict competition.
3. Public sector bodies shall, in accordance with Union and national law, ensure that the protected nature of data is preserved. They may provide for the following requirements:
(a) to grant access for the re-use of data only where the public sector body or the competent body, following the request for re-use, has ensured that data has been: (i) anonymised, in the case of personal data; and (ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights; (i) anonymised, in the case of personal data; and (ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights;
(i) anonymised, in the case of personal data; and
(ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights;
(b) to access and re-use the data remotely within a secure processing environment that is provided or controlled by the public sector body;

---

[4] Data Act, Article 17 - Requests for data to be made available, part 3/3  (distance 0.288)
Data Act, Article 17: Requests for data to be made available
3. A public sector body, the Commission, the European Central Bank or a Union body shall not make data obtained pursuant to this Chapter available for reuse as defined in Article 2, point (2), of Regulation (EU) 2022/868 or Article 2, point (11), of Directive (EU) 2019/1024. Regulation (EU) 2022/868 and Directive (EU) 2019/1024 shall not apply to the data held by public sector bodies obtained pursuant to this Chapter.
4. Paragraph 3 of this Article does not preclude a public sector body, the Commission, the European Central Bank or a Union body to exchange data obtained pursuant to this Chapter with another public sector body or the Commission, the European Central Bank or a Union body in view of completing the tasks referred to in Article 15, as specified in the request in accordance with paragraph 1, point (f), of this Article or to make the data available to a third party where it has delegated, by means of a publicly available agreement, technical inspections or other functions to that third party. The obligations on public sector bodies pursuant to Article 19, in particular safeguards to preserve the confidentiality of trade secrets, shall apply also to such third parties. Where a public sector body, the Commission, the European Central Bank or a Union body transmits or makes data available under this paragraph, it shall notify the data holder from whom the data was received without undue delay.
5. Where the data holder considers that its rights under this Chapter have been infringed by the transmission or making available of data, it may lodge a complaint with the competent authority designated pursuant to Article 37 of the Member State where the data holder is established.
6. The Commission shall develop a model template for requests pursuant to this Article.

---

[5] Data Act, Article 17 - Requests for data to be made available, part 1/3  (distance 0.288)
Data Act, Article 17: Requests for data to be made available
1. When requesting data pursuant to Article 14, a public sector body, the Commission, the European Central Bank or a Union body shall:
(a) specify the data required, including the relevant metadata necessary to interpret and use those data;
(b) demonstrate that the conditions necessary for the existence of an exceptional need as referred to in Article 15 for the purpose of which the data are requested are met;
(c) explain the purpose of the request, the intended use of the data requested, including, where applicable, by a third party in accordance with paragraph 4 of this Article, the duration of that use, and, where relevant, how the processing of personal data is to address the exceptional need;
(d) specify, if possible, when the data are expected to be erased by all parties that have access to them;
(e) justify the choice of data holder to which the request is addressed;
(f) specify any other public sector bodies or the Commission, European Central Bank or Union bodies and the third parties with which the data requested is expected to be shared with;
(g) where personal data are requested, specify any technical and organisational measures necessary and proportionate to implement data protection principles and necessary safeguards, such as pseudonymisation, and whether anonymisation can be applied by the data holder before making the data available;
(h) state the legal provision allocating to the requesting public sector body, the Commission, the European Central Bank or the Union body the specific task carried out in the public interest relevant for requesting the data;
(i) specify the deadline by which the data are to be made available and the deadline referred to in Article 18(2) by which the data holder may decline or seek modification of the request;
(j) make its best efforts to avoid compliance with the data request resulting in the data holders’ liability for infringement of Union or national law.
2. A request for data made pursuant to paragraph 1 of this Article shall:
(a) be made in writing and expressed in clear, concise and plain language understandable to the data holder;
```
</details>


---

## q17 (single)

**Question:** How long can an exclusive right to re-use public sector data last?

**Reference answer:** Exclusive arrangements are prohibited in general. Where an exclusive right is exceptionally allowed for a service in the general interest, it may not exceed 12 months.

**Agent answer:**

The duration of an exclusive right to re-use data shall not exceed 12 months, and where a contract is concluded, the duration of the contract shall be the same as the duration of the exclusive right.

(Data Governance Act, Article 4)

<details><summary>Retrieved passages</summary>

```
[1] Data Governance Act, Article 4 - Prohibition of exclusive arrangements  (distance 0.179)
Data Governance Act, Article 4: Prohibition of exclusive arrangements
1. Agreements or other practices pertaining to the re-use of data held by public sector bodies containing categories of data referred to in Article 3(1) which grant exclusive rights or which have as their objective or effect to grant such exclusive rights or to restrict the availability of data for re-use by entities other than the parties to such agreements or other practices shall be prohibited.
2. By way of derogation from paragraph 1, an exclusive right to re-use data referred to in that paragraph may be granted to the extent necessary for the provision of a service or the supply of a product in the general interest that would not otherwise be possible.
3. An exclusive right as referred to in paragraph 2 shall be granted through an administrative act or contractual arrangement in accordance with applicable Union or national law and in compliance with the principles of transparency, equal treatment and non-discrimination.
4. The duration of an exclusive right to re-use data shall not exceed 12 months. Where a contract is concluded, the duration of the contract shall be the same as the duration of the exclusive right.
5. The grant of an exclusive right pursuant to paragraphs 2, 3 and 4, including the reasons as to why it is necessary to grant such a right, shall be transparent and be made publicly available online, in a form that complies with relevant Union law on public procurement.
6. Agreements or other practices falling within the scope of the prohibition referred to in paragraph 1 which do not meet the conditions laid down in paragraphs 2 and 3 and which were concluded before 23 June 2022 shall be terminated at the end of the applicable contract and in any event by 24 December 2024.

---

[2] Data Governance Act, Article 9 - Procedure for requests for re-use  (distance 0.235)
Data Governance Act, Article 9: Procedure for requests for re-use
1. Unless shorter time limits have been established in accordance with national law, the competent public sector bodies or the competent bodies referred to in Article 7(1) shall adopt a decision on the request for the re-use of the categories of data referred to in Article 3(1) within two months of the date of receipt of the request.
In the case of exceptionally extensive and complex requests for re-use, that two-month period may be extended by up to 30 days. In such cases the competent public sector bodies or the competent bodies referred to in Article 7(1) shall notify the applicant as soon as possible that more time is needed for conducting the procedure, together with the reasons for the delay.
2. Any natural or legal person directly affected by a decision as referred to in paragraph 1 shall have an effective right of redress in the Member State where the relevant body is located. Such a right of redress shall be laid down in national law and shall include the possibility of review by an impartial body with the appropriate expertise, such as the national competition authority, the relevant access-to-documents authority, the supervisory authority established in accordance with Regulation (EU) 2016/679 or a national judicial authority, whose decisions are binding upon the public sector body or the competent body concerned.

---

[3] Data Governance Act, Article 5 - Conditions for re-use, part 1/5  (distance 0.241)
Data Governance Act, Article 5: Conditions for re-use
1. Public sector bodies which are competent under national law to grant or refuse access for the re-use of one or more of the categories of data referred to in Article 3(1) shall make publicly available the conditions for allowing such re-use and the procedure to request the re-use via the single information point referred to in Article 8. Where they grant or refuse access for re-use, they may be assisted by the competent bodies referred to in Article 7(1).
Member States shall ensure that public sector bodies are equipped with the necessary resources to comply with this Article.
2. Conditions for re-use shall be non-discriminatory, transparent, proportionate and objectively justified with regard to the categories of data and the purposes of re-use and the nature of the data for which re-use is allowed. Those conditions shall not be used to restrict competition.
3. Public sector bodies shall, in accordance with Union and national law, ensure that the protected nature of data is preserved. They may provide for the following requirements:
(a) to grant access for the re-use of data only where the public sector body or the competent body, following the request for re-use, has ensured that data has been: (i) anonymised, in the case of personal data; and (ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights; (i) anonymised, in the case of personal data; and (ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights;
(i) anonymised, in the case of personal data; and
(ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights;
(b) to access and re-use the data remotely within a secure processing environment that is provided or controlled by the public sector body;

---

[4] Data Governance Act, Article 5 - Conditions for re-use, part 3/5  (distance 0.243)
Data Governance Act, Article 5: Conditions for re-use
6. Where the re-use of data cannot be allowed in accordance with the obligations laid down in paragraphs 3 and 4 of this Article and there is no legal basis for transmitting the data under Regulation (EU) 2016/679, the public sector body shall make best efforts, in accordance with Union and national law, to provide assistance to potential re-users in seeking consent of the data subjects or permission from the data holders whose rights and interests may be affected by such re-use, where it is feasible without a disproportionate burden on the public sector body. Where it provides such assistance, the public sector body may be assisted by the competent bodies referred to in Article 7(1).
7. Re-use of data shall be allowed only in compliance with intellectual property rights. The right of the maker of a database as provided for in Article 7(1) of Directive 96/9/EC shall not be exercised by public sector bodies in order to prevent the re-use of data or to restrict re-use beyond the limits set by this Regulation.
8. Where data requested is considered to be confidential, in accordance with Union or national law on commercial or statistical confidentiality, the public sector bodies shall ensure that the confidential data is not disclosed as a result of allowing re-use, unless such re-use is allowed in accordance with paragraph 6.
9. Where a re-user intends to transfer non-personal data protected on the grounds set out in Article 3(1) to a third country, it shall inform the public sector body of its intention to transfer such data and the purpose of such transfer at the time of requesting the re-use of such data. In the case of re-use in accordance with paragraph 6 of this Article, the re-user shall, where appropriate with the assistance of the public sector body, inform the legal person whose rights and interests may be affected of that intention, purpose and the appropriate safeguards. The public sector body shall not allow the re-use unless the legal person gives permission for the transfer.

---

[5] Data Governance Act, Article 3 - Categories of data  (distance 0.253)
Data Governance Act, Article 3: Categories of data
1. This Chapter applies to data held by public sector bodies which are protected on grounds of:
(a) commercial confidentiality, including business, professional and company secrets;
(b) statistical confidentiality;
(c) the protection of intellectual property rights of third parties; or
(d) the protection of personal data, insofar as such data fall outside the scope of Directive (EU) 2019/1024.
2. This Chapter does not apply to:
(a) data held by public undertakings;
(b) data held by public service broadcasters and their subsidiaries, and by other bodies or their subsidiaries for the fulfilment of a public service broadcasting remit;
(c) data held by cultural establishments and educational establishments;
(d) data held by public sector bodies which are protected for reasons of public security, defence or national security; or
(e) data the supply of which is an activity falling outside the scope of the public task of the public sector bodies concerned as defined by law or by other binding rules in the Member State concerned, or, in the absence of such rules, as defined in accordance with common administrative practice in that Member State, provided that the scope of the public tasks is transparent and subject to review.
3. This Chapter is without prejudice to:
(a) Union and national law and international agreements to which the Union or Member States are party on the protection of categories of data referred to in paragraph 1; and
(b) Union and national law on access to documents.
```
</details>


---

## q18 (single)

**Question:** Which kinds of data-sharing services have to be notified to an authority?

**Reference answer:** Data intermediation services between data holders and potential data users, services between data subjects (or individuals with non-personal data) and potential data users, and services of data cooperatives.

**Agent answer:**

Any data intermediation services provider that intends to provide data intermediation services must submit a notification to the competent authority for data intermediation services (Data Governance Act, Article 11).

The services subject to this notification requirement are:
- Intermediation services between data holders and potential data users, including making available technical or other means to enable such services (such as bilateral or multilateral data exchanges, platforms, databases, or specific infrastructure for interconnecting data holders with data users) (Data Governance Act, Article 10).
- Intermediation services between data subjects seeking to make their personal data available (or natural persons seeking to make non-personal data available) and potential data users, including enabling the exercise of data subjects' rights under Regulation (EU) 2016/679 (Data Governance Act, Article 10).
- Services of data cooperatives (Data Governance Act, Article 10).

<details><summary>Retrieved passages</summary>

```
[1] Data Governance Act, Article 11 - Notification by data intermediation services providers, part 1/3  (distance 0.245)
Data Governance Act, Article 11: Notification by data intermediation services providers
1. Any data intermediation services provider who intends to provide the data intermediation services referred to in Article 10 shall submit a notification to the competent authority for data intermediation services.
2. For the purposes of this Regulation, a data intermediation services provider with establishments in more than one Member State shall be deemed to be under the jurisdiction of the Member State in which it has its main establishment, without prejudice to Union law regulating cross-border actions for damages and related proceedings.
3. A data intermediation services provider that is not established in the Union, but which offers the data intermediation services referred to in Article 10 within the Union, shall designate a legal representative in one of the Member States in which those services are offered.
For the purpose of ensuring compliance with this Regulation, the legal representative shall be mandated by the data intermediation services provider to be addressed in addition to or instead of it by competent authorities for data intermediation services or data subjects and data holders, with regard to all issues related to the data intermediation services provided. The legal representative shall cooperate with and comprehensively demonstrate to the competent authorities for data intermediation services, upon request, the actions taken and provisions put in place by the data intermediation services provider to ensure compliance with this Regulation.
The data intermediation services provider shall be deemed to be under the jurisdiction of the Member State in which the legal representative is located. The designation of a legal representative by the data intermediation services provider shall be without prejudice to any legal actions which could be initiated against the data intermediation services provider.
4. After having submitted a notification in accordance with paragraph 1, the data intermediation services provider may start the activity subject to the conditions laid down in this Chapter.
5. The notification referred to in paragraph 1 shall entitle the data intermediation services provider to provide data intermediation services in all Member States.
6. The notification referred to in paragraph 1 shall include the following information:

---

[2] Data Governance Act, Article 11 - Notification by data intermediation services providers, part 3/3  (distance 0.247)
Data Governance Act, Article 11: Notification by data intermediation services providers
In order to ensure that data intermediation services providers recognised in the Union are easily identifiable throughout the Union, the Commission shall, by means of implementing acts, establish a design for the common logo. Data intermediation services providers recognised in the Union shall display the common logo clearly on every online and offline publication that relates to their data intermediation activities.
Those implementing acts shall be adopted in accordance with the advisory procedure referred to in Article 33(2).
10. The competent authority for data intermediation services shall notify the Commission of each new notification by electronic means without delay. The Commission shall keep and regularly update a public register of all data intermediation services providers providing their services in the Union. The information referred to in paragraph 6, points (a), (b), (c), (d), (f) and (g), shall be published in the public register.
11. The competent authority for data intermediation services may charge fees for the notification in accordance with national law. Such fees shall be proportionate and objective and be based on the administrative costs related to the monitoring of compliance and other market control activities of the competent authority for data intermediation services in relation to notifications of data intermediation services providers. In the case of SMEs and start-ups, the competent authority for data intermediation services may charge a discounted fee or waive the fee.
12. Data intermediation services providers shall notify the competent authority for data intermediation services of any changes to the information provided pursuant to paragraph 6 within 14 days of the date of the change.
13. Where a data intermediation services provider ceases its activities, it shall notify the relevant competent authority for data intermediation services determined pursuant to paragraphs 1, 2 and 3 within 15 days.
14. The competent authority for data intermediation services shall notify the Commission of each notification referred to in paragraphs 12 and 13 by electronic means without delay. The Commission shall update the public register of the data intermediation services providers in the Union accordingly.

---

[3] Data Governance Act, Article 11 - Notification by data intermediation services providers, part 2/3  (distance 0.249)
Data Governance Act, Article 11: Notification by data intermediation services providers
(a) the name of the data intermediation services provider;
(b) the data intermediation services provider’s legal status, form, ownership structure, relevant subsidiaries and, where the data intermediation services provider is registered in a trade or other similar public national register, registration number;
(c) the address of the data intermediation services provider’s main establishment in the Union, if any, and, where applicable, of any secondary branch in another Member State or that of the legal representative;
(d) a public website where complete and up-to-date information on the data intermediation services provider and the activities can be found, including as a minimum the information referred to in points (a), (b), (c) and (f);
(e) the data intermediation services provider’s contact persons and contact details;
(f) a description of the data intermediation service the data intermediation services provider intends to provide, and an indication of the categories listed in Article 10 under which such data intermediation service falls;
(g) the estimated date for starting the activity, if different from the date of the notification.
7. The competent authority for data intermediation services shall ensure that the notification procedure is non-discriminatory and does not distort the competition.
8. At the request of the data intermediation services provider, the competent authority for data intermediation services shall, within one week of a duly and fully completed notification, issue a standardised declaration, confirming that the data intermediation services provider has submitted the notification referred to in paragraph 1 and that the notification contains the information referred to in paragraph 6.
9. At the request of the data intermediation services provider, the competent authority for data intermediation services shall confirm that the data intermediation services provider complies with this Article and Article 12. Upon receipt of such a confirmation, that data intermediation services provider may use the label ‘data intermediation services provider recognised in the Union’ in its written and spoken communication, as well as a common logo.

---

[4] Data Act, Article 21 - Sharing of data obtained in the context of an exceptional need with research organisations or statistical bodies, part 2/2  (distance 0.251)
Data Act, Article 21: Sharing of data obtained in the context of an exceptional need with research organisations or statistical bodies
5. Where a public sector body, the Commission, the European Central Bank or a Union body intends to transmit or make data available under paragraph 1 of this Article, it shall notify without undue delay the data holder from whom the data was received, stating the identity and contact details of the organisation or the individual receiving the data, the purpose of the transmission or making available of the data, the period for which the data is to be used and the technical protection and organisational measures taken, including where personal data or trade secrets are involved. Where the data holder disagrees with the transmission or making available of data, it may lodge a complaint with the competent authority designated pursuant to Article 37 of the Member State where the data holder is established.

---

[5] Data Governance Act, Article 13 - Competent authorities for data intermediation services  (distance 0.262)
Data Governance Act, Article 13: Competent authorities for data intermediation services
1. Each Member State shall designate one or more competent authorities to carry out the tasks related to the notification procedure for data intermediation services and shall notify the Commission of the identity of those competent authorities by 24 September 2023. Each Member State shall also notify the Commission of any subsequent change to the identity of those competent authorities.
2. The competent authorities for data intermediation services shall comply with the requirements set out in Article 26.
3. The powers of the competent authorities for data intermediation services are without prejudice to the powers of the data protection authorities, national competition authorities, authorities in charge of cybersecurity and other relevant sectoral authorities. In accordance with their respective competences under Union and national law, those authorities shall establish strong cooperation and exchange information as is necessary for the exercise of their tasks in relation to data intermediation services providers, and shall aim to achieve consistency in the decisions taken in applying this Regulation.

---

[1] Data Governance Act, Article 10 - Data intermediation services  (distance 0.140)
Data Governance Act, Article 10: Data intermediation services
The provision of the following data intermediation services shall comply with Article 12 and shall be subject to a notification procedure:
(a) intermediation services between data holders and potential data users, including making available the technical or other means to enable such services; those services may include bilateral or multilateral exchanges of data or the creation of platforms or databases enabling the exchange or joint use of data, as well as the establishment of other specific infrastructure for the interconnection of data holders with data users;
(b) intermediation services between data subjects that seek to make their personal data available or natural persons that seek to make non-personal data available, and potential data users, including making available the technical or other means to enable such services, and in particular enabling the exercise of the data subjects’ rights provided in Regulation (EU) 2016/679;
(c) services of data cooperatives.

---

[2] Data Governance Act, Article 2 - Definitions, part 2/6  (distance 0.169)
Data Governance Act, Article 2: Definitions
(11) ‘data intermediation service’ means a service which aims to establish commercial relationships for the purposes of data sharing between an undetermined number of data subjects and data holders on the one hand and data users on the other, through technical, legal or other means, including for the purpose of exercising the rights of data subjects in relation to personal data, excluding at least the following: (a) services that obtain data from data holders and aggregate, enrich or transform the data for the purpose of adding substantial value to it and license the use of the resulting data to data users, without establishing a commercial relationship between data holders and data users; (b) services that focus on the intermediation of copyright-protected content; (c) services that are exclusively used by one data holder in order to enable the use of the data held by that data holder, or that are used by multiple legal persons in a closed group, including supplier or customer relationships or collaborations established by contract, in particular those that have as a main objective to ensure the functionalities of objects and devices connected to the Internet of Things; (d) data sharing services offered by public sector bodies that do not aim to establish commercial relationships; (a) services that obtain data from data holders and aggregate, enrich or transform the data for the purpose of adding substantial value to it and license the use of the resulting data to data users, without establishing a commercial relationship between data holders and data users; (b) services that focus on the intermediation of copyright-protected content; (c) services that are exclusively used by one data holder in order to enable the use of the data held by that data holder, or that are used by multiple legal persons in a closed group, including supplier or customer relationships or collaborations established by contract, in particular those that have as a main objective to ensure the functionalities of objects and devices connected to the Internet of Things; (d) data sharing services offered by public sector bodies that do not aim to establish commercial relationships;

---

[3] Data Governance Act, Article 12 - Conditions for providing data intermediation services, part 1/3  (distance 0.169)
Data Governance Act, Article 12: Conditions for providing data intermediation services
The provision of data intermediation services referred in Article 10 shall be subject to the following conditions:
(a) the data intermediation services provider shall not use the data for which it provides data intermediation services for purposes other than to put them at the disposal of data users and shall provide data intermediation services through a separate legal person;
(b) the commercial terms, including pricing, for the provision of data intermediation services to a data holder or data user shall not be dependent upon whether the data holder or data user uses other services provided by the same data intermediation services provider or by a related entity, and if so to what degree the data holder or data user uses such other services;
(c) the data collected with respect to any activity of a natural or legal person for the purpose of the provision of the data intermediation service, including the date, time and geolocation data, duration of activity and connections to other natural or legal persons established by the person who uses the data intermediation service, shall be used only for the development of that data intermediation service, which may entail the use of data for the detection of fraud or cybersecurity, and shall be made available to the data holders upon request;
(d) the data intermediation services provider shall facilitate the exchange of the data in the format in which it receives it from a data subject or a data holder, shall convert the data into specific formats only to enhance interoperability within and across sectors or if requested by the data user or where mandated by Union law or to ensure harmonisation with international or European data standards and shall offer an opt-out possibility regarding those conversions to data subjects or data holders, unless the conversion is mandated by Union law;

---

[4] Data Governance Act, Article 12 - Conditions for providing data intermediation services, part 2/3  (distance 0.170)
Data Governance Act, Article 12: Conditions for providing data intermediation services
(e) data intermediation services may include offering additional specific tools and services to data holders or data subjects for the specific purpose of facilitating the exchange of data, such as temporary storage, curation, conversion, anonymisation and pseudonymisation, such tools being used only at the explicit request or approval of the data holder or data subject and third-party tools offered in that context not being used for other purposes;
(f) the data intermediation services provider shall ensure that the procedure for access to its service is fair, transparent and non-discriminatory for both data subjects and data holders, as well as for data users, including with regard to prices and terms of service;
(g) the data intermediation services provider shall have procedures in place to prevent fraudulent or abusive practices in relation to parties seeking access through its data intermediation services;
(h) the data intermediation services provider shall, in the event of its insolvency, ensure a reasonable continuity of the provision of its data intermediation services and, where such data intermediation services ensure the storage of data, shall have mechanisms in place to allow data holders and data users to obtain access to, to transfer or to retrieve their data and, where such data intermediation services are provided between data subjects and data users, to allow data subjects to exercise their rights;
(i) the data intermediation services provider shall take appropriate measures to ensure interoperability with other data intermediation services, inter alia , by means of commonly used open standards in the sector in which the data intermediation services provider operates;
(j) the data intermediation services provider shall put in place adequate technical, legal and organisational measures in order to prevent the transfer of or access to non-personal data that is unlawful under Union law or the national law of the relevant Member State;
(k) the data intermediation services provider shall without delay inform data holders in the event of an unauthorised transfer, access or use of the non-personal data that it has shared;

---

[5] Data Governance Act, Article 2 - Definitions, part 3/6  (distance 0.182)
Data Governance Act, Article 2: Definitions
(a) services that obtain data from data holders and aggregate, enrich or transform the data for the purpose of adding substantial value to it and license the use of the resulting data to data users, without establishing a commercial relationship between data holders and data users;
(b) services that focus on the intermediation of copyright-protected content;
(c) services that are exclusively used by one data holder in order to enable the use of the data held by that data holder, or that are used by multiple legal persons in a closed group, including supplier or customer relationships or collaborations established by contract, in particular those that have as a main objective to ensure the functionalities of objects and devices connected to the Internet of Things;
(d) data sharing services offered by public sector bodies that do not aim to establish commercial relationships;
(12) ‘processing’ means processing as defined in Article 4, point (2), of Regulation (EU) 2016/679 with regard to personal data or Article 3, point (2), of Regulation (EU) 2018/1807 with regard to non-personal data;
(13) ‘access’ means data use, in accordance with specific technical, legal or organisational requirements, without necessarily implying the transmission or downloading of data;
(14) ‘main establishment’ of a legal person means the place of its central administration in the Union;
(15) ‘services of data cooperatives’ means data intermediation services offered by an organisational structure constituted by data subjects, one-person undertakings or SMEs who are members of that structure, having as its main objectives to support its members in the exercise of their rights with respect to certain data, including with regard to making informed choices before they consent to data processing, to exchange views on data processing purposes and conditions that would best represent the interests of its members in relation to their data, and to negotiate terms and conditions for data processing on behalf of its members before giving permission to the processing of non-personal data or before they consent to the processing of personal data;
```
</details>


---

## q19 (single)

**Question:** Does the Data Governance Act give a legal basis for processing personal data?

**Reference answer:** No. It does not create a legal basis for processing personal data or affect rights and obligations under the GDPR. If it conflicts with EU or national data protection law, the data protection law prevails.

**Agent answer:**

The indexed documents do not cover this. I searched for whether the Data Governance Act provides a legal basis for processing personal data.

<details><summary>Retrieved passages</summary>

```
[1] Data Governance Act, Article 1 - Subject matter and scope, part 1/2  (distance 0.193)
Data Governance Act, Article 1: Subject matter and scope
1. This Regulation lays down:
(a) conditions for the re-use, within the Union, of certain categories of data held by public sector bodies;
(b) a notification and supervisory framework for the provision of data intermediation services;
(c) a framework for voluntary registration of entities which collect and process data made available for altruistic purposes; and
(d) a framework for the establishment of a European Data Innovation Board.
2. This Regulation does not create any obligation on public sector bodies to allow the re-use of data, nor does it release public sector bodies from their confidentiality obligations under Union or national law.
This Regulation is without prejudice to:
(a) specific provisions in Union or national law regarding the access to or re-use of certain categories of data, in particular with regard to the granting of access to and disclosure of official documents; and
(b) the obligations of public sector bodies under Union or national law to allow the re-use of data or to requirements related to processing of non-personal data.
Where sector-specific Union or national law requires public sector bodies, data intermediation services providers or recognised data altruism organisations to comply with specific additional technical, administrative or organisational requirements, including through an authorisation or certification regime, those provisions of that sector-specific Union or national law shall also apply. Any such specific additional requirements shall be non-discriminatory, proportionate and objectively justified.

---

[2] GDPR, Article 6 - Lawfulness of processing, part 1/3  (distance 0.204)
GDPR, Article 6: Lawfulness of processing
1. Processing shall be lawful only if and to the extent that at least one of the following applies:
(a) the data subject has given consent to the processing of his or her personal data for one or more specific purposes;
(b) processing is necessary for the performance of a contract to which the data subject is party or in order to take steps at the request of the data subject prior to entering into a contract;
(c) processing is necessary for compliance with a legal obligation to which the controller is subject;
(d) processing is necessary in order to protect the vital interests of the data subject or of another natural person;
(e) processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller;
(f) processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject which require protection of personal data, in particular where the data subject is a child.
Point (f) of the first subparagraph shall not apply to processing carried out by public authorities in the performance of their tasks.
2. Member States may maintain or introduce more specific provisions to adapt the application of the rules of this Regulation with regard to processing for compliance with points (c) and (e) of paragraph 1 by determining more precisely specific requirements for the processing and other measures to ensure lawful and fair processing including for other specific processing situations as provided for in Chapter IX.
3. The basis for the processing referred to in point (c) and (e) of paragraph 1 shall be laid down by:
(a) Union law; or
(b) Member State law to which the controller is subject.

---

[3] Data Act, Article 14 - Obligation to make data available on the basis of an exceptional need  (distance 0.205)
Data Act, Article 14: Obligation to make data available on the basis of an exceptional need
Where a public sector body, the Commission, the European Central Bank or a Union body demonstrates an exceptional need, as set out in Article 15, to use certain data, including the relevant metadata necessary to interpret and use those data, to carry out its statutory duties in the public interest, data holders that are legal persons, other than public sectors bodies, which hold those data shall make them available upon a duly reasoned request.

---

[4] Data Governance Act, Article 5 - Conditions for re-use, part 1/5  (distance 0.208)
Data Governance Act, Article 5: Conditions for re-use
1. Public sector bodies which are competent under national law to grant or refuse access for the re-use of one or more of the categories of data referred to in Article 3(1) shall make publicly available the conditions for allowing such re-use and the procedure to request the re-use via the single information point referred to in Article 8. Where they grant or refuse access for re-use, they may be assisted by the competent bodies referred to in Article 7(1).
Member States shall ensure that public sector bodies are equipped with the necessary resources to comply with this Article.
2. Conditions for re-use shall be non-discriminatory, transparent, proportionate and objectively justified with regard to the categories of data and the purposes of re-use and the nature of the data for which re-use is allowed. Those conditions shall not be used to restrict competition.
3. Public sector bodies shall, in accordance with Union and national law, ensure that the protected nature of data is preserved. They may provide for the following requirements:
(a) to grant access for the re-use of data only where the public sector body or the competent body, following the request for re-use, has ensured that data has been: (i) anonymised, in the case of personal data; and (ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights; (i) anonymised, in the case of personal data; and (ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights;
(i) anonymised, in the case of personal data; and
(ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights;
(b) to access and re-use the data remotely within a secure processing environment that is provided or controlled by the public sector body;

---

[5] Data Governance Act, Article 5 - Conditions for re-use, part 3/5  (distance 0.208)
Data Governance Act, Article 5: Conditions for re-use
6. Where the re-use of data cannot be allowed in accordance with the obligations laid down in paragraphs 3 and 4 of this Article and there is no legal basis for transmitting the data under Regulation (EU) 2016/679, the public sector body shall make best efforts, in accordance with Union and national law, to provide assistance to potential re-users in seeking consent of the data subjects or permission from the data holders whose rights and interests may be affected by such re-use, where it is feasible without a disproportionate burden on the public sector body. Where it provides such assistance, the public sector body may be assisted by the competent bodies referred to in Article 7(1).
7. Re-use of data shall be allowed only in compliance with intellectual property rights. The right of the maker of a database as provided for in Article 7(1) of Directive 96/9/EC shall not be exercised by public sector bodies in order to prevent the re-use of data or to restrict re-use beyond the limits set by this Regulation.
8. Where data requested is considered to be confidential, in accordance with Union or national law on commercial or statistical confidentiality, the public sector bodies shall ensure that the confidential data is not disclosed as a result of allowing re-use, unless such re-use is allowed in accordance with paragraph 6.
9. Where a re-user intends to transfer non-personal data protected on the grounds set out in Article 3(1) to a third country, it shall inform the public sector body of its intention to transfer such data and the purpose of such transfer at the time of requesting the re-use of such data. In the case of re-use in accordance with paragraph 6 of this Article, the re-user shall, where appropriate with the assistance of the public sector body, inform the legal person whose rights and interests may be affected of that intention, purpose and the appropriate safeguards. The public sector body shall not allow the re-use unless the legal person gives permission for the transfer.

---

[1] Data Governance Act, Article 1 - Subject matter and scope, part 1/2  (distance 0.171)
Data Governance Act, Article 1: Subject matter and scope
1. This Regulation lays down:
(a) conditions for the re-use, within the Union, of certain categories of data held by public sector bodies;
(b) a notification and supervisory framework for the provision of data intermediation services;
(c) a framework for voluntary registration of entities which collect and process data made available for altruistic purposes; and
(d) a framework for the establishment of a European Data Innovation Board.
2. This Regulation does not create any obligation on public sector bodies to allow the re-use of data, nor does it release public sector bodies from their confidentiality obligations under Union or national law.
This Regulation is without prejudice to:
(a) specific provisions in Union or national law regarding the access to or re-use of certain categories of data, in particular with regard to the granting of access to and disclosure of official documents; and
(b) the obligations of public sector bodies under Union or national law to allow the re-use of data or to requirements related to processing of non-personal data.
Where sector-specific Union or national law requires public sector bodies, data intermediation services providers or recognised data altruism organisations to comply with specific additional technical, administrative or organisational requirements, including through an authorisation or certification regime, those provisions of that sector-specific Union or national law shall also apply. Any such specific additional requirements shall be non-discriminatory, proportionate and objectively justified.

---

[2] Data Governance Act, Article 5 - Conditions for re-use, part 1/5  (distance 0.181)
Data Governance Act, Article 5: Conditions for re-use
1. Public sector bodies which are competent under national law to grant or refuse access for the re-use of one or more of the categories of data referred to in Article 3(1) shall make publicly available the conditions for allowing such re-use and the procedure to request the re-use via the single information point referred to in Article 8. Where they grant or refuse access for re-use, they may be assisted by the competent bodies referred to in Article 7(1).
Member States shall ensure that public sector bodies are equipped with the necessary resources to comply with this Article.
2. Conditions for re-use shall be non-discriminatory, transparent, proportionate and objectively justified with regard to the categories of data and the purposes of re-use and the nature of the data for which re-use is allowed. Those conditions shall not be used to restrict competition.
3. Public sector bodies shall, in accordance with Union and national law, ensure that the protected nature of data is preserved. They may provide for the following requirements:
(a) to grant access for the re-use of data only where the public sector body or the competent body, following the request for re-use, has ensured that data has been: (i) anonymised, in the case of personal data; and (ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights; (i) anonymised, in the case of personal data; and (ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights;
(i) anonymised, in the case of personal data; and
(ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights;
(b) to access and re-use the data remotely within a secure processing environment that is provided or controlled by the public sector body;

---

[3] Data Governance Act, Article 5 - Conditions for re-use, part 3/5  (distance 0.182)
Data Governance Act, Article 5: Conditions for re-use
6. Where the re-use of data cannot be allowed in accordance with the obligations laid down in paragraphs 3 and 4 of this Article and there is no legal basis for transmitting the data under Regulation (EU) 2016/679, the public sector body shall make best efforts, in accordance with Union and national law, to provide assistance to potential re-users in seeking consent of the data subjects or permission from the data holders whose rights and interests may be affected by such re-use, where it is feasible without a disproportionate burden on the public sector body. Where it provides such assistance, the public sector body may be assisted by the competent bodies referred to in Article 7(1).
7. Re-use of data shall be allowed only in compliance with intellectual property rights. The right of the maker of a database as provided for in Article 7(1) of Directive 96/9/EC shall not be exercised by public sector bodies in order to prevent the re-use of data or to restrict re-use beyond the limits set by this Regulation.
8. Where data requested is considered to be confidential, in accordance with Union or national law on commercial or statistical confidentiality, the public sector bodies shall ensure that the confidential data is not disclosed as a result of allowing re-use, unless such re-use is allowed in accordance with paragraph 6.
9. Where a re-user intends to transfer non-personal data protected on the grounds set out in Article 3(1) to a third country, it shall inform the public sector body of its intention to transfer such data and the purpose of such transfer at the time of requesting the re-use of such data. In the case of re-use in accordance with paragraph 6 of this Article, the re-user shall, where appropriate with the assistance of the public sector body, inform the legal person whose rights and interests may be affected of that intention, purpose and the appropriate safeguards. The public sector body shall not allow the re-use unless the legal person gives permission for the transfer.

---

[4] Data Governance Act, Article 5 - Conditions for re-use, part 2/5  (distance 0.190)
Data Governance Act, Article 5: Conditions for re-use
(c) to access and re-use the data within the physical premises in which the secure processing environment is located in accordance with high security standards, provided that remote access cannot be allowed without jeopardising the rights and interests of third parties.
4. In the case of re-use allowed in accordance with paragraph 3, points (b) and (c), the public sector bodies shall impose conditions that preserve the integrity of the functioning of the technical systems of the secure processing environment used. The public sector body shall reserve the right to verify the process, the means and any results of processing of data undertaken by the re-user to preserve the integrity of the protection of the data and reserve the right to prohibit the use of results that contain information jeopardising the rights and interests of third parties. The decision to prohibit the use of the results shall be comprehensible and transparent to the re-user.
5. Unless national law provides for specific safeguards on applicable confidentiality obligations relating to the re-use of data referred to in Article 3(1), the public sector body shall make the re-use of data provided in accordance with paragraph 3 of this Article conditional on the adherence by the re-user to a confidentiality obligation that prohibits the disclosure of any information that jeopardises the rights and interests of third parties that the re-user may have acquired despite the safeguards put in place. Re-users shall be prohibited from re-identifying any data subject to whom the data relates and shall take technical and operational measures to prevent re-identification and to notify any data breach resulting in the re-identification of the data subjects concerned to the public sector body. In the event of the unauthorised re-use of non-personal data, the re-user shall, without delay, where appropriate with the assistance of the public sector body, inform the legal persons whose rights and interests may be affected.

---

[5] Data Governance Act, Article 2 - Definitions, part 1/6  (distance 0.192)
Data Governance Act, Article 2: Definitions
For the purposes of this Regulation, the following definitions apply:
(1) ‘data’ means any digital representation of acts, facts or information and any compilation of such acts, facts or information, including in the form of sound, visual or audiovisual recording;
(2) ‘re-use’ means the use by natural or legal persons of data held by public sector bodies, for commercial or non-commercial purposes other than the initial purpose within the public task for which the data were produced, except for the exchange of data between public sector bodies purely in pursuit of their public tasks;
(3) ‘personal data’ means personal data as defined in Article 4, point (1), of Regulation (EU) 2016/679;
(4) ‘non-personal data’ means data other than personal data;
(5) ‘consent’ means consent as defined in Article 4, point (11), of Regulation (EU) 2016/679;
(6) ‘permission’ means giving data users the right to the processing of non-personal data;
(7) ‘data subject’ means data subject as referred to in Article 4, point (1), of Regulation (EU) 2016/679;
(8) ‘data holder’ means a legal person, including public sector bodies and international organisations, or a natural person who is not a data subject with respect to the specific data in question, which, in accordance with applicable Union or national law, has the right to grant access to or to share certain personal data or non-personal data;
(9) ‘data user’ means a natural or legal person who has lawful access to certain personal or non-personal data and has the right, including under Regulation (EU) 2016/679 in the case of personal data, to use that data for commercial or non-commercial purposes;
(10) ‘data sharing’ means the provision of data by a data subject or a data holder to a data user for the purpose of the joint or individual use of such data, based on voluntary agreements or Union or national law, directly or through an intermediary, for example under open or commercial licences subject to a fee or free of charge;
```
</details>


---

## q20 (multi)

**Question:** What are our deadlines to react to a data breach, both towards the authority and towards the people affected?

**Reference answer:** Authority: without undue delay and where feasible within 72 hours, unless no risk is likely (Art. 33). Individuals: without undue delay, only where the breach is likely to result in a high risk (Art. 34), with exceptions such as encryption.

**Agent answer:**

**Towards the supervisory authority:**
The controller must notify the personal data breach to the supervisory authority without undue delay and, where feasible, not later than 72 hours after having become aware of it, unless the breach is unlikely to result in a risk to the rights and freedoms of natural persons. If the notification is not made within 72 hours, it must be accompanied by reasons for the delay (GDPR, Article 33). 
If you are a processor, you must notify the controller without undue delay after becoming aware of a personal data breach (GDPR, Article 33).

**Towards the people affected (data subjects):**
When the personal data breach is likely to result in a high risk to the rights and freedoms of natural persons, the controller must communicate the breach to the data subject without undue delay (GDPR, Article 34). This communication is not required if certain conditions are met, such as when the data was rendered unintelligible (e.g., encrypted) through appropriate technical and organisational measures, when subsequent measures ensure the high risk is no longer likely to materialise, or if it would involve disproportionate effort (in which case a public communication or similar measure is used instead) (GDPR, Article 34).

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 33 - Notification of a personal data breach to the supervisory authority  (distance 0.216)
GDPR, Article 33: Notification of a personal data breach to the supervisory authority
1. In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority competent in accordance with Article 55, unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where the notification to the supervisory authority is not made within 72 hours, it shall be accompanied by reasons for the delay.
2. The processor shall notify the controller without undue delay after becoming aware of a personal data breach.
3. The notification referred to in paragraph 1 shall at least:
(a) describe the nature of the personal data breach including where possible, the categories and approximate number of data subjects concerned and the categories and approximate number of personal data records concerned;
(b) communicate the name and contact details of the data protection officer or other contact point where more information can be obtained;
(c) describe the likely consequences of the personal data breach;
(d) describe the measures taken or proposed to be taken by the controller to address the personal data breach, including, where appropriate, measures to mitigate its possible adverse effects.
4. Where, and in so far as, it is not possible to provide the information at the same time, the information may be provided in phases without undue further delay.
5. The controller shall document any personal data breaches, comprising the facts relating to the personal data breach, its effects and the remedial action taken. That documentation shall enable the supervisory authority to verify compliance with this Article.

---

[2] GDPR, Article 34 - Communication of a personal data breach to the data subject  (distance 0.263)
GDPR, Article 34: Communication of a personal data breach to the data subject
1. When the personal data breach is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall communicate the personal data breach to the data subject without undue delay.
2. The communication to the data subject referred to in paragraph 1 of this Article shall describe in clear and plain language the nature of the personal data breach and contain at least the information and measures referred to in points (b), (c) and (d) of Article 33(3).
3. The communication to the data subject referred to in paragraph 1 shall not be required if any of the following conditions are met:
(a) the controller has implemented appropriate technical and organisational protection measures, and those measures were applied to the personal data affected by the personal data breach, in particular those that render the personal data unintelligible to any person who is not authorised to access it, such as encryption;
(b) the controller has taken subsequent measures which ensure that the high risk to the rights and freedoms of data subjects referred to in paragraph 1 is no longer likely to materialise;
(c) it would involve disproportionate effort. In such a case, there shall instead be a public communication or similar measure whereby the data subjects are informed in an equally effective manner.
4. If the controller has not already communicated the personal data breach to the data subject, the supervisory authority, having considered the likelihood of the personal data breach resulting in a high risk, may require it to do so or may decide that any of the conditions referred to in paragraph 3 are met.

---

[3] GDPR, Article 66 - Urgency procedure  (distance 0.295)
GDPR, Article 66: Urgency procedure
1. In exceptional circumstances, where a supervisory authority concerned considers that there is an urgent need to act in order to protect the rights and freedoms of data subjects, it may, by way of derogation from the consistency mechanism referred to in Articles 63, 64 and 65 or the procedure referred to in Article 60, immediately adopt provisional measures intended to produce legal effects on its own territory with a specified period of validity which shall not exceed three months. The supervisory authority shall, without delay, communicate those measures and the reasons for adopting them to the other supervisory authorities concerned, to the Board and to the Commission.
2. Where a supervisory authority has taken a measure pursuant to paragraph 1 and considers that final measures need urgently be adopted, it may request an urgent opinion or an urgent binding decision from the Board, giving reasons for requesting such opinion or decision.
3. Any supervisory authority may request an urgent opinion or an urgent binding decision, as the case may be, from the Board where a competent supervisory authority has not taken an appropriate measure in a situation where there is an urgent need to act, in order to protect the rights and freedoms of data subjects, giving reasons for requesting such opinion or decision, including for the urgent need to act.
4. By derogation from Article 64(3) and Article 65(2), an urgent opinion or an urgent binding decision referred to in paragraphs 2 and 3 of this Article shall be adopted within two weeks by simple majority of the members of the Board.

---

[4] GDPR, Article 77 - Right to lodge a complaint with a supervisory authority  (distance 0.306)
GDPR, Article 77: Right to lodge a complaint with a supervisory authority
1. Without prejudice to any other administrative or judicial remedy, every data subject shall have the right to lodge a complaint with a supervisory authority, in particular in the Member State of his or her habitual residence, place of work or place of the alleged infringement if the data subject considers that the processing of personal data relating to him or her infringes this Regulation.
2. The supervisory authority with which the complaint has been lodged shall inform the complainant on the progress and the outcome of the complaint including the possibility of a judicial remedy pursuant to Article 78.

---

[5] GDPR, Article 32 - Security of processing  (distance 0.314)
GDPR, Article 32: Security of processing
1. Taking into account the state of the art, the costs of implementation and the nature, scope, context and purposes of processing as well as the risk of varying likelihood and severity for the rights and freedoms of natural persons, the controller and the processor shall implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk, including inter alia as appropriate:
(a) the pseudonymisation and encryption of personal data;
(b) the ability to ensure the ongoing confidentiality, integrity, availability and resilience of processing systems and services;
(c) the ability to restore the availability and access to personal data in a timely manner in the event of a physical or technical incident;
(d) a process for regularly testing, assessing and evaluating the effectiveness of technical and organisational measures for ensuring the security of the processing.
2. In assessing the appropriate level of security account shall be taken in particular of the risks that are presented by processing, in particular from accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to personal data transmitted, stored or otherwise processed.
3. Adherence to an approved code of conduct as referred to in Article 40 or an approved certification mechanism as referred to in Article 42 may be used as an element by which to demonstrate compliance with the requirements set out in paragraph 1 of this Article.
4. The controller and processor shall take steps to ensure that any natural person acting under the authority of the controller or the processor who has access to personal data does not process them except on instructions from the controller, unless he or she is required to do so by Union or Member State law.
```
</details>


---

## q21 (multi)

**Question:** If we process children's data for an online service without parental consent where it is needed, what is the maximum fine?

**Reference answer:** Art. 8 requires parental consent below the age of 16 (or lower national age, not below 13). Breaching Art. 8 falls under Art. 83(4): up to EUR 10 million or 2% of worldwide annual turnover, whichever is higher.

**Agent answer:**

Infringements of the obligations of the controller pursuant to Article 8 (which governs conditions applicable to child's consent in relation to information society services) shall be subject to administrative fines up to 10 000 000 EUR, or in the case of an undertaking, up to 2 % of the total worldwide annual turnover of the preceding financial year, whichever is higher, in accordance with the general conditions for imposing administrative fines.

(GDPR, Article 83, paragraph 4(a))

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 83 - General conditions for imposing administrative fines, part 1/3  (distance 0.228)
GDPR, Article 83: General conditions for imposing administrative fines
1. Each supervisory authority shall ensure that the imposition of administrative fines pursuant to this Article in respect of infringements of this Regulation referred to in paragraphs 4, 5 and 6 shall in each individual case be effective, proportionate and dissuasive.
2. Administrative fines shall, depending on the circumstances of each individual case, be imposed in addition to, or instead of, measures referred to in points (a) to (h) and (j) of Article 58(2). When deciding whether to impose an administrative fine and deciding on the amount of the administrative fine in each individual case due regard shall be given to the following:
(a) the nature, gravity and duration of the infringement taking into account the nature scope or purpose of the processing concerned as well as the number of data subjects affected and the level of damage suffered by them;
(b) the intentional or negligent character of the infringement;
(c) any action taken by the controller or processor to mitigate the damage suffered by data subjects;
(d) the degree of responsibility of the controller or processor taking into account technical and organisational measures implemented by them pursuant to Articles 25 and 32;
(e) any relevant previous infringements by the controller or processor;
(f) the degree of cooperation with the supervisory authority, in order to remedy the infringement and mitigate the possible adverse effects of the infringement;
(g) the categories of personal data affected by the infringement;
(h) the manner in which the infringement became known to the supervisory authority, in particular whether, and if so to what extent, the controller or processor notified the infringement;
(i) where measures referred to in Article 58(2) have previously been ordered against the controller or processor concerned with regard to the same subject-matter, compliance with those measures;
(j) adherence to approved codes of conduct pursuant to Article 40 or approved certification mechanisms pursuant to Article 42; and
(k) any other aggravating or mitigating factor applicable to the circumstances of the case, such as financial benefits gained, or losses avoided, directly or indirectly, from the infringement.

---

[2] GDPR, Article 8 - Conditions applicable to child's consent in relation to information society services  (distance 0.230)
GDPR, Article 8: Conditions applicable to child's consent in relation to information society services
1. Where point (a) of Article 6(1) applies, in relation to the offer of information society services directly to a child, the processing of the personal data of a child shall be lawful where the child is at least 16 years old. Where the child is below the age of 16 years, such processing shall be lawful only if and to the extent that consent is given or authorised by the holder of parental responsibility over the child.
Member States may provide by law for a lower age for those purposes provided that such lower age is not below 13 years.
2. The controller shall make reasonable efforts to verify in such cases that consent is given or authorised by the holder of parental responsibility over the child, taking into consideration available technology.
3. Paragraph 1 shall not affect the general contract law of Member States such as the rules on the validity, formation or effect of a contract in relation to a child.

---

[3] GDPR, Article 83 - General conditions for imposing administrative fines, part 2/3  (distance 0.232)
GDPR, Article 83: General conditions for imposing administrative fines
3. If a controller or processor intentionally or negligently, for the same or linked processing operations, infringes several provisions of this Regulation, the total amount of the administrative fine shall not exceed the amount specified for the gravest infringement.
4. Infringements of the following provisions shall, in accordance with paragraph 2, be subject to administrative fines up to 10 000 000 EUR, or in the case of an undertaking, up to 2 % of the total worldwide annual turnover of the preceding financial year, whichever is higher:
(a) the obligations of the controller and the processor pursuant to Articles 8, 11, 25 to 39 and 42 and 43;
(b) the obligations of the certification body pursuant to Articles 42 and 43;
(c) the obligations of the monitoring body pursuant to Article 41(4).
5. Infringements of the following provisions shall, in accordance with paragraph 2, be subject to administrative fines up to 20 000 000 EUR, or in the case of an undertaking, up to 4 % of the total worldwide annual turnover of the preceding financial year, whichever is higher:
(a) the basic principles for processing, including conditions for consent, pursuant to Articles 5, 6, 7 and 9;
(b) the data subjects' rights pursuant to Articles 12 to 22;
(c) the transfers of personal data to a recipient in a third country or an international organisation pursuant to Articles 44 to 49;
(d) any obligations pursuant to Member State law adopted under Chapter IX;
(e) non-compliance with an order or a temporary or definitive limitation on processing or the suspension of data flows by the supervisory authority pursuant to Article 58(2) or failure to provide access in violation of Article 58(1).
6. Non-compliance with an order by the supervisory authority as referred to in Article 58(2) shall, in accordance with paragraph 2 of this Article, be subject to administrative fines up to 20 000 000 EUR, or in the case of an undertaking, up to 4 % of the total worldwide annual turnover of the preceding financial year, whichever is higher.

---

[4] GDPR, Article 83 - General conditions for imposing administrative fines, part 3/3  (distance 0.251)
GDPR, Article 83: General conditions for imposing administrative fines
7. Without prejudice to the corrective powers of supervisory authorities pursuant to Article 58(2), each Member State may lay down the rules on whether and to what extent administrative fines may be imposed on public authorities and bodies established in that Member State.
8. The exercise by the supervisory authority of its powers under this Article shall be subject to appropriate procedural safeguards in accordance with Union and Member State law, including effective judicial remedy and due process.
9. Where the legal system of the Member State does not provide for administrative fines, this Article may be applied in such a manner that the fine is initiated by the competent supervisory authority and imposed by competent national courts, while ensuring that those legal remedies are effective and have an equivalent effect to the administrative fines imposed by supervisory authorities. In any event, the fines imposed shall be effective, proportionate and dissuasive. Those Member States shall notify to the Commission the provisions of their laws which they adopt pursuant to this paragraph by 25 May 2018 and, without delay, any subsequent amendment law or amendment affecting them.

---

[5] GDPR, Article 58 - Powers, part 2/3  (distance 0.275)
GDPR, Article 58: Powers
(h) to withdraw a certification or to order the certification body to withdraw a certification issued pursuant to Articles 42 and 43, or to order the certification body not to issue certification if the requirements for the certification are not or are no longer met;
(i) to impose an administrative fine pursuant to Article 83, in addition to, or instead of measures referred to in this paragraph, depending on the circumstances of each individual case;
(j) to order the suspension of data flows to a recipient in a third country or to an international organisation.
3. Each supervisory authority shall have all of the following authorisation and advisory powers:
(a) to advise the controller in accordance with the prior consultation procedure referred to in Article 36;
(b) to issue, on its own initiative or on request, opinions to the national parliament, the Member State government or, in accordance with Member State law, to other institutions and bodies as well as to the public on any issue related to the protection of personal data;
(c) to authorise processing referred to in Article 36(5), if the law of the Member State requires such prior authorisation;
(d) to issue an opinion and approve draft codes of conduct pursuant to Article 40(5);
(e) to accredit certification bodies pursuant to Article 43;
(f) to issue certifications and approve criteria of certification in accordance with Article 42(5);
(g) to adopt standard data protection clauses referred to in Article 28(8) and in point (d) of Article 46(2);
(h) to authorise contractual clauses referred to in point (a) of Article 46(3);
(i) to authorise administrative arrangements referred to in point (b) of Article 46(3);
(j) to approve binding corporate rules pursuant to Article 47.
4. The exercise of the powers conferred on the supervisory authority pursuant to this Article shall be subject to appropriate safeguards, including effective judicial remedy and due process, set out in Union and Member State law in accordance with the Charter.
```
</details>


---

## q22 (multi)

**Question:** We want to make fully automated decisions about loan applicants. Which rights of the applicant and which assessment obligation does that trigger?

**Reference answer:** Individuals have the right not to be subject to decisions based solely on automated processing, including profiling, with legal or similarly significant effects, subject to exceptions (Art. 22). Such systematic, profiling-based decision making also requires a data protection impact assessment (Art. 35(3)(a)).

**Agent answer:**

The data subject has the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning them or similarly significantly affects them, unless the decision is necessary for entering into or performing a contract, is authorised by law, or is based on explicit consent (GDPR, Article 22). 

If such a decision is necessary for entering into or performing a contract, or is based on explicit consent, the data controller must implement suitable measures to safeguard the data subject's rights, freedoms, and legitimate interests, which must include at least:
* The right to obtain human intervention on the part of the controller;
* The right to express their point of view; and
* The right to contest the decision.
(GDPR, Article 22)

Additionally, where decisions are based on automated processing, including profiling, that produce legal effects or similarly significantly affect the natural person, a systematic and extensive evaluation of personal aspects triggers an assessment obligation: the controller must, prior to the processing, carry out a data protection impact assessment of the impact of the envisaged processing operations on the protection of personal data (GDPR, Article 35).

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 22 - Automated individual decision-making, including profiling  (distance 0.219)
GDPR, Article 22: Automated individual decision-making, including profiling
1. The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her.
2. Paragraph 1 shall not apply if the decision:
(a) is necessary for entering into, or performance of, a contract between the data subject and a data controller;
(b) is authorised by Union or Member State law to which the controller is subject and which also lays down suitable measures to safeguard the data subject's rights and freedoms and legitimate interests; or
(c) is based on the data subject's explicit consent.
3. In the cases referred to in points (a) and (c) of paragraph 2, the data controller shall implement suitable measures to safeguard the data subject's rights and freedoms and legitimate interests, at least the right to obtain human intervention on the part of the controller, to express his or her point of view and to contest the decision.
4. Decisions referred to in paragraph 2 shall not be based on special categories of personal data referred to in Article 9(1), unless point (a) or (g) of Article 9(2) applies and suitable measures to safeguard the data subject's rights and freedoms and legitimate interests are in place.

---

[2] GDPR, Article 14 - Information to be provided where personal data have not been obtained from the data subject, part 2/3  (distance 0.297)
GDPR, Article 14: Information to be provided where personal data have not been obtained from the data subject
(f) from which source the personal data originate, and if applicable, whether it came from publicly accessible sources;
(g) the existence of automated decision-making, including profiling, referred to in Article 22(1) and (4) and, at least in those cases, meaningful information about the logic involved, as well as the significance and the envisaged consequences of such processing for the data subject.
3. The controller shall provide the information referred to in paragraphs 1 and 2:
(a) within a reasonable period after obtaining the personal data, but at the latest within one month, having regard to the specific circumstances in which the personal data are processed;
(b) if the personal data are to be used for communication with the data subject, at the latest at the time of the first communication to that data subject; or
(c) if a disclosure to another recipient is envisaged, at the latest when the personal data are first disclosed.
4. Where the controller intends to further process the personal data for a purpose other than that for which the personal data were obtained, the controller shall provide the data subject prior to that further processing with information on that other purpose and with any relevant further information as referred to in paragraph 2.
5. Paragraphs 1 to 4 shall not apply where and insofar as:
(a) the data subject already has the information;
(b) the provision of such information proves impossible or would involve a disproportionate effort, in particular for processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes, subject to the conditions and safeguards referred to in Article 89(1) or in so far as the obligation referred to in paragraph 1 of this Article is likely to render impossible or seriously impair the achievement of the objectives of that processing. In such cases the controller shall take appropriate measures to protect the data subject's rights and freedoms and legitimate interests, including making the information publicly available;

---

[3] GDPR, Article 35 - Data protection impact assessment, part 1/3  (distance 0.298)
GDPR, Article 35: Data protection impact assessment
1. Where a type of processing in particular using new technologies, and taking into account the nature, scope, context and purposes of the processing, is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall, prior to the processing, carry out an assessment of the impact of the envisaged processing operations on the protection of personal data. A single assessment may address a set of similar processing operations that present similar high risks.
2. The controller shall seek the advice of the data protection officer, where designated, when carrying out a data protection impact assessment.
3. A data protection impact assessment referred to in paragraph 1 shall in particular be required in the case of:
(a) a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person;
(b) processing on a large scale of special categories of data referred to in Article 9(1), or of personal data relating to criminal convictions and offences referred to in Article 10; or
(c) a systematic monitoring of a publicly accessible area on a large scale.
4. The supervisory authority shall establish and make public a list of the kind of processing operations which are subject to the requirement for a data protection impact assessment pursuant to paragraph 1. The supervisory authority shall communicate those lists to the Board referred to in Article 68.
5. The supervisory authority may also establish and make public a list of the kind of processing operations for which no data protection impact assessment is required. The supervisory authority shall communicate those lists to the Board.

---

[4] GDPR, Article 13 - Information to be provided where personal data are collected from the data subject, part 2/2  (distance 0.305)
GDPR, Article 13: Information to be provided where personal data are collected from the data subject
(d) the right to lodge a complaint with a supervisory authority;
(e) whether the provision of personal data is a statutory or contractual requirement, or a requirement necessary to enter into a contract, as well as whether the data subject is obliged to provide the personal data and of the possible consequences of failure to provide such data;
(f) the existence of automated decision-making, including profiling, referred to in Article 22(1) and (4) and, at least in those cases, meaningful information about the logic involved, as well as the significance and the envisaged consequences of such processing for the data subject.
3. Where the controller intends to further process the personal data for a purpose other than that for which the personal data were collected, the controller shall provide the data subject prior to that further processing with information on that other purpose and with any relevant further information as referred to in paragraph 2.
4. Paragraphs 1, 2 and 3 shall not apply where and insofar as the data subject already has the information.

---

[5] GDPR, Article 6 - Lawfulness of processing, part 1/3  (distance 0.315)
GDPR, Article 6: Lawfulness of processing
1. Processing shall be lawful only if and to the extent that at least one of the following applies:
(a) the data subject has given consent to the processing of his or her personal data for one or more specific purposes;
(b) processing is necessary for the performance of a contract to which the data subject is party or in order to take steps at the request of the data subject prior to entering into a contract;
(c) processing is necessary for compliance with a legal obligation to which the controller is subject;
(d) processing is necessary in order to protect the vital interests of the data subject or of another natural person;
(e) processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller;
(f) processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject which require protection of personal data, in particular where the data subject is a child.
Point (f) of the first subparagraph shall not apply to processing carried out by public authorities in the performance of their tasks.
2. Member States may maintain or introduce more specific provisions to adapt the application of the rules of this Regulation with regard to processing for compliance with points (c) and (e) of paragraph 1 by determining more precisely specific requirements for the processing and other measures to ensure lawful and fair processing including for other specific processing situations as provided for in Chapter IX.
3. The basis for the processing referred to in point (c) and (e) of paragraph 1 shall be laid down by:
(a) Union law; or
(b) Member State law to which the controller is subject.
```
</details>


---

## q23 (multi)

**Question:** How can we transfer personal data to a country that has no adequacy decision?

**Reference answer:** Only with appropriate safeguards and enforceable data subject rights and remedies (Art. 46, e.g. binding corporate rules), or, absent safeguards, under one of the specific derogations in Art. 49.

**Agent answer:**

In the absence of an adequacy decision, a controller or processor may transfer personal data to a third country or international organisation only if they have provided appropriate safeguards, and on condition that enforceable data subject rights and effective legal remedies for data subjects are available (GDPR, Article 46). 

Appropriate safeguards can be provided without requiring specific authorisation from a supervisory authority by:
* A legally binding and enforceable instrument between public authorities or bodies (GDPR, Article 46);
* Binding corporate rules in accordance with Article 47 (GDPR, Article 46);
* Standard data protection clauses adopted by the Commission (GDPR, Article 46);
* Standard data protection clauses adopted by a supervisory authority and approved by the Commission (GDPR, Article 46);
* An approved code of conduct pursuant to Article 40 together with binding and enforceable commitments of the controller or processor in the third country to apply the appropriate safeguards (GDPR, Article 46); or
* An approved certification mechanism pursuant to Article 42 together with binding and enforceable commitments of the controller or processor in the third country to apply the appropriate safeguards (GDPR, Article 46).

Subject to authorisation from the competent supervisory authority, appropriate safeguards may also be provided by:
* Contractual clauses between the controller or processor and the controller, processor or the recipient of the personal data in the third country or international organisation (GDPR, Article 46); or
* Provisions to be inserted into administrative arrangements between public authorities or bodies which include enforceable and effective data subject rights (GDPR, Article 46).

In the absence of an adequacy decision or appropriate safeguards, a transfer or set of transfers may take place only under specific derogations, such as explicit consent from the data subject after being informed of the risks, necessity for the performance of a contract, important reasons of public interest, or for the establishment, exercise, or defence of legal claims (GDPR, Article 49).

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 45 - Transfers on the basis of an adequacy decision, part 1/3  (distance 0.157)
GDPR, Article 45: Transfers on the basis of an adequacy decision
1. A transfer of personal data to a third country or an international organisation may take place where the Commission has decided that the third country, a territory or one or more specified sectors within that third country, or the international organisation in question ensures an adequate level of protection. Such a transfer shall not require any specific authorisation.
2. When assessing the adequacy of the level of protection, the Commission shall, in particular, take account of the following elements:
(a) the rule of law, respect for human rights and fundamental freedoms, relevant legislation, both general and sectoral, including concerning public security, defence, national security and criminal law and the access of public authorities to personal data, as well as the implementation of such legislation, data protection rules, professional rules and security measures, including rules for the onward transfer of personal data to another third country or international organisation which are complied with in that country or international organisation, case-law, as well as effective and enforceable data subject rights and effective administrative and judicial redress for the data subjects whose personal data are being transferred;
(b) the existence and effective functioning of one or more independent supervisory authorities in the third country or to which an international organisation is subject, with responsibility for ensuring and enforcing compliance with the data protection rules, including adequate enforcement powers, for assisting and advising the data subjects in exercising their rights and for cooperation with the supervisory authorities of the Member States; and
(c) the international commitments the third country or international organisation concerned has entered into, or other obligations arising from legally binding conventions or instruments as well as from its participation in multilateral or regional systems, in particular in relation to the protection of personal data.

---

[2] GDPR, Article 46 - Transfers subject to appropriate safeguards, part 1/2  (distance 0.194)
GDPR, Article 46: Transfers subject to appropriate safeguards
1. In the absence of a decision pursuant to Article 45(3), a controller or processor may transfer personal data to a third country or an international organisation only if the controller or processor has provided appropriate safeguards, and on condition that enforceable data subject rights and effective legal remedies for data subjects are available.
2. The appropriate safeguards referred to in paragraph 1 may be provided for, without requiring any specific authorisation from a supervisory authority, by:
(a) a legally binding and enforceable instrument between public authorities or bodies;
(b) binding corporate rules in accordance with Article 47;
(c) standard data protection clauses adopted by the Commission in accordance with the examination procedure referred to in Article 93(2);
(d) standard data protection clauses adopted by a supervisory authority and approved by the Commission pursuant to the examination procedure referred to in Article 93(2);
(e) an approved code of conduct pursuant to Article 40 together with binding and enforceable commitments of the controller or processor in the third country to apply the appropriate safeguards, including as regards data subjects' rights; or
(f) an approved certification mechanism pursuant to Article 42 together with binding and enforceable commitments of the controller or processor in the third country to apply the appropriate safeguards, including as regards data subjects' rights.
3. Subject to the authorisation from the competent supervisory authority, the appropriate safeguards referred to in paragraph 1 may also be provided for, in particular, by:
(a) contractual clauses between the controller or processor and the controller, processor or the recipient of the personal data in the third country or international organisation; or
(b) provisions to be inserted into administrative arrangements between public authorities or bodies which include enforceable and effective data subject rights.
4. The supervisory authority shall apply the consistency mechanism referred to in Article 63 in the cases referred to in paragraph 3 of this Article.

---

[3] GDPR, Article 45 - Transfers on the basis of an adequacy decision, part 2/3  (distance 0.203)
GDPR, Article 45: Transfers on the basis of an adequacy decision
3. The Commission, after assessing the adequacy of the level of protection, may decide, by means of implementing act, that a third country, a territory or one or more specified sectors within a third country, or an international organisation ensures an adequate level of protection within the meaning of paragraph 2 of this Article. The implementing act shall provide for a mechanism for a periodic review, at least every four years, which shall take into account all relevant developments in the third country or international organisation. The implementing act shall specify its territorial and sectoral application and, where applicable, identify the supervisory authority or authorities referred to in point (b) of paragraph 2 of this Article. The implementing act shall be adopted in accordance with the examination procedure referred to in Article 93(2).
4. The Commission shall, on an ongoing basis, monitor developments in third countries and international organisations that could affect the functioning of decisions adopted pursuant to paragraph 3 of this Article and decisions adopted on the basis of Article 25(6) of Directive 95/46/EC.
5. The Commission shall, where available information reveals, in particular following the review referred to in paragraph 3 of this Article, that a third country, a territory or one or more specified sectors within a third country, or an international organisation no longer ensures an adequate level of protection within the meaning of paragraph 2 of this Article, to the extent necessary, repeal, amend or suspend the decision referred to in paragraph 3 of this Article by means of implementing acts without retro-active effect. Those implementing acts shall be adopted in accordance with the examination procedure referred to in Article 93(2).
On duly justified imperative grounds of urgency, the Commission shall adopt immediately applicable implementing acts in accordance with the procedure referred to in Article 93(3).
6. The Commission shall enter into consultations with the third country or international organisation with a view to remedying the situation giving rise to the decision made pursuant to paragraph 5.

---

[4] GDPR, Article 49 - Derogations for specific situations, part 1/3  (distance 0.217)
GDPR, Article 49: Derogations for specific situations
1. In the absence of an adequacy decision pursuant to Article 45(3), or of appropriate safeguards pursuant to Article 46, including binding corporate rules, a transfer or a set of transfers of personal data to a third country or an international organisation shall take place only on one of the following conditions:
(a) the data subject has explicitly consented to the proposed transfer, after having been informed of the possible risks of such transfers for the data subject due to the absence of an adequacy decision and appropriate safeguards;
(b) the transfer is necessary for the performance of a contract between the data subject and the controller or the implementation of pre-contractual measures taken at the data subject's request;
(c) the transfer is necessary for the conclusion or performance of a contract concluded in the interest of the data subject between the controller and another natural or legal person;
(d) the transfer is necessary for important reasons of public interest;
(e) the transfer is necessary for the establishment, exercise or defence of legal claims;
(f) the transfer is necessary in order to protect the vital interests of the data subject or of other persons, where the data subject is physically or legally incapable of giving consent;
(g) the transfer is made from a register which according to Union or Member State law is intended to provide information to the public and which is open to consultation either by the public in general or by any person who can demonstrate a legitimate interest, but only to the extent that the conditions laid down by Union or Member State law for consultation are fulfilled in the particular case.

---

[5] GDPR, Article 49 - Derogations for specific situations, part 3/3  (distance 0.222)
GDPR, Article 49: Derogations for specific situations
5. In the absence of an adequacy decision, Union or Member State law may, for important reasons of public interest, expressly set limits to the transfer of specific categories of personal data to a third country or an international organisation. Member States shall notify such provisions to the Commission.
6. The controller or processor shall document the assessment as well as the suitable safeguards referred to in the second subparagraph of paragraph 1 of this Article in the records referred to in Article 30.
```
</details>


---

## q24 (multi)

**Question:** How does a user's right to get their connected-device data passed to another company relate to the GDPR right to data portability?

**Reference answer:** Data Act Art. 5: on the user's request the data holder must make product and related-service data available to a third party, free of charge to the user. GDPR Art. 20: a person can receive personal data they provided and have it transmitted to another controller where processing is based on consent or contract and automated. The Data Act rights complement the GDPR rights (Art. 1(5)).

**Agent answer:**

Any failure by the data holder and the third party to agree on arrangements for transmitting the data shall not hinder, prevent, or interfere with the exercise of the rights of the data subject under Regulation (EU) 2016/679, and in particular with the right to data portability under Article 20 of that Regulation (Data Act, Article 5).

Furthermore, where the user is not the data subject whose personal data is requested, any personal data generated by the use of a connected product or related service shall only be made available to the third party if there is a valid legal basis for processing under Article 6 of Regulation (EU) 2016/679 and, where relevant, the conditions of Article 9 of that Regulation and Article 5(3) of Directive 2002/58/EC are fulfilled (Data Act, Article 5).

<details><summary>Retrieved passages</summary>

```
[1] Data Act, Article 5 - Right of the user to share data with third parties, part 1/4  (distance 0.168)
Data Act, Article 5: Right of the user to share data with third parties
1. Upon request by a user, or by a party acting on behalf of a user, the data holder shall make available readily available data, as well as the relevant metadata necessary to interpret and use those data, to a third party without undue delay, of the same quality as is available to the data holder, easily, securely, free of charge to the user, in a comprehensive, structured, commonly used and machine-readable format and, where relevant and technically feasible, continuously and in real-time. The data shall be made available by the data holder to the third party in accordance with Articles 8 and 9.
2. Paragraph 1 shall not apply to readily available data in the context of the testing of new connected products, substances or processes that are not yet placed on the market unless their use by a third party is contractually permitted.
3. Any undertaking designated as a gatekeeper, pursuant to Article 3 of Regulation (EU) 2022/1925, shall not be an eligible third party under this Article and therefore shall not:
(a) solicit or commercially incentivise a user in any manner, including by providing monetary or any other compensation, to make data available to one of its services that the user has obtained pursuant to a request under Article 4(1);
(b) solicit or commercially incentivise a user to request the data holder to make data available to one of its services pursuant to paragraph 1 of this Article;
(c) receive data from a user that the user has obtained pursuant to a request under Article 4(1).
4. For the purpose of verifying whether a natural or legal person qualifies as a user or as a third party for the purposes of paragraph 1, the user or the third party shall not be required to provide any information beyond what is necessary. Data holders shall not keep any information on the third party’s access to the data requested beyond what is necessary for the sound execution of the third party’s access request and for the security and maintenance of the data infrastructure.

---

[2] Data Act, Article 6 - Obligations of third parties receiving data at the request of the user, part 1/2  (distance 0.193)
Data Act, Article 6: Obligations of third parties receiving data at the request of the user
1. A third party shall process the data made available to it pursuant to Article 5 only for the purposes and under the conditions agreed with the user and subject to Union and national law on the protection of personal data including the rights of the data subject insofar as personal data are concerned. The third party shall erase the data when they are no longer necessary for the agreed purpose, unless otherwise agreed with the user in relation to non-personal data.
2. The third party shall not:
(a) make the exercise of choices or rights under Article 5 and this Article by the user unduly difficult, including by offering choices to the user in a non-neutral manner, or by coercing, deceiving or manipulating the user, or by subverting or impairing the autonomy, decision-making or choices of the user, including by means of a user digital interface or a part thereof;
(b) notwithstanding Article 22(2), points (a) and (c), of Regulation (EU) 2016/679, use the data it receives for the profiling, unless it is necessary to provide the service requested by the user;
(c) make the data it receives available to another third party, unless the data is made available on the basis of a contract with the user, and provided that the other third party takes all necessary measures agreed between the data holder and the third party to preserve the confidentiality of trade secrets;
(d) make the data it receives available to an undertaking designated as a gatekeeper pursuant to Article 3 of Regulation (EU) 2022/1925;
(e) use the data it receives to develop a product that competes with the connected product from which the accessed data originate or share the data with another third party for that purpose; third parties shall also not use any non-personal product data or related service data made available to them to derive insights about the economic situation, assets and production methods of, or use by, the data holder;

---

[3] Data Act, Article 4 - The rights and obligations of users and data holders with regard to access, use and making available product data and related service data, part 1/4  (distance 0.199)
Data Act, Article 4: The rights and obligations of users and data holders with regard to access, use and making available product data and related service data
1. Where data cannot be directly accessed by the user from the connected product or related service, data holders shall make readily available data, as well as the relevant metadata necessary to interpret and use those data, accessible to the user without undue delay, of the same quality as is available to the data holder, easily, securely, free of charge, in a comprehensive, structured, commonly used and machine-readable format and, where relevant and technically feasible, continuously and in real-time. This shall be done on the basis of a simple request through electronic means where technically feasible.
2. Users and data holders may contractually restrict or prohibit accessing, using or further sharing data, if such processing could undermine security requirements of the connected product, as laid down by Union or national law, resulting in a serious adverse effect on the health, safety or security of natural persons. Sectoral authorities may provide users and data holders with technical expertise in that context. Where the data holder refuses to share data pursuant to this Article, it shall notify the competent authority designated pursuant to Article 37.
3. Without prejudice to the user’s right to seek redress at any stage before a court or tribunal of a Member State, the user may, in relation to any dispute with the data holder concerning the contractual restrictions or prohibitions referred to in paragraph 2:
(a) lodge, in accordance with Article 37(5), point (b), a complaint with the competent authority; or
(b) agree with the data holder to refer the matter to a dispute settlement body in accordance with Article 10(1).
4. Data holders shall not make the exercise of choices or rights under this Article by the user unduly difficult, including by offering choices to the user in a non-neutral manner or by subverting or impairing the autonomy, decision-making or choices of the user via the structure, design, function or manner of operation of a user digital interface or a part thereof.

---

[4] Data Act, Article 5 - Right of the user to share data with third parties, part 2/4  (distance 0.200)
Data Act, Article 5: Right of the user to share data with third parties
5. The third party shall not use coercive means or abuse gaps in the technical infrastructure of a data holder which is designed to protect the data in order to obtain access to data.
6. A data holder shall not use any readily available data to derive insights about the economic situation, assets and production methods of, or the use by, the third party in any other manner that could undermine the commercial position of the third party on the markets in which the third party is active, unless the third party has given permission to such use and has the technical possibility to easily withdraw that permission at any time.
7. Where the user is not the data subject whose personal data is requested, any personal data generated by the use of a connected product or related service shall be made available by the data holder to the third party only where there is a valid legal basis for processing under Article 6 of Regulation (EU) 2016/679 and, where relevant, the conditions of Article 9 of that Regulation and of Article 5(3) of Directive 2002/58/EC are fulfilled.
8. Any failure on the part of the data holder and the third party to agree on arrangements for transmitting the data shall not hinder, prevent or interfere with the exercise of the rights of the data subject under Regulation (EU) 2016/679 and, in particular, with the right to data portability under Article 20 of that Regulation.

---

[5] Data Act, Article 1 - Subject matter and scope, part 1/3  (distance 0.201)
Data Act, Article 1: Subject matter and scope
1. This Regulation lays down harmonised rules, inter alia, on:
(a) the making available of product data and related service data to the user of the connected product or related service;
(b) the making available of data by data holders to data recipients;
(c) the making available of data by data holders to public sector bodies, the Commission, the European Central Bank and Union bodies, where there is an exceptional need for those data for the performance of a specific task carried out in the public interest;
(d) facilitating switching between data processing services;
(e) introducing safeguards against unlawful third-party access to non-personal data; and
(f) the development of interoperability standards for data to be accessed, transferred and used.
2. This Regulation covers personal and non-personal data, including the following types of data, in the following contexts:
(a) Chapter II applies to data, with the exception of content, concerning the performance, use and environment of connected products and related services;
(b) Chapter III applies to any private sector data that is subject to statutory data sharing obligations;
(c) Chapter IV applies to any private sector data accessed and used on the basis of contract between enterprises;
(d) Chapter V applies to any private sector data with a focus on non-personal data;
(e) Chapter VI applies to any data and services processed by providers of data processing services;
(f) Chapter VII applies to any non-personal data held in the Union by providers of data processing services.
3. This Regulation applies to:
(a) manufacturers of connected products placed on the market in the Union and providers of related services, irrespective of the place of establishment of those manufacturers and providers;
(b) users in the Union of connected products or related services as referred to in point (a);
(c) data holders, irrespective of their place of establishment, that make data available to data recipients in the Union;
(d) data recipients in the Union to whom data are made available;

---

[1] GDPR, Article 20 - Right to data portability  (distance 0.161)
GDPR, Article 20: Right to data portability
1. The data subject shall have the right to receive the personal data concerning him or her, which he or she has provided to a controller, in a structured, commonly used and machine-readable format and have the right to transmit those data to another controller without hindrance from the controller to which the personal data have been provided, where:
(a) the processing is based on consent pursuant to point (a) of Article 6(1) or point (a) of Article 9(2) or on a contract pursuant to point (b) of Article 6(1); and
(b) the processing is carried out by automated means.
2. In exercising his or her right to data portability pursuant to paragraph 1, the data subject shall have the right to have the personal data transmitted directly from one controller to another, where technically feasible.
3. The exercise of the right referred to in paragraph 1 of this Article shall be without prejudice to Article 17. That right shall not apply to processing necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller.
4. The right referred to in paragraph 1 shall not adversely affect the rights and freedoms of others.

---

[2] Data Act, Article 5 - Right of the user to share data with third parties, part 1/4  (distance 0.203)
Data Act, Article 5: Right of the user to share data with third parties
1. Upon request by a user, or by a party acting on behalf of a user, the data holder shall make available readily available data, as well as the relevant metadata necessary to interpret and use those data, to a third party without undue delay, of the same quality as is available to the data holder, easily, securely, free of charge to the user, in a comprehensive, structured, commonly used and machine-readable format and, where relevant and technically feasible, continuously and in real-time. The data shall be made available by the data holder to the third party in accordance with Articles 8 and 9.
2. Paragraph 1 shall not apply to readily available data in the context of the testing of new connected products, substances or processes that are not yet placed on the market unless their use by a third party is contractually permitted.
3. Any undertaking designated as a gatekeeper, pursuant to Article 3 of Regulation (EU) 2022/1925, shall not be an eligible third party under this Article and therefore shall not:
(a) solicit or commercially incentivise a user in any manner, including by providing monetary or any other compensation, to make data available to one of its services that the user has obtained pursuant to a request under Article 4(1);
(b) solicit or commercially incentivise a user to request the data holder to make data available to one of its services pursuant to paragraph 1 of this Article;
(c) receive data from a user that the user has obtained pursuant to a request under Article 4(1).
4. For the purpose of verifying whether a natural or legal person qualifies as a user or as a third party for the purposes of paragraph 1, the user or the third party shall not be required to provide any information beyond what is necessary. Data holders shall not keep any information on the third party’s access to the data requested beyond what is necessary for the sound execution of the third party’s access request and for the security and maintenance of the data infrastructure.

---

[3] Data Act, Article 26 - Information obligation of providers of data processing services  (distance 0.204)
Data Act, Article 26: Information obligation of providers of data processing services
The provider of data processing services shall provide the customer with:
(a) information on available procedures for switching and porting to the data processing service, including information on available switching and porting methods and formats as well as restrictions and technical limitations which are known to the provider of data processing services;
(b) a reference to an up-to-date online register hosted by the provider of data processing services, with details of all the data structures and data formats as well as the relevant standards and open interoperability specifications, in which the exportable data referred to in Article 25(2), point (e), are available.

---

[4] Data Act, Article 38 - Right to lodge a complaint  (distance 0.208)
Data Act, Article 38: Right to lodge a complaint
1. Without prejudice to any other administrative or judicial remedy, natural and legal persons shall have the right to lodge a complaint, individually or, where relevant, collectively, with the relevant competent authority in the Member State of their habitual residence, place of work or establishment if they consider that their rights under this Regulation have been infringed. The data coordinator shall, upon request, provide all the necessary information to natural and legal persons for the lodging of their complaints with the appropriate competent authority.
2. The competent authority with which the complaint has been lodged shall inform the complainant, in accordance with national law, of the progress of the proceedings and of the decision taken.
3. Competent authorities shall cooperate to handle and resolve complaints effectively and in a timely manner, including by exchanging all relevant information by electronic means, without undue delay. This cooperation shall not affect the cooperation mechanisms provided for by Chapters VI and VII of Regulation (EU) 2016/679 and by Regulation (EU) 2017/2394.

---

[5] Data Act, Article 1 - Subject matter and scope, part 1/3  (distance 0.210)
Data Act, Article 1: Subject matter and scope
1. This Regulation lays down harmonised rules, inter alia, on:
(a) the making available of product data and related service data to the user of the connected product or related service;
(b) the making available of data by data holders to data recipients;
(c) the making available of data by data holders to public sector bodies, the Commission, the European Central Bank and Union bodies, where there is an exceptional need for those data for the performance of a specific task carried out in the public interest;
(d) facilitating switching between data processing services;
(e) introducing safeguards against unlawful third-party access to non-personal data; and
(f) the development of interoperability standards for data to be accessed, transferred and used.
2. This Regulation covers personal and non-personal data, including the following types of data, in the following contexts:
(a) Chapter II applies to data, with the exception of content, concerning the performance, use and environment of connected products and related services;
(b) Chapter III applies to any private sector data that is subject to statutory data sharing obligations;
(c) Chapter IV applies to any private sector data accessed and used on the basis of contract between enterprises;
(d) Chapter V applies to any private sector data with a focus on non-personal data;
(e) Chapter VI applies to any data and services processed by providers of data processing services;
(f) Chapter VII applies to any non-personal data held in the Union by providers of data processing services.
3. This Regulation applies to:
(a) manufacturers of connected products placed on the market in the Union and providers of related services, irrespective of the place of establishment of those manufacturers and providers;
(b) users in the Union of connected products or related services as referred to in point (a);
(c) data holders, irrespective of their place of establishment, that make data available to data recipients in the Union;
(d) data recipients in the Union to whom data are made available;
```
</details>


---

## q25 (multi)

**Question:** What fines can apply if a manufacturer breaches the Data Act's rules on giving users access to their product data?

**Reference answer:** Member States set penalties, but for breaches of Chapters II, III and V the data protection supervisory authorities may impose administrative fines under GDPR Art. 83, up to the amount in Art. 83(5): EUR 20 million or 4% of worldwide annual turnover, whichever is higher.

**Agent answer:**

Member States are required to lay down rules on penalties for infringements of the Data Act and ensure they are implemented, with such penalties being effective, proportionate, and dissuasive (Data Act, Article 40(1)). 

When imposing penalties, Member States must take into account recommendations of the European Data Innovation Board (EDIB) and non-exhaustive criteria including:
* the nature, gravity, scale, and duration of the infringement;
* any action taken by the infringing party to mitigate or remedy the damage caused;
* any previous infringements by the infringing party;
* financial benefits gained or losses avoided by the infringing party, where reliably established;
* any other aggravating or mitigating factors;
* the infringing party's annual turnover in the preceding financial year in the Union.
(Data Act, Article 40(3))

Additionally, for infringements of obligations laid down in Chapters II, III, and V of the Data Act, supervisory authorities responsible for monitoring the GDPR (Regulation (EU) 2016/679) may, within their scope of competence, impose administrative fines in accordance with Article 83 of Regulation (EU) 2016/679 and up to the amount referred to in Article 83(5) of that Regulation (Data Act, Article 40(4)). Competent authorities may also impose effective, proportionate, and dissuasive financial penalties, which may include periodic penalties and penalties with retroactive effect, or initiate legal proceedings for fines (Data Act, Article 37(5)).

<details><summary>Retrieved passages</summary>

```
[1] Data Act, Article 40 - Penalties  (distance 0.177)
Data Act, Article 40: Penalties
1. Member States shall lay down the rules on penalties applicable to infringements of this Regulation and shall take all measures necessary to ensure that they are implemented. The penalties provided for shall be effective, proportionate and dissuasive.
2. Member States shall by 12 September 2025 notify the Commission of those rules and measures and shall notify it without delay of any subsequent amendment affecting them. The Commission shall regularly update and maintain an easily accessible public register of those measures.
3. Member States shall take into account the recommendations of the EDIB and the following non-exhaustive criteria for the imposition of penalties for infringements of this Regulation:
(a) the nature, gravity, scale and duration of the infringement;
(b) any action taken by the infringing party to mitigate or remedy the damage caused by the infringement;
(c) any previous infringements by the infringing party;
(d) the financial benefits gained or losses avoided by the infringing party due to the infringement, insofar as such benefits or losses can be reliably established;
(e) any other aggravating or mitigating factor applicable to the circumstances of the case;
(f) infringing party’s annual turnover in the preceding financial year in the Union.
4. For infringements of the obligations laid down in Chapter II, III and V of this Regulation, the supervisory authorities responsible for monitoring the application of Regulation (EU) 2016/679 may within their scope of competence impose administrative fines in accordance with Article 83 of Regulation (EU) 2016/679 and up to the amount referred to in Article 83(5) of that Regulation.
5. For infringements of the obligations laid down in Chapter V of this Regulation, the European Data Protection Supervisor may impose within its scope of competence administrative fines in accordance with Article 66 of Regulation (EU) 2018/1725 up to the amount referred to in Article 66(3) of that Regulation.

---

[2] Data Act, Article 37 - Competent authorities and data coordinators, part 4/5  (distance 0.206)
Data Act, Article 37: Competent authorities and data coordinators
12. For the purpose of ensuring compliance with this Regulation, a legal representative shall be mandated by an entity falling within the scope of this Regulation that makes connected products available or offers services in the Union to be addressed in addition to or instead of it by competent authorities with regard to all issues related to that entity. That legal representative shall cooperate with and comprehensively demonstrate to the competent authorities, upon request, the actions taken and provisions put in place by the entity falling within the scope of this Regulation that makes connected products available or offers services in the Union to ensure compliance with this Regulation.
13. An entity falling within the scope of this Regulation that makes connected products available or offers services in the Union, shall be considered to be under the competence of the Member State in which its legal representative is located. The designation of a legal representative by such an entity shall be without prejudice to the liability of, and any legal action that could be initiated against, such an entity. Until such time as an entity designates a legal representative in accordance with this Article, it shall be under the competence of all Member States, where applicable, for the purposes of ensuring the application and enforcement of this Regulation. Any competent authority may exercise its competence, including by imposing effective, proportionate and dissuasive penalties, provided that the entity is not subject to enforcement proceedings under this Regulation regarding the same facts by another competent authority.
14. Competent authorities shall have the power to request from users, data holders, or data recipients, or their legal representatives, falling under the competence of their Member State all information necessary to verify compliance with this Regulation. Any request for information shall be proportionate to the performance of the underlying task and shall be reasoned.

---

[3] Data Act, Article 11 - Technical protection measures on the unauthorised use or disclosure of data, part 2/2  (distance 0.217)
Data Act, Article 11: Technical protection measures on the unauthorised use or disclosure of data
(a) for the purposes of obtaining data, provided false information to a data holder, deployed deceptive or coercive means or abused gaps in the technical infrastructure of the data holder designed to protect the data;
(b) used the data made available for unauthorised purposes, including the development of a competing connected product within the meaning of Article 6(2), point (e);
(c) unlawfully disclosed data to another party;
(d) not maintained the technical and organisational measures agreed pursuant to Article 5(9); or
(e) altered or removed technical protection measures applied by the data holder pursuant to paragraph 1 of this Article without the agreement of the data holder.
4. Paragraph 2 shall also apply where a user alters or removes technical protection measures applied by the data holder or does not maintain the technical and organisational measures taken by the user in agreement with the data holder or, where they are not the same person, the trade secrets holder, in order to preserve trade secrets, as well as in respect of any other party that receives the data from the user by means of an infringement of this Regulation.
5. Where the data recipient infringes Article 6(2), point (a) or (b), users shall have the same rights as data holders under paragraph 2 of this Article.

---

[4] Data Act, Article 4 - The rights and obligations of users and data holders with regard to access, use and making available product data and related service data, part 1/4  (distance 0.230)
Data Act, Article 4: The rights and obligations of users and data holders with regard to access, use and making available product data and related service data
1. Where data cannot be directly accessed by the user from the connected product or related service, data holders shall make readily available data, as well as the relevant metadata necessary to interpret and use those data, accessible to the user without undue delay, of the same quality as is available to the data holder, easily, securely, free of charge, in a comprehensive, structured, commonly used and machine-readable format and, where relevant and technically feasible, continuously and in real-time. This shall be done on the basis of a simple request through electronic means where technically feasible.
2. Users and data holders may contractually restrict or prohibit accessing, using or further sharing data, if such processing could undermine security requirements of the connected product, as laid down by Union or national law, resulting in a serious adverse effect on the health, safety or security of natural persons. Sectoral authorities may provide users and data holders with technical expertise in that context. Where the data holder refuses to share data pursuant to this Article, it shall notify the competent authority designated pursuant to Article 37.
3. Without prejudice to the user’s right to seek redress at any stage before a court or tribunal of a Member State, the user may, in relation to any dispute with the data holder concerning the contractual restrictions or prohibitions referred to in paragraph 2:
(a) lodge, in accordance with Article 37(5), point (b), a complaint with the competent authority; or
(b) agree with the data holder to refer the matter to a dispute settlement body in accordance with Article 10(1).
4. Data holders shall not make the exercise of choices or rights under this Article by the user unduly difficult, including by offering choices to the user in a non-neutral manner or by subverting or impairing the autonomy, decision-making or choices of the user via the structure, design, function or manner of operation of a user digital interface or a part thereof.

---

[5] Data Act, Article 3 - Obligation to make product data and related service data accessible to the user, part 1/2  (distance 0.230)
Data Act, Article 3: Obligation to make product data and related service data accessible to the user
1. Connected products shall be designed and manufactured, and related services shall be designed and provided, in such a manner that product data and related service data, including the relevant metadata necessary to interpret and use those data, are, by default, easily, securely, free of charge, in a comprehensive, structured, commonly used and machine-readable format, and, where relevant and technically feasible, directly accessible to the user.
2. Before concluding a contract for the purchase, rent or lease of a connected product, the seller, rentor or lessor, which may be the manufacturer, shall provide at least the following information to the user, in a clear and comprehensible manner:
(a) the type, format and estimated volume of product data which the connected product is capable of generating;
(b) whether the connected product is capable of generating data continuously and in real-time;
(c) whether the connected product is capable of storing data on-device or on a remote server, including, where applicable, the intended duration of retention;
(d) how the user may access, retrieve or, where relevant, erase the data, including the technical means to do so, as well as their terms of use and quality of service.
3. Before concluding a contract for the provision of a related service, the provider of such related service shall provide at least the following information to the user, in a clear and comprehensible manner:
(a) the nature, estimated volume and collection frequency of product data that the prospective data holder is expected to obtain and, where relevant, the arrangements for the user to access or retrieve such data, including the prospective data holder’s data storage arrangements and the duration of retention;
(b) the nature and estimated volume of related service data to be generated, as well as the arrangements for the user to access or retrieve such data, including the prospective data holder’s data storage arrangements and the duration of retention;

---

[1] Data Act, Article 40 - Penalties  (distance 0.124)
Data Act, Article 40: Penalties
1. Member States shall lay down the rules on penalties applicable to infringements of this Regulation and shall take all measures necessary to ensure that they are implemented. The penalties provided for shall be effective, proportionate and dissuasive.
2. Member States shall by 12 September 2025 notify the Commission of those rules and measures and shall notify it without delay of any subsequent amendment affecting them. The Commission shall regularly update and maintain an easily accessible public register of those measures.
3. Member States shall take into account the recommendations of the EDIB and the following non-exhaustive criteria for the imposition of penalties for infringements of this Regulation:
(a) the nature, gravity, scale and duration of the infringement;
(b) any action taken by the infringing party to mitigate or remedy the damage caused by the infringement;
(c) any previous infringements by the infringing party;
(d) the financial benefits gained or losses avoided by the infringing party due to the infringement, insofar as such benefits or losses can be reliably established;
(e) any other aggravating or mitigating factor applicable to the circumstances of the case;
(f) infringing party’s annual turnover in the preceding financial year in the Union.
4. For infringements of the obligations laid down in Chapter II, III and V of this Regulation, the supervisory authorities responsible for monitoring the application of Regulation (EU) 2016/679 may within their scope of competence impose administrative fines in accordance with Article 83 of Regulation (EU) 2016/679 and up to the amount referred to in Article 83(5) of that Regulation.
5. For infringements of the obligations laid down in Chapter V of this Regulation, the European Data Protection Supervisor may impose within its scope of competence administrative fines in accordance with Article 66 of Regulation (EU) 2018/1725 up to the amount referred to in Article 66(3) of that Regulation.

---

[2] Data Act, Article 37 - Competent authorities and data coordinators, part 4/5  (distance 0.190)
Data Act, Article 37: Competent authorities and data coordinators
12. For the purpose of ensuring compliance with this Regulation, a legal representative shall be mandated by an entity falling within the scope of this Regulation that makes connected products available or offers services in the Union to be addressed in addition to or instead of it by competent authorities with regard to all issues related to that entity. That legal representative shall cooperate with and comprehensively demonstrate to the competent authorities, upon request, the actions taken and provisions put in place by the entity falling within the scope of this Regulation that makes connected products available or offers services in the Union to ensure compliance with this Regulation.
13. An entity falling within the scope of this Regulation that makes connected products available or offers services in the Union, shall be considered to be under the competence of the Member State in which its legal representative is located. The designation of a legal representative by such an entity shall be without prejudice to the liability of, and any legal action that could be initiated against, such an entity. Until such time as an entity designates a legal representative in accordance with this Article, it shall be under the competence of all Member States, where applicable, for the purposes of ensuring the application and enforcement of this Regulation. Any competent authority may exercise its competence, including by imposing effective, proportionate and dissuasive penalties, provided that the entity is not subject to enforcement proceedings under this Regulation regarding the same facts by another competent authority.
14. Competent authorities shall have the power to request from users, data holders, or data recipients, or their legal representatives, falling under the competence of their Member State all information necessary to verify compliance with this Regulation. Any request for information shall be proportionate to the performance of the underlying task and shall be reasoned.

---

[3] Data Governance Act, Article 34 - Penalties  (distance 0.201)
Data Governance Act, Article 34: Penalties
1. Member States shall lay down the rules on penalties applicable to infringements of the obligations regarding transfers of non-personal data to third countries pursuant to Article 5(14) and Article 31, the notification obligation of data intermediation services providers pursuant to Article 11, the conditions for providing data intermediation services pursuant to Article 12 and the conditions for the registration as a recognised data altruism organisation pursuant to Articles 18, 20, 21 and 22, and shall take all measures necessary to ensure that they are implemented. The penalties provided for shall be effective, proportionate and dissuasive. In their rules on penalties, Member States shall take into account the recommendations of the European Data Innovation Board. Member States shall, by 24 September 2023, notify the Commission of those rules and of those measures and shall notify it, without delay, of any subsequent amendment affecting them.
2. Member States shall take into account the following non-exhaustive and indicative criteria for the imposition of penalties on data intermediation services providers and recognised data altruism organisations for infringements of this Regulation, where appropriate:
(a) the nature, gravity, scale and duration of the infringement;
(b) any action taken by the data intermediation services provider or recognised data altruism organisation to mitigate or remedy the damage caused by the infringement;
(c) any previous infringements by the data intermediation services provider or recognised data altruism organisation;
(d) the financial benefits gained or losses avoided by the data intermediation services provider or recognised data altruism organisation due to the infringement, insofar as such benefits or losses can be reliably established;
(e) any other aggravating or mitigating factors applicable to the circumstances of the case.

---

[4] Data Act, Article 11 - Technical protection measures on the unauthorised use or disclosure of data, part 2/2  (distance 0.202)
Data Act, Article 11: Technical protection measures on the unauthorised use or disclosure of data
(a) for the purposes of obtaining data, provided false information to a data holder, deployed deceptive or coercive means or abused gaps in the technical infrastructure of the data holder designed to protect the data;
(b) used the data made available for unauthorised purposes, including the development of a competing connected product within the meaning of Article 6(2), point (e);
(c) unlawfully disclosed data to another party;
(d) not maintained the technical and organisational measures agreed pursuant to Article 5(9); or
(e) altered or removed technical protection measures applied by the data holder pursuant to paragraph 1 of this Article without the agreement of the data holder.
4. Paragraph 2 shall also apply where a user alters or removes technical protection measures applied by the data holder or does not maintain the technical and organisational measures taken by the user in agreement with the data holder or, where they are not the same person, the trade secrets holder, in order to preserve trade secrets, as well as in respect of any other party that receives the data from the user by means of an infringement of this Regulation.
5. Where the data recipient infringes Article 6(2), point (a) or (b), users shall have the same rights as data holders under paragraph 2 of this Article.

---

[5] Data Act, Article 37 - Competent authorities and data coordinators, part 2/5  (distance 0.204)
Data Act, Article 37: Competent authorities and data coordinators
(b) handling complaints arising from alleged infringements of this Regulation, including in relation to trade secrets, and investigating, to the extent appropriate, the subject matter of complaints and regularly informing complainants, where relevant in accordance with national law, of the progress and the outcome of the investigation within a reasonable period, in particular if further investigation or coordination with another competent authority is necessary;
(c) conducting investigations into matters that concern the application of this Regulation, including on the basis of information received from another competent authority or other public authority;
(d) imposing effective, proportionate and dissuasive financial penalties which may include periodic penalties and penalties with retroactive effect, or initiating legal proceedings for the imposition of fines;
(e) monitoring technological and relevant commercial developments of relevance for the making available and use of data;
(f) cooperating with competent authorities of other Member States and, where relevant, with the Commission or the EDIB, to ensure the consistent and efficient application of this Regulation, including the exchange of all relevant information by electronic means, without undue delay, including regarding paragraph 10 of this Article;
(g) cooperating with the relevant competent authorities responsible for the implementation of other Union or national legal acts, including with authorities competent in the field of data and electronic communication services, with the supervisory authority responsible for monitoring the application of Regulation (EU) 2016/679 or with sectoral authorities to ensure that this Regulation is enforced consistently with other Union and national law;
(h) cooperating with the relevant competent authorities to ensure that Articles 23 to 31 and Articles 34 and 35 are enforced consistently with other Union law and self-regulation applicable to providers of data processing services;
(i) ensuring that switching charges are withdrawn in accordance with Article 29;
(j) examining the requests for data made pursuant to Chapter V.
Where designated, the data coordinator shall facilitate the cooperation referred to in points (f), (g) and (h) of the first subparagraph and shall assist the competent authorities upon their request.
6. The data coordinator, where such competent authority has been designated, shall:
```
</details>


---

## q26 (multi)

**Question:** What must a data altruism organisation provide regarding consent, and how easy must withdrawal be under the GDPR?

**Reference answer:** DGA Art. 21: it must provide tools for obtaining consent or permissions and tools for easy withdrawal. GDPR Art. 7(3): withdrawal must be as easy as giving consent and can be done at any time.

**Agent answer:**

The indexed documents do not cover this. What a data altruism organisation must provide regarding consent and withdrawal is governed by the Data Governance Act (Articles 21 and 25), not the GDPR.

<details><summary>Retrieved passages</summary>

```
[1] Data Governance Act, Article 21 - Specific requirements to safeguard rights and interests of data subjects and data holders with regard to their data  (distance 0.238)
Data Governance Act, Article 21: Specific requirements to safeguard rights and interests of data subjects and data holders with regard to their data
1. A recognised data altruism organisation shall inform data subjects or data holders prior to any processing of their data in a clear and easily comprehensible manner of:
(a) the objectives of general interest and, if applicable, the specified, explicit and legitimate purpose for which personal data is to be processed, and for which it permits the processing of their data by a data user;
(b) the location of and the objectives of general interest for which it permits any processing carried out in a third country, where the processing is carried out by the recognised data altruism organisation.
2. The recognised data altruism organisation shall not use the data for other objectives than those of general interest for which the data subject or data holder allows the processing. The recognised data altruism organisation shall not use misleading marketing practices to solicit the provision of data.
3. The recognised data altruism organisation shall provide tools for obtaining consent from data subjects or permissions to process data made available by data holders. The recognised data altruism organisation shall also provide tools for easy withdrawal of such consent or permission.
4. The recognised data altruism organisation shall take measures to ensure an appropriate level of security for the storage and processing of non-personal data that it has collected based on data altruism.
5. The recognised data altruism organisation shall, without delay, inform data holders in the event of any unauthorised transfer, access or use of the non-personal data that it has shared.
6. Where the recognised data altruism organisation facilitates data processing by third parties, including by providing tools for obtaining consent from data subjects or permissions to process data made available by data holders, it shall, where relevant, specify the third-country jurisdiction in which the data use is intended to take place.

---

[2] Data Governance Act, Article 25 - European data altruism consent form  (distance 0.247)
Data Governance Act, Article 25: European data altruism consent form
1. In order to facilitate the collection of data based on data altruism, the Commission shall adopt implementing acts establishing and developing a European data altruism consent form, after consulting the European Data Protection Board, taking into account the advice of the European Data Innovation Board and duly involving relevant stakeholders. The form shall allow the collection of consent or permission across Member States in a uniform format. Those implementing acts shall be adopted in accordance with the advisory procedure referred to in Article 33(2).
2. The European data altruism consent form shall use a modular approach allowing customisation for specific sectors and for different purposes.
3. Where personal data are provided, the European data altruism consent form shall ensure that data subjects are able to give consent to and withdraw consent from a specific data processing operation in compliance with the requirements of Regulation (EU) 2016/679.
4. The form shall be available in a manner that can be printed on paper and is easily understandable as well as in an electronic, machine-readable form.

---

[3] Data Governance Act, Article 18 - General requirements for registration  (distance 0.265)
Data Governance Act, Article 18: General requirements for registration
In order to qualify for registration in a public national register of recognised data altruism organisations, an entity shall:
(a) carry out data altruism activities;
(b) be a legal person established pursuant to national law to meet objectives of general interest as provided for in national law, where applicable;
(c) operate on a not-for-profit basis and be legally independent from any entity that operates on a for-profit basis;
(d) carry out its data altruism activities through a structure that is functionally separate from its other activities;
(e) comply with the rulebook referred to Article 22(1), at the latest 18 months after the date of entry into force of the delegated acts referred to in that paragraph.

---

[4] Data Governance Act, Article 16 - National arrangements for data altruism  (distance 0.272)
Data Governance Act, Article 16: National arrangements for data altruism
Member States may have in place organisational or technical arrangements, or both, to facilitate data altruism. To that end, Member States may establish national policies for data altruism. Those national policies may, in particular, assist data subjects in making personal data related to them held by public sector bodies available voluntarily for data altruism, and set out the necessary information that is required to be provided to data subjects concerning the re-use of their data in the general interest.
If a Member State develops such national policies, it shall notify the Commission thereof.

---

[5] Data Governance Act, Article 24 - Monitoring of compliance, part 1/2  (distance 0.273)
Data Governance Act, Article 24: Monitoring of compliance
1. The competent authorities for the registration of data altruism organisations shall monitor and supervise compliance of recognised data altruism organisations with the requirements laid down in this Chapter. The competent authority for the registration of data altruism organisations may also monitor and supervise the compliance of such recognised data altruism organisations, on the basis of a request by a natural or legal person.
2. The competent authorities for the registration of data altruism organisations shall have the power to request information from recognised data altruism organisations that is necessary to verify compliance with the requirements of this Chapter. Any request for information shall be proportionate to the performance of the task and shall be reasoned.
3. Where the competent authority for the registration of data altruism organisations finds that a recognised data altruism organisation does not comply with one or more of the requirements of this Chapter, it shall notify the recognised data altruism organisation of those findings and give it the opportunity to state its views within 30 days of the receipt of the notification.
4. The competent authority for the registration of data altruism organisations shall have the power to require the cessation of the infringement referred to in paragraph 3 either immediately or within a reasonable time limit and shall take appropriate and proportionate measures with the aim of ensuring compliance.
5. If a recognised data altruism organisation does not comply with one or more of the requirements of this Chapter even after having been notified in accordance with paragraph 3 by the competent authority for the registration of data altruism organisations, that recognised data altruism organisation shall:
(a) lose its right to use the label ‘data altruism organisation recognised in the Union’ in any written and spoken communication;
(b) be removed from the relevant public national register of recognised data altruism organisations and the public Union register of recognised data altruism organisations.
```
</details>


---

## q27 (multi)

**Question:** What must a cloud provider's contract say about switching, and when do switching charges disappear?

**Reference answer:** Art. 25: a written contract with clauses allowing the customer to switch provider or port data without undue delay within the maximum notice and transition periods, with assistance and security during switching. Art. 29: reduced charges (not above direct costs) until 12 January 2027, none afterwards.

**Agent answer:**

A data processing service provider's written contract must clearly set out the rights of the customer and the obligations of the provider regarding switching, and must include at least the following:

* Clauses allowing the customer, upon request, to switch to another provider or port all exportable data and digital assets to an on-premises ICT infrastructure without undue delay and within a mandatory maximum transitional period of 30 calendar days (initiated after the maximum notice period), during which the service contract remains applicable and the provider must provide reasonable assistance, maintain business continuity, provide clear information on continuity risks, and ensure a high level of security (Data Act, Article 25).
* An obligation for the provider to support the customer's exit strategy, including by providing all relevant information (Data Act, Article 25).
* Clauses specifying that the contract is considered terminated either upon the successful completion of the switching process or at the end of the maximum notice period if the customer chooses to erase their data instead (Data Act, Article 25).
* A maximum notice period for initiating switching that does not exceed two months (Data Act, Article 25).
* An exhaustive specification of all categories of data and digital assets that can be ported, including at a minimum all exportable data (Data Act, Article 25).
* An exhaustive specification of categories of internal functioning data exempted from exportable data due to trade secret risks, provided they do not delay or impede switching (Data Act, Article 25).
* A minimum data retrieval period of at least 30 calendar days starting after the agreed transitional period (Data Act, Article 25).
* A clause guaranteeing the full erasure of all exportable data and digital assets generated directly by or relating to the customer after the retrieval period (or an agreed later date) once switching is successfully completed (Data Act, Article 25).
* Switching charges, where applicable in accordance with Article 29 (Data Act, Article 25).
* Clauses allowing the customer to notify the provider upon termination of the maximum notice period of their decision to switch provider, switch to an on-premises infrastructure, or erase their data (Data Act, Article 25).

Regarding switching charges:
* From 12 January 2027, providers shall not impose any switching charges on the customer for the switching process (Data Act, Article 29).
* From 11 January 2024 to 12 January 2027, providers may impose reduced switching charges that do not exceed the costs incurred by the provider that are directly linked to the switching process (Data Act, Article 29).

<details><summary>Retrieved passages</summary>

```
[1] Data Act, Article 25 - Contractual terms concerning switching, part 2/5  (distance 0.263)
Data Act, Article 25: Contractual terms concerning switching
(a) clauses allowing the customer, upon request, to switch to a data processing service offered by a different provider of data processing services or to port all exportable data and digital assets to an on-premises ICT infrastructure, without undue delay and in any event not after the mandatory maximum transitional period of 30 calendar days, to be initiated after the maximum notice period referred to in point (d), during which the service contract remains applicable and during which the provider of data processing services shall: (i) provide reasonable assistance to the customer and third parties authorised by the customer in the switching process; (ii) act with due care to maintain business continuity, and continue the provision of the functions or services under the contract; (iii) provide clear information concerning known risks to continuity in the provision of the functions or services on the part of the source provider of data processing services; (iv) ensure that a high level of security is maintained throughout the switching process, in particular the security of the data during their transfer and the continued security of the data during the retrieval period specified in point (g), in accordance with applicable Union or national law; (i) provide reasonable assistance to the customer and third parties authorised by the customer in the switching process; (ii) act with due care to maintain business continuity, and continue the provision of the functions or services under the contract; (iii) provide clear information concerning known risks to continuity in the provision of the functions or services on the part of the source provider of data processing services; (iv) ensure that a high level of security is maintained throughout the switching process, in particular the security of the data during their transfer and the continued security of the data during the retrieval period specified in point (g), in accordance with applicable Union or national law;
(i) provide reasonable assistance to the customer and third parties authorised by the customer in the switching process;

---

[2] Data Act, Article 25 - Contractual terms concerning switching, part 4/5  (distance 0.265)
Data Act, Article 25: Contractual terms concerning switching
(f) an exhaustive specification of categories of data specific to the internal functioning of the provider’s data processing service that are to be exempted from the exportable data under point (e) of this paragraph where a risk of breach of trade secrets of the provider exists, provided that such exemptions do not impede or delay the switching process provided for in Article 23;
(g) a minimum period for data retrieval of at least 30 calendar days, starting after the termination of the transitional period that was agreed between the customer and the provider of data processing services, in accordance with point (a) of this paragraph and paragraph 4;
(h) a clause guaranteeing full erasure of all exportable data and digital assets generated directly by the customer, or relating to the customer directly, after the expiry of the retrieval period referred to in point (g) or after the expiry of an alternative agreed period at a date later than the date of expiry of the retrieval period referred to in point (g), provided that the switching process has been completed successfully;
(i) switching charges, that may be imposed by providers of data processing services in accordance with Article 29.
3. The contract referred to in paragraph 1 shall include clauses providing that the customer may notify the provider of data processing services of its decision to perform one or more of the following actions upon termination of the maximum notice period referred to in paragraph 2, point (d):
(a) switch to a different provider of data processing services, in which case the customer shall provide the necessary details of that provider;
(b) switch to an on-premises ICT infrastructure;
(c) erase its exportable data and digital assets.

---

[3] Data Act, Article 29 - Gradual withdrawal of switching charges  (distance 0.271)
Data Act, Article 29: Gradual withdrawal of switching charges
1. From 12 January 2027, providers of data processing services shall not impose any switching charges on the customer for the switching process.
2. From 11 January 2024 to 12 January 2027, providers of data processing services may impose reduced switching charges on the customer for the switching process.
3. The reduced switching charges referred to in paragraph 2 shall not exceed the costs incurred by the provider of data processing services that are directly linked to the switching process concerned.
4. Before entering into a contract with a customer, providers of data processing services shall provide the prospective customer with clear information on the standard service fees and early termination penalties that might be imposed, as well as on the reduced switching charges that might be imposed during the timeframe referred to in paragraph 2.
5. Where relevant, providers of data processing services shall provide information to a customer on data processing services that involve highly complex or costly switching or for which it is impossible to switch without significant interference in the data, digital assets or service architecture.
6. Where applicable, providers of data processing services shall make the information referred to in paragraphs 4 and 5 publicly available to customers via a dedicated section of their website or in any other easily accessible way.
7. The Commission is empowered to adopt delegated acts in accordance with Article 45 to supplement this Regulation by establishing a monitoring mechanism for the Commission to monitor switching charges, imposed by providers of data processing services on the market to ensure that the withdrawal and reduction of switching charges, pursuant to paragraphs 1 and 2 of this Article are to be attained in accordance with the deadlines laid down in those paragraphs.

---

[4] Data Act, Article 23 - Removing obstacles to effective switching  (distance 0.274)
Data Act, Article 23: Removing obstacles to effective switching
Providers of data processing services shall take the measures provided for in Articles 25, 26, 27, 29 and 30 to enable customers to switch to a data processing service, covering the same service type, which is provided by a different provider of data processing services, or to on-premises ICT infrastructure, or, where relevant, to use several providers of data processing services at the same time. In particular, providers of data processing services shall not impose and shall remove pre-commercial, commercial, technical, contractual and organisational obstacles, which inhibit customers from:
(a) terminating, after the maximum notice period and the successful completion of the switching process, in accordance with Article 25, the contract of the data processing service;
(b) concluding new contracts with a different provider of data processing services covering the same service type;
(c) porting the customer’s exportable data and digital assets, to a different provider of data processing services or to an on-premises ICT infrastructure, including after having benefited from a free-tier offering;
(d) in accordance with Article 24, achieving functional equivalence in the use of the new data processing service in the ICT environment of a different provider of data processing services covering the same service type;
(e) unbundling, where technically feasible, data processing services referred to in Article 30(1) from other data processing services provided by the provider of data processing services.

---

[5] Data Act, Article 25 - Contractual terms concerning switching, part 3/5  (distance 0.279)
Data Act, Article 25: Contractual terms concerning switching
(ii) act with due care to maintain business continuity, and continue the provision of the functions or services under the contract;
(iii) provide clear information concerning known risks to continuity in the provision of the functions or services on the part of the source provider of data processing services;
(iv) ensure that a high level of security is maintained throughout the switching process, in particular the security of the data during their transfer and the continued security of the data during the retrieval period specified in point (g), in accordance with applicable Union or national law;
(b) an obligation of the provider of data processing services to support the customer’s exit strategy relevant to the contracted services, including by providing all relevant information;
(c) a clause specifying that the contract shall be considered to be terminated and the customer shall be notified of the termination, in one of the following cases: (i) where applicable, upon the successful completion of the switching process; (ii) at the end of the maximum notice period referred to in paragraph (d), where the customer does not wish to switch but to erase its exportable data and digital assets upon service termination; (i) where applicable, upon the successful completion of the switching process; (ii) at the end of the maximum notice period referred to in paragraph (d), where the customer does not wish to switch but to erase its exportable data and digital assets upon service termination;
(i) where applicable, upon the successful completion of the switching process;
(ii) at the end of the maximum notice period referred to in paragraph (d), where the customer does not wish to switch but to erase its exportable data and digital assets upon service termination;
(d) a maximum notice period for initiation of the switching process, which shall not exceed two months;
(e) an exhaustive specification of all categories of data and digital assets that can be ported during the switching process, including, at a minimum, all exportable data;

---

[1] Data Act, Article 25 - Contractual terms concerning switching, part 1/5  (distance 0.100)
Data Act, Article 25: Contractual terms concerning switching
1. The rights of the customer and the obligations of the provider of data processing services in relation to switching between providers of such services or, where applicable, to an on-premises ICT infrastructure shall be clearly set out in a written contract. The provider of data processing services shall make that contract available to the customer prior to signing the contract in a way that allows the customer to store and reproduce the contract.
2. Without prejudice to Directive (EU) 2019/770, the contract referred to in paragraph 1 of this Article shall include at least the following:

---

[2] Data Act, Article 25 - Contractual terms concerning switching, part 4/5  (distance 0.125)
Data Act, Article 25: Contractual terms concerning switching
(f) an exhaustive specification of categories of data specific to the internal functioning of the provider’s data processing service that are to be exempted from the exportable data under point (e) of this paragraph where a risk of breach of trade secrets of the provider exists, provided that such exemptions do not impede or delay the switching process provided for in Article 23;
(g) a minimum period for data retrieval of at least 30 calendar days, starting after the termination of the transitional period that was agreed between the customer and the provider of data processing services, in accordance with point (a) of this paragraph and paragraph 4;
(h) a clause guaranteeing full erasure of all exportable data and digital assets generated directly by the customer, or relating to the customer directly, after the expiry of the retrieval period referred to in point (g) or after the expiry of an alternative agreed period at a date later than the date of expiry of the retrieval period referred to in point (g), provided that the switching process has been completed successfully;
(i) switching charges, that may be imposed by providers of data processing services in accordance with Article 29.
3. The contract referred to in paragraph 1 shall include clauses providing that the customer may notify the provider of data processing services of its decision to perform one or more of the following actions upon termination of the maximum notice period referred to in paragraph 2, point (d):
(a) switch to a different provider of data processing services, in which case the customer shall provide the necessary details of that provider;
(b) switch to an on-premises ICT infrastructure;
(c) erase its exportable data and digital assets.

---

[3] Data Act, Article 25 - Contractual terms concerning switching, part 2/5  (distance 0.125)
Data Act, Article 25: Contractual terms concerning switching
(a) clauses allowing the customer, upon request, to switch to a data processing service offered by a different provider of data processing services or to port all exportable data and digital assets to an on-premises ICT infrastructure, without undue delay and in any event not after the mandatory maximum transitional period of 30 calendar days, to be initiated after the maximum notice period referred to in point (d), during which the service contract remains applicable and during which the provider of data processing services shall: (i) provide reasonable assistance to the customer and third parties authorised by the customer in the switching process; (ii) act with due care to maintain business continuity, and continue the provision of the functions or services under the contract; (iii) provide clear information concerning known risks to continuity in the provision of the functions or services on the part of the source provider of data processing services; (iv) ensure that a high level of security is maintained throughout the switching process, in particular the security of the data during their transfer and the continued security of the data during the retrieval period specified in point (g), in accordance with applicable Union or national law; (i) provide reasonable assistance to the customer and third parties authorised by the customer in the switching process; (ii) act with due care to maintain business continuity, and continue the provision of the functions or services under the contract; (iii) provide clear information concerning known risks to continuity in the provision of the functions or services on the part of the source provider of data processing services; (iv) ensure that a high level of security is maintained throughout the switching process, in particular the security of the data during their transfer and the continued security of the data during the retrieval period specified in point (g), in accordance with applicable Union or national law;
(i) provide reasonable assistance to the customer and third parties authorised by the customer in the switching process;

---

[4] Data Act, Article 25 - Contractual terms concerning switching, part 3/5  (distance 0.135)
Data Act, Article 25: Contractual terms concerning switching
(ii) act with due care to maintain business continuity, and continue the provision of the functions or services under the contract;
(iii) provide clear information concerning known risks to continuity in the provision of the functions or services on the part of the source provider of data processing services;
(iv) ensure that a high level of security is maintained throughout the switching process, in particular the security of the data during their transfer and the continued security of the data during the retrieval period specified in point (g), in accordance with applicable Union or national law;
(b) an obligation of the provider of data processing services to support the customer’s exit strategy relevant to the contracted services, including by providing all relevant information;
(c) a clause specifying that the contract shall be considered to be terminated and the customer shall be notified of the termination, in one of the following cases: (i) where applicable, upon the successful completion of the switching process; (ii) at the end of the maximum notice period referred to in paragraph (d), where the customer does not wish to switch but to erase its exportable data and digital assets upon service termination; (i) where applicable, upon the successful completion of the switching process; (ii) at the end of the maximum notice period referred to in paragraph (d), where the customer does not wish to switch but to erase its exportable data and digital assets upon service termination;
(i) where applicable, upon the successful completion of the switching process;
(ii) at the end of the maximum notice period referred to in paragraph (d), where the customer does not wish to switch but to erase its exportable data and digital assets upon service termination;
(d) a maximum notice period for initiation of the switching process, which shall not exceed two months;
(e) an exhaustive specification of all categories of data and digital assets that can be ported during the switching process, including, at a minimum, all exportable data;

---

[5] Data Act, Article 23 - Removing obstacles to effective switching  (distance 0.142)
Data Act, Article 23: Removing obstacles to effective switching
Providers of data processing services shall take the measures provided for in Articles 25, 26, 27, 29 and 30 to enable customers to switch to a data processing service, covering the same service type, which is provided by a different provider of data processing services, or to on-premises ICT infrastructure, or, where relevant, to use several providers of data processing services at the same time. In particular, providers of data processing services shall not impose and shall remove pre-commercial, commercial, technical, contractual and organisational obstacles, which inhibit customers from:
(a) terminating, after the maximum notice period and the successful completion of the switching process, in accordance with Article 25, the contract of the data processing service;
(b) concluding new contracts with a different provider of data processing services covering the same service type;
(c) porting the customer’s exportable data and digital assets, to a different provider of data processing services or to an on-premises ICT infrastructure, including after having benefited from a free-tier offering;
(d) in accordance with Article 24, achieving functional equivalence in the use of the new data processing service in the ICT environment of a different provider of data processing services covering the same service type;
(e) unbundling, where technically feasible, data processing services referred to in Article 30(1) from other data processing services provided by the provider of data processing services.
```
</details>


---

## q28 (multi)

**Question:** In a public emergency, how fast can a data holder push back on a public body's data request and does it get paid?

**Reference answer:** It may decline or seek modification no later than five working days after receipt (Art. 18). For emergency requests, data holders other than micro and small enterprises must provide the data free of charge (Art. 20(1)).

**Agent answer:**

A data holder can decline or seek the modification of a request to respond to a public emergency without undue delay and, in any event, no later than five working days after the receipt of the request, based on specific grounds such as not having control over the data, a similar request having been previously submitted, or the request failing to meet certain legal conditions (Data Act, Article 18).

Regarding payment, data holders other than microenterprises and small enterprises must make data available to respond to a public emergency free of charge (Data Act, Article 20). 

(Data Act, Article 15; Data Act, Article 18; Data Act, Article 20)

<details><summary>Retrieved passages</summary>

```
[1] Data Act, Article 20 - Compensation in cases of an exceptional need  (distance 0.148)
Data Act, Article 20: Compensation in cases of an exceptional need
1. Data holders other than microenterprises and small enterprises shall make available data necessary to respond to a public emergency pursuant to Article 15(1), point (a), free of charge. The public sector body, the Commission, the European Central Bank or the Union body that has received data shall provide public acknowledgement to the data holder if requested by the data holder.
2. The data holder shall be entitled to fair compensation for making data available in compliance with a request made pursuant to Article 15(1), point (b). Such compensation shall cover the technical and organisational costs incurred to comply with the request including, where applicable, the costs of anonymisation, pseudonymisation, aggregation and of technical adaptation, and a reasonable margin. Upon request of the public sector body, the Commission, the European Central Bank or the Union body, the data holder shall provide information on the basis for the calculation of the costs and the reasonable margin.
3. Paragraph 2 shall also apply where a microenterprise and small enterprise claims compensation for making data available.
4. Data holders shall not be entitled to compensation for making data available in compliance with a request made pursuant to Article 15(1), point (b), where the specific task carried out in the public interest is the production of official statistics and where the purchase of data is not allowed by national law. Member States shall notify the Commission where the purchase of data for the production of official statistics is not allowed by national law.
5. Where the public sector body, the Commission, the European Central Bank or the Union body disagrees with the level of compensation requested by the data holder, they may lodge a complaint with the competent authority designated pursuant to Article 37 of the Member State where the data holder is established.

---

[2] Data Act, Article 15 - Exceptional need to use data, part 1/3  (distance 0.164)
Data Act, Article 15: Exceptional need to use data
1. An exceptional need to use certain data within the meaning of this Chapter shall be limited in time and scope and shall be considered to exist only in any of the following circumstances:
(a) where the data requested is necessary to respond to a public emergency and the public sector body, the Commission, the European Central Bank or the Union body is unable to obtain such data by alternative means in a timely and effective manner under equivalent conditions;

---

[3] Data Act, Article 18 - Compliance with requests for data, part 1/2  (distance 0.178)
Data Act, Article 18: Compliance with requests for data
1. A data holder receiving a request to make data available under this Chapter shall make the data available to the requesting public sector body, the Commission, the European Central Bank or a Union body without undue delay, taking into account necessary technical, organisational and legal measures.
2. Without prejudice to specific needs regarding the availability of data defined in Union or national law, a data holder may decline or seek the modification of a request to make data available under this Chapter without undue delay and, in any event, no later than five working days after the receipt of a request for the data necessary to respond to a public emergency and without undue delay and, in any event, no later than 30 working days after the receipt of such a request in other cases of an exceptional need, on any of the following grounds:
(a) the data holder does not have control over the data requested;
(b) a similar request for the same purpose has been previously submitted by another public sector body or the Commission, the European Central Bank or a Union body and the data holder has not been notified of the erasure of the data pursuant to Article 19(1), point (c);
(c) the request does not meet the conditions laid down in Article 17(1) and (2).
3. If the data holder decides to decline the request or to seek its modification in accordance with paragraph 2, point (b), it shall indicate the identity of the public sector body or the Commission, the European Central Bank or the Union body that previously submitted a request for the same purpose.
4. Where the data requested includes personal data, the data holder shall properly anonymise the data, unless the compliance with the request to make data available to a public sector body, the Commission, the European Central Bank or a Union body requires the disclosure of personal data. In such cases, the data holder shall pseudonymise the data.

---

[4] Data Act, Article 15 - Exceptional need to use data, part 3/3  (distance 0.188)
Data Act, Article 15: Exceptional need to use data
(i) a public sector body, the Commission, the European Central Bank or a Union body is acting on the basis of Union or national law and has identified specific data, the lack of which prevents it from fulfilling a specific task carried out in the public interest, that has been explicitly provided for by law, such as the production of official statistics or the mitigation of or recovery from a public emergency; and
(ii) the public sector body, the Commission, the European Central Bank or the Union body has exhausted all other means at its disposal to obtain such data, including purchase of non-personal data on the market by offering market rates, or by relying on existing obligations to make data available or the adoption of new legislative measures which could guarantee the timely availability of the data.
2. Paragraph 1, point (b), shall not apply to microenterprises and small enterprises.
3. The obligation to demonstrate that the public sector body was unable to obtain non-personal data by purchasing them on the market shall not apply where the specific task carried out in the public interest is the production of official statistics and where the purchase of such data is not allowed by national law.

---

[5] Data Act, Article 14 - Obligation to make data available on the basis of an exceptional need  (distance 0.189)
Data Act, Article 14: Obligation to make data available on the basis of an exceptional need
Where a public sector body, the Commission, the European Central Bank or a Union body demonstrates an exceptional need, as set out in Article 15, to use certain data, including the relevant metadata necessary to interpret and use those data, to carry out its statutory duties in the public interest, data holders that are legal persons, other than public sectors bodies, which hold those data shall make them available upon a duly reasoned request.
```
</details>


---

## q29 (multi)

**Question:** What must a company do before running a data-sharing marketplace, and which conditions apply once it is running?

**Reference answer:** Notify the competent authority for data intermediation services before starting (Art. 11). Conditions (Art. 12) include not using the data for other purposes, providing the service through a separate legal person, and commercial terms not tied to the provider's other services.

**Agent answer:**

Before running a data-sharing marketplace (operating as a data intermediation services provider), a company must:

* Submit a notification to the competent authority for data intermediation services regarding its intention to provide such services (Data Governance Act, Article 11).
* If the provider has establishments in more than one Member State, it is deemed to be under the jurisdiction of the Member State of its main establishment (Data Governance Act, Article 11).
* If the provider is not established in the Union but offers data intermediation services within the Union, it must designate a legal representative in one of the Member States in which those services are offered (Data Governance Act, Article 11).
* Include specific information in the notification, such as its name, legal status and ownership structure, address of its main establishment, public website, contact details, a description of the intended service, and the estimated start date (Data Governance Act, Article 11).

Once running, the provider is subject to the following conditions:

* It must not use the data for which it provides intermediation services for other purposes, and it must provide the intermediation services through a separate legal person (Data Governance Act, Article 12).
* Commercial terms, including pricing, must not depend on whether the data holder or data user uses other services from the provider or a related entity (Data Governance Act, Article 12).
* Data collected regarding any person's activity for the purpose of providing the service (such as date, time, geolocation, duration, and connections) may only be used to develop the data intermediation service (including fraud detection or cybersecurity) and must be made available to data holders upon request (Data Governance Act, Article 12).
* It must facilitate data exchange in the format received, converting it only to enhance interoperability, if requested by the user, or as mandated by law, while offering an opt-out to data subjects or holders (Data Governance Act, Article 12).
* Additional specific tools (such as temporary storage, curation, conversion, anonymisation, and pseudonymisation) may only be offered at the explicit request or approval of the data holder or data subject, and third-party tools cannot be used for other purposes (Data Governance Act, Article 12).
* Access procedures must be fair, transparent, and non-discriminatory for data subjects, holders, and users (Data Governance Act, Article 12).
* It must have procedures to prevent fraudulent or abusive practices by parties seeking access (Data Governance Act, Article 12).
* In the event of insolvency, it must ensure reasonable continuity of services and have mechanisms in place for data holders and users to access, transfer, or retrieve their data, or for data subjects to exercise their rights (Data Governance Act, Article 12).
* It must take appropriate measures to ensure interoperability with other data intermediation services using commonly used open standards (Data Governance Act, Article 12).
* It must put in place adequate technical, legal, and organisational measures to prevent unlawful transfer or access to non-personal data under Union or national law (Data Governance Act, Article 12).
* It must inform data holders without delay in the event of unauthorized transfer, access, or use of shared non-personal data (Data Governance Act, Article 12).
* It must take necessary measures to ensure an appropriate level of security for non-personal data storage, processing, and transmission, and the highest level of security for competitively sensitive information (Data Governance Act, Article 12).
* When offering services to data subjects, it must act in their best interest, informing and advising them transparently about intended data uses and standard terms before they give consent (Data Governance Act, Article 12).
* Where it provides tools for obtaining consent or permissions, it must specify the third-country jurisdiction of intended data use and provide tools to both give and withdraw consent or permissions (Data Governance Act, Article 12).
* It must maintain a log record of the data intermediation activity (Data Governance Act, Article 12).
* It must notify the competent authority of any changes to the notification information within 14 days, and notify within 15 days if it ceases its activities (Data Governance Act, Article 11).
* It must clearly display the common logo for recognised data intermediation services providers on every online and offline publication relating to its activities (Data Governance Act, Article 11).

<details><summary>Retrieved passages</summary>

```
[1] Data Governance Act, Article 11 - Notification by data intermediation services providers, part 3/3  (distance 0.256)
Data Governance Act, Article 11: Notification by data intermediation services providers
In order to ensure that data intermediation services providers recognised in the Union are easily identifiable throughout the Union, the Commission shall, by means of implementing acts, establish a design for the common logo. Data intermediation services providers recognised in the Union shall display the common logo clearly on every online and offline publication that relates to their data intermediation activities.
Those implementing acts shall be adopted in accordance with the advisory procedure referred to in Article 33(2).
10. The competent authority for data intermediation services shall notify the Commission of each new notification by electronic means without delay. The Commission shall keep and regularly update a public register of all data intermediation services providers providing their services in the Union. The information referred to in paragraph 6, points (a), (b), (c), (d), (f) and (g), shall be published in the public register.
11. The competent authority for data intermediation services may charge fees for the notification in accordance with national law. Such fees shall be proportionate and objective and be based on the administrative costs related to the monitoring of compliance and other market control activities of the competent authority for data intermediation services in relation to notifications of data intermediation services providers. In the case of SMEs and start-ups, the competent authority for data intermediation services may charge a discounted fee or waive the fee.
12. Data intermediation services providers shall notify the competent authority for data intermediation services of any changes to the information provided pursuant to paragraph 6 within 14 days of the date of the change.
13. Where a data intermediation services provider ceases its activities, it shall notify the relevant competent authority for data intermediation services determined pursuant to paragraphs 1, 2 and 3 within 15 days.
14. The competent authority for data intermediation services shall notify the Commission of each notification referred to in paragraphs 12 and 13 by electronic means without delay. The Commission shall update the public register of the data intermediation services providers in the Union accordingly.

---

[2] Data Governance Act, Article 11 - Notification by data intermediation services providers, part 2/3  (distance 0.263)
Data Governance Act, Article 11: Notification by data intermediation services providers
(a) the name of the data intermediation services provider;
(b) the data intermediation services provider’s legal status, form, ownership structure, relevant subsidiaries and, where the data intermediation services provider is registered in a trade or other similar public national register, registration number;
(c) the address of the data intermediation services provider’s main establishment in the Union, if any, and, where applicable, of any secondary branch in another Member State or that of the legal representative;
(d) a public website where complete and up-to-date information on the data intermediation services provider and the activities can be found, including as a minimum the information referred to in points (a), (b), (c) and (f);
(e) the data intermediation services provider’s contact persons and contact details;
(f) a description of the data intermediation service the data intermediation services provider intends to provide, and an indication of the categories listed in Article 10 under which such data intermediation service falls;
(g) the estimated date for starting the activity, if different from the date of the notification.
7. The competent authority for data intermediation services shall ensure that the notification procedure is non-discriminatory and does not distort the competition.
8. At the request of the data intermediation services provider, the competent authority for data intermediation services shall, within one week of a duly and fully completed notification, issue a standardised declaration, confirming that the data intermediation services provider has submitted the notification referred to in paragraph 1 and that the notification contains the information referred to in paragraph 6.
9. At the request of the data intermediation services provider, the competent authority for data intermediation services shall confirm that the data intermediation services provider complies with this Article and Article 12. Upon receipt of such a confirmation, that data intermediation services provider may use the label ‘data intermediation services provider recognised in the Union’ in its written and spoken communication, as well as a common logo.

---

[3] Data Governance Act, Article 11 - Notification by data intermediation services providers, part 1/3  (distance 0.267)
Data Governance Act, Article 11: Notification by data intermediation services providers
1. Any data intermediation services provider who intends to provide the data intermediation services referred to in Article 10 shall submit a notification to the competent authority for data intermediation services.
2. For the purposes of this Regulation, a data intermediation services provider with establishments in more than one Member State shall be deemed to be under the jurisdiction of the Member State in which it has its main establishment, without prejudice to Union law regulating cross-border actions for damages and related proceedings.
3. A data intermediation services provider that is not established in the Union, but which offers the data intermediation services referred to in Article 10 within the Union, shall designate a legal representative in one of the Member States in which those services are offered.
For the purpose of ensuring compliance with this Regulation, the legal representative shall be mandated by the data intermediation services provider to be addressed in addition to or instead of it by competent authorities for data intermediation services or data subjects and data holders, with regard to all issues related to the data intermediation services provided. The legal representative shall cooperate with and comprehensively demonstrate to the competent authorities for data intermediation services, upon request, the actions taken and provisions put in place by the data intermediation services provider to ensure compliance with this Regulation.
The data intermediation services provider shall be deemed to be under the jurisdiction of the Member State in which the legal representative is located. The designation of a legal representative by the data intermediation services provider shall be without prejudice to any legal actions which could be initiated against the data intermediation services provider.
4. After having submitted a notification in accordance with paragraph 1, the data intermediation services provider may start the activity subject to the conditions laid down in this Chapter.
5. The notification referred to in paragraph 1 shall entitle the data intermediation services provider to provide data intermediation services in all Member States.
6. The notification referred to in paragraph 1 shall include the following information:

---

[4] Data Act, Article 21 - Sharing of data obtained in the context of an exceptional need with research organisations or statistical bodies, part 2/2  (distance 0.278)
Data Act, Article 21: Sharing of data obtained in the context of an exceptional need with research organisations or statistical bodies
5. Where a public sector body, the Commission, the European Central Bank or a Union body intends to transmit or make data available under paragraph 1 of this Article, it shall notify without undue delay the data holder from whom the data was received, stating the identity and contact details of the organisation or the individual receiving the data, the purpose of the transmission or making available of the data, the period for which the data is to be used and the technical protection and organisational measures taken, including where personal data or trade secrets are involved. Where the data holder disagrees with the transmission or making available of data, it may lodge a complaint with the competent authority designated pursuant to Article 37 of the Member State where the data holder is established.

---

[5] Data Governance Act, Article 10 - Data intermediation services  (distance 0.290)
Data Governance Act, Article 10: Data intermediation services
The provision of the following data intermediation services shall comply with Article 12 and shall be subject to a notification procedure:
(a) intermediation services between data holders and potential data users, including making available the technical or other means to enable such services; those services may include bilateral or multilateral exchanges of data or the creation of platforms or databases enabling the exchange or joint use of data, as well as the establishment of other specific infrastructure for the interconnection of data holders with data users;
(b) intermediation services between data subjects that seek to make their personal data available or natural persons that seek to make non-personal data available, and potential data users, including making available the technical or other means to enable such services, and in particular enabling the exercise of the data subjects’ rights provided in Regulation (EU) 2016/679;
(c) services of data cooperatives.

---

[1] Data Governance Act, Article 12 - Conditions for providing data intermediation services, part 1/3  (distance 0.147)
Data Governance Act, Article 12: Conditions for providing data intermediation services
The provision of data intermediation services referred in Article 10 shall be subject to the following conditions:
(a) the data intermediation services provider shall not use the data for which it provides data intermediation services for purposes other than to put them at the disposal of data users and shall provide data intermediation services through a separate legal person;
(b) the commercial terms, including pricing, for the provision of data intermediation services to a data holder or data user shall not be dependent upon whether the data holder or data user uses other services provided by the same data intermediation services provider or by a related entity, and if so to what degree the data holder or data user uses such other services;
(c) the data collected with respect to any activity of a natural or legal person for the purpose of the provision of the data intermediation service, including the date, time and geolocation data, duration of activity and connections to other natural or legal persons established by the person who uses the data intermediation service, shall be used only for the development of that data intermediation service, which may entail the use of data for the detection of fraud or cybersecurity, and shall be made available to the data holders upon request;
(d) the data intermediation services provider shall facilitate the exchange of the data in the format in which it receives it from a data subject or a data holder, shall convert the data into specific formats only to enhance interoperability within and across sectors or if requested by the data user or where mandated by Union law or to ensure harmonisation with international or European data standards and shall offer an opt-out possibility regarding those conversions to data subjects or data holders, unless the conversion is mandated by Union law;

---

[2] Data Governance Act, Article 12 - Conditions for providing data intermediation services, part 2/3  (distance 0.147)
Data Governance Act, Article 12: Conditions for providing data intermediation services
(e) data intermediation services may include offering additional specific tools and services to data holders or data subjects for the specific purpose of facilitating the exchange of data, such as temporary storage, curation, conversion, anonymisation and pseudonymisation, such tools being used only at the explicit request or approval of the data holder or data subject and third-party tools offered in that context not being used for other purposes;
(f) the data intermediation services provider shall ensure that the procedure for access to its service is fair, transparent and non-discriminatory for both data subjects and data holders, as well as for data users, including with regard to prices and terms of service;
(g) the data intermediation services provider shall have procedures in place to prevent fraudulent or abusive practices in relation to parties seeking access through its data intermediation services;
(h) the data intermediation services provider shall, in the event of its insolvency, ensure a reasonable continuity of the provision of its data intermediation services and, where such data intermediation services ensure the storage of data, shall have mechanisms in place to allow data holders and data users to obtain access to, to transfer or to retrieve their data and, where such data intermediation services are provided between data subjects and data users, to allow data subjects to exercise their rights;
(i) the data intermediation services provider shall take appropriate measures to ensure interoperability with other data intermediation services, inter alia , by means of commonly used open standards in the sector in which the data intermediation services provider operates;
(j) the data intermediation services provider shall put in place adequate technical, legal and organisational measures in order to prevent the transfer of or access to non-personal data that is unlawful under Union law or the national law of the relevant Member State;
(k) the data intermediation services provider shall without delay inform data holders in the event of an unauthorised transfer, access or use of the non-personal data that it has shared;

---

[3] Data Governance Act, Article 12 - Conditions for providing data intermediation services, part 3/3  (distance 0.156)
Data Governance Act, Article 12: Conditions for providing data intermediation services
(l) the data intermediation services provider shall take necessary measures to ensure an appropriate level of security for the storage, processing and transmission of non-personal data, and the data intermediation services provider shall further ensure the highest level of security for the storage and transmission of competitively sensitive information;
(m) the data intermediation services provider offering services to data subjects shall act in the data subjects’ best interest where it facilitates the exercise of their rights, in particular by informing and, where appropriate, advising data subjects in a concise, transparent, intelligible and easily accessible manner about intended data uses by data users and standard terms and conditions attached to such uses before data subjects give consent;
(n) where a data intermediation services provider provides tools for obtaining consent from data subjects or permissions to process data made available by data holders, it shall, where relevant, specify the third-country jurisdiction in which the data use is intended to take place and provide data subjects with tools to both give and withdraw consent and data holders with tools to both give and withdraw permissions to process data;
(o) the data intermediation services provider shall maintain a log record of the data intermediation activity.

---

[4] Data Act, Article 12 - Scope of obligations for data holders obliged pursuant to Union law to make data available  (distance 0.162)
Data Act, Article 12: Scope of obligations for data holders obliged pursuant to Union law to make data available
1. This Chapter shall apply where, in business-to-business relations, a data holder is obliged under Article 5 or under applicable Union law or national legislation adopted in accordance with Union law, to make data available to a data recipient.
2. A contractual term in a data sharing agreement which, to the detriment of one party, or, where applicable, to the detriment of the user, excludes the application of this Chapter, derogates from it, or varies its effect, shall not be binding on that party.

---

[5] Data Governance Act, Article 1 - Subject matter and scope, part 1/2  (distance 0.165)
Data Governance Act, Article 1: Subject matter and scope
1. This Regulation lays down:
(a) conditions for the re-use, within the Union, of certain categories of data held by public sector bodies;
(b) a notification and supervisory framework for the provision of data intermediation services;
(c) a framework for voluntary registration of entities which collect and process data made available for altruistic purposes; and
(d) a framework for the establishment of a European Data Innovation Board.
2. This Regulation does not create any obligation on public sector bodies to allow the re-use of data, nor does it release public sector bodies from their confidentiality obligations under Union or national law.
This Regulation is without prejudice to:
(a) specific provisions in Union or national law regarding the access to or re-use of certain categories of data, in particular with regard to the granting of access to and disclosure of official documents; and
(b) the obligations of public sector bodies under Union or national law to allow the re-use of data or to requirements related to processing of non-personal data.
Where sector-specific Union or national law requires public sector bodies, data intermediation services providers or recognised data altruism organisations to comply with specific additional technical, administrative or organisational requirements, including through an authorisation or certification regime, those provisions of that sector-specific Union or national law shall also apply. Any such specific additional requirements shall be non-discriminatory, proportionate and objectively justified.
```
</details>


---

## q30 (unanswerable)

**Question:** Can a Member State require that non-personal business data be stored only on servers in its own territory?

**Reference answer:** The corpus does not cover data localisation requirements for non-personal data. The assistant should say it cannot answer from the indexed documents.

**Agent answer:**

The indexed documents do not cover this. I searched for provisions on whether a Member State can require non-personal business data to be stored only on servers in its own territory.

<details><summary>Retrieved passages</summary>

```
[1] Data Act, Article 28 - Contractual transparency obligations on international access and transfer  (distance 0.231)
Data Act, Article 28: Contractual transparency obligations on international access and transfer
1. Providers of data processing services shall make the following information available on their websites, and keep that information up to date:
(a) the jurisdiction to which the ICT infrastructure deployed for data processing of their individual services is subject;
(b) a general description of the technical, organisational and contractual measures adopted by the provider of data processing services in order to prevent international governmental access to or transfer of non-personal data held in the Union where such access or transfer would create a conflict with Union law or the national law of the relevant Member State.
2. The websites referred to in paragraph 1 shall be listed in contracts for all data processing services offered by providers of data processing services.

---

[2] Data Act, Article 32 - International governmental access and transfer, part 1/3  (distance 0.249)
Data Act, Article 32: International governmental access and transfer
1. Providers of data processing services shall take all adequate technical, organisational and legal measures, including contracts, in order to prevent international and third-country governmental access and transfer of non-personal data held in the Union where such transfer or access would create a conflict with Union law or with the national law of the relevant Member State, without prejudice to paragraph 2 or 3.
2. Any decision or judgment of a third-country court or tribunal and any decision of a third-country administrative authority requiring a provider of data processing services to transfer or give access to non-personal data falling within the scope of this Regulation held in the Union shall be recognised or enforceable in any manner only if based on an international agreement, such as a mutual legal assistance treaty, in force between the requesting third country and the Union, or any such agreement between the requesting third country and a Member State.
3. In the absence of an international agreement as referred to in paragraph 2, where a provider of data processing services is the addressee of a decision or judgment of a third-country court or tribunal or a decision of a third-country administrative authority to transfer or give access to non-personal data falling within the scope of this Regulation held in the Union and compliance with such a decision would risk putting the addressee in conflict with Union law or with the national law of the relevant Member State, transfer to or access to such data by that third-country authority shall take place only where:
(a) the third-country system requires the reasons and proportionality of such a decision or judgment to be set out and requires such a decision or judgment to be specific in character, for instance by establishing a sufficient link to certain suspected persons or infringements;
(b) the reasoned objection of the addressee is subject to a review by a competent third-country court or tribunal; and

---

[3] Data Governance Act, Article 5 - Conditions for re-use, part 2/5  (distance 0.259)
Data Governance Act, Article 5: Conditions for re-use
(c) to access and re-use the data within the physical premises in which the secure processing environment is located in accordance with high security standards, provided that remote access cannot be allowed without jeopardising the rights and interests of third parties.
4. In the case of re-use allowed in accordance with paragraph 3, points (b) and (c), the public sector bodies shall impose conditions that preserve the integrity of the functioning of the technical systems of the secure processing environment used. The public sector body shall reserve the right to verify the process, the means and any results of processing of data undertaken by the re-user to preserve the integrity of the protection of the data and reserve the right to prohibit the use of results that contain information jeopardising the rights and interests of third parties. The decision to prohibit the use of the results shall be comprehensible and transparent to the re-user.
5. Unless national law provides for specific safeguards on applicable confidentiality obligations relating to the re-use of data referred to in Article 3(1), the public sector body shall make the re-use of data provided in accordance with paragraph 3 of this Article conditional on the adherence by the re-user to a confidentiality obligation that prohibits the disclosure of any information that jeopardises the rights and interests of third parties that the re-user may have acquired despite the safeguards put in place. Re-users shall be prohibited from re-identifying any data subject to whom the data relates and shall take technical and operational measures to prevent re-identification and to notify any data breach resulting in the re-identification of the data subjects concerned to the public sector body. In the event of the unauthorised re-use of non-personal data, the re-user shall, without delay, where appropriate with the assistance of the public sector body, inform the legal persons whose rights and interests may be affected.

---

[4] Data Act, Article 32 - International governmental access and transfer, part 3/3  (distance 0.259)
Data Act, Article 32: International governmental access and transfer
5. The provider of data processing services shall inform the customer about the existence of a request of a third-country authority to access its data before complying with that request, except where the request serves law enforcement purposes and for as long as this is necessary to preserve the effectiveness of the law enforcement activity.

---

[5] Data Governance Act, Article 5 - Conditions for re-use, part 1/5  (distance 0.262)
Data Governance Act, Article 5: Conditions for re-use
1. Public sector bodies which are competent under national law to grant or refuse access for the re-use of one or more of the categories of data referred to in Article 3(1) shall make publicly available the conditions for allowing such re-use and the procedure to request the re-use via the single information point referred to in Article 8. Where they grant or refuse access for re-use, they may be assisted by the competent bodies referred to in Article 7(1).
Member States shall ensure that public sector bodies are equipped with the necessary resources to comply with this Article.
2. Conditions for re-use shall be non-discriminatory, transparent, proportionate and objectively justified with regard to the categories of data and the purposes of re-use and the nature of the data for which re-use is allowed. Those conditions shall not be used to restrict competition.
3. Public sector bodies shall, in accordance with Union and national law, ensure that the protected nature of data is preserved. They may provide for the following requirements:
(a) to grant access for the re-use of data only where the public sector body or the competent body, following the request for re-use, has ensured that data has been: (i) anonymised, in the case of personal data; and (ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights; (i) anonymised, in the case of personal data; and (ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights;
(i) anonymised, in the case of personal data; and
(ii) modified, aggregated or treated by any other method of disclosure control, in the case of commercially confidential information, including trade secrets or content protected by intellectual property rights;
(b) to access and re-use the data remotely within a secure processing environment that is provided or controlled by the public sector body;

---

[1] Data Act, Article 28 - Contractual transparency obligations on international access and transfer  (distance 0.240)
Data Act, Article 28: Contractual transparency obligations on international access and transfer
1. Providers of data processing services shall make the following information available on their websites, and keep that information up to date:
(a) the jurisdiction to which the ICT infrastructure deployed for data processing of their individual services is subject;
(b) a general description of the technical, organisational and contractual measures adopted by the provider of data processing services in order to prevent international governmental access to or transfer of non-personal data held in the Union where such access or transfer would create a conflict with Union law or the national law of the relevant Member State.
2. The websites referred to in paragraph 1 shall be listed in contracts for all data processing services offered by providers of data processing services.

---

[2] Data Act, Article 1 - Subject matter and scope, part 1/3  (distance 0.241)
Data Act, Article 1: Subject matter and scope
1. This Regulation lays down harmonised rules, inter alia, on:
(a) the making available of product data and related service data to the user of the connected product or related service;
(b) the making available of data by data holders to data recipients;
(c) the making available of data by data holders to public sector bodies, the Commission, the European Central Bank and Union bodies, where there is an exceptional need for those data for the performance of a specific task carried out in the public interest;
(d) facilitating switching between data processing services;
(e) introducing safeguards against unlawful third-party access to non-personal data; and
(f) the development of interoperability standards for data to be accessed, transferred and used.
2. This Regulation covers personal and non-personal data, including the following types of data, in the following contexts:
(a) Chapter II applies to data, with the exception of content, concerning the performance, use and environment of connected products and related services;
(b) Chapter III applies to any private sector data that is subject to statutory data sharing obligations;
(c) Chapter IV applies to any private sector data accessed and used on the basis of contract between enterprises;
(d) Chapter V applies to any private sector data with a focus on non-personal data;
(e) Chapter VI applies to any data and services processed by providers of data processing services;
(f) Chapter VII applies to any non-personal data held in the Union by providers of data processing services.
3. This Regulation applies to:
(a) manufacturers of connected products placed on the market in the Union and providers of related services, irrespective of the place of establishment of those manufacturers and providers;
(b) users in the Union of connected products or related services as referred to in point (a);
(c) data holders, irrespective of their place of establishment, that make data available to data recipients in the Union;
(d) data recipients in the Union to whom data are made available;

---

[3] Data Act, Article 2 - Definitions, part 1/6  (distance 0.244)
Data Act, Article 2: Definitions
For the purposes of this Regulation, the following definitions apply:
(1) ‘data’ means any digital representation of acts, facts or information and any compilation of such acts, facts or information, including in the form of sound, visual or audio-visual recording;
(2) ‘metadata’ means a structured description of the contents or the use of data facilitating the discovery or use of that data;
(3) ‘personal data’ means personal data as defined in Article 4, point (1), of Regulation (EU) 2016/679;
(4) ‘non-personal data’ means data other than personal data;
(5) ‘connected product’ means an item that obtains, generates or collects data concerning its use or environment and that is able to communicate product data via an electronic communications service, physical connection or on-device access, and whose primary function is not the storing, processing or transmission of data on behalf of any party other than the user;
(6) ‘related service’ means a digital service, other than an electronic communications service, including software, which is connected with the product at the time of the purchase, rent or lease in such a way that its absence would prevent the connected product from performing one or more of its functions, or which is subsequently connected to the product by the manufacturer or a third party to add to, update or adapt the functions of the connected product;
(7) ‘processing’ means any operation or set of operations which is performed on data or on sets of data, whether or not by automated means, such as collection, recording, organisation, structuring, storage, adaptation or alteration, retrieval, consultation, use, disclosure by transmission, dissemination, or other means of making them available, alignment or combination, restriction, erasure or destruction;
(8) ‘data processing service’ means a digital service that is provided to a customer and that enables ubiquitous and on-demand network access to a shared pool of configurable, scalable and elastic computing resources of a centralised, distributed or highly distributed nature that can be rapidly provisioned and released with minimal management effort or service provider interaction;

---

[4] Data Act, Article 32 - International governmental access and transfer, part 1/3  (distance 0.248)
Data Act, Article 32: International governmental access and transfer
1. Providers of data processing services shall take all adequate technical, organisational and legal measures, including contracts, in order to prevent international and third-country governmental access and transfer of non-personal data held in the Union where such transfer or access would create a conflict with Union law or with the national law of the relevant Member State, without prejudice to paragraph 2 or 3.
2. Any decision or judgment of a third-country court or tribunal and any decision of a third-country administrative authority requiring a provider of data processing services to transfer or give access to non-personal data falling within the scope of this Regulation held in the Union shall be recognised or enforceable in any manner only if based on an international agreement, such as a mutual legal assistance treaty, in force between the requesting third country and the Union, or any such agreement between the requesting third country and a Member State.
3. In the absence of an international agreement as referred to in paragraph 2, where a provider of data processing services is the addressee of a decision or judgment of a third-country court or tribunal or a decision of a third-country administrative authority to transfer or give access to non-personal data falling within the scope of this Regulation held in the Union and compliance with such a decision would risk putting the addressee in conflict with Union law or with the national law of the relevant Member State, transfer to or access to such data by that third-country authority shall take place only where:
(a) the third-country system requires the reasons and proportionality of such a decision or judgment to be set out and requires such a decision or judgment to be specific in character, for instance by establishing a sufficient link to certain suspected persons or infringements;
(b) the reasoned objection of the addressee is subject to a review by a competent third-country court or tribunal; and

---

[5] Data Act, Article 1 - Subject matter and scope, part 3/3  (distance 0.258)
Data Act, Article 1: Subject matter and scope
This Regulation does not affect Union or national legal acts providing for the sharing of, access to and the use of data for the purpose of the prevention, investigation, detection or prosecution of criminal offences or for the execution of criminal penalties, or for customs and taxation purposes, in particular Regulations (EU) 2021/784, (EU) 2022/2065 and (EU) 2023/1543 and Directive (EU) 2023/1544, or international cooperation in that area. This Regulation does not apply to the collection or sharing of, access to or the use of data under Regulation (EU) 2015/847 and Directive (EU) 2015/849. This Regulation does not apply to areas that fall outside the scope of Union law and in any event does not affect the competences of the Member States concerning public security, defence or national security, regardless of the type of entity entrusted by the Member States to carry out tasks in relation to those competences, or their power to safeguard other essential State functions, including ensuring the territorial integrity of the State and the maintenance of law and order. This Regulation does not affect the competences of the Member States concerning customs and tax administration or the health and safety of citizens.
7. This Regulation complements the self-regulatory approach of Regulation (EU) 2018/1807 by adding generally applicable obligations on cloud switching.
8. This Regulation is without prejudice to Union and national legal acts providing for the protection of intellectual property rights, in particular Directives 2001/29/EC, 2004/48/EC and (EU) 2019/790.
9. This Regulation complements and is without prejudice to Union law which aims to promote the interests of consumers and ensure a high level of consumer protection, and to protect their health, safety and economic interests, in particular Directives 93/13/EEC, 2005/29/EC and 2011/83/EU.
10. This Regulation does not preclude the conclusion of voluntary lawful data sharing contracts, including contracts concluded on a reciprocal basis, which comply with the requirements laid down in this Regulation.
```
</details>


---

## q31 (unanswerable)

**Question:** How long can a website keep a tracking cookie before it has to ask for consent again?

**Reference answer:** The corpus contains no rules on cookies or tracking technologies and gives no such duration. The assistant should say so.

**Agent answer:**

The indexed documents do not cover this. I searched for rules on tracking cookie duration and consent renewal.

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 7 - Conditions for consent  (distance 0.344)
GDPR, Article 7: Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data.
2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding.
3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.
4. When assessing whether consent is freely given, utmost account shall be taken of whether, inter alia , the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

---

[2] GDPR, Article 13 - Information to be provided where personal data are collected from the data subject, part 1/2  (distance 0.353)
GDPR, Article 13: Information to be provided where personal data are collected from the data subject
1. Where personal data relating to a data subject are collected from the data subject, the controller shall, at the time when personal data are obtained, provide the data subject with all of the following information:
(a) the identity and the contact details of the controller and, where applicable, of the controller's representative;
(b) the contact details of the data protection officer, where applicable;
(c) the purposes of the processing for which the personal data are intended as well as the legal basis for the processing;
(d) where the processing is based on point (f) of Article 6(1), the legitimate interests pursued by the controller or by a third party;
(e) the recipients or categories of recipients of the personal data, if any;
(f) where applicable, the fact that the controller intends to transfer personal data to a third country or international organisation and the existence or absence of an adequacy decision by the Commission, or in the case of transfers referred to in Article 46 or 47, or the second subparagraph of Article 49(1), reference to the appropriate or suitable safeguards and the means by which to obtain a copy of them or where they have been made available.
2. In addition to the information referred to in paragraph 1, the controller shall, at the time when personal data are obtained, provide the data subject with the following further information necessary to ensure fair and transparent processing:
(a) the period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period;
(b) the existence of the right to request from the controller access to and rectification or erasure of personal data or restriction of processing concerning the data subject or to object to processing as well as the right to data portability;
(c) where the processing is based on point (a) of Article 6(1) or point (a) of Article 9(2), the existence of the right to withdraw consent at any time, without affecting the lawfulness of processing based on consent before its withdrawal;

---

[3] GDPR, Article 8 - Conditions applicable to child's consent in relation to information society services  (distance 0.372)
GDPR, Article 8: Conditions applicable to child's consent in relation to information society services
1. Where point (a) of Article 6(1) applies, in relation to the offer of information society services directly to a child, the processing of the personal data of a child shall be lawful where the child is at least 16 years old. Where the child is below the age of 16 years, such processing shall be lawful only if and to the extent that consent is given or authorised by the holder of parental responsibility over the child.
Member States may provide by law for a lower age for those purposes provided that such lower age is not below 13 years.
2. The controller shall make reasonable efforts to verify in such cases that consent is given or authorised by the holder of parental responsibility over the child, taking into consideration available technology.
3. Paragraph 1 shall not affect the general contract law of Member States such as the rules on the validity, formation or effect of a contract in relation to a child.

---

[4] GDPR, Article 42 - Certification, part 2/2  (distance 0.380)
GDPR, Article 42: Certification
7. Certification shall be issued to a controller or processor for a maximum period of three years and may be renewed, under the same conditions, provided that the relevant requirements continue to be met. Certification shall be withdrawn, as applicable, by the certification bodies referred to in Article 43 or by the competent supervisory authority where the requirements for the certification are not or are no longer met.
8. The Board shall collate all certification mechanisms and data protection seals and marks in a register and shall make them publicly available by any appropriate means.

---

[5] GDPR, Article 6 - Lawfulness of processing, part 1/3  (distance 0.382)
GDPR, Article 6: Lawfulness of processing
1. Processing shall be lawful only if and to the extent that at least one of the following applies:
(a) the data subject has given consent to the processing of his or her personal data for one or more specific purposes;
(b) processing is necessary for the performance of a contract to which the data subject is party or in order to take steps at the request of the data subject prior to entering into a contract;
(c) processing is necessary for compliance with a legal obligation to which the controller is subject;
(d) processing is necessary in order to protect the vital interests of the data subject or of another natural person;
(e) processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller;
(f) processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject which require protection of personal data, in particular where the data subject is a child.
Point (f) of the first subparagraph shall not apply to processing carried out by public authorities in the performance of their tasks.
2. Member States may maintain or introduce more specific provisions to adapt the application of the rules of this Regulation with regard to processing for compliance with points (c) and (e) of paragraph 1 by determining more precisely specific requirements for the processing and other measures to ensure lawful and fair processing including for other specific processing situations as provided for in Chapter IX.
3. The basis for the processing referred to in point (c) and (e) of paragraph 1 shall be laid down by:
(a) Union law; or
(b) Member State law to which the controller is subject.
```
</details>


---

## q32 (unanswerable)

**Question:** What conformity requirements apply to high-risk AI systems in the EU?

**Reference answer:** The indexed documents (GDPR, Data Act, Data Governance Act) do not cover AI systems or high-risk AI rules. The assistant should say so.

**Agent answer:**

The indexed documents do not cover this. I searched for requirements applicable to high-risk AI systems.

<details><summary>Retrieved passages</summary>

```
[1] Data Act, Article 36 - Essential requirements regarding smart contracts for executing data sharing agreements, part 1/4  (distance 0.269)
Data Act, Article 36: Essential requirements regarding smart contracts for executing data sharing agreements
1. The vendor of an application using smart contracts or, in the absence thereof, the person whose trade, business or profession involves the deployment of smart contracts for others in the context of executing an agreement or part of it, to make data available shall ensure that those smart contracts comply with the following essential requirements of:
(a) robustness and access control, to ensure that the smart contract has been designed to offer access control mechanisms and a very high degree of robustness to avoid functional errors and to withstand manipulation by third parties;
(b) safe termination and interruption, to ensure that a mechanism exists to terminate the continued execution of transactions and that the smart contract includes internal functions which can reset or instruct the contract to stop or interrupt the operation, in particular to avoid future accidental executions;
(c) data archiving and continuity, to ensure, in circumstances in which a smart contract must be terminated or deactivated, there is a possibility to archive the transactional data, smart contract logic and code in order to keep the record of operations performed on the data in the past (auditability);
(d) access control, to ensure that a smart contract is protected through rigorous access control mechanisms at the governance and smart contract layers; and
(e) consistency, to ensure consistency with the terms of the data sharing agreement that the smart contract executes.
2. The vendor of a smart contract or, in the absence thereof, the person whose trade, business or profession involves the deployment of smart contracts for others in the context of executing an agreement or part of it, to make data available shall perform a conformity assessment with a view to fulfilling the essential requirements laid down in paragraph 1 and, on the fulfilment of those requirements, issue an EU declaration of conformity.

---

[2] Data Act, Article 36 - Essential requirements regarding smart contracts for executing data sharing agreements, part 2/4  (distance 0.280)
Data Act, Article 36: Essential requirements regarding smart contracts for executing data sharing agreements
3. By drawing up the EU declaration of conformity, the vendor of an application using smart contracts or, in the absence thereof, the person whose trade, business or profession involves the deployment of smart contracts for others in the context of executing an agreement or part of it, to make data available shall be responsible for compliance with the essential requirements laid down in paragraph 1.
4. A smart contract that meets the harmonised standards or the relevant parts thereof, the references of which are published in the Official Journal of the European Union , shall be presumed to be in conformity with the essential requirements laid down in paragraph 1 to the extent that those requirements are covered by such harmonised standards or parts thereof.
5. The Commission shall, pursuant to Article 10 of Regulation (EU) No 1025/2012, request one or more European standardisation organisations to draft harmonised standards that satisfy the essential requirements laid down in paragraph 1 of this Article.
6. The Commission may, by means of implementing acts, adopt common specifications covering any or all of the essential requirements laid down in paragraph 1 where the following conditions have been fulfilled:
(a) the Commission has requested, pursuant to Article 10(1) of Regulation (EU) No 1025/2012, one or more European standardisation organisations to draft a harmonised standard that satisfies the essential requirements laid down in paragraph 1 of this Article and: (i) the request has not been accepted; (ii) the harmonised standards addressing that request are not delivered within the deadline set in accordance with Article 10(1) of Regulation (EU) No 1025/2012; or (iii) the harmonised standards do not comply with the request; and (i) the request has not been accepted; (ii) the harmonised standards addressing that request are not delivered within the deadline set in accordance with Article 10(1) of Regulation (EU) No 1025/2012; or (iii) the harmonised standards do not comply with the request; and
(i) the request has not been accepted;

---

[3] GDPR, Article 35 - Data protection impact assessment, part 1/3  (distance 0.294)
GDPR, Article 35: Data protection impact assessment
1. Where a type of processing in particular using new technologies, and taking into account the nature, scope, context and purposes of the processing, is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall, prior to the processing, carry out an assessment of the impact of the envisaged processing operations on the protection of personal data. A single assessment may address a set of similar processing operations that present similar high risks.
2. The controller shall seek the advice of the data protection officer, where designated, when carrying out a data protection impact assessment.
3. A data protection impact assessment referred to in paragraph 1 shall in particular be required in the case of:
(a) a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person;
(b) processing on a large scale of special categories of data referred to in Article 9(1), or of personal data relating to criminal convictions and offences referred to in Article 10; or
(c) a systematic monitoring of a publicly accessible area on a large scale.
4. The supervisory authority shall establish and make public a list of the kind of processing operations which are subject to the requirement for a data protection impact assessment pursuant to paragraph 1. The supervisory authority shall communicate those lists to the Board referred to in Article 68.
5. The supervisory authority may also establish and make public a list of the kind of processing operations for which no data protection impact assessment is required. The supervisory authority shall communicate those lists to the Board.

---

[4] Data Act, Article 33 - Essential requirements regarding interoperability of data, of data sharing mechanisms and services, as well as of common European data spaces, part 1/4  (distance 0.299)
Data Act, Article 33: Essential requirements regarding interoperability of data, of data sharing mechanisms and services, as well as of common European data spaces
1. Participants in data spaces that offer data or data services to other participants shall comply with the following essential requirements to facilitate the interoperability of data, of data sharing mechanisms and services, as well as of common European data spaces which are purpose- or sector-specific or cross-sectoral interoperable frameworks for common standards and practices to share or jointly process data for, inter alia, the development of new products and services, scientific research or civil society initiatives:
(a) the dataset content, use restrictions, licences, data collection methodology, data quality and uncertainty shall be sufficiently described, where applicable, in a machine-readable format, to allow the recipient to find, access and use the data;
(b) the data structures, data formats, vocabularies, classification schemes, taxonomies and code lists, where available, shall be described in a publicly available and consistent manner;
(c) the technical means to access the data, such as application programming interfaces, and their terms of use and quality of service shall be sufficiently described to enable automatic access and transmission of data between parties, including continuously, in bulk download or in real-time in a machine-readable format where that is technically feasible and does not hamper the good functioning of the connected product;
(d) where applicable, the means to enable the interoperability of tools for automating the execution of data sharing agreements, such as smart contracts shall be provided.
The requirements can have a generic nature or concern specific sectors, while taking fully into account the interrelation with requirements arising from other Union or national law.
2. The Commission is empowered to adopt delegated acts, in accordance with Article 45 of this Regulation to supplement this Regulation by further specifying the essential requirements laid down in paragraph 1 of this Article, in relation to those requirements that, by their nature, cannot produce the intended effect unless they are further specified in binding Union legal acts and in order to properly reflect technological and market developments.
The Commission shall when adopting delegated acts take into account the advice of the EDIB in accordance with Article 42, point (c)(iii).

---

[5] Data Act, Article 36 - Essential requirements regarding smart contracts for executing data sharing agreements, part 3/4  (distance 0.299)
Data Act, Article 36: Essential requirements regarding smart contracts for executing data sharing agreements
(ii) the harmonised standards addressing that request are not delivered within the deadline set in accordance with Article 10(1) of Regulation (EU) No 1025/2012; or
(iii) the harmonised standards do not comply with the request; and
(b) no reference to harmonised standards covering the relevant essential requirements laid down in paragraph 1 of this Article is published in the Official Journal of the European Union in accordance with Regulation (EU) No 1025/2012 and no such reference is expected to be published within a reasonable period.
Those implementing acts shall be adopted in accordance with the examination procedure referred to in Article 46(2).
7. Before preparing a draft implementing act referred to in paragraph 6 of this Article, the Commission shall inform the committee referred to in Article 22 of Regulation (EU) No 1025/2012 that it considers that the conditions in paragraph 6 of this Article have been fulfilled.
8. When preparing the draft implementing act referred to in paragraph 6, the Commission shall take into account the advice of the EDIB and views of other relevant bodies or expert groups and shall duly consult all relevant stakeholders.
9. The vendor of a smart contract or, in the absence thereof, the person whose trade, business or profession involves the deployment of smart contracts for others in the context of executing an agreement or part of it, to make data available that meet the common specifications established by implementing acts referred to in paragraph 6 or parts thereof shall be presumed to be in conformity with the essential requirements laid down in paragraph 1 to the extent that those requirements are covered by such common specifications or parts thereof.
```
</details>


---

## q33 (unanswerable)

**Question:** What amount did the Spanish data protection authority fine the last company that breached the GDPR?

**Reference answer:** The corpus contains legislation only, not enforcement decisions or fines imposed by any authority. The assistant should say so.

**Agent answer:**

The indexed documents do not cover this. I searched for information regarding fines issued by the Spanish data protection authority to specific companies.

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 83 - General conditions for imposing administrative fines, part 1/3  (distance 0.262)
GDPR, Article 83: General conditions for imposing administrative fines
1. Each supervisory authority shall ensure that the imposition of administrative fines pursuant to this Article in respect of infringements of this Regulation referred to in paragraphs 4, 5 and 6 shall in each individual case be effective, proportionate and dissuasive.
2. Administrative fines shall, depending on the circumstances of each individual case, be imposed in addition to, or instead of, measures referred to in points (a) to (h) and (j) of Article 58(2). When deciding whether to impose an administrative fine and deciding on the amount of the administrative fine in each individual case due regard shall be given to the following:
(a) the nature, gravity and duration of the infringement taking into account the nature scope or purpose of the processing concerned as well as the number of data subjects affected and the level of damage suffered by them;
(b) the intentional or negligent character of the infringement;
(c) any action taken by the controller or processor to mitigate the damage suffered by data subjects;
(d) the degree of responsibility of the controller or processor taking into account technical and organisational measures implemented by them pursuant to Articles 25 and 32;
(e) any relevant previous infringements by the controller or processor;
(f) the degree of cooperation with the supervisory authority, in order to remedy the infringement and mitigate the possible adverse effects of the infringement;
(g) the categories of personal data affected by the infringement;
(h) the manner in which the infringement became known to the supervisory authority, in particular whether, and if so to what extent, the controller or processor notified the infringement;
(i) where measures referred to in Article 58(2) have previously been ordered against the controller or processor concerned with regard to the same subject-matter, compliance with those measures;
(j) adherence to approved codes of conduct pursuant to Article 40 or approved certification mechanisms pursuant to Article 42; and
(k) any other aggravating or mitigating factor applicable to the circumstances of the case, such as financial benefits gained, or losses avoided, directly or indirectly, from the infringement.

---

[2] GDPR, Article 83 - General conditions for imposing administrative fines, part 2/3  (distance 0.265)
GDPR, Article 83: General conditions for imposing administrative fines
3. If a controller or processor intentionally or negligently, for the same or linked processing operations, infringes several provisions of this Regulation, the total amount of the administrative fine shall not exceed the amount specified for the gravest infringement.
4. Infringements of the following provisions shall, in accordance with paragraph 2, be subject to administrative fines up to 10 000 000 EUR, or in the case of an undertaking, up to 2 % of the total worldwide annual turnover of the preceding financial year, whichever is higher:
(a) the obligations of the controller and the processor pursuant to Articles 8, 11, 25 to 39 and 42 and 43;
(b) the obligations of the certification body pursuant to Articles 42 and 43;
(c) the obligations of the monitoring body pursuant to Article 41(4).
5. Infringements of the following provisions shall, in accordance with paragraph 2, be subject to administrative fines up to 20 000 000 EUR, or in the case of an undertaking, up to 4 % of the total worldwide annual turnover of the preceding financial year, whichever is higher:
(a) the basic principles for processing, including conditions for consent, pursuant to Articles 5, 6, 7 and 9;
(b) the data subjects' rights pursuant to Articles 12 to 22;
(c) the transfers of personal data to a recipient in a third country or an international organisation pursuant to Articles 44 to 49;
(d) any obligations pursuant to Member State law adopted under Chapter IX;
(e) non-compliance with an order or a temporary or definitive limitation on processing or the suspension of data flows by the supervisory authority pursuant to Article 58(2) or failure to provide access in violation of Article 58(1).
6. Non-compliance with an order by the supervisory authority as referred to in Article 58(2) shall, in accordance with paragraph 2 of this Article, be subject to administrative fines up to 20 000 000 EUR, or in the case of an undertaking, up to 4 % of the total worldwide annual turnover of the preceding financial year, whichever is higher.

---

[3] GDPR, Article 84 - Penalties  (distance 0.288)
GDPR, Article 84: Penalties
1. Member States shall lay down the rules on other penalties applicable to infringements of this Regulation in particular for infringements which are not subject to administrative fines pursuant to Article 83, and shall take all measures necessary to ensure that they are implemented. Such penalties shall be effective, proportionate and dissuasive.
2. Each Member State shall notify to the Commission the provisions of its law which it adopts pursuant to paragraph 1, by 25 May 2018 and, without delay, any subsequent amendment affecting them.

---

[4] GDPR, Article 82 - Right to compensation and liability  (distance 0.291)
GDPR, Article 82: Right to compensation and liability
1. Any person who has suffered material or non-material damage as a result of an infringement of this Regulation shall have the right to receive compensation from the controller or processor for the damage suffered.
2. Any controller involved in processing shall be liable for the damage caused by processing which infringes this Regulation. A processor shall be liable for the damage caused by processing only where it has not complied with obligations of this Regulation specifically directed to processors or where it has acted outside or contrary to lawful instructions of the controller.
3. A controller or processor shall be exempt from liability under paragraph 2 if it proves that it is not in any way responsible for the event giving rise to the damage.
4. Where more than one controller or processor, or both a controller and a processor, are involved in the same processing and where they are, under paragraphs 2 and 3, responsible for any damage caused by processing, each controller or processor shall be held liable for the entire damage in order to ensure effective compensation of the data subject.
5. Where a controller or processor has, in accordance with paragraph 4, paid full compensation for the damage suffered, that controller or processor shall be entitled to claim back from the other controllers or processors involved in the same processing that part of the compensation corresponding to their part of responsibility for the damage, in accordance with the conditions set out in paragraph 2.
6. Court proceedings for exercising the right to receive compensation shall be brought before the courts competent under the law of the Member State referred to in Article 79(2).

---

[5] GDPR, Article 83 - General conditions for imposing administrative fines, part 3/3  (distance 0.293)
GDPR, Article 83: General conditions for imposing administrative fines
7. Without prejudice to the corrective powers of supervisory authorities pursuant to Article 58(2), each Member State may lay down the rules on whether and to what extent administrative fines may be imposed on public authorities and bodies established in that Member State.
8. The exercise by the supervisory authority of its powers under this Article shall be subject to appropriate procedural safeguards in accordance with Union and Member State law, including effective judicial remedy and due process.
9. Where the legal system of the Member State does not provide for administrative fines, this Article may be applied in such a manner that the fine is initiated by the competent supervisory authority and imposed by competent national courts, while ensuring that those legal remedies are effective and have an equivalent effect to the administrative fines imposed by supervisory authorities. In any event, the fines imposed shall be effective, proportionate and dissuasive. Those Member States shall notify to the Commission the provisions of their laws which they adopt pursuant to this paragraph by 25 May 2018 and, without delay, any subsequent amendment law or amendment affecting them.
```
</details>


---

## q34 (unanswerable)

**Question:** What is the penalty in German law for breaching the Data Act?

**Reference answer:** The Data Act leaves penalties to Member States and the corpus has no national legislation, so the specific German penalty is not available. The assistant should say so.

**Agent answer:**

The indexed documents do not cover this. I searched for rules on penalties in German law for breaching the Data Act.

<details><summary>Retrieved passages</summary>

```
[1] Data Act, Article 40 - Penalties  (distance 0.163)
Data Act, Article 40: Penalties
1. Member States shall lay down the rules on penalties applicable to infringements of this Regulation and shall take all measures necessary to ensure that they are implemented. The penalties provided for shall be effective, proportionate and dissuasive.
2. Member States shall by 12 September 2025 notify the Commission of those rules and measures and shall notify it without delay of any subsequent amendment affecting them. The Commission shall regularly update and maintain an easily accessible public register of those measures.
3. Member States shall take into account the recommendations of the EDIB and the following non-exhaustive criteria for the imposition of penalties for infringements of this Regulation:
(a) the nature, gravity, scale and duration of the infringement;
(b) any action taken by the infringing party to mitigate or remedy the damage caused by the infringement;
(c) any previous infringements by the infringing party;
(d) the financial benefits gained or losses avoided by the infringing party due to the infringement, insofar as such benefits or losses can be reliably established;
(e) any other aggravating or mitigating factor applicable to the circumstances of the case;
(f) infringing party’s annual turnover in the preceding financial year in the Union.
4. For infringements of the obligations laid down in Chapter II, III and V of this Regulation, the supervisory authorities responsible for monitoring the application of Regulation (EU) 2016/679 may within their scope of competence impose administrative fines in accordance with Article 83 of Regulation (EU) 2016/679 and up to the amount referred to in Article 83(5) of that Regulation.
5. For infringements of the obligations laid down in Chapter V of this Regulation, the European Data Protection Supervisor may impose within its scope of competence administrative fines in accordance with Article 66 of Regulation (EU) 2018/1725 up to the amount referred to in Article 66(3) of that Regulation.

---

[2] Data Act, Article 37 - Competent authorities and data coordinators, part 4/5  (distance 0.189)
Data Act, Article 37: Competent authorities and data coordinators
12. For the purpose of ensuring compliance with this Regulation, a legal representative shall be mandated by an entity falling within the scope of this Regulation that makes connected products available or offers services in the Union to be addressed in addition to or instead of it by competent authorities with regard to all issues related to that entity. That legal representative shall cooperate with and comprehensively demonstrate to the competent authorities, upon request, the actions taken and provisions put in place by the entity falling within the scope of this Regulation that makes connected products available or offers services in the Union to ensure compliance with this Regulation.
13. An entity falling within the scope of this Regulation that makes connected products available or offers services in the Union, shall be considered to be under the competence of the Member State in which its legal representative is located. The designation of a legal representative by such an entity shall be without prejudice to the liability of, and any legal action that could be initiated against, such an entity. Until such time as an entity designates a legal representative in accordance with this Article, it shall be under the competence of all Member States, where applicable, for the purposes of ensuring the application and enforcement of this Regulation. Any competent authority may exercise its competence, including by imposing effective, proportionate and dissuasive penalties, provided that the entity is not subject to enforcement proceedings under this Regulation regarding the same facts by another competent authority.
14. Competent authorities shall have the power to request from users, data holders, or data recipients, or their legal representatives, falling under the competence of their Member State all information necessary to verify compliance with this Regulation. Any request for information shall be proportionate to the performance of the underlying task and shall be reasoned.

---

[3] Data Governance Act, Article 34 - Penalties  (distance 0.195)
Data Governance Act, Article 34: Penalties
1. Member States shall lay down the rules on penalties applicable to infringements of the obligations regarding transfers of non-personal data to third countries pursuant to Article 5(14) and Article 31, the notification obligation of data intermediation services providers pursuant to Article 11, the conditions for providing data intermediation services pursuant to Article 12 and the conditions for the registration as a recognised data altruism organisation pursuant to Articles 18, 20, 21 and 22, and shall take all measures necessary to ensure that they are implemented. The penalties provided for shall be effective, proportionate and dissuasive. In their rules on penalties, Member States shall take into account the recommendations of the European Data Innovation Board. Member States shall, by 24 September 2023, notify the Commission of those rules and of those measures and shall notify it, without delay, of any subsequent amendment affecting them.
2. Member States shall take into account the following non-exhaustive and indicative criteria for the imposition of penalties on data intermediation services providers and recognised data altruism organisations for infringements of this Regulation, where appropriate:
(a) the nature, gravity, scale and duration of the infringement;
(b) any action taken by the data intermediation services provider or recognised data altruism organisation to mitigate or remedy the damage caused by the infringement;
(c) any previous infringements by the data intermediation services provider or recognised data altruism organisation;
(d) the financial benefits gained or losses avoided by the data intermediation services provider or recognised data altruism organisation due to the infringement, insofar as such benefits or losses can be reliably established;
(e) any other aggravating or mitigating factors applicable to the circumstances of the case.

---

[4] Data Act, Article 37 - Competent authorities and data coordinators, part 2/5  (distance 0.215)
Data Act, Article 37: Competent authorities and data coordinators
(b) handling complaints arising from alleged infringements of this Regulation, including in relation to trade secrets, and investigating, to the extent appropriate, the subject matter of complaints and regularly informing complainants, where relevant in accordance with national law, of the progress and the outcome of the investigation within a reasonable period, in particular if further investigation or coordination with another competent authority is necessary;
(c) conducting investigations into matters that concern the application of this Regulation, including on the basis of information received from another competent authority or other public authority;
(d) imposing effective, proportionate and dissuasive financial penalties which may include periodic penalties and penalties with retroactive effect, or initiating legal proceedings for the imposition of fines;
(e) monitoring technological and relevant commercial developments of relevance for the making available and use of data;
(f) cooperating with competent authorities of other Member States and, where relevant, with the Commission or the EDIB, to ensure the consistent and efficient application of this Regulation, including the exchange of all relevant information by electronic means, without undue delay, including regarding paragraph 10 of this Article;
(g) cooperating with the relevant competent authorities responsible for the implementation of other Union or national legal acts, including with authorities competent in the field of data and electronic communication services, with the supervisory authority responsible for monitoring the application of Regulation (EU) 2016/679 or with sectoral authorities to ensure that this Regulation is enforced consistently with other Union and national law;
(h) cooperating with the relevant competent authorities to ensure that Articles 23 to 31 and Articles 34 and 35 are enforced consistently with other Union law and self-regulation applicable to providers of data processing services;
(i) ensuring that switching charges are withdrawn in accordance with Article 29;
(j) examining the requests for data made pursuant to Chapter V.
Where designated, the data coordinator shall facilitate the cooperation referred to in points (f), (g) and (h) of the first subparagraph and shall assist the competent authorities upon their request.
6. The data coordinator, where such competent authority has been designated, shall:

---

[5] Data Act, Article 37 - Competent authorities and data coordinators, part 1/5  (distance 0.224)
Data Act, Article 37: Competent authorities and data coordinators
1. Each Member State shall designate one or more competent authorities to be responsible for the application and enforcement of this Regulation (competent authorities). Member States may establish one or more new authorities or rely on existing authorities.
2. Where a Member State designates more than one competent authority, it shall designate a data coordinator from among them to facilitate cooperation between the competent authorities and to assist entities within the scope of this Regulation on all matters related to its application and enforcement. Competent authorities shall, in the exercise of the tasks and powers assigned to them under paragraph 5, cooperate with each other.
3. The supervisory authorities responsible for monitoring the application of Regulation (EU) 2016/679 shall be responsible for monitoring the application of this Regulation insofar as the protection of personal data is concerned. Chapters VI and VII of Regulation (EU) 2016/679 shall apply mutatis mutandis .
The European Data Protection Supervisor shall be responsible for monitoring the application of this Regulation insofar as it concerns the Commission, the European Central Bank or Union bodies. Where relevant, Article 62 of Regulation (EU) 2018/1725 shall apply mutatis mutandis .
The tasks and powers of the supervisory authorities referred to in this paragraph shall be exercised with regard to the processing of personal data.
4. Without prejudice to paragraph 1 of this Article:
(a) for specific sectoral data access and use issues related to the application of this Regulation, the competence of sectoral authorities shall be respected;
(b) the competent authority responsible for the application and enforcement of Articles 23 to 31 and Articles 34 and 35 shall have experience in the field of data and electronic communications services.
5. Member States shall ensure that the tasks and powers of the competent authorities are clearly defined and include:
(a) promoting data literacy and awareness among users and entities falling within the scope of this Regulation of the rights and obligations under this Regulation;
```
</details>


---

## q35 (unanswerable)

**Question:** For how many years must we keep customer invoices that contain personal data?

**Reference answer:** The corpus sets no retention periods for invoices or tax records. The assistant should say it cannot answer from the indexed documents.

**Agent answer:**

The indexed documents do not cover this. I searched for the retention period and number of years for keeping customer invoices containing personal data.

<details><summary>Retrieved passages</summary>

```
[1] GDPR, Article 5 - Principles relating to processing of personal data  (distance 0.320)
GDPR, Article 5: Principles relating to processing of personal data
1. Personal data shall be:
(a) processed lawfully, fairly and in a transparent manner in relation to the data subject (‘lawfulness, fairness and transparency’);
(b) collected for specified, explicit and legitimate purposes and not further processed in a manner that is incompatible with those purposes; further processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes shall, in accordance with Article 89(1), not be considered to be incompatible with the initial purposes (‘purpose limitation’);
(c) adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed (‘data minimisation’);
(d) accurate and, where necessary, kept up to date; every reasonable step must be taken to ensure that personal data that are inaccurate, having regard to the purposes for which they are processed, are erased or rectified without delay (‘accuracy’);
(e) kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed; personal data may be stored for longer periods insofar as the personal data will be processed solely for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) subject to implementation of the appropriate technical and organisational measures required by this Regulation in order to safeguard the rights and freedoms of the data subject (‘storage limitation’);
(f) processed in a manner that ensures appropriate security of the personal data, including protection against unauthorised or unlawful processing and against accidental loss, destruction or damage, using appropriate technical or organisational measures (‘integrity and confidentiality’).
2. The controller shall be responsible for, and be able to demonstrate compliance with, paragraph 1 (‘accountability’).

---

[2] GDPR, Article 30 - Records of processing activities, part 1/2  (distance 0.320)
GDPR, Article 30: Records of processing activities
1. Each controller and, where applicable, the controller's representative, shall maintain a record of processing activities under its responsibility. That record shall contain all of the following information:
(a) the name and contact details of the controller and, where applicable, the joint controller, the controller's representative and the data protection officer;
(b) the purposes of the processing;
(c) a description of the categories of data subjects and of the categories of personal data;
(d) the categories of recipients to whom the personal data have been or will be disclosed including recipients in third countries or international organisations;
(e) where applicable, transfers of personal data to a third country or an international organisation, including the identification of that third country or international organisation and, in the case of transfers referred to in the second subparagraph of Article 49(1), the documentation of suitable safeguards;
(f) where possible, the envisaged time limits for erasure of the different categories of data;
(g) where possible, a general description of the technical and organisational security measures referred to in Article 32(1).
2. Each processor and, where applicable, the processor's representative shall maintain a record of all categories of processing activities carried out on behalf of a controller, containing:
(a) the name and contact details of the processor or processors and of each controller on behalf of which the processor is acting, and, where applicable, of the controller's or the processor's representative, and the data protection officer;
(b) the categories of processing carried out on behalf of each controller;
(c) where applicable, transfers of personal data to a third country or an international organisation, including the identification of that third country or international organisation and, in the case of transfers referred to in the second subparagraph of Article 49(1), the documentation of suitable safeguards;
(d) where possible, a general description of the technical and organisational security measures referred to in Article 32(1).
3. The records referred to in paragraphs 1 and 2 shall be in writing, including in electronic form.

---

[3] GDPR, Article 17 - Right to erasure (‘right to be forgotten’), part 2/2  (distance 0.332)
GDPR, Article 17: Right to erasure (‘right to be forgotten’)
(c) for reasons of public interest in the area of public health in accordance with points (h) and (i) of Article 9(2) as well as Article 9(3);
(d) for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) in so far as the right referred to in paragraph 1 is likely to render impossible or seriously impair the achievement of the objectives of that processing; or
(e) for the establishment, exercise or defence of legal claims.

---

[4] GDPR, Article 13 - Information to be provided where personal data are collected from the data subject, part 1/2  (distance 0.341)
GDPR, Article 13: Information to be provided where personal data are collected from the data subject
1. Where personal data relating to a data subject are collected from the data subject, the controller shall, at the time when personal data are obtained, provide the data subject with all of the following information:
(a) the identity and the contact details of the controller and, where applicable, of the controller's representative;
(b) the contact details of the data protection officer, where applicable;
(c) the purposes of the processing for which the personal data are intended as well as the legal basis for the processing;
(d) where the processing is based on point (f) of Article 6(1), the legitimate interests pursued by the controller or by a third party;
(e) the recipients or categories of recipients of the personal data, if any;
(f) where applicable, the fact that the controller intends to transfer personal data to a third country or international organisation and the existence or absence of an adequacy decision by the Commission, or in the case of transfers referred to in Article 46 or 47, or the second subparagraph of Article 49(1), reference to the appropriate or suitable safeguards and the means by which to obtain a copy of them or where they have been made available.
2. In addition to the information referred to in paragraph 1, the controller shall, at the time when personal data are obtained, provide the data subject with the following further information necessary to ensure fair and transparent processing:
(a) the period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period;
(b) the existence of the right to request from the controller access to and rectification or erasure of personal data or restriction of processing concerning the data subject or to object to processing as well as the right to data portability;
(c) where the processing is based on point (a) of Article 6(1) or point (a) of Article 9(2), the existence of the right to withdraw consent at any time, without affecting the lawfulness of processing based on consent before its withdrawal;

---

[5] GDPR, Article 17 - Right to erasure (‘right to be forgotten’), part 1/2  (distance 0.342)
GDPR, Article 17: Right to erasure (‘right to be forgotten’)
1. The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay and the controller shall have the obligation to erase personal data without undue delay where one of the following grounds applies:
(a) the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed;
(b) the data subject withdraws consent on which the processing is based according to point (a) of Article 6(1), or point (a) of Article 9(2), and where there is no other legal ground for the processing;
(c) the data subject objects to the processing pursuant to Article 21(1) and there are no overriding legitimate grounds for the processing, or the data subject objects to the processing pursuant to Article 21(2);
(d) the personal data have been unlawfully processed;
(e) the personal data have to be erased for compliance with a legal obligation in Union or Member State law to which the controller is subject;
(f) the personal data have been collected in relation to the offer of information society services referred to in Article 8(1).
2. Where the controller has made the personal data public and is obliged pursuant to paragraph 1 to erase the personal data, the controller, taking account of available technology and the cost of implementation, shall take reasonable steps, including technical measures, to inform controllers which are processing the personal data that the data subject has requested the erasure by such controllers of any links to, or copy or replication of, those personal data.
3. Paragraphs 1 and 2 shall not apply to the extent that processing is necessary:
(a) for exercising the right of freedom of expression and information;
(b) for compliance with a legal obligation which requires processing by Union or Member State law to which the controller is subject or for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller;
```
</details>


---

## q36 (unanswerable)

**Question:** What cybersecurity requirements must a connected product meet before it can be sold in the EU?

**Reference answer:** The corpus does not cover product cybersecurity requirements (they are in separate legislation). The assistant should say so.

**Agent answer:**

The indexed documents do not cover this. I searched for cybersecurity requirements for connected products under the Data Act, GDPR, and Data Governance Act.

<details><summary>Retrieved passages</summary>

```
[1] Data Act, Article 3 - Obligation to make product data and related service data accessible to the user, part 1/2  (distance 0.211)
Data Act, Article 3: Obligation to make product data and related service data accessible to the user
1. Connected products shall be designed and manufactured, and related services shall be designed and provided, in such a manner that product data and related service data, including the relevant metadata necessary to interpret and use those data, are, by default, easily, securely, free of charge, in a comprehensive, structured, commonly used and machine-readable format, and, where relevant and technically feasible, directly accessible to the user.
2. Before concluding a contract for the purchase, rent or lease of a connected product, the seller, rentor or lessor, which may be the manufacturer, shall provide at least the following information to the user, in a clear and comprehensible manner:
(a) the type, format and estimated volume of product data which the connected product is capable of generating;
(b) whether the connected product is capable of generating data continuously and in real-time;
(c) whether the connected product is capable of storing data on-device or on a remote server, including, where applicable, the intended duration of retention;
(d) how the user may access, retrieve or, where relevant, erase the data, including the technical means to do so, as well as their terms of use and quality of service.
3. Before concluding a contract for the provision of a related service, the provider of such related service shall provide at least the following information to the user, in a clear and comprehensible manner:
(a) the nature, estimated volume and collection frequency of product data that the prospective data holder is expected to obtain and, where relevant, the arrangements for the user to access or retrieve such data, including the prospective data holder’s data storage arrangements and the duration of retention;
(b) the nature and estimated volume of related service data to be generated, as well as the arrangements for the user to access or retrieve such data, including the prospective data holder’s data storage arrangements and the duration of retention;

---

[2] Data Act, Article 1 - Subject matter and scope, part 1/3  (distance 0.214)
Data Act, Article 1: Subject matter and scope
1. This Regulation lays down harmonised rules, inter alia, on:
(a) the making available of product data and related service data to the user of the connected product or related service;
(b) the making available of data by data holders to data recipients;
(c) the making available of data by data holders to public sector bodies, the Commission, the European Central Bank and Union bodies, where there is an exceptional need for those data for the performance of a specific task carried out in the public interest;
(d) facilitating switching between data processing services;
(e) introducing safeguards against unlawful third-party access to non-personal data; and
(f) the development of interoperability standards for data to be accessed, transferred and used.
2. This Regulation covers personal and non-personal data, including the following types of data, in the following contexts:
(a) Chapter II applies to data, with the exception of content, concerning the performance, use and environment of connected products and related services;
(b) Chapter III applies to any private sector data that is subject to statutory data sharing obligations;
(c) Chapter IV applies to any private sector data accessed and used on the basis of contract between enterprises;
(d) Chapter V applies to any private sector data with a focus on non-personal data;
(e) Chapter VI applies to any data and services processed by providers of data processing services;
(f) Chapter VII applies to any non-personal data held in the Union by providers of data processing services.
3. This Regulation applies to:
(a) manufacturers of connected products placed on the market in the Union and providers of related services, irrespective of the place of establishment of those manufacturers and providers;
(b) users in the Union of connected products or related services as referred to in point (a);
(c) data holders, irrespective of their place of establishment, that make data available to data recipients in the Union;
(d) data recipients in the Union to whom data are made available;

---

[3] Data Act, Article 6 - Obligations of third parties receiving data at the request of the user, part 2/2  (distance 0.223)
Data Act, Article 6: Obligations of third parties receiving data at the request of the user
(f) use the data it receives in a manner that has an adverse impact on the security of the connected product or related service;
(g) disregard the specific measures agreed with a data holder or with the trade secrets holder pursuant to Article 5(9) and undermine the confidentiality of trade secrets;
(h) prevent the user that is a consumer, including on the basis of a contract, from making the data it receives available to other parties.

---

[4] Data Act, Article 2 - Definitions, part 1/6  (distance 0.225)
Data Act, Article 2: Definitions
For the purposes of this Regulation, the following definitions apply:
(1) ‘data’ means any digital representation of acts, facts or information and any compilation of such acts, facts or information, including in the form of sound, visual or audio-visual recording;
(2) ‘metadata’ means a structured description of the contents or the use of data facilitating the discovery or use of that data;
(3) ‘personal data’ means personal data as defined in Article 4, point (1), of Regulation (EU) 2016/679;
(4) ‘non-personal data’ means data other than personal data;
(5) ‘connected product’ means an item that obtains, generates or collects data concerning its use or environment and that is able to communicate product data via an electronic communications service, physical connection or on-device access, and whose primary function is not the storing, processing or transmission of data on behalf of any party other than the user;
(6) ‘related service’ means a digital service, other than an electronic communications service, including software, which is connected with the product at the time of the purchase, rent or lease in such a way that its absence would prevent the connected product from performing one or more of its functions, or which is subsequently connected to the product by the manufacturer or a third party to add to, update or adapt the functions of the connected product;
(7) ‘processing’ means any operation or set of operations which is performed on data or on sets of data, whether or not by automated means, such as collection, recording, organisation, structuring, storage, adaptation or alteration, retrieval, consultation, use, disclosure by transmission, dissemination, or other means of making them available, alignment or combination, restriction, erasure or destruction;
(8) ‘data processing service’ means a digital service that is provided to a customer and that enables ubiquitous and on-demand network access to a shared pool of configurable, scalable and elastic computing resources of a centralised, distributed or highly distributed nature that can be rapidly provisioned and released with minimal management effort or service provider interaction;

---

[5] Data Act, Article 4 - The rights and obligations of users and data holders with regard to access, use and making available product data and related service data, part 1/4  (distance 0.228)
Data Act, Article 4: The rights and obligations of users and data holders with regard to access, use and making available product data and related service data
1. Where data cannot be directly accessed by the user from the connected product or related service, data holders shall make readily available data, as well as the relevant metadata necessary to interpret and use those data, accessible to the user without undue delay, of the same quality as is available to the data holder, easily, securely, free of charge, in a comprehensive, structured, commonly used and machine-readable format and, where relevant and technically feasible, continuously and in real-time. This shall be done on the basis of a simple request through electronic means where technically feasible.
2. Users and data holders may contractually restrict or prohibit accessing, using or further sharing data, if such processing could undermine security requirements of the connected product, as laid down by Union or national law, resulting in a serious adverse effect on the health, safety or security of natural persons. Sectoral authorities may provide users and data holders with technical expertise in that context. Where the data holder refuses to share data pursuant to this Article, it shall notify the competent authority designated pursuant to Article 37.
3. Without prejudice to the user’s right to seek redress at any stage before a court or tribunal of a Member State, the user may, in relation to any dispute with the data holder concerning the contractual restrictions or prohibitions referred to in paragraph 2:
(a) lodge, in accordance with Article 37(5), point (b), a complaint with the competent authority; or
(b) agree with the data holder to refer the matter to a dispute settlement body in accordance with Article 10(1).
4. Data holders shall not make the exercise of choices or rights under this Article by the user unduly difficult, including by offering choices to the user in a non-neutral manner or by subverting or impairing the autonomy, decision-making or choices of the user via the structure, design, function or manner of operation of a user digital interface or a part thereof.
```
</details>


---

## q37 (unanswerable)

**Question:** What obligations do very large online platforms have to assess systemic risks?

**Reference answer:** The corpus does not cover platform regulation or systemic risk assessments. The assistant should say so.

**Agent answer:**

The indexed documents do not cover this. What obligations do very large online platforms have to assess systemic risks?

<details><summary>Retrieved passages</summary>

```
[1] Data Governance Act, Article 10 - Data intermediation services  (distance 0.323)
Data Governance Act, Article 10: Data intermediation services
The provision of the following data intermediation services shall comply with Article 12 and shall be subject to a notification procedure:
(a) intermediation services between data holders and potential data users, including making available the technical or other means to enable such services; those services may include bilateral or multilateral exchanges of data or the creation of platforms or databases enabling the exchange or joint use of data, as well as the establishment of other specific infrastructure for the interconnection of data holders with data users;
(b) intermediation services between data subjects that seek to make their personal data available or natural persons that seek to make non-personal data available, and potential data users, including making available the technical or other means to enable such services, and in particular enabling the exercise of the data subjects’ rights provided in Regulation (EU) 2016/679;
(c) services of data cooperatives.

---

[2] Data Act, Article 49 - Evaluation and review, part 2/2  (distance 0.325)
Data Act, Article 49: Evaluation and review
(g) whether the list of unfair contractual terms referred to in Article 13 is up-to-date in light of new business practices and the rapid pace of market innovation;
(h) changes in the contractual practices of providers of data processing services and whether this results in sufficient compliance with Article 25;
(i) the diminution of charges imposed by providers of data processing services for the switching process, in line with the gradual withdrawal of switching charges pursuant to Article 29;
(j) the interplay of this Regulation with other Union legal acts of relevance to the data economy;
(k) the prevention of unlawful governmental access to non-personal data;
(l) the efficacy of the enforcement regime required under Article 37;
(m) the impact of this Regulation on SMEs with regard to their capacity to innovate and to the availability of data processing services for users in the Union and the burden of complying with new obligations.
2. By 12 September 2028, the Commission shall carry out an evaluation of this Regulation and submit a report on its main findings to the European Parliament and to the Council, and to the European Economic and Social Committee. That evaluation shall assess the impact of Articles 23 to 31 and Articles 34 and 35, in particular regarding pricing and the diversity of data processing services offered within the Union, with a special focus on SME providers.
3. Member States shall provide the Commission with the information necessary for the preparation of the reports referred to in paragraphs 1 and 2.
4. On the basis of the reports referred to in paragraphs 1 and 2, the Commission may, where appropriate, submit a legislative proposal to the European Parliament and to the Council to amend this Regulation.

---

[3] Data Governance Act, Article 11 - Notification by data intermediation services providers, part 3/3  (distance 0.326)
Data Governance Act, Article 11: Notification by data intermediation services providers
In order to ensure that data intermediation services providers recognised in the Union are easily identifiable throughout the Union, the Commission shall, by means of implementing acts, establish a design for the common logo. Data intermediation services providers recognised in the Union shall display the common logo clearly on every online and offline publication that relates to their data intermediation activities.
Those implementing acts shall be adopted in accordance with the advisory procedure referred to in Article 33(2).
10. The competent authority for data intermediation services shall notify the Commission of each new notification by electronic means without delay. The Commission shall keep and regularly update a public register of all data intermediation services providers providing their services in the Union. The information referred to in paragraph 6, points (a), (b), (c), (d), (f) and (g), shall be published in the public register.
11. The competent authority for data intermediation services may charge fees for the notification in accordance with national law. Such fees shall be proportionate and objective and be based on the administrative costs related to the monitoring of compliance and other market control activities of the competent authority for data intermediation services in relation to notifications of data intermediation services providers. In the case of SMEs and start-ups, the competent authority for data intermediation services may charge a discounted fee or waive the fee.
12. Data intermediation services providers shall notify the competent authority for data intermediation services of any changes to the information provided pursuant to paragraph 6 within 14 days of the date of the change.
13. Where a data intermediation services provider ceases its activities, it shall notify the relevant competent authority for data intermediation services determined pursuant to paragraphs 1, 2 and 3 within 15 days.
14. The competent authority for data intermediation services shall notify the Commission of each notification referred to in paragraphs 12 and 13 by electronic means without delay. The Commission shall update the public register of the data intermediation services providers in the Union accordingly.

---

[4] Data Governance Act, Article 12 - Conditions for providing data intermediation services, part 2/3  (distance 0.328)
Data Governance Act, Article 12: Conditions for providing data intermediation services
(e) data intermediation services may include offering additional specific tools and services to data holders or data subjects for the specific purpose of facilitating the exchange of data, such as temporary storage, curation, conversion, anonymisation and pseudonymisation, such tools being used only at the explicit request or approval of the data holder or data subject and third-party tools offered in that context not being used for other purposes;
(f) the data intermediation services provider shall ensure that the procedure for access to its service is fair, transparent and non-discriminatory for both data subjects and data holders, as well as for data users, including with regard to prices and terms of service;
(g) the data intermediation services provider shall have procedures in place to prevent fraudulent or abusive practices in relation to parties seeking access through its data intermediation services;
(h) the data intermediation services provider shall, in the event of its insolvency, ensure a reasonable continuity of the provision of its data intermediation services and, where such data intermediation services ensure the storage of data, shall have mechanisms in place to allow data holders and data users to obtain access to, to transfer or to retrieve their data and, where such data intermediation services are provided between data subjects and data users, to allow data subjects to exercise their rights;
(i) the data intermediation services provider shall take appropriate measures to ensure interoperability with other data intermediation services, inter alia , by means of commonly used open standards in the sector in which the data intermediation services provider operates;
(j) the data intermediation services provider shall put in place adequate technical, legal and organisational measures in order to prevent the transfer of or access to non-personal data that is unlawful under Union law or the national law of the relevant Member State;
(k) the data intermediation services provider shall without delay inform data holders in the event of an unauthorised transfer, access or use of the non-personal data that it has shared;

---

[5] Data Governance Act, Article 11 - Notification by data intermediation services providers, part 2/3  (distance 0.332)
Data Governance Act, Article 11: Notification by data intermediation services providers
(a) the name of the data intermediation services provider;
(b) the data intermediation services provider’s legal status, form, ownership structure, relevant subsidiaries and, where the data intermediation services provider is registered in a trade or other similar public national register, registration number;
(c) the address of the data intermediation services provider’s main establishment in the Union, if any, and, where applicable, of any secondary branch in another Member State or that of the legal representative;
(d) a public website where complete and up-to-date information on the data intermediation services provider and the activities can be found, including as a minimum the information referred to in points (a), (b), (c) and (f);
(e) the data intermediation services provider’s contact persons and contact details;
(f) a description of the data intermediation service the data intermediation services provider intends to provide, and an indication of the categories listed in Article 10 under which such data intermediation service falls;
(g) the estimated date for starting the activity, if different from the date of the notification.
7. The competent authority for data intermediation services shall ensure that the notification procedure is non-discriminatory and does not distort the competition.
8. At the request of the data intermediation services provider, the competent authority for data intermediation services shall, within one week of a duly and fully completed notification, issue a standardised declaration, confirming that the data intermediation services provider has submitted the notification referred to in paragraph 1 and that the notification contains the information referred to in paragraph 6.
9. At the request of the data intermediation services provider, the competent authority for data intermediation services shall confirm that the data intermediation services provider complies with this Article and Article 12. Upon receipt of such a confirmation, that data intermediation services provider may use the label ‘data intermediation services provider recognised in the Union’ in its written and spoken communication, as well as a common logo.
```
</details>
