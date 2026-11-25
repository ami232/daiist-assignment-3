# Hoja compacta para calificar (sin veredicto del juez)
Rellena `eval/human_labels.csv` con `id,correct,supported,notes`. correct = coincide con la referencia (o rechazo correcto en las unanswerable). supported = cada afirmación está en el texto recuperado (si dudas, mira el texto completo en grading_sheet.md). Nota obligatoria para cada 0.

## q01 (single)
**Pregunta:** What are the seven characteristics of trustworthy AI systems in the AI RMF?

**Referencia:** Valid and reliable; safe; secure and resilient; accountable and transparent; explainable and interpretable; privacy-enhanced; and fair with harmful bias managed.

**Respuesta del agente:** The AI Risk Management Framework articulates the following seven characteristics of trustworthy AI systems:

* Valid and reliable [nist-ai-rmf-1.0, pp. 15-17]
* Safe [nist-ai-rmf-1.0, pp. 15-17]
* Secure and resilient [nist-ai-rmf-1.0, pp. 15-17]
* Accountable and transparent [nist-ai-rmf-1.0, pp. 15-17]
* Explainable and interpretable [nist-ai-rmf-1.0, pp. 15-17]
* Privacy-enhanced [nist-ai-rmf-1.0, pp. 15-17]
* Fair with harmful bias managed [nist-ai-rmf-1.0, pp. 15-17]

_Recuperado:_ [nist-ai-rmf-1.0, p. 17], [nist-ai-rmf-1.0, p. 5], [nist-ai-rmf-1.0, pp. 15-17], [nist-ai-rmf-1.0, pp. 5-6], [nist-ai-rmf-1.0, pp. 7-8]

## q02 (single)
**Pregunta:** Which trustworthiness characteristic does the AI RMF treat as a necessary condition and show as the base for the others?

**Referencia:** Valid and reliable.

**Respuesta del agente:** The AI RMF treats **Valid & Reliable** as a necessary condition of trustworthiness and shows it as the base for the other trustworthiness characteristics [nist-ai-rmf-1.0, pp. 5-6].

_Recuperado:_ [nist-ai-rmf-1.0, p. 17], [nist-ai-rmf-1.0, p. 18], [nist-ai-rmf-1.0, p. 5], [nist-ai-rmf-1.0, pp. 20-21], [nist-ai-rmf-1.0, pp. 5-6]

## q03 (single)
**Pregunta:** What does subcategory GOVERN 1.1 of the AI RMF require?

**Referencia:** That legal and regulatory requirements involving AI are understood, managed, and documented.

**Respuesta del agente:** Subcategory GOVERN 1.1 of the AI RMF requires that legal and regulatory requirements involving AI are understood, managed, and documented [nist-ai-rmf-1.0, pp. 27-28].

_Recuperado:_ [nist-ai-600-1, p. 17], [nist-ai-rmf-1.0, p. 26], [nist-ai-rmf-1.0, pp. 27-28], [nist-ai-rmf-1.0, pp. 28-29]

## q04 (single)
**Pregunta:** Once GOVERN is in place, which AI RMF function do most users start with?

**Referencia:** MAP, then MEASURE or MANAGE.

**Respuesta del agente:** Once GOVERN is in place, most users of the AI RMF start with the MAP function and continue to MEASURE or MANAGE [nist-ai-rmf-1.0, p. 26].

_Recuperado:_ [nist-ai-600-1, p. 17], [nist-ai-rmf-1.0, p. 26], [nist-ai-rmf-1.0, p. 8], [nist-ai-rmf-1.0, pp. 24-25], [nist-ai-rmf-1.0, pp. 5-6]

## q05 (single)
**Pregunta:** Does the AI RMF prescribe a risk tolerance for organizations?

**Referencia:** No. It can be used to prioritize risk but does not prescribe risk tolerance, which varies by organization and context.

**Respuesta del agente:** No, the AI RMF does not prescribe a risk tolerance [nist-ai-rmf-1.0, pp. 11-12]. While the framework can be used to prioritize risks, risk tolerance is highly contextual, application- and use-case-specific, and varies based on organizational priorities, resource considerations, legal or regulatory requirements, and established norms [nist-ai-rmf-1.0, pp. 11-12]. 

Organizations should follow existing regulations, guidelines, or professional requirements for risk tolerance, or define a reasonable risk tolerance themselves where established guidelines do not exist [nist-ai-rmf-1.0, p. 12]. Once defined, the AI RMF can be used to manage risks and document the process [nist-ai-rmf-1.0, p. 12].

