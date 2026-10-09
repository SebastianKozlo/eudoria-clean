# INPUT_IDENTITIES — PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009

Production executor record (this file was referenced by PREREGISTRATION.md as
written by the first executor session; that session CRASHED before creating it.
This fresh retry session re-performed the ENTIRE preflight from physical bytes
and writes it now. Nothing below is inherited from the crashed session without
re-verification.)

## I1. Authorization (recorded before science)

- Authoritative contract:
  `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_ENTRY_CALLER_BRIDGE_PROMPT_REVIEW_20261009\OPENCODE_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_REVISED_20261009.md`
  SIZE=23187 B, SHA256=773C1310A2CB02B365068EE2D9C684A97765E4D416E30B415B8672D8CC09FF07.
  Verified byte-for-byte (Get-FileHash SHA256) BEFORE any other action of this
  retry session. MATCH. The contract alone authorizes nothing; the actual
  dispatch is the human-authorized worker assignment delivered to this OpenCode
  executor session (2026-10-09, agent `pe-reconstruction`, model
  `nask-glm/glm-5-3`), identifying the contract by exact path/size/SHA256 and
  authorizing exactly RUN_ID PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009
  including the crash-continuation instruction for the 3 crash-left files.
- Scope granted to THIS worker (production package only, all under OUTPUT_ROOT):
  PREREGISTRATION.md (extension), INPUT_IDENTITIES.md (this file),
  WINDOW_IDENTITIES.json, 01_RAW/ raw disassembler text per window,
  ENTRY_FRAME_LEDGER.csv, CALLER_STACK_LEDGER.csv, BRIDGE_PROVENANCE.json,
  CLAIM_MATRIX.csv, 03_SCRIPTS/run_frame_bridge.py, CONTROL_RESULTS.json,
  ARTIFACT_CONTROL_RESULTS.json, SUPERSESSION_AND_STANDING.md.
- Explicitly NOT this worker's (per dispatch): qc_frame_bridge.py +
  QC_RESULTS.json + QC_REPORT.md (separate fresh-QC worker/session);
  FINAL_REPORT.md / PE_MASTER_REVIEW.md / EVIDENCE_INDEX.md / HANDOFF.md /
  MANIFEST / AUDIT_ENTRYPOINT.md row / any stage/commit/push (parent phases).
  Fresh internal QC: NOT_PERFORMED_BY_THIS_WORKER (never invented, never faked).
- No commit, no push, no entrypoint write, no modification of any file outside
  OUTPUT_ROOT in this session.

## I2. Session continuity — prior executor crash (disclosure)

- A PRIOR executor session (same RUN_ID; it recorded itself in PREREGISTRATION.md
  P1 as model `nask-glm/glm-5-2`) CRASHED mid-run and returned an EMPTY handoff.
  On disk it left EXACTLY 3 files under OUTPUT_ROOT (this retry session's
  discovery census, sizes and SHA256 at discovery):

  | File | Size | SHA256 at discovery |
  |---|---:|---|
  | PREREGISTRATION.md | 19151 B | F36DE40AF53CEE9FE2F0F5A11A65475239E5035DE96F2FD45D4E5669E775EACC |
  | 01_RAW/WINDOW_A_OBJDUMP.txt | 1882 B | 7AABA008CFBD8BAF4CDF868BA25E3E9A014E9F732E375402553AAA3282D2C86B |
  | 01_RAW/WINDOW_B_OBJDUMP.txt | 1557 B | B82C5532D1E10EE3116C7E74EA72471257FA1E3A110F7BCFEA0C452B01ED99CC |

