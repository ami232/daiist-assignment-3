# Blind grading

For each question, grade the agent's answer in `eval/human_labels.csv` (columns `id,correct,supported,notes`) before you look at the judge's verdicts:

- `correct` 1/0: matches your reference answer (for unanswerable questions: a proper refusal).
- `supported` 1/0: every claim is in the retrieved text.
- `notes`: why, for every 0.

Only the passages the answer cites are shown below; the judge saw everything the search tool returned (`eval/answers.jsonl`, field `trace`).

---

## q01 (single)

**Question:** We had to remove a rotten tree from the garden because it was no longer stable. Can I include the cost in the tenants’ service charge statement?

**Your reference answer:** Yes. Felling a rotten tree that is no longer stable counts as garden maintenance under § 2 Nr. 10 BetrKV, so it can be passed on if the lease covers garden maintenance costs (BGH VIII ZR 107/20).

**Agent's answer:**

> **Yes, in principle, you can include the cost**, provided that an agreement transferring operating costs to the tenant exists in the lease.
>
> The Federal Court of Justice (*Bundesgerichtshof*) has specifically addressed this issue:
>
> * **Allocable under garden maintenance (*Gartenpflege*):** According to **BGH VIII ZR 107/20, Leitsatz** (judgment of 2021-11-10), the costs of felling a rotten tree that is no longer structurally stable (*morscher, nicht mehr standsicherer Baum*) are fundamentally allocable costs of garden maintenance (*Gartenpflege*) within the meaning of § 2 Nr. 10 BetrKV. 
> * **Scope of garden maintenance:** Trees are classified as woody plants (*Gehölze*), and garden maintenance encompasses all measures objectively serving to preserve the garden grounds as a whole; this includes removing plants and trees that are diseased, dead, or rotten and no longer safe (**BGH VIII ZR 107/20, Rn. 19–22**).
> * **Not excluded as repair or maintenance (*Instandhaltung und Instandsetzung*):** The costs do not qualify as non-allocable maintenance or repair costs (*Instandhaltungs- und Instandsetzungskosten*) under § 1 Abs. 2 Nr. 2 BetrKV (**BGH VIII ZR 107/20, Rn. 22–25**; **§ 1 BetrKV**). The mere fact that a tree is rotten does not establish a defect in the leased property, nor does the fact that the landlord is fulfilling a public safety obligation (*Verkehrssicherungspflicht*) prevent the cost from being an allocable operating cost (**BGH VIII ZR 107/20, Rn. 23–25**).
>
> ---
>
> ### Crucial Conditions and Dependent Facts:
>
> 1. **Lease allocation clause (*Umlagevereinbarung*):**
>    * Under **§ 556 BGB** (specifically § 556 Abs. 1), operating costs can only be passed on if the lease agreement expressly provides that the tenant bears them. 
>    * It is sufficient if the tenancy agreement includes a standard clause stating that the tenant bears "the operating costs" (*die Betriebskosten*), even without attaching the statutory catalogue or explicitly referencing the statutory provisions (**BGH VIII ZR 137/15, Leitsatz**). 
>    * If the tenancy agreement does not transfer operating costs (or if garden maintenance is specifically excluded), the landlord cannot bill this expense to the tenant.
> 2. **Principle of economic efficiency (*Grundsatz der Wirtschaftlichkeit*):**
>    * The landlord must comply with the statutory requirement of economic efficiency when incurring and billing operating costs (**§ 556 BGB**, specifically § 556 Abs. 3).
>
> ⚠ Citation check: these citations could not be matched to the retrieved passages, verify them before relying on this answer: § 2 Nr. 10 BetrKV

**Cited passages:**

<details><summary>BGH VIII ZR 107/20, Leitsatz</summary>

Die Kosten der Fällung eines - wie hier - morschen, nicht mehr standsicheren Baums sind grundsätzlich umlagefähige Kosten der Gartenpflege im Sinne von § 2 Nr. 10 BetrKV.

</details>

<details><summary>BGH VIII ZR 107/20, Rn. 19–22</summary>

aa) Dies folgt bereits aus dem Wortlaut des § 2 Nr. 10 BetrKV. Zwar sind dort Baumfällarbeiten nicht ausdrücklich genannt. Jedoch sind nach dieser Vorschrift die Kosten der Gartenpflege Betriebskosten im Sinne von § 1 BetrKV und gehören hierzu (unter anderem) die Kosten der Pflege gärtnerisch angelegter Flächen einschließlich der Erneuerung von Pflanzen und Gehölzen.
Zutreffend geht das Berufungsgericht davon aus, dass es sich bei Bäumen sowohl um (verholzte) Pflanzen als auch um Gehölze in diesem Sinne handelt. Denn der Begriff des "Gehölzes" umschreibt nach allgemeinem Sprachgebrauch von dem ersichtlich auch der Verordnungsgeber ausgegangen ist, entweder allgemein eine Pflanze, deren Stamm und Äste verholzen, oder eine geschlossene Ansammlung solcher Pflanzen im Sinne von Wald, Wäldchen, Hain, Hecke oder Gebüsch (vgl. Duden, Das große Wörterbuch der deutschen Sprache, 3. Aufl., Band 3, Stichwort "Gehölz"; siehe auch "Der deutsche Wortschatz von 1600 bis heute", abzurufen unter https://www.dwds.de/wb/Gehölz). Eine Beschränkung auf "Gehölze" einer bestimmten Größe oder Art ergibt sich aus dem Wortlaut des § 2 Nr. 10 BetrKV nicht.
Der Umstand, dass in der Erläuterung des § 2 Nr. 10 BetrKV lediglich die "Erneuerung" von Pflanzen und Gehölzen und nicht deren Entfernung erwähnt wird, steht einer Umlagefähigkeit von (bloßen) Beseitigungskosten nicht entgegen. Denn zum einen unterfällt das Entfernen von Pflanzen und Gehölzen bereits dem (Ober-)Begriff der "Gartenpflege". Hierzu zählen sämtliche Maßnahmen, die objektiv dem Erhalt der Gartenanlage als solche infolge eines Pflegebedarfs dienen. Dies erfordert nicht nur Arbeiten, die dem Erhalt einzelner Pflanzen und Gehölze dienen, sondern auch deren Entfernung, wenn sie krank, abgestorben oder - wie hier im Falle eines Baums - morsch und nicht mehr standsicher sind. Denn solche Umstände beeinträchtigen die Gartenanlage als Ganzes. Zum anderen setzt eine "Erneuerung" von Pflanzen und Gehölzen regelmäßig deren vorherige Entfernung voraus. Daher bedurfte es entgegen der Ansicht der Revision einer ausdrücklichen Nennung der "Entfernung" in § 2 Nr. 10 BetrKV nicht.
bb) Das Berufungsgericht hat ferner zutreffend aus einer systematischen Betrachtung auf die Umlagefähigkeit der Baumfällkosten geschlossen und hierin keine - der Umlagemöglichkeit entzogenen - Instandsetzungskosten im Sinne des § 1 Abs. 2 Nr. 2 BetrKV gesehen.

</details>

<details><summary>§ 1 BetrKV</summary>

(1) Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Sach- und Arbeitsleistungen des Eigentümers oder Erbbauberechtigten dürfen mit dem Betrag angesetzt werden, der für eine gleichwertige Leistung eines Dritten, insbesondere eines Unternehmers, angesetzt werden könnte; die Umsatzsteuer des Dritten darf nicht angesetzt werden.
(2) Zu den Betriebskosten gehören nicht:
1. die Kosten der zur Verwaltung des Gebäudes erforderlichen Arbeitskräfte und Einrichtungen, die Kosten der Aufsicht, der Wert der vom Vermieter persönlich geleisteten Verwaltungsarbeit, die Kosten für die gesetzlichen oder freiwilligen Prüfungen des Jahresabschlusses und die Kosten für die Geschäftsführung (Verwaltungskosten),
2. die Kosten, die während der Nutzungsdauer zur Erhaltung des bestimmungsmäßigen Gebrauchs aufgewendet werden müssen, um die durch Abnutzung, Alterung und Witterungseinwirkung entstehenden baulichen oder sonstigen Mängel ordnungsgemäß zu beseitigen (Instandhaltungs- und Instandsetzungskosten).

</details>

<details><summary>BGH VIII ZR 107/20, Rn. 23–25</summary>

(1) Gemäß § 556 Abs. 1 Satz 2 BGB, § 1 Abs. 1 Satz 1 BetrKV sind Betriebskosten diejenigen Kosten, die dem Eigentümer durch das Eigentum an dem Grundstück oder durch den bestimmungsgemäßen Gebrauch des Gebäudes oder der Wirtschaftseinheit, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Umlagefähige Betriebskosten sind dabei von Kosten der Instandsetzung und Instandhaltung abzugrenzen, die der Vermieter zu tragen hat. Die (nicht als Betriebskosten umlagefähigen) Aufwendungen für Instandsetzung und Instandhaltung werden durch Reparatur und Wiederbeschaffung verursacht und müssen zur Erhaltung des bestimmungsgemäßen Gebrauchs erbracht werden, um die durch Abnutzung, Alterung oder Witterungseinwirkung entstehenden baulichen oder sonstigen Mängel ordnungsgemäß zu beseitigen (§ 1 Abs. 2 Nr. 2 BetrKV). Instandsetzung und Instandhaltung betreffen deshalb Mängel an der Substanz der Immobilie oder ihrer Teile (vgl. Senatsurteile vom 7. April 2004 - VIII ZR 167/03, NZM 2004, 417 unter II 1 a; vom 14. Februar 2007 - VIII ZR 123/06, NJW 2007, 1356 Rn. 10, 14; vom 18. Dezember 2019 - VIII ZR 62/19, NZM 2020, 457 Rn. 12).
(2) Die Kosten der Fällung eines morschen Baums sind nicht deshalb - wie teilweise angenommen wird - Instandhaltungskosten, weil hiermit stets ein Mangel im vorgenannten Sinne beseitigt würde. Denn darin liegt ein unzutreffender pauschaler Schluss von der Morschheit eines Baums auf die Mangelhaftigkeit der Mietsache (Gartenanlage). Die bloße Tatsache, dass ein Baum morsch oder eine Pflanze abgestorben ist, erfüllt grundsätzlich in Anbetracht des Umstands, dass ein Garten aus einer Vielzahl von Pflanzen besteht und eine konkrete Zusammensetzung an Pflanzen regelmäßig nicht geschuldet ist, nicht aus sich heraus die Tatbestandsvoraussetzungen eines Mangels (vgl. zum Mangel der Mietsache Senatsurteile vom 5. Dezember 2018 - VIII ZR 271/17, NJW 2019, 507 Rn. 21; vom 29. April 2020 - VIII ZR 31/18, NJW 2020, 2884 Rn. 24).
Die für die Fällung eines nicht mehr standfesten Baums entstandenen Kosten sind - entgegen einer oben aufgezeigten Ansicht - auch nicht deshalb als Instandhaltungskosten anzusehen, weil der Vermieter durch die Fällung zugleich seiner Verkehrssicherungspflicht genüge. Denn die Erfüllung von Verkehrssicherungspflichten ist als rein haftungsrechtlicher Gesichtspunkt kein maßgebendes Kriterium zur Abgrenzung zwischen Instandhaltungs- und Betriebskosten; vielmehr können auch Kosten für Maßnahmen, die zudem der Wahrnehmung einer Verkehrssicherungspflicht des Vermieters dienen, als Betriebskosten umlagefähig sein (vgl. Senatsurteil vom 14. Februar 2007 - VIII ZR 123/06, NJW 2007, 1356 Rn. 12).

</details>

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>BGH VIII ZR 137/15, Leitsatz</summary>

In der Wohnraummiete genügt zur Übertragung der Betriebskosten auf den Mieter die - auch formularmäßige - Vereinbarung, dass dieser "die Betriebskosten" zu tragen hat. Auch ohne Beifügung des Betriebskostenkatalogs oder ausdrückliche Bezugnahme auf § 556 Abs. 1 Satz 2 BGB und die Betriebskostenverordnung vom 25. November 2003 (BGBl. I. S. 2347) ist damit die Umlage der in § 556 Abs. 1 Satz 2 BGB definierten und in der Betriebskostenverordnung erläuterten Betriebskosten vereinbart.

</details>

---

## q02 (single)

**Question:** The city keeps complaining that our residual waste isn’t sorted properly, so we hired a company to check the bins and re-sort them by hand. Can I pass that cost on to the tenants?

**Your reference answer:** Yes. The cost of an external company checking the residual waste bins and re-sorting them by hand is a waste disposal cost under § 2 Nr. 8 BetrKV (BGH VIII ZR 117/21, LS 1).

**Agent's answer:**

> **Yes**, you can generally pass these costs on to your tenants as operating costs (*Betriebskosten*), provided certain requirements are met.
>
> According to the Federal Court of Justice (*Bundesgerichtshof*), the costs of an external service provider for regularly checking residual waste bins for compliance with waste separation rules and re-sorting waste by hand (*Nachsortierung von Hand*) qualify as allocable waste disposal costs (*Kosten der Müllbeseitigung*) under the Operating Costs Ordinance (**BGH VIII ZR 117/21, Leitsatz**; **BGH VIII ZR 230/21, Rn. 23–26**). Re-sorting costs serve to prepare waste disposal and are categorized as waste disposal costs rather than administrative costs (**BGH VIII ZR 230/21, Rn. 23–26**).
>
> Whether you can pass them on in your specific case depends on the following:
>
> ### 1. Cost allocation clause in the lease (*Umlagevereinbarung*)
> Operating costs can only be billed if the parties agreed to it in the lease agreement (**BGH VIII ZR 117/21, Rn. 27–30**).
> * A clause in the lease agreeing to pass on waste disposal costs (*Kosten der Müllbeseitigung*), or a general reference in the contract to the Operating Costs Ordinance (*Betriebskostenverordnung*), is sufficient to cover these costs (**BGH VIII ZR 117/21, Rn. 27–30**).
> * Because manual re-sorting costs fall under general waste disposal costs, they do not need to be designated as "other operating costs" (*sonstige Betriebskosten*) or listed individually by name in the lease (**BGH VIII ZR 117/21, Rn. 27–30**).
>
> ### 2. Misconduct by individual tenants
> Even if the re-sorting is prompted by incorrect sorting habits or contract-breaching behavior of certain tenants, the costs recur periodically from the rental use of the property and do not count as non-billable administrative costs (*Verwaltungskosten*) (**BGH VIII ZR 117/21, Rn. 24–26**). The required connection to the property exists regardless of whether the measure was triggered by the specific tenant billed or by other tenants or third parties (**BGH VIII ZR 117/21, Rn. 24–26**).
>
> ### 3. Principle of economic efficiency (*Grundsatz der Wirtschaftlichkeit*)
> When contracting an external service provider, you must respect the principle of economic efficiency (*Grundsatz der Wirtschaftlichkeit* / *Wirtschaftlichkeitsgebot*), ensuring an appropriate cost-benefit ratio (**BGH VIII ZR 117/21, Rn. 10, 18–23**; **BGH VIII ZR 230/21, Rn. 23–26**).

**Cited passages:**

<details><summary>BGH VIII ZR 117/21, Leitsatz</summary>

1. Die Kosten eines externen Dienstleisters für die regelmäßige Kontrolle der Restmüllbehälter des Mietobjekts auf Einhaltung der satzungsmäßigen Vorgaben für die Mülltrennung und für die bei fehlerhafter Abfalltrennung erfolgende Nachsortierung von Hand sind im Wohnraummietverhältnis gemäß § 2 Nr. 8 BetrKV auf den Mieter umlegbare Betriebskosten.
2. Die Kosten für die regelmäßige Prüfung und Sicherstellung der Betriebsbereitschaft von in den Mieträumen angebrachten Rauchwarnmeldern sind im Wohnraummietverhältnis als "sonstige Betriebskosten" im Sinne von § 2 Nr. 17 BetrKV auf den Mieter umlegbar. Sie werden von einer vertraglichen Umlagevereinbarung erfasst, welche die Umlage der Kosten des Betriebs von Brandschutz- und Brandmeldeanlagen auf den Mieter vorsieht.
Dem stehen Regelungen in den Bauordnungen der Länder (hier: § 48 Abs. 4 Satz 4 BauO Bln), nach denen (öffentlich-rechtlich) die Wartung dem Mieter obliegt, nicht entgegen.

</details>

<details><summary>BGH VIII ZR 230/21, Rn. 23–26</summary>

2. Mit der von dem Berufungsgericht bisher gegebenen Begründung kann ein Schadensersatzanspruch der Kläger zu 1, 2, 4 und 5 gegen die Beklagte gemäß § 280 Abs. 1 BGB in Verbindung mit § 241 Abs. 2 BGB auf Rückzahlung der aus der Beauftragung der externen Dienstleisterin mit dem Müllmanagement resultierenden Betriebskosten für die Jahre 2016 bis 2018 nicht bejaht werden. Das Berufungsgericht hat den Inhalt der vertraglichen Nebenpflicht des Vermieters, auf ein angemessenes Kosten-Nutzen-Verhältnis bei den Betriebskosten Rücksicht zu nehmen, verkannt. In diesem Zusammenhang hat es überdies eine unzutreffende Verteilung der Darlegungs- und Beweislast zwischen Mieter und Vermieter angenommen.
a) Das Berufungsgericht ist zunächst - unausgesprochen und von den Parteien nicht angegriffen - rechtsfehlerfrei davon ausgegangen, dass die Beklagte nach den zwischen den Parteien getroffenen Vereinbarungen die im Streit stehenden Kosten für das Müllmanagement grundsätzlich als Betriebskosten gemäß § 556 Abs. 1 Satz 1 BGB und dem Betriebskostenkatalog gemäß der dazu erlassenen Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346; im Folgenden: BetrKV) auf die Kläger umlegen kann.
aa) Die Kosten für den Betrieb der chipgesteuerten Müllschleusenanlage als Müllmengenerfassungsanlage und der durch die wiederkehrende Beseitigung von (zu entsorgenden) Beistellungen der Mieter oder Dritter ausgelöste Aufwand sind als Kosten der Müllbeseitigung im Sinne von § 2 Nr. 8 BetrKV dem Grunde nach auf die Kläger umlegbar (vgl. Senatsurteile vom 10. Februar 2016 - VIII ZR 33/15, WuM 2016, 214 Rn. 15; vom 13. Januar 2010 - VIII ZR 137/09, WuM 2010, 153 Rn. 24). Auch die Kosten der Nachsortierung des Abfalls werden als der Vorbereitung der Müllbeseitigung dienende Kosten von § 2 Nr. 8 BetrKV umfasst (vgl. hierzu ausführlich Senatsurteil vom 5. Oktober 2022 - VIII ZR 117/21, NJW-RR 2022, 1593 Rn. 28 ff.; vgl. auch Langenberg/Zehelein, Betriebs- und Heizkostenrecht, 10. Aufl., Teil H Rn. 76; Wall, Betriebs- und Heizkosten-Kommentar, 5. Aufl., Rn. 3879).
bb) Die Kosten für die von der externen Dienstleisterin darüber hinaus vorgenommene Reinigung der Mülltonnenstandplätze sind ebenfalls umlagefähig, wobei dahingestellt bleiben kann, ob es sich hierbei um Kosten nach § 2 Nr. 9 oder Nr. 10 BetrKV handelt (vgl. Langenberg/Zehelein, aaO; Wall, aaO).

</details>

<details><summary>BGH VIII ZR 117/21, Rn. 27–30</summary>

Auch der Einwand der Revision, das vom Berufungsgericht angeführte gesamtgesellschaftliche Interesse an einer optimalen Trennung und Wiederverwertung des Mülls könne einen "Bezug zum einzelnen Mietvertrag" nicht begründen, geht bereits deshalb fehl, weil die Einordnung von Kosten als Betriebskosten nach § 556 Abs. 1 Satz 2 BGB, § 1 Abs. 1 Satz 1 BetrKV einen solchen individuellen Bezug zum Mieter nicht verlangt. Maßgeblich ist vielmehr, dass es sich - wie hier - um Kosten handelt, die durch die Bewirtschaftung des betreffenden Grundstücks im Rahmen der Vermietung entstehen (vgl. hierzu BeckOGK-BGB/Drager, Stand: 1. Juli 2021, § 556 Rn. 65; MünchKomm-BGB/Zehelein, 8. Aufl., § 1 BetrKV Rn. 16; Wall, Betriebs- und Heizkosten-Kommentar, 5. Aufl., Rn. 2905).
cc) Mit Recht hat das Berufungsgericht angenommen, dass die von der Beklagten angesetzten Kosten eines externen Dienstleisters für die Kontrolle der Restmüllbehälter der Liegenschaft auf Einhaltung der satzungsmäßigen Vorgaben für die Mülltrennung und für die bei fehlerhafter Abfalltrennung erfolgende Nachsortierung von Hand - von Anfang an - als "Kosten der Müllbeseitigung" wirksam auf die Kläger umgelegt wurden.
(1) Gemäß § 535 Abs. 1 Satz 3, § 556 Abs. 1, 4 BGB hat der Mieter Betriebskosten zu tragen, wenn die Parteien eine entsprechende Vereinbarung wirksam getroffen haben. Grundsätzlich genügt dafür - wie hier im Mietvertrag enthalten und soweit es nicht um "sonstige" Betriebskosten im Sinne von § 2 Nr. 17 BetrKV geht - eine Verweisung auf die Betriebskostenverordnung (st. Rspr.; vgl. nur Senatsurteile vom 10. Februar 2016 - VIII ZR 137/15, NZM 2016, 235 Rn. 11; vom 18. Dezember 2019 - VIII ZR 62/19, NZM 2020, 457 Rn. 10; jeweils mwN).
(2) Der zwischen den Parteien geschlossene Mietvertrag sieht über die Bezugnahme auf Anlage 4 des Mietvertrags mit einer beispielhaften Auflistung der umlegbaren Betriebskosten und über die zudem enthaltene allgemeine Verweisung auf "alle Betriebskosten" im Sinne von § 2 BetrKV auch eine Umlage von "Kosten der Müllbeseitigung" auf die Kläger vor (Nr. 1 Buchst. f der Anlage 4 des Mietvertrags; § 2 Nr. 8 BetrKV). Diese wirksam getroffene Umlagevereinbarung umfasst - wie das Berufungsgericht zutreffend gewürdigt hat - die in Rede stehenden Kosten unabhängig davon, dass diese erstmals längere Zeit nach dem Vertragsschluss angefallen sind.

</details>

<details><summary>BGH VIII ZR 117/21, Rn. 24–26</summary>

bb) Diese - damit allein zu beurteilenden - Kosten sind grundsätzlich auf den Mieter umlegbare Betriebskosten im Sinne von § 556 Abs. 1 Satz 2 BGB, § 1 Abs. 1 Satz 1 BetrKV. Sie entstehen der Beklagten als Grundstückseigentümerin regelmäßig wiederkehrend durch die Mietnutzung des Grundstücks und sind insbesondere nicht den durch die Grundmiete abgedeckten Verwaltungskosten zuzuordnen (vgl. zur Abgrenzung Senatsurteil vom 18. Dezember 2019 - VIII ZR 62/19, NZM 2020, 457 Rn. 13 ff.).
Dem kann die Revision nicht mit Erfolg entgegenhalten, dass die betreffende Maßnahme eine Reaktion der Beklagten auf ein fehlerhaftes Mülltrennungsverhalten von Teilen der Mieterschaft sei, die diesbezüglichen Kosten also durch ein vertragswidriges Verhalten von Mietern verursacht und demzufolge nicht - wie es § 556 Abs. 1 Satz 2 BGB voraussetze - durch einen bestimmungsgemäßen Gebrauch entstanden seien (so aber auch Wall, Betriebs- und Heizkosten-Kommentar, 5. Aufl., Rn. 3855, 3876, jeweils mwN; Blank/Börstinghaus, Miete, 6. Aufl., § 556 BGB Rn. 7; Schmidt-Futterer/Lehmann-Richter, Mietrecht, 15. Aufl., § 556 BGB Rn. 205; Schmid, WuM 2008, 519 f.; skeptisch, aber im Ergebnis wie hier Sentek, NZM 2017, 721, 723).
Der durch das vorgenannte Merkmal beschriebene erforderliche Bezug der Kosten zur Mietsache (vgl. Senatsurteil vom 10. Februar 2016 - VIII ZR 33/15, NZM 2016, 353 Rn. 13) besteht nach der Senatsrechtsprechung unabhängig davon, ob die von dem Vermieter im Rahmen der ordnungsgemäßen Bewirtschaftung des Grundstücks vorgenommene Maßnahme der Müllbeseitigung auch durch den auf Zahlung von Betriebskosten in Anspruch genommenen Mieter oder allein durch andere Mieter oder Dritte veranlasst wurde und ob deren Verhalten als vertrags- oder rechtswidrig einzuordnen ist (vgl. Senatsurteile vom 13. Januar 2010 - VIII ZR 137/09, NZM 2010, 274 Rn. 24 [zur Beseitigung von unberechtigt abgestelltem Sperrmüll]; vom 10. Februar 2016 - VIII ZR 33/15, aaO Rn. 15 [zur Beseitigung von durch Dritte verursachten Verunreinigungen]; BeckOGK-BGB/Drager, Stand: 1. Juli 2021, § 556 Rn. 65; MünchKomm-BGB/Zehelein, 8. Aufl., § 1 BetrKV Rn. 16).

</details>

<details><summary>BGH VIII ZR 117/21, Rn. 10, 18–23</summary>

Die im Umfang der Zulassung eingelegte Revision der Kläger hat keinen Erfolg.
Diese Beurteilung hält - teilweise nur im Ergebnis - rechtlicher Nachprüfung, soweit sie aufgrund des beschränkten Umfangs der Revisionszulassung eröffnet ist, stand. Die Revision ist daher zurückzuweisen. Das Berufungsgericht hat zu Recht angenommen, dass die Beklagte die bei ihr angefallenen Kosten für Maßnahmen des sogenannten "Behältermanagements" und für die Wartung der Rauchwarnmelder wirksam als Betriebskosten auf die Kläger umgelegt hat und deshalb den Klägern ein Anspruch auf Rückzahlung der für das Jahr 2018 geleisteten Betriebskostenvorauszahlungen gegen die Beklagte insoweit weder aus § 812 Abs. 1 Satz 1 Alt. 1 BGB noch aus einem anderen Rechtsgrund zusteht.
1. Rechtsfehlerfrei - und von der Revision auch nicht beanstandet - ist das Berufungsgericht davon ausgegangen, dass sich die Umlagefähigkeit der in Rede stehenden Kostenpositionen vorliegend nach der Betriebskostenverordnung (BetrKV) richtet.
2. Ohne Rechtsfehler hat das Berufungsgericht auch angenommen, dass die Beklagte die von ihr in der Betriebskostenabrechnung für das Jahr 2018 mit der Bezeichnung "Behältermanagement" entsprechend dem vertraglich vereinbarten Umlageschlüssel angesetzten Kosten in Höhe von 12,09 € verlangen kann, weil sie diese wirksam auf die Kläger umgelegt und durch die kostenpflichtige Beauftragung eines externen Dienstleisters mit den zugrundeliegenden Tätigkeiten nicht gegen den Grundsatz der Wirtschaftlichkeit verstoßen hat.
a) Hierbei ist das Berufungsgericht rechtsfehlerfrei davon ausgegangen, dass es sich bei den geltend gemachten Kosten, deren Anfall bei der Beklagten die Kläger nicht in Abrede stellen, um gemäß Nr. 1 Buchst. f der Anlage 4 zum Mietvertrag, § 2 Nr. 8 BetrKV wirksam auf die Kläger umgelegte Betriebskosten handelt.
aa) Entgegen der Ansicht der Revision stellt sich im Streitfall die von ihr aufgeworfene und als höchst umstritten bezeichnete Frage nicht, inwieweit "Kosten für ein Müllmanagement" angesichts des breiten Spektrums möglicher Dienstleistungen (vgl. die Auflistung bei Sentek, NZM 2017, 721, 722; Wall, Betriebs- und Heizkosten-Kommentar, 5. Aufl., Rn. 3879) und des auf eine Zugehörigkeit zur Verwaltungstätigkeit des Vermieters hindeutenden Begriffs des "Müllmanagements" nach § 2 Nr. 8 BetrKV auf einen Mieter umgelegt werden könnten.
Denn die von der Beklagten in die Betriebskostenabrechnung eingestellten Kosten des externen Dienstleisters sind nach den - von der Revision insoweit nicht angegriffenen - Feststellungen des Berufungsgerichts (allein) für die regelmäßige Kontrolle der Restmüllbehälter der Liegenschaft auf Einhaltung der satzungsmäßigen Vorgaben für die Mülltrennung und für die bei fehlerhafter Abfalltrennung erfolgende Nachsortierung von Hand angefallen.

</details>

---

## q03 (single)

**Question:** We pay a company to check the smoke detectors in the flats every year. The building code says maintenance is the tenant’s responsibility. Can I still bill the tenants for the inspections?

**Your reference answer:** Yes, if the lease covers it. Regular smoke detector inspections are "other operating costs" under § 2 Nr. 17 BetrKV and are covered by a lease clause on fire safety and fire alarm systems. A building code rule making the tenant responsible for maintenance doesn't change this (BGH VIII ZR 117/21).

**Agent's answer:**

> **Yes, in principle you can bill the tenants for the inspection costs**, but whether you can actually do so depends on whether your lease agreement contains a clause allowing these costs to be passed on.
>
> ### 1. State building code rules do not prevent billing
> Provisions in state building codes (*Bauordnungen der Länder*)—under which the maintenance of smoke detectors is assigned to the tenant as an obligation of public law—do not prevent the landlord from arranging the inspections and passing on the recurring costs to the tenant (BGH VIII ZR 117/21, Leitsatz). 
>
> Such building code regulations solely govern the public-law relationship between the building authorities and the obligated party; they do not dictate or alter the civil-law rights and obligations between landlord and tenant under § 535 Abs. 1 Satz 2 BGB (BGH VIII ZR 117/21, Rn. 47–49).
>
> ### 2. A lease agreement (*Umlagevereinbarung*) is required
> The costs of regularly checking and ensuring the operational readiness (*Prüfung und Sicherstellung der Betriebsbereitschaft*) of smoke detectors installed in the rented premises are classified as "other operating costs" (*sonstige Betriebskosten*) pursuant to § 2 Nr. 17 BetrKV (BGH VIII ZR 117/21, Leitsatz; BGH VIII ZR 117/21, Rn. 47–49). 
>
> Because they fall under the category of "other operating costs," they can only be billed to the tenant if the lease agreement contains an express allocation clause (*Umlagevereinbarung*). An agreement that provides for allocating the costs of operating fire protection and fire alarm systems (*Betrieb von Brandschutz- und Brandmeldeanlagen*) covers these inspection and maintenance costs (BGH VIII ZR 117/21, Leitsatz; BGH VIII ZR 117/21, Rn. 61–63).
>
> ### 3. Further limitations
> * **Principle of economic efficiency (*Wirtschaftlichkeitsgebot*):** Hiring an external specialist company for regular maintenance must comply with the statutory principle of economic efficiency under § 556 Abs. 3 Satz 1 Halbs. 2, § 560 Abs. 5 BGB (BGH VIII ZR 117/21, Rn. 61–63).
> * **Equipment rental fees (*Miete von Rauchwarnmeldern*):** While regular inspection and operational checks are billable operating costs, fees for renting the smoke detectors themselves cannot be passed on to tenants as operating costs (BGH VIII ZR 379/20, Leitsatz).
>
> ⚠ Citation check: these citations could not be matched to the retrieved passages, verify them before relying on this answer: § 535 Abs. 1 Satz 2 BGB; § 2 Nr. 17 BetrKV; § 560 Abs. 5 BGB

**Cited passages:**

<details><summary>BGH VIII ZR 117/21, Leitsatz</summary>

1. Die Kosten eines externen Dienstleisters für die regelmäßige Kontrolle der Restmüllbehälter des Mietobjekts auf Einhaltung der satzungsmäßigen Vorgaben für die Mülltrennung und für die bei fehlerhafter Abfalltrennung erfolgende Nachsortierung von Hand sind im Wohnraummietverhältnis gemäß § 2 Nr. 8 BetrKV auf den Mieter umlegbare Betriebskosten.
2. Die Kosten für die regelmäßige Prüfung und Sicherstellung der Betriebsbereitschaft von in den Mieträumen angebrachten Rauchwarnmeldern sind im Wohnraummietverhältnis als "sonstige Betriebskosten" im Sinne von § 2 Nr. 17 BetrKV auf den Mieter umlegbar. Sie werden von einer vertraglichen Umlagevereinbarung erfasst, welche die Umlage der Kosten des Betriebs von Brandschutz- und Brandmeldeanlagen auf den Mieter vorsieht.
Dem stehen Regelungen in den Bauordnungen der Länder (hier: § 48 Abs. 4 Satz 4 BauO Bln), nach denen (öffentlich-rechtlich) die Wartung dem Mieter obliegt, nicht entgegen.

</details>

<details><summary>BGH VIII ZR 117/21, Rn. 47–49</summary>

aa) Wie der Senat bereits für die Kosten der Revision einer Elektroanlage entschieden hat, ist eine regelmäßig anfallende, nicht durch eine bereits aufgetretene Störung veranlasste Maßnahme, die der Überprüfung der Funktionsfähigkeit und Betriebssicherheit einer technischen Einrichtung des Mietobjekts dient, keine Mangelbeseitigung und sind die hierdurch verursachten wiederkehrenden Kosten deshalb als sonstige - grundsätzlich umlegbare - Betriebskosten im Sinne von § 2 Nr. 17 BetrKV anzusehen (vgl. Senatsurteil vom 14. Februar 2007 - VIII ZR 123/06, NZM 2007, 282 Rn. 11 ff.; siehe auch Senatsurteil vom 18. Dezember 2019 - VIII ZR 62/19, NZM 2020, 457 Rn. 18 f. [für Maßnahmen der Kontrolle und Überwachung durch einen Hauswart]).
Entsprechendes gilt für die Kosten, die bei dem Eigentümer eines vermieteten Objekts für die regelmäßige Prüfung und Sicherstellung der Betriebsbereitschaft von in den Mieträumen angebrachten Rauchwarnmeldern wiederkehrend anfallen.
Der von der Revision - im Zusammenhang mit den Rügen gegen die ergänzende Vertragsauslegung durch das Berufungsgericht - herangezogenen Vorschrift des § 48 Abs. 4 Satz 4 BauO Bln lässt sich ein für die Einordnung der Wartungskosten als Betriebskosten maßgeblicher Wertungsgesichtspunkt nicht entnehmen. Soweit danach die Sicherstellung der Betriebsbereitschaft der Rauchwarnmelder den Mietern oder sonstigen Nutzungsberechtigten obliegt, es sei denn, der Eigentümer übernimmt diese Verpflichtung selbst, betrifft dies allein das bauordnungsrechtliche Verhältnis zwischen der Behörde und dem hinsichtlich der Wartung öffentlich-rechtlichen Verpflichteten. Dafür, dass § 48 Abs. 4 Satz 4 BauO Bln eine Bestimmung zur zivilrechtlichen Zuständigkeit des Vermieters aus § 535 Abs. 1 Satz 2 BGB im Verhältnis zum Mieter und zu den beiderseitigen Rechten und Pflichten bezogen auf die Wartung von Rauchwarnmeldern treffen sollte, gibt es keinen Anhaltspunkt (so im Ergebnis auch Langenberg/Zehelein, Betriebs- und Heizkostenrecht, 10. Aufl., Teil A Rn. 308 mwN; Blank/Börstinghaus, Miete, 6. Aufl., § 556 Rn. 100; Zehelein, WuM 2016, 400, 407; Serwe, ZMR 2019, 6, 9; Fritsch, ZMR 2016, 925, 927; siehe auch BGH, Urteil vom 7. Dezember 2018 - V ZR 273/17, NZM 2019, 214 Rn. 10 [kein Eingriff in Aufgabenverteilung bei der Wohnungseigentümergemeinschaft]; aA Wall, WuM 2013, 3, 21; ders., WuM 2016, 482, 483; offen Cramer, ZMR 2016, 505, 506 f.).

</details>

<details><summary>BGH VIII ZR 117/21, Rn. 61–63</summary>

Der Umstand, dass Nr. 1 Buchst. o der Anlage 4 des Mietvertrags von den Kosten des "Betriebs" und nicht ausdrücklich von den Kosten der "Wartung" spricht, steht einem auch diese Kosten umfassenden Verständnis eines redlichen und verständigen Mieters nicht entgegen. Denn der "Betrieb einer Brandschutz- und -meldeanlage" umfasst auch deren notwendige regelmäßige Überprüfung auf ihre Betriebsfähigkeit, mithin deren Wartung (vgl. in diesem Sinne auch die Regelungen in § 2 Nr. 4 Buchst. a BetrKV für die zentrale Heizungsanlage, in § 2 Nr. 7 BetrKV für den Personen- und Lastenaufzug, in § 2 Nr. 15 Buchst. a BetrKV für die Gemeinschaftsantennenanlage oder in § 2 Nr. 16 BetrKV für Einrichtungen für die Wäschepflege). Derartige Kosten für eine regelmäßige Prüfung der Betriebsbereitschaft und -sicherheit können auch nach dem Verständnis eines nicht juristisch vorgebildeten Mieters bei den in Nr. 1 Buchst. o der Anlage 4 des Mietvertrags aufgeführten Brandschutz- und Brandmeldeanlagen anfallen.
c) Rechtsfehlerfrei hat das Berufungsgericht schließlich einen Verstoß gegen das Gebot der Wirtschaftlichkeit gemäß § 556 Abs. 3 Satz 1 Halbs. 2, § 560 Abs. 5 BGB weder in der Durchführung einer regelmäßigen Wartung als solcher noch darin gesehen, dass die Beklagte diesbezüglich einen Fachbetrieb beauftragt hat.
Dass die insoweit entstandenen und von der Beklagten abgerechneten geringfügigen Kosten für die Wartung der Rauchwarnmelder in Höhe von 8,02 € für das Jahr 2018 dem Wirtschaftlichkeitsgebot widersprächen, wird von der Revision nicht geltend gemacht.

</details>

<details><summary>BGH VIII ZR 379/20, Leitsatz</summary>

Bei den Kosten für die Miete von Rauchwarnmeldern handelt es sich nicht um sonstige Betriebskosten im Sinne von § 2 Nr. 17 BetrKV, sondern - da sie den Kosten für den Erwerb von Rauchwarnmeldern gleichzusetzen sind - um betriebskostenrechtlich nicht umlagefähige Aufwendungen.

</details>

---

## q04 (single)

**Question:** A tenant wants to see the bank statements showing we actually paid the invoices, not just the invoices themselves. Do I have to show him those?

**Your reference answer:** Yes. The tenant's right to inspect the receipts includes the payment receipts (Zahlungsbelege) showing the invoices were paid (BGH VIII ZR 118/19).

**Agent's answer:**

> **Yes, you must allow the tenant to inspect the bank statements or proof of payment.**
>
> The relevant rulings established by the Federal Court of Justice (BGH):
>
> * **Scope of inspection:** The tenant's right to inspect the supporting documents of a service charge statement (*Betriebskostenabrechnung*) extends to the underlying payment vouchers and records (*Zahlungsbelege*) (**BGH VIII ZR 118/19, Leitsatz**).
> * **Both invoices and payment records:** The documents subject to the tenant's right of inspection (*Belegeinsicht*) include not only the invoices (*Rechnungen*) but also the associated proof of payment (*Zahlungsbelege*) for the operating costs passed on to the tenant (**BGH VIII ZR 118/19, Rn. 3, 10–15**).
> * **No special interest needed:** The tenant does not need to establish a special interest (*besonderes Interesse*); the general interest in reviewing the landlord's accounting is sufficient (**BGH VIII ZR 118/19, Rn. 3, 10–15**).
> * **Accounting method does not matter:** This right applies regardless of whether the landlord bills according to the cash principle (*Abflussprinzip*) or the service/accrual principle (*Leistungsprinzip*) (**BGH VIII ZR 118/19, Rn. 16–19**).
> * **Right to withhold payment:** As long as the landlord does not grant the requested inspection of the underlying payment records, the tenant holds a temporary right to refuse payment (*temporäres Leistungsverweigerungsrecht*) against the landlord's demand for an additional balance (*Nachforderung*) (**BGH VIII ZR 118/19, Rn. 3, 10–15**).

**Cited passages:**

<details><summary>BGH VIII ZR 118/19, Leitsatz</summary>

Das Recht des Mieters auf Einsicht in die Belege einer Betriebskostenabrechnung erstreckt sich auch auf die zugrundeliegenden Zahlungsbelege.

</details>

<details><summary>BGH VIII ZR 118/19, Rn. 3, 10–15</summary>

Die Revision hat keinen Erfolg.
Diese Beurteilung hält rechtlicher Nachprüfung stand, so dass die Revision zurückzuweisen ist.
Das Berufungsgericht hat die Klage zutreffend mit Rücksicht darauf als derzeit unbegründet abgewiesen, dass die Klägerin dem Beklagten die begehrte Einsicht in die der Betriebskostenabrechnung 2013 zu Grunde liegenden Zahlungsbelege nicht gewährt hat.
1. Nach der Rechtsprechung des Senats, die das Berufungsgericht zutreffend angewendet hat, steht dem Mieter gegenüber dem auf eine Betriebskostenabrechnung gestützten Zahlungsverlangen des Vermieters ein aus § 242 BGB folgendes (temporäres) Leistungsverweigerungsrecht zu, solange ihm eine nach § 259 Abs. 1 BGB berechtigterweise begehrte Belegeinsicht nicht gewährt worden ist (Senatsurteile vom 7. Februar 2018 - VIII ZR 189/17, NJW 2018, 1599 Rn. 29; vom 10. April 2019 - VIII ZR 250/17, NJW-RR 2019, 977 Rn. 36 ff.).
2. Zu den Abrechnungsunterlagen, auf die sich das Einsichtsrecht des Mieters bezieht, gehören - wie das Berufungsgericht ebenfalls richtig gesehen hat - neben den Rechnungen auch die dazugehörigen Zahlungsbelege über die in der Abrechnung auf die Mieter umgelegten Betriebskosten. Denn mit Hilfe dieser Belege wird der Mieter in die Lage versetzt, die Berechtigung der jeweils in Rechnung gestellten Beträge zu überprüfen. Der Darlegung eines besonderen Interesses bedarf es dabei nicht, es genügt vielmehr das allgemeine Interesse des Mieters, die Tätigkeit des abrechnungspflichtigen Vermieters zu kontrollieren (Senatsurteil vom 7. Februar 2018 - VIII ZR 189/17, aaO Rn. 18).
Entgegen der Auffassung der Revision gilt das auch für die Einsichtnahme in die Zahlungsbelege, und zwar unabhängig davon, ob der Vermieter nach dem Abflussprinzip oder nach dem Leistungsprinzip abrechnet oder bei den unterschiedlichen Betriebskostenarten teils die eine, teils die andere Abrechnungsmethode anwendet (zu den unterschiedlichen Abrechnungsmethoden vgl. Senatsurteil vom 20. Februar 2008 - VIII ZR 49/07, NJW 2008, 1300 Rn. 16 ff.).
a) Zu Unrecht meint die Revision, der Mieter habe an der Vorlage der Zahlungsbelege kein berechtigtes Interesse, weil etwaige Kürzungen oder Nachlässe nicht nur aus dem Zahlungsbeleg ersichtlich seien, sondern vom Vermieter pflichtgemäß bereits auf dem Rechnungsbeleg zu vermerken seien, der Vermieter sich im Falle der Umlage eines nicht oder nicht in voller Höhe entstandenen Rechnungsbetrags wegen Betrugs zu verantworten hätte und die Belegeinsicht dem Mieter ohnehin keinen Schutz biete, da auch Belege manipuliert sein könnten. Mit derartigen Spekulationen kann das der Belegeinsicht zugrundeliegende (allgemeine) Kontrollinteresse des Mieters nicht verneint werden. Zudem verkennt die Revision, dass die Belegeinsicht auch der Aufdeckung möglicher bloßer Versehen bei der Abrechnung dient.

</details>

<details><summary>BGH VIII ZR 118/19, Rn. 16–19</summary>

aa) Entgegen der Auffassung der Revision ist es für den Anspruch des Mieters auf Belegeinsicht (inklusive der Zahlungsbelege) auch nicht von Bedeutung, dass der nach dem Leistungsprinzip abrechnende Vermieter die im Abrechnungszeitraum erbrachten beziehungsweise darauf entfallenden Leistungen unabhängig davon umlegen kann, ob diese (bereits) im Abrechnungszeitraum bezahlt wurden. Denn dies ändert nichts daran, dass sich das allgemeine Kontrollinteresse des Mieters darauf erstreckt, ob der Vermieter die in die Abrechnung eingestellten Leistungen Dritter seinerseits (vollständig) bezahlt hat. Ist das nicht der Fall, besteht für den Mieter zumindest Anlass zu Nachfragen oder zur Erhebung von Einwendungen. Im Zeitpunkt der Erteilung der Abrechnung wird im allgemeinen ein Zeitraum von mehreren Monaten seit Ablauf der Abrechnungsperiode (hier fast 10 Monate) verstrichen und deshalb regelmäßig zu erwarten sein, dass der Vermieter berechtigte Rechnungsbeträge seinerseits inzwischen im normalen Geschäftsgang bezahlt hat. Soweit der Vermieter insoweit einen Zahlungsbeleg nicht vorzulegen vermag, kann das - wie ausgeführt - Anlass für Nachfragen des Mieters oder zur Erhebung von Einwendungen gegen einzelne Kostenpositionen sein.
bb) Soweit der Vermieter nach dem Abflussprinzip abrechnet, das auf die im Abrechnungszeitraum abgeflossenen Mittel (bei Rechnungen Dritter also die Bezahlung dieser Rechnungen durch den Vermieter) abstellt, ist der Mieter zur Überprüfung der Abrechnung - wie das Berufungsgericht ebenfalls richtig gesehen hat - sogar zwingend auf die Einsicht in die Zahlungsbelege angewiesen, eben weil es für die Richtigkeit der Abrechnung in diesem Fall entscheidend darauf ankommt, ob die jeweiligen Betriebskosten im Abrechnungszeitraum bezahlt worden sind.
b) Ohne Erfolg macht die Revision schließlich geltend, das Berufungsgericht hätte der Klägerin die streitige Nachforderung zumindest insoweit zusprechen müssen, als sie sich allein aus den nach dem Leistungsprinzip abgerechneten Betriebskostenarten (also unter Außerachtlassung der nach dem Abflussprinzip in Rechnung gestellten Positionen) ergab.
Das Berufungsgericht hat schon keine abschließenden Feststellungen zu der bei sämtlichen Betriebskostenpositionen jeweils angewendeten Abrechnungsmethode getroffen. Übergangenen Sachvortrag zeigt die Revision insoweit nicht auf. Vor allem aber bezieht sich das Einsichtsrecht des Mieters - unabhängig von der aus der Abrechnung als solcher ohnehin nicht ersichtlichen Abrechnungsmethode - auf die jeweiligen (und damit auf sämtliche vorhandenen) Zahlungsbelege. Anhaltspunkte dafür, dass der Beklagte sein Einsichtsbegehren - etwa im Laufe des Prozesses - auf einzelne Zahlungsbelege zu bestimmten Positionen beschränkt hätte, trägt die Revision nicht vor und sind auch nicht ersichtlich.

</details>

---

## q05 (single)

**Question:** Our lease only says the tenant pays “die Betriebskosten”, with no list of costs attached. Is that enough to bill the tenant for service charges?

**Your reference answer:** Yes. A lease clause saying the tenant pays "die Betriebskosten" is enough, even in a standard form lease. It covers all operating costs in § 2 Nr. 1–16 BetrKV without attaching the list; "other operating costs" (Nr. 17) must be named in the lease (BGH VIII ZR 137/15, Rn. 11).

**Agent's answer:**

> **Yes, that is sufficient.**
>
> According to the Federal Court of Justice (*Bundesgerichtshof* – BGH), an agreement in a residential lease stating that the tenant must bear "the operating costs" (*"die Betriebskosten"*) is sufficient to pass those costs on to the tenant, even when included as a standard form clause (*formularmäßige Vereinbarung*) (**BGH VIII ZR 137/15, Leitsatz**, decided 2016-02-10).
>
> ### Key Rules and Legal Principles:
> 1. **No list or statutory reference required:**
>    Even without attaching a list of operating costs (*Betriebskostenkatalog*) or making an express statutory reference to the legal definition or the Operating Costs Ordinance (*Betriebskostenverordnung*), agreeing that the tenant bears "the operating costs" effectively transfers the operating costs defined by statute and detailed in the ordinance (**BGH VIII ZR 137/15, Leitsatz**).
>
> 2. **Compliance with transparency requirements:**
>    Because the concept of operating costs (*Betriebskosten*) has long been defined by law and standard practice, it requires no further breakdown or explanation in residential leases. It is presumed known and is sufficiently clear and understandable to an average tenant under standard contract transparency rules (**BGH VIII ZR 137/15, Rn. 19–22**).
>
> ### Facts and Limitations This Depends On:
> * **No conflicting or ambiguous lease clauses:**
>   This rule applies as long as no other additions or clauses in the lease create ambiguity as to whether all permissible operating costs or only certain selected categories were meant (**BGH VIII ZR 137/15, Rn. 19–22**).
> * **"Other operating costs" (*sonstige Betriebskosten*):**
>   This general clause does not automatically cover "other" operating costs (*"sonstige" Betriebskosten*) (**BGH VIII ZR 137/15, Rn. 5, 10–13**). To pass on "other operating costs," the specific cost type must generally be expressly designated in the agreement (for example, maintenance of smoke alarm systems under an agreement covering fire protection systems, as addressed in **BGH VIII ZR 117/21, Leitsatz**, decided 2022-10-05).

**Cited passages:**

<details><summary>BGH VIII ZR 137/15, Leitsatz</summary>

In der Wohnraummiete genügt zur Übertragung der Betriebskosten auf den Mieter die - auch formularmäßige - Vereinbarung, dass dieser "die Betriebskosten" zu tragen hat. Auch ohne Beifügung des Betriebskostenkatalogs oder ausdrückliche Bezugnahme auf § 556 Abs. 1 Satz 2 BGB und die Betriebskostenverordnung vom 25. November 2003 (BGBl. I. S. 2347) ist damit die Umlage der in § 556 Abs. 1 Satz 2 BGB definierten und in der Betriebskostenverordnung erläuterten Betriebskosten vereinbart.

</details>

<details><summary>BGH VIII ZR 137/15, Rn. 19–22</summary>

bb) So liegt der Fall hier aber nicht. Wie bereits ausgeführt, ist der Begriff der Betriebskosten seit langem gesetzlich definiert und durch die Aufzählung der einzelnen Betriebskostenarten in einer hierzu ergangenen Verordnung und dem darin enthaltenen Betriebskostenkatalog erläutert. Zudem ist es auch - sowohl im preisfreien als auch im preisgebundenen Wohnraum - seit Jahrzehnten allgemein üblich, in Mietverträgen die Umlage sämtlicher Betriebskosten zu vereinbaren und abzurechnen, die nach den genannten Definitionen umlagefähig sind. Angesichts dessen bedarf der Begriff der "Betriebskosten" in der Wohnraummiete grundsätzlich keiner Erläuterung oder Aufschlüsselung, da er als bekannt vorausgesetzt werden kann und für den durchschnittlichen Mieter hinreichend klar und verständlich (§ 307 Abs. 1 Satz 2 BGB) ist (so bereits zutreffend Schmid, GE 2003, 446 sowie in MünchKommBGB, 6. Aufl., § 556 Rn. 18; ebenso Lehmann-Richter WuM 2012, 647, 648). Die Möglichkeit, dass der Verwender sich ungerechtfertigte Beurteilungsspielräume verschaffen könnte, erscheint angesichts der gesetzlichen Definition und Aufzählung der einzelnen Betriebskostenarten im Betriebskostenkatalog ausgeschlossen.
Eine andere Beurteilung käme allenfalls in Betracht, falls durch Zusätze oder weitere Bestimmungen im Mietvertrag unklar würde, ob "die Betriebskosten" im Sinne sämtlicher umlegbarer Betriebskosten oder nur einzelner Betriebskostenarten gemeint sind. Ein solcher Fall liegt hier aber nicht vor. Er ergibt sich insbesondere nicht daraus, dass der Mietvertrag einen Hinweis auf die zum damaligen Zeitpunkt bereits außer Kraft getretene Anlage 3 zu § 27 der Zweiten Berechnungsverordnung enthält. Denn aus diesem Umstand ergeben sich keinerlei Anhaltspunkte dafür, dass etwas anderes gemeint gewesen sein könnte als die Abwälzung sämtlicher umlegbarer Betriebskosten. Auch die in § 4 des Mietvertrags enthaltene beispielhafte Aufzählung einzelner Betriebskosten mit dem Zusatz "etc" zeigt unabweisbar, dass eine umfassende Umlagevereinbarung im gesetzlich zulässigen Umfang gemeint war.
Nach alledem kann das Urteil des Berufungsgerichts keinen Bestand haben; es ist daher aufzuheben (§ 562 Abs. 1 ZPO).
1. Der Senat entscheidet in der Sache selbst, soweit es keiner weiteren Feststellungen bedarf (§ 563 Abs. 3 ZPO). Dies betrifft die von den Klägerinnen geltend gemachten Mietforderungen in Höhe von 3.809,58 € sowie die vorgerichtlichen Anwaltskosten und die Kosten einer Meldeauskunft, jeweils nebst Zinsen.

</details>

<details><summary>BGH VIII ZR 137/15, Rn. 5, 10–13</summary>

Die Revision hat Erfolg.
Diese Beurteilung hält rechtlicher Nachprüfung nicht stand. Entgegen der Auffassung des Berufungsgerichts sind die den Klägerinnen gemäß § 535 Abs. 2 BGB zustehenden Mietforderungen in Höhe von 3.809,58 € (nebst Zinsen) nicht durch Aufrechnung erloschen. Denn den Beklagten steht hinsichtlich der von Januar 2009 bis März 2012 geleisteten Betriebskostenvorauszahlungen kein Anspruch aus ungerechtfertigter Bereicherung (§ 812 Abs. 1 Satz 1 Alt. 1 BGB) zu. Anders als das Berufungsgericht meint, sind sie nach § 4 Ziffer 1 und 3 des Formularmietvertrags zur Tragung der Betriebskosten und zur Erbringung monatlicher Vorauszahlungen verpflichtet. Die genannten Regelungen im Mietvertrag sind ausreichend bestimmt und halten einer AGB-rechtlichen Inhaltskontrolle stand. Aus diesen Gründen kann mit der vom Berufungsgericht gegebenen Begründung auch ein Anspruch auf Leistung einer Betriebskostenvorauszahlung für den Monat April 2012 (100 €) - hinsichtlich der Monate Mai bis Juli 2012 ist der Rechtsstreit in der Berufungsinstanz übereinstimmend für erledigt erklärt worden - nicht verneint werden.
1. Nach der Rechtsprechung des Senats bedarf es zu einer wirksamen Umlagevereinbarung von Betriebskosten in der Wohnraummiete - auch in einem Formularvertrag - nicht der Aufzählung der einzelnen Betriebskosten. Vielmehr hat es der Senat - jedenfalls soweit es nicht um "sonstige" Betriebskosten im Sinne von Nr. 17 der Anlage 3 zu § 27 der Zweiten Berechnungsverordnung geht - genügen lassen, dass auf die Betriebskosten gemäß der Anlage 3 zu § 27 der Zweiten Berechnungsverordnung verwiesen wird (Senatsurteile vom 7. April 2004 - VIII ZR 167/03, NZM 2004, 417 unter II 1 b bb; vom 27. Juni 2007 - VIII ZR 202/06, NJW 2007, 3060 Rn. 19; vom 13. Januar 2010 - VIII ZR 128/08, NJW 2010, 1198 Rn. 19).
Um eine derartige Klausel geht es auch hier. Entgegen der Auffassung, die das Berufungsgericht im Anschluss an Langenberg (Schmidt-Futterer/Langenberg, BGB, 12. Aufl., § 556 Rn. 46; ähnlich Blum WuM 2010, 13; Lützenkirchen in Lützenkirchen, Mietrecht, 2. Aufl. § 556 Rn. 319; AG Hanau NZM 2015, 47, 49) vertritt, ist es ohne Bedeutung, dass die Anlage 3 zu § 27 der Zweiten Berechnungsverordnung bei Abschluss des Mietvertrags nicht mehr in Kraft, sondern inzwischen durch die - im wesentlichen inhaltsgleiche - Betriebskostenverordnung ersetzt worden war.
2. Die im Mietvertrag vom 27. April 2007 zu den Betriebskosten getroffenen formularmäßigen Bestimmungen sind dahin auszulegen, dass die Beklagten die Betriebskosten gemäß § 556 Abs. 1 Satz 2 BGB in Verbindung mit dem Betriebskostenkatalog in der dazu erlassenen Betriebskostenverordnung zu tragen haben.

</details>

<details><summary>BGH VIII ZR 117/21, Leitsatz</summary>

1. Die Kosten eines externen Dienstleisters für die regelmäßige Kontrolle der Restmüllbehälter des Mietobjekts auf Einhaltung der satzungsmäßigen Vorgaben für die Mülltrennung und für die bei fehlerhafter Abfalltrennung erfolgende Nachsortierung von Hand sind im Wohnraummietverhältnis gemäß § 2 Nr. 8 BetrKV auf den Mieter umlegbare Betriebskosten.
2. Die Kosten für die regelmäßige Prüfung und Sicherstellung der Betriebsbereitschaft von in den Mieträumen angebrachten Rauchwarnmeldern sind im Wohnraummietverhältnis als "sonstige Betriebskosten" im Sinne von § 2 Nr. 17 BetrKV auf den Mieter umlegbar. Sie werden von einer vertraglichen Umlagevereinbarung erfasst, welche die Umlage der Kosten des Betriebs von Brandschutz- und Brandmeldeanlagen auf den Mieter vorsieht.
Dem stehen Regelungen in den Bauordnungen der Länder (hier: § 48 Abs. 4 Satz 4 BauO Bln), nach denen (öffentlich-rechtlich) die Wartung dem Mieter obliegt, nicht entgegen.

</details>

---

## q06 (single)

**Question:** The flats have heat cost allocators and hot water meters, but the central boiler has no heat meter for the hot water. Does our billing still count as consumption-based?

**Your reference answer:** No. If the central system has no heat meter as required by § 9 Abs. 2 HeizkostenV, the billing counts as not consumption-based, so the tenant can cut his share by 15% under § 12 Abs. 1 HeizkostenV, even with allocators and water meters in the flats (BGH VIII ZR 151/20).

**Agent's answer:**

> **No, the billing is legally treated as not consumption-based (nicht verbrauchsabhängig).**
>
> The legal rules and consequences are as follows:
>
> ### 1. Obligation to measure with a heat meter
> Where a central heating installation is combined with the central hot water preparation system (verbundene Anlage), the amount of heat consumed by the central hot water system must be measured using a heat meter (**§ 9 Abs. 1–2 HeizkostenV**). 
>
> Under **§ 9 Abs. 1–2 HeizkostenV**, determining this heat quantity via a mathematical formula is only permitted if measuring it would involve unreasonably high expense (unzumutbar hoher Aufwand).
>
> ### 2. Legal assessment under BGH case law
> According to **BGH VIII ZR 151/20, Leitsatz** (decided 2022-01-12), billing must be classified as **not consumption-based** (nicht verbrauchsabhängig) within the meaning of the heating cost regulations even if the individual apartments have heat cost allocators (Heizkostenverteiler) and hot water meters (Warmwasserzähler), as long as the combined central system lacks the required heat meter (Wärmemengenzähler).
>
> ### 3. Tenant's 15% reduction right
> Under **§ 12 HeizkostenV** and **BGH VIII ZR 151/20, Rn. 28–30**, if heating or hot water costs are not billed based on consumption in accordance with the regulations, the tenant is entitled to reduce their allocated share of both the heating and hot water costs by **15%** (Kürzungsrecht in Höhe von 15%).
>
> ---
>
> ### Facts this depends on:
> * **Cost allocation agreement (Umlagevereinbarung):** Operating costs can only be passed on to tenants if the parties have agreed in the tenancy agreement that the tenant bears operating costs (**§ 556 BGB**).
> * **Unreasonable expense exception:** Under **§ 9 Abs. 1–2 HeizkostenV**, calculating the heat amount instead of measuring it is only lawful if installing/measuring with a heat meter involves an unreasonably high expense. If this exception does not apply and the meter is simply missing, the tenant's right of reduction applies (**BGH VIII ZR 151/20, Rn. 28–30**).

**Cited passages:**

<details><summary>BGH VIII ZR 151/20, Leitsatz</summary>

Von einer nicht verbrauchsabhängigen Abrechnung im Sinne von § 12 Abs. 1 Satz 1 HeizkostenV ist auch dann auszugehen, wenn zwar die Wohnung über Heizkostenverteiler und Warmwasserzähler, jedoch die verbundene zentrale Wärme- und Warmwasserversorgungsanlage nicht über den nach § 9 Abs. 2 Satz 1 HeizkostenV vorgesehenen Wärmemengenzähler verfügt.

</details>

<details><summary>§ 12 HeizkostenV</summary>

(1) Soweit die Kosten der Versorgung mit Wärme oder Warmwasser entgegen den Vorschriften dieser Verordnung nicht verbrauchsabhängig abgerechnet werden, hat der Nutzer das Recht, bei der nicht verbrauchsabhängigen Abrechnung der Kosten den auf ihn entfallenden Anteil um 15 vom Hundert zu kürzen. Wenn der Gebäudeeigentümer entgegen § 5 Absatz 2 oder Absatz 3 keine fernablesbare Ausstattung zur Verbrauchserfassung installiert hat, hat der Nutzer das Recht, bei der Abrechnung der Kosten den auf ihn entfallenden Anteil um 3 vom Hundert zu kürzen. Dasselbe ist anzuwenden, wenn der Gebäudeeigentümer die Informationen nach § 6a nicht oder nicht vollständig mitteilt. Die Sätze 1 bis 3 sind nicht anzuwenden beim Wohnungseigentum im Verhältnis des einzelnen Wohnungseigentümers zur Gemeinschaft der Wohnungseigentümer; insoweit verbleibt es bei den allgemeinen Vorschriften.
(2) Wird in den Fällen des § 1 Absatz 3 der Wärmeverbrauch der einzelnen Nutzer am 30. September 1989 mit Einrichtungen zur Messung der Wassermenge ermittelt, gilt die Anforderung des § 5 Absatz 1 Satz 1 als erfüllt.
(3) Wenn der anteilige Verbrauch der Nutzer an Wärme oder Warmwasser aus Wärmepumpen am 1. Oktober 2024 noch nicht erfasst wird, hat der Gebäudeeigentümer bis zum Ablauf des 30. September 2025 eine Ausstattung zur Verbrauchserfassung zu installieren. In den Fällen des Satzes 1 sind die Vorschriften dieser Verordnung für den Abrechnungszeitraum, der nach der Installation beginnt, erstmalig anzuwenden. Der Eigentümer eines vermieteten Gebäudes, in dem mindestens ein Mieter eine Bruttowarmmiete entrichtet, hat vor Beginn des ersten Abrechnungszeitraums nach dem 30. September 2025 Folgendes zu bestimmen:
1. den Durchschnittswert der in den Jahren 2022, 2023 und 2024 jährlich angefallenen Kosten der Versorgung mit Wärme und Warmwasser sowie
2. den Anteil der einzelnen Nutzeinheiten an dem ermittelten Durchschnittswert entsprechend ihrer Wohn- oder Nutzfläche.

</details>

<details><summary>BGH VIII ZR 151/20, Rn. 28–30</summary>

b) Die Beklagte durfte eine Trennung der Kosten für Wärme und Warmwasser auch nicht nach der in § 9 Abs. 2 Satz 4 HeizkostenV aufgeführten Rechenformel vornehmen, weil die Voraussetzungen für eine Trennung der Kosten nach dieser Vorschrift ebenfalls nicht gegeben waren. Die genannte Bestimmung erlaubt in Ausnahmefällen eine rechnerische Ermittlung der auf die zentrale Warmwasserversorgungsanlage entfallenden Wärmemenge in Abhängigkeit zu der durch die zentrale Anlage mit Warmwasser versorgten Fläche, wenn weder die Wärmemenge noch das Volumen des verbrauchten Wassers gemessen werden können. Der Beklagten war jedoch nach den im Revisionsverfahren nicht angegriffenen Feststellungen des Berufungsgerichts ausweislich der von ihr erstellten Abrechnungen die Messung des Volumens des verbrauchten Wassers aufgrund der für die einzelnen Wohnungen installierten Warmwasserzähler möglich.
c) Die im Hinblick auf § 9 Abs. 1, Abs. 2 Satz 1, 4 HeizkostenV nicht ordnungsgemäße Abrechnung führt - entgegen der Auffassung des Berufungsgerichts (ebenso LG Berlin, Urteil vom 20. Juni 2018 - 65 S 29/18, juris Rn. 7 ff.; LG Berlin [67. Zivilkammer], WuM 2017, 463 f.; MünchKommBGB/Zehelein, 8. Aufl., § 12 HeizkostenV Rn. 1; Langenberg/Zehelein, Betriebskosten- und Heizkostenrecht, 9. Aufl., K Rn. 150; wohl auch BeckOGK/Drager, HeizkostenV, Stand: 1. Juli 2021, § 12 Rn. 8) - nach den dargestellten Grundsätzen dazu, dass dem Kläger im Hinblick auf die Kosten für Wärme und Warmwasser das Kürzungsrecht nach § 12 Abs. 1 Satz 1 HeizkostenV in Höhe von 15 % zusteht (vgl. auch LG Potsdam, WuM 2018, 90; LG Berlin, Urteil vom 16. Januar 2018 - 63 S 91/17, juris Rn. 25 ff.; LG Halle, WuM 2019, 318 f.; LG Frankfurt aM, Urteil vom 28. Oktober 2019 - 2/11 S 38/19, juris Rn. 26 ff.; AG Osnabrück, WuM 2021, 591; BeckOK-Mietrecht/Pfeifer, Stand: 1. November 2021, § 12 HeizkostenV Rn. 11c; Wall, Betriebs- und Heizkosten-Kommentar, 5. Aufl., § 9 HeizkostenV Rn. 6329; Schmidt-Futterer/Lammel, Mietrecht, 15. Aufl., § 9 HeizkostenV Rn. 13; Lützenkirchen, Mietrecht, 3. Aufl., § 12 HeizkostenV Rn. 24; im Grundsatz ebenso LG Itzehoe, ZMR 2019, 499, 500; Schmid/Harz/Ormanschick, Mietrecht, 6. Aufl., § 12 HeizkostenV Rn. 13).
3. Die vom Berufungsgericht zur Begründung seiner gegenteiligen Auffassung angeführten Gründe vermögen demgegenüber nicht zu überzeugen.

</details>

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

---

## q07 (single)

**Question:** A tenant missed the deadline to object to last year’s statement. Now he says some of the costs I billed were never allowed. Can he still challenge them?

**Your reference answer:** Generally no. Once the 12-month objection deadline has passed (§ 556 Abs. 3 S. 6 BGB), the tenant is barred even from objecting to costs that could never be passed on (BGH VIII ZR 209/15, Rn. 25), unless the tenant wasn't responsible for missing the deadline (§ 556 Abs. 3 S. 6 BGB). Exception: if the landlord's own statement showed those items as non-billable, he can't rely on the deadline under § 242 BGB (Rn. 28).

**Agent's answer:**

> As a general rule, **no**, the tenant can no longer challenge the billed costs once the objection deadline has expired. 
>
> The legal situation is governed by the following rules and rulings:
>
> ### 1. The statutory objection deadline and preclusion
> * Under **§ 556 Abs. 3 Satz 5 BGB**, the tenant must notify the landlord of any objections to the statement (Einwendungen gegen die Abrechnung) at the latest by the end of the twelfth month following receipt of the statement.
> * Under **§ 556 Abs. 3 Satz 6 BGB**, once this deadline expires, the tenant is precluded from raising objections (Einwendungsausschluss), unless the tenant is not responsible for the delay (nicht zu vertreten).
>
> ### 2. Scope: Non-allocable costs are also barred
> The preclusion applies broadly to substantive billing errors:
> * **Costs generally not allocable:** The Federal Court of Justice (BGH) established that the preclusion of objections under **§ 556 Abs. 3 Satz 6 BGB** also applies to costs that cannot generally be passed on to residential tenants under § 556 Abs. 1 Satz 1 BGB in conjunction with the Operating Costs Ordinance (*Betriebskostenverordnung*), such as repair and maintenance costs (*Instandsetzungskosten*) or administrative costs (*Verwaltungskosten*) (**BGH VIII ZR 209/15, Leitsatz** and **BGH VIII ZR 209/15, Rn. 22–25**).
> * **Missing lease agreement:** The preclusion likewise covers objections that the lease lacked a contractual agreement to allocate those specific costs (*Umlagevereinbarung*) (**BGH VIII ZR 47/25, Rn. 31–32**).
>
> ### Facts the answer depends on
> Whether the tenant is barred depends on:
> 1. **Lack of fault:** The tenant can only raise late objections if he proves that he was not responsible for missing the 12-month objection window (**§ 556 Abs. 3 Satz 6 BGB**; **BGH VIII ZR 47/25, Rn. 31–32**).
> 2. **Formal validity:** The preclusion presupposes that the service charge statement was formally proper (*formell ordnungsgemäß*) (**BGH VIII ZR 47/25, Rn. 31–32**).
>
> If there is a dispute over whether the tenant was at fault for the delay or whether the statement complied with formal requirements, you should consult a tenancy lawyer (*Fachanwalt für Mietrecht*).

**Cited passages:**

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>BGH VIII ZR 209/15, Leitsatz</summary>

Der Einwendungsausschluss gemäß § 556 Abs. 3 Satz 6 BGB gilt grundsätzlich auch für solche Kosten, die gemäß § 556 Abs. 1 Satz 1 BGB in Verbindung mit der Betriebskostenverordnung in der Wohnraummiete generell nicht auf den Mieter umgelegt werden können.

</details>

<details><summary>BGH VIII ZR 209/15, Rn. 22–25</summary>

b) Die Frage, ob vom Einwendungsausschluss gemäß § 556 Abs. 3 Satz 6 BGB auch die gemäß § 556 Abs. 1 Satz 1 BGB in Verbindung mit der Betriebskostenverordnung generell nicht auf den Mieter umlagefähigen Kosten - wie hier Instandsetzungs- und Verwaltungskosten sowie Rücklagen für die an die Kläger vermietete Eigentumswohnung des Beklagten - umfasst sind, ist umstritten und vom Senat bisher offengelassen worden (Senatsurteil vom 10. Oktober 2007 - VIII ZR 279/06, NJW 2008, 283 Rn. 24 f.).
aa) Einige Stimmen (AG Karlsruhe, ZMR 2012, 787 f.; Langenberg/Zehelein, Betriebskosten- und Heizkostenrecht, 8. Aufl., H VI Rn. 269; Schmidt-Futterer/Langenberg, Mietrecht, 12. Aufl., § 556 BGB Rn. 503) sind der Auffassung, dass der Einwendungsausschluss nicht für abgerechnete Kosten gelte, die nicht zu den Betriebskosten im Sinne der Betriebskostenverordnung zählten. Andernfalls entstünde ein Wertungswiderspruch, wenn das Gesetz die Umlage derartiger Kosten einerseits generell nicht gestatte und dem Mieter andererseits die Berufung darauf durch Fristablauf abschneiden würde.
bb) Nach anderer Auffassung (Staudinger/Weitemeyer, BGB, Neubearb. 2014, § 556 Rn. 129a; MünchKommBGB/Schmid, 6. Aufl., § 556 Rn. 96; Blank/Börstinghaus, Miete, 4. Aufl., § 556 BGB, Rn. 224; Schmid, Handbuch der Mietnebenkosten, 10. Aufl., Rn. 3262c; Streyl, WuM 2005, 505 f.; Sternel, Mietrecht aktuell, 4. Aufl., Rn. V 464 f.) könne es nach dem Sinn und Zweck der Einwendungsobliegenheit des Mieters keinen Unterschied bedeuten, ob sich der Abrechnungsfehler aus dem Vertrag oder dem Gesetz ergebe. Nur ein vollständiger Einwendungsausschluss verwirkliche die gesetzgeberische Absicht, Rechtsfrieden über die Betriebskostenabrechnung herzustellen. Der Einwendungsausschluss gelte auch dann, wenn Kosten umgelegt seien, die nach § 556 Abs. 1 BGB in Verbindung mit der Betriebskostenverordnung nicht umgelegt werden dürften. Es könne nämlich durchaus streitig sein, welche Kosten unter den Katalog der Betriebskostenverordnung fielen (MünchKommBGB/Schmid, aaO).
cc) Der Senat beantwortet die bislang offen gelassene Frage nunmehr dahin, dass die Ausschlussfrist gemäß § 556 Abs. 3 Satz 5, 6 BGB auch für die Einwendung des Mieters gilt, die Abrechnung enthalte Positionen, die generell nicht als Betriebskosten umlegbar seien.

</details>

<details><summary>BGH VIII ZR 47/25, Rn. 31–32</summary>

a) Der Beklagte ist, wie das Berufungsgericht zutreffend erkannt hat, mit Einwendungen gegen die - formell ordnungsgemäße (vgl. hierzu Senatsurteile vom 20. Januar 2016 - VIII ZR 93/15, NJW 2016, 866 Rn. 10; vom 19. Juli 2017 - VIII ZR 3/17, WuM 2017, 529 Rn. 15; jeweils mwN) - Betriebs- und Heizkostenabrechnung vom 5. Dezember 2018 für das Jahr 2017 betreffend die Wohnung Nr. 40020 gemäß § 556 Abs. 3 Satz 6 BGB ausgeschlossen. Denn er hat solche Einwendungen innerhalb der bis zum zwölften Monat nach Zugang der Abrechnung laufenden Frist des § 556 Abs. 3 Satz 5 BGB nicht erhoben. Nach Ablauf dieser Frist kann der Mieter Einwendungen jedoch nicht mehr geltend machen, es sei denn, er hätte die verspätete Geltendmachung nicht zu vertreten (§ 556 Abs. 3 Satz 6 BGB). Zu den Einwendungen gegen eine Betriebskostenabrechnung des Vermieters im Sinne von § 556 Abs. 3 Satz 5 und 6 BGB gehört auch der - hier von dem Beklagten mit Blick auf die ihm gegenüber abgerechneten Wärmelieferungskosten erhobene - Einwand, dass es für einzelne, nach § 556 Abs. 1 BGB grundsätzlich umlagefähige Betriebskosten an einer vertraglichen Vereinbarung über deren Umlage fehlt (vgl. Senatsurteile vom 10. Oktober 2007 - VIII ZR 279/06, NJW 2008, 283 Rn. 24; vom 12. Mai 2010 - VIII ZR 185/09, NJW 2010, 2275 Rn. 15). Feststellungen zu einem fehlenden Verschulden des Beklagten hat das Berufungsgericht nicht getroffen und die Revision zeigt übergangenen Sachvortrag insofern nicht auf.
Die Frist hat mit dem Zugang der Abrechnung bei dem Beklagten im Dezember 2018 zu laufen begonnen. Die Vorschrift des § 11 Abs. 3 der Verordnung über die Umstellung auf gewerbliche Wärmelieferung für Mietwohnraum vom 7. Juni 2013 (Wärmelieferverordnung - WärmeLV; im Folgenden: WärmeLV), wonach die Frist für Einwendungen gegen die Abrechnung der Wärmelieferungskosten (§ 556 Abs. 3 Satz 5 BGB) frühestens dann zu laufen beginnt, wenn der Mieter eine Mitteilung erhalten hat, die den Anforderungen nach § 11 Abs. 1 und 2 WärmeLV entspricht, findet - entgegen der Annahme der Revisionserwiderung - hier keine Anwendung. Sie regelt nur die Folgen einer fehlerhaften oder fehlenden Umstellungsankündigung im Sinne von § 556c Abs. 2 BGB (vgl. BAnz AT vom 20. Juni 2013 B 2, S. 8; siehe auch Lammel/Lammel, Heizkostenverordnung, 5. Aufl., § 1 WärmeLV Rn. 3). Die Vorschrift des § 556c BGB ist im vorliegenden Fall jedoch nicht anwendbar (siehe hierzu nachfolgend unter II 2 a).

</details>

---

## q08 (single)

**Question:** The lease says the flat is 70 m², but when we measured it, it was actually 75 m². Which size do I use to split the service charges?

**Your reference answer:** Use the actual size, 75 m². Where costs are split by floor area, what counts is the flat's actual floor area as a share of the building's actual total floor area, not the area in the lease (BGH VIII ZR 220/17).

**Agent's answer:**

> You must use the **actual living space (tatsächliche Wohnfläche)** of **75 m²**, not the contractually agreed size of 70 m².
>
> ### Legal Assessment
>
> 1. **Actual Area Determines the Allocation:**  
>    When service charges are apportioned wholly or partially by floor area, the calculation is generally based on the proportion of the flat's actual living space (*tatsächliche Wohnfläche*) to the total living space actually existing in the economic unit (*tatsächlich vorhandene Gesamtwohnfläche*) (BGH VIII ZR 220/17, Leitsatz, judgment of 30 May 2018).
>
> 2. **Contractual Size Specifications Are Inapplicable for Building-Wide Apportionment:**  
>    Costs incurred for an entire building or economic unit (*Wirtschaftseinheit*) must be distributed under an objective allocation key (*Abrechnungsmaßstab*) that applies equally to all occupants. Subjective contractual agreements between individual parties regarding flat size (*Beschaffenheitsvereinbarung zur Wohnfläche*) do not provide an objective standard and cannot be used to apportion costs (BGH VIII ZR 220/17, Rn. 22–23).
>
> 3. **Abandonment of the 10% Tolerance Threshold:**  
>    The Federal Court of Justice previously considered deviations of up to 10% between agreed and actual floor area to be negligible in service charge statements, but expressly abandoned that rule in this decision. Service charges must be billed strictly according to actual circumstances (BGH VIII ZR 220/17, Leitsatz and Rn. 18–21).
>
> ### Facts the Answer Depends On
> * **Cost allocation agreement (*Umlagevereinbarung*):** The answer depends on whether the lease actually contains an agreement transferring the service charges to the tenant (BGH VIII ZR 137/15, Leitsatz).
> * **Floor area as the allocation key:** This applies to those service charge items that are allocated based on floor area proportions (BGH VIII ZR 220/17, Leitsatz).
> * **Total floor area calculation:** When you apply the actual 75 m² for the flat, the total building area (*Gesamtwohnfläche*) in the calculation must likewise reflect the actual total living space of the property (BGH VIII ZR 220/17, Leitsatz).

**Cited passages:**

<details><summary>BGH VIII ZR 220/17, Leitsatz</summary>

Sofern und soweit Betriebskosten nach gesetzlichen Vorgaben (vgl. etwa § 556a Abs. 1 BGB, § 7 Abs. 1 HeizkostenV) ganz oder teilweise nach Wohnflächenanteilen umgelegt werden, ist für die Abrechnung im Allgemeinen der jeweilige Anteil der tatsächlichen Wohnfläche der betroffenen Wohnung an der in der Wirtschaftseinheit tatsächlich vorhandenen Gesamtwohnfläche maßgebend (insoweit Aufgabe von BGH, Urteil vom 31. Oktober 2007, VIII ZR 261/06, NJW 2008, 142 Rn. 19).

</details>

<details><summary>BGH VIII ZR 220/17, Rn. 22–23</summary>

Auch wenn bei der Umlage von Betriebskosten absolute Verteilungsgerechtigkeit nicht zu erreichen sein mag und eine solche auch vom Gesetz nicht verlangt wird (vgl. hierzu Senatsurteile vom 10. Dezember 2014 - VIII ZR 9/14, NJW-RR 2015, 437 Rn. 29; vom 6. Oktober 2010 - VIII ZR 183/09, NJW 2010, 3645 Rn. 17), erfordert eine in der gebotenen Gesamtschau angemessene und nach allen Seiten hin interessengerechte Verteilung von Betriebskosten doch jedenfalls grundsätzlich, dass objektiv entstandene und für eine geschlossene Wirtschaftseinheit (im Streitfall: für mehrere Wohnungen in einem Mehrfamilienhaus) einheitlich erfasste Betriebskosten (hier: Heizkosten) nach einem objektiven Abrechnungsmaßstab umgelegt werden, der gleichermaßen für alle zur Wirtschaftseinheit zählenden Nutzer gilt. Damit scheiden im Allgemeinen subjektive Vorstellungen einzelner Mietvertragsparteien zur Wohnungsgröße, die ihren Ausdruck in einer Beschaffenheitsvereinbarung zur Wohnfläche gefunden haben, schon von vornherein als tauglicher Abrechnungsmaßstab aus.
Sofern und soweit Betriebskosten nach gesetzlichen Vorgaben (vgl. etwa § 566a Abs. 1 BGB, § 7 Abs. 1 HeizkostenV) daher ganz oder teilweise nach Wohnflächenanteilen umgelegt werden, geht es mithin im Allgemeinen um den Anteil der tatsächlichen Wohnfläche der jeweils betroffenen Wohnung an der in der Wirtschaftseinheit tatsächlich vorhandenen Gesamtwohnfläche (so jedenfalls im Ergebnis auch: Staudinger/Artz, BGB, Neubearb. 2018, § 556a Rn. 23; Blank in Blank/Börstinghaus, Miete, 5. Aufl., § 556a Rn. 36; Wall, Betriebskostenkommentar, 4. Aufl., Rn. 2338; Langenberg/Zehelein, Betriebs- und Heizkostenrecht, 8. Aufl., F Rn. 83; Schmidt-Futterer/Langenberg, Mietrecht, 13. Aufl., § 556a BGB Rn. 28; Emmerich/Sonnenschein, Miete, 11. Aufl., § 556a Rn. 19; Schmid/Harsch in Schmid/Harz, Mietrecht Kommentar, 5. Aufl., 2017, § 556a Rn. 166c; Heix, WuM 2016, 263, 265; Hinz, JR 2017, 284, 286; unklar: MünchKommBGB/Schmid-Zehelein, 7. Aufl., § 556a Rn. 31). Auch erwähnt die Heizkostenverordnung mehrfach den Begriff der "anerkannten Regeln der Technik" (so in § 5 Abs. 2 Satz 2, § 7 Abs. 1 Satz 3, § 9 Abs. 1 Satz 5, § 9b Abs. 2), der eher darauf hindeutet, dass der Verordnungsgeber in erster Linie in diesen Regeln niedergelegte objektive Kriterien für die Heizkostenverteilung als maßgeblich ansieht. Dies spricht ebenfalls dafür, die tatsächlichen Verhältnisse bei der Abrechnung nach Wohnflächenanteilen heranzuziehen.

</details>

<details><summary>BGH VIII ZR 137/15, Leitsatz</summary>

In der Wohnraummiete genügt zur Übertragung der Betriebskosten auf den Mieter die - auch formularmäßige - Vereinbarung, dass dieser "die Betriebskosten" zu tragen hat. Auch ohne Beifügung des Betriebskostenkatalogs oder ausdrückliche Bezugnahme auf § 556 Abs. 1 Satz 2 BGB und die Betriebskostenverordnung vom 25. November 2003 (BGBl. I. S. 2347) ist damit die Umlage der in § 556 Abs. 1 Satz 2 BGB definierten und in der Betriebskostenverordnung erläuterten Betriebskosten vereinbart.

</details>

---

## q09 (single)

**Question:** We signed an expensive cleaning contract before this tenant moved in. Can the tenant claim I’m breaking the rule to keep costs reasonable?

**Your reference answer:** Not for signing the contract, because there was no lease yet at that point. A breach is only possible if you could reasonably have reduced the costs during the tenancy, e.g. by terminating the contract, and didn't (BGH VIII ZR 230/21, LS 1).

**Agent's answer:**

> Whether the tenant can claim a breach of the principle of economic efficiency (*Grundsatz der Wirtschaftlichkeit*) depends on the following rules and facts:
>
> ### 1. Prerequisite: Lease Agreement (*Umlagevereinbarung*)
> Operating costs can only be passed on to the tenant if the contracting parties have agreed in the lease that the tenant bears operating costs (**§ 556 BGB**). Costs for building cleaning are eligible operating costs (**§ 2 Nr. 5–13 BetrKV**, specifically Nr. 9 for *Gebäudereinigung*).
>
> ---
>
> ### 2. Entering into the Contract Prior to the Tenancy
> The tenant **cannot** establish a breach simply by pointing out that you concluded an expensive cleaning contract before they moved in:
> * While the principle of economic efficiency must be observed when billing prepayments (**§ 556 BGB**; **BGH VIII ZR 230/21, Rn. 27–30**, decided 2023-01-25), concluding the service contract before the lease was signed does not constitute a breach of this duty. 
> * At the time the cleaning contract was executed, no tenancy relationship or pre-existing duty of mutual consideration (*mietvertragliche Rücksichtnahmepflicht*) existed toward this tenant (**BGH VIII ZR 230/21, Leitsatz 1 and Rn. 31–34**).
>
> ---
>
> ### 3. When a Breach *Can* Be Claimed
> A violation of the duty of economic efficiency (*Wirtschaftlichkeitsgebot*) can only come into question during the ongoing tenancy if:
> 1. There is an unreasonable cost-benefit ratio (*nicht angemessenes Kosten-Nutzen-Verhältnis*), **and**
> 2. It was both **possible and economically reasonable** (*möglich und wirtschaftlich zumutbar*) for you as the landlord to correct the measure leading to excessive costs during the lease—for example, by terminating a contract with unfavorable terms—and you failed to seize that opportunity (**BGH VIII ZR 230/21, Leitsatz 1 and Rn. 31–34**).
>
> ---
>
> ### 4. Burden of Proof
> The tenant bears the full burden of presentation and proof (*Darlegungs- und Beweislast*) regarding a breach of duty by the landlord (**BGH VIII ZR 230/21, Leitsatz 2**; **BGH VIII ZR 117/21, Rn. 35–38**, decided 2022-10-05). It is up to the tenant to show that a correction of the contract was feasible and economically reasonable for you during the tenancy and that you neglected to act.

**Cited passages:**

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>§ 2 Nr. 5–13 BetrKV</summary>

hierzu gehören das Entgelt für die Lieferung des Warmwassers und die Kosten des Betriebs der zugehörigen Hausanlagen entsprechend Nummer 4 Buchstabe a
oder
c) der Reinigung und Wartung von Warmwassergeräten,
hierzu gehören die Kosten der Beseitigung von Wasserablagerungen und Verbrennungsrückständen im Innern der Geräte sowie die Kosten der regelmäßigen Prüfung der Betriebsbereitschaft und Betriebssicherheit und der damit zusammenhängenden Einstellung durch eine Fachkraft;
6. die Kosten verbundener Heizungs- und Warmwasserversorgungsanlagen
a) bei zentralen Heizungsanlagen entsprechend Nummer 4 Buchstabe a und entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind,
oder
b) bei der eigenständig gewerblichen Lieferung von Wärme entsprechend Nummer 4 Buchstabe c und entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind,
oder
c) bei verbundenen Etagenheizungen und Warmwasserversorgungsanlagen entsprechend Nummer 4 Buchstabe d und entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind;
7. die Kosten des Betriebs des Personen- oder Lastenaufzugs,
hierzu gehören die Kosten des Betriebsstroms, die Kosten der Beaufsichtigung, der Bedienung, Überwachung und Pflege der Anlage, der regelmäßigen Prüfung ihrer Betriebsbereitschaft und Betriebssicherheit einschließlich der Einstellung durch eine Fachkraft sowie die Kosten der Reinigung der Anlage;
8. die Kosten der Straßenreinigung und Müllbeseitigung,
zu den Kosten der Straßenreinigung gehören die für die öffentliche Straßenreinigung zu entrichtenden Gebühren und die Kosten entsprechender nicht öffentlicher Maßnahmen; zu den Kosten der Müllbeseitigung gehören namentlich die für die Müllabfuhr zu entrichtenden Gebühren, die Kosten entsprechender nicht öffentlicher Maßnahmen, die Kosten des Betriebs von Müllkompressoren, Müllschluckern, Müllabsauganlagen sowie des Betriebs von Müllmengenerfassungsanlagen einschließlich der Kosten der Berechnung und Aufteilung;
9. die Kosten der Gebäudereinigung und Ungezieferbekämpfung,
zu den Kosten der Gebäudereinigung gehören die Kosten für die Säuberung der von den Bewohnern gemeinsam genutzten Gebäudeteile, wie Zugänge, Flure, Treppen, Keller, Bodenräume, Waschküchen, Fahrkorb des Aufzugs;
10. die Kosten der Gartenpflege,
hierzu gehören die Kosten der Pflege gärtnerisch angelegter Flächen einschließlich der Erneuerung von Pflanzen und Gehölzen, der Pflege von Spielplätzen einschließlich der Erneuerung von Sand und der Pflege von Plätzen, Zugängen und Zufahrten, die dem nicht öffentlichen Verkehr dienen;
11. die Kosten der Beleuchtung,
hierzu gehören die Kosten des Stroms für die Außenbeleuchtung und die Beleuchtung der von den Bewohnern gemeinsam genutzten Gebäudeteile, wie Zugänge, Flure, Treppen, Keller, Bodenräume, Waschküchen;
12. die Kosten der Schornsteinreinigung,
hierzu gehören die Kehrgebühren nach der maßgebenden Gebührenordnung, soweit sie nicht bereits als Kosten nach Nummer 4 Buchstabe a berücksichtigt sind;
13. die Kosten der Sach- und Haftpflichtversicherung,

</details>

<details><summary>BGH VIII ZR 230/21, Rn. 27–30</summary>

b) Das Berufungsgericht hat weiter zu Recht angenommen, dass die Beklagte als Vermieterin gemäß § 556 Abs. 3 Satz 1 Halbs. 2 BGB gegenüber den Klägern als ihren Mietern die vertragliche Nebenpflicht trifft, bei Maßnahmen und Entscheidungen, die Einfluss auf die Höhe der von diesen zu tragenden Betriebskosten haben, auf ein angemessenes Kosten-Nutzen-Verhältnis Rücksicht zu nehmen (sogenannter Wirtschaftlichkeitsgrundsatz; vgl. BGH, Urteile vom 28. November 2007 - VIII ZR 243/06, NJW 2008, 440 Rn. 14; vom 6. Juli 2011 - VIII ZR 340/10, NJW 2011, 3028 Rn. 13; vom 17. Dezember 2014 - XII ZR 170/13, NJW 2015, 855 Rn. 10; vom 27. Oktober 2021 - VIII ZR 114/21, NJW-RR 2022, 157 Rn. 30), und dass die Verletzung dieser Pflicht durch den Vermieter zu einem Schadensersatzanspruch des Mieters nach § 280 Abs. 1, § 241 Abs. 2 BGB führen kann, der auf Rückzahlung der unnötigen Kosten beziehungsweise auf Freihaltung von diesen gerichtet ist (vgl. Senatsurteile vom 28. November 2007 - VIII ZR 243/06, aaO; vom 6. Juli 2011 - VIII ZR 340/10, aaO; vom 5. Oktober 2022 - VIII ZR 117/21, NJW-RR 2022, 1593 Rn. 36).
c) Das Berufungsgericht hat jedoch - wie die Revision mit Recht geltend macht - die für eine Verletzung dieser Pflicht notwendigen Feststellungen nicht getroffen, weil es sowohl den Inhalt dieser Pflicht als auch die diesbezügliche Verteilung der Darlegungs- und Beweislast verkannt hat.
aa) Die Beurteilung der Frage, ob die Beklagte gegen das Wirtschaftlichkeitsgebot verstoßen hat, ist zwar das Ergebnis einer tatrichterlichen Würdigung, die in der Revisionsinstanz nur eingeschränkt darauf überprüft werden kann, ob das Berufungsgericht den Rechtsbegriff des Gebots der Wirtschaftlichkeit verkannt, wesentliche Umstände übersehen oder nicht vollständig gewürdigt, Denkgesetze oder Erfahrungssätze verletzt oder Verfahrensfehler begangen hat (vgl. Senatsbeschluss vom 20. April 2010 - VIII ZR 254/09, WuM 2010, 431 Rn. 5 mwN).
bb) Solche Fehler liegen hier indes vor.

</details>

<details><summary>BGH VIII ZR 230/21, Leitsatz</summary>

1. Wurde ein die Betriebskosten auslösender Dienstleistungsvertrag bereits vor Abschluss des Wohnraummietvertrags geschlossen, kann eine mögliche Verletzung des Wirtschaftlichkeitsgebots als Nebenpflicht des Vermieters schon wegen einer zu diesem Zeitpunkt noch nicht bestehenden mietvertraglichen Rücksichtnahmepflicht nicht in der Eingehung dieser Verbindlichkeit gesehen werden. Vielmehr kommt eine Verletzung des Wirtschaftlichkeitsgebots nur in Betracht, soweit dem Vermieter - im Falle eines nicht angemessenen Kosten-Nutzen-Verhältnisses - eine Korrektur der zu überhöhten Kosten führenden Maßnahme während des Mietverhältnisses - beispielsweise durch Kündigung eines Vertrags mit ungünstigen Bedingungen - möglich und wirtschaftlich zumutbar gewesen wäre und er diese Möglichkeit nicht ergriffen hat (im Anschluss an Senatsurteil vom 28. November 2007 - VIII ZR 243/06, NJW 2008, 440 Rn. 15).
2. Aus der Einordnung des Wirtschaftlichkeitsgebots als vertragliche Nebenpflicht des Vermieters folgt nach allgemeinen Grundsätzen, dass der Mieter, der wegen einer solchen Pflichtverletzung Ansprüche erhebt, die Darlegungs- und Beweislast für ein pflichtwidriges Verhalten des Vermieters trägt (im Anschluss an Senatsurteile vom 6. Juli 2011 - VIII ZR 340/10, NJW 2011, 3028 Rn. 16; vom 5. Oktober 2022 - VIII ZR 117/21, NJW-RR 2022, 1593 Rn. 36).

</details>

<details><summary>BGH VIII ZR 117/21, Rn. 35–38</summary>

aa) Die Revision geht zwar zutreffend davon aus, dass die Beklagte bei einem Verstoß gegen das Wirtschaftlichkeitsgebot die durch die Beauftragung des externen Dienstleisters mit der Kontrolle der Restmüllbehälter und mit der Nachsortierung von Hand entstandenen Kosten nicht auf die Kläger umlegen könnte.
Denn den Vermieter trifft die vertragliche Nebenpflicht, bei Maßnahmen und Entscheidungen, die Einfluss auf die Höhe der vom Mieter zu tragenden Betriebskosten haben, auf ein angemessenes Kosten-Nutzen-Verhältnis Rücksicht zu nehmen. Eine Verletzung dieser Pflicht durch den Vermieter kann zu einem Schadensersatzanspruch des Mieters gemäß § 280 Abs. 1, § 241 Abs. 2 BGB führen, der sich auf dessen Freihaltung von den unnötigen Kosten richtet (vgl. BGH, Urteile vom 28. November 2007 - VIII ZR 243/06, NZM 2008, 78 Rn. 14; vom 6. Juli 2011 - VIII ZR 340/10, NZM 2011, 705 Rn. 13; vom 17. Dezember 2014 - XII ZR 170/13, NZM 2015, 132 Rn. 10 f.). Die Darlegungs- und Beweislast für ein in diesem Sinne pflichtwidriges Verhalten des Vermieters trägt der Mieter, der wegen einer Verletzung des Wirtschaftlichkeitsgebots Ansprüche erhebt (vgl. Senatsurteil vom 6. Juli 2011 - VIII ZR 340/10, aaO Rn. 16).
bb) Das Berufungsgericht, das von diesem rechtlichen Maßstab ausgegangen ist, hat jedoch zu Recht angenommen, dass die Kläger im Streitfall eine diesbezügliche Pflichtverletzung der Beklagten nicht (hinreichend) dargelegt haben.
(1) Ohne Erfolg beanstandet die Revision insoweit mit der Verfahrensrüge, das Berufungsgericht habe entscheidungserheblichen Sachvortrag der Kläger zur Nichterkennbarkeit einer Kostenersparnis durch das "Behältermanagement" nicht beachtet und sei (nur) deshalb von einem nicht ausreichenden oder unzulässigen Vortrag der Kläger ausgegangen.

</details>

---

## q10 (single)

**Question:** A tenant claims our caretaker service is overpriced. Do I have to prove the price is reasonable, or does the tenant have to prove it isn’t?

**Your reference answer:** The tenant has to prove it. A tenant who claims the landlord breached the duty to keep costs reasonable carries the burden of stating and proving it (BGH VIII ZR 230/21, LS 2).

**Agent's answer:**

> The **tenant bears the burden of pleading and proof (*Darlegungs- und Beweislast*)**; you do not have to prove that the price is reasonable simply because the tenant claims it is overpriced.
>
> ### 1. Allocation of the Burden of Proof
> * **The duty of economic efficiency:** Under **§ 556 Abs. 3 Satz 1 Halbs. 2 BGB**, the landlord has a contractual ancillary duty (*vertragliche Nebenpflicht*) to consider an appropriate cost-benefit ratio when making decisions affecting the amount of service charges (*BGH VIII ZR 230/21, Rn. 27–30*). A breach of this duty can give rise to a tenant damages claim to be kept free from unnecessary costs (*BGH VIII ZR 230/21, Rn. 27–30*; *BGH VIII ZR 117/21, Rn. 35–38*).
> * **The tenant must prove the breach:** Under general civil procedural rules, the tenant who raises claims based on a breach of the principle of economic efficiency (*Wirtschaftlichkeitsgebot*) carries the burden of pleading and proving that the landlord acted in breach of duty (*BGH VIII ZR 230/21, Leitsatz*; *BGH VIII ZR 230/21, Rn. 40–43*; *BGH VIII ZR 117/21, Rn. 35–38*). 
>
> ### 2. Timing of the Service Contract
> * If the service contract for the caretaker was concluded *before* the residential lease was signed, entering into that contract cannot constitute a breach of duty toward the tenant (*BGH VIII ZR 230/21, Leitsatz*; *BGH VIII ZR 230/21, Rn. 31–34*).
> * In that situation, a breach can only exist if the landlord had a viable and economically reasonable opportunity to correct or terminate the unfavorable contract during the active tenancy and failed to take it (*BGH VIII ZR 230/21, Leitsatz*; *BGH VIII ZR 230/21, Rn. 31–34*).
>
> ### 3. Facts the Charge Depends On
> * **Lease agreement (*Umlagevereinbarung*):** Caretaker costs can only be passed on if the lease agreement explicitly stipulates that the tenant bears operating costs under **§ 556 Abs. 1 BGB**.
> * **Eligible caretaker costs:** Under **§ 2 Nr. 13–17 BetrKV** (specifically Nr. 14), only routine care, cleaning, and maintenance tasks belong to caretaker costs (*Kosten für den Hauswart*). Tasks concerning repair/maintenance (*Instandhaltung, Instandsetzung*), renewal, cosmetic repairs, or property administration (*Hausverwaltung*) must be deducted. An on-call emergency fee (*Notdienstpauschale*) paid to a caretaker cannot be passed on as operating costs, but constitutes non-billable administrative costs (*Verwaltungskosten*) (*BGH VIII ZR 62/19, Leitsatz*).

**Cited passages:**

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>BGH VIII ZR 230/21, Rn. 27–30</summary>

b) Das Berufungsgericht hat weiter zu Recht angenommen, dass die Beklagte als Vermieterin gemäß § 556 Abs. 3 Satz 1 Halbs. 2 BGB gegenüber den Klägern als ihren Mietern die vertragliche Nebenpflicht trifft, bei Maßnahmen und Entscheidungen, die Einfluss auf die Höhe der von diesen zu tragenden Betriebskosten haben, auf ein angemessenes Kosten-Nutzen-Verhältnis Rücksicht zu nehmen (sogenannter Wirtschaftlichkeitsgrundsatz; vgl. BGH, Urteile vom 28. November 2007 - VIII ZR 243/06, NJW 2008, 440 Rn. 14; vom 6. Juli 2011 - VIII ZR 340/10, NJW 2011, 3028 Rn. 13; vom 17. Dezember 2014 - XII ZR 170/13, NJW 2015, 855 Rn. 10; vom 27. Oktober 2021 - VIII ZR 114/21, NJW-RR 2022, 157 Rn. 30), und dass die Verletzung dieser Pflicht durch den Vermieter zu einem Schadensersatzanspruch des Mieters nach § 280 Abs. 1, § 241 Abs. 2 BGB führen kann, der auf Rückzahlung der unnötigen Kosten beziehungsweise auf Freihaltung von diesen gerichtet ist (vgl. Senatsurteile vom 28. November 2007 - VIII ZR 243/06, aaO; vom 6. Juli 2011 - VIII ZR 340/10, aaO; vom 5. Oktober 2022 - VIII ZR 117/21, NJW-RR 2022, 1593 Rn. 36).
c) Das Berufungsgericht hat jedoch - wie die Revision mit Recht geltend macht - die für eine Verletzung dieser Pflicht notwendigen Feststellungen nicht getroffen, weil es sowohl den Inhalt dieser Pflicht als auch die diesbezügliche Verteilung der Darlegungs- und Beweislast verkannt hat.
aa) Die Beurteilung der Frage, ob die Beklagte gegen das Wirtschaftlichkeitsgebot verstoßen hat, ist zwar das Ergebnis einer tatrichterlichen Würdigung, die in der Revisionsinstanz nur eingeschränkt darauf überprüft werden kann, ob das Berufungsgericht den Rechtsbegriff des Gebots der Wirtschaftlichkeit verkannt, wesentliche Umstände übersehen oder nicht vollständig gewürdigt, Denkgesetze oder Erfahrungssätze verletzt oder Verfahrensfehler begangen hat (vgl. Senatsbeschluss vom 20. April 2010 - VIII ZR 254/09, WuM 2010, 431 Rn. 5 mwN).
bb) Solche Fehler liegen hier indes vor.

</details>

<details><summary>BGH VIII ZR 117/21, Rn. 35–38</summary>

aa) Die Revision geht zwar zutreffend davon aus, dass die Beklagte bei einem Verstoß gegen das Wirtschaftlichkeitsgebot die durch die Beauftragung des externen Dienstleisters mit der Kontrolle der Restmüllbehälter und mit der Nachsortierung von Hand entstandenen Kosten nicht auf die Kläger umlegen könnte.
Denn den Vermieter trifft die vertragliche Nebenpflicht, bei Maßnahmen und Entscheidungen, die Einfluss auf die Höhe der vom Mieter zu tragenden Betriebskosten haben, auf ein angemessenes Kosten-Nutzen-Verhältnis Rücksicht zu nehmen. Eine Verletzung dieser Pflicht durch den Vermieter kann zu einem Schadensersatzanspruch des Mieters gemäß § 280 Abs. 1, § 241 Abs. 2 BGB führen, der sich auf dessen Freihaltung von den unnötigen Kosten richtet (vgl. BGH, Urteile vom 28. November 2007 - VIII ZR 243/06, NZM 2008, 78 Rn. 14; vom 6. Juli 2011 - VIII ZR 340/10, NZM 2011, 705 Rn. 13; vom 17. Dezember 2014 - XII ZR 170/13, NZM 2015, 132 Rn. 10 f.). Die Darlegungs- und Beweislast für ein in diesem Sinne pflichtwidriges Verhalten des Vermieters trägt der Mieter, der wegen einer Verletzung des Wirtschaftlichkeitsgebots Ansprüche erhebt (vgl. Senatsurteil vom 6. Juli 2011 - VIII ZR 340/10, aaO Rn. 16).
bb) Das Berufungsgericht, das von diesem rechtlichen Maßstab ausgegangen ist, hat jedoch zu Recht angenommen, dass die Kläger im Streitfall eine diesbezügliche Pflichtverletzung der Beklagten nicht (hinreichend) dargelegt haben.
(1) Ohne Erfolg beanstandet die Revision insoweit mit der Verfahrensrüge, das Berufungsgericht habe entscheidungserheblichen Sachvortrag der Kläger zur Nichterkennbarkeit einer Kostenersparnis durch das "Behältermanagement" nicht beachtet und sei (nur) deshalb von einem nicht ausreichenden oder unzulässigen Vortrag der Kläger ausgegangen.

</details>

<details><summary>BGH VIII ZR 230/21, Leitsatz</summary>

1. Wurde ein die Betriebskosten auslösender Dienstleistungsvertrag bereits vor Abschluss des Wohnraummietvertrags geschlossen, kann eine mögliche Verletzung des Wirtschaftlichkeitsgebots als Nebenpflicht des Vermieters schon wegen einer zu diesem Zeitpunkt noch nicht bestehenden mietvertraglichen Rücksichtnahmepflicht nicht in der Eingehung dieser Verbindlichkeit gesehen werden. Vielmehr kommt eine Verletzung des Wirtschaftlichkeitsgebots nur in Betracht, soweit dem Vermieter - im Falle eines nicht angemessenen Kosten-Nutzen-Verhältnisses - eine Korrektur der zu überhöhten Kosten führenden Maßnahme während des Mietverhältnisses - beispielsweise durch Kündigung eines Vertrags mit ungünstigen Bedingungen - möglich und wirtschaftlich zumutbar gewesen wäre und er diese Möglichkeit nicht ergriffen hat (im Anschluss an Senatsurteil vom 28. November 2007 - VIII ZR 243/06, NJW 2008, 440 Rn. 15).
2. Aus der Einordnung des Wirtschaftlichkeitsgebots als vertragliche Nebenpflicht des Vermieters folgt nach allgemeinen Grundsätzen, dass der Mieter, der wegen einer solchen Pflichtverletzung Ansprüche erhebt, die Darlegungs- und Beweislast für ein pflichtwidriges Verhalten des Vermieters trägt (im Anschluss an Senatsurteile vom 6. Juli 2011 - VIII ZR 340/10, NJW 2011, 3028 Rn. 16; vom 5. Oktober 2022 - VIII ZR 117/21, NJW-RR 2022, 1593 Rn. 36).

</details>

<details><summary>BGH VIII ZR 230/21, Rn. 40–43</summary>

(c) Das Berufungsgericht ist bei seinen Erwägungen zum Wirtschaftlichkeitsgebot zwar zutreffend davon ausgegangen, dass der Mieter, der wegen der Verletzung des Wirtschaftlichkeitsgebots Ansprüche geltend macht, für ein in diesem Sinne pflichtwidriges Verhalten des Vermieters die Darlegungs- und Beweislast trägt. Rechtsfehlerhaft hat das Berufungsgericht indes angenommen, etwas Anderes gelte hinsichtlich des von ihm so bezeichneten "Kostengrunds", mithin hinsichtlich der von dem Berufungsgericht unter den hier gegebenen Umständen als der Sache nach mit keinerlei ersichtlichen Nutzen für den Mieter verbunden erachteten Durchführung des Müllmanagements. Denn es hat von der Beklagten substantiierten Vortrag hinreichender tatsächlicher Umstände verlangt, aus denen sich ergebe, dass sie auch insoweit das Wirtschaftlichkeitsgebot hinreichend beachtet habe.
(aa) Bei der Beachtung des Wirtschaftlichkeitsgebots handelt es sich um eine vertragliche Nebenpflicht des Vermieters (so bereits Senatsurteil vom 28. November 2007 - VIII ZR 243/06, NJW 2008, 440 Rn. 14). Aus dieser Einordnung folgt nach allgemeinen Grundsätzen, dass der Mieter, der wegen einer solchen Pflichtverletzung Ansprüche erhebt, die Darlegungs- und Beweislast für ein pflichtwidriges Verhalten des Vermieters trägt (Senatsurteile vom 6. Juli 2011 - VIII ZR 340/10, NJW 2011, 3028 Rn. 16; vom 5. Oktober 2022 - VIII ZR 117/21, NJW-RR 2022, 1593 Rn. 36; vgl. bereits Senatsurteil vom 31. Mai 1978 - VIII ZR 263/76, NJW 1978, 2197 unter 3 a; siehe auch Milger, NZM 2012, 657, 662).
(bb) Zu Unrecht hat das Berufungsgericht gemeint, dieser Grundsatz gelte allein für die Kostenhöhe, nicht indes für den von ihm so bezeichneten "Kostengrund". Zwar mag es sachgerecht sein, bei der Prüfung des Vorliegens eines angemessenen Kosten-Nutzen-Verhältnisses zunächst in den Blick zu nehmen, ob die konkrete Maßnahme überhaupt einen Nutzen für den Mieter hat und nicht etwa "überflüssig" (vgl. hierzu Milger, NZM 2012, 657, 662) ist, und bejahendenfalls im Anschluss hieran eine Prüfung der Angemessenheit der Höhe der konkreten Kosten vorzunehmen. Dies ändert indes nichts daran, dass der Mieter seinen Anspruch auf eine - einheitlich zu betrachtende - Pflichtverletzung stützt, für deren Vorliegen er insgesamt die Darlegungs- und Beweislast trägt. Genau dies - und nicht etwa, wie das Berufungsgericht gemeint hat, das Gegenteil - ergibt sich aus dem allgemeinen zivilprozessualen Grundsatz, wonach jede Partei die für sie günstigen Tatsachen darzulegen und zu beweisen hat.
3. Das angegriffene Urteil ist auch, soweit das Berufungsgericht den von den Klägern erhobenen Feststellungsklagen entsprochen hat, nicht frei von Rechtsfehlern.

</details>

<details><summary>BGH VIII ZR 230/21, Rn. 31–34</summary>

(1) Das Berufungsgericht hat bereits im Ausgangspunkt verkannt, dass eine mögliche Verletzung des Wirtschaftlichkeitsgebots durch die Beklagte nicht in der "Entscheidung für das Müllmanagementsystem" - mithin nicht in dem Abschluss des Vertrags mit der externen Dienstleisterin - liegt. Wurde ein die Betriebskosten auslösender Dienstleistungsvertrag - wie hier - bereits vor Abschluss des Wohnraummietvertrags geschlossen, kann eine mögliche Nebenpflichtverletzung des Vermieters schon wegen einer zu diesem Zeitpunkt noch nicht bestehenden mietvertraglichen Rücksichtnahmepflicht nicht in der Eingehung dieser Verbindlichkeit gesehen werden. Vielmehr kommt eine Verletzung des Wirtschaftlichkeitsgebots nur in Betracht, soweit dem Vermieter - im Falle eines nicht angemessenen Kosten-Nutzen-Verhältnisses - eine Korrektur der zu überhöhten Kosten führenden Maßnahme während des Mietverhältnisses - beispielsweise durch Kündigung eines Vertrags mit ungünstigen Bedingungen - möglich und wirtschaftlich zumutbar gewesen wäre und er diese Möglichkeit nicht ergriffen hat (vgl. Senatsurteil vom 28. November 2007 - VIII ZR 243/06, NJW 2008, 440 Rn. 15; Milger, NZM 2008, 1, 9).
(2) Nach diesen Maßstäben kann mit der vom Berufungsgericht gegebenen Begründung ein Verstoß gegen das Wirtschaftlichkeitsgebot nicht angenommen werden.
(a) Das Berufungsgericht hat - wie die Revision zu Recht geltend macht - bereits die erforderlichen tatsächlichen Feststellungen dazu, ob die Beklagte nach Abschluss der Mietverträge mit den Klägern die Möglichkeit gehabt hätte, den mit der Dienstleisterin geschlossenen Vertrag - einen Verstoß gegen das Wirtschaftlichkeitsgebot bei der Abwägung zwischen den Kosten und dem Nutzen dieses Vertrags unterstellt - zu kündigen oder abzuändern, nicht getroffen. Es hat sich den Blick hierauf zum einen schon durch die unzutreffende Annahme verstellt, die Pflichtverletzung der Beklagten sei in der "Entscheidung" für das Müllmanagement zu sehen, und zum anderen, indem es rechtfehlerhaft angenommen hat, die Beklagte sei für das Fortbestehen eines "ordnungsgemäßen Kostengrunds" hinsichtlich des hier in Rede stehenden Müllmanagementsystems der externen Dienstleisterin darlegungs- und beweisbelastet (hierzu im Einzelnen nachfolgend unter (c)) und habe einen hinreichend substantiierten Vortrag insoweit nicht gehalten.
(b) Unabhängig davon rechtfertigen die von dem Berufungsgericht bislang getroffenen Feststellungen auch nicht die Annahme, die Beklagte habe als Vermieterin nicht hinreichend auf ein angemessenes Kosten-Nutzen-Verhältnis bei den hier in Rede stehenden Betriebskosten Rücksicht genommen.

</details>

<details><summary>§ 2 Nr. 13–17 BetrKV</summary>

hierzu gehören namentlich die Kosten der Versicherung des Gebäudes gegen Feuer-, Sturm-, Wasser- sowie sonstige Elementarschäden, der Glasversicherung, der Haftpflichtversicherung für das Gebäude, den Öltank und den Aufzug;
14. die Kosten für den Hauswart,
hierzu gehören die Vergütung, die Sozialbeiträge und alle geldwerten Leistungen, die der Eigentümer oder Erbbauberechtigte dem Hauswart für seine Arbeit gewährt, soweit diese nicht die Instandhaltung, Instandsetzung, Erneuerung, Schönheitsreparaturen oder die Hausverwaltung betrifft; soweit Arbeiten vom Hauswart ausgeführt werden, dürfen Kosten für Arbeitsleistungen nach den Nummern 2 bis 10 und 16 nicht angesetzt werden;
15. die Kosten
a) des Betriebs der Gemeinschafts-Antennenanlage,
hierzu gehören die Kosten des Betriebsstroms und die Kosten der regelmäßigen Prüfung ihrer Betriebsbereitschaft einschließlich ihrer Einstellung durch eine Fachkraft,
bis zum 30. Juni 2024 außerdem das Nutzungsentgelt für eine nicht zu dem Gebäude gehörende Antennenanlage sowie die Gebühren, die nach dem Urheberrechtsgesetz für die Kabelweitersendung entstehen,
oder
b) des Betriebs der mit einem Breitbandnetz verbundenen privaten Verteilanlage,
hierzu gehören die Kosten des Betriebsstroms,
bis zum 30. Juni 2024 außerdem die weiteren Kosten entsprechend Buchstabe a, sowie die laufenden monatlichen Grundgebühren für Breitbandanschlüsse,
oder
c) des Betriebs einer gebäudeinternen Verteilanlage, die vollständig mittels Glasfaser mit einem öffentlichen Netz mit sehr hoher Kapazität im Sinne des § 3 Nummer 33 des Telekommunikationsgesetzes verbunden ist, wenn der Mieter seinen Anbieter von öffentlich zugänglichen Telekommunikationsdiensten über seinen Anschluss frei wählen kann,
hierzu gehören die Kosten des Betriebsstroms sowie ein Bereitstellungsentgelt gemäß § 72 Absatz 1 des Telekommunikationsgesetzes;
16. die Kosten des Betriebs der Einrichtungen für die Wäschepflege,
hierzu gehören die Kosten des Betriebsstroms, die Kosten der Überwachung, Pflege und Reinigung der Einrichtungen, der regelmäßigen Prüfung ihrer Betriebsbereitschaft und Betriebssicherheit sowie die Kosten der Wasserversorgung entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind;
17. sonstige Betriebskosten,
hierzu gehören Betriebskosten im Sinne des § 1, die von den Nummern 1 bis 16 nicht erfasst sind.
Für Anlagen, die ab dem 1. Dezember 2021 errichtet worden sind, ist Satz 1 Nummer 15 Buchstabe a und b nicht anzuwenden.

</details>

<details><summary>BGH VIII ZR 62/19, Leitsatz</summary>

Bei einer an den Hausmeister entrichteten Notdienstpauschale handelt es sich nicht um umlagefähige Betriebskosten, sondern um vom Vermieter zu tragende Verwaltungskosten.

</details>

---

## q11 (single)

**Question:** I rent out a condo, and the owners’ association hasn’t approved its annual statement yet. Can I wait for that before sending the tenant’s statement?

**Your reference answer:** No. You still have to send the statement within the one-year deadline of § 556 Abs. 3 S. 2 BGB. The owners' association approving its annual statement is not a precondition (BGH VIII ZR 249/15, LS 1).

**Agent's answer:**

> **No, you generally cannot wait.**
>
> Under German tenancy law, the absence of an approved annual statement (Jahresabrechnung) from the condominium owners’ association does not relieve you of your billing deadline:
>
> ### 1. The Billing Deadline Applies Regardless of Association Approval
> * If the tenancy agreement stipulates that the tenant bears service charges (Betriebskosten) and makes advance payments (Vorauszahlungen), the landlord must issue the statement annually and communicate it to the tenant within twelve months after the end of the billing period (BGH VIII ZR 249/15, Rn. 5, 12–14, decided 2017-01-25).
> * The landlord of a rented condominium (Eigentumswohnung) is fundamentally required to issue this statement within the statutory one-year deadline even if the owners' association has not yet passed a resolution (Beschluss der Wohnungseigentümer) approving the administrator's annual statement (BGH VIII ZR 249/15, Leitsatz and Rn. 15–17).
> * Such a resolution by the owners is not an unwritten prerequisite for issuing the service charge statement to the tenant (BGH VIII ZR 249/15, Leitsatz and Rn. 20–21).
>
> ### 2. Preclusion of Additional Claims (Ausschlussfrist)
> * If the statement is not communicated within the twelve-month deadline, the landlord is barred from claiming any subsequent back payments (Nachforderungen) (BGH VIII ZR 249/15, Rn. 15–17).
> * An exception applies only if the landlord is not responsible for the delay (BGH VIII ZR 249/15, Rn. 15–17 and Rn. 40–42).
> * Although the property manager of the condominium association is generally not considered the landlord’s vicarious agent (Erfüllungsgehilfe) regarding the landlord’s tenancy obligations (BGH VIII ZR 249/15, Leitsatz and Rn. 40–42), simply waiting for the association’s accounts does not exonerate the landlord (BGH VIII ZR 249/15, Rn. 46–48).
> * To be excused from the missed deadline, the landlord must concretely demonstrate what personal efforts were undertaken to ensure a timely statement (BGH VIII ZR 249/15, Leitsatz and Rn. 46–48). Merely stating that the administrator delayed the statement or that the owners' meeting has not taken place is insufficient (BGH VIII ZR 249/15, Rn. 46–48).
>
> ### 3. Facts This Depends On
> * This depends on whether your lease agreement contains a valid agreement to pass on service charges and require advance payments (BGH VIII ZR 249/15, Rn. 5, 12–14). If the lease does not obligate the tenant to bear service charges, no prepayments or subsequent claims can be billed.

**Cited passages:**

<details><summary>BGH VIII ZR 249/15, Rn. 5, 12–14</summary>

Die Revision hat keinen Erfolg.
Diese Beurteilung hält rechtlicher Nachprüfung stand, so dass die Revision zurückzuweisen ist.
Das Berufungsgericht hat rechtsfehlerfrei einen Anspruch des Klägers auf Zahlung restlicher Betriebskosten aus den Betriebskostenabrechnungen für die Jahre 2010, 2011 und 2012 verneint. Die Geltendmachung der Betriebskostennachforderungen für die Jahre 2010 und 2011 ist gemäß § 556 Abs. 3 Satz 3 BGB ausgeschlossen, weil der Kläger die Abrechnungsfrist gemäß § 556 Abs. 3 Satz 2 BGB nicht eingehalten und er nicht dargetan hat, dass er die verspätete Geltendmachung der Nachforderungen nicht zu vertreten hat. Entgegen der Auffassung der Revision hat der Vermieter einer Eigentumswohnung über die Betriebskostenvorauszahlungen des Mieters grundsätzlich auch dann innerhalb der Frist des § 556 Abs. 3 Satz 2 BGB abzurechnen, wenn zu diesem Zeitpunkt ein Beschluss der Wohnungseigentümer gemäß § 28 Abs. 5 WEG über die Jahresabrechnung (§ 28 Abs. 3 WEG) des Verwalters der Wohnungseigentümergemeinschaft noch nicht vorliegt. Hinsichtlich der Betriebskostenabrechnung für das Jahr 2012, die der Kläger der Beklagten rechtzeitig mitgeteilt hat, hat das Berufungsgericht eine Nachforderung des Klägers ebenfalls ohne Rechtsfehler verneint, da diese Forderung jedenfalls durch die vom Kläger vorgenommene Aufrechnung gegen das Kautionsguthaben der Beklagten erloschen ist (§ 389 BGB).
1. Haben die Parteien - wie hier der Fall - im Wohnraummietvertrag vereinbart, dass der Mieter die Betriebskosten trägt und hierfür Vorauszahlungen leistet (§ 535 Abs. 2, § 556 Abs. 1 Satz 1, Abs. 2 BGB), hat der Vermieter über die Vorauszahlungen jährlich abzurechnen (§ 556 Abs. 3 Satz 1 Halbs. 1 BGB). Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen (§ 556 Abs. 3 Satz 2 BGB). Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn der Vermieter hat die verspätete Geltendmachung nicht zu vertreten (§ 556 Abs. 3 Satz 3 BGB). Diese Grundsätze gelten, wie das Berufungsgericht zutreffend angenommen hat, auch für den Vermieter einer Eigentumswohnung.

</details>

<details><summary>BGH VIII ZR 249/15, Leitsatz</summary>

1. Der Vermieter einer Eigentumswohnung hat über die Betriebskostenvorauszahlungen des Mieters grundsätzlich auch dann innerhalb der Jahresfrist des § 556 Abs. 3 Satz 2 BGB abzurechnen, wenn zu diesem Zeitpunkt der Beschluss der Wohnungseigentümer gemäß § 28 Abs. 5 WEG über die Jahresabrechnung (§ 28 Abs. 3 WEG) des Verwalters der Wohnungseigentümergemeinschaft noch nicht vorliegt. Ein solcher Beschluss ist keine (ungeschriebene) Voraussetzung für die Abrechnung der Betriebskosten gemäß § 556 Abs. 3 BGB.
2. Der Verwalter einer Wohnungseigentümergemeinschaft ist als solcher nicht Erfüllungsgehilfe des Wohnungseigentümers nach § 278 BGB in Bezug auf dessen mietvertragliche Pflichten hinsichtlich der Abrechnung der Betriebskosten.
3. Für die nach § 556 Abs. 3 Satz 3 Halbs. 2 BGB mögliche Entlastung des Vermieters hinsichtlich einer von ihm nicht fristgerecht vorgenommenen Betriebskostenabrechnung hat dieser konkret darzulegen, welche Bemühungen er unternommen hat, um eine rechtzeitige Abrechnung sicherzustellen (Bestätigung und Fortführung des Senatsurteils vom 21. Januar 2009, VIII ZR 107/08, NJW 2009, 2197 Rn. 13).

</details>

<details><summary>BGH VIII ZR 249/15, Rn. 15–17</summary>

2. Das Berufungsgericht ist mit Recht und von der Revision insoweit auch nicht angegriffen davon ausgegangen, dass der Kläger im Rahmen der von ihm kalenderjährlich vorgenommenen Abrechnungen der Betriebskosten die Betriebskostenabrechnungen für die Jahre 2010 und 2011 der Beklagten erst mit Schreiben vom 7. Dezember 2013 und damit - da die im Mietvertrag enthaltene handschriftliche Ergänzung der Abrechnungsregelung im Hinblick auf § 556 Abs. 4 BGB unwirksam ist - jeweils nicht innerhalb der Jahresfrist des § 556 Abs. 3 Satz 2 BGB mitgeteilt hat. Die Betriebskostenabrechnung für das Jahr 2010 hätte der Beklagten bis zum 31. Dezember 2011 und diejenige für das Jahr 2011 bis zum 31. Dezember 2012 mitgeteilt werden müssen.
a) Aufgrund dieser erst nach Ablauf der Frist des § 556 Abs. 3 Satz 2 BGB vorgenommenen Abrechnungen der Betriebskosten ist der Kläger hinsichtlich der Abrechnungszeiträume 2010 und 2011 mit Nachforderungen ausgeschlossen (§ 556 Abs. 3 Satz 3 Halbs. 1 BGB), da er nach der insoweit rechtsfehlerfreien Beurteilung des Berufungsgerichts nicht dargetan hat, dass er die verspätete Geltendmachung nicht zu vertreten hat (§ 556 Abs. 3 Satz 3 Halbs. 2 BGB; siehe hierzu nachfolgend unter II 2 b).
Dem Ablauf der Abrechnungsfrist steht nicht entgegen, dass die Wohnungseigentümer erst wenige Tage vor der durch Schreiben des Klägers vom 7. Dezember 2013 erfolgten Mitteilung der Betriebskostenabrechnung an die Beklagte den Beschluss nach § 28 Abs. 5 WEG über die Jahresabrechnung des Verwalters der Wohnungseigentümergemeinschaft (§ 28 Abs. 3 WEG) gefasst hatten. Denn entgegen der Auffassung der Revision ist das Vorliegen eines solchen Beschlusses der Wohnungseigentümer über die Jahresabrechnung - wie das Berufungsgericht mit Recht angenommen hat - keine (ungeschriebene) Voraussetzung für die Abrechnung der Betriebskosten des Vermieters einer vermieteten Eigentumswohnung gegenüber seinem Mieter. Vielmehr hat der Vermieter einer Eigentumswohnung grundsätzlich auch dann innerhalb der Frist des § 556 Abs. 3 Satz 2 BGB über die Vorauszahlung der Betriebskosten abzurechnen und dem Mieter diese Abrechnung mitzuteilen, wenn ein Beschluss der Wohnungseigentümer nach § 28 Abs. 5 WEG über die Jahresabrechnung noch nicht ergangen ist. Diese Frage, die der Senat bisher nicht zu entscheiden gehabt hat, ist in der Rechtsprechung der Instanzgerichte und in der Literatur allerdings umstritten.

</details>

<details><summary>BGH VIII ZR 249/15, Rn. 46–48</summary>

cc) Der Kläger hat aber den Entlastungsbeweis, dass ihn kein eigenes Verschulden an der verspäteten Abrechnung der Betriebskosten der Abrechnungszeiträume 2010 und 2011 trifft, nicht geführt. Er hatte konkret darzulegen, inwiefern er die Verspätung nicht zu vertreten hatte. Hierzu gehörte insbesondere die Darlegung der Bemühungen, die er unternommen hat, um eine rechtzeitige Abrechnung sicherzustellen (vgl. Senatsurteil vom 21. Januar 2009 - VIII ZR 107/08, aaO; vgl. v. Brunn/Emmerich in Bub/Treier, aaO, III. Rn. 262). Hieran fehlt es. Denn nach den rechtsfehlerfreien Feststellungen des Berufungsgerichts hat der Kläger insoweit lediglich geltend gemacht, die bis zum 31. Dezember 2012 tätige Hausverwaltung habe die Wohngeldabrechnung der Hauseigentümer für die Jahre 2010 und 2011 nicht ordnungsgemäß erstellt und sei wegen dieser Versäumnisse von der Wohnungseigentümergemeinschaft zum 31. Dezember 2012 abberufen worden. Die neue, ab 1. Januar 2013 tätige Hausverwaltung sei mit Beschluss der Wohnungseigentümergemeinschaft vom 20. August 2013 zur Abrechnung der Wohngelder für die Jahre 2010 und 2011 beauftragt worden und habe diese - nachdem die bisherige Hausverwaltung zuvor noch erfolglos zur Erstellung ordnungsgemäßer Jahresabrechnungen für die vorbezeichneten Abrechnungszeiträume aufgefordert worden war - im November 2013 fertiggestellt.
Dies genügt nicht. Denn es fehlt jeder Vortrag dazu, was der Kläger selbst veranlasst hat, nachdem für ihn im Laufe des Jahres 2010 erkennbar wurde, dass die bisherige Hausverwaltung die Wohngeldabrechnung, die er als Grundlage für die von ihm selbst erstellte Betriebskostenabrechnung benötigte, nicht rechtzeitig erstellen würde oder die schließlich erstellte Abrechnung so fehlerhaft war, dass sie sich nicht als Grundlage für die Betriebskostenabrechnung eignete. Übergangenen Sachvortrag zeigt die Revision nicht auf. Soweit sie sich auf den Schriftsatz des Klägers vom 8. September 2014 beruft, enthält dieser nur die vorstehend genannte Darstellung der Vorgehensweise der Wohnungseigentümergemeinschaft, die den Schluss, der Kläger habe den ihm obliegenden Entlastungsbeweis geführt, nicht zulässt.
3. Hinsichtlich des Abrechnungszeitraums 2012 ist die Betriebskostenabrechnung vom 7. Dezember 2013 hingegen, wie das Berufungsgericht zutreffend angenommen hat und wovon auch die Parteien im Revisionsverfahren ausgehen, rechtzeitig innerhalb der Frist des § 556 Abs. 3 Satz 2 BGB erfolgt. Trotzdem steht dem Kläger der hinsichtlich dieser Betriebskostenabrechnung geltend gemachte Anspruch auf Nachzahlung von Betriebskosten in Höhe von 553,38 € nicht zu, da diese Forderung gemäß § 389 BGB durch die vom Kläger vorgenommene Aufrechnung gegen den Kautionsrückzahlungsanspruch der Beklagten (640,45 €) erloschen ist.

</details>

---

## q12 (single)

**Question:** The WEG property manager sent me the figures late, so I missed the deadline for the tenant’s statement. Can I blame the manager and still claim the back payment?

**Your reference answer:** Not automatically. The WEG manager's fault isn't attributed to you under § 278 BGB, but to keep the back payment you have to show concretely that you yourself weren't responsible for the delay and did what you could to get the statement out in time (BGH VIII ZR 249/15, LS 2 and 3).

**Agent's answer:**

> Under German tenancy law, simply blaming the late figures from the property manager of the condominium owners’ association (*Verwalter einer Wohnungseigentümergemeinschaft*) is **not** enough to preserve your claim to a back payment (*Nachforderung*).
>
> ---
>
> ### 1. Prerequisite: The Lease Agreement (*Umlagevereinbarung*)
> * Whether you can bill operating costs (*Betriebskosten*) and demand prepayments (*Vorauszahlungen*) or back payments depends on the tenancy contract containing an agreement that the tenant bears these costs (**§ 556 BGB**; **BGH VIII ZR 249/15, Rn. 5, 12–14**). Without such a contractual basis, no operating costs can be charged.
>
> ---
>
> ### 2. The Billing Deadline and Preclusion
> * Operating cost prepayments must be billed annually, and the statement must be provided to the tenant no later than the end of the twelfth month following the end of the billing period (**§ 556 BGB**; **BGH VIII ZR 249/15, Rn. 5, 12–14**).
> * Once this deadline expires, claiming a back payment is barred unless the landlord is not responsible for the late submission (*es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten*, **§ 556 BGB**; **BGH VIII ZR 249/15, Rn. 5, 12–14**; **BGH VIII ZR 249/15, Rn. 15–17**).
>
> ---
>
> ### 3. Status of the WEG Property Manager
> * The manager of a condominium owners’ association is as such **not** a vicarious agent (*kein Erfüllungsgehilfe*) of the apartment owner regarding the landlord’s tenancy obligations to settle service charges (**BGH VIII ZR 249/15, Leitsatz**; **BGH VIII ZR 249/15, Rn. 40–42**).
> * As a result, the fault of the property manager is not automatically imputed to the landlord (**BGH VIII ZR 249/15, Rn. 40–42**).
>
> ---
>
> ### 4. Why Blaming the Manager is Not Enough
> Even though the manager's fault is not automatically attributed to you, you cannot simply rely on the manager's delay:
>
> * **No Dependency on WEG Approvals:** A landlord of a condominium unit must generally bill the tenant within the 12-month period even if the owners' resolution approving the property manager's annual statement (*Beschluss über die Jahresabrechnung*) has not yet taken place (**BGH VIII ZR 249/15, Leitsatz**; **BGH VIII ZR 249/15, Rn. 15–17**).
> * **Proof of Own Lack of Fault (*Entlastung*):** The landlord must demonstrate that they bear no personal fault (*kein eigenes Verschulden*) for the delay (**BGH VIII ZR 249/15, Rn. 40–42**; **BGH VIII ZR 249/15, Rn. 46–48**).
> * **Requirement of Concrete Efforts (*Bemühungen*):** To establish that the landlord is not responsible for missing the deadline, the landlord must specifically state and prove what concrete efforts they personally undertook to ensure a timely statement (**BGH VIII ZR 249/15, Leitsatz**; **BGH VIII ZR 249/15, Rn. 46–48**).
> * **Passive Waiting Does Not Suffice:** Merely stating that the property manager failed to prepare the figures on time is inadequate if the landlord fails to show what steps they personally initiated once it became apparent during the year that the manager was delayed (**BGH VIII ZR 249/15, Rn. 46–48**).
>
> ### Conclusion
> If you merely waited for the manager to deliver the figures without taking active, demonstrable steps to obtain the numbers and issue the statement on time, you bear personal responsibility for the delay, and your back payment is excluded (**§ 556 BGB**; **BGH VIII ZR 249/15, Rn. 15–17**; **BGH VIII ZR 249/15, Rn. 46–48**).

**Cited passages:**

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>BGH VIII ZR 249/15, Rn. 5, 12–14</summary>

Die Revision hat keinen Erfolg.
Diese Beurteilung hält rechtlicher Nachprüfung stand, so dass die Revision zurückzuweisen ist.
Das Berufungsgericht hat rechtsfehlerfrei einen Anspruch des Klägers auf Zahlung restlicher Betriebskosten aus den Betriebskostenabrechnungen für die Jahre 2010, 2011 und 2012 verneint. Die Geltendmachung der Betriebskostennachforderungen für die Jahre 2010 und 2011 ist gemäß § 556 Abs. 3 Satz 3 BGB ausgeschlossen, weil der Kläger die Abrechnungsfrist gemäß § 556 Abs. 3 Satz 2 BGB nicht eingehalten und er nicht dargetan hat, dass er die verspätete Geltendmachung der Nachforderungen nicht zu vertreten hat. Entgegen der Auffassung der Revision hat der Vermieter einer Eigentumswohnung über die Betriebskostenvorauszahlungen des Mieters grundsätzlich auch dann innerhalb der Frist des § 556 Abs. 3 Satz 2 BGB abzurechnen, wenn zu diesem Zeitpunkt ein Beschluss der Wohnungseigentümer gemäß § 28 Abs. 5 WEG über die Jahresabrechnung (§ 28 Abs. 3 WEG) des Verwalters der Wohnungseigentümergemeinschaft noch nicht vorliegt. Hinsichtlich der Betriebskostenabrechnung für das Jahr 2012, die der Kläger der Beklagten rechtzeitig mitgeteilt hat, hat das Berufungsgericht eine Nachforderung des Klägers ebenfalls ohne Rechtsfehler verneint, da diese Forderung jedenfalls durch die vom Kläger vorgenommene Aufrechnung gegen das Kautionsguthaben der Beklagten erloschen ist (§ 389 BGB).
1. Haben die Parteien - wie hier der Fall - im Wohnraummietvertrag vereinbart, dass der Mieter die Betriebskosten trägt und hierfür Vorauszahlungen leistet (§ 535 Abs. 2, § 556 Abs. 1 Satz 1, Abs. 2 BGB), hat der Vermieter über die Vorauszahlungen jährlich abzurechnen (§ 556 Abs. 3 Satz 1 Halbs. 1 BGB). Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen (§ 556 Abs. 3 Satz 2 BGB). Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn der Vermieter hat die verspätete Geltendmachung nicht zu vertreten (§ 556 Abs. 3 Satz 3 BGB). Diese Grundsätze gelten, wie das Berufungsgericht zutreffend angenommen hat, auch für den Vermieter einer Eigentumswohnung.

</details>

<details><summary>BGH VIII ZR 249/15, Rn. 15–17</summary>

2. Das Berufungsgericht ist mit Recht und von der Revision insoweit auch nicht angegriffen davon ausgegangen, dass der Kläger im Rahmen der von ihm kalenderjährlich vorgenommenen Abrechnungen der Betriebskosten die Betriebskostenabrechnungen für die Jahre 2010 und 2011 der Beklagten erst mit Schreiben vom 7. Dezember 2013 und damit - da die im Mietvertrag enthaltene handschriftliche Ergänzung der Abrechnungsregelung im Hinblick auf § 556 Abs. 4 BGB unwirksam ist - jeweils nicht innerhalb der Jahresfrist des § 556 Abs. 3 Satz 2 BGB mitgeteilt hat. Die Betriebskostenabrechnung für das Jahr 2010 hätte der Beklagten bis zum 31. Dezember 2011 und diejenige für das Jahr 2011 bis zum 31. Dezember 2012 mitgeteilt werden müssen.
a) Aufgrund dieser erst nach Ablauf der Frist des § 556 Abs. 3 Satz 2 BGB vorgenommenen Abrechnungen der Betriebskosten ist der Kläger hinsichtlich der Abrechnungszeiträume 2010 und 2011 mit Nachforderungen ausgeschlossen (§ 556 Abs. 3 Satz 3 Halbs. 1 BGB), da er nach der insoweit rechtsfehlerfreien Beurteilung des Berufungsgerichts nicht dargetan hat, dass er die verspätete Geltendmachung nicht zu vertreten hat (§ 556 Abs. 3 Satz 3 Halbs. 2 BGB; siehe hierzu nachfolgend unter II 2 b).
Dem Ablauf der Abrechnungsfrist steht nicht entgegen, dass die Wohnungseigentümer erst wenige Tage vor der durch Schreiben des Klägers vom 7. Dezember 2013 erfolgten Mitteilung der Betriebskostenabrechnung an die Beklagte den Beschluss nach § 28 Abs. 5 WEG über die Jahresabrechnung des Verwalters der Wohnungseigentümergemeinschaft (§ 28 Abs. 3 WEG) gefasst hatten. Denn entgegen der Auffassung der Revision ist das Vorliegen eines solchen Beschlusses der Wohnungseigentümer über die Jahresabrechnung - wie das Berufungsgericht mit Recht angenommen hat - keine (ungeschriebene) Voraussetzung für die Abrechnung der Betriebskosten des Vermieters einer vermieteten Eigentumswohnung gegenüber seinem Mieter. Vielmehr hat der Vermieter einer Eigentumswohnung grundsätzlich auch dann innerhalb der Frist des § 556 Abs. 3 Satz 2 BGB über die Vorauszahlung der Betriebskosten abzurechnen und dem Mieter diese Abrechnung mitzuteilen, wenn ein Beschluss der Wohnungseigentümer nach § 28 Abs. 5 WEG über die Jahresabrechnung noch nicht ergangen ist. Diese Frage, die der Senat bisher nicht zu entscheiden gehabt hat, ist in der Rechtsprechung der Instanzgerichte und in der Literatur allerdings umstritten.

</details>

<details><summary>BGH VIII ZR 249/15, Leitsatz</summary>

1. Der Vermieter einer Eigentumswohnung hat über die Betriebskostenvorauszahlungen des Mieters grundsätzlich auch dann innerhalb der Jahresfrist des § 556 Abs. 3 Satz 2 BGB abzurechnen, wenn zu diesem Zeitpunkt der Beschluss der Wohnungseigentümer gemäß § 28 Abs. 5 WEG über die Jahresabrechnung (§ 28 Abs. 3 WEG) des Verwalters der Wohnungseigentümergemeinschaft noch nicht vorliegt. Ein solcher Beschluss ist keine (ungeschriebene) Voraussetzung für die Abrechnung der Betriebskosten gemäß § 556 Abs. 3 BGB.
2. Der Verwalter einer Wohnungseigentümergemeinschaft ist als solcher nicht Erfüllungsgehilfe des Wohnungseigentümers nach § 278 BGB in Bezug auf dessen mietvertragliche Pflichten hinsichtlich der Abrechnung der Betriebskosten.
3. Für die nach § 556 Abs. 3 Satz 3 Halbs. 2 BGB mögliche Entlastung des Vermieters hinsichtlich einer von ihm nicht fristgerecht vorgenommenen Betriebskostenabrechnung hat dieser konkret darzulegen, welche Bemühungen er unternommen hat, um eine rechtzeitige Abrechnung sicherzustellen (Bestätigung und Fortführung des Senatsurteils vom 21. Januar 2009, VIII ZR 107/08, NJW 2009, 2197 Rn. 13).

</details>

<details><summary>BGH VIII ZR 249/15, Rn. 40–42</summary>

b) Das Berufungsgericht hat - entgegen der Auffassung der Revision - ebenfalls rechtsfehlerfrei das Vorliegen des in § 556 Abs. 3 Satz 3 Halbs. 2 BGB geregelten Ausnahmetatbestandes verneint. Nach dieser Vorschrift ist die Geltendmachung einer Nachforderung durch den Vermieter nach Ablauf der Abrechnungsfrist des § 556 Abs. 3 Satz 2 BGB dann nicht ausgeschlossen, wenn der Vermieter die verspätete Geltendmachung nicht zu vertreten hat. Für das Vertretenmüssen im Sinne von § 556 Abs. 3 Satz 3 Halbs. 2 BGB gilt § 276 BGB; nach § 278 BGB hat der Vermieter auch ein Fehlverhalten seiner Erfüllungsgehilfen zu vertreten (BGH, Urteil vom 21. Januar 2009 - VIII ZR 107/08, aaO Rn. 13).
Hiervon ausgehend muss sich der Kläger hier zwar ein Verschulden des (früheren) Verwalters der Wohnungseigentümergemeinschaft nicht zurechnen lassen, weil dieser nicht Erfüllungsgehilfe des Klägers zur Erstellung der mietrechtlichen Betriebskostenabrechnung gewesen ist. Gleichwohl kann der Kläger eine Nachforderung nicht geltend machen, denn er hat nicht einmal im Ansatz dargelegt, dass ihn auch kein eigenes Verschulden an der verspäteten Abrechnung für die Jahre 2010 und 2011 trifft.
aa) Der Verwalter einer Wohnungseigentümergemeinschaft ist, wie das Berufungsgericht zutreffend angenommen hat und wovon auch die Revision ausgeht, grundsätzlich nicht Erfüllungsgehilfe des Wohnungseigentümers nach § 278 BGB in Bezug auf dessen mietvertragliche Pflichten hinsichtlich der Abrechnung der Betriebskosten (vgl. LG Frankfurt am Main, Urteil vom 14. Oktober 2011 - 2-09 S 2/11, juris Rn. 19; AG Singen, Beschluss vom 24. Februar 2004 - 7 UR WEG 48/03, juris; AG Erfurt, aaO; Palandt/Weidenkaff, aaO; MünchKommBGB/Schmid/Zehelein, aaO, § 556 Rn. 55; Blank in Blank/Börstinghaus aaO Rn. 209; BeckOK-BGB/Ehlert, Stand 1. Mai 2014, § 556 Rn. 65c; BeckOGK/Drager, aaO; Langenberg/Zehelein, Betriebs- und Heizkostenrecht, 8. Aufl., G Rn. 59; Jennißen, Die Verwalterabrechnung nach dem WEG, aaO Rn. 1128; Drasdo, NZM 2004, 372, 374; Flatow, WuM 2010, 606, 611; Schmid, MDR 2015, 985, 986; aA wohl AG Potsdam, WuM 2003, 456; Gies, NZM 2002, 514; Staudinger/Weitemeyer, aaO Rn. 109; Emmerich in Emmerich/Sonnenschein, aaO Rn. 64; Riecke in Riecke/Schmid, aaO Rn. 26).

</details>

<details><summary>BGH VIII ZR 249/15, Rn. 46–48</summary>

cc) Der Kläger hat aber den Entlastungsbeweis, dass ihn kein eigenes Verschulden an der verspäteten Abrechnung der Betriebskosten der Abrechnungszeiträume 2010 und 2011 trifft, nicht geführt. Er hatte konkret darzulegen, inwiefern er die Verspätung nicht zu vertreten hatte. Hierzu gehörte insbesondere die Darlegung der Bemühungen, die er unternommen hat, um eine rechtzeitige Abrechnung sicherzustellen (vgl. Senatsurteil vom 21. Januar 2009 - VIII ZR 107/08, aaO; vgl. v. Brunn/Emmerich in Bub/Treier, aaO, III. Rn. 262). Hieran fehlt es. Denn nach den rechtsfehlerfreien Feststellungen des Berufungsgerichts hat der Kläger insoweit lediglich geltend gemacht, die bis zum 31. Dezember 2012 tätige Hausverwaltung habe die Wohngeldabrechnung der Hauseigentümer für die Jahre 2010 und 2011 nicht ordnungsgemäß erstellt und sei wegen dieser Versäumnisse von der Wohnungseigentümergemeinschaft zum 31. Dezember 2012 abberufen worden. Die neue, ab 1. Januar 2013 tätige Hausverwaltung sei mit Beschluss der Wohnungseigentümergemeinschaft vom 20. August 2013 zur Abrechnung der Wohngelder für die Jahre 2010 und 2011 beauftragt worden und habe diese - nachdem die bisherige Hausverwaltung zuvor noch erfolglos zur Erstellung ordnungsgemäßer Jahresabrechnungen für die vorbezeichneten Abrechnungszeiträume aufgefordert worden war - im November 2013 fertiggestellt.
Dies genügt nicht. Denn es fehlt jeder Vortrag dazu, was der Kläger selbst veranlasst hat, nachdem für ihn im Laufe des Jahres 2010 erkennbar wurde, dass die bisherige Hausverwaltung die Wohngeldabrechnung, die er als Grundlage für die von ihm selbst erstellte Betriebskostenabrechnung benötigte, nicht rechtzeitig erstellen würde oder die schließlich erstellte Abrechnung so fehlerhaft war, dass sie sich nicht als Grundlage für die Betriebskostenabrechnung eignete. Übergangenen Sachvortrag zeigt die Revision nicht auf. Soweit sie sich auf den Schriftsatz des Klägers vom 8. September 2014 beruft, enthält dieser nur die vorstehend genannte Darstellung der Vorgehensweise der Wohnungseigentümergemeinschaft, die den Schluss, der Kläger habe den ihm obliegenden Entlastungsbeweis geführt, nicht zulässt.
3. Hinsichtlich des Abrechnungszeitraums 2012 ist die Betriebskostenabrechnung vom 7. Dezember 2013 hingegen, wie das Berufungsgericht zutreffend angenommen hat und wovon auch die Parteien im Revisionsverfahren ausgehen, rechtzeitig innerhalb der Frist des § 556 Abs. 3 Satz 2 BGB erfolgt. Trotzdem steht dem Kläger der hinsichtlich dieser Betriebskostenabrechnung geltend gemachte Anspruch auf Nachzahlung von Betriebskosten in Höhe von 553,38 € nicht zu, da diese Forderung gemäß § 389 BGB durch die vom Kläger vorgenommene Aufrechnung gegen den Kautionsrückzahlungsanspruch der Beklagten (640,45 €) erloschen ist.

</details>

---

## q13 (single)

**Question:** Our standard lease lists a monthly administration fee separately from the rent. Is that allowed?

**Your reference answer:** No, unless the lease makes clear the fee is part of the base rent. Otherwise a separate administration fee in a standard lease deviates from § 556 Abs. 1 BGB to the tenant's disadvantage and is void (BGH VIII ZR 254/17; the judgment cites § 556 Abs. 4 BGB, now § 556 Abs. 5).

**Agent's answer:**

> **Generally, no.** In a standard residential lease (*formularmäßiger Wohnraummietvertrag*), listing a separate monthly administration fee (*Verwaltungskostenpauschale*) is legally invalid.
>
> ### 1. Legal Rules
> * **Excluded from operating costs:** Administration costs (*Verwaltungskosten*) are expressly excluded from the definition of operating costs (*Betriebskosten*) under **§ 1 BetrKV** (also noted in **BGH VIII ZR 254/17, Rn. 13–17**).
> * **Restrictions on cost-shifting:** Under § 556 Abs. 1 BGB, parties to a residential lease may only agree that the tenant bears operating costs defined in the *Betriebskostenverordnung* (**BGH VIII ZR 254/17, Rn. 4, 10–12**). Under § 556 Abs. 4 BGB, contractual arrangements that deviate from this to the tenant's disadvantage are invalid (**BGH VIII ZR 254/17, Rn. 13–17**). Because the statutory list of billable operating costs is exhaustive, landlords cannot contractually extend it to include general administration costs (**BGH VIII ZR 254/17, Rn. 13–17**).
>
> ### 2. The Ruling of the Federal Court of Justice (BGH)
> In its decision of 19 December 2018, the Federal Court of Justice (*Bundesgerichtshof*) established:
> * A separately specified administration fee (*Verwaltungskostenpauschale*) in a standard residential lease constitutes a prohibited deviation from § 556 Abs. 1 BGB to the tenant's detriment and is invalid under § 556 Abs. 4 BGB, unless the lease contract unequivocally makes clear that the fee is an integral part of the basic rent (*Grundmiete / Nettomiete*) (**BGH VIII ZR 254/17, Leitsatz**).
> * Where such a clause is invalid, the tenant is not obligated to pay the fee and is entitled to a refund of any amounts paid without legal ground pursuant to § 812 Abs. 1 Satz 1 Alt. 1 BGB (**BGH VIII ZR 254/17, Rn. 4, 10–12**).
>
> ### 3. What Is Permitted
> * **Factoring into basic rent:** A landlord is free to factor administrative expenses directly into the basic rent (*Grundmiete / Nettomiete*) (**BGH VIII ZR 254/17, Rn. 13–17**).
> * **Disclosing internal calculations:** A landlord may disclose their internal cost calculation within the lease agreement (for example, stating which portion of the basic rent reflects administrative overhead), provided the total sum forms a single unified starting rent that is subject to standard rent-increase rules under § 558 BGB rather than functioning as an independent, separately billable charge (**BGH VIII ZR 254/17, Rn. 13–17**).
>
> ---
> *Whether your clause is valid depends on the exact wording of the lease—specifically, whether it unmistakably designates the fee as an integrated component of the basic rent rather than a separate surcharge. For evaluating or adjusting standard contract templates, consult a tenancy lawyer (*Fachanwalt für Mietrecht*).*
>
> ⚠ Citation check: these citations could not be matched to the retrieved passages, verify them before relying on this answer: § 556 Abs. 1 BGB; § 556 Abs. 4 BGB; § 558 BGB

**Cited passages:**

<details><summary>§ 1 BetrKV</summary>

(1) Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Sach- und Arbeitsleistungen des Eigentümers oder Erbbauberechtigten dürfen mit dem Betrag angesetzt werden, der für eine gleichwertige Leistung eines Dritten, insbesondere eines Unternehmers, angesetzt werden könnte; die Umsatzsteuer des Dritten darf nicht angesetzt werden.
(2) Zu den Betriebskosten gehören nicht:
1. die Kosten der zur Verwaltung des Gebäudes erforderlichen Arbeitskräfte und Einrichtungen, die Kosten der Aufsicht, der Wert der vom Vermieter persönlich geleisteten Verwaltungsarbeit, die Kosten für die gesetzlichen oder freiwilligen Prüfungen des Jahresabschlusses und die Kosten für die Geschäftsführung (Verwaltungskosten),
2. die Kosten, die während der Nutzungsdauer zur Erhaltung des bestimmungsmäßigen Gebrauchs aufgewendet werden müssen, um die durch Abnutzung, Alterung und Witterungseinwirkung entstehenden baulichen oder sonstigen Mängel ordnungsgemäß zu beseitigen (Instandhaltungs- und Instandsetzungskosten).

</details>

<details><summary>BGH VIII ZR 254/17, Rn. 13–17</summary>

Zum Schutz des Mieters von Wohnraum sieht § 556 Abs. 4 BGB allerdings vor, dass Vereinbarungen, die zum Nachteil des Mieters von den Bestimmungen des § 556 Abs. 1, Abs. 2 Satz 2 und Abs. 3 BGB abweichen, unwirksam sind. Dies gilt sowohl für Individualvereinbarungen, als auch für - hier nach den rechtsfehlerfreien und unangegriffenen Feststellungen des Berufungsgerichts vorliegende - Allgemeine Geschäftsbedingungen. Deshalb können in der Wohnraummiete nur die enumerativ in der Betriebskostenverordnung aufgezählten Bewirtschaftungskosten als Nebenkosten (Betriebskosten) vereinbart werden, nicht aber (allgemeine) Verwaltungskosten, die nach der ausdrücklichen Regelung in § 1 Abs. 2 Nr. 1 der Verordnung über die Aufstellung von Betriebskosten (Betriebskostenverordnung - BetrKV) in der Wohnraummiete nicht als Betriebskosten umgelegt werden können. Dementsprechend führt bereits die Gesetzesbegründung des Entwurfs eines Gesetzes zur Neugliederung, Vereinfachung und Reform des Mietrechts (Mietrechtsreformgesetz) explizit aus, dass die umlagefähigen Betriebskosten abschließend aufgezählt sind und eine vertragliche Erweiterung, zum Beispiel auf Verwaltungskosten, nicht möglich ist (vgl. BT-Drucks. 14/4553, S. 50).
2. In der im vorliegenden Mietvertrag vereinbarten Verwaltungskostenpauschale hat das Berufungsgericht rechtsfehlerfrei eine gegen § 556 Abs. 1 BGB verstoßende und deshalb gemäß § 556 Abs. 4 BGB unwirksame Vereinbarung gesehen.
Entgegen der Auffassung der Revision ist dies nicht deshalb anders zu beurteilen, weil es sich bei der Verwaltungskostenpauschale um eine "zusätzliche Preishauptabrede über die Nettomiete" handelte und die Beklagte hier nur ihre Kalkulation dahingehend offengelegt habe, dass in der Netto- oder Grundmiete Verwaltungskosten in Höhe von monatlich 34,38 € enthalten seien.
Allerdings trifft es - wie auch das Berufungsgericht richtig gesehen hat - zu, dass es dem Vermieter freisteht, im Mietvertrag eine Aufschlüsselung der vereinbarten (Grund-)Miete beziehungsweise (Netto-)Miete vorzunehmen und dadurch einen - aus Sicht des Mieters allerdings regelmäßig belanglosen - Hinweis auf seine interne Kalkulation zu geben (vgl. Senatsbeschluss vom 30. Mai 2017 - VIII ZR 31/17, NJW-RR 2017, 981 Rn. 7). Dies gilt auch für Verwaltungskosten, die der Vermieter ebenso wie sonstige nicht gesondert umlegbare Kosten in die Grundmiete "einpreisen" oder auch separat als weiteren Bestandteil der Grundmiete angeben kann, mit der Folge, dass der Gesamtbetrag die Ausgangsmiete bildet, die im Falle späterer Mieterhöhungen der ortsüblichen Vergleichsmiete gegenüberzustellen ist (§ 558 Abs. 1 BGB).
Das Berufungsgericht hat jedoch zutreffend angenommen, dass in der hier formularmäßig vereinbarten "Verwaltungskostenpauschale" eine bloße Offenlegung als Bestandteil der Nettomiete nicht gesehen werden kann.

</details>

<details><summary>BGH VIII ZR 254/17, Rn. 4, 10–12</summary>

Die Revision hat keinen Erfolg.
Diese Beurteilung hält rechtlicher Nachprüfung stand, so dass die Revision zurückzuweisen ist. Das Berufungsgericht hat rechtsfehlerfrei angenommen, dass die im Mietvertrag vereinbarte Verwaltungskostenpauschale wegen Verstoßes gegen § 556 Abs. 4 BGB unwirksam ist und dem Kläger deshalb aus § 812 Abs. 1 Satz 1 Alt. 1 BGB ein Anspruch auf Rückzahlung der hierauf ohne Rechtsgrund erbrachten Zahlungen zusteht.
1. Gemäß § 556 Abs. 1, 2 BGB können die Parteien eines Wohnraummietvertrages vereinbaren, dass der Mieter bestimmte, in der Betriebskostenverordnung bezeichnete Betriebskosten trägt, entweder als Pauschale oder im Wege (angemessener) Vorauszahlungen mit Abrechnungspflicht (§ 556 Abs. 2, 3 BGB). Einer solchen Vereinbarung bedarf es, weil der Vermieter nach der Grundregel des § 535 Abs. 1 Satz 3 BGB die auf der Mietsache ruhenden Lasten zu tragen hat. Die Miete ist von ihrer gesetzgeberischen Ausgestaltung her eine Inklusivmiete, so dass die aus der Gebrauchsgewährung herrührenden Kosten grundsätzlich mit der vereinbarten Miete abgegolten werden (vgl. BGH, Urteil vom 2. Mai 2012 - XII ZR 88/10, NJW-RR 2012, 1034 Rn. 13; BT-Drucks. 14/4553, S. 50; MünchKommBGB/Schmid/Zehelein, 7. Aufl., § 556 Rn. 5).
Hintergrund für die - in der Praxis auch seit langem allgemein übliche - gesonderte Umlage bestimmter Betriebskosten ist letztlich eine vereinfachte Anpassung bei Kostensteigerungen in diesem überschaubaren und klar definierten Bereich. Insoweit soll der Vermieter bei Kostensteigerungen nicht auf das - wesentlich aufwendigere - Verfahren einer Mieterhöhung nach § 558 BGB (Vergleichsmietenverfahren) verwiesen sein (vgl. schon BT-Drucks. VI/2421, S. 4; BT-Drucks. 7/2011, S. 8). Vielmehr kann er im Fall einer Betriebskostenpauschale unter den Voraussetzungen des § 560 Abs. 1 BGB eine Anpassung im Wege einer Erklärung in Textform vornehmen, während bei Vorauszahlungen von Betriebskosten jeder Partei diese Anpassungsmöglichkeit nach einer Abrechnung eröffnet ist.

</details>

<details><summary>BGH VIII ZR 254/17, Leitsatz</summary>

Eine in einem formularmäßigen Wohnraummietvertrag gesondert ausgewiesene Verwaltungskostenpauschale stellt eine zum Nachteil des Mieters von § 556 Abs. 1 BGB abweichende und damit gemäß § 556 Abs. 4 BGB unwirksame Vereinbarung dar, sofern aus dem Mietvertrag nicht eindeutig hervorgeht, dass es sich bei dieser Pauschale um einen Teil der Grundmiete (Nettomiete) handelt.

</details>

---

## q14 (single)

**Question:** We rent our smoke detectors instead of buying them. Can I pass the rental fee on to the tenants?

**Your reference answer:** No. Rental fees for smoke detectors are treated like purchase costs, not operating costs, so they can't be passed on (BGH VIII ZR 379/20).

**Agent's answer:**

> **No, you cannot pass the rental fee for smoke detectors on to your tenants.**
>
> ### Legal Assessment
> * **Not an eligible service charge:** Costs for renting smoke detectors (*Kosten für die Miete von Rauchwarnmeldern*) are not considered "other service charges" (*sonstige Betriebskosten*). Because they are equivalent to acquisition costs (*Kosten für den Erwerb*), they are non-recoverable expenses under service charge law (*betriebskostenrechtlich nicht umlagefähige Aufwendungen*) (**BGH VIII ZR 379/20, Leitsatz**).
> * **Reasoning:** Costs for acquiring operating equipment are not billable to tenants. A landlord cannot circumvent this principle by choosing to rent the equipment instead of buying it (**BGH VIII ZR 379/20, Rn. 33–35**).
>
> ---
>
> ### Distinction: Maintenance vs. Rental
> While the **rental fee** (*Mietkosten*) cannot be passed on:
> * The costs for regularly checking and ensuring the operational readiness (maintenance / *Wartung*) of smoke detectors can be passed on to residential tenants as "other service charges" (*sonstige Betriebskosten*) (**BGH VIII ZR 117/21, Leitsatz**).
> * Passing on such maintenance costs depends on having an effective cost-allocation agreement (*Umlagevereinbarung*) in the lease that covers fire protection and alarm systems or explicitly designates these operating costs (**BGH VIII ZR 117/21, Leitsatz**; **BGH VIII ZR 117/21, Rn. 50–52**).

**Cited passages:**

<details><summary>BGH VIII ZR 379/20, Leitsatz</summary>

Bei den Kosten für die Miete von Rauchwarnmeldern handelt es sich nicht um sonstige Betriebskosten im Sinne von § 2 Nr. 17 BetrKV, sondern - da sie den Kosten für den Erwerb von Rauchwarnmeldern gleichzusetzen sind - um betriebskostenrechtlich nicht umlagefähige Aufwendungen.

</details>

<details><summary>BGH VIII ZR 379/20, Rn. 33–35</summary>

Zwar ist der Klägerin dieser Aufwand - wie das Berufungsgericht zutreffend erkannt hat - erst infolge neuerer technischer und damit einhergehender rechtlicher Entwicklungen (hier: Pflicht zur Ausstattung von Wohnungen mit Rauchwarnmeldern gemäß der ab dem 1. April 2013 geltenden Regelung des § 49 Abs. 7 BauO NRW; seit dem 1. Januar 2019 durch § 47 Abs. 3 BauO NRW abgelöst) entstanden. Ihrem Wesen nach sind diese Kosten indes nicht als umlagefähige Betriebskosten einzustufen (so etwa - jedenfalls im Ergebnis - auch: LG Hagen, ZMR 2016, 701; LG Düsseldorf, ZMR 2020, 650, 651; LG Berlin, WuM 2021, 367; Langenberg/Zehelein, aaO A Rn. 37, 309; Wall, aaO Rn. 4778 f.; MünchKommBGB/Zehelein, aaO, § 2 BetrKV Rn. 79; Schmidt-Futterer/Lehmann-Richter, aaO, § 556 BGB Rn. 304; Blank/Börstinghaus, Miete, 6. Aufl., § 556 BGB Rn. 100; BeckOGK-BGB/Drager, Stand: 1. Juli 2021, § 556 Rn. 67.1; aA etwa LG Magdeburg, NJW 2012, 544, 545; AG Hamburg-Altona, ZMR 2014, 801, 802; Pistorius, ZMR 2011, 934).
aa) Kosten für die Miete von Rauchwarnmeldern fallen ausschließlich dann an, wenn der Vermieter sich - was allein in seiner Entscheidungsmacht steht - dazu entschließt, die in der Mietwohnung zu installierenden Rauchwarnmelder nicht zu Eigentum zu erwerben, sondern sie stattdessen anzumieten. Wie oben aufgezeigt, wären die Kosten für den Erwerb von Rauchwarnmeldern - selbst wenn sie infolge einer Fremdfinanzierung nicht nur einmalig, sondern periodisch und deshalb möglicherweise laufend im Sinne von § 1 Abs. 1 Satz 1 BetrKV anfielen - nicht umlagefähig.
Es ließe sich mit dem oben aufgezeigten in den Gesetzesmaterialien eindeutig zum Ausdruck gebrachten Willen des Verordnungsgebers, dass Kosten für die Anschaffung von Betriebsmitteln grundsätzlich nicht zu den umlagefähigen Betriebskosten gehören (vgl. BR-Drucks. 568/03, S. 29), nicht vereinbaren, wenn man die - vom Vermieter anstatt eines Erwerbs gewählte - Miete von Rauchwarnmeldern demgegenüber als umlagefähige (sonstige) Betriebskosten einordnete. Denn das bedeutete im Ergebnis, dass dem Vermieter ein Weg eröffnet würde, auf einfache Weise - nicht nur im Fall der Ausstattung einer Wohnung mit Rauchwarnmeldern, sondern auch in anderen Fällen, in denen er das Mietobjekt mit bestimmten Einrichtungen zu versehen hätte - die im Grundsatz ihm zugewiesene Belastung mit Anschaffungskosten zu umgehen, indem er die allein ihm obliegende wirtschaftliche Entscheidung zugunsten einer Miete anstatt eines Kaufs des fraglichen Betriebsmittels träfe.

</details>

<details><summary>BGH VIII ZR 117/21, Leitsatz</summary>

1. Die Kosten eines externen Dienstleisters für die regelmäßige Kontrolle der Restmüllbehälter des Mietobjekts auf Einhaltung der satzungsmäßigen Vorgaben für die Mülltrennung und für die bei fehlerhafter Abfalltrennung erfolgende Nachsortierung von Hand sind im Wohnraummietverhältnis gemäß § 2 Nr. 8 BetrKV auf den Mieter umlegbare Betriebskosten.
2. Die Kosten für die regelmäßige Prüfung und Sicherstellung der Betriebsbereitschaft von in den Mieträumen angebrachten Rauchwarnmeldern sind im Wohnraummietverhältnis als "sonstige Betriebskosten" im Sinne von § 2 Nr. 17 BetrKV auf den Mieter umlegbar. Sie werden von einer vertraglichen Umlagevereinbarung erfasst, welche die Umlage der Kosten des Betriebs von Brandschutz- und Brandmeldeanlagen auf den Mieter vorsieht.
Dem stehen Regelungen in den Bauordnungen der Länder (hier: § 48 Abs. 4 Satz 4 BauO Bln), nach denen (öffentlich-rechtlich) die Wartung dem Mieter obliegt, nicht entgegen.

</details>

<details><summary>BGH VIII ZR 117/21, Rn. 50–52</summary>

bb) Eine andere Bewertung, insbesondere eine Zuordnung zu den nicht auf den Mieter umlegbaren Verwaltungskosten im Sinne von § 1 Abs. 2 Nr. 1BetrKV, ist entgegen der Ansicht der Revision nicht deshalb geboten, weil die Beklagte mit der Wartung der Rauchwarnmelder zugleich Vorsorge im eigenen Interesse - zur Erfüllung einer eigenen Verkehrssicherungspflicht als Gebäudeeigentümerin und damit zur Vermeidung einer Inanspruchnahme auf Schadensersatz - betreibt (so aber auch AG Dortmund, WuM 2017, 203, 204; AG Gelsenkirchen, WuM 2022, 158). Denn die Erfüllung von Verkehrssicherungspflichten ist als rein haftungsrechtlicher Gesichtspunkt kein maßgebendes Kriterium zur Abgrenzung zwischen Instandhaltungs- und Betriebskosten; vielmehr können auch Kosten für Maßnahmen, die zudem der Wahrnehmung einer Verkehrssicherungspflicht des Vermieters dienen, als Betriebskosten umlagefähig sein(Senatsurteil vom 10. November 2021 - VIII ZR 107/20, NZM 2022, 175 Rn. 25; vgl. auch Senatsurteil vom 14. Februar 2007 - VIII ZR 123/06, NZM 2007, 282 Rn. 12; Langenberg/Zehelein, Betriebskosten- und Heizkostenrecht, 10. Aufl., Teil A Rn. 256). Das gilt in gleicher Weise für die Abgrenzung zu den in § 1 Abs. 2 Nr. 1 BetrKV genannten Verwaltungskosten (vgl. Senatsurteil vom 18. Dezember 2019 - VIII ZR 62/19, NZM 2020, 457 Rn. 18 ff. [für die Kontrolle und Überwachung durch einen Hauswart]).
b) Die Annahme des Berufungsgerichts, eine Umlagefähigkeit dieser Kosten ergebe sich im Streitfall aufgrund einer ergänzenden Vertragsauslegung, ist zwar rechtsfehlerhaft. Dies wirkt sich jedoch im Ergebnis nicht aus, weil die Parteien die Kosten jedenfalls mit der vertraglichen Vereinbarung in Nr. 1 Buchst. o der Anlage 4 des Mietvertrags wirksam auf die Kläger umgelegt haben.
aa) Das Berufungsgericht hat eine ergänzende Vertragsauslegung vorgenommen, obwohl deren Voraussetzungen vorliegend nicht gegeben sind. Insoweit durfte es nicht offenlassen, ob eine mietvertragliche Regelung - etwa die von ihm angeführte allgemeine Verweisung von Nr. 1 Buchst. o der Anlage 4 des Mietvertrags auf § 2 Nr. 17 BetrKV oder eine vertragliche Neukostenklausel - die Umlage der Wartungskosten für die Rauchwarnmelder auf die Kläger erlaubte.

</details>

---

## q15 (single)

**Question:** The tenants used to heat with their own individual stoves. We switched to a heating contractor who supplies the heat. Can I pass the contractor’s costs on to tenants under § 556c BGB?

**Your reference answer:** No, not under § 556c BGB. When switching from tenant-run stoves to commercial heat supply, it doesn't apply directly because the tenant wasn't paying heating costs as operating costs before the switch (Rn. 39), and not by analogy either (BGH VIII ZR 47/25, Leitsatz, Rn. 37). Whether you can pass the costs on depends on an agreement with the tenant; in this case the BGH found at least a tacit one after the switch and sent the case back (Rn. 29).

**Agent's answer:**

> **No**, you cannot pass the heating contractor’s costs on to the tenants under the statutory conversion rule for commercial heat supply (*Wärmelieferung*).
>
> ### Legal Grounds
>
> According to the Federal Court of Justice (Bundesgerichtshof), the statutory provision governing the conversion to commercial heat contracting applies **neither directly nor by analogy** (*weder unmittelbare noch entsprechende Anwendung*) when switching from tenant-operated individual stoves (*durch den Mieter betriebene Einzelöfen*) to commercial heat delivery by an external supplier (**BGH VIII ZR 47/25, Leitsatz**):
>
> * **No direct application:** Direct application requires a lease under which the tenant is already contractually obligated to pay operating costs for heating or hot water as service charges (*Betriebskosten*). With individual stoves, tenants heated by self-supply (*Selbstversorgung*) and were billed directly by energy providers, rather than paying heating costs under a service charge allocation agreement (*Umlagevereinbarung*) with the landlord (**BGH VIII ZR 47/25, Rn. 36–39**). For the statutory conversion rule to apply, a cost allocation agreement must have already existed at the time of the switch (**BGH VIII ZR 47/25, Rn. 40–42**).
> * **No application by analogy:** An analogy is not permissible because there is no unintended statutory gap (*keine planwidrige Regelungslücke*). The legislature deliberately restricted the statutory conversion mechanism to tenancies where heating costs were already agreed to be borne as service charges (**BGH VIII ZR 47/25, Rn. 46–47**).
>
> ### What This Depends On
>
> The ability to allocate heating contractor costs in this scenario depends entirely on the lease and contractual agreements with your tenants:
>
> * Commercial heat delivery costs (*Wärmelieferungskosten*) include non-fuel overheads (such as maintenance, capital, depreciation, and contractor profit). Without the statutory conversion mechanism, these contractor costs cannot be passed on as service charges unless the lease agreement already explicitly provides for allocating commercial heat supply costs, or the tenant consents to a contractual change (**BGH VIII ZR 47/25, Rn. 45, 48–50**).
> * If the parties reach an agreement (expressly or implicitly) after the switch to allocate heating costs as service charges, the landlord can only recover the specific costs covered by that agreement (**BGH VIII ZR 47/25, Rn. 12, 27–30**, **BGH VIII ZR 47/25, Rn. 54–56**).
>
> For drafting a contractual amendment or assessing existing lease terms, you should consult a tenancy lawyer (*Fachanwalt für Miet- und Wohnungseigentumsrecht*).

**Cited passages:**

<details><summary>BGH VIII ZR 47/25, Leitsatz</summary>

Auf die seitens des Vermieters von Wohnraum vorgenommene Umstellung der Wärmeversorgung von durch den Mieter betriebenen Einzelöfen auf die eigenständig gewerbliche Lieferung der Wärme durch einen Wärmelieferanten findet die Vorschrift des § 556c BGB über die Umlage der Kosten einer solchen Lieferung als Betriebskosten auf die Mieter weder unmittelbare noch entsprechende Anwendung.

</details>

<details><summary>BGH VIII ZR 47/25, Rn. 36–39</summary>

2. In welcher Höhe der Klägerin darüber hinaus ein Anspruch auf Zahlung restlicher Wärmekosten auch für die Jahre 2018 bis 2020 gegen den Beklagten zusteht, kann anhand der von dem Berufungsgericht bislang getroffenen Feststellungen jedoch nicht abschließend beurteilt werden. Jedenfalls aber kann sie Zahlung des Anteils der Kosten der zentralen Wärmeversorgung durch die Wärmelieferantin verlangen, der auch bei einer zentralen Wärmeversorgung durch die Klägerin gemäß § 7 Abs. 2 der Verordnung über die verbrauchsabhängige Abrechnung der Heiz- und Warmwasserkosten vom 5. Oktober 2009 (Verordnung über Heizkostenabrechnung - HeizkostenV; BGBl. I S. 3250; im Folgenden: HeizkostenV) in der hier anzuwendenden, bis zum 30. November 2021 geltenden Fassung (im Folgenden: aF), § 8 Abs. 2 HeizkostenV angefallen wäre.
a) Das Berufungsgericht hat noch zu Recht angenommen, dass die - halbzwingende (§ 556c Abs. 4 BGB) - Vorschrift des § 556c Abs. 1 Satz 1 BGB auf den - hier vorliegenden - Fall einer Umstellung der Selbstversorgung der Mieter mit Wärme und Warmwasser auf eine gewerbliche Lieferung durch einen Wärmelieferanten weder unmittelbar noch entsprechend anwendbar ist.
aa) Nach dieser Bestimmung hat der Mieter, wenn dieser die Betriebskosten für Wärme oder Warmwasser zu tragen hat und der Vermieter die Versorgung von der Eigenversorgung auf die eigenständig gewerbliche Lieferung durch einen Wärmelieferanten (Wärmelieferung) umstellt, die Kosten der Wärmelieferung als Betriebskosten zu tragen, wenn die Wärme mit verbesserter Effizienz aus einer vom Wärmelieferanten errichteten neuen Anlage oder aus einem Wärmenetz geliefert wird (Nr. 1) und die Kosten der Wärmelieferung die Betriebskosten für die bisherige Eigenversorgung mit Wärme oder Warmwasser nicht übersteigen (Nr. 2).
bb) Das Berufungsgericht hat insoweit zunächst rechtsfehlerfrei eine unmittelbare Anwendung dieser Vorschrift auf die hier streitgegenständlichen Mietverhältnisse der Parteien verneint. Denn die unmittelbare Anwendbarkeit des § 556c Abs. 1 Satz 1 BGB setzt voraus, dass es sich um einen zum Zeitpunkt der beabsichtigten Umstellung bereits laufenden Mietvertrag handelt, bei dem die Kosten für Wärme oder Warmwasser (oder von beidem) vom Mieter - nach § 556 BGB - als Betriebskosten zu tragen sind (vgl. BT-Drucks. 17/10485, S. 23; siehe auch BeckOK-Mietrecht/Pfeifer, Stand: 1. März 2026, § 556c BGB Rn. 37, 40). Bis zu der Umstellung auf die Wärmelieferung trug der Beklagte die Wärmekosten jedoch nicht aufgrund einer mit der Klägerin getroffenen Umlagevereinbarung im Sinne von § 556 Abs. 1 BGB, sondern diese Kosten wurden dem Beklagten aufgrund der Selbstversorgung mit Wärme von dem Stromanbieter unmittelbar in Rechnung gestellt.

</details>

<details><summary>BGH VIII ZR 47/25, Rn. 40–42</summary>

Soweit die Revisionserwiderung meint, es habe eine konkludente Vereinbarung der Parteien über die Umlage der Kosten für Wärme und Warmwasser auf den Beklagten gegeben, weil der Beklagte sich in der Klageerwiderung nicht gegen die Abrechnung der Betriebskosten für die Jahre ab 2017 dem Grunde nach gewandt habe, übersieht sie, dass es für die Anwendung der Vorschrift des § 556c BGB maßgeblich auf das Vorliegen einer Umlagevereinbarung im Zeitpunkt der Umstellung auf die Wärmelieferung ankommt.
cc) Die Vorschrift des § 556c Abs. 1 Satz 1 BGB ist entgegen einer in der Literatur vertretenen Ansicht (vgl. Lee, WuM 2025, 385, 392; NZM 2025, 889, 898; eine analoge Anwendung erwägend auch Staudinger/Artz, BGB, Neubearb. 2024, § 556c Rn. 19) auf den - hier vorliegenden - Fall der Umstellung von einer Selbstversorgung der Mieter mit Wärme und Warmwasser durch zur Ausstattung der Wohnung gehörende mitvermietete Einzelheizungen auf eine gewerbliche Wärmelieferung durch einen Wärmelieferanten auch nicht entsprechend anwendbar (so auch Bentrop, WuM 2025, 649, 658; NK-BGB/Hinz, 4. Aufl., § 556c Rn. 15).
(1) Eine Analogie ist nur zulässig, wenn das Gesetz eine planwidrige Regelungslücke enthält und der zu beurteilende Sachverhalt in rechtlicher Hinsicht so weit mit dem Tatbestand, den der Gesetzgeber geregelt hat, vergleichbar ist, dass angenommen werden kann, der Gesetzgeber wäre bei einer Interessenabwägung, bei der er sich von den gleichen Grundsätzen hätte leiten lassen wie bei dem Erlass der herangezogenen Gesetzesvorschrift, zu dem gleichen Abwägungsergebnis gekommen (st. Rspr.; siehe nur Senatsurteile vom 18. Januar 2017 - VIII ZR 278/15, NVwZ-RR 2017, 372 Rn. 32; vom 24. Februar 2021 - VIII ZR 36/20, BGHZ 229, 59 Rn. 38; jeweils mwN; vom 21. Mai 2025 - VIII ZR 201/23, NJW-RR 2025, 1228 Rn. 23).

</details>

<details><summary>BGH VIII ZR 47/25, Rn. 46–47</summary>

(b) Mit Blick auf diese je nach Vertragsgestaltung bestehenden Unsicherheiten, ob und unter welchen Voraussetzungen der Vermieter von der Eigenerzeugung der Heizwärme zum Fremdbezug übergehen und dem Mieter die Kosten der Wärmelieferung als Betriebskosten in Rechnung stellen konnte, wollte der Gesetzgeber durch die Einführung des § 556c BGB klare Rahmenbedingungen für die Umstellung durch den Vermieter im laufenden Mietverhältnis schaffen (vgl. BT-Drucks. 17/10485, S. 14; siehe auch Bentrop, WuM 2025, 649, 658). Dass der Gesetzgeber auch Umstellungen von einer Selbstversorgung durch die Mieter auf eine Wärmelieferung von der Regelung des § 556c BGB erfasst wissen wollte, ist den Gesetzesmaterialien nicht zu entnehmen. Zwar wird in der Gesetzesbegründung ausgeführt, dass diese Regelung für sämtliche Umstellungen in laufenden Mietverhältnissen gelten (vgl. BT-Drucks., aaO S. 2) und hierdurch ein einheitlicher Rechtsrahmen für die Umstellung auf Contracting geschaffen werden sollte (vgl. BT-Drucks., aaO S. 14). Der Gesetzgeber hat jedoch an anderer Stelle ausdrücklich darauf hingewiesen, dass § 556c Abs. 1 BGB klarstelle, dass die Regelung auf Fallgestaltungen anwendbar sein soll, bei denen die Kosten für Wärme oder Warmwasser (oder von beidem) nach § 556 BGB vom Mieter zu tragen sind (vgl. BT-Drucks., aaO S. 23). Dementsprechend hat er auch im Wortlaut dieser Bestimmung (siehe oben unter II 2 a aa) ausdrücklich an eine Betriebskostentragungspflicht des Mieters angeknüpft ("Hat der Mieter die Betriebskosten für Wärme oder Warmwasser zu tragen [...]").
Dem Gesetzgeber war mithin bewusst, dass es auch Fallgestaltungen gibt, bei denen eine Umlage der Wärmekosten als Betriebskosten auf den Mieter von den Mietvertragsparteien nicht vereinbart worden ist. Er ist jedoch bei seinen Erwägungen davon ausgegangen, dass der Mieter in der Praxis regelmäßig die Wärmekosten als Betriebskosten zu tragen hat (vgl. BT-Drucks., aaO), und die geschaffene Regelung somit zwar nicht alle Fälle der Umstellung auf eine Wärmelieferung im laufenden Mietverhältnis, aber den weit überwiegenden Teil erfasst. Eine planwidrige Regelungslücke mit Blick auf die hier in Rede stehende Umstellung von der Selbstversorgung durch die Mieter auf eine Wärmelieferung liegt deshalb nicht vor.

</details>

<details><summary>BGH VIII ZR 47/25, Rn. 12, 27–30</summary>

Die Revision des Beklagten hat teilweise Erfolg.
Diese Beurteilung hält rechtlicher Nachprüfung nicht in jeder Hinsicht stand.
Das Berufungsgericht hat zwar rechtsfehlerfrei angenommen, dass die Klägerin die Zahlung des sich aus der Betriebs- und Heizkostenabrechnung für das Jahr 2017 betreffend die Wohnung Nr. 40020 ergebenden Saldos in Höhe von 704,73 € nebst Zinsen verlangen kann, weil der Beklagte mit Einwendungen gegen diese Abrechnung gemäß § 556 Abs. 3 Satz 6 BGB ausgeschlossen und dieser Zahlungsanspruch auch nicht verjährt ist.
Mit der vom Berufungsgericht gegebenen Begründung kann jedoch ein Anspruch der Klägerin auf Zahlung des sich aus den Betriebs- und Heizkostenabrechnungen für die Jahre 2018 bis 2020 ergebenden Saldos in Höhe von 1.843,70 € nicht bejaht werden. Das Berufungsgericht hat zwar noch zu Recht eine entsprechende Anwendbarkeit der Vorschrift des § 556c BGB verneint. Es hat jedoch im Rahmen der von ihm vorgenommenen ergänzenden Vertragsauslegung bei der Annahme einer hierfür erforderlichen Regelungslücke übersehen, dass die Parteien sich nach der Umstellung der Wärmeversorgung auf eine Wärmelieferung zumindest stillschweigend grundsätzlich auf eine Umlage von Wärmekosten als Betriebskosten geeinigt haben. Ob diese Vereinbarung auch die Umlage der hier noch streitgegenständlichen Wärmekosten erfasst, kann anhand der vom Berufungsgericht bislang getroffenen Feststellungen nicht abschließend beurteilt werden.
1. Das Berufungsgericht hat allerdings noch zu Recht angenommen, dass der Klägerin ein Anspruch auf Zahlung restlicher Wärmekosten in der geltend gemachten Höhe von 704,73 € für das Jahr 2017 gegen den Beklagten zusteht.

</details>

<details><summary>BGH VIII ZR 47/25, Rn. 54–56</summary>

Aufgrund der bislang von dem Berufungsgericht getroffenen Feststellungen kann aber nicht abschließend beurteilt werden, ob der Beklagte angesichts der ihm im Zuge der Umstellung der Wärmeversorgung erteilten Informationen die Aufforderung der Hausverwaltung dahingehend verstehen musste, dass die Klägerin nicht nur den Anteil der Kosten der zentralen Wärmeversorgung durch die Wärmelieferantin, der auch bei einer zentralen Wärmeversorgung durch den Vermieter nach § 7 Abs. 2 HeizkostenV aF, § 8 Abs. 2 HeizkostenV angefallen wäre, sondern die gesamten Kosten nach § 7 Abs. 4, § 8 Abs. 4 HeizkostenV einschließlich der kalkulatorischen Kosten auf den Beklagten umlegen wollte, und ob dieser durch die Aufnahme der monatlichen Vorauszahlungen das darin liegende Angebot zur Änderung der Mietverträge angenommen hat. Insofern bedarf es weiterer Feststellungen seitens des Berufungsgerichts.
Dabei werden die im Zusammenhang mit der Umstellung erfolgten (konkludenten) Willenserklärungen der Parteien auch vor dem Hintergrund zu würdigen sein, dass die Parteien in § 5 Nr. 2 und 9 ihrer beiden Mietverträge die Möglichkeit einer Wärmeversorgung der Wohnungen durch eine zentrale vermieterseitige Eigenversorgung oder durch eine Wärmelieferung zumindest in den Blick genommen haben.
Nach alledem kann das Berufungsurteil in dem aus dem Tenor ersichtlichen Umfang keinen Bestand haben; es ist daher insoweit aufzuheben (§ 562 Abs. 1 ZPO). Die nicht zur Endentscheidung reife Sache ist im Umfang der Aufhebung zur neuen Verhandlung und Entscheidung an das Berufungsgericht zurückzuverweisen (§ 563 Abs. 1 Satz 1 ZPO), damit dieses die erforderlichen Feststellungen - gegebenenfalls nach ergänzendem Vortrag der Parteien und deren Anhörung sowie unter Berücksichtigung der im Zusammenhang mit der Umstellung von den Parteien geführten Korrespondenz - treffen kann.

</details>

---

## q16 (single)

**Question:** We pay the caretaker a flat fee to be on call for emergencies at night and on weekends. Can I bill that to the tenants?

**Your reference answer:** No. A flat fee paid to the caretaker for emergency on-call service is an administrative cost the landlord has to carry (BGH VIII ZR 62/19).

**Agent's answer:**

> **No**, you cannot bill a flat-rate emergency on-call fee (*Notdienstpauschale*) paid to a caretaker to your tenants.
>
> ### Legal Basis and Reasons
>
> * **Administrative Costs, Not Operating Costs:**  
>   The Federal Court of Justice (*Bundesgerichtshof*, BGH) ruled that a flat fee paid to a caretaker for emergency standby is not an allocable operating cost (*Betriebskosten*), but rather administrative costs (*Verwaltungskosten*) that the landlord must bear (**BGH VIII ZR 62/19, Leitsatz**; **BGH VIII ZR 62/19, Rn. 4, 8–12**).
>
> * **Statutory Exclusion:**  
>   Under **§ 1 BetrKV**, operating costs do not include administrative costs (*Verwaltungskosten*), which are defined as the costs of personnel and facilities required to manage the building. In addition, under **§ 2 Nr. 13–17 BetrKV** (specifically Nr. 14), costs of the caretaker (*Kosten für den Hauswart*) may only be billed to the extent they do not involve property management (*Hausverwaltung*), repair, or maintenance.
>
> * **Why On-Call Standby Counts as Property Management:**  
>   Being on call to take tenant reports about defects, casualties, damage, or emergencies and subsequently ordering repair measures are duties of property management (*Grundstücksverwaltung*). Outside business hours, the on-call caretaker merely substitutes for the property management that would handle such calls during regular business hours (**BGH VIII ZR 62/19, Rn. 13–16**). By contrast, billable caretaker tasks are routine, periodic monitoring and control measures to ensure safety and order on common areas (**BGH VIII ZR 62/19, Rn. 17–19**).
>
> * **Distinction from Elevator Emergency Services:**  
>   The court noted that this general emergency on-call service differs from an emergency monitoring system for a passenger elevator. While continuous standby for elevator passenger rescue is legally required by safety regulations and therefore allocable, a general caretaker standby covering all potential property disruptions outside normal business hours cannot be passed on (**BGH VIII ZR 62/19, Rn. 24**).
>
> ### Contractual Prerequisites
> Under German tenancy law, operating costs can only be billed if the parties have agreed in the lease that the tenant bears operating costs (**BGH VIII ZR 62/19, Rn. 4, 8–12**). However, even if the lease agreement (*Mietvertrag*) contains a clause allocating caretaker costs (*Kosten des Hauswarts*), the flat on-call fee cannot be included in the bill, because administrative tasks must be deducted (**BGH VIII ZR 62/19, Rn. 4, 8–12**; **§ 2 Nr. 13–17 BetrKV**).

**Cited passages:**

<details><summary>BGH VIII ZR 62/19, Leitsatz</summary>

Bei einer an den Hausmeister entrichteten Notdienstpauschale handelt es sich nicht um umlagefähige Betriebskosten, sondern um vom Vermieter zu tragende Verwaltungskosten.

</details>

<details><summary>BGH VIII ZR 62/19, Rn. 4, 8–12</summary>

Die Revision hat keinen Erfolg.
Diese Beurteilung hält rechtlicher Nachprüfung stand; die Revision ist daher zurückzuweisen.
Das Berufungsgericht hat zu Recht einen Anspruch der Klägerin auf Zahlung der den Beklagten anteilig berechneten Notdienstpauschale verneint. Bei diesen Kosten handelt es sich, wie das Berufungsgericht richtig gesehen hat, nicht um umlagefähige Betriebskosten, sondern um vom Vermieter zu tragende Verwaltungskosten.
1. Gemäß § 535 Abs. 1 Satz 3, § 556 Abs. 1, 4 BGB hat der Mieter Betriebskosten zu tragen, wenn die Parteien eine entsprechende Vereinbarung wirksam getroffen haben. Grundsätzlich genügt dafür - wie hier im Mietvertrag enthalten - eine Verweisung auf die Anlage 3 zu § 27 Abs. 1 II. Berechnungsverordnung (BV) oder auf die seit dem 1. Januar 2004 geltende Betriebskostenverordnung (Senatsurteil vom 27. Juni 2007 - VIII ZR 202/06, NJW 2007, 3060 Rn. 19).
Betriebskosten sind - wie in Anlage 3 zu § 27 Abs. 1 II. BV und ebenso in § 1 der ab 1. Januar 2004 geltenden Betriebskostenverordnung sowie in § 556 Abs. 1 Satz 2 BGB in der ab 1. Januar 2007 geltenden Fassung definiert - die Kosten, die dem Eigentümer durch das Eigentum an dem Grundstück oder durch den bestimmungsgemäßen Gebrauch des Gebäudes oder der Wirtschaftseinheit, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Von den umlagefähigen Betriebskosten abzugrenzen sind einerseits Kosten der Instandsetzung und Instandhaltung sowie andererseits Verwaltungskosten.
Die (nicht als Betriebskosten umlagefähigen) Aufwendungen für Instandsetzung und Instandhaltung werden durch Reparatur und Wiederbeschaffung verursacht und müssen zur Erhaltung des bestimmungsgemäßen Gebrauchs erbracht werden, um die durch Abnutzung, Alterung, Witterungseinwirkung entstehenden baulichen oder sonstigen Mängel ordnungsgemäß zu beseitigen (§ 28 Abs. 1 II. BV; seit 1. Januar 2004: § 1 Abs. 2 Nr. 2 BetrKV). Instandsetzung und Instandhaltung betreffen deshalb Mängel an der Substanz der Immobilie oder ihrer Teile (Senatsurteile vom 14. Februar 2007 - VIII ZR 123/06, NZM 2007, 282 Rn. 10, 14; vom 7. April 2004 - VIII ZR 167/03, NZM 2004, 417 unter II 1 a). Bei den ebenfalls nicht auf den Mieter umlagefähigen Verwaltungskosten handelt es sich um die Kosten der zur Verwaltung des Gebäudes erforderlichen Arbeitskräfte und Einrichtungen, die Kosten der Aufsicht, den Wert der vom Vermieter persönlich geleisteten Verwaltungsarbeit, die Kosten für die gesetzlichen oder freiwilligen Prüfungen des Jahresabschlusses und die Kosten für die Geschäftsführung (§ 26 Abs. 1 II. BV; seit 1. Januar 2004: § 1 Abs. 2 Nr. 1 BetrKV).

</details>

<details><summary>§ 1 BetrKV</summary>

(1) Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Sach- und Arbeitsleistungen des Eigentümers oder Erbbauberechtigten dürfen mit dem Betrag angesetzt werden, der für eine gleichwertige Leistung eines Dritten, insbesondere eines Unternehmers, angesetzt werden könnte; die Umsatzsteuer des Dritten darf nicht angesetzt werden.
(2) Zu den Betriebskosten gehören nicht:
1. die Kosten der zur Verwaltung des Gebäudes erforderlichen Arbeitskräfte und Einrichtungen, die Kosten der Aufsicht, der Wert der vom Vermieter persönlich geleisteten Verwaltungsarbeit, die Kosten für die gesetzlichen oder freiwilligen Prüfungen des Jahresabschlusses und die Kosten für die Geschäftsführung (Verwaltungskosten),
2. die Kosten, die während der Nutzungsdauer zur Erhaltung des bestimmungsmäßigen Gebrauchs aufgewendet werden müssen, um die durch Abnutzung, Alterung und Witterungseinwirkung entstehenden baulichen oder sonstigen Mängel ordnungsgemäß zu beseitigen (Instandhaltungs- und Instandsetzungskosten).

</details>

<details><summary>§ 2 Nr. 13–17 BetrKV</summary>

hierzu gehören namentlich die Kosten der Versicherung des Gebäudes gegen Feuer-, Sturm-, Wasser- sowie sonstige Elementarschäden, der Glasversicherung, der Haftpflichtversicherung für das Gebäude, den Öltank und den Aufzug;
14. die Kosten für den Hauswart,
hierzu gehören die Vergütung, die Sozialbeiträge und alle geldwerten Leistungen, die der Eigentümer oder Erbbauberechtigte dem Hauswart für seine Arbeit gewährt, soweit diese nicht die Instandhaltung, Instandsetzung, Erneuerung, Schönheitsreparaturen oder die Hausverwaltung betrifft; soweit Arbeiten vom Hauswart ausgeführt werden, dürfen Kosten für Arbeitsleistungen nach den Nummern 2 bis 10 und 16 nicht angesetzt werden;
15. die Kosten
a) des Betriebs der Gemeinschafts-Antennenanlage,
hierzu gehören die Kosten des Betriebsstroms und die Kosten der regelmäßigen Prüfung ihrer Betriebsbereitschaft einschließlich ihrer Einstellung durch eine Fachkraft,
bis zum 30. Juni 2024 außerdem das Nutzungsentgelt für eine nicht zu dem Gebäude gehörende Antennenanlage sowie die Gebühren, die nach dem Urheberrechtsgesetz für die Kabelweitersendung entstehen,
oder
b) des Betriebs der mit einem Breitbandnetz verbundenen privaten Verteilanlage,
hierzu gehören die Kosten des Betriebsstroms,
bis zum 30. Juni 2024 außerdem die weiteren Kosten entsprechend Buchstabe a, sowie die laufenden monatlichen Grundgebühren für Breitbandanschlüsse,
oder
c) des Betriebs einer gebäudeinternen Verteilanlage, die vollständig mittels Glasfaser mit einem öffentlichen Netz mit sehr hoher Kapazität im Sinne des § 3 Nummer 33 des Telekommunikationsgesetzes verbunden ist, wenn der Mieter seinen Anbieter von öffentlich zugänglichen Telekommunikationsdiensten über seinen Anschluss frei wählen kann,
hierzu gehören die Kosten des Betriebsstroms sowie ein Bereitstellungsentgelt gemäß § 72 Absatz 1 des Telekommunikationsgesetzes;
16. die Kosten des Betriebs der Einrichtungen für die Wäschepflege,
hierzu gehören die Kosten des Betriebsstroms, die Kosten der Überwachung, Pflege und Reinigung der Einrichtungen, der regelmäßigen Prüfung ihrer Betriebsbereitschaft und Betriebssicherheit sowie die Kosten der Wasserversorgung entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind;
17. sonstige Betriebskosten,
hierzu gehören Betriebskosten im Sinne des § 1, die von den Nummern 1 bis 16 nicht erfasst sind.
Für Anlagen, die ab dem 1. Dezember 2021 errichtet worden sind, ist Satz 1 Nummer 15 Buchstabe a und b nicht anzuwenden.

</details>

<details><summary>BGH VIII ZR 62/19, Rn. 13–16</summary>

2. Ausgehend von der danach zu treffenden Unterscheidung zwischen Betriebskosten und Verwaltungskosten kommt es darauf an, ob die Notdienstpauschale unter die im Streitfall allein in Betracht kommende Betriebskostenposition "Kosten des Hauswarts" (Nr. 14 der Anlage 3 zu § 27 Abs. 1 II. BV) fällt oder ob sie den vom Vermieter selbst zu tragenden Verwaltungskosten zuzuordnen ist.
a) In der Rechtsprechung der Instanzgerichte wird überwiegend die Auffassung vertreten, es handele sich dabei um umlagefähige Betriebskosten. Das wird zum Teil damit begründet, dass die Stellung einer Notdienstbereitschaft im Interesse des Mieters liege, weil sie in erster Linie - insbesondere in großen Wohnanlagen - dazu diene, die vom Mieter eingebrachten Sachen vor Schäden durch beispielsweise Strom- oder Heizungsausfall oder bei einem Wasserrohrbruch zu bewahren (LG Köln, WuM 1997, 230, 231). Zum Teil wird die Umlagefähigkeit einer Notdienstpauschale deswegen angenommen, weil die Erreichbarkeit des Hausmeisters zur Störungsbeseitigung in Notfällen auch außerhalb der (üblichen) Geschäftszeiten zu den dem Sicherheitsbereich angehörenden Tätigkeiten eines Hausmeisters gehöre, deren Kosten grundsätzlich umlagefähig seien (AG Hohenschönhausen, Urteil vom 31. März 2008 - 16 C 205/07, juris Rn. 12 f.; AG Brandenburg, Urteil vom 7. Juni 2010 - 31 C 210/09, juris Rn. 20). Andere Instanzgerichte bejahen die Umlagefähigkeit von Bereitschaftskosten ohne nähere Begründung (LG Leipzig, Urteil vom 9. März 2017 - 1 S 330/16, juris Rn. 21; LG Berlin, Urteil vom 4. Dezember 2006 - 67 S 223/06, juris Rn. 27; ebenso in der Literatur Langenberg/Zehelein, Betriebskosten- und Heizkostenrecht, 9. Aufl., A. Rn. 201; Erman/Lützenkirchen, BGB, 15. Aufl., § 556 Rn. 90; BeckOGK-BGB/Drager, Stand 1. Oktober 2019, § 2 BetrKV Rn. 92; Schneider in Spielbauer/Schneider, Mietrecht, 2. Aufl., § 556 BGB Rn. 262).
b) Nach anderer Ansicht, der sich auch das Berufungsgericht angeschlossen hat, handelt es sich bei den Kosten für eine Notdienstbereitschaft um Verwaltungskosten. Zur Begründung wird angeführt, die Bereithaltung für die Entgegennahme von Mängel-, Havarie-, Schadens- und Notfallmeldungen und die darauffolgende Veranlassung von Reparaturmaßnahmen seien Tätigkeiten im Zusammenhang mit der Grundstücksverwaltung, was sich nicht zuletzt daran zeige, dass solche Meldungen während der normalen Geschäftszeiten üblicherweise an die Hausverwaltung gerichtet würden (AG Charlottenburg, NZM 2018, 747, 748; ebenso BeckOK-MietR/Pfeifer, Stand 1. September 2019, § 556 BGB Rn. 957a; Wall, Betriebs- und Heizkosten, 4. Aufl., Rn. 4428).
c) Die zuletzt genannte Ansicht verdient den Vorzug.

</details>

<details><summary>BGH VIII ZR 62/19, Rn. 17–19</summary>

aa) Zu den umlagefähigen Kosten für den Hauswart gehören die Vergütung, die Sozialbeiträge sowie alle geldwerten Leistungen, die der Eigentümer dem Hauswart für seine Arbeit gewährt, soweit diese nicht die Instandhaltung, Instandsetzung, Erneuerung, Schönheitsreparaturen oder die Hausverwaltung betrifft (Nr. 14 der Anlage 3 zu § 27 Abs. 1 II. BV).
Als umlagefähige Kosten des Hauswarts kommen dabei zum einen Aufwendungen für bestimmte Wartungs-, Reinigungs- und Pflegetätigkeiten in Betracht (vgl. Nr. 14 Satz 2 der Anlage 3 zu § 27 Abs. 1 II. BV; ab 1. Januar 2004: § 2 Nr. 14 Halbs. 2 BetrKV). Zum anderen sind diejenigen Kosten als Betriebskosten anzusehen, die durch die (typische) Aufgabe eines Hauswarts verursacht werden, in den allgemein zugänglichen Räumen und auf den allgemein zugänglichen Flächen des Mietobjekts für Sicherheit und Ordnung zu sorgen. Diese Aufgaben sind dadurch gekennzeichnet, dass es sich um jeweils ohne konkreten Anlass ("routinemäßig") in bestimmten zeitlichen Intervallen im Sicherheitsinteresse durchzuführende Maßnahmen der Kontrolle und Überwachung handelt.
Hierzu gehört etwa die Überwachung, dass Rettungs- oder Fluchtwege nicht zugestellt sind, keine gefährlichen Gegenstände auf den Gemeinschaftsflächen des Hauses gelagert werden, Außentüren ordnungsgemäß schließen und bei Fehlen einer Türöffneranlage nachts verschlossen sind, Abflüsse im Keller oder auf dem Grundstück freiliegen, die Beleuchtung von Gemeinschaftsflächen ordnungsgemäß funktioniert, haustechnische Anlagen in ordnungsgemäßem Zustand sind, Glasbereiche keine Schäden aufweisen, Handwerker im Rahmen umlagefähiger Wartungs-, Reinigungs- oder Gartenpflegearbeiten eingewiesen werden und der allgemeinen Verkehrssicherungspflicht des Vermieters (Frostschutz, Brandschutz, gefahrloser Zustand von Wohnflächen im Innen- und Außenbereich) genügt ist. Im Ordnungsbereich zählt zu den Aufgaben eines Hauswarts im Wesentlichen die Einhaltung der Hausordnung (Überwachung der Treppenhausreinigung, des Winterdienstes, Einhaltung der Ruhezeiten etc.; vgl. im Einzelnen etwa die Darstellung bei Langenberg/Zehelein, aaO, A. Rn. 201 f. mwN; Wall, aaO Rn. 4416 mwN).

</details>

<details><summary>BGH VIII ZR 62/19, Rn. 24</summary>

Dabei nimmt die Einrichtung einer Notrufbereitschaft für einen Personenaufzug insofern eine Sonderstellung ein, als Nr. 7 der Anlage 3 zu § 27 Abs. 1 II. BV (ab 1. Januar 2004: § 2 Nr. 7 BetrKV) unter anderem die Beaufsichtigung und Überwachung der Anlage aufführt und für Aufzugsanlagen, die zu gewerblichen oder wirtschaftlichen Zwecken Personen befördern, die Vorschriften der Betriebssicherheitsverordnung gelten (§ 2 Abs. 3 Satz 2 Nr. 1 BetrSichV), wonach der Betreiber einer Aufzugsanlage sicherstellen muss, dass auf Notrufe aus einem Fahrkorb in angemessener Zeit reagiert wird und Befreiungsmaßnahmen sachgerecht durchgeführt werden (Anhang 1 Nr. 4.1 BetrSichV). Da dieses Ziel nur durch eine ständig besetzte Notrufbereitschaft zu erreichen ist, wird die Umlagefähigkeit der entsprechenden Kosten bejaht (vgl. BR-Drucks. 568/03, S. 31; Langenberg/Zehelein, aaO, A. Rn. 93; Wall, aaO Rn. 3707). Diese besonderen Voraussetzungen liegen in Bezug auf die Entrichtung einer Notdienstpauschale an den Hausmeister, die eine "allgemeine" Notdienstbereitschaft für alle denkbaren Störungsfälle im Mietobjekt außerhalb üblicher Geschäftszeiten abdeckt, ersichtlich nicht vor.

</details>

---

## q17 (single)

**Question:** Our building has shops on the ground floor and flats above. Do I have to deduct a share for the shops before splitting the property tax among the tenants?

**Your reference answer:** No. For property tax in a mixed-use building, you don't need to deduct a share for the commercial units first (BGH VIII ZR 79/16).

**Agent's answer:**

> **No**, as a general rule, you do not have to deduct a share for the shops before allocating the property tax (*Grundsteuer*) among the residential tenants.
>
> ### Legal Basis
> * **No commercial deduction required:** When preparing a service charge statement (*Betriebskostenabrechnung*) for a property used partly for commercial and partly for residential purposes, no prior deduction (*Vorwegabzug*) for the commercial units is required regarding the allocation of property tax (**BGH VIII ZR 79/16, Leitsatz**, decided 2017-05-10).
> * **Nature of property tax:** Property tax is a non-yield-related object tax (*ertragsunabhängige Objektsteuer*). It does not depend on the actual income generated in a billing year or on tenant conduct, but rather on uniform municipal and tax office determinations (*Einheitswert*, *Grundsteuermessbetrag*, and *Hebesatz*) (**BGH VIII ZR 79/16, Rn. 20–22**). Therefore, it cannot be established that the commercial use causes substantial additional costs per square meter (*erhebliche Mehrkosten pro Quadratmeter*) (**BGH VIII ZR 79/16, Rn. 20–22**, **BGH VIII ZR 79/16, Rn. 23–25**).
> * **Statutory and equitable principles:** A deduction in advance on equity grounds is only required if the commercial use causes substantial additional costs per square meter, which the tenant bears the burden of presenting and proving (**BGH VIII ZR 79/16, Rn. 20–22**). Furthermore, statutory rules concerning cost allocation based on recorded causation or consumption do not mandate a commercial deduction for property tax, because property tax is based on a uniform assessment by the municipality rather than tenant conduct (**BGH VIII ZR 79/16, Rn. 8, 14–19**).
>
> ---
>
> ### What your answer depends on
> * **Cost allocation agreement (*Umlagevereinbarung*):** Under **§ 556 BGB**, passing on operating costs requires an agreement between the contracting parties in the lease.
> * **Lease terms regarding commercial deduction:** The rule dispensing with a commercial deduction applies unless the parties explicitly agreed on a separate calculation. A clause that merely allocates costs according to the ratio of living and usable space (*Wohn- und Nutzfläche*) distributes the costs across all units by area and does not establish an obligation to make a prior deduction for commercial units (**BGH VIII ZR 79/16, Rn. 8, 14–19**).

**Cited passages:**

<details><summary>BGH VIII ZR 79/16, Leitsatz</summary>

Bei der Betriebskostenabrechnung für ein teils gewerblich und teils zu Wohnzwecken genutztes Grundstück bedarf es bezüglich der Umlage der Grundsteuer keines Vorwegabzugs für die gewerblich genutzten Einheiten.

</details>

<details><summary>BGH VIII ZR 79/16, Rn. 20–22</summary>

a) Nach der gefestigten Rechtsprechung des Senats ist ein Vorwegabzug aus Billigkeitsgründen gemäß §§ 315, 316 BGB (hierzu Senatsurteile vom 8. März 2006 - VIII ZR 78/05, aaO Rn. 16; vom 25. Oktober 2006 - VIII ZR 251/05, aaO) (nur) dann erforderlich, wenn - wofür der Mieter die Darlegungs- und Beweislast trägt - durch die gewerbliche Nutzung erhebliche Mehrkosten (pro Quadratmeter) entstehen (Senatsurteile vom 11. August 2010 - VIII ZR 45/10, NJW 2010, 3363 Rn. 22; vom 13. Oktober 2010 - VIII ZR 46/10, NZM 2011, 118 Rn. 21 f.; vom 8. März 2006 - VIII ZR 78/05, aaO Rn. 31 und Ls 1; vom 25. Oktober 2006 - VIII ZR 251/05, aaO Rn. 15 f.).
b) Gemessen an diesem Maßstab hat das Berufungsgericht die Notwendigkeit eines Vorwegabzugs bei der Grundsteuer rechtsfehlerfrei verneint.
Wie bereits das Amtsgericht zutreffend ausgeführt hat, handelt es sich bei der Grundsteuer um eine ertragsunabhängige Objektsteuer, das heißt, die in einem Abrechnungsjahr erhobene Steuer hängt grundsätzlich nicht von den in diesem Jahr erzielten Erträgen und ihrer Verteilung auf die Nutzung zu gewerblichen Zwecken einerseits und zu Wohnzwecken andererseits ab. Vielmehr wird die Grundsteuer auf der Basis der vom örtlichen Finanzamt erlassenen Bescheide über den Einheitswert (hier: 110.600 DM bzw. 56.548 €) und den Grundsteuermessbetrag (hier: 565,48 €, errechnet im Wege der Multiplikation des Einheitswertes mit der Steuermesszahl 10 vom Tausend) sowie des von der Gemeinde durch Satzungsbeschluss festgelegten Hebesatzes (in Berlin Multiplikator 8,1 [810 %]) ermittelt.

</details>

<details><summary>BGH VIII ZR 79/16, Rn. 23–25</summary>

Zwar findet bei der Festsetzung des Einheitswertes für ein - wie hier - Grundstück mit einem gemischt genutzten Gebäude das Ertragswertverfahren Anwendung (vgl. §§ 36 ff. BewG). Wie das Berufungsgericht richtig gesehen hat, wird dabei ein in der Vergangenheit festgesetzter Einheitswert (wie hier der Bescheid vom 1. Januar 1996) anlässlich eines Eigentümerwechsels in der Regel nicht aktualisiert, sondern wirkt auch gegenüber dem Rechtsnachfolger (vgl. § 182 Abs. 2 AO). Zudem erfolgt die Festsetzung des Einheitswertes regelmäßig bezogen auf die Wertverhältnisse zu einem weit zurückliegenden Zeitpunkt - hier auf den 1. Januar 1935. Auch die Revision stellt nicht in Abrede, dass es bei der derzeitigen gesetzlichen Regelung und behördlichen Praxis der Grundsteuererhebung keinen direkten Zusammenhang zwischen der im Abrechnungsjahr anfallenden Grundsteuer und der konkreten Nutzungsaufteilung sowie der konkreten Ertragssituation in diesem Zeitraum gibt. Damit fehlt es aber an der maßgeblichen Voraussetzung eines Vorwegabzugs, dass die gewerbliche Nutzung erhebliche Mehrkosten verursacht, die es unbillig erscheinen lassen, die Kosten (ohne Vorwegabzug) einheitlich nach dem Flächenmaßstab zu verteilen.
Entgegen einer in der Literatur vertretenen Auffassung (Staudinger/Weitemeyer, Neub. 2014, § 556a BGB Rn. 34 ff. [Rn. 34a: die Aufteilung der Grundsteuer müsse "aus dem Grundsteuermessbescheid herausgerechnet" werden]; Schmidt-Futterer/Langenberg, Mietrecht, 12. Aufl., § 556a BGB Rn. 84 bis 89; Langenberg/Zehelein, Betriebskosten und Heizkostenrecht, 8. Aufl., F V Rn. 173, F VI Rn. 202 f.; Wall, Betriebskostenrecht, 4. Aufl., Rn. 3106) ist daher bei der Grundsteuer kein Vorwegabzug "aus Gerechtigkeitsgründen" vorzunehmen. Die Vertreter dieser Auffassung berücksichtigen zum einen den Ausnahmecharakter, der einem Vorwegabzug nach der Rechtsprechung des Senats zukommt, nicht in der gebotenen Weise. Zum anderen wird meist nicht ausreichend erfasst, dass bei dem gegenwärtigen System der Grundsteuererhebung - wie oben ausgeführt - gerade nicht festgestellt werden kann, dass die gewerbliche Nutzung im jeweiligen Abrechnungsjahr deutlich höhere Kosten je Quadratmeter verursacht. Soweit überhaupt erkannt wird, dass es bei der Festsetzung der Grundsteuer für das jeweilige aktuelle Abrechnungsjahr nicht darauf ankommt, ob die Nutzung der Gewerbeflächen und das Verhältnis der Erträge im Abrechnungszeitraum den im Einheitswertbescheid zugrunde gelegten Verhältnissen entspricht (vgl. Langenberg/Zehelein, aaO), wird daraus nicht die nach der Senatsrechtsprechung zum Vorwegabzug notwendige Rechtsfolge gezogen.
Wenn die Revision fordert, der Vermieter müsse für jedes Abrechnungsjahr ermitteln, welche Erträge auf die gewerbliche und auf die Wohnnutzung entfielen, und sodann einen Vorwegabzug in Höhe des Anteils der gewerblichen Nutzung am Gesamtertrag im Abrechnungsjahr vornehmen, verkennt sie, dass dies schon deshalb nicht zu einer von den Klägern eingeforderten "gerechteren" Kostenverteilung führen kann, weil die Höhe der im Abrechnungsjahr jeweils umzulegenden Grundsteuer von diesen Umständen gerade nicht abhängt.

</details>

<details><summary>BGH VIII ZR 79/16, Rn. 8, 14–19</summary>

Die Revision hat keinen Erfolg.
Diese Beurteilung hält rechtlicher Nachprüfung stand, so dass die Revision zurückzuweisen ist.
Zu Recht hat das Berufungsgericht einen Anspruch der Kläger gemäß § 812 Abs. 1 Satz 1 Alt. 1 BGB auf Auszahlung eines Betriebskostenguthabens in Höhe eines anteiligen Grundsteuerbetrags von 209,31 € verneint. Die von der Beklagten vorgenommene Umlage der Grundsteuer in der Betriebskostenabrechnung für das Jahr 2013 ist aus Rechtsgründen nicht zu beanstanden; insbesondere bedurfte es keines Vorwegabzugs für die gewerblich genutzten Einheiten.
1. Entgegen der Auffassung der Revision enthält der Mietvertrag keine Vereinbarung über eine getrennte Abrechnung der auf die gewerblichen Einheiten entfallenden Betriebskosten (sogenannter Vorwegabzug). Mit der Umlage der Betriebskosten "nach dem Verhältnis der Wohn- und Nutzflächen des Hauses" (§ 3 Nr. 4 des Formular-Mietvertrags) wird lediglich geregelt, dass die Betriebskosten - insgesamt - nach dem Flächenmaßstab zu verteilen sind. Die Frage eines Vorwegabzugs wird in der Klausel nicht einmal erwähnt.
Ohne Erfolg macht die Revision in diesem Zusammenhang geltend, die Mietvertragsparteien hätten - wie die Abrechnungspraxis der ursprünglichen Vermieterin zeige - die genannte Klausel übereinstimmend dahin verstanden, dass der Vermieter einen Vorwegabzug für die gewerblich genutzten Einheiten vornehmen müsse. Unabhängig davon, ob es sich dabei um neuen, in der Revisionsinstanz unbeachtlichen Tatsachenvortrag handelt, lässt die bloße Abrechnungsweise der Rechtsvorgängerin einen derartigen Schluss nicht zu.
2. Auch aus § 556a Abs. 1 Satz 2 BGB lässt sich, wie das Berufungsgericht richtig gesehen hat, nichts für eine Notwendigkeit des von den Klägern geforderten Vorwegabzugs bei der Grundsteuer herleiten. Nach dieser Vorschrift sind Betriebskosten, die von einem erfassten Verbrauch oder von einer erfassten Verursachung durch die Mieter abhängen, nach einem Maßstab umzulegen, der dem unterschiedlichen Verbrauch oder der unterschiedlichen Verursachung Rechnung trägt. Eine erfasste unterschiedliche Verursachung im Sinne dieser Vorschrift scheidet jedoch von vornherein aus, weil die Grundsteuer auf einer einheitlichen Festsetzung durch die Gemeinde beruht und nicht von einem Verhalten der Mieter abhängt. Zudem ergibt sich aus dieser Vorschrift - wie der Senat schon entschieden hat - keine Verpflichtung zu einem Vorwegabzug der auf die gewerblichen Mieter entfallenden Betriebskosten (Senatsurteile vom 8. März 2006 - VIII ZR 78/05, NJW 2006, 1419 Rn. 30; vom 25. Oktober 2006 - VIII ZR 251/05, NJW 2007, 211 Rn. 16).
3. Auch aus Billigkeitsgründen ist der Vermieter nicht zu einem Vorwegabzug für die Gewerbeeinheiten bei der Grundsteuer verpflichtet.

</details>

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

---

## q18 (single)

**Question:** Before I enter the total costs in the statement, I remove the parts that can’t be passed on. Do I have to show the tenant how I calculated those totals?

**Your reference answer:** No. It's enough to state the total for each cost type that you actually split among the tenants, even if you already removed non-billable parts. You don't have to show those calculation steps (BGH VIII ZR 93/15).

**Agent's answer:**

> **No**, you do not have to show or explain the calculation steps or the deductions in the statement for it to be formally valid.
>
> ### Legal Rules and Precedent
>
> According to the Federal Court of Justice (*Bundesgerichtshof*):
>
> 1. **Stating the net total is sufficient:**  
>    For a service charge statement to be formally orderly (*formell ordnungsgemäß*), it is sufficient regarding the specification of the total costs (*Gesamtkosten*) that the landlord states the total amount allocated to the residential tenants of the billing unit under the respective category of operating costs (*BGH VIII ZR 93/15, Leitsatz*).
>
> 2. **No obligation to explain calculation steps:**  
>    This also applies when the landlord has previously deducted cost shares that cannot be passed on to the tenant (*nicht auf den Mieter umlagefähige Kostenanteile*). Stating and explaining the calculation steps that lead to the entered total amount is not required (*BGH VIII ZR 93/15, Leitsatz*; *BGH VIII ZR 93/15, Rn. 19–21*). 
>
> 3. **Formal validity versus substantive correctness:**  
>    Whether the landlord correctly calculated the total or improperly included non-apportionable items is exclusively a question of substantive correctness (*materielle Richtigkeit*). The tenant cannot verify this from the statement alone, but by inspecting the underlying vouchers and receipts (*Belegeinsicht*) (*BGH VIII ZR 93/15, Rn. 19–21*).
>
> ---
>
> ### Facts the Answer Depends On
>
> * **Apportionment agreement (*Umlagevereinbarung*):** Service charges can only be passed on to the tenant if the parties have agreed in the lease that the tenant bears operating costs (*§ 556 BGB*).
> * **Voucher inspection (*Belegeinsicht*):** Although you do not have to break down the calculation in the statement itself, you must retain the underlying invoices and calculation records, because the landlord must grant the tenant inspection of the receipts supporting the statement upon request (*§ 556 BGB*).

**Cited passages:**

<details><summary>BGH VIII ZR 93/15, Leitsatz</summary>

1. Zur formellen Ordnungsgemäßheit einer Betriebskostenabrechnung genügt es hinsichtlich der Angabe der "Gesamtkosten", wenn der Vermieter bei der jeweiligen Betriebskostenart den Gesamtbetrag angibt, den er auf die Wohnungsmieter der gewählten Abrechnungseinheit umlegt.
2. Dies gilt auch dann, wenn der Vermieter diesen Gesamtbetrag vorab um nicht auf den Mieter umlagefähige Kostenanteile bereinigt hat; einer Angabe und Erläuterung der zum angesetzten Gesamtbetrag führenden Rechenschritte bedarf es nicht (Aufgabe der Senatsrechtsprechung; vgl. Senatsurteile vom 14. Februar 2007, VIII ZR 1/06, NJW 2007, 1059 Rn. 10; und vom 9. Oktober 2013, VIII ZR 22/13, WuM 2013, 734 Rn. 14 ff. mwN).

</details>

<details><summary>BGH VIII ZR 93/15, Rn. 19–21</summary>

c) Vor dem Hintergrund der beschriebenen Interessenlage von Mieter und Vermieter und der dargestellten Entwicklung der Senatsrechtsprechung, hält der Senat die Auffassung, bei sogenannten "bereinigten" Kosten bedürfe es für die formelle Ordnungsgemäßheit einer Nebenkostenabrechnung zusätzlicher Angaben zu den Betriebskosten der gesamten Wohnanlage oder zu den Gesamtkosten einschließlich nicht umlagefähiger Kostenanteile und der Erläuterung insoweit angewendeter Rechenschritte, nicht mehr aufrecht. Vielmehr genügt es auch in diesen Fällen, wenn der Vermieter in der Abrechnung bei der jeweiligen Betriebskostenart - beziehungsweise, soweit eine Zusammenfassung mehrerer Betriebskostenarten zulässig ist (vgl. etwa Senatsurteil vom 15. Juli 2009 - VIII ZR 340/08, NZM 2009, 698 Rn. 18), bei dieser zusammengefassten Position - den Gesamtbetrag angibt, den er auf die Wohnungsmieter der gewählten Abrechnungseinheit umlegt. Ob der Vermieter diesen Gesamtbetrag zutreffend errechnet beziehungsweise ermittelt hat oder dabei Kostenanteile mit angesetzt hat, die nicht umlagefähig sind, ist ausschließlich eine Frage der materiellen Richtigkeit, deren Überprüfung der Mieter ohnehin nicht allein anhand der Abrechnung vornehmen kann, sondern nur mittels einer Einsicht in die Belege. Entsprechendes gilt für einen Vorwegabzug für die gewerbliche Nutzung einzelner Einheiten.
Nach alledem kann das Urteil des Berufungsgerichts keinen Bestand haben; es ist daher aufzuheben (§ 562 Abs. 1 ZPO).
Die Sache ist nicht zur Endentscheidung reif, weil das Berufungsgericht - vor dem Hintergrund seiner Rechtsauffassung folgerichtig - keine Feststellungen zur materiellen Richtigkeit der Abrechnung und zur hilfsweise erklärten Aufrechnung der Beklagten getroffen hat. Die Sache ist daher zur neuen Verhandlung und Entscheidung an das Berufungsgericht zurückzuverweisen (§ 563 Abs. 1 Satz 1 ZPO).
Dr. Milger Dr. Schneider Dr. Fetzer

</details>

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

---

## q19 (single)

**Question:** Half the building is empty because it’s going to be demolished, and the remaining tenants’ hot water costs have gone up a lot. Can I stop billing hot water by consumption?

**Your reference answer:** No. Even with high vacancy, hot water still has to be billed partly by consumption. But the landlord may in individual cases have to agree to the tenant's request to lower the consumption share to the legal minimum of 50% (Rn. 24), and in individual cases the claim can be capped under § 242 BGB, taking into account that the landlord also carries vacancy costs (BGH VIII ZR 9/14).

**Agent's answer:**

> **No, you cannot simply stop billing hot water according to consumption.**
>
> Under German law, even high vacancy rates (*Wohnungsleerstände*) caused by a planned building demolition do not entitle you to unilaterally abandon consumption-based billing.
>
> According to the Federal Court of Justice (*Bundesgerichtshof – BGH*) and the Heating Costs Ordinance (*Heizkostenverordnung*):
>
> ### 1. Mandatory consumption-based billing remains in effect
> Even with high vacancy rates in connection with a planned demolition, the proportional allocation of hot water costs based on consumption fundamentally remains mandatory (**BGH VIII ZR 9/14, Leitsatz**, decision date 2014-12-10). 
>
> The Federal Court of Justice clarified that the statutory objective of making tenants aware of individual consumption to incentivize energy savings remains valid, even if the calculation leads to results perceived as unfair in an individual case (**BGH VIII ZR 9/14, Rn. 20–23**). An analogous application of rules that bypass consumption measurements does not apply when metering equipment is installed and functioning (**BGH VIII ZR 9/14, Rn. 20–23**).
>
> ### 2. Legal mechanisms for handling vacancy-related cost shifts
> Instead of abandoning consumption-based billing, the case law and statutory rules outline the following options:
>
> * **Lowering the consumption share to the statutory minimum:** In individual cases, the landlord may be obligated to agree to a contract amendment requested by the tenant to reduce the consumption-based portion of hot water costs to the statutory minimum of 50% of the total costs, in order to distribute fixed costs appropriately during periods of high vacancy (**BGH VIII ZR 9/14, Leitsatz**).
> * **Limitation of the claim under good faith (*Treu und Glauben*):** In individual cases, vacancy-related cost burdens on remaining tenants can lead to a reduction of the landlord’s claim based on the principle of good faith. However, this evaluation balances both sides' interests and takes into account that the landlord also suffers substantial disadvantages from vacancies by bearing the non-consumption-based floor area portion of the costs without receiving rent (**BGH VIII ZR 9/14, Leitsatz** and **BGH VIII ZR 9/14, Rn. 29–31**).
> * **Official exemption (*Ausnahme*):** Under **§ 11 HeizkostenV** (specifically **§ 11 Abs. 1 Nr. 5** in conjunction with **§ 11 Abs. 2 HeizkostenV**), an exemption from the duty to bill hot water based on consumption applies only if the competent authority under state law (*nach Landesrecht zuständige Stelle*) has granted an exemption for that specific case due to special circumstances to avoid unreasonable expense or undue hardship (*unbillige Härte*).

**Cited passages:**

<details><summary>BGH VIII ZR 9/14, Leitsatz</summary>

1. Auch bei hohen Wohnungsleerständen (hier: im Hinblick auf einen im Rahmen der Stadtplanung vorgesehenen Abriss eines 28-Familienhauses) hat es grundsätzlich bei der in § 9 Abs. 4, § 8 Abs. 1 HeizkostenVO vorgeschriebenen anteiligen Umlage von Warmwasserkosten nach Verbrauch zu bleiben.
2. Im Einzelfall kann der Vermieter nach § 241 Abs. 2 BGB verpflichtet sein, dem Verlangen des Mieters auf eine Vertragsänderung dahin gehend zuzustimmen, den nach Verbrauch zu berechnenden Teil der Warmwasserkosten auf das gesetzliche Mindestmaß von 50 % der Gesamtkosten abzusenken, um die Fixkosten bei hohen Leerständen angemessen zu verteilen.
3. Leerstandsbedingten Kostenverschiebungen zu Lasten des Mieters kann darüber hinaus im Einzelfall mit einer aus dem Prinzip von Treu und Glauben (§ 242 BGB) abzuleitenden Anspruchsbegrenzung Rechnung getragen werden. Dabei ist zu berücksichtigen, dass auch der Vermieter durch den Leerstand beträchtliche Nachteile erleidet, weil er - ohne entsprechende Mieteinnahmen zu erhalten - bereits über den von ihm zu tragenden Wohnflächenanteil ebenfalls nicht unbeträchtliche Kosten zu tragen hat.

</details>

<details><summary>BGH VIII ZR 9/14, Rn. 20–23</summary>

3. Diese Auffassung teilt der Senat nicht.
a) Auch wenn - wie der Streitfall zeigt - die allein auf den Vorschriften der Heizkostenverordnung beruhende verbrauchsbezogene Abrechnung im Einzelfall zu als unangemessen empfundenen Ergebnissen führen kann, wird dadurch der über die Einzelfallgerechtigkeit hinausreichende Zweck der Heizkostenverordnung, dem jeweiligen Nutzer den Zusammenhang zwischen dem individuellen Verbrauch und den daraus resultierenden Kosten bewusst zu machen und dadurch Energiespareffekte zu erzielen, nicht in Frage gestellt. Denn die Frage der Sinnhaftigkeit der Vorschriften der Heizkostenverordnung einerseits und die Frage, ob die von der Heizkostenverordnung vorgeschriebene verbrauchsbezogene Abrechnung im Einzelfall zu als billig und gerecht empfundenen Ergebnissen führt andererseits, liegen auf verschiedenen Beurteilungsebenen.
Es muss daher auch bei hohen Leerständen grundsätzlich bei der von der Heizkostenverordnung vorgegebenen verbrauchsabhängigen Abrechnung verbleiben. Insbesondere eine vom Berufungsgericht befürwortete (ähnlich auch Wall in Eisenschmid/Wall, aaO, Rn. 3030; ders., WuM 2007, 415, 418 [differenzierend und eine Lösung de lege ferenda fordernd]; Langenberg, Betriebskosten- und Heizkostenrecht, 7. Aufl., K Rn. 189) analoge Anwendung des § 9a HeizkostenV kommt nicht in Betracht. Die analoge Anwendung einer Einzelnorm verlangt, dass der von dieser Vorschrift nicht geregelte Sachverhalt, der in den Anwendungsbereich der Norm gezogen werden soll, mit den von ihr erfassten Sachverhalten vergleichbar ist (BGH, Urteil vom 13. Juli 1988 - IVa ZR 55/87, BGHZ 105, 140, 143). Daran fehlt es hier. Die unter § 9a Abs. 1 HeizkostenV zu subsumierenden Sachverhalte haben ersichtlich Fallgestaltungen zum Gegenstand, in denen aus zwingenden Gründen (namentlich eines Geräteausfalls) eine ordnungsgemäße Erfassung des Verbrauchs nicht möglich ist. Derartige Sachverhalte sind nicht mit den hier in Rede stehenden Fällen vergleichbar, die dadurch gekennzeichnet sind, dass eine Verbrauchserfassung sehr wohl möglich ist und auch erfolgt.
b) Unzuträglichkeiten in der Abrechnung aufgrund eines hohen Leerstands kann im Einzelfall in anderer Weise Rechnung getragen werden.

</details>

<details><summary>BGH VIII ZR 9/14, Rn. 29–31</summary>

Eine allgemeine Aussage dazu, in welcher Fallkonstellation sich eine nach den Vorschriften der Heizkostenverordnung zutreffend berechnete Forderung nach den Grundsätzen von Treu und Glauben für den betroffenen Mieter als unzumutbare Belastung darstellt, so dass eine Begrenzung des Anspruchs des Vermieters der Höhe nach angezeigt ist, verbietet sich. Ob eine Anspruchskürzung geboten ist und gegebenenfalls in welchem Umfang, obliegt der Beurteilung des Tatrichters, der hierbei alle Umstände des jeweiligen Einzelfalls bei seiner Entscheidung zu berücksichtigen hat. Dabei hat der Tatrichter auch in seine Betrachtung einzubeziehen, dass eine absolute Verteilungsgerechtigkeit bei der Umlage von Betriebskosten vom Gesetz nicht gefordert wird (Senatsurteil vom 6. Oktober 2010 - VIII ZR 183/09, NJW 2010, 3645 Rn. 17). Es geht vielmehr darum, die beiderseitigen Interessen in der Gesamtschau zu einem angemessenen Ausgleich zu bringen.
Bereits das Amtsgericht hat zutreffend ausgeführt, dass in Gebäuden mit sehr hohen Leerständen sowohl der Vermieter als auch die verbleibenden Mieter erhebliche Nachteile erleiden. Die verbleibenden Mieter können von hohen Verbrauchskostenumlagen betroffen sein, während der Vermieter, ohne Mieteinnahmen zu haben, über den von ihm zu tragenden Wohnflächenanteil von 50 % ebenfalls nicht unbeträchtliche Kosten zu tragen hat. Dies trifft zu. Deshalb erscheint es auch nicht unbillig, wenn die verbleibenden Mieter einen angemessenen Teil der leerstandsbedingten Mehrkosten zu tragen haben.
Nach alledem kann das Berufungsurteil keinen Bestand haben; es ist aufzuheben (§ 562 Abs. 1 ZPO). Da keine weiteren Feststellungen zu treffen sind, hat der Senat in der Sache selbst zu entscheiden (§ 563 Abs. 3 ZPO).

</details>

<details><summary>§ 11 HeizkostenV</summary>

(1) Soweit sich die §§ 3 bis 7 auf die Versorgung mit Wärme beziehen, sind sie nicht anzuwenden
1. auf Räume,
a) in Gebäuden, die einen Heizwärmebedarf von weniger als 15 kWh/(m2 · a) aufweisen,
b) bei denen das Anbringen der Ausstattung zur Verbrauchserfassung, die Erfassung des Wärmeverbrauchs oder die Verteilung der Kosten des Wärmeverbrauchs nicht oder nur mit unverhältnismäßig hohen Kosten möglich ist; unverhältnismäßig hohe Kosten liegen vor, wenn diese nicht durch die Einsparungen, die in der Regel innerhalb von zehn Jahren erzielt werden können, erwirtschaftet werden können; oder
c) die vor dem 1. Juli 1981 bezugsfertig geworden sind und in denen der Nutzer den Wärmeverbrauch nicht beeinflussen kann;
2. a)
auf Alters- und Pflegeheime, Studenten- und Lehrlingsheime,
b) auf vergleichbare Gebäude oder Gebäudeteile, deren Nutzung Personengruppen vorbehalten ist, mit denen wegen ihrer besonderen persönlichen Verhältnisse regelmäßig keine üblichen Mietverträge abgeschlossen werden;
3. auf Räume in Gebäuden, die überwiegend versorgt werden
a) mit Wärme aus Anlagen zur Rückgewinnung von Wärme oder aus Solaranlagen oder
b) mit Wärme aus Anlagen der Kraft-Wärme-Kopplung oder aus Anlagen zur Verwertung von Abwärme, sofern der Wärmeverbrauch des Gebäudes nicht erfasst wird;
4. auf die Kosten des Betriebs der zugehörigen Hausanlagen, soweit diese Kosten in den Fällen des § 1 Absatz 3 nicht in den Kosten der Wärmelieferung enthalten sind, sondern vom Gebäudeeigentümer gesondert abgerechnet werden;
5. in sonstigen Einzelfällen, in denen die nach Landesrecht zuständige Stelle wegen besonderer Umstände von den Anforderungen dieser Verordnung befreit hat, um einen unangemessenen Aufwand oder sonstige unbillige Härten zu vermeiden.
(2) Soweit sich die §§ 3 bis 6 und § 8 auf die Versorgung mit Warmwasser beziehen, gilt Absatz 1 entsprechend.

</details>

---

## q20 (single)

**Question:** Can I still pass the cost of the building’s cable TV connection on to the tenants?

**Your reference answer:** Not the cable fees. The monthly basic fees for broadband cable connections and the related costs could only be passed on until 30 June 2024. For a distribution system connected to a broadband network, only the electricity to run it is still billable (§ 2 Nr. 15 b BetrKV).

**Agent's answer:**

> No, you can generally no longer pass on the regular cable TV fees or broadband connection fees to your tenants via the service charge statement (Nebenkostenabrechnung).
>
> ### Legal Details under the Current Statute
>
> 1. **Elimination of cable TV fee allocation (Nebenkostenprivileg):**
>    * Under **§ 2 Nr. 15 Buchstabe b BetrKV**, the passing on of running monthly base fees for broadband connections (*laufende monatliche Grundgebühren für Breitbandanschlüsse*) and fees under copyright law for cable retransmission (*Kabelweitersendung*) was only permitted **until June 30, 2024 (*bis zum 30. Juni 2024*)**.
>    * Furthermore, for systems installed on or after December 1, 2021, this option was already excluded entirely (**§ 2 Nr. 15 Satz 2 BetrKV**).
>
> 2. **What costs remain billable for cable systems:**
>    * Under **§ 2 Nr. 15 Buchstabe b BetrKV**, only the cost of operating electricity (*Betriebsstrom*) for the private distribution network connected to a broadband network (*mit einem Breitbandnetz verbundene private Verteilanlage*) can still be allocated.
>    * *(Note: Under **§ 2 Nr. 15 Buchstabe c BetrKV** and **§ 556 Abs. 3a BGB**, if the building has an in-house fiber-optic distribution network connected entirely via fiber-optic cable where the tenant can freely choose their provider, operating electricity and a fiber-optic provision fee (*Glasfaserbereitstellungsentgelt*) pursuant to § 72 Abs. 1 of the Telecommunications Act may be passed on, subject to specific statutory efficiency requirements).*
>
> 3. **Requirement of a contractual agreement:**
>    * Under **§ 556 Abs. 1 Satz 1 BGB**, operating costs (*Betriebskosten*) can only be passed on if the lease explicitly includes an allocation agreement (*Umlagevereinbarung*). Even for permissible items such as operating electricity, the costs cannot be billed unless agreed in the lease.

**Cited passages:**

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

---

## q21 (single)

**Question:** The annual statement showed a large back payment. Can I raise the tenant’s monthly advance payments now?

**Your reference answer:** Yes. After a statement, either side can adjust the advance payments to an appropriate amount by a declaration in text form (§ 560 Abs. 4 BGB).

**Agent's answer:**

> **Yes**, you can increase the monthly advance payments, provided certain legal conditions are met.
>
> ### Legal Basis and Requirements
>
> * **Right to adjust:** Under **§ 560 Abs. 4 BGB**, if advance payments for service charges (*Betriebskostenvorauszahlungen*) have been agreed in the contract, either contracting party may adjust them to a reasonable amount (*angemessene Höhe*) by declaration in text form (*Erklärung in Textform*) following an annual statement (*Abrechnung*).
> * **Text form requirement (*Textform*):** The notification must be provided in text form (for example, by letter, email, or directly included in the annual statement itself) pursuant to **§ 560 Abs. 4 BGB**.
> * **Reasonable amount (*angemessene Höhe*):** The adjustment must be reasonable. It is generally calculated based on the result of the past statement (for instance, dividing the total annual costs or the back payment by 12 months to set the new monthly rate). 
> * **Principle of economic efficiency (*Grundsatz der Wirtschaftlichkeit*):** Under **§ 560 Abs. 5 BGB**, the principle of economic efficiency must be observed when changing service charges.
>
> ---
>
> ### What Facts This Depends On
>
> 1. **Agreement in the lease (*Betriebskostenvorauszahlungen*):** Your lease must stipulate monthly advance payments subject to annual reconciliation, rather than a flat-rate lump sum (*Betriebskostenpauschale*) (see **§ 556 Abs. 2 BGB** and **§ 560 Abs. 1, 4 BGB**).
> 2. **A rendered annual statement (*Abrechnung*):** The adjustment can only be made *after* a statement has been issued (**§ 560 Abs. 4 BGB**).

**Cited passages:**

<details><summary>§§ 560–561 BGB</summary>

(1) Bei einer Betriebskostenpauschale ist der Vermieter berechtigt, Erhöhungen der Betriebskosten durch Erklärung in Textform anteilig auf den Mieter umzulegen, soweit dies im Mietvertrag vereinbart ist. Die Erklärung ist nur wirksam, wenn in ihr der Grund für die Umlage bezeichnet und erläutert wird.
(2) Der Mieter schuldet den auf ihn entfallenden Teil der Umlage mit Beginn des auf die Erklärung folgenden übernächsten Monats. Soweit die Erklärung darauf beruht, dass sich die Betriebskosten rückwirkend erhöht haben, wirkt sie auf den Zeitpunkt der Erhöhung der Betriebskosten, höchstens jedoch auf den Beginn des der Erklärung vorausgehenden Kalenderjahres zurück, sofern der Vermieter die Erklärung innerhalb von drei Monaten nach Kenntnis von der Erhöhung abgibt.
(3) Ermäßigen sich die Betriebskosten, so ist eine Betriebskostenpauschale vom Zeitpunkt der Ermäßigung an entsprechend herabzusetzen. Die Ermäßigung ist dem Mieter unverzüglich mitzuteilen.
(4) Sind Betriebskostenvorauszahlungen vereinbart worden, so kann jede Vertragspartei nach einer Abrechnung durch Erklärung in Textform eine Anpassung auf eine angemessene Höhe vornehmen.
(5) Bei Veränderungen von Betriebskosten ist der Grundsatz der Wirtschaftlichkeit zu beachten.
(6) Eine zum Nachteil des Mieters abweichende Vereinbarung ist unwirksam.
(1) Macht der Vermieter eine Mieterhöhung nach § 558 oder § 559 geltend, so kann der Mieter bis zum Ablauf des zweiten Monats nach dem Zugang der Erklärung des Vermieters das Mietverhältnis außerordentlich zum Ablauf des übernächsten Monats kündigen. Kündigt der Mieter, so tritt die Mieterhöhung nicht ein.
(2) Eine zum Nachteil des Mieters abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

---

## q22 (single)

**Question:** How long does a tenant have to object to the service charge statement?

**Your reference answer:** Twelve months after receiving the statement. After that, the tenant can't raise objections unless they weren't responsible for the delay (§ 556 Abs. 3 S. 5 and 6 BGB).

**Agent's answer:**

> Under German residential tenancy law, a tenant has until **the end of the twelfth month following receipt of the statement** to raise objections.
>
> ### Legal Rules and Deadlines
>
> 1. **Objection Period (*Einwendungsfrist*)**  
>    Under **§ 556 Abs. 3 Satz 5 BGB**, the tenant must notify the landlord of any objections to the statement (*Einwendungen gegen die Abrechnung*) at the latest by the end of the twelfth month after the statement was received (*Zugang der Abrechnung*).
>
> 2. **Preclusion of Objections (*Einwendungsausschluss*)**  
>    Under **§ 556 Abs. 3 Satz 6 BGB**, once this 12-month period expires, the tenant is strictly precluded from raising objections, unless the tenant was not responsible for the delay (*es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten*). 
>    * This preclusion also applies to substantive errors, such as incorrectly accounted prepayments, costs not agreed upon in the lease, or costs that are fundamentally non-allocable under the Service Charge Ordinance (*Betriebskostenverordnung*) (**BGH VIII ZR 209/15, Leitsatz**; **BGH VIII ZR 47/25, Rn. 31–32**).
>
> 3. **Mandatory Law (*Unabdingbarkeit*)**  
>    Under **§ 556 Abs. 5 BGB**, any agreement deviating from this rule to the detriment of the tenant is invalid. A landlord cannot shorten this period (for example, by stating in the invoice cover letter that objections must be raised within four weeks) (**BGH VIII ZR 47/25, Rn. 33**).
>
> 4. **Prerequisite: Formally Proper Statement (*formell ordnungsgemäße Abrechnung*)**  
>    The 12-month objection period only begins to run if the landlord has provided a formally proper statement (*formell ordnungsgemäße Betriebskostenabrechnung*) (**BGH VIII ZR 209/15, Rn. 15–17**; **BGH VIII ZR 47/25, Rn. 31–32**).

**Cited passages:**

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>BGH VIII ZR 209/15, Leitsatz</summary>

Der Einwendungsausschluss gemäß § 556 Abs. 3 Satz 6 BGB gilt grundsätzlich auch für solche Kosten, die gemäß § 556 Abs. 1 Satz 1 BGB in Verbindung mit der Betriebskostenverordnung in der Wohnraummiete generell nicht auf den Mieter umgelegt werden können.

</details>

<details><summary>BGH VIII ZR 47/25, Rn. 31–32</summary>

a) Der Beklagte ist, wie das Berufungsgericht zutreffend erkannt hat, mit Einwendungen gegen die - formell ordnungsgemäße (vgl. hierzu Senatsurteile vom 20. Januar 2016 - VIII ZR 93/15, NJW 2016, 866 Rn. 10; vom 19. Juli 2017 - VIII ZR 3/17, WuM 2017, 529 Rn. 15; jeweils mwN) - Betriebs- und Heizkostenabrechnung vom 5. Dezember 2018 für das Jahr 2017 betreffend die Wohnung Nr. 40020 gemäß § 556 Abs. 3 Satz 6 BGB ausgeschlossen. Denn er hat solche Einwendungen innerhalb der bis zum zwölften Monat nach Zugang der Abrechnung laufenden Frist des § 556 Abs. 3 Satz 5 BGB nicht erhoben. Nach Ablauf dieser Frist kann der Mieter Einwendungen jedoch nicht mehr geltend machen, es sei denn, er hätte die verspätete Geltendmachung nicht zu vertreten (§ 556 Abs. 3 Satz 6 BGB). Zu den Einwendungen gegen eine Betriebskostenabrechnung des Vermieters im Sinne von § 556 Abs. 3 Satz 5 und 6 BGB gehört auch der - hier von dem Beklagten mit Blick auf die ihm gegenüber abgerechneten Wärmelieferungskosten erhobene - Einwand, dass es für einzelne, nach § 556 Abs. 1 BGB grundsätzlich umlagefähige Betriebskosten an einer vertraglichen Vereinbarung über deren Umlage fehlt (vgl. Senatsurteile vom 10. Oktober 2007 - VIII ZR 279/06, NJW 2008, 283 Rn. 24; vom 12. Mai 2010 - VIII ZR 185/09, NJW 2010, 2275 Rn. 15). Feststellungen zu einem fehlenden Verschulden des Beklagten hat das Berufungsgericht nicht getroffen und die Revision zeigt übergangenen Sachvortrag insofern nicht auf.
Die Frist hat mit dem Zugang der Abrechnung bei dem Beklagten im Dezember 2018 zu laufen begonnen. Die Vorschrift des § 11 Abs. 3 der Verordnung über die Umstellung auf gewerbliche Wärmelieferung für Mietwohnraum vom 7. Juni 2013 (Wärmelieferverordnung - WärmeLV; im Folgenden: WärmeLV), wonach die Frist für Einwendungen gegen die Abrechnung der Wärmelieferungskosten (§ 556 Abs. 3 Satz 5 BGB) frühestens dann zu laufen beginnt, wenn der Mieter eine Mitteilung erhalten hat, die den Anforderungen nach § 11 Abs. 1 und 2 WärmeLV entspricht, findet - entgegen der Annahme der Revisionserwiderung - hier keine Anwendung. Sie regelt nur die Folgen einer fehlerhaften oder fehlenden Umstellungsankündigung im Sinne von § 556c Abs. 2 BGB (vgl. BAnz AT vom 20. Juni 2013 B 2, S. 8; siehe auch Lammel/Lammel, Heizkostenverordnung, 5. Aufl., § 1 WärmeLV Rn. 3). Die Vorschrift des § 556c BGB ist im vorliegenden Fall jedoch nicht anwendbar (siehe hierzu nachfolgend unter II 2 a).

</details>

<details><summary>BGH VIII ZR 47/25, Rn. 33</summary>

b) Entgegen der Ansicht der Revision ist die Klägerin auch nicht gehindert, sich auf den Einwendungsausschluss nach § 556 Abs. 3 Satz 6 BGB zu berufen, weil die Hausverwaltung der Klägerin dem Beklagten in dem Abrechnungsschreiben mitgeteilt hat, die Betriebskostenabrechnung gelte als anerkannt, wenn nicht innerhalb von vier Wochen nach Zugang dieses Schreibens schriftlich Einwände hiergegen erhoben würden. Ungeachtet dessen, dass der von der Revision neben der Vorschrift des § 242 BGB ebenfalls angeführten Bestimmung des § 323 Abs. 2 Nr. 1 BGB eine andere Wertung zugrunde liegt (vgl. BT-Drucks. 14/5663, S. 79; siehe auch Senatsurteile vom 10. Oktober 2007 - VIII ZR 279/06, NJW 2008, 283 Rn. 25; vom 11. Mai 2016 - VIII ZR 209/15, NJW 2016, 2254 Rn. 26), macht die Revision nicht geltend und es ist auch ansonsten nicht ersichtlich, dass die Klägerin durch das Setzen einer kürzeren als der in § 556 Abs. 3 Satz 5 BGB vorgesehenen Frist den Beklagten von der rechtzeitigen Geltendmachung seiner Einwendungen innerhalb der Frist des § 556 Abs. 3 Satz 5 BGB abgehalten hätte und die Berufung auf die Vorschrift des § 556 Abs. 3 Satz 6 BGB deshalb treuwidrig wäre (vgl. insoweit BGH, Beschluss vom 24. Oktober 2012 - IV ZB 13/12, NJW-RR 2013, 519 Rn. 13 [zum Ausschluss der Berufung auf eine gesetzliche Ausschlussfrist im Hinblick auf § 242 BGB]). Aus den vorstehend aufgezeigten Gründen liegt auch die von der Revision insoweit gerügte Verletzung von § 286 ZPO und Art. 103 Abs. 1 GG nicht vor.

</details>

<details><summary>BGH VIII ZR 209/15, Rn. 15–17</summary>

2. Das Berufungsgericht hat weiter zu Recht angenommen, dass den Klägern im Hinblick auf die in Höhe von 700 € geleistete, aber in der Abrechnung nicht berücksichtigte Vorauszahlung kein Anspruch auf Rückzahlung des entsprechenden Betrages aus § 812 Abs. 1 Satz 1 Alt. 1 BGB zusteht. Zwar ist die Nebenkostenabrechnung des Beklagten für das Jahr 2011 bezüglich der Vorauszahlungen unrichtig und haben die Kläger insoweit einen Betrag in Höhe von 700 € zu Unrecht - also ohne Rechtsgrund - gezahlt. Gleichwohl können sie diesen Betrag nicht mehr zurückfordern, weil sie ihre diesbezüglichen Einwendungen gegen die Abrechnung nicht innerhalb der Frist des § 566 Abs. 3 Satz 5 BGB vorgebracht haben und mit ihnen deshalb gemäß § 556 Abs. 3 Satz 6 BGB ausgeschlossen sind.
a) Nach § 556 Abs. 3 Satz 5 BGB obliegt es dem Mieter, gegenüber dem Vermieter Einwendungen gegen die Abrechnung bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Gemäß § 556 Abs. 3 Satz 6 BGB kann der Mieter nach Ablauf dieser Frist Einwendungen nicht mehr geltend machen, es sei denn, er hat die verspätete Geltendmachung nicht zu vertreten.
b) Zutreffend ist das Berufungsgericht auch davon ausgegangen, dass nur eine formell ordnungsgemäße Betriebskostenabrechnung die Frist gemäß § 556 Abs. 3 Satz 5, 6 BGB in Gang setzt, nach deren Ablauf der Mieter mit Einwendungen gegen die Abrechnung ausgeschlossen ist (Senatsurteil vom 8. Dezember 2010 - VIII ZR 27/10, NJW 2011, 1867 Rn. 15 ff.). Diese Voraussetzung ist hier indes erfüllt. Die formelle Ordnungsgemäßheit der Abrechnung der Nebenkosten für das Jahr 2011 vom 12. Juli 2012 wird von der Revision nicht in Zweifel gezogen und begegnet auch im Übrigen keinen Bedenken. Insbesondere stellen die dem Beklagten darin unterlaufenen Fehler, wie die zu niedrig angesetzten Vorauszahlungen sowie die Abrechnung von Betriebskosten, die gemäß § 1 Abs. 2 der Betriebskostenverordnung nicht auf den Mieter umgelegt werden können, lediglich inhaltliche Fehler der Abrechnung dar, die die formelle Ordnungsgemäßheit der Abrechnung nicht in Frage stellen (vgl. Senatsurteile vom 12. Januar 2012 - VIII ZR 148/10, NZM 2011, 240 Rn. 15; vom 18. Mai 2011 - VIII ZR 240/10, NJW 2011, 2786 Rn. 12; Senatsbeschlüsse vom 13. Dezember 2011 - VIII ZR 286/10, WuM 2012, 98 Rn. 3, vom 23. September 2009 - VIII ZA 2/08, NJW 2009, 3575 Rn. 6).

</details>

---

## q23 (single)

**Question:** Our building emits 30 kg CO2 per m² per year. What share of the CO2 costs can I bill to the tenants?

**Your reference answer:** 60%. A building emitting 30 kg CO2/m²/year falls in the 27 to < 32 kg band, so the tenant pays 60% and the landlord 40% of the CO2 costs (CO2KostAufG, Anlage, § 5).

**Agent's answer:**

> Under the Carbon Dioxide Cost Allocation Act (*Kohlendioxidkostenaufteilungsgesetz* – CO2KostAufG), the share of carbon dioxide costs (*Kohlendioxidkosten*) you can pass on to your tenants depends on the building's specific emission level:
>
> ### 1. Cost Split
> For an emission level of **30 kg CO₂ per m² per year** in a residential building, the property falls into the bracket **"27 bis < 32 kg CO2/m2/a"** under the graduated model (*Stufenmodell*) set out in **Anlage CO2KostAufG**:
> * **Tenant’s share (*Anteil Mieter*): 60%**
> * **Landlord’s share (*Anteil Vermieter*): 40%**
>
> Therefore, you may pass on **60%** of the total CO₂ costs to the tenants, while you as the landlord must absorb the remaining 40% (**§ 5 Abs. 2 CO2KostAufG**, **Anlage CO2KostAufG**).
>
> ---
>
> ### 2. Relevant Conditions and Billing Requirements
> Passing on this cost depends on several facts and statutory requirements:
>
> * **Building type:** This graduated model applies to residential buildings (*Wohngebäude*) where the landlord provides central heating or heat and hot water (**§ 5 Abs. 1, 2 CO2KostAufG**).
> * **Lease agreement and distribution:** The 60% collective share is distributed among the individual tenants according to the agreement in the lease on the distribution of heating and hot water costs based on §§ 6 to 10 of the Heating Costs Ordinance (*Heizkostenverordnung* – HeizkostenV) (**§ 7 Abs. 1 CO2KostAufG**).
> * **Mandatory disclosures in the bill:** In the annual heating cost statement (*Heizkostenabrechnung*), you must explicitly state the tenant’s share of the CO₂ costs, the classification of the building (*Einstufung des Gebäudes*), and the calculation basis (**§ 7 Abs. 3 CO2KostAufG**). 
> * **Right of reduction (*Kürzungsrecht*):** If you fail to determine the tenant’s share or fail to provide the required information, the tenant has the right to reduce their billed share of heating costs by **3 percent** (**§ 7 Abs. 4 CO2KostAufG**).

**Cited passages:**

<details><summary>Anlage CO2KostAufG</summary>

(Fundstelle: BGBl. I 2022, 2159)
Kohlendioxidausstoß des vermieteten Gebäudes oder der Wohnung pro Quadratmeter Wohnfläche und Jahr | Anteil Mieter | Anteil Vermieter
< 12 kg CO2/m2/a | 100 % | 0 %
12 bis < 17 kg CO2/m2/a | 90 % | 10 %
17 bis < 22 kg CO2/m2/a | 80 % | 20 %
22 bis < 27 kg CO2/m2/a | 70 % | 30 %
27 bis < 32 kg CO2/m2/a | 60 % | 40 %
32 bis < 37 kg CO2/m2/a | 50 % | 50 %
37 bis < 42 kg CO2/m2/a | 40 % | 60 %
42 bis < 47 kg CO2/m2/a | 30 % | 70 %
47 bis < 52 kg CO2/m2/a | 20 % | 80 %
> = 52 kg CO2/m2/a | 5 % | 95 %

</details>

<details><summary>§ 5 CO2KostAufG</summary>

(1) Der Vermieter ermittelt im Zuge der jährlichen Heizkostenabrechnung den Kohlendioxidausstoß des Gebäudes in Kilogramm Kohlendioxid pro Quadratmeter Wohnfläche und Jahr. Versorgt der Vermieter eine vermietete Wohnung gesondert mit Wärme oder mit Wärme und Warmwasser, ermittelt er den Kohlendioxidausstoß der Wohnung pro Quadratmeter Wohnfläche und Jahr; vermietet er in einem Gebäude mehrere Wohnungen mit gesonderter oder zentraler Versorgung mit Wärme oder mit Wärme und Warmwasser, ist deren Gesamtwohnfläche maßgeblich. Der Wert des nach Satz 1 oder Satz 2 ermittelten spezifischen Kohlendioxidausstoßes ist auf die erste Nachkommastelle zu runden. Ist ein Abrechnungszeitraum von unter einem Jahr vereinbart, so sind die Werte der Einstufungstabelle in der Anlage anteilig zu kürzen. Weichen die Abrechnungszeiträume der Brennstoff- oder Wärmelieferungen von den zwischen Mieter und Vermieter vereinbarten Abrechnungszeiträumen ab, sind die auf den Rechnungen ausgewiesenen Brennstoffemissionen auf den vereinbarten Zeitraum umzurechnen.
(2) Die Aufteilung der im Abrechnungszeitraum angefallenen Kohlendioxidkosten zwischen Mieter und Vermieter richtet sich nach dem spezifischen Kohlendioxidausstoß des Gebäudes oder, in Fällen des Absatzes 1 Satz 2, nach der zugrunde zu legenden Wohnfläche. Dieser Wert ist in die Tabelle in der Anlage einzuordnen, um das maßgebliche Aufteilungsverhältnis zu ermitteln.
(3) Versorgt sich der Mieter selbst mit Wärme oder mit Wärme und Warmwasser, ermittelt der Mieter im Zuge der jährlichen Betriebskostenabrechnung den Kohlendioxidausstoß der gemieteten Wohnung in Kilogramm Kohlendioxid pro Quadratmeter Wohnfläche und Jahr. Zur Einstufung der gemieteten Wohnung wird der spezifische Kohlendioxidausstoß mit der Tabelle in der Anlage abgeglichen und die Wohnung danach der anwendbaren Stufe zugeordnet. Aus der Tabelle ergibt sich das Verhältnis der Aufteilung der im Abrechnungszeitraum des Wärmeversorgers angefallenen Kohlendioxidkosten. Absatz 1 Satz 4 und 5 gilt entsprechend.

</details>

<details><summary>§ 7 CO2KostAufG</summary>

(1) Der Vermieter ermittelt die auf den oder die Mieter gemäß § 5 Absatz 1 Satz 1 oder 2 entfallenden Kohlendioxidkosten, indem er den im Abrechnungszeitraum verursachten Kohlendioxidausstoß gemäß § 5 Absatz 1 sowie die angefallenen Kohlendioxidkosten gemäß § 5 Absatz 2 berechnet und den auf den Vermieter entfallenden Anteil abzieht. Der Vermieter berechnet sodann den auf den einzelnen Mieter entfallenden Anteil an den Kohlendioxidkosten gemäß der Vereinbarung zwischen Vermieter und Mieter über die Verteilung der Heiz- und Warmwasserkosten auf Grundlage der §§ 6 bis 10 der Verordnung über Heizkostenabrechnung.
(2) Bei Wohngebäuden mit nicht mehr als zwei Wohnungen, von denen eine der Vermieter selbst bewohnt, und in den Fällen von § 11 der Verordnung über Heizkostenabrechnung, in denen die Vertragsparteien eine Abrechnung der Heiz- und Warmwasserkosten vereinbart haben, trägt der Mieter die auf ihn nach Absatz 1 entfallenden Kohlendioxidkosten entsprechend dem mit dem Vermieter vereinbarten Verfahren zur Abrechnung der Heizkosten.
(3) Der Vermieter weist in der Heizkostenabrechnung den auf den Mieter entfallenden Anteil an den Kohlendioxidkosten, die Einstufung des Gebäudes oder der Wohnung im Sinne von § 5 Absatz 1 Satz 1 oder 2 sowie die Berechnungsgrundlagen aus.
(4) Bestimmt der Vermieter den auf den einzelnen Mieter entfallenden Anteil an den Kohlendioxidkosten nicht oder weist er die gemäß Absatz 3 erforderlichen Informationen nicht aus, so hat der Mieter das Recht, den gemäß der Heizkostenabrechnung auf ihn entfallenden Anteil an den Heizkosten um 3 Prozent zu kürzen.
(5) Der Vermieter ermittelt die auf den oder die Mieter gemäß § 5a Absatz 3 entfallenden Kosten, indem er die im Abrechnungszeitraum verursachten Kosten gemäß § 5a Absatz 1 berechnet und den auf den Vermieter entfallenden Anteil nach § 5a Absatz 3 abzieht. Der Vermieter berechnet sodann den auf den einzelnen Mieter entfallenden Anteil an den Kosten gemäß der Vereinbarung zwischen Vermieter und Mieter über die Verteilung der Heiz- und Warmwasserkosten auf Grundlage der §§ 6 bis 10 der Verordnung über Heizkostenabrechnung. Absatz 4 ist entsprechend anwendbar.

</details>

---

## q24 (single)

**Question:** What share of the heating costs do I have to bill by actual consumption?

**Your reference answer:** At least 50% and at most 70% must be billed by recorded consumption. In buildings that don't meet the 1994 insulation standard, are heated by oil or gas, and have mostly insulated exposed pipes, it must be exactly 70% (§ 7 Abs. 1 HeizkostenV).

**Agent's answer:**

> Under German law, the share of heating costs that must be billed based on actual recorded consumption is governed by the Heating Costs Ordinance (*Heizkostenverordnung* – HeizkostenV):
>
> ### 1. General Rule: 50% to 70%
> Under **§§ 7–8 HeizkostenV** (specifically § 7 Abs. 1 Satz 1 HeizkostenV), **at least 50% and at most 70%** of the operating costs of the central heating system must be allocated according to the recorded heat consumption (*erfasster Wärmeverbrauch*) of the users.
> * The choice of the allocation ratio within this range is left to the building owner pursuant to **§ 6 HeizkostenV** (§ 6 Abs. 4 Satz 1 HeizkostenV).
> * The remaining costs (30% to 50%) must be distributed based on living or usable floor space (*Wohn- oder Nutzfläche*) or enclosed volume (*umbauter Raum*) pursuant to **§§ 7–8 HeizkostenV** (§ 7 Abs. 1 Satz 5 HeizkostenV).
>
> ### 2. Mandatory 70% Rule
> Under **§§ 7–8 HeizkostenV** (§ 7 Abs. 1 Satz 2 HeizkostenV), the landlord **must bill exactly 70%** based on recorded heat consumption if **all three** of the following conditions are met:
> 1. The building does not meet the standards of the Thermal Insulation Ordinance of August 16, 1994 (*Wärmeschutzverordnung vom 16. August 1994*),
> 2. The building is supplied by an oil or gas heating system (*Öl- oder Gasheizung*), **and**
> 3. The exposed heat distribution pipes (*freiliegende Leitungen der Wärmeverteilung*) are predominantly insulated.
>
> ### Essential Prerequisite
> Whether you can pass these costs on to the tenant at all depends on the lease: under **§ 556 BGB** (§ 556 Abs. 1 Satz 1 BGB), the contracting parties must have agreed that the tenant bears operating costs (*Betriebskosten*).

**Cited passages:**

<details><summary>§§ 7–8 HeizkostenV</summary>

(1) Von den Kosten des Betriebs der zentralen Heizungsanlage sind mindestens 50 vom Hundert, höchstens 70 vom Hundert nach dem erfassten Wärmeverbrauch der Nutzer zu verteilen. In Gebäuden, die das Anforderungsniveau der Wärmeschutzverordnung vom 16. August 1994 (BGBl. I S. 2121) nicht erfüllen, die mit einer Öl- oder Gasheizung versorgt werden und in denen die freiliegenden Leitungen der Wärmeverteilung überwiegend gedämmt sind, sind von den Kosten des Betriebs der zentralen Heizungsanlage 70 vom Hundert nach dem erfassten Wärmeverbrauch der Nutzer zu verteilen. In Gebäuden, in denen die freiliegenden Leitungen der Wärmeverteilung überwiegend ungedämmt sind und deswegen ein wesentlicher Anteil des Wärmeverbrauchs nicht erfasst wird, kann der Wärmeverbrauch der Nutzer nach anerkannten Regeln der Technik bestimmt werden. Der so bestimmte Verbrauch der einzelnen Nutzer wird als erfasster Wärmeverbrauch nach Satz 1 berücksichtigt. Die übrigen Kosten sind nach der Wohn- oder Nutzfläche oder nach dem umbauten Raum zu verteilen; es kann auch die Wohn- oder Nutzfläche oder der umbaute Raum der beheizten Räume zu Grunde gelegt werden.
(2) Zu den Kosten des Betriebs der zentralen Heizungsanlage einschließlich der Abgasanlage gehören die Kosten des zur Wärmeerzeugung verbrauchten Stroms und der verbrauchten Brennstoffe und ihrer Lieferung, die Kosten des Betriebsstromes, die Kosten der Bedienung, Überwachung und Pflege der Anlage, der regelmäßigen Prüfung ihrer Betriebsbereitschaft und Betriebssicherheit einschließlich der Einstellung durch eine Fachkraft, der Reinigung der Anlage und des Betriebsraumes, die Kosten der Messungen nach dem Bundes-Immissionsschutzgesetz, die Kosten der Anmietung oder anderer Arten der Gebrauchsüberlassung einer Ausstattung zur Verbrauchserfassung sowie die Kosten der Verwendung einer Ausstattung zur Verbrauchserfassung einschließlich der Kosten der Eichung sowie der Kosten der Berechnung, Aufteilung und Abrechnungs- und Verbrauchsinformationen gemäß § 6a.
(3) Für die Verteilung der Kosten der Wärmelieferung gilt Absatz 1 Satz 1 und 3 bis 5 entsprechend.
(4) Zu den Kosten der Wärmelieferung gehören das Entgelt für die Wärmelieferung und die Kosten des Betriebs der zugehörigen Hausanlagen entsprechend Absatz 2.
(1) Von den Kosten des Betriebs der zentralen Warmwasserversorgungsanlage sind mindestens 50 vom Hundert, höchstens 70 vom Hundert nach dem erfassten Warmwasserverbrauch, die übrigen Kosten nach der Wohn- oder Nutzfläche zu verteilen.
(2) Zu den Kosten des Betriebs der zentralen Warmwasserversorgungsanlage gehören die Kosten der Wasserversorgung, soweit sie nicht gesondert abgerechnet werden, und die Kosten der Wassererwärmung entsprechend § 7 Absatz 2. Zu den Kosten der Wasserversorgung gehören die Kosten des Wasserverbrauchs, die Grundgebühren und die Zählermiete, die Kosten der Verwendung von Zwischenzählern, die Kosten des Betriebs einer hauseigenen Wasserversorgungsanlage und einer Wasseraufbereitungsanlage einschließlich der Aufbereitungsstoffe.
(3) Für die Verteilung der Kosten der Warmwasserlieferung gilt Absatz 1 entsprechend.
(4) Zu den Kosten der Warmwasserlieferung gehören das Entgelt für die Lieferung des Warmwassers und die Kosten des Betriebs der zugehörigen Hausanlagen entsprechend § 7 Absatz 2.

</details>

<details><summary>§ 6 HeizkostenV</summary>

(1) Der Gebäudeeigentümer hat die Kosten der Versorgung mit Wärme und Warmwasser auf der Grundlage der Verbrauchserfassung nach Maßgabe der §§ 7 bis 9 auf die einzelnen Nutzer zu verteilen. Das Ergebnis der Ablesung bei nicht fernablesbaren Ausstattungen soll dem Nutzer in der Regel innerhalb eines Monats mitgeteilt werden. Eine gesonderte Mitteilung ist nicht erforderlich, wenn das Ableseergebnis über einen längeren Zeitraum in den Räumen des Nutzers gespeichert ist und von diesem selbst abgerufen werden kann. Einer gesonderten Mitteilung des Warmwasserverbrauchs bedarf es auch dann nicht, wenn in der Nutzeinheit ein Warmwasserzähler eingebaut ist.
(2) In den Fällen des § 5 Absatz 2 sind die Kosten zunächst mindestens zu 50 vom Hundert nach dem Verhältnis der erfassten Anteile am Gesamtverbrauch auf die Nutzergruppen aufzuteilen. Werden die Kosten nicht vollständig nach dem Verhältnis der erfassten Anteile am Gesamtverbrauch aufgeteilt, sind
1. die übrigen Kosten der Versorgung mit Wärme nach der Wohn- oder Nutzfläche oder nach dem umbauten Raum auf die einzelnen Nutzergruppen zu verteilen; es kann auch die Wohn- oder Nutzfläche oder der umbaute Raum der beheizten Räume zu Grunde gelegt werden,
2. die übrigen Kosten der Versorgung mit Warmwasser nach der Wohn- oder Nutzfläche auf die einzelnen Nutzergruppen zu verteilen.
Die Kostenanteile der Nutzergruppen sind dann nach Absatz 1 auf die einzelnen Nutzer zu verteilen.
(3) In den Fällen des § 4 Absatz 3 Satz 2 sind die Kosten nach dem Verhältnis der erfassten Anteile am Gesamtverbrauch auf die Gemeinschaftsräume und die übrigen Räume aufzuteilen. Die Verteilung der auf die Gemeinschaftsräume entfallenden anteiligen Kosten richtet sich nach rechtsgeschäftlichen Bestimmungen.
(4) Die Wahl der Abrechnungsmaßstäbe nach Absatz 2 sowie nach § 7 Absatz 1 Satz 1, §§ 8 und 9 bleibt dem Gebäudeeigentümer überlassen. Er kann diese für künftige Abrechnungszeiträume durch Erklärung gegenüber den Nutzern ändern
1. bei der Einführung einer Vorerfassung nach Nutzergruppen,
2. nach Durchführung von baulichen Maßnahmen, die nachhaltig Einsparungen von Heizenergie bewirken oder
3. aus anderen sachgerechten Gründen nach deren erstmaliger Bestimmung.
Die Festlegung und die Änderung der Abrechnungsmaßstäbe sind nur mit Wirkung zum Beginn eines Abrechnungszeitraumes zulässig.

</details>

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

---

## q25 (single)

**Question:** For years our tenant paid garden maintenance costs that weren’t in the lease, without complaining. Does that mean we have agreed he pays them?

**Your reference answer:** No. Just billing costs the lease doesn't cover and the tenant paying them doesn't change the lease; that needs special circumstances (BGH VIII ZR 36/14, Rn. 19). One example: you announce the new costs in advance and then bill them, and the tenant pays (Rn. 20).

**Agent's answer:**

> Whether your tenant’s uncomplaining payments mean you have agreed that they pay garden maintenance costs (Gartenpflege) depends on several key legal factors:
>
> ### 1. Does the lease already cover garden maintenance?
> Before looking at tacit agreements, check the cost allocation agreement (Umlagevereinbarung) in your lease:
> * Under **§ 556 BGB** (specifically § 556 Abs. 1), the contracting parties can agree that the tenant bears operating costs (Betriebskosten).
> * In residential tenancies, it is sufficient to agree—even in standard contract terms—that the tenant bears "the operating costs" (*„die Betriebskosten“*). Even without an attached list or express statutory citation, such a clause validly agrees to the allocation of all operating costs defined in the statute and specified in the Betriebskostenverordnung (**BGH VIII ZR 137/15, Leitsatz**, decided 2016-02-10).
> * Under **§ 2 Nr. 5–13 BetrKV** (specifically Nr. 10), operating costs include garden maintenance (*Kosten der Gartenpflege*), which covers the maintenance of landscaped areas including the renewal of plants and shrubs (see also **BGH VIII ZR 107/20, Leitsatz**, decided 2021-11-10).
> * Therefore, if your lease contains a general clause assigning "the operating costs" to the tenant, garden maintenance was already agreed upon from the start.
>
> ### 2. Can a tacit agreement (konkludente Vereinbarung) arise from payment?
> If the lease did not contain a general clause and instead listed specific operating costs that omitted garden maintenance:
> * An announcement of a change in service charges, followed by sending an accounting statement that includes the announced additional operating costs, constitutes an offer from the landlord to amend the operating cost allocation agreement (*Angebot zur Änderung der Betriebskostenumlagevereinbarung*), which the tenant can accept by paying the additional demand resulting from the statement or paying the adjusted advance payments (**BGH VIII ZR 47/25, Rn. 51–53**, decided 2026-05-20).
> * **Scope of the retrieved documents:** The indexed sources do not contain a ruling establishing whether the tenant's unobjected payment of annual statements over years *without* any prior announcement or explanation automatically constitutes a binding tacit agreement for future years. Because this requires interpreting the specific facts of the individual tenancy, you should consult a **tenancy lawyer (Fachanwalt für Miet- und Wohnungseigentumsrecht)**.
>
> ### 3. Preclusion of objections for past years (Einwendungsausschluss)
> Regardless of future liability, settled past billing periods are subject to strict statutory deadlines:
> * Under **§ 556 BGB** (specifically § 556 Abs. 3), the tenant must communicate objections to the statement (*Einwendungen gegen die Abrechnung*) no later than the end of the twelfth month after receiving it; after that deadline, the tenant is excluded from raising objections.
> * This statutory preclusion of objections (*Einwendungsausschluss*) applies broadly, even to costs that generally cannot be passed on to residential tenants under statutory operating cost rules (**BGH VIII ZR 209/15, Leitsatz**, decided 2016-05-11). Consequently, for past accounting periods where this 12-month objection period has expired, the tenant cannot reclaim past payments on the grounds that garden maintenance was not originally agreed upon.

**Cited passages:**

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>BGH VIII ZR 137/15, Leitsatz</summary>

In der Wohnraummiete genügt zur Übertragung der Betriebskosten auf den Mieter die - auch formularmäßige - Vereinbarung, dass dieser "die Betriebskosten" zu tragen hat. Auch ohne Beifügung des Betriebskostenkatalogs oder ausdrückliche Bezugnahme auf § 556 Abs. 1 Satz 2 BGB und die Betriebskostenverordnung vom 25. November 2003 (BGBl. I. S. 2347) ist damit die Umlage der in § 556 Abs. 1 Satz 2 BGB definierten und in der Betriebskostenverordnung erläuterten Betriebskosten vereinbart.

</details>

<details><summary>§ 2 Nr. 5–13 BetrKV</summary>

hierzu gehören das Entgelt für die Lieferung des Warmwassers und die Kosten des Betriebs der zugehörigen Hausanlagen entsprechend Nummer 4 Buchstabe a
oder
c) der Reinigung und Wartung von Warmwassergeräten,
hierzu gehören die Kosten der Beseitigung von Wasserablagerungen und Verbrennungsrückständen im Innern der Geräte sowie die Kosten der regelmäßigen Prüfung der Betriebsbereitschaft und Betriebssicherheit und der damit zusammenhängenden Einstellung durch eine Fachkraft;
6. die Kosten verbundener Heizungs- und Warmwasserversorgungsanlagen
a) bei zentralen Heizungsanlagen entsprechend Nummer 4 Buchstabe a und entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind,
oder
b) bei der eigenständig gewerblichen Lieferung von Wärme entsprechend Nummer 4 Buchstabe c und entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind,
oder
c) bei verbundenen Etagenheizungen und Warmwasserversorgungsanlagen entsprechend Nummer 4 Buchstabe d und entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind;
7. die Kosten des Betriebs des Personen- oder Lastenaufzugs,
hierzu gehören die Kosten des Betriebsstroms, die Kosten der Beaufsichtigung, der Bedienung, Überwachung und Pflege der Anlage, der regelmäßigen Prüfung ihrer Betriebsbereitschaft und Betriebssicherheit einschließlich der Einstellung durch eine Fachkraft sowie die Kosten der Reinigung der Anlage;
8. die Kosten der Straßenreinigung und Müllbeseitigung,
zu den Kosten der Straßenreinigung gehören die für die öffentliche Straßenreinigung zu entrichtenden Gebühren und die Kosten entsprechender nicht öffentlicher Maßnahmen; zu den Kosten der Müllbeseitigung gehören namentlich die für die Müllabfuhr zu entrichtenden Gebühren, die Kosten entsprechender nicht öffentlicher Maßnahmen, die Kosten des Betriebs von Müllkompressoren, Müllschluckern, Müllabsauganlagen sowie des Betriebs von Müllmengenerfassungsanlagen einschließlich der Kosten der Berechnung und Aufteilung;
9. die Kosten der Gebäudereinigung und Ungezieferbekämpfung,
zu den Kosten der Gebäudereinigung gehören die Kosten für die Säuberung der von den Bewohnern gemeinsam genutzten Gebäudeteile, wie Zugänge, Flure, Treppen, Keller, Bodenräume, Waschküchen, Fahrkorb des Aufzugs;
10. die Kosten der Gartenpflege,
hierzu gehören die Kosten der Pflege gärtnerisch angelegter Flächen einschließlich der Erneuerung von Pflanzen und Gehölzen, der Pflege von Spielplätzen einschließlich der Erneuerung von Sand und der Pflege von Plätzen, Zugängen und Zufahrten, die dem nicht öffentlichen Verkehr dienen;
11. die Kosten der Beleuchtung,
hierzu gehören die Kosten des Stroms für die Außenbeleuchtung und die Beleuchtung der von den Bewohnern gemeinsam genutzten Gebäudeteile, wie Zugänge, Flure, Treppen, Keller, Bodenräume, Waschküchen;
12. die Kosten der Schornsteinreinigung,
hierzu gehören die Kehrgebühren nach der maßgebenden Gebührenordnung, soweit sie nicht bereits als Kosten nach Nummer 4 Buchstabe a berücksichtigt sind;
13. die Kosten der Sach- und Haftpflichtversicherung,

</details>

<details><summary>BGH VIII ZR 107/20, Leitsatz</summary>

Die Kosten der Fällung eines - wie hier - morschen, nicht mehr standsicheren Baums sind grundsätzlich umlagefähige Kosten der Gartenpflege im Sinne von § 2 Nr. 10 BetrKV.

</details>

<details><summary>BGH VIII ZR 47/25, Rn. 51–53</summary>

Jedoch stellt etwa die Ankündigung einer Änderung der Nebenkosten sowie die nachfolgende Übersendung einer Abrechnung, in die auch die mitgeteilten zusätzlichen Betriebskosten eingestellt sind, aus der maßgeblichen Sicht des objektiven Empfängers ein Angebot zur Änderung der Betriebskostenumlagevereinbarung dar, das der Mieter durch Begleichung einer auf der Abrechnung beruhenden Nachforderung oder Zahlung der daraufhin angepassten (erhöhten) Vorauszahlungen akzeptiert haben kann (vgl. Senatsurteil vom 9. Juli 2014 - VIII ZR 36/14, aaO Rn. 20; siehe auch Senatsurteil vom 21. Januar 2004 - VIII ZR 101/03, WuM 2004, 151 unter II 2 c [zur Umlage von Aufzugskosten]).
bb) Gemessen daran ist das Berufungsgericht - wie bereits das Amtsgericht - zunächst rechtsfehlerfrei davon ausgegangen, dass sich die Parteien im vorliegenden Fall - wie auch die Revision und die Revisionserwiderung in der mündlichen Verhandlung vor dem Senat bestätigt haben - jedenfalls auf eine Umlage derjenigen Kosten geeinigt haben, die auch bei einem Betrieb der Wärmeversorgungsanlage durch die Klägerin selbst gemäß § 7 Abs. 2 HeizkostenV aF, § 8 Abs. 2 HeizkostenV auf den Beklagten umzulegen gewesen wären. Denn die Hausverwaltung der Klägerin hat dem Beklagten mit Schreiben vom 23. Juni 2015 mitgeteilt, dass er nunmehr an die neue zentrale Heizungsversorgung der Wärmelieferantin angeschlossen sei, die künftigen Nebenkostenabrechnungen auch die Kosten für die Heizung beinhalten würden und der Beklagte zukünftig monatliche Heizkostenvorauszahlungen zu leisten habe. Diese Heizkostenvorauszahlungen hat der Beklagte in der Folgezeit unstreitig erbracht.
Soweit die Revision darüber hinaus meint, der Beklagte habe lediglich der Umlage von Wärmekosten in Höhe der monatlich geleisteten Vorauszahlungen zugestimmt, übergeht sie, dass der Beklagte sich nicht mit der Leistung einer Pauschale, sondern mit monatlich zu leistenden Vorauszahlungen, über die gemäß § 556 Abs. 3 Satz 1 Halbs. 1 BGB jährlich abzurechnen ist und die dementsprechend auch zu Nachforderungen des Vermieters führen können, einverstanden erklärt hat (§§ 133, 157 BGB).

</details>

<details><summary>BGH VIII ZR 209/15, Leitsatz</summary>

Der Einwendungsausschluss gemäß § 556 Abs. 3 Satz 6 BGB gilt grundsätzlich auch für solche Kosten, die gemäß § 556 Abs. 1 Satz 1 BGB in Verbindung mit der Betriebskostenverordnung in der Wohnraummiete generell nicht auf den Mieter umgelegt werden können.

</details>

---

## q26 (multi)

**Question:** We rent our smoke detectors from a company that also inspects them every year, and it’s all on one invoice. Which part can I pass on to the tenants?

**Your reference answer:** Only the inspection part. The rental fees for the detectors can't be passed on (BGH VIII ZR 379/20), but the annual inspection can, as other operating costs under § 2 Nr. 17 BetrKV (BGH VIII ZR 117/21). You have to be able to separate the two on the invoice.

**Agent's answer:**

> Only the **annual inspection and maintenance part** can be passed on to the tenants; the **rental part cannot be passed on**. Because both items are on a single invoice, you must separate them and bill only the maintenance amount.
>
> ### 1. The rental portion cannot be passed on
> The costs for renting smoke detectors (*Miete von Rauchwarnmeldern*) are not considered "other operating costs" (*sonstige Betriebskosten*) under § 2 Nr. 17 BetrKV. Instead, they are treated as equivalent to acquisition costs (*Erwerbskosten*) and are expenses that cannot be passed on to tenants as service charges (*betriebskostenrechtlich nicht umlagefähige Aufwendungen*) (**BGH VIII ZR 379/20, Leitsatz**; **BGH VIII ZR 379/20, Rn. 33–35**).
>
> ### 2. The annual inspection and maintenance portion can be passed on
> The costs for the regular inspection and ensuring the operational readiness (*regelmäßige Prüfung und Sicherstellung der Betriebsbereitschaft*) of smoke detectors installed in rented premises are chargeable to the tenant as "other operating costs" (*sonstige Betriebskosten*) under § 2 Nr. 17 BetrKV (**BGH VIII ZR 117/21, Leitsatz**). 
>
> ### What this depends on:
> * **A contractual allocation agreement (*Umlagevereinbarung*):** Passing on these costs depends on the terms of the lease. They are only recoverable if covered by a lease agreement that provides for the allocation of such costs, such as a clause covering the operation of fire protection and fire alarm systems (*Kosten des Betriebs von Brandschutz- und Brandmeldeanlagen*) (**BGH VIII ZR 117/21, Leitsatz**; **BGH VIII ZR 117/21, Rn. 50–52**). If the lease does not contain an agreement covering these costs, they cannot be billed to the tenant.
> * **Separation of the invoice items:** Because the rental and maintenance fees are combined on one invoice, you must separate the non-billable device rental costs from the billable maintenance costs and charge only the maintenance share.
>
> ⚠ Citation check: these citations could not be matched to the retrieved passages, verify them before relying on this answer: § 2 Nr. 17 BetrKV

**Cited passages:**

<details><summary>BGH VIII ZR 379/20, Leitsatz</summary>

Bei den Kosten für die Miete von Rauchwarnmeldern handelt es sich nicht um sonstige Betriebskosten im Sinne von § 2 Nr. 17 BetrKV, sondern - da sie den Kosten für den Erwerb von Rauchwarnmeldern gleichzusetzen sind - um betriebskostenrechtlich nicht umlagefähige Aufwendungen.

</details>

<details><summary>BGH VIII ZR 379/20, Rn. 33–35</summary>

Zwar ist der Klägerin dieser Aufwand - wie das Berufungsgericht zutreffend erkannt hat - erst infolge neuerer technischer und damit einhergehender rechtlicher Entwicklungen (hier: Pflicht zur Ausstattung von Wohnungen mit Rauchwarnmeldern gemäß der ab dem 1. April 2013 geltenden Regelung des § 49 Abs. 7 BauO NRW; seit dem 1. Januar 2019 durch § 47 Abs. 3 BauO NRW abgelöst) entstanden. Ihrem Wesen nach sind diese Kosten indes nicht als umlagefähige Betriebskosten einzustufen (so etwa - jedenfalls im Ergebnis - auch: LG Hagen, ZMR 2016, 701; LG Düsseldorf, ZMR 2020, 650, 651; LG Berlin, WuM 2021, 367; Langenberg/Zehelein, aaO A Rn. 37, 309; Wall, aaO Rn. 4778 f.; MünchKommBGB/Zehelein, aaO, § 2 BetrKV Rn. 79; Schmidt-Futterer/Lehmann-Richter, aaO, § 556 BGB Rn. 304; Blank/Börstinghaus, Miete, 6. Aufl., § 556 BGB Rn. 100; BeckOGK-BGB/Drager, Stand: 1. Juli 2021, § 556 Rn. 67.1; aA etwa LG Magdeburg, NJW 2012, 544, 545; AG Hamburg-Altona, ZMR 2014, 801, 802; Pistorius, ZMR 2011, 934).
aa) Kosten für die Miete von Rauchwarnmeldern fallen ausschließlich dann an, wenn der Vermieter sich - was allein in seiner Entscheidungsmacht steht - dazu entschließt, die in der Mietwohnung zu installierenden Rauchwarnmelder nicht zu Eigentum zu erwerben, sondern sie stattdessen anzumieten. Wie oben aufgezeigt, wären die Kosten für den Erwerb von Rauchwarnmeldern - selbst wenn sie infolge einer Fremdfinanzierung nicht nur einmalig, sondern periodisch und deshalb möglicherweise laufend im Sinne von § 1 Abs. 1 Satz 1 BetrKV anfielen - nicht umlagefähig.
Es ließe sich mit dem oben aufgezeigten in den Gesetzesmaterialien eindeutig zum Ausdruck gebrachten Willen des Verordnungsgebers, dass Kosten für die Anschaffung von Betriebsmitteln grundsätzlich nicht zu den umlagefähigen Betriebskosten gehören (vgl. BR-Drucks. 568/03, S. 29), nicht vereinbaren, wenn man die - vom Vermieter anstatt eines Erwerbs gewählte - Miete von Rauchwarnmeldern demgegenüber als umlagefähige (sonstige) Betriebskosten einordnete. Denn das bedeutete im Ergebnis, dass dem Vermieter ein Weg eröffnet würde, auf einfache Weise - nicht nur im Fall der Ausstattung einer Wohnung mit Rauchwarnmeldern, sondern auch in anderen Fällen, in denen er das Mietobjekt mit bestimmten Einrichtungen zu versehen hätte - die im Grundsatz ihm zugewiesene Belastung mit Anschaffungskosten zu umgehen, indem er die allein ihm obliegende wirtschaftliche Entscheidung zugunsten einer Miete anstatt eines Kaufs des fraglichen Betriebsmittels träfe.

</details>

<details><summary>BGH VIII ZR 117/21, Leitsatz</summary>

1. Die Kosten eines externen Dienstleisters für die regelmäßige Kontrolle der Restmüllbehälter des Mietobjekts auf Einhaltung der satzungsmäßigen Vorgaben für die Mülltrennung und für die bei fehlerhafter Abfalltrennung erfolgende Nachsortierung von Hand sind im Wohnraummietverhältnis gemäß § 2 Nr. 8 BetrKV auf den Mieter umlegbare Betriebskosten.
2. Die Kosten für die regelmäßige Prüfung und Sicherstellung der Betriebsbereitschaft von in den Mieträumen angebrachten Rauchwarnmeldern sind im Wohnraummietverhältnis als "sonstige Betriebskosten" im Sinne von § 2 Nr. 17 BetrKV auf den Mieter umlegbar. Sie werden von einer vertraglichen Umlagevereinbarung erfasst, welche die Umlage der Kosten des Betriebs von Brandschutz- und Brandmeldeanlagen auf den Mieter vorsieht.
Dem stehen Regelungen in den Bauordnungen der Länder (hier: § 48 Abs. 4 Satz 4 BauO Bln), nach denen (öffentlich-rechtlich) die Wartung dem Mieter obliegt, nicht entgegen.

</details>

<details><summary>BGH VIII ZR 117/21, Rn. 50–52</summary>

bb) Eine andere Bewertung, insbesondere eine Zuordnung zu den nicht auf den Mieter umlegbaren Verwaltungskosten im Sinne von § 1 Abs. 2 Nr. 1BetrKV, ist entgegen der Ansicht der Revision nicht deshalb geboten, weil die Beklagte mit der Wartung der Rauchwarnmelder zugleich Vorsorge im eigenen Interesse - zur Erfüllung einer eigenen Verkehrssicherungspflicht als Gebäudeeigentümerin und damit zur Vermeidung einer Inanspruchnahme auf Schadensersatz - betreibt (so aber auch AG Dortmund, WuM 2017, 203, 204; AG Gelsenkirchen, WuM 2022, 158). Denn die Erfüllung von Verkehrssicherungspflichten ist als rein haftungsrechtlicher Gesichtspunkt kein maßgebendes Kriterium zur Abgrenzung zwischen Instandhaltungs- und Betriebskosten; vielmehr können auch Kosten für Maßnahmen, die zudem der Wahrnehmung einer Verkehrssicherungspflicht des Vermieters dienen, als Betriebskosten umlagefähig sein(Senatsurteil vom 10. November 2021 - VIII ZR 107/20, NZM 2022, 175 Rn. 25; vgl. auch Senatsurteil vom 14. Februar 2007 - VIII ZR 123/06, NZM 2007, 282 Rn. 12; Langenberg/Zehelein, Betriebskosten- und Heizkostenrecht, 10. Aufl., Teil A Rn. 256). Das gilt in gleicher Weise für die Abgrenzung zu den in § 1 Abs. 2 Nr. 1 BetrKV genannten Verwaltungskosten (vgl. Senatsurteil vom 18. Dezember 2019 - VIII ZR 62/19, NZM 2020, 457 Rn. 18 ff. [für die Kontrolle und Überwachung durch einen Hauswart]).
b) Die Annahme des Berufungsgerichts, eine Umlagefähigkeit dieser Kosten ergebe sich im Streitfall aufgrund einer ergänzenden Vertragsauslegung, ist zwar rechtsfehlerhaft. Dies wirkt sich jedoch im Ergebnis nicht aus, weil die Parteien die Kosten jedenfalls mit der vertraglichen Vereinbarung in Nr. 1 Buchst. o der Anlage 4 des Mietvertrags wirksam auf die Kläger umgelegt haben.
aa) Das Berufungsgericht hat eine ergänzende Vertragsauslegung vorgenommen, obwohl deren Voraussetzungen vorliegend nicht gegeben sind. Insoweit durfte es nicht offenlassen, ob eine mietvertragliche Regelung - etwa die von ihm angeführte allgemeine Verweisung von Nr. 1 Buchst. o der Anlage 4 des Mietvertrags auf § 2 Nr. 17 BetrKV oder eine vertragliche Neukostenklausel - die Umlage der Wartungskosten für die Rauchwarnmelder auf die Kläger erlaubte.

</details>

---

## q27 (multi)

**Question:** We had a dying tree removed from the garden, and we pay someone to clean the playground and replace the sand in the sandpit. Can I bill the tenants for both?

**Your reference answer:** Yes, both. Removing a dying (abgängig) tree counts as garden maintenance (BGH VIII ZR 107/20), and § 2 Nr. 10 BetrKV explicitly covers maintaining playgrounds including replacing the sand.

**Agent's answer:**

> Yes, you can generally bill tenants for both measures as part of the operating costs for garden maintenance (**Kosten der Gartenpflege**), provided the lease agreement allows for it. 
>
> Here are the details and requirements based on statutory law and case law:
>
> ---
>
> ### 1. Removing a Dying Tree
> * **Billability:** The costs of felling and removing a rotten, diseased, or dying tree that is no longer structurally sound are fundamentally billable as garden maintenance costs (**Gartenpflege**) under **§ 2 Nr. 10 BetrKV** (**BGH VIII ZR 107/20, Leitsatz**).
> * **Legal Distinction:** The Federal Court of Justice (BGH) established that removing dead or decaying trees is not an excluded maintenance or repair measure (**Instandhaltungs- und Instandsetzungskosten**) under **§ 1 Abs. 2 Nr. 2 BetrKV**, but falls under the general scope of garden maintenance aimed at preserving the garden grounds (**BGH VIII ZR 107/20, Rn. 19–25**).
>
> ---
>
> ### 2. Playground Cleaning and Sand Replacement
> * **Billability:** These costs are expressly defined by statute as part of garden maintenance costs. Under **§ 2 Nr. 10 BetrKV**, garden maintenance specifically includes:
>   > *"... the maintenance of playgrounds including the renewal of sand ..."* (*"die Pflege von Spielplätzen einschließlich der Erneuerung von Sand"*).
> * Cleaning the playground and periodically replenishing or replacing the sand in a sandpit therefore squarely qualifies as billable operating costs (**Betriebskosten**).
>
> ---
>
> ### Key Requirements (What This Depends On)
> Whether you can actually charge these amounts to your tenants in their annual statement depends on the following factors:
>
> 1. **Lease Agreement Clause (**Umlagevereinbarung**):** 
>    Under **§ 556 Abs. 1 BGB**, operating costs can only be passed on to the tenant if the rental contract explicitly agrees that the tenant bears service charges, specifically naming garden maintenance (**Kosten der Gartenpflege**) or referencing **§ 2 Nr. 10 BetrKV**. If the lease does not include an agreement to allocate garden maintenance, you cannot bill either cost.
> 2. **First-Time Installation vs. Ongoing Maintenance:** 
>    The initial creation or initial equipping of a garden or playground (initial purchase/setup) cannot be billed as an operating cost; the measures must concern the ongoing upkeep, maintenance, and renewal of existing facilities and flora (**BGH VIII ZR 107/20, Rn. 40**; **§ 2 Nr. 10 BetrKV**).
> 3. **Principle of Economic Efficiency (**Wirtschaftlichkeitsgebot**):**
>    Under **§ 556 Abs. 3 Satz 1 BGB**, the landlord must adhere to the principle of economic efficiency when incurring and billing these operating expenses.

**Cited passages:**

<details><summary>§ 2 Nr. 5–13 BetrKV</summary>

hierzu gehören das Entgelt für die Lieferung des Warmwassers und die Kosten des Betriebs der zugehörigen Hausanlagen entsprechend Nummer 4 Buchstabe a
oder
c) der Reinigung und Wartung von Warmwassergeräten,
hierzu gehören die Kosten der Beseitigung von Wasserablagerungen und Verbrennungsrückständen im Innern der Geräte sowie die Kosten der regelmäßigen Prüfung der Betriebsbereitschaft und Betriebssicherheit und der damit zusammenhängenden Einstellung durch eine Fachkraft;
6. die Kosten verbundener Heizungs- und Warmwasserversorgungsanlagen
a) bei zentralen Heizungsanlagen entsprechend Nummer 4 Buchstabe a und entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind,
oder
b) bei der eigenständig gewerblichen Lieferung von Wärme entsprechend Nummer 4 Buchstabe c und entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind,
oder
c) bei verbundenen Etagenheizungen und Warmwasserversorgungsanlagen entsprechend Nummer 4 Buchstabe d und entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind;
7. die Kosten des Betriebs des Personen- oder Lastenaufzugs,
hierzu gehören die Kosten des Betriebsstroms, die Kosten der Beaufsichtigung, der Bedienung, Überwachung und Pflege der Anlage, der regelmäßigen Prüfung ihrer Betriebsbereitschaft und Betriebssicherheit einschließlich der Einstellung durch eine Fachkraft sowie die Kosten der Reinigung der Anlage;
8. die Kosten der Straßenreinigung und Müllbeseitigung,
zu den Kosten der Straßenreinigung gehören die für die öffentliche Straßenreinigung zu entrichtenden Gebühren und die Kosten entsprechender nicht öffentlicher Maßnahmen; zu den Kosten der Müllbeseitigung gehören namentlich die für die Müllabfuhr zu entrichtenden Gebühren, die Kosten entsprechender nicht öffentlicher Maßnahmen, die Kosten des Betriebs von Müllkompressoren, Müllschluckern, Müllabsauganlagen sowie des Betriebs von Müllmengenerfassungsanlagen einschließlich der Kosten der Berechnung und Aufteilung;
9. die Kosten der Gebäudereinigung und Ungezieferbekämpfung,
zu den Kosten der Gebäudereinigung gehören die Kosten für die Säuberung der von den Bewohnern gemeinsam genutzten Gebäudeteile, wie Zugänge, Flure, Treppen, Keller, Bodenräume, Waschküchen, Fahrkorb des Aufzugs;
10. die Kosten der Gartenpflege,
hierzu gehören die Kosten der Pflege gärtnerisch angelegter Flächen einschließlich der Erneuerung von Pflanzen und Gehölzen, der Pflege von Spielplätzen einschließlich der Erneuerung von Sand und der Pflege von Plätzen, Zugängen und Zufahrten, die dem nicht öffentlichen Verkehr dienen;
11. die Kosten der Beleuchtung,
hierzu gehören die Kosten des Stroms für die Außenbeleuchtung und die Beleuchtung der von den Bewohnern gemeinsam genutzten Gebäudeteile, wie Zugänge, Flure, Treppen, Keller, Bodenräume, Waschküchen;
12. die Kosten der Schornsteinreinigung,
hierzu gehören die Kehrgebühren nach der maßgebenden Gebührenordnung, soweit sie nicht bereits als Kosten nach Nummer 4 Buchstabe a berücksichtigt sind;
13. die Kosten der Sach- und Haftpflichtversicherung,

</details>

<details><summary>BGH VIII ZR 107/20, Leitsatz</summary>

Die Kosten der Fällung eines - wie hier - morschen, nicht mehr standsicheren Baums sind grundsätzlich umlagefähige Kosten der Gartenpflege im Sinne von § 2 Nr. 10 BetrKV.

</details>

<details><summary>§ 1 BetrKV</summary>

(1) Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Sach- und Arbeitsleistungen des Eigentümers oder Erbbauberechtigten dürfen mit dem Betrag angesetzt werden, der für eine gleichwertige Leistung eines Dritten, insbesondere eines Unternehmers, angesetzt werden könnte; die Umsatzsteuer des Dritten darf nicht angesetzt werden.
(2) Zu den Betriebskosten gehören nicht:
1. die Kosten der zur Verwaltung des Gebäudes erforderlichen Arbeitskräfte und Einrichtungen, die Kosten der Aufsicht, der Wert der vom Vermieter persönlich geleisteten Verwaltungsarbeit, die Kosten für die gesetzlichen oder freiwilligen Prüfungen des Jahresabschlusses und die Kosten für die Geschäftsführung (Verwaltungskosten),
2. die Kosten, die während der Nutzungsdauer zur Erhaltung des bestimmungsmäßigen Gebrauchs aufgewendet werden müssen, um die durch Abnutzung, Alterung und Witterungseinwirkung entstehenden baulichen oder sonstigen Mängel ordnungsgemäß zu beseitigen (Instandhaltungs- und Instandsetzungskosten).

</details>

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>BGH VIII ZR 107/20, Rn. 39–40</summary>

(2) Auch die Begründung zur Betriebskostenverordnung vom 25. November 2003, welche die Formulierung zu den Gartenpflegekosten aus Anlage 3 zu § 27 der II. BV unverändert übernommen hat, schließt die Kosten zur Fällung eines morschen beziehungsweise nicht mehr standsicheren Baums nicht von den Gartenpflegekosten nach § 2 Nr. 10 BetrKV aus. Insbesondere lässt die Begründung zur BetrKV, wonach auch das "Schneiden und Ausasten von Bäumen" zur Gartenpflege gehört (BR-Drucks. 568/03, S. 32), einen Rückschluss darauf nicht zu, dass (ausschließlich) nur solche - durchaus kostenintensive - Arbeiten an Bäumen, nicht jedoch die Fällung nicht erhaltbarer Bäume als umlagefähige Betriebskosten angesehen wurden.
ee) Schließlich kann sich die Revision nicht mit Erfolg darauf berufen, die Fällarbeiten seien mit solchen Kosten vergleichbar, die im Zuge der Anlegung des Gartens angefallen seien, weswegen, weil die Kosten einer sogenannten Erstausstattung nicht umlagefähig seien, auch diejenigen Kosten nicht auf den Mieter umgelegt werden könnten, welche der "Entfernung der Erstausstattung des Gartens" dienten. Zum einen lässt sich der Ausschluss der Umlagefähigkeit derartiger Entfernungskosten der Vorschrift des § 2 Nr. 10 BetrKV nicht entnehmen. Zum anderen fehlt es vorliegend - wie die Revisionserwiderung zutreffend geltend macht - an Feststellungen dazu, dass es sich bei dem gefällten Baum um die Erstausstattung der Grünfläche des Hausanwesens gehandelt habe. Übergangenen Sachvortrag hierzu zeigt die Revision nicht auf.

</details>

---

## q28 (multi)

**Question:** Last year I accidentally billed the caretaker’s on-call fee. The tenant only noticed 14 months after getting the statement. Do I have to refund it?

**Your reference answer:** Probably not. The on-call fee was never billable (BGH VIII ZR 62/19), but after the 12-month deadline the tenant is generally barred even for costs that can't be passed on at all (BGH VIII ZR 209/15; § 556 Abs. 3 S. 5 and 6 BGB), unless your statement itself showed the item as non-billable (§ 242 BGB, 209/15 Rn. 28).

**Agent's answer:**

> Generally, **no**, you do not have to refund the fee, because the tenant's objection is time-barred. 
>
> ### Legal Background and Preclusion of Objections
> * **12-month objection deadline:** Under **§ 556 Abs. 3 Satz 5 BGB**, the tenant must communicate objections to the statement (Einwendungen gegen die Abrechnung) to the landlord at the latest by the end of the twelfth month after receiving the statement.
> * **Preclusion of late objections:** Under **§ 556 Abs. 3 Satz 6 BGB**, after this period expires, the tenant can no longer assert objections unless they are not responsible for the delay (nicht zu vertreten).
> * **Application to non-allocable costs:** The Federal Court of Justice (*Bundesgerichtshof*) has ruled that this preclusion of objections (Einwendungsausschluss) also applies to costs that generally cannot be passed on to a tenant under § 556 Abs. 1 Satz 1 BGB and the Betriebskostenverordnung (**BGH VIII ZR 209/15, Leitsatz**; confirmed also in **BGH VIII ZR 47/25, Rn. 31**).
> * **No claim for refund:** Because the objection is precluded under § 556 Abs. 3 Satz 6 BGB, the tenant has no claim for repayment/refund (Anspruch auf Rückzahlung) under unjust enrichment rules (§ 812 Abs. 1 Satz 1 Alt. 1 BGB), even if the amount was wrongfully billed and paid (**BGH VIII ZR 209/15, Rn. 15**).
>
> ---
>
> ### What this depends on
> Your right to refuse the refund depends on two factors:
>
> 1. **Formal validity of the statement (formelle Ordnungsgemäßheit):**
>    Only a formally proper statement sets the 12-month preclusion period running (**BGH VIII ZR 209/15, Rn. 16**). Erroneously billing non-allocable costs is merely a substantive error (inhaltlicher Fehler) and does not impair the formal validity of the statement (**BGH VIII ZR 209/15, Rn. 16**). However, if the statement suffered from fundamental formal defects (e.g., missing essential minimum information such as an orderly summary of total costs, applicable allocation keys, or the deduction of prepayments), the deadline would not have started running.
> 2. **Tenant's fault for the delay:**
>    The preclusion applies unless the tenant is not responsible for the late objection (§ 556 Abs. 3 Satz 6 BGB; **BGH VIII ZR 47/25, Rn. 31**). Simply failing to notice or check the line item for 14 months does not excuse the delay.

**Cited passages:**

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>BGH VIII ZR 209/15, Leitsatz</summary>

Der Einwendungsausschluss gemäß § 556 Abs. 3 Satz 6 BGB gilt grundsätzlich auch für solche Kosten, die gemäß § 556 Abs. 1 Satz 1 BGB in Verbindung mit der Betriebskostenverordnung in der Wohnraummiete generell nicht auf den Mieter umgelegt werden können.

</details>

<details><summary>BGH VIII ZR 47/25, Rn. 31–32</summary>

a) Der Beklagte ist, wie das Berufungsgericht zutreffend erkannt hat, mit Einwendungen gegen die - formell ordnungsgemäße (vgl. hierzu Senatsurteile vom 20. Januar 2016 - VIII ZR 93/15, NJW 2016, 866 Rn. 10; vom 19. Juli 2017 - VIII ZR 3/17, WuM 2017, 529 Rn. 15; jeweils mwN) - Betriebs- und Heizkostenabrechnung vom 5. Dezember 2018 für das Jahr 2017 betreffend die Wohnung Nr. 40020 gemäß § 556 Abs. 3 Satz 6 BGB ausgeschlossen. Denn er hat solche Einwendungen innerhalb der bis zum zwölften Monat nach Zugang der Abrechnung laufenden Frist des § 556 Abs. 3 Satz 5 BGB nicht erhoben. Nach Ablauf dieser Frist kann der Mieter Einwendungen jedoch nicht mehr geltend machen, es sei denn, er hätte die verspätete Geltendmachung nicht zu vertreten (§ 556 Abs. 3 Satz 6 BGB). Zu den Einwendungen gegen eine Betriebskostenabrechnung des Vermieters im Sinne von § 556 Abs. 3 Satz 5 und 6 BGB gehört auch der - hier von dem Beklagten mit Blick auf die ihm gegenüber abgerechneten Wärmelieferungskosten erhobene - Einwand, dass es für einzelne, nach § 556 Abs. 1 BGB grundsätzlich umlagefähige Betriebskosten an einer vertraglichen Vereinbarung über deren Umlage fehlt (vgl. Senatsurteile vom 10. Oktober 2007 - VIII ZR 279/06, NJW 2008, 283 Rn. 24; vom 12. Mai 2010 - VIII ZR 185/09, NJW 2010, 2275 Rn. 15). Feststellungen zu einem fehlenden Verschulden des Beklagten hat das Berufungsgericht nicht getroffen und die Revision zeigt übergangenen Sachvortrag insofern nicht auf.
Die Frist hat mit dem Zugang der Abrechnung bei dem Beklagten im Dezember 2018 zu laufen begonnen. Die Vorschrift des § 11 Abs. 3 der Verordnung über die Umstellung auf gewerbliche Wärmelieferung für Mietwohnraum vom 7. Juni 2013 (Wärmelieferverordnung - WärmeLV; im Folgenden: WärmeLV), wonach die Frist für Einwendungen gegen die Abrechnung der Wärmelieferungskosten (§ 556 Abs. 3 Satz 5 BGB) frühestens dann zu laufen beginnt, wenn der Mieter eine Mitteilung erhalten hat, die den Anforderungen nach § 11 Abs. 1 und 2 WärmeLV entspricht, findet - entgegen der Annahme der Revisionserwiderung - hier keine Anwendung. Sie regelt nur die Folgen einer fehlerhaften oder fehlenden Umstellungsankündigung im Sinne von § 556c Abs. 2 BGB (vgl. BAnz AT vom 20. Juni 2013 B 2, S. 8; siehe auch Lammel/Lammel, Heizkostenverordnung, 5. Aufl., § 1 WärmeLV Rn. 3). Die Vorschrift des § 556c BGB ist im vorliegenden Fall jedoch nicht anwendbar (siehe hierzu nachfolgend unter II 2 a).

</details>

<details><summary>BGH VIII ZR 209/15, Rn. 15–17</summary>

2. Das Berufungsgericht hat weiter zu Recht angenommen, dass den Klägern im Hinblick auf die in Höhe von 700 € geleistete, aber in der Abrechnung nicht berücksichtigte Vorauszahlung kein Anspruch auf Rückzahlung des entsprechenden Betrages aus § 812 Abs. 1 Satz 1 Alt. 1 BGB zusteht. Zwar ist die Nebenkostenabrechnung des Beklagten für das Jahr 2011 bezüglich der Vorauszahlungen unrichtig und haben die Kläger insoweit einen Betrag in Höhe von 700 € zu Unrecht - also ohne Rechtsgrund - gezahlt. Gleichwohl können sie diesen Betrag nicht mehr zurückfordern, weil sie ihre diesbezüglichen Einwendungen gegen die Abrechnung nicht innerhalb der Frist des § 566 Abs. 3 Satz 5 BGB vorgebracht haben und mit ihnen deshalb gemäß § 556 Abs. 3 Satz 6 BGB ausgeschlossen sind.
a) Nach § 556 Abs. 3 Satz 5 BGB obliegt es dem Mieter, gegenüber dem Vermieter Einwendungen gegen die Abrechnung bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Gemäß § 556 Abs. 3 Satz 6 BGB kann der Mieter nach Ablauf dieser Frist Einwendungen nicht mehr geltend machen, es sei denn, er hat die verspätete Geltendmachung nicht zu vertreten.
b) Zutreffend ist das Berufungsgericht auch davon ausgegangen, dass nur eine formell ordnungsgemäße Betriebskostenabrechnung die Frist gemäß § 556 Abs. 3 Satz 5, 6 BGB in Gang setzt, nach deren Ablauf der Mieter mit Einwendungen gegen die Abrechnung ausgeschlossen ist (Senatsurteil vom 8. Dezember 2010 - VIII ZR 27/10, NJW 2011, 1867 Rn. 15 ff.). Diese Voraussetzung ist hier indes erfüllt. Die formelle Ordnungsgemäßheit der Abrechnung der Nebenkosten für das Jahr 2011 vom 12. Juli 2012 wird von der Revision nicht in Zweifel gezogen und begegnet auch im Übrigen keinen Bedenken. Insbesondere stellen die dem Beklagten darin unterlaufenen Fehler, wie die zu niedrig angesetzten Vorauszahlungen sowie die Abrechnung von Betriebskosten, die gemäß § 1 Abs. 2 der Betriebskostenverordnung nicht auf den Mieter umgelegt werden können, lediglich inhaltliche Fehler der Abrechnung dar, die die formelle Ordnungsgemäßheit der Abrechnung nicht in Frage stellen (vgl. Senatsurteile vom 12. Januar 2012 - VIII ZR 148/10, NZM 2011, 240 Rn. 15; vom 18. Mai 2011 - VIII ZR 240/10, NJW 2011, 2786 Rn. 12; Senatsbeschlüsse vom 13. Dezember 2011 - VIII ZR 286/10, WuM 2012, 98 Rn. 3, vom 23. September 2009 - VIII ZA 2/08, NJW 2009, 3575 Rn. 6).

</details>

---

## q29 (multi)

**Question:** I rent out a condo and the owners’ association hasn’t approved the annual statement yet. Do I have to wait for it, and when I use its figures, do I need to show how I removed the non-billable parts from the building totals?

**Your reference answer:** You can't wait. The one-year deadline applies even without the owners' association approving its statement (BGH VIII ZR 249/15, LS 1). And you only need to state the total you split among the tenants for each cost type, not how you removed the non-billable parts (BGH VIII ZR 93/15).

**Agent's answer:**

> ### 1. Prerequisite: Lease Agreement
> A landlord may only bill operating costs if the tenancy agreement contains an express agreement that the tenant bears service charges and pays advances on them (*Umlagevereinbarung*; **BGH VIII ZR 249/15, Rn. 5, 12–14**, decided 2017-01-25).
>
> ---
>
> ### 2. Waiting for the Owners' Association Statement Approval
> **You do not have to wait for the owners' association (*Wohnungseigentümergemeinschaft* – WEG) to approve the statement, and doing so risks losing your claim to back payments.**
>
> * **No legal prerequisite:** A formal resolution by the condominium owners (*Beschluss der Wohnungseigentümer*) approving the property manager's annual statement (*Jahresabrechnung*) is not an unwritten prerequisite for billing operating costs to the tenant (**BGH VIII ZR 249/15, Leitsatz**; **BGH VIII ZR 249/15, Rn. 20–21**, decided 2017-01-25). 
> * **Statutory 12-month billing deadline:** The landlord of a condominium unit must generally settle the tenant’s advance payments (*Betriebskostenvorauszahlungen*) within the statutory twelve-month deadline following the end of the billing period, even if the owners' resolution has not yet been passed (**BGH VIII ZR 249/15, Leitsatz**; **BGH VIII ZR 249/15, Rn. 15–17**).
> * **Preclusion of back payments (*Ausschlussfrist*):** If the twelve-month deadline is missed, the landlord is precluded from asserting back payments (*Nachforderungen*) unless the landlord is not responsible for the delay (**BGH VIII ZR 249/15, Rn. 5, 12–14**; **BGH VIII ZR 249/15, Rn. 15–17**).
> * **Delayed resolution does not excuse the landlord:** The WEG property manager (*Verwalter*) is not the landlord's vicarious agent (*Erfüllungsgehilfe*) regarding the landlord's contractual billing obligations toward the tenant (**BGH VIII ZR 249/15, Leitsatz**). To establish that a delay was unpreventable, the landlord must set out specifically what concrete efforts were undertaken to secure a timely statement (**BGH VIII ZR 249/15, Leitsatz**).
>
> ---
>
> ### 3. Disclosing Deductions of Non-Billable Costs
> **When using the figures, you do not need to show or explain the calculation steps used to deduct non-billable portions.**
>
> * **Formal requirement limited to allocated total:** For formal validity (*formelle Ordnungsgemäßheit*) of the statement, it is sufficient that the landlord states the total amount (*Gesamtbetrag*) for each cost category that is actually being allocated to the tenants of the chosen billing unit (**BGH VIII ZR 93/15, Leitsatz**, decided 2016-01-20).
> * **No duty to explain intermediate arithmetic steps:** This also applies when the landlord has cleaned up this total amount in advance by deducting cost portions that cannot be passed on to the tenant (*nicht umlagefähige Kostenanteile*). Disclosing and explaining the intermediate calculation steps (*Rechenschritte*) leading to the final total amount is not required (**BGH VIII ZR 93/15, Leitsatz**; **BGH VIII ZR 93/15, Rn. 19–21**).
> * **Substantive accuracy vs. formal validity:** Whether the landlord calculated the total amount correctly or improperly included non-billable costs is solely an issue of substantive correctness (*materielle Richtigkeit*), which the tenant can examine by inspecting the underlying receipts and accounting documents (*Belegeinsicht*) (**BGH VIII ZR 93/15, Rn. 19–21**).

**Cited passages:**

<details><summary>BGH VIII ZR 249/15, Rn. 5, 12–14</summary>

Die Revision hat keinen Erfolg.
Diese Beurteilung hält rechtlicher Nachprüfung stand, so dass die Revision zurückzuweisen ist.
Das Berufungsgericht hat rechtsfehlerfrei einen Anspruch des Klägers auf Zahlung restlicher Betriebskosten aus den Betriebskostenabrechnungen für die Jahre 2010, 2011 und 2012 verneint. Die Geltendmachung der Betriebskostennachforderungen für die Jahre 2010 und 2011 ist gemäß § 556 Abs. 3 Satz 3 BGB ausgeschlossen, weil der Kläger die Abrechnungsfrist gemäß § 556 Abs. 3 Satz 2 BGB nicht eingehalten und er nicht dargetan hat, dass er die verspätete Geltendmachung der Nachforderungen nicht zu vertreten hat. Entgegen der Auffassung der Revision hat der Vermieter einer Eigentumswohnung über die Betriebskostenvorauszahlungen des Mieters grundsätzlich auch dann innerhalb der Frist des § 556 Abs. 3 Satz 2 BGB abzurechnen, wenn zu diesem Zeitpunkt ein Beschluss der Wohnungseigentümer gemäß § 28 Abs. 5 WEG über die Jahresabrechnung (§ 28 Abs. 3 WEG) des Verwalters der Wohnungseigentümergemeinschaft noch nicht vorliegt. Hinsichtlich der Betriebskostenabrechnung für das Jahr 2012, die der Kläger der Beklagten rechtzeitig mitgeteilt hat, hat das Berufungsgericht eine Nachforderung des Klägers ebenfalls ohne Rechtsfehler verneint, da diese Forderung jedenfalls durch die vom Kläger vorgenommene Aufrechnung gegen das Kautionsguthaben der Beklagten erloschen ist (§ 389 BGB).
1. Haben die Parteien - wie hier der Fall - im Wohnraummietvertrag vereinbart, dass der Mieter die Betriebskosten trägt und hierfür Vorauszahlungen leistet (§ 535 Abs. 2, § 556 Abs. 1 Satz 1, Abs. 2 BGB), hat der Vermieter über die Vorauszahlungen jährlich abzurechnen (§ 556 Abs. 3 Satz 1 Halbs. 1 BGB). Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen (§ 556 Abs. 3 Satz 2 BGB). Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn der Vermieter hat die verspätete Geltendmachung nicht zu vertreten (§ 556 Abs. 3 Satz 3 BGB). Diese Grundsätze gelten, wie das Berufungsgericht zutreffend angenommen hat, auch für den Vermieter einer Eigentumswohnung.

</details>

<details><summary>BGH VIII ZR 249/15, Leitsatz</summary>

1. Der Vermieter einer Eigentumswohnung hat über die Betriebskostenvorauszahlungen des Mieters grundsätzlich auch dann innerhalb der Jahresfrist des § 556 Abs. 3 Satz 2 BGB abzurechnen, wenn zu diesem Zeitpunkt der Beschluss der Wohnungseigentümer gemäß § 28 Abs. 5 WEG über die Jahresabrechnung (§ 28 Abs. 3 WEG) des Verwalters der Wohnungseigentümergemeinschaft noch nicht vorliegt. Ein solcher Beschluss ist keine (ungeschriebene) Voraussetzung für die Abrechnung der Betriebskosten gemäß § 556 Abs. 3 BGB.
2. Der Verwalter einer Wohnungseigentümergemeinschaft ist als solcher nicht Erfüllungsgehilfe des Wohnungseigentümers nach § 278 BGB in Bezug auf dessen mietvertragliche Pflichten hinsichtlich der Abrechnung der Betriebskosten.
3. Für die nach § 556 Abs. 3 Satz 3 Halbs. 2 BGB mögliche Entlastung des Vermieters hinsichtlich einer von ihm nicht fristgerecht vorgenommenen Betriebskostenabrechnung hat dieser konkret darzulegen, welche Bemühungen er unternommen hat, um eine rechtzeitige Abrechnung sicherzustellen (Bestätigung und Fortführung des Senatsurteils vom 21. Januar 2009, VIII ZR 107/08, NJW 2009, 2197 Rn. 13).

</details>

<details><summary>BGH VIII ZR 249/15, Rn. 20–21</summary>

cc) Der letztgenannten Auffassung gebührt der Vorzug. Eine (ungeschriebene) Voraussetzung dahingehend, dass ein Beschluss der Wohnungseigentümer nach § 28 Abs. 5 WEG über die Jahresabrechnung des Verwalters der Wohnungseigentümergemeinschaft (§ 28 Abs. 3 WEG) vorliegen muss, um über die Betriebskosten bei vermietetem Wohnungseigentum abrechnen zu können, ergibt sich weder aus dem Wortlaut des § 556 Abs. 3 BGB noch aus den Gesetzesmaterialien, der Gesetzessystematik oder dem Sinn und Zweck dieser Vorschrift.
(1) Aus dem Wortlaut des § 556 BGB lässt sich nicht herleiten, dass ein Beschluss der Wohnungseigentümer gemäß § 28 Abs. 5 WEG über die vom Verwalter einer Wohnungseigentümergemeinschaft gemäß § 28 Abs. 3 WEG nach Ablauf des Kalenderjahres zu erstellenden Abrechnung über die gesamten im Kalenderjahr angefallenen tatsächlichen Einnahmen und Ausgaben der Wohnungseigentümergemeinschaft (vgl. hierzu BGH, Urteile vom 4. Dezember 2009 - V ZR 44/09, NJW 2010, 2127 Rn. 10; vom 17. Februar 2012 - V ZR 251/10, NJW 2012, 1434 Rn. 11; vom 11. Oktober 2013 - V ZR 271/12, NJW 2014, 145 Rn. 6; jeweils mwN) Voraussetzung für das Anfallen beziehungsweise die Fälligkeit und für die Abrechnung der Betriebskosten im Wohnraummietverhältnis ist. Nach der gesetzlichen Definition in § 556 Abs. 1 Satz 2 BGB, § 1 Abs. 1 Satz 1 BetrKV sind Betriebskosten diejenigen Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Über die Vorauszahlungen hat der Vermieter jährlich abzurechnen (§ 556 Abs. 3 Satz 1 BGB).

</details>

<details><summary>BGH VIII ZR 249/15, Rn. 15–17</summary>

2. Das Berufungsgericht ist mit Recht und von der Revision insoweit auch nicht angegriffen davon ausgegangen, dass der Kläger im Rahmen der von ihm kalenderjährlich vorgenommenen Abrechnungen der Betriebskosten die Betriebskostenabrechnungen für die Jahre 2010 und 2011 der Beklagten erst mit Schreiben vom 7. Dezember 2013 und damit - da die im Mietvertrag enthaltene handschriftliche Ergänzung der Abrechnungsregelung im Hinblick auf § 556 Abs. 4 BGB unwirksam ist - jeweils nicht innerhalb der Jahresfrist des § 556 Abs. 3 Satz 2 BGB mitgeteilt hat. Die Betriebskostenabrechnung für das Jahr 2010 hätte der Beklagten bis zum 31. Dezember 2011 und diejenige für das Jahr 2011 bis zum 31. Dezember 2012 mitgeteilt werden müssen.
a) Aufgrund dieser erst nach Ablauf der Frist des § 556 Abs. 3 Satz 2 BGB vorgenommenen Abrechnungen der Betriebskosten ist der Kläger hinsichtlich der Abrechnungszeiträume 2010 und 2011 mit Nachforderungen ausgeschlossen (§ 556 Abs. 3 Satz 3 Halbs. 1 BGB), da er nach der insoweit rechtsfehlerfreien Beurteilung des Berufungsgerichts nicht dargetan hat, dass er die verspätete Geltendmachung nicht zu vertreten hat (§ 556 Abs. 3 Satz 3 Halbs. 2 BGB; siehe hierzu nachfolgend unter II 2 b).
Dem Ablauf der Abrechnungsfrist steht nicht entgegen, dass die Wohnungseigentümer erst wenige Tage vor der durch Schreiben des Klägers vom 7. Dezember 2013 erfolgten Mitteilung der Betriebskostenabrechnung an die Beklagte den Beschluss nach § 28 Abs. 5 WEG über die Jahresabrechnung des Verwalters der Wohnungseigentümergemeinschaft (§ 28 Abs. 3 WEG) gefasst hatten. Denn entgegen der Auffassung der Revision ist das Vorliegen eines solchen Beschlusses der Wohnungseigentümer über die Jahresabrechnung - wie das Berufungsgericht mit Recht angenommen hat - keine (ungeschriebene) Voraussetzung für die Abrechnung der Betriebskosten des Vermieters einer vermieteten Eigentumswohnung gegenüber seinem Mieter. Vielmehr hat der Vermieter einer Eigentumswohnung grundsätzlich auch dann innerhalb der Frist des § 556 Abs. 3 Satz 2 BGB über die Vorauszahlung der Betriebskosten abzurechnen und dem Mieter diese Abrechnung mitzuteilen, wenn ein Beschluss der Wohnungseigentümer nach § 28 Abs. 5 WEG über die Jahresabrechnung noch nicht ergangen ist. Diese Frage, die der Senat bisher nicht zu entscheiden gehabt hat, ist in der Rechtsprechung der Instanzgerichte und in der Literatur allerdings umstritten.

</details>

<details><summary>BGH VIII ZR 93/15, Leitsatz</summary>

1. Zur formellen Ordnungsgemäßheit einer Betriebskostenabrechnung genügt es hinsichtlich der Angabe der "Gesamtkosten", wenn der Vermieter bei der jeweiligen Betriebskostenart den Gesamtbetrag angibt, den er auf die Wohnungsmieter der gewählten Abrechnungseinheit umlegt.
2. Dies gilt auch dann, wenn der Vermieter diesen Gesamtbetrag vorab um nicht auf den Mieter umlagefähige Kostenanteile bereinigt hat; einer Angabe und Erläuterung der zum angesetzten Gesamtbetrag führenden Rechenschritte bedarf es nicht (Aufgabe der Senatsrechtsprechung; vgl. Senatsurteile vom 14. Februar 2007, VIII ZR 1/06, NJW 2007, 1059 Rn. 10; und vom 9. Oktober 2013, VIII ZR 22/13, WuM 2013, 734 Rn. 14 ff. mwN).

</details>

<details><summary>BGH VIII ZR 93/15, Rn. 19–21</summary>

c) Vor dem Hintergrund der beschriebenen Interessenlage von Mieter und Vermieter und der dargestellten Entwicklung der Senatsrechtsprechung, hält der Senat die Auffassung, bei sogenannten "bereinigten" Kosten bedürfe es für die formelle Ordnungsgemäßheit einer Nebenkostenabrechnung zusätzlicher Angaben zu den Betriebskosten der gesamten Wohnanlage oder zu den Gesamtkosten einschließlich nicht umlagefähiger Kostenanteile und der Erläuterung insoweit angewendeter Rechenschritte, nicht mehr aufrecht. Vielmehr genügt es auch in diesen Fällen, wenn der Vermieter in der Abrechnung bei der jeweiligen Betriebskostenart - beziehungsweise, soweit eine Zusammenfassung mehrerer Betriebskostenarten zulässig ist (vgl. etwa Senatsurteil vom 15. Juli 2009 - VIII ZR 340/08, NZM 2009, 698 Rn. 18), bei dieser zusammengefassten Position - den Gesamtbetrag angibt, den er auf die Wohnungsmieter der gewählten Abrechnungseinheit umlegt. Ob der Vermieter diesen Gesamtbetrag zutreffend errechnet beziehungsweise ermittelt hat oder dabei Kostenanteile mit angesetzt hat, die nicht umlagefähig sind, ist ausschließlich eine Frage der materiellen Richtigkeit, deren Überprüfung der Mieter ohnehin nicht allein anhand der Abrechnung vornehmen kann, sondern nur mittels einer Einsicht in die Belege. Entsprechendes gilt für einen Vorwegabzug für die gewerbliche Nutzung einzelner Einheiten.
Nach alledem kann das Urteil des Berufungsgerichts keinen Bestand haben; es ist daher aufzuheben (§ 562 Abs. 1 ZPO).
Die Sache ist nicht zur Endentscheidung reif, weil das Berufungsgericht - vor dem Hintergrund seiner Rechtsauffassung folgerichtig - keine Feststellungen zur materiellen Richtigkeit der Abrechnung und zur hilfsweise erklärten Aufrechnung der Beklagten getroffen hat. Die Sache ist daher zur neuen Verhandlung und Entscheidung an das Berufungsgericht zurückzuverweisen (§ 563 Abs. 1 Satz 1 ZPO).
Dr. Milger Dr. Schneider Dr. Fetzer

</details>

---

## q30 (multi)

**Question:** Our building has a shop on the ground floor, and some flats are bigger than the lease says. How should I split the property tax?

**Your reference answer:** Split the property tax across all units without first taking out the shop's share (BGH VIII ZR 79/16). Where costs are split by floor area, use the actual sizes, not the ones in the lease (BGH VIII ZR 220/17).

**Agent's answer:**

> To split the property tax (*Grundsteuer*) correctly, two legal aspects must be addressed: the commercial unit on the ground floor and the deviation in apartment sizes. 
>
> ### 1. Prerequisite: Lease Agreement (*Umlagevereinbarung*)
> First, property tax can only be charged to the tenants if the lease agreement (*Mietvertrag*) expressly provides that the tenant bears the operating costs (*Betriebskosten*) pursuant to § 556 Abs. 1 BGB and § 2 Nr. 1 BetrKV.
>
> ---
>
> ### 2. The Ground Floor Shop: Is an Advance Deduction (*Vorwegabzug*) Required?
> **No.** For property tax, you do not need to separate or deduct the commercial share in advance:
>
> * According to the Federal Court of Justice (BGH), in the service charge settlement (*Betriebskostenabrechnung*) for a property used partly for commercial purposes and partly for residential purposes, **no advance deduction (*Vorwegabzug*) for the commercial units is required** when allocating property tax (**BGH VIII ZR 79/16, Leitsatz**).
> * An advance deduction for commercial use is generally only required if the commercial operation causes significant additional costs per square metre. However, property tax is an asset-based tax assessed uniformly by the municipality on the property as a whole, rather than on the current annual yields or tenant conduct (**BGH VIII ZR 79/16, Rn. 20–22, Rn. 23–25**). 
> * Unless your lease agreements explicitly stipulate a separate accounting or advance deduction for the commercial unit, the property tax is allocated across both the residential and commercial areas together (**BGH VIII ZR 79/16, Rn. 8, 14–19**).
>
> ---
>
> ### 3. Flats Bigger than the Lease States: Which Area Applies?
> **The actual area (*tatsächliche Wohnfläche*) must be used:**
>
> * Under **§ 556a Abs. 1 BGB**, unless the parties have agreed otherwise, operating costs are allocated according to the proportion of living area (*Wohnfläche*).
> * If costs are apportioned by area, the relevant measure is the **actual living area (*tatsächliche Wohnfläche*)** of the individual unit in relation to the total actual area (*tatsächlich vorhandene Gesamtwohnfläche*) of the building, **not** the area stated in the lease contract (**BGH VIII ZR 220/17, Leitsatz**).
> * Contractual area specifications or subjective assumptions in individual leases cannot serve as an objective allocation key. The BGH has explicitly abandoned its former rule that deviations between agreed and actual area of up to 10% could be disregarded; the calculation must strictly reflect the objective, actual floor areas (**BGH VIII ZR 220/17, Rn. 18–23**).
>
> ---
>
> ### Summary of How to Allocate:
> 1. Ensure the leases contain a valid clause passing on operating costs (*Betriebskosten*).
> 2. Take the total property tax assessed for the entire property (no advance deduction for the shop needed).
> 3. Distribute the total tax based on the ratio of each unit’s **actual floor area** to the **total actual floor area** of the building (commercial plus residential).

**Cited passages:**

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>§ 2 Nr. 1–5 BetrKV</summary>

Betriebskosten im Sinne von § 1 sind:
1. die laufenden öffentlichen Lasten des Grundstücks,
hierzu gehört namentlich die Grundsteuer;
2. die Kosten der Wasserversorgung,
hierzu gehören die Kosten des Wasserverbrauchs, die Grundgebühren, die Kosten der Anmietung oder anderer Arten der Gebrauchsüberlassung von Wasserzählern sowie die Kosten ihrer Verwendung einschließlich der Kosten der Eichung sowie der Kosten der Berechnung und Aufteilung, die Kosten der Wartung von Wassermengenreglern, die Kosten des Betriebs einer hauseigenen Wasserversorgungsanlage und einer Wasseraufbereitungsanlage einschließlich der Aufbereitungsstoffe;
3. die Kosten der Entwässerung,
hierzu gehören die Gebühren für die Haus- und Grundstücksentwässerung, die Kosten des Betriebs einer entsprechenden nicht öffentlichen Anlage und die Kosten des Betriebs einer Entwässerungspumpe;
4. die Kosten
a) des Betriebs der zentralen Heizungsanlage einschließlich der Abgasanlage,
hierzu gehören die Kosten des zur Wärmeerzeugung verbrauchten Stroms und der verbrauchten Brennstoffe und ihrer Lieferung, die Kosten des Betriebsstroms, die Kosten der Bedienung, Überwachung und Pflege der Anlage, der regelmäßigen Prüfung ihrer Betriebsbereitschaft und Betriebssicherheit einschließlich der Einstellung durch eine Fachkraft, der Reinigung der Anlage und des Betriebsraums, die Kosten der Messungen nach dem Bundes-Immissionsschutzgesetz, die Kosten der Anmietung oder anderer Arten der Gebrauchsüberlassung einer Ausstattung zur Verbrauchserfassung sowie die Kosten der Verwendung einer Ausstattung zur Verbrauchserfassung einschließlich der Kosten der Eichung sowie der Kosten der Berechnung und Aufteilung
oder
b) des Betriebs der zentralen Brennstoffversorgungsanlage,
hierzu gehören die Kosten der verbrauchten Brennstoffe und ihrer Lieferung, die Kosten des Betriebsstroms und die Kosten der Überwachung sowie die Kosten der Reinigung der Anlage und des Betriebsraums
oder
c) der eigenständig gewerblichen Lieferung von Wärme, auch aus Anlagen im Sinne des Buchstabens a,
hierzu gehören das Entgelt für die Wärmelieferung und die Kosten des Betriebs der zugehörigen Hausanlagen entsprechend Buchstabe a
oder
d) der Reinigung und Wartung von Etagenheizungen und Gaseinzelfeuerstätten,
hierzu gehören die Kosten der Beseitigung von Wasserablagerungen und Verbrennungsrückständen in der Anlage, die Kosten der regelmäßigen Prüfung der Betriebsbereitschaft und Betriebssicherheit und der damit zusammenhängenden Einstellung durch eine Fachkraft sowie die Kosten der Messungen nach dem Bundes-Immissionsschutzgesetz;
5. die Kosten
a) des Betriebs der zentralen Warmwasserversorgungsanlage,
hierzu gehören die Kosten der Wasserversorgung entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind, und die Kosten der Wassererwärmung entsprechend Nummer 4 Buchstabe a
oder
b) der eigenständig gewerblichen Lieferung von Warmwasser, auch aus Anlagen im Sinne des Buchstabens a,

</details>

<details><summary>BGH VIII ZR 79/16, Leitsatz</summary>

Bei der Betriebskostenabrechnung für ein teils gewerblich und teils zu Wohnzwecken genutztes Grundstück bedarf es bezüglich der Umlage der Grundsteuer keines Vorwegabzugs für die gewerblich genutzten Einheiten.

</details>

<details><summary>BGH VIII ZR 79/16, Rn. 20–22</summary>

a) Nach der gefestigten Rechtsprechung des Senats ist ein Vorwegabzug aus Billigkeitsgründen gemäß §§ 315, 316 BGB (hierzu Senatsurteile vom 8. März 2006 - VIII ZR 78/05, aaO Rn. 16; vom 25. Oktober 2006 - VIII ZR 251/05, aaO) (nur) dann erforderlich, wenn - wofür der Mieter die Darlegungs- und Beweislast trägt - durch die gewerbliche Nutzung erhebliche Mehrkosten (pro Quadratmeter) entstehen (Senatsurteile vom 11. August 2010 - VIII ZR 45/10, NJW 2010, 3363 Rn. 22; vom 13. Oktober 2010 - VIII ZR 46/10, NZM 2011, 118 Rn. 21 f.; vom 8. März 2006 - VIII ZR 78/05, aaO Rn. 31 und Ls 1; vom 25. Oktober 2006 - VIII ZR 251/05, aaO Rn. 15 f.).
b) Gemessen an diesem Maßstab hat das Berufungsgericht die Notwendigkeit eines Vorwegabzugs bei der Grundsteuer rechtsfehlerfrei verneint.
Wie bereits das Amtsgericht zutreffend ausgeführt hat, handelt es sich bei der Grundsteuer um eine ertragsunabhängige Objektsteuer, das heißt, die in einem Abrechnungsjahr erhobene Steuer hängt grundsätzlich nicht von den in diesem Jahr erzielten Erträgen und ihrer Verteilung auf die Nutzung zu gewerblichen Zwecken einerseits und zu Wohnzwecken andererseits ab. Vielmehr wird die Grundsteuer auf der Basis der vom örtlichen Finanzamt erlassenen Bescheide über den Einheitswert (hier: 110.600 DM bzw. 56.548 €) und den Grundsteuermessbetrag (hier: 565,48 €, errechnet im Wege der Multiplikation des Einheitswertes mit der Steuermesszahl 10 vom Tausend) sowie des von der Gemeinde durch Satzungsbeschluss festgelegten Hebesatzes (in Berlin Multiplikator 8,1 [810 %]) ermittelt.

</details>

<details><summary>BGH VIII ZR 79/16, Rn. 8, 14–19</summary>

Die Revision hat keinen Erfolg.
Diese Beurteilung hält rechtlicher Nachprüfung stand, so dass die Revision zurückzuweisen ist.
Zu Recht hat das Berufungsgericht einen Anspruch der Kläger gemäß § 812 Abs. 1 Satz 1 Alt. 1 BGB auf Auszahlung eines Betriebskostenguthabens in Höhe eines anteiligen Grundsteuerbetrags von 209,31 € verneint. Die von der Beklagten vorgenommene Umlage der Grundsteuer in der Betriebskostenabrechnung für das Jahr 2013 ist aus Rechtsgründen nicht zu beanstanden; insbesondere bedurfte es keines Vorwegabzugs für die gewerblich genutzten Einheiten.
1. Entgegen der Auffassung der Revision enthält der Mietvertrag keine Vereinbarung über eine getrennte Abrechnung der auf die gewerblichen Einheiten entfallenden Betriebskosten (sogenannter Vorwegabzug). Mit der Umlage der Betriebskosten "nach dem Verhältnis der Wohn- und Nutzflächen des Hauses" (§ 3 Nr. 4 des Formular-Mietvertrags) wird lediglich geregelt, dass die Betriebskosten - insgesamt - nach dem Flächenmaßstab zu verteilen sind. Die Frage eines Vorwegabzugs wird in der Klausel nicht einmal erwähnt.
Ohne Erfolg macht die Revision in diesem Zusammenhang geltend, die Mietvertragsparteien hätten - wie die Abrechnungspraxis der ursprünglichen Vermieterin zeige - die genannte Klausel übereinstimmend dahin verstanden, dass der Vermieter einen Vorwegabzug für die gewerblich genutzten Einheiten vornehmen müsse. Unabhängig davon, ob es sich dabei um neuen, in der Revisionsinstanz unbeachtlichen Tatsachenvortrag handelt, lässt die bloße Abrechnungsweise der Rechtsvorgängerin einen derartigen Schluss nicht zu.
2. Auch aus § 556a Abs. 1 Satz 2 BGB lässt sich, wie das Berufungsgericht richtig gesehen hat, nichts für eine Notwendigkeit des von den Klägern geforderten Vorwegabzugs bei der Grundsteuer herleiten. Nach dieser Vorschrift sind Betriebskosten, die von einem erfassten Verbrauch oder von einer erfassten Verursachung durch die Mieter abhängen, nach einem Maßstab umzulegen, der dem unterschiedlichen Verbrauch oder der unterschiedlichen Verursachung Rechnung trägt. Eine erfasste unterschiedliche Verursachung im Sinne dieser Vorschrift scheidet jedoch von vornherein aus, weil die Grundsteuer auf einer einheitlichen Festsetzung durch die Gemeinde beruht und nicht von einem Verhalten der Mieter abhängt. Zudem ergibt sich aus dieser Vorschrift - wie der Senat schon entschieden hat - keine Verpflichtung zu einem Vorwegabzug der auf die gewerblichen Mieter entfallenden Betriebskosten (Senatsurteile vom 8. März 2006 - VIII ZR 78/05, NJW 2006, 1419 Rn. 30; vom 25. Oktober 2006 - VIII ZR 251/05, NJW 2007, 211 Rn. 16).
3. Auch aus Billigkeitsgründen ist der Vermieter nicht zu einem Vorwegabzug für die Gewerbeeinheiten bei der Grundsteuer verpflichtet.

</details>

<details><summary>§§ 556a–556c BGB</summary>

(1) Haben die Vertragsparteien nichts anderes vereinbart, sind die Betriebskosten vorbehaltlich anderweitiger Vorschriften nach dem Anteil der Wohnfläche umzulegen. Betriebskosten, die von einem erfassten Verbrauch oder einer erfassten Verursachung durch die Mieter abhängen, sind nach einem Maßstab umzulegen, der dem unterschiedlichen Verbrauch oder der unterschiedlichen Verursachung Rechnung trägt.
(2) Haben die Vertragsparteien etwas anderes vereinbart, kann der Vermieter durch Erklärung in Textform bestimmen, dass die Betriebskosten zukünftig abweichend von der getroffenen Vereinbarung ganz oder teilweise nach einem Maßstab umgelegt werden dürfen, der dem erfassten unterschiedlichen Verbrauch oder der erfassten unterschiedlichen Verursachung Rechnung trägt. Die Erklärung ist nur vor Beginn eines Abrechnungszeitraums zulässig. Sind die Kosten bislang in der Miete enthalten, so ist diese entsprechend herabzusetzen.
(3) Ist Wohnungseigentum vermietet und haben die Vertragsparteien nichts anderes vereinbart, sind die Betriebskosten abweichend von Absatz 1 nach dem für die Verteilung zwischen den Wohnungseigentümern jeweils geltenden Maßstab umzulegen. Widerspricht der Maßstab billigem Ermessen, ist nach Absatz 1 umzulegen.
(4) Eine zum Nachteil des Mieters von Absatz 2 abweichende Vereinbarung ist unwirksam.
(1) Die Miete ist zu Beginn, spätestens bis zum dritten Werktag der einzelnen Zeitabschnitte zu entrichten, nach denen sie bemessen ist.
(2) Der Mieter kann entgegen einer vertraglichen Bestimmung gegen eine Mietforderung mit einer Forderung auf Grund der §§ 536a, 539 oder aus ungerechtfertigter Bereicherung wegen zu viel gezahlter Miete aufrechnen oder wegen einer solchen Forderung ein Zurückbehaltungsrecht ausüben, wenn er seine Absicht dem Vermieter mindestens einen Monat vor der Fälligkeit der Miete in Textform angezeigt hat. Eine zum Nachteil des Mieters abweichende Vereinbarung ist unwirksam.
(1) Hat der Mieter die Betriebskosten für Wärme oder Warmwasser zu tragen und stellt der Vermieter die Versorgung von der Eigenversorgung auf die eigenständig gewerbliche Lieferung durch einen Wärmelieferanten (Wärmelieferung) um, so hat der Mieter die Kosten der Wärmelieferung als Betriebskosten zu tragen, wenn
1. die Wärme mit verbesserter Effizienz entweder aus einer vom Wärmelieferanten errichteten neuen Anlage oder aus einem Wärmenetz geliefert wird und
2. die Kosten der Wärmelieferung die Betriebskosten für die bisherige Eigenversorgung mit Wärme oder Warmwasser nicht übersteigen.
Beträgt der Jahresnutzungsgrad der bestehenden Anlage vor der Umstellung mindestens 80 Prozent, kann sich der Wärmelieferant anstelle der Maßnahmen nach Nummer 1 auf die Verbesserung der Betriebsführung der Anlage beschränken.
(2) Der Vermieter hat die Umstellung spätestens drei Monate zuvor in Textform anzukündigen (Umstellungsankündigung).
(3) Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften für Wärmelieferverträge, die bei einer Umstellung nach Absatz 1 geschlossen werden, sowie für die Anforderungen nach den Absätzen 1 und 2 zu erlassen. Hierbei sind die Belange von Vermietern, Mietern und Wärmelieferanten angemessen zu berücksichtigen.
(4) Eine zum Nachteil des Mieters abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>BGH VIII ZR 220/17, Leitsatz</summary>

Sofern und soweit Betriebskosten nach gesetzlichen Vorgaben (vgl. etwa § 556a Abs. 1 BGB, § 7 Abs. 1 HeizkostenV) ganz oder teilweise nach Wohnflächenanteilen umgelegt werden, ist für die Abrechnung im Allgemeinen der jeweilige Anteil der tatsächlichen Wohnfläche der betroffenen Wohnung an der in der Wirtschaftseinheit tatsächlich vorhandenen Gesamtwohnfläche maßgebend (insoweit Aufgabe von BGH, Urteil vom 31. Oktober 2007, VIII ZR 261/06, NJW 2008, 142 Rn. 19).

</details>

---

## q31 (multi)

**Question:** Our lease only says the tenant pays “die Betriebskosten”. Does that cover the waste-sorting service we hired?

**Your reference answer:** Yes. "Die Betriebskosten" covers all operating costs in § 2 Nr. 1–16 BetrKV; "other operating costs" (Nr. 17) must be named in the lease (BGH VIII ZR 137/15, Rn. 11), and the waste-sorting service counts as waste disposal under § 2 Nr. 8 BetrKV (BGH VIII ZR 117/21, LS 1).

**Agent's answer:**

> **Yes**, agreeing in a residential lease that the tenant simply bears “die Betriebskosten” covers the costs of an external waste-sorting service.
>
> ### 1. Sufficiency of the lease clause
> In residential tenancy, an agreement—even in standard form—stating simply that the tenant has to bear “die Betriebskosten” is legally sufficient to pass on the operating costs defined in the law and detailed in the Operating Costs Ordinance (*Betriebskostenverordnung* – BetrKV) (**BGH VIII ZR 137/15, Leitsatz**). It is not necessary to attach the operating cost catalog or to make an explicit reference to the statute or the BetrKV (**BGH VIII ZR 137/15, Leitsatz**).
>
> ### 2. Classification of waste-sorting costs
> * The costs of an external service provider for regularly checking residual waste containers to ensure compliance with municipal waste-separation regulations and for subsequent manual re-sorting (*Nachsortierung von Hand*) in case of incorrect separation are chargeable to the tenant as waste disposal costs (*Kosten der Müllbeseitigung*) (**BGH VIII ZR 117/21, Leitsatz**; **BGH VIII ZR 230/21, Rn. 23–26**).
> * Because these manual sorting costs serve to prepare waste disposal and are categorized directly as waste disposal costs rather than "other operating costs" (*sonstige Betriebskosten*), they do not need to be individually specified in the lease agreement (**BGH VIII ZR 117/21, Rn. 27–30**; **BGH VIII ZR 230/21, Rn. 23–26**). 
> * Such costs are covered by the transfer clause even if the service was hired long after the lease began (**BGH VIII ZR 117/21, Rn. 27–30**).
>
> ### 3. Limitation: Principle of economic efficiency
> When hiring an external waste management service, the landlord has a contractual duty to respect the principle of economic efficiency (*Wirtschaftlichkeitsgebot*) by maintaining a reasonable cost-benefit ratio (*Kosten-Nutzen-Verhältnis*) (**BGH VIII ZR 230/21, Rn. 23–26**).

**Cited passages:**

<details><summary>BGH VIII ZR 137/15, Leitsatz</summary>

In der Wohnraummiete genügt zur Übertragung der Betriebskosten auf den Mieter die - auch formularmäßige - Vereinbarung, dass dieser "die Betriebskosten" zu tragen hat. Auch ohne Beifügung des Betriebskostenkatalogs oder ausdrückliche Bezugnahme auf § 556 Abs. 1 Satz 2 BGB und die Betriebskostenverordnung vom 25. November 2003 (BGBl. I. S. 2347) ist damit die Umlage der in § 556 Abs. 1 Satz 2 BGB definierten und in der Betriebskostenverordnung erläuterten Betriebskosten vereinbart.

</details>

<details><summary>BGH VIII ZR 117/21, Leitsatz</summary>

1. Die Kosten eines externen Dienstleisters für die regelmäßige Kontrolle der Restmüllbehälter des Mietobjekts auf Einhaltung der satzungsmäßigen Vorgaben für die Mülltrennung und für die bei fehlerhafter Abfalltrennung erfolgende Nachsortierung von Hand sind im Wohnraummietverhältnis gemäß § 2 Nr. 8 BetrKV auf den Mieter umlegbare Betriebskosten.
2. Die Kosten für die regelmäßige Prüfung und Sicherstellung der Betriebsbereitschaft von in den Mieträumen angebrachten Rauchwarnmeldern sind im Wohnraummietverhältnis als "sonstige Betriebskosten" im Sinne von § 2 Nr. 17 BetrKV auf den Mieter umlegbar. Sie werden von einer vertraglichen Umlagevereinbarung erfasst, welche die Umlage der Kosten des Betriebs von Brandschutz- und Brandmeldeanlagen auf den Mieter vorsieht.
Dem stehen Regelungen in den Bauordnungen der Länder (hier: § 48 Abs. 4 Satz 4 BauO Bln), nach denen (öffentlich-rechtlich) die Wartung dem Mieter obliegt, nicht entgegen.

</details>

<details><summary>BGH VIII ZR 230/21, Rn. 23–26</summary>

2. Mit der von dem Berufungsgericht bisher gegebenen Begründung kann ein Schadensersatzanspruch der Kläger zu 1, 2, 4 und 5 gegen die Beklagte gemäß § 280 Abs. 1 BGB in Verbindung mit § 241 Abs. 2 BGB auf Rückzahlung der aus der Beauftragung der externen Dienstleisterin mit dem Müllmanagement resultierenden Betriebskosten für die Jahre 2016 bis 2018 nicht bejaht werden. Das Berufungsgericht hat den Inhalt der vertraglichen Nebenpflicht des Vermieters, auf ein angemessenes Kosten-Nutzen-Verhältnis bei den Betriebskosten Rücksicht zu nehmen, verkannt. In diesem Zusammenhang hat es überdies eine unzutreffende Verteilung der Darlegungs- und Beweislast zwischen Mieter und Vermieter angenommen.
a) Das Berufungsgericht ist zunächst - unausgesprochen und von den Parteien nicht angegriffen - rechtsfehlerfrei davon ausgegangen, dass die Beklagte nach den zwischen den Parteien getroffenen Vereinbarungen die im Streit stehenden Kosten für das Müllmanagement grundsätzlich als Betriebskosten gemäß § 556 Abs. 1 Satz 1 BGB und dem Betriebskostenkatalog gemäß der dazu erlassenen Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346; im Folgenden: BetrKV) auf die Kläger umlegen kann.
aa) Die Kosten für den Betrieb der chipgesteuerten Müllschleusenanlage als Müllmengenerfassungsanlage und der durch die wiederkehrende Beseitigung von (zu entsorgenden) Beistellungen der Mieter oder Dritter ausgelöste Aufwand sind als Kosten der Müllbeseitigung im Sinne von § 2 Nr. 8 BetrKV dem Grunde nach auf die Kläger umlegbar (vgl. Senatsurteile vom 10. Februar 2016 - VIII ZR 33/15, WuM 2016, 214 Rn. 15; vom 13. Januar 2010 - VIII ZR 137/09, WuM 2010, 153 Rn. 24). Auch die Kosten der Nachsortierung des Abfalls werden als der Vorbereitung der Müllbeseitigung dienende Kosten von § 2 Nr. 8 BetrKV umfasst (vgl. hierzu ausführlich Senatsurteil vom 5. Oktober 2022 - VIII ZR 117/21, NJW-RR 2022, 1593 Rn. 28 ff.; vgl. auch Langenberg/Zehelein, Betriebs- und Heizkostenrecht, 10. Aufl., Teil H Rn. 76; Wall, Betriebs- und Heizkosten-Kommentar, 5. Aufl., Rn. 3879).
bb) Die Kosten für die von der externen Dienstleisterin darüber hinaus vorgenommene Reinigung der Mülltonnenstandplätze sind ebenfalls umlagefähig, wobei dahingestellt bleiben kann, ob es sich hierbei um Kosten nach § 2 Nr. 9 oder Nr. 10 BetrKV handelt (vgl. Langenberg/Zehelein, aaO; Wall, aaO).

</details>

<details><summary>BGH VIII ZR 117/21, Rn. 27–30</summary>

Auch der Einwand der Revision, das vom Berufungsgericht angeführte gesamtgesellschaftliche Interesse an einer optimalen Trennung und Wiederverwertung des Mülls könne einen "Bezug zum einzelnen Mietvertrag" nicht begründen, geht bereits deshalb fehl, weil die Einordnung von Kosten als Betriebskosten nach § 556 Abs. 1 Satz 2 BGB, § 1 Abs. 1 Satz 1 BetrKV einen solchen individuellen Bezug zum Mieter nicht verlangt. Maßgeblich ist vielmehr, dass es sich - wie hier - um Kosten handelt, die durch die Bewirtschaftung des betreffenden Grundstücks im Rahmen der Vermietung entstehen (vgl. hierzu BeckOGK-BGB/Drager, Stand: 1. Juli 2021, § 556 Rn. 65; MünchKomm-BGB/Zehelein, 8. Aufl., § 1 BetrKV Rn. 16; Wall, Betriebs- und Heizkosten-Kommentar, 5. Aufl., Rn. 2905).
cc) Mit Recht hat das Berufungsgericht angenommen, dass die von der Beklagten angesetzten Kosten eines externen Dienstleisters für die Kontrolle der Restmüllbehälter der Liegenschaft auf Einhaltung der satzungsmäßigen Vorgaben für die Mülltrennung und für die bei fehlerhafter Abfalltrennung erfolgende Nachsortierung von Hand - von Anfang an - als "Kosten der Müllbeseitigung" wirksam auf die Kläger umgelegt wurden.
(1) Gemäß § 535 Abs. 1 Satz 3, § 556 Abs. 1, 4 BGB hat der Mieter Betriebskosten zu tragen, wenn die Parteien eine entsprechende Vereinbarung wirksam getroffen haben. Grundsätzlich genügt dafür - wie hier im Mietvertrag enthalten und soweit es nicht um "sonstige" Betriebskosten im Sinne von § 2 Nr. 17 BetrKV geht - eine Verweisung auf die Betriebskostenverordnung (st. Rspr.; vgl. nur Senatsurteile vom 10. Februar 2016 - VIII ZR 137/15, NZM 2016, 235 Rn. 11; vom 18. Dezember 2019 - VIII ZR 62/19, NZM 2020, 457 Rn. 10; jeweils mwN).
(2) Der zwischen den Parteien geschlossene Mietvertrag sieht über die Bezugnahme auf Anlage 4 des Mietvertrags mit einer beispielhaften Auflistung der umlegbaren Betriebskosten und über die zudem enthaltene allgemeine Verweisung auf "alle Betriebskosten" im Sinne von § 2 BetrKV auch eine Umlage von "Kosten der Müllbeseitigung" auf die Kläger vor (Nr. 1 Buchst. f der Anlage 4 des Mietvertrags; § 2 Nr. 8 BetrKV). Diese wirksam getroffene Umlagevereinbarung umfasst - wie das Berufungsgericht zutreffend gewürdigt hat - die in Rede stehenden Kosten unabhängig davon, dass diese erstmals längere Zeit nach dem Vertragsschluss angefallen sind.

</details>

---

## q32 (multi)

**Question:** Half our building is empty, and the boiler has no heat meter for the hot water. How should I bill the remaining tenants for hot water?

**Your reference answer:** Without a heat meter on the central system, the billing counts as not consumption-based and the tenant can cut his share by 15% (§ 12 HeizkostenV; BGH VIII ZR 151/20). Vacancy alone doesn't let you drop consumption-based billing, but the landlord may in individual cases have to agree to the tenant's request to lower the consumption share to the legal minimum of 50% (9/14, Rn. 24), and the claim can be capped under § 242 BGB (BGH VIII ZR 9/14).

**Agent's answer:**

> To bill the remaining tenants for hot water when the building has a combined heating and hot water boiler, a 50% vacancy rate, and no heat meter for hot water, you must follow the provisions of the Heating Costs Ordinance (*Heizkostenverordnung* – HeizkostenV) and the relevant decisions of the Federal Court of Justice (*Bundesgerichtshof* – BGH).
>
> The answer depends on several key facts:
>
> ---
>
> ### 1. Underlying Prerequisite: Lease Clause (*Umlagevereinbarung*)
> Operating costs (*Betriebskosten*), including hot water and heating, can only be charged to tenants if the lease agreement contains an agreement transferring them to the tenant (§ 556 Abs. 1 BGB). In residential leases, an agreement—including in standard terms—stating that the tenant bears "the operating costs" (*die Betriebskosten*) is sufficient to transfer all statutory operating costs without listing them individually (BGH VIII ZR 137/15, Leitsatz).
>
> ---
>
> ### 2. Splitting the Boiler Costs Without a Heat Meter (§ 9 HeizkostenV)
> Where a central heating boiler supplies both space heating and hot water (*verbundene Anlage*), the jointly incurred operating costs must be split (§ 9 Abs. 1–2 HeizkostenV):
>
> * **Requirement for a heat meter:** Under § 9 Abs. 1–2 HeizkostenV, the heat quantity (*Wärmemenge*, $Q$) consumed by the central hot water system must be measured with a heat meter (*Wärmezähler*).
> * **Formula in case of disproportionate expense:** If measuring the heat quantity is only possible at an unreasonably high expense (*unzumutbar hoher Aufwand*), § 9 Abs. 1–2 HeizkostenV permits calculating the heat quantity using the statutory formula:
>   $$Q = 2.5 \times V \times (t_w - 10)$$
>   where $V$ is the measured volume of consumed hot water in cubic meters (via apartment water meters), and $t_w$ is the average hot water temperature in °C.
> * **Area formula strictly limited:** § 9 Abs. 1–2 HeizkostenV allows determining the heat quantity based on living space ($Q = 32 \times A_{\text{Wohn}}$) only in exceptional cases where *neither* the heat quantity nor the consumed hot water volume can be measured. If individual hot water meters exist in the apartments so that the volume ($V$) can be measured, the area-based calculation formula may not be used (BGH VIII ZR 151/20, Rn. 28–30).
> * **Fuel consumption calculation:** For boiler systems (*Heizkessel*), the corresponding fuel consumption (*Brennstoffverbrauch*, $B$) allocated to hot water is determined by the equation $B = Q / H_i$ using the fuel's calorific value ($H_i$) (§ 9 Abs. 3–4 HeizkostenV).
>
> #### Risk: 15% Reduction Right of the Tenants (*Kürzungsrecht*)
> If the combined system lacks the required heat meter and the statutory exceptions for substitute formulas do not apply, the billing is legally deemed non-consumption-based (*nicht verbrauchsabhängig*), even if the apartments have individual hot water meters (BGH VIII ZR 151/20, Leitsatz). Under § 12 HeizkostenV, the tenant is entitled to reduce their billed share of heating and hot water costs by **15%** (BGH VIII ZR 151/20, Rn. 28–30).
>
> ---
>
> ### 3. Allocation of Hot Water Costs to Tenants (§§ 7–8 HeizkostenV)
> Once the total hot water cost share is separated from the heating costs, it must be distributed among the units under §§ 7–8 HeizkostenV:
> * **50% to 70%** based on recorded individual hot water consumption (*erfasster Warmwasserverbrauch*).
> * The remaining **30% to 50%** based on living or usable floor area (*Wohn- oder Nutzfläche*).
>
> ---
>
> ### 4. Impact of the 50% Vacancy (*Leerstand*)
> The Federal Court of Justice has established clear rules for handling high vacancy rates:
>
> * **Consumption-based billing remains mandatory:** Even in cases of high apartment vacancies, hot water costs must fundamentally still be allocated partly by consumption and partly by area pursuant to §§ 7–8 HeizkostenV and § 9 Abs. 3–4 HeizkostenV (BGH VIII ZR 9/14, Leitsatz).
> * **The landlord bears the vacancy share:** Where costs are allocated by floor area, the calculation must be based on the total actual living area of the property (BGH VIII ZR 220/17, Leitsatz). The landlord must bear the fixed costs for the vacant apartments (the 50% empty space) and cannot distribute those costs onto the remaining tenants (BGH VIII ZR 9/14, Rn. 29–31).
> * **Adjustments to prevent unfair hardship:** High vacancies cause circulation and distribution heat losses to fall heavily on the few remaining users. According to BGH VIII ZR 9/14, Leitsatz:
>   * In individual cases, the landlord can be obliged to agree to reduce the consumption-based portion to the statutory minimum of **50%** of total costs to distribute the fixed loss costs appropriately.
>   * In specific individual cases where vacancy shifts cause an unreasonable burden on the tenant, a limitation of the landlord's claim can be derived from the principle of good faith (*Treu und Glauben*), taking into account that the landlord also suffers considerable disadvantages by bearing the vacant floor area's costs (BGH VIII ZR 9/14, Leitsatz and Rn. 29–31).
>
> ---
>
> *If you are uncertain whether your lack of a heat meter meets the strict high-expense exception of § 9 Abs. 1–2 HeizkostenV, or whether your tenants qualify for a good-faith cost reduction due to the vacancy, you should consult a tenancy lawyer (*Fachanwalt für Miet- und Wohnungseigentumsrecht*).*

**Cited passages:**

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>BGH VIII ZR 137/15, Leitsatz</summary>

In der Wohnraummiete genügt zur Übertragung der Betriebskosten auf den Mieter die - auch formularmäßige - Vereinbarung, dass dieser "die Betriebskosten" zu tragen hat. Auch ohne Beifügung des Betriebskostenkatalogs oder ausdrückliche Bezugnahme auf § 556 Abs. 1 Satz 2 BGB und die Betriebskostenverordnung vom 25. November 2003 (BGBl. I. S. 2347) ist damit die Umlage der in § 556 Abs. 1 Satz 2 BGB definierten und in der Betriebskostenverordnung erläuterten Betriebskosten vereinbart.

</details>

<details><summary>§ 9 Abs. 1–2 HeizkostenV</summary>

(1) Ist die zentrale Anlage zur Versorgung mit Wärme mit der zentralen Warmwasserversorgungsanlage verbunden, so sind die einheitlich entstandenen Kosten des Betriebs aufzuteilen. Die Anteile an den einheitlich entstandenen Kosten sind bei Anlagen mit Heizkesseln nach den Anteilen am Brennstoffverbrauch oder am Energieverbrauch, bei Wärmepumpen oder und bei eigenständiger gewerblicher Wärmelieferung nach den Anteilen am Wärmeverbrauch zu bestimmen. Kosten, die nicht einheitlich entstanden sind, sind dem Anteil an den einheitlich entstandenen Kosten hinzuzurechnen. Der Anteil der zentralen Anlage zur Versorgung mit Wärme ergibt sich aus dem gesamten Verbrauch nach Abzug des Verbrauchs der zentralen Warmwasserversorgungsanlage. Bei Anlagen, die nicht ausschließlich durch Heizkessel, durch Wärmepumpen oder durch eigenständige gewerbliche Wärmelieferung mit Wärme versorgt werden, können anerkannte Regeln der Technik zur Aufteilung der Kosten verwendet werden. Der Anteil der zentralen Warmwasserversorgungsanlage am Wärmeverbrauch ist nach Absatz 2, der Anteil am Brennstoffverbrauch nach Absatz 3 zu ermitteln.
(2) Die auf die zentrale Warmwasserversorgungsanlage entfallende Wärmemenge (Q) ist mit einem Wärmezähler zu messen. Kann die Wärmemenge nur mit einem unzumutbar hohen Aufwand gemessen werden, kann sie nach folgender Zahlenwertgleichung als Ergebnis in Kilowattstunden pro Jahr bestimmt werden:
Q = 2,5 x V x (tw-10).
Dabei sind zu Grunde zu legen:
1. der Wert 2,5 für die Erzeugeraufwandszahl des Wärmeerzeugers, die mittlere spezifische Wärmekapazität des Wassers, die Wärmeverluste für Warmwasserspeicher, Verteilung einschließlich Zirkulation, Messdatenerhebungen zum Warmwasserverbrauch,
2. das gemessene Volumen des verbrauchten Warmwassers (V) in Kubikmetern,
3. die gemessene oder geschätzte mittlere Temperatur des Warmwassers (tw) in Grad Celsius und
4. der Wert 10 für die übliche Kaltwassereintrittstemperatur in die Warmwasserversorgungsanlage in Grad Celsius.
Wenn in Ausnahmefällen weder die Wärmemenge noch das Volumen des verbrauchten Warmwassers gemessen werden können, kann die Wärmemenge, die auf die zentrale Warmwasserversorgungsanlage entfällt, nach folgender Zahlenwertgleichung als Ergebnis in Kilowattstunden pro Jahr bestimmt werden:
Q = 32 x AWohn.
Dabei sind zu Grunde zu legen:
1. der Wert 32 für den Nutzwärmebedarf für Warmwasser, die Erzeugeraufwandszahl des Wärmeerzeugers, Messdatenerhebungen zum Warmwasserverbrauch und
2. die durch die zentrale Anlage mit Warmwasser versorgte Wohn- oder Nutzfläche (AWohn) in Quadratmeter.
Die nach den Zahlenwertgleichungen in Satz 2 oder 4 bestimmte Wärmemenge (Q) ist
1. bei brennwertbezogener Abrechnung von Erdgas mit 1,11 zu multiplizieren,
2. bei eigenständiger gewerblicher Wärmelieferung durch 1,15 zu dividieren und
3. bei dem Betrieb einer monovalenten Wärmepumpe mit 0,30 zu multiplizieren.

</details>

<details><summary>§ 9 Abs. 3–4 HeizkostenV</summary>

(3) Bei Anlagen mit Heizkesseln ist der Brennstoffverbrauch der zentralen Warmwasserversorgungsanlage (B) in Litern, Kubikmetern oder Kilogramm nach folgender Gleichung zu bestimmen:
B = Q / Hi [Formel aus Bild übertragen] .
Dabei sind zu Grunde zu legen
1. die auf die zentrale Warmwasserversorgungsanlage entfallende Wärmemenge (Q) nach Absatz 2 in kWh;
2. der Heizwert des verbrauchten Brennstoffes (Hi) in Kilowattstunden je Liter, Kubikmeter oder Kilogramm.
Als Heizwerte nach Satz 2 Nummer 2 sind die in den Abrechnungsunterlagen des Energieversorgungsunternehmens oder Brennstofflieferanten angegebenen Heizwerte zu verwenden. Wenn diese vom Energieversorgungsunternehmen oder Brennstofflieferanten nicht angegeben werden, können hilfsweise folgende Werte verwendet werden:
| Heiz- wert Hi | Einheit
Leichtes Heizöl extra leichtflüssig | 10 | Kilowattstunden je Liter
Schweres Heizöl | 10,9 | Kilowattstunden je Liter
Erdgas H | 10 | Kilowattstunden je Kubikmeter
Erdgas L | 9 | Kilowattstunden je Kubikmeter
Flüssiggas | 13 | Kilowattstunden je Kilogramm
Koks | 8 | Kilowattstunden je Kilogramm
Braunkohle | 5,5 | Kilowattstunden je Kilogramm
Steinkohle | 8 | Kilowattstunden je Kilogramm
Brennholz (lufttrocken) | 4,1 | Kilowattstunden je Kilogramm
Holzpellets | 5 | Kilowattstunden je Kilogramm
Holzhackschnitzel (lufttrocken) | 4 | Kilowattstunden je Kilogramm
Soweit die Abrechnung über Kilowattstunden-Werte erfolgt, ist eine Umrechnung in Brennstoffverbrauch nicht erforderlich. Als Hi-Werte können verwendet werden für
Leichtes Heizöl EL | 10 | kWh/l
Schweres Heizöl | 10,9 | kWh/l
Erdgas H | 10 | kWh/m3
Erdgas L | 9 | kWh/m3
Flüssiggas | 13 | kWh/kg
Koks | 8 | kWh/kg
Braunkohle | 5,5 | kWh/kg
Steinkohle | 8 | kWh/kg
Holz (lufttrocken) | 4,1 | kWh/kg
Holzpellets | 5 | kWh/kg
Holzhackschnitzel | 650 | kWh/SRm.
Enthalten die Abrechnungsunterlagen des Energieversorgungsunternehmens oder Brennstofflieferanten Hi-Werte, so sind diese zu verwenden. Soweit die Abrechnung über kWh-Werte erfolgt, ist eine Umrechnung in Brennstoffverbrauch nicht erforderlich.
(4) Der Anteil an den Kosten der Versorgung mit Wärme ist nach § 7 Absatz 1, der Anteil an den Kosten der Versorgung mit Warmwasser nach § 8 Absatz 1 zu verteilen, soweit diese Verordnung nichts anderes bestimmt oder zulässt.

</details>

<details><summary>BGH VIII ZR 151/20, Rn. 28–30</summary>

b) Die Beklagte durfte eine Trennung der Kosten für Wärme und Warmwasser auch nicht nach der in § 9 Abs. 2 Satz 4 HeizkostenV aufgeführten Rechenformel vornehmen, weil die Voraussetzungen für eine Trennung der Kosten nach dieser Vorschrift ebenfalls nicht gegeben waren. Die genannte Bestimmung erlaubt in Ausnahmefällen eine rechnerische Ermittlung der auf die zentrale Warmwasserversorgungsanlage entfallenden Wärmemenge in Abhängigkeit zu der durch die zentrale Anlage mit Warmwasser versorgten Fläche, wenn weder die Wärmemenge noch das Volumen des verbrauchten Wassers gemessen werden können. Der Beklagten war jedoch nach den im Revisionsverfahren nicht angegriffenen Feststellungen des Berufungsgerichts ausweislich der von ihr erstellten Abrechnungen die Messung des Volumens des verbrauchten Wassers aufgrund der für die einzelnen Wohnungen installierten Warmwasserzähler möglich.
c) Die im Hinblick auf § 9 Abs. 1, Abs. 2 Satz 1, 4 HeizkostenV nicht ordnungsgemäße Abrechnung führt - entgegen der Auffassung des Berufungsgerichts (ebenso LG Berlin, Urteil vom 20. Juni 2018 - 65 S 29/18, juris Rn. 7 ff.; LG Berlin [67. Zivilkammer], WuM 2017, 463 f.; MünchKommBGB/Zehelein, 8. Aufl., § 12 HeizkostenV Rn. 1; Langenberg/Zehelein, Betriebskosten- und Heizkostenrecht, 9. Aufl., K Rn. 150; wohl auch BeckOGK/Drager, HeizkostenV, Stand: 1. Juli 2021, § 12 Rn. 8) - nach den dargestellten Grundsätzen dazu, dass dem Kläger im Hinblick auf die Kosten für Wärme und Warmwasser das Kürzungsrecht nach § 12 Abs. 1 Satz 1 HeizkostenV in Höhe von 15 % zusteht (vgl. auch LG Potsdam, WuM 2018, 90; LG Berlin, Urteil vom 16. Januar 2018 - 63 S 91/17, juris Rn. 25 ff.; LG Halle, WuM 2019, 318 f.; LG Frankfurt aM, Urteil vom 28. Oktober 2019 - 2/11 S 38/19, juris Rn. 26 ff.; AG Osnabrück, WuM 2021, 591; BeckOK-Mietrecht/Pfeifer, Stand: 1. November 2021, § 12 HeizkostenV Rn. 11c; Wall, Betriebs- und Heizkosten-Kommentar, 5. Aufl., § 9 HeizkostenV Rn. 6329; Schmidt-Futterer/Lammel, Mietrecht, 15. Aufl., § 9 HeizkostenV Rn. 13; Lützenkirchen, Mietrecht, 3. Aufl., § 12 HeizkostenV Rn. 24; im Grundsatz ebenso LG Itzehoe, ZMR 2019, 499, 500; Schmid/Harz/Ormanschick, Mietrecht, 6. Aufl., § 12 HeizkostenV Rn. 13).
3. Die vom Berufungsgericht zur Begründung seiner gegenteiligen Auffassung angeführten Gründe vermögen demgegenüber nicht zu überzeugen.

</details>

<details><summary>BGH VIII ZR 151/20, Leitsatz</summary>

Von einer nicht verbrauchsabhängigen Abrechnung im Sinne von § 12 Abs. 1 Satz 1 HeizkostenV ist auch dann auszugehen, wenn zwar die Wohnung über Heizkostenverteiler und Warmwasserzähler, jedoch die verbundene zentrale Wärme- und Warmwasserversorgungsanlage nicht über den nach § 9 Abs. 2 Satz 1 HeizkostenV vorgesehenen Wärmemengenzähler verfügt.

</details>

<details><summary>§ 12 HeizkostenV</summary>

(1) Soweit die Kosten der Versorgung mit Wärme oder Warmwasser entgegen den Vorschriften dieser Verordnung nicht verbrauchsabhängig abgerechnet werden, hat der Nutzer das Recht, bei der nicht verbrauchsabhängigen Abrechnung der Kosten den auf ihn entfallenden Anteil um 15 vom Hundert zu kürzen. Wenn der Gebäudeeigentümer entgegen § 5 Absatz 2 oder Absatz 3 keine fernablesbare Ausstattung zur Verbrauchserfassung installiert hat, hat der Nutzer das Recht, bei der Abrechnung der Kosten den auf ihn entfallenden Anteil um 3 vom Hundert zu kürzen. Dasselbe ist anzuwenden, wenn der Gebäudeeigentümer die Informationen nach § 6a nicht oder nicht vollständig mitteilt. Die Sätze 1 bis 3 sind nicht anzuwenden beim Wohnungseigentum im Verhältnis des einzelnen Wohnungseigentümers zur Gemeinschaft der Wohnungseigentümer; insoweit verbleibt es bei den allgemeinen Vorschriften.
(2) Wird in den Fällen des § 1 Absatz 3 der Wärmeverbrauch der einzelnen Nutzer am 30. September 1989 mit Einrichtungen zur Messung der Wassermenge ermittelt, gilt die Anforderung des § 5 Absatz 1 Satz 1 als erfüllt.
(3) Wenn der anteilige Verbrauch der Nutzer an Wärme oder Warmwasser aus Wärmepumpen am 1. Oktober 2024 noch nicht erfasst wird, hat der Gebäudeeigentümer bis zum Ablauf des 30. September 2025 eine Ausstattung zur Verbrauchserfassung zu installieren. In den Fällen des Satzes 1 sind die Vorschriften dieser Verordnung für den Abrechnungszeitraum, der nach der Installation beginnt, erstmalig anzuwenden. Der Eigentümer eines vermieteten Gebäudes, in dem mindestens ein Mieter eine Bruttowarmmiete entrichtet, hat vor Beginn des ersten Abrechnungszeitraums nach dem 30. September 2025 Folgendes zu bestimmen:
1. den Durchschnittswert der in den Jahren 2022, 2023 und 2024 jährlich angefallenen Kosten der Versorgung mit Wärme und Warmwasser sowie
2. den Anteil der einzelnen Nutzeinheiten an dem ermittelten Durchschnittswert entsprechend ihrer Wohn- oder Nutzfläche.

</details>

<details><summary>§§ 7–8 HeizkostenV</summary>

(1) Von den Kosten des Betriebs der zentralen Heizungsanlage sind mindestens 50 vom Hundert, höchstens 70 vom Hundert nach dem erfassten Wärmeverbrauch der Nutzer zu verteilen. In Gebäuden, die das Anforderungsniveau der Wärmeschutzverordnung vom 16. August 1994 (BGBl. I S. 2121) nicht erfüllen, die mit einer Öl- oder Gasheizung versorgt werden und in denen die freiliegenden Leitungen der Wärmeverteilung überwiegend gedämmt sind, sind von den Kosten des Betriebs der zentralen Heizungsanlage 70 vom Hundert nach dem erfassten Wärmeverbrauch der Nutzer zu verteilen. In Gebäuden, in denen die freiliegenden Leitungen der Wärmeverteilung überwiegend ungedämmt sind und deswegen ein wesentlicher Anteil des Wärmeverbrauchs nicht erfasst wird, kann der Wärmeverbrauch der Nutzer nach anerkannten Regeln der Technik bestimmt werden. Der so bestimmte Verbrauch der einzelnen Nutzer wird als erfasster Wärmeverbrauch nach Satz 1 berücksichtigt. Die übrigen Kosten sind nach der Wohn- oder Nutzfläche oder nach dem umbauten Raum zu verteilen; es kann auch die Wohn- oder Nutzfläche oder der umbaute Raum der beheizten Räume zu Grunde gelegt werden.
(2) Zu den Kosten des Betriebs der zentralen Heizungsanlage einschließlich der Abgasanlage gehören die Kosten des zur Wärmeerzeugung verbrauchten Stroms und der verbrauchten Brennstoffe und ihrer Lieferung, die Kosten des Betriebsstromes, die Kosten der Bedienung, Überwachung und Pflege der Anlage, der regelmäßigen Prüfung ihrer Betriebsbereitschaft und Betriebssicherheit einschließlich der Einstellung durch eine Fachkraft, der Reinigung der Anlage und des Betriebsraumes, die Kosten der Messungen nach dem Bundes-Immissionsschutzgesetz, die Kosten der Anmietung oder anderer Arten der Gebrauchsüberlassung einer Ausstattung zur Verbrauchserfassung sowie die Kosten der Verwendung einer Ausstattung zur Verbrauchserfassung einschließlich der Kosten der Eichung sowie der Kosten der Berechnung, Aufteilung und Abrechnungs- und Verbrauchsinformationen gemäß § 6a.
(3) Für die Verteilung der Kosten der Wärmelieferung gilt Absatz 1 Satz 1 und 3 bis 5 entsprechend.
(4) Zu den Kosten der Wärmelieferung gehören das Entgelt für die Wärmelieferung und die Kosten des Betriebs der zugehörigen Hausanlagen entsprechend Absatz 2.
(1) Von den Kosten des Betriebs der zentralen Warmwasserversorgungsanlage sind mindestens 50 vom Hundert, höchstens 70 vom Hundert nach dem erfassten Warmwasserverbrauch, die übrigen Kosten nach der Wohn- oder Nutzfläche zu verteilen.
(2) Zu den Kosten des Betriebs der zentralen Warmwasserversorgungsanlage gehören die Kosten der Wasserversorgung, soweit sie nicht gesondert abgerechnet werden, und die Kosten der Wassererwärmung entsprechend § 7 Absatz 2. Zu den Kosten der Wasserversorgung gehören die Kosten des Wasserverbrauchs, die Grundgebühren und die Zählermiete, die Kosten der Verwendung von Zwischenzählern, die Kosten des Betriebs einer hauseigenen Wasserversorgungsanlage und einer Wasseraufbereitungsanlage einschließlich der Aufbereitungsstoffe.
(3) Für die Verteilung der Kosten der Warmwasserlieferung gilt Absatz 1 entsprechend.
(4) Zu den Kosten der Warmwasserlieferung gehören das Entgelt für die Lieferung des Warmwassers und die Kosten des Betriebs der zugehörigen Hausanlagen entsprechend § 7 Absatz 2.

</details>

<details><summary>BGH VIII ZR 9/14, Leitsatz</summary>

1. Auch bei hohen Wohnungsleerständen (hier: im Hinblick auf einen im Rahmen der Stadtplanung vorgesehenen Abriss eines 28-Familienhauses) hat es grundsätzlich bei der in § 9 Abs. 4, § 8 Abs. 1 HeizkostenVO vorgeschriebenen anteiligen Umlage von Warmwasserkosten nach Verbrauch zu bleiben.
2. Im Einzelfall kann der Vermieter nach § 241 Abs. 2 BGB verpflichtet sein, dem Verlangen des Mieters auf eine Vertragsänderung dahin gehend zuzustimmen, den nach Verbrauch zu berechnenden Teil der Warmwasserkosten auf das gesetzliche Mindestmaß von 50 % der Gesamtkosten abzusenken, um die Fixkosten bei hohen Leerständen angemessen zu verteilen.
3. Leerstandsbedingten Kostenverschiebungen zu Lasten des Mieters kann darüber hinaus im Einzelfall mit einer aus dem Prinzip von Treu und Glauben (§ 242 BGB) abzuleitenden Anspruchsbegrenzung Rechnung getragen werden. Dabei ist zu berücksichtigen, dass auch der Vermieter durch den Leerstand beträchtliche Nachteile erleidet, weil er - ohne entsprechende Mieteinnahmen zu erhalten - bereits über den von ihm zu tragenden Wohnflächenanteil ebenfalls nicht unbeträchtliche Kosten zu tragen hat.

</details>

<details><summary>BGH VIII ZR 220/17, Leitsatz</summary>

Sofern und soweit Betriebskosten nach gesetzlichen Vorgaben (vgl. etwa § 556a Abs. 1 BGB, § 7 Abs. 1 HeizkostenV) ganz oder teilweise nach Wohnflächenanteilen umgelegt werden, ist für die Abrechnung im Allgemeinen der jeweilige Anteil der tatsächlichen Wohnfläche der betroffenen Wohnung an der in der Wirtschaftseinheit tatsächlich vorhandenen Gesamtwohnfläche maßgebend (insoweit Aufgabe von BGH, Urteil vom 31. Oktober 2007, VIII ZR 261/06, NJW 2008, 142 Rn. 19).

</details>

<details><summary>BGH VIII ZR 9/14, Rn. 29–31</summary>

Eine allgemeine Aussage dazu, in welcher Fallkonstellation sich eine nach den Vorschriften der Heizkostenverordnung zutreffend berechnete Forderung nach den Grundsätzen von Treu und Glauben für den betroffenen Mieter als unzumutbare Belastung darstellt, so dass eine Begrenzung des Anspruchs des Vermieters der Höhe nach angezeigt ist, verbietet sich. Ob eine Anspruchskürzung geboten ist und gegebenenfalls in welchem Umfang, obliegt der Beurteilung des Tatrichters, der hierbei alle Umstände des jeweiligen Einzelfalls bei seiner Entscheidung zu berücksichtigen hat. Dabei hat der Tatrichter auch in seine Betrachtung einzubeziehen, dass eine absolute Verteilungsgerechtigkeit bei der Umlage von Betriebskosten vom Gesetz nicht gefordert wird (Senatsurteil vom 6. Oktober 2010 - VIII ZR 183/09, NJW 2010, 3645 Rn. 17). Es geht vielmehr darum, die beiderseitigen Interessen in der Gesamtschau zu einem angemessenen Ausgleich zu bringen.
Bereits das Amtsgericht hat zutreffend ausgeführt, dass in Gebäuden mit sehr hohen Leerständen sowohl der Vermieter als auch die verbleibenden Mieter erhebliche Nachteile erleiden. Die verbleibenden Mieter können von hohen Verbrauchskostenumlagen betroffen sein, während der Vermieter, ohne Mieteinnahmen zu haben, über den von ihm zu tragenden Wohnflächenanteil von 50 % ebenfalls nicht unbeträchtliche Kosten zu tragen hat. Dies trifft zu. Deshalb erscheint es auch nicht unbillig, wenn die verbleibenden Mieter einen angemessenen Teil der leerstandsbedingten Mehrkosten zu tragen haben.
Nach alledem kann das Berufungsurteil keinen Bestand haben; es ist aufzuheben (§ 562 Abs. 1 ZPO). Da keine weiteren Feststellungen zu treffen sind, hat der Senat in der Sache selbst zu entscheiden (§ 563 Abs. 3 ZPO).

</details>

---

## q33 (unanswerable)

**Question:** Do I have to get comparison quotes before hiring a cleaning company?

**Your reference answer:** The documents don't say whether you need comparison quotes before hiring a cleaning company. The only quote requirement in the documents (§ 556 Abs. 3a BGB, three offers) concerns fibre provision fees, not other services. Otherwise they only cover the general duty to keep costs reasonable. Check with a tenancy lawyer or your landlord association.

**Agent's answer:**

> Based on the indexed statutes and Federal Court of Justice (*Bundesgerichtshof*, BGH) decisions, the legal requirements are as follows:
>
> ### 1. Agreement in the Lease (*Umlagevereinbarung*)
> Whether you can pass on the costs of a cleaning company at all depends on the lease agreement:
> * Operating costs can only be billed to the tenant if the parties have agreed in the contract that the tenant bears them (*Umlagevereinbarung*) (§ 556 BGB).
> * Under the catalog of operating costs, building cleaning costs (*Kosten der Gebäudereinigung*), which cover the cleaning of jointly used areas such as hallways, staircases, and basements, constitute eligible operating costs (§ 2 Nr. 5–13 BetrKV).
>
> ### 2. The Principle of Economic Efficiency (*Grundsatz der Wirtschaftlichkeit*)
> * In billing operating costs, the landlord must comply with the principle of economic efficiency (*Grundsatz der Wirtschaftlichkeit*) (§ 556 BGB).
> * The landlord has a contractual collateral duty (*vertragliche Nebenpflicht*) to maintain a reasonable cost-benefit ratio (*angemessenes Kosten-Nutzen-Verhältnis*) when making decisions and taking measures that affect the amount of operating costs borne by the tenant (BGH VIII ZR 230/21, Rn. 27–30; BGH VIII ZR 117/21, Rn. 35–38).
> * A breach of this duty can result in a claim for damages by the tenant aimed at reimbursement of unnecessary costs or indemnification from them (BGH VIII ZR 230/21, Rn. 27–30; BGH VIII ZR 117/21, Rn. 35–38).
> * The burden of presentation and proof (*Darlegungs- und Beweislast*) for a breach of duty by the landlord rests on the tenant who asserts the claim (BGH VIII ZR 230/21, Leitsatz; BGH VIII ZR 117/21, Rn. 35–38).
>
> ### 3. Comparison Quotes (*Vergleichsangebote*)
> * The statutory rules governing operating costs do not contain a general obligation to obtain comparison quotes (*Vergleichsangebote*) before hiring routine service providers (§ 556 BGB). By contrast, § 556 BGB explicitly requires obtaining three quotes only for specific complex measures, such as elaborate fiber-optic installations (§ 556 BGB).
> * The retrieved documents and BGH judgments do not state that a landlord is obligated to solicit comparison quotes before hiring a cleaning service. 
>
> Because the indexed documents do not cover whether or when obtaining comparison quotes is required to guard against economic efficiency objections for cleaning contracts, please consult a tenancy lawyer (*Fachanwalt für Miet- und Wohnungseigentumsrecht*).

**Cited passages:**

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>§ 2 Nr. 5–13 BetrKV</summary>

hierzu gehören das Entgelt für die Lieferung des Warmwassers und die Kosten des Betriebs der zugehörigen Hausanlagen entsprechend Nummer 4 Buchstabe a
oder
c) der Reinigung und Wartung von Warmwassergeräten,
hierzu gehören die Kosten der Beseitigung von Wasserablagerungen und Verbrennungsrückständen im Innern der Geräte sowie die Kosten der regelmäßigen Prüfung der Betriebsbereitschaft und Betriebssicherheit und der damit zusammenhängenden Einstellung durch eine Fachkraft;
6. die Kosten verbundener Heizungs- und Warmwasserversorgungsanlagen
a) bei zentralen Heizungsanlagen entsprechend Nummer 4 Buchstabe a und entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind,
oder
b) bei der eigenständig gewerblichen Lieferung von Wärme entsprechend Nummer 4 Buchstabe c und entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind,
oder
c) bei verbundenen Etagenheizungen und Warmwasserversorgungsanlagen entsprechend Nummer 4 Buchstabe d und entsprechend Nummer 2, soweit sie nicht dort bereits berücksichtigt sind;
7. die Kosten des Betriebs des Personen- oder Lastenaufzugs,
hierzu gehören die Kosten des Betriebsstroms, die Kosten der Beaufsichtigung, der Bedienung, Überwachung und Pflege der Anlage, der regelmäßigen Prüfung ihrer Betriebsbereitschaft und Betriebssicherheit einschließlich der Einstellung durch eine Fachkraft sowie die Kosten der Reinigung der Anlage;
8. die Kosten der Straßenreinigung und Müllbeseitigung,
zu den Kosten der Straßenreinigung gehören die für die öffentliche Straßenreinigung zu entrichtenden Gebühren und die Kosten entsprechender nicht öffentlicher Maßnahmen; zu den Kosten der Müllbeseitigung gehören namentlich die für die Müllabfuhr zu entrichtenden Gebühren, die Kosten entsprechender nicht öffentlicher Maßnahmen, die Kosten des Betriebs von Müllkompressoren, Müllschluckern, Müllabsauganlagen sowie des Betriebs von Müllmengenerfassungsanlagen einschließlich der Kosten der Berechnung und Aufteilung;
9. die Kosten der Gebäudereinigung und Ungezieferbekämpfung,
zu den Kosten der Gebäudereinigung gehören die Kosten für die Säuberung der von den Bewohnern gemeinsam genutzten Gebäudeteile, wie Zugänge, Flure, Treppen, Keller, Bodenräume, Waschküchen, Fahrkorb des Aufzugs;
10. die Kosten der Gartenpflege,
hierzu gehören die Kosten der Pflege gärtnerisch angelegter Flächen einschließlich der Erneuerung von Pflanzen und Gehölzen, der Pflege von Spielplätzen einschließlich der Erneuerung von Sand und der Pflege von Plätzen, Zugängen und Zufahrten, die dem nicht öffentlichen Verkehr dienen;
11. die Kosten der Beleuchtung,
hierzu gehören die Kosten des Stroms für die Außenbeleuchtung und die Beleuchtung der von den Bewohnern gemeinsam genutzten Gebäudeteile, wie Zugänge, Flure, Treppen, Keller, Bodenräume, Waschküchen;
12. die Kosten der Schornsteinreinigung,
hierzu gehören die Kehrgebühren nach der maßgebenden Gebührenordnung, soweit sie nicht bereits als Kosten nach Nummer 4 Buchstabe a berücksichtigt sind;
13. die Kosten der Sach- und Haftpflichtversicherung,

</details>

<details><summary>BGH VIII ZR 230/21, Rn. 27–30</summary>

b) Das Berufungsgericht hat weiter zu Recht angenommen, dass die Beklagte als Vermieterin gemäß § 556 Abs. 3 Satz 1 Halbs. 2 BGB gegenüber den Klägern als ihren Mietern die vertragliche Nebenpflicht trifft, bei Maßnahmen und Entscheidungen, die Einfluss auf die Höhe der von diesen zu tragenden Betriebskosten haben, auf ein angemessenes Kosten-Nutzen-Verhältnis Rücksicht zu nehmen (sogenannter Wirtschaftlichkeitsgrundsatz; vgl. BGH, Urteile vom 28. November 2007 - VIII ZR 243/06, NJW 2008, 440 Rn. 14; vom 6. Juli 2011 - VIII ZR 340/10, NJW 2011, 3028 Rn. 13; vom 17. Dezember 2014 - XII ZR 170/13, NJW 2015, 855 Rn. 10; vom 27. Oktober 2021 - VIII ZR 114/21, NJW-RR 2022, 157 Rn. 30), und dass die Verletzung dieser Pflicht durch den Vermieter zu einem Schadensersatzanspruch des Mieters nach § 280 Abs. 1, § 241 Abs. 2 BGB führen kann, der auf Rückzahlung der unnötigen Kosten beziehungsweise auf Freihaltung von diesen gerichtet ist (vgl. Senatsurteile vom 28. November 2007 - VIII ZR 243/06, aaO; vom 6. Juli 2011 - VIII ZR 340/10, aaO; vom 5. Oktober 2022 - VIII ZR 117/21, NJW-RR 2022, 1593 Rn. 36).
c) Das Berufungsgericht hat jedoch - wie die Revision mit Recht geltend macht - die für eine Verletzung dieser Pflicht notwendigen Feststellungen nicht getroffen, weil es sowohl den Inhalt dieser Pflicht als auch die diesbezügliche Verteilung der Darlegungs- und Beweislast verkannt hat.
aa) Die Beurteilung der Frage, ob die Beklagte gegen das Wirtschaftlichkeitsgebot verstoßen hat, ist zwar das Ergebnis einer tatrichterlichen Würdigung, die in der Revisionsinstanz nur eingeschränkt darauf überprüft werden kann, ob das Berufungsgericht den Rechtsbegriff des Gebots der Wirtschaftlichkeit verkannt, wesentliche Umstände übersehen oder nicht vollständig gewürdigt, Denkgesetze oder Erfahrungssätze verletzt oder Verfahrensfehler begangen hat (vgl. Senatsbeschluss vom 20. April 2010 - VIII ZR 254/09, WuM 2010, 431 Rn. 5 mwN).
bb) Solche Fehler liegen hier indes vor.

</details>

<details><summary>BGH VIII ZR 117/21, Rn. 35–38</summary>

aa) Die Revision geht zwar zutreffend davon aus, dass die Beklagte bei einem Verstoß gegen das Wirtschaftlichkeitsgebot die durch die Beauftragung des externen Dienstleisters mit der Kontrolle der Restmüllbehälter und mit der Nachsortierung von Hand entstandenen Kosten nicht auf die Kläger umlegen könnte.
Denn den Vermieter trifft die vertragliche Nebenpflicht, bei Maßnahmen und Entscheidungen, die Einfluss auf die Höhe der vom Mieter zu tragenden Betriebskosten haben, auf ein angemessenes Kosten-Nutzen-Verhältnis Rücksicht zu nehmen. Eine Verletzung dieser Pflicht durch den Vermieter kann zu einem Schadensersatzanspruch des Mieters gemäß § 280 Abs. 1, § 241 Abs. 2 BGB führen, der sich auf dessen Freihaltung von den unnötigen Kosten richtet (vgl. BGH, Urteile vom 28. November 2007 - VIII ZR 243/06, NZM 2008, 78 Rn. 14; vom 6. Juli 2011 - VIII ZR 340/10, NZM 2011, 705 Rn. 13; vom 17. Dezember 2014 - XII ZR 170/13, NZM 2015, 132 Rn. 10 f.). Die Darlegungs- und Beweislast für ein in diesem Sinne pflichtwidriges Verhalten des Vermieters trägt der Mieter, der wegen einer Verletzung des Wirtschaftlichkeitsgebots Ansprüche erhebt (vgl. Senatsurteil vom 6. Juli 2011 - VIII ZR 340/10, aaO Rn. 16).
bb) Das Berufungsgericht, das von diesem rechtlichen Maßstab ausgegangen ist, hat jedoch zu Recht angenommen, dass die Kläger im Streitfall eine diesbezügliche Pflichtverletzung der Beklagten nicht (hinreichend) dargelegt haben.
(1) Ohne Erfolg beanstandet die Revision insoweit mit der Verfahrensrüge, das Berufungsgericht habe entscheidungserheblichen Sachvortrag der Kläger zur Nichterkennbarkeit einer Kostenersparnis durch das "Behältermanagement" nicht beachtet und sei (nur) deshalb von einem nicht ausreichenden oder unzulässigen Vortrag der Kläger ausgegangen.

</details>

<details><summary>BGH VIII ZR 230/21, Leitsatz</summary>

1. Wurde ein die Betriebskosten auslösender Dienstleistungsvertrag bereits vor Abschluss des Wohnraummietvertrags geschlossen, kann eine mögliche Verletzung des Wirtschaftlichkeitsgebots als Nebenpflicht des Vermieters schon wegen einer zu diesem Zeitpunkt noch nicht bestehenden mietvertraglichen Rücksichtnahmepflicht nicht in der Eingehung dieser Verbindlichkeit gesehen werden. Vielmehr kommt eine Verletzung des Wirtschaftlichkeitsgebots nur in Betracht, soweit dem Vermieter - im Falle eines nicht angemessenen Kosten-Nutzen-Verhältnisses - eine Korrektur der zu überhöhten Kosten führenden Maßnahme während des Mietverhältnisses - beispielsweise durch Kündigung eines Vertrags mit ungünstigen Bedingungen - möglich und wirtschaftlich zumutbar gewesen wäre und er diese Möglichkeit nicht ergriffen hat (im Anschluss an Senatsurteil vom 28. November 2007 - VIII ZR 243/06, NJW 2008, 440 Rn. 15).
2. Aus der Einordnung des Wirtschaftlichkeitsgebots als vertragliche Nebenpflicht des Vermieters folgt nach allgemeinen Grundsätzen, dass der Mieter, der wegen einer solchen Pflichtverletzung Ansprüche erhebt, die Darlegungs- und Beweislast für ein pflichtwidriges Verhalten des Vermieters trägt (im Anschluss an Senatsurteile vom 6. Juli 2011 - VIII ZR 340/10, NJW 2011, 3028 Rn. 16; vom 5. Oktober 2022 - VIII ZR 117/21, NJW-RR 2022, 1593 Rn. 36).

</details>

---

## q34 (unanswerable)

**Question:** How does the CO2 step model work for commercial buildings?

**Your reference answer:** The documents don't contain the step model for commercial buildings; they only say one is planned. Check the current CO2KostAufG or ask a specialist.

**Agent's answer:**

> Under current statutory law in the Carbon Dioxide Cost Allocation Act (*Kohlendioxidkostenaufteilungsgesetz* – CO2KostAufG), there is **no operational graduated step model (*Stufenmodell*) for commercial / non-residential buildings (*Nichtwohngebäude*)**. 
>
> Instead, non-residential buildings are governed by a statutory **50/50 split** under **§ 8 CO2KostAufG**:
>
> ### 1. General Rule: 50/50 Split
> * **Definition:** A non-residential building (*Nichtwohngebäude*) is defined as a building that, according to its designated purpose, does not predominantly serve residential use (§ 8 Abs. 1 Satz 2 CO2KostAufG).
> * **Cost Cap:** Agreements in lease contracts for residential space or non-residential premises located in a non-residential building under which the tenant must bear more than 50 percent of the carbon dioxide costs (*Kohlendioxidkosten*) are invalid (§ 8 Abs. 1 Satz 1 CO2KostAufG).
> * **Self-Supply (*Selbstversorgung*):** If the tenant supplies heat or hot water independently, the landlord must reimburse 50 percent of the carbon dioxide costs to the tenant (§ 8 Abs. 2 CO2KostAufG).
>
> ### 2. Billing Allocation
> * Under § 8 Abs. 3 CO2KostAufG, the landlord calculates the portion of carbon dioxide costs attributable to the tenants by determining the total carbon dioxide costs incurred for the building during the accounting period and deducting the landlord's mandatory share. The remaining share is then distributed among the individual tenants in accordance with their contractual cost distribution arrangement (§ 8 Abs. 3 CO2KostAufG).
>
> ### 3. Transition to a Step Model
> * The 10-tier graduated step model (*Stufenmodell*) based on specific annual emissions per square meter of living space applies to residential buildings (*Wohngebäude*) pursuant to § 5 CO2KostAufG and Anlage CO2KostAufG.
> * For non-residential buildings, § 8 Abs. 4 CO2KostAufG explicitly states that the 50/50 division of carbon dioxide costs is to be replaced in the year 2025 by a graduated model for non-residential buildings. Until such a model is introduced in the statute, the 50/50 cost split remains the applicable rule.

**Cited passages:**

<details><summary>§ 8 CO2KostAufG</summary>

(1) Vereinbarungen, nach denen der Mieter mehr als 50 Prozent der Kohlendioxidkosten zu tragen hat, sind in Mietverträgen über Wohnraum oder über Räume, die keine Wohnräume sind, in einem Nichtwohngebäude im Sinn von § 3 Absatz 1 Nummer 23 des Gebäudemodernisierungsgesetzes unwirksam. Ein Nichtwohngebäude ist ein Gebäude, das nach seiner Zweckbestimmung nicht überwiegend dem Wohnen dient.
(2) Versorgt sich der Mieter selbst mit Wärme oder Warmwasser, so hat der Vermieter dem Mieter 50 Prozent der Kohlendioxidkosten zu erstatten; § 6 Absatz 2 Satz 2 bis 4 und Absatz 3 gilt entsprechend.
(3) Der Vermieter berechnet die auf den oder die Mieter im Gebäude entfallenden Kohlendioxidkosten, indem er die im Abrechnungszeitraum für das Gebäude angefallenen Kohlendioxidkosten ermittelt und den gemäß Absatz 1 auf den Vermieter entfallenden Teil abzieht. Der Vermieter berechnet sodann den auf den einzelnen Mieter entfallenden Anteil an den Kohlendioxidkosten gemäß der Vereinbarung zwischen Vermieter und Mieter über die Verteilung der Heiz- und Warmwasserkosten auf Grundlage der §§ 6 bis 10 der Verordnung über Heizkostenabrechnung. § 7 Absatz 3 und 4 gilt entsprechend.
(4) Die hälftige Aufteilung der Kohlendioxidkosten bei Nichtwohngebäuden wird im Jahr 2025 von einem Stufenmodell für Nichtwohngebäude abgelöst werden.

</details>

<details><summary>§ 5 CO2KostAufG</summary>

(1) Der Vermieter ermittelt im Zuge der jährlichen Heizkostenabrechnung den Kohlendioxidausstoß des Gebäudes in Kilogramm Kohlendioxid pro Quadratmeter Wohnfläche und Jahr. Versorgt der Vermieter eine vermietete Wohnung gesondert mit Wärme oder mit Wärme und Warmwasser, ermittelt er den Kohlendioxidausstoß der Wohnung pro Quadratmeter Wohnfläche und Jahr; vermietet er in einem Gebäude mehrere Wohnungen mit gesonderter oder zentraler Versorgung mit Wärme oder mit Wärme und Warmwasser, ist deren Gesamtwohnfläche maßgeblich. Der Wert des nach Satz 1 oder Satz 2 ermittelten spezifischen Kohlendioxidausstoßes ist auf die erste Nachkommastelle zu runden. Ist ein Abrechnungszeitraum von unter einem Jahr vereinbart, so sind die Werte der Einstufungstabelle in der Anlage anteilig zu kürzen. Weichen die Abrechnungszeiträume der Brennstoff- oder Wärmelieferungen von den zwischen Mieter und Vermieter vereinbarten Abrechnungszeiträumen ab, sind die auf den Rechnungen ausgewiesenen Brennstoffemissionen auf den vereinbarten Zeitraum umzurechnen.
(2) Die Aufteilung der im Abrechnungszeitraum angefallenen Kohlendioxidkosten zwischen Mieter und Vermieter richtet sich nach dem spezifischen Kohlendioxidausstoß des Gebäudes oder, in Fällen des Absatzes 1 Satz 2, nach der zugrunde zu legenden Wohnfläche. Dieser Wert ist in die Tabelle in der Anlage einzuordnen, um das maßgebliche Aufteilungsverhältnis zu ermitteln.
(3) Versorgt sich der Mieter selbst mit Wärme oder mit Wärme und Warmwasser, ermittelt der Mieter im Zuge der jährlichen Betriebskostenabrechnung den Kohlendioxidausstoß der gemieteten Wohnung in Kilogramm Kohlendioxid pro Quadratmeter Wohnfläche und Jahr. Zur Einstufung der gemieteten Wohnung wird der spezifische Kohlendioxidausstoß mit der Tabelle in der Anlage abgeglichen und die Wohnung danach der anwendbaren Stufe zugeordnet. Aus der Tabelle ergibt sich das Verhältnis der Aufteilung der im Abrechnungszeitraum des Wärmeversorgers angefallenen Kohlendioxidkosten. Absatz 1 Satz 4 und 5 gilt entsprechend.

</details>

<details><summary>Anlage CO2KostAufG</summary>

(Fundstelle: BGBl. I 2022, 2159)
Kohlendioxidausstoß des vermieteten Gebäudes oder der Wohnung pro Quadratmeter Wohnfläche und Jahr | Anteil Mieter | Anteil Vermieter
< 12 kg CO2/m2/a | 100 % | 0 %
12 bis < 17 kg CO2/m2/a | 90 % | 10 %
17 bis < 22 kg CO2/m2/a | 80 % | 20 %
22 bis < 27 kg CO2/m2/a | 70 % | 30 %
27 bis < 32 kg CO2/m2/a | 60 % | 40 %
32 bis < 37 kg CO2/m2/a | 50 % | 50 %
37 bis < 42 kg CO2/m2/a | 40 % | 60 %
42 bis < 47 kg CO2/m2/a | 30 % | 70 %
47 bis < 52 kg CO2/m2/a | 20 % | 80 %
> = 52 kg CO2/m2/a | 5 % | 95 %

</details>

---

## q35 (unanswerable)

**Question:** Can tenants deduct these costs from their taxes under § 35a EStG?

**Your reference answer:** The documents don't cover whether tenants can deduct these costs from their taxes. Check § 35a EStG or ask a tax advisor.

**Agent's answer:**

> The available legal documents (BGB §§ 535–580a, BetrKV, HeizkostenV, CO2KostAufG, and BGH case law) do not cover tax law (*Steuerrecht*), such as tax reductions under § 35a EStG (*Einkommensteuergesetz*). 
>
> Therefore, the documents do not provide an answer to whether or how tenants can deduct these costs. For questions regarding tax deductions, please consult a tax advisor (*Steuerberater*) or a tenancy lawyer (*Rechtsanwalt/Fachanwalt für Miet- und Wohnungseigentumsrecht*).

**Cited passages:** none matched a retrieved chunk

---

## q36 (unanswerable)

**Question:** My lease makes tenants pay for small repairs up to €100 each. Is that clause valid?

**Your reference answer:** The documents don't cover small-repair clauses. Whether yours is valid depends on its exact wording, so have a tenancy lawyer check it.

**Agent's answer:**

> Based on the search results from the available legal sources:
>
> ### 1. General Statutory Rules on Repairs and Operating Costs
> * **Landlord’s maintenance duty:** Under **§ 535 Abs. 1 Satz 2 BGB**, the landlord is legally obligated to maintain the leased property in a condition suitable for contractual use throughout the tenancy. Furthermore, under **§ 538 BGB**, the tenant is not responsible for wear and tear or deterioration caused by normal contractual use.
> * **Exclusion from operating costs:** Under **§ 1 Abs. 2 Nr. 2 BetrKV** and confirmed by **BGH VIII ZR 62/19, Rn. 8–12**, maintenance and repair costs (*Instandhaltungs- und Instandsetzungskosten*) incurred to fix defects arising from wear and tear, aging, or weather conditions do not constitute operating costs (*Betriebskosten*) and cannot be passed on as service charges.
>
> ### 2. Validity of a Small Repairs Clause (*Kleinreparaturklausel*)
> The documents in this database (which cover residential tenancy law in BGB §§ 535–580a, the BetrKV, the HeizkostenV, the CO2KostAufG, and selected BGH rulings) **do not contain the specific rules governing the validity of standard form small-repair clauses (*Kleinreparaturklauseln*)**. 
>
> The validity of clauses shifting small repairs to tenants—including whether a per-repair cap of €100 is enforceable and what additional restrictions are required (such as an annual aggregate cap or limiting the clause to fixtures subject to frequent, direct physical access by the tenant)—is governed by the law on standard terms and conditions (*Allgemeine Geschäftsbedingungen / AGB*, §§ 305 ff. BGB) and specific case law outside this collection.
>
> Because the documents do not cover these rules, please consult a **tenancy lawyer (*Fachanwalt für Mietrecht*)** to assess whether your specific clause is valid.

**Cited passages:**

<details><summary>§§ 535–536a BGB</summary>

(1) Durch den Mietvertrag wird der Vermieter verpflichtet, dem Mieter den Gebrauch der Mietsache während der Mietzeit zu gewähren. Der Vermieter hat die Mietsache dem Mieter in einem zum vertragsgemäßen Gebrauch geeigneten Zustand zu überlassen und sie während der Mietzeit in diesem Zustand zu erhalten. Er hat die auf der Mietsache ruhenden Lasten zu tragen.
(2) Der Mieter ist verpflichtet, dem Vermieter die vereinbarte Miete zu entrichten.
(1) Hat die Mietsache zur Zeit der Überlassung an den Mieter einen Mangel, der ihre Tauglichkeit zum vertragsgemäßen Gebrauch aufhebt, oder entsteht während der Mietzeit ein solcher Mangel, so ist der Mieter für die Zeit, in der die Tauglichkeit aufgehoben ist, von der Entrichtung der Miete befreit. Für die Zeit, während der die Tauglichkeit gemindert ist, hat er nur eine angemessen herabgesetzte Miete zu entrichten. Eine unerhebliche Minderung der Tauglichkeit bleibt außer Betracht.
(1a) Für die Dauer von drei Monaten bleibt eine Minderung der Tauglichkeit außer Betracht, soweit diese auf Grund einer Maßnahme eintritt, die einer energetischen Modernisierung nach § 555b Nummer 1 dient.
(2) Absatz 1 Satz 1 und 2 gilt auch, wenn eine zugesicherte Eigenschaft fehlt oder später wegfällt.
(3) Wird dem Mieter der vertragsgemäße Gebrauch der Mietsache durch das Recht eines Dritten ganz oder zum Teil entzogen, so gelten die Absätze 1 und 2 entsprechend.
(4) Bei einem Mietverhältnis über Wohnraum ist eine zum Nachteil des Mieters abweichende Vereinbarung unwirksam.
(1) Ist ein Mangel im Sinne des § 536 bei Vertragsschluss vorhanden oder entsteht ein solcher Mangel später wegen eines Umstands, den der Vermieter zu vertreten hat, oder kommt der Vermieter mit der Beseitigung eines Mangels in Verzug, so kann der Mieter unbeschadet der Rechte aus § 536 Schadensersatz verlangen.
(2) Der Mieter kann den Mangel selbst beseitigen und Ersatz der erforderlichen Aufwendungen verlangen, wenn
1. der Vermieter mit der Beseitigung des Mangels in Verzug ist oder
2. die umgehende Beseitigung des Mangels zur Erhaltung oder Wiederherstellung des Bestands der Mietsache notwendig ist.

</details>

<details><summary>§§ 536b–539 BGB</summary>

Kennt der Mieter bei Vertragsschluss den Mangel der Mietsache, so stehen ihm die Rechte aus den §§ 536 und 536a nicht zu. Ist ihm der Mangel infolge grober Fahrlässigkeit unbekannt geblieben, so stehen ihm diese Rechte nur zu, wenn der Vermieter den Mangel arglistig verschwiegen hat. Nimmt der Mieter eine mangelhafte Sache an, obwohl er den Mangel kennt, so kann er die Rechte aus den §§ 536 und 536a nur geltend machen, wenn er sich seine Rechte bei der Annahme vorbehält.
(1) Zeigt sich im Laufe der Mietzeit ein Mangel der Mietsache oder wird eine Maßnahme zum Schutz der Mietsache gegen eine nicht vorhergesehene Gefahr erforderlich, so hat der Mieter dies dem Vermieter unverzüglich anzuzeigen. Das Gleiche gilt, wenn ein Dritter sich ein Recht an der Sache anmaßt.
(2) Unterlässt der Mieter die Anzeige, so ist er dem Vermieter zum Ersatz des daraus entstehenden Schadens verpflichtet. Soweit der Vermieter infolge der Unterlassung der Anzeige nicht Abhilfe schaffen konnte, ist der Mieter nicht berechtigt,
1. die in § 536 bestimmten Rechte geltend zu machen,
2. nach § 536a Abs. 1 Schadensersatz zu verlangen oder
3. ohne Bestimmung einer angemessenen Frist zur Abhilfe nach § 543 Abs. 3 Satz 1 zu kündigen.
Auf eine Vereinbarung, durch die die Rechte des Mieters wegen eines Mangels der Mietsache ausgeschlossen oder beschränkt werden, kann sich der Vermieter nicht berufen, wenn er den Mangel arglistig verschwiegen hat.
(1) Der Mieter wird von der Entrichtung der Miete nicht dadurch befreit, dass er durch einen in seiner Person liegenden Grund an der Ausübung seines Gebrauchsrechts gehindert wird. Der Vermieter muss sich jedoch den Wert der ersparten Aufwendungen sowie derjenigen Vorteile anrechnen lassen, die er aus einer anderweitigen Verwertung des Gebrauchs erlangt.
(2) Solange der Vermieter infolge der Überlassung des Gebrauchs an einen Dritten außerstande ist, dem Mieter den Gebrauch zu gewähren, ist der Mieter zur Entrichtung der Miete nicht verpflichtet.
Veränderungen oder Verschlechterungen der Mietsache, die durch den vertragsgemäßen Gebrauch herbeigeführt werden, hat der Mieter nicht zu vertreten.
(1) Der Mieter kann vom Vermieter Aufwendungen auf die Mietsache, die der Vermieter ihm nicht nach § 536a Abs. 2 zu ersetzen hat, nach den Vorschriften über die Geschäftsführung ohne Auftrag ersetzt verlangen.
(2) Der Mieter ist berechtigt, eine Einrichtung wegzunehmen, mit der er die Mietsache versehen hat.

</details>

<details><summary>§ 1 BetrKV</summary>

(1) Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Sach- und Arbeitsleistungen des Eigentümers oder Erbbauberechtigten dürfen mit dem Betrag angesetzt werden, der für eine gleichwertige Leistung eines Dritten, insbesondere eines Unternehmers, angesetzt werden könnte; die Umsatzsteuer des Dritten darf nicht angesetzt werden.
(2) Zu den Betriebskosten gehören nicht:
1. die Kosten der zur Verwaltung des Gebäudes erforderlichen Arbeitskräfte und Einrichtungen, die Kosten der Aufsicht, der Wert der vom Vermieter persönlich geleisteten Verwaltungsarbeit, die Kosten für die gesetzlichen oder freiwilligen Prüfungen des Jahresabschlusses und die Kosten für die Geschäftsführung (Verwaltungskosten),
2. die Kosten, die während der Nutzungsdauer zur Erhaltung des bestimmungsmäßigen Gebrauchs aufgewendet werden müssen, um die durch Abnutzung, Alterung und Witterungseinwirkung entstehenden baulichen oder sonstigen Mängel ordnungsgemäß zu beseitigen (Instandhaltungs- und Instandsetzungskosten).

</details>

<details><summary>BGH VIII ZR 62/19, Rn. 4, 8–12</summary>

Die Revision hat keinen Erfolg.
Diese Beurteilung hält rechtlicher Nachprüfung stand; die Revision ist daher zurückzuweisen.
Das Berufungsgericht hat zu Recht einen Anspruch der Klägerin auf Zahlung der den Beklagten anteilig berechneten Notdienstpauschale verneint. Bei diesen Kosten handelt es sich, wie das Berufungsgericht richtig gesehen hat, nicht um umlagefähige Betriebskosten, sondern um vom Vermieter zu tragende Verwaltungskosten.
1. Gemäß § 535 Abs. 1 Satz 3, § 556 Abs. 1, 4 BGB hat der Mieter Betriebskosten zu tragen, wenn die Parteien eine entsprechende Vereinbarung wirksam getroffen haben. Grundsätzlich genügt dafür - wie hier im Mietvertrag enthalten - eine Verweisung auf die Anlage 3 zu § 27 Abs. 1 II. Berechnungsverordnung (BV) oder auf die seit dem 1. Januar 2004 geltende Betriebskostenverordnung (Senatsurteil vom 27. Juni 2007 - VIII ZR 202/06, NJW 2007, 3060 Rn. 19).
Betriebskosten sind - wie in Anlage 3 zu § 27 Abs. 1 II. BV und ebenso in § 1 der ab 1. Januar 2004 geltenden Betriebskostenverordnung sowie in § 556 Abs. 1 Satz 2 BGB in der ab 1. Januar 2007 geltenden Fassung definiert - die Kosten, die dem Eigentümer durch das Eigentum an dem Grundstück oder durch den bestimmungsgemäßen Gebrauch des Gebäudes oder der Wirtschaftseinheit, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Von den umlagefähigen Betriebskosten abzugrenzen sind einerseits Kosten der Instandsetzung und Instandhaltung sowie andererseits Verwaltungskosten.
Die (nicht als Betriebskosten umlagefähigen) Aufwendungen für Instandsetzung und Instandhaltung werden durch Reparatur und Wiederbeschaffung verursacht und müssen zur Erhaltung des bestimmungsgemäßen Gebrauchs erbracht werden, um die durch Abnutzung, Alterung, Witterungseinwirkung entstehenden baulichen oder sonstigen Mängel ordnungsgemäß zu beseitigen (§ 28 Abs. 1 II. BV; seit 1. Januar 2004: § 1 Abs. 2 Nr. 2 BetrKV). Instandsetzung und Instandhaltung betreffen deshalb Mängel an der Substanz der Immobilie oder ihrer Teile (Senatsurteile vom 14. Februar 2007 - VIII ZR 123/06, NZM 2007, 282 Rn. 10, 14; vom 7. April 2004 - VIII ZR 167/03, NZM 2004, 417 unter II 1 a). Bei den ebenfalls nicht auf den Mieter umlagefähigen Verwaltungskosten handelt es sich um die Kosten der zur Verwaltung des Gebäudes erforderlichen Arbeitskräfte und Einrichtungen, die Kosten der Aufsicht, den Wert der vom Vermieter persönlich geleisteten Verwaltungsarbeit, die Kosten für die gesetzlichen oder freiwilligen Prüfungen des Jahresabschlusses und die Kosten für die Geschäftsführung (§ 26 Abs. 1 II. BV; seit 1. Januar 2004: § 1 Abs. 2 Nr. 1 BetrKV).

</details>

---

## q37 (unanswerable)

**Question:** A tenant wants copies of all the receipts sent to him. Can I charge him for the copies?

**Your reference answer:** The documents don't say whether you can charge for copies of receipts. They only confirm the tenant's right to inspect them, including payment receipts. Ask a tenancy lawyer.

**Agent's answer:**

> Based on the legal sources in the corpus:
>
> ### What the law provides regarding document inspection
> * **Right of inspection (Belegeinsicht):** Under **§ 556 Abs. 4 Satz 1 BGB**, the landlord must grant the tenant inspection of the supporting documents and receipts underlying the service charge statement upon request (*"Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren"*). This right to inspect receipts also includes the underlying payment receipts (*Zahlungsbelege*; **BGH VIII ZR 118/19, Leitsatz**).
> * **Electronic provision:** Under **§ 556 Abs. 4 Satz 2 BGB**, the landlord is legally entitled to make the receipts available electronically (*"Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen"*).
>
> ### Charging for paper copies
> The documents in the corpus (BGB §§ 535–580a, BetrKV, HeizkostenV, CO2KostAufG, and the indexed BGH judgments) **do not answer** whether or what fee you can charge the tenant for preparing and mailing physical copies of receipts, nor under what circumstances a tenant is legally entitled to paper copies rather than in-person inspection or electronic access.
>
> Because the corpus documents do not cover this specific issue, please consult a **tenancy lawyer (Fachanwalt für Miet- und Wohnungseigentumsrecht)** to determine whether and to what extent you can demand reimbursement of copying and mailing costs (Aufwendungsersatz / Kopierkosten) in your specific situation.

**Cited passages:**

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>BGH VIII ZR 118/19, Leitsatz</summary>

Das Recht des Mieters auf Einsicht in die Belege einer Betriebskostenabrechnung erstreckt sich auch auf die zugrundeliegenden Zahlungsbelege.

</details>

---

## q38 (unanswerable)

**Question:** Can I charge the tenant interest on a late back payment?

**Your reference answer:** The documents don't cover interest on late back payments. Check the BGB rules on default (Verzug) or ask a lawyer.

**Agent's answer:**

> Based on the legal documents in the corpus, the situation regarding charging interest on a late back payment (Betriebskostennachzahlung) is as follows:
>
> ### 1. General Entitlement Recognized by Case Law
> The Federal Court of Justice (BGH) recognizes that a landlord can claim the balance of a service and heating charge statement plus interest (*"Saldos [...] nebst Zinsen"*, **BGH VIII ZR 47/25, Rn. 12, 27–30**). Furthermore, claims for default damages and interest generally relate to statutory default provisions (**BGH VIII ZR 137/15, Rn. 23–26**, citing §§ 280 Abs. 2, 286, 288 BGB).
>
> ### 2. Required Facts and Prerequisites for the Underlying Claim
> Whether the tenant owes the back payment itself depends on key statutory conditions:
> * **Lease Agreement (*Umlagevereinbarung*):** The tenant is only obligated to pay operating costs if the tenancy contract expressly agrees that the tenant bears operating costs (**§ 556 Abs. 1 Satz 1 BGB**).
> * **Timely Billing:** The statement must be communicated to the tenant no later than twelve months after the end of the billing period (**§ 556 Abs. 3 Satz 2 BGB**). After this period expires, asserting a back payment is generally excluded unless the landlord is not responsible for the delay (**§ 556 Abs. 3 Satz 3 BGB**; **BGH VIII ZR 249/15, Rn. 5, 12–14**).
>
> ### 3. Missing Specifics in the Corpus
> The specific legal prerequisites governing **default interest** (*Verzugszinsen*)—such as:
> * when the payment precisely falls due (*Fälligkeit*),
> * when the tenant is legally in default (*Verzug*),
> * whether a reminder (*Mahnung*) or payment period is required, and
> * the applicable statutory default interest rate (*Verzugszinssatz*),
>
> are governed by the general law of obligations in the German Civil Code (Allgemeines Schuldrecht des BGB, notably §§ 286, 288 BGB). Because this corpus only contains residential tenancy law (**BGB §§ 535–580a**, BetrKV, HeizkostenV, CO2KostAufG, and selected BGH decisions), these detailed general statutory default rules are **not covered by the documents**. 
>
> To determine the exact prerequisites, deadlines, and calculation for charging default interest in your specific case, you should consult a **tenancy lawyer** (*Fachanwalt für Mietrecht*).

**Cited passages:**

<details><summary>BGH VIII ZR 47/25, Rn. 12, 27–30</summary>

Die Revision des Beklagten hat teilweise Erfolg.
Diese Beurteilung hält rechtlicher Nachprüfung nicht in jeder Hinsicht stand.
Das Berufungsgericht hat zwar rechtsfehlerfrei angenommen, dass die Klägerin die Zahlung des sich aus der Betriebs- und Heizkostenabrechnung für das Jahr 2017 betreffend die Wohnung Nr. 40020 ergebenden Saldos in Höhe von 704,73 € nebst Zinsen verlangen kann, weil der Beklagte mit Einwendungen gegen diese Abrechnung gemäß § 556 Abs. 3 Satz 6 BGB ausgeschlossen und dieser Zahlungsanspruch auch nicht verjährt ist.
Mit der vom Berufungsgericht gegebenen Begründung kann jedoch ein Anspruch der Klägerin auf Zahlung des sich aus den Betriebs- und Heizkostenabrechnungen für die Jahre 2018 bis 2020 ergebenden Saldos in Höhe von 1.843,70 € nicht bejaht werden. Das Berufungsgericht hat zwar noch zu Recht eine entsprechende Anwendbarkeit der Vorschrift des § 556c BGB verneint. Es hat jedoch im Rahmen der von ihm vorgenommenen ergänzenden Vertragsauslegung bei der Annahme einer hierfür erforderlichen Regelungslücke übersehen, dass die Parteien sich nach der Umstellung der Wärmeversorgung auf eine Wärmelieferung zumindest stillschweigend grundsätzlich auf eine Umlage von Wärmekosten als Betriebskosten geeinigt haben. Ob diese Vereinbarung auch die Umlage der hier noch streitgegenständlichen Wärmekosten erfasst, kann anhand der vom Berufungsgericht bislang getroffenen Feststellungen nicht abschließend beurteilt werden.
1. Das Berufungsgericht hat allerdings noch zu Recht angenommen, dass der Klägerin ein Anspruch auf Zahlung restlicher Wärmekosten in der geltend gemachten Höhe von 704,73 € für das Jahr 2017 gegen den Beklagten zusteht.

</details>

<details><summary>BGH VIII ZR 137/15, Rn. 23–26</summary>

Da die Beklagten die Betriebskosten zu tragen und für den Zeitraum von Januar 2009 bis einschließlich März 2012 die vereinbarten Vorauszahlungen zu entrichten hatten, sind sie - nachdem die Parteien den Rechtsstreit in Höhe eines Betrages von 300 € (Vorauszahlungen für Mai bis Juli 2012) in der Hauptsache übereinstimmend für erledigt erklärt haben - zur Zahlung dieses Betrages (nebst Zinsen) verpflichtet, dessen Höhe zwischen den Parteien nicht im Streit steht. Die von den Beklagten insoweit erklärte Aufrechnung geht ins Leere, weil ihnen kein Anspruch auf Rückzahlung erbrachter Nebenkostenvorauszahlungen zusteht.
Zudem haben die Beklagten den Klägerinnen gemäß § 280 Abs. 2, §§ 286, 288 Abs. 4, § 249 Abs. 1 BGB die gemachten außergerichtlichen Anwaltskosten und gemäß § 280 Abs.1, § 249 Abs. 1 BGB die Kosten für die eingeholte Meldeauskunft, jeweils nebst Zinsen, zu erstatten.
Die Berufung der Beklagten gegen das amtsgerichtliche Urteil ist daher hinsichtlich der vorgenannten Ansprüche zurückzuweisen.
2. Soweit das Berufungsgericht die Klage bezüglich der Vorauszahlung für den Monat April 2012 in Höhe von 100 € nebst Zinsen abgewiesen hat, ist der Rechtsstreit nicht zur Endentscheidung reif und insoweit an das Berufungsgericht zurückzuverweisen (§ 563 Abs. 1 Satz 1 ZPO). Denn die ursprünglich geschuldeten und damit von den Beklagten zunächst auch zu verzinsenden Vorauszahlungen stehen den Klägerinnen nicht mehr zu, weil vor dem Schluss der mündlichen Berufungsverhandlung Abrechnungsreife eingetreten ist (hier mit dem Ablauf des 31. Dezember 2013; § 556 Abs. 3 Satz 2 BGB). Die Klägerinnen können daher nur noch einen sich aus einer ordnungsgemäßen Nebenkostenabrechnung ergebenden Saldo verlangen und - wozu ihnen Gelegenheit zu geben ist - die Klage gemäß § 264 Nr. 3 ZPO entsprechend umstellen (vgl. Senatsurteil vom 16. Juni 2010 - VIII ZR 258/09, NJW 2011, 145 Rn. 22 mwN).
Dr. Milger Dr. Achilles Dr. Fetzer

</details>

<details><summary>§ 556 BGB</summary>

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003 (BGBl. I S. 2346, 2347) fort. Die Bundesregierung wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates Vorschriften über die Aufstellung der Betriebskosten zu erlassen.
(2) Die Vertragsparteien können vorbehaltlich anderweitiger Vorschriften vereinbaren, dass Betriebskosten als Pauschale oder als Vorauszahlung ausgewiesen werden. Vorauszahlungen für Betriebskosten dürfen nur in angemessener Höhe vereinbart werden.
(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen. Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten. Der Vermieter ist zu Teilabrechnungen nicht verpflichtet. Einwendungen gegen die Abrechnung hat der Mieter dem Vermieter spätestens bis zum Ablauf des zwölften Monats nach Zugang der Abrechnung mitzuteilen. Nach Ablauf dieser Frist kann der Mieter Einwendungen nicht mehr geltend machen, es sei denn, der Mieter hat die verspätete Geltendmachung nicht zu vertreten.
(3a) Ein Glasfaserbereitstellungsentgelt nach § 72 Absatz 1 des Telekommunikationsgesetzes hat der Mieter nur bei wirtschaftlicher Umsetzung der Maßnahme zu tragen. Handelt es sich um eine aufwändige Maßnahme im Sinne von § 72 Absatz 2 Satz 4 des Telekommunikationsgesetzes, hat der Mieter die Kosten nur dann zu tragen, wenn der Vermieter vor Vereinbarung der Glasfaserbereitstellung soweit möglich drei Angebote eingeholt und das wirtschaftlichste ausgewählt hat.
(4) Der Vermieter hat dem Mieter auf Verlangen Einsicht in die der Abrechnung zugrundeliegenden Belege zu gewähren. Der Vermieter ist berechtigt, die Belege elektronisch bereitzustellen.
(5) Eine zum Nachteil des Mieters von Absatz 1, Absatz 2 Satz 2, Absatz 3 oder Absatz 3a abweichende Vereinbarung ist unwirksam.

</details>

<details><summary>BGH VIII ZR 249/15, Rn. 5, 12–14</summary>

Die Revision hat keinen Erfolg.
Diese Beurteilung hält rechtlicher Nachprüfung stand, so dass die Revision zurückzuweisen ist.
Das Berufungsgericht hat rechtsfehlerfrei einen Anspruch des Klägers auf Zahlung restlicher Betriebskosten aus den Betriebskostenabrechnungen für die Jahre 2010, 2011 und 2012 verneint. Die Geltendmachung der Betriebskostennachforderungen für die Jahre 2010 und 2011 ist gemäß § 556 Abs. 3 Satz 3 BGB ausgeschlossen, weil der Kläger die Abrechnungsfrist gemäß § 556 Abs. 3 Satz 2 BGB nicht eingehalten und er nicht dargetan hat, dass er die verspätete Geltendmachung der Nachforderungen nicht zu vertreten hat. Entgegen der Auffassung der Revision hat der Vermieter einer Eigentumswohnung über die Betriebskostenvorauszahlungen des Mieters grundsätzlich auch dann innerhalb der Frist des § 556 Abs. 3 Satz 2 BGB abzurechnen, wenn zu diesem Zeitpunkt ein Beschluss der Wohnungseigentümer gemäß § 28 Abs. 5 WEG über die Jahresabrechnung (§ 28 Abs. 3 WEG) des Verwalters der Wohnungseigentümergemeinschaft noch nicht vorliegt. Hinsichtlich der Betriebskostenabrechnung für das Jahr 2012, die der Kläger der Beklagten rechtzeitig mitgeteilt hat, hat das Berufungsgericht eine Nachforderung des Klägers ebenfalls ohne Rechtsfehler verneint, da diese Forderung jedenfalls durch die vom Kläger vorgenommene Aufrechnung gegen das Kautionsguthaben der Beklagten erloschen ist (§ 389 BGB).
1. Haben die Parteien - wie hier der Fall - im Wohnraummietvertrag vereinbart, dass der Mieter die Betriebskosten trägt und hierfür Vorauszahlungen leistet (§ 535 Abs. 2, § 556 Abs. 1 Satz 1, Abs. 2 BGB), hat der Vermieter über die Vorauszahlungen jährlich abzurechnen (§ 556 Abs. 3 Satz 1 Halbs. 1 BGB). Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen (§ 556 Abs. 3 Satz 2 BGB). Nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn der Vermieter hat die verspätete Geltendmachung nicht zu vertreten (§ 556 Abs. 3 Satz 3 BGB). Diese Grundsätze gelten, wie das Berufungsgericht zutreffend angenommen hat, auch für den Vermieter einer Eigentumswohnung.

</details>

---

## q39 (unanswerable)

**Question:** What are typical service charges per m² in Munich?

**Your reference answer:** The documents don't contain typical service charge figures for Munich. Check a current Betriebskostenspiegel, e.g. from the Deutscher Mieterbund or a local landlord association.

**Agent's answer:**

> The indexed legal documents (BGB §§ 535–580a, BetrKV, HeizkostenV, CO2KostAufG, and BGH case law) do not contain statistical data or figures on local price levels, such as the typical or average service charges (*Betriebskosten*) per square meter in Munich. 
>
> For local figures and benchmarks (such as the local operating cost index, *Betriebskostenspiegel*), please consult a tenancy lawyer (*Fachanwalt für Miet- und Wohnungseigentumsrecht*), a local landlord or property owners' association (e.g., *Haus & Grund München*), or a local tenants' association (*Mieterverein München*).

**Cited passages:** none matched a retrieved chunk

---
