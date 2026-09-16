# REPORT_CORRECTION_R1 — PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916

Bounded WORKAUDIT_CORRECTION_REVALIDATION of
`PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915` (correction stays inside
the existing package; NO EU935-M2). Executor: pe-reconstruction under
PE-MASTER governance; RUN_CLASS MATERIAL (declared by PE-MASTER).
Executor performed ZERO git operations; persistence is deferred to
pe-master-auditor after PE-MASTER adjudication.

## C0 — Repin (PASS)

- BASE_SHA verified: HEAD == origin/master == ls-remote ==
  `91e2af0249f4242cf41eb1f96bc8a1a7f3e63839`; working tree = exactly
  the 2 pre-existing untracked roots
  (`docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`,
  `experiments/`) — untouched, never staged.
- Models.bnt: 395,412,868 B; SHA256 C950A8C26F2063F4DD748D88C95BD769AA
  C77A2F5F76FACE7E969BE0B3D3BEE0 (own rehash — pin match).
- BABYLENGUIN.NIF: 1,737,966 B; SHA256 A86C49384E62DF41339101B62E48BE6
  DCAE10E06B5F7CAC39DC627CF89635EA9 (full own measurement).
- nif.xml hash closure (C10): 5/5 pins rehashed, 5/5 MATCH —
  MOD D6B76A83EA5FBADD21DA5F06348B236A1C43DA6BB76D108A2E8B749C22618DD6
  (565,041 B); HIST 1D5C8E580B95D3EB8E1EEF06E1A12A8F2C06BF441FE97E333
  2080A5099D9FAF5 (401,093 B); NifSkope 0DCE5092060E0CABB95B8C07AF1BC
  59049C685D8D6E681771C816988505DDED3 (466,952 B); fo76utils 880C31
  6787950299A29291FEB609593949E726AC13E581ED36C6636A157E7003
  (667,577 B); NiflySharp-bundled 752C79786CEB217641FD7E94BE4033898C97
  E9AA38025BF05F2CBEE9CFFBBF0D (570,454 B — at the REAL physical path
  `ousnius-NiflySharp-104d79f\nifxml\nif.xml`; the earlier-documented
  `...\NiflySharp\nif.xml` does not exist — SRC-04 erratum recorded,
  SOURCE_REGISTRY annotated).

## C1/C1A — BABYLENGUIN byte reproduction (counterexample REPRODUCED)

Fresh engine-transcribed byte walker (s15; no s04/s06, no external
offsets; 3 executed negative controls — truncation / corrupted string
length / wrong version — all fail as designed):

- Block 5 NiTexturingProperty 1408-1464; TextureCount=7; slot[5]
  (BUMP) HasMap=0 -> BumpMap extras NOT read (VALUE condition honored;
  no false boundary).
- Block 6 NiSourceTexture 1464-1517: GroupID=0; Name=""; UseExternal=**0**
  (internal pixel data); File Name='LEN-SKIN_02.BMP' (15 B @1485);
  Pixel Data link=7 -> block 7 NiPixelData; IsStatic=1.
- **Block 7 (NiPixelData) GroupID = 0 @1517** (the REAL boundary).
- 479309 (0x0007504D) occurs exactly once in the file — at 1498: bytes
  4D 50 07 00 = filename tail 'M','P' + low 2 bytes of the pixel-data
  link 07 00. **NOT a GroupID.**
- OLD-model mechanism reproduced exactly (s16 executed negative
  control): dedup lost `File Name[Use External == 0]` -> old block 6
  end=1498 -> "block 7 GroupID"=479309@1498. Comparator (post-freeze):
  my derivation matches the external prompt-audit's sequence on ALL
  points (1464/1464/1517/1517/1498/IsStatic=1) with ZERO discrepancy.

**OLD_XPU_CLAIM_STATUS = REJECTED.** Evidence:
01_RAW/BABYLENGUIN_BOUNDARY_REDERIVATION.csv;
01_RAW/FIELD_IDENTITY_V2_NEGATIVE_CONTROL.csv;
02_ANALYSIS/BABYLENGUIN_GROUPID_ADJUDICATION.md.

## C2/C4 — Field-identity defect (CONFIRMED; fix = FIELD_IDENTITY_V2)

- s06 `_fields_for` L106-115 dedups by bare FIELD_NAME —
  FIELD_NAME was treated as FIELD_IDENTITY. Two conditional
  `File Name` alternatives in NiSourceTexture collapse; the
  `Use External == 0` variant is LOST.