_Recuperado:_ [nist-ai-rmf-1.0, p. 12], [nist-ai-rmf-1.0, p. 47], [nist-ai-rmf-1.0, pp. 11-12], [nist-ai-rmf-1.0, pp. 13-14]

## q06 (single)
**Pregunta:** By when is a formal review of the AI RMF, with input from the AI community, expected to take place?

**Referencia:** No later than 2028.

**Respuesta del agente:** A formal review of the AI RMF with input from the AI community is expected to take place no later than 2028 [nist-ai-rmf-1.0, pp. 1-3].

_Recuperado:_ [nist-ai-rmf-1.0, p. 47], [nist-ai-rmf-1.0, p. 8], [nist-ai-rmf-1.0, pp. 1-3], [nist-ai-rmf-1.0, pp. 23-24], [nist-ai-rmf-1.0, pp. 3-4]

## q07 (single)
**Pregunta:** What term does NIST's Generative AI Profile use for confidently stated but false generated content, which is colloquially called a hallucination?

**Referencia:** Confabulation.

**Respuesta del agente:** NIST's Generative AI Profile uses the term **confabulation** for generated content that is erroneous, false, and presented confidently in response to prompts [nist-ai-600-1, pp. 9-10].

_Recuperado:_ [nist-ai-600-1, p. 10], [nist-ai-600-1, pp. 58-59], [nist-ai-600-1, pp. 59-60], [nist-ai-600-1, pp. 63-64], [nist-ai-600-1, pp. 9-10]

## q08 (single)
**Pregunta:** How many risks unique to or exacerbated by generative AI does the NIST Generative AI Profile define?

**Referencia:** Twelve.

**Respuesta del agente:** Model call limits exceeded: run limit (8/8)

_Recuperado:_ [nist-ai-600-1, p. 16], [nist-ai-600-1, p. 51], [nist-ai-600-1, p. 6], [nist-ai-600-1, p. 7], [nist-ai-600-1, pp. 1-3], [nist-ai-600-1, pp. 39-40], [nist-ai-600-1, pp. 41-42], [nist-ai-600-1, pp. 5-6], [nist-ai-600-1, pp. 6-7], [nist-ai-600-1, pp. 7-8], [nist-ai-rmf-1.0, p. 37], [nist-ai-rmf-1.0, pp. 1-3], [nist-ai-rmf-1.0, pp. 27-28], [nist-ai-rmf-1.0, pp. 3-4], [nist-ai-rmf-1.0, pp. 35-36], [nist-ai-rmf-1.0, pp. 37-38], [nist-ai-rmf-1.0, pp. 4-5]

## q09 (single)
**Pregunta:** What does the 'Environmental Impacts' risk refer to in the Generative AI Profile?

**Referencia:** Impacts due to high compute resource use in training or operating GAI models, and related outcomes that may adversely affect ecosystems.

**Respuesta del agente:** The 'Environmental Impacts' risk refers to the impacts caused by high compute resource utilization during the training, maintaining, and operating (running inference on) of Generative AI models, along with related outcomes that may adversely impact ecosystems [nist-ai-600-1, pp. 11-12, 8]. These resource-intensive activities result in potentially large energy and environmental footprints, with energy and carbon emissions varying based on tasks (e.g., pre-training, fine-tuning, inference), content modalities, hardware, and application types [nist-ai-600-1, pp. 11-12].

_Recuperado:_ [nist-ai-600-1, p. 12], [nist-ai-600-1, p. 5], [nist-ai-600-1, p. 8], [nist-ai-600-1, pp. 11-12], [nist-ai-600-1, pp. 41-42]

## q10 (single)
**Pregunta:** What is the 'Human-AI Configuration' risk in the Generative AI Profile?

**Referencia:** Arrangements or interactions between a human and an AI system that can lead to anthropomorphizing, algorithmic aversion, automation bias, over-reliance or emotional entanglement.

**Respuesta del agente:** In the Generative AI Profile, 'Human-AI Configuration' refers to risks arising from how humans interact with generative AI systems [nist-ai-600-1, p. 13]. Key aspects of this risk include:

