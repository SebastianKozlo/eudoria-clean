# QC_REPORT — PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007

SELF-CLASSIFICATION: this is the executor's own fresh-context INTERNAL QC
(SELF_CHECK, contract §9) — NOT an independent external Desktop post-audit and
NOT a PE-MASTER qualification. Machine measurements: 03_SCRIPTS/qc_internal.py ->
QC_INTERNAL_RESULTS.json (OVERALL = QC_PASS, 23/23 checks). Control machinery:
03_SCRIPTS/qc_controls.py -> CONTROL_RESULTS.json (CTRL_1..4 all PASS).

## 1. What was independently re-verified (fresh reads from the hash-pinned EXE)

- S1 EXE identity: 8,015,872 B / SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 — MATCH (fail-closed import + re-hash).
- S2 all 56 recorded byte pins re-read at their exact VAs — ALL MATCH (zero mismatches).
- S3 all 23 recorded rel32 call targets independently recomputed — ALL MATCH (zero mismatches).
- S4 load-bearing facts re-verified byte-for-byte: the getter body (8B 41 68 C3),
  the writer store (89 7E 68 @0x006C67E2), the writer source read (8B 78 04
  @0x006C67BE), both name constants (push 0x00A859F8 = 'ArkTexture'; push
  0x00A8547C = 'ArkAnimation'), and the empty-string lookup key (0x00A7957B =
  0x00; 'Entropia' at 0x00A7957C).
- S5 the RTTI class names re-derived from the vtable COL chains:
  .?AVArkModelManagerMain@@ (0xA855D0), .?AVArkModelManager@@ (0xA85A08),
  .?AVArkModelResourceInstanceRef@@ (0xA864B8) — MATCH.

## 2. Edge-count reconstruction (the §9 mandate)

- S6 ACCOUNTED_EDGE_COUNT (EDGE_ACCOUNTING_LEDGER.csv ANALYZED_NEW rows) = 24.
  INDEPENDENT_RECONSTRUCTED_EDGE_COUNT = 24. ACCOUNTED_EDGE_COUNT ==
  INDEPENDENT_RECONSTRUCTED_EDGE_COUNT (PASS).
- Completeness of the census within the analyzed scope: the QC independently
  decoded the 6 opened bodies' recorded extents (FUN_006C66D0: 4 B;
  FUN_006C0D50: 0x5E B; FUN_006C8F80: 0xB6 B; FUN_006C8B20: 0x8A B;
  FUN_006C6F60: 0x112 B; FUN_006C6780: the 0xC8 B partial window) and
  enumerated every CALL instruction in them (26): every one appears in the
  ledger as ANALYZED_NEW or RAW_VISIBLE_ONLY (zero missing; zero in-body rows
  without a matching CALL instruction). The 5 caller-side units E-01..E-05 are
  callsites in the PRIOR-decoded callers (FUN_0050A310/FUN_006A3930) and are
  outside the opened-extent census by design (recorded as ledger rows).
- EDGE_ACCOUNTING_STATUS = BUDGET_EXCEEDED (24 > MAX 8; 16 past the stop line).
  ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL — recorded honestly in the ledger
  header and FINAL_REPORT §5; RETROACTIVE_PRIOR_AUTHORIZATION = NO.

## 3. Budget ledger re-derivation

- NEW_FUNCTION_BODIES_OPENED = 6/6 (the 6th — FUN_006C6780 — PARTIAL with
  extent UNRESOLVED past 0x006C6848; the load-bearing facts are inside the
  seen window; no continuation claimed).
- NEW_MANAGER_FIELD_WRITERS_TRACED = 2/6 (W1 NULL reset; W2 value producer)
  plus 3 declared coverage gaps (GAP-1 creation-chain internals; GAP-2
  FUN_006C8BB0; GAP-3 off-path writers out of scope by governance).
- NEW_WRAPPER_HOPS = 2/3 (H-1, H-2; H-3/H-4 are SAME_OBJECT moves, not hops).
- NEW_CHILD_PROVENANCE_CANDIDATES = 3/3 (ctor reset; producer chain;
  FUN_006C8BB0 alternative — the limit reached exactly).

