# QC_REPORT — INTERNAL_QC of PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031

- QC mode: INTERNAL_QC (fresh context; QC did not author this run's spec artifacts —
  the run's contract was authored by a DIFFERENT pe-master-auditor session at formalize
  time; this QC session had no prior contact with the run).
- QC date: 2026-10-31. PARENT_LOOP: 75db9418-2d3e-4e05-9799-eeb4c3f63955.
- Scope: verify the executor's claims against actual code, raw evidence and gates.
- Writes: ONLY under 00_CONTROL/qc_probe/ (this directory). No executor evidence modified.

## QC_VERDICT: QC_PASS_WITH_FINDINGS
## REQUIRE_CORRECTIONS: NO
(all findings are P3; PE-MASTER may optionally order a prose-cleanup correction round.)

---

## 1. Independent verification performed (full method trail)

1. Read to EOF: REPORT.md, HANDOFF.md, HANDOFF_CONTRACT.md, PRE_DISPATCH_QC.md,
   all 4 x 02_ANALYSIS files, artifact_index.csv, STAGE_ACCEPTANCE_GATES.csv,
   all 6 x tools/ sources (decode_a.py, decode_b.cjs, volume_pin.py, field_stats.py,
   bvi_extract.py, compare_census_join.py), PINS_SHA256.txt, all 01_RAW JSONs
   (VOLUME_PIN, AB_AGREEMENT, MODEL_JOIN, TYPE0_FIELD_STATS, CORPUS_HEADER_CENSUS,
   SAMPLE_MANIFEST). FULL_READ_LOG: everything in the run package was read in full;
   hexdumps (4 files) were spot-checked, not read line-by-line (non-load-bearing —
   .bin files were independently re-hashed and re-parsed from Volumes.bnt).
2. Re-hash: P1–P5 + Z2 CSV + contract + Volumes.bnt + Models.bnt — 9/9 MATCH
   (QC_REHASH_RESULTS.txt). artifact_index.csv: 12 random rows re-hashed — 12/12 MATCH,
   0 MISSING.
3. Independent recount from Volumes.bnt/Models.bnt bytes with QC's own script
   (qc_recount_census_join.py; output QC_RECOUNT_OUTPUT.txt):
   - three-way census 1865=1865=1865 REPRODUCED;
   - header census 1686 TYPE0 (1686/1686 size-ok) + 164 TYPE1 (164/164 block-ok)
     + 15 other = 1865 REPRODUCED; TYPE0 records 21,818 REPRODUCED;
   - Models.bnt 5,596 entries / 0 duplicate names REPRODUCED;
   - name join exact 0 / id-1 1098 / id+1 10 / not-joined 757 REPRODUCED;
   - field join 675 fields, u32 0, u16 5 with EXACTLY the executor's 5 hits
     (506237.bvi recs 9/13/14 f8 -> 16201, recs 53/58 f5 -> 16645) REPRODUCED;
   - NEW QC MEASUREMENT (not in the run): full-corpus f1-f6 per-file spans over all
     1686 TYPE0 files — max span 1790.73 (506044), 0 files with span > 524,287,
     buckets <1:96, 1-100:1495, 100-1k:94, 1k-10k:1. CONFIRMS the per-file clustering
     claim corpus-wide (the report cited only 3 examples).
4. Negative controls: parsed DECODE_A.json + DECODE_B.json directly — 24/24 controls
   have failed=true WITH recorded failure output; 4/4 samples ok in both. EXECUTED, not
   declared (L19 satisfied).
5. Git boundaries: `git status --porcelain` = only `?? docs/audits/PE_WORLD_R2_.../`;
   `git rev-parse HEAD` = dc6f1961125596dba9f3156371fb427a90881436 == BASE_SHA;
   `git diff --stat HEAD -- compat/ src/` empty; zero commits. Production untouched.
6. Canon: §6 five lines quoted verbatim and byte-identical in REPORT §5 and
   PLACEMENT_CLASSIFICATION; no supersession proposed; PE_AXES_AND_UNITS = UNVERIFIED
   preserved; no world-coordinate naming of f32 values anywhere in the report.