- Verification performed by THIS retry session:
  1. PREREGISTRATION.md — full-content review against the contract: complete and
     PRE-consistent (contains only the contract's §1/§4/§5/§6/§7 expected
     hypotheses, scope, budgets, controls and stop rules; NO post-science result
     leakage). Decision: KEPT as the preregistration of record (its P1–P9 body
     is NOT rewritten; PRE is never rewritten to match POST), extended with the
     dated section P10 (session continuity disclosure).
  2. 01_RAW/WINDOW_A_OBJDUMP.txt — header records GNU objdump (GNU Binutils for
     Debian) 2.44, command with --adjust-vma=0x528e50, fixture provenance
     (66 bytes from the EXE at raw offset 1216080, SHA256
     F8735567340CD3BE2F6B64B4BBC2BE292487E97B6184758CA408E6FF1CE78E85), exit
     status 0. Its disassembly section (23 instruction lines) is BYTE-IDENTICAL
     to this session's own fresh objdump invocation on an independently
     extracted fixture (WINDOW_IDENTITIES.json
     crash_continuation_verification.A.disassembly_lines_identical = true).
     The crashed session's temp fixture (still present at discovery) hashes to the
     pinned window-A SHA256 — equal to this session's retry fixture bytes.
     Decision: KEPT unchanged (sound; authorized path).
  3. 01_RAW/WINDOW_B_OBJDUMP.txt — same verification: --adjust-vma=0x4c4792,
     52 bytes at raw offset 804754, SHA256
     B59E16DC116F4CE0438A1E92BC6B2CBC33FAB0B19FABC24CB3A29C911C1EFB6A,
     rc 0, 17 instruction lines byte-identical to this session's fresh
     invocation (…B.disassembly_lines_identical = true). Decision: KEPT
     unchanged.
  4. Continuation decision: this retry re-performed the ENTIRE preflight from
     physical bytes (git triple, EXE hash, window extraction/hashes, all 8
     required repo inputs, PE section mapping, toolchain identity) and re-ran
     all science (disassembly verification, Phase A, Phase B, bridge join,
     12-case control matrix, artifact gate) with its own invocations. No claim
     from the crashed session is reused without re-derivation; the only reused
     artifacts are the 3 verified files above. This retry session's fresh raw
     invocations are additionally persisted as 01_RAW/WINDOW_A_OBJDUMP_RETRY.txt
     and 01_RAW/WINDOW_B_OBJDUMP_RETRY.txt.

## I3. Git identity (preflight, re-verified)

```text
LOCAL_HEAD              = ce75b7b3ee0b7b87c1f0a03bc79167169aed71a0
origin/master           = ce75b7b3ee0b7b87c1f0a03bc79167169aed71a0
ACTUAL REMOTE master    = ce75b7b3ee0b7b87c1f0a03bc79167169aed71a0
(git ls-remote origin master — queried live at preflight; a cached tracking
 ref alone is NOT relied on)
EXPECTED_BASE_SHA       = ce75b7b3ee0b7b87c1f0a03bc79167169aed71a0   MATCH
tracked worktree/index  = clean (0 modified, 0 staged tracked paths)
untracked inventory     = 5 unrelated foreign audit dirs + experiments/
                          (pre-existing; inventoried; left untouched)
OUTPUT_ROOT at preflight = the 3 crash-left files of I2 (disclosed; the
                          dispatch authorizes keep-or-regenerate, not the
                          contract's pristine-absent condition; nothing else
                          pre-existed)
```

## I4. Read-only binary identity (re-hashed before AND after all work)

```text
EXE_PATH   = D:\Eudoria_Reconstruction\pcg_install\Entropia.exe
EXE_SIZE   = 8015872 B                    (contract pin 8015872 — MATCH)
EXE_SHA256 = E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
             (re-hashed before every mode run and after all work: UNCHANGED;
              every run_frame_bridge.py invocation re-verifies and prints it)
```

## I5. Physical code windows (extracted from the EXE and hashed by this session)

| Window | Half-open VA interval | Bytes | Raw offset | SHA256 (physical == pin) |
|---|---|---:|---:|---|
| A | [0x00528E50,0x00528E92) | 66 | 1216080 / 0x128E50 | F8735567340CD3BE2F6B64B4BBC2BE292487E97B6184758CA408E6FF1CE78E85 |
| B | [0x004C4792,0x004C47C6) | 52 | 804754 / 0x0C4792 | B59E16DC116F4CE0438A1E92BC6B2CBC33FAB0B19FABC24CB3A29C911C1EFB6A |

PE mapping (identity/mapping only; PE header + section table read, not
interpreted as code): ImageBase 0x400000; 5 sections; both windows' RVAs
(0x128E50, 0x0C4792) lie ENTIRELY inside `.text` RVA [0x1000,0x6745E5),
RAW-backed (raw range [0x1000,0x675000)), unique mapping, no BSS ambiguity;
raw offset == RVA for `.text` (PointerToRawData == VirtualAddress == 0x1000).
Decode: window A = 23 contiguous instructions covering the window exactly
(first VA 0x00528E50, last call ends exactly at 0x00528E92); window B = 16
contiguous instructions covering it exactly (ends at 0x004C47C6). Boundary
provenance cross-check: the pinned historical listings
F00528E50_CTOR_MOBJ.txt (blob 3648e1b86aa6933df6017840a20704f04e642bc1) and
F004C46C0_CREATE.txt (blob dc61d1b45df788b257c49771c0e55668fa2036b8) show the
same instruction streams at the window boundaries (input records only; function
starts were NOT inferred from padding or E8 searches).

## I6. Required repository inputs at BASE (physical size/SHA256 + worktree==HEAD blob equality)

