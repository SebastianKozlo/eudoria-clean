# QC_REPORT — PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_QC_R1_20261009

- **QC_RUN_ID**: PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_QC_R1_20261009
- **RUN_ID_AUDITED**: PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_R1_20261009
- **QC_CLASS**: INTERNAL_QC — fresh-context pe-master-auditor child dispatched by PE-MASTER
  (NO_NESTED_TASKS; NOT a Desktop post-audit; NOT executor self-review).
- **VERDICT**: **QC_PASS_WITH_FINDINGS** — every load-bearing claim independently re-measured
  and CONFIRMED; 0× P0, 0× P1, 3× P2, 2× P3 (documentation/record precision only).
- **What this QC did NOT do**: no executor artifact modified (only the two QC outputs the
  dispatch ordered into the package root); no commit/push; no AUDIT_ENTRYPOINT.md touch;
  no MANIFEST; the 16 B at 0x008BD720 were byte-verified but NOT decoded (the quarantined
  0x18-thunk hypothesis is not adjudicated here).
- **QC inputs**: all 18 package files read in full (OWN_DECODER_WINDOWS.json additionally
  processed record-by-record: all 105 instruction records compared against the auditor's own
  decode, 0 diffs); SCRATCH evidence inspected; executor SCRATCH scripts NOT read to EOF —
  they are hash-pinned (10/10 re-verified) and every load-bearing output was independently
  re-derived from the physical EXE by the auditor's own pipeline, so no claim rests on
  unread script internals (honest NOT_CHECKED entry).
- **Auditor tooling (AUDITOR_RECHECK)**: fresh pure-Python PE parser, fresh restricted
  x86-32 decoder (strict; raises on any FPU/SSE/prefix opcode), fresh CFG-worklist
  ESP-depth sim — all under SCRATCH\QC_FRESH\ (qc1_identity.py / qc2_decode.py /
  qc3_espsim.py / qc4_repo.py; outputs qc1–qc4 JSON). All byte work in binary-mode Python
  (no PowerShell redirection / no '>' transcoding anywhere in the byte path). python -B
  throughout; final residue scan incl. QC_FRESH: 0 hits.

---

## D1 — IDENTITY: PASS

| Check | Result |
|---|---|
| EXE re-hash (auditor) | 8,015,872 B; SHA256 `E7785430…F31` == expected — **MATCH** |
| Predecessor `PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009` | all 27 MANIFEST_SHA256.csv rows re-hashed from disk: **27/27 MATCH** (incl. the entrypoint row) |
| Git | HEAD == origin/master == live `ls-remote` master == BASE `fbb6e958…` (all four re-verified by the auditor) |
| Tracked tree | worktree diff and cached diff **EMPTY**; zero tracked files modified |
| Untracked set | exactly the new package + the 6 declared foreign paths (matches INPUT_IDENTITIES declaration) |
| .pyc / __pycache__ | **0** (auditor scan of SCRATCH + package) |
| Package inventory | 19 files = 18 declared + EVIDENCE_INDEX.md (self-excluded) ✓; **28/28 EVIDENCE_INDEX hash rows re-verified** (18 package + 10 tooling scripts; sizes + SHA256 all MATCH) |

## D2 — SUBJECT PINS (auditor's own byte reads, own PE parser): ALL MATCH

- **Windows**: W-SUBJ 0x006C3640–0x006C36A8 = **105 B** (RET C3 @0x36A8 + 6×CC + next
  prologue `55 8B 6C 24 10…` @0x36B0 — body-end rule satisfied); W-CALLER 0x006C3F50–0x006C3FDB
  = **140 B** (RET C3 + 4×CC + next prologue @0x3FE0). W-DEP1 `8D 41 14 C3`; W-DEP2 `8B 41 08 C3`.
- **Anchor**: `E8 6E F6 FF FF` @0x006C3FCD; rel32 = **−2450**; next_va 0x006C3FD2; recomputed
  target **0x006C3640** == subject entry — MATCH.
- **Caller pins**: `BB 20 D7 8B 00` @0x006C3FB0 (imm32 == **0x008BD720**) MATCH; `8B 50 04`
  @0x006C3FBE MATCH; `8B 00` @0x006C3FC1 MATCH; push sequence **51/53/56/52/50** @FC3–FC7 +
  `8D 4C 24 30` @FC8 + `51` @FCC MATCH.
