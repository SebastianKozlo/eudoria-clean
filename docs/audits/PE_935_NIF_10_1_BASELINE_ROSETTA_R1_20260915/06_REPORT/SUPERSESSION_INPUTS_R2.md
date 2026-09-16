# SUPERSESSION_INPUTS_R2 — C14 factual inputs for PE-MASTER

RUN: PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916 (2026-09-16).
Executor-prepared FACTUAL answers to the 8 supersession questions
(contract C14). These are INPUTS + proposed statuses + the
discriminator used — the FINAL adjudicated statuses and the
PE_MASTER_REVIEW_SUPERSESSION_R2.md verdict document belong to
PE-MASTER (advisory). Proposed statuses are marked PROPOSED.

## 1. CORE_SCIENCE_CHANGED — PROPOSED: NO

Discriminator: does any frozen MEASUREMENT (census counts, closure
counts, holdout results, layout-variant decisions, ArkTexture
re-derivations) change under the corrected instrument?
Answer: NO. The C6 world-slice regression (s18, executed over all
2,363 slice files) shows 2,363/2,363 identical outcomes between the
frozen decoder re-executed now (which reproduces the frozen TRAIN
1,876/1,890 + HOLDOUT 467/473 = 2,343 closures + the same 20 blocked
files bit-exactly) and FIELD_IDENTITY_V2: 0 changed boundaries, 0
changed field interpretations, 0 newly closing, 0 newly failing
(01_RAW/WORLD_SLICE_FIELDIDENTITY_REGRESSION.csv;
02_ANALYSIS/FIELD_IDENTITY_V2_BLAST_RADIUS.md). Census/closure
denominators unchanged (C5 recomputed 45 blocks/5 files = prior
expectation).
What DID change is INTERPRETIVE (witness retraction, see #3) — not a
core measurement.

## 2. GROUPID_FRAMING_CHANGED — PROPOSED: NO

Discriminator: engine source + physical slot evidence for the
per-block GroupID u32 (5.0.0.6 <= v < 10.1.0.114).
Evidence stands: engine NiObject.cpp L134-143 (re-read this run);
s15 physically read the GroupID slot at every BABYLENGUIN block
boundary 0-7 (all 0); s19 confirmed EE2 lodtest.nif CLOSURE_OK under
BOTH decoders (framing identical); all PE-corpus blocks continue to
read GroupID==0 across 2,343 closures + 45 NiSourceTexture blocks
under V2. The framing verdicts A (Gamebryo), B (Entropia), C (EE2
demonstration) are CONFIRMED and unchanged.

## 3. BABYLENGUIN_XPU_CHANGED — PROPOSED: YES

Discriminator: independent byte reproduction from the physical file.
The external counterexample REPRODUCED: 479309 (0x0007504D) = bytes
@1498-1501 = NiSourceTexture File Name tail 'M','P' (end of
'LEN-SKIN_02.BMP') + low 2 bytes of the Pixel Data link (7 -> NiPixel
Data block). NOT a GroupID. Real block 7 (NiPixelData) GroupID = 0
@1517. The OLD-model mechanism was reproduced exactly (old model
ends block 6 at 1498 and reads 479309 as "block 7 GroupID") — executed
as the s16 negative-control pair. Evidence:
02_ANALYSIS/BABYLENGUIN_GROUPID_ADJUDICATION.md; 01_RAW/
BABYLENGUIN_BOUNDARY_REDERIVATION.csv; 01_RAW/
FIELD_IDENTITY_V2_NEGATIVE_CONTROL.csv.

## 4. TOOLING_DEFECT_CONFIRMED — PROPOSED: YES

Discriminator: code-level inspection + executed reproduction +
census.
- Code level (my own reading): s06 _fields_for L106-115 dedups by bare
  field NAME across the inheritance chain.
- Schema census (s13): 148 duplicate-name groups / 302 occurrences /
  58 types; 21 LOAD-BEARING at 10.1.0.0; 4 load-bearing types
  physically observed in PCG (NiSourceTexture, NiPSysData,
  NiMeshPSysData, NiTriShapeData); TexSource compound orphan.
- Executed repro (s16): old model loses File Name[UE==0] -> block 6
  end 1498 -> false 479309; V2 keeps both occurrences -> 1517/0.
General lesson PROPOSED (C11, pending PE-MASTER adjudication):
FIELD_NAME_IS_NOT_FIELD_IDENTITY / NEVER_DEDUP_SCHEMA_FIELDS_BY_
DISPLAY_NAME — "In schema-driven forensic decoding, duplicate field
labels must remain distinct when their owner, occurrence, condition,
version gate, template or schema position differ. Deduplication by
display name alone is prohibited for load-bearing parsing."

## 5. NISOURCETEXTURE_REGRESSION — PROPOSED: PASS (45/45)

Discriminator: full physical denominator + per-block structural
verification under V2 (contract C5 R1/R2/R3).
- R3 denominator recomputed independently: 45 blocks / 5 files
  (matches prior expectation; s17 independent BNT2 walk + header scan
  over all 4,838 v10.1 payloads).
- R1 (Use External != 0): 44 blocks, external File Name path consumed,
  link=-1, next-block GroupID==0 verified — PASS.
- R2 (Use External == 0): 1 block (204828.nif blk159), internal File
  Name path consumed ('NPC_Animals_scaboreas_01_01.tga'), Pixel Data
  link=160 -> NiPixelData, next-block GroupID==0 — PASS.
- Total 45 PASS / 0 FAIL / 0 AMBIGUOUS. No hidden failures; the 3/5
  files whose FULL closure still fails are blocked by unsupported
  controller/PSys types OUTSIDE NiSourceTexture (recorded per row;
  unchanged limitation, disclosed in the CSV closure_status column).
Evidence: 01_RAW/NISOURCETEXTURE_FIELDIDENTITY_REGRESSION.csv.

## 6. FUTURE_NISOURCETEXTURE_BLOCKER_CLEARED — PROPOSED: YES

Discriminator: can future NiSourceTexture validation proceed safely
with corrected instrumentation?
YES — with the field-identity fix (s14/s13 model), both
NiSourceTexture branches decode correctly on every physically
existing PCG block (C5 45/45), the BABYLENGUIN class of false
boundary is eliminated (s16), and the G6 deferral basis (NiSourceTexture
census-level-only) is now lifted to structural-level for all 45
blocks. Remaining non-NiSourceTexture blockers (controller/keyframe/
PSys-family types) are unchanged and out of this correction's scope.
No regression to prior validated types (C6: zero deltas).

## 7. WORLD_SLICE_REGRESSION_COMPLETE — PROPOSED: YES

Discriminator: contract C11 algebra over the full slice.
2,363/2,363 executed in one deterministic pass (single chunk, sorted
order, no timeouts): PASS 2,343 + FAIL 20 + AMBIGUOUS 0 +
INFRA_UNRESOLVED 0 = 2,363 (closes exactly). The 20 FAIL are the SAME
20 blocked files as the frozen run (12 ArkBlockError search-exhausted
+ 8 struct.error EOF — the disclosed frozen-decoder search limits,
not new failures; not counted as NIF science failures and not
infra). Evidence: 01_RAW/WORLD_SLICE_FIELDIDENTITY_REGRESSION.csv
(2,363 rows).

## 8. LIVE_DOC_APPLICATION_READY — PROPOSED: YES (docs unchanged by this run; REPORT-ONLY)

Discriminator: are the live-docs application decisions (KEEP/CLARIFY/
SUPERSEDE/REVALIDATE/NO_CHANGE) still valid after the correction?
The recomputed LIVE_DOC tally (E2, from the packaged matrix) is
KEEP 5 / CLARIFY 6 / SUPERSEDE 4 / REVALIDATE 1 / NO_CHANGE 1 = 17 —
identical to the REPORT/HANDOFF post-correction tally. The BABYLENGUIN
retraction touches docs/nif content ONLY via the [XPU] GroupID
realism line that lived in the RUN's reports (live docs were never
edited by the original run and are NOT edited here — REPORT-ONLY
policy). The GroupID CLARIFY entries (docs/nif/01 preamble == GroupID)
rest on engine + physical evidence — unchanged by the witness
retraction. Live docs remain READY for application by the
docs-owning process; no LIVE_DOC row changes as a result of this
correction (the PE_MASTER_REVIEW.md's stale pre-AMEND-009 tally line
is inside PE-MASTER's own verdict document — flagged for PE-MASTER,
not editable here).

