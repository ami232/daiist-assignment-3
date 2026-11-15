# Agent answers for grading

Grade in eval/human_labels.csv (id, correct, supported, notes) before opening judge_verdicts.jsonl.

## s01 (single)

**Question:** Can I use pre-ticked boxes on our signup form to get consent for marketing?

**Reference:** No. Consent must be a clear affirmative act. Silence, pre-ticked boxes or inactivity do not count as consent.

**Expected:** GDPR, Recital 32

**Answer:**

No, you cannot use pre-ticked boxes to get consent for marketing. 

Under the GDPR, consent requires a clear affirmative act that shows a freely given, specific, informed, and unambiguous agreement (GDPR, Recital 32). Recital 32 explicitly states that silence, pre-ticked boxes, or inactivity do not constitute consent. Furthermore, you must be able to demonstrate that the user has consented (GDPR, Article 7(1)). 

Because this concerns compliance with core consent rules, you should confirm your final signup flow with a lawyer before launch. The corpus does not cover national ePrivacy laws or local rules that may impose additional restrictions on electronic marketing.

**Retrieved:** GDPR, Article 7; GDPR, Recital 32; GDPR, Recital 40; GDPR, Recital 47; GDPR, Recital 70

<details><summary>search: consent pre-ticked boxes marketing GDPR</summary>

```
[1] Cite as: GDPR, Recital 32 | type: recital
Consent should be given by a clear affirmative act establishing a freely given, specific, informed and unambiguous indication of the data subject's agreement to the processing of personal data relating to him or her, such as by a written statement, including by electronic means, or an oral statement. This could include ticking a box when visiting an internet website, choosing technical settings for information society services or another statement or conduct which clearly indicates in this context the data subject's acceptance of the proposed processing of his or her personal data. Silence, pre-ticked boxes or inactivity should not therefore constitute consent. Consent should cover all processing activities carried out for the same purpose or purposes. When the processing has multiple purposes, consent should be given for all of them. If the data subject's consent is to be given following a request by electronic means, the request must be clear, concise and not unnecessarily disruptive to the use of the service for which it is provided.

[2] Cite as: GDPR, Article 7 | type: article — Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data.
2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding.
3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.
4. When assessing whether consent is freely given, utmost account shall be taken of whether,
inter alia
, the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

[3] Cite as: GDPR, Recital 70 | type: recital
Where personal data are processed for the purposes of direct marketing, the data subject should have the right to object to such processing, including profiling to the extent that it is related to such direct marketing, whether with regard to initial or further processing, at any time and free of charge. That right should be explicitly brought to the attention of the data subject and presented clearly and separately from any other information.

[4] Cite as: GDPR, Recital 40 | type: recital
In order for processing to be lawful, personal data should be processed on the basis of the consent of the data subject concerned or some other legitimate basis, laid down by law, either in this Regulation or in other Union or Member State law as referred to in this Regulation, including the necessity for compliance with the legal obligation to which the controller is subject or the necessity for the performance of a contract to which the data subject is party or in order to take steps at the request of the data subject prior to entering into a contract.

[5] Cite as: GDPR, Recital 47 | type: recital
The legitimate interests of a controller, including those of a controller to which the personal data may be disclosed, or of a third party, may provide a legal basis for processing, provided that the interests or the fundamental rights and freedoms of the data subject are not overriding, taking into consideration the reasonable expectations of data subjects based on their relationship with the controller. Such legitimate interest could exist for example where there is a relevant and appropriate relationship between the data subject and the controller in situations such as where the data subject is a client or in the service of the controller. At any rate the existence of a legitimate interest would need careful assessment including whether a data subject can reasonably expect at the time and in the context of the collection of the personal data that processing for that purpose may take place. The interests and fundamental rights of the data subject could in particular override the interest of the data controller where personal data are processed in circumstances where data subjects do not reasonably expect further processing. Given that it is for the legislator to provide by law for the legal basis for public authorities to process personal data, that legal basis should not apply to the processing by public authorities in the performance of their tasks. The processing of personal data strictly necessary for the purposes of preventing fraud also constitutes a legitimate interest of the data controller concerned. The processing of personal data for direct marketing purposes may be regarded as carried out for a legitimate interest.
```
</details>

---

## s02 (single)

**Question:** A user asked us to delete their account and all their data. Do we have to, and are there exceptions?

**Reference:** Yes, you must erase the data without undue delay where a ground applies, for example the data is no longer needed, consent is withdrawn, the user objects, or the processing was unlawful. Exceptions include freedom of expression, compliance with a legal obligation, public health, archiving or research purposes, and the establishment or defence of legal claims.

**Expected:** GDPR, Article 17

**Answer:**

Yes, you generally have to delete the user's personal data without undue delay when requested, but there are explicit exceptions (GDPR, Article 17). 

You must erase the data if one of the following grounds applies:
* The data is no longer necessary for the purposes it was collected for (GDPR, Article 17(1)(a)).
* The user withdraws consent and there is no other legal ground for processing (GDPR, Article 17(1)(b)).
* The user objects to the processing and there are no overriding legitimate grounds (GDPR, Article 17(1)(c)).
* The data was unlawfully processed (GDPR, Article 17(1)(d)).
* The data must be erased to comply with a legal obligation (GDPR, Article 17(1)(e)).

**Exceptions:**
Erasure does not apply to the extent that keeping the data is necessary for:
* Exercising the right of freedom of expression and information (GDPR, Article 17(3)(a)).
* Complying with a legal obligation under EU or Member State law, or performing a public interest task (GDPR, Article 17(3)(b)).
* Public health reasons (GDPR, Article 17(3)(c)).
* Archiving, scientific, historical, or statistical purposes where erasure would seriously impair that processing (GDPR, Article 17(3)(d)).
* The establishment, exercise, or defence of legal claims (GDPR, Article 17(3)(e)).

Because whether an exception applies (such as a legal obligation to retain invoice data or defending legal claims) depends on your specific records and legal requirements, confirm with a lawyer before refusing an erasure request.

**Retrieved:** GDPR, Article 16; GDPR, Article 17; GDPR, Article 19; GDPR, Recital 65; GDPR, Recital 66

<details><summary>search: right to erasure deletion account data GDPR Article 17</summary>

```
[1] Cite as: GDPR, Article 17 | type: article — Right to erasure (‘right to be forgotten’)
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
(c) for reasons of public interest in the area of public health in accordance with points (h) and (i) of Article 9(2) as well as Article 9(3);
(d) for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) in so far as the right referred to in paragraph 1 is likely to render impossible or seriously impair the achievement of the objectives of that processing; or
(e) for the establishment, exercise or defence of legal claims.

[2] Cite as: GDPR, Recital 65 | type: recital
A data subject should have the right to have personal data concerning him or her rectified and a ‘right to be forgotten’ where the retention of such data infringes this Regulation or Union or Member State law to which the controller is subject. In particular, a data subject should have the right to have his or her personal data erased and no longer processed where the personal data are no longer necessary in relation to the purposes for which they are collected or otherwise processed, where a data subject has withdrawn his or her consent or objects to the processing of personal data concerning him or her, or where the processing of his or her personal data does not otherwise comply with this Regulation. That right is relevant in particular where the data subject has given his or her consent as a child and is not fully aware of the risks involved by the processing, and later wants to remove such personal data, especially on the internet. The data subject should be able to exercise that right notwithstanding the fact that he or she is no longer a child. However, the further retention of the personal data should be lawful where it is necessary, for exercising the right of freedom of expression and information, for compliance with a legal obligation, for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller, on the grounds of public interest in the area of public health, for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes, or for the establishment, exercise or defence of legal claims.

[3] Cite as: GDPR, Recital 66 | type: recital
To strengthen the right to be forgotten in the online environment, the right to erasure should also be extended in such a way that a controller who has made the personal data public should be obliged to inform the controllers which are processing such personal data to erase any links to, or copies or replications of those personal data. In doing so, that controller should take reasonable steps, taking into account available technology and the means available to the controller, including technical measures, to inform the controllers which are processing the personal data of the data subject's request.

[4] Cite as: GDPR, Article 19 | type: article — Notification obligation regarding rectification or erasure of personal data or restriction of processing
The controller shall communicate any rectification or erasure of personal data or restriction of processing carried out in accordance with Article 16, Article 17(1) and Article 18 to each recipient to whom the personal data have been disclosed, unless this proves impossible or involves disproportionate effort. The controller shall inform the data subject about those recipients if the data subject requests it.

[5] Cite as: GDPR, Article 16 | type: article — Right to rectification
The data subject shall have the right to obtain from the controller without undue delay the rectification of inaccurate personal data concerning him or her. Taking into account the purposes of the processing, the data subject shall have the right to have incomplete personal data completed, including by means of providing a supplementary statement.
```
</details>

---

## s03 (single)

**Question:** We had a data breach last night. How quickly do we have to tell the regulator?

**Reference:** Without undue delay and, where feasible, within 72 hours of becoming aware of it, unless the breach is unlikely to result in a risk to people's rights and freedoms. If you notify later than 72 hours, you must give the reasons for the delay. A processor must notify the controller without undue delay.

**Expected:** GDPR, Article 33

**Answer:**

You must notify the competent supervisory authority **without undue delay and, where feasible, not later than 72 hours** after having become aware of the personal data breach (GDPR, Article 33). 

However, this requirement has one exception: you do not need to notify the authority if the breach is **unlikely to result in a risk to the rights and freedoms of natural persons** (GDPR, Article 33). 

If you cannot notify them within 72 hours, your notification must be accompanied by reasons for the delay, and you may provide the required information in phases without undue further delay (GDPR, Article 33). Additionally, processors must notify controllers without undue delay after becoming aware of a breach (GDPR, Article 33). 

Because whether a breach creates a "risk" depends entirely on the specific facts of the incident (such as the nature of the data and whether it was encrypted), you should confirm your assessment and notification strategy with a lawyer before proceeding.

**Retrieved:** GDPR, Article 33; GDPR, Recital 137; GDPR, Recital 85; GDPR, Recital 86; GDPR, Recital 87

<details><summary>search: personal data breach notification to supervisory authority timeline hours</summary>

```
[1] Cite as: GDPR, Article 33 | type: article — Notification of a personal data breach to the supervisory authority
1. In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority competent in accordance with Article 55, unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where the notification to the supervisory authority is not made within 72 hours, it shall be accompanied by reasons for the delay.
2. The processor shall notify the controller without undue delay after becoming aware of a personal data breach.
3. The notification referred to in paragraph 1 shall at least:
(a) describe the nature of the personal data breach including where possible, the categories and approximate number of data subjects concerned and the categories and approximate number of personal data records concerned;
(b) communicate the name and contact details of the data protection officer or other contact point where more information can be obtained;
(c) describe the likely consequences of the personal data breach;
(d) describe the measures taken or proposed to be taken by the controller to address the personal data breach, including, where appropriate, measures to mitigate its possible adverse effects.
4. Where, and in so far as, it is not possible to provide the information at the same time, the information may be provided in phases without undue further delay.
5. The controller shall document any personal data breaches, comprising the facts relating to the personal data breach, its effects and the remedial action taken. That documentation shall enable the supervisory authority to verify compliance with this Article.

[2] Cite as: GDPR, Recital 85 | type: recital
A personal data breach may, if not addressed in an appropriate and timely manner, result in physical, material or non-material damage to natural persons such as loss of control over their personal data or limitation of their rights, discrimination, identity theft or fraud, financial loss, unauthorised reversal of pseudonymisation, damage to reputation, loss of confidentiality of personal data protected by professional secrecy or any other significant economic or social disadvantage to the natural person concerned. Therefore, as soon as the controller becomes aware that a personal data breach has occurred, the controller should notify the personal data breach to the supervisory authority without undue delay and, where feasible, not later than 72 hours after having become aware of it, unless the controller is able to demonstrate, in accordance with the accountability principle, that the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where such notification cannot be achieved within 72 hours, the reasons for the delay should accompany the notification and information may be provided in phases without undue further delay.

[3] Cite as: GDPR, Recital 87 | type: recital
It should be ascertained whether all appropriate technological protection and organisational measures have been implemented to establish immediately whether a personal data breach has taken place and to inform promptly the supervisory authority and the data subject. The fact that the notification was made without undue delay should be established taking into account in particular the nature and gravity of the personal data breach and its consequences and adverse effects for the data subject. Such notification may result in an intervention of the supervisory authority in accordance with its tasks and powers laid down in this Regulation.

[4] Cite as: GDPR, Recital 86 | type: recital
The controller should communicate to the data subject a personal data breach, without undue delay, where that personal data breach is likely to result in a high risk to the rights and freedoms of the natural person in order to allow him or her to take the necessary precautions. The communication should describe the nature of the personal data breach as well as recommendations for the natural person concerned to mitigate potential adverse effects. Such communications to data subjects should be made as soon as reasonably feasible and in close cooperation with the supervisory authority, respecting guidance provided by it or by other relevant authorities such as law-enforcement authorities. For example, the need to mitigate an immediate risk of damage would call for prompt communication with data subjects whereas the need to implement appropriate measures against continuing or similar personal data breaches may justify more time for communication.

[5] Cite as: GDPR, Recital 137 | type: recital
There may be an urgent need to act in order to protect the rights and freedoms of data subjects, in particular when the danger exists that the enforcement of a right of a data subject could be considerably impeded. A supervisory authority should therefore be able to adopt duly justified provisional measures on its territory with a specified period of validity which should not exceed three months.
```
</details>

---

## s04 (single)

**Question:** Our social app has users aged 14. Can they consent to us processing their data themselves?

**Reference:** For online services offered directly to a child and relying on consent, the child must be at least 16. Below that age, a parent must give or authorise consent. Member States may lower the age, but not below 13. The controller must make reasonable efforts to verify parental consent.

**Expected:** GDPR, Article 8

**Answer:**

It depends on the law of the EU Member State where your users reside. 

Under the GDPR, when offering information society services (such as a social app) directly to a child based on consent, processing is lawful only if the child is at least 16 years old (GDPR, Article 8(1)). However, EU Member States are allowed by law to lower this age threshold for their country down to 13 years old (GDPR, Article 8(1)). 

This means:
* If a 14-year-old user lives in a Member State that set the age of consent at 16, they **cannot** consent themselves; you must obtain consent authorized by a holder of parental responsibility (GDPR, Article 8(1)).
* If they live in a Member State that lowered the age to 13, 14, or 15, they **can** consent themselves.

Because your users may span multiple EU countries with different national age limits, you need to check the specific age of consent laws in each country where your 14-year-old users are located. You must also make reasonable efforts to verify parental authorization when required, taking available technology into account (GDPR, Article 8(2)). 

As this depends heavily on the user's country of residence and your verification methods, confirm your implementation with a lawyer before launch. The texts provided do not cover later legislative changes by individual Member States.

**Retrieved:** DSA, Article 28; GDPR, Article 14; GDPR, Article 7; GDPR, Article 8; GDPR, Recital 38

<details><summary>search: consent child 14 information society services GDPR Article 8</summary>

```
[1] Cite as: GDPR, Article 8 | type: article — Conditions applicable to child's consent in relation to information society services
1. Where point (a) of Article 6(1) applies, in relation to the offer of information society services directly to a child, the processing of the personal data of a child shall be lawful where the child is at least 16 years old. Where the child is below the age of 16 years, such processing shall be lawful only if and to the extent that consent is given or authorised by the holder of parental responsibility over the child.
Member States may provide by law for a lower age for those purposes provided that such lower age is not below 13 years.
2. The controller shall make reasonable efforts to verify in such cases that consent is given or authorised by the holder of parental responsibility over the child, taking into consideration available technology.
3. Paragraph 1 shall not affect the general contract law of Member States such as the rules on the validity, formation or effect of a contract in relation to a child.

[2] Cite as: GDPR, Recital 38 | type: recital
Children merit specific protection with regard to their personal data, as they may be less aware of the risks, consequences and safeguards concerned and their rights in relation to the processing of personal data. Such specific protection should, in particular, apply to the use of personal data of children for the purposes of marketing or creating personality or user profiles and the collection of personal data with regard to children when using services offered directly to a child. The consent of the holder of parental responsibility should not be necessary in the context of preventive or counselling services offered directly to a child.

[3] Cite as: GDPR, Article 7 | type: article — Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data.
2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding.
3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.
4. When assessing whether consent is freely given, utmost account shall be taken of whether,
inter alia
, the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

[4] Cite as: DSA, Article 28 | type: article — Online protection of minors
1. Providers of online platforms accessible to minors shall put in place appropriate and proportionate measures to ensure a high level of privacy, safety, and security of minors, on their service.
2. Providers of online platform shall not present advertisements on their interface based on profiling as defined in Article 4, point (4), of Regulation (EU) 2016/679 using personal data of the recipient of the service when they are aware with reasonable certainty that the recipient of the service is a minor.
3. Compliance with the obligations set out in this Article shall not oblige providers of online platforms to process additional personal data in order to assess whether the recipient of the service is a minor.
4. The Commission, after consulting the Board, may issue guidelines to assist providers of online platforms in the application of paragraph 1.

[5] Cite as: GDPR, Article 14 | type: article — Information to be provided where personal data have not been obtained from the data subject (part 1 of 2)
1. Where personal data have not been obtained from the data subject, the controller shall provide the data subject with the following information:
(a) the identity and the contact details of the controller and, where applicable, of the controller's representative;
(b) the contact details of the data protection officer, where applicable;
(c) the purposes of the processing for which the personal data are intended as well as the legal basis for the processing;
(d) the categories of personal data concerned;
(e) the recipients or categories of recipients of the personal data, if any;
(f) where applicable, that the controller intends to transfer personal data to a recipient in a third country or international organisation and the existence or absence of an adequacy decision by the Commission, or in the case of transfers referred to in Article 46 or 47, or the second subparagraph of Article 49(1), reference to the appropriate or suitable safeguards and the means to obtain a copy of them or where they have been made available.
2. In addition to the information referred to in paragraph 1, the controller shall provide the data subject with the following information necessary to ensure fair and transparent processing in respect of the data subject:
(a) the period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period;
(b) where the processing is based on point (f) of Article 6(1), the legitimate interests pursued by the controller or by a third party;
(c) the existence of the right to request from the controller access to and rectification or erasure of personal data or restriction of processing concerning the data subject and to object to processing as well as the right to data portability;
(d) where processing is based on point (a) of Article 6(1) or point (a) of Article 9(2), the existence of the right to withdraw consent at any time, without affecting the lawfulness of processing based on consent before its withdrawal;
(e) the right to lodge a complaint with a supervisory authority;
(f) from which source the personal data originate, and if applicable, whether it came from publicly accessible sources;
(g) the existence of automated decision-making, including profiling, referred to in Article 22(1) and (4) and, at least in those cases, meaningful information about the logic involved, as well as the significance and the envisaged consequences of such processing for the data subject.
3. The controller shall provide the information referred to in paragraphs 1 and 2:
(a) within a reasonable period after obtaining the personal data, but at the latest within one month, having regard to the specific circumstances in which the personal data are processed;
(b) if the personal data are to be used for communication with the data subject, at the latest at the time of the first communication to that data subject; or
(c) if a disclosure to another recipient is envisaged, at the latest when the personal data are first disclosed.
4. Where the controller intends to further process the personal data for a purpose other than that for which the personal data were obtained, the controller shall provide the data subject prior to that further processing with information on that other purpose and with any relevant further information as referred to in paragraph 2.
5. Paragraphs 1 to 4 shall not apply where and insofar as:
(a) the data subject already has the information;
```
</details>

---

## s05 (single)

**Question:** We're a 10-person startup. Do we need to appoint a data protection officer?

**Reference:** Company size is not the test. A DPO is required if you are a public authority, if your core activities involve regular and systematic monitoring of people on a large scale, or if your core activities involve large-scale processing of special-category or criminal-conviction data.

**Expected:** GDPR, Article 37

**Answer:**

It depends on your startup's core activities, not your staff size. Being a 10-person company does not automatically exempt you or require you to have a data protection officer (DPO).

You must appoint a DPO only if:
* Your core activities consist of processing operations that require regular and systematic monitoring of data subjects on a large scale (GDPR, Article 37(1)(b)); or
* Your core activities consist of processing special categories of data (such as health data, biometric data, or data revealing racial or ethnic origin) or criminal conviction data on a large scale (GDPR, Article 37(1)(c)); or
* You are a public authority or body (GDPR, Article 37(1)(a)).

If your startup does not fall into these categories, EU law does not require a DPO, though you may still choose to appoint one voluntarily (GDPR, Article 37(4)). Note that individual EU Member States may also enact national laws requiring a DPO in other specific cases (GDPR, Article 37(4)).

Because determining whether your processing qualifies as "large scale" or involves "core activities" depends on the specific nature of your product and data flows, you should confirm your classification with a lawyer before deciding to forgo a DPO.

**Retrieved:** GDPR, Article 37; GDPR, Article 38; GDPR, Article 39; GDPR, Article 54; GDPR, Recital 97

<details><summary>search: data protection officer appointment GDPR Article</summary>

```
[1] Cite as: GDPR, Article 37 | type: article — Designation of the data protection officer
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

[2] Cite as: GDPR, Article 38 | type: article — Position of the data protection officer
1. The controller and the processor shall ensure that the data protection officer is involved, properly and in a timely manner, in all issues which relate to the protection of personal data.
2. The controller and processor shall support the data protection officer in performing the tasks referred to in Article 39 by providing resources necessary to carry out those tasks and access to personal data and processing operations, and to maintain his or her expert knowledge.
3. The controller and processor shall ensure that the data protection officer does not receive any instructions regarding the exercise of those tasks. He or she shall not be dismissed or penalised by the controller or the processor for performing his tasks. The data protection officer shall directly report to the highest management level of the controller or the processor.
4. Data subjects may contact the data protection officer with regard to all issues related to processing of their personal data and to the exercise of their rights under this Regulation.
5. The data protection officer shall be bound by secrecy or confidentiality concerning the performance of his or her tasks, in accordance with Union or Member State law.
6. The data protection officer may fulfil other tasks and duties. The controller or processor shall ensure that any such tasks and duties do not result in a conflict of interests.

[3] Cite as: GDPR, Recital 97 | type: recital
Where the processing is carried out by a public authority, except for courts or independent judicial authorities when acting in their judicial capacity, where, in the private sector, processing is carried out by a controller whose core activities consist of processing operations that require regular and systematic monitoring of the data subjects on a large scale, or where the core activities of the controller or the processor consist of processing on a large scale of special categories of personal data and data relating to criminal convictions and offences, a person with expert knowledge of data protection law and practices should assist the controller or processor to monitor internal compliance with this Regulation. In the private sector, the core activities of a controller relate to its primary activities and do not relate to the processing of personal data as ancillary activities. The necessary level of expert knowledge should be determined in particular according to the data processing operations carried out and the protection required for the personal data processed by the controller or the processor. Such data protection officers, whether or not they are an employee of the controller, should be in a position to perform their duties and tasks in an independent manner.

[4] Cite as: GDPR, Article 39 | type: article — Tasks of the data protection officer
1. The data protection officer shall have at least the following tasks:
(a) to inform and advise the controller or the processor and the employees who carry out processing of their obligations pursuant to this Regulation and to other Union or Member State data protection provisions;
(b) to monitor compliance with this Regulation, with other Union or Member State data protection provisions and with the policies of the controller or processor in relation to the protection of personal data, including the assignment of responsibilities, awareness-raising and training of staff involved in processing operations, and the related audits;
(c) to provide advice where requested as regards the data protection impact assessment and monitor its performance pursuant to Article 35;
(d) to cooperate with the supervisory authority;
(e) to act as the contact point for the supervisory authority on issues relating to processing, including the prior consultation referred to in Article 36, and to consult, where appropriate, with regard to any other matter.
2. The data protection officer shall in the performance of his or her tasks have due regard to the risk associated with processing operations, taking into account the nature, scope, context and purposes of processing.

[5] Cite as: GDPR, Article 54 | type: article — Rules on the establishment of the supervisory authority
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

## s06 (single)

**Question:** We store EU customer data with a US cloud provider. What legal mechanism lets us transfer it there?

**Reference:** Without an adequacy decision, transfers need appropriate safeguards such as standard contractual clauses, binding corporate rules, or approved codes of conduct or certification. Enforceable rights and effective legal remedies must also be available to the people concerned.

**Expected:** GDPR, Article 46

**Answer:**

It depends on whether the US cloud provider participates in a recognized adequacy framework (such as an adequacy decision under GDPR Article 45) or whether you implement appropriate safeguards. 

In the absence of an adequacy decision, you may transfer personal data to a third country only if you provide appropriate safeguards and ensure that enforceable data subject rights and effective legal remedies are available (GDPR, Article 46(1)). 

According to GDPR Article 46(2) and Recital 108, those appropriate safeguards can include:
* Binding corporate rules (BCRs)
* Standard data protection clauses adopted by the Commission or a supervisory authority
* An approved code of conduct or certification mechanism with binding and enforceable commitments in the third country

You can also use contractual clauses or administrative arrangements subject to authorization from the competent supervisory authority (GDPR, Article 46(3)).

Because international data transfers and cloud compliance involve complex assessments regarding US surveillance laws and supplementary technical measures, you should confirm your transfer mechanism with a lawyer before launch.

**Retrieved:** GDPR, Article 45; GDPR, Article 46; GDPR, Recital 103; GDPR, Recital 108; GDPR, Recital 114

<details><summary>search: transfer third country adequate safeguards binding corporate rules standard contractual clauses</summary>

```
[1] Cite as: GDPR, Recital 108 | type: recital
In the absence of an adequacy decision, the controller or processor should take measures to compensate for the lack of data protection in a third country by way of appropriate safeguards for the data subject. Such appropriate safeguards may consist of making use of binding corporate rules, standard data protection clauses adopted by the Commission, standard data protection clauses adopted by a supervisory authority or contractual clauses authorised by a supervisory authority. Those safeguards should ensure compliance with data protection requirements and the rights of the data subjects appropriate to processing within the Union, including the availability of enforceable data subject rights and of effective legal remedies, including to obtain effective administrative or judicial redress and to claim compensation, in the Union or in a third country. They should relate in particular to compliance with the general principles relating to personal data processing, the principles of data protection by design and by default. Transfers may also be carried out by public authorities or bodies with public authorities or bodies in third countries or with international organisations with corresponding duties or functions, including on the basis of provisions to be inserted into administrative arrangements, such as a memorandum of understanding, providing for enforceable and effective rights for data subjects. Authorisation by the competent supervisory authority should be obtained when the safeguards are provided for in administrative arrangements that are not legally binding.

[2] Cite as: GDPR, Article 46 | type: article — Transfers subject to appropriate safeguards
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
5. Authorisations by a Member State or supervisory authority on the basis of Article 26(2) of Directive 95/46/EC shall remain valid until amended, replaced or repealed, if necessary, by that supervisory authority. Decisions adopted by the Commission on the basis of Article 26(4) of Directive 95/46/EC shall remain in force until amended, replaced or repealed, if necessary, by a Commission Decision adopted in accordance with paragraph 2 of this Article.

[3] Cite as: GDPR, Recital 114 | type: recital
In any case, where the Commission has taken no decision on the adequate level of data protection in a third country, the controller or processor should make use of solutions that provide data subjects with enforceable and effective rights as regards the processing of their data in the Union once those data have been transferred so that that they will continue to benefit from fundamental rights and safeguards.

[4] Cite as: GDPR, Article 45 | type: article — Transfers on the basis of an adequacy decision (part 1 of 2)
1. A transfer of personal data to a third country or an international organisation may take place where the Commission has decided that the third country, a territory or one or more specified sectors within that third country, or the international organisation in question ensures an adequate level of protection. Such a transfer shall not require any specific authorisation.
2. When assessing the adequacy of the level of protection, the Commission shall, in particular, take account of the following elements:
(a) the rule of law, respect for human rights and fundamental freedoms, relevant legislation, both general and sectoral, including concerning public security, defence, national security and criminal law and the access of public authorities to personal data, as well as the implementation of such legislation, data protection rules, professional rules and security measures, including rules for the onward transfer of personal data to another third country or international organisation which are complied with in that country or international organisation, case-law, as well as effective and enforceable data subject rights and effective administrative and judicial redress for the data subjects whose personal data are being transferred;
(b) the existence and effective functioning of one or more independent supervisory authorities in the third country or to which an international organisation is subject, with responsibility for ensuring and enforcing compliance with the data protection rules, including adequate enforcement powers, for assisting and advising the data subjects in exercising their rights and for cooperation with the supervisory authorities of the Member States; and
(c) the international commitments the third country or international organisation concerned has entered into, or other obligations arising from legally binding conventions or instruments as well as from its participation in multilateral or regional systems, in particular in relation to the protection of personal data.
3. The Commission, after assessing the adequacy of the level of protection, may decide, by means of implementing act, that a third country, a territory or one or more specified sectors within a third country, or an international organisation ensures an adequate level of protection within the meaning of paragraph 2 of this Article. The implementing act shall provide for a mechanism for a periodic review, at least every four years, which shall take into account all relevant developments in the third country or international organisation. The implementing act shall specify its territorial and sectoral application and, where applicable, identify the supervisory authority or authorities referred to in point (b) of paragraph 2 of this Article. The implementing act shall be adopted in accordance with the examination procedure referred to in Article 93(2).
4. The Commission shall, on an ongoing basis, monitor developments in third countries and international organisations that could affect the functioning of decisions adopted pursuant to paragraph 3 of this Article and decisions adopted on the basis of Article 25(6) of Directive 95/46/EC.
5. The Commission shall, where available information reveals, in particular following the review referred to in paragraph 3 of this Article, that a third country, a territory or one or more specified sectors within a third country, or an international organisation no longer ensures an adequate level of protection within the meaning of paragraph 2 of this Article, to the extent necessary, repeal, amend or suspend the decision referred to in paragraph 3 of this Article by means of implementing acts without retro-active effect. Those implementing acts shall be adopted in accordance with the examination procedure referred to in Article 93(2).
On duly justified imperative grounds of urgency, the Commission shall adopt immediately applicable implementing acts in accordance with the procedure referred to in Article 93(3).

[5] Cite as: GDPR, Recital 103 | type: recital
The Commission may decide with effect for the entire Union that a third country, a territory or specified sector within a third country, or an international organisation, offers an adequate level of data protection, thus providing legal certainty and uniformity throughout the Union as regards the third country or international organisation which is considered to provide such level of protection. In such cases, transfers of personal data to that third country or international organisation may take place without the need to obtain any further authorisation. The Commission may also decide, having given notice and a full statement setting out the reasons to the third country or international organisation, to revoke such a decision.
```
</details>

---

## s07 (single)

**Question:** We're building a customer-support chatbot. Do we have to tell users they're talking to an AI?

**Reference:** Yes. Providers must design AI systems that interact directly with people so that those people are informed they are interacting with an AI system, unless this is obvious from the context to a reasonably well-informed person.

**Expected:** AI Act, Article 50

**Answer:**

Yes, generally you must tell users they are interacting with an AI system. 

Under the AI Act, providers of AI systems intended to interact directly with natural persons must design and develop them so that users are informed that they are interacting with an AI (AI Act, Article 50(1)). 

There is only one exception: you do not need to notify users if it is already "obvious from the point of view of a natural person who is reasonably well-informed, observant and circumspect, taking into account the circumstances and the context of use" (AI Act, Article 50(1)). For a standard customer-support chatbot where users might not immediately realize they are speaking to software rather than a human agent, relying on this exception is risky, so disclosure is required.

When you provide this notice, it must be given in a "clear and distinguishable manner at the latest at the time of the first interaction or exposure" and conform to accessibility requirements (AI Act, Article 50(5)). 

Because liability depends on the exact context and design of your chatbot, you should consult a lawyer before launch to confirm whether your disclosure setup meets these requirements. The corpus does not cover subsequent amendments, national laws, or enforcement practices.

**Retrieved:** AI Act, Article 50; AI Act, Recital 119; AI Act, Recital 132; AI Act, Recital 134; AI Act, Recital 137

<details><summary>search: chatbot AI transparency disclosure AI Act</summary>

```
[1] Cite as: AI Act, Recital 132 | type: recital
Certain AI systems intended to interact with natural persons or to generate content may pose specific risks of impersonation or deception irrespective of whether they qualify as high-risk or not. In certain circumstances, the use of these systems should therefore be subject to specific transparency obligations without prejudice to the requirements and obligations for high-risk AI systems and subject to targeted exceptions to take into account the special need of law enforcement. In particular, natural persons should be notified that they are interacting with an AI system, unless this is obvious from the point of view of a natural person who is reasonably well-informed, observant and circumspect taking into account the circumstances and the context of use. When implementing that obligation, the characteristics of natural persons belonging to vulnerable groups due to their age or disability should be taken into account to the extent the AI system is intended to interact with those groups as well. Moreover, natural persons should be notified when they are exposed to AI systems that, by processing their biometric data, can identify or infer the emotions or intentions of those persons or assign them to specific categories. Such specific categories can relate to aspects such as sex, age, hair colour, eye colour, tattoos, personal traits, ethnic origin, personal preferences and interests. Such information and notifications should be provided in accessible formats for persons with disabilities.

[2] Cite as: AI Act, Article 50 | type: article — Transparency obligations for providers and deployers of certain AI systems (part 1 of 2)
1. Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system, unless this is obvious from the point of view of a natural person who is reasonably well-informed, observant and circumspect, taking into account the circumstances and the context of use. This obligation shall not apply to AI systems authorised by law to detect, prevent, investigate or prosecute criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, unless those systems are available for the public to report a criminal offence.
2. Providers of AI systems, including general-purpose AI systems, generating synthetic audio, image, video or text content, shall ensure that the outputs of the AI system are marked in a machine-readable format and detectable as artificially generated or manipulated. Providers shall ensure their technical solutions are effective, interoperable, robust and reliable as far as this is technically feasible, taking into account the specificities and limitations of various types of content, the costs of implementation and the generally acknowledged state of the art, as may be reflected in relevant technical standards. This obligation shall not apply to the extent the AI systems perform an assistive function for standard editing or do not substantially alter the input data provided by the deployer or the semantics thereof, or where authorised by law to detect, prevent, investigate or prosecute criminal offences.
3. Deployers of an emotion recognition system or a biometric categorisation system shall inform the natural persons exposed thereto of the operation of the system, and shall process the personal data in accordance with Regulations (EU) 2016/679 and (EU) 2018/1725 and Directive (EU) 2016/680, as applicable. This obligation shall not apply to AI systems used for biometric categorisation and emotion recognition, which are permitted by law to detect, prevent or investigate criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, and in accordance with Union law.
4. Deployers of an AI system that generates or manipulates image, audio or video content constituting a deep fake, shall disclose that the content has been artificially generated or manipulated. This obligation shall not apply where the use is authorised by law to detect, prevent, investigate or prosecute criminal offence. Where the content forms part of an evidently artistic, creative, satirical, fictional or analogous work or programme, the transparency obligations set out in this paragraph are limited to disclosure of the existence of such generated or manipulated content in an appropriate manner that does not hamper the display or enjoyment of the work.
Deployers of an AI system that generates or manipulates text which is published with the purpose of informing the public on matters of public interest shall disclose that the text has been artificially generated or manipulated. This obligation shall not apply where the use is authorised by law to detect, prevent, investigate or prosecute criminal offences or where the AI-generated content has undergone a process of human review or editorial control and where a natural or legal person holds editorial responsibility for the publication of the content.
5. The information referred to in paragraphs 1 to 4 shall be provided to the natural persons concerned in a clear and distinguishable manner at the latest at the time of the first interaction or exposure. The information shall conform to the applicable accessibility requirements.

[3] Cite as: AI Act, Recital 137 | type: recital
Compliance with the transparency obligations for the AI systems covered by this Regulation should not be interpreted as indicating that the use of the AI system or its output is lawful under this Regulation or other Union and Member State law and should be without prejudice to other transparency obligations for deployers of AI systems laid down in Union or national law.

[4] Cite as: AI Act, Recital 134 | type: recital
Further to the technical solutions employed by the providers of the AI system, deployers who use an AI system to generate or manipulate image, audio or video content that appreciably resembles existing persons, objects, places, entities or events and would falsely appear to a person to be authentic or truthful (deep fakes), should also clearly and distinguishably disclose that the content has been artificially created or manipulated by labelling the AI output accordingly and disclosing its artificial origin. Compliance with this transparency obligation should not be interpreted as indicating that the use of the AI system or its output impedes the right to freedom of expression and the right to freedom of the arts and sciences guaranteed in the Charter, in particular where the content is part of an evidently creative, satirical, artistic, fictional or analogous work or programme, subject to appropriate safeguards for the rights and freedoms of third parties. In those cases, the transparency obligation for deep fakes set out in this Regulation is limited to disclosure of the existence of such generated or manipulated content in an appropriate manner that does not hamper the display or enjoyment of the work, including its normal exploitation and use, while maintaining the utility and quality of the work. In addition, it is also appropriate to envisage a similar disclosure obligation in relation to AI-generated or manipulated text to the extent it is published with the purpose of informing the public on matters of public interest unless the AI-generated content has undergone a process of human review or editorial control and a natural or legal person holds editorial responsibility for the publication of the content.

[5] Cite as: AI Act, Recital 119 | type: recital
Considering the quick pace of innovation and the technological evolution of digital services in scope of different instruments of Union law in particular having in mind the usage and the perception of their recipients, the AI systems subject to this Regulation may be provided as intermediary services or parts thereof within the meaning of Regulation (EU) 2022/2065, which should be interpreted in a technology-neutral manner. For example, AI systems may be used to provide online search engines, in particular, to the extent that an AI system such as an online chatbot performs searches of, in principle, all websites, then incorporates the results into its existing knowledge and uses the updated knowledge to generate a single output that combines different sources of information.
```
</details>

---

## s08 (single)

**Question:** Can we build a feature that uses AI to detect how stressed our employees are at work from their faces and voices?

**Reference:** No. Placing on the market or using AI systems to infer the emotions of people in the workplace or in education institutions is prohibited, except for medical or safety reasons.

**Expected:** AI Act, Article 5

**Answer:**

**No**, you cannot build or launch this feature. 

The AI Act explicitly prohibits placing on the market, putting into service, or using AI systems to infer the emotions of individuals in the areas of the workplace and educational institutions, unless the system is strictly for medical or safety reasons (such as therapeutic use) (AI Act, Article 5). 

Because your feature is designed to detect employee stress at work from faces and voices, it falls squarely under this workplace emotion-recognition prohibition.

### Key points from the law:
* **Prohibited Practice:** Using AI to infer emotions in the workplace is classified as a prohibited practice under EU law (AI Act, Article 5).
* **Scope:** The prohibition covers emotion recognition based on biometric data such as facial expressions and voice characteristics (AI Act, Recital 18, Recital 44).
* **Exceptions:** The only permitted exceptions are systems used strictly for medical or safety reasons (e.g., therapeutic use or fatigue-monitoring for professional drivers or pilots to prevent accidents) (AI Act, Recital 18, Recital 44, Article 5). Routine workplace stress monitoring is not exempt.

Because this feature violates a core prohibition of the AI Act, you should confirm with legal counsel before planning any development or deployment in this area.

**Retrieved:** AI Act, Article 5; AI Act, Recital 18; AI Act, Recital 44; AI Act, Recital 54; AI Act, Recital 57; AI Act, Recital 63

<details><summary>search: emotion recognition workplace AI Act</summary>

```
[1] Cite as: AI Act, Recital 44 | type: recital
There are serious concerns about the scientific basis of AI systems aiming to identify or infer emotions, particularly as expression of emotions vary considerably across cultures and situations, and even within a single individual. Among the key shortcomings of such systems are the limited reliability, the lack of specificity and the limited generalisability. Therefore, AI systems identifying or inferring emotions or intentions of natural persons on the basis of their biometric data may lead to discriminatory outcomes and can be intrusive to the rights and freedoms of the concerned persons. Considering the imbalance of power in the context of work or education, combined with the intrusive nature of these systems, such systems could lead to detrimental or unfavourable treatment of certain natural persons or whole groups thereof. Therefore, the placing on the market, the putting into service, or the use of AI systems intended to be used to detect the emotional state of individuals in situations related to the workplace and education should be prohibited. That prohibition should not cover AI systems placed on the market strictly for medical or safety reasons, such as systems intended for therapeutical use.

