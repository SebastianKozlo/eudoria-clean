# PE_NIF_WITNESS_MATRIX_MAP_R1 — FINAL REPORT (RUN-C)

**RUN_ID:** PE_NIF_WITNESS_MATRIX_MAP_R1_20260905_123428
**RUN_CLASS:** RUN-C — WITNESS-MATRIX MAP for the NIF corpus (offline analysis; ZERO renders; MAP ONLY)
**SCOPE:** EU935-M2 contribution — NIF documentation loop. Wiki HOLD semantics released for THIS map only. **NO M2 ADVANCEMENT.**

## 1. P0 ANSWER (one paragraph)

The witness set for future falsification testing of the R61 frozen parser and the documented
grammars is **5 known-good primary witnesses** (KG-1..KG-5: 424276, 426763, 500078, 146709, 592572),
**3 mildly-wrong single-byte recipes** (MILD-1..MILD-3, each with machine-verified byte/offset/before/after
values and a code-path-cited failure-mode prediction), **3 severely-scrambled recipes**
(SCRAMBLE-1..3, each destroying a named structural anchor with a MUST_FAIL_LOUDLY prediction), and a
**character/clothing witness layer** (500078 Bip01 skeleton, 146709/137260 class-01 mob rigs,
592572 torso_xtra, 574703/574845 avatar body-part sets) identified via prior run data because the
manifests carry no type column. Every witness SHA256 was **computed personally from physical bytes**
(9.3.5 payloads sliced from Models.bnt by BNT2 index offset; 2003-era files hashed from the
M1B3 extraction dir); 7/8 witnesses are byte-identical across both corpus eras (dual-provenance
hashes recorded); 592572 is 9.3.5-only (era-drift datum). NO corrupted variant was built or parsed —
recipes + predictions only.

## 2. Baseline + corpus integrity (machine-verified this run)

| Item | Result |
|---|---|
| R61 frozen baseline (01_source, 10 files) | **10/10 SHA256 MATCH** (re-hashed personally vs SHA256_SOURCE.json; source used AS-IS, READ-ONLY) |
| Models.bnt (9.3.5, pcg_install\Data\Models) | SHA256 `c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0`, 395,412,868 B, BNT2 index_start=395262727, declared=parsed=5,596 entries |
| 2003 corpus extraction dir | 5,426 .nif files (PE_M1B3_REAL_PE_NIF_COMPATIBILITY_LAB_V1_20260819_010815\02_extraction\nif) |
| Frozen-parser parse closure (context) | 5,596/5,596 (9.3.5) + 5,426/5,426 (2003) — the R61 baseline this map tests against |

## 3. Known-good witness set (5 primary; ALL parse-confirmed PASS this run, READ-ONLY)

All five were parsed this run with the frozen R61 parser (raw payloads only): **5/5 PASS,
blocks == header num_blocks in every case** (35/35, 17/17, 121/121, 79/79, 71/71).

