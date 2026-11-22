# Grade these answers yourself

Fill `eval/human_labels.csv` (columns id, correct, supported, notes) for at least 20 of them,
**before** looking at `eval/judge_verdicts.json`.
- `correct` = 1 if the answer matches the reference answer (or is a proper refusal for an unanswerable question), else 0.
- `supported` = 1 if every claim is in the retrieved passages, else 0. Explain every 0 in `notes`.

## q01 (single)
**Question:** How much time does a company have to answer a person who asks to see or delete their data?
**Reference answer:** Without undue delay and at most one month from receiving the request. It can be extended by two more months if requests are complex or numerous, but the person must be told about the extension, with reasons, within the first month.
**Agent answer:** A controller must provide information on action taken regarding a data subject request (such as for access or deletion) without undue delay and in any event within one month of receiving the request `[gdpr, Article 12(3)]`. This period may be extended by two further months where necessary, taking into account the complexity and number of requests, provided the controller informs the data subject of the extension and reasons for the delay within one month of receipt `[gdpr, Article 12(3)]`.
**Searches:** ['time limit response data subject request access deletion']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 12(3)-(4) | distance: 0.237
3. The controller shall provide information on action taken on a request under Articles 15 to 22 to the data subject without undue delay and in any event within one month of receipt of 
- 2] source: gdpr | location: Article 15(1) | distance: 0.296
Right of access by the data subject. 1. The data subject shall have the right to obtain from the controller confirmation as to whether or not personal data concerning him or her are being pr
- 3] source: edpb_controller_processor | location: paras 132-133 (p.38) | distance: 0.301
132. It is crucial to bear in mind that, although the practical management of individual requests can be outsourced to the processor, the controller bears the res
- 4] source: gdpr | location: Article 13(2) | distance: 0.303
2. In addition to the information referred to in paragraph 1, the controller shall, at the time when personal data are obtained, provide the data subject with the following further informati
- 5] source: gdpr | location: Article 17(1) | distance: 0.306
Right to erasure (‘right to be forgotten’). 1. The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay and 

## q02 (single)
**Question:** In which situations must a company appoint a data protection officer?
**Reference answer:** When it is a public authority, or its core activities involve large-scale regular and systematic monitoring of people, or large-scale processing of special categories of data or criminal convictions data (Art. 37(1)).
**Agent answer:** A controller or processor must designate a data protection officer (DPO) if:
*   The processing is carried out by a public authority or body (except for courts acting in their judicial capacity) [gdpr, Article 37(1)(a)];
*   The core activities of the controller or processor consist of processing operations that require regular and systematic monitoring of data subjects on a large scale [gdpr, Article 37(1)(b)]; or
*   The core activities consist of processing on a large scale of special categories of data or personal data relating to criminal convictions and offences [gdpr, Article 37(1)(c)].

Additionally, a DPO must be designated where required by Union or Member State law [gdpr, Article 37(4)].
**Searches:** ['when must a company appoint a data protection officer?']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 37(1)-(3) | distance: 0.203
Designation of the data protection officer. 1. The controller and the processor shall designate a data protection officer in any case where: (a) the processing is carried out by a publi
- 2] source: gdpr | location: Article 37(4)-(7) | distance: 0.253
4. In cases other than those referred to in paragraph 1, the controller or processor or associations and other bodies representing categories of controllers or processors may or, where r
- 3] source: gdpr | location: Article 38 | distance: 0.268
Position of the data protection officer. 1. The controller and the processor shall ensure that the data protection officer is involved, properly and in a timely manner, in all issues which rela
- 4] source: gdpr | location: Article 39 | distance: 0.275
Tasks of the data protection officer. 1. The data protection officer shall have at least the following tasks: (a) to inform and advise the controller or the processor and the employees who carr
- 5] source: edpb_breach_notification | location: paras 131-132 (p.27) | distance: 0.287
131. Of particular relevance to breach notification, the mandatory tasks of the DPO includes, amongst other duties, providing data protection advice and informatio

## q03 (single)
**Question:** If a person is harmed because a company broke the data protection rules, who can they claim compensation from?
**Reference answer:** From the controller or the processor. The controller is liable for damage caused by infringing processing. A processor is liable only if it ignored obligations aimed specifically at processors or acted outside or against the controller's lawful instructions.
**Agent answer:** A person who has suffered material or non-material damage from an infringement can claim compensation from the controller or processor involved in the processing [gdpr, Article 82(1)]. While any controller involved is liable for damage caused by infringing processing, a processor is liable only if it failed to comply with GDPR obligations specifically directed to processors or acted outside or contrary to lawful instructions of the controller [gdpr, Article 82(2)]. Where multiple controllers or processors are responsible, each can be held liable for the entire damage to ensure effective compensation [gdpr, Article 82(4)].
**Searches:** ['right to compensation liability controller processor damages']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 82(1)-(4) | distance: 0.182
Right to compensation and liability. 1. Any person who has suffered material or non-material damage as a result of an infringement of this Regulation shall have the right to receive com
- 2] source: gdpr | location: Article 82(5)-(6) | distance: 0.229
5. Where a controller or processor has, in accordance with paragraph 4, paid full compensation for the damage suffered, that controller or processor shall be entitled to claim back from 
- 3] source: gdpr | location: Article 79 | distance: 0.272
Right to an effective judicial remedy against a controller or processor. 1. Without prejudice to any available administrative or non-judicial remedy, including the right to lodge a complaint wi
- 4] source: edpb_controller_processor | location: paras 8-9 (p.8) | distance: 0.283
8. The accountability principle has been further elaborated in Article 24, which states that the controller shall implement appropriate technical and organisational me
- 5] source: edpb_controller_processor | location: paras 72-74 (p.25) | distance: 0.284
Of course, the other public entities, as controllers for their own processing activities, are responsible for ensuring the accuracy of the data t hey previously pro

## q04 (single)
**Question:** A company loses a USB stick with unencrypted customer data and cannot tell whether anyone read it. Does it still have to report the breach?
**Reference answer:** Yes. Even if it cannot establish a confidentiality breach, an availability breach has occurred, and the company becomes aware when it realises the stick is lost.
**Agent answer:** Yes, the loss of a USB stick with unencrypted personal data must be notified [edpb_breach_notification, para 33 (p.11)]. Even if it is impossible to ascertain whether unauthorized persons accessed the data, the loss constitutes an availability breach, and the controller becomes "aware" of the breach when they realize the USB stick is missing [edpb_breach_notification, para 33 (p.11)].
**Searches:** ['personal data breach USB stick unencrypted notification requirement']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_breach_notification | location: para 138 (p.29) | distance: 0.203
The controller becomes “ aware ” of a personal data breach and assesses risk to individuals. B. Examples of personal data breaches and who to notify The following non-
- 2] source: edpb_breach_notification | location: para 33 (p.11) | distance: 0.203
33. When, exactly, a controller can be considered to be “aware” of a particular breach will depend on the circumstances of the specific breach. In some cases, it will be
- 3] source: edpb_breach_notification | location: para 78 (p.19) | distance: 0.239
78. Consequently, if personal data have been made essentially unintelligible to unautho rised parties and where the data are a copy or a backup exists, a confidentiality
- 4] source: edpb_breach_notification | location: para 79 (p.19) | distance: 0.247
79. Furthermore, it should be noted that if there is a breach where there are no backups of the encrypted personal data then there will have been an availability breach,
- 5] source: edpb_breach_notification | location: paras 60-61 (p.16) | distance: 0.247
60. It should also be clear that after making an initial notification, a controller could update the supervisory authority if a follow-up investigation uncovers evid

