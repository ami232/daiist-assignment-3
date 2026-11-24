# Answers to grade by hand

Fill eval/human_labels.csv (id, correct, supported, notes) with the rules in eval/rubric.md, before looking at eval/judgments.jsonl.

## q01 (single)

**Question.** Someone got into our server and copied our customers' email addresses. How long do we have to tell the regulator?

**Reference.** The controller must notify the supervisory authority without undue delay and, where feasible, within 72 hours of becoming aware of the breach, unless the breach is unlikely to result in a risk to individuals. *(expected: GDPR Article 33(1))*

**Agent answer.**

You must notify the supervisory authority without undue delay and, where feasible, not later than 72 hours after having become aware of the personal data breach, unless the breach is unlikely to result in a risk to the rights and freedoms of natural persons.

* The controller must notify the competent supervisory authority without undue delay and, where feasible, within 72 hours of becoming aware of the breach, unless it is unlikely to result in a risk to rights and freedoms (GDPR Article 33(1)).
* If the notification is not made within 72 hours, it must be accompanied by reasons for the delay (GDPR Article 33(1)).
* If you are a processor rather than the controller, you must notify the controller without undue delay after becoming aware of the breach (GDPR Article 33(2)).
* The notification must describe the nature of the breach, categories and approximate numbers of data subjects and records concerned, and provide contact details for your data protection officer or other contact point (GDPR Article 33(3)).
* Information that cannot be provided simultaneously may be supplied in phases without undue further delay (GDPR Article 33(4)).

**Cited:** GDPR Article 33  
**Retrieved:** GDPR Article 33, GDPR Article 34, GDPR Article 77

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: personal data breach notification to supervisory authority time limit GDPR

[1] GDPR Article 33(1)-(2) (similarity 0.821)
GDPR Article 33(1)-(2) - Notification of a personal data breach to the supervisory authority
1. In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority competent in accordance with Article 55, unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where the notification to the supervisory authority is not made within 72 hours, it shall be accompanied by reasons for the delay. 2. The processor shall notify the controller without undue delay after becoming aware of a personal data breach.

[2] GDPR Article 33(3) (similarity 0.778)
GDPR Article 33(3) - Notification of a personal data breach to the supervisory authority
3. The notification referred to in paragraph 1 shall at least: (a) describe the nature of the personal data breach including where possible, the categories and approximate number of data subjects concerned and the categories and approximate number of personal data records concerned; (b) communicate the name and contact details of the data protection officer or other contact point where more information can be obtained; (c) describe the likely consequences of the personal data breach; (d) describe the measures taken or proposed to be taken by the controller to address the personal data breach, including, where appropriate, measures to mitigate its possible adverse effects.

[3] GDPR Article 33(4)-(5) (similarity 0.768)
GDPR Article 33(4)-(5) - Notification of a personal data breach to the supervisory authority
4. Where, and in so far as, it is not possible to provide the information at the same time, the information may be provided in phases without undue further delay. 5. The controller shall document any personal data breaches, comprising the facts relating to the personal data breach, its effects and the remedial action taken. That documentation shall enable the supervisory authority to verify compliance with this Article.

[4] GDPR Article 77 (similarity 0.758)
GDPR Article 77 - Right to lodge a complaint with a supervisory authority
1. Without prejudice to any other administrative or judicial remedy, every data subject shall have the right to lodge a complaint with a supervisory authority, in particular in the Member State of his or her habitual residence, place of work or place of the alleged infringement if the data subject considers that the processing of personal data relating to him or her infringes this Regulation. 2. The supervisory authority with which the complaint has been lodged shall inform the complainant on the progress and the outcome of the complaint including the possibility of a judicial remedy pursuant to Article 78.

[5] GDPR Article 34(4) (similarity 0.753)
GDPR Article 34(4) - Communication of a personal data breach to the data subject
4. If the controller has not already communicated the personal data breach to the data subject, the supervisory authority, having considered the likelihood of the personal data breach resulting in a high risk, may require it to do so or may decide that any of the conditions referred to in paragraph 3 are met.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q02 (single)

**Question.** What is the worst-case fine if we ignore the basic data protection principles or block users from exercising their rights?

**Reference.** Up to EUR 20 million or, for an undertaking, up to 4% of total worldwide annual turnover of the preceding financial year, whichever is higher. *(expected: GDPR Article 83(5))*

**Agent answer.**

The worst-case administrative fine for infringing basic data protection principles or blocking user rights is up to 20,000,000 EUR, or in the case of an undertaking, up to 4% of the total worldwide annual turnover of the preceding financial year, whichever is higher.

* Infringements of the basic principles for processing (Articles 5, 6, 7, and 9) fall under the highest tier of administrative fines.
* Infringements of data subjects' rights (Articles 12 to 22) also fall under this same highest tier.
* Fines must be imposed on a case-by-case basis and be effective, proportionate, and dissuasive, taking into account factors such as gravity, intentional or negligent character, and mitigation measures.
* Supervisory authorities may impose these fines either in addition to or instead of corrective powers such as bans on processing or compliance orders.
* If a controller or processor intentionally or negligently infringes several provisions for the same or linked processing operations, the total fine cannot exceed the amount specified for the gravest infringement.

- GDPR Article 83(5)
- GDPR Article 83(1)
- GDPR Article 83(2)
- GDPR Article 83(3)
- GDPR Article 58(2)

**Cited:** GDPR Article 58, GDPR Article 83  
**Retrieved:** GDPR Article 5, GDPR Article 58, GDPR Article 83

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: fine basic principles data protection rights GDPR infringement

[1] GDPR Article 83(5) (similarity 0.800)
GDPR Article 83(5) - General conditions for imposing administrative fines
5. Infringements of the following provisions shall, in accordance with paragraph 2, be subject to administrative fines up to 20 000 000 EUR, or in the case of an undertaking, up to 4 % of the total worldwide annual turnover of the preceding financial year, whichever is higher: (a) the basic principles for processing, including conditions for consent, pursuant to Articles 5, 6, 7 and 9; (b) the data subjects' rights pursuant to Articles 12 to 22; (c) the transfers of personal data to a recipient in a third country or an international organisation pursuant to Articles 44 to 49; (d) any obligations pursuant to Member State law adopted under Chapter IX; (e) non-compliance with an order or a temporary or definitive limitation on processing or the suspension of data flows by the supervisory authority pursuant to Article 58(2) or failure to provide access in violation of Article 58(1).

[2] GDPR Article 83(1)-(2) (similarity 0.789)
GDPR Article 83(1)-(2) - General conditions for imposing administrative fines
1. Each supervisory authority shall ensure that the imposition of administrative fines pursuant to this Article in respect of infringements of this Regulation referred to in paragraphs 4, 5 and 6 shall in each individual case be effective, proportionate and dissuasive. 2. Administrative fines shall, depending on the circumstances of each individual case, be imposed in addition to, or instead of, measures referred to in points (a) to (h) and (j) of Article 58(2). When deciding whether to impose an administrative fine and deciding on the amount of the administrative fine in each individual case due regard shall be given to the following: (a) the nature, gravity and duration of the infringement taking into account the nature scope or purpose of the processing concerned as well as the number of data subjects affected and the level of damage suffered by them; (b) the intentional or negligent character of the infringement; (c) any action taken by the controller or processor to mitigate the damage suffered by data subjects; (d) the degree of responsibility of the controller or processor taking into account technical and organisational measures implemented by them pursuant to Articles 25 and 32; (e) any relevant previous infringements by the controller or processor; (f) the degree of cooperation with the supervisory authority, in order to remedy the infringement and mitigate the possible adverse effects of the infringement; (g) the categories of personal data affected by the infringement; (h) the manner in which the infringement became known to the supervisory authority, in particular whether, and if so to what extent, the controller or processor notified the infringement; (i) where measures referred to in Article 58(2) have previously been ordered against the controller or processor concerned with regard to the same subject-matter, compliance with those measures; (j) adherence to approved codes of conduct pursuant to Article 40 or approved certification mechanisms pursuant to Article 42; and (k) any other aggravating or mitigating factor applicable to the circumstances of the case, such as financial benefits gained, or losses avoided, directly or indirectly, from the infringement.

[3] GDPR Article 83(3)-(4) (similarity 0.778)
GDPR Article 83(3)-(4) - General conditions for imposing administrative fines
3. If a controller or processor intentionally or negligently, for the same or linked processing operations, infringes several provisions of this Regulation, the total amount of the administrative fine shall not exceed the amount specified for the gravest infringement. 4. Infringements of the following provisions shall, in accordance with paragraph 2, be subject to administrative fines up to 10 000 000 EUR, or in the case of an undertaking, up to 2 % of the total worldwide annual turnover of the preceding financial year, whichever is higher: (a) the obligations of the controller and the processor pursuant to Articles 8, 11, 25 to 39 and 42 and 43; (b) the obligations of the certification body pursuant to Articles 42 and 43; (c) the obligations of the monitoring body pursuant to Article 41(4).

[4] GDPR Article 5 (similarity 0.760)
GDPR Article 5 - Principles relating to processing of personal data
1. Personal data shall be: (a) processed lawfully, fairly and in a transparent manner in relation to the data subject ('lawfulness, fairness and transparency'); (b) collected for specified, explicit and legitimate purposes and not further processed in a manner that is incompatible with those purposes; further processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes shall, in accordance with Article 89(1), not be considered to be incompatible with the initial purposes ('purpose limitation'); (c) adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed ('data minimisation'); (d) accurate and, where necessary, kept up to date; every reasonable step must be taken to ensure that personal data that are inaccurate, having regard to the purposes for which they are processed, are erased or rectified without delay ('accuracy'); (e) kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed; personal data may be stored for longer periods insofar as the personal data will be processed solely for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) subject to implementation of the appropriate technical and organisational measures required by this Regulation in order to safeguard the rights and freedoms of the data subject ('storage limitation'); (f) processed in a manner that ensures appropriate security of the personal data, including protection against unauthorised or unlawful processing and against accidental loss, destruction or damage, using appropriate technical or organisational measures ('integrity and confidentiality'). 2. The controller shall be responsible for, and be able to demonstrate compliance with, paragraph 1 ('accountability').

[5] GDPR Article 58(2) (similarity 0.753)
GDPR Article 58(2) - Powers
2. Each supervisory authority shall have all of the following corrective powers: (a) to issue warnings to a controller or processor that intended processing operations are likely to infringe provisions of this Regulation; (b) to issue reprimands to a controller or a processor where processing operations have infringed provisions of this Regulation; (c) to order the controller or the processor to comply with the data subject's requests to exercise his or her rights pursuant to this Regulation; (d) to order the controller or processor to bring processing operations into compliance with the provisions of this Regulation, where appropriate, in a specified manner and within a specified period; (e) to order the controller to communicate a personal data breach to the data subject; (f) to impose a temporary or definitive limitation including a ban on processing; (g) to order the rectification or erasure of personal data or restriction of processing pursuant to Articles 16, 17 and 18 and the notification of such actions to recipients to whom the personal data have been disclosed pursuant to Article 17(2) and Article 19; (h) to withdraw a certification or to order the certification body to withdraw a certification issued pursuant to Articles 42 and 43, or to order the certification body not to issue certification if the requirements for the certification are not or are no longer met; (i) to impose an administrative fine pursuant to Article 83, in addition to, or instead of measures referred to in this paragraph, depending on the circumstances of each individual case; (j) to order the suspension of data flows to a recipient in a third country or to an international organisation.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q03 (single)

**Question.** Our fitness app tracks the location of thousands of users all day. Do we have to appoint a data protection officer?

**Reference.** Yes. A DPO is required when the core activities consist of regular and systematic monitoring of data subjects on a large scale. *(expected: GDPR Article 37(1)(b))*

**Agent answer.**

You must appoint a data protection officer if your fitness app's core activities consist of processing operations that require regular and systematic monitoring of data subjects on a large scale.

* You must designate a data protection officer if your core activities require regular and systematic monitoring of data subjects on a large scale. (GDPR Article 37(1)(b))
* A data protection officer is also required if your core activities consist of processing special categories of data on a large scale. (GDPR Article 37(1)(c))
* The data protection officer may be a staff member or fulfill the tasks via a service contract. (GDPR Article 37(6))
* You must publish the contact details of the data protection officer and communicate them to the supervisory authority. (GDPR Article 37(7))

**Cited:** GDPR Article 37  
**Retrieved:** GDPR Article 35, GDPR Article 37, GDPR Article 39

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: data protection officer designation core activities regular and systematic monitoring location data GDPR

[1] GDPR Article 37(1) (similarity 0.804)
GDPR Article 37(1) - Designation of the data protection officer
1. The controller and the processor shall designate a data protection officer in any case where: (a) the processing is carried out by a public authority or body, except for courts acting in their judicial capacity; (b) the core activities of the controller or the processor consist of processing operations which, by virtue of their nature, their scope and/or their purposes, require regular and systematic monitoring of data subjects on a large scale; or (c) the core activities of the controller or the processor consist of processing on a large scale of special categories of data pursuant to Article 9 and personal data relating to criminal convictions and offences referred to in Article 10.

[2] GDPR Article 35(3) (similarity 0.751)
GDPR Article 35(3) - Data protection impact assessment
3. A data protection impact assessment referred to in paragraph 1 shall in particular be required in the case of: (a) a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person; (b) processing on a large scale of special categories of data referred to in Article 9(1), or of personal data relating to criminal convictions and offences referred to in Article 10; or (c) a systematic monitoring of a publicly accessible area on a large scale.

[3] GDPR Article 37(5)-(7) (similarity 0.749)
GDPR Article 37(5)-(7) - Designation of the data protection officer
5. The data protection officer shall be designated on the basis of professional qualities and, in particular, expert knowledge of data protection law and practices and the ability to fulfil the tasks referred to in Article 39. 6. The data protection officer may be a staff member of the controller or processor, or fulfil the tasks on the basis of a service contract. 7. The controller or the processor shall publish the contact details of the data protection officer and communicate them to the supervisory authority.

[4] GDPR Article 39 (similarity 0.733)
GDPR Article 39 - Tasks of the data protection officer
1. The data protection officer shall have at least the following tasks: (a) to inform and advise the controller or the processor and the employees who carry out processing of their obligations pursuant to this Regulation and to other Union or Member State data protection provisions; (b) to monitor compliance with this Regulation, with other Union or Member State data protection provisions and with the policies of the controller or processor in relation to the protection of personal data, including the assignment of responsibilities, awareness-raising and training of staff involved in processing operations, and the related audits; (c) to provide advice where requested as regards the data protection impact assessment and monitor its performance pursuant to Article 35; (d) to cooperate with the supervisory authority; (e) to act as the contact point for the supervisory authority on issues relating to processing, including the prior consultation referred to in Article 36, and to consult, where appropriate, with regard to any other matter. 2. The data protection officer shall in the performance of his or her tasks have due regard to the risk associated with processing operations, taking into account the nature, scope, context and purposes of processing.

[5] GDPR Article 37(2)-(4) (similarity 0.729)
GDPR Article 37(2)-(4) - Designation of the data protection officer
2. A group of undertakings may appoint a single data protection officer provided that a data protection officer is easily accessible from each establishment. 3. Where the controller or the processor is a public authority or body, a single data protection officer may be designated for several such authorities or bodies, taking account of their organisational structure and size. 4. In cases other than those referred to in paragraph 1, the controller or processor or associations and other bodies representing categories of controllers or processors may or, where required by Union or Member State law shall, designate a data protection officer. The data protection officer may act for such associations and other bodies representing controllers or processors.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q04 (single)

**Question.** A customer emailed asking for a copy of everything we hold on them. How long do we have to answer?

**Reference.** Within one month of receiving the request, extendable by two further months where necessary given complexity and number of requests, informing the person of the extension within the first month. *(expected: GDPR Article 12(3))*

**Agent answer.**

You must respond to the data subject's request without undue delay and at the latest within one month of receipt.

* The controller must provide information on action taken on a request under Articles 15 to 22 without undue delay and in any event within one month of receipt of the request. (GDPR Article 12(3))
* The one-month period may be extended by two further months where necessary, taking into account the complexity and number of the requests. (GDPR Article 12(3))
* The controller must inform the data subject of any such extension within one month of receipt of the request, together with the reasons for the delay. (GDPR Article 12(3))
* Where the data subject makes the request by electronic means, the information shall be provided by electronic means where possible, unless otherwise requested by the data subject. (GDPR Article 12(3))

**Cited:** GDPR Article 12  
**Retrieved:** Data Act Article 18, GDPR Article 12, GDPR Article 15

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: time limit response data subject access request copy personal data

[1] GDPR Article 12(2)-(3) (similarity 0.748)
GDPR Article 12(2)-(3) - Transparent information, communication and modalities for the exercise of the rights of the data subject
2. The controller shall facilitate the exercise of data subject rights under Articles 15 to 22. In the cases referred to in Article 11(2), the controller shall not refuse to act on the request of the data subject for exercising his or her rights under Articles 15 to 22, unless the controller demonstrates that it is not in a position to identify the data subject. 3. The controller shall provide information on action taken on a request under Articles 15 to 22 to the data subject without undue delay and in any event within one month of receipt of the request. That period may be extended by two further months where necessary, taking into account the complexity and number of the requests. The controller shall inform the data subject of any such extension within one month of receipt of the request, together with the reasons for the delay. Where the data subject makes the request by electronic form means, the information shall be provided by electronic means where possible, unless otherwise requested by the data subject.

[2] GDPR Article 12(4)-(5) (similarity 0.741)
GDPR Article 12(4)-(5) - Transparent information, communication and modalities for the exercise of the rights of the data subject
4. If the controller does not take action on the request of the data subject, the controller shall inform the data subject without delay and at the latest within one month of receipt of the request of the reasons for not taking action and on the possibility of lodging a complaint with a supervisory authority and seeking a judicial remedy. 5. Information provided under Articles 13 and 14 and any communication and any actions taken under Articles 15 to 22 and 34 shall be provided free of charge. Where requests from a data subject are manifestly unfounded or excessive, in particular because of their repetitive character, the controller may either: (a) charge a reasonable fee taking into account the administrative costs of providing the information or communication or taking the action requested; or (b) refuse to act on the request. The controller shall bear the burden of demonstrating the manifestly unfounded or excessive character of the request.

[3] Data Act Article 18(1)-(2) (similarity 0.716)
Data Act Article 18(1)-(2) - Compliance with requests for data
1. A data holder receiving a request to make data available under this Chapter shall make the data available to the requesting public sector body, the Commission, the European Central Bank or a Union body without undue delay, taking into account necessary technical, organisational and legal measures. 2. Without prejudice to specific needs regarding the availability of data defined in Union or national law, a data holder may decline or seek the modification of a request to make data available under this Chapter without undue delay and, in any event, no later than five working days after the receipt of a request for the data necessary to respond to a public emergency and without undue delay and, in any event, no later than 30 working days after the receipt of such a request in other cases of an exceptional need, on any of the following grounds: (a) the data holder does not have control over the data requested; (b) a similar request for the same purpose has been previously submitted by another public sector body or the Commission, the European Central Bank or a Union body and the data holder has not been notified of the erasure of the data pursuant to Article 19(1), point (c); (c) the request does not meet the conditions laid down in Article 17(1) and (2).

[4] GDPR Article 15(2)-(4) (similarity 0.714)
GDPR Article 15(2)-(4) - Right of access by the data subject
2. Where personal data are transferred to a third country or to an international organisation, the data subject shall have the right to be informed of the appropriate safeguards pursuant to Article 46 relating to the transfer. 3. The controller shall provide a copy of the personal data undergoing processing. For any further copies requested by the data subject, the controller may charge a reasonable fee based on administrative costs. Where the data subject makes the request by electronic means, and unless otherwise requested by the data subject, the information shall be provided in a commonly used electronic form. 4. The right to obtain a copy referred to in paragraph 3 shall not adversely affect the rights and freedoms of others.

[5] GDPR Article 15(1) (similarity 0.708)
GDPR Article 15(1) - Right of access by the data subject
1. The data subject shall have the right to obtain from the controller confirmation as to whether or not personal data concerning him or her are being processed, and, where that is the case, access to the personal data and the following information: (a) the purposes of the processing; (b) the categories of personal data concerned; (c) the recipients or categories of recipient to whom the personal data have been or will be disclosed, in particular recipients in third countries or international organisations; (d) where possible, the envisaged period for which the personal data will be stored, or, if not possible, the criteria used to determine that period; (e) the existence of the right to request from the controller rectification or erasure of personal data or restriction of processing of personal data concerning the data subject or to object to such processing; (f) the right to lodge a complaint with a supervisory authority; (g) where the personal data are not collected from the data subject, any available information as to their source; (h) the existence of automated decision-making, including profiling, referred to in Article 22(1) and (4) and, at least in those cases, meaningful information about the logic involved, as well as the significance and the envisaged consequences of such processing for the data subject.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q05 (single)

**Question.** Our game is popular with teenagers. Below what age do we need a parent's permission before signing someone up based on their consent?

**Reference.** Below 16 years, parental authorisation is needed; Member States may lower this age, but not below 13. *(expected: GDPR Article 8(1))*

**Agent answer.**

Parental permission is required for children below the age of 16, unless a Member State provides by law for a lower age that is not below 13 years.

* Processing personal data based on a child's consent in relation to information society services is lawful if the child is at least 16 years old (GDPR Article 8(1)).
* If the child is below the age of 16 years, processing is lawful only if and to the extent that consent is given or authorised by the holder of parental responsibility over the child (GDPR Article 8(1)).
* Member States may provide by law for a lower age for these purposes, provided that it is not below 13 years (GDPR Article 8(1)).

**Cited:** GDPR Article 8  
**Retrieved:** GDPR Article 4, GDPR Article 7, GDPR Article 8

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: child consent age information society services parent permission GDPR

[1] GDPR Article 8(1) (similarity 0.844)
GDPR Article 8(1) - Conditions applicable to child's consent in relation to information society services
1. Where point (a) of Article 6(1) applies, in relation to the offer of information society services directly to a child, the processing of the personal data of a child shall be lawful where the child is at least 16 years old. Where the child is below the age of 16 years, such processing shall be lawful only if and to the extent that consent is given or authorised by the holder of parental responsibility over the child. Member States may provide by law for a lower age for those purposes provided that such lower age is not below 13 years.

[2] GDPR Article 8(2)-(3) (similarity 0.786)
GDPR Article 8(2)-(3) - Conditions applicable to child's consent in relation to information society services
2. The controller shall make reasonable efforts to verify in such cases that consent is given or authorised by the holder of parental responsibility over the child, taking into consideration available technology. 3. Paragraph 1 shall not affect the general contract law of Member States such as the rules on the validity, formation or effect of a contract in relation to a child.

[3] GDPR Article 7(1)-(3) (similarity 0.718)
GDPR Article 7(1)-(3) - Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data. 2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding. 3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.

[4] GDPR Article 4, points (24) to (26) (similarity 0.705)
GDPR Article 4, points (24) to (26) - Definitions
(24) 'relevant and reasoned objection' means an objection to a draft decision as to whether there is an infringement of this Regulation, or whether envisaged action in relation to the controller or processor complies with this Regulation, which clearly demonstrates the significance of the risks posed by the draft decision as regards the fundamental rights and freedoms of data subjects and, where applicable, the free flow of personal data within the Union; (25) 'information society service' means a service as defined in point (b) of Article 1(1) of Directive (EU) 2015/1535 of the European Parliament and of the Council (); (26) 'international organisation' means an organisation and its subordinate bodies governed by public international law, or any other body which is set up by, or on the basis of, an agreement between two or more countries.

[5] GDPR Article 7(4) (similarity 0.704)
GDPR Article 7(4) - Conditions for consent
4. When assessing whether consent is freely given, utmost account shall be taken of whether, inter alia, the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q06 (single)

**Question.** A former user wants all their data deleted, but we have to keep their invoices for tax audits. Do we have to delete those too?

**Reference.** No. The right to erasure does not apply where processing is necessary to comply with a legal obligation that requires the processing. *(expected: GDPR Article 17(3)(b))*

**Agent answer.**

You do not have to delete the invoices to the extent that processing is necessary for compliance with a legal obligation to which you are subject.

* The right to erasure does not apply to the extent that processing is necessary for compliance with a legal obligation requiring processing under Union or Member State law. (GDPR Article 17(3))
* Union or Member State law may restrict the scope of rights like the right to erasure to safeguard important objectives of general public interest, including taxation matters. (GDPR Article 23(1))

**Cited:** GDPR Article 17, GDPR Article 23  
**Retrieved:** GDPR Article 17, GDPR Article 23, GDPR Article 5, GDPR Article 6

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: right to erasure exemption compliance with legal obligation invoice tax audit GDPR

[1] GDPR Article 17(1) (similarity 0.737)
GDPR Article 17(1) - Right to erasure ('right to be forgotten')
1. The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay and the controller shall have the obligation to erase personal data without undue delay where one of the following grounds applies: (a) the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed; (b) the data subject withdraws consent on which the processing is based according to point (a) of Article 6(1), or point (a) of Article 9(2), and where there is no other legal ground for the processing; (c) the data subject objects to the processing pursuant to Article 21(1) and there are no overriding legitimate grounds for the processing, or the data subject objects to the processing pursuant to Article 21(2); (d) the personal data have been unlawfully processed; (e) the personal data have to be erased for compliance with a legal obligation in Union or Member State law to which the controller is subject; (f) the personal data have been collected in relation to the offer of information society services referred to in Article 8(1).

[2] GDPR Article 17(2)-(3) (similarity 0.733)
GDPR Article 17(2)-(3) - Right to erasure ('right to be forgotten')
2. Where the controller has made the personal data public and is obliged pursuant to paragraph 1 to erase the personal data, the controller, taking account of available technology and the cost of implementation, shall take reasonable steps, including technical measures, to inform controllers which are processing the personal data that the data subject has requested the erasure by such controllers of any links to, or copy or replication of, those personal data. 3. Paragraphs 1 and 2 shall not apply to the extent that processing is necessary: (a) for exercising the right of freedom of expression and information; (b) for compliance with a legal obligation which requires processing by Union or Member State law to which the controller is subject or for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller; (c) for reasons of public interest in the area of public health in accordance with points (h) and (i) of Article 9(2) as well as Article 9(3); (d) for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) in so far as the right referred to in paragraph 1 is likely to render impossible or seriously impair the achievement of the objectives of that processing; or (e) for the establishment, exercise or defence of legal claims.

[3] GDPR Article 6(1) (similarity 0.730)
GDPR Article 6(1) - Lawfulness of processing
1. Processing shall be lawful only if and to the extent that at least one of the following applies: (a) the data subject has given consent to the processing of his or her personal data for one or more specific purposes; (b) processing is necessary for the performance of a contract to which the data subject is party or in order to take steps at the request of the data subject prior to entering into a contract; (c) processing is necessary for compliance with a legal obligation to which the controller is subject; (d) processing is necessary in order to protect the vital interests of the data subject or of another natural person; (e) processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller; (f) processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject which require protection of personal data, in particular where the data subject is a child. Point (f) of the first subparagraph shall not apply to processing carried out by public authorities in the performance of their tasks.

[4] GDPR Article 5 (similarity 0.727)
GDPR Article 5 - Principles relating to processing of personal data
1. Personal data shall be: (a) processed lawfully, fairly and in a transparent manner in relation to the data subject ('lawfulness, fairness and transparency'); (b) collected for specified, explicit and legitimate purposes and not further processed in a manner that is incompatible with those purposes; further processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes shall, in accordance with Article 89(1), not be considered to be incompatible with the initial purposes ('purpose limitation'); (c) adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed ('data minimisation'); (d) accurate and, where necessary, kept up to date; every reasonable step must be taken to ensure that personal data that are inaccurate, having regard to the purposes for which they are processed, are erased or rectified without delay ('accuracy'); (e) kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed; personal data may be stored for longer periods insofar as the personal data will be processed solely for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) subject to implementation of the appropriate technical and organisational measures required by this Regulation in order to safeguard the rights and freedoms of the data subject ('storage limitation'); (f) processed in a manner that ensures appropriate security of the personal data, including protection against unauthorised or unlawful processing and against accidental loss, destruction or damage, using appropriate technical or organisational measures ('integrity and confidentiality'). 2. The controller shall be responsible for, and be able to demonstrate compliance with, paragraph 1 ('accountability').

