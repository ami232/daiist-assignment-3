# Label sheet
Grade the answers in this order (it is random) in `eval/human_labels.csv`, one line per answer: `id,correct,supported,notes`. At least 20; more is better. This file shows no judge verdicts.
Follow your rubric (`eval/judge_rubric.md`). `correct` is 1 only for a fully correct answer: a partial answer is 0, with a note that starts with `partial:`.
- `correct`: 1 if the answer is right against the reference answer (for an unanswerable question: a proper refusal), else 0.
- `supported`: 1 if every claim in the answer is in the retrieved passages below, else 0.
- `notes`: why, for every 0.

---

## 1. q22 (single)

**Question:** What is the maximum fine I could face if I get data protection wrong?

**Reference answer:** There are two tiers, and in each the cap is the higher of the fixed amount or, for an undertaking, a percentage of total worldwide annual turnover of the preceding financial year. Up to EUR 10 million or 2%: breaches of the controller and processor obligations in Articles 8, 11 and 25-39 (which include security, records, breach notification, DPIAs and the DPO) and 42-43, plus the certification-body and monitoring-body obligations. Up to EUR 20 million or 4%: breaches of the basic principles including consent (Articles 5, 6, 7, 9), data subjects' rights (Articles 12-22), transfers to third countries (Articles 44-49), obligations under national law adopted under Chapter IX, and non-compliance with an authority's order. These are maximums. The actual fine must be effective, proportionate and dissuasive and takes into account factors such as the nature, gravity and duration of the breach and whether it was intentional or negligent. If several provisions are infringed in the same or linked processing, the total cannot exceed the amount for the gravest infringement.

**Agent answer:**

```text
Depending on which part of the rulebook is breached, the maximum fine can fall into one of two tiers:

1. **Lower tier (up to 10,000,000 EUR, or up to 2% of total worldwide annual turnover for an undertaking, whichever is higher):** Applies to infringements of obligations such as data protection by design and by default, security of processing, data protection impact assessments, and the tasks of a data protection officer [gdpr: Article 83, paragraphs 2-4].
2. **Higher tier (up to 20,000,000 EUR, or up to 4% of total worldwide annual turnover for an undertaking, whichever is higher):** Applies to infringements of the core principles of processing, conditions for consent, data subjects' rights, and international data transfers [gdpr: Article 83, paragraphs 5-6].

Fines are decided on a case-by-case basis by the supervisory authority to be effective, proportionate, and dissuasive, taking into account factors such as the nature, gravity, and duration of the infringement, whether it was intentional or negligent, and any actions taken to mitigate damage [gdpr: Article 83, paragraphs 1-2].
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: maximum fine administrative fines article 83 GDPR

5 closest passages for: maximum fine administrative fines article 83 GDPR

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 83, paragraphs 5-6, page 83 | similarity 0.83
Heading: General conditions for imposing administrative fines
5. Infringements of the following provisions shall, in accordance with paragraph 2, be subject to administrative fines up to 20 000 000 EUR, or in the case of an undertaking, up to 4 % of the total worldwide annual turnover of the preceding financial year, whichever is higher: (a) the basic principles for processing, including conditions for consent, pursuant to Articles 5, 6, 7 and 9; (b) the data subjects' rights pursuant to Articles 12 to 22; (c) the transfers of personal data to a recipient in a third country or an international organisation pursuant to Articles 44 to 49; (d) any obligations pursuant to Member State law adopted under Chapter IX; (e) non-compliance with an order or a temporary or definitive limitation on processing or the suspension of data flows by the supervisory authority pursuant to Article 58(2) or failure to provide access in violation of Article 58(1). 6. Non-compliance with an order by the supervisory authority as referred to in Article 58(2) shall, in accordance with paragraph 2 of this Article, be subject to administrative fines up to 20 000 000 EUR, or in the case of an undertaking, up to 4 % of the total worldwide annual turnover of the preceding financial year, whichever is higher.

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 83, paragraphs 2-4, page 82 | similarity 0.82
Heading: General conditions for imposing administrative fines
(i) where measures referred to in Article 58(2) have previously been ordered against the controller or processor concerned with regard to the same subject-matter, compliance with those measures; (j) adherence to approved codes of conduct pursuant to Article 40 or approved certification mechanisms pursuant to Article 42; and (k) any other aggravating or mitigating factor applicable to the circumstances of the case, such as financial benefits gained, or losses avoided, directly or indirectly, from the infringement. 3. If a controller or processor intentionally or negligently, for the same or linked processing operations, infringes several provisions of this Regulation, the total amount of the administrative fine shall not exceed the amount specified for the gravest infringement. 4. Infringements of the following provisions shall, in accordance with paragraph 2, be subject to administrative fines up to 10 000 000 EUR, or in the case of an undertaking, up to 2 % of the total worldwide annual turnover of the preceding financial year, whichever is higher: (a) the obligations of the controller and the processor pursuant to Articles 8, 11, 25 to 39 and 42 and 43; (b) the obligations of the certification body pursuant to Articles 42 and 43; (c) the obligations of the monitoring body pursuant to Article 41(4).

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 83, paragraph 2 (part 1 of 2), page 82 | similarity 0.81
Heading: General conditions for imposing administrative fines
2. Administrative fines shall, depending on the circumstances of each individual case, be imposed in addition to, or instead of, measures referred to in points (a) to (h) and (j) of Article 58(2). When deciding whether to impose an administrative fine and deciding on the amount of the administrative fine in each individual case due regard shall be given to the following: (a) the nature, gravity and duration of the infringement taking into account the nature scope or purpose of the processing concerned as well as the number of data subjects affected and the level of damage suffered by them; (b) the intentional or negligent character of the infringement; (c) any action taken by the controller or processor to mitigate the damage suffered by data subjects; (d) the degree of responsibility of the controller or processor taking into account technical and organisational measures implemented by them pursuant to Articles 25 and 32; (e) any relevant previous infringements by the controller or processor; (f) the degree of cooperation with the supervisory authority, in order to remedy the infringement and mitigate the possible adverse effects of the infringement; (g) the categories of personal data affected by the infringement; (h) the manner in which the infringement became known to the supervisory authority, in particular whether, and if so to what extent, the controller or processor notified the infringement;

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 83, paragraph 1, page 82 | similarity 0.81
Heading: General conditions for imposing administrative fines
1. Each supervisory authority shall ensure that the imposition of administrative fines pursuant to this Article in respect of infringements of this Regulation referred to in paragraphs 4, 5 and 6 shall in each individual case be effective, proportionate and dissuasive.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 150, page 27 | similarity 0.79
(150) In order to strengthen and harmonise administrative penalties for infringements of this Regulation, each supervisory authority should have the power to impose administrative fines. This Regulation should indicate infringements and the upper limit and criteria for setting the related administrative fines, which should be determined by the competent supervisory authority in each individual case, taking into account all relevant circumstances of the specific situation, with due regard in particular to the nature, gravity and duration of the infringement and of its consequences and the measures taken to ensure compliance with the obligations under this Regulation and to prevent or mitigate the consequences of the infringement. Where administrative fines are imposed on an undertaking, an undertaking should be understood to be an undertaking in accordance with Articles 101 and 102 TFEU for those purposes. Where administrative fines are imposed on persons that are not an undertaking, the supervisory authority should take account of the general level of income in the Member State as well as the economic situation of the person in considering the appropriate amount of the fine. The consistency mechanism may also be used to promote a consistent application of administrative fines. It should be for the Member States to determine whether and to which extent public authorities should be subject to adminis trative fines. Imposing an administrative fine or giving a warning does not affect the application of other powers of the supervisory authorities or of other penalties under this Regulation.
```

</details>

---

## 2. q06 (multi)

**Question:** Customers join our newsletter with one click on the website. To unsubscribe, I tell them to call our shop during opening hours. Is that okay?

**Reference answer:** No. Article 7(3) says withdrawing consent must be as easy as giving it, and people must be told they can withdraw before they consent. The guidelines say that if consent is given with one click, withdrawal must be possible just as easily. Making people phone during business hours is more burdensome and does not comply (the music-festival example). Withdrawal doesn't make earlier processing unlawful, but you must stop the processing and delete the data if you have no other lawful basis.

**Agent answer:**

```text
No, that is not okay. 

The rules state that withdrawing consent must be as easy as giving consent, and people must be able to do it at any time [gdpr: Article 7, paragraph 3; edpb_consent: Section 5.2, paragraph 113]. If someone joins your newsletter with a single click on your website, you cannot make them call your shop during opening hours to unsubscribe, because a telephone call during business hours is more burdensome than a one-click online sign-up [edpb_consent: Section 5.2, paragraphs 114-115]. When consent is given electronically via a website, users must be able to withdraw it through the same electronic interface [edpb_consent: Section 5.2, paragraph 114].
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: withdrawal of consent easy as to give unsubscribe newsletter

5 closest passages for: withdrawal of consent easy as to give unsubscribe newsletter

[1] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 5.2, paragraphs 112-114, page 23 | similarity 0.77
Heading: Withdrawal of consent
112. Withdrawal of consent is given a prominent place in the GDPR. The provisions and recitals on withdrawal of consent in the GDPR can be regarded as codification of theexisting interpretation of this matter in WP29 Opinions.52 113. Article 7(3) of the GDPR prescribes that the controller must ensure that consent can be withdrawn by the data subject as easy as giving consent and at any given time. The GDPR does not say that giv ing and withdrawing consent must always be done through the same action. 114. However, when consent is obtained via electronic means through only one mouse -click, swipe, or keystroke, data subjects must, in practice, be able to withdraw that consent equally as easily. Where consent is obtained through use of a service-specific user interface (for example, via a website, an app, a log-on account, the interface of an IoT device or by e-mail), there is no doubt a data subject must be able to withdraw consent via the same electronic interface, as switching to another interface for the sole reason of withdrawing consentwould require undue effort. Furthermore, the data subject should be able to withdraw his/her consent without detriment. This means, inter alia, that a controller must make withdrawal of consent possible free of charge or without lowering service levels.53

[2] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 5.2, paragraphs 115-116, page 24 | similarity 0.77
Heading: Withdrawal of consent
115. Example 22: A music festival sells tickets through an online ticket agent. With each online ticket sale, consent is requested in order to use contact details for marketing purposes. To indicate consent for this purpose, customers can select either No or Yes . The controller informs customers that they have the possibility to withdraw consent. To do this, they could contact a call centre on business days between 8am and 5pm, free of charge. The controller in this example doesnot comply with article 7(3) of the GDPR. Withdrawing consent in this case requires a telephone call during business hours, this is more burdensome than the one mouse -click needed for giving consent through the online ticket vendor, which is open 24/7. 116. The requirement of an easy withdrawalis described as a necessary aspect of valid consent in the GDPR. If the withdrawal right does not meet the GDPR requirements, then the consent mechanism of the controller does not comply with the GDPR. As mentioned in section 3.1 on the condition of informed consent, the controller must inform the data subject of the right to withdraw consent prior to actually giving consent, pursuant to Article 7(3) of the GDPR. Additionally, the controller must as part of the transparency obligation inform the data subjects on how to exercise their rights.54

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 7, page 37 | similarity 0.75
Heading: Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data. 2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding. 3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent. 4. When assessing whether consent is freely given, utmost account shall be taken of whether, inter alia, the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

[4] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 5.2, paragraphs 119-120, page 25 | similarity 0.72
Heading: Withdrawal of consent
119. Controllers have an obligation to delete data that was processed on the basis of consent once that consent is withdrawn, assuming that there is no other purpose justifying the continued retention. 56 Besides this situation, covered in Article 17 (1)(b), an individual data subject may request erasure of other data concerning him that is processed on another lawful basis, e.g. on the basis of Article 6(1)(b).57 Controllers are obliged to assess whether continued processing of the data in question is appropriate, even in the absence of an erasure request by the data subject.58 120. In cases where the data subject withdraws his/her conse nt and the controller wishes to continue to process the personal data on another lawful basis, they cannot silently migrate from consent (which is withdrawn) to this other lawful basis. Any change in the lawful basis for processing must be notified to a data subject in accordance with the information requirements in Articles 13 and 14 and under the general principle of transparency.

[5] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 7.2 (part 5 of 5), page 30 | similarity 0.72
Heading: Scientific research
It is important to recall that where consent is being used as the lawful basis for processing there must be a possibility for a data subject to withdraw that consent.The EDPB notes that withdrawal of consent could undermine types scientific research that require data that can be linked to individuals, however the GDPR is clear that consent can be withdrawn and controllers must act upon this – there is no exemption to this requirement for scientific research. If a controller receives a withdrawal request, it must in principle delete the personal data straight away if it wishes to continue to use the data for the purposes of the research.76
```

</details>

---

## 3. q16 (single)

**Question:** Do I always need my customers' consent to use their data, or are there other legal reasons I can rely on?

**Reference answer:** No, consent is only one of six lawful bases. Processing is lawful only if at least one applies: consent, necessity for a contract with the person (or steps before one), necessity for a legal obligation, protecting vital interests, a public-interest task or official authority, or legitimate interests of the controller or a third party. Legitimate interests do not apply where the person's rights and freedoms override them, in particular where the person is a child. Public authorities cannot use legitimate interests for their tasks.

**Agent answer:**

```text
No, you do not always need consent. Consent is only one of six lawful bases you can rely on to process personal data [gdpr: Article 6, paragraph 1, edpb_consent: Section 6, paragraph 121]. 

Under Article 6 of the GDPR, processing is lawful if it meets at least one of these six grounds:
1. **Consent:** The individual has given clear consent for you to process their personal data for a specific purpose [gdpr: Article 6, paragraph 1(a)].
2. **Contract:** Processing is necessary because you have a contract with the individual (or because they asked you to take steps before entering into a contract) [gdpr: Article 6, paragraph 1(b)].
3. **Legal obligation:** Processing is necessary for you to comply with the law (not including contractual obligations) [gdpr: Article 6, paragraph 1(c)].
4. **Vital interests:** Processing is necessary to protect someone's life [gdpr: Article 6, paragraph 1(d)].
5. **Public interest:** Processing is necessary to perform a task in the public interest or in your official authority [gdpr: Article 6, paragraph 1(e)].
6. **Legitimate interests:** Processing is necessary for your legitimate interests (or those of a third party), provided those interests are not overridden by the rights and freedoms of the individual [gdpr: Article 6, paragraph 1(f)].

You must choose and establish the applicable lawful basis before you start processing, and you must decide this in advance of collection [edpb_consent: Section 6, paragraphs 121 and 123].
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: lawful bases for processing personal data article 6 gdpr

5 closest passages for: lawful bases for processing personal data article 6 gdpr

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 6, paragraph 1, page 36 | similarity 0.82
Heading: Lawfulness of processing
1. Processing shall be lawful only if and to the extent that at least one of the following applies: (a) the data subject has given consent to the processing of his or her personal data for one or more specific purposes; (b) processing is necessary for the performance of a contract to which the data subject is party or in order to take steps at the request of the data subject prior to entering into a contract; (c) processing is necessary for compliance with a legal obligation to which the controller is subject; (d) processing is necessary in order to protect the vital interests of the data subject or of another natural person; (e) processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller; (f) processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject which require protection of personal data, in particular where the data subject is a child. Point (f) of the first subparagraph shall not apply to processing carried out by public authorities in the performance of their tasks.

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 40, page 7 | similarity 0.78
(40) In order for processing to be lawful, personal data should be processed on the basis of the consent of the data subject concerned or some other legitimate basis, laid down by law, either in this Regulation or in other Union or Member State law as referred to in this Regulation, including the necessity for compliance with the legal obligation to which the controller is subject or the necessity for the performance of a contract to which the data subject is party or in order to take steps at the request of the data subject prior to entering into a contract.

[3] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 6, page 25 | similarity 0.77
Heading: Interaction Between Consent And Other Lawful Grounds
IN ARTICLE 6 GDPR 121. Article 6 sets the conditions for a lawful personal dat a processing and describes six lawful bases on which a controller can rely. The application of one of these six bases must be established prior to the processing activity and in relation to a specific purpose.59 122. It is important to note here that if a controller chooses to rely on consent for any part of the processing, they must be prepared to respect that choice and stop that part of the processing if an individual withdraws consent. Sending out the message that data will be processed on the basis of consent, while actually some other lawful basis is relied on, would be fundamentally unfair to individuals. 123. In other words, the controller cannot swap from consent to other lawful bases. For example, it is not allowed to retrospectively utilise the legitimate in terest basis in order to justify processing, where problems have been encountered with the validity of consent. Because of the requirement to disclose the lawful basis, which the controller is relying upon at the time of collection of personal data, controllers must have decided in advance of collection what the applicable lawful basis is.

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 6, paragraph 3, page 36 | similarity 0.76
Heading: Lawfulness of processing
3. The basis for the processing referred to in point (c) and (e) of paragraph 1 shall be laid down by: (a) Union law; or (b) Member State law to which the controller is subject. The purpose of the processing shall be determined in that legal basis or, as regards the processing referred to in point (e) of paragraph 1, shall be necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller. That legal basis may contain specific provisions to adapt the application of rules of this Regulation, inter alia: the general conditions governing the lawfulness of processing by the controller; the types of data which are subject to the processing; the data subjects concerned; the entities to, and the purposes for which, the personal data may be disclosed; the purpose limitation; storage periods; and processing operations and processing procedures, including measures to ensure lawful and fair processing such as those for other specific processing situations as provided for in Chapter IX. The Union or the Member State law shall meet an objective of public interest and be proportionate to the legitimate aim pursued.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 6, paragraph 4, page 37 | similarity 0.76
Heading: Lawfulness of processing
4. Where the processing for a purpose other than that for which the personal data have been collected is not based on the data subject's consent or on a Union or Member State law which constitutes a necessary and proportionate measure in a democratic society to safeguard the objectives referred to in Article 23(1), the controller shall, in order to ascertain whether processing for another purpose is compatible with the purpose for which the personal data are initially collected, take into account, inter alia: (a) any link between the purposes for which the personal data have been collected and the purposes of the intended further processing; (b) the context in which the personal data have been collected, in particular regarding the relationship between data subjects and the controller; (c) the nature of the personal data, in particular whether special categories of personal data are processed, pursuant to Article 9, or whether personal data related to criminal convictions and offences are processed, pursuant to Article 10; (d) the possible consequences of the intended further processing for data subjects; (e) the existence of appropriate safeguards, which may include encryption or pseudonymisation.
```

</details>

---

## 4. q30 (single)

**Question:** We discovered several similar breaches at once and need more time to investigate. Can we report them together, and what if we go past 72 hours?

**Reference answer:** Yes, in limited circumstances. Where notification is not made within 72 hours, it must be accompanied by reasons for the delay. The guidelines accept that this can happen, for example when a controller experiences multiple similar confidentiality breaches over a short period, affecting many people in the same way, and needs time to establish the extent. Strictly each breach is a reportable incident, but the controller may submit one bundled notification, provided the breaches concern the same type of personal data breached in the same way over a relatively short space of time. If the breaches involve different types of data or different ways of breaching, each must be notified normally. Delayed notification should not be seen as something that regularly takes place. Bundled notifications can also be made for multiple similar breaches reported within 72 hours.

**Agent answer:**

```text
Yes, you may submit a "bundled" notification for multiple similar breaches—provided they concern the same type of personal data breached in the same way over a relatively short space of time. If they involve different types of data or are breached in different ways, they should be reported individually [edpb_breach: Section II.B.3, paragraphs 64-65].

If your investigation takes you past the 72-hour mark, the notification can be delayed past 72 hours, provided that you accompany the late notification with reasons for the delay. The GDPR also allows you to notify the authority in phases if you do not yet have all the necessary information, as long as you explain why and state that you will provide more details later [edpb_breach: Section II.B.2, paragraph 57, Section II.B.3, paragraph 62].
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: multiple breaches at once report together 72 hours EDPB breach guidelines

5 closest passages for: multiple breaches at once report together 72 hours EDPB breach guidelines

[1] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.B.3, paragraphs 64-65, page 16 | similarity 0.84
Heading: Delayed notifications
64. Strictly speaking, each individual breach is a reportable incident. However, to avoid being overly burdensome, the controller may be able to submit a “bundled” notification representing all these breaches, provided that they concern the same type of personal data breached in the same way, over a relatively short space of time. If a series of breaches take place that concern different types of personal data, breached in different ways, then notification should proceed in the normal way, with each breach being reported in accordance with Article 33. 65. Whilst the GDPR allows for delayed notifications to an extent, this s hould not be seen as something that regularly takes place. It is worth pointing out that bundled notifications can also be made for multiple similar breaches reported within 72 hours.

[2] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.B.3, paragraphs 62-63, page 16 | similarity 0.80
Heading: Delayed notifications
62. Article 33(1) GDPR makes it clear that where notification to the supervisory authority is not made within 72 hours, it shall be accompanied by reasons for the delay. This, along with the concept of notification in phases, recognises that a controller may not always be able to notify a breach wi thin that time period, and that a delayed notification may be permissible. 63. Such a scenario might take place where, for example, a controller experiences multiple, similar confidentiality breaches over a short period of time, affecting large numbers of dat a subjects in the same way. A controller could become aware of a breach and, whilst beginning its investigation, and before notification, detect further similar breaches, which have different causes. Depending on the circumstances, it may take the controller some time to establish the extent of the breaches and, rather than notify each breach individually, the controller instead organises a meaningful notification that represents several very similar breaches, with possible different causes. This could lead to notification to the supervisory authority being delayed by more than 72 hours after the controller first becomes aware of these breaches.

[3] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.B.2, paragraph 57, page 15 | similarity 0.79
Heading: Notification in phases
57. This means that the GDPR recognises that controllers will not always have all of the necessary information concerning a breach within 72 hours of becoming aware of it, as full and comprehensive details of the incident may not always be available during this initial period. As such, it allows for a notification in phases. It is m ore likely this will be the case for more complex breaches, such as some types of cyber security incidents where, for example, an indepth forensic investigation may be necessary to fully establish the nature of the breach and the extent to which personal data have been compromised. Consequently, in many cases the controller will have to do more investigation and follow-up with additional information at a later point. This is permissible, providing the controller gives reasons for the delay, in accordance w ith Article 33(1) GDPR. The EDPB recommends that when the controller first notifies the supervisory authority, the controller should also inform the supervisory authority if the controller does not yet have all the required information and will provide more details later on. The supervisory authority should agree how and when additional information should be provided. This does not prevent the controller from providing further information at any other stage, if it becomes aware of additional relevant details about the breach that need to be provided to the supervisory authority.

[4] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section VII.A, page 30 | similarity 0.78
Heading: Flowchart showing notification requirements
Is the breach likely to result in a high risk to individuals’ rights and freedoms? Controll er detects/is made aware of a security incident and establishes if personal data beach has occurred . Is the breach likely to result in a risk to individuals’ rights ? and freedoms? Yes No No requirement to notify supervisory authority or individuals. Notify competent supervisory authority. If the breach affects individuals in more than one Member State and the conntroller has an establishment in the EEA, notify the lead supervisory authority. If the breach affects individuals in more than one Member state and the controller does not have any establishments in the EEA, but is subject to the GDPR by virtue of Article 3(2), notify every supervisory authority for which affected data subjects reside in their Member state. Yes No No requirement to notify individuals. Notify affected individuals and, where required, provide information on steps they can take to prot ect themselves from consequences of the breach. All breaches recordable under Article 33(5). Breach should be documented and record maintained by the controller. The controller becomes “ aware ” of a personal data breach and assesses risk to individuals.

[5] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.C.2, paragraphs 73-74, page 18 | similarity 0.78
Heading: Breaches at non-EU establishments
73. However, the mere presence of a representative in a Member State does not trigger the onestopshop system.36 For this reason the breach will need to be notified to every supervisory authority for which affected data subjects reside in their Member S tate. This (These) notification(s) shall be the responsibility of the controller.37 74. Similarly, where a processor is subject to Article 3(2) GDPR, it will be bound by the obligations on processors, of particular relevance here, the duty to notify a breach to the controller under Article 33(2) GDPR.
```

