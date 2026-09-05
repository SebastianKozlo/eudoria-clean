# HANDOFF — PE_NIF_WITNESS_MATRIX_MAP_R1 (RUN-C)

```
AUDIT_OUTPUT_ROOT      = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_WITNESS_MATRIX_MAP_R1_20260905_123428\
FINAL_REPORT_PATH      = 06_REPORT\00_FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS = 05_ANALYSIS\WITNESS_MATRIX.json
                         01_RAW\witness_hashes.json
                         01_RAW\parse_confirmations.json
                         01_RAW\anchor_forensics.json
                         01_RAW\r61_baseline_verification.json
                         01_RAW\corpus_identity.json
RUN_STATUS             = COMPLETE (MAP delivered; 5 known-good + 3 mild recipes + 3 scramble recipes + character/clothing layer; R61 10/10 verified; 8/8 raw witnesses parse PASS; all recipe preconditions machine-verified from raw bytes)
HARD_STOP_REASON       = NONE (MAP ONLY contract held: zero corrupted variants built/parsed; no M2 advancement; nothing authorizes the falsification EXECUTION run without explicit GO)
```

## Witness counts per class
- known-good primary: **5** (KG-1 424276 v4/TEXT_CRLF, KG-2 426763 v4/SHORT28, KG-3 500078 v10/G3B+Bip01, KG-4 146709 v10/G3D class-01, KG-5 592572 v10/G3D morph, 9.3.5-only)
- mildly-wrong recipes: **3** (MILD-1 G3D→G3E self-heal PASS predicted; MILD-2 TEXT_CRLF→G9_RTTI self-heal PASS predicted; MILD-3 u2 0x02→0x03 MUST-REJECT FAIL_CLOSED predicted)
- severely-scrambled recipes: **3** (SCRAMBLE-1 BNT2 magic; SCRAMBLE-2 version u32→0xFFFFFFFF; SCRAMBLE-3 first v10 preamble→0xDEADBEEF — all MUST_FAIL_LOUDLY)
- character witnesses: 2 primary (500078 Bip01, 146709 class-01) + 1 alternate (137260, re-hashed)
- clothing witnesses: 1 primary (592572 torso_xtra) + 2 alternates (574703/574845, re-hashed)

## Machine-verified identity anchors
- R61 frozen baseline: **10/10 SHA256 MATCH** (re-hashed personally before any use; READ-ONLY)
- Models.bnt (9.3.5): `c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0` (395,412,868 B; BNT2 index_start=395262727; 5,596 entries)
- 7/8 witnesses byte-identical across 2003 + 9.3.5 corpora (BOTH hashes computed personally);
  592572.nif is 9.3.5-only (era-drift datum)
- Key semantic pins re-verified from raw bytes: 592572 morph u32 N=1294 (docs pairing CONFIRMED);
  500078 G3B record size=388 → 392 B total, marker 0x02, flag 0x01 (13 event strings)

## Falsification predictions (see WITNESS_MATRIX.json for full citations)
- MILD-1: byte@639 0x18→0x19 → PASS via G3E recovery (boundary search on raw returns 766 == true boundary)
- MILD-2: byte@306 0x32→0x33 → PASS via G9_RTTI recovery (first known-RTTI candidate @537 == true boundary)
- MILD-3: byte@625 0x02→0x03 → FAIL_CLOSED "u2=0x00000003 has no P0-verified parser. FAIL CLOSED."
- SCRAMBLE-1: BNT2 footer → ValueError before any parse
- SCRAMBLE-2: version u32@41 → FAIL_ERROR "header parse error: absurd string length 1766719488 at pos=51" (simulated from real bytes)
- SCRAMBLE-3: preamble@481 → FAIL_CLOSED "non-zero block_preamble_u32=3735928559" at block 0

## Next step (GATED)
The falsification **EXECUTION** run: build the 6 recipe variants in a sandbox copy (never the
originals), parse with the R61 frozen parser, compare against the 6 recorded predictions.
**Requires explicit authorization** (this run's MAP ONLY contract forbade building/parsing corrupted
variants). See `00_CONTROL\NEXT_PROMPT.md`.

## MILESTONE_PROGRESS
- M1: PARTIAL — P0-1 x87 CW experiment DESIGN READY (awaiting review+GO); witness matrix + scrambled
  falsification MAP = THIS RUN (delivered); next queue: georef/P-DATUM → P-CELLSTREAM/P-CLIMATE
- M2: NOT_ADVANCED (EU935-M2 contribution only; wiki HOLD semantics released for THIS map only)
- Documentation loop: RUN-C contribution complete; zero M2-advancement claims
```