- Census (s13): 148 duplicate-name groups / 302 occurrences / 58
  effective types; 21 LOAD-BEARING at 10.1.0.0; observed in PCG:
  NiSourceTexture, NiPSysData, NiMeshPSysData, NiTriShapeData
  (in-slice byte-neutral for NiTriShapeData; PSys latent, non-slice);
  TexSource compound pair is an orphan (zero reach).
- Fix (s14): occurrence-preserving identity
  (owner_type + field_name + occurrence_index + field_type + ver1 +
  ver2 + vercond + cond + template + schema_order); s14 subclasses the
  frozen s06 with ONLY `_fields_for` changed. s01-s12 byte-unchanged;
  hypothesis sha 6DB2F1E3...93752 NOT rewritten.
- Evidence: 01_RAW/DUPLICATE_FIELD_IDENTITY_CENSUS.csv.

## C5 — NiSourceTexture regression: **PASS 45/45**

- Denominator recomputed independently (BNT2 walk + header/type-table
  scan over ALL 4,838 v10.1 payloads): **45 blocks / 5 files** —
  matches the prior expectation.
- R1 (Use External != 0): 44 blocks — external File Name path consumed,
  link=-1, next-block GroupID==0 verified — PASS.
- R2 (Use External == 0): 1 block (204828.nif blk159: FN=
  'NPC_Animals_scaboreas_01_01.tga', link=160 -> NiPixelData, next
  gid=0) — PASS. (This is the single PCG block the OLD model would
  have mis-consumed.)
- R3: TOTAL 45 / PASS 45 / FAIL 0 / AMBIGUOUS 0. No hidden failures;
  3/5 files' full-file closure still fails on unsupported controller/
  PSys types OUTSIDE NiSourceTexture (per-row closure_status, unchanged
  limitation). Evidence:
  01_RAW/NISOURCETEXTURE_FIELDIDENTITY_REGRESSION.csv.

## C6 — World-slice regression: 2,363/2,363 accounted; ZERO deltas

- Executed in one deterministic pass (single chunk; 0 infra stops; no
  infrastructure timeout classified as parser failure):
  **PASS 2,343 + FAIL 20 + AMBIGUOUS 0 + INFRA_UNRESOLVED 0 = 2,363**
  (algebra closes).
- The frozen decoder re-executed now REPRODUCES the frozen results
  bit-exactly (2,343 closures; the same 20 blocked: 12 ArkBlockError
  search-exhausted + 8 struct.error EOF).
- V2 identical on all 2,363: files_same_closure=2,363;
  newly_closing=0; newly_failing=0; ambiguous=0;
  **changed_boundaries=0; changed_field_interpretations=0** (per-block
  boundary arrays + canonical value fingerprints compared per file).
- In-slice frozen measurements remain VALID; closure difference != 
  science correction — there IS no closure difference.
- Evidence: 01_RAW/WORLD_SLICE_FIELDIDENTITY_REGRESSION.csv (2,363
  rows); 02_ANALYSIS/FIELD_IDENTITY_V2_BLAST_RADIUS.md.

## C7 — GroupID re-adjudication

- A Gamebryo GroupID framing exists: CONFIRMED (engine NiObject.cpp
  L134-143; physically read at every BABYLENGUIN block boundary).
- B Entropia GroupID framing exists: CONFIRMED (unchanged; all PE
  blocks GroupID==0 across 2,343 closures + 45 ST blocks).
- C EE2 demonstrates standard 10.1 framing: CONFIRMED (lodtest.nif
  CLOSURE_OK under BOTH decoders; no NiSourceTexture in the file).
- D BABYLENGUIN has non-zero GroupID=479309: **REJECTED** (false read;
  real block 7 GroupID = 0 @1517).
- Loss of D does NOT downgrade A/B/C. Evidence:
  01_RAW/CROSS_PUBLISHER_RETEST_FIELDIDENTITY.csv.

## C8 — External WORK-AUDIT denominator (re-verified)

Physical recount of 01_TWIERDZENIA.md: **TOTAL 36 = CONFIRMED 31 +
REJECTED 4 (rows 25/29/32/33) + UNCHECKED 1 (row 35 — nif.xml hashes,
NOW CLOSED by C10) + PARTIAL 0 + OTHER 0**; algebra closes; matches
the second external audit's corrected tally (36 = 31 + 4 + 1).
Evidence: 01_RAW/WORKAUDIT_DENOMINATOR_RECOMPUTE.csv.