</details>

---

## 5. q08 (multi)

**Question:** We have a data protection officer. What should they be doing when we have a breach?

**Reference answer:** Under Article 39(1) the DPO informs and advises, monitors compliance, advises on impact assessments, cooperates with the authority and acts as its contact point. For breaches specifically, Art. 33(3)(b) means the DPO's name and contact details (or another contact point) go into the notification. The EDPB recommends the DPO is promptly informed of any breach and involved throughout the response and notification. It also suggests the DPO can advise on, or even maintain, the breach documentation.

**Agent answer:**

```text
When you have a data protection officer (DPO), they should be involved in the following ways during a breach:

* **Promptly informed and involved:** They should be informed about the breach straight away and involved throughout the entire breach management and notification process [edpb_breach: Section V.B, paragraph 133].
* **Providing advice and cooperation:** They provide data protection advice and information, and they must cooperate with the supervisory authority as well as act as a contact point for both the supervisory authority and data subjects [edpb_breach: Section V.B, paragraph 131].
* **Assisting with notifications:** Their name and contact details (or another contact point) must be provided to the supervisory authority when you notify them of a breach [edpb_breach: Section V.B, paragraph 131]. They also play a role during any subsequent investigations by the supervisory authority [edpb_breach: Section V.B, paragraph 133].
* **Documentation:** You may ask for their opinion on the structure, setup, and administration of your breach documentation, or they may be given the task of maintaining those records [edpb_breach: Section V.B, paragraph 132].
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: data protection officer breach notification responsibilities tasks

5 closest passages for: data protection officer breach notification responsibilities tasks

[1] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section V.B, paragraphs 130-132, page 27 | similarity 0.80
Heading: Role of the Data Protection Officer
130. A controller or processor may have a Data Protection Officer (DPO) 52, either as required by Article 37 GDPR, or voluntarily as a matter of good practice. Article 39 of the GDPR sets a number of mandatory tasks for the DPO, but does not prevent further tasks being allocated by the controller, if appropriate. 131. Of particular relevance to breach notification, the mandatory tasks of the DPO includes, amongst other duties, providing data protection advice and information to the controller or processor, monitoring compliance with the GDPR, and providing a dvice in relation to DPIAs. The DPO must also cooperate with the supervisory authority and act as a contact point for the supervisory authority and for data subjects. It should also be noted that, when notifying the breach to the supervisory authority, Article 33(3)(b) GDPR requires the controller to provide the name and contact details of its DPO, or other contact point. 132. In terms of documenting breaches, the controller or processor may wish to obtain the opinion of its DPO as to the structure, the settin g up and the administration of this documentation. The DPO could also be additionally tasked with maintaining such records.

[2] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section V.B, paragraph 133, page 27 | similarity 0.79
Heading: Role of the Data Protection Officer
133. These factors mean that the DPO should play an key role in assisting the prevention of or preparation for a breach by providing advice and monitoring compliance, as well as during a breach (i.e. when notifying the supervisory authority), and during any subsequent investigation by the supervisory authority. In this light, the EDPB recommends that the DPO is promptly informed about the existence of a breach and is involved throughout the breach management and notification process.

[3] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraph 39, page 13 | similarity 0.76
Heading: When does a controller become “aware”?
39. Whilst it is the responsibility of controllers and processors to put in place suitable measures to be able to prevent, react and address a breach, there are some practical steps that should be taken in all cases. • Information concerning all security -related events should be directed towards a responsible person or persons with the task of addressing incidents, establishing the existence of a breach and assessing risk. • Risk to individuals as a result of a breach should then be assessed (likelihood of no risk, risk or high risk), with relevant sections of the organisation being informed. • Notification to the supervisory authority, and potentially communication of the breach to the affected individuals should be made, if required. • At the same time, the controller should act to contain and recover the breach. Documentation of the breach should take place as it develops.

[4] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section VII.A, page 30 | similarity 0.74
Heading: Flowchart showing notification requirements
Is the breach likely to result in a high risk to individuals’ rights and freedoms? Controll er detects/is made aware of a security incident and establishes if personal data beach has occurred . Is the breach likely to result in a risk to individuals’ rights ? and freedoms? Yes No No requirement to notify supervisory authority or individuals. Notify competent supervisory authority. If the breach affects individuals in more than one Member State and the conntroller has an establishment in the EEA, notify the lead supervisory authority. If the breach affects individuals in more than one Member state and the controller does not have any establishments in the EEA, but is subject to the GDPR by virtue of Article 3(2), notify every supervisory authority for which affected data subjects reside in their Member state. Yes No No requirement to notify individuals. Notify affected individuals and, where required, provide information on steps they can take to prot ect themselves from consequences of the breach. All breaches recordable under Article 33(5). Breach should be documented and record maintained by the controller. The controller becomes “ aware ” of a personal data breach and assesses risk to individuals.

[5] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section 0, paragraphs 5-6, page 6 | similarity 0.74
Heading: Preface
5. The EDPB considers that the notification requirement has a number of benefits. When notifying the supervisory authority, controllers can obtain advice on whether the affected individuals need to be informed. Indeed, the supervisory authority may order the controller to inform those individuals about the breach10. Communicating a breach to individuals a llows the controller to provide information on the risks presented as a result of the breach and the steps those individuals can take to protect themselves from its potential consequences. The focus of any breach response plan should be on protecting individuals and their personal data. Consequently, breach notification should be seen as a tool enhancing compliance in relation to the protection of personal data. At the same time, it should be noted that failure to report a breach to either an individual or a supervisory authority may mean that under Article 83 GDPR a possible sanction is applicable to the controller. 6. Controllers and processors are therefore encouraged to plan in advance and put in place processes to be able to detect and promptly contain a breach, to assess the risk to individuals 11, and then to determine whether it is necessary to notify the competent supervisory authority, and to communicate the breach to the individuals concerned when necessary. Notification to the supervisory authority should form a part of that incident response plan.
```

</details>

---

## 6. q29 (single)

**Question:** On my sign-up page I want one tick box saying 'I agree to receive offers and to let partner shops use my details'. Is a single box okay?

**Reference answer:** No. When processing serves several purposes, people must be free to choose which purposes they accept, so each purpose needs its own separate consent. Consent is presumed not to be freely given if it does not allow separate consent for different processing operations where that is appropriate. The guidelines' own retailer example is similar: combining email marketing with sharing details with group companies in one request is not granular and the consent is not valid. The fix is to separate the purposes, for example one opt-in for your own marketing and another for passing details to named partners. Consent obtained for sharing with partners is valid only for the partners whose identity was given at the time of collection and only for that same purpose.

**Agent answer:**

```text
No, a single tick box is not okay. 

Consent must be granular when there are multiple purposes. If you are asking for consent to send marketing emails *and* to share details with partner shops, these are separate purposes, so you must provide separate, distinct consents for each one rather than bundling them into a single box. 

[edpb_consent: Section 3.1.3, paragraph 45]
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: consent bundled separate distinct sign up box offers partners

5 closest passages for: consent bundled separate distinct sign up box offers partners

[1] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.1.2, paragraphs 25-26, page 10 | similarity 0.73
Heading: Conditionality
25. To assess whether consent is freely given, Article 7(4) GDPR plays an important role.22 26. Article 7(4) GDPR indicates that, inter alia, the situation of “bundling” consent with acceptance of terms or conditions, or “tying” the provision of a contract or a service to a request for consent to process personal data that are not necessary for the p erformance of that contract or service, is considered highly undesirable. If consent is given in this situation, it is presumed to be not freely given (recital 43). Article 7(4) seeks to ensure that the purpose of personal data processing is not disguised nor bundled with the provision of a contract of a service for which these personal data are not necessary. In doing so, the GDPR ensures that the processing of personal data for which consent is sought cannot become directly or indirectly the counter -performance of a contract. The two lawful bases for the lawful processing of personal data, i.e. consent and contract cannot be merged and blurred.

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 32, page 6 | similarity 0.73
(32) Consent should be given by a clear affirmative act establishing a freely given, specific, informed and unambiguous indication of the data subject's agreement to the processing of personal data relating to him or her, such as by a written statement, including by electronic means, or an oral statement. This could include ticking a box when visiting an internet website, choosing technical settings for information society services or another statement or conduct which clearly indicates in this context the data subject's acceptance of the proposed processing of his or her personal data. Silence, pre-ticked boxes or inactivity should not therefore constitute consent. Consent should cover all processing activities carried out for the same purpose or purposes. When the processing has multiple purposes, consent should be given for all of them. If the data subject's consent is to be given following a request by electronic means, the request must be clear, concise and not unnecessarily disruptive to the use of the service for which it is provided.

[3] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.1.3, paragraph 45, page 12 | similarity 0.73
Heading: Granularity
45. Example 7: Within the same consent request a retailer asks its customers for consent to use their data to send them marketing by email and also to share their details with other companies within their group. This consent is not granular as there is no separate consents for these two separate purposes, therefore the consent will not be valid. In this case, a specific consent should be collected to send the contact details to commercial partners. Such specific consent will be deemed valid for each partner (see also section 3.3.1), whose identity has been provided to the data subject at the time of the collection of his or her consent, insofar as it is sent to them for the same purpose (in this example: a marketing purpose).

[4] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.4, paragraphs 79-81, page 18 | similarity 0.72
Heading: Unambiguous indication of wishes
79. Without prejudice to existing (national) contract law, consent can be obtained through a recorded oral statement, although due note must be taken of the information available to the data subject, prior to the indication of consent. The use of pre -ticked opt-in boxes is invalid under the GDPR. Silence or inactivity on the part of the data subject, as well as merely proceeding with a service cannot be regarded as an active indication of choice. 80. Example 14: When installing software, the application asks the data subject for consent to us e nonanonymised crash reports to improve the software. A layered privacy notice providing the necessary information accompanies the request for consent. By actively ticking the optional box stating, “I consent”, the user is able to validly perform a ´clear affirmative act´ to consent to the processing. 81. A controller must also beware that consent cannot be obtained through the same motion as agreeing to a contract or accepting general terms and conditions of a service. Blanket acceptance of general terms and conditions cannot be seen as a clear affirmative action to consent to the use of personal data. The GDPR does not allow controllers to offer pre -ticked boxes or opt -out constructions that require an intervention from the data subject to prevent agreement (for example ‘opt-out boxes’).44

[5] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.1.2, paragraphs 27-29, page 10 | similarity 0.72
Heading: Conditionality
27. Compulsion to agree with the use of personal data additional to what is strictly necessary limits data subject’s choices and stands in the way of free consent. As data protection law is aiming at the protection of fundamental rights, an individual’s control over their personal data is essential and there is a strong presumption that consent to the processing of personal data that is unnecessary, cannot be seen as a mandatory consideration in exchange for the performance of a contract or the provision of a service. 28. Hence, whenever a request for consent is tied to the performance of a contract by the controller, a data subject that does not wish to make his/her personal data available for processing by the controller runs the risk to be denied services they have requested. 29. To assess whether such a situation of bundling or tying occurs, it is important to determine what t he scope of the contract is and what data would be necessary for the performance of that contract.
```

</details>

---

## 7. q10 (single)

**Question:** I use an outside company to send my email newsletters. What does the law say I need to have in place with them?

**Reference answer:** The company is a processor, and you must use only processors giving sufficient guarantees. Their processing must be governed by a written contract (electronic is fine) that sets out the subject-matter, duration, nature and purpose, data types and categories of people. It must require them to act only on your documented instructions, ensure staff confidentiality, apply the Article 32 security measures, and not use another processor without your authorisation. It must also require them to assist with data subject requests and your other obligations, delete or return the data at the end, and give you the information and audits needed to show compliance.

**Agent answer:**

```text
When you use an outside company to process personal data on your behalf (such as sending newsletters), you must use only processors that provide sufficient guarantees to implement appropriate technical and organisational measures to meet the requirements of the GDPR and protect data subject rights. 

Your relationship with them must be governed by a contract or other legal act in writing (which can be in electronic form) that is binding on the processor. This agreement must set out the subject-matter, duration, nature and purpose of the processing, the type of personal data, categories of data subjects, and your obligations and rights as the controller. 

Specifically, the contract must stipulate that the processor:
* Processes the data only on your documented instructions (including regarding data transfers outside the EU/EEA, unless required by law).
* Ensures that people authorised to process the data have committed themselves to confidentiality or are under an appropriate statutory obligation of confidentiality.
* Takes all required security measures.
* Only engages another subcontractor processor with your prior specific or general written authorisation.
* Assists you, using appropriate technical and organisational measures, in responding to individuals exercising their data protection rights.
* Assists you in ensuring compliance with security, breach notification, data protection impact assessments, and prior consultation obligations.
* Deletes or returns all personal data to you after the services end, and deletes existing copies unless storage is required by law.
* Makes available all information necessary to demonstrate compliance and allows for and contributes to audits and inspections conducted by you or another auditor you mandate.
* Immediately informs you if they believe one of your instructions infringes data protection rules.

[gdpr: Article 28, paragraphs 1-4, 7-10]
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: processor contract controller article 28

5 closest passages for: processor contract controller article 28

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 28, paragraph 3 (part 1 of 2), page 49 | similarity 0.82
Heading: Processor
3. Processing by a processor shall be governed by a contract or other legal act under Union or Member State law, that is binding on the processor with regard to the controller and that sets out the subject-matter and duration of the processing, the nature and purpose of the processing, the type of personal data and categories of data subjects and the obligations and rights of the controller. That contract or other legal act shall stipulate, in particular, that the processor: (a) processes the personal data only on documented instructions from the controller, including with regard to transfers of personal data to a third country or an international organisation, unless required to do so by Union or Member State law to which the processor is subject; in such a case, the processor shall inform the controller of that legal requirement before processing, unless that law prohibits such information on important grounds of public interest; (b) ensures that persons authorised to process the personal data have committed themselves to confidentiality or are under an appropriate statutory obligation of confidentiality; (c) takes all measures required pursuant to Article 32; (d) respects the conditions referred to in paragraphs 2 and 4 for engaging another processor; (e) taking into account the nature of the processing, assists the controller by appropriate technical and organisational measures, insofar as this is possible, for the fulfilment of the controller's obligation to respond to requests for exercising the data subject's rights laid down in Chapter III;

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 28, paragraphs 1-2, page 49 | similarity 0.80
Heading: Processor
1. Where processing is to be carried out on behalf of a controller, the controller shall use only processors providing sufficient guarantees to implement appropriate technical and organisational measures in such a manner that processing will meet the requirements of this Regulation and ensure the protection of the rights of the data subject. 2. The processor shall not engage another processor without prior specific or general written authorisation of the controller. In the case of general written authorisation, the processor shall inform the controller of any intended changes concerning the addition or replacement of other processors, thereby giving the controller the opportunity to object to such changes.

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 28, paragraphs 7-10, page 50 | similarity 0.79
Heading: Processor
7. The Commission may lay down standard contractual clauses for the matters referred to in paragraph 3 and 4 of this Article and in accordance with the examination procedure referred to in Article 93(2). 8. A supervisory authority may adopt standard contractual clauses for the matters referred to in paragraph 3 and 4 of this Article and in accordance with the consistency mechanism referred to in Article 63. 9. The contract or the other legal act referred to in paragraphs 3 and 4 shall be in writing, including in electronic form. 10. Without prejudice to Articles 82, 83 and 84, if a processor infringes this Regulation by determining the purposes and means of processing, the processor shall be considered to be a controller in respect of that processing.

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 28, paragraph 3 (part 2 of 2), page 49 | similarity 0.79
Heading: Processor
(f) assists the controller in ensuring compliance with the obligations pursuant to Articles 32 to 36 taking into account the nature of processing and the information available to the processor; (g) at the choice of the controller, deletes or returns all the personal data to the controller after the end of the provision of services relating to processing, and deletes existing copies unless Union or Member State law requires storage of the personal data; (h) makes available to the controller all information necessary to demonstrate compliance with the obligations laid down in this Article and allow for and contribute to audits, including inspections, conducted by the controller or another auditor mandated by the controller. With regard to point (h) of the first subparagraph, the processor shall immediately inform the controller if, in its opinion, an instruction infringes this Regulation or other Union or Member State data protection provisions.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 28, paragraphs 4-6, page 50 | similarity 0.79
Heading: Processor
4. Where a processor engages another processor for carrying out specific processing activities on behalf of the controller, the same data protection obligations as set out in the contract or other legal act between the controller and the processor as referred to in paragraph 3 shall be imposed on that other processor by way of a contract or other legal act under Union or Member State law, in particular providing sufficient guarantees to implement appropriate technical and organisational measures in such a manner that the processing will meet the requirements of this Regulation. Where that other processor fails to fulfil its data protection obligations, the initial processor shall remain fully liable to the controller for the performance of that other processor's obligations. 5. Adherence of a processor to an approved code of conduct as referred to in Article 40 or an approved certification mechanism as referred to in Article 42 may be used as an element by which to demonstrate sufficient guarantees as referred to in paragraphs 1 and 4 of this Article. 6. Without prejudice to an individual contract between the controller and the processor, the contract or the other legal act referred to in paragraphs 3 and 4 of this Article may be based, in whole or in part, on standard contractual clauses referred to in paragraphs 7 and 8 of this Article, including when they are part of a certification granted to the controller or processor pursuant to Articles 42 and 43.
```

</details>

---

## 8. q01 (single)

**Question:** Someone stole a laptop with our customer loyalty list on Friday evening, but we only noticed on Monday morning. How long do we have to tell the data protection authority?

**Reference answer:** The clock starts when you become aware of the breach (Monday morning), not when the theft happened. You must notify the supervisory authority without undue delay and, where feasible, within 72 hours of becoming aware. If you miss the 72 hours, the notification must explain the reasons for the delay. The only exception is if the breach is unlikely to result in a risk to people's rights and freedoms.

**Agent answer:**

```text
You must notify the supervisory authority without undue delay and, where feasible, not later than 72 hours after having become aware of the breach [gdpr: Article 33, paragraph 1, edpb_breach: Section II.A.1, paragraph 29]. 

For the purposes of the 72-hour timeframe, a controller is generally considered to become "aware" when they have a reasonable degree of certainty that a security incident has occurred that led to personal data being compromised [edpb_breach: Section II.A.2, paragraph 31]. If you only noticed the theft on Monday morning, the 72-hour countdown typically starts from that point of awareness on Monday, provided you did not have earlier alerts that you failed to act upon in a timely manner [edpb_breach: Section II.A.2, paragraph 40]. 

This notification is required unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons [gdpr: Article 33, paragraph 1, edpb_breach: Section II.A.1, paragraph 29]. During the 72-hour window, you are expected to assess the likely risk to individuals to determine if notification is triggered [edpb_breach: Section II.A.2, paragraph 35]. If you cannot notify within 72 hours, you must provide the reasons for the delay along with the notification [gdpr: Article 33, paragraph 1, edpb_breach: Section II.A.1, paragraph 29].
```

**Citation check (code):** not found in the retrieved passages: [gdpr: Article 33, paragraph 1, edpb_breach: Section II.A.1, paragraph 29]

<details><summary>Passages the agent retrieved</summary>

