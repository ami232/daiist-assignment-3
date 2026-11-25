# Hoja de calificación (tu parte)

Para cada respuesta pon dos notas **sin mirar al juez**:

- **correct** = 1 si da los mismos datos esenciales que la referencia (o se niega correctamente en las `unanswerable`), 0 si falta el dato clave o hay un error.
- **supported** = 1 si TODO lo que afirma aparece en los pasajes citados, 0 si añade algo que no está en el corpus.
- Si pones algún 0, escribe brevemente por qué.

Puedes abrir los pasajes citados en `index/chunks_structure.jsonl` (busca el id entre corchetes).

Respóndeme en el chat con una línea por pregunta, así:  `q01 1 1` o `m06 0 1 falta la condición de 150 m`.


---

## q01 (single)

**Pregunta:** What is the maximum take-off mass a drone can have to be flown in the 'open' category?

**Referencia:** Less than 25 kg (Article 4(1)(b)).

**Respuesta del agente:**

> Yes, the maximum take-off mass for a drone to be flown in the 'open' category must be **less than 25 kg** [32019R0947-s0016]. 
> 
> Conditions:
> * The unmanned aircraft must belong to one of the classes set out in Delegated Regulation (EU) 2019/945, be privately built, or meet the transitional conditions defined in Article 20 [32019R0947-s0016, 32019R0947-s0042].
> * Specific sub-categories (A1, A2, A3) have much lower mass thresholds (e.g., less than 250 g or less than 900 g) governing where and how they may be operated [32019R0947-s0046, 32019R0947-s0042, 32019R0945-s0084].

**Pasajes recuperados:** 32019R0947-s0016 (Regulation (EU) 2019/947, Article 4), 32019R0947-s0046 (Regulation (EU) 2019/947, Annex, UAS.OPEN.010 General provisions), 32019R0947-s0042 (Regulation (EU) 2019/947, Article 20), 32019R0947-s0003 (Regulation (EU) 2019/947, Recitals (part 3/8)), 32019R0945-s0084 (Regulation (EU) 2019/945, Annex, Requirements for a class C1 Unmanned aircraft system (part 1/6))

correct: ___   supported: ___   notas: ______


---

## q02 (single)

**Pregunta:** How high can we fly in the 'open' category?

**Referencia:** Within 120 m from the closest point of the surface of the earth, except when overflying an obstacle as specified in Part A of the Annex.

**Respuesta del agente:**

> In the 'open' category, the maximum flight height is **120 metres** from the closest point of the surface of the earth [32019R0947-s0016, 32019R0947-s0046]. 
> 
> Exceptions and conditions:
> * **Artificial obstacles:** When flying within a horizontal distance of 50 metres from an artificial obstacle taller than 105 metres, the maximum height may be increased up to 15 metres above the obstacle's height, upon request from the entity responsible for the obstacle [32019R0947-s0046].
> * **Unmanned sailplanes:** Sailplanes with an MTOM (including payload) of less than 10 kg may exceed 120 metres from the earth's surface, provided they are not flown higher than 120 metres above the remote pilot at any time [32019R0947-s0046].

**Pasajes recuperados:** 32019R0947-s0046 (Regulation (EU) 2019/947, Annex, UAS.OPEN.010 General provisions), 32019R0947-s0016 (Regulation (EU) 2019/947, Article 4), 32019R0945-s0084 (Regulation (EU) 2019/945, Annex, Requirements for a class C1 Unmanned aircraft system (part 1/6)), 32020R1058-s0029 (Regulation (EU) 2020/1058, Annex, Requirements for a class C2 Unmanned aircraft system (part 1/8)), 32020R1058-s0021 (Regulation (EU) 2020/1058, Annex, Requirements for a class C1 Unmanned aircraft system (part 1/8))

correct: ___   supported: ___   notas: ______


---

## q05 (single)

**Pregunta:** Our camera drone weighs 249 g and is not a toy. Do we have to register as a UAS operator to fly it in the open category?

**Referencia:** Yes. Operators must register for open-category drones of 250 g or more or above 80 J, or equipped with a sensor able to capture personal data unless the drone complies with the Toy Directive 2009/48/EC.

**Respuesta del agente:**

> **Yes**, you must register as a UAS operator. 
> 
> Even though your drone weighs less than 250 g, Article 14(5)(a)ii of Regulation (EU) 2019/947 requires UAS operators in the open category to register if they operate an unmanned aircraft that is **equipped with a sensor able to capture personal data**, unless it complies with Directive 2009/48/EC (toy safety) [32019R0947-s0034]. Since you stated the drone is not a toy, this exemption does not apply to a camera drone.