[2] Cite as: AI Act, Recital 18 | type: recital
The notion of ‘emotion recognition system’ referred to in this Regulation should be defined as an AI system for the purpose of identifying or inferring emotions or intentions of natural persons on the basis of their biometric data. The notion refers to emotions or intentions such as happiness, sadness, anger, surprise, disgust, embarrassment, excitement, shame, contempt, satisfaction and amusement. It does not include physical states, such as pain or fatigue, including, for example, systems used in detecting the state of fatigue of professional pilots or drivers for the purpose of preventing accidents. This does also not include the mere detection of readily apparent expressions, gestures or movements, unless they are used for identifying or inferring emotions. Those expressions can be basic facial expressions, such as a frown or a smile, or gestures such as the movement of hands, arms or head, or characteristics of a person’s voice, such as a raised voice or whispering.

[3] Cite as: AI Act, Recital 63 | type: recital
The fact that an AI system is classified as a high-risk AI system under this Regulation should not be interpreted as indicating that the use of the system is lawful under other acts of Union law or under national law compatible with Union law, such as on the protection of personal data, on the use of polygraphs and similar tools or other systems to detect the emotional state of natural persons. Any such use should continue to occur solely in accordance with the applicable requirements resulting from the Charter and from the applicable acts of secondary Union law and national law. This Regulation should not be understood as providing for the legal ground for processing of personal data, including special categories of personal data, where relevant, unless it is specifically otherwise provided for in this Regulation.

[4] Cite as: AI Act, Recital 54 | type: recital
As biometric data constitutes a special category of personal data, it is appropriate to classify as high-risk several critical-use cases of biometric systems, insofar as their use is permitted under relevant Union and national law. Technical inaccuracies of AI systems intended for the remote biometric identification of natural persons can lead to biased results and entail discriminatory effects. The risk of such biased results and discriminatory effects is particularly relevant with regard to age, ethnicity, race, sex or disabilities. Remote biometric identification systems should therefore be classified as high-risk in view of the risks that they pose. Such a classification excludes AI systems intended to be used for biometric verification, including authentication, the sole purpose of which is to confirm that a specific natural person is who that person claims to be and to confirm the identity of a natural person for the sole purpose of having access to a service, unlocking a device or having secure access to premises. In addition, AI systems intended to be used for biometric categorisation according to sensitive attributes or characteristics protected under Article 9(1) of Regulation (EU) 2016/679 on the basis of biometric data, in so far as these are not prohibited under this Regulation, and emotion recognition systems that are not prohibited under this Regulation, should be classified as high-risk. Biometric systems which are intended to be used solely for the purpose of enabling cybersecurity and personal data protection measures should not be considered to be high-risk AI systems.

[5] Cite as: AI Act, Recital 57 | type: recital
AI systems used in employment, workers management and access to self-employment, in particular for the recruitment and selection of persons, for making decisions affecting terms of the work-related relationship, promotion and termination of work-related contractual relationships, for allocating tasks on the basis of individual behaviour, personal traits or characteristics and for monitoring or evaluation of persons in work-related contractual relationships, should also be classified as high-risk, since those systems may have an appreciable impact on future career prospects, livelihoods of those persons and workers’ rights. Relevant work-related contractual relationships should, in a meaningful manner, involve employees and persons providing services through platforms as referred to in the Commission Work Programme 2021. Throughout the recruitment process and in the evaluation, promotion, or retention of persons in work-related contractual relationships, such systems may perpetuate historical patterns of discrimination, for example against women, certain age groups, persons with disabilities, or persons of certain racial or ethnic origins or sexual orientation. AI systems used to monitor the performance and behaviour of such persons may also undermine their fundamental rights to data protection and privacy.
```
</details>

<details><summary>search: Article 5 AI Act prohibited practices emotion recognition workplace</summary>

```
[1] Cite as: AI Act, Recital 44 | type: recital
There are serious concerns about the scientific basis of AI systems aiming to identify or infer emotions, particularly as expression of emotions vary considerably across cultures and situations, and even within a single individual. Among the key shortcomings of such systems are the limited reliability, the lack of specificity and the limited generalisability. Therefore, AI systems identifying or inferring emotions or intentions of natural persons on the basis of their biometric data may lead to discriminatory outcomes and can be intrusive to the rights and freedoms of the concerned persons. Considering the imbalance of power in the context of work or education, combined with the intrusive nature of these systems, such systems could lead to detrimental or unfavourable treatment of certain natural persons or whole groups thereof. Therefore, the placing on the market, the putting into service, or the use of AI systems intended to be used to detect the emotional state of individuals in situations related to the workplace and education should be prohibited. That prohibition should not cover AI systems placed on the market strictly for medical or safety reasons, such as systems intended for therapeutical use.

[2] Cite as: AI Act, Article 5 | type: article — Prohibited AI practices (part 1 of 4)
1. The following AI practices shall be prohibited:
(a) the placing on the market, the putting into service or the use of an AI system that deploys subliminal techniques beyond a person’s consciousness or purposefully manipulative or deceptive techniques, with the objective, or the effect of materially distorting the behaviour of a person or a group of persons by appreciably impairing their ability to make an informed decision, thereby causing them to take a decision that they would not have otherwise taken in a manner that causes or is reasonably likely to cause that person, another person or group of persons significant harm;
(b) the placing on the market, the putting into service or the use of an AI system that exploits any of the vulnerabilities of a natural person or a specific group of persons due to their age, disability or a specific social or economic situation, with the objective, or the effect, of materially distorting the behaviour of that person or a person belonging to that group in a manner that causes or is reasonably likely to cause that person or another person significant harm;
(c) the placing on the market, the putting into service or the use of AI systems for the evaluation or classification of natural persons or groups of persons over a certain period of time based on their social behaviour or known, inferred or predicted personal or personality characteristics, with the social score leading to either or both of the following:
(i) detrimental or unfavourable treatment of certain natural persons or groups of persons in social contexts that are unrelated to the contexts in which the data was originally generated or collected;
(ii) detrimental or unfavourable treatment of certain natural persons or groups of persons that is unjustified or disproportionate to their social behaviour or its gravity;
(d) the placing on the market, the putting into service for this specific purpose, or the use of an AI system for making risk assessments of natural persons in order to assess or predict the risk of a natural person committing a criminal offence, based solely on the profiling of a natural person or on assessing their personality traits and characteristics; this prohibition shall not apply to AI systems used to support the human assessment of the involvement of a person in a criminal activity, which is already based on objective and verifiable facts directly linked to a criminal activity;
(e) the placing on the market, the putting into service for this specific purpose, or the use of AI systems that create or expand facial recognition databases through the untargeted scraping of facial images from the internet or CCTV footage;
(f) the placing on the market, the putting into service for this specific purpose, or the use of AI systems to infer emotions of a natural person in the areas of workplace and education institutions, except where the use of the AI system is intended to be put in place or into the market for medical or safety reasons;
(g) the placing on the market, the putting into service for this specific purpose, or the use of biometric categorisation systems that categorise individually natural persons based on their biometric data to deduce or infer their race, political opinions, trade union membership, religious or philosophical beliefs, sex life or sexual orientation; this prohibition does not cover any labelling or filtering of lawfully acquired biometric datasets, such as images, based on biometric data or categorizing of biometric data in the area of law enforcement;

[3] Cite as: AI Act, Article 5 | type: article — Prohibited AI practices (part 2 of 4)
(h) the use of ‘real-time’ remote biometric identification systems in publicly accessible spaces for the purposes of law enforcement, unless and in so far as such use is strictly necessary for one of the following objectives:
(i) the targeted search for specific victims of abduction, trafficking in human beings or sexual exploitation of human beings, as well as the search for missing persons;
(ii) the prevention of a specific, substantial and imminent threat to the life or physical safety of natural persons or a genuine and present or genuine and foreseeable threat of a terrorist attack;
(iii) the localisation or identification of a person suspected of having committed a criminal offence, for the purpose of conducting a criminal investigation or prosecution or executing a criminal penalty for offences referred to in Annex II and punishable in the Member State concerned by a custodial sentence or a detention order for a maximum period of at least four years.
Point (h) of the first subparagraph is without prejudice to Article 9 of Regulation (EU) 2016/679 for the processing of biometric data for purposes other than law enforcement.
2. The use of ‘real-time’ remote biometric identification systems in publicly accessible spaces for the purposes of law enforcement for any of the objectives referred to in paragraph 1, first subparagraph, point (h), shall be deployed for the purposes set out in that point only to confirm the identity of the specifically targeted individual, and it shall take into account the following elements:
(a) the nature of the situation giving rise to the possible use, in particular the seriousness, probability and scale of the harm that would be caused if the system were not used;
(b) the consequences of the use of the system for the rights and freedoms of all persons concerned, in particular the seriousness, probability and scale of those consequences.
In addition, the use of ‘real-time’ remote biometric identification systems in publicly accessible spaces for the purposes of law enforcement for any of the objectives referred to in paragraph 1, first subparagraph, point (h), of this Article shall comply with necessary and proportionate safeguards and conditions in relation to the use in accordance with the national law authorising the use thereof, in particular as regards the temporal, geographic and personal limitations. The use of the ‘real-time’ remote biometric identification system in publicly accessible spaces shall be authorised only if the law enforcement authority has completed a fundamental rights impact assessment as provided for in Article 27 and has registered the system in the EU database according to Article 49. However, in duly justified cases of urgency, the use of such systems may be commenced without the registration in the EU database, provided that such registration is completed without undue delay.

[4] Cite as: AI Act, Recital 18 | type: recital
The notion of ‘emotion recognition system’ referred to in this Regulation should be defined as an AI system for the purpose of identifying or inferring emotions or intentions of natural persons on the basis of their biometric data. The notion refers to emotions or intentions such as happiness, sadness, anger, surprise, disgust, embarrassment, excitement, shame, contempt, satisfaction and amusement. It does not include physical states, such as pain or fatigue, including, for example, systems used in detecting the state of fatigue of professional pilots or drivers for the purpose of preventing accidents. This does also not include the mere detection of readily apparent expressions, gestures or movements, unless they are used for identifying or inferring emotions. Those expressions can be basic facial expressions, such as a frown or a smile, or gestures such as the movement of hands, arms or head, or characteristics of a person’s voice, such as a raised voice or whispering.

[5] Cite as: AI Act, Article 5 | type: article — Prohibited AI practices (part 3 of 4)
3. For the purposes of paragraph 1, first subparagraph, point (h) and paragraph 2, each use for the purposes of law enforcement of a ‘real-time’ remote biometric identification system in publicly accessible spaces shall be subject to a prior authorisation granted by a judicial authority or an independent administrative authority whose decision is binding of the Member State in which the use is to take place, issued upon a reasoned request and in accordance with the detailed rules of national law referred to in paragraph 5. However, in a duly justified situation of urgency, the use of such system may be commenced without an authorisation provided that such authorisation is requested without undue delay, at the latest within 24 hours. If such authorisation is rejected, the use shall be stopped with immediate effect and all the data, as well as the results and outputs of that use shall be immediately discarded and deleted.
The competent judicial authority or an independent administrative authority whose decision is binding shall grant the authorisation only where it is satisfied, on the basis of objective evidence or clear indications presented to it, that the use of the ‘real-time’ remote biometric identification system concerned is necessary for, and proportionate to, achieving one of the objectives specified in paragraph 1, first subparagraph, point (h), as identified in the request and, in particular, remains limited to what is strictly necessary concerning the period of time as well as the geographic and personal scope. In deciding on the request, that authority shall take into account the elements referred to in paragraph 2. No decision that produces an adverse legal effect on a person may be taken based solely on the output of the ‘real-time’ remote biometric identification system.
4. Without prejudice to paragraph 3, each use of a ‘real-time’ remote biometric identification system in publicly accessible spaces for law enforcement purposes shall be notified to the relevant market surveillance authority and the national data protection authority in accordance with the national rules referred to in paragraph 5. The notification shall, as a minimum, contain the information specified under paragraph 6 and shall not include sensitive operational data.
5. A Member State may decide to provide for the possibility to fully or partially authorise the use of ‘real-time’ remote biometric identification systems in publicly accessible spaces for the purposes of law enforcement within the limits and under the conditions listed in paragraph 1, first subparagraph, point (h), and paragraphs 2 and 3. Member States concerned shall lay down in their national law the necessary detailed rules for the request, issuance and exercise of, as well as supervision and reporting relating to, the authorisations referred to in paragraph 3. Those rules shall also specify in respect of which of the objectives listed in paragraph 1, first subparagraph, point (h), including which of the criminal offences referred to in point (h)(iii) thereof, the competent authorities may be authorised to use those systems for the purposes of law enforcement. Member States shall notify those rules to the Commission at the latest 30 days following the adoption thereof. Member States may introduce, in accordance with Union law, more restrictive laws on the use of remote biometric identification systems.
```
</details>

---

## s09 (single)

**Question:** Our product uses AI to filter and rank job applicants. Is that considered high-risk?

**Reference:** Yes. Annex III, point 4 (employment) lists AI systems used for recruitment or selection, in particular to place targeted job ads, analyse and filter applications, and evaluate candidates. Article 6(3) allows narrow exceptions where the system does not pose a significant risk.

**Expected:** AI Act, Annex III

**Answer:**

Yes, your AI system is considered **high-risk** (AI Act, Annex III). 

Under the AI Act, high-risk AI systems include those intended to be used for the recruitment or selection of natural persons—specifically to place targeted job advertisements, to **analyse and filter job applications**, and to **evaluate candidates** (AI Act, Annex III). 

Recital 57 explains that such systems are classified as high-risk because they may have an appreciable impact on future career prospects, livelihoods, and workers' rights, and may perpetuate historical patterns of discrimination (AI Act, Recital 57).

Because high-risk classification carries strict regulatory requirements regarding transparency, data governance, human oversight, and conformity assessments, we strongly recommend confirming your compliance obligations with a lawyer before launch.

**Retrieved:** AI Act, Annex III; AI Act, Recital 56; AI Act, Recital 57

<details><summary>search: job applicants employment high risk AI Act Annex III</summary>

```
[1] Cite as: AI Act, Annex III | type: annex — High-risk AI systems referred to in Article 6(2) (part 1 of 3)
High-risk AI systems pursuant to Article 6(2) are the AI systems listed in any of the following areas:
1. Biometrics, in so far as their use is permitted under relevant Union or national law:
(a) remote biometric identification systems.
This shall not include AI systems intended to be used for biometric verification the sole purpose of which is to confirm that a specific natural person is the person he or she claims to be;
(b) AI systems intended to be used for biometric categorisation, according to sensitive or protected attributes or characteristics based on the inference of those attributes or characteristics;
(c) AI systems intended to be used for emotion recognition.
2. Critical infrastructure: AI systems intended to be used as safety components in the management and operation of critical digital infrastructure, road traffic, or in the supply of water, gas, heating or electricity.
3. Education and vocational training:
(a) AI systems intended to be used to determine access or admission or to assign natural persons to educational and vocational training institutions at all levels;
(b) AI systems intended to be used to evaluate learning outcomes, including when those outcomes are used to steer the learning process of natural persons in educational and vocational training institutions at all levels;
(c) AI systems intended to be used for the purpose of assessing the appropriate level of education that an individual will receive or will be able to access, in the context of or within educational and vocational training institutions at all levels;
(d) AI systems intended to be used for monitoring and detecting prohibited behaviour of students during tests in the context of or within educational and vocational training institutions at all levels.
4. Employment, workers’ management and access to self-employment:
(a) AI systems intended to be used for the recruitment or selection of natural persons, in particular to place targeted job advertisements, to analyse and filter job applications, and to evaluate candidates;
(b) AI systems intended to be used to make decisions affecting terms of work-related relationships, the promotion or termination of work-related contractual relationships, to allocate tasks based on individual behaviour or personal traits or characteristics or to monitor and evaluate the performance and behaviour of persons in such relationships.
5. Access to and enjoyment of essential private services and essential public services and benefits:
(a) AI systems intended to be used by public authorities or on behalf of public authorities to evaluate the eligibility of natural persons for essential public assistance benefits and services, including healthcare services, as well as to grant, reduce, revoke, or reclaim such benefits and services;
(b) AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score, with the exception of AI systems used for the purpose of detecting financial fraud;
(c) AI systems intended to be used for risk assessment and pricing in relation to natural persons in the case of life and health insurance;
(d) AI systems intended to evaluate and classify emergency calls by natural persons or to be used to dispatch, or to establish priority in the dispatching of, emergency first response services, including by police, firefighters and medical aid, as well as of emergency healthcare patient triage systems.
6. Law enforcement, in so far as their use is permitted under relevant Union or national law:

[2] Cite as: AI Act, Recital 57 | type: recital
AI systems used in employment, workers management and access to self-employment, in particular for the recruitment and selection of persons, for making decisions affecting terms of the work-related relationship, promotion and termination of work-related contractual relationships, for allocating tasks on the basis of individual behaviour, personal traits or characteristics and for monitoring or evaluation of persons in work-related contractual relationships, should also be classified as high-risk, since those systems may have an appreciable impact on future career prospects, livelihoods of those persons and workers’ rights. Relevant work-related contractual relationships should, in a meaningful manner, involve employees and persons providing services through platforms as referred to in the Commission Work Programme 2021. Throughout the recruitment process and in the evaluation, promotion, or retention of persons in work-related contractual relationships, such systems may perpetuate historical patterns of discrimination, for example against women, certain age groups, persons with disabilities, or persons of certain racial or ethnic origins or sexual orientation. AI systems used to monitor the performance and behaviour of such persons may also undermine their fundamental rights to data protection and privacy.

[3] Cite as: AI Act, Annex III | type: annex — High-risk AI systems referred to in Article 6(2) (part 2 of 3)
(a) AI systems intended to be used by or on behalf of law enforcement authorities, or by Union institutions, bodies, offices or agencies in support of law enforcement authorities or on their behalf to assess the risk of a natural person becoming the victim of criminal offences;
(b) AI systems intended to be used by or on behalf of law enforcement authorities or by Union institutions, bodies, offices or agencies in support of law enforcement authorities as polygraphs or similar tools;
(c) AI systems intended to be used by or on behalf of law enforcement authorities, or by Union institutions, bodies, offices or agencies, in support of law enforcement authorities to evaluate the reliability of evidence in the course of the investigation or prosecution of criminal offences;
(d) AI systems intended to be used by law enforcement authorities or on their behalf or by Union institutions, bodies, offices or agencies in support of law enforcement authorities for assessing the risk of a natural person offending or re-offending not solely on the basis of the profiling of natural persons as referred to in Article 3(4) of Directive (EU) 2016/680, or to assess personality traits and characteristics or past criminal behaviour of natural persons or groups;
(e) AI systems intended to be used by or on behalf of law enforcement authorities or by Union institutions, bodies, offices or agencies in support of law enforcement authorities for the profiling of natural persons as referred to in Article 3(4) of Directive (EU) 2016/680 in the course of the detection, investigation or prosecution of criminal offences.
7. Migration, asylum and border control management, in so far as their use is permitted under relevant Union or national law:
(a) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies as polygraphs or similar tools;
(b) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies to assess a risk, including a security risk, a risk of irregular migration, or a health risk, posed by a natural person who intends to enter or who has entered into the territory of a Member State;
(c) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies to assist competent public authorities for the examination of applications for asylum, visa or residence permits and for associated complaints with regard to the eligibility of the natural persons applying for a status, including related assessments of the reliability of evidence;
(d) AI systems intended to be used by or on behalf of competent public authorities, or by Union institutions, bodies, offices or agencies, in the context of migration, asylum or border control management, for the purpose of detecting, recognising or identifying natural persons, with the exception of the verification of travel documents.
8. Administration of justice and democratic processes:
(a) AI systems intended to be used by a judicial authority or on their behalf to assist a judicial authority in researching and interpreting facts and the law and in applying the law to a concrete set of facts, or to be used in a similar way in alternative dispute resolution;

[4] Cite as: AI Act, Annex III | type: annex — High-risk AI systems referred to in Article 6(2) (part 3 of 3)
(b) AI systems intended to be used for influencing the outcome of an election or referendum or the voting behaviour of natural persons in the exercise of their vote in elections or referenda. This does not include AI systems to the output of which natural persons are not directly exposed, such as tools used to organise, optimise or structure political campaigns from an administrative or logistical point of view.

[5] Cite as: AI Act, Recital 56 | type: recital
The deployment of AI systems in education is important to promote high-quality digital education and training and to allow all learners and teachers to acquire and share the necessary digital skills and competences, including media literacy, and critical thinking, to take an active part in the economy, society, and in democratic processes. However, AI systems used in education or vocational training, in particular for determining access or admission, for assigning persons to educational and vocational training institutions or programmes at all levels, for evaluating learning outcomes of persons, for assessing the appropriate level of education for an individual and materially influencing the level of education and training that individuals will receive or will be able to access or for monitoring and detecting prohibited behaviour of students during tests should be classified as high-risk AI systems, since they may determine the educational and professional course of a person’s life and therefore may affect that person’s ability to secure a livelihood. When improperly designed and used, such systems may be particularly intrusive and may violate the right to education and training as well as the right not to be discriminated against and perpetuate historical patterns of discrimination, for example against women, certain age groups, persons with disabilities, or persons of certain racial or ethnic origins or sexual orientation.
```
</details>

---

## s10 (single)

**Question:** We bought a high-risk AI tool from a vendor and use it internally. What do we have to do as the user?

**Reference:** As a deployer you must use the system according to the provider's instructions; assign human oversight to competent, trained people; make sure input data under your control is relevant and representative; monitor the system and inform the provider of risks or incidents; keep automatically generated logs for at least six months; inform workers' representatives before using it in the workplace; and inform people subject to its decisions.

**Expected:** AI Act, Article 26

**Answer:**

As a deployer using an internal high-risk AI system, you must take several technical, organizational, and operational steps under the AI Act (Article 26):

* **Follow instructions:** Use the system in accordance with the vendor's instructions for use (AI Act, Article 26(1)).
* **Assign human oversight:** Designate natural persons with the necessary competence, training, authority, and support to oversee the system's operation (AI Act, Article 26(2)).
* **Ensure relevant input data:** To the extent you control the input data, ensure it is relevant and sufficiently representative for the system's intended purpose (AI Act, Article 26(4)).
* **Monitor and report:** Monitor the system's operation based on the instructions for use. If you have reason to believe the system presents a risk, you must suspend its use and immediately inform the vendor, distributor, and market surveillance authority. If a serious incident occurs, you must report it immediately (AI Act, Article 26(5)).
* **Keep logs:** Keep the logs automatically generated by the system (if under your control) for at least six months, unless other Union or national law (such as GDPR) requires otherwise (AI Act, Article 26(6)).
* **Inform workers (if applicable):** If you are an employer, inform workers' representatives and affected workers before putting the system into service at the workplace (AI Act, Article 26(7)).
* **Inform affected individuals:** If the system makes or assists in making decisions related to natural persons, inform those individuals that they are subject to the use of the high-risk AI system (AI Act, Article 26(11)).
* **Use information for GDPR impact assessments:** Use the information provided by the vendor to help carry out data protection impact assessments under the GDPR where applicable (AI Act, Article 26(9)).
* **Cooperate:** Cooperate with competent authorities on any actions they take regarding the system (AI Act, Article 26(12)).

Because these obligations depend heavily on your specific sector, how the AI tool is used, and your control over data and logs, you should confirm your compliance setup with a lawyer before relying on the system in production.

**Retrieved:** AI Act, Article 13; AI Act, Article 26; AI Act, Recital 91; AI Act, Recital 93

<details><summary>search: deployer obligations high-risk AI system AI Act</summary>

```
[1] Cite as: AI Act, Article 26 | type: article — Obligations of deployers of high-risk AI systems (part 1 of 2)
1. Deployers of high-risk AI systems shall take appropriate technical and organisational measures to ensure they use such systems in accordance with the instructions for use accompanying the systems, pursuant to paragraphs 3 and 6.
2. Deployers shall assign human oversight to natural persons who have the necessary competence, training and authority, as well as the necessary support.
3. The obligations set out in paragraphs 1 and 2, are without prejudice to other deployer obligations under Union or national law and to the deployer’s freedom to organise its own resources and activities for the purpose of implementing the human oversight measures indicated by the provider.
4. Without prejudice to paragraphs 1 and 2, to the extent the deployer exercises control over the input data, that deployer shall ensure that input data is relevant and sufficiently representative in view of the intended purpose of the high-risk AI system.
5. Deployers shall monitor the operation of the high-risk AI system on the basis of the instructions for use and, where relevant, inform providers in accordance with Article 72. Where deployers have reason to consider that the use of the high-risk AI system in accordance with the instructions may result in that AI system presenting a risk within the meaning of Article 79(1), they shall, without undue delay, inform the provider or distributor and the relevant market surveillance authority, and shall suspend the use of that system. Where deployers have identified a serious incident, they shall also immediately inform first the provider, and then the importer or distributor and the relevant market surveillance authorities of that incident. If the deployer is not able to reach the provider, Article 73 shall apply
mutatis mutandis
. This obligation shall not cover sensitive operational data of deployers of AI systems which are law enforcement authorities.
For deployers that are financial institutions subject to requirements regarding their internal governance, arrangements or processes under Union financial services law, the monitoring obligation set out in the first subparagraph shall be deemed to be fulfilled by complying with the rules on internal governance arrangements, processes and mechanisms pursuant to the relevant financial service law.
6. Deployers of high-risk AI systems shall keep the logs automatically generated by that high-risk AI system to the extent such logs are under their control, for a period appropriate to the intended purpose of the high-risk AI system, of at least six months, unless provided otherwise in applicable Union or national law, in particular in Union law on the protection of personal data.
Deployers that are financial institutions subject to requirements regarding their internal governance, arrangements or processes under Union financial services law shall maintain the logs as part of the documentation kept pursuant to the relevant Union financial service law.
7. Before putting into service or using a high-risk AI system at the workplace, deployers who are employers shall inform workers’ representatives and the affected workers that they will be subject to the use of the high-risk AI system. This information shall be provided, where applicable, in accordance with the rules and procedures laid down in Union and national law and practice on information of workers and their representatives.
8. Deployers of high-risk AI systems that are public authorities, or Union institutions, bodies, offices or agencies shall comply with the registration obligations referred to in Article 49. When such deployers find that the high-risk AI system that they envisage using has not been registered in the EU database referred to in Article 71, they shall not use that system and shall inform the provider or the distributor.

[2] Cite as: AI Act, Recital 91 | type: recital
Given the nature of AI systems and the risks to safety and fundamental rights possibly associated with their use, including as regards the need to ensure proper monitoring of the performance of an AI system in a real-life setting, it is appropriate to set specific responsibilities for deployers. Deployers should in particular take appropriate technical and organisational measures to ensure they use high-risk AI systems in accordance with the instructions of use and certain other obligations should be provided for with regard to monitoring of the functioning of the AI systems and with regard to record-keeping, as appropriate. Furthermore, deployers should ensure that the persons assigned to implement the instructions for use and human oversight as set out in this Regulation have the necessary competence, in particular an adequate level of AI literacy, training and authority to properly fulfil those tasks. Those obligations should be without prejudice to other deployer obligations in relation to high-risk AI systems under Union or national law.

[3] Cite as: AI Act, Recital 93 | type: recital
Whilst risks related to AI systems can result from the way such systems are designed, risks can as well stem from how such AI systems are used. Deployers of high-risk AI system therefore play a critical role in ensuring that fundamental rights are protected, complementing the obligations of the provider when developing the AI system. Deployers are best placed to understand how the high-risk AI system will be used concretely and can therefore identify potential significant risks that were not foreseen in the development phase, due to a more precise knowledge of the context of use, the persons or groups of persons likely to be affected, including vulnerable groups. Deployers of high-risk AI systems listed in an annex to this Regulation also play a critical role in informing natural persons and should, when they make decisions or assist in making decisions related to natural persons, where applicable, inform the natural persons that they are subject to the use of the high-risk AI system. This information should include the intended purpose and the type of decisions it makes. The deployer should also inform the natural persons about their right to an explanation provided under this Regulation. With regard to high-risk AI systems used for law enforcement purposes, that obligation should be implemented in accordance with Article 13 of Directive (EU) 2016/680.

[4] Cite as: AI Act, Article 26 | type: article — Obligations of deployers of high-risk AI systems (part 2 of 2)
9. Where applicable, deployers of high-risk AI systems shall use the information provided under Article 13 of this Regulation to comply with their obligation to carry out a data protection impact assessment under Article 35 of Regulation (EU) 2016/679 or Article 27 of Directive (EU) 2016/680.
10. Without prejudice to Directive (EU) 2016/680, in the framework of an investigation for the targeted search of a person suspected or convicted of having committed a criminal offence, the deployer of a high-risk AI system for post-remote biometric identification shall request an authorisation,
ex ante
, or without undue delay and no later than 48 hours, by a judicial authority or an administrative authority whose decision is binding and subject to judicial review, for the use of that system, except when it is used for the initial identification of a potential suspect based on objective and verifiable facts directly linked to the offence. Each use shall be limited to what is strictly necessary for the investigation of a specific criminal offence.
If the authorisation requested pursuant to the first subparagraph is rejected, the use of the post-remote biometric identification system linked to that requested authorisation shall be stopped with immediate effect and the personal data linked to the use of the high-risk AI system for which the authorisation was requested shall be deleted.
In no case shall such high-risk AI system for post-remote biometric identification be used for law enforcement purposes in an untargeted way, without any link to a criminal offence, a criminal proceeding, a genuine and present or genuine and foreseeable threat of a criminal offence, or the search for a specific missing person. It shall be ensured that no decision that produces an adverse legal effect on a person may be taken by the law enforcement authorities based solely on the output of such post-remote biometric identification systems.
This paragraph is without prejudice to Article 9 of Regulation (EU) 2016/679 and Article 10 of Directive (EU) 2016/680 for the processing of biometric data.
Regardless of the purpose or deployer, each use of such high-risk AI systems shall be documented in the relevant police file and shall be made available to the relevant market surveillance authority and the national data protection authority upon request, excluding the disclosure of sensitive operational data related to law enforcement. This subparagraph shall be without prejudice to the powers conferred by Directive (EU) 2016/680 on supervisory authorities.
Deployers shall submit annual reports to the relevant market surveillance and national data protection authorities on their use of post-remote biometric identification systems, excluding the disclosure of sensitive operational data related to law enforcement. The reports may be aggregated to cover more than one deployment.
Member States may introduce, in accordance with Union law, more restrictive laws on the use of post-remote biometric identification systems.
11. Without prejudice to Article 50 of this Regulation, deployers of high-risk AI systems referred to in Annex III that make decisions or assist in making decisions related to natural persons shall inform the natural persons that they are subject to the use of the high-risk AI system. For high-risk AI systems used for law enforcement purposes Article 13 of Directive (EU) 2016/680 shall apply.
12. Deployers shall cooperate with the relevant competent authorities in any action those authorities take in relation to the high-risk AI system in order to implement this Regulation.

[5] Cite as: AI Act, Article 13 | type: article — Transparency and provision of information to deployers
1. High-risk AI systems shall be designed and developed in such a way as to ensure that their operation is sufficiently transparent to enable deployers to interpret a system’s output and use it appropriately. An appropriate type and degree of transparency shall be ensured with a view to achieving compliance with the relevant obligations of the provider and deployer set out in Section 3.
2. High-risk AI systems shall be accompanied by instructions for use in an appropriate digital format or otherwise that include concise, complete, correct and clear information that is relevant, accessible and comprehensible to deployers.
3. The instructions for use shall contain at least the following information:
(a) the identity and the contact details of the provider and, where applicable, of its authorised representative;
(b) the characteristics, capabilities and limitations of performance of the high-risk AI system, including:
(i) its intended purpose;
(ii) the level of accuracy, including its metrics, robustness and cybersecurity referred to in Article 15 against which the high-risk AI system has been tested and validated and which can be expected, and any known and foreseeable circumstances that may have an impact on that expected level of accuracy, robustness and cybersecurity;
(iii) any known or foreseeable circumstance, related to the use of the high-risk AI system in accordance with its intended purpose or under conditions of reasonably foreseeable misuse, which may lead to risks to the health and safety or fundamental rights referred to in Article 9(2);
(iv) where applicable, the technical capabilities and characteristics of the high-risk AI system to provide information that is relevant to explain its output;
(v) when appropriate, its performance regarding specific persons or groups of persons on which the system is intended to be used;
(vi) when appropriate, specifications for the input data, or any other relevant information in terms of the training, validation and testing data sets used, taking into account the intended purpose of the high-risk AI system;
(vii) where applicable, information to enable deployers to interpret the output of the high-risk AI system and use it appropriately;
(c) the changes to the high-risk AI system and its performance which have been pre-determined by the provider at the moment of the initial conformity assessment, if any;
(d) the human oversight measures referred to in Article 14, including the technical measures put in place to facilitate the interpretation of the outputs of the high-risk AI systems by the deployers;
(e) the computational and hardware resources needed, the expected lifetime of the high-risk AI system and any necessary maintenance and care measures, including their frequency, to ensure the proper functioning of that AI system, including as regards software updates;
(f) where relevant, a description of the mechanisms included within the high-risk AI system that allows deployers to properly collect, store and interpret the logs in accordance with Article 12.
```
</details>

---

## s11 (single)

**Question:** When do the AI Act's rules for high-risk systems actually start applying?

**Reference:** Under the regulation as adopted, most rules, including the Annex III high-risk obligations, apply from 2 August 2026. Chapters I and II (including prohibitions) apply from 2 February 2025; general-purpose AI rules, governance and penalties from 2 August 2025; Article 6(1) (high-risk products under sectoral law) from 2 August 2027. The corpus does not reflect any later amendments.

**Expected:** AI Act, Article 113

**Answer:**

It depends on whether the system is a product safety component or listed in Annex III, and when it was placed on the market:

* **General application:** The AI Act's rules for high-risk systems generally apply starting **2 August 2026** (AI Act, Article 113).
* **Product-related high-risk systems:** Rules tied to certain product safety components (Article 6(1)) apply starting **2 August 2027** (AI Act, Article 113).
* **Existing systems already on the market:** High-risk systems placed on the market or put into service before 2 August 2026 generally only need to comply if they undergo significant changes in their design after that date (AI Act, Article 111). However, high-risk systems intended to be used by public authorities must comply by **2 August 2030** at the latest, and certain large-scale IT systems have until 31 December 2030 (AI Act, Article 111).

*Note: The corpus does not cover later amendments, delays, or enforcement actions.* Confirm your high-risk classification and exact compliance timeline with a lawyer before launch.

**Retrieved:** AI Act, Article 111; AI Act, Article 113; AI Act, Article 6; AI Act, Recital 177; AI Act, Recital 179

<details><summary>search: high-risk AI systems application date AI Act</summary>

```
[1] Cite as: AI Act, Article 113 | type: article — Entry into force and application
This Regulation shall enter into force on the twentieth day following that of its publication in the
Official Journal of the European Union
.
It shall apply from 2 August 2026.
However:
(a) Chapters I and II shall apply from 2 February 2025;
(b) Chapter III Section 4, Chapter V, Chapter VII and Chapter XII and Article 78 shall apply from 2 August 2025, with the exception of Article 101;
(c) Article 6(1) and the corresponding obligations in this Regulation shall apply from 2 August 2027.

[2] Cite as: AI Act, Recital 177 | type: recital
In order to ensure legal certainty, ensure an appropriate adaptation period for operators and avoid disruption to the market, including by ensuring continuity of the use of AI systems, it is appropriate that this Regulation applies to the high-risk AI systems that have been placed on the market or put into service before the general date of application thereof, only if, from that date, those systems are subject to significant changes in their design or intended purpose. It is appropriate to clarify that, in this respect, the concept of significant change should be understood as equivalent in substance to the notion of substantial modification, which is used with regard only to high-risk AI systems pursuant to this Regulation. On an exceptional basis and in light of public accountability, operators of AI systems which are components of the large-scale IT systems established by the legal acts listed in an annex to this Regulation and operators of high-risk AI systems that are intended to be used by public authorities should, respectively, take the necessary steps to comply with the requirements of this Regulation by end of 2030 and by 2 August 2030.

[3] Cite as: AI Act, Recital 179 | type: recital
This Regulation should apply from 2 August 2026. However, taking into account the unacceptable risk associated with the use of AI in certain ways, the prohibitions as well as the general provisions of this Regulation should already apply from 2 February 2025. While the full effect of those prohibitions follows with the establishment of the governance and enforcement of this Regulation, anticipating the application of the prohibitions is important to take account of unacceptable risks and to have an effect on other procedures, such as in civil law. Moreover, the infrastructure related to the governance and the conformity assessment system should be operational before 2 August 2026, therefore the provisions on notified bodies and governance structure should apply from 2 August 2025. Given the rapid pace of technological advancements and adoption of general-purpose AI models, obligations for providers of general-purpose AI models should apply from 2 August 2025. Codes of practice should be ready by 2 May 2025 in view of enabling providers to demonstrate compliance on time. The AI Office should ensure that classification rules and procedures are up to date in light of technological developments. In addition, Member States should lay down and notify to the Commission the rules on penalties, including administrative fines, and ensure that they are properly and effectively implemented by the date of application of this Regulation. Therefore the provisions on penalties should apply from 2 August 2025.

[4] Cite as: AI Act, Article 111 | type: article — AI systems already placed on the market or put into service and general-purpose AI models already placed on the marked
1. Without prejudice to the application of Article 5 as referred to in Article 113(3), point (a), AI systems which are components of the large-scale IT systems established by the legal acts listed in Annex X that have been placed on the market or put into service before 2 August 2027 shall be brought into compliance with this Regulation by 31 December 2030.
The requirements laid down in this Regulation shall be taken into account in the evaluation of each large-scale IT system established by the legal acts listed in Annex X to be undertaken as provided for in those legal acts and where those legal acts are replaced or amended.
2. Without prejudice to the application of Article 5 as referred to in Article 113(3), point (a), this Regulation shall apply to operators of high-risk AI systems, other than the systems referred to in paragraph 1 of this Article, that have been placed on the market or put into service before 2 August 2026, only if, as from that date, those systems are subject to significant changes in their designs. In any case, the providers and deployers of high-risk AI systems intended to be used by public authorities shall take the necessary steps to comply with the requirements and obligations of this Regulation by 2 August 2030.
3. Providers of general-purpose AI models that have been placed on the market before 2 August 2025 shall take the necessary steps in order to comply with the obligations laid down in this Regulation by 2 August 2027.