[5] GDPR Article 23(1) (similarity 0.708)
GDPR Article 23(1) - Restrictions
1. Union or Member State law to which the data controller or processor is subject may restrict by way of a legislative measure the scope of the obligations and rights provided for in Articles 12 to 22 and Article 34, as well as Article 5 in so far as its provisions correspond to the rights and obligations provided for in Articles 12 to 22, when such a restriction respects the essence of the fundamental rights and freedoms and is a necessary and proportionate measure in a democratic society to safeguard: (a) national security; (b) defence; (c) public security; (d) the prevention, investigation, detection or prosecution of criminal offences or the execution of criminal penalties, including the safeguarding against and the prevention of threats to public security; (e) other important objectives of general public interest of the Union or of a Member State, in particular an important economic or financial interest of the Union or of a Member State, including monetary, budgetary and taxation a matters, public health and social security; (f) the protection of judicial independence and judicial proceedings; (g) the prevention, investigation, detection and prosecution of breaches of ethics for regulated professions; (h) a monitoring, inspection or regulatory function connected, even occasionally, to the exercise of official authority in the cases referred to in points (a) to (e) and (g); (i) the protection of the data subject or the rights and freedoms of others; (j) the enforcement of civil law claims.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q07 (single)

**Question.** We use an outside cloud company to run our customer database. What does our contract with them have to cover?

**Reference.** A binding contract must set out the subject matter, duration, nature and purpose of processing, the data types and categories of people, and require the processor to act only on documented instructions, ensure confidentiality and security, use sub-processors only with authorisation, assist the controller, and delete or return data at the end. *(expected: GDPR Article 28(3))*

**Agent answer.**

Your contract with the cloud company processing your customer database must cover personal data protection instructions, security, audit rights, and cloud switching and data porting terms.

* The contract must set out the subject-matter, duration, nature, and purpose of the processing, the types of personal data and categories of data subjects, and the controller's rights and obligations. (GDPR Article 28(3))
* It must require the cloud provider to process personal data only on your documented instructions and ensure persons authorized to process the data are bound by confidentiality. (GDPR Article 28(3))
* It must require the provider to take security measures, assist you with data subjects' rights and regulatory compliance, and either delete or return all personal data at the end of the services. (GDPR Article 28(3))
* It must establish rules regarding sub-processors, audit and information-sharing obligations, and restrictions on engaging another processor without prior authorization. (GDPR Article 28(2) and (3))
* For data processing services, it must clearly set out switching and porting rights, transitional periods of up to 30 days, exit strategy support, data retrieval periods, and data erasure terms. (Data Act Article 25(1)-(2))

**Cited:** Data Act Article 25, GDPR Article 28  
**Retrieved:** Data Act Article 2, Data Act Article 24, Data Act Article 25, Data Act Article 28, Data Act Article 41, GDPR Article 28, GDPR Article 29

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: processor contract processor obligations GDPR article 28

[1] GDPR Article 28(3) (similarity 0.862)
GDPR Article 28(3) - Processor
3. Processing by a processor shall be governed by a contract or other legal act under Union or Member State law, that is binding on the processor with regard to the controller and that sets out the subject-matter and duration of the processing, the nature and purpose of the processing, the type of personal data and categories of data subjects and the obligations and rights of the controller. That contract or other legal act shall stipulate, in particular, that the processor: (a) processes the personal data only on documented instructions from the controller, including with regard to transfers of personal data to a third country or an international organisation, unless required to do so by Union or Member State law to which the processor is subject; in such a case, the processor shall inform the controller of that legal requirement before processing, unless that law prohibits such information on important grounds of public interest; (b) ensures that persons authorised to process the personal data have committed themselves to confidentiality or are under an appropriate statutory obligation of confidentiality; (c) takes all measures required pursuant to Article 32; (d) respects the conditions referred to in paragraphs 2 and 4 for engaging another processor; (e) taking into account the nature of the processing, assists the controller by appropriate technical and organisational measures, insofar as this is possible, for the fulfilment of the controller's obligation to respond to requests for exercising the data subject's rights laid down in Chapter III; (f) assists the controller in ensuring compliance with the obligations pursuant to Articles 32 to 36 taking into account the nature of processing and the information available to the processor; (g) at the choice of the controller, deletes or returns all the personal data to the controller after the end of the provision of services relating to processing, and deletes existing copies unless Union or Member State law requires storage of the personal data; (h) makes available to the controller all information necessary to demonstrate compliance with the obligations laid down in this Article and allow for and contribute to audits, including inspections, conducted by the controller or another auditor mandated by the controller. With regard to point (h) of the first subparagraph, the processor shall immediately inform the controller if, in its opinion, an instruction infringes this Regulation or other Union or Member State data protection provisions.

[2] GDPR Article 28(1)-(2) (similarity 0.836)
GDPR Article 28(1)-(2) - Processor
1. Where processing is to be carried out on behalf of a controller, the controller shall use only processors providing sufficient guarantees to implement appropriate technical and organisational measures in such a manner that processing will meet the requirements of this Regulation and ensure the protection of the rights of the data subject. 2. The processor shall not engage another processor without prior specific or general written authorisation of the controller. In the case of general written authorisation, the processor shall inform the controller of any intended changes concerning the addition or replacement of other processors, thereby giving the controller the opportunity to object to such changes.

[3] GDPR Article 28(4) (similarity 0.816)
GDPR Article 28(4) - Processor
4. Where a processor engages another processor for carrying out specific processing activities on behalf of the controller, the same data protection obligations as set out in the contract or other legal act between the controller and the processor as referred to in paragraph 3 shall be imposed on that other processor by way of a contract or other legal act under Union or Member State law, in particular providing sufficient guarantees to implement appropriate technical and organisational measures in such a manner that the processing will meet the requirements of this Regulation. Where that other processor fails to fulfil its data protection obligations, the initial processor shall remain fully liable to the controller for the performance of that other processor's obligations.

[4] GDPR Article 28(7)-(10) (similarity 0.815)
GDPR Article 28(7)-(10) - Processor
7. The Commission may lay down standard contractual clauses for the matters referred to in paragraph 3 and 4 of this Article and in accordance with the examination procedure referred to in Article 93(2). 8. A supervisory authority may adopt standard contractual clauses for the matters referred to in paragraph 3 and 4 of this Article and in accordance with the consistency mechanism referred to in Article 63. 9. The contract or the other legal act referred to in paragraphs 3 and 4 shall be in writing, including in electronic form. 10. Without prejudice to Articles 82, 83 and 84, if a processor infringes this Regulation by determining the purposes and means of processing, the processor shall be considered to be a controller in respect of that processing.

[5] GDPR Article 29 (similarity 0.801)
GDPR Article 29 - Processing under the authority of the controller or processor
The processor and any person acting under the authority of the controller or of the processor, who has access to personal data, shall not process those data except on instructions from the controller, unless required to do so by Union or Member State law.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.

5 passages for: Data Act contract between controller and processor cloud

[1] Data Act Article 25(1)-(2) (similarity 0.834)
Data Act Article 25(1)-(2) - Contractual terms concerning switching
1. The rights of the customer and the obligations of the provider of data processing services in relation to switching between providers of such services or, where applicable, to an on-premises ICT infrastructure shall be clearly set out in a written contract. The provider of data processing services shall make that contract available to the customer prior to signing the contract in a way that allows the customer to store and reproduce the contract. 2. Without prejudice to Directive (EU) 2019/770, the contract referred to in paragraph 1 of this Article shall include at least the following: (a) clauses allowing the customer, upon request, to switch to a data processing service offered by a different provider of data processing services or to port all exportable data and digital assets to an on-premises ICT infrastructure, without undue delay and in any event not after the mandatory maximum transitional period of 30 calendar days, to be initiated after the maximum notice period referred to in point (d), during which the service contract remains applicable and during which the provider of data processing services shall: (i) provide reasonable assistance to the customer and third parties authorised by the customer in the switching process; (ii) act with due care to maintain business continuity, and continue the provision of the functions or services under the contract; (iii) provide clear information concerning known risks to continuity in the provision of the functions or services on the part of the source provider of data processing services; (iv) ensure that a high level of security is maintained throughout the switching process, in particular the security of the data during their transfer and the continued security of the data during the retrieval period specified in point (g), in accordance with applicable Union or national law; (b) an obligation of the provider of data processing services to support the customer's exit strategy relevant to the contracted services, including by providing all relevant information; (c) a clause specifying that the contract shall be considered to be terminated and the customer shall be notified of the termination, in one of the following cases: (i) where applicable, upon the successful completion of the switching process; (ii) at the end of the maximum notice period referred to in paragraph (d), where the customer does not wish to switch but to erase its exportable data and digital assets upon service termination; (d) a maximum notice period for initiation of the switching process, which shall not exceed two months; (e) an exhaustive specification of all categories of data and digital assets that can be ported during the switching process, including, at a minimum, all exportable data; (f) an exhaustive specification of categories of data specific to the internal functioning of the provider's data processing service that are to be exempted from the exportable data under point (e) of this paragraph where a risk of breach of trade secrets of the provider exists, provided that such exemptions do not impede or delay the switching process provided for in Article 23; (g) a minimum period for data retrieval of at least 30 calendar days, starting after the termination of the transitional period that was agreed between the customer and the provider of data processing services, in accordance with point (a) of this paragraph and paragraph 4; (h) a clause guaranteeing full erasure of all exportable data and digital assets generated directly by the customer, or relating to the customer directly, after the expiry of the retrieval period referred to in point (g) or after the expiry of an alternative agreed period at a date later than the date of expiry of the retrieval period referred to in point (g), provided that the switching process has been completed successfully; (i) switching charges, that may be imposed by providers of data processing services in accordance with Article 29.

[2] Data Act Article 28 (similarity 0.833)
Data Act Article 28 - Contractual transparency obligations on international access and transfer
1. Providers of data processing services shall make the following information available on their websites, and keep that information up to date: (a) the jurisdiction to which the ICT infrastructure deployed for data processing of their individual services is subject; (b) a general description of the technical, organisational and contractual measures adopted by the provider of data processing services in order to prevent international governmental access to or transfer of non-personal data held in the Union where such access or transfer would create a conflict with Union law or the national law of the relevant Member State. 2. The websites referred to in paragraph 1 shall be listed in contracts for all data processing services offered by providers of data processing services.

[3] Data Act Article 41 (similarity 0.824)
Data Act Article 41 - Model contractual terms and standard contractual clauses
The Commission, before 12 September 2025, shall develop and recommend non-binding model contractual terms on data access and use, including terms on reasonable compensation and the protection of trade secrets, and non-binding standard contractual clauses for cloud computing contracts to assist parties in drafting and negotiating contracts with fair, reasonable and non-discriminatory contractual rights and obligations.

[4] Data Act Article 24 (similarity 0.822)
Data Act Article 24 - Scope of the technical obligations
The responsibilities of providers of data processing services laid down in Articles 23, 25, 29, 30 and 34 shall apply only to the services, contracts or commercial practices provided by the source provider of data processing services.

[5] Data Act Article 2, points (8) to (11) (similarity 0.820)
Data Act Article 2, points (8) to (11) - Definitions
(8) 'data processing service' means a digital service that is provided to a customer and that enables ubiquitous and on-demand network access to a shared pool of configurable, scalable and elastic computing resources of a centralised, distributed or highly distributed nature that can be rapidly provisioned and released with minimal management effort or service provider interaction; (9) 'same service type' means a set of data processing services that share the same primary objective, data processing service model and main functionalities; (10) 'data intermediation service' means data intermediation service as defined in Article 2, point (11), of Regulation (EU) 2022/868; (11) 'data subject' means data subject as referred to in Article 4, point (1), of Regulation (EU) 2016/679;

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q08 (single)

**Question.** Can we use software that reads our call-centre employees' emotions from their voice to rate their performance?

**Reference.** No. Using AI to infer emotions of people in the workplace is prohibited, except for medical or safety reasons. *(expected: AI Act Article 5(1)(f))*

**Agent answer.**

No, you generally cannot use an AI system to infer the emotions of your call-centre employees in the workplace to rate their performance, as such use is prohibited by the AI Act unless it is strictly for medical or safety reasons.

* The placement on the market, putting into service for this specific purpose, or use of AI systems to infer emotions of a natural person in the area of the workplace is prohibited. (AI Act Article 5(1)(f))
* An emotion recognition system is defined as an AI system for the purpose of identifying or inferring emotions or intentions of natural persons on the basis of their biometric data. (AI Act Article 3, point (39))
* This prohibition contains an exception only where the use of the AI system is intended to be put in place or into the market for medical or safety reasons. (AI Act Article 5(1)(f))

**Cited:** AI Act Article 3, AI Act Article 5  
**Retrieved:** AI Act Annex III, AI Act Article 3, AI Act Article 5

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: emotion recognition workplace AI Act prohibition

[1] AI Act Article 5(1) (similarity 0.798)
AI Act Article 5(1) - Prohibited AI practices
1. The following AI practices shall be prohibited: (a) the placing on the market, the putting into service or the use of an AI system that deploys subliminal techniques beyond a person's consciousness or purposefully manipulative or deceptive techniques, with the objective, or the effect of materially distorting the behaviour of a person or a group of persons by appreciably impairing their ability to make an informed decision, thereby causing them to take a decision that they would not have otherwise taken in a manner that causes or is reasonably likely to cause that person, another person or group of persons significant harm; (b) the placing on the market, the putting into service or the use of an AI system that exploits any of the vulnerabilities of a natural person or a specific group of persons due to their age, disability or a specific social or economic situation, with the objective, or the effect, of materially distorting the behaviour of that person or a person belonging to that group in a manner that causes or is reasonably likely to cause that person or another person significant harm; (c) the placing on the market, the putting into service or the use of AI systems for the evaluation or classification of natural persons or groups of persons over a certain period of time based on their social behaviour or known, inferred or predicted personal or personality characteristics, with the social score leading to either or both of the following: (i) detrimental or unfavourable treatment of certain natural persons or groups of persons in social contexts that are unrelated to the contexts in which the data was originally generated or collected; (ii) detrimental or unfavourable treatment of certain natural persons or groups of persons that is unjustified or disproportionate to their social behaviour or its gravity; (d) the placing on the market, the putting into service for this specific purpose, or the use of an AI system for making risk assessments of natural persons in order to assess or predict the risk of a natural person committing a criminal offence, based solely on the profiling of a natural person or on assessing their personality traits and characteristics; this prohibition shall not apply to AI systems used to support the human assessment of the involvement of a person in a criminal activity, which is already based on objective and verifiable facts directly linked to a criminal activity; (e) the placing on the market, the putting into service for this specific purpose, or the use of AI systems that create or expand facial recognition databases through the untargeted scraping of facial images from the internet or CCTV footage; (f) the placing on the market, the putting into service for this specific purpose, or the use of AI systems to infer emotions of a natural person in the areas of workplace and education institutions, except where the use of the AI system is intended to be put in place or into the market for medical or safety reasons; (g) the placing on the market, the putting into service for this specific purpose, or the use of biometric categorisation systems that categorise individually natural persons based on their biometric data to deduce or infer their race, political opinions, trade union membership, religious or philosophical beliefs, sex life or sexual orientation; this prohibition does not cover any labelling or filtering of lawfully acquired biometric datasets, such as images, based on biometric data or categorizing of biometric data in the area of law enforcement; (h) the use of 'real-time' remote biometric identification systems in publicly accessible spaces for the purposes of law enforcement, unless and in so far as such use is strictly necessary for one of the following objectives: (i) the targeted search for specific victims of abduction, trafficking in human beings or sexual exploitation of human beings, as well as the search for missing persons; (ii) the prevention of a specific, substantial and imminent threat to the life or physical safety of natural persons or a genuine and present or genuine and foreseeable threat of a terrorist attack; (iii) the localisation or identification of a person suspected of having committed a criminal offence, for the purpose of conducting a criminal investigation or prosecution or executing a criminal penalty for offences referred to in Annex II and punishable in the Member State concerned by a custodial sentence or a detention order for a maximum period of at least four years. Point (h) of the first subparagraph is without prejudice to Article 9 of Regulation (EU) 2016/679 for the processing of biometric data for purposes other than law enforcement.

[2] AI Act Article 3, points (38) to (41) (similarity 0.756)
AI Act Article 3, points (38) to (41) - Definitions
(38) 'sensitive operational data' means operational data related to activities of prevention, detection, investigation or prosecution of criminal offences, the disclosure of which could jeopardise the integrity of criminal proceedings; (39) 'emotion recognition system' means an AI system for the purpose of identifying or inferring emotions or intentions of natural persons on the basis of their biometric data; (40) 'biometric categorisation system' means an AI system for the purpose of assigning natural persons to specific categories on the basis of their biometric data, unless it is ancillary to another commercial service and strictly necessary for objective technical reasons; (41) 'remote biometric identification system' means an AI system for the purpose of identifying natural persons, without their active involvement, typically at a distance through the comparison of a person's biometric data with the biometric data contained in a reference database;

[3] AI Act Article 5(3) (similarity 0.755)
AI Act Article 5(3) - Prohibited AI practices
3. For the purposes of paragraph 1, first subparagraph, point (h) and paragraph 2, each use for the purposes of law enforcement of a 'real-time' remote biometric identification system in publicly accessible spaces shall be subject to a prior authorisation granted by a judicial authority or an independent administrative authority whose decision is binding of the Member State in which the use is to take place, issued upon a reasoned request and in accordance with the detailed rules of national law referred to in paragraph 5. However, in a duly justified situation of urgency, the use of such system may be commenced without an authorisation provided that such authorisation is requested without undue delay, at the latest within 24 hours. If such authorisation is rejected, the use shall be stopped with immediate effect and all the data, as well as the results and outputs of that use shall be immediately discarded and deleted. The competent judicial authority or an independent administrative authority whose decision is binding shall grant the authorisation only where it is satisfied, on the basis of objective evidence or clear indications presented to it, that the use of the 'real-time' remote biometric identification system concerned is necessary for, and proportionate to, achieving one of the objectives specified in paragraph 1, first subparagraph, point (h), as identified in the request and, in particular, remains limited to what is strictly necessary concerning the period of time as well as the geographic and personal scope. In deciding on the request, that authority shall take into account the elements referred to in paragraph 2. No decision that produces an adverse legal effect on a person may be taken based solely on the output of the 'real-time' remote biometric identification system.

[4] AI Act Article 5(2) (similarity 0.755)
AI Act Article 5(2) - Prohibited AI practices
2. The use of 'real-time' remote biometric identification systems in publicly accessible spaces for the purposes of law enforcement for any of the objectives referred to in paragraph 1, first subparagraph, point (h), shall be deployed for the purposes set out in that point only to confirm the identity of the specifically targeted individual, and it shall take into account the following elements: (a) the nature of the situation giving rise to the possible use, in particular the seriousness, probability and scale of the harm that would be caused if the system were not used; (b) the consequences of the use of the system for the rights and freedoms of all persons concerned, in particular the seriousness, probability and scale of those consequences. In addition, the use of 'real-time' remote biometric identification systems in publicly accessible spaces for the purposes of law enforcement for any of the objectives referred to in paragraph 1, first subparagraph, point (h), of this Article shall comply with necessary and proportionate safeguards and conditions in relation to the use in accordance with the national law authorising the use thereof, in particular as regards the temporal, geographic and personal limitations. The use of the 'real-time' remote biometric identification system in publicly accessible spaces shall be authorised only if the law enforcement authority has completed a fundamental rights impact assessment as provided for in Article 27 and has registered the system in the EU database according to Article 49. However, in duly justified cases of urgency, the use of such systems may be commenced without the registration in the EU database, provided that such registration is completed without undue delay.

[5] AI Act Annex III, points intro to (1) (similarity 0.754)
AI Act Annex III, points intro to (1) - High-risk AI systems referred to in Article 6(2)
High-risk AI systems pursuant to Article 6(2) are the AI systems listed in any of the following areas: 1. Biometrics, in so far as their use is permitted under relevant Union or national law: (a) remote biometric identification systems. This shall not include AI systems intended to be used for biometric verification the sole purpose of which is to confirm that a specific natural person is the person he or she claims to be; (b) AI systems intended to be used for biometric categorisation, according to sensitive or protected attributes or characteristics based on the inference of those attributes or characteristics; (c) AI systems intended to be used for emotion recognition.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q09 (single)

**Question.** What is the maximum penalty if we use an AI practice that the law bans outright?

**Reference.** Administrative fines of up to EUR 35 million or, for an undertaking, up to 7% of total worldwide annual turnover, whichever is higher. *(expected: AI Act Article 99(3))*

**Agent answer.**

Non-compliance with the prohibition of the AI practices referred to in Article 5 is subject to administrative fines of up to EUR 35 000 000 or, if the offender is an undertaking, up to 7 % of its total worldwide annual turnover for the preceding financial year, whichever is higher.

* For SMEs, including start-ups, each fine shall be up to the percentages or amount referred to in the general penalty provisions, whichever is lower.
* AI Act Article 99(3)
* AI Act Article 99(6)

**Cited:** AI Act Article 99  
**Retrieved:** AI Act Article 100, AI Act Article 5, AI Act Article 99

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: prohibited AI practices penalties fines AI Act

[1] AI Act Article 99(3)-(4) (similarity 0.814)
AI Act Article 99(3)-(4) - Penalties
3. Non-compliance with the prohibition of the AI practices referred to in Article 5 shall be subject to administrative fines of up to EUR 35 000 000 or, if the offender is an undertaking, up to 7 % of its total worldwide annual turnover for the preceding financial year, whichever is higher. 4. Non-compliance with any of the following provisions related to operators or notified bodies, other than those laid down in Articles 5, shall be subject to administrative fines of up to EUR 15 000 000 or, if the offender is an undertaking, up to 3 % of its total worldwide annual turnover for the preceding financial year, whichever is higher: (a) obligations of providers pursuant to Article 16; (b) obligations of authorised representatives pursuant to Article 22; (c) obligations of importers pursuant to Article 23; (d) obligations of distributors pursuant to Article 24; (e) obligations of deployers pursuant to Article 26; (f) requirements and obligations of notified bodies pursuant to Article 31, Article 33(1), (3) and (4) or Article 34; (g) transparency obligations for providers and deployers pursuant to Article 50.

[2] AI Act Article 5(1) (similarity 0.809)
AI Act Article 5(1) - Prohibited AI practices
1. The following AI practices shall be prohibited: (a) the placing on the market, the putting into service or the use of an AI system that deploys subliminal techniques beyond a person's consciousness or purposefully manipulative or deceptive techniques, with the objective, or the effect of materially distorting the behaviour of a person or a group of persons by appreciably impairing their ability to make an informed decision, thereby causing them to take a decision that they would not have otherwise taken in a manner that causes or is reasonably likely to cause that person, another person or group of persons significant harm; (b) the placing on the market, the putting into service or the use of an AI system that exploits any of the vulnerabilities of a natural person or a specific group of persons due to their age, disability or a specific social or economic situation, with the objective, or the effect, of materially distorting the behaviour of that person or a person belonging to that group in a manner that causes or is reasonably likely to cause that person or another person significant harm; (c) the placing on the market, the putting into service or the use of AI systems for the evaluation or classification of natural persons or groups of persons over a certain period of time based on their social behaviour or known, inferred or predicted personal or personality characteristics, with the social score leading to either or both of the following: (i) detrimental or unfavourable treatment of certain natural persons or groups of persons in social contexts that are unrelated to the contexts in which the data was originally generated or collected; (ii) detrimental or unfavourable treatment of certain natural persons or groups of persons that is unjustified or disproportionate to their social behaviour or its gravity; (d) the placing on the market, the putting into service for this specific purpose, or the use of an AI system for making risk assessments of natural persons in order to assess or predict the risk of a natural person committing a criminal offence, based solely on the profiling of a natural person or on assessing their personality traits and characteristics; this prohibition shall not apply to AI systems used to support the human assessment of the involvement of a person in a criminal activity, which is already based on objective and verifiable facts directly linked to a criminal activity; (e) the placing on the market, the putting into service for this specific purpose, or the use of AI systems that create or expand facial recognition databases through the untargeted scraping of facial images from the internet or CCTV footage; (f) the placing on the market, the putting into service for this specific purpose, or the use of AI systems to infer emotions of a natural person in the areas of workplace and education institutions, except where the use of the AI system is intended to be put in place or into the market for medical or safety reasons; (g) the placing on the market, the putting into service for this specific purpose, or the use of biometric categorisation systems that categorise individually natural persons based on their biometric data to deduce or infer their race, political opinions, trade union membership, religious or philosophical beliefs, sex life or sexual orientation; this prohibition does not cover any labelling or filtering of lawfully acquired biometric datasets, such as images, based on biometric data or categorizing of biometric data in the area of law enforcement; (h) the use of 'real-time' remote biometric identification systems in publicly accessible spaces for the purposes of law enforcement, unless and in so far as such use is strictly necessary for one of the following objectives: (i) the targeted search for specific victims of abduction, trafficking in human beings or sexual exploitation of human beings, as well as the search for missing persons; (ii) the prevention of a specific, substantial and imminent threat to the life or physical safety of natural persons or a genuine and present or genuine and foreseeable threat of a terrorist attack; (iii) the localisation or identification of a person suspected of having committed a criminal offence, for the purpose of conducting a criminal investigation or prosecution or executing a criminal penalty for offences referred to in Annex II and punishable in the Member State concerned by a custodial sentence or a detention order for a maximum period of at least four years. Point (h) of the first subparagraph is without prejudice to Article 9 of Regulation (EU) 2016/679 for the processing of biometric data for purposes other than law enforcement.

[3] AI Act Article 100(2)-(4) (similarity 0.790)
AI Act Article 100(2)-(4) - Administrative fines on Union institutions, bodies, offices and agencies
2. Non-compliance with the prohibition of the AI practices referred to in Article 5 shall be subject to administrative fines of up to EUR 1 500 000. 3. The non-compliance of the AI system with any requirements or obligations under this Regulation, other than those laid down in Article 5, shall be subject to administrative fines of up to EUR 750 000. 4. Before taking decisions pursuant to this Article, the European Data Protection Supervisor shall give the Union institution, body, office or agency which is the subject of the proceedings conducted by the European Data Protection Supervisor the opportunity of being heard on the matter regarding the possible infringement. The European Data Protection Supervisor shall base his or her decisions only on elements and circumstances on which the parties concerned have been able to comment. Complainants, if any, shall be associated closely with the proceedings.

[4] AI Act Article 99(5)-(7) (similarity 0.784)
AI Act Article 99(5)-(7) - Penalties
5. The supply of incorrect, incomplete or misleading information to notified bodies or national competent authorities in reply to a request shall be subject to administrative fines of up to EUR 7 500 000 or, if the offender is an undertaking, up to 1 % of its total worldwide annual turnover for the preceding financial year, whichever is higher. 6. In the case of SMEs, including start-ups, each fine referred to in this Article shall be up to the percentages or amount referred to in paragraphs 3, 4 and 5, whichever thereof is lower. 7. When deciding whether to impose an administrative fine and when deciding on the amount of the administrative fine in each individual case, all relevant circumstances of the specific situation shall be taken into account and, as appropriate, regard shall be given to the following: (a) the nature, gravity and duration of the infringement and of its consequences, taking into account the purpose of the AI system, as well as, where appropriate, the number of affected persons and the level of damage suffered by them; (b) whether administrative fines have already been applied by other market surveillance authorities to the same operator for the same infringement; (c) whether administrative fines have already been applied by other authorities to the same operator for infringements of other Union or national law, when such infringements result from the same activity or omission constituting a relevant infringement of this Regulation; (d) the size, the annual turnover and market share of the operator committing the infringement; (e) any other aggravating or mitigating factor applicable to the circumstances of the case, such as financial benefits gained, or losses avoided, directly or indirectly, from the infringement; (f) the degree of cooperation with the national competent authorities, in order to remedy the infringement and mitigate the possible adverse effects of the infringement; (g) the degree of responsibility of the operator taking into account the technical and organisational measures implemented by it; (h) the manner in which the infringement became known to the national competent authorities, in particular whether, and if so to what extent, the operator notified the infringement; (i) the intentional or negligent character of the infringement; (j) any action taken by the operator to mitigate the harm suffered by the affected persons.

[5] AI Act Article 99(1)-(2) (similarity 0.774)
AI Act Article 99(1)-(2) - Penalties
1. In accordance with the terms and conditions laid down in this Regulation, Member States shall lay down the rules on penalties and other enforcement measures, which may also include warnings and non-monetary measures, applicable to infringements of this Regulation by operators, and shall take all measures necessary to ensure that they are properly and effectively implemented, thereby taking into account the guidelines issued by the Commission pursuant to Article 96. The penalties provided for shall be effective, proportionate and dissuasive. They shall take into account the interests of SMEs, including start-ups, and their economic viability. 2. The Member States shall, without delay and at the latest by the date of entry into application, notify the Commission of the rules on penalties and of other enforcement measures referred to in paragraph 1, and shall notify it, without delay, of any subsequent amendment to them.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q10 (single)

**Question.** Our website chatbot answers customer questions. Do we have to tell people they are talking to a machine?

**Reference.** Yes. Systems meant to interact directly with people must be designed so that people are informed they are interacting with an AI system, unless that is obvious to a reasonably well-informed person. *(expected: AI Act Article 50(1))*

**Agent answer.**

Yes, you must inform users that they are interacting with an AI system, unless it is already obvious to a reasonably well-informed, observant, and circumspect person based on the circumstances and context.