* **Unnecessary Averse Behavior:** Human experts who are new to interacting with AI systems—while potentially knowledgeable in their own domains—may lack detailed knowledge of how AI works, leading them to be unnecessarily averse to GAI systems and depriving themselves or others of beneficial uses [nist-ai-600-1, p. 13].
* **Automation Bias and Over-reliance:** Over time, due to the complexity and increasing reliability of GAI technology, humans may over-rely on GAI systems or unjustifiably perceive GAI content to be of higher quality than content from other sources [nist-ai-600-1, p. 13]. This excessive deference to automated systems can exacerbate other risks like confabulation, bias, or homogenization [nist-ai-600-1, p. 13].
* **Emotional Entanglement:** Concerns about emotional entanglement between humans and GAI systems, which could lead to negative psychological impacts [nist-ai-600-1, p. 13].

_Recuperado:_ [nist-ai-600-1, p. 13], [nist-ai-600-1, p. 48], [nist-ai-600-1, p. 5], [nist-ai-600-1, pp. 1-3], [nist-ai-600-1, pp. 27-28], [nist-ai-600-1, pp. 29-30], [nist-ai-600-1, pp. 3-5], [nist-ai-600-1, pp. 33-34], [nist-ai-600-1, pp. 34-35], [nist-ai-600-1, pp. 35-36], [nist-ai-600-1, pp. 5-6], [nist-ai-rmf-1.0, pp. 46-47]

## q11 (single)
**Pregunta:** What are the four Tiers of CSF 2.0?

**Referencia:** Partial (Tier 1), Risk Informed (Tier 2), Repeatable (Tier 3) and Adaptive (Tier 4).

**Respuesta del agente:** The four Tiers of CSF 2.0 characterize the rigor of an organization's cybersecurity risk governance and management practices [nist-csf-2.0, pp. 12-13]:

* **Tier 1: Partial** [nist-csf-2.0, pp. 12-13]
* **Tier 2: Risk Informed** [nist-csf-2.0, pp. 12-13]
* **Tier 3: Repeatable** [nist-csf-2.0, pp. 12-13]
* **Tier 4: Adaptive** [nist-csf-2.0, pp. 12-13]

These Tiers describe a progression from informal, ad hoc responses to approaches that are agile, risk-informed, and continuously improving [nist-csf-2.0, pp. 12-13].

_Recuperado:_ [nist-csf-2.0, p. 6], [nist-csf-2.0, pp. 12-13], [nist-csf-2.0, pp. 13-14], [nist-csf-2.0, pp. 28-29], [nist-csf-2.0, pp. 5-6]

## q12 (single)
**Pregunta:** What is a Community Profile in CSF 2.0?

**Referencia:** A baseline of CSF outcomes created and published to address shared interests and goals of several organizations, typically for a sector, technology, threat type or other use case.

**Respuesta del agente:** A Community Profile is a baseline of CSF outcomes created and published to address shared interests and goals among multiple organizations [nist-csf-2.0, p. 11]. It is typically developed for a particular sector, subsector, technology, threat type, or other use case [nist-csf-2.0, p. 11], and an organization can use it as the basis for its own Target Profile [nist-csf-2.0, p. 11].

_Recuperado:_ [nist-csf-2.0, p. 11], [nist-csf-2.0, pp. 11-12], [nist-sp-800-61r3, p. 18], [nist-sp-800-61r3, p. 19], [nist-sp-800-61r3, p. 31]

## q13 (single)
**Pregunta:** Why is GOVERN drawn at the center of the CSF 2.0 Functions wheel?

**Referencia:** Because it informs how an organization will implement the other five Functions.

**Respuesta del agente:** GOVERN is drawn at the center of the CSF Functions wheel because it informs how an organization will implement the other five Functions [nist-csf-2.0, pp. 9-10].

_Recuperado:_ [nist-csf-2.0, p. 20], [nist-csf-2.0, p. 8], [nist-csf-2.0, p. 9], [nist-csf-2.0, pp. 9-10], [nist-sp-800-61r3, p. 13]

## q14 (single)
**Pregunta:** What are the four groups of practices in the Secure Software Development Framework?

**Referencia:** Prepare the Organization (PO), Protect the Software (PS), Produce Well-Secured Software (PW) and Respond to Vulnerabilities (RV).

**Respuesta del agente:** The Secure Software Development Framework (SSDF) organizes its practices into four groups:

1. **Prepare the Organization (PO)**: Ensure that people, processes, and technology are prepared to perform secure software development at the organization level [nist-sp-800-218, p. 13].
2. **Protect the Software (PS)**: Protect all components of the software from tampering and unauthorized access [nist-sp-800-218, p. 13].
3. **Produce Well-Secured Software (PW)**: Produce well-secured software with minimal security vulnerabilities in its releases [nist-sp-800-218, p. 13].
4. **Respond to Vulnerabilities (RV)**: Identify residual vulnerabilities in software releases and respond appropriately to address them and prevent similar vulnerabilities from occurring in the future [nist-sp-800-218, p. 13].

