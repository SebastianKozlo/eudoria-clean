# QC_AUDIT_R2.md — G13 FRESH-CONTEXT INDEPENDENT RE-QC (post-PACKAGING_AND_PROVENANCE_CORRECTION) — PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915

- QC session: FRESH independent pe-master-auditor session (did NOT formalize, execute,
  correct or self-check this run; not the R1 QC session; not the executor).
- Date: 2026-09-15 | Mode: INTERNAL_QC re-QC (G13) after the bounded
  PACKAGING_AND_PROVENANCE_CORRECTION batch (AMEND_LOG_R2.md R2-6) | STATIC-ONLY
  (the client binary was NEVER executed by this session; it was never opened either —
  this re-QC worked from the package artifacts, git read-only commands and its own
  recomputations of the packaged raw data).
- Scope: bounded PACKAGE/PROVENANCE re-QC per the 12-item PE-MASTER mandate. This is NOT
  a new science run: the R2 science result is standing (externally work-audited +
  PE-MASTER spot-checked); this re-QC verifies the package/provenance state and that
  the packaging batch did not disturb the science (raw byte-identity + headline-number
  stability — item 11).
- QC tooling: countercheck scripts OUTSIDE the package at
  `C:\Users\User\AppData\Local\Temp\opencode\pe_qc_holder_r2\` (AUDITOR COUNTERCHECK,
  NOT project evidence):
  - qc1_hashes.ps1 (SHA256 574697BE131C99F1AD0448BF59EC6A12AAFB41FFF03F0535FE2FD4B4F3EE2DB3, 7,509 B) — package-wide hash, pins, registries, manifest, pycache, payload scan
  - qc2_rawdata.ps1 (SHA256 A185F3B23C74F9E7D8D030E889333228A75327F81E31DB1341A18125C2DA2B47, 3,912 B) — independent recomputation of the science numbers from the raw CSVs + [IV-8] verification
  - qc3_ledger.ps1 (SHA256 362E68C558915966DC8CD61C19D1109D9929C913EFC658F012F34E9D00C2408B, 5,246 B) — R2-6 OLD->NEW ledger consistency vs current disk + old-hash leak check
  - package_hashes.csv (SHA256 9A9FD7670BFBA81AC2ED780EB0E390EB74109F38477D3C440EC7FAF78B3B24A, 4,748 B) — all 43 file hashes measured by this session
- Git: ZERO mutations by this session (read-only commands only: rev-parse, ls-remote,
  status --porcelain). The ONLY file created inside the package by this session is this
  QC_AUDIT_R2.md (mandate-authorized; intentionally NOT added to MANIFEST_SHA256.csv,
  which this session must not mutate; per the same convention as QC_AUDIT.md).

## FINAL VERDICT: **QC_PASS_WITH_FINDINGS**

Two P3 findings (informational, non-blocking, dispositioned in §FINDINGS). All 12
mandate items verified independently and PASS. No P0/P1/P2 defect found. The package/
provenance state is consistent, complete and honest; the packaging batch did not
disturb the raw science evidence (all 16 raw pins byte-identical) nor the six
load-bearing science numbers (all re-verified against the packaged raw data).

## GIT READ-ONLY OBSERVATION (measured by this session, before and after the audit work)

- HEAD == origin/master == ls-remote == `895bbc8baa2d002c562b7e5b43212e38c2abb16f`
  (branch master) — matches the mandate's expected state exactly, at both the start and
  the end of this re-QC session.
- `git status --porcelain` == exactly:
  `?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`,
  `?? docs/audits/PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915/`,
  `?? experiments/` — the expected untracked set; no modified/staged tracked path; no
  deviation.
- ZERO git mutations by this session (no add/commit/push/stash/checkout/reset).

## PER-ITEM VERDICTS (items 1–12 of the mandate)

### Item 1 — AMEND_LOG_R2.md exists and matches the actual correction history: **PASS**

- `00_CONTROL/AMEND_LOG_R2.md` exists (29,429 B; disk SHA256
  `28BC33DE4CDA985854584668D1FB0D5B728A677CE43460ED66FB90027A469CF4`; manifest row 3).
- Entries match the declared history exactly:
  R2-1 = the universal-NULL defect + the edge-aware slice engine (EdgeContext,
  MULTI_PATH/MULTI_ENTRY, test/cmp read-model, this-cross); R2-2 = declared slice bound
  widened 4→6 levels; R2-3 = corrected held-value disposition (per-class table) + the
  retractions it supersedes; R2-4 = SceneFeeder re-base (REJECTED AT THE
  RECEIVER-IDENTITY LINK) + the QC P3-x fixes sub-section (P3-1..P3-8, all completed on
  disk — [N7] 57-function/22-refs, [C4] complete caller census, ArkVegetationObservable
  real dword 0x566B7241, PIN-NN printed address 0x00A8CD38, AT_RUN_END timestamp,
  AT_RUN_START re-point to AMEND_LOG_R1 A8, [IV-0d] PSP/PSPMod sites, 0x00AA7958 RTTI
  wording); R2-5 = secondary corrections (fault-shortcut retraction, P2-1
  "no statically-identifiable caller" qualification, P2-2 [C8] histogram under a
  declared rule); R2-6 = bulk-copy channel bound + the final packaging-repair
  sub-section (a)–(j) with OLD→NEW SHA256 pairs.
- OLD SHA256 sample verification (mandate-required):
  - pre-R2 `HOLDER14_WRITER_RAW.txt` `8E2B17E010BBE6DB47792110DE8CF3A9DBB3C800F599A32984C73E80422DB6FD`
    (38,942 B) appears as the OLD value in R2-1 ✓ → NEW `50F3AD14C2045B272A95DB2AD2E2AE96D6559F713610700F6190FAFF9AB26CCD`
    (83,245 B) == the CURRENT pinned raw ✓.
  - pre-packaging `REPORT.md` `889232AB54872A93E37FA06B55AFB4A0440E8E3470C23F14F89FFD34AAE9A17D`
    (22,468 B) appears as the OLD value in R2-6 (h) ✓ → NEW `AAD491552F24E4C3573A59085D70D38FAE92E872C6F4EC6ECD92ECB35E52A494`
    (24,583 B) == the CURRENT disk REPORT ✓; and `889232AB…` consistently appears as
    the NEW value of the R2-3 science batch (OLD `20DF475D…`, 13,681 B) — the ledger
    chain is internally consistent end-to-end:
    REPORT `20DF475D` → `889232AB` (R2-3) → `AAD49155` (R2-6 h) ✓;
    HOLDER14_PROVENANCE `F2921B0E` → `85AB003A` (R2-3) → `CF170AA3` (R2-6 h) ✓;
    RECEIVER_IDENTITY `1EFF528E` → `404D15EA` (R2-3) → `9174B2E2` (R2-6 h) ✓;
    SCIENCE_STATUS_DELTA `0704799E` → `39AA96D2` (R2-3) → `F16FDF08` (R2-6 h) ✓.
  - R2-4/R2-5 NEW values equal the current pinned raws (NEGCTL 859B5626…,
    CENSUS_SUMMARY 199413B8…, ARG2_VALUE_FLOW 1CE0D33A…, IDENTITY_VERIFICATION
    EAE24400…, AT_RUN_END E39CE917…, AT_RUN_START A28A326C…, FORWARDER 1DA2F284…,
    ARG2_UPSTREAM 1B85729C…) ✓ — all also equal the §3 raw pins (item 11).
- ALL 17 NEW values printed in the R2-6 sub-section (b)(c)(d)(e)(h)(j) + the ledger's
  own manifest row + the 7 corrected script registry rows verified EQUAL to the current
  disk hashes and sizes (qc3: R26_NEW_FAILURES=0).
- The R1-era manifest hashes are gone from the current manifest: 23 OLD values tested
  against the current MANIFEST_SHA256.csv text — OLD_HASH_LEAKS=0 ✓ (the OLD values
  survive only inside the ledger's historical entries, which is where they belong).

### Item 2 — no dangling AMEND_LOG_R2 references: **PASS**

- Whole-package grep for `AMEND_LOG_R2`: **70 reference lines** across 15 files —
  matches the mandate's expectation (~70 incl. the ledger's own citations).
- Classification (measured per file):
  - The original 51 dangling references (ledger R2-6 (a) enumeration) — REPORT.md 8,
    HOLDER14_WRITER_RAW.txt 17, HOLDER14_PROVENANCE.md 4, RECEIVER_IDENTITY.md 2,
    ARG2_UPSTREAM_ANALYSIS.md 2, SCIENCE_STATUS_DELTA.csv 3, FORWARDER_ANALYSIS.md 1,
    phase_c_anchor.py 6, s0_common.py 8 = 51 — **all now resolve** to the existing
    `00_CONTROL/AMEND_LOG_R2.md` (entries R2-1..R2-6) ✓.
  - 19 packaging-batch-added references: HANDOFF.md 7, STAGE_ACCEPTANCE_GATES.csv 2,
    EVIDENCE_INDEX.csv 2, MANIFEST_SHA256.csv 1, SOURCE_IDENTITIES.json 1,
    AMEND_LOG_R2.md self-citations 5, and +1 in REPORT.md (line 11, the R2 CORRECTION
    PROVENANCE header added by the (h) regeneration). 51 + 19 = 70 ✓.
- No reference points to any other path variant; every occurrence is either
  `00_CONTROL/AMEND_LOG_R2.md`, `AMEND_LOG_R2.md`, or `AMEND_LOG_R2 R2-x`. Zero
  dangling references remain.

### Item 3 — HANDOFF carries no stale universal-NULL/stub headline: **PASS**

- HANDOFF.md fully read (150 lines). Live-hit probe result for ALL 9 probe strings
  ("NULL at all six sites", "NULL at ALL 6", "no class ever bound", "no object ever
  bound", "unexercised stub layer", "unbound/unexercised", "receiver = NULL",
  "ladder terminates at LEVEL 0", "814 THIS_ENTRY"): **ZERO hits in HANDOFF.md** ✓
  (HANDOFF's residue line reads "68 PARAM_CHAIN / 820 THIS_ENTRY … [C8] histogram sums
  to exactly 1,895" — the corrected values).
- HANDOFF carries the corrected headline (lines 25–90): holder binding REAL
  (HOLDER_BINDING_MECHANISM: REAL — live composite/channel-animation binding);
  per-class table; live .?AVArkAnimationFloatValue@@-hierarchy children
  (Scale/Rotation/Translation/Intensity/Color/Alpha) on the normal paths of the
  param-chained classes; failure paths NULL; SCENEFEEDER_LINK REJECTED AT THE
  RECEIVER-IDENTITY LINK (slot-3 dwords 0x006FFF00/0x009154A0 != 0x0050A050, measured);
  zero PROVEN slot-2 caller / no statically-identifiable caller; 1,433
  INSUFFICIENT_PROOF; ARG2_SEMANTIC_ROLE UNVERIFIED ✓.
- The probe strings appear elsewhere in the package ONLY as: quoted R1 history inside
  QC_AUDIT.md (the immutable R1 record), quoted retractions in REPORT.md line 94 /
  RECEIVER_IDENTITY.md line 73 (negation) / SCIENCE_STATUS_DELTA.csv rows 13/15, and
  quoted-retracted text inside AMEND_LOG_R2.md — all legitimate history/retraction
  citations, zero live stale claims.

### Item 4 — gates describe R2 science and QC chronology honestly: **PASS**

- STAGE_ACCEPTANCE_GATES.csv fully read (17 lines):
  - G5 PASS: "ctor writer sources climb L0->L1->L2->L3->L4-NEGATIVE per child chain …
    5-class NULL sources terminate at L0; dtor/deleting-dtor imm 0 (L0)" ✓.
  - G6 PASS: "strong-positive test A/B/C executed under the corrected values: A not
    met …; B EXECUTES AND REJECTS (RTTI-identified sources whose slot-3 != 0x0050A050);
    C not met … SCENEFEEDER_LINK REJECTED AT THE RECEIVER-IDENTITY LINK (the binding
    edge is real and live)" ✓.
  - G12 NOT_APPLICABLE: "receiver != SceneFeeder (the bounded receivers are the
    FloatValue-hierarchy children …); the NiNode slot-17 pin value revalidated in
    IDENTITY_VERIFICATION.txt [5] as a pins-table revalidation only (printed address
    0x00A8CD38)" ✓ (and IDENTITY_VERIFICATION.txt [5] prints exactly that:
    measured dword @0x00A8CD38 = 0x007B5390, MATCH=True).
  - G13 PENDING with the honest append-only chronology: "initial R1 fresh QC verdict
    QC_FAIL (06_REPORT/QC_AUDIT.md; one P0 load-bearing defect) -> CORRECTION_BATCH_R2
    (… R2-1..R2-3) -> PACKAGING_AND_PROVENANCE_CORRECTION (this batch; AMEND_LOG_R2.md
    entry R2-6) -> RE-QC: PENDING" ✓; G14_MASTER_ADJUDICATION PENDING ✓;
    G15_PERSISTENCE PENDING ✓.
- The initial QC_FAIL was NOT erased: `06_REPORT/QC_AUDIT.md` still exists unchanged
  (36,113 B; this session's measured SHA256
  `58793C7F89BA697756416BAD55DEA93A855D786EB2873F7000998EC81BA52114` — for PE-MASTER's
  comparison against the known R1-era value) and its full content is the R1 QC record:
  fresh-context G13 QC, verdict QC_FAIL, P0-1 with the byte counter-evidence table,
  P2-1/P2-2, P3-1..P3-8, §4 counterexample hunts, §5 independent re-derivations,
  §6 confirmed-correct list, §7 coverage/NOT_CHECKED, §8 adjudication inputs ✓.

### Item 5 — EVIDENCE_INDEX points to current evidence; C17 sample verified against [IV-8]: **PASS**

- EVIDENCE_INDEX.csv fully read (header + claims C1..C23):
  - C8 and C10 carry the PER-CLASS disposition (not universal NULL), both with the
    R1-universal-NULL recorded as the detected failure case and the 11/13 + 2-Alpha
    ret-this qualification ✓.
  - C12 carries the qualification: "no statically-identifiable caller of the thunk (4
    channels; qualified per QC P2-1) … 1438 dispatch candidates -> 0 proven / 5
    rejected / 1433 INSUFFICIENT_PROOF (unproven - not disproven)" ✓.
  - New rows C17–C23 present and bound to current evidence (live child allocation
    paths [IV-8]; RTTI names + vtable VAs [IV-8]/RECEIVER_IDENTITY.md; slot-3 dwords
    [IV-8][IV-9]; SceneFeeder negative identity test RECEIVER_IDENTITY.md G6 + [N1];
    corrected holder table [IV-9]; dispatcher reachability [MAP]; branch-aware slicing
    [IV-1..6] + EDGE-AWARENESS header) ✓.
- C17 measured quantities verified DIRECTLY (fully, not just a sample) against
  `01_RAW/HOLDER14_WRITER_RAW.txt` [IV-8] (lines 422–550):
  - 7 local ??2+push pairs, address- and size-exact vs C17:
    push 0xC @0x006D2042 (line 439), push 0x30 @0x006D21DC (449), push 0x7C @0x006D1EAF
    (462), push 0x24 @0x006D1F7C (468), push 0x1C @0x006D211C (474), push 0x48
    @0x006D233C (480), push 0x24 @0x006D1D2B (490) ✓ — 7/7 match.
  - 6 honest "no local ??2+push pair within the declared 32/16-byte windows (recorded
    honestly)" child paths (lines 500, 510, 520, 532, 538, 544) — all six at the
    CyclicSin factory sites, as C17 states ✓ — 6/6 match.
  - 7 + 6 = 13 child paths; the raw summary line (550) confirms "13
    xor/allocation-failure path(s) … and 13 child-construction path(s) across the 8
    factory call sites; NO path binds a SceneFeederObject" ✓.

### Item 6 — SCRIPT_SHA256.csv == disk: **PASS**

- Recomputed SHA256 + BYTES for all 10 scripts: 10/10 rows match disk exactly
  (SCRIPT_FAILURES=0; no missing, no extra — row count == script inventory count ==
  10; both SHA256 and BYTES columns verified) ✓.
- Raw-header GENERATOR cross-check: every raw that prints a GENERATOR SHA256 prints
  the CURRENT script hash (phase_a_thunk 39ED41ED…, phase_b_rtti D7AEE05A…,
  phase_c_anchor AA7B01D7…, phase_c_census FE3CFC48…, phase_d_callers 81D5E7E3…,
  phase_e_disposition 693F4DA4…, probe_identity 8CFD06E4…, negctl_receiver C30C8585…)
  — the generation-provenance chain from raws to the registry to disk is intact ✓.
- No `__pycache__` (see item 8).

### Item 7 — MANIFEST_SHA256.csv == disk: **PASS**

- Recomputed every row: MANIFEST_ROWS=41; missing=0; SHA mismatches=0; BYTES
  mismatches=0 ✓.
- Census accounting (measured denominators): package disk files = **43**; manifest rows
  = **41** = 43 − MANIFEST_SHA256.csv itself (L12 self-exclusion) − QC_AUDIT.md (R1
  convention). The disk-not-in-manifest set is EXACTLY {06_REPORT/MANIFEST_SHA256.csv,
  06_REPORT/QC_AUDIT.md} — both expected ✓. (This re-QC session adds QC_AUDIT_R2.md as
  a 44th disk file, intentionally NOT added to the manifest, per the mandate; the
  executor-generated manifest was already consistent for the 43-file state.)
- `00_CONTROL/AMEND_LOG_R2.md` IS in the manifest (row 3) ✓.
- MANIFEST_SHA256.csv's own on-disk hash (self-excluded by L12, recorded here for
  provenance): `C611AECFA5276520A3B16F523FDE0A882256B281E679C2316B16BE837C6351B4`
  (4,283 B).

### Item 8 — no __pycache__ / .pyc anywhere in the package: **PASS**

- Recursive scan: PYCACHE_DIRS=0; PYC_FILES=0 ✓.

### Item 9 — Alpha narrative scope is honest: **PASS**

All mandated locations verified to carry the 11/13 + 2-Alpha qualification:
- REPORT.md §1 (lines 59–70), §2 (115–117), §3 P0-1 (178–181), H3 row (line 31) ✓.
- RECEIVER_IDENTITY.md ladder table (line 25) ✓.
- HOLDER14_PROVENANCE.md [C(v)] (lines 216–219: "this-return shape measured for 5 of
  the 6 child ctors — the Alpha ctor's ret site is measured (0x006FD268) but its
  return-value shape is not derived in this package") ✓.
- SCIENCE_STATUS_DELTA.csv H3 row (line 16: "ret-this shape byte-proven on 11/13 (the
  2 Alpha paths: construction byte-proven - ctor ret site measured 0x006FD268 -
  return-value shape not derived in-package)") + HELD_OBJECT_IDENTITY row ✓.
- EVIDENCE_INDEX C8/C10 (both carry "ret-this shape byte-proven 11/13 - the 2 Alpha
  paths construction-proven with ctor return-value shape not derived in-package") ✓.
- HANDOFF.md (lines 45–53) ✓.
- Per-chain allocation honesty verified in the raw: the 0x006D213D Alpha chain carries
  the LOCAL ??2 pair (push 0x1C @0x006D211C -> ??2 @0x006D211E, lines 473–474); the
  0x006D17BF Alpha chain records "no local ??2+push pair … (recorded honestly)"
  (lines 509–510) ✓ — exactly the asymmetry the mandate requires to be disclosed.
- The raw is HONEST and unchanged: [IV-8] prints the Alpha child "ret @0x006FD268"
  (lines 477 and 513) WITHOUT the "(this-return shape)" annotation, while the other
  five child classes carry the annotation (11 annotated ret-shape lines: 442, 452,
  465, 471, 483, 493, 503, 523, 535, 541, 547) — 11/13 annotated, 2/13 not ✓.
- Raw byte-identity: HOLDER14_WRITER_RAW.txt SHA256 ==
  `50F3AD14C2045B272A95DB2AD2E2AE96D6559F713610700F6190FAFF9AB26CCD` ✓ (item 11 pin
  verification) — the Alpha ret lines are unchanged.

### Item 10 — capstone timing note downgraded, not a live magnitude claim: **PASS** (one P3 informational note, see FINDINGS)

- REPORT.md P2-2 (lines 231–240): "capstone 5.0.7 Cs.disasm() per-call setup makes
  per-function decode loops pathological; prefer streaming/batched decoding (the map
  pass = a single stream). The R1-era "~25–35 ms fixed per-call setup cost" magnitude
  is RETRACTED as unreproducible … Exact magnitudes are environment-dependent and NOT
  load-bearing; the operational lesson … stands on observed run behavior only." ✓
  (operational lesson + retraction carried).
- HANDOFF.md P2-2 (lines 123–130): same downgraded form — "magnitude is RETRACTED as
  unreproducible … operational lesson only, no magnitude; exact numbers are
  environment-dependent and NOT load-bearing" ✓.
- Occurrence census of the exact magnitude string across the package (measured):
  AMEND_LOG_R1.md A2 (line 21 — historical record, intentionally NOT edited per
  R2-6 (i)) ✓ permitted; s0_common.py docstrings (lines 301 and 371 — generation
  provenance, intentionally NOT edited per R2-6 (i), supersession recorded in the
  ledger) ✓ permitted; AMEND_LOG_R2.md line 410 (quoted-retracted) ✓ permitted;
  REPORT.md line 234 and HANDOFF.md line 126 (both quoted-retracted, inside the
  mandated P2-2 retraction statements themselves — see P3-1);
  QC_AUDIT.md: ZERO occurrences (the mandate's "QC_AUDIT history" slot is empty —
  "may remain" is permissive, nothing to preserve there).
- No live magnitude claim exists anywhere in the package: no current text asserts the
  25–35 ms figure as fact; every occurrence is historical or explicitly-retracted.

### Item 11 — science headline unchanged by the packaging batch: **PASS**

- ALL 16 files in 01_RAW/ pin-verified byte-identical (independent SHA256 recompute,
  RAW_PIN_FAILURES=0; 01_RAW disk count == 16 == exactly the pinned set):
  ARG2_VALUE_FLOW_RAW.txt 1CE0D33A… ✓; ARKANIMATION_VTABLE_MAP.csv 438DB8F3… ✓;
  AT_RUN_END_GIT_OBSERVATION.md E39CE917… ✓; AT_RUN_START_GIT_OBSERVATION.md
  A28A326C… ✓; B5_FUNCTION_MAP.csv CD436256… ✓; FUN_006FAB80_DISASM.txt 0F052BA9… ✓;
  HOLDER14_CENSUS_SUMMARY.txt 199413B8… ✓; HOLDER14_WRITER_CENSUS.csv DBD069EC… ✓;
  HOLDER14_WRITER_RAW.txt 50F3AD14… ✓; IDENTITY_VERIFICATION.txt EAE24400… ✓;
  IMM32_THUNK_CENSUS.txt CDA470B2… ✓; NEGCTL_RECEIVER_RAW.txt 859B5626… ✓;
  RTTI_COL_RAW.txt A8E8C1D3… ✓; THUNK_CALLER_CENSUS.csv 36FDB15A… ✓;
  THUNK_CALLER_CENSUS.txt FB497B04… ✓; VTABLE_INVENTORY.csv EFBA7978… ✓.
- The six load-bearing science numbers still stand in the package documents AND were
  independently re-derived by this session from the packaged raw data (recompute, not
  re-read of prose):
  1. Census 10,711 rows (1,898 REG_INDIRECT / 8,811 STACK / 2 SIB / 0 ABSOLUTE / 0
     UNKNOWN) — own full recount of HOLDER14_WRITER_CENSUS.csv: 10,711 rows;
     REG_INDIRECT=1898, STACK_FRAME=8811, SIB=2, no ABSOLUTE rows, no UNKNOWN rows
     (EXCLUDED_FORM=8813 = 8811+2; FAMILY_CONTEXT_PROVEN=3; NON_FAMILY=1895;
     duplicate ROW_VA groups=0) ✓; same numbers in REPORT §2, HANDOFF,
     CENSUS_SUMMARY [C5], EVIDENCE_INDEX C7 ✓.
  2. 3 family writers — own recount: FAMILY_CONTEXT_PROVEN=3 (0x006FABB5
     mov [eax+0x14],ecx; 0x006FAC25 mov [esi+0x14],0; 0x006FAC75 mov [esi+0x14],0) ✓.
  3. Dispatch candidates 1,438 → 0 PROVEN / 5 REJECTED / 1,433 INSUFFICIENT_PROOF —
     own full recount of THUNK_CALLER_CENSUS.csv: 1,438 rows; INSUFFICIENT_PROOF=1433,
     REJECTED_TARGET_NOT_FAMILY=5 (MaPanelText/Line/Rect/Map + ArkVegetationObservable),
     no PROVEN rows ✓; raw [D4] and E8/E9/EB denominators 156,829/40,668/17,961 → 0 ✓.
  4. Five-class membership: 5 vtables, slot ordinal 2 in ALL five — RTTI_COL_RAW [B2]
     (5 COL-backed vtables 0x00A864C0/0x00A86550/0x00A86574/0x00A865A0/0x00A86650, each
     "thunk slot ordinal=2"), IMM32_THUNK_CENSUS (5 hits, all ordinal 2),
     THUNK_CALLER_CENSUS [D2]/[D3], ARKANIMATION_VTABLE_MAP.csv
     (thunk_slot_ordinal=2 in all 5 rows) ✓.
  5. [C8] histogram sums to 1,895 — own arithmetic on the printed breakdown
     (THIS_ENTRY=820 + BOUND_EXHAUSTED=487 + LEA_ADDR=244 + OTHER_WRITE=224 +
     PARAM_CHAIN=68 + NO_RET=20 + ZERO=21 + ALIAS_RISK_NOTE=5 + IMMEDIATE=2 +
     PARTIAL_NOTE=2 + CALLEE_UNDECODEABLE=1 + X87_STORE=1) = **1,895** == the
     NON_FAMILY count ("True" in the raw) ✓; REPORT/HANDOFF quote 820 THIS_ENTRY and
     the 1,895 sum ✓ (the stale "814" exists only in the immutable R1 QC history).
  6. Child slot-3 dwords 0x006FFF00 (Scale/Rotation/Translation) and 0x009154A0
     (Intensity/Color/Alpha) != 0x0050A050 — raw [IV-8] per-path lines (443, 453, 466,
     472, 478, 484, 494, 504, 514, 524, 536, 542, 548) + [IV-9] slot-3 negative-control
     table (lines 582–588, with SF 0x00A7D458 slot-3 = 0x0050A050 re-confirmed as the
     only 1/803) + RECEIVER_IDENTITY.md table ✓.
- Headline stability: the R2 science result as stated in the mandate context
  (composite/channel-animation binding REAL; live FloatValue-hierarchy children on
  normal paths; failure paths NULL; SceneFeeder rejected at the receiver-identity
  link; zero PROVEN slot-2 caller; 1,433 INSUFFICIENT_PROOF; ARG2 UNVERIFIED) is
  carried CONSISTENTLY by REPORT/HANDOFF/SCIENCE_STATUS_DELTA/EVIDENCE_INDEX — the
  packaging batch did not disturb it.

### Item 12 — no proprietary payload entered the package: **PASS**

- Payload-extension scan (.nif/.bnt/.ark/.bvi/.dds/.tga/.obj/.vfs/.dat): **0 hits** ✓.
- Files > 2 MB: exactly 1 — `01_RAW/B5_FUNCTION_MAP.csv` (2,982,144 B), the documented
  package file ✓.
- Known-file sizes verified exact: HOLDER14_WRITER_CENSUS.csv 1,574,138 B ✓;
  HOLDER14_WRITER_RAW.txt 83,245 B ✓; VTABLE_INVENTORY.csv 149,654 B ✓;
  THUNK_CALLER_CENSUS.csv 116,355 B ✓; B5_FUNCTION_MAP.csv 2,982,144 B ✓.
- The only non-package input reference is the pinned EXE identity record
  (SOURCE_IDENTITIES.json: path/size/SHA256/machine/PE-magic/imagebase/sections —
  metadata only; no payload) ✓. No payload bytes anywhere in the package.

## FINDINGS

**P3-1 (informational; non-blocking) — the exact "~25–35 ms" magnitude string appears as quoted-retracted text in REPORT.md P2-2 (line 234) and HANDOFF.md P2-2 (line 126).**
- Exact locations: 06_REPORT/REPORT.md line 234; 06_REPORT/HANDOFF.md line 126.
- Context: both occurrences are inside the retraction sentence itself ("The R1-era
  "~25–35 ms fixed per-call setup cost" magnitude is RETRACTED as unreproducible …").
- Contradicted claim: none — the mandate's item-10 "ONLY" enumeration (historical
  records + quoted-retracted text inside AMEND_LOG_R2.md) did not explicitly list
  REPORT/HANDOFF as permitted locations for the exact string.
- Disposition and justification: NON-BLOCKING. The mandate simultaneously requires
  "REPORT P2-2 and HANDOFF P2-2 must carry the operational lesson with the retraction"
  — a retraction must name the magnitude it retracts; both spots carry the explicit
  RETRACTED-as-unreproducible framing, the operational lesson, and the
  "environment-dependent and NOT load-bearing" qualifier. There is NO live magnitude
  claim anywhere in the package (verified by occurrence census, item 10). The purpose
  of item 10 (downgrade, not a live magnitude claim) is fully met. Note for
  completeness: QC_AUDIT.md contains zero occurrences of the magnitude (the mandate's
  "QC_AUDIT history" slot is empty — permitted, since "may remain" is permissive).
- Correction (optional, at PE-MASTER's discretion at G15 persistence): none required;
  if a stricter literal reading is desired, the two quoted strings could be reworded
  to "the R1-era fixed-per-call magnitude" at the next authorized text touch — NOT
  performed by this re-QC (this session may only create this file).

**P3-2 (informational; non-blocking) — AMEND_LOG_R2.md R2-6 (a) says "across 10 files" but enumerates 9 files.**
- Exact location: 00_CONTROL/AMEND_LOG_R2.md line 302 ("The 51 dangling AMEND_LOG_R2
  text-line references across 10 files (REPORT.md 8, HOLDER14_WRITER_RAW.txt 17,
  HOLDER14_PROVENANCE.md 4, RECEIVER_IDENTITY.md 2, ARG2_UPSTREAM_ANALYSIS.md 2,
  SCIENCE_STATUS_DELTA.csv 3, FORWARDER_ANALYSIS.md 1, phase_c_anchor.py 6,
  s0_common.py 8)").
- Measured: the enumeration lists 9 files whose counts sum to exactly 51 (8+17+4+2+2+
  3+1+6+8 = 51 ✓); this session's current-state grep finds the 51 pre-existing
  references in exactly those 9 files (plus 19 packaging-batch-added references in 6
  other places, incl. the ledger's own 5 self-citations; total 70).
- Contradicted claim: none load-bearing — the reference-line sum (51) and the
  all-resolve property are correct and verified; only the file-count word is off by
  one.
- Disposition and justification: NON-BLOCKING (cosmetic ledger-prose slip; no gate, no
  science claim, no registry row depends on it).
- Correction (optional, at the next authorized AMEND_LOG_R2 touch or as an erratum
  note at persistence): change "across 10 files" to "across 9 files" — NOT performed
  by this re-QC (this session may only create this file).

No P0, P1 or P2 findings. No load-bearing package/provenance defect.

## DENOMINATORS SUMMARY (measured)

- Package disk files: 43 (before this QC file; 44 after — my QC_AUDIT_R2.md).
- 01_RAW files: 16 (== the pinned set; 16/16 pins match).
- Scripts: 10 (registry 10/10 match; zero __pycache__/.pyc).
- MANIFEST_SHA256.csv rows: 41 (== 43 − self − QC_AUDIT.md); missing=0, mismatch=0.
- AMEND_LOG_R2 reference lines: 70 (51 original, all resolving + 19 packaging-added).
- Census CSV rows: 10,711 (1,898/8,811/2/0/0; 3 family / 1,895 non-family / 0 unknown).
- Thunk-caller CSV rows: 1,438 (0/5/1,433).
- [IV-8]: 13 xor-paths + 13 child-paths over 8 factory sites (7 local ??2 pairs + 6
  no-local-pair); 11/13 ret-this annotated, 2/13 Alpha without annotation.
- [C8] histogram: 12 leaf kinds summing to 1,895.
- Payload-extension hits: 0; >2MB files: 1 (documented B5 map).
- Git: HEAD == origin/master == ls-remote == 895bbc8…; untracked set == expected 3
  entries; zero mutations.

## COVERAGE / FULL_READ_LOG (this session read to EOF, independently)

- 00_CONTROL: AMEND_LOG_R1.md, AMEND_LOG_R2.md, RUN_CONTRACT.md, SCRIPT_SHA256.csv,
  SOURCE_IDENTITIES.json (5/5).
- 01_RAW (12/16 fully read): ARG2_VALUE_FLOW_RAW.txt, ARKANIMATION_VTABLE_MAP.csv,
  AT_RUN_END_GIT_OBSERVATION.md, AT_RUN_START_GIT_OBSERVATION.md,
  FUN_006FAB80_DISASM.txt, HOLDER14_CENSUS_SUMMARY.txt, HOLDER14_WRITER_RAW.txt
  (all 928 lines), IDENTITY_VERIFICATION.txt, IMM32_THUNK_CENSUS.txt,
  NEGCTL_RECEIVER_RAW.txt, RTTI_COL_RAW.txt, THUNK_CALLER_CENSUS.txt.
  The remaining 4 (HOLDER14_WRITER_CENSUS.csv, THUNK_CALLER_CENSUS.csv — full-row
  parsed and recounted by script, stronger than reading; B5_FUNCTION_MAP.csv,
  VTABLE_INVENTORY.csv — hash-pinned lookup indexes) — see NOT_CHECKED.
- 02_ANALYSIS: all 5 files (ARG2_UPSTREAM_ANALYSIS.md, FORWARDER_ANALYSIS.md,
  HOLDER14_PROVENANCE.md, RECEIVER_IDENTITY.md, SCIENCE_STATUS_DELTA.csv).
- 03_EVIDENCE: README.md, EVIDENCE_INDEX.csv (2/2).
- 06_REPORT: HANDOFF.md, MANIFEST_SHA256.csv, QC_AUDIT.md (all 415 lines),
  REPORT.md (all 355 lines), STAGE_ACCEPTANCE_GATES.csv (5/5).
- 00_CONTROL/scripts: s0_common.py docstring regions relevant to item 10 (lines
  28–45, 290–319, 360–384 read); all 10 scripts hash-verified against the registry and
  the raw GENERATOR headers.

## NOT_CHECKED (explicit; none load-bearing for this bounded re-QC)

- Full script-code re-derivation of the 10 generators (tool-logic audit): OUT OF SCOPE
  for this bounded PACKAGE/PROVENANCE re-QC — the mandate declares the R2 science
  standing (externally work-audited + PE-MASTER byte spot-checks; the R1 QC performed
  the original tool-logic audit). Scripts verified at the registry/hash/raw-header
  level only (which is what items 6/1 require).
- B5_FUNCTION_MAP.csv (2,982,144 B) and VTABLE_INVENTORY.csv (149,654 B) row contents:
  hash-pinned (byte-identical per item 11) lookup indexes; no re-QC claim depends on
  re-walking them.
- No generator was re-executed and no binary was opened/executed (STATIC-ONLY re-QC;
  recomputations were performed by this session's own scripts over the PACKAGED raw
  data).
- The 614 out-of-cluster rep-movs destination-provenance tracing: declared NOT_CHECKED
  by the package itself (R2-6 / [VIII]) — standing declaration, unchanged.
- The 1,433 INSUFFICIENT_PROOF dispatch candidates beyond the R1 QC's samples:
  standing science (census numbers re-verified in aggregate by full recount).

## VERDICT INPUTS FOR PE-MASTER (G14) — compact

- All 12 mandate items: PASS (measured numbers above).
- Findings: P3-1, P3-2 (both informational, non-blocking, with justifications and
  optional corrections that this session was NOT authorized to perform).
- QC_VERDICT: **QC_PASS_WITH_FINDINGS** — the PACKAGING_AND_PROVENANCE_CORRECTION
  batch (AMEND_LOG_R2.md R2-6) is verified as correctly and completely applied; the
  raw science evidence is byte-identical to the pre-correction state; the six
  load-bearing science numbers stand; the R1 QC_FAIL history is preserved; the
  package is internally consistent (registries == disk, references resolve,
  denominators exact). G13 re-QC (this verdict) → ready for PE-MASTER adjudication
  (G14) and persistence (G15, owned by pe-master-auditor).
- Zero git mutations by this session; the only file created inside the package is this
  QC_AUDIT_R2.md (not added to the manifest, per the mandate and the QC-file
  convention).
