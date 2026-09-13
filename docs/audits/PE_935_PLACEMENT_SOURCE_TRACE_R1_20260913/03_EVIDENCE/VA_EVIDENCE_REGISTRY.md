# 03_EVIDENCE — Rejestr dowodowy VA (każde twierdzenie → era/hash → VA/instrukcja → artefakt)

ERA: EU 9.3.5 (pcg_install). Binarium: Entropia.exe SHA256
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, 8,015,872 B.
S0 (asercja własna, fail-closed): 01_RAW\S0_ERA_ASSERTION.json — SHA==kanon, PE 5 sekcji,
image_base 0x00400000, dll_chars 0x0000 (ASLR OFF), spot-checki VA→file-offset
(entry 0x0095DA11→5,626,385 .text; RTTI TD w .data; stringi w .rdata).
Mapping: file_offset = section.raw_ptr + (VA − section.va_start).
Surowe bajty każdego VA: 01_RAW\S14_VA_EVIDENCE.json (64 wiersze; ten plik
= rejestr odczytu; bajty z S14, artefakty z 01_RAW\ghidra_output).

## E.1 System atrybutów — kontener i walker-y (Z1a)
| element | VA | bajty (S14) | artefakt |
|---|---|---|---|
| singleton getter (manager 0x8c) | 0x004154F0 | zob. S14 | ZS1_PSEUDO_004154F0.txt (RUN3) + ZS1_PSEUDO_008550C0 |
| ctor managera (3× CS + mapa) | 0x008550C0 | zob. S14 | ZS1_PSEUDO_008550C0.txt |
| walker start (singleton+resolve) | 0x0085B840 | zob. S14 | ZS1_PSEUDO_0085B840.txt |
| resolve klucza→[hit+8] (map find) | 0x008544D0 | zob. S14 | ZS2_PSEUDO_008544D0.txt |
| lock/unlock | 0x00413440/50 | zob. S14 | ZS1_PSEUDO_00413440.txt |
| walk-init (key→FUN_00841920) | 0x00843D60 | zob. S14 | ZS2_PSEUDO_00843D60.txt |
| container z encji ([obj+4]) | 0x00844130 | zob. S14 | ZS2_PSEUDO_00844130.txt |
| fetch pozycji (0x6A4/0x6A5/0x6A8/0x6A9) | 0x00846840 | zob. S14 | GA8 (RUN3) + ZS1 walidacja S5 |
| fetch trójki +0x68/0x6c/0x70 | 0x00854720 | zob. S14 | GA8 (RUN3) |
| SETTER atrybutu | 0x00845F70 | zob. S14 | ZS3_PSEUDO_00845F70.txt; 53 callerów (ZS3_CALLERS) |
| GETTER int / float / check | 0x008452D0/0x00845360/0x00844020 | zob. S14 | ZS3/ZS1 |
| filtr transformu {0x6a8,0x6a9,0x6a4,0x6a5,0x6ac,0x23} | 0x00846430 | zob. S14 | ZS2_PSEUDO_00846430.txt |
| resolver par typów (3 palety UI) | 0x006BD1B0 | — | ZS2_PSEUDO_006BD1B0.txt |

## E.2 Producenci/dispatchery atrybutów (Z1b/iii)
| element | VA | dowód | artefakt |
|---|---|---|---|
| dispatcher zmiany atrybutu (attach modelu, skala 1.0; 0x39=model, 0x42=0x66) | 0x0043F4B0 | CMP 0x6a4/0x6a5/0x6a8/0x6ac/0x23 | ZS2_PSEUDO_0043F4B0.txt |
| propagacja (0x2720/0x271f/0x3f3) | 0x005146B0 | CMP 0x6a4/0x6ac/0x6a5 | ZS2_PSEUDO_005146B0.txt |
| setter rodziny 0x6a5 (+0x271b/0x271c=0x6ac) | 0x004387A0 | PUSH 0x6a5 ×2 | ZS2_PSEUDO_004387A0.txt |
| dispatch typu {0x6a4/0x6a5→0x619fa; 0x6a8/0x6a9→0x619f9} | 0x00847270 | CMP chain | ZS2_PSEUDO_00847270.txt |
| konstruktor-walker (0x4e34/0x38b0/0x4e38; +0x44..+0x4c pozycja) | 0x008553D0 | 7 callerów | ZS1_PSEUDO_008553D0.txt |
| handler transform (write 0x2b/0x2c; tabela .rdata) | 0x00514EF0 | DANE-xref @0x00A7D778 | ZS2_PSEUDO_00514EF0.txt; ZS10_ALL_REFS.json |
| tabela handlerów CWO-Logic | 0x00A7D764 | run 16 wskaźników | S13_CWO_HANDLER_TABLE.json |
| string assert CWO-Logic | 0x00A7D624 | 'ArkClientWorldObjectLogic::OnDelayedTextureUpdated' | S13 (rows_text) |

