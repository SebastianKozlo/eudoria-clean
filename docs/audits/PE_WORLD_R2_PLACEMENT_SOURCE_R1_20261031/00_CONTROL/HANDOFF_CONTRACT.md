# HANDOFF_CONTRACT — PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031

Target executor: pe-reconstruction (STATIC DATA RE ONLY).
Written by: pe-master-auditor, mode FORMALIZE, under PE-MASTER loop 75db9418-2d3e-4e05-9799-eeb4c3f63955.
Contract version: 1.0 (2026-10-31). This file is the single authority for this run.

---

## 1. Run identity

```text
RUN_ID:            PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031
PARENT_LOOP_ID:    75db9418-2d3e-4e05-9799-eeb4c3f63955
MILESTONE:         pe-world-continuous-r2 (world building placement — declared project priority)
ERA:               PCG_9_3_5
CANONICAL DATA:    D:\Eudoria_Reconstruction\pcg_install\  (read-only)
WORKTREE:          D:\Eudoria_Reconstruction\12_WebGame\pe-world-continuous-r2
BRANCH:            codex/pe-world-continuous-r2-20261010
RUN_CLASS:         MATERIAL (data-source investigation; NO production changes)
BASE_SHA (full):   dc6f1961125596dba9f3156371fb427a90881436
                   (verified by `git rev-parse HEAD` at contract time; worktree clean,
                    `git status --porcelain` empty)
AUDIT_OUTPUT_ROOT: docs/audits/PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031/  (this run, fresh+empty at dispatch)
CHILD DEADLINE:    one bounded batch, 25–30 min of work. If it does not fit, return the
                   completed stages and a RESUME_POINT; do NOT overrun.
```

STARTUP OBLIGATION (executor, before any analysis): re-run `git rev-parse HEAD` and
`git status --porcelain`; record the full SHA and any dirty paths in the run report as
BASE_SHA_AT_EXECUTION and DIRTY_PATH_INVENTORY. If HEAD differs from BASE_SHA above,
STOP and return a CORRECTION_REQUEST to PE-MASTER (base moved between formalize and dispatch).

## 2. Primary question (verbatim)

> "Czy rekordy placementu obiektów świata (identyfikator modelu + pozycja [+ orientacja/skala])
> są odzyskiwalne z istniejących danych PCG_9_3_5 — w pierwszej kolejności z Volumes.bnt /
> wpisów .bvi — na poziomie dowodu dual-independent decode, i jaką mają strukturę?"

Scope: STATIC DATA RE ONLY. The classification of the space in which any decoded values
live (world-space / local / packed) is PART OF THE RESULT, never an assumption (V2-009).

## 3. Boundaries — FORBIDDEN vs ALLOWED

FORBIDDEN in this run (any of these = RUN invalid, return immediately):
- ANY modification of `compat/` or `src/` (production code paths).
- Running the original PCG client, frida injection, debuggers on the client, any runtime
  instrumentation of original binaries. This run is purely static.
- Starting new servers or touching standing servers (8140/8161/8162/9163/9350 and the
  127.0.0.1:8163 world server — do not restart or modify them).
- Editing, moving or deleting ANY file inside existing audit packages
  (docs/audits/PE_935_* and PE_WORLD_* are READ_ONLY).
- Any `git commit`, `git push`, `git add`, staging changes. Persistence is a separate
  stage performed after MASTER_AUDIT by a separately dispatched worker.
- Publishing proprietary payloads (original .bnt/.bvi/.nif bytes) anywhere outside the
  local run directory; evidence extracts must stay small and local-only.

ALLOWED:
- Creating and writing files ONLY under `docs/audits/PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031/`
  (subdirs: `00_CONTROL/`, `01_RAW/`, `02_ANALYSIS/`, `03_EVIDENCE/`, `04_REPORT/`,
  `tools/` for run-local scripts).
- Reading everything in the worktree, pcg_install, and the listed prior-canon packages.
- Run-local tools (node/python) that operate read-only on pcg_install data and write
  only inside this run directory.

## 4. Verified input pins (measured by pe-master-auditor at formalize time)

```text
Volumes.bnt:  D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt
              size   = 3,746,375 B
              SHA256 = 6AD8BA3C5AD6F7534F91C1956A0E36485A49BBEF3FFA918CBDDC0C68EDBABC09
Models.bnt:   D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt
              size   = 395,412,868 B
              SHA256 = C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0
```

