# QC_R1 — niezależny internal-QC (fresh, DEFAULT)

RUN_ID: PE_935_OWNER_ATTACH_PROVIDER_IDENTITY_QC_R1_20261020
Parent: PE_935_OWNER_ATTACH_PROVIDER_IDENTITY_SAVED_R1_20261020
Contract: AUTHORING_R1 CONTRACT.md sec.10. Atrybucja: świeża sesja pe-master-auditor (nask-glm/glm-5-3-default, medium). Re-derivation wykonana od zera z EXTRACTS, bez kopiowania pochodnych parenta.

## QC_VERDICT: REQUIRE_CORRECTIONS

Nauka (re-derivation, budżety, strukturа JSON/CSV) — zgodna; blokują wyłącznie defekty formalne CLAIMS (statusy poza taksonomią, błędny source_pin) oraz niespójność budżetu w child HANDOFF.

---

## Zadanie 1: niezależna re-derivation store 0x0085ACE9 (P01)

Oznaczam ESP0 = ESP na wejściu 0085ACD0 (retaddr @ [ESP0], ARG1 @ [ESP0+4]).

| VA | instr | ESP po | efekt |
|---|---|---|---|
| 0085ACD0 | SUB ESP,8 | ESP0-8 | rezerwacja par L0=[ESP0-8], L1=[ESP0-4] |
| 0085ACD3 | LEA EAX,[ECX+0x88] | -8 | adres guardu |
| 0085ACD9 | XOR EDX,EDX | -8 | EDX:=0 |
| 0085ACDB | CMP [EAX],EDX | -8 | test [ECX+0x88]==0 |
| 0085ACDD | PUSH ESI | -0xC | save ESI |
| 0085ACDE | MOV ESI,[ESP+0x10] | -0xC | [-0xC+0x10]=[ESP0+4]=ARG1 |
| 0085ACE2 | JNZ 0085AD12 | -0xC | skip gdy ≠0 |
| 0085ACE4 | PUSH EDX | -0x10 | push 0 (przyszły arg6) |
| 0085ACE5 | MOV [ESP+8],EDX | -0x10 | [ESP0-8]=L0:=0 |
| 0085ACE9 | **MOV [ESP+0xC],EDX** | -0x10 | [ESP0-4]=**L1:=0** — store analizowany |

**Wniosek P01:** efektywnym przeznaczeniem 0085ACE9 jest **ESP-relatywny stack local L1 = ESP0-4** (nie ECX-relatywny, nie slot retaddr; PUSH EDX uwzględnniony: -0x10+0xC = -4). Wartość = 0 (EDX z XOR 0085ACD9, pierwsza redefinicja LEA EDX @0085ACF2 — po store). Para L0/L1 jest przekazywana adresowo (LEA EAX,[ESP+8] @ACED; PUSH EAX @ACF1) jako **arg5 z 6** do CALL 00730F00 (arg1=[ECX+0x74] … arg6=0) — out-buffer, nie zapis pola obiektu. B→R attach @ACE9: **odrzucony dla tego body** (uzasadnione).

- **P01-C1: VERIFIED** (moja niezależna ESP arytmetyka = claim; zgodne z STACK_MAP.md childa).
- **P01-C2: VERIFIED** (zero z XOR, brak redefinicji przed store; para 8-bajtowa [ESP0-8,ESP0-4]).
- **P01-C3: VERIFIED** (arg5/6 z dokładnej kolejności PUSH).
- **P01-C4: VERIFIED** (negatywny, scoped; destination stackowy wyklucza zapis pola obiektu w tym body).
- P01-C5..C9 (poza zakresem zadania, ale odczytane): spójne z extractem; C8 callee-cleanup 0x18 to jedyna spójna z epilogiem lektura w oknie (callee body nieotwarte) — STRONGLY_SUPPORTED zasadne.

## Zadanie 1: niezależna re-derivation store 0x0085CD17 (P06)

