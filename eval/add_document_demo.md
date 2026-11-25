# Adding a document: before and after

Question q27 (marked unanswerable in the test set): Do I need to use U-space services to fly in a U-space zone over Madrid?

Document added: Commission Implementing Regulation (EU) 2021/664 on a regulatory framework for the U-space (https://publications.europa.eu/resource/celex/32021R0664), file `corpus/reg-2021-664-u-space.html`.

## Before

**Tool calls:** search({'query': 'U-space services airspace requirement U-space airspace'})

**Harness events:** none

The corpus does not cover this. 

The provided EU drone regulations and EASA guidance material in our corpus do not contain specific rules detailing whether or not U-space services must be used to fly in a U-space zone over Madrid. Specifically, rules regarding the operational requirements and mandatory use of U-space services within designated U-space airspaces are not covered in the current corpus. 

To find out about the specific requirements for flying in a U-space zone in Madrid, you should check with the Spanish national aviation authority (AESA — *Agencia Estatal de Seguridad Aérea*) or consult official Spanish aeronautical information services and local geographical zone publications.

## Add the document (approval asked in the terminal)

**Tool calls:** add_document({'path': 'corpus/reg-2021-664-u-space.html'})

**Harness events:** approval granted for add_document({'path': 'corpus/reg-2021-664-u-space.html'})

The document `corpus/reg-2021-664-u-space.html` has been successfully added to the index (source ID `reg-2021-664-u-space`, 47 chunks indexed).

## After

**Tool calls:** search({'query': 'U-space services flight requirements Regulation (EU) 2019/947'})

**Harness events:** none

The corpus does not cover this fully because U-space operational regulations (such as Implementing Regulation (EU) 2021/664 on a U-space framework) are not fully integrated into the provided EU drone rules corpus, though Article 3 of the U-space regulation specifies that all UAS operations in a designated U-space airspace are subject to mandatory U-space services (such as network identification, geo-awareness, flight authorisation, and traffic information) `[reg-2021-664-u-space | Article 3 - U-space airspace]`. 

Because specific local rules, geographical zones, and national implementations for Madrid are handled by the Spanish national aviation authority (AESA), you must check with AESA or the Spanish AIS to verify current U-space deployment and service requirements for Madrid.

## Adding the same file again

**Tool calls:** add_document({'path': 'corpus/reg-2021-664-u-space.html'})

**Harness events:** approval granted for add_document({'path': 'corpus/reg-2021-664-u-space.html'})

The document `corpus/reg-2021-664-u-space.html` is already present in the index as source `reg-2021-664-u-space` (47 chunks). No changes were made.
