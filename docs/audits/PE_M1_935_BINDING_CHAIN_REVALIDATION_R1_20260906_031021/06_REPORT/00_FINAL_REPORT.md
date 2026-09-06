# PE_M1_935_BINDING_CHAIN_REVALIDATION_R1 — FINAL REPORT (era PCG_9_3_5)

**RUN_ID**: PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021
**PARENT_RUN**: PE-MASTER loop 0132d23c-2f0f-42f2-bb07-fb74f637488b (KROK 1 of 3)
**MILESTONE**: EU935-M1 (bounded EU935-M2-contribution run; era-primary PCG_9_3_5; NO milestone crossing)
**RUN_CLASS**: MATERIAL (declared by PE-MASTER)
**Corpus**: `D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt` (SHA256 `c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0`, 395,412,868 B, 5,596 NIF payloads, uncompressed)
**Container 2**: `D:\Eudoria_Reconstruction\pcg_install\Data\Textures\Textures.bnt` (FULL SHA256 measured fresh this run: `61acd13b140e130647eee24c1e2669d3734990b76cf74897ddd3ba0f4ea61393`, 973,942,771 B, 8,381 entries, names `<id>.dat`)
**Frozen parser**: R61 (`PE_R61_FROZEN_BASELINE_20260828\01_source`, 10/10 SHA pins verified in-driver BEFORE any parse, READ-ONLY, never modified; usage `PENifReader().parse_bytes(payload, source_name=...)`)
**Driver**: `00_CONTROL\binding_chain_revalidation_r1.py`, SHA256 `8f20229025e31a449e9401ecb73249ad5406cd24d108babbc6952de266d253b4` (hash-after-last-edit rule, verified in-driver)

---

## 1. P0 ANSWER

**YES.** The mesh → NiArkTextureExtraData → bnt2_id → Textures.bnt binding chain resolves on the PCG 9.3.5 corpus at the SAME closure level as the canon 2003 chain:

| Metric | Era-2003 canon (M3-4 R2 + M3-4.5 V2) | **This run, era PCG_9_3_5** |
|---|---|---|
| ArkTexture entries | 23,488 (v4 4,901 + v10 18,587) | **24,508** (v4 4,871 + v10 19,637) — exact ITER-32 reconciliation |
| Resolved | 23,455 | **24,474** |
| **Resolution rate** | 99.8595% | **99.8613%** |
| Dangling | 33 | **34** |
| Dangling classes | 18 SuperSpray particle slots (3 ids × 6) + 15 unshipped | **18 SuperSpray particle slots (SAME 3 ids × 6, SAME 3 files: 425247/425261/425271) + 15 unshipped individual slots (all SAME ids as 2003) + 1 NEW 9.3.5 missing id** |
| Unique missing ids | 14 | **15** = the 2003 fourteen (all still missing) + `592148` |

The 2003 dangling set is a strict subset of the 9.3.5 dangling set: `only_in_2003 = []`, `only_in_935 = [592148]` (one entry: `592146.nif`, `Mesh01_0_BASE`, slot BASE). The mechanism (trailing-9B `anim_flag u8 + frame_index u32 LE + bnt2_id u32 LE`; canon "bytes[5:8] u32 LE = BNT2 texture ID") closes identically across eras — 9.3.5 adds one unshipped texture id and keeps every 2003 missing id missing.

## 2. Binding edges (M3-4.5 V2 method, recomputed era-9.3.5)