**DISPUTED PIN — 900 vs 1865 .bvi entries (recorded honestly, fail-closed handling):**
The parent handoff stated "900 wpisów .bvi wg Z2_VOLUMES_BNT_INDEX_NAMES.csv".
Recount of that CSV at formalize time yields **1865 data rows, all with names ending
`.bvi`** (columns: entry_index|name|packed_size|offset; e.g. row 0: `506044.bvi`,
packed_size 148, offset 0). The figure "900" does NOT match the referenced file.
The executor must NOT hard-stop on either number blindly. Instead (Gate G2):
measure the entry census DIRECTLY from the Volumes.bnt index with the executor's own
parser, then reconcile three numbers: (a) direct index parse count, (b) Z2 CSV row
count recounted by the executor, (c) distinct .bvi name count. All three must agree.
Record the 900-vs-1865 discrepancy and its resolution in the report. HARD STOP applies
only if (a), (b), (c) disagree with EACH OTHER, or if the Volumes.bnt SHA256 above
does not match, or Volumes.bnt is missing.

Other standing facts (premises; executor re-verifies before use, fail-closed):
- Models.bnt: 5596 indexed NIF entries (4838 x NIF-10.1, 757 x 4.1.0.12, 1 x 4.0.0.2)
  per PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20260909.
- Terrain 50.bnt: 51,920 tiles, grid 220x236, TILE_WORLD=128, u16/128 heightScale
  (skill ground truth).

## 5. READ-FIRST prior canon (READ_ONLY; extract BEFORE any new decoding)

Paths verified to exist at formalize time (worktree-relative), with SHA256 of the
primary report file:

```text
P1 docs/audits/PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913/
   primary: 06_REPORT/REPORT.md
   SHA256 = 6BC4DCED40BCD36937C01029AB0D0059FCE219E5D3A6858CE1E2625001384A20
P2 docs/audits/PE_935_STATIC_PLACEMENT_DESKTOP_AUDIT_R1_20260913/
   primary: REPORT.md
   SHA256 = 9014F963470FFA34E233C63AE326FF78158C00990C3634B3E98CE787FB266547
P3 docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/
   primary: 06_REPORT/FINAL_REPORT.md
   SHA256 = EDC245EFE76CB774FA2F65863AF9E14531BCBC9AFAB9EA8B84EB251764E048B0
P4 docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004/
   primary: FINAL_REPORT.md
   SHA256 = 5C946B94F00EE867A2AB4EE1E5141CD0CF80813342597F5126DFF5FB14C6BA9B
P5 docs/audits/PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913/
   primary: 06_REPORT/00_FINAL_REPORT.md
   SHA256 = 6D6B9C8D1C9EE3BECCB5BCE16A594284058511A85EB549611ACE28D9594E123E
   key raw: 01_RAW/Z2_VOLUMES_BNT_INDEX_NAMES.csv
   SHA256 = 556259003E203351B148F02F089BFABC327A5762ECA4F40B616FA61323FDCD7E
   (this CSV contains BVI<->NIF joins; also Z2_JOIN_RESULT.json,
    Z2_JOIN_A_TO_NIF_DETAIL.csv, Z2_JOIN_B_TO_BVI_DETAIL.csv)
```

Executor must re-hash the primary files at start (fail-closed on mismatch; a mismatch
means the package changed post-formalize — STOP and return CORRECTION_REQUEST).

PRIOR-CANON RULE: if prior canon already RESOLVED or REJECTED a placement hypothesis
(including any verdict about .bvi being or not being placement data), the executor
must DOCUMENT that verdict with its evidence file path and NOT re-derive it. Only
genuinely new questions (e.g., payload-level dual decode with a second independent
implementation, if prior canon only did single-parser inspection) are open. Any
re-derivation of an already-resolved point is a report defect.

## 6. Standing canon — QUOTED VERBATIM, UNTOUCHED by this run

These canonical statuses must appear verbatim in the run report and MUST NOT be
promoted, demoted or reworded by this run's results without a separate MASTER review:

```text
HISTORICAL_BUILDING_PLACEMENT   = NOT_ESTABLISHED
MODEL_218757_TO_WORLD_INSTANCE   = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED              = NO
HISTORICAL_WORLD_INSTANCE        = NOT_ESTABLISHED
PE_AXES_AND_UNITS                = UNVERIFIED
```

This run may PROPOSE supersessions with evidence, but the proposal is advisory; the
canonical values remain as above until PE-MASTER accepts a supersession. Gates must NOT
assume .bvi payload values are world-space positions — space classification is an
output, not a premise (V2-009).