## REVALIDATOR INPUTS (C13 — for the fresh pe-master-auditor context)

All 17 C13 items map to the following executable inputs:
1-3 (BABYLENGUIN boundary / block7 GroupID / 479309 ownership):
   re-run `python 00_CONTROL/scripts/s15_babylenguin_boundary_walker.py`
   (asserts block6 end=1517, block7 GroupID=0@1517, needle@1498;
   negative controls must all fail) +
   `python 00_CONTROL/scripts/s16_field_identity_mechanism_repro.py`
   (OLD=1498/479309 REPRODUCED; V2=1517/0 PASS).
4 (Bump conditional): s15 console/CSV rows block5.slot[5].HasMap=0 ->
   no BumpMap fields read; block5 end=1464.
5-6 (census + corrected implementation):
   `python 00_CONTROL/scripts/s13_schema_field_identity_v2.py`
   (census CSV + summary JSON; NiSourceTexture File Name group
   load-bearing, occurrence 1 LOST by old model) and code-level
   check of s14 _fields_for (no dedup).
7-8 (denominator + 45 blocks):
   `python 00_CONTROL/scripts/s17_nisourcetexture_fieldidentity_regression.py`
   (45/45 PASS; 44 external + 1 internal; denominator recomputed).
9-10 (world-slice accounting + infra separation):
   `python 00_CONTROL/scripts/s18_world_slice_fieldidentity_regression.py --chunk 0 --nchunks 1`
   (then the packaged 01_RAW/WORLD_SLICE_FIELDIDENTITY_REGRESSION.csv;
   algebra PASS+FAIL+AMBIG+INFRA = 2363, INFRA_UNRESOLVED = 0).
11 (LIVE_DOC tally): recount actions in 02_ANALYSIS/
   LIVE_DOC_IMPACT_MATRIX.csv (5/6/4/1/1 = 17).
12 (s11/s12 SHA): Get-FileHash on 00_CONTROL/scripts/s11*/s12*.
13 (QC P3 tally): QC_AUDIT.md enumeration vs header (F-QC-8/F-QC-9
   = 2 OPEN P3).
14 (NiflySharp path): Test-Path ousnius-NiflySharp-104d79f\NiflySharp\
   BaseTypes\NiObject.cs + L61-62 quote.
15 (WORK-AUDIT denominator):
   01_RAW/WORKAUDIT_DENOMINATOR_RECOMPUTE.csv (36 = 31+4+1).
16 (5 nif.xml pins): 01_RAW/NIFXML_SOURCE_REHASH.csv (5/5 MATCH).
17 (final provenance): 06_REPORT/MANIFEST_SHA256.csv after the
   AMEND-018 regeneration (0 stale / 0 missing / L12 self-exclusion /
   0 .pyc / 0 __pycache__).
