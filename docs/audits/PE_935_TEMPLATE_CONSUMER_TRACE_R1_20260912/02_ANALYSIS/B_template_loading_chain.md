# 02_ANALYSIS — B. Łańcuch ładowania template + konsument pola A (code trace, VA-locked)

RUN: PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912 | ERA: EU 9.3.5 | Entropia.exe SHA256 E7785430...
Image base 0x00400000, brak ASLR (S3_PE_HEADER.json). Każde VA z surowymi bajtami w
01_RAW\ghidra_output\S*_DISASM_*.txt; wszystkie dekompilacje własne, w TYM binarium.
Żaden adres z PE2/2003 nie był użyty (GATE-ERA asercja — patrz 03_EVIDENCE\ERA_ASSERTION.md).

## B.1 W pełni zablokowany bajtowo łańcuch wczytyania rekordu (od pliku do rejestru)

| # | ogniwo | funkcja @VA | dowód (surowe bajty + dekompilacja) |
|---|---|---|---|
| 1 | loader templates.vfs | FUN_0072fa30 @0x0072FA30 | disasm S7_DISASM_loader: PUSH 0xA86D30 ("Parameters\\templates.vfs") @0x0072FAAC; wywoływany z FUN_00452490 (EAX=FUN_0043a550(); ECX=EAX; JMP) |
| 2 | budowa ścieżki | FUN_00401e70 @0x00401E70 | [ESI]=this(string), arg = DAT_00b6c3d8 (bazowy katalog, runtime-init) + "Parameters\\templates.vfs" |
| 3 | otwarcie VFS + magia | FUN_00972df0 @0x00972DF0 | CreateFileA; ReadFile(8B); FUN_00408b60(buf,"ArkVFS01") @0x00973010, potem FUN_00408b60(buf,"ArkVFS02") @0x0097302x; dla ArkVFS02: ver=2 @+0xa0, u32 z nagłówka → +0x8c = **base stride**; potem FUN_00972ad0 |
| 4 | budowa indeksu | FUN_00972ad0 @0x00972AD0 | pętla: GetFileSize/SetFilePointer; FUN_0040e260(handle,0x10) = read 16-B header {id,size,ver,crc32}; węzły: FUN_00972280 / FUN_009721d0 (id, size, offset, crc do drzewa id: FUN_00971780 lookup po id); seek forward = FUN_00979d00 |
| 5 | wzór stride | FUN_00979d00 @0x00979D00 | `MOV EAX,[ECX+4]; MOV ECX,[ECX+0x14]; ADD EAX,0xF; XOR EDX,EDX; DIV ECX; ADD EAX,1; IMUL EAX,ECX; ADD EAX,-0x10` = **(floor((size+15)/base)+1)*base − 16** bajtów relatywnie; tożsame z empiryczną regułą S2 (walk 5438/5438 do EOF) |
| 6 | odczyt rekordu | FUN_00971ad0 @0x00971AD0 | lookup id: FUN_00971780(VFS+0x50); seek: FUN_00979d20 = `[node+0x10]+0x10`; read [node+4] B: FUN_0040e260; stream.cursor=0 (@0x00971B3E), valid=1 (@0x00971B41) |
| 7 | bramka CRC32 | FUN_004063d0 @0x004063d0 | klasyczny CRC-32 (init 0xFFFFFFFF, tabela FUN_00406110, `crc>>8 ^ table[(b^crc)&0xFF]`, finalny ~); porównanie z [node+0xC] (FUN_006b22d0) @0x00971B67: `CMP [ESP+0x18],EAX; SETZ BL` |
| 8 | parser rekordu | FUN_00730c90 @0x00730C90 | payload u32 po u32: [EDI+0x00]=p[0] id2 (@0x00730CB6), **[EDI+0x08]=p[1] A** (@0x00730CE6), [EDI+0x04]=p[2] B (@0x00730D14), [EDI+0x0C]=p[3] C (@0x00730D42), [EDI+0x10]=p[4] D_f32 (@0x00730D..); sub1 lista stringów: FUN_00730b70 → +0x14 (vector<string>, append stride 0x20); sub2 lista u32: FUN_00730970 → +0x20 (vector<u32>); [EDI+0x2C]=p[6] F |
| 9 | konstruktor obiektu | FUN_00730700 @0x00730700 | zerowanie pól +0x00..+0x2C oraz **FLDZ / FSTP [EAX+0x10]** — pole +0x10 jest F32 (PARAM/D) |
| 10 | rejestracja | FUN_005670a0 (copy-ctor do węzła) + FUN_0072f8d0 @0x0072F8D0 | STLport _Rb_tree insert, klucz = **id2** (FUN_004123d0 = `MOV EAX,[ECX]` @0x004123D0); this = obiekt loadera (MOV ECX,[ESP+0x3C] @0x0072FBD4) |
| 11 | singleton rejestru | FUN_0043a550 @0x0043A550 | globalny slot **DAT_00ba1824**; new(0x18) + ctor FUN_0052a260 → obiekt = std::map (nagłówek _Rb_tree + licznik) |
| 12 | lookup w rejestrze | FUN_0072f580 @0x0072F580 | FUN_004d1430 (RB-tree find) → found: **value = node+0x14** (@0x0072F59E `ADD EAX,0x14`); brak: sentinel **0x00BA5800** |
| 13 | walidacja | FUN_0072fce0 @0x0072FCE0 | `CMP [ECX],0 / JZ → 0`; valid iff id2≠0 **ORAZ** (A≠0 LUB B≠0 LUB C≠0) — A/B/C = trzy sloty zasobów (dowód bajtowy) |
| 14 | **getter A** | FUN_007ce1e0 @0x007CE1E0 | `MOV EAX,[ECX+0x8]; RET` (8b 41 08 c3) |
| 15 | **żądanie modelu** | FUN_006c9700 @0x006C9700 | `local_14 = 0x66` (**kod typu zasobu MODEL**), potem FUN_00415670 (singleton ArkResourceManager, slot DAT_00ba12f4, obiekt 0x98) + FUN_00823c10 (dispatcher) |
| 16 | dispatcher provider-chain | FUN_00823c10 @0x00823C10 | RB-tree find (FUN_004d1430) → node+0x24 = obiekt providera → **wywołania wirtualne `(**(code**)(**(int**)(node+0x24)+4))(...)` i `[+0x38]`**; przy braku zasobu: FUN_008237d0 (kolejkowanie pary {type,id}) |
| 17 | konsument kompletny (A→request) | FUN_006b4c50 @0x006B4C50 | `FUN_006c2840()` (resolver slotu→TemplateObject) → **`iVar2 = FUN_007ce1e0()`** (A) → drugi slot (FUN_006c2870) → **`FUN_006c9700(iVar2,...)` i `FUN_006c9700(local_40,...)`** → wynik → encja (+0x1b8/+0x1bc), release starego przez vtable[+0xA8] |
| 18 | wariant consumera (avatar) | FUN_00511070 → FUN_0043eae0 @0x0043EAE0 | lookup(hardcoded id 11769 (0x2DF9) @0x00511245) → walidacja → **`FUN_007ce1e0(EBP)` = A @0x0043EBA5** → para {**0x66, A**} → FUN_0043c700 (insert do pair-keyed map requestera); request struct {factory=0x43eae0, mgr, id, id2, A,...} budowany przez FUN_0050d8c0; obiekt docelowy: new(0x130) → FUN_006c0d50 → **`*obj = ArkModelManagerMain::vftable`** (RTTI Ghidra) |
| 19 | cache get-or-create | FUN_00799930 @0x00799930 | vtable[+4] hash → bucket; vtable[+8] compare; hit: [+0x10] touch; miss: [+0x14] create → [+0xC] attach |
| 20 | store BNT2 | FUN_00967d00 @0x00967D00 | referencja do stringa **"BNT2" @0x00A9BF2C** @0x00967F5C (jedyny hit magii w binarium); parser indeksu BNT2 (tree walk po footerze) |