## 4. Status algebra + claim checks

- S8 components re-checked: CHILD_RESOURCE_PROVENANCE =
  STRONGLY_SUPPORTED_MODEL_DERIVED; CHILD_VISUAL_ROLE = UNRESOLVED;
  CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED (NOT CONFIRMED); EXACT_PARENT =
  CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (carried). CHILD_EVIDENCE_COMPLETE =
  FALSE => CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND (the
  weakest required edge honored; no averaging up).
- S9 overclaim sweep: no forbidden ACTIVE claim token outside
  negation/policy/formula-definition contexts (the §8 formula quotes in
  PREREGISTRATION/FINAL_REPORT are definition contexts; no
  CONFIRMED_MODEL_DERIVED claim; no CHILD_TO_JOIN_IDENTITY = CONFIRMED claim;
  no SCIENCE_PASS anywhere; RUNTIME_JOIN_OBSERVED = NO; WORLD_XYZ_RECOVERED = NO).
- S10 the four §9 controls: CTRL_1..4 all PASS (each: clean PASS -> mutated
  FAIL on the SAME checker, same range, recorded cause; the real-input
  classification of CTRL_1 is recorded POLICY_ONLY — the real child is not
  confirmed main-visual by absence of the §6 proof legs, not by detection).

## 5. Package integrity checks

- S11 encoding: every package file is UTF-8 without BOM with LF line endings
  (zero violations).
- S12 historical packages immutable: P1 (the audited source run) 49/49 BASE
  git-blob identity match, 0 missing; P2 (the J1–J3 correction) 27/27 match,
  0 missing — read-only preserved throughout this run.
- S13 repo state: HEAD == d65fa12e5bae4e9aab291c3cc7815b1822e41cff (== BASE);
  zero tracked modifications; the 6 foreign untracked roots untouched; this
  run's OUTPUT_ROOT is the only new content under docs/audits/.

## 6. QC-tooling defects found and fixed (QC scripts only; NO executor evidence was modified)

Round 1 (5 defects, all in qc_internal.py unless noted):
1. S2 pin-name regex did not match names containing parentheses/spaces (fixed:
   relaxed the name pattern) — the pins themselves always verified (zero
   mismatches from the first run).
2. S6 "extra rows" logic flagged E-01..E-05 (callsites in prior-decoded
   callers) as outside the opened extents — fixed: the completeness check now
   applies only to rows whose CALLER is one of the 6 opened bodies, and each
   such row must match a real CALL instruction in that body's extent.
3. S7 hop filter used exact string equality on RELATION_TYPE and missed
   SAME_OBJECT values carrying annotation text — fixed with a startswith test.
