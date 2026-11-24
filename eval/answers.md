# Agent answers (no verdicts here: grade these first, in eval/human_labels.csv)

## q01 (single)

**Question:** What is the maximum administrative fine for infringing the prohibitions of AI practices in Article 5?

**Reference:** Up to EUR 35,000,000 or, for an undertaking, up to 7% of total worldwide annual turnover of the preceding financial year, whichever is higher.

**Answer:**

For providers and deployers generally, infringing the prohibitions in Article 5 is subject to administrative fines of up to EUR 35 000 000 or, if the offender is an undertaking, up to 7% of its total worldwide annual turnover for the preceding financial year, whichever is higher [ai_act_consolidated_2026-07-27 | Article 99(3)]. For EU institutions, bodies, offices, and agencies, such violations are subject to administrative fines of up to EUR 1 500 000 [ai_act_consolidated_2026-07-27 | Article 100(2)]. For SMEs (including start-ups), each fine is capped at whichever amount or percentage is lower [ai_act_consolidated_2026-07-27 | Article 99(6)].

This should be checked by a legal professional before making compliance decisions for a real system.

## q02 (single)

**Question:** How are fines calculated for SMEs, including start-ups?

**Reference:** For SMEs, including start-ups, each fine is up to the percentages or amounts above, whichever of them is lower.

**Answer:**

For SMEs, including start-ups, administrative fines are capped at whichever is the **lower** amount: either the standard percentage/absolute maximum fine set out in the regulation (paragraphs 3, 4, and 5 of Article 99) or the proportionate limits established for their size. Additionally, Member States are required to take the interests of SMEs, start-ups, and their economic viability into account when imposing penalties [ai_act_consolidated_2026-07-27 | Article 99(1), (6)].

*This matter should be reviewed by a legal professional before making operational or compliance decisions.*

## q03 (single)

**Question:** What does the AI literacy obligation require of providers and deployers?

**Reference:** They must take measures to ensure, to their best extent, a sufficient level of AI literacy of their staff and others operating AI systems on their behalf. It does not require guaranteeing any specific level of AI literacy of any individual.

**Answer:**

Providers and deployers of AI systems must take measures to support the development of AI literacy for their staff and other persons dealing with the operation and use of AI systems on their behalf `[ai_act_consolidated_2026-07-27 | Article 4(1)]`. 

When taking these measures, providers and deployers must take into account:
* The technical knowledge, experience, education, and training of the persons `[ai_act_consolidated_2026-07-27 | Article 4(1)]`;
* The context in which the AI systems are to be used `[ai_act_consolidated_2026-07-27 | Article 4(1)]`; and
* The persons or groups of persons on whom the AI systems are to be used `[ai_act_consolidated_2026-07-27 | Article 4(1)]`.

This obligation does not require providers or deployers to guarantee any specific level of AI literacy for any individual `[ai_act_consolidated_2026-07-27 | Article 4(1)]`.

*For a decision about a real system, this should be checked by a legal professional.*

## q04 (single)

**Question:** Is it prohibited to infer the emotions of employees at work?

**Reference:** Yes. Article 5(1)(f) prohibits AI systems that infer emotions of a natural person in the areas of workplace and education institutions, except where intended for medical or safety reasons.

**Answer:**

Yes, it is prohibited to place on the market, put into service for that specific purpose, or use AI systems to infer the emotions of employees at the workplace, except where the use is intended for medical or safety reasons [guidelines_prohibited_practices_C2025-5052 | paragraph (241)]. According to the Commission guidelines, this prohibition applies to both providers and deployers [guidelines_prohibited_practices_C2025-5052 | paragraph (243)] and covers a broad interpretation of the workplace, including recruitment stages and virtual or physical spaces where tasks are performed [guidelines_prohibited_practices_C2025-5052 | paragraph (254)].

For a decision about a real system, this should be checked by a legal professional.

[guidelines_prohibited_practices_C2025-5052 | paragraph (241)]
[guidelines_prohibited_practices_C2025-5052 | paragraph (243)]
[guidelines_prohibited_practices_C2025-5052 | paragraph (254)]

## q05 (single)

**Question:** In which situations may real-time remote biometric identification be used in publicly accessible spaces for law enforcement?

**Reference:** Only for three objectives: targeted search for victims of abduction, trafficking or sexual exploitation and missing persons; prevention of a specific, substantial and imminent threat to life or physical safety or a terrorist attack; localisation or identification of a suspect of an Annex II offence punishable by at least four years.

**Answer:**

The use of "real-time" remote biometric identification systems in publicly accessible spaces for law enforcement is prohibited unless it is strictly necessary for one of the following three objectives:

1. The targeted search for specific victims of abduction, trafficking in human beings, or sexual exploitation of human beings, as well as the search for missing persons [ai_act_consolidated_2026-07-27 | Article 5(1)(h)(i)];
2. The prevention of a specific, substantial, and imminent threat to the life or physical safety of natural persons, or a genuine and present or genuine and foreseeable threat of a terrorist attack [ai_act_consolidated_2026-07-27 | Article 5(1)(h)(ii)];
3. The localisation or identification of a person suspected of having committed a criminal offence, for the purpose of conducting a criminal investigation or prosecution or executing a criminal penalty for offences referred to in Annex II and punishable in the Member State concerned by a custodial sentence or a detention order for a maximum period of at least four years [ai_act_consolidated_2026-07-27 | Article 5(1)(h)(iii)].

Any such use also requires domestic Member State legislation authorising it, prior authorisation from a judicial or independent administrative authority (except in duly justified urgent cases), and adherence to strict fundamental rights, proportionality, and safeguard conditions [ai_act_consolidated_2026-07-27 | Article 5(2)-(3), guidelines_prohibited_practices_C2025-5052 | paragraph (326)]. 

*Because compliance depends heavily on specific facts, national laws, and individual circumstances, this assessment should be verified by a legal professional.*

## q06 (single)

**Question:** At what training compute is a general-purpose AI model presumed to have high-impact capabilities?

**Reference:** When the cumulative compute used for training, measured in floating point operations, is greater than 10^25 FLOPs.

**Answer:**

A general-purpose AI model is presumed to have high-impact capabilities when the cumulative amount of computation used for its training, measured in floating point operations (FLOPs), is greater than $10^{25}$.

[ai_act_consolidated_2026-07-27 | Article 51(2)]

*This should be checked by a legal professional for any specific application.*

## q07 (single)

**Question:** Which employment-related uses of AI are listed as high-risk?

**Reference:** Annex III point 4: recruitment and selection, decisions on terms of work, promotion and termination, task allocation based on behaviour or personal traits, and monitoring and evaluating performance.

**Answer:**

The employment-related uses of AI listed as high-risk under Annex III of the EU AI Act are:

1. **Recruitment and selection:** AI systems intended to be used for the recruitment or selection of natural persons, including placing targeted job advertisements, analysing and filtering job applications, and evaluating candidates `[ai_act_consolidated_2026-07-27 | Annex III(4)(a)]`.
2. **Work-related decisions, task allocation, and monitoring:** AI systems intended to be used to:
   - Make decisions affecting the terms of work-related relationships, promotion, or termination of work-related contractual relationships `[ai_act_consolidated_2026-07-27 | Annex III(4)(b)]`.
   - Allocate tasks based on individual behaviour or personal traits or characteristics `[ai_act_consolidated_2026-07-27 | Annex III(4)(b)]`.
   - Monitor and evaluate the performance and behaviour of persons in such relationships `[ai_act_consolidated_2026-07-27 | Annex III(4)(b)]`.

*This should be checked by a legal professional to determine whether a specific system falls within these definitions.*

## q08 (single)

**Question:** Which deployers must carry out a fundamental rights impact assessment?

**Reference:** Deployers that are bodies governed by public law or private entities providing public services, and deployers of certain Annex III systems (point 5(b) and (c)); Annex III point 2 is excluded.

**Answer:**

Prior to deploying certain high-risk AI systems, a fundamental rights impact assessment must be carried out by:
1. Deployers that are **bodies governed by public law** or **private entities providing public services**, when deploying high-risk AI systems referred to in Article 6(2), with the exception of those intended to be used in the area listed in point 2 of Annex III [ai_act_consolidated_2026-07-27 | Article 27(1)].
2. Deployers of high-risk AI systems referred to in **points 5(b) and (c) of Annex III** [ai_act_consolidated_2026-07-27 | Article 27(1)].
3. Deployers of **real-time remote biometric identification (RBI)** systems meeting conditions to benefit from exceptions under Article 5(1)(h) [guidelines_prohibited_practices_C2025-5052 | paragraphs (369)–(371)].

This should be verified by a legal professional for any specific system.

## q09 (single)

**Question:** How does the AI Act define an emotion recognition system?

**Reference:** Article 3(39): an AI system for the purpose of identifying or inferring emotions or intentions of natural persons on the basis of their biometric data.

**Answer:**

The AI Act defines an "emotion recognition system" as an AI system for the purpose of identifying or inferring emotions or intentions of natural persons on the basis of their biometric data `[ai_act_consolidated_2026-07-27 | Article 3(39)]`. 

This system should be checked by a legal professional to determine its exact legal status and compliance requirements.

## q10 (single)

**Question:** What must deployers of emotion recognition systems tell the people exposed to them?