[POST-QC F1 2026-09-13 — ogniwo 18: poprawiono stałe avatar-hardcode. Pierwotne stałe
avatar (poprzednia wersja dokumentu; dokładne wartości w QC_REPORT F1) nie istnieją
w .text jako imm32 (skan rekalibracyjny: 0 hitów; istnieją wyłącznie jako wartości u32
w tabeli .rdata @0x00A85838/0x00A8583C, bez xref z .text).
Realne stałe: 11769 (0x2DF9) @0x00511245 w FUN_00511070 (ogniwo 18 — MOV EAX,0x2DF9,
imm32 @0x00511246, jedyny hit w .text) oraz rodzina 11655/11656 (+obliczany 11657:
MOV EAX,0x2D88 @0x006B28F6 + ADD EAX,0x2D87 @0x006B2922) w FUN_006b28e0 — obie klasy
POZA generyczną ścieżką łańcucha. Wniosek bramki GATE-NC (generyczność ścieżki; 0 hitów
296445/4508/296446/126740/278453 w 29 funkcjach łańcucha) NIEZMIENIONY — niezależnie
potwierdzony przez QC (skan imm32) i rekalibrację PERSIST (persist_p1_recalibration.py).]

## B.2 Mechanizm otwarcia zasobu modelu (rozstrzygnięcie)