| ID | File | Era | Variant | SHA256 (computed personally; both eras identical unless noted) | Roles | Why PASS (grammar citation) |
|---|---|---|---|---|---|---|
| KG-1 | 424276.nif (28,794 B) | v4.1.0.12 | TEXT_CRLF | `533429333c9947c660c2a25e3bd74ea99c5013f244beed86d351612549e8beda` | TEXT-records witness; v4-era rep; viewport-bearing | v4 header grammar (pe_header.py v4 layout); NiArkAnimation v4 selector → TEXT_CRLF self-terminating grammar: CRLF → ASCII node_count (=2) → 2×NodeDataStart records → trailer 6B (byte[5]=0x00) (pe_niark_animation.py L95-155, L162-264; docs/nif/08 L293) |
| KG-2 | 426763.nif (10,351 B) | v4.1.0.12 | SHORT28 | `bb44cdf6610cee72ab4b79abfca633a01206caded647443729ec9df103225982` | v4 FIXED-family rep; 2nd v4 variant family | selector u3==0xFFFFFFFF && u2>=4 && peek[7]==0x00 → fixed 8B all-zero ext (pe_niark_animation.py L117-121; docs L291 "8x00, verified 35/35 ITER-31"); ext re-verified this run: `0000000000000000` |
| KG-3 | 500078.nif (57,642 B) | v10.1.0.0 | G3B | `d26ad81161122f3ef1f3444ca495723c43a0e8892722efb78dbce7a387779df2` | G3B-bearing; Bip01 character rig; 392 B event-block record | v10 header + per-block preamble u32=0 (pe_block_reader.py L269-282); u2=2 family → u3=0 binary → G3B boundary search (pe_niark_animation.py L782-810); ext = ONE record [u32 size=388][u8 02][u8 flag=01][...][13 strings] → 392 B total, byte-exact grammar (docs L457-464, L497) |
| KG-4 | 146709.nif (41,473 B) | v10.1.0.0 | G3D | `135d20f27657bd7720ab56d0eed00e78ede25fb8e88d461351be75a852417194` | G3D-bearing; class-01 mob rig (18 bones); MILD-1 carrier | G3D formula ext_size = byte[1]×5 = 24×5 = 120 B (pe_niark_animation.py L817-849); node-reference list 5-byte records (docs L316, 348/348); formula boundary validated against next-block preamble (verified: u32@766==0); NiSkinInstance/Data/Partition (C19/20/21) |
| KG-5 | 592572.nif (159,622 B) | v10.1.0.0 | G3D | `2ea8b23f5e45cc613debc799224fdda800336fe5bd4087c3f14ed5eeac3bf209` **(9.3.5-ONLY)** | Morph-bearing (NiVertexMorphExtraData N=1294); clothing (torso_xtra) | G3D formula (u3 byte1=49 → 245 B ext); NiVertexMorphExtraData = C24 boundary-search parser, PARTIALLY_KNOWN/EXACT; wiki-decoded record model re-verified from raw bytes this run: 0x01 const + u32 N=**1294** + u16 tag=64 (docs/nif/08 L146: "592572.nif 1294 == 1294 CONFIRMED") |

**Era mix:** v4-era ×2 (KG-1, KG-2) + v10-era ×3 (KG-3..KG-5). **Corpus era mix:** KG-1..KG-4
byte-identical across 2003 + 9.3.5 (both hashes computed personally); KG-5 9.3.5-only.

**Prior-run cross-references used for selection (as mandated):** 592572/574703/574845 morph files
(docs 08 L146, 09-semantics span census, G3D class runs); 424276/426763 viewport files
(NiArkViewportInfoExtraData-bearing, both manifests); 146709/137260 class-01 G3D files
(PE_NIF_G3D_CLASS_ROLE_R37 REPORT L75-77: 7/7 class-01 list); 500078 392B event-block file
(docs 08 L497 + PE_KEYFRAME_FORMAT_R1 keyframe_inventory.csv).

## 4. Mildly-wrong recipes (3; single byte; exact values machine-verified from raw payload bytes)