**Reference:** Article 50(3): deployers must inform the natural persons exposed to the operation of the system.

**Answer:**

Deployers of an emotion recognition system must inform the natural persons exposed to it of the system's operation [ai_act_consolidated_2026-07-27 | Article 50(3)]. They must also process personal data in accordance with applicable EU data protection regulations and directives [ai_act_consolidated_2026-07-27 | Article 50(3)]. 

This information obligation does not apply to emotion recognition systems that are permitted by law to detect, prevent, or investigate criminal offences, provided they are subject to appropriate safeguards for third-party rights and freedoms and comply with Union law [ai_act_consolidated_2026-07-27 | Article 50(3)].

*Note: For a decision about a real system, this should be checked by a legal professional.*

## q11 (single)

**Question:** From what date does the AI Act apply?

**Reference:** The Act applies from 2 August 2026. Chapters I and II apply from 2 February 2025, except Article 5(1)(ba), (bb), (1a) and (1b), which apply from 2 December 2026.

**Answer:**

The AI Act generally applies from 2 August 2026, but different provisions apply at different times [ai_act_consolidated_2026-07-27 | Article 113]:

* Chapters I and II (including definitions and prohibited AI practices under Article 5) apply from 2 February 2025 [ai_act_consolidated_2026-07-27 | Article 113, guidelines_ai_system_definition_C2025-5053 | paragraphs (1)–(5)], with specific exceptions applying from 2 December 2026 [ai_act_consolidated_2026-07-27 | Article 113].
* Certain governance, penalty, and competent authority provisions (such as Chapter III Section 4, Chapter V, Chapter VII, Chapter XII, and Article 78) apply from 2 August 2025 [ai_act_consolidated_2026-07-27 | Article 113].
* High-risk AI system rules (Chapter III, Sections 1, 2, and 3) apply from 2 December 2027 for systems under Article 6(2) and Annex III, and from 2 August 2028 for systems under Article 6(1) and Annex I [ai_act_consolidated_2026-07-27 | Article 113].

*This should be checked by a legal professional for any specific use case.*

## q12 (single)

**Question:** Within what deadline must a serious incident be reported?

**Reference:** Immediately after the causal link is established and in any event not later than 15 days after the provider becomes aware of the serious incident.

**Answer:**

For high-risk AI systems, a serious incident must be reported:
* **General deadline:** Immediately after establishing a causal link (or reasonable likelihood) between the AI system and the incident, and **not later than 15 days** after the provider or deployer becomes aware of it [ai_act_consolidated_2026-07-27 | Article 73(2)].
* **Widespread infringement or specific critical incidents:** Immediately, and **not later than 2 days** after becoming aware of the incident [ai_act_consolidated_2026-07-27 | Article 73(3)].
* **In the event of a person's death:** Immediately after establishing or suspecting a causal relationship, and **not later than 10 days** after becoming aware of the incident [ai_act_consolidated_2026-07-27 | Article 73(4)].

For a decision about a real system, this should be checked by a legal professional.

## q13 (single)

**Question:** Must users be told they are interacting with an AI system such as a chatbot?

**Reference:** Yes. Article 50(1): providers must design interactive AI systems so that people are informed they are interacting with AI, unless this is obvious.

**Answer:**

Yes. Providers must ensure that AI systems intended to interact directly with natural persons are designed and developed so that the persons concerned are informed they are interacting with an AI system, unless this is obvious from the point of view of a reasonably well-informed, observant, and circumspect person given the circumstances and context of use. This information must be provided in a clear and distinguishable manner at the latest at the time of the first interaction or exposure.

Exemptions apply to AI systems authorised by law to detect, prevent, investigate, or prosecute criminal offences (unless available for the public to report a crime).

[ai_act_consolidated_2026-07-27 | Article 50(1)]
[ai_act_consolidated_2026-07-27 | Article 50(5)]

*This should be checked by a legal professional for your specific system and context.*

## q14 (single)

**Question:** Is adaptiveness a required element of the AI system definition?

**Reference:** No. Adaptiveness is facultative: the definition says the system 'may' exhibit adaptiveness after deployment.

**Answer:**

No, adaptiveness is not a required element of the AI system definition. According to the Commission guidelines, the use of the term "may" in relation to the adaptiveness element indicates that a system may, but does not necessarily have to, possess adaptiveness or self-learning capabilities after deployment to constitute an AI system, making it a facultative rather than a decisive condition `[guidelines_ai_system_definition_C2025-5053 | paragraphs (22)–(23)]`.

*Note: This interpretation is set out in Commission guidelines and should be checked by a legal professional for any real-world compliance decision.*

## q15 (single)

**Question:** What are the elements of the AI system definition according to the Commission guidelines?

