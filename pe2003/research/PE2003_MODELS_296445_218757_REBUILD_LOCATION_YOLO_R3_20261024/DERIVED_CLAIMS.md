# DERIVED_CLAIMS — public claim list with statuses

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.
Evidence taxonomy: CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED.
A rejected-as-worded claim may retain an accepted finding disposition.

## Source/build identity

| Claim | Status |
|---|---|
| pe42_en.exe CAB extraction PASS; 711 files, all hashed | CONFIRMED |
| Client = Project Entropia 4.02.0000 Commercial Open Trial, PE.exe 53A6F341…, UPX-packed, 2003-01-30 | CONFIRMED |
| PE.exe == PE_CD.exe | CONFIRMED (IDENTICAL_BYTES) |
| upx -d(PE.exe) == PE2_unpacked_out.exe (56178993…); VA base of the 2003 static RE | CONFIRMED (causal R1a experiment; supersedes the older UNVERIFIED_RELATION record) |
| ARK corpus byte-identical across 3 physical copies | CONFIRMED (HASH_EQUAL_COPY ×3) |
| manifest_2003.csv is a MIXED_CORPUS_LOCATOR (row 218757 = 9.3.5 payload), not an era proof | CONFIRMED (CS06) |
| ISO NOV2003 container DEGRADED; member ZIP PASS; separation statement holds | CONFIRMED |
| PCG demo inner content vs PE42 corpus | UNVERIFIED (NSIS_EXTRACT_BLOCKED block #40) |

## Models

| Claim | Status |
|---|---|
| 296445.nif: Models.ark index 1720, 108 876 B, SHA 656795D8…, NIF 4.1.0.12, 155 blocks | CONFIRMED |
| 296445 SAME_MODEL vs 9.3.5 = IDENTICAL_BYTES (3-way; payload identity only) | CONFIRMED |
| 218757.nif: index 1189, 56 535 B, SHA C13D0873…, NIF 4.1.0.12, 62 blocks | CONFIRMED |
| 218757 SAME_MODEL vs 9.3.5 = VARIANT_SAME_ID (no era/build/instance transfer) | CONFIRMED |
| 296445 role = B_Eu_Slum_Building_b047_01 + flare rig | CO-NAMED (CONFIRMED as naming evidence); building-class = PLAUSIBLE only |
| 218757 role = B_Outpost_me01 plain exterior mesh | CO-NAMED; outpost-exterior = PLAUSIBLE only |
| NIF inspector censuses 155/155 and 62/62, footer cross-checks | CONFIRMED |
| Fitted NiTextureEffect/NiUVController/NiUVData field grammars | UNVERIFIED (single-instance fits, labeled) |

## Definitions / loader / join

| Claim | Status |
|---|---|
| Loader chain: mount → manager 0x5E7974 (slots nif/bvi/tga/dds, sprintf %d+ext) → reader FUN_00464F30 → NIF 0x522010→0x5B7170 "NetI" → wrapper 0x5EBC1C | CONFIRMED |
| Definitions 4508.obj (296445+296446) and 4057.obj (218757+218758) carry the ID constants in the attach-resource-pair macro (E18) | CONFIRMED (byte-verified) |
| type-id→definition lookup FUN_00441230 | CONFIRMED (33-callsite census) |
| definition→open static consumer EXISTS on build 56178993 | REJECTED (0 direct callers ×3; 0 qualified virtual sites of 5776 indirect CALLs / 576 444 instructions; SFO/0x415xxx candidate REJECTED-PRECISELY) — CONFIRMED-NEGATIVE; dynamic-only |
| Client-side 0x7700xxxx interpreter | UNVERIFIED/NEGATIVE with denominators (0x7fffec7x runtime opcodes ARE consumed — partial revision); server-side suspected |
| BVI pairing (296445/296446, 218757/218758) code-side proof | UNVERIFIED (co-occurrence + 9.3.5 oracle only) |

## Spawn / transform / placement

| Claim | Status |
|---|---|
| Spawn chain: frame 0x06 → FUN_005bc5a0 → FUN_00528a40 → FUN_004688d0 → avatar 0x118B (vtable 0x5E4628) → FUN_005030c0 → scene | CONFIRMED |
| Position = 3× f32 LE in BE envelope; ×100.0 (0x42C80000) storage multiplier at scene attach | CONFIRMED |
| Orientation = 3×3 row-major row-vector (v·M) at obj+0x2C; consumers FUN_004193f0 + FUN_00419090 | CONFIRMED (live source UNVERIFIED — W3-11) |
| Local 2003 corpus contains instance/placement data | REJECTED (negatives with denominators: install census; Volumes 831/831; Scripts 1936 decoded; Models 2492) |
| TRANSFORM_SOURCE = NETWORK_RUNTIME_ONLY; AUTHENTIC_INSTANCE_COUNT (offline) = 0 | CONFIRMED (as negative results) |
| PLACEMENT_VERDICT = MECHANISM_CONFIRMED_LOCATIONS_NOT_RECOVERABLE_FROM_LOCAL_2003_CORPUS | CONFIRMED |
| World-axis/meters calibration | UNANSWERABLE with local data (no anchor) |
| Camera-record class 0x5E49B8 vs avatar class 0x5E4628 confusion | CORRECTED (W2→W3; CLR-01) |

## Process claims (honesty ledger)

- Per-job decompile counts are LOWER_BOUNDs; untracked totals marked UNMEASURED.
- Native Task attempt accounting was internally inconsistent (13 census entries
  vs used=12 vs REPORT/BODY "11 of 96" vs ROLE_LEDGER 0) — QC finding F-01 (P2),
  resolved by master dispositions (MASTER-CLR-12); canonical statement = 12
  worker-job attempts + A1 assembly + QC.
- The stale METHOD_935_TO_2003_REPLAY status column was a documentation defect
  fixed by QC (F-02 → QC-CLR-11; 43 rows re-derived, 7 honestly UNVERIFIED).
- No positive "placement reconstructed" claim exists anywhere in the package
  (QC grep sweep, QW-05).