- **Loop/append/growth VAs**: `3B FD`/`74 4E` @0x364A/4C; `8B CF` @0x3658; **`FF D3` @0x365A**;
  `8B 4E 04`/`3B 4E 08` @0x365C/5F; **`89 11`/`89 41 04` @0x366A/0x366F**; `83 46 04 08` @0x3672;
  **`83 C7 20` @0x368A**; `3B FD`/`75 C7` @0x368D/8F; **`E8 76 F7 FF FF` @0x3685 → 0x006C2E00**;
  `89 30` @0x3695; `89 08` @0x36A5; RET C3 both epilogues — ALL MATCH my decode.
- **16 B @0x008BD720**: == `8D 41 18 C3 CC×12` (file-mapped @0x4BD720, .text, in_text TRUE);
  SHA256 `de298cd7…d9f8` == ANCHOR_008BD720_16B_DUMP.json — MATCH. **Not decoded by the auditor.**
- **Independent decode**: 47 + 54 + 2 + 2 = **105 instructions**; 0 disagreements vs the
  package objdump listings (all 4 windows) and vs all 105 executor decoder records;
  contiguous full coverage ending at the RETs.

## D3 — DATAFLOW / ESP SIM (auditor's own CFG-worklist sim): CONFIRMED

- **Slot table (CONFIRMED)**: arg1 = &caller_param_2 (push ECX @FCC, eo 4); **arg2 = [P+0x14]
  (push EAX @FC7, eo 8)**; arg3 = [P+0x18] (push EDX @FC6, eo 0xC); arg4 = caller vector
  (push ESI @FC5, eo 0x10); arg5 = 0x008BD720 (push EBX @FC4, eo 0x14); **arg6 = [P+8] (push
  ECX @FC3, eo 0x18)**. Push depths 24/28/32/36/40/44; depth at anchor call 44; callee read
  offsets join 6/6.
- **arg6 DEAD — CONFIRMED**: my sim enumerates exactly **8 esp-relative ops** in W-SUBJ
  (7 accesses + 1 LEA; entry_offsets arg3/arg2/arg5/arg4/arg1/&arg1-LEA/arg1/arg4);
  **none resolves to entry_offset 0x18** — arg6 is never read; discarded by ADD ESP,0x18.
- **Growth-path frame balance — CONFIRMED**: growth cleanup **20** derived from join equality
  (fast 16 == growth 36−X ⇒ X=20); callback cleanup 0; merges @0x3672/0x3658/0x368A all (16,16);
  both RETs at depth 0. Caller side: getter+lookup combined cleanup 4; **both split variants
  produce identical downstream maps** (split invariance independently reproduced); growth
  @0x3FA9 cleanup 20; RET @0x3FDB depth 0.
- **F4 ABI conditions — CONFIRMED reasonable**: all loop-carried carriers (EDI/EBP/EBX/ESI)
  are callee-saved-class across the two CLOSED calls; no crossing relies on EAX/ECX/EDX
  survival; the preservation assumption is recorded as an explicit condition (not waived,
  not silently proven) — correct treatment for CLOSED bodies.
- **F8 disjointness — CONFIRMED**: container chain: ESI's only in-window writer is @0x3F79,
  loading from the incoming param_2 slot (entry_offset 8); template chain: P = lookup return
  → EDI @0x3F67; no in-window instruction derives ESI from P's chain; the tracked values
  reach memory as data 0 times in W-SUBJ. Container ≠ template object.

## D4 — FALSIFIER AUDIT: PASS

All 8 falsifiers designed (PREREGISTRATION §7) and executed with the 4-part record
(MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED).

**F1 adjudication — THE EXECUTOR IS RIGHT.** The frozen contract said "arg2 = [P+0x14] with
push @0x006C3FC3". Auditor bytes: 0x006C3FC3 = `51` (push ECX) where ECX = LOCAL_B = **[P+8]**
(loaded @0x3FBA from the local saved @0x3F83, source getter2 0x007CE1E0 = [P+8]); **[P+0x14]
is pushed @0x006C3FC7** (`50`, push EAX, EAX = [P+0x14] loaded @0x3FC1 `8B 00` from the
0x0040B070 thunk return). The contract's slot attributions are CONFIRMED correct; its VA
annotations were imprecise; the executor's corrected slot table is byte-correct, and its
PROMPT_VA_ANNOTATION_CORRECTION classification is appropriate.