Zakładam S = ESP po 0085CC90 (ADD ESP,8; region zaczyna się mid-function). Wszystkie bloki FLD/SUB ESP,8/FSTP/CALL/ADD ESP,8 (CC9E..CCFB) są zbalansowane: przy każdym FLD oraz na 0085CD06 **ESP=S**.

**Zadanie 2: pełny ESP trace 0085CD06..0085CD20:**

| VA | instr | ESP | efekt |
|---|---|---|---|
| 0085CD06 | MOV ESI,[ESP+0x34] | S | ESI := frame slot [S+0x34] (ESP-relatywny slot, nie ECX) |
| 0085CD0A | MOV ECX,[ESI+0x28] | S | receiver = obiekt w polu +0x28 ESI |
| 0085CD0D | MOV EDX,[ECX] | S | VT := [ECX] |
| 0085CD0F | MOV EAX,[EDX+0x18] | S | F := [VT+0x18] |
| 0085CD12 | PUSH EBX | **S-4** | arg (wartość EBX spoza okna — nieustalona) |
| 0085CD13 | CALL EAX | S-8 w callee; S-4 po powrocie przy cdecl | receiver ECX=[ESI+0x28] |
| 0085CD15 | TEST EAX,EAX | S-4 (przy braku callee-cleanup) | test produktu |
| 0085CD17 | **MOV [ESI+0x2C],EAX** | S-4 | dest = **pole +0x2C obiektu ESI** (ESI z frame slotu; nie ECX-relatywnie; nie ESP bezpośrednio) |
| 0085CD1A | JNZ 0x0085CA48 | S-4 | ≠0 → ścieżka użycia |
| 0085CD20 | JMP 0x0085CA43 | S-4 | =0 → byte [ESP+0x1E]:=0 |

**Kluczowa obserwacja ABI (niezależna):** cele JNZ/JMP (CA48/CA43) leżą w oknie P07, gdzie te same wiersze są osiągane z ścieżek z **ESP=S** (np. CA3D→CA3F→CA43; CC98 JNZ CA3F). Spójność frame-offsetów ([ESP+0x1E], [ESP+0x24..0x2C], [ESP+0x34]) między ścieżkami wymusza, że **callee CALL EAX @CD13 czyści wypchnięty EBX (stdcall RET 4)** — inaczej ścieżki miałyby przesunięte o 4 offsety ramki. Callee body nieotwarte → wniosek STRONGLY_SUPPORTED (analogicznie do P01-C8), nie CONFIRMED; w obrębie admitted windows żadnej sprzeczności ESP nie ma.

**Wniosek P06:** MOV [ESI+0x2C],EAX zapisuje **retval wirtualnego wywołania** (receiver [ESI+0x28], slot VT+0x18) do pola +0x2C obiegu ESI=[ESP+0x34]. Wartość = produkt call z provenance obiektowym; downstream (CD27..CD45 w oknie P06; CA5D..CA94 w oknie P07: sloty +0xAC float-getter z FLDZ/FCOM vs 0.0, +0xB0 3-float out przez PUSH &local, przy [ESI+0x20]==3 po null-check) potwierdza traktowanie [ESI+0x2C] jako vtable-bearing receiver.

- **P06-C1: VERIFIED co do treści** (dest/value provenance dokładnie jak w claimie). Superlatyw „first store+2C candidate with object-pointer provenance" — prawdziwy w zbiorze kandydatów tego runu (P02-C2: kopia global-constant 3-dword — zweryfikowałem w P02_EXTRACT rows BE62..BE79; P05-C1: float slot transform write — zweryfikowałem rows C066..C0B4); scope „w tym runie" jest tylko implikowany, minor.
- **P06-C2: VERIFIED co do treści, DEFECTYWNY source_pin** — patrz F2.
- **P06-C3: treść poprawna (join ESI==R nieustalony), status „UNKNOWN" poza taksonomią** — patrz F1.