_Recuperado:_ [nist-sp-800-218, p. 13], [nist-sp-800-218, pp. 11-12], [nist-sp-800-218, pp. 12-13], [nist-sp-800-218, pp. 32-33], [nist-sp-800-218, pp. 5-6]

## q15 (single)
**Pregunta:** What does 'shifting left' mean in the SSDF and why does it matter?

**Referencia:** Addressing security earlier in the software development life cycle; it takes less effort and cost, minimizes technical debt and yields stronger, more resilient software.

**Respuesta del agente:** In the SSDF, "shifting left" refers to the principle that the earlier security is addressed in the Software Development Life Cycle (SDLC), the less effort and cost is ultimately required to achieve the same level of security [nist-sp-800-218, p. 10]. 

It matters for several reasons:
* It minimizes technical debt that would otherwise require remediating early security flaws late in development or after production [nist-sp-800-218, p. 10].
* It reduces the effort and cost needed to achieve security [nist-sp-800-218, p. 10].
* It results in software with stronger overall security and resiliency [nist-sp-800-218, p. 10].

_Recuperado:_ [nist-sp-800-218, p. 10], [nist-sp-800-218, pp. 11-12], [nist-sp-800-218, pp. 12-13], [nist-sp-800-218, pp. 13-14], [nist-sp-800-218, pp. 4-5]

## q16 (single)
**Pregunta:** According to SP 800-61 Rev. 3, what do incident handlers do?

**Referencia:** They verify that an incident has occurred, collect and analyze data and evidence, prioritize response activities, and act to limit damage, find root causes and restore operations.

**Respuesta del agente:** According to SP 800-61 Rev. 3, incident handlers:* Verify that an incident has occurred [nist-sp-800-61r3, pp. 14-15].
* Collect and analyze data and evidence [nist-sp-800-61r3, pp. 14-15].
* Prioritize incident response activities [nist-sp-800-61r3, pp. 14-15].
* Act appropriately to limit damage, find root causes, and restore operations [nist-sp-800-61r3, pp. 14-15].
* Provide input to others on mitigating cybersecurity issues and improving resiliency [nist-sp-800-61r3, pp. 14-15].
* Manually select and perform containment and eradication actions when allowed (instead of or in addition to automated measures) [nist-sp-800-61r3, pp. 40-41].

_Recuperado:_ [nist-sp-800-61r3, pp. 13-14], [nist-sp-800-61r3, pp. 14-15], [nist-sp-800-61r3, pp. 3-5], [nist-sp-800-61r3, pp. 37-38], [nist-sp-800-61r3, pp. 40-41]

## q17 (single)
**Pregunta:** What do the High, Medium and Low priorities mean in the CSF 2.0 Community Profile for cyber incident risk management?

**Referencia:** High: a core incident response activity for most organizations; Medium: directly supports incident response; Low: indirectly supports it.

**Respuesta del agente:** In the CSF 2.0 Community Profile for cyber incident risk management, the relative priorities indicate the following within the context of incident response [nist-sp-800-61r3, p. 18]:

* **High:** Functions as a core incident response activity for most organizations [nist-sp-800-61r3, p. 18].
* **Medium:** Directly supports incident response activities for most organizations [nist-sp-800-61r3, p. 18].
* **Low:** Indirectly supports incident response activities for most organizations [nist-sp-800-61r3, p. 18].

These priorities serve as a starting point, and organizations are encouraged to customize the Community Profile to reflect their own specific priorities and needs [nist-sp-800-61r3, p. 18].

_Recuperado:_ [nist-sp-800-61r3, p. 18], [nist-sp-800-61r3, p. 19], [nist-sp-800-61r3, p. 31], [nist-sp-800-61r3, pp. 19-20]

## q18 (single)
**Pregunta:** What does SSDF practice PW.2.1 call for?

**Referencia:** Having a qualified person not involved in the design and/or automated processes review the software design to confirm it meets the security requirements and addresses the identified risk information.

**Respuesta del agente:** SSDF practice PW.2.1 calls for having a qualified person (or people) who were not involved with the design, and/or automated processes instantiated in the toolchain, review the software design to confirm and enforce that it meets all security requirements and satisfactorily addresses identified risk information [nist-sp-800-218, pp. 20-21].

_Recuperado:_ [nist-sp-800-218, p. 13], [nist-sp-800-218, p. 22], [nist-sp-800-218, pp. 20-21], [nist-sp-800-218, pp. 21-22], [nist-sp-800-218, pp. 25-26]