## E.3 Łańcuch buildera rekordu placementu (Z2)
| element | VA | dowód | artefakt |
|---|---|---|---|
| builder rekordu (settery f60/f90/fb0/fd0) | 0x00567770 | disasm okno 0x00567860-0x00567960 | GA5 (RUN3) + ZS2_DISASM_FUN_00567770_setter_calls.txt |
| 3-drogowy driver | 0x00567C50 | call @0x0056836C | ZS1_PSEUDO_00567C50.txt + ZS2_DISASM okno |
| droga A (update CWO) | 0x0058DB50 | call @0x0058E0B7; FUN_0058db50 callerzy: FUN_00468910 ×3 | ZS2_PSEUDO_0058DB50.txt; ZS10_CALLERS |
| droga B (komunikat 0xB9) | 0x005B72C0 | case 0xb9 w FUN_004b18d0 | ZS3_PSEUDO_004B18D0.txt |
| droga C (tabela .rdata) | 0x00514EF0 | DANE @0x00A7D778 | ZS2_PSEUDO_00514EF0.txt |
| silnik update (state machine 0x6a4/0x6a8) | 0x00468910 | 12 callerów; FUN_0058db50 ×3 | ZS2_PSEUDO_00468910.txt; ZS10 |
| capacity-push (arg D) | 0x00567B40 | capacity [obj+0x40..0x60] | ZS4_PSEUDO_00567B40.txt |

## E.4 Kolejka/executor/komunikacja (Z1b/ii, Z2)
| element | VA | dowód | artefakt |
|---|---|---|---|
| CommunicationSubsystem ctor (executor@+0x28) | 0x00419DD0 | RTTI verbatim w pseudo | ZS6_PSEUDO_00419DD0.txt |
| executor ctor (0x34 B) | 0x004B15F0 | MOV [ESI],0xa7c1fc | ZS5_PSEUDO_004B15F0.txt |
| executor Execute | 0x004B2950 | gate FUN_0042bc20 | ZS1_PSEUDO_004B2950.txt; ZS6_DISASM_FUN_004b2950_full.txt |
| dispatcher typów (0xA2–0xC6; case 0xB9) | 0x004B18D0 | switch | ZS3_PSEUDO_004B18D0.txt |
| enqueue ring {type,x,payload} | 0x004B1890 | 12B entries | ZS4_PSEUDO_004B1890.txt |
| cursor advance | 0x0040DE60 | 703 call-site'y (ZS8) | ZS7_PSEUDO_0040DE60.txt; ZS8_CURSOR_CALL_SITES.json |
| odczyt wpisów kolejki t1/t2 | 0x00752700/0x00752640 | {u32,u32,u8,u8}/{u32,u32,u8} | ZS4_PSEUDO_00752700.txt |
| klon payloadu (memcpy) | 0x0040E0D0 | operator_new+memcpy | ZS7_PSEUDO_0040E0D0.txt |
| odbiór sieci (ntohl, ramki 0x11–0x13) | 0x00833EA0 | ntohl @+0x20/@+0x1C | ZS5_PSEUDO_00833EA0.txt |
| ArkStaticPacket parse (protokół połączenia) | 0x008310D0 | chunki 0xFE (FUN_00839a50), 0xFF-ack | ZS4_PSEUDO_008310D0.txt |
| StaticPacket ctor | 0x00830030 | MOV [ESP+8],0xa91a44 | ZS2_VTABLESTORE_CONTAINING.json |
| vtable executora | 0x00A7C1FC | [004B1210, 004B2950] | S4b + S14 |

## E.5 Kanał FILE (Z1b/i)
| element | VA | dowód | artefakt |
|---|---|---|---|
| store "Data\Parameters\" (0xa4, VFS reader) | 0x0094DFC0 | singleton DAT_00ba8df4 | ZS2_PSEUDO_0094DFC0.txt |
| string ścieżki | 0x0094BA00 | 'Data\Parameters\' | ZS1_PSEUDO_0094BA00.txt |
| parser VFS (kursor) | 0x00730C90 | RUN3 (templates.vfs) | ZS8 census (PUSH 0x1/0x2/0x4) |
| VFS reader store'u | 0x00972DF0 | — | ZS7_PSEUDO_00972DF0.txt |
| brak 20006.vfs (negatyw) | — | census Data\Parameters (20 plików) | listing + S5 (29 trafień 0x4E26 w .text) |

