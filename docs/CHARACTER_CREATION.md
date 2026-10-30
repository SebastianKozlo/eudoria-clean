# CHARACTER_CREATION — recovered 2003-era avatar-creation knowledge

Scope: static research on the CD-era ArkScript corpus (Scripts.ark members `1883.obj.dec`
= CharDefUI creation script, `635.obj.dec` = CharDef class, `4093.obj.dec` = welcome
screen; all SHA-pinned) and the **PE2_unpacked_out.exe** binary (SHA256
`56178993692A7409C896398089E482EDDF96177666BACB91A8CC1A638D9A0650`, canon-verified).
Static only — the client was NOT executed. There is **no playable character creator
here**; this is a documented schema + VM decode.

## Recovered vs. not — one line

RECOVERED: 40-field creation schema, 21 controls (labels ×2 languages, layout),
validation texts, class/flow evidence, PDAT structure, the ArkScript VM opcode
idioms. NOT RECOVERED: per-control ranges/palettes/defaults (engine-side), the wire
format, slider→bone runtime proof, asset template binding. **A "full character
creator" is therefore at best partially reconstructed; the values pipeline is
VM/server-dependent.**

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
| **Ranges / palettes / defaults** | **ENGINE_DEPENDENT — open.** No opcode produces min/max/step/default/palette in the script bytes: proven by (a) a clean full-CODE sweep (4,901 op items + 71 inline strings, ZERO residue), (b) creator-function internals (layout/font/white-color/callback only), (c) `CharDef::227472` contains no clamps. Values are built engine-side behind FF8F HOSTCALLs whose command ids are binder-patched slots (raw 0x0 statically). f32 0.1f/1.0f remain CONDITIONAL candidates. | CHAR_B §4 |

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

## Also recovered (class/flow evidence)

- Welcome → CharDefUI flow proven (`4093` references CharDefUI 4784).
- Name validation texts (≥2 chars per field; forbidden words; uniqueness;
  immutability; accept prompt) — EN+FR. Whether the length check runs client- or
  server-side is UNKNOWN (no regex/limit operand in bytes).
- Preview actions (naked / clothed / armored), attachment slots
  (hand/hair/head/upperarm/forearm/torso/calf/leg/foot), full face-morph bone set
  (`Bip01_face_cd_*`, `Bip01_cd_{r,l}_calf_*`) in 635, clothing regions, GetSex
  Female/Male. **No gender selector in 1883** — byte-proven negative (gender is a CharDef
  attribute).
- Slider→bone dataflow partially recovered: event handlers read an f32 PARAM and call
  `CharDef::227472` with slot constants 31/32/33 (pure delegation, no clamps).

## Ranked gaps

1. **HOSTAPI catalog** (`PE_VM_HOSTAPI_R1`): decompile the GCE vtable[3] dispatcher →
   host-command catalog → widget range/palette/default tables engine-side. This closes
   the ENGINE_DEPENDENT block.
2. **Runtime namespace capture**: the 26 PDAT name_ids (208688–227997) resolve only at
   runtime (frida hook on the client's symbol-lookup when 1883 loads) → true property
   names.
3. **Wire format**: capture the client→server submit after "Accept Look".
4. **Template registry**: find the 2003-era mapping of garment/hair/face classes to
   numeric Models.ark ids (analog of the later 20040.vfs).
