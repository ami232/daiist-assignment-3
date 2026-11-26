# Grading sheet (no judge verdicts here)

Grade each answer in eval/human_labels.csv: `correct` (1/0) against the reference, `supported` (1/0) every claim is in the retrieved text, `notes` for every 0.


---

## q01 (single)

**Question:** We're launching an online shop. Can we use a customer's address to ship their order without a separate opt-in?

**Reference:** Yes, if necessary to perform the customer contract.

**Expected:** GDPR Article 6

**Agent's answer:**

Yes, you can use a customer's address to ship their order without a separate opt-in (consent), provided that processing the address is necessary for the performance of the contract (i.e., fulfilling the purchase made by the customer) [GDPR, Article 6].

Under the GDPR, processing is lawful if it is "necessary for the performance of a contract to which the data subject is party or in order to take steps at the request of the data subject prior to entering into a contract" [GDPR, Article 6]. Therefore, collecting and using delivery details for order fulfillment does not require separate consent [GDPR, Article 6].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [GDPR, Article 6] (part 1 of 3)  relevance 0.6952
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 6 — Lawfulness of processing (part 1 of 3)
1. Processing shall be lawful only if and to the extent that at least one of the following applies: (a) the data subject has given consent to the processing of his or her personal data for one or more specific purposes; (b) processing is necessary for the performance of a contract to which the data subject is party or in order to take steps at the request of the data subject prior to entering into a contract; (c) processing is necessary for compliance with a legal obligation to which the controller is subject; (d) processing is necessary in order to protect the vital interests of the data subject or of another natural person; (e) processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller; (f) processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject which require protection of personal data, in particular where the data subject is a child. Point (f) of the first subparagraph shall not apply to processing carried out by public authorities in the performance of their tasks.
2. Member States may maintain or introduce more specific provisions to adapt the application of the rules of this Regulation with regard to processing for compliance with points (c) and (e) of paragraph 1 by determining more precisely specific requirements for the processing and other measures to ensure lawful and fair processing including for other specific processing situations as provided for in Chapter IX.

---

Result 2  cite as [GDPR, Article 7]  relevance 0.6878
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 7 — Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data.
2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding.
3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.
4. When assessing whether consent is freely given, utmost account shall be taken of whether, inter alia, the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

---

Result 3  cite as [ePrivacy Directive, Article 9]  relevance 0.6815
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 9 — Location data other than traffic data
1. Where location data other than traffic data, relating to users or subscribers of public communications networks or publicly available electronic communications services, can be processed, such data may only be processed when they are made anonymous, or with the consent of the users or subscribers to the extent and for the duration necessary for the provision of a value added service. The service provider must inform the users or subscribers, prior to obtaining their consent, of the type of location data other than traffic data which will be processed, of the purposes and duration of the processing and whether the data will be transmitted to a third party for the purpose of providing the value added service. Users or subscribers shall be given the possibility to withdraw their consent for the processing of location data other than traffic data at any time.
2. Where consent of the users or subscribers has been obtained for the processing of location data other than traffic data, the user or subscriber must continue to have the possibility, using a simple means and free of charge, of temporarily refusing the processing of such data for each connection to the network or for each transmission of a communication.
3. Processing of location data other than traffic data in accordance with paragraphs 1 and 2 must be restricted to persons acting under the authority of the provider of the public communications network or publicly available communications service or of the third party providing the value added service, and must be restricted to what is necessary for the purposes of providing the value added service.

---

Result 4  cite as [ePrivacy Directive, Article 6]  relevance 0.6784
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 6 — Traffic data
1. Traffic data relating to subscribers and users processed and stored by the provider of a public communications network or publicly available electronic communications service must be erased or made anonymous when it is no longer needed for the purpose of the transmission of a communication without prejudice to paragraphs 2, 3 and 5 of this Article and Article 15(1).
2. Traffic data necessary for the purposes of subscriber billing and interconnection payments may be processed. Such processing is permissible only up to the end of the period during which the bill may lawfully be challenged or payment pursued.
3. For the purpose of marketing electronic communications services or for the provision of value added services, the provider of a publicly available electronic communications service may process the data referred to in paragraph 1 to the extent and for the duration necessary for such services or marketing, if the subscriber or user to whom the data relate has given his or her prior consent. Users or subscribers shall be given the possibility to withdraw their consent for the processing of traffic data at any time.
4. The service provider must inform the subscriber or user of the types of traffic data which are processed and of the duration of such processing for the purposes mentioned in paragraph 2 and, prior to obtaining consent, for the purposes mentioned in paragraph 3.
5. Processing of traffic data, in accordance with paragraphs 1, 2, 3 and 4, must be restricted to persons acting under the authority of providers of the public communications networks and publicly available electronic communications services handling billing or traffic management, customer enquiries, fraud detection, marketing electronic communications services or providing a value added service, and must be restricted to what is necessary for the purposes of such activities.
6. Paragraphs 1, 2, 3 and 5 shall apply without prejudice to the possibility for competent bodies to be informed of traffic data in conformity with applicable legislation with a view to settling disputes, in particular interconnection or billing disputes.

---

Result 5  cite as [ePrivacy Directive, Article 2]  relevance 0.6698
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 2 — Definitions
Save as oth
```
</details>


---

## q02 (single)

**Question:** Our newsletter subscriber changes their mind. Can we make unsubscribing harder than signing up?

**Reference:** No; withdrawing consent must be as easy as giving it.

**Expected:** GDPR Article 7

**Agent's answer:**

No, you cannot make unsubscribing harder than signing up. 

If newsletter subscriptions are based on consent, the GDPR explicitly requires that **it shall be as easy to withdraw as to give consent** [GDPR, Article 7(3)]. Furthermore, for direct marketing communications, data subjects have the right to object to processing at any time [GDPR, Article 21(2)], and in the context of information society services, they must be able to exercise this right by automated means using technical specifications [GDPR, Article 21(5)]. 

Making the unsubscribe process more burdensome or difficult than the sign-up process violates these requirements.

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [GDPR, Article 21]  relevance 0.7902
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 21 — Right to object
1. The data subject shall have the right to object, on grounds relating to his or her particular situation, at any time to processing of personal data concerning him or her which is based on point (e) or (f) of Article 6(1), including profiling based on those provisions. The controller shall no longer process the personal data unless the controller demonstrates compelling legitimate grounds for the processing which override the interests, rights and freedoms of the data subject or for the establishment, exercise or defence of legal claims.
2. Where personal data are processed for direct marketing purposes, the data subject shall have the right to object at any time to processing of personal data concerning him or her for such marketing, which includes profiling to the extent that it is related to such direct marketing.
3. Where the data subject objects to processing for direct marketing purposes, the personal data shall no longer be processed for such purposes.
4. At the latest at the time of the first communication with the data subject, the right referred to in paragraphs 1 and 2 shall be explicitly brought to the attention of the data subject and shall be presented clearly and separately from any other information.
5. In the context of the use of information society services, and notwithstanding Directive 2002/58/EC, the data subject may exercise his or her right to object by automated means using technical specifications.
6. Where personal data are processed for scientific or historical research purposes or statistical purposes pursuant to Article 89(1), the data subject, on grounds relating to his or her particular situation, shall have the right to object to processing of personal data concerning him or her, unless the processing is necessary for the performance of a task carried out for reasons of public interest.

---

Result 2  cite as [GDPR, Article 7]  relevance 0.7422
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 7 — Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data.
2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding.
3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.
4. When assessing whether consent is freely given, utmost account shall be taken of whether, inter alia, the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

---

Result 3  cite as [GDPR, Article 17]  relevance 0.7275
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 17 — Right to erasure (‘right to be forgotten’)
1. The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay and the controller shall have the obligation to erase personal data without undue delay where one of the following grounds applies: (a) the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed; (b) the data subject withdraws consent on which the processing is based according to point (a) of Article 6(1), or point (a) of Article 9(2), and where there is no other legal ground for the processing; (c) the data subject objects to the processing pursuant to Article 21(1) and there are no overriding legitimate grounds for the processing, or the data subject objects to the processing pursuant to Article 21(2); (d) the personal data have been unlawfully processed; (e) the personal data have to be erased for compliance with a legal obligation in Union or Member State law to which the controller is subject; (f) the personal data have been collected in relation to the offer of information society services referred to in Article 8(1).
2. Where the controller has made the personal data public and is obliged pursuant to paragraph 1 to erase the personal data, the controller, taking account of available technology and the cost of implementation, shall take reasonable steps, including technical measures, to inform controllers which are processing the personal data that the data subject has requested the erasure by such controllers of any links to, or copy or replication of, those personal data.
3. Paragraphs 1 and 2 shall not apply to the extent that processing is necessary: (a) for exercising the right of freedom of expression and information; (b) for compliance with a legal obligation which requires processing by Union or Member State law to which the controller is subject or for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller; (c) for reasons of public interest in the area of public health in accordance with points (h) and (i) of Article 9(2) as well as Article 9(3); (d) for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) in so far as the right referred to in paragraph 1 is likely to render impossible or seriously impair the achievement of the objectives of that processing; or (e) for the establishment, exercise or defence of legal claims.

---

Result 4  cite as [GDPR, Article 18]  relevance 0.7105
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 18 — Right to restriction of processing
1. The data subject shall have the right to obtain from the controller restriction of processing where one of the following applies: (a) the accuracy of the personal data is contested by the data subject, for a period enabling the controller to verify the accuracy of the personal data; (b) the processing is unlawful and the data subject opposes the erasure of the personal data and requests the restriction of their use instead; (c) the controller no longer needs the personal data for the purposes of the processing, but they are required by the data subject for the establishment, exercise or defence of legal claims; (d) the data subject has objected to processing pursuant to Article 21(1) pending the verification whether the legitimate grounds of the controller override those of the data subject.
2. Where processing has been restricted under paragraph 1, such personal data shall, with the exception of storage, only be processed with the data subject's consent or for the establishment, exercise or defence of legal claims or for the protection of the rights of another natural or legal person or for reasons of important public interest of the Union or of a Member State.
3. A data subject who has obtained restriction of processing pursuant to paragraph 1 shall be informed by the controller before the restriction of processing is lifted.

---

Result 5  cite as [GDPR, Article 6] (part 1 of 3)  relevan
```
</details>


---

## q03 (single)

**Question:** We're a US app tracking the online behaviour of people in France. Does having no EU office exempt us from GDPR?

**Reference:** No; monitoring behaviour occurring in the EU brings the relevant processing within scope.

**Expected:** GDPR Article 3

**Agent's answer:**

No, having no EU office does not exempt you from the GDPR. 

The GDPR applies to controllers or processors not established in the Union when their processing activities are related to the monitoring of the behaviour of data subjects who are in the Union, as far as that behaviour takes place within the Union [GDPR, Article 3]. 

Since your US-based app is tracking the online behavior of individuals located in France (who are in the EU), your activities fall within the territorial scope of the GDPR regardless of your lack of an EU establishment [GDPR, Article 3].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [GDPR, Article 3]  relevance 0.7867
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 3 — Territorial scope
1. This Regulation applies to the processing of personal data in the context of the activities of an establishment of a controller or a processor in the Union, regardless of whether the processing takes place in the Union or not.
2. This Regulation applies to the processing of personal data of data subjects who are in the Union by a controller or processor not established in the Union, where the processing activities are related to: (a) the offering of goods or services, irrespective of whether a payment of the data subject is required, to such data subjects in the Union; or (b) the monitoring of their behaviour as far as their behaviour takes place within the Union.
3. This Regulation applies to the processing of personal data by a controller not established in the Union, but in a place where Member State law applies by virtue of public international law.

---

Result 2  cite as [GDPR, Article 2]  relevance 0.7632
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 2 — Material scope
1. This Regulation applies to the processing of personal data wholly or partly by automated means and to the processing other than by automated means of personal data which form part of a filing system or are intended to form part of a filing system.
2. This Regulation does not apply to the processing of personal data: (a) in the course of an activity which falls outside the scope of Union law; (b) by the Member States when carrying out activities which fall within the scope of Chapter 2 of Title V of the TEU; (c) by a natural person in the course of a purely personal or household activity; (d) by competent authorities for the purposes of the prevention, investigation, detection or prosecution of criminal offences or the execution of criminal penalties, including the safeguarding against and the prevention of threats to public security.
3. For the processing of personal data by the Union institutions, bodies, offices and agencies, Regulation (EC) No 45/2001 applies. Regulation (EC) No 45/2001 and other Union legal acts applicable to such processing of personal data shall be adapted to the principles and rules of this Regulation in accordance with Article 98.
4. This Regulation shall be without prejudice to the application of Directive 2000/31/EC, in particular of the liability rules of intermediary service providers in Articles 12 to 15 of that Directive.

---

Result 3  cite as [AI Act, Article 2] (part 1 of 3)  relevance 0.7332
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 2 — Scope (part 1 of 3)
1. This Regulation applies to: (a) providers placing on the market or putting into service AI systems or placing on the market general-purpose AI models in the Union, irrespective of whether those providers are established or located within the Union or in a third country; (b) deployers of AI systems that have their place of establishment or are located within the Union; (c) providers and deployers of AI systems that have their place of establishment or are located in a third country, where the output produced by the AI system is used in the Union; (d) importers and distributors of AI systems; (e) product manufacturers placing on the market or putting into service an AI system together with their product and under their own name or trademark; (f) authorised representatives of providers, which are not established in the Union; (g) affected persons that are located in the Union.
2. For AI systems classified as high-risk AI systems in accordance with Article 6(1) related to products covered by the Union harmonisation legislation listed in Section B of Annex I, only Article 6(1), Articles 102 to 109 and Article 112 apply. Article 57 applies only in so far as the requirements for high-risk AI systems under this Regulation have been integrated in that Union harmonisation legislation.

---

Result 4  cite as [GDPR, Article 55]  relevance 0.7232
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 55 — Competence
1. Each supervisory authority shall be competent for the performance of the tasks assigned to and the exercise of the powers conferred on it in accordance with this Regulation on the territory of its own Member State.
2. Where processing is carried out by public authorities or private bodies acting on the basis of point (c) or (e) of Article 6(1), the supervisory authority of the Member State concerned shall be competent. In such cases Article 56 does not apply.
3. Supervisory authorities shall not be competent to supervise processing operations of courts acting in their judicial capacity.

---

Result 5  cite as [ePrivacy Directive, Article 1]  relevance 0.7226
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 1 — Scope and aim
1. This Directive provides for the harmonisation of the national provisions required to ensure an equivalent level of protection of fundamental rights and freedoms, and in particular the right to privacy and confidentiality, with respect to the processing of personal data in the electronic communication sector and to ensure the free movement of such data and of electronic communication equipment and services in the Community.
2. The provisions of this Directive particularise and complement Directive 95/46/EC for the purposes mentioned in paragraph 1. Moreover, they provide for protection of the legitimate interests of subscribers who are legal persons.
3. This Directive shall not apply to activities which fall outside the scope of the Treaty establishing the European Community, such as those covered by Titles V and VI of the Treaty on European Union, and in any case to activities concerning public security, defence, State security (including the economic well-being of the State when the activities relate to State security matters) and the activities of the State in areas of criminal law.
```
</details>


---

## q04 (single)

**Question:** A customer asks us for a copy of their personal data. Can we charge for the first copy as standard?

**Reference:** No; the first copy is free, with a reasonable administrative fee possible for further copies.

**Expected:** GDPR Article 15

**Agent's answer:**

No, you cannot charge for the first copy as standard. 

Under the GDPR, actions taken regarding a data subject's right of access (Article 15) must be provided **free of charge** [GDPR, Article 12]. While you may charge a reasonable fee based on administrative costs for any *further* copies requested by the data subject, the first copy must always be free [GDPR, Article 15].

**Exception:** You may only charge a fee for a request (or refuse to act on it) if the request is **manifestly unfounded or excessive**, particularly because of its repetitive character. In such cases, the burden of proof rests on you as the controller to demonstrate that the request is manifestly unfounded or excessive [GDPR, Article 12].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [GDPR, Article 12] (part 2 of 2)  relevance 0.7085
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 12 — Transparent information, communication and modalities for the exercise of the rights of the data subject (part 2 of 2)
5. Information provided under Articles 13 and 14 and any communication and any actions taken under Articles 15 to 22 and 34 shall be provided free of charge. Where requests from a data subject are manifestly unfounded or excessive, in particular because of their repetitive character, the controller may either: (a) charge a reasonable fee taking into account the administrative costs of providing the information or communication or taking the action requested; or (b) refuse to act on the request. The controller shall bear the burden of demonstrating the manifestly unfounded or excessive character of the request.
6. Without prejudice to Article 11, where the controller has reasonable doubts concerning the identity of the natural person making the request referred to in Articles 15 to 21, the controller may request the provision of additional information necessary to confirm the identity of the data subject.
7. The information to be provided to data subjects pursuant to Articles 13 and 14 may be provided in combination with standardised icons in order to give in an easily visible, intelligible and clearly legible manner a meaningful overview of the intended processing. Where the icons are presented electronically they shall be machine-readable.
8. The Commission shall be empowered to adopt delegated acts in accordance with Article 92 for the purpose of determining the information to be presented by the icons and the procedures for providing standardised icons.

---

Result 2  cite as [GDPR, Article 15]  relevance 0.7052
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 15 — Right of access by the data subject
1. The data subject shall have the right to obtain from the controller confirmation as to whether or not personal data concerning him or her are being processed, and, where that is the case, access to the personal data and the following information: (a) the purposes of the processing; (b) the categories of personal data concerned; (c) the recipients or categories of recipient to whom the personal data have been or will be disclosed, in particular recipients in third countries or international organisations; (d) where possible, the envisaged period for which the personal data will be stored, or, if not possible, the criteria used to determine that period; (e) the existence of the right to request from the controller rectification or erasure of personal data or restriction of processing of personal data concerning the data subject or to object to such processing; (f) the right to lodge a complaint with a supervisory authority; (g) where the personal data are not collected from the data subject, any available information as to their source; (h) the existence of automated decision-making, including profiling, referred to in Article 22(1) and (4) and, at least in those cases, meaningful information about the logic involved, as well as the significance and the envisaged consequences of such processing for the data subject.
2. Where personal data are transferred to a third country or to an international organisation, the data subject shall have the right to be informed of the appropriate safeguards pursuant to Article 46 relating to the transfer.
3. The controller shall provide a copy of the personal data undergoing processing. For any further copies requested by the data subject, the controller may charge a reasonable fee based on administrative costs. Where the data subject makes the request by electronic means, and unless otherwise requested by the data subject, the information shall be provided in a commonly used electronic form.
4. The right to obtain a copy referred to in paragraph 3 shall not adversely affect the rights and freedoms of others.

---

Result 3  cite as [GDPR, Article 20]  relevance 0.6687
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 20 — Right to data portability
1. The data subject shall have the right to receive the personal data concerning him or her, which he or she has provided to a controller, in a structured, commonly used and machine-readable format and have the right to transmit those data to another controller without hindrance from the controller to which the personal data have been provided, where: (a) the processing is based on consent pursuant to point (a) of Article 6(1) or point (a) of Article 9(2) or on a contract pursuant to point (b) of Article 6(1); and (b) the processing is carried out by automated means.
2. In exercising his or her right to data portability pursuant to paragraph 1, the data subject shall have the right to have the personal data transmitted directly from one controller to another, where technically feasible.
3. The exercise of the right referred to in paragraph 1 of this Article shall be without prejudice to Article 17. That right shall not apply to processing necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller.
4. The right referred to in paragraph 1 shall not adversely affect the rights and freedoms of others.

---

Result 4  cite as [GDPR, Article 12] (part 1 of 2)  relevance 0.665
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 12 — Transparent information, communication and modalities for the exercise of the rights of the data subject (part 1 of 2)
1. The controller shall take appropriate measures to provide any information referred to in Articles 13 and 14 and any communication under Articles 15 to 22 and 34 relating to processing to the data subject in a concise, transparent, intelligible and easily accessible form, using clear and plain language, in particular for any information addressed specifically to a child. The information shall be provided in writing, or by other means, including, where appropriate, by electronic means. When requested by the data subject, the information may be provided orally, provided that the identity of the data subject is proven by other means.
2. The controller shall facilitate the exercise of data subject rights under Articles 15 to 22. In the cases referred to in Article 11(2), the controller shall not refuse to act on the request of the data subject for exercising his or her rights under Articles 15 to 22, unless the controller demonstrates that it is not in a position to identify the data subject.
3. The controller shall provide information on action taken on a request under Articles 15 to 22 to the data subject without undue delay and in any event within one month of receipt of the request. That period may be extended by two further months where necessary, taking into account the complexity and number of the requests. The controller shall inform the data subject of any such extension within one month of receipt of the request, together with the reasons for the delay. Where the data subject makes the request by electronic form means, the information shall be provided by electronic means where possible, unless otherwise requested by the data subject.
4. If the controller does not take action on the request of the data subject, the controller shall inform the data subject without delay and at the latest within one month of receipt of the request of the reasons for not taking action and on the possibility of lodging a complaint with a supervisory authority and seeking a judicial remedy.

---

Result 5  cite as [
```
</details>


---

## q05 (single)