The auditor independently replicated the load-bearing measurements of F1 (slot join), F2
(census + base-provenance classes), F3 (FPU/SSE 0/0 over 105 insns), F4 (crossing census),
F5 (per-path EAX census; growth-call return machine-verified UNUSED; caller never reads EAX
after the anchor call), F6 (Ghidra export exists only as quarantined hypothesis; no gate claim
cites it), F7 (0 disagreements — a third decode), F8 (disjointness).

## D5 — GATES/RECORDS: PASS (7/7 gates supported; findings below)

- **G1–G7**: all PASS, each re-verified by the auditor's own measurements (details in QC_RESULTS.json).
- **Preregistration-before-science**: consistent — PREREGISTRATION.md is the earliest-mtime
  package file (11:44:13 < final objdump listings 11:49:21 < everything else); content matches
  the executed structure. (mtime = weak evidence; nothing contradicts the ordering.)
- **Budget respected**: dual-verified decode scope == declared windows: **105 + 140 + 4 + 4 =
  253 B code + 16 B data** — auditor-verified by exact window sizes and full coverage;
  packaged listings contain ONLY the windows. Phase-0 raw boundary-scan slices (subj 4096 B /
  caller 176 B; recon_manifest.json) are disclosed pre-science recon material (raw bytes, no
  published decode beyond the windows) — not a violation.
- **Counts**: 105 total instructions CONFIRMED (47+54+2+2). Access census = **16 memory
  accesses + 1 LEA = 17 rows** CONFIRMED (esp-frame/args 7+1; container 3; callback-result 2;
  cursor 2; arg1-slot 2). F3 scan 0/0 replicated. Note for the reader: the correct
  decomposition is "16 accesses + 1 LEA" — FINAL_REPORT/BODY_CFG/F2 are correct; HANDOFF's
  "17 esp-relative operations" phrasing is wrong (P2-3).
- **Claim limits verbatim**: identical strings confirmed in FINAL_REPORT §10 / HANDOFF /
  FALSIFIER_RESULTS.
- **Zero promotion**: auditor term-scan: 91 occurrences of position/rotation/scale/transform/
  coordinate/placement/XYZ — **all in negation/discipline/claim-limit contexts**; the
  quarantined 0x18-thunk hypothesis is explicitly labeled UNVERIFIED, excluded from gates,
  not decoded, not promoted.
- **EVIDENCE_INDEX**: 28/28 rows re-verified (18 package + 10 scripts).
- **NOT_CHECKED honesty**: adjudicated honest (closed callees not decoded; forbidden
  addresses have no in-window edges — confirmed by the auditor's decode; STATIC_ONLY respected).
- **Intervention ledger**: adjudicated **HONEST** (Ghidra reuse pre-declared; 4 tooling
  defects disclosed pre-conclusion, caught by the discipline machinery, fixed, re-run;
  2 PowerShell quoting failures disclosed; no undisclosed intervention; auditor's
  independent replication corroborates the final state). **NO VIOLATION.**

---

## FINDINGS LEDGER

**P2-1 — BODY_CFG_AND_ACCESS_CENSUS.json BB_exit block count off-by-one (declared 6, actual 7).**
Source: `cfg.blocks[8]` `{BB_exit, 0x006C3691-0x006C369B, insns: 6}`. Counter-evidence: the
dual-verified stream (and the auditor's decode) has 7 instructions in that range
(0x3691 mov eax,[esp+0x14]; 0x3695 mov [eax],esi; 0x3697/98/99/9A pops; 0x369B ret); the 10
declared block counts sum to 46 ≠ 47. Mechanism: manual census slip in a machine-readable
artifact. Scope: record precision only — the block RANGE, roles, the 47 total and the
16+1 access census are all correct; no gate/disposition depends on the per-block field.
Correction: change `insns: 6` → `7` in a records-correction round (block counts then sum to
47). Revalidation: corrected sum == 47 == auditor decode; other fields byte-unchanged;
EVIDENCE_INDEX row re-hashed.

**P2-2 — FALSIFIER_RESULTS.json F1 itemization internally inconsistent (multiset sums to 9, stated total 8).**
Source: `falsifiers[0].measured_quantity` "{arg1 x3, arg2 x1, arg3 x1, arg4 x2, arg5 x1,
&arg1 x1}". Counter-evidence: ESP_SLOT_MAP + auditor sim = exactly 8 ops = arg1×2 +
&arg1(LEA)×1 + arg2×1 + arg3×1 + arg4×2 + arg5×1. Mechanism: prose double-count of the
arg1-slot family. Scope: prose precision only; the count 8, the join and the PASS are
correct; arg6-dead unaffected. Correction: reword to the 8-element multiset. Revalidation:
multiset sums to 8; EVIDENCE_INDEX row re-hashed.

**P2-3 — HANDOFF.md mislabels the census as "17 esp-relative operations" (actual: 8 esp-relative ops; 17 = total census rows).**
Source: HANDOFF.md PER-VALUE DISPOSITION arg6 bullet. Counter-evidence: auditor sim —
8 esp-relative operations (7 accesses + 1 LEA); the other 9 census rows are esi/eax/ecx-based;
FINAL_REPORT §4 and BODY_CFG census_note are correct. Mechanism: handoff-summary wording
drift. Scope: the arg6-dead claim is correct either way; a reader could mis-derive the
esp-op denominator. Correction: reword to "0 of the window's 17 census rows (16 accesses +
1 LEA; 8 of them esp-relative) resolve to entry offset 0x18". Revalidation: consistent with
BODY_CFG/VALUE_DISPOSITION wording; EVIDENCE_INDEX row re-hashed.

