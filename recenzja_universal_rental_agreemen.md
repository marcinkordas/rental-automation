### 1. §3, §4, §6 – ocena pod kątem „najem” vs „usługa zakwaterowania”

#### §3 – Okres najmu i charakter umowy

Plusy (dobrze chroniące „najem mieszkaniowy”):

- Wyraźne wskazanie: „**Najem mieszkaniowy (powyżej 30 dni)**” – to jest spójne z PKD 68.20 i praktyką, że najem na miesiące/lata bez usług hotelowych kwalifikuje się jako najem lokali mieszkalnych. [luxise](https://luxise.pl/pkd-wynajem-krotkoterminowy/)
- Oświadczenie: „najem jest na **cele mieszkaniowe** (zgodnie z art. 659 KC)” – to jest dokładnie to, czego wymaga art. 43 ust. 1 pkt 36 ustawy o VAT: lokal mieszkalny, używany wyłącznie na cele mieszkaniowe. [inforlex](https://www.inforlex.pl/dok/tresc,FOB0000000000006916038,Zwolnienie-z-VAT-najmu-dlugoterminowego-nieruchomosci-o-charakterze-mieszkalnym-na-cele-mieszkaniowe-art-43-ust-1-pkt-36-ustawy-o-VAT-Interpretacja-indywidualna-z-dnia-4-kwietnia-2025-r-Dyrektor.html)

Ryzyka / czerwone lampki:

- Tabela z „Zameldowanie / Check‑in, Wymeldowanie / Check‑out, Liczba nocy / Number of nights” jest żywcem z hotelu/zakwaterowania krótkoterminowego. To są słowa‑klucze, które **audytor od razu skojarzy z PKD 55.20** i usługą zakwaterowania, nawet przy >30 dniach. [jakplacicpodatki](https://www.jakplacicpodatki.pl/aktualnosci/-uslugi-zakwaterowania-a-uslugi-najmu-dlugoterminowego-62)
- Sformułowanie „Zameldowanie / Wymeldowanie” jest hotelowe; przy najmie cywilnoprawnym raczej: „rozpoczęcie najmu”, „zakończenie najmu”, „wydanie lokalu”, „zwrot lokalu”.

Proponowana korekta §3 (kluczowe fragmenty):

- Zamiast tabeli „check‑in/check‑out/liczba nocy”:

> **Okres najmu:** Umowa zostaje zawarta na czas oznaczony od dnia {{ CHECKIN_DATE }} do dnia {{ CHECKOUT_DATE }}. Łączny okres najmu wynosi co najmniej 30 dni kalendarzowych.

- Zamiast „Liczba nocy / Number of nights” – **usunąć całkowicie** ten parametr z umowy (może zostać w systemie Airbnb, ale nie w umowie cywilnoprawnej).

- Dodać zakaz niemieszkalnego wykorzystania:

> Lokal może być wykorzystywany wyłącznie w celu zaspokajania potrzeb mieszkaniowych Najemcy i osób z nim zamieszkujących. Zabronione jest wykorzystywanie lokalu do celów usługowych, biurowych, hotelowych, krótkotrwałego zakwaterowania osób trzecich oraz dalszego podnajmu na doby lub tygodnie.

To wzmacnia cel mieszkaniowy w rozumieniu art. 43 ust. 1 pkt 36 VAT. [tpa-group](https://www.tpa-group.pl/pl/news/wynajem-nieruchomosci-mieszkalnych-a-vat-kiedy-stawka-8-kiedy-23-a-kiedy-zwolnienie/)

#### §4 – Czynsz i płatności

Plusy:

- „Całkowity czynsz za okres najmu wynosi … PLN” – określenie globalnego czynszu za cały okres jest spójne z klasycznym najmem (może być też za miesiąc, ale ryczałt za okres oznaczony jest OK).
- Brak słów typu „opłata za pobyt za dobę / per night” w umowie – to dobrze, że to nie jest powielone z Airbnb.

Ryzyka:

- Dwukrotne podkreślenie rozliczenia „za pośrednictwem platformy Airbnb” jeszcze tutaj nie szkodzi, ale w połączeniu z §5 (AirCover), §7 (zawarcie przez Airbnb) i kontekstem działalności może być użyte przez KAS jako argument: „to jest typowy model platformy zakwaterowania, nie standardowy najem”. [ifirma](https://www.ifirma.pl/blog/jak-rozliczyc-sprzedaz-i-zakup-airbnb-lub-booking-com/)

Proponowana delikatna modyfikacja:

> Czynsz najmu płatny jest z góry za cały okres najmu. Zapłata może być dokonana za pośrednictwem systemu płatności udostępnionego przez pośrednika (np. platformę rezerwacyjną).

Czyli:

- sprowadzasz Airbnb do roli **pośrednika płatności**,
- nie budujesz narracji, że umowa „jest Airbnb‑owa” – umowa jest między Tobą a najemcą.

#### §6 – Standard utrzymania i obsługi

To jest najważniejszy paragraf pod kątem granicy 68.20 vs 55.20.

Plusy:

- Wyraźne: „Wynajmujący **nie świadczy** usług sprzątania Pokoju w trakcie trwania najmu (brak serwisu hotelowego).” – bardzo dobre i wprost odcina codzienny/regularny serwis hotelowy, który MF i KAS wskazują jako typową cechę usług zakwaterowania objętych stawką 8%. [tpa-group](https://www.tpa-group.pl/pl/news/wynajem-nieruchomosci-mieszkalnych-a-vat-kiedy-stawka-8-kiedy-23-a-kiedy-zwolnienie/)
- Części wspólne opisane jako „zarząd nieruchomością” i „wymóg sanitarny obiektu” – to jest linia obrony, że to nie jest usługa wobec konkretnego najemcy, tylko zwykłe świadczenie właściciela budynku.

Główne ryzyko – punkt 3 (sprzątanie końcowe):

- „Opłata w wysokości {{ CLEANING_FEE }} PLN (pobrana przez Airbnb) …” – sam fakt **wyszczególnienia osobnej „opłaty za sprzątanie”** jest typowy dla usług zakwaterowania na platformach (Airbnb fee, cleaning fee) i bywa używany przez organy do tezy, że mamy kompleksową usługę zakwaterowania (lokal + serwis sprzątania). [jakplacicpodatki](https://www.jakplacicpodatki.pl/aktualnosci/-uslugi-zakwaterowania-a-uslugi-najmu-dlugoterminowego-62)
- Ryzyko zwiększa wskazanie, że opłata jest „pobrana przez Airbnb” – to znów zbliża całość do modelu hotelowego/zakwaterowania przez pośrednika.

Lepsza konstrukcja (tak bardzo bym to „wyprasował”):

1. **W ogóle nie nazywać tego „opłatą za sprzątanie”**, tylko np. „ryczałt na pokrycie kosztów doprowadzenia lokalu do stanu pierwotnego po zakończeniu najmu”.
2. Wprost wskazać, że stanowi **część przychodu z czynszu**, a nie odrębne świadczenie:

Proponowana wersja §6 ust. 3:

> 3. Strony ustalają, że w czynszu najmu zawarty jest również ryczałt na pokrycie kosztów doprowadzenia lokalu do stanu pierwotnego po zakończeniu najmu. Kwota tego ryczałtu wynosi {{ CLEANING_FEE }} PLN i stanowi integralny element wynagrodzenia za najem lokalu, a nie odrębną usługę sprzątania.

A w §4 można doprecyzować:

> Całkowity czynsz za okres najmu, obejmujący również ryczałt na pokrycie kosztów doprowadzenia lokalu do stanu pierwotnego po zakończeniu najmu, wynosi {{ TOTAL_PRICE }} PLN.

Wtedy na fakturze/ewidencji masz **jeden przychód z tytułu najmu zwolnionego z VAT**, bez rozbijania na „najem + cleaning”. To idzie wprost w kierunku świadczenia głównego (najem) i kosztów pomocniczych w nim zawartych. [izbapodatkowa](https://izbapodatkowa.pl/baza-wiedzy/wynajem-lokali-zwolniony-od-vat/)

Słowa, które bym usunął lub mocno ograniczył:

- „opłata za sprzątanie końcowe” – zastąpić jak wyżej.
- „pobrana przez Airbnb” – w umowie między Tobą a najemcą to jest zbędne; technika płatności nie ma znaczenia dla treści stosunku najmu.

---

### 2. „Paradoks Airbnb” – czy sam fakt użycia Airbnb podważa „najem mieszkaniowy”?

Aktualna linia organów (interpretacja ogólna MF 8.10.2021 + liczne KIS):

- O **kwalifikacji VAT i PKD** decyduje faktyczny charakter świadczenia: charakter lokalu, czas trwania, cel najmu (mieszkaniowy czy zakwaterowanie turystyczne), zakres usług dodatkowych (sprzątanie, wymiana pościeli, recepcja, concierge). [doradca.lublin](https://doradca.lublin.pl/publikacje/vat/interpretacja-ogolna-najem-na-cele-mieszkaniowe)
- To, że korzystasz z pośrednika typu Airbnb/Booking, **samo w sobie nie przesądza** o zaklasyfikowaniu do usług zakwaterowania, ale jest „red flagiem”, bo wiąże się zwykle z krótkimi pobytami, obsługą turystów i „hotelową” strukturą opłat. [bed-booking](https://bed-booking.com/pl/czy-musze-miec-dzialalnosc-gospodarcza-przy-wynajmie-krotkoterminowym/)

W Twoim modelu:

- Stawiasz warunek >30 dni, brak recepcji, brak usług bieżącego sprzątania, brak wyżywienia – to mocne argumenty za 68.20 + art. 43 ust. 1 pkt 36 VAT. [izbapodatkowa](https://izbapodatkowa.pl/baza-wiedzy/wynajem-lokali-zwolniony-od-vat/)
- Natomiast używanie Airbnb z vocabularium „check‑in, check‑out, cleaning fee, AirCover, reservation code” **zwiększa ryzyko, że kontroler stwierdzi: „to jest jednak usługa zakwaterowania, tylko na dłuższe pobyty”**.

Rekomendacja:

- W umowie cywilnej maksymalnie **odkleić się językowo** od modelu hotelowego. Airbnb może być w tle jako system płatności i wymiany wiadomości, ale nie jako „struktura prawna” usługi.
- Wewnętrznie (procedury, screeny), pilnować, aby oferty jasno wskazywały „minimum 30 dni, długoterminowy pobyt, brak sprzątania w trakcie, brak śniadań itp.” – to są dowody na cele mieszkaniowe w razie sporu. [luxise](https://luxise.pl/pkd-wynajem-krotkoterminowy/)

---

### 3. VAT – ryzyko „opłaty za sprzątanie” i jak ją ułożyć

Organy podatkowe:

- Jeżeli mamy **świadczenie złożone**: nocleg + sprzątanie, wymiana pościeli, recepcja itp., to całość kwalifikuje się jako usługa zakwaterowania objęta VAT 8% (poz. 47 załącznika nr 3 do ustawy). [legalis](https://legalis.pl/interpretacja-ogolna-mf-w-sprawie-zwolnienia-z-vat-najmu-nieruchomosci-mieszkalnych/)
- Jeżeli mamy **„goły” najem mieszkalny na cele mieszkaniowe**, bez usług dodatkowych, korzysta ze zwolnienia art. 43 ust. 1 pkt 36. [inforlex](https://www.inforlex.pl/dok/tresc,FOB0000000000006916038,Zwolnienie-z-VAT-najmu-dlugoterminowego-nieruchomosci-o-charakterze-mieszkalnym-na-cele-mieszkaniowe-art-43-ust-1-pkt-36-ustawy-o-VAT-Interpretacja-indywidualna-z-dnia-4-kwietnia-2025-r-Dyrektor.html)

Twoja konstrukcja:

- Sprzątanie końcowe po wyprowadzce – z definicji NIE jest usługą świadczoną „w trakcie pobytu” i można ją obronić jako koszt przywrócenia lokalu po zakończeniu najmu.
- Problemem jest **wyodrębnienie opłaty** i jej nazwanie jako usługi sprzątania, bo to rodzi pokusę dla fiskusa, by twierdzić, że świadczysz **dwie usługi**: najmu (zwolnioną) i sprzątania (opodatkowaną, co najmniej 8% lub 23%), ewentualnie jedną kompleksową usługę zakwaterowania (8%). [gov.legalis](https://gov.legalis.pl/stawka-vat-na-uslugi-sprzatania-wewnatrz-i-na-zewnatrz-budynkow/)

Bezpieczniejsza strategia VAT:

- W umowie i w ewidencji traktować całość jako **czynsz najmu zwolniony**, a element odpowiadający „sprzątaniu końcowemu” jako **część tego czynszu** (ryczałt na koszty odtworzenia stanu lokalu).
- Nie wystawiać osobnych pozycji typu „usługa sprzątania”, tylko jedna pozycja „najem lokalu mieszkalnego na cele mieszkaniowe – zwolnione art. 43 ust. 1 pkt 36 VAT”. [inforlex](https://www.inforlex.pl/dok/tresc,FOB0000000000006916038,Zwolnienie-z-VAT-najmu-dlugoterminowego-nieruchomosci-o-charakterze-mieszkalnym-na-cele-mieszkaniowe-art-43-ust-1-pkt-36-ustawy-o-VAT-Interpretacja-indywidualna-z-dnia-4-kwietnia-2025-r-Dyrektor.html)

Jeśli koniecznie chcesz przejrzystości dla gościa:

- Możesz w komunikacji (np. w opisie oferty na Airbnb) wskazać, że „w cenie uwzględniona jest opłata za sprzątanie po wyjeździe”, ale w umowie + ewidencji księgowej nie rozbijasz tego na osobne świadczenia.

---

### 4. §7 – „per facta concludentia” a ważność umowy i ochrona konsumenta

Prawo cywilne:

- Zawarcie umowy najmu lokalu mieszkalnego **nie wymaga formy pisemnej pod rygorem nieważności**; forma pisemna jest dla celów dowodowych (art. 659 i nast. KC). Umowa może być skutecznie zawarta przez wymianę wiadomości, kliknięcie, wejście do lokalu i zapłatę – klasyczne facta concludentia. [doradca.lublin](https://doradca.lublin.pl/publikacje/vat/interpretacja-ogolna-najem-na-cele-mieszkaniowe)
- Problem nie jest w **ważności** umowy, tylko w sporach dowodowych i w relacji do prawa konsumenckiego (informacja, jasność warunków, brak klauzul abuzywnych).

Twój §7:

- Co do zasady – jest **prawnie poprawny**: sekwencja (rezerwacja i płatność – udostępnienie treści umowy – przekazanie kluczy – objęcie lokalu) dobrze opisuje mechanizm zawarcia umowy przez czynności faktyczne.
- Ryzyko UOKiK/u konsumenta będzie głównie wtedy, jeśli:
  - nie jesteś w stanie **udowodnić chwili przekazania umowy** (np. brak śladu w systemie, że wysłałeś PDF przed przyjazdem),
  - treść umowy zawiera klauzule, które mogą być uznane za niedozwolone, a konsument nie miał realnej możliwości zapoznania się z nimi przed związaniem się (wtedy te klauzule mogą być bezskuteczne).

Dlatego sugeruję wzmocnić §7 dwoma drobnymi doprecyzowaniami:

1. Podkreślić, że treść umowy jest udostępniana w sposób **trwały i możliwy do zapisania**:

> Wynajmujący udostępnia Najemcy treść niniejszej umowy na trwałym nośniku (w szczególności jako plik PDF przesłany za pośrednictwem systemu wiadomości platformy rezerwacyjnej lub poczty elektronicznej) przed rozpoczęciem najmu.

2. Dodać krótkie zdanie o charakterze potwierdzenia przez Najemcę:

> Dokonanie rezerwacji i zapłaty oraz objęcie lokalu w posiadanie po otrzymaniu treści umowy jest równoznaczne z potwierdzeniem zapoznania się z jej treścią i jej akceptacją.

Umowa nie jest nieważna bez „mokrego podpisu”; kwestia jest wyłącznie dowodowa. W razie sporu sąd może jednak uznać niektóre postanowienia za niedoręczone lub abuzywne, jeśli konsument nie miał szansy realnie ich poznać – stąd ważna jest ścieżka dowodowa i minimalistyczna, nieopresyjna treść (brak kar umownych rażąco wygórowanych itd.). [doradca.lublin](https://doradca.lublin.pl/publikacje/vat/interpretacja-ogolna-najem-na-cele-mieszkaniowe)

---

### 5. Ocena ryzyka rekwalifikacji na PKD 55.20 i VAT

Biorąc pod uwagę:

- minimalny okres >30 dni,
- brak recepcji, brak świadczenia usług sprzątania w trakcie pobytu, brak wyżywienia,
- deklarowany cel mieszkaniowy,
- brak rozbijania ceny na „dobowe pobyty” w samej umowie,
- ale też: użycie Airbnb, terminologia „check‑in/check‑out/liczba nocy”, AirCover, „opłata za sprzątanie końcowe” osobno,

szacunkowo:

- **Ryzyko zakwestionowania zastosowania zwolnienia z VAT (art. 43 ust. 1 pkt 36)** w obecnym brzmieniu umowy: **średnie (ok. 40–50%)** – głównie przez red flags językowe i osobno wykazaną opłatę za sprzątanie. [tpa-group](https://www.tpa-group.pl/pl/news/wynajem-nieruchomosci-mieszkalnych-a-vat-kiedy-stawka-8-kiedy-23-a-kiedy-zwolnienie/)
- Po wprowadzeniu opisanych korekt (usunięcie słownictwa hotelowego, włączenie cleaning do czynszu, wzmocnienie zapisu o wyłącznym celu mieszkaniowym): **spadek ryzyka do niskiego–średniego (ok. 20–30%)**, przy założeniu, że faktycznie wszystkie rezerwacje są 30+ dni, a komunikacja marketingowa nie jest „turystyczno‑hotelowa”. [izbapodatkowa](https://izbapodatkowa.pl/baza-wiedzy/wynajem-lokali-zwolniony-od-vat/)

Jeśli chodzi o:

- **rekwalifikację działalności na PKD 55.20** (i w konsekwencji ryczałt 17% oraz VAT 8% wstecz):
  - przy zachowaniu realnego minimum 30 dni, jednej umowy z jednym Najemcą, braku dodatkowych usług typowo hotelowych: **po korektach umowy** oceniam ryzyko jako **raczej niskie (15–25%)**,
  - w obecnym kształcie (z językiem hotelowym i osobną „opłatą za sprzątanie końcowe”): **umiarkowane (30–40%)**, zwłaszcza jeśli kontroler zobaczy ofertę na Airbnb sformatowaną jak typowe zakwaterowanie.

---

### 6. Krótkie podsumowanie strategiczne (co bym zmienił od razu)

1. **§3:**
   - Usunąć tabelę z „Zameldowanie/Check‑in, Wymeldowanie/Check‑out, Liczba nocy”.
   - Opisać okres jako „od dnia X do dnia Y, co najmniej 30 dni kalendarzowych”.
   - Dodać zakaz wykorzystywania lokalu do celów innych niż mieszkaniowe i zakaz podnajmu na doby/tygodnie.

2. **§4:**
   - Zamiast „płatność została zrealizowana w pełni za pośrednictwem platformy Airbnb” – napisać, że czynsz może być płatny za pośrednictwem systemu płatności pośrednika.
   - Wskazać, że całkowity czynsz obejmuje również ryczałt na doprowadzenie lokalu do stanu pierwotnego.

3. **§6:**
   - Zachować expressis verb brak bieżącego sprzątania i brak serwisu hotelowego.
   - Przeredagować ust. 3 tak, aby:
     - nie używać nazwy „opłata za sprzątanie”,
     - nie wskazywać, że opłata jest „pobrana przez Airbnb”,
     - wyraźnie stwierdzić, że kwota jest **integralną częścią czynszu**.

4. **§7:**
   - Dopisać, że umowa jest doręczana na trwałym nośniku przed rozpoczęciem najmu i że rezerwacja + objęcie lokalu po otrzymaniu treści umowy stanowią akceptację warunków.

5. **Operacyjnie (poza umową):**
   - W opisach ofert na Airbnb mocno akcentować: minimum 30 dni, cel mieszkaniowy, brak usług hotelowych, brak sprzątania w trakcie, brak śniadań.
   - Trzymać screeny/archiwum opisów i komunikacji jako materiał dowodowy przy ewentualnym sporze.

Jeśli chcesz, mogę w kolejnym kroku przepisać całe §3, §4, §6, §7 w postaci gotowego, „odchudzonego” brzmienia pod 68.20 + art. 43 ust. 1 pkt 36, tak żebyś mógł to od razu wkleić do szablonu.