```text
Search: notify personal data breach authority time limit without undue delay 72 hours discovery

5 closest passages for: notify personal data breach authority time limit without undue delay 72 hours discovery

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 85, page 16 | similarity 0.80
(85) A personal data breach may, if not addressed in an appropriate and timely manner, result in physical, material or non-material damage to natural persons such as loss of control over their personal data or limitation of their rights, discrimination, identity theft or fraud, financial loss, unauthorised reversal of pseudonymisation, damage to reputation, loss of confidentiality of personal data protected by professional secrecy or any other significant economic or social disadvantage to the natural person concerned. Therefore, as soon as the controller becomes aware that a personal data breach has occurred, the controller should notify the personal data breach to the supervisory authority without undue delay and, where feasible, not later than 72 hours after having become aware of it, unless the controller is able to demonstrate, in accordance with the accountability principle, that the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where such notification cannot be achieved within 72 hours, the reasons for the delay should accompany the notification and information may be provided in phases without undue further delay.

[2] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraphs 40-41, page 13 | similarity 0.78
Heading: When does a controller become “aware”?
40. Accordingly, it should be clear that there is an obligation on the controller to act on any initial alert and establish whether or not a breach has, in fact, occurred. This brief period allows for some investigation, and for the controller to gather evidence and other relevant details. However, once the controller has established with a reasonable degree of certainty that a breach has occurred, if the conditions in Article 33(1) GDPR have been met, it must then notify the supervisory authority without undue delay and, where feasible, not later than 72 hours27. If a controller fails to act in a timely manner and it becomes apparent that a bre ach did occur, this could be considered as a failure to notify in accordance with Article 33 GDPR. 41. Article 32 GDPR makes clear that the controller and processor should have appropriate technical and organisational measures in place to ensure an appropriate level of security of personal data: the ability to detect, address, and report a breach in a timely manner should be seen as essential elements of these measures.

[3] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.1, page 10 | similarity 0.78
Heading: Article 33 requirements
29. Article 33(1) GDPR provides that: “In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority competent in accordance with Article 55, unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where the notification to the supervisory authority is not made within 72 hours, it shall be accompanied by reasons for the delay.” 30. Recital 87 GDPR states23: “It should be ascertained whether all appropriate techno logical protection and organisational measures have been implemented to establish immediately whether a personal data breach has taken place and to inform promptly the supervisory authority and the data subject. The fact that the notification was made without undue delay should be established taking into account in particular the nature and gravity of the personal data breach and its consequences and adverse effects for the data subject. Such notification may result in an intervention of the supervisory authority in accordance with its tasks and powers laid down in this Regulation.”

[4] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraph 35, page 12 | similarity 0.77
Heading: When does a controller become “aware”?
35. Once the controller has become aware, a notifiable breach must be notified without undue delay, and where feasible, not later than 72 hours. During this period, the controller should assess the likely risk to individuals in order to determine whether the requirement for notification has been triggered, as well as the action(s) needed to address the breach. However, a controller may already hav e an initial assessment of the potential risk that could result from a breach as part of a data protection impact assessment (DPIA) 25 made prior to carrying out the processing operation concerned. However, the DPIA may be more generalised in comparison to t he specific circumstances of any actual breach, and so in any event an additional assessment taking into account those circumstances will need to be made. For more detail on assessing risk, see section IV.

[5] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraphs 31-32, page 11 | similarity 0.76
Heading: When does a controller become “aware”?
31. As detailed above, the GDPR requires that, in the case of a breach, the controller shall notify the breach without undue delay and, where feasible, not later than 72 hours after having become aware of it. This may raise the question of when a controller can be considered to have become “aware” of a breach. The EDPB considers that a controller should be regarded as having become “aware” when that controller has a reasonable degree of certainty that a security incident has occurred that has led to personal data being compromised. 32. However, as indicated earlier, the GDPR requires the controller to implement all appropriate technical protection and organisational measures to establish immediately whether a breach has taken place and to inform promptly the supervisory authority and the data subjects. It also states that the fact that the notification was made without undue delay should be established taking into account in particular the nature and gravity of the breach and its consequences and adverse effects for the data subject 24. This puts an obligation on the controller to ensure that they will be “aware” of any breaches in a timely manner so that they can take appropriate action.

Search: when become aware data breach weekend detection monday

5 closest passages for: when become aware data breach weekend detection monday

[1] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraphs 33-34, page 11 | similarity 0.74
Heading: When does a controller become “aware”?
The controller checks its systems to establish whether personal data held on that system has been compromised and confirms this is the case. Once again, as t he controller now has clear evidence of a breach there can be no doubt that it has become “aware”. 4. A cybercriminal contacts the controller after having hacked its system in order to ask for a ransom. In that case, after checking its system to confirm it has been attacked the controller has clear evidence that a breach has occurred and there is no doubt that it has become aware. 34. After first being informed of a potential breach by an individual, a media organisation, or another source, or when it has itself detected a security incident, the controller may undertake a short period of investigation in order to establish whether or not a breach has in fact occurred. During this period of investigation the controller may not be regarded as being “aware”. However, it is expected that the initial investigation should begin as soon as possible and establish with a reasonable degree of certainty whether a breach has taken place; a more detailed investigation can then follow.

[2] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraph 39, page 13 | similarity 0.73
Heading: When does a controller become “aware”?
39. Whilst it is the responsibility of controllers and processors to put in place suitable measures to be able to prevent, react and address a breach, there are some practical steps that should be taken in all cases. • Information concerning all security -related events should be directed towards a responsible person or persons with the task of addressing incidents, establishing the existence of a breach and assessing risk. • Risk to individuals as a result of a breach should then be assessed (likelihood of no risk, risk or high risk), with relevant sections of the organisation being informed. • Notification to the supervisory authority, and potentially communication of the breach to the affected individuals should be made, if required. • At the same time, the controller should act to contain and recover the breach. Documentation of the breach should take place as it develops.

[3] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraphs 40-41, page 13 | similarity 0.73
Heading: When does a controller become “aware”?
40. Accordingly, it should be clear that there is an obligation on the controller to act on any initial alert and establish whether or not a breach has, in fact, occurred. This brief period allows for some investigation, and for the controller to gather evidence and other relevant details. However, once the controller has established with a reasonable degree of certainty that a breach has occurred, if the conditions in Article 33(1) GDPR have been met, it must then notify the supervisory authority without undue delay and, where feasible, not later than 72 hours27. If a controller fails to act in a timely manner and it becomes apparent that a bre ach did occur, this could be considered as a failure to notify in accordance with Article 33 GDPR. 41. Article 32 GDPR makes clear that the controller and processor should have appropriate technical and organisational measures in place to ensure an appropriate level of security of personal data: the ability to detect, address, and report a breach in a timely manner should be seen as essential elements of these measures.

[4] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraph 36, page 12 | similarity 0.73
Heading: When does a controller become “aware”?
36. In most cases these preliminary actions should be completed soon after the initial alert (i.e. when the controller or processor suspects there has been a security incident which may involve personal data.) – it should take longer than this only in exceptional cases. Example An individual informs the c ontroller that they have received an email impersonating the controller which contains personal data relating to his (actual) use of the controller’s service, suggesting that the security of the controller has been compromised. The controller conducts a short period of investigation and identifies an intrusion into their network and evidence of unauthorised access to personal data. The controller would now be considered as “aware” and notification to the supervisory authority is required unless this is unli kely to present a risk to the rights and freedoms of individuals. The controller will need to take appropriate remedial action to address the breach.

[5] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraphs 37-38, page 12 | similarity 0.72
Heading: When does a controller become “aware”?
37. The controller should therefore have internal processes in place to be able to detect and address a breach. For example, for finding some irregularities in data processing the controller or processor may use certain technical measures such as data flow and log analysers, from which is possible to define events and alerts by correlating any log data 26. It is im portant that when a breach is detected it is reported upwards to the appropriate level of management so it can be addressed and, if required, notified in accordance with Article 33 and, if necessary, Article 34. Such measures and reporting mechanisms could be detailed in the controller’s incident response plans and/or governance arrangements. These will help the controller to plan effectively and determine who has operational responsibility within the organisation for managing a breach and how or whether to escalate an incident as appropriate. 38. The controller should also have in place arrangements with any processors the controller uses, which themselves have an obligation to notify the controller in the event of a breach (see below).
```

</details>

---

## 9. q14 (unanswerable)

**Question:** I want to use a US email marketing company. Is there currently an adequacy decision covering transfers to the US, so I can send them customer data without extra safeguards?

**Reference answer:** The documents don't say which countries have adequacy decisions or what their current status is. They only describe how transfers work in general (Arts. 44-49: adequacy, safeguards, derogations). A correct answer should say the current status can't be confirmed from them and point the user to the Commission's published list or an adviser.

**Agent answer:**

```text
The documents do not state whether there is currently an adequacy decision covering the United States, nor do they name specific countries that have been granted adequacy. 

The texts explain that data can be transferred to a third country without specific authorisation if the European Commission has decided that the country, a territory, or a specified sector ensures an adequate level of protection [gdpr: Article 45, paragraph 1]. In the absence of such an adequacy decision, a transfer may only take place if appropriate safeguards are provided—such as standard data protection clauses adopted by the Commission, binding corporate rules, or approved codes of conduct—along with enforceable data subject rights and effective legal remedies [gdpr: Article 46, paragraphs 1-2, recital 108]. 

Because the provided documents do not list current adequacy decisions, you should consult your data protection authority or a lawyer to verify the current status of transfers to the US.
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: transfer United States adequacy decision safeguards EU US Data Privacy Framework

5 closest passages for: transfer United States adequacy decision safeguards EU US Data Privacy Framework

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 45, paragraph 1, page 61 | similarity 0.77
Heading: Transfers on the basis of an adequacy decision
1. A transfer of personal data to a third country or an international organisation may take place where the Commission has decided that the third country, a territory or one or more specified sectors within that third country, or the international organisation in question ensures an adequate level of protection. Such a transfer shall not require any specific authorisation.

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 46, paragraphs 1-2, page 62 | similarity 0.76
Heading: Transfers subject to appropriate safeguards
1. In the absence of a decision pursuant to Article 45(3), a controller or processor may transfer personal data to a third country or an international organisation only if the controller or processor has provided appropriate safeguards, and on condition that enforceable data subject rights and effective legal remedies for data subjects are available. 2. The appropriate safeguards referred to in paragraph 1 may be provided for, without requiring any specific authoris ation from a supervisory authority, by: (a) a legally binding and enforceable instrument between public authorities or bodies; (b) binding corporate rules in accordance with Article 47; (c) standard data protection clauses adopted by the Commission in accordance with the examination procedure referred to in Article 93(2); (d) standard data protection clauses adopted by a supervisory authority and approved by the Commission pursuant to the examination procedure referred to in Article 93(2); (e) an approved code of conduct pursuant to Article 40 together with binding and enforceable commitments of the controller or processor in the third country to apply the appropriate safeguards, including as regards data subjects' rights; or (f) an approved certification mechanism pursuant to Article 42 together with binding and enforceable commitments of the controller or processor in the third country to apply the appropriate safeguards, including as regards data subjects' rights.

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 108, page 20 | similarity 0.76
(108) In the absence of an adequacy decision, the controller or processor should take measures to compensate for the lack of data protection in a third country by way of appropriate safeguards for the data subject. Such appropriate safeguards may consist of making use of binding corporate rules, standard data protection clauses adopted by the Commission, standard data protection clauses adopted by a supervisory authority or contractual clauses authorised by a supervisory authority. Those safeguards should ensure compliance with data protection requirements and the rights of the data subjects appropriate to processing within the Union, including the availability of enforceable data subject rights and of effective legal remedies, including to obtain effective adminis trative or judicial redress and to claim compensation, in the Union or in a third country. They should relate in particular to compliance with the general principles relating to personal data processing, the principles of data protection by design and by default. Transfers may also be carried out by public authorities or bodies with public authorities or bodies in third countries or with international organisations with corresponding duties or functions, including on the basis of provisions to be inserted into administrative arrangements, such as a memorandum of understanding, providing for enforceable and effective rights for data subjects. Authorisation by the competent supervisory authority should be obtained when the safeguards are provided for in administrative arrangements that are not legally binding.

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 45, paragraph 2, page 61 | similarity 0.75
Heading: Transfers on the basis of an adequacy decision
2. When assessing the adequacy of the level of protection, the Commission shall, in particular, take account of the following elements: (a) the rule of law, respect for human rights and fundamental freedoms, relevant legislation, both general and sectoral, including concerning public security, defence, national security and criminal law and the access of public authorities to personal data, as well as the implementation of such legislation, data protection rules, professional rules and security measures, including rules for the onward transfer of personal data to another third country or international organisation which are complied with in that country or international organisation, case-law, as well as effective and enforceable data subject rights and effective administrative and judicial redress for the data subjects whose personal data are being transferred; (b) the existence and effective functioning of one or more independent supervisory authorities in the third country or to which an international organisation is subject, with responsibility for ensuring and enforcing compliance with the data protection rules, including adequate enforcement powers, for assisting and advising the data subjects in exercising their rights and for cooperation with the supervisory authorities of the Member States; and (c) the international commitments the third country or international organisation concerned has entered into, or other obligations arising from legally binding conventions or instruments as well as from its participation in multilateral or regional systems, in particular in relation to the protection of personal data.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 104, page 19 | similarity 0.74
(104) In line with the fundamental values on which the Union is founded, in particular the protection of human rights, the Commission should, in its assessment of the third country, or of a territory or specified sector within a third country, take into account how a particular third country respects the rule of law, access to justice as well as in ternational human rights norms and standards and its general and sectoral law, including legislation concerning public security, defence and national security as well as public order and criminal law. The adoption of an adequacy decision with regard to a territory or a specified sector in a third country should take into account clear and objective criteria, such as specific processing activities and the scope of applicable legal standards and legislation in force in the third country. The third country should offer guarantees ensuring an adequate level of protection essentially equivalent to that ensured within the Union, in particular where personal data are processed in one or several specific sectors. In particular, the third country should ensure effective independent data protection supervision and should provide for cooperation mechanisms with the Member States' data protection authorities, and the data subjects should be provided with effective and enforceable rights and effective administrative and judicial redress.
```

</details>

---

## 10. q09 (multi)

**Question:** I run an online game app that is popular with teenagers, and I want to ask users for consent to send them marketing. A user says he is 15. Can he consent himself?

**Reference answer:** It depends on the age set in national law. Article 8(1) sets 16 as the default for consent to information society services offered directly to a child. Member States may lower it, but not below 13. Below the applicable age, you need consent from the holder of parental responsibility and must make reasonable efforts to verify it (Art. 8(2)). The guidelines add that a cross-border service may need to follow each Member State's age where it offers the service. The documents don't say what the age is in any particular country, so the answer for a 15-year-old can't be given from them alone.

**Agent answer:**

```text
Whether a 15-year-old can consent depends on the digital age of consent set by the law of the specific Member State where the user resides. 

Under the GDPR, when offering online services directly to children based on consent, processing is lawful if the child is at least 16 years old. However, individual Member States are allowed by law to lower this age for these purposes, provided that the lower age is not below 13. If a user is below the applicable age of digital consent, processing is lawful only if and to the extent that consent is given or authorised by the holder of parental responsibility over the child [gdpr: Article 8, paragraph 1]. 

Because digital consent rules can vary between countries, you must check the specific national law of the country where the 15-year-old user resides [edpb_consent: Section 7.1.3, paragraphs 131-132]. If that country has set the age of digital consent at 15 or lower (for example, 13, 14, or 15), the user can consent himself. If that country has set the age at 16, a parent or guardian must give or authorise the consent, and you must make reasonable efforts to verify this using available technology [gdpr: Article 8, paragraphs 1-2].
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: consent child age information society services 15

5 closest passages for: consent child age information society services 15

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 8, page 37 | similarity 0.80
Heading: Conditions applicable to child's consent in relation to information society services
1. Where point (a) of Article 6(1) applies, in relation to the offer of information society services directly to a child, the processing of the personal data of a child shall be lawful where the child is at least 16 years old. Where the child is below the age of 16 years, such processing shall be lawful only if and to the extent that consent is given or authorised by the holder of parental responsibility over the child. Member States may provide by law for a lower age for those purposes provided that such lower age is not below 13 years. 2. The controller shall make reasonable efforts to verify in such cases that consent is given or authorised by the holder of parental responsibility over the child, taking into consideration available technology. 3. Paragraph 1 shall not affect the general contract law of Member States such as the rules on the validity, formation or effect of a contract in relation to a child.

[2] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 7.1, paragraphs 125-127, page 26 | similarity 0.79
Heading: Children (Article 8)
125. Article 8(1) states that where consent applies, in relation to the offer of information society services directly to a child, the processing of the personal data of a child shall be lawful where the child is at least 16 years old. Where the child is below the age of 16 years, such processing shall be lawful only if and to the extent that consent is given or authorised by the holder of parental responsibility over the child.60 Regarding the age limit of valid consent the GDPR provides flexibility, Mem ber States can provide by law a lower age, but this age cannot be below 13 years. 126. As mentioned in section 3.1. on informed consent, the information shall be understandable to the audience addressed by the controller, paying particular attention to the posi tion of children. In order to obtain “informed consent” from a child, the controller must explain in language that is clear and plain for children how it intends to process the data it collects. 61 If it is the parent that is supposed to consent, then a set of information may be required that allows adults to make an informed decision. 127. It is clear from the foregoing that Article 8 shall only apply when the following conditions are met:  The processing is related to the offer of information society services directly to a child.62, 63  The processing is based on consent.

[3] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 7.1.4, paragraphs 139-144, page 28 | similarity 0.76
Heading: Children’s consent and parental responsibility
139. Step 1: ask the user to state whether they are under or over the age of 16 (or alternative age of digital consent) If the user states that they are under the age of digital consent: 140. Step 2: service informs the child that a parent or guardian needs to consent or authorise the processing before the service is provided to the child. The user is requested to disclose the email address of a parent or guardian. 141. Step 3: service contacts the parent or guardian and obtains their consent via email for processing and take reasonable steps to confirm that the adult has parental responsibility. 142. Step 4: in case of complaints, the platform takes additional steps to verify the age of the subscriber. 143. If the platform has met the other consent requirements, the platform can comply with the additional criteria of Article 8 GDPR by following these steps. 144. The example shows that the controller can put itself in a position to show that reasonable efforts have been made to ensure that valid consent has been obtained, in relation to the services provided to a child. Article 8(2) particularly adds that “ The controller shall make reasonable efforts to verify that consent is given or authorised by the holder of parental responsibility over the child, taking into consideration available technology.”

[4] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 7.1.3, paragraphs 131-132, page 27 | similarity 0.76
Heading: Age
131. The GDPR specifies that “Member States may provide by law for a lower age for those purposes provided that such lower age is not below 13 years.” The controller must be aware of those different national laws, by taking into account the public targeted by its services. Inparticular, it should be noted that a controller providing a cross-border service cannot always rely on complying with only the lawof the Member State in which it has its main establishment but may need to comply with the respective national laws of each Member State in which it offers the information society service(s). This depends on whether a Member State chooses to use the placeof main establishment of the controller as a point of reference in its national law, or the residence of the data subject. First of all the Member States shall consider the best interests of the child during making their choice. The Working Group encourages the Member States to search for a harmonized solution in this matter. 132. When providing information society services to children on the basis of consent, controllers will be expected to make reasonable efforts to verify that the user is over the age of digital consent, and these measures should be proportionate to the nature and risks of the processing activities.

[5] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 7.1.4, paragraphs 145-148, page 29 | similarity 0.75
Heading: Children’s consent and parental responsibility
145. It is up to the controller to determine what measures are appropriate in a specific case. As a general rule, controllers should avoid verification solutions which themselves involve excessive collection of personal data. 146. The EDPB acknowledges that there may be cases where verification is challenging (for example where children providing their own consent have not yet established an ‘identity footprint’, or where parental responsibility is not easily checked. This can be taken into a ccount when deciding what efforts are reasonable, but controllers will also be expected to keep their processes and the available technology under constant review. 147. With regard to the data subject’s autonomy to consent to the processing of their personal da ta and have full control over the processing, consent by a holder of parental responsibility or authorized by a holder of parental responsibility for the processing of personal data of children can be confirmed, modified or withdrawn, once the data subject reaches the age of digital consent. 148. In practice, this means that if the child does not take any action, consent given by a holder of parental responsibility or authorized by a holder of parental responsibility for the processing of personal data given prior to the age of digital consent, will remain a valid ground for processing.
```

</details>

---

## 11. q28 (single)

**Question:** Our IT contractor thinks someone may have got into our customer database, but they're still checking. When does my 72-hour clock start?

**Reference answer:** The clock starts when you become 'aware' of the breach, which the guidelines define as having a reasonable degree of certainty that a security incident has occurred that has led to personal data being compromised. After an initial alert you may carry out a short period of investigation to establish whether a breach has really occurred. During that short period you are not regarded as aware. The investigation must begin as soon as possible and be quick, and a more detailed investigation can follow later. Once you have reasonable certainty, for example clear evidence of unauthorised access, you are aware and the 72 hours run. A controller that fails to act in a timely manner on an alert risks being treated as having failed to notify.

**Agent answer:**

