# 03_EVIDENCE — Rejestr dowodowy VA (każde twierdzenie → era/hash → VA/instrukcja → test → artefakt)

ERA: EU 9.3.5 (pcg_install). Binarium: Entropia.exe SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31.
Wszystkie VA własne, z tego binarium (mapping S3: image base 0x00400000, brak ASLR; VA→file przez tabele sekcji w 01_RAW\S3_PE_HEADER.json).

## E.1 Tabela ogniw łańcucha (funkcja → VA → kluczowa instrukcja → artefakt z surowymi bajtami)

| ogniwo | VA | kluczowe bajty/instrukcja | artefakt (disasm z raw bytes) |
|---|---|---|---|
| string "Parameters\templates.vfs" | 0x00A86D30 | ASCII @file 6,843,696 | S4B_RAW_HITS.json |
| string magii "ArkVFS02" ×2 / "ArkVFS01" | 0x00A9C4D8 / 0x00A9C4E4 / 0x00A9C4F0 | 3 stringi | S4B_RAW_HITS.json |
| string ".nif" / ".bvi" / ".tdf" / ".amu" / ".vfs" | 0x00A7A774 / 0x00A7A734 / 0x00A7A73C / 0x00A7A744 / 0x00A86820 | tablica rozszerzeń | S4B_RAW_HITS.json |
| string "BNT2" | 0x00A9BF2C | jedyny hit magii BNT2 | file-scan (skrypt inline, log w S18) |
| loader templates.vfs | 0x0072FA30 | `68 30 6d a8 00` PUSH 0xa86d30 @0x0072FAAC | S7_DISASM_loader_0072fa30.txt |
| otwarcie VFS + magia | 0x00972DF0 | ReadFile(8B); compare "ArkVFS01"/"ArkVFS02"; base→+0x8c | S5_PSEUDO_REF_00972DF0.txt |
| zapisywacz magii (ścieżka write) | 0x00971680 | `8b 15 d8 c4 a9 00` MOV EDX,[0x00A9C4D8]; WriteFile | S5_PSEUDO_REF_00971680.txt |
| index walk | 0x00972AD0 | pętla 16-B header + node build + seek | S7_DISASM_indexwalk_00972ad0.txt |
| stride | 0x00979D00 | `8b 41 04 ... 83 c0 0f ... f7 f1 ... 83 c0 01 0f af c1 83 c0 f0` | S6_DISASM_stride_00979d00.txt |
| record read + CRC gate | 0x00971AD0 | seek/re`ad/CRC: `CALL 004063d0` vs `CALL 006b22d0`; `39 44 24 18 0f 94 c3` CMP/SETZ | S5_DISASM_LEAD_00971AD0.txt |
| CRC-32 impl | 0x004063d0 | init 0xFFFFFFFF + tabela + `crc>>8 ^ tbl[]`, ~ | S6_PSEUDO_helper_004063d0.txt |
| parser rekordu | 0x00730C90 | `[EDI+8],EAX` (A) @0x00730CE6; [EDI+4] (B); [EDI+0xC] (C); [EDI+0x10] (D f32) | S6_DISASM_parse_00730c90.txt |
| ctor parsed-template | 0x00730700 | `d9 ee / d9 58 10` FLDZ/FSTP [+0x10] (pole F32) | S6_DISASM_helper_00730700.txt |
| sub-parser listy stringów | 0x00730B70 | u16 count; vector<string> append stride 0x20 | S7_PSEUDO_subparser1_00730b70.txt |
| sub-parser listy u32 | 0x00730970 | u16 count; vector<u32> | S7_PSEUDO_subparser2_00730970.txt |
| copy-ctor do węzła | 0x005670A0 | kopiuje +0x00..+0x10 + sub1 + sub2 + 0x2C | S6_PSEUDO_postparse_005670a0.txt |
| RB-tree insert (rejestr) | 0x0072F8D0 | STLport insert, klucz=node+0x10 | S6_DISASM_register_0072f8d0.txt |
| klucz insertu getter | 0x004123D0 | `8b 01 c3` MOV EAX,[ECX] | S6_DISASM_helper_004123d0.txt |
| singleton rejestru | 0x0043A550 | `a1 24 18 ba 00` MOV EAX,[0x00BA1824] | S9_DISASM_SINGLETON_0043a550.txt |
| lookup rejestru | 0x0072F580 | FUN_004d1430 find; `83 c0 14` ADD EAX,0x14; sentinel `b8 00 58 ba 00` | S10_DISASM_LOOKUP_0072f580.txt |
| walidacja (A/B/C sloty) | 0x0072FCE0 | `83 39 00 / 83 79 08 00 / 83 79 04 00 / 83 79 0c 00` | S11_DISASM_valid_0072fce0.txt |
| **getter A** | 0x007CE1E0 | `8b 41 08 c3` MOV EAX,[ECX+0x8] | S11_DISASM_getter_007ce1e0.txt |
| getter B (rodzina, +0x04) | 0x00746550 | `8b 41 04 c3` | S6_DISASM_helper_00746550.txt |
| getter C (rodzina, +0x0C) | 0x006B22D0 | `8b 41 0c c3` | S6_DISASM_crc_006b22d0.txt |
| pump żądań modeli {0x66,id} | 0x006C9700 | `local_14 = 0x66` + FUN_00415670 + FUN_00823c10 | S20_PSEUDO_DISPCALLER_006C9700 + S19 dumps |
| singleton ArkResourceManager | 0x00415670 | slot DAT_00ba12f4, obiekt 0x98 (kontekst CONT R2 re-verified w tym binarium) | S11_PSEUDO_singleton2_00415670.txt |
| dispatcher provider-chain | 0x00823C10 | `(**(code**)(**(int**)(node+0x24)+4))(...)` `[+0x38]`; queue: FUN_008237d0 | S11_PSEUDO_dispatcher_00823c10.txt |
| konsument kompletny A→request | 0x006B4C50 | `FUN_007ce1e0()` ×2 → `FUN_006c9700(A,...)` ×2 → attach | S20_PSEUDO_MRQ_006B4C50.txt |
| fabryka (wariant avatar) | 0x0043EAE0 | `CALL 007ce1e0` @0x0043EBA5 → pair {0x66,A} FUN_0043c700 | S10_DISASM_CALLER_0043EAE0.txt |
| pair-insert {type,value} | 0x0043C700 | pair-keyed RB-tree insert (key: node+0x10, node+0x14) | S13_PSEUDO_emitter_0043c700.txt |
| ArkModelManagerMain create | 0x006C0D50 | `*obj = ArkModelManagerMain::vftable` (RTTI) | S16_PSEUDO_objcreate_006c0d50.txt |
| cache get-or-create | 0x00799930 | vtable[+4]/[+8]/[+0x14]/[+0xC]/[+0x10] | S18_PSEUDO_loadbyname_00799930.txt |
| BNT2 store reader | 0x00967D00 | ref "BNT2" @0x00967F5C (`68 ??`/DATA do 0xA9BF2C) | S18_PSEUDO_BNT2_00967D00.txt |
| RM-init (rejestracja .nif/.bvi/…) | 0x0041DAE0 | PUSH 0xa7a774 @0x0041F1E9/@0x0041F23C; ".bvi" @0x0041F51C/@0x0041F56F; ".amu" @0x0041F47B; ".tdf" @0x0041F4CE | S14_DISASM_rm_init_0041dae0.txt |
| tester ".nif" | 0x007EE5F0 | `_stricmp(x,".nif")==0`; wpis w tabeli klas @0x00A9026C | S5_PSEUDO_REF_007EE5F0.txt + file-table dump (log) |

## E.2 Stringi ery (census)

- 9.3.5 ZAWIERA pełną warstwę ArkVFS02: "ArkVFS02"×2 + "ArkVFS01" (obsługa obu wersji magii),
  "Parameters\templates.vfs", "Parameters\hierarchy.vfs", "Parameters\Materials.vfs",
  "parameters\sids.vfs" (lowercase), "\TerrainImageCache1/2.vfs", ".vfs" ext.
  → w PE2/2003 (kanon TEMPLATE_READER_GHIDRA_R1, hash 561789…): ZERO — potwierdzenie
  niezależne, że era 9.3.5 wprowadza reader ArkVFS02. (Fakt era-contrasted; adresy PE2 NIE są
  używane w żadnym pomiarze tego runu.)

## E.3 Kontrola wrong-ID (negatywna, byte-logic)

Predykat śladu: lookup(id) → obiekt → walidacja → get A → request {0x66, A}.
Kontrola: id nieistniejące (999,999,999):
1. FUN_004d1430 zwraca header drzewa → FUN_0072f580 zwraca sentinel **0x00BA5800**
   (`b8 00 58 ba 00` MOV EAX,0xba5800 @0x0072F5A5).
2. Sentinel leży w .data-bss: VA 0x00BA5800 > raw-end .data (0xB6C000+212,992=0xBA0000)
   → bajty zainicjalizowane zerem (S3: virtual_size 251,620 > raw_size 212,992).
3. Walidacja FUN_0072fce0: `CMP [ECX],0` (id2==0) → JZ → return 0 → **UNIEWAŻNIA** dalszy
   ślad (w FUN_0043EAE0: JZ 0043eb3c przeskakuje get-A+insert; w FUN_006B4C50 gałąź pomija
   się przez warunek zasobu).
4. Data-level: "999999999.nif" NIE istnieje w Models.bnt; "999999999.bvi" NIE istnieje
   w Volumes.bnt (kontrola skanem, log w 01_RAW\S1_ANCHOR_RESULT.json / skan negative).
Wniosek: predykat śladu jest selektywny — działa tylko dla realnych template'ów.

## E.4 Kontrola generyczności sibling (4508 vs 4752 vs 2249)

- Te SAME funkcje czytają wszystkie rekordy: pętla w FUN_0072fa30 iteruje po WSZYSTKICH
  id z indeksu (FUN_00972df0 → lista); parser FUN_00730c90 jest bez-id-owy (strumień).
- Data-level: A każdego siblinga nazywa realny wpis: "126740.nif" (395,268,719),
  "278453.nif" (395,268,746), "296445.nif" (395,268,773) — trzy kolejne wpisy BNT2.
- B każdego siblinga: "126741.bvi" (3,701,883), "278454.bvi" (3,701,910),
  "296446.bvi" (3,701,937) — trzy kolejne wpisy w Volumes.bnt.
- Brak jakiejkolwiek stałej 296445/4508/296446/126740/278453 w łańcuchu (0 hitów imm32 w
  29 funkcjach łańcucha — niezależny skan QC; rekalibracja PERSIST własnym skanem .text).
  Jedyne hardcode'y id w consumerach to avatar-sloty: 11769 (0x2DF9) @0x00511245
  (fun. FUN_00511070) oraz rodzina 11655/11656 (+obliczany 11657) dla FUN_006b28e0 —
  POZA ścieżką generyczną.
  [POST-QC F1 2026-09-13: pierwotne stałe avatar (poprzednia wersja dokumentu; dokładne
  wartości w QC_REPORT F1) nie istnieją w .text jako imm32 (skan rekalibracyjny: 0 hitów;
  istnieją wyłącznie jako wartości u32 w tabeli .rdata @0x00A85838/0x00A8583C, bez xref
  z .text); wniosek bramki GATE-NC (generyczność ścieżki) NIEZMIENIONY — niezależnie
  potwierdzony przez QC.]

## E.5 ERA assertion (GATE-ERA)

- Wykluczenie transferu: w S1..S20 nie użyto żadnego adresu PE2 (FUN_005977b0, 0x1C,
  vtable[0x50], FUN_00478950 itd. występują wyłącznie jako OPIS wzorca w 02_ANALYSIS/C
  i w notkach kontraktu — nigdy jako pomiar). Adresy CONT R1/R2 (FUN_00971ad0, FUN_00972ad0,
  FUN_0094bd30, FUN_00959090, FUN_00823c10, FUN_00415670, FUN_0094e470) to LEADY z TEGO
  samego binarium (SHA E7785430 — zgodność potwierdzona w raportach tamtych runów),
  każdy ponownie wyznaczony własną dekompilacją/disasmem w tym runie (S5-S20).
- Hashe binarium weryfikowane fail-closed w S1 (asercja == E7785430...) i ponownie w S3.