[5] Cite as: AI Act, Article 6 | type: article — Classification rules for high-risk AI systems (part 1 of 2)
1. Irrespective of whether an AI system is placed on the market or put into service independently of the products referred to in points (a) and (b), that AI system shall be considered to be high-risk where both of the following conditions are fulfilled:
(a) the AI system is intended to be used as a safety component of a product, or the AI system is itself a product, covered by the Union harmonisation legislation listed in Annex I;
(b) the product whose safety component pursuant to point (a) is the AI system, or the AI system itself as a product, is required to undergo a third-party conformity assessment, with a view to the placing on the market or the putting into service of that product pursuant to the Union harmonisation legislation listed in Annex I.
2. In addition to the high-risk AI systems referred to in paragraph 1, AI systems referred to in Annex III shall be considered to be high-risk.
3. By derogation from paragraph 2, an AI system referred to in Annex III shall not be considered to be high-risk where it does not pose a significant risk of harm to the health, safety or fundamental rights of natural persons, including by not materially influencing the outcome of decision making.
The first subparagraph shall apply where any of the following conditions is fulfilled:
(a) the AI system is intended to perform a narrow procedural task;
(b) the AI system is intended to improve the result of a previously completed human activity;
(c) the AI system is intended to detect decision-making patterns or deviations from prior decision-making patterns and is not meant to replace or influence the previously completed human assessment, without proper human review; or
(d) the AI system is intended to perform a preparatory task to an assessment relevant for the purposes of the use cases listed in Annex III.
Notwithstanding the first subparagraph, an AI system referred to in Annex III shall always be considered to be high-risk where the AI system performs profiling of natural persons.
4. A provider who considers that an AI system referred to in Annex III is not high-risk shall document its assessment before that system is placed on the market or put into service. Such provider shall be subject to the registration obligation set out in Article 49(2). Upon request of national competent authorities, the provider shall provide the documentation of the assessment.
5. The Commission shall, after consulting the European Artificial Intelligence Board (the ‘Board’), and no later than 2 February 2026, provide guidelines specifying the practical implementation of this Article in line with Article 96 together with a comprehensive list of practical examples of use cases of AI systems that are high-risk and not high-risk.
6. The Commission is empowered to adopt delegated acts in accordance with Article 97 in order to amend paragraph 3, second subparagraph, of this Article by adding new conditions to those laid down therein, or by modifying them, where there is concrete and reliable evidence of the existence of AI systems that fall under the scope of Annex III, but do not pose a significant risk of harm to the health, safety or fundamental rights of natural persons.
7. The Commission shall adopt delegated acts in accordance with Article 97 in order to amend paragraph 3, second subparagraph, of this Article by deleting any of the conditions laid down therein, where there is concrete and reliable evidence that this is necessary to maintain the level of protection of health, safety and fundamental rights provided for by this Regulation.
```
</details>

---

## s12 (single)

**Question:** Do our employees need any training before they use AI tools at work?

**Reference:** Providers and deployers must take measures to ensure, to their best extent, a sufficient level of AI literacy among staff and others operating AI systems on their behalf, taking into account their technical knowledge, experience, education, training and the context of use.

**Expected:** AI Act, Article 4

**Answer:**

Yes, depending on your role as a provider or deployer of AI systems, you must take measures to ensure a sufficient level of AI literacy for your staff (AI Act, Article 4). 

Specifically, the law requires:
* **General AI Literacy:** Providers and deployers of AI systems must take measures to ensure, to their best extent, a sufficient level of AI literacy for their staff and anyone else operating or using AI systems on their behalf (AI Act, Article 4). This takes into account their technical knowledge, experience, education, training, and the context in which the AI is used (AI Act, Article 4).
* **High-Risk AI Systems:** If your employees are assigned to implement human oversight for high-risk AI systems, deployers must ensure those individuals have the necessary competence, training, and authority to properly fulfill those tasks (AI Act, Article 26(2), Recital 91). 

Whether specific training is legally mandatory depends on the risk classification of the AI tools your employees use and their specific roles. Before launching or deciding on training programs, we recommend confirming your exact classifications and obligations with a lawyer.

**Retrieved:** AI Act, Article 26; AI Act, Article 4; AI Act, Recital 13; AI Act, Recital 20; AI Act, Recital 91

<details><summary>search: AI literacy provider deployer employees training</summary>

```
[1] Cite as: AI Act, Article 4 | type: article — AI literacy
Providers and deployers of AI systems shall take measures to ensure, to their best extent, a sufficient level of AI literacy of their staff and other persons dealing with the operation and use of AI systems on their behalf, taking into account their technical knowledge, experience, education and training and the context the AI systems are to be used in, and considering the persons or groups of persons on whom the AI systems are to be used.

[2] Cite as: AI Act, Recital 91 | type: recital
Given the nature of AI systems and the risks to safety and fundamental rights possibly associated with their use, including as regards the need to ensure proper monitoring of the performance of an AI system in a real-life setting, it is appropriate to set specific responsibilities for deployers. Deployers should in particular take appropriate technical and organisational measures to ensure they use high-risk AI systems in accordance with the instructions of use and certain other obligations should be provided for with regard to monitoring of the functioning of the AI systems and with regard to record-keeping, as appropriate. Furthermore, deployers should ensure that the persons assigned to implement the instructions for use and human oversight as set out in this Regulation have the necessary competence, in particular an adequate level of AI literacy, training and authority to properly fulfil those tasks. Those obligations should be without prejudice to other deployer obligations in relation to high-risk AI systems under Union or national law.

[3] Cite as: AI Act, Recital 20 | type: recital
In order to obtain the greatest benefits from AI systems while protecting fundamental rights, health and safety and to enable democratic control, AI literacy should equip providers, deployers and affected persons with the necessary notions to make informed decisions regarding AI systems. Those notions may vary with regard to the relevant context and can include understanding the correct application of technical elements during the AI system’s development phase, the measures to be applied during its use, the suitable ways in which to interpret the AI system’s output, and, in the case of affected persons, the knowledge necessary to understand how decisions taken with the assistance of AI will have an impact on them. In the context of the application this Regulation, AI literacy should provide all relevant actors in the AI value chain with the insights required to ensure the appropriate compliance and its correct enforcement. Furthermore, the wide implementation of AI literacy measures and the introduction of appropriate follow-up actions could contribute to improving working conditions and ultimately sustain the consolidation, and innovation path of trustworthy AI in the Union. The European Artificial Intelligence Board (the ‘Board’) should support the Commission, to promote AI literacy tools, public awareness and understanding of the benefits, risks, safeguards, rights and obligations in relation to the use of AI systems. In cooperation with the relevant stakeholders, the Commission and the Member States should facilitate the drawing up of voluntary codes of conduct to advance AI literacy among persons dealing with the development, operation and use of AI.

[4] Cite as: AI Act, Article 26 | type: article — Obligations of deployers of high-risk AI systems (part 1 of 2)
1. Deployers of high-risk AI systems shall take appropriate technical and organisational measures to ensure they use such systems in accordance with the instructions for use accompanying the systems, pursuant to paragraphs 3 and 6.
2. Deployers shall assign human oversight to natural persons who have the necessary competence, training and authority, as well as the necessary support.
3. The obligations set out in paragraphs 1 and 2, are without prejudice to other deployer obligations under Union or national law and to the deployer’s freedom to organise its own resources and activities for the purpose of implementing the human oversight measures indicated by the provider.
4. Without prejudice to paragraphs 1 and 2, to the extent the deployer exercises control over the input data, that deployer shall ensure that input data is relevant and sufficiently representative in view of the intended purpose of the high-risk AI system.
5. Deployers shall monitor the operation of the high-risk AI system on the basis of the instructions for use and, where relevant, inform providers in accordance with Article 72. Where deployers have reason to consider that the use of the high-risk AI system in accordance with the instructions may result in that AI system presenting a risk within the meaning of Article 79(1), they shall, without undue delay, inform the provider or distributor and the relevant market surveillance authority, and shall suspend the use of that system. Where deployers have identified a serious incident, they shall also immediately inform first the provider, and then the importer or distributor and the relevant market surveillance authorities of that incident. If the deployer is not able to reach the provider, Article 73 shall apply
mutatis mutandis
. This obligation shall not cover sensitive operational data of deployers of AI systems which are law enforcement authorities.
For deployers that are financial institutions subject to requirements regarding their internal governance, arrangements or processes under Union financial services law, the monitoring obligation set out in the first subparagraph shall be deemed to be fulfilled by complying with the rules on internal governance arrangements, processes and mechanisms pursuant to the relevant financial service law.
6. Deployers of high-risk AI systems shall keep the logs automatically generated by that high-risk AI system to the extent such logs are under their control, for a period appropriate to the intended purpose of the high-risk AI system, of at least six months, unless provided otherwise in applicable Union or national law, in particular in Union law on the protection of personal data.
Deployers that are financial institutions subject to requirements regarding their internal governance, arrangements or processes under Union financial services law shall maintain the logs as part of the documentation kept pursuant to the relevant Union financial service law.
7. Before putting into service or using a high-risk AI system at the workplace, deployers who are employers shall inform workers’ representatives and the affected workers that they will be subject to the use of the high-risk AI system. This information shall be provided, where applicable, in accordance with the rules and procedures laid down in Union and national law and practice on information of workers and their representatives.
8. Deployers of high-risk AI systems that are public authorities, or Union institutions, bodies, offices or agencies shall comply with the registration obligations referred to in Article 49. When such deployers find that the high-risk AI system that they envisage using has not been registered in the EU database referred to in Article 71, they shall not use that system and shall inform the provider or the distributor.

[5] Cite as: AI Act, Recital 13 | type: recital
The notion of ‘deployer’ referred to in this Regulation should be interpreted as any natural or legal person, including a public authority, agency or other body, using an AI system under its authority, except where the AI system is used in the course of a personal non-professional activity. Depending on the type of AI system, the use of the system may affect persons other than the deployer.
```
</details>

---

## s13 (single)

**Question:** Are there any special measures under the AI Act that help small startups like ours?

**Reference:** Yes. Member States must give SMEs, including startups, priority access to AI regulatory sandboxes, run awareness and training activities, provide dedicated communication channels, and facilitate their participation in standardisation. Conformity-assessment fees must take SMEs' interests into account and be reduced in proportion to their size.

**Expected:** AI Act, Article 62

**Answer:**

Yes, the AI Act includes several special measures and support mechanisms tailored for small enterprises and start-ups:

* **Priority access to regulatory sandboxes:** Member States must provide EU-based SMEs and start-ups with priority access to AI regulatory sandboxes, provided they meet the eligibility and selection criteria (AI Act, Article 62(1)).
* **Proportionate conformity fees:** Conformity assessment fees must take into account the specific interests and needs of SME providers, and be reduced proportionately to their size and market size (AI Act, Article 62(2)).
* **Targeted guidance and training:** Member States are required to organise specific awareness-raising and training activities, and establish communication channels to provide advice and answer queries regarding the implementation of the regulation (AI Act, Article 62(1)).
* **Simplified quality management for microenterprises:** Microenterprises are allowed to fulfill quality management system requirements in a simplified manner, as specified by upcoming Commission guidelines, provided they have no partner or linked enterprises (AI Act, Article 63). 
* **EU-level tools:** The AI Office will provide standardised templates, maintain a single information platform, and promote best practices to help operators comply (AI Act, Article 62(3)). Recitals also point to support from European Digital Innovation Hubs and testing facilities (AI Act, Recital 145).

Whether these measures apply directly depends on your enterprise classification (such as microenterprise status under EU rules) and your participation in national sandbox schemes. Confirming your precise enterprise category and eligibility with a lawyer before launch is recommended.

**Retrieved:** AI Act, Article 62; AI Act, Article 63; AI Act, Recital 143; AI Act, Recital 145; AI Act, Recital 146

<details><summary>search: small scale enterprise startup SME AI Act measures support</summary>

```
[1] Cite as: AI Act, Recital 143 | type: recital
In order to promote and protect innovation, it is important that the interests of SMEs, including start-ups, that are providers or deployers of AI systems are taken into particular account. To that end, Member States should develop initiatives, which are targeted at those operators, including on awareness raising and information communication. Member States should provide SMEs, including start-ups, that have a registered office or a branch in the Union, with priority access to the AI regulatory sandboxes provided that they fulfil the eligibility conditions and selection criteria and without precluding other providers and prospective providers to access the sandboxes provided the same conditions and criteria are fulfilled. Member States should utilise existing channels and where appropriate, establish new dedicated channels for communication with SMEs, including start-ups, deployers, other innovators and, as appropriate, local public authorities, to support SMEs throughout their development path by providing guidance and responding to queries about the implementation of this Regulation. Where appropriate, these channels should work together to create synergies and ensure homogeneity in their guidance to SMEs, including start-ups, and deployers. Additionally, Member States should facilitate the participation of SMEs and other relevant stakeholders in the standardisation development processes. Moreover, the specific interests and needs of providers that are SMEs, including start-ups, should be taken into account when notified bodies set conformity assessment fees. The Commission should regularly assess the certification and compliance costs for SMEs, including start-ups, through transparent consultations and should work with Member States to lower such costs. For example, translation costs related to mandatory documentation and communication with authorities may constitute a significant cost for providers and other operators, in particular those of a smaller scale. Member States should possibly ensure that one of the languages determined and accepted by them for relevant providers’ documentation and for communication with operators is one which is broadly understood by the largest possible number of cross-border deployers. In order to address the specific needs of SMEs, including start-ups, the Commission should provide standardised templates for the areas covered by this Regulation, upon request of the Board. Additionally, the Commission should complement Member States’ efforts by providing a single information platform with easy-to-use information with regards to this Regulation for all providers and deployers, by organising appropriate communication campaigns to raise awareness about the obligations arising from this Regulation, and by evaluating and promoting the convergence of best practices in public procurement procedures in relation to AI systems. Medium-sized enterprises which until recently qualified as small enterprises within the meaning of the Annex to Commission Recommendation 2003/361/EC
should have access to those support measures, as those new medium-sized enterprises may sometimes lack the legal resources and training necessary to ensure proper understanding of, and compliance with, this Regulation.

[2] Cite as: AI Act, Article 62 | type: article — Measures for providers and deployers, in particular SMEs, including start-ups
1. Member States shall undertake the following actions:
(a) provide SMEs, including start-ups, having a registered office or a branch in the Union, with priority access to the AI regulatory sandboxes, to the extent that they fulfil the eligibility conditions and selection criteria; the priority access shall not preclude other SMEs, including start-ups, other than those referred to in this paragraph from access to the AI regulatory sandbox, provided that they also fulfil the eligibility conditions and selection criteria;
(b) organise specific awareness raising and training activities on the application of this Regulation tailored to the needs of SMEs including start-ups, deployers and, as appropriate, local public authorities;
(c) utilise existing dedicated channels and where appropriate, establish new ones for communication with SMEs including start-ups, deployers, other innovators and, as appropriate, local public authorities to provide advice and respond to queries about the implementation of this Regulation, including as regards participation in AI regulatory sandboxes;
(d) facilitate the participation of SMEs and other relevant stakeholders in the standardisation development process.
2. The specific interests and needs of the SME providers, including start-ups, shall be taken into account when setting the fees for conformity assessment under Article 43, reducing those fees proportionately to their size, market size and other relevant indicators.
3. The AI Office shall undertake the following actions:
(a) provide standardised templates for areas covered by this Regulation, as specified by the Board in its request;
(b) develop and maintain a single information platform providing easy to use information in relation to this Regulation for all operators across the Union;
(c) organise appropriate communication campaigns to raise awareness about the obligations arising from this Regulation;
(d) evaluate and promote the convergence of best practices in public procurement procedures in relation to AI systems.

[3] Cite as: AI Act, Recital 145 | type: recital
In order to minimise the risks to implementation resulting from lack of knowledge and expertise in the market as well as to facilitate compliance of providers, in particular SMEs, including start-ups, and notified bodies with their obligations under this Regulation, the AI-on-demand platform, the European Digital Innovation Hubs and the testing and experimentation facilities established by the Commission and the Member States at Union or national level should contribute to the implementation of this Regulation. Within their respective mission and fields of competence, the AI-on-demand platform, the European Digital Innovation Hubs and the testing and experimentation Facilities are able to provide in particular technical and scientific support to providers and notified bodies.

[4] Cite as: AI Act, Recital 146 | type: recital
Moreover, in light of the very small size of some operators and in order to ensure proportionality regarding costs of innovation, it is appropriate to allow microenterprises to fulfil one of the most costly obligations, namely to establish a quality management system, in a simplified manner which would reduce the administrative burden and the costs for those enterprises without affecting the level of protection and the need for compliance with the requirements for high-risk AI systems. The Commission should develop guidelines to specify the elements of the quality management system to be fulfilled in this simplified manner by microenterprises.

[5] Cite as: AI Act, Article 63 | type: article — Derogations for specific operators
1. Microenterprises within the meaning of Recommendation 2003/361/EC may comply with certain elements of the quality management system required by Article 17 of this Regulation in a simplified manner, provided that they do not have partner enterprises or linked enterprises within the meaning of that Recommendation. For that purpose, the Commission shall develop guidelines on the elements of the quality management system which may be complied with in a simplified manner considering the needs of microenterprises, without affecting the level of protection or the need for compliance with the requirements in respect of high-risk AI systems.
2. Paragraph 1 of this Article shall not be interpreted as exempting those operators from fulfilling any other requirements or obligations laid down in this Regulation, including those established in Articles 9, 10, 11, 12, 13, 14, 15, 72 and 73.
```
</details>

---

## s14 (single)

**Question:** Do we have to explain to users why we removed their post or suspended their account?

**Reference:** Yes. Hosting providers must give affected users a clear and specific statement of reasons for restrictions such as removal, demotion, suspension of monetisation or account suspension. It must state the facts, whether automated means were used, the legal or terms-and-conditions ground, and the available redress options.

**Expected:** DSA, Article 17

**Answer:**

Yes, if you are a hosting service provider, you must provide a clear and specific "statement of reasons" to affected users when you remove their content, restrict its visibility, or suspend or terminate their account because the content is illegal or violates your terms and conditions (DSA, Article 17(1)).

This obligation applies as soon as the restriction is imposed, provided you have the user's electronic contact details (DSA, Article 17(2)). 

The statement of reasons must include:
* The specific type of restriction (such as removal, demotion, account suspension, or termination) and its duration or territorial scope (DSA, Article 17(3)(a)).
* The facts and circumstances relied on, including whether the decision was based on a notice or an own-initiative investigation (DSA, Article 17(3)(b)).
* Information on whether automated means were used to make the decision (DSA, Article 17(3)(c)).
* The legal ground or the specific contractual terms and conditions violated, with an explanation of why the information is considered illegal or incompatible (DSA, Article 17(3)(d) and (e)).
* Clear, user-friendly information on redress possibilities, such as internal complaints or out-of-court dispute settlement (DSA, Article 17(3)(f)).

Exemptions apply for deceptive high-volume commercial content and certain legal orders (DSA, Article 17(2) and (5)). Because compliance depends on whether your service qualifies as a hosting service under the Digital Services Act and how you implement these notices, you should confirm your setup with a lawyer before launch.

**Retrieved:** DSA, Article 14; DSA, Article 17; DSA, Recital 54; DSA, Recital 55; DSA, Recital 64

<details><summary>search: statement of reasons restriction content account DSA</summary>

```
[1] Cite as: DSA, Article 17 | type: article — Statement of reasons
1. Providers of hosting services shall provide a clear and specific statement of reasons to any affected recipients of the service for any of the following restrictions imposed on the ground that the information provided by the recipient of the service is illegal content or incompatible with their terms and conditions:
(a) any restrictions of the visibility of specific items of information provided by the recipient of the service, including removal of content, disabling access to content, or demoting content;
(b) suspension, termination or other restriction of monetary payments;
(c) suspension or termination of the provision of the service in whole or in part;
(d) suspension or termination of the recipient of the service's account.
2. Paragraph 1 shall only apply where the relevant electronic contact details are known to the provider. It shall apply at the latest from the date that the restriction is imposed, regardless of why or how it was imposed.
Paragraph 1 shall not apply where the information is deceptive high-volume commercial content.
3. The statement of reasons referred to in paragraph 1 shall at least contain the following information:
(a) information on whether the decision entails either the removal of, the disabling of access to, the demotion of or the restriction of the visibility of the information, or the suspension or termination of monetary payments related to that information, or imposes other measures referred to in paragraph 1 with regard to the information, and, where relevant, the territorial scope of the decision and its duration;
(b) the facts and circumstances relied on in taking the decision, including, where relevant, information on whether the decision was taken pursuant to a notice submitted in accordance with Article 16 or based on voluntary own-initiative investigations and, where strictly necessary, the identity of the notifier;
(c) where applicable, information on the use made of automated means in taking the decision, including information on whether the decision was taken in respect of content detected or identified using automated means;
(d) where the decision concerns allegedly illegal content, a reference to the legal ground relied on and explanations as to why the information is considered to be illegal content on that ground;
(e) where the decision is based on the alleged incompatibility of the information with the terms and conditions of the provider of hosting services, a reference to the contractual ground relied on and explanations as to why the information is considered to be incompatible with that ground;
(f) clear and user-friendly information on the possibilities for redress available to the recipient of the service in respect of the decision, in particular, where applicable through internal complaint-handling mechanisms, out-of-court dispute settlement and judicial redress.
4. The information provided by the providers of hosting services in accordance with this Article shall be clear and easily comprehensible and as precise and specific as reasonably possible under the given circumstances. The information shall, in particular, be such as to reasonably allow the recipient of the service concerned to effectively exercise the possibilities for redress referred to in of paragraph 3, point (f).
5. This Article shall not apply to any orders referred to in Article 9.

[2] Cite as: DSA, Recital 54 | type: recital
Where a provider of hosting services decides, on the ground that the information provided by the recipients is illegal content or is incompatible with its terms and conditions, to remove or disable access to information provided by a recipient of the service or to otherwise restrict its visibility or monetisation, for instance following receipt of a notice or acting on its own initiative, including exclusively by automated means, that provider should inform in a clear and easily comprehensible way the recipient of its decision, the reasons for its decision and the available possibilities for redress to contest the decision, in view of the negative consequences that such decisions may have for the recipient, including as regards the exercise of its fundamental right to freedom of expression. That obligation should apply irrespective of the reasons for the decision, in particular whether the action has been taken because the information notified is considered to be illegal content or incompatible with the applicable terms and conditions. Where the decision was taken following receipt of a notice, the provider of hosting services should only reveal the identity of the person or entity who submitted the notice to the recipient of the service where this information is necessary to identify the illegality of the content, such as in cases of infringements of intellectual property rights.

[3] Cite as: DSA, Recital 55 | type: recital
Restriction of visibility may consist in demotion in ranking or in recommender systems, as well as in limiting accessibility by one or more recipients of the service or blocking the user from an online community without the user being aware (‘shadow banning’). The monetisation via advertising revenue of information provided by the recipient of the service can be restricted by suspending or terminating the monetary payment or revenue associated to that information. The obligation to provide a statement of reasons should however not apply with respect to deceptive high-volume commercial content disseminated through intentional manipulation of the service, in particular inauthentic use of the service such as the use of bots or fake accounts or other deceptive uses of the service. Irrespective of other possibilities to challenge the decision of the provider of hosting services, the recipient of the service should always have a right to effective remedy before a court in accordance with the national law.

[4] Cite as: DSA, Recital 64 | type: recital
Under certain conditions, providers of online platforms should temporarily suspend their relevant activities in respect of the person engaged in abusive behaviour. This is without prejudice to the freedom by providers of online platforms to determine their terms and conditions and establish stricter measures in the case of manifestly illegal content related to serious crimes, such as child sexual abuse material. For reasons of transparency, this possibility should be set out, clearly and in sufficient detail, in the terms and conditions of the online platforms. Redress should always be open to the decisions taken in this regard by providers of online platforms and they should be subject to oversight by the competent Digital Services Coordinator. Providers of online platforms should send a prior warning before deciding on the suspension, which should include the reasons for the possible suspension and the means of redress against the decision of the providers of the online platform. When deciding on the suspension, providers of online platforms should send the statement of reasons in accordance with the rules set out in this Regulation. The rules of this Regulation on misuse should not prevent providers of online platforms from taking other measures to address the provision of illegal content by recipients of their service or other misuse of their services, including through the violation of their terms and conditions, in accordance with the applicable Union and national law. Those rules are without prejudice to any possibility to hold the persons engaged in misuse liable, including for damages, provided for in Union or national law.

[5] Cite as: DSA, Article 14 | type: article — Terms and conditions
1. Providers of intermediary services shall include information on any restrictions that they impose in relation to the use of their service in respect of information provided by the recipients of the service, in their terms and conditions. That information shall include information on any policies, procedures, measures and tools used for the purpose of content moderation, including algorithmic decision-making and human review, as well as the rules of procedure of their internal complaint handling system. It shall be set out in clear, plain, intelligible, user-friendly and unambiguous language, and shall be publicly available in an easily accessible and machine-readable format.
2. Providers of intermediary services shall inform the recipients of the service of any significant change to the terms and conditions.
3. Where an intermediary service is primarily directed at minors or is predominantly used by them, the provider of that intermediary service shall explain the conditions for, and any restrictions on, the use of the service in a way that minors can understand.
4. Providers of intermediary services shall act in a diligent, objective and proportionate manner in applying and enforcing the restrictions referred to in paragraph 1, with due regard to the rights and legitimate interests of all parties involved, including the fundamental rights of the recipients of the service, such as the freedom of expression, freedom and pluralism of the media, and other fundamental rights and freedoms as enshrined in the Charter.
5. Providers of very large online platforms and of very large online search engines shall provide recipients of services with a concise, easily-accessible and machine-readable summary of the terms and conditions, including the available remedies and redress mechanisms, in clear and unambiguous language.
6. Very large online platforms and very large online search engines within the meaning of Article 33 shall publish their terms and conditions in the official languages of all the Member States in which they offer their services.
```
</details>

---

## s15 (single)

**Question:** Someone reported illegal listings on our marketplace. What do we need to have in place to handle these reports?

**Reference:** An easy-to-access, user-friendly electronic notice-and-action mechanism. You must confirm receipt, process notices in a timely, diligent, non-arbitrary and objective way, inform the notifier of your decision and the redress options, and disclose whether you used automated means.

**Expected:** DSA, Article 16

**Answer:**

Yes, under the Digital Services Act (DSA), if your marketplace qualifies as a hosting service or online platform, you must put an easy-to-access, user-friendly **notice and action mechanism** in place to handle reports of illegal content electronically (DSA, Article 16(1)).

To comply, your reporting system must enable submitters to provide:
* A substantiated explanation of why the content is illegal (DSA, Article 16(2)(a)).
* The exact electronic location, such as a URL (DSA, Article 16(2)(b)).
* The name and email address of the submitter (except for certain criminal offences), plus a statement confirming their bona fide belief that the information is accurate and complete (DSA, Article 16(2)(c)–(d)).

When handling notices, you must:
* Send a confirmation of receipt to the submitter without undue delay, provided you have their contact info (DSA, Article 16(4)).
* Process notices and make decisions in a timely, diligent, non-arbitrary, and objective manner (DSA, Article 16(6)).
* Inform the submitter of your decision without undue delay, including details on available redress (DSA, Article 16(5)).
* If your marketplace allows consumers to conclude distance contracts with traders and you learn that an illegal product or service was sold, you must also inform the affected consumers who bought it within the preceding six months (if you have their contact details) or publish that information (DSA, Article 32).

Because exact obligations depend on your platform’s classification (e.g., whether you act as an online marketplace for traders) and your specific setup, consider confirming your compliance workflow with a lawyer before launch.

**Retrieved:** DSA, Article 16; DSA, Article 32; DSA, Recital 50; DSA, Recital 52; DSA, Recital 53

<details><summary>search: notice and action mechanism illegal content marketplace</summary>

```
[1] Cite as: DSA, Article 16 | type: article — Notice and action mechanisms
1. Providers of hosting services shall put mechanisms in place to allow any individual or entity to notify them of the presence on their service of specific items of information that the individual or entity considers to be illegal content. Those mechanisms shall be easy to access and user-friendly, and shall allow for the submission of notices exclusively by electronic means.
2. The mechanisms referred to in paragraph 1 shall be such as to facilitate the submission of sufficiently precise and adequately substantiated notices. To that end, the providers of hosting services shall take the necessary measures to enable and to facilitate the submission of notices containing all of the following elements:
(a) a sufficiently substantiated explanation of the reasons why the individual or entity alleges the information in question to be illegal content;
(b) a clear indication of the exact electronic location of that information, such as the exact URL or URLs, and, where necessary, additional information enabling the identification of the illegal content adapted to the type of content and to the specific type of hosting service;
(c) the name and email address of the individual or entity submitting the notice, except in the case of information considered to involve one of the offences referred to in Articles 3 to 7 of Directive 2011/93/EU;
(d) a statement confirming the bona fide belief of the individual or entity submitting the notice that the information and allegations contained therein are accurate and complete.
3. Notices referred to in this Article shall be considered to give rise to actual knowledge or awareness for the purposes of Article 6 in respect of the specific item of information concerned where they allow a diligent provider of hosting services to identify the illegality of the relevant activity or information without a detailed legal examination.
4. Where the notice contains the electronic contact information of the individual or entity that submitted it, the provider of hosting services shall, without undue delay, send a confirmation of receipt of the notice to that individual or entity.
5. The provider shall also, without undue delay, notify that individual or entity of its decision in respect of the information to which the notice relates, providing information on the possibilities for redress in respect of that decision.
6. Providers of hosting services shall process any notices that they receive under the mechanisms referred to in paragraph 1 and take their decisions in respect of the information to which the notices relate, in a timely, diligent, non-arbitrary and objective manner. Where they use automated means for that processing or decision-making, they shall include information on such use in the notification referred to in paragraph 5.

[2] Cite as: DSA, Recital 50 | type: recital
Providers of hosting services play a particularly important role in tackling illegal content online, as they store information provided by and at the request of the recipients of the service and typically give other recipients access thereto, sometimes on a large scale. It is important that all providers of hosting services, regardless of their size, put in place easily accessible and user-friendly notice and action mechanisms that facilitate the notification of specific items of information that the notifying party considers to be illegal content to the provider of hosting services concerned (‘notice’), pursuant to which that provider can decide whether or not it agrees with that assessment and wishes to remove or disable access to that content (‘action’). Such mechanisms should be clearly identifiable, located close to the information in question and at least as easy to find and use as notification mechanisms for content that violates the terms and conditions of the hosting service provider. Provided the requirements on notices are met, it should be possible for individuals or entities to notify multiple specific items of allegedly illegal content through a single notice in order to ensure the effective operation of notice and action mechanisms. The notification mechanism should allow, but not require, the identification of the individual or the entity submitting a notice. For some types of items of information notified, the identity of the individual or the entity submitting a notice might be necessary to determine whether the information in question constitutes illegal content, as alleged. The obligation to put in place notice and action mechanisms should apply, for instance, to file storage and sharing services, web hosting services, advertising servers and paste bins, in so far as they qualify as hosting services covered by this Regulation.

[3] Cite as: DSA, Recital 53 | type: recital
The notice and action mechanisms should allow for the submission of notices which are sufficiently precise and adequately substantiated to enable the provider of hosting services concerned to take an informed and diligent decision, compatible with the freedom of expression and of information, in respect of the content to which the notice relates, in particular whether or not that content is to be considered illegal content and is to be removed or access thereto is to be disabled. Those mechanisms should be such as to facilitate the provision of notices that contain an explanation of the reasons why the individual or the entity submitting a notice considers that content to be illegal content, and a clear indication of the location of that content. Where a notice contains sufficient information to enable a diligent provider of hosting services to identify, without a detailed legal examination, that it is clear that the content is illegal, the notice should be considered to give rise to actual knowledge or awareness of illegality. Except for the submission of notices relating to offences referred to in Articles 3 to 7 of Directive 2011/93/EU of the European Parliament and of the Council
, those mechanisms should ask the individual or the entity submitting a notice to disclose its identity in order to avoid misuse.

[4] Cite as: DSA, Article 32 | type: article — Right to information
1. Where a provider of an online platform allowing consumers to conclude distance contracts with traders becomes aware, irrespective of the means used, that an illegal product or service has been offered by a trader to consumers located in the Union through its services, that provider shall inform, insofar as it has their contact details, consumers who purchased the illegal product or service through its services of the following:
(a) the fact that the product or service is illegal;
(b) the identity of the trader; and
(c) any relevant means of redress.
The obligation laid down in the first subparagraph shall be limited to purchases of illegal products or services made within the six months preceding the moment that the provider became aware of the illegality.
2. Where, in the situation referred to in paragraph 1, the provider of the online platform allowing consumers to conclude distance contracts with traders does not have the contact details of all consumers concerned, that provider shall make publicly available and easily accessible on its online interface the information concerning the illegal product or service, the identity of the trader and any relevant means of redress.

[5] Cite as: DSA, Recital 52 | type: recital
The rules on such notice and action mechanisms should be harmonised at Union level, so as to provide for the timely, diligent and non-arbitrary processing of notices on the basis of rules that are uniform, transparent and clear and that provide for robust safeguards to protect the right and legitimate interests of all affected parties, in particular their fundamental rights guaranteed by the Charter, irrespective of the Member State in which those parties are established or reside and of the field of law at issue. Those fundamental rights include but are not limited to: for the recipients of the service, the right to freedom of expression and of information, the right to respect for private and family life, the right to protection of personal data, the right to non-discrimination and the right to an effective remedy; for the service providers, the freedom to conduct a business, including the freedom of contract; for parties affected by illegal content, the right to human dignity, the rights of the child, the right to protection of property, including intellectual property, and the right to non-discrimination. Providers of hosting services should act upon notices in a timely manner, in particular by taking into account the type of illegal content being notified and the urgency of taking action. For instance, such providers can be expected to act without delay when allegedly illegal content involving a threat to life or safety of persons is being notified. The provider of hosting services should inform the individual or entity notifying the specific content without undue delay after taking a decision whether or not to act upon the notice.
```
</details>

---

## s16 (single)

**Question:** Can we make cancelling a subscription on our platform harder than signing up for it?

**Reference:** Online platforms must not design interfaces that deceive or manipulate users or materially distort their ability to make free and informed decisions. Making termination more difficult than subscribing is named as a practice the Commission may address in guidelines. Practices already covered by the GDPR or consumer-protection law fall under those rules instead.

**Expected:** DSA, Article 25

**Answer:**

No, making the procedure for terminating a service more difficult than subscribing to it is treated as a practice that impairs users' ability to make free and informed decisions (DSA, Article 25). 

Under the Digital Services Act, providers of online platforms must not design or organise their online interfaces in a way that deceives, manipulates, or materially distorts or impairs the ability of users to make free and informed choices (DSA, Article 25(1)). The European Commission may issue guidelines specifically targeting the practice of making the procedure for terminating a service more difficult than subscribing to it (DSA, Article 25(3)(c)).

Because this involves platform interface design rules and potential compliance risks, you should confirm with a lawyer before launch, as the exact classification depends on how your signup and cancellation flows are structured.

**Retrieved:** DSA, Article 12; DSA, Article 25; DSA, Article 54; DSA, Recital 149; DSA, Recital 58

<details><summary>search: cancelling subscription digital services act service recipient contract easy</summary>

```
[1] Cite as: DSA, Article 25 | type: article — Online interface design and organisation
1. Providers of online platforms shall not design, organise or operate their online interfaces in a way that deceives or manipulates the recipients of their service or in a way that otherwise materially distorts or impairs the ability of the recipients of their service to make free and informed decisions.
2. The prohibition in paragraph 1 shall not apply to practices covered by Directive 2005/29/EC or Regulation (EU) 2016/679.
3. The Commission may issue guidelines on how paragraph 1 applies to specific practices, notably:
(a) giving more prominence to certain choices when asking the recipient of the service for a decision;
(b) repeatedly requesting that the recipient of the service make a choice where that choice has already been made, especially by presenting pop-ups that interfere with the user experience;
(c) making the procedure for terminating a service more difficult than subscribing to it.

[2] Cite as: DSA, Article 12 | type: article — Points of contact for recipients of the service
1. Providers of intermediary services shall designate a single point of contact to enable recipients of the service to communicate directly and rapidly with them, by electronic means and in a user-friendly manner, including by allowing recipients of the service to choose the means of communication, which shall not solely rely on automated tools.
2. In addition to the obligations provided under Directive 2000/31/EC, providers of intermediary services shall make public the information necessary for the recipients of the service in order to easily identify and communicate with their single points of contact. That information shall be easily accessible, and shall be kept up to date.

[3] Cite as: DSA, Article 54 | type: article — Compensation
Recipients of the service shall have the right to seek, in accordance with Union and national law, compensation from providers of intermediary services, in respect of any damage or loss suffered due to an infringement by those providers of their obligations under this Regulation.

[4] Cite as: DSA, Recital 149 | type: recital
Without prejudice to the rights of recipients of services to turn to a representative in accordance with the Directive (EU) 2020/1828 of the European Parliament and of the Council
or to any other type of representation under national law, recipients of the services should also have the right to mandate a legal person or a public body to exercise their rights provided for in this Regulation. Such rights may include the rights related to the submission of notices, the challenging of the decisions taken by providers of intermediary services, and the lodging of complaints against the providers for infringing this Regulation. Certain bodies, organisations and associations have particular expertise and competence in detecting and flagging erroneous or unjustified content moderation decisions, and their complaints on behalf of recipients of the service may have a positive impact on freedom of expression and of information in general, therefore, providers of online platforms should treat those complaints without undue delay.