**Question:** Our startup has 20 staff and processes customer data every day. Can we skip keeping processing records just because we're small?

**Reference:** No; the small-organisation exemption does not cover non-occasional processing.

**Expected:** GDPR Article 30

**Agent's answer:**

No, you cannot skip keeping records of processing activities simply because your startup has fewer than 250 employees. 

While enterprises and organisations employing fewer than 250 persons are generally exempt from the record-keeping obligation, this exception does **not** apply if any of the following conditions are met [GDPR, Article 30(5)]:

1. **Risk:** The processing is likely to result in a risk to the rights and freedoms of data subjects [GDPR, Article 30(5)].
2. **Not occasional:** The processing is **not occasional** [GDPR, Article 30(5)]. Because your startup processes customer data **every day**, your data processing activities are considered regular and continuous rather than occasional, meaning this exception will likely strip away your exemption.
3. **Special categories or criminal data:** The processing includes special categories of data (such as health data, biometric data, or ethnic origin) or personal data relating to criminal convictions and offences [GDPR, Article 30(5)].

Since you process customer data on a daily basis, your processing is not occasional. Therefore, you are required to maintain written records of your processing activities [GDPR, Article 30(1), Article 30(3), Article 30(5)].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [GDPR, Article 30]  relevance 0.8206
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 30 — Records of processing activities
1. Each controller and, where applicable, the controller's representative, shall maintain a record of processing activities under its responsibility. That record shall contain all of the following information: (a) the name and contact details of the controller and, where applicable, the joint controller, the controller's representative and the data protection officer; (b) the purposes of the processing; (c) a description of the categories of data subjects and of the categories of personal data; (d) the categories of recipients to whom the personal data have been or will be disclosed including recipients in third countries or international organisations; (e) where applicable, transfers of personal data to a third country or an international organisation, including the identification of that third country or international organisation and, in the case of transfers referred to in the second subparagraph of Article 49(1), the documentation of suitable safeguards; (f) where possible, the envisaged time limits for erasure of the different categories of data; (g) where possible, a general description of the technical and organisational security measures referred to in Article 32(1).
2. Each processor and, where applicable, the processor's representative shall maintain a record of all categories of processing activities carried out on behalf of a controller, containing: (a) the name and contact details of the processor or processors and of each controller on behalf of which the processor is acting, and, where applicable, of the controller's or the processor's representative, and the data protection officer; (b) the categories of processing carried out on behalf of each controller; (c) where applicable, transfers of personal data to a third country or an international organisation, including the identification of that third country or international organisation and, in the case of transfers referred to in the second subparagraph of Article 49(1), the documentation of suitable safeguards; (d) where possible, a general description of the technical and organisational security measures referred to in Article 32(1).
3. The records referred to in paragraphs 1 and 2 shall be in writing, including in electronic form.
4. The controller or the processor and, where applicable, the controller's or the processor's representative, shall make the record available to the supervisory authority on request.
5. The obligations referred to in paragraphs 1 and 2 shall not apply to an enterprise or an organisation employing fewer than 250 persons unless the processing it carries out is likely to result in a risk to the rights and freedoms of data subjects, the processing is not occasional, or the processing includes special categories of data as referred to in Article 9(1) or personal data relating to criminal convictions and offences referred to in Article 10.

---

Result 2  cite as [GDPR, Article 2]  relevance 0.7039
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 2 — Material scope
1. This Regulation applies to the processing of personal data wholly or partly by automated means and to the processing other than by automated means of personal data which form part of a filing system or are intended to form part of a filing system.
2. This Regulation does not apply to the processing of personal data: (a) in the course of an activity which falls outside the scope of Union law; (b) by the Member States when carrying out activities which fall within the scope of Chapter 2 of Title V of the TEU; (c) by a natural person in the course of a purely personal or household activity; (d) by competent authorities for the purposes of the prevention, investigation, detection or prosecution of criminal offences or the execution of criminal penalties, including the safeguarding against and the prevention of threats to public security.
3. For the processing of personal data by the Union institutions, bodies, offices and agencies, Regulation (EC) No 45/2001 applies. Regulation (EC) No 45/2001 and other Union legal acts applicable to such processing of personal data shall be adapted to the principles and rules of this Regulation in accordance with Article 98.
4. This Regulation shall be without prejudice to the application of Directive 2000/31/EC, in particular of the liability rules of intermediary service providers in Articles 12 to 15 of that Directive.

---

Result 3  cite as [GDPR, Article 29]  relevance 0.702
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 29 — Processing under the authority of the controller or processor
The processor and any person acting under the authority of the controller or of the processor, who has access to personal data, shall not process those data except on instructions from the controller, unless required to do so by Union or Member State law.

---

Result 4  cite as [GDPR, Article 27]  relevance 0.6995
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 27 — Representatives of controllers or processors not established in the Union
1. Where Article 3(2) applies, the controller or the processor shall designate in writing a representative in the Union.
2. The obligation laid down in paragraph 1 of this Article shall not apply to: (a) processing which is occasional, does not include, on a large scale, processing of special categories of data as referred to in Article 9(1) or processing of personal data relating to criminal convictions and offences referred to in Article 10, and is unlikely to result in a risk to the rights and freedoms of natural persons, taking into account the nature, context, scope and purposes of the processing; or (b) a public authority or body.
3. The representative shall be established in one of the Member States where the data subjects, whose personal data are processed in relation to the offering of goods or services to them, or whose behaviour is monitored, are.
4. The representative shall be mandated by the controller or processor to be addressed in addition to or instead of the controller or the processor by, in particular, supervisory authorities and data subjects, on all issues related to processing, for the purposes of ensuring compliance with this Regulation.
5. The designation of a representative by the controller or processor shall be without prejudice to legal actions which could be initiated against the controller or the processor themselves.

---

Result 5  cite as [GDPR, Article 5]  relevance 0.6954
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 5 — Principles relating to processing of personal data
1. Personal data shall be: (a) processed lawfully, fairly and in a transparent manner in relation to the data subject (‘lawfulness, fairness and transparency’); (b) collected for specified, explicit and legitimate purposes and not further processed in a manner that is incompatible with those purposes; further processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes shall, in accordance with Article 89(1), not be considered to be incompatible with the initial purposes (‘purpose limitation’); (c) adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed (‘data minimisation’); (d) accurate and, where necessary, kept up to date; every reasonable step must be ta
```
</details>


---

## q06 (single)

**Question:** We're transferring customer data to a country covered by an EU adequacy decision. Do we need separate transfer authorisation on that basis?

**Reference:** No, provided the transfer is covered by the decision.

**Expected:** GDPR Article 45

**Agent's answer:**

No, you do not need any specific transfer authorisation [GDPR, Article 45]. 

Under the GDPR, transfers of personal data to a third country or an international organisation that is covered by a European Commission adequacy decision do not require any specific authorisation from a supervisory authority [GDPR, Article 45].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [GDPR, Article 45] (part 1 of 3)  relevance 0.8137
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 45 — Transfers on the basis of an adequacy decision (part 1 of 3)
1. A transfer of personal data to a third country or an international organisation may take place where the Commission has decided that the third country, a territory or one or more specified sectors within that third country, or the international organisation in question ensures an adequate level of protection. Such a transfer shall not require any specific authorisation.
2. When assessing the adequacy of the level of protection, the Commission shall, in particular, take account of the following elements: (a) the rule of law, respect for human rights and fundamental freedoms, relevant legislation, both general and sectoral, including concerning public security, defence, national security and criminal law and the access of public authorities to personal data, as well as the implementation of such legislation, data protection rules, professional rules and security measures, including rules for the onward transfer of personal data to another third country or international organisation which are complied with in that country or international organisation, case-law, as well as effective and enforceable data subject rights and effective administrative and judicial redress for the data subjects whose personal data are being transferred; (b) the existence and effective functioning of one or more independent supervisory authorities in the third country or to which an international organisation is subject, with responsibility for ensuring and enforcing compliance with the data protection rules, including adequate enforcement powers, for assisting and advising the data subjects in exercising their rights and for cooperation with the supervisory authorities of the Member States; and (c) the international commitments the third country or international organisation concerned has entered into, or other obligations arising from legally binding conventions or instruments as well as from its participation in multilateral or regional systems, in particular in relation to the protection of personal data.

---

Result 2  cite as [GDPR, Article 45] (part 2 of 3)  relevance 0.789
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 45 — Transfers on the basis of an adequacy decision (part 2 of 3)
3. The Commission, after assessing the adequacy of the level of protection, may decide, by means of implementing act, that a third country, a territory or one or more specified sectors within a third country, or an international organisation ensures an adequate level of protection within the meaning of paragraph 2 of this Article. The implementing act shall provide for a mechanism for a periodic review, at least every four years, which shall take into account all relevant developments in the third country or international organisation. The implementing act shall specify its territorial and sectoral application and, where applicable, identify the supervisory authority or authorities referred to in point (b) of paragraph 2 of this Article. The implementing act shall be adopted in accordance with the examination procedure referred to in Article 93(2).
4. The Commission shall, on an ongoing basis, monitor developments in third countries and international organisations that could affect the functioning of decisions adopted pursuant to paragraph 3 of this Article and decisions adopted on the basis of Article 25(6) of Directive 95/46/EC.
5. The Commission shall, where available information reveals, in particular following the review referred to in paragraph 3 of this Article, that a third country, a territory or one or more specified sectors within a third country, or an international organisation no longer ensures an adequate level of protection within the meaning of paragraph 2 of this Article, to the extent necessary, repeal, amend or suspend the decision referred to in paragraph 3 of this Article by means of implementing acts without retro-active effect. Those implementing acts shall be adopted in accordance with the examination procedure referred to in Article 93(2). On duly justified imperative grounds of urgency, the Commission shall adopt immediately applicable implementing acts in accordance with the procedure referred to in Article 93(3).
6. The Commission shall enter into consultations with the third country or international organisation with a view to remedying the situation giving rise to the decision made pursuant to paragraph 5.

---

Result 3  cite as [GDPR, Article 45] (part 3 of 3)  relevance 0.7552
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 45 — Transfers on the basis of an adequacy decision (part 3 of 3)
7. A decision pursuant to paragraph 5 of this Article is without prejudice to transfers of personal data to the third country, a territory or one or more specified sectors within that third country, or the international organisation in question pursuant to Articles 46 to 49.
8. The Commission shall publish in the Official Journal of the European Union and on its website a list of the third countries, territories and specified sectors within a third country and international organisations for which it has decided that an adequate level of protection is or is no longer ensured.
9. Decisions adopted by the Commission on the basis of Article 25(6) of Directive 95/46/EC shall remain in force until amended, replaced or repealed by a Commission Decision adopted in accordance with paragraph 3 or 5 of this Article.

---

Result 4  cite as [GDPR, Article 46]  relevance 0.7527
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 46 — Transfers subject to appropriate safeguards
1. In the absence of a decision pursuant to Article 45(3), a controller or processor may transfer personal data to a third country or an international organisation only if the controller or processor has provided appropriate safeguards, and on condition that enforceable data subject rights and effective legal remedies for data subjects are available.
2. The appropriate safeguards referred to in paragraph 1 may be provided for, without requiring any specific authorisation from a supervisory authority, by: (a) a legally binding and enforceable instrument between public authorities or bodies; (b) binding corporate rules in accordance with Article 47; (c) standard data protection clauses adopted by the Commission in accordance with the examination procedure referred to in Article 93(2); (d) standard data protection clauses adopted by a supervisory authority and approved by the Commission pursuant to the examination procedure referred to in Article 93(2); (e) an approved code of conduct pursuant to Article 40 together with binding and enforceable commitments of the controller or processor in the third country to apply the appropriate safeguards, including as regards data subjects' rights; or (f) an approved certification mechanism pursuant to Article 42 together with binding and enforceable commitments of the controller or processor in the third country to apply the appropriate safeguards, including as regards data subjects' rights.
3. Subject to the authorisation from the competent supervisory authority, the appropriate safeguards referred to in paragraph 1 may also be provided for, in particular, by: (a) contractual clauses between the controller or processor and the controller, processor or the recipient of the personal data in the third country or international organisation; or (b) provisions to be inserted in
```
</details>


---

## q07 (single)

**Question:** Our DPO also advises us on compliance. Can our CEO instruct them what conclusion to reach in that role?

**Reference:** No; the DPO must not receive instructions about performing those tasks.

**Expected:** GDPR Article 38

**Agent's answer:**

No, the CEO cannot instruct the Data Protection Officer (DPO) what conclusions to reach [GDPR, Article 38]. 

The controller and processor must ensure that the DPO does not receive any instructions regarding the exercise of their tasks [GDPR, Article 38]. This includes advising on compliance and monitoring adherence to data protection laws [GDPR, Article 39]. Furthermore, the DPO must not be dismissed or penalized by the controller or processor for performing their tasks [GDPR, Article 38].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [GDPR, Article 38]  relevance 0.772
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 38 — Position of the data protection officer
1. The controller and the processor shall ensure that the data protection officer is involved, properly and in a timely manner, in all issues which relate to the protection of personal data.
2. The controller and processor shall support the data protection officer in performing the tasks referred to in Article 39 by providing resources necessary to carry out those tasks and access to personal data and processing operations, and to maintain his or her expert knowledge.
3. The controller and processor shall ensure that the data protection officer does not receive any instructions regarding the exercise of those tasks. He or she shall not be dismissed or penalised by the controller or the processor for performing his tasks. The data protection officer shall directly report to the highest management level of the controller or the processor.
4. Data subjects may contact the data protection officer with regard to all issues related to processing of their personal data and to the exercise of their rights under this Regulation.
5. The data protection officer shall be bound by secrecy or confidentiality concerning the performance of his or her tasks, in accordance with Union or Member State law.
6. The data protection officer may fulfil other tasks and duties. The controller or processor shall ensure that any such tasks and duties do not result in a conflict of interests.

---

Result 2  cite as [GDPR, Article 39]  relevance 0.7445
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 39 — Tasks of the data protection officer
1. The data protection officer shall have at least the following tasks: (a) to inform and advise the controller or the processor and the employees who carry out processing of their obligations pursuant to this Regulation and to other Union or Member State data protection provisions; (b) to monitor compliance with this Regulation, with other Union or Member State data protection provisions and with the policies of the controller or processor in relation to the protection of personal data, including the assignment of responsibilities, awareness-raising and training of staff involved in processing operations, and the related audits; (c) to provide advice where requested as regards the data protection impact assessment and monitor its performance pursuant to Article 35; (d) to cooperate with the supervisory authority; (e) to act as the contact point for the supervisory authority on issues relating to processing, including the prior consultation referred to in Article 36, and to consult, where appropriate, with regard to any other matter.
2. The data protection officer shall in the performance of his or her tasks have due regard to the risk associated with processing operations, taking into account the nature, scope, context and purposes of processing.

---

Result 3  cite as [GDPR, Article 37]  relevance 0.727
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 37 — Designation of the data protection officer
1. The controller and the processor shall designate a data protection officer in any case where: (a) the processing is carried out by a public authority or body, except for courts acting in their judicial capacity; (b) the core activities of the controller or the processor consist of processing operations which, by virtue of their nature, their scope and/or their purposes, require regular and systematic monitoring of data subjects on a large scale; or (c) the core activities of the controller or the processor consist of processing on a large scale of special categories of data pursuant to Article 9 and personal data relating to criminal convictions and offences referred to in Article 10.
2. A group of undertakings may appoint a single data protection officer provided that a data protection officer is easily accessible from each establishment.
3. Where the controller or the processor is a public authority or body, a single data protection officer may be designated for several such authorities or bodies, taking account of their organisational structure and size.
4. In cases other than those referred to in paragraph 1, the controller or processor or associations and other bodies representing categories of controllers or processors may or, where required by Union or Member State law shall, designate a data protection officer. The data protection officer may act for such associations and other bodies representing controllers or processors.
5. The data protection officer shall be designated on the basis of professional qualities and, in particular, expert knowledge of data protection law and practices and the ability to fulfil the tasks referred to in Article 39.
6. The data protection officer may be a staff member of the controller or processor, or fulfil the tasks on the basis of a service contract.
7. The controller or the processor shall publish the contact details of the data protection officer and communicate them to the supervisory authority.

---

Result 4  cite as [GDPR, Article 58] (part 2 of 3)  relevance 0.7252
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 58 — Powers (part 2 of 3)
2. Each supervisory authority shall have all of the following corrective powers: (a) to issue warnings to a controller or processor that intended processing operations are likely to infringe provisions of this Regulation; (b) to issue reprimands to a controller or a processor where processing operations have infringed provisions of this Regulation; (c) to order the controller or the processor to comply with the data subject's requests to exercise his or her rights pursuant to this Regulation; (d) to order the controller or processor to bring processing operations into compliance with the provisions of this Regulation, where appropriate, in a specified manner and within a specified period; (e) to order the controller to communicate a personal data breach to the data subject; (f) to impose a temporary or definitive limitation including a ban on processing; (g) to order the rectification or erasure of personal data or restriction of processing pursuant to Articles 16, 17 and 18 and the notification of such actions to recipients to whom the personal data have been disclosed pursuant to Article 17(2) and Article 19; (h) to withdraw a certification or to order the certification body to withdraw a certification issued pursuant to Articles 42 and 43, or to order the certification body not to issue certification if the requirements for the certification are not or are no longer met; (i) to impose an administrative fine pursuant to Article 83, in addition to, or instead of measures referred to in this paragraph, depending on the circumstances of each individual case; (j) to order the suspension of data flows to a recipient in a third country or to an international organisation.

---

Result 5  cite as [GDPR, Article 53]  relevance 0.71
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 53 — General conditions for the members of the supervisory authority
1. Member States shall provide for each member of their supervisory authorities to be appointed by means of a transparent procedure by: — their parliament; — their government; — their head of State; or — an independent body entrusted with the appointment under Member State law.
2. Each member shall have the qualifications, experience and skills, in partic
```
</details>


---

## q08 (single)

**Question:** Our HR team wants an AI tool that infers employees' emotions from facial expressions to measure engagement. Is that allowed?

**Reference:** No; workplace emotion inference is prohibited except for medical or safety reasons.

**Expected:** AI Act Article 5

**Agent's answer:**

No, this is generally **not allowed**. 

Under the Artificial Intelligence Act, the placing on the market, putting into service, or use of AI systems to **infer emotions of a natural person in the areas of the workplace** and educational institutions is strictly **prohibited** [AI Act, Article 5]. 

The only exception to this prohibition in the workplace is if the AI system is intended to be put on the market or put into service strictly for **medical or safety reasons** [AI Act, Article 5]. Measuring general employee engagement does not qualify as a medical or safety exemption.

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [AI Act, Article 5] (part 2 of 7)  relevance 0.7953
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 5 — Prohibited AI practices (part 2 of 7)
(d) the placing on the market, the putting into service for this specific purpose, or the use of an AI system for making risk assessments of natural persons in order to assess or predict the risk of a natural person committing a criminal offence, based solely on the profiling of a natural person or on assessing their personality traits and characteristics; this prohibition shall not apply to AI systems used to support the human assessment of the involvement of a person in a criminal activity, which is already based on objective and verifiable facts directly linked to a criminal activity;
(e) the placing on the market, the putting into service for this specific purpose, or the use of AI systems that create or expand facial recognition databases through the untargeted scraping of facial images from the internet or CCTV footage;
(f) the placing on the market, the putting into service for this specific purpose, or the use of AI systems to infer emotions of a natural person in the areas of workplace and education institutions, except where the use of the AI system is intended to be put in place or into the market for medical or safety reasons;
(g) the placing on the market, the putting into service for this specific purpose, or the use of biometric categorisation systems that categorise individually natural persons based on their biometric data to deduce or infer their race, political opinions, trade union membership, religious or philosophical beliefs, sex life or sexual orientation; this prohibition does not cover any labelling or filtering of lawfully acquired biometric datasets, such as images, based on biometric data or categorizing of biometric data in the area of law enforcement;

---

Result 2  cite as [AI Act, Article 5] (part 1 of 7)  relevance 0.7459
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 5 — Prohibited AI practices (part 1 of 7)
1. The following AI practices shall be prohibited:
(a) the placing on the market, the putting into service or the use of an AI system that deploys subliminal techniques beyond a person’s consciousness or purposefully manipulative or deceptive techniques, with the objective, or the effect of materially distorting the behaviour of a person or a group of persons by appreciably impairing their ability to make an informed decision, thereby causing them to take a decision that they would not have otherwise taken in a manner that causes or is reasonably likely to cause that person, another person or group of persons significant harm;
(b) the placing on the market, the putting into service or the use of an AI system that exploits any of the vulnerabilities of a natural person or a specific group of persons due to their age, disability or a specific social or economic situation, with the objective, or the effect, of materially distorting the behaviour of that person or a person belonging to that group in a manner that causes or is reasonably likely to cause that person or another person significant harm;
(c) the placing on the market, the putting into service or the use of AI systems for the evaluation or classification of natural persons or groups of persons over a certain period of time based on their social behaviour or known, inferred or predicted personal or personality characteristics, with the social score leading to either or both of the following: (i) detrimental or unfavourable treatment of certain natural persons or groups of persons in social contexts that are unrelated to the contexts in which the data was originally generated or collected; (ii) detrimental or unfavourable treatment of certain natural persons or groups of persons that is unjustified or disproportionate to their social behaviour or its gravity;

---

Result 3  cite as [AI Act, Article 5] (part 3 of 7)  relevance 0.7377
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 5 — Prohibited AI practices (part 3 of 7)
(h) the use of ‘real-time’ remote biometric identification systems in publicly accessible spaces for the purposes of law enforcement, unless and in so far as such use is strictly necessary for one of the following objectives: (i) the targeted search for specific victims of abduction, trafficking in human beings or sexual exploitation of human beings, as well as the search for missing persons; (ii) the prevention of a specific, substantial and imminent threat to the life or physical safety of natural persons or a genuine and present or genuine and foreseeable threat of a terrorist attack; (iii) the localisation or identification of a person suspected of having committed a criminal offence, for the purpose of conducting a criminal investigation or prosecution or executing a criminal penalty for offences referred to in Annex II and punishable in the Member State concerned by a custodial sentence or a detention order for a maximum period of at least four years.
Point (h) of the first subparagraph is without prejudice to Article 9 of Regulation (EU) 2016/679 for the processing of biometric data for purposes other than law enforcement.

---

Result 4  cite as [AI Act, Article 5] (part 5 of 7)  relevance 0.7336
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 5 — Prohibited AI practices (part 5 of 7)
3. For the purposes of paragraph 1, first subparagraph, point (h) and paragraph 2, each use for the purposes of law enforcement of a ‘real-time’ remote biometric identification system in publicly accessible spaces shall be subject to a prior authorisation granted by a judicial authority or an independent administrative authority whose decision is binding of the Member State in which the use is to take place, issued upon a reasoned request and in accordance with the detailed rules of national law referred to in paragraph 5. However, in a duly justified situation of urgency, the use of such system may be commenced without an authorisation provided that such authorisation is requested without undue delay, at the latest within 24 hours. If such authorisation is rejected, the use shall be stopped with immediate effect and all the data, as well as the results and outputs of that use shall be immediately discarded and deleted. The competent judicial authority or an independent administrative authority whose decision is binding shall grant the authorisation only where it is satisfied, on the basis of objective evidence or clear indications presented to it, that the use of the ‘real-time’ remote biometric identification system concerned is necessary for, and proportionate to, achieving one of the objectives specified in paragraph 1, first subparagraph, point (h), as identified in the request and, in particular, remains limited to what is strictly necessary concerning the period of time as well as the geographic and personal scope. In deciding on the request, that authority shall take into account the elements referred to in paragraph 2. No decision that produces an adverse legal effect on a person may be taken based solely on the output of the ‘real-time’ remote biometric identification system.

---

Result 5  cite as [AI Act, Article 26] (part 3 of 5)  relevance 0.7321
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 26 — Obligations of deployers of high-risk AI systems (part 3 of 5)
7. Before putting into service or using a high-risk AI system at the workplace, deployers who are employers shal
```
</details>


