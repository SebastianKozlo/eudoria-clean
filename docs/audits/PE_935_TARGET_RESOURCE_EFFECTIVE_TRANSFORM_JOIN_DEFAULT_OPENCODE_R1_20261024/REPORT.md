# REPORT — PE_935_TARGET_RESOURCE_EFFECTIVE_TRANSFORM_JOIN_DEFAULT_OPENCODE_R1_20261024

RUN_STATUS = COMPLETED (bounded campaign; HARD STOP po terminalu)
SCIENCE_VERDICT = PARTIAL_PASS_WITH_MATERIAL_NEW_FINDINGS
PROCESS_VERDICT = NONCOMPLIANT_WITH_DISCLOSED_INCIDENTS (6 empty task returns; A1 exposure overshoot; mitigated by tiny-job method)
ROOT_SESSION = ses_e92b135b0ffeF6KM96luHwXIZL (pe-master, nask-glm/glm-5-3, variant=default; DB census mode=ro)
WORLD_XYZ_RECOVERED = NO; HISTORICAL_PLACEMENT = NOT_ESTABLISHED; CANONICAL_GATE_EFFECT = NONE; AUTHORITY_STATUS = ADVISORY_PRE_QUALIFICATION
NOWE USTALENIA = REPORTED_PENDING_EXTERNAL_POSTAUDIT

## 1. Pytanie główne: czym jest T=M32[B+0xC0]

**T = instancja SceneFeederObject (SFO).** Łańcuch akwizycji (każda krawędź potwierdzona bajtowo):

B (ClientMovableObject, new 0x128, vtable 0x00A7DCB0) w derived ctor 00528E50:
- zero-init [B+0xC0]=0 @0x00528EC0 (89 9E C0 00 00 00);
- 00401360(arg4 pushed @0x00528FA5, ALE RET C3 — arg4 NIE jest konsumowane przez 00401360) = lazy singleton getter obiektu 0x88 B @0x00B9FE5C (ctor 004157B0, vtable store 0x00A79F18);
- 00485050(ECX=singleton) = MOV EAX,[ECX+0x1C]; RET → sub-manager;
- 0048CBB0(ECX=sub-manager, stack arg4) = lookup w kontenerze; **RET 4 — TU arg4 jest konsumowane**; wynik EDI = holder (lookup-miss → 0);
- gate: EDI==0 → JZ pomija cały blok SFO (B+0xC0 pozostaje NULL);
- 0085B120(B,&local_str) → 00414130(B)=[B+0x74]=klucz instancji (RET C3 — push przechodzi dalej);
- 005247C0(this=holder, arg1=klucz, arg2=str): new(0x98) → 00509330(new SFO, holder, klucz, str) (vtable store 0x00A7D458, RET 0xC) → 005094E0(SFO, &holder+0xC0) → rejestracja 006A8980(**[holder+0x24]**, &slot_str, &slot_SFO) → **RET 8, EAX=SFO**;
- **[B+0xC0]=EAX @0x00528FEA (89 86 C0 00 00 00)** — CONFIRMED.

arg4 ctor 00528E50 pochodzi od creatora 004C46C0, którego arg4 = **stała 1** (PUSH 0x1 @caller 004C4941) — arg4 NIE jest model_id ani identyfikatorem rekordu.

## 2. Pola transformacyjne T (fala A)