* AI systems intended to interact directly with natural persons must be designed and developed to inform users that they are interacting with an AI system, subject to exceptions for law enforcement. AI Act Article 50(1)
* This transparency information must be provided to the individuals concerned in a clear and distinguishable manner no later than the time of the first interaction or exposure. AI Act Article 50(5)
* The provided information must conform to applicable accessibility requirements. AI Act Article 50(5)

**Cited:** AI Act Article 50  
**Retrieved:** AI Act Article 13, AI Act Article 26, AI Act Article 50

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: chatbot inform natural person AI Act transparency

[1] AI Act Article 50(1) (similarity 0.844)
AI Act Article 50(1) - Transparency obligations for providers and deployers of certain AI systems
1. Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system, unless this is obvious from the point of view of a natural person who is reasonably well-informed, observant and circumspect, taking into account the circumstances and the context of use. This obligation shall not apply to AI systems authorised by law to detect, prevent, investigate or prosecute criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, unless those systems are available for the public to report a criminal offence.

[2] AI Act Article 50(3)-(4) (similarity 0.787)
AI Act Article 50(3)-(4) - Transparency obligations for providers and deployers of certain AI systems
3. Deployers of an emotion recognition system or a biometric categorisation system shall inform the natural persons exposed thereto of the operation of the system, and shall process the personal data in accordance with Regulations (EU) 2016/679 and (EU) 2018/1725 and Directive (EU) 2016/680, as applicable. This obligation shall not apply to AI systems used for biometric categorisation and emotion recognition, which are permitted by law to detect, prevent or investigate criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, and in accordance with Union law. 4. Deployers of an AI system that generates or manipulates image, audio or video content constituting a deep fake, shall disclose that the content has been artificially generated or manipulated. This obligation shall not apply where the use is authorised by law to detect, prevent, investigate or prosecute criminal offence. Where the content forms part of an evidently artistic, creative, satirical, fictional or analogous work or programme, the transparency obligations set out in this paragraph are limited to disclosure of the existence of such generated or manipulated content in an appropriate manner that does not hamper the display or enjoyment of the work. Deployers of an AI system that generates or manipulates text which is published with the purpose of informing the public on matters of public interest shall disclose that the text has been artificially generated or manipulated. This obligation shall not apply where the use is authorised by law to detect, prevent, investigate or prosecute criminal offences or where the AI-generated content has undergone a process of human review or editorial control and where a natural or legal person holds editorial responsibility for the publication of the content.

[3] AI Act Article 13 (similarity 0.780)
AI Act Article 13 - Transparency and provision of information to deployers
1. High-risk AI systems shall be designed and developed in such a way as to ensure that their operation is sufficiently transparent to enable deployers to interpret a system's output and use it appropriately. An appropriate type and degree of transparency shall be ensured with a view to achieving compliance with the relevant obligations of the provider and deployer set out in Section 3. 2. High-risk AI systems shall be accompanied by instructions for use in an appropriate digital format or otherwise that include concise, complete, correct and clear information that is relevant, accessible and comprehensible to deployers. 3. The instructions for use shall contain at least the following information: (a) the identity and the contact details of the provider and, where applicable, of its authorised representative; (b) the characteristics, capabilities and limitations of performance of the high-risk AI system, including: (i) its intended purpose; (ii) the level of accuracy, including its metrics, robustness and cybersecurity referred to in Article 15 against which the high-risk AI system has been tested and validated and which can be expected, and any known and foreseeable circumstances that may have an impact on that expected level of accuracy, robustness and cybersecurity; (iii) any known or foreseeable circumstance, related to the use of the high-risk AI system in accordance with its intended purpose or under conditions of reasonably foreseeable misuse, which may lead to risks to the health and safety or fundamental rights referred to in Article 9(2); (iv) where applicable, the technical capabilities and characteristics of the high-risk AI system to provide information that is relevant to explain its output; (v) when appropriate, its performance regarding specific persons or groups of persons on which the system is intended to be used; (vi) when appropriate, specifications for the input data, or any other relevant information in terms of the training, validation and testing data sets used, taking into account the intended purpose of the high-risk AI system; (vii) where applicable, information to enable deployers to interpret the output of the high-risk AI system and use it appropriately; (c) the changes to the high-risk AI system and its performance which have been pre-determined by the provider at the moment of the initial conformity assessment, if any; (d) the human oversight measures referred to in Article 14, including the technical measures put in place to facilitate the interpretation of the outputs of the high-risk AI systems by the deployers; (e) the computational and hardware resources needed, the expected lifetime of the high-risk AI system and any necessary maintenance and care measures, including their frequency, to ensure the proper functioning of that AI system, including as regards software updates; (f) where relevant, a description of the mechanisms included within the high-risk AI system that allows deployers to properly collect, store and interpret the logs in accordance with Article 12.

[4] AI Act Article 26(11)-(12) (similarity 0.771)
AI Act Article 26(11)-(12) - Obligations of deployers of high-risk AI systems
11. Without prejudice to Article 50 of this Regulation, deployers of high-risk AI systems referred to in Annex III that make decisions or assist in making decisions related to natural persons shall inform the natural persons that they are subject to the use of the high-risk AI system. For high-risk AI systems used for law enforcement purposes Article 13 of Directive (EU) 2016/680 shall apply. 12. Deployers shall cooperate with the relevant competent authorities in any action those authorities take in relation to the high-risk AI system in order to implement this Regulation.

[5] AI Act Article 50(5)-(7) (similarity 0.768)
AI Act Article 50(5)-(7) - Transparency obligations for providers and deployers of certain AI systems
5. The information referred to in paragraphs 1 to 4 shall be provided to the natural persons concerned in a clear and distinguishable manner at the latest at the time of the first interaction or exposure. The information shall conform to the applicable accessibility requirements. 6. Paragraphs 1 to 4 shall not affect the requirements and obligations set out in Chapter III, and shall be without prejudice to other transparency obligations laid down in Union or national law for deployers of AI systems. 7. The AI Office shall encourage and facilitate the drawing up of codes of practice at Union level to facilitate the effective implementation of the obligations regarding the detection and labelling of artificially generated or manipulated content. The Commission may adopt implementing acts to approve those codes of practice in accordance with the procedure laid down in Article 56 (6). If it deems the code is not adequate, the Commission may adopt an implementing act specifying common rules for the implementation of those obligations in accordance with the examination procedure laid down in Article 98(2).

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q11 (single)

**Question.** We generate realistic AI videos of people for our ads. Do we have to label them?

**Reference.** Yes. Deployers of AI that generates or manipulates deep fake content must disclose that the content is artificially generated or manipulated, with a lighter duty for evidently artistic, creative or satirical works. *(expected: AI Act Article 50(4))*

**Agent answer.**

Yes, if you deploy an AI system to generate or manipulate video content constituting a deepfake for your ads, you must disclose that the content has been artificially generated or manipulated.

* Deployers of an AI system that generates or manipulates image, audio, or video content constituting a deepfake must disclose that the content has been artificially generated or manipulated. AI Act Article 50(4)
* Providers of AI systems that generate synthetic image or video content must also ensure that the outputs are marked in a machine-readable format and detectable as artificially generated or manipulated. AI Act Article 50(2)
* The required information must be provided to the natural persons concerned in a clear and distinguishable manner at the latest at the time of the first interaction or exposure. AI Act Article 50(5)

**Cited:** AI Act Article 50  
**Retrieved:** AI Act Annex XII, AI Act Article 50

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: AI generated video labelling transparency requirements synthetic media deepfake

[1] AI Act Article 50(2) (similarity 0.808)
AI Act Article 50(2) - Transparency obligations for providers and deployers of certain AI systems
2. Providers of AI systems, including general-purpose AI systems, generating synthetic audio, image, video or text content, shall ensure that the outputs of the AI system are marked in a machine-readable format and detectable as artificially generated or manipulated. Providers shall ensure their technical solutions are effective, interoperable, robust and reliable as far as this is technically feasible, taking into account the specificities and limitations of various types of content, the costs of implementation and the generally acknowledged state of the art, as may be reflected in relevant technical standards. This obligation shall not apply to the extent the AI systems perform an assistive function for standard editing or do not substantially alter the input data provided by the deployer or the semantics thereof, or where authorised by law to detect, prevent, investigate or prosecute criminal offences.

[2] AI Act Article 50(3)-(4) (similarity 0.793)
AI Act Article 50(3)-(4) - Transparency obligations for providers and deployers of certain AI systems
3. Deployers of an emotion recognition system or a biometric categorisation system shall inform the natural persons exposed thereto of the operation of the system, and shall process the personal data in accordance with Regulations (EU) 2016/679 and (EU) 2018/1725 and Directive (EU) 2016/680, as applicable. This obligation shall not apply to AI systems used for biometric categorisation and emotion recognition, which are permitted by law to detect, prevent or investigate criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, and in accordance with Union law. 4. Deployers of an AI system that generates or manipulates image, audio or video content constituting a deep fake, shall disclose that the content has been artificially generated or manipulated. This obligation shall not apply where the use is authorised by law to detect, prevent, investigate or prosecute criminal offence. Where the content forms part of an evidently artistic, creative, satirical, fictional or analogous work or programme, the transparency obligations set out in this paragraph are limited to disclosure of the existence of such generated or manipulated content in an appropriate manner that does not hamper the display or enjoyment of the work. Deployers of an AI system that generates or manipulates text which is published with the purpose of informing the public on matters of public interest shall disclose that the text has been artificially generated or manipulated. This obligation shall not apply where the use is authorised by law to detect, prevent, investigate or prosecute criminal offences or where the AI-generated content has undergone a process of human review or editorial control and where a natural or legal person holds editorial responsibility for the publication of the content.

[3] AI Act Article 50(5)-(7) (similarity 0.767)
AI Act Article 50(5)-(7) - Transparency obligations for providers and deployers of certain AI systems
5. The information referred to in paragraphs 1 to 4 shall be provided to the natural persons concerned in a clear and distinguishable manner at the latest at the time of the first interaction or exposure. The information shall conform to the applicable accessibility requirements. 6. Paragraphs 1 to 4 shall not affect the requirements and obligations set out in Chapter III, and shall be without prejudice to other transparency obligations laid down in Union or national law for deployers of AI systems. 7. The AI Office shall encourage and facilitate the drawing up of codes of practice at Union level to facilitate the effective implementation of the obligations regarding the detection and labelling of artificially generated or manipulated content. The Commission may adopt implementing acts to approve those codes of practice in accordance with the procedure laid down in Article 56 (6). If it deems the code is not adequate, the Commission may adopt an implementing act specifying common rules for the implementation of those obligations in accordance with the examination procedure laid down in Article 98(2).

[4] AI Act Article 50(1) (similarity 0.742)
AI Act Article 50(1) - Transparency obligations for providers and deployers of certain AI systems
1. Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system, unless this is obvious from the point of view of a natural person who is reasonably well-informed, observant and circumspect, taking into account the circumstances and the context of use. This obligation shall not apply to AI systems authorised by law to detect, prevent, investigate or prosecute criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, unless those systems are available for the public to report a criminal offence.

[5] AI Act Annex XII (similarity 0.730)
AI Act Annex XII - Transparency information referred to in Article 53(1), point (b) — technical documentation for providers of general-purpose AI models to downstream providers that integrate the model into their AI system
The information referred to in Article 53(1), point (b) shall contain at least the following: 1. A general description of the general-purpose AI model including: (a) the tasks that the model is intended to perform and the type and nature of AI systems into which it can be integrated; (b) the acceptable use policies applicable; (c) the date of release and methods of distribution; (d) how the model interacts, or can be used to interact, with hardware or software that is not part of the model itself, where applicable; (e) the versions of relevant software related to the use of the general-purpose AI model, where applicable; (f) the architecture and number of parameters; (g) the modality (e.g. text, image) and format of inputs and outputs; (h) the licence for the model. 2. A description of the elements of the model and of the process for its development, including: (a) the technical means (e.g. instructions for use, infrastructure, tools) required for the general-purpose AI model to be integrated into AI systems; (b) the modality (e.g. text, image, etc.) and format of the inputs and outputs and their maximum size (e.g. context window length, etc.); (c) information on the data used for training, testing and validation, where applicable, including the type and provenance of data and curation methodologies.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q12 (single)

**Question.** Even if our AI tools are low risk, do we have to train our staff on AI?

**Reference.** Yes. Providers and deployers must take measures to ensure, to their best extent, a sufficient level of AI literacy of their staff and others operating AI systems on their behalf. *(expected: AI Act Article 4)*

**Agent answer.**

Yes, providers and deployers of AI systems must take measures to ensure a sufficient level of AI literacy of their staff, regardless of the risk level of the AI tools.

* Providers and deployers of AI systems shall take measures to ensure, to their best extent, a sufficient level of AI literacy of their staff and other persons dealing with the operation and use of AI systems on their behalf (AI Act Article 4).
* This requirement takes into account the staff's technical knowledge, experience, education, and training, as well as the context in which the AI systems are to be used and the persons on whom they are to be used (AI Act Article 4).
* AI literacy means skills, knowledge, and understanding that allow providers, deployers, and affected persons to make an informed deployment of AI systems and gain awareness about the opportunities, risks, and possible harm of AI (AI Act Article 3, point (56)).

**Cited:** AI Act Article 3, AI Act Article 4  
**Retrieved:** AI Act Annex III, AI Act Article 10, AI Act Article 15, AI Act Article 3, AI Act Article 4

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: AI literacy staff training AI Act low risk

[1] AI Act Article 4 (similarity 0.833)
AI Act Article 4 - AI literacy
Providers and deployers of AI systems shall take measures to ensure, to their best extent, a sufficient level of AI literacy of their staff and other persons dealing with the operation and use of AI systems on their behalf, taking into account their technical knowledge, experience, education and training and the context the AI systems are to be used in, and considering the persons or groups of persons on whom the AI systems are to be used.

[2] AI Act Article 3, points (56) to (57) (similarity 0.750)
AI Act Article 3, points (56) to (57) - Definitions
(56) 'AI literacy' means skills, knowledge and understanding that allow providers, deployers and affected persons, taking into account their respective rights and obligations in the context of this Regulation, to make an informed deployment of AI systems, as well as to gain awareness about the opportunities and risks of AI and possible harm it can cause; (57) 'testing in real-world conditions' means the temporary testing of an AI system for its intended purpose in real-world conditions outside a laboratory or otherwise simulated environment, with a view to gathering reliable and robust data and to assessing and verifying the conformity of the AI system with the requirements of this Regulation and it does not qualify as placing the AI system on the market or putting it into service within the meaning of this Regulation, provided that all the conditions laid down in Article 57 or 60 are fulfilled;

[3] AI Act Article 10(1)-(2) (similarity 0.745)
AI Act Article 10(1)-(2) - Data and data governance
1. High-risk AI systems which make use of techniques involving the training of AI models with data shall be developed on the basis of training, validation and testing data sets that meet the quality criteria referred to in paragraphs 2 to 5 whenever such data sets are used. 2. Training, validation and testing data sets shall be subject to data governance and management practices appropriate for the intended purpose of the high-risk AI system. Those practices shall concern in particular: (a) the relevant design choices; (b) data collection processes and the origin of data, and in the case of personal data, the original purpose of the data collection; (c) relevant data-preparation processing operations, such as annotation, labelling, cleaning, updating, enrichment and aggregation; (d) the formulation of assumptions, in particular with respect to the information that the data are supposed to measure and represent; (e) an assessment of the availability, quantity and suitability of the data sets that are needed; (f) examination in view of possible biases that are likely to affect the health and safety of persons, have a negative impact on fundamental rights or lead to discrimination prohibited under Union law, especially where data outputs influence inputs for future operations; (g) appropriate measures to detect, prevent and mitigate possible biases identified according to point (f); (h) the identification of relevant data gaps or shortcomings that prevent compliance with this Regulation, and how those gaps and shortcomings can be addressed.

[4] AI Act Article 15(5) (similarity 0.737)
AI Act Article 15(5) - Accuracy, robustness and cybersecurity
5. High-risk AI systems shall be resilient against attempts by unauthorised third parties to alter their use, outputs or performance by exploiting system vulnerabilities. The technical solutions aiming to ensure the cybersecurity of high-risk AI systems shall be appropriate to the relevant circumstances and the risks. The technical solutions to address AI specific vulnerabilities shall include, where appropriate, measures to prevent, detect, respond to, resolve and control for attacks trying to manipulate the training data set (data poisoning), or pre-trained components used in training (model poisoning), inputs designed to cause the AI model to make a mistake (adversarial examples or model evasion), confidentiality attacks or model flaws.

[5] AI Act Annex III, points (2) to (3) (similarity 0.736)
AI Act Annex III, points (2) to (3) - High-risk AI systems referred to in Article 6(2)
2. Critical infrastructure: AI systems intended to be used as safety components in the management and operation of critical digital infrastructure, road traffic, or in the supply of water, gas, heating or electricity. 3. Education and vocational training: (a) AI systems intended to be used to determine access or admission or to assign natural persons to educational and vocational training institutions at all levels; (b) AI systems intended to be used to evaluate learning outcomes, including when those outcomes are used to steer the learning process of natural persons in educational and vocational training institutions at all levels; (c) AI systems intended to be used for the purpose of assessing the appropriate level of education that an individual will receive or will be able to access, in the context of or within educational and vocational training institutions at all levels; (d) AI systems intended to be used for monitoring and detecting prohibited behaviour of students during tests in the context of or within educational and vocational training institutions at all levels.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q13 (single)

**Question.** How much computing power used to train a general-purpose AI model makes it presumed to pose systemic risk?

**Reference.** A model is presumed to have high-impact capabilities when the cumulative compute used for its training is greater than 10^25 floating-point operations. *(expected: AI Act Article 51(2))*

**Agent answer.**

A general-purpose AI model is presumed to pose systemic risk when the cumulative amount of computation used for its training, measured in floating point operations, is greater than $10^{25}$.

* A general-purpose AI model is classified as having systemic risk if it meets certain conditions, including having high-impact capabilities (AI Act Article 51(1)).
* A model is presumed to have these high-impact capabilities when the cumulative amount of training computation measured in floating point operations exceeds $10^{25}$ (AI Act Article 51(2)).

**Cited:** AI Act Article 51  
**Retrieved:** AI Act Annex XI, AI Act Annex XIII, AI Act Article 3, AI Act Article 51, AI Act Article 55

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: computing power systemic risk general purpose AI model training float cumulative FLOPs

[1] AI Act Article 51(1)-(2) (similarity 0.795)
AI Act Article 51(1)-(2) - Classification of general-purpose AI models as general-purpose AI models with systemic risk
1. A general-purpose AI model shall be classified as a general-purpose AI model with systemic risk if it meets any of the following conditions: (a) it has high impact capabilities evaluated on the basis of appropriate technical tools and methodologies, including indicators and benchmarks; (b) based on a decision of the Commission, ex officio or following a qualified alert from the scientific panel, it has capabilities or an impact equivalent to those set out in point (a) having regard to the criteria set out in Annex XIII. 2. A general-purpose AI model shall be presumed to have high impact capabilities pursuant to paragraph 1, point (a), when the cumulative amount of computation used for its training measured in floating point operations is greater than 10^25.

[2] AI Act Annex XIII (similarity 0.761)
AI Act Annex XIII - Criteria for the designation of general-purpose AI models with systemic risk referred to in Article 51
For the purpose of determining that a general-purpose AI model has capabilities or an impact equivalent to those set out in Article 51(1), point (a), the Commission shall take into account the following criteria: (a) the number of parameters of the model; (b) the quality or size of the data set, for example measured through tokens; (c) the amount of computation used for training the model, measured in floating point operations or indicated by a combination of other variables such as estimated cost of training, estimated time required for the training, or estimated energy consumption for the training; (d) the input and output modalities of the model, such as text to text (large language models), text to image, multi-modality, and the state of the art thresholds for determining high-impact capabilities for each modality, and the specific type of inputs and outputs (e.g. biological sequences); (e) the benchmarks and evaluations of capabilities of the model, including considering the number of tasks without additional training, adaptability to learn new, distinct tasks, its level of autonomy and scalability, the tools it has access to; (f) whether it has a high impact on the internal market due to its reach, which shall be presumed when it has been made available to at least 10 000 registered business users established in the Union; (g) the number of registered end-users.

[3] AI Act Article 3, points (64) to (66) (similarity 0.752)
AI Act Article 3, points (64) to (66) - Definitions
(64) 'high-impact capabilities' means capabilities that match or exceed the capabilities recorded in the most advanced general-purpose AI models; (65) 'systemic risk' means a risk that is specific to the high-impact capabilities of general-purpose AI models, having a significant impact on the Union market due to their reach, or due to actual or reasonably foreseeable negative effects on public health, safety, public security, fundamental rights, or the society as a whole, that can be propagated at scale across the value chain; (66) 'general-purpose AI system' means an AI system which is based on a general-purpose AI model and which has the capability to serve a variety of purposes, both for direct use as well as for integration in other AI systems;

[4] AI Act Annex XI, point (2) (similarity 0.735)
AI Act Annex XI, point (2) - Technical documentation referred to in Article 53(1), point (a) — technical documentation for providers of general-purpose AI models
2. A detailed description of the elements of the model referred to in point 1, and relevant information of the process for the development, including the following elements: (a) the technical means (e.g. instructions of use, infrastructure, tools) required for the general-purpose AI model to be integrated in AI systems; (b) the design specifications of the model and training process, including training methodologies and techniques, the key design choices including the rationale and assumptions made; what the model is designed to optimise for and the relevance of the different parameters, as applicable; (c) information on the data used for training, testing and validation, where applicable, including the type and provenance of data and curation methodologies (e.g. cleaning, filtering, etc.), the number of data points, their scope and main characteristics; how the data was obtained and selected as well as all other measures to detect the unsuitability of data sources and methods to detect identifiable biases, where applicable; (d) the computational resources used to train the model (e.g. number of floating point operations), training time, and other relevant details related to the training; (e) known or estimated energy consumption of the model. With regard to point (e), where the energy consumption of the model is unknown, the energy consumption may be based on information about computational resources used. Section 2 Additional information to be provided by providers of general-purpose AI models with systemic risk

[5] AI Act Article 55(1) (similarity 0.731)
AI Act Article 55(1) - Obligations of providers of general-purpose AI models with systemic risk
1. In addition to the obligations listed in Articles 53 and 54, providers of general-purpose AI models with systemic risk shall: (a) perform model evaluation in accordance with standardised protocols and tools reflecting the state of the art, including conducting and documenting adversarial testing of the model with a view to identifying and mitigating systemic risks; (b) assess and mitigate possible systemic risks at Union level, including their sources, that may stem from the development, the placing on the market, or the use of general-purpose AI models with systemic risk; (c) keep track of, document, and report, without undue delay, to the AI Office and, as appropriate, to national competent authorities, relevant information about serious incidents and possible corrective measures to address them; (d) ensure an adequate level of cybersecurity protection for the general-purpose AI model with systemic risk and the physical infrastructure of the model.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q14 (single)

**Question.** We bought a high-risk AI system from a vendor and run it ourselves. How long must we keep the logs it generates?

**Reference.** At least six months, unless other Union or national law, in particular data protection law, provides otherwise. *(expected: AI Act Article 26(6))*

**Agent answer.**

As a deployer, you must keep the automatically generated logs under your control for a period appropriate to the system's intended purpose, which is at least six months, unless otherwise provided by applicable Union or national law (such as personal data protection rules).

* Deployers must keep the logs under their control for a period appropriate to the intended purpose of the system, of at least six months, unless provided otherwise in applicable Union or national law: AI Act Article 26(6)
* Financial institutions subject to internal governance requirements under Union financial services law shall maintain the logs as part of their documentation kept under that law: AI Act Article 26(6)

**Cited:** AI Act Article 26  
**Retrieved:** AI Act Article 12, AI Act Article 18, AI Act Article 19, AI Act Article 26

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: high-risk AI system logs keep retention period deployer provider

[1] AI Act Article 26(6) (similarity 0.876)
AI Act Article 26(6) - Obligations of deployers of high-risk AI systems
6. Deployers of high-risk AI systems shall keep the logs automatically generated by that high-risk AI system to the extent such logs are under their control, for a period appropriate to the intended purpose of the high-risk AI system, of at least six months, unless provided otherwise in applicable Union or national law, in particular in Union law on the protection of personal data. Deployers that are financial institutions subject to requirements regarding their internal governance, arrangements or processes under Union financial services law shall maintain the logs as part of the documentation kept pursuant to the relevant Union financial service law.

[2] AI Act Article 19 (similarity 0.853)
AI Act Article 19 - Automatically generated logs
1. Providers of high-risk AI systems shall keep the logs referred to in Article 12(1), automatically generated by their high-risk AI systems, to the extent such logs are under their control. Without prejudice to applicable Union or national law, the logs shall be kept for a period appropriate to the intended purpose of the high-risk AI system, of at least six months, unless provided otherwise in the applicable Union or national law, in particular in Union law on the protection of personal data. 2. Providers that are financial institutions subject to requirements regarding their internal governance, arrangements or processes under Union financial services law shall maintain the logs automatically generated by their high-risk AI systems as part of the documentation kept under the relevant financial services law.

[3] AI Act Article 12(1)-(2) (similarity 0.846)
AI Act Article 12(1)-(2) - Record-keeping
1. High-risk AI systems shall technically allow for the automatic recording of events (logs) over the lifetime of the system. 2. In order to ensure a level of traceability of the functioning of a high-risk AI system that is appropriate to the intended purpose of the system, logging capabilities shall enable the recording of events relevant for: (a) identifying situations that may result in the high-risk AI system presenting a risk within the meaning of Article 79(1) or in a substantial modification; (b) facilitating the post-market monitoring referred to in Article 72; and (c) monitoring the operation of high-risk AI systems referred to in Article 26(5).

[4] AI Act Article 18 (similarity 0.828)
AI Act Article 18 - Documentation keeping
1. The provider shall, for a period ending 10 years after the high-risk AI system has been placed on the market or put into service, keep at the disposal of the national competent authorities: (a) the technical documentation referred to in Article 11; (b) the documentation concerning the quality management system referred to in Article 17; (c) the documentation concerning the changes approved by notified bodies, where applicable; (d) the decisions and other documents issued by the notified bodies, where applicable; (e) the EU declaration of conformity referred to in Article 47. 2. Each Member State shall determine conditions under which the documentation referred to in paragraph 1 remains at the disposal of the national competent authorities for the period indicated in that paragraph for the cases when a provider or its authorised representative established on its territory goes bankrupt or ceases its activity prior to the end of that period. 3. Providers that are financial institutions subject to requirements regarding their internal governance, arrangements or processes under Union financial services law shall maintain the technical documentation as part of the documentation kept under the relevant Union financial services law.

[5] AI Act Article 12(3) (similarity 0.825)
AI Act Article 12(3) - Record-keeping
3. For high-risk AI systems referred to in point 1 (a), of Annex III, the logging capabilities shall provide, at a minimum: (a) recording of the period of each use of the system (start date and time and end date and time of each use); (b) the reference database against which input data has been checked by the system; (c) the input data for which the search has led to a match; (d) the identification of the natural persons involved in the verification of the results, as referred to in Article 14(5).

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q15 (single)

**Question.** We build connected industrial machines. A customer wants the data their machine produced. Do we have to hand it over, and can we charge for it?

**Reference.** Yes. Where the user cannot access the data directly, the data holder must make readily available data available to the user without undue delay, free of charge, and continuously and in real time where relevant. *(expected: Data Act Article 4(1))*

**Agent answer.**

Yes, connected products must be designed and manufactured so that product data and related metadata are accessible to the user by default, easily, securely, and **free of charge**.

* Connected products and related services must be designed so that product data and relevant metadata are, by default, easily, securely, free of charge, in a structured, commonly used, and machine-readable format, and directly accessible where feasible (Data Act Article 3(1)).
* If the user cannot directly access the data from the connected product, data holders must make the readily available data accessible to the user without undue delay, easily, securely, and free of charge (Data Act Article 4(1)).
* Compensation rules that allow charging a reasonable margin apply to business-to-business relations between data *holders* and data *recipients* (Data Act Article 9(1)), but the specific obligation to provide data directly to the *user* under Article 3 and Article 4 is mandated to be free of charge.

**Cited:** Data Act Article 3, Data Act Article 4, Data Act Article 9  
**Retrieved:** Data Act Article 2, Data Act Article 20, Data Act Article 3, Data Act Article 4, Data Act Article 8, Data Act Article 9

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: make available data user connected product agreement user access