## q05 (single)
**Question:** Can a company send one single report to the authority for several similar data breaches?
**Reference answer:** Possibly, as a bundled notification, if the breaches involve the same type of data, breached in the same way, over a short period. If they differ, each breach must be reported separately.
**Agent answer:** Yes, a controller may submit a "bundled" notification for several similar breaches to avoid being overly burdensome [edpb_breach_notification, para 64 (p.16)]. This is permissible provided the breaches concern the same type of personal data, were breached in the same way, and occurred over a relatively short period of time [edpb_breach_notification, para 64 (p.16)]. If the breaches involve different types of data or were caused in different ways, they should generally be reported individually in accordance with Article 33 [edpb_breach_notification, para 64 (p.16)].
**Searches:** ['single report for several similar data breaches']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_breach_notification | location: paras 64-65 (p.16) | distance: 0.241
64. Strictly speaking, each individual breach is a reportable incident. However, to avoid being overly burdensome, the controller may be able to submit a “bundled” 
- 2] source: edpb_breach_notification | location: paras 62-63 (p.16) | distance: 0.278
62. Article 33(1) GDPR makes it clear that where notification to the supervisory authority is not made within 72 hours, it shall be accompanied by reasons for the de
- 3] source: edpb_breach_notification | location: paras 107-108 (p.24) | distance: 0.296
107. Of course, when assessing risk, a key factor is the type and sensitivity of personal data that has been compromised by the breach. Usually, the more sensitive
- 4] source: edpb_breach_notification | location: para 138 (p.29) | distance: 0.298
The controller then must notify the supervisory authority exploited with any of its controllers a notifiable breach may not have occurred but it is likely to be recorda
- 5] source: edpb_breach_notification | location: paras 52-54 (p.15) | distance: 0.298
52. Where precise information is not available (e.g. exact number of data subjects affected) this should not be a barrier to timely breach notification. The GDPR all

## q06 (single)
**Question:** Can an IT provider send the breach notification to the authority instead of the company?
**Reference answer:** Yes, if the company authorised it and it is part of their contract. But the legal responsibility to notify stays with the controller.
**Agent answer:** A processor (such as an IT provider) must notify the controller of a personal data breach without undue delay [gdpr, Article 33(2); edpb_breach_notification, para 44 (p.13)]. While the legal responsibility to notify the supervisory authority remains with the controller, a processor may make the notification on the controller's behalf if the controller has provided proper authorization and this is included in their contractual arrangements [edpb_breach_notification, para 48 (p.14)].
**Searches:** ['processor breach notification to supervisory authority']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_breach_notification | location: para 44 (p.13) | distance: 0.203
44. Article 33(2) GDPR makes it clear that if a processor is used by a controller and the processor becomes aware of a breach of the personal data it is processing on b
- 2] source: gdpr | location: Article 33(1)-(3) | distance: 0.205
Notification of a personal data breach to the supervisory authority. 1. In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later tha
- 3] source: edpb_controller_processor | location: para 136 (p.39) | distance: 0.210
136. Secondly, the processor must assist the controller in meeting the obligation to notify personal data breaches to the supervisory authority and to data subjects. T
- 4] source: edpb_breach_notification | location: paras 47-49 (p.14) | distance: 0.215
47. Where the processor provides services to multiple controllers that are all affected by the same incident, the processor will have to report details of the incide
- 5] source: edpb_breach_notification | location: paras 44-46 (p.13) | distance: 0.219
The controller might also want to investigate the breach, as the processor might not be in a position to know all the relevant facts relating to the matter, for exam

## q07 (single)
**Question:** If a contract calls a company a processor, does that decide whether it is really a processor?
**Reference answer:** No. The roles depend on the actual activities in the specific situation, not on the label in a contract, and they are not negotiable.
**Agent answer:** No, a contract calling a company a processor does not decide its status. The concepts of controller and processor are functional, meaning their status is determined by their actual activities and the factual circumstances of the processing, rather than by formal designation in a contract [edpb_controller_processor, para 12 (p.8), para 29 (p.13)].

If a party in fact decides the "why" and "how" of the processing, it is a controller regardless of what the contract says [edpb_controller_processor, para 29 (p.13)]. Parties cannot escape controller obligations or allocate responsibilities simply by shaping a contract in a certain way if the factual reality is different [edpb_controller_processor, paras 27-28 (p.12)].
**Searches:** ['does a contract calling a company a processor decide its status?']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_controller_processor | location: para 29 (p.13) | distance: 0.178
29. If one party in fact decides why and how personal data are processed that party will be a controller even if a contract says that it is a processor. Similarly, it 
- 2] source: edpb_controller_processor | location: para 30 (p.13) | distance: 0.202
30. In line with the factual approach, the word “determines” means that the entity that actually exerts a decisive influence on the purposes and means of the processing
- 3] source: edpb_controller_processor | location: paras 27-28 (p.12) | distance: 0.204
The controller in respect of any personal data contained inside the message will normally be considered to be the person from whom the message originates, rather th
- 4] source: edpb_controller_processor | location: paras 10-12 (p.8) | distance: 0.211
10. The accountability principle, together with the other, more specific rules on how to comply with the GDPR and the distribution of responsibility, therefore makes
- 5] source: edpb_controller_processor | location: para 104 (p.32) | distance: 0.213
104. In order to comply with the duty to enter into a contract, the controller and the processor may choose to negotiate their own contract including all the compulsor

## q08 (single)
**Question:** Who is responsible for personal data that employees handle as part of their job: the employee or the company?
**Reference answer:** The company. Processing by employees within the organisation's activities is presumed to be under its control, and employees are generally not controllers themselves. Even if an employee misuses data, the company must have adequate measures, such as training.
**Agent answer:** Employees who handle personal data within the scope of their work are generally considered to be acting under the authority of the organization, which acts as the controller [edpb_controller_processor, para 19 (p.10), para 88 (p.29)]. It is the organization's responsibility to ensure compliance through adequate technical and organizational measures [edpb_controller_processor, para 19 (p.10)].

However, if an employee processes personal data for their own purposes, distinct from those of the employer, they may be considered a controller themselves and assume the resulting liabilities [edpb_controller_processor, para 19 (p.10), para 88 (p.29)].
**Searches:** ['who is the controller for employee data processing']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_controller_processor | location: para 19 (p.10) | distance: 0.215
19. In principle, any processing of personal data by employees which takes place within the realm of activities of an organisation may be presumed to take place under 
- 2] source: edpb_controller_processor | location: para 17 (p.10) | distance: 0.224
17. The first building block relates to the type of entity that can be a controller. Under the GDPR, a controller can be “a natural or legal person, public authority, a
- 3] source: edpb_controller_processor | location: para 27 (p.12) | distance: 0.226
27. In practice, certain processing activities can be considered as naturally attached to the role or activities of an entity ultimately entailing responsibilities from
- 4] source: edpb_controller_processor | location: para 88 (p.29) | distance: 0.233
88. Whereas the terms “ personal data”, “data subject ”, “controller” and “ processor” are defined in the Regulation, the concept of “persons who, under the direct auth
- 5] source: edpb_controller_processor | location: front matter (p.1) | distance: 0.237
Controller In principle, there is no limitation as to the type of entity that may assume the role of a controller but in practice it is usually the organisation as 