---

## q09 (single)

**Question:** We're building a high-risk AI product. Can we treat risk management as a one-time exercise before launch?

**Reference:** No; it must be an ongoing iterative process throughout the system lifecycle.

**Expected:** AI Act Article 9

**Agent's answer:**

No, you cannot treat risk management as a one-time pre-launch exercise. 

Under the AI Act, the risk management system for a high-risk AI product must be understood as a **continuous iterative process** that is planned, run, and maintained throughout the **entire lifecycle** of the system [AI Act, Article 9]. 

Key requirements for your risk management process include:
* **Ongoing Reviews:** It requires regular systematic reviews and updating [AI Act, Article 9].
* **Post-Market Integration:** Risk management must account for other risks that emerge based on data gathered from your post-market monitoring system [AI Act, Article 9].
* **Lifecycle Obligations:** Testing and risk measures must be maintained as part of an overarching quality management system that operates before, during, and after development [AI Act, Article 9, Article 17].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [AI Act, Article 9] (part 1 of 3)  relevance 0.8402
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 9 — Risk management system (part 1 of 3)
1. A risk management system shall be established, implemented, documented and maintained in relation to high-risk AI systems.
2. The risk management system shall be understood as a continuous iterative process planned and run throughout the entire lifecycle of a high-risk AI system, requiring regular systematic review and updating. It shall comprise the following steps: (a) the identification and analysis of the known and the reasonably foreseeable risks that the high-risk AI system can pose to health, safety or fundamental rights when the high-risk AI system is used in accordance with its intended purpose; (b) the estimation and evaluation of the risks that may emerge when the high-risk AI system is used in accordance with its intended purpose, and under conditions of reasonably foreseeable misuse; (c) the evaluation of other risks possibly arising, based on the analysis of data gathered from the post-market monitoring system referred to in Article 72; (d) the adoption of appropriate and targeted risk management measures designed to address the risks identified pursuant to point (a).
3. The risks referred to in this Article shall concern only those which may be reasonably mitigated or eliminated through the development or design of the high-risk AI system, or the provision of adequate technical information.
4. The risk management measures referred to in paragraph 2, point (d), shall give due consideration to the effects and possible interaction resulting from the combined application of the requirements set out in this Section, with a view to minimising risks more effectively while achieving an appropriate balance in implementing the measures to fulfil those requirements.

---

Result 2  cite as [AI Act, Article 9] (part 2 of 3)  relevance 0.786
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 9 — Risk management system (part 2 of 3)
5. The risk management measures referred to in paragraph 2, point (d), shall be such that the relevant residual risk associated with each hazard, as well as the overall residual risk of the high-risk AI systems is judged to be acceptable. In identifying the most appropriate risk management measures, the following shall be ensured: (a) elimination or reduction of risks identified and evaluated pursuant to paragraph 2 in as far as technically feasible through adequate design and development of the high-risk AI system; (b) where appropriate, implementation of adequate mitigation and control measures addressing risks that cannot be eliminated; (c) provision of information required pursuant to Article 13 and, where appropriate, training to deployers. With a view to eliminating or reducing risks related to the use of the high-risk AI system, due consideration shall be given to the technical knowledge, experience, education, the training to be expected by the deployer, and the presumable context in which the system is intended to be used.
6. High-risk AI systems shall be tested for the purpose of identifying the most appropriate and targeted risk management measures. Testing shall ensure that high-risk AI systems perform consistently for their intended purpose and that they are in compliance with the requirements set out in this Section.
7. Testing procedures may include testing in real-world conditions in accordance with Article 60.
8. The testing of high-risk AI systems shall be performed, as appropriate, at any time throughout the development process, and, in any event, prior to their being placed on the market or put into service. Testing shall be carried out against prior defined metrics and probabilistic thresholds that are appropriate to the intended purpose of the high-risk AI system.
9. When implementing the risk management system as provided for in paragraphs 1 to 7, providers shall give consideration to whether in view of its intended purpose the high-risk AI system is likely to have an adverse impact on persons under the age of 18 and, as appropriate, other vulnerable groups.

---

Result 3  cite as [AI Act, Article 17] (part 1 of 2)  relevance 0.7831
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 17 — Quality management system (part 1 of 2)
1. Providers of high-risk AI systems shall put a quality management system in place that ensures compliance with this Regulation. That system shall be documented in a systematic and orderly manner in the form of written policies, procedures and instructions, and shall include at least the following aspects:
(a) a strategy for regulatory compliance, including compliance with conformity assessment procedures and procedures for the management of modifications to the high-risk AI system;
(b) techniques, procedures and systematic actions to be used for the design, design control and design verification of the high-risk AI system;
(c) techniques, procedures and systematic actions to be used for the development, quality control and quality assurance of the high-risk AI system;
(d) examination, test and validation procedures to be carried out before, during and after the development of the high-risk AI system, and the frequency with which they have to be carried out;
(e) technical specifications, including standards, to be applied and, where the relevant harmonised standards are not applied in full or do not cover all of the relevant requirements set out in Section 2, the means to be used to ensure that the high-risk AI system complies with those requirements;
(f) systems and procedures for data management, including data acquisition, data collection, data analysis, data labelling, data storage, data filtration, data mining, data aggregation, data retention and any other operation regarding the data that is performed before and for the purpose of the placing on the market or the putting into service of high-risk AI systems;
(g) the risk management system referred to in Article 9;
(h) the setting-up, implementation and maintenance of a post-market monitoring system, in accordance with Article 72;
(i) procedures related to the reporting of a serious incident in accordance with Article 73;
(j) the handling of communication with national competent authorities, other relevant authorities, including those providing or supporting the access to data, notified bodies, other operators, customers or other interested parties;
(k) systems and procedures for record-keeping of all relevant documentation and information;
(l) resource management, including security-of-supply related measures;

---

Result 4  cite as [AI Act, Article 72]  relevance 0.7745
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 72 — Post-market monitoring by providers and post-market monitoring plan for high-risk AI systems
1. Providers shall establish and document a post-market monitoring system in a manner that is proportionate to the nature of the AI technologies and the risks of the high-risk AI system.
2. The post-market monitoring system shall actively and systematically collect, document and analyse relevant data which may be provided by deployers or which may be collected through other sources on the performance of high-risk AI systems throughout their lifetime, and which allow the provider to evaluate the continuous compliance of AI systems with the requirements set out in Chapter III, Section 2. Where relevant, post-market monitoring shall include an analysis of the interaction with other AI systems. This obligation shall not cover sensitive operational dat
```
</details>


---

## q10 (single)

**Question:** We're selling a high-risk AI tool. Do we need to design it so a human can stop it when necessary?

**Reference:** Yes; appropriate human oversight must enable intervention or stopping the system where appropriate.

**Expected:** AI Act Article 14

**Agent's answer:**

Yes. As a provider of a high-risk AI system, you must design and develop the tool in such a way that natural persons assigned to human oversight are enabled, as appropriate and proportionate, to **intervene in the operation of the system or interrupt it through a "stop" button or a similar procedure** that allows the system to come to a halt in a safe state [AI Act, Article 14]. 

The oversight measures—including the means to intervene or stop the system—must be built into the high-risk AI system before it is placed on the market or put into service, where technically feasible, and must be commensurate with the risks, level of autonomy, and context of use of the system [AI Act, Article 14].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [AI Act, Article 14] (part 2 of 2)  relevance 0.8145
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 14 — Human oversight (part 2 of 2)
4. For the purpose of implementing paragraphs 1, 2 and 3, the high-risk AI system shall be provided to the deployer in such a way that natural persons to whom human oversight is assigned are enabled, as appropriate and proportionate: (a) to properly understand the relevant capacities and limitations of the high-risk AI system and be able to duly monitor its operation, including in view of detecting and addressing anomalies, dysfunctions and unexpected performance; (b) to remain aware of the possible tendency of automatically relying or over-relying on the output produced by a high-risk AI system (automation bias), in particular for high-risk AI systems used to provide information or recommendations for decisions to be taken by natural persons; (c) to correctly interpret the high-risk AI system’s output, taking into account, for example, the interpretation tools and methods available; (d) to decide, in any particular situation, not to use the high-risk AI system or to otherwise disregard, override or reverse the output of the high-risk AI system; (e) to intervene in the operation of the high-risk AI system or interrupt the system through a ‘stop’ button or a similar procedure that allows the system to come to a halt in a safe state.
5. For high-risk AI systems referred to in point 1(a) of Annex III, the measures referred to in paragraph 3 of this Article shall be such as to ensure that, in addition, no action or decision is taken by the deployer on the basis of the identification resulting from the system unless that identification has been separately verified and confirmed by at least two natural persons with the necessary competence, training and authority. The requirement for a separate verification by at least two natural persons shall not apply to high-risk AI systems used for the purposes of law enforcement, migration, border control or asylum, where Union or national law considers the application of this requirement to be disproportionate.

---

Result 2  cite as [AI Act, Article 14] (part 1 of 2)  relevance 0.7953
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 14 — Human oversight (part 1 of 2)
1. High-risk AI systems shall be designed and developed in such a way, including with appropriate human-machine interface tools, that they can be effectively overseen by natural persons during the period in which they are in use.
2. Human oversight shall aim to prevent or minimise the risks to health, safety or fundamental rights that may emerge when a high-risk AI system is used in accordance with its intended purpose or under conditions of reasonably foreseeable misuse, in particular where such risks persist despite the application of other requirements set out in this Section.
3. The oversight measures shall be commensurate with the risks, level of autonomy and context of use of the high-risk AI system, and shall be ensured through either one or both of the following types of measures: (a) measures identified and built, when technically feasible, into the high-risk AI system by the provider before it is placed on the market or put into service; (b) measures identified by the provider before placing the high-risk AI system on the market or putting it into service and that are appropriate to be implemented by the deployer.

---

Result 3  cite as [AI Act, Article 26] (part 1 of 5)  relevance 0.7359
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 26 — Obligations of deployers of high-risk AI systems (part 1 of 5)
1. Deployers of high-risk AI systems shall take appropriate technical and organisational measures to ensure they use such systems in accordance with the instructions for use accompanying the systems, pursuant to paragraphs 3 and 6.
2. Deployers shall assign human oversight to natural persons who have the necessary competence, training and authority, as well as the necessary support.
3. The obligations set out in paragraphs 1 and 2, are without prejudice to other deployer obligations under Union or national law and to the deployer’s freedom to organise its own resources and activities for the purpose of implementing the human oversight measures indicated by the provider.
4. Without prejudice to paragraphs 1 and 2, to the extent the deployer exercises control over the input data, that deployer shall ensure that input data is relevant and sufficiently representative in view of the intended purpose of the high-risk AI system.

---

Result 4  cite as [AI Act, Article 20]  relevance 0.7286
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 20 — Corrective actions and duty of information
1. Providers of high-risk AI systems which consider or have reason to consider that a high-risk AI system that they have placed on the market or put into service is not in conformity with this Regulation shall immediately take the necessary corrective actions to bring that system into conformity, to withdraw it, to disable it, or to recall it, as appropriate. They shall inform the distributors of the high-risk AI system concerned and, where applicable, the deployers, the authorised representative and importers accordingly.
2. Where the high-risk AI system presents a risk within the meaning of Article 79(1) and the provider becomes aware of that risk, it shall immediately investigate the causes, in collaboration with the reporting deployer, where applicable, and inform the market surveillance authorities competent for the high-risk AI system concerned and, where applicable, the notified body that issued a certificate for that high-risk AI system in accordance with Article 44, in particular, of the nature of the non-compliance and of any relevant corrective action taken.

---

Result 5  cite as [AI Act, Article 26] (part 2 of 5)  relevance 0.7245
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 26 — Obligations of deployers of high-risk AI systems (part 2 of 5)
5. Deployers shall monitor the operation of the high-risk AI system on the basis of the instructions for use and, where relevant, inform providers in accordance with Article 72. Where deployers have reason to consider that the use of the high-risk AI system in accordance with the instructions may result in that AI system presenting a risk within the meaning of Article 79(1), they shall, without undue delay, inform the provider or distributor and the relevant market surveillance authority, and shall suspend the use of that system. Where deployers have identified a serious incident, they shall also immediately inform first the provider, and then the importer or distributor and the relevant market surveillance authorities of that incident. If the deployer is not able to reach the provider, Article 73 shall apply mutatis mutandis. This obligation shall not cover sensitive operational data of deployers of AI systems which are law enforcement authorities. For deployers that are financial institutions subject to requirements regarding their internal governance, arrangements or processes under Union financial services law, the monitoring obligation set out in the first subparagraph shall be deemed to be fulfilled by complying with the rules on internal governance arrangements, processes and mechanisms pursuant to the relevant financial service law.
6. Deployers of high-risk AI systems shall keep the logs automatically generated by that high-risk AI system to the ext
```
</details>


---

## q11 (single)

**Question:** We're providing a customer support chatbot that users could mistake for a human. Do we need to tell them it's AI?

**Reference:** Yes; users must be informed unless this is obvious to a reasonably informed and observant person in context.

**Expected:** AI Act Article 50

**Agent's answer:**

Yes. Under the Artificial Intelligence Act, providers of AI systems intended to interact directly with natural persons must ensure that users are informed that they are interacting with an AI system, unless it is already obvious from the perspective of a reasonably well-informed, observant, and circumspect user given the circumstances and context of use [AI Act, Article 50]. 

Since your users could mistake the chatbot for a human, it is not obvious that they are interacting with AI. Therefore, you must inform them in a clear and distinguishable manner at the latest at the time of the first interaction [AI Act, Article 50].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [AI Act, Article 50] (part 1 of 3)  relevance 0.7454
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 50 — Transparency obligations for providers and deployers of certain AI systems (part 1 of 3)
1. Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system, unless this is obvious from the point of view of a natural person who is reasonably well-informed, observant and circumspect, taking into account the circumstances and the context of use. This obligation shall not apply to AI systems authorised by law to detect, prevent, investigate or prosecute criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, unless those systems are available for the public to report a criminal offence.
2. Providers of AI systems, including general-purpose AI systems, generating synthetic audio, image, video or text content, shall ensure that the outputs of the AI system are marked in a machine-readable format and detectable as artificially generated or manipulated. Providers shall ensure their technical solutions are effective, interoperable, robust and reliable as far as this is technically feasible, taking into account the specificities and limitations of various types of content, the costs of implementation and the generally acknowledged state of the art, as may be reflected in relevant technical standards. This obligation shall not apply to the extent the AI systems perform an assistive function for standard editing or do not substantially alter the input data provided by the deployer or the semantics thereof, or where authorised by law to detect, prevent, investigate or prosecute criminal offences.
3. Deployers of an emotion recognition system or a biometric categorisation system shall inform the natural persons exposed thereto of the operation of the system, and shall process the personal data in accordance with Regulations (EU) 2016/679 and (EU) 2018/1725 and Directive (EU) 2016/680, as applicable. This obligation shall not apply to AI systems used for biometric categorisation and emotion recognition, which are permitted by law to detect, prevent or investigate criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, and in accordance with Union law.

---

Result 2  cite as [AI Act, Article 13] (part 1 of 2)  relevance 0.7149
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 13 — Transparency and provision of information to deployers (part 1 of 2)
1. High-risk AI systems shall be designed and developed in such a way as to ensure that their operation is sufficiently transparent to enable deployers to interpret a system’s output and use it appropriately. An appropriate type and degree of transparency shall be ensured with a view to achieving compliance with the relevant obligations of the provider and deployer set out in Section 3.
2. High-risk AI systems shall be accompanied by instructions for use in an appropriate digital format or otherwise that include concise, complete, correct and clear information that is relevant, accessible and comprehensible to deployers.
3. The instructions for use shall contain at least the following information:
(a) the identity and the contact details of the provider and, where applicable, of its authorised representative;
(b) the characteristics, capabilities and limitations of performance of the high-risk AI system, including: (i) its intended purpose; (ii) the level of accuracy, including its metrics, robustness and cybersecurity referred to in Article 15 against which the high-risk AI system has been tested and validated and which can be expected, and any known and foreseeable circumstances that may have an impact on that expected level of accuracy, robustness and cybersecurity; (iii) any known or foreseeable circumstance, related to the use of the high-risk AI system in accordance with its intended purpose or under conditions of reasonably foreseeable misuse, which may lead to risks to the health and safety or fundamental rights referred to in Article 9(2); (iv) where applicable, the technical capabilities and characteristics of the high-risk AI system to provide information that is relevant to explain its output; (v) when appropriate, its performance regarding specific persons or groups of persons on which the system is intended to be used; (vi) when appropriate, specifications for the input data, or any other relevant information in terms of the training, validation and testing data sets used, taking into account the intended purpose of the high-risk AI system; (vii) where applicable, information to enable deployers to interpret the output of the high-risk AI system and use it appropriately;

---

Result 3  cite as [AI Act, Article 50] (part 2 of 3)  relevance 0.706
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 50 — Transparency obligations for providers and deployers of certain AI systems (part 2 of 3)
4. Deployers of an AI system that generates or manipulates image, audio or video content constituting a deep fake, shall disclose that the content has been artificially generated or manipulated. This obligation shall not apply where the use is authorised by law to detect, prevent, investigate or prosecute criminal offence. Where the content forms part of an evidently artistic, creative, satirical, fictional or analogous work or programme, the transparency obligations set out in this paragraph are limited to disclosure of the existence of such generated or manipulated content in an appropriate manner that does not hamper the display or enjoyment of the work. Deployers of an AI system that generates or manipulates text which is published with the purpose of informing the public on matters of public interest shall disclose that the text has been artificially generated or manipulated. This obligation shall not apply where the use is authorised by law to detect, prevent, investigate or prosecute criminal offences or where the AI-generated content has undergone a process of human review or editorial control and where a natural or legal person holds editorial responsibility for the publication of the content.
5. The information referred to in paragraphs 1 to 4 shall be provided to the natural persons concerned in a clear and distinguishable manner at the latest at the time of the first interaction or exposure. The information shall conform to the applicable accessibility requirements.
6. Paragraphs 1 to 4 shall not affect the requirements and obligations set out in Chapter III, and shall be without prejudice to other transparency obligations laid down in Union or national law for deployers of AI systems.

---