**Pasajes recuperados:** 32019R0947-s0033 (Regulation (EU) 2019/947, Article 14 (part 1/3)), 32019R0947-s0034 (Regulation (EU) 2019/947, Article 14 (part 2/3)), 32019R0947-s0035 (Regulation (EU) 2019/947, Article 14 (part 3/3)), 32019R0947-s0052 (Regulation (EU) 2019/947, Annex, UAS.OPEN.050 Responsibilities of the UAS operator), 32019R0947-s0030 (Regulation (EU) 2019/947, Article 12 (part 3/3))

correct: ___   supported: ___   notas: ______


---

## q07 (single)

**Pregunta:** In subcategory A2, how far must the drone stay from uninvolved people?

**Referencia:** A safe horizontal distance of at least 30 m, reducible to a minimum of 5 m with an active low-speed mode after assessing weather, drone performance and segregation of the area.

**Respuesta del agente:**

> In subcategory A2, the drone must not overfly uninvolved persons and must maintain a safe horizontal distance of at least 30 metres from them [32019R0947-s0049]. 
> 
> The remote pilot may reduce this horizontal safety distance down to a minimum of 5 metres from uninvolved persons only if:
> - The drone is operated with an active low speed mode function [32019R0947-s0049].
> - The pilot has evaluated the situation regarding weather conditions, the performance of the unmanned aircraft, and the segregation of the overflown area [32019R0947-s0049].

**Pasajes recuperados:** 32019R0947-s0049 (Regulation (EU) 2019/947, Annex, UAS.OPEN.030 UAS operations in subcategory A2 (part 1/2)), 32019R0947-s0051 (Regulation (EU) 2019/947, Annex, UAS.OPEN.040 UAS operations in subcategory A3), 32019R0947-s0047 (Regulation (EU) 2019/947, Annex, UAS.OPEN.020 UAS operations in subcategory A1 (part 1/2)), 32019R0945-s0136 (Regulation (EU) 2019/945, Annex, Test area:), 32019R0947-s0055 (Regulation (EU) 2019/947, Annex, UAS.OPEN.060 Responsibilities of the remote pilot (part 3/3))

correct: ___   supported: ___   notas: ______


---

## q11 (single)

**Pregunta:** How long is a certificate of remote pilot competency for A2 valid?

**Referencia:** Five years (the same applies to the online theoretical competency for A1/A3).

**Respuesta del agente:**

> Yes, the certificate of remote pilot competency is valid for **five years** [32019R0947-s0056]. 
> 
> **Conditions for renewal:**
> The renewal of the certificate requires the demonstration of competencies in accordance with the initial qualification requirements [32019R0947-s0056].

**Pasajes recuperados:** 32019R0947-s0056 (Regulation (EU) 2019/947, Annex, UAS.OPEN.070 Duration and validity of the remote pilot online theoretical competency and certificates of remote pilot competency), 32019R0947-s0049 (Regulation (EU) 2019/947, Annex, UAS.OPEN.030 UAS operations in subcategory A2 (part 1/2)), 32019R0947-s0050 (Regulation (EU) 2019/947, Annex, UAS.OPEN.030 UAS operations in subcategory A2 (part 2/2)), 32019R0947-s0068 (Regulation (EU) 2019/947, Annex, UAS.SPEC.080 Duration and validity of an operational authorisation), 32019R0947-s0043 (Regulation (EU) 2019/947, Article 21)

correct: ___   supported: ___   notas: ______


---

## q13 (single)

**Pregunta:** What are the mass and speed limits for a class C0 drone?

**Referencia:** MTOM of less than 250 g including payload, and a maximum speed in level flight of 19 m/s (height limited to 120 m above the take-off point).

**Respuesta del agente:**

> Yes. A class C0 drone must comply with the following limits:
> 
> * **Mass limit:** Maximum Take-Off Mass (MTOM) of less than 250 g, including payload [32020R1058-s0019].
> * **Speed limit:** Maximum speed in level flight of 19 m/s [32020R1058-s0019].

**Pasajes recuperados:** 32020R1058-s0019 (Regulation (EU) 2020/1058, Annex, Requirements for a class C0 Unmanned aircraft system (part 1/2)), 32019R0945-s0081 (Regulation (EU) 2019/945, Annex, Requirements for a class C0 Unmanned aircraft system (part 1/3)), 32019R0945-s0084 (Regulation (EU) 2019/945, Annex, Requirements for a class C1 Unmanned aircraft system (part 1/6)), 32020R1058-s0021 (Regulation (EU) 2020/1058, Annex, Requirements for a class C1 Unmanned aircraft system (part 1/8)), 32020R1058-s0029 (Regulation (EU) 2020/1058, Annex, Requirements for a class C2 Unmanned aircraft system (part 1/8))

