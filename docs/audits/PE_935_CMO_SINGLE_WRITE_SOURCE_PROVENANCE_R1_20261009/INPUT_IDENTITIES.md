# INPUT_IDENTITIES — PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009

All identities MEASURED at preflight (2026-10-08/09, local executor session)
with independent size + SHA256, compared against the contract's expected pairs.
No metadata assertion was trusted without measurement.

## 1. Contract and repository identity

| Item | Measured value | Expected | Status |
|---|---|---|---|
| Contract file | C:\Users\User\Downloads\OPENCODE_CMO_SINGLE_WRITE_PROVENANCE_R1_REVISED.md | — | — |
| Contract SIZE | 20158 bytes | 20158 | MATCH |
| Contract SHA256 | C6599C0CCEB93DA5CD0E6B950DC3EF8AE6826FA962ABE99492F3931C7244CEB5 | same | MATCH |
| Repo | D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean (SebastianKozlo/eudoria-clean, branch master) | — | — |
| git HEAD | b2feef34122d2118da6ab38fc78f20f337315570 | EXPECTED_BASE_SHA b2feef34122d2118da6ab38fc78f20f337315570 | MATCH |
| origin/master | b2feef34122d2118da6ab38fc78f20f337315570 | same | MATCH |
| remote refs/heads/master (git ls-remote) | b2feef34122d2118da6ab38fc78f20f337315570 | same | MATCH (triple verified) |
| Tracked tree | clean (git status --porcelain: no tracked modifications) | clean | MATCH |
| OUTPUT_ROOT | absent before creation (verified) then created per §11 | must not pre-exist | MATCH |

## 2. Primary corpus identity (fail-closed)

| Item | Measured | Expected | Status |
|---|---|---|---|
| PRIMARY_EXE = D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8015872 bytes | 8015872 | MATCH |
| EXE SHA256 (full independent rehash, preflight) | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | same | MATCH |
| EXE SHA256 (re-verified inside the science script via Source B load_pinned()) | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | same | MATCH (post-science rehash recorded in CONTROL_RESULTS.json) |

## 3. Pinned source A — docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/ (commit-tracked; 49 files)

| File | Measured bytes | Expected | Measured SHA256 | Expected | Status |
|---|---:|---:|---|---|---|
| PRE_REGISTERED_ANCHORS.md | 10650 | 10650 | ABC21A0D9C36C564F2328648AF1997D93810813B44D337C55A027B1B24F3A695 | same | MATCH |
| 01_RAW/FUN_00528E50_CONTINUATION.txt | 5471 | 5471 | BAB06CEB76C33AB47B69A9A27E7D18F1AAA81481EB8F5AA1D9DD3EE5AF16DBD1 | same | MATCH |
| 01_RAW/FUN_509x_SF_METHODS.txt | 6078 | 6078 | 3A011632A3D96050FDB1DA81D3231C28BECDE3E8517F3820E57E495C8B9FEC85 | same | MATCH |
| FINAL_REPORT.md | 13663 | 13663 | E62B7581564A2A6B6946EDFDA29D5077D333C485647A9E2F5969E5732AD8C75B | same | MATCH |

Source A status (era/status discipline): the source run's ACTIVE
interpretations are subject to J3 SUPERSESSION (S-1..S-5), in particular
S-5 for transform standing. Source A is used for: the PA4 CMO-ctor pin scope
([CMO+0xC0] store @0x00528FEA; SF re-receipt @0x0052901A; the three SF-method
calls), the FUN_00509510 SF+0x4C `rep movsd` record (used ONLY as a
must-not-conflate object-distinction record), and the REPIN_ANCHOR_WINDOWS
PA1-PA4/CH1 raw windows. Its transform claim
(`SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC`) is SUPERSEDED by J3 S-5
and is NOT used as an active conclusion.

## 4. Pinned source B — read-only validated bounded PE reader

| File | Measured bytes | Expected | Measured SHA256 | Expected | Status |
|---|---:|---:|---|---|---|
| docs/audits/PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008/03_SCRIPTS/checker_plus4_successor_v2.py | 38568 | 38568 | 80EBEE27883AA61173737590FB822B3503B4658CDA511B4B690F8E75B6B64E62 | same | MATCH |

Import-inertness: verified by FULL READ of the 776-line file before reuse.
Module level contains ONLY constants (EXE_PATH/EXE_SIZE/EXE_SHA256,
IMAGE_BASE_PIN, classification strings, CANONICAL_RECORD_IDENTITY, pin
tables) plus class/function definitions; the executable entry is guarded by
`if __name__ == "__main__": sys.exit(main())` (line 775). It sets
`sys.dont_write_bytecode = True` at import. Reuse mode: imported read-only by
the science script; used ONLY for `load_pinned()` + `RangeSafePE` read API;
the file is never modified.

## 5. Pinned source J3 — ACTIVE supersession (read BEFORE any source-A transform use)

| File | Measured bytes | Expected | Measured SHA256 | Expected | Status |
|---|---:|---:|---|---|---|
| docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/SUPERSESSION.md | 8339 | 8339 | DD11137A0E79491511A7688B7C1DE9252DB7BA443FA31892C345CA76CE136845 | same | MATCH |
| docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/CORRECTED_STATUS_ALGEBRA.md | 8987 | 8987 | 00D09B0F72F1F6859C9DAF8A73C592659F251B596588DA304D9BC6912A40FA9F | same | MATCH |