Result 4  cite as [AI Act, Article 14] (part 1 of 2)  relevance 0.7027
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 14 — Human oversight (part 1 of 2)
1. High-risk AI systems shall be designed and developed in such a way, including with appropriate human-machine interface tools, that they can be effectively overseen by natural persons during the period in which they are in use.
2. Human oversight shall aim to prevent or minimise the risks to health, safety or fundamental rights that may emerge when a high-risk AI system is used in accordance with its intended purpose or under conditions of reasonably foreseeable misuse, in particular where such risks persist despite the application of other requirements set out in this Section.
3. The oversight measures shall
```
</details>


---

## q12 (single)

**Question:** We're providing a high-risk AI system and control its automatically generated logs. How long must we normally keep those logs?

**Reference:** At least six months, unless applicable Union or national law provides otherwise; the period must be appropriate to the intended purpose.

**Expected:** AI Act Article 19

**Agent's answer:**

As a provider of a high-risk AI system who controls its automatically generated logs, you must keep them for a period appropriate to the intended purpose of the system, which must be **at least six months**, unless otherwise provided by applicable Union or national law (such as data protection law) [AI Act, Article 19]. 

* **Exception for Financial Institutions:** If you are a financial institution subject to requirements regarding internal governance, arrangements, or processes under Union financial services law, you must instead maintain the automatically generated logs as part of the documentation kept under the relevant financial services law [AI Act, Article 19].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [AI Act, Article 19]  relevance 0.8667
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 19 — Automatically generated logs
1. Providers of high-risk AI systems shall keep the logs referred to in Article 12(1), automatically generated by their high-risk AI systems, to the extent such logs are under their control. Without prejudice to applicable Union or national law, the logs shall be kept for a period appropriate to the intended purpose of the high-risk AI system, of at least six months, unless provided otherwise in the applicable Union or national law, in particular in Union law on the protection of personal data.
2. Providers that are financial institutions subject to requirements regarding their internal governance, arrangements or processes under Union financial services law shall maintain the logs automatically generated by their high-risk AI systems as part of the documentation kept under the relevant financial services law.

---

Result 2  cite as [AI Act, Article 12]  relevance 0.8302
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 12 — Record-keeping
1. High-risk AI systems shall technically allow for the automatic recording of events (logs) over the lifetime of the system.
2. In order to ensure a level of traceability of the functioning of a high-risk AI system that is appropriate to the intended purpose of the system, logging capabilities shall enable the recording of events relevant for: (a) identifying situations that may result in the high-risk AI system presenting a risk within the meaning of Article 79(1) or in a substantial modification; (b) facilitating the post-market monitoring referred to in Article 72; and (c) monitoring the operation of high-risk AI systems referred to in Article 26(5).
3. For high-risk AI systems referred to in point 1 (a), of Annex III, the logging capabilities shall provide, at a minimum: (a) recording of the period of each use of the system (start date and time and end date and time of each use); (b) the reference database against which input data has been checked by the system; (c) the input data for which the search has led to a match; (d) the identification of the natural persons involved in the verification of the results, as referred to in Article 14(5).

---

Result 3  cite as [AI Act, Article 18]  relevance 0.7934
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 18 — Documentation keeping
1. The provider shall, for a period ending 10 years after the high-risk AI system has been placed on the market or put into service, keep at the disposal of the national competent authorities: (a) the technical documentation referred to in Article 11; (b) the documentation concerning the quality management system referred to in Article 17; (c) the documentation concerning the changes approved by notified bodies, where applicable; (d) the decisions and other documents issued by the notified bodies, where applicable; (e) the EU declaration of conformity referred to in Article 47.
2. Each Member State shall determine conditions under which the documentation referred to in paragraph 1 remains at the disposal of the national competent authorities for the period indicated in that paragraph for the cases when a provider or its authorised representative established on its territory goes bankrupt or ceases its activity prior to the end of that period.
3. Providers that are financial institutions subject to requirements regarding their internal governance, arrangements or processes under Union financial services law shall maintain the technical documentation as part of the documentation kept under the relevant Union financial services law.

---

Result 4  cite as [AI Act, Article 26] (part 2 of 5)  relevance 0.7676
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 26 — Obligations of deployers of high-risk AI systems (part 2 of 5)
5. Deployers shall monitor the operation of the high-risk AI system on the basis of the instructions for use and, where relevant, inform providers in accordance with Article 72. Where deployers have reason to consider that the use of the high-risk AI system in accordance with the instructions may result in that AI system presenting a risk within the meaning of Article 79(1), they shall, without undue delay, inform the provider or distributor and the relevant market surveillance authority, and shall suspend the use of that system. Where deployers have identified a serious incident, they shall also immediately inform first the provider, and then the importer or distributor and the relevant market surveillance authorities of that incident. If the deployer is not able to reach the provider, Article 73 shall apply mutatis mutandis. This obligation shall not cover sensitive operational data of deployers of AI systems which are law enforcement authorities. For deployers that are financial institutions subject to requirements regarding their internal governance, arrangements or processes under Union financial services law, the monitoring obligation set out in the first subparagraph shall be deemed to be fulfilled by complying with the rules on internal governance arrangements, processes and mechanisms pursuant to the relevant financial service law.
6. Deployers of high-risk AI systems shall keep the logs automatically generated by that high-risk AI system to the extent such logs are under their control, for a period appropriate to the intended purpose of the high-risk AI system, of at least six months, unless provided otherwise in applicable Union or national law, in particular in Union law on the protection of personal data. Deployers that are financial institutions subject to requirements regarding their internal governance, arrangements or processes under Union financial services law shall maintain the logs as part of the documentation kept pursuant to the relevant Union financial service law.

---

Result 5  cite as [AI Act, Article 47]  relevance 0.7435
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 47 — EU declaration of conformity
1. The provider shall draw up a written machine readable, physical or electronically signed EU declaration of conformity for each high-risk AI system, and keep it at the disposal of the national competent authorities for 10 years after the high-risk AI system has been placed on the market or put into service. The EU declaration of conformity shall identify the high-risk AI system for which it has been drawn up. A copy of the EU declaration of conformity shall be submitted to the relevant national competent authorities upon request.
2. The EU declaration of conformity shall state that the high-risk AI system concerned meets the requirements set out in Section 2. The EU declaration of conformity shall contain the information set out in Annex V, and shall be translated into a language that can be easily understood by the national competent authorities of the Member States in which the high-risk AI system is placed on the market or made available.
3. Where high-risk AI systems are subject to other Union harmonisation legislation which also requires an EU declaration of conformity, a single EU declaration of conformity shall be drawn up in respect of all Union law applicable to the high-risk AI system. The declaration shall contain all the information required to identify the Union harmonisation legislation to which the declaration relates.
4. By drawing up the EU declaration of conformity, the provider shall assume responsibility for compliance with the req
```
</details>


---

## q13 (single)

**Question:** We're releasing a proprietary general-purpose AI model. Do we need to publish a summary of its training content?

**Reference:** Yes; a sufficiently detailed public summary following the AI Office template is required.

**Expected:** AI Act Article 53

**Agent's answer:**

Yes. As a provider of a general-purpose AI model, you are required to draw up and make publicly available a sufficiently detailed summary about the content used for training your model [AI Act, Article 53]. 

This summary must be prepared in accordance with a template provided by the AI Office [AI Act, Article 53].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [AI Act, Article 53] (part 1 of 2)  relevance 0.8025
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 53 — Obligations for providers of general-purpose AI models (part 1 of 2)
1. Providers of general-purpose AI models shall: (a) draw up and keep up-to-date the technical documentation of the model, including its training and testing process and the results of its evaluation, which shall contain, at a minimum, the information set out in Annex XI for the purpose of providing it, upon request, to the AI Office and the national competent authorities; (b) draw up, keep up-to-date and make available information and documentation to providers of AI systems who intend to integrate the general-purpose AI model into their AI systems. Without prejudice to the need to observe and protect intellectual property rights and confidential business information or trade secrets in accordance with Union and national law, the information and documentation shall: (i) enable providers of AI systems to have a good understanding of the capabilities and limitations of the general-purpose AI model and to comply with their obligations pursuant to this Regulation; and (ii) contain, at a minimum, the elements set out in Annex XII; (c) put in place a policy to comply with Union law on copyright and related rights, and in particular to identify and comply with, including through state-of-the-art technologies, a reservation of rights expressed pursuant to Article 4(3) of Directive (EU) 2019/790; (d) draw up and make publicly available a sufficiently detailed summary about the content used for training of the general-purpose AI model, according to a template provided by the AI Office.
2. The obligations set out in paragraph 1, points (a) and (b), shall not apply to providers of AI models that are released under a free and open-source licence that allows for the access, usage, modification, and distribution of the model, and whose parameters, including the weights, the information on the model architecture, and the information on model usage, are made publicly available. This exception shall not apply to general-purpose AI models with systemic risks.
3. Providers of general-purpose AI models shall cooperate as necessary with the Commission and the national competent authorities in the exercise of their competences and powers pursuant to this Regulation.

---

Result 2  cite as [AI Act, Annex XI]  relevance 0.7608
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Annex XI — Technical documentation referred to in Article 53(1), point (a) — technical documentation for providers of general-purpose AI models
Section 1
Information to be provided by all providers of general-purpose AI models
The technical documentation referred to in Article 53(1), point (a) shall contain at least the following information as appropriate to the size and risk profile of the model:
1. A general description of the general-purpose AI model including: (a) the tasks that the model is intended to perform and the type and nature of AI systems in which it can be integrated; (b) the acceptable use policies applicable; (c) the date of release and methods of distribution; (d) the architecture and number of parameters; (e) the modality (e.g. text, image) and format of inputs and outputs; (f) the licence.
2. A detailed description of the elements of the model referred to in point 1, and relevant information of the process for the development, including the following elements: (a) the technical means (e.g. instructions of use, infrastructure, tools) required for the general-purpose AI model to be integrated in AI systems; (b) the design specifications of the model and training process, including training methodologies and techniques, the key design choices including the rationale and assumptions made; what the model is designed to optimise for and the relevance of the different parameters, as applicable; (c) information on the data used for training, testing and validation, where applicable, including the type and provenance of data and curation methodologies (e.g. cleaning, filtering, etc.), the number of data points, their scope and main characteristics; how the data was obtained and selected as well as all other measures to detect the unsuitability of data sources and methods to detect identifiable biases, where applicable; (d) the computational resources used to train the model (e.g. number of floating point operations), training time, and other relevant details related to the training; (e) known or estimated energy consumption of the model. With regard to point (e), where the energy consumption of the model is unknown, the energy consumption may be based on information about computational resources used.
Section 2
Additional information to be provided by providers of general-purpose AI models with systemic risk
1. A detailed description of the evaluation strategies, including evaluation results, on the basis of available public evaluation protocols and tools or otherwise of other evaluation methodologies. Evaluation strategies shall include evaluation criteria, metrics and the methodology on the identification of limitations.
2. Where applicable, a detailed description of the measures put in place for the purpose of conducting internal and/or external adversarial testing (e.g. red teaming), model adaptations, including alignment and fine-tuning.
3. Where applicable, a detailed description of the system architecture explaining how software components build or feed into each other and integrate into the overall processing.

---

Result 3  cite as [AI Act, Annex XIII]  relevance 0.7564
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Annex XIII — Criteria for the designation of general-purpose AI models with systemic risk referred to in Article 51
For the purpose of determining that a general-purpose AI model has capabilities or an impact equivalent to those set out in Article 51(1), point (a), the Commission shall take into account the following criteria:
(a) the number of parameters of the model;
(b) the quality or size of the data set, for example measured through tokens;
(c) the amount of computation used for training the model, measured in floating point operations or indicated by a combination of other variables such as estimated cost of training, estimated time required for the training, or estimated energy consumption for the training;
(d) the input and output modalities of the model, such as text to text (large language models), text to image, multi-modality, and the state of the art thresholds for determining high-impact capabilities for each modality, and the specific type of inputs and outputs (e.g. biological sequences);
(e) the benchmarks and evaluations of capabilities of the model, including considering the number of tasks without additional training, adaptability to learn new, distinct tasks, its level of autonomy and scalability, the tools it has access to;
(f) whether it has a high impact on the internal market due to its reach, which shall be presumed when it has been made available to at least 10 000 registered business users established in the Union;
(g) the number of registered end-users.

---

Result 4  cite as [AI Act, Article 51]  relevance 0.753
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 51 — Classification of general-purpose AI models as general-purpose AI models with systemic risk
1. A general-purpose AI model shall be classified as a general-purpose AI model with systemic risk if it meets any of the following conditions: (a) it has high impact capabilities evaluated on the basis of ap
```
</details>


---

## q14 (single)

**Question:** We're training a general-purpose AI model using more than 10^25 FLOPs. Does that trigger a presumption of high-impact capabilities?

**Reference:** Yes; exceeding that training compute threshold triggers the presumption.

**Expected:** AI Act Article 51

**Agent's answer:**

Yes. Under the AI Act, a general-purpose AI model is **presumed** to have high-impact capabilities when the cumulative amount of computation used for its training, measured in floating-point operations (FLOPs), is greater than $10^{25}$ [AI Act, Article 51]. 

Meeting this threshold also results in the model being classified as a general-purpose AI model with **systemic risk** [AI Act, Article 51].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [AI Act, Article 51]  relevance 0.7442
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 51 — Classification of general-purpose AI models as general-purpose AI models with systemic risk
1. A general-purpose AI model shall be classified as a general-purpose AI model with systemic risk if it meets any of the following conditions: (a) it has high impact capabilities evaluated on the basis of appropriate technical tools and methodologies, including indicators and benchmarks; (b) based on a decision of the Commission, ex officio or following a qualified alert from the scientific panel, it has capabilities or an impact equivalent to those set out in point (a) having regard to the criteria set out in Annex XIII.
2. A general-purpose AI model shall be presumed to have high impact capabilities pursuant to paragraph 1, point (a), when the cumulative amount of computation used for its training measured in floating point operations is greater than 10 25.
3. The Commission shall adopt delegated acts in accordance with Article 97 to amend the thresholds listed in paragraphs 1 and 2 of this Article, as well as to supplement benchmarks and indicators in light of evolving technological developments, such as algorithmic improvements or increased hardware efficiency, when necessary, for these thresholds to reflect the state of the art.

---

Result 2  cite as [AI Act, Article 3] (part 8 of 8)  relevance 0.7157
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 3 — Definitions (part 8 of 8)
(63) ‘general-purpose AI model’ means an AI model, including where such an AI model is trained with a large amount of data using self-supervision at scale, that displays significant generality and is capable of competently performing a wide range of distinct tasks regardless of the way the model is placed on the market and that can be integrated into a variety of downstream systems or applications, except AI models that are used for research, development or prototyping activities before they are placed on the market;
(64) ‘high-impact capabilities’ means capabilities that match or exceed the capabilities recorded in the most advanced general-purpose AI models;
(65) ‘systemic risk’ means a risk that is specific to the high-impact capabilities of general-purpose AI models, having a significant impact on the Union market due to their reach, or due to actual or reasonably foreseeable negative effects on public health, safety, public security, fundamental rights, or the society as a whole, that can be propagated at scale across the value chain;
(66) ‘general-purpose AI system’ means an AI system which is based on a general-purpose AI model and which has the capability to serve a variety of purposes, both for direct use as well as for integration in other AI systems;
(67) ‘floating-point operation’ means any mathematical operation or assignment involving floating-point numbers, which are a subset of the real numbers typically represented on computers by an integer of fixed precision scaled by an integer exponent of a fixed base;
(68) ‘downstream provider’ means a provider of an AI system, including a general-purpose AI system, which integrates an AI model, regardless of whether the AI model is provided by themselves and vertically integrated or provided by another entity based on contractual relations.

---

Result 3  cite as [AI Act, Annex XIII]  relevance 0.7097
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Annex XIII — Criteria for the designation of general-purpose AI models with systemic risk referred to in Article 51
For the purpose of determining that a general-purpose AI model has capabilities or an impact equivalent to those set out in Article 51(1), point (a), the Commission shall take into account the following criteria:
(a) the number of parameters of the model;
(b) the quality or size of the data set, for example measured through tokens;
(c) the amount of computation used for training the model, measured in floating point operations or indicated by a combination of other variables such as estimated cost of training, estimated time required for the training, or estimated energy consumption for the training;
(d) the input and output modalities of the model, such as text to text (large language models), text to image, multi-modality, and the state of the art thresholds for determining high-impact capabilities for each modality, and the specific type of inputs and outputs (e.g. biological sequences);
(e) the benchmarks and evaluations of capabilities of the model, including considering the number of tasks without additional training, adaptability to learn new, distinct tasks, its level of autonomy and scalability, the tools it has access to;
(f) whether it has a high impact on the internal market due to its reach, which shall be presumed when it has been made available to at least 10 000 registered business users established in the Union;
(g) the number of registered end-users.

---

Result 4  cite as [AI Act, Annex XI]  relevance 0.69
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Annex XI — Technical documentation referred to in Article 53(1), point (a) — technical documentation for providers of general-purpose AI models
Section 1
Information to be provided by all providers of general-purpose AI models
The technical documentation referred to in Article 53(1), point (a) shall contain at least the following information as appropriate to the size and risk profile of the model:
1. A general description of the general-purpose AI model including: (a) the tasks that the model is intended to perform and the type and nature of AI systems in which it can be integrated; (b) the acceptable use policies applicable; (c) the date of release and methods of distribution; (d) the architecture and number of parameters; (e) the modality (e.g. text, image) and format of inputs and outputs; (f) the licence.
2. A detailed description of the elements of the model referred to in point 1, and relevant information of the process for the development, including the following elements: (a) the technical means (e.g. instructions of use, infrastructure, tools) required for the general-purpose AI model to be integrated in AI systems; (b) the design specifications of the model and training process, including training methodologies and techniques, the key design choices including the rationale and assumptions made; what the model is designed to optimise for and the relevance of the different parameters, as applicable; (c) information on the data used for training, testing and validation, where applicable, including the type and provenance of data and curation methodologies (e.g. cleaning, filtering, etc.), the number of data points, their scope and main characteristics; how the data was obtained and selected as well as all other measures to detect the unsuitability of data sources and methods to detect identifiable biases, where applicable; (d) the computational resources used to train the model (e.g. number of floating point operations), training time, and other relevant details related to the training; (e) known or estimated energy consumption of the model. With regard to point (e), where the energy consumption of the model is unknown, the energy consumption may be based on information about computational resources used.
Section 2
Additional information to be provided by providers of general-purpose AI models with systemic risk
1. A detailed description of the evaluation strategies, including evaluation results, on the basis of available public evaluation protocols and tools or otherwise of other evaluati
```
</details>


---

## q15 (single)

**Question:** Our shopping site uses a cookie solely to remember items in the basket requested by the shopper. Do we need opt-in for that cookie?

**Reference:** No, if it is strictly necessary to provide the service explicitly requested by the user.

**Expected:** ePrivacy Directive Article 5

**Agent's answer:**

No, you do not need opt-in (consent) for that cookie. 

Under the ePrivacy Directive, storing information or gaining access to information already stored in a user's terminal equipment requires consent, **except** when it is strictly necessary in order for the provider to deliver an information society service that the subscriber or user has explicitly requested [ePrivacy Directive, Article 5(3)]. 

Because the cookie is used solely to remember the items in the basket requested by the shopper, it falls under this explicit exemption as storage strictly necessary to provide the requested shopping service.

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [ePrivacy Directive, Article 5]  relevance 0.7385
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 5 — Confidentiality of the communications
1. Member States shall ensure the confidentiality of communications and the related traffic data by means of a public communications network and publicly available electronic communications services, through national legislation. In particular, they shall prohibit listening, tapping, storage or other kinds of interception or surveillance of communications and the related traffic data by persons other than users, without the consent of the users concerned, except when legally authorised to do so in accordance with Article 15(1). This paragraph shall not prevent technical storage which is necessary for the conveyance of a communication without prejudice to the principle of confidentiality.
2. Paragraph 1 shall not affect any legally authorised recording of communications and the related traffic data when carried out in the course of lawful business practice for the purpose of providing evidence of a commercial transaction or of any other business communication.
3. Member States shall ensure that the storing of information, or the gaining of access to information already stored, in the terminal equipment of a subscriber or user is only allowed on condition that the subscriber or user concerned has given his or her consent, having been provided with clear and comprehensive information, in accordance with Directive 95/46/EC, inter alia, about the purposes of the processing. This shall not prevent any technical storage or access for the sole purpose of carrying out the transmission of a communication over an electronic communications network, or as strictly necessary in order for the provider of an information society service explicitly requested by the subscriber or user to provide the service.

---

Result 2  cite as [ePrivacy Directive, Article 1]  relevance 0.7311
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 1 — Scope and aim
1. This Directive provides for the harmonisation of the national provisions required to ensure an equivalent level of protection of fundamental rights and freedoms, and in particular the right to privacy and confidentiality, with respect to the processing of personal data in the electronic communication sector and to ensure the free movement of such data and of electronic communication equipment and services in the Community.
2. The provisions of this Directive particularise and complement Directive 95/46/EC for the purposes mentioned in paragraph 1. Moreover, they provide for protection of the legitimate interests of subscribers who are legal persons.
3. This Directive shall not apply to activities which fall outside the scope of the Treaty establishing the European Community, such as those covered by Titles V and VI of the Treaty on European Union, and in any case to activities concerning public security, defence, State security (including the economic well-being of the State when the activities relate to State security matters) and the activities of the State in areas of criminal law.

