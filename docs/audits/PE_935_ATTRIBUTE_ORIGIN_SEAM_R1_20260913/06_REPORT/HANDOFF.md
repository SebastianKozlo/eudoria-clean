# HANDOFF — PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913

**RUN_ID:** PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913
**RUN_CLASS:** LOAD_BEARING | **TRYB:** STATIC-ONLY (klient/Frida/x32dbg/mock/sieć NIE uruchomione)
**ERA:** EU 9.3.5 (pcg_install). Entropia.exe SHA256
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31; templates.vfs
BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77 (S0 PASS).
**Executor:** pe-reconstruction (RESEARCH_FINDINGS.md zachowany verbatim).
**INTERNAL_QC + formalizacja + publikacja:** pe-master-auditor — **QC_PASS**
(0×P0/P1; 2×P2 + 4×P3 klasy dokumentacyjnej; 06_REPORT\QC_REPORT.md;
poprawki: ERRATA_R4 [SE-R4-1..7]; evidence 01_RAW/02_ANALYSIS nietknięte;
GB6 8 pakietów + repeat per-plikowy 1385/1385 IDENTICAL).

**RUN_STATUS: PASS_WITH_BOUNDARY.**

## Odpowiedź na pytanie szwu (jedno zdanie)

Na kanale instancji RUCHOMYCH pozycja przybywa w bajtach KURSORA KOMUNIKATU
(typów 0xB0/0xC6/0xC7 — case'y dispatchera FUN_004B18D0 — oraz 0xB2 —
special-case w Execute FUN_004B2950; **0xB9 NIE deserializuje pozycji**),
FUN_007453D0 czyta z sub-pakietu klucz u32 + wariant u16 + POZYCJĘ vec3 12B +
rotację + wektor-drugi, setter f90 pisze pozycję do rekordu placementu
+8/+0xC/+0x10, ctor kopiuje ją do instancji MovableObject/ClientMovableObject
+0x44..0x4C i klucz (rekord[0]) do +0x74, a insert FUN_00856190 wstawia parę
{klucz=[value+0x74]=rekord[0], instancja} do STLport hash_map@mgr+0x10 —
JEDEN klucz wiąże komunikat, rekord, węzeł i instancję; upstream bajtów
kursora (sieć vs lokalna kolejka) NIEUDOWODNIONY; STATYKI (4508/296445) NIE
objęte tym kanałem; pozycje 296445 NIEODZYSKANE.

## Granice (do następnej rundy)

1. Upstream kursora (UNPROVEN — 2 callerów dispatchera; vtable
   0x00A7C200 = ArkClientPacketExecutor per RTTI QC).
2. Osie/jednostki value+0x44..0x4C (UNRESOLVED — wymaga FUN_0085B6A0 +
   FUN_008599A0).
3. Statyki vs movable (statyki OPEN; kandydaci FUN_00567170/FUN_005B5F90/
   FUN_006CB6F0 bez zmian).
4. [singleton 0x00BA1260+8] = HIPOTEZA „własny klucz awatara".
5. Wiązanie modelu movables (sub-obiekt +0xC0 via FUN_005247C0; string
   tworzenia) — poza szwem.
6. 19 ctor-callers bez setterów (Faza A) — NOT_CHECKED.
7. Bounded negatyw VFS (E8-direct; payloady poza zakresem).

## Następny eksperyment (jeden, STATIC)

Dekod UPSTREAM kursora: enumeracja callerów FUN_004B2950 przez vtable
0x00A7C200 (xrefy danych + rejestracje w CommunicationSubsystem FUN_00419DD0;
dekod ringa FUN_004B1890/FUN_004B1B70 — skąd wpisy {typ,cursor}; rozstrzyga
sieć-vs-lokalna kolejka); równolegle slot3 FUN_0085B6A0 + FUN_008599A0
(osie/jednostki) oraz sub-obiekt +0xC0 (wiązanie modelu movables).

