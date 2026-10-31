# CHARACTER_CREATION — recovered 2003-era avatar-creation knowledge

Doc version **V10** (= CHARACTER_CREATION_SCHEMA_V10.json, CHAR_J marshalling
+ control-slot map; W26 head-namespace resolution). **V10 deltas vs V9** (CHAR_J,
jobs\CHAR_J + W26, jobs\W26): (a) **GCE marshalling contract RECOVERED
(byte-proven)** — ff8f handler sets [GCE+0x14]:=VM SP before dispatch;
__thiscall 1 arg = resolved id; results at GCE+4 (f32) / +8 (int) / +0x10 (A);
the derived dispatcher 0x485260 does NOT pop the VM stack — arg pop is
CALLER-side (script ADD_SP_imm); arg layout per BASE case 227471: arg0=stream
RAW, arg1=slot DEREF, arg2=value DEREF; push order value/slot/stream-last
(the CHAR_G/CHAR_I inherited ABI is now byte-proven, not pattern-inherited).
(b) **SLOT SEMANTICS CORRECTED** (supersedes the CHAR_H "slot = validated
index only" wording): slot = RANDOM-ACCESS byte index into the serialized
CharDef parameter stream — FUN_0044F8B0 sets the copy cursor := index,
FUN_00463D40 writes buffer[cursor] with grow-if-needed; slot K = byte offset
K of the CharDef stream; the 635-ctor 46-f32 default table = the 46-parameter
default layout. (c) CHAR_I's "repeated slot-local pattern" RESOLVED: the
6051/6060/670 apply-SETs write SEQUENTIAL stream indices 0..N through a
counter cell (CLR at entry + INC after every hostcall) — pattern-local, no
control→slot information. (d) Control→slot pairing advanced: Hair type→slot
26 RECOVERED 1:1, Sex→45 RECOVERED, gender factor→39 RECOVERED anchor; 18
positional PLAUSIBLE (3 documented positional hypotheses); Mouth UNKNOWN;
17-cell structure fn 303635 + slider callback fn 208728 with per-cell slot
pairs byte-identical (double-proven read+write); CALL-227469 census corrected
44→47 sites. (e) **W26 head-mesh namespace RESOLVED**: the 20 "MESH_TABLE"
6051 ids are Textures.ark `.tga` 20/20 (128×128 uncompressed, imgtype 2);
bimodal separation both ways (hair 34/34 Models.ark; head 20/20 Textures.ark);
"2008 Models.bnt" hypothesis REFUTED (era-labelled REFERENCE_OTHER_BUILD,
checked and excluded); semantics (why a "mesh" accessor returns texture ids)
OPEN — appearance-map hypothesis; NOT decoded/rendered in W26. V9 basis
(CHAR_I: all 4 consumers decoded residue-0; COLOR palettes = NONE, continuous
3×f32 RGB; Hair type double-sourced; 112 face-preset literals PLAUSIBLE) +
V8 basis (CHAR_G gender/clothing/41-slot census; CHAR_H 19-range native codec,
StringStream storage, SERVER_FED=0; W25 hair re-pair) otherwise unchanged.

Scope: static research on the CD-era ArkScript corpus (Scripts.ark members `1883.obj.dec`
= CharDefUI creation script, `635.obj.dec` = CharDef class, `4093.obj.dec` = welcome
screen; all SHA-pinned) and the **PE2_unpacked_out.exe** binary (SHA256
`56178993692A7409C896398089E482EDDF96177666BACB91A8CC1A638D9A0650`, canon-verified).
Static only — the client was NOT executed. There is **no playable character creator
here**; this is a documented schema + VM decode.

## Recovered vs. not — one line

RECOVERED (V10, phase 2 + CHAR_G/CHAR_H/CHAR_I/CHAR_J/W26): 40-field creation schema, 21 controls (labels ×2
languages, layout), validation texts, class/flow evidence, PDAT structure, ArkScript VM
opcode idioms, the widget class + hostcmd registry (CHAR_D/E), control *value model*
(numeric f32 → CharDef property slots; CHAR_F), **21/21 range semantics** — `Size`
COMPUTED_RUNTIME 0..299, `Hair type` 17 × 2 gender arrays, and the **remaining 19 ranges
= NATIVE_CODEC_RECOVERED (CHAR_H)**: uniform value codec f32 ∈ [0.0, 1.0039] step 1/254
(byte 0x7F = exactly 1.0) / int ∈ [0,254], stored in a serialized **StringStream**
(NUL-terminated char buffer; **slot semantics CORRECTED by CHAR_J, superseding the
CHAR_H "validated index only" wording**: slot = RANDOM-ACCESS byte index into the
CharDef parameter stream — the handler sets the copy cursor to the index and writes
buffer[cursor] with grow-if-needed; slot K = byte K of the stream; no per-slot
min/max/step tables — proven absent by full decompilation); **gender byte-proven** (slot 45 via
227469: 1 = MALE classtypes {926,4195}, 2 = FEMALE {1014,4063}; GetSex error strings),
hair mesh↔texture gender pairing corrected (CHAR_G), the 2003 template-registry analog
(VREG: 22 ArkScript registry scripts; avatar model candidates 205), clothing-class
registries 5509/5504/453/2284/1464 (= Shirt / leg-calf / leg / hand / head equipment
classes, NOT skin/eye palettes), and the slider→target chain
(227469/227472 thin dispatchers → StringStream → consumers 6052 Hair / 6051 HairBase /
6060 / 670 via the 635::240520 assembly + factory 0x7FFFEC7E). **CHAR_I (V9):**
Skin/Eye/Hair **COLOR palettes do not exist as discrete tables** — all 4 consumer
scripts fully decoded (residue 0, inline regions included, bounded negative: zero
RGBA/HSV/texture-id color tables); colors are consumed as **continuous 3×f32 RGB**
at *this[0,4,8] via virtual CALL_IND 279761 (owner 345); the palette domain IS the
CHAR_H native codec (f32 [0, 1.0039], step 1/254) — palette=NONE; head texture
selection is hair-TYPE-indexed (slot 26), NOT color-indexed. `Hair type` now
**DOUBLE-sourced**: 6052 gender tables 17×2 (V7) + 6051 head tables slot-26
(mesh 20 / tex 21, gender-independent; 21/21 textures ∈ Textures.ark ✓). 6060
SetPreset = 4 cases × 28 f32 = **112 face-preset literals** (PLAUSIBLE join to
`Face type`; not proven). 6051 = **HairBase** (name via CHAR_G ctor evidence):
GetMeshId('head')→slot 26→MESH_TABLE, GetTextureId analog, MorphDefaults 28 f32,
new slot-39 driver (0/2 gender-chain selector + blend factor — `Hair volume`
PLAUSIBLE candidate). **CHAR_J (V10)**: GCE hostcall marshalling contract
byte-proven (SP stored at [GCE+0x14] before dispatch; __thiscall 1 arg = id;
results GCE+4/+8/+0x10; caller-side ADD_SP_imm arg pop; arg layout
stream-RAW/slot-DEREF/value-DEREF, push order value/slot/stream-last); apply-SETs
= sequential stream indices 0..N via a counter cell (CHAR_I pattern RESOLVED);
control→slot pairing: Hair type→26 RECOVERED 1:1, Sex→45 RECOVERED, gender
factor→39 RECOVERED anchor, 18 positional PLAUSIBLE, Mouth UNKNOWN; CALL-227469
census corrected 44→47 sites. **W26 (V10)**: the 6051 head "MESH_TABLE" namespace
is **RESOLVED — Textures.ark `.tga` 20/20** (128×128 uncompressed truecolor,
imgtype 2; bimodal separation proven both ways: hair 34/34 Models.ark vs head
20/20 Textures.ark; the "2008 Models.bnt ids" hypothesis REFUTED via the
era-labelled EU_9_2_2 reference check; semantics of the mesh-labelled accessor
returning texture ids OPEN — appearance-map hypothesis, STRONGLY_SUPPORTED by
the 187058–187065 id-adjacency block). NOT RECOVERED (honest UNKNOWN): per-control exact 1:1
widget→slot pairing (18 of 21 positional PLAUSIBLE with 3 competing hypotheses;
Mouth UNKNOWN), head-attachment positions,
name-validation side, the wire format, slider→bone runtime proof, which of the
21 controls the 112 preset matrices / slot-39 driver serve (unproven), and
**the engine-side semantics of the 20 head TGA ids** (appearance-map role —
W27 decoded/rendered all 20 with a HYPOTHESIS badge; W28 chain-CONFIRMED 1/20:
19706 = `head_0_BASE` of 11663.nif male, 32279 female out-of-set family repro;
18/20 remain runtime-slot hypothesis — see the head-appearance section). **A
"full character creator" is therefore at best partially reconstructed; a read-only
preview** exists (`terrain/character_preview.html`, W18 + W25 re-pair) — see below.

## Schema (40 fields, `CHARACTER_CREATION_SCHEMA.json`)

- 26 PDAT property records × 7 dwords, **byte-proven**: dw0=name_id, dw1=owner(1883),
  dw2=hash32, dw3=init-region **word count** (dw3×4 == distance to next region — 26/26
  exact; corrected tiling end 892→896), dw4=CODE offset, dw5=multiplicity (1×13, 2×5,
  8×2 strings), dw6=flags.
- The 26 init regions tile CODE[0..896] exactly. PDAT is *not* a "control configuration
  candidate" (CHAR_A hypothesis overturned by the boundary proof); no palette values
  exist anywhere in 1883 raw bytes.

## 21 controls — status per contract taxonomy

| Aspect | Status | Evidence |
|---|---|---|
| **Labels** | RECOVERED — 21 EN + 21 FR at exact CODE offsets (Skin color, Hair color, Eye color, Hair type, Face type, Hair volume, Constitution, Length and Proportions, Chest size, Eyes1, Eyes2, Ear position, Ear angle/size, Cheeks, Cheekbones, Chin, Forehead, Size, Nose1, Nose2, Mouth) | CHAR_A label stream probes |
| **Layout** | RECOVERED — body panel: vertical positions 84,142,200,269,328,386,498,606,715 (~58 px steps); face panel: x/y ∈ {65,238,258,338}×{7,161}; 4 sub-panels (B+0x00×9, B+0x0C×4, B+0x10×5, B+0x14×3) | CHAR_A operands, CONFIRMED by CHAR_B re-decode |
| **Ranges** | **21/21 bounded (V8).** `Size` = **0..299** COMPUTED_RUNTIME (creator 211689: hostcall 299 → 2·count−1 → hostcall 15846 RANDOM → interp 211669). `Hair type` = **17 items × 2 gender arrays = 34** (6052 Hair::GetMeshId/GetTexture gender dispatch byte-proven; item 0: MALE mesh 32498 + tex 216257, FEMALE mesh 32509 + tex 216302; gender-corrected join in `PALETTE_MAPS_HAIR_V7.csv`). Remaining **19 = NATIVE_CODEC_RECOVERED (CHAR_H)**: no per-control bounds exist anywhere — the native 22745x chain is a **uniform value codec**: f32 decode `(b+128)·(1/254)` with (min=0,max=1.0) → **f32 ∈ [0.0, 1.0039], step 1/254, byte 0x7F = exactly 1.0**; int decode → **[0,254]** (bytes 0/1 collide at 128); f32 set gate [min−1e−6, max+1e−6] else SILENT DROP (1.0→0x7D→0.9921 asymmetry documented); typed set gate byte ≤ 0xFE. Per-slot min/max/step tables **PROVEN ABSENT** (full decompilation of all handlers + validators + codec fns). **V9 (CHAR_I) consumer-side:** `Hair type` now **DOUBLE-sourced** — 6052 gender tables 17×2 (V7) + **6051 HairBase head tables** (slot 26: mesh table 20 entries / tex table 21 entries, gender-independent, join byte-proven via STOREI slot=26 + SHL_C_2 lookup; 21/21 tex ids ∈ Textures.ark ✓, 0/20 mesh ids in 2003 Models.ark — **namespace RESOLVED by W26: the 20 ids are Textures.ark `.tga` 20/20** (128×128 uncompressed truecolor; appearance-map candidates, semantics OPEN)). `Face type` = **PARTIAL**: 6060 SetPreset = 4 cases × 28 f32 = **112 literals** (byte-proven LOADF+CLRPARAM census) — face-preset candidates, join to the `Face type` control **PLAUSIBLE** (not proven). `Hair volume` = **PARTIAL** (6051 slot-39 driver → 0/2 gender-chain selector + blend factor — PLAUSIBLE candidate). Remaining per-control semantic domains of the 19 codec ranges: still consumer-side open for the non-head consumers (635 xref scripts 1796/3560/4653/5132/6123/401 undecoded). | CHAR_F §4–6; VREG §3; CHAR_G §3–5; CHAR_H §5; CHAR_I §2–4; W26 §3–5 |
| **Widget class (host side)** | RECOVERED — the 0xB0 widget is a **text-list/edit widget** (vtable 0x005E5028; +0x12C append item, +0x130 clear; maxItems/maxChars = −1 unlimited, guard-only). **No setMin/setMax/setStep/setDefault/setPalette method exists** (all four vtable slots enumerated). Siblings: editbox 0x11C, list-with-images 0xC4. | CHAR_E §2–3 |
| **Value feed** | **SCRIPT_FED — SERVER_FED REJECTED (0 producers).** Whole-image indirect-call census (688,210 instructions, 91 sites): zero producers in a network/protocol parser; CHAR_H native-side confirms: server-fed ranges **none found (0)** — the chain is a local byte buffer the scripts assemble. Hostcmd registry two-layer (bind-time vtable[2] resolver, run-time vtable[3] dispatcher). **Slider→target chain (CHAR_G §3, closed):** slider event → 1883 handler → **227472(slot)** thin dispatcher (unrolled BEQ switch on slot ∈ {26, 34, 30, 45, 0}; duplicate-34 case = dead code, byte-proven) → engine hostcalls **227470/227471** (+ convert ops **0x7FFFEC7A** f32→int / **0x7FFFEC7B** int→f32 — NOTATION CORRECTED from 0x7FFE001A/B, which were decimal→hex slips) → avatar update via 635::240520 assembly → factory 0x7FFFEC7E → registry scripts → mesh/texture id. Consumers (all 4 now decoded, CHAR_I): **6052 (Hair), 6051 (HairBase), 6060 (head/face-preset consumer, name UNKNOWN — no literal), 670 (head consumer, name UNKNOWN)**. **No min/max/step/default/palette value tables exist in the binary.** | CHAR_E §4; CHAR_D §2–4; CHAR_G §3; CHAR_H §3–5 |
| **Palettes** | Hair palette → mesh+texture ids **gender-corrected** (CHAR_G: MALE(1) tex@CODE+800, FEMALE(2) tex@CODE+636 — CHAR_F had the two texture tables crossed; `PALETTE_MAPS_HAIR_V7.csv`, 34 rows) and **V9 DOUBLE-sourced** with the 6051 head tables (`PALETTE_MAPS_V9.csv`, 135 rows: hair V7 34 + 6051 head tables 41 + sections 42 + 6060/670 consts 8 + clothing 10). **Skin/eye/hair COLOR palettes: palette=NONE (V9, CHAR_I)** — all 4 ctor-635::240520 consumer scripts (6051/6052/6060/670) fully decoded, residue 0, inline regions included: **zero RGBA/HSV/texture-id color tables** (bounded negative, positive coverage of the complete CODE of all consumers). Colors are consumed as **continuous 3×f32 RGB at *this[0,4,8]** in the 6051+6060 applies → virtual CALL_IND 279761 (owner 345); the palette domain = the CHAR_H native codec itself (f32 [0, 1.0039], step 1/254, byte 0x7F = 1.0). **Head texture selection is hair-TYPE-indexed** (slot-26 table), NOT color-indexed; 6060/670 carry single texture constants 21333/274039 (both ∈ Textures.ark ✓). Native-side negative (CHAR_H §6) stands: zero RGBA/HSV/color tables in the fully-decompiled 22745x search space. White 0xFFFFFFFF remains the only binary constant (creation). | CHAR_F §4,§6; CHAR_G §4–5; CHAR_H §6; CHAR_I §3 |
| **Gender** | **BYTE-PROVEN (CHAR_G §4).** No gender selector in 1883 (byte-proven negative); gender is CharDef **slot 45**, read via 227469 → 0x7FFFEC7B: **1 = MALE (classtypes {926,4195}), 2 = FEMALE ({1014,4063})** (GetSex error strings @635 CODE+79676/79952 + membership hostcall 4471). Drives 6052 Hair::GetMeshId/GetTexture and all clothing-registry gender dispatches. | CHAR_G §4 |
| **Clothing registries** | **RESOLVED as equipment classes (CHAR_G §5)** — the 5 palette candidates are 1-fn avatar EQUIPMENT classes with GetMeshId gender dispatch + section strings + variant tables (shared "No Gender??" boilerplate = clone evidence): **5509 = Shirt** (torso/upperarm/forearm; name string-proven), **5504 = leg/calf class** (tables {13562,271585}/{33578,271610}), **453 = leg class** (m 11663 / f 28614), **2284 = hand class (Glovesplate)**, **1464 = head class (Facemaskplate)** (m 797 / f 33281 both). NOT skin/eye palettes. | CHAR_G §5 |
| **Slot census** | **41 distinct slot ids** byte-proven from CALL-227469 sites in 1883 init (CORRECTED by CHAR_J: 47 sites, recounting CHAR_G's 44): 1..6, 8..21, 22..30, 32, 33, 36..38, 39..44 (no 7, 31, 34, 35 in UI init; 34 = engine-internal, 45 = sex). 26 and 30 among the 227472-convertible set. | CHAR_G §6 (site count CORRECTED by CHAR_J §5) |
| **Control→slot pairing (V10, CHAR_J)** | **PARTIAL — 2 RECOVERED 1:1 + 1 RECOVERED anchor + 18 PLAUSIBLE (positional) + 1 UNKNOWN.** RECOVERED: `Hair type`→slot 26 (consumer 6051/6052 + SET site fn208716 @CODE+1536, byte-proven), `Sex`→45, gender factor→39 (pair-slave of cell B+0x04); hair-section morphs→27/28/29. The 17-cell structure table (fn 303635 init) and the slider-change callback (fn 208728) carry **byte-identical per-cell slot pairs** (double-proven read+write paths); fn 303638 binds 3 color cells to pairs (32,33)/(28,29)/(36,37) via combine fn 227917. PLAUSIBLE: the 17-cell and 3-cell tables bind to controls only via creation order — 3 competing positional hypotheses documented (all-widgets-order vs sliders-only vs colors-in-303638; see `CONTROL_SLOT_MAP.csv`); widget handle values are binder/engine-time data (not in the static image). `Mouth` = UNKNOWN (outside all decoded tables; fn 208720 SET-sites not decoded). | CHAR_J §5 + CONTROL_SLOT_MAP.csv |
| **Defaults** | Size = COMPUTED_RUNTIME (`FUN_00461710() % (max−min+1) + min`, min/max = script literals); other 20 ENGINE_DEPENDENT | CHAR_D §4; CHAR_F §6 |

## ArkScript VM opcodes — CONFIRMED (handler VAs + ASM, R2 project reused)

| Opcode | Mnemonic | Handler VA | Semantics (1883 context) |
|---|---|---|---|
| 0xFF91 | LEA_A_inline | 0x00457B79 | A := cursor+4; with FEEB = inline string block base |
| 0xFEEB | JMP_rel | 0x00456D2C | cursor += disp; disp>8 skips inline data |
| 0xFFA0 | PUSHEA_B_off | 0x00457CE5 | push (B+off) = panel/sub-object selector |
| 0xFEDE | STOREI_SPoff | 0x00456C32 | [SP+off] := imm32 (frame-local store) |
| 0xFEEE | CALL_abs | 0x00456D4B | binder-patched call (slot raw 0x0) — CONFIRMED |
| 0xFF8F | HOSTCALL | 0x00458182 | GCE.vtable[3] engine call — CONFIRMED |
| support | STRCPY 0xFEC8, LEA_B_SPoff 0xFEBD, PUSHEA_SPoff 0xFF09, STOREF 0xFEE7 | | CONFIRMED |

This **overturns** the CHAR_A hypotheses ("FF91/FEEB = string push", "FFA0/FEDE = UI
params"). The 21-control creation idiom (builder @CODE+46048..48984) decodes as:
`FEDE` layout stores → `FF91+FEEB 'label'` → `STRCPY` → `FFA0` panel push → `FF09`
label push → `FF09` params push → `FEEE CALL` creator (20/21 → name_id 210421,
'Size' → 211689, hash-double-confirmed).

## PDAT correction (vs. CHAR_A)

- PDAT dw3 is a **word count** (region tiling proof), not a palette size; tiling end
  corrected to CODE[0..896]. CHAR_A's monotonic layout reading and 4-panel census were
  CONFIRMED, not corrected.

## Phase-2 corrections (recorded, not silently fixed)

- **"0xB0" is the widget OBJECT SIZE**, not a class id (CHAR_E).
- **EXTN dw2 is NOT a string-type hash**: the claim "string-typed props carry dw2
  hash `D56B88DA`" does **not reproduce** — 0/1403 EXTN records carry it; dw2 is the
  owner script id (1883/635/1/…). EXTN itself is proven to be a **fixup table**
  (every FF8F/FEEE operand slot resolves; 0 unresolved calls in the whole CODE).
- **Inline strings are cp1252 single-byte NUL-terminated**, 8-byte-aligned —
  NOT UTF-16 (fixture: `'Coleur de peau'` É=0xE9).

## Also recovered (class/flow evidence)

- Welcome → CharDefUI flow proven (`4093` references CharDefUI 4784).
- Name validation texts (≥2 chars per field; forbidden words; uniqueness;
  immutability; accept prompt) — EN+FR. Whether the length check runs client- or
  server-side is UNKNOWN (no regex/limit operand in bytes).
- Preview actions (naked / clothed / armored), attachment slots
  (hand/hair/head/upperarm/forearm/torso/calf/leg/foot), full face-morph bone set
  (`Bip01_face_cd_*`, `Bip01_cd_{r,l}_calf_*`) in 635, clothing regions, GetSex
  Female/Male. **No gender selector in 1883** — byte-proven negative (gender is a
  CharDef attribute: **slot 45**, CHAR_G).
- Slider→bone dataflow partially recovered: event handlers read an f32 PARAM and call
  `CharDef::227472` with slot constants 31/32/33 (pure delegation, no clamps).

## 2003 template registry (VREG — closes old gap #4)

The 2003 analog of the later template registry is **ArkScript class code in
Scripts.ark** — *not* a VFS container (Volumes.ark = bounded negative:
831/831 members scanned, 0 hits for all 9 needles; the 2003 client has 0
occurrences of `VFS`/`ArkVFS`/`.vfs` — the later `20040.vfs` mechanism does not
exist in this corpus):

- **22 registry scripts** with `*::GetMeshId/GetTexture` id arrays: Hair 6052
  (34 mesh + 34 texture ids, gender dispatch byte-proven per CHAR_G), Boots 5500,
  Shoes 4288, Shirt 453, shirt/torso variants
  (3577/3580/3581/3703/5493/5504/5509/6153/6174–6181),
  Facemaskplate 1464, Glovesplate 2284 — the 5 former "palette candidates"
  classified by CHAR_G as clothing equipment classes (see table above). Ids are
  membership-qualified (∈ Models.ark / ∈ Textures.ark, clean bimodal split),
  not opcode-verified; ids outside both archives are **UNBOUND** (likely VM
  constants or server-side).
- **Avatar model candidates**: 205 Models.ark members carry the complete
  `Bip01_face_cd_*` morph bone signature (primary family 207222–208861;
  208860/208861 likely a gender pair — **which is which gender: UNPROVEN**
  (CHAR_G proved the SLOT-45 gender semantics and the HAIR gender pairing, not
  the avatar-body mesh pair); naked vs clothed distinction inside a family
  UNPROVEN without server data).
- Models.ark NIF version census: 4.1.0.12 = 1815, 4.0.0.2 = 440,
  4.0.0.0 = 237, **10.1.0.0 = 0** (first explicit ISO-corpus check).

## Read-only preview (W18 + W25 re-pair — NOT a playable creator)

`terrain/character_preview.html` renders the real 2003 avatar **208861.nif**
(549 blocks, IR_READY) plus hair meshes **32498 (MALE) / 32509 (FEMALE)** with
era TGA textures applied. Honest bounds, shown on the page itself: the hair
meshes render **separately, NOT attached** (no head-attachment position
recovered); hair gender pairing is now **BYTE-PROVEN** (CHAR_G GetSex 1=MALE /
2=FEMALE + 6052 gender tables; W25 re-paired the previously crossed textures:
32498+216257 MALE, 32509+216302 FEMALE — CHAR_F/W18 had them swapped);
which of 208860/208861 is which gender remains UNPROVEN; the avatar's
NiKeyframe*/NiArk* blocks and the hair NiSkinInstance/NiSkinData are OPAQUE
(censused with offset+span, not decoded — W09 adapter backlog); the 21 control
labels are displayed as strings only with their CHAR_F statuses — **no
fictional sliders** (DOM-gated: 0 input/range elements).

## GCE hostcall marshalling contract (V10, CHAR_J — RECOVERED byte-proven)

- **ff8f HOSTCALL handler @0x00458182**: ECX = GCE; **[GCE+0x14] := VM SP
  BEFORE the dispatch**; PUSH resolved-id; CALL [vtable+0xC] as
  `__thiscall(ECX=GCE), 1 x86 arg = id`. Results read back from **GCE+4 (f32
  PARAM), GCE+8 (int C), GCE+0x10 (A)**; VM code cursor += 8.
- **Derived dispatcher 0x485260** zeroes GCE+4/+8/+0x10, binary-search +
  scaled jump tables over its OWN id set; per-case `CALL engine_fn; POP ESI;
  RET 0x4`. **NO VM-stack pop exists anywhere in the derived body**
  (2230-line listing, 0 undefined bytes) — arg pop is **CALLER-side**
  (script `ADD_SP_imm`, e.g. 635 CODE+67812 ADD_SP 8 after the 2-arg 227470).
  Hub 0x486F89 tail-calls the BASE dispatcher (0x441DF0), identical
  interface. Negative control: no case constants 227457–227471
  (0x37881..0x3788F) in the derived body — all CharDef hostcalls run in the
  BASE dispatcher; only 0x7FFFEC77 and 0x7FFFEC7C/7D (FSIN/FCOS) are derived.
- **Arg layout (VM stack at [GCE+0x14]; last push = +0)**, per BASE case
  bodies: 227457 raw GET / 227470 conv GET / 227458 raw SET →
  arg0 = stream RAW, arg1 = slot DEREF, arg2 (SETs) = value DEREF (f32
  FLD-DEREF, gate [0,1]±1e−6 / typed byte ≤ 0xFE). **Push order**: script
  pushes in REVERSE (SETs: value first, stream last) — the CHAR_G/CHAR_I
  inherited ABI is now **byte-proven, not pattern-inherited**.
- **Slot semantics CORRECTION (supersedes the CHAR_H §4 "slot = validated
  index only" wording)**: the slot is a **random-access byte index** into the
  serialized CharDef parameter stream. FUN_0044F8B0 copies the stream and
  sets the copy cursor := index; FUN_00463D40 writes the encoded byte at
  `buffer[cursor]` (grow by cursor−length+1 if needed); GET analogously
  (FUN_00463BE0 reads buffer[cursor], cursor++). Consequence: CharDef
  "slot K" = byte offset K of the stream; the 635-ctor 46-f32 default table =
  the 46-parameter default layout.
- **CHAR_I "repeated slot-local pattern" RESOLVED**: the 6051/6060/670
  apply-SETs write **sequential stream indices 0..N** through a frame counter
  cell (CLR at entry, INC after every hostcall) — one FRAME CELL holding a
  different index per write; part-local parameter block; those SETs carry no
  control→slot information. CHAR_I honest-gap #2 CLOSED.

## Head-mesh namespace (V10, W26 — RESOLVED)

The 20 ids of 6051's head "MESH_TABLE" (27697, 19704–08, 4336, 5691,
5989–91, 5997, 6081/82, 187058–61, 216925/26) are **texture-namespace
resource ids physically present in Textures.ark 2003 as 128×128 uncompressed
truecolor TGA (20/20, imgtype 2)**; the 21 section STOREI "mesh" constants are
likewise 21/21 `.tga`. **Bimodal separation runs both ways**: 6052 hair34 =
34/34 Models.ark `.nif` / 0/34 Textures.ark (positive control PASS);
6051 head20 = 0/20 Models.ark / 20/20 Textures.ark — the membership test
cleanly discriminates namespaces. The "2008 Models.bnt ids" hypothesis
(CHAR_I gap #2) is **REFUTED**: era-labelled REFERENCE_OTHER_BUILD
(EU_9_2_2) Models.bnt index → 0/20 and Textures.bnt index → 0/20 (exact
greedy-digit regex; 6 substring false positives caught and corrected).
The 187058–187065 id-adjacency block (mesh-labelled + tex-labelled in one
contiguous allocation series) makes plain texture consumption
STRONGLY_SUPPORTED. **Semantics — W27/W28 UPDATE (see next section): decoded
and chain-resolved: 1/20 chain-confirmed (19706 → `head_0_BASE` of the male
base-body mesh 11663.nif).**

## Head-appearance semantics (W27 decode + W28 chain verdict)

**W27 (decode/render):** all 20 head TGA extracted STRICT and decoded
(128×128, imageType 2, 24bpp BGR, **no alpha**; TGA 2.0 footer; constant
49,196 B; per-file payload SHA256 pinned in `W27_TGA_STATS.json`). Shown in
the character preview as **"HEAD APPEARANCE CANDIDATES"** (6 canvas + 20/20
table + toggle) with a **HYPOTHESIS** badge — the W26 semantic gap was closed
to HYPOTHESIS level only; all W27 opinions were based on bytes/statistics,
not visual inspection. Hypothesis set (all era-labelled, W27 status):
H-APPEARANCE-COLOR-MAPS (STRONGLY_SUPPORTED among hypotheses: 5,269–8,818
unique colors = 32–54% of pixels + zero alpha → color maps, not masks),
H-SKIN-TONE-FAMILY (PLAUSIBLE: uniform warm R>G>B, R−B +18…+25),
H-SHARED-LAYOUT (PLAUSIBLE: darker bottom third in 20/20 + darker edges in
19/20), H-PALETTE-SERIES (PLAUSIBLE), H-MASK/H-HAIR-COLOR (WEAK/REJECTED-leaning).

**W28 (chain verdict — STRUCTURAL, SHA-pinned 2003 corpus):** the head:0
NiTriShape of **11663.nif** (male base-body candidate) → properties →
NiTexturingProperty (blk 11, single active slot 0 = BASE, uv_set 0) ←
ArkTexture **`head_0_BASE`** → texture id **19706** — a member of the 20.
**H-APPEARANCE-COLOR-MAPS is CONFIRMED for 19706** (full ref chain + unique
corpus hit: pattern-scan of Models.ark payloads finds 19706 exactly in
11663.nif and nowhere else). The second gender, **28614.nif**, bakes
`head_0_BASE` = **32279 — OUTSIDE the set of 20** but reproducing the same
family signature (warm R>G>B, R−B≈+25, dark bottom band) →
**H-SKIN-TONE-FAMILY STRONGLY_SUPPORTED**; the 20 are a SUBSET of a larger
head-appearance map family. **18/20 have no baked references in Models.ark**
— consistent with runtime slot-26 selection (W26 §2): NIFs bake one default
head_0_BASE, the rest are chosen per-avatar at runtime (27697 is consumed by
4 other NIFs — candidate other avatars/NPCs, undecoded).

Supporting W28 evidence: NiArkTextureExtraData **empirically decoded**
(9-byte entries, id @ bytes 5–8; full spans consumed 721/721 B in 11663 —
18 entries — and 756/756 B in 28614 — 19 entries; all 37 texture ids ∈
Textures.ark; built-in negative control: body ids correctly NOT in head20,
0 false hits; independent pattern-scan decode cross-check). UV side: head:0
footprint = full-tile bbox with ~48.4% dispersed occupancy (tile-wide
islands, not a compact centered blob) — the texture-side layout convention
RETAINS, the UV-side "centered object" fragment is DOWNGRADED
(H-SHARED-LAYOUT SPLIT).

**Hypothesis table after W28:** H-APPEARANCE-COLOR-MAPS **CONFIRMED** (for
19706; family inference); H-SKIN-TONE-FAMILY **STRONGLY_SUPPORTED**;
H-SHARED-LAYOUT **SPLIT** (texture-side retain / UV-side downgrade);
H-PALETTE-SERIES **PLAUSIBLE** (retained); H-MASK/H-HAIR-COLOR
**REJECTED-leaning (strengthened)** — the head_0_BASE role of 19706
contradicts hair-color/mask semantics for at least 1/20.

**Preview badge:** the HYPOTHESIS badge may remain for the 18 unconfirmed
candidates, but the preview section now carries **"1/20 chain-confirmed
(19706→head_0_BASE male)"**. NOT_TESTED (W28 honest bounds): head:1–3
sub-shape semantics (ids 21333/21337/274039 — likely eyes/teeth, textures
not decoded); the 4 NIFs consuming 27697; the engine-side slot-26 runtime
selection itself (Ghidra follow-up, ranked gap).

## Ranked gaps (updated after CHAR_J/W26 — V10)

1. ~~Consumer-script decode (6060/670/6051)~~ **DONE for the 4 ctor-635::240520
   consumers** (CHAR_I, residue 0). Remaining: 635 xref scripts
   (1796/3560/4653/5132/6123/401/…) if further per-slot consumers needed —
   lower priority now that the head/hair chain is closed.
2. ~~6051 head MESH namespace~~ **RESOLVED by W26**: the 20 ids are
   Textures.ark `.tga` 20/20 (appearance-map candidates; semantics OPEN —
   decode/render of the 20 TGA is the W27 follow-up).
3. ~~GCE hostcall arg marshalling~~ **DONE by CHAR_J**: marshalling contract
   byte-proven (see the V10 section above); apply-SET slot targets resolved
   as sequential indices 0..N; the 227471 (value,slot) push roles proven
   (arg1=slot DEREF, arg2=value DEREF).
4. **Preset/driver→control joins**: which of the 21 controls the 4×28=112
   preset matrices (6060) / slot-39 driver (6051) / MorphDefaults (28 f32)
   serve — PLAUSIBLE candidates (`Face type`, `Hair volume`) flagged, not
   proven; needs runtime confirmation.
5. **NiKeyframe/NiSkin adapters** (W09 backlog extension, real fixtures from
   W18): NiKeyframeController/Data (avatar ×70), NiSkinInstance/Data (hair) →
   unlock skinning + head-attachment proof.
6. **Per-control widget→slot exact 1:1 pairing**: NARROWED by CHAR_J from
   "41 slots flat" to a 17-cell double-proven slot-pair table + 2–3 competing
   positional hypotheses (see the Control→slot pairing row); RECOVERED 1:1:
   Hair type→26, Sex→45 (+anchor 39); 18 positional PLAUSIBLE; Mouth UNKNOWN
   (fn 208720 SET-sites not decoded). **Runtime closure would decide it in
   one run — but the "frida one-shot" (CHAR_J next-step) is FORBIDDEN in
   this campaign (CONTRACT §14) and remains a FUTURE task requiring
   separate authorization** (governance note, backlog).
7. **Runtime namespace capture**: the 26 PDAT name_ids (208688–227997) resolve
   only at runtime (frida hook on the client's symbol-lookup when 1883 loads)
   → true property names. (Same governance constraint as #6: runtime
   instrumentation is out of campaign scope.)
8. **Name validation** (UNKNOWN side): not found in the resolved op set —
   ranked candidates: server-side, runtime-tree id space, un-enumerated
   dispatcher jump-table cases.
9. **Wire format**: capture the client→server submit after "Accept Look".
10. **11663/28614 re-classification** (CHAR_I flag): same mesh pair in 453
    (CHAR_G "leg") and the head consumers 6060/670 → candidate base-body mesh
    pair; flagged for MASTER, NOT overturned here.
11. **Head-appearance-map semantics** (W26 follow-up): ~~decode/render the 20
    head TGA~~ **DONE by W27** (all 20 decoded + shown in the preview with a
    HYPOTHESIS badge); ~~chain-confirm the appearance-map role~~ **DONE by W28
    for 1/20** (19706 = `head_0_BASE` of 11663.nif male; 32279 female
    out-of-set family repro; 18/20 remain runtime-slot hypothesis). Remaining:
    locate the engine consumer of 6051's slot-26 head ids (Ghidra — closes
    the runtime-selection chain and the 18/20) and optionally decode the 4
    NIFs consuming 27697 (284429/284437/28680/797 — other avatars/NPC?).
