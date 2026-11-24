# Before / after adding NIS2 (Directive (EU) 2022/2555) with add_document

1. **Before**: index = GDPR, AI Act, Data Act.
2. **After, first try**: NIS2 indexed and retrieved, but the search tool description and AGENTS.md still listed only three acts, so the agent treated NIS2 passages as outside the corpus.
3. **After the fix**: every search result starts with the acts read from the index, and AGENTS.md says every listed act is part of the corpus.

## q28: Our cloud platform just suffered a serious cyberattack. Do we have to send an early warning to the authorities within 24 hours?

**1. Before** (refused=True; retrieved: AI Act Article 15, AI Act Article 3, AI Act Article 73, Data Act Article 2, Data Act Article 37)

The indexed legislation does not cover this question. The corpus does not contain provisions establishing a 24-hour early warning obligation for general cloud platform cyberattacks; please check relevant cybersecurity legislation such as the NIS 2 Directive, national laws, or consult a lawyer.

**2. After, first try** (refused=True; retrieved: AI Act Article 73, GDPR Article 33, GDPR Article 34, NIS2 Article 23, NIS2 Article 35)

The indexed legislation does not cover this question. The corpus contains provisions on personal data breaches under the GDPR and reporting for high-risk AI systems, but general cybersecurity incident reporting for cloud platforms falls outside the indexed texts; please check relevant national cybersecurity laws (such as NIS2 transposition acts) or consult a lawyer.

**3. After the fix** (refused=False; cited: NIS2 Article 23)

Yes, if your cloud platform qualifies as an essential or important entity under NIS2 and suffers a significant incident affecting your services, you must submit an early warning to the CSIRT or competent authority without undue delay and within 24 hours of becoming aware of it.

* Essential and important entities must notify their CSIRT or competent authority without undue delay of any significant incident impacting their services. NIS2 Article 23(1)
* An incident is significant if it causes or can cause severe operational disruption or financial loss, or considerable material or non-material damage to others. NIS2 Article 23(3)
* The early warning must be submitted without undue delay and in any event within 24 hours of becoming aware of the significant incident. NIS2 Article 23(4)(a)
* The early warning must indicate whether the incident is suspected of being caused by unlawful or malicious acts or could have a cross-border impact. NIS2 Article 23(4)(a)
* Cloud computing service providers are specifically subject to these NIS2 reporting requirements. NIS2 Article 23(11)

---

## q29: Can our company directors be held personally responsible if we ignore cybersecurity risk measures?

**1. Before** (refused=True; retrieved: AI Act Article 15, AI Act Article 3, AI Act Article 4)

The indexed legislation does not cover this question. 

The provided corpus does not address the personal liability of company directors for ignoring cybersecurity risk measures. You should check relevant national corporate law, other EU acts, or consult a qualified lawyer.

**2. After, first try** (refused=True; retrieved: AI Act Article 15, NIS2 Article 20, NIS2 Article 21, NIS2 Article 32)

The indexed legislation does not cover this question. The retrieved provisions on cybersecurity risk measures and management body liability are from the NIS2 Directive, which is not included in the searchable corpus of the GDPR, AI Act, and Data Act. You should check the applicable EU directives, national laws, or consult legal counsel regarding director liability.

**3. After the fix** (refused=False; cited: NIS2 Article 20, NIS2 Article 32)

Yes, under the NIS2 Directive, Member States must ensure that management bodies of essential and important entities can be held liable for infringements of cybersecurity risk-management measures.

* Member States must ensure that management bodies approve cybersecurity risk-management measures, oversee their implementation, and can be held liable for infringements of those measures. NIS2 Article 20(1)
* Members of management bodies are required to follow training to gain sufficient knowledge and skills to identify risks and assess cybersecurity risk-management practices. NIS2 Article 20(2)
* Natural persons responsible for or acting as a legal representative with the authority to take decisions, exercise control, or ensure compliance can be held liable for breaching their duties to ensure compliance with the Directive. NIS2 Article 32(6)

---
