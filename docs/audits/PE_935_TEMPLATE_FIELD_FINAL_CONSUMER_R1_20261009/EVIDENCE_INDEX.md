# EVIDENCE_INDEX — PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_R1_20261009

Every package file (this index self-excluded) hashed from disk AFTER the run's final
write. SHA256 lowercase. File count: 18 (EVIDENCE_INDEX.md itself excluded).

## Package artifacts

| path | size | sha256 |
|---|---|---|
| ANCHOR_008BD720_CLASSIFICATION.json | 4260 | cb73b429a49c4832125e1aa663a3aed10a95318eeb1dadfeeede06404440ef53 |
| ARGUMENT_PROVENANCE.json | 6994 | 8b2e5a33fee8fe9b95dce821967cdbf80069f41cca5ef0232a00fb1ca72519d8 |
| BODY_CFG_AND_ACCESS_CENSUS.json | 11128 | 3d6903142d2c5e2cb75b744a2f5a11717b51c5216e9cccd30466acefd8bf4222 |
| FALSIFIER_RESULTS.json | 12934 | ec8a8a1b7d283a1ea6e3b036454ca7d9797d21a4bcce83a36f3c780fabd1bad0 |
| FINAL_REPORT.md | 17307 | 3071b30c1ca051483e1a36c5cebd2490005a5f7ff0b6c125134e0c61ca5e39b0 |
| HANDOFF.md | 15197 | 5558b870b5c9ae808e834174bba357ff6d229cbe7beb4c013aacad60c7b3145a |
| INPUT_IDENTITIES.json | 6543 | 1e6ca4b980127911f481e173fb8856625e7b06be14b468bf3ce93963cc110b83 |
| PREREGISTRATION.md | 16413 | 97bd8b05cdc4b32f1e866af5814b94d3e0100084ecf7e3f14db950acb9ebd2f4 |
| VALUE_DISPOSITION.json | 6113 | 35c10b12723231f7bca2edc74099f7c7d6b87912cfce1c2ffa98d2880ebd4b03 |
| 01_RAW/ANCHOR_008BD720_16B_DUMP.json | 811 | c44e0c221acc961114d2f06484af347038322ae2a5496a1f36063a0c44382fbb |
| 01_RAW/ESP_SLOT_MAP.json | 20684 | a807f4cf306027d60b9d94360de0ef1a594a22f1005f8241020489df6ded7453 |
| 01_RAW/GHIDRA_HYPOTHESIS_EXPORT.json | 4466 | 3f8367e506d69dbf359e7a1b55749c4b267f4cf53d4c7e144ad76efa4b41404b |
| 01_RAW/KEY_REGION_LISTINGS.md | 10058 | 25190273e65fb9a894ffd381e49816cff7c03fcc8f90da6c8a3a194c359a4b32 |
| 01_RAW/OWN_DECODER_WINDOWS.json | 64133 | a7176934dbb2ae064ed5f973b8e493f4099349893308c227892dd1504326f3a1 |
| 01_RAW/OBJDUMP_LISTINGS/objdump_W_CALLER_FUN_006C3F50.txt | 2950 | 41b1f1548933a4e1978d76bcea5fd38fc302aed43169717d26caa7a54a08d0d5 |
| 01_RAW/OBJDUMP_LISTINGS/objdump_W_DEP1_FUN_0040B070.txt | 307 | d8195ccc3a85bfd1b824510c1bc1cf5ad49c2cd3deb974cc41440a396aad7ec3 |
| 01_RAW/OBJDUMP_LISTINGS/objdump_W_DEP2_FUN_007CE1E0.txt | 316 | 53fff57b99ab466a02256e7ca3762822d6af072dbb904bd0b5a925442c1610f0 |
| 01_RAW/OBJDUMP_LISTINGS/objdump_W_SUBJ_FUN_006C3640.txt | 2645 | 36a39f965b34616a9fc02934bb25a1ae4d7d4fe3486ab49f8ba9c0f5a4b72929 |

## Tooling provenance (SCRATCH, local-only, outside git)