## Zadanie 3: budżety CONTROL vs HANDOFF/ledger

Zsumowałem niezależnie z CONTROL/EVENTS (ADMIT counts + INCIDENT_DEBIT):
- bodies: 3+4+4+4+3+3+2+3 = 26 reserved; incident debits 3+1 = 4; **charged 30/48** ✓
- listing rows: 26+125+56+52+36+63+184+110 = **652/9000** ✓
- calls: 1+8+2+8+2+7+10+12 = **50/300** ✓ (P06: zadeklarowane call_reservation 6, rozpoznane tekstowo 7 — naliczone 7, zgodnie z regułą max; P07: zadeklarowane 20 vs rozpoznane 10 — listing kind, reguła max obowiązuje dla document_body, naliczenie 10 dopuszczalne; obserwacja, nie naruszenie)
- candidates: 3+4+2+3+2+2+2+2 = **20/48** ✓; document_lines 0/3000 ✓

Ledger (reserved/charged/caps) = moja suma; root HANDOFF „left: 18 bodies, ~8350 rows, 250 calls, 28 candidates" = 48-30 / 9000-652 / 300-50 / 48-20 ✓ (8348≈8350 z „~" — uczciwe). Root GATES „30/48, 652/9000, 50/300, 20/48" ✓. Incydenty 2 (events 000004/000010) ujawnione jako PARTIAL_NONCOMPLIANT, regiony później właściwie admitowane (P03/P08) ✓ — brak retroaktywnej legalizacji.

**F3 (P2): P01_OWNER_ATTACH/HANDOFF.md deklaruje „BUDGET: 1 body + 1 candidate reservation consumed", podczas gdy CONTROL/PLANS/P01 i event 000004_ADMIT naliczają 3 bodies / 3 candidates (kontrakt §6: „3body/3candidate reservations").** CONTROL jest autorytatywny; deklaracja childa przeczy naliczeniu. Poprawka: skorygować linię BUDGET w P01 HANDOFF (pakiet niezamrożony, z retencją) albo dodać erratum; test rewalidacji: grep „1 body" w P01/HANDOFF → brak trafień po korekcie, zgodność z event 000002 counts.

## Zadanie 4: parsery JSON/CSV (root + P01 + P02; przy okazji wszystkie pakiety)

- 52 pliki JSON: **wszystkie strict-parse bez błędów, zero duplicate keys** (object_pairs_hook). Schema CLAIMS {claim_id,text,evidence_status,claim_resolution,source_pin,rows} obecna wszędzie; brak duplikatów claim_id w plikach.
- CSV: wszystkie wiersze stałej szerokości w każdym pliku (P01 artifact_index 4 kol, pozostałe 3 kol; GATES 3 kol) ✓. Brak „~" jako SIZE/SHA w pomiarach ✓.

### F1 (P1) — evidence_status poza taksonomią projektu
Taksonomia (CONTRACT §9 / AGENTS.md): CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED. Naruszenia (plik! claim_id! wartość):
- `CLAIMS.json` root: R-C5 „UNKNOWN", R-C7 „UNKNOWN"
- `P02_PROVIDER_FIELD/CLAIMS.json`: P02-C5 „SUPPORTED", P02-C7 „SUPPORTED", P02-C6 „UNKNOWN", P02-C9 „UNKNOWN"
- `P05_TRANSFORMWRITE/CLAIMS.json`: P05-C2 „UNKNOWN"
- `P06_PROVIDER_FACTORY/CLAIMS.json`: P06-C3 „UNKNOWN"
- `P08_EARLY_SERIALIZE/CLAIMS.json`: P08-C2 „UNKNOWN"

