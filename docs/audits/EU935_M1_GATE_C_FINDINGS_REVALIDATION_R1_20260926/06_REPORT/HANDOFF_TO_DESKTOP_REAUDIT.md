# HANDOFF TO DESKTOP REAUDIT — EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926

For: the SECOND independent ChatGPT Desktop Gate-C deep post-audit (relayed by
the human). Expected verdict vocabulary: MILESTONE_POST_AUDIT_PASS / _PARTIAL /
_REJECTED per POM §13 Gate C.

## WHAT TO AUDIT (the falsifiable core of this correction run)

This package is the bounded successor to your GATEC_REPORT_20260926 (verdict
MILESTONE_POST_AUDIT_REJECTED, findings GC-F01..GC-F06). Every load-bearing
number below was re-derived from physical sources by NEW probes written for
this run (not by re-running yours), then cross-compared with your outputs:

1. F01 — your zero-primary counterexample: reproduced. Our probe reads the
   constants from the LOCAL installed SDK
   (`C:\Program Files (x86)\Windows Kits\10\Include\10.0.22621.0\um\wingdi.h`;
   PRIMARY_DEVICE=0x4, MULTI_DRIVER=0x2) and recomputes all 6 adapters from the
   raw StateFlags: DISPLAY1 0x04000005 = ATTACHED+PRIMARY+REMOTE -> 1/6
   primaries, NOT zero. Mask controls 0/1/2/4/5/0x04000005 executed
   (03_EVIDENCE/F01_PRIMARY_DEVICE_REVALIDATION.json). The dependent records
   (M1-CL-20 / X87_RUNTIME_AUDIT / CLOSURE_GATE_MATRIX-Gate-A / entrypoint
   blocker cell / your N-3, N-13 final states) are re-classified per finding
   §5.1; the x87 cause class is corrected ENVIRONMENT_BLOCKED -> UNKNOWN with
   A. CW UNMEASURED / B. exit -1 CONFIRMED (re-derived from the trace: 1 PID,
   2,193 rows, 1 Process Exit -1, 0 ddraw/d3d8/d3d9 loads) / C. observed facts
   kept / D. cause UNKNOWN / E. AV/EAX supersession preserved. NOTE the trace
   total-row delta is ROOT-CAUSED (AMEND_R1,
   03_EVIDENCE/F01_TRACE_LINECOUNT_ERRATUM.json): your quoted 282,059 data
   rows = CORRECT (the LF convention: 282,060 LF bytes = header + 282,059
   data rows; confirmed by a quote-aware RFC4180 parse of the same bytes, 0
   malformed); our successor probe's 282,192 = a CR-splitting line-count
   artifact (133 lone CR bytes embedded inside quoted Detail fields were each
   counted as an extra line boundary: 282,060 LF + 133 = 282,193 reader lines
   -> 282,192 "data rows"); the per-client load-bearing facts (1 PID / 2,193
   Entropia.exe rows / exactly one "Exit Status: -1" / 0 ddraw-d3d8-d3d9
   loads) are UNAFFECTED (all re-verified under the CR-correct parse).
2. F02 — your VCL counterexample: reproduced to the byte. 32 / 492 lines /
   5,916 tokens = 493 groups; 25.vcl group 9 = six comma tokens (first "0,2"
   @payload byte 447); the current decoder = 31/32 files / 472 records /
   25.vcl THROWS; the historical float()-skip demonstrated by re-running a
   byte-identical copy of m1_iter032k_vcl_columns.py (only the OUT line
   patched; the historical output file verified untouched). V4 row 7's old
   MATCH is now recorded CONTRADICTION_FOUND (not preserved for cosmetic
   continuity). The two authorized source corrections are behavior-controlled
   (VegetationClimateDecoder.js comment-only, identical 31/1/472 + identical
   exception pre/post edit; PEFoliageCore.js comment lines + the one exactness
   metadata string — no executable change).
3. F03 — your denominator separation: adopted. The figures stay as NIF/MODEL
   TEXTURE CROSS-REFERENCE (eabf6cf: 24,508 K1 ArkTexture entries over 5,596
   NIF models; c380a26: 19,705/24,508 name-anchor OBSERVED); removed from
   terrain-coverage positions; the height A/B separation with BRIDGE_STATUS =
   UNKNOWN (02_ANALYSIS/F03 + DOWNSTREAM_CONTRACT_CORRECTIONS).