```text
Your 72-hour clock does not necessarily start the exact moment your IT contractor flags a suspicion or an initial alert. You are considered to have become "aware"—and your 72-hour clock begins—once you have established **with a reasonable degree of certainty** that a security incident has occurred and that personal data has actually been compromised [edpb_breach: Section II.A.2, paragraphs 31, 40].

The guidelines allow for a brief period of investigation after an initial alert so that you can gather evidence, check your systems, and confirm whether a breach has in fact taken place [edpb_breach: Section II.A.2, paragraphs 34, 40]. These preliminary actions and investigations should be completed soon after the initial alert [edpb_breach: Section II.A.2, paragraph 36]. 

However, you have an obligation to act on initial alerts promptly and ensure your systems allow you to detect and address incidents in a timely manner [edpb_breach: Section II.A.2, paragraphs 32, 40]. Failing to act quickly to investigate an alert when it becomes apparent a breach did occur can be treated as a failure to notify [edpb_breach: Section II.A.2, paragraph 40].

### Sources:
- [gdpr: Recital 85]
- [edpb_breach: Section II.A.1, paragraphs 29-30]
- [edpb_breach: Section II.A.2, paragraphs 31-36, 40-41]
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: 72 hour clock start personal data breach notification guidelines breach notification

5 closest passages for: 72 hour clock start personal data breach notification guidelines breach notification

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 85, page 16 | similarity 0.77
(85) A personal data breach may, if not addressed in an appropriate and timely manner, result in physical, material or non-material damage to natural persons such as loss of control over their personal data or limitation of their rights, discrimination, identity theft or fraud, financial loss, unauthorised reversal of pseudonymisation, damage to reputation, loss of confidentiality of personal data protected by professional secrecy or any other significant economic or social disadvantage to the natural person concerned. Therefore, as soon as the controller becomes aware that a personal data breach has occurred, the controller should notify the personal data breach to the supervisory authority without undue delay and, where feasible, not later than 72 hours after having become aware of it, unless the controller is able to demonstrate, in accordance with the accountability principle, that the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where such notification cannot be achieved within 72 hours, the reasons for the delay should accompany the notification and information may be provided in phases without undue further delay.

[2] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraphs 40-41, page 13 | similarity 0.76
Heading: When does a controller become “aware”?
40. Accordingly, it should be clear that there is an obligation on the controller to act on any initial alert and establish whether or not a breach has, in fact, occurred. This brief period allows for some investigation, and for the controller to gather evidence and other relevant details. However, once the controller has established with a reasonable degree of certainty that a breach has occurred, if the conditions in Article 33(1) GDPR have been met, it must then notify the supervisory authority without undue delay and, where feasible, not later than 72 hours27. If a controller fails to act in a timely manner and it becomes apparent that a bre ach did occur, this could be considered as a failure to notify in accordance with Article 33 GDPR. 41. Article 32 GDPR makes clear that the controller and processor should have appropriate technical and organisational measures in place to ensure an appropriate level of security of personal data: the ability to detect, address, and report a breach in a timely manner should be seen as essential elements of these measures.

[3] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraph 35, page 12 | similarity 0.76
Heading: When does a controller become “aware”?
35. Once the controller has become aware, a notifiable breach must be notified without undue delay, and where feasible, not later than 72 hours. During this period, the controller should assess the likely risk to individuals in order to determine whether the requirement for notification has been triggered, as well as the action(s) needed to address the breach. However, a controller may already hav e an initial assessment of the potential risk that could result from a breach as part of a data protection impact assessment (DPIA) 25 made prior to carrying out the processing operation concerned. However, the DPIA may be more generalised in comparison to t he specific circumstances of any actual breach, and so in any event an additional assessment taking into account those circumstances will need to be made. For more detail on assessing risk, see section IV.

[4] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.1, page 10 | similarity 0.76
Heading: Article 33 requirements
29. Article 33(1) GDPR provides that: “In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority competent in accordance with Article 55, unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where the notification to the supervisory authority is not made within 72 hours, it shall be accompanied by reasons for the delay.” 30. Recital 87 GDPR states23: “It should be ascertained whether all appropriate techno logical protection and organisational measures have been implemented to establish immediately whether a personal data breach has taken place and to inform promptly the supervisory authority and the data subject. The fact that the notification was made without undue delay should be established taking into account in particular the nature and gravity of the personal data breach and its consequences and adverse effects for the data subject. Such notification may result in an intervention of the supervisory authority in accordance with its tasks and powers laid down in this Regulation.”

[5] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraphs 31-32, page 11 | similarity 0.75
Heading: When does a controller become “aware”?
31. As detailed above, the GDPR requires that, in the case of a breach, the controller shall notify the breach without undue delay and, where feasible, not later than 72 hours after having become aware of it. This may raise the question of when a controller can be considered to have become “aware” of a breach. The EDPB considers that a controller should be regarded as having become “aware” when that controller has a reasonable degree of certainty that a security incident has occurred that has led to personal data being compromised. 32. However, as indicated earlier, the GDPR requires the controller to implement all appropriate technical protection and organisational measures to establish immediately whether a breach has taken place and to inform promptly the supervisory authority and the data subjects. It also states that the fact that the notification was made without undue delay should be established taking into account in particular the nature and gravity of the breach and its consequences and adverse effects for the data subject 24. This puts an obligation on the controller to ensure that they will be “aware” of any breaches in a timely manner so that they can take appropriate action.

Search: when does controller become aware processor IT contractor breach guidelines

5 closest passages for: when does controller become aware processor IT contractor breach guidelines

[1] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraph 36, page 12 | similarity 0.83
Heading: When does a controller become “aware”?
36. In most cases these preliminary actions should be completed soon after the initial alert (i.e. when the controller or processor suspects there has been a security incident which may involve personal data.) – it should take longer than this only in exceptional cases. Example An individual informs the c ontroller that they have received an email impersonating the controller which contains personal data relating to his (actual) use of the controller’s service, suggesting that the security of the controller has been compromised. The controller conducts a short period of investigation and identifies an intrusion into their network and evidence of unauthorised access to personal data. The controller would now be considered as “aware” and notification to the supervisory authority is required unless this is unli kely to present a risk to the rights and freedoms of individuals. The controller will need to take appropriate remedial action to address the breach.

[2] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraphs 37-38, page 12 | similarity 0.82
Heading: When does a controller become “aware”?
37. The controller should therefore have internal processes in place to be able to detect and address a breach. For example, for finding some irregularities in data processing the controller or processor may use certain technical measures such as data flow and log analysers, from which is possible to define events and alerts by correlating any log data 26. It is im portant that when a breach is detected it is reported upwards to the appropriate level of management so it can be addressed and, if required, notified in accordance with Article 33 and, if necessary, Article 34. Such measures and reporting mechanisms could be detailed in the controller’s incident response plans and/or governance arrangements. These will help the controller to plan effectively and determine who has operational responsibility within the organisation for managing a breach and how or whether to escalate an incident as appropriate. 38. The controller should also have in place arrangements with any processors the controller uses, which themselves have an obligation to notify the controller in the event of a breach (see below).

[3] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraphs 31-32, page 11 | similarity 0.82
Heading: When does a controller become “aware”?
31. As detailed above, the GDPR requires that, in the case of a breach, the controller shall notify the breach without undue delay and, where feasible, not later than 72 hours after having become aware of it. This may raise the question of when a controller can be considered to have become “aware” of a breach. The EDPB considers that a controller should be regarded as having become “aware” when that controller has a reasonable degree of certainty that a security incident has occurred that has led to personal data being compromised. 32. However, as indicated earlier, the GDPR requires the controller to implement all appropriate technical protection and organisational measures to establish immediately whether a breach has taken place and to inform promptly the supervisory authority and the data subjects. It also states that the fact that the notification was made without undue delay should be established taking into account in particular the nature and gravity of the breach and its consequences and adverse effects for the data subject 24. This puts an obligation on the controller to ensure that they will be “aware” of any breaches in a timely manner so that they can take appropriate action.

[4] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraphs 33-34, page 11 | similarity 0.82
Heading: When does a controller become “aware”?
The controller checks its systems to establish whether personal data held on that system has been compromised and confirms this is the case. Once again, as t he controller now has clear evidence of a breach there can be no doubt that it has become “aware”. 4. A cybercriminal contacts the controller after having hacked its system in order to ask for a ransom. In that case, after checking its system to confirm it has been attacked the controller has clear evidence that a breach has occurred and there is no doubt that it has become aware. 34. After first being informed of a potential breach by an individual, a media organisation, or another source, or when it has itself detected a security incident, the controller may undertake a short period of investigation in order to establish whether or not a breach has in fact occurred. During this period of investigation the controller may not be regarded as being “aware”. However, it is expected that the initial investigation should begin as soon as possible and establish with a reasonable degree of certainty whether a breach has taken place; a more detailed investigation can then follow.

[5] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraph 33 (part 1 of 2), page 11 | similarity 0.82
Heading: When does a controller become “aware”?
33. When, exactly, a controller can be considered to be “aware” of a particular breach will depend on the circumstances of the specific breach. In some cases, it will be relatively clear from the outset that there has been a breach, whereas in others, it may take some time to establish if personal data have been compromised. However, the emphasis should be on prompt action to investigate an incident to determine whether personal data have indeed been breached, and if so, to take remedial action and notify if required. Examples 1. In the case of a loss of a USB key with unencrypted personal data it is often not possible to ascertain whether unauthorised persons gained access to that data. Nevertheless, even though the controller may not be able to establish if a confidentiality brea ch has taken place, such a case has to be notified as there is a reasonable degree of certainty that an availability breach has occurred; the controller would become “aware” when it realised the USB key had been lost. 2. A third party informs a controller that they have accidentally received the personal data of one of its customers and provides evidence of the unauthorised disclosure. As the controller has been presented with clear evidence of a confidentiality breach then there can be no doubt that it ha s become “aware”. 3. A controller detects that there has been a possible intrusion into its network.
```

</details>

---

## 12. q23 (single)

**Question:** We had a breach and I'd rather not email all our customers about it. Are there cases where I don't have to tell them?

**Reference answer:** Yes, but only where a communication to individuals would otherwise be required (high risk). There are three conditions, and meeting any one is enough: you had applied appropriate protection before the breach that makes the data unintelligible to unauthorised people, for example state-of-the-art encryption or tokenisation; immediately after the breach you took steps so that the high risk is no longer likely to materialise; or contacting people would involve disproportionate effort, for example because contact details were lost, in which case you must make a public communication or similar measure that informs people in an equally effective manner. You must be able to demonstrate that a condition is met. The authority can still require you to inform individuals if it considers the breach likely to cause high risk, and it may use its powers if your decision not to notify is not well founded. The risk must be re-evaluated over time, because it can change.

**Agent answer:**

```text
Yes, you do not have to notify your customers if any of the following conditions are met:

1. **The data was protected so no one could read it:** You applied appropriate technical and organisational measures (such as state-of-the-art encryption or tokenisation) prior to the breach that rendered the affected personal data unintelligible to anyone not authorized to access it [gdpr: Article 34(3)(a); edpb_breach: Section III.D, paragraph 97].
2. **The high risk is no longer likely to happen:** Immediately following the breach, you took steps that ensure the high risk to your customers' rights and freedoms is no longer likely to materialize (for example, if you immediately caught the unauthorized person and recovered the data before they could use it) [gdpr: Article 34(3)(b); edpb_breach: Section III.D, paragraph 97].
3. **It would involve disproportionate effort:** Contacting every customer would require disproportionate effort. In this case, you must instead make a public communication or take a similar measure that informs individuals in an equally effective manner (such as making information available on demand) [gdpr: Article 34(3)(c); edpb_breach: Section III.D, paragraph 97].
4. **There is no high risk:** You only need to communicate a breach to individuals if the breach is *likely to result in a high risk* to their rights and freedoms [gdpr: Article 34(1)]. 

Additionally, you must be able to demonstrate to your supervisory authority that one of these exemption conditions has been met. Note that even if you decide not to notify your customers, the supervisory authority can still require you to do so if it believes the risk is high [edpb_breach: Section III.D, paragraphs 98-99].
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: communication of a personal data breach to the data subject exemptions

5 closest passages for: communication of a personal data breach to the data subject exemptions

[1] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section III.D, paragraph 97 (part 1 of 2), page 22 | similarity 0.78
Heading: Conditions where communication is not required
97. Article 34(3) GDPR states three conditions that, if met, do not require notification to individuals in the event of a breach. These are: • The controller has applied appropriate technical and organisational measures to protect personal data prior to the breach, in particular those measures that render personal data unintelligible to any person who is not authorised to access it. This could, for example, include protecting personal data with state-of-the-art encryption, or by tokenization. • Immediately following a breach, the controller has taken steps to ensure that the high risk posed to individuals’ rights and freedoms is no longer likely to materialise. For example, depending on the circumstances of the case, the controller may h ave immediately identified and taken action against the individual who has accessed personal data before they were able to do anything with it. Due regard still needs to be given to the possible consequences of any breach of confidentiality, again, depending on the nature of the data concerned. • It would involve disproportionate effort41 to contact individuals, perhaps where their contact details have been lost as a result of the breach or are not known in the first place. For example, the warehouse of a statistical office has flooded and the documents containing personal data were stored only in paper form. Instead, the controller must make a public communication or take a similar measure, whereby the individuals are informed in an equally effective manner.

[2] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.D, paragraphs 75-76, page 18 | similarity 0.78
Heading: Conditions where notification is not required
75. Article 33(1) GDPR makes it clear that breaches that are “unlikely to result in a risk to the rights and freedoms of natural persons” do not require notification to the supervisory authority. An example might be where personal data are already publically available and a disc losure of such data does not constitute a likely risk to the individual. This is in contrast to existing breach notification requirements for providers of publically available electronic communications services in Directive 2009/136/EC that state all relevant breaches have to be notified to the competent authority. 76. In its Opinion 03/2014 on breach notification 38 , WP29 explained that a confidentiality breach of personal data that were encrypted with a state of the art algorithm is still a personal data breach, and has to be notified. However, if the confidentiality of the key is intact – i.e., the key was not compromised in any security breach, and was generated so that it cannot be ascertained by available technical means by any person who is not authorised to access it – then the data are in principle unintelligible. Thus, the breach is unlikely to adversely affect individuals and therefore would not require communication to those individuals 39 . However, even where data is encrypted, a loss or alteration can have negative consequences for data subjects where the controller has no adequate backups. In that instance communication to data subjects would be required, even if the data itself was subject to adequate encryption measures.

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 34, paragraphs 1-3, page 52 | similarity 0.77
Heading: Communication of a personal data breach to the data subject
1. When the personal data breach is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall communicate the personal data breach to the data subject without undue delay. 2. The communication to the data subject referred to in paragraph 1 of this Article shall describe in clear and plain language the nature of the personal data breach and contain at least the information and measures referred to in points (b), (c) and (d) of Article 33(3). 3. The communication to the data subject referred to in paragraph 1 shall not be required if any of the following conditions are met: (a) the controller has implemented appropriate technical and organisational protection measures, and those measures were applied to the personal data affected by the personal data breach, in particular those that render the personal data unintelligible to any person who is not authorised to access it, such as encryption; (b) the controller has taken subsequent measures which ensure that the high risk to the rights and freedoms of data subjects referred to in paragraph 1 is no longer likely to materialise; (c) it would involve disproportionate effort. In such a case, there shall instead be a public communication or similar measure whereby the data subjects are informed in an equally effective manner.

[4] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section III.D, paragraphs 97-99, page 22 | similarity 0.76
Heading: Conditions where communication is not required
In the case of disproportionate effort, technical arrangements could also be envisaged to make information about the breach available on demand, which could prove useful to those individuals who may be affected by a breach, but the controller cannot otherwise contact. 98. In accordance with the accountability principle controllers should be able to demonstrate to the supervisory authority that they meet one or more of these conditions 42. It should be borne in mind that while notification may initially not be required if there is no risk to the rights and freedoms of natural persons, this may change over time and the risk would have to be re-evaluated. 99. If a controller decides not to communicate a breach to the individual, Article 34(4) GDPR explains that the supervisory authority can require it to do so, if it considers the breach is likely to result in a high risk to individuals. Alternatively, it may consider that the conditions in Articl e 34(3) GDPR have been met in which case notification to individuals is not required. If the supervisory authority determines that the decision not to notify data subjects is not well founded, it may consider employing its available powers and sanctions.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 86, page 17 | similarity 0.76
(86) The controller should communicate to the data subject a personal data breach, without undue delay, where that personal data breach is likely to result in a high risk to the rights and freedoms of the natural person in order to allow him or her to take the necessary precautions. The communication should describe the nature of the personal data breach as well as recommendations for the natural person concerned to mitigate potential adverse effects. Such communications to data subjects should be made as soon as reasonably feasible and in close cooperation with the supervisory authority, respecting guidance provided by it or by other relevant authorities such as law-enforcement authorities. For example, the need to mitigate an immediate risk of damage would call for prompt communication with data subjects whereas the need to implement appropriate measures against continuing or similar personal data breaches may justify more time for communication.
```

</details>

---

## 13. q27 (multi)

**Question:** I'm writing the consent text for my newsletter sign-up form. What qualities must the consent have, and what is the minimum information I have to give people before they tick the box?

**Reference answer:** Under Article 4(11), consent must be freely given, specific, informed and unambiguous, expressed by a statement or a clear affirmative action. For consent to be informed, the guidelines say the person must be told at least: the controller's identity; the purpose of each processing operation for which consent is sought; what type of data will be collected and used; the existence of the right to withdraw consent; where relevant, the use of the data for automated decision-making under Art. 22(2)(c); and where relevant, the possible risks of data transfers due to the absence of an adequacy decision and appropriate safeguards. If other controllers will rely on the consent, they must all be named. Processors do not need to be named in the consent request.

**Agent answer:**

```text
For consent to be valid, it must have four key qualities:
1. **Freely given**: Individuals must have a genuine choice and control, and cannot be forced or penalized for refusing.
2. **Specific**: It must be specific to the particular processing purpose and granular (separate consents for separate things).
3. **Informed**: Individuals must receive clear information before deciding.
4. **Unambiguous**: It must be given by a statement or a clear affirmative action (such as actively ticking an un-ticked box). Pre-ticked boxes, silence, inactivity, or bundling consent into general terms and conditions are not valid.

Before someone ticks the box, you must at least provide the following minimum information for consent to be considered "informed":
- The controller’s identity.
- The purpose of each processing operation for which consent is sought.
- What types of data will be collected and used.
- The existence of the right to withdraw consent at any time.
- Information about automated decision-making under Article 22(2)(c), where relevant.
- Information on the possible risks of data transfers to countries outside the EEA where there is no adequacy decision or appropriate safeguards.

Sources:
- [edpb_consent: Section 3, page 7]
- [edpb_consent: Section 3.3.1, paragraph 64]
- [edpb_consent: Section 3.4, paragraphs 79-81]
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: conditions for consent valid freely given specific informed unambiguous

5 closest passages for: conditions for consent valid freely given specific informed unambiguous

[1] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3, page 7 | similarity 0.74
Heading: Elements Of Valid Consent
11. Article 4(11) of the GDPR stipulates that consent of the data subject means any:  freely given,  specific,  informed and  unambiguous indication of the data subject's wishes by which he or she, by a statement or by a clear affirmative action, signifies agreement to the proc essing of personal data relating to him or her. 12. In the sections below, it is analysed to what extent the wording of Article 4(11) requires controllers to change their consent requests/forms, in order to ensure compliance with the GDPR.11

[2] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.4, paragraphs 75-78, page 18 | similarity 0.72
Heading: Unambiguous indication of wishes
75. The GDPR is clear that consent requires a sta tement from the data subject or a clear affirmative act, which means that it must always be given through an active motion or declaration. It must be obvious that the data subject has consented to the particular processing. 76. Article 2(h) of Directive 95/46/ EC described consent as an “indication of wishes by which the data subject signifies his agreement to personal data relating to him being processed”. Article 4(11) GDPR builds on this definition, by clarifying that valid consent requires anunambiguous indication by means of a statement or by a clear affirmative action, in line with previous guidance issued by the WP29. 77. A “clear affirmative act” means that the data subject must have taken a deliberate action to consent to the particular processing.43 Recital 32 sets out additional guidance on this. Consent can be collected through a written or (a recorded) oral statement, including by electronic means. 78. Perhaps the most literal way to fulfil the criterion of a “written statement” is to make sure a data subject writes in a letter or types an email to the controller explaining what exactly he/she agrees to. However, this is often not realistic. Written statements can come in many shapes and sizes that could be compliant with the GDPR.

[3] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.4, paragraphs 79-81, page 18 | similarity 0.72
Heading: Unambiguous indication of wishes
79. Without prejudice to existing (national) contract law, consent can be obtained through a recorded oral statement, although due note must be taken of the information available to the data subject, prior to the indication of consent. The use of pre -ticked opt-in boxes is invalid under the GDPR. Silence or inactivity on the part of the data subject, as well as merely proceeding with a service cannot be regarded as an active indication of choice. 80. Example 14: When installing software, the application asks the data subject for consent to us e nonanonymised crash reports to improve the software. A layered privacy notice providing the necessary information accompanies the request for consent. By actively ticking the optional box stating, “I consent”, the user is able to validly perform a ´clear affirmative act´ to consent to the processing. 81. A controller must also beware that consent cannot be obtained through the same motion as agreeing to a contract or accepting general terms and conditions of a service. Blanket acceptance of general terms and conditions cannot be seen as a clear affirmative action to consent to the use of personal data. The GDPR does not allow controllers to offer pre -ticked boxes or opt -out constructions that require an intervention from the data subject to prevent agreement (for example ‘opt-out boxes’).44

[4] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.3.1, paragraph 64, page 15 | similarity 0.72
Heading: Minimum content requirements for consent to be ‘informed’
64. For consent to be informed, it is necessary to inform the data subject of certain elements that are crucial to make a choice. Therefore, the EDPB is of the opinion that at least the following information is required for obtaining valid consent: i. the controller’s identity, 32 ii. the purpose of each of the processing operations for which consent is sought,33 iii. what (type of) data will be collected and used, 34 iv. the existence of the right to withdraw consent,35 v. information about the use of the data for automated decision -making in accordance with Article 22 (2)(c)36 where relevant, and vi. on the possible risks of data t ransfers due to absence of an adequacy decision and of appropriate safeguards as described in Article 46.37

[5] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 2, page 6 | similarity 0.71
Heading: Consent In Article 4(11) Of The GDPR
8. Article 4(11) of the GDPR defines consent as: “any freely given, specific, informed and unambiguous indication of the data subject's wishes by which he or she, by a statement or by a clear affirmative action, signifies agreement to the processing of personal data relating to him or her.” 9. The basic concept of consent remains similar to that under the Directive 95/46/EC and consent is one of the lawful grounds on which personal data processing has to be based, pursuant to Article 6 of the GDPR.10 Besides the amended definition in Article 4(11), the GDPR provides additional guidance in Article 7 and in recitals 32, 33, 42, and 43 as to how the controller must act to comply with the main elements of the consent requirement. 10. Finally, the inclusion of specific provisions and recitals on the withdrawal of consent confirms that consent should be a reversible decision and that there remains a degree of control on the side of the data subject.
```

</details>

---

## 14. q15 (unanswerable)

**Question:** How long do I have to keep invoices that contain customer names and addresses to satisfy Spanish tax rules?

**Reference answer:** The documents don't cover this. They say data should not be kept longer than necessary and that a legal obligation can justify retention, but they name no tax or accounting retention period. A correct answer should say so and refer to Spanish tax rules, not give a number of years.

**Agent answer:**