## C9/C10 — Errata applied (append-only; AMEND-016/017)

- **E1**: BABYLENGUIN XPU witness RETRACTED — F-18 appended (F-17
  pointer); REPORT headline 4 rewritten with mechanism + evidence;
  FIELD_VALIDATION_RAW cross-publisher row corrected; HANDOFF
  retractions list extended.
- **E2**: LIVE_DOC tally re-verified from the matrix: KEEP 5 / CLARIFY
  6 / SUPERSEDE 4 / REVALIDATE 1 / NO_CHANGE 1 = 17 (REPORT/HANDOFF
  already correct — no edit needed; PE_MASTER_REVIEW.md's stale
  pre-AMEND-009 tally line is PE-MASTER's document — flagged, not
  edited).
- **E3**: s11/s12 SHA re-attribution — s11 = 6A8FD958E4EBA4A20BEE34
  BA4F531C4862B90E89B9339B25C3BD5A0396B8E0DB (5,477 B); s12 =
  CEC66531E3670872F51DF44F22724A468F59A7C097212BD560B37E08A0753AAC
  (26,530 B); AMEND-009's text swap disclosed (F-20(a)); SCRIPT_SHA256
  always correct.
- **E4**: QC P3 open count reconciled — only F-QC-8/F-QC-9 OPEN (=2);
  QC header corrected; HANDOFF "7xP3" -> "6xP3 (4 fixed + 2 open)".
- **E5**: NiflySharp NiObject.cs real path pinned
  (`ousnius-NiflySharp-104d79f\NiflySharp\BaseTypes\NiObject.cs`,
  L61-62 quote byte-verified); path citations corrected/annotated in
  QC_AUDIT/BASELINE_SPEC/REPORT/SOURCE_REGISTRY; F-16 text preserved.
- **C10**: 01_RAW/NIFXML_SOURCE_REHASH.csv — 5/5 MATCH (see C0).

## C11 — Proposed standing lesson (PENDING PE-MASTER adjudication)

FIELD_NAME_IS_NOT_FIELD_IDENTITY / NEVER_DEDUP_SCHEMA_FIELDS_BY_
DISPLAY_NAME: "In schema-driven forensic decoding, duplicate field
labels must remain distinct when their owner, occurrence, condition,
version gate, template or schema position differ. Deduplication by
display name alone is prohibited for load-bearing parsing."

## C12 — Gates

Historical supersession states + revalidation evidence rows recorded
append-only in STAGE_ACCEPTANCE_GATES.csv:
G16_OLD = SUPERSEDED_BY_EXTERNAL_COUNTEREXAMPLE; G17_OLD = SUPERSEDED;
G18_OLD = PERSISTENCE_FACT_RETAINED; G16R/G17R/G18R =
PENDING_PE_MASTER_ADJUDICATION (evidence recorded; final R-verdicts
are PE-MASTER's per governance addendum C).

## C13/C14 — Revalidation + supersession inputs prepared

SUPERSESSION_INPUTS_R2.md (06_REPORT/) carries the 8 factual answers
with evidence pointers + proposed statuses + discriminators
(CORE_SCIENCE_CHANGED=NO / GROUPID_FRAMING_CHANGED=NO /
BABYLENGUIN_XPU_CHANGED=YES / TOOLING_DEFECT_CONFIRMED=YES /
NISOURCETEXTURE_REGRESSION=PASS / FUTURE_NISOURCETEXTURE_BLOCKER_
CLEARED=YES / WORLD_SLICE_REGRESSION_COMPLETE=YES /
LIVE_DOC_APPLICATION_READY=YES — all PROPOSED, PE-MASTER adjudicates)
plus the full 17-item revalidator command map. The fresh
pe-master-auditor revalidation context executes AFTER this return
(addendum C); ENTRYPOINT_ROW_R2.md holds the prepared append-only
entrypoint row for the persistence worker.

## Provenance

AMEND-016 (science correction), AMEND-017 (errata), AMEND-018 (final
provenance regeneration) in 00_CONTROL/AMEND_LOG_R1.md; PRE_EDIT
snapshots under 00_CONTROL/PRE_EDIT/*.AMEND-016.pre; provenance
regenerated by s10 in the canonical §21 order (SCRIPT_SHA256.csv —
19 scripts s01-s19 — -> 03_EVIDENCE/README.md -> EVIDENCE_INDEX.csv ->
MANIFEST_SHA256.csv; L12 self-exclusion; 0 stale / 0 missing / 0 .pyc
/ 0 __pycache__).