correct: ___   supported: ___   notas: ______


---

## q18 (single)

**Pregunta:** When does the design of a drone have to be certified?

**Referencia:** When it has a characteristic dimension of 3 m or more and is designed to fly over assemblies of people, is designed to transport people, transports dangerous goods needing high robustness, or when a specific-category authorisation concludes the risk cannot be mitigated without certification.

**Respuesta del agente:**

> The design of a drone must be certified if it meets any of the following conditions:
> 
> * It has a characteristic dimension of 3 meters or more and is designed to be operated over assemblies of people [32020R1058-s0015].
> * It is designed for transporting people [32020R1058-s0015].
> * It is designed for transporting dangerous goods and requires a high level of robustness to mitigate third-party accident risks [32020R1058-s0015].
> * It is used in the 'specific' category, and the competent authority's operational authorisation (based on a risk assessment) considers that the risk of the operation cannot be adequately mitigated without UAS certification [32020R1058-s0015].
> 
> *(Note: Regulation (EU) 2020/1058 amends the wording of Article 40(1)(d) from Regulation (EU) 2019/945 to clarify that the intent is tied to operations defined in Article 5 of Implementing Regulation (EU) 2019/947) [32020R1058-s0015, 32019R0945-s0078].*

**Pasajes recuperados:** 32020R1058-s0015 (Regulation (EU) 2020/1058, ‘Article 40 (part 1/3)), 32019R0945-s0078 (Regulation (EU) 2019/945, Article 40), 32019R0947-s0019 (Regulation (EU) 2019/947, Article 6), 32019R0945-s0017 (Regulation (EU) 2019/945, Recitals (part 17/18)), 32019R0947-s0003 (Regulation (EU) 2019/947, Recitals (part 3/8))

correct: ___   supported: ___   notas: ______


---

## q20 (single)

**Pregunta:** Which U-space services are mandatory for all operations in U-space airspace?

**Referencia:** Network identification, geo-awareness, UAS flight authorisation and traffic information services.

**Respuesta del agente:**

> Yes. All UAS operations in U-space airspace are subject to at least the following four mandatory U-space services:
> 
> 1. **Network identification service** [32021R0664-s0012]
> 2. **Geo-awareness service** [32021R0664-s0012]
> 3. **UAS flight authorisation service** [32021R0664-s0012]
> 4. **Traffic information service** [32021R0664-s0012]
> 
> Depending on the airspace risk assessment, Member States may also require additional U-space services for specific U-space airspaces [32021R0664-s0012].

**Pasajes recuperados:** 32021R0664-s0012 (Regulation (EU) 2021/664, Article 3 (part 1/2)), 32021R0664-s0001 (Regulation (EU) 2021/664, Recitals (part 1/9)), 32021R0664-s0005 (Regulation (EU) 2021/664, Recitals (part 5/9)), 32021R0664-s0018 (Regulation (EU) 2021/664, Article 6 (part 1/2)), 32021R0664-s0023 (Regulation (EU) 2021/664, Article 10 (part 1/3))

correct: ___   supported: ___   notas: ______


---

## q22 (single)

**Pregunta:** How does a U-space service provider decide between two flight authorisation requests with the same priority?

**Referencia:** First come, first served (special operations get priority over others).

**Respuesta del agente:**

> When two UAS flight authorisation requests have the same priority, they must be processed on a first-come, first-served basis [32021R0664-s0024].

**Pasajes recuperados:** 32021R0664-s0024 (Regulation (EU) 2021/664, Article 10 (part 2/3)), 32021R0664-s0023 (Regulation (EU) 2021/664, Article 10 (part 1/3)), 32021R0664-s0048 (Regulation (EU) 2021/664, Annex VI, U-SPACE SERVICE PROVISION CONDITIONS AND LIMITATIONS), 32021R0664-s0040 (Regulation (EU) 2021/664, Annex I, 1. Operational conditions), 32021R0664-s0041 (Regulation (EU) 2021/664, Annex I, 2. Airspace constraints)

correct: ___   supported: ___   notas: ______


---

## q24 (single)

**Pregunta:** What must happen when an operation in the specific category is planned in another Member State than the one where the operator is registered?

**Referencia:** The operator must apply to the competent authority of the Member State of intended operation with a copy of its operational authorisation and the locations of the operation, including updated mitigation measures if needed.

**Respuesta del agente:**