## q19 (multi)
**Pregunta:** Which CSF 2.0 Function sits at the center of its wheel, and which AI RMF function is described as cross-cutting?

**Referencia:** GOVERN in both: the center of the CSF wheel, and the AI RMF's cross-cutting function infused through the others.

**Respuesta del agente:** The GOVERN Function sits at the center of the CSF 2.0 wheel because it informs how an organization will implement the other five Functions [nist-csf-2.0, pp. 9-10]. Similarly, the GOVERN function in the AI RMF is described as a cross-cutting function that is infused throughout AI risk management to inform and enable the other functions [nist-ai-rmf-1.0, pp. 26-27, 42].

_Recuperado:_ [nist-ai-rmf-1.0, p. 26], [nist-ai-rmf-1.0, pp. 25-26], [nist-ai-rmf-1.0, pp. 26-27], [nist-ai-rmf-1.0, pp. 4-5], [nist-ai-rmf-1.0, pp. 5-6], [nist-csf-2.0, p. 20], [nist-csf-2.0, p. 8], [nist-csf-2.0, p. 9], [nist-csf-2.0, pp. 1-2], [nist-csf-2.0, pp. 9-10]

## q20 (multi)
**Pregunta:** How many Functions do the CSF 2.0 Core and the AI RMF Core have, and what are they?

**Referencia:** CSF 2.0 has six: Govern, Identify, Protect, Detect, Respond, Recover. The AI RMF has four: Govern, Map, Measure, Manage.

**Respuesta del agente:** The CSF 2.0 Core has six Functions: Govern, Identify, Protect, Detect, Respond, and Recover [nist-csf-2.0, p. 8].

The AI RMF Core has four Functions: Govern, Map, Measure, and Manage [nist-ai-rmf-1.0, p. 25].

_Recuperado:_ [nist-ai-rmf-1.0, p. 26], [nist-ai-rmf-1.0, p. 8], [nist-ai-rmf-1.0, pp. 24-25], [nist-ai-rmf-1.0, pp. 25-26], [nist-ai-rmf-1.0, pp. 4-5], [nist-csf-2.0, p. 20], [nist-csf-2.0, p. 31], [nist-csf-2.0, p. 8], [nist-csf-2.0, pp. 9-10], [nist-sp-800-61r3, p. 13]

## q21 (multi)
**Pregunta:** How does the incident response life cycle in SP 800-61 Rev. 3 differ from the one in the previous revision?

**Referencia:** The old model had Preparation, Detection & Analysis, Containment/Eradication/Recovery and Post-Incident Activity as a circular cycle; the new one is based on the six CSF 2.0 Functions, with response integrated into risk management and continuous improvement.

**Respuesta del agente:** SP 800-61 Rev. 3 replaces the previous revision's circular incident response life cycle model with a new model based on NIST Cybersecurity Framework (CSF) 2.0 Functions [nist-sp-800-61r3, pp. 11-14]. 

The previous model's phases map to CSF 2.0 Functions as follows:
* **Preparation** maps to *Govern*, *Identify* (all Categories), and *Protect* [nist-sp-800-61r3, pp. 13-14].
* **Detection & Analysis** maps to *Detect* and *Identify* (Improvement Category) [nist-sp-800-61r3, pp. 13-14].
* **Containment, Eradication & Recovery** maps to *Respond*, *Recover*, and *Identify* (Improvement Category) [nist-sp-800-61r3, pp. 13-14].
* **Post-Incident Activity** maps to *Identify* (Improvement Category) [nist-sp-800-61r3, pp. 13-14].

While the previous revision treated incident response as a separate set of circular activities performed by a separate team, the new model integrates incident response into broader cybersecurity risk management, separating out broader risk management activities (Govern, Identify, Protect) from direct incident response (Detect, Respond, Recover) while emphasizing continuous improvement through the Identify Function's Improvement Category [nist-sp-800-61r3, pp. 11-14].

_Recuperado:_ [nist-sp-800-61r3, p. 14], [nist-sp-800-61r3, pp. 11-12], [nist-sp-800-61r3, pp. 13-14], [nist-sp-800-61r3, pp. 3-5], [nist-sp-800-61r3, pp. 44-45]

## q22 (multi)
**Pregunta:** What do a Current Profile and a Target Profile specify in CSF 2.0, and what comes after creating them?

**Referencia:** Current: outcomes currently achieved; Target: desired outcomes selected and prioritized. Next, analyze the gaps between them and create an action plan.