## q09 (multi)
**Question:** A hacker emails a company demanding a ransom after breaking into its systems. By when must the company notify the authority, and when does that period start counting?
**Reference answer:** Within 72 hours where feasible after becoming aware (Art. 33(1)). It is aware once it has checked its systems and has clear evidence that the attack happened (para 33, ransom example).
**Agent answer:** A company must notify the competent supervisory authority of a personal data breach without undue delay and, where feasible, not later than 72 hours after becoming aware of it [gdpr, Article 33(1); edpb_breach_notification, para 29 (p.10)]. 

A controller is considered to have become "aware" when it has a reasonable degree of certainty that a security incident has occurred that has led to personal data being compromised [edpb_breach_notification, para 31 (p.11)]. The 72-hour period begins at this point of awareness [edpb_breach_notification, para 35 (p.12)]. If the notification is not made within 72 hours, it must be accompanied by reasons for the delay [gdpr, Article 33(1)].
**Searches:** ['time limit for personal data breach notification to authority']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_breach_notification | location: para 35 (p.12) | distance: 0.219
35. Once the controller has become aware, a notifiable breach must be notified without undue delay, and where feasible, not later than 72 hours. During this period, the
- 2] source: edpb_breach_notification | location: paras 28-29 (p.10) | distance: 0.224
In that case, the supervisory authority will also have the possibility to issue sanctions for failure to notify or communicate the breach (Articles 33 and 34 GDPR) o
- 3] source: edpb_breach_notification | location: paras 31-32 (p.11) | distance: 0.227
31. As detailed above, the GDPR requires that, in the case of a breach, the controller shall notify the breach without undue delay and, where feasible, not later tha
- 4] source: gdpr | location: Article 33(1)-(3) | distance: 0.229
Notification of a personal data breach to the supervisory authority. 1. In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later tha
- 5] source: edpb_breach_notification | location: paras 40-41 (p.13) | distance: 0.232
40. Accordingly, it should be clear that there is an obligation on the controller to act on any initial alert and establish whether or not a breach has, in fact, occ

## q10 (multi)
**Question:** If hackers steal encrypted customer data, does the company still have to report the breach, and does it have to tell the customers?
**Reference answer:** A confidentiality breach of encrypted data is still a personal data breach and has to be notified (para 76). Telling the customers is not required if the key was not compromised and the data is unintelligible (Art. 34(3)(a)), but it would be required if people can be harmed through lost or altered data without adequate backups.
**Agent answer:** Whether a company must report a breach of encrypted data depends on whether the breach poses a risk to individuals' rights and freedoms [edpb_breach_notification, para 78 (p.19)]. If the data is properly encrypted and the key remains secure, the data is considered unintelligible, and notification may not be required because the breach is unlikely to pose a risk [edpb_breach_notification, para 76 (p.18), para 78 (p.19)].

However, notification may still be required if:
*   The encryption key is compromised or the encryption software is vulnerable [edpb_breach_notification, para 78 (p.19), para 79 (p.19)].
*   There are no adequate backups, leading to an availability breach that poses risks to individuals [edpb_breach_notification, para 76 (p.18), para 79 (p.19)].
*   The loss of data, even if encrypted, results in a lack of availability that negatively affects individuals [edpb_breach_notification, para 79 (p.19)].

If the breach is unlikely to result in a risk to individuals, notification to the supervisory authority and the data subjects is generally not required, though the risk must be re-evaluated if circumstances change [edpb_breach_notification, para 78 (p.19)].
**Searches:** ['breach notification encrypted data']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_breach_notification | location: para 78 (p.19) | distance: 0.232
78. Consequently, if personal data have been made essentially unintelligible to unautho rised parties and where the data are a copy or a backup exists, a confidentialit
- 2] source: edpb_breach_notification | location: paras 76-77 (p.18) | distance: 0.241
38 WP29, Opinion 03/2014 on breach notification, http://ec.europa.eu/justice/dataprotection/article29/documentation/opinion-recommendation/files/2014/wp213_en.pdf re
- 3] source: edpb_breach_notification | location: para 79 (p.19) | distance: 0.244
79. Furthermore, it should be noted that if there is a breach where there are no backups of the encrypted personal data then there will have been an availability breach,
- 4] source: edpb_breach_notification | location: para 76 (p.18) | distance: 0.245
76. In its Opinion 03/2014 on breach notification 38 , WP29 explained that a confidentiality breach of personal data that were encrypted with a state of the art algorith
- 5] source: edpb_breach_notification | location: para 79 (p.19) | distance: 0.257
If it later become s evident that the encryption key was compromised or that the encryption software or algorithm is vulnerable, then the risk to the rights and freedoms

## q11 (multi)
**Question:** Does a company have to keep a record of data breaches, and how long must it keep it?
**Reference answer:** Yes, it must document any breach: the facts, its effects and the remedial action (Art. 33(5)). The GDPR sets no specific retention period, so the controller decides an appropriate one under the data protection principles (para 124).
**Agent answer:** Yes, under Article 33(5) of the GDPR, a controller must document all personal data breaches, including the facts relating to the breach, its effects, and the remedial action taken, to enable the supervisory authority to verify compliance [edpb_breach_notification, para 121 (p.26)].

The GDPR does not specify a retention period for these records [edpb_breach_notification, para 124 (p.26)]. If the records contain personal data, the controller must determine an appropriate retention period in accordance with GDPR principles, such as the storage limitation principle, and ensure there is a lawful basis for processing [edpb_breach_notification, para 124 (p.26)].
**Searches:** ['record of data breaches retention period']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_breach_notification | location: para 124 (p.26) | distance: 0.203
124. The GDPR does not specify a retention period for such documentation. Where such records contain personal data, it will be incumbent on the controller to de termin
- 2] source: edpb_breach_notification | location: paras 122-123 (p.26) | distance: 0.227
122. This is linked to the accountability principle of the GDPR, contained in Article 5(2) GDPR. The purpose of recording non- notifiable breaches, as well notifia
- 3] source: edpb_breach_notification | location: paras 119-121 (p.26) | distance: 0.264
119. Therefore, when assessing the risk that is likely to result from a breach, the controller should consider a combination of the severity of the potential impac
- 4] source: edpb_breach_notification | location: paras 125-127 (p.27) | distance: 0.268
125. In addition to these details, the EDPB recommends that the controller also document its reasoning for the decisions taken in response to a breach. In particul
- 5] source: gdpr | location: Article 30(1) | distance: 0.277
Records of processing activities. 1. Each controller and, where applicable, the controller's representative, shall maintain a record of processing activities under its responsibility. That r

## q12 (multi)
**Question:** If a service provider that processes data for a company starts using it for its own business, what is its legal position and can it be held liable?
**Reference answer:** It infringes the GDPR by going beyond the controller's instructions and is considered a controller for that processing, and may face sanctions (para 81). A processor is liable for damage when it acted outside or contrary to the controller's lawful instructions (Art. 82(2)).
**Agent answer:** If a service provider processes data for its own purposes, it goes beyond the controller's instructions and is considered a data controller for that specific processing [edpb_controller_processor, para 81 (p.26)]. By determining its own purposes and means of processing, the provider infringes the GDPR and may be subject to sanctions [edpb_controller_processor, para 81 (p.26)].
**Searches:** ['processor using data for own purposes controller processor role change']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_controller_processor | location: para 81 (p.26) | distance: 0.200
81. Acting “on behalf of” also means that the processor may not carry out proc essing for its own purpose(s). As provided in Article 28(10), a processor infringes the 
- 2] source: edpb_controller_processor | location: para 191 (p.48) | distance: 0.216
Factors that indicate that you are the controller Factors that indicate that you are the processor • You obtain a benefit from, or have an interest in, the processing 
- 3] source: edpb_controller_processor | location: paras 75-77 (p.25) | distance: 0.216
75. Processing of personal data can involve multiple processors. For example, a co ntroller may itself choose to directly engage multiple processors, by involving d
- 4] source: edpb_controller_processor | location: paras 34-36 (p.14) | distance: 0.217
34. The GDPR establishes that data must be collected for specified, explicit and legitimate purposes and not further processed in a way incompatible with those purp
- 5] source: edpb_controller_processor | location: para 40 (p.15) | distance: 0.226
Employer A gives clear instructions on who to pay, what amounts, by what date, by which bank, how long the data shall be stored, what data should be disclosed to the ta

