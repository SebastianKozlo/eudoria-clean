# Postaudyt PROVIDER PROVENANCE / APPLIER JOIN HIGH

SCIENCE_VERDICT = PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS
PROCESS_VERDICT = PARTIAL_NONCOMPLIANT_WITH_SCOPE_AND_ACCOUNTING_LIMITS
EVIDENCE_INTEGRITY = PASS (117 manifest rows + manifest = 118 physical files)
INPUT_PINS = INDEPENDENT_PASS (820 at audit time; not a historical pre-seal observation)
PACKET_PARITY = PASS (432 saved x86 rows, 0 mismatch vs pinned H5)
NATIVE_TASKS = PASS (21 true children; parent/prompt binding; 13 stop, 8 length; 0 grandchildren)
PUBLICATION = PASS (11 blob pins; exact 12 diff paths; entrypoint 1/0; remote 56b013ec9b0fcc735ee69bb275ddc003e3342fd5 at audit time)
CANONICAL_GATE_EFFECT = NONE

PPA-A01 [P1]: POST_CONSTRUCTION_ONLY jest nieudowodnione. Bazowy ctor zeruje B+0xC/B+0x10; to zachowany fakt instrukcyjny. Brak dalszych bezpośrednich stores nie dowodzi zachowania NULL przez opaque calls, a wycinek głowy pochodnego ctora nie obejmuje jego końca. Zapis w jego tailu nadal byłby zapisem PODCZAS konstrukcji. Poprawić na NONZERO_WRITER_NOT_ESTABLISHED; CONSTRUCTION_PHASE_OPEN. QC QSCI_1b X3 powtarza błąd: complete base body nie jest complete derived construction ani dowodem mod/ref. P04 „No call can attach” i P05 „still null at exit” również wymagają tej korekty. Nie podważa to zero-init ani construction-level vtable binding.

PPA-A02 [P1]: „brak saved coverage taila 00528F07+” jest fałszywym opisem bariery. Przypięty I0316, PACKETS/A3_00528E50_ctor.txt ze starszego OWNER_TRANSFORM_RECEIVER_JOIN, ma 139 wierszy H5, od 00528E50 do 00529072, i zawiera dalszy tail. To PRIOR_AVAILABLE_NOT_READ_IN_CURRENT_RUN. Pełny zapisany H5 również już istnieje. Nie potrzeba nowego eksportu Ghidry ani odczytu EXE. Metadane zasięgu nie są jeszcze analizą CFG, normal exits, pochodzenia receivera ani writera. Następny run ma wykorzystać dostępne dowody, nie zgłaszać sztucznego data-blockera.

PPA-A03 [P2]: MASTER_DERIVED po STOP_JOB ma prawdziwą atrybucję i świeże QC, ale kontrakt §4 mówił, że root nie przepisuje niewykonanej pracy workerów. MASTER_READ upoważnia do zarezerwowanej lektury, nie tworzy sam z siebie wyjątku od tej reguły ani nie resetuje rodziny S. Jakość niezależnie sprawdzonej mechaniki może pozostać ważna, lecz odstępstwa nie można retroaktywnie uznać za compliant. Nowy kontrakt musi albo jawnie dopuścić ograniczony fallback z własną pulą i QC, albo go wykluczyć. Preferowany jest dalszy podział mniejszych jobów przed wyczerpaniem prób.

PPA-A04 [P2]: oddzielić reserved od actual. Zarezerwowane code2203/doc10750 i Task21/28 można odtworzyć. Własny licznik widocznych instrukcji w publicznych outputach narzędzi DB daje co najmniej1156 wystąpień; nie jest pełnym miernikiem ekspozycji, nie obejmuje całego kontekstu/cytatów i nie wyznacza upperbound. Dlatego ~800–870 nie jest kompletnym rachunkiem ani podstawą exact capPASS. Final INPUT_RECHECK obejmuje46 źródeł ticketów, nie820 wejść całego katalogu. Obecny niezależny rehash820 ma PASS, lecz nie może odtworzyć brakującej historycznej bramki. 8 length attempts wymaga szczególnie uwzględnienia failed-tooloutput/context exposures. 117 to liczba wierszy manifestu, plików jest118. Sąsiedni fragment00528600 ma6wierszy, nie deklarowane3; osobny bodyID został na szczęście rozliczony.

PPA-A05 [P2]: „równość wartości statycznie niedowodliwa” zamienić na NOT_ESTABLISHED_IN_ADMITTED_SCOPE przy niezamkniętych mod/ref. Opaque call nie jest twierdzeniem o fundamentalnej niemożliwości dowodu statycznego. Cztery odczyty tego samego fieldaddress zachowują osobne nazwy/czas. „Brak P w writerze” oznacza brak bezpośredniego dereference w tym ciele; wywołany applier czyta P=[R+2C]. Zona census do00528E60 nie obejmuje taila konstruktora. 742 to kandydaci konkretnego wzorca adresowania w saved H5, nie wszyscy writerzy pola ani pełny census klasy. Base vtable A91E4C to potwierdzenie wcześniejszego prioru na tych saved rows, a nie odzyskanie nieznanej wcześniej klasy.

Zachowane wyniki: cztery field-loady i kolejność apply/read/cache; enum3 wybiera identity matrix; 13DWORD record oraz cache; P_apply=M32[R_apply+2C], VT+14, permutacja48B i warunkowy raw cache52B; staticbase/derived vtable stores; census pattern counts ze scoped negatives. SDK porównanie reference-only. Nie potwierdzono R-instance provenance, P-vptr, model-instance join, scene/world role ani źródła historycznych danych. Publikacja jest poprawna integralnościowo i nie nadaje akceptacji naukowej.

NEXT_BASELINE: najpierw pełny saved ctor00528E50 i creator004C46C0 z precyzyjnym this/stack/phase/mod-ref; następnie wyłącznie receiver-qualified writer B+0xC. Nie powtarzać applier/getter/SDK shape ani szerokiego +2C census bez nowej przesłanki. Następny run DEFAULT/MEDIUM dla root/small/children, bo HIGH był jednorazowy. Wymagane prawdziwe nativeTask, małe pakiety, freshscienceQC i odrębne accountingQC, jawne statusy oraz sanitizowany commit/push.

WORLD_XYZ_RECOVERED=NO;HISTORICAL_PLACEMENT=NOT_ESTABLISHED;CURSOR_SOURCE_MEDIUM=UNKNOWN;CANONICAL_GATE_EFFECT=NONE.