> For an operation in the specific category planned in another Member State, the requirements depend on whether the operation is based on an operational authorisation or a standard scenario declaration:
> 
> **1. Operations requiring an operational authorisation:**
> * The UAS operator must provide the competent authority of the Member State of intended operation with an application containing:
>   * A copy of the operational authorisation granted under Article 12 [32019R0947-s0031].
>   * The intended location(s) and any updated mitigation measures needed for local airspace, terrain, population characteristics, and climatic conditions [32019R0947-s0031].
> * The competent authority of the Member State of intended operation assesses the application and provides confirmation that the updated mitigation measures are satisfactory [32019R0947-s0031]. 
> * The operator may start the operation only upon receipt of that confirmation [32019R0947-s0031].
> 
> **2. Operations based on a declaration (standard scenarios):**
> * The UAS operator must provide the competent authority of the Member State of intended operation with a copy of the declaration submitted to the Member State of registration, along with a copy of the confirmation of receipt and completeness [32019R0947-s0032].

**Pasajes recuperados:** 32019R0947-s0031 (Regulation (EU) 2019/947, Article 13 (part 1/2)), 32019R0947-s0032 (Regulation (EU) 2019/947, Article 13 (part 2/2)), 32019R0947-s0017 (Regulation (EU) 2019/947, Article 5 (part 1/2)), 32019R0947-s0018 (Regulation (EU) 2019/947, Article 5 (part 2/2)), 32019R0947-s0058 (Regulation (EU) 2019/947, Annex, UAS.SPEC.020 Operational declaration (part 1/2)), 32019R0947-s0059 (Regulation (EU) 2019/947, Annex, UAS.SPEC.020 Operational declaration (part 2/2)), 32019R0945-s0045 (Regulation (EU) 2019/945, Article 14), 32019R0947-s0030 (Regulation (EU) 2019/947, Article 12 (part 3/3))

correct: ___   supported: ___   notas: ______


---

## m01 (multi)

**Pregunta:** Our drone is class C2. In which open subcategories can we fly it, and how close to uninvolved people can it fly in A2?

**Referencia:** In A2 (with remote ID and geo-awareness active) and in A3. In A2 it must stay at least 30 m horizontally from uninvolved people, or 5 m with low-speed mode active.

**Respuesta del agente:**

> A class C2 drone can be flown in open subcategories **A2** and **A3** [32019R0947-s0050, 32019R0947-s0051].
> 
> In subcategory A2, operations must be conducted so that the unmanned aircraft does not overfly uninvolved persons, maintaining a safe horizontal distance of at least **30 metres** from them [32019R0947-s0049]. 
> 
> The remote pilot may reduce this horizontal safety distance down to a minimum of **5 metres** from uninvolved persons only if:
> * The drone is operated with an active low speed mode function, and
> * The pilot has evaluated the situation regarding weather conditions, aircraft performance, and segregation of the overflown area [32019R0947-s0049].

**Pasajes recuperados:** 32019R0947-s0049 (Regulation (EU) 2019/947, Annex, UAS.OPEN.030 UAS operations in subcategory A2 (part 1/2)), 32019R0947-s0050 (Regulation (EU) 2019/947, Annex, UAS.OPEN.030 UAS operations in subcategory A2 (part 2/2)), 32019R0947-s0051 (Regulation (EU) 2019/947, Annex, UAS.OPEN.040 UAS operations in subcategory A3), 32019R0947-s0048 (Regulation (EU) 2019/947, Annex, UAS.OPEN.020 UAS operations in subcategory A1 (part 2/2)), 32019R0947-s0047 (Regulation (EU) 2019/947, Annex, UAS.OPEN.020 UAS operations in subcategory A1 (part 1/2))

correct: ___   supported: ___   notas: ______


---

## m02 (multi)

**Pregunta:** If our planned flight does not meet the open-category requirements, what do we need and what must we submit with the application?

**Referencia:** An operational authorisation in the specific category from the competent authority of the Member State of registration; the application must include an operational risk assessment per Article 11 with adequate mitigating measures (or a declaration for a standard scenario, or an LUC).

**Respuesta del agente:**

> You must obtain an **operational authorisation** from the competent authority in the Member State where you are registered [32019R0947-s0017]. 
> 
> With your application, you must submit:
> * An **operational risk assessment** performed in accordance with Article 11, including adequate mitigating measures and sufficient information for the authority to assess their adequacy [32019R0947-s0017, 32019R0947-s0060].
> * The **registration number** of the UAS operator [32019R0947-s0060].
> * The name of the accountable manager or the operator (if a natural person) [32019R0947-s0060].
> * An **operations manual**, if required by the risk and complexity of the operation [32019R0947-s0060].
> * A **confirmation that appropriate insurance cover** will be in place at the start of the operations, if required by Union or national law [32019R0947-s0060].