| Edge class | Era-2003 canon | **This run, era PCG_9_3_5** | Definition (explicit semantics) |
|---|---|---|---|
| Static (mesh → texturing-property slot → ArkTexture) | 20,427 | **21,390** (bnt2 resolved 21,374 / dangling 16) | `(nif, NiTriShape.block, prop_ref, ark.block, ark.idx)` where prop_ref ∈ NiTriShape.properties[] → NiTexturingProperty and ark entry.ref == prop_ref |
| Controller (NiFlipController) | 148 (from 125 NiFlipController) | **118 DIRECT** (canon-V2 definition: NiTexturingProperty.controller → NiFlipController) / **125 chain-inclusive** | DIRECT = (nif, NiTexturingProperty.block, NiFlipController.block) via fields['controller']. Chain-inclusive adds 7 next_controller-chained controllers (126 NiFlipController blocks total; 1 not reachable from any property chain). See 05_ANALYSIS/CONTROLLER_CHAIN_COUNTS.json |
| Effect (NiTextureEffect) | 1,749 (1,649 attached + 100 orphan; 1,646 blocks) | **1,798 = 1,772 attached + 26 orphan** (1,694 NiTextureEffect blocks) | (nif, NiNode.block, NiTextureEffect.block) via NiNode.effects[]; orphan NiTextureEffect (no parent NiNode) = 1 orphan edge each |
| Static edge self-check (two independent traversal paths) | builder/validator Jaccard 1.0 | **Jaccard = 1.000000** (21,390 = 21,390, intersection 21,390, union 21,390) | builder geometry-centric vs validator entry-centric |
| ANIM entries ref → NiFlipController | (1,149 animated entries, M3-4 R2) | **1,145** | informational join |
| NIF status | BOUND 3,562 / NO_GEOMETRY 1,789 / PARTIAL 55 / NO_TEX 20 (sum 5,426) | BOUND 3,699 / NO_GEOMETRY 1,818 / PARTIAL 58 / NO_TEX 21 (sum **5,596** ✓) | M3-4.5 V2 STATUS-01 semantics |

