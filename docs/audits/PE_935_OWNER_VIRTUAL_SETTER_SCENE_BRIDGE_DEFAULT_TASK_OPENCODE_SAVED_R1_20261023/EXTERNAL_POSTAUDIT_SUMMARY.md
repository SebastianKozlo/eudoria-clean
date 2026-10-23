# Zewnętrzny postaudyt OWNER FACTORY / ATTACH / LOOKUP

SCIENCE_VERDICT = PARTIAL_PASS_WITH_MATERIAL_SCOPE_CORRECTIONS
PROCESS_VERDICT = PARTIAL_NONCOMPLIANT_WITH_STALE_FINAL_ACCOUNTING
EVIDENCE_INTEGRITY = PASS (44 rows + manifest = 45 files; 435 pinned inputs)
PUBLICATION_INTEGRITY = PASS (11 manifest rows; all public blobs re-hashed)
QC_ORIGIN = INDEPENDENT_DESKTOP_POSTAUDIT (saved evidence only)
CANONICAL_GATE_EFFECT = NONE

OFL-A01: 0085B3E0 ma zero bezpośrednich zapisów do pól receivera w badanym ciele. Nie wolno rozszerzać tego na „nie jest setterem”: końcowe CALL EDX @0085B5CE wywołuje slot VT+4 z adresem lokalnego trio i drugim argumentem. Skutki pośrednie są UNKNOWN. Pierwszy virtual call VT+0xC jest @0085B473, nie @0085B475 (tam FLD).

OFL-A02: node+4=[Q], node+8=[Q+4] i stosowa para {key,B} są potwierdzone dla pokazanej ścieżki tworzenia węzła, pod przesłankami prawidłowych dostępów/preservation. Nie zamknięto całego find-or-insert: JZ @00854DC4 prowadzi do nieotwartego 00854E11. Test @00854279 bada ECX=EAX+4; nie jest testem EAX!=0. Przy EAX=0 ECX=4 i JZ nie zachodzi. Zachować UNKNOWN kontrakt alokatora; nie nazywać gałęzi po JZ zwykłą obsługą null-allocation. Bucket walk jest ograniczony wartościami sąsiednich elementów tablicy; nie dowiedziono osobnych NULL-terminated chains.

OFL-A03: [mgr+0x24]+1 trafia do reserve-like 00856090, a klucz pary pochodzi z [B+0x74]. Nie są to automatycznie dwa namespace keys. Ogólna reguła lookup→payload jest mocna; konkretny B_registered=B_lookup wymaga rzeczywistego klucza callera, udanego insert, retencji wpisu, manager identity i lifetime. Istniejący wpis z innym payloadem lub późniejsza wymiana są kontrmodelami. Nie podnosić faktycznej tożsamości do bezwarunkowego CONFIRMED ani wybierać dynamicznego vptr B na podstawie konstruktora innej instancji.

OFL-A04: rzeczywiście wykonano 11 native Task: 8 workerów + 3 audytorów; finishe 10 stop + 1 length. Wszystkie 11 prompt parity/parent binding PASS; zero grandchildren. ROLE_LEDGER, BODY ledger, FINAL_ACCOUNTING i STAGE gates zachowały 10/PENDING; są nieaktualne. Format PASS nie wykrywa takich sprzeczności. Historia retry A3→A3R/A5 jest ujawniona; podział nie dowodzi automatycznie zgodności z capem per obligation.

OFL-A05: niezależne packet counts: 784 literal instruction occurrences, 553 unikalne VA, 46 CALL occurrences. To nie jest pełna suma exposures runu (master, failed/re-read, cytaty, QC dodatkowo). Deklarowane 1109/596 nie mają kompletnego odtwarzalnego row-set mappingu; nie certyfikować z nich exact global bounds. BODY ledger wlicza found-path 00854E00 jak osobne ciało i pomija odrębne sibling 00854520/00529100 widoczne w packetach; potrzebne osobne body identities i exposure intervals. Nie twierdzimy, że przekroczono globalny cap 80 — pomiar jego zgodności jest niepełny. 78 pre-ADMIT peeks i 4 late READ pozostają naruszeniami, także po ujawnieniu.

OFL-A06: brak slotów w H5/GA3 jest barierą konkretnych reprezentacji. Nie dowodzi ich braku w całym lokalnym archiwum. Najpierw ograniczony katalog zapisanych vtable/xref/data eksportów. Adresy komórek dla hipotezy derived VT=0xA7DCB0: +4=0xA7DCB4, +0xC=0xA7DCBC. Dla base VT=0xA91E4C: 0xA91E50/0xA91E58. To adresy do wyszukania, nie odzyskane targets ani proof dynamic type. SDK Gamebryo jest referencją implementacji, nie źródłem tych komórek MindArk.

Zachowane fakty: stosowa para key/B; kopia do node+8 na zbadanej insertion path; lookup node-key i caller-side payload load; mechaniczna polaryzacja flag na otwartych found/nonempty-miss paths; direct-store negative B3E0; destructor-shaped 00529080. Ograniczenia nie unieważniają tych faktów.

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN.
Publikacja jest poprawnym transportem raportu, nie akceptacją wszystkich jego twierdzeń. Poprawki publikować addytywnie, bez modyfikacji frozen runu.