**Reference:** Seven elements: machine-based system; designed to operate with varying levels of autonomy; may exhibit adaptiveness; explicit or implicit objectives; infers from input how to generate outputs; outputs such as predictions, content, recommendations or decisions; influence on physical or virtual environments.

**Answer:**

According to the Commission guidelines, the definition of an AI system comprises seven main elements:
1. A machine-based system [guidelines_ai_system_definition_C2025-5053 | paragraphs (8)–(10)].
2. Designed to operate with varying levels of autonomy [guidelines_ai_system_definition_C2025-5053 | paragraphs (8)–(10)].
3. That may exhibit adaptiveness after deployment [guidelines_ai_system_definition_C2025-5053 | paragraphs (8)–(10)].
4. That operates for explicit or implicit objectives [guidelines_ai_system_definition_C2025-5053 | paragraphs (8)–(10)].
5. That infers, from the input it receives, how to generate outputs [guidelines_ai_system_definition_C2025-5053 | paragraphs (8)–(10)].
6. Such as predictions, content, recommendations, or decisions [guidelines_ai_system_definition_C2025-5053 | paragraphs (8)–(10)].
7. That can influence physical or virtual environments [guidelines_ai_system_definition_C2025-5053 | paragraphs (8)–(10)].

These elements should be understood as interpreted by the Commission guidelines rather than strict legislative provisions, and any real-world assessment of a system should be verified by a legal professional.

## q16 (single)

**Question:** Are systems based on linear or logistic regression AI systems under the guidelines?

**Reference:** Systems that optimise using such methods but do not transcend basic data processing fall outside the AI system definition.

**Answer:**

The Commission guidelines on the definition of an AI system state that systems used to improve mathematical optimisation or to accelerate and approximate traditional, well-established optimisation methods, such as linear or logistic regression methods, fall outside the scope of the AI system definition because they do not transcend basic data processing.

[guidelines_ai_system_definition_C2025-5053 | paragraphs (40)–(43)]

*This determination should be verified by a legal professional for any specific real-world system.*

## q17 (single)

**Question:** Which practice does Article 5(1)(e) prohibit regarding facial images?

**Reference:** Untargeted scraping of facial images from the internet or CCTV footage to create or expand facial recognition databases.

**Answer:**

Article 5(1)(e) AI Act prohibits the placing on the market, putting into service for this specific purpose, or the use of AI systems that create or expand facial recognition databases through the untargeted scraping of facial images from the Internet or CCTV footage [guidelines_prohibited_practices_C2025-5052 | paragraph (222)].

*For a decision about a real system, this should be checked by a legal professional.*

## q18 (single)

**Question:** What do the prohibited-practices guidelines say about the fines for breaching Article 5?

**Reference:** Fines up to EUR 35 million or 7% of worldwide annual turnover; for EU institutions, bodies and agencies up to EUR 1.5 million.

**Answer:**

The Commission guidelines on prohibited AI practices state that breaches of Article 5 are treated as the most severe infringements under the AI Act's tiered penalty approach [guidelines_prohibited_practices_C2025-5052 | paragraphs (55)–(57)]. Providers and deployers can be fined up to EUR 35 million or, for undertakings, up to 7% of their total worldwide annual turnover for the preceding financial year, whichever is higher [guidelines_prohibited_practices_C2025-5052 | paragraphs (55)–(57)]. EU institutions, bodies, and agencies that violate the prohibitions may face administrative fines of up to EUR 1.5 million [guidelines_prohibited_practices_C2025-5052 | paragraphs (55)–(57)]. The guidelines also note that while the prohibitions applied directly from 2 February 2025, the provisions on penalties did not become applicable until 2 August 2025 [guidelines_prohibited_practices_C2025-5052 | paragraphs (429)–(431)].

*This should be checked by a legal professional for any specific deployment decision.*

## q19 (single)

**Question:** What interests does the social scoring prohibition protect?

**Reference:** Human dignity, non-discrimination, data protection and related fundamental rights and values.

**Answer:**

As stated in the Commission guidelines on prohibited AI practices, the social scoring prohibition aims to protect:
* The right to human dignity [guidelines_prohibited_practices_C2025-5052 | paragraph (148)].
* Fundamental rights, including the right to non-discrimination and equality, the right to data protection, and the right to private and family life, as well as relevant social and economic rights [guidelines_prohibited_practices_C2025-5052 | paragraph (148)].
* Union values of democracy, equality (including equal access to public and private services), and justice [guidelines_prohibited_practices_C2025-5052 | paragraph (148)].

*For a decision about a real system, this should be checked by a legal professional.*

## q20 (single)

**Question:** How do the guidelines treat emotion recognition in the workplace?

**Reference:** They explain the Article 5(1)(f) prohibition on emotion recognition in the workplace and its medical and safety exceptions.