[1] Data Act Article 3(1)-(2) (similarity 0.786)
Data Act Article 3(1)-(2) - Obligation to make product data and related service data accessible to the user
1. Connected products shall be designed and manufactured, and related services shall be designed and provided, in such a manner that product data and related service data, including the relevant metadata necessary to interpret and use those data, are, by default, easily, securely, free of charge, in a comprehensive, structured, commonly used and machine-readable format, and, where relevant and technically feasible, directly accessible to the user. 2. Before concluding a contract for the purchase, rent or lease of a connected product, the seller, rentor or lessor, which may be the manufacturer, shall provide at least the following information to the user, in a clear and comprehensible manner: (a) the type, format and estimated volume of product data which the connected product is capable of generating; (b) whether the connected product is capable of generating data continuously and in real-time; (c) whether the connected product is capable of storing data on-device or on a remote server, including, where applicable, the intended duration of retention; (d) how the user may access, retrieve or, where relevant, erase the data, including the technical means to do so, as well as their terms of use and quality of service.

[2] Data Act Article 4(1)-(2) (similarity 0.769)
Data Act Article 4(1)-(2) - The rights and obligations of users and data holders with regard to access, use and making available product data and related service data
1. Where data cannot be directly accessed by the user from the connected product or related service, data holders shall make readily available data, as well as the relevant metadata necessary to interpret and use those data, accessible to the user without undue delay, of the same quality as is available to the data holder, easily, securely, free of charge, in a comprehensive, structured, commonly used and machine-readable format and, where relevant and technically feasible, continuously and in real-time. This shall be done on the basis of a simple request through electronic means where technically feasible. 2. Users and data holders may contractually restrict or prohibit accessing, using or further sharing data, if such processing could undermine security requirements of the connected product, as laid down by Union or national law, resulting in a serious adverse effect on the health, safety or security of natural persons. Sectoral authorities may provide users and data holders with technical expertise in that context. Where the data holder refuses to share data pursuant to this Article, it shall notify the competent authority designated pursuant to Article 37.

[3] Data Act Article 3(3) (similarity 0.762)
Data Act Article 3(3) - Obligation to make product data and related service data accessible to the user
3. Before concluding a contract for the provision of a related service, the provider of such related service shall provide at least the following information to the user, in a clear and comprehensible manner: (a) the nature, estimated volume and collection frequency of product data that the prospective data holder is expected to obtain and, where relevant, the arrangements for the user to access or retrieve such data, including the prospective data holder's data storage arrangements and the duration of retention; (b) the nature and estimated volume of related service data to be generated, as well as the arrangements for the user to access or retrieve such data, including the prospective data holder's data storage arrangements and the duration of retention; (c) whether the prospective data holder expects to use readily available data itself and the purposes for which those data are to be used, and whether it intends to allow one or more third parties to use the data for purposes agreed upon with the user; (d) the identity of the prospective data holder, such as its trading name and the geographical address at which it is established and, where applicable, of other data processing parties; (e) the means of communication which make it possible to contact the prospective data holder quickly and communicate with that data holder efficiently; (f) how the user can request that the data are shared with a third party and, where applicable, end the data sharing; (g) the user's right to lodge a complaint alleging an infringement of any of the provisions of this Chapter with the competent authority designated pursuant to Article 37; (h) whether a prospective data holder is the holder of trade secrets contained in the data that is accessible from the connected product or generated during the provision of a related service, and, where the prospective data holder is not the trade secret holder, the identity of the trade secret holder; (i) the duration of the contract between the user and the prospective data holder, as well as the arrangements for terminating such a contract.

[4] Data Act Article 4(12)-(13) (similarity 0.759)
Data Act Article 4(12)-(13) - The rights and obligations of users and data holders with regard to access, use and making available product data and related service data
12. Where the user is not the data subject whose personal data is requested, any personal data generated by the use of a connected product or related service shall be made available by the data holder to the user only where there is a valid legal basis for processing under Article 6 of Regulation (EU) 2016/679 and, where relevant, the conditions of Article 9 of that Regulation and of Article 5(3) of Directive 2002/58/EC are fulfilled. 13. A data holder shall only use any readily available data that is non-personal data on the basis of a contract with the user. A data holder shall not use such data to derive insights about the economic situation, assets and production methods of, or the use by, the user in any other manner that could undermine the commercial position of that user on the markets in which the user is active.

[5] Data Act Article 2, points (15) to (17) (similarity 0.744)
Data Act Article 2, points (15) to (17) - Definitions
(15) 'product data' means data generated by the use of a connected product that the manufacturer designed to be retrievable, via an electronic communications service, physical connection or on-device access, by a user, data holder or a third party, including, where relevant, the manufacturer; (16) 'related service data' means data representing the digitisation of user actions or of events related to the connected product, recorded intentionally by the user or generated as a by-product of the user's action during the provision of a related service by the provider; (17) 'readily available data' means product data and related service data that a data holder lawfully obtains or can lawfully obtain from the connected product or related service, without disproportionate effort going beyond a simple operation;

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.

5 passages for: Data Act compensation making available data to user reasonable cost fee

[1] Data Act Article 9(1)-(2) (similarity 0.854)
Data Act Article 9(1)-(2) - Compensation for making data available
1. Any compensation agreed upon between a data holder and a data recipient for making data available in business-to-business relations shall be non- discriminatory and reasonable and may include a margin. 2. When agreeing on any compensation, the data holder and the data recipient shall take into account in particular: (a) costs incurred in making the data available, including, in particular, the costs necessary for the formatting of data, dissemination via electronic means and storage; (b) investments in the collection and production of data, where applicable, taking into account whether other parties contributed to obtaining, generating or collecting the data in question.

[2] Data Act Article 9(3)-(6) (similarity 0.847)
Data Act Article 9(3)-(6) - Compensation for making data available
3. The compensation referred to in paragraph 1 may also depend on the volume, format and nature of the data. 4. Where the data recipient is an SME or a not-for-profit research organisation and where such a data recipient does not have partner enterprises or linked enterprises that do not qualify as SMEs, any compensation agreed shall not exceed the costs referred to in paragraph 2, point (a). 5. The Commission shall adopt guidelines on the calculation of reasonable compensation, taking into account the advice of the European Data Innovation Board (EDIB) referred to in Article 42. 6. This Article shall not preclude other Union law or national legislation adopted in accordance with Union law from excluding compensation for making data available or providing for lower compensation.

[3] Data Act Article 20(1)-(2) (similarity 0.834)
Data Act Article 20(1)-(2) - Compensation in cases of an exceptional need
1. Data holders other than microenterprises and small enterprises shall make available data necessary to respond to a public emergency pursuant to Article 15(1), point (a), free of charge. The public sector body, the Commission, the European Central Bank or the Union body that has received data shall provide public acknowledgement to the data holder if requested by the data holder. 2. The data holder shall be entitled to fair compensation for making data available in compliance with a request made pursuant to Article 15(1), point (b). Such compensation shall cover the technical and organisational costs incurred to comply with the request including, where applicable, the costs of anonymisation, pseudonymisation, aggregation and of technical adaptation, and a reasonable margin. Upon request of the public sector body, the Commission, the European Central Bank or the Union body, the data holder shall provide information on the basis for the calculation of the costs and the reasonable margin.

[4] Data Act Article 9(7) (similarity 0.818)
Data Act Article 9(7) - Compensation for making data available
7. The data holder shall provide the data recipient with information setting out the basis for the calculation of the compensation in sufficient detail so that the data recipient can assess whether the requirements of paragraphs 1 to 4 are met.

[5] Data Act Article 20(3)-(5) (similarity 0.818)
Data Act Article 20(3)-(5) - Compensation in cases of an exceptional need
3. Paragraph 2 shall also apply where a microenterprise and small enterprise claims compensation for making data available. 4. Data holders shall not be entitled to compensation for making data available in compliance with a request made pursuant to Article 15(1), point (b), where the specific task carried out in the public interest is the production of official statistics and where the purchase of data is not allowed by national law. Member States shall notify the Commission where the purchase of data for the production of official statistics is not allowed by national law. 5. Where the public sector body, the Commission, the European Central Bank or the Union body disagrees with the level of compensation requested by the data holder, they may lodge a complaint with the competent authority designated pursuant to Article 37 of the Member State where the data holder is established.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.

5 passages for: Data Act Article 8 compensation user making data available business-to-consumer

[1] Data Act Article 9(1)-(2) (similarity 0.871)
Data Act Article 9(1)-(2) - Compensation for making data available
1. Any compensation agreed upon between a data holder and a data recipient for making data available in business-to-business relations shall be non- discriminatory and reasonable and may include a margin. 2. When agreeing on any compensation, the data holder and the data recipient shall take into account in particular: (a) costs incurred in making the data available, including, in particular, the costs necessary for the formatting of data, dissemination via electronic means and storage; (b) investments in the collection and production of data, where applicable, taking into account whether other parties contributed to obtaining, generating or collecting the data in question.

[2] Data Act Article 9(3)-(6) (similarity 0.853)
Data Act Article 9(3)-(6) - Compensation for making data available
3. The compensation referred to in paragraph 1 may also depend on the volume, format and nature of the data. 4. Where the data recipient is an SME or a not-for-profit research organisation and where such a data recipient does not have partner enterprises or linked enterprises that do not qualify as SMEs, any compensation agreed shall not exceed the costs referred to in paragraph 2, point (a). 5. The Commission shall adopt guidelines on the calculation of reasonable compensation, taking into account the advice of the European Data Innovation Board (EDIB) referred to in Article 42. 6. This Article shall not preclude other Union law or national legislation adopted in accordance with Union law from excluding compensation for making data available or providing for lower compensation.

[3] Data Act Article 8(1)-(2) (similarity 0.849)
Data Act Article 8(1)-(2) - Conditions under which data holders make data available to data recipients
1. Where, in business-to-business relations, a data holder is obliged to make data available to a data recipient under Article 5 or under other applicable Union law or national legislation adopted in accordance with Union law, it shall agree with a data recipient the arrangements for making the data available and shall do so under fair, reasonable and non-discriminatory terms and conditions and in a transparent manner in accordance with this Chapter and Chapter IV. 2. A contractual term concerning access to and the use of data, or liability and remedies for the breach or termination of data-related obligations, shall not be binding if it constitutes an unfair contractual term within the meaning of Article 13 or if, to the detriment of the user, it excludes the application of, derogates from or varies the effect of the user's rights under Chapter II.

[4] Data Act Article 20(1)-(2) (similarity 0.844)
Data Act Article 20(1)-(2) - Compensation in cases of an exceptional need
1. Data holders other than microenterprises and small enterprises shall make available data necessary to respond to a public emergency pursuant to Article 15(1), point (a), free of charge. The public sector body, the Commission, the European Central Bank or the Union body that has received data shall provide public acknowledgement to the data holder if requested by the data holder. 2. The data holder shall be entitled to fair compensation for making data available in compliance with a request made pursuant to Article 15(1), point (b). Such compensation shall cover the technical and organisational costs incurred to comply with the request including, where applicable, the costs of anonymisation, pseudonymisation, aggregation and of technical adaptation, and a reasonable margin. Upon request of the public sector body, the Commission, the European Central Bank or the Union body, the data holder shall provide information on the basis for the calculation of the costs and the reasonable margin.

[5] Data Act Article 9(7) (similarity 0.841)
Data Act Article 9(7) - Compensation for making data available
7. The data holder shall provide the data recipient with information setting out the basis for the calculation of the compensation in sufficient detail so that the data recipient can assess whether the requirements of paragraphs 1 to 4 are met.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q16 (single)

**Question.** If a customer wants to leave our cloud service for a competitor, what are the longest waiting periods we can impose?

**Reference.** The customer may initiate switching with a notice period of at most two months, and the mandatory maximum transitional period for completing the switch is 30 calendar days. *(expected: Data Act Article 25(2))*

**Agent answer.**

The maximum notice period for initiating the switching process shall not exceed two months.

* Data Act Article 25(2)(d)

The mandatory maximum transitional period for completing the switch shall not exceed 30 calendar days, though this can be extended to an alternative transitional period of up to seven months if technically unfeasible.

* Data Act Article 25(2)(a)
* Data Act Article 25(4)

After the transitional period, there must be a minimum data retrieval period of at least 30 calendar days.

* Data Act Article 25(2)(g)

**Cited:** Data Act Article 25  
**Retrieved:** Data Act Article 2, Data Act Article 23, Data Act Article 25, Data Act Article 29

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: switching charges transition period data act cloud service competitor

[1] Data Act Article 23 (similarity 0.818)
Data Act Article 23 - Removing obstacles to effective switching
Providers of data processing services shall take the measures provided for in Articles 25, 26, 27, 29 and 30 to enable customers to switch to a data processing service, covering the same service type, which is provided by a different provider of data processing services, or to on-premises ICT infrastructure, or, where relevant, to use several providers of data processing services at the same time. In particular, providers of data processing services shall not impose and shall remove pre-commercial, commercial, technical, contractual and organisational obstacles, which inhibit customers from: (a) terminating, after the maximum notice period and the successful completion of the switching process, in accordance with Article 25, the contract of the data processing service; (b) concluding new contracts with a different provider of data processing services covering the same service type; (c) porting the customer's exportable data and digital assets, to a different provider of data processing services or to an on-premises ICT infrastructure, including after having benefited from a free-tier offering; (d) in accordance with Article 24, achieving functional equivalence in the use of the new data processing service in the ICT environment of a different provider of data processing services covering the same service type; (e) unbundling, where technically feasible, data processing services referred to in Article 30(1) from other data processing services provided by the provider of data processing services.

[2] Data Act Article 29(1)-(4) (similarity 0.810)
Data Act Article 29(1)-(4) - Gradual withdrawal of switching charges
1. From 12 January 2027, providers of data processing services shall not impose any switching charges on the customer for the switching process. 2. From 11 January 2024 to 12 January 2027, providers of data processing services may impose reduced switching charges on the customer for the switching process. 3. The reduced switching charges referred to in paragraph 2 shall not exceed the costs incurred by the provider of data processing services that are directly linked to the switching process concerned. 4. Before entering into a contract with a customer, providers of data processing services shall provide the prospective customer with clear information on the standard service fees and early termination penalties that might be imposed, as well as on the reduced switching charges that might be imposed during the timeframe referred to in paragraph 2.

[3] Data Act Article 25(3)-(4) (similarity 0.805)
Data Act Article 25(3)-(4) - Contractual terms concerning switching
3. The contract referred to in paragraph 1 shall include clauses providing that the customer may notify the provider of data processing services of its decision to perform one or more of the following actions upon termination of the maximum notice period referred to in paragraph 2, point (d): (a) switch to a different provider of data processing services, in which case the customer shall provide the necessary details of that provider; (b) switch to an on-premises ICT infrastructure; (c) erase its exportable data and digital assets. 4. Where the mandatory maximum transitional period as provided for in paragraph 2, point (a) is technically unfeasible, the provider of data processing services shall notify the customer within 14 working days of the making of the switching request, and shall duly justify the technical unfeasibility and indicate an alternative transitional period, which shall not exceed seven months. In accordance with paragraph 1, service continuity shall be ensured throughout the alternative transitional period.

[4] Data Act Article 25(1)-(2) (similarity 0.805)
Data Act Article 25(1)-(2) - Contractual terms concerning switching
1. The rights of the customer and the obligations of the provider of data processing services in relation to switching between providers of such services or, where applicable, to an on-premises ICT infrastructure shall be clearly set out in a written contract. The provider of data processing services shall make that contract available to the customer prior to signing the contract in a way that allows the customer to store and reproduce the contract. 2. Without prejudice to Directive (EU) 2019/770, the contract referred to in paragraph 1 of this Article shall include at least the following: (a) clauses allowing the customer, upon request, to switch to a data processing service offered by a different provider of data processing services or to port all exportable data and digital assets to an on-premises ICT infrastructure, without undue delay and in any event not after the mandatory maximum transitional period of 30 calendar days, to be initiated after the maximum notice period referred to in point (d), during which the service contract remains applicable and during which the provider of data processing services shall: (i) provide reasonable assistance to the customer and third parties authorised by the customer in the switching process; (ii) act with due care to maintain business continuity, and continue the provision of the functions or services under the contract; (iii) provide clear information concerning known risks to continuity in the provision of the functions or services on the part of the source provider of data processing services; (iv) ensure that a high level of security is maintained throughout the switching process, in particular the security of the data during their transfer and the continued security of the data during the retrieval period specified in point (g), in accordance with applicable Union or national law; (b) an obligation of the provider of data processing services to support the customer's exit strategy relevant to the contracted services, including by providing all relevant information; (c) a clause specifying that the contract shall be considered to be terminated and the customer shall be notified of the termination, in one of the following cases: (i) where applicable, upon the successful completion of the switching process; (ii) at the end of the maximum notice period referred to in paragraph (d), where the customer does not wish to switch but to erase its exportable data and digital assets upon service termination; (d) a maximum notice period for initiation of the switching process, which shall not exceed two months; (e) an exhaustive specification of all categories of data and digital assets that can be ported during the switching process, including, at a minimum, all exportable data; (f) an exhaustive specification of categories of data specific to the internal functioning of the provider's data processing service that are to be exempted from the exportable data under point (e) of this paragraph where a risk of breach of trade secrets of the provider exists, provided that such exemptions do not impede or delay the switching process provided for in Article 23; (g) a minimum period for data retrieval of at least 30 calendar days, starting after the termination of the transitional period that was agreed between the customer and the provider of data processing services, in accordance with point (a) of this paragraph and paragraph 4; (h) a clause guaranteeing full erasure of all exportable data and digital assets generated directly by the customer, or relating to the customer directly, after the expiry of the retrieval period referred to in point (g) or after the expiry of an alternative agreed period at a date later than the date of expiry of the retrieval period referred to in point (g), provided that the switching process has been completed successfully; (i) switching charges, that may be imposed by providers of data processing services in accordance with Article 29.

[5] Data Act Article 2, points (35) to (37) (similarity 0.788)
Data Act Article 2, points (35) to (37) - Definitions
(35) 'data egress charges' means data transfer fees charged to customers for extracting their data through the network from the ICT infrastructure of a provider of data processing services to the system of a different provider or to on-premises ICT infrastructure; (36) 'switching charges' means charges, other than standard service fees or early termination penalties, imposed by a provider of data processing services on a customer for the actions mandated by this Regulation for switching to the system of a different provider or to on-premises ICT infrastructure, including data egress charges; (37) 'functional equivalence' means re-establishing on the basis of the customer's exportable data and digital assets, a minimum level of functionality in the environment of a new data processing service of the same service type after the switching process, where the destination data processing service delivers a materially comparable outcome in response to the same input for shared features supplied to the customer under the contract;

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q17 (single)

**Question.** A big client made us sign a clause that lets them use all the data our product collects, for free, with heavy penalties if we refuse. Can we challenge it?

**Reference.** Yes. A contractual term on access to and use of data, or on liability and remedies, that was unilaterally imposed on an enterprise is not binding if it is unfair. *(expected: Data Act Article 13(1))*

**Agent answer.**

Yes, you can challenge the clause if it was unilaterally imposed by the client and is unfair under the rules governing business-to-business data access and use contracts.

* A contractual term concerning data access and use that is unilaterally imposed by one enterprise on another is not binding if it is unfair, meaning its use grossly deviates from good commercial practice in data access and use, contrary to good faith and fair dealing. (Data Act Article 13(1) and Article 13(3))
* A term is presumed unfair if its object or effect is to allow the imposing party to access and use the other party's data in a manner significantly detrimental to their legitimate interests, particularly for commercially sensitive data, trade secrets, or intellectual property. (Data Act Article 13(5)(b))
* A term is also presumed unfair if it prevents the party upon whom it was imposed from using the data provided or generated by it, or limits such use so that they cannot adequately exploit, access, or control that data. (Data Act Article 13(5)(c))
* A term is considered unilaterally imposed if it was supplied by one party and the other party could not influence its content despite attempting to negotiate it, with the burden of proof resting on the party who supplied the term. (Data Act Article 13(6))
* If the unfair term is severable from the rest of the contract, the remaining terms remain binding. (Data Act Article 13(7))

**Cited:** Data Act Article 13  
**Retrieved:** Data Act Article 13, Data Act Article 8

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: unfair contractual terms data holder business data act

[1] Data Act Article 13(5) (similarity 0.816)
Data Act Article 13(5) - Unfair contractual terms unilaterally imposed on another enterprise
5. A contractual term shall be presumed to be unfair for the purposes of paragraph 3 if its object or effect is to: (a) inappropriately limit remedies in the case of non-performance of contractual obligations or liability in the case of a breach of those obligations, or extend the liability of the enterprise upon whom the term has been unilaterally imposed; (b) allow the party that unilaterally imposed the term to access and use the data of the other contracting party in a manner that is significantly detrimental to the legitimate interests of the other contracting party, in particular when such data contain commercially sensitive data or are protected by trade secrets or by intellectual property rights; (c) prevent the party upon whom the term has been unilaterally imposed from using the data provided or generated by that party during the period of the contract, or to limit the use of such data to the extent that that party is not entitled to use, capture, access or control such data or exploit the value of such data in an adequate manner; (d) prevent the party upon whom the term has been unilaterally imposed from terminating the agreement within a reasonable period; (e) prevent the party upon whom the term has been unilaterally imposed from obtaining a copy of the data provided or generated by that party during the period of the contract or within a reasonable period after the termination thereof; (f) enable the party that unilaterally imposed the term to terminate the contract at unreasonably short notice, taking into consideration any reasonable possibility of the other contracting party to switch to an alternative and comparable service and the financial detriment caused by such termination, except where there are serious grounds for so doing; (g) enable the party that unilaterally imposed the term to substantially change the price specified in the contract or any other substantive condition related to the nature, format, quality or quantity of the data to be shared, where no valid reason and no right of the other party to terminate the contract in the case of such a change is specified in the contract. Point (g) of the first subparagraph shall not affect terms by which the party that unilaterally imposed the term reserves the right to unilaterally change the terms of a contract of an indeterminate duration, provided that the contract specified a valid reason for such unilateral changes, that the party that unilaterally imposed the term is required to provide the other contracting party with reasonable notice of any such intended change, and that the other contracting party is free to terminate the contract at no cost in the case of a change.

[2] Data Act Article 13(1)-(3) (similarity 0.813)
Data Act Article 13(1)-(3) - Unfair contractual terms unilaterally imposed on another enterprise
1. A contractual term concerning access to and the use of data or liability and remedies for the breach or the termination of data related obligations, which has been unilaterally imposed by an enterprise on another enterprise, shall not be binding on the latter enterprise if it is unfair. 2. A contractual term which reflects mandatory provisions of Union law, or provisions of Union law which would apply if the contractual terms did not regulate the matter, shall not be considered to be unfair. 3. A contractual term is unfair if it is of such a nature that its use grossly deviates from good commercial practice in data access and use, contrary to good faith and fair dealing.

[3] Data Act Article 8(1)-(2) (similarity 0.796)
Data Act Article 8(1)-(2) - Conditions under which data holders make data available to data recipients
1. Where, in business-to-business relations, a data holder is obliged to make data available to a data recipient under Article 5 or under other applicable Union law or national legislation adopted in accordance with Union law, it shall agree with a data recipient the arrangements for making the data available and shall do so under fair, reasonable and non-discriminatory terms and conditions and in a transparent manner in accordance with this Chapter and Chapter IV. 2. A contractual term concerning access to and the use of data, or liability and remedies for the breach or termination of data-related obligations, shall not be binding if it constitutes an unfair contractual term within the meaning of Article 13 or if, to the detriment of the user, it excludes the application of, derogates from or varies the effect of the user's rights under Chapter II.

[4] Data Act Article 13(6)-(7) (similarity 0.795)
Data Act Article 13(6)-(7) - Unfair contractual terms unilaterally imposed on another enterprise
6. A contractual term shall be considered to be unilaterally imposed within the meaning of this Article if it has been supplied by one contracting party and the other contracting party has not been able to influence its content despite an attempt to negotiate it. The contracting party that supplied the contractual term bears the burden of proving that that term has not been unilaterally imposed. The contracting party that supplied the contested contractual term may not argue that the term is an unfair contractual term. 7. Where the unfair contractual term is severable from the remaining terms of the contract, those remaining terms shall be binding.

[5] Data Act Article 13(4) (similarity 0.794)
Data Act Article 13(4) - Unfair contractual terms unilaterally imposed on another enterprise
4. In particular, a contractual term shall be unfair for the purposes of paragraph 3, if its object or effect is to: (a) exclude or limit the liability of the party that unilaterally imposed the term for intentional acts or gross negligence; (b) exclude the remedies available to the party upon whom the term has been unilaterally imposed in the case of non-performance of contractual obligations, or the liability of the party that unilaterally imposed the term in the case of a breach of those obligations; (c) give the party that unilaterally imposed the term the exclusive right to determine whether the data supplied are in conformity with the contract or to interpret any contractual term.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q18 (multi)

**Question.** Can a city government force us to hand over our data during a flood emergency?

**Reference.** Yes. Under Art. 14 data holders must make data available to a public sector body that demonstrates an exceptional need; Art. 15(1)(a) counts responding to a public emergency, if the body cannot obtain the data by other means in a timely and effective manner under equivalent conditions. *(expected: Data Act;Data Act Article 14;Article 15(1)(a))*

**Agent answer.**

Yes, a local city government can request and force you to hand over data during a flood emergency if it demonstrates an exceptional need to respond to that natural disaster, provided alternative means are unavailable.

* A city government qualifies as a public sector body under the law and can submit a duly reasoned request for data to carry out its statutory duties in the public interest based on an exceptional need. Data Act Article 14
* A flood emergency constitutes a public emergency, defined as an exceptional situation resulting from a natural disaster that negatively affects the population and carries a risk of serious repercussions. Data Act Article 2, points (28) to (29)
* An exceptional need to use data exists when the requested data is necessary to respond to a public emergency and the public sector body cannot obtain it by alternative means in a timely and effective manner. Data Act Article 15(1)
* You must make the requested data available without undue delay, though you may decline or seek modification of the request within a maximum of five working days on specific grounds such as lack of control over the data. Data Act Article 18(1)-(2)
* Data holders other than microenterprises and small enterprises must make data available free of charge when requested to respond to a public emergency. Data Act Article 20(1)

**Cited:** Data Act Article 14, Data Act Article 15, Data Act Article 18, Data Act Article 2, Data Act Article 20  
**Retrieved:** Data Act Article 14, Data Act Article 15, Data Act Article 18, Data Act Article 19, Data Act Article 2, Data Act Article 20

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: public authority access data flood emergency disaster Data Act

[1] Data Act Article 15(1) (similarity 0.795)
Data Act Article 15(1) - Exceptional need to use data
1. An exceptional need to use certain data within the meaning of this Chapter shall be limited in time and scope and shall be considered to exist only in any of the following circumstances: (a) where the data requested is necessary to respond to a public emergency and the public sector body, the Commission, the European Central Bank or the Union body is unable to obtain such data by alternative means in a timely and effective manner under equivalent conditions; (b) in circumstances not covered by point (a) and only insofar as non-personal data is concerned, where: (i) a public sector body, the Commission, the European Central Bank or a Union body is acting on the basis of Union or national law and has identified specific data, the lack of which prevents it from fulfilling a specific task carried out in the public interest, that has been explicitly provided for by law, such as the production of official statistics or the mitigation of or recovery from a public emergency; and (ii) the public sector body, the Commission, the European Central Bank or the Union body has exhausted all other means at its disposal to obtain such data, including purchase of non-personal data on the market by offering market rates, or by relying on existing obligations to make data available or the adoption of new legislative measures which could guarantee the timely availability of the data.

[2] Data Act Article 2, points (28) to (29) (similarity 0.792)
Data Act Article 2, points (28) to (29) - Definitions
(28) 'public sector body' means national, regional or local authorities of the Member States and bodies governed by public law of the Member States, or associations formed by one or more such authorities or one or more such bodies; (29) 'public emergency' means an exceptional situation, limited in time, such as a public health emergency, an emergency resulting from natural disasters, a human-induced major disaster, including a major cybersecurity incident, negatively affecting the population of the Union or the whole or part of a Member State, with a risk of serious and lasting repercussions for living conditions or economic stability, financial stability, or the substantial and immediate degradation of economic assets in the Union or the relevant Member State and which is determined or officially declared in accordance with the relevant procedures under Union or national law;

[3] Data Act Article 14 (similarity 0.780)
Data Act Article 14 - Obligation to make data available on the basis of an exceptional need
Where a public sector body, the Commission, the European Central Bank or a Union body demonstrates an exceptional need, as set out in Article 15, to use certain data, including the relevant metadata necessary to interpret and use those data, to carry out its statutory duties in the public interest, data holders that are legal persons, other than public sectors bodies, which hold those data shall make them available upon a duly reasoned request.