[5] Cite as: DSA, Recital 58 | type: recital
Recipients of the service should be able to easily and effectively contest certain decisions of providers of online platforms concerning the illegality of content or its incompatibility with the terms and conditions that negatively affect them. Therefore, providers of online platforms should be required to provide for internal complaint-handling systems, which meet certain conditions that aim to ensure that the systems are easily accessible and lead to swift, non-discriminatory, non-arbitrary and fair outcomes, and are subject to human review where automated means are used. Such systems should enable all recipients of the service to lodge a complaint and should not set formal requirements, such as referral to specific, relevant legal provisions or elaborate legal explanations. Recipients of the service who submitted a notice through the notice and action mechanism provided for in this Regulation or through the notification mechanism for content that violate the terms and conditions of the provider of online platforms should be entitled to use the complaint mechanism to contest the decision of the provider of online platforms on their notices, including when they consider that the action taken by that provider was not adequate. The possibility to lodge a complaint for the reversal of the contested decisions should be available for at least six months, to be calculated from the moment at which the provider of online platforms informed the recipient of the service of the decision.
```
</details>

---

## s17 (single)

**Question:** Can we show targeted ads to teenagers on our platform based on their profile?

**Reference:** No. Online platforms must not present ads based on profiling using personal data when they are aware with reasonable certainty that the user is a minor. They are not required to process additional personal data just to assess whether a user is a minor.

**Expected:** DSA, Article 28

**Answer:**

It depends on whether you are aware with reasonable certainty that the user is a minor, but generally no if they are. 

Under the Digital Services Act, providers of online platforms accessible to minors must not present advertisements on their interface that are based on profiling (as defined in the GDPR) using personal data of the service recipient when the provider is aware with reasonable certainty that the recipient is a minor (DSA, Article 28(2)). 

However, compliance with this rule does not require platforms to process additional personal data (such as collecting age data beforehand) solely to assess whether a user is a minor (DSA, Article 28(3); Recital 71). 

Because this restriction depends heavily on your platform's specific user demographics, how you handle age information, and whether your features constitute an online platform under the DSA, you should confirm with a lawyer before launch. The corpus does not cover subsequent amendments, national enforcement actions, or specific GDPR consent requirements for minors.

**Retrieved:** DSA, Article 28; DSA, Recital 69; DSA, Recital 71; DSA, Recital 89; DSA, Recital 95

<details><summary>search: targeted advertising minors children GDPR AI Act DSA</summary>

```
[1] Cite as: DSA, Recital 71 | type: recital
The protection of minors is an important policy objective of the Union. An online platform can be considered to be accessible to minors when its terms and conditions permit minors to use the service, when its service is directed at or predominantly used by minors, or where the provider is otherwise aware that some of the recipients of its service are minors, for example because it already processes personal data of the recipients of its service revealing their age for other purposes. Providers of online platforms used by minors should take appropriate and proportionate measures to protect minors, for example by designing their online interfaces or parts thereof with the highest level of privacy, safety and security for minors by default where appropriate or adopting standards for protection of minors, or participating in codes of conduct for protecting minors. They should consider best practices and available guidance, such as that provided by the communication of the Commission on A Digital Decade for children and youth: the new European strategy for a better internet for kids (BIK+). Providers of online platforms should not present advertisements based on profiling using personal data of the recipient of the service when they are aware with reasonable certainty that the recipient of the service is a minor. In accordance with Regulation (EU) 2016/679, notably the principle of data minimisation as provided for in Article 5(1), point (c), thereof, this prohibition should not lead the provider of the online platform to maintain, acquire or process more personal data than it already has in order to assess if the recipient of the service is a minor. Thus, this obligation should not incentivize providers of online platforms to collect the age of the recipient of the service prior to their use. It should be without prejudice to Union law on protection of personal data.

[2] Cite as: DSA, Article 28 | type: article — Online protection of minors
1. Providers of online platforms accessible to minors shall put in place appropriate and proportionate measures to ensure a high level of privacy, safety, and security of minors, on their service.
2. Providers of online platform shall not present advertisements on their interface based on profiling as defined in Article 4, point (4), of Regulation (EU) 2016/679 using personal data of the recipient of the service when they are aware with reasonable certainty that the recipient of the service is a minor.
3. Compliance with the obligations set out in this Article shall not oblige providers of online platforms to process additional personal data in order to assess whether the recipient of the service is a minor.
4. The Commission, after consulting the Board, may issue guidelines to assist providers of online platforms in the application of paragraph 1.

[3] Cite as: DSA, Recital 69 | type: recital
When recipients of the service are presented with advertisements based on targeting techniques optimised to match their interests and potentially appeal to their vulnerabilities, this can have particularly serious negative effects. In certain cases, manipulative techniques can negatively impact entire groups and amplify societal harms, for example by contributing to disinformation campaigns or by discriminating against certain groups. Online platforms are particularly sensitive environments for such practices and they present a higher societal risk. Consequently, providers of online platforms should not present advertisements based on profiling as defined in Article 4, point (4), of Regulation (EU) 2016/679, using special categories of personal data referred to in Article 9(1) of that Regulation, including by using profiling categories based on those special categories. This prohibition is without prejudice to the obligations applicable to providers of online platforms or any other service provider or advertiser involved in the dissemination of the advertisements under Union law on protection of personal data.

[4] Cite as: DSA, Recital 89 | type: recital
Providers of very large online platforms and of very large online search engines should take into account the best interests of minors in taking measures such as adapting the design of their service and their online interface, especially when their services are aimed at minors or predominantly used by them. They should ensure that their services are organised in a way that allows minors to access easily mechanisms provided for in this Regulation, where applicable, including notice and action and complaint mechanisms. They should also take measures to protect minors from content that may impair their physical, mental or moral development and provide tools that enable conditional access to such information. In selecting the appropriate mitigation measures, providers can consider, where appropriate, industry best practices, including as established through self-regulatory cooperation, such as codes of conduct, and should take into account the guidelines from the Commission.

[5] Cite as: DSA, Recital 95 | type: recital
Advertising systems used by very large online platforms and very large online search engines pose particular risks and require further public and regulatory supervision on account of their scale and ability to target and reach recipients of the service based on their behaviour within and outside that platform’s or search engine's online interface. Very large online platforms or very large online search engines should ensure public access to repositories of advertisements presented on their online interfaces to facilitate supervision and research into emerging risks brought about by the distribution of advertising online, for example in relation to illegal advertisements or manipulative techniques and disinformation with a real and foreseeable negative impact on public health, public security, civil discourse, political participation and equality. Repositories should include the content of advertisements, including the name of the product, service or brand and the subject matter of the advertisement, and related data on the advertiser, and, if different, the natural or legal person who paid for the advertisement, and the delivery of the advertisement, in particular where targeted advertising is concerned. This information should include both information about targeting criteria and delivery criteria, in particular when advertisements are delivered to persons in vulnerable situations, such as minors.
```
</details>

---

## s18 (single)

**Question:** At what point does our platform count as a 'very large online platform'?

**Reference:** When it has an average of at least 45 million monthly active recipients in the EU and the Commission designates it as a very large online platform.

**Expected:** DSA, Article 33

**Answer:**

It depends on reaching a threshold of active users in the European Union, and being formally designated by the European Commission (DSA, Article 33). 

Your platform counts as a very large online platform (VLOP) when it has an average of **45 million or more monthly active recipients of the service in the Union** (DSA, Article 33). This numeric threshold represents 10% of the EU population (DSA, Recital 76).

Key details for your calculation:
* **Active recipients:** This includes anyone actually engaging with your service at least once a month (such as viewing or listening to information), not just registered users (DSA, Recital 77). 
* **Formal designation:** Crossing the 45 million threshold is the factual trigger, but the platform must also be formally designated as a VLOP by a decision of the European Commission, based on user data reported by providers and other available information (DSA, Article 33).

Because classification depends on precise user metrics across interfaces and potential Commission methodology rules, you should consult a lawyer to confirm how your platform measures monthly active recipients before concluding whether your user numbers cross the threshold.

**Retrieved:** DSA, Article 33; DSA, Recital 65; DSA, Recital 75; DSA, Recital 76; DSA, Recital 77

<details><summary>search: very large online platform threshold recipients DSA</summary>

```
[1] Cite as: DSA, Recital 76 | type: recital
Very large online platforms and very large online search engines may cause societal risks, different in scope and impact from those caused by smaller platforms. Providers of such very large online platforms and of very large online search engines should therefore bear the highest standard of due diligence obligations, proportionate to their societal impact. Once the number of active recipients of an online platform or of active recipients of an online search engine, calculated as an average over a period of six months, reaches a significant share of the Union population, the systemic risks the online platform or online search engine poses may have a disproportionate impact in the Union. Such significant reach should be considered to exist where such number exceeds an operational threshold set at 45 million, that is, a number equivalent to 10 % of the Union population. This operational threshold should be kept up to date and therefore the Commission should be empowered to supplement the provisions of this Regulation by adopting delegated acts, where necessary.

[2] Cite as: DSA, Article 33 | type: article — Very large online platforms and very large online search engines (part 1 of 2)
1. This Section shall apply to online platforms and online search engines which have a number of average monthly active recipients of the service in the Union equal to or higher than 45 million, and which are designated as very large online platforms or very large online search engines pursuant to paragraph 4.
2. The Commission shall adopt delegated acts in accordance with Article 87 to adjust the number of average monthly active recipients of the service in the Union referred to in paragraph 1, where the Union’s population increases or decreases at least by 5 % in relation to its population in 2020 or its population after adjustment by means of a delegated act in the year in which the latest delegated act was adopted. In such a case, it shall adjust the number so that it corresponds to 10 % of the Union’s population in the year in which it adopts the delegated act, rounded up or down to allow the number to be expressed in millions.
3. The Commission may adopt delegated acts in accordance with Article 87, after consulting the Board, to supplement the provisions of this Regulation by laying down the methodology for calculating the number of average monthly active recipients of the service in the Union, for the purposes of paragraph 1 of this Article and Article 24(2), ensuring that the methodology takes account of market and technological developments.
4. The Commission shall, after having consulted the Member State of establishment or after taking into account the information provided by the Digital Services Coordinator of establishment pursuant to Article 24(4), adopt a decision designating as a very large online platform or a very large online search engine for the purposes of this Regulation the online platform or the online search engine which has a number of average monthly active recipients of the service equal to or higher than the number referred to in paragraph 1 of this Article. The Commission shall take its decision on the basis of data reported by the provider of the online platform or of the online search engine pursuant to Article 24(2), or information requested pursuant to Article 24(3) or any other information available to the Commission.
The failure by the provider of the online platform or of the online search engine to comply with Article 24(2) or to comply with the request by the Digital Services Coordinator of establishment or by the Commission pursuant to Article 24(3) shall not prevent the Commission from designating that provider as a provider of a very large online platform or of a very large online search engine pursuant to this paragraph.
Where the Commission bases its decision on other information available to the Commission pursuant to the first subparagraph of this paragraph or on the basis of additional information requested pursuant to Article 24(3), the Commission shall give the provider of the online platform or of the online search engine concerned 10 working days in which to submit its views on the Commission’s preliminary findings and on its intention to designate the online platform or the online search engine as a very large online platform or as a very large online search engine, respectively. The Commission shall take due account of the views submitted by the provider concerned.

[3] Cite as: DSA, Recital 75 | type: recital
Given the importance of very large online platforms, due to their reach, in particular as expressed in the number of recipients of the service, in facilitating public debate, economic transactions and the dissemination to the public of information, opinions and ideas and in influencing how recipients obtain and communicate information online, it is necessary to impose specific obligations on the providers of those platforms, in addition to the obligations applicable to all online platforms. Due to their critical role in locating and making information retrievable online, it is also necessary to impose those obligations, to the extent they are applicable, on the providers of very large online search engines. Those additional obligations on providers of very large online platforms and of very large online search engines are necessary to address those public policy concerns, there being no alternative and less restrictive measures that would effectively achieve the same result.

[4] Cite as: DSA, Recital 77 | type: recital
In order to determine the reach of a given online platform or online search engine, it is necessary to establish the average number of active recipients of each service individually. Accordingly, the number of average monthly active recipients of an online platform should reflect all the recipients actually engaging with the service at least once in a given period of time, by being exposed to information disseminated on the online interface of the online platform, such as viewing it or listening to it, or by providing information, such as traders on an online platforms allowing consumers to conclude distance contracts with traders.
For the purposes of this Regulation, engagement is not limited to interacting with information by clicking on, commenting, linking, sharing, purchasing or carrying out transactions on an online platform. Consequently, the concept of active recipient of the service does not necessarily coincide with that of a registered user of a service. As regards online search engines, the concept of active recipients of the service should cover those who view information on their online interface, but not, for example, the owners of the websites indexed by an online search engine, as they do not actively engage with the service. The number of active recipients of a service should include all unique recipients of the service that engage with the specific service. To this effect, a recipient of the service that uses different online interfaces, such as websites or applications, including where the services are accessed through different uniform resource locators (URLs) or domain names, should, where possible, be counted only once. However, the concept of active recipient of the service should not include incidental use of the service by recipients of other providers of intermediary services that indirectly make available information hosted by the provider of online platforms through linking or indexing by a provider of online search engine. Further, this Regulation does not require providers of online platforms or of online search engines to perform specific tracking of individuals online. Where such providers are able to discount automated users such as bots or scrapers without further processing of personal data and tracking, they may do so. The determination of the number of active recipients of the service can be impacted by market and technical developments and therefore the Commission should be empowered to supplement the provisions of this Regulation by adopting delegated acts laying down the methodology to determine the active recipients of an online platform or of an online search engine, where necessary, reflecting the nature of the service and the way recipients of the service interact with it.

[5] Cite as: DSA, Recital 65 | type: recital
In view of the particular responsibilities and obligations of providers of online platforms, they should be made subject to transparency reporting obligations, which apply in addition to the transparency reporting obligations applicable to all providers of intermediary services under this Regulation. For the purposes of determining whether online platforms and online search engines may be very large online platforms or very large online search engines, respectively, that are subject to certain additional obligations under this Regulation, the transparency reporting obligations for online platforms and online search engines should include certain obligations relating to the publication and communication of information on the average monthly active recipients of the service in the Union.
```
</details>

---

## s19 (single)

**Question:** Our app automatically rejects loan applicants using an algorithm with no human review. Is that allowed?

**Reference:** People have the right not to be subject to a decision based solely on automated processing, including profiling, that has legal or similarly significant effects. It is allowed only if necessary for a contract, authorised by law, or based on explicit consent, and then the person must be able to obtain human intervention, express their view and contest the decision.

**Expected:** GDPR, Article 22

**Answer:**

It depends on your legal basis, but an automated credit rejection without human review is strictly regulated and generally restricted under EU law. 

### 1. The GDPR Restrictions
Under the GDPR, individuals have the right **not** to be subject to a decision based solely on automated processing (including profiling) that produces legal effects or similarly significantly affects them—such as the automatic refusal of an online credit application (GDPR, Article 22(1); GDPR, Recital 71). 

An automatic rejection *is* allowed only if it meets one of three exceptions (GDPR, Article 22(2)):
* It is necessary for entering into, or performance of, a contract between the applicant and you;
* It is authorised by Union or Member State law; or
* It is based on the applicant's explicit consent.

Even if you rely on contract performance or consent, you **must** implement suitable safeguards, including giving the applicant the right to obtain human intervention, express their point of view, and contest the decision (GDPR, Article 22(3); GDPR, Recital 71). Furthermore, this type of systematic evaluation triggers the requirement to perform a Data Protection Impact Assessment (DPIA) beforehand (GDPR, Article 35(3)).

### 2. The AI Act Classification
Under the AI Act, AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score are explicitly classified as **high-risk AI systems** (AI Act, Annex III; AI Act, Recital 58). 

Because your system evaluates credit scores, it falls into this high-risk category, which carries heavy compliance obligations regarding data governance, technical documentation, transparency, risk management, and human oversight.

### Next Steps
Because this feature involves both high-risk AI obligations and strict automated decision-making prohibitions under the GDPR, you should **consult a lawyer before launch** to confirm whether your legal basis (such as contract necessity) is sufficient and whether your human oversight mechanisms satisfy EU requirements.

**Retrieved:** AI Act, Annex III; AI Act, Article 6; AI Act, Article 7; AI Act, Recital 58; GDPR, Article 22; GDPR, Article 35; GDPR, Recital 71; GDPR, Recital 72; GDPR, Recital 75

<details><summary>search: loan applicant credit scoring high risk AI Act Annex III</summary>

```
[1] Cite as: AI Act, Annex III | type: annex — High-risk AI systems referred to in Article 6(2) (part 1 of 3)
High-risk AI systems pursuant to Article 6(2) are the AI systems listed in any of the following areas:
1. Biometrics, in so far as their use is permitted under relevant Union or national law:
(a) remote biometric identification systems.
This shall not include AI systems intended to be used for biometric verification the sole purpose of which is to confirm that a specific natural person is the person he or she claims to be;
(b) AI systems intended to be used for biometric categorisation, according to sensitive or protected attributes or characteristics based on the inference of those attributes or characteristics;
(c) AI systems intended to be used for emotion recognition.
2. Critical infrastructure: AI systems intended to be used as safety components in the management and operation of critical digital infrastructure, road traffic, or in the supply of water, gas, heating or electricity.
3. Education and vocational training:
(a) AI systems intended to be used to determine access or admission or to assign natural persons to educational and vocational training institutions at all levels;
(b) AI systems intended to be used to evaluate learning outcomes, including when those outcomes are used to steer the learning process of natural persons in educational and vocational training institutions at all levels;
(c) AI systems intended to be used for the purpose of assessing the appropriate level of education that an individual will receive or will be able to access, in the context of or within educational and vocational training institutions at all levels;
(d) AI systems intended to be used for monitoring and detecting prohibited behaviour of students during tests in the context of or within educational and vocational training institutions at all levels.
4. Employment, workers’ management and access to self-employment:
(a) AI systems intended to be used for the recruitment or selection of natural persons, in particular to place targeted job advertisements, to analyse and filter job applications, and to evaluate candidates;
(b) AI systems intended to be used to make decisions affecting terms of work-related relationships, the promotion or termination of work-related contractual relationships, to allocate tasks based on individual behaviour or personal traits or characteristics or to monitor and evaluate the performance and behaviour of persons in such relationships.
5. Access to and enjoyment of essential private services and essential public services and benefits:
(a) AI systems intended to be used by public authorities or on behalf of public authorities to evaluate the eligibility of natural persons for essential public assistance benefits and services, including healthcare services, as well as to grant, reduce, revoke, or reclaim such benefits and services;
(b) AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score, with the exception of AI systems used for the purpose of detecting financial fraud;
(c) AI systems intended to be used for risk assessment and pricing in relation to natural persons in the case of life and health insurance;
(d) AI systems intended to evaluate and classify emergency calls by natural persons or to be used to dispatch, or to establish priority in the dispatching of, emergency first response services, including by police, firefighters and medical aid, as well as of emergency healthcare patient triage systems.
6. Law enforcement, in so far as their use is permitted under relevant Union or national law:

[2] Cite as: AI Act, Recital 58 | type: recital
Another area in which the use of AI systems deserves special consideration is the access to and enjoyment of certain essential private and public services and benefits necessary for people to fully participate in society or to improve one’s standard of living. In particular, natural persons applying for or receiving essential public assistance benefits and services from public authorities namely healthcare services, social security benefits, social services providing protection in cases such as maternity, illness, industrial accidents, dependency or old age and loss of employment and social and housing assistance, are typically dependent on those benefits and services and in a vulnerable position in relation to the responsible authorities. If AI systems are used for determining whether such benefits and services should be granted, denied, reduced, revoked or reclaimed by authorities, including whether beneficiaries are legitimately entitled to such benefits or services, those systems may have a significant impact on persons’ livelihood and may infringe their fundamental rights, such as the right to social protection, non-discrimination, human dignity or an effective remedy and should therefore be classified as high-risk. Nonetheless, this Regulation should not hamper the development and use of innovative approaches in the public administration, which would stand to benefit from a wider use of compliant and safe AI systems, provided that those systems do not entail a high risk to legal and natural persons. In addition, AI systems used to evaluate the credit score or creditworthiness of natural persons should be classified as high-risk AI systems, since they determine those persons’ access to financial resources or essential services such as housing, electricity, and telecommunication services. AI systems used for those purposes may lead to discrimination between persons or groups and may perpetuate historical patterns of discrimination, such as that based on racial or ethnic origins, gender, disabilities, age or sexual orientation, or may create new forms of discriminatory impacts. However, AI systems provided for by Union law for the purpose of detecting fraud in the offering of financial services and for prudential purposes to calculate credit institutions’ and insurance undertakings’ capital requirements should not be considered to be high-risk under this Regulation. Moreover, AI systems intended to be used for risk assessment and pricing in relation to natural persons for health and life insurance can also have a significant impact on persons’ livelihood and if not duly designed, developed and used, can infringe their fundamental rights and can lead to serious consequences for people’s life and health, including financial exclusion and discrimination. Finally, AI systems used to evaluate and classify emergency calls by natural persons or to dispatch or establish priority in the dispatching of emergency first response services, including by police, firefighters and medical aid, as well as of emergency healthcare patient triage systems, should also be classified as high-risk since they make decisions in very critical situations for the life and health of persons and their property.

[3] Cite as: AI Act, Annex III | type: annex — High-risk AI systems referred to in Article 6(2) (part 2 of 3)
(a) AI systems intended to be used by or on behalf of law enforcement authorities, or by Union institutions, bodies, offices or agencies in support of law enforcement authorities or on their behalf to assess the risk of a natural person becoming the victim of criminal offences;
(b) AI systems intended to be used by or on behalf of law enforcement authorities or by Union institutions, bodies, offices or agencies in support of law enforcement authorities as polygraphs or similar tools;
(c) AI systems intended to be used by or on behalf of law enforcement authorities, or by Union institutions, bodies, offices or agencies, in support of law enforcement authorities to evaluate the reliability of evidence in the course of the investigation or prosecution of criminal offences;
(d) AI systems intended to be used by law enforcement authorities or on their behalf or by Union institutions, bodies, offices or agencies in support of law enforcement authorities for assessing the risk of a natural person offending or re-offending not solely on the basis of the profiling of natural persons as referred to in Article 3(4) of Directive (EU) 2016/680, or to assess personality traits and characteristics or past criminal behaviour of natural persons or groups;
(e) AI systems intended to be used by or on behalf of law enforcement authorities or by Union institutions, bodies, offices or agencies in support of law enforcement authorities for the profiling of natural persons as referred to in Article 3(4) of Directive (EU) 2016/680 in the course of the detection, investigation or prosecution of criminal offences.
7. Migration, asylum and border control management, in so far as their use is permitted under relevant Union or national law:
(a) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies as polygraphs or similar tools;
(b) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies to assess a risk, including a security risk, a risk of irregular migration, or a health risk, posed by a natural person who intends to enter or who has entered into the territory of a Member State;
(c) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies to assist competent public authorities for the examination of applications for asylum, visa or residence permits and for associated complaints with regard to the eligibility of the natural persons applying for a status, including related assessments of the reliability of evidence;
(d) AI systems intended to be used by or on behalf of competent public authorities, or by Union institutions, bodies, offices or agencies, in the context of migration, asylum or border control management, for the purpose of detecting, recognising or identifying natural persons, with the exception of the verification of travel documents.
8. Administration of justice and democratic processes:
(a) AI systems intended to be used by a judicial authority or on their behalf to assist a judicial authority in researching and interpreting facts and the law and in applying the law to a concrete set of facts, or to be used in a similar way in alternative dispute resolution;

[4] Cite as: AI Act, Article 6 | type: article — Classification rules for high-risk AI systems (part 1 of 2)
1. Irrespective of whether an AI system is placed on the market or put into service independently of the products referred to in points (a) and (b), that AI system shall be considered to be high-risk where both of the following conditions are fulfilled:
(a) the AI system is intended to be used as a safety component of a product, or the AI system is itself a product, covered by the Union harmonisation legislation listed in Annex I;
(b) the product whose safety component pursuant to point (a) is the AI system, or the AI system itself as a product, is required to undergo a third-party conformity assessment, with a view to the placing on the market or the putting into service of that product pursuant to the Union harmonisation legislation listed in Annex I.
2. In addition to the high-risk AI systems referred to in paragraph 1, AI systems referred to in Annex III shall be considered to be high-risk.
3. By derogation from paragraph 2, an AI system referred to in Annex III shall not be considered to be high-risk where it does not pose a significant risk of harm to the health, safety or fundamental rights of natural persons, including by not materially influencing the outcome of decision making.
The first subparagraph shall apply where any of the following conditions is fulfilled:
(a) the AI system is intended to perform a narrow procedural task;
(b) the AI system is intended to improve the result of a previously completed human activity;
(c) the AI system is intended to detect decision-making patterns or deviations from prior decision-making patterns and is not meant to replace or influence the previously completed human assessment, without proper human review; or
(d) the AI system is intended to perform a preparatory task to an assessment relevant for the purposes of the use cases listed in Annex III.
Notwithstanding the first subparagraph, an AI system referred to in Annex III shall always be considered to be high-risk where the AI system performs profiling of natural persons.
4. A provider who considers that an AI system referred to in Annex III is not high-risk shall document its assessment before that system is placed on the market or put into service. Such provider shall be subject to the registration obligation set out in Article 49(2). Upon request of national competent authorities, the provider shall provide the documentation of the assessment.
5. The Commission shall, after consulting the European Artificial Intelligence Board (the ‘Board’), and no later than 2 February 2026, provide guidelines specifying the practical implementation of this Article in line with Article 96 together with a comprehensive list of practical examples of use cases of AI systems that are high-risk and not high-risk.
6. The Commission is empowered to adopt delegated acts in accordance with Article 97 in order to amend paragraph 3, second subparagraph, of this Article by adding new conditions to those laid down therein, or by modifying them, where there is concrete and reliable evidence of the existence of AI systems that fall under the scope of Annex III, but do not pose a significant risk of harm to the health, safety or fundamental rights of natural persons.
7. The Commission shall adopt delegated acts in accordance with Article 97 in order to amend paragraph 3, second subparagraph, of this Article by deleting any of the conditions laid down therein, where there is concrete and reliable evidence that this is necessary to maintain the level of protection of health, safety and fundamental rights provided for by this Regulation.

[5] Cite as: AI Act, Article 7 | type: article — Amendments to Annex III
1. The Commission is empowered to adopt delegated acts in accordance with Article 97 to amend Annex III by adding or modifying use-cases of high-risk AI systems where both of the following conditions are fulfilled:
(a) the AI systems are intended to be used in any of the areas listed in Annex III;
(b) the AI systems pose a risk of harm to health and safety, or an adverse impact on fundamental rights, and that risk is equivalent to, or greater than, the risk of harm or of adverse impact posed by the high-risk AI systems already referred to in Annex III.
2. When assessing the condition under paragraph 1, point (b), the Commission shall take into account the following criteria:
(a) the intended purpose of the AI system;
(b) the extent to which an AI system has been used or is likely to be used;
(c) the nature and amount of the data processed and used by the AI system, in particular whether special categories of personal data are processed;
(d) the extent to which the AI system acts autonomously and the possibility for a human to override a decision or recommendations that may lead to potential harm;
(e) the extent to which the use of an AI system has already caused harm to health and safety, has had an adverse impact on fundamental rights or has given rise to significant concerns in relation to the likelihood of such harm or adverse impact, as demonstrated, for example, by reports or documented allegations submitted to national competent authorities or by other reports, as appropriate;
(f) the potential extent of such harm or such adverse impact, in particular in terms of its intensity and its ability to affect multiple persons or to disproportionately affect a particular group of persons;
(g) the extent to which persons who are potentially harmed or suffer an adverse impact are dependent on the outcome produced with an AI system, in particular because for practical or legal reasons it is not reasonably possible to opt-out from that outcome;
(h) the extent to which there is an imbalance of power, or the persons who are potentially harmed or suffer an adverse impact are in a vulnerable position in relation to the deployer of an AI system, in particular due to status, authority, knowledge, economic or social circumstances, or age;
(i) the extent to which the outcome produced involving an AI system is easily corrigible or reversible, taking into account the technical solutions available to correct or reverse it, whereby outcomes having an adverse impact on health, safety or fundamental rights, shall not be considered to be easily corrigible or reversible;
(j) the magnitude and likelihood of benefit of the deployment of the AI system for individuals, groups, or society at large, including possible improvements in product safety;
(k) the extent to which existing Union law provides for:
(i) effective measures of redress in relation to the risks posed by an AI system, with the exclusion of claims for damages;
(ii) effective measures to prevent or substantially minimise those risks.
3. The Commission is empowered to adopt delegated acts in accordance with Article 97 to amend the list in Annex III by removing high-risk AI systems where both of the following conditions are fulfilled:
(a) the high-risk AI system concerned no longer poses any significant risks to fundamental rights, health or safety, taking into account the criteria listed in paragraph 2;
(b) the deletion does not decrease the overall level of protection of health, safety and fundamental rights under Union law.
```
</details>

<details><summary>search: GDPR automated decision making Article 22 profiling loan applicants</summary>

```
[1] Cite as: GDPR, Article 22 | type: article — Automated individual decision-making, including profiling
1. The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her.
2. Paragraph 1 shall not apply if the decision:
(a) is necessary for entering into, or performance of, a contract between the data subject and a data controller;
(b) is authorised by Union or Member State law to which the controller is subject and which also lays down suitable measures to safeguard the data subject's rights and freedoms and legitimate interests; or
(c) is based on the data subject's explicit consent.
3. In the cases referred to in points (a) and (c) of paragraph 2, the data controller shall implement suitable measures to safeguard the data subject's rights and freedoms and legitimate interests, at least the right to obtain human intervention on the part of the controller, to express his or her point of view and to contest the decision.
4. Decisions referred to in paragraph 2 shall not be based on special categories of personal data referred to in Article 9(1), unless point (a) or (g) of Article 9(2) applies and suitable measures to safeguard the data subject's rights and freedoms and legitimate interests are in place.

[2] Cite as: GDPR, Recital 71 | type: recital
The data subject should have the right not to be subject to a decision, which may include a measure, evaluating personal aspects relating to him or her which is based solely on automated processing and which produces legal effects concerning him or her or similarly significantly affects him or her, such as automatic refusal of an online credit application or e-recruiting practices without any human intervention. Such processing includes ‘profiling’ that consists of any form of automated processing of personal data evaluating the personal aspects relating to a natural person, in particular to analyse or predict aspects concerning the data subject's performance at work, economic situation, health, personal preferences or interests, reliability or behaviour, location or movements, where it produces legal effects concerning him or her or similarly significantly affects him or her. However, decision-making based on such processing, including profiling, should be allowed where expressly authorised by Union or Member State law to which the controller is subject, including for fraud and tax-evasion monitoring and prevention purposes conducted in accordance with the regulations, standards and recommendations of Union institutions or national oversight bodies and to ensure the security and reliability of a service provided by the controller, or necessary for the entering or performance of a contract between the data subject and a controller, or when the data subject has given his or her explicit consent. In any case, such processing should be subject to suitable safeguards, which should include specific information to the data subject and the right to obtain human intervention, to express his or her point of view, to obtain an explanation of the decision reached after such assessment and to challenge the decision. Such measure should not concern a child.
In order to ensure fair and transparent processing in respect of the data subject, taking into account the specific circumstances and context in which the personal data are processed, the controller should use appropriate mathematical or statistical procedures for the profiling, implement technical and organisational measures appropriate to ensure, in particular, that factors which result in inaccuracies in personal data are corrected and the risk of errors is minimised, secure personal data in a manner that takes account of the potential risks involved for the interests and rights of the data subject and that prevents, inter alia, discriminatory effects on natural persons on the basis of racial or ethnic origin, political opinion, religion or beliefs, trade union membership, genetic or health status or sexual orientation, or that result in measures having such an effect. Automated decision-making and profiling based on special categories of personal data should be allowed only under specific conditions.

[3] Cite as: GDPR, Recital 72 | type: recital
Profiling is subject to the rules of this Regulation governing the processing of personal data, such as the legal grounds for processing or data protection principles. The European Data Protection Board established by this Regulation (the ‘Board’) should be able to issue guidance in that context.

[4] Cite as: GDPR, Article 35 | type: article — Data protection impact assessment (part 1 of 2)
1. Where a type of processing in particular using new technologies, and taking into account the nature, scope, context and purposes of the processing, is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall, prior to the processing, carry out an assessment of the impact of the envisaged processing operations on the protection of personal data. A single assessment may address a set of similar processing operations that present similar high risks.
2. The controller shall seek the advice of the data protection officer, where designated, when carrying out a data protection impact assessment.
3. A data protection impact assessment referred to in paragraph 1 shall in particular be required in the case of:
(a) a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person;
(b) processing on a large scale of special categories of data referred to in Article 9(1), or of personal data relating to criminal convictions and offences referred to in Article 10; or
(c) a systematic monitoring of a publicly accessible area on a large scale.
4. The supervisory authority shall establish and make public a list of the kind of processing operations which are subject to the requirement for a data protection impact assessment pursuant to paragraph 1. The supervisory authority shall communicate those lists to the Board referred to in Article 68.
5. The supervisory authority may also establish and make public a list of the kind of processing operations for which no data protection impact assessment is required. The supervisory authority shall communicate those lists to the Board.
6. Prior to the adoption of the lists referred to in paragraphs 4 and 5, the competent supervisory authority shall apply the consistency mechanism referred to in Article 63 where such lists involve processing activities which are related to the offering of goods or services to data subjects or to the monitoring of their behaviour in several Member States, or may substantially affect the free movement of personal data within the Union.
7. The assessment shall contain at least:
(a) a systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitimate interest pursued by the controller;
(b) an assessment of the necessity and proportionality of the processing operations in relation to the purposes;
(c) an assessment of the risks to the rights and freedoms of data subjects referred to in paragraph 1; and
(d) the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned.
8. Compliance with approved codes of conduct referred to in Article 40 by the relevant controllers or processors shall be taken into due account in assessing the impact of the processing operations performed by such controllers or processors, in particular for the purposes of a data protection impact assessment.
9. Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to the protection of commercial or public interests or the security of processing operations.

[5] Cite as: GDPR, Recital 75 | type: recital
The risk to the rights and freedoms of natural persons, of varying likelihood and severity, may result from personal data processing which could lead to physical, material or non-material damage, in particular: where the processing may give rise to discrimination, identity theft or fraud, financial loss, damage to the reputation, loss of confidentiality of personal data protected by professional secrecy, unauthorised reversal of pseudonymisation, or any other significant economic or social disadvantage; where data subjects might be deprived of their rights and freedoms or prevented from exercising control over their personal data; where personal data are processed which reveal racial or ethnic origin, political opinions, religion or philosophical beliefs, trade union membership, and the processing of genetic data, data concerning health or data concerning sex life or criminal convictions and offences or related security measures; where personal aspects are evaluated, in particular analysing or predicting aspects concerning performance at work, economic situation, health, personal preferences or interests, reliability or behaviour, location or movements, in order to create or use personal profiles; where personal data of vulnerable natural persons, in particular of children, are processed; or where processing involves a large amount of personal data and affects a large number of data subjects.
```
</details>

---

## s20 (single)

**Question:** Can our wellness app process health data from users' fitness trackers?

**Reference:** Health data is a special category, so processing is prohibited unless an exception applies. For a consumer app the most relevant is the user's explicit consent for one or more specified purposes.

**Expected:** GDPR, Article 9

**Answer:**

It depends on whether you meet the strict conditions for processing health data under the GDPR. 

Data concerning health—which includes information on physical or mental health status, disease risk, or physiological state—is classified as a special category of personal data (GDPR, Recital 35). As a general rule, processing health data is **prohibited** (GDPR, Article 9(1)).

However, you can process health data from fitness trackers if you satisfy an exception under GDPR Article 9(2). The most relevant exception for a wellness app is usually **explicit consent**: the data subject must have given explicit consent to the processing of those personal data for one or more specified purposes (GDPR, Article 9(2)(a)), unless Union or Member State law provides otherwise. Other exceptions under Article 9 generally apply to healthcare professionals, employment, or substantial public interest grounds.

Because health data requires higher protection, whether your feature can launch depends on facts you have not provided, such as how you collect and record explicit consent and whether national laws place additional conditions on health data processing. For high-stakes decisions like handling health data, we recommend confirming your approach with a lawyer before launch.

**Retrieved:** GDPR, Article 9; GDPR, Recital 35; GDPR, Recital 52; GDPR, Recital 53; GDPR, Recital 54

<details><summary>search: processing health data fitness trackers GDPR special categories consent</summary>

```
[1] Cite as: GDPR, Article 9 | type: article — Processing of special categories of personal data (part 1 of 2)
1. Processing of personal data revealing racial or ethnic origin, political opinions, religious or philosophical beliefs, or trade union membership, and the processing of genetic data, biometric data for the purpose of uniquely identifying a natural person, data concerning health or data concerning a natural person's sex life or sexual orientation shall be prohibited.
2. Paragraph 1 shall not apply if one of the following applies:
(a) the data subject has given explicit consent to the processing of those personal data for one or more specified purposes, except where Union or Member State law provide that the prohibition referred to in paragraph 1 may not be lifted by the data subject;
(b) processing is necessary for the purposes of carrying out the obligations and exercising specific rights of the controller or of the data subject in the field of employment and social security and social protection law in so far as it is authorised by Union or Member State law or a collective agreement pursuant to Member State law providing for appropriate safeguards for the fundamental rights and the interests of the data subject;
(c) processing is necessary to protect the vital interests of the data subject or of another natural person where the data subject is physically or legally incapable of giving consent;
(d) processing is carried out in the course of its legitimate activities with appropriate safeguards by a foundation, association or any other not-for-profit body with a political, philosophical, religious or trade union aim and on condition that the processing relates solely to the members or to former members of the body or to persons who have regular contact with it in connection with its purposes and that the personal data are not disclosed outside that body without the consent of the data subjects;
(e) processing relates to personal data which are manifestly made public by the data subject;
(f) processing is necessary for the establishment, exercise or defence of legal claims or whenever courts are acting in their judicial capacity;
(g) processing is necessary for reasons of substantial public interest, on the basis of Union or Member State law which shall be proportionate to the aim pursued, respect the essence of the right to data protection and provide for suitable and specific measures to safeguard the fundamental rights and the interests of the data subject;
(h) processing is necessary for the purposes of preventive or occupational medicine, for the assessment of the working capacity of the employee, medical diagnosis, the provision of health or social care or treatment or the management of health or social care systems and services on the basis of Union or Member State law or pursuant to contract with a health professional and subject to the conditions and safeguards referred to in paragraph 3;
(i) processing is necessary for reasons of public interest in the area of public health, such as protecting against serious cross-border threats to health or ensuring high standards of quality and safety of health care and of medicinal products or medical devices, on the basis of Union or Member State law which provides for suitable and specific measures to safeguard the rights and freedoms of the data subject, in particular professional secrecy;

[2] Cite as: GDPR, Recital 54 | type: recital
The processing of special categories of personal data may be necessary for reasons of public interest in the areas of public health without consent of the data subject. Such processing should be subject to suitable and specific measures so as to protect the rights and freedoms of natural persons. In that context, ‘public health’ should be interpreted as defined in Regulation (EC) No 1338/2008 of the European Parliament and of the Council
, namely all elements related to health, namely health status, including morbidity and disability, the determinants having an effect on that health status, health care needs, resources allocated to health care, the provision of, and universal access to, health care as well as health care expenditure and financing, and the causes of mortality. Such processing of data concerning health for reasons of public interest should not result in personal data being processed for other purposes by third parties such as employers or insurance and banking companies.

[3] Cite as: GDPR, Recital 53 | type: recital
Special categories of personal data which merit higher protection should be processed for health-related purposes only where necessary to achieve those purposes for the benefit of natural persons and society as a whole, in particular in the context of the management of health or social care services and systems, including processing by the management and central national health authorities of such data for the purpose of quality control, management information and the general national and local supervision of the health or social care system, and ensuring continuity of health or social care and cross-border healthcare or health security, monitoring and alert purposes, or for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes, based on Union or Member State law which has to meet an objective of public interest, as well as for studies conducted in the public interest in the area of public health. Therefore, this Regulation should provide for harmonised conditions for the processing of special categories of personal data concerning health, in respect of specific needs, in particular where the processing of such data is carried out for certain health-related purposes by persons subject to a legal obligation of professional secrecy. Union or Member State law should provide for specific and suitable measures so as to protect the fundamental rights and the personal data of natural persons. Member States should be allowed to maintain or introduce further conditions, including limitations, with regard to the processing of genetic data, biometric data or data concerning health. However, this should not hamper the free flow of personal data within the Union when those conditions apply to cross-border processing of such data.