## q13 (multi)
**Question:** When a company reports a breach, does it have to tell the authority who its data protection officer is, and can that officer be an outside consultant?
**Reference answer:** Yes, the notification must include the DPO's name and contact details, or another contact point (Art. 33(3)(b)). A DPO may be a staff member or work under a service contract, so an external provider is allowed (Art. 37(6)).
**Agent answer:** When a company notifies a supervisory authority of a personal data breach, it is required to provide the name and contact details of its data protection officer (DPO) or another contact point where more information can be obtained [gdpr, Article 33(3)(b); edpb_breach_notification, para 131 (p.27)].

Regarding the DPO's status, the GDPR explicitly states that a DPO may be a staff member of the controller or processor, or they may fulfill the tasks on the basis of a service contract [gdpr, Article 37(6)].
**Searches:** ['breach notification content data protection officer contact details', 'can the data protection officer be an external consultant']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_breach_notification | location: paras 131-132 (p.27) | distance: 0.198
131. Of particular relevance to breach notification, the mandatory tasks of the DPO includes, amongst other duties, providing data protection advice and informati
- 2] source: edpb_breach_notification | location: paras 86-87 (p.20) | distance: 0.223
86. According to this provision, the controller should at least provide the following information: • a description of the nature of the breach; • the name and contac
- 3] source: edpb_breach_notification | location: paras 128-130 (p.27) | distance: 0.238
128. To aid compliance with Articles 33 and 34 GDPR, it would be advantageous to both controllers and processors to have a documented notification procedure in pla
- 4] source: gdpr | location: Article 33(1)-(3) | distance: 0.242
Notification of a personal data breach to the supervisory authority. 1. In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later tha
- 5] source: edpb_breach_notification | location: paras 133-134 (p.27) | distance: 0.250
133. These factors mean that the DPO should play an key role in assisting the prevention of or preparation for a breach by providing advice and monitoring complian

## q14 (multi)
**Question:** When are two companies considered to be deciding jointly about the same data, and what must they arrange between themselves if they are?
**Reference answer:** They are joint controllers when both take part in determining the purposes and means, through a common decision or converging decisions (para 54). They must set out transparently, in an arrangement, who is responsible for what, especially for data subject rights and information duties (Art. 26(1)).
**Agent answer:** Two companies are considered joint controllers when they jointly determine the purposes and means of a specific processing activity, meaning they have a decisive influence over whether and how the processing takes place [gdpr, Article 26(1); edpb_controller_processor, para 51 (p.19), para 54 (p.19)]. This joint participation can result from a common decision or converging decisions that are necessary for the processing to occur [edpb_controller_processor, front matter (p.1), para 54 (p.19)].

If they are joint controllers, they must determine their respective responsibilities for compliance with the GDPR—particularly regarding data subject rights and information duties—by means of a transparent arrangement [gdpr, Article 26(1)]. This arrangement should reflect their actual roles and relationships, and its essence must be made available to the data subject [gdpr, Article 26(2)]. The EDPB recommends that this arrangement be a binding document, such as a contract, to ensure legal certainty, transparency, and accountability [edpb_controller_processor, front matter (p.1)]. Regardless of this arrangement, data subjects may exercise their rights against each of the controllers [gdpr, Article 26(3)].
**Searches:** ['joint controllers definition and arrangement between them']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 26 | distance: 0.217
Joint controllers. 1. Where two or more controllers jointly determine the purposes and means of processing, they shall be joint controllers. They shall in a transparent manner determine their 
- 2] source: edpb_controller_processor | location: para 51 (p.19) | distance: 0.222
51. Article 26 GDPR, which reflects the definition in Article 4 (7) GDPR, provides that “[w]here two or more controllers jointly determine the purposes and means of pro
- 3] source: edpb_controller_processor | location: paras 53-54 (p.19) | distance: 0.227
53. Not all processing involving several entities give rise to joint controllership. The overarching criterion for joint controllership to exist is the joint partic
- 4] source: edpb_controller_processor | location: front matter (p.1) | distance: 0.229
Joint controllers The qualification as joint controllers may arise where more than one actor is involved in the processing. The GDPR introduces specific rules for j
- 5] source: edpb_controller_processor | location: front matter (p.1) | distance: 0.229
In addition to this, the distribution of responsibilities should cover other controller obligations such as regarding the general data protection principles, legal 

## q15 (multi)
**Question:** A company uses an outside provider to handle sensitive data on a large scale. Who must carry out the impact assessment, and when is one required?
**Reference answer:** The controller must carry one out before processing that is likely to result in a high risk, for example large-scale processing of special categories of data (Art. 35(1), (3)(b)). The processor may do the work in practice but only assists when necessary and on request, so the controller remains accountable and must take the initiative (para 138).
**Agent answer:** The controller is responsible for carrying out a data protection impact assessment (DPIA) prior to processing when a type of processing is likely to result in a high risk to the rights and freedoms of natural persons [gdpr, Article 35(1)].

A DPIA is specifically required for:
*   Systematic and extensive evaluation of personal aspects based on automated processing (including profiling) that produces legal or similarly significant effects [gdpr, Article 35(3)(a)].
*   Processing on a large scale of special categories of data or personal data relating to criminal convictions and offences [gdpr, Article 35(3)(b)].
*   Systematic monitoring of a publicly accessible area on a large scale [gdpr, Article 35(3)(c)].

When carrying out the assessment, the controller must seek the advice of their data protection officer, if one has been designated [gdpr, Article 35(2)].
**Searches:** ['who must carry out data protection impact assessment and when is it required']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 35(1)-(3) | distance: 0.236
Data protection impact assessment. 1. Where a type of processing in particular using new technologies, and taking into account the nature, scope, context and purposes of the processing,
- 2] source: gdpr | location: Article 35(7)-(9) | distance: 0.257
7. The assessment shall contain at least: (a) a systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitim
- 3] source: gdpr | location: Article 35(10)-(11) | distance: 0.276
10. Where processing pursuant to point (c) or (e) of Article 6(1) has a legal basis in Union law or in the law of the Member State to which the controller is subject, that law regulate
- 4] source: edpb_breach_notification | location: para 104 (p.23) | distance: 0.286
104. It should be noted that assessing the risk to people’s rights and freedoms as a result of a breach has a different focus to the risk considered in a DPIA) 44. The 
- 5] source: gdpr | location: Article 35(4)-(6) | distance: 0.287
4. The supervisory authority shall establish and make public a list of the kind of processing operations which are subject to the requirement for a data protection impact assessment purs

