# R3 EXTERNAL POSTAUDIT NOTICE — addytywny (pliki R3 NIE zmienione)

RUN_ID kontekstu: PE2003_ISO_ARCHIVE_RESOURCE_INSTANCE_PLACEMENT_STATIC_R4_20261025 (publikacja PUB1, 2026-10-25).
Ten plik jest addytywnym powiadomieniem w zamrożonym katalogu R3; żadnemu
plikowi pakietu R3 nie zmieniono ani jednego bajtu.

## Werdykt Desktop postaudytu R3

Zewnętrzny Desktop postaudyt R3
(99_Audits\PE2003_R3_ISO_PAYLOAD_DESKTOP_POSTAUDIT_R1_20261025):
**PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS**. Przyjęte korekty R3-A01..A12
zostały wykonane/zachowane w kampanii R4 — nowy pakiet:
`pe2003/research/PE2003_ISO_ARCHIVE_RESOURCE_INSTANCE_PLACEMENT_STATIC_R4_20261025`
(w tym commicie; seal lokalny 99_Audits\PE2003_ISO_ARCHIVE_RESOURCE_INSTANCE_PLACEMENT_STATIC_R4_20261025).

## Korekty R3-A01..A12 i realizacja w R4 (skrót)

- **A01** (SERVER_DELIVERED_ONLY): obniżone — R4: Download.data
  ("1 PE_PCG.ark") nie ma konsumenta w przypiętym korpusie (census
  ASCII+UTF16LE trzech obrazów, niezależnie potwierdzony), ale capabilityFTP
  (pełny klient FTP WSOCK32) pozostaje zachowane; PE_PCG.ark scoped — nie
  dowodzi zawartości.
- **A02** (adresy 0x413B97/0x41F370): doprecyzowane w R4 — 0x41F370 to etap
  VERIFY (kotwice Models\/Models.ark), ekstrakcja to 0x41D400..0x41E700;
  0x413B97 rozstrzygnięte w M01.
- **A05/A06** (parser NIF end-to-end): naprawiony w R4 jako parser v2
  (jobs/N01, tools/nif_transform_parser_v2.py SHA256
  B71C209BF7A9B1D0AD5F3B150F6F04919135A901BC0D774830F6600CED3762EB):
  51/51 przypadków kontrolnych PASS, regeneracja end-to-end **byte-identical
  z R3** na obu NIF bez ręcznych poprawek (nonunity_scale=0 z generatora).
- **A07** (CSV strict): MODEL_INSTANCE_EDGE_MAP.csv i pozostale CSV pakietu
  R4 strict (role/schema jawne).
- **A09**: w R4 brak LOWER_BOUND — wszystkie denominatory jawne
  (L01 DENOMINATOR.json).
- **A10** (NiTriShapeData 44 = 30+14): odtworzone w R4 (censusy per typ,
  MODEL_INSTANCE_EDGE_MAP.csv).
- **A11/A12** (scoped negatives / zakres ISO): utrzymane jako scoped
  negatives z jawnymi denominatorami (LOCAL_SOURCE_EXHAUSTED=NO; era-label
  wariantów NIF: to nie są warianty przypięte do wydania ISO 5.1.0.0).
- Pozostałe (A03, A04, A08): patrz CORRECTION_DISPOSITION.md pakietu R4
  (pełne mapowanie R3-A01..A12 na wykonane korekty).

Standing naukowy przeniesiony bez zmian: WORLD_XYZ_RECOVERED=NO;
HISTORICAL_PLACEMENT=NOT_ESTABLISHED; SOURCE_SPECIFIC_ISO_MODELS=UNKNOWN
(narrowed); CANONICAL_GATE_EFFECT=NONE; ADVISORY_PENDING_EXTERNAL_POSTAUDIT.
