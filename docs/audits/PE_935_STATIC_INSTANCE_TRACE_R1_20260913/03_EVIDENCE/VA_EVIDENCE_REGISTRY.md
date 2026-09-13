# 03_EVIDENCE — Rejestr dowodowy VA (każde twierdzenie → era/hash → VA/instrukcja → artefakt)

ERA: EU 9.3.5 (pcg_install). Binarium: Entropia.exe SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, 8,015,872 B.
S0 (asercja własna, fail-closed): 01_RAW\S0_ERA_ASSERTION.json — SHA==kanon, PE 5 sekcji,
image_base 0x00400000, dll_chars 0x0000 (ASLR OFF), spot-check VA→file-offset (entry 0x0095DA11→5,626,385 = .text; 0x00A86D30→.rdata). Mapping rule zapisana w S0.

## E.1 Oracle NiAVObject (VA-locked) — podstawa Z4
| element | VA | kluczowe bajty/dowód | artefakt |
|---|---|---|---|
| m_bAppCulled @+0x20 | 0x007C053A | `8a 45 20` MOV AL,[EBP+0x20]; PUSH 0xa8d8ac ("m_bAppCulled") | GA2_DISASM_FUN_007c04f0.txt |
| m_kLocal.m_Translate @+0x5C | 0x007C0580→0x007C05B3 | `68 98 d8 a8 00` PUSH "m_localTranslate"; `8d 4d 5c` LEA ECX,[EBP+0x5C] — dla m_localRotate LEA [EBP+0x38] | GA2_DISASM_FUN_007c04f0.txt |
| m_kWorld.m_Translate @+0x90 | 0x007C0620 | PUSH "m_worldTranslate"(0xa8d864); `8d 8d 90 00 00 00` LEA ECX,[EBP+0x90]; m_worldRotate LEA [EBP+0x6C] | GA2_DISASM_FUN_007c04f0.txt |
| m_kWorldBound @+0x28 | 0x007C06C6 | PUSH "m_kWorldBound"(0xa8d834); `8d 4d 28` | GA2_DISASM_FUN_007c04f0.txt |
| stringi NIF-token | 0x00A8D7D0-0x00A8D8BC | '***dpvs*', m_kWorldBound/…/m_bAppCulled, 'NiAVObject' | S2_STRING_CENSUS_ALL.txt; zgodność 1:1 z Gb12 NiAVObject.cpp GetViewerStrings |

## E.2 Setterzy transformu rekordu placementu (Z4 slice S-A)
| element | VA | bajty | artefakt |
|---|---|---|---|
| FUN_00730f90 (pozycja vec3 @+0x08) | 0x00730F90 | `MOV [param+8],*p; MOV [param+0xC],p[1]; MOV [param+0x10],p[2]` | GA8_PSEUDO_00730F90.txt |
| FUN_00730fb0 (rotacja @+0x14) | 0x00730FB0 | MOV [param+0x14/0x18/0x1C] | GA8_PSEUDO_00730FB0.txt |
| FUN_00730fd0 (@+0x20/+0x24) | 0x00730FD0 | MOV [param+0x20],*p; [param+0x24],p[1] | GA8_PSEUDO_00730FD0.txt |
| FUN_00730f60 (init 11 dwordów) | 0x00730F60 | *param=0..param[10]=0 | GA8_PSEUDO_00730F60.txt |
| wywołanie w FUN_00567770 (ECX=lokal @ESP+0xB4) | 0x00567906 | `8d 8c 24 b4 00 00 00` … (kontekst @0x005678F0: 4× LEA ECX,[ESP+0xB4] + CALL-y) | S9-read + GA8_PSEUDO_00567770.txt (GA5) |
| reader atrybutów (switch 0x6A4/0x6A5/0x6A8/0x6A9) | 0x00846840 | body 0x00846840-0x00846B8A | GA8_PSEUDO_00846840.txt |
| rejestracja (map-insert z nazwą) | 0x00457930 | body 0x00457930-0x00457BFB, basic_string lokal | GA8_PSEUDO_00457930.txt |

## E.3 Twórca instancji modelu (Z4 slice S-B; Z6 domknięty)
| element | VA | bajty/dowód | artefakt |
|---|---|---|---|
| FUN_006cb6f0 (cache→pump→ref→instancja) | 0x006CB6F0 | pump CALL @0x006CB7CF `e8 2c df ff ff`; new(0xC) CALL 0x0095d3c4 @0x006CB81B-0x006CB819 | GA5_DISASM_006CB6F0.txt; GA5_PSEUDO_006CB6F0.txt |
| ctor ArkModelResourceInstanceRef | 0x006FA8B0 | `c7 00 b8 64 a8 00` MOV [EAX],0xa864b8; `89 48 08` MOV [EAX+8],ECX; RET 4 | GA3_CTOR_ArkModelResourceInstanceRef_006FA8B0.txt |
| dtor (baza ArkRefObject 0x00A864B0) | 0x006FA8D0→0x006FA952 | `c7 06 b0 64 a8 00` | jw. |
| twórca instancji nazwanej "<id>__<name>" 0x110 B | 0x006CB020 | stringstream + `operator_new(0x110)`; check "ArkAnimation" (FUN_007b6c30) | GA6_PSEUDO_006CB020.txt |
| pending-attach queue processor | 0x006CB3C0 | type@+0x5C, A@+0x64; CALL FUN_006f2af0 reset | GA5_DISASM_006CB3C0.txt |
| reset pending (NIE transform) | 0x006F2AF0 | `d9 05 34 b3 a7 00` FLD const1.0; zapisy +0x68/+0x5C/+0x6C/+0x60/+0x64 | GA5_DISASM_006F2AF0 (GA4_PSEUDO_006F2AF0.txt) |

