# Case 218757 — B_Outpost_me01 (plain outpost exterior mesh)

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.
Full sanitized case: `research/PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024/REPORT.md`
(private source: `MODEL_218757_CASE.md` in the sealed run package).

## Status block

| Field | Value |
|---|---|
| SAME_MODEL_2003_vs_935 | **VARIANT_SAME_ID** — 2003-ARK variant (56 535 B / CRC C40B12CA / SHA256 `C13D08736D7E778803E20A3105067448007F32D15290AF168F836CD99248AD98` / NIF 4.1.0.12 / 62 blocks) vs 9.3.5 variant (57 316 B / `3E8A22C2…` / NIF 10.1.0.0, verified at 2 disk locations). Same ID, DIFFERENT payloads/eras; NO build/instance/placement transfer (CS08). manifest_2003.csv row = the 9.3.5 payload → manifest is a MIXED_CORPUS_LOCATOR, not an era proof (CS06). The 2003-ARK file was MISSING as a standalone .nif before the campaign and was recreated by re-extraction, bit-exact with the prior pin |
| Role | CO-NAMED `B_Outpost_me01_Ext_sign/_main/_vent03/_bigdoors/_smaldoor` + occluders `dPVS_occ01..05`; plain textured mesh, 14 shapes / 1130 vtx / 526 tri; NO billboards / UV controller / texture effect; outpost-building-exterior PLAUSIBLE (naming only) |
| Definition | Scripts.ark `4057.obj` (decoded 2688 B, SHA256 `EA93FCA9…`); IDs 218757 (@456) + 218758 (@~372) byte-verified in the attach-resource-pair macro (E18); additional resource ids in 4057 CODE: 218588, 218760, 218762, 218768 |
| Paired volume | `218758.bvi` in Volumes.ark (864 B = 18×48 B, CRC 5DD32B83) — W1 discovery (absent in the initial F1 report; draft error corrected by self-check). `218757.bvi` does NOT exist. Pairing NOT PROVEN code-side |
| Join verdict | type-id→definition CONFIRMED (def 4057, E18/W3-08); definition→model-open CONFIRMED-NEGATIVE static / OPEN dynamic (identical COMMON negative as 296445; no cross-model promotion — per-model tracking); spawn-packet→instance CONFIRMED (W3-02) |
| TRANSFORM_SOURCE | NETWORK_RUNTIME_ONLY (same COMMON negatives with denominators) |
| AUTHENTIC_INSTANCE_COUNT (offline) | **0** |
| PLACEMENT_VERDICT | MECHANISM_CONFIRMED_LOCATIONS_NOT_RECOVERABLE_FROM_LOCAL_2003_CORPUS |

## Model-specific open items (absent for 296445)

- Cross-variant structural diff (4.1.0.12 vs 10.1.0.0 payloads): NOT EXECUTED
  (deferred). Whether the 10.1 payload is an up-conversion of the 4.1 payload:
  UNKNOWN.
- 9.3.5 template float 21.2574 (templates.vfs 4057 payload+0x10): semantics
  unknown; PRIOR_DESKTOP_MEASUREMENT with a MISSING primary history source —
  not re-executable; era transfer NOT claimed.
- 9.3.5 fingerprint relation (CS22): NO_MATCH_IN_SELECTED_INPUTS — negative
  within selected inputs only; ceiling NOT_ESTABLISHED.

## REPRODUCE (parameterized)

With your own PE42 corpus (NOT included in this repository):

```powershell
python pe2003/tools/pe2003_case_pipeline.py 218757 `
  --ark-root <your install Data dir> `
  --listings-dir <dir with the 4 *_ark_full_listing.csv> `
  --decoded-scripts-dir <dir with decoded Scripts blobs> `
  --f1-decoder pe2003/tools/ark_vfs_decoder_f1.py `
  --inspector pe2003/tools/pe2003_model_inspector.py `
  --extract-dir <out> --report-dir <out> --science-root <out>
# expected: overall=CONFIRMED, blocks=62, census match, footer cross-check CONFIRMED
```

Verification pins: SHA256 `C13D08736D7E778803E20A3105067448007F32D15290AF168F836CD99248AD98`
(56 535 B), CRC32 C40B12CA, NIF 4.1.0.12, 62 blocks (61 FIELDS_CONFIRMED + 1
NiArkAnimationExtraData PARTIAL_FIELDS_OPAQUE_TAIL).

Run report: `../../research/PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024/REPORT.md`


## R2 update — PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025

The independent Desktop postaudit of R1 (REQUIRE_CORRECTIONS, SP-A01..09) was executed by the
static closing wave R2; full sanitized projection:
`../research/PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025/REPORT.md`.
Corrections supersede the table rows above where stated; the R1 file itself is byte-untouched
(see `../research/PE2003_MODEL_INSTANCE_PLACEMENT_STATIC_R1_20261024/STATIC_R1_EXTERNAL_POSTAUDIT_NOTICE.md`).

- **TRANSFORM_SOURCE corrected to SOURCE_UNKNOWN** (was NETWORK_RUNTIME_ONLY): neither local
  nor network exclusivity is proven (postaudit SP-A01). CONFIRMED mechanism: the network
  transform channel reaches FUN_005030c0 (translation x100.0f + 3x3 rotation matrix on
  vt-0x5E2A3C-class objects); NIF local transforms are ALL identity (31/31 NiNode blocks
  across both model files) — no local placement data in the NIF files; +0x6C/+0x70 are
  NIF_FILE_LOCAL on the owner class 0x78 (vt 0x5EBBEC).
- **Instance join, family level: ESTABLISHED (CONFIRMED mechanism)** — loader create-fn
  0x4077F0 and FUN_005030c0 both target the vt 0x5E2A3C class. **Object-instance join:
  STILL_AMBIGUOUS (OPEN)** — decisive edge = registry+0x3C root identity (BLK-R2-01); no
  historical world placement of 218757 is claimed. Per-model tracking: the identical COMMON
  negative does not close the 218757-specific join.
- **"missing 768.obj/382.obj" context corrected to FILE_CLASS_PRESENT** — namespace error;
  raw members PROVEN byte-identical in Scripts.ark. The 4057 attach chain is fully decoded
  (same COMMON plumbing as 4508; EXTN bijection 8/8, zero unmatched, 0 unknown opcodes over
  1419 items). Model ids 218757/218758 appear only as DYN getters with cross-dispatch
  consumers (MISSING_EDGE; bounded negative: 13 target ids, 0 foreign raw hits).
- Standing: WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; SOURCE_UNKNOWN;
  PE2003_LOCAL_SOURCE_EXHAUSTED=NO; CANONICAL_GATE_EFFECT=NONE;
  ADVISORY_PENDING_EXTERNAL_POSTAUDIT.
