# STATIC_R2_POSTAUDIT_NOTICE — PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025

RUN_ID powiązania: PE2003_R2_ISO_PROVENANCE_DESKTOP_POSTAUDIT_R1_20261025 |
Zakładka addytywna do publicznego pakietu R2, 2026-10-25.
Ten plik jest DODATKIEM: wszystkie pliki R2 w tym folderze pozostają
nietknięte (byte-identical z publikacją R2); wiersze ENTRYPOINT runu R2
pozostają bez zmian.

## Powiadomienie o rozstrzygnięciach zewnętrznego postaudytu

Niezależny zewnętrzny postaudyt Desktop pakietu R2
(99_Audits\PE2003_R2_ISO_PROVENANCE_DESKTOP_POSTAUDIT_R1_20261025,
seal MANIFEST_SHA256 SHA256 700215C8DE11F8E165FB0656740F25E35AA1E611BB1665B228865758ED0FD27A)
rozstrzygnął następujące kwestie otwarte po R2 — skorygowane i opublikowane
w następnym runie **PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025**
(pe2003/research/PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025):

1. **NIF identity transforms 31/31 — OBFALONE jako dowód lokalnego
   placementu.** Wniosek R2 „31/31 bloków NiNode identity = brak lokalnych
   danych placementu w dwóch plikach NIF" był oparty na niepełnym
   dekodowaniu. Postaudyt wykazał obecność transformów lokalnych, które R2
   nie zdekodował: w 296445.nif — 5 NiNode + 14 NiTriShape + 7
   NiArkBillboardNode niezerowych translacji oraz 4 NiNode + 7 ArkBillboard
   nie-identity rotacji (TriShape transforms były dotąd niezdekodowane);
   w 218757.nif — 7 NiTriShape niezerowych translacji (patrz
   NIF_TRANSFORM_SUMMARY.md w pakiecie R3).
2. **Kolejność pól P01 BŁĘDNA.** Stara kolumna `translation` w
   P01_NIF_BLOCK_MAP.csv to later triple, nie translacja; poprawna kolejność:
   translation @ rotation_off − 12 (przed macierzą rotacji) — potwierdzone
   bajtowo w R3 (loader 00416860).
3. **Dodatni NIF writer macierzy istnieje.** Sieć wywołań
   004078C0 → 00416860 → 0041B690 (PE2_unpacked_out.exe) — kontrmodel
   „brak pozytywnego writera macierzy NIF w grafie dostępnym z entrypointów
   R2" rozstrzygnięty na korzyść istnienia writera.
4. **Graf sieciowy = ArkBoundingVolumeRenderer.** Rodzina
   ArkBoundingVolumeRenderer (8 vtx/12 tri, m_ptBoxes), do której R2
   dotarł przez create-fn 0x4077F0 / FUN_005030c0, NIE dowodzi instancji
   modelu — pozycja R2-A04 (MISSING_EDGE resource→instance) utrzymana.
5. **PE42 nie jest wykazanym payloadem ISO.** Wydanie ISO 2003-11 zawiera
   build 5.1.0.0 (DIFFERENT_BUILD, NO VA TRANSFER); kanał danych modeli =
   SERVER_DELIVERED_ONLY (FTP MindArk 2003) — corpus PE42 pozostaje
   referencją, nie payloadem ISO.

Korekty wykonane i opublikowane w R3; standing końcowy bez zmian:
WORLD_XYZ_RECOVERED=NO, HISTORICAL_PLACEMENT=NOT_ESTABLISHED,
CANONICAL_GATE_EFFECT=NONE, ADVISORY_PENDING_EXTERNAL_POSTAUDIT.