**Answer:**

The Commission guidelines state that Article 5(1)(f) of the AI Act prohibits AI systems from inferring the emotions of a natural person in the areas of the workplace and education institutions, except where the use is intended for medical or safety reasons [guidelines_prohibited_practices_C2025-5052 | paragraph (239)]. 

The guidelines interpret the "workplace" broadly to include virtual and physical spaces, self-employment, and candidates during selection and hiring [guidelines_prohibited_practices_C2025-5052 | paragraph (254)]. Examples of prohibited practices include call centres using webcams and voice recognition to track employee anger [guidelines_prohibited_practices_C2025-5052 | paragraph (254)], assessing employees' wellbeing, motivation levels, or job satisfaction [guidelines_prohibited_practices_C2025-5052 | paragraph (263)], and measuring anxiety or boredom unless elevated stress or lack of concentration poses a specific danger (such as when deploying dangerous machines or dealing with dangerous chemicals) [guidelines_prohibited_practices_C2025-5052 | paragraph (263)]. 

Permitted exceptions include emotion recognition deployed for medical reasons (e.g., to assist employees with autism) [guidelines_prohibited_practices_C2025-5052 | paragraph (263)] or for personal training purposes if results are not shared with HR and do not impact assessment or promotion [guidelines_prohibited_practices_C2025-5052 | paragraph (254)]. Employers should only deploy these systems for medical and safety reasons in case of an explicit need, and data collected may not be used for any other purpose [guidelines_prohibited_practices_C2025-5052 | paragraph (260)–(262)].

This should be checked by a legal professional for any specific system.

## q21 (single)

**Question:** What fine applies to a provider that breaches its obligations under the Act (not Article 5)?

**Reference:** Article 99(4): up to EUR 15,000,000 or 3% of total worldwide annual turnover, whichever is higher.

**Answer:**

Non-compliance with provider obligations under Article 16 (other than those laid down in Article 5) is subject to administrative fines of up to EUR 15 000 000, or, if the offender is an undertaking, up to 3% of its total worldwide annual turnover for the preceding financial year, whichever is higher [ai_act_consolidated_2026-07-27 | Article 99(4)]. 

For SMEs including start-ups and SMCs, the fine is capped at the lower of the percentages/amounts or the limits specified for them in the regulation [ai_act_consolidated_2026-07-27 | Article 99(6), (6a)].

*This should be checked by a legal professional for any specific application.*

## q22 (multi)

**Question:** Is social scoring prohibited, and what fine can result?

**Reference:** Yes, Article 5(1)(c) prohibits social scoring; infringement can lead to a fine of up to EUR 35,000,000 or 7% of worldwide turnover, whichever is higher (Article 99).

**Answer:**

Yes, social scoring practices that meet the criteria of Article 5(1)(c) are prohibited [guidelines_prohibited_practices_C2025-5052 | paragraph (148)].

Non-compliance with this prohibition is subject to administrative fines of up to EUR 35 000 000 or, if the offender is an undertaking, up to 7% of its total worldwide annual turnover for the preceding financial year, whichever is higher [ai_act_consolidated_2026-07-27 | Article 99(3)].

*This assessment should be checked by a legal professional before making decisions about a real system.*

## q23 (multi)

**Question:** How does the Act define an AI system and does it require adaptiveness?

**Reference:** Article 3 defines the AI system; the guidelines clarify that adaptiveness is facultative.

**Answer:**

The AI Act defines an AI system as:
> “a machine-based system that is designed to operate with varying levels of autonomy and that may exhibit adaptiveness after deployment, and that, for explicit or implicit objectives, infers, from the input it receives, how to generate outputs such as predictions, content, recommendations, or decisions that can influence physical or virtual environments” [guidelines_ai_system_definition_C2025-5053 | paragraphs (8)–(10)].

No, adaptiveness is **not** required [guidelines_ai_system_definition_C2025-5053 | paragraphs (22)–(23)]. The Commission guidelines state that because the definition uses the word "may" regarding adaptiveness after deployment, a system can qualify as an AI system whether or not it possesses self-learning capabilities after deployment [guidelines_ai_system_definition_C2025-5053 | paragraphs (22)–(23)]. 

For a decision about a real system, this should be checked by a legal professional.

## q24 (multi)

**Question:** Is emotion recognition at work banned and what transparency applies elsewhere?

**Reference:** Banned in workplace and education except medical or safety reasons (Article 5(1)(f)); otherwise deployers must inform exposed persons (Article 50(3)).

**Answer:**