| Pole T | Writer (ctor) | Źródło | Reader | Status |
|---|---|---|---|---|
| +0x34/38/3C | 005094C0(T,&B+0x44) | pierwsza trójka B (B+0x44) | slot1 005090A0 (address-of, 8D 41 34 C3); slot3 0050A050 fallback (X/Y/Z→bufor caller) | stored placement; semantyka pozycji STRONGLY_SUPPORTED (prior canon SF_DOWNSTREAM G14, klasy B/C/D) |
| +0x4C..0x70 (36B) | 00509510(T,&B+0x5C)→0096CDD0→00437F70→0048BAC0 | druga trójka B (B+0x5C) + origin S | BOUNDED NEGATIVE: sloty 0-5 nie czytają +0x4C; reader poza vtable NIE ZNALEZIONY w dostępnych packetach | writer CONFIRMED; reader NOT_FOUND_IN_AVAILABLE_PACKETS (bounded) |
| +0x74/78/7C | 00509510 (ten sam call) | [B+0x5C..0x64] (verbatim) | slot2 005090B0 = lea [ecx+0x74] (address-of) | CONFIRMED (kopia trójki wejściowej) |
| +0x80..0x88 | 00509070(T,&B+0x50), RET 0x4 | [B+0x50..0x58] | slot4 005090C0 = lea [ecx+0x80] (address-of) | CONFIRMED |
| +0x40..0x48 | 005094E0(T,&holder+0xC0) | [holder+0xC0..0xC8], gated bitem [T+0x2C]>>4&1 | — | CONFIRMED (writer); semantyka UNKNOWN |
| +0x30 (link) | SFO ctor 00509330: new(0x118)→007B6000 | fresh link object | slot3 primary: [SF+0x30]→vcall slot17(+0x44)→result+0x90 = world translate→00437F70→0082B5A0(x0.01−S) | prior canon CONFIRMED; klasa linka UNKNOWN (next-test z SCENEFEEDER census) |

## 3. H i creator (fale C/B)

Creator 004C46C0 (cdecl, ARGC=4: &44B factory-record, selector u16, 00765930-result, 1; RET C3 @0x004C47EF; caller 004C47F0 od 0x004C47F0):
- kopiuje CAŁY record 11 DWORD [arg1+0x00..0x28] → [ESP+0x08..0x30] (G+off=record[off]); v1=record+0x08..0x10;
- selector {3,4,5,6,7} omija TYLKO blok H (alloc/ctor/rejestracja bezwarunkowe);
- blok H: FLD v1.x,v1.y → 004154F0 (RET C3) → 00853A80(mgr, x1,y1,0,0) → **RET 0x10**; H=[ESP+0x44]; FLD v1.z; FLD H; FCOM; FNSTSW; TEST AH,0x41; JNZ skip → **v1.z := H iff H > v1.z (ordered strict GT)** — zapis [ESP+0x18] @0x004C478A;
- alloc 0x128 → ctor 00528E50(this=B, &stack-copy, selector, arg3, 1) @0x004C47C1; potem rejestracja: 004154F0→00856190(mgr, B) → AL bool (RET 00856190 poza window — inferred).

**00853A80 (producent H):** ESI=ECX=manager (singleton 0x8C @0x00BA12E8, getter 004154F0). ZWALIDUJ {x,y,0} przez 00755F90(this=&mgr+0x58 inline region floatów) — fail ⇒ H=0.0 (FLDZ, RET 0x10). Primary: [mgr+0]≠0 ⇒ lock 00413440(ECX=[mgr+0x50]) ⇒ **vcall slot1 (vtable+4) na obiekcie [mgr+0]** ⇒ wynik float = H ⇒ unlock 00413450 ⇒ RET 0x10. Secondary: [mgr+0x4C] — vcall slot1 bez locka. **ZERO arytmetyki FPU w ciele — H pochodzi w całości z providera.** Terrain-height = PLAUSIBLE (wzorzec validate→fallback0→query); klasa providera i jego instalacja (runtime writer mgr+0; ctor 008550C0 zeruje) — poza packetami: UNVERIFIED.

**0096CDD0 (builder orientacji):** ECX=out 36B; arg=&float3 (RET 0x4). Predykat strict LT: |x²−qword[0xA9C4B0]| < dword[0xA797C8] (wartości NIEZNANE). Path A (fall-through): a=y+z; _CIcos/_CIsin (thunki 0095DA1C/0095DA28) → baza [[c,s,0],[0,0,1],[s,−c,0]] — CONFIRMED orthonormal. Path B (trzy _CIcos osobno): **window ucięty @0x0096CE9F — UNVERIFIED**. Kolejność elementów macierzy w T+0x4C: wg Path A.

## 4. Selector (C2)

