# QC_R3_REPORT — FRESH INDEPENDENT QC ROUND 3 (DESKTOP_CORRECTION_R1)

- RUN_ID (QC round) = PE_935_20002_PAYLOAD30_QC_R3_DESKTOP_CORRECTION_20261002 (fresh-context
  pe-master-auditor QC session; PE-MASTER direct dispatch; NO_NESTED_TASKS)
- TARGET = the focused correction PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002 of the
  package PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002
- GOVERNING CONTRACT = 00_CONTROL\DESKTOP_CORRECTION_R1\CORRECTION_RUN_CONTRACT.md
  (SHA256 1E592EBC056FD4110EB8151C92872DDBEF744755FF3AAB50C1A87CAFFABFE557, 21,076 B —
  re-verified at QC start: MATCH)
- BASE_SHA = 9203b6d1ad5025f4158d5165863594132aaac49f (HEAD re-verified: MATCH, branch master)
- Pinned inputs re-hashed by this QC with its OWN tools (no executor code):
  Entropia.exe 8,015,872 B / E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 MATCH;
  20002.vfs 174,864 B / C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4 MATCH;
  starting manifest 06_REPORT\MANIFEST_SHA256.csv 50,698 B / CD938AD7C05C41A62B5847057A92EBF12C0B1890964AEC0ADCDA0F87ECE1E4BF MATCH (byte-unchanged by the executor).
- QC WRITE SCOPE = ONLY 04_QC\QC_R3_DESKTOP_CORRECTION\ (+ its qc_tools\); nothing else touched;
  no executor evidence altered; no commits/staging/push; no runtime execution (STATIC-ONLY).
- INDEPENDENCE = this QC wrote its own PE32 parser + own x86-32 decoder + own VFS walker
  (qc_tools\qc3_pe32_x86.py, qc3_q0..q5 scripts); NO executor script was executed or imported.

## VERDICT: **PASS_WITH_FINDINGS**

The correction's load-bearing science is INDEPENDENTLY VERIFIED in full (every pin, the branch
selection, the cursor provenance, the destination, the framing census, the BEFORE-copy discipline,
the identity/history protections). The findings are bounded wording/count residuals in four
document/evidence locations — none load-bearing, all with deterministic one-line dispositions for
the QC-DISPOSITION step (contract §10 step 3) before the persistence phase.

## QC verdict gate predicates (contract §6) — ALL PASS

| Gate predicate (contract §6 "QC must FAIL if...") | Result |
|---|---|
| descriptor non-NULL ignored | NOT THE CASE — my own model + bytes: descriptor+0 = 0x00BA937C (non-NULL, proven from the registration dataflow + factory return); the detector's variant B predicts VIRTUAL; mutant models ignoring non-NULL are DETECTED (M1/M2) |
| fallback selected despite the proven non-NULL descriptor for tag ID 17 | NOT THE CASE — JZ @0x75F66E not taken; tag17 prediction = VIRTUAL 0x009777F0; fallback-predicting mutants DETECTED |
| virtual target not proven (static vtable dword not pinned) | PROVEN — dword @ VA 0x00A9C684 (FO 0x69C684) = F0 77 97 00 = 0x009777F0, read from the physical .rdata by my own parser; RTTI .?AUArkRTTraitsInt@@ confirmed via COL 0x00AB8360 -> TD 0x00B9F10C |
| reader VA/FO wrong | CORRECT — READ VA 0x00977807 / RVA 0x00577807 / FO 0x00577807 / bytes 8B 04 10; STORE VA 0x00977810 / bytes 89 02; error path @0x97781A (dest=0 + flag clear) distinct |
| cursor does not reach +0x30 at the tag-ID-17 iteration for the selected reader | REACHED — offset == 0x30 at the tag-17 VALUE read in 1366/1366 records (own walk); record 0 raw BB2E0000=11963; record 1014 raw 00000000=0 |
| destination is not slot 21 | PROVEN — field index = tag+4 = 0x15 = 21 (@0x70CBF6/@0x75F5D7/@0x726A0E); dest = value_array+21*4 = +0x54 (LEA @0x726A14); width 4 (store @0x00977810) |
| A/B/C PATH-SELECTION CHANGE detection (contract §6 MANDATORY) | DEMONSTRATED (see the A/B/C table; all 3 mutant models DETECTED; NULL treated as LEGAL fallback input, not invalid input) |

## FINDINGS

### P2-1 — Rezydualne, wzajemnie sprzeczne cyfry liczby plików CURRENT w 2 lokalizacjach poprawionego stanu

- **Defekt**: 06_REPORT\HANDOFF.md, linia 90 ("Historical delivery counts..." akapit, klauzula
  końcowa): *"the CURRENT count is the **418** above"* — sprzeczne z linią 74 TEGO SAMEGO pliku
  ("CURRENT PHYSICAL FILE COUNT: **420** files on disk") oraz 06_REPORT\REPORT.md (L113: 420)
  i 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md §10 (420 = 389 + 31).
  06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md, §7 (wiersz cenzusu wzorca "364 files"):
  *"The CURRENT count (**419**) is freshly measured in REPORT.md and HANDOFF.md"* — REPORT/HANDOFF
  faktycznie podają 420.
