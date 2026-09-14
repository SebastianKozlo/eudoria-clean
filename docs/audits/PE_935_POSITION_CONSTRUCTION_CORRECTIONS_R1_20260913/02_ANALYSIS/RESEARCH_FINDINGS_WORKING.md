# RESEARCH_FINDINGS (WORKING) — PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913

**Roboczy raport badawczy wykonawcy (odrębny od REPORT.md; będzie cytowany przez QC).**
**Uwaga metodologiczna:** poniższe to notatnik badawczy z własnych dekodów; twierdzenia NOŚNE są w REPORT.md; tu — pełny kontekst odkrycia, ślepe uliczki i pomiary pomocnicze. Warstwy oznaczane [BYTES]/[DISASM]/[DECOMP]/[MODEL]/[SYNTHETIC].

## 1. Ślepe uliczki censusu writerów (dlaczego census5 był potrzebny)

- **census1-3 (post-getter window / dataflow 1-poziom / setter-scan):** 0 trafień dla mgr1+0/mgr1+0x4C przez EAX-flow; 44 kandydatów [reg+0] po getterze — wszystkie false-positive (vtable-write nowych obiektów: `mov [esi], 0xA91E4C` = ctor MovableObject; `mov [eax], 0xA7DB64` itd.; zeroingi; funktory na stosie: `mov eax, esp; mov [eax], ecx` @0x00567676 = budowa functoru {FUN_00855DC0, mgr, key} dla FUN_00567030 — deferred-delete, nie zapis pola managera!).
- **census4 (2-poziomowy: mgr przekazywany do callee):** 36 callee; jedyny prawdziwy zapis mgr1+0x4C = **FUN_00855340** @0x0085536D (`MOV [EBX+0x4C],EAX`); reszta = zapisy do [esi] innych obiektów (FUN_00797280 = [this+4]; FUN_00853A50 = [this] na PLACEMENT recordzie i — jak się okazało — na mgr1!).
- **census5 (pełny spill-tracking + arg-seeding w callee):** trafił FUN_00853A50 wywołaną z **mgr1 jako this** z getter-callera 0x0044CC67 → odkrycie: mgr1+0 = pole „aktualnego obiektu" pisane przez rodzinę FUN_0044CCxx (metody mgr3!), a NIE statyczny provider z rejestracji.

## 2. Kluczowy moment: identyfikacja providera1

- FUN_0044CC60 [DISASM]: `mgr1 = FUN_004154F0(); FUN_00853A50(mgr1, [mgr3+0x18])` — mgr1+0 = [mgr3+0x18]; mgr1+4 = [mgr3+0x18]+4 (para begin/end!). Analogicznie FUN_0044CD30 (stan 1) = [[mgr3+0]].
- FUN_0044CEE0 [DISASM] — jedyny caller rodziny; this = **mgr3** (z gettera FUN_004147F0 @0x0048D3BE!); maszyna stanów na [mgr3+0x34] ∈ {1,2}; bounds-check x87 na (x,y) na wejściu (qword [0xA7B098]=−500.0).
- FUN_0044D0F0 @0x0044D210 [BYTES]: `MOV [EDI+0x18], EAX` po `new(0x14)+FUN_00538B70` → **mgr3+0x18 = nowy obiekt**.
- FUN_00538B70 [BYTES]: `mov [esi], 0x00A7F430; mov [esi+4], 0x00A7F420` → RTTI: **MaTerrainManagerRuntime**. Slot+4 vtable 0xA7F430 = 0x00934540.
- FUN_00934540 [DISASM]: `[this+8]==NULL→FLDZ`; else FUN_00936D50([this+8],x,y,arg2)/FUN_00936C30([this+8],x,y) — **x,y przekazywane dalej z &L0 (arg1+0/+4)**.
- FUN_00936C30 [DISASM]: cell index → node resolve → lock → sample → interp → **FCHS**; fallbacki 10.0/[−1000.0].
- FUN_00936A60 [BYTES]: `FILD [esp+0xC](cell); x/cell; floor; fist; SHL ESI,0x10; y/cell; floor; fist; AND EAX,0xFFFF; OR EAX,ESI` — **packed 16:16 cell id**.
- FUN_00935870 [DISASM]: dwa puste std::string → FUN_00934670(str1, str2, …) → **FUN_00415670 (singleton!) → FUN_00823C10** — komórki terenu = named resources (tag 0x6E = 110).

## 3. Stałe liczbowe (z EXE, własny odczyt)