[4] Data Act Article 18(1)-(2) (similarity 0.780)
Data Act Article 18(1)-(2) - Compliance with requests for data
1. A data holder receiving a request to make data available under this Chapter shall make the data available to the requesting public sector body, the Commission, the European Central Bank or a Union body without undue delay, taking into account necessary technical, organisational and legal measures. 2. Without prejudice to specific needs regarding the availability of data defined in Union or national law, a data holder may decline or seek the modification of a request to make data available under this Chapter without undue delay and, in any event, no later than five working days after the receipt of a request for the data necessary to respond to a public emergency and without undue delay and, in any event, no later than 30 working days after the receipt of such a request in other cases of an exceptional need, on any of the following grounds: (a) the data holder does not have control over the data requested; (b) a similar request for the same purpose has been previously submitted by another public sector body or the Commission, the European Central Bank or a Union body and the data holder has not been notified of the erasure of the data pursuant to Article 19(1), point (c); (c) the request does not meet the conditions laid down in Article 17(1) and (2).

[5] Data Act Article 19(1) (similarity 0.776)
Data Act Article 19(1) - Obligations of public sector bodies, the Commission, the European Central Bank and Union bodies
1. A public sector body, the Commission, the European Central Bank or a Union body receiving data pursuant to a request made under Article 14 shall: (a) not use the data in a manner incompatible with the purpose for which they were requested; (b) have implemented technical and organisational measures that preserve the confidentiality and integrity of the requested data and the security of the data transfers, in particular personal data, and safeguard the rights and freedoms of data subjects; (c) erase the data as soon as they are no longer necessary for the stated purpose and inform the data holder and individuals or organisations that received the data pursuant to Article 21(1) without undue delay that the data have been erased, unless archiving of the data is required in accordance with Union or national law on public access to documents in the context of transparency obligations.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.

5 passages for: exceptional need public authority emergency Data Act

[1] Data Act Article 15(1) (similarity 0.888)
Data Act Article 15(1) - Exceptional need to use data
1. An exceptional need to use certain data within the meaning of this Chapter shall be limited in time and scope and shall be considered to exist only in any of the following circumstances: (a) where the data requested is necessary to respond to a public emergency and the public sector body, the Commission, the European Central Bank or the Union body is unable to obtain such data by alternative means in a timely and effective manner under equivalent conditions; (b) in circumstances not covered by point (a) and only insofar as non-personal data is concerned, where: (i) a public sector body, the Commission, the European Central Bank or a Union body is acting on the basis of Union or national law and has identified specific data, the lack of which prevents it from fulfilling a specific task carried out in the public interest, that has been explicitly provided for by law, such as the production of official statistics or the mitigation of or recovery from a public emergency; and (ii) the public sector body, the Commission, the European Central Bank or the Union body has exhausted all other means at its disposal to obtain such data, including purchase of non-personal data on the market by offering market rates, or by relying on existing obligations to make data available or the adoption of new legislative measures which could guarantee the timely availability of the data.

[2] Data Act Article 14 (similarity 0.862)
Data Act Article 14 - Obligation to make data available on the basis of an exceptional need
Where a public sector body, the Commission, the European Central Bank or a Union body demonstrates an exceptional need, as set out in Article 15, to use certain data, including the relevant metadata necessary to interpret and use those data, to carry out its statutory duties in the public interest, data holders that are legal persons, other than public sectors bodies, which hold those data shall make them available upon a duly reasoned request.

[3] Data Act Article 2, points (28) to (29) (similarity 0.822)
Data Act Article 2, points (28) to (29) - Definitions
(28) 'public sector body' means national, regional or local authorities of the Member States and bodies governed by public law of the Member States, or associations formed by one or more such authorities or one or more such bodies; (29) 'public emergency' means an exceptional situation, limited in time, such as a public health emergency, an emergency resulting from natural disasters, a human-induced major disaster, including a major cybersecurity incident, negatively affecting the population of the Union or the whole or part of a Member State, with a risk of serious and lasting repercussions for living conditions or economic stability, financial stability, or the substantial and immediate degradation of economic assets in the Union or the relevant Member State and which is determined or officially declared in accordance with the relevant procedures under Union or national law;

[4] Data Act Article 15(2)-(3) (similarity 0.818)
Data Act Article 15(2)-(3) - Exceptional need to use data
2. Paragraph 1, point (b), shall not apply to microenterprises and small enterprises. 3. The obligation to demonstrate that the public sector body was unable to obtain non-personal data by purchasing them on the market shall not apply where the specific task carried out in the public interest is the production of official statistics and where the purchase of such data is not allowed by national law.

[5] Data Act Article 20(1)-(2) (similarity 0.809)
Data Act Article 20(1)-(2) - Compensation in cases of an exceptional need
1. Data holders other than microenterprises and small enterprises shall make available data necessary to respond to a public emergency pursuant to Article 15(1), point (a), free of charge. The public sector body, the Commission, the European Central Bank or the Union body that has received data shall provide public acknowledgement to the data holder if requested by the data holder. 2. The data holder shall be entitled to fair compensation for making data available in compliance with a request made pursuant to Article 15(1), point (b). Such compensation shall cover the technical and organisational costs incurred to comply with the request including, where applicable, the costs of anonymisation, pseudonymisation, aggregation and of technical adaptation, and a reasonable margin. Upon request of the public sector body, the Commission, the European Central Bank or the Union body, the data holder shall provide information on the basis for the calculation of the costs and the reasonable margin.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q19 (multi)

**Question.** Our recruiting tool uses AI to automatically reject job applicants with no human looking at it. What rules apply to that?

**Reference.** GDPR gives people the right not to be subject to decisions based solely on automated processing with legal or similarly significant effects, and the AI Act lists AI systems used for recruitment and selection of candidates as high-risk. *(expected: GDPR;AI Act Article 22(1);Annex III, point (4))*

**Agent answer.**

An AI tool used to automatically reject job applicants without human review is regulated as a high-risk AI system under the AI Act and falls under strict rules governing automated decision-making under the GDPR:

* AI systems intended to be used for the recruitment or selection of natural persons, including to analyze and filter job applications and evaluate candidates, are classified as high-risk AI systems AI Act Annex III, points (4) to (5).
* Before putting into service or using a high-risk AI system at the workplace, employers must inform workers' representatives and the affected workers AI Act Article 26(7)-(8).
* Data subjects have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects or similarly significantly affects them GDPR Article 22(1)-(2).
* Solely automated decisions are prohibited unless the decision is necessary for entering into or performing a contract, authorized by law with safeguard measures, or based on explicit consent GDPR Article 22(1)-(2).
* When automated decisions are based on contract necessity or explicit consent, controllers must implement suitable measures to safeguard rights, including the right to obtain human intervention, express a point of view, and contest the decision GDPR Article 22(3)-(4).

**Cited:** AI Act Annex III, AI Act Article 26, GDPR Article 22  
**Retrieved:** AI Act Annex III, AI Act Article 26, AI Act Article 5, GDPR Article 22, GDPR Article 4, GDPR Article 88

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: AI Act employment recruitment worker management high-risk AI system

[1] AI Act Annex III, points (4) to (5) (similarity 0.831)
AI Act Annex III, points (4) to (5) - High-risk AI systems referred to in Article 6(2)
4. Employment, workers' management and access to self-employment: (a) AI systems intended to be used for the recruitment or selection of natural persons, in particular to place targeted job advertisements, to analyse and filter job applications, and to evaluate candidates; (b) AI systems intended to be used to make decisions affecting terms of work-related relationships, the promotion or termination of work-related contractual relationships, to allocate tasks based on individual behaviour or personal traits or characteristics or to monitor and evaluate the performance and behaviour of persons in such relationships. 5. Access to and enjoyment of essential private services and essential public services and benefits: (a) AI systems intended to be used by public authorities or on behalf of public authorities to evaluate the eligibility of natural persons for essential public assistance benefits and services, including healthcare services, as well as to grant, reduce, revoke, or reclaim such benefits and services; (b) AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score, with the exception of AI systems used for the purpose of detecting financial fraud; (c) AI systems intended to be used for risk assessment and pricing in relation to natural persons in the case of life and health insurance; (d) AI systems intended to evaluate and classify emergency calls by natural persons or to be used to dispatch, or to establish priority in the dispatching of, emergency first response services, including by police, firefighters and medical aid, as well as of emergency healthcare patient triage systems.

[2] AI Act Annex III, point (7) (similarity 0.790)
AI Act Annex III, point (7) - High-risk AI systems referred to in Article 6(2)
7. Migration, asylum and border control management, in so far as their use is permitted under relevant Union or national law: (a) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies as polygraphs or similar tools; (b) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies to assess a risk, including a security risk, a risk of irregular migration, or a health risk, posed by a natural person who intends to enter or who has entered into the territory of a Member State; (c) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies to assist competent public authorities for the examination of applications for asylum, visa or residence permits and for associated complaints with regard to the eligibility of the natural persons applying for a status, including related assessments of the reliability of evidence; (d) AI systems intended to be used by or on behalf of competent public authorities, or by Union institutions, bodies, offices or agencies, in the context of migration, asylum or border control management, for the purpose of detecting, recognising or identifying natural persons, with the exception of the verification of travel documents.

[3] AI Act Article 26(7)-(8) (similarity 0.784)
AI Act Article 26(7)-(8) - Obligations of deployers of high-risk AI systems
7. Before putting into service or using a high-risk AI system at the workplace, deployers who are employers shall inform workers' representatives and the affected workers that they will be subject to the use of the high-risk AI system. This information shall be provided, where applicable, in accordance with the rules and procedures laid down in Union and national law and practice on information of workers and their representatives. 8. Deployers of high-risk AI systems that are public authorities, or Union institutions, bodies, offices or agencies shall comply with the registration obligations referred to in Article 49. When such deployers find that the high-risk AI system that they envisage using has not been registered in the EU database referred to in Article 71, they shall not use that system and shall inform the provider or the distributor.

[4] AI Act Annex III, points (2) to (3) (similarity 0.775)
AI Act Annex III, points (2) to (3) - High-risk AI systems referred to in Article 6(2)
2. Critical infrastructure: AI systems intended to be used as safety components in the management and operation of critical digital infrastructure, road traffic, or in the supply of water, gas, heating or electricity. 3. Education and vocational training: (a) AI systems intended to be used to determine access or admission or to assign natural persons to educational and vocational training institutions at all levels; (b) AI systems intended to be used to evaluate learning outcomes, including when those outcomes are used to steer the learning process of natural persons in educational and vocational training institutions at all levels; (c) AI systems intended to be used for the purpose of assessing the appropriate level of education that an individual will receive or will be able to access, in the context of or within educational and vocational training institutions at all levels; (d) AI systems intended to be used for monitoring and detecting prohibited behaviour of students during tests in the context of or within educational and vocational training institutions at all levels.

[5] AI Act Article 5(1) (similarity 0.771)
AI Act Article 5(1) - Prohibited AI practices
1. The following AI practices shall be prohibited: (a) the placing on the market, the putting into service or the use of an AI system that deploys subliminal techniques beyond a person's consciousness or purposefully manipulative or deceptive techniques, with the objective, or the effect of materially distorting the behaviour of a person or a group of persons by appreciably impairing their ability to make an informed decision, thereby causing them to take a decision that they would not have otherwise taken in a manner that causes or is reasonably likely to cause that person, another person or group of persons significant harm; (b) the placing on the market, the putting into service or the use of an AI system that exploits any of the vulnerabilities of a natural person or a specific group of persons due to their age, disability or a specific social or economic situation, with the objective, or the effect, of materially distorting the behaviour of that person or a person belonging to that group in a manner that causes or is reasonably likely to cause that person or another person significant harm; (c) the placing on the market, the putting into service or the use of AI systems for the evaluation or classification of natural persons or groups of persons over a certain period of time based on their social behaviour or known, inferred or predicted personal or personality characteristics, with the social score leading to either or both of the following: (i) detrimental or unfavourable treatment of certain natural persons or groups of persons in social contexts that are unrelated to the contexts in which the data was originally generated or collected; (ii) detrimental or unfavourable treatment of certain natural persons or groups of persons that is unjustified or disproportionate to their social behaviour or its gravity; (d) the placing on the market, the putting into service for this specific purpose, or the use of an AI system for making risk assessments of natural persons in order to assess or predict the risk of a natural person committing a criminal offence, based solely on the profiling of a natural person or on assessing their personality traits and characteristics; this prohibition shall not apply to AI systems used to support the human assessment of the involvement of a person in a criminal activity, which is already based on objective and verifiable facts directly linked to a criminal activity; (e) the placing on the market, the putting into service for this specific purpose, or the use of AI systems that create or expand facial recognition databases through the untargeted scraping of facial images from the internet or CCTV footage; (f) the placing on the market, the putting into service for this specific purpose, or the use of AI systems to infer emotions of a natural person in the areas of workplace and education institutions, except where the use of the AI system is intended to be put in place or into the market for medical or safety reasons; (g) the placing on the market, the putting into service for this specific purpose, or the use of biometric categorisation systems that categorise individually natural persons based on their biometric data to deduce or infer their race, political opinions, trade union membership, religious or philosophical beliefs, sex life or sexual orientation; this prohibition does not cover any labelling or filtering of lawfully acquired biometric datasets, such as images, based on biometric data or categorizing of biometric data in the area of law enforcement; (h) the use of 'real-time' remote biometric identification systems in publicly accessible spaces for the purposes of law enforcement, unless and in so far as such use is strictly necessary for one of the following objectives: (i) the targeted search for specific victims of abduction, trafficking in human beings or sexual exploitation of human beings, as well as the search for missing persons; (ii) the prevention of a specific, substantial and imminent threat to the life or physical safety of natural persons or a genuine and present or genuine and foreseeable threat of a terrorist attack; (iii) the localisation or identification of a person suspected of having committed a criminal offence, for the purpose of conducting a criminal investigation or prosecution or executing a criminal penalty for offences referred to in Annex II and punishable in the Member State concerned by a custodial sentence or a detention order for a maximum period of at least four years. Point (h) of the first subparagraph is without prejudice to Article 9 of Regulation (EU) 2016/679 for the processing of biometric data for purposes other than law enforcement.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.

5 passages for: GDPR automated individual decision-making profiling recruitment

[1] GDPR Article 22(1)-(2) (similarity 0.816)
GDPR Article 22(1)-(2) - Automated individual decision-making, including profiling
1. The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her. 2. Paragraph 1 shall not apply if the decision: (a) is necessary for entering into, or performance of, a contract between the data subject and a data controller; (b) is authorised by Union or Member State law to which the controller is subject and which also lays down suitable measures to safeguard the data subject's rights and freedoms and legitimate interests; or (c) is based on the data subject's explicit consent.

[2] GDPR Article 22(3)-(4) (similarity 0.790)
GDPR Article 22(3)-(4) - Automated individual decision-making, including profiling
3. In the cases referred to in points (a) and (c) of paragraph 2, the data controller shall implement suitable measures to safeguard the data subject's rights and freedoms and legitimate interests, at least the right to obtain human intervention on the part of the controller, to express his or her point of view and to contest the decision. 4. Decisions referred to in paragraph 2 shall not be based on special categories of personal data referred to in Article 9(1), unless point (a) or (g) of Article 9(2) applies and suitable measures to safeguard the data subject's rights and freedoms and legitimate interests are in place.

[3] GDPR Article 4, points (3) to (5) (similarity 0.771)
GDPR Article 4, points (3) to (5) - Definitions
(3) 'restriction of processing' means the marking of stored personal data with the aim of limiting their processing in the future; (4) 'profiling' means any form of automated processing of personal data consisting of the use of personal data to evaluate certain personal aspects relating to a natural person, in particular to analyse or predict aspects concerning that natural person's performance at work, economic situation, health, personal preferences, interests, reliability, behaviour, location or movements; (5) 'pseudonymisation' means the processing of personal data in such a manner that the personal data can no longer be attributed to a specific data subject without the use of additional information, provided that such additional information is kept separately and is subject to technical and organisational measures to ensure that the personal data are not attributed to an identified or identifiable natural person;

[4] GDPR Article 4, points intro to (2) (similarity 0.761)
GDPR Article 4, points intro to (2) - Definitions
For the purposes of this Regulation: (1) 'personal data' means any information relating to an identified or identifiable natural person ('data subject'); an identifiable natural person is one who can be identified, directly or indirectly, in particular by reference to an identifier such as a name, an identification number, location data, an online identifier or to one or more factors specific to the physical, physiological, genetic, mental, economic, cultural or social identity of that natural person; (2) 'processing' means any operation or set of operations which is performed on personal data or on sets of personal data, whether or not by automated means, such as collection, recording, organisation, structuring, storage, adaptation or alteration, retrieval, consultation, use, disclosure by transmission, dissemination or otherwise making available, alignment or combination, restriction, erasure or destruction;

[5] GDPR Article 88(1) (similarity 0.760)
GDPR Article 88(1) - Processing in the context of employment
1. Member States may, by law or by collective agreements, provide for more specific rules to ensure the protection of the rights and freedoms in respect of the processing of employees' personal data in the employment context, in particular for the purposes of the recruitment, the performance of the contract of employment, including discharge of obligations laid down by law or by collective agreements, management, planning and organisation of work, equality and diversity in the workplace, health and safety at work, protection of employer's or customer's property and for the purposes of the exercise and enjoyment, on an individual or collective basis, of rights and benefits related to employment, and for the purpose of the termination of the employment relationship.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q20 (multi)

**Question.** We are a lender about to use an AI system to score customers' creditworthiness with their personal data. Which impact assessments do we have to run first?

**Reference.** A data protection impact assessment is required for high-risk processing of personal data, and deployers of credit-scoring high-risk AI must also do a fundamental rights impact assessment, which complements any DPIA already done (Art. 27(4)). *(expected: GDPR;AI Act Article 35(1);Article 27(1))*

**Agent answer.**

As a lender using an AI system to evaluate creditworthiness and establish credit scores, your system is classified as a high-risk AI system under AI Act Annex III, point 5(b), which requires you to run specific impact assessments prior to deployment:

* **Fundamental Rights Impact Assessment (FRIA):** Prior to deploying the high-risk AI system, you must conduct an assessment of the impact on fundamental rights, covering your processes, intended use period, affected groups, specific risks of harm, human oversight measures, and internal risk-management mechanisms.
* **Data Protection Impact Assessment (DPIA):** Because credit scoring involves a systematic and extensive evaluation of personal aspects based on automated processing (profiling) that produces legal or similarly significant effects, you must also carry out a DPIA prior to the processing under GDPR Article 35.
* **Complementary Assessment:** If your obligations for the fundamental rights impact assessment are already met through your GDPR data protection impact assessment, the fundamental rights impact assessment can complement it.
* **Notification to Authorities:** Once you have performed the fundamental rights impact assessment, you must notify the national market surveillance authority of its results by submitting the completed assessment template.
* **DPO Involvement:** You must seek the advice of your data protection officer (if designated) when carrying out the data protection impact assessment.

**Cited:** AI Act Annex III, GDPR Article 35  
**Retrieved:** AI Act Annex III, AI Act Article 27, AI Act Article 77, GDPR Article 35

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: fundamental rights impact assessment AI system creditworthiness credit scoring AI Act

[1] AI Act Article 27(1) (similarity 0.790)
AI Act Article 27(1) - Fundamental rights impact assessment for high-risk AI systems
1. Prior to deploying a high-risk AI system referred to in Article 6(2), with the exception of high-risk AI systems intended to be used in the area listed in point 2 of Annex III, deployers that are bodies governed by public law, or are private entities providing public services, and deployers of high-risk AI systems referred to in points 5 (b) and (c) of Annex III, shall perform an assessment of the impact on fundamental rights that the use of such system may produce. For that purpose, deployers shall perform an assessment consisting of: (a) a description of the deployer's processes in which the high-risk AI system will be used in line with its intended purpose; (b) a description of the period of time within which, and the frequency with which, each high-risk AI system is intended to be used; (c) the categories of natural persons and groups likely to be affected by its use in the specific context; (d) the specific risks of harm likely to have an impact on the categories of natural persons or groups of persons identified pursuant to point (c) of this paragraph, taking into account the information given by the provider pursuant to Article 13; (e) a description of the implementation of human oversight measures, according to the instructions for use; (f) the measures to be taken in the case of the materialisation of those risks, including the arrangements for internal governance and complaint mechanisms.

[2] AI Act Annex III, points (4) to (5) (similarity 0.776)
AI Act Annex III, points (4) to (5) - High-risk AI systems referred to in Article 6(2)
4. Employment, workers' management and access to self-employment: (a) AI systems intended to be used for the recruitment or selection of natural persons, in particular to place targeted job advertisements, to analyse and filter job applications, and to evaluate candidates; (b) AI systems intended to be used to make decisions affecting terms of work-related relationships, the promotion or termination of work-related contractual relationships, to allocate tasks based on individual behaviour or personal traits or characteristics or to monitor and evaluate the performance and behaviour of persons in such relationships. 5. Access to and enjoyment of essential private services and essential public services and benefits: (a) AI systems intended to be used by public authorities or on behalf of public authorities to evaluate the eligibility of natural persons for essential public assistance benefits and services, including healthcare services, as well as to grant, reduce, revoke, or reclaim such benefits and services; (b) AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score, with the exception of AI systems used for the purpose of detecting financial fraud; (c) AI systems intended to be used for risk assessment and pricing in relation to natural persons in the case of life and health insurance; (d) AI systems intended to evaluate and classify emergency calls by natural persons or to be used to dispatch, or to establish priority in the dispatching of, emergency first response services, including by police, firefighters and medical aid, as well as of emergency healthcare patient triage systems.

[3] AI Act Article 27(4)-(5) (similarity 0.766)
AI Act Article 27(4)-(5) - Fundamental rights impact assessment for high-risk AI systems
4. If any of the obligations laid down in this Article is already met through the data protection impact assessment conducted pursuant to Article 35 of Regulation (EU) 2016/679 or Article 27 of Directive (EU) 2016/680, the fundamental rights impact assessment referred to in paragraph 1 of this Article shall complement that data protection impact assessment. 5. The AI Office shall develop a template for a questionnaire, including through an automated tool, to facilitate deployers in complying with their obligations under this Article in a simplified manner.

[4] AI Act Article 27(2)-(3) (similarity 0.762)
AI Act Article 27(2)-(3) - Fundamental rights impact assessment for high-risk AI systems
2. The obligation laid down in paragraph 1 applies to the first use of the high-risk AI system. The deployer may, in similar cases, rely on previously conducted fundamental rights impact assessments or existing impact assessments carried out by provider. If, during the use of the high-risk AI system, the deployer considers that any of the elements listed in paragraph 1 has changed or is no longer up to date, the deployer shall take the necessary steps to update the information. 3. Once the assessment referred to in paragraph 1 of this Article has been performed, the deployer shall notify the market surveillance authority of its results, submitting the filled-out template referred to in paragraph 5 of this Article as part of the notification. In the case referred to in Article 46(1), deployers may be exempt from that obligation to notify.

[5] AI Act Article 77(1)-(2) (similarity 0.754)
AI Act Article 77(1)-(2) - Powers of authorities protecting fundamental rights
1. National public authorities or bodies which supervise or enforce the respect of obligations under Union law protecting fundamental rights, including the right to non-discrimination, in relation to the use of high-risk AI systems referred to in Annex III shall have the power to request and access any documentation created or maintained under this Regulation in accessible language and format when access to that documentation is necessary for effectively fulfilling their mandates within the limits of their jurisdiction. The relevant public authority or body shall inform the market surveillance authority of the Member State concerned of any such request. 2. By 2 November 2024, each Member State shall identify the public authorities or bodies referred to in paragraph 1 and make a list of them publicly available. Member States shall notify the list to the Commission and to the other Member States, and shall keep the list up to date.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.

5 passages for: data protection impact assessment credit scoring GDPR Article 35

[1] GDPR Article 35(1)-(2) (similarity 0.795)
GDPR Article 35(1)-(2) - Data protection impact assessment
1. Where a type of processing in particular using new technologies, and taking into account the nature, scope, context and purposes of the processing, is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall, prior to the processing, carry out an assessment of the impact of the envisaged processing operations on the protection of personal data. A single assessment may address a set of similar processing operations that present similar high risks. 2. The controller shall seek the advice of the data protection officer, where designated, when carrying out a data protection impact assessment.

[2] GDPR Article 35(3) (similarity 0.783)
GDPR Article 35(3) - Data protection impact assessment
3. A data protection impact assessment referred to in paragraph 1 shall in particular be required in the case of: (a) a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person; (b) processing on a large scale of special categories of data referred to in Article 9(1), or of personal data relating to criminal convictions and offences referred to in Article 10; or (c) a systematic monitoring of a publicly accessible area on a large scale.

[3] GDPR Article 35(7) (similarity 0.774)
GDPR Article 35(7) - Data protection impact assessment
7. The assessment shall contain at least: (a) a systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitimate interest pursued by the controller; (b) an assessment of the necessity and proportionality of the processing operations in relation to the purposes; (c) an assessment of the risks to the rights and freedoms of data subjects referred to in paragraph 1; and (d) the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned.

[4] GDPR Article 35(8)-(11) (similarity 0.761)
GDPR Article 35(8)-(11) - Data protection impact assessment
8. Compliance with approved codes of conduct referred to in Article 40 by the relevant controllers or processors shall be taken into due account in assessing the impact of the processing operations performed by such controllers or processors, in particular for the purposes of a data protection impact assessment. 9. Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to the protection of commercial or public interests or the security of processing operations. 10. Where processing pursuant to point (c) or (e) of Article 6(1) has a legal basis in Union law or in the law of the Member State to which the controller is subject, that law regulates the specific processing operation or set of operations in question, and a data protection impact assessment has already been carried out as part of a general impact assessment in the context of the adoption of that legal basis, paragraphs 1 to 7 shall not apply unless Member States deem it to be necessary to carry out such an assessment prior to processing activities. 11. Where necessary, the controller shall carry out a review to assess if processing is performed in accordance with the data protection impact assessment at least when there is a change of the risk represented by processing operations.

[5] GDPR Article 35(4)-(6) (similarity 0.757)
GDPR Article 35(4)-(6) - Data protection impact assessment
4. The supervisory authority shall establish and make public a list of the kind of processing operations which are subject to the requirement for a data protection impact assessment pursuant to paragraph 1. The supervisory authority shall communicate those lists to the Board referred to in Article 68. 5. The supervisory authority may also establish and make public a list of the kind of processing operations for which no data protection impact assessment is required. The supervisory authority shall communicate those lists to the Board. 6. Prior to the adoption of the lists referred to in paragraphs 4 and 5, the competent supervisory authority shall apply the consistency mechanism referred to in Article 63 where such lists involve processing activities which are related to the offering of goods or services to data subjects or to the monitoring of their behaviour in several Member States, or may substantially affect the free movement of personal data within the Union.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q21 (multi)

**Question.** A customer who rents out flats with our smart appliances asks for all the usage data, which also shows what their tenants do. Can we hand it over, and what would justify sharing the tenants' data?

**Reference.** Only if there is a valid legal basis under GDPR Art. 6 for the tenants' personal data (and Art. 9 conditions where relevant), as Data Act Art. 4(12) requires; Art. 6(1) lists the bases, e.g. the tenants' consent or legitimate interests not overridden by their rights. *(expected: Data Act;GDPR Article 4(12);Article 6(1))*

**Agent answer.**

The indexed legislation does not cover this question in full, as specific criteria regarding who qualifies as the "user" under the Data Act for rented smart appliances are not detailed in the retrieved passages. However, sharing personal data relating to tenants requires a valid legal basis under the GDPR.

* Personal data generated by the use of a connected product where the user is not the data subject can only be made available to a third party if there is a valid legal basis for processing under GDPR Article 6 (and Article 9 where relevant). Data Act Article 5(7)
* Processing of personal data is lawful only if at least one condition applies, such as the data subject's consent, performance of a contract, compliance with a legal obligation, protection of vital interests, a public interest task, or a legitimate interest pursued by the controller or a third party (unless overridden by the data subject's rights). GDPR Article 6(1)

**Cited:** Data Act Article 5, GDPR Article 6  
**Retrieved:** Data Act Article 1, Data Act Article 3, Data Act Article 4, Data Act Article 5, Data Act Article 6, GDPR Article 29, GDPR Article 4, GDPR Article 5, GDPR Article 6

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: Data Act making data available user tenant smart appliances customer sharing

[1] Data Act Article 3(1)-(2) (similarity 0.826)
Data Act Article 3(1)-(2) - Obligation to make product data and related service data accessible to the user
1. Connected products shall be designed and manufactured, and related services shall be designed and provided, in such a manner that product data and related service data, including the relevant metadata necessary to interpret and use those data, are, by default, easily, securely, free of charge, in a comprehensive, structured, commonly used and machine-readable format, and, where relevant and technically feasible, directly accessible to the user. 2. Before concluding a contract for the purchase, rent or lease of a connected product, the seller, rentor or lessor, which may be the manufacturer, shall provide at least the following information to the user, in a clear and comprehensible manner: (a) the type, format and estimated volume of product data which the connected product is capable of generating; (b) whether the connected product is capable of generating data continuously and in real-time; (c) whether the connected product is capable of storing data on-device or on a remote server, including, where applicable, the intended duration of retention; (d) how the user may access, retrieve or, where relevant, erase the data, including the technical means to do so, as well as their terms of use and quality of service.