[4] Cite as: GDPR, Recital 35 | type: recital
Personal data concerning health should include all data pertaining to the health status of a data subject which reveal information relating to the past, current or future physical or mental health status of the data subject. This includes information about the natural person collected in the course of the registration for, or the provision of, health care services as referred to in Directive 2011/24/EU of the European Parliament and of the Council
to that natural person; a number, symbol or particular assigned to a natural person to uniquely identify the natural person for health purposes; information derived from the testing or examination of a body part or bodily substance, including from genetic data and biological samples; and any information on, for example, a disease, disability, disease risk, medical history, clinical treatment or the physiological or biomedical state of the data subject independent of its source, for example from a physician or other health professional, a hospital, a medical device or an in vitro diagnostic test.

[5] Cite as: GDPR, Recital 52 | type: recital
Derogating from the prohibition on processing special categories of personal data should also be allowed when provided for in Union or Member State law and subject to suitable safeguards, so as to protect personal data and other fundamental rights, where it is in the public interest to do so, in particular processing personal data in the field of employment law, social protection law including pensions and for health security, monitoring and alert purposes, the prevention or control of communicable diseases and other serious threats to health. Such a derogation may be made for health purposes, including public health and the management of health-care services, especially in order to ensure the quality and cost-effectiveness of the procedures used for settling claims for benefits and services in the health insurance system, or for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes. A derogation should also allow the processing of such personal data where necessary for the establishment, exercise or defence of legal claims, whether in court proceedings or in an administrative or out-of-court procedure.
```
</details>

---

## s21 (single)

**Question:** Do we have to explain to users how our recommendation feed decides what they see?

**Reference:** Yes. Online platforms using recommender systems must set out the main parameters in plain language in their terms and conditions, including the most significant criteria and their relative importance, and describe any options users have to modify or influence those parameters.

**Expected:** DSA, Article 27

**Answer:**

Yes, if your platform uses a recommender system to determine what users see, you must explain its main parameters to them (DSA, Article 27). 

Specifically, online platforms using recommender systems must:
* Set out the main parameters of their recommender systems in plain and intelligible language within their terms and conditions (DSA, Article 27).
* Explain why certain information is suggested, including the most significant criteria used to determine it and the reasons for their relative importance (DSA, Article 27).
* Inform users about any options they have to modify or influence those main parameters (DSA, Article 27).
* Provide an easily accessible functionality to let users select and modify their preferred option at any time, where multiple options are available for sorting or prioritizing information (DSA, Article 27).

According to Recital 70 of the DSA, explaining how information is prioritised helps users understand how recommender systems impact displayed content, including when information is prioritised based on profiling and online behavior (DSA, Recital 70).

Whether additional rules apply—such as providing a recommendation option not based on profiling—depends on whether your platform qualifies as a "very large online platform" (DSA, Article 38). Because this classification depends on your specific user numbers and facts, you should confirm with a lawyer before launch. The corpus does not cover subsequent changes or enforcement actions.

**Retrieved:** DSA, Article 27; DSA, Article 38; DSA, Recital 70; DSA, Recital 88; DSA, Recital 94

<details><summary>search: recommendation system transparency parameters DSA</summary>

```
[1] Cite as: DSA, Article 27 | type: article — Recommender system transparency
1. Providers of online platforms that use recommender systems shall set out in their terms and conditions, in plain and intelligible language, the main parameters used in their recommender systems, as well as any options for the recipients of the service to modify or influence those main parameters.
2. The main parameters referred to in paragraph 1 shall explain why certain information is suggested to the recipient of the service. They shall include, at least:
(a) the criteria which are most significant in determining the information suggested to the recipient of the service;
(b) the reasons for the relative importance of those parameters.
3. Where several options are available pursuant to paragraph 1 for recommender systems that determine the relative order of information presented to recipients of the service, providers of online platforms shall also make available a functionality that allows the recipient of the service to select and to modify at any time their preferred option. That functionality shall be directly and easily accessible from the specific section of the online platform’s online interface where the information is being prioritised.

[2] Cite as: DSA, Recital 70 | type: recital
A core part of the online platform’s business is the manner in which information is prioritised and presented on its online interface to facilitate and optimise access to information for the recipients of the service. This is done, for example, by algorithmically suggesting, ranking and prioritising information, distinguishing through text or other visual representations, or otherwise curating information provided by recipients. Such recommender systems can have a significant impact on the ability of recipients to retrieve and interact with information online, including to facilitate the search of relevant information for recipients of the service and contribute to an improved user experience. They also play an important role in the amplification of certain messages, the viral dissemination of information and the stimulation of online behaviour. Consequently, online platforms should consistently ensure that recipients of their service are appropriately informed about how recommender systems impact the way information is displayed, and can influence how information is presented to them. They should clearly present the parameters for such recommender systems in an easily comprehensible manner to ensure that the recipients of the service understand how information is prioritised for them. Those parameters should include at least the most important criteria in determining the information suggested to the recipient of the service and the reasons for their respective importance, including where information is prioritised based on profiling and their online behaviour.

[3] Cite as: DSA, Recital 94 | type: recital
The obligations on assessment and mitigation of risks should trigger, on a case-by-case basis, the need for providers of very large online platforms and of very large online search engines to assess and, where necessary, adjust the design of their recommender systems, for example by taking measures to prevent or minimise biases that lead to the discrimination of persons in vulnerable situations, in particular where such adjustment is in accordance with data protection law and when the information is personalised on the basis of special categories of personal data referred to in Article 9 of the Regulation (EU) 2016/679. In addition, and complementing the transparency obligations applicable to online platforms as regards their recommender systems, providers of very large online platforms and of very large online search engines should consistently ensure that recipients of their service enjoy alternative options which are not based on profiling, within the meaning of Regulation (EU) 2016/679, for the main parameters of their recommender systems. Such choices should be directly accessible from the online interface where the recommendations are presented.

[4] Cite as: DSA, Article 38 | type: article — Recommender systems
In addition to the requirements set out in Article 27, providers of very large online platforms and of very large online search engines that use recommender systems shall provide at least one option for each of their recommender systems which is not based on profiling as defined in Article 4, point (4), of Regulation (EU) 2016/679.

[5] Cite as: DSA, Recital 88 | type: recital
Providers of very large online platforms and of very large online search engines should also be diligent in the measures they take to test and, where necessary, adapt their algorithmic systems, not least their recommender systems. They may need to mitigate the negative effects of personalised recommendations and correct the criteria used in their recommendations. The advertising systems used by providers of very large online platforms and of very large online search engines can also be a catalyser for the systemic risks. Those providers should consider corrective measures, such as discontinuing advertising revenue for specific information, or other actions, such as improving the visibility of authoritative information sources, or more structurally adapting their advertising systems. Providers of very large online platforms and of very large online search engines may need to reinforce their internal processes or supervision of any of their activities, in particular as regards the detection of systemic risks, and conduct more frequent or targeted risk assessments related to new functionalities. In particular, where risks are shared across different online platforms or online search engines, they should cooperate with other service providers, including by initiating or joining existing codes of conduct or other self-regulatory measures. They should also consider awareness-raising actions, in particular where risks relate to disinformation campaigns.
```
</details>

---

## s22 (single)

**Question:** Does the AI Act cover simple rule-based software in our product, or only machine learning?

**Reference:** The definition of an AI system should not cover systems based on rules defined solely by natural persons to automatically execute operations. A key characteristic of AI systems is the capability to infer.

**Expected:** AI Act, Recital 12

**Answer:**

It depends on how the software operates, but the AI Act distinguishes AI from simpler traditional software by whether the system has the capability to *infer* outputs from inputs. 

According to Recital 12, the definition of an AI system is designed to be distinct from simpler traditional software systems or programming approaches and **should not cover systems that are based on the rules defined solely by natural persons to automatically execute operations** (AI Act, Recital 12). 

However, the AI Act does cover not only machine learning approaches that learn from data, but also **logic- and knowledge-based approaches** that infer from encoded knowledge or symbolic representations of the task (AI Act, Recital 12). 

Under Article 3, an AI system is defined as a machine-based system designed to operate with varying levels of autonomy that infers, from the input it receives, how to generate outputs like predictions, content, recommendations, or decisions that can influence physical or virtual environments (AI Act, Article 3(1)).

### Key takeaways for your product:
* **Purely manual rule systems:** If your software simply executes rigid, deterministic rules entirely authored by humans without an inference capability transcending basic data processing, it generally falls outside the AI Act's definition of an AI system (AI Act, Recital 12).
* **Logic- or knowledge-based reasoning:** If your rule-based system uses symbolic logic, knowledge graphs, or inference engines to derive new conclusions or handle complex reasoning autonomously, it may still meet the legal definition of an AI system.

Because classification depends heavily on the technical architecture and how the software generates its outputs, you should confirm with a lawyer whether your specific feature crosses the line from traditional programming into AI inference before launch.

**Retrieved:** AI Act, Article 3; AI Act, Article 6; AI Act, Recital 12; AI Act, Recital 26

<details><summary>search: AI system definition machine learning rule based AI Act</summary>

```
[1] Cite as: AI Act, Recital 12 | type: recital
The notion of ‘AI system’ in this Regulation should be clearly defined and should be closely aligned with the work of international organisations working on AI to ensure legal certainty, facilitate international convergence and wide acceptance, while providing the flexibility to accommodate the rapid technological developments in this field. Moreover, the definition should be based on key characteristics of AI systems that distinguish it from simpler traditional software systems or programming approaches and should not cover systems that are based on the rules defined solely by natural persons to automatically execute operations. A key characteristic of AI systems is their capability to infer. This capability to infer refers to the process of obtaining the outputs, such as predictions, content, recommendations, or decisions, which can influence physical and virtual environments, and to a capability of AI systems to derive models or algorithms, or both, from inputs or data. The techniques that enable inference while building an AI system include machine learning approaches that learn from data how to achieve certain objectives, and logic- and knowledge-based approaches that infer from encoded knowledge or symbolic representation of the task to be solved. The capacity of an AI system to infer transcends basic data processing by enabling learning, reasoning or modelling. The term ‘machine-based’ refers to the fact that AI systems run on machines. The reference to explicit or implicit objectives underscores that AI systems can operate according to explicit defined objectives or to implicit objectives. The objectives of the AI system may be different from the intended purpose of the AI system in a specific context. For the purposes of this Regulation, environments should be understood to be the contexts in which the AI systems operate, whereas outputs generated by the AI system reflect different functions performed by AI systems and include predictions, content, recommendations or decisions. AI systems are designed to operate with varying levels of autonomy, meaning that they have some degree of independence of actions from human involvement and of capabilities to operate without human intervention. The adaptiveness that an AI system could exhibit after deployment, refers to self-learning capabilities, allowing the system to change while in use. AI systems can be used on a stand-alone basis or as a component of a product, irrespective of whether the system is physically integrated into the product (embedded) or serves the functionality of the product without being integrated therein (non-embedded).

[2] Cite as: AI Act, Article 3 | type: article — Definitions (part 1 of 5)
For the purposes of this Regulation, the following definitions apply:
(1) ‘AI system’ means a machine-based system that is designed to operate with varying levels of autonomy and that may exhibit adaptiveness after deployment, and that, for explicit or implicit objectives, infers, from the input it receives, how to generate outputs such as predictions, content, recommendations, or decisions that can influence physical or virtual environments;
(2) ‘risk’ means the combination of the probability of an occurrence of harm and the severity of that harm;
(3) ‘provider’ means a natural or legal person, public authority, agency or other body that develops an AI system or a general-purpose AI model or that has an AI system or a general-purpose AI model developed and places it on the market or puts the AI system into service under its own name or trademark, whether for payment or free of charge;
(4) ‘deployer’ means a natural or legal person, public authority, agency or other body using an AI system under its authority except where the AI system is used in the course of a personal non-professional activity;
(5) ‘authorised representative’ means a natural or legal person located or established in the Union who has received and accepted a written mandate from a provider of an AI system or a general-purpose AI model to, respectively, perform and carry out on its behalf the obligations and procedures established by this Regulation;
(6) ‘importer’ means a natural or legal person located or established in the Union that places on the market an AI system that bears the name or trademark of a natural or legal person established in a third country;
(7) ‘distributor’ means a natural or legal person in the supply chain, other than the provider or the importer, that makes an AI system available on the Union market;
(8) ‘operator’ means a provider, product manufacturer, deployer, authorised representative, importer or distributor;
(9) ‘placing on the market’ means the first making available of an AI system or a general-purpose AI model on the Union market;
(10) ‘making available on the market’ means the supply of an AI system or a general-purpose AI model for distribution or use on the Union market in the course of a commercial activity, whether in return for payment or free of charge;
(11) ‘putting into service’ means the supply of an AI system for first use directly to the deployer or for own use in the Union for its intended purpose;
(12) ‘intended purpose’ means the use for which an AI system is intended by the provider, including the specific context and conditions of use, as specified in the information supplied by the provider in the instructions for use, promotional or sales materials and statements, as well as in the technical documentation;
(13) ‘reasonably foreseeable misuse’ means the use of an AI system in a way that is not in accordance with its intended purpose, but which may result from reasonably foreseeable human behaviour or interaction with other systems, including other AI systems;
(14) ‘safety component’ means a component of a product or of an AI system which fulfils a safety function for that product or AI system, or the failure or malfunctioning of which endangers the health and safety of persons or property;
(15) ‘instructions for use’ means the information provided by the provider to inform the deployer of, in particular, an AI system’s intended purpose and proper use;

[3] Cite as: AI Act, Article 6 | type: article — Classification rules for high-risk AI systems (part 1 of 2)
1. Irrespective of whether an AI system is placed on the market or put into service independently of the products referred to in points (a) and (b), that AI system shall be considered to be high-risk where both of the following conditions are fulfilled:
(a) the AI system is intended to be used as a safety component of a product, or the AI system is itself a product, covered by the Union harmonisation legislation listed in Annex I;
(b) the product whose safety component pursuant to point (a) is the AI system, or the AI system itself as a product, is required to undergo a third-party conformity assessment, with a view to the placing on the market or the putting into service of that product pursuant to the Union harmonisation legislation listed in Annex I.
2. In addition to the high-risk AI systems referred to in paragraph 1, AI systems referred to in Annex III shall be considered to be high-risk.
3. By derogation from paragraph 2, an AI system referred to in Annex III shall not be considered to be high-risk where it does not pose a significant risk of harm to the health, safety or fundamental rights of natural persons, including by not materially influencing the outcome of decision making.
The first subparagraph shall apply where any of the following conditions is fulfilled:
(a) the AI system is intended to perform a narrow procedural task;
(b) the AI system is intended to improve the result of a previously completed human activity;
(c) the AI system is intended to detect decision-making patterns or deviations from prior decision-making patterns and is not meant to replace or influence the previously completed human assessment, without proper human review; or
(d) the AI system is intended to perform a preparatory task to an assessment relevant for the purposes of the use cases listed in Annex III.
Notwithstanding the first subparagraph, an AI system referred to in Annex III shall always be considered to be high-risk where the AI system performs profiling of natural persons.
4. A provider who considers that an AI system referred to in Annex III is not high-risk shall document its assessment before that system is placed on the market or put into service. Such provider shall be subject to the registration obligation set out in Article 49(2). Upon request of national competent authorities, the provider shall provide the documentation of the assessment.
5. The Commission shall, after consulting the European Artificial Intelligence Board (the ‘Board’), and no later than 2 February 2026, provide guidelines specifying the practical implementation of this Article in line with Article 96 together with a comprehensive list of practical examples of use cases of AI systems that are high-risk and not high-risk.
6. The Commission is empowered to adopt delegated acts in accordance with Article 97 in order to amend paragraph 3, second subparagraph, of this Article by adding new conditions to those laid down therein, or by modifying them, where there is concrete and reliable evidence of the existence of AI systems that fall under the scope of Annex III, but do not pose a significant risk of harm to the health, safety or fundamental rights of natural persons.
7. The Commission shall adopt delegated acts in accordance with Article 97 in order to amend paragraph 3, second subparagraph, of this Article by deleting any of the conditions laid down therein, where there is concrete and reliable evidence that this is necessary to maintain the level of protection of health, safety and fundamental rights provided for by this Regulation.

[4] Cite as: AI Act, Article 3 | type: article — Definitions (part 5 of 5)
(63) ‘general-purpose AI model’ means an AI model, including where such an AI model is trained with a large amount of data using self-supervision at scale, that displays significant generality and is capable of competently performing a wide range of distinct tasks regardless of the way the model is placed on the market and that can be integrated into a variety of downstream systems or applications, except AI models that are used for research, development or prototyping activities before they are placed on the market;
(64) ‘high-impact capabilities’ means capabilities that match or exceed the capabilities recorded in the most advanced general-purpose AI models;
(65) ‘systemic risk’ means a risk that is specific to the high-impact capabilities of general-purpose AI models, having a significant impact on the Union market due to their reach, or due to actual or reasonably foreseeable negative effects on public health, safety, public security, fundamental rights, or the society as a whole, that can be propagated at scale across the value chain;
(66) ‘general-purpose AI system’ means an AI system which is based on a general-purpose AI model and which has the capability to serve a variety of purposes, both for direct use as well as for integration in other AI systems;
(67) ‘floating-point operation’ means any mathematical operation or assignment involving floating-point numbers, which are a subset of the real numbers typically represented on computers by an integer of fixed precision scaled by an integer exponent of a fixed base;
(68) ‘downstream provider’ means a provider of an AI system, including a general-purpose AI system, which integrates an AI model, regardless of whether the AI model is provided by themselves and vertically integrated or provided by another entity based on contractual relations.

[5] Cite as: AI Act, Recital 26 | type: recital
In order to introduce a proportionate and effective set of binding rules for AI systems, a clearly defined risk-based approach should be followed. That approach should tailor the type and content of such rules to the intensity and scope of the risks that AI systems can generate. It is therefore necessary to prohibit certain unacceptable AI practices, to lay down requirements for high-risk AI systems and obligations for the relevant operators, and to lay down transparency obligations for certain AI systems.
```
</details>

---

## s23 (single)

**Question:** Can we send marketing emails to existing customers based on legitimate interest instead of consent?

**Reference:** The GDPR says processing for direct marketing may be regarded as carried out for a legitimate interest, subject to the balancing test against the person's interests and reasonable expectations. Specific rules on marketing emails come from the ePrivacy framework, which is not in the corpus.

**Expected:** GDPR, Recital 47

**Answer:**

It depends, but generally yes under the GDPR, provided specific conditions are met. 

The corpus covers the following rules:
* **Legitimate interest can apply:** The GDPR states that processing personal data for direct marketing purposes may be regarded as carried out for a legitimate interest (GDPR, Recital 47). A relevant and appropriate relationship—such as where the data subject is a client—can create a legitimate interest, provided the data subjects have a reasonable expectation at the collection time that their data might be used this way (GDPR, Recital 47).
* **Balancing test required:** Processing is only lawful under legitimate interest if the controller's interests are not overridden by the fundamental rights and freedoms of the data subject (GDPR, Article 6(1)(f)).
* **Right to object:** Data subjects have the absolute right to object to direct marketing at any time and free of charge (GDPR, Article 21(2)). This right must be explicitly brought to their attention clearly and separately from other information at the latest at the time of the first communication (GDPR, Article 21(4); GDPR, Recital 70).

**What the corpus does not cover:** The corpus does not cover the ePrivacy Directive or national electronic communications laws, which often govern electronic marketing (such as whether an "opt-in" consent or an "opt-out" soft-opt-in is required specifically for emails). 

*Recommendation:* Because electronic marketing rules frequently depend on national implementations of the ePrivacy rules and the exact context of your customer relationship, confirm with a lawyer before launch.

**Retrieved:** GDPR, Article 21; GDPR, Article 6; GDPR, Recital 47; GDPR, Recital 49; GDPR, Recital 70

<details><summary>search: legitimate interest direct marketing existing customers GDPR</summary>

```
[1] Cite as: GDPR, Recital 47 | type: recital
The legitimate interests of a controller, including those of a controller to which the personal data may be disclosed, or of a third party, may provide a legal basis for processing, provided that the interests or the fundamental rights and freedoms of the data subject are not overriding, taking into consideration the reasonable expectations of data subjects based on their relationship with the controller. Such legitimate interest could exist for example where there is a relevant and appropriate relationship between the data subject and the controller in situations such as where the data subject is a client or in the service of the controller. At any rate the existence of a legitimate interest would need careful assessment including whether a data subject can reasonably expect at the time and in the context of the collection of the personal data that processing for that purpose may take place. The interests and fundamental rights of the data subject could in particular override the interest of the data controller where personal data are processed in circumstances where data subjects do not reasonably expect further processing. Given that it is for the legislator to provide by law for the legal basis for public authorities to process personal data, that legal basis should not apply to the processing by public authorities in the performance of their tasks. The processing of personal data strictly necessary for the purposes of preventing fraud also constitutes a legitimate interest of the data controller concerned. The processing of personal data for direct marketing purposes may be regarded as carried out for a legitimate interest.

[2] Cite as: GDPR, Recital 70 | type: recital
Where personal data are processed for the purposes of direct marketing, the data subject should have the right to object to such processing, including profiling to the extent that it is related to such direct marketing, whether with regard to initial or further processing, at any time and free of charge. That right should be explicitly brought to the attention of the data subject and presented clearly and separately from any other information.

[3] Cite as: GDPR, Article 6 | type: article — Lawfulness of processing (part 1 of 2)
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
The purpose of the processing shall be determined in that legal basis or, as regards the processing referred to in point (e) of paragraph 1, shall be necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller. That legal basis may contain specific provisions to adapt the application of rules of this Regulation, inter alia: the general conditions governing the lawfulness of processing by the controller; the types of data which are subject to the processing; the data subjects concerned; the entities to, and the purposes for which, the personal data may be disclosed; the purpose limitation; storage periods; and processing operations and processing procedures, including measures to ensure lawful and fair processing such as those for other specific processing situations as provided for in Chapter IX. The Union or the Member State law shall meet an objective of public interest and be proportionate to the legitimate aim pursued.
4. Where the processing for a purpose other than that for which the personal data have been collected is not based on the data subject's consent or on a Union or Member State law which constitutes a necessary and proportionate measure in a democratic society to safeguard the objectives referred to in Article 23(1), the controller shall, in order to ascertain whether processing for another purpose is compatible with the purpose for which the personal data are initially collected, take into account, inter alia:
(a) any link between the purposes for which the personal data have been collected and the purposes of the intended further processing;

[4] Cite as: GDPR, Recital 49 | type: recital
The processing of personal data to the extent strictly necessary and proportionate for the purposes of ensuring network and information security, i.e. the ability of a network or an information system to resist, at a given level of confidence, accidental events or unlawful or malicious actions that compromise the availability, authenticity, integrity and confidentiality of stored or transmitted personal data, and the security of the related services offered by, or accessible via, those networks and systems, by public authorities, by computer emergency response teams (CERTs), computer security incident response teams (CSIRTs), by providers of electronic communications networks and services and by providers of security technologies and services, constitutes a legitimate interest of the data controller concerned. This could, for example, include preventing unauthorised access to electronic communications networks and malicious code distribution and stopping ‘denial of service’ attacks and damage to computer and electronic communication systems.

[5] Cite as: GDPR, Article 21 | type: article — Right to object
1. The data subject shall have the right to object, on grounds relating to his or her particular situation, at any time to processing of personal data concerning him or her which is based on point (e) or (f) of Article 6(1), including profiling based on those provisions. The controller shall no longer process the personal data unless the controller demonstrates compelling legitimate grounds for the processing which override the interests, rights and freedoms of the data subject or for the establishment, exercise or defence of legal claims.
2. Where personal data are processed for direct marketing purposes, the data subject shall have the right to object at any time to processing of personal data concerning him or her for such marketing, which includes profiling to the extent that it is related to such direct marketing.
3. Where the data subject objects to processing for direct marketing purposes, the personal data shall no longer be processed for such purposes.
4. At the latest at the time of the first communication with the data subject, the right referred to in paragraphs 1 and 2 shall be explicitly brought to the attention of the data subject and shall be presented clearly and separately from any other information.
5. In the context of the use of information society services, and notwithstanding Directive 2002/58/EC, the data subject may exercise his or her right to object by automated means using technical specifications.
6. Where personal data are processed for scientific or historical research purposes or statistical purposes pursuant to Article 89(1), the data subject, on grounds relating to his or her particular situation, shall have the right to object to processing of personal data concerning him or her, unless the processing is necessary for the performance of a task carried out for reasons of public interest.
```
</details>

---

## m01 (multi)

**Question:** Our CV-screening tool is high-risk. What must it log, and does the GDPR limit fully automated rejection of candidates?

**Reference:** Under the AI Act, high-risk systems must technically allow automatic recording of events (logs) over their lifetime, to identify risk situations, support post-market monitoring and monitor operation. Under the GDPR, candidates have the right not to be subject to solely automated decisions with significant effects unless an exception applies (contract, law, explicit consent), with the right to human intervention and to contest the decision.

**Expected:** AI Act, Article 12; GDPR, Article 22

**Answer:**

Yes, the GDPR limits fully automated rejection, and the AI Act imposes specific logging requirements.

### 1. What a high-risk CV-screening tool must log
Under the AI Act, high-risk AI systems must technically allow for the automatic recording of events (logs) over the lifetime of the system to ensure appropriate traceability (AI Act, Article 12). Specifically for AI systems used for recruitment or selection of persons—and for evaluating persons for terms of work relationships (falling under Annex III, point 1(a))—the logging capabilities must record at a minimum:
* The period of each use of the system, including the start date, start time, end date, and end time for each use (AI Act, Article 12).
* The reference database against which input data has been checked by the system (AI Act, Article 12).
* The input data for which the search has led to a match (AI Act, Article 12).
* The identification of the natural persons involved in the verification of the results, where human oversight is applied (AI Act, Article 12).

Providers must keep these automatically generated logs under their control for a period appropriate to the intended purpose, of at least six months, unless other Union or national law (such as data protection rules) provides otherwise (AI Act, Article 19).

### 2. Does the GDPR limit fully automated rejection?
**Yes.** Under the GDPR, candidates generally have the right not to be subject to a decision based *solely* on automated processing—including profiling—that produces legal effects or similarly significantly affects them (GDPR, Article 22(1)). Recital 71 explicitly cites "e-recruiting practices without any human intervention" as an example of such prohibited fully automated decisions.

However, fully automated rejection *can* be permitted if an exception applies, such as when it is necessary for entering into a contract, authorised by law, or based on the candidate's explicit consent (GDPR, Article 22(2)). Even when an exception applies, you must implement suitable safeguards, including at least the candidate's right to obtain human intervention on the part of the controller, to express their point of view, and to contest the decision (GDPR, Article 22(3); GDPR, Recital 71).

*Because compliance depends heavily on your legal basis, system architecture, and workflows, confirm these setup choices with a lawyer before launch.*

**Retrieved:** AI Act, Article 12; AI Act, Article 16; AI Act, Article 19; AI Act, Recital 131; AI Act, Recital 71; GDPR, Article 21; GDPR, Article 22; GDPR, Recital 71; GDPR, Recital 72; GDPR, Recital 75

<details><summary>search: high risk AI systems logging capabilities recording events AI Act</summary>

```
[1] Cite as: AI Act, Article 12 | type: article — Record-keeping
1. High-risk AI systems shall technically allow for the automatic recording of events (logs) over the lifetime of the system.
2. In order to ensure a level of traceability of the functioning of a high-risk AI system that is appropriate to the intended purpose of the system, logging capabilities shall enable the recording of events relevant for:
(a) identifying situations that may result in the high-risk AI system presenting a risk within the meaning of Article 79(1) or in a substantial modification;
(b) facilitating the post-market monitoring referred to in Article 72; and
(c) monitoring the operation of high-risk AI systems referred to in Article 26(5).
3. For high-risk AI systems referred to in point 1 (a), of Annex III, the logging capabilities shall provide, at a minimum:
(a) recording of the period of each use of the system (start date and time and end date and time of each use);
(b) the reference database against which input data has been checked by the system;
(c) the input data for which the search has led to a match;
(d) the identification of the natural persons involved in the verification of the results, as referred to in Article 14(5).

[2] Cite as: AI Act, Recital 71 | type: recital
Having comprehensible information on how high-risk AI systems have been developed and how they perform throughout their lifetime is essential to enable traceability of those systems, verify compliance with the requirements under this Regulation, as well as monitoring of their operations and post market monitoring. This requires keeping records and the availability of technical documentation, containing information which is necessary to assess the compliance of the AI system with the relevant requirements and facilitate post market monitoring. Such information should include the general characteristics, capabilities and limitations of the system, algorithms, data, training, testing and validation processes used as well as documentation on the relevant risk-management system and drawn in a clear and comprehensive form. The technical documentation should be kept up to date, appropriately throughout the lifetime of the AI system. Furthermore, high-risk AI systems should technically allow for the automatic recording of events, by means of logs, over the duration of the lifetime of the system.

[3] Cite as: AI Act, Article 19 | type: article — Automatically generated logs
1. Providers of high-risk AI systems shall keep the logs referred to in Article 12(1), automatically generated by their high-risk AI systems, to the extent such logs are under their control. Without prejudice to applicable Union or national law, the logs shall be kept for a period appropriate to the intended purpose of the high-risk AI system, of at least six months, unless provided otherwise in the applicable Union or national law, in particular in Union law on the protection of personal data.
2. Providers that are financial institutions subject to requirements regarding their internal governance, arrangements or processes under Union financial services law shall maintain the logs automatically generated by their high-risk AI systems as part of the documentation kept under the relevant financial services law.

[4] Cite as: AI Act, Article 16 | type: article — Obligations of providers of high-risk AI systems
Providers of high-risk AI systems shall:
(a) ensure that their high-risk AI systems are compliant with the requirements set out in Section 2;
(b) indicate on the high-risk AI system or, where that is not possible, on its packaging or its accompanying documentation, as applicable, their name, registered trade name or registered trade mark, the address at which they can be contacted;
(c) have a quality management system in place which complies with Article 17;
(d) keep the documentation referred to in Article 18;
(e) when under their control, keep the logs automatically generated by their high-risk AI systems as referred to in Article 19;
(f) ensure that the high-risk AI system undergoes the relevant conformity assessment procedure as referred to in Article 43, prior to its being placed on the market or put into service;
(g) draw up an EU declaration of conformity in accordance with Article 47;
(h) affix the CE marking to the high-risk AI system or, where that is not possible, on its packaging or its accompanying documentation, to indicate conformity with this Regulation, in accordance with Article 48;
(i) comply with the registration obligations referred to in Article 49(1);
(j) take the necessary corrective actions and provide information as required in Article 20;
(k) upon a reasoned request of a national competent authority, demonstrate the conformity of the high-risk AI system with the requirements set out in Section 2;
(l) ensure that the high-risk AI system complies with accessibility requirements in accordance with Directives (EU) 2016/2102 and (EU) 2019/882.

[5] Cite as: AI Act, Recital 131 | type: recital
In order to facilitate the work of the Commission and the Member States in the AI field as well as to increase the transparency towards the public, providers of high-risk AI systems other than those related to products falling within the scope of relevant existing Union harmonisation legislation, as well as providers who consider that an AI system listed in the high-risk use cases in an annex to this Regulation is not high-risk on the basis of a derogation, should be required to register themselves and information about their AI system in an EU database, to be established and managed by the Commission. Before using an AI system listed in the high-risk use cases in an annex to this Regulation, deployers of high-risk AI systems that are public authorities, agencies or bodies, should register themselves in such database and select the system that they envisage to use. Other deployers should be entitled to do so voluntarily. This section of the EU database should be publicly accessible, free of charge, the information should be easily navigable, understandable and machine-readable. The EU database should also be user-friendly, for example by providing search functionalities, including through keywords, allowing the general public to find relevant information to be submitted upon the registration of high-risk AI systems and on the use case of high-risk AI systems, set out in an annex to this Regulation, to which the high-risk AI systems correspond. Any substantial modification of high-risk AI systems should also be registered in the EU database. For high-risk AI systems in the area of law enforcement, migration, asylum and border control management, the registration obligations should be fulfilled in a secure non-public section of the EU database. Access to the secure non-public section should be strictly limited to the Commission as well as to market surveillance authorities with regard to their national section of that database. High-risk AI systems in the area of critical infrastructure should only be registered at national level. The Commission should be the controller of the EU database, in accordance with Regulation (EU) 2018/1725. In order to ensure the full functionality of the EU database, when deployed, the procedure for setting the database should include the development of functional specifications by the Commission and an independent audit report. The Commission should take into account cybersecurity risks when carrying out its tasks as data controller on the EU database. In order to maximise the availability and use of the EU database by the public, the EU database, including the information made available through it, should comply with requirements under the Directive (EU) 2019/882.
```
</details>

<details><summary>search: automated decision making profiling GDPR article 22 candidate rejection CV screening</summary>

```
[1] Cite as: GDPR, Article 22 | type: article — Automated individual decision-making, including profiling
1. The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her.
2. Paragraph 1 shall not apply if the decision:
(a) is necessary for entering into, or performance of, a contract between the data subject and a data controller;
(b) is authorised by Union or Member State law to which the controller is subject and which also lays down suitable measures to safeguard the data subject's rights and freedoms and legitimate interests; or
(c) is based on the data subject's explicit consent.
3. In the cases referred to in points (a) and (c) of paragraph 2, the data controller shall implement suitable measures to safeguard the data subject's rights and freedoms and legitimate interests, at least the right to obtain human intervention on the part of the controller, to express his or her point of view and to contest the decision.
4. Decisions referred to in paragraph 2 shall not be based on special categories of personal data referred to in Article 9(1), unless point (a) or (g) of Article 9(2) applies and suitable measures to safeguard the data subject's rights and freedoms and legitimate interests are in place.

[2] Cite as: GDPR, Recital 71 | type: recital
The data subject should have the right not to be subject to a decision, which may include a measure, evaluating personal aspects relating to him or her which is based solely on automated processing and which produces legal effects concerning him or her or similarly significantly affects him or her, such as automatic refusal of an online credit application or e-recruiting practices without any human intervention. Such processing includes ‘profiling’ that consists of any form of automated processing of personal data evaluating the personal aspects relating to a natural person, in particular to analyse or predict aspects concerning the data subject's performance at work, economic situation, health, personal preferences or interests, reliability or behaviour, location or movements, where it produces legal effects concerning him or her or similarly significantly affects him or her. However, decision-making based on such processing, including profiling, should be allowed where expressly authorised by Union or Member State law to which the controller is subject, including for fraud and tax-evasion monitoring and prevention purposes conducted in accordance with the regulations, standards and recommendations of Union institutions or national oversight bodies and to ensure the security and reliability of a service provided by the controller, or necessary for the entering or performance of a contract between the data subject and a controller, or when the data subject has given his or her explicit consent. In any case, such processing should be subject to suitable safeguards, which should include specific information to the data subject and the right to obtain human intervention, to express his or her point of view, to obtain an explanation of the decision reached after such assessment and to challenge the decision. Such measure should not concern a child.
In order to ensure fair and transparent processing in respect of the data subject, taking into account the specific circumstances and context in which the personal data are processed, the controller should use appropriate mathematical or statistical procedures for the profiling, implement technical and organisational measures appropriate to ensure, in particular, that factors which result in inaccuracies in personal data are corrected and the risk of errors is minimised, secure personal data in a manner that takes account of the potential risks involved for the interests and rights of the data subject and that prevents, inter alia, discriminatory effects on natural persons on the basis of racial or ethnic origin, political opinion, religion or beliefs, trade union membership, genetic or health status or sexual orientation, or that result in measures having such an effect. Automated decision-making and profiling based on special categories of personal data should be allowed only under specific conditions.

[3] Cite as: GDPR, Recital 72 | type: recital
Profiling is subject to the rules of this Regulation governing the processing of personal data, such as the legal grounds for processing or data protection principles. The European Data Protection Board established by this Regulation (the ‘Board’) should be able to issue guidance in that context.

[4] Cite as: GDPR, Recital 75 | type: recital
The risk to the rights and freedoms of natural persons, of varying likelihood and severity, may result from personal data processing which could lead to physical, material or non-material damage, in particular: where the processing may give rise to discrimination, identity theft or fraud, financial loss, damage to the reputation, loss of confidentiality of personal data protected by professional secrecy, unauthorised reversal of pseudonymisation, or any other significant economic or social disadvantage; where data subjects might be deprived of their rights and freedoms or prevented from exercising control over their personal data; where personal data are processed which reveal racial or ethnic origin, political opinions, religion or philosophical beliefs, trade union membership, and the processing of genetic data, data concerning health or data concerning sex life or criminal convictions and offences or related security measures; where personal aspects are evaluated, in particular analysing or predicting aspects concerning performance at work, economic situation, health, personal preferences or interests, reliability or behaviour, location or movements, in order to create or use personal profiles; where personal data of vulnerable natural persons, in particular of children, are processed; or where processing involves a large amount of personal data and affects a large number of data subjects.

