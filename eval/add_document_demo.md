# Adding a document: before and after

Question (q33): **¿Puede el casero negarse a que me empadrone en el piso?**

Document: Resolución de 17 de febrero de 2020 (INE / Dirección General de Cooperación Autonómica y Local), instrucciones técnicas a los Ayuntamientos sobre la gestión del Padrón municipal, BOE-A-2020-4784, consolidated text: https://www.boe.es/buscar/pdf/2020/BOE-A-2020-4784-consolidado.pdf

Approval requests shown to the user: ["add_document({'path': '/Users/enrique/daiist-assignment-3/corpus/Padron.pdf'})", "add_document({'path': '/Users/enrique/daiist-assignment-3/corpus/Padron.pdf'})"] (approved with --yes)

## 1. Before adding the document

Tool calls: ['search', 'search']

Search queries: ['empadronamiento arrendador vivienda alquiler', 'habitantes empadronamiento vivienda arrendatario padrón municipal']

- (no add_document call)

**Answer:**

No encuentro esta información en el corpus legal disponible.

_(3 model calls, 4.76 s)_

## 2. Request: Añade al corpus el documento /Users/enrique/daiist-assignment-3/corpus/Padron.pdf

Tool calls: ['add_document']

Search queries: []

- `add_document` returned: Added 'Padron': 140 chunks are now searchable.

**Answer:**

El documento `/Users/enrique/daiist-assignment-3/corpus/Padron.pdf` ha sido añadido correctamente al corpus y sus 140 fragmentos ya son buscables.

_(2 model calls, 6.45 s)_

## 3. After adding the document

Tool calls: ['search', 'search']

Search queries: ['empadronamiento arrendador vivienda inquilino', 'arrendador prohibir empadronamiento LAU']

- (no add_document call)

**Answer:**

El título que acredita la ocupación de la vivienda para el empadronamiento puede ser un contrato vigente de arrendamiento de vivienda para uso de residencia habitual acompañado del último recibo de alquiler [Padron, Disposición final quinta, p. 10]. El empadronamiento refleja el domicilio donde realmente vive cada vecino [Padron, Disposición final quinta, p. 11]. El Ayuntamiento no tiene competencias para juzgar cuestiones de arrendamientos urbanos, sino que el título solo sirve para acreditar que habitas el domicilio [Padron, Disposición final quinta, p. 10].

Parte no cubierta por el corpus: la consecuencia jurídica exacta de que el casero se niegue expresamente.
Aviso: información general basada en la legislación estatal; no es asesoramiento legal.

_(3 model calls, 4.39 s)_

## 4. Adding the same document again

Tool calls: ['add_document']

Search queries: []

- `add_document` returned: 'Padron' is already indexed and unchanged; nothing was added.

**Answer:**

El documento `/Users/enrique/daiist-assignment-3/corpus/Padron.pdf` ya estaba indexado y sin cambios, por lo que no ha sido necesario añadirlo de nuevo.

_(2 model calls, 11.28 s)_