[2] Data Act Article 1(1) (similarity 0.804)
Data Act Article 1(1) - Subject matter and scope
1. This Regulation lays down harmonised rules, inter alia, on: (a) the making available of product data and related service data to the user of the connected product or related service; (b) the making available of data by data holders to data recipients; (c) the making available of data by data holders to public sector bodies, the Commission, the European Central Bank and Union bodies, where there is an exceptional need for those data for the performance of a specific task carried out in the public interest; (d) facilitating switching between data processing services; (e) introducing safeguards against unlawful third-party access to non-personal data; and (f) the development of interoperability standards for data to be accessed, transferred and used.

[3] Data Act Article 4(1)-(2) (similarity 0.804)
Data Act Article 4(1)-(2) - The rights and obligations of users and data holders with regard to access, use and making available product data and related service data
1. Where data cannot be directly accessed by the user from the connected product or related service, data holders shall make readily available data, as well as the relevant metadata necessary to interpret and use those data, accessible to the user without undue delay, of the same quality as is available to the data holder, easily, securely, free of charge, in a comprehensive, structured, commonly used and machine-readable format and, where relevant and technically feasible, continuously and in real-time. This shall be done on the basis of a simple request through electronic means where technically feasible. 2. Users and data holders may contractually restrict or prohibit accessing, using or further sharing data, if such processing could undermine security requirements of the connected product, as laid down by Union or national law, resulting in a serious adverse effect on the health, safety or security of natural persons. Sectoral authorities may provide users and data holders with technical expertise in that context. Where the data holder refuses to share data pursuant to this Article, it shall notify the competent authority designated pursuant to Article 37.

[4] Data Act Article 6 (similarity 0.794)
Data Act Article 6 - Obligations of third parties receiving data at the request of the user
1. A third party shall process the data made available to it pursuant to Article 5 only for the purposes and under the conditions agreed with the user and subject to Union and national law on the protection of personal data including the rights of the data subject insofar as personal data are concerned. The third party shall erase the data when they are no longer necessary for the agreed purpose, unless otherwise agreed with the user in relation to non-personal data. 2. The third party shall not: (a) make the exercise of choices or rights under Article 5 and this Article by the user unduly difficult, including by offering choices to the user in a non-neutral manner, or by coercing, deceiving or manipulating the user, or by subverting or impairing the autonomy, decision-making or choices of the user, including by means of a user digital interface or a part thereof; (b) notwithstanding Article 22(2), points (a) and (c), of Regulation (EU) 2016/679, use the data it receives for the profiling, unless it is necessary to provide the service requested by the user; (c) make the data it receives available to another third party, unless the data is made available on the basis of a contract with the user, and provided that the other third party takes all necessary measures agreed between the data holder and the third party to preserve the confidentiality of trade secrets; (d) make the data it receives available to an undertaking designated as a gatekeeper pursuant to Article 3 of Regulation (EU) 2022/1925; (e) use the data it receives to develop a product that competes with the connected product from which the accessed data originate or share the data with another third party for that purpose; third parties shall also not use any non-personal product data or related service data made available to them to derive insights about the economic situation, assets and production methods of, or use by, the data holder; (f) use the data it receives in a manner that has an adverse impact on the security of the connected product or related service; (g) disregard the specific measures agreed with a data holder or with the trade secrets holder pursuant to Article 5(9) and undermine the confidentiality of trade secrets; (h) prevent the user that is a consumer, including on the basis of a contract, from making the data it receives available to other parties.

[5] Data Act Article 1(3) (similarity 0.794)
Data Act Article 1(3) - Subject matter and scope
3. This Regulation applies to: (a) manufacturers of connected products placed on the market in the Union and providers of related services, irrespective of the place of establishment of those manufacturers and providers; (b) users in the Union of connected products or related services as referred to in point (a); (c) data holders, irrespective of their place of establishment, that make data available to data recipients in the Union; (d) data recipients in the Union to whom data are made available; (e) public sector bodies, the Commission, the European Central Bank and Union bodies that request data holders to make data available where there is an exceptional need for those data for the performance of a specific task carried out in the public interest and to the data holders that provide those data in response to such request; (f) providers of data processing services, irrespective of their place of establishment, providing such services to customers in the Union; (g) participants in data spaces and vendors of applications using smart contracts and persons whose trade, business or profession involves the deployment of smart contracts for others in the context of executing an agreement.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.

5 passages for: GDPR lawfulness of processing sharing usage data customer tenant flats

[1] GDPR Article 6(1) (similarity 0.803)
GDPR Article 6(1) - Lawfulness of processing
1. Processing shall be lawful only if and to the extent that at least one of the following applies: (a) the data subject has given consent to the processing of his or her personal data for one or more specific purposes; (b) processing is necessary for the performance of a contract to which the data subject is party or in order to take steps at the request of the data subject prior to entering into a contract; (c) processing is necessary for compliance with a legal obligation to which the controller is subject; (d) processing is necessary in order to protect the vital interests of the data subject or of another natural person; (e) processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller; (f) processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject which require protection of personal data, in particular where the data subject is a child. Point (f) of the first subparagraph shall not apply to processing carried out by public authorities in the performance of their tasks.

[2] GDPR Article 5 (similarity 0.757)
GDPR Article 5 - Principles relating to processing of personal data
1. Personal data shall be: (a) processed lawfully, fairly and in a transparent manner in relation to the data subject ('lawfulness, fairness and transparency'); (b) collected for specified, explicit and legitimate purposes and not further processed in a manner that is incompatible with those purposes; further processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes shall, in accordance with Article 89(1), not be considered to be incompatible with the initial purposes ('purpose limitation'); (c) adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed ('data minimisation'); (d) accurate and, where necessary, kept up to date; every reasonable step must be taken to ensure that personal data that are inaccurate, having regard to the purposes for which they are processed, are erased or rectified without delay ('accuracy'); (e) kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed; personal data may be stored for longer periods insofar as the personal data will be processed solely for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) subject to implementation of the appropriate technical and organisational measures required by this Regulation in order to safeguard the rights and freedoms of the data subject ('storage limitation'); (f) processed in a manner that ensures appropriate security of the personal data, including protection against unauthorised or unlawful processing and against accidental loss, destruction or damage, using appropriate technical or organisational measures ('integrity and confidentiality'). 2. The controller shall be responsible for, and be able to demonstrate compliance with, paragraph 1 ('accountability').

[3] GDPR Article 29 (similarity 0.752)
GDPR Article 29 - Processing under the authority of the controller or processor
The processor and any person acting under the authority of the controller or of the processor, who has access to personal data, shall not process those data except on instructions from the controller, unless required to do so by Union or Member State law.

[4] Data Act Article 5(6)-(7) (similarity 0.744)
Data Act Article 5(6)-(7) - Right of the user to share data with third parties
6. A data holder shall not use any readily available data to derive insights about the economic situation, assets and production methods of, or the use by, the third party in any other manner that could undermine the commercial position of the third party on the markets in which the third party is active, unless the third party has given permission to such use and has the technical possibility to easily withdraw that permission at any time. 7. Where the user is not the data subject whose personal data is requested, any personal data generated by the use of a connected product or related service shall be made available by the data holder to the third party only where there is a valid legal basis for processing under Article 6 of Regulation (EU) 2016/679 and, where relevant, the conditions of Article 9 of that Regulation and of Article 5(3) of Directive 2002/58/EC are fulfilled.

[5] GDPR Article 4, points intro to (2) (similarity 0.744)
GDPR Article 4, points intro to (2) - Definitions
For the purposes of this Regulation: (1) 'personal data' means any information relating to an identified or identifiable natural person ('data subject'); an identifiable natural person is one who can be identified, directly or indirectly, in particular by reference to an identifier such as a name, an identification number, location data, an online identifier or to one or more factors specific to the physical, physiological, genetic, mental, economic, cultural or social identity of that natural person; (2) 'processing' means any operation or set of operations which is performed on personal data or on sets of personal data, whether or not by automated means, such as collection, recording, organisation, structuring, storage, adaptation or alteration, retrieval, consultation, use, disclosure by transmission, dissemination or otherwise making available, alignment or combination, restriction, erasure or destruction;

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q22 (multi)

**Question.** We want to use health data from our wellness app to personalise recommendations. What do we need in place?

**Reference.** We need a lawful basis under Art. 6(1) and, because health data is a special category, also one of the Art. 9(2) conditions, such as the user's explicit consent. *(expected: GDPR;GDPR Article 6(1);Article 9(2)(a))*

**Agent answer.**

To use health data for personalising recommendations, you generally need a lawful basis for processing personal data, and because health data is a special category, you must also meet one of the specific conditions that lift the general prohibition on processing it.

* Processing must be based on at least one lawful ground, such as the data subject's consent or necessity for the performance of a contract. GDPR Article 6(1)
* The processing of data concerning health is prohibited unless an exception applies, such as the data subject giving explicit consent for one or more specified purposes. GDPR Article 9(1)-(2)
* When processing is based on consent, you must be able to demonstrate that the data subject consented, and keep the request clearly distinguishable from other matters. GDPR Article 7(1)-(2)
* The data subject must be able to withdraw their consent at any time, and it must be as easy to withdraw as it is to give. GDPR Article 7(3)
* When assessing if consent is freely given, account must be taken of whether the service is made conditional on consent to data processing that is not necessary for the contract. GDPR Article 7(4)

The indexed legislation does not cover specific technical safeguards, sector-specific health regulations, or potential requirements under the AI Act if the recommendation system uses artificial intelligence. Check relevant national laws, sector guidelines, or consult a lawyer.

**Cited:** GDPR Article 6, GDPR Article 7, GDPR Article 9  
**Retrieved:** GDPR Article 4, GDPR Article 6, GDPR Article 7, GDPR Article 9

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: health data wellness app personal recommendations GDPR processing conditions

[1] GDPR Article 6(1) (similarity 0.749)
GDPR Article 6(1) - Lawfulness of processing
1. Processing shall be lawful only if and to the extent that at least one of the following applies: (a) the data subject has given consent to the processing of his or her personal data for one or more specific purposes; (b) processing is necessary for the performance of a contract to which the data subject is party or in order to take steps at the request of the data subject prior to entering into a contract; (c) processing is necessary for compliance with a legal obligation to which the controller is subject; (d) processing is necessary in order to protect the vital interests of the data subject or of another natural person; (e) processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller; (f) processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject which require protection of personal data, in particular where the data subject is a child. Point (f) of the first subparagraph shall not apply to processing carried out by public authorities in the performance of their tasks.

[2] GDPR Article 9(1)-(2) (similarity 0.744)
GDPR Article 9(1)-(2) - Processing of special categories of personal data
1. Processing of personal data revealing racial or ethnic origin, political opinions, religious or philosophical beliefs, or trade union membership, and the processing of genetic data, biometric data for the purpose of uniquely identifying a natural person, data concerning health or data concerning a natural person's sex life or sexual orientation shall be prohibited. 2. Paragraph 1 shall not apply if one of the following applies: (a) the data subject has given explicit consent to the processing of those personal data for one or more specified purposes, except where Union or Member State law provide that the prohibition referred to in paragraph 1 may not be lifted by the data subject; (b) processing is necessary for the purposes of carrying out the obligations and exercising specific rights of the controller or of the data subject in the field of employment and social security and social protection law in so far as it is authorised by Union or Member State law or a collective agreement pursuant to Member State law providing for appropriate safeguards for the fundamental rights and the interests of the data subject; (c) processing is necessary to protect the vital interests of the data subject or of another natural person where the data subject is physically or legally incapable of giving consent; (d) processing is carried out in the course of its legitimate activities with appropriate safeguards by a foundation, association or any other not-for-profit body with a political, philosophical, religious or trade union aim and on condition that the processing relates solely to the members or to former members of the body or to persons who have regular contact with it in connection with its purposes and that the personal data are not disclosed outside that body without the consent of the data subjects; (e) processing relates to personal data which are manifestly made public by the data subject; (f) processing is necessary for the establishment, exercise or defence of legal claims or whenever courts are acting in their judicial capacity; (g) processing is necessary for reasons of substantial public interest, on the basis of Union or Member State law which shall be proportionate to the aim pursued, respect the essence of the right to data protection and provide for suitable and specific measures to safeguard the fundamental rights and the interests of the data subject; (h) processing is necessary for the purposes of preventive or occupational medicine, for the assessment of the working capacity of the employee, medical diagnosis, the provision of health or social care or treatment or the management of health or social care systems and services on the basis of Union or Member State law or pursuant to contract with a health professional and subject to the conditions and safeguards referred to in paragraph 3; (i) processing is necessary for reasons of public interest in the area of public health, such as protecting against serious cross-border threats to health or ensuring high standards of quality and safety of health care and of medicinal products or medical devices, on the basis of Union or Member State law which provides for suitable and specific measures to safeguard the rights and freedoms of the data subject, in particular professional secrecy; (j) processing is necessary for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) based on Union or Member State law which shall be proportionate to the aim pursued, respect the essence of the right to data protection and provide for suitable and specific measures to safeguard the fundamental rights and the interests of the data subject.

[3] GDPR Article 4, points intro to (2) (similarity 0.732)
GDPR Article 4, points intro to (2) - Definitions
For the purposes of this Regulation: (1) 'personal data' means any information relating to an identified or identifiable natural person ('data subject'); an identifiable natural person is one who can be identified, directly or indirectly, in particular by reference to an identifier such as a name, an identification number, location data, an online identifier or to one or more factors specific to the physical, physiological, genetic, mental, economic, cultural or social identity of that natural person; (2) 'processing' means any operation or set of operations which is performed on personal data or on sets of personal data, whether or not by automated means, such as collection, recording, organisation, structuring, storage, adaptation or alteration, retrieval, consultation, use, disclosure by transmission, dissemination or otherwise making available, alignment or combination, restriction, erasure or destruction;

[4] GDPR Article 7(4) (similarity 0.716)
GDPR Article 7(4) - Conditions for consent
4. When assessing whether consent is freely given, utmost account shall be taken of whether, inter alia, the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

[5] GDPR Article 7(1)-(3) (similarity 0.714)
GDPR Article 7(1)-(3) - Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data. 2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding. 3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q23 (multi)

**Question.** Hackers leaked our customer database. Who do we have to tell, and when?

**Reference.** Tell the supervisory authority within 72 hours where feasible, and, if the breach is likely to result in a high risk to people's rights and freedoms, also tell the affected individuals without undue delay. *(expected: GDPR;GDPR Article 33(1);Article 34(1))*

**Agent answer.**

You must notify the competent supervisory authority without undue delay and, where feasible, within 72 hours of becoming aware of the breach, unless the breach is unlikely to result in a risk to individuals' rights and freedoms. If the breach is likely to result in a high risk to individuals, you must also communicate it to the affected data subjects without undue delay.

* As controller, notify the supervisory authority without undue delay and not later than 72 hours after becoming aware of the breach, unless it is unlikely to result in a risk to rights and freedoms. (GDPR Article 33(1))
* If you are a processor, you must notify the controller without undue delay after becoming aware of the breach. (GDPR Article 33(2))
* Communicate the breach to the data subject without undue delay when it is likely to result in a high risk to their rights and freedoms. (GDPR Article 34(1))
* The notification to the supervisory authority must include specific details such as the nature of the breach, categories and approximate numbers of data subjects and records concerned, and measures taken or proposed. (GDPR Article 33(3))
* Communication to data subjects is not required if the data was rendered unintelligible (e.g. encrypted), if subsequent measures ensure the high risk is no longer likely to materialise, or if it would involve disproportionate effort (in which case a public communication or similar measure must be used instead). (GDPR Article 34(3))

**Cited:** GDPR Article 33, GDPR Article 34  
**Retrieved:** GDPR Article 33, GDPR Article 34

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: personal data breach notification to supervisory authority and data subjects

[1] GDPR Article 33(1)-(2) (similarity 0.785)
GDPR Article 33(1)-(2) - Notification of a personal data breach to the supervisory authority
1. In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority competent in accordance with Article 55, unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where the notification to the supervisory authority is not made within 72 hours, it shall be accompanied by reasons for the delay. 2. The processor shall notify the controller without undue delay after becoming aware of a personal data breach.

[2] GDPR Article 33(3) (similarity 0.775)
GDPR Article 33(3) - Notification of a personal data breach to the supervisory authority
3. The notification referred to in paragraph 1 shall at least: (a) describe the nature of the personal data breach including where possible, the categories and approximate number of data subjects concerned and the categories and approximate number of personal data records concerned; (b) communicate the name and contact details of the data protection officer or other contact point where more information can be obtained; (c) describe the likely consequences of the personal data breach; (d) describe the measures taken or proposed to be taken by the controller to address the personal data breach, including, where appropriate, measures to mitigate its possible adverse effects.

[3] GDPR Article 34(1)-(3) (similarity 0.767)
GDPR Article 34(1)-(3) - Communication of a personal data breach to the data subject
1. When the personal data breach is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall communicate the personal data breach to the data subject without undue delay. 2. The communication to the data subject referred to in paragraph 1 of this Article shall describe in clear and plain language the nature of the personal data breach and contain at least the information and measures referred to in points (b), (c) and (d) of Article 33(3). 3. The communication to the data subject referred to in paragraph 1 shall not be required if any of the following conditions are met: (a) the controller has implemented appropriate technical and organisational protection measures, and those measures were applied to the personal data affected by the personal data breach, in particular those that render the personal data unintelligible to any person who is not authorised to access it, such as encryption; (b) the controller has taken subsequent measures which ensure that the high risk to the rights and freedoms of data subjects referred to in paragraph 1 is no longer likely to materialise; (c) it would involve disproportionate effort. In such a case, there shall instead be a public communication or similar measure whereby the data subjects are informed in an equally effective manner.

[4] GDPR Article 33(4)-(5) (similarity 0.757)
GDPR Article 33(4)-(5) - Notification of a personal data breach to the supervisory authority
4. Where, and in so far as, it is not possible to provide the information at the same time, the information may be provided in phases without undue further delay. 5. The controller shall document any personal data breaches, comprising the facts relating to the personal data breach, its effects and the remedial action taken. That documentation shall enable the supervisory authority to verify compliance with this Article.

[5] GDPR Article 34(4) (similarity 0.751)
GDPR Article 34(4) - Communication of a personal data breach to the data subject
4. If the controller has not already communicated the personal data breach to the data subject, the supervisory authority, having considered the likelihood of the personal data breach resulting in a high risk, may require it to do so or may decide that any of the conditions referred to in paragraph 3 are met.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q24 (multi)

**Question.** Can we send our EU customers' data to an analytics vendor outside the EU?

**Reference.** Yes, if the destination has a Commission adequacy decision, or otherwise if appropriate safeguards such as standard contractual clauses are in place with enforceable rights and effective remedies. *(expected: GDPR;GDPR Article 45(1);Article 46(1))*

**Agent answer.**

Yes, you can send EU customers' data to an analytics vendor outside the EU, provided that the transfer complies with Chapter V of the GDPR regarding international data transfers.

* Transfers may occur without specific authorization if the European Commission has decided that the third country ensures an adequate level of protection. (GDPR Article 45(1))
* In the absence of an adequacy decision, you may transfer data only if you provide appropriate safeguards—such as standard data protection clauses, binding corporate rules, or approved codes of conduct—along with enforceable data subject rights and effective legal remedies. (GDPR Article 46(1))
* Specific contractual clauses or administrative arrangements between authorities may also provide appropriate safeguards, subject to authorization from the competent supervisory authority where applicable. (GDPR Article 46(3))
* In the absence of an adequacy decision or appropriate safeguards, a transfer may occur under specific derogations, such as when the data subject has explicitly consented after being informed of the risks, or if the transfer is necessary for the performance of a contract between the data subject and the controller. (GDPR Article 49(1))
* Any foreign court judgment or administrative decision requiring a controller or processor to disclose personal data can only be recognized or enforced if based on an international agreement like a mutual legal assistance treaty in force between the requesting third country and the EU or a Member State. (GDPR Article 48)

**Cited:** GDPR Article 45, GDPR Article 46, GDPR Article 48, GDPR Article 49  
**Retrieved:** GDPR Article 44, GDPR Article 45, GDPR Article 46, GDPR Article 48, GDPR Article 49

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: transfer of personal data to a third country or international organisation GDPR

[1] GDPR Article 45(1)-(2) (similarity 0.820)
GDPR Article 45(1)-(2) - Transfers on the basis of an adequacy decision
1. A transfer of personal data to a third country or an international organisation may take place where the Commission has decided that the third country, a territory or one or more specified sectors within that third country, or the international organisation in question ensures an adequate level of protection. Such a transfer shall not require any specific authorisation. 2. When assessing the adequacy of the level of protection, the Commission shall, in particular, take account of the following elements: (a) the rule of law, respect for human rights and fundamental freedoms, relevant legislation, both general and sectoral, including concerning public security, defence, national security and criminal law and the access of public authorities to personal data, as well as the implementation of such legislation, data protection rules, professional rules and security measures, including rules for the onward transfer of personal data to another third country or international organisation which are complied with in that country or international organisation, case-law, as well as effective and enforceable data subject rights and effective administrative and judicial redress for the data subjects whose personal data are being transferred; (b) the existence and effective functioning of one or more independent supervisory authorities in the third country or to which an international organisation is subject, with responsibility for ensuring and enforcing compliance with the data protection rules, including adequate enforcement powers, for assisting and advising the data subjects in exercising their rights and for cooperation with the supervisory authorities of the Member States; and (c) the international commitments the third country or international organisation concerned has entered into, or other obligations arising from legally binding conventions or instruments as well as from its participation in multilateral or regional systems, in particular in relation to the protection of personal data.

[2] GDPR Article 49(1) (similarity 0.816)
GDPR Article 49(1) - Derogations for specific situations
1. In the absence of an adequacy decision pursuant to Article 45(3), or of appropriate safeguards pursuant to Article 46, including binding corporate rules, a transfer or a set of transfers of personal data to a third country or an international organisation shall take place only on one of the following conditions: (a) the data subject has explicitly consented to the proposed transfer, after having been informed of the possible risks of such transfers for the data subject due to the absence of an adequacy decision and appropriate safeguards; (b) the transfer is necessary for the performance of a contract between the data subject and the controller or the implementation of pre-contractual measures taken at the data subject's request; (c) the transfer is necessary for the conclusion or performance of a contract concluded in the interest of the data subject between the controller and another natural or legal person; (d) the transfer is necessary for important reasons of public interest; (e) the transfer is necessary for the establishment, exercise or defence of legal claims; (f) the transfer is necessary in order to protect the vital interests of the data subject or of other persons, where the data subject is physically or legally incapable of giving consent; (g) the transfer is made from a register which according to Union or Member State law is intended to provide information to the public and which is open to consultation either by the public in general or by any person who can demonstrate a legitimate interest, but only to the extent that the conditions laid down by Union or Member State law for consultation are fulfilled in the particular case. Where a transfer could not be based on a provision in Article 45 or 46, including the provisions on binding corporate rules, and none of the derogations for a specific situation referred to in the first subparagraph of this paragraph is applicable, a transfer to a third country or an international organisation may take place only if the transfer is not repetitive, concerns only a limited number of data subjects, is necessary for the purposes of compelling legitimate interests pursued by the controller which are not overridden by the interests or rights and freedoms of the data subject, and the controller has assessed all the circumstances surrounding the data transfer and has on the basis of that assessment provided suitable safeguards with regard to the protection of personal data. The controller shall inform the supervisory authority of the transfer. The controller shall, in addition to providing the information referred to in Articles 13 and 14, inform the data subject of the transfer and on the compelling legitimate interests pursued.

[3] GDPR Article 44 (similarity 0.811)
GDPR Article 44 - General principle for transfers
Any transfer of personal data which are undergoing processing or are intended for processing after transfer to a third country or to an international organisation shall take place only if, subject to the other provisions of this Regulation, the conditions laid down in this Chapter are complied with by the controller and processor, including for onward transfers of personal data from the third country or an international organisation to another third country or to another international organisation. All provisions in this Chapter shall be applied in order to ensure that the level of protection of natural persons guaranteed by this Regulation is not undermined.

[4] GDPR Article 49(4)-(6) (similarity 0.801)
GDPR Article 49(4)-(6) - Derogations for specific situations
4. The public interest referred to in point (d) of the first subparagraph of paragraph 1 shall be recognised in Union law or in the law of the Member State to which the controller is subject. 5. In the absence of an adequacy decision, Union or Member State law may, for important reasons of public interest, expressly set limits to the transfer of specific categories of personal data to a third country or an international organisation. Member States shall notify such provisions to the Commission. 6. The controller or processor shall document the assessment as well as the suitable safeguards referred to in the second subparagraph of paragraph 1 of this Article in the records referred to in Article 30.

[5] GDPR Article 48 (similarity 0.800)
GDPR Article 48 - Transfers or disclosures not authorised by Union law
Any judgment of a court or tribunal and any decision of an administrative authority of a third country requiring a controller or processor to transfer or disclose personal data may only be recognised or enforceable in any manner if based on an international agreement, such as a mutual legal assistance treaty, in force between the requesting third country and the Union or a Member State, without prejudice to other grounds for transfer pursuant to this Chapter.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.

5 passages for: appropriate safeguards transfer third country GDPR Article 46

[1] GDPR Article 46(1)-(2) (similarity 0.896)
GDPR Article 46(1)-(2) - Transfers subject to appropriate safeguards
1. In the absence of a decision pursuant to Article 45(3), a controller or processor may transfer personal data to a third country or an international organisation only if the controller or processor has provided appropriate safeguards, and on condition that enforceable data subject rights and effective legal remedies for data subjects are available. 2. The appropriate safeguards referred to in paragraph 1 may be provided for, without requiring any specific authorisation from a supervisory authority, by: (a) a legally binding and enforceable instrument between public authorities or bodies; (b) binding corporate rules in accordance with Article 47; (c) standard data protection clauses adopted by the Commission in accordance with the examination procedure referred to in Article 93(2); (d) standard data protection clauses adopted by a supervisory authority and approved by the Commission pursuant to the examination procedure referred to in Article 93(2); (e) an approved code of conduct pursuant to Article 40 together with binding and enforceable commitments of the controller or processor in the third country to apply the appropriate safeguards, including as regards data subjects' rights; or (f) an approved certification mechanism pursuant to Article 42 together with binding and enforceable commitments of the controller or processor in the third country to apply the appropriate safeguards, including as regards data subjects' rights.

[2] GDPR Article 46(3)-(5) (similarity 0.863)
GDPR Article 46(3)-(5) - Transfers subject to appropriate safeguards
3. Subject to the authorisation from the competent supervisory authority, the appropriate safeguards referred to in paragraph 1 may also be provided for, in particular, by: (a) contractual clauses between the controller or processor and the controller, processor or the recipient of the personal data in the third country or international organisation; or (b) provisions to be inserted into administrative arrangements between public authorities or bodies which include enforceable and effective data subject rights. 4. The supervisory authority shall apply the consistency mechanism referred to in Article 63 in the cases referred to in paragraph 3 of this Article. 5. Authorisations by a Member State or supervisory authority on the basis of Article 26(2) of Directive 95/46/EC shall remain valid until amended, replaced or repealed, if necessary, by that supervisory authority. Decisions adopted by the Commission on the basis of Article 26(4) of Directive 95/46/EC shall remain in force until amended, replaced or repealed, if necessary, by a Commission Decision adopted in accordance with paragraph 2 of this Article.

[3] GDPR Article 45(1)-(2) (similarity 0.834)
GDPR Article 45(1)-(2) - Transfers on the basis of an adequacy decision
1. A transfer of personal data to a third country or an international organisation may take place where the Commission has decided that the third country, a territory or one or more specified sectors within that third country, or the international organisation in question ensures an adequate level of protection. Such a transfer shall not require any specific authorisation. 2. When assessing the adequacy of the level of protection, the Commission shall, in particular, take account of the following elements: (a) the rule of law, respect for human rights and fundamental freedoms, relevant legislation, both general and sectoral, including concerning public security, defence, national security and criminal law and the access of public authorities to personal data, as well as the implementation of such legislation, data protection rules, professional rules and security measures, including rules for the onward transfer of personal data to another third country or international organisation which are complied with in that country or international organisation, case-law, as well as effective and enforceable data subject rights and effective administrative and judicial redress for the data subjects whose personal data are being transferred; (b) the existence and effective functioning of one or more independent supervisory authorities in the third country or to which an international organisation is subject, with responsibility for ensuring and enforcing compliance with the data protection rules, including adequate enforcement powers, for assisting and advising the data subjects in exercising their rights and for cooperation with the supervisory authorities of the Member States; and (c) the international commitments the third country or international organisation concerned has entered into, or other obligations arising from legally binding conventions or instruments as well as from its participation in multilateral or regional systems, in particular in relation to the protection of personal data.