**Pasajes recuperados:** 32019R0947-s0017 (Regulation (EU) 2019/947, Article 5 (part 1/2)), 32019R0947-s0060 (Regulation (EU) 2019/947, Annex, UAS.SPEC.030 Application for an operational authorisation), 32019R0947-s0024 (Regulation (EU) 2019/947, Article 11 (part 1/4)), 32019R0947-s0028 (Regulation (EU) 2019/947, Article 12 (part 1/3)), 32019R0947-s0016 (Regulation (EU) 2019/947, Article 4)

correct: ___   supported: ___   notas: ______


---

## m03 (multi)

**Pregunta:** We want to fly a class C1 drone in A1. What mass or energy limit applies to the drone, and what must the pilot have completed?

**Referencia:** The drone must transmit less than 80 J to a human head on impact or have an MTOM under 900 g; the pilot must have completed an online training course and passed the 40-question online theoretical knowledge examination.

**Respuesta del agente:**

> **Mass or energy limit:**
> A class C1 drone must be made of materials and have performance characteristics ensuring that the energy transmitted to a human head in an impact at terminal velocity is less than 80 J, or alternatively, have a maximum take-off mass (MTOM) of less than 900 g, including payload [32019R0945-s0084, 32020R1058-s0021].
> 
> **Pilot competency requirements:**
> The remote pilot must:
> 1. Be familiarised with the manufacturer's user manual [32019R0947-s0047].
> 2. Have completed an online training course [32019R0947-s0048].
> 3. Have successfully completed an online theoretical knowledge examination (comprising 40 multiple-choice questions across subjects such as air safety, airspace restrictions, aviation regulation, human performance, operational procedures, UAS general knowledge, privacy/data protection, insurance, and security) provided by the competent authority or a recognised entity [32019R0947-s0048].

**Pasajes recuperados:** 32019R0945-s0084 (Regulation (EU) 2019/945, Annex, Requirements for a class C1 Unmanned aircraft system (part 1/6)), 32020R1058-s0021 (Regulation (EU) 2020/1058, Annex, Requirements for a class C1 Unmanned aircraft system (part 1/8)), 32019R0947-s0048 (Regulation (EU) 2019/947, Annex, UAS.OPEN.020 UAS operations in subcategory A1 (part 2/2)), 32020R1058-s0037 (Regulation (EU) 2020/1058, Annex, Requirements for a class C3 Unmanned aircraft system (part 1/7)), 32019R0945-s0097 (Regulation (EU) 2019/945, Annex, Requirements for a class C3 Unmanned aircraft system (part 1/6)), 32019R0947-s0047 (Regulation (EU) 2019/947, Annex, UAS.OPEN.020 UAS operations in subcategory A1 (part 1/2)), 32019R0947-s0021 (Regulation (EU) 2019/947, Article 8), 32019R0947-s0049 (Regulation (EU) 2019/947, Annex, UAS.OPEN.030 UAS operations in subcategory A2 (part 1/2)), 32019R0947-s0056 (Regulation (EU) 2019/947, Annex, UAS.OPEN.070 Duration and validity of the remote pilot online theoretical competency and certificates of remote pilot competency)

correct: ___   supported: ___   notas: ______


---

## m04 (multi)

**Pregunta:** What data does a C1 drone broadcast through direct remote identification and what extra information does the U-space network identification service provide?

**Referencia:** Direct remote ID broadcasts the operator registration number, the UA serial number, position and height, route course and ground speed, and the pilot (or take-off) position. Network identification adds the altitude above mean sea level, the emergency status and the time the messages were generated.

**Respuesta del agente:**

> A C1 drone broadcasts the following data through its direct remote identification system:
> 
> * The UAS operator registration number and the verification code provided by the Member State of registration [32020R1058-s0024];
> * The unique physical serial number of the unmanned aircraft [32020R1058-s0024];
> * A time-stamp [32020R1058-s0024];
> * The geographical position of the unmanned aircraft and its height above the surface or take-off point [32020R1058-s0024];
> * The route course measured clockwise from true north and the ground speed of the unmanned aircraft [32020R1058-s0024];
> * The geographical position of the remote pilot or, if not available, the take-off point [32020R1058-s0024];
> * An indication of the emergency status of the UAS [32020R1058-s0024].
> 
> The U-space network identification service provides the remote identification of the UAS in an aggregated manner [32021R0664-s0021] containing:
> * The UAS operator registration number [32021R0664-s0021];
> * The unique serial number of the unmanned aircraft (or unique serial number of the add-on if privately built) [32021R0664-s0021];
> * The geographical position of the UAS, its altitude above mean sea level, and its height above the surface or take-off point [32021R0664-s0021];
> * The route course measured clockwise from true north and the ground speed of the UAS [32021R0664-s0021];
> * The geographical position of the remote pilot or, if not available, the take-off point [32021R0664-s0021];
> * The emergency status of the UAS [32021R0664-s0021];
> * The time at which the messages were generated [32021R0664-s0021].