4. S9 overclaim sweep scanned the 03_SCRIPTS/*.py checker files themselves
   (whose check-definition strings legitimately contain the forbidden tokens)
   and missed the formula-definition context of the §8 algebra quote — fixed:
   machinery scripts excluded; negation/policy and IF-formula contexts allowed.
5. S12 prior-package immutability was first computed with a different
   path-format aggregate than the preflight (false mismatch) — fixed: the QC
   now re-runs the preflight's git-blob identity method (49/49 + 27/27 MATCH).
Round 2 (1 defect): S2's byte-count regex required at least 2 bytes per pin and
missed the four 1-byte pins (50/57) — fixed: the byte pattern now accepts a
single byte; 56/56 pin lines verified.
Also in qc_controls.py round 1: CTRL_2's operand comparison used capstone's
0x-prefixed offset format while capstone 5.0.7 prints small offsets unprefixed
([eax + 4]) — a checker-spec defect that made the CLEAN case fail; fixed in the
checker (both formats accepted). No control fixture or result semantics
changed: all four controls re-ran clean PASS -> mutated FAIL.

## 7. QC verdict

QC_VERDICT = QC_PASS (SELF_CHECK; 23/23 checks) — with the explicit
classification above. The run's component findings stand on the re-verified
bytes; the edge-budget exceedance (24 analyzed units vs MAX 8) is an honest
process finding disclosed by this run itself (EDGE_ACCOUNTING_LEDGER header,
FINAL_REPORT §5, HANDOFF): it does not falsify the byte evidence, and no
retroactive authorization is claimed. The four §9 machinery controls PASS;
their PASS is falsifiability-of-the-predicate evidence only (SYNTHETIC PASS is
not PCG science).

NOT_CHECKED by this QC (explicit): the four §7 intervening callee bodies
(FUN_006C0F90, FUN_006C10B0, FUN_0050A1E0, FUN_005246E0); FUN_006C8BB0;
FUN_006C9700 and the creation chain internals; FUN_007B6C30; the manager vtable
slot-2/slot-3 target bodies (0x006C0FD0/0x006C19B0); all neighbor bodies caught
by windows (NEIGH rows); the FUN_006C6780 unseen continuation; runtime anything
(STATIC-ONLY); payloads; the independent PE-MASTER audit of THIS package
(pending).

## 8. Record-repair log (RECORDS-ONLY; post-internal-QC; 2026-10-07)

Records-repair session: PE-MASTER direct dispatch continuation of
PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007 (records-only closure of the
internal-QC findings; NO_NESTED_TASKS). Origin: the independent internal QC of
this package (00_CONTROL_INTERNAL_QC/QC_IND_REPORT.md +
QC_IND_RESULTS.json; verdict QC_PASS_WITH_FINDINGS; 5 findings, ALL P3).
PE-MASTER adjudication of the findings: ALL CORRECT-AND-FIXED. This log
records the records-only repair executed after that QC: label/annotation/
record edits based on already-measured facts; ZERO new RE, ZERO new bodies
opened, ZERO new analysis. All learning statuses of the run are UNCHANGED
(CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND; edges
NEW_INTERPROCEDURAL_EDGES_SEMANTICALLY_ANALYZED = 24 ANALYZED_NEW unchanged;
closure/provenance/visual-role statuses unchanged).

- F-QC-A fixed (NEIGH row-range annotation defects; ONLY the range labels
  changed — every referenced row exists in the ledger and is byte-verified by
  the internal QC):
  01_RAW/FUN_006C8F80_BASECTOR_DECODE.txt now cites NEIGH-12..NEIGH-20
  (base-ctor window rows); 01_RAW/FUN_006C8B20_LAZYINIT_DECODE.txt now cites
  NEIGH-21..NEIGH-24 (FUN_006C8BB0-window rows);
  01_RAW/FUN_006C6F60_PRODUCER_DECODE.txt now cites NEIGH-25..NEIGH-27
  (producer-window rows; the nonexistent NEIGH-28..NEIGH-31 label removed);
  FIELD_PRODUCER_LEDGER.csv GAP-2 evidence cell now cites NEIGH-21..NEIGH-24.
- F-QC-B fixed (garbled window-end sentence):
  FUN_006C6F60_PRODUCER_DECODE.txt window-end rewritten to ONE clear
  statement — the window ends at 0x006C70F0 (LEN 400); the malformed
  "0x006C7088+0xC8 = 0x006C7088?" draft fragment removed.
- F-QC-C fixed (inaccurate directory-census sentence): INPUT_IDENTITIES.md
  §5 Gamebryo-2.6-mirror availability justification now states the physical
  D:\gamebyroengine listing ('extracted' directory incl. the Gb12_Source oracle tree;
  'Gamebryo 1.1.2 Evaluation' directory; 'Gamebryo 1.1.2 Evaluation.zip';
  'Gamebryo 1.2 Source.rar'; 'GameBryo2.6.7z'; 'gamebryo_1.2.7z';
  'Gamebryo_Version_1.1.2_Gamebryo_2004.iso'; 'GB_2.3.iso'). Operative
  ruling UNCHANGED: the .7z archive is not the sigmaco/gamebryo-v2.6 git
  mirror at commit 329cd25; identity unmeasurable without extraction (out
  of scope) => NOT_USED; no oracle-based mechanism claim exists anywhere in
  the package.
- F-QC-D fixed (unpersisted re-hash attribution): the HANDOFF.md "Manifest
  verification" section now attributes the independent manifest re-hash to
  the internal QC (00_CONTROL_INTERNAL_QC/QC_IND_RESULTS.json — 27/27
  size+SHA256 MATCH, zero mismatch), notes the persistence phase repeats
  the re-hash over the final physical package, and drops the false "reported
  in QC_REPORT.md" citation (the executor-phase QC checks §1-§7 predate the
  manifest generation and contain no re-hash record).
- F-QC-E fixed (the four prior-scope §7 intervening callsites had no ledger
  row): EDGE_ACCOUNTING_LEDGER.csv gained four REPIN_PRIOR_SCOPE rows
  RP-08..RP-11 (0x0050A3B9->FUN_006C0F90; 0x0050A3CF->FUN_006C10B0;
  0x0050A3D8->FUN_0050A1E0; 0x0050A3E4->FUN_005246E0), each COUNTED=NO
  with a per-row reason (prior-recorded interpretation of the source run's
  join-window record + its QC S4; free re-verification; no new semantics;
  the four callee bodies remain NOT_CHECKED). Ledger census after the
  repair: 69 rows = 24 ANALYZED_NEW (UNCHANGED) + 7 RAW_VISIBLE_ONLY + 11
  REPIN_PRIOR_SCOPE + 27 OUT_OF_ANALYZED_EXTENT. EVIDENCE_INDEX.md wording
  narrowed from "the FULL callsite census" to the per-row-class census
  scope with the 4 prior-scope rows now present. Consequential
  census-summary consistency updates (same measured facts; no claim,
  classification or ANALYZED_NEW count changed): FINAL_REPORT.md §4
  (7 -> 11 REPIN_PRIOR_SCOPE), CLAIM_MATRIX.csv CL-14 evidence cell
  (7 -> 11 REPIN), HANDOFF.md key-artifact note (41 -> 45 non-counted rows).

Post-repair verification (this records-repair session; read-only after the
manifest regeneration):
- Per-finding revalidation: F-QC-A — every cited NEIGH range now equals the
  ledger rows enumerated for that window; F-QC-B — the producer window-end
  record contains exactly one window-end arithmetic, 0x006C70F0; F-QC-C —
  the directory census quoted in INPUT_IDENTITIES.md equals the physical
  listing; F-QC-D — the manifest-verification note cites the persisted
  internal-QC record; F-QC-E — the ledger enumerates every callsite touched
  by the run's records with a class and reason for each.
- MANIFEST_SHA256.csv REGENERATED LAST (after every edit above; the
  every-write-after-the-manifest rule). Scope UNCHANGED: the executor-phase
  package files minus the manifest (ROW_COUNT = 27; the same 27 paths as
  the previous manifest, re-verified); 00_CONTROL_INTERNAL_QC/ stays OUT
  pending the persistence-phase regeneration over the final physical
  package; AUDIT_ENTRYPOINT.md excluded pending persistence. Generator
  bijection self-check: PASS (zero missing/extra/duplicate; sizes+SHA256
  re-read from disk at generation). INDEPENDENT post-generation re-hash by
  a separate implementation (generator = Python hashlib; verifier = .NET
  SHA-256 via PowerShell): performed by this session, result reported in
  its terminal response (not written as a package file — any write after
  the manifest requires regeneration; the persistence phase repeats the
  re-hash over the final package and persists its own record).
- Encoding: every package file (incl. 00_CONTROL_INTERNAL_QC/, read-only
  there) UTF-8 no-BOM, LF-only, strict-decodable — zero violations (scan
  re-run by this session).
- Repo state: HEAD == BASE d65fa12e5bae4e9aab291c3cc7815b1822e41cff; no
  commit/push by this repair; AUDIT_ENTRYPOINT.md untouched; the two prior
  evidence packages untouched; the 00_CONTROL_INTERNAL_QC records
  untouched; no new files created inside the package (in-place edits + the
  manifest regeneration only).
