# Grading sheet

For each answer fill a row in eval/human_labels.csv: `correct` (1/0: matches the reference, or is a proper refusal), `supported` (1/0: every claim is in the retrieved passages below), `notes` (why, for every 0).

---

## q01 (single)

**Question:** What is the maximum height I can fly at in the open category?

**Reference:** The drone must stay within 120 metres of the closest point of the surface of the earth, except when overflying an obstacle as set out in Part A of the Annex.

**Agent answer:**

The maximum height is **120 metres (400 feet)** from the closest point of the surface of the earth [reg-2019-947 | Article 4 and UAS.OPEN.010]. 

### Exceptions and Conditions:
* **Artificial obstacles:** When flying within a horizontal distance of 50 metres from an artificial obstacle taller than 105 metres, the maximum height may be increased up to **15 metres above the height of the obstacle**, provided you have explicit permission from the entity responsible for the obstacle [reg-2019-947 | UAS.OPEN.010].
* **Unmanned sailplanes:** Unmanned sailplanes with a maximum take-off mass (including payload) of less than 10 kg may be flown at a distance exceeding 120 metres from the surface of the earth, as long as they are not flown at a height greater than **120 metres above the remote pilot** at any time [reg-2019-947 | UAS.OPEN.010].

*Citations: [reg-2019-947 | Article 4], [reg-2019-947 | UAS.OPEN.010], [easa-amc-gm | GM1 UAS.OPEN.010]*

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | GM1 UAS.OPEN.010 General provisions]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 UAS.OPEN.010 General provisions
MAXIMUM HEIGHT
The remote pilot must ensure that he or she keeps the unmanned aircraft (UA) at a distance less than 120 m (400 ft) from the terrain, and the picture below shows how the maximum height that the UA may reach changes according to the topography of the terrain. In addition, when the Member State (MS) has defined a geographical zone with a lower maximum height, the remote pilot must ensure that the UA always complies with the requirements of the geographical zone.
The entity responsible for the artificial obstacle referred to in point UAS.OPEN.010(3) needs to explicitly grant the unmanned aircraft system (UAS) operator permission to conduct an operation close to a tall man-made obstacle, e.g. a building, or antenna. No UAS operator should conduct an operation close to such an obstacle without permission from the entity responsible for the obstacle.

#### Result 2
Citation: [reg-2019-947 | UAS.OPEN.010 General provisions]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.010 General provisions
(1) The category of UAS ‘open’ operations is divided into three subcategories A1, A2 and A3, on the basis of operational limitations, requirements for the remote pilot and technical requirements for UAS.
(2) Where the UAS operation involves the flight of the unmanned aircraft starting from a natural elevation in the terrain or over terrain with natural elevations, the unmanned aircraft shall be maintained within 120 metres from the closest point of the surface of the earth. The measurement of distances shall be adapted accordingly to the geographical characteristics of the terrain, such as plains, hills, mountains.
(3) When flying an unmanned aircraft within a horizontal distance of 50 metres from an artificial obstacle taller than 105 metres, the maximum height of the UAS operation may be increased up to 15 metres above the height of the obstacle at the request of the entity responsible for the obstacle.
(4) By way of derogation from point (2), unmanned sailplanes with a MTOM, including payload, of less than 10 kg, may be flown at a distance in excess of 120 metres from the closest point of the surface of the earth, provided that the unmanned sailplane is not flown at a height greater than 120 metres above the remote pilot at any time.

#### Result 3
Citation: [reg-2019-947 | Article 4 - ‘Open’ category of UAS operations]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 4 - ‘Open’ category of UAS operations
1. Operations shall be classified as UAS operations in the ‘open’ category only where the following requirements are met:
(a) the UAS belongs to one of the classes set out in Delegated Regulation (EU) 2019/945 or is privately built or meets the conditions defined in Article 20;
(b) the unmanned aircraft has a maximum take-off mass of less than 25 kg;
(c) the remote pilot ensures that the unmanned aircraft is kept at a safe distance from people and that it is not flown over assemblies of people;
(d) the remote pilot keeps the unmanned aircraft in VLOS at all times except when flying in follow-me mode or when using an unmanned aircraft observer as specified in Part A of the Annex;
(e) during flight, the unmanned aircraft is maintained within 120 metres from the closest point of the surface of the earth, except when overflying an obstacle, as specified in Part A of the Annex
(f) during flight, the unmanned aircraft does not carry dangerous goods and does not drop any material;
2. UAS operations in the ‘open’ category shall be divided in three sub-categories in accordance with the requirements set out in Part A of the Annex.

#### Result 4
Citation: [reg-2019-947 | UAS.STS-02.010 General provisions]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.STS-02.010 General provisions
(1) During flight, the unmanned aircraft shall be maintained within 120 m from the closest point of the surface of the earth. The measurement of distances shall be adapted according to the geographical characteristics of the terrain, such as plains, hills, mountains.
(2) When flying an unmanned aircraft within a horizontal distance of 50 m from an artificial obstacle taller than 105 m, the maximum height of the UAS operation may be increased up to 15 m above the height of the obstacle at the request of the entity responsible for the obstacle.
(3) The maximum height of the operational volume shall not exceed 30 m above the maximum height allowed in points (1) and (2).
(4) During flight, the unmanned aircraft shall not carry dangerous goods.

#### Result 5
Citation: [easa-amc-gm | GM1 UAS.OPEN.010(4) General provisions]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 UAS.OPEN.010(4) General provisions
OPERATIONS WITH UNMANNED SAILPLANES
This derogation was included to allow model gliders to continue to operate along slopes. Strictly applying the 120-metre distance from the closest point of the surface of the earth would have had disproportionate consequences. These operations have been conducted successfully for decades and have generated a micro-economy in certain countries. Two measures have been put in place to reduce the risk:
(a) A maximum takeoff mass (MTOM), including the payload, limited to 10 kg to reduce the consequences of an impact. 10 kg should cover the vast majority of gliders in operation.
(b) The maximum height above the remote pilot is limited to 120 m, which reduces the air risk.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q02 (single)

**Question:** How old do I have to be to fly a drone in the open category?

**Reference:** The minimum age is 16, with exceptions (e.g. toy C0 in A1, privately built under 250 g, or under direct supervision of a qualified pilot). Member States may lower it by up to 4 years for the open category, valid only in their territory.

**Agent answer:**

The standard minimum age to fly a drone in the open category is **16 years** [reg-2019-947 | Article 9].

However, **no minimum age** is required in the following cases:
* When operating a C0 class drone that is considered a toy under Directive 2009/48/EC in subcategory A1 [reg-2019-947 | Article 9];
* For privately-built drones with a maximum take-off mass of less than 250 g [reg-2019-947 | Article 9];
* When flying under the direct supervision of a remote pilot who is at least 16 years old and meets all competency requirements [reg-2019-947 | Article 9, easa-amc-gm | GM1 Article 9].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-947 | Article 9 - Minimum age for remote pilots]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 9 - Minimum age for remote pilots
1. The minimum age for remote pilots operating a UAS in the ‘open’ and ‘specific’ category shall be 16 years.
2. No minimum age for remote pilots shall be required:
(a) when they operate in subcategory A1 as specified in Part A of the Annex to this Regulation, with a UAS Class C0 defined in Part 1 of the Annex to Delegated Regulation (EU) 2019/945 that is a toy within the meaning of Directive 2009/48/EC;
(b) for privately-built UAS with a maximum take-off mass of less than 250g;
(c) when they operate under the direct supervision of a remote pilot complying with paragraph 1 and Article 8.
3. Member States may lower the minimum age following a risk-based approach taking into account specific risks associated with the operations in their territory:
(a) for remote pilots operating in the ‘open’ category by up to 4 years;
(b) for remote pilots operating in the ‘specific’ category by up to 2 years.
4. Where a Member State lowers the minimum age for remote pilots, those remote pilots shall only be allowed to operate a UAS on the territory of that Member State.
5. Member States may define a different minimum age for remote pilots operating in the framework of model aircraft clubs or associations in the authorisation issued in accordance with Article 16.

#### Result 2
Citation: [reg-2019-947 | Article 4 - ‘Open’ category of UAS operations]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 4 - ‘Open’ category of UAS operations
1. Operations shall be classified as UAS operations in the ‘open’ category only where the following requirements are met:
(a) the UAS belongs to one of the classes set out in Delegated Regulation (EU) 2019/945 or is privately built or meets the conditions defined in Article 20;
(b) the unmanned aircraft has a maximum take-off mass of less than 25 kg;
(c) the remote pilot ensures that the unmanned aircraft is kept at a safe distance from people and that it is not flown over assemblies of people;
(d) the remote pilot keeps the unmanned aircraft in VLOS at all times except when flying in follow-me mode or when using an unmanned aircraft observer as specified in Part A of the Annex;
(e) during flight, the unmanned aircraft is maintained within 120 metres from the closest point of the surface of the earth, except when overflying an obstacle, as specified in Part A of the Annex
(f) during flight, the unmanned aircraft does not carry dangerous goods and does not drop any material;
2. UAS operations in the ‘open’ category shall be divided in three sub-categories in accordance with the requirements set out in Part A of the Annex.

#### Result 3
Citation: [easa-amc-gm | GM1 Article 9 Minimum age for remote pilots]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 Article 9 Minimum age for remote pilots
SUPERVISOR
A person may act as a remote pilot even if he or she has not reached the minimum age defined in Article 9(1) of the UAS Regulation, provided that the person is supervised. The supervising remote pilot must, in any case, comply with the age requirement specified in that Article. The possibility to lower the minimum age applies only to remote pilots (and not to supervisors). Since the supervisor and the young remote pilot must both demonstrate competency to act as a remote pilot, no minimum age is defined to conduct the training and pass the test to demonstrate the minimum competency to act as a remote pilot in the ‘open’ category.

#### Result 4
Citation: [reg-2019-947 | Article 8 - Rules and procedures for the competency of remote pilots]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 8 - Rules and procedures for the competency of remote pilots
1. Remote pilots operating UAS in the ‘open’ category shall comply with the competency requirements set in Part A of the Annex.
2. Remote pilots operating UAS in the ‘specific’ category shall comply with the competency requirements set out in the operational authorisation by the competent authority or in the standard scenario defined in Appendix 1 to the Annex or as defined by the LUC and shall have at least the following competencies:
(a) ability to apply operational procedures (normal, contingency and emergency procedures, flight planning, pre-flight and post-flight inspections);
(b) ability to manage aeronautical communication;
(c) manage the unmanned aircraft flight path and automation;
(d) leadership, teamwork and self-management;
(e) problem solving and decision-making;
(f) situational awareness;
(g) workload management;
(h) coordination or handover, as applicable.
3. Remote pilots operating in the framework of model aircraft clubs or associations shall comply with the minimum competency requirements defined in the authorisation granted in accordance with Article 16.

#### Result 5
Citation: [reg-2019-947 | UAS.OPEN.070 Duration and validity of the remote pilot online theoretical competency and certificates of remote pilot competency]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.070 Duration and validity of the remote pilot online theoretical competency and certificates of remote pilot competency
(1) The remote pilot online theoretical competency, required by points (4)(b) of point UAS.OPEN.020 and point (3) of point UAS.OPEN.040, and the certificate of remote pilot competency, required by point (2) of point UAS.OPEN.030, shall be valid for five years.
(2) The revalidation of the remote pilot online theoretical competency and of the certificate of remote pilot competency is, within its validity period, subject to:
(a) demonstration of competencies respectively in accordance with point (4)(b) of point UAS.OPEN.020 or point (2) of point UAS.OPEN.030; or
(b) the completion of a refresher training addressing respectively the theoretical knowledge subjects as defined in point (4)(b) of point UAS.OPEN.020 or point (2) of point UAS.OPEN.030 provided by the competent authority or by an entity designated by the competent authority.
(3) In order to revalidate the remote pilot online theoretical competency or the certificate of remote pilot competency upon its expiration, the remote pilot shall comply with point (2)(a).
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q03 (single)

**Question:** My drone weighs 300 g and has no camera. Do I need to register as an operator?

**Reference:** Yes. Operators must register when flying in the open category an aircraft with an MTOM of 250 g or more (or over 80 J impact energy), regardless of camera.

**Agent answer:**

**Yes**, you need to register as a drone operator.

Even though your drone has no camera, its Maximum Take-Off Mass (MTOM) is **300 g**, which is 250 g or more. Under the EU rules for the open category, operators must register themselves when operating unmanned aircraft with an MTOM of 250 g or more.

* **Binding rule:** Regulation (EU) 2019/947, Article 14(5)(a)(i) [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 2/3)
4. Member States shall ensure that registration systems are digital and interoperable and allow for mutual access and exchange of information through the repository referred to in Article 74 of Regulation (EU) 2018/1139.
5. UAS operators shall register themselves:
(a) when operating within the ‘open’ category any of the following unmanned aircraft:
i. with a MTOM of 250 g or more, or, which in the case of an impact can transfer to a human kinetic energy above 80 Joules;
ii. that is equipped with a sensor able to capture personal data, unless it complies with Directive 2009/48/EC.
(b) when operating within the ‘specific’ category an unmanned aircraft of any mass.
6. UAS operators shall register themselves in the Member State where they have their residence for natural persons or where they have their principal place of business for legal persons and ensure that their registration information is accurate. A UAS operator cannot be registered in more than one Member State at a time.
Member States shall issue a unique digital registration number for UAS operators and for the UAS that require registration, allowing their individual identification.
The registration number for UAS operators shall be established on the basis of standards that support the interoperability of the registration systems;
7. The owner of an unmanned aircraft whose design is subject to certification shall register the unmanned aircraft.

#### Result 2
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 1/3)
1. Member States shall establish and maintain accurate registration systems for UAS whose design is subject to certification and for UAS operators whose operation may present a risk to safety, security, privacy, and protection of personal data or environment.
2. The registration systems for UAS operators shall provide the fields for introducing and exchanging the following information:
(a) the full name and the date of birth for natural persons and the name and their identification number for legal persons;
(b) the address of UAS operators;
(c) their email address and telephone number;
(d) an insurance policy number for UAS if required by Union or national law;
(e) the confirmation by legal persons of the following statement: ‘All personnel directly involved in the operations are competent to perform their tasks, and the UAS will be operated only by remote pilots with the appropriate level of competency’;
(f) operational authorisations and LUCs held and declarations followed by a confirmation in accordance with Article 12(5)(b).
3. The registration systems for unmanned aircraft whose design is subject to certification shall provide the fields for introducing and exchanging the following information:
(a) manufacturer’s name;
(b) manufacturer’s designation of the unmanned aircraft;
(c) unmanned aircraft’s serial number;
(d) full name, address, email address and telephone number of the natural or legal person under whose name the unmanned aircraft is registered.

#### Result 3
Citation: [easa-amc-gm | AMC1 Article 14(8) Registration of UAS operators and ‘certified’ UAS]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 14(8) Registration of UAS operators and ‘certified’ UAS
DISPLAY OF REGISTRATION INFORMATION
(a) If the UAS operator owns the UAS or uses a UAS that is owned by a third party, it should:
(1) register itself;
(2) display on the UA the UAS operator registration number, which is received at the end of the registration process, in a way that the number is readable at least when the UA is on the ground, without using other devices than eyeglasses or corrective lenses; and
(3) upload the full string, which consists of the UAS operator registration number and the three (3) randomly generated alphanumerics, into the electronic identification system, if available.
(b) A QR code (quick response code) may be used.
(c) If the size of the UA does not allow the mark to be displayed in a visible way on the fuselage, or the UA represents a real aircraft where affixing the marking on the UA would spoil the realism of the representation, a marking inside the battery compartment is acceptable if the compartment is accessible.

#### Result 4
Citation: [reg-2019-947 | Powers and recitals]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Powers and recitals (part 3/7)
(11) Operations in the ‘certified’ category should, as a principle, be subject to rules on certification of the operator, and the licensing of remote pilots, in addition to the certification of the aircraft pursuant to Delegated Regulation (EU) 2019/945.
(12) Whilst mandatory for the ‘certified category’, for the ‘specific’ category a certificate delivered by the competent authorities for the operation of an unmanned aircraft, as well as for the personnel, including remote pilots and organisations involved in those activities, or for the aircraft pursuant to Delegated Regulation (EU) 2019/945 could also be required.
(13) Rules and procedures should be established for the marking and identification of unmanned aircraft and for the registration of operators of unmanned aircraft or certified unmanned aircraft.
(14) Operators of unmanned aircraft should be registered where they operate an unmanned aircraft which, in case of impact, can transfer, to a human, a kinetic energy above 80 Joules or the operation of which presents risks to privacy, protection of personal data, security or the environment.
(15) Studies have demonstrated that unmanned aircraft with a take-off mass of 250 g or more would present risks to security and therefore UAS operators of such unmanned aircraft should be required to register themselves when operating such aircraft in the ‘open’ category.

#### Result 5
Citation: [reg-2019-947 | ]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)


COMMISSION IMPLEMENTING REGULATION (EU) 2019/947 of 24 May 2019 on the rules and procedures for the operation of unmanned aircraft systems
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q04 (single)

**Question:** How far must I stay from residential areas when flying in subcategory A3?

**Reference:** At least 150 metres horizontally from residential, commercial, industrial or recreational areas, in an area where no uninvolved person is expected to be endangered.

**Agent answer:**

You must stay at a safe horizontal distance of **at least 150 metres** from residential, commercial, industrial, or recreational areas [reg-2019-947 | UAS.OPEN.040].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | GM1 UAS.OPEN.030(1) and UAS.OPEN.040(1) UAS operations in subcategories A1 and A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 UAS.OPEN.030(1) and UAS.OPEN.040(1) UAS operations in subcategories A1 and A3
DIFFERENCE BETWEEN SUB-CATEGORIES A2 AND A3
Subcategory A2 addresses operations during which flying close to people is intended for a significant portion of the flight. The minimum distance ranges from 30 m to 5 m from uninvolved people. 5 m is only allowed when there is an active low-speed mode function on the UA, and the remote pilot has conducted an evaluation of the situation regarding the weather, the performance of the UA and the segregation of the overflown area.
Sub-category A3 addresses operations that are conducted in an area (hereafter referred to as ‘the area’) where the remote pilot reasonably expects that no uninvolved people will be endangered within the range of the unmanned aircraft where it is flown during the mission. In addition, the operation must be conducted at a safe horizontal distance of at least 150 m from residential, commercial, industrial or recreational areas.

#### Result 2
Citation: [reg-2019-947 | UAS.OPEN.040 UAS operations in subcategory A3]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.040 UAS operations in subcategory A3
UAS operations in subcategory A3 shall comply with all of the following conditions:
(1) be conducted in an area where the remote pilot reasonably expects that no uninvolved person will be endangered within the range where the unmanned aircraft is flown during the entire time of the UAS operation;
(2) be conducted at a safe horizontal distance of at least 150 metres from residential, commercial, industrial or recreational areas;
(3) be performed by a remote pilot who is familiar with manufacturer’s instructions provided by the manufacturer of the UAS and who has completed an online training course and passed an online theoretical knowledge examination as defined in point (4)(b) of point UAS.OPEN.020;
(4) be performed with an unmanned aircraft that:
(a) has an MTOM, including payload, of less than 25 kg, in the case of a privately built UAS, or
(b) meets the requirements defined in point (b) of Article 20;
(c) is marked as class C2 and complies with the requirements of that class, as defined in Part 3 of the Annex to Delegated Regulation (EU) 2019/945 and is operated with active and updated direct remote identification system and geo-awareness function or;
(d) is marked as class C3 and complies with the requirements of that class, as defined in Part 4 of the Annex to Delegated Regulation (EU) 2019/945 and is operated with active and updated direct remote identification system and geo-awareness function; or
(e) is marked as class C4 and complies with the requirements of that class, as defined in Part 5 of the Annex to Delegated Regulation (EU) 2019/945.

#### Result 3
Citation: [easa-amc-gm | AMC1 UAS.OPEN.040(1) Operations in subcategory A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.040(1) Operations in subcategory A3
AREAS WHERE UAS OPERATIONS IN A3 MAY BE CONDUCTED
(a) If an uninvolved person enters the range of the UAS operation, the remote pilot should, where necessary, adjust the operation to ensure the safety of the uninvolved person and discontinue the operation if the safety of the UAS operation is not ensured.
(b) A minimum horizontal distance from the person that is passing the area could be estimated as follows:
(1) no less than 30 m;
(2) no less than the height (‘1:1 rule’, i.e. if the UA is flying at a height of 30 m, the distance of the UA from the uninvolved person should be at least 30 m), and
(3) no less than the distance that the UA would cover in 2 seconds at the maximum speed (this assumes a reaction time of 2 seconds).
This minimum horizontal distance is intended to protect people on the ground, but can be extended to property and animals.

#### Result 4
Citation: [easa-amc-gm | GM1 UAS.OPEN.030(1) UAS operations in subcategory A2]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 UAS.OPEN.030(1) UAS operations in subcategory A2
SAFE DISTANCE FROM UNINVOLVED PERSONS
The safe distance of the UA from uninvolved persons is variable and is heavily dependent on the performance and characteristics of the UAS involved, the weather conditions and the segregation of the overflown area. The remote pilot is ultimately responsible for the determination of this distance.

#### Result 5
Citation: [reg-2019-947 | UAS.OPEN.030 UAS operations in subcategory A2]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.030 UAS operations in subcategory A2
UAS operations in subcategory A2 shall comply with all of the following conditions:
(1) be conducted in such a way that the unmanned aircraft does not overfly uninvolved persons and the UAS operations take place at a safe horizontal distance of at least 30 metres from them; the remote pilot may reduce the horizontal safety distance down to a minimum of 5 metres from an uninvolved person when operating an unmanned aircraft with an active low speed mode function and after evaluation of the situation regarding:
(a) weather conditions,
(b) performance of the unmanned aircraft,
(c) segregation of the overflown area.
(2) be performed by a remote pilot who is familiar with manufacturer’s instructions provided by the manufacturer of the UAS and holds a certificate of remote pilot competency issued by the competent authority or by an entity designated by the competent authority of a Member State. This certificate shall be obtained after complying with all of the following conditions and in the order indicated:
(a) completing an online training course and passed the online theoretical knowledge examination as referred to in point (4)(b) of point UAS.OPEN.020;
(b) completing a self-practical training in the operating conditions of the subcategory A3 set out in points (1) and (2) of point UAS.OPEN.040;
(c) declaring the completion of the self-practical training defined in point (b) and passing an additional theoretical knowledge examination provided by the competent authority or at an entity designated by the competent authority of a Member State achieving at least 75% of the overall marks. The examination shall comprise at least 30 multiple-choice questions aimed at assessing the remote pilot’s knowledge of the technical and operational mitigations for ground risk, distributed appropriately across the following subjects:
(i) meteorology;
(ii) UAS flight performance;
(iii) technical and operational mitigations for ground risk.
(3) be performed with an unmanned aircraft which is marked as class C2 and complies with the requirements of that class, as defined in Part 3 of the Annex to Delegated Regulation (EU) 2019/945, and is operated with active and updated direct remote identification system and geo-awareness function.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q05 (single)

**Question:** What is the minimum horizontal distance from uninvolved people in subcategory A2?

**Reference:** At least 30 metres; it can be reduced to a minimum of 5 metres with an active low-speed mode and after evaluating weather, UA performance and segregation of the area. The UA must never overfly uninvolved persons.

**Agent answer:**

The standard minimum horizontal distance from uninvolved persons in subcategory A2 is **30 metres** [reg-2019-947 | UAS.OPEN.030].

However, the distance may be reduced:
* **Down to a minimum of 5 metres** if the unmanned aircraft has an active low-speed mode function set to 3 metres per second, and after the remote pilot evaluates the weather conditions, UA performance, and area segregation [reg-2019-947 | UAS.OPEN.030].
* As an operational reference (Acceptable Means of Compliance), the remote pilot should also follow the **'1:1 rule'** (keeping a lateral distance from any uninvolved person that is not shorter than the current flight height, e.g. a 30 m height requires at least a 30 m distance) [easa-amc-gm | AMC1 UAS.OPEN.030(1)].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | AMC1 UAS.OPEN.030(1) UAS operations in subcategory A2]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.030(1) UAS operations in subcategory A2
SAFE DISTANCE FROM UNINVOLVED PERSONS
(a) The minimum horizontal distance of the UA from uninvolved persons should be defined as the distance between the points where the UA would hit the ground in the event of a vertical fall and the position of the uninvolved persons.
(b) As a reference, when the UA is operating in close proximity to people, the remote pilot should keep the UA at a lateral distance from any uninvolved person that is not shorter than the height (‘1:1 rule’, i.e. if the UA is flying at a height of 30 m, the distance from any uninvolved person should be at least 30 m).
(c) In any case, the distance from uninvolved persons should always be greater than:
(1) 5 m, when the low-speed mode function on the UA is activated and set to 3 m per second;
(2) 5 m, when operating a UAS balloon or airship; or
(3) 30 m in all other cases.

#### Result 2
Citation: [easa-amc-gm | GM1 UAS.OPEN.030(1) UAS operations in subcategory A2]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 UAS.OPEN.030(1) UAS operations in subcategory A2
SAFE DISTANCE FROM UNINVOLVED PERSONS
The safe distance of the UA from uninvolved persons is variable and is heavily dependent on the performance and characteristics of the UAS involved, the weather conditions and the segregation of the overflown area. The remote pilot is ultimately responsible for the determination of this distance.