Emotion recognition at the workplace is **banned**, subject to a narrow exception for medical or safety reasons [guidelines_prohibited_practices_C2025-5052 | paragraph (239)]. Under Article 5(1)(f) of the AI Act, placing on the market, putting into service, or using AI systems to infer emotions of natural persons in the areas of the workplace and educational institutions is prohibited [guidelines_prohibited_practices_C2025-5052 | paragraph (241)].

Where emotion recognition systems are permitted elsewhere (such as outside the workplace and education, or when deployed for allowed medical or safety reasons), deployers must inform the natural persons exposed to the system of its operation [ai_act_consolidated_2026-07-27 | Article 50(3)].

*This should be checked by a legal professional for any specific deployment.*

## q25 (multi)

**Question:** What fines apply to prohibited practices and what is different for EU institutions?

**Reference:** Up to EUR 35M or 7% turnover under Article 99; EU institutions up to EUR 1.5M per the guidelines.

**Answer:**

For undertakings and other standard operators, non-compliance with the prohibition of AI practices under Article 5 is subject to administrative fines of up to EUR 35,000,000 or, if the offender is an undertaking, up to 7% of its total worldwide annual turnover for the preceding financial year, whichever is higher `[ai_act_consolidated_2026-07-27 | Article 99(3)]`.

For EU institutions, bodies, offices, and agencies, the rules differ: they may be fined up to EUR 1,500,000 for non-compliance with the prohibited practices, and these fines are imposed by the European Data Protection Supervisor `[ai_act_consolidated_2026-07-27 | Article 100(1)–(2)]`, `[guidelines_prohibited_practices_C2025-5052 | paragraphs (55)–(57)]`.

*This should be checked by a legal professional for any specific application.*

## q26 (multi)

**Question:** What new prohibitions on intimate or abuse imagery exist and when do they apply?

**Reference:** Article 5(1)(ba) and (bb) prohibit non-consensual realistic intimate imagery and child sexual abuse material; they apply from 2 December 2026.

**Answer:**

The EU AI Act prohibits two categories of AI practices concerning intimate and abuse imagery:

1. **Intimate imagery:** The placing on the market, putting into service, or use of an AI system that generates or manipulates realistic images, videos, audio, or similar material of an identifiable natural person's intimate parts, or of an identifiable natural person engaged in sexually explicit activities, without that person's freely-given, specific, informed, unambiguous, and explicit consent [ai_act_consolidated_2026-07-27 | Article 5(1)(ba)].
2. **Abuse imagery:** The placing on the market, putting into service, or use of an AI system that generates or manipulates material or performance within the meaning of Article 2, points (c) and (e), of Directive 2011/93/EU (related to child sexual abuse material), except where a "without right" defence applies under national law [ai_act_consolidated_2026-07-27 | Article 5(1)(bb)].

**Application conditions and scope:**
* For providers, the prohibition applies when the generation or manipulation is the intended purpose, or when the system's design, training, architecture, capabilities, or user-facing functionalities make it a reasonably foreseeable and reproducible outcome (without requiring significant technical modification) and the system lacks reasonable and adequate technical safety measures and safeguards to reliably prevent and correct misuse [ai_act_consolidated_2026-07-27 | Article 5(1a)(a)].
* For deployers, the prohibition applies when the system is used for the purpose of generating or manipulating such material or performance [ai_act_consolidated_2026-07-27 | Article 5(1a)(b)].
* Manipulation of material that does not increase the exposure of any depicted intimate parts or alter the nature of any depicted sexually explicit activities does not constitute manipulation under point (ba) [ai_act_consolidated_2026-07-27 | Article 5(1b)].

**When they apply:**
These specific prohibitions apply from **2 December 2026** [ai_act_consolidated_2026-07-27 | Article 113(3)(a)]. 

*This matter should be checked by a legal professional for compliance with your specific system features.*

## q27 (multi)

**Question:** Which offences justify real-time remote biometric identification for suspects?

**Reference:** Suspects of Annex II offences (e.g. terrorism, trafficking in human beings, sexual exploitation of children) punishable by at least four years (Article 5(1)(h)).

**Answer:**

Real-time remote biometric identification (RBI) of suspects in publicly accessible spaces for law enforcement purposes is only justified for specific serious crimes listed in Annex II of the AI Act, provided that the offence is punishable in the Member State concerned by a custodial sentence or a detention order for a maximum period of at least four years [guidelines_prohibited_practices_C2025-5052 | paragraphs (348)–(349)].