---

Result 3  cite as [ePrivacy Directive, Article 2]  relevance 0.7266
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 2 — Definitions
Save as otherwise provided, the definitions in Directive 95/46/EC and in Directive 2002/21/EC of the European Parliament and of the Council of 7 March 2002 on a common regulatory framework for electronic communications networks and services (Framework Directive) (8) shall apply.
The following definitions shall also apply:
(a) ‘user’ means any natural person using a publicly available electronic communications service, for private or business purposes, without necessarily having subscribed to this service;
(b) ‘traffic data’ means any data processed for the purpose of the conveyance of a communication on an electronic communications network or for the billing thereof;
(c) ‘location data’ means any data processed in an electronic communications network or by an electronic communications service, indicating the geographic position of the terminal equipment of a user of a publicly available electronic communications service;
(d) ‘communication’ means any information exchanged or conveyed between a finite number of parties by means of a publicly available electronic communications service. This does not include any information conveyed as part of a broadcasting service to the public over an electronic communications network except to the extent that the information can be related to the identifiable subscriber or user receiving the information;
(f) ‘consent’ by a user or subscriber corresponds to the data subject's consent in Directive 95/46/EC;
(g) ‘value added service’ means any service which requires the processing of traffic data or location data other than traffic data beyond what is necessary for the transmission of a communication or the billing thereof;
(h) ‘electronic mail’ means any text, voice, sound or image message sent over a public communications network which can be stored in the network or in the recipient's terminal equipment until it is collected by the recipient;
(i) ‘personal data breach’ means a breach of security leading to the accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to, personal data transmitted, stored or otherwise processed in connection with the provision of a publicly available electronic communications service in the Community.

---

Result 4  cite as [ePrivacy Directive, Article 6]  relevance 0.7159
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 6 — Traffic data
1. Traffic data relating to subscribers and users processed and stored by the provider of a public communications network or publicly available electronic communications service must be erased or made anonymous when it is no longer needed for the purpose of the transmission of a communication without prejudice to paragraphs 2, 3 and 5 of this Article and Article 15(1).
2. Traffic data necessary for the purposes of subscriber billing and interconnection payments may be processed. Such processing is permissible only up to the end of the period during which the bill may lawfully be challenged or payment pursued.
3. For the purpose of marketing electronic communications services or for the provision of value added services, the provider of a publicly available electronic communications service may process the data referred to in paragraph 1 to the extent and for the duration necessary for such services or marketing, if the subscriber or user to whom the data relate has given his or her prior consent. Users or subscribers shall be given the possibility to withdraw their consent for the processing of traffic data at any time.
4. The service provider must inform the subscriber or user of the types of traffic data which are processed and of the duration of such processing for the purposes mentioned in paragraph 2 and, prior to obtaining consent, for the purposes mentioned in paragraph 3.
5. Processing of traffic data, in accordance with paragraphs 1, 2, 3 and 4, must be restricted to persons acting under the authority of providers of the public communications networks and publicly available electronic communications services handling billing or traffic management, customer enquiries, fraud detection, marketing electronic communications services or providing a value added service, and must be rest
```
</details>


---

## q16 (single)

**Question:** We're a telecom operator. Can we keep traffic data indefinitely after it stops being needed to transmit calls, just in case it becomes useful?

**Reference:** No; erase or anonymise it when no longer needed for transmission, subject to the specified exceptions.

**Expected:** ePrivacy Directive Article 6

**Agent's answer:**

No, you cannot keep traffic data indefinitely "just in case it becomes useful." 

Under the ePrivacy Directive, traffic data relating to subscribers and users must be erased or made anonymous when it is no longer needed for the purpose of transmitting a communication [ePrivacy Directive, Article 6(1)]. 

Storage is permitted only under specific, limited exceptions:
* **Billing and Interconnection:** Traffic data necessary for subscriber billing and interconnection payments may be processed, but only up to the end of the period during which the bill may lawfully be challenged or payment pursued [ePrivacy Directive, Article 6(2)].
* **Marketing and Value-Added Services:** Traffic data may be processed for marketing electronic communications services or value-added services, but only to the extent and for the duration necessary, and **only with the prior consent** of the subscriber or user, who must be able to withdraw consent at any time [ePrivacy Directive, Article 6(3)].
* **Legal Restrictions:** Retention may also be required under specific lawful national legislative measures in accordance with Article 15(1) [ePrivacy Directive, Article 6(1)]. 

Retaining traffic data indefinitely for future, unspecified usefulness is not permitted.

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [ePrivacy Directive, Article 6]  relevance 0.8658
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 6 — Traffic data
1. Traffic data relating to subscribers and users processed and stored by the provider of a public communications network or publicly available electronic communications service must be erased or made anonymous when it is no longer needed for the purpose of the transmission of a communication without prejudice to paragraphs 2, 3 and 5 of this Article and Article 15(1).
2. Traffic data necessary for the purposes of subscriber billing and interconnection payments may be processed. Such processing is permissible only up to the end of the period during which the bill may lawfully be challenged or payment pursued.
3. For the purpose of marketing electronic communications services or for the provision of value added services, the provider of a publicly available electronic communications service may process the data referred to in paragraph 1 to the extent and for the duration necessary for such services or marketing, if the subscriber or user to whom the data relate has given his or her prior consent. Users or subscribers shall be given the possibility to withdraw their consent for the processing of traffic data at any time.
4. The service provider must inform the subscriber or user of the types of traffic data which are processed and of the duration of such processing for the purposes mentioned in paragraph 2 and, prior to obtaining consent, for the purposes mentioned in paragraph 3.
5. Processing of traffic data, in accordance with paragraphs 1, 2, 3 and 4, must be restricted to persons acting under the authority of providers of the public communications networks and publicly available electronic communications services handling billing or traffic management, customer enquiries, fraud detection, marketing electronic communications services or providing a value added service, and must be restricted to what is necessary for the purposes of such activities.
6. Paragraphs 1, 2, 3 and 5 shall apply without prejudice to the possibility for competent bodies to be informed of traffic data in conformity with applicable legislation with a view to settling disputes, in particular interconnection or billing disputes.

---

Result 2  cite as [ePrivacy Directive, Article 5]  relevance 0.7791
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 5 — Confidentiality of the communications
1. Member States shall ensure the confidentiality of communications and the related traffic data by means of a public communications network and publicly available electronic communications services, through national legislation. In particular, they shall prohibit listening, tapping, storage or other kinds of interception or surveillance of communications and the related traffic data by persons other than users, without the consent of the users concerned, except when legally authorised to do so in accordance with Article 15(1). This paragraph shall not prevent technical storage which is necessary for the conveyance of a communication without prejudice to the principle of confidentiality.
2. Paragraph 1 shall not affect any legally authorised recording of communications and the related traffic data when carried out in the course of lawful business practice for the purpose of providing evidence of a commercial transaction or of any other business communication.
3. Member States shall ensure that the storing of information, or the gaining of access to information already stored, in the terminal equipment of a subscriber or user is only allowed on condition that the subscriber or user concerned has given his or her consent, having been provided with clear and comprehensive information, in accordance with Directive 95/46/EC, inter alia, about the purposes of the processing. This shall not prevent any technical storage or access for the sole purpose of carrying out the transmission of a communication over an electronic communications network, or as strictly necessary in order for the provider of an information society service explicitly requested by the subscriber or user to provide the service.

---

Result 3  cite as [ePrivacy Directive, Article 2]  relevance 0.7784
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 2 — Definitions
Save as otherwise provided, the definitions in Directive 95/46/EC and in Directive 2002/21/EC of the European Parliament and of the Council of 7 March 2002 on a common regulatory framework for electronic communications networks and services (Framework Directive) (8) shall apply.
The following definitions shall also apply:
(a) ‘user’ means any natural person using a publicly available electronic communications service, for private or business purposes, without necessarily having subscribed to this service;
(b) ‘traffic data’ means any data processed for the purpose of the conveyance of a communication on an electronic communications network or for the billing thereof;
(c) ‘location data’ means any data processed in an electronic communications network or by an electronic communications service, indicating the geographic position of the terminal equipment of a user of a publicly available electronic communications service;
(d) ‘communication’ means any information exchanged or conveyed between a finite number of parties by means of a publicly available electronic communications service. This does not include any information conveyed as part of a broadcasting service to the public over an electronic communications network except to the extent that the information can be related to the identifiable subscriber or user receiving the information;
(f) ‘consent’ by a user or subscriber corresponds to the data subject's consent in Directive 95/46/EC;
(g) ‘value added service’ means any service which requires the processing of traffic data or location data other than traffic data beyond what is necessary for the transmission of a communication or the billing thereof;
(h) ‘electronic mail’ means any text, voice, sound or image message sent over a public communications network which can be stored in the network or in the recipient's terminal equipment until it is collected by the recipient;
(i) ‘personal data breach’ means a breach of security leading to the accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to, personal data transmitted, stored or otherwise processed in connection with the provision of a publicly available electronic communications service in the Community.

---

Result 4  cite as [ePrivacy Directive, Article 9]  relevance 0.765
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 9 — Location data other than traffic data
1. Where location data other than traffic data, relating to users or subscribers of public communications networks or publicly available electronic communications services, can be processed, such data may only be processed when they are made anonymous, or with the consent of the users or subscribers to the extent and for the duration necessary for the provision of a value added service. The service provider must inform the users or subscribers, prior to obtaining their consent, of the type of location data other than traffic data which will be processed, of the purposes and duration of the processing and whether the data will be transmitted to a third party for the purpose of providing the value added service. Users or subscribers shall be given the p
```
</details>


---

## q17 (single)

**Question:** We're a mobile network offering a location-based service. Can users temporarily turn off processing of their non-traffic location data after consenting?

**Reference:** Yes; they must have a simple free way to temporarily refuse processing for each connection or transmission.

**Expected:** ePrivacy Directive Article 9

**Agent's answer:**

Yes. After giving consent for the processing of location data other than traffic data for a value-added service, users must continue to have the possibility of **temporarily refusing** the processing of such data for each connection to the network or for each transmission of a communication [ePrivacy Directive, Article 9]. 

Additionally, users must be provided with:
* A simple means to temporarily refuse the processing [ePrivacy Directive, Article 9].
* The ability to do so free of charge [ePrivacy Directive, Article 9].
* The right to withdraw their consent completely at any time [ePrivacy Directive, Article 9].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [ePrivacy Directive, Article 9]  relevance 0.768
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 9 — Location data other than traffic data
1. Where location data other than traffic data, relating to users or subscribers of public communications networks or publicly available electronic communications services, can be processed, such data may only be processed when they are made anonymous, or with the consent of the users or subscribers to the extent and for the duration necessary for the provision of a value added service. The service provider must inform the users or subscribers, prior to obtaining their consent, of the type of location data other than traffic data which will be processed, of the purposes and duration of the processing and whether the data will be transmitted to a third party for the purpose of providing the value added service. Users or subscribers shall be given the possibility to withdraw their consent for the processing of location data other than traffic data at any time.
2. Where consent of the users or subscribers has been obtained for the processing of location data other than traffic data, the user or subscriber must continue to have the possibility, using a simple means and free of charge, of temporarily refusing the processing of such data for each connection to the network or for each transmission of a communication.
3. Processing of location data other than traffic data in accordance with paragraphs 1 and 2 must be restricted to persons acting under the authority of the provider of the public communications network or publicly available communications service or of the third party providing the value added service, and must be restricted to what is necessary for the purposes of providing the value added service.

---

Result 2  cite as [ePrivacy Directive, Article 6]  relevance 0.7227
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 6 — Traffic data
1. Traffic data relating to subscribers and users processed and stored by the provider of a public communications network or publicly available electronic communications service must be erased or made anonymous when it is no longer needed for the purpose of the transmission of a communication without prejudice to paragraphs 2, 3 and 5 of this Article and Article 15(1).
2. Traffic data necessary for the purposes of subscriber billing and interconnection payments may be processed. Such processing is permissible only up to the end of the period during which the bill may lawfully be challenged or payment pursued.
3. For the purpose of marketing electronic communications services or for the provision of value added services, the provider of a publicly available electronic communications service may process the data referred to in paragraph 1 to the extent and for the duration necessary for such services or marketing, if the subscriber or user to whom the data relate has given his or her prior consent. Users or subscribers shall be given the possibility to withdraw their consent for the processing of traffic data at any time.
4. The service provider must inform the subscriber or user of the types of traffic data which are processed and of the duration of such processing for the purposes mentioned in paragraph 2 and, prior to obtaining consent, for the purposes mentioned in paragraph 3.
5. Processing of traffic data, in accordance with paragraphs 1, 2, 3 and 4, must be restricted to persons acting under the authority of providers of the public communications networks and publicly available electronic communications services handling billing or traffic management, customer enquiries, fraud detection, marketing electronic communications services or providing a value added service, and must be restricted to what is necessary for the purposes of such activities.
6. Paragraphs 1, 2, 3 and 5 shall apply without prejudice to the possibility for competent bodies to be informed of traffic data in conformity with applicable legislation with a view to settling disputes, in particular interconnection or billing disputes.

---

Result 3  cite as [GDPR, Article 7]  relevance 0.7055
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 7 — Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data.
2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding.
3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.
4. When assessing whether consent is freely given, utmost account shall be taken of whether, inter alia, the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

---

Result 4  cite as [ePrivacy Directive, Article 10]  relevance 0.6883
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 10 — Exceptions
Member States shall ensure that there are transparent procedures governing the way in which a provider of a public communications network and/or a publicly available electronic communications service may override:
(a) the elimination of the presentation of calling line identification, on a temporary basis, upon application of a subscriber requesting the tracing of malicious or nuisance calls. In this case, in accordance with national law, the data containing the identification of the calling subscriber will be stored and be made available by the provider of a public communications network and/or publicly available electronic communications service;
(b) the elimination of the presentation of calling line identification and the temporary denial or absence of consent of a subscriber or user for the processing of location data, on a per-line basis for organisations dealing with emergency calls and recognised as such by a Member State, including law enforcement agencies, ambulance services and fire brigades, for the purpose of responding to such calls.

---

Result 5  cite as [GDPR, Article 18]  relevance 0.6853
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 18 — Right to restriction of processing
1. The data subject shall have the right to obtain from the controller restriction of processing where one of the following applies: (a) the accuracy of the personal data is contested by the data subject, for a period enabling the controller to verify the accuracy of the personal data; (b) the processing is unlawful and the data subject opposes the erasure of the personal data and requests the restriction of their use instead; (c) the controller no longer needs the personal data for the purposes of the processing, but they are required by the data subject for the establishment, exercise or defence of legal claims; (d) the dat
```
</details>


---

## q18 (single)

**Question:** We're publishing a public telephone directory. Can subscribers ask us to remove their details without paying?

**Reference:** Yes; subscribers can withdraw their personal data from the directory free of charge.

**Expected:** ePrivacy Directive Article 12

**Agent's answer:**

Yes. Subscribers who are natural persons must be given the opportunity to withdraw, verify, or correct their personal data from a public subscriber directory, and to not be included in it at all, **free of charge** [ePrivacy Directive, Article 12].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [ePrivacy Directive, Article 12]  relevance 0.7464
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 12 — Directories of subscribers
1. Member States shall ensure that subscribers are informed, free of charge and before they are included in the directory, about the purpose(s) of a printed or electronic directory of subscribers available to the public or obtainable through directory enquiry services, in which their personal data can be included and of any further usage possibilities based on search functions embedded in electronic versions of the directory.
2. Member States shall ensure that subscribers are given the opportunity to determine whether their personal data are included in a public directory, and if so, which, to the extent that such data are relevant for the purpose of the directory as determined by the provider of the directory, and to verify, correct or withdraw such data. Not being included in a public subscriber directory, verifying, correcting or withdrawing personal data from it shall be free of charge.
3. Member States may require that for any purpose of a public directory other than the search of contact details of persons on the basis of their name and, where necessary, a minimum of other identifiers, additional consent be asked of the subscribers.
4. Paragraphs 1 and 2 shall apply to subscribers who are natural persons. Member States shall also ensure, in the framework of Community law and applicable national legislation, that the legitimate interests of subscribers other than natural persons with regard to their entry in public directories are sufficiently protected.

---

Result 2  cite as [ePrivacy Directive, Article 16]  relevance 0.6947
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 16 — Transitional arrangements
1. Article 12 shall not apply to editions of directories already produced or placed on the market in printed or off-line electronic form before the national provisions adopted pursuant to this Directive enter into force.
2. Where the personal data of subscribers to fixed or mobile public voice telephony services have been included in a public subscriber directory in conformity with the provisions of Directive 95/46/EC and of Article 11 of Directive 97/66/EC before the national provisions adopted in pursuance of this Directive enter into force, the personal data of such subscribers may remain included in this public directory in its printed or electronic versions, including versions with reverse search functions, unless subscribers indicate otherwise, after having received complete information about purposes and options in accordance with Article 12 of this Directive.

---

Result 3  cite as [ePrivacy Directive, Article 7]  relevance 0.6815
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 7 — Itemised billing
1. Subscribers shall have the right to receive non-itemised bills.
2. Member States shall apply national provisions in order to reconcile the rights of subscribers receiving itemised bills with the right to privacy of calling users and called subscribers, for example by ensuring that sufficient alternative privacy enhancing methods of communications or payments are available to such users and subscribers.

---

Result 4  cite as [ePrivacy Directive, Article 10]  relevance 0.6557
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 10 — Exceptions
Member States shall ensure that there are transparent procedures governing the way in which a provider of a public communications network and/or a publicly available electronic communications service may override:
(a) the elimination of the presentation of calling line identification, on a temporary basis, upon application of a subscriber requesting the tracing of malicious or nuisance calls. In this case, in accordance with national law, the data containing the identification of the calling subscriber will be stored and be made available by the provider of a public communications network and/or publicly available electronic communications service;
(b) the elimination of the presentation of calling line identification and the temporary denial or absence of consent of a subscriber or user for the processing of location data, on a per-line basis for organisations dealing with emergency calls and recognised as such by a Member State, including law enforcement agencies, ambulance services and fire brigades, for the purpose of responding to such calls.

---

Result 5  cite as [ePrivacy Directive, Article 8]  relevance 0.6511
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 8 — Presentation and restriction of calling and connected line identification
1. Where presentation of calling line identification is offered, the service provider must offer the calling user the possibility, using a simple means and free of charge, of preventing the presentation of the calling line identification on a per-call basis. The calling subscriber must have this possibility on a per-line basis.
2. Where presentation of calling line identification is offered, the service provider must offer the called subscriber the possibility, using a simple means and free of charge for reasonable use of this function, of preventing the presentation of the calling line identification of incoming calls.
3. Where presentation of calling line identification is offered and where the calling line identification is presented prior to the call being established, the service provider must offer the called subscriber the possibility, using a simple means, of rejecting incoming calls where the presentation of the calling line identification has been prevented by the calling user or subscriber.
4. Where presentation of connected line identification is offered, the service provider must offer the called subscriber the possibility, using a simple means and free of charge, of preventing the presentation of the connected line identification to the calling user.
5. Paragraph 1 shall also apply with regard to calls to third countries originating in the Community. Paragraphs 2, 3 and 4 shall also apply to incoming calls originating in third countries.
6. Member States shall ensure that where presentation of calling and/or connected line identification is offered, the providers of publicly available electronic communications services inform the public thereof and of the possibilities set out in paragraphs 1, 2, 3 and 4.
```
</details>


---

## q19 (multi)

**Question:** Our customer database was leaked and identity theft is likely. When do we tell the regulator and when do we warn customers?

**Reference:** Notify the regulator without undue delay and where feasible within 72 hours of awareness unless risk is unlikely; notify affected people without undue delay where high risk is likely, subject to Article 34 exceptions.

**Expected:** GDPR;GDPR Article 33;Article 34

**Agent's answer:**

Based on the GDPR, your obligations and timelines are as follows:

### 1. When to tell the regulator (Supervisory Authority)
* **Timeline:** You must notify the competent supervisory authority **without undue delay and, where feasible, not later than 72 hours** after having become aware of the personal data breach [GDPR, Article 33(1)].
* **Exception:** Notification is not required if the breach is *unlikely* to result in a risk to the rights and freedoms of natural persons [GDPR, Article 33(1)]. However, given that identity theft is likely, this threshold is almost certainly met, so notification will be required.
* **Late notification:** If you cannot notify within 72 hours, the notification must be accompanied by reasons for the delay, and information can be provided in phases [GDPR, Article 33(1), (4)].

