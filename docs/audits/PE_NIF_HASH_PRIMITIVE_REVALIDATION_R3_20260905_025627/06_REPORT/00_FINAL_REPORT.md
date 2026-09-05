# Final Report — PE-NIF-HASH-PRIMITIVE-REVALIDATION-R3

Run: PE-NIF-HASH-PRIMITIVE_REVALIDATION_R3_20260905_025627 (2026-09-05)
Executor: pe-reconstruction. Chartered by the external post-audit
PE_NIF_R2_POST_AUDIT_20260905_025627 (verdict REVALIDATION_REQUIRED; full text +
hashes persisted in 00_CONTROL/EXTERNAL_REVIEW.md) via
00_CONTROL/OPENCODE_REVALIDATION_PROMPT.md (SHA256 662d4c52..., gate R3G1).
P0 = HASH_PRIMITIVE_VALUE_IDENTITY_BEFORE_AGGREGATE_ACCEPTANCE.

Result: **23/23 executable gates PASS; 4 human-review gates PENDING
(three-state preserved); RUN_STATUS = COMPLETED (correction package + safe
publication).** OVERALL EXECUTABLE PASS IS NOT HUMAN ACCEPTANCE. All R2 and
historical artifacts are byte-unchanged; every physical result the external
audit accepted is retained; only unsupported method assurances are superseded.

## 1. Defect reproduction from actual bytes (prompt items 1-2; R3C-01/02)

The five literal pure helper declarations (crc32 + CRC_T table + adler32 +
fnv1a) were extracted from the HASH-PINNED R2 source (control_r2.cjs, SHA256
666c378d..., pin verified by gate R3G3a) and executed as pure functions in a
Node vm context (00_CONTROL/probe_r2_helpers.cjs; the historical R2 script
itself was NOT executed). The prompt's counterexamples were TESTED, not
assumed — all ten values reproduced exactly:

| Input / function | R2 Node (executed literal) | Correct reference | 
|---|---|---|
| "" / Adler-32 | **00010000** | 00000001 |
| "a" / Adler-32 | **00620061** | 00620062 |
| "hello" / Adler-32 | **06280214** | 062c0215 |
| "hello" / FNV-1a-32 | **a82fb4a1** | 4f9f2cab |
| "548296.nif" / FNV-1a-32 | **200d96de** | 4e2b6736 |

Root causes (R3C-02, source inspection + exact-int characterization): the R2
adler32 misassigns the RFC 1950 roles/initials (byte-sum accumulator starts at
0, accumulated-sum at 1; the standard requires s1=1, s2=0); the R2 fnv1a
multiplies in float64 before `>>>0` (products above 2^53 round before the
32-bit reduction — the exact-int Python transcription of the SAME formula
produces the CORRECT values, isolating the defect to the arithmetic).

Corrected stage-local primitives (00_CONTROL/r3_primitives.py): Adler-32 per
RFC 1950 (s1=1, s2=0, mod 65521, result (s2<<16)|s1) and FNV-1a-32 per RFC 9923
(exact multiply mod 2^32 — Python exact-int + Node BigInt legs). No shared
tool, no R2 file, no historical script was edited.

## 2. Known-answer tests BEFORE aggregation (item 3; R3G4/R3G5)

Executable KAT suite (00_CONTROL/run_kats.py, subprocess exit codes recorded):
14 vectors — empty, single byte (0x00/0xFF/'a'), multi-byte ASCII, binary
sweep with zero/high bytes (bytes 0..255), overflow-sensitive (0xFF×4096;
0x00×4096 pure multiply-chain), repeated and incremental inputs — plus
streaming carry-in identity for adler/fnv/crc and ORACLE SELF-VALIDATION
against published constants (zlib.adler32("Wikipedia")=0x11E60398,
zlib.crc32("123456789")=0xCBF43926, FNV vectors 0x811C9DC5/0xE40C292C/
0xBF9CF968/0x4F9F2CAB). Corrected set: **exit 0**. The corpus aggregation
phase is structurally unreachable unless this phase passes (driver abort).

## 3. Per-entry VALUE comparison across both corpora (item 4; R3G9/R3G10)

Keyed by era + file + candidate input identity (join verified 11,022/11,022 on
size/off/c/d, gate R3G9join; per-entry payload SHA256 recorded in the
local-only full census):

- **Identity pass (before any aggregate)**: corrected Python == zlib == corrected
  Node for adler32(name) and adler32(payload) on every entry (11,022/11,022
  each; plus a numpy closed-form leg and an iterative-spec sample of 6,335
  entries / 247.0 MB); fnv1a(name) exact-int == Node BigInt 11,022/11,022;
  all five crc32 input classes 11,022/11,022 (R2-literal == zlib == own table).