| ID | Source | Anchor | Exact corruption (payload offset, before → after) | Prediction (R61 code path) |
|---|---|---|---|---|
| MILD-1 | 146709.nif | NiArkAnimationExtraData **u3 byte1** = G3D formula count N (offset **639**, u3@638 = 0x00001801) | `0x18` (N=24) → `0x19` (N=25); formula ext 120→125 B; corrupted formula end @771 reads u32=1,107,296,256 ≠ 0 (verified) | **PASS (self-healed, silent variant flip)**: is_valid_boundary fails at ext_start+125 → G3E else-branch → `_find_v10_block_boundary(raw, 646)` returns **766 == true boundary** (precondition verified by running the frozen boundary search on the raw bytes) → ark_variant G3D→G3E, boundary_method formula→boundary_search (pe_niark_animation.py L817-862, L516-589) |
| MILD-2 | 424276.nif | TEXT_CRLF **node_count last ASCII digit** (offset **306**, digits line = "2" @306-307) | `0x32` ('2') → `0x33` ('3'); declared node count 2→3 | **PASS (self-healed, silent variant flip)**: extra node iteration raises ArkAnimationError `TEXT: NodeDataStart not found for node 2` (marker find is first in every loop iteration) → `_parse_v4_variant` catches → G9_RTTI fallback scan → first known-RTTI candidate @537 **== true next-block boundary** (NiArkTextureExtraData, verified) → ark_variant TEXT_CRLF→G9_RTTI, PARTIALLY_KNOWN (pe_niark_animation.py L219-222, L146-155, L389-424) |
| MILD-3 | 500078.nif | NiArkAnimationExtraData **u2 LSB** = v10 family selector (offset **625**, u2@625 = 0x00000002) | `0x02` → `0x03`; u2 = 0x00000002 → 0x00000003 | **FAIL_CLOSED (must reject)**: u2u ≠ 0xFFFFFFFF and ≠ 2 → ArkAnimationError "v10 NiArkAnimationExtraData u2=0x00000003 has no P0-verified parser. FAIL CLOSED." → dispatch_block generic except → FailClosedError "variant parse error: ..." → FAIL_CLOSED, fail_block_type=NiArkAnimationExtraData, boundary UNSAFE (pe_niark_animation.py L647-653; pe_block_reader.py L356-362; pe_nif_reader.py L88-106). **If this ever parses PASS, the variant-closed failsafe contract is broken.** |

MILD-1/MILD-2 document the parser's **tolerance boundary** (documented self-heal paths: G3E
boundary-search fallback; TEXT_CRLF→G9 catch-all); MILD-3 documents the **rejection boundary**
(variant-closed contract). RECIPE-ALTERNATE recorded (not executed): 426763 peek[7] @305
`0x00`→`0x01` flips SHORT28→FIXED_B_61 (+33 B over-consume → predicted FAIL via v4 inline-RTTI desync).

## 5. Severely-scrambled recipes (3; each MUST_FAIL_LOUDLY; anchors named)

| ID | Source (copy, never original) | Anchor destroyed | Corruption | Prediction |
|---|---|---|---|---|
| SCRAMBLE-1 | byte-copy of Models.bnt (395,412,868 B) | **BNT2 footer magic** (outermost container anchor) | last 4 bytes `42 4E 54 32` ('BNT2') → `58 58 58 58` ('XXXX') @ file_size-4 | **MUST_FAIL_LOUDLY**: ValueError `not a BNT2 archive: footer magic=b'XXXX'` in load_bnt2 BEFORE any NIF parse; all 5,596 payloads unreachable; container SHA256 also changes (audit_pcg935_nif_r1.py L83-84 container gate) |
| SCRAMBLE-2 | payload copy 424276.nif | **NIF version selector u32** (routes ALL downstream grammar mode flags) | @41: `0c 00 01 04` (0x0401000C) → `ff ff ff ff` | **MUST_FAIL_LOUDLY**: parse_version(0xFFFFFFFF): major=255 → type_table=True while is_v10=False → header reads NumBlockTypes u16 = 6 from v4 block data → first sized_string i32 = **1,766,719,488** (computed from real bytes) → pe_stream absurd-length guard → FAIL_ERROR `header parse error: absurd string length 1766719488 at pos=51` (pe_version.py L57-58; pe_header.py L75-80; pe_stream.py L121-127; pe_nif_reader.py L55-60) |
| SCRAMBLE-3 | payload copy 500078.nif | **v10 4-byte block record separator** (preamble u32=0 framing EVERY block) | @481 (data_start_offset): `00 00 00 00` → `ef be ad de` (0xDEADBEEF) | **MUST_FAIL_LOUDLY**: dispatch_block reads record_preamble_u32=3,735,928,559 ≠ 0 → FailClosedError `non-zero block_preamble_u32=3735928559` → FAIL_CLOSED, fail_block_index=0, boundary UNSAFE (pe_version.py L76; pe_block_reader.py L269-282) |