### 2. When to warn customers (Data Subjects)
* **Timeline:** When the personal data breach is likely to result in a **high risk** to the rights and freedoms of natural persons, you must communicate the breach to the data subjects **without undue delay** [GDPR, Article 34(1)]. (A scenario where identity theft is likely generally constitutes a high risk).
* **Content:** The communication to customers must be in clear and plain language and describe the nature of the breach, along with contact details for your DPO/contact point, likely consequences, and measures taken or recommended to mitigate adverse effects [GDPR, Article 34(2), Article 33(3)(b)–(d)].
* **Exceptions:** You do **not** have to inform customers if:
  * You implemented appropriate technical and organizational protection measures (such as robust encryption) that rendered the affected data unintelligible to unauthorized persons [GDPR, Article 34(3)(a)];
  * You took subsequent measures that ensure the high risk is no longer likely to materialize [GDPR, Article 34(3)(b)]; or
  * Informing every customer would involve **disproportionate effort**. In that case, you must issue a public communication or similar measure so that individuals are informed in an equally effective manner [GDPR, Article 34(3)(c)].

*Note: Even if you believe an exception applies, the supervisory authority can still require you to notify your customers after considering the likelihood of a high risk [GDPR, Article 34(4)].*

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [GDPR, Article 33]  relevance 0.7851
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 33 — Notification of a personal data breach to the supervisory authority
1. In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority competent in accordance with Article 55, unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where the notification to the supervisory authority is not made within 72 hours, it shall be accompanied by reasons for the delay.
2. The processor shall notify the controller without undue delay after becoming aware of a personal data breach.
3. The notification referred to in paragraph 1 shall at least: (a) describe the nature of the personal data breach including where possible, the categories and approximate number of data subjects concerned and the categories and approximate number of personal data records concerned; (b) communicate the name and contact details of the data protection officer or other contact point where more information can be obtained; (c) describe the likely consequences of the personal data breach; (d) describe the measures taken or proposed to be taken by the controller to address the personal data breach, including, where appropriate, measures to mitigate its possible adverse effects.
4. Where, and in so far as, it is not possible to provide the information at the same time, the information may be provided in phases without undue further delay.
5. The controller shall document any personal data breaches, comprising the facts relating to the personal data breach, its effects and the remedial action taken. That documentation shall enable the supervisory authority to verify compliance with this Article.

---

Result 2  cite as [GDPR, Article 34]  relevance 0.7737
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 34 — Communication of a personal data breach to the data subject
1. When the personal data breach is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall communicate the personal data breach to the data subject without undue delay.
2. The communication to the data subject referred to in paragraph 1 of this Article shall describe in clear and plain language the nature of the personal data breach and contain at least the information and measures referred to in points (b), (c) and (d) of Article 33(3).
3. The communication to the data subject referred to in paragraph 1 shall not be required if any of the following conditions are met: (a) the controller has implemented appropriate technical and organisational protection measures, and those measures were applied to the personal data affected by the personal data breach, in particular those that render the personal data unintelligible to any person who is not authorised to access it, such as encryption; (b) the controller has taken subsequent measures which ensure that the high risk to the rights and freedoms of data subjects referred to in paragraph 1 is no longer likely to materialise; (c) it would involve disproportionate effort. In such a case, there shall instead be a public communication or similar measure whereby the data subjects are informed in an equally effective manner.
4. If the controller has not already communicated the personal data breach to the data subject, the supervisory authority, having considered the likelihood of the personal data breach resulting in a high risk, may require it to do so or may decide that any of the conditions referred to in paragraph 3 are met.

---

Result 3  cite as [ePrivacy Directive, Article 4] (part 2 of 3)  relevance 0.7176
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 4 — Security of processing (part 2 of 3)
3. In the case of a personal data breach, the provider of publicly available electronic communications services shall, without undue delay, notify the personal data breach to the competent national authority. When the personal data breach is likely to adversely affect the personal data or privacy of a subscriber or individual, the provider shall also notify the subscriber or individual of the breach without undue delay. Notification of a personal data breach to a subscriber or individual concerned shall not be required if the provider has demonstrated to the satisfaction of the competent authority that it has implemented appropriate technological protection measures, and that those measures were applied to the data concerned by the security breach. Such technological protection measures shall render the data unintelligible to any person who is not authorised to access it. Without prejudice to the provider's obligation to notify subscribers and individuals concerned, if the provider has not already notified the subscriber or individual of the personal data breach, the competent national authority, having considered the likely adverse effects of the breach, may require it to do so. The notification to the subscriber or individual shall at least describe the nature of the personal data breach and the contact points where more information can be obtained, and shall recommend measures to mitigate the possible adverse effects of the personal data breach. The notification to the competent national authority shall, in addition, describe the consequences of, and the measures proposed or taken by the provider to address, the personal data breach.

---

Result 4  cite as [GDPR, Article 77]  relevance 0.6943
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 77 — Right to lodge a complaint with a supervisory authority
1. Without prejudice to any other administrative or judicial remedy, every data subject shall have the right to lodge a complaint with a supervisory authority, in particular in the Member State of his or her habitual residence, place of work or place of the alleged infringement if the data subject considers that the processing of personal data relating to him or her infringes this Regulation.
2. The supervisory authority with which the complaint has been lodged shall inform the complainant on the progress and the outcome of the complaint including the possibility of a judicial remedy pursuant to Article 78.

---

Result 5  cite as [GDPR, Article 66]  relevance 0.6901
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 66 — Urgency procedure
1. In exceptional circumstances, where a supervisory authority concerned considers that there is an urgent need to act in order to protect the rights and freedoms of data subjects, it may, by way of derogation from the consistency mechanism referred to in Articles 63, 64 and 65 or the procedure referred to in Article 60, immediately adopt provisional measures intended to produce legal effects on its own territory with a specified period of validity which shall not exceed three months. The supervisory authority shall, without delay, communicate those measures and the reasons for adopting them to the other supervisory authorities concerned, to the Board and to the Commission.
2. Where a supervisory authority has taken a measure pursuant to paragraph 1 and considers that final measures need urgently be adopted, it may request an urgent opinion or an urgent binding decision from the Board, giving reasons for requesting such opinion or decision.
3. Any su
```
</details>


---

## q20 (multi)

**Question:** We're building AI that scores job applicants to shortlist them. Is it high-risk if the scores materially influence selection, and do we need human oversight built in?

**Reference:** Yes; recruitment and candidate evaluation materially influencing decisions fall under high-risk classification; design for effective human oversight.

**Expected:** AI Act;AI Act;AI Act Article 6;Annex III;Article 14

**Agent's answer:**

**Yes, your AI system is considered high-risk, and yes, human oversight must be built in.**

### 1. Is it high-risk?
Yes. Under the AI Act, AI systems intended to be used for the recruitment or selection of natural persons—specifically to **analyse and filter job applications** and to **evaluate candidates**—are explicitly classified as high-risk AI systems [AI Act, Annex III]. Because your system scores applicants and its scores materially influence selection, it falls directly under this high-risk category.

### 2. Do you need human oversight built in?
Yes. High-risk AI systems must be designed and developed with appropriate human-machine interface tools so that they can be effectively overseen by natural persons [AI Act, Article 14]. 

Specifically:
* **Provider obligations:** As the developer/provider, you must build technical oversight measures into the system (or identify appropriate measures for the deployer to implement) [AI Act, Article 14]. The system must be provided in a way that enables designated individuals to understand its capacities and limitations, avoid automation bias, interpret outputs correctly, and retain the ability to disregard, override, reverse, or stop the system's decisions [AI Act, Article 14].
* **Deployer obligations:** Organizations using your AI system (deployers) are legally required to assign human oversight to competent, trained individuals, and ensure those overseers can actively monitor the system's operation and override its recommendations [AI Act, Article 14, AI Act, Article 26].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [AI Act, Article 14] (part 1 of 2)  relevance 0.797
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 14 — Human oversight (part 1 of 2)
1. High-risk AI systems shall be designed and developed in such a way, including with appropriate human-machine interface tools, that they can be effectively overseen by natural persons during the period in which they are in use.
2. Human oversight shall aim to prevent or minimise the risks to health, safety or fundamental rights that may emerge when a high-risk AI system is used in accordance with its intended purpose or under conditions of reasonably foreseeable misuse, in particular where such risks persist despite the application of other requirements set out in this Section.
3. The oversight measures shall be commensurate with the risks, level of autonomy and context of use of the high-risk AI system, and shall be ensured through either one or both of the following types of measures: (a) measures identified and built, when technically feasible, into the high-risk AI system by the provider before it is placed on the market or put into service; (b) measures identified by the provider before placing the high-risk AI system on the market or putting it into service and that are appropriate to be implemented by the deployer.

---

Result 2  cite as [AI Act, Article 14] (part 2 of 2)  relevance 0.7877
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 14 — Human oversight (part 2 of 2)
4. For the purpose of implementing paragraphs 1, 2 and 3, the high-risk AI system shall be provided to the deployer in such a way that natural persons to whom human oversight is assigned are enabled, as appropriate and proportionate: (a) to properly understand the relevant capacities and limitations of the high-risk AI system and be able to duly monitor its operation, including in view of detecting and addressing anomalies, dysfunctions and unexpected performance; (b) to remain aware of the possible tendency of automatically relying or over-relying on the output produced by a high-risk AI system (automation bias), in particular for high-risk AI systems used to provide information or recommendations for decisions to be taken by natural persons; (c) to correctly interpret the high-risk AI system’s output, taking into account, for example, the interpretation tools and methods available; (d) to decide, in any particular situation, not to use the high-risk AI system or to otherwise disregard, override or reverse the output of the high-risk AI system; (e) to intervene in the operation of the high-risk AI system or interrupt the system through a ‘stop’ button or a similar procedure that allows the system to come to a halt in a safe state.
5. For high-risk AI systems referred to in point 1(a) of Annex III, the measures referred to in paragraph 3 of this Article shall be such as to ensure that, in addition, no action or decision is taken by the deployer on the basis of the identification resulting from the system unless that identification has been separately verified and confirmed by at least two natural persons with the necessary competence, training and authority. The requirement for a separate verification by at least two natural persons shall not apply to high-risk AI systems used for the purposes of law enforcement, migration, border control or asylum, where Union or national law considers the application of this requirement to be disproportionate.

---

Result 3  cite as [AI Act, Annex III] (part 2 of 5)  relevance 0.7799
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Annex III — High-risk AI systems referred to in Article 6(2) (part 2 of 5)
4. Employment, workers’ management and access to self-employment: (a) AI systems intended to be used for the recruitment or selection of natural persons, in particular to place targeted job advertisements, to analyse and filter job applications, and to evaluate candidates; (b) AI systems intended to be used to make decisions affecting terms of work-related relationships, the promotion or termination of work-related contractual relationships, to allocate tasks based on individual behaviour or personal traits or characteristics or to monitor and evaluate the performance and behaviour of persons in such relationships.
5. Access to and enjoyment of essential private services and essential public services and benefits: (a) AI systems intended to be used by public authorities or on behalf of public authorities to evaluate the eligibility of natural persons for essential public assistance benefits and services, including healthcare services, as well as to grant, reduce, revoke, or reclaim such benefits and services; (b) AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score, with the exception of AI systems used for the purpose of detecting financial fraud; (c) AI systems intended to be used for risk assessment and pricing in relation to natural persons in the case of life and health insurance; (d) AI systems intended to evaluate and classify emergency calls by natural persons or to be used to dispatch, or to establish priority in the dispatching of, emergency first response services, including by police, firefighters and medical aid, as well as of emergency healthcare patient triage systems.

---

Result 4  cite as [AI Act, Article 26] (part 1 of 5)  relevance 0.7674
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 26 — Obligations of deployers of high-risk AI systems (part 1 of 5)
1. Deployers of high-risk AI systems shall take appropriate technical and organisational measures to ensure they use such systems in accordance with the instructions for use accompanying the systems, pursuant to paragraphs 3 and 6.
2. Deployers shall assign human oversight to natural persons who have the necessary competence, training and authority, as well as the necessary support.
3. The obligations set out in paragraphs 1 and 2, are without prejudice to other deployer obligations under Union or national law and to the deployer’s freedom to organise its own resources and activities for the purpose of implementing the human oversight measures indicated by the provider.
4. Without prejudice to paragraphs 1 and 2, to the extent the deployer exercises control over the input data, that deployer shall ensure that input data is relevant and sufficiently representative in view of the intended purpose of the high-risk AI system.

---

Result 5  cite as [AI Act, Annex III] (part 4 of 5)  relevance 0.7412
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Annex III — High-risk AI systems referred to in Article 6(2) (part 4 of 5)
7. Migration, asylum and border control management, in so far as their use is permitted under relevant Union or national law: (a) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies as polygraphs or similar tools; (b) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies to assess a risk, including a security risk, a risk of irregular migration, or a health risk, posed by a natural person who intends to enter or who has entered into the territory of a Member State; (c) AI systems intended to be used by or on behalf of competent public authorities or by Union institutions, bodies, offices or agencies to assist competent public authorities for the examination of applications for asylum, visa or resi
```
</details>


---

## q21 (multi)

**Question:** We're a bank using high-risk AI to automatically reject loan applicants without human involvement. What GDPR protection applies to applicants and what oversight must the AI provider design in?

**Reference:** Applicants have the right not to be subject to solely automated significantly affecting decisions unless an exception applies, with applicable safeguards; the provider must enable effective human oversight of the high-risk system.

**Expected:** GDPR;AI Act Article 22;Article 14

**Agent's answer:**

Based on the provided legislation, here are the protections that apply to loan applicants and the oversight requirements for high-risk AI systems:

### 1. GDPR Protections for Loan Applicants

* **Right not to be subject to solely automated decisions:** Loan applicants generally have the right not to be subject to a decision based *solely* on automated processing (including profiling) that produces legal effects or similarly significantly affects them [GDPR, Article 22(1)]. 
* **Exceptions to the prohibition:** This restriction does not apply if the decision is necessary for entering into or performing a contract between the applicant and the bank, is authorized by EU or Member State law, or is based on the applicant's explicit consent [GDPR, Article 22(2)].
* **Mandatory safeguards:** If an exception applies (such as contract necessity), the bank must implement suitable measures to safeguard the applicant's rights, freedoms, and legitimate interests [GDPR, Article 22(3)]. At a minimum, this includes giving the applicant:
  * The right to obtain human intervention on the part of the controller [GDPR, Article 22(3)].
  * The right to express their point of view [GDPR, Article 22(3)].
  * The right to contest the decision [GDPR, Article 22(3)].
* **Data Protection Impact Assessment (DPIA):** Because automated evaluations of personal aspects leading to decisions that produce legal or significant effects constitute a high risk, the bank must conduct a DPIA prior to the processing, seeking advice from its Data Protection Officer (DPO) [GDPR, Article 35(1), (2), (3)].

---

### 2. AI Provider Design & Oversight Requirements

Under the AI Act, high-risk AI systems must be designed to enable effective human oversight by natural persons [AI Act, Article 14(1)]. The provider must build or identify oversight measures—commensurate with the system's risks, autonomy, and context—into the system before it is placed on the market or put into service [AI Act, Article 14(3)]. 

Specifically, the AI provider must design the system so that human overseers are enabled to:
* **Understand capacities and limitations:** Properly comprehend the relevant capabilities and limitations of the AI system, monitor its operation, and detect anomalies, dysfunctions, or unexpected performance [AI Act, Article 14(4)(a)].
* **Mitigate automation bias:** Remain aware of the tendency to automatically rely or over-rely on AI outputs [AI Act, Article 14(4)(b)].
* **Interpret outputs correctly:** Accurately interpret the AI system’s output using available interpretation tools and methods [AI Act, Article 14(4)(c)].
* **Override or disregard:** Decide in any given situation not to use the system, or to otherwise disregard, override, or reverse its output [AI Act, Article 14(4)(d)].
* **Intervene and halt:** Intervene in the system's operation or interrupt it via a "stop" button or similar safe-state procedure [AI Act, Article 14(4)(e)].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [GDPR, Article 22]  relevance 0.8655
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 22 — Automated individual decision-making, including profiling
1. The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her.
2. Paragraph 1 shall not apply if the decision: (a) is necessary for entering into, or performance of, a contract between the data subject and a data controller; (b) is authorised by Union or Member State law to which the controller is subject and which also lays down suitable measures to safeguard the data subject's rights and freedoms and legitimate interests; or (c) is based on the data subject's explicit consent.
3. In the cases referred to in points (a) and (c) of paragraph 2, the data controller shall implement suitable measures to safeguard the data subject's rights and freedoms and legitimate interests, at least the right to obtain human intervention on the part of the controller, to express his or her point of view and to contest the decision.
4. Decisions referred to in paragraph 2 shall not be based on special categories of personal data referred to in Article 9(1), unless point (a) or (g) of Article 9(2) applies and suitable measures to safeguard the data subject's rights and freedoms and legitimate interests are in place.

---

Result 2  cite as [AI Act, Article 14] (part 2 of 2)  relevance 0.7263
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 14 — Human oversight (part 2 of 2)
4. For the purpose of implementing paragraphs 1, 2 and 3, the high-risk AI system shall be provided to the deployer in such a way that natural persons to whom human oversight is assigned are enabled, as appropriate and proportionate: (a) to properly understand the relevant capacities and limitations of the high-risk AI system and be able to duly monitor its operation, including in view of detecting and addressing anomalies, dysfunctions and unexpected performance; (b) to remain aware of the possible tendency of automatically relying or over-relying on the output produced by a high-risk AI system (automation bias), in particular for high-risk AI systems used to provide information or recommendations for decisions to be taken by natural persons; (c) to correctly interpret the high-risk AI system’s output, taking into account, for example, the interpretation tools and methods available; (d) to decide, in any particular situation, not to use the high-risk AI system or to otherwise disregard, override or reverse the output of the high-risk AI system; (e) to intervene in the operation of the high-risk AI system or interrupt the system through a ‘stop’ button or a similar procedure that allows the system to come to a halt in a safe state.
5. For high-risk AI systems referred to in point 1(a) of Annex III, the measures referred to in paragraph 3 of this Article shall be such as to ensure that, in addition, no action or decision is taken by the deployer on the basis of the identification resulting from the system unless that identification has been separately verified and confirmed by at least two natural persons with the necessary competence, training and authority. The requirement for a separate verification by at least two natural persons shall not apply to high-risk AI systems used for the purposes of law enforcement, migration, border control or asylum, where Union or national law considers the application of this requirement to be disproportionate.

---

Result 3  cite as [AI Act, Article 14] (part 1 of 2)  relevance 0.7246
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 14 — Human oversight (part 1 of 2)
1. High-risk AI systems shall be designed and developed in such a way, including with appropriate human-machine interface tools, that they can be effectively overseen by natural persons during the period in which they are in use.
2. Human oversight shall aim to prevent or minimise the risks to health, safety or fundamental rights that may emerge when a high-risk AI system is used in accordance with its intended purpose or under conditions of reasonably foreseeable misuse, in particular where such risks persist despite the application of other requirements set out in this Section.
3. The oversight measures shall be commensurate with the risks, level of autonomy and context of use of the high-risk AI system, and shall be ensured through either one or both of the following types of measures: (a) measures identified and built, when technically feasible, into the high-risk AI system by the provider before it is placed on the market or put into service; (b) measures identified by the provider before placing the high-risk AI system on the market or putting it into service and that are appropriate to be implemented by the deployer.

---

Result 4  cite as [AI Act, Article 86]  relevance 0.7164
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 86 — Right to explanation of individual decision-making
1. Any affected person subject to a decision which is taken by the deployer on the basis of the output from a high-risk AI system listed in Annex III, with the exception of systems listed under point 2 thereof, and which produces legal effects or similarly significantly affects that person in a way that they consider to have an adverse impact on their health, safety or fundamental rights shall have the right to obtain from the deployer clear and meaningful explanations of the role of the AI system in the decision-making procedure and the main elements of the decision taken.
2. Paragraph 1 shall not apply to the use of AI systems for which exceptions from, or restrictions to, the obligation under that paragraph follow from Union or national law in compliance with Union law.
3. This Article shall apply only to the extent that the right referred to in paragraph 1 is not otherwise provided for under Union law.

---