## 7. Stages (execute in order; each produces files under the run dir)

### Stage A — PRIOR_CANON_EXTRACTION
Read P1–P5 (primary reports + placement-related evidence files cited in them).
Produce `02_ANALYSIS/PRIOR_CANON_PLACEMENT_VERDICTS.md`: for EVERY placement-related
verdict — the verdict text, the package, the exact evidence file path it rests on, and
a status (STANDING / SUPERSEDED / DISPUTED). Extract from FILES, not memory. If any
prior package already resolves the primary question or rejects the .bvi hypothesis,
HARD STOP with class PRIOR_CANON_ALREADY_RESOLVED (document what is resolved, with paths).

### Stage B — VOLUME_PIN
Re-hash Volumes.bnt (path/size/SHA256 per section 4) and run the executor's own index
parser over it. Census per Gate G2 (including the 900-vs-1865 reconciliation).
Produce `01_RAW/VOLUME_PIN.json`.

### Stage C — SAMPLE_DUAL_DECODE
Decode >= 3 diverse .bvi payloads (choose diversity: different sizes, different name
patterns, at least one small ~148 B and one much larger). EACH payload decoded by TWO
implementations with DIFFERENT lineage (e.g., executor's own parser + Kaitai/pe-binary-
structures C6-hexpat style spec). Shared field-maps between the two implementations
= SHARED_ASSUMPTION_ORACLE and do NOT count as semantic independence (QH-009): the
second implementation must be written from the bytes (or from a spec derived
independently), not from the first implementation's field table. Produce per-sample
byte dumps and both decoders' field outputs in `01_RAW/`, tools pinned in `tools/`
with SHA256 recorded before execution.

