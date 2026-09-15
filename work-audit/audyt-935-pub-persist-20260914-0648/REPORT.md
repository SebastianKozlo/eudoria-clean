# WORK-AUDIT REPORT — audyt-935-pub-persist-20260914-0648
# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-pub-persist-20260914-0648) — plik audytora, NIE jest częścią pracy wykonawcy

PRZEDMIOT: publikacja + twierdzenia PE_MASTER_REVIEW dla runu
  PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 (BASE e30f99f -> commit 6465019,
  180 sciezek, STATIC-ONLY) oraz pastowany komunikat sesji PE-MASTER (rekonsens po zawieszonej sesji).
  Audytowno 2026-09-14 06:48-08:30, wlasnymi narzedziami, izolacja pelna (zero zapisow poza tym katalogiem).

WERDYKT: **POTWIERDZONY CAŁKOWICIE** (z 3 notami P3 klasu dokumentacyjnego w warstwie QC/kontraktu,
  zaden nie dotyka twierdzenia nosnego; + 1 nota ewolucji HEAD po komunikacie).

## MACIERZ TWIERDZEŃ
Pelna macierz: 01_TWIERDZENIA.md (57 pozycji). Esencja:
- TWIERDZENIA wykonawcy/mastera: patrz pastowany PE_MASTER_REVIEW + komunikat commita 6465019.
- DOWODY z dysku: wszystkie cytowane SHA/VA/byte-piny istnieja i zostaly przeze mnie odczytane.
- MOJA WERYFIKACJA: wlasny parser PE + wlasne disassembly (capstone 5.0.7, zainstalowany do katalogu audytu),
  wlasna rekomputacja composite G7 (niezalezna implementacja), wlasne censusy, wlasne tally JSON-ow,
  wlasne diffe .pre, wlasne pomiary offsetow UTF-8, wlasny import-walk, wlasny RTTI-walk.
- STATUS: 53 POTWIERDZONE, 3 CZESCIOWO POTWIERDZONE (nr 1 z nota ewolucji; nr 20 snapshot pre-refresh;
  nr 51 cytat "[[]]"), 0 ODRZUCONE, NIESPRAWDZONE — patrz sekcja nizej.

## FINDINGS (posortowane wg wagi)

**[P3-1] QC_AUDIT_R1 §5 — błędna tabela sekcji PE.**
- Twierdzenie: "5 sekcji (.text RVA 0x1000/Raw 0x1000/VSize 0x676205; .rdata RVA 0x676000/Raw 0x676000; …)".
- Fakty (moj parser + S0_ERA_ASSERTION.json wykonawcy): .text VSZ = **0x6735E5**, .rdata RVA/Raw = **0x675000**.
- Wplyw: ZEROWY na wyniki — Raw==RVA w obu odczytach, wszystkie piny VA->offset wypadaja identycznie
  (potwierdzone ~50 wlasnymi odczytami bajtow); wlasny S0 runu zawiera poprawne wartosci.
- Do poprawienia (wykonawca, nie ja): transkrypcja sekcji w QC_AUDIT_R1 §5.