4. F04 — your predicate-insensitivity: reproduced (RGB 49,941 B / RGBA 16,918 B
   / zlib 27 B fixtures all MISSED by the historical predicates; raw-u8
   DETECTED). The negative language is corrected to per-method index-enumeration
   claims; the two methods kept separate; the honest BLOCKED-UNKNOWN survives on
   the corrected basis.
5. F05 — your exactness/origin points: adopted. The four-way separation
   (BYTE-LOCKED / CONDITIONAL-MODEL / UNVERIFIED-PARITY / NOT-RECOVERED-INPUTS)
   is now IN the corrected code comments (zero arithmetic change); the typed-K
   control re-derived exactly with hex bits (0x3d4ccccc vs 0x3d4ccccd).
6. F06 — your Gate-B split: adopted (TWO variables; canonical authority BLOCKED
   while Q1 is absent; the advisory disposition recorded separately). No Q1
   self-award; no POM edit; no science rerun on governance grounds.

## WHERE EVERYTHING IS

- Package root: docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/
- Control: 00_CONTROL/RUN_CONTRACT.md (the verbatim dispatch contract),
  BASELINE_PIN.md (all pins re-verified), SOURCE_INDEX.md (every input hashed).
- Raw deltas: 01_RAW/FINDINGS.csv (6 findings, full §16 fields),
  V4_1_DELTA.csv (19 rows), UNRESOLVED_DELTA.csv (39 rows),
   RETRACTION_SUPERSESSION_DELTA.csv (9 preserved + 6 new edges: NEW-F01,
   NEW-F02, NEW-P3A, NEW-P3B, NEW-P3C, NEW-P3D),
  GATE_REVALIDATION.csv, MODIFIED_PATHS.csv (with diffs).
- Analyses: 02_ANALYSIS/F01..F06 + BLAST_RADIUS.md +
  DOWNSTREAM_CONTRACT_CORRECTIONS.md (the successor contract content — the
  historical contract file itself is NOT mutated) + SELF_ADVERSARIAL_PASS.md
  (10 falsification attempts + 8 negative controls + the honest NOT_CHECKED
  list).
- Evidence: 03_EVIDENCE/ (probes + outputs + the byte-exact diffs + the
  synthetic detector controls; EVIDENCE_INDEX.csv lists each with generator).
- Report + gates: 06_REPORT/ (this handoff, the full report,
  STAGE_ACCEPTANCE_GATES.csv, MANIFEST_SHA256.csv).

## GIT STATE FOR YOUR AUDIT

- HEAD = origin/master = remote = cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d
  (unchanged; PRE-PERSISTENCE by design — no commit/stage/push).
- Tracked diffs (unstaged; true `git diff --numstat` values, re-verified for
  AMEND_R1): AUDIT_ENTRYPOINT.md (+1/-0: one new row only),
  src/pesource/VegetationClimateDecoder.js (+30/-6 comment-only),
  src/peworld/PEFoliageCore.js (+20/-5 comment + one documentation-metadata
  string).
- Untracked: this package + the 2 pre-existing roots (untouched).

## WHAT WE DID NOT DO (scope honesty)

No new client/GPU/physical-console experiment; no new corpus; no Entropia.exe
patching; no historical package rewritten; no V4.1 acceptance criteria
weakened; no POM modification; no M1 closure; no M2 opening; no Viewer; no
decoder behavior change (the fail-closed flow is byte-identical; the unverified
parenthetical inside the thrown message string is recorded as an open residue
for a future authorized wording change).

## OPEN ITEMS WE HAND BACK (unchanged owners)

- Gate A re-award: gated on the post-audit of the REBUILT x87 P0 record (the
  corrected premises are in FINDINGS.csv F01 + GATE_REVALIDATION.csv).
- Gate B canonical authority: human Q1 decision (POM §12).
- Gate D: human only.
- The exact boot rejection predicate: UNKNOWN (needs a human-authorized runtime
  route or a real display environment — none started here).