## E.4 Kwalifikacja FUN_006b4c50 (Z2a) — AVATAR
| element | VA | dowód | artefakt |
|---|---|---|---|
| FUN_006b4c50 body | 0x006B4C50 | sloty FUN_006c2840/FUN_006c2870 → A×2 → pump×2 → attach | S20_PSEUDO_MRQ_006B4C50.txt (poprzedni run, bajtowo re-weryf. S9) |
| jedyny caller: FUN_006b9970 | 0x006B9970 | vtable-call `(**(..+0x44))("CharacterPosition")` — węzeł pozycji postaci; potem odczyt [node+0x64] | GA5_PSEUDO_006B9970.txt |
| upward: FUN_00489810 | 0x00489810 | chain RM (FUN_00423b10→004b9ec0→00414670→0043c5a0), getter A, płeć FUN_006c1f60(2-(stan!=1)), potem FUN_006b9970 | GA6_PSEUDO_00489810.txt |

## E.5 Wzorce 4508 (Z3)
| wzorzec | instrukcja (VA, bajty) | funkcja | artefakt |
|---|---|---|---|
| 0x0053270C | LEA ECX,[ESP+0x119C] @0x00532709 `8d 8c 24 9c 11 00 00` | FUN_0052d6d0 (0x0052D6D0-0x005388BE); caller FUN_005388c0 | GA1_PATTERNS.json + GA1_PATTERN_WINDOWS.txt |
| 0x00532769 | LEA ECX,[ESP+0x119C] @0x00532766 `8d 8c 24 9c 11 00 00` | FUN_0052d6d0 | jw. |
| 0x0083427E | MOV [ESI+0x119C],EBX @0x0083427C `89 9e 9c 11 00 00` | FUN_00834010 = ctor **ArkCommunicator** (vft @ dekompilacie; RTTI) | jw. + GA1 disasm okno |
| IAT przy wzorcach | 0x00A75A38=allocator<char>, 0x00A75A40=~allocator, 0x00A75A5C=~basic_string (symbole Ghidra PTR_*) | — | GA1_IAT.json |

## E.6 RTTI/vtable (Z1/Z4; metoda COL offline S4 + Ghidra GA3)
- TypeDescriptor→COL→vtable: 41 klas wyznaczonych (S4_RTTI_VTABLES.json). Przykłady:
  ArkObject vft 0x00A86B48, ArkObjectClass vft 0x00A86850, ArkPortalCell vft 0x00A91CF8,
  ArkModelResourceInstanceRef vft 0x00A864B8, ArkSceneObject vft 0x00A98050,
  NiAVObject vft 0x00A8D534, NiNode vft 0x00A8CCF4.
- ctor ArkObject: FUN_00726e70 @0x00726E70 — `*this=ArkObject::vftable`;
  **[this+0x28]=FUN_007ce1e0(param_1)** — getter A z obiektu template'u (GA4_PSEUDO_00726E70 nie ma — w GA3_CTOR_ArkObject_00726E70.txt).
- ArkObjectClass::create (vtable slot 1): FUN_0070bf50 — operator_new(0x58) → FUN_00726e70.
- Per-class factory: FUN_007351e0 = ctor ArkSurgeonObject (template globalny DAT_00ba58cc).

## E.7 Kontrole negatywne i dane
- Round-trip 8/8 (S3_ROUNDTRIP_4508.json): pack→unpack wszystkich ID przed skanem.
- Skan .text: 4508 LE = dokładnie 3 (kontraktowe VA), BE = 0, 296445 = 0
  (S3_ROUNDTRIP_4508.json → text_scan).
- Bajtowa re-weryfikacja censusu: 25 lookup + 13 pump — **38/38 zgodnych, 0 mismatch**
  (S9_BYTE_VERIFY.json).
- "460563.nif" (hardcode 0x70D17 @FUN_0093be20): 0 hitów w Models.bnt (skan z terminatorem
  0x0A, kalibracja: 296445.nif@395,268,773 = 1 hit, 126740.nif@395,268,719 = 1,
  278453.nif@395,268,746 = 1); 460563 — 0 hitów też w Portals/TEZ/Volumes/VegetationClimates.
- Datowy census instalacji: patrz Z5 §3 (brak Sectors.xbc/Objects.pak/Planets.pak w 9.3.5).

## E.8 ERA (GE-ERA)
- Wszystkie VA z TEGO binarium (SHA E7785430… asercja S0 fail-closed).
- Gb12_Source użyty WYŁĄCZNIE jako oracle semantyki setterów NiAVObject (kolejność
  viewer-strings + NiTransform layout); zero transferu PE2/2003 (adresy PE2 nie występują
  w żadnym pomiarze; poprzedni run E.5 re-cytowane tylko jako census call-site'ów z
  re-weryfikacją bajtową).
- Stare dumpy S10/S20/S12/S14 poprzedniego runu użyte jako dekompilacje TEGO samego
  binarium (projekt Ghidra GHIDRA_LOCAL — ten sam program, ten sam SHA; każdy kluczowy
  wniosek ma dodatkowo WŁASNY dump z tego runu GA1-GA8).
