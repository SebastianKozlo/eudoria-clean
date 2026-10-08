# INPUT_IDENTITIES — PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007

Written at preflight, BEFORE any correction work. Every SHA256 below was measured by
this executor from the physical files at preflight time (2026-10-07T18:37–19:20Z).
All identities MATCHED their dispatch-pinned values; none were substituted from memory;
any mismatch would have been BLOCKED + HARD STOP (none occurred).

## 1. Contract (the instruction set of this correction)

| input | size_bytes | SHA256 |
|---|---|---|
| C:\Users\User\Documents\ChatGPT\PE\PE_935_CAND4_CORRECTION_PROMPT_REVIEW_20261007\OPENCODE_C4_C1_C2_CORRECTION_REVIEWED.md | 11,851 | 364D5C82BBCDD95E44ACF63BB676D026AA482E57950572CE83D71526DD05F348 |

Dispatch-pinned identity: 11,851 B / 364D5C82…DD05F348 — MATCH. Read in full (333
lines, §1–§8) from disk before any work; applied literally, not modified.

## 2. Repository / base state (the write target and its pinned base)

- REPO_ROOT = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean (SebastianKozlo/eudoria-clean)
- EXPECTED_BASE_SHA = 790e83735b439e2d76a250868a47a599c2c10184
- Measured 2026-10-07T18:37:13Z / 18:37:17Z (UTC): LOCAL_HEAD (git rev-parse HEAD) ==
  origin/master (git rev-parse origin/master) == actual remote master (git ls-remote
  origin refs/heads/master) == 790e83735b439e2d76a250868a47a599c2c10184 — MATCH, no
  error, zero mismatch.
- Tracked changes at preflight: NONE. Foreign untracked (inventoried, untouched):
  docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/,
  docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/,
  docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/,
  docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/,
  docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/, experiments/.
- OUTPUT_ROOT docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/
  absent at preflight (Test-Path = False, 2026-10-07T18:37:17Z) — collision check PASS.

## 3. Authoritative Desktop post-audit inputs (the correction basis)

Base directory: C:\Users\User\Documents\ChatGPT\PE\PE_935_CAND4_CHILD_ROOT_DESKTOP_POST_AUDIT_790E837_20261007\

| input | size_bytes | SHA256 (measured) | dispatch pin | match |
|---|---|---|---|---|
| REPORT.md | 12,454 | BDE7B9EB873DF8E80A1E6C6A39B132A3EA1E1545E7A15977571DE7830D63EEEA | BDE7B9EB…D63EEEA | MATCH |
| CONTROL_COUNTERCHECKS.json | 2,443 | 32DC3FEEE9881BADDD40AA44A040499E86071C9D7B0E3B3D0F8E772D8C3CCB4C | 32DC3FEE…C3CCB4C | MATCH |
| EDGE_AND_SCOPE_COUNTERCHECKS.json | 5,042 | E275035BDF9FC8DF6383A8287546AB4009835F8E0DA66254CF5F0EF0B68C22CC | E275035B…B68C22CC | MATCH |

All three were read IN FULL before any work (REPORT.md 224 lines; CONTROL_COUNTERCHECKS.json
85 lines; EDGE_AND_SCOPE_COUNTERCHECKS.json 123 lines). Roles:
- REPORT.md — the Desktop post-audit verdict (REQUIRE_CORRECTIONS) with the C4-C1 (edge
  accounting) and C4-C2 (CTRL_4 exact endpoint) findings and dispositions.
- CONTROL_COUNTERCHECKS.json — the Desktop's countercheck matrix: the two CTRL_4
  false-PASS mutants (0x0050A3F6: 57→56 push esi / 57→90 nop) that keep the old checker's
  boolean PASS, the own exact-endpoint predicate results, and the CTRL_3 foreign accessor
  bytes (8B 81 20 01 00 00 C3 CC at FUN_006C0EE0).
- EDGE_AND_SCOPE_COUNTERCHECKS.json — the Desktop's 8 excluded-but-interpreted rows
  (RV-01..RV-07 + NEIGH-09 with their recorded NOT_COUNTED_REASON content), the
  conservative minimum (>= 32), the new-body minimum (>= 7) and the QC-I5/QC-I9 defect
  analysis.

## 4. SOURCE_PACKAGE (READ-ONLY basis of the re-adjudication)