Result 5  cite as [GDPR, Article 35] (part 1 of 3)  relevance 0.7132
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 35 — Data protection impact assessment (part 1 of 3)
1. Where a type of processing in particular using new technologies, and taking into account the nature, scope, context and purposes of the processing, is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall, prior to the processing, carry out an assessment of the impact of the envisaged processing operations on the protection of personal data. A single assessment may address a set of similar processing operations that present similar high risks.
2. The controller shall seek the advice of the data protection officer, where designated, when carrying out a data protection impact assessment.
3. A data protection impact assessment referred to in paragraph 1 shall in particular be required in the case of: (a) a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person; (b) processing on a large scale of special categories of data referred to in Article 9(1), or of personal data relating to criminal convictions and offences referred to in Article 10; or (c) a systematic monitoring of a publicly accessible area on a large scale.
4. The supe
```
</details>


---

## q22 (multi)

**Question:** We're adding optional advertising cookies that track identifiable visitors. Can we install them before opt-in, and must withdrawing consent be as easy as accepting?

**Reference:** No; non-essential device storage or access requires informed consent; withdrawal must be as easy as giving consent.

**Expected:** ePrivacy Directive;GDPR Article 5;Article 7

**Agent's answer:**

**1. Can you install optional advertising cookies before opt-in?**
No. Storing information or gaining access to information already stored in a user's terminal equipment (such as installing cookies) is only allowed on the condition that the subscriber or user has given their **prior** consent, after being provided with clear and comprehensive information about the purposes of the processing [ePrivacy Directive, Article 5(3)]. Because these are optional advertising cookies and not strictly necessary for the transmission of a communication or to provide a requested service, they cannot be placed before the user actively opts in.

**2. Must withdrawing consent be as easy as accepting?**
Yes. Data subjects must have the right to withdraw their consent at any time, and **it shall be as easy to withdraw as to give consent** [GDPR, Article 7(3)].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [GDPR, Article 7]  relevance 0.7729
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 7 — Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data.
2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding.
3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.
4. When assessing whether consent is freely given, utmost account shall be taken of whether, inter alia, the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

---

Result 2  cite as [ePrivacy Directive, Article 5]  relevance 0.7366
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 5 — Confidentiality of the communications
1. Member States shall ensure the confidentiality of communications and the related traffic data by means of a public communications network and publicly available electronic communications services, through national legislation. In particular, they shall prohibit listening, tapping, storage or other kinds of interception or surveillance of communications and the related traffic data by persons other than users, without the consent of the users concerned, except when legally authorised to do so in accordance with Article 15(1). This paragraph shall not prevent technical storage which is necessary for the conveyance of a communication without prejudice to the principle of confidentiality.
2. Paragraph 1 shall not affect any legally authorised recording of communications and the related traffic data when carried out in the course of lawful business practice for the purpose of providing evidence of a commercial transaction or of any other business communication.
3. Member States shall ensure that the storing of information, or the gaining of access to information already stored, in the terminal equipment of a subscriber or user is only allowed on condition that the subscriber or user concerned has given his or her consent, having been provided with clear and comprehensive information, in accordance with Directive 95/46/EC, inter alia, about the purposes of the processing. This shall not prevent any technical storage or access for the sole purpose of carrying out the transmission of a communication over an electronic communications network, or as strictly necessary in order for the provider of an information society service explicitly requested by the subscriber or user to provide the service.

---

Result 3  cite as [ePrivacy Directive, Article 6]  relevance 0.729
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 6 — Traffic data
1. Traffic data relating to subscribers and users processed and stored by the provider of a public communications network or publicly available electronic communications service must be erased or made anonymous when it is no longer needed for the purpose of the transmission of a communication without prejudice to paragraphs 2, 3 and 5 of this Article and Article 15(1).
2. Traffic data necessary for the purposes of subscriber billing and interconnection payments may be processed. Such processing is permissible only up to the end of the period during which the bill may lawfully be challenged or payment pursued.
3. For the purpose of marketing electronic communications services or for the provision of value added services, the provider of a publicly available electronic communications service may process the data referred to in paragraph 1 to the extent and for the duration necessary for such services or marketing, if the subscriber or user to whom the data relate has given his or her prior consent. Users or subscribers shall be given the possibility to withdraw their consent for the processing of traffic data at any time.
4. The service provider must inform the subscriber or user of the types of traffic data which are processed and of the duration of such processing for the purposes mentioned in paragraph 2 and, prior to obtaining consent, for the purposes mentioned in paragraph 3.
5. Processing of traffic data, in accordance with paragraphs 1, 2, 3 and 4, must be restricted to persons acting under the authority of providers of the public communications networks and publicly available electronic communications services handling billing or traffic management, customer enquiries, fraud detection, marketing electronic communications services or providing a value added service, and must be restricted to what is necessary for the purposes of such activities.
6. Paragraphs 1, 2, 3 and 5 shall apply without prejudice to the possibility for competent bodies to be informed of traffic data in conformity with applicable legislation with a view to settling disputes, in particular interconnection or billing disputes.

---

Result 4  cite as [ePrivacy Directive, Article 2]  relevance 0.7217
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 2 — Definitions
Save as otherwise provided, the definitions in Directive 95/46/EC and in Directive 2002/21/EC of the European Parliament and of the Council of 7 March 2002 on a common regulatory framework for electronic communications networks and services (Framework Directive) (8) shall apply.
The following definitions shall also apply:
(a) ‘user’ means any natural person using a publicly available electronic communications service, for private or business purposes, without necessarily having subscribed to this service;
(b) ‘traffic data’ means any data processed for the purpose of the conveyance of a communication on an electronic communications network or for the billing thereof;
(c) ‘location data’ means any data processed in an electronic communications network or by an electronic communications service, indicating the geographic position of the terminal equipment of a user of a publicly available electronic communications service;
(d) ‘communication’ means any information exchanged or conveyed between a finite number of parties by means of a publicly available electronic communications service. This does not include any information conveyed as part of a broadcasting service to the public over an electronic communications network except to the extent that the information can be related to the identifiable subscriber or user receiving the information;
(f) ‘consent’ by a user or subscriber corresponds to the data subject's consent in Directive 95/46/EC;
(g) ‘value added service’ means any service which requires the processing of traffic data or location data other than traffic data beyond what is necessary for the transmission of a communication or the billing thereof;
(h) ‘electronic mail’ means any text, voice, sound or image message sent over a public communications network which can be stored in the network or in the recipient's terminal equipmen
```
</details>


---

## q23 (multi)

**Question:** We email existing customers about our own similar products using contact details collected during a sale. What opt-out must we offer, and what happens if someone objects to direct marketing?

**Reference:** Offer a clear free easy opt-out at collection and in every message if not initially refused; stop processing personal data for direct marketing upon objection.

**Expected:** ePrivacy Directive;GDPR Article 13;Article 21

**Agent's answer:**

Based on the provided legislation, here are the requirements and consequences regarding opt-outs and objections for direct marketing to existing customers:

### Required Opt-Outs
When collecting electronic contact details in the context of the sale of a product or service, you are permitted to use those details to send direct marketing for your own similar products or services without prior consent, **provided that**:
* Customers are clearly and distinctly given the opportunity to object, free of charge and in an easy manner, to such use of their contact details **at the time of collection** [ePrivacy Directive, Article 13(2)].
* The same clear, free, and easy opportunity to object must also be provided **on the occasion of each subsequent marketing message** (if the customer did not initially refuse) [ePrivacy Directive, Article 13(2)].

Additionally, under the GDPR, the right to object to direct marketing must be explicitly brought to the attention of the data subject at the latest at the time of the first communication, presented clearly and separately from any other information [GDPR, Article 21(4)].

### What Happens If Someone Objects?
If a customer objects to direct marketing:
* **Immediate Cessation:** You must no longer process their personal data for direct marketing purposes [GDPR, Article 21(3)]. 
* **Scope:** The personal data shall no longer be processed for such marketing [GDPR, Article 21(3)].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [ePrivacy Directive, Article 13] (part 1 of 2)  relevance 0.7184
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 13 — Unsolicited communications (part 1 of 2)
1. The use of automated calling and communication systems without human intervention (automatic calling machines), facsimile machines (fax) or electronic mail for the purposes of direct marketing may be allowed only in respect of subscribers or users who have given their prior consent.
2. Notwithstanding paragraph 1, where a natural or legal person obtains from its customers their electronic contact details for electronic mail, in the context of the sale of a product or a service, in accordance with Directive 95/46/EC, the same natural or legal person may use these electronic contact details for direct marketing of its own similar products or services provided that customers clearly and distinctly are given the opportunity to object, free of charge and in an easy manner, to such use of electronic contact details at the time of their collection and on the occasion of each message in case the customer has not initially refused such use.
3. Member States shall take appropriate measures to ensure that unsolicited communications for the purposes of direct marketing, in cases other than those referred to in paragraphs 1 and 2, are not allowed either without the consent of the subscribers or users concerned or in respect of subscribers or users who do not wish to receive these communications, the choice between these options to be determined by national legislation, taking into account that both options must be free of charge for the subscriber or user.
4. In any event, the practice of sending electronic mail for the purposes of direct marketing which disguise or conceal the identity of the sender on whose behalf the communication is made, which contravene Article 6 of Directive 2000/31/EC, which do not have a valid address to which the recipient may send a request that such communications cease or which encourage recipients to visit websites that contravene that Article shall be prohibited.

---

Result 2  cite as [GDPR, Article 21]  relevance 0.6837
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 21 — Right to object
1. The data subject shall have the right to object, on grounds relating to his or her particular situation, at any time to processing of personal data concerning him or her which is based on point (e) or (f) of Article 6(1), including profiling based on those provisions. The controller shall no longer process the personal data unless the controller demonstrates compelling legitimate grounds for the processing which override the interests, rights and freedoms of the data subject or for the establishment, exercise or defence of legal claims.
2. Where personal data are processed for direct marketing purposes, the data subject shall have the right to object at any time to processing of personal data concerning him or her for such marketing, which includes profiling to the extent that it is related to such direct marketing.
3. Where the data subject objects to processing for direct marketing purposes, the personal data shall no longer be processed for such purposes.
4. At the latest at the time of the first communication with the data subject, the right referred to in paragraphs 1 and 2 shall be explicitly brought to the attention of the data subject and shall be presented clearly and separately from any other information.
5. In the context of the use of information society services, and notwithstanding Directive 2002/58/EC, the data subject may exercise his or her right to object by automated means using technical specifications.
6. Where personal data are processed for scientific or historical research purposes or statistical purposes pursuant to Article 89(1), the data subject, on grounds relating to his or her particular situation, shall have the right to object to processing of personal data concerning him or her, unless the processing is necessary for the performance of a task carried out for reasons of public interest.

---

Result 3  cite as [ePrivacy Directive, Article 13] (part 2 of 2)  relevance 0.6605
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 13 — Unsolicited communications (part 2 of 2)
5. Paragraphs 1 and 3 shall apply to subscribers who are natural persons. Member States shall also ensure, in the framework of Community law and applicable national legislation, that the legitimate interests of subscribers other than natural persons with regard to unsolicited communications are sufficiently protected.
6. Without prejudice to any administrative remedy for which provision may be made, inter alia, under Article 15a(2), Member States shall ensure that any natural or legal person adversely affected by infringements of national provisions adopted pursuant to this Article and therefore having a legitimate interest in the cessation or prohibition of such infringements, including an electronic communications service provider protecting its legitimate business interests, may bring legal proceedings in respect of such infringements. Member States may also lay down specific rules on penalties applicable to providers of electronic communications services which by their negligence contribute to infringements of national provisions adopted pursuant to this Article.

---

Result 4  cite as [ePrivacy Directive, Article 2]  relevance 0.6585
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 2 — Definitions
Save as otherwise provided, the definitions in Directive 95/46/EC and in Directive 2002/21/EC of the European Parliament and of the Council of 7 March 2002 on a common regulatory framework for electronic communications networks and services (Framework Directive) (8) shall apply.
The following definitions shall also apply:
(a) ‘user’ means any natural person using a publicly available electronic communications service, for private or business purposes, without necessarily having subscribed to this service;
(b) ‘traffic data’ means any data processed for the purpose of the conveyance of a communication on an electronic communications network or for the billing thereof;
(c) ‘location data’ means any data processed in an electronic communications network or by an electronic communications service, indicating the geographic position of the terminal equipment of a user of a publicly available electronic communications service;
(d) ‘communication’ means any information exchanged or conveyed between a finite number of parties by means of a publicly available electronic communications service. This does not include any information conveyed as part of a broadcasting service to the public over an electronic communications network except to the extent that the information can be related to the identifiable subscriber or user receiving the information;
(f) ‘consent’ by a user or subscriber corresponds to the data subject's consent in Directive 95/46/EC;
(g) ‘value added service’ means any service which requires the processing of traffic data or location data other than traffic data beyond what is necessary for the transmission of a communication or the billing thereof;
(h) ‘electronic mail’ means any text, voice, sound or image message sent over a public communications network which can be stored in the network or in the recipient's terminal equipment until it is collected by the recipient;
(i) ‘personal data breach’ means a breach of security leading to the accidental or unlawful de
```
</details>


---

## q24 (multi)

**Question:** We're launching a chatbot that collects customers' names and emails directly. What must we tell them about the AI interaction and about our use of their personal data?

**Reference:** Disclose AI interaction unless obvious; at collection provide applicable privacy information including controller identity, purposes, legal basis, recipients, retention and rights.

**Expected:** AI Act;GDPR Article 50;Article 13

**Agent's answer:**

When launching a chatbot that collects customers' names and emails directly, you must comply with transparency requirements under both EU AI transparency rules and the GDPR. 

### 1. Information about the AI Interaction
Unless it is already obvious to a reasonably well-informed, observant, and circumspect user from the context that they are interacting with an AI, you must inform the users that they are interacting with an AI system [AI Act, Article 50]. This disclosure should be made clear and transparently before or at the start of the interaction.

### 2. Information about the Use of Personal Data (GDPR)
Because you are collecting personal data (names and emails) directly from the data subjects, you must provide them with the following information at the time the data are obtained [GDPR, Article 13]:

* **Identity and Contact Details:** Your organization's identity and contact details, and where applicable, those of your representative or Data Protection Officer (DPO) [GDPR, Article 13(1)(a)-(b)].
* **Purposes and Legal Basis:** The specific purposes for which you are processing their names and emails (e.g., customer support, communication) and the legal basis for the processing [GDPR, Article 13(1)(c)].
* **Legitimate Interests:** If your processing is based on legitimate interests, specify those interests [GDPR, Article 13(1)(d)].
* **Recipients:** The recipients or categories of recipients of the personal data, if any [GDPR, Article 13(1)(e)].
* **International Transfers:** If applicable, whether you intend to transfer the data to a third country or international organization, and the safeguards in place [GDPR, Article 13(1)(f)].
* **Storage Period:** The period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period [GDPR, Article 13(2)(a)].
* **Data Subject Rights:** Inform users of their rights, including the right to request access to, rectification, or erasure of their personal data, restriction of processing, objection to processing, and the right to data portability [GDPR, Article 13(2)(b)].
* **Right to Withdraw Consent:** If processing relies on consent, inform them of their right to withdraw consent at any time without affecting prior lawfulness [GDPR, Article 13(2)(c)].
* **Right to Lodge a Complaint:** Their right to lodge a complaint with a supervisory authority [GDPR, Article 13(2)(d)].
* **Statutory/Contractual Requirements:** Whether the provision of personal data is a statutory or contractual requirement, or a requirement necessary to enter into a contract, and whether the data subject is obliged to provide the personal data and the possible consequences of failure to provide such data [GDPR, Article 13(2)(e)].
* **Automated Decision-Making:** The existence of automated decision-making (including profiling) if used, along with meaningful information about the logic involved and the significance and envisaged consequences for the user [GDPR, Article 13(2)(f)].

### Presentation
All information must be provided in a concise, transparent, intelligible, and easily accessible form, using clear and plain language [GDPR, Article 12(1)].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [GDPR, Article 12] (part 1 of 2)  relevance 0.6748
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 12 — Transparent information, communication and modalities for the exercise of the rights of the data subject (part 1 of 2)
1. The controller shall take appropriate measures to provide any information referred to in Articles 13 and 14 and any communication under Articles 15 to 22 and 34 relating to processing to the data subject in a concise, transparent, intelligible and easily accessible form, using clear and plain language, in particular for any information addressed specifically to a child. The information shall be provided in writing, or by other means, including, where appropriate, by electronic means. When requested by the data subject, the information may be provided orally, provided that the identity of the data subject is proven by other means.
2. The controller shall facilitate the exercise of data subject rights under Articles 15 to 22. In the cases referred to in Article 11(2), the controller shall not refuse to act on the request of the data subject for exercising his or her rights under Articles 15 to 22, unless the controller demonstrates that it is not in a position to identify the data subject.
3. The controller shall provide information on action taken on a request under Articles 15 to 22 to the data subject without undue delay and in any event within one month of receipt of the request. That period may be extended by two further months where necessary, taking into account the complexity and number of the requests. The controller shall inform the data subject of any such extension within one month of receipt of the request, together with the reasons for the delay. Where the data subject makes the request by electronic form means, the information shall be provided by electronic means where possible, unless otherwise requested by the data subject.
4. If the controller does not take action on the request of the data subject, the controller shall inform the data subject without delay and at the latest within one month of receipt of the request of the reasons for not taking action and on the possibility of lodging a complaint with a supervisory authority and seeking a judicial remedy.

---

Result 2  cite as [AI Act, Article 50] (part 1 of 3)  relevance 0.6675
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 50 — Transparency obligations for providers and deployers of certain AI systems (part 1 of 3)
1. Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system, unless this is obvious from the point of view of a natural person who is reasonably well-informed, observant and circumspect, taking into account the circumstances and the context of use. This obligation shall not apply to AI systems authorised by law to detect, prevent, investigate or prosecute criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, unless those systems are available for the public to report a criminal offence.
2. Providers of AI systems, including general-purpose AI systems, generating synthetic audio, image, video or text content, shall ensure that the outputs of the AI system are marked in a machine-readable format and detectable as artificially generated or manipulated. Providers shall ensure their technical solutions are effective, interoperable, robust and reliable as far as this is technically feasible, taking into account the specificities and limitations of various types of content, the costs of implementation and the generally acknowledged state of the art, as may be reflected in relevant technical standards. This obligation shall not apply to the extent the AI systems perform an assistive function for standard editing or do not substantially alter the input data provided by the deployer or the semantics thereof, or where authorised by law to detect, prevent, investigate or prosecute criminal offences.
3. Deployers of an emotion recognition system or a biometric categorisation system shall inform the natural persons exposed thereto of the operation of the system, and shall process the personal data in accordance with Regulations (EU) 2016/679 and (EU) 2018/1725 and Directive (EU) 2016/680, as applicable. This obligation shall not apply to AI systems used for biometric categorisation and emotion recognition, which are permitted by law to detect, prevent or investigate criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties, and in accordance with Union law.

---

Result 3  cite as [AI Act, Article 13] (part 1 of 2)  relevance 0.6599
Source: Regulation (EU) 2024/1689 (Artificial Intelligence Act) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
AI Act, Article 13 — Transparency and provision of information to deployers (part 1 of 2)
1. High-risk AI systems shall be designed and developed in such a way as to ensure that their operation is sufficiently transparent to enable deployers to interpret a system’s output and use it appropriately. An appropriate type and degree of transparency shall be ensured with a view to achieving compliance with the relevant obligations of the provider and deployer set out in Section 3.
2. High-risk AI systems shall be accompanied by instructions for use in an appropriate digital format or otherwise that include concise, complete, correct and clear information that is relevant, accessible and comprehensible to deployers.
3. The instructions for use shall contain at least the following information:
(a) the identity and the contact details of the provider and, where applicable, of its authorised representative;
(b) the characteristics, capabilities and limitations of performance of the high-risk AI system, including: (i) its intended purpose; (ii) the level of accuracy, including its metrics, robustness and cybersecurity referred to in Article 15 against which the high-risk AI system has been tested and validated and which can be expected, and any known and foreseeable circumstances that may have an impact on that expected level of accuracy, robustness and cybersecurity; (iii) any known or foreseeable circumstance, related to the use of the high-risk AI system in accordance with its intended purpose or under conditions of reasonably foreseeable misuse, which may lead to risks to the health and safety or fundamental rights referred to in Article 9(2); (iv) where applicable, the technical capabilities and characteristics of the high-risk AI system to provide information that is relevant to explain its output; (v) when appropriate, its performance regarding specific persons or groups of persons on which the system is intended to be used; (vi) when appropriate, specifications for the input data, or any other relevant information in terms of the training, validation and testing data sets used, taking into account the intended purpose of the high-risk AI system; (vii) where applicable, information to enable deployers to interpret the output of the high-risk AI system and use it appropriately;

---

Result 4  cite as [GDPR, Article 13] (part 1 of 2)  relevance 0.6592
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 13 — Information to be provided where personal data are collected from the data subject (part 1 of 2)
1. Where personal data relating to a data subject are collected from the data subject, the controller shall, at the time when personal data are obtained, provide the data subject with all of the following information: (a) the ident
```
</details>


---

## q25 (unanswerable)

**Question:** We're budgeting for a compliance officer in Paris. What exact monthly salary must we pay them?

**Reference:** The corpus does not cover this question.

**Expected:**  

**Agent's answer:**

The corpus does not cover this question.

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [GDPR, Article 38]  relevance 0.6778
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 38 — Position of the data protection officer
1. The controller and the processor shall ensure that the data protection officer is involved, properly and in a timely manner, in all issues which relate to the protection of personal data.
2. The controller and processor shall support the data protection officer in performing the tasks referred to in Article 39 by providing resources necessary to carry out those tasks and access to personal data and processing operations, and to maintain his or her expert knowledge.
3. The controller and processor shall ensure that the data protection officer does not receive any instructions regarding the exercise of those tasks. He or she shall not be dismissed or penalised by the controller or the processor for performing his tasks. The data protection officer shall directly report to the highest management level of the controller or the processor.
4. Data subjects may contact the data protection officer with regard to all issues related to processing of their personal data and to the exercise of their rights under this Regulation.
5. The data protection officer shall be bound by secrecy or confidentiality concerning the performance of his or her tasks, in accordance with Union or Member State law.
6. The data protection officer may fulfil other tasks and duties. The controller or processor shall ensure that any such tasks and duties do not result in a conflict of interests.

---