[5] Cite as: GDPR, Article 21 | type: article — Right to object
1. The data subject shall have the right to object, on grounds relating to his or her particular situation, at any time to processing of personal data concerning him or her which is based on point (e) or (f) of Article 6(1), including profiling based on those provisions. The controller shall no longer process the personal data unless the controller demonstrates compelling legitimate grounds for the processing which override the interests, rights and freedoms of the data subject or for the establishment, exercise or defence of legal claims.
2. Where personal data are processed for direct marketing purposes, the data subject shall have the right to object at any time to processing of personal data concerning him or her for such marketing, which includes profiling to the extent that it is related to such direct marketing.
3. Where the data subject objects to processing for direct marketing purposes, the personal data shall no longer be processed for such purposes.
4. At the latest at the time of the first communication with the data subject, the right referred to in paragraphs 1 and 2 shall be explicitly brought to the attention of the data subject and shall be presented clearly and separately from any other information.
5. In the context of the use of information society services, and notwithstanding Directive 2002/58/EC, the data subject may exercise his or her right to object by automated means using technical specifications.
6. Where personal data are processed for scientific or historical research purposes or statistical purposes pursuant to Article 89(1), the data subject, on grounds relating to his or her particular situation, shall have the right to object to processing of personal data concerning him or her, unless the processing is necessary for the performance of a task carried out for reasons of public interest.
```
</details>

---

## m02 (multi)

**Question:** We're launching a chatbot that collects users' names and emails. What do we have to tell users about the AI and about their data?

**Reference:** Under the AI Act, users must be informed they are interacting with an AI system unless it is obvious. Under the GDPR, when collecting personal data you must provide your identity and contact details, DPO contact if any, purposes and legal basis, recipients, any international transfers, retention period, and the person's rights.

**Expected:** AI Act, Article 50; GDPR, Article 13

**Answer:**

**It depends** on whether it is obvious to the users that they are interacting with an AI (rather than a human) (AI Act, Article 50(1)). 

### 1. What to tell users about the AI
* **AI Interaction Notice:** Under the AI Act, you must inform users at the latest at the time of the first interaction that they are interacting with an AI system, presented in a clear and distinguishable manner, unless this is obvious from the point of view of a reasonably well-informed, observant, and circumspect person in that context (AI Act, Article 50(1), Article 50(5)). 

### 2. What to tell users about their data (Names and Emails)
Under the GDPR, when you collect personal data directly from users (such as names and emails), you must provide them with the following information at the time of collection (GDPR, Article 13(1), Article 13(2)):
* Your identity and contact details (and those of your DPO, if applicable) (GDPR, Article 13(1)).
* The purposes of the processing and the legal basis for it (GDPR, Article 13(1)).
* The recipients or categories of recipients of the data, if any (GDPR, Article 13(1)).
* Whether data will be transferred outside the EU, and what safeguards apply (GDPR, Article 13(1)).
* How long the data will be stored, or the criteria used to determine that period (GDPR, Article 13(2)).
* Users' data rights (access, rectification, erasure, restriction, objection, and data portability), and how to withdraw consent if consent is your legal basis (GDPR, Article 13(2)).
* The right to lodge a complaint with a supervisory authority (GDPR, Article 13(2)).
* Whether providing the data is a statutory or contractual requirement, and the consequences of failing to provide it (GDPR, Article 13(2)).
* Information on any automated decision-making or profiling, including meaningful information about the logic involved and the consequences (GDPR, Article 13(2)).

*Note:* This information must be provided in concise, easily accessible, clear, and plain language (GDPR, Recital 39, Recital 58). Because these requirements depend on your exact legal basis, data retention plans, and system architecture, confirm your notices with a lawyer before launch.

**Retrieved:** AI Act, Article 13; AI Act, Article 50; AI Act, Recital 119; AI Act, Recital 132; AI Act, Recital 137; GDPR, Article 13; GDPR, Recital 39; GDPR, Recital 58; GDPR, Recital 60; GDPR, Recital 61

<details><summary>search: chatbot transparency AI Act AI system users informed</summary>

```
[1] Cite as: AI Act, Recital 132 | type: recital
Certain AI systems intended to interact with natural persons or to generate content may pose specific risks of impersonation or deception irrespective of whether they qualify as high-risk or not. In certain circumstances, the use of these systems should therefore be subject to specific transparency obligations without prejudice to the requirements and obligations for high-risk AI systems and subject to targeted exceptions to take into account the special need of law enforcement. In particular, natural persons should be notified that they are interacting with an AI system, unless this is obvious from the point of view of a natural person who is reasonably well-informed, observant and circumspect taking into account the circumstances and the context of use. When implementing that obligation, the characteristics of natural persons belonging to vulnerable groups due to their age or disability should be taken into account to the extent the AI system is intended to interact with those groups as well. Moreover, natural persons should be notified when they are exposed to AI systems that, by processing their biometric data, can identify or infer the emotions or intentions of those persons or assign them to specific categories. Such specific categories can relate to aspects such as sex, age, hair colour, eye colour, tattoos, personal traits, ethnic origin, personal preferences and interests. Such information and notifications should be provided in accessible formats for persons with disabilities.

[2] Cite as: AI Act, Article 50 | type: article — Transparency obligations for providers and deployers of certain AI systems (part 1 of 2)
1. Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system, unless this is obvious from the point of view of a natural person who is reasonably well-informed, observant and circumspect, taking into account the circumstances and the context of use. This obligation shall not apply to AI systems authorised by law to detect, prevent, investigate or prosecute criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, unless those systems are available for the public to report a criminal offence.
2. Providers of AI systems, including general-purpose AI systems, generating synthetic audio, image, video or text content, shall ensure that the outputs of the AI system are marked in a machine-readable format and detectable as artificially generated or manipulated. Providers shall ensure their technical solutions are effective, interoperable, robust and reliable as far as this is technically feasible, taking into account the specificities and limitations of various types of content, the costs of implementation and the generally acknowledged state of the art, as may be reflected in relevant technical standards. This obligation shall not apply to the extent the AI systems perform an assistive function for standard editing or do not substantially alter the input data provided by the deployer or the semantics thereof, or where authorised by law to detect, prevent, investigate or prosecute criminal offences.
3. Deployers of an emotion recognition system or a biometric categorisation system shall inform the natural persons exposed thereto of the operation of the system, and shall process the personal data in accordance with Regulations (EU) 2016/679 and (EU) 2018/1725 and Directive (EU) 2016/680, as applicable. This obligation shall not apply to AI systems used for biometric categorisation and emotion recognition, which are permitted by law to detect, prevent or investigate criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, and in accordance with Union law.
4. Deployers of an AI system that generates or manipulates image, audio or video content constituting a deep fake, shall disclose that the content has been artificially generated or manipulated. This obligation shall not apply where the use is authorised by law to detect, prevent, investigate or prosecute criminal offence. Where the content forms part of an evidently artistic, creative, satirical, fictional or analogous work or programme, the transparency obligations set out in this paragraph are limited to disclosure of the existence of such generated or manipulated content in an appropriate manner that does not hamper the display or enjoyment of the work.
Deployers of an AI system that generates or manipulates text which is published with the purpose of informing the public on matters of public interest shall disclose that the text has been artificially generated or manipulated. This obligation shall not apply where the use is authorised by law to detect, prevent, investigate or prosecute criminal offences or where the AI-generated content has undergone a process of human review or editorial control and where a natural or legal person holds editorial responsibility for the publication of the content.
5. The information referred to in paragraphs 1 to 4 shall be provided to the natural persons concerned in a clear and distinguishable manner at the latest at the time of the first interaction or exposure. The information shall conform to the applicable accessibility requirements.

[3] Cite as: AI Act, Recital 137 | type: recital
Compliance with the transparency obligations for the AI systems covered by this Regulation should not be interpreted as indicating that the use of the AI system or its output is lawful under this Regulation or other Union and Member State law and should be without prejudice to other transparency obligations for deployers of AI systems laid down in Union or national law.

[4] Cite as: AI Act, Recital 119 | type: recital
Considering the quick pace of innovation and the technological evolution of digital services in scope of different instruments of Union law in particular having in mind the usage and the perception of their recipients, the AI systems subject to this Regulation may be provided as intermediary services or parts thereof within the meaning of Regulation (EU) 2022/2065, which should be interpreted in a technology-neutral manner. For example, AI systems may be used to provide online search engines, in particular, to the extent that an AI system such as an online chatbot performs searches of, in principle, all websites, then incorporates the results into its existing knowledge and uses the updated knowledge to generate a single output that combines different sources of information.

[5] Cite as: AI Act, Article 13 | type: article — Transparency and provision of information to deployers
1. High-risk AI systems shall be designed and developed in such a way as to ensure that their operation is sufficiently transparent to enable deployers to interpret a system’s output and use it appropriately. An appropriate type and degree of transparency shall be ensured with a view to achieving compliance with the relevant obligations of the provider and deployer set out in Section 3.
2. High-risk AI systems shall be accompanied by instructions for use in an appropriate digital format or otherwise that include concise, complete, correct and clear information that is relevant, accessible and comprehensible to deployers.
3. The instructions for use shall contain at least the following information:
(a) the identity and the contact details of the provider and, where applicable, of its authorised representative;
(b) the characteristics, capabilities and limitations of performance of the high-risk AI system, including:
(i) its intended purpose;
(ii) the level of accuracy, including its metrics, robustness and cybersecurity referred to in Article 15 against which the high-risk AI system has been tested and validated and which can be expected, and any known and foreseeable circumstances that may have an impact on that expected level of accuracy, robustness and cybersecurity;
(iii) any known or foreseeable circumstance, related to the use of the high-risk AI system in accordance with its intended purpose or under conditions of reasonably foreseeable misuse, which may lead to risks to the health and safety or fundamental rights referred to in Article 9(2);
(iv) where applicable, the technical capabilities and characteristics of the high-risk AI system to provide information that is relevant to explain its output;
(v) when appropriate, its performance regarding specific persons or groups of persons on which the system is intended to be used;
(vi) when appropriate, specifications for the input data, or any other relevant information in terms of the training, validation and testing data sets used, taking into account the intended purpose of the high-risk AI system;
(vii) where applicable, information to enable deployers to interpret the output of the high-risk AI system and use it appropriately;
(c) the changes to the high-risk AI system and its performance which have been pre-determined by the provider at the moment of the initial conformity assessment, if any;
(d) the human oversight measures referred to in Article 14, including the technical measures put in place to facilitate the interpretation of the outputs of the high-risk AI systems by the deployers;
(e) the computational and hardware resources needed, the expected lifetime of the high-risk AI system and any necessary maintenance and care measures, including their frequency, to ensure the proper functioning of that AI system, including as regards software updates;
(f) where relevant, a description of the mechanisms included within the high-risk AI system that allows deployers to properly collect, store and interpret the logs in accordance with Article 12.
```
</details>

<details><summary>search: GDPR personal data collection information to users transparency rights</summary>

```
[1] Cite as: GDPR, Article 13 | type: article — Information to be provided where personal data are collected from the data subject
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
(d) the right to lodge a complaint with a supervisory authority;
(e) whether the provision of personal data is a statutory or contractual requirement, or a requirement necessary to enter into a contract, as well as whether the data subject is obliged to provide the personal data and of the possible consequences of failure to provide such data;
(f) the existence of automated decision-making, including profiling, referred to in Article 22(1) and (4) and, at least in those cases, meaningful information about the logic involved, as well as the significance and the envisaged consequences of such processing for the data subject.
3. Where the controller intends to further process the personal data for a purpose other than that for which the personal data were collected, the controller shall provide the data subject prior to that further processing with information on that other purpose and with any relevant further information as referred to in paragraph 2.
4. Paragraphs 1, 2 and 3 shall not apply where and insofar as the data subject already has the information.

[2] Cite as: GDPR, Recital 39 | type: recital
Any processing of personal data should be lawful and fair. It should be transparent to natural persons that personal data concerning them are collected, used, consulted or otherwise processed and to what extent the personal data are or will be processed. The principle of transparency requires that any information and communication relating to the processing of those personal data be easily accessible and easy to understand, and that clear and plain language be used. That principle concerns, in particular, information to the data subjects on the identity of the controller and the purposes of the processing and further information to ensure fair and transparent processing in respect of the natural persons concerned and their right to obtain confirmation and communication of personal data concerning them which are being processed. Natural persons should be made aware of risks, rules, safeguards and rights in relation to the processing of personal data and how to exercise their rights in relation to such processing. In particular, the specific purposes for which personal data are processed should be explicit and legitimate and determined at the time of the collection of the personal data. The personal data should be adequate, relevant and limited to what is necessary for the purposes for which they are processed. This requires, in particular, ensuring that the period for which the personal data are stored is limited to a strict minimum. Personal data should be processed only if the purpose of the processing could not reasonably be fulfilled by other means. In order to ensure that the personal data are not kept longer than necessary, time limits should be established by the controller for erasure or for a periodic review. Every reasonable step should be taken to ensure that personal data which are inaccurate are rectified or deleted. Personal data should be processed in a manner that ensures appropriate security and confidentiality of the personal data, including for preventing unauthorised access to or use of personal data and the equipment used for the processing.

[3] Cite as: GDPR, Recital 61 | type: recital
The information in relation to the processing of personal data relating to the data subject should be given to him or her at the time of collection from the data subject, or, where the personal data are obtained from another source, within a reasonable period, depending on the circumstances of the case. Where personal data can be legitimately disclosed to another recipient, the data subject should be informed when the personal data are first disclosed to the recipient. Where the controller intends to process the personal data for a purpose other than that for which they were collected, the controller should provide the data subject prior to that further processing with information on that other purpose and other necessary information. Where the origin of the personal data cannot be provided to the data subject because various sources have been used, general information should be provided.

[4] Cite as: GDPR, Recital 58 | type: recital
The principle of transparency requires that any information addressed to the public or to the data subject be concise, easily accessible and easy to understand, and that clear and plain language and, additionally, where appropriate, visualisation be used. Such information could be provided in electronic form, for example, when addressed to the public, through a website. This is of particular relevance in situations where the proliferation of actors and the technological complexity of practice make it difficult for the data subject to know and understand whether, by whom and for what purpose personal data relating to him or her are being collected, such as in the case of online advertising. Given that children merit specific protection, any information and communication, where processing is addressed to a child, should be in such a clear and plain language that the child can easily understand.

[5] Cite as: GDPR, Recital 60 | type: recital
The principles of fair and transparent processing require that the data subject be informed of the existence of the processing operation and its purposes. The controller should provide the data subject with any further information necessary to ensure fair and transparent processing taking into account the specific circumstances and context in which the personal data are processed. Furthermore, the data subject should be informed of the existence of profiling and the consequences of such profiling. Where the personal data are collected from the data subject, the data subject should also be informed whether he or she is obliged to provide the personal data and of the consequences, where he or she does not provide such data. That information may be provided in combination with standardised icons in order to give in an easily visible, intelligible and clearly legible manner, a meaningful overview of the intended processing. Where the icons are presented electronically, they should be machine-readable.
```
</details>

---

## m03 (multi)

**Question:** We use a vendor's AI credit-scoring tool. Do we need a fundamental-rights impact assessment, a data protection impact assessment, or both?

**Reference:** Likely both. Deployers of high-risk AI used to evaluate creditworthiness (Annex III point 5(b)) must carry out a fundamental-rights impact assessment before first use. The GDPR requires a DPIA where processing is likely to result in a high risk, in particular systematic and extensive automated evaluation, including profiling, with legal or similarly significant effects. Where a DPIA has been done, the FRIA complements it.

**Expected:** AI Act, Article 27; GDPR, Article 35

**Answer:**

It depends on your organization's role and legal status, but you may need **both** a Data Protection Impact Assessment (DPIA) under the GDPR and a Fundamental Rights Impact Assessment (FRIA) under the AI Act. 

Here is how the two assessments apply to an AI credit-scoring tool:

### 1. Data Protection Impact Assessment (DPIA) — GDPR
* **Is it required?** Usually yes. Under the GDPR, a DPIA is specifically required for a "systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person" (GDPR, Article 35(3)(a)). 
* Because a credit-scoring tool evaluates personal aspects through profiling to make decisions that significantly affect individuals (e.g., granting financial resources or housing), it typically triggers the requirement for a DPIA prior to processing (GDPR, Article 35(1)).

### 2. Fundamental Rights Impact Assessment (FRIA) — AI Act
* **Is it required?** It depends on who you are and how you use the tool. AI systems that evaluate the credit score or creditworthiness of natural persons are classified as high-risk AI systems (AI Act, Recital 58). 
* However, the obligation to perform a FRIA prior to deployment falls specifically on deployers that are **bodies governed by public law**, **private entities providing public services**, or deployers of specific high-risk categories listed in Annex III (such as certain banking and insurance entities) (AI Act, Article 27(1), AI Act, Recital 96). 
* If your startup is a standard private commercial business (e.g., a fintech or marketplace) using a vendor's credit-scoring tool rather than acting as a public authority or private entity providing public services or covered financial entity, check carefully whether your specific use-case falls under the deployer obligations in Article 27. 

### How they interact
If you are required to do both, the AI Act notes that if your obligations for a FRIA are already met through a GDPR DPIA, the FRIA can simply complement that existing DPIA rather than duplicating it entirely (AI Act, Article 27(4)).

*Because classification as a high-risk deployer and the exact triggers for a DPIA depend heavily on your specific sector, status, and processing setup, you should confirm these requirements with a lawyer before launch.*

**Retrieved:** AI Act, Article 27; AI Act, Recital 31; AI Act, Recital 48; AI Act, Recital 58; AI Act, Recital 96; GDPR, Article 35; GDPR, Article 36; GDPR, Recital 84; GDPR, Recital 90

<details><summary>search: credit scoring fundamental rights impact assessment AI Act</summary>

```
[1] Cite as: AI Act, Recital 58 | type: recital
Another area in which the use of AI systems deserves special consideration is the access to and enjoyment of certain essential private and public services and benefits necessary for people to fully participate in society or to improve one’s standard of living. In particular, natural persons applying for or receiving essential public assistance benefits and services from public authorities namely healthcare services, social security benefits, social services providing protection in cases such as maternity, illness, industrial accidents, dependency or old age and loss of employment and social and housing assistance, are typically dependent on those benefits and services and in a vulnerable position in relation to the responsible authorities. If AI systems are used for determining whether such benefits and services should be granted, denied, reduced, revoked or reclaimed by authorities, including whether beneficiaries are legitimately entitled to such benefits or services, those systems may have a significant impact on persons’ livelihood and may infringe their fundamental rights, such as the right to social protection, non-discrimination, human dignity or an effective remedy and should therefore be classified as high-risk. Nonetheless, this Regulation should not hamper the development and use of innovative approaches in the public administration, which would stand to benefit from a wider use of compliant and safe AI systems, provided that those systems do not entail a high risk to legal and natural persons. In addition, AI systems used to evaluate the credit score or creditworthiness of natural persons should be classified as high-risk AI systems, since they determine those persons’ access to financial resources or essential services such as housing, electricity, and telecommunication services. AI systems used for those purposes may lead to discrimination between persons or groups and may perpetuate historical patterns of discrimination, such as that based on racial or ethnic origins, gender, disabilities, age or sexual orientation, or may create new forms of discriminatory impacts. However, AI systems provided for by Union law for the purpose of detecting fraud in the offering of financial services and for prudential purposes to calculate credit institutions’ and insurance undertakings’ capital requirements should not be considered to be high-risk under this Regulation. Moreover, AI systems intended to be used for risk assessment and pricing in relation to natural persons for health and life insurance can also have a significant impact on persons’ livelihood and if not duly designed, developed and used, can infringe their fundamental rights and can lead to serious consequences for people’s life and health, including financial exclusion and discrimination. Finally, AI systems used to evaluate and classify emergency calls by natural persons or to dispatch or establish priority in the dispatching of emergency first response services, including by police, firefighters and medical aid, as well as of emergency healthcare patient triage systems, should also be classified as high-risk since they make decisions in very critical situations for the life and health of persons and their property.

[2] Cite as: AI Act, Recital 96 | type: recital
In order to efficiently ensure that fundamental rights are protected, deployers of high-risk AI systems that are bodies governed by public law, or private entities providing public services and deployers of certain high-risk AI systems listed in an annex to this Regulation, such as banking or insurance entities, should carry out a fundamental rights impact assessment prior to putting it into use. Services important for individuals that are of public nature may also be provided by private entities. Private entities providing such public services are linked to tasks in the public interest such as in the areas of education, healthcare, social services, housing, administration of justice. The aim of the fundamental rights impact assessment is for the deployer to identify the specific risks to the rights of individuals or groups of individuals likely to be affected, identify measures to be taken in the case of a materialisation of those risks. The impact assessment should be performed prior to deploying the high-risk AI system, and should be updated when the deployer considers that any of the relevant factors have changed. The impact assessment should identify the deployer’s relevant processes in which the high-risk AI system will be used in line with its intended purpose, and should include a description of the period of time and frequency in which the system is intended to be used as well as of specific categories of natural persons and groups who are likely to be affected in the specific context of use. The assessment should also include the identification of specific risks of harm likely to have an impact on the fundamental rights of those persons or groups. While performing this assessment, the deployer should take into account information relevant to a proper assessment of the impact, including but not limited to the information given by the provider of the high-risk AI system in the instructions for use. In light of the risks identified, deployers should determine measures to be taken in the case of a materialisation of those risks, including for example governance arrangements in that specific context of use, such as arrangements for human oversight according to the instructions of use or, complaint handling and redress procedures, as they could be instrumental in mitigating risks to fundamental rights in concrete use-cases. After performing that impact assessment, the deployer should notify the relevant market surveillance authority. Where appropriate, to collect relevant information necessary to perform the impact assessment, deployers of high-risk AI system, in particular when AI systems are used in the public sector, could involve relevant stakeholders, including the representatives of groups of persons likely to be affected by the AI system, independent experts, and civil society organisations in conducting such impact assessments and designing measures to be taken in the case of materialisation of the risks. The European Artificial Intelligence Office (AI Office) should develop a template for a questionnaire in order to facilitate compliance and reduce the administrative burden for deployers.

[3] Cite as: AI Act, Article 27 | type: article — Fundamental rights impact assessment for high-risk AI systems
1. Prior to deploying a high-risk AI system referred to in Article 6(2), with the exception of high-risk AI systems intended to be used in the area listed in point 2 of Annex III, deployers that are bodies governed by public law, or are private entities providing public services, and deployers of high-risk AI systems referred to in points 5 (b) and (c) of Annex III, shall perform an assessment of the impact on fundamental rights that the use of such system may produce. For that purpose, deployers shall perform an assessment consisting of:
(a) a description of the deployer’s processes in which the high-risk AI system will be used in line with its intended purpose;
(b) a description of the period of time within which, and the frequency with which, each high-risk AI system is intended to be used;
(c) the categories of natural persons and groups likely to be affected by its use in the specific context;
(d) the specific risks of harm likely to have an impact on the categories of natural persons or groups of persons identified pursuant to point (c) of this paragraph, taking into account the information given by the provider pursuant to Article 13;
(e) a description of the implementation of human oversight measures, according to the instructions for use;
(f) the measures to be taken in the case of the materialisation of those risks, including the arrangements for internal governance and complaint mechanisms.
2. The obligation laid down in paragraph 1 applies to the first use of the high-risk AI system. The deployer may, in similar cases, rely on previously conducted fundamental rights impact assessments or existing impact assessments carried out by provider. If, during the use of the high-risk AI system, the deployer considers that any of the elements listed in paragraph 1 has changed or is no longer up to date, the deployer shall take the necessary steps to update the information.
3. Once the assessment referred to in paragraph 1 of this Article has been performed, the deployer shall notify the market surveillance authority of its results, submitting the filled-out template referred to in paragraph 5 of this Article as part of the notification. In the case referred to in Article 46(1), deployers may be exempt from that obligation to notify.
4. If any of the obligations laid down in this Article is already met through the data protection impact assessment conducted pursuant to Article 35 of Regulation (EU) 2016/679 or Article 27 of Directive (EU) 2016/680, the fundamental rights impact assessment referred to in paragraph 1 of this Article shall complement that data protection impact assessment.
5. The AI Office shall develop a template for a questionnaire, including through an automated tool, to facilitate deployers in complying with their obligations under this Article in a simplified manner.

[4] Cite as: AI Act, Recital 48 | type: recital
The extent of the adverse impact caused by the AI system on the fundamental rights protected by the Charter is of particular relevance when classifying an AI system as high risk. Those rights include the right to human dignity, respect for private and family life, protection of personal data, freedom of expression and information, freedom of assembly and of association, the right to non-discrimination, the right to education, consumer protection, workers’ rights, the rights of persons with disabilities, gender equality, intellectual property rights, the right to an effective remedy and to a fair trial, the right of defence and the presumption of innocence, and the right to good administration. In addition to those rights, it is important to highlight the fact that children have specific rights as enshrined in Article 24 of the Charter and in the United Nations Convention on the Rights of the Child, further developed in the UNCRC General Comment No 25 as regards the digital environment, both of which require consideration of the children’s vulnerabilities and provision of such protection and care as necessary for their well-being. The fundamental right to a high level of environmental protection enshrined in the Charter and implemented in Union policies should also be considered when assessing the severity of the harm that an AI system can cause, including in relation to the health and safety of persons.

[5] Cite as: AI Act, Recital 31 | type: recital
AI systems providing social scoring of natural persons by public or private actors may lead to discriminatory outcomes and the exclusion of certain groups. They may violate the right to dignity and non-discrimination and the values of equality and justice. Such AI systems evaluate or classify natural persons or groups thereof on the basis of multiple data points related to their social behaviour in multiple contexts or known, inferred or predicted personal or personality characteristics over certain periods of time. The social score obtained from such AI systems may lead to the detrimental or unfavourable treatment of natural persons or whole groups thereof in social contexts, which are unrelated to the context in which the data was originally generated or collected or to a detrimental treatment that is disproportionate or unjustified to the gravity of their social behaviour. AI systems entailing such unacceptable scoring practices and leading to such detrimental or unfavourable outcomes should therefore be prohibited. That prohibition should not affect lawful evaluation practices of natural persons that are carried out for a specific purpose in accordance with Union and national law.
```
</details>

<details><summary>search: GDPR Article 35 data protection impact assessment credit scoring</summary>

```
[1] Cite as: GDPR, Article 35 | type: article — Data protection impact assessment (part 1 of 2)
1. Where a type of processing in particular using new technologies, and taking into account the nature, scope, context and purposes of the processing, is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall, prior to the processing, carry out an assessment of the impact of the envisaged processing operations on the protection of personal data. A single assessment may address a set of similar processing operations that present similar high risks.
2. The controller shall seek the advice of the data protection officer, where designated, when carrying out a data protection impact assessment.
3. A data protection impact assessment referred to in paragraph 1 shall in particular be required in the case of:
(a) a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person;
(b) processing on a large scale of special categories of data referred to in Article 9(1), or of personal data relating to criminal convictions and offences referred to in Article 10; or
(c) a systematic monitoring of a publicly accessible area on a large scale.
4. The supervisory authority shall establish and make public a list of the kind of processing operations which are subject to the requirement for a data protection impact assessment pursuant to paragraph 1. The supervisory authority shall communicate those lists to the Board referred to in Article 68.
5. The supervisory authority may also establish and make public a list of the kind of processing operations for which no data protection impact assessment is required. The supervisory authority shall communicate those lists to the Board.
6. Prior to the adoption of the lists referred to in paragraphs 4 and 5, the competent supervisory authority shall apply the consistency mechanism referred to in Article 63 where such lists involve processing activities which are related to the offering of goods or services to data subjects or to the monitoring of their behaviour in several Member States, or may substantially affect the free movement of personal data within the Union.
7. The assessment shall contain at least:
(a) a systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitimate interest pursued by the controller;
(b) an assessment of the necessity and proportionality of the processing operations in relation to the purposes;
(c) an assessment of the risks to the rights and freedoms of data subjects referred to in paragraph 1; and
(d) the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned.
8. Compliance with approved codes of conduct referred to in Article 40 by the relevant controllers or processors shall be taken into due account in assessing the impact of the processing operations performed by such controllers or processors, in particular for the purposes of a data protection impact assessment.
9. Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to the protection of commercial or public interests or the security of processing operations.

[2] Cite as: GDPR, Article 35 | type: article — Data protection impact assessment (part 2 of 2)
10. Where processing pursuant to point (c) or (e) of Article 6(1) has a legal basis in Union law or in the law of the Member State to which the controller is subject, that law regulates the specific processing operation or set of operations in question, and a data protection impact assessment has already been carried out as part of a general impact assessment in the context of the adoption of that legal basis, paragraphs 1 to 7 shall not apply unless Member States deem it to be necessary to carry out such an assessment prior to processing activities.
11. Where necessary, the controller shall carry out a review to assess if processing is performed in accordance with the data protection impact assessment at least when there is a change of the risk represented by processing operations.

[3] Cite as: GDPR, Recital 84 | type: recital
In order to enhance compliance with this Regulation where processing operations are likely to result in a high risk to the rights and freedoms of natural persons, the controller should be responsible for the carrying-out of a data protection impact assessment to evaluate, in particular, the origin, nature, particularity and severity of that risk. The outcome of the assessment should be taken into account when determining the appropriate measures to be taken in order to demonstrate that the processing of personal data complies with this Regulation. Where a data-protection impact assessment indicates that processing operations involve a high risk which the controller cannot mitigate by appropriate measures in terms of available technology and costs of implementation, a consultation of the supervisory authority should take place prior to the processing.

[4] Cite as: GDPR, Recital 90 | type: recital
In such cases, a data protection impact assessment should be carried out by the controller prior to the processing in order to assess the particular likelihood and severity of the high risk, taking into account the nature, scope, context and purposes of the processing and the sources of the risk. That impact assessment should include, in particular, the measures, safeguards and mechanisms envisaged for mitigating that risk, ensuring the protection of personal data and demonstrating compliance with this Regulation.

[5] Cite as: GDPR, Article 36 | type: article — Prior consultation
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
5. Notwithstanding paragraph 1, Member State law may require controllers to consult with, and obtain prior authorisation from, the supervisory authority in relation to processing by a controller for the performance of a task carried out by the controller in the public interest, including processing in relation to social protection and public health.
```
</details>

---

## m04 (multi)

**Question:** We target ads on our platform using user profiles. What must each ad show, and can we target based on users' religion or health?

**Reference:** Each ad must be clearly identifiable as an ad, and show on whose behalf it is presented, who paid for it, and meaningful information about the main parameters used to target it. Platforms must not present ads based on profiling using special categories of personal data, such as religion or health, as defined in GDPR Article 9.

**Expected:** DSA, Article 26; GDPR, Article 9

**Answer:**

It depends on whether your platform qualifies as an online platform under the Digital Services Act and how you handle user consent under the GDPR. 

### What each ad must show
For each specific ad presented on your online platform, you must ensure that users can clearly, concisely, unambiguously, and in real time identify:
* That the information is an advertisement, using prominent markings (DSA, Article 26(1)(a)).
* The natural or legal person on whose behalf the ad is presented (DSA, Article 26(1)(b)).
* The natural or legal person who paid for the ad, if different from the above (DSA, Article 26(1)(c)).
* Meaningful information, easily accessible directly from the ad, about the main parameters used to determine the recipient and how to change those parameters (DSA, Article 26(1)(d)).

### Targeting based on religion or health
**No.** Online platforms are strictly prohibited from presenting ads based on profiling using special categories of personal data (such as data concerning health or religion) as referred to in Article 9(1) of the GDPR (DSA, Article 26(3)).

### Next steps
Because these advertising and transparency duties carry heavy risks and depend on your exact platform features and user data practices, you should confirm your setup with a lawyer before launch.

**Retrieved:** DSA, Article 26; DSA, Article 39; DSA, Recital 107; DSA, Recital 68; DSA, Recital 95

<details><summary>search: advertisement transparent information recipient ad shown DSA</summary>

```
[1] Cite as: DSA, Recital 68 | type: recital
Online advertising plays an important role in the online environment, including in relation to the provision of online platforms, where the provision of the service is sometimes in whole or in part remunerated directly or indirectly, through advertising revenues. Online advertising can contribute to significant risks, ranging from advertisements that are themselves illegal content, to contributing to financial incentives for the publication or amplification of illegal or otherwise harmful content and activities online, or the discriminatory presentation of advertisements with an impact on the equal treatment and opportunities of citizens. In addition to the requirements resulting from Article 6 of Directive 2000/31/EC, providers of online platforms should therefore be required to ensure that the recipients of the service have certain individualised information necessary for them to understand when and on whose behalf the advertisement is presented. They should ensure that the information is salient, including through standardised visual or audio marks, clearly identifiable and unambiguous for the average recipient of the service, and should be adapted to the nature of the individual service’s online interface. In addition, recipients of the service should have information directly accessible from the online interface where the advertisement is presented, on the main parameters used for determining that a specific advertisement is presented to them, providing meaningful explanations of the logic used to that end, including when this is based on profiling.
Such explanations should include information on the method used for presenting the advertisement, for example whether it is contextual or other type of advertising, and, where applicable, the main profiling criteria used; it should also inform the recipient about any means available for them to change such criteria. The requirements of this Regulation on the provision of information relating to advertising is without prejudice to the application of the relevant provisions of Regulation (EU) 2016/679, in particular those regarding the right to object, automated individual decision-making, including profiling, and specifically the need to obtain consent of the data subject prior to the processing of personal data for targeted advertising. Similarly, it is without prejudice to the provisions laid down in Directive 2002/58/EC in particular those regarding the storage of information in terminal equipment and the access to information stored therein. Finally, this Regulation complements the application of the Directive 2010/13/EU which imposes measures to enable users to declare audiovisual commercial communications in user-generated videos. It also complements the obligations for traders regarding the disclosure of commercial communications deriving from Directive 2005/29/EC.

[2] Cite as: DSA, Article 26 | type: article — Advertising on online platforms
1. Providers of online platforms that present advertisements on their online interfaces shall ensure that, for each specific advertisement presented to each individual recipient, the recipients of the service are able to identify, in a clear, concise and unambiguous manner and in real time, the following:
(a) that the information is an advertisement, including through prominent markings, which might follow standards pursuant to Article 44;
(b) the natural or legal person on whose behalf the advertisement is presented;
(c) the natural or legal person who paid for the advertisement if that person is different from the natural or legal person referred to in point (b);
(d) meaningful information directly and easily accessible from the advertisement about the main parameters used to determine the recipient to whom the advertisement is presented and, where applicable, about how to change those parameters.
2. Providers of online platforms shall provide recipients of the service with a functionality to declare whether the content they provide is or contains commercial communications.
When the recipient of the service submits a declaration pursuant to this paragraph, the provider of online platforms shall ensure that other recipients of the service can identify in a clear and unambiguous manner and in real time, including through prominent markings, which might follow standards pursuant to Article 44, that the content provided by the recipient of the service is or contains commercial communications, as described in that declaration.
3. Providers of online platforms shall not present advertisements to recipients of the service based on profiling as defined in Article 4, point (4), of Regulation (EU) 2016/679 using special categories of personal data referred to in Article 9(1) of Regulation (EU) 2016/679.

[3] Cite as: DSA, Article 39 | type: article — Additional online advertising transparency
1. Providers of very large online platforms or of very large online search engines that present advertisements on their online interfaces shall compile and make publicly available in a specific section of their online interface, through a searchable and reliable tool that allows multicriteria queries and through application programming interfaces, a repository containing the information referred to in paragraph 2, for the entire period during which they present an advertisement and until one year after the advertisement was presented for the last time on their online interfaces. They shall ensure that the repository does not contain any personal data of the recipients of the service to whom the advertisement was or could have been presented, and shall make reasonable efforts to ensure that the information is accurate and complete.
2. The repository shall include at least all of the following information:
(a) the content of the advertisement, including the name of the product, service or brand and the subject matter of the advertisement;
(b) the natural or legal person on whose behalf the advertisement is presented;
(c) the natural or legal person who paid for the advertisement, if that person is different from the person referred to in point (b);
(d) the period during which the advertisement was presented;
(e) whether the advertisement was intended to be presented specifically to one or more particular groups of recipients of the service and if so, the main parameters used for that purpose including where applicable the main parameters used to exclude one or more of such particular groups;
(f) the commercial communications published on the very large online platforms and identified pursuant to Article 26(2);
(g) the total number of recipients of the service reached and, where applicable, aggregate numbers broken down by Member State for the group or groups of recipients that the advertisement specifically targeted.
3. As regards paragraph 2, points (a), (b) and (c), where a provider of very large online platform or of very large online search engine has removed or disabled access to a specific advertisement based on alleged illegality or incompatibility with its terms and conditions, the repository shall not include the information referred to in those points. In such case, the repository shall include, for the specific advertisement concerned, the information referred to in Article 17(3), points (a) to (e), or Article 9(2), point (a)(i), as applicable.
The Commission may, after consultation of the Board, the relevant vetted researchers referred to in Article 40 and the public, issue guidelines on the structure, organisation and functionalities of the repositories referred to in this Article.

[4] Cite as: DSA, Recital 95 | type: recital
Advertising systems used by very large online platforms and very large online search engines pose particular risks and require further public and regulatory supervision on account of their scale and ability to target and reach recipients of the service based on their behaviour within and outside that platform’s or search engine's online interface. Very large online platforms or very large online search engines should ensure public access to repositories of advertisements presented on their online interfaces to facilitate supervision and research into emerging risks brought about by the distribution of advertising online, for example in relation to illegal advertisements or manipulative techniques and disinformation with a real and foreseeable negative impact on public health, public security, civil discourse, political participation and equality. Repositories should include the content of advertisements, including the name of the product, service or brand and the subject matter of the advertisement, and related data on the advertiser, and, if different, the natural or legal person who paid for the advertisement, and the delivery of the advertisement, in particular where targeted advertising is concerned. This information should include both information about targeting criteria and delivery criteria, in particular when advertisements are delivered to persons in vulnerable situations, such as minors.

[5] Cite as: DSA, Recital 107 | type: recital
The provision of online advertising generally involves several actors, including intermediary services that connect publishers of advertisements with advertisers. Codes of conduct should support and complement the transparency obligations relating to advertising for providers of online platforms, of very large online platforms and of very large online search engines set out in this Regulation in order to provide for flexible and effective mechanisms to facilitate and enhance the compliance with those obligations, notably as concerns the modalities of the transmission of the relevant information. This should include facilitating the transmission of the information on the advertiser who pays for the advertisement when they differ from the natural or legal person on whose behalf the advertisement is presented on the online interface of an online platform. The codes of conduct should also include measures to ensure that meaningful information about the monetisation of data is appropriately shared throughout the value chain. The involvement of a wide range of stakeholders should ensure that those codes of conduct are widely supported, technically sound, effective and offer the highest levels of user-friendliness to ensure that the transparency obligations achieve their objectives. In order to ensure the effectiveness of codes of conduct, the Commission should include evaluation mechanisms in drawing up the codes of conduct. Where appropriate, the Commission may invite the Fundamental Rights Agency or the European Data Protection Supervisor to express their opinions on the respective code of conduct.
```
</details>

---

## m05 (multi)

**Question:** We're releasing a general-purpose foundation model. What documentation must we provide, and do we have to inform people whose personal data was in the training set?

**Reference:** GPAI providers must keep technical documentation (including training and testing), provide information to downstream providers, put in place a copyright-compliance policy, and publish a sufficiently detailed summary of the training content. Under the GDPR, when data is not obtained from the person, the controller must inform them, unless this proves impossible or would involve disproportionate effort, in which case other measures such as making the information public apply.

**Expected:** AI Act, Article 53; GDPR, Article 14

**Answer:**

**Yes, you must provide specific documentation, and whether you must inform people whose personal data was in your training set depends on whether doing so would involve a "disproportionate effort."**

### 1. Documentation You Must Provide

Under the AI Act, providers of general-purpose AI models have distinct documentation and transparency duties:

* **Technical Documentation:** You must draw up and keep up-to-date technical documentation containing at least the items set out in **Annex XI** of the AI Act (AI Act, Article 53(1)(a)). This includes:
  * A general description of the model (tasks, intended integrations, architecture, parameter count, modalities, and license) (AI Act, Annex XI, Section 1).
  * A detailed description of the development process, design specifications, training methodologies, computational resources used, and **information on the training data** (type, provenance, curation methods, scope, number of data points, and data selection measures) (AI Act, Annex XI, Section 1).
  * *Note:* This technical documentation must be made available to the AI Office and national competent authorities upon request (AI Act, Article 53(1)(a)).
* **Upstream Documentation for Downstream Integrators:** You must make documentation available to providers of downstream AI systems to help them understand the model's capabilities and limitations (AI Act, Article 53(1)(b)).
* **Public Training Content Summary:** You must draw up and make publicly available a sufficiently detailed summary of the content used to train the model, using a template provided by the AI Office (AI Act, Article 53(1)(d)). According to Recital 107, this summary should list main data collections, sets, or archives rather than being overly technical, to help copyright holders enforce their rights while protecting trade secrets (AI Act, Recital 107).
* **Copyright Policy:** You must put in place a policy to comply with EU copyright law, including identifying and respecting opt-outs expressed by rightsholders via text and data mining reservations (AI Act, Article 53(1)(c)).

---

### 2. Informing People Whose Personal Data Was in the Training Set

Because you obtained personal data from third-party sources (the training set) rather than directly from the data subjects, the GDPR generally requires you to provide those individuals with specific information—such as your identity, the purposes of processing, the categories of personal data, and their data rights—within a reasonable period (and at the latest within one month) (GDPR, Article 14(1)–(3)). 

However, **an exception applies**:
* You are **not** required to provide individual notice if doing so proves **impossible** or would involve a **disproportionate effort** (GDPR, Article 14(5)(b)). 
* When relying on the disproportionate effort exception, you must take appropriate measures to protect the data subjects' rights and freedoms and legitimate interests, which **includes making the information publicly available** (GDPR, Article 14(b); GDPR, Recital 62).

### Next Steps & Counsel
Whether notifying millions of web-scraped data subjects counts as a "disproportionate effort" depends on your specific training dataset size, how difficult it is to contact the individuals, and the safeguards you implement. Because fines under both the GDPR and AI Act can be severe, you should **confirm your documentation completeness and your GDPR notice strategy with a lawyer before launch.**

**Retrieved:** AI Act, Annex XI; AI Act, Article 53; AI Act, Recital 105; AI Act, Recital 107; AI Act, Recital 108; GDPR, Article 12; GDPR, Article 14; GDPR, Article 19; GDPR, Recital 62

<details><summary>search: general-purpose AI model documentation training data personal data copyright</summary>

```
[1] Cite as: AI Act, Recital 107 | type: recital
In order to increase transparency on the data that is used in the pre-training and training of general-purpose AI models, including text and data protected by copyright law, it is adequate that providers of such models draw up and make publicly available a sufficiently detailed summary of the content used for training the general-purpose AI model. While taking into due account the need to protect trade secrets and confidential business information, this summary should be generally comprehensive in its scope instead of technically detailed to facilitate parties with legitimate interests, including copyright holders, to exercise and enforce their rights under Union law, for example by listing the main data collections or sets that went into training the model, such as large private or public databases or data archives, and by providing a narrative explanation about other data sources used. It is appropriate for the AI Office to provide a template for the summary, which should be simple, effective, and allow the provider to provide the required summary in narrative form.