**Pasajes recuperados:** 32019R0945-s0084 (Regulation (EU) 2019/945, Annex, Requirements for a class C1 Unmanned aircraft system (part 1/6)), 32020R1058-s0021 (Regulation (EU) 2020/1058, Annex, Requirements for a class C1 Unmanned aircraft system (part 1/8)), 32020R1058-s0029 (Regulation (EU) 2020/1058, Annex, Requirements for a class C2 Unmanned aircraft system (part 1/8)), 32019R0945-s0087 (Regulation (EU) 2019/945, Annex, Requirements for a class C1 Unmanned aircraft system (part 4/6)), 32020R1058-s0039 (Regulation (EU) 2020/1058, Annex, Requirements for a class C3 Unmanned aircraft system (part 3/7)), 32021R0664-s0021 (Regulation (EU) 2021/664, Article 8), 32021R0664-s0015 (Regulation (EU) 2021/664, Article 5 (part 1/3)), 32021R0664-s0046 (Regulation (EU) 2021/664, Annex V, Exchange of relevant operational data and information between U-space service providers and air traffic service providers in accordance with Article 7(3)), 32021R0664-s0048 (Regulation (EU) 2021/664, Annex VI, U-SPACE SERVICE PROVISION CONDITIONS AND LIMITATIONS), 32021R0664-s0042 (Regulation (EU) 2021/664, Annex II, Publication of the common information referred to in Article 5(4)(a)), 32020R1058-s0045 (Regulation (EU) 2020/1058, Annex, Requirements for a direct remote identification add-on (part 1/2)), 32020R1058-s0024 (Regulation (EU) 2020/1058, Annex, Requirements for a class C1 Unmanned aircraft system (part 4/8)), 32019R0945-s0104 (Regulation (EU) 2019/945, Annex, Requirements for a direct remote identification add-on)

correct: ___   supported: ___   notas: ______


---

## m05 (multi)

**Pregunta:** Do flights in a model aircraft club need an operational authorisation and until when could clubs keep operating under national rules?

**Referencia:** No operational authorisation or declaration is needed if the club holds an authorisation under Article 16; clubs could continue under national rules without that authorisation until 1 July 2022.

**Respuesta del agente:**

> No operational authorisation is required for operations conducted in the framework of model aircraft clubs and associations that have received an authorisation in accordance with Article 16 [32019R0947-s0018]. 
> 
> Clubs and associations could continue operating under relevant national rules without an Article 16 authorisation until **1 July 2022** [32019R0947-s0043].

**Pasajes recuperados:** 32019R0947-s0037 (Regulation (EU) 2019/947, Article 16), 32019R0947-s0018 (Regulation (EU) 2019/947, Article 5 (part 2/2)), 32019R0947-s0043 (Regulation (EU) 2019/947, Article 21), 32019R0947-s0008 (Regulation (EU) 2019/947, Recitals (part 8/8)), 32019R0947-s0060 (Regulation (EU) 2019/947, Annex, UAS.SPEC.030 Application for an operational authorisation)

correct: ___   supported: ___   notas: ______


---

## m06 (multi)

**Pregunta:** We have a 1.5 kg drone without a class label bought in 2021. Can we still fly it in the open category and under what conditions?

**Referencia:** Yes, if it was placed on the market before 1 July 2022 it can be flown in subcategory A3 (it is over 250 g), i.e. where no uninvolved person is endangered and at least 150 m from residential, commercial, industrial or recreational areas.

**Respuesta del agente:**

> Yes, you can still fly it in the open category under Article 20, provided it was placed on the market before 1 July 2022 [32019R0947-s0042]. 
> 
> Conditions:
> - It must be operated in subcategory A3 [32019R0947-s0042].
> - The maximum take-off mass must be less than 25 kg [32019R0947-s0042].
> - General open category requirements apply (e.g., kept in VLOS, max 120m height, safe distance from people, no assemblies of people) [32019R0947-s0016].

