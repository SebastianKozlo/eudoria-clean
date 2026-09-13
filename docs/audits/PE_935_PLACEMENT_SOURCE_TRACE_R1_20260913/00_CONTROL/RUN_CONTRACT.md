# RUN_CONTRACT — PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913

## Zlecenie (PE-MASTER §8–§9, kontynuacja P0 rundy EU935)
Ustal, KTO i Z JAKICH DANYCH produkuje transformacje rekordów placementu statycznych
obiektów w Entropia.exe EU 9.3.5 — rozstrzygając między H1/H2 (lokalne dane/pochodne)
vs H3 (sieć) vs H4 (hybryda). RUN_CLASS: LOAD_BEARING. STATIC-ONLY. NO_NESTED_TASKS.

## Kanon startowy (z RUN 3 — PE_935_STATIC_INSTANCE_TRACE_R1; S0 re-asercja tego runu)
- Binarium: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe
  SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (8,015,872 B),
  image base 0x00400000, brak ASLR.
- Repo: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean
  BASE_SHA = 4d4cde5c09be503bab9dbbd358d75d229d175a97 (HEAD==origin/master — zweryfikowane).
  DIRTY: ?? experiments/ obcej sesji — POZA ZAKRESEM, NIETKNIĘTY.
- Placement-record setters: FUN_00730f90 (pozycja@+0x08), FUN_00730fb0 (rotacja@+0x14),
  FUN_00730f60/FD0 — zasilane z systemu atrybutów FUN_00846840 (ID 0x6A4/0x6A5/0x6A8/0x6A9).
  Builder rekordu: FUN_00567770 ← jedyny caller FUN_00567c50 @0x0056836C.
  Rejestracja: FUN_004148f0 + FUN_00457930 (map-insert z nazwą).
- Most template→encja: ctor ArkObject FUN_00726e70 (A z gettera FUN_007ce1e0 → encja@+0x28).
  Kreator instancji modelu: FUN_006cb6f0 → ArkModelResourceInstanceRef → FUN_006cb020
  ("<id>__<name>") → kolejka FUN_006cb3c0.
- 9.3.5: brak Sector/Region/Entity; cell space = ArkPortalCell (dPVS);
  RM-init FUN_0041dae0 rejestruje .nif/.bvi/.amu/.tdf/.prt/.tez/portals.bnt/TEZ.bnt.
- RTTI census: S1_RTTI_CENSUS.json (483 klas Ark; NOWE dla tego runu: rodzina
  ArkParameter* — ArkParameterTransformation @0x00B8EC08 class-id 0xEODN,
  ArkParameterContainer @0x00B8ED14 class-id 0xEODO, ArkParameterSetObject 0xEOP,
  ArkParameterServerGlobal/Local, ArkObjectFileStorage; sieć: ArkPacket/ArkStaticPacket/
  ArkPacketDecoder/ArkClientPacketExecutor/ArkCommunicator).
- Template record (dane): A→+0x08, B→+0x04, C→+0x0C, D f32→+0x10 w obiekcie template'u
  (parser); w pliku: [id2][A][B][C][D_f32][slot] @payload 28 B. 4508: D=124.941f.

## Hipotezy (bez zwycięzcy z góry)
H1 LOCAL (lokalne pliki niosą placementy), H2 LOCAL_DERIVED (reguły/komórki/pochodne),
H3 NETWORK (transformacje z sieci), H4 HYBRID. Dowód z kodu decyduje; network-first
odrzucony jako założenie (ERRATA_R2); client-side system atrybutów = FAKT (RUN 3);
źródło danych tego systemu = pytanie tego runu.

## Zadania (Z1–Z5) — jak w zleceniu
- Z1: PRODUCENT ATRYBUTÓW — backward slice od FUN_00846840: struktura kontenera,
  PRODUCENT (reader pliku / dekoder pakietu / inny mechanizm), werdykt-źródło
  FILE/NETWORK/BOTH/UNKNOWN-boundary z VA-locked łańcuchem.
- Z2: ŁAŃCUCH CWO/ARKOBJECT — jak powstaje STATYCZNY obiekt świata: creator rekordu
  placementu, wywołujący setterów, łączenie z template'em i instancją modelu; diagram.
- Z3: PORTALS.BNT/.PRT — reader w kodzie, struktura .prt zdekodowana z bajtów i
  zwalidowana przeciw readerowi; werdykt o roli (cell-graph vs placement) z dowodem.
  Portals.bnt READ-ONLY; sample: wpisy 505k–510k + outliery 382811/422806/592739/592741.
- Z4: POLE D (PARAM f32; przy 4508: 124.941) — getter + caller, semantyka.
- Z5: RÓŻNORODNOŚĆ ŚCIEŻEK — drugi przypadek (sibling 4752/2249 lub inny statyk) +
  kontrola negatywna (atrybut z nieistniejącym ID → ścieżka pomijana).

## Kontrole obowiązkowe (§11)
- Każdy VA: plik→SHA→image base→RVA→file offset→surowe bajty (VA_EVIDENCE_REGISTRY).
- Round-trip ID przed skanami wzorców; finiteness (odrzucaj NaN/Inf przy f32);
  STATIC-PROOF vs RUNTIME-UNOBSERVED na każdym twierdzeniu.
- Wykluczenia fałszywych trafień transformacyjnych (kości/kamera/billboardy/UI/lokalne
  części) z powodami.

## Bramki (fail-closed)
- G1-PRODUCER: werdykt-źródło atrybutów placementu z VA-locked łańcuchem do GRANICY.
- G2-CWO: łańcuch tworzenia statycznego rekordu placementu (creator→setters→attach)
  z diagramem; nieudowodnione krawędzie oznaczone.
- G3-PORTALS: reader znaleziony/nie; struktura .prt + walidacja; rola z dowodem.
- G4-D-FIELD: konsument D rozstrzygnięty lub jawna granica.
- G5-ERA: SHA+mapping+zero transferu PE2.
- G6-GENERALITY: drugi przypadek + negative controls.

## NON-PASS / HARD STOPS
- PRODUCER_UNREACHABLE_STATICALLY (jawna granica), TOOL_BLOCKED, SCOPE_CREEP.
- HARD STOPS: runtime/sieć/mock; modyfikacja oryginałów (exe, VFS, BNT — Portals.bnt
  READ-ONLY!); obce runy (GHIDRA_LOCAL skopiowany do 00_CONTROL\GHIDRA_LOCAL tego
  runu — manifests w GHIDRA_LOCAL_MANIFEST_SHA256.csv); pod-agenty.

## Wyjście
D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913\
(00_CONTROL, 01_RAW, 02_ANALYSIS, 03_EVIDENCE, 06_REPORT)
+ commit path-limited docs/audits/... + AUDIT_ENTRYPOINT (+1 wiersz, 0 usunięć) + push.
RAPORT po polsku (7 punktów wg zlecenia).

## Era
EU 9.3.5 (pcg_install, 2008). Wszystkie twierdzenia era-labelled. Zero transferu PE2/2003.