## 6. Character / clothing witnesses (identified via prior run data; manifest has NO type column)

| File | Class | Identification (source) |
|---|---|---|
| 500078.nif | character (PRIMARY, =KG-3) | ANIMATION_SKELETON, full **Bip01 rig** (Pelvis/Spine*/Neck*/Head/Ponytail*/Clavicle/UpperArm/Forearm…), 38 NiKeyframeControllers, DUNGMASTER anim set (PE_KEYFRAME_FORMAT_R1 keyframe_inventory.csv) |
| 146709.nif | character (PRIMARY, =KG-4) | **class-01** G3D file (7/7 list: 137260, 146709, 205850, 353140, 459889, 501549, 546608) — core-bone flag on small **non-biped mob rig**, skinned_meshes=1, max_bones=18 (PE_NIF_G3D_CLASS_ROLE_R37 REPORT.md L75-86) |
| 137260.nif | character (ALTERNATE) | class-01 G3D mob rig, max_bones=49; re-hashed this run (identical both eras) |
| 592572.nif | clothing (PRIMARY, =KG-5) | avatar body-part/clothing mesh: **torso_xtra** BASE+BUMP; morph-bearing N=1294 |
| 574703.nif / 574845.nif | clothing (ALTERNATES) | avatar body-part sets: calf/foot/forearm/glasses/hand/head_up/leg/torso/upperarm BASE+BUMP (9/8 skinned morph parts, max_bones=24); both re-hashed this run (identical both eras) |

No NOT_IDENTIFIABLE entry was required — but the manifest alone would NOT have sufficed (no type
column); prior-run cross-referencing was the mandated and used route.

## 7. Falsification value summary

1. **Loudness contract**: SCRAMBLE-1/2/3 + MILD-3 give 4 deterministic MUST-FAIL predictions with
   exact simulated messages — if any future parser version parses them (or fails differently than
   predicted), the failsafe contract or the grammar has regressed.
2. **Tolerance contract**: MILD-1/MILD-2 give 2 self-heal predictions with variant flips — they pin
   the documented G3E/G9 fallback paths; strict-grammar evolution flips them to FAIL (detectable).
3. **Identity contract**: all witness SHA256s pinned from physical bytes; the 1294 morph pairing
   (KG-5) and the 392 B event record (KG-3) pin the documented semantic layer.
4. The **falsification EXECUTION run** (building + parsing the 6 recipe variants in a sandbox copy)
   is the proposed NEXT run — GATED on explicit authorization (MAP ONLY this run; nothing built).

## 8. Standing-rule compliance

- **No payloads**: outputs carry identity metadata only (hashes, offsets, single anchor bytes); zero
  payload bytes written to the run dir or the publish tree.
- **MAP ONLY**: frozen parser run READ-ONLY on raw known-good files only (explicitly permitted);
  zero corrupted variants built/parsed; zero renders; zero game code.
- **READ-ONLY sources**: Models.bnt, 2003 extraction dir, R61 frozen source (10/10 verified first),
  manifests, prior-run census files — nothing modified outside the run dir.
- **No M2 advancement**: EU935-M2 contribution only; wiki HOLD semantics released for this map only.

## 9. Artifacts

- `05_ANALYSIS\WITNESS_MATRIX.json` — THE MAP (primary deliverable)
- `01_RAW\r61_baseline_verification.json`, `corpus_identity.json`, `witness_hashes.json`,
  `parse_confirmations.json`, `anchor_forensics.json` — machine evidence
- `00_CONTROL\witness_matrix_driver.py` — the driver (SHA256 in SHA256_DRIVER.txt)
- `STAGE_ACCEPTANCE_GATES.csv` — gates (a)-(f) + compliance rows
- `artifact_index.csv` — REAL SHA-256 of every artifact