### Stage D — STRUCTURE
Declare the .bvi payload structure explicitly: offsets, widths, endianness, and for
every field a semantics label tagged OBSERVED (byte-level evidence, e.g. "u32 LE at +4
equals Models.bnt index 218757 for sample X, joined by exact match") or HYPOTHESIS
(e.g. "three f32 LE could be a translation"). Untested hypotheses stay HYPOTHESIS.
Produce `02_ANALYSIS/BVI_STRUCTURE.md`.

### Stage E — PLACEMENT CLASSIFICATION (OPEN taxonomy, V2-010)
Assign the .bvi corpus (or the sampled subset, denominators explicit) exactly one class:

```text
PLACEMENT_RECORDS_YES_FULL      (model id + position [+ orient/scale] present, dual-decoded)
PLACEMENT_RECORDS_YES_PARTIAL   (subset of fields; which fields missing, per-record denominators)
NOT_PLACEMENT_DATA              (payloads serve another purpose — what purpose, evidenced)
INCONCLUSIVE                    (evidence does not discriminate; say exactly what is missing)
OTHER                           (fits none; define what it is)
```

MANDATORY: a table ALTERNATIVE_HYPOTHESES with, for each load-bearing interpretation,
at least one material alternative (alignment artifact; adjacent/nested structure
misread as fields; indirect reference; padding coincidence) and its resolution BY
EVIDENCE (a discriminating measurement), not by prose. If an alternative cannot be
excluded, the class cannot be *_YES_* for that aspect. Produce
`02_ANALYSIS/PLACEMENT_CLASSIFICATION.md`.

### Stage F — MODEL JOIN PROBE
For every decoded model-id-like field: join against the Models.bnt index (P5's
Z2_MODELS_BNT_INDEX_NAMES.csv may be used as a cross-check but the executor must join
against their own parsed index as primary). Report counts joined / not-joined /
ambiguous + the exact join criterion (field width, endianness, match key). "First
matching value" is NOT a join criterion; ambiguous matches must be counted as
ambiguous. Produce `02_ANALYSIS/MODEL_JOIN.md`.

## 8. Gates (exact boolean predicates)

```text
G1 PRIOR_CANON_RECONCILED:
   (P1..P5 primary reports all re-hashed and match section 5)
 AND (every placement-related verdict in P1..P5 extracted with its evidence file path
      from the file content, recorded in PRIOR_CANON_PLACEMENT_VERDICTS.md)
 AND (no verdict sourced from memory/summary alone)

G2 VOLUME_PIN_VERIFIED:
   (Volumes.bnt exists at the pinned path)
 AND (SHA256 == 6AD8BA3C5AD6F7534F91C1956A0E36485A49BBEF3FFA918CBDDC0C68EDBABC09)
 AND (direct index parse count == executor recount of Z2 CSV == distinct .bvi name count)
 AND (the 900-vs-1865 discrepancy explicitly documented with resolution)
   — any pairwise disagreement of the three counts = PIN_FAILURE hard stop.

G3 DUAL_DECODE_AGREEMENT:
   (>= 3 diverse .bvi payloads decoded by both implementations)
 AND (field-by-field agreement table produced; every field either agrees in both or
      the divergence is recorded)
 AND NEGATIVE CONTROLS EXECUTED (not merely declared — L19): each of
      (a) wrong-endian variant, (b) truncated payload, (c) wrong-width read
      MUST demonstrably FAIL BOTH decoders (record the actual failure output).
 AND (the two implementations do not share a field-map; lineage of the second
      implementation documented — else G3 = NOT_PERFORMED, SHARED_ASSUMPTION_ORACLE)

G4 PLACEMENT_CLASS_ASSIGNED:
   (exactly one class from the taxonomy assigned)
 AND (ALTERNATIVE_HYPOTHESES table present; every alternative either resolved by a
      discriminating measurement or the claim is downgraded accordingly)
 AND (no gate or classification text assumes .bvi values are world-space — space
      classification, if claimed, has its own OBSERVED evidence chain)

G5 MODEL_JOIN_MEASURED:
   (join counts joined / not-joined / ambiguous reported with an exact join criterion)
 AND (denominators explicit: total decoded id-like fields, how many tested)
 AND (ambiguous matches counted as ambiguous, not resolved by first-match)
```

Non-pass classes: `NOT_PERFORMED / DECODE_DIVERGENCE / PIN_FAILURE /
PRIOR_CANON_ALREADY_RESOLVED`. Hard STOP triggers: prior canon already resolves the
primary question; census three-way mismatch (G2); SHA mismatch on Volumes.bnt or on
any read-first primary report; Volumes.bnt missing. A hard stop is a VALID result —
document it and return; do not improvise around it.

## 9. Intervention ledger

This run is PURELY STATIC: no runtime processes of the original client, no frida, no
hooks, no patches, no environment overrides, no server changes. The executor's report
must contain an intervention ledger section stating `INTERVENTIONS: NONE (static data
analysis only)` or enumerating any deviation with the L1 record fields. Any accidental
deviation must be disclosed, not silently absorbed.

## 10. Required output package (under docs/audits/PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031/)

```text
00_CONTROL/HANDOFF_CONTRACT.md     (this file, read-only for the executor)
00_CONTROL/PRE_DISPATCH_QC.md      (formalizer's QC — read-only for the executor)
04_REPORT/REPORT.md                (final report; 20-point human-first format)
04_REPORT/HANDOFF.md               (handoff block below, mandatory)
STAGE_ACCEPTANCE_GATES.csv         (G1..G5 rows: gate, predicate, result, evidence path)
artifact_index.csv                 (every artifact: path, SHA256, generator path+SHA,
                                    executed command, counts, limitations)
tools/                             (run-local scripts, each with recorded SHA256
                                    pinned BEFORE execution)
```

MANDATORY HANDOFF BLOCK in the executor's final answer (exact fields):

```text
AUDIT_OUTPUT_ROOT / FINAL_REPORT_PATH / PRIMARY_EVIDENCE_PATHS /
RUN_STATUS / HARD_STOP_REASON
```

plus: BASE_SHA_AT_EXECUTION, HEAD unchanged (no commits), GATE results G1–G5,
NOT_CHECKED list, and any CORRECTION_REQUEST for PE-MASTER.

## 11. NO_NESTED_TASKS

The executor does NOT spawn agents, does NOT dispatch sub-runs, does NOT act as a
loop controller. The result returns to PE-MASTER (parent loop 75db9418-2d3e-4e05-9799-
eeb4c3f63955) via the Task return only. A missing Task tool in the child session is
expected.

## 12. Honesty rules (binding)

- Evidence vocabulary only: CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED /
  REJECTED; keep claim status, gate result and canonical supersession separate.
- Coverage algebra: never write "fully audited/complete" without a denominator
  (TOTAL = used + inventoried_only + excluded + missing).
- MISSING_PHYSICAL_INPUT stays visible; absence of evidence is not negative evidence.
- One sample does not prove a family; classify per-sample and per-corpus separately.
- FLOAT-LOOKING VALUES ARE NOT WORLD COORDINATES without consumer/frame evidence
  (PE_AXES_AND_UNITS = UNVERIFIED stands).
- Function/field identity: OBSERVED means byte-level evidence; everything inferred
  stays HYPOTHESIS.