- **R2-vs-corrected complete mismatch census** (01_RAW/PRIMITIVE_VALUE_COMPARISON.json):
  adler32(name) **11,022/11,022** mismatches; adler32(payload) **11,022/11,022**
  (the first complete per-payload census — the external audit explicitly did
  not claim one); fnv1a(name) **11,016/11,022** with exactly 6 coincidences
  identified (508629.nif, 186733.nif, 147508.nif — same names in both eras;
  float64 products stay exact when (x XOR b) ≡ 0 mod 4); all crc32 candidates
  0 mismatches (R3C-03: the R2 crc32 literal is NOT defective — defect census
  bounded to adler32 + fnv1a).
- Match-count tables were derived ONLY AFTER the identity pass. No original
  payload bytes are published anywhere (values and SHA256 metadata only).

## 4. Negative controls (item 5; R3G6a/R3G7a/R3G7b/R3G8a/R3G8b)

All controls captured ACTUAL exit codes and failed predicates — no hand-written
FAIL labels:

| Control | Actual outcome |
|---|---|
| unchanged R2 helper semantics (exact-int transcription) | KAT exit **1**; failed predicates adler_impl!=zlib, adler!=published on every vector |
| executed R2 literals (Node) | the 5 counterexamples above (R3G6b); R2 crc32 clean (R3G6c) |
| deliberately wrong-value primitives (adler XOR 0x5A5A5A5A; fnv basis 0x811C9DC6) | KAT exit **1** — AND the full-corpus census with them still yields **0 d-matches on all three wrong candidates in both eras** (aggregate zero-match PRESERVED) |
| R2 bool(ok) coercion | three-state predicate exit **1**; failed predicate "serialize(None) == 'PENDING'" with actual 'FAIL' |
| corrected three-state serializer | same predicates exit **0** (PASS/PENDING/FAIL distinct) |

The wrong-value control pair (fails KATs, preserves aggregates) is the P0
demonstration: **aggregate-only acceptance provably cannot detect value
errors; value-identity gates are required before aggregate acceptance.**

## 5. Recount with corrected primitives (item 6; R3G11; R3C-07/R3C-08)

The corrected ten-candidate census reproduces the physical result UNCHANGED:
nine exact-zero candidates on both corpora; d==crc32(payload)=3,435/5,596
(61.42%) and 3,299/5,426 (60.80%); c==CRC32(payload)=11,022/11,022 with 0
directory mismatches; **20/20 agreement** with the R2 aggregates AND the R36
historical FIELD_D_TESTS.json. The independent Python (zlib/exact-int) had
already confirmed the aggregate; the R2 Node leg was computing different
functions whose zero-match aggregates coincidentally agreed.

SUPERSEDED (05_ANALYSIS/SUPERSESSION_MAP.csv S-03..S-08, quotes verified
present in the pinned R2 artifacts): R2G8's "Python == Node == R36" /
"three independent computations"; the R2 report's "Node hand-rolled
CRC32/adler32/FNV-1a cross-checked against Python zlib"; C2-B-01 method
provenance; C2-E-02 gate-detection assurance (the R2 suite did NOT detect the
R2 helper value defects — no value-identity gate existed; R3 adds gates that
do); the R2 handoff wording. Historical evidence is not erased: R2 files are
byte-unchanged, and the physical counts remain CONFIRMED.

## 6. The two bounded non-research inconsistencies (item 7; R3G12/R3G13/R3G15/R3G16)

**F2 — morph residual (R3C-10, historical re-sum of the hash-pinned R34
per_span records):** 334 is the VARIABLE-K residual among the 2,427
classifier-real spans (2,093 fit = 86.2%); of those 334, **62 have another
recorded fit** (g1_ok/g2_ok/mscan_ok_m) and **272 have none among the recorded
alternatives**; all-span fit 3,186/6,167 preserved. Concrete counterexamples:
592572.nif (bi=65, si=45, mscan_ok_m=[30]); 579739.nif (bi=109, si=138,
mscan_ok_m=[4]); 574751.nif (bi=80, si=4, g2_ok=1, mscan_ok_m=[11]).
Alternative fits are NOT promoted to true segmentation. Corrected wording:
P1R2-5-R3 (proposals only).

**F2b — 21-claim summary (R3C-11, verbatim transcription of the R35 table):**
19 ERA-STABLE + 2 EVOLVED (C-G3B-3, C-SHAD-2); C-MORPH-1 is a PARTIAL-FIT
claim (rr 2,093/2,427 = 86.2% on 9.3.5; 1,180/1,457 = 81.0% on 2003).
"Every byte-exact grammar reproduced at 100%" is valid only for the byte-exact
validator populations; all 21 claims are NOT 100% fits. Corrected wording:
P2R2-2-R3 (proposals only).