## E.6 Pole D (Z4)
| element | VA | bajty | artefakt |
|---|---|---|---|
| getter D dword | 0x0048ADA0 | 8B 41 10 C3 | S9 + ZS3_CALLERS (80) |
| getter D f32 | 0x00861240 | D9 41 10 C3 | S9 + ZS3_CALLERS (10) |
| getterzy B/A/C | 0x00746550/0x007CE1E0/0x006B22D0 | 8B 41 04/08/0C C3 | S9 + census |
| consumer D w gałęzi 0x4e38 (selektor 4/5→2, 6→3, 7→4) | 0x008553D0 | — | ZS1_PSEUDO_008553D0.txt |
| consumer D w push kolejki | 0x00567B40 | — | ZS4_PSEUDO_00567B40.txt |

## E.7 Portals/.prt (Z3)
| element | VA | dowód | artefakt |
|---|---|---|---|
| fabryka slot1 (create+parse) | 0x0084B270 | operator_new(0x14)→FUN_00852a90→FUN_0084f7a0 | ZS1_PSEUDO_0084B270.txt |
| item ctor (CellGraph@+0x10) | 0x00852A90 | MOV [ESI],0xa91d04 + new(0x58) | ZS3_PSEUDO_00852A90.txt |
| graph reader (u16; sub; u32 count; cells) | 0x00852750 | disasm 133 wiersze | ZS9_PSEUDO + ZS9_DISASM_FUN_00852750_full.txt |
| cell tag-reader (vtable slot1) | 0x00852A30 | tag==1→sub | ZS1_PSEUDO_00852A30.txt |
| cell-readers | 0x00852BF0/0x00852D60 | u16@+0x8c, u32@+0x0c | ZS9_PSEUDO |
| index BNT (stopka) | 0x13B22 (file) | [73218]['BNT2'] | S11B_PORTALS_INDEX.json |
| negatyw ID w .prt | — | 0 trafień ×13 anchorów ×276 plików | S12_PRT_CONTENT_CHECK.json |

## E.8 Klasy i vtable'e (RTTI, metoda COL — S4b)
ArkParameterContainer TD 0x00B8ED0C → vtable 0x00A8784C [slot0 FUN_00761230
(create, vtable-store @0x00761278); slot1 0x008E0010; slot2 0x009154A0; slot3
0x007263E0; slot4 0x008E0110; slot5 0x00726340] (bazowe sloty ArkObject vtable
0x00A86B48 [0x00764740, 008E0010, 009154A0, 007263E0, 008E0110, 00726340]).
ArkParameterTransformation vtable 0x00A877DC [slot0 FUN_00760FE0].
ArkObjectClassImpl<ArkParameterContainer> vtable 0x00A86FBC [0x0073C2A0,
**0x0073A160=create**]; <ArkParameterTransformation> 0x00A86F98 [create
FUN_00739E30]; <ArkRealWorldItem> 0x00A8701C [create FUN_0073A9E0];
<ArkRealWorldProvider> 0x00A87028 [FUN_0073AAF0]; <ArkInteractiveWorldObject>
0x00A87010 [FUN_0073A8D0]. Class-id (FOURCC w manglingu, bajty: EODN/EODO/EOEC/
EOCP/FNMJ — S6: wyłącznie w stringach RTTI, brak dwordów klas w .text/.data).
ArkPortalResourceItemFactory vtable 0x00A91C88 [0x0041B870, 0x0084B270, 0x008E0010];
ArkPortalResourceItem 0x00A91D04; ArkPortalCell 0x00A91CF8 [0x00850C50, 0x00852A30];
ArkPortalCellGraph 0x00A91CB4 [0x0084EC00, 0x0084E7F0, 0x0084D650, 0x0084D750,
0x0084C2C0].

## E.9 Kontrole (§11)
- Round-trip: S5 (wszystkie skanowane wartości), S9 (stuby), S10, S12 (assert) ✓.
- Finiteness: nagłówki .prt f32 finite (S11B), wartości D w dumpach bez NaN/Inf ✓.
- Negatywy: 0x66AA (instrukcja-koincydencja wykluczona), .prt-bez-ID, brak
  20006.vfs, STATIC_WORLD=0 (RUN 3 — bez zmian) ✓.
- Pułapki: LEA [ESP+0x6a4/0x6a8] (stack), FSTP [ESI+0x6a4] (pole klasy),
  JNZ/JZ/CALL-koincydencje — wszystkie z powodami (Z5 §3) ✓.
- ERA: wszystkie VA z TEGO binarium (SHA E7785430… S0 fail-closed); zero
  transferu PE2/2003; Gb12 tylko jako oracle (RUN 3, bez zmian).

## E.10 Skrypty i hashe (hash-after-final-edit)
Wszystkie skrypty control (00_CONTROL) i ich SHA256: 00_CONTROL\SCRIPT_SHA256.csv.
Ghidra postScripty zs1-zs10 — wykonywane z projektu GHIDRA_LOCAL (kopia lokalna
manifestu RUN 3; hashes w GHIDRA_LOCAL_MANIFEST_SHA256.csv — niezmienione).