## q16 (unanswerable)
**Question:** What form must a company in Spain fill in to report a data breach to the Spanish data protection authority?
**Reference answer:** The documents do not cover the Spanish authority's forms or procedure. The assistant should say so; it may only mention that Article 33(3) lists the minimum content of a notification.
**Agent answer:** The provided documents do not contain information regarding specific forms required by the Spanish data protection authority. The GDPR and EDPB guidelines specify the information that must be included in a breach notification [gdpr, Article 33(3); edpb_breach_notification, para 86 (p.20)], but they do not mandate a specific form.
**Searches:** ['form to report a data breach to the Spanish data protection authority']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 33(1)-(3) | distance: 0.342
Notification of a personal data breach to the supervisory authority. 1. In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later th
- 2] source: edpb_breach_notification | location: para 37 (p.12) | distance: 0.359
37. The controller should therefore have internal processes in place to be able to detect and address a breach. For example, for finding some irregularities in data proc
- 3] source: edpb_breach_notification | location: paras 86-87 (p.20) | distance: 0.363
86. According to this provision, the controller should at least provide the following information: • a description of the nature of the breach; • the name and contac
- 4] source: edpb_breach_notification | location: para 13 (p.7) | distance: 0.365
13. As part of any attempt to address a breach the controller should first be able to recognise one. The GDPR defines a “personal data breach” in Article 4(12) as: “a bre
- 5] source: edpb_breach_notification | location: para 57 (p.15) | distance: 0.367
57. This means that the GDPR recognises that controllers will not always have all of the necessary information concerning a breach within 72 hours of becoming aware of i

## q17 (unanswerable)
**Question:** What deadline does the NIS2 Directive set for reporting a major cyber incident?
**Reference answer:** Not covered. The corpus only mentions the older NIS Directive, which requires notifying incidents, and gives no NIS2 deadlines. The assistant should say it does not know.
**Agent answer:** The provided corpus does not contain information regarding the NIS2 Directive or its specific deadlines for reporting cyber incidents. The documents only reference the earlier NIS Directive (Directive 2016/1148) in the context of its relationship with GDPR breach notification requirements [edpb_breach_notification, para 136 (p.28)].
**Searches:** ['NIS2 Directive deadline reporting major cyber incident']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_breach_notification | location: para 136 (p.28) | distance: 0.283
136. Articles 14 and 16 of the NIS Directive require operators of essential services and digital service providers to notify security incidents to their competent auth
- 2] source: edpb_breach_notification | location: para 135 (p.28) | distance: 0.300
135. Article 19(2) of the eIDAS Regulation requires trust service providers to notify their supervisory body of a breach of security or loss of integrity that has a sig
- 3] source: edpb_breach_notification | location: para 138 (p.29) | distance: 0.309
The controller should take action, e.g. by forcing password resets of the affected accounts, as well as other steps to mitigate the risk. The controller should also con
- 4] source: edpb_breach_notification | location: para 138 (p.29) | distance: 0.311
The controller then must notify the supervisory authority exploited with any of its controllers a notifiable breach may not have occurred but it is likely to be recorda
- 5] source: edpb_breach_notification | location: para 21 (p.9) | distance: 0.316
21. Therefore, a security incident resulting in personal data being made unavailable for a period of time is also a type of breach, as the lack of access to the data can 

## q18 (unanswerable)
**Question:** Does a website need a cookie banner to track its visitors?
**Reference answer:** Not covered. The documents do not deal with the rules on cookies. The assistant should say the corpus does not answer this.
**Agent answer:** The provided corpus does not contain information regarding cookie banners. It covers the GDPR's requirements for processing personal data, including conditions for consent [gdpr, Article 7] and the information that must be provided when collecting personal data [gdpr, Article 13], but it does not specifically address the use of cookie banners.
**Searches:** ['cookie banner tracking visitors']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 4 part 1 | distance: 0.387
Definitions. For the purposes of this Regulation: (1) ‘personal data’ means any information relating to an identified or identifiable natural person (‘data subject’); an identifiable nat
- 2] source: gdpr | location: Article 7 | distance: 0.389
Conditions for consent. 1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data. 2. If 
- 3] source: gdpr | location: Article 3 | distance: 0.395
Territorial scope. 1. This Regulation applies to the processing of personal data in the context of the activities of an establishment of a controller or a processor in the Union, regardless of w
- 4] source: gdpr | location: Article 22 | distance: 0.402
Automated individual decision-making, including profiling. 1. The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, wh
- 5] source: gdpr | location: Article 13(1) | distance: 0.403
Information to be provided where personal data are collected from the data subject. 1. Where personal data relating to a data subject are collected from the data subject, the controller shal

## q19 (unanswerable)
**Question:** How long should a shop keep its security camera recordings?
**Reference answer:** Not covered. The documents set no retention period for video surveillance recordings. The assistant should say so.
**Agent answer:** The GDPR does not specify a fixed retention period for security camera recordings. Under the principle of "storage limitation," personal data must be kept in a form that permits identification of data subjects for no longer than is necessary for the purposes for which the data are processed [gdpr, Article 5(1)(e)]. It is the responsibility of the controller to determine the appropriate retention period in accordance with these principles [edpb_breach_notification, para 124 (p.26)].
**Searches:** ['retention period security camera recordings GDPR']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 5(1)-(2) | distance: 0.256
(e) kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed; personal data may be stored f
- 2] source: edpb_breach_notification | location: para 124 (p.26) | distance: 0.264
124. The GDPR does not specify a retention period for such documentation. Where such records contain personal data, it will be incumbent on the controller to de termine
- 3] source: gdpr | location: Article 32(1)-(2) | distance: 0.294
Security of processing. 1. Taking into account the state of the art, the costs of implementation and the nature, scope, context and purposes of processing as well as the risk of varying 
- 4] source: gdpr | location: Article 30(1) | distance: 0.296
Records of processing activities. 1. Each controller and, where applicable, the controller's representative, shall maintain a record of processing activities under its responsibility. That r
- 5] source: gdpr | location: Article 5(1) | distance: 0.297
Principles relating to processing of personal data. 1. Personal data shall be: (a) processed lawfully, fairly and in a transparent manner in relation to the data subject (‘lawfulness, fairnes

## q20 (unanswerable)
**Question:** What does the EU AI Act say about using facial recognition in shops?
**Reference answer:** Not covered. The corpus does not deal with the EU AI Act. The assistant should say so.
**Agent answer:** The provided corpus does not contain the EU AI Act; therefore, I cannot provide information regarding its provisions on the use of facial recognition in shops. The available documents are limited to the GDPR and specific EDPB guidelines.
**Searches:** ['facial recognition in shops AI Act']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 35(1)-(3) | distance: 0.350
Data protection impact assessment. 1. Where a type of processing in particular using new technologies, and taking into account the nature, scope, context and purposes of the processing,
- 2] source: gdpr | location: Article 4 part 1 | distance: 0.355
Definitions. For the purposes of this Regulation: (1) ‘personal data’ means any information relating to an identified or identifiable natural person (‘data subject’); an identifiable natu
- 3] source: gdpr | location: Article 22 | distance: 0.359
Automated individual decision-making, including profiling. 1. The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, wh
- 4] source: gdpr | location: Article 4 part 4 | distance: 0.363
(13) ‘genetic data’ means personal data relating to the inherited or acquired genetic characteristics of a natural person which give unique information about the physiology or the health 
- 5] source: gdpr | location: Article 3 | distance: 0.372
Territorial scope. 1. This Regulation applies to the processing of personal data in the context of the activities of an establishment of a controller or a processor in the Union, regardless of w