**P3-1 — Invalid UTF-8 byte 0x97 (CP1252 em-dash) in line 1 of EVIDENCE_INDEX.md (offset 17) and 01_RAW/KEY_REGION_LISTINGS.md (offset 22).**
Counter-evidence: strict UTF-8 decode fails at those offsets; the other package files decode
cleanly. Mechanism: generator wrote a CP1252 em-dash byte. Scope: cosmetic + one-byte
machine-parseability; no content loss. Correction: replace 0x97 with UTF-8 em-dash (E2 80 94)
in a records round; KEY_REGION_LISTINGS.md's EVIDENCE_INDEX row must be re-hashed in the same
round (EVIDENCE_INDEX.md itself is self-excluded from its table).

**P3-2 (observation, no action) — SCRATCH intermediates (analysis_results.json, dbg_entry.json,
ghidra_hypothesis_raw.json, sim_slots.json, Phase-0 recon slices) are not hash-pinned in
EVIDENCE_INDEX** (only the 10 scripts are; the 4 final window slices ARE pinned by SHA256
inside OWN_DECODER_WINDOWS.json — auditor re-verified against both the physical EXE and the
on-disk slices: all MATCH). Scope/provenance nit for local-only, non-load-bearing files.

---

## COVERAGE (honest)

- FULL_READ: all 18 package files (OWN_DECODER_WINDOWS.json: structural read + complete
  programmatic comparison of all 105 records).
- RECOMPUTED by the auditor: EXE/section identity; 4 window slices; anchor rel32; all byte
  pins; instruction decode of all 253 B (105 insns, 0 disagreements with both prior decoders);
  FPU/SSE scan; ESP-depth sim both windows (incl. both getter/lookup split variants); slot
  join; arg6-dead; growth/caller cleanups from frame balance; EAX census incl. growth-return-
  unused; 28 EVIDENCE_INDEX hashes; 27 predecessor manifest rows; git quad-check; pyc scan.
- NOT_CHECKED by the auditor (explicit): executor SCRATCH script internals (see QC inputs —
  mitigated by independent replication + hash pinning); the body semantics of 0x008BD720 and
  0x006C2E00 (CLOSED; hypothesis not adjudicated); runtime behavior (STATIC_ONLY); foreign
  untracked dirs' content vs a baseline (no baseline exists — set-membership + zero tracked
  impact verified instead).

## NEXT PARENT ACTION

PE-MASTER decision: (a) accept QC_PASS_WITH_FINDINGS and dispatch a bounded records-correction
round for P2-1/P2-2/P2-3/P3-1 (pure text/count fixes + EVIDENCE_INDEX re-hash; zero semantic
change to any claim), then persist/publish per its own plan; (b) optionally open the new
bounded 4-byte dual-decode contract at 0x008BD720 to settle the quarantined thunk-family
hypothesis; (c) milestone closure remains PE-MASTER's/human's gate — not this QC's.