J3 sections read COMPLETELY. S-5 applied verbatim (see PREREGISTRATION §3).
J3 historical ORIGINAL_EDGE_BUDGET_COMPLIANCE=FAIL (22 vs 6) preserved WITHOUT
transfer to this run (this run uses 0 edges).

## 6. Further required historical context (measured identity before use; read-only)

| File | Measured bytes | SHA256 |
|---|---:|---|
| docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006/FINAL_REPORT.md | 14656 | 39DA4D869400D43F3675280EA38B6314618EAD10F3FD1DB1E839DE5989BEEA7A |
| docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/CLAIM_MATRIX.csv | 5232 | 32F81A962262ACB5DAF668A425B57775F2F6BD2C117D702B26EBF23763C75DDF |
| docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/01_RAW/REPIN_ANCHOR_WINDOWS.txt | 18633 | 5BE0AC8A5BE0F46BD9FE1E200173E86174CF795D3D5A000E028C5C8032D370F3 |

## 7. Governance inputs (identity pinned before use)

| File | Measured bytes | SHA256 | Status |
|---|---:|---|---|
| AUDIT_ENTRYPOINT.md | 266375 | 9377E0FE6E288EE321C44D7FB0BDBDDDF04F375F800F942AA41546729DA21EF4 | present; NOT modified by this run (no entrypoint writes per dispatch) |
| PROJECT_OPERATING_MODEL.md | 54413 | 99AE12375A9C4D60A4034263F2DE1D26EA5A817F12D630BA5B5340C672169E2A | present; read-only context |
| PROJECT_STATE.json | — | — | ABSENT (recorded N/A; not invented; contract §2 anticipated absence) |

## 8. Additional committed evidence measured/used for anchor discovery (all commit-tracked at BASE; untracked packages excluded)

Anchor discovery searched COMMITTED documentation only. The CMO-related
committed packages enumerated and searched (git ls-files counts verified):

| Package (docs/audits/...) | Tracked files | Role in this run |
|---|---:|---|
| PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 | 211 | candidate store family (REPORT S9/RESEARCH_FINDINGS; 01_RAW/T1_REGION_0085B100_0085B900.txt raw bytes; 01_RAW/DECOMP/F0085B1B0.c Ghidra decompile; SEAM_FLOW_MAP) — historical status of its field labels: axes/units UNRESOLVED (its own §conclusions), used as historical context only |
| PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 | 179 | candidate store family (06_REPORT/REPORT.md §4.1 item 4 + ERRATA_R5; 01_RAW/F00746560_CTOR_COPY.txt 4-byte accessor pin; 00_CONTROL/PRE_EDIT/REPORT.md.pre same content) |
| PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006 | 36 | CMO ctor canon (prologue pins, [CMO+0xC0] store @0x00528FEA, vtable 0x00A7DCB0 @0x00528EA2, `8B F1` @0x00528E76, RTTI_PROBES.json ClientMovableObject RTTI chain) |
| PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006 | 21 | corrected ledger wording (P3-2: vtable store VA 0x00528EA2 with `89 9E A4 00 00 00` at 0x00528EA8 noted) |
| PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006 | 49 | source A (see §3) |
| PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007 | 27 | source J3 (see §5) |
| PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008 | 80 | source B (see §4) |
| PE_NIGHT_AGGREGATE_20260905_160000 | 119 | committed Ghidra disassembly of the store window (GHIDRA_H5_VTABLE2.txt lines 1169819-1169826: 0085b27a CALL / 0085b27f MOV ECX,[EAX] / 0085b281 MOV [ESI+0x44],ECX / 0085b284 / 0085b287 / 0085b28a / 0085b28d) |
| PE_935_SF_ARG2_PROVENANCE_R1_20260914 | 36 | FUN_00528E50 "writer of container+0xC0" canon (B3_PIN_REVERIFICATION) |
| PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915 | 45 | holder/vtable inventory context |
| PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 | 41 | SF+0x30 writers canon (object-distinction context) |
| PE_935_STATIC_INSTANCE_TRACE_R1_20260913 | 210 | RTTI census context (S1_RTTI_CENSUS .?AVClientMovableObject@@ @0x00B79960) |
| PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913 | 13 | desktop audit context |
| PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915 | (tracked) | ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt — negative-boundary check: its +0x44-family store hits are the request-queue family, NOT the CMO instance |

EXCLUDED from anchor-discovery evidence (foreign, untracked at BASE — census
recorded, left intact, untouched):
- docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/ (untracked)
- docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/ (untracked)
- docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ (untracked)
- docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/ (untracked)
- docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/ (untracked; contains CMO-context text but is NOT committed evidence — excluded per contract §4 "committed evidence ONLY")
- experiments/ (untracked)

## 9. Era statement

Primary target = PCG_9_3_5 / Entropia Universe 9.3.5 (build EXE SHA256
E7785430..., 8015872 B). All physical reads in this run come from that single
pinned EXE. No 2003-era corpus, no MindArk asset payloads, no other builds.

## 10. Preflight verdict

PREFLIGHT = PASS (git triple MATCH, tracked tree clean, OUTPUT_ROOT created
only after verification of absence, EXE size+SHA MATCH, all pinned source
pairs MATCH, J3 read before source-A use, governance pinned, PROJECT_STATE.json
recorded N/A/absent). SCIENCE_EXECUTED = YES (the bounded re-pin + provenance
derivation of the single selected store, within the pre-registered budget).