- **Dowód przeciwstawny (mój pomiar)**: własny cenzus fizyczny na początku QC (przed moimi
  zapisami) = **420** plików = 389 pre-correction (388 manifest-covered + manifest self-excluded)
  + 31 nowych; skład zgodny co do pliku z raportem executora. Liczby 418/419 to relikty
  pośrednich stanów roboczych (419 = stan przed dodaniem 10. kopii BEFORE VFS_TO_PARSER_TRACE.md;
  418 = stan przed jeszcze jedną pozycją).
- **Skutek**: wewnętrzna niespójność liczby plików w stanie CURRENT; podważa literalne
  wykonanie kontraktu §7 pkt 2/5 ("Freshly measure ... do NOT hard-code", "No ... conflation
  anywhere in the corrected state") i self-check C7/C8 executora (który w miejscach
  autorytatywnych jest poprawny).
- **Nie wpływa** na jakiekolwiek twierdzenie naukowe (branch/cursor/destination/census).
- **Poprawka (dyspozycja)**: jednokrotne słowne poprawienie 2 klauzul w kroku QC DISPOSITION
  (przed finalną persistence): HANDOFF.md L90 "418" -> "420"; AMEND_LOG §7 "(419)" -> "(420)".
  Po poprawce: rewalidacja = grep "CURRENT count" w stanie current — każda wzmianka == 420;
  wynik hash plików zmieni się — musi nastąpić PRZED regeneracją manifestu (§10 krok 10).
  Ewentualnie (wariant minimalny): zakomunikować przez PE-MASTER, że dwie wzmianki boczne są
  znane-stale i mają być naprawione w fazie persistence wraz z §10 krok 5-8 (finalizacja
  REPORT/HANDOFF) — ale wtedy tablica BEFORE/AFTER w AMEND_LOG wymaga rozszerzenia o te edycje.

### P2-2 — Fraza z nazwanej listy §5 ("reads are runtime-tag-driven") przetrwała w 2 klauzulach stanu CURRENT

- **Defekt**: kontrakt §5 nakazuje REPLACE over-broad claims, w tym dokładnie tę frazę. W poprawionym
  stanie pozostały: 06_REPORT\REPORT.md L66: *"the read side is runtime-tag-driven generic
  property machinery"* oraz 06_REPORT\HANDOFF.md (CORRECTED result paragraph, L109):
  *"reads are runtime-tag-driven"*.
