# BLAST RADIUS — EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927

Dependency-census discipline: for every corrected item, a bounded search of
the tracked repo files for dependents, with per-item dispositions
(PROVEN_AFFECTED / POTENTIALLY_AFFECTED / PROVEN_UNAFFECTED /
DEPENDENCY_UNKNOWN).

## 1. The old counter 1,664,000 (R2-F01-COUNTER)

- SEARCH (timing-explicit record, each value re-measured 2026-09-27):
  - (a) Phase 1 — pre-edit worktree (git ls-files at HEAD cc747df), all
    2,594 tracked repo files, 133,463,531 bytes, literals "1,664,000" /
    "1664000" / "1.664.000": ZERO tracked hits (the defect text lived only
    in the UNTRACKED R1 package F03).
  - (b) Post-Phase-4 re-verification — worktree WITH the R2 row, all 2,594
    tracked files, 133,465,692 bytes: exactly ONE tracked hit —
    AUDIT_ENTRYPOINT.md line 30, THIS run's own new R2 registration row,
    whose text DESCRIBES the correction ("1,664,000 -> 53,166,080"). HEAD
    (cc747df) contains ZERO hits; the R1 registration row (line 31) contains
    none.
  - (c) The R1 predecessor package (49 files, post-EDIT-A): exactly ONE
    occurrence — the corrected F03 statement itself (the correction text
    quoting the superseded value).
- DEPENDENTS: (d) ZERO live dependents of the old counter remain anywhere;
  the only occurrences are correction descriptions.
- Dispositions:
  - F03_TERRAIN_TEXTURE_SCOPE.md line 102 (the statement itself): PROVEN_AFFECTED
    — corrected by EDIT A (1 removed + 11 added lines, everything else
    byte-preserved).
  - Every other tracked repo file and every other R1 package file:
    PROVEN_UNAFFECTED (the byte-level search found no other occurrence; no
    decoding, rendering, or runtime value derives from a printed analysis
    counter).
  - The TDF height bytes, terrain.bnt, the 7.2 A/B separation, the
    BRIDGE_STATUS = UNKNOWN line, all calibration/unknown labels:
    PROVEN_UNAFFECTED (byte-identity checks; EDIT_A diff shows no other
    change).

## 2. The bad review equation 491x12 + 24 + 252 (R2-F02-ERRATUM)

- SEARCH: all 2,594 tracked repo files for "491x12 + 24 + 252",
  "491*12 + 24 + 252", "491 × 12 + 24" plus the whitespace-flexible regex
  /491\s*[x*×]\s*12\s*\+\s*24/. RESULT: 0 hits. Search timing: Phase 1
  (pre-edit worktree, 133,463,531 bytes; the R2 entrypoint row and this
  package's own records did not yet exist); post-run, the equation string
  appears ONLY in this run's own correction records — inside THIS package
  (its erratum, self-check, blast-radius, report, raw/control and evidence
  records) and in the new AUDIT_ENTRYPOINT.md R2 row — always quoted AS the
  corrected-false OLD_STATEMENT; no repo file asserts it.
- DEPENDENTS: none — the equation existed only in the human-pasted
  PE_MASTER_REVIEW chat relay, never in a repo file.
- Dispositions:
  - The pasted-review arithmetic (a chat-relay artifact): PROVEN_AFFECTED at
    the relay level only — documented as an erratum by this package (no repo
    edit was required).
  - The raw census 32/492/5,916/493/6/31/1/472 and all R1 package contents:
    PROVEN_UNAFFECTED (re-derived from the per_file rows and confirmed valid;
    no file was touched for this edge).

## 3. The evidence label "comment-only" (R2-P3-LABEL)

- SEARCH: all 49 files of the R1 predecessor package for "comment-only"
  (case-insensitive): 41 hits, each dispositioned in
  02_ANALYSIS/R2_P3_EVIDENCE_LABEL.md section 4 and
  03_EVIDENCE/R2_P3_PATCH_CLASS.json.
- Dispositions:
  - EVIDENCE_INDEX.csv line 10 (the DIFF_PEFoliageCore.js.patch row):
    PROVEN_AFFECTED — corrected by EDIT B (1 removed + 1 added line; the row
    stays one line, 5 fields, strict RFC4180).
  - 02_ANALYSIS/F05_EXACTNESS_ORIGIN_PRECISION.md line 87: PROVEN_AFFECTED as
    a LABEL (an additional imprecise "(comment-only; zero arithmetic
    change)" phrasing) but OUTSIDE the authorized edit set — recorded as open
    residue, NOT edited. Its factual content (zero arithmetic change) is
    true; only the "comment-only" lead word is imprecise. No consumer depends
    on that word.
  - The frozen patch bytes, the frozen sources (VegetationClimateDecoder.js /
    PEFoliageCore.js), the decoder, all runtime behavior:
    PROVEN_UNAFFECTED (byte-identity verified at S0 and re-verified at
    handoff; the label is a description string with zero behavior
    consumers).
  - The 06_REPORT already-precise phrasings, the VCD-scoped-accurate hits,
    and the AMEND_LOG historical fix records: PROVEN_UNAFFECTED (their
    statements are accurate for their scopes; they are not mislabels).

## 4. AUDIT_ENTRYPOINT.md (Phase 4)

- ONE row inserted at the top of the LATEST RUNS table; ALL existing rows
  byte-preserved (verified: the only vs-HEAD changes are the 2 added rows —
  the R1 row + the new R2 row; numstat 2/0; zero deletions).
- Disposition: the entrypoint's LATEST RUNS table = PROVEN_AFFECTED by
  design (the registration row is the run's own record). Every historical
  row: PROVEN_UNAFFECTED (byte-preserved).

## 5. DEPENDENCY_UNKNOWN items

- None for the three correction edges: every dependent search closed with a
  full-population result (0 or 1 hit, each dispositioned).
- The historical F05_EXACTNESS_ORIGIN_PRECISION.md:87 residue (open, outside
  the edit set) is a LABEL residue only; no functional dependency is unknown.