**Pasajes recuperados:** 32019R0947-s0044 (Regulation (EU) 2019/947, Article 22), 32019R0947-s0042 (Regulation (EU) 2019/947, Article 20), 32019R0947-s0016 (Regulation (EU) 2019/947, Article 4), 32019R0945-s0084 (Regulation (EU) 2019/945, Annex, Requirements for a class C1 Unmanned aircraft system (part 1/6)), 32020R1058-s0021 (Regulation (EU) 2020/1058, Annex, Requirements for a class C1 Unmanned aircraft system (part 1/8))

correct: ___   supported: ___   notas: ______


---

## u01 (unanswerable)

**Pregunta:** How long does an operational declaration for a standard scenario remain valid?

**Referencia:** The corpus does not say how long an operational declaration is valid; check the current consolidated Regulation 2019/947 or the competent authority.

**Respuesta del agente:**

> The corpus does not cover the validity period or expiration duration of an operational declaration for a standard scenario. 
> 
> You should check with your national competent authority or national aviation law to see if a specific validity period applies.

**Pasajes recuperados:** 32019R0947-s0058 (Regulation (EU) 2019/947, Annex, UAS.SPEC.020 Operational declaration (part 1/2)), 32019R0947-s0059 (Regulation (EU) 2019/947, Annex, UAS.SPEC.020 Operational declaration (part 2/2)), 32019R0947-s0068 (Regulation (EU) 2019/947, Annex, UAS.SPEC.080 Duration and validity of an operational authorisation), 32019R0947-s0018 (Regulation (EU) 2019/947, Article 5 (part 2/2)), 32019R0947-s0056 (Regulation (EU) 2019/947, Annex, UAS.OPEN.070 Duration and validity of the remote pilot online theoretical competency and certificates of remote pilot competency)

correct: ___   supported: ___   notas: ______


---

## u02 (unanswerable)

**Pregunta:** What is the maximum ground speed allowed in standard scenario STS-01?

**Referencia:** The corpus does not define the content of standard scenario STS-01; the assistant should say so.

**Respuesta del agente:**

> The corpus does not cover this question. (The harness withheld a draft answer: answer without any citation. Please check the regulation directly or ask again.)

**Pasajes recuperados:** 32019R0945-s0084 (Regulation (EU) 2019/945, Annex, Requirements for a class C1 Unmanned aircraft system (part 1/6)), 32020R1058-s0021 (Regulation (EU) 2020/1058, Annex, Requirements for a class C1 Unmanned aircraft system (part 1/8)), 32020R1058-s0079 (Regulation (EU) 2020/1058, Annex, Requirements for a class C6 unmanned aircraft system (part 1/2)), 32019R0945-s0081 (Regulation (EU) 2019/945, Annex, Requirements for a class C0 Unmanned aircraft system (part 1/3)), 32020R1058-s0019 (Regulation (EU) 2020/1058, Annex, Requirements for a class C0 Unmanned aircraft system (part 1/2)), 32021R0664-s0048 (Regulation (EU) 2021/664, Annex VI, U-SPACE SERVICE PROVISION CONDITIONS AND LIMITATIONS), 32021R0664-s0049 (Regulation (EU) 2021/664, Annex VII, [CERTIFICATE NUMBER/ISSUE No]), 32021R0664-s0040 (Regulation (EU) 2021/664, Annex I, 1. Operational conditions), 32019R0947-s0058 (Regulation (EU) 2019/947, Annex, UAS.SPEC.020 Operational declaration (part 1/2)), 32019R0945-s0135 (Regulation (EU) 2019/945, Annex, 1. BASIC NOISE EMISSION STANDARD), 32020R1058-s0071 (Regulation (EU) 2020/1058, Annex, 3. OPERATING CONDITIONS DURING TEST), 32020R1058-s0076 (Regulation (EU) 2020/1058, Annex, Requirements for a class C5 unmanned aircraft system and C5 accessories (part 1/3))

correct: ___   supported: ___   notas: ______


---

## u03 (unanswerable)

**Pregunta:** What fine does AESA impose in Spain for flying a drone without registering?

**Referencia:** The corpus covers EU regulations only and does not state national fines; consult Spanish law or AESA.

**Respuesta del agente:**

> The corpus does not cover this question. You should check the national aviation law of Spain or consult AESA (Agencia Estatal de Seguridad Aérea) directly regarding penalty amounts for unregistered drone operations.