**Respuesta del agente:** In CSF 2.0, the two profiles specify the following:

* **Current Profile:** Specifies the Core outcomes that an organization is currently achieving (or attempting to achieve) and characterizes how or to what extent each outcome is being achieved [nist-csf-2.0, p. 11].
* **Target Profile:** Specifies the desired outcomes that an organization has selected and prioritized for achieving its cybersecurity risk management objectives, taking into account anticipated changes such as new requirements, new technology adoption, and threat intelligence trends [nist-csf-2.0, p. 11].

After creating them, the next steps are:
1. **Analyze the gaps and create an action plan:** Conduct a gap analysis to identify and analyze differences between the Current and Target Profiles, and develop a prioritized action plan (such as a risk register, risk detail report, or Plan of Action and Milestones [POA&M]) to address those gaps [nist-csf-2.0, p. 12].
2. **Implement the action plan and update the Organizational Profile:** Follow the action plan to address the gaps, move the organization toward the Target Profile, and update the profile as part of continual improvement [nist-csf-2.0, p. 12].

_Recuperado:_ [nist-csf-2.0, p. 11], [nist-csf-2.0, p. 12], [nist-csf-2.0, p. 31], [nist-csf-2.0, pp. 11-12], [nist-csf-2.0, pp. 6-7], [nist-sp-800-61r3, p. 18]

## q23 (multi)
**Pregunta:** What does the Generative AI Profile mean by the 'Value Chain and Component Integration' risk, and which SSDF practice addresses acquiring well-secured third-party software?

**Referencia:** Non-transparent or untraceable integration of upstream third-party components, with poor supplier vetting; SSDF PW.4.1 acquires and maintains well-secured software components.

**Respuesta del agente:** The Generative AI Profile defines "Value Chain and Component Integration" as the risk arising because Generative AI (GAI) value chains involve many third-party components (such as procured datasets, pre-trained models, and software libraries) that may be improperly obtained or inadequately vetted [nist-ai-600-1, p. 15]. This leads to diminished transparency or accountability for downstream users [nist-ai-600-1, p. 15]. This risk is exacerbated by factors such as the massive scale of training data (which is too large for humans to vet), the difficulty of training foundation models leading to extensive reuse of limited models, and the integration of GAI into various devices and services, making it difficult to attribute behavioral issues or downstream errors to any single source [nist-ai-600-1, pp. 15–16].

Acquiring well-secured third-party software components is addressed by SSDF Practice **PW.4 (Reuse Existing, Well-Secure Software When Feasible Instead of Duplicating Functionality)**, specifically task **PW.4.1** (Acquire and maintain well-secured software components from commercial, open-source, and other third-party developers) [nist-sp-800-218, p. 21]. Additionally, communicating requirements for third-party software components is addressed under Practice **PO.1 (Define Security Requirements for Software Development)**, specifically task **PO.1.3** [nist-sp-800-218, pp. 14–15].

_Recuperado:_ [nist-ai-600-1, p. 16], [nist-ai-600-1, p. 25], [nist-ai-600-1, pp. 15-16], [nist-ai-600-1, pp. 24-25], [nist-csf-2.0, pp. 18-19], [nist-sp-800-218, p. 21], [nist-sp-800-218, pp. 11-12], [nist-sp-800-218, pp. 13-14], [nist-sp-800-218, pp. 14-15], [nist-sp-800-218, pp. 4-5]

## q24 (multi)
**Pregunta:** Both the AI RMF and CSF 2.0 use Current and Target Profiles. How does the AI RMF describe temporal profiles, and how does CSF 2.0 define a Target Profile?

**Referencia:** AI RMF temporal profiles describe the current state or the desired target state of AI risk management; a CSF Target Profile specifies the desired outcomes an organization has selected and prioritized.

**Respuesta del agente:** The AI RMF describes temporal profiles as descriptions of either the current state or the desired, target state of specific AI risk management activities within a given sector, industry, organization, or application context [nist-ai-rmf-1.0, pp. 38-39]. 

CSF 2.0 defines a Target Profile as a part of an Organizational Profile that specifies the desired Core outcomes that an organization has selected and prioritized for achieving its cybersecurity risk management objectives [nist-csf-2.0, p. 31]. It considers anticipated changes to the organization's cybersecurity posture, such as new requirements, new technology adoption, and threat intelligence trends [nist-csf-2.0, p. 11].