- **Łagodzące**: w OBU miejscach bounded wording §5 występuje wprost i bezpośrednio obok
  (REPORT L66: pełny verbatim "Within the inspected 202 direct descriptor-lookup sites ...";
  HANDOFF L109: "no statically-coded tag-0x11 reader was identified within the 202-site
  bounded census"); żadna nieograniczona konkluzja (resolvability/consumer) nie jest wyprowadzana
  z tej frazy w poprawionym tekście; fraza jest zarazem opisem mechanizmu (censused machinery
  jest faktycznie tag-driven — byte-proven), więc ryzyko semantyczne jest niskie.
- **Skutek**: literalna niezgodność wordingowa z §5; self-check executora "§5 bounded consumer
  wording applied verbatim" jest prawdziwy co do obecności verbatim, ale fraza-docelowo-do-
  zastąpienia nie została w pełni usunięta.
- **Poprawka (dyspozycja)**: w kroku QC DISPOSITION przeformułować 2 klauzule, np. REPORT L66:
  "...; the CENSUSED read machinery is runtime-tag-driven (bounded wording below)" lub usunąć
  frazę (bounded wording już ją zastępuje); HANDOFF L109: usunąć klauzulę "; reads are
  runtime-tag-driven" (poprzedzający człon już zawiera scoping). ALBO dyspozycja PE-MASTER:
  uznać za opis mechanizmu (accept as-is) — wtedy finding zamyka się jako ACCEPTED.
- **Rewalidacja**: po poprawce grep "runtime-tag-driven" w 10 skorygowanych dokach: 0 hits
  w sekcjach current (historical section HANDOFF — dozwolona etykietowana obecność).

### P3-1 — Martwy licznik "tag_sequence_ok": 0 w CURSOR_PROOF_CORRECTION_R1.json

- **Defekt**: 03_SCRIPTS\desktop_correction_r1\s4_cursor_walk.py L210 definiuje pole cenzusu
  `"tag_sequence_ok": 0`, które nigdy nie jest inkrementowane w pętli cenzusu — w wyemitowanym
  01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json pole ma wartość 0, którą można
  błędnie odczytać jako "0 rekordów ma poprawną sekwencję tagów".
- **Dowód przeciwstawny (mój pomiar)**: sekwencja tagów [1, 0xC, 0xD, 0xE, 0x10, 0x11] jest
  JEDNOLITA we wszystkich 1366/1366 rekordów (mój niezależny walk, QC_R3_VFS_WALK_RESULT.json
  tag_sequences). Semantycznie zamierzona teza jest PRAWDZIWA; pole jest martwe/mylące.
- **Poprawka (dyspozycja)**: nie zmieniać artefaktu dowodowego (historia); przy ewentualnej
  przyszłej regeneracji usunąć pole lub je inkrementować; QC-R3 utrwala poprawną wartość w
  QC_R3_VFS_WALK_RESULT.json (census.tag_sequences = 1366/1366).

### P3-2 — Dekoratywny charakter pola "match" w części pinów artefaktów korekcyjnych

- **Defekt**: w s4_cursor_walk.py lokalny wrapper `pin()` ustawia `match = True` bezwarunkowo
  (bez porównania expected-vs-original); w BRANCH_SELECTION_TRACE.json większość pinów ma
  `expected_bytes_hex: null`, co czyni `match: true` trywialnym (s2_branch_pins.py: match =
  (expected is None) or (original == expected)).
- **Dowód przeciwstawny**: bajty w polu `original_bytes_hex` pochodzą z FAKTYCZNYCH odczytów
  fizycznego EXE (pe_parse.py czyta raw; brak hardcode) i zostały NIEZALEŻNIE zweryfikowane
  przez ten QC: 185/185 pinów == fizyczne bajty (mój parser). Defekt dotyczy notacji
  proweniencji (pole bez falsifiera), nie danych.
- **Poprawka (dyspozycja)**: notacja dla przyszłych regeneracji: zawsze podawać expected z
  niezależnego źródła albo zmienić nazwę pola (np. "measured_no_expected"); artefakty
  istniejące pozostają (ich treść jest poprawna).

### P3-3 — Obserwacja: napięcie kontraktu §4 vs §10 dla PE_MASTER_REVIEW.md (rozstrzygnięte zgodnie z interpretacją QC)

- Kontrakt §4 wymienia 06_REPORT\PE_MASTER_REVIEW.md w zbiorze korekt, ale §10 krok 7 przypisuje
  FINAL PE_MASTER_REVIEW fazie persistence (pe-master-auditor). Executor NIE ruszył pliku
  (byte-unchanged — potwierdzone: 25,523 B / 811E03E3... == manifest startowy) i wyraźnie
  udokumentował dyspozycję ("persistence-phase domain; NOT touched by the executor") w
  AMEND_LOG §9 i HANDOFF. Zadanie QC (Q6) same potwierdza interpretację "persistence-phase files;
  their supersession comes later". **Bez akcji dla executora**; warunkowe: faza persistence
  MUSI wykonać supersession note (§10 krok 7) przed regeneracją manifestu — PE-MASTER proszony
  o kontrolę tego kroku w dyspozycji.

## Q0 — IDENTITY (PASS)

- Kontrakt: SHA 1E592EBC... (21,076 B) MATCH; HEAD == BASE_SHA MATCH; EXE/VFS/starting-manifest
  wszystkie MATCH (pełne SHAs wyżej).
- 04_QC\QC_R3_DESKTOP_CORRECTION NIE istniał przed QC (stwierdzone przed zapisem).
- Bijection vs manifest startowy (mój własny re-hash wszystkich 388 wierszy):
  **378 identycznych + dokładnie 10 zmienionych + 0 brakujących**. Zmienione = dokładnie lista
  10 skorygowanych doków: FIELD_TO_DESTINATION_TRACE, CONSUMER_TRACE, SEMANTIC_ASSESSMENT,
  NEGATIVE_CONTROLS, DESTINATION_CONSUMER_CENSUS.json, BLAST_RADIUS, VFS_TO_PARSER_TRACE
  (02_ANALYSIS) + REPORT.md, EVIDENCE_INDEX.md, HANDOFF.md (06_REPORT).
- Nowe pliki executora: **31** (3 frozen formalizer control + BEFORE_COPIES_INDEX + 10 BEFORE
  kopii + 5 artefaktów 01_RAW\DESKTOP_CORRECTION_R1 + 11 skryptów + 1 AMEND_LOG) — zgodnie z
  twierdzeniem; dysk = 420 plików fizycznych przed zapisami QC.
- Pliki chronione — wszystkie byte-unchanged: 01_RAW\CLIENT_READ_BYTES.json (3C4CD87F...),
  04_QC\QC_REPORT.md (2D83DE3B...), wszystkie QC1_*/QC_R2_* wyniki + qc_tools (10 plików —
  all_unchanged), 00_CONTROL\RUN_CONTRACT.md (24B3A559...), CONTRACT_FREEZE.json (D0A2A02F...),
  zamrożone pliki kontrolne DESKTOP_CORRECTION_R1 (kontrakt == pinned SHA; freeze JSON spójny),
  PE_MASTER_REVIEW.md (811E03E3...), MANIFEST_SHA256.csv (CD938AD7...).
- Wynik maszynowy: QC_R3_Q0_IDENTITY_RESULT.json.

## Q1 — BRANCH-SELECTION INDEPENDENT RE-DERIVATION (PASS; mój cenzus pinów: 185/185, 0 niezgodnych)

Własny parser PE32 (nagłówki/sekcje odczytane, nie założone; .tls/.rsrc demonstrably różne od
.tożsamości .text/.rdata/.data) + własny dekoder x86-32 (fail-closed na nieznanych opkodach;
okna zdekodowane semantycznie, nie tylko porównaniem bajtów):

- **Cenzus pinów**: 185/185 claimed pins zweryfikowanych (BRANCH_SELECTION_TRACE 96/96;
  FALLBACK_PATH_RECORD 25/25; DESTINATION_PROOF 23/23; CURSOR_PROOF entry+width pins 41/41);
  51/51 asercji semantycznych; extra: slot dwords type-2 (@0xA9C660 = 0x00977840, RTTI
  .?AUArkRTTraitsFloat@@) i type-4 (@0xA79A44 = 0x00409ED0, RTTI .?AURT@?$ArkTraits@VArkMonetary@@@@),
  RTTI selected (.?AUArkRTTraitsInt@@), klasyfikacja BSS-tail obiektu 0x00BA937C (poza raw size
  .data → zero-init przy load; spójne z lazy-init; wartość runtime pochodzi z byte-pinned
  store @0x977A68).
- **Łańcuch (każde ogniwo z fizycznych bajtów, mój dekod)**:
  1. Rejestracja @0x76170F-0x761727: CALL 0x977a50; PUSH EAX(arg5); PUSH 0; PUSH 0xC0; PUSH 1;
     PUSH 0x11(tag 17); MOV ECX,ESI; CALL 0x70cbc0 — potwierdzone bajt po bajcie.
  2. Fabryka FUN_00977a50: TEST byte [0xBA9380],AL; JNE @0x977a7a; OR [0xBA9380],EAX;
     PUSH 0xA744B0; MOV dword [0xBA937C],0xA9C670 (@0x977A68); CALL 0x95d4db; ADD ESP,4;
     MOV EAX,0xBA937C; RET — obie ścieżki wracają 0x00BA937C (non-NULL); brak ścieżki NULL.
  3. FUN_0070cbc0: arg5 @0x70CBE3 (stack 0x28 po SUB 0x10+PUSH ESI); ADD ECX,4 @0x70CBF6
     (field = tag+4 = 0x15); LEA ECX,[ESP+0x18]; CALL 0x75f5c0; PUSH EAX; MOV ECX,ESI;
     CALL 0x70c980; RET 20.
  4. FUN_0075f5c0: MOV EDX,[ESP+8](arg2); MOV EAX,ECX(this=descriptor); MOV ECX,[ESP+0x14](arg5);
     MOV [EAX],ECX @0x75F5CA (*** descriptor+0 = obiekt ***); +4=arg2; MOV ECX,[ESP+4](arg1);
     MOV [EAX+8],ECX @0x75F5D7 (field index); MOV [EAX+0xC],EDX; RET 20.
  5. FUN_0070c980: vector [ESI+0x88]/[ESI+0x8C]; MOV EDX,[EDI+8](field); SUB EDX,4 (=tag);
     SAR EBX,4 (count, stride 0x10); CMP EDX,EBX; JNZ fail (tag==count invariant);
     PUSH EDI; CALL 0x70c7b0 (append: kopiuje 4 dwords, end += 0x10).
  6. Lookup FUN_0070c180 (ścieżka bazowa @0x70C1C0..): SHL EAX,4 @0x70C1D3; ADD EAX,[ECX+0x88]
     @0x70C1D6 — descriptor = classObj->[0x88] + tag*0x10.
  7. Dispatch FUN_0075F660: MOV EAX,ECX; MOV ECX,[EAX] @0x75F662; TEST ECX,ECX @0x75F664;
     PUSH EBX/ESI; MOV ESI,[ESP+0xc](arg1=cursor); MOV BL,1; JE 0x75F687 @0x75F66E (fallback);
     virtual: MOV EDX,[ESP+0x10](arg2=dest) @0x75F670; MOV EAX,[ECX](vtable) @0x75F674;
     MOV EAX,[EAX+0x14](slot) @0x75F676; PUSH EDX @0x75F679; PUSH ESI; CALL EAX @0x75F67B;
     MOV AL,[ESI+0x11]; RET 8. Fallback @0x75F687: TEST byte [EAX+0xC],1; MOV EAX,[EAX+4];
     JE → CALL 0x412d80 / CALL 0x4129c0 (rodzina fallback).
  8. Vtable dword: @VA 0x00A9C684 (FO 0x69C684) = F0 77 97 00 = 0x009777F0; RTTI:
     [vtable-4]=0xAB8360 (COL); COL+0xC=0xB9F10C (TD); nazwa .?AUArkRTTraitsInt@@.
  9. Reader FUN_009777F0: MOV ECX,[ESP+4](cursor); CMP byte [ECX+0x11],0 @0x9777F4; JE error;
     MOV EAX,[ECX+0xC](offset); LEA EDX,[EAX+4] @0x9777FD; CMP EDX,[ECX+8]; JA error;
     MOV EDX,[ECX](base); MOV EAX,[EAX+EDX] @0x977807 (8B 04 10) — THE READ;
     MOV EDX,[ESP+8] @0x97780A (dest=arg2); PUSH 4; MOV [EDX],EAX @0x977810 (89 02) — THE STORE;
     CALL 0x40de60 @0x977812 (advance 4); RET 8; error @0x97781A: MOV EAX,[ESP+8]; MOV [EAX],0
     (dest=0); CMP/[clear] byte [ECX+0x11] (flag clear); RET 8 — odrębna ścieżka błędu.
  10. Fallback FUN_00412540 (NIE-wybrany): CMP byte [ECX+0x11],0; JE 0x412569; MOV EAX,[ECX+0xC];
      LEA EDX,[EAX+4]; CMP EDX,[ECX+8]; JA 0x412569; MOV EDX,[ECX]; MOV EAX,[EAX+EDX]
      @0x00412553 (8B 04 10); MOV EDX,[ESP+4]; MOV [EDX],EAX @0x0041255A (89 02);
      MOV [ESP+4],4; JMP 0x40de60 — bajtowo poprawny, warunek reachability = descriptor+0==NULL
      (JZ @0x75F66E), NIESPEŁNIONY dla tag 17. Poprawione offsety FO 0x12553/0x1255A; stara
      transkrypcja 0x00125553 = digit-shift (superseded — spójnie odnotowane).
  11. Destination chain: 0x726A0E (MOV ECX,[EAX+8] — field=21); 0x726A11 (MOV EDX,[EBP+0x40] —
      value_array, EBP=instance bo FUN_00726900 MOV EBP,ECX); 0x726A14 (LEA ECX,[EDX+ECX*4] =
      +0x54); PUSH ECX/PUSH ESI/MOV ECX,EAX/CALL 0x75f660; 0x70D9B8 (SAR ECX,4) + 0x70D9BB
      (ADD ECX,4 = count+4) + 0x70D9BF (LEA EDI,[EBX+0x40]) + CALL 0x412c50 — 22 sloty.
  12. Cursor chain: 0x70DDA2-0x70DDA8 (PUSH 8; LEA ECX,&cursor; CALL 0x40de60 — advance-8 po
      bounds offset+8<=limit @0x70DD95-0x70DDA0); FUN_00409ed0 → FUN_004099c0 (tag 1: dwa
      dwordy, LEA [EDX+8], advance 8 — width 8); FUN_00977840 (tag 0xC: FLD/FSTP dword,
      advance 4 — width 4); FUN_0040de60 (ADD [ECX+0xC],EAX; CMP [ECX+8]; clear [ECX+0x11]
      przy overrun — layout kursora +0=base/+8=limit/+0xC=offset/+0x11=flag).
- Wynik maszynowy: QC_R3_PINVERIFY_RESULT.json (pełne okna semantyczne z mojego dekodera).

## Q2 — DISCRIMINATING BRANCH-SELECTION DETECTOR (contract §6 MANDATORY) — PASS

Wykonawcza reimplementacja (moja własna, z mojego dekodu) control flow FUN_0075F660 +
dataflowu deskryptora, sterowana STATYCZNYMI bajtami (slot dword czytany z fizycznego EXE;
wartość vtable 0x00A9C670 z byte-pinned store @0x977A68):

| Wariant | descriptor+0 | vtable/slot | Przewidywana ścieżka | Przewidywany cel | Oczekiwane | Zgodne |
|---|---|---|---|---|---|---|
| **A** | NULL | n/a (JZ taken) | FALLBACK | 0x004129C0 (flags 0xC0 & 1 == 0 → scalar) | FALLBACK (FUN_00412d80/FUN_004129c0 family) | TAK (NULL = LEGALNY input → fallback) |
| **B** | 0x00BA937C (proven non-NULL) | 0x00A9C670 → slot dword @0xA9C684 = 0x009777F0 | VIRTUAL | 0x009777F0 (FUN_009777F0) | VIRTUAL = static slot dword | TAK |
| **C** | 0x00BA937C | synthetic slot = 0x00412540 | VIRTUAL | 0x00412540 (ZMIENIONY cel) | target MUSI śledzić wartość slotu | TAK (B→C target CHANGE wykryty) |

Dyskryminacja (detektor MUSI wykryć wadliwe modele — wykryte wszystkie 3):
- M1 (ignoruje non-NULL → zawsze fallback): przewidywał FALLBACK dla B → **DETECTED-SELECTION-ERROR**
- M2 (fallback mimo non-NULL): przewidywał FALLBACK 0x4129C0 dla B → **DETECTED-SELECTION-ERROR**
- M3 (cel virtual hard-coded, nie z slotu): dla C nie śledził syntetycznego slotu
  (0x9777F0 zamiast 0x412540) → **DETECTED-TARGET-NOT-DERIVED-FROM-SLOT**
- NULL-is-legal-input: TAK (wariant A = poprawny wybór fallback; detektor NIE traktuje NULL
  jako invalid input — zgodnie z ostrzeżeniem kontraktu §6).
- Tożsamość vtable obiektu readera (ze statycznych bajtów): runtime [0x00BA937C] = 0x00A9C670
  (z byte-pinned store); slot +0x14 = dword @0x00A9C684 = 0x009777F0; RTTI .?AUArkRTTraitsInt@@ — TAK.
- Wynik maszynowy: QC_R3_BRANCH_MODEL_RESULT.json (verdict PASS, failed predicates: []).

## Q3 — CURSOR + DESTINATION RE-DERIVATION (PASS; 20/20 checków)

Własna re-derivation framingu z surowych bajtów (bez kopiowania modelu executora):
magic "ArkVFS02" + dword 0x80 @offset 8; **16-bajtowy global header + 1366 rekordów × stride 128
= 174,864 B — EXACT EOF (leftover 0)**; rekord = 16-bajtowy header {u32 id, u32 size=56, u32
ver=1, u32 crc=0} (jednolite 1366/1366) + 56-bajtowy payload (+ 56B padding).

Własny walk (widths: tag 1→8B, 0xC→4B, 0xD/0xE/0x10/0x11→4B):
- advance-8 (class id 20002 + record id) → offset 8; flags u16 = 0x80; count u16 = 6;
  6 wpisów {u16 tag + value}; mode-1 tail u32 = 0 → offset 56 == limit (pełna konsumpcja).
- **Cursor offset przy odczycie VALUE tag ID 17 == 0x30 w 1366/1366 rekordów** (jedyne
  observed offset; warianty w 0 rekordach); **record 0: BB 2E 00 00 = 11963**;
  **record 1014: 00 00 00 00 = 0**; **zera DOKŁADNIE [1014, 1015]**; sekwencja tagów
  [1, 0xC, 0xD, 0xE, 0x10, 0x11] jednolita 1366/1366; flags 0x80 / count 6 / size 56 /
  ver 1 / crc 0 — jednolite 1366/1366.
- Destination: field index = tag+4 = 0x11+4 = 0x15 = 21; dest = value_array + 21*4 = +0x54
  (SLOT 21 z 22 = 18+4) — TAK.
- MOJE negatywne kontrole (własne, nie dziedziczone): NC1 truncate-payload-48 → BOUNDS_FAILURE
  offset 48+4 > 48 (DETECTED — ścieżka błędu readera); NC2 corrupt tag→0x06 → UNKNOWN TAG
  (DETECTED); NC3 count=0 → 0 wpisów (strukturalna spójność modelu).
- Wynik maszynowy: QC_R3_VFS_WALK_RESULT.json (verdict PASS, failed checks: []).

## Q4 — BEFORE COPIES + AMEND LOG (PASS: 10/10)

- **10/10 kopii BEFORE** (00_CONTROL\DESKTOP_CORRECTION_R1\BEFORE\) == wiersze manifestu
  startowego (size+SHA256 każdej ścieżki) — kopie BEFORE są PRAWDZIWYMI bajtami pre-correction.
- BEFORE_COPIES_INDEX.json: 10/10 wpisów == pliki na dysku (moje pierwotne "problemy" były
  błędem mojego parsera klucza — rozstrzygnięte: klucz relative_path).
- AMEND_LOG_DESKTOP_CORRECTION_R1.md — obecne i poprawne: Desktop finding (§1), superseded
  claim (§2, w tym digit-shift 0x00125553), branch-selection correction (§3), BEFORE/AFTER
  pary path+size+SHA256 (§5 — obie SHA każdej pary zweryfikowane: BEFORE==manifest, AFTER==disk),
  QC1/QC2 superseded-conclusion record (§6), contradiction census 7 wzorców + hit VFS_TO_PARSER_TRACE
  line 40 (§7), remaining unknowns (§8), affected dependency set (§9 — 10 corrected + dispositioned
  non-dependent), §8 lesson line "correct instruction bytes != proven selected execution/parser
  path" (§6, wyróżniona wprost).
- Generator SHA spójność: 4/4 generator_sha256 w artefaktach == bieżące skrypty == wartości
  z assignmentu (s2 37AD7431..., s3 F141645E..., s4 620F13CB..., s5 D07E84F9...).
  (Zastrzeżenie proweniencji: hash po-run nie dowodzi wykonanych bajtów — ale każdy OUTPUT
  został przeze mnie niezależnie odtworzony ze źródeł fizycznych: 185/185 pinów + pełny walk.)
- Wynik maszynowy: QC_R3_BEFORE_COPIES_RESULT.json.

## Q5 — WORDING + DEPENDENCY SWEEP (PASS_WITH_FINDINGS — patrz P2-1/P2-2/P3 powyżej)

- Statusy §5 w stanie current: RUN_STATUS = CONSUMER_UNREACHED (REPORT; SEMANTIC_ASSESSMENT
  §RUN_STATUS; HANDOFF; wszystkie pozostałe wzmianki CONSUMER_REACHED_... są jawnie etykietowane
  historical/superseded); DEST_FIELD_IDENTIFIED = YES; DOWNSTREAM_CONSUMER_IDENTIFIED = NO;
  FINAL_SEMANTIC_STATUS = UNVERIFIED; WORLD_INSTANCE_TO_MODEL_EDGE = NOT_TESTED;
  PLACEMENT_XYZ_RECOVERED = NO.
- Bounded wording §5: obecny VERBATIM (REPORT L66; SEMANTIC_ASSESSMENT; HANDOFF; CONSUMER_TRACE;
  DESTINATION_CONSUMER_CENSUS.json DOWNSTREAM_CONSUMER_WORDING).
- "tag ID 17": konwencja zastosowana; **0** wystąpień "17th property/descriptor" w sekcjach
  current (pozostałości tylko w etykietowanych sekcjach historycznych + BEFORE).
- ONE_DIRECT_CALLER_FOUND: wszędzie scoped ("within the censused machinery", "NOT global proof
  that slot 21 has exactly one writer across the client").
- REPORT.md §18: **46/46 kluczy obecnych** (38 pól §18 + 8 governance), wszystkie ze
  skorygowanymi wartościami (READ_FUNCTION=FUN_009777F0; READ VA/RVA/FO 0x977807/0x577807/0x577807;
  STORE 0x977810; RUN_STATUS=CONSUMER_UNREACHED).
- Liczby: rozróżnione (physical 420 vs 388 file rows vs 391 raw lines vs NOTE row; brak
  hard-code 389 jako current; historyczne 364/389 zachowane jako historyczne) + statement
  manifest-stale-until-regeneration obecny (REPORT + HANDOFF). **WYJĄTKI = finding P2-1**
  (418 w HANDOFF L90; 419 w AMEND_LOG §7).
- High-risk words (only/all/never/global/exhaustiv/unique/proves/must/every/no-X-exists) w 10
  skorygowanych dokach: 148 hits przejrzanych — wszystkie zakotwiczone w dowodach
  (warunki reachability "only when descriptor+0 == NULL"; cenzusy "all 1366"; "never NULL"
  = byte-proof fabryki; "GLOBAL ... UNVERIFIED"/"NOT global proof" = bounded; "unique WITHIN
  the censused machinery"; "must" = imperatywy metodologiczne) LUB osłabione. Wyjątki
  literalne = P2-2.
- Wynik maszynowy: QC_R3_WORDING_SWEEP_RESULT.json.

## Q6 — PE_MASTER_REVIEW + ENTRYPOINT UNTOUCHED (PASS)

- 06_REPORT\PE_MASTER_REVIEW.md: 25,523 B / SHA256 811E03E341D7A28F01AF69A47B1643D8E6C71C0F50D047E5B257419A119C248F
  == wiersz manifestu startowego — **byte-unchanged** (faza persistence wykona supersession per §10 krok 7).
- AUDIT_ENTRYPOINT.md (repo root, tracked): git diff HEAD pusty + status czysty — **unmodified
  względem HEAD**.

## COVERAGE (algebra pokrycia; L11)

- QC scope wykonane: Q0 (identities + full 388-row bijection + protections), Q1 (185 pins +
  51 semantic assertions + 19 zdekodowanych okien kodu), Q2 (A/B/C + 3 mutants + identity),
  Q3 (własny framing + walk 1366 rekordów + 2 negatywne kontrole + destination check),
  Q4 (10 kopii BEFORE + index + pełny AMEND_LOG), Q5 (10 doków current: statusy, frazy,
  konwencje, §18, liczby, high-risk words), Q6 (2 pliki persistence-phase).
- **NOT_CHECKED** (jawne ograniczenia tego QC; żadne nie jest load-bearing dla twierdzeń
  korekcji):
  1. Nie wykonałem ponownie 202-site consumer census (PASS15) — to historyczny dowód runu,
     nie obiekt tej korekty (nie zmieniony; metoda/scope opisane spójnie w poprawionych dokach).
  2. Nie ponownie kalibrowałem $0EOCC@ RTTI mangling (historyczny S3; poza zakresem).
  3. Nie re-executowałem skryptów executora (niezależność) — tożsamość generatorów vs SHAs
     potwierdzona, a WYNIKI odtworzone niezależnie ze źródeł fizycznych (silniejsza gwarancja).
  4. Appendix A PRE_CORRECTION_STATE (skrypt cenzusu) nie był re-executed — jego wnioski
     odtworzono moim Q0 (378/10/0 + 389/420 algebra).
  5. Nie dekodowałem całego FUN_00726900/FUN_0070dcf0 do końca (linie tail/mode-1 za 0x726A40;
     strumień FUN_00971ad0 wewn. I/O) — nie nośne dla badanych twierdzeń; okna nośne
     (destination chain, advance-8, odczyty nagłówka) zdekodowane.
- FULL_READ_LOG (pełne lektury tego QC): CORRECTION_RUN_CONTRACT.md (308L), PRE_CORRECTION_STATE.md
  (280L), CORRECTION_CONTRACT_FREEZE.json, AMEND_LOG_DESKTOP_CORRECTION_R1.md (284L),
  REPORT.md (120L), HANDOFF.md (227L), EVIDENCE_INDEX.md (101L), SEMANTIC_ASSESSMENT.md (96L),
  wszystkie 5 artefaktów 01_RAW\DESKTOP_CORRECTION_R1 (JSON w całości), BEFORE_COPIES_INDEX.json,
  pe_parse.py (159L), fragmenty s4_cursor_walk.py (L150-303 + def-cenzus), s2_branch_pins.py
  (def pin + rel32_target), RUN_CONTRACT.md §18 (ekstrakt pól), DESTINATION_CONSUMER_CENSUS.json
  (klucze nośne); plus 19 okien dekodu EXE i surowe hexdumpy VFS.

## DISPOSITION (dla PE-MASTER)

1. **PASS_WITH_FINDINGS**; core korekcji (branch selection → FUN_009777F0, cursor +0x30,
   destination slot 21/+0x54, framing/census, BEFORE discipline, identity/history protection)
   — niezależnie potwierdzone w całości; twierdzenia executora o korekcie są PRAWDZIWE.
2. Findings P2-1/P2-2: rekomendowane poprawki w kroku QC DISPOSITION (edycja 2 klauzul liczbowych
   i 2 klauzul frazowych; jednorazowe, deterministyczne) LUB jawna dyspozycja accept-as-is
   od PE-MASTER ( wtedy finding P2-2 zamyka się jako ACCEPTED-mechanism-description, a P2-1
   wymaga mimo to korekty przed finalnym manifestem, bo liczb 420/418/419 nie można zostawić
   sprzecznych w published state).
3. P3-1/P3-2: notacja provenance — bez akcji w pakiecie (utwalone w QC_R3 wynikach maszynowych).
4. P3-3: kontrola fazy persistence — supersession PE_MASTER_REVIEW (§10 krok 7) przed
   regeneracją manifestu.
5. Persistence dispatch należy do PE-MASTER (HARD_STOP_REASON = QC_R3_COMPLETE).

## QC tools (qc_tools\) i wyniki maszynowe (ten katalog)

- qc_tools\qc3_pe32_x86.py — własny parser PE32 + dekoder x86-32
- qc_tools\qc3_q0_identity.py → QC_R3_Q0_IDENTITY_RESULT.json
- qc_tools\qc3_q1_pinverify.py → QC_R3_PINVERIFY_RESULT.json
- qc_tools\qc3_q2_branch_model.py → QC_R3_BRANCH_MODEL_RESULT.json
- qc_tools\qc3_q3_vfs_walk.py → QC_R3_VFS_WALK_RESULT.json
- qc_tools\qc3_q4_before_copies.py → QC_R3_BEFORE_COPIES_RESULT.json
- qc_tools\qc3_q5_wording_sweep.py → QC_R3_WORDING_SWEEP_RESULT.json
- QC_R3_SUMMARY.json — skonsolidowane wyniki + verdict

## QC-SELF INCIDENT (znaleziony i naprawiony w trakcie; pełne ujawnienie)

Podczas QC import modułu qc3_pe32_x86 przez moje skrypty spowodował, że CPython utworzył
`qc_tools\__pycache__\qc3_pe32_x86.cpython-312.pyc` (klasa incydentu bytecode znana z tego
projektu — oryginalny run udokumentował identyczny przypadek; skrypty executora stosują
`sys.dont_write_bytecode = True`; moje skrypty tego nie zrobiły). NAPRAWA: katalog __pycache__
został usunięty w trakcie QC; weryfikacja po usunięciu: Test-Path __pycache__ = False; cały
zapis QC pozostał w autoryzowanym katalogu 04_QC\QC_R3_DESKTOP_CORRECTION\ (żadna lokalizacja
poza nim nie została dotknięta). Nie wpływa na żaden wynik merytoryczny.

(End of QC_R3_REPORT)