SOURCE_PACKAGE = docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/
(audited run PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007 at AUDITED_SHA
790e83735b439e2d76a250868a47a599c2c10184 == this correction's BASE).

- 38 files tracked at BASE; 38 physical files present; 38/38 working-tree to git-blob
  identity match (git hash-object == ls-tree blob for every file; measured before work,
  zero mismatches) — the working-tree copies ARE byte-identical to the BASE blobs and are
  the read basis of this correction (the contract's "BASE git blob or byte-identical copy").
- The package's own manifest (MANIFEST_SHA256.csv, ROW_COUNT 38) declares the same 38
  files (final persistence scope incl. AUDIT_ENTRYPOINT.md — identity of that row belongs
  to the persistence phase, out of this correction's scope).
- Used records (read in full or as cited): EDGE_ACCOUNTING_LEDGER.csv (the 69-row census —
  the re-adjudication target), CONTROL_RESULTS.json (the historical control results),
  03_SCRIPTS/qc_controls.py (the old CTRL_3/CTRL_4 implementations — logic read; NOT
  executed as-is because of its top-level writes into SOURCE_PACKAGE; the needed logic was
  re-implemented in this package with pinned provenance), 03_SCRIPTS/qc_internal.py (the
  S-checks incl. the defective S6 reconstruction), 00_CONTROL_INTERNAL_QC/qc_ind_census.py
  (the QC-I5/QC-I9 defect locus), PREREGISTRATION.md (§2/§3/§4 budget + unit rules),
  FINAL_REPORT.md / HANDOFF.md / CLAIM_MATRIX.csv / QC_REPORT.md / PE_MASTER_REVIEW.md
  (the superseded claims), POINTER_LINEAGE.csv (H-1..H-4), FIELD_PRODUCER_LEDGER.csv,
  01_RAW/FUN_006C66D0_GETTER_FULL.txt, 01_RAW/FUN_006C0D50_CTOR_DECODE.txt, 01_RAW/
  FUN_006C8B20_LAZYINIT_DECODE.txt, 01_RAW/FUN_006C6F60_PRODUCER_DECODE.txt, 01_RAW/
  JOIN_WINDOW_50A3B7_REPIN.txt (the published per-instruction window bytes — the clean
  CTRL_4 fixture basis), INPUT_IDENTITIES.md, GOVERNANCE_DECISION.md, EVIDENCE_INDEX.md,
  MANIFEST_SHA256.csv, 03_SCRIPTS/make_manifest.py (format basis of this package's
  manifest generator).
- READ-ONLY discipline: zero writes into SOURCE_PACKAGE by this correction (verified:
  38/38 blob identity re-verified AFTER all work — SOURCE_PACKAGE_UNCHANGED; see
  FINAL_REPORT §5 / HANDOFF).

## 5. Byte-buffer fixtures (synthetic / in-memory only; NO EXE access)

All fixtures are byte constants pinned to PUBLISHED records; no EXE read is performed by
this correction (NEW_PCG_FUNCTION_BODIES_ALLOWED = 0):

- CLEAN_GETTER_FIXTURE = 8B 41 68 C3 CC CC CC CC — the getter body bytes
  @0x006C66D0..0x006C66D7 as persisted in SOURCE_PACKAGE 01_RAW/
  FUN_006C66D0_GETTER_FULL.txt (RAW BYTES line, first 8 of the 96-byte window). Prior pin
  of an already-budgeted, already-opened body (source-run body #1) — not a new probe.
- FOREIGN_ACCESSOR_FIXTURE = 8B 81 20 01 00 00 C3 CC — the bytes historically probed by
  the old CTRL_3 at FUN_006C0EE0 (8-byte read, interpreted as the [+0x120] getter), as
  recorded in SOURCE_PACKAGE CONTROL_RESULTS.json (CTRL_3 mutated_case detail) and
  Desktop CONTROL_COUNTERCHECKS.json (foreign_accessor_bytes). Used here as a RECORDED
  CONSTANT only; the historical probe itself is now ACCOUNTED as the proven 7th real-body
  opening (FUNCTION_BODY_ACCOUNTING.csv row 7; MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7).
- JOIN_WINDOW_CLEAN_BUFFER = the 0x42 (66) bytes of WINDOW 0x0050A3B7..0x0050A3F8 exactly as
  published per-instruction in SOURCE_PACKAGE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt
  (byte sequence and instruction-boundary arithmetic re-verified by this correction:
  every instruction length, both rel8 branch targets, all four rel32 call targets and the
  total window length 0x42 recompute correctly from the published bytes). Basis of the
  CTRL_4 clean case and of the three in-memory mutants (see 03_SCRIPTS/FIXTURES.md).
- All mutants (the historical EDI clobber @0x0050A3DD = 8B 3D D0 D8 B9 00; the final-argument
  mutants 57→56 and 57→90 @0x0050A3F6) are SYNTHETIC, IN-MEMORY ONLY — no mutation is ever
  written to any file outside this package's outputs; nothing is written to the EXE, to
  SOURCE_PACKAGE, or to any historical record.

## 6. Tooling of this correction (no decoder library; no EXE reader)

- 03_SCRIPTS/ctrl3_rebuilt.py — rebuilt CTRL_3 (wrong-manager-field predicate) over
  synthetic/persisted byte fixtures with a minimal in-script ModRM decode of the 8B /r
  mov r32, r/m32 form. No EXE access; no new accessor discovery.
- 03_SCRIPTS/ctrl4_exact_endpoint.py — rebuilt CTRL_4 (caller-side exact final-argument
  predicate) over the published window buffer with a minimal in-script x86-32 linear
  decoder (opcode coverage: 8B/89 mov, 8D lea, 84 test, 74/EB short jumps, 83 grp1-imm8,
  6A push imm8, 50-57 push r32, 58-5F pop r32, BF mov r32-imm32, E8 call rel32, FF /2
  call r/m, 90 nop) and exact-address instruction lookup on correct decode boundaries;
  includes a faithful LOGIC-ONLY reproduction of the old checker (qc_controls.py
  ctrl4_preservation, lines 151–176 semantics) over the same in-memory buffers to
  demonstrate its two false PASS.
- 03_SCRIPTS/build_corrected_ledger.py — builds CORRECTED_EDGE_ACCOUNTING_LEDGER.csv from
  the SOURCE ledger, copying every original column verbatim and appending the corrected
  adjudication (explicit in-script per-row map; the original text is never retyped).
- 03_SCRIPTS/qc_correction.py — the fresh internal QC (SELF-REVIEW; see QC_REPORT.md):
  content-based re-derivation of the corrected classification from the SOURCE ledger
  (NOT trusting LEDGER_CLASS or the corrected ledger's own class column), body-accounting
  verification incl. a package-script scan for undeclared real-body probes, control
  result verification against the Desktop counterchecks, no-new-science-branch sweep,
  corrected wrapper terminology checks, historical-FAIL preservation checks, source
  package immutability, encoding, repo state.
- 03_SCRIPTS/make_manifest.py — the manifest generator (format/provenance derived from the
  source package's 03_SCRIPTS/make_manifest.py, rewritten for this package; scope = the
  physical OUTPUT_ROOT files minus the manifest; entrypoint excluded pending persistence).
- Python 3.12.10 (CPython; stdlib only — hashlib/csv/json/os/re/subprocess/sys). No
  capstone, no pe_reader, no EXE reads, no network, no runtime.

## 7. Private scratch (outside the repo; registered; not published)

SCRATCH_DIR = C:\Users\User\AppData\Local\Temp\opencode\PE_935_CAND4_CORR_R1 (registered;
transient binary-safe hashing/verification work outside the repo). The failed tar-based
extraction attempt there (corrupted PowerShell pipe) created no repo content and was
discarded; the working-tree == BASE-blob identity method (38/38) was used instead.

## 8. Preflight verification record (measured)

- Contract identity: §1 — MATCH (11,851 B / 364D5C82…).
- Base triple verification: §2 — LOCAL_HEAD == origin/master == actual remote ==
  EXPECTED_BASE_SHA 790e837… (queries 2026-10-07T18:37:13Z / 18:37:17Z).
- Desktop inputs: §3 — all three MATCH their pins; read in full.
- SOURCE_PACKAGE: §4 — 38/38 BASE blob identity (read-only basis established).
- OUTPUT_ROOT: absent (collision check PASS).
- No other inputs are used by this run. No EXE access of any kind; no payloads; no
  VFS/BNT/NIF; no runtime; the EXE identity of the source run (8,015,872 B / E7785430…
  D5280F31) is carried as context only and is NOT re-measured (no artifact of this
  correction depends on an EXE read).