_Recuperado:_ [nist-ai-600-1, p. 5], [nist-ai-600-1, pp. 3-5], [nist-ai-rmf-1.0, p. 38], [nist-ai-rmf-1.0, pp. 38-39], [nist-ai-rmf-1.0, pp. 38-40], [nist-csf-2.0, p. 11], [nist-csf-2.0, p. 12], [nist-csf-2.0, p. 31], [nist-csf-2.0, pp. 11-12], [nist-csf-2.0, pp. 12-13]

## q25 (multi)
**Pregunta:** Do the CSF 2.0 Core and the AI RMF Core treat their outcomes as a checklist?

**Referencia:** No. The CSF outcomes are not a checklist, and AI RMF actions are neither a checklist nor necessarily an ordered set of steps.

**Respuesta del agente:** No, neither framework treats its outcomes as a checklist:

* **CSF 2.0 Core:** The outcomes in the CSF Core are explicitly stated to "not [be] a checklist of actions to perform," as the specific actions taken and the responsible individuals will vary by organization and use case [nist-csf-2.0, p. 8].
* **AI RMF Core:** The AI RMF states that its actions and outcomes "do not constitute a checklist, nor are they necessarily an ordered set of steps" [nist-ai-rmf-1.0, p. 25].

_Recuperado:_ [nist-ai-600-1, pp. 60-61], [nist-ai-rmf-1.0, p. 47], [nist-ai-rmf-1.0, pp. 24-25], [nist-ai-rmf-1.0, pp. 25-26], [nist-ai-rmf-1.0, pp. 4-5], [nist-csf-2.0, p. 20], [nist-csf-2.0, p. 31], [nist-csf-2.0, p. 8], [nist-csf-2.0, pp. 5-6], [nist-csf-2.0, pp. 7-8]

## q26 (multi)
**Pregunta:** Which kinds of staff can act as incident handlers in SP 800-61 Rev. 3, and how should responsibilities with third-party providers be handled?

**Referencia:** Handlers may be on staff, on contract or available when needed; with third parties it is a shared responsibility model whose responsibilities should be clearly defined in a contract.