## q21 (unanswerable)
**Question:** What did the Schrems II court case decide about sending data to the United States?
**Reference answer:** Not covered. The corpus does not discuss that judgment or transfers to the United States specifically. The assistant should say so.
**Agent answer:** The provided corpus does not contain information regarding the *Schrems II* court case. Therefore, I cannot answer your question using these sources.
**Searches:** ['Schrems II court case United States data transfer']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 45(1)-(2) | distance: 0.297
Transfers on the basis of an adequacy decision. 1. A transfer of personal data to a third country or an international organisation may take place where the Commission has decided that t
- 2] source: gdpr | location: Article 48 | distance: 0.309
Transfers or disclosures not authorised by Union law. Any judgment of a court or tribunal and any decision of an administrative authority of a third country requiring a controller or processor 
- 3] source: gdpr | location: Article 46(1)-(2) | distance: 0.324
Transfers subject to appropriate safeguards. 1. In the absence of a decision pursuant to Article 45(3), a controller or processor may transfer personal data to a third country or an inte
- 4] source: gdpr | location: Article 45(5)-(7) | distance: 0.325
5. The Commission shall, where available information reveals, in particular following the review referred to in paragraph 3 of this Article, that a third country, a territory or one or m
- 5] source: gdpr | location: Article 45(2) | distance: 0.330
(b) the existence and effective functioning of one or more independent supervisory authorities in the third country or to which an international organisation is subject, with responsibility 

## q22 (unanswerable)
**Question:** What is the largest fine ever imposed under the GDPR?
**Reference answer:** The corpus contains the legal maximum amounts of fines (Article 83) but nothing about fines actually imposed, so the assistant should say it cannot tell which fine was the largest.
**Agent answer:** The provided corpus does not contain information regarding specific fines imposed by supervisory authorities, including the largest fine ever issued. It only outlines the legal framework for administrative fines, including the maximum amounts and the criteria for their imposition [gdpr, Article 83].
**Searches:** ['largest fine ever imposed under the GDPR']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 83(5)-(6) | distance: 0.241
5. Infringements of the following provisions shall, in accordance with paragraph 2, be subject to administrative fines up to 20 000 000 EUR, or in the case of an undertaking, up to 4 % 
- 2] source: gdpr | location: Article 83(2) | distance: 0.278
2. Administrative fines shall, depending on the circumstances of each individual case, be imposed in addition to, or instead of, measures referred to in points (a) to (h) and (j) of Article 
- 3] source: gdpr | location: Article 83(4) | distance: 0.289
4. Infringements of the following provisions shall, in accordance with paragraph 2, be subject to administrative fines up to 10 000 000 EUR, or in the case of an undertaking, up to 2 % of th
- 4] source: gdpr | location: Article 83(1) | distance: 0.289
General conditions for imposing administrative fines. 1. Each supervisory authority shall ensure that the imposition of administrative fines pursuant to this Article in respect of infringeme
- 5] source: gdpr | location: Article 58(2) | distance: 0.292
2. Each supervisory authority shall have all of the following corrective powers: (a) to issue warnings to a controller or processor that intended processing operations are likely to infringe

## q23 (single)
**Question:** If a customer agreed to receive marketing emails, can they take that agreement back later, and how easy must that be?
**Reference answer:** Yes, at any time. Withdrawing consent must be as easy as giving it, and it does not affect the lawfulness of processing done before the withdrawal (Art. 7(3)).
**Agent answer:** Yes, a customer has the right to withdraw their consent at any time [gdpr, Article 7(3)]. It must be as easy to withdraw consent as it was to give it [gdpr, Article 7(3)]. Additionally, for direct marketing, individuals have the right to object to the processing of their personal data for such purposes at any time [gdpr, Article 21(2)].
**Searches:** ['withdrawal of consent marketing emails']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 7 | distance: 0.279
Conditions for consent. 1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data. 2. If
- 2] source: gdpr | location: Article 17(1) | distance: 0.337
Right to erasure (‘right to be forgotten’). 1. The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay and 
- 3] source: gdpr | location: Article 21(1)-(4) | distance: 0.344
Right to object. 1. The data subject shall have the right to object, on grounds relating to his or her particular situation, at any time to processing of personal data concerning him or 
- 4] source: gdpr | location: Article 21(5)-(6) | distance: 0.359
5. In the context of the use of information society services, and notwithstanding Directive 2002/58/EC, the data subject may exercise his or her right to object by automated means using 
- 5] source: gdpr | location: Article 6(1) | distance: 0.359
Lawfulness of processing. 1. Processing shall be lawful only if and to the extent that at least one of the following applies: (a) the data subject has given consent to the processing of his o

## q24 (single)
**Question:** Can a customer ask a company to hand over their data in a format that another provider can use?
**Reference answer:** Yes. For data they provided, where processing is based on consent or a contract and done by automated means, they can receive it in a structured, commonly used, machine-readable format and have it transmitted to another controller, directly where technically feasible (Art. 20).
**Agent answer:** Yes, under the right to data portability, a data subject has the right to receive the personal data they provided to a controller in a "structured, commonly used and machine-readable format" [gdpr, Article 20(1)]. They also have the right to have those data transmitted directly from one controller to another, where technically feasible, provided the processing is based on consent or a contract and is carried out by automated means [gdpr, Article 20(1)-(2)].
**Searches:** ['right to data portability format']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 20 | distance: 0.208
Right to data portability. 1. The data subject shall have the right to receive the personal data concerning him or her, which he or she has provided to a controller, in a structured, commonly 
- 2] source: gdpr | location: Article 15(1) | distance: 0.313
Right of access by the data subject. 1. The data subject shall have the right to obtain from the controller confirmation as to whether or not personal data concerning him or her are being pr
- 3] source: gdpr | location: Article 15(2)-(4) | distance: 0.317
2. Where personal data are transferred to a third country or to an international organisation, the data subject shall have the right to be informed of the appropriate safeguards pursuant
- 4] source: gdpr | location: Article 12(1)-(2) | distance: 0.340
Transparent information, communication and modalities for the exercise of the rights of the data subject. 1. The controller shall take appropriate measures to provide any information ref
- 5] source: gdpr | location: Article 13(2) | distance: 0.341
2. In addition to the information referred to in paragraph 1, the controller shall, at the time when personal data are obtained, provide the data subject with the following further informati

## q25 (single)
**Question:** Can a person tell a company to stop using their data for advertising?
**Reference answer:** Yes. They can object at any time to processing for direct marketing, and the data must then no longer be processed for that purpose (Art. 21(2)-(3)).
**Agent answer:** Yes, a person has the right to object at any time to the processing of their personal data for direct marketing purposes, which includes related profiling [gdpr, Article 21(2)]. Once a person objects to such processing, the company must stop using their data for those purposes [gdpr, Article 21(3)].
**Searches:** ['right to object to processing for direct marketing']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 21(1)-(4) | distance: 0.224
Right to object. 1. The data subject shall have the right to object, on grounds relating to his or her particular situation, at any time to processing of personal data concerning him or
- 2] source: gdpr | location: Article 21(5)-(6) | distance: 0.251
5. In the context of the use of information society services, and notwithstanding Directive 2002/58/EC, the data subject may exercise his or her right to object by automated means using 
- 3] source: gdpr | location: Article 18 | distance: 0.306
Right to restriction of processing. 1. The data subject shall have the right to obtain from the controller restriction of processing where one of the following applies: (a) the accuracy of the 
- 4] source: gdpr | location: Article 17(3) | distance: 0.314
3. Paragraphs 1 and 2 shall not apply to the extent that processing is necessary: (a) for exercising the right of freedom of expression and information; (b) for compliance with a legal oblig
- 5] source: gdpr | location: Article 22 | distance: 0.322
Automated individual decision-making, including profiling. 1. The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, wh