**[P3-2] RUN_CONTRACT §14 — zla sciezka RESEARCH_FINDINGS.md.**
- Twierdzenie: tabela identycznosci "…/02_ANALYSIS/RESEARCH_FINDINGS.md | 9F24A747…".
- Fakty: plik istnieje pod **06_REPORT/**RESEARCH_FINDINGS.md (repo @e30f99f i lokalnie); SHA 9F24A747… **zgodny co do bajta**.
- Wplyw: brak (SHA i tresc poprawne); ten sam blad sciezki widac w ERRATA_R5_QUOTES published_match (repo-path-missing).
- Do poprawienia: kolumna sciezki w tabeli §14 (dokument formalizatora, nie evidence runu).

**[P3-3] QC_AUDIT_R1 §8.2 — cytat "[[]]" nie jest doslowny.**
- Twierdzenie: "P2_CENSUS2.json = `[[]]` (2 bajty)".
- Fakty: zawartosc = **`[]`** (2 bajty — rozmiar sie zgadza, doslowny cytat nie).
- Wplyw: brak (dysklosura uczciwa tak samo; plik nie jest nosny).
- Do poprawienia: doslowny cytat w §8.2.

**[NOTA] PERSISTENCE_CHECK "6465019 == HEAD == origin == ls-remote".**
- Prawdziwe w chwili publikacji. Obecnie HEAD = **1a490ee** (popublikowany nastepny run
  PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 — wlasciwie wykonany NEXT_EXPERIMENT z HANDOFF).
- Audytowana tresc 6465019: nietknieta (diff pakietu 6465019..HEAD = pusty; edycja wiersza 31/32
  entrypointu nietknieta, stare 0/0/0 / nowe 1/1/1 takze na HEAD); 6465019 osiagalny z origin/master.
- Ewolucja stanu, nie sprzecznosc komunikatu.

## POTWIERDZONE UCZCIWIE (wykaz najmocniejszych, z sposobem weryfikacji)

1. **G7 composite A606CF52… (1022 pliki)** — niezalezna rekomputacja wlasna implementacja:
   preorder DFS + sortowanie code-point (Ordinal); EXACT dopasowanie do zapisanej wartosci; dodatkowo
   zywy odczyt dzisiejszy == wartosc z czasow runu => oryginaly i 8 pakietow historycznych byte-identical.
   (Lekcja wlasna: kulturowe sortowanie/CP1252 daja zle composite — QC_AUDIT_R1 §3 opisuje te sama puenta.)
2. **Censusy 104/15/14/14** — wlasny linear sweep capstone (skipdata); lista 15 call-site'ow
   FUN_00853A80 VA-po-VA == REPORT; 9x WAVES @0x48C05B..0x48C2B7. Silniej niz master (2 fizyczne + 13 census-level).
3. **Tabela x87 21/21** — wlasna re-derivacja IEEE-754 FCOM: flagi C0/C2/C3, TEST AH,0x41=C0|C3,
   zprime-bity, bits<->value 42/42; NaN(h)->z'=z (dywergencja od Math.max), z=-0,h=+0 -> 0x80000000.
4. **~50 bajtowych pinow** — wszystkie PASS wlasnym odczytem: T-26 FSTP @0x004C478A, EXISTING FSTP
   @0x0085B439 + discard @0x0085B43F, krok 0x3FB99999A0000000, guard 2/3/6/5/4/7, thunki+IAT,
   0x00413340 nie-start, vtable-writes (0x538BA9/BAF, 0x85B1C1, 0x509366), FUN_005094C0 value-copy,
   fallbacki/stale, epilogi D-3, cell-formula, FCHS, 6x FCOMPP, MOV [EBX+0x4C],EAX @0x85536D.
5. **NOWE ODKRYCIE runu (EXISTING bez bramki)** — wlasne disassembly okna 0x85B3E0-0x85B460:
   korekta z' @0x85B426-0x85B43F bez jakiejkolwiek bramki wariantu; pierwszy CMP [EDI+8],3 @0x0085B451
   PO zapisie z'. Potwierdzone bajtowo — twierdzenie nosne runu STOI.
6. **RTTI 7/7** — wlasny chod vtable->COL->TD->nazwa (identyczne wartosci jak w REVIEW).
7. **Manifest 177/177** — re-hash wlasny; brak self-row; pokrycie 179=177+2; artifact_index 177/177
   (hash+rozmiar); man==ai zbiory identyczne; SCRIPT_SHA256 20/20.
8. **Entrypoint row-31 edit** — stare fragmenty 0/0/0 / nowe dokladnie-raz w committed blob 6465019
   i na HEAD; offsety 1679/3594/3818 EXACT (wlasny odczyt UTF-8; wczesniejszy moj blad CP1252 skorygowany).
9. **Poprawki A-F** — diffe .pre: DOKLADNIE linie {102,153} / {16,69,70,71+nowa 72} / {10+2 nowe};
   hashe pre/post == AMEND_LOG 6/6; remnanty starych pinow = 0; ERRATA_R5 capstone 5.0.7 bez remnantu.
10. **GHIDRA_LOCAL** — FINAL 10/10 vs dysk (re-hash db.73/74 po ~180 MB kazdy); at_copy == FINAL
   zrodla fazy B 10/10; 11 plikow local-only = GHIDRA_LOCAL(10)+pycache(1) zgodnie z deklaracja LOCAL-ONLY.
11. **LIVE_SCAN 41/18/0 (59, 17 sond)** — wlasny tally JSON-a; grep-y fragmentow T-08/T-16/D-4 = 0 na repo.
12. **Werdykt integrity** — PE_MASTER_REVIEW committed == kopia lokalna (SHA 3FEDD65A); AUDYT.md ==
   Desktop REPORT.md (C4C87C2B); D-1 window == independent_hexdumps.txt:69 == wlasne bajty EXE; kontrakt
   SHA BAB59EEC; tozsamosci §14 12/12 SHA; S0 17/17; G7 before==after (9FB8BCE0).
13. **Stan otoczenia** — PE_CURRENT_CHECKPOINT przestarzaly (2026-09-01) POTWIERDZONY; loop-state
   89968363 RUNNING_UNATTENDED / stop_reason=null / nietkniety-od-06.09 POTWIERDZONY; drzewo czyste
   poza ?? experiments/; 03_EVIDENCE lokalnie puste (0 plikow).

## NIESPRAWDZONE (uczciwie)
- Porty 8000/9350 "bez ingerencji" — stan historyczny procesow, nieodtwarzalny z dysku.
- Wewnetrzne liczby pakietu Desktop (T6 64/64, VFS 5438/0 CRC, 1385/1385, manifesty 129+210) — warstwa
  historyczna, przedmiot adjudykacji F1-F3 (ktora potwierdzilem na poziomie bajtow EXE).
- Snapshot manifestu pre-refresh (171 wierszy, 168+3) — zastapiony przez refresh STEP 4; mechanizm
  potwierdzony posrednio (hashe pre/post == AMEND_LOG; 171+3+3=177), samego snapshotu nie da sie odtworzyc.
- Pelny 2-poziomowy census zapisow mgr+0x4C poza potwierdzonym jedynym zapisem @0x85536D (dataflow
  executora nieodtwarzalny jednym bajtem; falsyfikacja odbyla sie w census4/5 runu).
- 67 dekompilatow DECOMP_P2 (warstwa pomocnicza) — nie odczytalem kazdego; censusy je cytujace
  potwierdzilem wlasnymi bajtami na wezlach nosnych.
- Pelne ciala WAVES 9x, FUN_00936C30/00936D50 (glowy/cell-formula potwierdzone), FUN_0093F710,
  19 ctor-callers, pisarz mgr3+0 (stan-1) — deklarowane granice runu; utrzymane jako granice.
- Pozycja rekordu 4508 w templates.vfs (D@4508) — arytmetka f32 potwierdzona; parsowanie VFS
  przeniesione z faz A/B, nie re-derivowane w tym audycie.

## CO CZYTAŁEM (FULL_READ_LOG)
PELNA LEKTURA (od poczatku do konca): REPORT.md (287), ERRATA_R5.md (258), PE_MASTER_REVIEW.md (41),
QC_AUDIT_R1.md (122), QC_REPORT.md (54), HANDOFF.md (77), AMEND_LOG_R1.md (81), RUN_CONTRACT.md (776/776),
SOURCE_IDENTITIES.json (71), ENTRYPOINT_ROW_DRAFT.md (24), RESEARCH_FINDINGS_WORKING.md (64),
STAGE_ACCEPTANCE_GATES.csv (8 bramek), SCRIPT_SHA256.csv (28 wierszy), MANIFEST_SHA256.csv (177 wierszy,
re-hash), artifact_index.csv (177, re-hash), GHIDRA_LOCAL_MANIFEST_at_copy/final (10+10, re-hash),
g7_census.py (80), errata_live_scan.py (naglowek+KEYS), f1_model_decoder_suite.py (liczba linii 355 = claim),
S0_ERA_ASSERTION.json, IMPORT_RESOLUTION.json, DECODE_INDEX.json, F1_MASK_SUITE.json, F2_X87_TABLE.json,
F1_CONSUMER_CENSUS.json, P2_CENSUS.json/2/4/5, ERRATA_LIVE_SCAN.json (tally), ERRATA_R5_QUOTES.json (struktura
+ spot-checky), X004C4770_479F_D1_WINDOW.txt, F0085B3E0_SET_POS_EXISTING_FULL.txt (l.33-36 + okno 0x85B3E0-85B460),
AUDIT_ENTRYPOINT.md (wiersz 31/32 + kontekst tabeli na 3 rewizjach blobow), PE_MASTER_LOOP_STATE.json,
PE_CURRENT_CHECKPOINT.md (naglowek), Desktop AUDYT.md:55 + independent_hexdumps.txt:69 (wycinki celowe).
PRZEGREPANE: remnanty starych pinow (0 trafien), sciezki RESEARCH_FINDINGS, loop-state ( przeszukanie katalogow).
NIESPRAWDZONE: patrz sekcja NIESPRAWDZONE.

## KROKI PO CZŁOWIEKA
1. Poprawki P3 (opcjonalne, moze byc jeden dispatch do pe-master-auditor):
   a) QC_AUDIT_R1 §5: tabela sekcji PE (.text VSZ 0x6735E5, .rdata RVA/Raw 0x675000);
   b) RUN_CONTRACT §14: sciezka RESEARCH_FINDINGS.md -> 06_REPORT/;
   c) QC_AUDIT_R1 §8.2: "[[]]" -> "[]".
   Uwaga: (a)/(c) dotycza opublikowanych plikow pakietu — edycja wymaga nowego dispatchu i
   nowelizacji przez publikatora wg obowiazujacego procesu (nie "w locie").
2. Stan "wiszacej sesji" = zamkniety slusznie: praca opublikowana, zweryfikowana, nic nie utracono.
   Claim "publikacja zamknieta" = PRAWDZIWA (z nota: HEAD od tego czasu posunal sie o nastepny run
   PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 — wlasciwie GO z NEXT_EXPERIMENT, juz wykonane).
3. Aby unikac dual-mowiennych statusow w komunikatach: rozrozniaj "PERSISTENCE_CHECK w chwili T"
   od "stan biezacy" (HEAD mutuje sie z kazdym runem).
4. Kontynuacja toru EU935: nastepne ogniwo (wg HANDOFF nowego runu SceneFeeder) = SF+0x30 link identity
   + vtable slot-17 decode (CANDIDATE_MODEL_BRIDGE) — poza zakresem tego audytu.

## PODSUMOWANIE LICZB
Twierdzen w macierzy: 57; POTWIERDZONE: 53; CZESCIOWO POTWIERDZONE: 3 (nr 1 nota ewolucji, nr 20 snapshot,
nr 51 cytat); ODRZUCONE: 0; NIESPRAWDZONE: granice wyliczone wyzej (zawsze z powodem).
FINDINGS: 0xP0, 0xP1, 0xP2, 3xP3 (+1 nota). Zero defektow w nosnej warstwie dowodowej.
