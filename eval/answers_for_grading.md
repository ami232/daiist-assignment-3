# Answers to grade by hand
Grade into eval/human_labels.csv (id, correct, supported, notes) BEFORE opening judge.jsonl or results.csv.

---

## q01 (single)

**Question:** ¿Cuánto tiempo mínimo tiene que envejecer un tinto de Rioja para llevar la mención «Reserva», y cuánto de ese tiempo en barrica?

**Reference:** 36 meses en total como mínimo, con al menos 12 meses en barrica de roble y al menos 6 meses en botella.

**Agent answer:**

Para llevar la mención «Reserva», un vino tinto de Rioja debe tener un envejecimiento total en barrica de roble y botella de treinta y seis meses, como mínimo [pliego_doca_rioja, Sección 3.c]. 
De ese tiempo total, la duración mínima de la crianza en barrica de roble debe ser de doce meses, seguida y complementada con un envejecimiento mínimo en botella de seis meses [pliego_doca_rioja, Sección 3.c].

<details><summary>search: Reserva tinto Rioja meses barrica tiempo mínimo</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 3.c] | Pliego de condiciones de la DOCa Rioja, page 10
Pliego de condiciones de la DOCa Rioja — Sección 3.c. CRIANZA Y ENVEJECIMIENTO DE LOS VINOS
Requisitos para el uso de los términos tradicionales “Crianza”, “Reserva” y “Gran Reserva”:
• Para el término tradicional “Crianza”:
La crianza se efectuará en las bodegas inscritas en el Registro de Bodegas de Crianza durante, al menos, dos años naturales en el caso de los vinos tintos, y de dieciocho meses en el caso de los vinos blancos y rosados.
Los vinos se someterán al sistema tradicional mixto de envejecimiento en barrica de roble de 225 litros de capacidad aproximadamente, de forma continuada y sin interrupción durante un año, como mínimo, para los vinos tintos y durante seis meses, como mínimo, para los vinos blancos y rosados, seguido y complementado con envejecimiento en botella.
El Consejo Regulador podrá adoptar acuerdos relativos al inicio del cómputo del período de envejecimiento de los vinos
• Para el término tradicional “Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de treinta y seis meses, como mínimo, con una duración mínima de crianza en barrica de roble de doce meses, seguida y complementada con un envejecimiento mínimo en botella de seis meses.
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 24 meses Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de veinticuatro meses, como mínimo, con una duración mínima de crianza en barrica de roble de seis meses.
• Para el término tradicional “Gran Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de sesenta meses, como mínimo, con una duración mínima de crianza en barrica de roble de veinticuatro meses seguida y complementada con un envejecimiento mínimo en botella de veinticuatro meses.
Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de cuarenta y ocho meses, como mínimo, con una duración mínima de envejecimiento en barrica de roble de seis meses.
• Requisitos para el uso de la mención “Gran Añada”:
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 36 meses. La mención deberá ir acompañada del año de la cosecha.

---

Result 2 | cite as [pliego_doca_rioja, Sección 8.b.10.8] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.8. Términos tradicionales
Para la denominación de origen protegida “Rioja” el término tradicional al que se refiere el artículo 118 duovicies. 1a) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, Reglamento único para las OCM, es: “Denominación de Origen Calificada”.
Los términos tradicionales, a los que se refiere el artículo 118 duovicies.1b) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, que pueden utilizarse en los vinos amparados por la denominación de origen calificada “Rioja” son: “Crianza”, “Reserva”, “Gran Reserva”, “Añejo”, “Noble” y “Viejo”.

---

Result 3 | cite as [pliego_doca_rioja, Sección 8.b.10.11] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.11. Instalaciones de envejecimiento o crianza del vino
Las instalaciones en las que se realice la actividad de envejecimiento o crianza del vino con derecho a la Denominación de Origen Calificada Rioja, deberán estar exentas de trepidaciones, con temperatura constante y fresca durante todo el año y con estado higrométrico y ventilación adecuados. A este respecto, la temperatura en la nave de barricas estará comprendida entre 10ºC y 18ºC; y el estado higrométrico deberá estar entre 60% y 90% de humedad.
Las instalaciones deberán tener unas existencias mínimas de 225 hectolitros o en proceso de envejecimiento, de los que la mitad, al menos, deberán estar contenidos en un mínimo de 50 barricas de roble de 225 litros de capacidad aproximada.

---

Result 4 | cite as [rd_1363_2011_etiquetado, Artículo 24] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 24. Menciones relativas al envejecimiento del vino con denominación de origen protegida en recipientes de madera.
1. De acuerdo con el artículo 66.2 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, para indicar que el vino con denominación de origen protegida ha sido criado o envejecido en barrica de madera de roble, además de las indicaciones que figuran en el anexo XVI del citado reglamento, se podrán utilizar los términos tradiciones «crianza», «reserva» y «gran reserva» contemplados, para España, en el la base de datos electrónica E-Bacchus de la Unión Europea.
2. Estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aún cuando se hayan empleado también en dichos procesos barricas de madera de roble.

---

Result 5 | cite as [pliego_doca_rioja, Sección 2.a.1] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Sección 2.a.1. Graduación
Los vinos amparados son: tintos, rosados y blancos, con una graduación alcohólica adquirida mínima de 11,5 % Vol. para los tintos y de 10,5 % Vol. para los blancos y rosados.
Una vez finalizada la primera fermentación, la graduación alcohólica adquirida del vino con destino a vino espumoso de calidad deberá estar comprendida entre 9,5%vol. y 11,5%vol.
Los vinos espumosos de calidad amparados dispuestos para el consumo son blancos y rosados, con una graduación alcohólica adquirida mínima de 11% vol. y máxima de 13% vol.
Los vinos protegidos, para poder llevar el nombre de las unidades geográficas menores que la región delimitada o zonas “Rioja Alta”, “Rioja Oriental” y “Rioja Alavesa”, o el de una entidad geográfica menor incluida en una de estas zonas, como los municipios, además de haber sido obtenidos totalmente a partir de uva recolectada en el ámbito territorial de la correspondiente zona o entidad geográfica menor, deben reunir las siguientes condiciones en cuanto a características analíticas.
Zonas y tipos de vinos Grado alcohólico adquirido mínimo (% vol.) Rioja Alta y Rioja Alavesa:
Tintos 11,5 Blancos 11 Rosados 10,5 Rioja Oriental:
Tintos 12 Blancos 11,5 Rosados 11 Excepcionalmente se considerará que el vino procede de la zona o del municipio si en su elaboración incluye como máximo un 15% de uva procedente de viñedos inscritos, en términos municipales limítrofes a la zona o municipio de ubicación del operador y siempre que se acredite por cualquier título jurídico válido en derecho, disponer en exclusiva por un periodo mínimo de 10 años de forma ininterrumpida del citado 15% de la uva.
Los vinos con derecho a las indicaciones Reserva y Gran Reserva deberán alcanzar una graduación adquirida mínima de 12% Vol., en el caso de los tintos, o de 11% Vol., en el caso de los blancos y rosados.

</details>

---

## q02 (single)

**Question:** ¿Qué graduación alcohólica mínima necesita un vino tinto de Rioja?

**Reference:** 11,5 % vol. para los tintos (10,5 % vol. blancos y rosados); en la zona Rioja Oriental 12 % vol. para tintos.

**Agent answer:**

Los vinos tintos de la DOCa Rioja necesitan una graduación alcohólica adquirida mínima de 11,5 % Vol [pliego_doca_rioja, Sección 2.a.1]. 
Para los vinos tintos de la zona de Rioja Oriental, el grado alcohólico adquirido mínimo exigido es del 12 % vol [pliego_doca_rioja, Sección 2.a.1]. 
Los vinos tintos con derecho a las indicaciones Reserva y Gran Reserva deben alcanzar una graduación adquirida mínima de 12 % Vol [pliego_doca_rioja, Sección 2.a.1].

<details><summary>search: graduacion alcoholica minima vino tinto Rioja</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 2.a.1] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Sección 2.a.1. Graduación
Los vinos amparados son: tintos, rosados y blancos, con una graduación alcohólica adquirida mínima de 11,5 % Vol. para los tintos y de 10,5 % Vol. para los blancos y rosados.
Una vez finalizada la primera fermentación, la graduación alcohólica adquirida del vino con destino a vino espumoso de calidad deberá estar comprendida entre 9,5%vol. y 11,5%vol.
Los vinos espumosos de calidad amparados dispuestos para el consumo son blancos y rosados, con una graduación alcohólica adquirida mínima de 11% vol. y máxima de 13% vol.
Los vinos protegidos, para poder llevar el nombre de las unidades geográficas menores que la región delimitada o zonas “Rioja Alta”, “Rioja Oriental” y “Rioja Alavesa”, o el de una entidad geográfica menor incluida en una de estas zonas, como los municipios, además de haber sido obtenidos totalmente a partir de uva recolectada en el ámbito territorial de la correspondiente zona o entidad geográfica menor, deben reunir las siguientes condiciones en cuanto a características analíticas.
Zonas y tipos de vinos Grado alcohólico adquirido mínimo (% vol.) Rioja Alta y Rioja Alavesa:
Tintos 11,5 Blancos 11 Rosados 10,5 Rioja Oriental:
Tintos 12 Blancos 11,5 Rosados 11 Excepcionalmente se considerará que el vino procede de la zona o del municipio si en su elaboración incluye como máximo un 15% de uva procedente de viñedos inscritos, en términos municipales limítrofes a la zona o municipio de ubicación del operador y siempre que se acredite por cualquier título jurídico válido en derecho, disponer en exclusiva por un periodo mínimo de 10 años de forma ininterrumpida del citado 15% de la uva.
Los vinos con derecho a las indicaciones Reserva y Gran Reserva deberán alcanzar una graduación adquirida mínima de 12% Vol., en el caso de los tintos, o de 11% Vol., en el caso de los blancos y rosados.

---

Result 2 | cite as [pliego_doca_rioja, Sección 3.b.2] | Pliego de condiciones de la DOCa Rioja, page 8
Pliego de condiciones de la DOCa Rioja — Sección 3.b.2. Características de la uva
Se dedicarán exclusivamente a la elaboración de vinos protegidos partidas de uva sana con un grado alcohólico volumétrico (% Vol.) natural mínimo de 11 % Vol. para las uvas tintas y de 10,5 % Vol. para las uvas blancas, separando las uvas tintas de las blancas en cada entrega parcial o pesada en báscula.
Se dedicarán exclusivamente a la elaboración de vinos espumosos de calidad partidas de uva sana con un grado alcohólico volumétrico (% vol.) natural mínimo de 9,5 % vol. tanto para las uvas tintas como para las uvas blancas, separando las uvas tintas de las blancas en cada entrega parcial o pesada en báscula.

---

Result 3 | cite as [pliego_doca_rioja, Sección 3.b.1] | Pliego de condiciones de la DOCa Rioja, page 7
Pliego de condiciones de la DOCa Rioja — Sección 3.b.1. Proporción de variedades por tipos de vino
TINTO En los vinos tintos elaborados con uva desgranada, deberá emplearse, como mínimo, un 95% de uva de las variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. En los vinos tintos elaborados con uva entera, este porcentaje será, como mínimo, del 85 %.
BLANCO En la elaboración de vinos blancos se emplearán exclusivamente uvas de las variedades Viura, Garnacha Blanca, Malvasía, Maturana blanca, Tempranillo blanco, Turruntés, Chardonnay, Sauvignon blanc y Verdejo.
ROSADO Se empleará un mínimo del 25 % de uvas de variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. La mezcla opcional para el supuesto de los vinos rosados deberá realizarse con posterioridad a la entrega o pesada en báscula.
VINO ESPUMOSO DE CALIDAD La elaboración se realizará con uvas de las variedades blancas y/o tintas definidas en el apartado 6.
En la elaboración de vinos espumosos de calidad rosados se empleará un mínimo del 25% de uvas de las variedades de uva tinta definidas en el apartado 6.

---

Result 4 | cite as [pliego_doca_rioja, Sección 2.a.3] | Pliego de condiciones de la DOCa Rioja, page 3
Pliego de condiciones de la DOCa Rioja — Sección 2.a.3. Intensidad colorante
La intensidad colorante mínima para los vinos tintos (A420 + A520 + A620) será de 3'5 para el caso de que la fermentación maloláctica esté realizada (máximo 0'5 g/l de ácido málico) y de 4 para el caso de que la fermentación maloláctica no éste realizada, siendo el índice de polifenoles totales mínimo de 30.
Los vinos rosados amparados deberán situarse en una intensidad de color entre 0.10 y 1.8 UA/cm, como resultado de la suma de los parámetros A420+A520+A620.

---

Result 5 | cite as [pliego_doca_rioja, Sección 8.b.10.11] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.11. Instalaciones de envejecimiento o crianza del vino
Las instalaciones en las que se realice la actividad de envejecimiento o crianza del vino con derecho a la Denominación de Origen Calificada Rioja, deberán estar exentas de trepidaciones, con temperatura constante y fresca durante todo el año y con estado higrométrico y ventilación adecuados. A este respecto, la temperatura en la nave de barricas estará comprendida entre 10ºC y 18ºC; y el estado higrométrico deberá estar entre 60% y 90% de humedad.
Las instalaciones deberán tener unas existencias mínimas de 225 hectolitros o en proceso de envejecimiento, de los que la mitad, al menos, deberán estar contenidos en un mínimo de 50 barricas de roble de 225 litros de capacidad aproximada.

</details>

---

## q03 (single)

**Question:** Para poner «Crianza» en un rosado de Rioja, ¿cuánto tiempo de envejecimiento y de barrica necesita?

**Reference:** Al menos 18 meses de crianza, con un mínimo de 6 meses en barrica de roble de unos 225 litros, seguido de botella.

**Agent answer:**

Para los vinos rosados en la DOCa Rioja, el término tradicional «Crianza» exige un envejecimiento total de al menos dieciocho meses [pliego_doca_rioja, Sección 3.c]. 
Dentro de ese periodo, el vino debe someterse a una crianza en barrica de roble de aproximadamente 225 litros de forma continuada y sin interrupción durante un mínimo de seis meses [pliego_doca_rioja, Sección 3.c]. 
El tiempo restante hasta completar los dieciocho meses se efectúa mediante envejecimiento en botella [pliego_doca_rioja, Sección 3.c].

<details><summary>search: Crianza rosado Rioja barrica envejecimiento meses</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 3.c] | Pliego de condiciones de la DOCa Rioja, page 10
Pliego de condiciones de la DOCa Rioja — Sección 3.c. CRIANZA Y ENVEJECIMIENTO DE LOS VINOS
Requisitos para el uso de los términos tradicionales “Crianza”, “Reserva” y “Gran Reserva”:
• Para el término tradicional “Crianza”:
La crianza se efectuará en las bodegas inscritas en el Registro de Bodegas de Crianza durante, al menos, dos años naturales en el caso de los vinos tintos, y de dieciocho meses en el caso de los vinos blancos y rosados.
Los vinos se someterán al sistema tradicional mixto de envejecimiento en barrica de roble de 225 litros de capacidad aproximadamente, de forma continuada y sin interrupción durante un año, como mínimo, para los vinos tintos y durante seis meses, como mínimo, para los vinos blancos y rosados, seguido y complementado con envejecimiento en botella.
El Consejo Regulador podrá adoptar acuerdos relativos al inicio del cómputo del período de envejecimiento de los vinos
• Para el término tradicional “Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de treinta y seis meses, como mínimo, con una duración mínima de crianza en barrica de roble de doce meses, seguida y complementada con un envejecimiento mínimo en botella de seis meses.
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 24 meses Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de veinticuatro meses, como mínimo, con una duración mínima de crianza en barrica de roble de seis meses.
• Para el término tradicional “Gran Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de sesenta meses, como mínimo, con una duración mínima de crianza en barrica de roble de veinticuatro meses seguida y complementada con un envejecimiento mínimo en botella de veinticuatro meses.
Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de cuarenta y ocho meses, como mínimo, con una duración mínima de envejecimiento en barrica de roble de seis meses.
• Requisitos para el uso de la mención “Gran Añada”:
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 36 meses. La mención deberá ir acompañada del año de la cosecha.

---

Result 2 | cite as [pliego_doca_rioja, Sección 8.b.10.11] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.11. Instalaciones de envejecimiento o crianza del vino
Las instalaciones en las que se realice la actividad de envejecimiento o crianza del vino con derecho a la Denominación de Origen Calificada Rioja, deberán estar exentas de trepidaciones, con temperatura constante y fresca durante todo el año y con estado higrométrico y ventilación adecuados. A este respecto, la temperatura en la nave de barricas estará comprendida entre 10ºC y 18ºC; y el estado higrométrico deberá estar entre 60% y 90% de humedad.
Las instalaciones deberán tener unas existencias mínimas de 225 hectolitros o en proceso de envejecimiento, de los que la mitad, al menos, deberán estar contenidos en un mínimo de 50 barricas de roble de 225 litros de capacidad aproximada.

---

Result 3 | cite as [pliego_doca_rioja, Sección 8.b.10.8] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.8. Términos tradicionales
Para la denominación de origen protegida “Rioja” el término tradicional al que se refiere el artículo 118 duovicies. 1a) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, Reglamento único para las OCM, es: “Denominación de Origen Calificada”.
Los términos tradicionales, a los que se refiere el artículo 118 duovicies.1b) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, que pueden utilizarse en los vinos amparados por la denominación de origen calificada “Rioja” son: “Crianza”, “Reserva”, “Gran Reserva”, “Añejo”, “Noble” y “Viejo”.

---

Result 4 | cite as [rd_1363_2011_etiquetado, Artículo 24] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 24. Menciones relativas al envejecimiento del vino con denominación de origen protegida en recipientes de madera.
1. De acuerdo con el artículo 66.2 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, para indicar que el vino con denominación de origen protegida ha sido criado o envejecido en barrica de madera de roble, además de las indicaciones que figuran en el anexo XVI del citado reglamento, se podrán utilizar los términos tradiciones «crianza», «reserva» y «gran reserva» contemplados, para España, en el la base de datos electrónica E-Bacchus de la Unión Europea.
2. Estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aún cuando se hayan empleado también en dichos procesos barricas de madera de roble.

---

Result 5 | cite as [pliego_doca_rioja, Sección 3.b.1] | Pliego de condiciones de la DOCa Rioja, page 7
Pliego de condiciones de la DOCa Rioja — Sección 3.b.1. Proporción de variedades por tipos de vino
TINTO En los vinos tintos elaborados con uva desgranada, deberá emplearse, como mínimo, un 95% de uva de las variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. En los vinos tintos elaborados con uva entera, este porcentaje será, como mínimo, del 85 %.
BLANCO En la elaboración de vinos blancos se emplearán exclusivamente uvas de las variedades Viura, Garnacha Blanca, Malvasía, Maturana blanca, Tempranillo blanco, Turruntés, Chardonnay, Sauvignon blanc y Verdejo.
ROSADO Se empleará un mínimo del 25 % de uvas de variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. La mezcla opcional para el supuesto de los vinos rosados deberá realizarse con posterioridad a la entrega o pesada en báscula.
VINO ESPUMOSO DE CALIDAD La elaboración se realizará con uvas de las variedades blancas y/o tintas definidas en el apartado 6.
En la elaboración de vinos espumosos de calidad rosados se empleará un mínimo del 25% de uvas de las variedades de uva tinta definidas en el apartado 6.

</details>

---

## q04 (single)

**Question:** ¿Cuál es la producción máxima de uva por hectárea para las variedades tintas en Rioja?

**Reference:** 6.500 kg de uva por hectárea (45,5 hl); 9.000 kg/ha para variedades blancas.

**Agent answer:**

La producción máxima admitida por hectárea para las variedades tintas en Rioja es de 6.500 kg de uva, equivalente a 45,5 Hl [pliego_doca_rioja, Sección 5]. Para las uvas destinadas a la elaboración de vinos con el reconocimiento de «viñedo singular», la producción máxima es de 5.000 kg de uva, equivalente a 32,50 Hl [pliego_doca_rioja, Sección 5]. Además, esta producción máxima puede ser modificada anualmente por el Consejo Regulador, pudiendo incrementarse hasta un máximo de 8.125 kg por hectárea o reducirse hasta 5.525 kg por hectárea según las circunstancias de la campaña [pliego_doca_rioja, Sección 8.b.6.1].

<details><summary>search: producción máxima uva hectárea variedades tintas Rioja</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 5] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 5. Rendimiento Máximo
La producción máxima admitida por hectárea será de 6.500 kg de uva, equivalente a 45,5 Hl para las variedades tintas, y de 9.000 kg, equivalente a 63 Hl para las variedades blancas.
Los rendimientos de producción de uva se contabilizarán de forma separada e independiente para las variedades tintas y para las variedades blancas, sin que quepa compensación de colores.
La producción máxima admitida por hectárea en el caso de uva destinada a la elaboración de vinos con reconocimiento de la entidad geográfica menor ‘viñedo singular’, será de 5.000 kg de uva, equivalente a 32,50 Hl para las variedades tintas, y de 6.922 kg, equivalente a 44,99 Hl para las variedades blancas. Este rendimiento no podrá ser modificado en ningún caso.

---

Result 2 | cite as [pliego_doca_rioja, Sección 8.b.6.1] | Pliego de condiciones de la DOCa Rioja, page 25
Pliego de condiciones de la DOCa Rioja — Sección 8.b.6.1. Variación del rendimiento amparable
No obstante, lo establecido en el epígrafe 5, la producción máxima admitida por hectárea podrá ser modificada anualmente por el Consejo Regulador, sin que pueda superar, al alza, 8.125 kg por hectárea para las variedades tintas y 11.250 kg por hectárea para las variedades blancas. Del mismo modo, en función de las circunstancias de la Campaña, el Consejo Regulador podrá reducir la producción máxima admitida por hectárea hasta 5.525 kg por hectárea para las variedades tintas y 7.650 kg por hectárea para las variedades blancas.
El control de la producción se efectuará de conformidad con lo previsto en las Normas de Campaña.

---

Result 3 | cite as [pliego_doca_rioja, Sección 3.b.1] | Pliego de condiciones de la DOCa Rioja, page 7
Pliego de condiciones de la DOCa Rioja — Sección 3.b.1. Proporción de variedades por tipos de vino
TINTO En los vinos tintos elaborados con uva desgranada, deberá emplearse, como mínimo, un 95% de uva de las variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. En los vinos tintos elaborados con uva entera, este porcentaje será, como mínimo, del 85 %.
BLANCO En la elaboración de vinos blancos se emplearán exclusivamente uvas de las variedades Viura, Garnacha Blanca, Malvasía, Maturana blanca, Tempranillo blanco, Turruntés, Chardonnay, Sauvignon blanc y Verdejo.
ROSADO Se empleará un mínimo del 25 % de uvas de variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. La mezcla opcional para el supuesto de los vinos rosados deberá realizarse con posterioridad a la entrega o pesada en báscula.
VINO ESPUMOSO DE CALIDAD La elaboración se realizará con uvas de las variedades blancas y/o tintas definidas en el apartado 6.
En la elaboración de vinos espumosos de calidad rosados se empleará un mínimo del 25% de uvas de las variedades de uva tinta definidas en el apartado 6.

---

Result 4 | cite as [pliego_doca_rioja, Sección 6] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 6. Variedades De Uva
La elaboración de los vinos protegidos se realizará exclusivamente con uvas de las variedades siguientes:
TINTAS BLANCAS Tempranillo Garnacha tinta Graciano Mazuelo Maturana tinta Viura Sauvignon blanc Malvasía Verdejo Garnacha Blanca Maturana blanca Chardonnay Tempranillo blanco Turruntés La uva procedente de plantaciones de viñedo efectuadas con anterioridad al 1 de enero de 1956 y con variedades de uva distintas a las que figuran en el Reglamento de la Denominación, pueden ser empleadas en la elaboración de vinos protegidos, en tanto subsistan dichas plantaciones. En el caso de la variedad vinífera Calagraño, las plantaciones han de ser anteriores a 27 de octubre de 1970.

---

Result 5 | cite as [pliego_doca_rioja, Sección 3] | Pliego de condiciones de la DOCa Rioja, page 6
Pliego de condiciones de la DOCa Rioja — Sección 3. Prácticas Específicas Para Elaboración Y Restricciones
IMPUESTAS.

</details>

---

## q05 (single)

**Question:** ¿Puedo elaborar un blanco de Rioja con uva Albariño?

**Reference:** No. Las variedades blancas autorizadas son Viura, Malvasía, Verdejo, Garnacha Blanca, Maturana blanca, Chardonnay, Sauvignon blanc, Tempranillo blanco y Turruntés; el Albariño no está.

**Agent answer:**

No, no puedes elaborar un vino blanco de Rioja protegido con uva Albariño [pliego_doca_rioja, Sección 3.b.1]. En la elaboración de vinos blancos de la DOCa Rioja se emplearán exclusivamente uvas de las variedades Viura, Garnacha Blanca, Malvasía, Maturana blanca, Tempranillo blanco, Turruntés, Chardonnay, Sauvignon blanc y Verdejo [pliego_doca_rioja, Sección 3.b.1]. La variedad Albariño no figura entre las variedades blancas autorizadas en el pliego de condiciones de la denominación [pliego_doca_rioja, Sección 6].

<details><summary>search: variedades autorizadas blanco rioja albariño</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 6] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 6. Variedades De Uva
La elaboración de los vinos protegidos se realizará exclusivamente con uvas de las variedades siguientes:
TINTAS BLANCAS Tempranillo Garnacha tinta Graciano Mazuelo Maturana tinta Viura Sauvignon blanc Malvasía Verdejo Garnacha Blanca Maturana blanca Chardonnay Tempranillo blanco Turruntés La uva procedente de plantaciones de viñedo efectuadas con anterioridad al 1 de enero de 1956 y con variedades de uva distintas a las que figuran en el Reglamento de la Denominación, pueden ser empleadas en la elaboración de vinos protegidos, en tanto subsistan dichas plantaciones. En el caso de la variedad vinífera Calagraño, las plantaciones han de ser anteriores a 27 de octubre de 1970.

---

Result 2 | cite as [pliego_doca_rioja, Sección 3.b.1] | Pliego de condiciones de la DOCa Rioja, page 7
Pliego de condiciones de la DOCa Rioja — Sección 3.b.1. Proporción de variedades por tipos de vino
TINTO En los vinos tintos elaborados con uva desgranada, deberá emplearse, como mínimo, un 95% de uva de las variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. En los vinos tintos elaborados con uva entera, este porcentaje será, como mínimo, del 85 %.
BLANCO En la elaboración de vinos blancos se emplearán exclusivamente uvas de las variedades Viura, Garnacha Blanca, Malvasía, Maturana blanca, Tempranillo blanco, Turruntés, Chardonnay, Sauvignon blanc y Verdejo.
ROSADO Se empleará un mínimo del 25 % de uvas de variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. La mezcla opcional para el supuesto de los vinos rosados deberá realizarse con posterioridad a la entrega o pesada en báscula.
VINO ESPUMOSO DE CALIDAD La elaboración se realizará con uvas de las variedades blancas y/o tintas definidas en el apartado 6.
En la elaboración de vinos espumosos de calidad rosados se empleará un mínimo del 25% de uvas de las variedades de uva tinta definidas en el apartado 6.

---

Result 3 | cite as [pliego_doca_rioja, Encabezado] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Encabezado
REGISTRO:
Número de expediente en el registro comunitario: PDO-ES-A0117 Fecha de recepción por la Comisión Europea: 11/11/2011.Fecha de modificación (eliminación restricción uso de marcas): 26/11/2014.
MODIFICACIONES:
Número de expediente en el registro comunitario: PDO-ES-A0117-AM03.
Fecha de modificación (corrección de errores): 29/02/2016.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM04.
Fecha de modificación (uso variedades en blancos y rosados y tiempos de envejecimiento): 14/7/2017.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM05.
Fecha de modificación (viñedo singular, vino espumoso, zona, municipio, intensidad colorante rosados): 15/02/2018.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM06.
Fecha de modificación (inicio computo envejecimiento): 24/09/2018.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM07.
Fecha de modificación (crianza de blancos y rosados): 23/09/2019.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM08.
Fecha de modificación (delimitación de viñedo singular, referencia requisitos mínimos de etiquetado): 31/01/2020 y 05/11/2020.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM09.
Fecha de modificación (plantaciones mixtas, calificación e informes sobre viñedos, delimitación viñedos singulares, condiciones instalaciones envejecimiento): 18-11-2021.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM10.
Fecha de modificación (nuevos tipos de vinos espumosos de calidad, cambios en la vendimia de uvas destinadas a vinos espumosos de calidad, cambios en las descripciones organolépticas, delimitación viñedos singulares, destino exclusivo de la producción de las viñas inscritas en Registro de Viñas a elaboración de vino amparado): 01-05-2023 y 07-06-2023 PLIEGO DE CONDICIONES DE LA DENOMINACIÓN DE ORIGEN PROTEGIDA (Denominación de Origen Calificada) “RIOJA”

---

Result 4 | cite as [pliego_doca_rioja, Sección 2.a.1] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Sección 2.a.1. Graduación
Los vinos amparados son: tintos, rosados y blancos, con una graduación alcohólica adquirida mínima de 11,5 % Vol. para los tintos y de 10,5 % Vol. para los blancos y rosados.
Una vez finalizada la primera fermentación, la graduación alcohólica adquirida del vino con destino a vino espumoso de calidad deberá estar comprendida entre 9,5%vol. y 11,5%vol.
Los vinos espumosos de calidad amparados dispuestos para el consumo son blancos y rosados, con una graduación alcohólica adquirida mínima de 11% vol. y máxima de 13% vol.
Los vinos protegidos, para poder llevar el nombre de las unidades geográficas menores que la región delimitada o zonas “Rioja Alta”, “Rioja Oriental” y “Rioja Alavesa”, o el de una entidad geográfica menor incluida en una de estas zonas, como los municipios, además de haber sido obtenidos totalmente a partir de uva recolectada en el ámbito territorial de la correspondiente zona o entidad geográfica menor, deben reunir las siguientes condiciones en cuanto a características analíticas.
Zonas y tipos de vinos Grado alcohólico adquirido mínimo (% vol.) Rioja Alta y Rioja Alavesa:
Tintos 11,5 Blancos 11 Rosados 10,5 Rioja Oriental:
Tintos 12 Blancos 11,5 Rosados 11 Excepcionalmente se considerará que el vino procede de la zona o del municipio si en su elaboración incluye como máximo un 15% de uva procedente de viñedos inscritos, en términos municipales limítrofes a la zona o municipio de ubicación del operador y siempre que se acredite por cualquier título jurídico válido en derecho, disponer en exclusiva por un periodo mínimo de 10 años de forma ininterrumpida del citado 15% de la uva.
Los vinos con derecho a las indicaciones Reserva y Gran Reserva deberán alcanzar una graduación adquirida mínima de 12% Vol., en el caso de los tintos, o de 11% Vol., en el caso de los blancos y rosados.

---

Result 5 | cite as [pliego_doca_rioja, Sección 5] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 5. Rendimiento Máximo
La producción máxima admitida por hectárea será de 6.500 kg de uva, equivalente a 45,5 Hl para las variedades tintas, y de 9.000 kg, equivalente a 63 Hl para las variedades blancas.
Los rendimientos de producción de uva se contabilizarán de forma separada e independiente para las variedades tintas y para las variedades blancas, sin que quepa compensación de colores.
La producción máxima admitida por hectárea en el caso de uva destinada a la elaboración de vinos con reconocimiento de la entidad geográfica menor ‘viñedo singular’, será de 5.000 kg de uva, equivalente a 32,50 Hl para las variedades tintas, y de 6.922 kg, equivalente a 44,99 Hl para las variedades blancas. Este rendimiento no podrá ser modificado en ningún caso.

</details>

---

## q06 (single)

**Question:** ¿Se puede embotellar vino de Rioja fuera de la zona de producción?

**Reference:** No. El embotellado debe hacerse exclusivamente en bodegas inscritas autorizadas por el Consejo Regulador; si no, el vino pierde el derecho a la denominación.

**Agent answer:**

No, el embotellado de los vinos de la DOCa Rioja debe realizarse exclusivamente en las bodegas inscritas autorizadas por el Consejo Regulador [pliego_doca_rioja, Sección 8.b.10.5]. En caso contrario, el vino pierde el derecho al uso de la denominación [pliego_doca_rioja, Sección 8.b.10.5]. Este requisito se exige porque el transporte y el embotellado fuera de la zona de producción implican un riesgo más elevado para la calidad del producto [pliego_doca_rioja, Sección 8.b.10.5].

<details><summary>search: embotellar Rioja fuera de la zona de producción</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 8.b.10.5] | Pliego de condiciones de la DOCa Rioja, page 31
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.5. Embotellado en origen y otros requisitos de embotellado
El embotellado de vinos amparados por la denominación de origen calificada Rioja deberá ser realizado exclusivamente en las bodegas inscritas autorizadas por el Consejo Regulador, perdiendo el vino en otro caso el derecho al uso de la denominación.
Este requisito se establece al constatar que el riesgo para la calidad del vino finalmente ofrecido al consumo es más elevado cuando el vino ha sido transportado y embotellado fuera de la zona de producción que cuando estas operaciones se realizan en dicha zona. Sirve para proteger la gran reputación del vino de Rioja mediante un reforzamiento del control de sus características particulares y de su calidad protegiendo la denominación de origen calificada de la que es beneficiaria la colectividad de productores afectados. La decisión fue reconocida por sentencia del Tribunal de Justicia de la Unión Europea de 16 de mayo de 2000.
Los vinos amparados únicamente pueden circular y ser expedidos en los tipos de envase que no perjudiquen su calidad o prestigio y aprobados por el Consejo Regulador. Con carácter general los envases deberán ser de vidrio, de las capacidades autorizadas por la Unión Europea a excepción de la gama de un litro.
Excepcionalmente, el Consejo Regulador podrá autorizar para usos especiales otros tipos de envase, que entienda no perjudican la calidad o prestigio de los vinos protegidos.
No se permitirán embotellados por encargo en los casos de vinos procedentes de viñedos singulares.

---

Result 2 | cite as [pliego_doca_rioja, Sección 7.a] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 7.a. ÁREA GEOGRÁFICA (parte 6/7)
- las instalaciones de dichas bodegas han de estar claramente separadas de aquellas en las que se producen y almacenan vinos sin derecho a la denominación de origen calificada (artículo 24).
73. Así pues, resulta que, para los vinos de Rioja transportados y embotellados en la zona de producción, los controles son profundos y sistemáticos, son responsabilidad de la colectividad de los propios productores, que tienen un interés primordial en la conservación de la reputación adquirida, y sólo los lotes que hayan sido sometidos a tales controles pueden llevar la denominación de origen calificada.
74. De estas afirmaciones se deduce que el riesgo para la calidad del producto finalmente ofrecido al consumo es más elevado cuando dicho producto ha sido transportado y embotellado fuera de la zona de producción que cuando estas operaciones se realizan en dicha zona.
75. Por consiguiente, ha de admitirse que la obligatoriedad del embotellado en origen el requisito controvertido, que tiene como objetivo proteger la gran reputación del vino de Rioja mediante un reforzamiento del control de sus características particulares y de su calidad, está justificado por ser una medida que protege la denominación de origen calificada de la que es beneficiaria la colectividad de productores afectados y que reviste para éstos una importancia decisiva.
77. A este respecto, la denominación de origen calificada no quedaría protegida de forma comparable mediante la obligación, impuesta a los operadores establecidos fuera de la zona de producción, de informar a los consumidores, a través de un etiquetado adecuado, de que el embotellado se ha producido fuera de dicha zona. En efecto, un menoscabo de la calidad del vino embotellado fuera de la zona de producción que fuera consecuencia de la realización de los riesgos derivados del transporte a granel y/o de la operación de embotellado correlativa, podría afectar negativamente a la reputación de todos los vinos comercializados bajo la denominación de origen calificada Rioja, incluidos los embotellados en la zona de producción bajo el control de la colectividad titular de la denominación.

---

Result 3 | cite as [pliego_doca_rioja, Sección 7.a] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 7.a. ÁREA GEOGRÁFICA (parte 5/7)
57. Debe señalarse que un vino de calidad es un producto caracterizado por una gran especificidad, circunstancia que, en cualquier caso, no se discute por lo que respecta al vino de Rioja. Sus cualidades y características particulares, que resultan de la conjunción de una serie de factores naturales y humanos, están vinculadas a su zona geográfica de origen y su mantenimiento requiere vigilancia y esfuerzos.
58. La normativa de la denominación de origen calificada Rioja tiene por objeto garantizar el mantenimiento de estas cualidades y características. Al garantizar a los operadores del sector vitivinícola de la zona de La Rioja, a petición de los cuales se reconoció la denominación de origen, también el control del embotellado, su objeto es proteger mejor la calidad del producto y, en consecuencia, la reputación de la denominación, cuya responsabilidad asumen en la actualidad plena y colectivamente dichos operadores.
60. A este respecto, el Gobierno español, apoyado por los Gobiernos italiano y portugués y por la Comisión, alega que, sin el requisito controvertido, podría efectivamente peligrar la reputación de la denominación de origen calificada Rioja. En efecto, el transporte y el embotellado fuera de la zona de producción suponen riesgos para la calidad del vino. El requisito controvertido contribuye de forma decisiva a la protección de las características particulares y de la calidad del producto, puesto que equivale a confiar a los productores y al Consejo Regulador del Rioja, es decir, a quienes poseen los conocimientos y la técnica necesarios, así como un interés primordial en la conservación de la reputación adquirida, la aplicación y el control del respeto de todas las normas relativas al transporte y al embotellado.
71. ‘… la normativa española de que se trata prevé que los vinos que pueden llevar una denominación de origen calificada deben ser sometidos, partida por partida, a exámenes organolépticos y analíticos…’.
72. Además, de conformidad con el Reglamento Rioja:
- toda expedición de vino de Rioja a granel dentro de la zona debe ser previamente autorizada por el Consejo Regulador del Rioja (artículo 31),
- el embotellado sólo puede ser efectuado por bodegas embotelladoras autorizadas por el Consejo Regulador del Rioja (artículo 32),

---

Result 4 | cite as [pliego_doca_rioja, Sección 7.a] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 7.a. ÁREA GEOGRÁFICA (parte 7/7)
En términos más generales, la mera coexistencia de dos procesos de embotellado diferentes, dentro o fuera de la zona de producción, con o sin el control sistemático efectuado por dicha colectividad, podría reducir el crédito de confianza de que goza la denominación entre los consumidores convencidos de que todas las etapas de producción de un v.c.p.r.d. reputado deben efectuarse bajo el control y la responsabilidad de la colectividad beneficiaria de la denominación.” Con fecha 7 de junio de 2017, el Pleno del Consejo Regulador de la Denominación de Origen Calificada Rioja acordó la inclusión de una nueva categoría de producto que permitirá el amparo de la producción de vinos espumosos blancos y rosados de calidad obtenidos mediante el método tradicional.
La elaboración de vinos espumosos en la región no es novedosa. El historiador D. Manuel Llano Gorostiza ya citaba en su libro titulado Los Vinos de Rioja (1973) la Exposición de Agricultura de Madrid en el año 1857, donde se presentaron algunos vinos de Rioja Alta y Alavesa: “Tintos, blancos y espumosos hechos por el método de Champaña”. Esta mención situaría la primera elaboración de vinos espumosos en España en el año 1857, con un origen riojano.
La elaboración de vinos espumosos en Rioja, vino más tarde de la mano de la sociedad francesa 'Savignon Frères et Cie', establecida en el Barrio de la Estación de Haro en 1857, y que en el año 1890 contrató a un maestro champañero de Reims para desarrollar la elaboración de este tipo de vinos.

---

Result 5 | cite as [pliego_doca_rioja, Sección 4] | Pliego de condiciones de la DOCa Rioja, page 11
Pliego de condiciones de la DOCa Rioja — Sección 4. Delimitación De La Zona Geográfica (parte 1/3)
La zona de producción, crianza y envejecimiento está constituida por los terrenos ubicados en los términos municipales que se citan a continuación, que constituyen las zonas denominadas “Rioja Alta”, “Rioja Oriental” y “Rioja Alavesa”.
El Consejo Regulador determinará la ampliación de la zona geográfica a partir de informes que acrediten tanto la aptitud de los terrenos para la producción de uva de las variedades con la calidad necesaria para producir vinos de las características específicas de los protegidos por la denominación.
La calificación de los terrenos a la que se refiere el apartado e) Denominación de Origen Calificada, Términos Tradicionales, de la Disposición Adicional Tercera de la Ley 6/2015, de 12 de mayo, de Denominaciones de Origen e Indicaciones Geográficas Protegidas de ámbito territorial supraautonómico, será realizada por el Consejo Regulador.
Para las nuevas plantaciones o replantaciones en terrenos o viñedos situados en la zona de producción, así como para las modificaciones de las condiciones que puedan afectar al cumplimiento de este pliego de condiciones, será preceptivo el informe del Consejo Regulador, a efectos de su inscripción en el Registro correspondiente de la Denominación.

</details>

---

## q07 (single)

**Question:** ¿Qué tiene que aparecer obligatoriamente en la etiqueta de un Rioja en relación con la denominación?

**Reference:** El nombre de la denominación de forma destacada con la mención «Denominación de Origen Calificada» justo debajo y el sello del Consejo Regulador; además, marca comercial y nombre o razón social de una bodega inscrita.

**Agent answer:**

En las etiquetas de vinos envasados de Rioja figurará obligatoriamente de forma destacada el nombre de la denominación junto con la mención "Denominación de Origen Calificada" justo debajo de aquél y el sello del Consejo Regulador [pliego_doca_rioja, Sección 8.b.9].

<details><summary>search: etiqueta Rioja denominación obligatoriamente</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 8.b.9] | Pliego de condiciones de la DOCa Rioja, page 28
Pliego de condiciones de la DOCa Rioja — Sección 8.b.9. DESIGNACION, ETIQUETADO (parte 1/3)
En las etiquetas de vinos envasados figurará obligatoriamente de forma destacada el nombre de la denominación junto con la mención “Denominación de Origen Calificada” justo debajo de aquél y el sello del Consejo Regulador, además de las menciones obligatorias que se determinen en la normativa y regulación específica, así como en la legislación aplicable. Así mismo podrán figurar las menciones facultativas y unidades geográficas menores en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable, si bien no podrán destacar respecto al nombre de “RIOJA”.
Antes de la puesta en circulación de etiquetas, éstas deberán ser autorizadas por el Consejo Regulador, en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable.
En el etiquetado de los vinos protegidos por la Denominación de Origen Calificada Rioja será obligatoria la indicación de la correspondiente marca comercial.
En el etiquetado deberá figurar obligatoriamente el nombre o razón social de una bodega inscrita. También podrá utilizarse un nombre comercial, en la forma prevista en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado de la expresión “Maceración carbónica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado principal de vinos blancos y rosados de la expresión “Fermentado en barrica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable Se prohíbe la utilización de cualquier tipo de referencia o alusión a las expresiones "barrica" y "madera" en la comercialización, propaganda y etiquetado de los vinos genéricos (sin agotar procesos de crianza).
Únicamente puede aplicarse a un vino el nombre de una zona o municipio cuando el vino proceda exclusivamente de uva de tal zona de producción o municipio, y su elaboración, crianza en su caso y embotellado se realicen en los mismos.

---

Result 2 | cite as [pliego_doca_rioja, Sección 8.b.10.3] | Pliego de condiciones de la DOCa Rioja, page 30
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.3. Pruebas de conformidad
Cualquiera que sea el tipo de envase en que se expidan los vinos para el consumo, irán provistos de precintas de garantía, etiquetas o contraetiquetas numeradas, expedidas por el Consejo Regulador, y siempre en forma que no permita una segunda utilización. Deberá existir correspondencia entre las contraetiquetas, etiquetas y elementos de control del Consejo Regulador.
Para los vinos espumosos de calidad, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Método Tradicional”.
Para los vinos procedentes de ‘viñedo singular’, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Viñedo Singular”.
Para los vinos procedentes de zona o de municipio, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas con numeración controlada.
Si concurren las dos indicaciones en el vino o concurren con la de ‘Viñedo Singular’, se utilizará la precinta correspondiente a la unidad geográfica de menor tamaño.
Para los vinos de Crianza, Reserva y Gran Reserva, el Consejo Regulador expedirá contraetiquetas específicas y autorizará la mención de dichas indicaciones en la etiqueta.

---

Result 3 | cite as [pliego_doca_rioja, Sección 8.b.10.5] | Pliego de condiciones de la DOCa Rioja, page 31
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.5. Embotellado en origen y otros requisitos de embotellado
El embotellado de vinos amparados por la denominación de origen calificada Rioja deberá ser realizado exclusivamente en las bodegas inscritas autorizadas por el Consejo Regulador, perdiendo el vino en otro caso el derecho al uso de la denominación.
Este requisito se establece al constatar que el riesgo para la calidad del vino finalmente ofrecido al consumo es más elevado cuando el vino ha sido transportado y embotellado fuera de la zona de producción que cuando estas operaciones se realizan en dicha zona. Sirve para proteger la gran reputación del vino de Rioja mediante un reforzamiento del control de sus características particulares y de su calidad protegiendo la denominación de origen calificada de la que es beneficiaria la colectividad de productores afectados. La decisión fue reconocida por sentencia del Tribunal de Justicia de la Unión Europea de 16 de mayo de 2000.
Los vinos amparados únicamente pueden circular y ser expedidos en los tipos de envase que no perjudiquen su calidad o prestigio y aprobados por el Consejo Regulador. Con carácter general los envases deberán ser de vidrio, de las capacidades autorizadas por la Unión Europea a excepción de la gama de un litro.
Excepcionalmente, el Consejo Regulador podrá autorizar para usos especiales otros tipos de envase, que entienda no perjudican la calidad o prestigio de los vinos protegidos.
No se permitirán embotellados por encargo en los casos de vinos procedentes de viñedos singulares.

---

Result 4 | cite as [pliego_doca_rioja, Sección 8.b.9] | Pliego de condiciones de la DOCa Rioja, page 28
Pliego de condiciones de la DOCa Rioja — Sección 8.b.9. DESIGNACION, ETIQUETADO (parte 2/3)
Excepcionalmente se considerará que el vino procede de la zona o del municipio si en su elaboración incluye como máximo un 15% de uva procedente de viñedos inscritos, en términos municipales limítrofes a la zona o municipio de ubicación del operador y siempre que se acredite por cualquier título jurídico válido en derecho, disponer en exclusiva por un periodo mínimo de 10 años de forma ininterrumpida del citado 15% de la uva.
Estos vinos se verán sometidos a un sistema de control previsto en la normativa y regulación específica, así como en la legislación aplicable.
En los vinos espumosos de calidad figurará el término relativo al contenido en azúcar, además de la expresión “Método Tradicional” en todas las etiquetas que porte la botella, o en todos los campos visuales si se trata de una etiqueta continua.
La expresión “Método Tradicional” se ubicará inmediatamente debajo del término relativo al contenido en azúcar y con caracteres de tamaño equivalentes como máximo a los utilizados para indicar el nombre de la Denominación “Rioja”.
En la etiqueta que porte las menciones obligatorias, los caracteres de la expresión “Método Tradicional” no podrán representarse en un tamaño inferior a 0,3 cm.
De conformidad con lo establecido en el punto segundo de la Disposición adicional cuarta de la Ley 6/2015, de 12 de mayo, de Denominaciones de Origen e Indicaciones Geográficas Protegidas de ámbito territorial supra autonómico, la regulación relativa a un paraje vitícola identificado que contempla el primer punto de la misma Disposición puede ser extensible a las Denominaciones de Origen Calificadas de vinos de ámbito territorial supra autonómico.
A estos efectos, en el caso de los vinos amparados por la Denominación de Origen Calificada ‘Rioja’, los operadores acogidos a la misma que cumplan los requisitos específicos establecidos en este pliego podrán solicitar hacer uso de la designación ‘viñedo singular’ en el etiquetado, presentación y publicidad de este.

---

Result 5 | cite as [pliego_doca_rioja, Sección 8.b.10.10] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.10. Etiquetado y adscripción exclusiva de las marcas utilizadas
Las marcas utilizadas en los etiquetados que incluyan el nombre de un municipio serán exclusivas para el vino con esta procedencia geográfica, para lo cual el titular presentará una declaración responsable relativa a este uso exclusivo de la marca en dichos vinos. De no mediar esta declaración, las etiquetas utilizadas para el vino de municipio serán diferentes de las utilizadas por la bodega para el resto de sus vinos, en orden a evitar la confusión del consumidor.

</details>

---

## q08 (single)

**Question:** ¿Puedo poner el nombre de mi municipio en la etiqueta si un 10 % de la uva viene de un pueblo vecino?

**Reference:** Sí, excepcionalmente: se admite hasta un 15 % de uva de viñedos inscritos en municipios limítrofes si se acredita disponer de ella en exclusiva al menos 10 años ininterrumpidos.

**Agent answer:**

No, no puede utilizar el nombre de su municipio en la etiqueta, ya que únicamente puede aplicarse a un vino el nombre de una zona o municipio cuando el vino proceda exclusivamente de uva de tal zona de producción o municipio [pliego_doca_rioja, Sección 8.b.9].

<details><summary>search: </summary>

Error executing tool search: 1 validation error for searchArguments
query
  Field required [type=missing, input_value={'queries': ['municipio e...ueta rioja uva origen']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.14/v/missing

</details>

<details><summary>search: municipio etiqueta rioja uva origen</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 4] | Pliego de condiciones de la DOCa Rioja, page 11
Pliego de condiciones de la DOCa Rioja — Sección 4. Delimitación De La Zona Geográfica (parte 2/3)
RIOJA ALTA Comunidad Autónoma de La Rioja Ábalos Camprovín Foncea Matute Tirgo Alesanco Canillas Fonzaleche Medrano Tormantos Alesón Cañas Fuenmayor Nájera Torrecilla sobre Alesanco Anguciana Cárdenas Galbárruli Navarrete Torremontalbo Arenzana de Abajo Casalarreina Gimileo Ochánduri Treviana Arenzana de Arriba Castañares de Rioja Haro Ollauri Tricio Azofra Cellórigo Hervías Rodezno Uruñuela Badarán Cenicero Herramélluri Sajazarra Ventosa Bañares Cidamón Hormilla San Asensio Villalba de Rioja Baños de Río Tobía Cihuri Hormilleja San Millán de Yécora Villar de Torre Baños de Rioja Cirueña Hornos de Moncalvillo San Torcuato Villarejo Berceo Bezares Cordovín Huércanos San Vicente de la Sonsierra Zarratón Bobadilla Cuzcurrita de Río Tirón Lardero Santa Coloma Briñas Daroca de Rioja Leiva Sojuela Briones Entrena Logroño Sorzano Estollo Manjarrés Sotés Provincia de Burgos (Miranda de Ebro) El Ternero (enclave) RIOJA ORIENTAL Comunidad Autónoma de La Rioja Agoncillo Arrúbal Cornago Molinos de Ocón Rincón de Soto Aguilar del Río Ausejo El Redal Murillo de Río Leza Santa Engracia de Jubera (Zona Norte) Alhama Albelda Autol El villar de Arnedo Muro de aguas Santa Eulalia Bajera Alberite Bergasilla Galilea Nalda Tudelilla Alcanadre Bergasa Grávalos Ocón (La Villa) Villamediana de Iregua Aldeanueva de Ebro Calahorra Herce Pradejón Villarroya Alfaro Cervera del Río Alhama Igea Préjano Arnedillo Clavijo Lagunilla de Jubera Quel Arnedo Corera Leza del Río Leza Ribafrecha Comunidad Autónoma de Navarra Andosilla Bargota San Adrián Viana Aras Mendavia Sartaguda Azagra RIOJA ALAVESA Provincia de Álava Baños de Ebro Elvillar de Álava Lanciego Navaridas Villabuena de Álava Barriobusto Labastida Lapuebla de Labarca Oyón Yécora Cripán Labraza Leza Salinillas de Buradón Elciego Laguardia Moreda de Álava Samaniego Los viñedos del municipio de Lodosa, situados en la margen derecha del Ebro, que a fecha 29 de abril de 1991 se hallasen inscritos en el Registro de viñedos del Consejo, mantendrán su inscripción en cuanto subsistan.
Cualquier modificación que se produzca en los límites de los términos municipales incluidos en la zona de producción no llevará aparejada la baja en el Registro de Viñas de los viñedos afectados que se hallen inscritos.
Dentro de la zona de producción se incluyen entidades geográficas menores identificadas como ‘viñedo singular’.

---

Result 2 | cite as [pliego_doca_rioja, Sección 8.b.9] | Pliego de condiciones de la DOCa Rioja, page 28
Pliego de condiciones de la DOCa Rioja — Sección 8.b.9. DESIGNACION, ETIQUETADO (parte 1/3)
En las etiquetas de vinos envasados figurará obligatoriamente de forma destacada el nombre de la denominación junto con la mención “Denominación de Origen Calificada” justo debajo de aquél y el sello del Consejo Regulador, además de las menciones obligatorias que se determinen en la normativa y regulación específica, así como en la legislación aplicable. Así mismo podrán figurar las menciones facultativas y unidades geográficas menores en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable, si bien no podrán destacar respecto al nombre de “RIOJA”.
Antes de la puesta en circulación de etiquetas, éstas deberán ser autorizadas por el Consejo Regulador, en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable.
En el etiquetado de los vinos protegidos por la Denominación de Origen Calificada Rioja será obligatoria la indicación de la correspondiente marca comercial.
En el etiquetado deberá figurar obligatoriamente el nombre o razón social de una bodega inscrita. También podrá utilizarse un nombre comercial, en la forma prevista en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado de la expresión “Maceración carbónica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado principal de vinos blancos y rosados de la expresión “Fermentado en barrica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable Se prohíbe la utilización de cualquier tipo de referencia o alusión a las expresiones "barrica" y "madera" en la comercialización, propaganda y etiquetado de los vinos genéricos (sin agotar procesos de crianza).
Únicamente puede aplicarse a un vino el nombre de una zona o municipio cuando el vino proceda exclusivamente de uva de tal zona de producción o municipio, y su elaboración, crianza en su caso y embotellado se realicen en los mismos.

---

Result 3 | cite as [pliego_doca_rioja, Sección 3.b.1] | Pliego de condiciones de la DOCa Rioja, page 7
Pliego de condiciones de la DOCa Rioja — Sección 3.b.1. Proporción de variedades por tipos de vino
TINTO En los vinos tintos elaborados con uva desgranada, deberá emplearse, como mínimo, un 95% de uva de las variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. En los vinos tintos elaborados con uva entera, este porcentaje será, como mínimo, del 85 %.
BLANCO En la elaboración de vinos blancos se emplearán exclusivamente uvas de las variedades Viura, Garnacha Blanca, Malvasía, Maturana blanca, Tempranillo blanco, Turruntés, Chardonnay, Sauvignon blanc y Verdejo.
ROSADO Se empleará un mínimo del 25 % de uvas de variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. La mezcla opcional para el supuesto de los vinos rosados deberá realizarse con posterioridad a la entrega o pesada en báscula.
VINO ESPUMOSO DE CALIDAD La elaboración se realizará con uvas de las variedades blancas y/o tintas definidas en el apartado 6.
En la elaboración de vinos espumosos de calidad rosados se empleará un mínimo del 25% de uvas de las variedades de uva tinta definidas en el apartado 6.

---

Result 4 | cite as [pliego_doca_rioja, Sección 6] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 6. Variedades De Uva
La elaboración de los vinos protegidos se realizará exclusivamente con uvas de las variedades siguientes:
TINTAS BLANCAS Tempranillo Garnacha tinta Graciano Mazuelo Maturana tinta Viura Sauvignon blanc Malvasía Verdejo Garnacha Blanca Maturana blanca Chardonnay Tempranillo blanco Turruntés La uva procedente de plantaciones de viñedo efectuadas con anterioridad al 1 de enero de 1956 y con variedades de uva distintas a las que figuran en el Reglamento de la Denominación, pueden ser empleadas en la elaboración de vinos protegidos, en tanto subsistan dichas plantaciones. En el caso de la variedad vinífera Calagraño, las plantaciones han de ser anteriores a 27 de octubre de 1970.

---

Result 5 | cite as [pliego_doca_rioja, Sección 4] | Pliego de condiciones de la DOCa Rioja, page 11
Pliego de condiciones de la DOCa Rioja — Sección 4. Delimitación De La Zona Geográfica (parte 1/3)
La zona de producción, crianza y envejecimiento está constituida por los terrenos ubicados en los términos municipales que se citan a continuación, que constituyen las zonas denominadas “Rioja Alta”, “Rioja Oriental” y “Rioja Alavesa”.
El Consejo Regulador determinará la ampliación de la zona geográfica a partir de informes que acrediten tanto la aptitud de los terrenos para la producción de uva de las variedades con la calidad necesaria para producir vinos de las características específicas de los protegidos por la denominación.
La calificación de los terrenos a la que se refiere el apartado e) Denominación de Origen Calificada, Términos Tradicionales, de la Disposición Adicional Tercera de la Ley 6/2015, de 12 de mayo, de Denominaciones de Origen e Indicaciones Geográficas Protegidas de ámbito territorial supraautonómico, será realizada por el Consejo Regulador.
Para las nuevas plantaciones o replantaciones en terrenos o viñedos situados en la zona de producción, así como para las modificaciones de las condiciones que puedan afectar al cumplimiento de este pliego de condiciones, será preceptivo el informe del Consejo Regulador, a efectos de su inscripción en el Registro correspondiente de la Denominación.

</details>

---

## q09 (single)

**Question:** ¿Puedo mencionar «barrica» o «madera» en la publicidad de un Rioja genérico sin crianza?

**Reference:** No. Está prohibida cualquier referencia a «barrica» y «madera» en la comercialización, propaganda y etiquetado de vinos genéricos sin procesos de crianza.

**Agent answer:**

Se prohíbe expresamente la utilización de cualquier tipo de referencia o alusión a las expresiones «barrica» y «madera» en la comercialización, propaganda y etiquetado de los vinos genéricos (sin agotar procesos de crianza) de la DOCa Rioja [pliego_doca_rioja, Sección 8.b.9].

<details><summary>search: mencionar barrica madera Rioja genérico publicidad</summary>

Result 1 | cite as [rd_1363_2011_etiquetado, Artículo 18] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 9
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 18. Menciones relativas a la fermentación o envejecimiento del vino con denominación de origen o indicación geográfica protegida, en recipientes de madera.
1. De acuerdo con el artículo 66.2 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, además de las indicaciones que figuran en el anexo XVI del citado reglamento, para indicar que el vino con denominación de origen o indicación geográfica protegidas ha sido fermentado, criado o envejecido en recipientes de madera se podrán utilizar también:
a) Los términos tradiciones «noble» y «añejo» contemplados, para España, en la base de datos electrónica E-Bacchus de la Unión Europea.
b) «Barrica» y «roble» siempre que cumplan las condiciones señaladas en el anexo III del presente real decreto.
Las indicaciones «noble», «añejo» y «roble» sólo podrán emplearse cuando el recipiente sea de madera de roble, mientras que «barrica» podrá emplearse cuando el recipiente sea de cualquier especie de madera.
2. Estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aún cuando se hayan empleado también en dichos procesos recipientes de madera de roble o de otras especies.

---

Result 2 | cite as [rd_1363_2011_etiquetado, Artículo 24] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 24. Menciones relativas al envejecimiento del vino con denominación de origen protegida en recipientes de madera.
1. De acuerdo con el artículo 66.2 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, para indicar que el vino con denominación de origen protegida ha sido criado o envejecido en barrica de madera de roble, además de las indicaciones que figuran en el anexo XVI del citado reglamento, se podrán utilizar los términos tradiciones «crianza», «reserva» y «gran reserva» contemplados, para España, en el la base de datos electrónica E-Bacchus de la Unión Europea.
2. Estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aún cuando se hayan empleado también en dichos procesos barricas de madera de roble.

---

Result 3 | cite as [pliego_doca_rioja, Sección 8.b.10.8] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.8. Términos tradicionales
Para la denominación de origen protegida “Rioja” el término tradicional al que se refiere el artículo 118 duovicies. 1a) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, Reglamento único para las OCM, es: “Denominación de Origen Calificada”.
Los términos tradicionales, a los que se refiere el artículo 118 duovicies.1b) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, que pueden utilizarse en los vinos amparados por la denominación de origen calificada “Rioja” son: “Crianza”, “Reserva”, “Gran Reserva”, “Añejo”, “Noble” y “Viejo”.

---

Result 4 | cite as [pliego_doca_rioja, Sección 8.b.9] | Pliego de condiciones de la DOCa Rioja, page 28
Pliego de condiciones de la DOCa Rioja — Sección 8.b.9. DESIGNACION, ETIQUETADO (parte 1/3)
En las etiquetas de vinos envasados figurará obligatoriamente de forma destacada el nombre de la denominación junto con la mención “Denominación de Origen Calificada” justo debajo de aquél y el sello del Consejo Regulador, además de las menciones obligatorias que se determinen en la normativa y regulación específica, así como en la legislación aplicable. Así mismo podrán figurar las menciones facultativas y unidades geográficas menores en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable, si bien no podrán destacar respecto al nombre de “RIOJA”.
Antes de la puesta en circulación de etiquetas, éstas deberán ser autorizadas por el Consejo Regulador, en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable.
En el etiquetado de los vinos protegidos por la Denominación de Origen Calificada Rioja será obligatoria la indicación de la correspondiente marca comercial.
En el etiquetado deberá figurar obligatoriamente el nombre o razón social de una bodega inscrita. También podrá utilizarse un nombre comercial, en la forma prevista en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado de la expresión “Maceración carbónica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado principal de vinos blancos y rosados de la expresión “Fermentado en barrica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable Se prohíbe la utilización de cualquier tipo de referencia o alusión a las expresiones "barrica" y "madera" en la comercialización, propaganda y etiquetado de los vinos genéricos (sin agotar procesos de crianza).
Únicamente puede aplicarse a un vino el nombre de una zona o municipio cuando el vino proceda exclusivamente de uva de tal zona de producción o municipio, y su elaboración, crianza en su caso y embotellado se realicen en los mismos.

---

Result 5 | cite as [rd_1363_2011_etiquetado, Anexo III] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 12
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Anexo III (parte 2/2)
Cuando se emplee o se haga referencia a este término, deberá indicarse en las informaciones relativas al vino en cuestión el periodo de tiempo, en meses o años, que ha permanecido en tales recipientes de madera, cuya capacidad máxima deberá ser de 600 litros. No obstante lo anterior, podrá utilizarse la indicación «Fermentado en barrica» siempre que la fermentación del vino haya tenido lugar en los recipientes citados, sin que sea preciso indicar en este caso el periodo de tiempo de permanencia. «Roble». Aplicable a los vinos con denominación de origen o indicación geográfica protegidas que hayan sido fermentados, criados o envejecidos en recipientes de madera de roble. Cuando se emplee o se haga referencia a este término, deberá indicarse en las informaciones relativas al vino en cuestión el periodo de tiempo, en meses o años, que ha permanecido en recipientes de madera de esa especie, cuya capacidad máxima deberá ser de 600 litros.

</details>

---

## q10 (single)

**Question:** ¿Cuál es el rendimiento máximo de transformación de uva en vino en Rioja?

**Reference:** 70 litros de vino por cada 100 kg de vendimia (62 litros para vinos espumosos de calidad).

**Agent answer:**

El rendimiento de transformación general no debe ser superior a 70 litros de vino por cada 100 kilogramos de vendimia [pliego_doca_rioja, Sección 3.b.3]. 
En el caso de los vinos espumosos de calidad, el rendimiento no será superior a 62 litros por cada 100 kilogramos, y para los vinos de viñedo singular no será superior a 65 litros por cada 100 kilogramos [pliego_doca_rioja, Sección 3.b.3]. 
Excepcionalmente, el Consejo Regulador puede modificar estos límites hasta un máximo de 72 litros para los vinos generales y de 64 litros para los espumosos de calidad [pliego_doca_rioja, Sección 8.b.5.1].

<details><summary>search: rendimiento máximo transformación uva vino Rioja</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 3.b.3] | Pliego de condiciones de la DOCa Rioja, page 8
Pliego de condiciones de la DOCa Rioja — Sección 3.b.3. Rendimiento de Transformación
En la producción de mosto se seguirán las prácticas tradicionales aplicadas con una moderna tecnología, orientada hacia la optimización de la calidad de los vinos. Se aplicarán presiones adecuadas para la extracción del mosto o del vino y su separación de los orujos, de forma que el rendimiento no sea superior a 70 litros de vino por cada 100 kilogramos de vendimia.
En el caso de vinos espumosos de calidad, el rendimiento de transformación no será superior a 62 litros de vino por cada 100 kilogramos de vendimia.
En el caso de los vinos procedentes de viñedo singular, el rendimiento de transformación no será superior a 65 litros de vino por cada 100 kilogramos de vendimia. Este rendimiento no podrá ser modificado en ningún caso. El exceso que se produzca por encima de dicho rendimiento se considerará no amparado por la denominación, debiendo estar identificado hasta su salida de la bodega como vino sin derecho a la Denominación de Origen Calificada Rioja o para la destilación.

---

Result 2 | cite as [pliego_doca_rioja, Sección 8.b.5.1] | Pliego de condiciones de la DOCa Rioja, page 23
Pliego de condiciones de la DOCa Rioja — Sección 8.b.5.1. Variación del rendimiento de Transformación
No obstante, lo establecido en el epígrafe 3.b.3 el límite de litros de vino amparable por cada 100 kilogramos de vendimia podrá ser modificado, excepcionalmente, por el Consejo Regulador, a iniciativa propia o a petición de los inscritos interesados, hasta un máximo de 72 litros por cada 100 kilogramos.
Del mismo modo, en función de las circunstancias de la Denominación, en determinadas campañas el Consejo Regulador podrá reducirlo hasta 66 litros por cada 100 kilogramos.
Sin perjuicio de lo anterior, el límite de litros de vino que está justificado obtener por cada 100 kilogramos de vendimia queda establecido en 74 por cada 100 kilogramos.
No obstante, lo establecido en el epígrafe 3.b.3 el límite de litros de vino espumoso de calidad amparable por cada 100 kilogramos de vendimia podrá ser modificado, excepcionalmente, por el Consejo Regulador, a iniciativa propia o a petición de los inscritos interesados, hasta un máximo de 64 litros por cada 100 kilogramos.
Sin perjuicio de lo anterior, el límite de litros de vino espumoso de calidad que está justificado obtener por cada 100 kilogramos de vendimia queda establecido en 66 por cada 100 kilogramos.

---

Result 3 | cite as [pliego_doca_rioja, Sección 5] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 5. Rendimiento Máximo
La producción máxima admitida por hectárea será de 6.500 kg de uva, equivalente a 45,5 Hl para las variedades tintas, y de 9.000 kg, equivalente a 63 Hl para las variedades blancas.
Los rendimientos de producción de uva se contabilizarán de forma separada e independiente para las variedades tintas y para las variedades blancas, sin que quepa compensación de colores.
La producción máxima admitida por hectárea en el caso de uva destinada a la elaboración de vinos con reconocimiento de la entidad geográfica menor ‘viñedo singular’, será de 5.000 kg de uva, equivalente a 32,50 Hl para las variedades tintas, y de 6.922 kg, equivalente a 44,99 Hl para las variedades blancas. Este rendimiento no podrá ser modificado en ningún caso.

---

Result 4 | cite as [pliego_doca_rioja, Sección 8.b.6.1] | Pliego de condiciones de la DOCa Rioja, page 25
Pliego de condiciones de la DOCa Rioja — Sección 8.b.6.1. Variación del rendimiento amparable
No obstante, lo establecido en el epígrafe 5, la producción máxima admitida por hectárea podrá ser modificada anualmente por el Consejo Regulador, sin que pueda superar, al alza, 8.125 kg por hectárea para las variedades tintas y 11.250 kg por hectárea para las variedades blancas. Del mismo modo, en función de las circunstancias de la Campaña, el Consejo Regulador podrá reducir la producción máxima admitida por hectárea hasta 5.525 kg por hectárea para las variedades tintas y 7.650 kg por hectárea para las variedades blancas.
El control de la producción se efectuará de conformidad con lo previsto en las Normas de Campaña.

---

Result 5 | cite as [pliego_doca_rioja, Sección 8.b.6.4] | Pliego de condiciones de la DOCa Rioja, page 26
Pliego de condiciones de la DOCa Rioja — Sección 8.b.6.4. Precisiones en materia de rendimientos
Cuando las uvas procedan de vendimia mecánica el peso se incrementará en un 3% y en los traslados de uva despalillada el peso se incrementará en un 5%.
No será de aplicación para los viñedos incluidos en una entidad de ‘viñedo singular’.

</details>

---

## q11 (single)

**Question:** Si pongo un solo nombre de variedad en la etiqueta, ¿qué porcentaje mínimo del vino debe ser de esa variedad?

**Reference:** Al menos el 85 % del producto debe haberse elaborado con esa variedad.

**Agent answer:**

Si se menciona el nombre de una sola variedad de uva de vinificación en la etiqueta, al menos el 85 % del producto deberá haber sido elaborado a partir de dicha variedad [reg_ue_2019_33, Artículo 50].

<details><summary>search: variedad etiqueta porcentaje mínimo vino</summary>

Result 1 | cite as [rd_1363_2011_etiquetado, Artículo 13] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 8
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 13. Definición de vinos varietales.
1. A los efectos de este real decreto, se consideran vinos varietales los producidos de conformidad con el artículo 118 septvicies, apartado 2, del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007; con los artículos 61, 62 y 63 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009; y con la normativa nacional de desarrollo.
2. En aplicación del artículo 63.7 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, estos vinos podrán emplear los términos «vino varietal» completado con el nombre «España» y el nombre o nombres de la variedad o variedades de uva de vinificación que se hayan empleado en su elaboración.

---

Result 2 | cite as [rd_1363_2011_etiquetado, Artículo 21] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 21. Términos tradicionales.
1. En aplicación del artículo 70.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, los términos tradicionales a los que se refiere la letra a) del apartado 1 del artículo 118 duovicies del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007, que, para España, se incluyen en la base de datos electrónica E-Bacchus de la Unión Europea, se indicarán en las etiquetas con caracteres cuyas dimensiones no superen a los que indiquen el nombre geográfico.
2. Igualmente, los términos tradicionales: «crianza», «reserva», y «gran reserva» se indicarán en caracteres de tamaño igual o inferior al de los utilizados en el nombre geográfico.

---

Result 3 | cite as [rd_1363_2011_etiquetado, Artículo 14] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 8
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 14. Procedimiento de control de la veracidad de las indicaciones de la variedad de uva de vinificación o la añada en los vinos varietales.
1. En cumplimiento del artículo 118 septvicies, apartado 2, letra a), del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007, se establece que los vinos varietales deberán someterse a un procedimiento de certificación, aprobación y control, que cada comunidad autónoma deberá regular y poner en aplicación para los producidos en su territorio.
2. Los procedimientos de certificación, aprobación y control deberán cumplir las normas específicas contempladas en el artículo 63 del Reglamento (CE) n.º 607/2009, de la Comisión, de 14 de julio de 2009, incluyendo:
a) La designación de la autoridad o autoridades competentes.
b) Garantizar la certificación del vino en cualquier fase de la producción, incluso durante el envasado del mismo, por la autoridad competente o, en su caso, por uno o varios organismos de control.
c) La determinación del método de control seleccionado, que podrá ser aleatorio, por muestreo o sistemático.
d) Los requisitos de autorización de los productores.
3. En aplicación del segundo párrafo del artículo 63.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, las comunidades autónomas podrán decidir que el procedimiento de certificación incluya la realización de exámenes organolépticos o analíticos.

---

Result 4 | cite as [rd_1363_2011_etiquetado, Anexo III] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 12
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Anexo III (parte 1/2)
Condiciones de utilización de menciones relativas al modo de obtención o a los métodos de elaboración de vinos con denominación de origen o indicación geográfica protegidas (artículo 17) «Maceración carbónica». Aplicable a los vinos en cuyo proceso de fermentación se ha seguido dicho método. «Pale dry». Aplicable a aquellos vinos de licor con denominación de origen protegida cuyo contenido en azúcares sea inferior a 50 g/l y que cumplan los requisitos establecidos en sus respectivos pliegos de condiciones. «Pale Cream». Aplicable a los vinos de licor con denominación de origen protegida con un contenido en azucares inferior a 115 gr/l y que cumplan los requisitos establecidos en sus respectivos pliegos de condiciones. «Mistela». Aplicable a los vinos de licor con denominación de origen protegida a los que se refiere el punto 3.c).4.º guión del anexo XI ter del Reglamento (CE) n.º 1234/2007, de 22 de octubre de 2007. «Naturalmente dulce». Aplicable a los vinos con denominación de origen protegida elaborados sin aumento artificial de su graduación y con el alcohol procedente en su totalidad de la fermentación, con un grado alcohólico volumétrico natural superior a 15% vol. y un grado alcohólico volumétrico adquirido no inferior a 13% vol. Y también a los vinos con indicación geográfica protegida de uva sobremadurada. «Vendimia tardía». Aplicable a los vinos con denominación de origen o indicación geográfica protegidas de uva sobremadurada. «Vendimia seleccionada». Aplicable a los vinos con denominación de origen o indicación geográfica protegidas, para los que la elección de la uva utilizada en su elaboración se ha realizado siguiendo criterios o normas especiales. «Barrica». Aplicable a los vinos con denominación de origen o indicación geográfica protegidas que hayan sido fermentados, criados o envejecidos en recipientes de madera.

---

Result 5 | cite as [pliego_doca_rioja, Sección 3.b.1] | Pliego de condiciones de la DOCa Rioja, page 7
Pliego de condiciones de la DOCa Rioja — Sección 3.b.1. Proporción de variedades por tipos de vino
TINTO En los vinos tintos elaborados con uva desgranada, deberá emplearse, como mínimo, un 95% de uva de las variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. En los vinos tintos elaborados con uva entera, este porcentaje será, como mínimo, del 85 %.
BLANCO En la elaboración de vinos blancos se emplearán exclusivamente uvas de las variedades Viura, Garnacha Blanca, Malvasía, Maturana blanca, Tempranillo blanco, Turruntés, Chardonnay, Sauvignon blanc y Verdejo.
ROSADO Se empleará un mínimo del 25 % de uvas de variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. La mezcla opcional para el supuesto de los vinos rosados deberá realizarse con posterioridad a la entrega o pesada en báscula.
VINO ESPUMOSO DE CALIDAD La elaboración se realizará con uvas de las variedades blancas y/o tintas definidas en el apartado 6.
En la elaboración de vinos espumosos de calidad rosados se empleará un mínimo del 25% de uvas de las variedades de uva tinta definidas en el apartado 6.

</details>

<details><summary>search: Reglamento 607 2009 porcentaje variedad etiqueta</summary>

Result 1 | cite as [rd_1363_2011_etiquetado, Artículo 13] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 8
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 13. Definición de vinos varietales.
1. A los efectos de este real decreto, se consideran vinos varietales los producidos de conformidad con el artículo 118 septvicies, apartado 2, del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007; con los artículos 61, 62 y 63 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009; y con la normativa nacional de desarrollo.
2. En aplicación del artículo 63.7 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, estos vinos podrán emplear los términos «vino varietal» completado con el nombre «España» y el nombre o nombres de la variedad o variedades de uva de vinificación que se hayan empleado en su elaboración.

---

Result 2 | cite as [rd_1363_2011_etiquetado, Preámbulo] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 4
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Preámbulo (parte 2/3)
Principalmente, el presente real decreto desarrolla la regulación comunitaria en materia de etiquetado y presentación de determinados productos vitivinícolas, que está contenida, además de en la organización común de mercados agrícolas, en el Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, por el que se establecen determinadas disposiciones de aplicación del Reglamento (CE) n.º 479/2008 del Consejo en lo que atañe a las denominaciones de origen e indicaciones geográficas protegidas, a los términos tradicionales, al etiquetado y a la presentación de determinados productos vitivinícolas, incluyendo la adaptación de las normas sobre el empleo de códigos y la precisión de ciertos requisitos que han de cumplir los vinos sin denominación de origen protegida o indicación geográfica protegida y los operadores que los elaboran, para poder indicar la variedad de uva de vinificación o el año de cosecha. También se desarrolla algún aspecto sobre la identificación del contenido de los recipientes para el almacenamiento de determinados productos vitivinícolas, teniendo como base el Reglamento (CE) n.º 436/2009 de la Comisión, de 26 de mayo de 2009, por el que se establecen disposiciones de aplicación del Reglamento (CE) n.º 479/2008 del Consejo, en lo que respecta al registro vitícola, a las declaraciones obligatorias y a la recopilación de información para el seguimiento del mercado, a los documentos que acompañan al transporte de productos y a los registros que se han de llevar en el sector vitivinícola.
En aplicación de lo dispuesto en el artículo 118 septvicies, apartado 2, letra b), del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007, se plantea la posibilidad de exclusión de determinadas variedades en el etiquetado de los vinos sin denominación de origen o indicación geográfica protegidas. Por el momento dicha opción se aplica exclusivamente a la variedad de vid Albariño.
También, el presente real decreto reconoce la capacidad de las administraciones competentes para establecer menciones de etiquetado de los tipos que se regulan, y definir sus condiciones de empleo.

---

Result 3 | cite as [rd_1363_2011_etiquetado, Artículo 14] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 8
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 14. Procedimiento de control de la veracidad de las indicaciones de la variedad de uva de vinificación o la añada en los vinos varietales.
1. En cumplimiento del artículo 118 septvicies, apartado 2, letra a), del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007, se establece que los vinos varietales deberán someterse a un procedimiento de certificación, aprobación y control, que cada comunidad autónoma deberá regular y poner en aplicación para los producidos en su territorio.
2. Los procedimientos de certificación, aprobación y control deberán cumplir las normas específicas contempladas en el artículo 63 del Reglamento (CE) n.º 607/2009, de la Comisión, de 14 de julio de 2009, incluyendo:
a) La designación de la autoridad o autoridades competentes.
b) Garantizar la certificación del vino en cualquier fase de la producción, incluso durante el envasado del mismo, por la autoridad competente o, en su caso, por uno o varios organismos de control.
c) La determinación del método de control seleccionado, que podrá ser aleatorio, por muestreo o sistemático.
d) Los requisitos de autorización de los productores.
3. En aplicación del segundo párrafo del artículo 63.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, las comunidades autónomas podrán decidir que el procedimiento de certificación incluya la realización de exámenes organolépticos o analíticos.

---

Result 4 | cite as [reg_ue_2019_33, Artículo 51] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 20
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 51. Normas específicas para la indicación de variedades de uva de
vinificación en productos vitivinícolas que no estén acogidos a una denominación de origen o indicación geográfica protegida En lo que se refiere a los productos vitivinícolas contemplados en el anexo VII, parte II, puntos 1 a 9 y 16, del Reglamento (UE) n.o 1308/2013 que no estén acogidos a una denominación de origen protegida o indicación geográfica protegida y siempre que se cumplan las condiciones establecidas en el artículo 120, apartado 2, de dicho Reglamento, los Estados miembros podrán decidir emplear los términos «vino varietal», completados con la información siguiente:
a) nombre del Estado miembro o Estados miembros de que se trate, y/o
b) nombre de la variedad o variedades de uva de vinificación.
En el caso de los productos vitivinícolas a que se refiere el párrafo primero que no estén acogidos a una denominación de origen protegida ni a una indicación geográfica protegida o no lleven una indicación geográfica de un tercer país con el nombre de una o más variedades de uva de vinificación en sus etiquetas, los terceros países podrán decidir emplear los términos «vino varietal» completado con el nombre o los nombres del tercer país o terceros países de que se trate.
El artículo 45 del presente Reglamento no será de aplicación en lo que respecta a la indicación del nombre o nombres del Estado miembro o Estados miembros o el tercer país o terceros países.

---

Result 5 | cite as [rd_1363_2011_etiquetado, Artículo 23] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 23. Indicación obligatoria del año de la cosecha junto con términos tradicionales de envejecimiento.
En aplicación del artículo 70.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, será obligatoria la indicación del año de la cosecha en el etiquetado de los vinos incluidos en la categoría 1 del anexo XI ter del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007, con denominación de origen protegida, acompañando a los términos tradicionales «crianza», «reserva» o «gran reserva».

</details>

<details><summary>search: Reglamento Delegado UE 2019 33 porcentaje variedad etiqueta</summary>

Result 1 | cite as [reg_ue_2019_33, Artículo 51] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 20
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 51. Normas específicas para la indicación de variedades de uva de
vinificación en productos vitivinícolas que no estén acogidos a una denominación de origen o indicación geográfica protegida En lo que se refiere a los productos vitivinícolas contemplados en el anexo VII, parte II, puntos 1 a 9 y 16, del Reglamento (UE) n.o 1308/2013 que no estén acogidos a una denominación de origen protegida o indicación geográfica protegida y siempre que se cumplan las condiciones establecidas en el artículo 120, apartado 2, de dicho Reglamento, los Estados miembros podrán decidir emplear los términos «vino varietal», completados con la información siguiente:
a) nombre del Estado miembro o Estados miembros de que se trate, y/o
b) nombre de la variedad o variedades de uva de vinificación.
En el caso de los productos vitivinícolas a que se refiere el párrafo primero que no estén acogidos a una denominación de origen protegida ni a una indicación geográfica protegida o no lleven una indicación geográfica de un tercer país con el nombre de una o más variedades de uva de vinificación en sus etiquetas, los terceros países podrán decidir emplear los términos «vino varietal» completado con el nombre o los nombres del tercer país o terceros países de que se trate.
El artículo 45 del presente Reglamento no será de aplicación en lo que respecta a la indicación del nombre o nombres del Estado miembro o Estados miembros o el tercer país o terceros países.

---

Result 2 | cite as [reg_ue_2019_33, Artículo 50] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 18
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 50. Nombre de la variedad de uva de vinificación (parte 1/3)
1. Los nombres de las variedades de uva de vinificación o sus sinónimos a que hace referencia el artículo 120, apartado 1, letra b), del Reglamento (UE) n.o 1308/2013, utilizados para la producción de los productos vitivinícolas contemplados en el anexo VII, parte II, puntos 1 a 11, 13, 15 y 16, del Reglamento (UE) n.o 1308/2013, podrán figurar en la etiqueta de dichos productos en las condiciones establecidas en las letras a) y b), en caso de que se produzcan en la Unión, o en las condiciones previstas en las letras a) y c), en caso de que se produzcan en terceros países.
a) Los nombres de las variedades de uva de vinificación o sus sinónimos podrán indicarse de acuerdo con las siguientes condiciones:
i) si se menciona el nombre de una sola variedad de uva de vinificación o su sinónimo, al menos el 85 % del producto deberá haber sido elaborado a partir de dicha variedad, excluyendo: (5) Reglamento de Ejecución (UE) 2018/274 de la Comisión, de 11 de diciembre de 2017, por el que se establecen las normas de desarrollo del Reglamento (UE) n.o 1308/2013 del Parlamento Europeo y del Consejo en lo que respecta al régimen de autorizaciones para plantaciones de vid, la certificación, el registro de entradas y salidas, las declaraciones obligatorias y las notificaciones, y del Reglamento (UE) n.o 1306/2013 del Parlamento Europeo y del Consejo en lo que respecta a los controles pertinentes, y por el que se deroga el Reglamento de Ejecución (UE) 2015/561 de la Comisión (DO L 58 de 28.2.2018, pp. 1-59).
— cualquier cantidad de productos vitivinícolas utilizados en la edulcoración, de «licor de expedición» o de «licor de tiraje», o
— cualquier cantidad de productos vitivinícolas a que se hace referencia en el anexo VII, parte II, punto 3, letras e) y f), del Reglamento (UE) n.o 1308/2013,
ii) si se menciona el nombre de dos o más variedades de uva de vinificación o sus sinónimos, el 100 % de los productos en cuestión deberá haber sido elaborado a partir de dichas variedades, excluyendo:
— cualquier cantidad de productos vitivinícolas utilizados en la edulcoración, de «licor de expedición» o de «licor de tiraje», o

---

Result 3 | cite as [reg_ue_2019_33, Artículo 50] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 18
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 50. Nombre de la variedad de uva de vinificación (parte 2/3)
— cualquier cantidad de productos vitivinícolas a que se hace referencia en el anexo VII, parte II, punto 3, letras e) y f), del Reglamento (UE) n.o 1308/2013.
Las variedades de uva de vinificación deberán aparecer en la etiqueta en orden descendente en función de la proporción utilizada y en caracteres del mismo tamaño.
b) En el caso de los productos vitivinícolas producidos en la Unión, los nombres de las variedades de uva de vinificación o sus sinónimos serán aquellos que se especifican en la clasificación de variedades de uva de vinificación a que se hace referencia en el artículo 81, apartado 2, del Reglamento (UE) n.o 1308/2013.
En el caso de los Estados miembros exentos de la obligación de clasificación prevista en el artículo 81, apartado 3, del Reglamento (UE) n.o 1308/2013, los nombres de las variedades de uva de vinificación o sus sinónimos serán los que figuran en la «Lista internacional de variedades de vid y sus sinónimos» gestionada por la Organización Internacional de la Viña y el Vino.
c) En el caso de los productos vitivinícolas originarios de terceros países, las condiciones de utilización de los nombres de las variedades de uva de vinificación o sus sinónimos cumplirán las normas aplicables a los productores de vino en el tercer país de que se trate, incluidas las que emanen de organizaciones profesionales representativas, y los nombres de las variedades de uva de vinificación o sus sinónimos serán los que figuren en la lista de al menos una de las siguientes organizaciones:
i) Organización Internacional de la Viña y el Vino,
ii) Unión Internacional para la Protección de las Obtenciones Vegetales,
iii) Consejo Internacional sobre Recursos Fitogenéticos.
2. A los efectos del apartado 1, el producto vitivinícola que no esté acogido a una denominación de origen o una indicación geográfica protegida, pero sí lleve una indicación del nombre de la variedad de uva de vinificación en la etiqueta, se certificará de conformidad con el artículo 12 del Reglamento de Ejecución (UE) 2018/274.

---

Result 4 | cite as [reg_ue_2019_33, Artículo 49] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 18
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 49. Año de cosecha
1. El año de cosecha, al que se hace referencia en el artículo 120, apartado 1, letra a), del Reglamento (UE) n.o 1308/2013, podrá aparecer en las etiquetas de los productos vitivinícolas contemplados en el anexo VII, parte II, puntos 1 a 11, 13, 15 y 16, del Reglamento (UE) n.o 1308/2013, a condición de que al menos el 85 % de las uvas utilizadas para elaborar esos productos haya sido cosechado el año en cuestión. Quedan excluidas:
a) cualquier cantidad de productos vitivinícolas utilizados en la edulcoración, de «licor de expedición» o de «licor de tiraje», o
b) cualquier cantidad de productos vitivinícolas a los que se hace referencia en el anexo VII, parte II, punto 3, letras e) y f), del Reglamento (UE) n.o 1308/2013.
2. A los efectos del apartado 1, los productos vitivinícolas que no estén acogidos a una denominación de origen o una indicación geográfica protegida, pero sí lleven una indicación del año de la cosecha en la etiqueta, se certificarán de conformidad con el artículo 12 del Reglamento de Ejecución (UE) 2018/274 de la Comisión (5).
3. En el caso de los productos obtenidos tradicionalmente a partir de uvas cosechadas en enero o febrero, el año de cosecha que deberá aparecer en la etiqueta de los productos vitivinícolas será el del año civil anterior.

---

Result 5 | cite as [reg_ue_2019_33, Artículo 1] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 2
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 1. Objeto
El presente Reglamento establece normas que completan el Reglamento (UE) n.o 1308/2013 en lo que se refiere a los siguientes aspectos:
a) en lo que respecta a las denominaciones de origen protegidas y las indicaciones geográficas protegidas en el sector vitivinícola:
i) el nombre que debe protegerse;
ii) los requisitos adicionales aplicables a los pliegos de condiciones;
iii) las excepciones relativas a la producción en la zona geográfica delimitada;
iv) las excepciones a la obligación de utilizar “indicaciones” en las etiquetas;
b) en lo que respecta a los términos tradicionales en el sector vitivinícola:
i) las solicitudes de protección;
ii) el procedimiento de oposición;
iii) las modificaciones;
iv) la cancelación;
c) en lo que respecta al sector vitivinícola en general: el etiquetado y la presentación.
DENOMINACIONES DE ORIGEN E INDICACIONES GEOGRÁFICAS PROTEGIDAS Solicitudes de protección

</details>

---

## q12 (single)

**Question:** Para indicar el año de cosecha en la etiqueta, ¿qué parte de la uva debe ser de ese año?

**Reference:** Al menos el 85 % de las uvas utilizadas deben haberse cosechado en ese año.

**Agent answer:**

Para poder indicar el año de cosecha en la etiqueta, al menos el 85 % de las uvas utilizadas para elaborar el producto debe haber sido cosechado en ese año [reg_ue_2019_33, Artículo 49].

<details><summary>search: </summary>

Error executing tool search: 1 validation error for searchArguments
query
  Field required [type=missing, input_value={'queries': ['año de cos...entaje uva reglamento']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.14/v/missing

</details>

<details><summary>search: año de cosecha etiqueta porcentaje uva</summary>

Result 1 | cite as [reg_ue_2019_33, Artículo 49] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 18
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 49. Año de cosecha
1. El año de cosecha, al que se hace referencia en el artículo 120, apartado 1, letra a), del Reglamento (UE) n.o 1308/2013, podrá aparecer en las etiquetas de los productos vitivinícolas contemplados en el anexo VII, parte II, puntos 1 a 11, 13, 15 y 16, del Reglamento (UE) n.o 1308/2013, a condición de que al menos el 85 % de las uvas utilizadas para elaborar esos productos haya sido cosechado el año en cuestión. Quedan excluidas:
a) cualquier cantidad de productos vitivinícolas utilizados en la edulcoración, de «licor de expedición» o de «licor de tiraje», o
b) cualquier cantidad de productos vitivinícolas a los que se hace referencia en el anexo VII, parte II, punto 3, letras e) y f), del Reglamento (UE) n.o 1308/2013.
2. A los efectos del apartado 1, los productos vitivinícolas que no estén acogidos a una denominación de origen o una indicación geográfica protegida, pero sí lleven una indicación del año de la cosecha en la etiqueta, se certificarán de conformidad con el artículo 12 del Reglamento de Ejecución (UE) 2018/274 de la Comisión (5).
3. En el caso de los productos obtenidos tradicionalmente a partir de uvas cosechadas en enero o febrero, el año de cosecha que deberá aparecer en la etiqueta de los productos vitivinícolas será el del año civil anterior.

---

Result 2 | cite as [rd_1363_2011_etiquetado, Artículo 23] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 23. Indicación obligatoria del año de la cosecha junto con términos tradicionales de envejecimiento.
En aplicación del artículo 70.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, será obligatoria la indicación del año de la cosecha en el etiquetado de los vinos incluidos en la categoría 1 del anexo XI ter del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007, con denominación de origen protegida, acompañando a los términos tradicionales «crianza», «reserva» o «gran reserva».

---

Result 3 | cite as [rd_1363_2011_etiquetado, Anexo III] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 12
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Anexo III (parte 1/2)
Condiciones de utilización de menciones relativas al modo de obtención o a los métodos de elaboración de vinos con denominación de origen o indicación geográfica protegidas (artículo 17) «Maceración carbónica». Aplicable a los vinos en cuyo proceso de fermentación se ha seguido dicho método. «Pale dry». Aplicable a aquellos vinos de licor con denominación de origen protegida cuyo contenido en azúcares sea inferior a 50 g/l y que cumplan los requisitos establecidos en sus respectivos pliegos de condiciones. «Pale Cream». Aplicable a los vinos de licor con denominación de origen protegida con un contenido en azucares inferior a 115 gr/l y que cumplan los requisitos establecidos en sus respectivos pliegos de condiciones. «Mistela». Aplicable a los vinos de licor con denominación de origen protegida a los que se refiere el punto 3.c).4.º guión del anexo XI ter del Reglamento (CE) n.º 1234/2007, de 22 de octubre de 2007. «Naturalmente dulce». Aplicable a los vinos con denominación de origen protegida elaborados sin aumento artificial de su graduación y con el alcohol procedente en su totalidad de la fermentación, con un grado alcohólico volumétrico natural superior a 15% vol. y un grado alcohólico volumétrico adquirido no inferior a 13% vol. Y también a los vinos con indicación geográfica protegida de uva sobremadurada. «Vendimia tardía». Aplicable a los vinos con denominación de origen o indicación geográfica protegidas de uva sobremadurada. «Vendimia seleccionada». Aplicable a los vinos con denominación de origen o indicación geográfica protegidas, para los que la elección de la uva utilizada en su elaboración se ha realizado siguiendo criterios o normas especiales. «Barrica». Aplicable a los vinos con denominación de origen o indicación geográfica protegidas que hayan sido fermentados, criados o envejecidos en recipientes de madera.

---

Result 4 | cite as [rd_1363_2011_etiquetado, Artículo 21] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 21. Términos tradicionales.
1. En aplicación del artículo 70.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, los términos tradicionales a los que se refiere la letra a) del apartado 1 del artículo 118 duovicies del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007, que, para España, se incluyen en la base de datos electrónica E-Bacchus de la Unión Europea, se indicarán en las etiquetas con caracteres cuyas dimensiones no superen a los que indiquen el nombre geográfico.
2. Igualmente, los términos tradicionales: «crianza», «reserva», y «gran reserva» se indicarán en caracteres de tamaño igual o inferior al de los utilizados en el nombre geográfico.

---

Result 5 | cite as [rd_1363_2011_etiquetado, Artículo 13] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 8
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 13. Definición de vinos varietales.
1. A los efectos de este real decreto, se consideran vinos varietales los producidos de conformidad con el artículo 118 septvicies, apartado 2, del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007; con los artículos 61, 62 y 63 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009; y con la normativa nacional de desarrollo.
2. En aplicación del artículo 63.7 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, estos vinos podrán emplear los términos «vino varietal» completado con el nombre «España» y el nombre o nombres de la variedad o variedades de uva de vinificación que se hayan empleado en su elaboración.

</details>

---

## q13 (single)

**Question:** ¿Qué tamaño mínimo deben tener los caracteres de las indicaciones obligatorias de la etiqueta?

**Reference:** 1,2 mm o más, independientemente del formato de caracteres.

**Agent answer:**

El tamaño de los caracteres de las indicaciones obligatorias debe ser igual o superior a 1,2 mm, independientemente del formato de caracteres utilizado [reg_ue_2019_33, Artículo 40].

<details><summary>search: tamaño minimo caracteres indicaciones obligatorias etiqueta vino</summary>

Result 1 | cite as [rd_1363_2011_etiquetado, Artículo 21] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 21. Términos tradicionales.
1. En aplicación del artículo 70.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, los términos tradicionales a los que se refiere la letra a) del apartado 1 del artículo 118 duovicies del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007, que, para España, se incluyen en la base de datos electrónica E-Bacchus de la Unión Europea, se indicarán en las etiquetas con caracteres cuyas dimensiones no superen a los que indiquen el nombre geográfico.
2. Igualmente, los términos tradicionales: «crianza», «reserva», y «gran reserva» se indicarán en caracteres de tamaño igual o inferior al de los utilizados en el nombre geográfico.

---

Result 2 | cite as [rd_1363_2011_etiquetado, Artículo 6] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 6
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 6. Uso facultativo de códigos en el etiquetado.
1. De acuerdo con lo dispuesto en el artículo 56.5 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, la indicación del nombre y la dirección del embotellador, o la del productor o vendedor, o la del importador podrá ser sustituida en el etiquetado por un código.
Como código se utilizará el número de Registro de Envasadores de Vinos.
2. En aquellos casos en los que el producto en cuestión o en los que el operador económico citado en el primer párrafo, no sean objeto de inscripción en el Registro de Envasadores de Vinos, como código se utilizará el Código de Identificación Fiscal (CIF).

---

Result 3 | cite as [rd_1363_2011_etiquetado, Artículo 16] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 9
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 16. Ubicación de los nombres geográficos en el etiquetado.
En el etiquetado de los vinos con denominación de origen o con indicación geográfica protegidas deberá figurar inmediatamente próximo de dichas indicaciones o del término tradicional que las sustituya (de acuerdo con lo dispuesto en el artículo 118 sexvicies apartado 3, letra a, del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007), el nombre geográfico correspondiente.

---

Result 4 | cite as [rd_1363_2011_etiquetado, Artículo 2] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 5
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 2. Ámbito de aplicación.
1. Las disposiciones contenidas en el presente real decreto son aplicables a los productos del sector vitivinícola que se indican a continuación, producidos en España, amparados o no por una denominación de origen o indicación geográfica protegidas: vino, vino nuevo en proceso de fermentación, vino de licor, vino espumoso, vino espumoso de calidad, vino espumoso aromático de calidad, vino espumoso gasificado, vino de aguja, vino de aguja gasificado, mosto de uva, mosto de uva parcialmente fermentado, mosto de uva concentrado, vino de uvas pasificadas y vino de uvas sobremaduradas.
2. Los artículos 3 a 10, ambos inclusive, son de aplicación a los productos del sector vitivinícola indicados en el apartado 1 que, procedentes de otros países, se embotellen en España.
3. Por otra parte, en el marco del Reglamento (CE) n.º 436/2009 de la Comisión, de 26 de mayo de 2009, el artículo 11 es de aplicación a los productos del sector vitivinícola que se almacenen, a granel, en España.

---

Result 5 | cite as [rd_1363_2011_etiquetado, Artículo 3] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 5
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 3. Obligación de etiquetar.
1. En aplicación del artículo 70.4 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, los vinos embotellados en España deberán ir etiquetados.
2. Quedan exceptuados de dicha obligación:
a) Los vinos transportados entre dos o más instalaciones de una misma empresa.
b) El vino no destinado a la venta, hasta un máximo de 30 litros por partida.
c) El vino destinado al consumo familiar del productor y de sus empleados.
d) Las botellas de vinos espumosos con denominación de origen protegida elaborados según el «método tradicional» que, cumpliendo lo establecido para esta mención en el artículo 66.4 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, satisfagan, además, los siguientes requisitos: 1.º) Que las botellas circulen dentro de la zona de producción de la denominación de origen protegida de que se trate y entre bodegas con derecho a la misma. 2.º) Que las botellas se encuentren en fase de elaboración cerradas con tapón de tiraje en el que se identifique el lote de procedencia y la bodega que efectuó su tiraje y fermentación. 3.º) Que vayan provistos de un documento de acompañamiento. 4.º) Que sean objeto de controles específicos.

</details>

<details><summary>search: reglamento 2019 33 tamaño caracteres indicaciones obligatorias etiqueta vino</summary>

Result 1 | cite as [reg_ue_2019_33, Artículo 1] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 2
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 1. Objeto
El presente Reglamento establece normas que completan el Reglamento (UE) n.o 1308/2013 en lo que se refiere a los siguientes aspectos:
a) en lo que respecta a las denominaciones de origen protegidas y las indicaciones geográficas protegidas en el sector vitivinícola:
i) el nombre que debe protegerse;
ii) los requisitos adicionales aplicables a los pliegos de condiciones;
iii) las excepciones relativas a la producción en la zona geográfica delimitada;
iv) las excepciones a la obligación de utilizar “indicaciones” en las etiquetas;
b) en lo que respecta a los términos tradicionales en el sector vitivinícola:
i) las solicitudes de protección;
ii) el procedimiento de oposición;
iii) las modificaciones;
iv) la cancelación;
c) en lo que respecta al sector vitivinícola en general: el etiquetado y la presentación.
DENOMINACIONES DE ORIGEN E INDICACIONES GEOGRÁFICAS PROTEGIDAS Solicitudes de protección

---

Result 2 | cite as [reg_ue_2019_33, Artículo 40] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 11
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 40. Presentación de las indicaciones obligatorias
1. Las indicaciones obligatorias mencionadas en el artículo 119 del Reglamento (UE) n.o 1308/2013 deberán aparecer en el mismo campo visual del envase, de tal manera que sean simultáneamente legibles sin tener que girar el envase, en caracteres indelebles y se distinguirán claramente del texto o dibujos adyacentes.
2. No obstante lo dispuesto en el apartado 1, las siguientes indicaciones obligatorias podrán figurar fuera del campo visual mencionado en dicho apartado:
a) las sustancias o productos que causan alergias o intolerancias, contemplados en el artículo 9, apartado 1, letra c), del Reglamento (UE) n.o 1169/2011, cuando la lista de ingredientes se facilite por medios electrónicos;
b) la mención del importador;
c) el número de lote, y
d) la fecha de durabilidad mínima.
3. El tamaño de los caracteres de las indicaciones a que se hace referencia en el apartado 1 del presente artículo y en el artículo 41, apartado 1, deberá ser igual o superior a 1,2 mm, independientemente del formato de caracteres utilizado.

---

Result 3 | cite as [reg_ue_2019_33, Encabezado] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 1
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Encabezado
Este texto es exclusivamente un instrumento de documentación y no surte efecto jurídico. Las instituciones de la UE no asumen responsabilidad alguna por su contenido. Las versiones auténticas de los actos pertinentes, incluidos sus preámbulos, son las publicadas en el Diario Oficial de la Unión Europea, que pueden consultarse a través de EUR-Lex. Los textos oficiales son accesibles directamente mediante los enlaces integrados en este documento REGLAMENTO DELEGADO DE LA COMISIÓN (UE) 2019/33, de 17 de octubre de 2018, por el que se completa el Reglamento (UE) n.o 1308/2013 del Parlamento Europeo y del Consejo en lo que respecta a las solicitudes de protección y al etiquetado de denominaciones de origen e indicaciones geográficas, a las solicitudes de protección, al procedimiento de oposición, a la modificación y la cancelación de términos tradicionales y al etiquetado y la presentación en el sector vitivinícola (DO L 9 de 11.1.2019, p. 2) Modificado por:
Diario Oficial no página fecha Reglamento Delegado (UE) 2021/1375 de la Comisión de 11 de junio de 2021 L 297 16 20.8.2021 Reglamento Delegado (UE) 2023/1606 de la Comisión de 30 de mayo de 2023 L 198 6 8.8.2023 Reglamento Delegado (UE) 2025/28 de la Comisión de 30 de octubre de 2024 L 28 1 15.1.2025 Rectificado por:
Rectificación, DO L 269 de 23.10.2019, p. 14 (2019/33) Rectificación, DO L 90170 de 11.3.2024, p. 1 (2023/1606) REGLAMENTO DELEGADO DE LA COMISIÓN (UE) 2019/33, de 17 de octubre de 2018, por el que se completa el Reglamento (UE) n.o 1308/2013 del Parlamento Europeo y del Consejo en lo que respecta a las solicitudes de protección y al etiquetado de denominaciones de origen e indicaciones geográficas, a las solicitudes de protección, al procedimiento de oposición, a la modificación y la cancelación de términos tradicionales y al etiquetado y la presentación en el sector vitivinícola DISPOSICIÓN PRELIMINAR

---

Result 4 | cite as [reg_ue_2019_33, Artículo 23] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 4
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 23. Excepciones a la obligación de utilizar la expresión «denominación
de origen protegida» en las etiquetas De conformidad con el artículo 119, apartado 3, del Reglamento (UE) n.o 1308/2013, las referencias a los términos «denominación de origen protegida» podrán omitirse en los vinos acogidos a las siguientes denominaciones de origen:
a) Grecia:
Σάμος (Samos);
b) España:
Cava, Jerez, Xérès o Sherry, Manzanilla;
c) Francia:
Champagne;
d) Italia:
Asti, Marsala, Franciacorta;
e) Chipre:
Κουμανδαρία (Commandaria);
f) Portugal:
Madeira o Madère, Port o Porto.
TÉRMINOS TRADICIONALES Solicitudes de protección y procedimiento de examen

---

Result 5 | cite as [rd_1363_2011_etiquetado, Artículo 21] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 21. Términos tradicionales.
1. En aplicación del artículo 70.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, los términos tradicionales a los que se refiere la letra a) del apartado 1 del artículo 118 duovicies del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007, que, para España, se incluyen en la base de datos electrónica E-Bacchus de la Unión Europea, se indicarán en las etiquetas con caracteres cuyas dimensiones no superen a los que indiquen el nombre geográfico.
2. Igualmente, los términos tradicionales: «crianza», «reserva», y «gran reserva» se indicarán en caracteres de tamaño igual o inferior al de los utilizados en el nombre geográfico.

</details>

---

## q14 (single)

**Question:** ¿Cuánto puede diferir el grado alcohólico de la etiqueta del que da el análisis?

**Reference:** No más de 0,5 % vol. por encima o por debajo (con tolerancias mayores para algunos productos, como los vinos con DOP o IGP almacenados más de tres años en botella o los espumosos).

**Agent answer:**

El grado alcohólico indicado en la etiqueta no podrá ser superior ni inferior en más de un 0,5 % vol. al grado determinado por el análisis [reg_ue_2019_33, Artículo 44]. 
No obstante, para los productos con denominación de origen almacenados en botella durante más de tres años, vinos espumosos, de aguja, de licor y de uvas sobremaduradas, esta diferencia admisible no podrá ser superior ni inferior en más de un 0,8 % vol. al grado determinado por el análisis [reg_ue_2019_33, Artículo 44].

<details><summary>search: tolerancia grado alcoholico etiqueta analisis</summary>

Result 1 | cite as [reg_ue_2019_33, Artículo 44] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 12
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 44. Grado alcohólico adquirido
El grado alcohólico volumétrico adquirido, contemplado en el artículo 119, apartado 1, letra c), del Reglamento (UE) n.o 1308/2013, se indicará en unidades o medias unidades porcentuales.
La cifra irá seguida del símbolo «% vol.» y podrá ir precedida de los términos «grado alcohólico adquirido» o «alcohol adquirido», o de la abreviatura «alc.». En lo que respecta al mosto de uva parcialmente fermentado o al vino nuevo aún en fermentación, la indicación del grado alcohólico adquirido podrá ser sustituida o completada por la del grado alcohólico total, seguida del símbolo «% vol.» y precedida de los términos «grado alcohólico total» o «alcohol total».
Sin perjuicio de las tolerancias previstas en relación con el método de análisis de referencia utilizado, el grado alcohólico indicado no podrá ser superior ni inferior en más de un 0,5 % vol. al grado determinado por el análisis. No obstante, por lo que respecta a los productos vitivinícolas con denominaciones de origen o indicaciones geográficas protegidas almacenados en botella durante más de tres años, y a los vinos espumosos, los vinos espumosos de calidad, los vinos espumosos gasificados, los vinos de aguja, los vinos de aguja gasificados, los vinos de licor y los vinos de uvas sobremaduradas, sin perjuicio de las tolerancias previstas en relación con el método de análisis de referencia utilizado, el grado alcohólico indicado no podrá ser superior ni inferior en más de un 0,8 % vol. al grado determinado por el análisis.

---

Result 2 | cite as [pliego_doca_rioja, Sección 2.a.1] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Sección 2.a.1. Graduación
Los vinos amparados son: tintos, rosados y blancos, con una graduación alcohólica adquirida mínima de 11,5 % Vol. para los tintos y de 10,5 % Vol. para los blancos y rosados.
Una vez finalizada la primera fermentación, la graduación alcohólica adquirida del vino con destino a vino espumoso de calidad deberá estar comprendida entre 9,5%vol. y 11,5%vol.
Los vinos espumosos de calidad amparados dispuestos para el consumo son blancos y rosados, con una graduación alcohólica adquirida mínima de 11% vol. y máxima de 13% vol.
Los vinos protegidos, para poder llevar el nombre de las unidades geográficas menores que la región delimitada o zonas “Rioja Alta”, “Rioja Oriental” y “Rioja Alavesa”, o el de una entidad geográfica menor incluida en una de estas zonas, como los municipios, además de haber sido obtenidos totalmente a partir de uva recolectada en el ámbito territorial de la correspondiente zona o entidad geográfica menor, deben reunir las siguientes condiciones en cuanto a características analíticas.
Zonas y tipos de vinos Grado alcohólico adquirido mínimo (% vol.) Rioja Alta y Rioja Alavesa:
Tintos 11,5 Blancos 11 Rosados 10,5 Rioja Oriental:
Tintos 12 Blancos 11,5 Rosados 11 Excepcionalmente se considerará que el vino procede de la zona o del municipio si en su elaboración incluye como máximo un 15% de uva procedente de viñedos inscritos, en términos municipales limítrofes a la zona o municipio de ubicación del operador y siempre que se acredite por cualquier título jurídico válido en derecho, disponer en exclusiva por un periodo mínimo de 10 años de forma ininterrumpida del citado 15% de la uva.
Los vinos con derecho a las indicaciones Reserva y Gran Reserva deberán alcanzar una graduación adquirida mínima de 12% Vol., en el caso de los tintos, o de 11% Vol., en el caso de los blancos y rosados.

---

Result 3 | cite as [ley_24_2003_vina_vino, Artículo 10] | Ley 24/2003 de la Viña y del Vino (consolidada), page 8
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 10. Aumento artificial de la graduación alcohólica natural.
1. Queda prohibido el aumento artificial de la graduación alcohólica natural de uva, mostos y vinos, con la excepción de los supuestos en que expresamente se permita.
2. No obstante, las comunidades autónomas cuando concurran condiciones meteorológicas desfavorables podrán autorizar el aumento de la graduación alcohólica de la uva, de los mostos y del vino nuevo aún en proceso de fermentación. A estos efectos el Gobierno, a propuesta del Ministro de Agricultura, Pesca y Alimentación, previa consulta de las comunidades autónomas, regulará las condiciones básicas de autorización del aumento de graduación alcohólica natural de uvas, mostos y vinos.
A tal fin, sin perjuicio de los métodos establecidos en la normativa comunitaria, se utilizará, con carácter preferente, la adición de mosto concentrado, o mosto concentrado rectificado.
3. En el marco de la normativa comunitaria vigente, queda prohibida la adición de sacarosa y de otros azúcares no procedentes de uva de vinificación para aumentar la graduación alcohólica natural de mostos y vinos.

---

Result 4 | cite as [rd_1363_2011_etiquetado, Artículo 6] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 6
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 6. Uso facultativo de códigos en el etiquetado.
1. De acuerdo con lo dispuesto en el artículo 56.5 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, la indicación del nombre y la dirección del embotellador, o la del productor o vendedor, o la del importador podrá ser sustituida en el etiquetado por un código.
Como código se utilizará el número de Registro de Envasadores de Vinos.
2. En aquellos casos en los que el producto en cuestión o en los que el operador económico citado en el primer párrafo, no sean objeto de inscripción en el Registro de Envasadores de Vinos, como código se utilizará el Código de Identificación Fiscal (CIF).

---

Result 5 | cite as [pliego_doca_rioja, Sección 3.b.2] | Pliego de condiciones de la DOCa Rioja, page 8
Pliego de condiciones de la DOCa Rioja — Sección 3.b.2. Características de la uva
Se dedicarán exclusivamente a la elaboración de vinos protegidos partidas de uva sana con un grado alcohólico volumétrico (% Vol.) natural mínimo de 11 % Vol. para las uvas tintas y de 10,5 % Vol. para las uvas blancas, separando las uvas tintas de las blancas en cada entrega parcial o pesada en báscula.
Se dedicarán exclusivamente a la elaboración de vinos espumosos de calidad partidas de uva sana con un grado alcohólico volumétrico (% vol.) natural mínimo de 9,5 % vol. tanto para las uvas tintas como para las uvas blancas, separando las uvas tintas de las blancas en cada entrega parcial o pesada en báscula.

</details>

---

## q15 (single)

**Question:** ¿Cuánto azúcar puede tener como máximo un espumoso para llamarse «brut nature»?

**Reference:** Menos de 3 gramos por litro, y solo si no se ha añadido azúcar después de la fermentación secundaria.

**Agent answer:**

Un vino espumoso puede llamarse «brut nature» si su contenido de azúcar es inferior a 3 gramos por litro y no se le ha añadido azúcar después de la segunda fermentación [reg_ue_2019_33, Anexo III, Parte A].

<details><summary>search: brut nature azucar espumoso</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 2.a.5] | Pliego de condiciones de la DOCa Rioja, page 4
Pliego de condiciones de la DOCa Rioja — Sección 2.a.5. Azúcares reductores
Los azúcares reductores residuales no deberán superar los 4 g/l. Se exceptúan los vinos tintos, blancos y rosados semisecos y los blancos y rosados dulces y semidulces. La obtención de estos vinos podrá efectuarse bien mediante la paralización de la fermentación, antes de su conclusión o bien partiendo de vinos secos mediante su edulcoración en las condiciones previstas en el Anexo I Parte D del Reglamento Delegado (UE) 2019/934, de la Comisión.
En función del contenido en azúcar, se autoriza para el vino espumoso de calidad el uso de los términos:
• Brut Nature: Inferior a 3 g/l sin adición de azúcar después de la segunda fermentación
• Extra brut: entre 0 y 6 g/l
• Brut: inferior a 12g/l
• Extra seco: entre 12 y 17 g/l
• Seco: entre 17 y 32 g/l
• Semi seco: entre 32 y 50 g/l En el caso de vinos espumosos de calidad con las menciones Reserva y Gran Añada únicamente se autorizan los términos Brut Nature, Extra Brut y Brut.

---

Result 2 | cite as [reg_ue_2019_33, Anexo III, Parte A] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 31
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Anexo III, Parte A. Lista de términos a que hace referencia el artículo 47, apartado 1, que han de
utilizarse para el vino espumoso, el vino espumoso gasificado, el vino espumoso de calidad o el vino espumoso aromático de calidad Términos Condiciones de utilización brut nature, naturherb, bruto natural, pas dosé, dosage zéro, natūralusis briutas, īsts bruts, přírodně tvrdé, popolnoma suho, dosaggio zero, брют натюр, brut natur Si su contenido de azúcar es inferior a 3 gramos por litro; estos términos únicamente podrán utilizarse para los productos a los que no se haya añadido azúcar después de la fermentación secundaria. extra brut, extra herb, ekstra briutas, ekstra brut, ekstra bruts, zvláště tvrdé, extra bruto, izredno suho, ekstra wytrawne, екстра брют Si su contenido de azúcar se sitúa entre 0 y 6 gramos por litro. brut, herb, briutas, bruts, tvrdé, bruto, zelo suho, bardzo wytrawne, брют Si su contenido de azúcar es inferior a 12 gramos por litro. extra dry, extra trocken, extra seco, labai sausas, ekstra kuiv, ekstra sausais, különlegesen száraz, wytrawne, suho, zvláště suché, extra suché, екстра сухо, extra sec, ekstra tør, vrlo suho Si su contenido de azúcar se sitúa entre 12 y 17 gramos por litro. sec, trocken, secco, asciutto, dry, tør, ξηρός, seco, torr, kuiva, sausas, kuiv, sausais, száraz, półwytrawne, polsuho, suché, сухо, suho Si su contenido de azúcar se sitúa entre 17 y 32 gramos por litro. demi-sec, halbtrocken, abboccato, medium dry, halvtør, ημίξηρος, semi seco, meio seco, halvtorr, puolikuiva, pusiau sausas, poolkuiv, pussausais, félszáraz, półsłodkie, polsladko, polosuché, polosladké, полусухо, polusuho Si su contenido de azúcar se sitúa entre 32 y 50 gramos por litro. doux, mild, dolce, sweet, sød, γλυκός, dulce, doce, söt, makea, saldus, magus, édes, ħelu, słodkie, sladko, sladké, сладко, dulce, saldais, slatko Si su contenido de azúcar es superior a 50 gramos por litro.

---

Result 3 | cite as [reg_ue_2019_33, Artículo 47] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 16
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 47. Indicación del contenido de azúcar en el vino espumoso, el vino
espumoso gasificado, el vino espumoso de calidad o el vino espumoso aromático de calidad
1. Los términos que figuran en el anexo III, parte A, del presente Reglamento para indicar el contenido de azúcar aparecerán en la etiqueta de los productos vitivinícolas contemplados en el artículo 119, apartado 1, letra g), del Reglamento (UE) n.o 1308/2013.
2. Si el contenido de azúcar de los productos vitivinícolas, expresado en términos de fructosa, glucosa y sacarosa, justifica el uso de dos de los términos enumerados en el anexo III, parte A, únicamente se elegirá uno de esos dos términos.
3. Sin perjuicio de las condiciones de utilización descritas en el anexo III, parte A, el contenido de azúcar no podrá ser superior ni inferior en más de 3 gramos por litro al contenido de azúcar indicado en la etiqueta del producto.

---

Result 4 | cite as [reg_ue_2019_33, Anexo III, Parte B] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 31
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Anexo III, Parte B. Lista de términos mencionados en el artículo 52, apartado 1, que han de utilizarse
para otros productos distintos de los enumerados en la parte A Términos Condiciones de utilización сухо, seco, suché, tør, trocken, kuiv, ξηρός, dry, sec, secco, asciutto, sausais, sausas, száraz, droog, wytrawne, seco, sec, suho, kuiva, torrt Si su contenido de azúcar no es superior a:
— 4 gramos por litro, o
— 9 gramos por litro, cuando la acidez total expresada en gramos de ácido tartárico por litro no sea inferior en más de 2 gramos al contenido de azúcar residual.
Términos Condiciones de utilización полусухо, semiseco, polosuché, halvtør, halbtrocken, poolkuiv, ημίξηρος, medium dry, demi-sec, abboccato, pussausais, pusiau sausas, félszáraz, halfdroog, półwytrawne, meio seco, adamado, demisec, polsuho, puolikuiva, halvtorrt, polusuho Si su contenido de azúcar supera el máximo antes establecido pero no es superior a:
— 12 gramos por litro, o
— 18 gramos por litro, cuando la acidez total expresada en gramos de ácido tartárico por litro no sea inferior en más de 10 gramos al contenido de azúcar residual. полусладко, semidulce, polosladké, halvsød, lieblich, poolmagus, ημίγλυκος, medium, medium sweet, moelleux, amabile, pussaldais, pusiau saldus, félédes, halfzoet, półsłodkie, meio doce, demidulce, polsladko, puolimakea, halvsött, poluslatko Si su contenido de azúcar supera el máximo establecido en la segunda fila de este cuadro, pero no es superior a 45 gramos por litro. сладко, dulce, sladké, sød, süss, magus, γλυκός, sweet, doux, dolce, saldais, saldus, édes, ħelu, zoet, słodkie, doce, dulce, sladko, makea, sött, slatko.
Si su contenido de azúcar es igual o superior a 45 gramos por litro.

---

Result 5 | cite as [reg_ue_2019_33, Artículo 52] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 20
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 52. Indicación del contenido de azúcar en los productos vitivinícolas
distintos del vino espumoso, el vino espumoso gasificado, el vino espumoso de calidad o el vino espumoso aromático de calidad
1. El contenido de azúcar expresado como fructosa y glucosa previsto en el anexo III, parte B, del presente Reglamento podrá figurar en la etiqueta de los productos vitivinícolas distintos de los mencionados en el artículo 119, apartado 1, letra g), del Reglamento (UE) n.o 1308/2013.
2. Si el contenido de azúcar de los productos vitivinícolas justifica el uso de dos de los términos enumerados en el anexo III, parte B, del presente Reglamento, se deberá elegir solamente uno de esos dos términos.
3. Sin perjuicio de las condiciones de utilización descritas en el anexo III, parte B, del presente Reglamento, el contenido de azúcar no podrá ser superior ni inferior en más de 1 gramo por litro al que aparece en la etiqueta del producto.
4. El apartado 1 no se aplicará a los productos vitivinícolas mencionados en el anexo VII, parte II, puntos 3, 8 y 9, del Reglamento (UE) n.o 1308/2013, siempre que las condiciones de utilización de la indicación del contenido de azúcar estén reguladas por los Estados miembros o establecidas en normas aplicables en el tercer país en cuestión, incluidas, en el caso de los terceros países, las normas procedentes de organizaciones profesionales representativas.

</details>

---

## q16 (single)

**Question:** ¿Tienen que estar todas las indicaciones obligatorias en el mismo campo visual de la botella?

**Reference:** Sí, legibles a la vez sin girar el envase; pueden ir fuera los alérgenos si la lista de ingredientes es electrónica, el importador, el número de lote y la fecha de durabilidad mínima.

**Agent answer:**

Sí, de forma general, las indicaciones obligatorias deben aparecer en el mismo campo visual del envase para ser simultáneamente legibles sin tener que girar el envase [reg_ue_2019_33, Artículo 40]. No obstante, pueden figurar fuera de dicho campo visual las sustancias o productos que causan alergias o intolerancias (cuando la lista de ingredientes se facilite por medios electrónicos), la mención del importador, el número de lote y la fecha de durabilidad mínima [reg_ue_2019_33, Artículo 40].

<details><summary>search: indicaciones obligatorias mismo campo visual reglamento</summary>

Result 1 | cite as [reg_ue_2019_33, Artículo 40] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 11
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 40. Presentación de las indicaciones obligatorias
1. Las indicaciones obligatorias mencionadas en el artículo 119 del Reglamento (UE) n.o 1308/2013 deberán aparecer en el mismo campo visual del envase, de tal manera que sean simultáneamente legibles sin tener que girar el envase, en caracteres indelebles y se distinguirán claramente del texto o dibujos adyacentes.
2. No obstante lo dispuesto en el apartado 1, las siguientes indicaciones obligatorias podrán figurar fuera del campo visual mencionado en dicho apartado:
a) las sustancias o productos que causan alergias o intolerancias, contemplados en el artículo 9, apartado 1, letra c), del Reglamento (UE) n.o 1169/2011, cuando la lista de ingredientes se facilite por medios electrónicos;
b) la mención del importador;
c) el número de lote, y
d) la fecha de durabilidad mínima.
3. El tamaño de los caracteres de las indicaciones a que se hace referencia en el apartado 1 del presente artículo y en el artículo 41, apartado 1, deberá ser igual o superior a 1,2 mm, independientemente del formato de caracteres utilizado.

---

Result 2 | cite as [rd_1363_2011_etiquetado, Artículo 6] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 6
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 6. Uso facultativo de códigos en el etiquetado.
1. De acuerdo con lo dispuesto en el artículo 56.5 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, la indicación del nombre y la dirección del embotellador, o la del productor o vendedor, o la del importador podrá ser sustituida en el etiquetado por un código.
Como código se utilizará el número de Registro de Envasadores de Vinos.
2. En aquellos casos en los que el producto en cuestión o en los que el operador económico citado en el primer párrafo, no sean objeto de inscripción en el Registro de Envasadores de Vinos, como código se utilizará el Código de Identificación Fiscal (CIF).

---

Result 3 | cite as [rd_1363_2011_etiquetado, Artículo 16] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 9
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 16. Ubicación de los nombres geográficos en el etiquetado.
En el etiquetado de los vinos con denominación de origen o con indicación geográfica protegidas deberá figurar inmediatamente próximo de dichas indicaciones o del término tradicional que las sustituya (de acuerdo con lo dispuesto en el artículo 118 sexvicies apartado 3, letra a, del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007), el nombre geográfico correspondiente.

---

Result 4 | cite as [reg_ue_2019_33, Artículo 41] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 11
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 41. Aplicación de ciertas normas horizontales
1. A los efectos de la indicación de determinadas sustancias o productos que causan alergias o intolerancias, contemplados en el artículo 21 del Reglamento (UE) n.o 1169/2011, los términos relativos a los sulfitos, los huevos y los productos a base de huevo y la leche y los productos lácteos que se utilizarán son los enumerados en el anexo I, parte A.
2. Los términos a que se refiere el apartado 1 podrán ir acompañados del correspondiente pictograma que figura en el anexo I, parte B.

---

Result 5 | cite as [rd_1363_2011_etiquetado, Artículo 23] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 23. Indicación obligatoria del año de la cosecha junto con términos tradicionales de envejecimiento.
En aplicación del artículo 70.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, será obligatoria la indicación del año de la cosecha en el etiquetado de los vinos incluidos en la categoría 1 del anexo XI ter del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007, con denominación de origen protegida, acompañando a los términos tradicionales «crianza», «reserva» o «gran reserva».

</details>

---

## q17 (single)

**Question:** Según la Ley de la Viña y del Vino, ¿qué multa corresponde a una infracción grave?

**Reference:** Multa de 2.001 a 30.000 euros, que puede llegar al 5 % del volumen de ventas del producto del ejercicio anterior.

**Agent answer:**

Las infracciones graves serán sancionadas con multa comprendida entre 2.001 y 30.000 euros [ley_24_2003_vina_vino, Artículo 42]. Esta cantidad podrá rebasarse hasta alcanzar el cinco por ciento del volumen de ventas del producto objeto de infracción, correspondiente al ejercicio económico inmediatamente anterior al de la iniciación del procedimiento sancionador [ley_24_2003_vina_vino, Artículo 42]. En el caso de infracciones graves en materia específica de viticultura, el importe de la sanción será del tanto al quíntuplo del valor de la producción afectada [ley_24_2003_vina_vino, Artículo 42].

<details><summary>search: Ley 24/2003 infracción grave multa</summary>

Result 1 | cite as [ley_24_2003_vina_vino, Artículo 37] | Ley 24/2003 de la Viña y del Vino (consolidada), page 10
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 37. Infracciones.
Los incumplimientos de lo dispuesto en esta ley, en la normativa comunitaria, en las disposiciones de las comunidades autónomas o en las disposiciones de desarrollo serán considerados como infracciones administrativas, que podrán ser leves, graves o muy graves.

---

Result 2 | cite as [ley_24_2003_vina_vino, Artículo 42] | Ley 24/2003 de la Viña y del Vino (consolidada), page 15
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 42. Sanciones. (parte 1/2)
1. Las infracciones leves serán sancionadas con apercibimiento o multa de hasta 2.000 euros, pudiendo rebasarse este importe hasta alcanzar el valor de las mercancías, productos o superficies objeto de la infracción. En materia de viticultura el cálculo del valor de los productos se realizará en la forma que se recoge en el apartado 2.
En el caso de la infracción recogida en el artículo 38.1.m), cuando se trate de una falta de utilización de una autorización de replantación o de conversión concedida, se aplicará siempre un apercibimiento, y, en caso de que se trate de una falta de una utilización de una autorización de nueva plantación concedida, el importe de la sanción será proporcional a la superficie no ejecutada de la autorización, como criterio determinante de la naturaleza de los perjuicios causados.
2. Las infracciones graves serán sancionadas con multa comprendida entre 2.001 y 30.000 euros, pudiendo rebasarse esta cantidad hasta alcanzar el cinco por ciento del volumen de ventas del producto objeto de infracción, correspondiente al ejercicio económico inmediatamente anterior al de la iniciación del procedimiento sancionador.
En el caso de infracciones graves en materia específica de viticultura, el importe de la sanción será del tanto al quíntuplo del valor de la producción afectada.
Ésta se calculará multiplicando la producción anual media por hectárea en el quinquenio precedente en la zona o provincia donde esté enclavada la superficie afectada por el precio medio ponderado en el mismo período y en la misma zona y provincia.
3. Las infracciones muy graves serán sancionadas con multa comprendida entre 30.001 y 300.000 euros, pudiendo rebasarse esta cantidad hasta alcanzar el 10 por ciento del volumen de ventas del producto objeto de infracción correspondiente al ejercicio económico, inmediatamente anterior al de la iniciación del procedimiento sancionador.
4. Cuando las infracciones graves sean cometidas por operadores acogidos a un nivel de protección y afecten a éste, podrá imponerse como sanción accesoria la pérdida temporal del uso del nombre protegido por un plazo máximo de tres años. Si se tratase de infracciones muy graves, podrá imponerse como sanción accesoria la pérdida temporal por un plazo máximo de cinco años o la pérdida definitiva de tal uso.

---

Result 3 | cite as [ley_24_2003_vina_vino, Artículo 39] | Ley 24/2003 de la Viña y del Vino (consolidada), page 11
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 39. Infracciones graves. (parte 3/4)
s) La falta de supervisión por parte de los organismos de control de que los operadores cumplen con las obligaciones que resulten de la aplicación del artículo 33.3.
2. Además, para los operadores voluntariamente acogidos a un nivel de protección, constituirán infracciones graves:
a) Las inexactitudes u omisiones en los datos y comprobantes que en cada caso sean precisos en los registros del nivel de protección correspondiente, cuando la diferencia entre la cantidad consignada y la correcta supere el porcentaje que se establezca en la normativa estatal o autonómica, según corresponda, que en ningún caso podrá ser superior al cinco por ciento de dicha diferencia.
b) El incumplimiento de las normas específicas del nivel de protección, sobre prácticas de producción, elaboración, transformación, conservación, transporte, acondicionamiento, etiquetado, envasado y presentación.
c) La expedición, comercialización o circulación de vinos amparados sin estar provistos de las contraetiquetas, precintas numeradas o cualquier otro medio de control establecido por la norma reguladora del nivel de protección.
d) Efectuar operaciones de elaboración, envasado o etiquetado de vinos amparados en instalaciones no inscritas en el nivel de protección correspondiente ni autorizadas.
e) El impago de las cuotas obligatorias establecidas, en su caso, para la financiación del órgano de gestión.
f) Cualquier otra infracción de la norma específica del nivel de protección, o de los acuerdos de su órgano de gestión en materia de producción, elaboración o características de los vinos amparados.
g) La elaboración y comercialización de un v.e.c.p.r.d. mediante la utilización de vino base procedente de instalaciones no inscritas en el nivel de protección correspondiente, así como la de un v.c.p.r.d. a partir de uvas, mostos o vino procedente de viñas no inscritas en el nivel de protección correspondiente.
h) Para las Denominaciones de Origen Calificadas, la introducción en viñas o bodegas inscritas de uva, mostos, o vinos procedentes de viñas o bodegas no inscritas.
i) Utilizar en la elaboración de productos de un determinado nivel de protección, uva procedente de parcelas en las que los rendimientos hayan sido superiores a los autorizados a los que se refiere el artículo 16.

---

Result 4 | cite as [ley_24_2003_vina_vino, Artículo 39] | Ley 24/2003 de la Viña y del Vino (consolidada), page 11
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 39. Infracciones graves. (parte 1/4)
1. Se considerarán infracciones graves:
a) La falta de libros-registro, documentos de acompañamiento o declaraciones relativas a uvas, vinos y mostos, así como los errores, inexactitudes u omisiones en ellos que afecten a las características de los productos o mercancías consignados.
b) Las inexactitudes o errores en libros-registro, documentos de acompañamiento o declaraciones relativas a uvas, vinos y mostos cuando la diferencia entre la cantidad consignada y la real supere un 15 por ciento de esta última.
c) La falta de actualización de los libros-registro cuando haya transcurrido más de un mes desde la fecha en que debió practicarse el primer asiento no reflejado.
d) La aportación de datos falsos en las solicitudes de ayudas y subvenciones públicas y el suministro de información falsa en las solicitudes relativas a viticultura.
e) La omisión en la etiqueta de la razón social responsable, o la falta de etiquetas o rotulación indeleble que fueran preceptivas, o la utilización de envases o embalajes que no reúnan los requisitos exigidos por las disposiciones vigentes.
f) La utilización en el etiquetado, presentación o publicidad de los productos, de denominaciones, indicaciones, calificaciones, expresiones o signos que no correspondan al producto o induzcan a confusión, salvo lo previsto en los párrafos a) y c) del apartado 2 del artículo siguiente. En particular, la utilización, cuando no se tenga derecho a ello, de las menciones sobre envejecimiento reguladas en el párrafo a) del artículo 3, o de las menciones reservadas a v.c.p.r.d. distintas a las reguladas en el párrafo b) del mismo artículo.
g) El incumplimiento de la entrega de productos para las destilaciones obligatorias de dos o más campañas en el período de cinco años anteriores a la inspección.
h) La tenencia o venta de productos enológicos sin autorización.
i) La elaboración o transformación de los productos regulados en esta ley mediante tratamientos, prácticas o procesos no autorizados, siempre que no existan riesgos para la salud, así como la adición o sustracción de sustancias que modifiquen la composición de los productos regulados con resultados fraudulentos.

---

Result 5 | cite as [ley_24_2003_vina_vino, Artículo 40] | Ley 24/2003 de la Viña y del Vino (consolidada), page 13
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 40. Infracciones muy graves. (parte 1/2)
1. Se considerarán infracciones muy graves:
a) La elaboración, transformación o comercialización de los productos regulados en esta ley mediante tratamientos, prácticas o procesos no autorizados, siempre que existan riesgos para la salud.
b) La no introducción en las etiquetas y presentación de los vinos de los elementos suficientes para diferenciar claramente su calificación y procedencia, a fin de evitar confusión en los consumidores, derivada de la utilización de una misma marca, nombre comercial o razón social en la comercialización de vinos correspondientes a distintos niveles de protección o procedentes de diferentes ámbitos geográficos.
c) La tenencia de maquinaria, instalaciones o productos no autorizados para la elaboración o almacenamiento de los vinos o mostos en locales de las industrias elaboradoras o envasadoras, cuando entrañen riesgos para la salud.
d) La falsificación de productos o la venta de productos falsificados, siempre que no sean constitutivas de delito o falta.
e) La negativa absoluta a la actuación de los servicios públicos de inspección.
f) La manipulación, traslado o disposición, sin autorización, de mercancías intervenidas cautelarmente, si se violan los precintos o si las mercancías salen de las instalaciones donde fueron intervenidas.
g) Las coacciones, amenazas, injurias, represalias, agresiones o cualquier otra forma de presión a los empleados públicos encargados de las funciones de inspección o vigilancia administrativa, siempre que no sean constitutivas de delito o falta.
2. En relación con los v.c.p.r.d. constituirán, asimismo, infracciones muy graves:
a) La utilización, cuando no se tenga derecho a ello, de indicaciones, nombres comerciales, marcas, símbolos o emblemas que hagan referencia a los nombres amparados por un nivel de protección, o que, por su similitud fonética o gráfica con los nombres protegidos o con los signos o emblemas que le sean característicos, puedan inducir a confusión sobre la naturaleza, calidad u origen de los productos, aunque vayan precedidos por los términos "tipo", "estilo", "género", "imitación", "sucedáneo" u otros análogos.
b) La utilización, cuando no se tenga derecho a ello, de las menciones reservadas a v.c.p.r.d. reguladas en el párrafo b) del artículo 3.
c) El uso de los nombres protegidos en productos a los que expresamente se les haya negado, así como las infracciones de los artículos 18.2 y 18.3.

</details>

---

## q18 (single)

**Question:** Según la Ley de la Viña y del Vino, ¿en cuánto tiempo prescribe una infracción grave?

**Reference:** A los dos años (las muy graves a los tres y las leves al año).

**Agent answer:**

Las infracciones graves prescribirán a los dos años [ley_24_2003_vina_vino, Artículo 45].

<details><summary>search: prescripción infracción grave Ley de la Viña y del Vino</summary>

Result 1 | cite as [ley_24_2003_vina_vino, Artículo 45] | Ley 24/2003 de la Viña y del Vino (consolidada), page 17
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 45. Prescripción de las infracciones y sanciones.
1. Las infracciones muy graves prescribirán a los tres años, las graves a los dos años, y las leves al año.
2. Las sanciones impuestas por infracciones muy graves prescribirán a los tres años; las impuestas por infracciones graves a los dos años ; y las impuestas por infracciones leves al año.

---

Result 2 | cite as [ley_24_2003_vina_vino, Artículo 39] | Ley 24/2003 de la Viña y del Vino (consolidada), page 11
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 39. Infracciones graves. (parte 1/4)
1. Se considerarán infracciones graves:
a) La falta de libros-registro, documentos de acompañamiento o declaraciones relativas a uvas, vinos y mostos, así como los errores, inexactitudes u omisiones en ellos que afecten a las características de los productos o mercancías consignados.
b) Las inexactitudes o errores en libros-registro, documentos de acompañamiento o declaraciones relativas a uvas, vinos y mostos cuando la diferencia entre la cantidad consignada y la real supere un 15 por ciento de esta última.
c) La falta de actualización de los libros-registro cuando haya transcurrido más de un mes desde la fecha en que debió practicarse el primer asiento no reflejado.
d) La aportación de datos falsos en las solicitudes de ayudas y subvenciones públicas y el suministro de información falsa en las solicitudes relativas a viticultura.
e) La omisión en la etiqueta de la razón social responsable, o la falta de etiquetas o rotulación indeleble que fueran preceptivas, o la utilización de envases o embalajes que no reúnan los requisitos exigidos por las disposiciones vigentes.
f) La utilización en el etiquetado, presentación o publicidad de los productos, de denominaciones, indicaciones, calificaciones, expresiones o signos que no correspondan al producto o induzcan a confusión, salvo lo previsto en los párrafos a) y c) del apartado 2 del artículo siguiente. En particular, la utilización, cuando no se tenga derecho a ello, de las menciones sobre envejecimiento reguladas en el párrafo a) del artículo 3, o de las menciones reservadas a v.c.p.r.d. distintas a las reguladas en el párrafo b) del mismo artículo.
g) El incumplimiento de la entrega de productos para las destilaciones obligatorias de dos o más campañas en el período de cinco años anteriores a la inspección.
h) La tenencia o venta de productos enológicos sin autorización.
i) La elaboración o transformación de los productos regulados en esta ley mediante tratamientos, prácticas o procesos no autorizados, siempre que no existan riesgos para la salud, así como la adición o sustracción de sustancias que modifiquen la composición de los productos regulados con resultados fraudulentos.

---

Result 3 | cite as [ley_24_2003_vina_vino, Artículo 39] | Ley 24/2003 de la Viña y del Vino (consolidada), page 11
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 39. Infracciones graves. (parte 2/4)
j) Las defraudaciones en la naturaleza, composición, calidad, peso o volumen o cualquier discrepancia entre las características reales de los productos de que se trate y las ofrecidas por el productor, elaborador o envasador, así como cualquier acto de naturaleza similar cuyo resultado sea el incumplimiento de las características de los productos establecidas en la legislación vigente.
k) La tenencia de maquinaria, instalaciones o productos no autorizados para la elaboración o almacenamiento de los vinos o mostos en locales de las industrias elaboradoras o envasadoras, siempre que no entrañen riesgos para la salud.
l) Destino de productos a usos no conformes con la normativa relativa al potencial vitícola.
m) Para las plantaciones realizadas con anterioridad al 1 de enero de 2016, las plantaciones realizadas con variedades de vid o portainjertos no clasificados por la comunidad autónoma correspondiente, el incumplimiento de la obligación del arranque de la parcela que ha sido objeto de la concesión de un derecho de plantación anticipado, o las plantaciones de vid o de portainjertos sin autorización, cuando el infractor no procediera, en un plazo inferior a dos meses desde que la comunidad autónoma lo requiera para el arranque, de la superficie afectada por la infracción.
n) La oposición a la toma de muestras, la dilación injustificada o la negativa a suministrar información o documentación necesaria para las funciones de inspección y control administrativo, así como la aportación de documentación o información falsa. ñ) La manipulación o disposición en cualquier forma, sin contar con la autorización del órgano competente, de mercancías intervenidas cautelarmente, cuando no resulte acreditado que entrañasen un riesgo para la salud.
o) El traslado físico, sin autorización del órgano competente, de las mercancías intervenidas cautelarmente, siempre que no se violen los precintos ni las mercancías salgan de las instalaciones en las que fueron intervenidas.
p) El incumplimiento de las condiciones esenciales de la autorización de plantación o replantación concedida, siempre que la comunidad autónoma que concedió la misma no considere la plantación realizada con el incumplimiento de estas condiciones como una plantación no autorizada.
q) (Suprimida)
r) El incumplimiento por los operadores de las obligaciones que resulten de la aplicación del artículo 33.3.

---

Result 4 | cite as [ley_6_2015_dop_igp, Artículo 37] | Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada), page 22
Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada) — Artículo 37. Prescripción y caducidad.
1. Las infracciones muy graves prescribirán a los tres años, las graves a los dos años, y las leves al año, a contar desde la fecha de comisión de la infracción.
2. Las sanciones impuestas por infracciones muy graves prescribirán a los tres años; las impuestas por infracciones graves a los dos años; y las impuestas por infracciones leves al año, a contar desde el día siguiente a aquel en que adquiera firmeza la resolución por la que se impone la sanción.
3. Caducará la acción para perseguir infracciones cuando conocida por la Administración la existencia de una infracción y finalizadas las diligencias dirigidas al esclarecimiento de los hechos, hubiera transcurrido un año sin que la autoridad competente hubiera ordenado incoar ningún procedimiento en relación con la infracción. En caso de caducidad del procedimiento este apartado no será de aplicación.
A estos efectos, cuando exista toma de muestras, las actuaciones de la inspección se entenderán finalizadas después de practicado el análisis inicial.
Las solicitudes de análisis contradictorios y dirimentes que fueren necesarios, interrumpirán los plazos de caducidad hasta que se practiquen.
4. El plazo máximo para resolver el procedimiento sancionador y notificar la resolución expresa del procedimiento sancionador por las infracciones establecidas en la presente ley será de diez meses.
5. La toma de muestras y análisis efectuados, así como los actos, documentos y trámites cuyo contenido se hubiere mantenido igual de no haber caducado el procedimiento anterior, podrán conservarse y surtir efectos en el nuevo procedimiento sancionador.

---

Result 5 | cite as [ley_24_2003_vina_vino, Artículo 38] | Ley 24/2003 de la Viña y del Vino (consolidada), page 10
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 38. Infracciones leves. (parte 1/2)
1. Se considerarán infracciones leves:
a) La ausencia de los libros-registro, sin causa justificada, cuando fueren requeridos para su control en actos de inspección.
b) Las inexactitudes o errores en libros-registro, en declaraciones relativas a uvas, vinos y mostos, o en documentos de acompañamiento, cuando la diferencia entre la cantidad consignada y la real no supere un 15 por ciento de esta última.
c) La falta de actualización de los libros-registro cuando no haya transcurrido más de un mes desde la fecha en que debió practicarse el primer asiento no reflejado.
d) La presentación de declaraciones relativas a uvas, vinos y mostos fuera del plazo reglamentario.
e) El suministro de información incorrecta en las solicitudes relativas a viticultura.
f) (Derogada).
g) (Derogada).
h) La falta de alguna de las indicaciones obligatorias en el etiquetado o presentación de los productos, salvo lo previsto en el párrafo e) del artículo siguiente, o su expresión en forma distinta a la reglamentaria.
i) La falta de identificación de los recipientes destinados al almacenamiento de productos a granel y de la indicación de su volumen nominal, así como de las indicaciones previstas para la identificación de su contenido, a excepción de los recipientes de menos de 600 litros, que se realizará de acuerdo con lo previsto en el artículo 10.5 del Reglamento CE 753/2002.
j) El incumplimiento de la entrega de productos para las destilaciones obligatorias.
k) La aplicación, en forma distinta a la legalmente establecida, de tratamientos, prácticas o procesos autorizados en la elaboración o transformación de los productos regulados en esta ley, siempre que no exista un riesgo para la salud.
l) La regularización de las plantaciones realizadas antes del 1 de septiembre de 1998 de acuerdo con lo dispuesto en el artículo 2.3, párrafos a) y c) del Reglamento (CE) 1493/1999.
m) La no utilización de una autorización de nueva plantación, de replantación o de conversión concedida, salvo en los casos fijados en la normativa nacional o de la Unión Europea.

</details>

---

## q19 (single)

**Question:** ¿Qué número de registro debe figurar obligatoriamente en la etiqueta de un vino embotellado en España?

**Reference:** El número de Registro de Envasadores de Vinos, atribuido por la comunidad autónoma competente.

**Agent answer:**

En el etiquetado de los vinos embotellados en España deberá figurar obligatoriamente el número de Registro de Envasadores de Vinos [rd_1363_2011_etiquetado, Artículo 4]. Dicho número de registro es atribuido por las comunidades autónomas competentes [rd_1363_2011_etiquetado, Artículo 4].

<details><summary>search: etiqueta vino numero de registro obligatoriamente España</summary>

Result 1 | cite as [rd_1363_2011_etiquetado, Artículo 4] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 6
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 4. Indicación del número de Registro de Envasadores de Vinos.
En aplicación del artículo 70.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, en el etiquetado de los vinos, deberá figurar obligatoriamente el número de Registro de Envasadores de Vinos, atribuido por las comunidades autónomas competentes.

---

Result 2 | cite as [rd_1363_2011_etiquetado, Artículo 6] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 6
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 6. Uso facultativo de códigos en el etiquetado.
1. De acuerdo con lo dispuesto en el artículo 56.5 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, la indicación del nombre y la dirección del embotellador, o la del productor o vendedor, o la del importador podrá ser sustituida en el etiquetado por un código.
Como código se utilizará el número de Registro de Envasadores de Vinos.
2. En aquellos casos en los que el producto en cuestión o en los que el operador económico citado en el primer párrafo, no sean objeto de inscripción en el Registro de Envasadores de Vinos, como código se utilizará el Código de Identificación Fiscal (CIF).

---

Result 3 | cite as [rd_1363_2011_etiquetado, Artículo 3] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 5
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 3. Obligación de etiquetar.
1. En aplicación del artículo 70.4 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, los vinos embotellados en España deberán ir etiquetados.
2. Quedan exceptuados de dicha obligación:
a) Los vinos transportados entre dos o más instalaciones de una misma empresa.
b) El vino no destinado a la venta, hasta un máximo de 30 litros por partida.
c) El vino destinado al consumo familiar del productor y de sus empleados.
d) Las botellas de vinos espumosos con denominación de origen protegida elaborados según el «método tradicional» que, cumpliendo lo establecido para esta mención en el artículo 66.4 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, satisfagan, además, los siguientes requisitos: 1.º) Que las botellas circulen dentro de la zona de producción de la denominación de origen protegida de que se trate y entre bodegas con derecho a la misma. 2.º) Que las botellas se encuentren en fase de elaboración cerradas con tapón de tiraje en el que se identifique el lote de procedencia y la bodega que efectuó su tiraje y fermentación. 3.º) Que vayan provistos de un documento de acompañamiento. 4.º) Que sean objeto de controles específicos.

---

Result 4 | cite as [ley_24_2003_vina_vino, Disposición adicional cuarta] | Ley 24/2003 de la Viña y del Vino (consolidada), page 18
Ley 24/2003 de la Viña y del Vino (consolidada) — Disposición adicional cuarta. Registros de envasadores de vino.
1. Cada comunidad autónoma deberá llevar un Registro de envasadores de vinos. Se facilitará el acceso a los datos contenidos en estos Registros, que serán comunicados al Ministerio de Agricultura, Pesca y Alimentación.
En el etiquetado de los productos afectados por el Registro de envasadores de vinos deberá figurar como mención obligatoria el número de registro atribuido por las comunidades autónomas competentes.
2. Se mantiene vigente el registro de embotelladoras de otras bebidas alcohólicas distintas del vino y su normativa de aplicación en los términos actuales, en tanto no se apruebe la normativa específica de dicho registro para estas bebidas.

---

Result 5 | cite as [rd_1363_2011_etiquetado, Artículo 9] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 7
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 9. Referencia al Estado miembro.
La referencia al Estado miembro en cuestión con la que deben completarse los códigos utilizados, según se establece en el artículo 56.5 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, se realizará añadiendo al final de los mismos la expresión «ES».

</details>

---

## q20 (single)

**Question:** ¿Puedo usar «crianza» o «reserva» si he envejecido el vino con trozos de madera de roble?

**Reference:** No. Estas menciones no pueden usarse en vinos elaborados con ayuda de trozos de madera de roble, aunque también se hayan usado barricas.

**Agent answer:**

Estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aún cuando se hayan empleado también en dichos procesos barricas de madera de roble [rd_1363_2011_etiquetado, Artículo 24].

<details><summary>search: trozos de madera de roble crianza reserva</summary>

Result 1 | cite as [rd_1363_2011_etiquetado, Artículo 24] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 24. Menciones relativas al envejecimiento del vino con denominación de origen protegida en recipientes de madera.
1. De acuerdo con el artículo 66.2 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, para indicar que el vino con denominación de origen protegida ha sido criado o envejecido en barrica de madera de roble, además de las indicaciones que figuran en el anexo XVI del citado reglamento, se podrán utilizar los términos tradiciones «crianza», «reserva» y «gran reserva» contemplados, para España, en el la base de datos electrónica E-Bacchus de la Unión Europea.
2. Estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aún cuando se hayan empleado también en dichos procesos barricas de madera de roble.

---

Result 2 | cite as [pliego_doca_rioja, Sección 3.c] | Pliego de condiciones de la DOCa Rioja, page 10
Pliego de condiciones de la DOCa Rioja — Sección 3.c. CRIANZA Y ENVEJECIMIENTO DE LOS VINOS
Requisitos para el uso de los términos tradicionales “Crianza”, “Reserva” y “Gran Reserva”:
• Para el término tradicional “Crianza”:
La crianza se efectuará en las bodegas inscritas en el Registro de Bodegas de Crianza durante, al menos, dos años naturales en el caso de los vinos tintos, y de dieciocho meses en el caso de los vinos blancos y rosados.
Los vinos se someterán al sistema tradicional mixto de envejecimiento en barrica de roble de 225 litros de capacidad aproximadamente, de forma continuada y sin interrupción durante un año, como mínimo, para los vinos tintos y durante seis meses, como mínimo, para los vinos blancos y rosados, seguido y complementado con envejecimiento en botella.
El Consejo Regulador podrá adoptar acuerdos relativos al inicio del cómputo del período de envejecimiento de los vinos
• Para el término tradicional “Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de treinta y seis meses, como mínimo, con una duración mínima de crianza en barrica de roble de doce meses, seguida y complementada con un envejecimiento mínimo en botella de seis meses.
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 24 meses Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de veinticuatro meses, como mínimo, con una duración mínima de crianza en barrica de roble de seis meses.
• Para el término tradicional “Gran Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de sesenta meses, como mínimo, con una duración mínima de crianza en barrica de roble de veinticuatro meses seguida y complementada con un envejecimiento mínimo en botella de veinticuatro meses.
Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de cuarenta y ocho meses, como mínimo, con una duración mínima de envejecimiento en barrica de roble de seis meses.
• Requisitos para el uso de la mención “Gran Añada”:
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 36 meses. La mención deberá ir acompañada del año de la cosecha.

---

Result 3 | cite as [rd_1363_2011_etiquetado, Artículo 18] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 9
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 18. Menciones relativas a la fermentación o envejecimiento del vino con denominación de origen o indicación geográfica protegida, en recipientes de madera.
1. De acuerdo con el artículo 66.2 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, además de las indicaciones que figuran en el anexo XVI del citado reglamento, para indicar que el vino con denominación de origen o indicación geográfica protegidas ha sido fermentado, criado o envejecido en recipientes de madera se podrán utilizar también:
a) Los términos tradiciones «noble» y «añejo» contemplados, para España, en la base de datos electrónica E-Bacchus de la Unión Europea.
b) «Barrica» y «roble» siempre que cumplan las condiciones señaladas en el anexo III del presente real decreto.
Las indicaciones «noble», «añejo» y «roble» sólo podrán emplearse cuando el recipiente sea de madera de roble, mientras que «barrica» podrá emplearse cuando el recipiente sea de cualquier especie de madera.
2. Estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aún cuando se hayan empleado también en dichos procesos recipientes de madera de roble o de otras especies.

---

Result 4 | cite as [rd_1363_2011_etiquetado, Anexo III] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 12
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Anexo III (parte 2/2)
Cuando se emplee o se haga referencia a este término, deberá indicarse en las informaciones relativas al vino en cuestión el periodo de tiempo, en meses o años, que ha permanecido en tales recipientes de madera, cuya capacidad máxima deberá ser de 600 litros. No obstante lo anterior, podrá utilizarse la indicación «Fermentado en barrica» siempre que la fermentación del vino haya tenido lugar en los recipientes citados, sin que sea preciso indicar en este caso el periodo de tiempo de permanencia. «Roble». Aplicable a los vinos con denominación de origen o indicación geográfica protegidas que hayan sido fermentados, criados o envejecidos en recipientes de madera de roble. Cuando se emplee o se haga referencia a este término, deberá indicarse en las informaciones relativas al vino en cuestión el periodo de tiempo, en meses o años, que ha permanecido en recipientes de madera de esa especie, cuya capacidad máxima deberá ser de 600 litros.

---

Result 5 | cite as [pliego_doca_rioja, Sección 8.b.10.11] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.11. Instalaciones de envejecimiento o crianza del vino
Las instalaciones en las que se realice la actividad de envejecimiento o crianza del vino con derecho a la Denominación de Origen Calificada Rioja, deberán estar exentas de trepidaciones, con temperatura constante y fresca durante todo el año y con estado higrométrico y ventilación adecuados. A este respecto, la temperatura en la nave de barricas estará comprendida entre 10ºC y 18ºC; y el estado higrométrico deberá estar entre 60% y 90% de humedad.
Las instalaciones deberán tener unas existencias mínimas de 225 hectolitros o en proceso de envejecimiento, de los que la mitad, al menos, deberán estar contenidos en un mínimo de 50 barricas de roble de 225 litros de capacidad aproximada.

</details>

---

## q21 (single)

**Question:** ¿Qué menciones de color se pueden usar en la etiqueta de un vino?

**Reference:** «Blanco», «Blanco de uva blanca», «Blanco de uva tinta», «Rosado», «Clarete» y «Tinto».

**Agent answer:**

Las menciones relativas a un color particular del vino que se pueden utilizar en la etiqueta son: «Blanco», «Blanco de uva blanca», «Blanco de uva tinta», «Rosado», «Clarete» y «Tinto» [rd_1363_2011_etiquetado, Anexo I]. Asimismo, las administraciones competentes pueden establecer otras menciones relativas a un color particular para incorporarlas a la normativa [rd_1363_2011_etiquetado, Artículo 12].

<details><summary>search: menciones de color etiqueta vino</summary>

Result 1 | cite as [rd_1363_2011_etiquetado, Anexo I] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 11
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Anexo I
Menciones relativas a un color particular del vino (artículo 12) «Blanco». «Blanco de uva blanca». «Blanco de uva tinta». «Rosado». «Clarete». «Tinto».

---

Result 2 | cite as [rd_1363_2011_etiquetado, Artículo 12] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 8
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 12. Menciones relativas al color.
En aplicación del artículo 70.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, las administraciones competentes podrán señalar requisitos para las menciones que figuran en el anexo I. Además, podrán establecer otras menciones relativas a un color particular del vino, las cuales serán comunicadas al Ministerio de Medio Ambiente y Medio Rural, y Marino a los efectos de su incorporación por el mismo al citado anexo.

---

Result 3 | cite as [pliego_doca_rioja, Sección 8.b.9] | Pliego de condiciones de la DOCa Rioja, page 28
Pliego de condiciones de la DOCa Rioja — Sección 8.b.9. DESIGNACION, ETIQUETADO (parte 1/3)
En las etiquetas de vinos envasados figurará obligatoriamente de forma destacada el nombre de la denominación junto con la mención “Denominación de Origen Calificada” justo debajo de aquél y el sello del Consejo Regulador, además de las menciones obligatorias que se determinen en la normativa y regulación específica, así como en la legislación aplicable. Así mismo podrán figurar las menciones facultativas y unidades geográficas menores en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable, si bien no podrán destacar respecto al nombre de “RIOJA”.
Antes de la puesta en circulación de etiquetas, éstas deberán ser autorizadas por el Consejo Regulador, en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable.
En el etiquetado de los vinos protegidos por la Denominación de Origen Calificada Rioja será obligatoria la indicación de la correspondiente marca comercial.
En el etiquetado deberá figurar obligatoriamente el nombre o razón social de una bodega inscrita. También podrá utilizarse un nombre comercial, en la forma prevista en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado de la expresión “Maceración carbónica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado principal de vinos blancos y rosados de la expresión “Fermentado en barrica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable Se prohíbe la utilización de cualquier tipo de referencia o alusión a las expresiones "barrica" y "madera" en la comercialización, propaganda y etiquetado de los vinos genéricos (sin agotar procesos de crianza).
Únicamente puede aplicarse a un vino el nombre de una zona o municipio cuando el vino proceda exclusivamente de uva de tal zona de producción o municipio, y su elaboración, crianza en su caso y embotellado se realicen en los mismos.

---

Result 4 | cite as [rd_1363_2011_etiquetado, Artículo 16] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 9
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 16. Ubicación de los nombres geográficos en el etiquetado.
En el etiquetado de los vinos con denominación de origen o con indicación geográfica protegidas deberá figurar inmediatamente próximo de dichas indicaciones o del término tradicional que las sustituya (de acuerdo con lo dispuesto en el artículo 118 sexvicies apartado 3, letra a, del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007), el nombre geográfico correspondiente.

---

Result 5 | cite as [rd_1363_2011_etiquetado, Anexo III] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 12
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Anexo III (parte 1/2)
Condiciones de utilización de menciones relativas al modo de obtención o a los métodos de elaboración de vinos con denominación de origen o indicación geográfica protegidas (artículo 17) «Maceración carbónica». Aplicable a los vinos en cuyo proceso de fermentación se ha seguido dicho método. «Pale dry». Aplicable a aquellos vinos de licor con denominación de origen protegida cuyo contenido en azúcares sea inferior a 50 g/l y que cumplan los requisitos establecidos en sus respectivos pliegos de condiciones. «Pale Cream». Aplicable a los vinos de licor con denominación de origen protegida con un contenido en azucares inferior a 115 gr/l y que cumplan los requisitos establecidos en sus respectivos pliegos de condiciones. «Mistela». Aplicable a los vinos de licor con denominación de origen protegida a los que se refiere el punto 3.c).4.º guión del anexo XI ter del Reglamento (CE) n.º 1234/2007, de 22 de octubre de 2007. «Naturalmente dulce». Aplicable a los vinos con denominación de origen protegida elaborados sin aumento artificial de su graduación y con el alcohol procedente en su totalidad de la fermentación, con un grado alcohólico volumétrico natural superior a 15% vol. y un grado alcohólico volumétrico adquirido no inferior a 13% vol. Y también a los vinos con indicación geográfica protegida de uva sobremadurada. «Vendimia tardía». Aplicable a los vinos con denominación de origen o indicación geográfica protegidas de uva sobremadurada. «Vendimia seleccionada». Aplicable a los vinos con denominación de origen o indicación geográfica protegidas, para los que la elección de la uva utilizada en su elaboración se ha realizado siguiendo criterios o normas especiales. «Barrica». Aplicable a los vinos con denominación de origen o indicación geográfica protegidas que hayan sido fermentados, criados o envejecidos en recipientes de madera.

</details>

---

## q22 (single)

**Question:** ¿Tengo que etiquetar el vino que no vendo y que es para consumo de mi familia?

**Reference:** No. Están exceptuados el vino destinado al consumo familiar del productor y sus empleados (y el vino no destinado a la venta hasta 30 litros por partida).

**Agent answer:**

No, el vino destinado al consumo familiar del productor y de sus empleados queda exceptuado de la obligación de ir etiquetado [rd_1363_2011_etiquetado, Artículo 3].

<details><summary>search: etiquetado vino consumo familiar excepcion</summary>

Result 1 | cite as [rd_1363_2011_etiquetado, Artículo 3] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 5
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 3. Obligación de etiquetar.
1. En aplicación del artículo 70.4 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, los vinos embotellados en España deberán ir etiquetados.
2. Quedan exceptuados de dicha obligación:
a) Los vinos transportados entre dos o más instalaciones de una misma empresa.
b) El vino no destinado a la venta, hasta un máximo de 30 litros por partida.
c) El vino destinado al consumo familiar del productor y de sus empleados.
d) Las botellas de vinos espumosos con denominación de origen protegida elaborados según el «método tradicional» que, cumpliendo lo establecido para esta mención en el artículo 66.4 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, satisfagan, además, los siguientes requisitos: 1.º) Que las botellas circulen dentro de la zona de producción de la denominación de origen protegida de que se trate y entre bodegas con derecho a la misma. 2.º) Que las botellas se encuentren en fase de elaboración cerradas con tapón de tiraje en el que se identifique el lote de procedencia y la bodega que efectuó su tiraje y fermentación. 3.º) Que vayan provistos de un documento de acompañamiento. 4.º) Que sean objeto de controles específicos.

---

Result 2 | cite as [rd_1363_2011_etiquetado, Artículo 6] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 6
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 6. Uso facultativo de códigos en el etiquetado.
1. De acuerdo con lo dispuesto en el artículo 56.5 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, la indicación del nombre y la dirección del embotellador, o la del productor o vendedor, o la del importador podrá ser sustituida en el etiquetado por un código.
Como código se utilizará el número de Registro de Envasadores de Vinos.
2. En aquellos casos en los que el producto en cuestión o en los que el operador económico citado en el primer párrafo, no sean objeto de inscripción en el Registro de Envasadores de Vinos, como código se utilizará el Código de Identificación Fiscal (CIF).

---

Result 3 | cite as [rd_1363_2011_etiquetado, Artículo 2] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 5
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 2. Ámbito de aplicación.
1. Las disposiciones contenidas en el presente real decreto son aplicables a los productos del sector vitivinícola que se indican a continuación, producidos en España, amparados o no por una denominación de origen o indicación geográfica protegidas: vino, vino nuevo en proceso de fermentación, vino de licor, vino espumoso, vino espumoso de calidad, vino espumoso aromático de calidad, vino espumoso gasificado, vino de aguja, vino de aguja gasificado, mosto de uva, mosto de uva parcialmente fermentado, mosto de uva concentrado, vino de uvas pasificadas y vino de uvas sobremaduradas.
2. Los artículos 3 a 10, ambos inclusive, son de aplicación a los productos del sector vitivinícola indicados en el apartado 1 que, procedentes de otros países, se embotellen en España.
3. Por otra parte, en el marco del Reglamento (CE) n.º 436/2009 de la Comisión, de 26 de mayo de 2009, el artículo 11 es de aplicación a los productos del sector vitivinícola que se almacenen, a granel, en España.

---

Result 4 | cite as [rd_1363_2011_etiquetado, Artículo 21] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 21. Términos tradicionales.
1. En aplicación del artículo 70.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, los términos tradicionales a los que se refiere la letra a) del apartado 1 del artículo 118 duovicies del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007, que, para España, se incluyen en la base de datos electrónica E-Bacchus de la Unión Europea, se indicarán en las etiquetas con caracteres cuyas dimensiones no superen a los que indiquen el nombre geográfico.
2. Igualmente, los términos tradicionales: «crianza», «reserva», y «gran reserva» se indicarán en caracteres de tamaño igual o inferior al de los utilizados en el nombre geográfico.

---

Result 5 | cite as [rd_1363_2011_etiquetado, Artículo 8] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 7
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 8. Condicionantes para la utilización de códigos.
1. Las sustituciones por un código a las que hacen referencia los artículos 6 y 7.1 están condicionadas a que el embotellador, productor, importador o vendedor tenga su sede en España y a que aparezca en la etiqueta el nombre y dirección de cualquier otra persona física o jurídica implicada en la distribución comercial, distinta del embotellador, productor, importador o vendedor indicados por el código.
2. En el caso de que no haya otra persona física o jurídica implicada en la distribución comercial, distinta del embotellador, productor, importador o vendedor indicados por el código, podrá emplearse una de las dos opciones siguientes:
a) El nombre o razón social del embotellador, productor, importador o vendedor podrá ser sustituido por un nombre comercial, conforme a lo establecido en el artículo 10.
b) Las comunidades autónomas podrán autorizar el empleo de siglas o abreviaturas, en el nombre o razón social del embotellador, productor, importador o vendedor, siempre y cuando se eliminen las palabras que consten de, o contengan, la denominación de origen o indicación geográfica protegidas a la que el producto embotellado no tiene derecho y siga siendo posible identificar al responsable del mismo a partir del Registro de Envasadores de Vinos.

</details>

---

## q23 (single)

**Question:** Si pongo «roble» en la etiqueta, ¿qué capacidad máxima puede tener el recipiente y qué más debo indicar?

**Reference:** Recipientes de roble de 600 litros como máximo, indicando el tiempo en meses o años que el vino ha permanecido en ellos.

**Agent answer:**

La capacidad máxima del recipiente de madera de roble debe ser de 600 litros [rd_1363_2011_etiquetado, Anexo III]. Cuando se emplee el término «roble», deberá indicarse el periodo de tiempo, en meses o años, que el vino ha permanecido en recipientes de madera de esa especie [rd_1363_2011_etiquetado, Anexo III].

<details><summary>search: etiqueta roble capacidad recipiente indicacion</summary>

Result 1 | cite as [rd_1363_2011_etiquetado, Anexo III] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 12
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Anexo III (parte 2/2)
Cuando se emplee o se haga referencia a este término, deberá indicarse en las informaciones relativas al vino en cuestión el periodo de tiempo, en meses o años, que ha permanecido en tales recipientes de madera, cuya capacidad máxima deberá ser de 600 litros. No obstante lo anterior, podrá utilizarse la indicación «Fermentado en barrica» siempre que la fermentación del vino haya tenido lugar en los recipientes citados, sin que sea preciso indicar en este caso el periodo de tiempo de permanencia. «Roble». Aplicable a los vinos con denominación de origen o indicación geográfica protegidas que hayan sido fermentados, criados o envejecidos en recipientes de madera de roble. Cuando se emplee o se haga referencia a este término, deberá indicarse en las informaciones relativas al vino en cuestión el periodo de tiempo, en meses o años, que ha permanecido en recipientes de madera de esa especie, cuya capacidad máxima deberá ser de 600 litros.

---

Result 2 | cite as [rd_1363_2011_etiquetado, Artículo 18] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 9
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 18. Menciones relativas a la fermentación o envejecimiento del vino con denominación de origen o indicación geográfica protegida, en recipientes de madera.
1. De acuerdo con el artículo 66.2 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, además de las indicaciones que figuran en el anexo XVI del citado reglamento, para indicar que el vino con denominación de origen o indicación geográfica protegidas ha sido fermentado, criado o envejecido en recipientes de madera se podrán utilizar también:
a) Los términos tradiciones «noble» y «añejo» contemplados, para España, en la base de datos electrónica E-Bacchus de la Unión Europea.
b) «Barrica» y «roble» siempre que cumplan las condiciones señaladas en el anexo III del presente real decreto.
Las indicaciones «noble», «añejo» y «roble» sólo podrán emplearse cuando el recipiente sea de madera de roble, mientras que «barrica» podrá emplearse cuando el recipiente sea de cualquier especie de madera.
2. Estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aún cuando se hayan empleado también en dichos procesos recipientes de madera de roble o de otras especies.

---

Result 3 | cite as [rd_1363_2011_etiquetado, Artículo 24] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 24. Menciones relativas al envejecimiento del vino con denominación de origen protegida en recipientes de madera.
1. De acuerdo con el artículo 66.2 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, para indicar que el vino con denominación de origen protegida ha sido criado o envejecido en barrica de madera de roble, además de las indicaciones que figuran en el anexo XVI del citado reglamento, se podrán utilizar los términos tradiciones «crianza», «reserva» y «gran reserva» contemplados, para España, en el la base de datos electrónica E-Bacchus de la Unión Europea.
2. Estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aún cuando se hayan empleado también en dichos procesos barricas de madera de roble.

---

Result 4 | cite as [rd_1363_2011_etiquetado, Artículo 11] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 7
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 11. Identificación del contenido de los recipientes para el almacenamiento de los productos vitivinícolas.
1. En desarrollo del artículo 47.1.j) del Reglamento (CE) n.º 436/2009 de la Comisión, de 26 de mayo de 2009, y de acuerdo con lo dispuesto el artículo 40.3 del citado reglamento, en los recipientes para el almacenamiento de los productos del sector vitivinícola deberá aparecer marcada de forma indeleble su identificación y volumen nominal.
Asimismo, con el fin de permitir a los organismos encargados del control proceder a la identificación de su contenido con la ayuda de los registros o de los documentos que los sustituyan, figurará en los recipientes la denominación de los productos que contengan, utilizando para ello las que se establecen en el anexo XI ter del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007.
En el caso de que los recipientes contengan un vino con denominación de origen o con indicación geográfica protegidas, se hará constar el nombre geográfico correspondiente.
2. No obstante, para los recipientes de un volumen nominal de 600 litros o menos, llenados con el mismo producto y almacenados juntos bajo el mismo lote, podrá sustituirse el marcado de los recipientes por el del lote en su totalidad, siempre que dicho lote esté claramente identificado y separado de los demás.

---

Result 5 | cite as [reg_ue_2019_33, Anexo V] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 39
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Anexo V. Indicaciones autorizadas en el etiquetado de los vinos en aplicación del
artículo 53, apartado 2 Fermentado en barrica Criado en barrica Envejecido en barrica Fermentado en tonel de […] [indicación del tipo de madera correspondiente] Criado en tonel de […] [indicación del tipo de madera correspondiente] Envejecido en tonel de […] [indicación del tipo de madera correspondiente] Fermentado en tonel Criado en tonel Envejecido en tonel La palabra «tonel» podrá sustituirse por la palabra «barrica».

</details>

---

## q24 (single)

**Question:** ¿Qué tipo de entidad jurídica es el Consejo Regulador de la DOCa Rioja?

**Reference:** Una corporación de derecho público creada por la Ley 6/2015.

**Agent answer:**

El corpus no cubre esta pregunta.

<details><summary>search: Consejo Regulador DOCa Rioja entidad jurídica</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 7.a] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 7.a. ÁREA GEOGRÁFICA (parte 3/7)
Ya en el siglo XX, en 1902, se promulgó una Real Orden que definía el "origen" para su aplicación a los vinos de Rioja. En 1926 se decretó la creación del Consejo Regulador cuya misión era delimitar la zona del Rioja, controlar la expedición de la "precinta de garantía" y recomendar las medidas legales que se tomarían contra los usurpadores y falsificadores del nombre "Rioja". Sin embargo, hasta 1945, este organismo no sería legalmente estructurado.
Finalmente, el Consejo Regulador quedó constituido en 1953, y comenzó así a sentar las bases de una actuación moderna y eficaz.
En la evolución hasta la actualidad del vino de Rioja destaca la aprobación, en 1970, del Reglamento de la Denominación de Origen y de su Consejo Regulador.
Fue en esa fecha cuando este organismo adquirió una estructuración y funciones perfectamente definidas: "La defensa de la Denominación de Origen, la aplicación, el control y fomento de la calidad de los vinos amparados quedaron encomendados, en primer término, al Consejo Regulador".
Tras varias modificaciones del Reglamento por el que se rige el Consejo Regulador, que lo han ido adaptando a las necesidades planteadas en los últimos años, los sistemas de control de calidad se han perfeccionado y a la vez se ha potenciado la promoción.
Después de un largo proceso en el que la Denominación de Origen Rioja apostó siempre por la calidad y el control en origen, este esfuerzo alcanzó su reconocimiento.
El 3 de abril de 1991 una Orden Ministerial otorgó el carácter de Calificada a la Denominación de Origen Rioja, primera en España que posee este rango, de manera que se alcanza el nivel cualitativo más alto de las figuras de calidad reguladas.

---

Result 2 | cite as [pliego_doca_rioja, Sección 4] | Pliego de condiciones de la DOCa Rioja, page 11
Pliego de condiciones de la DOCa Rioja — Sección 4. Delimitación De La Zona Geográfica (parte 1/3)
La zona de producción, crianza y envejecimiento está constituida por los terrenos ubicados en los términos municipales que se citan a continuación, que constituyen las zonas denominadas “Rioja Alta”, “Rioja Oriental” y “Rioja Alavesa”.
El Consejo Regulador determinará la ampliación de la zona geográfica a partir de informes que acrediten tanto la aptitud de los terrenos para la producción de uva de las variedades con la calidad necesaria para producir vinos de las características específicas de los protegidos por la denominación.
La calificación de los terrenos a la que se refiere el apartado e) Denominación de Origen Calificada, Términos Tradicionales, de la Disposición Adicional Tercera de la Ley 6/2015, de 12 de mayo, de Denominaciones de Origen e Indicaciones Geográficas Protegidas de ámbito territorial supraautonómico, será realizada por el Consejo Regulador.
Para las nuevas plantaciones o replantaciones en terrenos o viñedos situados en la zona de producción, así como para las modificaciones de las condiciones que puedan afectar al cumplimiento de este pliego de condiciones, será preceptivo el informe del Consejo Regulador, a efectos de su inscripción en el Registro correspondiente de la Denominación.

---

Result 3 | cite as [pliego_doca_rioja, Sección 8.b.10.5] | Pliego de condiciones de la DOCa Rioja, page 31
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.5. Embotellado en origen y otros requisitos de embotellado
El embotellado de vinos amparados por la denominación de origen calificada Rioja deberá ser realizado exclusivamente en las bodegas inscritas autorizadas por el Consejo Regulador, perdiendo el vino en otro caso el derecho al uso de la denominación.
Este requisito se establece al constatar que el riesgo para la calidad del vino finalmente ofrecido al consumo es más elevado cuando el vino ha sido transportado y embotellado fuera de la zona de producción que cuando estas operaciones se realizan en dicha zona. Sirve para proteger la gran reputación del vino de Rioja mediante un reforzamiento del control de sus características particulares y de su calidad protegiendo la denominación de origen calificada de la que es beneficiaria la colectividad de productores afectados. La decisión fue reconocida por sentencia del Tribunal de Justicia de la Unión Europea de 16 de mayo de 2000.
Los vinos amparados únicamente pueden circular y ser expedidos en los tipos de envase que no perjudiquen su calidad o prestigio y aprobados por el Consejo Regulador. Con carácter general los envases deberán ser de vidrio, de las capacidades autorizadas por la Unión Europea a excepción de la gama de un litro.
Excepcionalmente, el Consejo Regulador podrá autorizar para usos especiales otros tipos de envase, que entienda no perjudican la calidad o prestigio de los vinos protegidos.
No se permitirán embotellados por encargo en los casos de vinos procedentes de viñedos singulares.

---

Result 4 | cite as [pliego_doca_rioja, Sección 8.a] | Pliego de condiciones de la DOCa Rioja, page 21
Pliego de condiciones de la DOCa Rioja — Sección 8.a. MARCO LEGAL
● Legislación Nacional
- Orden APA/3465/2004, de 20 de octubre, por la que se aprueba el Reglamento de la D.O.Ca. Rioja y de su Consejo Regulador, y sus modificaciones posteriores.
- Orden APM/544/2017, de 5 de junio, por la que se aprueban los Estatutos del Consejo Regulador de la Denominación de Origen Calificada “Rioja”.
- Acuerdos del Consejo Regulador (circulares) de divulgación general a través de los Boletines Oficiales de La Rioja, Álava y Navarra.

---

Result 5 | cite as [pliego_doca_rioja, Sección 7.c] | Pliego de condiciones de la DOCa Rioja, page 20
Pliego de condiciones de la DOCa Rioja — Sección 7.c. NEXO CAUSAL ENTRE LA ZONA GEOGRÁFICA Y LAS CARACTERÍSTICAS (parte 1/2)
DEL PRODUCTO.
VINOS TRANQUILOS.
Los vinos de uvas procedentes de Rioja Alta se caracterizan por la especial influencia del clima atlántico, que hace que los vinos tengan una graduación media y cuerpo y acidez elevada, consecuencia de lo cual son vinos aptos para el envejecimiento en barrica. Es una zona con menor número de horas de luminosidad durante el ciclo vegetativo que en la zona más meridional de la Denominación y mayor pluviometría, lo que guarda relación directa con su acidez, que consideradas junto a la protección que ejerce la Sierra de Cantabria refuerzan las características descritas, tanto si se elaboran solos como si se ensamblan con vinos procedentes de las otras zonas. En el caso de la zona Rioja Alavesa, la confluencia de climas atlántico y mediterráneo supone que la graduación media sea algo más elevada que la de los anteriores, vinos con algo menos de acidez y más versátiles, en el sentido de que son vinos tanto para un consumo más inmediato como también aptos para el envejecimiento. La protección de la Sierra de Cantabria, al norte, se hace todavía más decisiva. Las horas de luminosidad son similares a las de Rioja Alta, si bien la pluviometría es algo inferior. Su versatilidad alcanza también a la idoneidad para obtener vinos de ensamblaje. Finalmente, en el caso de los vinos procedentes de la Rioja Oriental, observamos una menor pluviometría, un clima marcadamente mediterráneo caracterizado también por una mayor insolación con carácter general, un grado más elevado, extracto e idoneidad para el ensamblaje en vinos dedicados al envejecimiento en barrica, a la vez que ofrece también vinos que pueden ser aptos también para el consumo más inmediato.
La diferente tipología de suelos descubre tres con carácter mayoritario. De un lado los arcillo-calcáreos, situados en la parte más septentrional de la Denominación, que constituyen la fuente fundamental para la crianza, a caballo entre Rioja Alavesa y Rioja Alta, mientras que en esta última zona y en la Rioja Oriental, también aparecen los aluviales y los arcillo-ferrosos, que caracterizan vinos de menor cuerpo que los anteriores.

</details>

---

## q25 (single)

**Question:** ¿Es infracción usar «estilo Rioja» en la etiqueta de un vino que no está amparado por la denominación?

**Reference:** Sí, es infracción muy grave: usar sin derecho nombres o indicaciones que hagan referencia a una DOP o puedan inducir a confusión, aunque vayan precedidos de «tipo», «estilo», «imitación» u otros análogos.

**Agent answer:**

El corpus no cubre esta pregunta.

<details><summary>search: estilo Rioja infraccion etiqueta denominacion</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 8.b.9] | Pliego de condiciones de la DOCa Rioja, page 28
Pliego de condiciones de la DOCa Rioja — Sección 8.b.9. DESIGNACION, ETIQUETADO (parte 1/3)
En las etiquetas de vinos envasados figurará obligatoriamente de forma destacada el nombre de la denominación junto con la mención “Denominación de Origen Calificada” justo debajo de aquél y el sello del Consejo Regulador, además de las menciones obligatorias que se determinen en la normativa y regulación específica, así como en la legislación aplicable. Así mismo podrán figurar las menciones facultativas y unidades geográficas menores en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable, si bien no podrán destacar respecto al nombre de “RIOJA”.
Antes de la puesta en circulación de etiquetas, éstas deberán ser autorizadas por el Consejo Regulador, en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable.
En el etiquetado de los vinos protegidos por la Denominación de Origen Calificada Rioja será obligatoria la indicación de la correspondiente marca comercial.
En el etiquetado deberá figurar obligatoriamente el nombre o razón social de una bodega inscrita. También podrá utilizarse un nombre comercial, en la forma prevista en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado de la expresión “Maceración carbónica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado principal de vinos blancos y rosados de la expresión “Fermentado en barrica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable Se prohíbe la utilización de cualquier tipo de referencia o alusión a las expresiones "barrica" y "madera" en la comercialización, propaganda y etiquetado de los vinos genéricos (sin agotar procesos de crianza).
Únicamente puede aplicarse a un vino el nombre de una zona o municipio cuando el vino proceda exclusivamente de uva de tal zona de producción o municipio, y su elaboración, crianza en su caso y embotellado se realicen en los mismos.

---

Result 2 | cite as [pliego_doca_rioja, Sección 8.b.10.5] | Pliego de condiciones de la DOCa Rioja, page 31
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.5. Embotellado en origen y otros requisitos de embotellado
El embotellado de vinos amparados por la denominación de origen calificada Rioja deberá ser realizado exclusivamente en las bodegas inscritas autorizadas por el Consejo Regulador, perdiendo el vino en otro caso el derecho al uso de la denominación.
Este requisito se establece al constatar que el riesgo para la calidad del vino finalmente ofrecido al consumo es más elevado cuando el vino ha sido transportado y embotellado fuera de la zona de producción que cuando estas operaciones se realizan en dicha zona. Sirve para proteger la gran reputación del vino de Rioja mediante un reforzamiento del control de sus características particulares y de su calidad protegiendo la denominación de origen calificada de la que es beneficiaria la colectividad de productores afectados. La decisión fue reconocida por sentencia del Tribunal de Justicia de la Unión Europea de 16 de mayo de 2000.
Los vinos amparados únicamente pueden circular y ser expedidos en los tipos de envase que no perjudiquen su calidad o prestigio y aprobados por el Consejo Regulador. Con carácter general los envases deberán ser de vidrio, de las capacidades autorizadas por la Unión Europea a excepción de la gama de un litro.
Excepcionalmente, el Consejo Regulador podrá autorizar para usos especiales otros tipos de envase, que entienda no perjudican la calidad o prestigio de los vinos protegidos.
No se permitirán embotellados por encargo en los casos de vinos procedentes de viñedos singulares.

---

Result 3 | cite as [pliego_doca_rioja, Encabezado] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Encabezado
REGISTRO:
Número de expediente en el registro comunitario: PDO-ES-A0117 Fecha de recepción por la Comisión Europea: 11/11/2011.Fecha de modificación (eliminación restricción uso de marcas): 26/11/2014.
MODIFICACIONES:
Número de expediente en el registro comunitario: PDO-ES-A0117-AM03.
Fecha de modificación (corrección de errores): 29/02/2016.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM04.
Fecha de modificación (uso variedades en blancos y rosados y tiempos de envejecimiento): 14/7/2017.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM05.
Fecha de modificación (viñedo singular, vino espumoso, zona, municipio, intensidad colorante rosados): 15/02/2018.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM06.
Fecha de modificación (inicio computo envejecimiento): 24/09/2018.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM07.
Fecha de modificación (crianza de blancos y rosados): 23/09/2019.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM08.
Fecha de modificación (delimitación de viñedo singular, referencia requisitos mínimos de etiquetado): 31/01/2020 y 05/11/2020.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM09.
Fecha de modificación (plantaciones mixtas, calificación e informes sobre viñedos, delimitación viñedos singulares, condiciones instalaciones envejecimiento): 18-11-2021.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM10.
Fecha de modificación (nuevos tipos de vinos espumosos de calidad, cambios en la vendimia de uvas destinadas a vinos espumosos de calidad, cambios en las descripciones organolépticas, delimitación viñedos singulares, destino exclusivo de la producción de las viñas inscritas en Registro de Viñas a elaboración de vino amparado): 01-05-2023 y 07-06-2023 PLIEGO DE CONDICIONES DE LA DENOMINACIÓN DE ORIGEN PROTEGIDA (Denominación de Origen Calificada) “RIOJA”

---

Result 4 | cite as [pliego_doca_rioja, Sección 8.b.10.3] | Pliego de condiciones de la DOCa Rioja, page 30
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.3. Pruebas de conformidad
Cualquiera que sea el tipo de envase en que se expidan los vinos para el consumo, irán provistos de precintas de garantía, etiquetas o contraetiquetas numeradas, expedidas por el Consejo Regulador, y siempre en forma que no permita una segunda utilización. Deberá existir correspondencia entre las contraetiquetas, etiquetas y elementos de control del Consejo Regulador.
Para los vinos espumosos de calidad, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Método Tradicional”.
Para los vinos procedentes de ‘viñedo singular’, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Viñedo Singular”.
Para los vinos procedentes de zona o de municipio, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas con numeración controlada.
Si concurren las dos indicaciones en el vino o concurren con la de ‘Viñedo Singular’, se utilizará la precinta correspondiente a la unidad geográfica de menor tamaño.
Para los vinos de Crianza, Reserva y Gran Reserva, el Consejo Regulador expedirá contraetiquetas específicas y autorizará la mención de dichas indicaciones en la etiqueta.

---

Result 5 | cite as [pliego_doca_rioja, Sección 8.b.10.8] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.8. Términos tradicionales
Para la denominación de origen protegida “Rioja” el término tradicional al que se refiere el artículo 118 duovicies. 1a) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, Reglamento único para las OCM, es: “Denominación de Origen Calificada”.
Los términos tradicionales, a los que se refiere el artículo 118 duovicies.1b) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, que pueden utilizarse en los vinos amparados por la denominación de origen calificada “Rioja” son: “Crianza”, “Reserva”, “Gran Reserva”, “Añejo”, “Noble” y “Viejo”.

</details>

---

## q26 (single)

**Question:** ¿Qué dice el artículo 3 de la Ley de la Viña y del Vino sobre las indicaciones de crianza y reserva?

**Reference:** El artículo 3 está derogado, por lo que no contiene requisitos vigentes.

**Agent answer:**

El artículo 3 de la Ley 24/2003 de la Viña y del Vino figura como derogado [ley_24_2003_vina_vino, Artículo 3].

<details><summary>search: Ley 24 2003 articulo 3 indicaciones crianza reserva</summary>

Result 1 | cite as [ley_24_2003_vina_vino, Artículo 3] | Ley 24/2003 de la Viña y del Vino (consolidada), page 7
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 3. Indicaciones relativas a las características de los vinos.
(Derogado)

---

Result 2 | cite as [rd_1363_2011_etiquetado, Artículo 24] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 24. Menciones relativas al envejecimiento del vino con denominación de origen protegida en recipientes de madera.
1. De acuerdo con el artículo 66.2 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, para indicar que el vino con denominación de origen protegida ha sido criado o envejecido en barrica de madera de roble, además de las indicaciones que figuran en el anexo XVI del citado reglamento, se podrán utilizar los términos tradiciones «crianza», «reserva» y «gran reserva» contemplados, para España, en el la base de datos electrónica E-Bacchus de la Unión Europea.
2. Estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aún cuando se hayan empleado también en dichos procesos barricas de madera de roble.

---

Result 3 | cite as [ley_24_2003_vina_vino, Disposición adicional primera] | Ley 24/2003 de la Viña y del Vino (consolidada), page 17
Ley 24/2003 de la Viña y del Vino (consolidada) — Disposición adicional primera. Productos derivados de la uva y del vino.
Esta ley será también de aplicación a los productos derivados de la uva o del vino y, en particular, al vinagre de vino, a los vinos aromatizados, al brandy, al aguardiente de orujo y al mosto. Reglamentariamente se regularán, para el brandy, las menciones "Solera", "Solera Reserva" y "Solera Gran Reserva", así como el empleo de indicaciones de edad en las etiquetas.

---

Result 4 | cite as [ley_24_2003_vina_vino, Artículo 1] | Ley 24/2003 de la Viña y del Vino (consolidada), page 6
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 1. Objeto.
1. El objeto de esta ley es la ordenación básica, en el marco de la normativa de la Unión Europea, de la viña y del vino, así como su designación, presentación, promoción y publicidad.
2. Asimismo se regulan en esta ley los niveles diferenciados del origen y la calidad de los vinos, así como el sistema de protección, en defensa de productores y consumidores, de las denominaciones y menciones que legalmente les están reservados frente a su uso indebido.
3. También se incluye en el ámbito de esta ley el régimen sancionador de las infracciones administrativas en las materias a las que se refieren los dos apartados anteriores.

---

Result 5 | cite as [ley_24_2003_vina_vino, Disposición final tercera] | Ley 24/2003 de la Viña y del Vino (consolidada), page 19
Ley 24/2003 de la Viña y del Vino (consolidada) — Disposición final tercera. Entrada en vigor.
La presente ley entrará en vigor el día siguiente al de su publicación en el "Boletín Oficial del Estado", a excepción de lo previsto en el artículo 11, que entrará en vigor el día 1 de agosto de 2003.
Por tanto, Mando a todos los españoles, particulares y autoridades, que guarden y hagan guardar esta ley.
Madrid, 10 de julio de 2003.
JUAN CARLOS R.
El Presidente del Gobierno en funciones, MARIANO RAJOY BREY Información relacionada
• Véase la Sentencia del TC 34/2013, de 14 de febrero. Ref. BOE-A-2013-2717, que declara la vulneración de competencias de la Comunidad Autónoma de Cataluña.
• Véase la Sentencia del TC 82/2013, de 11 de abril. Ref. BOE-A-2013-4902, sobre vulneración del orden de competencias establecido en determinados preceptos en relación con la Comunidad Autónoma de Castilla-La Mancha.
Este documento es de carácter informativo y no tiene valor jurídico.

</details>

---

## q27 (multi)

**Question:** Si pongo «Gran Reserva» en un tinto de Rioja que solo ha envejecido 48 meses, ¿incumplo algo y qué multa me pueden poner?

**Reference:** Sí: un tinto Gran Reserva exige 60 meses (24 en barrica y 24 en botella). Usar indicaciones que no cumplen el pliego es infracción grave (Ley 6/2015, art. 31.1.f), sancionada con multa de 2.000,01 a 30.000 euros (art. 34).

**Agent answer:**

El corpus no cubre esta pregunta.

<details><summary>search: infracciones multas Ley 24 2003 vino</summary>

Result 1 | cite as [ley_24_2003_vina_vino, Artículo 42] | Ley 24/2003 de la Viña y del Vino (consolidada), page 15
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 42. Sanciones. (parte 1/2)
1. Las infracciones leves serán sancionadas con apercibimiento o multa de hasta 2.000 euros, pudiendo rebasarse este importe hasta alcanzar el valor de las mercancías, productos o superficies objeto de la infracción. En materia de viticultura el cálculo del valor de los productos se realizará en la forma que se recoge en el apartado 2.
En el caso de la infracción recogida en el artículo 38.1.m), cuando se trate de una falta de utilización de una autorización de replantación o de conversión concedida, se aplicará siempre un apercibimiento, y, en caso de que se trate de una falta de una utilización de una autorización de nueva plantación concedida, el importe de la sanción será proporcional a la superficie no ejecutada de la autorización, como criterio determinante de la naturaleza de los perjuicios causados.
2. Las infracciones graves serán sancionadas con multa comprendida entre 2.001 y 30.000 euros, pudiendo rebasarse esta cantidad hasta alcanzar el cinco por ciento del volumen de ventas del producto objeto de infracción, correspondiente al ejercicio económico inmediatamente anterior al de la iniciación del procedimiento sancionador.
En el caso de infracciones graves en materia específica de viticultura, el importe de la sanción será del tanto al quíntuplo del valor de la producción afectada.
Ésta se calculará multiplicando la producción anual media por hectárea en el quinquenio precedente en la zona o provincia donde esté enclavada la superficie afectada por el precio medio ponderado en el mismo período y en la misma zona y provincia.
3. Las infracciones muy graves serán sancionadas con multa comprendida entre 30.001 y 300.000 euros, pudiendo rebasarse esta cantidad hasta alcanzar el 10 por ciento del volumen de ventas del producto objeto de infracción correspondiente al ejercicio económico, inmediatamente anterior al de la iniciación del procedimiento sancionador.
4. Cuando las infracciones graves sean cometidas por operadores acogidos a un nivel de protección y afecten a éste, podrá imponerse como sanción accesoria la pérdida temporal del uso del nombre protegido por un plazo máximo de tres años. Si se tratase de infracciones muy graves, podrá imponerse como sanción accesoria la pérdida temporal por un plazo máximo de cinco años o la pérdida definitiva de tal uso.

---

Result 2 | cite as [ley_24_2003_vina_vino, Artículo 37] | Ley 24/2003 de la Viña y del Vino (consolidada), page 10
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 37. Infracciones.
Los incumplimientos de lo dispuesto en esta ley, en la normativa comunitaria, en las disposiciones de las comunidades autónomas o en las disposiciones de desarrollo serán considerados como infracciones administrativas, que podrán ser leves, graves o muy graves.

---

Result 3 | cite as [ley_24_2003_vina_vino, Artículo 38] | Ley 24/2003 de la Viña y del Vino (consolidada), page 10
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 38. Infracciones leves. (parte 1/2)
1. Se considerarán infracciones leves:
a) La ausencia de los libros-registro, sin causa justificada, cuando fueren requeridos para su control en actos de inspección.
b) Las inexactitudes o errores en libros-registro, en declaraciones relativas a uvas, vinos y mostos, o en documentos de acompañamiento, cuando la diferencia entre la cantidad consignada y la real no supere un 15 por ciento de esta última.
c) La falta de actualización de los libros-registro cuando no haya transcurrido más de un mes desde la fecha en que debió practicarse el primer asiento no reflejado.
d) La presentación de declaraciones relativas a uvas, vinos y mostos fuera del plazo reglamentario.
e) El suministro de información incorrecta en las solicitudes relativas a viticultura.
f) (Derogada).
g) (Derogada).
h) La falta de alguna de las indicaciones obligatorias en el etiquetado o presentación de los productos, salvo lo previsto en el párrafo e) del artículo siguiente, o su expresión en forma distinta a la reglamentaria.
i) La falta de identificación de los recipientes destinados al almacenamiento de productos a granel y de la indicación de su volumen nominal, así como de las indicaciones previstas para la identificación de su contenido, a excepción de los recipientes de menos de 600 litros, que se realizará de acuerdo con lo previsto en el artículo 10.5 del Reglamento CE 753/2002.
j) El incumplimiento de la entrega de productos para las destilaciones obligatorias.
k) La aplicación, en forma distinta a la legalmente establecida, de tratamientos, prácticas o procesos autorizados en la elaboración o transformación de los productos regulados en esta ley, siempre que no exista un riesgo para la salud.
l) La regularización de las plantaciones realizadas antes del 1 de septiembre de 1998 de acuerdo con lo dispuesto en el artículo 2.3, párrafos a) y c) del Reglamento (CE) 1493/1999.
m) La no utilización de una autorización de nueva plantación, de replantación o de conversión concedida, salvo en los casos fijados en la normativa nacional o de la Unión Europea.

---

Result 4 | cite as [ley_24_2003_vina_vino, Artículo 36] | Ley 24/2003 de la Viña y del Vino (consolidada), page 10
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 36. Competencia.
Corresponde la titularidad de la potestad sancionadora por las infracciones tipificadas en esta ley:
a) A la Administración General del Estado, en el caso de infracciones relativas a los niveles de protección cuyo ámbito territorial se extienda a más de una comunidad autónoma.
b) Al órgano competente de la Administración de la comunidad autónoma correspondiente, en los demás casos.

---

Result 5 | cite as [ley_24_2003_vina_vino, Artículo 41] | Ley 24/2003 de la Viña y del Vino (consolidada), page 14
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 41. Responsabilidad por las infracciones.
1. De las infracciones en productos envasados serán responsables las firmas o razones sociales que figuren en la etiqueta, bien nominalmente o bien mediante cualquier indicación que permita su identificación cierta.
Asimismo será responsable solidario el elaborador, fabricante o envasador que no figure en la etiqueta si se prueba que conocía la infracción cometida y que prestó su consentimiento. En caso de que se hayan falsificado las etiquetas, la responsabilidad corresponderá a las personas que comercialicen los productos a sabiendas de la falsificación.
2. De las infracciones en productos a granel, o envasados sin etiqueta, o cuando en la etiqueta no figure ninguna firma o razón social, será responsable su tenedor, excepto cuando se pueda identificar de manera cierta la responsabilidad de un tenedor anterior, sin perjuicio de la responsabilidad que corresponda al actual.
3. De las infracciones relativas a plantaciones, replantaciones, reposiciones de marras o riego será responsable el titular de la explotación y, subsidiariamente, el propietario de la misma.
4. De las infracciones cometidas por las personas jurídicas, incluidos los órganos de gestión de los v.c.p.r.d. y los organismos u órganos de inspección o control, serán responsables subsidiariamente los administradores o titulares de los mismos que no realizaren los actos necesarios que fuesen de su incumbencia para el cumplimiento de las obligaciones infringidas, consintieren el incumplimiento por quienes de ellos dependan o adoptaren acuerdos que hicieran posibles tales infracciones.
5. Asimismo serán responsables subsidiariamente los técnicos responsables de la elaboración y control respecto de las infracciones directamente relacionadas con su actividad profesional.
6. La responsabilidad administrativa por las infracciones reguladas en esta ley será independiente de la responsabilidad civil o penal que, en su caso, pueda exigirse a sus responsables, sin perjuicio de que no puedan concurrir dos sanciones cuando se aprecie identidad del sujeto, hecho y fundamento.

</details>

<details><summary>search: Gran Reserva tinto Rioja meses barrica botella</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 3.c] | Pliego de condiciones de la DOCa Rioja, page 10
Pliego de condiciones de la DOCa Rioja — Sección 3.c. CRIANZA Y ENVEJECIMIENTO DE LOS VINOS
Requisitos para el uso de los términos tradicionales “Crianza”, “Reserva” y “Gran Reserva”:
• Para el término tradicional “Crianza”:
La crianza se efectuará en las bodegas inscritas en el Registro de Bodegas de Crianza durante, al menos, dos años naturales en el caso de los vinos tintos, y de dieciocho meses en el caso de los vinos blancos y rosados.
Los vinos se someterán al sistema tradicional mixto de envejecimiento en barrica de roble de 225 litros de capacidad aproximadamente, de forma continuada y sin interrupción durante un año, como mínimo, para los vinos tintos y durante seis meses, como mínimo, para los vinos blancos y rosados, seguido y complementado con envejecimiento en botella.
El Consejo Regulador podrá adoptar acuerdos relativos al inicio del cómputo del período de envejecimiento de los vinos
• Para el término tradicional “Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de treinta y seis meses, como mínimo, con una duración mínima de crianza en barrica de roble de doce meses, seguida y complementada con un envejecimiento mínimo en botella de seis meses.
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 24 meses Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de veinticuatro meses, como mínimo, con una duración mínima de crianza en barrica de roble de seis meses.
• Para el término tradicional “Gran Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de sesenta meses, como mínimo, con una duración mínima de crianza en barrica de roble de veinticuatro meses seguida y complementada con un envejecimiento mínimo en botella de veinticuatro meses.
Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de cuarenta y ocho meses, como mínimo, con una duración mínima de envejecimiento en barrica de roble de seis meses.
• Requisitos para el uso de la mención “Gran Añada”:
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 36 meses. La mención deberá ir acompañada del año de la cosecha.

---

Result 2 | cite as [pliego_doca_rioja, Sección 8.b.10.8] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.8. Términos tradicionales
Para la denominación de origen protegida “Rioja” el término tradicional al que se refiere el artículo 118 duovicies. 1a) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, Reglamento único para las OCM, es: “Denominación de Origen Calificada”.
Los términos tradicionales, a los que se refiere el artículo 118 duovicies.1b) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, que pueden utilizarse en los vinos amparados por la denominación de origen calificada “Rioja” son: “Crianza”, “Reserva”, “Gran Reserva”, “Añejo”, “Noble” y “Viejo”.

---

Result 3 | cite as [pliego_doca_rioja, Sección 8.b.10.3] | Pliego de condiciones de la DOCa Rioja, page 30
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.3. Pruebas de conformidad
Cualquiera que sea el tipo de envase en que se expidan los vinos para el consumo, irán provistos de precintas de garantía, etiquetas o contraetiquetas numeradas, expedidas por el Consejo Regulador, y siempre en forma que no permita una segunda utilización. Deberá existir correspondencia entre las contraetiquetas, etiquetas y elementos de control del Consejo Regulador.
Para los vinos espumosos de calidad, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Método Tradicional”.
Para los vinos procedentes de ‘viñedo singular’, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Viñedo Singular”.
Para los vinos procedentes de zona o de municipio, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas con numeración controlada.
Si concurren las dos indicaciones en el vino o concurren con la de ‘Viñedo Singular’, se utilizará la precinta correspondiente a la unidad geográfica de menor tamaño.
Para los vinos de Crianza, Reserva y Gran Reserva, el Consejo Regulador expedirá contraetiquetas específicas y autorizará la mención de dichas indicaciones en la etiqueta.

---

Result 4 | cite as [pliego_doca_rioja, Sección 2.a.1] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Sección 2.a.1. Graduación
Los vinos amparados son: tintos, rosados y blancos, con una graduación alcohólica adquirida mínima de 11,5 % Vol. para los tintos y de 10,5 % Vol. para los blancos y rosados.
Una vez finalizada la primera fermentación, la graduación alcohólica adquirida del vino con destino a vino espumoso de calidad deberá estar comprendida entre 9,5%vol. y 11,5%vol.
Los vinos espumosos de calidad amparados dispuestos para el consumo son blancos y rosados, con una graduación alcohólica adquirida mínima de 11% vol. y máxima de 13% vol.
Los vinos protegidos, para poder llevar el nombre de las unidades geográficas menores que la región delimitada o zonas “Rioja Alta”, “Rioja Oriental” y “Rioja Alavesa”, o el de una entidad geográfica menor incluida en una de estas zonas, como los municipios, además de haber sido obtenidos totalmente a partir de uva recolectada en el ámbito territorial de la correspondiente zona o entidad geográfica menor, deben reunir las siguientes condiciones en cuanto a características analíticas.
Zonas y tipos de vinos Grado alcohólico adquirido mínimo (% vol.) Rioja Alta y Rioja Alavesa:
Tintos 11,5 Blancos 11 Rosados 10,5 Rioja Oriental:
Tintos 12 Blancos 11,5 Rosados 11 Excepcionalmente se considerará que el vino procede de la zona o del municipio si en su elaboración incluye como máximo un 15% de uva procedente de viñedos inscritos, en términos municipales limítrofes a la zona o municipio de ubicación del operador y siempre que se acredite por cualquier título jurídico válido en derecho, disponer en exclusiva por un periodo mínimo de 10 años de forma ininterrumpida del citado 15% de la uva.
Los vinos con derecho a las indicaciones Reserva y Gran Reserva deberán alcanzar una graduación adquirida mínima de 12% Vol., en el caso de los tintos, o de 11% Vol., en el caso de los blancos y rosados.

---

Result 5 | cite as [rd_1363_2011_etiquetado, Artículo 24] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 24. Menciones relativas al envejecimiento del vino con denominación de origen protegida en recipientes de madera.
1. De acuerdo con el artículo 66.2 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, para indicar que el vino con denominación de origen protegida ha sido criado o envejecido en barrica de madera de roble, además de las indicaciones que figuran en el anexo XVI del citado reglamento, se podrán utilizar los términos tradiciones «crianza», «reserva» y «gran reserva» contemplados, para España, en el la base de datos electrónica E-Bacchus de la Unión Europea.
2. Estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aún cuando se hayan empleado también en dichos procesos barricas de madera de roble.

</details>

<details><summary>search: infracciones graves Ley 24 2003 etiquetado denominación origen</summary>

Result 1 | cite as [ley_24_2003_vina_vino, Artículo 39] | Ley 24/2003 de la Viña y del Vino (consolidada), page 11
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 39. Infracciones graves. (parte 1/4)
1. Se considerarán infracciones graves:
a) La falta de libros-registro, documentos de acompañamiento o declaraciones relativas a uvas, vinos y mostos, así como los errores, inexactitudes u omisiones en ellos que afecten a las características de los productos o mercancías consignados.
b) Las inexactitudes o errores en libros-registro, documentos de acompañamiento o declaraciones relativas a uvas, vinos y mostos cuando la diferencia entre la cantidad consignada y la real supere un 15 por ciento de esta última.
c) La falta de actualización de los libros-registro cuando haya transcurrido más de un mes desde la fecha en que debió practicarse el primer asiento no reflejado.
d) La aportación de datos falsos en las solicitudes de ayudas y subvenciones públicas y el suministro de información falsa en las solicitudes relativas a viticultura.
e) La omisión en la etiqueta de la razón social responsable, o la falta de etiquetas o rotulación indeleble que fueran preceptivas, o la utilización de envases o embalajes que no reúnan los requisitos exigidos por las disposiciones vigentes.
f) La utilización en el etiquetado, presentación o publicidad de los productos, de denominaciones, indicaciones, calificaciones, expresiones o signos que no correspondan al producto o induzcan a confusión, salvo lo previsto en los párrafos a) y c) del apartado 2 del artículo siguiente. En particular, la utilización, cuando no se tenga derecho a ello, de las menciones sobre envejecimiento reguladas en el párrafo a) del artículo 3, o de las menciones reservadas a v.c.p.r.d. distintas a las reguladas en el párrafo b) del mismo artículo.
g) El incumplimiento de la entrega de productos para las destilaciones obligatorias de dos o más campañas en el período de cinco años anteriores a la inspección.
h) La tenencia o venta de productos enológicos sin autorización.
i) La elaboración o transformación de los productos regulados en esta ley mediante tratamientos, prácticas o procesos no autorizados, siempre que no existan riesgos para la salud, así como la adición o sustracción de sustancias que modifiquen la composición de los productos regulados con resultados fraudulentos.

---

Result 2 | cite as [ley_24_2003_vina_vino, Artículo 39] | Ley 24/2003 de la Viña y del Vino (consolidada), page 11
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 39. Infracciones graves. (parte 3/4)
s) La falta de supervisión por parte de los organismos de control de que los operadores cumplen con las obligaciones que resulten de la aplicación del artículo 33.3.
2. Además, para los operadores voluntariamente acogidos a un nivel de protección, constituirán infracciones graves:
a) Las inexactitudes u omisiones en los datos y comprobantes que en cada caso sean precisos en los registros del nivel de protección correspondiente, cuando la diferencia entre la cantidad consignada y la correcta supere el porcentaje que se establezca en la normativa estatal o autonómica, según corresponda, que en ningún caso podrá ser superior al cinco por ciento de dicha diferencia.
b) El incumplimiento de las normas específicas del nivel de protección, sobre prácticas de producción, elaboración, transformación, conservación, transporte, acondicionamiento, etiquetado, envasado y presentación.
c) La expedición, comercialización o circulación de vinos amparados sin estar provistos de las contraetiquetas, precintas numeradas o cualquier otro medio de control establecido por la norma reguladora del nivel de protección.
d) Efectuar operaciones de elaboración, envasado o etiquetado de vinos amparados en instalaciones no inscritas en el nivel de protección correspondiente ni autorizadas.
e) El impago de las cuotas obligatorias establecidas, en su caso, para la financiación del órgano de gestión.
f) Cualquier otra infracción de la norma específica del nivel de protección, o de los acuerdos de su órgano de gestión en materia de producción, elaboración o características de los vinos amparados.
g) La elaboración y comercialización de un v.e.c.p.r.d. mediante la utilización de vino base procedente de instalaciones no inscritas en el nivel de protección correspondiente, así como la de un v.c.p.r.d. a partir de uvas, mostos o vino procedente de viñas no inscritas en el nivel de protección correspondiente.
h) Para las Denominaciones de Origen Calificadas, la introducción en viñas o bodegas inscritas de uva, mostos, o vinos procedentes de viñas o bodegas no inscritas.
i) Utilizar en la elaboración de productos de un determinado nivel de protección, uva procedente de parcelas en las que los rendimientos hayan sido superiores a los autorizados a los que se refiere el artículo 16.

---

Result 3 | cite as [ley_6_2015_dop_igp, Artículo 31] | Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada), page 18
Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada) — Artículo 31. Infracciones graves. (parte 1/2)
1. Se consideran infracciones graves las siguientes:
a) La falta de los registros o libros-registro o documentos de acompañamiento, declaraciones o, en general, cualquier documentación que fuera preceptiva, así como los errores, inexactitudes u omisiones en ellos que afecten a las características de los productos o mercancías consignados.
b) Las inexactitudes o errores de cantidad en los registros, los documentos de acompañamiento, las declaraciones, o en general, en la documentación que fuera preceptiva, cuando la diferencia entre la cantidad consignada y la real supere un cinco por ciento.
c) El retraso en las anotaciones de los registros, en la presentación de declaraciones y en general de la documentación que fuera preceptiva cuando haya transcurrido más de un mes desde la fecha en que debió practicarse el primer asiento no reflejado o la fecha límite para presentar la declaración o documentación.
d) El incumplimiento de la obligación de remitir información o documentación a la Administración competente o al organismo de control en el plazo establecido; la aportación de datos falsos así como la dilación y oposición a la toma de muestras necesarias para la inspección.
e) La falta de etiquetas, la omisión en las mismas de indicaciones obligatorias o su rotulación de forma no indeleble cuando fueren preceptivas para aquellos productos amparados por una DOP o IGP.
f) La utilización en el etiquetado, presentación o publicidad de los productos regulados en esta ley, de denominaciones, indicaciones, calificaciones, expresiones o signos que no cumplan con lo establecido en la normativa específica de la DOP o IGP o induzcan a confusión salvo lo previsto en las infracciones muy graves.
g) El incumplimiento de las normas específicas de la DOP o IGP sobre características, prácticas de producción, elaboración, transformación, conservación, almacenamiento, transporte, etiquetado, envasado o presentación.
h) La tenencia de maquinaria, instalaciones o substancias prohibidas o no autorizadas en el pliego de condiciones cuando sea preceptiva su autorización, para la elaboración o almacenamiento de los productos, en las instalaciones o almacenes de las empresas productoras, elaboradoras o envasadoras.
i) La manipulación o disposición en cualquier forma de mercancías intervenidas cautelarmente sin contar con la preceptiva autorización.

---

Result 4 | cite as [ley_24_2003_vina_vino, Artículo 37] | Ley 24/2003 de la Viña y del Vino (consolidada), page 10
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 37. Infracciones.
Los incumplimientos de lo dispuesto en esta ley, en la normativa comunitaria, en las disposiciones de las comunidades autónomas o en las disposiciones de desarrollo serán considerados como infracciones administrativas, que podrán ser leves, graves o muy graves.

---

Result 5 | cite as [ley_24_2003_vina_vino, Artículo 40] | Ley 24/2003 de la Viña y del Vino (consolidada), page 13
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 40. Infracciones muy graves. (parte 1/2)
1. Se considerarán infracciones muy graves:
a) La elaboración, transformación o comercialización de los productos regulados en esta ley mediante tratamientos, prácticas o procesos no autorizados, siempre que existan riesgos para la salud.
b) La no introducción en las etiquetas y presentación de los vinos de los elementos suficientes para diferenciar claramente su calificación y procedencia, a fin de evitar confusión en los consumidores, derivada de la utilización de una misma marca, nombre comercial o razón social en la comercialización de vinos correspondientes a distintos niveles de protección o procedentes de diferentes ámbitos geográficos.
c) La tenencia de maquinaria, instalaciones o productos no autorizados para la elaboración o almacenamiento de los vinos o mostos en locales de las industrias elaboradoras o envasadoras, cuando entrañen riesgos para la salud.
d) La falsificación de productos o la venta de productos falsificados, siempre que no sean constitutivas de delito o falta.
e) La negativa absoluta a la actuación de los servicios públicos de inspección.
f) La manipulación, traslado o disposición, sin autorización, de mercancías intervenidas cautelarmente, si se violan los precintos o si las mercancías salen de las instalaciones donde fueron intervenidas.
g) Las coacciones, amenazas, injurias, represalias, agresiones o cualquier otra forma de presión a los empleados públicos encargados de las funciones de inspección o vigilancia administrativa, siempre que no sean constitutivas de delito o falta.
2. En relación con los v.c.p.r.d. constituirán, asimismo, infracciones muy graves:
a) La utilización, cuando no se tenga derecho a ello, de indicaciones, nombres comerciales, marcas, símbolos o emblemas que hagan referencia a los nombres amparados por un nivel de protección, o que, por su similitud fonética o gráfica con los nombres protegidos o con los signos o emblemas que le sean característicos, puedan inducir a confusión sobre la naturaleza, calidad u origen de los productos, aunque vayan precedidos por los términos "tipo", "estilo", "género", "imitación", "sucedáneo" u otros análogos.
b) La utilización, cuando no se tenga derecho a ello, de las menciones reservadas a v.c.p.r.d. reguladas en el párrafo b) del artículo 3.
c) El uso de los nombres protegidos en productos a los que expresamente se les haya negado, así como las infracciones de los artículos 18.2 y 18.3.

</details>

---

## q28 (multi)

**Question:** ¿Es obligatorio indicar la añada en un Rioja Reserva, y qué porcentaje de la uva debe ser de ese año?

**Reference:** Sí, el año de cosecha es obligatorio junto a «crianza», «reserva» o «gran reserva»; al menos el 85 % de la uva debe ser de ese año.

**Agent answer:**

Sí, es obligatorio indicar el año de la cosecha en el etiquetado de los vinos con denominación de origen protegida cuando acompañan a los términos tradicionales de envejecimiento como «reserva» [rd_1363_2011_etiquetado, Artículo 23]. 

Para que pueda aparecer el año de la cosecha, al menos el 85% de las uvas utilizadas para elaborar el producto deben haber sido cosechadas en ese año [reg_ue_2019_33, Artículo 49].

<details><summary>search: Rioja anada obligatorio Reserva porcentaje uva</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 3.b.1] | Pliego de condiciones de la DOCa Rioja, page 7
Pliego de condiciones de la DOCa Rioja — Sección 3.b.1. Proporción de variedades por tipos de vino
TINTO En los vinos tintos elaborados con uva desgranada, deberá emplearse, como mínimo, un 95% de uva de las variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. En los vinos tintos elaborados con uva entera, este porcentaje será, como mínimo, del 85 %.
BLANCO En la elaboración de vinos blancos se emplearán exclusivamente uvas de las variedades Viura, Garnacha Blanca, Malvasía, Maturana blanca, Tempranillo blanco, Turruntés, Chardonnay, Sauvignon blanc y Verdejo.
ROSADO Se empleará un mínimo del 25 % de uvas de variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. La mezcla opcional para el supuesto de los vinos rosados deberá realizarse con posterioridad a la entrega o pesada en báscula.
VINO ESPUMOSO DE CALIDAD La elaboración se realizará con uvas de las variedades blancas y/o tintas definidas en el apartado 6.
En la elaboración de vinos espumosos de calidad rosados se empleará un mínimo del 25% de uvas de las variedades de uva tinta definidas en el apartado 6.

---

Result 2 | cite as [pliego_doca_rioja, Sección 6] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 6. Variedades De Uva
La elaboración de los vinos protegidos se realizará exclusivamente con uvas de las variedades siguientes:
TINTAS BLANCAS Tempranillo Garnacha tinta Graciano Mazuelo Maturana tinta Viura Sauvignon blanc Malvasía Verdejo Garnacha Blanca Maturana blanca Chardonnay Tempranillo blanco Turruntés La uva procedente de plantaciones de viñedo efectuadas con anterioridad al 1 de enero de 1956 y con variedades de uva distintas a las que figuran en el Reglamento de la Denominación, pueden ser empleadas en la elaboración de vinos protegidos, en tanto subsistan dichas plantaciones. En el caso de la variedad vinífera Calagraño, las plantaciones han de ser anteriores a 27 de octubre de 1970.

---

Result 3 | cite as [pliego_doca_rioja, Sección 8.b.10.8] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.8. Términos tradicionales
Para la denominación de origen protegida “Rioja” el término tradicional al que se refiere el artículo 118 duovicies. 1a) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, Reglamento único para las OCM, es: “Denominación de Origen Calificada”.
Los términos tradicionales, a los que se refiere el artículo 118 duovicies.1b) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, que pueden utilizarse en los vinos amparados por la denominación de origen calificada “Rioja” son: “Crianza”, “Reserva”, “Gran Reserva”, “Añejo”, “Noble” y “Viejo”.

---

Result 4 | cite as [pliego_doca_rioja, Sección 2.a.1] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Sección 2.a.1. Graduación
Los vinos amparados son: tintos, rosados y blancos, con una graduación alcohólica adquirida mínima de 11,5 % Vol. para los tintos y de 10,5 % Vol. para los blancos y rosados.
Una vez finalizada la primera fermentación, la graduación alcohólica adquirida del vino con destino a vino espumoso de calidad deberá estar comprendida entre 9,5%vol. y 11,5%vol.
Los vinos espumosos de calidad amparados dispuestos para el consumo son blancos y rosados, con una graduación alcohólica adquirida mínima de 11% vol. y máxima de 13% vol.
Los vinos protegidos, para poder llevar el nombre de las unidades geográficas menores que la región delimitada o zonas “Rioja Alta”, “Rioja Oriental” y “Rioja Alavesa”, o el de una entidad geográfica menor incluida en una de estas zonas, como los municipios, además de haber sido obtenidos totalmente a partir de uva recolectada en el ámbito territorial de la correspondiente zona o entidad geográfica menor, deben reunir las siguientes condiciones en cuanto a características analíticas.
Zonas y tipos de vinos Grado alcohólico adquirido mínimo (% vol.) Rioja Alta y Rioja Alavesa:
Tintos 11,5 Blancos 11 Rosados 10,5 Rioja Oriental:
Tintos 12 Blancos 11,5 Rosados 11 Excepcionalmente se considerará que el vino procede de la zona o del municipio si en su elaboración incluye como máximo un 15% de uva procedente de viñedos inscritos, en términos municipales limítrofes a la zona o municipio de ubicación del operador y siempre que se acredite por cualquier título jurídico válido en derecho, disponer en exclusiva por un periodo mínimo de 10 años de forma ininterrumpida del citado 15% de la uva.
Los vinos con derecho a las indicaciones Reserva y Gran Reserva deberán alcanzar una graduación adquirida mínima de 12% Vol., en el caso de los tintos, o de 11% Vol., en el caso de los blancos y rosados.

---

Result 5 | cite as [pliego_doca_rioja, Sección 3.b.2] | Pliego de condiciones de la DOCa Rioja, page 8
Pliego de condiciones de la DOCa Rioja — Sección 3.b.2. Características de la uva
Se dedicarán exclusivamente a la elaboración de vinos protegidos partidas de uva sana con un grado alcohólico volumétrico (% Vol.) natural mínimo de 11 % Vol. para las uvas tintas y de 10,5 % Vol. para las uvas blancas, separando las uvas tintas de las blancas en cada entrega parcial o pesada en báscula.
Se dedicarán exclusivamente a la elaboración de vinos espumosos de calidad partidas de uva sana con un grado alcohólico volumétrico (% vol.) natural mínimo de 9,5 % vol. tanto para las uvas tintas como para las uvas blancas, separando las uvas tintas de las blancas en cada entrega parcial o pesada en báscula.

</details>

<details><summary>search: "Reserva" "añada" Rioja porcentaje indicación obligatorio</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 8.b.9] | Pliego de condiciones de la DOCa Rioja, page 28
Pliego de condiciones de la DOCa Rioja — Sección 8.b.9. DESIGNACION, ETIQUETADO (parte 1/3)
En las etiquetas de vinos envasados figurará obligatoriamente de forma destacada el nombre de la denominación junto con la mención “Denominación de Origen Calificada” justo debajo de aquél y el sello del Consejo Regulador, además de las menciones obligatorias que se determinen en la normativa y regulación específica, así como en la legislación aplicable. Así mismo podrán figurar las menciones facultativas y unidades geográficas menores en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable, si bien no podrán destacar respecto al nombre de “RIOJA”.
Antes de la puesta en circulación de etiquetas, éstas deberán ser autorizadas por el Consejo Regulador, en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable.
En el etiquetado de los vinos protegidos por la Denominación de Origen Calificada Rioja será obligatoria la indicación de la correspondiente marca comercial.
En el etiquetado deberá figurar obligatoriamente el nombre o razón social de una bodega inscrita. También podrá utilizarse un nombre comercial, en la forma prevista en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado de la expresión “Maceración carbónica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado principal de vinos blancos y rosados de la expresión “Fermentado en barrica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable Se prohíbe la utilización de cualquier tipo de referencia o alusión a las expresiones "barrica" y "madera" en la comercialización, propaganda y etiquetado de los vinos genéricos (sin agotar procesos de crianza).
Únicamente puede aplicarse a un vino el nombre de una zona o municipio cuando el vino proceda exclusivamente de uva de tal zona de producción o municipio, y su elaboración, crianza en su caso y embotellado se realicen en los mismos.

---

Result 2 | cite as [pliego_doca_rioja, Sección 8.b.10.8] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.8. Términos tradicionales
Para la denominación de origen protegida “Rioja” el término tradicional al que se refiere el artículo 118 duovicies. 1a) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, Reglamento único para las OCM, es: “Denominación de Origen Calificada”.
Los términos tradicionales, a los que se refiere el artículo 118 duovicies.1b) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, que pueden utilizarse en los vinos amparados por la denominación de origen calificada “Rioja” son: “Crianza”, “Reserva”, “Gran Reserva”, “Añejo”, “Noble” y “Viejo”.

---

Result 3 | cite as [pliego_doca_rioja, Sección 3.c] | Pliego de condiciones de la DOCa Rioja, page 10
Pliego de condiciones de la DOCa Rioja — Sección 3.c. CRIANZA Y ENVEJECIMIENTO DE LOS VINOS
Requisitos para el uso de los términos tradicionales “Crianza”, “Reserva” y “Gran Reserva”:
• Para el término tradicional “Crianza”:
La crianza se efectuará en las bodegas inscritas en el Registro de Bodegas de Crianza durante, al menos, dos años naturales en el caso de los vinos tintos, y de dieciocho meses en el caso de los vinos blancos y rosados.
Los vinos se someterán al sistema tradicional mixto de envejecimiento en barrica de roble de 225 litros de capacidad aproximadamente, de forma continuada y sin interrupción durante un año, como mínimo, para los vinos tintos y durante seis meses, como mínimo, para los vinos blancos y rosados, seguido y complementado con envejecimiento en botella.
El Consejo Regulador podrá adoptar acuerdos relativos al inicio del cómputo del período de envejecimiento de los vinos
• Para el término tradicional “Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de treinta y seis meses, como mínimo, con una duración mínima de crianza en barrica de roble de doce meses, seguida y complementada con un envejecimiento mínimo en botella de seis meses.
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 24 meses Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de veinticuatro meses, como mínimo, con una duración mínima de crianza en barrica de roble de seis meses.
• Para el término tradicional “Gran Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de sesenta meses, como mínimo, con una duración mínima de crianza en barrica de roble de veinticuatro meses seguida y complementada con un envejecimiento mínimo en botella de veinticuatro meses.
Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de cuarenta y ocho meses, como mínimo, con una duración mínima de envejecimiento en barrica de roble de seis meses.
• Requisitos para el uso de la mención “Gran Añada”:
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 36 meses. La mención deberá ir acompañada del año de la cosecha.

---

Result 4 | cite as [pliego_doca_rioja, Sección 8.b.10.3] | Pliego de condiciones de la DOCa Rioja, page 30
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.3. Pruebas de conformidad
Cualquiera que sea el tipo de envase en que se expidan los vinos para el consumo, irán provistos de precintas de garantía, etiquetas o contraetiquetas numeradas, expedidas por el Consejo Regulador, y siempre en forma que no permita una segunda utilización. Deberá existir correspondencia entre las contraetiquetas, etiquetas y elementos de control del Consejo Regulador.
Para los vinos espumosos de calidad, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Método Tradicional”.
Para los vinos procedentes de ‘viñedo singular’, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Viñedo Singular”.
Para los vinos procedentes de zona o de municipio, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas con numeración controlada.
Si concurren las dos indicaciones en el vino o concurren con la de ‘Viñedo Singular’, se utilizará la precinta correspondiente a la unidad geográfica de menor tamaño.
Para los vinos de Crianza, Reserva y Gran Reserva, el Consejo Regulador expedirá contraetiquetas específicas y autorizará la mención de dichas indicaciones en la etiqueta.

---

Result 5 | cite as [pliego_doca_rioja, Sección 2.a.1] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Sección 2.a.1. Graduación
Los vinos amparados son: tintos, rosados y blancos, con una graduación alcohólica adquirida mínima de 11,5 % Vol. para los tintos y de 10,5 % Vol. para los blancos y rosados.
Una vez finalizada la primera fermentación, la graduación alcohólica adquirida del vino con destino a vino espumoso de calidad deberá estar comprendida entre 9,5%vol. y 11,5%vol.
Los vinos espumosos de calidad amparados dispuestos para el consumo son blancos y rosados, con una graduación alcohólica adquirida mínima de 11% vol. y máxima de 13% vol.
Los vinos protegidos, para poder llevar el nombre de las unidades geográficas menores que la región delimitada o zonas “Rioja Alta”, “Rioja Oriental” y “Rioja Alavesa”, o el de una entidad geográfica menor incluida en una de estas zonas, como los municipios, además de haber sido obtenidos totalmente a partir de uva recolectada en el ámbito territorial de la correspondiente zona o entidad geográfica menor, deben reunir las siguientes condiciones en cuanto a características analíticas.
Zonas y tipos de vinos Grado alcohólico adquirido mínimo (% vol.) Rioja Alta y Rioja Alavesa:
Tintos 11,5 Blancos 11 Rosados 10,5 Rioja Oriental:
Tintos 12 Blancos 11,5 Rosados 11 Excepcionalmente se considerará que el vino procede de la zona o del municipio si en su elaboración incluye como máximo un 15% de uva procedente de viñedos inscritos, en términos municipales limítrofes a la zona o municipio de ubicación del operador y siempre que se acredite por cualquier título jurídico válido en derecho, disponer en exclusiva por un periodo mínimo de 10 años de forma ininterrumpida del citado 15% de la uva.
Los vinos con derecho a las indicaciones Reserva y Gran Reserva deberán alcanzar una graduación adquirida mínima de 12% Vol., en el caso de los tintos, o de 11% Vol., en el caso de los blancos y rosados.

</details>

<details><summary>search: Reglamento 2019/33 añada porcentaje obligatorio etiquetado</summary>

Result 1 | cite as [reg_ue_2019_33, Artículo 40] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 11
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 40. Presentación de las indicaciones obligatorias
1. Las indicaciones obligatorias mencionadas en el artículo 119 del Reglamento (UE) n.o 1308/2013 deberán aparecer en el mismo campo visual del envase, de tal manera que sean simultáneamente legibles sin tener que girar el envase, en caracteres indelebles y se distinguirán claramente del texto o dibujos adyacentes.
2. No obstante lo dispuesto en el apartado 1, las siguientes indicaciones obligatorias podrán figurar fuera del campo visual mencionado en dicho apartado:
a) las sustancias o productos que causan alergias o intolerancias, contemplados en el artículo 9, apartado 1, letra c), del Reglamento (UE) n.o 1169/2011, cuando la lista de ingredientes se facilite por medios electrónicos;
b) la mención del importador;
c) el número de lote, y
d) la fecha de durabilidad mínima.
3. El tamaño de los caracteres de las indicaciones a que se hace referencia en el apartado 1 del presente artículo y en el artículo 41, apartado 1, deberá ser igual o superior a 1,2 mm, independientemente del formato de caracteres utilizado.

---

Result 2 | cite as [reg_ue_2019_33, Artículo 1] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 2
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 1. Objeto
El presente Reglamento establece normas que completan el Reglamento (UE) n.o 1308/2013 en lo que se refiere a los siguientes aspectos:
a) en lo que respecta a las denominaciones de origen protegidas y las indicaciones geográficas protegidas en el sector vitivinícola:
i) el nombre que debe protegerse;
ii) los requisitos adicionales aplicables a los pliegos de condiciones;
iii) las excepciones relativas a la producción en la zona geográfica delimitada;
iv) las excepciones a la obligación de utilizar “indicaciones” en las etiquetas;
b) en lo que respecta a los términos tradicionales en el sector vitivinícola:
i) las solicitudes de protección;
ii) el procedimiento de oposición;
iii) las modificaciones;
iv) la cancelación;
c) en lo que respecta al sector vitivinícola en general: el etiquetado y la presentación.
DENOMINACIONES DE ORIGEN E INDICACIONES GEOGRÁFICAS PROTEGIDAS Solicitudes de protección

---

Result 3 | cite as [reg_ue_2019_33, Encabezado] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 1
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Encabezado
Este texto es exclusivamente un instrumento de documentación y no surte efecto jurídico. Las instituciones de la UE no asumen responsabilidad alguna por su contenido. Las versiones auténticas de los actos pertinentes, incluidos sus preámbulos, son las publicadas en el Diario Oficial de la Unión Europea, que pueden consultarse a través de EUR-Lex. Los textos oficiales son accesibles directamente mediante los enlaces integrados en este documento REGLAMENTO DELEGADO DE LA COMISIÓN (UE) 2019/33, de 17 de octubre de 2018, por el que se completa el Reglamento (UE) n.o 1308/2013 del Parlamento Europeo y del Consejo en lo que respecta a las solicitudes de protección y al etiquetado de denominaciones de origen e indicaciones geográficas, a las solicitudes de protección, al procedimiento de oposición, a la modificación y la cancelación de términos tradicionales y al etiquetado y la presentación en el sector vitivinícola (DO L 9 de 11.1.2019, p. 2) Modificado por:
Diario Oficial no página fecha Reglamento Delegado (UE) 2021/1375 de la Comisión de 11 de junio de 2021 L 297 16 20.8.2021 Reglamento Delegado (UE) 2023/1606 de la Comisión de 30 de mayo de 2023 L 198 6 8.8.2023 Reglamento Delegado (UE) 2025/28 de la Comisión de 30 de octubre de 2024 L 28 1 15.1.2025 Rectificado por:
Rectificación, DO L 269 de 23.10.2019, p. 14 (2019/33) Rectificación, DO L 90170 de 11.3.2024, p. 1 (2023/1606) REGLAMENTO DELEGADO DE LA COMISIÓN (UE) 2019/33, de 17 de octubre de 2018, por el que se completa el Reglamento (UE) n.o 1308/2013 del Parlamento Europeo y del Consejo en lo que respecta a las solicitudes de protección y al etiquetado de denominaciones de origen e indicaciones geográficas, a las solicitudes de protección, al procedimiento de oposición, a la modificación y la cancelación de términos tradicionales y al etiquetado y la presentación en el sector vitivinícola DISPOSICIÓN PRELIMINAR

---

Result 4 | cite as [reg_ue_2019_33, Artículo 44] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 12
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 44. Grado alcohólico adquirido
El grado alcohólico volumétrico adquirido, contemplado en el artículo 119, apartado 1, letra c), del Reglamento (UE) n.o 1308/2013, se indicará en unidades o medias unidades porcentuales.
La cifra irá seguida del símbolo «% vol.» y podrá ir precedida de los términos «grado alcohólico adquirido» o «alcohol adquirido», o de la abreviatura «alc.». En lo que respecta al mosto de uva parcialmente fermentado o al vino nuevo aún en fermentación, la indicación del grado alcohólico adquirido podrá ser sustituida o completada por la del grado alcohólico total, seguida del símbolo «% vol.» y precedida de los términos «grado alcohólico total» o «alcohol total».
Sin perjuicio de las tolerancias previstas en relación con el método de análisis de referencia utilizado, el grado alcohólico indicado no podrá ser superior ni inferior en más de un 0,5 % vol. al grado determinado por el análisis. No obstante, por lo que respecta a los productos vitivinícolas con denominaciones de origen o indicaciones geográficas protegidas almacenados en botella durante más de tres años, y a los vinos espumosos, los vinos espumosos de calidad, los vinos espumosos gasificados, los vinos de aguja, los vinos de aguja gasificados, los vinos de licor y los vinos de uvas sobremaduradas, sin perjuicio de las tolerancias previstas en relación con el método de análisis de referencia utilizado, el grado alcohólico indicado no podrá ser superior ni inferior en más de un 0,8 % vol. al grado determinado por el análisis.

---

Result 5 | cite as [reg_ue_2019_33, Artículo 49] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 18
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 49. Año de cosecha
1. El año de cosecha, al que se hace referencia en el artículo 120, apartado 1, letra a), del Reglamento (UE) n.o 1308/2013, podrá aparecer en las etiquetas de los productos vitivinícolas contemplados en el anexo VII, parte II, puntos 1 a 11, 13, 15 y 16, del Reglamento (UE) n.o 1308/2013, a condición de que al menos el 85 % de las uvas utilizadas para elaborar esos productos haya sido cosechado el año en cuestión. Quedan excluidas:
a) cualquier cantidad de productos vitivinícolas utilizados en la edulcoración, de «licor de expedición» o de «licor de tiraje», o
b) cualquier cantidad de productos vitivinícolas a los que se hace referencia en el anexo VII, parte II, punto 3, letras e) y f), del Reglamento (UE) n.o 1308/2013.
2. A los efectos del apartado 1, los productos vitivinícolas que no estén acogidos a una denominación de origen o una indicación geográfica protegida, pero sí lleven una indicación del año de la cosecha en la etiqueta, se certificarán de conformidad con el artículo 12 del Reglamento de Ejecución (UE) 2018/274 de la Comisión (5).
3. En el caso de los productos obtenidos tradicionalmente a partir de uvas cosechadas en enero o febrero, el año de cosecha que deberá aparecer en la etiqueta de los productos vitivinícolas será el del año civil anterior.

</details>

<details><summary>search: Rioja "año de cosecha" obligatorio "Reserva"</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 8.b.10.8] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.8. Términos tradicionales
Para la denominación de origen protegida “Rioja” el término tradicional al que se refiere el artículo 118 duovicies. 1a) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, Reglamento único para las OCM, es: “Denominación de Origen Calificada”.
Los términos tradicionales, a los que se refiere el artículo 118 duovicies.1b) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, que pueden utilizarse en los vinos amparados por la denominación de origen calificada “Rioja” son: “Crianza”, “Reserva”, “Gran Reserva”, “Añejo”, “Noble” y “Viejo”.

---

Result 2 | cite as [pliego_doca_rioja, Sección 8.b.9] | Pliego de condiciones de la DOCa Rioja, page 28
Pliego de condiciones de la DOCa Rioja — Sección 8.b.9. DESIGNACION, ETIQUETADO (parte 1/3)
En las etiquetas de vinos envasados figurará obligatoriamente de forma destacada el nombre de la denominación junto con la mención “Denominación de Origen Calificada” justo debajo de aquél y el sello del Consejo Regulador, además de las menciones obligatorias que se determinen en la normativa y regulación específica, así como en la legislación aplicable. Así mismo podrán figurar las menciones facultativas y unidades geográficas menores en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable, si bien no podrán destacar respecto al nombre de “RIOJA”.
Antes de la puesta en circulación de etiquetas, éstas deberán ser autorizadas por el Consejo Regulador, en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable.
En el etiquetado de los vinos protegidos por la Denominación de Origen Calificada Rioja será obligatoria la indicación de la correspondiente marca comercial.
En el etiquetado deberá figurar obligatoriamente el nombre o razón social de una bodega inscrita. También podrá utilizarse un nombre comercial, en la forma prevista en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado de la expresión “Maceración carbónica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado principal de vinos blancos y rosados de la expresión “Fermentado en barrica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable Se prohíbe la utilización de cualquier tipo de referencia o alusión a las expresiones "barrica" y "madera" en la comercialización, propaganda y etiquetado de los vinos genéricos (sin agotar procesos de crianza).
Únicamente puede aplicarse a un vino el nombre de una zona o municipio cuando el vino proceda exclusivamente de uva de tal zona de producción o municipio, y su elaboración, crianza en su caso y embotellado se realicen en los mismos.

---

Result 3 | cite as [pliego_doca_rioja, Sección 3.c] | Pliego de condiciones de la DOCa Rioja, page 10
Pliego de condiciones de la DOCa Rioja — Sección 3.c. CRIANZA Y ENVEJECIMIENTO DE LOS VINOS
Requisitos para el uso de los términos tradicionales “Crianza”, “Reserva” y “Gran Reserva”:
• Para el término tradicional “Crianza”:
La crianza se efectuará en las bodegas inscritas en el Registro de Bodegas de Crianza durante, al menos, dos años naturales en el caso de los vinos tintos, y de dieciocho meses en el caso de los vinos blancos y rosados.
Los vinos se someterán al sistema tradicional mixto de envejecimiento en barrica de roble de 225 litros de capacidad aproximadamente, de forma continuada y sin interrupción durante un año, como mínimo, para los vinos tintos y durante seis meses, como mínimo, para los vinos blancos y rosados, seguido y complementado con envejecimiento en botella.
El Consejo Regulador podrá adoptar acuerdos relativos al inicio del cómputo del período de envejecimiento de los vinos
• Para el término tradicional “Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de treinta y seis meses, como mínimo, con una duración mínima de crianza en barrica de roble de doce meses, seguida y complementada con un envejecimiento mínimo en botella de seis meses.
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 24 meses Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de veinticuatro meses, como mínimo, con una duración mínima de crianza en barrica de roble de seis meses.
• Para el término tradicional “Gran Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de sesenta meses, como mínimo, con una duración mínima de crianza en barrica de roble de veinticuatro meses seguida y complementada con un envejecimiento mínimo en botella de veinticuatro meses.
Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de cuarenta y ocho meses, como mínimo, con una duración mínima de envejecimiento en barrica de roble de seis meses.
• Requisitos para el uso de la mención “Gran Añada”:
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 36 meses. La mención deberá ir acompañada del año de la cosecha.

---

Result 4 | cite as [rd_1363_2011_etiquetado, Artículo 23] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 23. Indicación obligatoria del año de la cosecha junto con términos tradicionales de envejecimiento.
En aplicación del artículo 70.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, será obligatoria la indicación del año de la cosecha en el etiquetado de los vinos incluidos en la categoría 1 del anexo XI ter del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007, con denominación de origen protegida, acompañando a los términos tradicionales «crianza», «reserva» o «gran reserva».

---

Result 5 | cite as [pliego_doca_rioja, Sección 8.b.10.3] | Pliego de condiciones de la DOCa Rioja, page 30
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.3. Pruebas de conformidad
Cualquiera que sea el tipo de envase en que se expidan los vinos para el consumo, irán provistos de precintas de garantía, etiquetas o contraetiquetas numeradas, expedidas por el Consejo Regulador, y siempre en forma que no permita una segunda utilización. Deberá existir correspondencia entre las contraetiquetas, etiquetas y elementos de control del Consejo Regulador.
Para los vinos espumosos de calidad, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Método Tradicional”.
Para los vinos procedentes de ‘viñedo singular’, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Viñedo Singular”.
Para los vinos procedentes de zona o de municipio, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas con numeración controlada.
Si concurren las dos indicaciones en el vino o concurren con la de ‘Viñedo Singular’, se utilizará la precinta correspondiente a la unidad geográfica de menor tamaño.
Para los vinos de Crianza, Reserva y Gran Reserva, el Consejo Regulador expedirá contraetiquetas específicas y autorizará la mención de dichas indicaciones en la etiqueta.

</details>

---

## q29 (multi)

**Question:** ¿Qué graduación mínima necesita un tinto Rioja Reserva y cuánto puede desviarse la cifra de la etiqueta respecto al análisis?

**Reference:** Al menos 12 % vol.; la cifra indicada no puede desviarse más de 0,5 % vol. del análisis (salvo tolerancias específicas).

**Agent answer:**

Un vino tinto con la indicación Rioja Reserva debe alcanzar una graduación alcohólica adquirida mínima del 12 % Vol. [pliego_doca_rioja, Sección 2.a.1]. 

Respecto a la desviación, el grado alcohólico indicado en la etiqueta no podrá ser superior ni inferior en más de un 0,8 % vol. al grado determinado por el análisis, debido a que se trata de un producto vitivinícola con denominación de origen protegida almacenado en botella durante más de tres años [reg_ue_2019_33, Artículo 44].

<details><summary>search: grado alcoholico minimo tinto Reserva Rioja</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 2.a.1] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Sección 2.a.1. Graduación
Los vinos amparados son: tintos, rosados y blancos, con una graduación alcohólica adquirida mínima de 11,5 % Vol. para los tintos y de 10,5 % Vol. para los blancos y rosados.
Una vez finalizada la primera fermentación, la graduación alcohólica adquirida del vino con destino a vino espumoso de calidad deberá estar comprendida entre 9,5%vol. y 11,5%vol.
Los vinos espumosos de calidad amparados dispuestos para el consumo son blancos y rosados, con una graduación alcohólica adquirida mínima de 11% vol. y máxima de 13% vol.
Los vinos protegidos, para poder llevar el nombre de las unidades geográficas menores que la región delimitada o zonas “Rioja Alta”, “Rioja Oriental” y “Rioja Alavesa”, o el de una entidad geográfica menor incluida en una de estas zonas, como los municipios, además de haber sido obtenidos totalmente a partir de uva recolectada en el ámbito territorial de la correspondiente zona o entidad geográfica menor, deben reunir las siguientes condiciones en cuanto a características analíticas.
Zonas y tipos de vinos Grado alcohólico adquirido mínimo (% vol.) Rioja Alta y Rioja Alavesa:
Tintos 11,5 Blancos 11 Rosados 10,5 Rioja Oriental:
Tintos 12 Blancos 11,5 Rosados 11 Excepcionalmente se considerará que el vino procede de la zona o del municipio si en su elaboración incluye como máximo un 15% de uva procedente de viñedos inscritos, en términos municipales limítrofes a la zona o municipio de ubicación del operador y siempre que se acredite por cualquier título jurídico válido en derecho, disponer en exclusiva por un periodo mínimo de 10 años de forma ininterrumpida del citado 15% de la uva.
Los vinos con derecho a las indicaciones Reserva y Gran Reserva deberán alcanzar una graduación adquirida mínima de 12% Vol., en el caso de los tintos, o de 11% Vol., en el caso de los blancos y rosados.

---

Result 2 | cite as [pliego_doca_rioja, Sección 3.b.2] | Pliego de condiciones de la DOCa Rioja, page 8
Pliego de condiciones de la DOCa Rioja — Sección 3.b.2. Características de la uva
Se dedicarán exclusivamente a la elaboración de vinos protegidos partidas de uva sana con un grado alcohólico volumétrico (% Vol.) natural mínimo de 11 % Vol. para las uvas tintas y de 10,5 % Vol. para las uvas blancas, separando las uvas tintas de las blancas en cada entrega parcial o pesada en báscula.
Se dedicarán exclusivamente a la elaboración de vinos espumosos de calidad partidas de uva sana con un grado alcohólico volumétrico (% vol.) natural mínimo de 9,5 % vol. tanto para las uvas tintas como para las uvas blancas, separando las uvas tintas de las blancas en cada entrega parcial o pesada en báscula.

---

Result 3 | cite as [pliego_doca_rioja, Sección 3.b.1] | Pliego de condiciones de la DOCa Rioja, page 7
Pliego de condiciones de la DOCa Rioja — Sección 3.b.1. Proporción de variedades por tipos de vino
TINTO En los vinos tintos elaborados con uva desgranada, deberá emplearse, como mínimo, un 95% de uva de las variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. En los vinos tintos elaborados con uva entera, este porcentaje será, como mínimo, del 85 %.
BLANCO En la elaboración de vinos blancos se emplearán exclusivamente uvas de las variedades Viura, Garnacha Blanca, Malvasía, Maturana blanca, Tempranillo blanco, Turruntés, Chardonnay, Sauvignon blanc y Verdejo.
ROSADO Se empleará un mínimo del 25 % de uvas de variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. La mezcla opcional para el supuesto de los vinos rosados deberá realizarse con posterioridad a la entrega o pesada en báscula.
VINO ESPUMOSO DE CALIDAD La elaboración se realizará con uvas de las variedades blancas y/o tintas definidas en el apartado 6.
En la elaboración de vinos espumosos de calidad rosados se empleará un mínimo del 25% de uvas de las variedades de uva tinta definidas en el apartado 6.

---

Result 4 | cite as [pliego_doca_rioja, Sección 3.c] | Pliego de condiciones de la DOCa Rioja, page 10
Pliego de condiciones de la DOCa Rioja — Sección 3.c. CRIANZA Y ENVEJECIMIENTO DE LOS VINOS
Requisitos para el uso de los términos tradicionales “Crianza”, “Reserva” y “Gran Reserva”:
• Para el término tradicional “Crianza”:
La crianza se efectuará en las bodegas inscritas en el Registro de Bodegas de Crianza durante, al menos, dos años naturales en el caso de los vinos tintos, y de dieciocho meses en el caso de los vinos blancos y rosados.
Los vinos se someterán al sistema tradicional mixto de envejecimiento en barrica de roble de 225 litros de capacidad aproximadamente, de forma continuada y sin interrupción durante un año, como mínimo, para los vinos tintos y durante seis meses, como mínimo, para los vinos blancos y rosados, seguido y complementado con envejecimiento en botella.
El Consejo Regulador podrá adoptar acuerdos relativos al inicio del cómputo del período de envejecimiento de los vinos
• Para el término tradicional “Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de treinta y seis meses, como mínimo, con una duración mínima de crianza en barrica de roble de doce meses, seguida y complementada con un envejecimiento mínimo en botella de seis meses.
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 24 meses Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de veinticuatro meses, como mínimo, con una duración mínima de crianza en barrica de roble de seis meses.
• Para el término tradicional “Gran Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de sesenta meses, como mínimo, con una duración mínima de crianza en barrica de roble de veinticuatro meses seguida y complementada con un envejecimiento mínimo en botella de veinticuatro meses.
Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de cuarenta y ocho meses, como mínimo, con una duración mínima de envejecimiento en barrica de roble de seis meses.
• Requisitos para el uso de la mención “Gran Añada”:
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 36 meses. La mención deberá ir acompañada del año de la cosecha.

---

Result 5 | cite as [pliego_doca_rioja, Sección 2.a.5] | Pliego de condiciones de la DOCa Rioja, page 4
Pliego de condiciones de la DOCa Rioja — Sección 2.a.5. Azúcares reductores
Los azúcares reductores residuales no deberán superar los 4 g/l. Se exceptúan los vinos tintos, blancos y rosados semisecos y los blancos y rosados dulces y semidulces. La obtención de estos vinos podrá efectuarse bien mediante la paralización de la fermentación, antes de su conclusión o bien partiendo de vinos secos mediante su edulcoración en las condiciones previstas en el Anexo I Parte D del Reglamento Delegado (UE) 2019/934, de la Comisión.
En función del contenido en azúcar, se autoriza para el vino espumoso de calidad el uso de los términos:
• Brut Nature: Inferior a 3 g/l sin adición de azúcar después de la segunda fermentación
• Extra brut: entre 0 y 6 g/l
• Brut: inferior a 12g/l
• Extra seco: entre 12 y 17 g/l
• Seco: entre 17 y 32 g/l
• Semi seco: entre 32 y 50 g/l En el caso de vinos espumosos de calidad con las menciones Reserva y Gran Añada únicamente se autorizan los términos Brut Nature, Extra Brut y Brut.

</details>

<details><summary>search: tolerancia desviacion graduacion alcoholica etiquetado Rioja</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 2.a.1] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Sección 2.a.1. Graduación
Los vinos amparados son: tintos, rosados y blancos, con una graduación alcohólica adquirida mínima de 11,5 % Vol. para los tintos y de 10,5 % Vol. para los blancos y rosados.
Una vez finalizada la primera fermentación, la graduación alcohólica adquirida del vino con destino a vino espumoso de calidad deberá estar comprendida entre 9,5%vol. y 11,5%vol.
Los vinos espumosos de calidad amparados dispuestos para el consumo son blancos y rosados, con una graduación alcohólica adquirida mínima de 11% vol. y máxima de 13% vol.
Los vinos protegidos, para poder llevar el nombre de las unidades geográficas menores que la región delimitada o zonas “Rioja Alta”, “Rioja Oriental” y “Rioja Alavesa”, o el de una entidad geográfica menor incluida en una de estas zonas, como los municipios, además de haber sido obtenidos totalmente a partir de uva recolectada en el ámbito territorial de la correspondiente zona o entidad geográfica menor, deben reunir las siguientes condiciones en cuanto a características analíticas.
Zonas y tipos de vinos Grado alcohólico adquirido mínimo (% vol.) Rioja Alta y Rioja Alavesa:
Tintos 11,5 Blancos 11 Rosados 10,5 Rioja Oriental:
Tintos 12 Blancos 11,5 Rosados 11 Excepcionalmente se considerará que el vino procede de la zona o del municipio si en su elaboración incluye como máximo un 15% de uva procedente de viñedos inscritos, en términos municipales limítrofes a la zona o municipio de ubicación del operador y siempre que se acredite por cualquier título jurídico válido en derecho, disponer en exclusiva por un periodo mínimo de 10 años de forma ininterrumpida del citado 15% de la uva.
Los vinos con derecho a las indicaciones Reserva y Gran Reserva deberán alcanzar una graduación adquirida mínima de 12% Vol., en el caso de los tintos, o de 11% Vol., en el caso de los blancos y rosados.

---

Result 2 | cite as [pliego_doca_rioja, Sección 8.b.9] | Pliego de condiciones de la DOCa Rioja, page 28
Pliego de condiciones de la DOCa Rioja — Sección 8.b.9. DESIGNACION, ETIQUETADO (parte 1/3)
En las etiquetas de vinos envasados figurará obligatoriamente de forma destacada el nombre de la denominación junto con la mención “Denominación de Origen Calificada” justo debajo de aquél y el sello del Consejo Regulador, además de las menciones obligatorias que se determinen en la normativa y regulación específica, así como en la legislación aplicable. Así mismo podrán figurar las menciones facultativas y unidades geográficas menores en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable, si bien no podrán destacar respecto al nombre de “RIOJA”.
Antes de la puesta en circulación de etiquetas, éstas deberán ser autorizadas por el Consejo Regulador, en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable.
En el etiquetado de los vinos protegidos por la Denominación de Origen Calificada Rioja será obligatoria la indicación de la correspondiente marca comercial.
En el etiquetado deberá figurar obligatoriamente el nombre o razón social de una bodega inscrita. También podrá utilizarse un nombre comercial, en la forma prevista en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado de la expresión “Maceración carbónica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado principal de vinos blancos y rosados de la expresión “Fermentado en barrica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable Se prohíbe la utilización de cualquier tipo de referencia o alusión a las expresiones "barrica" y "madera" en la comercialización, propaganda y etiquetado de los vinos genéricos (sin agotar procesos de crianza).
Únicamente puede aplicarse a un vino el nombre de una zona o municipio cuando el vino proceda exclusivamente de uva de tal zona de producción o municipio, y su elaboración, crianza en su caso y embotellado se realicen en los mismos.

---

Result 3 | cite as [pliego_doca_rioja, Sección 3.b.2] | Pliego de condiciones de la DOCa Rioja, page 8
Pliego de condiciones de la DOCa Rioja — Sección 3.b.2. Características de la uva
Se dedicarán exclusivamente a la elaboración de vinos protegidos partidas de uva sana con un grado alcohólico volumétrico (% Vol.) natural mínimo de 11 % Vol. para las uvas tintas y de 10,5 % Vol. para las uvas blancas, separando las uvas tintas de las blancas en cada entrega parcial o pesada en báscula.
Se dedicarán exclusivamente a la elaboración de vinos espumosos de calidad partidas de uva sana con un grado alcohólico volumétrico (% vol.) natural mínimo de 9,5 % vol. tanto para las uvas tintas como para las uvas blancas, separando las uvas tintas de las blancas en cada entrega parcial o pesada en báscula.

---

Result 4 | cite as [pliego_doca_rioja, Sección 3] | Pliego de condiciones de la DOCa Rioja, page 6
Pliego de condiciones de la DOCa Rioja — Sección 3. Prácticas Específicas Para Elaboración Y Restricciones
IMPUESTAS.

---

Result 5 | cite as [pliego_doca_rioja, Sección 9.b] | Pliego de condiciones de la DOCa Rioja, page 33
Pliego de condiciones de la DOCa Rioja — Sección 9.b. TAREAS Y METODOLOGÍA DE CONTROL
El alcance de la verificación y los métodos de control son los que a continuación se detallan:
Tareas y ámbito Tipo de control BODEGAS -Inspección de instalaciones antes de su inscripción y comprobación de modificaciones. -Registro previo CC.AA.
Sistemático.
VIÑEDOS -Inspección viñedos de 2º año. -Registro previo CC.AA. -Ubicación, superficie, marco, variedad. -Aforo producción.
Sistemático - Apoyo Sistema de Información Geográfica (SIG) e instrumentos de precisión.
Poda. Aleatorio basado en análisis de riesgos.
Riego. Aleatorio basado en análisis de riesgos.
Expectativa rendimientos sobre admitido. Aleatorio basado en análisis de riesgos >10%.
Entrega de cosecha de uva:
Cantidad, color, procedencia, grado, sanidad.
Sistemático - Sistema informático de información y transmisión - Acceso web.
VINOS Aforo elaboración anual. Sistemático.
Proceso de calificación.
Toma de muestras elaboración. Sistemático Análisis químico. Sistemático - Lotes < 100.000 litros.
Análisis organoléptico. Sistemático - Lotes < 100.000 litros.
Toma de muestras de almacén de producto terminado.
Aleatorio.
Toma de muestras punto de venta. Aleatorio.
Aforo existencias de vino en bodega Aleatorio - Rotación completa 2 años.
Recuento de documentos de garantía Aleatorio - Rotación completa 2 años.
Control de traslado de vino entre instalaciones Aleatorio > 5%.
DECLARACIONES Existencias y movimientos de vino - Mensual Sistemático.
Exportación - Mensual Sistemático.
Documentos de garantía en poder de la firma
- Trimestral Sistemático.
Documentos de garantía en poder de la firma
- Serie y numeración - Anual Sistemático.
Existencias en almacén de producto terminado
- Anual Sistemático.
OTROS Etiquetados previos a utilización Sistemático.

</details>

<details><summary>search: tolerancia graduacion alcoholica etiquetado vino Reglamento</summary>

Result 1 | cite as [reg_ue_2019_33, Artículo 44] | Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025), page 12
Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025) — Artículo 44. Grado alcohólico adquirido
El grado alcohólico volumétrico adquirido, contemplado en el artículo 119, apartado 1, letra c), del Reglamento (UE) n.o 1308/2013, se indicará en unidades o medias unidades porcentuales.
La cifra irá seguida del símbolo «% vol.» y podrá ir precedida de los términos «grado alcohólico adquirido» o «alcohol adquirido», o de la abreviatura «alc.». En lo que respecta al mosto de uva parcialmente fermentado o al vino nuevo aún en fermentación, la indicación del grado alcohólico adquirido podrá ser sustituida o completada por la del grado alcohólico total, seguida del símbolo «% vol.» y precedida de los términos «grado alcohólico total» o «alcohol total».
Sin perjuicio de las tolerancias previstas en relación con el método de análisis de referencia utilizado, el grado alcohólico indicado no podrá ser superior ni inferior en más de un 0,5 % vol. al grado determinado por el análisis. No obstante, por lo que respecta a los productos vitivinícolas con denominaciones de origen o indicaciones geográficas protegidas almacenados en botella durante más de tres años, y a los vinos espumosos, los vinos espumosos de calidad, los vinos espumosos gasificados, los vinos de aguja, los vinos de aguja gasificados, los vinos de licor y los vinos de uvas sobremaduradas, sin perjuicio de las tolerancias previstas en relación con el método de análisis de referencia utilizado, el grado alcohólico indicado no podrá ser superior ni inferior en más de un 0,8 % vol. al grado determinado por el análisis.

---

Result 2 | cite as [ley_24_2003_vina_vino, Artículo 10] | Ley 24/2003 de la Viña y del Vino (consolidada), page 8
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 10. Aumento artificial de la graduación alcohólica natural.
1. Queda prohibido el aumento artificial de la graduación alcohólica natural de uva, mostos y vinos, con la excepción de los supuestos en que expresamente se permita.
2. No obstante, las comunidades autónomas cuando concurran condiciones meteorológicas desfavorables podrán autorizar el aumento de la graduación alcohólica de la uva, de los mostos y del vino nuevo aún en proceso de fermentación. A estos efectos el Gobierno, a propuesta del Ministro de Agricultura, Pesca y Alimentación, previa consulta de las comunidades autónomas, regulará las condiciones básicas de autorización del aumento de graduación alcohólica natural de uvas, mostos y vinos.
A tal fin, sin perjuicio de los métodos establecidos en la normativa comunitaria, se utilizará, con carácter preferente, la adición de mosto concentrado, o mosto concentrado rectificado.
3. En el marco de la normativa comunitaria vigente, queda prohibida la adición de sacarosa y de otros azúcares no procedentes de uva de vinificación para aumentar la graduación alcohólica natural de mostos y vinos.

---

Result 3 | cite as [rd_1363_2011_etiquetado, Artículo 2] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 5
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 2. Ámbito de aplicación.
1. Las disposiciones contenidas en el presente real decreto son aplicables a los productos del sector vitivinícola que se indican a continuación, producidos en España, amparados o no por una denominación de origen o indicación geográfica protegidas: vino, vino nuevo en proceso de fermentación, vino de licor, vino espumoso, vino espumoso de calidad, vino espumoso aromático de calidad, vino espumoso gasificado, vino de aguja, vino de aguja gasificado, mosto de uva, mosto de uva parcialmente fermentado, mosto de uva concentrado, vino de uvas pasificadas y vino de uvas sobremaduradas.
2. Los artículos 3 a 10, ambos inclusive, son de aplicación a los productos del sector vitivinícola indicados en el apartado 1 que, procedentes de otros países, se embotellen en España.
3. Por otra parte, en el marco del Reglamento (CE) n.º 436/2009 de la Comisión, de 26 de mayo de 2009, el artículo 11 es de aplicación a los productos del sector vitivinícola que se almacenen, a granel, en España.

---

Result 4 | cite as [pliego_doca_rioja, Sección 2.a.1] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Sección 2.a.1. Graduación
Los vinos amparados son: tintos, rosados y blancos, con una graduación alcohólica adquirida mínima de 11,5 % Vol. para los tintos y de 10,5 % Vol. para los blancos y rosados.
Una vez finalizada la primera fermentación, la graduación alcohólica adquirida del vino con destino a vino espumoso de calidad deberá estar comprendida entre 9,5%vol. y 11,5%vol.
Los vinos espumosos de calidad amparados dispuestos para el consumo son blancos y rosados, con una graduación alcohólica adquirida mínima de 11% vol. y máxima de 13% vol.
Los vinos protegidos, para poder llevar el nombre de las unidades geográficas menores que la región delimitada o zonas “Rioja Alta”, “Rioja Oriental” y “Rioja Alavesa”, o el de una entidad geográfica menor incluida en una de estas zonas, como los municipios, además de haber sido obtenidos totalmente a partir de uva recolectada en el ámbito territorial de la correspondiente zona o entidad geográfica menor, deben reunir las siguientes condiciones en cuanto a características analíticas.
Zonas y tipos de vinos Grado alcohólico adquirido mínimo (% vol.) Rioja Alta y Rioja Alavesa:
Tintos 11,5 Blancos 11 Rosados 10,5 Rioja Oriental:
Tintos 12 Blancos 11,5 Rosados 11 Excepcionalmente se considerará que el vino procede de la zona o del municipio si en su elaboración incluye como máximo un 15% de uva procedente de viñedos inscritos, en términos municipales limítrofes a la zona o municipio de ubicación del operador y siempre que se acredite por cualquier título jurídico válido en derecho, disponer en exclusiva por un periodo mínimo de 10 años de forma ininterrumpida del citado 15% de la uva.
Los vinos con derecho a las indicaciones Reserva y Gran Reserva deberán alcanzar una graduación adquirida mínima de 12% Vol., en el caso de los tintos, o de 11% Vol., en el caso de los blancos y rosados.

---

Result 5 | cite as [rd_1363_2011_etiquetado, Artículo 21] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 21. Términos tradicionales.
1. En aplicación del artículo 70.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, los términos tradicionales a los que se refiere la letra a) del apartado 1 del artículo 118 duovicies del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007, que, para España, se incluyen en la base de datos electrónica E-Bacchus de la Unión Europea, se indicarán en las etiquetas con caracteres cuyas dimensiones no superen a los que indiquen el nombre geográfico.
2. Igualmente, los términos tradicionales: «crianza», «reserva», y «gran reserva» se indicarán en caracteres de tamaño igual o inferior al de los utilizados en el nombre geográfico.

</details>

---

## q30 (multi)

**Question:** Quiero poner «Tempranillo» en la etiqueta de mi Rioja tinto: ¿es una variedad autorizada y qué porcentaje mínimo de ella necesito?

**Reference:** Sí, Tempranillo es una variedad tinta autorizada en Rioja; para mencionar una sola variedad, al menos el 85 % del vino debe ser de ella.

**Agent answer:**

El corpus no cubre esta pregunta. El pliego de condiciones de la DOCa Rioja determina las variedades de uva autorizadas (como la Tempranillo), pero no especifica las normas concretas para indicar el nombre de la variedad en el etiquetado del vino tinto.

<details><summary>search: variedades autorizadas Rioja Tempranillo porcentaje minimo</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 3.b.1] | Pliego de condiciones de la DOCa Rioja, page 7
Pliego de condiciones de la DOCa Rioja — Sección 3.b.1. Proporción de variedades por tipos de vino
TINTO En los vinos tintos elaborados con uva desgranada, deberá emplearse, como mínimo, un 95% de uva de las variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. En los vinos tintos elaborados con uva entera, este porcentaje será, como mínimo, del 85 %.
BLANCO En la elaboración de vinos blancos se emplearán exclusivamente uvas de las variedades Viura, Garnacha Blanca, Malvasía, Maturana blanca, Tempranillo blanco, Turruntés, Chardonnay, Sauvignon blanc y Verdejo.
ROSADO Se empleará un mínimo del 25 % de uvas de variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. La mezcla opcional para el supuesto de los vinos rosados deberá realizarse con posterioridad a la entrega o pesada en báscula.
VINO ESPUMOSO DE CALIDAD La elaboración se realizará con uvas de las variedades blancas y/o tintas definidas en el apartado 6.
En la elaboración de vinos espumosos de calidad rosados se empleará un mínimo del 25% de uvas de las variedades de uva tinta definidas en el apartado 6.

---

Result 2 | cite as [pliego_doca_rioja, Sección 6] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 6. Variedades De Uva
La elaboración de los vinos protegidos se realizará exclusivamente con uvas de las variedades siguientes:
TINTAS BLANCAS Tempranillo Garnacha tinta Graciano Mazuelo Maturana tinta Viura Sauvignon blanc Malvasía Verdejo Garnacha Blanca Maturana blanca Chardonnay Tempranillo blanco Turruntés La uva procedente de plantaciones de viñedo efectuadas con anterioridad al 1 de enero de 1956 y con variedades de uva distintas a las que figuran en el Reglamento de la Denominación, pueden ser empleadas en la elaboración de vinos protegidos, en tanto subsistan dichas plantaciones. En el caso de la variedad vinífera Calagraño, las plantaciones han de ser anteriores a 27 de octubre de 1970.

---

Result 3 | cite as [pliego_doca_rioja, Sección 3] | Pliego de condiciones de la DOCa Rioja, page 6
Pliego de condiciones de la DOCa Rioja — Sección 3. Prácticas Específicas Para Elaboración Y Restricciones
IMPUESTAS.

---

Result 4 | cite as [pliego_doca_rioja, Sección 5] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 5. Rendimiento Máximo
La producción máxima admitida por hectárea será de 6.500 kg de uva, equivalente a 45,5 Hl para las variedades tintas, y de 9.000 kg, equivalente a 63 Hl para las variedades blancas.
Los rendimientos de producción de uva se contabilizarán de forma separada e independiente para las variedades tintas y para las variedades blancas, sin que quepa compensación de colores.
La producción máxima admitida por hectárea en el caso de uva destinada a la elaboración de vinos con reconocimiento de la entidad geográfica menor ‘viñedo singular’, será de 5.000 kg de uva, equivalente a 32,50 Hl para las variedades tintas, y de 6.922 kg, equivalente a 44,99 Hl para las variedades blancas. Este rendimiento no podrá ser modificado en ningún caso.

---

Result 5 | cite as [pliego_doca_rioja, Sección 3.b.2] | Pliego de condiciones de la DOCa Rioja, page 8
Pliego de condiciones de la DOCa Rioja — Sección 3.b.2. Características de la uva
Se dedicarán exclusivamente a la elaboración de vinos protegidos partidas de uva sana con un grado alcohólico volumétrico (% Vol.) natural mínimo de 11 % Vol. para las uvas tintas y de 10,5 % Vol. para las uvas blancas, separando las uvas tintas de las blancas en cada entrega parcial o pesada en báscula.
Se dedicarán exclusivamente a la elaboración de vinos espumosos de calidad partidas de uva sana con un grado alcohólico volumétrico (% vol.) natural mínimo de 9,5 % vol. tanto para las uvas tintas como para las uvas blancas, separando las uvas tintas de las blancas en cada entrega parcial o pesada en báscula.

</details>

<details><summary>search: mencion variedad Tempranillo etiquetado Rioja porcentaje</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 3.b.1] | Pliego de condiciones de la DOCa Rioja, page 7
Pliego de condiciones de la DOCa Rioja — Sección 3.b.1. Proporción de variedades por tipos de vino
TINTO En los vinos tintos elaborados con uva desgranada, deberá emplearse, como mínimo, un 95% de uva de las variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. En los vinos tintos elaborados con uva entera, este porcentaje será, como mínimo, del 85 %.
BLANCO En la elaboración de vinos blancos se emplearán exclusivamente uvas de las variedades Viura, Garnacha Blanca, Malvasía, Maturana blanca, Tempranillo blanco, Turruntés, Chardonnay, Sauvignon blanc y Verdejo.
ROSADO Se empleará un mínimo del 25 % de uvas de variedades Tempranillo, Garnacha Tinta, Graciano, Mazuelo y Maturana Tinta. La mezcla opcional para el supuesto de los vinos rosados deberá realizarse con posterioridad a la entrega o pesada en báscula.
VINO ESPUMOSO DE CALIDAD La elaboración se realizará con uvas de las variedades blancas y/o tintas definidas en el apartado 6.
En la elaboración de vinos espumosos de calidad rosados se empleará un mínimo del 25% de uvas de las variedades de uva tinta definidas en el apartado 6.

---

Result 2 | cite as [pliego_doca_rioja, Sección 6] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 6. Variedades De Uva
La elaboración de los vinos protegidos se realizará exclusivamente con uvas de las variedades siguientes:
TINTAS BLANCAS Tempranillo Garnacha tinta Graciano Mazuelo Maturana tinta Viura Sauvignon blanc Malvasía Verdejo Garnacha Blanca Maturana blanca Chardonnay Tempranillo blanco Turruntés La uva procedente de plantaciones de viñedo efectuadas con anterioridad al 1 de enero de 1956 y con variedades de uva distintas a las que figuran en el Reglamento de la Denominación, pueden ser empleadas en la elaboración de vinos protegidos, en tanto subsistan dichas plantaciones. En el caso de la variedad vinífera Calagraño, las plantaciones han de ser anteriores a 27 de octubre de 1970.

---

Result 3 | cite as [pliego_doca_rioja, Sección 8.b.10.3] | Pliego de condiciones de la DOCa Rioja, page 30
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.3. Pruebas de conformidad
Cualquiera que sea el tipo de envase en que se expidan los vinos para el consumo, irán provistos de precintas de garantía, etiquetas o contraetiquetas numeradas, expedidas por el Consejo Regulador, y siempre en forma que no permita una segunda utilización. Deberá existir correspondencia entre las contraetiquetas, etiquetas y elementos de control del Consejo Regulador.
Para los vinos espumosos de calidad, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Método Tradicional”.
Para los vinos procedentes de ‘viñedo singular’, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Viñedo Singular”.
Para los vinos procedentes de zona o de municipio, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas con numeración controlada.
Si concurren las dos indicaciones en el vino o concurren con la de ‘Viñedo Singular’, se utilizará la precinta correspondiente a la unidad geográfica de menor tamaño.
Para los vinos de Crianza, Reserva y Gran Reserva, el Consejo Regulador expedirá contraetiquetas específicas y autorizará la mención de dichas indicaciones en la etiqueta.

---

Result 4 | cite as [pliego_doca_rioja, Sección 8.b.9] | Pliego de condiciones de la DOCa Rioja, page 28
Pliego de condiciones de la DOCa Rioja — Sección 8.b.9. DESIGNACION, ETIQUETADO (parte 1/3)
En las etiquetas de vinos envasados figurará obligatoriamente de forma destacada el nombre de la denominación junto con la mención “Denominación de Origen Calificada” justo debajo de aquél y el sello del Consejo Regulador, además de las menciones obligatorias que se determinen en la normativa y regulación específica, así como en la legislación aplicable. Así mismo podrán figurar las menciones facultativas y unidades geográficas menores en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable, si bien no podrán destacar respecto al nombre de “RIOJA”.
Antes de la puesta en circulación de etiquetas, éstas deberán ser autorizadas por el Consejo Regulador, en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable.
En el etiquetado de los vinos protegidos por la Denominación de Origen Calificada Rioja será obligatoria la indicación de la correspondiente marca comercial.
En el etiquetado deberá figurar obligatoriamente el nombre o razón social de una bodega inscrita. También podrá utilizarse un nombre comercial, en la forma prevista en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado de la expresión “Maceración carbónica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado principal de vinos blancos y rosados de la expresión “Fermentado en barrica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable Se prohíbe la utilización de cualquier tipo de referencia o alusión a las expresiones "barrica" y "madera" en la comercialización, propaganda y etiquetado de los vinos genéricos (sin agotar procesos de crianza).
Únicamente puede aplicarse a un vino el nombre de una zona o municipio cuando el vino proceda exclusivamente de uva de tal zona de producción o municipio, y su elaboración, crianza en su caso y embotellado se realicen en los mismos.

---

Result 5 | cite as [pliego_doca_rioja, Sección 8.b.10.8] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.8. Términos tradicionales
Para la denominación de origen protegida “Rioja” el término tradicional al que se refiere el artículo 118 duovicies. 1a) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, Reglamento único para las OCM, es: “Denominación de Origen Calificada”.
Los términos tradicionales, a los que se refiere el artículo 118 duovicies.1b) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, que pueden utilizarse en los vinos amparados por la denominación de origen calificada “Rioja” son: “Crianza”, “Reserva”, “Gran Reserva”, “Añejo”, “Noble” y “Viejo”.

</details>

---

## q31 (multi)

**Question:** Para un tinto Crianza de Rioja, ¿qué barrica exige el pliego y puedo usar trozos de roble para envejecerlo?

**Reference:** Barrica de roble de unos 225 litros, al menos 1 año, dentro de 2 años naturales de crianza; no se puede usar la mención si se han usado trozos de madera de roble.

**Agent answer:**

Para un vino tinto Crianza de Rioja, la crianza se efectuará en bodegas inscritas durante al menos dos años naturales [pliego_doca_rioja, Sección 3.c]. 
El vino se someterá a un envejecimiento en barrica de roble de 225 litros de capacidad aproximadamente de forma continuada y sin interrupción durante un año, como mínimo, seguido y complementado con envejecimiento en botella [pliego_doca_rioja, Sección 3.c]. 
No se pueden utilizar trozos de madera de roble, ya que estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aun cuando se hayan empleado también en dichos procesos barricas de madera de roble [rd_1363_2011_etiquetado, Artículo 24].

<details><summary>search: Crianza Rioja tinto barrica meses</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 3.c] | Pliego de condiciones de la DOCa Rioja, page 10
Pliego de condiciones de la DOCa Rioja — Sección 3.c. CRIANZA Y ENVEJECIMIENTO DE LOS VINOS
Requisitos para el uso de los términos tradicionales “Crianza”, “Reserva” y “Gran Reserva”:
• Para el término tradicional “Crianza”:
La crianza se efectuará en las bodegas inscritas en el Registro de Bodegas de Crianza durante, al menos, dos años naturales en el caso de los vinos tintos, y de dieciocho meses en el caso de los vinos blancos y rosados.
Los vinos se someterán al sistema tradicional mixto de envejecimiento en barrica de roble de 225 litros de capacidad aproximadamente, de forma continuada y sin interrupción durante un año, como mínimo, para los vinos tintos y durante seis meses, como mínimo, para los vinos blancos y rosados, seguido y complementado con envejecimiento en botella.
El Consejo Regulador podrá adoptar acuerdos relativos al inicio del cómputo del período de envejecimiento de los vinos
• Para el término tradicional “Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de treinta y seis meses, como mínimo, con una duración mínima de crianza en barrica de roble de doce meses, seguida y complementada con un envejecimiento mínimo en botella de seis meses.
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 24 meses Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de veinticuatro meses, como mínimo, con una duración mínima de crianza en barrica de roble de seis meses.
• Para el término tradicional “Gran Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de sesenta meses, como mínimo, con una duración mínima de crianza en barrica de roble de veinticuatro meses seguida y complementada con un envejecimiento mínimo en botella de veinticuatro meses.
Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de cuarenta y ocho meses, como mínimo, con una duración mínima de envejecimiento en barrica de roble de seis meses.
• Requisitos para el uso de la mención “Gran Añada”:
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 36 meses. La mención deberá ir acompañada del año de la cosecha.

---

Result 2 | cite as [pliego_doca_rioja, Sección 8.b.10.11] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.11. Instalaciones de envejecimiento o crianza del vino
Las instalaciones en las que se realice la actividad de envejecimiento o crianza del vino con derecho a la Denominación de Origen Calificada Rioja, deberán estar exentas de trepidaciones, con temperatura constante y fresca durante todo el año y con estado higrométrico y ventilación adecuados. A este respecto, la temperatura en la nave de barricas estará comprendida entre 10ºC y 18ºC; y el estado higrométrico deberá estar entre 60% y 90% de humedad.
Las instalaciones deberán tener unas existencias mínimas de 225 hectolitros o en proceso de envejecimiento, de los que la mitad, al menos, deberán estar contenidos en un mínimo de 50 barricas de roble de 225 litros de capacidad aproximada.

---

Result 3 | cite as [pliego_doca_rioja, Sección 8.b.10.8] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.8. Términos tradicionales
Para la denominación de origen protegida “Rioja” el término tradicional al que se refiere el artículo 118 duovicies. 1a) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, Reglamento único para las OCM, es: “Denominación de Origen Calificada”.
Los términos tradicionales, a los que se refiere el artículo 118 duovicies.1b) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, que pueden utilizarse en los vinos amparados por la denominación de origen calificada “Rioja” son: “Crianza”, “Reserva”, “Gran Reserva”, “Añejo”, “Noble” y “Viejo”.

---

Result 4 | cite as [rd_1363_2011_etiquetado, Artículo 24] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 24. Menciones relativas al envejecimiento del vino con denominación de origen protegida en recipientes de madera.
1. De acuerdo con el artículo 66.2 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, para indicar que el vino con denominación de origen protegida ha sido criado o envejecido en barrica de madera de roble, además de las indicaciones que figuran en el anexo XVI del citado reglamento, se podrán utilizar los términos tradiciones «crianza», «reserva» y «gran reserva» contemplados, para España, en el la base de datos electrónica E-Bacchus de la Unión Europea.
2. Estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aún cuando se hayan empleado también en dichos procesos barricas de madera de roble.

---

Result 5 | cite as [pliego_doca_rioja, Sección 2.b] | Pliego de condiciones de la DOCa Rioja, page 5
Pliego de condiciones de la DOCa Rioja — Sección 2.b. CARACTERÍSTICAS ORGANOLÉPTICAS (parte 1/2)
La calificación organoléptica se referirá, principalmente, a la tipicidad, color, limpidez, olor, sabor y calidad del vino, teniendo en cuenta el momento del proceso productivo en que se encuentra la muestra.
VINO BLANCO JOVEN Vista: Amarillo pajizo con ribetes verde limón, limpio y brillante.
Olfato: Aromas frutales, florales o vegetales típicos de la variedad.
Boca: Acidez presente con sensación de frescor.
VINO BLANCO CON CRIANZA Vista: Amarillo pajizo con ribetes verde dorado, limpio y brillante.
Olfato: Floral o frutal ensamblado con aromas de madera de roble (vainilla, tostados y ahumados).
Boca: Vinos con acidez bien integrada con los tostados de la madera.
VINO ROSADO JOVEN Vista: Fresa con ribetes frambuesa, brillante, limpio.
Olfato: Aromas a fruta fresca o florales.
Boca: Equilibrio acidez/ fruta con sensación de frescor.
VINO ROSADO CON CRIANZA Vista: Rosa con ribetes salmón.
Olfato: Aromas frutales o florales ensamblados con aromas de madera de roble (vainilla, tostados y ahumados).
Boca: Vinos con acidez bien integrada con los tostados de la madera.
VINO TINTO JOVEN Vista: Púrpura con tonos violáceos.
Olfato: Aromas afrutados o florales varietales.
Boca: Sabroso con equilibrio acidez / grado / tanino.
VINO TINTO CRIANZA Vista: Rojo granate, cereza.
Olfato: Armonía entre aromas frutales o florales y aromas tostados de madera de roble.
Boca: Buen cuerpo con taninos suaves y sabrosos.
VINO TINTO RESERVA Vista: Rojo cereza picota con ribetes rubí.
Olfato: Complejo, buena integración de la fruta madura y los aromas especiados (vainillas, torrefactos, tabaco).
Boca: Buena estructura y armonía gustativa. Suaves y aterciopelados.
VINO TINTO GRAN RESERVA Vista: Rojo rubí con tonos teja.
Olfato: Gran complejidad e intensidad aromática con notas especiadas (tabaco, torrefactos, frutos secos, clavo, nuez, cedro).
Boca: Suaves, finos, elegantes y persistentes.
VINO ESPUMOSO DE CALIDAD Vino con desprendimiento continuo de dióxido de carbono expresado visualmente en la formación de finas burbujas en el momento de su servicio para el consumo.
El vino espumoso de calidad, así como su vino base tras su primera fermentación, será limpio, sin partículas en suspensión y de color amarillo y rosado en sus diferentes tonalidades.

</details>

---

## q32 (multi)

**Question:** Si embotello Rioja fuera de una bodega autorizada, ¿qué pierdo según el pliego y en cuánto prescribe una infracción grave según la Ley 6/2015?

**Reference:** El vino pierde el derecho a usar la denominación; las infracciones graves prescriben a los dos años.

**Agent answer:**

Si se embotella vino amparado por la denominación de origen calificada Rioja fuera de las bodegas inscritas autorizadas por el Consejo Regulador, el vino pierde el derecho al uso de la denominación [pliego_doca_rioja, Sección 8.b.10.5]. 

Las infracciones graves prescriben a los dos años, a contar desde la fecha de comisión de la infracción [ley_6_2015_dop_igp, Artículo 37].

<details><summary>search: embotellado fuera de bodega autorizada Rioja pliego</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 8.b.10.5] | Pliego de condiciones de la DOCa Rioja, page 31
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.5. Embotellado en origen y otros requisitos de embotellado
El embotellado de vinos amparados por la denominación de origen calificada Rioja deberá ser realizado exclusivamente en las bodegas inscritas autorizadas por el Consejo Regulador, perdiendo el vino en otro caso el derecho al uso de la denominación.
Este requisito se establece al constatar que el riesgo para la calidad del vino finalmente ofrecido al consumo es más elevado cuando el vino ha sido transportado y embotellado fuera de la zona de producción que cuando estas operaciones se realizan en dicha zona. Sirve para proteger la gran reputación del vino de Rioja mediante un reforzamiento del control de sus características particulares y de su calidad protegiendo la denominación de origen calificada de la que es beneficiaria la colectividad de productores afectados. La decisión fue reconocida por sentencia del Tribunal de Justicia de la Unión Europea de 16 de mayo de 2000.
Los vinos amparados únicamente pueden circular y ser expedidos en los tipos de envase que no perjudiquen su calidad o prestigio y aprobados por el Consejo Regulador. Con carácter general los envases deberán ser de vidrio, de las capacidades autorizadas por la Unión Europea a excepción de la gama de un litro.
Excepcionalmente, el Consejo Regulador podrá autorizar para usos especiales otros tipos de envase, que entienda no perjudican la calidad o prestigio de los vinos protegidos.
No se permitirán embotellados por encargo en los casos de vinos procedentes de viñedos singulares.

---

Result 2 | cite as [pliego_doca_rioja, Sección 3] | Pliego de condiciones de la DOCa Rioja, page 6
Pliego de condiciones de la DOCa Rioja — Sección 3. Prácticas Específicas Para Elaboración Y Restricciones
IMPUESTAS.

---

Result 3 | cite as [pliego_doca_rioja, Sección 7.a] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 7.a. ÁREA GEOGRÁFICA (parte 6/7)
- las instalaciones de dichas bodegas han de estar claramente separadas de aquellas en las que se producen y almacenan vinos sin derecho a la denominación de origen calificada (artículo 24).
73. Así pues, resulta que, para los vinos de Rioja transportados y embotellados en la zona de producción, los controles son profundos y sistemáticos, son responsabilidad de la colectividad de los propios productores, que tienen un interés primordial en la conservación de la reputación adquirida, y sólo los lotes que hayan sido sometidos a tales controles pueden llevar la denominación de origen calificada.
74. De estas afirmaciones se deduce que el riesgo para la calidad del producto finalmente ofrecido al consumo es más elevado cuando dicho producto ha sido transportado y embotellado fuera de la zona de producción que cuando estas operaciones se realizan en dicha zona.
75. Por consiguiente, ha de admitirse que la obligatoriedad del embotellado en origen el requisito controvertido, que tiene como objetivo proteger la gran reputación del vino de Rioja mediante un reforzamiento del control de sus características particulares y de su calidad, está justificado por ser una medida que protege la denominación de origen calificada de la que es beneficiaria la colectividad de productores afectados y que reviste para éstos una importancia decisiva.
77. A este respecto, la denominación de origen calificada no quedaría protegida de forma comparable mediante la obligación, impuesta a los operadores establecidos fuera de la zona de producción, de informar a los consumidores, a través de un etiquetado adecuado, de que el embotellado se ha producido fuera de dicha zona. En efecto, un menoscabo de la calidad del vino embotellado fuera de la zona de producción que fuera consecuencia de la realización de los riesgos derivados del transporte a granel y/o de la operación de embotellado correlativa, podría afectar negativamente a la reputación de todos los vinos comercializados bajo la denominación de origen calificada Rioja, incluidos los embotellados en la zona de producción bajo el control de la colectividad titular de la denominación.

---

Result 4 | cite as [pliego_doca_rioja, Sección 8.b.10.3] | Pliego de condiciones de la DOCa Rioja, page 30
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.3. Pruebas de conformidad
Cualquiera que sea el tipo de envase en que se expidan los vinos para el consumo, irán provistos de precintas de garantía, etiquetas o contraetiquetas numeradas, expedidas por el Consejo Regulador, y siempre en forma que no permita una segunda utilización. Deberá existir correspondencia entre las contraetiquetas, etiquetas y elementos de control del Consejo Regulador.
Para los vinos espumosos de calidad, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Método Tradicional”.
Para los vinos procedentes de ‘viñedo singular’, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Viñedo Singular”.
Para los vinos procedentes de zona o de municipio, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas con numeración controlada.
Si concurren las dos indicaciones en el vino o concurren con la de ‘Viñedo Singular’, se utilizará la precinta correspondiente a la unidad geográfica de menor tamaño.
Para los vinos de Crianza, Reserva y Gran Reserva, el Consejo Regulador expedirá contraetiquetas específicas y autorizará la mención de dichas indicaciones en la etiqueta.

---

Result 5 | cite as [pliego_doca_rioja, Sección 8.b.10.6] | Pliego de condiciones de la DOCa Rioja, page 31
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.6. Correspondencia entre entradas y salidas
El vino expedido por cada bodega inscrita deberá estar de acuerdo en todo caso con las cantidades de uva adquirida, existencias de campañas anteriores y adquisiciones de vinos o mostos a otras firmas inscritas.
De las existencias de vino en crianza o envejecimiento en cada bodega sólo podrán expedirse aquellos vinos que hayan cumplido los requisitos establecidos en el pliego de condiciones.

</details>

<details><summary>search: prescripción infracción grave Ley 6/2015</summary>

Result 1 | cite as [ley_6_2015_dop_igp, Artículo 37] | Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada), page 22
Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada) — Artículo 37. Prescripción y caducidad.
1. Las infracciones muy graves prescribirán a los tres años, las graves a los dos años, y las leves al año, a contar desde la fecha de comisión de la infracción.
2. Las sanciones impuestas por infracciones muy graves prescribirán a los tres años; las impuestas por infracciones graves a los dos años; y las impuestas por infracciones leves al año, a contar desde el día siguiente a aquel en que adquiera firmeza la resolución por la que se impone la sanción.
3. Caducará la acción para perseguir infracciones cuando conocida por la Administración la existencia de una infracción y finalizadas las diligencias dirigidas al esclarecimiento de los hechos, hubiera transcurrido un año sin que la autoridad competente hubiera ordenado incoar ningún procedimiento en relación con la infracción. En caso de caducidad del procedimiento este apartado no será de aplicación.
A estos efectos, cuando exista toma de muestras, las actuaciones de la inspección se entenderán finalizadas después de practicado el análisis inicial.
Las solicitudes de análisis contradictorios y dirimentes que fueren necesarios, interrumpirán los plazos de caducidad hasta que se practiquen.
4. El plazo máximo para resolver el procedimiento sancionador y notificar la resolución expresa del procedimiento sancionador por las infracciones establecidas en la presente ley será de diez meses.
5. La toma de muestras y análisis efectuados, así como los actos, documentos y trámites cuyo contenido se hubiere mantenido igual de no haber caducado el procedimiento anterior, podrán conservarse y surtir efectos en el nuevo procedimiento sancionador.

---

Result 2 | cite as [ley_6_2015_dop_igp, Artículo 31] | Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada), page 18
Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada) — Artículo 31. Infracciones graves. (parte 1/2)
1. Se consideran infracciones graves las siguientes:
a) La falta de los registros o libros-registro o documentos de acompañamiento, declaraciones o, en general, cualquier documentación que fuera preceptiva, así como los errores, inexactitudes u omisiones en ellos que afecten a las características de los productos o mercancías consignados.
b) Las inexactitudes o errores de cantidad en los registros, los documentos de acompañamiento, las declaraciones, o en general, en la documentación que fuera preceptiva, cuando la diferencia entre la cantidad consignada y la real supere un cinco por ciento.
c) El retraso en las anotaciones de los registros, en la presentación de declaraciones y en general de la documentación que fuera preceptiva cuando haya transcurrido más de un mes desde la fecha en que debió practicarse el primer asiento no reflejado o la fecha límite para presentar la declaración o documentación.
d) El incumplimiento de la obligación de remitir información o documentación a la Administración competente o al organismo de control en el plazo establecido; la aportación de datos falsos así como la dilación y oposición a la toma de muestras necesarias para la inspección.
e) La falta de etiquetas, la omisión en las mismas de indicaciones obligatorias o su rotulación de forma no indeleble cuando fueren preceptivas para aquellos productos amparados por una DOP o IGP.
f) La utilización en el etiquetado, presentación o publicidad de los productos regulados en esta ley, de denominaciones, indicaciones, calificaciones, expresiones o signos que no cumplan con lo establecido en la normativa específica de la DOP o IGP o induzcan a confusión salvo lo previsto en las infracciones muy graves.
g) El incumplimiento de las normas específicas de la DOP o IGP sobre características, prácticas de producción, elaboración, transformación, conservación, almacenamiento, transporte, etiquetado, envasado o presentación.
h) La tenencia de maquinaria, instalaciones o substancias prohibidas o no autorizadas en el pliego de condiciones cuando sea preceptiva su autorización, para la elaboración o almacenamiento de los productos, en las instalaciones o almacenes de las empresas productoras, elaboradoras o envasadoras.
i) La manipulación o disposición en cualquier forma de mercancías intervenidas cautelarmente sin contar con la preceptiva autorización.

---

Result 3 | cite as [ley_6_2015_dop_igp, Artículo 34] | Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada), page 21
Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada) — Artículo 34. Sanciones.
1. Las infracciones leves serán sancionadas con apercibimiento o multa de hasta 2.000,00 euros, pudiendo rebasarse este importe hasta alcanzar el valor del beneficio ilícito obtenido o de las mercancías o productos objeto de infracción, correspondiente al ejercicio económico inmediatamente anterior al de la iniciación del procedimiento sancionador.
2. Las infracciones graves serán sancionadas con multa comprendida entre 2.000,01 y 30.000,00 euros, pudiendo rebasarse esta cantidad hasta alcanzar el quíntuplo del valor del beneficio ilícito obtenido, o de las mercancías o productos objeto de infracción, correspondiente al ejercicio económico inmediatamente anterior al de la iniciación del procedimiento sancionador.
3. Las infracciones muy graves serán sancionadas con multa comprendida entre 30.000,01 y 300.000 euros, pudiendo rebasarse esta cantidad hasta alcanzar el décuplo del valor del beneficio ilícito obtenido, o de las mercancías o productos objeto de infracción, correspondiente al ejercicio económico inmediatamente anterior al de la iniciación del procedimiento sancionador.
4. Los límites mínimos de las sanciones establecidos en los apartados anteriores, podrán ser reducidos hasta en un cincuenta por cien, cuando de las circunstancias económicas del infractor se dedujera que la sanción es demasiado onerosa para él en virtud del volumen o valor de la mercancía afectada por la infracción y del volumen de ventas o producción y la posición de la empresa infractora en el sector, no se hubieran producido graves efectos perjudiciales para los intereses de los consumidores y no existiera reincidencia.
5. Cuando las infracciones graves sean cometidas por operadores acogidos a DOP o IGP y afecten a éstas, podrá imponerse como sanción accesoria la pérdida temporal del uso de las mismas por un plazo máximo de tres años. Si se tratase de infracciones muy graves, podrá imponerse como sanción accesoria la pérdida temporal por un plazo máximo de cinco años.
6. Las sanciones previstas en esta ley serán compatibles con la pérdida o retirada de derechos económicos previstos en la normativa europea o nacional.

---

Result 4 | cite as [ley_6_2015_dop_igp, Artículo 26] | Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada), page 16
Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada) — Artículo 26. Principios generales.
1. A los efectos de esta ley, se considerarán infracciones administrativas las que se tipifican en los artículos siguientes como leves, graves y muy graves.
2. El ejercicio de la potestad sancionadora en ejecución de lo dispuesto en esta ley corresponderá al Ministerio de Agricultura, Alimentación y Medio Ambiente siendo conforme a lo dispuesto en el capítulo II del título IX de la Ley 30/1992, de 26 de noviembre, de Régimen Jurídico de las Administraciones Públicas y del Procedimiento Administrativo Común.
3. Cuando los servicios del Ministerio de Agricultura, Alimentación y Medio Ambiente en el ejercicio de sus funciones de control oficial aprecien que pudiera existir riesgos para la salud de las personas, la salud animal y vegetal, incluido el material de reproducción vegetal, el medio ambiente o incumplimiento de la legislación en materia de calidad comercial o consumo, trasladarán la parte correspondiente de las actuaciones a las autoridades competentes.

---

Result 5 | cite as [ley_24_2003_vina_vino, Artículo 45] | Ley 24/2003 de la Viña y del Vino (consolidada), page 17
Ley 24/2003 de la Viña y del Vino (consolidada) — Artículo 45. Prescripción de las infracciones y sanciones.
1. Las infracciones muy graves prescribirán a los tres años, las graves a los dos años, y las leves al año.
2. Las sanciones impuestas por infracciones muy graves prescribirán a los tres años; las impuestas por infracciones graves a los dos años ; y las impuestas por infracciones leves al año.

</details>

---

## q33 (unanswerable)

**Question:** ¿Cuánto tiempo mínimo en barrica necesita un vino Crianza de Ribera del Duero?

**Reference:** El corpus no cubre esta pregunta: solo incluye el pliego de Rioja, no el de Ribera del Duero.

**Agent answer:**

El corpus no cubre esta pregunta. Esta parte no está en el corpus: El pliego de condiciones de Ribera del Duero no está incluido en los documentos disponibles.

<details><summary>search: Ribera del Duero Crianza tiempo barrica</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 3.c] | Pliego de condiciones de la DOCa Rioja, page 10
Pliego de condiciones de la DOCa Rioja — Sección 3.c. CRIANZA Y ENVEJECIMIENTO DE LOS VINOS
Requisitos para el uso de los términos tradicionales “Crianza”, “Reserva” y “Gran Reserva”:
• Para el término tradicional “Crianza”:
La crianza se efectuará en las bodegas inscritas en el Registro de Bodegas de Crianza durante, al menos, dos años naturales en el caso de los vinos tintos, y de dieciocho meses en el caso de los vinos blancos y rosados.
Los vinos se someterán al sistema tradicional mixto de envejecimiento en barrica de roble de 225 litros de capacidad aproximadamente, de forma continuada y sin interrupción durante un año, como mínimo, para los vinos tintos y durante seis meses, como mínimo, para los vinos blancos y rosados, seguido y complementado con envejecimiento en botella.
El Consejo Regulador podrá adoptar acuerdos relativos al inicio del cómputo del período de envejecimiento de los vinos
• Para el término tradicional “Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de treinta y seis meses, como mínimo, con una duración mínima de crianza en barrica de roble de doce meses, seguida y complementada con un envejecimiento mínimo en botella de seis meses.
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 24 meses Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de veinticuatro meses, como mínimo, con una duración mínima de crianza en barrica de roble de seis meses.
• Para el término tradicional “Gran Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de sesenta meses, como mínimo, con una duración mínima de crianza en barrica de roble de veinticuatro meses seguida y complementada con un envejecimiento mínimo en botella de veinticuatro meses.
Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de cuarenta y ocho meses, como mínimo, con una duración mínima de envejecimiento en barrica de roble de seis meses.
• Requisitos para el uso de la mención “Gran Añada”:
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 36 meses. La mención deberá ir acompañada del año de la cosecha.

---

Result 2 | cite as [pliego_doca_rioja, Sección 8.b.10.11] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.11. Instalaciones de envejecimiento o crianza del vino
Las instalaciones en las que se realice la actividad de envejecimiento o crianza del vino con derecho a la Denominación de Origen Calificada Rioja, deberán estar exentas de trepidaciones, con temperatura constante y fresca durante todo el año y con estado higrométrico y ventilación adecuados. A este respecto, la temperatura en la nave de barricas estará comprendida entre 10ºC y 18ºC; y el estado higrométrico deberá estar entre 60% y 90% de humedad.
Las instalaciones deberán tener unas existencias mínimas de 225 hectolitros o en proceso de envejecimiento, de los que la mitad, al menos, deberán estar contenidos en un mínimo de 50 barricas de roble de 225 litros de capacidad aproximada.

---

Result 3 | cite as [rd_1363_2011_etiquetado, Artículo 24] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 24. Menciones relativas al envejecimiento del vino con denominación de origen protegida en recipientes de madera.
1. De acuerdo con el artículo 66.2 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, para indicar que el vino con denominación de origen protegida ha sido criado o envejecido en barrica de madera de roble, además de las indicaciones que figuran en el anexo XVI del citado reglamento, se podrán utilizar los términos tradiciones «crianza», «reserva» y «gran reserva» contemplados, para España, en el la base de datos electrónica E-Bacchus de la Unión Europea.
2. Estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aún cuando se hayan empleado también en dichos procesos barricas de madera de roble.

---

Result 4 | cite as [pliego_doca_rioja, Sección 7.c] | Pliego de condiciones de la DOCa Rioja, page 20
Pliego de condiciones de la DOCa Rioja — Sección 7.c. NEXO CAUSAL ENTRE LA ZONA GEOGRÁFICA Y LAS CARACTERÍSTICAS (parte 2/2)
La antiquísima actividad vitivinícola y la trascendencia del vino en la región, cuyo impacto económico se sitúa en el 20% de su Producto Interior Bruto, ha supuesto que la dependencia para la sostenibilidad haya optimizado las ventajas que ofrecen las condiciones naturales que se describen y en particular la especialización en la crianza de los vinos hasta culminar una de las mayores concentraciones de barricas de roble en el mundo.
VINOS ESPUMOSOS DE CALIDAD.
El hecho de que la Denominación se encuentre enclavada en una zona fresca según la integral térmica de Winkler contribuye a ciclos vegetativos cortos que culminan una correcta maduración fenólica sin alcanzar graduaciones elevadas, extremos que constituyen el punto de partida idóneo para la obtención de estos vinos.

---

Result 5 | cite as [pliego_doca_rioja, Sección 2.b] | Pliego de condiciones de la DOCa Rioja, page 5
Pliego de condiciones de la DOCa Rioja — Sección 2.b. CARACTERÍSTICAS ORGANOLÉPTICAS (parte 1/2)
La calificación organoléptica se referirá, principalmente, a la tipicidad, color, limpidez, olor, sabor y calidad del vino, teniendo en cuenta el momento del proceso productivo en que se encuentra la muestra.
VINO BLANCO JOVEN Vista: Amarillo pajizo con ribetes verde limón, limpio y brillante.
Olfato: Aromas frutales, florales o vegetales típicos de la variedad.
Boca: Acidez presente con sensación de frescor.
VINO BLANCO CON CRIANZA Vista: Amarillo pajizo con ribetes verde dorado, limpio y brillante.
Olfato: Floral o frutal ensamblado con aromas de madera de roble (vainilla, tostados y ahumados).
Boca: Vinos con acidez bien integrada con los tostados de la madera.
VINO ROSADO JOVEN Vista: Fresa con ribetes frambuesa, brillante, limpio.
Olfato: Aromas a fruta fresca o florales.
Boca: Equilibrio acidez/ fruta con sensación de frescor.
VINO ROSADO CON CRIANZA Vista: Rosa con ribetes salmón.
Olfato: Aromas frutales o florales ensamblados con aromas de madera de roble (vainilla, tostados y ahumados).
Boca: Vinos con acidez bien integrada con los tostados de la madera.
VINO TINTO JOVEN Vista: Púrpura con tonos violáceos.
Olfato: Aromas afrutados o florales varietales.
Boca: Sabroso con equilibrio acidez / grado / tanino.
VINO TINTO CRIANZA Vista: Rojo granate, cereza.
Olfato: Armonía entre aromas frutales o florales y aromas tostados de madera de roble.
Boca: Buen cuerpo con taninos suaves y sabrosos.
VINO TINTO RESERVA Vista: Rojo cereza picota con ribetes rubí.
Olfato: Complejo, buena integración de la fruta madura y los aromas especiados (vainillas, torrefactos, tabaco).
Boca: Buena estructura y armonía gustativa. Suaves y aterciopelados.
VINO TINTO GRAN RESERVA Vista: Rojo rubí con tonos teja.
Olfato: Gran complejidad e intensidad aromática con notas especiadas (tabaco, torrefactos, frutos secos, clavo, nuez, cedro).
Boca: Suaves, finos, elegantes y persistentes.
VINO ESPUMOSO DE CALIDAD Vino con desprendimiento continuo de dióxido de carbono expresado visualmente en la formación de finas burbujas en el momento de su servicio para el consumo.
El vino espumoso de calidad, así como su vino base tras su primera fermentación, será limpio, sin partículas en suspensión y de color amarillo y rosado en sus diferentes tonalidades.

</details>

---

## q34 (unanswerable)

**Question:** ¿Qué exige Estados Unidos en la etiqueta para exportar allí un vino de Rioja?

**Reference:** El corpus no cubre esta pregunta: solo contiene normativa de la UE y de España.

**Agent answer:**

El corpus no cubre esta pregunta. Las normas del corpus solo regulan las indicaciones y requisitos del etiquetado general y de la DOCa Rioja, pero no contienen las exigencias específicas de Estados Unidos para la importación.

<details><summary>search: Estados Unidos exportar etiqueta Rioja</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 8.b.9] | Pliego de condiciones de la DOCa Rioja, page 28
Pliego de condiciones de la DOCa Rioja — Sección 8.b.9. DESIGNACION, ETIQUETADO (parte 1/3)
En las etiquetas de vinos envasados figurará obligatoriamente de forma destacada el nombre de la denominación junto con la mención “Denominación de Origen Calificada” justo debajo de aquél y el sello del Consejo Regulador, además de las menciones obligatorias que se determinen en la normativa y regulación específica, así como en la legislación aplicable. Así mismo podrán figurar las menciones facultativas y unidades geográficas menores en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable, si bien no podrán destacar respecto al nombre de “RIOJA”.
Antes de la puesta en circulación de etiquetas, éstas deberán ser autorizadas por el Consejo Regulador, en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable.
En el etiquetado de los vinos protegidos por la Denominación de Origen Calificada Rioja será obligatoria la indicación de la correspondiente marca comercial.
En el etiquetado deberá figurar obligatoriamente el nombre o razón social de una bodega inscrita. También podrá utilizarse un nombre comercial, en la forma prevista en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado de la expresión “Maceración carbónica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado principal de vinos blancos y rosados de la expresión “Fermentado en barrica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable Se prohíbe la utilización de cualquier tipo de referencia o alusión a las expresiones "barrica" y "madera" en la comercialización, propaganda y etiquetado de los vinos genéricos (sin agotar procesos de crianza).
Únicamente puede aplicarse a un vino el nombre de una zona o municipio cuando el vino proceda exclusivamente de uva de tal zona de producción o municipio, y su elaboración, crianza en su caso y embotellado se realicen en los mismos.

---

Result 2 | cite as [pliego_doca_rioja, Sección 8.b.10.3] | Pliego de condiciones de la DOCa Rioja, page 30
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.3. Pruebas de conformidad
Cualquiera que sea el tipo de envase en que se expidan los vinos para el consumo, irán provistos de precintas de garantía, etiquetas o contraetiquetas numeradas, expedidas por el Consejo Regulador, y siempre en forma que no permita una segunda utilización. Deberá existir correspondencia entre las contraetiquetas, etiquetas y elementos de control del Consejo Regulador.
Para los vinos espumosos de calidad, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Método Tradicional”.
Para los vinos procedentes de ‘viñedo singular’, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Viñedo Singular”.
Para los vinos procedentes de zona o de municipio, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas con numeración controlada.
Si concurren las dos indicaciones en el vino o concurren con la de ‘Viñedo Singular’, se utilizará la precinta correspondiente a la unidad geográfica de menor tamaño.
Para los vinos de Crianza, Reserva y Gran Reserva, el Consejo Regulador expedirá contraetiquetas específicas y autorizará la mención de dichas indicaciones en la etiqueta.

---

Result 3 | cite as [pliego_doca_rioja, Encabezado] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Encabezado
REGISTRO:
Número de expediente en el registro comunitario: PDO-ES-A0117 Fecha de recepción por la Comisión Europea: 11/11/2011.Fecha de modificación (eliminación restricción uso de marcas): 26/11/2014.
MODIFICACIONES:
Número de expediente en el registro comunitario: PDO-ES-A0117-AM03.
Fecha de modificación (corrección de errores): 29/02/2016.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM04.
Fecha de modificación (uso variedades en blancos y rosados y tiempos de envejecimiento): 14/7/2017.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM05.
Fecha de modificación (viñedo singular, vino espumoso, zona, municipio, intensidad colorante rosados): 15/02/2018.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM06.
Fecha de modificación (inicio computo envejecimiento): 24/09/2018.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM07.
Fecha de modificación (crianza de blancos y rosados): 23/09/2019.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM08.
Fecha de modificación (delimitación de viñedo singular, referencia requisitos mínimos de etiquetado): 31/01/2020 y 05/11/2020.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM09.
Fecha de modificación (plantaciones mixtas, calificación e informes sobre viñedos, delimitación viñedos singulares, condiciones instalaciones envejecimiento): 18-11-2021.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM10.
Fecha de modificación (nuevos tipos de vinos espumosos de calidad, cambios en la vendimia de uvas destinadas a vinos espumosos de calidad, cambios en las descripciones organolépticas, delimitación viñedos singulares, destino exclusivo de la producción de las viñas inscritas en Registro de Viñas a elaboración de vino amparado): 01-05-2023 y 07-06-2023 PLIEGO DE CONDICIONES DE LA DENOMINACIÓN DE ORIGEN PROTEGIDA (Denominación de Origen Calificada) “RIOJA”

---

Result 4 | cite as [pliego_doca_rioja, Sección 8.b.10.5] | Pliego de condiciones de la DOCa Rioja, page 31
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.5. Embotellado en origen y otros requisitos de embotellado
El embotellado de vinos amparados por la denominación de origen calificada Rioja deberá ser realizado exclusivamente en las bodegas inscritas autorizadas por el Consejo Regulador, perdiendo el vino en otro caso el derecho al uso de la denominación.
Este requisito se establece al constatar que el riesgo para la calidad del vino finalmente ofrecido al consumo es más elevado cuando el vino ha sido transportado y embotellado fuera de la zona de producción que cuando estas operaciones se realizan en dicha zona. Sirve para proteger la gran reputación del vino de Rioja mediante un reforzamiento del control de sus características particulares y de su calidad protegiendo la denominación de origen calificada de la que es beneficiaria la colectividad de productores afectados. La decisión fue reconocida por sentencia del Tribunal de Justicia de la Unión Europea de 16 de mayo de 2000.
Los vinos amparados únicamente pueden circular y ser expedidos en los tipos de envase que no perjudiquen su calidad o prestigio y aprobados por el Consejo Regulador. Con carácter general los envases deberán ser de vidrio, de las capacidades autorizadas por la Unión Europea a excepción de la gama de un litro.
Excepcionalmente, el Consejo Regulador podrá autorizar para usos especiales otros tipos de envase, que entienda no perjudican la calidad o prestigio de los vinos protegidos.
No se permitirán embotellados por encargo en los casos de vinos procedentes de viñedos singulares.

---

Result 5 | cite as [pliego_doca_rioja, Sección 8.b.10.10] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.10. Etiquetado y adscripción exclusiva de las marcas utilizadas
Las marcas utilizadas en los etiquetados que incluyan el nombre de un municipio serán exclusivas para el vino con esta procedencia geográfica, para lo cual el titular presentará una declaración responsable relativa a este uso exclusivo de la marca en dichos vinos. De no mediar esta declaración, las etiquetas utilizadas para el vino de municipio serán diferentes de las utilizadas por la bodega para el resto de sus vinos, en orden a evitar la confusión del consumidor.

</details>

---

## q35 (unanswerable)

**Question:** ¿Cuánto cuesta cada contraetiqueta del Consejo Regulador de Rioja?

**Reference:** El corpus no cubre esta pregunta: no recoge precios ni tarifas del Consejo Regulador.

**Agent answer:**

El corpus no cubre esta pregunta. El pliego de condiciones de la DOCa Rioja regula la expedición y el uso de las contraetiquetas y precintas de garantía por parte del Consejo Regulador, pero no especifica su precio de venta [pliego_doca_rioja, Sección 8.b.10.3].

<details><summary>search: contraetiqueta Consejo Regulador Rioja precio cuesta</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 8.b.10.3] | Pliego de condiciones de la DOCa Rioja, page 30
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.3. Pruebas de conformidad
Cualquiera que sea el tipo de envase en que se expidan los vinos para el consumo, irán provistos de precintas de garantía, etiquetas o contraetiquetas numeradas, expedidas por el Consejo Regulador, y siempre en forma que no permita una segunda utilización. Deberá existir correspondencia entre las contraetiquetas, etiquetas y elementos de control del Consejo Regulador.
Para los vinos espumosos de calidad, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Método Tradicional”.
Para los vinos procedentes de ‘viñedo singular’, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas que incluirán la mención “Viñedo Singular”.
Para los vinos procedentes de zona o de municipio, el Consejo Regulador expedirá contraetiquetas y/o precintas específicas con numeración controlada.
Si concurren las dos indicaciones en el vino o concurren con la de ‘Viñedo Singular’, se utilizará la precinta correspondiente a la unidad geográfica de menor tamaño.
Para los vinos de Crianza, Reserva y Gran Reserva, el Consejo Regulador expedirá contraetiquetas específicas y autorizará la mención de dichas indicaciones en la etiqueta.

---

Result 2 | cite as [pliego_doca_rioja, Sección 7.a] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 7.a. ÁREA GEOGRÁFICA (parte 3/7)
Ya en el siglo XX, en 1902, se promulgó una Real Orden que definía el "origen" para su aplicación a los vinos de Rioja. En 1926 se decretó la creación del Consejo Regulador cuya misión era delimitar la zona del Rioja, controlar la expedición de la "precinta de garantía" y recomendar las medidas legales que se tomarían contra los usurpadores y falsificadores del nombre "Rioja". Sin embargo, hasta 1945, este organismo no sería legalmente estructurado.
Finalmente, el Consejo Regulador quedó constituido en 1953, y comenzó así a sentar las bases de una actuación moderna y eficaz.
En la evolución hasta la actualidad del vino de Rioja destaca la aprobación, en 1970, del Reglamento de la Denominación de Origen y de su Consejo Regulador.
Fue en esa fecha cuando este organismo adquirió una estructuración y funciones perfectamente definidas: "La defensa de la Denominación de Origen, la aplicación, el control y fomento de la calidad de los vinos amparados quedaron encomendados, en primer término, al Consejo Regulador".
Tras varias modificaciones del Reglamento por el que se rige el Consejo Regulador, que lo han ido adaptando a las necesidades planteadas en los últimos años, los sistemas de control de calidad se han perfeccionado y a la vez se ha potenciado la promoción.
Después de un largo proceso en el que la Denominación de Origen Rioja apostó siempre por la calidad y el control en origen, este esfuerzo alcanzó su reconocimiento.
El 3 de abril de 1991 una Orden Ministerial otorgó el carácter de Calificada a la Denominación de Origen Rioja, primera en España que posee este rango, de manera que se alcanza el nivel cualitativo más alto de las figuras de calidad reguladas.

---

Result 3 | cite as [pliego_doca_rioja, Sección 8.b.9] | Pliego de condiciones de la DOCa Rioja, page 28
Pliego de condiciones de la DOCa Rioja — Sección 8.b.9. DESIGNACION, ETIQUETADO (parte 1/3)
En las etiquetas de vinos envasados figurará obligatoriamente de forma destacada el nombre de la denominación junto con la mención “Denominación de Origen Calificada” justo debajo de aquél y el sello del Consejo Regulador, además de las menciones obligatorias que se determinen en la normativa y regulación específica, así como en la legislación aplicable. Así mismo podrán figurar las menciones facultativas y unidades geográficas menores en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable, si bien no podrán destacar respecto al nombre de “RIOJA”.
Antes de la puesta en circulación de etiquetas, éstas deberán ser autorizadas por el Consejo Regulador, en las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable.
En el etiquetado de los vinos protegidos por la Denominación de Origen Calificada Rioja será obligatoria la indicación de la correspondiente marca comercial.
En el etiquetado deberá figurar obligatoriamente el nombre o razón social de una bodega inscrita. También podrá utilizarse un nombre comercial, en la forma prevista en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado de la expresión “Maceración carbónica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable.
Se permite la utilización en el etiquetado principal de vinos blancos y rosados de la expresión “Fermentado en barrica”, en las condiciones establecidas en la normativa y regulación específica, así como en la legislación aplicable Se prohíbe la utilización de cualquier tipo de referencia o alusión a las expresiones "barrica" y "madera" en la comercialización, propaganda y etiquetado de los vinos genéricos (sin agotar procesos de crianza).
Únicamente puede aplicarse a un vino el nombre de una zona o municipio cuando el vino proceda exclusivamente de uva de tal zona de producción o municipio, y su elaboración, crianza en su caso y embotellado se realicen en los mismos.

---

Result 4 | cite as [pliego_doca_rioja, Sección 9.b] | Pliego de condiciones de la DOCa Rioja, page 33
Pliego de condiciones de la DOCa Rioja — Sección 9.b. TAREAS Y METODOLOGÍA DE CONTROL
El alcance de la verificación y los métodos de control son los que a continuación se detallan:
Tareas y ámbito Tipo de control BODEGAS -Inspección de instalaciones antes de su inscripción y comprobación de modificaciones. -Registro previo CC.AA.
Sistemático.
VIÑEDOS -Inspección viñedos de 2º año. -Registro previo CC.AA. -Ubicación, superficie, marco, variedad. -Aforo producción.
Sistemático - Apoyo Sistema de Información Geográfica (SIG) e instrumentos de precisión.
Poda. Aleatorio basado en análisis de riesgos.
Riego. Aleatorio basado en análisis de riesgos.
Expectativa rendimientos sobre admitido. Aleatorio basado en análisis de riesgos >10%.
Entrega de cosecha de uva:
Cantidad, color, procedencia, grado, sanidad.
Sistemático - Sistema informático de información y transmisión - Acceso web.
VINOS Aforo elaboración anual. Sistemático.
Proceso de calificación.
Toma de muestras elaboración. Sistemático Análisis químico. Sistemático - Lotes < 100.000 litros.
Análisis organoléptico. Sistemático - Lotes < 100.000 litros.
Toma de muestras de almacén de producto terminado.
Aleatorio.
Toma de muestras punto de venta. Aleatorio.
Aforo existencias de vino en bodega Aleatorio - Rotación completa 2 años.
Recuento de documentos de garantía Aleatorio - Rotación completa 2 años.
Control de traslado de vino entre instalaciones Aleatorio > 5%.
DECLARACIONES Existencias y movimientos de vino - Mensual Sistemático.
Exportación - Mensual Sistemático.
Documentos de garantía en poder de la firma
- Trimestral Sistemático.
Documentos de garantía en poder de la firma
- Serie y numeración - Anual Sistemático.
Existencias en almacén de producto terminado
- Anual Sistemático.
OTROS Etiquetados previos a utilización Sistemático.

---

Result 5 | cite as [pliego_doca_rioja, Sección 8.b.10.5] | Pliego de condiciones de la DOCa Rioja, page 31
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.5. Embotellado en origen y otros requisitos de embotellado
El embotellado de vinos amparados por la denominación de origen calificada Rioja deberá ser realizado exclusivamente en las bodegas inscritas autorizadas por el Consejo Regulador, perdiendo el vino en otro caso el derecho al uso de la denominación.
Este requisito se establece al constatar que el riesgo para la calidad del vino finalmente ofrecido al consumo es más elevado cuando el vino ha sido transportado y embotellado fuera de la zona de producción que cuando estas operaciones se realizan en dicha zona. Sirve para proteger la gran reputación del vino de Rioja mediante un reforzamiento del control de sus características particulares y de su calidad protegiendo la denominación de origen calificada de la que es beneficiaria la colectividad de productores afectados. La decisión fue reconocida por sentencia del Tribunal de Justicia de la Unión Europea de 16 de mayo de 2000.
Los vinos amparados únicamente pueden circular y ser expedidos en los tipos de envase que no perjudiquen su calidad o prestigio y aprobados por el Consejo Regulador. Con carácter general los envases deberán ser de vidrio, de las capacidades autorizadas por la Unión Europea a excepción de la gama de un litro.
Excepcionalmente, el Consejo Regulador podrá autorizar para usos especiales otros tipos de envase, que entienda no perjudican la calidad o prestigio de los vinos protegidos.
No se permitirán embotellados por encargo en los casos de vinos procedentes de viñedos singulares.

</details>

---

## q36 (unanswerable)

**Question:** ¿Cuántas botellas de Rioja se vendieron en 2024?

**Reference:** El corpus no cubre esta pregunta: no contiene datos de ventas.

**Agent answer:**

El corpus no cubre esta pregunta. El pliego de condiciones de la DOCa Rioja no contiene datos sobre las ventas o el número de botellas comercializadas en el año 2024.

<details><summary>search: ventas botellas Rioja 2024</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 8.b.10.5] | Pliego de condiciones de la DOCa Rioja, page 31
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.5. Embotellado en origen y otros requisitos de embotellado
El embotellado de vinos amparados por la denominación de origen calificada Rioja deberá ser realizado exclusivamente en las bodegas inscritas autorizadas por el Consejo Regulador, perdiendo el vino en otro caso el derecho al uso de la denominación.
Este requisito se establece al constatar que el riesgo para la calidad del vino finalmente ofrecido al consumo es más elevado cuando el vino ha sido transportado y embotellado fuera de la zona de producción que cuando estas operaciones se realizan en dicha zona. Sirve para proteger la gran reputación del vino de Rioja mediante un reforzamiento del control de sus características particulares y de su calidad protegiendo la denominación de origen calificada de la que es beneficiaria la colectividad de productores afectados. La decisión fue reconocida por sentencia del Tribunal de Justicia de la Unión Europea de 16 de mayo de 2000.
Los vinos amparados únicamente pueden circular y ser expedidos en los tipos de envase que no perjudiquen su calidad o prestigio y aprobados por el Consejo Regulador. Con carácter general los envases deberán ser de vidrio, de las capacidades autorizadas por la Unión Europea a excepción de la gama de un litro.
Excepcionalmente, el Consejo Regulador podrá autorizar para usos especiales otros tipos de envase, que entienda no perjudican la calidad o prestigio de los vinos protegidos.
No se permitirán embotellados por encargo en los casos de vinos procedentes de viñedos singulares.

---

Result 2 | cite as [pliego_doca_rioja, Encabezado] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Encabezado
REGISTRO:
Número de expediente en el registro comunitario: PDO-ES-A0117 Fecha de recepción por la Comisión Europea: 11/11/2011.Fecha de modificación (eliminación restricción uso de marcas): 26/11/2014.
MODIFICACIONES:
Número de expediente en el registro comunitario: PDO-ES-A0117-AM03.
Fecha de modificación (corrección de errores): 29/02/2016.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM04.
Fecha de modificación (uso variedades en blancos y rosados y tiempos de envejecimiento): 14/7/2017.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM05.
Fecha de modificación (viñedo singular, vino espumoso, zona, municipio, intensidad colorante rosados): 15/02/2018.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM06.
Fecha de modificación (inicio computo envejecimiento): 24/09/2018.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM07.
Fecha de modificación (crianza de blancos y rosados): 23/09/2019.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM08.
Fecha de modificación (delimitación de viñedo singular, referencia requisitos mínimos de etiquetado): 31/01/2020 y 05/11/2020.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM09.
Fecha de modificación (plantaciones mixtas, calificación e informes sobre viñedos, delimitación viñedos singulares, condiciones instalaciones envejecimiento): 18-11-2021.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM10.
Fecha de modificación (nuevos tipos de vinos espumosos de calidad, cambios en la vendimia de uvas destinadas a vinos espumosos de calidad, cambios en las descripciones organolépticas, delimitación viñedos singulares, destino exclusivo de la producción de las viñas inscritas en Registro de Viñas a elaboración de vino amparado): 01-05-2023 y 07-06-2023 PLIEGO DE CONDICIONES DE LA DENOMINACIÓN DE ORIGEN PROTEGIDA (Denominación de Origen Calificada) “RIOJA”

---

Result 3 | cite as [pliego_doca_rioja, Sección 7.a] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 7.a. ÁREA GEOGRÁFICA (parte 7/7)
En términos más generales, la mera coexistencia de dos procesos de embotellado diferentes, dentro o fuera de la zona de producción, con o sin el control sistemático efectuado por dicha colectividad, podría reducir el crédito de confianza de que goza la denominación entre los consumidores convencidos de que todas las etapas de producción de un v.c.p.r.d. reputado deben efectuarse bajo el control y la responsabilidad de la colectividad beneficiaria de la denominación.” Con fecha 7 de junio de 2017, el Pleno del Consejo Regulador de la Denominación de Origen Calificada Rioja acordó la inclusión de una nueva categoría de producto que permitirá el amparo de la producción de vinos espumosos blancos y rosados de calidad obtenidos mediante el método tradicional.
La elaboración de vinos espumosos en la región no es novedosa. El historiador D. Manuel Llano Gorostiza ya citaba en su libro titulado Los Vinos de Rioja (1973) la Exposición de Agricultura de Madrid en el año 1857, donde se presentaron algunos vinos de Rioja Alta y Alavesa: “Tintos, blancos y espumosos hechos por el método de Champaña”. Esta mención situaría la primera elaboración de vinos espumosos en España en el año 1857, con un origen riojano.
La elaboración de vinos espumosos en Rioja, vino más tarde de la mano de la sociedad francesa 'Savignon Frères et Cie', establecida en el Barrio de la Estación de Haro en 1857, y que en el año 1890 contrató a un maestro champañero de Reims para desarrollar la elaboración de este tipo de vinos.

---

Result 4 | cite as [pliego_doca_rioja, Sección 4] | Pliego de condiciones de la DOCa Rioja, page 11
Pliego de condiciones de la DOCa Rioja — Sección 4. Delimitación De La Zona Geográfica (parte 2/3)
RIOJA ALTA Comunidad Autónoma de La Rioja Ábalos Camprovín Foncea Matute Tirgo Alesanco Canillas Fonzaleche Medrano Tormantos Alesón Cañas Fuenmayor Nájera Torrecilla sobre Alesanco Anguciana Cárdenas Galbárruli Navarrete Torremontalbo Arenzana de Abajo Casalarreina Gimileo Ochánduri Treviana Arenzana de Arriba Castañares de Rioja Haro Ollauri Tricio Azofra Cellórigo Hervías Rodezno Uruñuela Badarán Cenicero Herramélluri Sajazarra Ventosa Bañares Cidamón Hormilla San Asensio Villalba de Rioja Baños de Río Tobía Cihuri Hormilleja San Millán de Yécora Villar de Torre Baños de Rioja Cirueña Hornos de Moncalvillo San Torcuato Villarejo Berceo Bezares Cordovín Huércanos San Vicente de la Sonsierra Zarratón Bobadilla Cuzcurrita de Río Tirón Lardero Santa Coloma Briñas Daroca de Rioja Leiva Sojuela Briones Entrena Logroño Sorzano Estollo Manjarrés Sotés Provincia de Burgos (Miranda de Ebro) El Ternero (enclave) RIOJA ORIENTAL Comunidad Autónoma de La Rioja Agoncillo Arrúbal Cornago Molinos de Ocón Rincón de Soto Aguilar del Río Ausejo El Redal Murillo de Río Leza Santa Engracia de Jubera (Zona Norte) Alhama Albelda Autol El villar de Arnedo Muro de aguas Santa Eulalia Bajera Alberite Bergasilla Galilea Nalda Tudelilla Alcanadre Bergasa Grávalos Ocón (La Villa) Villamediana de Iregua Aldeanueva de Ebro Calahorra Herce Pradejón Villarroya Alfaro Cervera del Río Alhama Igea Préjano Arnedillo Clavijo Lagunilla de Jubera Quel Arnedo Corera Leza del Río Leza Ribafrecha Comunidad Autónoma de Navarra Andosilla Bargota San Adrián Viana Aras Mendavia Sartaguda Azagra RIOJA ALAVESA Provincia de Álava Baños de Ebro Elvillar de Álava Lanciego Navaridas Villabuena de Álava Barriobusto Labastida Lapuebla de Labarca Oyón Yécora Cripán Labraza Leza Salinillas de Buradón Elciego Laguardia Moreda de Álava Samaniego Los viñedos del municipio de Lodosa, situados en la margen derecha del Ebro, que a fecha 29 de abril de 1991 se hallasen inscritos en el Registro de viñedos del Consejo, mantendrán su inscripción en cuanto subsistan.
Cualquier modificación que se produzca en los límites de los términos municipales incluidos en la zona de producción no llevará aparejada la baja en el Registro de Viñas de los viñedos afectados que se hallen inscritos.
Dentro de la zona de producción se incluyen entidades geográficas menores identificadas como ‘viñedo singular’.

---

Result 5 | cite as [pliego_doca_rioja, Sección 7.c] | Pliego de condiciones de la DOCa Rioja, page 20
Pliego de condiciones de la DOCa Rioja — Sección 7.c. NEXO CAUSAL ENTRE LA ZONA GEOGRÁFICA Y LAS CARACTERÍSTICAS (parte 1/2)
DEL PRODUCTO.
VINOS TRANQUILOS.
Los vinos de uvas procedentes de Rioja Alta se caracterizan por la especial influencia del clima atlántico, que hace que los vinos tengan una graduación media y cuerpo y acidez elevada, consecuencia de lo cual son vinos aptos para el envejecimiento en barrica. Es una zona con menor número de horas de luminosidad durante el ciclo vegetativo que en la zona más meridional de la Denominación y mayor pluviometría, lo que guarda relación directa con su acidez, que consideradas junto a la protección que ejerce la Sierra de Cantabria refuerzan las características descritas, tanto si se elaboran solos como si se ensamblan con vinos procedentes de las otras zonas. En el caso de la zona Rioja Alavesa, la confluencia de climas atlántico y mediterráneo supone que la graduación media sea algo más elevada que la de los anteriores, vinos con algo menos de acidez y más versátiles, en el sentido de que son vinos tanto para un consumo más inmediato como también aptos para el envejecimiento. La protección de la Sierra de Cantabria, al norte, se hace todavía más decisiva. Las horas de luminosidad son similares a las de Rioja Alta, si bien la pluviometría es algo inferior. Su versatilidad alcanza también a la idoneidad para obtener vinos de ensamblaje. Finalmente, en el caso de los vinos procedentes de la Rioja Oriental, observamos una menor pluviometría, un clima marcadamente mediterráneo caracterizado también por una mayor insolación con carácter general, un grado más elevado, extracto e idoneidad para el ensamblaje en vinos dedicados al envejecimiento en barrica, a la vez que ofrece también vinos que pueden ser aptos también para el consumo más inmediato.
La diferente tipología de suelos descubre tres con carácter mayoritario. De un lado los arcillo-calcáreos, situados en la parte más septentrional de la Denominación, que constituyen la fuente fundamental para la crianza, a caballo entre Rioja Alavesa y Rioja Alta, mientras que en esta última zona y en la Rioja Oriental, también aparecen los aluviales y los arcillo-ferrosos, que caracterizan vinos de menor cuerpo que los anteriores.

</details>

---

## q37 (unanswerable)

**Question:** ¿Qué calificación oficial obtuvo la añada 2023 en Rioja?

**Reference:** El corpus no cubre esta pregunta: no incluye calificaciones de añadas.

**Agent answer:**

El corpus no cubre esta pregunta. El pliego de condiciones de la DOCa Rioja no contiene la calificación oficial de la añada 2023.

<details><summary>search: calificacion anada 2023 Rioja</summary>

Result 1 | cite as [pliego_doca_rioja, Encabezado] | Pliego de condiciones de la DOCa Rioja, page 1
Pliego de condiciones de la DOCa Rioja — Encabezado
REGISTRO:
Número de expediente en el registro comunitario: PDO-ES-A0117 Fecha de recepción por la Comisión Europea: 11/11/2011.Fecha de modificación (eliminación restricción uso de marcas): 26/11/2014.
MODIFICACIONES:
Número de expediente en el registro comunitario: PDO-ES-A0117-AM03.
Fecha de modificación (corrección de errores): 29/02/2016.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM04.
Fecha de modificación (uso variedades en blancos y rosados y tiempos de envejecimiento): 14/7/2017.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM05.
Fecha de modificación (viñedo singular, vino espumoso, zona, municipio, intensidad colorante rosados): 15/02/2018.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM06.
Fecha de modificación (inicio computo envejecimiento): 24/09/2018.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM07.
Fecha de modificación (crianza de blancos y rosados): 23/09/2019.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM08.
Fecha de modificación (delimitación de viñedo singular, referencia requisitos mínimos de etiquetado): 31/01/2020 y 05/11/2020.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM09.
Fecha de modificación (plantaciones mixtas, calificación e informes sobre viñedos, delimitación viñedos singulares, condiciones instalaciones envejecimiento): 18-11-2021.
Número de expediente en el registro comunitario: PDO-ES-A0117-AM10.
Fecha de modificación (nuevos tipos de vinos espumosos de calidad, cambios en la vendimia de uvas destinadas a vinos espumosos de calidad, cambios en las descripciones organolépticas, delimitación viñedos singulares, destino exclusivo de la producción de las viñas inscritas en Registro de Viñas a elaboración de vino amparado): 01-05-2023 y 07-06-2023 PLIEGO DE CONDICIONES DE LA DENOMINACIÓN DE ORIGEN PROTEGIDA (Denominación de Origen Calificada) “RIOJA”

---

Result 2 | cite as [pliego_doca_rioja, Sección 7.a] | Pliego de condiciones de la DOCa Rioja, page 14
Pliego de condiciones de la DOCa Rioja — Sección 7.a. ÁREA GEOGRÁFICA (parte 3/7)
Ya en el siglo XX, en 1902, se promulgó una Real Orden que definía el "origen" para su aplicación a los vinos de Rioja. En 1926 se decretó la creación del Consejo Regulador cuya misión era delimitar la zona del Rioja, controlar la expedición de la "precinta de garantía" y recomendar las medidas legales que se tomarían contra los usurpadores y falsificadores del nombre "Rioja". Sin embargo, hasta 1945, este organismo no sería legalmente estructurado.
Finalmente, el Consejo Regulador quedó constituido en 1953, y comenzó así a sentar las bases de una actuación moderna y eficaz.
En la evolución hasta la actualidad del vino de Rioja destaca la aprobación, en 1970, del Reglamento de la Denominación de Origen y de su Consejo Regulador.
Fue en esa fecha cuando este organismo adquirió una estructuración y funciones perfectamente definidas: "La defensa de la Denominación de Origen, la aplicación, el control y fomento de la calidad de los vinos amparados quedaron encomendados, en primer término, al Consejo Regulador".
Tras varias modificaciones del Reglamento por el que se rige el Consejo Regulador, que lo han ido adaptando a las necesidades planteadas en los últimos años, los sistemas de control de calidad se han perfeccionado y a la vez se ha potenciado la promoción.
Después de un largo proceso en el que la Denominación de Origen Rioja apostó siempre por la calidad y el control en origen, este esfuerzo alcanzó su reconocimiento.
El 3 de abril de 1991 una Orden Ministerial otorgó el carácter de Calificada a la Denominación de Origen Rioja, primera en España que posee este rango, de manera que se alcanza el nivel cualitativo más alto de las figuras de calidad reguladas.

---

Result 3 | cite as [pliego_doca_rioja, Sección 8.b.7] | Pliego de condiciones de la DOCa Rioja, page 26
Pliego de condiciones de la DOCa Rioja — Sección 8.b.7. CONDICIONES CUALITATIVAS PARA EL USO DE LA DENOMINACIÓN (parte 1/2)
EN VINOS AMPARADOS. VERIFICACIONES Y ENSAYOS. b.7.1.) Todos los vinos obtenidos en la zona de producción en bodegas inscritas, para poder hacer uso de la denominación de origen calificada Rioja deberán superar un proceso de calificación que verifique las condiciones fisicoquímicas y organolépticas de acuerdo con lo dispuesto en la normativa comunitaria.
El proceso de calificación se efectuará por partida o lote homogéneo y deberá ser realizado de acuerdo con las Normas para la calificación de los vinos con derecho a la Denominación de Origen Calificada Rioja, elaboradas por el Consejo Regulador.
Los vinos que no superen el proceso de calificación se regirán por lo dispuesto en la normativa específica.
La constatación de alteraciones en las cualidades organolépticas de los vinos calificados o del incumplimiento de la legislación aplicable en su elaboración o crianza conllevará su descalificación y la pérdida del derecho al uso de la denominación de la partida afectada, que quedará sometida a las condiciones previstas en la normativa y regulación específica, así como en la legislación aplicable.
La posibilidad de adelanto de calificación se regirá por lo dispuesto en la normativa y regulación específica, así como en la legislación aplicable. b.7.2.) Los vinos de 1ª fermentación con destino a vino espumoso de calidad deberán ser objeto, además del proceso inicial de verificación como partida independiente que compruebe el cumplimiento de las características generales previstas para los vinos protegidos por la Denominación de Origen Calificada ‘Rioja’ en el apartado 2, de una declaración de aptitud de cada partida, consistente en análisis físico-químico y organoléptico, que deberá ser validada por el Consejo Regulador con carácter previo a su salida al mercado.
El vino espumoso de calidad deberá obtener, con carácter previo a su salida al mercado, la valoración de “Bueno” en el análisis organoléptico realizado conforme a Ficha de Cata OIV, y en el caso de Vino espumoso de calidad Reserva o Gran Añada la valoración mínima de “Muy Bueno”. b.7.3.) Vinos procedentes de viñedos singulares.

---

Result 4 | cite as [pliego_doca_rioja, Sección 7.c] | Pliego de condiciones de la DOCa Rioja, page 20
Pliego de condiciones de la DOCa Rioja — Sección 7.c. NEXO CAUSAL ENTRE LA ZONA GEOGRÁFICA Y LAS CARACTERÍSTICAS (parte 1/2)
DEL PRODUCTO.
VINOS TRANQUILOS.
Los vinos de uvas procedentes de Rioja Alta se caracterizan por la especial influencia del clima atlántico, que hace que los vinos tengan una graduación media y cuerpo y acidez elevada, consecuencia de lo cual son vinos aptos para el envejecimiento en barrica. Es una zona con menor número de horas de luminosidad durante el ciclo vegetativo que en la zona más meridional de la Denominación y mayor pluviometría, lo que guarda relación directa con su acidez, que consideradas junto a la protección que ejerce la Sierra de Cantabria refuerzan las características descritas, tanto si se elaboran solos como si se ensamblan con vinos procedentes de las otras zonas. En el caso de la zona Rioja Alavesa, la confluencia de climas atlántico y mediterráneo supone que la graduación media sea algo más elevada que la de los anteriores, vinos con algo menos de acidez y más versátiles, en el sentido de que son vinos tanto para un consumo más inmediato como también aptos para el envejecimiento. La protección de la Sierra de Cantabria, al norte, se hace todavía más decisiva. Las horas de luminosidad son similares a las de Rioja Alta, si bien la pluviometría es algo inferior. Su versatilidad alcanza también a la idoneidad para obtener vinos de ensamblaje. Finalmente, en el caso de los vinos procedentes de la Rioja Oriental, observamos una menor pluviometría, un clima marcadamente mediterráneo caracterizado también por una mayor insolación con carácter general, un grado más elevado, extracto e idoneidad para el ensamblaje en vinos dedicados al envejecimiento en barrica, a la vez que ofrece también vinos que pueden ser aptos también para el consumo más inmediato.
La diferente tipología de suelos descubre tres con carácter mayoritario. De un lado los arcillo-calcáreos, situados en la parte más septentrional de la Denominación, que constituyen la fuente fundamental para la crianza, a caballo entre Rioja Alavesa y Rioja Alta, mientras que en esta última zona y en la Rioja Oriental, también aparecen los aluviales y los arcillo-ferrosos, que caracterizan vinos de menor cuerpo que los anteriores.

---

Result 5 | cite as [pliego_doca_rioja, Sección 8.b.10.8] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.8. Términos tradicionales
Para la denominación de origen protegida “Rioja” el término tradicional al que se refiere el artículo 118 duovicies. 1a) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, Reglamento único para las OCM, es: “Denominación de Origen Calificada”.
Los términos tradicionales, a los que se refiere el artículo 118 duovicies.1b) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, que pueden utilizarse en los vinos amparados por la denominación de origen calificada “Rioja” son: “Crianza”, “Reserva”, “Gran Reserva”, “Añejo”, “Noble” y “Viejo”.

</details>

---

## q38 (unanswerable)

**Question:** ¿Cuánto tiempo de crianza exige la AOC Bordeaux para un vino Grand Cru?

**Reference:** El corpus no cubre esta pregunta: solo contiene normativa española y de la UE sobre etiquetado, no las reglas de las denominaciones francesas.

**Agent answer:**

El corpus no cubre esta pregunta. Las normas sobre denominaciones extranjeras como la AOC Bordeaux quedan fuera del ámbito de nuestra documentación.

<details><summary>search: Grand Cru Bordeaux crianza</summary>

Result 1 | cite as [pliego_doca_rioja, Sección 3.c] | Pliego de condiciones de la DOCa Rioja, page 10
Pliego de condiciones de la DOCa Rioja — Sección 3.c. CRIANZA Y ENVEJECIMIENTO DE LOS VINOS
Requisitos para el uso de los términos tradicionales “Crianza”, “Reserva” y “Gran Reserva”:
• Para el término tradicional “Crianza”:
La crianza se efectuará en las bodegas inscritas en el Registro de Bodegas de Crianza durante, al menos, dos años naturales en el caso de los vinos tintos, y de dieciocho meses en el caso de los vinos blancos y rosados.
Los vinos se someterán al sistema tradicional mixto de envejecimiento en barrica de roble de 225 litros de capacidad aproximadamente, de forma continuada y sin interrupción durante un año, como mínimo, para los vinos tintos y durante seis meses, como mínimo, para los vinos blancos y rosados, seguido y complementado con envejecimiento en botella.
El Consejo Regulador podrá adoptar acuerdos relativos al inicio del cómputo del período de envejecimiento de los vinos
• Para el término tradicional “Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de treinta y seis meses, como mínimo, con una duración mínima de crianza en barrica de roble de doce meses, seguida y complementada con un envejecimiento mínimo en botella de seis meses.
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 24 meses Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de veinticuatro meses, como mínimo, con una duración mínima de crianza en barrica de roble de seis meses.
• Para el término tradicional “Gran Reserva”:
Vinos tintos: Envejecimiento en barrica de roble y botella durante un período total de sesenta meses, como mínimo, con una duración mínima de crianza en barrica de roble de veinticuatro meses seguida y complementada con un envejecimiento mínimo en botella de veinticuatro meses.
Vinos blancos y rosados: Envejecimiento en barrica de roble y botella durante un período total de cuarenta y ocho meses, como mínimo, con una duración mínima de envejecimiento en barrica de roble de seis meses.
• Requisitos para el uso de la mención “Gran Añada”:
Vinos espumosos de calidad: El proceso de elaboración, desde el momento del tiraje hasta el degüelle, no será inferior a 36 meses. La mención deberá ir acompañada del año de la cosecha.

---

Result 2 | cite as [rd_1363_2011_etiquetado, Artículo 24] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 24. Menciones relativas al envejecimiento del vino con denominación de origen protegida en recipientes de madera.
1. De acuerdo con el artículo 66.2 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, para indicar que el vino con denominación de origen protegida ha sido criado o envejecido en barrica de madera de roble, además de las indicaciones que figuran en el anexo XVI del citado reglamento, se podrán utilizar los términos tradiciones «crianza», «reserva» y «gran reserva» contemplados, para España, en el la base de datos electrónica E-Bacchus de la Unión Europea.
2. Estas menciones no podrán utilizarse para designar vinos elaborados con ayuda de trozos de madera de roble, aún cuando se hayan empleado también en dichos procesos barricas de madera de roble.

---

Result 3 | cite as [rd_1363_2011_etiquetado, Artículo 21] | Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado), page 10
Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado) — Artículo 21. Términos tradicionales.
1. En aplicación del artículo 70.3 del Reglamento (CE) n.º 607/2009 de la Comisión, de 14 de julio de 2009, los términos tradicionales a los que se refiere la letra a) del apartado 1 del artículo 118 duovicies del Reglamento (CE) n.º 1234/2007 del Consejo, de 22 de octubre de 2007, que, para España, se incluyen en la base de datos electrónica E-Bacchus de la Unión Europea, se indicarán en las etiquetas con caracteres cuyas dimensiones no superen a los que indiquen el nombre geográfico.
2. Igualmente, los términos tradicionales: «crianza», «reserva», y «gran reserva» se indicarán en caracteres de tamaño igual o inferior al de los utilizados en el nombre geográfico.

---

Result 4 | cite as [ley_6_2015_dop_igp, Disposición adicional segunda] | Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada), page 23
Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada) — Disposición adicional segunda. Indicaciones relativas a las características de los vinos. (parte 2/2)
b) Además de las indicaciones reguladas en el párrafo anterior, los vinos con DOP correspondientes a la categoría 1 del anexo VII, parte II, del Reglamento (UE) 1308/2013 del Parlamento Europeo y del Consejo, de 17 de diciembre, podrán utilizar las siguientes: «Crianza», que podrán utilizar los vinos tintos con un período mínimo de envejecimiento de veinticuatro meses, de los que al menos seis habrán permanecido en barricas de madera de roble de capacidad máxima de 330 litros; y los vinos blancos y rosados con un período mínimo de envejecimiento de dieciocho meses, de los que al menos seis habrán permanecido en barricas de madera de roble de la misma capacidad máxima. «Reserva», que podrán utilizar los vinos tintos con un período mínimo de envejecimiento de treinta y seis meses, de los que habrán permanecido al menos doce en barricas de madera de roble de capacidad máxima de 330 litros, y en botella el resto de dicho período; los vinos blancos y rosados con un período mínimo de envejecimiento de veinticuatro meses, de los que habrán permanecido al menos seis en barricas de madera de roble de la misma capacidad máxima, y en botella el resto de dicho período. «Gran reserva», que podrán utilizar los vinos tintos con un período mínimo de envejecimiento de sesenta meses, de los que habrán permanecido al menos dieciocho en barricas de madera de roble de capacidad máxima de 330 litros, y en botella el resto de dicho período; los vinos blancos y rosados con un período mínimo de envejecimiento de cuarenta y ocho meses, de los que habrán permanecido al menos seis en barricas de madera de roble de la misma capacidad máxima, y en botella el resto de dicho período.
c) Indicaciones propias de los vinos espumosos de calidad. Podrán utilizar las siguientes indicaciones: «Premium» y «reserva», que podrán utilizar los vinos espumosos de calidad definidos en la normativa europea y los vinos espumosos con DOP. «Gran reserva», que podrán utilizar los vinos con DOP «Cava», con un período mínimo de envejecimiento de treinta meses contados desde el tiraje hasta el degüelle.

---

Result 5 | cite as [pliego_doca_rioja, Sección 8.b.10.8] | Pliego de condiciones de la DOCa Rioja, page 32
Pliego de condiciones de la DOCa Rioja — Sección 8.b.10.8. Términos tradicionales
Para la denominación de origen protegida “Rioja” el término tradicional al que se refiere el artículo 118 duovicies. 1a) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, Reglamento único para las OCM, es: “Denominación de Origen Calificada”.
Los términos tradicionales, a los que se refiere el artículo 118 duovicies.1b) del Reglamento (CE) N.º 1234/2007 del Consejo, de 22 de octubre de 2007, que pueden utilizarse en los vinos amparados por la denominación de origen calificada “Rioja” son: “Crianza”, “Reserva”, “Gran Reserva”, “Añejo”, “Noble” y “Viejo”.

</details>