**Respuesta del agente:** An organization's incident handlers can be:
* **On staff** (e.g., an internal incident response team) [nist-sp-800-61r3, pp. 14–15].
* **On contract** (e.g., outsourcing a security operations center to a managed security services provider [MSSP], or leveraging a cloud service provider's incident response team) [nist-sp-800-61r3, pp. 14–15].
* **Available when needed** (e.g., from a parent organization, a cybersecurity services provider, a business partner, or a law enforcement agency) [nist-sp-800-61r3, pp. 14–15, 15].

Responsibilities with third-party providers should be handled through a shared responsibility model where responsibilities are clearly defined in a contract [nist-sp-800-61r3, p. 16]. Specifically:
* The incident response team must be aware of the division of responsibilities, including information flows, coordination, and the provider's authority to act on behalf of the organization [nist-sp-800-61r3, p. 16].
* Contracts should outline restrictions on what service providers can do, such as sharing sanitized incident information with other customers or making and implementing operational decisions [nist-sp-800-61r3, p. 16].
* Risks related to malicious insiders or provider compromise should be addressed using mechanisms like non-disclosure agreements (NDAs) and contracting clauses [nist-sp-800-61r3, p. 16].

_Recuperado:_ [nist-sp-800-61r3, p. 15], [nist-sp-800-61r3, p. 16], [nist-sp-800-61r3, pp. 14-15], [nist-sp-800-61r3, pp. 40-41]

## q27 (unanswerable)
**Pregunta:** What minimum password length does NIST require for user-chosen passwords?

**Referencia:** The corpus does not cover this; the assistant should say so instead of answering.

**Respuesta del agente:** The corpus does not cover this. The available documents include the NIST Cybersecurity Framework 2.0, SP 800-218 (Secure Software Development Framework), SP 800-61 Rev. 3 (Incident Response), the AI Risk Management Framework 1.0, and the Generative AI Profile, but they do not contain password length requirements for user-chosen passwords (which are typically addressed in NIST SP 800-63 Digital Identity Guidelines, not present in this corpus).

_Recuperado:_ [nist-sp-800-218, p. 29], [nist-sp-800-218, pp. 1-3], [nist-sp-800-218, pp. 29-30], [nist-sp-800-218, pp. 30-31], [nist-sp-800-61r3, pp. 41-42]

## q28 (unanswerable)
**Pregunta:** What penalties does the EU AI Act impose on providers of high-risk AI systems?

**Referencia:** The corpus does not cover this; the assistant should say so instead of answering.

**Respuesta del agente:** The corpus does not cover this. The provided NIST documents (AI Risk Management Framework 1.0, Generative AI Profile, Cybersecurity Framework 2.0, SP 800-61 Rev. 3, and SP 800-218) do not contain information regarding the EU AI Act or its specific penalties for providers of high-risk AI systems.

_Recuperado:_ [nist-ai-600-1, p. 25], [nist-ai-600-1, pp. 25-26], [nist-ai-rmf-1.0, p. 42], [nist-ai-rmf-1.0, pp. 41-42], [nist-ai-rmf-1.0, pp. 43-44]

## q29 (unanswerable)
**Pregunta:** Which post-quantum algorithms does NIST recommend for protecting AI model weights?

**Referencia:** The corpus does not cover this; the assistant should say so instead of answering.

**Respuesta del agente:** The corpus does not cover post-quantum algorithms or recommendations for protecting AI model weights using post-quantum cryptography. The indexed documents discuss information security and the protection of model weights [nist-ai-600-1, p. 14], but do not specify post-quantum algorithms for this purpose.

_Recuperado:_ [nist-ai-600-1, p. 47], [nist-ai-600-1, p. 62], [nist-ai-600-1, pp. 14-15], [nist-ai-600-1, pp. 36-37], [nist-ai-600-1, pp. 59-60]

## q30 (unanswerable)
**Pregunta:** Within how many hours must a significant cyber incident be reported to CISA under CIRCIA?

**Referencia:** The corpus does not cover this; the assistant should say so instead of answering.

**Respuesta del agente:** The corpus does not cover this. The NIST documents do not contain information regarding reporting timelines under CIRCIA or specific requirements for reporting to CISA.

_Recuperado:_ [nist-sp-800-61r3, pp. 36-37], [nist-sp-800-61r3, pp. 37-38], [nist-sp-800-61r3, pp. 39-40], [nist-sp-800-61r3, pp. 43-44], [nist-sp-800-61r3, pp. 46-47]

## q31 (unanswerable)
**Pregunta:** Which SOC 2 trust services criteria correspond to the CSF 2.0 Protect function?

**Referencia:** The corpus does not cover this; the assistant should say so instead of answering.

**Respuesta del agente:** The corpus does not cover SOC 2 trust services criteria. It covers the NIST Cybersecurity Framework (CSF) 2.0 Protect function, which includes categories such as identity management, authentication, and access control (PR.AA), awareness and training (PR.AT), data security (PR.DS), platform security (PR.PS), and technology infrastructure resilience (PR.IR) [nist-csf-2.0, p. 20].

_Recuperado:_ [nist-csf-2.0, p. 20], [nist-csf-2.0, pp. 28-29], [nist-csf-2.0, pp. 8-9], [nist-sp-800-61r3, p. 13], [nist-sp-800-61r3, p. 18]

## q32 (unanswerable)
**Pregunta:** What is the maximum GDPR fine for a personal data breach that is found during incident response?

**Referencia:** The corpus does not cover this; the assistant should say so instead of answering.

**Respuesta del agente:** The corpus does not cover this. The NIST documents discuss incident response procedures [nist-sp-800-61r3, p. 35] and alignment with data protection or breach reporting laws [nist-ai-600-1, p. 25], but they do not contain legal details or specific fine amounts for the GDPR.

_Recuperado:_ [nist-ai-600-1, pp. 25-26], [nist-sp-800-61r3, pp. 35-36], [nist-sp-800-61r3, pp. 36-37], [nist-sp-800-61r3, pp. 43-44]

## q33 (unanswerable)
**Pregunta:** Which TLS version does the SSDF require between build servers and artifact repositories?

**Referencia:** The corpus does not cover this; the assistant should say so instead of answering.

**Respuesta del agente:** The corpus does not cover specific TLS versions or requirements for communication between build servers and artifact repositories. The SSDF (NIST SP 800-218) outlines high-level secure software development practices and tasks—such as securing software development infrastructures and environments [nist-sp-800-218, p. 13]—but does not specify protocol versions or technical connection criteria for build servers and artifact repositories.

_Recuperado:_ [nist-sp-800-218, p. 16], [nist-sp-800-218, pp. 1-3], [nist-sp-800-218, pp. 12-13], [nist-sp-800-218, pp. 13-14], [nist-sp-800-218, pp. 16-17], [nist-sp-800-218, pp. 30-31], [nist-sp-800-218, pp. 31-32], [nist-sp-800-218, pp. 32-33], [nist-sp-800-61r3, pp. 45-47]