**F3 — three-state + tally (R3C-12/R3C-13):** PENDING is preserved distinctly
from FAIL and PASS through the R3 gate function, TEST_RESULTS.json (HR gates
carry pass=null, state=PENDING), STAGE_ACCEPTANCE_GATES.csv and this report;
the R2 bool(None)→false/FAIL serialization is reproduced and detected
(negative control exit 1). The actual R2 CLAIM_MATRIX tally is **16 CONFIRMED /
8 REJECTED** (recounted from the emitted rows); the R2G13 gate label
"{CONFIRMED 17, REJECTED 7}" is stale — R3 gate labels derive from actual rows
at emit time (CONFIRMED 14 / REJECTED-as-worded 1 for this run's 15 claims).
OVERALL EXECUTABLE PASS never means human acceptance (explicit field).

## 7. Sidecars: 12/12 preserved + explicit bare-CR policy (item 8; R3G14; R3C-14)

The accepted 12/12 byte-lossless sidecars are PRESERVED: full-file byte
reconstruction re-verified 12/12 SHA-equal; a NEW field-level comparison under
the EXPLICIT custom physical-line contract (bare CR inside a row = data; the
R2 builder csvParse semantics) yields **0 mapping errors across all strict
rows** — including R39 row 10, where computed_by="n/a\r" matches the sidecar
mapping exactly. Under standard CSV record semantics the same row parses as
"n/a" — recorded as an INTERPRETIVE difference, NOT raw-byte loss; both layers
preserve the original bytes. No manifest migration is requested or authorized.
(01_RAW/SIDECAR_BARE_CR_ANALYSIS.json.)

## 8. Method separation and evidence discipline (item 9)

Every gate record carries method_class ∈ {PHYSICAL_RECOMPUTATION,
STAGE_LOCAL_REPRODUCTION, SOURCE_INSPECTION (via quote verification),
HISTORICAL_RESUM, HISTORICAL_TRANSCRIPTION} plus
MEASURED_QUANTITY/DENOMINATOR/INDEPENDENT_SOURCE_OF_TRUTH/
WHY_NON_CIRCULAR/FAILURE_CASE_DETECTED. Source-inspection (R2 helper bytes, R2
gate serialization), physical recomputation (identity pass, census recount,
sidecar reconstruction), and historical re-sums (R34 per_span, R35 table, R2
tally) are kept separate throughout. All 12 supersession quotes were verified
present in their pinned R2 artifacts at emit time (exit-enforced).

## 9. Scope compliance (R3C-15)

Writes were confined to this run directory and the single authorized
publication path. R2 and all historical runs are byte-unchanged (hash pins
re-verified before use). No game/Ghidra execution (04_RUNTIME/NOT_RUN.md), no
wiki application, no canonical/vault update, no milestone promotion, no
morph-boundary research, no nested agents. The unrelated untracked
docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/ (another writer) was not
touched or staged.

## 10. Publication

This package is published (byte-identical, explicit-path staging only) at
docs/audits/PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627/ in
SebastianKozlo/eudoria-clean (master). BASE_SHA (run start) =
f37ba25468a39d9c89c7b01e106fab3215db7e4c; the publication HEAD_SHA is reported
in the final handoff (a commit cannot embed its own hash). NO original payload
is published: the original corpora are represented by era/build + local path +
size + SHA256 + reproduction method (below). The local-only full per-entry
census (01_RAW/PRIMITIVE_VALUE_CENSUS_FULL.json, SHA256 recorded in the
manifest) is excluded from the published package.

LOCAL_ONLY_ORIGINAL_SOURCES (identity metadata only):
- PCG 9.3.5 (Entropia Universe 9.3.5) Models.bnt (BNT2, 5,596 NIF entries) —
  D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt — 395,412,868 B —
  SHA256 c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0
- 2003 installer era Models.bnt (5,426 entries) —
  D:\Eudoria_Reconstruction\01_Original_Files\BNT_Models\Models.bnt —
  375,322,581 B — SHA256 1322adf2919b1b24a8b4fda9618347e00c5a2b35dbb54516e353f1cefd3524a6
- Reproduction method: direct BNT2 index parse (bounds-checked, index
  consumption exact), payloads read in-place (read-only), hashed with the
  corrected primitives per 00_CONTROL/revalidate_r3.py + probe_r2_helpers.cjs.

## 11. Open / unresolved (honest limits)

- The 4 R3 human-review gates are PENDING (external acceptance is a human act).
- All R3 corrections to documentation remain PROPOSALS (P1R2-5-R3, P2R2-2-R3,
  P3R3, P4R3, P5R3) — nothing has been applied to docs/nif or the wiki.
- The FNV float64 coincidence mechanism (mod-4 divisibility of x^b) is a
  measured characterization, not a formal proof.
- The 6 FNV coincidence inputs are corpus facts; no claim is made about inputs
  outside the two corpora.
- Per the external audit: R2's 18 historical executable PASS results were
  inspected, not rerun in place; R3 re-verified every load-bearing number by
  fresh physical recomputation instead.

HARD STOP after this corrected published package and handoff. Wait for
independent revalidation before proposals are applied. No next milestone, no
unbounded loop.