| Repository path | Bytes | SHA256 (match) | git blob == HEAD blob |
|---|---:|---|---|
| docs/audits/PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913/01_RAW/F00528E50_CTOR_MOBJ.txt | 8613 | YES = A6ECDFD8350EA511625E296337002F1C45E3CAA8309D79CA843B35088903AF56 | YES; blob 3648e1b86aa6933df6017840a20704f04e642bc1 == pinned blob A |
| docs/audits/PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913/01_RAW/F004C46C0_CREATE.txt | 14517 | YES = 32BDC6455F98078ED7D198FA96AD98ACF5D86908CA1B4DC950E6127EA3F7AF6D | YES; blob dc61d1b45df788b257c49771c0e55668fa2036b8 == pinned blob B |
| docs/audits/PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009/FINAL_REPORT.md | 19514 | YES = 0F84FC111D893778CA410DC83A439E2A8E653FBB9466F409828DC3BC419DF762 | YES |
| docs/audits/PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009/ARG1_PROVENANCE.json | 10071 | YES = 29FF09675BEC2A4604524CBD202E6542AA850FD54A6ABBAEFF0395BF6813F85E | YES |
| docs/audits/PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009/SUPERSESSION_AND_STANDING.md | 6848 | YES = 0AB2CDECE09CB2FF1419C48E9A1169832A0A061C618A7F94F290089C75F49921 | YES |
| docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/SUPERSESSION.md | 8339 | YES = DD11137A0E79491511A7688B7C1DE9252DB7BA443FA31892C345CA76CE136845 | YES |
| docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/CORRECTED_STATUS_ALGEBRA.md | 8987 | YES = 00D09B0F72F1F6859C9DAF8A73C592659F251B596588DA304D9BC6912A40FA9F | YES |
| AUDIT_ENTRYPOINT.md | 273796 | YES = 9F5E83940ECD0496FA21310C5AEAFE6F49D4631F86D495BF4E536548B6AD84A5 | YES |

Applicable operating-model/governance rules and supersessions were read
(contract §0/§2; CMO_C1 SUPERSESSION_AND_STANDING.md; J3 SUPERSESSION.md and
CORRECTED_STATUS_ALGEBRA.md; prior ARG1_PROVENANCE.json and its FINAL_REPORT.md).
No genuine authorization conflict was found; the dispatched scope is not blanket
milestone authority.

## I7. Toolchain (verified live by this session)

```text
Disassembler : GNU objdump (GNU Binutils for Debian) 2.44 — WSL distro PE-AI
               (Debian; kernel 6.18.33.2-microsoft-standard-WSL2)
Command form : objdump -D -b binary -m i386 -M intel --adjust-vma=<VA> <fixture>
               (rc 0 recorded for every invocation; raw outputs persisted)
Python       : Python 3.13.5 (WSL PE-AI), invoked as python3 -B (no .pyc residue)
Replay       : 03_SCRIPTS/run_frame_bridge.py (this package; decoder-assisted
               symbolic replay; fail-closed on unsupported shapes; the ONLY
               decoder is GNU objdump)
```

## I8. Temporary fixtures (outside Git; removed at end of run)

Synthetic control fixtures and mutated artifact-control copies were created only
under `C:\Users\User\AppData\Local\Temp\opencode\PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009\`
(outside the repository; never staged). No `.bin` window extract is committed;
the persisted 01_RAW artifacts are disassembly TEXT only. The temp directory is
removed at the end of this run.

## I9. Scope-compliance census (this production run)

```text
AUTHORIZED_PARTIAL_CODE_WINDOWS          = 2 of max 2        (A 66 B, B 52 B)
UNIQUE_ORIGINAL_CODE_BYTES_ANALYZED     = 118 of max 118    (66 + 52; disjoint)
COMPLETE_FUNCTION_BODIES_TO_OPEN         = 0
NEW_CALLEE_BODIES                        = 0 (0x0085B1B0 and 0x0095D3C4 unopened)
TARGET_CALLSITES_ANALYZED                = {0x004C47C1, 0x00528E8D} (2 of 2)
INCIDENTAL_OPAQUE_CALLSITE               = 0x004C4797 -> 0x0095D3C4 (opaque,
                                           AS3 condition recorded, never opened)
UPSTREAM_BEYOND_WINDOW_B                 = 0
OTHER_CALLSITES_OR_XREF_CENSUS           = 0
FIELD_SEMANTIC_PROMOTIONS                = 0
RUNTIME / NETWORK / MODEL / VFS_BNT_NIF  = 0
Gamebryo/OpenMW research                 = 0 (not performed, not loaded)
```

The EXE was read only for: whole-file hashing, PE header/section-table reads
(identity/mapping), and the two pinned window byte ranges (the interpreted code
bytes). Physical metadata reads are separated from interpreted code bytes in the
records above.