7. Decoder independence (QH-009): decode_a.py is structure-first (trusts u16 header
   count); decode_b.cjs NEVER reads the header count for TYPE0 — it solves the record
   grid from repeating-pattern statistics + divisibility and derives vcount by f32-run
   scan; different languages (Python vs Node), different derivation paths, no shared
   field table (verified by reading both sources to EOF; B's corpus calibration uses
   strides B itself derived from pattern support, not A's table). The 12|36 sub-grid
   ambiguity is honestly persisted in stride_solutions. INDEPENDENCE: CONFIRMED.

## 2. Gate table — predicate vs printed result (L14: read the predicate, not the label)

| Gate | Predicate (from code/evidence) | Result | Gap vs report label |
|---|---|---|---|
| G1 | 6 SHA re-hash vs contract §5 (QC: 7/7 MATCH incl. Z2CSV); verdicts extracted from P1–P5 files with evidence paths (PRIOR_CANON_PLACEMENT_VERDICTS.md — 5 package tables, none memory-sourced); P5's "payloads not studied" honestly recorded, so no re-derivation | PASS | NONE. G1 label matches. P5 did not study .bvi payloads -> no re-derivation occurred; QC verified the run's own dual decode is genuinely new work. |
| G2 | Volumes.bnt exists; SHA == pin (QC MATCH); (a) own parse == (b) Z2 CSV recount == (c) distinct names — QC independently recomputed 1865=1865=1865; roundtrip true, 0 boundary violations, per-row name mismatches 0; 900-vs-1865 documented in VOLUME_PIN.json + report | PASS | NONE. G2 label matches; the "900" is correctly reported as unsupported. |
| G3 | >=3 diverse payloads (4: 148/40/2524/190690 B) x 2 independent impls; agreement table AB_AGREEMENT.json 4/4 both_ok, 0 divergences (36+9+630 fields + 29 type1 checks); negatives EXECUTED: QC parsed both JSONs — 24/24 failed with recorded output; lineage split documented in script headers; no shared field-map (verified by QC from both sources) | PASS | MINOR (P3-2): gates CSV says "12/12 negative controls" while REPORT says 24 (12+12). Both true per-decoder; no defect. |
| G4 | exactly one class (NOT_PLACEMENT_DATA); ALTERNATIVE_HYPOTHESES A1–A7 present, each resolved by measurement or explicitly open (A6/A7 = RESUME_POINT, honestly open); no gate text assumes world-space — space classification is an output; V2-009 kept | PASS | MINOR (P3-4): dowod 4's recorded evidence cites 3 sample files; see finding below. Class assignment itself does NOT rest on dowod 4 alone (dowody 1+3 are load-bearing). |
| G5 | counts with exact criterion (numeric filename vs numeric .nif id; unique names both sides -> no first-match); denominators explicit (1865 names; 675 fields; 1350 u16 halves; TYPE1 fields excluded with reason); ambiguous=0 (each criterion exact-match against duplicate-free key sets) | PASS | NONE. QC reproduced all counts 1:1. See P3-3 nuance on cross-criterion overlap. |

No predicate is weaker than its label. No gate promotes a low-level success into a
higher-level one (L4 respected: decode agreement is never printed as "placement
understood"; NOT_PLACEMENT_DATA is a NEGATIVE role claim backed by absence-of-id +
geometry family + consumer join, each with denominators).

## 3. Findings

**P3-1 REPORT.md §4 — garbled coverage-algebra sentence (prose defect, no gate impact).**
Path: 04_REPORT/REPORT.md lines 73-75. The parenthetical "1851 zdekodowane wyłącznie na
poziomie nagłówka" contradicts the correct figure 1,861 given in §8.3 NOT_CHECKED item 3
(1865 − 4 dual-decoded = 1861; 1850 are family-censused, 15 unclassified — 4 dual-decoded
files are a SUBSET of the 1850, not additive). Blast radius: human-reader confusion only;
every load-bearing denominator elsewhere (4/1865, 1850/1865, 15, 1861, 675, 1350) is
correct and mutually consistent; gates unaffected. Suggested fix (for a future
correction round, executor doc — QC cannot edit it): replace the parenthetical with
"1865 = 4 dual-decoded (subset of 1850) + 1851 header-only-family (1850 censused + 15
unclassified)"; NOTE 1851 = 1865−4−(4 of the... ) — actually simplest correct phrasing:
"payload-dual-decoded 4; header-family-confirmed 1850 (includes the 4); header-unclassified
15; total 1865; header-only (no payload decode) = 1861".

**P3-2 STAGE_ACCEPTANCE_GATES.csv G3 row says "12/12 negative controls"** while
REPORT.md §3/§7 says 24 (12 per decoder). Both numbers are true (12+12=24; QC verified
each JSON has 12 failed controls). Cosmetic inconsistency only.

**P3-3 name-level join cross-criterion overlap (QC-discovered, no reported count wrong).**
tools/compare_census_join.py lines 130-137 use elif ordering; QC's independent recount
found 5 .bvi ids for which BOTH id−1 and id+1 exist in the NIF id set — the elif
attributes them to id_minus_1. Within each single criterion the match is exact against a
duplicate-free key set (0 duplicate names on both sides), so "ambiguous = 0" is correct
PER CRITERION and the contract's no-first-match rule is satisfied. The two shifted
criteria are reported as separate alternative measurements, not as one resolution, so no
claim is affected. Blast radius: none on the primary claim (exact = 0) or on the
bvi_id=nif_id+1 pattern measurement (1098). Recorded so PE-MASTER sees the elif's
 tie-breaking semantics explicitly.