```text
The documents do not cover specific retention periods under national tax rules, such as Spanish tax law. The provided documents focus on the EU GDPR and EDPB guidelines, which do not specify time limits for keeping invoices. 

For questions regarding tax obligations and retention periods required by local authorities, you should consult a lawyer or your local data protection authority.
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: Spanish tax rules invoices retention period

5 closest passages for: Spanish tax rules invoices retention period

[1] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section V.A, paragraphs 124-125, page 26 | similarity 0.65
Heading: Documenting breaches
124. The GDPR does not specify a retention period for such documentation. Where such records contain personal data, it will be incumbent on the controller to de termine the appropriate period of retention in accordance with the principles in relation to the processing of personal data48 and to meet a lawful basis for processing 49. It will need to retain documentation in accordance with Article 33(5) GDPR insofar as it may be called to provide evidence of compliance with that Article, or with the accountability principle more generally, to the supervisory authority. Clearly, if the records themselves contain no personal data then the storage limitation principle50 of the GDPR does not apply. 125. In addition to these details, the EDPB recommends that the controller also document its reasoning for the decisions taken in response to a breach. In particular, if a breach is not notified, a justification for that decision should be documented. This should include reasons why the controller considers the breach is unlikely to result in a risk to the rights and freedoms of individuals 51 . Alternatively, if the controller considers that any of the conditions in Article 34(3) GDPR are met, then it should be able to provide appropriate evidence that this is the case.

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 30, paragraph 1, page 50 | similarity 0.64
Heading: Records of processing activities
1. Each controller and, where applicable, the controller's representative, shall maintain a record of processing activities under its responsibility. That record shall contain all of the following information: (a) the name and contact details of the controller and, where applicable, the joint controller, the controller's representa tive and the data protection officer; (b) the purposes of the processing; (c) a description of the categories of data subjects and of the categories of personal data; (d) the categories of recipients to whom the personal data have been or will be disclosed including recipients in third countries or international organisations; (e) where applicable, transfers of personal data to a third country or an international organisation, including the identifi cation of that third country or international organisation and, in the case of transfers referred to in the second subparagraph of Article 49(1), the documentation of suitable safeguards; (f) where possible, the envisaged time limits for erasure of the different categories of data; (g) where possible, a general description of the technical and organisational security measures referred to in Article 32(1).

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 17, paragraph 1, page 43 | similarity 0.64
Heading: Right to erasure (‘right to be forgotten’)
1. The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay and the controller shall have the obligation to erase personal data without undue delay where one of the following grounds applies: (a) the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed; (b) the data subject withdraws consent on which the processing is based according to point (a) of Article 6(1), or point (a) of Article 9(2), and where there is no other legal ground for the processing; (c) the data subject objects to the processing pursuant to Article 21(1) and there are no overriding legitimate grounds for the processing, or the data subject objects to the processing pursuant to Article 21(2); (d) the personal data have been unlawfully processed; (e) the personal data have to be erased for compliance with a legal obligation in Union or Member State law to which the controller is subject; (f) the personal data have been collected in relation to the offer of information society services referred to in Article 8(1).

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 158, page 29 | similarity 0.64
(158) Where personal data are processed for archiving purposes, this Regulation should also apply to that processing, bearing in mind that this Regulation should not apply to deceased persons. Public authorities or public or private bodies that hold records of public interest should be services which, pursuant to Union or Member State law, have a legal obligation to acquire, preserve, appraise, arrange, describe, communicate, promote, disseminate and provide access to records of enduring value for general public interest. Member States should also be authorised to provide for the further processing of personal data for archiving purposes, for example with a view to providing specific information related to the political behaviour under former totalitarian state regimes, genocide, crimes against humanity, in particular the Holocaust, or war crimes.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 31, page 6 | similarity 0.64
(31) Public authorities to which personal data are disclosed in accordance with a legal obligation for the exercise of their official mission, such as tax and customs authorities, financial investigation units, independent adminis trative authorities, or financial market authorities responsible for the regulation and supervision of securities markets should not be regarded as recipients if they receive personal data which are necessary to carry out a particular inquiry in the general interest, in accordance with Union or Member State law. The requests for disclosure sent by the public authorities should always be in writing, reasoned and occasional and should not concern the entirety of a filing system or lead to the interconnection of filing systems. The processing of personal data by those public authorities should comply with the applicable data-protection rules according to the purposes of the processing.
```

</details>

---

## 15. q24 (single)

**Question:** I want to put my staff's photos on the shop's website and I plan to get them to sign a consent form. Is consent a safe legal basis when the person asking is their employer?

**Reference answer:** It is problematic. Because of the dependency in the employment relationship, an employee is unlikely to be able to refuse without fearing or actually suffering negative consequences, so consent is unlikely to be freely given. For the majority of data processing at work, consent should not be the lawful basis. Employers can rely on consent only in exceptional circumstances, where the employer can demonstrate that the employee can truly refuse with no adverse consequences at all, as in the film-crew example, where those who refuse are given equivalent desks elsewhere.

**Agent answer:**

```text
No, consent is generally not a safe or valid legal basis when an employer asks staff for it. 

Because of the dependency in the employer-employee relationship, there is a clear imbalance of power [edpb_consent: Section 3.1.1, paragraphs 21-22]. Employees may fear negative consequences or feel pressured if they refuse, which means consent cannot be freely given [edpb_consent: Section 3.1.1, paragraphs 21-22]. Therefore, it is considered problematic to use consent for employee data processing, and it can only be relied upon in exceptional circumstances where refusal has no adverse consequences at all [edpb_consent: Section 3.1.1, paragraphs 21-22].

The documents do not state which alternative legal basis might apply to publishing staff photos on a website, so you may need to consult a lawyer or your data protection authority.
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: consent employer employee imbalance of power valid GDPR

5 closest passages for: consent employer employee imbalance of power valid GDPR

[1] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.1.1, paragraphs 21-22, page 9 | similarity 0.87
Heading: Imbalance of power
21. An imbalance of power also occurs in the employment context.18 Given the dependency that results from the employer/employee relationship, it is unlikely that the data subject is able to deny his/her employer consent to data processing without experiencing the fear or real risk of detrimental effects as a result of a refusal. It is unlikely that an employee would be able to respond freely to a request for consent from his/her employer to, for example, activate monitoring systems such as camera observation in a workplace, or to fill out assessment forms, without feeling any pressure to consent.19 Therefore, the EDPB deems it problematic for employers to process personal data of current or future employees on the basis of consent as it is unlikely to be freely given. For the majority of such data processing at work, the lawful basis cannot and should not be the consent of the employees (Article 6(1)(a)) due to the nature of the relationship between employer and employee.20 22. However, this does not mean that employers can never rely on consent as a lawful basis for processing. There may be situations when it is possible for the employer to demonstrate that consent ac tually is freely given. Given the imbalance of power between an employer and its staff members, employees can only give free consent in exceptional circumstances, when it will have no adverse consequences at all whether or not they give consent.21

[2] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.1.1, paragraphs 23-24, page 9 | similarity 0.84
Heading: Imbalance of power
23. Example 5: A film crew is going to be filming in a certain part of an office. The employer asks all the employees who sit in that area for their consent to be filmed, as they may appear in the background of the video. Those who do not want to be filmed are not penalised in any way but instead are given equivalent desks elsewhere in the building for the duration of the filming. 24. Imbalances of power are not limited to public authorities and employers, they may also occur in other situations. As highlightedby the WP29 in several Opinions, consent can only be valid if the data subject is able to exercise a real choice, and there is no risk of deception, intimidation, coercion or significant negative consequences (e.g. substantial extra costs) if he/she does not consent. Consent will not be free in cases where there is any element of compulsion, pressure or inability to exercise free will.

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 155, page 29 | similarity 0.79
(155) Member State law or collective agreements, including ‘works agreements’, may provide for specific rules on the processing of employees' personal data in the employment context, in particular for the conditions under which personal data in the employment context may be processed on the basis of the consent of the employee, the purposes of the recruitment, the performance of the contract of employment, including discharge of obligations laid down by law or by collective agreements, management, planning and organisation of work, equality and diversity in the workplace, health and safety at work, and for the purposes of the exercise and enjoyment, on an individual or collective basis, of rights and benefits related to employment, and for the purpose of the termination of the employment relationship.

[4] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.1.1, paragraphs 16-17, page 8 | similarity 0.78
Heading: Imbalance of power
16. Recital 4315 clearly indicates that it is unlikely thatpublic authorities can rely on consent for processing as whenever the controller is a public authority, there is often a clear imbalance of power in the relationship between the c ontroller and the data subject. It is also clear in most cases that the data subject will have no realistic alternatives to accepting the processing (terms) of this controller. The EDPB considers that there are other lawful bases that are, in principle, more appropriate to the activity of public authorities.16 17. Without prejudice to these general considerations, the use of consent as a lawful basis for data processing by public authorities is not totally excluded under the legal framework of the GDPR. The following examples show that the use of consent can be appropriate under certain circumstances.

[5] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.1.1, paragraph 18, page 8 | similarity 0.78
Heading: Imbalance of power
18. Example 2: A local municipality is planning road maintenance works. As the road works may disrupt traffic for a long time, the municipality offers its citizens the opportunity to subscribe to an email list to receive updates on the progress of the works and on expected delays. The municipality makes clear that there is no obligation to participate and asks for consent to use email addresses for this (exclusive) purpose. Citizens that do not consent will not miss out on any core service of the municipality or the exercise of any right, so they are able to give or refuse their consent to this use of data freely. All information on the road works will also be available on the municipality’s website.
```

</details>

---

## 16. q25 (unanswerable)

**Question:** Which controls do I have to implement to get ISO 27001 certified, and how long does the audit usually take?

**Reference answer:** The documents do not cover ISO 27001 certification, its controls or how long an audit takes. A correct answer should say so and not invent controls or timelines. It may suggest asking a certification body or an adviser.

**Agent answer:**

```text
The documents do not cover ISO 27001 certification controls or audit durations. 

The corpus only covers data protection certifications and security measures under the GDPR (such as implementing appropriate technical and organisational measures for data security, and general rules for GDPR certification mechanisms) [gdpr: Article 32, paragraphs 1-3, page 51, Article 42, paragraphs 5-8, page 59]. 

For specific standards like ISO 27001, you should consult an accredited certification body, a legal expert, or the relevant standard documentation.
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: ISO 27001 certification controls audit duration

5 closest passages for: ISO 27001 certification controls audit duration

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 42, paragraphs 5-8, page 59 | similarity 0.68
Heading: Certification
5. A certification pursuant to this Article shall be issued by the certification bodies referred to in Article 43 or by the competent supervisory authority, on the basis of criteria approved by that competent supervisory authority pursuant to Article 58(3) or by the Board pursuant to Article 63. Where the criteria are approved by the Board, this may result in a common certification, the European Data Protection Seal. 6. The controller or processor which submits its processing to the certification mechanism shall provide the certifi cation body referred to in Article 43, or where applicable, the competent supervisory authority, with all information and access to its processing activities which are necessary to conduct the certification procedure. 7. Certification shall be issued to a controller or processor for a maximum period of three years and may be renewed, under the same conditions, provided that the relevant requirements continue to be met. Certification shall be withdrawn, as applicable, by the certification bodies referred to in Article 43 or by the competent supervisory authority where the requirements for the certification are not or are no longer met. 8. The Board shall collate all certification mechanisms and data protection seals and marks in a register and shall make them publicly available by any appropriate means.

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 43, paragraphs 4-7, page 60 | similarity 0.68
Heading: Certification bodies
4. The certification bodies referred to in paragraph 1 shall be responsible for the proper assessment leading to the certification or the withdrawal of such certification without prejudice to the responsibility of the controller or processor for compliance with this Regulation. The accreditation shall be issued for a maximum period of five years and may be renewed on the same conditions provided that the certification body meets the requirements set out in this Article. 5. The certification bodies referred to in paragraph 1 shall provide the competent supervisory authorities with the reasons for granting or withdrawing the requested certification. 6. The requirements referred to in paragraph 3 of this Article and the criteria referred to in Article 42(5) shall be made public by the supervisory authority in an easily accessible form. The supervisory authorities shall also transmit those requirements and criteria to the Board. The Board shall collate all certification mechanisms and data protection seals in a register and shall make them publicly available by any appropriate means. 7. Without prejudice to Chapter VIII, the competent supervisory authority or the national accreditation body shall revoke an accreditation of a certification body pursuant to paragraph 1 of this Article where the conditions for the accreditation are not, or are no longer, met or where actions taken by a certification body infringe this Regulation.

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 58, paragraph 1, page 69 | similarity 0.68
Heading: Powers
1. Each supervisory authority shall have all of the following investigative powers: (a) to order the controller and the processor, and, where applicable, the controller's or the processor's representative to provide any information it requires for the performance of its tasks; (b) to carry out investigations in the form of data protection audits; (c) to carry out a review on certifications issued pursuant to Article 42(7); (d) to notify the controller or the processor of an alleged infringement of this Regulation; (e) to obtain, from the controller and the processor, access to all personal data and to all information necessary for the performance of its tasks; (f) to obtain access to any premises of the controller and the processor, including to any data processing equipment and means, in accordance with Union or Member State procedural law.

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 32, paragraphs 1-3, page 51 | similarity 0.67
Heading: Security of processing
1. Taking into account the state of the art, the costs of implementation and the nature, scope, context and purposes of processing as well as the risk of varying likelihood and severity for the rights and freedoms of natural persons, the controller and the processor shall implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk, including inter alia as appropriate: (a) the pseudonymisation and encryption of personal data; (b) the ability to ensure the ongoing confidentiality, integrity, availability and resilience of processing systems and services; (c) the ability to restore the availability and access to personal data in a timely manner in the event of a physical or technical incident; (d) a process for regularly testing, assessing and evaluating the effectiveness of technical and organisational measures for ensuring the security of the processing. 2. In assessing the appropriate level of security account shall be taken in particular of the risks that are presented by processing, in particular from accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to personal data transmitted, stored or otherwise processed. 3. Adherence to an approved code of conduct as referred to in Article 40 or an approved certification mechanism as referred to in Article 42 may be used as an element by which to demonstrate compliance with the requirements set out in paragraph 1 of this Article.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 24, page 47 | similarity 0.67
Heading: Responsibility of the controller
1. Taking into account the nature, scope, context and purposes of processing as well as the risks of varying likelihood and severity for the rights and freedoms of natural persons, the controller shall implement appropriate technical and organisational measures to ensure and to be able to demonstrate that processing is performed in accordance with this Regulation. Those measures shall be reviewed and updated where necessary. 2. Where proportionate in relation to processing activities, the measures referred to in paragraph 1 shall include the implementation of appropriate data protection policies by the controller. 3. Adherence to approved codes of conduct as referred to in Article 40 or approved certification mechanisms as referred to in Article 42 may be used as an element by which to demonstrate compliance with the obligations of the controller.
```

</details>

---

## 17. q20 (single)

**Question:** What security measures does the law require for my customer database? Is there a fixed checklist?

**Reference answer:** There is no fixed checklist. You must apply technical and organisational measures that give a level of security appropriate to the risk, taking into account the state of the art, implementation costs, and the nature, scope, context and purposes of the processing. Measures to consider include pseudonymisation and encryption, ongoing confidentiality, integrity, availability and resilience of systems, the ability to restore access to data quickly after an incident, and regular testing and evaluation of the measures. Anyone working under your authority who has access to the data must process it only on your instructions.

**Agent answer:**

```text
No, there is no fixed checklist. 

Instead, the law requires you to implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk [gdpr: Article 32, paragraph 1]. To decide what is appropriate, you must take into account:
- The state of the art
- The costs of implementation
- The nature, scope, context, and purposes of your processing
- The likelihood and severity of risks to people's rights and freedoms [gdpr: Article 32, paragraph 1]

Depending on what is appropriate for your specific situation, measures may include:
- Pseudonymisation and encryption of personal data [gdpr: Article 32, paragraph 1(a)]
- Ensuring ongoing confidentiality, integrity, availability, and resilience of processing systems and services [gdpr: Article 32, paragraph 1(b)]
- The ability to restore access to data in a timely manner after a physical or technical incident [gdpr: Article 32, paragraph 1(c)]
- A process for regularly testing, assessing, and evaluating the effectiveness of your security measures [gdpr: Article 32, paragraph 1(d)]

You can also use approved codes of conduct or certification mechanisms to help demonstrate compliance [gdpr: Article 32, paragraph 3]. Because the law does not provide a one-size-fits-all checklist and requires you to assess the risks yourself, you may want to consult a lawyer or your data protection authority if you are unsure whether your specific setup meets the requirement.
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: security of processing measures small business checklist appropriate technical and organisational measures

5 closest passages for: security of processing measures small business checklist appropriate technical and organisational measures

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 32, paragraphs 1-3, page 51 | similarity 0.76
Heading: Security of processing
1. Taking into account the state of the art, the costs of implementation and the nature, scope, context and purposes of processing as well as the risk of varying likelihood and severity for the rights and freedoms of natural persons, the controller and the processor shall implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk, including inter alia as appropriate: (a) the pseudonymisation and encryption of personal data; (b) the ability to ensure the ongoing confidentiality, integrity, availability and resilience of processing systems and services; (c) the ability to restore the availability and access to personal data in a timely manner in the event of a physical or technical incident; (d) a process for regularly testing, assessing and evaluating the effectiveness of technical and organisational measures for ensuring the security of the processing. 2. In assessing the appropriate level of security account shall be taken in particular of the risks that are presented by processing, in particular from accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to personal data transmitted, stored or otherwise processed. 3. Adherence to an approved code of conduct as referred to in Article 40 or an approved certification mechanism as referred to in Article 42 may be used as an element by which to demonstrate compliance with the requirements set out in paragraph 1 of this Article.

[2] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section I.A, page 7 | similarity 0.75
Heading: Basic security considerations
10. One of the requirements of the GDPR is that, by using appropriate technical and organisational measures, personal data shall be processed in a manner to ensure the appropriate security of the personal data, including protection against unauthorised or unlawful processing and against accidental loss, destruction or damage13. 11. Accordingly, the GDPR requires both controllers and processors to have in place appropriate technical and organisational measures to ensure a level of security appropriate to the risk posed to the personal data being processed. They should take into account the state of the art, the costs of implementation and the nature, the scope, context and purposes of processing, as well as the risk of varying likelihood and severity for the rights and freedoms of natural persons 14. Also, the GDPR requires all appropriate technological protection an organisational measures to be in place to establish immediately whether a breach has taken place, which then determines whether the notification obligation is engaged 15. 12. Consequently, a key element of any data security policy is being able, where possible, to prevent a breach and, where it nevertheless occurs, to react to it in a timely manner.

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 83, page 16 | similarity 0.74
(83) In order to maintain security and to prevent processing in infringement of this Regulation, the controller or processor should evaluate the risks inherent in the processing and implement measures to mitigate those risks, such as encryption. Those measures should ensure an appropriate level of security, including confidentiality, taking into account the state of the art and the costs of implementation in relation to the risks and the nature of the personal data to be protected. In assessing data security risk, consideration should be given to the risks that are presented by personal data processing, such as accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to, personal data transmitted, stored or otherwise processed which may in particular lead to physical, material or non-material damage.

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 78, page 15 | similarity 0.74
(78) The protection of the rights and freedoms of natural persons with regard to the processing of personal data require that appropriate technical and organisational measures be taken to ensure that the requirements of this Regulation are met. In order to be able to demonstrate compliance with this Regulation, the controller should adopt internal policies and implement measures which meet in particular the principles of data protection by design and data protection by default. Such measures could consist, inter alia, of minimising the processing of personal data, pseudonymising personal data as soon as possible, transparency with regard to the functions and processing of personal data, enabling the data subject to monitor the data processing, enabling the controller to create and improve security features. When developing, designing, selecting and using applications, services and products that are based on the processing of personal data or process personal data to fulfil their task, producers of the products, services and applications should be encouraged to take into account the right to data protection when developing and designing such products, services and applications and, with due regard to the state of the art, to make sure that controllers and processors are able to fulfil their data protection obligations. The principles of data protection by design and by default should also be taken into consideration in the context of public tenders.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 5, paragraphs 1-2, page 35 | similarity 0.73
Heading: Principles relating to processing of personal data
(f) processed in a manner that ensures appropriate security of the personal data, including protection against unauthorised or unlawful processing and against accidental loss, destruction or damage, using appropriate technical or organisational measures (‘integrity and confidentiality’). 2. The controller shall be responsible for, and be able to demonstrate compliance with, paragraph 1 (‘accountability’).
```

</details>

---

## 18. q07 (multi)

**Question:** We've had a breach but don't yet know exactly how many customers are affected. Can we wait until we have exact numbers before telling the authority?

**Reference answer:** No. Article 33(3) requires the notification to describe the nature of the breach, the categories and approximate number of people and records affected, the DPO or contact point, the likely consequences, and the measures taken or proposed. The word "approximate" matters: the guidelines say missing exact figures is not a barrier to timely notification. Under Art. 33(4) you can provide information in phases without undue further delay. The EDPB recommends telling the authority at the first notification that more details will follow. Missing the 72-hour deadline requires reasons for the delay.

**Agent answer:**

```text
No, you should not wait for exact numbers. 

The GDPR allows you to provide information in phases without undue further delay when it is not possible to provide all details at once [edpb_breach: Section II.B.2, paragraph 56]. Where precise information—such as the exact number of affected data subjects—is not yet available, this should not prevent you from making a timely breach notification; you are permitted to use approximations for the number of individuals and records concerned [edpb_breach: Section II.B.1, paragraph 52]. 

When you make your initial notification within 72 hours, you should inform the authority that you do not yet have all the required information and will provide more details later [edpb_breach: Section II.B.2, paragraph 57]. You should also provide reasons for any delay in supplying full details [edpb_breach: Section II.B.2, paragraph 57].
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: personal data breach notification to supervisory authority incomplete information phase phased notification

5 closest passages for: personal data breach notification to supervisory authority incomplete information phase phased notification

[1] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.B.2, paragraph 57, page 15 | similarity 0.82
Heading: Notification in phases
57. This means that the GDPR recognises that controllers will not always have all of the necessary information concerning a breach within 72 hours of becoming aware of it, as full and comprehensive details of the incident may not always be available during this initial period. As such, it allows for a notification in phases. It is m ore likely this will be the case for more complex breaches, such as some types of cyber security incidents where, for example, an indepth forensic investigation may be necessary to fully establish the nature of the breach and the extent to which personal data have been compromised. Consequently, in many cases the controller will have to do more investigation and follow-up with additional information at a later point. This is permissible, providing the controller gives reasons for the delay, in accordance w ith Article 33(1) GDPR. The EDPB recommends that when the controller first notifies the supervisory authority, the controller should also inform the supervisory authority if the controller does not yet have all the required information and will provide more details later on. The supervisory authority should agree how and when additional information should be provided. This does not prevent the controller from providing further information at any other stage, if it becomes aware of additional relevant details about the breach that need to be provided to the supervisory authority.

[2] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.B.2, paragraph 56, page 15 | similarity 0.80
Heading: Notification in phases
56. Depending on the nature of a breach, further investigation by the controller may be necessary to establish all of the relevant facts relating to the incident. Article 33(4) GDPR therefore states: “Where, and in so far as, it is not possible to provide the information at the same time, the information may be provided in phases without undue further delay.”

[3] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.B.2, paragraphs 60-61, page 16 | similarity 0.78
Heading: Notification in phases
60. It should also be clear that after making an initial notification, a controller could update the supervisory authority if a follow-up investigation uncovers evidence that the security incident was contai ned and no breach actually occurred. This information could then be added to the information already given to the supervisory authority and the incident recorded accordingly as not being a breach. There is no penalty for reporting an incident that ultimately transpires not to be a breach. Example A controller notifies the supervisory authority within 72 hours of detecting a breach that it has lost a USB key containing a copy of the personal data of some of its customers. The USB key is later found misfiled within the controller’s premises and recovered. The controller updates the supervisory authority and requests the notification be amended. 61. It should be noted that a phased approach to notification is already the case under the existing obligations of Directive 2002/58/EC, Regulation 611/2013 and other self-reported incidents.

[4] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.B.2, paragraphs 58-59, page 15 | similarity 0.77
Heading: Notification in phases
58. The focus of the notification requirement is to encourage controllers to act promptly on a breach, contain it and, if possible, recover the compromised personal data, and to seek re levant advice from the supervisory authority. Notifying the supervisory authority within the first 72 hours can allow the controller to make sure that decisions about notifying or not notifying individuals are correct. 59. However, the purpose of notifying the supervisory authority is not solely to obtain guidance on whether to notify the affected individuals. It will be obvious in some cases that, due to the nature of the breach and the severity of the risk, the controller will need to notify the affected individuals without delay. For example, if there is an immediate threat of identity theft, or if special categories of personal data 29 are disclosed online, the controller should act without undue delay to contain the breach and to communicate it to the indivi duals concerned (see section III). In exceptional circumstances, this might even take place before notifying the supervisory authority. More generally, notification of the supervisory authority may not serve as a justification for failure to communicate the breach to the data subject where it is required.

[5] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.B.1, paragraphs 51-53, page 15 | similarity 0.76
Heading: Information to be provided
51. Recital 85 GDPR makes it clear that one of the purposes of notification is limiting damage to individuals. Accordingly, if the types of data subjects or the types of personal data indicate a risk of particular damage occurring as a result of a breach (e.g. identity theft, fraud, financial loss, threat to professional secrecy), then it is important the notification indicates these categories. In this way, it is linked to the requirement of describing the likely consequences of the breach. 52. Where precise information is not available (e.g. exact number of data subjects affected) this should not be a barrier to timely breach notification. The GDPR allows for approximations to be made in the number of individuals affected and the number of personal data records concerned. The focus should be directed towards addressing the adverse effects of the breach rather than providing precise figures. 53. Thus, when it has become clear that here has been a breach, but the extent of it is not yet known, a notification in phases (see below) is a safe way to meet the notification obligations.
```

