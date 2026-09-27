# SELF-ADVERSARIAL PASS — EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926

RUN_ID: EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926 (02_ANALYSIS)

Each load-bearing claim of THIS package was actively attacked before
finalizing. Format: CLAIM / FALSIFIER / TEST / RESULT / IMPACT. Executable
negative controls were run where feasible (evidence pointers included).

## 1. The corrected PRIMARY_DEVICE count (1/6, not zero)

- FALSIFIER: maybe the corrected mask is also wrong, or the raw flags contain
  another bit pattern; maybe DISPLAY1 is not really primary under a different
  SDK version.
- TEST: constants parsed from the LOCAL installed SDK wingdi.h (not a web
  citation); all 6 adapters recomputed from raw StateFlags only; mask controls
  0/1/2/4/5/0x04000005 with expected outputs pre-stated (2 -> old-true
  FALSE-POSITIVE; 4/5/0x04000005 -> corrected-true).
- RESULT: all controls as predicted; DISPLAY1 0x04000005 = ATTACHED+PRIMARY+
  REMOTE; count 1/6. (03_EVIDENCE/F01_PRIMARY_DEVICE_REVALIDATION.json)
- IMPACT: the ZERO-PRIMARY retraction stands.

## 2. The proposed new x87 blocker disposition (A-E split; cause UNKNOWN)

- FALSIFIER: maybe there IS a valid CW measurement (which would change variable
  A), or the exit -1 is not reproducible (variable B), or AV/EAX really was
  the mechanism (variable E).
- TEST: (a) searched the retraction record: the f0906b9 session died in the
  loader phase (0xC0000135) and its "init-CW datum 0x027F" is explicitly the
  W2.3 COMPARISON datum (the documented Win32 default read at CREATE_PROCESS)
  — NOT a measurement of CW at foliage-chain execution; no contrary evidence
  found -> UNMEASURED stands. (b) the exit -1 independently re-derived from
  the trace: 1 PID, 2,193 rows, exactly ONE Process Exit "Exit Status: -1",
  zero ddraw/d3d8/d3d9 loads. (c) N-13's debugger-artifact retraction read in
  full; AV/EAX not resurrected.
- RESULT: A = UNMEASURED; B = CONFIRMED (reproduced); C = observed facts stand;
  D = UNKNOWN (no causal proof: ordering is not causality; reserved DeviceKey
  is not malfunction evidence); E = supersession preserved.
- IMPACT: the disposition is falsifiable and survived; ENVIRONMENT_BLOCKED as a
  CONFIRMED cause class is correctly retracted to hypothesis.

## 3. The VCL corpus counts (32/492/5,916/493/6/31/1/472/256/246)

- FALSIFIER: maybe the whitespace census double-counts or the TSV count
  mis-parses; maybe the counts disagree with the historical raw output.
- TEST: (a) sum check: 5,916 = 493 x 12 exactly (integer total across files);
  (b) per-file groups12 all integers (each file's token count divisible by 12);
  (c) the historical generator RE-RUN as a byte-identical copy (SHA proven;
  only the OUT line patched) reproduced total_rows_alltokens=492 /
  numeric_rows_12cols=491 / special rows 3 / models 256 EXACTLY;
  (d) cross-compared with Desktop's six claims: all MATCH (492/493/31+1/472/
  447/bad-files-25vcl-only); (e) the historical iter032_vcl_columns.json SHA
  verified unchanged before/after the re-run (A62D9473...).
- RESULT: counts reproduce from bytes; no disagreement found anywhere.
- IMPACT: the F02 census is solid.

## 4. Any proposed 25.vcl semantics (actively avoided + attacked)

- FALSIFIER: does this package anywhere claim "0,2 means 0.2" or "the engine
  rejects 25.vcl"?
- TEST: text scan of the package's F02 artifacts: the claims are limited to
  JS/Python behavior + UNVERIFIED markers for engine semantics; the comma-line
  record lists the tokens WITHOUT interpretation.
- RESULT: no semantic claim made; §6.4 statuses all UNVERIFIED where evidence
  is absent; §6.5 honored (no parser change).
- IMPACT: the overclaim trap avoided. RESIDUE recorded honestly: the decoder's
  throw string still contains the unverified parenthetical "(the engine stream
  would fail here too)" — behavior-locked; carried for a future authorized
  wording change.

## 5. Any claim that decoder coverage is complete

- FALSIFIER: maybe after the corrections the decoder still covers everything.
- TEST: the decoder itself executed over all 32 originals: 31 successes /
  1 THROW (25.vcl) / 472 records — 21 groups of 25.vcl (252 tokens) never
  returned; 10 model ids unreachable via the decoder (256 raw -> 246 returned).
- RESULT: coverage is INCOMPLETE and now documented as such
  (UNSUPPORTED_BY_CURRENT_DECODER); no completeness claim anywhere in the
  package.
- IMPACT: V4 row 18 correction justified; the coverage deficit carried
  explicitly.
- EXECUTABLE NEGATIVE CONTROL (03_EVIDENCE/scripts/r1_selfadversarial_decoder_controls.mjs):
  valid 24-token payload -> SUCCESS(2) as expected; corrupted comma token ->
  THROW (non-numeric); 13-token partial -> THROW (not a multiple of 12); empty
  payload -> THROW. 4/4 PASS — the decoder fails CLOSED, not silently.

## 6. The terrain-vs-NIF denominator separation (24,508 is NOT a terrain denominator)

- FALSIFIER: maybe the K1 table IS a terrain resource set (e.g., if the models
  were terrain meshes).