**Pasajes recuperados:** 32019R0947-s0034 (Regulation (EU) 2019/947, Article 14 (part 2/3)), 32019R0947-s0039 (Regulation (EU) 2019/947, Article 18 (part 1/2)), 32019R0947-s0004 (Regulation (EU) 2019/947, Recitals (part 4/8)), 32019R0947-s0033 (Regulation (EU) 2019/947, Article 14 (part 1/3)), 32019R0947-s0035 (Regulation (EU) 2019/947, Article 14 (part 3/3))

correct: ___   supported: ___   notas: ______


---

## u04 (unanswerable)

**Pregunta:** What is the minimum third-party liability insurance cover required for a 20 kg drone?

**Referencia:** The corpus mentions insurance where required by Union or national law but gives no minimum amounts.

**Respuesta del agente:**

> The corpus does not cover this question. 
> 
> You should check national aviation law or consult your national competent authority, as requirements regarding third-party liability insurance are typically set at the national level within EU member states rather than in the EU drone regulations.

**Pasajes recuperados:** 32020R1058-s0037 (Regulation (EU) 2020/1058, Annex, Requirements for a class C3 Unmanned aircraft system (part 1/7)), 32019R0945-s0057 (Regulation (EU) 2019/945, Article 22 (part 5/5)), 32019R0945-s0097 (Regulation (EU) 2019/945, Annex, Requirements for a class C3 Unmanned aircraft system (part 1/6)), 32019R0947-s0062 (Regulation (EU) 2019/947, Annex, UAS.SPEC.050 Responsibilities of the UAS operator (part 1/4)), 32019R0947-s0016 (Regulation (EU) 2019/947, Article 4), 32021R0664-s0031 (Regulation (EU) 2021/664, Article 15 (part 2/2)), 32019R0947-s0073 (Regulation (EU) 2019/947, Annex, UAS.LUC.030 Safety management system (part 1/2)), 32019R0947-s0065 (Regulation (EU) 2019/947, Annex, UAS.SPEC.050 Responsibilities of the UAS operator (part 4/4)), 32019R0947-s0072 (Regulation (EU) 2019/947, Annex, UAS.LUC.020 Responsibilities of the LUC holder)

correct: ___   supported: ___   notas: ______


---

## u05 (unanswerable)

**Pregunta:** What does AESA require in Spain to approve night flights with a drone?

**Referencia:** The corpus does not contain Spanish national requirements for night operations.

**Respuesta del agente:**

> The corpus does not cover specific national administrative approval procedures required by AESA in Spain for night flights. 
> 
> You should look into the national aviation authority (Avenida de General Perón, 40, 28020 Madrid, Spain) or consult the national operational rules published directly by AESA.

**Pasajes recuperados:** 32021R0664-s0045 (Regulation (EU) 2021/664, Annex IV, UAS flight authorisation request referred to in Article 6(4)), 32019R0947-s0001 (Regulation (EU) 2019/947, Recitals (part 1/8)), 32019R0947-s0016 (Regulation (EU) 2019/947, Article 4), 32019R0947-s0017 (Regulation (EU) 2019/947, Article 5 (part 1/2)), 32019R0947-s0037 (Regulation (EU) 2019/947, Article 16), 32019R0947-s0054 (Regulation (EU) 2019/947, Annex, UAS.OPEN.060 Responsibilities of the remote pilot (part 2/3)), 32021R0664-s0050 (Regulation (EU) 2021/664, Appendix, ATS airspace classes and U-space – services provided), 32020R1058-s0034 (Regulation (EU) 2020/1058, Annex, Requirements for a class C2 Unmanned aircraft system (part 6/8)), 32019R0945-s0095 (Regulation (EU) 2019/945, Annex, Requirements for a class C2 Unmanned aircraft system (part 6/7))

correct: ___   supported: ___   notas: ______


---

## u06 (unanswerable)

**Pregunta:** How much does the competent authority charge to issue an operational authorisation?

**Referencia:** The corpus does not state any fees.

**Respuesta del agente:**

> The corpus does not cover this question. You should check the national laws or fee schedules of the competent authority in the Member State where you are registered.

**Pasajes recuperados:** 32019R0947-s0060 (Regulation (EU) 2019/947, Annex, UAS.SPEC.030 Application for an operational authorisation), 32019R0947-s0039 (Regulation (EU) 2019/947, Article 18 (part 1/2)), 32019R0947-s0061 (Regulation (EU) 2019/947, Annex, UAS.SPEC.040 Issuing of an operational authorisation), 32019R0947-s0017 (Regulation (EU) 2019/947, Article 5 (part 1/2)), 32019R0947-s0028 (Regulation (EU) 2019/947, Article 12 (part 1/3))

correct: ___   supported: ___   notas: ______