| script | size | sha256 |
|---|---|---|
| analyze.py | 9331 | 691d5dc37702d341ddabef092157ea6a09e79c744d3eb227d6d4566746dcf599 |
| dbg_entry.py | 878 | 448394ccd0686c33b307df3b899c04f50f3b5d0e7d2a3443f9aebe36ed3f85db |
| dump_hypothesis_fc.py | 3293 | 9768cb3c2aa54530e6f464706c816ebdf0827fa236a65bbae0b201fdeed9dbc1 |
| extract_recon.py | 3696 | be50f4bf0f0cab6aecc370f8ea8ac71f1f32e3ef35e3170f7988cd12842c6585 |
| make_evidence_index.py | 4404 | a74792d7eed4875865a9293b2f754859c7eeae775a000c2c39b7ec948f8127e5 |
| make_listings.py | 5894 | e0976c788b5fd3551537ce0b0e6719868bbc9e09d87af786ef7de16fe2dcb548 |
| package_raw.py | 3700 | e004893bf65e0c82ecdcde276300a226dc20119a0c0ba9e1ac378e030fa81ca3 |
| sim_slots.py | 9910 | f9e8edf80c725131cd8b66e837510e93099bc8a343ba68ed7fe01844e6e90153 |
| verify_baseline.py | 2436 | 40f779f44162a5909699f712523dfd1957e78941140ee2ffd537716f46d9e7a4 |
| x86dec.py | 28252 | b288897a18f9a0b500f6535f18338deb5568a9dca1634814c4920bc6e11bd602 |

## Evidence map (claim -> primary evidence)

- Anchor identity (CALL 0x006C3FCD -> 0x006C3640): ARGUMENT_PROVENANCE.json anchor_call; 01_RAW/OWN_DECODER_WINDOWS.json (F7 rel32 recompute); 01_RAW/OBJDUMP_LISTINGS/objdump_W_CALLER_FUN_006C3F50.txt
- Argument slot table (6 slots): ARGUMENT_PROVENANCE.json; 01_RAW/ESP_SLOT_MAP.json (W_CALLER.anchor_pushes + callee read map)
- Subject body structure/CFG/census: BODY_CFG_AND_ACCESS_CENSUS.json; 01_RAW/KEY_REGION_LISTINGS.md; 01_RAW/OWN_DECODER_WINDOWS.json (W_SUBJ decode)
- arg6 dead (never read): BODY_CFG_AND_ACCESS_CENSUS.json tracked_value_register_usage; 01_RAW/ESP_SLOT_MAP.json (W_SUBJ.arg6_never_read = true; machine scan)
- Per-value dispositions: VALUE_DISPOSITION.json
- 0x008BD720 identity: ANCHOR_008BD720_CLASSIFICATION.json; 01_RAW/ANCHOR_008BD720_16B_DUMP.json; 01_RAW/GHIDRA_HYPOTHESIS_EXPORT.json (quarantined corroboration)
- Falsifier outcomes: FALSIFIER_RESULTS.json
- Dual-decode agreement (F7 gate): 01_RAW/OWN_DECODER_WINDOWS.json f7_gate (0 disagreements / 105 instructions)
- FPU/SSE absence (F3): 01_RAW/OWN_DECODER_WINDOWS.json f3_fpu_sse_scan (0/0)
- Boundary determination + preregistration: PREREGISTRATION.md (windows/budgets/falsifiers declared before the science)
- Input identities: INPUT_IDENTITIES.json (EXE SHA before/after, git, predecessor integrity, toolchain)
- objdump independent listings: 01_RAW/OBJDUMP_LISTINGS/ (4 files)

## Integrity notes

- Raw .bin slices stay in SCRATCH (no payloads in the package); slice SHA256s recorded
  in 01_RAW/OWN_DECODER_WINDOWS.json exe_slices.
- The predecessor package (PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009) was reopened
  READ-ONLY; all 27 of its manifest rows re-hashed BEFORE and AFTER this run: 27/27 match
  both times (0 mismatches). AUDIT_ENTRYPOINT.md untouched.
- Zero .pyc/__pycache__ residue in this run's locations (scan 0/0; python -B throughout).
- SCRATCH intermediates (analysis outputs, raw_slices/) are intentionally NOT hash-pinned
  here (local-only, outside git); the final window slices ARE pinned by SHA256 in
  01_RAW/OWN_DECODER_WINDOWS.json exe_slices (QC_R1 finding P3-2 note).