## Struktura pakietu

```
00_CONTROL\  pe_core.py, s0_era_assertion.py, gh1/gh2/gh3_decomp.py,
             t1_value_class.py, t2*(insert-seam: extract/b/c/d), t4/t4b/t6,
             gb6_immutable.py, ghidra_manifest.py, final_selfcheck.py,
             SCRIPT_SHA256.csv, RUN_CONTRACT.md, GHIDRA_LOCAL\ (tylko lokalnie,
             manifesty AT_COPY/FINAL), qc_probe\ (narzędzia QC auditora:
             qc_pe/qc_census/qc_dispatcher/qc_gb6_*/qc_hash_evidence + wyniki
             QC_*.json)
01_RAW\      S0, SELF_CHECK, T1/T2*/T4/T6/GB6*, GH1-GH3 censusy,
             DECOMP\F*.c (112), T*_HEX\*
02_ANALYSIS\ SEAM_FLOW_MAP.md, KEY_MODEL_MATRIX.md (executor; korekty w
             ERRATA_R4 — patrz niżej)
06_REPORT\   RESEARCH_FINDINGS.md (executor, verbatim), REPORT.md (FINAL),
             ERRATA_R4.md (ledger supresji), QC_REPORT.md (auditor),
             STAGE_ACCEPTANCE_GATES.csv (GB1-GB7 + QC-1..QC-8), HANDOFF.md
root\        artifact_index.csv, MANIFEST_SHA256.csv (closure)
```

## Wykaz poprawek formalizacyjnych (auditor)

- **ERRATA_R4 [SE-R4-1]:** twierdzenie rundy-1 „komunikat 0xB9 niesie KLUCZE,
  nie transformy" — ZATRZYMANE dla typu 0xB9 (własne bajty: pełna konsumpcja
  handlera, brak call do procesora placementu); uogólnienie rodzinne
  („kontrprzykładu transform→+0x08 nie znaleziono") — SUPERSEDED: typy siostrane
  0xB0/0xC6/0xC7/0xB2 deserializują pozycję PROSTO do +8..0x10; upstream
  kursora NIEUDOWODNIONY (nie ogłaszamy „z sieci").
- **[SE-R4-2]:** wartość mapy = instancja MovableObject/ClientMovableObject
  (RTTI własne) — RECEIVER_UNRESOLVED #1 Fazy A zamknięte.
- **[SE-R4-3]:** klucz mapy = uchwyt instancji z komunikatu (rekord[0]); nie
  class-ID/param-set/0x6A4.
- **[SE-R4-4]:** receiverzy gettera D w driverze rozstrzygnięci per-site
  (arg3-rekord @0x00567D16/D46; this-kolejka @0x00567F72).
- **[SE-R4-5]/[SE-R4-6]:** korekty raportu run-B (zbiór typów: 0xB2 nie 0xB9;
  pola: pozycja→rec+0x38 przez FUN_00412430, wariant→u16@+0x34; wektor-drugi
  @+0x50..0x58: X2→placement+4/nazwa, Z2→slot5→+0x98).
- **[SE-R4-7]:** P3 — DIV (nie IDIV); piny kontekstowe; slot5=+0x98;
  null-guard insertu (obserwacja).

## Kwalifikacje dla PE-MASTER (loop audit)

- NIE ogłoszono STATIC_INSTANCE_MECHANISM_CONFIRMED ani źródła placementu
  statyków; pozycje 296445 NIEODZYSKANE; D@4508=124.941
  ANCHORS_ABSENT_SEMANTICS_OPEN bez zmian.
- Rezultat dotyczy JAWNE kanału instancji ruchomych (MovableObject) —
  przeniesienie na statyki wymaga osobnej rundy (granica §3).
- Evidence executora: hash-przed==hash-po (QC_HASH_before/after.json);
  manifest closure pokrywa wszystkie pliki publikowane.