[2] Cite as: AI Act, Recital 105 | type: recital
General-purpose AI models, in particular large generative AI models, capable of generating text, images, and other content, present unique innovation opportunities but also challenges to artists, authors, and other creators and the way their creative content is created, distributed, used and consumed. The development and training of such models require access to vast amounts of text, images, videos and other data. Text and data mining techniques may be used extensively in this context for the retrieval and analysis of such content, which may be protected by copyright and related rights. Any use of copyright protected content requires the authorisation of the rightsholder concerned unless relevant copyright exceptions and limitations apply. Directive (EU) 2019/790 introduced exceptions and limitations allowing reproductions and extractions of works or other subject matter, for the purpose of text and data mining, under certain conditions. Under these rules, rightsholders may choose to reserve their rights over their works or other subject matter to prevent text and data mining, unless this is done for the purposes of scientific research. Where the rights to opt out has been expressly reserved in an appropriate manner, providers of general-purpose AI models need to obtain an authorisation from rightsholders if they want to carry out text and data mining over such works.

[3] Cite as: AI Act, Annex XI | type: annex — Technical documentation referred to in Article 53(1), point (a) — technical documentation for providers of general-purpose AI models
Section 1
Information to be provided by all providers of general-purpose AI models
The technical documentation referred to in Article 53(1), point (a) shall contain at least the following information as appropriate to the size and risk profile of the model:
1. A general description of the general-purpose AI model including:
(a) the tasks that the model is intended to perform and the type and nature of AI systems in which it can be integrated;
(b) the acceptable use policies applicable;
(c) the date of release and methods of distribution;
(d) the architecture and number of parameters;
(e) the modality (e.g. text, image) and format of inputs and outputs;
(f) the licence.
2. A detailed description of the elements of the model referred to in point 1, and relevant information of the process for the development, including the following elements:
(a) the technical means (e.g. instructions of use, infrastructure, tools) required for the general-purpose AI model to be integrated in AI systems;
(b) the design specifications of the model and training process, including training methodologies and techniques, the key design choices including the rationale and assumptions made; what the model is designed to optimise for and the relevance of the different parameters, as applicable;
(c) information on the data used for training, testing and validation, where applicable, including the type and provenance of data and curation methodologies (e.g. cleaning, filtering, etc.), the number of data points, their scope and main characteristics; how the data was obtained and selected as well as all other measures to detect the unsuitability of data sources and methods to detect identifiable biases, where applicable;
(d) the computational resources used to train the model (e.g. number of floating point operations), training time, and other relevant details related to the training;
(e) known or estimated energy consumption of the model.
With regard to point (e), where the energy consumption of the model is unknown, the energy consumption may be based on information about computational resources used.
Section 2
Additional information to be provided by providers of general-purpose AI models with systemic risk
1. A detailed description of the evaluation strategies, including evaluation results, on the basis of available public evaluation protocols and tools or otherwise of other evaluation methodologies. Evaluation strategies shall include evaluation criteria, metrics and the methodology on the identification of limitations.
2. Where applicable, a detailed description of the measures put in place for the purpose of conducting internal and/or external adversarial testing (e.g. red teaming), model adaptations, including alignment and fine-tuning.
3. Where applicable, a detailed description of the system architecture explaining how software components build or feed into each other and integrate into the overall processing.

[4] Cite as: AI Act, Article 53 | type: article — Obligations for providers of general-purpose AI models
1. Providers of general-purpose AI models shall:
(a) draw up and keep up-to-date the technical documentation of the model, including its training and testing process and the results of its evaluation, which shall contain, at a minimum, the information set out in Annex XI for the purpose of providing it, upon request, to the AI Office and the national competent authorities;
(b) draw up, keep up-to-date and make available information and documentation to providers of AI systems who intend to integrate the general-purpose AI model into their AI systems. Without prejudice to the need to observe and protect intellectual property rights and confidential business information or trade secrets in accordance with Union and national law, the information and documentation shall:
(i) enable providers of AI systems to have a good understanding of the capabilities and limitations of the general-purpose AI model and to comply with their obligations pursuant to this Regulation; and
(ii) contain, at a minimum, the elements set out in Annex XII;
(c) put in place a policy to comply with Union law on copyright and related rights, and in particular to identify and comply with, including through state-of-the-art technologies, a reservation of rights expressed pursuant to Article 4(3) of Directive (EU) 2019/790;
(d) draw up and make publicly available a sufficiently detailed summary about the content used for training of the general-purpose AI model, according to a template provided by the AI Office.
2. The obligations set out in paragraph 1, points (a) and (b), shall not apply to providers of AI models that are released under a free and open-source licence that allows for the access, usage, modification, and distribution of the model, and whose parameters, including the weights, the information on the model architecture, and the information on model usage, are made publicly available. This exception shall not apply to general-purpose AI models with systemic risks.
3. Providers of general-purpose AI models shall cooperate as necessary with the Commission and the national competent authorities in the exercise of their competences and powers pursuant to this Regulation.
4. Providers of general-purpose AI models may rely on codes of practice within the meaning of Article 56 to demonstrate compliance with the obligations set out in paragraph 1 of this Article, until a harmonised standard is published. Compliance with European harmonised standards grants providers the presumption of conformity to the extent that those standards cover those obligations. Providers of general-purpose AI models who do not adhere to an approved code of practice or do not comply with a European harmonised standard shall demonstrate alternative adequate means of compliance for assessment by the Commission.
5. For the purpose of facilitating compliance with Annex XI, in particular points 2 (d) and (e) thereof, the Commission is empowered to adopt delegated acts in accordance with Article 97 to detail measurement and calculation methodologies with a view to allowing for comparable and verifiable documentation.
6. The Commission is empowered to adopt delegated acts in accordance with Article 97(2) to amend Annexes XI and XII in light of evolving technological developments.
7. Any information or documentation obtained pursuant to this Article, including trade secrets, shall be treated in accordance with the confidentiality obligations set out in Article 78.

[5] Cite as: AI Act, Recital 108 | type: recital
With regard to the obligations imposed on providers of general-purpose AI models to put in place a policy to comply with Union copyright law and make publicly available a summary of the content used for the training, the AI Office should monitor whether the provider has fulfilled those obligations without verifying or proceeding to a work-by-work assessment of the training data in terms of copyright compliance. This Regulation does not affect the enforcement of copyright rules as provided for under Union law.
```
</details>

<details><summary>search: GDPR personal data training model inform data subjects notification exception disproportionate effort</summary>

```
[1] Cite as: GDPR, Recital 62 | type: recital
However, it is not necessary to impose the obligation to provide information where the data subject already possesses the information, where the recording or disclosure of the personal data is expressly laid down by law or where the provision of information to the data subject proves to be impossible or would involve a disproportionate effort. The latter could in particular be the case where processing is carried out for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes. In that regard, the number of data subjects, the age of the data and any appropriate safeguards adopted should be taken into consideration.

[2] Cite as: GDPR, Article 14 | type: article — Information to be provided where personal data have not been obtained from the data subject (part 2 of 2)
(b) the provision of such information proves impossible or would involve a disproportionate effort, in particular for processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes, subject to the conditions and safeguards referred to in Article 89(1) or in so far as the obligation referred to in paragraph 1 of this Article is likely to render impossible or seriously impair the achievement of the objectives of that processing. In such cases the controller shall take appropriate measures to protect the data subject's rights and freedoms and legitimate interests, including making the information publicly available;
(c) obtaining or disclosure is expressly laid down by Union or Member State law to which the controller is subject and which provides appropriate measures to protect the data subject's legitimate interests; or
(d) where the personal data must remain confidential subject to an obligation of professional secrecy regulated by Union or Member State law, including a statutory obligation of secrecy.

[3] Cite as: GDPR, Article 14 | type: article — Information to be provided where personal data have not been obtained from the data subject (part 1 of 2)
1. Where personal data have not been obtained from the data subject, the controller shall provide the data subject with the following information:
(a) the identity and the contact details of the controller and, where applicable, of the controller's representative;
(b) the contact details of the data protection officer, where applicable;
(c) the purposes of the processing for which the personal data are intended as well as the legal basis for the processing;
(d) the categories of personal data concerned;
(e) the recipients or categories of recipients of the personal data, if any;
(f) where applicable, that the controller intends to transfer personal data to a recipient in a third country or international organisation and the existence or absence of an adequacy decision by the Commission, or in the case of transfers referred to in Article 46 or 47, or the second subparagraph of Article 49(1), reference to the appropriate or suitable safeguards and the means to obtain a copy of them or where they have been made available.
2. In addition to the information referred to in paragraph 1, the controller shall provide the data subject with the following information necessary to ensure fair and transparent processing in respect of the data subject:
(a) the period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period;
(b) where the processing is based on point (f) of Article 6(1), the legitimate interests pursued by the controller or by a third party;
(c) the existence of the right to request from the controller access to and rectification or erasure of personal data or restriction of processing concerning the data subject and to object to processing as well as the right to data portability;
(d) where processing is based on point (a) of Article 6(1) or point (a) of Article 9(2), the existence of the right to withdraw consent at any time, without affecting the lawfulness of processing based on consent before its withdrawal;
(e) the right to lodge a complaint with a supervisory authority;
(f) from which source the personal data originate, and if applicable, whether it came from publicly accessible sources;
(g) the existence of automated decision-making, including profiling, referred to in Article 22(1) and (4) and, at least in those cases, meaningful information about the logic involved, as well as the significance and the envisaged consequences of such processing for the data subject.
3. The controller shall provide the information referred to in paragraphs 1 and 2:
(a) within a reasonable period after obtaining the personal data, but at the latest within one month, having regard to the specific circumstances in which the personal data are processed;
(b) if the personal data are to be used for communication with the data subject, at the latest at the time of the first communication to that data subject; or
(c) if a disclosure to another recipient is envisaged, at the latest when the personal data are first disclosed.
4. Where the controller intends to further process the personal data for a purpose other than that for which the personal data were obtained, the controller shall provide the data subject prior to that further processing with information on that other purpose and with any relevant further information as referred to in paragraph 2.
5. Paragraphs 1 to 4 shall not apply where and insofar as:
(a) the data subject already has the information;

[4] Cite as: GDPR, Article 12 | type: article — Transparent information, communication and modalities for the exercise of the rights of the data subject
1. The controller shall take appropriate measures to provide any information referred to in Articles 13 and 14 and any communication under Articles 15 to 22 and 34 relating to processing to the data subject in a concise, transparent, intelligible and easily accessible form, using clear and plain language, in particular for any information addressed specifically to a child. The information shall be provided in writing, or by other means, including, where appropriate, by electronic means. When requested by the data subject, the information may be provided orally, provided that the identity of the data subject is proven by other means.
2. The controller shall facilitate the exercise of data subject rights under Articles 15 to 22. In the cases referred to in Article 11(2), the controller shall not refuse to act on the request of the data subject for exercising his or her rights under Articles 15 to 22, unless the controller demonstrates that it is not in a position to identify the data subject.
3. The controller shall provide information on action taken on a request under Articles 15 to 22 to the data subject without undue delay and in any event within one month of receipt of the request. That period may be extended by two further months where necessary, taking into account the complexity and number of the requests. The controller shall inform the data subject of any such extension within one month of receipt of the request, together with the reasons for the delay. Where the data subject makes the request by electronic form means, the information shall be provided by electronic means where possible, unless otherwise requested by the data subject.
4. If the controller does not take action on the request of the data subject, the controller shall inform the data subject without delay and at the latest within one month of receipt of the request of the reasons for not taking action and on the possibility of lodging a complaint with a supervisory authority and seeking a judicial remedy.
5. Information provided under Articles 13 and 14 and any communication and any actions taken under Articles 15 to 22 and 34 shall be provided free of charge. Where requests from a data subject are manifestly unfounded or excessive, in particular because of their repetitive character, the controller may either:
(a) charge a reasonable fee taking into account the administrative costs of providing the information or communication or taking the action requested; or
(b) refuse to act on the request.
The controller shall bear the burden of demonstrating the manifestly unfounded or excessive character of the request.
6. Without prejudice to Article 11, where the controller has reasonable doubts concerning the identity of the natural person making the request referred to in Articles 15 to 21, the controller may request the provision of additional information necessary to confirm the identity of the data subject.
7. The information to be provided to data subjects pursuant to Articles 13 and 14 may be provided in combination with standardised icons in order to give in an easily visible, intelligible and clearly legible manner a meaningful overview of the intended processing. Where the icons are presented electronically they shall be machine-readable.
8. The Commission shall be empowered to adopt delegated acts in accordance with Article 92 for the purpose of determining the information to be presented by the icons and the procedures for providing standardised icons.

[5] Cite as: GDPR, Article 19 | type: article — Notification obligation regarding rectification or erasure of personal data or restriction of processing
The controller shall communicate any rectification or erasure of personal data or restriction of processing carried out in accordance with Article 16, Article 17(1) and Article 18 to each recipient to whom the personal data have been disclosed, unless this proves impossible or involves disproportionate effort. The controller shall inform the data subject about those recipients if the data subject requests it.
```
</details>

---

## m06 (multi)

**Question:** Worst case, how big a fine could we face if our AI hiring tool breaks the AI Act's high-risk rules and we also mishandle candidates' data under the GDPR?

**Reference:** Breaching high-risk obligations carries up to EUR 15 million or 3% of worldwide turnover; the 7% / EUR 35 million tier applies only to prohibited practices. For SMEs and startups the lower of the two amounts applies. GDPR fines go up to EUR 10 million or 2%, or EUR 20 million or 4% for breaches of principles, legal bases and data-subject rights, whichever is higher.

**Expected:** AI Act, Article 99; GDPR, Article 83

**Answer:**

Yes, your startup could face severe administrative fines under both frameworks. 

### 1. Under the AI Act
For non-compliance with obligations regarding high-risk AI systems (such as AI hiring tools, which fall under high-risk categories), infringements can lead to administrative fines of up to **EUR 15 000 000**, or, if the offender is an undertaking, up to **3 % of its total worldwide annual turnover** for the preceding financial year, whichever is higher (AI Act, Article 99(4)). 

However, because your business is a start-up or SME, the rules state that the fine shall be up to the percentage or amount specified **whichever is lower** (AI Act, Article 99(6)).

### 2. Under the GDPR
Depending on which data protection rules you mishandle, GDPR fines are split into tiers:
* Infringements of basic processing principles, lawful consent, or data subjects' rights can reach up to **EUR 20 000 000**, or up to **4 % of the total worldwide annual turnover** of the preceding financial year, whichever is higher (GDPR, Article 83(5)).
* Infringements of general obligations (such as security of processing or data protection by design/default) can reach up to **EUR 10 000 000**, or up to **2 % of the total worldwide annual turnover**, whichever is higher (GDPR, Article 83(4)).

### Cumulative Penalties and Next Steps
Authorities take into account factors such as the nature, gravity, and duration of the infringement, whether it was intentional or negligent, and your cooperation (AI Act, Article 99(7); GDPR, Article 83(2)). If you commit multiple linked violations, the GDPR notes that the total fine should not exceed the amount specified for the gravest infringement (GDPR, Article 83(3)), but separate regulators enforce the AI Act and GDPR respectively.

*Because potential turnover-based fines can threaten the economic viability of a startup, you should confirm your high-risk classification, data processing legal bases, and compliance posture with a lawyer before launch.*

**Retrieved:** AI Act, Article 100; AI Act, Article 101; AI Act, Article 99; AI Act, Recital 169; GDPR, Article 83; GDPR, Article 84; GDPR, Recital 150; GDPR, Recital 152

<details><summary>search: AI Act fines high risk infringement Article 99</summary>

```
[1] Cite as: AI Act, Article 99 | type: article — Penalties (part 1 of 2)
1. In accordance with the terms and conditions laid down in this Regulation, Member States shall lay down the rules on penalties and other enforcement measures, which may also include warnings and non-monetary measures, applicable to infringements of this Regulation by operators, and shall take all measures necessary to ensure that they are properly and effectively implemented, thereby taking into account the guidelines issued by the Commission pursuant to Article 96. The penalties provided for shall be effective, proportionate and dissuasive. They shall take into account the interests of SMEs, including start-ups, and their economic viability.
2. The Member States shall, without delay and at the latest by the date of entry into application, notify the Commission of the rules on penalties and of other enforcement measures referred to in paragraph 1, and shall notify it, without delay, of any subsequent amendment to them.
3. Non-compliance with the prohibition of the AI practices referred to in Article 5 shall be subject to administrative fines of up to EUR 35 000 000 or, if the offender is an undertaking, up to 7 % of its total worldwide annual turnover for the preceding financial year, whichever is higher.
4. Non-compliance with any of the following provisions related to operators or notified bodies, other than those laid down in Articles 5, shall be subject to administrative fines of up to EUR 15 000 000 or, if the offender is an undertaking, up to 3 % of its total worldwide annual turnover for the preceding financial year, whichever is higher:
(a) obligations of providers pursuant to Article 16;
(b) obligations of authorised representatives pursuant to Article 22;
(c) obligations of importers pursuant to Article 23;
(d) obligations of distributors pursuant to Article 24;
(e) obligations of deployers pursuant to Article 26;
(f) requirements and obligations of notified bodies pursuant to Article 31, Article 33(1), (3) and (4) or Article 34;
(g) transparency obligations for providers and deployers pursuant to Article 50.
5. The supply of incorrect, incomplete or misleading information to notified bodies or national competent authorities in reply to a request shall be subject to administrative fines of up to EUR 7 500 000 or, if the offender is an undertaking, up to 1 % of its total worldwide annual turnover for the preceding financial year, whichever is higher.
6. In the case of SMEs, including start-ups, each fine referred to in this Article shall be up to the percentages or amount referred to in paragraphs 3, 4 and 5, whichever thereof is lower.
7. When deciding whether to impose an administrative fine and when deciding on the amount of the administrative fine in each individual case, all relevant circumstances of the specific situation shall be taken into account and, as appropriate, regard shall be given to the following:
(a) the nature, gravity and duration of the infringement and of its consequences, taking into account the purpose of the AI system, as well as, where appropriate, the number of affected persons and the level of damage suffered by them;
(b) whether administrative fines have already been applied by other market surveillance authorities to the same operator for the same infringement;
(c) whether administrative fines have already been applied by other authorities to the same operator for infringements of other Union or national law, when such infringements result from the same activity or omission constituting a relevant infringement of this Regulation;
(d) the size, the annual turnover and market share of the operator committing the infringement;

[2] Cite as: AI Act, Article 100 | type: article — Administrative fines on Union institutions, bodies, offices and agencies
1. The European Data Protection Supervisor may impose administrative fines on Union institutions, bodies, offices and agencies falling within the scope of this Regulation. When deciding whether to impose an administrative fine and when deciding on the amount of the administrative fine in each individual case, all relevant circumstances of the specific situation shall be taken into account and due regard shall be given to the following:
(a) the nature, gravity and duration of the infringement and of its consequences, taking into account the purpose of the AI system concerned, as well as, where appropriate, the number of affected persons and the level of damage suffered by them;
(b) the degree of responsibility of the Union institution, body, office or agency, taking into account technical and organisational measures implemented by them;
(c) any action taken by the Union institution, body, office or agency to mitigate the damage suffered by affected persons;
(d) the degree of cooperation with the European Data Protection Supervisor in order to remedy the infringement and mitigate the possible adverse effects of the infringement, including compliance with any of the measures previously ordered by the European Data Protection Supervisor against the Union institution, body, office or agency concerned with regard to the same subject matter;
(e) any similar previous infringements by the Union institution, body, office or agency;
(f) the manner in which the infringement became known to the European Data Protection Supervisor, in particular whether, and if so to what extent, the Union institution, body, office or agency notified the infringement;
(g) the annual budget of the Union institution, body, office or agency.
2. Non-compliance with the prohibition of the AI practices referred to in Article 5 shall be subject to administrative fines of up to EUR 1 500 000.
3. The non-compliance of the AI system with any requirements or obligations under this Regulation, other than those laid down in Article 5, shall be subject to administrative fines of up to EUR 750 000.
4. Before taking decisions pursuant to this Article, the European Data Protection Supervisor shall give the Union institution, body, office or agency which is the subject of the proceedings conducted by the European Data Protection Supervisor the opportunity of being heard on the matter regarding the possible infringement. The European Data Protection Supervisor shall base his or her decisions only on elements and circumstances on which the parties concerned have been able to comment. Complainants, if any, shall be associated closely with the proceedings.
5. The rights of defence of the parties concerned shall be fully respected in the proceedings. They shall be entitled to have access to the European Data Protection Supervisor’s file, subject to the legitimate interest of individuals or undertakings in the protection of their personal data or business secrets.
6. Funds collected by imposition of fines in this Article shall contribute to the general budget of the Union. The fines shall not affect the effective operation of the Union institution, body, office or agency fined.
7. The European Data Protection Supervisor shall, on an annual basis, notify the Commission of the administrative fines it has imposed pursuant to this Article and of any litigation or judicial proceedings it has initiated.

[3] Cite as: AI Act, Article 101 | type: article — Fines for providers of general-purpose AI models
1. The Commission may impose on providers of general-purpose AI models fines not exceeding 3 % of their annual total worldwide turnover in the preceding financial year or EUR 15 000 000, whichever is higher., when the Commission finds that the provider intentionally or negligently:
(a) infringed the relevant provisions of this Regulation;
(b) failed to comply with a request for a document or for information pursuant to Article 91, or supplied incorrect, incomplete or misleading information;
(c) failed to comply with a measure requested under Article 93;
(d) failed to make available to the Commission access to the general-purpose AI model or general-purpose AI model with systemic risk with a view to conducting an evaluation pursuant to Article 92.
In fixing the amount of the fine or periodic penalty payment, regard shall be had to the nature, gravity and duration of the infringement, taking due account of the principles of proportionality and appropriateness. The Commission shall also into account commitments made in accordance with Article 93(3) or made in relevant codes of practice in accordance with Article 56.
2. Before adopting the decision pursuant to paragraph 1, the Commission shall communicate its preliminary findings to the provider of the general-purpose AI model and give it an opportunity to be heard.
3. Fines imposed in accordance with this Article shall be effective, proportionate and dissuasive.
4. Information on fines imposed under this Article shall also be communicated to the Board as appropriate.
5. The Court of Justice of the European Union shall have unlimited jurisdiction to review decisions of the Commission fixing a fine under this Article. It may cancel, reduce or increase the fine imposed.
6. The Commission shall adopt implementing acts containing detailed arrangements and procedural safeguards for proceedings in view of the possible adoption of decisions pursuant to paragraph 1 of this Article. Those implementing acts shall be adopted in accordance with the examination procedure referred to in Article 98(2).

[4] Cite as: AI Act, Article 99 | type: article — Penalties (part 2 of 2)
(e) any other aggravating or mitigating factor applicable to the circumstances of the case, such as financial benefits gained, or losses avoided, directly or indirectly, from the infringement;
(f) the degree of cooperation with the national competent authorities, in order to remedy the infringement and mitigate the possible adverse effects of the infringement;
(g) the degree of responsibility of the operator taking into account the technical and organisational measures implemented by it;
(h) the manner in which the infringement became known to the national competent authorities, in particular whether, and if so to what extent, the operator notified the infringement;
(i) the intentional or negligent character of the infringement;
(j) any action taken by the operator to mitigate the harm suffered by the affected persons.
8. Each Member State shall lay down rules on to what extent administrative fines may be imposed on public authorities and bodies established in that Member State.
9. Depending on the legal system of the Member States, the rules on administrative fines may be applied in such a manner that the fines are imposed by competent national courts or by other bodies, as applicable in those Member States. The application of such rules in those Member States shall have an equivalent effect.
10. The exercise of powers under this Article shall be subject to appropriate procedural safeguards in accordance with Union and national law, including effective judicial remedies and due process.
11. Member States shall, on an annual basis, report to the Commission about the administrative fines they have issued during that year, in accordance with this Article, and about any related litigation or judicial proceedings.

[5] Cite as: AI Act, Recital 169 | type: recital
Compliance with the obligations on providers of general-purpose AI models imposed under this Regulation should be enforceable, inter alia, by means of fines. To that end, appropriate levels of fines should also be laid down for infringement of those obligations, including the failure to comply with measures requested by the Commission in accordance with this Regulation, subject to appropriate limitation periods in accordance with the principle of proportionality. All decisions taken by the Commission under this Regulation are subject to review by the Court of Justice of the European Union in accordance with the TFEU, including the unlimited jurisdiction of the Court of Justice with regard to penalties pursuant to Article 261 TFEU.
```
</details>

<details><summary>search: GDPR maximum fines Article 83</summary>

```
[1] Cite as: GDPR, Article 83 | type: article — General conditions for imposing administrative fines (part 1 of 2)
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

[2] Cite as: GDPR, Article 83 | type: article — General conditions for imposing administrative fines (part 2 of 2)
(e) non-compliance with an order or a temporary or definitive limitation on processing or the suspension of data flows by the supervisory authority pursuant to Article 58(2) or failure to provide access in violation of Article 58(1).
6. Non-compliance with an order by the supervisory authority as referred to in Article 58(2) shall, in accordance with paragraph 2 of this Article, be subject to administrative fines up to 20 000 000 EUR, or in the case of an undertaking, up to 4 % of the total worldwide annual turnover of the preceding financial year, whichever is higher.
7. Without prejudice to the corrective powers of supervisory authorities pursuant to Article 58(2), each Member State may lay down the rules on whether and to what extent administrative fines may be imposed on public authorities and bodies established in that Member State.
8. The exercise by the supervisory authority of its powers under this Article shall be subject to appropriate procedural safeguards in accordance with Union and Member State law, including effective judicial remedy and due process.
9. Where the legal system of the Member State does not provide for administrative fines, this Article may be applied in such a manner that the fine is initiated by the competent supervisory authority and imposed by competent national courts, while ensuring that those legal remedies are effective and have an equivalent effect to the administrative fines imposed by supervisory authorities. In any event, the fines imposed shall be effective, proportionate and dissuasive. Those Member States shall notify to the Commission the provisions of their laws which they adopt pursuant to this paragraph by 25 May 2018 and, without delay, any subsequent amendment law or amendment affecting them.

[3] Cite as: GDPR, Recital 150 | type: recital
In order to strengthen and harmonise administrative penalties for infringements of this Regulation, each supervisory authority should have the power to impose administrative fines. This Regulation should indicate infringements and the upper limit and criteria for setting the related administrative fines, which should be determined by the competent supervisory authority in each individual case, taking into account all relevant circumstances of the specific situation, with due regard in particular to the nature, gravity and duration of the infringement and of its consequences and the measures taken to ensure compliance with the obligations under this Regulation and to prevent or mitigate the consequences of the infringement. Where administrative fines are imposed on an undertaking, an undertaking should be understood to be an undertaking in accordance with Articles 101 and 102 TFEU for those purposes. Where administrative fines are imposed on persons that are not an undertaking, the supervisory authority should take account of the general level of income in the Member State as well as the economic situation of the person in considering the appropriate amount of the fine. The consistency mechanism may also be used to promote a consistent application of administrative fines. It should be for the Member States to determine whether and to which extent public authorities should be subject to administrative fines. Imposing an administrative fine or giving a warning does not affect the application of other powers of the supervisory authorities or of other penalties under this Regulation.

[4] Cite as: GDPR, Article 84 | type: article — Penalties
1. Member States shall lay down the rules on other penalties applicable to infringements of this Regulation in particular for infringements which are not subject to administrative fines pursuant to Article 83, and shall take all measures necessary to ensure that they are implemented. Such penalties shall be effective, proportionate and dissuasive.
2. Each Member State shall notify to the Commission the provisions of its law which it adopts pursuant to paragraph 1, by 25 May 2018 and, without delay, any subsequent amendment affecting them.

[5] Cite as: GDPR, Recital 152 | type: recital
Where this Regulation does not harmonise administrative penalties or where necessary in other cases, for example in cases of serious infringements of this Regulation, Member States should implement a system which provides for effective, proportionate and dissuasive penalties. The nature of such penalties, criminal or administrative, should be determined by Member State law.
```
</details>

---

## u01 (unanswerable)

**Question:** Has the Spanish AI agency AESIA fined anyone yet?

**Reference:** The corpus doesn't cover this. It contains the regulations, not national enforcement records.

**Expected:** (none)

**Answer:**

The corpus does not cover this. 

The retrieved legal texts (the AI Act, GDPR, and DSA) establish rules on penalties, enforcement, and upper limits for fines that Member States must implement (e.g., AI Act, Article 99; DSA, Article 52; GDPR, Article 83), but they do not contain factual information about whether specific national authorities, such as Spain's AESIA, have issued any fines yet.

**Retrieved:** AI Act, Article 99; AI Act, Recital 168; DSA, Article 52; DSA, Article 78; GDPR, Article 83

<details><summary>search: AESIA fined penalty enforcement Spain</summary>

```
[1] Cite as: DSA, Article 78 | type: article — Limitation period for the enforcement of penalties
1. The power of the Commission to enforce decisions taken pursuant to Articles 74 and 76 shall be subject to a limitation period of five years.
2. Time shall begin to run on the day on which the decision becomes final.
3. The limitation period for the enforcement of penalties shall be interrupted:
(a) by notification of a decision varying the original amount of the fine or periodic penalty payment or refusing an application for variation;
(b) by any action of the Commission, or of a Member State acting at the request of the Commission, designed to enforce payment of the fine or periodic penalty payment.
4. Each interruption shall start time running afresh.
5. The limitation period for the enforcement of penalties shall be suspended for so long as:
(a) time to pay is allowed;
(b) enforcement of payment is suspended pursuant to a decision of the Court of Justice of the European Union or to a decision of a national court.

[2] Cite as: AI Act, Recital 168 | type: recital
Compliance with this Regulation should be enforceable by means of the imposition of penalties and other enforcement measures. Member States should take all necessary measures to ensure that the provisions of this Regulation are implemented, including by laying down effective, proportionate and dissuasive penalties for their infringement, and to respect the
ne bis in idem
principle. In order to strengthen and harmonise administrative penalties for infringement of this Regulation, the upper limits for setting the administrative fines for certain specific infringements should be laid down. When assessing the amount of the fines, Member States should, in each individual case, take into account all relevant circumstances of the specific situation, with due regard in particular to the nature, gravity and duration of the infringement and of its consequences and to the size of the provider, in particular if the provider is an SME, including a start-up. The European Data Protection Supervisor should have the power to impose fines on Union institutions, agencies and bodies falling within the scope of this Regulation.

[3] Cite as: DSA, Article 52 | type: article — Penalties
1. Member States shall lay down the rules on penalties applicable to infringements of this Regulation by providers of intermediary services within their competence and shall take all the necessary measures to ensure that they are implemented in accordance with Article 51.
2. Penalties shall be effective, proportionate and dissuasive. Member States shall notify the Commission of those rules and of those measures and shall notify it, without delay, of any subsequent amendments affecting them.
3. Member States shall ensure that the maximum amount of fines that may be imposed for a failure to comply with an obligation laid down in this Regulation shall be 6 % of the annual worldwide turnover of the provider of intermediary services concerned in the preceding financial year. Member States shall ensure that the maximum amount of the fine that may be imposed for the supply of incorrect, incomplete or misleading information, failure to reply or rectify incorrect, incomplete or misleading information and failure to submit to an inspection shall be 1 % of the annual income or worldwide turnover of the provider of intermediary services or person concerned in the preceding financial year.
4. Member States shall ensure that the maximum amount of a periodic penalty payment shall be 5 % of the average daily worldwide turnover or income of the provider of intermediary services concerned in the preceding financial year per day, calculated from the date specified in the decision concerned.

[4] Cite as: AI Act, Article 99 | type: article — Penalties (part 1 of 2)
1. In accordance with the terms and conditions laid down in this Regulation, Member States shall lay down the rules on penalties and other enforcement measures, which may also include warnings and non-monetary measures, applicable to infringements of this Regulation by operators, and shall take all measures necessary to ensure that they are properly and effectively implemented, thereby taking into account the guidelines issued by the Commission pursuant to Article 96. The penalties provided for shall be effective, proportionate and dissuasive. They shall take into account the interests of SMEs, including start-ups, and their economic viability.
2. The Member States shall, without delay and at the latest by the date of entry into application, notify the Commission of the rules on penalties and of other enforcement measures referred to in paragraph 1, and shall notify it, without delay, of any subsequent amendment to them.
3. Non-compliance with the prohibition of the AI practices referred to in Article 5 shall be subject to administrative fines of up to EUR 35 000 000 or, if the offender is an undertaking, up to 7 % of its total worldwide annual turnover for the preceding financial year, whichever is higher.
4. Non-compliance with any of the following provisions related to operators or notified bodies, other than those laid down in Articles 5, shall be subject to administrative fines of up to EUR 15 000 000 or, if the offender is an undertaking, up to 3 % of its total worldwide annual turnover for the preceding financial year, whichever is higher:
(a) obligations of providers pursuant to Article 16;
(b) obligations of authorised representatives pursuant to Article 22;
(c) obligations of importers pursuant to Article 23;
(d) obligations of distributors pursuant to Article 24;
(e) obligations of deployers pursuant to Article 26;
(f) requirements and obligations of notified bodies pursuant to Article 31, Article 33(1), (3) and (4) or Article 34;
(g) transparency obligations for providers and deployers pursuant to Article 50.
5. The supply of incorrect, incomplete or misleading information to notified bodies or national competent authorities in reply to a request shall be subject to administrative fines of up to EUR 7 500 000 or, if the offender is an undertaking, up to 1 % of its total worldwide annual turnover for the preceding financial year, whichever is higher.
6. In the case of SMEs, including start-ups, each fine referred to in this Article shall be up to the percentages or amount referred to in paragraphs 3, 4 and 5, whichever thereof is lower.
7. When deciding whether to impose an administrative fine and when deciding on the amount of the administrative fine in each individual case, all relevant circumstances of the specific situation shall be taken into account and, as appropriate, regard shall be given to the following:
(a) the nature, gravity and duration of the infringement and of its consequences, taking into account the purpose of the AI system, as well as, where appropriate, the number of affected persons and the level of damage suffered by them;
(b) whether administrative fines have already been applied by other market surveillance authorities to the same operator for the same infringement;
(c) whether administrative fines have already been applied by other authorities to the same operator for infringements of other Union or national law, when such infringements result from the same activity or omission constituting a relevant infringement of this Regulation;
(d) the size, the annual turnover and market share of the operator committing the infringement;

[5] Cite as: GDPR, Article 83 | type: article — General conditions for imposing administrative fines (part 1 of 2)
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
```
</details>

---

## u02 (unanswerable)

**Question:** Has the European Commission actually fined any platform under the DSA yet, and how much?

**Reference:** The corpus doesn't cover this. It sets maximum fines (DSA Article 74) but contains no enforcement decisions.

**Expected:** (none)

**Answer:**

The corpus does not cover this. 

While the retrieved text outlines the Commission's powers to impose fines of up to 6% of total worldwide annual turnover for infringements (DSA, Article 74) and periodic penalty payments (DSA, Article 76), the provided legal text does not contain records of any specific fines actually issued by the European Commission against platforms.

**Retrieved:** DSA, Article 43; DSA, Article 52; DSA, Article 74; DSA, Article 76; DSA, Recital 144

<details><summary>search: fined penalty platform DSA European Commission</summary>

```
[1] Cite as: DSA, Article 74 | type: article — Fines
1. In the decision referred to in Article 73, the Commission may impose on the provider of the very large online platform or of the very large online search engine concerned fines not exceeding 6 % of its total worldwide annual turnover in the preceding financial year where it finds that the provider, intentionally or negligently:
(a) infringes the relevant provisions of this Regulation;
(b) fails to comply with a decision ordering interim measures under Article 70; or
(c) fails to comply with a commitment made binding by a decision pursuant to Article 71.
2. The Commission may adopt a decision imposing on the provider of the very large online platform or of the very large online search engine concerned or on another natural or legal person referred to in Article 67(1) fines not exceeding 1 % of the total annual income or worldwide turnover in the preceding financial year, where they intentionally or negligently:
(a) supply incorrect, incomplete or misleading information in response to a simple request or request by a decision pursuant to Article 67;
(b) fail to reply to the request for information by decision within the set period;
(c) fail to rectify within the period set by the Commission, incorrect, incomplete or misleading information given by a member of staff, or fail or refuse to provide complete information;
(d) refuse to submit to an inspection pursuant to Article 69;
(e) fail to comply with the measures adopted by the Commission pursuant to Article 72; or
(f) fail to comply with the conditions for access to the Commission’s file pursuant to Article 79(4).
3. Before adopting the decision pursuant to paragraph 2 of this Article, the Commission shall communicate its preliminary findings to the provider of the very large online platform or of the very large online search engine concerned or to another person referred to in Article 67(1).
4. In fixing the amount of the fine, the Commission shall have regard to the nature, gravity, duration and recurrence of the infringement and, for fines imposed pursuant to paragraph 2, the delay caused to the proceedings.