[4] GDPR Article 49(1) (similarity 0.829)
GDPR Article 49(1) - Derogations for specific situations
1. In the absence of an adequacy decision pursuant to Article 45(3), or of appropriate safeguards pursuant to Article 46, including binding corporate rules, a transfer or a set of transfers of personal data to a third country or an international organisation shall take place only on one of the following conditions: (a) the data subject has explicitly consented to the proposed transfer, after having been informed of the possible risks of such transfers for the data subject due to the absence of an adequacy decision and appropriate safeguards; (b) the transfer is necessary for the performance of a contract between the data subject and the controller or the implementation of pre-contractual measures taken at the data subject's request; (c) the transfer is necessary for the conclusion or performance of a contract concluded in the interest of the data subject between the controller and another natural or legal person; (d) the transfer is necessary for important reasons of public interest; (e) the transfer is necessary for the establishment, exercise or defence of legal claims; (f) the transfer is necessary in order to protect the vital interests of the data subject or of other persons, where the data subject is physically or legally incapable of giving consent; (g) the transfer is made from a register which according to Union or Member State law is intended to provide information to the public and which is open to consultation either by the public in general or by any person who can demonstrate a legitimate interest, but only to the extent that the conditions laid down by Union or Member State law for consultation are fulfilled in the particular case. Where a transfer could not be based on a provision in Article 45 or 46, including the provisions on binding corporate rules, and none of the derogations for a specific situation referred to in the first subparagraph of this paragraph is applicable, a transfer to a third country or an international organisation may take place only if the transfer is not repetitive, concerns only a limited number of data subjects, is necessary for the purposes of compelling legitimate interests pursued by the controller which are not overridden by the interests or rights and freedoms of the data subject, and the controller has assessed all the circumstances surrounding the data transfer and has on the basis of that assessment provided suitable safeguards with regard to the protection of personal data. The controller shall inform the supervisory authority of the transfer. The controller shall, in addition to providing the information referred to in Articles 13 and 14, inform the data subject of the transfer and on the compelling legitimate interests pursued.

[5] GDPR Article 49(4)-(6) (similarity 0.810)
GDPR Article 49(4)-(6) - Derogations for specific situations
4. The public interest referred to in point (d) of the first subparagraph of paragraph 1 shall be recognised in Union law or in the law of the Member State to which the controller is subject. 5. In the absence of an adequacy decision, Union or Member State law may, for important reasons of public interest, expressly set limits to the transfer of specific categories of personal data to a third country or an international organisation. Member States shall notify such provisions to the Commission. 6. The controller or processor shall document the assessment as well as the suitable safeguards referred to in the second subparagraph of paragraph 1 of this Article in the records referred to in Article 30.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q25 (multi)

**Question.** Is an AI tool that grades students' exams considered high-risk?

**Reference.** Yes. Art. 6(2) treats the Annex III use cases as high-risk, and Annex III point 3(b) lists AI systems used to evaluate learning outcomes in education. *(expected: AI Act;AI Act Article 6(2);Annex III, point (3))*

**Agent answer.**

Yes, an AI tool that grades students' exams is considered high-risk because AI systems intended to be used to evaluate learning outcomes in educational and vocational training institutions are classified as high-risk under the AI Act.

* AI systems referred to in Annex III are considered to be high-risk. (AI Act Article 6(2))
* High-risk AI systems include those intended to be used to evaluate learning outcomes, including when those outcomes are used to steer the learning process of natural persons in educational and vocational training institutions at all levels. (AI Act Annex III, point 3(b))
* An AI system listed in Annex III is exempt from being high-risk if it does not pose a significant risk of harm and meets conditions such as performing a narrow procedural task or improving a previously completed human activity, unless it performs profiling. (AI Act Article 6(3))

**Cited:** AI Act Annex III, AI Act Article 6  
**Retrieved:** AI Act Annex III, AI Act Article 6

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: AI tool that grades students exams high-risk AI Act

[1] AI Act Annex III, points (2) to (3) (similarity 0.819)
AI Act Annex III, points (2) to (3) - High-risk AI systems referred to in Article 6(2)
2. Critical infrastructure: AI systems intended to be used as safety components in the management and operation of critical digital infrastructure, road traffic, or in the supply of water, gas, heating or electricity. 3. Education and vocational training: (a) AI systems intended to be used to determine access or admission or to assign natural persons to educational and vocational training institutions at all levels; (b) AI systems intended to be used to evaluate learning outcomes, including when those outcomes are used to steer the learning process of natural persons in educational and vocational training institutions at all levels; (c) AI systems intended to be used for the purpose of assessing the appropriate level of education that an individual will receive or will be able to access, in the context of or within educational and vocational training institutions at all levels; (d) AI systems intended to be used for monitoring and detecting prohibited behaviour of students during tests in the context of or within educational and vocational training institutions at all levels.

[2] AI Act Annex III, point (7) (similarity 0.787)
AI Act Annex III, point (7) - High-risk AI systems referred to in Article 6(2)
7. Migration, asylum and border control management, in so far as their use is permitted under relevant Union or national law: (a) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies as polygraphs or similar tools; (b) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies to assess a risk, including a security risk, a risk of irregular migration, or a health risk, posed by a natural person who intends to enter or who has entered into the territory of a Member State; (c) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies to assist competent public authorities for the examination of applications for asylum, visa or residence permits and for associated complaints with regard to the eligibility of the natural persons applying for a status, including related assessments of the reliability of evidence; (d) AI systems intended to be used by or on behalf of competent public authorities, or by Union institutions, bodies, offices or agencies, in the context of migration, asylum or border control management, for the purpose of detecting, recognising or identifying natural persons, with the exception of the verification of travel documents.

[3] AI Act Article 6(2)-(3) (similarity 0.786)
AI Act Article 6(2)-(3) - Classification rules for high-risk AI systems
2. In addition to the high-risk AI systems referred to in paragraph 1, AI systems referred to in Annex III shall be considered to be high-risk. 3. By derogation from paragraph 2, an AI system referred to in Annex III shall not be considered to be high-risk where it does not pose a significant risk of harm to the health, safety or fundamental rights of natural persons, including by not materially influencing the outcome of decision making. The first subparagraph shall apply where any of the following conditions is fulfilled: (a) the AI system is intended to perform a narrow procedural task; (b) the AI system is intended to improve the result of a previously completed human activity; (c) the AI system is intended to detect decision-making patterns or deviations from prior decision-making patterns and is not meant to replace or influence the previously completed human assessment, without proper human review; or (d) the AI system is intended to perform a preparatory task to an assessment relevant for the purposes of the use cases listed in Annex III. Notwithstanding the first subparagraph, an AI system referred to in Annex III shall always be considered to be high-risk where the AI system performs profiling of natural persons.

[4] AI Act Annex III, points (4) to (5) (similarity 0.783)
AI Act Annex III, points (4) to (5) - High-risk AI systems referred to in Article 6(2)
4. Employment, workers' management and access to self-employment: (a) AI systems intended to be used for the recruitment or selection of natural persons, in particular to place targeted job advertisements, to analyse and filter job applications, and to evaluate candidates; (b) AI systems intended to be used to make decisions affecting terms of work-related relationships, the promotion or termination of work-related contractual relationships, to allocate tasks based on individual behaviour or personal traits or characteristics or to monitor and evaluate the performance and behaviour of persons in such relationships. 5. Access to and enjoyment of essential private services and essential public services and benefits: (a) AI systems intended to be used by public authorities or on behalf of public authorities to evaluate the eligibility of natural persons for essential public assistance benefits and services, including healthcare services, as well as to grant, reduce, revoke, or reclaim such benefits and services; (b) AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score, with the exception of AI systems used for the purpose of detecting financial fraud; (c) AI systems intended to be used for risk assessment and pricing in relation to natural persons in the case of life and health insurance; (d) AI systems intended to evaluate and classify emergency calls by natural persons or to be used to dispatch, or to establish priority in the dispatching of, emergency first response services, including by police, firefighters and medical aid, as well as of emergency healthcare patient triage systems.

[5] AI Act Article 6(1) (similarity 0.773)
AI Act Article 6(1) - Classification rules for high-risk AI systems
1. Irrespective of whether an AI system is placed on the market or put into service independently of the products referred to in points (a) and (b), that AI system shall be considered to be high-risk where both of the following conditions are fulfilled: (a) the AI system is intended to be used as a safety component of a product, or the AI system is itself a product, covered by the Union harmonisation legislation listed in Annex I; (b) the product whose safety component pursuant to point (a) is the AI system, or the AI system itself as a product, is required to undergo a third-party conformity assessment, with a view to the placing on the market or the putting into service of that product pursuant to the Union harmonisation legislation listed in Annex I.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q26 (multi)

**Question.** We think our AI tool, although used in a sensitive area, is not really high-risk. Do we have to write that down or register anything?

**Reference.** Yes. A provider who concludes an Annex III system is not high-risk must document that assessment before placing it on the market and register the system in the EU database. *(expected: AI Act;AI Act Article 6(4);Article 49(2))*

**Agent answer.**

Yes, if you consider that your AI system falls under an area listed in Annex III but is not high-risk, you must document your assessment before placing it on the market or putting it into service, and you are subject to a registration obligation.

* A provider who considers that an AI system referred to in Annex III is not high-risk must document its assessment before placing it on the market or putting it into service. AI Act Article 6(4)
* You are subject to the registration obligation set out in Article 49(2). AI Act Article 6(4)
* Upon request of national competent authorities, you must provide the documentation of the assessment. AI Act Article 6(4)
* The registration includes the condition or conditions under Article 6(3) based on which the system is considered not-high-risk. AI Act Annex VIII, point 6
* The registration also includes a short summary of the grounds on which the AI system is considered to be not-high-risk in application of the procedure under Article 6(3). AI Act Annex VIII, point 7

**Cited:** AI Act Annex VIII, AI Act Article 6  
**Retrieved:** AI Act Annex IV, AI Act Annex VIII, AI Act Article 6

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: AI Act high risk exception assessment documentation registration

[1] AI Act Annex VIII, points (3) to (5) (similarity 0.829)
AI Act Annex VIII, points (3) to (5) - Information to be submitted upon the registration of high-risk AI systems in accordance with Article 49
3. The URL of the entry of the AI system in the EU database by its provider; 4. A summary of the findings of the fundamental rights impact assessment conducted in accordance with Article 27; 5. A summary of the data protection impact assessment carried out in accordance with Article 35 of Regulation (EU) 2016/679 or Article 27 of Directive (EU) 2016/680 as specified in Article 26(8) of this Regulation, where applicable.

[2] AI Act Annex IV, points (4) to (7) (similarity 0.823)
AI Act Annex IV, points (4) to (7) - Technical documentation referred to in Article 11(1)
4. A description of the appropriateness of the performance metrics for the specific AI system; 5. A detailed description of the risk management system in accordance with Article 9; 6. A description of relevant changes made by the provider to the system through its lifecycle; 7. A list of the harmonised standards applied in full or in part the references of which have been published in the Official Journal of the European Union; where no such harmonised standards have been applied, a detailed description of the solutions adopted to meet the requirements set out in Chapter III, Section 2, including a list of other relevant standards and technical specifications applied;

[3] AI Act Annex VIII, points (1) to (7) (similarity 0.817)
AI Act Annex VIII, points (1) to (7) - Information to be submitted upon the registration of high-risk AI systems in accordance with Article 49
1. The name, address and contact details of the provider; 2. Where submission of information is carried out by another person on behalf of the provider, the name, address and contact details of that person; 3. The name, address and contact details of the authorised representative, where applicable; 4. The AI system trade name and any additional unambiguous reference allowing the identification and traceability of the AI system; 5. A description of the intended purpose of the AI system; 6. The condition or conditions under Article 6(3)based on which the AI system is considered to be not-high-risk; 7. A short summary of the grounds on which the AI system is considered to be not-high-risk in application of the procedure under Article 6(3);

[4] AI Act Annex VIII, points (5) to (9) (similarity 0.813)
AI Act Annex VIII, points (5) to (9) - Information to be submitted upon the registration of high-risk AI systems in accordance with Article 49
5. A description of the intended purpose of the AI system and of the components and functions supported through this AI system; 6. A basic and concise description of the information used by the system (data, inputs) and its operating logic; 7. The status of the AI system (on the market, or in service; no longer placed on the market/in service, recalled); 8. The type, number and expiry date of the certificate issued by the notified body and the name or identification number of that notified body, where applicable; 9. A scanned copy of the certificate referred to in point 8, where applicable;

[5] AI Act Article 6(4)-(5) (similarity 0.813)
AI Act Article 6(4)-(5) - Classification rules for high-risk AI systems
4. A provider who considers that an AI system referred to in Annex III is not high-risk shall document its assessment before that system is placed on the market or put into service. Such provider shall be subject to the registration obligation set out in Article 49(2). Upon request of national competent authorities, the provider shall provide the documentation of the assessment. 5. The Commission shall, after consulting the European Artificial Intelligence Board (the 'Board'), and no later than 2 February 2026, provide guidelines specifying the practical implementation of this Article in line with Article 96 together with a comprehensive list of practical examples of use cases of AI systems that are high-risk and not high-risk.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q27 (multi)

**Question.** Our customer wants us to send their machine data straight to a huge tech platform of the kind regulated as a gatekeeper. Do we have to?

**Reference.** Art. 5(1) obliges us to share data with a third party chosen by the user, but under Art. 5(3) an undertaking designated as a gatekeeper is not an eligible third party. *(expected: Data Act;Data Act Article 5(1);Article 5(3))*

**Agent answer.**

No, you do not have to (and cannot) send the machine data straight to a designated gatekeeper under a user request, because gatekeepers are explicitly barred from being eligible third parties to receive data under these provisions.

* Any undertaking designated as a gatekeeper pursuant to Article 3 of Regulation (EU) 2022/1925 shall not be an eligible third party under the Data Act's data-sharing provisions and must not receive data from a user that the user obtained via a data access request. Data Act Article 5(3)
* A designated gatekeeper is prohibited from soliciting or commercially incentivizing a user to make data available to one of its services, or soliciting a user to request a data holder to make data available to the gatekeeper. Data Act Article 5(3)

**Cited:** Data Act Article 5  
**Retrieved:** Data Act Article 3, Data Act Article 5, Data Act Article 6, Data Act Article 8

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: gatekeeper make available data third party Data Act

[1] Data Act Article 5(2)-(3) (similarity 0.821)
Data Act Article 5(2)-(3) - Right of the user to share data with third parties
2. Paragraph 1 shall not apply to readily available data in the context of the testing of new connected products, substances or processes that are not yet placed on the market unless their use by a third party is contractually permitted. 3. Any undertaking designated as a gatekeeper, pursuant to Article 3 of Regulation (EU) 2022/1925, shall not be an eligible third party under this Article and therefore shall not: (a) solicit or commercially incentivise a user in any manner, including by providing monetary or any other compensation, to make data available to one of its services that the user has obtained pursuant to a request under Article 4(1); (b) solicit or commercially incentivise a user to request the data holder to make data available to one of its services pursuant to paragraph 1 of this Article; (c) receive data from a user that the user has obtained pursuant to a request under Article 4(1).

[2] Data Act Article 6 (similarity 0.816)
Data Act Article 6 - Obligations of third parties receiving data at the request of the user
1. A third party shall process the data made available to it pursuant to Article 5 only for the purposes and under the conditions agreed with the user and subject to Union and national law on the protection of personal data including the rights of the data subject insofar as personal data are concerned. The third party shall erase the data when they are no longer necessary for the agreed purpose, unless otherwise agreed with the user in relation to non-personal data. 2. The third party shall not: (a) make the exercise of choices or rights under Article 5 and this Article by the user unduly difficult, including by offering choices to the user in a non-neutral manner, or by coercing, deceiving or manipulating the user, or by subverting or impairing the autonomy, decision-making or choices of the user, including by means of a user digital interface or a part thereof; (b) notwithstanding Article 22(2), points (a) and (c), of Regulation (EU) 2016/679, use the data it receives for the profiling, unless it is necessary to provide the service requested by the user; (c) make the data it receives available to another third party, unless the data is made available on the basis of a contract with the user, and provided that the other third party takes all necessary measures agreed between the data holder and the third party to preserve the confidentiality of trade secrets; (d) make the data it receives available to an undertaking designated as a gatekeeper pursuant to Article 3 of Regulation (EU) 2022/1925; (e) use the data it receives to develop a product that competes with the connected product from which the accessed data originate or share the data with another third party for that purpose; third parties shall also not use any non-personal product data or related service data made available to them to derive insights about the economic situation, assets and production methods of, or use by, the data holder; (f) use the data it receives in a manner that has an adverse impact on the security of the connected product or related service; (g) disregard the specific measures agreed with a data holder or with the trade secrets holder pursuant to Article 5(9) and undermine the confidentiality of trade secrets; (h) prevent the user that is a consumer, including on the basis of a contract, from making the data it receives available to other parties.

[3] Data Act Article 5(1) (similarity 0.815)
Data Act Article 5(1) - Right of the user to share data with third parties
1. Upon request by a user, or by a party acting on behalf of a user, the data holder shall make available readily available data, as well as the relevant metadata necessary to interpret and use those data, to a third party without undue delay, of the same quality as is available to the data holder, easily, securely, free of charge to the user, in a comprehensive, structured, commonly used and machine-readable format and, where relevant and technically feasible, continuously and in real-time. The data shall be made available by the data holder to the third party in accordance with Articles 8 and 9.

[4] Data Act Article 8(3)-(4) (similarity 0.797)
Data Act Article 8(3)-(4) - Conditions under which data holders make data available to data recipients
3. A data holder shall not discriminate regarding the arrangements for making data available between comparable categories of data recipients, including partner enterprises or linked enterprises of the data holder when making data available. Where a data recipient considers that the conditions under which data has been made available to it are discriminatory, the data holder shall without undue delay provide the data recipient, upon its reasoned request, with information showing that there has been no discrimination. 4. A data holder shall not make data available to a data recipient, including on an exclusive basis, unless requested to do so by the user under Chapter II.

[5] Data Act Article 3(1)-(2) (similarity 0.796)
Data Act Article 3(1)-(2) - Obligation to make product data and related service data accessible to the user
1. Connected products shall be designed and manufactured, and related services shall be designed and provided, in such a manner that product data and related service data, including the relevant metadata necessary to interpret and use those data, are, by default, easily, securely, free of charge, in a comprehensive, structured, commonly used and machine-readable format, and, where relevant and technically feasible, directly accessible to the user. 2. Before concluding a contract for the purchase, rent or lease of a connected product, the seller, rentor or lessor, which may be the manufacturer, shall provide at least the following information to the user, in a clear and comprehensible manner: (a) the type, format and estimated volume of product data which the connected product is capable of generating; (b) whether the connected product is capable of generating data continuously and in real-time; (c) whether the connected product is capable of storing data on-device or on a remote server, including, where applicable, the intended duration of retention; (d) how the user may access, retrieve or, where relevant, erase the data, including the technical means to do so, as well as their terms of use and quality of service.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q28 (unanswerable)

**Question.** Our cloud platform just suffered a serious cyberattack. Do we have to send an early warning to the authorities within 24 hours?

**Reference.** Not answerable from the indexed corpus (GDPR Art. 33 only covers personal data breaches with a 72-hour deadline; the 24-hour early warning for significant incidents is in NIS2).

**Agent answer.**

The indexed legislation does not cover this question. The corpus does not contain provisions establishing a 24-hour early warning obligation for general cloud platform cyberattacks; please check relevant cybersecurity legislation such as the NIS 2 Directive, national laws, or consult a lawyer.

**Cited:** none  
**Retrieved:** AI Act Article 15, AI Act Article 3, AI Act Article 73, Data Act Article 2, Data Act Article 37

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: cyberattack early warning 24 hours cybersecurity incident reporting Data Act

[1] AI Act Article 73(1)-(2) (similarity 0.742)
AI Act Article 73(1)-(2) - Reporting of serious incidents
1. Providers of high-risk AI systems placed on the Union market shall report any serious incident to the market surveillance authorities of the Member States where that incident occurred. 2. The report referred to in paragraph 1 shall be made immediately after the provider has established a causal link between the AI system and the serious incident or the reasonable likelihood of such a link, and, in any event, not later than 15 days after the provider or, where applicable, the deployer, becomes aware of the serious incident. The period for the reporting referred to in the first subparagraph shall take account of the severity of the serious incident.

[2] AI Act Article 15(5) (similarity 0.729)
AI Act Article 15(5) - Accuracy, robustness and cybersecurity
5. High-risk AI systems shall be resilient against attempts by unauthorised third parties to alter their use, outputs or performance by exploiting system vulnerabilities. The technical solutions aiming to ensure the cybersecurity of high-risk AI systems shall be appropriate to the relevant circumstances and the risks. The technical solutions to address AI specific vulnerabilities shall include, where appropriate, measures to prevent, detect, respond to, resolve and control for attacks trying to manipulate the training data set (data poisoning), or pre-trained components used in training (model poisoning), inputs designed to cause the AI model to make a mistake (adversarial examples or model evasion), confidentiality attacks or model flaws.

[3] AI Act Article 73(3)-(4) (similarity 0.726)
AI Act Article 73(3)-(4) - Reporting of serious incidents
3. Notwithstanding paragraph 2 of this Article, in the event of a widespread infringement or a serious incident as defined in Article 3, point (49)(b), the report referred to in paragraph 1 of this Article shall be provided immediately, and not later than two days after the provider or, where applicable, the deployer becomes aware of that incident. 4. Notwithstanding paragraph 2, in the event of the death of a person, the report shall be provided immediately after the provider or the deployer has established, or as soon as it suspects, a causal relationship between the high-risk AI system and the serious incident, but not later than 10 days after the date on which the provider or, where applicable, the deployer becomes aware of the serious incident.

[4] Data Act Article 2, points (28) to (29) (similarity 0.725)
Data Act Article 2, points (28) to (29) - Definitions
(28) 'public sector body' means national, regional or local authorities of the Member States and bodies governed by public law of the Member States, or associations formed by one or more such authorities or one or more such bodies; (29) 'public emergency' means an exceptional situation, limited in time, such as a public health emergency, an emergency resulting from natural disasters, a human-induced major disaster, including a major cybersecurity incident, negatively affecting the population of the Union or the whole or part of a Member State, with a risk of serious and lasting repercussions for living conditions or economic stability, financial stability, or the substantial and immediate degradation of economic assets in the Union or the relevant Member State and which is determined or officially declared in accordance with the relevant procedures under Union or national law;

[5] Data Act Article 37(1)-(2) (similarity 0.722)
Data Act Article 37(1)-(2) - Competent authorities and data coordinators
1. Each Member State shall designate one or more competent authorities to be responsible for the application and enforcement of this Regulation (competent authorities). Member States may establish one or more new authorities or rely on existing authorities. 2. Where a Member State designates more than one competent authority, it shall designate a data coordinator from among them to facilitate cooperation between the competent authorities and to assist entities within the scope of this Regulation on all matters related to its application and enforcement. Competent authorities shall, in the exercise of the tasks and powers assigned to them under paragraph 5, cooperate with each other.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.

5 passages for: incident notification 24 hours AI Act GDPR

[1] AI Act Article 73(1)-(2) (similarity 0.810)
AI Act Article 73(1)-(2) - Reporting of serious incidents
1. Providers of high-risk AI systems placed on the Union market shall report any serious incident to the market surveillance authorities of the Member States where that incident occurred. 2. The report referred to in paragraph 1 shall be made immediately after the provider has established a causal link between the AI system and the serious incident or the reasonable likelihood of such a link, and, in any event, not later than 15 days after the provider or, where applicable, the deployer, becomes aware of the serious incident. The period for the reporting referred to in the first subparagraph shall take account of the severity of the serious incident.

[2] AI Act Article 73(3)-(4) (similarity 0.806)
AI Act Article 73(3)-(4) - Reporting of serious incidents
3. Notwithstanding paragraph 2 of this Article, in the event of a widespread infringement or a serious incident as defined in Article 3, point (49)(b), the report referred to in paragraph 1 of this Article shall be provided immediately, and not later than two days after the provider or, where applicable, the deployer becomes aware of that incident. 4. Notwithstanding paragraph 2, in the event of the death of a person, the report shall be provided immediately after the provider or the deployer has established, or as soon as it suspects, a causal relationship between the high-risk AI system and the serious incident, but not later than 10 days after the date on which the provider or, where applicable, the deployer becomes aware of the serious incident.

[3] AI Act Article 73(5)-(6) (similarity 0.780)
AI Act Article 73(5)-(6) - Reporting of serious incidents
5. Where necessary to ensure timely reporting, the provider or, where applicable, the deployer, may submit an initial report that is incomplete, followed by a complete report. 6. Following the reporting of a serious incident pursuant to paragraph 1, the provider shall, without delay, perform the necessary investigations in relation to the serious incident and the AI system concerned. This shall include a risk assessment of the incident, and corrective action. The provider shall cooperate with the competent authorities, and where relevant with the notified body concerned, during the investigations referred to in the first subparagraph, and shall not perform any investigation which involves altering the AI system concerned in a way which may affect any subsequent evaluation of the causes of the incident, prior to informing the competent authorities of such action.

[4] AI Act Article 73(7)-(8) (similarity 0.778)
AI Act Article 73(7)-(8) - Reporting of serious incidents
7. Upon receiving a notification related to a serious incident referred to in Article 3, point (49)(c), the relevant market surveillance authority shall inform the national public authorities or bodies referred to in Article 77(1). The Commission shall develop dedicated guidance to facilitate compliance with the obligations set out in paragraph 1 of this Article. That guidance shall be issued by 2 August 2025, and shall be assessed regularly. 8. The market surveillance authority shall take appropriate measures, as provided for in Article 19 of Regulation (EU) 2019/1020, within seven days from the date it received the notification referred to in paragraph 1 of this Article, and shall follow the notification procedures as provided in that Regulation.

[5] AI Act Article 3, points (49) to (51) (similarity 0.774)
AI Act Article 3, points (49) to (51) - Definitions
(49) 'serious incident' means an incident or malfunctioning of an AI system that directly or indirectly leads to any of the following: (a) the death of a person, or serious harm to a person's health; (b) a serious and irreversible disruption of the management or operation of critical infrastructure; (c) the infringement of obligations under Union law intended to protect fundamental rights; (d) serious harm to property or the environment; (50) 'personal data' means personal data as defined in Article 4, point (1), of Regulation (EU) 2016/679; (51) 'non-personal data' means data other than personal data as defined in Article 4, point (1), of Regulation (EU) 2016/679;

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q29 (unanswerable)

**Question.** Can our company directors be held personally responsible if we ignore cybersecurity risk measures?

**Reference.** Not answerable from the indexed corpus; management-body responsibility for cybersecurity measures is set out in NIS2.

**Agent answer.**

The indexed legislation does not cover this question. 

The provided corpus does not address the personal liability of company directors for ignoring cybersecurity risk measures. You should check relevant national corporate law, other EU acts, or consult a qualified lawyer.

**Cited:** none  
**Retrieved:** AI Act Article 15, AI Act Article 3, AI Act Article 4

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: directors personal liability cybersecurity risk measures AI Act GDPR Data Act

[1] AI Act Article 15(5) (similarity 0.756)
AI Act Article 15(5) - Accuracy, robustness and cybersecurity
5. High-risk AI systems shall be resilient against attempts by unauthorised third parties to alter their use, outputs or performance by exploiting system vulnerabilities. The technical solutions aiming to ensure the cybersecurity of high-risk AI systems shall be appropriate to the relevant circumstances and the risks. The technical solutions to address AI specific vulnerabilities shall include, where appropriate, measures to prevent, detect, respond to, resolve and control for attacks trying to manipulate the training data set (data poisoning), or pre-trained components used in training (model poisoning), inputs designed to cause the AI model to make a mistake (adversarial examples or model evasion), confidentiality attacks or model flaws.

[2] AI Act Article 15(1)-(3) (similarity 0.743)
AI Act Article 15(1)-(3) - Accuracy, robustness and cybersecurity
1. High-risk AI systems shall be designed and developed in such a way that they achieve an appropriate level of accuracy, robustness, and cybersecurity, and that they perform consistently in those respects throughout their lifecycle. 2. To address the technical aspects of how to measure the appropriate levels of accuracy and robustness set out in paragraph 1 and any other relevant performance metrics, the Commission shall, in cooperation with relevant stakeholders and organisations such as metrology and benchmarking authorities, encourage, as appropriate, the development of benchmarks and measurement methodologies. 3. The levels of accuracy and the relevant accuracy metrics of high-risk AI systems shall be declared in the accompanying instructions of use.