**P3-4 world-frame rejection (dowod 4 / A1): recorded evidence thinner than the claim's
scope; QC counter-measurement CLOSES the gap.**
02_ANALYSIS/PLACEMENT_CLASSIFICATION.md lines 32-37 and BVI_STRUCTURE.md lines 35-38
state "ranges f1–f6 strongly clustered per-file" but cite only 3 sample files. For the
4-sample classification this is sufficient (diagnostic on the decoded samples). For the
corpus-level wording the report had no persisted corpus measurement. QC executed one
independently (qc_recount_census_join.py; QC_RECOUNT_OUTPUT.txt): over ALL 1686 TYPE0
files, max per-file f1-f6 span = 1790.73, 0 files span > 524,287 (world scale), 1495/1686
spans in 1–100, 96 spans < 1 — the clustering claim holds corpus-wide. QC also notes
(L8) that per-file clustering ALONE cannot fully exclude a shared world frame (a regional
clustering alternative exists); the report is aware of this and scopes the exclusion to
"a shared world frame" while keeping per-record space UNDETERMINED and PE_AXES_AND_UNITS
UNVERIFIED, and A1's resolution rests on dowody 1+3+4 jointly (no model id + consumer
join + clustering), so the NOT_PLACEMENT_DATA class does not depend on dowod 4 being a
hard gate. No correction required; the QC measurement is persisted here as the missing
corpus-level evidence if PE-MASTER wants it on record.

**QC-side transparency note (not an executor finding):** QC's first P4 hash comparison used
a hand-transcribed expected literal and produced a false MISMATCH ("A4AB" vs the
contract's actual "A2AB"). Re-verification against the contract FILE itself confirmed
MATCH. Error was in the QC transcription; executor evidence unaffected (L10:
SOURCE_FILE_UNCHANGED / MANIFEST_IDENTITY_CORRECT distinction applied).

## 4. Sample->corpus promotion check (QH-019)

The corpus class NOT_PLACEMENT_DATA rests on: (i) 4/4 dual-decoded samples fully
measured; (ii) header census 1850/1865 = 99.2% with STRONG structural predicates
(TYPE0: 4+count*36==packed holds for 1686/1686 — a 1-in-epsilon size coincidence;
TYPE1: vertex block fits 164/164); (iii) P5's STANDING consumer join 1,666/1,666
(template B -> single .bvi per model). The 15 "other" files (0.80%) and the 584781 tail
(80.9% of that one payload) are NOT silently absorbed — they are in NOT_CHECKED (§8
items 1-2), in ALTERNATIVE_HYPOTHESES as explicitly open A6/A7, and in the RESUME_POINT
list. Denominators are explicit at every level. QC judges the promotion honest: the
sample->corpus step is disclosed as census-based, not claimed as payload-proven.

## 5. NOT_CHECKED (QC)

- 01_RAW hexdump .txt files (4): spot-checked only (bins independently verified from
  Volumes.bnt; hexdumps are derivative views).
- No re-execution of decode_a.py/decode_b.cjs by QC (tools re-hashed; their outputs
  independently reproduced by QC's own parse of the same raw bytes for all load-bearing
  counts; the negative-control FAIL outputs were verified from the persisted JSONs, not
  re-run). This is a bounded-inspection choice, not a gap in any gate predicate.
- P1–P5 evidence files cited inside PRIOR_CANON_PLACEMENT_VERDICTS.md (e.g.
  Z2_JOIN_RESULT.json): NOT re-opened by QC; G1 requires their PRIMARY reports re-hashed
  (done, 7/7 MATCH) and verdicts extracted (verified present with paths).

## 6. Compact handoff

ASSIGNMENT_MODE=INTERNAL_QC / RUN_ID=PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031 /
PARENT_LOOP=75db9418-2d3e-4e05-9799-eeb4c3f63955 / MILESTONE=pe-world-continuous-r2 /
SCOPE=run package + raw pins (read-only) / QC_VERDICT=QC_PASS_WITH_FINDINGS
(REQUIRE_CORRECTIONS: NO; 4 findings, all P3) / FINDINGS=P3-1..P3-4 (above) /
FULL_READ_LOG_PATH=00_CONTROL/qc_probe/QC_REPORT.md §1 /
NOT_CHECKED=§5 above / FINAL_REPORT_PATH=04_REPORT/REPORT.md (executor, untouched) /
GATES_PATH=STAGE_ACCEPTANCE_GATES.csv / MANIFEST_PATH=artifact_index.csv (29 rows,
12 random re-hash MATCH) / INPUT_AND_OUTPUT_HASHES=QC_REHASH_RESULTS.txt +
QC_RECOUNT_OUTPUT.txt / FILES_CHANGED=00_CONTROL/qc_probe/ only (3 new files) /
BASE_SHA=dc6f1961125596dba9f3156371fb427a90881436 / HEAD_SHA=dc6f196 (unchanged, zero
commits) / PUSH_STATUS=N/A (no git operations; persistence is PE-MASTER's separate
stage) / UNRELATED_WORK_EXCLUDED=none (worktree clean outside run dir) /
NEXT_PARENT_ACTION=MASTER_AUDIT; optionally order a P3 prose-cleanup correction round
(P3-1, P3-2) and/or promote QC's corpus-span measurement (P3-4) into the run's evidence
via a new amendment run.