According to the Commission guidelines, those offences are:
- terrorism [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- trafficking in human beings [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- sexual exploitation of children, and child pornography [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- illicit trafficking in narcotic drugs or psychotropic substances [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- illicit trafficking in weapons, munitions or explosives [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- murder, grievous bodily injury [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- illicit trade in human organs or tissue [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- illicit trafficking in nuclear or radioactive materials [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- kidnapping, illegal restraint or hostage-taking [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- crimes within the jurisdiction of the International Criminal Court [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- unlawful seizure of aircraft or ships [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- rape [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- environmental crime [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- organised or armed robbery [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- sabotage [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]
- participation in a criminal organisation involved in one or more of the offences listed above [guidelines_prohibited_practices_C2025-5052 | paragraph (349)]

This application should be checked by a legal professional for any specific deployment.

## q28 (multi)

**Question:** When is an Annex III system high-risk?

**Reference:** Article 6(2): systems referred to in Annex III are high-risk; Annex III lists the areas.

**Answer:**

An AI system referred to in Annex III is considered high-risk unless it does not pose a significant risk of harm to the health, safety, or fundamental rights of natural persons (including by not materially influencing decision-making outcomes). 

Specifically, an Annex III system is **not** considered high-risk if it fulfills any of the following conditions:
* It is intended to perform a narrow procedural task [cite as [ai_act_consolidated_2026-07-27 | Article 6(3)]].
* It is intended to improve the result of a previously completed human activity [cite as [ai_act_consolidated_2026-07-27 | Article 6(3)]].
* It is intended to detect decision-making patterns or deviations from prior decision-making patterns and is not meant to replace or influence the previously completed human assessment without proper human review [cite as [ai_act_consolidated_2026-07-27 | Article 6(3)]].
* It is intended to perform a preparatory task to an assessment relevant for the purposes of the use cases listed in Annex III [cite as [ai_act_consolidated_2026-07-27 | Article 6(3)]].

However, notwithstanding the above exemptions, an Annex III system **shall always be considered high-risk** if it performs profiling of natural persons [cite as [ai_act_consolidated_2026-07-27 | Article 6(3)]]. A provider concluding that an Annex III system is not high-risk must document that assessment before placing it on the market or putting it into service and register it accordingly [cite as [ai_act_consolidated_2026-07-27 | Article 6(4)]].

*This assessment should be verified by a legal professional.*

## q29 (multi)

**Question:** How can a general-purpose AI model be designated as having systemic risk by the Commission?

**Reference:** By Commission decision under Article 51(1)(b) based on the Annex XIII criteria such as parameters, dataset size and quality, and compute.

**Answer:**

A general-purpose AI model can be designated as having systemic risk by the Commission in the following ways:

* **Ex officio or following a qualified alert:** The Commission may designate a model as presenting systemic risks on its own initiative (*ex officio*) or following a qualified alert from the scientific panel, based on the evaluation criteria set out in Annex XIII (such as parameters, training compute, data set size, modalities, benchmarks, and market reach) [ai_act_consolidated_2026-07-27 | Article 51(1)(b), Article 52(4), Annex XIII].
* **Failure to notify or failure to rebut classification:** A provider must notify the Commission when its model meets the high-impact capability threshold (such as training compute greater than $10^{25}$ floating point operations). If the Commission becomes aware of a model presenting systemic risks that was not notified, or if a provider submits arguments to claim its model does not present systemic risks due to specific characteristics and the Commission rejects those arguments, the model is considered a general-purpose AI model with systemic risk [ai_act_consolidated_2026-07-27 | Article 51(2), Article 52(1)–(3)].

This should be verified by a legal professional for any specific system.

## q30 (multi)

**Question:** Is a linear regression model an AI system under the Act?

**Reference:** Article 3 gives the definition; the guidelines say simple regression optimisation that does not transcend basic data processing falls outside it.

**Answer:**

According to the Commission guidelines on the definition of an AI system, systems used to improve mathematical optimisation or to accelerate and approximate traditional, well-established optimisation methods, such as **linear** or logistic regression methods, fall outside the scope of the AI system definition. This is because, while those models have the capacity to infer, they do not transcend "basic data processing" due to their limited capacity to analyse patterns and adjust autonomously their output.

Citation: [guidelines_ai_system_definition_C2025-5053 | paragraphs (40)–(43)] (Commission guidelines)

*Note: This interpretation should be checked by a legal professional for any real-world compliance decision.*

## q31 (unanswerable)

**Question:** At what training compute is a general-purpose AI model classified as general-purpose under the Commission guidelines (10^23 FLOPs)?

**Reference:** The indexed documents do not cover this. The assistant should say it cannot answer from the corpus and must not invent an answer.

**Answer:**

The indexed documents do not state that a general-purpose AI model is classified at a training compute threshold of $10^{23}$ FLOPs. 

Under the AI Act, general-purpose AI models are defined by their display of significant generality and capability to competently perform a wide range of distinct tasks [ai_act_consolidated_2026-07-27 | Article 3(63)]. A general-purpose AI model is specifically classified as having **systemic risk** (based on a presumption of high-impact capabilities) when the cumulative amount of computation used for its training measured in floating-point operations is greater than **$10^{25}$** FLOPs [ai_act_consolidated_2026-07-27 | Article 51(1)–(2)].

*This assessment should be checked by a legal professional before making compliance decisions.*

## q32 (unanswerable)

**Question:** Which Spanish authority supervises the AI Act and what is its address?

**Reference:** The indexed documents do not cover this. The assistant should say it cannot answer from the corpus and must not invent an answer.

**Answer:**

The indexed documents do not cover the identity or address of the specific Spanish authority supervising the AI Act. 

The AI Act requires each Member State to establish or designate at least one notifying authority and at least one market surveillance authority (acting as a single point of contact) and to communicate their identities and contact information to the European Commission [ai_act_consolidated_2026-07-27 | Article 70(1)–(2)].

*This assessment should be verified by a legal professional.*

## q33 (unanswerable)

**Question:** What is the number of the harmonised standard for quality management systems under the AI Act?

**Reference:** The indexed documents do not cover this. The assistant should say it cannot answer from the corpus and must not invent an answer.

**Answer:**

The indexed documents do not specify a standard number for quality management systems under the AI Act; they only reference the general provisions for harmonised standards and quality management systems for high-risk AI system providers (such as Article 17 and Article 40) [ai_act_consolidated_2026-07-27 | Article 17(1), ai_act_consolidated_2026-07-27 | Article 40(1)]. 

*This assessment should be checked by a legal professional before making compliance decisions.*

## q34 (unanswerable)

**Question:** What examples does the Commission's Article 50 guidance give for labelling deep fakes?

**Reference:** The indexed documents do not cover this. The assistant should say it cannot answer from the corpus and must not invent an answer.

**Answer:**

The indexed guidelines on prohibited AI practices do not give specific examples illustrating the labelling of deep fakes under Article 50(4) of the AI Act; they only reference the general role of visible disclosure as a mitigating measure to reduce deception and harmful distorting effects on individuals [guidelines_prohibited_practices_C2025-5052 | paragraph (71)]. 

*(Note: This matter should be verified by a legal professional for any real-world compliance assessment.)*

## q35 (unanswerable)

**Question:** What GDPR fine applies to unlawful biometric processing?

**Reference:** The indexed documents do not cover this. The assistant should say it cannot answer from the corpus and must not invent an answer.

**Answer:**

The indexed documents do not cover the specific GDPR fines for unlawful biometric processing, as the GDPR falls outside the scope of the provided EU AI Act corpus. 

*(This question should be checked by a legal professional with respect to Regulation (EU) 2016/679).*

## q36 (unanswerable)

**Question:** What fines does the Digital Services Act impose on platforms?

**Reference:** The indexed documents do not cover this. The assistant should say it cannot answer from the corpus and must not invent an answer.

**Answer:**

The indexed documents do not cover the fines imposed by the Digital Services Act; they only cover the rules, prohibitions, and penalties established under Regulation (EU) 2024/1689 (the EU AI Act) and mention that the Digital Services Act regulates online intermediary services and dark patterns [guidelines_prohibited_practices_C2025-5052 | paragraph (139)]. 

*This is a general summary of the indexed legal corpus; a legal professional should review any specific compliance or enforcement situation.*

## q37 (unanswerable)

**Question:** Has the Commission published draft guidance on high-risk classification under Article 6(3)?

**Reference:** The indexed documents do not cover this. The assistant should say it cannot answer from the corpus and must not invent an answer.

**Answer:**

The indexed documents do not contain the text of draft or finalized guidance on high-risk classification under Article 6(3). They state only that the Commission is required to provide guidelines specifying the practical implementation of Article 6, including a comprehensive list of practical examples of high-risk and not high-risk AI system use cases, after consulting the European Artificial Intelligence Board [ai_act_consolidated_2026-07-27 | Article 6(5)].

*This response should be checked by a legal professional before being used for compliance decisions.*

## q38 (unanswerable)

**Question:** Has any company already been fined under Article 5 of the AI Act?

**Reference:** The indexed documents do not cover this. The assistant should say it cannot answer from the corpus and must not invent an answer.

**Answer:**

The indexed documents do not cover whether any company has actually been fined. 

The indexed texts do state that non-compliance with the prohibitions in Article 5 is subject to administrative fines of up to EUR 35,000,000 or, for undertakings, up to 7% of total worldwide annual turnover for the preceding financial year [ai_act_consolidated_2026-07-27 | Article 99(3)]. The provisions on penalties for non-compliance with Article 5 became applicable on 2 August 2025 [guidelines_prohibited_practices_C2025-5052 | paragraphs (429)–(431)].

This should be checked by a legal professional.