</details>

---

## 19. q17 (single)

**Question:** When customers fill in my online order form, what do I have to tell them about how I use their data?

**Reference answer:** At the time you collect the data you must give the person: your identity and contact details (and your DPO's, if you have one); the purposes and legal basis of the processing, and the legitimate interests pursued if you rely on them; the recipients or categories of recipients; and any intended transfer to a third country and the safeguards used. You must also tell them the storage period (or the criteria used to set it), their rights to access, rectification, erasure, restriction, objection and portability, and the right to withdraw consent where consent is the basis. You must also tell them about their right to complain to the authority, whether providing the data is a legal or contractual requirement and what happens if they don't, and any automated decision-making including profiling.

**Agent answer:**

```text
When you collect personal data directly from customers via an online order form, you must provide them with the following information at the time you obtain the data:

* Your identity and contact details (and those of your representative or data protection officer, if applicable) [gdpr: Article 13, paragraph 1].
* The purposes of the processing and the legal basis for it [gdpr: Article 13, paragraph 1].
* If you rely on legitimate interests as a legal basis, the specific legitimate interests pursued [gdpr: Article 13, paragraph 1].
* The recipients or categories of recipients of the data, if any [gdpr: Article 13, paragraph 1].
* Details of any intended international data transfers outside the EU and the safeguards used [gdpr: Article 13, paragraph 1].
* How long the data will be stored, or the criteria used to determine that period [gdpr: Article 13, paragraph 2].
* The data subject's rights: access, rectification, erasure, restriction of processing, objection to processing, and data portability [gdpr: Article 13, paragraph 2].
* If processing is based on consent, the right to withdraw consent at any time (without affecting the lawfulness of processing done before withdrawal) [gdpr: Article 13, paragraph 2].
* The right to lodge a complaint with a supervisory authority [gdpr: Article 13, paragraph 2].
* Whether providing the personal data is a statutory or contractual requirement (or necessary to enter into a contract), whether customers are obliged to provide it, and the possible consequences of not providing it [gdpr: Article 13, paragraph 2].
* The existence of any automated decision-making, including profiling, along with meaningful information about the logic, significance, and consequences involved [gdpr: Article 13, paragraph 2].
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: information to be provided when personal data are collected from the data subject article 13

5 closest passages for: information to be provided when personal data are collected from the data subject article 13

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 13, paragraph 1, page 40 | similarity 0.82
Heading: Information to be provided where personal data are collected from the data subject
1. Where personal data relating to a data subject are collected from the data subject, the controller shall, at the time when personal data are obtained, provide the data subject with all of the following information: (a) the identity and the contact details of the controller and, where applicable, of the controller's representative; (b) the contact details of the data protection officer, where applicable; (c) the purposes of the processing for which the personal data are intended as well as the legal basis for the processing; (d) where the processing is based on point (f) of Article 6(1), the legitimate interests pursued by the controller or by a third party; (e) the recipients or categories of recipients of the personal data, if any; (f) where applicable, the fact that the controller intends to transfer personal data to a third country or international organisation and the existence or absence of an adequacy decision by the Commission, or in the case of transfers referred to in Article 46 or 47, or the second subparagraph of Article 49(1), reference to the appropriate or suitable safeguards and the means by which to obtain a copy of them or where they have been made available.

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 13, paragraph 2, page 41 | similarity 0.78
Heading: Information to be provided where personal data are collected from the data subject
2. In addition to the information referred to in paragraph 1, the controller shall, at the time when personal data are obtained, provide the data subject with the following further information necessary to ensure fair and transparent processing: (a) the period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period; (b) the existence of the right to request from the controller access to and rectification or erasure of personal data or restriction of processing concerning the data subject or to object to processing as well as the right to data portability; (c) where the processing is based on point (a) of Article 6(1) or point (a) of Article 9(2), the existence of the right to withdraw consent at any time, without affecting the lawfulness of processing based on consent before its withdrawal; (d) the right to lodge a complaint with a supervisory authority; (e) whether the provision of personal data is a statutory or contractual requirement, or a requirement necessary to enter into a contract, as well as whether the data subject is obliged to provide the personal data and of the possible consequences of failure to provide such data; (f) the existence of automated decision-making, including profiling, referred to in Article 22(1) and (4) and, at least in those cases, meaningful information about the logic involved, as well as the significance and the envisaged consequences of such processing for the data subject.

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 13, paragraphs 3-4, page 41 | similarity 0.77
Heading: Information to be provided where personal data are collected from the data subject
3. Where the controller intends to further process the personal data for a purpose other than that for which the personal data were collected, the controller shall provide the data subject prior to that further processing with information on that other purpose and with any relevant further information as referred to in paragraph 2. 4. Paragraphs 1, 2 and 3 shall not apply where and insofar as the data subject already has the information.

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 14, paragraphs 3-4, page 42 | similarity 0.75
Heading: Information to be provided where personal data have not been obtained from the data subject
3. The controller shall provide the information referred to in paragraphs 1 and 2: (a) within a reasonable period after obtaining the personal data, but at the latest within one month, having regard to the specific circumstances in which the personal data are processed; (b) if the personal data are to be used for communication with the data subject, at the latest at the time of the first communication to that data subject; or (c) if a disclosure to another recipient is envisaged, at the latest when the personal data are first disclosed. 4. Where the controller intends to further process the personal data for a purpose other than that for which the personal data were obtained, the controller shall provide the data subject prior to that further processing with information on that other purpose and with any relevant further information as referred to in paragraph 2.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 61, page 12 | similarity 0.75
(61) The information in relation to the processing of personal data relating to the data subject should be given to him or her at the time of collection from the data subject, or, where the personal data are obtained from another source, within a reasonable period, depending on the circumstances of the case. Where personal data can be legitimately disclosed to another recipient, the data subject should be informed when the personal data are first disclosed to the recipient. Where the controller intends to process the personal data for a purpose other than that for which they were collected, the controller should provide the data subject prior to that further processing with information on that other purpose and other necessary information. Where the origin of the personal data cannot be provided to the data subject because various sources have been used, general information should be provided.
```

</details>

---

## 20. q26 (single)

**Question:** Last month a staff member emailed a customer's order details to the wrong person. We fixed it the same day and decided it was too minor to report to the authority. Do we still have to write anything down about it, and what should the record say?

**Reference answer:** Yes. Article 33(5) requires the controller to document any personal data breach, whether or not it is notified. The documentation must cover the facts of the breach, its effects and the remedial action taken, and must enable the authority to verify compliance. The guidelines add that the record should include the causes, what took place and the personal data affected. They also recommend recording your reasoning for the decision not to notify, including why you considered the breach unlikely to result in a risk to people's rights and freedoms. It is up to you what method and structure to use, although an internal register of breaches is encouraged. The GDPR sets no retention period for these records. Failing to document properly can lead to the authority using its Article 58 powers or imposing a fine.

**Agent answer:**

```text
Yes, you must still document the breach. Even if an incident does not need to be reported to the supervisory authority, you are required to keep a record of all personal data breaches [edpb_breach: Section V.A, paragraphs 121-122]. 

The record should include:
* The facts relating to the breach, including its causes, what took place, and the personal data that was affected [edpb_breach: Section V.A, paragraphs 121, 123].
* The effects and consequences of the breach [edpb_breach: Section V.A, paragraphs 121, 123].
* The remedial action taken (such as fixing the error the same day) [edpb_breach: Section V.A, paragraphs 121, 123].
* A justification for your decision not to notify the authority, including the reasons why you considered the breach unlikely to result in a risk to the rights and freedoms of individuals [edpb_breach: Section V.A, paragraph 125].
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: record personal data breach document internal register

5 closest passages for: record personal data breach document internal register

[1] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section V.A, paragraphs 121-123, page 26 | similarity 0.77
Heading: Documenting breaches
121. Regardless of whether or not a breach needs to be notified to the supervisory authority, the controller must keep documentation of all breaches, as Article 33(5) GDPR explains: “The controller shall document any personal data breaches, comprising the facts relating to the personal data breach, its effects and the remedial action taken. That documentation shall enable the supervisory authority to verify compliance with this Article.” 122. This is linked to the accountability principle of the GDPR, contained in Article 5(2) GDPR. The purpose of recording nonnotifiable breaches, as well notifiable breaches, also relates to the controller’s obligations under Article 24 GDPR, and the supervisory authority can request to see these records. Controllers are therefore encouraged to establish an internal register of breaches, regardless of whether they are required to notify or not47. 123. Whilst it is up to the controller to determine what method and structure to use when documenting a breach, in terms of recordable information there are key elements that should be included in all cases. As is required by Article 33(5) GDPR, the controller needs to record details concerning the breach, which should include its causes, what took place and the personal data affected. It should also include the effects and consequences of the breach, along with the remedial action taken by the controller.

[2] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section V.A, paragraphs 124-125, page 26 | similarity 0.74
Heading: Documenting breaches
124. The GDPR does not specify a retention period for such documentation. Where such records contain personal data, it will be incumbent on the controller to de termine the appropriate period of retention in accordance with the principles in relation to the processing of personal data48 and to meet a lawful basis for processing 49. It will need to retain documentation in accordance with Article 33(5) GDPR insofar as it may be called to provide evidence of compliance with that Article, or with the accountability principle more generally, to the supervisory authority. Clearly, if the records themselves contain no personal data then the storage limitation principle50 of the GDPR does not apply. 125. In addition to these details, the EDPB recommends that the controller also document its reasoning for the decisions taken in response to a breach. In particular, if a breach is not notified, a justification for that decision should be documented. This should include reasons why the controller considers the breach is unlikely to result in a risk to the rights and freedoms of individuals 51 . Alternatively, if the controller considers that any of the conditions in Article 34(3) GDPR are met, then it should be able to provide appropriate evidence that this is the case.

[3] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.A.2, paragraph 39, page 13 | similarity 0.73
Heading: When does a controller become “aware”?
39. Whilst it is the responsibility of controllers and processors to put in place suitable measures to be able to prevent, react and address a breach, there are some practical steps that should be taken in all cases. • Information concerning all security -related events should be directed towards a responsible person or persons with the task of addressing incidents, establishing the existence of a breach and assessing risk. • Risk to individuals as a result of a breach should then be assessed (likelihood of no risk, risk or high risk), with relevant sections of the organisation being informed. • Notification to the supervisory authority, and potentially communication of the breach to the affected individuals should be made, if required. • At the same time, the controller should act to contain and recover the breach. Documentation of the breach should take place as it develops.

[4] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section V.A, paragraphs 126-129, page 27 | similarity 0.73
Heading: Documenting breaches
126. Where the controller does notify a breach to the supervisory authority, but the notification is delayed, the controller must be able to provide reasons for that delay; documentation relating to this could help to demonstrate that the delay in reporting is justified and not excessive. 127. Where the controller communicates a breach to the affected individuals, it should be transparent about the breach and communicate in an effec tive and timely manner. Accordingly, it would help the controller to demonstrate accountability and compliance by retaining evidence of such communication. 128. To aid compliance with Articles 33 and 34 GDPR, it would be advantageous to both controllers and processors to have a documented notification procedure in place, setting out the process to follow once a breach has been detected, including how to contain, manage and recover the incident, as well as assessing risk, and notifying the breach. In this regard, to show compliance with GDPR it might also be useful to demonstrate that employees have been informed about the existence of such procedures and mechanisms and that they know how to react to breaches. 129. It should be noted that failure to properly document a breach can lead to the supervisory authority exercising its powers under Article 58 GDPR and, or imposing an administrative fine in accordance with Article 83 GDPR.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 33, paragraph 5, page 52 | similarity 0.73
Heading: Notification of a personal data breach to the supervisory authority
5. The controller shall document any personal data breaches, comprising the facts relating to the personal data breach, its effects and the remedial action taken. That documentation shall enable the supervisory authority to verify compliance with this Article.
```

</details>

---

## 21. q19 (single)

**Question:** I have 8 employees. Do I still have to keep a written record of my processing activities, or are small businesses exempt?

**Reference answer:** The exemption for organisations with fewer than 250 people is conditional. It does not apply if the processing is likely to risk people's rights and freedoms, is not occasional, or includes special categories of data or criminal-conviction data. Routine processing such as customer lists or payroll is normally not occasional, so a small business usually still has to keep the record. The record must be in writing (electronic is fine) and be made available to the supervisory authority on request.

**Agent answer:**

```text
Organizations with fewer than 250 employees are generally exempt from the obligation to maintain a written record of processing activities, but this exemption does not apply if:
- The processing you carry out is likely to result in a risk to the rights and freedoms of data subjects,
- The processing is not occasional, or
- The processing includes special categories of data (such as health data) or personal data relating to criminal convictions and offences.

You will need to assess your specific processing activities against these conditions to determine whether the exemption applies to your business.

[gdpr: Article 30, paragraph 5; gdpr: Recital 13]
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: record of processing activities small business exemption 250 employees

5 closest passages for: record of processing activities small business exemption 250 employees

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 30, paragraph 5, page 51 | similarity 0.81
Heading: Records of processing activities
5. The obligations referred to in paragraphs 1 and 2 shall not apply to an enterprise or an organisation employing fewer than 250 persons unless the processing it carries out is likely to result in a risk to the rights and freedoms of data subjects, the processing is not occasional, or the processing includes special categories of data as referred to in Article 9(1) or personal data relating to criminal convictions and offences referred to in Article 10.

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 13, page 3 | similarity 0.74
(13) In order to ensure a consistent level of protection for natural persons throughout the Union and to prevent divergences hampering the free movement of personal data within the internal market, a Regulation is necessary to provide legal certainty and transparency for economic operators, including micro, small and medium-sized enterprises, and to provide natural persons in all Member States with the same level of legally enforceable rights and obligations and responsibilities for controllers and processors, to ensure consistent monitoring of the processing of personal data, and equivalent sanctions in all Member States as well as effective cooperation between the supervisory authorities of different Member States. The proper functioning of the internal market requires that the free movement of personal data within the Union is not restricted or prohibited for reasons connected with the protection of natural persons with regard to the processing of personal data. To take account of the specific situation of micro, small and medium-sized enterprises, this Regulation includes a derogation for organisations with fewer than 250 employees with regard to record-keeping. In addition, the Union institutions and bodies, and Member States and their supervisory authorities, are encouraged to take account of the specific needs of micro, small and medium-sized enterprises in the application of this Regulation. The notion of micro, small and medium-sized enterprises should draw from Article 2 of the Annex to Commission Recommendation 2003/361/EC (1).

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 30, paragraph 1, page 50 | similarity 0.71
Heading: Records of processing activities
1. Each controller and, where applicable, the controller's representative, shall maintain a record of processing activities under its responsibility. That record shall contain all of the following information: (a) the name and contact details of the controller and, where applicable, the joint controller, the controller's representa tive and the data protection officer; (b) the purposes of the processing; (c) a description of the categories of data subjects and of the categories of personal data; (d) the categories of recipients to whom the personal data have been or will be disclosed including recipients in third countries or international organisations; (e) where applicable, transfers of personal data to a third country or an international organisation, including the identifi cation of that third country or international organisation and, in the case of transfers referred to in the second subparagraph of Article 49(1), the documentation of suitable safeguards; (f) where possible, the envisaged time limits for erasure of the different categories of data; (g) where possible, a general description of the technical and organisational security measures referred to in Article 32(1).

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 30, paragraphs 2-4, page 51 | similarity 0.70
Heading: Records of processing activities
2. Each processor and, where applicable, the processor's representative shall maintain a record of all categories of processing activities carried out on behalf of a controller, containing: (a) the name and contact details of the processor or processors and of each controller on behalf of which the processor is acting, and, where applicable, of the controller's or the processor's representative, and the data protection officer; (b) the categories of processing carried out on behalf of each controller; (c) where applicable, transfers of personal data to a third country or an international organisation, including the identifi cation of that third country or international organisation and, in the case of transfers referred to in the second subparagraph of Article 49(1), the documentation of suitable safeguards; (d) where possible, a general description of the technical and organisational security measures referred to in Article 32(1). 3. The records referred to in paragraphs 1 and 2 shall be in writing, including in electronic form. 4. The controller or the processor and, where applicable, the controller's or the processor's representative, shall make the record available to the supervisory authority on request.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 155, page 29 | similarity 0.69
(155) Member State law or collective agreements, including ‘works agreements’, may provide for specific rules on the processing of employees' personal data in the employment context, in particular for the conditions under which personal data in the employment context may be processed on the basis of the consent of the employee, the purposes of the recruitment, the performance of the contract of employment, including discharge of obligations laid down by law or by collective agreements, management, planning and organisation of work, equality and diversity in the workplace, health and safety at work, and for the purposes of the exercise and enjoyment, on an individual or collective basis, of rights and benefits related to employment, and for the purpose of the termination of the employment relationship.
```

</details>

---

## 22. q12 (single)

**Question:** A customer has asked for a copy of all the data I hold about them. What do I have to give them?

**Reference answer:** Under Article 15 the customer is entitled to confirmation of whether you process their data and, if so, access to it and a copy. They are also entitled to: the purposes of the processing; the categories of data; the recipients; the storage period or criteria; their rights to rectification, erasure, restriction and objection; the right to complain to the authority; the source of the data, if not collected from them; and any automated decision-making. If data is sent outside the EU they can also be told the safeguards used (Art. 15(2)). The first copy is free; a reasonable fee based on administrative costs may be charged for further copies. The copy must not adversely affect the rights and freedoms of others.

**Agent answer:**

```text
You must provide the customer with a copy of their personal data that is undergoing processing [gdpr: Article 15, paragraph 3]. 

Along with a copy of the data itself, you must also provide confirmation that you are processing their data and give them the following information:
* The purposes of the processing [gdpr: Article 15, paragraph 1(a)]
* The categories of personal data concerned [gdpr: Article 15, paragraph 1(b)]
* The recipients or categories of recipients to whom the data have been or will be disclosed (especially recipients in third countries or international organisations) [gdpr: Article 15, paragraph 1(c)]
* The envisaged storage period for the data, or if that is not possible, the criteria used to determine that period [gdpr: Article 15, paragraph 1(d)]
* The existence of their right to request rectification, erasure, restriction of processing, or to object to processing [gdpr: Article 15, paragraph 1(e)]
* The right to lodge a complaint with a supervisory authority [gdpr: Article 15, paragraph 1(f)]
* Where the data were not collected from the customer, any available information about their source [gdpr: Article 15, paragraph 1(g)]
* The existence of automated decision-making, including profiling, along with meaningful information about the logic involved, significance, and consequences [gdpr: Article 15, paragraph 1(h)]
* If the data are transferred to a third country or international organisation, information about the appropriate safeguards relating to the transfer [gdpr: Article 15, paragraph 2]

**Key rules to keep in mind:**
* **Format:** If the request is made by electronic means, you must provide the information in a commonly used electronic form, unless the customer asks for something else [gdpr: Article 15, paragraph 3]. The information must be provided in clear, plain language [gdpr: Article 12, paragraph 1].
* **Timing:** You must respond without undue delay and at the latest within one month of the request [gdpr: Recital 59].
* **Fees:** The first copy must be provided free of charge. If they ask for additional copies, you may charge a reasonable fee based on administrative costs [gdpr: Article 15, paragraph 3].
* **Limits:** The right to obtain a copy must not adversely affect the rights and freedoms of others [gdpr: Article 15, paragraph 4], such as trade secrets or intellectual property [gdpr: Recital 63].
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: right of access copy of personal data what to provide

5 closest passages for: right of access copy of personal data what to provide

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 15, paragraphs 2-4, page 43 | similarity 0.74
Heading: Right of access by the data subject
2. Where personal data are transferred to a third country or to an international organisation, the data subject shall have the right to be informed of the appropriate safeguards pursuant to Article 46 relating to the transfer. 3. The controller shall provide a copy of the personal data undergoing processing. For any further copies requested by the data subject, the controller may charge a reasonable fee based on administrative costs. Where the data subject makes the request by electronic means, and unless otherwise requested by the data subject, the information shall be provided in a commonly used electronic form. 4. The right to obtain a copy referred to in paragraph 3 shall not adversely affect the rights and freedoms of others.

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 63 (part 1 of 2), page 12 | similarity 0.73
(63) A data subject should have the right of access to personal data which have been collected concerning him or her, and to exercise that right easily and at reasonable intervals, in order to be aware of, and verify, the lawfulness of the processing. This includes the right for data subjects to have access to data concerning their health, for example the data in their medical records containing information such as diagnoses, examination results, assessments by treating physicians and any treatment or interventions provided. Every data subject should therefore have the right to know and obtain communication in particular with regard to the purposes for which the personal data are processed, where possible the period for which the personal data are processed, the recipients of the personal data, the logic involved in any automatic personal data processing and, at least when based on profiling, the consequences of such processing. Where possible, the controller should be able to provide remote access to a secure system which would provide the data subject with direct access to his or her personal data. That right should not adversely affect the rights or freedoms of others, including trade secrets or intellectual property and in particular the copyright protecting the software. However, the result of those considerations should not be a refusal to provide all information to the data subject.

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 15, paragraph 1, page 43 | similarity 0.73
Heading: Right of access by the data subject
1. The data subject shall have the right to obtain from the controller confirmation as to whether or not personal data concerning him or her are being processed, and, where that is the case, access to the personal data and the following information: (a) the purposes of the processing; (b) the categories of personal data concerned; (c) the recipients or categories of recipient to whom the personal data have been or will be disclosed, in particular recipients in third countries or international organisations; (d) where possible, the envisaged period for which the personal data will be stored, or, if not possible, the criteria used to determine that period; (e) the existence of the right to request from the controller rectification or erasure of personal data or restriction of processing of personal data concerning the data subject or to object to such processing; (f) the right to lodge a complaint with a supervisory authority; (g) where the personal data are not collected from the data subject, any available information as to their source; (h) the existence of automated decision-making, including profiling, referred to in Article 22(1) and (4) and, at least in those cases, meaningful information about the logic involved, as well as the significance and the envisaged consequences of such processing for the data subject.

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 59, page 11 | similarity 0.71
(59) Modalities should be provided for facilitating the exercise of the data subject's rights under this Regulation, including mechanisms to request and, if applicable, obtain, free of charge, in particular, access to and rectification or erasure of personal data and the exercise of the right to object. The controller should also provide means for requests to be made electronically, especially where personal data are processed by electronic means. The controller should be obliged to respond to requests from the data subject without undue delay and at the latest within one month and to give reasons where the controller does not intend to comply with any such requests.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 12, paragraphs 1-2, page 39 | similarity 0.70
Heading: Transparent information, communication and modalities for the exercise of the rights of the data
subject 1. The controller shall take appropriate measures to provide any information referred to in Articles 13 and 14 and any communication under Articles 15 to 22 and 34 relating to processing to the data subject in a concise, transparent, intelligible and easily accessible form, using clear and plain language, in particular for any information addressed specifically to a child. The information shall be provided in writing, or by other means, including, where appropriate, by electronic means. When requested by the data subject, the information may be provided orally, provided that the identity of the data subject is proven by other means. 2. The controller shall facilitate the exercise of data subject rights under Articles 15 to 22. In the cases referred to in Article 11(2), the controller shall not refuse to act on the request of the data subject for exercising his or her rights under Articles 15 to 22, unless the controller demonstrates that it is not in a position to identify the data subject.
```

</details>

---

## 23. q04 (single)

**Question:** A staff phone with customer data on it was lost. It was securely encrypted, the key was never on the phone, and everything is backed up. Do we have to report this as a breach?

**Reference answer:** Probably not. If the data was protected with state-of-the-art encryption, the key is not compromised, and a backup exists so the data can be restored in good time, the breach is unlikely to risk individuals' rights. You then need not notify the authority or the affected individuals. You must still document the incident internally. You must also re-assess if the key is later found to be compromised or the encryption turns out to be weak, because notification could then become necessary.

**Agent answer:**

```text
No, you likely do not have to report this as a breach to the supervisory authority or the individuals. 

According to the guidelines, the loss of a securely encrypted mobile device does not require notification to the supervisory authority, provided that:
* The encryption key remains in the secure possession of the controller and was not compromised [edpb_breach: Section II.D, paragraph 79].
* This is not the sole copy of the personal data (i.e., you have backups and can restore access in a timely manner) [edpb_breach: Section II.D, paragraph 79].

Because the data is properly encrypted and unintelligible to anyone who finds the phone, and backups exist so that availability is not permanently lost, the incident is considered unlikely to result in a risk to the rights and freedoms of the data subjects [edpb_breach: Section II.D, paragraph 78, 79]. 

However, you must still document the incident internally (such as in an internal breach register), and you must re-evaluate the risk if circumstances change—for example, if the encryption key is ever compromised [edpb_breach: Section II.D, paragraph 78; edpb_breach: Section VII.B, Example i].
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: personal data breach notification encrypted phone lost exception

5 closest passages for: personal data breach notification encrypted phone lost exception

[1] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.D, paragraph 79 (part 1 of 2), page 19 | similarity 0.78
Heading: Conditions where notification is not required
79. Furthermore, it should be noted that if there is a breach where there are no backups of the encrypted personal data then there will have been an availability breach, which could pose risks to individuals and therefore may require notification. Similarly, where a breach occurs involving the loss of encrypted data, even if a backup of the personal data exists this may still be a reportable breach, depending on the length of time taken to restore the data from that backup and the effect that lack of availability has on individuals. As Article 32(1)(c) GDPR states, an important factor of security is the “the ability to restore the availability and access to personal data in a timely manner in the event of a physical or technical incident”. Example A breach that would not require notification to the supervisory authority would be the loss of a securely encrypted mobile device, utilised by the controller and its staff. Provided the encryption key remains within the secure possession of the controller and this is not the sole copy of the personal data then the personal data would be inaccessible to an attacker. This means the breach is unlikely to result in a risk to the rights and freedoms of the data subjects in question.

[2] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.D, paragraphs 75-76, page 18 | similarity 0.76
Heading: Conditions where notification is not required
75. Article 33(1) GDPR makes it clear that breaches that are “unlikely to result in a risk to the rights and freedoms of natural persons” do not require notification to the supervisory authority. An example might be where personal data are already publically available and a disc losure of such data does not constitute a likely risk to the individual. This is in contrast to existing breach notification requirements for providers of publically available electronic communications services in Directive 2009/136/EC that state all relevant breaches have to be notified to the competent authority. 76. In its Opinion 03/2014 on breach notification 38 , WP29 explained that a confidentiality breach of personal data that were encrypted with a state of the art algorithm is still a personal data breach, and has to be notified. However, if the confidentiality of the key is intact – i.e., the key was not compromised in any security breach, and was generated so that it cannot be ascertained by available technical means by any person who is not authorised to access it – then the data are in principle unintelligible. Thus, the breach is unlikely to adversely affect individuals and therefore would not require communication to those individuals 39 . However, even where data is encrypted, a loss or alteration can have negative consequences for data subjects where the controller has no adequate backups. In that instance communication to data subjects would be required, even if the data itself was subject to adequate encryption measures.

[3] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section VII.B (part 1 of 5), page 31 | similarity 0.76
Heading: Examples of personal data breaches and who to notify
The following nonexhaustive examples will assist controllers in determining whether they need to notify in different personal data breach scenarios. These examples may also help to distinguish between risk and high risk to the rights and freedoms of individuals. Example Notify the supervisory authority Notify the data subject Notes/recommendations i A controller stored a backup of an archive of personal data encrypted on a USB key. The key is stolen during a break-in. No. No. As long as the data are encrypted with a state of the art algorithm, backups of the data exist the unique key is not compromised, and the data can be restored in good time, this may not be a reportable breach. However if it is later compromised, notification is required. ii A controller maintains an online service. As a result of a cyber attack on that service, personal data of individuals are exfiltrated. The controller has customers in a single Member State. Yes, report to the supervisory authority if there are likely consequences to individuals. Yes, report to individuals depending on the nature of the personal data affected and if the severity of the likely consequences to individuals is high. iii A brief power outage lasting several minutes at a controller’s call centre meaning customers are unable to call the controller and access their records. No. No. This is not a notifiable breach, but still a recordable incident under Article 33(5).

[4] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section II.D, paragraphs 77-78, page 19 | similarity 0.75
Heading: Conditions where notification is not required
77. WP29 also explained this would similarly be the case if personal data, such as passwords, were securely hashed and salted, the hashed value was calculated with a state of the art cryptographic keyed hash function, the key used to hash the data was not compromised in any breach, and the key used to hash the data has been generated in a way that it cannot be ascertained by available technological means by any person who is not authorised to access it. 78. Consequently, if personal data have been made essentially unintelligible to unautho rised parties and where the data are a copy or a backup exists, a confidentiality breach involving properly encrypted personal data may not need to be notified to the supervisory authority. This is because such a breach is unlikely to pose a risk to individuals’ rights and freedoms. This of course means that the individual would not need to be informed either as there is likely no high risk. However, it should be borne in mind that while notification may initially not be required if there is no likely risk to the rights and freedoms of individuals, this may change over time and the risk would have to be re -evaluated. For example, if the key is subsequently found to be compromised, or a vulnerability in the encryption software is exposed, then notification may still be required.

[5] Source: edpb_breach (EDPB Guidelines 9/2022 on personal data breach notification) | Location: Section I.B.1, paragraphs 13-14, page 7 | similarity 0.75
Heading: Definition
13. As part of any attempt to address a breach the controller should first be able to recognise one. The GDPR defines a “personal data breach” in Article 4(12) as: “a breach of security leading to the accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to, personal data transmitted, stored or otherwise processed.” 14. What is meant by “destruction” of personal data should be quite clear: this is where the data no longer exists, or no longer exists in a form that is of any use to the controller. “Damage” should also be relatively clear: this is where personal data has been altered, corrupted, or is no longer complete. In terms of “loss” of personal data, this should be interpreted as the data may still exist, but the controller has lost control or access to it, or no longer has it in its possession. Finally, unauthorised or unlawful processing may include disclosure of personal data to (or access by) recipients who are not authorised to receive (or access) the data, or any other form of processing which violates the GDPR. Example An example of loss of personal data can include where a device containing a copy of a controller’s customer database has been lost or stolen. A further example of loss may be where the only copy of a set of personal data has been encrypted by ransomware, or has been encrypted by the controller using a key that is no longer in its possession.
```

</details>

---

## 24. q18 (single)

**Question:** A customer has asked me to delete all the data I hold on them. Do I have to, or can I refuse?

**Reference answer:** You must erase the data without undue delay if one of these grounds applies: the data is no longer necessary for its original purpose, the person withdrew consent and no other legal ground exists, they objected and there are no overriding legitimate grounds (or it is direct marketing), the data was processed unlawfully, erasure is required by a legal obligation, or the data was collected from a child for online services. The right is not absolute. It does not apply to the extent processing is necessary for freedom of expression, compliance with a legal obligation, public-interest tasks, public health, archiving or research, or establishing, exercising or defending legal claims. So you can refuse only where one of those exceptions applies.

**Agent answer:**

```text
As a general rule, a customer has the right to obtain the erasure of their personal data without undue delay, and you have the obligation to erase it, if certain grounds apply [gdpr: Article 17, paragraph 1]. 

You must erase the data if one of the following applies:
* The personal data are no longer necessary for the purposes for which they were collected or processed [gdpr: Article 17, paragraph 1(a)].
* The customer withdraws their consent and there is no other legal ground for you to keep processing the data [gdpr: Article 17, paragraph 1(b)].
* The customer objects to the processing and there are no overriding legitimate grounds for you to continue [gdpr: Article 17, paragraph 1(c)].
* The data have been unlawfully processed [gdpr: Article 17, paragraph 1(d)].
* The data must be erased to comply with a legal obligation under EU or Member State law [gdpr: Article 17, paragraph 1(e)].
* The data were collected when the customer was a child in relation to information society services [gdpr: Article 17, paragraph 1(f)].

**When can you refuse?**
You do not have to delete the data if keeping or processing it is necessary for certain specific reasons, including [gdpr: Article 17, paragraph 3]:
* Exercising the right of freedom of expression and information [gdpr: Article 17, paragraph 3(a)].
* Complying with a legal obligation that requires processing under EU or Member State law, or performing a task in the public interest or official authority [gdpr: Article 17, paragraph 3(b)].
* Public health reasons [gdpr: Article 17, paragraph 3(c)].
* Archiving in the public interest, scientific/historical research, or statistical purposes, where erasure would likely make achieving those objectives impossible or seriously impair them [gdpr: Article 17, paragraph 3(d)].
* The establishment, exercise, or defence of legal claims [gdpr: Article 17, paragraph 3(e)].

Whether you must delete the data depends on your specific reasons for holding it and whether any of the exceptions above apply to your situation.
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: right to erasure data subject delete request customer

5 closest passages for: right to erasure data subject delete request customer

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 17, paragraph 1, page 43 | similarity 0.76
Heading: Right to erasure (‘right to be forgotten’)
1. The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay and the controller shall have the obligation to erase personal data without undue delay where one of the following grounds applies: (a) the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed; (b) the data subject withdraws consent on which the processing is based according to point (a) of Article 6(1), or point (a) of Article 9(2), and where there is no other legal ground for the processing; (c) the data subject objects to the processing pursuant to Article 21(1) and there are no overriding legitimate grounds for the processing, or the data subject objects to the processing pursuant to Article 21(2); (d) the personal data have been unlawfully processed; (e) the personal data have to be erased for compliance with a legal obligation in Union or Member State law to which the controller is subject; (f) the personal data have been collected in relation to the offer of information society services referred to in Article 8(1).

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 65 (part 1 of 2), page 12 | similarity 0.74
(65) A data subject should have the right to have personal data concerning him or her rectified and a ‘right to be forgotten’ where the retention of such data infringes this Regulation or Union or Member State law to which the controller is subject. In particular, a data subject should have the right to have his or her personal data erased and no longer processed where the personal data are no longer necessary in relation to the purposes for which they are collected or otherwise processed, where a data subject has withdrawn his or her consent or objects to the processing of personal data concerning him or her, or where the processing of his or her personal data does not otherwise comply with this Regulation. That right is relevant in particular where the data subject has given his or her consent as a child and is not fully aware of the risks involved by the processing, and later wants to remove such personal data, especially on the internet. The data subject should be able to exercise that right notwithstanding the fact that he or she is no longer a child.

[3] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 7.3, page 32 | similarity 0.72
Heading: Data subject’s rights
164. If a data processing activity is based on a data subject’s consent, this will affect that individual’s rights. Data subjects may have the right to data portability (Article 20) when processing is based on consent. At the same time, the right to object (Article 21) does not apply when processing is based on consent, although the right to withdraw consent at any time may provide a similar outcome. 165. Articles 16 to 20 of the GDPR indicate that (when data processing is based on consent), data subjects have the right to erasure when consent has been withdrawn and the rights to restriction, rectification and access.77

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 17, paragraphs 2-3, page 44 | similarity 0.72
Heading: Right to erasure (‘right to be forgotten’)
2. Where the controller has made the personal data public and is obliged pursuant to paragraph 1 to erase the personal data, the controller, taking account of available technology and the cost of implementation, shall take reasonable steps, including technical measures, to inform controllers which are processing the personal data that the data subject has requested the erasure by such controllers of any links to, or copy or replication of, those personal data. 3. Paragraphs 1 and 2 shall not apply to the extent that processing is necessary: (a) for exercising the right of freedom of expression and information; (b) for compliance with a legal obligation which requires processing by Union or Member State law to which the controller is subject or for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller; (c) for reasons of public interest in the area of public health in accordance with points (h) and (i) of Article 9(2) as well as Article 9(3); (d) for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) in so far as the right referred to in paragraph 1 is likely to render impossible or seriously impair the achievement of the objectives of that processing; or (e) for the establishment, exercise or defence of legal claims.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 66, page 13 | similarity 0.71
(66) To strengthen the right to be forgotten in the online environment, the right to erasure should also be extended in such a way that a controller who has made the personal data public should be obliged to inform the controllers which are processing such personal data to erase any links to, or copies or replications of those personal data. In doing so, that controller should take reasonable steps, taking into account available technology and the means available to the controller, including technical measures, to inform the controllers which are processing the personal data of the data subject's request.
```

</details>

---

## 25. q03 (single)

**Question:** Our website hides all its content until visitors click "Accept cookies". Is that valid consent?

**Reference answer:** No. If access to the site is conditional on accepting cookies (a cookie wall), the visitor has no genuine choice, so the consent is not freely given and is invalid.

**Agent answer:**

```text
No, that is not valid consent. 

Access to services and website functionalities must not be made conditional on a user consenting to store or access information on their device—a practice known as a "cookie wall". Because visitors are not presented with a genuine choice and cannot access the content without clicking "Accept cookies", the consent is not freely given [edpb_consent: Section 3.1.2, paragraphs 39-41].
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: cookie wall validity consent conditions free unbundled edpb consent

5 closest passages for: cookie wall validity consent conditions free unbundled edpb consent

[1] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.1.2, paragraphs 38-39, page 11 | similarity 0.82
Heading: Conditionality
38. The EDPB considers that consent cannot be considered as freely given if a controller argues that a choice exists between its service that includes consenting to the use of personal data fo r additional purposes on the one hand, and an equivalent service offered by a different controller on the other hand. In such a case, the freedom of choice would be made dependent on what other market players do and whether an individual data subject would find the other controller’s services genuinely equivalent. It would furthermore imply an obligation for controllers to monitor market developments to ensure the continued validity of consent for their data processing activities, as a competitor may alter its service at a later stage. Hence, using this argument means a consent relying on an alternative option offered by a third party fails to comply with the GDPR, meaning that a service provider cannot prevent data subjects from accessing a service on the basis that they do not consent. 39. In order for consent to be freely given, access to services and functionalities must not be made conditional on the consent of a user to the storing of information, or gaining of access to information already stored, in the terminal equipment of a user (so called cookie walls)27.

[2] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.1.2, paragraphs 40-41, page 12 | similarity 0.82
Heading: Conditionality
40. Example 6a: A website provider puts into place a script that will block content from being visible except for a request to accept cookies and the information about which cookies are being set and for what purposes data will be processed. There is no possibility to access the content without clicking on the “Accept cookies” button. Since the data subject is not presented with a genuine choice, its consent is not freely given. 41. This does not constitute valid consent, as the provision of the service relies on the data subject clicking the “Accept cookies” button. It is not presented with a genuine choice.

[3] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.1, paragraphs 13-14, page 7 | similarity 0.79
Heading: Free / freely given
13. The element “free” implies real choice and control for data subjects. As a general rule, the GDPR prescribes that if the data subject has no real choice, feels compelled to consent or will endure negative consequences if they do not consent, then consen t will not be valid. 13 If consent is bundled up as a non-negotiable part of terms and conditions it is presumed not to have been freely given. Accordingly, consent will not be considered to be free if the data subject is unable to refuse or withdraw his or her consent without detriment.14 The notion of imbalance between the controller and the data subject is also taken into consideration by the GDPR. 14. When assessing whether consent is freely given, one should also take into account the specific situation of tying consent into contracts or the provision of a service as described in Article 7(4). Article 7(4) has been drafted in a non -exhaustive fashion by the words “inter alia”, meaning that there may be a range of other situations, which are caught by this prov ision. In general terms, any element of inappropriate pressure or influence upon the data subject (which may be manifested in many different ways) which prevents a data subject from exercising their free will, shall render the consent invalid.

[4] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 0, page 4 | similarity 0.78
Heading: Preface
On 10 April 2018 the Article 29 Working Party adopted its Guidelines on consent under Regulation 2016/679 (WP259.01), which were endorsed by the European Data Protection Board (hereinafter “EDPB”) at its first Plenary meeting. This document is a slightly updated version of those Guidelines . Any reference to the WP29 Guidelines on consent (WP259 rev.01) should from now on be interpreted as a reference to these guidelines. The EDPB has noticed that there was a need for further clarifications, specifically regarding two questions: 1 The validity of consent provided by the data subject when interacting with so-called “cookie walls”; 2 The example 16 on scrolling and consent. The paragraphs concerning these two issues have been revised and updated, while the rest of the document was left unchanged, except for editorial changes. The revision concerns, more specifically:  Section on Conditionality (paragraphs 38 - 41).  Section on Unambiguous indication of wishes (paragraph 86)

[5] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.1.2, paragraphs 25-26, page 10 | similarity 0.77
Heading: Conditionality
25. To assess whether consent is freely given, Article 7(4) GDPR plays an important role.22 26. Article 7(4) GDPR indicates that, inter alia, the situation of “bundling” consent with acceptance of terms or conditions, or “tying” the provision of a contract or a service to a request for consent to process personal data that are not necessary for the p erformance of that contract or service, is considered highly undesirable. If consent is given in this situation, it is presumed to be not freely given (recital 43). Article 7(4) seeks to ensure that the purpose of personal data processing is not disguised nor bundled with the provision of a contract of a service for which these personal data are not necessary. In doing so, the GDPR ensures that the processing of personal data for which consent is sought cannot become directly or indirectly the counter -performance of a contract. The two lawful bases for the lawful processing of personal data, i.e. consent and contract cannot be merged and blurred.
```

</details>

---

## 26. q02 (single)

**Question:** I run a small shop with five staff. I keep a customer mailing list and take card payments. Do I have to appoint a data protection officer?

**Reference answer:** Only in three cases: you are a public authority, your core activities require regular and systematic monitoring of people on a large scale, or your core activities involve large-scale processing of special categories of data or criminal-conviction data. A mailing list and card payments for a small shop don't fit any of these on their face, so appointing a DPO is not mandatory under the GDPR. You may still appoint one voluntarily, and national law can add further cases (Art. 37(4)).

**Agent answer:**

```text
You do not automatically have to appoint a data protection officer just because you run a shop, keep a mailing list, and take card payments. 

Under the GDPR, you only have to designate a data protection officer if:
1. The processing is carried out by a public authority or body.
2. Your core activities consist of processing operations that require regular and systematic monitoring of data subjects on a large scale.
3. Your core activities consist of large-scale processing of special categories of data (such as health data) or criminal conviction and offence data.

For a small shop where processing customer mailing lists and card payments are ancillary rather than core activities, and are not on a large scale, a data protection officer is not mandatory under the EU rules. However, you may still choose to voluntarily designate one, or you might be required to do so if specific national laws in your Member State require it for cases outside of these criteria.

[gdpr: Article 37, paragraphs 1 and 4]
[gdpr: Recital 97]
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: data protection officer mandatory small business criteria appointment article 37

5 closest passages for: data protection officer mandatory small business criteria appointment article 37

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 37, paragraphs 1-4, page 55 | similarity 0.79
Heading: Designation of the data protection officer
1. The controller and the processor shall designate a data protection officer in any case where: (a) the processing is carried out by a public authority or body, except for courts acting in their judicial capacity; (b) the core activities of the controller or the processor consist of processing operations which, by virtue of their nature, their scope and/or their purposes, require regular and systematic monitoring of data subjects on a large scale; or (c) the core activities of the controller or the processor consist of processing on a large scale of special categories of data pursuant to Article 9 and personal data relating to criminal convictions and offences referred to in Article 10. 2. A group of undertakings may appoint a single data protection officer provided that a data protection officer is easily accessible from each establishment. 3. Where the controller or the processor is a public authority or body, a single data protection officer may be designated for several such authorities or bodies, taking account of their organisational structure and size. 4. In cases other than those referred to in paragraph 1, the controller or processor or associations and other bodies representing categories of controllers or processors may or, where required by Union or Member State law shall, designate a data protection officer. The data protection officer may act for such associations and other bodies representing controllers or processors.

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 97, page 18 | similarity 0.75
(97) Where the processing is carried out by a public authority, except for courts or independent judicial authorities when acting in their judicial capacity, where, in the private sector, processing is carried out by a controller whose core activities consist of processing operations that require regular and systematic monitoring of the data subjects on a large scale, or where the core activities of the controller or the processor consist of processing on a large scale of special categories of personal data and data relating to criminal convictions and offences, a person with expert knowledge of data protection law and practices should assist the controller or processor to monitor internal compliance with this Regulation. In the private sector, the core activities of a controller relate to its primary activities and do not relate to the processing of personal data as ancillary activities. The necessary level of expert knowledge should be determined in particular according to the data processing operations carried out and the protection required for the personal data processed by the controller or the processor. Such data protection officers, whether or not they are an employee of the controller, should be in a position to perform their duties and tasks in an independent manner.

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 37, paragraphs 5-7, page 55 | similarity 0.75
Heading: Designation of the data protection officer
5. The data protection officer shall be designated on the basis of professional qualities and, in particular, expert knowledge of data protection law and practices and the ability to fulfil the tasks referred to in Article 39. 6. The data protection officer may be a staff member of the controller or processor, or fulfil the tasks on the basis of a service contract. 7. The controller or the processor shall publish the contact details of the data protection officer and communicate them to the supervisory authority.

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 39, page 56 | similarity 0.74
Heading: Tasks of the data protection officer
1. The data protection officer shall have at least the following tasks: (a) to inform and advise the controller or the processor and the employees who carry out processing of their obligations pursuant to this Regulation and to other Union or Member State data protection provisions; (b) to monitor compliance with this Regulation, with other Union or Member State data protection provisions and with the policies of the controller or processor in relation to the protection of personal data, including the assignment of responsibilities, awareness-raising and training of staff involved in processing operations, and the related audits; (c) to provide advice where requested as regards the data protection impact assessment and monitor its performance pursuant to Article 35; (d) to cooperate with the supervisory authority; (e) to act as the contact point for the supervisory authority on issues relating to processing, including the prior consultation referred to in Article 36, and to consult, where appropriate, with regard to any other matter. 2. The data protection officer shall in the performance of his or her tasks have due regard to the risk associated with processing operations, taking into account the nature, scope, context and purposes of processing.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 38, page 55 | similarity 0.74
Heading: Position of the data protection officer
1. The controller and the processor shall ensure that the data protection officer is involved, properly and in a timely manner, in all issues which relate to the protection of personal data. 2. The controller and processor shall support the data protection officer in performing the tasks referred to in Article 39 by providing resources necessary to carry out those tasks and access to personal data and processing operations, and to maintain his or her expert knowledge. 3. The controller and processor shall ensure that the data protection officer does not receive any instructions regarding the exercise of those tasks. He or she shall not be dismissed or penalised by the controller or the processor for performing his tasks. The data protection officer shall directly report to the highest management level of the controller or the processor. 4. Data subjects may contact the data protection officer with regard to all issues related to processing of their personal data and to the exercise of their rights under this Regulation. 5. The data protection officer shall be bound by secrecy or confidentiality concerning the performance of his or her tasks, in accordance with Union or Member State law. 6. The data protection officer may fulfil other tasks and duties. The controller or processor shall ensure that any such tasks and duties do not result in a conflict of interests.
```

</details>

---

## 27. q21 (single)

**Question:** I'm thinking of installing a new customer-tracking system in my shop. When does the law say I have to do a data protection impact assessment first?

**Reference answer:** A DPIA is required before processing starts when the processing, particularly with new technologies, is likely to result in a high risk to people's rights and freedoms. Article 35(3) names three cases where one is specifically required: a systematic and extensive evaluation of personal aspects based on automated processing, including profiling, where decisions with legal or similarly significant effects are based on it; large-scale processing of special categories of data (Art. 9(1)) or of criminal-conviction data (Art. 10); and systematic monitoring of a publicly accessible area on a large scale. The supervisory authority also publishes a list of processing types that require a DPIA. A DPIA must contain at least a description of the processing and its purposes, an assessment of necessity and proportionality, an assessment of the risks, and the measures planned to address them.

**Agent answer:**

```text
The law requires you to do a data protection impact assessment prior to processing whenever a type of processing—particularly using new technologies, and considering its nature, scope, context, and purposes—is likely to result in a high risk to the rights and freedoms of individuals [gdpr: Article 35, paragraph 1]. 

Specifically, an assessment is required in cases that involve:
- A systematic and extensive evaluation of personal aspects of individuals based on automated processing (including profiling), where decisions are based on it and produce legal effects or similarly significantly affect the person [gdpr: Article 35, paragraph 3(a)].
- Large-scale processing of special categories of data (such as health data) or data relating to criminal convictions and offences [gdpr: Article 35, paragraph 3(b)].
- Systematic monitoring of a publicly accessible area on a large scale [gdpr: Article 35, paragraph 3(c)].

Whether your specific customer-tracking system triggers a "high risk" depends on how it operates (for example, whether it uses new technologies, involves profiling, or tracks people systematically on a large scale). If you have a data protection officer, you must seek their advice when carrying out the assessment [gdpr: Article 35, paragraph 2]. If you are unsure whether your setup crosses the threshold into high risk, you should consult your data protection authority or a lawyer.
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: data protection impact assessment when required systematic monitoring new technologies

5 closest passages for: data protection impact assessment when required systematic monitoring new technologies

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 35, paragraphs 1-3, page 53 | similarity 0.77
Heading: Data protection impact assessment
1. Where a type of processing in particular using new technologies, and taking into account the nature, scope, context and purposes of the processing, is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall, prior to the processing, carry out an assessment of the impact of the envisaged processing operations on the protection of personal data. A single assessment may address a set of similar processing operations that present similar high risks. 2. The controller shall seek the advice of the data protection officer, where designated, when carrying out a data protection impact assessment. 3. A data protection impact assessment referred to in paragraph 1 shall in particular be required in the case of: (a) a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person; (b) processing on a large scale of special categories of data referred to in Article 9(1), or of personal data relating to criminal convictions and offences referred to in Article 10; or (c) a systematic monitoring of a publicly accessible area on a large scale.

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 90, page 17 | similarity 0.74
(90) In such cases, a data protection impact assessment should be carried out by the controller prior to the processing in order to assess the particular likelihood and severity of the high risk, taking into account the nature, scope, context and purposes of the processing and the sources of the risk. That impact assessment should include, in particular, the measures, safeguards and mechanisms envisaged for mitigating that risk, ensuring the protection of personal data and demonstrating compliance with this Regulation.

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 84, page 16 | similarity 0.73
(84) In order to enhance compliance with this Regulation where processing operations are likely to result in a high risk to the rights and freedoms of natural persons, the controller should be responsible for the carrying-out of a data protection impact assessment to evaluate, in particular, the origin, nature, particularity and severity of that risk. The outcome of the assessment should be taken into account when determining the appropriate measures to be taken in order to demonstrate that the processing of personal data complies with this Regulation. Where a data-protection impact assessment indicates that processing operations involve a high risk which the controller cannot mitigate by appropriate measures in terms of available technology and costs of implementation, a consultation of the supervisory authority should take place prior to the processing.

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 35, paragraphs 7-9, page 54 | similarity 0.72
Heading: Data protection impact assessment
7. The assessment shall contain at least: (a) a systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitimate interest pursued by the controller; (b) an assessment of the necessity and proportionality of the processing operations in relation to the purposes; (c) an assessment of the risks to the rights and freedoms of data subjects referred to in paragraph 1; and (d) the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned. 8. Compliance with approved codes of conduct referred to in Article 40 by the relevant controllers or processors shall be taken into due account in assessing the impact of the processing operations performed by such controllers or processors, in particular for the purposes of a data protection impact assessment. 9. Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to the protection of commercial or public interests or the security of processing operations.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 91 (part 2 of 2), page 17 | similarity 0.71
A data protection impact assessment is equally required for monitoring publicly accessible areas on a large scale, especially when using optic-electronic devices or for any other operations where the competent supervisory authority considers that the processing is likely to result in a high risk to the rights and freedoms of data subjects, in particular because they prevent data subjects from exercising a right or using a service or a contract, or because they are carried out systematically on a large scale. The processing of personal data should not be considered to be on a large scale if the processing concerns personal data from patients or clients by an individual physician, other health care professional or lawyer. In such cases, a data protection impact assessment should not be mandatory.
```

</details>

---

## 28. q13 (unanswerable)

**Question:** My shop has security cameras. How many days does Spanish law let me keep the footage?

**Reference answer:** The documents don't cover this. They give general principles, such as storage limitation in Art. 5(1)(e), but no retention periods and no Spanish rules on camera footage. A correct answer should say so and point to the Spanish regulator (AEPD) or national law, not invent a number of days.

**Agent answer:**

```text
The provided documents do not specify a fixed number of days set by Spanish law for keeping security camera footage. 

However, the EU General Data Protection Regulation (GDPR) states that personal data should not be kept longer than necessary for the purposes for which they were collected [gdpr: Article 17, paragraph 1(a)]. It requires controllers to establish time limits for erasure or for a periodic review to ensure data are not kept longer than necessary [gdpr: Recital 39]. 

Because national retention periods (such as specific limits set by Spanish law) are outside the scope of these EU-level documents, you may want to consult the Spanish data protection authority (AEPD) or a legal professional for the exact day limits applicable in Spain.
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: 

Tool error: Error executing tool search: 1 validation error for searchArguments
query
  Field required [type=missing, input_value={'queries': ['retention p...ention days CCTV GDPR']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.14/v/missing

Search: retention period video surveillance camera days Spain

5 closest passages for: retention period video surveillance camera days Spain

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 91 (part 2 of 2), page 17 | similarity 0.67
A data protection impact assessment is equally required for monitoring publicly accessible areas on a large scale, especially when using optic-electronic devices or for any other operations where the competent supervisory authority considers that the processing is likely to result in a high risk to the rights and freedoms of data subjects, in particular because they prevent data subjects from exercising a right or using a service or a contract, or because they are carried out systematically on a large scale. The processing of personal data should not be considered to be on a large scale if the processing concerns personal data from patients or clients by an individual physician, other health care professional or lawyer. In such cases, a data protection impact assessment should not be mandatory.

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 17, paragraph 1, page 43 | similarity 0.67
Heading: Right to erasure (‘right to be forgotten’)
1. The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay and the controller shall have the obligation to erase personal data without undue delay where one of the following grounds applies: (a) the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed; (b) the data subject withdraws consent on which the processing is based according to point (a) of Article 6(1), or point (a) of Article 9(2), and where there is no other legal ground for the processing; (c) the data subject objects to the processing pursuant to Article 21(1) and there are no overriding legitimate grounds for the processing, or the data subject objects to the processing pursuant to Article 21(2); (d) the personal data have been unlawfully processed; (e) the personal data have to be erased for compliance with a legal obligation in Union or Member State law to which the controller is subject; (f) the personal data have been collected in relation to the offer of information society services referred to in Article 8(1).

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 39 (part 2 of 2), page 7 | similarity 0.67
Personal data should be processed only if the purpose of the processing could not reasonably be fulfilled by other means. In order to ensure that the personal data are not kept longer than necessary, time limits should be established by the controller for erasure or for a periodic review. Every reasonable step should be taken to ensure that personal data which are inaccurate are rectified or deleted. Personal data should be processed in a manner that ensures appropriate security and confidentiality of the personal data, including for preventing unauthorised access to or use of personal data and the equipment used for the processing.

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 49, page 9 | similarity 0.67
(49) The processing of personal data to the extent strictly necessary and proportionate for the purposes of ensuring network and information security, i.e. the ability of a network or an information system to resist, at a given level of confidence, accidental events or unlawful or malicious actions that compromise the availability, authenticity, integrity and confidentiality of stored or transmitted personal data, and the security of the related services offered by, or accessible via, those networks and systems, by public authorities, by computer emergency response teams (CERTs), computer security incident response teams (CSIRTs), by providers of electronic communications networks and services and by providers of security technologies and services, constitutes a legitimate interest of the data controller concerned. This could, for example, include preventing unauthorised access to electronic communications networks and malicious code distribution and stopping ‘denial of service’ attacks and damage to computer and electronic communication systems.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 64, page 12 | similarity 0.66
(64) The controller should use all reasonable measures to verify the identity of a data subject who requests access, in particular in the context of online services and online identifiers. A controller should not retain personal data for the sole purpose of being able to react to potential requests.
```

</details>

---

## 29. q05 (unanswerable)

**Question:** I ship products to customers in California. What do I have to do under the CCPA about letting them opt out of the sale of their data?

**Reference answer:** The provided documents don't cover this. They deal only with the GDPR and EDPB guidance, not California law, so a correct answer should say the documents can't answer and point the user to the relevant California rules or a lawyer, rather than inventing requirements.

**Agent answer:**

```text
The documents do not cover the CCPA (California Consumer Privacy Act) or its requirements regarding opting out of the sale of personal data, as they only cover the EU GDPR and related European data protection guidelines. 

The closest things they cover under EU law are the right to object to the processing of personal data [gdpr: Article 21, paragraphs 1-5, page 45], particularly for direct marketing purposes [gdpr: Recital 70, page 13], and the rules on obtaining consent [edpb_consent: Section 4, paragraph 102, page 22]. 

For obligations under California law, you should consult a lawyer or the relevant guidance from California regulatory authorities.
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: CCPA California opt out sale of data

5 closest passages for: CCPA California opt out sale of data

[1] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 4, paragraph 102, page 22 | similarity 0.67
Heading: Obtaining Explicit Consent
102. In order to be able to provide its customised products to customers who are short -sighted, this controller requests consent for the use of information on customers’ eye condition. Customers provide the necessary health data, such as their prescription data online when they place their order. Without this, it is not possible to provide the requested customized eyewear. The company also offers series of goggles with standardized correctional values. Customers that do not wish to share health data could opt for the standard versions. Therefore, an explicit consent under Article 9 is required and consent can be considered to be freely given.

[2] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 70, page 13 | similarity 0.67
(70) Where personal data are processed for the purposes of direct marketing, the data subject should have the right to object to such processing, including profiling to the extent that it is related to such direct marketing, whether with regard to initial or further processing, at any time and free of charge. That right should be explicitly brought to the attention of the data subject and presented clearly and separately from any other information.

[3] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 21, paragraphs 1-5, page 45 | similarity 0.66
Heading: Right to object
1. The data subject shall have the right to object, on grounds relating to his or her particular situation, at any time to processing of personal data concerning him or her which is based on point (e) or (f) of Article 6(1), including profiling based on those provisions. The controller shall no longer process the personal data unless the controller demonstrates compelling legitimate grounds for the processing which override the interests, rights and freedoms of the data subject or for the establishment, exercise or defence of legal claims. 2. Where personal data are processed for direct marketing purposes, the data subject shall have the right to object at any time to processing of personal data concerning him or her for such marketing, which includes profiling to the extent that it is related to such direct marketing. 3. Where the data subject objects to processing for direct marketing purposes, the personal data shall no longer be processed for such purposes. 4. At the latest at the time of the first communication with the data subject, the right referred to in paragraphs 1 and 2 shall be explicitly brought to the attention of the data subject and shall be presented clearly and separately from any other information. 5. In the context of the use of information society services, and notwithstanding Directive 2002/58/EC, the data subject may exercise his or her right to object by automated means using technical specifications.

[4] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 18, page 44 | similarity 0.66
Heading: Right to restriction of processing
1. The data subject shall have the right to obtain from the controller restriction of processing where one of the following applies: (a) the accuracy of the personal data is contested by the data subject, for a period enabling the controller to verify the accuracy of the personal data; (b) the processing is unlawful and the data subject opposes the erasure of the personal data and requests the restriction of their use instead; (c) the controller no longer needs the personal data for the purposes of the processing, but they are required by the data subject for the establishment, exercise or defence of legal claims; (d) the data subject has objected to processing pursuant to Article 21(1) pending the verification whether the legitimate grounds of the controller override those of the data subject. 2. Where processing has been restricted under paragraph 1, such personal data shall, with the exception of storage, only be processed with the data subject's consent or for the establishment, exercise or defence of legal claims or for the protection of the rights of another natural or legal person or for reasons of important public interest of the Union or of a Member State. 3. A data subject who has obtained restriction of processing pursuant to paragraph 1 shall be informed by the controller before the restriction of processing is lifted.

[5] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Article 9, paragraph 1, page 38 | similarity 0.66
Heading: Processing of special categories of personal data
1. Processing of personal data revealing racial or ethnic origin, political opinions, religious or philosophical beliefs, or trade union membership, and the processing of genetic data, biometric data for the purpose of uniquely identifying a natural person, data concerning health or data concerning a natural person's sex life or sexual orientation shall be prohibited.
```

</details>

---

## 30. q11 (single)

**Question:** At checkout we have a box for our newsletter that is already ticked. Customers can untick it. Is that valid consent?

**Reference answer:** No. Pre-ticked boxes and opt-out constructions are invalid. Silence, inactivity and merely proceeding with a service are not an active indication of choice. Consent must come from a clear affirmative act, and it can't be obtained through the same action as accepting general terms and conditions.

**Agent answer:**

```text
No, a pre-ticked box is not valid consent. 

Consent requires a clear affirmative act indicating agreement. Silence, inactivity, or pre-ticked boxes do not constitute valid consent, and opt-out constructions that require the customer to intervene to prevent agreement are not allowed [gdpr: Recital 32; edpb_consent: Section 3.4, paragraphs 79-81].
```

<details><summary>Passages the agent retrieved</summary>

```text
Search: pre-ticked box consent newsletter valid

5 closest passages for: pre-ticked box consent newsletter valid

[1] Source: gdpr (GDPR (Regulation (EU) 2016/679)) | Location: Recital 32, page 6 | similarity 0.76
(32) Consent should be given by a clear affirmative act establishing a freely given, specific, informed and unambiguous indication of the data subject's agreement to the processing of personal data relating to him or her, such as by a written statement, including by electronic means, or an oral statement. This could include ticking a box when visiting an internet website, choosing technical settings for information society services or another statement or conduct which clearly indicates in this context the data subject's acceptance of the proposed processing of his or her personal data. Silence, pre-ticked boxes or inactivity should not therefore constitute consent. Consent should cover all processing activities carried out for the same purpose or purposes. When the processing has multiple purposes, consent should be given for all of them. If the data subject's consent is to be given following a request by electronic means, the request must be clear, concise and not unnecessarily disruptive to the use of the service for which it is provided.

[2] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.4, paragraphs 79-81, page 18 | similarity 0.76
Heading: Unambiguous indication of wishes
79. Without prejudice to existing (national) contract law, consent can be obtained through a recorded oral statement, although due note must be taken of the information available to the data subject, prior to the indication of consent. The use of pre -ticked opt-in boxes is invalid under the GDPR. Silence or inactivity on the part of the data subject, as well as merely proceeding with a service cannot be regarded as an active indication of choice. 80. Example 14: When installing software, the application asks the data subject for consent to us e nonanonymised crash reports to improve the software. A layered privacy notice providing the necessary information accompanies the request for consent. By actively ticking the optional box stating, “I consent”, the user is able to validly perform a ´clear affirmative act´ to consent to the processing. 81. A controller must also beware that consent cannot be obtained through the same motion as agreeing to a contract or accepting general terms and conditions of a service. Blanket acceptance of general terms and conditions cannot be seen as a clear affirmative action to consent to the use of personal data. The GDPR does not allow controllers to offer pre -ticked boxes or opt -out constructions that require an intervention from the data subject to prevent agreement (for example ‘opt-out boxes’).44

[3] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.4, paragraph 90, page 20 | similarity 0.71
Heading: Unambiguous indication of wishes
90. In any event, consent must always be obtained before the controller starts processing personal data for which consent is needed. WP29 has consistently held in its opinions that consent should be given prior to the processing activity. 46 Although the GDPR does not literally prescribe in Article 4(11) that consent must be given prior to the processing activity, this is clearly implied. The heading of Article 6(1) and the wording “has given” in Article 6(1)(a) support this interpretation. It follows logically from Article 6 and Recital 40 that a valid lawful basis must be present before starting a data processing. Therefore, consent should be given prior to the processing activity. In principle, it can be sufficient to ask for a data subject’s consent once. However, controllers do need to obtain a new and specific consent if purposes for data processing change after consent was obtained or if an additional purpose is envisaged.

[4] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.1, paragraphs 13-14, page 7 | similarity 0.71
Heading: Free / freely given
13. The element “free” implies real choice and control for data subjects. As a general rule, the GDPR prescribes that if the data subject has no real choice, feels compelled to consent or will endure negative consequences if they do not consent, then consen t will not be valid. 13 If consent is bundled up as a non-negotiable part of terms and conditions it is presumed not to have been freely given. Accordingly, consent will not be considered to be free if the data subject is unable to refuse or withdraw his or her consent without detriment.14 The notion of imbalance between the controller and the data subject is also taken into consideration by the GDPR. 14. When assessing whether consent is freely given, one should also take into account the specific situation of tying consent into contracts or the provision of a service as described in Article 7(4). Article 7(4) has been drafted in a non -exhaustive fashion by the words “inter alia”, meaning that there may be a range of other situations, which are caught by this prov ision. In general terms, any element of inappropriate pressure or influence upon the data subject (which may be manifested in many different ways) which prevents a data subject from exercising their free will, shall render the consent invalid.

[5] Source: edpb_consent (EDPB Guidelines 05/2020 on consent) | Location: Section 3.3, page 15 | similarity 0.71
Heading: Informed
62. The GDPR reinforces the requirement that consent must be informed. Based on Article 5 of the GDPR, the requirement for transparency is one of the fundamental principles, closely related to the principles of fairness and lawfulness. Providing information to data subjects prior to obtaining their consent is essential in order to enable them to make informed decisions, understand what they are agreeing to, and for example exercis e their right to withdraw their consent. If the controller does not provide accessible information, user control becomes illusory and consent will be an invalid basis for processing. 63. The consequence of not complying with the requirements for informed consent is that consent will be invalid and the controller may be in breach of Article 6 of the GDPR.
```

</details>