Result 2  cite as [GDPR, Article 37]  relevance 0.6594
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 37 — Designation of the data protection officer
1. The controller and the processor shall designate a data protection officer in any case where: (a) the processing is carried out by a public authority or body, except for courts acting in their judicial capacity; (b) the core activities of the controller or the processor consist of processing operations which, by virtue of their nature, their scope and/or their purposes, require regular and systematic monitoring of data subjects on a large scale; or (c) the core activities of the controller or the processor consist of processing on a large scale of special categories of data pursuant to Article 9 and personal data relating to criminal convictions and offences referred to in Article 10.
2. A group of undertakings may appoint a single data protection officer provided that a data protection officer is easily accessible from each establishment.
3. Where the controller or the processor is a public authority or body, a single data protection officer may be designated for several such authorities or bodies, taking account of their organisational structure and size.
4. In cases other than those referred to in paragraph 1, the controller or processor or associations and other bodies representing categories of controllers or processors may or, where required by Union or Member State law shall, designate a data protection officer. The data protection officer may act for such associations and other bodies representing controllers or processors.
5. The data protection officer shall be designated on the basis of professional qualities and, in particular, expert knowledge of data protection law and practices and the ability to fulfil the tasks referred to in Article 39.
6. The data protection officer may be a staff member of the controller or processor, or fulfil the tasks on the basis of a service contract.
7. The controller or the processor shall publish the contact details of the data protection officer and communicate them to the supervisory authority.

---

Result 3  cite as [GDPR, Article 52]  relevance 0.6574
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 52 — Independence
1. Each supervisory authority shall act with complete independence in performing its tasks and exercising its powers in accordance with this Regulation.
2. The member or members of each supervisory authority shall, in the performance of their tasks and exercise of their powers in accordance with this Regulation, remain free from external influence, whether direct or indirect, and shall neither seek nor take instructions from anybody.
3. Member or members of each supervisory authority shall refrain from any action incompatible with their duties and shall not, during their term of office, engage in any incompatible occupation, whether gainful or not.
4. Each Member State shall ensure that each supervisory authority is provided with the human, technical and financial resources, premises and infrastructure necessary for the effective performance of its tasks and exercise of its powers, including those to be carried out in the context of mutual assistance, cooperation and participation in the Board.
5. Each Member State shall ensure that each supervisory authority chooses and has its own staff which shall be subject to the exclusive direction of the member or members of the supervisory authority concerned.
6. Each Member State shall ensure that each supervisory authority is subject to financial control which does not affect its independence and that it has separate, public annual budgets, which may be part of the overall state or national budget.

---

Result 4  cite as [GDPR, Article 39]  relevance 0.6515
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 39 — Tasks of the data protection officer
1. The data protection officer shall have at least the following tasks: (a) to inform and advise the controller or the processor and the employees who carry out processing of their obligations pursuant to this Regulation and to other Union or Member State data protection provisions; (b) to monitor compliance with this Regulation, with other Union or Member State data protection provisions and with the policies of the controller or processor in relation to the protection of personal data, including the assignment of responsibilities, awareness-raising and training of staff involved in processing operations, and the related audits; (c) to provide advice where requested as regards the data protection impact assessment and monitor its performance pursuant to Article 35; (d) to cooperate with the supervisory authority; (e) to act as the contact point for the supervisory authority on issues relating to processing, including the prior consultation referred to in Article 36, and to consult, where appropriate, with regard to any other matter.
2. The data protection officer shall in the performance of his or her tasks have due regard to the risk associated with processing operations, taking into account the nature, scope, context and purposes of processing.

---

Result 5  cite as [GDPR, Article 68]  relevance 0.65
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 68 — European Data Protection Board
1. The European Data Protection Board (the ‘Board’) is hereby established as a body of the Union and shall have legal personality.
2. The Board shall be represented by its Chair.
3. The Board shall be composed of the head of one supervisory authority of each Member State and of the European Data Protection Supervisor, or their respective representatives.
4. Where in a Member State more than one supervisory authority is responsible for monitoring the application of the provisions pursuant to this Regulation, a joint representative shall be appointed in accordance with that Member State's law.
5. The Commission shall have the right to 
```
</details>


---

## q26 (unanswerable)

**Question:** We're building an AI chatbot. Which commercial language model has the lowest hallucination rate on our own customer tickets?

**Reference:** The corpus does not cover this question.

**Expected:**  

**Agent's answer:**

The corpus does not cover this question.

<details><summary>Retrieved passages</summary>

```
(the agent did not search)
```
</details>


---

## q27 (unanswerable)

**Question:** We're choosing a cloud provider. Which vendor charges the lowest price for storing one terabyte of encrypted customer data?

**Reference:** The corpus does not cover this question.

**Expected:**  

**Agent's answer:**

The corpus does not cover this question.

<details><summary>Retrieved passages</summary>

```
(the agent did not search)
```
</details>


---

## q28 (unanswerable)

**Question:** We're preparing a privacy audit. What exact fee will our chosen external auditor charge?

**Reference:** The corpus does not cover this question.

**Expected:**  

**Agent's answer:**

The corpus does not cover this question.

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [GDPR, Article 58] (part 1 of 3)  relevance 0.7102
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 58 — Powers (part 1 of 3)
1. Each supervisory authority shall have all of the following investigative powers: (a) to order the controller and the processor, and, where applicable, the controller's or the processor's representative to provide any information it requires for the performance of its tasks; (b) to carry out investigations in the form of data protection audits; (c) to carry out a review on certifications issued pursuant to Article 42(7); (d) to notify the controller or the processor of an alleged infringement of this Regulation; (e) to obtain, from the controller and the processor, access to all personal data and to all information necessary for the performance of its tasks; (f) to obtain access to any premises of the controller and the processor, including to any data processing equipment and means, in accordance with Union or Member State procedural law.

---

Result 2  cite as [GDPR, Article 57] (part 2 of 2)  relevance 0.6766
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 57 — Tasks (part 2 of 2)
(m) encourage the drawing up of codes of conduct pursuant to Article 40(1) and provide an opinion and approve such codes of conduct which provide sufficient safeguards, pursuant to Article 40(5);
(n) encourage the establishment of data protection certification mechanisms and of data protection seals and marks pursuant to Article 42(1), and approve the criteria of certification pursuant to Article 42(5);
(o) where applicable, carry out a periodic review of certifications issued in accordance with Article 42(7);
(p) draft and publish the criteria for accreditation of a body for monitoring codes of conduct pursuant to Article 41 and of a certification body pursuant to Article 43;
(q) conduct the accreditation of a body for monitoring codes of conduct pursuant to Article 41 and of a certification body pursuant to Article 43;
(r) authorise contractual clauses and provisions referred to in Article 46(3);
(s) approve binding corporate rules pursuant to Article 47;
(t) contribute to the activities of the Board;
(u) keep internal records of infringements of this Regulation and of measures taken in accordance with Article 58(2); and
(v) fulfil any other tasks related to the protection of personal data.
2. Each supervisory authority shall facilitate the submission of complaints referred to in point (f) of paragraph 1 by measures such as a complaint submission form which can also be completed electronically, without excluding other means of communication.
3. The performance of the tasks of each supervisory authority shall be free of charge for the data subject and, where applicable, for the data protection officer.
4. Where requests are manifestly unfounded or excessive, in particular because of their repetitive character, the supervisory authority may charge a reasonable fee based on administrative costs, or refuse to act on the request. The supervisory authority shall bear the burden of demonstrating the manifestly unfounded or excessive character of the request.

---

Result 3  cite as [GDPR, Article 52]  relevance 0.6747
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 52 — Independence
1. Each supervisory authority shall act with complete independence in performing its tasks and exercising its powers in accordance with this Regulation.
2. The member or members of each supervisory authority shall, in the performance of their tasks and exercise of their powers in accordance with this Regulation, remain free from external influence, whether direct or indirect, and shall neither seek nor take instructions from anybody.
3. Member or members of each supervisory authority shall refrain from any action incompatible with their duties and shall not, during their term of office, engage in any incompatible occupation, whether gainful or not.
4. Each Member State shall ensure that each supervisory authority is provided with the human, technical and financial resources, premises and infrastructure necessary for the effective performance of its tasks and exercise of its powers, including those to be carried out in the context of mutual assistance, cooperation and participation in the Board.
5. Each Member State shall ensure that each supervisory authority chooses and has its own staff which shall be subject to the exclusive direction of the member or members of the supervisory authority concerned.
6. Each Member State shall ensure that each supervisory authority is subject to financial control which does not affect its independence and that it has separate, public annual budgets, which may be part of the overall state or national budget.

---

Result 4  cite as [GDPR, Article 28] (part 2 of 3)  relevance 0.6662
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 28 — Processor (part 2 of 3)
(e) taking into account the nature of the processing, assists the controller by appropriate technical and organisational measures, insofar as this is possible, for the fulfilment of the controller's obligation to respond to requests for exercising the data subject's rights laid down in Chapter III;
(f) assists the controller in ensuring compliance with the obligations pursuant to Articles 32 to 36 taking into account the nature of processing and the information available to the processor;
(g) at the choice of the controller, deletes or returns all the personal data to the controller after the end of the provision of services relating to processing, and deletes existing copies unless Union or Member State law requires storage of the personal data;
(h) makes available to the controller all information necessary to demonstrate compliance with the obligations laid down in this Article and allow for and contribute to audits, including inspections, conducted by the controller or another auditor mandated by the controller.
With regard to point (h) of the first subparagraph, the processor shall immediately inform the controller if, in its opinion, an instruction infringes this Regulation or other Union or Member State data protection provisions.
4. Where a processor engages another processor for carrying out specific processing activities on behalf of the controller, the same data protection obligations as set out in the contract or other legal act between the controller and the processor as referred to in paragraph 3 shall be imposed on that other processor by way of a contract or other legal act under Union or Member State law, in particular providing sufficient guarantees to implement appropriate technical and organisational measures in such a manner that the processing will meet the requirements of this Regulation. Where that other processor fails to fulfil its data protection obligations, the initial processor shall remain fully liable to the controller for the performance of that other processor's obligations.

---

Result 5  cite as [ePrivacy Directive, Article 7]  relevance 0.6643
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 7 — Itemised billing
1. Subscribers shall have the right to receive non-itemised bills.
2. Member States shall apply national provisions in order to reconcile the rights of subscribers receiving itemised bills with the right to privacy of calling users and called subscribers, for example by ensuring that sufficient alternative privacy enhancing methods of communications or payments are avai
```
</details>


---

## q29 (unanswerable)

**Question:** We're launching a cookie banner in France. What exact approval code will the French regulator assign to our particular banner?

**Reference:** The corpus does not cover this question.

**Expected:**  

**Agent's answer:**

The corpus does not cover this question.

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [ePrivacy Directive, Article 5]  relevance 0.6573
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 5 — Confidentiality of the communications
1. Member States shall ensure the confidentiality of communications and the related traffic data by means of a public communications network and publicly available electronic communications services, through national legislation. In particular, they shall prohibit listening, tapping, storage or other kinds of interception or surveillance of communications and the related traffic data by persons other than users, without the consent of the users concerned, except when legally authorised to do so in accordance with Article 15(1). This paragraph shall not prevent technical storage which is necessary for the conveyance of a communication without prejudice to the principle of confidentiality.
2. Paragraph 1 shall not affect any legally authorised recording of communications and the related traffic data when carried out in the course of lawful business practice for the purpose of providing evidence of a commercial transaction or of any other business communication.
3. Member States shall ensure that the storing of information, or the gaining of access to information already stored, in the terminal equipment of a subscriber or user is only allowed on condition that the subscriber or user concerned has given his or her consent, having been provided with clear and comprehensive information, in accordance with Directive 95/46/EC, inter alia, about the purposes of the processing. This shall not prevent any technical storage or access for the sole purpose of carrying out the transmission of a communication over an electronic communications network, or as strictly necessary in order for the provider of an information society service explicitly requested by the subscriber or user to provide the service.

---

Result 2  cite as [GDPR, Article 40] (part 2 of 3)  relevance 0.6514
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 40 — Codes of conduct (part 2 of 3)
3. In addition to adherence by controllers or processors subject to this Regulation, codes of conduct approved pursuant to paragraph 5 of this Article and having general validity pursuant to paragraph 9 of this Article may also be adhered to by controllers or processors that are not subject to this Regulation pursuant to Article 3 in order to provide appropriate safeguards within the framework of personal data transfers to third countries or international organisations under the terms referred to in point (e) of Article 46(2). Such controllers or processors shall make binding and enforceable commitments, via contractual or other legally binding instruments, to apply those appropriate safeguards including with regard to the rights of data subjects.
4. A code of conduct referred to in paragraph 2 of this Article shall contain mechanisms which enable the body referred to in Article 41(1) to carry out the mandatory monitoring of compliance with its provisions by the controllers or processors which undertake to apply it, without prejudice to the tasks and powers of supervisory authorities competent pursuant to Article 55 or 56.
5. Associations and other bodies referred to in paragraph 2 of this Article which intend to prepare a code of conduct or to amend or extend an existing code shall submit the draft code, amendment or extension to the supervisory authority which is competent pursuant to Article 55. The supervisory authority shall provide an opinion on whether the draft code, amendment or extension complies with this Regulation and shall approve that draft code, amendment or extension if it finds that it provides sufficient appropriate safeguards.
6. Where the draft code, or amendment or extension is approved in accordance with paragraph 5, and where the code of conduct concerned does not relate to processing activities in several Member States, the supervisory authority shall register and publish the code.

---

Result 3  cite as [ePrivacy Directive, Article 15a]  relevance 0.6493
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 15a — Implementation and enforcement
1. Member States shall lay down the rules on penalties, including criminal sanctions where appropriate, applicable to infringements of the national provisions adopted pursuant to this Directive and shall take all measures necessary to ensure that they are implemented. The penalties provided for must be effective, proportionate and dissuasive and may be applied to cover the period of any breach, even where the breach has subsequently been rectified. The Member States shall notify those provisions to the Commission by 25 May 2011, and shall notify it without delay of any subsequent amendment affecting them.
2. Without prejudice to any judicial remedy which might be available, Member States shall ensure that the competent national authority and, where relevant, other national bodies have the power to order the cessation of the infringements referred to in paragraph 1.
3. Member States shall ensure that the competent national authority and, where relevant, other national bodies have the necessary investigative powers and resources, including the power to obtain any relevant information they might need to monitor and enforce national provisions adopted pursuant to this Directive.
4. The relevant national regulatory authorities may adopt measures to ensure effective cross-border cooperation in the enforcement of the national laws adopted pursuant to this Directive and to create harmonised conditions for the provision of services involving cross-border data flows. The national regulatory authorities shall provide the Commission, in good time before adopting any such measures, with a summary of the grounds for action, the envisaged measures and the proposed course of action. The Commission may, having examined such information and consulted ENISA and the Working Party on the Protection of Individuals with regard to the Processing of Personal Data established by Article 29 of Directive 95/46/EC, make comments or recommendations thereupon, in particular to ensure that the envisaged measures do not adversely affect the functioning of the internal market. National regulatory authorities shall take the utmost account of the Commission's comments or recommendations when deciding on the measures.

---

Result 4  cite as [GDPR, Article 40] (part 3 of 3)  relevance 0.6473
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 40 — Codes of conduct (part 3 of 3)
7. Where a draft code of conduct relates to processing activities in several Member States, the supervisory authority which is competent pursuant to Article 55 shall, before approving the draft code, amendment or extension, submit it in the procedure referred to in Article 63 to the Board which shall provide an opinion on whether the draft code, amendment or extension complies with this Regulation or, in the situation referred to in paragraph 3 of this Article, provides appropriate safeguards.
8. Where the opinion referred to in paragraph 7 confirms that the draft code, amendment or extension complies with this Regulation, or, in the situation referred to in paragraph 3, provides appropriate safeguards, the Board shall submit its opinion to the Commission.
9. The Commission may, by way of implementing acts, decide that the approved code of conduct, amendment or extension submitted to it pursuant to paragraph 8 of this Article have general validity within the Union. Those implementing 
```
</details>


---

## q30 (unanswerable)

**Question:** We're training our staff on AI. Which commercial training course has the highest customer satisfaction rating this month?

**Reference:** The corpus does not cover this question.

**Expected:**  

**Agent's answer:**

The corpus does not cover this question.

<details><summary>Retrieved passages</summary>

```
(the agent did not search)
```
</details>


---

## q31 (unanswerable)

**Question:** We're launching a cookie banner in France. Does the French regulator require refusing cookies to be as easy as accepting them?

**Reference:** The corpus does not cover this question.

**Expected:**  

**Agent's answer:**

The corpus does not cover this question.

<details><summary>Retrieved passages</summary>

```
Result 1  cite as [ePrivacy Directive, Article 5]  relevance 0.6855
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 5 — Confidentiality of the communications
1. Member States shall ensure the confidentiality of communications and the related traffic data by means of a public communications network and publicly available electronic communications services, through national legislation. In particular, they shall prohibit listening, tapping, storage or other kinds of interception or surveillance of communications and the related traffic data by persons other than users, without the consent of the users concerned, except when legally authorised to do so in accordance with Article 15(1). This paragraph shall not prevent technical storage which is necessary for the conveyance of a communication without prejudice to the principle of confidentiality.
2. Paragraph 1 shall not affect any legally authorised recording of communications and the related traffic data when carried out in the course of lawful business practice for the purpose of providing evidence of a commercial transaction or of any other business communication.
3. Member States shall ensure that the storing of information, or the gaining of access to information already stored, in the terminal equipment of a subscriber or user is only allowed on condition that the subscriber or user concerned has given his or her consent, having been provided with clear and comprehensive information, in accordance with Directive 95/46/EC, inter alia, about the purposes of the processing. This shall not prevent any technical storage or access for the sole purpose of carrying out the transmission of a communication over an electronic communications network, or as strictly necessary in order for the provider of an information society service explicitly requested by the subscriber or user to provide the service.

---

Result 2  cite as [GDPR, Article 7]  relevance 0.6833
Source: Regulation (EU) 2016/679 (General Data Protection Regulation) — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
GDPR, Article 7 — Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data.
2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. Any part of such a declaration which constitutes an infringement of this Regulation shall not be binding.
3. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.
4. When assessing whether consent is freely given, utmost account shall be taken of whether, inter alia, the performance of a contract, including the provision of a service, is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.

---

Result 3  cite as [ePrivacy Directive, Article 14]  relevance 0.6829
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 14 — Technical features and standardisation
1. In implementing the provisions of this Directive, Member States shall ensure, subject to paragraphs 2 and 3, that no mandatory requirements for specific technical features are imposed on terminal or other electronic communication equipment which could impede the placing of equipment on the market and the free circulation of such equipment in and between Member States.
2. Where provisions of this Directive can be implemented only by requiring specific technical features in electronic communications networks, Member States shall inform the Commission in accordance with the procedure provided for by Directive 98/34/EC of the European Parliament and of the Council of 22 June 1998 laying down a procedure for the provision of information in the field of technical standards and regulations and of rules on information society services (9).
3. Where required, measures may be adopted to ensure that terminal equipment is constructed in a way that is compatible with the right of users to protect and control the use of their personal data, in accordance with Directive 1999/5/EC and Council Decision 87/95/EEC of 22 December 1986 on standardisation in the field of information technology and communications (10).

---

Result 4  cite as [ePrivacy Directive, Article 15a]  relevance 0.6809
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 15a — Implementation and enforcement
1. Member States shall lay down the rules on penalties, including criminal sanctions where appropriate, applicable to infringements of the national provisions adopted pursuant to this Directive and shall take all measures necessary to ensure that they are implemented. The penalties provided for must be effective, proportionate and dissuasive and may be applied to cover the period of any breach, even where the breach has subsequently been rectified. The Member States shall notify those provisions to the Commission by 25 May 2011, and shall notify it without delay of any subsequent amendment affecting them.
2. Without prejudice to any judicial remedy which might be available, Member States shall ensure that the competent national authority and, where relevant, other national bodies have the power to order the cessation of the infringements referred to in paragraph 1.
3. Member States shall ensure that the competent national authority and, where relevant, other national bodies have the necessary investigative powers and resources, including the power to obtain any relevant information they might need to monitor and enforce national provisions adopted pursuant to this Directive.
4. The relevant national regulatory authorities may adopt measures to ensure effective cross-border cooperation in the enforcement of the national laws adopted pursuant to this Directive and to create harmonised conditions for the provision of services involving cross-border data flows. The national regulatory authorities shall provide the Commission, in good time before adopting any such measures, with a summary of the grounds for action, the envisaged measures and the proposed course of action. The Commission may, having examined such information and consulted ENISA and the Working Party on the Protection of Individuals with regard to the Processing of Personal Data established by Article 29 of Directive 95/46/EC, make comments or recommendations thereupon, in particular to ensure that the envisaged measures do not adversely affect the functioning of the internal market. National regulatory authorities shall take the utmost account of the Commission's comments or recommendations when deciding on the measures.

---

Result 5  cite as [ePrivacy Directive, Article 1]  relevance 0.6662
Source: Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219
ePrivacy Directive, Article 1 — Scope and aim
1. This Directive provides for the harmonisation of the national provisions required to ensure an equivalent level of protection of fundamental rights and freedoms, and in particular the right to privacy and confidentiality, with respect to t
```
</details>