Controller count note (honest): the 2003 V2 controller-edge count 148 came from a traversal whose exact code is not extant; the 9.3.5 corpus has MORE NiFlipController blocks (126 vs 125) but FEWER direct property attachments (118 vs 148→125-blocks). The 8 non-direct controllers are chains (property.controller → NiFlipController#1 → next_controller → NiFlipController#2, same target property; e.g. 527569.nif blocks 20→21→22, num_sources 10→11). Both counts are reported under explicit semantics rather than forcing the 2003 number.

## 3. Census reconciliation vs ITER-32 (G3) — exact

- Total entries **24,508 == 24,508** (v10 19,637 ✓ / v4 4,871 ✓)
- Blocks: v10 4,838/4,838 ✓, v4 758/758 ✓; per-version 4,838×10.1.0.0 + 757×4.1.0.12 + 1×4.0.0.2 = 5,596 ✓
- Per-slot join vs R32 TEXTURE_SLOTS.json: **40/40 slots exact** (BASE 14,307 / GLOSS 2,791 / DARK 1,816 / ENVIRONMENT 1,694 / GLOW 1,524 / BUMP 970 / DETAIL 199 / DECAL0 50 / ANIM0–31 1,157)
- Convention exceptions: **0**; slot-exception census empty
- Validation layer: v10 raw re-decode **4,838/4,838 ok** (packed field2 formula + exact consumption + parser-vs-raw entry agreement), v4 raw decode **758/758 ok** (name recovery + exact consumption), zero raw-decode failures

## 4. BNT2 index validation (G2) — byte-exact, anomaly count 0

Both indexes parsed by an independent parser (footer u32 index_start @fs-8, `BNT2` magic @fs-4, name+`\n`+size+offset+8B stride):
- Models.bnt: 5,596 entries; adjacency `offset[i+1] == offset[i]+size[i]` for ALL — 0 breaks; exact index consumption (cursor == region end); first_offset=0; data region closes exactly at index_start.
- Textures.bnt: 8,381 entries; 0 adjacency breaks; exact consumption; 8,381 `<id>.dat` names, 0 non-conforming names.

## 5. Negative controls (G5) — collapse confirmed

| Control | Method | Result | Verdict |
|---|---|---|---|
| NC1 (contract control) | 10,000 uniform u32 draws vs the 8,381-id set | **0 hits = 0.0000%** | PASS — resolution collapses to ~0; lookup is not fuzzy |
| NC2 (density probe) | 10,000 uniform draws in observed id range [4584, 592856] | 156 hits = 1.56% vs expected namespace density 1.42% | consistent — in-range random ids hit at ~density, far below 99.86% |
| NC3 (permutation) | per-entry permutation of the real ids (seeded) | 99.8613% (== real) | set-membership is permutation-invariant — documented honestly as a pairing-vs-existence probe; NOT the collapse control (NC1/NC4 are) |
| NC4 (canon M3-4 R2 controls) | +1 shift (bytes 6:10) / −1 shift (bytes 4:8) / big-endian decode of bytes[5:9] | **0.0000% / 0.0000% / 0.0000%** (24,508 evaluated; 3,767 +1-shift windows skipped at block boundary — recorded) | PASS — the exact canonical byte window is required |

## 6. Honest NOT_CHECKED list

1. **The era-2003 chain was NOT re-run** — 23,488/23,455/33 and 20,427/148/1,749 are the audited canon reference (M3-4 R2, M3-4.5 V2, FOUNDATION_REBASE 25_M3_4_5_DENOMINATORS.csv), embedded read-only in the driver for comparison.
2. **Textures.bnt PAYLOAD contents were NOT opened/decoded** — only the tail index region (names `<id>.dat`) was parsed for resolution; the full file was hashed (integrity) but no texture bytes were decoded.
3. **The exact 2003 V2 controller-edge traversal code is not extant** — both 9.3.5 controller counts (118 direct / 125 chain-inclusive) are reported under explicit definitions instead of forcing comparability with 148.
4. **`592148`'s payload is unretrievable** — the id is absent from the 9.3.5 Textures.bnt index (unshipped texture; consistent with the id-adjacent-to-model-id pattern of the other 14 unshipped ids).
5. NiArkShaderExtraData, NiSourceTexture, VFS files and all other block families — out of scope (this run is the ArkTexture binding chain only).
6. The 26 orphan NiTextureEffect blocks (no parent NiNode) — counted as orphan edges per the canon V2 semantics; their scene-graph meaning not investigated further.

## 7. Taxonomy

- **CONFIRMED (era PCG_9_3_5):** binding chain closure 24,474/24,508 = 99.8613% (exact set membership); census 24,508 with 40/40 slot join vs ITER-32; both BNT2 indexes byte-exact (0 anomalies); static edges 21,390 with Jaccard 1.0 by two independent traversals; effect edges 1,798 = 1,772 + 26 from 1,694 blocks; direct controller edges 118 from 126 NiFlipController (7 chains + 1 unreachable); 15 unique missing ids = 14 canon + 592148; parse closure 5,596/5,596; v10/v4 raw re-decode 4,838+758 exact consumption.
- **STRONGLY_SUPPORTED:** the 9.3.5 unshipped-dangling classes mirror the 2003 classes (all 14 2003 ids still missing incl. the 18 SuperSpray slots in the same 3 files) — cross-era mechanism identity.
- **PLAUSIBLE:** 592148 = a 9.3.5-era unshipped texture (id adjacent to model id 592146, same pattern as 354708→354727, 418307→418308, 423167→420953); chained double flip controllers = per-slot animation sequences (BASE + another slot).
- **UNVERIFIED:** semantics of the 8 chained-controller targets beyond the structural link; effect-orphan runtime meaning; NC2's 156 in-range hits are namespace density (by design), not partial resolution.

## 8. Discipline (G6)

- Originals re-hashed after the run: Models.bnt == start pin, Textures.bnt == start full hash (**originals_untouched=True**).
- Zero payloads in the repo: only derived CSV/JSON/MD metadata (24,508-row id table, 34-row dangling list, 21,390/118/1,798 edge lists, negative-control results, gates, reports).
- Commit is path-limited to this run dir only; see HANDOFF.md for COMMIT_SHA / PUSH_STATUS.

## 9. Artifacts (REAL SHA-256 in artifact_index.csv)

`01_RAW/`: ARKTEXTURE_ID_TABLE.csv (24,508 rows), DANGLING_LIST.csv (34), DANGLING_CLASSIFICATION.json, STATIC_EDGES.csv (21,390), CONTROLLER_EDGES.csv (118), EFFECT_EDGES.csv (1,798), EDGE_COUNTS.json, NEGATIVE_CONTROLS.json, CENSUS_RECONCILIATION.json, INDEX_VALIDATION.json, SUMMARY.json.
`05_ANALYSIS/`: CONTROLLER_ATTACHMENT_ANALYSIS.json + CONTROLLER_CHAIN_COUNTS.json (the 8-chain investigation).
`00_CONTROL/`: driver + SHA256_DRIVER.txt. `06_REPORT/`: this report + HANDOFF.md. STAGE_ACCEPTANCE_GATES.csv at run root.

**STAGE_ACCEPTANCE_GATES: 6/6 PASS.**