| Adres | Wartość | Rola |
|---|---|---|
| 0x00A7B128 | **10.0f** | fallback wysokości „brak węzła terenu"; próg WAVES; górna granica dystansu interakcji (FUN_0084A090 porównuje DYSTANS z tą samą stałą — podwójna rola) |
| 0x00A7B270 | **−1000.0f** | fallback lock-fail |
| 0x00A7B098 | qword **−500.0** | bounds-check wejść (mgr3/metody) |
| 0x00A7B0A0 | qword **0.0** (para z −500) | druga granica bounds |
| 0x00A79A08 | qword **0.5** | half-cell w przeliczeniach komórkowych |
| 0x00A7BA38/3C | **−32767.0/+32767.0f** | domyślny AABB rejestracji ArkMoveSubsystem (accept-all) |
| 0x00A7B9F0 | qword **14.0** | promień samplingu WAVES (5-pkt) |
| 0x00A7AF88 | qword **25.0** | promień samplingu WAVES (4-pkt) |
| 0x00A7AF80 | qword **0.1** | krok drop-to-ground (FUN_0085B3E0) |
| 0x00A7B2D0 | qword ≈**0.2** | offset zmiennej-3 (FUN_0085B3E0 wariant-3) |

## 4. Wzorzec x87 — dwie instancje (CREATE/EXISTING)

Porównanie bajtowe obu okien [BYTES]: FUN_004C46C0 @0x004C4777-4790 vs FUN_0085B3E0 @0x0085B426-0x85B441: **identyczny ciąg semantyczny** (FLD z/FLD h/FCOM/FNSTSW/FSTP ST(1)/TEST AH,0x41/JNE/FSTP-z'albo-FSTP ST(0)) — różne tylko sloty stosu ([ESP+0x18] vs [ESP+0x24]) i scratch ([ESP+0x44] vs [ESP+0x50]). EXISTING: brak jakiejkolwiek bramki wariantu PRZED korektą (pierwszy cmp [edi+8] pojawia się @0x0085B451, PO zapisie z').

## 5. mgr1/mgr2/mgr3/mgr4 — cztery singletony w jednej rodzinie

- mgr1 [0xBA12E8] 0x8C — parameter map + Z-provider (ten run);
- mgr2 [0xBA12EC] 0xCC — sonda kolizyjna (FUN_00856800: CS@+0x18, query sub-obiekt@+0x44, vtable slot **+0x154**!);
- mgr3 [0xBA1280] 0xCC — move-subsystem grid (FUN_004147F0; +8 grid; +0x18 = MaTerrainManagerRuntime!);
- mgr4 [0xBA1260]-rodzina — singleton FUN_00401360 (holder ctor-chain FUN_00485050/FUN_0048CBB0 — sceno-holder, do dekodu w następnym runie).
**Ciekawostka:** provider2 (ArkMoveSubsystem) slot+4 woła FUN_004147F0 = getter mgr3 — TEN SAM manager, którego +0x18 = provider1-source. Zapis: `zapytanie Z powiadamia move-grid (mgr3+8) i pyta teren (mgr3+0x18)`.

## 6. Weryfikacja pinów — rozjazdy znalezione (do adjudykacji)

1. §12.4 „FUN_00413340 @0x00853AE8": cel calla = **FUN_00413440** [BYTES: `E8 53 F9 BB FF` → 0x00413440]; 0x00413340 = bajty `28 C2 08 00` (środek instrukcji poprzedniej funkcji — nie-start). IAT: [0xA75064]=EnterCriticalSection, [0xA7506C]=LeaveCriticalSection [własny import-parse].
2. D-3: MOV EAX,ESI @**0x0073459C** i @**0x007345B5** [BYTES surowe 0x00734588-0x007345BA]; Desktop 0x73459B/0x7345B4 = POP EDI.
3. SEAM_FLOW_MAP:46 atrybucja: „max(rekord[4], wynik)" — **jest to z4 = pos.z = rekord+0x10** (placement+0x10; 4-ta dword-para rekordu — licząc od +0: +0,+4,+8=**z**... konwencja „rekord[4]" = offset+0x10 = trzecia składowa — spójne, ale kwalifikacja semantyki x87 wymagana (ERRATA_R5 nota).

## 7. Pomiary pomocnicze

- ghidra_post_decomp: 67 funkcji → `01_RAW/DECOMP_P2/` (warstwa [DECOMP]; użycie: censusy konsumentów/falsy-positive eliminacja).
- Import table: 24 DLL; stlport.5.1.dll (205), MSVCR80 (129), KERNEL32 (82)… NxCooking.dll/PhysXLoader.dll obecne (bez użycia w tym runie — NOT_CHECKED).
- Suity: F1 28/28 + meta PASS; x87 21/21.

## 8. Czego NIE zrobiono (granice robocze → REPORT §7)

Format komórek (resource), FUN_0093F710 (side-effect), sloty SceneFeeder (FUN_0050A460+), FUN_0085D240/00861330, holder FUN_0048CBB0-class, pisarz mgr3+0, RUN3 model-channel re-derivation. Wszystkie jawne w HANDOFF NOT_CHECKED.