#### Result 3
Citation: [easa-amc-gm | GM1 UAS.OPEN.030(1) and UAS.OPEN.040(1) UAS operations in subcategories A1 and A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 UAS.OPEN.030(1) and UAS.OPEN.040(1) UAS operations in subcategories A1 and A3
DIFFERENCE BETWEEN SUB-CATEGORIES A2 AND A3
Subcategory A2 addresses operations during which flying close to people is intended for a significant portion of the flight. The minimum distance ranges from 30 m to 5 m from uninvolved people. 5 m is only allowed when there is an active low-speed mode function on the UA, and the remote pilot has conducted an evaluation of the situation regarding the weather, the performance of the UA and the segregation of the overflown area.
Sub-category A3 addresses operations that are conducted in an area (hereafter referred to as ‘the area’) where the remote pilot reasonably expects that no uninvolved people will be endangered within the range of the unmanned aircraft where it is flown during the mission. In addition, the operation must be conducted at a safe horizontal distance of at least 150 m from residential, commercial, industrial or recreational areas.

#### Result 4
Citation: [reg-2019-947 | UAS.OPEN.030 UAS operations in subcategory A2]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.030 UAS operations in subcategory A2
UAS operations in subcategory A2 shall comply with all of the following conditions:
(1) be conducted in such a way that the unmanned aircraft does not overfly uninvolved persons and the UAS operations take place at a safe horizontal distance of at least 30 metres from them; the remote pilot may reduce the horizontal safety distance down to a minimum of 5 metres from an uninvolved person when operating an unmanned aircraft with an active low speed mode function and after evaluation of the situation regarding:
(a) weather conditions,
(b) performance of the unmanned aircraft,
(c) segregation of the overflown area.
(2) be performed by a remote pilot who is familiar with manufacturer’s instructions provided by the manufacturer of the UAS and holds a certificate of remote pilot competency issued by the competent authority or by an entity designated by the competent authority of a Member State. This certificate shall be obtained after complying with all of the following conditions and in the order indicated:
(a) completing an online training course and passed the online theoretical knowledge examination as referred to in point (4)(b) of point UAS.OPEN.020;
(b) completing a self-practical training in the operating conditions of the subcategory A3 set out in points (1) and (2) of point UAS.OPEN.040;
(c) declaring the completion of the self-practical training defined in point (b) and passing an additional theoretical knowledge examination provided by the competent authority or at an entity designated by the competent authority of a Member State achieving at least 75% of the overall marks. The examination shall comprise at least 30 multiple-choice questions aimed at assessing the remote pilot’s knowledge of the technical and operational mitigations for ground risk, distributed appropriately across the following subjects:
(i) meteorology;
(ii) UAS flight performance;
(iii) technical and operational mitigations for ground risk.
(3) be performed with an unmanned aircraft which is marked as class C2 and complies with the requirements of that class, as defined in Part 3 of the Annex to Delegated Regulation (EU) 2019/945, and is operated with active and updated direct remote identification system and geo-awareness function.

#### Result 5
Citation: [easa-amc-gm | AMC1 UAS.OPEN.040(1) Operations in subcategory A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.040(1) Operations in subcategory A3
AREAS WHERE UAS OPERATIONS IN A3 MAY BE CONDUCTED
(a) If an uninvolved person enters the range of the UAS operation, the remote pilot should, where necessary, adjust the operation to ensure the safety of the uninvolved person and discontinue the operation if the safety of the UAS operation is not ensured.
(b) A minimum horizontal distance from the person that is passing the area could be estimated as follows:
(1) no less than 30 m;
(2) no less than the height (‘1:1 rule’, i.e. if the UA is flying at a height of 30 m, the distance of the UA from the uninvolved person should be at least 30 m), and
(3) no less than the distance that the UA would cover in 2 seconds at the maximum speed (this assumes a reaction time of 2 seconds).
This minimum horizontal distance is intended to protect people on the ground, but can be extended to property and animals.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q06 (single)

**Question:** How long is my online theoretical competency certificate valid?

**Reference:** It is valid for five years; revalidation is by demonstrating competency again or completing a refresher training.

**Agent answer:**

Your online theoretical competency certificate is valid for **five years** [reg-2019-947 | UAS.OPEN.070 Duration and validity of the remote pilot online theoretical competency and certificates of remote pilot competency].

Within its validity period, it can be revalidated by:
* demonstrating the required competencies again; or
* completing a refresher training addressing the relevant theoretical knowledge subjects provided by the competent authority or an entity designated by it [reg-2019-947 | UAS.OPEN.070 Duration and validity of the remote pilot online theoretical competency and certificates of remote pilot competency].

If the certificate expires, you must demonstrate your competencies again to revalidate it [reg-2019-947 | UAS.OPEN.070 Duration and validity of the remote pilot online theoretical competency and certificates of remote pilot competency].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | AMC1 UAS.OPEN.020(4)(b) and UAS.OPEN.040(3) UAS operations in subcategories A1 and A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.020(4)(b) and UAS.OPEN.040(3) UAS operations in subcategories A1 and A3 (part 1/4)
THEORETICAL KNOWLEDGE SUBJECTS FOR BASIC ONLINE THEORETICAL KNOWLEGDE TRAINING COURSES AND THEORETICAL KNOWLEGDE EXAMINATIONS FOR SUBCATEGORIES A1 AND A3
The acquisition of theoretical knowledge by the remote pilot should cover at least the following theoretical knowledge subjects:
(a) Air safety:
(1) non-reckless behaviour, safety precautions for UAS operations and basic requirements regarding dangerous goods;
(2) starting or stopping the operations taking into account environmental factors, UAS conditions and limitations, remote pilot limitations and human factors;
(3) operation in visual line of sight (VLOS) and in very low level (VLL), which entails:
(i) keeping a safe distance from people, animals, property, vehicles, and other airspace users;
(ii) the identification of assemblies of people;
(iii) a code of conduct in case the UA encounters other traffic;
(iv) respecting the height limitation; and
(v) when using a UA observer, the responsibilities and communication between the UA observer and the remote pilot; and
(4) familiarisation with the operating environment, in particular:
(i) how to perform the evaluations of the presence of uninvolved person in the overflown area as required in UAS.OPEN.020(1) and UAS.OPEN.040(1); and
(ii) informing the people involved;
(b) Airspace restrictions:
(1) obtain and observe updated information about any flight restrictions or conditions published by the MS according to Article 15 of the UAS Regulation;
(2) describe the types of geographical zones and the procedures for receiving a flight authorisation; and
(3) upload the geographical zones onto the geo-awareness system;
(c) Aviation regulations:
(1) Introduction to EASA and the aviation system;

#### Result 2
Citation: [easa-amc-gm | AMC2 UAS.OPEN.020(4)(b) and UAS.OPEN.040(3) UAS operations in subcategories A1 and A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC2 UAS.OPEN.020(4)(b) and UAS.OPEN.040(3) UAS operations in subcategories A1 and A3
PROOF OF COMPLETION OF THE ONLINE THEORETICAL KNOWLEGDE TRAINING COURSE AND SUCCESSFUL COMPLETION OF THE ONLINE THEORETICAL KNOWLEGDE EXAMINATION
Upon receipt of the proof that a remote pilot has successfully completed the online theoretical knowledge training course and the online theoretical knowledge examination, the competent authority should provide a proof of completion to the remote pilot in the format that is depicted in the figure below. An entity that is designated by the competent authority may issue the certificate on behalf of the competent authority. The proof may be provided in electronic form.
The remote pilot identification number that is provided by the competent authority or the entity that is designated by the competent authority that issues the proof of completion should have the following format:
NNN-RP-xxxxxxxxxxxx
Where:
‘NNN’ is the ISO 3166 Alpha-3 code of the MS that issues the proof of completion;
‘RP’ is a fixed field meaning ‘remote pilot’; and
‘xxxxxxxxxxxx’ are 12 alphanumeric characters (lower-case only) defined by the competent authority or the entity that is designated by the competent authority that issues the proof of completion.
Example: (FIN-RP-123456789abc)
The QR code provided a link to the national database where the information related to the remote pilot is stored. Through the ‘remote pilot identification number’, all information related to the training of the remote pilot can be retrieved by authorised bodies (e.g. competent authorities, law enforcement authorities, etc.) and authorised personnel.

#### Result 3
Citation: [reg-2019-947 | UAS.OPEN.070 Duration and validity of the remote pilot online theoretical competency and certificates of remote pilot competency]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.070 Duration and validity of the remote pilot online theoretical competency and certificates of remote pilot competency
(1) The remote pilot online theoretical competency, required by points (4)(b) of point UAS.OPEN.020 and point (3) of point UAS.OPEN.040, and the certificate of remote pilot competency, required by point (2) of point UAS.OPEN.030, shall be valid for five years.
(2) The revalidation of the remote pilot online theoretical competency and of the certificate of remote pilot competency is, within its validity period, subject to:
(a) demonstration of competencies respectively in accordance with point (4)(b) of point UAS.OPEN.020 or point (2) of point UAS.OPEN.030; or
(b) the completion of a refresher training addressing respectively the theoretical knowledge subjects as defined in point (4)(b) of point UAS.OPEN.020 or point (2) of point UAS.OPEN.030 provided by the competent authority or by an entity designated by the competent authority.
(3) In order to revalidate the remote pilot online theoretical competency or the certificate of remote pilot competency upon its expiration, the remote pilot shall comply with point (2)(a).

#### Result 4
Citation: [easa-amc-gm | AMC2 UAS.OPEN.030(2)(c) UAS operations in subcategory A2 and Attachment A to Chapter I of Appendix 1 ‘Remote pilot theoretical knowledge and practical-skills examination for STS-01’]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC2 UAS.OPEN.030(2)(c) UAS operations in subcategory A2 and Attachment A to Chapter I of Appendix 1 ‘Remote pilot theoretical knowledge and practical-skills examination for STS-01’
THEORETICAL KNOWLEDGE EXAMINATION FOR THE CERTIFICATE OF REMOTE PILOT COMPETENCY AND OF THE REMOTE PILOT THEORETICAL KNOWLEDGE FOR STSs
The theoretical knowledge examination to obtain a ‘certificate of remote pilot competency’ in subcategory A2 of the ‘open’ category (according to point UAS.OPEN.030(2)(c)) and the ‘certificate of remote pilot theoretical knowledge’ for STSs (as per Attachment A to Chapter I of Appendix 1 of the UAS Regulation) should be conducted:
(1) as a face-to-face examination at the facilities of the competent authority, or of the entity that is designated by the competent authority (if that entity issues the certificate), or of the entity recognised by the competent authority (if the certificate is issued by the competent authority); or
(2) through an online-proctored examination provided by the competent authority, or the entity that is designated by the competent authority (if that entity issues the certificate), or the entity recognised by the competent authority (if the certificate is issued by the competent authority). The examination provider should provide the participants in the exam with a clear procedure on how to conduct such an examination as well as with a system that:
(a) allows the adequate verification of the identity of the person that takes the examination;
(b) provides a method to verify that the person that takes the examination does not use during the examination support other than that specified in the examination procedure (e.g. computer traffic data lock and monitoring to prevent screen sharing, mirroring and remote desktop, video and room sound analysis).

#### Result 5
Citation: [easa-amc-gm | AMC1 UAS.STS-01.020(1)(e)(i) UAS operations in STS-01 and UAS.STS-02.020(7)(a) UAS operations in STS-02]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.STS-01.020(1)(e)(i) UAS operations in STS-01 and UAS.STS-02.020(7)(a) UAS operations in STS-02
CERTIFICATE OF REMOTE PILOT THEORETICAL KNOWLEDGE
Upon receipt of proof that the remote pilot has successfully completed the theoretical knowledge examination, the competent authority or the entity that is designated by the competent authority should provide the remote pilot with a certificate of remote pilot theoretical knowledge in the format that is depicted in the figure below. The certificate may be provided in electronic form.
The remote pilot identification number that is provided by the competent authority, or the entity that is designated by the competent authority, which issues the certificate of remote pilot theoretical knowledge should have the following format:
NNN-RP-xxxxxxxxxxxx
Where:
‘NNN’ is the ISO 3166 Alpha-3 code of the competent authority that issues the proof of completion;
‘RP’ is a fixed field meaning ‘remote pilot’; and
‘xxxxxxxxxxxx’ are 12 alphanumeric characters (lower-case only) defined by the competent authority that issues the proof of completion.
Example: (FIN-RP-123456789abc)
The QR code provides a link to the national database where the information related to the remote pilot is stored. Through the ‘remote pilot identification number’, all information related to the training of the remote pilot can be retrieved by authorised bodies (e.g. competent authorities, law enforcement authorities, etc.) and authorised personnel.
If the remote pilot provides the declaration of the practical-skills self-training as defined in point UAS.OPEN.030(2)(c), before passing the theoretical knowledge examination, the competent authority may include in the certificate also ‘subcategory A2’.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q07 (single)

**Question:** What score do I need to pass the online exam for A1/A3 and how many questions does it have?

**Reference:** The exam has 40 multiple-choice questions and the pass mark is at least 75% of the overall marks.

**Agent answer:**

To pass the online theoretical knowledge examination for subcategories A1/A3, you need:

* **Passing score:** At least **75%** of the overall marks [reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1].
* **Number of questions:** **40** multiple-choice questions [reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | AMC1 UAS.OPEN.020(4)(b) and UAS.OPEN.040(3) UAS operations in subcategories A1 and A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.020(4)(b) and UAS.OPEN.040(3) UAS operations in subcategories A1 and A3 (part 1/4)
THEORETICAL KNOWLEDGE SUBJECTS FOR BASIC ONLINE THEORETICAL KNOWLEGDE TRAINING COURSES AND THEORETICAL KNOWLEGDE EXAMINATIONS FOR SUBCATEGORIES A1 AND A3
The acquisition of theoretical knowledge by the remote pilot should cover at least the following theoretical knowledge subjects:
(a) Air safety:
(1) non-reckless behaviour, safety precautions for UAS operations and basic requirements regarding dangerous goods;
(2) starting or stopping the operations taking into account environmental factors, UAS conditions and limitations, remote pilot limitations and human factors;
(3) operation in visual line of sight (VLOS) and in very low level (VLL), which entails:
(i) keeping a safe distance from people, animals, property, vehicles, and other airspace users;
(ii) the identification of assemblies of people;
(iii) a code of conduct in case the UA encounters other traffic;
(iv) respecting the height limitation; and
(v) when using a UA observer, the responsibilities and communication between the UA observer and the remote pilot; and
(4) familiarisation with the operating environment, in particular:
(i) how to perform the evaluations of the presence of uninvolved person in the overflown area as required in UAS.OPEN.020(1) and UAS.OPEN.040(1); and
(ii) informing the people involved;
(b) Airspace restrictions:
(1) obtain and observe updated information about any flight restrictions or conditions published by the MS according to Article 15 of the UAS Regulation;
(2) describe the types of geographical zones and the procedures for receiving a flight authorisation; and
(3) upload the geographical zones onto the geo-awareness system;
(c) Aviation regulations:
(1) Introduction to EASA and the aviation system;

#### Result 2
Citation: [reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.020 UAS operations in subcategory A1 (part 2/2)
(b) in the case of an unmanned aircraft class C1, as defined in Part 2 of the Annex to Delegated Regulation (EU) 2019/945, has completed an online training course followed by completing successfully an online theoretical knowledge examination provided by the competent authority or by an entity designated by the competent authority of a Member State achieving at least 75% of the overall marks. The examination shall comprise 40 multiple-choice questions distributed appropriately across the following subjects:
air safety;
airspace restrictions;
aviation regulation;
human performance limitations;
operational procedures;
UAS general knowledge;
privacy and data protection;
insurance;
security.
(5) be performed with an unmanned aircraft that:
(a) has an MTOM, including payload, of less than 250 g and a maximum operating speed of less than 19 m/s, in the case of a privately built UAS; or
(b) meets the requirements defined in point (a) of Article 20;
(c) is marked as class C0 and complies with the requirements of that class, as defined in Part 1 of the Annex to Delegated Regulation (EU) 2019/945; or
(d) is marked as class C1 and complies with the requirements of that class, as defined in Part 2 of the Annex to Delegated Regulation (EU) 2019/945 and is operated with active and updated direct remote identification system and geo-awareness function.

#### Result 3
Citation: [easa-amc-gm | AMC2 UAS.OPEN.020(4)(b) and UAS.OPEN.040(3) UAS operations in subcategories A1 and A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC2 UAS.OPEN.020(4)(b) and UAS.OPEN.040(3) UAS operations in subcategories A1 and A3
PROOF OF COMPLETION OF THE ONLINE THEORETICAL KNOWLEGDE TRAINING COURSE AND SUCCESSFUL COMPLETION OF THE ONLINE THEORETICAL KNOWLEGDE EXAMINATION
Upon receipt of the proof that a remote pilot has successfully completed the online theoretical knowledge training course and the online theoretical knowledge examination, the competent authority should provide a proof of completion to the remote pilot in the format that is depicted in the figure below. An entity that is designated by the competent authority may issue the certificate on behalf of the competent authority. The proof may be provided in electronic form.
The remote pilot identification number that is provided by the competent authority or the entity that is designated by the competent authority that issues the proof of completion should have the following format:
NNN-RP-xxxxxxxxxxxx
Where:
‘NNN’ is the ISO 3166 Alpha-3 code of the MS that issues the proof of completion;
‘RP’ is a fixed field meaning ‘remote pilot’; and
‘xxxxxxxxxxxx’ are 12 alphanumeric characters (lower-case only) defined by the competent authority or the entity that is designated by the competent authority that issues the proof of completion.
Example: (FIN-RP-123456789abc)
The QR code provided a link to the national database where the information related to the remote pilot is stored. Through the ‘remote pilot identification number’, all information related to the training of the remote pilot can be retrieved by authorised bodies (e.g. competent authorities, law enforcement authorities, etc.) and authorised personnel.

#### Result 4
Citation: [easa-amc-gm | AMC2 UAS.OPEN.030(2)(c) UAS operations in subcategory A2 and Attachment A to Chapter I of Appendix 1 ‘Remote pilot theoretical knowledge and practical-skills examination for STS-01’]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC2 UAS.OPEN.030(2)(c) UAS operations in subcategory A2 and Attachment A to Chapter I of Appendix 1 ‘Remote pilot theoretical knowledge and practical-skills examination for STS-01’
THEORETICAL KNOWLEDGE EXAMINATION FOR THE CERTIFICATE OF REMOTE PILOT COMPETENCY AND OF THE REMOTE PILOT THEORETICAL KNOWLEDGE FOR STSs
The theoretical knowledge examination to obtain a ‘certificate of remote pilot competency’ in subcategory A2 of the ‘open’ category (according to point UAS.OPEN.030(2)(c)) and the ‘certificate of remote pilot theoretical knowledge’ for STSs (as per Attachment A to Chapter I of Appendix 1 of the UAS Regulation) should be conducted:
(1) as a face-to-face examination at the facilities of the competent authority, or of the entity that is designated by the competent authority (if that entity issues the certificate), or of the entity recognised by the competent authority (if the certificate is issued by the competent authority); or
(2) through an online-proctored examination provided by the competent authority, or the entity that is designated by the competent authority (if that entity issues the certificate), or the entity recognised by the competent authority (if the certificate is issued by the competent authority). The examination provider should provide the participants in the exam with a clear procedure on how to conduct such an examination as well as with a system that:
(a) allows the adequate verification of the identity of the person that takes the examination;
(b) provides a method to verify that the person that takes the examination does not use during the examination support other than that specified in the examination procedure (e.g. computer traffic data lock and monitoring to prevent screen sharing, mirroring and remote desktop, video and room sound analysis).

#### Result 5
Citation: [reg-2019-947 | UAS.OPEN.040 UAS operations in subcategory A3]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.040 UAS operations in subcategory A3
UAS operations in subcategory A3 shall comply with all of the following conditions:
(1) be conducted in an area where the remote pilot reasonably expects that no uninvolved person will be endangered within the range where the unmanned aircraft is flown during the entire time of the UAS operation;
(2) be conducted at a safe horizontal distance of at least 150 metres from residential, commercial, industrial or recreational areas;
(3) be performed by a remote pilot who is familiar with manufacturer’s instructions provided by the manufacturer of the UAS and who has completed an online training course and passed an online theoretical knowledge examination as defined in point (4)(b) of point UAS.OPEN.020;
(4) be performed with an unmanned aircraft that:
(a) has an MTOM, including payload, of less than 25 kg, in the case of a privately built UAS, or
(b) meets the requirements defined in point (b) of Article 20;
(c) is marked as class C2 and complies with the requirements of that class, as defined in Part 3 of the Annex to Delegated Regulation (EU) 2019/945 and is operated with active and updated direct remote identification system and geo-awareness function or;
(d) is marked as class C3 and complies with the requirements of that class, as defined in Part 4 of the Annex to Delegated Regulation (EU) 2019/945 and is operated with active and updated direct remote identification system and geo-awareness function; or
(e) is marked as class C4 and complies with the requirements of that class, as defined in Part 5 of the Annex to Delegated Regulation (EU) 2019/945.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q08 (single)

**Question:** What is the maximum take-off mass of a class C2 drone?

**Reference:** A class C2 UAS must have an MTOM of less than 4 kg, including payload.

**Agent answer:**

The maximum take-off mass (MTOM) of a class C2 drone is less than 4 kg, including payload [reg-2019-945 | PART 3 — Requirements for a class C2 Unmanned aircraft system].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-945 | PART 3 — Requirements for a class C2 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 3 — Requirements for a class C2 Unmanned aircraft system (part 1/6)
A class C2 UAS bears the following class identification label on the UA:
A class C2 UAS shall comply with the following:
(1) have an MTOM of less than 4 kg, including payload;
(2) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot. If the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(3) be safely controllable with regard to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;
(4) have the requisite mechanical strength for the UA, including any necessary safety factor, and, where appropriate, stability to withstand any stress to which it is subjected to during use without any breakage or deformation that might interfere with its safe flight;
(5) in the case of a tethered UA, have a tensile length of the tether that is less than 50 m and a mechanical strength that is no less than:
(a) for heavier-than-air aircraft, 10 times the weight of the aerodyne at maximum mass;

#### Result 2
Citation: [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 2 — Requirements for a class C1 Unmanned aircraft system (part 1/6)
A class C1 UAS bears the following class identification label on the UA:
A class C1 UAS shall comply with the following:
(1) be made of materials and have performance and physical characteristics such as to ensure that in the event of an impact at terminal velocity with a human head, the energy transmitted to the human head is less than 80 J, or, as an alternative, shall have an MTOM of less than 900 g, including payload;
(2) have a maximum speed in level flight of 19 m/s;
(3) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot; if the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(4) be safely controllable with regards to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;

#### Result 3
Citation: [reg-2019-945 | ]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)


COMMMISSION DELEGATED REGULATION (EU) 2019/945 of 12 March 2019 on unmanned aircraft systems and on third-country operators of unmanned aircraft systems

#### Result 4
Citation: [reg-2019-945 | PART 4 — Requirements for a class C3 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 4 — Requirements for a class C3 Unmanned aircraft system (part 1/6)
A class C3 UAS bears the following class identification label on the UA:
A class C3 UAS shall comply with the following:
(1) have an MTOM of less than 25 kg, including payload, and have a maximum characteristic dimension of less than 3 m;
(2) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot. If the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(3) be safely controllable with regard to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;
(4) in the case of a tethered UA, have a tensile length of the tether that is less than 50 m and a mechanical strength of no less than:
(a) for heavier-than-air aircraft, 10 times the weight of the aerodyne at maximum mass;
(b) for lighter-than-air aircraft, 4 times the force exerted by the combination of the maximum static thrust and the aerodynamic force of the maximum allowed wind speed in flight;

#### Result 5
Citation: [reg-2019-945 | PART 1 — Requirements for a class C0 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 1 — Requirements for a class C0 Unmanned aircraft system (part 1/2)
A class C0 UAS bears the following class identification label on the UA:
A class C0 UAS shall comply with the following:
(1) have an MTOM of less than 250 g, including payload;
(2) have a maximum speed in level flight of 19 m/s;
(3) have a maximum attainable height above the take-off point limited to 120 m;
(4) be safely controllable with regards to stability, manoeuvrability and the command and control link performance, by a remote pilot following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;
(5) be designed and constructed in such a way as to minimise injury to people during operation, sharp edges shall be avoided, unless technically unavoidable under good design and manufacturing practice. If equipped with propellers, the UA shall be designed in such a way as to limit any injury that may be inflicted by the propeller blades;
(6) be exclusively powered by electricity;
(7) if equipped with a follow-me mode and when this function is on, be in a range not exceeding 50 m from the remote pilot, and make it possible for the remote pilot to regain control of the UA;
(8) be placed on the market with manufacturer’s instructions providing:
(a) the characteristics of the UA including but not limited to the:
class of the UA
UA mass (with a description of the reference configuration) and the maximum take-off mass (MTOM);
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q09 (single)

**Question:** What are the mass and speed limits of a class C0 drone?

**Reference:** A C0 drone has an MTOM below 250 g including payload and a maximum level-flight speed of 19 m/s (and a height limit of 120 m above take-off point).

**Agent answer:**

For a class C0 drone under Regulation (EU) 2019/945 (binding law):

* **Mass limit:** Maximum Take-Off Mass (MTOM) of **less than 250 g**, including payload [reg-2019-945 | PART 1 — Requirements for a class C0 Unmanned aircraft system].
* **Speed limit:** Maximum speed in level flight of **19 m/s** [reg-2019-945 | PART 1 — Requirements for a class C0 Unmanned aircraft system].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-945 | PART 1 — Requirements for a class C0 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 1 — Requirements for a class C0 Unmanned aircraft system (part 1/2)
A class C0 UAS bears the following class identification label on the UA:
A class C0 UAS shall comply with the following:
(1) have an MTOM of less than 250 g, including payload;
(2) have a maximum speed in level flight of 19 m/s;
(3) have a maximum attainable height above the take-off point limited to 120 m;
(4) be safely controllable with regards to stability, manoeuvrability and the command and control link performance, by a remote pilot following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;
(5) be designed and constructed in such a way as to minimise injury to people during operation, sharp edges shall be avoided, unless technically unavoidable under good design and manufacturing practice. If equipped with propellers, the UA shall be designed in such a way as to limit any injury that may be inflicted by the propeller blades;
(6) be exclusively powered by electricity;
(7) if equipped with a follow-me mode and when this function is on, be in a range not exceeding 50 m from the remote pilot, and make it possible for the remote pilot to regain control of the UA;
(8) be placed on the market with manufacturer’s instructions providing:
(a) the characteristics of the UA including but not limited to the:
class of the UA
UA mass (with a description of the reference configuration) and the maximum take-off mass (MTOM);

#### Result 2
Citation: [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 2 — Requirements for a class C1 Unmanned aircraft system (part 1/6)
A class C1 UAS bears the following class identification label on the UA:
A class C1 UAS shall comply with the following:
(1) be made of materials and have performance and physical characteristics such as to ensure that in the event of an impact at terminal velocity with a human head, the energy transmitted to the human head is less than 80 J, or, as an alternative, shall have an MTOM of less than 900 g, including payload;
(2) have a maximum speed in level flight of 19 m/s;
(3) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot; if the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(4) be safely controllable with regards to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;

#### Result 3
Citation: [reg-2019-945 | PART 15 — Maximum sound power level per class of UA (including transition periods)]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 15 — Maximum sound power level per class of UA (including transition periods)
UA class | MTOM m in gram | Maximum sound power level LWA in dB
as from entry into force | as from 2 years after entry into force | as from 4 years after entry into force
C1 and C2 | m < 900 | 85 | 83 | 81
C2 | 900 ≤ m < 4 000 | 85 + 18,5 lg | 83 + 18,5 lg | 81 + 18,5 lg
Where ‘lg’ is the base 10 logarithm.

#### Result 4
Citation: [reg-2019-945 | PART 4 — Requirements for a class C3 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 4 — Requirements for a class C3 Unmanned aircraft system (part 1/6)
A class C3 UAS bears the following class identification label on the UA:
A class C3 UAS shall comply with the following:
(1) have an MTOM of less than 25 kg, including payload, and have a maximum characteristic dimension of less than 3 m;
(2) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot. If the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(3) be safely controllable with regard to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;
(4) in the case of a tethered UA, have a tensile length of the tether that is less than 50 m and a mechanical strength of no less than:
(a) for heavier-than-air aircraft, 10 times the weight of the aerodyne at maximum mass;
(b) for lighter-than-air aircraft, 4 times the force exerted by the combination of the maximum static thrust and the aerodynamic force of the maximum allowed wind speed in flight;

#### Result 5
Citation: [reg-2019-945 | PART 17 — Requirements for a class C6 unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 17 — Requirements for a class C6 unmanned aircraft system (part 1/2)
A class C6 UAS bears the following class identification label on the UA:
A class C6 UAS shall comply with the requirements defined in Part 4, except those defined in paragraphs (2), (7) and (10).
In addition, it shall comply with the following requirements:
have a maximum ground speed in level flight of not more than 50 m/s;
if it is equipped with a geo-awareness function, comply with paragraph (10) of Part 4;
during flight, provide the remote pilot with clear and concise information on the geographical position of the UA, its speed and its height above the surface or take-off point;
provide means to prevent the UA from breaching the horizontal and vertical limits of a programmable operational volume;
provide means for the remote pilot to terminate the flight of the UA, which shall:
(a) be reliable, predictable, independent from the automatic flight control and guidance system and independent from the means to prevent the UA from breaching the horizontal and vertical limits as required in point (4); this applies also to the activation of this means; and
(b) force the descent of the UA and prevent its powered horizontal displacement;
provide means to programme the UA trajectory;
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q10 (single)

**Question:** Can I fly a C1 drone over uninvolved people in subcategory A1?

**Reference:** You may not overfly assemblies of people, and you must reasonably expect that no uninvolved person will be overflown. If an unexpected overflight happens, reduce the time over those people as much as possible.

**Agent answer:**

**No**, you must reasonably expect that no uninvolved person will be overflown when using a C1 drone in subcategory A1 [reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1]. 

### Conditions and Rules:
* **Overflying uninvolved people:** Unlike C0 drones or privately built drones under 250 g, C1 drones must not intentionally overfly uninvolved people. Before starting your flight, you must assess the site (e.g., roads, paths, time of day) and ensure you reasonably expect no uninvolved person will be overflown [easa-amc-gm | AMC1 UAS.OPEN.020(1) and (2) UAS operations in subcategory A1].
* **Unexpected overflight:** If an uninvolved person is unexpectedly overflown, you must reduce the duration of the overflight as much as possible, for example by increasing the distance from them or flying the drone to an area where there are no uninvolved people [reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1, easa-amc-gm | AMC1 UAS.OPEN.020(1) and (2) UAS operations in subcategory A1].
* **Assemblies of people:** You must never overfly assemblies of people under any circumstances [reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1].

*(Note: The above points rely on binding regulations and EASA Acceptable Means of Compliance [reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1, easa-amc-gm | AMC1 UAS.OPEN.020(1) and (2) UAS operations in subcategory A1].)*

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | AMC1 UAS.OPEN.020(1) and (2) UAS operations in subcategory A1]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.020(1) and (2) UAS operations in subcategory A1
OPERATIONAL LIMITATIONS IN SUBCATEGORY A1
As a principle, the rules prohibit overflying assemblies of people. Overflying isolated people is possible, but there is a distinction between class C1 and class C0 UAS or privately built UAS with MTOMs of less than 250 g.
(a) For UAS in class C1, before starting the UAS operation, the remote pilot should assess the area and should reasonably expect that no uninvolved person will be overflown. This evaluation should be made taking into account the configuration of the site of operation (e.g. the existence of roads, streets, pedestrian or bicycle paths), and the possibility to secure the site and the time of the day. In case of an unexpected overflight, the remote pilot should reduce as much as possible the duration of the overflight, for example, by flying the UAS in such a way that the distance between the UA and the uninvolved people increases, or by positioning the UAS over a place where there are no uninvolved people.
(b) It is accepted that UAS in class C0 or privately built UAS with MTOMs less than 250 g may fly over uninvolved people; however, this should be avoided whenever possible, and where it is unavoidable, extreme caution should be used.

#### Result 2
Citation: [easa-amc-gm | AMC1 UAS.OPEN.040(1) Operations in subcategory A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.040(1) Operations in subcategory A3
AREAS WHERE UAS OPERATIONS IN A3 MAY BE CONDUCTED
(a) If an uninvolved person enters the range of the UAS operation, the remote pilot should, where necessary, adjust the operation to ensure the safety of the uninvolved person and discontinue the operation if the safety of the UAS operation is not ensured.
(b) A minimum horizontal distance from the person that is passing the area could be estimated as follows:
(1) no less than 30 m;
(2) no less than the height (‘1:1 rule’, i.e. if the UA is flying at a height of 30 m, the distance of the UA from the uninvolved person should be at least 30 m), and
(3) no less than the distance that the UA would cover in 2 seconds at the maximum speed (this assumes a reaction time of 2 seconds).
This minimum horizontal distance is intended to protect people on the ground, but can be extended to property and animals.

#### Result 3
Citation: [easa-amc-gm | AMC1 UAS.OPEN.030(1) UAS operations in subcategory A2]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.030(1) UAS operations in subcategory A2
SAFE DISTANCE FROM UNINVOLVED PERSONS
(a) The minimum horizontal distance of the UA from uninvolved persons should be defined as the distance between the points where the UA would hit the ground in the event of a vertical fall and the position of the uninvolved persons.
(b) As a reference, when the UA is operating in close proximity to people, the remote pilot should keep the UA at a lateral distance from any uninvolved person that is not shorter than the height (‘1:1 rule’, i.e. if the UA is flying at a height of 30 m, the distance from any uninvolved person should be at least 30 m).
(c) In any case, the distance from uninvolved persons should always be greater than:
(1) 5 m, when the low-speed mode function on the UA is activated and set to 3 m per second;
(2) 5 m, when operating a UAS balloon or airship; or
(3) 30 m in all other cases.

#### Result 4
Citation: [easa-amc-gm | GM1 Article 2(18) Definitions]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 Article 2(18) Definitions (part 1/3)
DEFINITION OF ‘UNINVOLVED PERSONS’
Due to the huge variety of possible circumstances, this GM only provides general guidelines.
An uninvolved person is a person that does not take part in the UAS operation, either directly or indirectly, and that could be potentially affected by the UAS operation. Persons protected by a shelter (e.g. a roof) are not considered to be affected by the UAS operation nor exposed to direct risks if the MTOM of the UA is below 25 kg or if the UA complies with the conditions defined in criterion #2 of mitigation M1 of the SORA (refer to point B.2 of Annex B to the SORA).
People that sit at a beach or in a park, or walk on a street or on a road, are also generally considered uninvolved persons.
A person may be considered to be ‘involved’ in the UAS operation when the following conditions are met.
Before the flight, the person:
(a) has given explicit consent (it may be verbal) to the UAS operator or to the remote pilot to be part of the UAS operation (even indirectly as a spectator or just accepting to be overflown by the UAS); and
(b) has received from the UAS operator or from the remote pilot clear instructions and safety precautions to follow in case the UAS exhibits any unplanned behaviour.
UAS operators are responsible for ensuring that all persons involved are able to follow in a timely manner the emergency procedures.

#### Result 5
Citation: [reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.020 UAS operations in subcategory A1 (part 1/2)
UAS operations in subcategory A1 shall comply with all of the following conditions:
(1) for unmanned aircraft referred to in point (5)(d), be conducted in such a way that a remote pilot of the unmanned aircraft does not overfly assemblies of people and reasonably expects that no uninvolved person will be overflown. In the event of unexpected overflight of uninvolved persons, the remote pilot shall reduce as much as possible the time during which the unmanned aircraft overflies those persons;
(2) in the case of an unmanned aircraft referred to in points (5)(a), (5)(b) and (5)(c), be conducted in such a way that the remote pilot of the unmanned aircraft may overfly uninvolved persons, but shall never overfly assemblies of people;
(3) by way of derogation from point (d) of paragraph 1 of Article 4, be conducted, when the followme mode is active, up to a distance of 50 metres from the remote pilot;
(4) be performed by a remote pilot who:
(a) is familiar with manufacturer’s instructions provided by the manufacturer of the UAS;
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q11 (single)

**Question:** What do I need to do with lights if I fly at night in the open category?

**Reference:** When operating at night the remote pilot must ensure that a green flashing light on the unmanned aircraft is activated.

**Agent answer:**

When operating at night in the open category, you must ensure that a **green flashing light** on the unmanned aircraft is activated [reg-2019-947 | UAS.OPEN.060 Responsibilities of the remote pilot].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

Error executing tool search: 1 validation error for searchArguments
query
  Field required [type=missing, input_value={'queries': ['night light...lights night UAS.OPEN']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.14/v/missing
#### Result 1
Citation: [easa-amc-gm | AMC3 UAS.SPEC.050(1)(d) Responsibilities of the UAS operator]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC3 UAS.SPEC.050(1)(d) Responsibilities of the UAS operator (part 4/18)
Turning off the front green flashing light might improve the view because there will be no reflection in the on-board camera. Recognise that the IR camera does not help in case of rain/humidity, and that the IR visibility significantly decreases. Explain the use of the green flashing light at night. Explain the use of navigation lights, position lights, anti-collision lights, and other lights for UA controllability. Explain the use of lights (e.g. navigation, position, or anti-collision lights) for recognising the presence of manned aircraft. Rationale: Those lights show where the UA is positioned and the direction in which the UA is aligned. For manned aircraft, a red navigation light is located on the leading edge of the left-wing tip and a green navigation light on the leading edge of the rightwing tip (for helicopters, on the left and right sides of the cockpit). A white navigation light is positioned on the tail as far aft as possible. High-intensity strobe lights are also located in those positions. They are used as anti-collision lights and flash twice after a short break. A red rotating beacon is also part of the anti-collision lights.
Degradation of visual acuity | Recognise that flying the UA at night degrades visual perception. Recognise night myopia, caused by the increasing pupil size. At low-light levels, without distant objects to focus on, the focusing mechanism of the eye may go to a resting myopic position. If night-vision goggles are used, know how they function.

#### Result 2
Citation: [easa-amc-gm | AMC3 UAS.SPEC.050(1)(d) Responsibilities of the UAS operator]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC3 UAS.SPEC.050(1)(d) Responsibilities of the UAS operator (part 5/18)
Night illusions | Define the term ‘night illusion’. Recognise and overcome visual illusions that are caused by darkness, and understand the physiological conditions that may degrade night vision. State the limitations of night vision techniques at night and by day.
Altered visual-scanning techniques | State the limitations of the different visual-scanning techniques at night and by day. Rationale: Despite the value of electronic means of conflict detection, physical lookout remains an important defence against the loss of visual separation for all types of aircraft. To avoid collisions, the remote pilot should visually scan effectively from the moment the UA starts moving until it comes to a stop at the end of the flight. Collision threats are present everywhere. Before take-off, the remote pilot should visually check the take-off area to ensure that there are no other objects. After take-off, the remote pilot should continue to visually scan to ensure a safe departure of the UA with no obstacles.
Altered identification of obstacles | Explain the effect of obstacles on the take-off distance that is required at night. Rationale: The remote pilot should know the flight area where the UA will fly at night. Objects look different and power lines are nearly invisible at night. It is, therefore, advisable that the remote pilot conduct a test flight during the daytime.
Overflight (flight over known populated areas or over assemblies of people) | Identification of populated areas and assemblies of people | Explain the definition of ‘populated area’ and ‘assemblies of people’.

#### Result 3
Citation: [easa-amc-gm | AMC3 UAS.SPEC.050(1)(d) Responsibilities of the UAS operator]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC3 UAS.SPEC.050(1)(d) Responsibilities of the UAS operator (part 3/18)
Night operations | General | Recognise the meaning of the definition of ‘night’ or other similar wording that is used for night flight. Rationale: In Regulation (EU) No 1178/2011 (the ‘Aircrew Regulation’), ‘night’ for manned aviation ‘means the period between the end of evening civil twilight and the beginning of morning civil twilight or such other period between sunset and sunrise as may be prescribed by the appropriate authority’. Some national laws use the sunset and sunrise times for the definition of a night flight. ‘Sunset’ is defined as the daily disappearance of the upper limb of the sun below the horizon. This time depends on the latitude and longitude of the viewpoint. There are many websites and apps to find out the sunset and sunrise times at a specific location. Recognise the benefits of illuminating the operational area, especially during the critical phases of take-off and landing. Recognise that during night flight it is hard to estimate the distance between the UA and other obstacles if visibility is only ensured by the lights of the UA. Recognise that a visual obstacle avoidance system may be less accurate in night-time operations. Understand that if the sight of the UA is lost at night, return-to-home (RTH) should be immediately followed. Rationale: During daytime, it is sometimes difficult to see the position of the UA, which is even more difficult at night. Recognise that an infrared radiation (IR) camera allows one to see enough at night.

#### Result 4
Citation: [reg-2019-947 | UAS.SPEC.050 Responsibilities of the UAS operator]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.SPEC.050 Responsibilities of the UAS operator (part 4/4)
(iii) using an unmanned aircraft which is designed to minimise noise and other emissions, taking into account the type of the intended operations and geographical areas where the aircraft noise and other emissions are of concern.
(j) establish and keep an up-to-date list of the designated remote pilots for each flight;
(k) establish and keep an up-to-date list of the maintenance staff employed by the operator to carry out maintenance activities; and
(l) ensure that each individual unmanned aircraft is installed with:
(i) at least one green flashing light for the purpose of visibility of the unmanned aircraft at night, and
(ii) an active and up-to-date remote identification system.

#### Result 5
Citation: [reg-2019-947 | UAS.OPEN.060 Responsibilities of the remote pilot]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.060 Responsibilities of the remote pilot (part 2/2)
(b) keep the unmanned aircraft in VLOS and maintain a thorough visual scan of the airspace surrounding the unmanned aircraft in order to avoid any risk of collision with any manned aircraft. The remote pilot shall discontinue the flight if the operation poses a risk to other aircraft, people, animals, environment or property;
(c) comply with the operational limitations in geographical zones defined in accordance with Article 15;
(d) have the ability to maintain control of the unmanned aircraft, except in the case of a lost link or when operating a free-flight unmanned aircraft;
(e) operate the UAS in accordance with manufacturer’s instructions provided by the manufacturer, including any applicable limitations;
(f) comply with the operator’s procedures when available;
(g) when operating at night, ensure that a green flashing light on the unmanned aircraft is activated.
(3) During the flight, remote pilots and UAS operators shall not fly close to or inside areas where an emergency response effort is ongoing unless they have permission to do so from the responsible emergency response services.
(4) For the purposes of point (2)(b), remote pilots may be assisted by an unmanned aircraft observer. In such case, clear and effective communication shall be established between the remote pilot and the unmanned aircraft observer.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q12 (single)

**Question:** Where do I have to display my operator registration number on the drone?

**Reference:** On the UA, readable at least on the ground without devices other than corrective lenses. A QR code is allowed, and if the UA is too small a marking inside an accessible battery compartment is acceptable.

**Agent answer:**

You must display your UAS operator registration number on every unmanned aircraft that requires registration (such as those with a MTOM of 250 g or more, or equipped with a camera/sensor capturing personal data, and all drones in the specific category) [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]. 

According to EASA's Acceptable Means of Compliance (AMC), the display must meet the following requirements:

* **Visibility:** The number must be displayed on the unmanned aircraft in a way that is readable at least when the aircraft is on the ground, without using devices other than eyeglasses or corrective lenses [easa-amc-gm | AMC1 Article 14(8) Registration of UAS operators and ‘certified’ UAS].
* **Format:** A Quick Response (QR) code may also be used [easa-amc-gm | AMC1 Article 14(8)].
* **Exceptions for size or scale models:** If the size of the aircraft does not allow the mark to be displayed in a visible way on the fuselage, or if the drone represents a real aircraft where affixing the marking on the exterior would spoil the realism of the representation, placing the marking inside an accessible battery compartment is acceptable [easa-amc-gm | AMC1 Article 14(8)].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | AMC1 Article 14(8) Registration of UAS operators and ‘certified’ UAS]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 14(8) Registration of UAS operators and ‘certified’ UAS
DISPLAY OF REGISTRATION INFORMATION
(a) If the UAS operator owns the UAS or uses a UAS that is owned by a third party, it should:
(1) register itself;
(2) display on the UA the UAS operator registration number, which is received at the end of the registration process, in a way that the number is readable at least when the UA is on the ground, without using other devices than eyeglasses or corrective lenses; and
(3) upload the full string, which consists of the UAS operator registration number and the three (3) randomly generated alphanumerics, into the electronic identification system, if available.
(b) A QR code (quick response code) may be used.
(c) If the size of the UA does not allow the mark to be displayed in a visible way on the fuselage, or the UA represents a real aircraft where affixing the marking on the UA would spoil the realism of the representation, a marking inside the battery compartment is acceptable if the compartment is accessible.

#### Result 2
Citation: [easa-amc-gm | GM1 to AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 to AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS
UAS OPERATOR REGISTRATION NUMBER
An example of a UAS operator registration number as defined in point (a) of AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS is ‘FIN87astrdge12k8’, where:
‘FIN’ is the ISO 3166 Alpha-3 code of Finland;
‘87astrdge12k’ is an example of the twelve (12) alphanumerics, as defined in point (a)(2) of AMC1 Article 14(6); and
‘8’ is the checksum, i.e. the result of the application of the Luhn-mod-36 algorithm to the fifteen (15) alphanumerics that result from the concatenation of the twelve (12) alphanumerics of the UAS operator registration number and the three (3) randomly generated alphanumerics (‘secret digits’, as defined in point (b) of AMC1 Article 14(6)): ‘87astrdge12kxyz’.
An example of the full registration string, as defined in point (e) of AMC1 Article 14(6), to be provided by a Member State, is ‘FIN87astrdge12k8-xyz’, where:
‘FIN87astrdge12k8’ is the UAS operator registration number; and
‘xyz’ is an example of the three (3) randomly generated ‘secret digits’.
The UAS operator must upload the UAS registration number and the three (3) ‘secret digits’ into the remote identification system of the UAS, if available, or into the electronic-identification system, if required by the geographical zone.
The UAS operator should not share with anybody the three (3) ‘secret digits’ that are used to enhance the protection of the UAS operator registration number from being illegally uploaded into a UA.

#### Result 3
Citation: [easa-amc-gm | AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS
UAS OPERATOR REGISTRATION NUMBER
(a) The unique UAS operator digital registration number that is issued by the Member States should consist of sixteen (16) alphanumerics in total, arranged as follows:
(1) the first three (3) alphanumerics (upper-case only) corresponding to the ISO 3166 Alpha3 code of the Member State of registration;
(2) followed by twelve (12) randomly generated characters that consist of alphanumerics (lower-case only); and
(3) one (1) character corresponding to the checksum that is generated in line with point (c).
(b) The Member States should randomly generate three (3) additional alphanumerics (lower-case only) called ‘secret digits’.
(c) The Member States should generate a checksum by applying the Luhn-mod-36 algorithm to the fifteen (15) alphanumerics that result from the concatenation, in the following order, of:
(1) the twelve (12) alphanumerics of the UAS operator registration number defined in point (a)(2); and
(2) the three (3) randomly generated ‘secret digits’ that are defined in point (b).
(d) For the Luhn-mod-36 algorithm, the mapping of the alphanumerics to the code-points should start with digits that are followed by lower-case letters, as shown below:
Alphanumeric | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | a | b | c | d | e | f | … | z
Code-point | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | … | 35
(e) At the time of registration, the Member State should provide the UAS operator with the full registration string that consists, in the following order, of:
(1) the UAS operator registration number as defined in point (a); and
(2) the three (3) randomly generated ‘secret digits’, separated by a hyphen ‘-’ (ASCII code [DEC] 45).

#### Result 4
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 3/3)
The nationality and registration mark of an unmanned aircraft shall be established in line with ICAO Annex 7. An unmanned aircraft cannot be registered in more than one State at a time.
8. The UAS operators shall display their registration number on every unmanned aircraft meeting the conditions described in paragraph 5.
9. In addition to the data defined in point (2) Member States may collect additional identity information from the UAS operators.

#### Result 5
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 2/3)
4. Member States shall ensure that registration systems are digital and interoperable and allow for mutual access and exchange of information through the repository referred to in Article 74 of Regulation (EU) 2018/1139.
5. UAS operators shall register themselves:
(a) when operating within the ‘open’ category any of the following unmanned aircraft:
i. with a MTOM of 250 g or more, or, which in the case of an impact can transfer to a human kinetic energy above 80 Joules;
ii. that is equipped with a sensor able to capture personal data, unless it complies with Directive 2009/48/EC.
(b) when operating within the ‘specific’ category an unmanned aircraft of any mass.
6. UAS operators shall register themselves in the Member State where they have their residence for natural persons or where they have their principal place of business for legal persons and ensure that their registration information is accurate. A UAS operator cannot be registered in more than one Member State at a time.
Member States shall issue a unique digital registration number for UAS operators and for the UAS that require registration, allowing their individual identification.
The registration number for UAS operators shall be established on the basis of standards that support the interoperability of the registration systems;
7. The owner of an unmanned aircraft whose design is subject to certification shall register the unmanned aircraft.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q13 (single)

**Question:** What format does the operator registration number have?

**Reference:** 16 alphanumerics: 3 upper-case letters with the ISO 3166 Alpha-3 country code, 12 random lower-case alphanumerics and 1 checksum character; the user also receives 3 secret digits after a hyphen.

**Agent answer:**

The UAS operator registration number consists of 16 alphanumeric characters in total, arranged as follows [easa-amc-gm | AMC1 Article 14(6)]:

1.  **First 3 characters:** The ISO 3166 Alpha-3 code of the Member State of registration (upper-case only).
2.  **Next 12 characters:** Randomly generated characters (lower-case only).
3.  **Last character:** A checksum character generated using the Luhn-mod-36 algorithm.

When you register, your Member State will provide you with a "full registration string" to be used for electronic identification. This string consists of your 16-character registration number, followed by a hyphen and three additional randomly generated "secret digits" (e.g., `FIN87astrdge12k8-xyz`) [easa-amc-gm | GM1 to AMC1 Article 14(6); easa-amc-gm | AMC1 Article 14(6)].

You must display the 16-character registration number on your unmanned aircraft so that it is readable when the aircraft is on the ground (without using devices other than eyeglasses). The full string (including the secret digits) must be uploaded into the electronic identification system if your drone is equipped with one [easa-amc-gm | AMC1 Article 14(8)]. You should not share the three "secret digits" with anyone [easa-amc-gm | GM1 to AMC1 Article 14(6)].

*Note: This information is based on EASA Acceptable Means of Compliance (AMC) and Guidance Material (GM), which provide accepted ways to comply with the requirements of Regulation (EU) 2019/947 [easa-amc-gm | AMC1 Article 14(6)].*

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | GM1 to AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 to AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS
UAS OPERATOR REGISTRATION NUMBER
An example of a UAS operator registration number as defined in point (a) of AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS is ‘FIN87astrdge12k8’, where:
‘FIN’ is the ISO 3166 Alpha-3 code of Finland;
‘87astrdge12k’ is an example of the twelve (12) alphanumerics, as defined in point (a)(2) of AMC1 Article 14(6); and
‘8’ is the checksum, i.e. the result of the application of the Luhn-mod-36 algorithm to the fifteen (15) alphanumerics that result from the concatenation of the twelve (12) alphanumerics of the UAS operator registration number and the three (3) randomly generated alphanumerics (‘secret digits’, as defined in point (b) of AMC1 Article 14(6)): ‘87astrdge12kxyz’.
An example of the full registration string, as defined in point (e) of AMC1 Article 14(6), to be provided by a Member State, is ‘FIN87astrdge12k8-xyz’, where:
‘FIN87astrdge12k8’ is the UAS operator registration number; and
‘xyz’ is an example of the three (3) randomly generated ‘secret digits’.
The UAS operator must upload the UAS registration number and the three (3) ‘secret digits’ into the remote identification system of the UAS, if available, or into the electronic-identification system, if required by the geographical zone.
The UAS operator should not share with anybody the three (3) ‘secret digits’ that are used to enhance the protection of the UAS operator registration number from being illegally uploaded into a UA.

#### Result 2
Citation: [easa-amc-gm | AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS
UAS OPERATOR REGISTRATION NUMBER
(a) The unique UAS operator digital registration number that is issued by the Member States should consist of sixteen (16) alphanumerics in total, arranged as follows:
(1) the first three (3) alphanumerics (upper-case only) corresponding to the ISO 3166 Alpha3 code of the Member State of registration;
(2) followed by twelve (12) randomly generated characters that consist of alphanumerics (lower-case only); and
(3) one (1) character corresponding to the checksum that is generated in line with point (c).
(b) The Member States should randomly generate three (3) additional alphanumerics (lower-case only) called ‘secret digits’.
(c) The Member States should generate a checksum by applying the Luhn-mod-36 algorithm to the fifteen (15) alphanumerics that result from the concatenation, in the following order, of:
(1) the twelve (12) alphanumerics of the UAS operator registration number defined in point (a)(2); and
(2) the three (3) randomly generated ‘secret digits’ that are defined in point (b).
(d) For the Luhn-mod-36 algorithm, the mapping of the alphanumerics to the code-points should start with digits that are followed by lower-case letters, as shown below:
Alphanumeric | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | a | b | c | d | e | f | … | z
Code-point | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | … | 35
(e) At the time of registration, the Member State should provide the UAS operator with the full registration string that consists, in the following order, of:
(1) the UAS operator registration number as defined in point (a); and
(2) the three (3) randomly generated ‘secret digits’, separated by a hyphen ‘-’ (ASCII code [DEC] 45).

#### Result 3
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 2/3)
4. Member States shall ensure that registration systems are digital and interoperable and allow for mutual access and exchange of information through the repository referred to in Article 74 of Regulation (EU) 2018/1139.
5. UAS operators shall register themselves:
(a) when operating within the ‘open’ category any of the following unmanned aircraft:
i. with a MTOM of 250 g or more, or, which in the case of an impact can transfer to a human kinetic energy above 80 Joules;
ii. that is equipped with a sensor able to capture personal data, unless it complies with Directive 2009/48/EC.
(b) when operating within the ‘specific’ category an unmanned aircraft of any mass.
6. UAS operators shall register themselves in the Member State where they have their residence for natural persons or where they have their principal place of business for legal persons and ensure that their registration information is accurate. A UAS operator cannot be registered in more than one Member State at a time.
Member States shall issue a unique digital registration number for UAS operators and for the UAS that require registration, allowing their individual identification.
The registration number for UAS operators shall be established on the basis of standards that support the interoperability of the registration systems;
7. The owner of an unmanned aircraft whose design is subject to certification shall register the unmanned aircraft.

#### Result 4
Citation: [easa-amc-gm | AMC1 Article 14(8) Registration of UAS operators and ‘certified’ UAS]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 14(8) Registration of UAS operators and ‘certified’ UAS
DISPLAY OF REGISTRATION INFORMATION
(a) If the UAS operator owns the UAS or uses a UAS that is owned by a third party, it should:
(1) register itself;
(2) display on the UA the UAS operator registration number, which is received at the end of the registration process, in a way that the number is readable at least when the UA is on the ground, without using other devices than eyeglasses or corrective lenses; and
(3) upload the full string, which consists of the UAS operator registration number and the three (3) randomly generated alphanumerics, into the electronic identification system, if available.
(b) A QR code (quick response code) may be used.
(c) If the size of the UA does not allow the mark to be displayed in a visible way on the fuselage, or the UA represents a real aircraft where affixing the marking on the UA would spoil the realism of the representation, a marking inside the battery compartment is acceptable if the compartment is accessible.

#### Result 5
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 1/3)
1. Member States shall establish and maintain accurate registration systems for UAS whose design is subject to certification and for UAS operators whose operation may present a risk to safety, security, privacy, and protection of personal data or environment.
2. The registration systems for UAS operators shall provide the fields for introducing and exchanging the following information:
(a) the full name and the date of birth for natural persons and the name and their identification number for legal persons;
(b) the address of UAS operators;
(c) their email address and telephone number;
(d) an insurance policy number for UAS if required by Union or national law;
(e) the confirmation by legal persons of the following statement: ‘All personnel directly involved in the operations are competent to perform their tasks, and the UAS will be operated only by remote pilots with the appropriate level of competency’;
(f) operational authorisations and LUCs held and declarations followed by a confirmation in accordance with Article 12(5)(b).
3. The registration systems for unmanned aircraft whose design is subject to certification shall provide the fields for introducing and exchanging the following information:
(a) manufacturer’s name;
(b) manufacturer’s designation of the unmanned aircraft;
(c) unmanned aircraft’s serial number;
(d) full name, address, email address and telephone number of the natural or legal person under whose name the unmanned aircraft is registered.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q14 (single)

**Question:** Can I carry dangerous goods or drop material from a drone in the open category?

**Reference:** No. In the open category the unmanned aircraft must not carry dangerous goods and must not drop any material.

**Agent answer:**

No, you cannot carry dangerous goods or drop any material from a drone in the open category, as it is required that during flight, the unmanned aircraft does not carry dangerous goods and does not drop any material [reg-2019-947 | Article 4 - ‘Open’ category of UAS operations].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** citation check failed: [reg-2019-947 | Article 4(1)(f)] is not one of the passages you retrieved; citation check passed after one retry; national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | GM1 Article 2(11) Definitions]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 Article 2(11) Definitions
DEFINITION OF ‘DANGEROUS GOODS’
The definition of ‘dangerous goods’ in Article 2(11) of the UAS Regulation stems from the definition and classification of ‘dangerous goods’ in the ICAO Technical Instructions. ICAO Advisory Circular (AC) 102-37, Revision 0, issued on 23 June 2020, contains further information.
Under the definition of ‘dangerous goods’ in Article 2(11), blood is considered capable of posing a hazard to health when it contains or may contain infectious substances.
‘Infectious substances’ means substances that are classified under Division 6.2 of the Technical Instructions. The definition and classification of such substances are also available in the abovementioned ICAO AC 102-37.
Blood for transfusion and medical samples that are not subject to the provisions of the Technical Instructions may be transported in the ‘open’, ‘specific’, or ‘certified’ categories.
Blood that contains or potentially contains infectious substances should be transported in the ‘specific’ or ‘certified’ categories. If such transport results in a high risk for third parties in case of an accident, the UAS operation falls under the ‘certified’ category (as per Article 6(1)(b)(iii) of the UAS Regulation). If the blood contains or potentially contains infectious substances and is enclosed in such a container such that the blood will not be spilled in case of an accident, the UAS operation may fall under the ‘specific’ category if there are no other causes of high risk for third parties.
Articles and substances which would otherwise be classified as dangerous goods (e.g. fuel, batteries and other goods used during the flight to supply energy to the drone’s system) but which are required to be on board the aircraft for the propulsion of the UAS or for the operation of its specialised equipment during transport, or which are required in accordance with the pertinent operating requirements should not be considered as transported dangerous goods and their safety should verified during the design verification of the UAS.

#### Result 2
Citation: [easa-amc-gm | AMC1 Article 5 ‘Specific’ category of UAS operations]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 5 ‘Specific’ category of UAS operations (part 1/2)
TRANSPORT OF DANGEROUS GOODS IN THE ‘SPECIFIC’ CATEGORY
(a) Dangerous goods may be transported in the ‘specific’ category of UAS operations only if the UAS operator is able to demonstrate that these goods will not cause harm or damage to third parties or to the environment in case of accident. When compatible with the operation, a crashprotected container, which will prevent the leakage/dispersion of dangerous goods in case of accident, would be acceptable. In this case, the UAS operator should demonstrate that the container is capable of maintaining/protecting the dangerous goods without causing damage or harm to third parties or the environment in case of accident. In demonstrating the conformity of the container, the operational characteristics of the flight (flight speed, altitude, weather conditions, etc.) shall be taken into account, as well as the defining aspects of the geographical area of operation.
(b) The assessment of the operational risk of transporting dangerous goods should take into account the following:
(1) the risk that such goods pose to persons that are directly involved in their handling, to the environment, and to third parties and their properties;
(2) the hazard posed by the quantity and class of the dangerous goods;
(3) the characteristics of the container for the dangerous goods;
(4) the level of competence of those handling the dangerous goods; and
(5) the geographical area in which the flight will be operated.

#### Result 3
Citation: [easa-amc-gm | AMC1 Article 2(11) Definitions]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 2(11) Definitions
DEFINITION OF ‘DANGEROUS GOODS’
‘Dangerous goods’ should be considered any articles or substances which are capable of posing a hazard to health, safety, property or the environment, and which are listed as dangerous goods in the ICAO Technical Instructions for the Safe Transport of Dangerous Goods by Air (ICAO Doc 9284), known as the ‘Technical Instructions’, or which are classified as such according to the Technical Instructions.

#### Result 4
Citation: [easa-amc-gm | AMC1 Article 5 ‘Specific’ category of UAS operations]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 5 ‘Specific’ category of UAS operations (part 2/2)
(c) The UAS operator that wishes to carry out operations in the ‘specific’ category to transport dangerous goods should establish a dangerous goods training programmes for the personnel involved, as required by the Technical Instructions. Such training programmes should be commensurate with the responsibilities of the personnel involved in those operations. The training programmes should be subject to review and approval by the competent authority, and should cover at least the following aspects:
(1) dangerous goods terminology;
(2) classification of dangerous goods;
(3) labelling of dangerous goods;
(4) identification of dangerous goods that use ‘SDSs’ and the Globally Harmonised System of Classification and Labelling of Chemicals (GHS) consumer labelling;
(5) use of the dangerous goods list provided in the Technical Instructions;
(6) storage and handling of dangerous goods, including but not limited to the segregation of incompatible dangerous goods, dangerous goods loading, and dangerous goods securing;
(7) instructions and safety precautions to be provided to employees and third parties; and
(8) emergency/reporting procedures included in the ERP in case of an accident/incident with dangerous goods.

#### Result 5
Citation: [easa-amc-gm | AMC3 UAS.SPEC.050(1)(d) Responsibilities of the UAS operator]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC3 UAS.SPEC.050(1)(d) Responsibilities of the UAS operator (part 14/18)
Transport of dangerous goods | Safe transport of dangerous goods | Explain the terminology relevant to dangerous goods. Be able to recognise dangerous goods and understand their labelling. Be able to interpret the documentation related to dangerous goods. Recognise dangerous goods by using ‘safety data sheets’ and the consumer labelling of the Globally Harmonized System of Classification and Labelling of Chemicals (GHS). Explain that the provisions for the transport of dangerous goods by air are included in ICAO Doc 9284 ‘Technical Instructions for the Safe Transport of Dangerous Goods by Air’. State the emergency/reporting procedures in case of an event with dangerous goods, including that in the event of a dangerous-goods-related emergency regarding the UA, the remote pilot should inform the ATC organisation of the transport of dangerous goods. Explain the principles of compatibility and segregation of dangerous goods. Explain the special requirements for loading radioactive materials. Explain the use of the dangerous goods list. Explain the procedures for collecting safety data, e.g. reporting accidents, incidents, and occurrences with dangerous goods. Note: The learning objectives should be derived from the Technical Instructions and should be commensurate with the personnel responsibilities.
Operations with multiple UASs and swarms | Limitations related to human factors | Understand the human performance limitations in an operation with multiple UASs, including UAS swarms. List the vital actions that the remote pilot and the persons who assist the remote pilot should perform in case of an emergency descent of the multiple/swarming UASs.
#### Result 1
Citation: [reg-2019-947 | Article 4 - ‘Open’ category of UAS operations]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 4 - ‘Open’ category of UAS operations
1. Operations shall be classified as UAS operations in the ‘open’ category only where the following requirements are met:
(a) the UAS belongs to one of the classes set out in Delegated Regulation (EU) 2019/945 or is privately built or meets the conditions defined in Article 20;
(b) the unmanned aircraft has a maximum take-off mass of less than 25 kg;
(c) the remote pilot ensures that the unmanned aircraft is kept at a safe distance from people and that it is not flown over assemblies of people;
(d) the remote pilot keeps the unmanned aircraft in VLOS at all times except when flying in follow-me mode or when using an unmanned aircraft observer as specified in Part A of the Annex;
(e) during flight, the unmanned aircraft is maintained within 120 metres from the closest point of the surface of the earth, except when overflying an obstacle, as specified in Part A of the Annex
(f) during flight, the unmanned aircraft does not carry dangerous goods and does not drop any material;
2. UAS operations in the ‘open’ category shall be divided in three sub-categories in accordance with the requirements set out in Part A of the Annex.

#### Result 2
Citation: [reg-2019-947 | UAS.OPEN.010 General provisions]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.010 General provisions
(1) The category of UAS ‘open’ operations is divided into three subcategories A1, A2 and A3, on the basis of operational limitations, requirements for the remote pilot and technical requirements for UAS.
(2) Where the UAS operation involves the flight of the unmanned aircraft starting from a natural elevation in the terrain or over terrain with natural elevations, the unmanned aircraft shall be maintained within 120 metres from the closest point of the surface of the earth. The measurement of distances shall be adapted accordingly to the geographical characteristics of the terrain, such as plains, hills, mountains.
(3) When flying an unmanned aircraft within a horizontal distance of 50 metres from an artificial obstacle taller than 105 metres, the maximum height of the UAS operation may be increased up to 15 metres above the height of the obstacle at the request of the entity responsible for the obstacle.
(4) By way of derogation from point (2), unmanned sailplanes with a MTOM, including payload, of less than 10 kg, may be flown at a distance in excess of 120 metres from the closest point of the surface of the earth, provided that the unmanned sailplane is not flown at a height greater than 120 metres above the remote pilot at any time.

#### Result 3
Citation: [reg-2019-947 | UAS.OPEN.060 Responsibilities of the remote pilot]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.060 Responsibilities of the remote pilot (part 1/2)
(1) Before starting an UAS operation, the remote pilot shall:
(a) have the appropriate competency in the subcategory of the intended UAS operations in accordance with points UAS.OPEN.020, UAS.OPEN.030 or UAS.OPEN.040 to perform its task and carry a proof of competency while operating the UAS, except when operating an unmanned aircraft referred to in points (5)(a), (5)(b) or (5)(c) of point UAS.OPEN.020;
(b) obtain updated information relevant to the intended UAS operation about any geographical zone published by the Member State of operation in accordance with Article 15;
(c) observe the operating environment, check the presence of obstacles and, unless operating in subcategory A1 with an unmanned aircraft referred to in points (5)(a), (5)(b) or (5)(c) of point UAS.OPEN.020, check the presence of any uninvolved person;
(d) ensure that the UAS is in a condition to safely complete the intended flight, and if applicable, check if the direct remote identification is active and up-to-date;
(e) if the UAS is fitted with an additional payload, verify that its mass does not exceed neither the MTOM defined by the manufacturer or the MTOM limit of its class.
(2) During the flight, the remote pilot shall:
(a) not perform duties under the influence of psychoactive substances or alcohol or when it is unfit to perform its tasks due to injury, fatigue, medication, sickness or other causes;

#### Result 4
Citation: [reg-2019-947 | Article 20 - Particular provisions concerning the use of certain UAS in the ‘open’ category]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 20 - Particular provisions concerning the use of certain UAS in the ‘open’ category
UAS types within the meaning of Decision No 768/2008/EC of the European Parliament and of the Council, which do not comply with Delegated Regulation (EU) 2019/945 and which are not privatelybuilt are allowed to continue to be operated under the following conditions, when they have been placed on the market before 1 January 2024:
(a) in subcategory A1 as defined in Part A of the Annex, provided that the unmanned aircraft has a maximum take-off mass of less than 250 g, including its payload;
(b) in subcategory A3 as defined in Part A of the Annex, provided that the unmanned aircraft has a maximum take-off mass of less than 25 kg, including its fuel and payload.

#### Result 5
Citation: [reg-2019-947 | UAS.OPEN.040 UAS operations in subcategory A3]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.040 UAS operations in subcategory A3
UAS operations in subcategory A3 shall comply with all of the following conditions:
(1) be conducted in an area where the remote pilot reasonably expects that no uninvolved person will be endangered within the range where the unmanned aircraft is flown during the entire time of the UAS operation;
(2) be conducted at a safe horizontal distance of at least 150 metres from residential, commercial, industrial or recreational areas;
(3) be performed by a remote pilot who is familiar with manufacturer’s instructions provided by the manufacturer of the UAS and who has completed an online training course and passed an online theoretical knowledge examination as defined in point (4)(b) of point UAS.OPEN.020;
(4) be performed with an unmanned aircraft that:
(a) has an MTOM, including payload, of less than 25 kg, in the case of a privately built UAS, or
(b) meets the requirements defined in point (b) of Article 20;
(c) is marked as class C2 and complies with the requirements of that class, as defined in Part 3 of the Annex to Delegated Regulation (EU) 2019/945 and is operated with active and updated direct remote identification system and geo-awareness function or;
(d) is marked as class C3 and complies with the requirements of that class, as defined in Part 4 of the Annex to Delegated Regulation (EU) 2019/945 and is operated with active and updated direct remote identification system and geo-awareness function; or
(e) is marked as class C4 and complies with the requirements of that class, as defined in Part 5 of the Annex to Delegated Regulation (EU) 2019/945.
#### Result 1
Citation: [reg-2019-947 | Article 4 - ‘Open’ category of UAS operations]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 4 - ‘Open’ category of UAS operations
1. Operations shall be classified as UAS operations in the ‘open’ category only where the following requirements are met:
(a) the UAS belongs to one of the classes set out in Delegated Regulation (EU) 2019/945 or is privately built or meets the conditions defined in Article 20;
(b) the unmanned aircraft has a maximum take-off mass of less than 25 kg;
(c) the remote pilot ensures that the unmanned aircraft is kept at a safe distance from people and that it is not flown over assemblies of people;
(d) the remote pilot keeps the unmanned aircraft in VLOS at all times except when flying in follow-me mode or when using an unmanned aircraft observer as specified in Part A of the Annex;
(e) during flight, the unmanned aircraft is maintained within 120 metres from the closest point of the surface of the earth, except when overflying an obstacle, as specified in Part A of the Annex
(f) during flight, the unmanned aircraft does not carry dangerous goods and does not drop any material;
2. UAS operations in the ‘open’ category shall be divided in three sub-categories in accordance with the requirements set out in Part A of the Annex.

#### Result 2
Citation: [easa-amc-gm | AMC1 Article 2(11) Definitions]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 2(11) Definitions
DEFINITION OF ‘DANGEROUS GOODS’
‘Dangerous goods’ should be considered any articles or substances which are capable of posing a hazard to health, safety, property or the environment, and which are listed as dangerous goods in the ICAO Technical Instructions for the Safe Transport of Dangerous Goods by Air (ICAO Doc 9284), known as the ‘Technical Instructions’, or which are classified as such according to the Technical Instructions.

#### Result 3
Citation: [easa-amc-gm | AMC1 Article 5 ‘Specific’ category of UAS operations]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 5 ‘Specific’ category of UAS operations (part 1/2)
TRANSPORT OF DANGEROUS GOODS IN THE ‘SPECIFIC’ CATEGORY
(a) Dangerous goods may be transported in the ‘specific’ category of UAS operations only if the UAS operator is able to demonstrate that these goods will not cause harm or damage to third parties or to the environment in case of accident. When compatible with the operation, a crashprotected container, which will prevent the leakage/dispersion of dangerous goods in case of accident, would be acceptable. In this case, the UAS operator should demonstrate that the container is capable of maintaining/protecting the dangerous goods without causing damage or harm to third parties or the environment in case of accident. In demonstrating the conformity of the container, the operational characteristics of the flight (flight speed, altitude, weather conditions, etc.) shall be taken into account, as well as the defining aspects of the geographical area of operation.
(b) The assessment of the operational risk of transporting dangerous goods should take into account the following:
(1) the risk that such goods pose to persons that are directly involved in their handling, to the environment, and to third parties and their properties;
(2) the hazard posed by the quantity and class of the dangerous goods;
(3) the characteristics of the container for the dangerous goods;
(4) the level of competence of those handling the dangerous goods; and
(5) the geographical area in which the flight will be operated.

#### Result 4
Citation: [easa-amc-gm | AMC1 Article 5 ‘Specific’ category of UAS operations]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 5 ‘Specific’ category of UAS operations (part 2/2)
(c) The UAS operator that wishes to carry out operations in the ‘specific’ category to transport dangerous goods should establish a dangerous goods training programmes for the personnel involved, as required by the Technical Instructions. Such training programmes should be commensurate with the responsibilities of the personnel involved in those operations. The training programmes should be subject to review and approval by the competent authority, and should cover at least the following aspects:
(1) dangerous goods terminology;
(2) classification of dangerous goods;
(3) labelling of dangerous goods;
(4) identification of dangerous goods that use ‘SDSs’ and the Globally Harmonised System of Classification and Labelling of Chemicals (GHS) consumer labelling;
(5) use of the dangerous goods list provided in the Technical Instructions;
(6) storage and handling of dangerous goods, including but not limited to the segregation of incompatible dangerous goods, dangerous goods loading, and dangerous goods securing;
(7) instructions and safety precautions to be provided to employees and third parties; and
(8) emergency/reporting procedures included in the ERP in case of an accident/incident with dangerous goods.

#### Result 5
Citation: [easa-amc-gm | GM1 Article 2(11) Definitions]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 Article 2(11) Definitions
DEFINITION OF ‘DANGEROUS GOODS’
The definition of ‘dangerous goods’ in Article 2(11) of the UAS Regulation stems from the definition and classification of ‘dangerous goods’ in the ICAO Technical Instructions. ICAO Advisory Circular (AC) 102-37, Revision 0, issued on 23 June 2020, contains further information.
Under the definition of ‘dangerous goods’ in Article 2(11), blood is considered capable of posing a hazard to health when it contains or may contain infectious substances.
‘Infectious substances’ means substances that are classified under Division 6.2 of the Technical Instructions. The definition and classification of such substances are also available in the abovementioned ICAO AC 102-37.
Blood for transfusion and medical samples that are not subject to the provisions of the Technical Instructions may be transported in the ‘open’, ‘specific’, or ‘certified’ categories.
Blood that contains or potentially contains infectious substances should be transported in the ‘specific’ or ‘certified’ categories. If such transport results in a high risk for third parties in case of an accident, the UAS operation falls under the ‘certified’ category (as per Article 6(1)(b)(iii) of the UAS Regulation). If the blood contains or potentially contains infectious substances and is enclosed in such a container such that the blood will not be spilled in case of an accident, the UAS operation may fall under the ‘specific’ category if there are no other causes of high risk for third parties.
Articles and substances which would otherwise be classified as dangerous goods (e.g. fuel, batteries and other goods used during the flight to supply energy to the drone’s system) but which are required to be on board the aircraft for the propulsion of the UAS or for the operation of its specialised equipment during transport, or which are required in accordance with the pertinent operating requirements should not be considered as transported dangerous goods and their safety should verified during the design verification of the UAS.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q15 (single)

**Question:** How far from me can a drone fly in follow-me mode in subcategory A1?

**Reference:** Up to 50 metres from the remote pilot when follow-me mode is active.

**Agent answer:**

When the follow-me mode is active, the drone can fly up to a maximum distance of **50 metres** from you [reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.020 UAS operations in subcategory A1 (part 1/2)
UAS operations in subcategory A1 shall comply with all of the following conditions:
(1) for unmanned aircraft referred to in point (5)(d), be conducted in such a way that a remote pilot of the unmanned aircraft does not overfly assemblies of people and reasonably expects that no uninvolved person will be overflown. In the event of unexpected overflight of uninvolved persons, the remote pilot shall reduce as much as possible the time during which the unmanned aircraft overflies those persons;
(2) in the case of an unmanned aircraft referred to in points (5)(a), (5)(b) and (5)(c), be conducted in such a way that the remote pilot of the unmanned aircraft may overfly uninvolved persons, but shall never overfly assemblies of people;
(3) by way of derogation from point (d) of paragraph 1 of Article 4, be conducted, when the followme mode is active, up to a distance of 50 metres from the remote pilot;
(4) be performed by a remote pilot who:
(a) is familiar with manufacturer’s instructions provided by the manufacturer of the UAS;

#### Result 2
Citation: [easa-amc-gm | GM1 UAS.OPEN.030(1) and UAS.OPEN.040(1) UAS operations in subcategories A1 and A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 UAS.OPEN.030(1) and UAS.OPEN.040(1) UAS operations in subcategories A1 and A3
DIFFERENCE BETWEEN SUB-CATEGORIES A2 AND A3
Subcategory A2 addresses operations during which flying close to people is intended for a significant portion of the flight. The minimum distance ranges from 30 m to 5 m from uninvolved people. 5 m is only allowed when there is an active low-speed mode function on the UA, and the remote pilot has conducted an evaluation of the situation regarding the weather, the performance of the UA and the segregation of the overflown area.
Sub-category A3 addresses operations that are conducted in an area (hereafter referred to as ‘the area’) where the remote pilot reasonably expects that no uninvolved people will be endangered within the range of the unmanned aircraft where it is flown during the mission. In addition, the operation must be conducted at a safe horizontal distance of at least 150 m from residential, commercial, industrial or recreational areas.

#### Result 3
Citation: [easa-amc-gm | AMC1 UAS.OPEN.030(1) UAS operations in subcategory A2]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.030(1) UAS operations in subcategory A2
SAFE DISTANCE FROM UNINVOLVED PERSONS
(a) The minimum horizontal distance of the UA from uninvolved persons should be defined as the distance between the points where the UA would hit the ground in the event of a vertical fall and the position of the uninvolved persons.
(b) As a reference, when the UA is operating in close proximity to people, the remote pilot should keep the UA at a lateral distance from any uninvolved person that is not shorter than the height (‘1:1 rule’, i.e. if the UA is flying at a height of 30 m, the distance from any uninvolved person should be at least 30 m).
(c) In any case, the distance from uninvolved persons should always be greater than:
(1) 5 m, when the low-speed mode function on the UA is activated and set to 3 m per second;
(2) 5 m, when operating a UAS balloon or airship; or
(3) 30 m in all other cases.

#### Result 4
Citation: [easa-amc-gm | AMC1 UAS.OPEN.040(1) Operations in subcategory A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.040(1) Operations in subcategory A3
AREAS WHERE UAS OPERATIONS IN A3 MAY BE CONDUCTED
(a) If an uninvolved person enters the range of the UAS operation, the remote pilot should, where necessary, adjust the operation to ensure the safety of the uninvolved person and discontinue the operation if the safety of the UAS operation is not ensured.
(b) A minimum horizontal distance from the person that is passing the area could be estimated as follows:
(1) no less than 30 m;
(2) no less than the height (‘1:1 rule’, i.e. if the UA is flying at a height of 30 m, the distance of the UA from the uninvolved person should be at least 30 m), and
(3) no less than the distance that the UA would cover in 2 seconds at the maximum speed (this assumes a reaction time of 2 seconds).
This minimum horizontal distance is intended to protect people on the ground, but can be extended to property and animals.

#### Result 5
Citation: [reg-2019-947 | UAS.OPEN.030 UAS operations in subcategory A2]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.030 UAS operations in subcategory A2
UAS operations in subcategory A2 shall comply with all of the following conditions:
(1) be conducted in such a way that the unmanned aircraft does not overfly uninvolved persons and the UAS operations take place at a safe horizontal distance of at least 30 metres from them; the remote pilot may reduce the horizontal safety distance down to a minimum of 5 metres from an uninvolved person when operating an unmanned aircraft with an active low speed mode function and after evaluation of the situation regarding:
(a) weather conditions,
(b) performance of the unmanned aircraft,
(c) segregation of the overflown area.
(2) be performed by a remote pilot who is familiar with manufacturer’s instructions provided by the manufacturer of the UAS and holds a certificate of remote pilot competency issued by the competent authority or by an entity designated by the competent authority of a Member State. This certificate shall be obtained after complying with all of the following conditions and in the order indicated:
(a) completing an online training course and passed the online theoretical knowledge examination as referred to in point (4)(b) of point UAS.OPEN.020;
(b) completing a self-practical training in the operating conditions of the subcategory A3 set out in points (1) and (2) of point UAS.OPEN.040;
(c) declaring the completion of the self-practical training defined in point (b) and passing an additional theoretical knowledge examination provided by the competent authority or at an entity designated by the competent authority of a Member State achieving at least 75% of the overall marks. The examination shall comprise at least 30 multiple-choice questions aimed at assessing the remote pilot’s knowledge of the technical and operational mitigations for ground risk, distributed appropriately across the following subjects:
(i) meteorology;
(ii) UAS flight performance;
(iii) technical and operational mitigations for ground risk.
(3) be performed with an unmanned aircraft which is marked as class C2 and complies with the requirements of that class, as defined in Part 3 of the Annex to Delegated Regulation (EU) 2019/945, and is operated with active and updated direct remote identification system and geo-awareness function.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q16 (single)

**Question:** Can I register as an operator in two EU countries at the same time?

**Reference:** No. You register in the Member State where you reside (or have your principal place of business) and cannot be registered in more than one Member State at a time.

**Agent answer:**

No, a UAS operator cannot be registered in more than one Member State at a time. You must register in the Member State where you have your residence (for natural persons) or your principal place of business (for legal persons).

[reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 2/3)
4. Member States shall ensure that registration systems are digital and interoperable and allow for mutual access and exchange of information through the repository referred to in Article 74 of Regulation (EU) 2018/1139.
5. UAS operators shall register themselves:
(a) when operating within the ‘open’ category any of the following unmanned aircraft:
i. with a MTOM of 250 g or more, or, which in the case of an impact can transfer to a human kinetic energy above 80 Joules;
ii. that is equipped with a sensor able to capture personal data, unless it complies with Directive 2009/48/EC.
(b) when operating within the ‘specific’ category an unmanned aircraft of any mass.
6. UAS operators shall register themselves in the Member State where they have their residence for natural persons or where they have their principal place of business for legal persons and ensure that their registration information is accurate. A UAS operator cannot be registered in more than one Member State at a time.
Member States shall issue a unique digital registration number for UAS operators and for the UAS that require registration, allowing their individual identification.
The registration number for UAS operators shall be established on the basis of standards that support the interoperability of the registration systems;
7. The owner of an unmanned aircraft whose design is subject to certification shall register the unmanned aircraft.

#### Result 2
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 1/3)
1. Member States shall establish and maintain accurate registration systems for UAS whose design is subject to certification and for UAS operators whose operation may present a risk to safety, security, privacy, and protection of personal data or environment.
2. The registration systems for UAS operators shall provide the fields for introducing and exchanging the following information:
(a) the full name and the date of birth for natural persons and the name and their identification number for legal persons;
(b) the address of UAS operators;
(c) their email address and telephone number;
(d) an insurance policy number for UAS if required by Union or national law;
(e) the confirmation by legal persons of the following statement: ‘All personnel directly involved in the operations are competent to perform their tasks, and the UAS will be operated only by remote pilots with the appropriate level of competency’;
(f) operational authorisations and LUCs held and declarations followed by a confirmation in accordance with Article 12(5)(b).
3. The registration systems for unmanned aircraft whose design is subject to certification shall provide the fields for introducing and exchanging the following information:
(a) manufacturer’s name;
(b) manufacturer’s designation of the unmanned aircraft;
(c) unmanned aircraft’s serial number;
(d) full name, address, email address and telephone number of the natural or legal person under whose name the unmanned aircraft is registered.

#### Result 3
Citation: [easa-amc-gm | AMC1 Article 13 Cross-border operations or operations outside the State of registration]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 13 Cross-border operations or operations outside the State of registration (part 1/3)
CROSS-BORDER OPERATIONS
(a) A UAS operator that intends to conduct an operation, for which an operational authorisation is required, partially or fully in a Member State other than the State of registration, it should firstly obtain any required authorisation for that operation from the State of registration, unless the UAS operator has a LUC with the appropriate privileges. This process applies also when the UAS operator intends to conduct an operation only in a MS other than the State of registration.
(b) The UAS operator should:
(1) identify the applicable local conditions in the area of operation;
(2) adapt the operational procedures, as necessary:
(i) to comply with the applicable local conditions; and
(ii) as required by the application to the new location(s) of the mitigation measures, identified in the operational authorisation;
(3) submit to the competent authority of the MS of operation (refer to https://www.easa.europa.eu/domains/civil-drones/naa for the links to the NAA websites) an application for a cross-border operation using the form provided in AMC1 Article 13(1), attaching the following:
(i) a copy of the operational authorisation issued by the competent authority of the MS of registration, or a copy of the LUC terms of reference if the operation is conducted under the privileges of the LUC;

#### Result 4
Citation: [reg-2019-947 | Article 13 - Cross-border operations or operations outside the state of registration]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 13 - Cross-border operations or operations outside the state of registration (part 1/2)
1. When an UAS operator intends to conduct an operation in the ‘specific’ category for which an operational authorisation has already been granted in accordance with Article 12, and which is intended to take place partially or entirely in the airspace of a Member State other than the Member State of registration, the UAS operator shall provide the competent authority of the Member State of intended operation with an application including the following information:
(a) a copy of the operational authorisation granted to the UAS operator in accordance with Article 12; and
(b) the location(s) of the intended operation including the updated mitigation measures, if needed, to address those risks identified under Article 11(2)(b) which are specific to the local airspace, terrain and population characteristics and the climatic conditions.
2. Upon receipt of the application set out in paragraph 1, the competent authority of the Member State of intended operation shall assess it without undue delay and provide the competent authority of the Member State of registration and the UAS operator with a confirmation that the updated mitigation measures referred to in point (b) of paragraph 1 are satisfactory for the operation at the intended location. Upon receipt of that confirmation, the UAS operator may start the intended operation and the Member State of registration shall record the updated mitigation measures that the UAS operator has to apply in the operational authorisation issued in accordance with Article 12.

#### Result 5
Citation: [reg-2019-947 | Article 13 - Cross-border operations or operations outside the state of registration]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 13 - Cross-border operations or operations outside the state of registration (part 2/2)
3. When an UAS operator intends to conduct an operation in the ‘specific’ category for which a declaration has been made in accordance with paragraph 5 of Article 5, and which is intended to take place partially or entirely in the airspace of a Member State other than the Member State of registration, the UAS operator shall provide the competent authority of the Member State of the intended operation with a copy of the declaration submitted to the Member State of registration, as well as a copy of the confirmation of receipt and completeness.
4. Where a UAS operator holding an LUC with privileges in accordance with point UAS.LUC.060 of the Annex intends to conduct an operation in the ‘specific category’ taking place partially or entirely in the airspace of a Member State other than the Member State of registration, the UAS operator shall provide the competent authority of the Member State of intended operation with the following information:
(a) a copy of the term of approval received in accordance with point UAS.LUC.050 of the Annex; and
(b) the location or locations of the intended operation in accordance with paragraph 1(b) of this Article.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q17 (single)

**Question:** What is the maximum mass and size of a class C3 drone?

**Reference:** A class C3 UAS must have an MTOM of less than 25 kg including payload and a maximum characteristic dimension of less than 3 m.

**Agent answer:**

A class C3 drone must have:
* A maximum take-off mass (MTOM) of less than 25 kg, including payload [reg-2019-945 | PART 4 — Requirements for a class C3 Unmanned aircraft system].
* A maximum characteristic dimension of less than 3 m [reg-2019-945 | PART 4 — Requirements for a class C3 Unmanned aircraft system].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** citation check failed: the answer makes claims but cites nothing; citation check passed after one retry; national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-945 | PART 4 — Requirements for a class C3 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 4 — Requirements for a class C3 Unmanned aircraft system (part 1/6)
A class C3 UAS bears the following class identification label on the UA:
A class C3 UAS shall comply with the following:
(1) have an MTOM of less than 25 kg, including payload, and have a maximum characteristic dimension of less than 3 m;
(2) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot. If the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(3) be safely controllable with regard to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;
(4) in the case of a tethered UA, have a tensile length of the tether that is less than 50 m and a mechanical strength of no less than:
(a) for heavier-than-air aircraft, 10 times the weight of the aerodyne at maximum mass;
(b) for lighter-than-air aircraft, 4 times the force exerted by the combination of the maximum static thrust and the aerodynamic force of the maximum allowed wind speed in flight;

#### Result 2
Citation: [reg-2019-945 | PART 4 — Requirements for a class C3 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 4 — Requirements for a class C3 Unmanned aircraft system (part 2/6)
(5) unless tethered, in case of a loss of the command and control link, have a reliable and predictable method for the UA to recover the command and control link or, if it fails, terminate the flight in a way that reduces the effect on third parties in the air or on the ground;
(6) unless it is a fixed-wing UA, have the indication of the guaranteed A-weighted sound power level LWA determined as per Part 13 affixed on the UA and/or its packaging as per Part 14;
(7) be exclusively powered by electricity;
(8) have a unique serial number compliant with standard ANSI/CTA-2063-A-2019, Small Unmanned Aerial Systems Serial Numbers, 2019;
(9) unless tethered, have a direct remote identification that:
(a) allows the upload of the UAS operator registration number required in accordance with Article 14 of Implementing Regulation (EU) 2019/947 and any additional number provided by the registration system; the system shall perform a consistency check verifying the integrity of the full string provided to the UAS operator at the time of registration; in case of inconsistency, the UAS shall emit an error message to the UAS operator;
(b) ensures, in real time during the whole duration of the flight, the direct periodic broadcast from the UA using an open and documented transmission protocol, in a way that it can be received directly by existing mobile devices within the broadcasting range, of at least the following data:

#### Result 3
Citation: [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 2 — Requirements for a class C1 Unmanned aircraft system (part 1/6)
A class C1 UAS bears the following class identification label on the UA:
A class C1 UAS shall comply with the following:
(1) be made of materials and have performance and physical characteristics such as to ensure that in the event of an impact at terminal velocity with a human head, the energy transmitted to the human head is less than 80 J, or, as an alternative, shall have an MTOM of less than 900 g, including payload;
(2) have a maximum speed in level flight of 19 m/s;
(3) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot; if the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(4) be safely controllable with regards to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;

#### Result 4
Citation: [reg-2019-945 | PART 3 — Requirements for a class C2 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 3 — Requirements for a class C2 Unmanned aircraft system (part 1/6)
A class C2 UAS bears the following class identification label on the UA:
A class C2 UAS shall comply with the following:
(1) have an MTOM of less than 4 kg, including payload;
(2) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot. If the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(3) be safely controllable with regard to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;
(4) have the requisite mechanical strength for the UA, including any necessary safety factor, and, where appropriate, stability to withstand any stress to which it is subjected to during use without any breakage or deformation that might interfere with its safe flight;
(5) in the case of a tethered UA, have a tensile length of the tether that is less than 50 m and a mechanical strength that is no less than:
(a) for heavier-than-air aircraft, 10 times the weight of the aerodyne at maximum mass;

#### Result 5
Citation: [reg-2019-945 | PART 5 — Requirements for a class C4 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 5 — Requirements for a class C4 Unmanned aircraft system
A class C4 UAS bears the following label on the UA in a visible manner:
A class C4 UAS shall comply with the following:
(1) have an MTOM of less than 25 kg, including payload;
(2) be safely controllable and manoeuvrable by a remote pilot following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;
(3) not be capable of automatic control modes except for flight stabilisation assistance with no direct effect on the trajectory and lost link assistance provided that a pre-determined fixed position of the flight controls in case of lost link is available;
(4) be placed on the market with manufacturer’s instructions providing:
(a) the characteristics of the UA including but not limited to the:
class of the UA
UA mass (with a description of the reference configuration) and the maximum take-off mass (MTOM);
general characteristics of allowed payloads in terms of mass, dimensions, interfaces with the UA and other possible restrictions;
equipment and software to control the UA remotely; and
a description of the behaviour of the UA in case of a loss of the command and control link;
(b) clear operational instructions;
(c) maintenance instructions;
(d) troubleshooting procedures;
(e) operational limitations (including but not limited to meteorological conditions and day/night operations); and
(f) appropriate description of all the risks related to UAS operations;
(5) include an information notice published by EASA providing the applicable limitations and obligations, in accordance with Implementing Regulation (EU) 2019/947.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q18 (single)

**Question:** How long is an operational declaration for a standard scenario valid?

**Reference:** An operational declaration has a limited duration of 2 years, and stops being complete if oversight finds non-conformity, conditions change, or the authority is denied access.

**Agent answer:**

An operational declaration for a standard scenario has a limited validity of **2 years** [reg-2019-947 | UAS.SPEC.085 Duration and validity of an operational declaration].

However, the declaration will no longer be considered complete before that period ends if:
1. During oversight, the competent authority finds that the operation is not conducted in accordance with the declaration [reg-2019-947 | UAS.SPEC.085 Duration and validity of an operational declaration];
2. The operating conditions change to the extent that the declaration no longer complies with the applicable requirements [reg-2019-947 | UAS.SPEC.085 Duration and validity of an operational declaration]; or
3. Access is not granted to the competent authority for oversight [reg-2019-947 | UAS.SPEC.085 Duration and validity of an operational declaration].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-947 | UAS.SPEC.085 Duration and validity of an operational declaration]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.SPEC.085 Duration and validity of an operational declaration
The operational declaration shall have a limited duration of 2 years. The declaration shall no longer be considered as complete within the meaning of point (4) of point UAS.SPEC.020 if:
(1) during the oversight of the UAS operator, the competent authority has found that the UAS operation is not conducted in accordance with the operational declaration;
(2) the conditions of the UAS operation have changed to the extent that the operational declaration no longer complies with the applicable requirements of this Regulation;
(3) the competent authority is not granted access in accordance with point UAS.SPEC.090.

#### Result 2
Citation: [reg-2019-947 | UAS.SPEC.020 Operational declaration]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.SPEC.020 Operational declaration (part 1/2)
(1) In accordance with Article 5, the UAS operator may submit an operational declaration of compliance with a standard scenario as defined in Appendix 1 to this Annex to the competent authority of the Member State of registration as an alternative to points UAS.SPEC.030 and UAS.SPEC.040 in relation to operations:
(a) of unmanned aircraft with:
(i) maximum characteristic dimension up to 3 metres in VLOS over controlled ground area except over assemblies of people,
(ii) maximum characteristic dimension up to 1 metre in VLOS except over assemblies of people;
(iii) maximum characteristic dimension up to 1 metre in BVLOS over sparsely populated areas;
(iv) maximum characteristic dimension up to 3 metres in BVLOS over controlled ground area.
(b) performed below 120 metres from the closest point of the surface of the earth, and:
(i) in uncontrolled airspace (class F or G) unless different limitations are provided by Member States through UAS geographical zones in areas where the probability of encountering manned aircraft is not low; or
(ii) in controlled airspace, in accordance with published procedures for the area of operation, so that a low probability of encountering manned aircraft is ensured.
(2) A declaration of UAS operators shall contain:
(a) administrative information about the UAS operator;
(b) a statement that the operation satisfies the operational requirement set out in point (1) and a standard scenario as defined in Appendix 1 to the Annex;

#### Result 3
Citation: [reg-2019-947 | Appendix 2 — Operational declaration]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Appendix 2 — Operational declaration
Operational declaration
Data protection: Personal data included in this declaration is processed by the competent authority pursuant to Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation). It will be processed for the purposes of the performance, management and follow up of the oversight activities according to Commission Implementing Regulation (EU) 2019/947. If you require further information concerning the processing of your personal data or you wish to exercise your rights (e.g. to access or rectify any inaccurate or incomplete data), please refer to the contact point of the competent authority. The applicant has the right to make a complaint regarding the processing of the personal data at any time to the national Data Protection Supervisory Authority.
UAS operator registration number
UAS operator name
UAS manufacturer
UAS model
UAS Serial number
I hereby declare that: I comply with all the applicable provisions of Implementing Regulation (EU) 2019/947 and with STS.x; and appropriate insurance cover will be in place for every flight made under the declaration, if required by Union or national law.
Date | Signature or other verification

#### Result 4
Citation: [reg-2019-947 | UAS.SPEC.020 Operational declaration]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.SPEC.020 Operational declaration (part 2/2)
(c) the commitment of the UAS operator to comply with the relevant mitigation measures required for the safety of the operation, including the associated instructions for the operation, for the design of the unmanned aircraft and the competency of involved personnel.
(d) confirmation by the UAS operator that an appropriate insurance cover will be in place for every flight made under the declaration, if required by Union or national law.
(3) Upon receipt of the declaration, the competent authority shall verify that the declaration contains all the elements listed in point (2) and shall provide the UAS operator with a confirmation of receipt and completeness without undue delay.
(4) After receiving the confirmation of receipt and completeness, the UAS operator is entitled to start the operation.
(5) UAS operators shall notify, without any delay, the competent authority of any change to the information contained in the operational declaration that they submitted.
(6) UAS operators holding an LUC with appropriate privileges, in accordance with Part C of this Annex, are not required to submit the declaration.

#### Result 5
Citation: [reg-2019-947 | UAS.SPEC.080 Duration and validity of an operational authorisation]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.SPEC.080 Duration and validity of an operational authorisation
(1) The competent authority shall specify the duration of the operational authorisation in the authorisation itself.
(2) Notwithstanding point (1), the operational authorisation remains valid as long as the UAS operator remains compliant with the relevant requirements of this Regulation and with the conditions defined in the operational authorisation.
(3) Upon revocation or surrender of the operational authorisation the UAS operator shall provide an acknowledgment in digital format that must be returned to the competent authority without delay.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q19 (single)

**Question:** What counts as an assembly of people?

**Reference:** Gatherings where people cannot move away because of density. Examples: sport, cultural, religious or political events, beaches or parks on a sunny day, commercial streets during opening hours, ski resorts.

**Agent answer:**

An **assembly of people** is legally defined as a gathering where persons are unable to move away due to the density of the people present `[reg-2019-945 | Article 3 - Definitions]`. 

Guidance material clarifies that this is based on an objective criterion related to the possibility for an individual to move around in order to limit the consequences of an out-of-control drone (rather than a specific numerical threshold) `[easa-amc-gm | GM1 Article 2(3) Definitions]`.

Qualitative examples of assemblies of people include:
* Sport, cultural, religious, or political events `[easa-amc-gm | GM1 Article 2(3) Definitions]`
* Beaches or parks on a sunny day `[easa-amc-gm | GM1 Article 2(3) Definitions]`
* Commercial streets during the opening hours of the shops `[easa-amc-gm | GM1 Article 2(3) Definitions]`
* Ski resorts, tracks, or lanes `[easa-amc-gm | GM1 Article 2(3) Definitions]`
* Spectators or crowds gathered for mass public events where the drone operation is not the primary focus (who are considered uninvolved persons) `[easa-amc-gm | GM1 Article 2(18) Definitions]`

*(Note: These points are from EASA Guidance Material and Acceptable Means of Compliance, which provide interpretive guidance on the binding definitions in Regulation (EU) 2019/945).*

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | GM1 Article 2(3) Definitions]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 Article 2(3) Definitions
DEFINITION OF ‘ASSEMBLIES OF PEOPLE’
Assemblies of people have been defined by an objective criterion related to the possibility for an individual to move around in order to limit the consequences of an out-of-control UA. It was indeed difficult to propose a number of people above which this group of people would turn into an assembly of people: numbers were indeed proposed, but they showed quite a large variation. Qualitative examples of assemblies of people are:
(a) sport, cultural, religious or political events;
(b) beaches or parks on a sunny day;
(c) commercial streets during the opening hours of the shops; and
(d) ski resorts/tracks/lanes.

#### Result 2
Citation: [easa-amc-gm | GM1 Article 2(18) Definitions]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 Article 2(18) Definitions (part 2/3)
In principle, in order to be considered a ‘person involved’, one:
(a) is able to decide whether or not to participate in the UAS operation;
(b) broadly understands the risks involved;
(c) has reasonable safeguards during the UAS operations, introduced by the site manager and the aircraft operator; and
(d) is not restricted from taking part in the event or activity if they decide not to participate in the UAS operation.
The person involved is expected to follow the directions and safety precautions provided by the UAS operator or the remote pilot, and the UAS operator or the remote pilot should check by asking simple questions to make sure that the directions and safety precautions have been properly understood.
It should be reminded that UAS operations over assemblies of people (e.g. sport activities or other mass public events) are never allowed in the ‘open’ category. These operations may be classified as falling into the ‘specific’ or ‘certified’ category, depending on the risk involved. Spectators or any other people gathered for sport activities or other mass public events for which the UAS operation is not the primary focus are generally considered ‘uninvolved persons’.

#### Result 3
Citation: [easa-amc-gm | AMC1 UAS.OPEN.020(1) and (2) UAS operations in subcategory A1]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.020(1) and (2) UAS operations in subcategory A1
OPERATIONAL LIMITATIONS IN SUBCATEGORY A1
As a principle, the rules prohibit overflying assemblies of people. Overflying isolated people is possible, but there is a distinction between class C1 and class C0 UAS or privately built UAS with MTOMs of less than 250 g.
(a) For UAS in class C1, before starting the UAS operation, the remote pilot should assess the area and should reasonably expect that no uninvolved person will be overflown. This evaluation should be made taking into account the configuration of the site of operation (e.g. the existence of roads, streets, pedestrian or bicycle paths), and the possibility to secure the site and the time of the day. In case of an unexpected overflight, the remote pilot should reduce as much as possible the duration of the overflight, for example, by flying the UAS in such a way that the distance between the UA and the uninvolved people increases, or by positioning the UAS over a place where there are no uninvolved people.
(b) It is accepted that UAS in class C0 or privately built UAS with MTOMs less than 250 g may fly over uninvolved people; however, this should be avoided whenever possible, and where it is unavoidable, extreme caution should be used.

#### Result 4
Citation: [easa-amc-gm | GM1 Article 2(18) Definitions]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 Article 2(18) Definitions (part 3/3)
An example: when filming with a UAS at a large music festival or public event, it is not sufficient to inform the audience or anyone present via a public address system, or via a statement on the ticket, or in advance by email or text message. Those types of communication channels do not satisfy the points above. In order to be considered a person involved, each person should be asked for their permission and be made aware of the possible risk(s).

#### Result 5
Citation: [reg-2019-945 | Article 3 - Definitions]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

Article 3 - Definitions (part 5/5)
(34) ‘measured sound power level’ means a sound power level as determined from measurements as laid down in Part 13 of the Annex; measured values may be determined either from a single UA representative for the type of equipment or from the average of a number of UA;
(35) ‘guaranteed sound power level’ means a sound power level determined in accordance with the requirements laid down in Part 13 of the Annex which includes the uncertainties due to production variation and measurement procedures and where the manufacturer, or his authorised representative established in the Community, confirms that according to the technical instruments applied and referred to in the technical documentation it is not exceeded;
(36) ‘hovering’ means staying in the same geographical position in the air;
(37) ‘assemblies of people’ means gatherings where persons are unable to move away due to the density of the people present;
(38) ‘control and monitoring unit’ (‘CMU’) means the equipment to control and monitor unmanned aircraft remotely, as defined in Article 3 point (32) of Regulation (EU) 2018/1139;
(39) ‘C2 link’ means the data link between the unmanned aircraft and the CMU for the purposes of managing the flight;
(40) ‘night’ means the hours between the end of evening civil twilight and the beginning of morning civil twilight as defined in Implementing Regulation (EU) No 923/2012 .
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q20 (single)

**Question:** What is the highest speed a class C5 drone can be limited to in low-speed mode?

**Reference:** Unless tethered, a C5 UAS needs a pilot-selectable low-speed mode limiting ground speed to not more than 5 m/s.

**Agent answer:**

A class C5 drone must be equipped with a low-speed mode selectable by the remote pilot that limits the ground speed to **not more than 5 m/s** (unless it is tethered).

*Source:* [reg-2019-945 | PART 16 — Requirements for a class C5 unmanned aircraft system and C5 accessories] (Commission Delegated Regulation (EU) 2019/945, binding law).

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-945 | PART 16 — Requirements for a class C5 unmanned aircraft system and C5 accessories]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 16 — Requirements for a class C5 unmanned aircraft system and C5 accessories (part 1/3)
A class C5 UAS bears the following class identification label on the UA:
A class C5 UAS shall comply with the requirements defined in Part 4, except those defined in paragraphs (2) and (10) of Part 4.
In addition, it shall comply with the following requirements:
(1) be an aircraft other than a fixed-wing aircraft unless tethered;
(2) if it is equipped with a geo-awareness function, comply with paragraph (10) of Part 4;
(3) during flight, provide the remote pilot with clear and concise information on the height of the UA above the surface or take-off point;
(4) unless tethered, be equipped with a low-speed mode selectable by the remote pilot and limiting the ground speed to not more than 5 m/s;
(5) unless tethered, provide means for the remote pilot to terminate the flight of the UA, which shall:
(a) be reliable, predictable and independent from the automatic flight control and guidance system; this applies also to the activation of this means;
(b) force the descent of the UA and prevent its powered horizontal displacement; and
(c) include means to reduce the effect of the UA impact dynamics;
(6) unless tethered, provide the remote pilot with means to continuously monitor the quality of the command and control link and receive an alert when it is likely that the link is going to be lost or degraded to the extent of compromising the safe conduct of the operation, and another alert when the link is lost; and

#### Result 2
Citation: [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 2 — Requirements for a class C1 Unmanned aircraft system (part 1/6)
A class C1 UAS bears the following class identification label on the UA:
A class C1 UAS shall comply with the following:
(1) be made of materials and have performance and physical characteristics such as to ensure that in the event of an impact at terminal velocity with a human head, the energy transmitted to the human head is less than 80 J, or, as an alternative, shall have an MTOM of less than 900 g, including payload;
(2) have a maximum speed in level flight of 19 m/s;
(3) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot; if the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(4) be safely controllable with regards to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;

#### Result 3
Citation: [reg-2019-945 | PART 1 — Requirements for a class C0 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 1 — Requirements for a class C0 Unmanned aircraft system (part 1/2)
A class C0 UAS bears the following class identification label on the UA:
A class C0 UAS shall comply with the following:
(1) have an MTOM of less than 250 g, including payload;
(2) have a maximum speed in level flight of 19 m/s;
(3) have a maximum attainable height above the take-off point limited to 120 m;
(4) be safely controllable with regards to stability, manoeuvrability and the command and control link performance, by a remote pilot following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;
(5) be designed and constructed in such a way as to minimise injury to people during operation, sharp edges shall be avoided, unless technically unavoidable under good design and manufacturing practice. If equipped with propellers, the UA shall be designed in such a way as to limit any injury that may be inflicted by the propeller blades;
(6) be exclusively powered by electricity;
(7) if equipped with a follow-me mode and when this function is on, be in a range not exceeding 50 m from the remote pilot, and make it possible for the remote pilot to regain control of the UA;
(8) be placed on the market with manufacturer’s instructions providing:
(a) the characteristics of the UA including but not limited to the:
class of the UA
UA mass (with a description of the reference configuration) and the maximum take-off mass (MTOM);

#### Result 4
Citation: [reg-2019-945 | PART 4 — Requirements for a class C3 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 4 — Requirements for a class C3 Unmanned aircraft system (part 1/6)
A class C3 UAS bears the following class identification label on the UA:
A class C3 UAS shall comply with the following:
(1) have an MTOM of less than 25 kg, including payload, and have a maximum characteristic dimension of less than 3 m;
(2) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot. If the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(3) be safely controllable with regard to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;
(4) in the case of a tethered UA, have a tensile length of the tether that is less than 50 m and a mechanical strength of no less than:
(a) for heavier-than-air aircraft, 10 times the weight of the aerodyne at maximum mass;
(b) for lighter-than-air aircraft, 4 times the force exerted by the combination of the maximum static thrust and the aerodynamic force of the maximum allowed wind speed in flight;

#### Result 5
Citation: [reg-2019-945 | PART 17 — Requirements for a class C6 unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 17 — Requirements for a class C6 unmanned aircraft system (part 1/2)
A class C6 UAS bears the following class identification label on the UA:
A class C6 UAS shall comply with the requirements defined in Part 4, except those defined in paragraphs (2), (7) and (10).
In addition, it shall comply with the following requirements:
have a maximum ground speed in level flight of not more than 50 m/s;
if it is equipped with a geo-awareness function, comply with paragraph (10) of Part 4;
during flight, provide the remote pilot with clear and concise information on the geographical position of the UA, its speed and its height above the surface or take-off point;
provide means to prevent the UA from breaching the horizontal and vertical limits of a programmable operational volume;
provide means for the remote pilot to terminate the flight of the UA, which shall:
(a) be reliable, predictable, independent from the automatic flight control and guidance system and independent from the means to prevent the UA from breaching the horizontal and vertical limits as required in point (4); this applies also to the activation of this means; and
(b) force the descent of the UA and prevent its powered horizontal displacement;
provide means to programme the UA trajectory;
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q21 (multi)

**Question:** I want to fly in A2 with a C2 drone. What must the drone have and what must I do as a pilot?

**Reference:** The drone must be C2 (under 4 kg, low-speed mode, direct remote ID, geo-awareness, etc.). The pilot needs a certificate of competency: online exam, self practical training, and an additional exam of at least 30 questions with 75% pass mark.

**Agent answer:**

To fly in subcategory A2 with a C2 drone, your drone and your pilot training/operations must meet the following requirements:

### What the C2 drone must have:
* **C2 Class Mark:** Bear the C2 class identification label [reg-2019-947 | UAS.OPEN.030].
* **Maximum Take-Off Mass:** Have an MTOM of less than 4 kg, including payload [reg-2019-945 | PART 3 — Requirements for a class C2 Unmanned aircraft system].
* **Height Limit:** Have its maximum attainable height above the take-off point limited to 120 m, or be equipped with a system that limits height to 120 m (or a selectable value with clear flight-information provided to the pilot) [reg-2019-945 | PART 3 — Requirements for a class C2 Unmanned aircraft system].
* **Remote ID & Geo-awareness:** Be operated with an active and updated direct remote identification system (broadcasting your operator registration number, serial number, position, speed, and pilot position) and a geo-awareness function [reg-2019-947 | UAS.OPEN.030, reg-2019-945 | PART 3 — Requirements for a class C2 Unmanned aircraft system].

### What you must do as a pilot:
* **Competency Certificate:** Hold a certificate of remote pilot competency (A2 Certificate of Competency) issued by a competent authority or designated entity. To get it, you must:
  1. Complete the online training course and pass the online theoretical knowledge examination (A1/A3 level) [reg-2019-947 | UAS.OPEN.030].
  2. Complete self-practical training under A3 operating conditions [reg-2019-947 | UAS.OPEN.030].
  3. Declare the completion of your self-practical training and pass an additional theoretical knowledge examination (at least 30 multiple-choice questions covering meteorology, flight performance, and technical/operational ground-risk mitigations) with a score of at least 75% [reg-2019-947 | UAS.OPEN.030].
* **Manufacturer's Instructions:** Be familiar with the manufacturer's instructions for the UAS [reg-2019-947 | UAS.OPEN.030].
* **Flight Distances:** Fly in a way that does not overfly uninvolved persons, maintaining a safe horizontal distance of at least **30 metres** from them [reg-2019-947 | UAS.OPEN.030]. 
* **Low Speed Mode:** You may reduce the horizontal safety distance down to a minimum of **5 metres** from an uninvolved person *only if* you operate the drone with an active low speed mode function and after evaluating the weather conditions, aircraft performance, and area segregation [reg-2019-947 | UAS.OPEN.030].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-945 | PART 3 — Requirements for a class C2 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 3 — Requirements for a class C2 Unmanned aircraft system (part 1/6)
A class C2 UAS bears the following class identification label on the UA:
A class C2 UAS shall comply with the following:
(1) have an MTOM of less than 4 kg, including payload;
(2) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot. If the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(3) be safely controllable with regard to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;
(4) have the requisite mechanical strength for the UA, including any necessary safety factor, and, where appropriate, stability to withstand any stress to which it is subjected to during use without any breakage or deformation that might interfere with its safe flight;
(5) in the case of a tethered UA, have a tensile length of the tether that is less than 50 m and a mechanical strength that is no less than:
(a) for heavier-than-air aircraft, 10 times the weight of the aerodyne at maximum mass;

#### Result 2
Citation: [reg-2019-947 | UAS.OPEN.030 UAS operations in subcategory A2]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.030 UAS operations in subcategory A2
UAS operations in subcategory A2 shall comply with all of the following conditions:
(1) be conducted in such a way that the unmanned aircraft does not overfly uninvolved persons and the UAS operations take place at a safe horizontal distance of at least 30 metres from them; the remote pilot may reduce the horizontal safety distance down to a minimum of 5 metres from an uninvolved person when operating an unmanned aircraft with an active low speed mode function and after evaluation of the situation regarding:
(a) weather conditions,
(b) performance of the unmanned aircraft,
(c) segregation of the overflown area.
(2) be performed by a remote pilot who is familiar with manufacturer’s instructions provided by the manufacturer of the UAS and holds a certificate of remote pilot competency issued by the competent authority or by an entity designated by the competent authority of a Member State. This certificate shall be obtained after complying with all of the following conditions and in the order indicated:
(a) completing an online training course and passed the online theoretical knowledge examination as referred to in point (4)(b) of point UAS.OPEN.020;
(b) completing a self-practical training in the operating conditions of the subcategory A3 set out in points (1) and (2) of point UAS.OPEN.040;
(c) declaring the completion of the self-practical training defined in point (b) and passing an additional theoretical knowledge examination provided by the competent authority or at an entity designated by the competent authority of a Member State achieving at least 75% of the overall marks. The examination shall comprise at least 30 multiple-choice questions aimed at assessing the remote pilot’s knowledge of the technical and operational mitigations for ground risk, distributed appropriately across the following subjects:
(i) meteorology;
(ii) UAS flight performance;
(iii) technical and operational mitigations for ground risk.
(3) be performed with an unmanned aircraft which is marked as class C2 and complies with the requirements of that class, as defined in Part 3 of the Annex to Delegated Regulation (EU) 2019/945, and is operated with active and updated direct remote identification system and geo-awareness function.

#### Result 3
Citation: [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 2 — Requirements for a class C1 Unmanned aircraft system (part 1/6)
A class C1 UAS bears the following class identification label on the UA:
A class C1 UAS shall comply with the following:
(1) be made of materials and have performance and physical characteristics such as to ensure that in the event of an impact at terminal velocity with a human head, the energy transmitted to the human head is less than 80 J, or, as an alternative, shall have an MTOM of less than 900 g, including payload;
(2) have a maximum speed in level flight of 19 m/s;
(3) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot; if the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(4) be safely controllable with regards to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;

#### Result 4
Citation: [reg-2019-945 | PART 4 — Requirements for a class C3 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 4 — Requirements for a class C3 Unmanned aircraft system (part 1/6)
A class C3 UAS bears the following class identification label on the UA:
A class C3 UAS shall comply with the following:
(1) have an MTOM of less than 25 kg, including payload, and have a maximum characteristic dimension of less than 3 m;
(2) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot. If the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(3) be safely controllable with regard to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;
(4) in the case of a tethered UA, have a tensile length of the tether that is less than 50 m and a mechanical strength of no less than:
(a) for heavier-than-air aircraft, 10 times the weight of the aerodyne at maximum mass;
(b) for lighter-than-air aircraft, 4 times the force exerted by the combination of the maximum static thrust and the aerodynamic force of the maximum allowed wind speed in flight;

#### Result 5
Citation: [reg-2019-945 | PART 3 — Requirements for a class C2 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 3 — Requirements for a class C2 Unmanned aircraft system (part 3/6)
(12) be exclusively powered by electricity;
(13) have a unique serial number compliant with standard ANSI/CTA-2063-A-2019, Small Unmanned Aerial Systems Serial Numbers, 2019;
(14) have a direct remote identification that:
(a) allows the upload of the UAS operator registration number required in accordance with Article 14 of Implementing Regulation (EU) 2019/947 and any additional number provided by the registration system. The system shall perform a consistency check verifying the integrity of the full string provided to the UAS operator at the time of registration. In case of inconsistency, the UAS shall emit an error message to the UAS operator;
(b) ensures, in real time during the whole duration of the flight, the direct periodic broadcast from the UA using an open and documented transmission protocol, in a way that it can be received directly by existing mobile devices within the broadcasting range, of at least the following data:
(i) the UAS operator registration number and the verification code provided by the Member State during the registration process, unless the consistency check defined in point (a) is not passed;
(ii) the unique serial number of the UA compliant with point (13);
(iii) the time stamp, the geographical position of the UA and its height above the surface or take-off point;
(iv) the route course measured clockwise from true north and ground speed of the UA;
(v) the geographical position of the remote pilot or, if not available, the take-off point; and
(vi) an indication of the emergency status of the UAS;
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q22 (multi)

**Question:** I have a C1 drone that weighs 800 g. Can I fly it in A1, and what technical features does it need to have?

**Reference:** Yes, A1 allows a C1 marked drone if operated with active and updated direct remote ID and geo-awareness, and the pilot passed the online exam. C1 requires under 80 J impact energy or under 900 g, max 19 m/s, remote ID, geo-awareness and a green flashing light.

**Agent answer:**

**Yes**, you can fly an 800 g C1 drone in subcategory A1, provided it is operated with an active and updated direct remote identification system and geo-awareness function [reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1]. *(Note: To pilot a C1 drone in subcategory A1, you must also complete the required online training and pass the online theoretical knowledge examination [reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1]).*

A class C1 UAS must meet the following technical requirements set out in Regulation (EU) 2019/945:
* **Mass/Impact limit:** Have an MTOM of less than 900 g (including payload), or be designed so that in an impact at terminal velocity with a human head, the energy transmitted is less than 80 J [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system].
* **Speed:** Have a maximum speed in level flight of 19 m/s [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system].
* **Height limitation:** Have a maximum attainable height above the take-off point limited to 120 m, or feature a system that limits height to 120 m (or a selectable value with clear height information provided to the pilot) [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system].
* **Controllability & Strength:** Be safely controllable under all anticipated operating conditions (including single system failures) and possess adequate mechanical strength and stability [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system].
* **Design for safety:** Be constructed to minimise injury to people (avoiding sharp edges and limiting propeller-blade injury) [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system].
* **C2 link loss:** Have a reliable and predictable method to recover the command and control link, or safely terminate the flight if the link is lost [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system].
* **Noise limits:** Unless it is a fixed-wing UA, meet guaranteed A-weighted sound power level limits and display the noise level indication [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system].
* **Power:** Be exclusively powered by electricity [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system].
* **Identification:** Feature a unique serial number compliant with standard ANSI/CTA-2063-A-2019, as well as an active and updated direct remote identification system and a geo-awareness function [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system, reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 2 — Requirements for a class C1 Unmanned aircraft system (part 1/6)
A class C1 UAS bears the following class identification label on the UA:
A class C1 UAS shall comply with the following:
(1) be made of materials and have performance and physical characteristics such as to ensure that in the event of an impact at terminal velocity with a human head, the energy transmitted to the human head is less than 80 J, or, as an alternative, shall have an MTOM of less than 900 g, including payload;
(2) have a maximum speed in level flight of 19 m/s;
(3) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot; if the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(4) be safely controllable with regards to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;

#### Result 2
Citation: [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 2 — Requirements for a class C1 Unmanned aircraft system (part 2/6)
(5) have the requisite mechanical strength for the UA, including any necessary safety factor, and, where appropriate, stability to withstand any stress to which it is subjected to during use without any breakage or deformation that might interfere with its safe flight;
(6) be designed and constructed in such a way as to minimise injury to people during operation, sharp edges of the UA shall be avoided, unless technically unavoidable under good design and manufacturing practice; if equipped with propellers, the UA shall be designed in such a way as to limit any injury that may be inflicted by the propeller blades;
(7) in case of a loss of the command and control link, have a reliable and predictable method for the UA to recover the command and control link or if this fails, terminate the flight in a way that reduces the effect on third parties in the air or on the ground;
(8) unless it is a fixed-wing UA, have a guaranteed A-weighted sound power level LWA determined as per Part 13 not exceeding the levels established in Part 15;
(9) unless it is a fixed-wing UA, have the indication of the guaranteed A-weighted sound power level affixed on the UA and/or its packaging as per Part 14;
(10) be exclusively powered by electricity;
(11) have a unique serial number compliant with standard ANSI/CTA-2063-A-2019, Small Unmanned Aerial Systems Serial Numbers, 2019;
(12) have a direct remote identification that:

#### Result 3
Citation: [reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.020 UAS operations in subcategory A1 (part 2/2)
(b) in the case of an unmanned aircraft class C1, as defined in Part 2 of the Annex to Delegated Regulation (EU) 2019/945, has completed an online training course followed by completing successfully an online theoretical knowledge examination provided by the competent authority or by an entity designated by the competent authority of a Member State achieving at least 75% of the overall marks. The examination shall comprise 40 multiple-choice questions distributed appropriately across the following subjects:
air safety;
airspace restrictions;
aviation regulation;
human performance limitations;
operational procedures;
UAS general knowledge;
privacy and data protection;
insurance;
security.
(5) be performed with an unmanned aircraft that:
(a) has an MTOM, including payload, of less than 250 g and a maximum operating speed of less than 19 m/s, in the case of a privately built UAS; or
(b) meets the requirements defined in point (a) of Article 20;
(c) is marked as class C0 and complies with the requirements of that class, as defined in Part 1 of the Annex to Delegated Regulation (EU) 2019/945; or
(d) is marked as class C1 and complies with the requirements of that class, as defined in Part 2 of the Annex to Delegated Regulation (EU) 2019/945 and is operated with active and updated direct remote identification system and geo-awareness function.

#### Result 4
Citation: [reg-2019-945 | PART 1 — Requirements for a class C0 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 1 — Requirements for a class C0 Unmanned aircraft system (part 1/2)
A class C0 UAS bears the following class identification label on the UA:
A class C0 UAS shall comply with the following:
(1) have an MTOM of less than 250 g, including payload;
(2) have a maximum speed in level flight of 19 m/s;
(3) have a maximum attainable height above the take-off point limited to 120 m;
(4) be safely controllable with regards to stability, manoeuvrability and the command and control link performance, by a remote pilot following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;
(5) be designed and constructed in such a way as to minimise injury to people during operation, sharp edges shall be avoided, unless technically unavoidable under good design and manufacturing practice. If equipped with propellers, the UA shall be designed in such a way as to limit any injury that may be inflicted by the propeller blades;
(6) be exclusively powered by electricity;
(7) if equipped with a follow-me mode and when this function is on, be in a range not exceeding 50 m from the remote pilot, and make it possible for the remote pilot to regain control of the UA;
(8) be placed on the market with manufacturer’s instructions providing:
(a) the characteristics of the UA including but not limited to the:
class of the UA
UA mass (with a description of the reference configuration) and the maximum take-off mass (MTOM);

#### Result 5
Citation: [reg-2019-945 | PART 4 — Requirements for a class C3 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 4 — Requirements for a class C3 Unmanned aircraft system (part 1/6)
A class C3 UAS bears the following class identification label on the UA:
A class C3 UAS shall comply with the following:
(1) have an MTOM of less than 25 kg, including payload, and have a maximum characteristic dimension of less than 3 m;
(2) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot. If the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(3) be safely controllable with regard to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;
(4) in the case of a tethered UA, have a tensile length of the tether that is less than 50 m and a mechanical strength of no less than:
(a) for heavier-than-air aircraft, 10 times the weight of the aerodyne at maximum mass;
(b) for lighter-than-air aircraft, 4 times the force exerted by the combination of the maximum static thrust and the aerodynamic force of the maximum allowed wind speed in flight;
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q23 (multi)

**Question:** How do I apply the 30 m distance rule in A2 in practice?

**Reference:** The rule requires at least 30 m horizontally (5 m with low-speed mode). The AMC measures it from the point where the UA would hit the ground in a vertical fall, and suggests the 1:1 rule (distance not less than height).

**Agent answer:**

In subcategory A2, the 30-metre horizontal distance rule is applied as follows in practice:

* **How to measure it:** The minimum horizontal distance is defined as the distance between the point where the unmanned aircraft (UA) would hit the ground in the event of a vertical fall and the position of the uninvolved person [easa-amc-gm | AMC1 UAS.OPEN.030(1) UAS operations in subcategory A2].
* **General requirement:** Under normal operations, you must maintain a safe horizontal distance of at least **30 metres** from uninvolved persons [reg-2019-947 | UAS.OPEN.030 UAS operations in subcategory A2]. 
* **The 1:1 reference rule:** As a practical reference when operating close to people, your lateral distance from any uninvolved person should not be shorter than your flight height (e.g., if you are flying at a height of 30 metres, your distance from the person must be at least 30 metres) [easa-amc-gm | AMC1 UAS.OPEN.030(1) UAS operations in subcategory A2].
* **Low-speed mode exception:** You may reduce this horizontal safety distance down to a minimum of **5 metres** from an uninvolved person *only* if the UA has an active low-speed mode function (set to 3 m/s) and you have first evaluated the weather conditions, the performance of the aircraft, and the segregation of the overflown area [reg-2019-947 | UAS.OPEN.030 UAS operations in subcategory A2].
* **Ultimate responsibility:** The safe distance is variable and depends on aircraft performance, weather, and area segregation; the remote pilot is ultimately responsible for determining this distance [easa-amc-gm | GM1 UAS.OPEN.030(1) UAS operations in subcategory A2].

*(Note: The above points reflect binding provisions from [reg-2019-947 | UAS.OPEN.030 UAS operations in subcategory A2] and acceptable means of compliance/guidance material from [easa-amc-gm | AMC1 UAS.OPEN.030(1) UAS operations in subcategory A2] and [easa-amc-gm | GM1 UAS.OPEN.030(1) UAS operations in subcategory A2].)*

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | AMC1 UAS.OPEN.040(1) Operations in subcategory A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.040(1) Operations in subcategory A3
AREAS WHERE UAS OPERATIONS IN A3 MAY BE CONDUCTED
(a) If an uninvolved person enters the range of the UAS operation, the remote pilot should, where necessary, adjust the operation to ensure the safety of the uninvolved person and discontinue the operation if the safety of the UAS operation is not ensured.
(b) A minimum horizontal distance from the person that is passing the area could be estimated as follows:
(1) no less than 30 m;
(2) no less than the height (‘1:1 rule’, i.e. if the UA is flying at a height of 30 m, the distance of the UA from the uninvolved person should be at least 30 m), and
(3) no less than the distance that the UA would cover in 2 seconds at the maximum speed (this assumes a reaction time of 2 seconds).
This minimum horizontal distance is intended to protect people on the ground, but can be extended to property and animals.

#### Result 2
Citation: [easa-amc-gm | AMC1 UAS.OPEN.030(1) UAS operations in subcategory A2]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.030(1) UAS operations in subcategory A2
SAFE DISTANCE FROM UNINVOLVED PERSONS
(a) The minimum horizontal distance of the UA from uninvolved persons should be defined as the distance between the points where the UA would hit the ground in the event of a vertical fall and the position of the uninvolved persons.
(b) As a reference, when the UA is operating in close proximity to people, the remote pilot should keep the UA at a lateral distance from any uninvolved person that is not shorter than the height (‘1:1 rule’, i.e. if the UA is flying at a height of 30 m, the distance from any uninvolved person should be at least 30 m).
(c) In any case, the distance from uninvolved persons should always be greater than:
(1) 5 m, when the low-speed mode function on the UA is activated and set to 3 m per second;
(2) 5 m, when operating a UAS balloon or airship; or
(3) 30 m in all other cases.

#### Result 3
Citation: [reg-2019-947 | UAS.OPEN.030 UAS operations in subcategory A2]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.030 UAS operations in subcategory A2
UAS operations in subcategory A2 shall comply with all of the following conditions:
(1) be conducted in such a way that the unmanned aircraft does not overfly uninvolved persons and the UAS operations take place at a safe horizontal distance of at least 30 metres from them; the remote pilot may reduce the horizontal safety distance down to a minimum of 5 metres from an uninvolved person when operating an unmanned aircraft with an active low speed mode function and after evaluation of the situation regarding:
(a) weather conditions,
(b) performance of the unmanned aircraft,
(c) segregation of the overflown area.
(2) be performed by a remote pilot who is familiar with manufacturer’s instructions provided by the manufacturer of the UAS and holds a certificate of remote pilot competency issued by the competent authority or by an entity designated by the competent authority of a Member State. This certificate shall be obtained after complying with all of the following conditions and in the order indicated:
(a) completing an online training course and passed the online theoretical knowledge examination as referred to in point (4)(b) of point UAS.OPEN.020;
(b) completing a self-practical training in the operating conditions of the subcategory A3 set out in points (1) and (2) of point UAS.OPEN.040;
(c) declaring the completion of the self-practical training defined in point (b) and passing an additional theoretical knowledge examination provided by the competent authority or at an entity designated by the competent authority of a Member State achieving at least 75% of the overall marks. The examination shall comprise at least 30 multiple-choice questions aimed at assessing the remote pilot’s knowledge of the technical and operational mitigations for ground risk, distributed appropriately across the following subjects:
(i) meteorology;
(ii) UAS flight performance;
(iii) technical and operational mitigations for ground risk.
(3) be performed with an unmanned aircraft which is marked as class C2 and complies with the requirements of that class, as defined in Part 3 of the Annex to Delegated Regulation (EU) 2019/945, and is operated with active and updated direct remote identification system and geo-awareness function.

#### Result 4
Citation: [easa-amc-gm | GM1 UAS.OPEN.030(1) and UAS.OPEN.040(1) UAS operations in subcategories A1 and A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 UAS.OPEN.030(1) and UAS.OPEN.040(1) UAS operations in subcategories A1 and A3
DIFFERENCE BETWEEN SUB-CATEGORIES A2 AND A3
Subcategory A2 addresses operations during which flying close to people is intended for a significant portion of the flight. The minimum distance ranges from 30 m to 5 m from uninvolved people. 5 m is only allowed when there is an active low-speed mode function on the UA, and the remote pilot has conducted an evaluation of the situation regarding the weather, the performance of the UA and the segregation of the overflown area.
Sub-category A3 addresses operations that are conducted in an area (hereafter referred to as ‘the area’) where the remote pilot reasonably expects that no uninvolved people will be endangered within the range of the unmanned aircraft where it is flown during the mission. In addition, the operation must be conducted at a safe horizontal distance of at least 150 m from residential, commercial, industrial or recreational areas.

#### Result 5
Citation: [easa-amc-gm | GM1 UAS.OPEN.030(1) UAS operations in subcategory A2]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 UAS.OPEN.030(1) UAS operations in subcategory A2
SAFE DISTANCE FROM UNINVOLVED PERSONS
The safe distance of the UA from uninvolved persons is variable and is heavily dependent on the performance and characteristics of the UAS involved, the weather conditions and the segregation of the overflown area. The remote pilot is ultimately responsible for the determination of this distance.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q24 (multi)

**Question:** Where do I register as an operator and what will my registration number look like?

**Reference:** Register in the Member State of your residence (only one at a time). The number has 16 alphanumerics, starting with the 3-letter ISO country code, plus 3 secret digits to upload to the remote ID.

**Agent answer:**

You must register yourself as a UAS operator in the **Member State where you have your residence** (if you are a natural person) or your **principal place of business** (if you are a legal person) [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]. Registration is carried out through the digital system established by the competent national aviation authority of that Member State [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]. You cannot be registered in more than one Member State at a time [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS].

### What your registration number will look like:
Your unique digital **UAS operator registration number** consists of **sixteen (16) alphanumerics** in total, arranged as follows [easa-amc-gm | AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS]:
1. The first **three (3) upper-case letters** corresponding to the ISO 3166 Alpha-3 country code of your Member State of registration (e.g., `FIN` for Finland) [easa-amc-gm | AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS].
2. Followed by **twelve (12) randomly generated lower-case alphanumeric characters** [easa-amc-gm | AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS].
3. One (1) final **checksum character** generated using the Luhn-mod-36 algorithm [easa-amc-gm | AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS].

*Example:* `FIN87astrdge12k8` [easa-amc-gm | GM1 to AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS]

Additionally, upon registration, the Member State will provide you with **three (3) additional randomly generated lower-case "secret digits"** separated by a hyphen (e.g., `-xyz`) to form the full registration string (`FIN87astrdge12k8-xyz`) [easa-amc-gm | GM1 to AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS, easa-amc-gm | AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS]. You must display the main operator registration number on your unmanned aircraft, and upload the full string (including the secret digits) into your drone's electronic identification system if available [easa-amc-gm | GM1 to AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS, easa-amc-gm | AMC1 Article 14(8) Registration of UAS operators and ‘certified’ UAS].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | GM1 to AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 to AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS
UAS OPERATOR REGISTRATION NUMBER
An example of a UAS operator registration number as defined in point (a) of AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS is ‘FIN87astrdge12k8’, where:
‘FIN’ is the ISO 3166 Alpha-3 code of Finland;
‘87astrdge12k’ is an example of the twelve (12) alphanumerics, as defined in point (a)(2) of AMC1 Article 14(6); and
‘8’ is the checksum, i.e. the result of the application of the Luhn-mod-36 algorithm to the fifteen (15) alphanumerics that result from the concatenation of the twelve (12) alphanumerics of the UAS operator registration number and the three (3) randomly generated alphanumerics (‘secret digits’, as defined in point (b) of AMC1 Article 14(6)): ‘87astrdge12kxyz’.
An example of the full registration string, as defined in point (e) of AMC1 Article 14(6), to be provided by a Member State, is ‘FIN87astrdge12k8-xyz’, where:
‘FIN87astrdge12k8’ is the UAS operator registration number; and
‘xyz’ is an example of the three (3) randomly generated ‘secret digits’.
The UAS operator must upload the UAS registration number and the three (3) ‘secret digits’ into the remote identification system of the UAS, if available, or into the electronic-identification system, if required by the geographical zone.
The UAS operator should not share with anybody the three (3) ‘secret digits’ that are used to enhance the protection of the UAS operator registration number from being illegally uploaded into a UA.

#### Result 2
Citation: [easa-amc-gm | AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS
UAS OPERATOR REGISTRATION NUMBER
(a) The unique UAS operator digital registration number that is issued by the Member States should consist of sixteen (16) alphanumerics in total, arranged as follows:
(1) the first three (3) alphanumerics (upper-case only) corresponding to the ISO 3166 Alpha3 code of the Member State of registration;
(2) followed by twelve (12) randomly generated characters that consist of alphanumerics (lower-case only); and
(3) one (1) character corresponding to the checksum that is generated in line with point (c).
(b) The Member States should randomly generate three (3) additional alphanumerics (lower-case only) called ‘secret digits’.
(c) The Member States should generate a checksum by applying the Luhn-mod-36 algorithm to the fifteen (15) alphanumerics that result from the concatenation, in the following order, of:
(1) the twelve (12) alphanumerics of the UAS operator registration number defined in point (a)(2); and
(2) the three (3) randomly generated ‘secret digits’ that are defined in point (b).
(d) For the Luhn-mod-36 algorithm, the mapping of the alphanumerics to the code-points should start with digits that are followed by lower-case letters, as shown below:
Alphanumeric | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | a | b | c | d | e | f | … | z
Code-point | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | … | 35
(e) At the time of registration, the Member State should provide the UAS operator with the full registration string that consists, in the following order, of:
(1) the UAS operator registration number as defined in point (a); and
(2) the three (3) randomly generated ‘secret digits’, separated by a hyphen ‘-’ (ASCII code [DEC] 45).

#### Result 3
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 3/3)
The nationality and registration mark of an unmanned aircraft shall be established in line with ICAO Annex 7. An unmanned aircraft cannot be registered in more than one State at a time.
8. The UAS operators shall display their registration number on every unmanned aircraft meeting the conditions described in paragraph 5.
9. In addition to the data defined in point (2) Member States may collect additional identity information from the UAS operators.

#### Result 4
Citation: [easa-amc-gm | AMC1 Article 14(8) Registration of UAS operators and ‘certified’ UAS]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 14(8) Registration of UAS operators and ‘certified’ UAS
DISPLAY OF REGISTRATION INFORMATION
(a) If the UAS operator owns the UAS or uses a UAS that is owned by a third party, it should:
(1) register itself;
(2) display on the UA the UAS operator registration number, which is received at the end of the registration process, in a way that the number is readable at least when the UA is on the ground, without using other devices than eyeglasses or corrective lenses; and
(3) upload the full string, which consists of the UAS operator registration number and the three (3) randomly generated alphanumerics, into the electronic identification system, if available.
(b) A QR code (quick response code) may be used.
(c) If the size of the UA does not allow the mark to be displayed in a visible way on the fuselage, or the UA represents a real aircraft where affixing the marking on the UA would spoil the realism of the representation, a marking inside the battery compartment is acceptable if the compartment is accessible.

#### Result 5
Citation: [easa-amc-gm | AMC2 UAS.OPEN.020(4)(b) and UAS.OPEN.040(3) UAS operations in subcategories A1 and A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC2 UAS.OPEN.020(4)(b) and UAS.OPEN.040(3) UAS operations in subcategories A1 and A3
PROOF OF COMPLETION OF THE ONLINE THEORETICAL KNOWLEGDE TRAINING COURSE AND SUCCESSFUL COMPLETION OF THE ONLINE THEORETICAL KNOWLEGDE EXAMINATION
Upon receipt of the proof that a remote pilot has successfully completed the online theoretical knowledge training course and the online theoretical knowledge examination, the competent authority should provide a proof of completion to the remote pilot in the format that is depicted in the figure below. An entity that is designated by the competent authority may issue the certificate on behalf of the competent authority. The proof may be provided in electronic form.
The remote pilot identification number that is provided by the competent authority or the entity that is designated by the competent authority that issues the proof of completion should have the following format:
NNN-RP-xxxxxxxxxxxx
Where:
‘NNN’ is the ISO 3166 Alpha-3 code of the MS that issues the proof of completion;
‘RP’ is a fixed field meaning ‘remote pilot’; and
‘xxxxxxxxxxxx’ are 12 alphanumeric characters (lower-case only) defined by the competent authority or the entity that is designated by the competent authority that issues the proof of completion.
Example: (FIN-RP-123456789abc)
The QR code provided a link to the national database where the information related to the remote pilot is stored. Through the ‘remote pilot identification number’, all information related to the training of the remote pilot can be retrieved by authorised bodies (e.g. competent authorities, law enforcement authorities, etc.) and authorised personnel.
#### Result 1
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 2/3)
4. Member States shall ensure that registration systems are digital and interoperable and allow for mutual access and exchange of information through the repository referred to in Article 74 of Regulation (EU) 2018/1139.
5. UAS operators shall register themselves:
(a) when operating within the ‘open’ category any of the following unmanned aircraft:
i. with a MTOM of 250 g or more, or, which in the case of an impact can transfer to a human kinetic energy above 80 Joules;
ii. that is equipped with a sensor able to capture personal data, unless it complies with Directive 2009/48/EC.
(b) when operating within the ‘specific’ category an unmanned aircraft of any mass.
6. UAS operators shall register themselves in the Member State where they have their residence for natural persons or where they have their principal place of business for legal persons and ensure that their registration information is accurate. A UAS operator cannot be registered in more than one Member State at a time.
Member States shall issue a unique digital registration number for UAS operators and for the UAS that require registration, allowing their individual identification.
The registration number for UAS operators shall be established on the basis of standards that support the interoperability of the registration systems;
7. The owner of an unmanned aircraft whose design is subject to certification shall register the unmanned aircraft.

#### Result 2
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 1/3)
1. Member States shall establish and maintain accurate registration systems for UAS whose design is subject to certification and for UAS operators whose operation may present a risk to safety, security, privacy, and protection of personal data or environment.
2. The registration systems for UAS operators shall provide the fields for introducing and exchanging the following information:
(a) the full name and the date of birth for natural persons and the name and their identification number for legal persons;
(b) the address of UAS operators;
(c) their email address and telephone number;
(d) an insurance policy number for UAS if required by Union or national law;
(e) the confirmation by legal persons of the following statement: ‘All personnel directly involved in the operations are competent to perform their tasks, and the UAS will be operated only by remote pilots with the appropriate level of competency’;
(f) operational authorisations and LUCs held and declarations followed by a confirmation in accordance with Article 12(5)(b).
3. The registration systems for unmanned aircraft whose design is subject to certification shall provide the fields for introducing and exchanging the following information:
(a) manufacturer’s name;
(b) manufacturer’s designation of the unmanned aircraft;
(c) unmanned aircraft’s serial number;
(d) full name, address, email address and telephone number of the natural or legal person under whose name the unmanned aircraft is registered.

#### Result 3
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 3/3)
The nationality and registration mark of an unmanned aircraft shall be established in line with ICAO Annex 7. An unmanned aircraft cannot be registered in more than one State at a time.
8. The UAS operators shall display their registration number on every unmanned aircraft meeting the conditions described in paragraph 5.
9. In addition to the data defined in point (2) Member States may collect additional identity information from the UAS operators.

#### Result 4
Citation: [easa-amc-gm | AMC1 Article 14 Registration of UAS operators and ‘certified’ UAS]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 14 Registration of UAS operators and ‘certified’ UAS
NATIONAL CONTACT POINT FOR ACCESSING AND EXERCISING THE RIGHTS
The competent authority should identify and publish the contact point for accessing and exercising the rights in accordance with Regulation (EU) 2016/679 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data.

#### Result 5
Citation: [easa-amc-gm | GM1 Article 14(1) Registration of UAS operators and ‘certified’ UAS]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 Article 14(1) Registration of UAS operators and ‘certified’ UAS
ACCURACY OF THE REGISTRATION SYSTEMS
UAS operators, when registering themselves or their certified UAS, are required to provide accurate information and update the registration data when it changes.
Member States are required to keep that information and registration data accurate in their registration systems.
An example of data that may change over time is:
a UAS operator address, email address, and telephone number; and
the validity of the insurance policy for the UAS.
To verify the validity of the insurance policy, Member States may require, at the time of registration, the UAS operator to provide the expiry date of the insurance policy and to consider the registration invalid after that date.
UAS operators, especially those conducting UAS operations for leisure, may decide to fly their UAS only for a short period; therefore, it is possible that even if the database of a registration system contains many registered UAS operators, only some of them are active. Member States may define a duration period for the validity of registration of all UAS operators and may revoke the registration number if the UAS operator does not renew that number before it expires. Member States may also decide to suspend or revoke the registration number if the UAS operator’s conduct justifies such a measure.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q25 (multi)

**Question:** I changed the parts of my C1 drone. Can I still fly it in A1 as a C1?

**Reference:** A1 with a C1 requires the drone to be marked C1 and comply with its class. Replacing parts with similar original or manufacturer-listed parts is fine, but modifications that breach compliance invalidate the class and the drone may then only be operated in the specific category.

**Agent answer:**

Whether you can still fly it in A1 as a C1 depends on the type of parts and how the changes were made:

* **Maintenance (Allowed):** Replacing a part with a similar one for maintenance purposes is **not** considered a modification, provided you use an original part or a part that complies with the characteristics defined by the manufacturer in their list of replaceable parts [easa-amc-gm | AMC1 UAS.OPEN.020(5)(c) and (d), UAS.OPEN.030(3) and UAS.OPEN.040(4)(c),(d) and (e)]. Replacing a component with another having the exact same physical and functional characteristics (such as a propeller of the same design) does not breach compliance [easa-amc-gm | GM1 UAS.OPEN.020(5)(c) and (d), UAS.OPEN.030(3) and UAS.OPEN.040(4)(c), (d) and (e)].
* **Modifications (Not Allowed):** If you make modifications that breach compliance with the product requirements or affect the weight and performance outside the manufacturer's user manual specifications, it invalidates the class conformity [easa-amc-gm | AMC1 UAS.OPEN.020(5)(c) and (d), UAS.OPEN.030(3) and UAS.OPEN.040(4)(c),(d) and (e), easa-amc-gm | GM1 UAS.OPEN.020(5)(c) and (d), UAS.OPEN.030(3) and UAS.OPEN.040(4)(c), (d) and (e)]. 

If the modification invalidates the class conformity, **the class identification label must be removed**, and the modified drone may no longer be operated in the open category as a C1, but only in the specific category (unless it qualifies as a privately built UAS under subcategory A3) [easa-amc-gm | AMC1 UAS.OPEN.020(5)(c) and (d), UAS.OPEN.030(3) and UAS.OPEN.040(4)(c),(d) and (e)].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | AMC1 UAS.OPEN.020(5)(c) and (d), UAS.OPEN.030(3) and UAS.OPEN.040(4)(c),(d) and (e) UAS operations in subcategories A1, A2 and A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.020(5)(c) and (d), UAS.OPEN.030(3) and UAS.OPEN.040(4)(c),(d) and (e) UAS operations in subcategories A1, A2 and A3
MODIFICATION OF A UAS WITH A CLASS IDENTIFICATION LABEL
When placing UASs with a class identification label on the market, manufacturers should ensure the compliance of those UASs with the applicable regulatory requirements. It is the responsibility of UAS operators to ensure that those UASs remain compliant throughout their lifetime. UAS operators should, therefore, not make any modifications to a UAS in class C0, C1, C2, C3 or C4 that breach compliance with the product requirements, unless the modification is foreseen by the manufacturer and documented in the manufacturer’s instructions.
The replacement of a part by a similar one for maintenance purposes is not considered a modification, provided the operator uses an original part or a part that complies with the characteristics defined by the manufacturer in the list of replaceable parts provided in the manufacturer’s instructions.
The affixation of payload is not considered a modification provided that affixing a payload is not forbidden by the manufacturer and the payload complies with the characteristics provided in the manufacturer’s instructions. Affixing a payload when it is forbidden by the manufacturer or affixing a payload that does not comply with the characteristics provided in the manufacturer’s instructions is strictly forbidden.
If the payload does not comply with the characteristics of the allowed payloads or if maintenance is not performed according to the manufacturer’s instructions, it is then considered a modification that invalidates the class conformity. The class identification label must be removed from the UAS identification label and the modified UAS may only be operated in the ‘specific’ category in accordance with Subpart B of Annex to the UAS Regulation.
Changes to UASs with a class identification label C4 are allowed, and such UASs can be considered ‘privately built’ UASs and continue to be operated in subcategory A3 of the ‘open’ category.

#### Result 2
Citation: [easa-amc-gm | GM1 UAS.OPEN.020(5)(c) and (d), UAS.OPEN.030(3) and UAS.OPEN.040(4)(c), (d) and (e) UAS operations in subcategories A1, A2 and A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 UAS.OPEN.020(5)(c) and (d), UAS.OPEN.030(3) and UAS.OPEN.040(4)(c), (d) and (e) UAS operations in subcategories A1, A2 and A3
MODIFICATION OF A UAS WITH A CE CLASS MARK
Modifications to UAS that breach compliance with the requirements for the CE marking are those that affect the weight or performance so that they are outside the specifications or the instructions provided by the manufacturer in the user manual. A replacement of a part with another that has the same physical and functional characteristics is not considered to be a breach of the requirements for the CE marking (e.g. a replacement of a propeller with another of the same design). The UA user manual should define instructions for performing maintenance and applying changes that do not breach compliance with the CE marking requirements.

#### Result 3
Citation: [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 2 — Requirements for a class C1 Unmanned aircraft system (part 1/6)
A class C1 UAS bears the following class identification label on the UA:
A class C1 UAS shall comply with the following:
(1) be made of materials and have performance and physical characteristics such as to ensure that in the event of an impact at terminal velocity with a human head, the energy transmitted to the human head is less than 80 J, or, as an alternative, shall have an MTOM of less than 900 g, including payload;
(2) have a maximum speed in level flight of 19 m/s;
(3) have a maximum attainable height above the take-off point limited to 120 m or be equipped with a system that limits the height above the surface or above the take-off point to 120 m or to a value selectable by the remote pilot; if the value is selectable, clear information about the height of the UA above the surface or take-off point during flight shall be provided to the remote pilot;
(4) be safely controllable with regards to stability, manoeuvrability and the command and control link performance, by a remote pilot with adequate competency as defined in Implementing Regulation (EU) 2019/947 and following the manufacturer’s instructions, as necessary under all anticipated operating conditions including following the failure of one or, if appropriate, more systems;

#### Result 4
Citation: [easa-amc-gm | GM1 UAS.OPEN.040(4) UAS operations in subcategory A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 UAS.OPEN.040(4) UAS operations in subcategory A3
USE OF UASs WITH A CLASS C0 OR C1 CLASS IDENTIFICATION LABEL IN SUBCATEGORY A3
Since subcategory A3 UAS operations are conducted at a 150-m distance from residential, commercial, and industrial areas, where no uninvolved persons are endangered, subcategory A3 encompass subcategory A1 (operations that are not conducted over assemblies of people and over uninvolved people). Therefore, UAS operations in subcategory A3 may also be conducted with an UA with:
(a) a class C0 class identification label that complies with the requirements of Part 1 of the Annex to Regulation (EU) 2019/945; or
(b) a class C1 class identification label that complies with the requirements of Part 1 of the Annex to Regulation (EU) 2019/945, as well as with an active and updated direct remote identification system and a geo-awareness function.

#### Result 5
Citation: [reg-2019-947 | UAS.OPEN.020 UAS operations in subcategory A1]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.020 UAS operations in subcategory A1 (part 2/2)
(b) in the case of an unmanned aircraft class C1, as defined in Part 2 of the Annex to Delegated Regulation (EU) 2019/945, has completed an online training course followed by completing successfully an online theoretical knowledge examination provided by the competent authority or by an entity designated by the competent authority of a Member State achieving at least 75% of the overall marks. The examination shall comprise 40 multiple-choice questions distributed appropriately across the following subjects:
air safety;
airspace restrictions;
aviation regulation;
human performance limitations;
operational procedures;
UAS general knowledge;
privacy and data protection;
insurance;
security.
(5) be performed with an unmanned aircraft that:
(a) has an MTOM, including payload, of less than 250 g and a maximum operating speed of less than 19 m/s, in the case of a privately built UAS; or
(b) meets the requirements defined in point (a) of Article 20;
(c) is marked as class C0 and complies with the requirements of that class, as defined in Part 1 of the Annex to Delegated Regulation (EU) 2019/945; or
(d) is marked as class C1 and complies with the requirements of that class, as defined in Part 2 of the Annex to Delegated Regulation (EU) 2019/945 and is operated with active and updated direct remote identification system and geo-awareness function.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q26 (multi)

**Question:** What lights must a C1 drone have and what must the pilot do with them at night?

**Reference:** A C1 UAS must have lights for controllability and at least one green flashing light for night conspicuity. At night the remote pilot must ensure the green flashing light is activated.

**Agent answer:**

A C1 drone must be equipped with:
1. **Lights for controllability** of the unmanned aircraft [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system].
2. **At least one green flashing light** for night conspicuity, allowing people on the ground to distinguish the drone from a manned aircraft [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system].

**What the pilot must do at night:**
When operating at night, the remote pilot must ensure that the green flashing light on the unmanned aircraft is **activated** [reg-2019-947 | UAS.OPEN.060 Responsibilities of the remote pilot].

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 2 — Requirements for a class C1 Unmanned aircraft system (part 4/6)
(a) an interface to load and update data containing information on airspace limitations related to UA position and height imposed by the UAS geographical zones, as defined by Article 15 of Implementing Regulation (EU) 2019/947, which ensures that the process of loading or updating such data does not degrade its integrity and validity;
(b) a warning alert to the remote pilot when a potential breach of airspace limitations is detected; and
(c) information to the remote pilot on the UA’s status as well as a warning alert when its positioning or navigation systems cannot ensure the proper functioning of the geoawareness function;
(14) if the UA has a function that limits its access to certain airspace areas or volumes, this function shall operate in such a manner that it interacts smoothly with the flight control system of the UA without adversely affecting flight safety; in addition, clear information shall be provided to the remote pilot when this function prevents the UA from entering these airspace areas or volume;
(15) provide the remote pilot with a clear warning when the battery of the UA or its CMU reaches a low level to allow the remote pilot sufficient time to safely land the UA;
(16) be equipped:
(a) with lights for the purpose of controllability of the UA; and
(b) with at least one green flashing light for the purpose of conspicuity of the UA at night to allow a person on the ground to distinguish the UA from a manned aircraft;

#### Result 2
Citation: [reg-2019-945 | PART 3 — Requirements for a class C2 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 3 — Requirements for a class C2 Unmanned aircraft system (part 5/6)
(b) with at least one green flashing light for the purpose of conspicuity of the UA at night to allow a person on the ground, to distinguish the UA from a manned aircraft;
(19) be placed on the market with manufacturer’s instructions providing:
(a) the characteristics of the UA including but not limited to the:
class of the UA;
UA mass (with a description of the reference configuration) and the maximum take-off mass (MTOM);
general characteristics of allowed payloads in terms of mass, dimensions, interfaces with the UA and other possible restrictions;
equipment and software to control the UA remotely;
the procedures to upload the UAS operator registration number into the remote identification system;
reference of the transmission protocol used for the direct remote identification system emission;
sound power level; and
description of the behaviour of the UA in case of a loss of the command and control link, and the method to recover the command and control link of the UA; and
(b) clear operational instructions;
(c) the procedure to upload the airspace limitations into the geo-awareness function;
(d) maintenance instructions;
(e) troubleshooting procedures;
(f) operational limitations (including but not limited to meteorological conditions and day/night operations); and
(g) appropriate description of all the risks related to UAS operations;
(20) include an information notice published by EASA providing the applicable limitations and obligations, in accordance with Implementing Regulation (EU) 2019/947;
(21) if equipped with a network remote identification system it shall:

#### Result 3
Citation: [reg-2019-945 | PART 4 — Requirements for a class C3 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 4 — Requirements for a class C3 Unmanned aircraft system (part 4/6)
(11) if the UA has a function that limits its access to certain airspace areas or volumes, this function shall operate in such a manner that it interacts smoothly with the flight control system of the UA without adversely affecting flight safety; in addition, clear information shall be provided to the remote pilot when this function prevents the UA from entering these airspace areas or volumes;
(12) unless tethered, be equipped with a command and control link protected against unauthorised access to the command and control functions;
(13) provide the remote pilot with a clear warning when the battery of the UA or its CMU reaches a low level to allow the remote pilot sufficient time to safely land the UA;
(14) be equipped:
(a) with lights for the purpose of controllability of the UA; and
(b) with at least one green flashing light for the purpose of conspicuity of the UA at night to allow a person on the ground to distinguish the UA from a manned aircraft;
(15) be placed on the market with manufacturer’s instructions providing:
(a) the characteristics of the UA including but not limited to the:
class of the UA;
UA mass (with a description of the reference configuration) and the maximum take-off mass (MTOM);
general characteristics of allowed payloads in terms of mass, dimensions, interfaces with the UA and other possible restrictions;
equipment and software to control the UA remotely;
the procedures to upload the UAS operator registration number into the remote identification system;

#### Result 4
Citation: [reg-2019-947 | UAS.SPEC.050 Responsibilities of the UAS operator]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.SPEC.050 Responsibilities of the UAS operator (part 4/4)
(iii) using an unmanned aircraft which is designed to minimise noise and other emissions, taking into account the type of the intended operations and geographical areas where the aircraft noise and other emissions are of concern.
(j) establish and keep an up-to-date list of the designated remote pilots for each flight;
(k) establish and keep an up-to-date list of the maintenance staff employed by the operator to carry out maintenance activities; and
(l) ensure that each individual unmanned aircraft is installed with:
(i) at least one green flashing light for the purpose of visibility of the unmanned aircraft at night, and
(ii) an active and up-to-date remote identification system.

#### Result 5
Citation: [easa-amc-gm | AMC3 UAS.SPEC.050(1)(d) Responsibilities of the UAS operator]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC3 UAS.SPEC.050(1)(d) Responsibilities of the UAS operator (part 4/18)
Turning off the front green flashing light might improve the view because there will be no reflection in the on-board camera. Recognise that the IR camera does not help in case of rain/humidity, and that the IR visibility significantly decreases. Explain the use of the green flashing light at night. Explain the use of navigation lights, position lights, anti-collision lights, and other lights for UA controllability. Explain the use of lights (e.g. navigation, position, or anti-collision lights) for recognising the presence of manned aircraft. Rationale: Those lights show where the UA is positioned and the direction in which the UA is aligned. For manned aircraft, a red navigation light is located on the leading edge of the left-wing tip and a green navigation light on the leading edge of the rightwing tip (for helicopters, on the left and right sides of the cockpit). A white navigation light is positioned on the tail as far aft as possible. High-intensity strobe lights are also located in those positions. They are used as anti-collision lights and flash twice after a short break. A red rotating beacon is also part of the anti-collision lights.
Degradation of visual acuity | Recognise that flying the UA at night degrades visual perception. Recognise night myopia, caused by the increasing pupil size. At low-light levels, without distant objects to focus on, the focusing mechanism of the eye may go to a resting myopic position. If night-vision goggles are used, know how they function.
#### Result 1
Citation: [reg-2019-947 | UAS.OPEN.060 Responsibilities of the remote pilot]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.060 Responsibilities of the remote pilot (part 2/2)
(b) keep the unmanned aircraft in VLOS and maintain a thorough visual scan of the airspace surrounding the unmanned aircraft in order to avoid any risk of collision with any manned aircraft. The remote pilot shall discontinue the flight if the operation poses a risk to other aircraft, people, animals, environment or property;
(c) comply with the operational limitations in geographical zones defined in accordance with Article 15;
(d) have the ability to maintain control of the unmanned aircraft, except in the case of a lost link or when operating a free-flight unmanned aircraft;
(e) operate the UAS in accordance with manufacturer’s instructions provided by the manufacturer, including any applicable limitations;
(f) comply with the operator’s procedures when available;
(g) when operating at night, ensure that a green flashing light on the unmanned aircraft is activated.
(3) During the flight, remote pilots and UAS operators shall not fly close to or inside areas where an emergency response effort is ongoing unless they have permission to do so from the responsible emergency response services.
(4) For the purposes of point (2)(b), remote pilots may be assisted by an unmanned aircraft observer. In such case, clear and effective communication shall be established between the remote pilot and the unmanned aircraft observer.

#### Result 2
Citation: [easa-amc-gm | AMC3 UAS.SPEC.050(1)(d) Responsibilities of the UAS operator]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC3 UAS.SPEC.050(1)(d) Responsibilities of the UAS operator (part 4/18)
Turning off the front green flashing light might improve the view because there will be no reflection in the on-board camera. Recognise that the IR camera does not help in case of rain/humidity, and that the IR visibility significantly decreases. Explain the use of the green flashing light at night. Explain the use of navigation lights, position lights, anti-collision lights, and other lights for UA controllability. Explain the use of lights (e.g. navigation, position, or anti-collision lights) for recognising the presence of manned aircraft. Rationale: Those lights show where the UA is positioned and the direction in which the UA is aligned. For manned aircraft, a red navigation light is located on the leading edge of the left-wing tip and a green navigation light on the leading edge of the rightwing tip (for helicopters, on the left and right sides of the cockpit). A white navigation light is positioned on the tail as far aft as possible. High-intensity strobe lights are also located in those positions. They are used as anti-collision lights and flash twice after a short break. A red rotating beacon is also part of the anti-collision lights.
Degradation of visual acuity | Recognise that flying the UA at night degrades visual perception. Recognise night myopia, caused by the increasing pupil size. At low-light levels, without distant objects to focus on, the focusing mechanism of the eye may go to a resting myopic position. If night-vision goggles are used, know how they function.

#### Result 3
Citation: [reg-2019-947 | UAS.SPEC.050 Responsibilities of the UAS operator]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.SPEC.050 Responsibilities of the UAS operator (part 4/4)
(iii) using an unmanned aircraft which is designed to minimise noise and other emissions, taking into account the type of the intended operations and geographical areas where the aircraft noise and other emissions are of concern.
(j) establish and keep an up-to-date list of the designated remote pilots for each flight;
(k) establish and keep an up-to-date list of the maintenance staff employed by the operator to carry out maintenance activities; and
(l) ensure that each individual unmanned aircraft is installed with:
(i) at least one green flashing light for the purpose of visibility of the unmanned aircraft at night, and
(ii) an active and up-to-date remote identification system.

#### Result 4
Citation: [reg-2019-945 | PART 2 — Requirements for a class C1 Unmanned aircraft system]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)

PART 2 — Requirements for a class C1 Unmanned aircraft system (part 4/6)
(a) an interface to load and update data containing information on airspace limitations related to UA position and height imposed by the UAS geographical zones, as defined by Article 15 of Implementing Regulation (EU) 2019/947, which ensures that the process of loading or updating such data does not degrade its integrity and validity;
(b) a warning alert to the remote pilot when a potential breach of airspace limitations is detected; and
(c) information to the remote pilot on the UA’s status as well as a warning alert when its positioning or navigation systems cannot ensure the proper functioning of the geoawareness function;
(14) if the UA has a function that limits its access to certain airspace areas or volumes, this function shall operate in such a manner that it interacts smoothly with the flight control system of the UA without adversely affecting flight safety; in addition, clear information shall be provided to the remote pilot when this function prevents the UA from entering these airspace areas or volume;
(15) provide the remote pilot with a clear warning when the battery of the UA or its CMU reaches a low level to allow the remote pilot sufficient time to safely land the UA;
(16) be equipped:
(a) with lights for the purpose of controllability of the UA; and
(b) with at least one green flashing light for the purpose of conspicuity of the UA at night to allow a person on the ground to distinguish the UA from a manned aircraft;

#### Result 5
Citation: [easa-amc-gm | AMC3 UAS.SPEC.050(1)(d) Responsibilities of the UAS operator]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC3 UAS.SPEC.050(1)(d) Responsibilities of the UAS operator (part 3/18)
Night operations | General | Recognise the meaning of the definition of ‘night’ or other similar wording that is used for night flight. Rationale: In Regulation (EU) No 1178/2011 (the ‘Aircrew Regulation’), ‘night’ for manned aviation ‘means the period between the end of evening civil twilight and the beginning of morning civil twilight or such other period between sunset and sunrise as may be prescribed by the appropriate authority’. Some national laws use the sunset and sunrise times for the definition of a night flight. ‘Sunset’ is defined as the daily disappearance of the upper limb of the sun below the horizon. This time depends on the latitude and longitude of the viewpoint. There are many websites and apps to find out the sunset and sunrise times at a specific location. Recognise the benefits of illuminating the operational area, especially during the critical phases of take-off and landing. Recognise that during night flight it is hard to estimate the distance between the UA and other obstacles if visibility is only ensured by the lights of the UA. Recognise that a visual obstacle avoidance system may be less accurate in night-time operations. Understand that if the sight of the UA is lost at night, return-to-home (RTH) should be immediately followed. Rationale: During daytime, it is sometimes difficult to see the position of the UA, which is even more difficult at night. Recognise that an infrared radiation (IR) camera allows one to see enough at night.
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q27 (unanswerable)

**Question:** Do I need to use U-space services to fly in a U-space zone over Madrid?

**Reference:** Not covered; U-space rules are not in the corpus. Ask AESA or check the national UAS geographical zones.

**Agent answer:**

The corpus does not cover this. 

Regulations (EU) 2019/947 and (EU) 2019/945 and their associated EASA Acceptable Means of Compliance and Guidance Material do not contain rules regarding specific U-space regulations, implementation details, or national airspace structures over Madrid. U-space regulations (such as Regulations (EU) 2021/664, 2021/665, and 2021/666) are not included in the provided corpus.

For specific requirements on flying in a U-space airspace over Madrid, you should consult Spain's national aviation authority (AESA — *Agencia Estatal de Seguridad Aérea*) or ENAIRE (the national air navigation service provider).

**Guardrail:** none

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | GM1 Article 15(3) Operational conditions for UAS geographical zones]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 Article 15(3) Operational conditions for UAS geographical zones (part 2/2)
UAS geographical zones where UAS operations are limited and subject to the fulfilment of a set of conditions that are imposed for such zones. Such limitations and conditions may concern administrative procedures, operational limitations, or technical requirements for the UAS or mandatory functions. For example, UAS operations are permitted in such UAS geographical zones if the UAS MTOM does not exceed 1.5 kg and the flight altitude is below 50 m above the ground.
UAS geographical zones that facilitate UAS operations in the ‘open’ category (UAS operations are exempt from one or more of the ‘open’ category requirements).
U-space airspace where UAS operations are supported by a set of Uspace services. UAS operations are compliant with the capability and performance requirements that are determined for the particular U-space airspace. The Member States should list the U-space service provider(s) (USSP(s)) that is (are) identified for that geographical zone.
Riga flight information region (FIR) boundary.
Figure 1 — Example of UAS geographical zones
Figure 2 — Example of UAS geographical including representation of planned U-space

#### Result 2
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.

#### Result 3
Citation: [reg-2019-947 | ]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)


COMMISSION IMPLEMENTING REGULATION (EU) 2019/947 of 24 May 2019 on the rules and procedures for the operation of unmanned aircraft systems

#### Result 4
Citation: [easa-amc-gm | GM1 Articsle 2(28), (29), (30), (31), (32) and (33) Definitions]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 Articsle 2(28), (29), (30), (31), (32) and (33) Definitions (part 1/2)
DEFINITIONS OF ‘FLIGHT GEOGRAPHY’, ‘FLIGHT GEOGRAPHY AREA’, ‘CONTINGENCY VOLUME’, ‘CONTINGENCY AREA’, ‘OPERATIONAL VOLUME’ AND ‘GROUND RISK BUFFER’
The ‘flight geography’ is the spatially and temporally defined volume of airspace in which the UAS operator plans to conduct the operation under normal procedures; the projection of such volume on the surface of the Earth constitutes the ‘flight geography area’. Additionally, the UA positioning errors must be accounted for in the definition of this area.
To cope with abnormal situations (e.g. navigation errors, UA drifting due to wind/gusts, etc.), the UAS operator should define the ‘contingency volume’ as an airspace volume where contingency procedures are applied in order to bring the UA back to a normal situation within the ‘flight geography’ (for example, if the UA exits the boundaries of the flight geography, the remote pilot should take actions to pilot the UAS back into the flight geography. If the contingency situation persists, the remote pilot should activate the FTS (if available) before the UAS exits the contingency volume). The projection of the contingency volume on the surface of the Earth is the ‘contingency area’.
The ‘operational volume’ includes the ‘flight geography’ and the ‘contingency volume’. To define the operational volume, the UAS operator should consider the position-keeping capabilities of the UAS in a 4D space (latitude, longitude, height, and time).

#### Result 5
Citation: [reg-2019-945 | ]
Document: Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)


COMMMISSION DELEGATED REGULATION (EU) 2019/945 of 12 March 2019 on unmanned aircraft systems and on third-country operators of unmanned aircraft systems

</details>

---

## q28 (unanswerable)

**Question:** What extra Spanish national rules or fees does AESA apply to drone pilots?

**Reference:** Not covered; national rules are not in the corpus. Ask AESA.

**Agent answer:**

The corpus does not cover this. The provided rules cover EU-wide regulations (Regulations (EU) 2019/947 and 2019/945 and EASA AMC/GM), but national administrative fees and specific national operational rules enacted by individual Member States (such as Spain's AESA) are not included in the corpus. You would need to check directly with the Spanish national aviation authority (Agencia Estatal de Seguridad Aérea, AESA).

**Guardrail:** none

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-947 | ]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)


COMMISSION IMPLEMENTING REGULATION (EU) 2019/947 of 24 May 2019 on the rules and procedures for the operation of unmanned aircraft systems

#### Result 2
Citation: [reg-2019-947 | Article 18 - Tasks of the competent authority]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 18 - Tasks of the competent authority (part 1/2)
The competent authority shall be responsible for:
(a) enforcing this Regulation;
(b) issuing, suspending or revoking certificates of UAS operators and licenses of remote pilots operating within the ‘certified’ category of UAS operations;
(c) issuing remote pilots with a proof of completion of an online theoretical knowledge examination according to points UAS.OPEN.020 and UAS.OPEN.040 of the Annex and issuing, amending, suspending, limiting or revoking certificates of competency of remote pilots according to point UAS.OPEN.030 of the Annex;
(d) issuing, amending, suspending, limiting or revoking operational authorisations and LUCs and verifying completeness of declarations, which are required to carry out UAS operations in the ‘specific’ category of UAS operations;
(e) keeping documents, records and reports concerning UAS operational authorisations, declarations, certificates of competency of the remote pilots and LUCs;
(f) making available in a common unique digital format information on UAS geographical zones identified by the Member States and established within the national airspace of its State;
(g) issuing a confirmation of receipt and completeness in accordance with Article 12(5)(b) or a confirmation in accordance with paragraph 2 of Article 13;
(h) developing a risk-based oversight system for:
i. UAS operators that have submitted a declaration or hold an operational authorisation or an LUC;
ii. model clubs and associations that hold an authorisation referred to in Article 16;

#### Result 3
Citation: [reg-2019-947 | Article 16 - UAS operations in the framework of model aircraft clubs and associations]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 16 - UAS operations in the framework of model aircraft clubs and associations
1. Upon request by a model aircraft club or association, the competent authority may issue an authorisation for UAS operations in the framework of model aircraft clubs and associations.
2. The authorisation referred to in paragraph 1 shall be issued in accordance with any of the following:
(a) relevant national rules;
(b) established procedures, organisational structure and management system of the model aircraft club or association, ensuring that:
i. remote pilots operating in the framework of model aircraft clubs or associations are informed of the conditions and limitations defined in the authorisation issued by the competent authority;
ii. remote pilots operating in the framework of model aircraft clubs or associations are assisted in achieving the minimum competency required to operate the UAS safely and in accordance with the conditions and limitations defined in the authorisation;
iii. the model aircraft club or association takes appropriate action when informed that a remote pilot operating in the framework of model aircraft clubs or associations does not comply with the conditions and limitations defined in the authorisation, and, if necessary, inform the competent authority;
iv. the model aircraft club or association provides, upon request from the competent authority, documentation required for oversight and monitoring purposes.
3. The authorisation referred to in paragraph 1 shall specify the conditions under which operations in the framework of the model aircraft clubs or associations may be conducted and shall be limited to the territory of the Member State in which it is issued.
4. Member States may enable model aircraft clubs and associations to register their members into the registration systems established in accordance with Article 14 on their behalf. If this is not the case, the members of model aircraft clubs and associations shall register themselves in accordance with Article 14.

#### Result 4
Citation: [reg-2019-947 | UAS.SPEC.060 Responsibilities of the remote pilot]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.SPEC.060 Responsibilities of the remote pilot
(1) The remote pilot shall:
(a) not perform duties under the influence of psychoactive substances or alcohol or when it is unfit to perform its tasks due to injury, fatigue, medication, sickness or other causes;
(b) have the appropriate remote pilot competency as defined in the operational authorisation, in the standard scenario defined in Appendix 1 or as defined by the LUC and carry a proof of competency while operating the UAS.
(c) be familiar with manufacturer’s instructions provided by the manufacturer of the UAS.
(2) Before starting an UAS operation, the remote pilot shall comply with all of the following:
(a) obtain updated information relevant to the intended operation about any geographical zones defined in accordance with Article 15;
(b) ensure that the operating environment is compatible with the authorised or declared limitations and conditions;
(c) ensure that the UAS is in a safe condition to complete the intended flight safely, and if applicable, check if the direct remote identification is active and up-to-date;
(d) ensure that the information about the operation has been made available to the relevant air traffic service (ATS) unit, other airspace users and relevant stakeholders, as required by the operational authorisation or by the conditions published by the Member State for the geographical zone of operation in accordance with Article 15.
(3) During the flight, the remote pilot shall:
(a) comply with the authorised or declared limitations and conditions;
(b) avoid any risk of collision with any manned aircraft and discontinue a flight when continuing it may pose a risk to other aircraft, people, animals, environment or property;
(c) comply with the operational limitations in geographical zones defined in accordance with Article 15;
(d) comply with the operator’s procedures;
(e) not fly close to or inside areas where an emergency response effort is ongoing unless they have permission to do so from the responsible emergency response services.

#### Result 5
Citation: [reg-2019-947 | Article 7 - Rules and procedures for the operation of UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 7 - Rules and procedures for the operation of UAS
1. UAS operations in the ‘open’ category shall comply with the operational limitations set out in Part A of the Annex.
2. UAS operations in the ‘specific’ category shall comply with the operational limitations set out in the operational authorisation as referred to in Article 12 or the authorisation as referred to in Article 16, or in a standard scenario defined in Appendix 1 to the Annex as declared by the UAS operator.
This paragraph shall not apply where the UAS operator holds an LUC with appropriate privileges.
UAS operations in the ‘specific’ category shall be subject to the applicable operational requirements laid down in Commission Implementing Regulation (EU) No 923/2012.
2a. The operator of a UAS that meets the conditions specified in point 1(d) of Article 40 of Delegated Regulation (EU) 2019/945 shall obtain the following certificates:
(i) a certificate of airworthiness or a restricted certificate of airworthiness issued in accordance with Subpart H of Annex I (Part 21) to Commission Regulation (EU) No 748/2012;
(ii) a noise certificate issued in accordance with Subpart I of Annex I (Part 21) to Commission Regulation (EU) No 748/2012 when the UA is subject to the environmental protection requirements laid down in point 21.B.85 of Regulation (EU) No 748/2012.
3. UAS operations in the ‘certified’ category shall be subject to the applicable operational requirements laid down in Implementing Regulation (EU) No 923/2012 and Commission Regulations (EU) No 965/2012 and (EU) No 1332/2011.

</details>

---

## q29 (unanswerable)

**Question:** What iGRC and SAIL do I get for flying a 3 m drone over an area with 5,000 people per square kilometre?

**Reference:** Not covered; the SORA method and its scores are excluded from the corpus. Ask AESA or consult the SORA.

**Agent answer:**

The corpus does not contain the specific tables or values required to determine the iGRC (Intrinsic Ground Risk Class) or the final SAIL (Specific Assurance and Integrity Level) for your operation.

The SORA (Specific Operations Risk Assessment) process, which determines these values, is referenced in the EASA Acceptable Means of Compliance (AMC) as the method for applying for an operational authorisation in the 'specific' category [easa-amc-gm | AMC1 UAS.SPEC.030(2) Application for an operational authorisation — EASA Form 208]. However, the provided documents contain the *templates* for the application (EASA Form 208) and the authorisation (EASA Form 209), which list the categories of population density (e.g., "up to 5 000 people/km²") [easa-amc-gm | AMC1 UAS.SPEC.030(2) Application for an operational authorisation — EASA Form 208], but they do not provide the underlying SORA tables that map these densities and drone characteristics to a specific iGRC or SAIL value.

To determine these values, you must consult the full SORA methodology (often found in the Annex to AMC1 Article 11 of Regulation (EU) 2019/947, which is not fully detailed in the provided search results). You should contact your national aviation authority for guidance on performing a SORA for your specific operation.

**Check local zones before flying.** In UAS geographical zones, Member States may "prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]. Information on these zones "is made publicly available in a common unique digital format" [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]; check it for the place where you plan to fly.

**Guardrail:** national-zones note added (Article 15)

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | AMC1 UAS.SPEC.040(1) Operational authorisation — EASA Form 209]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.SPEC.040(1) Operational authorisation — EASA Form 209 (part 1/10)
OPERATIONAL AUTHORISATION TEMPLATE
The competent authority should produce the operational authorisation according to the following form:
Operational authorisation for the ‘specific’ category
1. Authority that issues the authorisation
1.1 Issuing authority
1.2 Point of contact Office Telephone Email
2. UAS operator data
2.1 UAS operator registration number
2.2 UAS operator name
2.3 Point of contact Name Telephone Email
3. Authorised operation
3.1 Authorised location(s) including the lower and upper limits of the operational volume | Generic, lower limit __m (__ ft), upper limit __m (__ ft) Precise, specify coordinates _______________________, lower limit __m (__ ft), upper limit __m (__ ft)
3.2 Risk assessment reference and revision | SORA edition date ___ PDRA # __-__ edition date ___ other _________
3.3 Level of assurance and integrity | SAIL I SAIL II SAIL III SAIL IV SAIL V SAIL VI Other____________
3.4 Type of operation | VLOS BVLOS
3.5 Transport of dangerous goods | Yes No
3.6 Dropping material | Yes No
3.7 Ground risk characterisation | 3.7.1 Operational area (maximum population density) | controlled ground area people/km2 sparsely populated area up to 5 up to 50 up to 500 populated area up to 5 000 up to 50 000 more than 50 000 assemblies of people no limit
3.7.2 Adjacent ground area (average population density) | people/km2 sparsely populated area up to 50 up to 500 populated area up to 5 000 up to 50 000 assemblies of people no limit

#### Result 2
Citation: [reg-2019-947 | ]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)


COMMISSION IMPLEMENTING REGULATION (EU) 2019/947 of 24 May 2019 on the rules and procedures for the operation of unmanned aircraft systems

#### Result 3
Citation: [easa-amc-gm | AMC1 UAS.SPEC.040(1) Operational authorisation — EASA Form 209]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.SPEC.040(1) Operational authorisation — EASA Form 209 (part 2/10)
3.7.3 Adjacent ground area (outdoor assemblies of people allowed within 1 km of the operational volume) | up to 40 000 people up to 400 000 people more than 400 000 people
3.8 Ground risk mitigations | 3.8.1 M1(A) — Sheltering | No Low Medium
3.8.2 M1(B) — Operational restrictions | No Medium High
3.8.3 M1(C) — Ground observation | No Low
3.8.4 M2 — Mitigation to reduce effect of ground impact | No Medium High
3.9 Final ground risk class (GRC)
3.10 Residual air risk level in the operational volume | ARC-a ARC-b ARC-c ARC-d
3.11 Air risk mitigations | 3.11.1 Strategic mitigations | No Yes If yes, please describe _________________
3.11.2 Tactical mitigation methods
3.12 Achieved level of containment | Low Medium High Tethered
3.13 What is the minimum RP:UA ratio allowed between the remote pilot (RP) and the UA that may be operated simultaneously? | RP:UA ___:____
3.14 Remote pilot competency
3.15 Competency of staff, other than the remote pilot, essential for the safety of the operation
3.16 Type of events to be reported to the competent authority (in addition to those required by Regulation (EU) No 376/2014)
3.17 Insurance | No Yes
3.18 Compliance matrix file reference
3.19 Remarks / additional limitations
4. Data of authorised UAS
4.1 Design organisation name (optional) | 4.2 Model name (optional)
4.3 Type of UAS | Fixed-wing Rotorcraft-helicopter Rotorcraft-gyroplane VTOL-capable UA (including multirotors Lighter than air / other | 4.4 Maximum UA characteristic dimensions | _____ m

#### Result 4
Citation: [easa-amc-gm | AMC1 UAS.SPEC.030(2) Application for an operational authorisation — EASA Form 208]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.SPEC.030(2) Application for an operational authorisation — EASA Form 208 (part 5/12)
an up-to-date list of maintenance staff employed to carry out maintenance activities; the insurance coverage, if applicable, will be in place at the expected date of start of the UAS operation
Section 4 – Specific operations risk assessment (SORA)
Step #1 — Documentation of the proposed operation
Step #1.1 Description of proposed locations | If location-specific: Give reference to the file: ___________________________________ If location-independent: (generic authorisation) Give reference to the file as example of a location: ___________________________________
Step #1.2 Short description of the proposed operation
Step #1.3 Dimensions of the operational volume and the adjacent volume (Rounded up to first decimal place) | Maximum height of the flight geography Maximum height of the contingency volume Width of the contingency volume Width of the ground risk buffer Width of the adjacent volume | HFGmax HCVmax SCVmax SGRBmax SAV | ________ m ________ m ________ m ________ m ________ m
Step #2 — UAS intrinsic ground risk class (iGRC)
Step #2.1 Type of operational areas or maximum population density on the ground (including flight geography, contingency volume and ground risk buffer) | controlled ground area people/km2 sparsely populated area up to 5 up to 50 up to 500 populated area up to 5 000 up to 50 000 more than 50 000 assemblies of people no limit
Step #2.2 Specify the intrinsic ground risk class (iGRC)
Step #2.3 Remarks/Reasoning for Step #2 (optional)
Step #3 — Final ground risk class (GRC) determination (optional)

#### Result 5
Citation: [easa-amc-gm | AMC1 UAS.OPEN.040(1) Operations in subcategory A3]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.OPEN.040(1) Operations in subcategory A3
AREAS WHERE UAS OPERATIONS IN A3 MAY BE CONDUCTED
(a) If an uninvolved person enters the range of the UAS operation, the remote pilot should, where necessary, adjust the operation to ensure the safety of the uninvolved person and discontinue the operation if the safety of the UAS operation is not ensured.
(b) A minimum horizontal distance from the person that is passing the area could be estimated as follows:
(1) no less than 30 m;
(2) no less than the height (‘1:1 rule’, i.e. if the UA is flying at a height of 30 m, the distance of the UA from the uninvolved person should be at least 30 m), and
(3) no less than the distance that the UA would cover in 2 seconds at the maximum speed (this assumes a reaction time of 2 seconds).
This minimum horizontal distance is intended to protect people on the ground, but can be extended to property and animals.
#### Result 1
Citation: [easa-amc-gm | AMC1 UAS.SPEC.030(2) Application for an operational authorisation — EASA Form 208]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.SPEC.030(2) Application for an operational authorisation — EASA Form 208 (part 11/12)
3.15 Multiple options are possible. Direct remote ID developed according to EN 4709-002.
In order to compile Section 4, please refer to AMC1 Article 11 (SORA).
Section 4
Step #1.1:
The identification of the location(s) should contain the full operational volume and ground risk buffer (the red line in Figure 1; refer to Annex A to AMC1 Article 11 for guidance and examples on the calculation of the operational volume and ground risk buffer). Depending on the initial ground and air risk classification determined using the SORA process and on the application of mitigations, the location(s) may be ‘generic’ or ‘precise’ (refer to GM2 UAS.SPEC.030(2)).
Figure 1 — Operational area and ground risk buffer
— Please, refer to GM2 UAS.SPEC.030(2) for guidance on the conditions to apply for ‘generic’ versus ‘precise’ locations.
— If location-specific: please, provide a list with the geo-coordinates for each location including the operational volume (flight geography and contingency volume), the ground risk buffer and the air risk buffer (if available) as a separate file using either ‘.txt’, ‘.kmz’ or ‘.kml’.
— If location-independent: please, provide a reference to the documented process for the determination of volumes and buffers and the assessment of the local conditions and their compliance limitations. An example of a geographical file (e.g. ‘.kmz’ or ‘.kml’) may be provided to show a typical operational volume, ground risk buffer and the air risk buffer (if available).
Step #1.2: Insert, for example, transport, inspection, filming, testing, etc.

#### Result 2
Citation: [easa-amc-gm | AMC1 UAS.SPEC.030(2) Application for an operational authorisation — EASA Form 208]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.SPEC.030(2) Application for an operational authorisation — EASA Form 208 (part 6/12)
Step #3.1 Specify the ground risk mitigations applied and the level of robustness (if applicable) | M1(A) Strategic mitigation — sheltering
☐None | ☐Low | ☐Medium
M1(B) Strategic mitigation — operational restrictions
☐None | ☐Medium | ☐High
M1(C) Tactical mitigation — ground observation
☐None | ☐Low
M2 Effects of UA impact dynamics are reduced
☐None | ☐Medium | ☐High
Step #3.2 Specify the final ground risk class (GRC)
Step #3.2 Remarks/Reasoning for Step #3 (optional)
Step #4 — Initial air risk class (ARC)
Step #4.1 Classification of the airspace where the operation is intended to be conducted (multiple answers possible) | ☐A | ☐B | ☐C | ☐D | ☐E | ☐F | ☐G
☐Restricted area | ☐Danger area
☐TMZ ☐RMZ ☐ATZ ☐CTR ☐CTA ☐FIZ
Step 4.2 Specify the initial air risk class (ARC) of the operational volume | ☐ARC-a ☐ARC-b ☐ARC-c ☐ARC-d
Step #4.3 Remarks/Reasoning for choosing the ARC in Step #4
Step #5 — Strategic air risk mitigations and final air risk class (ARC)
Step #5.1 Specify the strategic mitigations of the air risk class, if applied | ☐No | ☐ VLOS ☐BVLOS with AOs ☐ Operational restrictions ☐ Common rules and structures
Step #5.2 Residual air risk class (after strategic mitigation) | ☐ARC-a ☐ARC-b ☐ARC-c ☐ARC-d
Step #5.3 Remarks/Reasoning for Step #5 (not needed if no mitigation applied)
Step #6 — Tactical mitigation performance requirements (TMPRs) and robustness level

#### Result 3
Citation: [easa-amc-gm | AMC1 UAS.SPEC.030(2) Application for an operational authorisation — EASA Form 208]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.SPEC.030(2) Application for an operational authorisation — EASA Form 208 (part 5/12)
an up-to-date list of maintenance staff employed to carry out maintenance activities; the insurance coverage, if applicable, will be in place at the expected date of start of the UAS operation
Section 4 – Specific operations risk assessment (SORA)
Step #1 — Documentation of the proposed operation
Step #1.1 Description of proposed locations | If location-specific: Give reference to the file: ___________________________________ If location-independent: (generic authorisation) Give reference to the file as example of a location: ___________________________________
Step #1.2 Short description of the proposed operation
Step #1.3 Dimensions of the operational volume and the adjacent volume (Rounded up to first decimal place) | Maximum height of the flight geography Maximum height of the contingency volume Width of the contingency volume Width of the ground risk buffer Width of the adjacent volume | HFGmax HCVmax SCVmax SGRBmax SAV | ________ m ________ m ________ m ________ m ________ m
Step #2 — UAS intrinsic ground risk class (iGRC)
Step #2.1 Type of operational areas or maximum population density on the ground (including flight geography, contingency volume and ground risk buffer) | controlled ground area people/km2 sparsely populated area up to 5 up to 50 up to 500 populated area up to 5 000 up to 50 000 more than 50 000 assemblies of people no limit
Step #2.2 Specify the intrinsic ground risk class (iGRC)
Step #2.3 Remarks/Reasoning for Step #2 (optional)
Step #3 — Final ground risk class (GRC) determination (optional)

#### Result 4
Citation: [easa-amc-gm | AMC2 UAS.OPEN.030(2)(b) UAS operations in subcategory A2]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC2 UAS.OPEN.030(2)(b) UAS operations in subcategory A2 (part 4/4)
(iv) identify situations where an occurrence report is necessary, and complete the occurrence report.

#### Result 5
Citation: [easa-amc-gm | AMC1 UAS.SPEC.040(1) Operational authorisation — EASA Form 209]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 UAS.SPEC.040(1) Operational authorisation — EASA Form 209 (part 2/10)
3.7.3 Adjacent ground area (outdoor assemblies of people allowed within 1 km of the operational volume) | up to 40 000 people up to 400 000 people more than 400 000 people
3.8 Ground risk mitigations | 3.8.1 M1(A) — Sheltering | No Low Medium
3.8.2 M1(B) — Operational restrictions | No Medium High
3.8.3 M1(C) — Ground observation | No Low
3.8.4 M2 — Mitigation to reduce effect of ground impact | No Medium High
3.9 Final ground risk class (GRC)
3.10 Residual air risk level in the operational volume | ARC-a ARC-b ARC-c ARC-d
3.11 Air risk mitigations | 3.11.1 Strategic mitigations | No Yes If yes, please describe _________________
3.11.2 Tactical mitigation methods
3.12 Achieved level of containment | Low Medium High Tethered
3.13 What is the minimum RP:UA ratio allowed between the remote pilot (RP) and the UA that may be operated simultaneously? | RP:UA ___:____
3.14 Remote pilot competency
3.15 Competency of staff, other than the remote pilot, essential for the safety of the operation
3.16 Type of events to be reported to the competent authority (in addition to those required by Regulation (EU) No 376/2014)
3.17 Insurance | No Yes
3.18 Compliance matrix file reference
3.19 Remarks / additional limitations
4. Data of authorised UAS
4.1 Design organisation name (optional) | 4.2 Model name (optional)
4.3 Type of UAS | Fixed-wing Rotorcraft-helicopter Rotorcraft-gyroplane VTOL-capable UA (including multirotors Lighter than air / other | 4.4 Maximum UA characteristic dimensions | _____ m
#### Result 1
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.



</details>

---

## q30 (unanswerable)

**Question:** Do I need to register my drone with the FAA if I fly in Florida?

**Reference:** Not covered; the corpus only covers EU rules, not US FAA rules. Check with the FAA.

**Agent answer:**

The corpus does not cover this. The rules in this corpus apply to the European Union (Regulation (EU) 2019/947 and Regulation (EU) 2019/945) and do not cover operations or registration requirements in Florida or under the FAA. For questions regarding drone rules in the United States, you should check the Federal Aviation Administration (FAA) regulations or consult the appropriate US aviation authority.

**Guardrail:** none

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 1/3)
1. Member States shall establish and maintain accurate registration systems for UAS whose design is subject to certification and for UAS operators whose operation may present a risk to safety, security, privacy, and protection of personal data or environment.
2. The registration systems for UAS operators shall provide the fields for introducing and exchanging the following information:
(a) the full name and the date of birth for natural persons and the name and their identification number for legal persons;
(b) the address of UAS operators;
(c) their email address and telephone number;
(d) an insurance policy number for UAS if required by Union or national law;
(e) the confirmation by legal persons of the following statement: ‘All personnel directly involved in the operations are competent to perform their tasks, and the UAS will be operated only by remote pilots with the appropriate level of competency’;
(f) operational authorisations and LUCs held and declarations followed by a confirmation in accordance with Article 12(5)(b).
3. The registration systems for unmanned aircraft whose design is subject to certification shall provide the fields for introducing and exchanging the following information:
(a) manufacturer’s name;
(b) manufacturer’s designation of the unmanned aircraft;
(c) unmanned aircraft’s serial number;
(d) full name, address, email address and telephone number of the natural or legal person under whose name the unmanned aircraft is registered.

#### Result 2
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 2/3)
4. Member States shall ensure that registration systems are digital and interoperable and allow for mutual access and exchange of information through the repository referred to in Article 74 of Regulation (EU) 2018/1139.
5. UAS operators shall register themselves:
(a) when operating within the ‘open’ category any of the following unmanned aircraft:
i. with a MTOM of 250 g or more, or, which in the case of an impact can transfer to a human kinetic energy above 80 Joules;
ii. that is equipped with a sensor able to capture personal data, unless it complies with Directive 2009/48/EC.
(b) when operating within the ‘specific’ category an unmanned aircraft of any mass.
6. UAS operators shall register themselves in the Member State where they have their residence for natural persons or where they have their principal place of business for legal persons and ensure that their registration information is accurate. A UAS operator cannot be registered in more than one Member State at a time.
Member States shall issue a unique digital registration number for UAS operators and for the UAS that require registration, allowing their individual identification.
The registration number for UAS operators shall be established on the basis of standards that support the interoperability of the registration systems;
7. The owner of an unmanned aircraft whose design is subject to certification shall register the unmanned aircraft.

#### Result 3
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 3/3)
The nationality and registration mark of an unmanned aircraft shall be established in line with ICAO Annex 7. An unmanned aircraft cannot be registered in more than one State at a time.
8. The UAS operators shall display their registration number on every unmanned aircraft meeting the conditions described in paragraph 5.
9. In addition to the data defined in point (2) Member States may collect additional identity information from the UAS operators.

#### Result 4
Citation: [easa-amc-gm | AMC1 Article 14(8) Registration of UAS operators and ‘certified’ UAS]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 14(8) Registration of UAS operators and ‘certified’ UAS
DISPLAY OF REGISTRATION INFORMATION
(a) If the UAS operator owns the UAS or uses a UAS that is owned by a third party, it should:
(1) register itself;
(2) display on the UA the UAS operator registration number, which is received at the end of the registration process, in a way that the number is readable at least when the UA is on the ground, without using other devices than eyeglasses or corrective lenses; and
(3) upload the full string, which consists of the UAS operator registration number and the three (3) randomly generated alphanumerics, into the electronic identification system, if available.
(b) A QR code (quick response code) may be used.
(c) If the size of the UA does not allow the mark to be displayed in a visible way on the fuselage, or the UA represents a real aircraft where affixing the marking on the UA would spoil the realism of the representation, a marking inside the battery compartment is acceptable if the compartment is accessible.

#### Result 5
Citation: [easa-amc-gm | AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

AMC1 Article 14(6) Registration of UAS operators and ‘certified’ UAS
UAS OPERATOR REGISTRATION NUMBER
(a) The unique UAS operator digital registration number that is issued by the Member States should consist of sixteen (16) alphanumerics in total, arranged as follows:
(1) the first three (3) alphanumerics (upper-case only) corresponding to the ISO 3166 Alpha3 code of the Member State of registration;
(2) followed by twelve (12) randomly generated characters that consist of alphanumerics (lower-case only); and
(3) one (1) character corresponding to the checksum that is generated in line with point (c).
(b) The Member States should randomly generate three (3) additional alphanumerics (lower-case only) called ‘secret digits’.
(c) The Member States should generate a checksum by applying the Luhn-mod-36 algorithm to the fifteen (15) alphanumerics that result from the concatenation, in the following order, of:
(1) the twelve (12) alphanumerics of the UAS operator registration number defined in point (a)(2); and
(2) the three (3) randomly generated ‘secret digits’ that are defined in point (b).
(d) For the Luhn-mod-36 algorithm, the mapping of the alphanumerics to the code-points should start with digits that are followed by lower-case letters, as shown below:
Alphanumeric | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | a | b | c | d | e | f | … | z
Code-point | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | … | 35
(e) At the time of registration, the Member State should provide the UAS operator with the full registration string that consists, in the following order, of:
(1) the UAS operator registration number as defined in point (a); and
(2) the three (3) randomly generated ‘secret digits’, separated by a hyphen ‘-’ (ASCII code [DEC] 45).

</details>

---

## q31 (unanswerable)

**Question:** What is the minimum liability insurance amount for a 2 kg drone in Spain?

**Reference:** Not covered; the corpus only says insurance is needed if required by Union or national law, with no amounts. Ask AESA or an insurer.

**Agent answer:**

The corpus does not cover this. 

Liability insurance requirements (such as minimum coverage amounts) are not specified in EU Regulations (EU) 2019/947 or (EU) 2019/945. Under EU rules, insurance is only mentioned as a field for operator registration if required by national law [reg-2019-947 | Article 14]. Specific liability insurance minimums for operating a 2 kg drone depend on national laws and aviation authorities (in Spain, the *Agencia Estatal de Seguridad Aérea* - AESA) rather than EU-wide drone regulations.

**Guardrail:** none

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [reg-2019-947 | Article 14 - Registration of UAS operators and certified UAS]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 14 - Registration of UAS operators and certified UAS (part 1/3)
1. Member States shall establish and maintain accurate registration systems for UAS whose design is subject to certification and for UAS operators whose operation may present a risk to safety, security, privacy, and protection of personal data or environment.
2. The registration systems for UAS operators shall provide the fields for introducing and exchanging the following information:
(a) the full name and the date of birth for natural persons and the name and their identification number for legal persons;
(b) the address of UAS operators;
(c) their email address and telephone number;
(d) an insurance policy number for UAS if required by Union or national law;
(e) the confirmation by legal persons of the following statement: ‘All personnel directly involved in the operations are competent to perform their tasks, and the UAS will be operated only by remote pilots with the appropriate level of competency’;
(f) operational authorisations and LUCs held and declarations followed by a confirmation in accordance with Article 12(5)(b).
3. The registration systems for unmanned aircraft whose design is subject to certification shall provide the fields for introducing and exchanging the following information:
(a) manufacturer’s name;
(b) manufacturer’s designation of the unmanned aircraft;
(c) unmanned aircraft’s serial number;
(d) full name, address, email address and telephone number of the natural or legal person under whose name the unmanned aircraft is registered.

#### Result 2
Citation: [reg-2019-947 | ]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)


COMMISSION IMPLEMENTING REGULATION (EU) 2019/947 of 24 May 2019 on the rules and procedures for the operation of unmanned aircraft systems

#### Result 3
Citation: [reg-2019-947 | UAS.SPEC.060 Responsibilities of the remote pilot]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.SPEC.060 Responsibilities of the remote pilot
(1) The remote pilot shall:
(a) not perform duties under the influence of psychoactive substances or alcohol or when it is unfit to perform its tasks due to injury, fatigue, medication, sickness or other causes;
(b) have the appropriate remote pilot competency as defined in the operational authorisation, in the standard scenario defined in Appendix 1 or as defined by the LUC and carry a proof of competency while operating the UAS.
(c) be familiar with manufacturer’s instructions provided by the manufacturer of the UAS.
(2) Before starting an UAS operation, the remote pilot shall comply with all of the following:
(a) obtain updated information relevant to the intended operation about any geographical zones defined in accordance with Article 15;
(b) ensure that the operating environment is compatible with the authorised or declared limitations and conditions;
(c) ensure that the UAS is in a safe condition to complete the intended flight safely, and if applicable, check if the direct remote identification is active and up-to-date;
(d) ensure that the information about the operation has been made available to the relevant air traffic service (ATS) unit, other airspace users and relevant stakeholders, as required by the operational authorisation or by the conditions published by the Member State for the geographical zone of operation in accordance with Article 15.
(3) During the flight, the remote pilot shall:
(a) comply with the authorised or declared limitations and conditions;
(b) avoid any risk of collision with any manned aircraft and discontinue a flight when continuing it may pose a risk to other aircraft, people, animals, environment or property;
(c) comply with the operational limitations in geographical zones defined in accordance with Article 15;
(d) comply with the operator’s procedures;
(e) not fly close to or inside areas where an emergency response effort is ongoing unless they have permission to do so from the responsible emergency response services.

#### Result 4
Citation: [reg-2019-947 | UAS.SPEC.050 Responsibilities of the UAS operator]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.SPEC.050 Responsibilities of the UAS operator (part 1/4)
(1) The UAS operator shall comply with all of the following:
(a) establish procedures and limitations adapted to the type of the intended operation and the risk involved, including:
(i) operational procedures to ensure the safety of the operations;
(ii) procedures to ensure that security requirements applicable to the area of operations are complied with in the intended operation;
(iii) measures to protect against unlawful interference and unauthorised access;
(iv) procedures to ensure that all operations are in respect of Regulation (EU) 2016/679 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data. In particular it shall carry out a data protection impact assessment, when required by the National Authority for data protection in application of Article 35 of Regulation (EU) 2016/679;
(v) guidelines for its remote pilots to plan UAS operations in a manner that minimises nuisances, including noise and other emissions-related nuisances, to people and animals.
(b) designate a remote pilot for each flight or, in the case of autonomous operations, ensure that during all phases of the flight, responsibilities and tasks especially those defined in points (2) and (3) of point UAS.SPEC.060 are properly allocated in accordance with the procedures established pursuant to point (a);
(c) ensure that all operations effectively use and support the efficient use of radio spectrum in order to avoid harmful interference;
(d) ensure that before conducting operations, remote pilots comply with all of the following conditions:

#### Result 5
Citation: [reg-2019-947 | UAS.OPEN.060 Responsibilities of the remote pilot]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

UAS.OPEN.060 Responsibilities of the remote pilot (part 1/2)
(1) Before starting an UAS operation, the remote pilot shall:
(a) have the appropriate competency in the subcategory of the intended UAS operations in accordance with points UAS.OPEN.020, UAS.OPEN.030 or UAS.OPEN.040 to perform its task and carry a proof of competency while operating the UAS, except when operating an unmanned aircraft referred to in points (5)(a), (5)(b) or (5)(c) of point UAS.OPEN.020;
(b) obtain updated information relevant to the intended UAS operation about any geographical zone published by the Member State of operation in accordance with Article 15;
(c) observe the operating environment, check the presence of obstacles and, unless operating in subcategory A1 with an unmanned aircraft referred to in points (5)(a), (5)(b) or (5)(c) of point UAS.OPEN.020, check the presence of any uninvolved person;
(d) ensure that the UAS is in a condition to safely complete the intended flight, and if applicable, check if the direct remote identification is active and up-to-date;
(e) if the UAS is fitted with an additional payload, verify that its mass does not exceed neither the MTOM defined by the manufacturer or the MTOM limit of its class.
(2) During the flight, the remote pilot shall:
(a) not perform duties under the influence of psychoactive substances or alcohol or when it is unfit to perform its tasks due to injury, fatigue, medication, sickness or other causes;

</details>

---

## q32 (unanswerable)

**Question:** What fine will I get in Spain if I fly in a no-fly zone?

**Reference:** Not covered; penalties are national and not in the corpus. Ask AESA.

**Agent answer:**

The corpus does not cover this. 

EU Regulations (EU) 2019/947 and (EU) 2019/945 and EASA's AMC and Guidance Material govern operational rules, drone classes, and the establishment of geographical zones by Member States [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones], but they do not define national penalties, fines, or enforcement measures for violating no-fly zones. 

To find out the specific fines applicable in Spain, you would need to consult Spanish national aviation law or contact Spain's national aviation authority (AESA — *Agencia Estatal de Seguridad Aérea*).

**Guardrail:** none

<details><summary>Retrieved passages</summary>

#### Result 1
Citation: [easa-amc-gm | GM1 Article 15(3) Operational conditions for UAS geographical zones]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 Article 15(3) Operational conditions for UAS geographical zones (part 2/2)
UAS geographical zones where UAS operations are limited and subject to the fulfilment of a set of conditions that are imposed for such zones. Such limitations and conditions may concern administrative procedures, operational limitations, or technical requirements for the UAS or mandatory functions. For example, UAS operations are permitted in such UAS geographical zones if the UAS MTOM does not exceed 1.5 kg and the flight altitude is below 50 m above the ground.
UAS geographical zones that facilitate UAS operations in the ‘open’ category (UAS operations are exempt from one or more of the ‘open’ category requirements).
U-space airspace where UAS operations are supported by a set of Uspace services. UAS operations are compliant with the capability and performance requirements that are determined for the particular U-space airspace. The Member States should list the U-space service provider(s) (USSP(s)) that is (are) identified for that geographical zone.
Riga flight information region (FIR) boundary.
Figure 1 — Example of UAS geographical zones
Figure 2 — Example of UAS geographical including representation of planned U-space

#### Result 2
Citation: [reg-2019-947 | Article 15 - Operational conditions for UAS geographical zones]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)

Article 15 - Operational conditions for UAS geographical zones
1. When defining UAS geographical zones for safety, security, privacy or environmental reasons, Member States may:
(a) prohibit certain or all UAS operations, request particular conditions for certain or all UAS operations or require a prior flight authorisation for certain or all UAS operations;
(b) subject UAS operations to specified environmental standards;
(c) allow access to certain UAS classes only;
(d) allow access only to UAS equipped with certain technical features, in particular remote identification systems or geo awareness systems.
2. On the basis of a risk assessment carried out by the competent authority, Member States may designate certain geographical zones in which UAS operations are exempt from one or more of the ‘open’ category requirements.
3. When pursuant to paragraphs 1 or 2 Member States define UAS geographical zones, for geo awareness purposes they shall ensure that the information on the UAS geographical zones, including their period of validity, is made publicly available in a common unique digital format.

#### Result 3
Citation: [easa-amc-gm | GM1 Article 15(3) Operational conditions for UAS geographical zones]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM1 Article 15(3) Operational conditions for UAS geographical zones (part 1/2)
EXAMPLES OF MAPS OF UAS GEOGRAPHICAL ZONES WITH COLOUR-CODE INDEX
Note: The following examples, including colour codes and explanations, are courtesy of the ‘Latvijas gaisa satiksme’, the Latvian ANSP, for the purpose of illustration only and should not be used for UAS operations.
The examples represent a possible approach of a Member State to present UAS geographical zones in a way which is proven to be compliant with the ED-269 standard. A maximum level of standardisation/harmonisation would be beneficial for the EU-wide implementation of Article 15 of the UAS Regulation.
This example provides a simplified and clearly understandable way to visualise UAS geographical zones to non-ATM professionals. The set of colours is limited to the three colours of the traffic light scheme illustrating the purpose of a UAS geographical zone.
Detailed information related to a respective UAS geographical zone, such as details of restrictions, maximum height, maximum noise level, application procedure for flight authorisation, etc., may be provided when the UAS operator selects the respective zone on the website or on the smartphone application.
COLOUR CODE | MEANING
UAS geographical zones where UAS operations are prohibited. However, restrictions may be waived for particular users. UAS operations in some UAS geographical zones may be subject to the fulfilment of special requirements, e.g. compliance with published procedures, request for flight authorisation, etc. The competent authority should publish the conditions for obtaining the waiver and the point of contact of the entity from which the flight authorisation needs to be requested.

#### Result 4
Citation: [reg-2019-947 | ]
Document: Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)


COMMISSION IMPLEMENTING REGULATION (EU) 2019/947 of 24 May 2019 on the rules and procedures for the operation of unmanned aircraft systems

#### Result 5
Citation: [easa-amc-gm | GM2 Article 15(1) Operational conditions for UAS geographical zones]
Document: EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)

GM2 Article 15(1) Operational conditions for UAS geographical zones
GENERAL ASPECTS
In line with the Chicago Convention, UAS geographical zones with restrictions and prohibitions should not be designated over the high seas / international airspace.
UAS geographical zones are defined in accordance with policies and procedures established by the Member States. Various entities (e.g. public institutions, law enforcement authorities, ANSPs, local authorities, nature park authorities, the military, etc.) may initiate the identification of UAS geographical zones. The initiating entity may provide the approving entity with the data on the UAS geographical zone(s) together with supporting material in accordance with the Member States’ arrangements for validation and confirmation or approval, as necessary.
Formal arrangements between the initiating entity and the entity that processes the data for the identification of the UAS geographical zone(s) may be considered. Such formal arrangements may include specific requirements on data quality.
If a flight authorisation is required to enter a UAS geographical zone, the Member States should also establish the related procedure and designate the entity responsible for providing such authorisation.

</details>