[2] Cite as: DSA, Article 76 | type: article — Periodic penalty payments
1. The Commission may adopt a decision, imposing on the provider of the very large online platform or of the very large online search engine concerned or other person referred to in Article 67(1), as applicable, periodic penalty payments not exceeding 5 % of the average daily income or worldwide annual turnover in the preceding financial year per day, calculated from the date appointed by the decision, in order to compel them to:
(a) supply correct and complete information in response to a decision requiring information pursuant to Article 67;
(b) submit to an inspection which it has ordered by decision pursuant to Article 69;
(c) comply with a decision ordering interim measures pursuant to Article 70(1);
(d) comply with commitments made legally binding by a decision pursuant to Article 71(1);
(e) comply with a decision pursuant to Article 73(1), including where applicable the requirements it contains relating to the action plan referred to in Article 75.
2. Where the provider of the very large online platform or of the very large online search engine concerned or other person referred to in Article 67(1) has satisfied the obligation which the periodic penalty payment was intended to enforce, the Commission may fix the definitive amount of the periodic penalty payment at a figure lower than that under the original decision.

[3] Cite as: DSA, Article 52 | type: article — Penalties
1. Member States shall lay down the rules on penalties applicable to infringements of this Regulation by providers of intermediary services within their competence and shall take all the necessary measures to ensure that they are implemented in accordance with Article 51.
2. Penalties shall be effective, proportionate and dissuasive. Member States shall notify the Commission of those rules and of those measures and shall notify it, without delay, of any subsequent amendments affecting them.
3. Member States shall ensure that the maximum amount of fines that may be imposed for a failure to comply with an obligation laid down in this Regulation shall be 6 % of the annual worldwide turnover of the provider of intermediary services concerned in the preceding financial year. Member States shall ensure that the maximum amount of the fine that may be imposed for the supply of incorrect, incomplete or misleading information, failure to reply or rectify incorrect, incomplete or misleading information and failure to submit to an inspection shall be 1 % of the annual income or worldwide turnover of the provider of intermediary services or person concerned in the preceding financial year.
4. Member States shall ensure that the maximum amount of a periodic penalty payment shall be 5 % of the average daily worldwide turnover or income of the provider of intermediary services concerned in the preceding financial year per day, calculated from the date specified in the decision concerned.

[4] Cite as: DSA, Recital 144 | type: recital
Compliance with the relevant obligations imposed under this Regulation should be enforceable by means of fines and periodic penalty payments. To that end, appropriate levels of fines and periodic penalty payments should also be laid down for non-compliance with the obligations and breach of the procedural rules, subject to appropriate limitation periods in accordance with the principles of proportionality and
ne bis in idem
. The Commission and the relevant national authorities should coordinate their enforcement efforts in order to ensure that those principles are respected. In particular, the Commission should take into account any fines and penalties imposed on the same legal person for the same facts through a final decision in proceedings relating to an infringement of other Union or national rules, so as to ensure that the overall fines and penalties imposed are proportionate and correspond to the seriousness of the infringements committed. All decisions taken by the Commission under this Regulation are subject to review by the Court of Justice of the European Union in accordance with the TFEU. The Court of Justice of the European Union should have unlimited jurisdiction in respect of fines and penalty payments in accordance with Article 261 TFEU.

[5] Cite as: DSA, Article 43 | type: article — Supervisory fee
1. The Commission shall charge providers of very large online platforms and of very large online search engines an annual supervisory fee upon their designation pursuant to Article 33.
2. The overall amount of the annual supervisory fees shall cover the estimated costs that the Commission incurs in relation to its supervisory tasks under this Regulation, in particular costs related to the designation pursuant to Article 33, to the set-up, maintenance and operation of the database pursuant to Article 24(5) and to the information sharing system pursuant to Article 85, to referrals pursuant to Article 59, to supporting the Board pursuant to Article 62 and to the supervisory tasks pursuant to Article 56 and Section 4 of Chapter IV.
3. The providers of very large online platforms and of very large online search engines shall be charged annually a supervisory fee for each service for which they have been designated pursuant to Article 33.
The Commission shall adopt implementing acts establishing the amount of the annual supervisory fee in respect of each provider of very large online platform or of very large online search engine. When adopting those implementing acts, the Commission shall apply the methodology laid down in the delegated act referred to in paragraph 4 of this Article and shall respect the principles set out in paragraph 5 of this Article. Those implementing acts shall be adopted in accordance with the advisory procedure referred to in Article 88.
4. The Commission shall adopt delegated acts, in accordance with Article 87, laying down the detailed methodology and procedures for:
(a) the determination of the estimated costs referred to in paragraph 2;
(b) the determination of the individual annual supervisory fees referred to in paragraph 5, points (b) and (c);
(c) the determination of the maximum overall limit defined in paragraph 5, point (c); and
(d) the detailed arrangements necessary to make payments.
When adopting those delegated acts, the Commission shall respect the principles set out in paragraph 5 of this Article.
5. The implementing act referred to in paragraph 3 and the delegated act referred to in paragraph 4 shall respect the following principles:
(a) the estimation of the overall amount of the annual supervisory fee takes into account the costs incurred in the previous year;
(b) the annual supervisory fee is proportionate to the number of average monthly active recipients in the Union of each very large online platform or each very large online search engine designated pursuant to Article 33;
(c) the overall amount of the annual supervisory fee charged on a given provider of very large online platform or very large search engine does not, in any case, exceed 0,05 % of its worldwide annual net income in the preceding financial year.
6. The individual annual supervisory fees charged pursuant to paragraph 1 of this Article shall constitute external assigned revenue in accordance with Article 21(5) of Regulation (EU, Euratom) 2018/1046 of the European Parliament and of the Council
.
7. The Commission shall report annually to the European Parliament and to the Council on the overall amount of the costs incurred for the fulfilment of the tasks under this Regulation and the total amount of the individual annual supervisory fees charged in the preceding year.
```
</details>

---

## u03_adddoc (unanswerable)

**Question:** What examples does the Commission's guidance on the AI-system definition give of software that falls outside the AI Act?

**Reference:** The corpus doesn't cover this. It contains the Article 3 definition and Recital 12, but not the Commission's guidelines on the definition of an AI system. [Becomes answerable after the add-document demo.]

**Expected:** (none)

**Answer:**

The corpus does not cover this. The retrieved passages mention that the Commission is tasked with developing guidelines on the application of the AI system definition (AI Act, Article 96), but the text of those guidelines is not included in the corpus. 

Recital 12 notes generally that simpler traditional software systems, programming approaches, or systems based on rules defined solely by natural persons to automatically execute operations are not covered, but specific examples from the Commission's guidance are not provided.

**Retrieved:** AI Act, Article 3; AI Act, Article 6; AI Act, Article 96; AI Act, Recital 12; AI Act, Recital 53

<details><summary>search: AI-system definition Commission guidance software outside AI Act examples</summary>

```
[1] Cite as: AI Act, Recital 12 | type: recital
The notion of ‘AI system’ in this Regulation should be clearly defined and should be closely aligned with the work of international organisations working on AI to ensure legal certainty, facilitate international convergence and wide acceptance, while providing the flexibility to accommodate the rapid technological developments in this field. Moreover, the definition should be based on key characteristics of AI systems that distinguish it from simpler traditional software systems or programming approaches and should not cover systems that are based on the rules defined solely by natural persons to automatically execute operations. A key characteristic of AI systems is their capability to infer. This capability to infer refers to the process of obtaining the outputs, such as predictions, content, recommendations, or decisions, which can influence physical and virtual environments, and to a capability of AI systems to derive models or algorithms, or both, from inputs or data. The techniques that enable inference while building an AI system include machine learning approaches that learn from data how to achieve certain objectives, and logic- and knowledge-based approaches that infer from encoded knowledge or symbolic representation of the task to be solved. The capacity of an AI system to infer transcends basic data processing by enabling learning, reasoning or modelling. The term ‘machine-based’ refers to the fact that AI systems run on machines. The reference to explicit or implicit objectives underscores that AI systems can operate according to explicit defined objectives or to implicit objectives. The objectives of the AI system may be different from the intended purpose of the AI system in a specific context. For the purposes of this Regulation, environments should be understood to be the contexts in which the AI systems operate, whereas outputs generated by the AI system reflect different functions performed by AI systems and include predictions, content, recommendations or decisions. AI systems are designed to operate with varying levels of autonomy, meaning that they have some degree of independence of actions from human involvement and of capabilities to operate without human intervention. The adaptiveness that an AI system could exhibit after deployment, refers to self-learning capabilities, allowing the system to change while in use. AI systems can be used on a stand-alone basis or as a component of a product, irrespective of whether the system is physically integrated into the product (embedded) or serves the functionality of the product without being integrated therein (non-embedded).

[2] Cite as: AI Act, Article 6 | type: article — Classification rules for high-risk AI systems (part 1 of 2)
1. Irrespective of whether an AI system is placed on the market or put into service independently of the products referred to in points (a) and (b), that AI system shall be considered to be high-risk where both of the following conditions are fulfilled:
(a) the AI system is intended to be used as a safety component of a product, or the AI system is itself a product, covered by the Union harmonisation legislation listed in Annex I;
(b) the product whose safety component pursuant to point (a) is the AI system, or the AI system itself as a product, is required to undergo a third-party conformity assessment, with a view to the placing on the market or the putting into service of that product pursuant to the Union harmonisation legislation listed in Annex I.
2. In addition to the high-risk AI systems referred to in paragraph 1, AI systems referred to in Annex III shall be considered to be high-risk.
3. By derogation from paragraph 2, an AI system referred to in Annex III shall not be considered to be high-risk where it does not pose a significant risk of harm to the health, safety or fundamental rights of natural persons, including by not materially influencing the outcome of decision making.
The first subparagraph shall apply where any of the following conditions is fulfilled:
(a) the AI system is intended to perform a narrow procedural task;
(b) the AI system is intended to improve the result of a previously completed human activity;
(c) the AI system is intended to detect decision-making patterns or deviations from prior decision-making patterns and is not meant to replace or influence the previously completed human assessment, without proper human review; or
(d) the AI system is intended to perform a preparatory task to an assessment relevant for the purposes of the use cases listed in Annex III.
Notwithstanding the first subparagraph, an AI system referred to in Annex III shall always be considered to be high-risk where the AI system performs profiling of natural persons.
4. A provider who considers that an AI system referred to in Annex III is not high-risk shall document its assessment before that system is placed on the market or put into service. Such provider shall be subject to the registration obligation set out in Article 49(2). Upon request of national competent authorities, the provider shall provide the documentation of the assessment.
5. The Commission shall, after consulting the European Artificial Intelligence Board (the ‘Board’), and no later than 2 February 2026, provide guidelines specifying the practical implementation of this Article in line with Article 96 together with a comprehensive list of practical examples of use cases of AI systems that are high-risk and not high-risk.
6. The Commission is empowered to adopt delegated acts in accordance with Article 97 in order to amend paragraph 3, second subparagraph, of this Article by adding new conditions to those laid down therein, or by modifying them, where there is concrete and reliable evidence of the existence of AI systems that fall under the scope of Annex III, but do not pose a significant risk of harm to the health, safety or fundamental rights of natural persons.
7. The Commission shall adopt delegated acts in accordance with Article 97 in order to amend paragraph 3, second subparagraph, of this Article by deleting any of the conditions laid down therein, where there is concrete and reliable evidence that this is necessary to maintain the level of protection of health, safety and fundamental rights provided for by this Regulation.

[3] Cite as: AI Act, Recital 53 | type: recital (part 2 of 2)
whether the teacher may have deviated from the grading pattern so as to flag potential inconsistencies or anomalies. The fourth condition should be that the AI system is intended to perform a task that is only preparatory to an assessment relevant for the purposes of the AI systems listed in an annex to this Regulation, thus making the possible impact of the output of the system very low in terms of representing a risk for the assessment to follow. That condition covers, inter alia, smart solutions for file handling, which include various functions from indexing, searching, text and speech processing or linking data to other data sources, or AI systems used for translation of initial documents. In any case, AI systems used in high-risk use-cases listed in an annex to this Regulation should be considered to pose significant risks of harm to the health, safety or fundamental rights if the AI system implies profiling within the meaning of Article 4, point (4) of Regulation (EU) 2016/679 or Article 3, point (4) of Directive (EU) 2016/680 or Article 3, point (5) of Regulation (EU) 2018/1725. To ensure traceability and transparency, a provider who considers that an AI system is not high-risk on the basis of the conditions referred to above should draw up documentation of the assessment before that system is placed on the market or put into service and should provide that documentation to national competent authorities upon request. Such a provider should be obliged to register the AI system in the EU database established under this Regulation. With a view to providing further guidance for the practical implementation of the conditions under which the AI systems listed in an annex to this Regulation are, on an exceptional basis, non-high-risk, the Commission should, after consulting the Board, provide guidelines specifying that practical implementation, completed by a comprehensive list of practical examples of use cases of AI systems that are high-risk and use cases that are not.

[4] Cite as: AI Act, Article 96 | type: article — Guidelines from the Commission on the implementation of this Regulation
1. The Commission shall develop guidelines on the practical implementation of this Regulation, and in particular on:
(a) the application of the requirements and obligations referred to in Articles 8 to 15 and in Article 25;
(b) the prohibited practices referred to in Article 5;
(c) the practical implementation of the provisions related to substantial modification;
(d) the practical implementation of transparency obligations laid down in Article 50;
(e) detailed information on the relationship of this Regulation with the Union harmonisation legislation listed in Annex I, as well as with other relevant Union law, including as regards consistency in their enforcement;
(f) the application of the definition of an AI system as set out in Article 3, point (1).
When issuing such guidelines, the Commission shall pay particular attention to the needs of SMEs including start-ups, of local public authorities and of the sectors most likely to be affected by this Regulation.
The guidelines referred to in the first subparagraph of this paragraph shall take due account of the generally acknowledged state of the art on AI, as well as of relevant harmonised standards and common specifications that are referred to in Articles 40 and 41, or of those harmonised standards or technical specifications that are set out pursuant to Union harmonisation law.
2. At the request of the Member States or the AI Office, or on its own initiative, the Commission shall update guidelines previously adopted when deemed necessary.

[5] Cite as: AI Act, Article 3 | type: article — Definitions (part 1 of 5)
For the purposes of this Regulation, the following definitions apply:
(1) ‘AI system’ means a machine-based system that is designed to operate with varying levels of autonomy and that may exhibit adaptiveness after deployment, and that, for explicit or implicit objectives, infers, from the input it receives, how to generate outputs such as predictions, content, recommendations, or decisions that can influence physical or virtual environments;
(2) ‘risk’ means the combination of the probability of an occurrence of harm and the severity of that harm;
(3) ‘provider’ means a natural or legal person, public authority, agency or other body that develops an AI system or a general-purpose AI model or that has an AI system or a general-purpose AI model developed and places it on the market or puts the AI system into service under its own name or trademark, whether for payment or free of charge;
(4) ‘deployer’ means a natural or legal person, public authority, agency or other body using an AI system under its authority except where the AI system is used in the course of a personal non-professional activity;
(5) ‘authorised representative’ means a natural or legal person located or established in the Union who has received and accepted a written mandate from a provider of an AI system or a general-purpose AI model to, respectively, perform and carry out on its behalf the obligations and procedures established by this Regulation;
(6) ‘importer’ means a natural or legal person located or established in the Union that places on the market an AI system that bears the name or trademark of a natural or legal person established in a third country;
(7) ‘distributor’ means a natural or legal person in the supply chain, other than the provider or the importer, that makes an AI system available on the Union market;
(8) ‘operator’ means a provider, product manufacturer, deployer, authorised representative, importer or distributor;
(9) ‘placing on the market’ means the first making available of an AI system or a general-purpose AI model on the Union market;
(10) ‘making available on the market’ means the supply of an AI system or a general-purpose AI model for distribution or use on the Union market in the course of a commercial activity, whether in return for payment or free of charge;
(11) ‘putting into service’ means the supply of an AI system for first use directly to the deployer or for own use in the Union for its intended purpose;
(12) ‘intended purpose’ means the use for which an AI system is intended by the provider, including the specific context and conditions of use, as specified in the information supplied by the provider in the instructions for use, promotional or sales materials and statements, as well as in the technical documentation;
(13) ‘reasonably foreseeable misuse’ means the use of an AI system in a way that is not in accordance with its intended purpose, but which may result from reasonably foreseeable human behaviour or interaction with other systems, including other AI systems;
(14) ‘safety component’ means a component of a product or of an AI system which fulfils a safety function for that product or AI system, or the failure or malfunctioning of which endangers the health and safety of persons or property;
(15) ‘instructions for use’ means the information provided by the provider to inform the deployer of, in particular, an AI system’s intended purpose and proper use;
```
</details>

---

## u04 (unanswerable)

**Question:** Is the EU-US Data Privacy Framework still valid for sending data to US providers?

**Reference:** The corpus doesn't cover this. The GDPR provides for adequacy decisions (Article 45), but the corpus does not contain the decision on the EU-US Data Privacy Framework or its current status.

**Expected:** (none)

**Answer:**

The corpus does not cover this. The draft answer was withheld by the citation check (cited passages that search did not return: GDPR, Article 46). Please check the official text or ask a lawyer.

**Guardrail fired:** cited passages that search did not return: GDPR, Article 46

**Withheld draft:**

The corpus does not cover this. 

The retrieved GDPR provisions explain the general legal framework for adequacy decisions (GDPR, Article 45) and appropriate safeguards (GDPR, Article 46 and Recital 108), but the corpus does not contain information regarding the EU-US Data Privacy Framework or its current status. 

Before relying on any transatlantic transfer mechanism, you should check whether the specific US provider is certified under the framework and confirm the current legal status of the adequacy decision with legal counsel.

**Retrieved:** GDPR, Article 45; GDPR, Recital 103; GDPR, Recital 104; GDPR, Recital 108

<details><summary>search: Data Privacy Framework transfer US adequacy</summary>

```
[1] Cite as: GDPR, Article 45 | type: article — Transfers on the basis of an adequacy decision (part 1 of 2)
1. A transfer of personal data to a third country or an international organisation may take place where the Commission has decided that the third country, a territory or one or more specified sectors within that third country, or the international organisation in question ensures an adequate level of protection. Such a transfer shall not require any specific authorisation.
2. When assessing the adequacy of the level of protection, the Commission shall, in particular, take account of the following elements:
(a) the rule of law, respect for human rights and fundamental freedoms, relevant legislation, both general and sectoral, including concerning public security, defence, national security and criminal law and the access of public authorities to personal data, as well as the implementation of such legislation, data protection rules, professional rules and security measures, including rules for the onward transfer of personal data to another third country or international organisation which are complied with in that country or international organisation, case-law, as well as effective and enforceable data subject rights and effective administrative and judicial redress for the data subjects whose personal data are being transferred;
(b) the existence and effective functioning of one or more independent supervisory authorities in the third country or to which an international organisation is subject, with responsibility for ensuring and enforcing compliance with the data protection rules, including adequate enforcement powers, for assisting and advising the data subjects in exercising their rights and for cooperation with the supervisory authorities of the Member States; and
(c) the international commitments the third country or international organisation concerned has entered into, or other obligations arising from legally binding conventions or instruments as well as from its participation in multilateral or regional systems, in particular in relation to the protection of personal data.
3. The Commission, after assessing the adequacy of the level of protection, may decide, by means of implementing act, that a third country, a territory or one or more specified sectors within a third country, or an international organisation ensures an adequate level of protection within the meaning of paragraph 2 of this Article. The implementing act shall provide for a mechanism for a periodic review, at least every four years, which shall take into account all relevant developments in the third country or international organisation. The implementing act shall specify its territorial and sectoral application and, where applicable, identify the supervisory authority or authorities referred to in point (b) of paragraph 2 of this Article. The implementing act shall be adopted in accordance with the examination procedure referred to in Article 93(2).
4. The Commission shall, on an ongoing basis, monitor developments in third countries and international organisations that could affect the functioning of decisions adopted pursuant to paragraph 3 of this Article and decisions adopted on the basis of Article 25(6) of Directive 95/46/EC.
5. The Commission shall, where available information reveals, in particular following the review referred to in paragraph 3 of this Article, that a third country, a territory or one or more specified sectors within a third country, or an international organisation no longer ensures an adequate level of protection within the meaning of paragraph 2 of this Article, to the extent necessary, repeal, amend or suspend the decision referred to in paragraph 3 of this Article by means of implementing acts without retro-active effect. Those implementing acts shall be adopted in accordance with the examination procedure referred to in Article 93(2).
On duly justified imperative grounds of urgency, the Commission shall adopt immediately applicable implementing acts in accordance with the procedure referred to in Article 93(3).

[2] Cite as: GDPR, Recital 103 | type: recital
The Commission may decide with effect for the entire Union that a third country, a territory or specified sector within a third country, or an international organisation, offers an adequate level of data protection, thus providing legal certainty and uniformity throughout the Union as regards the third country or international organisation which is considered to provide such level of protection. In such cases, transfers of personal data to that third country or international organisation may take place without the need to obtain any further authorisation. The Commission may also decide, having given notice and a full statement setting out the reasons to the third country or international organisation, to revoke such a decision.

[3] Cite as: GDPR, Recital 108 | type: recital
In the absence of an adequacy decision, the controller or processor should take measures to compensate for the lack of data protection in a third country by way of appropriate safeguards for the data subject. Such appropriate safeguards may consist of making use of binding corporate rules, standard data protection clauses adopted by the Commission, standard data protection clauses adopted by a supervisory authority or contractual clauses authorised by a supervisory authority. Those safeguards should ensure compliance with data protection requirements and the rights of the data subjects appropriate to processing within the Union, including the availability of enforceable data subject rights and of effective legal remedies, including to obtain effective administrative or judicial redress and to claim compensation, in the Union or in a third country. They should relate in particular to compliance with the general principles relating to personal data processing, the principles of data protection by design and by default. Transfers may also be carried out by public authorities or bodies with public authorities or bodies in third countries or with international organisations with corresponding duties or functions, including on the basis of provisions to be inserted into administrative arrangements, such as a memorandum of understanding, providing for enforceable and effective rights for data subjects. Authorisation by the competent supervisory authority should be obtained when the safeguards are provided for in administrative arrangements that are not legally binding.

[4] Cite as: GDPR, Article 45 | type: article — Transfers on the basis of an adequacy decision (part 2 of 2)
6. The Commission shall enter into consultations with the third country or international organisation with a view to remedying the situation giving rise to the decision made pursuant to paragraph 5.
7. A decision pursuant to paragraph 5 of this Article is without prejudice to transfers of personal data to the third country, a territory or one or more specified sectors within that third country, or the international organisation in question pursuant to Articles 46 to 49.
8. The Commission shall publish in the
Official Journal of the European Union
and on its website a list of the third countries, territories and specified sectors within a third country and international organisations for which it has decided that an adequate level of protection is or is no longer ensured.
9. Decisions adopted by the Commission on the basis of Article 25(6) of Directive 95/46/EC shall remain in force until amended, replaced or repealed by a Commission Decision adopted in accordance with paragraph 3 or 5 of this Article.

[5] Cite as: GDPR, Recital 104 | type: recital
In line with the fundamental values on which the Union is founded, in particular the protection of human rights, the Commission should, in its assessment of the third country, or of a territory or specified sector within a third country, take into account how a particular third country respects the rule of law, access to justice as well as international human rights norms and standards and its general and sectoral law, including legislation concerning public security, defence and national security as well as public order and criminal law. The adoption of an adequacy decision with regard to a territory or a specified sector in a third country should take into account clear and objective criteria, such as specific processing activities and the scope of applicable legal standards and legislation in force in the third country. The third country should offer guarantees ensuring an adequate level of protection essentially equivalent to that ensured within the Union, in particular where personal data are processed in one or several specific sectors. In particular, the third country should ensure effective independent data protection supervision and should provide for cooperation mechanisms with the Member States' data protection authorities, and the data subjects should be provided with effective and enforceable rights and effective administrative and judicial redress.
```
</details>

---

## u05 (unanswerable)

**Question:** Has the EU passed a new law delaying the AI Act's high-risk deadlines?

**Reference:** The corpus doesn't cover this. It contains only the AI Act as adopted in 2024 (Article 113 dates), not any later amending legislation.

**Expected:** (none)

**Answer:**

The corpus does not cover this. 

The available text only contains the AI Act (Regulation 2024/1689) as originally published in 2024. It does not cover whether any subsequent laws have been passed to delay the high-risk deadlines set out in the text (such as general application starting on 2 August 2026, or specific transition periods for existing systems under Article 111 and Article 113). 

For questions regarding updates, subsequent legislation, or ongoing enforcement changes enacted after publication, consult legal counsel.

**Retrieved:** AI Act, Article 111; AI Act, Article 113; AI Act, Article 46; AI Act, Recital 177; AI Act, Recital 179

<details><summary>search: delaying AI Act high risk deadlines</summary>

```
[1] Cite as: AI Act, Recital 177 | type: recital
In order to ensure legal certainty, ensure an appropriate adaptation period for operators and avoid disruption to the market, including by ensuring continuity of the use of AI systems, it is appropriate that this Regulation applies to the high-risk AI systems that have been placed on the market or put into service before the general date of application thereof, only if, from that date, those systems are subject to significant changes in their design or intended purpose. It is appropriate to clarify that, in this respect, the concept of significant change should be understood as equivalent in substance to the notion of substantial modification, which is used with regard only to high-risk AI systems pursuant to this Regulation. On an exceptional basis and in light of public accountability, operators of AI systems which are components of the large-scale IT systems established by the legal acts listed in an annex to this Regulation and operators of high-risk AI systems that are intended to be used by public authorities should, respectively, take the necessary steps to comply with the requirements of this Regulation by end of 2030 and by 2 August 2030.

[2] Cite as: AI Act, Article 111 | type: article — AI systems already placed on the market or put into service and general-purpose AI models already placed on the marked
1. Without prejudice to the application of Article 5 as referred to in Article 113(3), point (a), AI systems which are components of the large-scale IT systems established by the legal acts listed in Annex X that have been placed on the market or put into service before 2 August 2027 shall be brought into compliance with this Regulation by 31 December 2030.
The requirements laid down in this Regulation shall be taken into account in the evaluation of each large-scale IT system established by the legal acts listed in Annex X to be undertaken as provided for in those legal acts and where those legal acts are replaced or amended.
2. Without prejudice to the application of Article 5 as referred to in Article 113(3), point (a), this Regulation shall apply to operators of high-risk AI systems, other than the systems referred to in paragraph 1 of this Article, that have been placed on the market or put into service before 2 August 2026, only if, as from that date, those systems are subject to significant changes in their designs. In any case, the providers and deployers of high-risk AI systems intended to be used by public authorities shall take the necessary steps to comply with the requirements and obligations of this Regulation by 2 August 2030.
3. Providers of general-purpose AI models that have been placed on the market before 2 August 2025 shall take the necessary steps in order to comply with the obligations laid down in this Regulation by 2 August 2027.

[3] Cite as: AI Act, Recital 179 | type: recital
This Regulation should apply from 2 August 2026. However, taking into account the unacceptable risk associated with the use of AI in certain ways, the prohibitions as well as the general provisions of this Regulation should already apply from 2 February 2025. While the full effect of those prohibitions follows with the establishment of the governance and enforcement of this Regulation, anticipating the application of the prohibitions is important to take account of unacceptable risks and to have an effect on other procedures, such as in civil law. Moreover, the infrastructure related to the governance and the conformity assessment system should be operational before 2 August 2026, therefore the provisions on notified bodies and governance structure should apply from 2 August 2025. Given the rapid pace of technological advancements and adoption of general-purpose AI models, obligations for providers of general-purpose AI models should apply from 2 August 2025. Codes of practice should be ready by 2 May 2025 in view of enabling providers to demonstrate compliance on time. The AI Office should ensure that classification rules and procedures are up to date in light of technological developments. In addition, Member States should lay down and notify to the Commission the rules on penalties, including administrative fines, and ensure that they are properly and effectively implemented by the date of application of this Regulation. Therefore the provisions on penalties should apply from 2 August 2025.

[4] Cite as: AI Act, Article 113 | type: article — Entry into force and application
This Regulation shall enter into force on the twentieth day following that of its publication in the
Official Journal of the European Union
.
It shall apply from 2 August 2026.
However:
(a) Chapters I and II shall apply from 2 February 2025;
(b) Chapter III Section 4, Chapter V, Chapter VII and Chapter XII and Article 78 shall apply from 2 August 2025, with the exception of Article 101;
(c) Article 6(1) and the corresponding obligations in this Regulation shall apply from 2 August 2027.

[5] Cite as: AI Act, Article 46 | type: article — Derogation from conformity assessment procedure
1. By way of derogation from Article 43 and upon a duly justified request, any market surveillance authority may authorise the placing on the market or the putting into service of specific high-risk AI systems within the territory of the Member State concerned, for exceptional reasons of public security or the protection of life and health of persons, environmental protection or the protection of key industrial and infrastructural assets. That authorisation shall be for a limited period while the necessary conformity assessment procedures are being carried out, taking into account the exceptional reasons justifying the derogation. The completion of those procedures shall be undertaken without undue delay.
2. In a duly justified situation of urgency for exceptional reasons of public security or in the case of specific, substantial and imminent threat to the life or physical safety of natural persons, law-enforcement authorities or civil protection authorities may put a specific high-risk AI system into service without the authorisation referred to in paragraph 1, provided that such authorisation is requested during or after the use without undue delay. If the authorisation referred to in paragraph 1 is refused, the use of the high-risk AI system shall be stopped with immediate effect and all the results and outputs of such use shall be immediately discarded.
3. The authorisation referred to in paragraph 1 shall be issued only if the market surveillance authority concludes that the high-risk AI system complies with the requirements of Section 2. The market surveillance authority shall inform the Commission and the other Member States of any authorisation issued pursuant to paragraphs 1 and 2. This obligation shall not cover sensitive operational data in relation to the activities of law-enforcement authorities.
4. Where, within 15 calendar days of receipt of the information referred to in paragraph 3, no objection has been raised by either a Member State or the Commission in respect of an authorisation issued by a market surveillance authority of a Member State in accordance with paragraph 1, that authorisation shall be deemed justified.
5. Where, within 15 calendar days of receipt of the notification referred to in paragraph 3, objections are raised by a Member State against an authorisation issued by a market surveillance authority of another Member State, or where the Commission considers the authorisation to be contrary to Union law, or the conclusion of the Member States regarding the compliance of the system as referred to in paragraph 3 to be unfounded, the Commission shall, without delay, enter into consultations with the relevant Member State. The operators concerned shall be consulted and have the possibility to present their views. Having regard thereto, the Commission shall decide whether the authorisation is justified. The Commission shall address its decision to the Member State concerned and to the relevant operators.
6. Where the Commission considers the authorisation unjustified, it shall be withdrawn by the market surveillance authority of the Member State concerned.
7. For high-risk AI systems related to products covered by Union harmonisation legislation listed in Section A of Annex I, only the derogations from the conformity assessment established in that Union harmonisation legislation shall apply.
```
</details>

---

## u06 (unanswerable)

**Question:** Do we need user consent before setting analytics cookies on our website?

**Reference:** The corpus doesn't cover this. The consent requirement for cookies comes from the ePrivacy Directive (Article 5(3)), which is not in the corpus; the GDPR only defines what valid consent means.

**Expected:** (none)

**Answer:**

It depends, but generally **yes**, user consent is required if analytics cookies collect personal data (such as online identifiers, IP addresses, or user profiles) (GDPR, Recital 30). 

When consent is required, it must meet strict standards:
* It must be a clear affirmative act, such as choosing an option or ticking a box; silence, pre-ticked boxes, or inactivity do not constitute valid consent (GDPR, Recital 32).
* Users must be able to withdraw their consent as easily as they gave it (GDPR, Article 7(3)).
* The controller must be able to demonstrate that the user has consented (GDPR, Article 7(1)).

*Note:* The corpus does not cover the specific rules on the storing of information in terminal equipment found in the ePrivacy Directive (Directive 2002/58/EC), which also governs cookies. Because cookie rules sit at the intersection of the GDPR and the ePrivacy rules, confirm your specific analytics setup and tooling with a lawyer before launch.

**Retrieved:** GDPR, Article 4; GDPR, Article 7; GDPR, Article 95; GDPR, Recital 173; GDPR, Recital 30; GDPR, Recital 32; GDPR, Recital 33; GDPR, Recital 42; GDPR, Recital 43

<details><summary>search: cookies analytics consent</summary>

```
[1] Cite as: GDPR, Recital 32 | type: recital
Consent should be given by a clear affirmative act establishing a freely given, specific, informed and unambiguous indication of the data subject's agreement to the processing of personal data relating to him or her, such as by a written statement, including by electronic means, or an oral statement. This could include ticking a box when visiting an internet website, choosing technical settings for information society services or another statement or conduct which clearly indicates in this context the data subject's acceptance of the proposed processing of his or her personal data. Silence, pre-ticked boxes or inactivity should not therefore constitute consent. Consent should cover all processing activities carried out for the same purpose or purposes. When the processing has multiple purposes, consent should be given for all of them. If the data subject's consent is to be given following a request by electronic means, the request must be clear, concise and not unnecessarily disruptive to the use of the service for which it is provided.

[2] Cite as: GDPR, Article 7 | type: article — Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data.
2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding.
3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.
4. When assessing whether consent is freely given, utmost account shall be taken of whether,
inter alia
, the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

[3] Cite as: GDPR, Recital 33 | type: recital
It is often not possible to fully identify the purpose of personal data processing for scientific research purposes at the time of data collection. Therefore, data subjects should be allowed to give their consent to certain areas of scientific research when in keeping with recognised ethical standards for scientific research. Data subjects should have the opportunity to give their consent only to certain areas of research or parts of research projects to the extent allowed by the intended purpose.

[4] Cite as: GDPR, Recital 43 | type: recital
In order to ensure that consent is freely given, consent should not provide a valid legal ground for the processing of personal data in a specific case where there is a clear imbalance between the data subject and the controller, in particular where the controller is a public authority and it is therefore unlikely that consent was freely given in all the circumstances of that specific situation. Consent is presumed not to be freely given if it does not allow separate consent to be given to different personal data processing operations despite it being appropriate in the individual case, or if the performance of a contract, including the provision of a service, is dependent on the consent despite such consent not being necessary for such performance.

[5] Cite as: GDPR, Recital 42 | type: recital
Where processing is based on the data subject's consent, the controller should be able to demonstrate that the data subject has given consent to the processing operation. In particular in the context of a written declaration on another matter, safeguards should ensure that the data subject is aware of the fact that and the extent to which consent is given. In accordance with Council Directive 93/13/EEC
a declaration of consent pre-formulated by the controller should be provided in an intelligible and easily accessible form, using clear and plain language and it should not contain unfair terms. For consent to be informed, the data subject should be aware at least of the identity of the controller and the purposes of the processing for which the personal data are intended. Consent should not be regarded as freely given if the data subject has no genuine or free choice or is unable to refuse or withdraw consent without detriment.
```
</details>

<details><summary>search: cookie terminal equipment directive</summary>

```
[1] Cite as: GDPR, Recital 30 | type: recital
Natural persons may be associated with online identifiers provided by their devices, applications, tools and protocols, such as internet protocol addresses, cookie identifiers or other identifiers such as radio frequency identification tags. This may leave traces which, in particular when combined with unique identifiers and other information received by the servers, may be used to create profiles of the natural persons and identify them.

[2] Cite as: GDPR, Recital 32 | type: recital
Consent should be given by a clear affirmative act establishing a freely given, specific, informed and unambiguous indication of the data subject's agreement to the processing of personal data relating to him or her, such as by a written statement, including by electronic means, or an oral statement. This could include ticking a box when visiting an internet website, choosing technical settings for information society services or another statement or conduct which clearly indicates in this context the data subject's acceptance of the proposed processing of his or her personal data. Silence, pre-ticked boxes or inactivity should not therefore constitute consent. Consent should cover all processing activities carried out for the same purpose or purposes. When the processing has multiple purposes, consent should be given for all of them. If the data subject's consent is to be given following a request by electronic means, the request must be clear, concise and not unnecessarily disruptive to the use of the service for which it is provided.

[3] Cite as: GDPR, Article 4 | type: article — Definitions (part 1 of 3)
For the purposes of this Regulation:
(1) ‘personal data’ means any information relating to an identified or identifiable natural person (‘data subject’); an identifiable natural person is one who can be identified, directly or indirectly, in particular by reference to an identifier such as a name, an identification number, location data, an online identifier or to one or more factors specific to the physical, physiological, genetic, mental, economic, cultural or social identity of that natural person;
(2) ‘processing’ means any operation or set of operations which is performed on personal data or on sets of personal data, whether or not by automated means, such as collection, recording, organisation, structuring, storage, adaptation or alteration, retrieval, consultation, use, disclosure by transmission, dissemination or otherwise making available, alignment or combination, restriction, erasure or destruction;
(3) ‘restriction of processing’ means the marking of stored personal data with the aim of limiting their processing in the future;
(4) ‘profiling’ means any form of automated processing of personal data consisting of the use of personal data to evaluate certain personal aspects relating to a natural person, in particular to analyse or predict aspects concerning that natural person's performance at work, economic situation, health, personal preferences, interests, reliability, behaviour, location or movements;
(5) ‘pseudonymisation’ means the processing of personal data in such a manner that the personal data can no longer be attributed to a specific data subject without the use of additional information, provided that such additional information is kept separately and is subject to technical and organisational measures to ensure that the personal data are not attributed to an identified or identifiable natural person;
(6) ‘filing system’ means any structured set of personal data which are accessible according to specific criteria, whether centralised, decentralised or dispersed on a functional or geographical basis;
(7) ‘controller’ means the natural or legal person, public authority, agency or other body which, alone or jointly with others, determines the purposes and means of the processing of personal data; where the purposes and means of such processing are determined by Union or Member State law, the controller or the specific criteria for its nomination may be provided for by Union or Member State law;
(8) ‘processor’ means a natural or legal person, public authority, agency or other body which processes personal data on behalf of the controller;
(9) ‘recipient’ means a natural or legal person, public authority, agency or another body, to which the personal data are disclosed, whether a third party or not. However, public authorities which may receive personal data in the framework of a particular inquiry in accordance with Union or Member State law shall not be regarded as recipients; the processing of those data by those public authorities shall be in compliance with the applicable data protection rules according to the purposes of the processing;
(10) ‘third party’ means a natural or legal person, public authority, agency or body other than the data subject, controller, processor and persons who, under the direct authority of the controller or processor, are authorised to process personal data;
(11) ‘consent’ of the data subject means any freely given, specific, informed and unambiguous indication of the data subject's wishes by which he or she, by a statement or by a clear affirmative action, signifies agreement to the processing of personal data relating to him or her;
(12) ‘personal data breach’ means a breach of security leading to the accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to, personal data transmitted, stored or otherwise processed;

[4] Cite as: GDPR, Recital 173 | type: recital
This Regulation should apply to all matters concerning the protection of fundamental rights and freedoms
vis-à-vis
the processing of personal data which are not subject to specific obligations with the same objective set out in Directive 2002/58/EC of the European Parliament and of the Council
, including the obligations on the controller and the rights of natural persons. In order to clarify the relationship between this Regulation and Directive 2002/58/EC, that Directive should be amended accordingly. Once this Regulation is adopted, Directive 2002/58/EC should be reviewed in particular in order to ensure consistency with this Regulation,

[5] Cite as: GDPR, Article 95 | type: article — Relationship with Directive 2002/58/EC
This Regulation shall not impose additional obligations on natural or legal persons in relation to processing in connection with the provision of publicly available electronic communications services in public communication networks in the Union in relation to matters for which they are subject to specific obligations with the same objective set out in Directive 2002/58/EC.
```
</details>

---
