# R2-P3 — EVIDENCE LABEL CORRECTION RECORD

RUN_ID: EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927 (02_ANALYSIS)
Desktop finding: R2-P3 (GATEC_REAUDIT_R2_REPORT_20260927 section 10, the P3
wording residue). Verdict: INDEPENDENTLY REPRODUCED.

## 1. THE PATCH CLASS (verified from the frozen patch bytes + the fresh live diff)

- The frozen patch 03_EVIDENCE/DIFF_PEFoliageCore.js.patch (R1 predecessor
  package; SHA256 27DEE19810FDED98FBE37E2013B742DA500BCD107AD0C85FEAFBCCDBF1E
  A96DD, 3,377 B) is BYTE-IDENTICAL to the fresh live
  `git diff -- src/peworld/PEFoliageCore.js` (raw buffer SHA256 27dee198...,
  3,377 B) — verified twice (S0 and the 1d probe).
- Hunk 1 (@@ -35,11 +35,26 @@): 4 removed + 19 added lines, ALL `//` comment
  lines (the EXACTNESS comment block's four-way status separation).
- Hunk 2 (@@ -120,7 +135,7 @@, inside `export const FOLIAGE_OPERAND_LOCK`):
  exactly ONE removed + ONE added line — the `exactness:` field value, i.e.
  ONE documentation-metadata string (the operand-lock provenance record).
- Classification: comment lines + ONE documentation-metadata string
  (FOLIAGE_OPERAND_LOCK.exactness). NO arithmetic change; NO parser change;
  NO control-flow change; NO placement change. Basis: every changed line is
  either a // comment or the single exactness string; no other line of the
  file differs; a full src/ walk found ZERO runtime consumers of
  FOLIAGE_OPERAND_LOCK / operandLock / .exactness outside the definition.
  The changed string feeds documentation metadata only (no executable read).

## 2. THE MISLABEL SITE (EDIT B target)

EVIDENCE_INDEX.csv (R1 predecessor package), strict RFC4180 parse: 27 rows x
5 fields, 0 malformed. The DIFF_PEFoliageCore.js.patch row sits at physical
line 10 (0-based row index 9) and its description field read:

    "Byte-exact git diff of the authorized comment-only exactness-wording correction"

That label called the change "comment-only" with NO disclosure of the
exactness metadata string — a MISLABEL of the patch class.

## 3. THE CORRECTION (EDIT B, applied)

New description field (the ONLY change in the file; the row stays ONE line,
5 fields; the patch bytes were NOT regenerated or modified):

    "Byte-exact git diff of the authorized correction: comment lines + ONE
    documentation-metadata string (FOLIAGE_OPERAND_LOCK.exactness) - no
    arithmetic/parser/control-flow/placement change (label corrected by
    EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927)"

Before-image preserved byte-exact: 03_EVIDENCE/BEFORE_IMAGES/
BEFORE_EVIDENCE_INDEX.csv (02E03B7D..., 7,536 B). Exact diff:
03_EVIDENCE/EDIT_B_EVIDENCE_INDEX.diff (1 removed + 1 added line). The R1
manifest row for EVIDENCE_INDEX.csv was refreshed by EDIT C (the manifest
refresh authorized by the contract).

## 4. THE BOUNDED SCAN (all 49 R1 predecessor package files; 41 'comment-only' hits)

- MISLABEL_LIVE_UNDISCLOSED (1): EVIDENCE_INDEX.csv:10 — the EDIT B target.
- IMPRECISE_RESIDUE_LIVE (1): 02_ANALYSIS/F05_EXACTNESS_ORIGIN_PRECISION.md:87
  — "the exactness overclaim documented and corrected (comment-only; zero
  arithmetic change)" — an additional imprecise phrasing of the PEFoliageCore
  correction with NO additionally-disclosure. OUTSIDE the authorized edit set:
  recorded as open residue, NOT edited (the contract forbids editing any
  historical package span other than the three authorized). Note: the R1 QC
  post-fix byte-scan (AMEND_LOG lines 492-504) covered only the 06_REPORT
  prose files + the entrypoint added row, and never saw the 02_ANALYSIS hits.
- ALREADY_PRECISE (2): 06_REPORT/GATEC_FINDINGS_REVALIDATION_REPORT.md:227
  (the multi-line "comment-only (PEFoliageCore.js additionally: the one
  exactness metadata string — no executable change)" phrasing) and
  06_REPORT/STAGE_ACCEPTANCE_GATES.csv:11 (SG10: "comment lines + ONE
  documentation-metadata string").
- ALREADY_PRECISE_IN_SUBSTANCE (1): 01_RAW/FINDINGS.csv:6 — the lead word
  "comment-only" is loose but the same parenthetical explicitly discloses
  "the exactness string now carries the condition".
- ACCURATE VCD-scoped (the VegetationClimateDecoder.js diff IS comment-only):
  EVIDENCE_INDEX.csv:9, REPORT.md:44/:230, HANDOFF_TO_DESKTOP_REAUDIT.md:45/:92,
  BLAST_RADIUS.md:13, RETRACTION_SUPERSESSION_DELTA.csv:12,
  F02_VCL_CORPUS_DECODER_REVALIDATION.md:164 (F02's authorized corrections
  are decoder-only and cite the 31/1/472 decoder control).
- HISTORICAL_FIX_RECORD (28): all hits inside 00_CONTROL/AMEND_LOG_R1.md —
  before/after quotes of corrected phrasings, fix enumerations, and the R1 QC
  post-fix scan record itself (not live labels).

Full per-hit record: 03_EVIDENCE/R2_P3_PATCH_CLASS.json.

## 5. WHY THE CORRECTION IS SAFE

The corrected field is a DESCRIPTION STRING in an evidence index —
descriptive metadata only; zero behavior consumers; zero runtime readers. The
patch bytes and the frozen sources are untouched (verified byte-identical
throughout). Blast radius: none beyond the two description strings (the
EVIDENCE_INDEX row + its manifest hash refresh).