- TEST: the generator's own SUMMARY.json fields: "method: M3-4.5 V2 (mesh ->
  texturing-property slot -> ArkTexture...)", corpus = Models.bnt (BNT2 index
  5,596 NIF entries; parse closure 5596/5596), arktexture_entries = 24,508 =
  v10_entries 19,637 + v4_entries 4,871; the terrain texture chain's own
  denominators are distinct (175 manifest ids; 8,381 PCG entries; 96/96 climate
  textures; 51,920 tiles) and none equals 24,508.
- RESULT: the K1 population is NIF models; the separation stands.
- IMPACT: F03's re-labeling is correct; the measurements preserved with their
  true scope.

## 7. The bounded negative-search language (predicate sensitivity proven by a MISSED fixture)

- FALSIFIER: maybe the historical size predicates would actually catch
  RGB/RGBA/zlib grids (which would make "exhaustive" defensible).
- TEST: 8 synthetic fixtures generated + run against BOTH historical
  predicates: raw u8 65x65/129x129 DETECTED (positive control); RGB
  (12,693/49,941 B), RGBA (16,918/66,582 B), zlib (317/27 B) ALL MISSED —
  the predicates are provably blind to those encodings.
- RESULT: "all entries in corpus X were enumerated under predicate Y" = valid;
  "all possible grid representations are absent" = INVALID; the corrected
  language is forced.
- IMPACT: F04 stands; omitted classes carry NOT_DETECTED_UNDER_THESE_PREDICATES
  + UNKNOWN. Fixtures labeled SYNTHETIC DETECTOR CONTROLS (predicate
  calibration; NOT evidence resources exist).

## 8. The PC/RC conditional exactness wording

- FALSIFIER: maybe some evidence proves unconditional parity (which would make
  the conditional wording an UNDERclaim).
- TEST: (a) the PC24 measurements themselves: PC=24 differs on 14,104/229,376
  real + 103,073/1,245,184 synthetic — parity is model-dependent by direct
  measurement; (b) the site CW = UNMEASURED (see item 2); (c) the V4 HONEST
  LIMITS — the project's own binding text — already carried the condition.
- RESULT: the conditional wording is the strongest defensible form; the
  corrected comments now match the V4 row 11 formulation.
- IMPACT: F05 stands; the four-way separation prevents both over- and
  under-claiming.

## 9. The typed-origin formula (K = f32(0.01) widened)

- FALSIFIER: maybe the two K readings actually give the same f32 (which would
  make the typed-formula correction cosmetic).
- TEST: precision control at W=5, S=0: 0.04999999701976776 (0x3d4ccccc) vs
  0.05000000074505806 (0x3d4ccccd) — DIFFERENT by 1 ulp of f32; both decimal
  and hex recorded; the binary64 literal bits (0x3F847AE147AE147B) and the
  f32 bits (0x3c23d70a) recorded.
- RESULT: the shortened "W * 0.01" form is defective as an implementation
  instruction; the typed form restored in the successor contract content.
- IMPACT: F05 §10 stands.

## 10. The Q1/Gate-B authority status

- FALSIFIER: maybe a Q1 record exists somewhere else (renamed, another branch,
  another location).
- TEST: git ls-files '*QUALIFICATION*' (0); git ls-files | rg -i qualif (only
  the harness notepad); filesystem search of docs/audits (same);
  git log --all --diff-filter=A on the exact path (EMPTY — never added on ANY
  branch). The harness notepad was read for class: a debugging context log,
  not a benchmark record.
- RESULT: Q1 absent; canonical Gate-B authority = BLOCKED under the current
  POM; the advisory disposition recorded separately; nothing self-awarded.
- IMPACT: F06 stands; the split variables prevent the conflation.

## NEGATIVE-CONTROL SUMMARY (at least one per executable predicate)

| predicate | negative control | result |
|---|---|---|
| PRIMARY mask &4 | controls 0/1/2 (2 = the false-positive trap) | as predicted (2 -> old-true; 0/1 -> both false) |
| PRIMARY mask &2 (old) | controls 4/5/0x04000005 | false-negative on all three — the defect demonstrated |
| decoder fail-closed | corrupted token / partial record / empty payload | 3/3 THROW as designed (plus 1/1 valid PASS) |
| decoder pre/post-edit behavior | full 32-file census re-run after the comment edits | IDENTICAL 31/1/472 + identical exception |
| N-8 size predicate | RGB/RGBA/zlib fixtures | MISSED (insensitivity proven) |
| N-8 size predicate (positive) | raw u8 4225/16641 fixtures | DETECTED (the predicate is not inert) |
| typed-K vs binary64-K | W=5, S=0 both readings | DISTINCT (1-ulp f32 difference) |
| Q1 existence | git log --all --diff-filter=A on the Q1 path | empty (never existed on any branch) |

## NOT_CHECKED (honest limits of this pass)

- The Ghidra-level re-verification of FUN_0083a7d0's decompile was NOT re-run
  (the iter032 evidence is cited as standing; no new RE was authorized).
- The full ProcMon CSV was re-counted row-by-row; the total-row delta vs the
  historical "282,059" is ROOT-CAUSED (AMEND_R1,
  03_EVIDENCE/F01_TRACE_LINECOUNT_ERRATUM.json): this pass's original count of
  282,192 was a CR-splitting artifact (133 lone CR bytes embedded inside quoted
  Detail fields counted as extra line boundaries by a CR-sensitive reader);
  282,059 stands as the correct LF data-row count (LF = 282,060; lone CR = 133;
  both re-derived byte-exactly and matching PE-MASTER's independent counts); the
  per-client facts all reproduce.
- The 200xx.vfs interiors beyond the size census remain NOT_CHECKED (the
  historical run's own bound; unchanged).
- No claim in this package was validated by visual similarity or by a client
  run (STATIC-ONLY).