FAKTYCZNY mechanizm = **generyczne żądanie resource po ID numerycznym z kodem typu**:
{type=0x66 (MODEL), id=A} → FUN_006c9700 → singleton ArkResourceManager (FUN_00415670) +
dispatcher provider-chain (FUN_00823c10) → dostawca/fabryka → zasób modelu.
NIE jest to budowanie ścieżki "%d.nif" w consumerze: konsumer przekazuje SAMO ID;
rozszerzenie ".nif" jest zarejestrowane globalnie w RM-init FUN_0041dae0 (2× PUSH 0xA7A774
@0x0041F1E9/@0x0041F23C, rejestracja ".bvi" @0x0041F51C/@0x0041F56F, ".amu" @0x0041F47B,
".tdf" @0x0041F4CE, "models\\" @0x0041E5DC/@0x0041E62A, "Cache\\" @0x0041EC46,
TerrainImageCache1/2 @0x0041EC75/@0x0041ECD3), a tester rozszerzenia ".nif" =
FUN_007ee5f0 @0x007EE5F0 (`_stricmp(x,".nif")==0`), wpisany do tabeli deskryptorów klas
loaderów @0x00A90264-74 (rekord {0x00AB0EA8, 007EE680, 007EE5F0, 007EE6A0, 007EE780}).

Wiązanie ID→plik na poziomie DANYCH (byte-proof, S-negatywne):
- A=296445 → wpis **"296445.nif" ISTNIEJE** w Models.bnt (footer BNT2, offset 395,268,773).
- siblingi: "126740.nif", "278453.nif" ISTNIEJĄ; negatywna: "999999999.nif" NIE istnieje.
- klasa readera archiwum: FUN_00967d00 (magia "BNT2" @0x00A9BF2C).
- Inventory fabryk (RTTI/boost names @0xB6D851..0xB6D9DF): ArkModelResourceItemFactory,
  ArkImageResourceItemFactory, ArkBoundResourceItemFactory, ArkPortalResourceItemFactory,
  ArkVegetationClimateFactory, ArkTerrainEditZoneFactory — provider-chain dispatchuje
  do fabryk trzymanych w boost::shared_ptr (counted_impl_p@VArk*Factory@@).

## B.3 Residuum (dokładnie gdzie łańcuch się urywa)

Między FUN_00823c10 (wywołanie wirtualne `provider_vt[+4]`/`[+0x38]` na node+0x24)
a ciałami metod providera/fabryki: **ciała metod wirtualnych providera nie zostały
zdekompilowane w tym runie** — tożsamość klasy ustalona (RTTI: ArkModelResourceItemFactory),
ale para instrukcji "create(name/id) → store read" wewnątrz fabryki nie jest VA-locked.
Zidentyfikowane samodzielnie ogniwa magazynowe (FUN_00799930 cache get-or-create,
FUN_00967d00 BNT2 reader) + wiązanie danych ("296445.nif" w Models.bnt) domykają
mechanizm dowodowo, nie instrukcyjnie.