[3] AI Act Article 3, points (49) to (51) (similarity 0.735)
AI Act Article 3, points (49) to (51) - Definitions
(49) 'serious incident' means an incident or malfunctioning of an AI system that directly or indirectly leads to any of the following: (a) the death of a person, or serious harm to a person's health; (b) a serious and irreversible disruption of the management or operation of critical infrastructure; (c) the infringement of obligations under Union law intended to protect fundamental rights; (d) serious harm to property or the environment; (50) 'personal data' means personal data as defined in Article 4, point (1), of Regulation (EU) 2016/679; (51) 'non-personal data' means data other than personal data as defined in Article 4, point (1), of Regulation (EU) 2016/679;

[4] AI Act Article 4 (similarity 0.733)
AI Act Article 4 - AI literacy
Providers and deployers of AI systems shall take measures to ensure, to their best extent, a sufficient level of AI literacy of their staff and other persons dealing with the operation and use of AI systems on their behalf, taking into account their technical knowledge, experience, education and training and the context the AI systems are to be used in, and considering the persons or groups of persons on whom the AI systems are to be used.

[5] AI Act Article 15(4) (similarity 0.733)
AI Act Article 15(4) - Accuracy, robustness and cybersecurity
4. High-risk AI systems shall be as resilient as possible regarding errors, faults or inconsistencies that may occur within the system or the environment in which the system operates, in particular due to their interaction with natural persons or other systems. Technical and organisational measures shall be taken in this regard. The robustness of high-risk AI systems may be achieved through technical redundancy solutions, which may include backup or fail-safe plans. High-risk AI systems that continue to learn after being placed on the market or put into service shall be developed in such a way as to eliminate or reduce as far as possible the risk of possibly biased outputs influencing input for future operations (feedback loops), and as to ensure that any such feedback loops are duly addressed with appropriate mitigation measures.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q30 (unanswerable)

**Question.** Do we need a cookie banner for analytics cookies on our website?

**Reference.** Not answerable from the indexed corpus; cookie consent rules sit in the ePrivacy Directive, which is not indexed.

**Agent answer.**

The indexed legislation does not cover this question. The retrieved passages outline the general conditions for consent and lawfulness under the GDPR, but do not specifically address cookie banners or analytics cookies. Please check national cookie laws implementing the ePrivacy Directive, guidance from data protection authorities, or consult a lawyer.

**Cited:** none  
**Retrieved:** GDPR Article 3, GDPR Article 6, GDPR Article 7, GDPR Article 89

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: cookie banner analytics cookies website GDPR consent

[1] GDPR Article 7(1)-(3) (similarity 0.696)
GDPR Article 7(1)-(3) - Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data. 2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding. 3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.

[2] GDPR Article 6(1) (similarity 0.683)
GDPR Article 6(1) - Lawfulness of processing
1. Processing shall be lawful only if and to the extent that at least one of the following applies: (a) the data subject has given consent to the processing of his or her personal data for one or more specific purposes; (b) processing is necessary for the performance of a contract to which the data subject is party or in order to take steps at the request of the data subject prior to entering into a contract; (c) processing is necessary for compliance with a legal obligation to which the controller is subject; (d) processing is necessary in order to protect the vital interests of the data subject or of another natural person; (e) processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller; (f) processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject which require protection of personal data, in particular where the data subject is a child. Point (f) of the first subparagraph shall not apply to processing carried out by public authorities in the performance of their tasks.

[3] GDPR Article 89(1) (similarity 0.670)
GDPR Article 89(1) - Safeguards and derogations relating to processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes
1. Processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes, shall be subject to appropriate safeguards, in accordance with this Regulation, for the rights and freedoms of the data subject. Those safeguards shall ensure that technical and organisational measures are in place in particular in order to ensure respect for the principle of data minimisation. Those measures may include pseudonymisation provided that those purposes can be fulfilled in that manner. Where those purposes can be fulfilled by further processing which does not permit or no longer permits the identification of data subjects, those purposes shall be fulfilled in that manner.

[4] GDPR Article 7(4) (similarity 0.668)
GDPR Article 7(4) - Conditions for consent
4. When assessing whether consent is freely given, utmost account shall be taken of whether, inter alia, the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

[5] GDPR Article 3 (similarity 0.666)
GDPR Article 3 - Territorial scope
1. This Regulation applies to the processing of personal data in the context of the activities of an establishment of a controller or a processor in the Union, regardless of whether the processing takes place in the Union or not. 2. This Regulation applies to the processing of personal data of data subjects who are in the Union by a controller or processor not established in the Union, where the processing activities are related to: (a) the offering of goods or services, irrespective of whether a payment of the data subject is required, to such data subjects in the Union; or (b) the monitoring of their behaviour as far as their behaviour takes place within the Union. 3. This Regulation applies to the processing of personal data by a controller not established in the Union, but in a place where Member State law applies by virtue of public international law.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.

Error executing tool search
```
</details>

---

## q31 (unanswerable)

**Question.** What did the EU Court of Justice rule about standard contractual clauses for transfers to the US?

**Reference.** Not answerable from the indexed corpus; it contains legislation text, not case law.

**Agent answer.**

The indexed legislation does not cover this question. 

The corpus does not contain case law or rulings from the Court of Justice regarding standard contractual clauses. For this topic, you should check relevant court judgments, European Commission guidance, or consult a legal professional.

**Cited:** none  
**Retrieved:** Data Act Article 28, Data Act Article 32, Data Act Article 41, GDPR Article 45, GDPR Article 48

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: standard contractual clauses transfers US Court of Justice

[1] GDPR Article 45(1)-(2) (similarity 0.754)
GDPR Article 45(1)-(2) - Transfers on the basis of an adequacy decision
1. A transfer of personal data to a third country or an international organisation may take place where the Commission has decided that the third country, a territory or one or more specified sectors within that third country, or the international organisation in question ensures an adequate level of protection. Such a transfer shall not require any specific authorisation. 2. When assessing the adequacy of the level of protection, the Commission shall, in particular, take account of the following elements: (a) the rule of law, respect for human rights and fundamental freedoms, relevant legislation, both general and sectoral, including concerning public security, defence, national security and criminal law and the access of public authorities to personal data, as well as the implementation of such legislation, data protection rules, professional rules and security measures, including rules for the onward transfer of personal data to another third country or international organisation which are complied with in that country or international organisation, case-law, as well as effective and enforceable data subject rights and effective administrative and judicial redress for the data subjects whose personal data are being transferred; (b) the existence and effective functioning of one or more independent supervisory authorities in the third country or to which an international organisation is subject, with responsibility for ensuring and enforcing compliance with the data protection rules, including adequate enforcement powers, for assisting and advising the data subjects in exercising their rights and for cooperation with the supervisory authorities of the Member States; and (c) the international commitments the third country or international organisation concerned has entered into, or other obligations arising from legally binding conventions or instruments as well as from its participation in multilateral or regional systems, in particular in relation to the protection of personal data.

[2] GDPR Article 48 (similarity 0.743)
GDPR Article 48 - Transfers or disclosures not authorised by Union law
Any judgment of a court or tribunal and any decision of an administrative authority of a third country requiring a controller or processor to transfer or disclose personal data may only be recognised or enforceable in any manner if based on an international agreement, such as a mutual legal assistance treaty, in force between the requesting third country and the Union or a Member State, without prejudice to other grounds for transfer pursuant to this Chapter.

[3] Data Act Article 28 (similarity 0.739)
Data Act Article 28 - Contractual transparency obligations on international access and transfer
1. Providers of data processing services shall make the following information available on their websites, and keep that information up to date: (a) the jurisdiction to which the ICT infrastructure deployed for data processing of their individual services is subject; (b) a general description of the technical, organisational and contractual measures adopted by the provider of data processing services in order to prevent international governmental access to or transfer of non-personal data held in the Union where such access or transfer would create a conflict with Union law or the national law of the relevant Member State. 2. The websites referred to in paragraph 1 shall be listed in contracts for all data processing services offered by providers of data processing services.

[4] Data Act Article 32(3) (similarity 0.738)
Data Act Article 32(3) - International governmental access and transfer
3. In the absence of an international agreement as referred to in paragraph 2, where a provider of data processing services is the addressee of a decision or judgment of a third-country court or tribunal or a decision of a third-country administrative authority to transfer or give access to non-personal data falling within the scope of this Regulation held in the Union and compliance with such a decision would risk putting the addressee in conflict with Union law or with the national law of the relevant Member State, transfer to or access to such data by that third-country authority shall take place only where: (a) the third-country system requires the reasons and proportionality of such a decision or judgment to be set out and requires such a decision or judgment to be specific in character, for instance by establishing a sufficient link to certain suspected persons or infringements; (b) the reasoned objection of the addressee is subject to a review by a competent third-country court or tribunal; and (c) the competent third-country court or tribunal issuing the decision or judgment or reviewing the decision of an administrative authority is empowered under the law of that third country to take duly into account the relevant legal interests of the provider of the data protected by Union law or by the national law of the relevant Member State. The addressee of the decision or judgment may ask the opinion of the relevant national body or authority competent for international cooperation in legal matters, in order to determine whether the conditions laid down in the first subparagraph are met, in particular when it considers that the decision may relate to trade secrets and other commercially sensitive data as well as to content protected by intellectual property rights or the transfer may lead to re-identification. The relevant national body or authority may consult the Commission. If the addressee considers that the decision or judgment may impinge on the national security or defence interests of the Union or its Member States, it shall ask the opinion of the relevant national body or authority in order to determine whether the data requested concerns national security or defence interests of the Union or its Member States. If the addressee has not received a reply within one month, or if the opinion of such body or authority concludes that the conditions laid down in the first subparagraph are not met, the addressee may reject the request for transfer or access, to non-personal data, on those grounds. The EDIB referred to in Article 42 shall advise and assist the Commission in developing guidelines on the assessment of whether the conditions laid down in the first subparagraph of this paragraph are met.

[5] Data Act Article 41 (similarity 0.738)
Data Act Article 41 - Model contractual terms and standard contractual clauses
The Commission, before 12 September 2025, shall develop and recommend non-binding model contractual terms on data access and use, including terms on reasonable compensation and the protection of trade secrets, and non-binding standard contractual clauses for cloud computing contracts to assist parties in drafting and negotiating contracts with fair, reasonable and non-discriminatory contractual rights and obligations.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q32 (unanswerable)

**Question.** Which Spanish authority will supervise our AI product under the AI Act, and how do we contact it?

**Reference.** Not answerable from the indexed corpus: the AI Act (Art. 70) only requires each Member State to designate national competent authorities; it does not name the Spanish one or its contact details. Check national sources or a lawyer.

**Agent answer.**

The indexed legislation does not cover this question. The text requires Member States to designate authorities and make contact information publicly available by 2 August 2025, but it does not list specific national authorities or their contact details. Please check official Spanish government publications or consult a lawyer for the exact contact details of the Spanish market surveillance authority.

**Cited:** none  
**Retrieved:** AI Act Article 70, Data Act Article 37

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: Spanish authority national competent authority AI Act contact

[1] AI Act Article 70(2) (similarity 0.791)
AI Act Article 70(2) - Designation of national competent authorities and single points of contact
2. Member States shall communicate to the Commission the identity of the notifying authorities and the market surveillance authorities and the tasks of those authorities, as well as any subsequent changes thereto. Member States shall make publicly available information on how competent authorities and single points of contact can be contacted, through electronic communication means by 2 August 2025. Member States shall designate a market surveillance authority to act as the single point of contact for this Regulation, and shall notify the Commission of the identity of the single point of contact. The Commission shall make a list of the single points of contact publicly available.

[2] AI Act Article 70(8)-(9) (similarity 0.785)
AI Act Article 70(8)-(9) - Designation of national competent authorities and single points of contact
8. National competent authorities may provide guidance and advice on the implementation of this Regulation, in particular to SMEs including start-ups, taking into account the guidance and advice of the Board and the Commission, as appropriate. Whenever national competent authorities intend to provide guidance and advice with regard to an AI system in areas covered by other Union law, the national competent authorities under that Union law shall be consulted, as appropriate. 9. Where Union institutions, bodies, offices or agencies fall within the scope of this Regulation, the European Data Protection Supervisor shall act as the competent authority for their supervision.

[3] AI Act Article 70(1) (similarity 0.771)
AI Act Article 70(1) - Designation of national competent authorities and single points of contact
1. Each Member State shall establish or designate as national competent authorities at least one notifying authority and at least one market surveillance authority for the purposes of this Regulation. Those national competent authorities shall exercise their powers independently, impartially and without bias so as to safeguard the objectivity of their activities and tasks, and to ensure the application and implementation of this Regulation. The members of those authorities shall refrain from any action incompatible with their duties. Provided that those principles are observed, such activities and tasks may be performed by one or more designated authorities, in accordance with the organisational needs of the Member State.

[4] Data Act Article 37(1)-(2) (similarity 0.768)
Data Act Article 37(1)-(2) - Competent authorities and data coordinators
1. Each Member State shall designate one or more competent authorities to be responsible for the application and enforcement of this Regulation (competent authorities). Member States may establish one or more new authorities or rely on existing authorities. 2. Where a Member State designates more than one competent authority, it shall designate a data coordinator from among them to facilitate cooperation between the competent authorities and to assist entities within the scope of this Regulation on all matters related to its application and enforcement. Competent authorities shall, in the exercise of the tasks and powers assigned to them under paragraph 5, cooperate with each other.

[5] AI Act Article 70(3) (similarity 0.767)
AI Act Article 70(3) - Designation of national competent authorities and single points of contact
3. Member States shall ensure that their national competent authorities are provided with adequate technical, financial and human resources, and with infrastructure to fulfil their tasks effectively under this Regulation. In particular, the national competent authorities shall have a sufficient number of personnel permanently available whose competences and expertise shall include an in-depth understanding of AI technologies, data and data computing, personal data protection, cybersecurity, fundamental rights, health and safety risks and knowledge of existing standards and legal requirements. Member States shall assess and, if necessary, update competence and resource requirements referred to in this paragraph on an annual basis.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q33 (unanswerable)

**Question.** How do we know whether our dataset is anonymised well enough that GDPR no longer applies?

**Reference.** Not answerable from the articles alone; the test for anonymous information appears only in a recital.

**Agent answer.**

The indexed legislation does not cover this question. The retrieved passages define personal data and mention measures like pseudonymisation, but they do not state the threshold or criteria for when a dataset is sufficiently anonymised to remove it from the scope of the GDPR. Please check national guidance, other EU acts, or consult a lawyer.

**Cited:** none  
**Retrieved:** Data Act Article 18, GDPR Article 25, GDPR Article 4, GDPR Article 5, GDPR Article 89

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: anonymisation anonymized dataset application of GDPR personal data

[1] GDPR Article 4, points intro to (2) (similarity 0.761)
GDPR Article 4, points intro to (2) - Definitions
For the purposes of this Regulation: (1) 'personal data' means any information relating to an identified or identifiable natural person ('data subject'); an identifiable natural person is one who can be identified, directly or indirectly, in particular by reference to an identifier such as a name, an identification number, location data, an online identifier or to one or more factors specific to the physical, physiological, genetic, mental, economic, cultural or social identity of that natural person; (2) 'processing' means any operation or set of operations which is performed on personal data or on sets of personal data, whether or not by automated means, such as collection, recording, organisation, structuring, storage, adaptation or alteration, retrieval, consultation, use, disclosure by transmission, dissemination or otherwise making available, alignment or combination, restriction, erasure or destruction;

[2] GDPR Article 25(1) (similarity 0.759)
GDPR Article 25(1) - Data protection by design and by default
1. Taking into account the state of the art, the cost of implementation and the nature, scope, context and purposes of processing as well as the risks of varying likelihood and severity for rights and freedoms of natural persons posed by the processing, the controller shall, both at the time of the determination of the means for processing and at the time of the processing itself, implement appropriate technical and organisational measures, such as pseudonymisation, which are designed to implement data-protection principles, such as data minimisation, in an effective manner and to integrate the necessary safeguards into the processing in order to meet the requirements of this Regulation and protect the rights of data subjects.

[3] GDPR Article 89(1) (similarity 0.754)
GDPR Article 89(1) - Safeguards and derogations relating to processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes
1. Processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes, shall be subject to appropriate safeguards, in accordance with this Regulation, for the rights and freedoms of the data subject. Those safeguards shall ensure that technical and organisational measures are in place in particular in order to ensure respect for the principle of data minimisation. Those measures may include pseudonymisation provided that those purposes can be fulfilled in that manner. Where those purposes can be fulfilled by further processing which does not permit or no longer permits the identification of data subjects, those purposes shall be fulfilled in that manner.

[4] Data Act Article 18(3)-(4) (similarity 0.752)
Data Act Article 18(3)-(4) - Compliance with requests for data
3. If the data holder decides to decline the request or to seek its modification in accordance with paragraph 2, point (b), it shall indicate the identity of the public sector body or the Commission, the European Central Bank or the Union body that previously submitted a request for the same purpose. 4. Where the data requested includes personal data, the data holder shall properly anonymise the data, unless the compliance with the request to make data available to a public sector body, the Commission, the European Central Bank or a Union body requires the disclosure of personal data. In such cases, the data holder shall pseudonymise the data.

[5] GDPR Article 5 (similarity 0.752)
GDPR Article 5 - Principles relating to processing of personal data
1. Personal data shall be: (a) processed lawfully, fairly and in a transparent manner in relation to the data subject ('lawfulness, fairness and transparency'); (b) collected for specified, explicit and legitimate purposes and not further processed in a manner that is incompatible with those purposes; further processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes shall, in accordance with Article 89(1), not be considered to be incompatible with the initial purposes ('purpose limitation'); (c) adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed ('data minimisation'); (d) accurate and, where necessary, kept up to date; every reasonable step must be taken to ensure that personal data that are inaccurate, having regard to the purposes for which they are processed, are erased or rectified without delay ('accuracy'); (e) kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed; personal data may be stored for longer periods insofar as the personal data will be processed solely for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) subject to implementation of the appropriate technical and organisational measures required by this Regulation in order to safeguard the rights and freedoms of the data subject ('storage limitation'); (f) processed in a manner that ensures appropriate security of the personal data, including protection against unauthorised or unlawful processing and against accidental loss, destruction or damage, using appropriate technical or organisational measures ('integrity and confidentiality'). 2. The controller shall be responsible for, and be able to demonstrate compliance with, paragraph 1 ('accountability').

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q34 (unanswerable)

**Question.** Which technical standard should we certify against to show our high-risk AI meets the accuracy requirements?

**Reference.** Not answerable from the indexed corpus; the AI Act refers to harmonised standards in general but does not name specific ones.

**Agent answer.**

The indexed legislation does not specify a particular named technical standard to certify against for accuracy, but states that high-risk AI systems in conformity with harmonised standards whose references are published in the Official Journal of the European Union are presumed to comply with the accuracy requirements.

* High-risk AI systems must be designed and developed to achieve an appropriate level of accuracy, robustness, and cybersecurity, and perform consistently throughout their lifecycle, with accuracy levels and metrics declared in the instructions for use (AI Act Article 15(1)-(3)).
* Systems in conformity with harmonised standards (or parts thereof) published in the Official Journal of the European Union are presumed to be in conformity with the relevant requirements (AI Act Article 40(1)).
* Alternatively, common specifications adopted by the Commission may provide means to comply with certain requirements (AI Act Article 3, point (28) and Article 43(1)).
* The indexed legislation does not cover specific standard numbers or titles. Please check official European Commission publications regarding standardisation requests, harmonised standards under the AI Act, or consult a legal professional.

**Cited:** AI Act Article 15, AI Act Article 3, AI Act Article 40  
**Retrieved:** AI Act Article 15, AI Act Article 3, AI Act Article 32, AI Act Article 40, AI Act Article 43

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: high risk AI system accuracy requirements technical standard harmonised standards common specifications conformity assessment

[1] AI Act Article 15(1)-(3) (similarity 0.827)
AI Act Article 15(1)-(3) - Accuracy, robustness and cybersecurity
1. High-risk AI systems shall be designed and developed in such a way that they achieve an appropriate level of accuracy, robustness, and cybersecurity, and that they perform consistently in those respects throughout their lifecycle. 2. To address the technical aspects of how to measure the appropriate levels of accuracy and robustness set out in paragraph 1 and any other relevant performance metrics, the Commission shall, in cooperation with relevant stakeholders and organisations such as metrology and benchmarking authorities, encourage, as appropriate, the development of benchmarks and measurement methodologies. 3. The levels of accuracy and the relevant accuracy metrics of high-risk AI systems shall be declared in the accompanying instructions of use.

[2] AI Act Article 43(1) (similarity 0.814)
AI Act Article 43(1) - Conformity assessment
1. For high-risk AI systems listed in point 1 of Annex III, where, in demonstrating the compliance of a high-risk AI system with the requirements set out in Section 2, the provider has applied harmonised standards referred to in Article 40, or, where applicable, common specifications referred to in Article 41, the provider shall opt for one of the following conformity assessment procedures based on: (a) the internal control referred to in Annex VI; or (b) the assessment of the quality management system and the assessment of the technical documentation, with the involvement of a notified body, referred to in Annex VII. In demonstrating the compliance of a high-risk AI system with the requirements set out in Section 2, the provider shall follow the conformity assessment procedure set out in Annex VII where: (a) harmonised standards referred to in Article 40 do not exist, and common specifications referred to in Article 41 are not available; (b) the provider has not applied, or has applied only part of, the harmonised standard; (c) the common specifications referred to in point (a) exist, but the provider has not applied them; (d) one or more of the harmonised standards referred to in point (a) has been published with a restriction, and only on the part of the standard that was restricted. For the purposes of the conformity assessment procedure referred to in Annex VII, the provider may choose any of the notified bodies. However, where the high-risk AI system is intended to be put into service by law enforcement, immigration or asylum authorities or by Union institutions, bodies, offices or agencies, the market surveillance authority referred to in Article 74(8) or (9), as applicable, shall act as a notified body.

[3] AI Act Article 40(1)-(2) (similarity 0.810)
AI Act Article 40(1)-(2) - Harmonised standards and standardisation deliverables
1. High-risk AI systems or general-purpose AI models which are in conformity with harmonised standards or parts thereof the references of which have been published in the Official Journal of the European Union in accordance with Regulation (EU) No 1025/2012 shall be presumed to be in conformity with the requirements set out in Section 2 of this Chapter or, as applicable, with the obligations set out in of Chapter V, Sections 2 and 3, of this Regulation, to the extent that those standards cover those requirements or obligations. 2. In accordance with Article 10 of Regulation (EU) No 1025/2012, the Commission shall issue, without undue delay, standardisation requests covering all requirements set out in Section 2 of this Chapter and, as applicable, standardisation requests covering obligations set out in Chapter V, Sections 2 and 3, of this Regulation. The standardisation request shall also ask for deliverables on reporting and documentation processes to improve AI systems' resource performance, such as reducing the high-risk AI system's consumption of energy and of other resources during its lifecycle, and on the energy-efficient development of general-purpose AI models. When preparing a standardisation request, the Commission shall consult the Board and relevant stakeholders, including the advisory forum. When issuing a standardisation request to European standardisation organisations, the Commission shall specify that standards have to be clear, consistent, including with the standards developed in the various sectors for products covered by the existing Union harmonisation legislation listed in Annex I, and aiming to ensure that high-risk AI systems or general-purpose AI models placed on the market or put into service in the Union meet the relevant requirements or obligations laid down in this Regulation. The Commission shall request the European standardisation organisations to provide evidence of their best efforts to fulfil the objectives referred to in the first and the second subparagraph of this paragraph in accordance with Article 24 of Regulation (EU) No 1025/2012.

[4] AI Act Article 3, points (27) to (30) (similarity 0.805)
AI Act Article 3, points (27) to (30) - Definitions
(27) 'harmonised standard' means a harmonised standard as defined in Article 2(1), point (c), of Regulation (EU) No 1025/2012; (28) 'common specification' means a set of technical specifications as defined in Article 2, point (4) of Regulation (EU) No 1025/2012, providing means to comply with certain requirements established under this Regulation; (29) 'training data' means data used for training an AI system through fitting its learnable parameters; (30) 'validation data' means data used for providing an evaluation of the trained AI system and for tuning its non-learnable parameters and its learning process in order, inter alia, to prevent underfitting or overfitting;

[5] AI Act Article 32 (similarity 0.795)
AI Act Article 32 - Presumption of conformity with requirements relating to notified bodies
Where a conformity assessment body demonstrates its conformity with the criteria laid down in the relevant harmonised standards or parts thereof, the references of which have been published in the Official Journal of the European Union, it shall be presumed to comply with the requirements set out in Article 31 in so far as the applicable harmonised standards cover those requirements.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---

## q35 (unanswerable)

**Question.** Our AI tool produced faulty output and a client's business lost money. What compensation can they claim under EU product liability rules?

**Reference.** Not answerable from the indexed corpus; civil liability for defective products is outside GDPR, AI Act and Data Act.

**Agent answer.**

The indexed legislation does not cover this question. Product liability rules and specific compensation claims for financial loss caused by faulty AI outputs are not detailed in the indexed provisions of the GDPR, AI Act, or Data Act; please check relevant national civil law, product liability directives, or consult a lawyer.

**Cited:** none  
**Retrieved:** AI Act Article 15, AI Act Article 57, AI Act Article 60, AI Act Article 73

<details><summary>Retrieved passages (full text)</summary>

```
5 passages for: compensation damages product liability AI Act

[1] AI Act Article 57(12) (similarity 0.759)
AI Act Article 57(12) - AI regulatory sandboxes
12. Providers and prospective providers participating in the AI regulatory sandbox shall remain liable under applicable Union and national liability law for any damage inflicted on third parties as a result of the experimentation taking place in the sandbox. However, provided that the prospective providers observe the specific plan and the terms and conditions for their participation and follow in good faith the guidance given by the national competent authority, no administrative fines shall be imposed by the authorities for infringements of this Regulation. Where other competent authorities responsible for other Union and national law were actively involved in the supervision of the AI system in the sandbox and provided guidance for compliance, no administrative fines shall be imposed regarding that law.

[2] AI Act Article 60(7)-(9) (similarity 0.754)
AI Act Article 60(7)-(9) - Testing of high-risk AI systems in real world conditions outside AI regulatory sandboxes
7. Any serious incident identified in the course of the testing in real world conditions shall be reported to the national market surveillance authority in accordance with Article 73. The provider or prospective provider shall adopt immediate mitigation measures or, failing that, shall suspend the testing in real world conditions until such mitigation takes place, or otherwise terminate it. The provider or prospective provider shall establish a procedure for the prompt recall of the AI system upon such termination of the testing in real world conditions. 8. Providers or prospective providers shall notify the national market surveillance authority in the Member State where the testing in real world conditions is to be conducted of the suspension or termination of the testing in real world conditions and of the final outcomes. 9. The provider or prospective provider shall be liable under applicable Union and national liability law for any damage caused in the course of their testing in real world conditions.

[3] AI Act Article 15(1)-(3) (similarity 0.749)
AI Act Article 15(1)-(3) - Accuracy, robustness and cybersecurity
1. High-risk AI systems shall be designed and developed in such a way that they achieve an appropriate level of accuracy, robustness, and cybersecurity, and that they perform consistently in those respects throughout their lifecycle. 2. To address the technical aspects of how to measure the appropriate levels of accuracy and robustness set out in paragraph 1 and any other relevant performance metrics, the Commission shall, in cooperation with relevant stakeholders and organisations such as metrology and benchmarking authorities, encourage, as appropriate, the development of benchmarks and measurement methodologies. 3. The levels of accuracy and the relevant accuracy metrics of high-risk AI systems shall be declared in the accompanying instructions of use.

[4] AI Act Article 73(5)-(6) (similarity 0.738)
AI Act Article 73(5)-(6) - Reporting of serious incidents
5. Where necessary to ensure timely reporting, the provider or, where applicable, the deployer, may submit an initial report that is incomplete, followed by a complete report. 6. Following the reporting of a serious incident pursuant to paragraph 1, the provider shall, without delay, perform the necessary investigations in relation to the serious incident and the AI system concerned. This shall include a risk assessment of the incident, and corrective action. The provider shall cooperate with the competent authorities, and where relevant with the notified body concerned, during the investigations referred to in the first subparagraph, and shall not perform any investigation which involves altering the AI system concerned in a way which may affect any subsequent evaluation of the causes of the incident, prior to informing the competent authorities of such action.

[5] AI Act Article 73(1)-(2) (similarity 0.738)
AI Act Article 73(1)-(2) - Reporting of serious incidents
1. Providers of high-risk AI systems placed on the Union market shall report any serious incident to the market surveillance authorities of the Member States where that incident occurred. 2. The report referred to in paragraph 1 shall be made immediately after the provider has established a causal link between the AI system and the serious incident or the reasonable likelihood of such a link, and, in any event, not later than 15 days after the provider or, where applicable, the deployer, becomes aware of the serious incident. The period for the reporting referred to in the first subparagraph shall take account of the severity of the serious incident.

Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. If none of them answers the question, say the corpus does not cover it.
```
</details>

---