Parser 007453D0: selector = word z kursora (`MOV AX,word[EAX+EDX]`), zapis **tylko** gdy [cursor+0x11]≠0 i cursor+2≤end; default **0** @00745448; zero-init @00745378 (poza windowem). Reader: 004C493C word[F+0x44]=record+0x34 (F=stabilna baza 004C47F0, record=F+0x10) → MOVZX → creator arg2. Bounded negative: brak nadpisu record+0x34 między write a read w dostępnych windowach; ogon 004C4952..004C4A01 ma NO_DEF_IN_WINDOW (utrzymane). Preservation do użycia: potwierdzone w dostępnych granicach; pełny lifetime (wielokrotne create/update) NIE domknięty.

## 5. Resource-instance join (fala B) — PARTIAL

Prior canon (B03 poprzednika, utrzymany z pinami): rec+0x00 u32 = klucz lookupu registry 008544D0 I verbatim id factory-record (E8); creator→ctor→00856190 rejestracja per-instance. 00765930 = metoda na managerze 0x1C @0xBA12B8 (lazy z 004C4640) z EMPTY-STRING key 0xA7957B (zmierzony); importy [A75A38]/[A75A40]/[A75A44] = idiom temp-init/cleanup/lookup (tożsamość importów UNRESOLVED); zwraca arg1=&factory-record → creator arg3. **Krawędź do konkretnego zasobu modelu/NIF root: NIE domknięta** (brakujące: payload+0x0C sub-object, blok 004C49BF, lookupy 004C4981/004C4A9D). Model 296445.nif NIE podstawiony.

## 6. Proces

17 natywnych Task (DB census, mode=ro): 11 dostarczyło wyniki, **6 pustych powrotów** (A2, A2b, B1, QC_A, M1, QC_A2 — state=completed, brak treści i zapisów; 2 próby/atomic job zachowane: A2/A2b i B1 = uczciwy JOB_NONPASS). Diagnostyka kanału (T02 probe OK; D2 tiny read+summarize OK) ustaliła wzorzec: tylko małe jednoplikowe joby niezawodnie dostarczają → przejście na metodę tiny-job (M2-M6, QC_A3, QC_C, QC_B). A1: odchylenie ekspozycji ~653 linie > limit 600 (zgłoszone samodzielnie). Modele: wszystkie dzieci nask-glm/glm-5-3 variant=default (DB metadata); REQUEST_EFFORT/SERVER_EFFECTIVE_EFFORT = UNKNOWN/NOT_OBSERVED.

## 7. QC

- QC_A3: rejestracja SFO = **HOLDER_PLUS_0x24** — claim A1 "B+0x24" REJECTED (finding materialny, poprawiony w claimach centralnych).
- QC_C: PASS bounded (RET 0x10 ×2; 00755F90 validate; lock/unlock+vcall; bounded negative zero FPU-arytmetyki); zastrzeżenia: ścieżka zwrotu poza 0x00853B3D; "2 zera" w ABI = literalne zero caller-side.
- QC_B: PASS (RET C3 creator; kopia CAŁEGO recordu od +0x00 — korekta baseline "+0x08"; ARGC=4 cdecl; gate/H/ctor/new(0x128)/rejestracja potwierdzone); UNVERIFIED: RET 00856190.
- Master counter-check (line-level): kierunek H — st0=H vs st1=v1.z, TEST AH,0x41 → zapis tylko H>v1.z (sformułowanie QC_B "u2>stara" było nieprecyzyjne); receiver providera H = [mgr+0] (korekta M3 "na [ESI]"); QC_C "pod-obiekt @+0x58" retracted (LEA inline floats).

## 8. Granice

- Reader bloku T+0x4C: NOT_FOUND_IN_AVAILABLE_PACKETS (bounded: slot census + packety; NIE cały obraz).
- Path B 0096CDD0: ucięta — UNVERIFIED.
- Klasa providera H ([mgr+0]) i jego installer: UNVERIFIED (runtime writer poza packetami).
- Klasa linka SFO+0x30 (007B6000): UNKNOWN (prior-canon next-test).
- Wartości K=0xA9C4B0 / eps=0xA797C8: NIEZNANE (nie zgadywane).
- Model-instance join: PARTIAL; ścieżki hit (payload) i miss (factory record) rozdzielone, ale żadna nie dochodzi do konkretnego modelu.
- WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED.