## q26 (single)
**Question:** What does a data protection authority have to take into account when deciding how big a fine should be?
**Reference answer:** Factors such as the nature, gravity and duration of the infringement, whether it was intentional or negligent, actions taken to reduce the damage, the degree of responsibility, previous infringements, cooperation with the authority, the categories of data affected, how the authority learned of it (including whether the company notified it), and adherence to codes of conduct (Art. 83(2)).
**Agent answer:** When deciding on the amount of an administrative fine, a supervisory authority must ensure the fine is effective, proportionate, and dissuasive in each individual case [gdpr, Article 83(1)].

The authority must give due regard to the following factors:
*   The nature, gravity, and duration of the infringement, including the nature, scope, or purpose of the processing, the number of data subjects affected, and the level of damage suffered [gdpr, Article 83(2)(a)].
*   Whether the infringement was intentional or negligent [gdpr, Article 83(2)(b)].
*   Actions taken to mitigate the damage [gdpr, Article 83(2)(c)].
*   The degree of responsibility, considering technical and organisational measures implemented [gdpr, Article 83(2)(d)].
*   Any relevant previous infringements [gdpr, Article 83(2)(e)].
*   The degree of cooperation with the supervisory authority [gdpr, Article 83(2)(f)].
*   The categories of personal data affected [gdpr, Article 83(2)(g)].
*   The manner in which the infringement became known to the authority, including whether it was notified [gdpr, Article 83(2)(h)].
*   Compliance with previously ordered measures [gdpr, Article 83(2)(i)].
*   Adherence to approved codes of conduct or certification mechanisms [gdpr, Article 83(2)(j)].
*   Any other aggravating or mitigating factors, such as financial benefits gained or losses avoided [gdpr, Article 83(2)(k)].
**Searches:** ['factors for deciding administrative fines GDPR']
**Retrieved (first 250 characters of each passage):**
- [1] source: gdpr | location: Article 83(2) | distance: 0.146
2. Administrative fines shall, depending on the circumstances of each individual case, be imposed in addition to, or instead of, measures referred to in points (a) to (h) and (j) of Article
- 2] source: gdpr | location: Article 83(2)-(3) | distance: 0.196
(h) the manner in which the infringement became known to the supervisory authority, in particular whether, and if so to what extent, the controller or processor notified the infringement
- 3] source: gdpr | location: Article 83(1) | distance: 0.211
General conditions for imposing administrative fines. 1. Each supervisory authority shall ensure that the imposition of administrative fines pursuant to this Article in respect of infringeme
- 4] source: gdpr | location: Article 83(5)-(6) | distance: 0.220
5. Infringements of the following provisions shall, in accordance with paragraph 2, be subject to administrative fines up to 20 000 000 EUR, or in the case of an undertaking, up to 4 % o
- 5] source: gdpr | location: Article 83(4) | distance: 0.233
4. Infringements of the following provisions shall, in accordance with paragraph 2, be subject to administrative fines up to 10 000 000 EUR, or in the case of an undertaking, up to 2 % of th

## q27 (single)
**Question:** What are the three kinds of personal data breach?
**Reference answer:** Confidentiality breach (unauthorised or accidental disclosure of or access to data), integrity breach (unauthorised or accidental alteration of data) and availability breach (accidental or unauthorised loss of access to, or destruction of, data).
**Agent answer:** Personal data breaches can be categorized into the following three types based on information security principles [edpb_breach_notification, para 17 (p.7)]:

*   **Confidentiality breach:** Unauthorized or accidental disclosure of, or access to, personal data [edpb_breach_notification, para 17 (p.7)].
*   **Integrity breach:** Unauthorized or accidental alteration of personal data [edpb_breach_notification, para 17 (p.7)].
*   **Availability breach:** Accidental or unauthorized loss of access to, or destruction of, personal data [edpb_breach_notification, para 17 (p.7)].

A breach may involve one, two, or all three of these categories simultaneously [edpb_breach_notification, para 18 (p.8)].
**Searches:** ['three kinds of personal data breach']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_breach_notification | location: paras 15-17 (p.7) | distance: 0.232
15. What should be clear is that a breach is a type of security incident. However, as indicated by Article 4(12), the GDPR only applies where there is a breach of pe
- 2] source: edpb_breach_notification | location: para 14 (p.7) | distance: 0.250
14. What is meant by “destruction” of personal data should be quite clear: this is where the data no longer exists, or no longer exists in a form that is of any use to th
- 3] source: edpb_breach_notification | location: paras 18-19 (p.8) | distance: 0.250
18. It should also be noted that, depending on the circumstances, a breach can concern confidentiality, integrity and availability of personal data at the same time, 
- 4] source: edpb_breach_notification | location: para 114 (p.25) | distance: 0.261
114. Whether the controller is aware that personal data is in the hands of people whose intentions are unknown or possibly malicious can have a bearing on the level of 
- 5] source: edpb_breach_notification | location: para 33 (p.11) | distance: 0.276
As the controller has been presented with clear evidence of a confidentiality breach then there can be no doubt that it ha s become “aware”. 3. A controller detects that

## q28 (single)
**Question:** Why does the type of data matter when a company judges how risky a breach is?
**Reference answer:** Usually the more sensitive the data, the higher the risk of harm, but other data already available about the person must also be considered. Disclosing a name and address is normally minor, but in some situations, such as an adoptive parent's address reaching the birth parent, it can be very severe.
**Agent answer:** The type and sensitivity of personal data are key factors in assessing risk because they directly influence the potential severity of harm to the individuals affected [edpb_breach_notification, para 107 (p.24)]. Generally, more sensitive data—such as health, financial, or identity information—carries a higher risk of damage, such as identity theft, fraud, or discrimination [edpb_breach_notification, paras 102, 108 (pp.23-24)]. Furthermore, the context matters: even seemingly innocuous data can become sensitive depending on what it reveals about an individual, and combinations of different data points often increase the risk compared to a single piece of data [edpb_breach_notification, paras 108-109 (p.24)].
**Searches:** ['factors to consider when assessing risk of a personal data breach type of data']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_breach_notification | location: paras 107-108 (p.24) | distance: 0.219
107. Of course, when assessing risk, a key factor is the type and sensitivity of personal data that has been compromised by the breach. Usually, the more sensitiv
- 2] source: edpb_breach_notification | location: paras 104-106 (p.23) | distance: 0.224
44 See WP Guidelines on DPIAs here: http://ec.europa.eu/newsroom/document.cfm?doc_id=44137 a b reach occurs. The controller should assess the specific circumstance
- 3] source: edpb_breach_notification | location: paras 102-103 (p.23) | distance: 0.238
102. As explained above, notification of a breach is required unless it is unlikely to result in a risk to the rights and freedoms of individuals, and the key trig
- 4] source: edpb_breach_notification | location: paras 117-118 (p.25) | distance: 0.240
117. The nature and role of the controller and its activities may affect the level of risk to individuals as a result of a breach. For example, a medical organisat
- 5] source: edpb_breach_notification | location: paras 109-110 (p.24) | distance: 0.243
109. Some types of personal data may seem at first relatively innocuous, however, what that data may reveal about the affected individual should be carefully consi

