# QC_F1_CLASSID_PAIRS — reguła manglingu $0 i 4 pary klasa-ID (własny pomiar)

**QC:** pe-master-auditor, INTERNAL_QC, RUN PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913.
**ERA:** EU 9.3.5. Binarium `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`
SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (8015872 B).
Wszystkie VA przez własne mapowanie (qc_core.Bin; sekcje: .text 0x00401000-0x00A75000,
.rdata 0x00A75000-0x00B6C000, .data 0x00B6C000-0x00BA96E4; image base 0x00400000, ASLR OFF).

## 1. Reguła dekodowania manglingu MSVC `$0<value>@` (mechanicznie)

Suffix `$0` + ciąg znaków, w którym **każdy znak koduje jedną nibble** wg mapowania
**A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7, I=8, J=9, K=10, L=11, M=12, N=13, O=14, P=15**;
wartość = złożenie nibble big-endian (pierwszy znak = najbardziej znacząca nibble).
Odczyt mangled name z TD+8 (RTTI TypeDescriptor w .data, łańcuch ASCII zakończony 0x00).

**Kalibracja reguły (census pełny, nie tylko 4 pary):** 36 wystąpień
`.?AV?$ArkObjectClassImpl@V<Klasa>@@$0<suffix>@@@` w obrazie; dla KAŻDEJ z 36 klas:
dekod suffixu == imm32 arg1 wywołania ctor ArkObjectClass (0x0070CF80) w ciele ctora
tej klasy — **36/36 zgodnych, 0 rozbieżności** (QC_F1_CLASSID.json / QC_F1_REGARGS2.json).

## 2. Cztery wymagane pary (własne bajty)

### (a) Surgeon — 20035
- RTTI (własny odczyt z .data): `.?AV?$ArkObjectClassImpl@VArkSurgeonObject@@$0EOED@@@`
  przy vtable 0x00A87034 (TD 0x00B8DD94; zapis vft w ctorze FUN_0073AB60 @0x0073ABDB).
- Dekod: E=4, O=14, E=4, D=3 → **0x4E43 = 20035**.
- imm32 w kodzie rejestracji: `68 43 4E 00 00` **PUSH 0x4E43 @0x0073ABB1**, CALL
  ctor ArkObjectClass @0x0073ABBD (FUN_0073AB60).
- **PARA ZGODNA: $0EOED@ ↔ 0x4E43 (20035).**

### (b) Container — 20030
- RTTI: `.?AV?$ArkObjectClassImpl@VArkParameterContainer@@$0EODO@@@`
  przy vtable 0x00A86FBC (TD 0x00B8DC54; zapis vft w ctorze FUN_0073A0C0 @0x0073A13B).
- Dekod: E=4, O=14, D=3, O=14 → **0x4E3E = 20030**.
- imm32: `68 3E 4E 00 00` **PUSH 0x4E3E @0x0073A111**, CALL @0x0073A11D (FUN_0073A0C0).
  (Uwaga QC: pin „@0x0073A114" w RESEARCH_FINDINGS §2.2 executora wskazuje 4. bajt
  instrukcji PUSH — instrukcja zaczyna się @0x0073A111.)
- **PARA ZGODNA: $0EODO@ ↔ 0x4E3E (20030).**

### (c) RealWorldItem — 20034
- RTTI: `.?AV?$ArkObjectClassImpl@VArkRealWorldItem@@$0EOEC@@@`
  przy vtable 0x00A8701C (TD 0x00B8DD7C; zapis vft w ctorze FUN_0073A940 @0x0073A9BB).
- Dekod: E=4, O=14, E=4, C=2 → **0x4E42 = 20034**.
- imm32: `68 42 4E 00 00` **PUSH 0x4E42 @0x0073A991**, CALL @0x0073A99D (FUN_0073A940).
- **PARA ZGODNA: $0EOEC@ ↔ 0x4E42 (20034).**

### (d) 20006 / 0x4E26 — klasa: **ArkParameterCommon**
- RTTI: `.?AV?$ArkObjectClassImpl@VArkParameterCommon@@$0EOCG@@@`
  przy vtable 0x00A870C4 (TD 0x00B8DD44; zapis vft w ctorze FUN_0073B820 @0x0073B89B).
- Dekod: E=4, O=14, C=2, G=6 → **0x4E26 = 20006**.
- imm32: `68 26 4E 00 00` **PUSH 0x4E26 @0x0073B871**, CALL @0x0073B87D (FUN_0073B820).
- **PARA ZGODNA: $0EOCG@ ↔ 0x4E26 (20006) — ArkParameterCommon.**
- Znaczenie dla F3/SE-2: 0x4E26 (20006) to numeryczne ID KLASY ArkObjectClassImpl
  (rejestracja @0x0073B87D), identycznie jak 20035/20030/20034 — brak pliku 20006.vfs
  NIE mówi nic o źródle zasilania klasy danymi (pliki VFS = kandydat nośnika, nie definicja).

## 3. Pełny census rejestracji (kontekst par)

- Bezpośrednie CALL (E8) → 0x0070CF80 (ctor ArkObjectClass): **55 site'ów** (własny census
  raw po całym .text; identycznie Ghidra isCall).
- Z nich **54** z arg1 = PUSH imm32 z rodziny param-set (0x4E20..0x4E4B, 0x5DC2..0x5DD1;
  każda wartość dokładnie 1×) — pełna lista: QC_F1_REGARGS2.json.
- **1** site (0x007262B7, funkcja 0x00726230) z arg1 = `PUSH 0` — lazy-init singletonu
  klasy bazowej przechowywanego w DAT_00BA51C4 (ID klasy = 0; NOWE ustalenie QC — patrz
  QC_REPORT.md finding QC-1).
- Fabryka 0x0070BF50: 0 bezpośrednich CALL (E8 i Ghidra isCall = 0) — tylko dispatch
  wirtualny slot1.

## 4. Artefakty

- `QC_F1_CLASSID.json` — census 55 call-site'ów, wyodrębnienie imm32, RTTI po vtable
  z ciała każdej funkcji rejestracyjnej, korelacja 36/36.
- `QC_F1_REGARGS2.json` — pełna lista 55 site'ów z klasyfikacją arg1 (54×imm32, 1×PUSH 0).
- `QC_F1_REGARGS3.json` — dumpy regionów 4 par + klasyfikacja arg2.
- `QC_CENSUS_GETTERS.json` — E8/E9 census getterów (808+9=817; 116+1=117).
