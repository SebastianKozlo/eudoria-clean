# Case 296445 — B_Eu_Slum_Building_b047_01 (+ lens-flare rig)

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.
Full sanitized case: `research/PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024/REPORT.md`
(private source: `MODEL_296445_CASE.md` in the sealed run package).

## Status block

| Field | Value |
|---|---|
| SAME_MODEL_2003_vs_935 | **IDENTICAL_BYTES** (3-way: PE42-ARK member == manifest row == legacy extraction; all SHA256 `656795D8B3DDDF8F9192EE41C4710D592894860F6959B53B2C08036977E7B862`; 108 876 B / CRC CFAC1D3B / NIF 4.1.0.12 / 155 blocks). Payload identity only, NOT world-instance identity |
| Role | CO-NAMED `B_Eu_Slum_Building_b047_01` + lens-flare effect rig (7× NiArkBillboardNode, NiTextureEffect sphere-map, NiUVController U-scroll 0→5.0 / 3.3333 s LOOP); 30 shapes / 2415 vtx / 1030 tri; building-class PLAUSIBLE (naming only, CS07) |
| Definition | Scripts.ark `4508.obj` (decoded 3640 B, SHA256 `B6C96E9C…`); IDs 296445 (@~664) + 296446 (@~580) byte-verified in the attach-resource-pair macro (E18) |
| Paired volume | `296446.bvi` in Volumes.ark (index 555, 1008 B = 21×48 B, CRC 27EE4229); `296446.nif` NOT_FOUND in Models.ark (denominator 2492); pairing NOT PROVEN code-side (co-occurrence + 9.3.5 oracle) |
| Join verdict | type-id→definition CONFIRMED (FUN_00441230, def 4508, E18/W3-08); definition→model-open CONFIRMED-NEGATIVE static / OPEN dynamic (E20/R3-06); spawn-packet→instance CONFIRMED (W3-02) |
| TRANSFORM_SOURCE | NETWORK_RUNTIME_ONLY (local negatives with denominators: install census, Volumes 831/831, Scripts 1936 decoded, Models 2492) |
| AUTHENTIC_INSTANCE_COUNT (offline) | **0** |
| PLACEMENT_VERDICT | MECHANISM_CONFIRMED_LOCATIONS_NOT_RECOVERABLE_FROM_LOCAL_2003_CORPUS |

## Replay map (P01-P20 method rows, 2003 status after campaign + QC fix)

The 9.3.5→2003 replay matrix (private: `METHOD_935_TO_2003_REPLAY.csv`, 50 rows
P01-P25; 43 re-derived during QC, 7 honestly left UNVERIFIED) maps each
historical method question to its 2003-side status. Key rows for 296445:

- P01 member identity — ANSWERED (locate index 1720; 3-way IDENTICAL_BYTES).
- P02/P03/P06/P07/P09-P11/P13/P14/P15/P17/P20 — CONFIRMED-class (corpus,
  definitions, manager chain, decode, orientation math, network path).
- P04 pairing — CONFIRMED_DATA_LEVEL_PAIRING_NOT_CODE_PROVEN (BVI co-occurrence only).
- P05 open edge — PARTIAL (static-negative; dynamic-only next).
- P12 creator third component — CONFIRMED_NEGATIVE_CREATOR.
- P18 instance roster — PARTIAL_JOIN_MECHANISM_ONLY_ZERO_INSTANCES_OFFLINE.
- P19 offline rosters — NEGATIVE_CLOSED_OFFLINE_WITH_DENOMINATOR.
- P08/P16/P22/P25 — UNVERIFIED (live consumer / calibration anchor / fingerprint
  ceiling / open items).

## REPRODUCE (parameterized)

With your own PE42 corpus (NOT included in this repository):

```powershell
# 1) locate + extract + verify + reference-scan + structure (end-to-end)
python pe2003/tools/pe2003_case_pipeline.py 296445 `
  --ark-root <your install Data dir> `
  --listings-dir <dir with Models/Scripts/Textures/Volumes_ark_full_listing.csv> `
  --decoded-scripts-dir <dir with decoded Scripts blobs> `
  --f1-decoder pe2003/tools/ark_vfs_decoder_f1.py `
  --inspector pe2003/tools/pe2003_model_inspector.py `
  --extract-dir <out> --report-dir <out> --science-root <out>
# expected: overall=CONFIRMED, blocks=155, census match, footer cross-check CONFIRMED

# 2) negative control (member that must NOT be found)
python pe2003/tools/pe2003_case_pipeline.py 296446 ...
# expected: NOT_FOUND, denominator 2492

# 3) structure inspection alone
python pe2003/tools/pe2003_model_inspector.py <296445.nif> --json out.json
# expected: status=OK blocks=155 census_match=True
```

Verification pins: SHA256 `656795D8B3DDDF8F9192EE41C4710D592894860F6959B53B2C08036977E7B862`
(108 876 B), CRC32 CFAC1D3B, NIF 4.1.0.12, 155 blocks; block census per the
run REPORT (NiNode 19, NiArkBillboardNode 7, NiTriShape 30, …).

Run report: `../../research/PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024/REPORT.md`