Skutek: CONTRACT §10 wprost: błędy statusów „nie mogą zostać zapieczętowane jako PASS"; root GATES row `children_packages,PASS,...strict JSON/CSV verified` jest mylący (weryfikował parsowalność, nie taksonomię). Poprawka: w niezamrożonych pakietach przepisać statusy przez serializer: „UNKNOWN"→UNVERIFIED, „SUPPORTED"→STRONGLY_SUPPORTED (P02-C5/C7 mają solidne wsparcie strukturalne; jeśli autor chce słabsze — PLAUSIBLE), z retencją wersji poprzedniej; po seal — sibling corrigendum. Rewalidacja: parser QC odrzucający statusy spoza 5-słownego słownika → 0 naruszeń.

### F2 (P1) — P06-C2 source_pin przypisuje wiersze P07 do admission P06
`P06_PROVIDER_FACTORY/CLAIMS.json` P06-C2 rows „0085CA48..0085CA96" leżą w oknie [0x0085CA00,0x0085CC90) = **admission A5742dd0b9845 (P07)**, a source_pin cytuje tylko „admission Af3c179f81dac" (P06). Poprawka: pin do obu admissionów (wzorzec poprawny już istnieje w root R-C4: „P06/P07 extracts admissions Af3c179f81dac/A5742dd0b9845") lub przenieść wiersze head-region do claimu z pinem P07. Treść claimu pozostaje VERIFIED. (Zbieżność ID: event 000010 INCIDENT również cytuje A5742dd0b9845 — to poprawne wskazanie admissionu P07, w którym nastąpił over-display; nie jest to duplikat ID.)

### F4 (P2) — brak per-pakietowego STAGE_ACCEPTANCE_GATES.csv w P01 i P02
CONTRACT §10 wymaga od każdego kompletnego pakietu REPORT,CLAIMS,HANDOFF,GATES,artifact_index; P03..P08 mają GATES, **P01_OWNER_ATTACH i P02_PROVIDER_FIELD nie mają**. Root GATES (children_packages PASS) mapuje je zbiorczo — dopuszczalne jako „clearly mapped existing equivalent", ale niekonsekwentne względem P03..P08. Poprawka: dodać minimalne GATES.csv do obu pakietów (kolumny gate,status,note jak w P06) z jawnym odniesieniem do admissionów A954d84cd8720 / A48f4c758c48c.

### Obserwacje (bez korekty obowiązkowej)
- P01 STACK_MAP.md zgodny bajt-w-bajt z moją niezależną re-derivation (ESP0-0x10, L1=ESP0-4, arg5=&L0, cleanup 0x18 wyłącznie z balansu caller-side).
- Heterogeniczne nagłówki artifact_index.csv (P01 4-kol, reszta 3-kol; root 2-kol) — kontrakt nie narzuca jednego schematu childów; wskazane ujednolicenie przy publikacji.
- REPORT/HANDOFF root: SCIENCE_VERDICT PARTIAL_PASS i FIRST_MISSING_EDGE (binding [ESP+0x34] w serialize-entry) — zgodne z dowodami; join ESI==R niezasugerowany nigdzie; brak utożsamienia przez sąsiedztwo/layout.

## Werdykty claimów audytowanych (szczegóły w CLAIMS.json)
P01-C1..C4: VERIFIED (CONFIRMED within admitted body). P06-C1: VERIFIED (CONFIRMED). P06-C2: VERIFIED co do treści / pin do korekty. P06-C3: treść poprawna / status do korekty. Budżety: zgodne, poza F3.

**QC_VERDICT: REQUIRE_CORRECTIONS** — korekty F1 (statusy), F2 (pin P06-C2), F3 (P01 HANDOFF budget), F4 (GATES P01/P02); po korektach obowiązkowy final recheck zmienionych claimów i ich konsumentów (CONTRACT §10/§133) — proponuję ten sam fresh QC executor.

## Statusy
MODEL: fresh QC na nask-glm/glm-5-3-default (medium), sesja child pe-master-auditor. WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; kanon/milestones bez zmian.
