# HANDOFF — PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913

- **AUDIT_OUTPUT_ROOT** = `D:\Eudoria_Reconstruction\99_Audits\PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913\`
  (publikacja repo: `docs/audits/PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913\`)
- **FINAL_REPORT_PATH** = `06_REPORT\00_FINAL_REPORT.md`
- **ERRATA_PATH** = `06_REPORT\ERRATA_R2.md` ([E-1..E-6]; cytaty zastępowane 1×; G3 PASS)
- **PRIMARY_EVIDENCE_PATHS** =
  - `01_RAW\Z2_JOIN_RESULT.json` (pełny wynik join z mianownikami + kontrole + endianness + NC)
  - `01_RAW\Z2_JOIN_A_TO_NIF_DETAIL.csv` (3,618 wierszy per unikalne A) / `Z2_JOIN_B_TO_BVI_DETAIL.csv` (1,666)
  - `01_RAW\Z2_NEGATIVE_CONTROL_A.csv` (20 syntetycznych A+1,000,000 — wszystkie nieobecne)
  - `01_RAW\Z2_MODELS_BNT_INDEX_NAMES.csv` (5,596) / `Z2_VOLUMES_BNT_INDEX_NAMES.csv` (1,865) — metadane indeksów
  - `02_ANALYSIS\Z1_CLAIMS_MATRIX.md` (macierz A–E z dowodami)
  - `03_EVIDENCE\Z2C_INDEPENDENT_SPOTCHECK.json` (niezależny surowy byte-scan)
  - `03_EVIDENCE\Z3_QUANTIFIER_CENSUS.csv` (32 wiersze: plik/linia/fraza/ocena) + RAW + 2×JSON
  - `06_REPORT\GATE_CHECKS.json` (maszynowa weryfikacja G1–G4)
  - `00_CONTROL\z2_join_a_models.py` (+`z2c`, `z3`, `z3b`, `z4`) — piny SHA w `Z2_SCRIPT_SHA256.txt`
- **RUN_STATUS** = COMPLETE (audyt + join + census + errata + publikacja; wszystkie bramki PASS)
- **HARD_STOP_REASON** = NONE

## Wyniki bramek

- **G1-JOIN: PASS** — rekomputacja z zapisanych artefaktów zgodna (3,618/0; per-record 5,438;
  BONUS 1,666/1,692; tożsamości arytmetyczne trzymają); round-trip endianness 0 fail; NC 20/20
  absent; niezależny byte-scan PASS; census surowy ".nif\n"=5,596 i ".bvi\n"=1,865 == parser.
- **G2-CENSUS: PASS** — 32 wiersze maszynowe z ocenami (0 UNASSIGNED), CSV↔JSON zgodne.
- **G3-ERRATA: PASS** — frazy zastępowane obecne dokładnie 1× w ERRATA_R2 (cytaty), 0× w
  poprawionej narracji; [E-1..E-6] oznaczone. Ujawnienie: iteracja 1 wykryła duplikat frazy w
  nagłówku [E-4] — naprawione (FAIL→PASS).
- **G4-IMMUTABLE: PASS** — 674/674 plików pakietu R1 (obie kopie) przed/po identycznych.
- **G5-GIT: PASS** — commit path-limited (repo: `docs/audits/PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913\`
  + 1 plik AUDIT_ENTRYPOINT.md); census ścieżek == dozwolone; push OK; HEAD == origin/master
  (werdykt commitu: SHA do odczytania `git log -1 -- docs/audits/PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913/`).
- **G6-ENTRYPOINT: PASS** — dokładnie +1 wiersz, 0 usunięć (numstat 1/0).

## WYNIK JOIN (liczby z mianownikami)

- total T: **5,438** rekordów template (własny walk 5,438/5,438 do EOF, 0 CRC-fail; zgodność
  per-row z S2 R1: IDENTYCZNA); unikalne T: **5,438** (0 duplikatów id)
- unikalne A (niezerowe): **3,618**; **A==0: 0 rekordów** (pole A nie przyjmuje zera w korpusie)
- Models.bnt: **5,596** wpisów `<id>.nif` (0 duplikatów nazw; zakres [53..592,853])
- **JOIN A→`<A>.nif`: 3,618 trafień / 0 braków / wielokrotne w tym kierunku niemożliwe** (0
  duplikatów nazw; 253 wartości A dzielonych przez >1 template); per-record **5,438/5,438**
- A poza zakresem nazw: **0** (max A == max id .nif = 592,853; dziedzina A ⊆ dziedzina id .nif)
- **BONUS B→`<B>.bvi`**: **1,666/1,666** unikalnych niezerowych B (per-record 1,692/1,692;
  rekordów B==0: 3,746; Volumes.bnt 1,865 wpisów; 199 .bvi niereferencjonowanych; 1,978 .nif
  niereferencjonowanych — nadzbiory, spodziewane)
- kontrole: NC 20/20; endianness round-trip 0 fail + kotwica surowa 4508 (fd 85 04 00 → LE
  296445) + kontrola dyskryminatywna BE (1/3,618, palindrom A=592128 — zbieg); niezależny
  surowy byte-scan: pozytywy 8/8 + 5/5 (każdy dokładnie 1×), negatywy 0

## Werdykt twierdzenia C

**PEŁNE ODWZOROWANIE (FULL_MAPPING)** — CONFIRMED z pełnym censusem (era EU 9.3.5 pcg_install;
mapowanie statyczne danych; „odpowiednie A" = wszystkie niezerowe A; bez dekodowania payloadów).

## Macierz twierdzeń A–E

| | status |
|---|---|
| A | **CONFIRMED** (przepływ statyczny VA-locked do żądania {0x66,id}; kwalifikacja STATIC-ONLY) |
| B | **CONFIRMED** (byte-proof, scope: sprawdzone przypadki) |
| C | **CONFIRMED** (przez Z2: pełny join, nowy pomiar) |
| D | **REJECTED as worded** (do żądania = CONFIRMED; fizyczne otwarcie = STRONGLY_SUPPORTED, nie instruction-closed; residuum = ciała providera/fabryki) |
| E | **UNVERIFIED** (transform-source nieosiągnięty; hipotezy H_CLIENT/H2/H_SERVER/H4 otwarte) |

## Census — overclaimi (lista)

- [E-1] FINAL_REPORT §0 L16 (frazа o pełnym zakotwiczeniu mechanizmu) — warstwa główna
- [E-3] C_transform_source_and_D_placement.md C.4 L46 (nieudowodniona konieczność modalna +
  kolejność network-first) — warstwa główna
- [E-6] PE_MASTER_REVIEW.md L9 (fraza cytowana przez audyt zewnętrzny Finding A) — warstwa AUX
- plus [E-2]: 9 fraz indykatywnych (statyczne-vs-runtime; 7 główna + 2 AUX) — NEEDS_QUALIFICATION

## Publikacja

- COMMIT: path-limited `docs/audits/PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913/` (pełny
  pakiet: 00_CONTROL/01_RAW/02_ANALYSIS/03_EVIDENCE/06_REPORT) + `AUDIT_ENTRYPOINT.md` (+1 wiersz);
  SHA: `git log -1 -- docs/audits/PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913/`; HEAD==origin/master
  zweryfikowane po push; brak payloadów oryginałów (wyłącznie metadane nazw/offsetów).

## Granice / NOT_CHECKED (jawne)

Re-forensyka VA R1 nie była powtarzana (zaufanie: fresh QC R1 6/6+~40 + wyrywkowe reodczyty
dumpów: S6/S11/S20 — zgodne); dekompilacja ciał providera/fabryki (open item R1) — niewykonana;
sekcja E/transform — UNVERIFIED; payloady .nif/.bvi — niedekodowane (zakaz); pełna re-lektura
wszystkich 468 dumpów R1 — niewykonana (census + 4 pełne odczyty w tym runie); PE_MASTER_REVIEW.md
tego runu = PLACEHOLDER PENDING — werdykt MASTER_* orzeka PE-MASTER (audytor nie podpisuje).