## q29 (single)
**Question:** Is a breach that affects only one person less serious than one that affects thousands?
**Reference answer:** Not necessarily. Generally more affected people means a bigger impact, but a breach can have a severe impact on even one person depending on the nature of the data and the context. The key is the likelihood and severity of the impact.
**Agent answer:** While a higher number of affected individuals generally increases the potential impact of a breach, a breach affecting only one person can still have a severe impact depending on the nature of the data and the context [edpb_breach_notification, para 118 (p.25)]. The assessment of risk should focus on the likelihood and severity of the impact on those affected, rather than solely on the number of individuals involved [edpb_breach_notification, para 118 (p.25)]. Other factors, such as the sensitivity of the data and the specific circumstances of the breach, are also critical to this assessment [edpb_breach_notification, paras 105, 107 (pp.23-24)].
**Searches:** ['factors to consider for severity of personal data breach']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_breach_notification | location: paras 104-106 (p.23) | distance: 0.240
44 See WP Guidelines on DPIAs here: http://ec.europa.eu/newsroom/document.cfm?doc_id=44137 a b reach occurs. The controller should assess the specific circumstanc
- 2] source: edpb_breach_notification | location: paras 107-108 (p.24) | distance: 0.242
107. Of course, when assessing risk, a key factor is the type and sensitivity of personal data that has been compromised by the breach. Usually, the more sensitive
- 3] source: edpb_breach_notification | location: paras 117-118 (p.25) | distance: 0.251
117. The nature and role of the controller and its activities may affect the level of risk to individuals as a result of a breach. For example, a medical organisat
- 4] source: edpb_breach_notification | location: paras 102-103 (p.23) | distance: 0.252
102. As explained above, notification of a breach is required unless it is unlikely to result in a risk to the rights and freedoms of individuals, and the key trig
- 5] source: edpb_breach_notification | location: paras 109-110 (p.24) | distance: 0.254
109. Some types of personal data may seem at first relatively innocuous, however, what that data may reveal about the affected individual should be carefully consi

## q30 (single)
**Question:** Can a service provider choose which software to use for a job without becoming a controller?
**Reference answer:** Yes. Non-essential means, such as the choice of software or hardware and detailed security measures, can be left to the processor. Essential means, such as which data, for how long, who has access and whose data, are for the controller to decide.
**Agent answer:** A processor may be allowed to choose the technical and organisational means to serve the controller's interests, provided they do not determine the purposes and essential means of the processing [edpb_controller_processor, front matter (p.1)]. While a controller must decide the "why" and "how" of the processing, practical aspects of implementation—referred to as "non-essential means"—can be left to the processor [edpb_controller_processor, front matter (p.1)]. However, if a processor goes beyond the controller's instructions and begins to determine its own purposes and means, it will be considered a controller for that processing [edpb_controller_processor, front matter (p.1)].
**Searches:** ['can a processor choose software without becoming a controller']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_controller_processor | location: front matter (p.1) | distance: 0.214
Two basic conditions for qualifying as processor exist: that it is a separate entity in relation to the controller and that it processes personal data on the contr
- 2] source: edpb_controller_processor | location: front matter (p.1) | distance: 0.221
Controller In principle, there is no limitation as to the type of entity that may assume the role of a controller but in practice it is usually the organisation as 
- 3] source: edpb_controller_processor | location: paras 75-77 (p.25) | distance: 0.223
75. Processing of personal data can involve multiple processors. For example, a co ntroller may itself choose to directly engage multiple processors, by involving d
- 4] source: edpb_controller_processor | location: para 30 (p.13) | distance: 0.224
30. In line with the factual approach, the word “determines” means that the entity that actually exerts a decisive influence on the purposes and means of the processing
- 5] source: edpb_controller_processor | location: para 191 (p.48) | distance: 0.225
Factors that indicate that you are the controller Factors that indicate that you are the processor • You obtain a benefit from, or have an interest in, the processing 

## q31 (single)
**Question:** Does the GDPR set specific duties for a company just because it receives data from another company?
**Reference answer:** No. The Regulation lays down no specific obligations for recipients and third parties. These are relative concepts, and a recipient or third party may at the same time be a controller or processor from another perspective.
**Agent answer:** The GDPR's duties for a company receiving data depend on whether it acts as a "processor" or a "controller." If a company processes data on behalf of another entity, it is a processor and must follow documented instructions, ensure confidentiality, implement security measures, and enter into a binding contract [gdpr, Article 28(3); edpb_controller_processor, para 114 (p.34)]. If the receiving company determines the purposes and means of processing independently, it is a separate controller and must fulfill its own obligations under the GDPR, such as providing information to data subjects [edpb_controller_processor, para 70 (p.24), para 5 (p.1)].
**Searches:** ['duties of a company receiving data from another company GDPR controller processor']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_controller_processor | location: paras 114-115 (p.34) | distance: 0.225
As regards the obligations of the controller, examples include the controller’s obligation to provide the processor with the data mentioned in the contract, to p
- 2] source: gdpr | location: Article 28(1)-(2) | distance: 0.229
Processor. 1. Where processing is to be carried out on behalf of a controller, the controller shall use only processors providing sufficient guarantees to implement appropriate technical
- 3] source: edpb_controller_processor | location: para 70 (p.24) | distance: 0.233
70. For example, the exchange of the same data or set of data between two entities without jointly determined purposes or jointly determined means of processing should 
- 4] source: gdpr | location: Article 28(3) | distance: 0.233
3. Processing by a processor shall be governed by a contract or other legal act under Union or Member State law, that is binding on the processor with regard to the controller and that sets 
- 5] source: edpb_controller_processor | location: front matter (p.1) | distance: 0.235
Any processing of personal data by a processor must be governed by a contract or other legal act which shall be in writing, including in electronic form, and be bin

## q32 (single)
**Question:** Do concepts from other fields of law, like intellectual property, decide who counts as a controller?
**Reference answer:** No. The concept of controller is autonomous and is interpreted mainly under EU data protection law. It should not be prejudiced by other concepts, such as the creator or right holder in intellectual property or competition law.
**Agent answer:** The provided corpus does not mention intellectual property law as a factor for determining controller status. Under the GDPR, a controller is defined as the natural or legal person, public authority, agency, or other body which, alone or jointly with others, determines the purposes and means of the processing of personal data [edpb_controller_processor, para 17 (p.10); gdpr, Article 26].
**Searches:** ['how to determine controller status GDPR intellectual property']
**Retrieved (first 250 characters of each passage):**
- [1] source: edpb_controller_processor | location: para 191 (p.48) | distance: 0.227
Factors that indicate that you are the controller Factors that indicate that you are the processor • You obtain a benefit from, or have an interest in, the processing
- 2] source: edpb_controller_processor | location: para 191 (p.48) | distance: 0.236
191. It should be recalled that data protection authorities are not bound by the terms of the arrangement whether on the issue of the qualification of the parties as j
- 3] source: edpb_controller_processor | location: para 191 (p.48) | distance: 0.237
Does more than one party have a decisive influence over whether and how the processing takes place – either by a common decision or by converging decisions that comple
- 4] source: edpb_controller_processor | location: para 17 (p.10) | distance: 0.238
17. The first building block relates to the type of entity that can be a controller. Under the GDPR, a controller can be “a natural or legal person, public authority, a
- 5] source: gdpr | location: Article 26 | distance: 0.239
Joint controllers. 1. Where two or more controllers jointly determine the purposes and means of processing, they shall be joint controllers. They shall in a transparent manner determine their r
