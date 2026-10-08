# QC_REPORT — PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007

SELF-CLASSIFICATION (mandated by the correction contract §6 / §Artefakty): this is the
executor's own fresh-context internal QC — a SELF-REVIEW by the SAME pe-reconstruction
session that produced this correction package. It is NOT an independent external
Desktop post-audit and NOT a PE-MASTER qualification. The authoritative independent
input for THIS correction's basis was the Desktop post-audit OF THE SOURCE RUN
(REPORT.md / CONTROL_COUNTERCHECKS.json / EDGE_AND_SCOPE_COUNTERCHECKS.json —
identities re-verified, INPUT_IDENTITIES.md §3). An independent Desktop post-audit of
THIS correction's SHA remains NOT_PERFORMED (pending persistence/publication).

Machine record: 03_SCRIPTS/qc_correction.py -> 03_SCRIPTS/QC_CORRECTION_RESULTS.json
(OVERALL = QC_PASS, 21/21 checks). Control machinery: 03_SCRIPTS/ctrl3_rebuilt.py +
03_SCRIPTS/ctrl4_exact_endpoint.py -> CONTROL_RESULTS.json (rebuilt CTRL_3 verdict PASS;
rebuilt CTRL_4 verdict PASS with the required 4-case matrix).

## 1. Corrected ledger classification — content-based derivation (C1–C6)

The QC derived the corrected classification FROM THE SOURCE LEDGER'S RECORDED CONTENT
(69 rows parsed from the READ-ONLY source package), and the corrected ledger's own
CORRECTED_COUNTED / CORRECTED_CLASS columns were NOT trusted either (they were only
compared against the derivation). What check C2 (03_SCRIPTS/qc_correction.py) actually
does — restated here honestly per the independent internal QC finding F-IND-2 (the
pre-repair wording of this section over-promised C2's independence; the defect was this
SELF-DESCRIPTION, not the classification; qc_correction.py is NOT modified):

- the 24 E-rows: LEDGER_CLASS == "ANALYZED_NEW" is used as the BRANCH SELECTOR; within
  that branch the row content IS checked — counted iff NEW_INTERPRETATION is non-empty;
- the 8 mandatory rows RV-01..RV-07 + NEIGH-09 (the mandatory set of the correction
  contract §1, matching the Desktop's excluded_but_interpreted_rows): verified by
  CONTENT — the marker phrases in NOT_COUNTED_REASON (RV-01 argument construction;
  RV-02/RV-03 temp init of the two locals; RV-04..RV-07 cleanup of the identified
  temporaries; NEIGH-09 receiver esi + result passed as an argument of FUN_006C9F30);
- the remaining 37 rows (11 RP exemptions + 17 clean NEIGH + 9 candidate NEIGH):
  assigned not-counted DERIVATIONALLY, without per-row content examination — C2 alone
  would not have caught a misclassified RP row, and the C4 agreement
  (CORRECTED_COUNTED == derived) is structurally guaranteed for those rows.

LEDGER_CLASS is therefore NOT fully re-adjudicated from row content by C2 (the
historical QC-I9 defect is closed by the C2 machinery only for the E-branch emptiness
check and the 8 marker rows). The FULL per-row independent content adjudication of ALL
69 rows was performed by the fresh INDEPENDENT internal QC (00_CONTROL_INTERNAL_QC/
QC_IND_REPORT.md §2; QC_IND_RESULTS.json check I6): its own row-by-row reading of every
row's NEW_INTERPRETATION + NOT_COUNTED_REASON under the literal source-run contract §2
rule found ZERO differences vs the corrected ledger (its stricter reading could only
RAISE the floor) — THAT adjudication, not C2, is the independence basis of the
32/11/17/9 classification. Derivation results (C2–C6):

- content-derived counted set = 32 == the corrected ledger's COUNTED set for ALL 69 rows
  (zero mismatches; census: 32 COUNTED_ANALYZED_UNIT + 11 PRIOR_REPIN_EXEMPTION_UNREVERIFIED
  + 17 NOT_COUNTED_CLEAN + 9 CANDIDATE_UNADJUDICATED);
- MINIMUM_NEW_ANALYZED_EDGE_COUNT >= 32 CONFIRMED (measured proven floor = 32);
- verbatim round-trip: all 69 rows x 9 original fields byte-identical between the source
  ledger and the ORIGINAL_* columns (the source text was never retyped — csv round-trip
  through 03_SCRIPTS/build_corrected_ledger.py).

## 2. Body accounting (C7–C8)

- FUNCTION_BODY_ACCOUNTING.csv: 7 COUNTED_AS_NEW_BODY_OPENING rows (the 6 declared bodies
  + the undeclared historical CTRL_3 probe FUN_006C0EE0, bytes 8B 81 20 01 00 00 C3 CC,
  interpreted as the manager+0x120 getter) — MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7
  CONFIRMED; 1 CANDIDATE_UNADJUDICATED row (the bounded-window neighbor-body raw display
  question); EXACT_NEW_FUNCTION_BODIES_OPENED = UNRESOLVED.
- Records-only probe scan: every read/disasm/u32 VA in the audited run's recorded scripts
  (31 distinct VAs across 03_SCRIPTS/ and 00_CONTROL_INTERNAL_QC/) falls inside the 6
  declared bodies' windows, the accounted FUN_006C0EE0 8-byte probe, the prior-scoped
  caller windows (0x0050A310 / 0x006A3930) or the recorded data-section pins
  (IAT/RTTI/vtable/string/security-cookie) — ZERO unaccounted probes in the RECORDED
  scripts. This proves the recorded scripts contain no other undeclared probe; the
  unrecorded execution history is not provable from records — hence EXACT stays UNRESOLVED.

## 3. Rebuilt controls — re-executed from import (C9–C14)

- CTRL_3 (synthetic fixtures / persisted prior pins; ZERO EXE access): clean
  (8B 41 68 C3 CC CC CC CC — the persisted getter pin) = PASS — accessor reads
  [ecx+0x68] == the producer-written field; mutated (8B 81 20 01 00 00 C3 CC — the
  recorded historical probe constant) = FAIL — reads [ecx+0x120], not [ecx+0x68].
  CTRL3_SYNTHETIC_OR_PRIOR_PIN_STATUS = SYNTHETIC_FIXTURES_AND_PERSISTED_PRIOR_PINS_ONLY.
- CTRL_4 exact endpoint (all four predicates simultaneously, exact addresses on verified
  decode boundaries): REAL CLEAN = PASS; historical EDI-clobber mutant
  (@0x0050A3DD, 8B 3D D0 D8 B9 00) = FAIL (P2: caller-side EDI write in the required
  range); 0x0050A3F6 push edi -> push esi (57 -> 56) = FAIL (P3); 0x0050A3F6
  push edi -> nop (57 -> 90) = FAIL (P3). All mutants SYNTHETIC/IN-MEMORY ONLY.
- The old checker's LOGIC reproduction over the same buffers: clean PASS; clobber FAIL;
  FALSE PASS on the two final-argument mutants — exactly the Desktop's
  CONTROL_COUNTERCHECKS.json matrix (wrong_final_push_ESI / missing_final_push_NOP =
  true/true on the old predicate; own_exact_endpoint_predicate = false/false) — the
  rebuilt checker's matrix equals the Desktop's own_exact_endpoint_predicate.
- Clean-buffer provenance: the CTRL_4 clean buffer was independently re-derived from the
  published window record's byte column (01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt: first VA
  0x0050A3B7, contiguous decode boundaries, 22 instructions, total 0x42 bytes,
  byte-identical to the fixture); the four call rel32 targets (0x6C0F90/0x6C10B0/
  0x50A1E0/0x5246E0) and both rel8 branch targets (0x50A3C8/0x50A3CC) recompute exactly.
- CTRL_4 semantic scope unchanged: CALLER-SIDE exact final-argument predicate ONLY; the
  four intervening callee bodies remain UNOPENED; CHILD_TO_JOIN_IDENTITY is NOT promoted
  (stays STRONGLY_SUPPORTED, NOT CONFIRMED).

## 4. No new science branches / corrected terminology / historical FAILs (C15–C17)

- The 8 additionally counted rows adjudicate ONLY interpretations already recorded in
  the source ledger (verbatim quote checks per row — ALL OK); the forbidden-ACTIVE-token
  sweep over the correction records found NONE outside superseded/retraction/negation/
  policy contexts (CHILD_TO_JOIN_IDENTITY = CONFIRMED; SCIENCE_PASS; WRAPPER_DEPTH = 2;
  CHILD_RESOURCE_PROVENANCE = CONFIRMED_MODEL_DERIVED; MODEL_ROOT_RELATION = CONFIRMED;
  CAND4_CHILD_ROOT_CLOSURE = STRONGLY_SUPPORTED; EXACT counts as numbers — none active).
- Corrected wrapper terminology verified in CORRECTED_LINEAGE_STATUS.md: WRAPPER_DEPTH =
  UNRESOLVED (semantics != budget consumption); POINTER_LINEAGE_TRANSITIONS_OBSERVED = 2
  (the examined H-1/H-2 description, not a global census); H-2 RELATION_TYPE = UNRESOLVED;
  historical NEW_WRAPPER_HOPS = 2 / MAX_NEW_WRAPPER_HOPS = 3 PRESERVED (the unresolved
  relation still consumed the budget — not zeroed, not reduced); no 2-wrapper-layers claim.
- Historical budget FAILs preserved verbatim in the corrected records:
  ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL; RETROACTIVE_PRIOR_AUTHORIZATION = NO;
  ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE = FAIL; ORIGINAL_SCOPE_COMPLIANCE = FAIL
  (historical state, never becomes PASS); EXACT counts = UNRESOLVED.
- Standing statuses re-checked (not raised): MODEL_ROOT_RELATION = UNKNOWN;
  CHILD_VISUAL_ROLE = UNRESOLVED; CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED (NOT
  CONFIRMED); CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND; EXACT_PARENT =
  CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (carried, ACLD-scoped); JOIN_OPERATION =
  STRONGLY_SUPPORTED (ceiling). The preserved raw facts (getter DIRECT_FIELD_GETTER
  [manager+0x68]; base-ctor NULL-init +0x68; the measured store [manager+0x68]=[instance+4];
  the lazy producer chain byte/dataflow facts) are NOT superseded anywhere in this package.

## 5. Immutability / identity / encoding / repo (C18–C21)

- SOURCE_PACKAGE at QC time: 38/38 BASE git-blob identity, zero mismatches, zero missing
  — READ-ONLY preserved (zero writes by this correction).
- The three Desktop post-audit inputs re-hashed at QC time: ALL MATCH the dispatch pins.
- Encoding of every package file at QC time: UTF-8 no-BOM, LF-only, strict-decodable.
- Repo state: HEAD == BASE 790e83735b439e2d76a250868a47a599c2c10184; zero tracked
  modifications; the 6 foreign untracked roots untouched; this correction's writes are
  confined to OUTPUT_ROOT; AUDIT_ENTRYPOINT.md NOT edited; no commit/push this phase.

## 6. QC-tooling defects found and fixed (QC script only; NO correction record was modified)

Round 1 (5 defects, all in 03_SCRIPTS/qc_correction.py; every record the QC checks was
unchanged — the fixes were to the QC's own comparison logic):
1. C7 compared CORRECTED_STATUS by exact string equality and missed the annotated value
   "COUNTED_AS_NEW_BODY_OPENING (THE PROVEN 7TH)" — fixed with a startswith test.
2. C12 negated the historical-clobber result when building the comparison dict against
   the Desktop's own_exact_endpoint_predicate (whose values are checker results, not
   expected-outcome booleans) — fixed to the direct result mapping.
3. C14 compared call/jump target strings without the decoder's 8-hex-digit zero-padded
   format ("0x6c0f90" vs "0x006c0f90") — fixed to the decoder's actual format.
4. C15's forbidden-token sweep used a context window that stopped at the token line and
   missed negation/supersession markers split across line breaks (e.g. "no tool of this
   run / issues a SCIENCE_PASS"; the SUPERSEDED sentence following a quoted claim) —
   fixed with an enclosing-paragraph window (4 lines above .. 2 below) with explicit
   superseded/retraction/negation markers; both flagged hits were adjudicated as
   legitimate negation/superseded contexts.
5. C16 checked the literal string "still consumes the budget", which wraps across two
   lines in CORRECTED_LINEAGE_STATUS.md — fixed to "still consumes".
All 21 checks re-run PASS after the fixes; the first-round failures were QC-comparison
defects, NOT record defects (the corrected records themselves were already conformant).

## 7. Verdict

```text
QC_VERDICT = QC_PASS (SELF-REVIEW; 21/21 checks)
QC_ORIGIN = SELF-REVIEW — fresh internal QC by the same pe-reconstruction executor
  session that produced this correction package (author: pe-reconstruction); NOT an
  independent external Desktop post-audit; NOT a PE-MASTER qualification
CORRECTION_RECORDS_QC = PASS   (the result of the NEW correction's records/machinery)
ORIGINAL_SCOPE_COMPLIANCE = FAIL   (the HISTORICAL state of the audited run; separated
  from CORRECTION_RECORDS_QC; never becomes PASS)
```

C4-C1 and C4-C2 are NOT declared closed by this self-review: closure belongs to the
PE-MASTER audit + persistence (and, for the new SHA, an independent external post-audit
that remains NOT_PERFORMED). No SCIENCE_PASS is issued (REAL_SCIENCE_AUTO_QUALIFICATION
stays DISABLED). Publication is not acceptance.

NOT_CHECKED by this QC (explicit): the unrecorded execution history of the audited run
(hence EXACT counts stay UNRESOLVED); the four §7 intervening callee bodies;
FUN_006C9700; FUN_006C8BB0; FUN_007B6C30; FUN_007BF900/FUN_007BF630; the manager
slot-2/slot-3 target bodies; the FUN_006C6780 continuation; all NEIGH bodies; runtime
anything (STATIC-ONLY lineage); payloads; the independent PE-MASTER audit of THIS
package (pending).

## 8. Record-repair (2026-10-07, PE-MASTER direct dispatch — post-independent-QC)

Origin: the independent internal QC of THIS package (00_CONTROL_INTERNAL_QC/
QC_IND_REPORT.md findings F-IND-1/F-IND-2; QC_IND_RESULTS.json; QC_VERDICT =
QC_PASS_WITH_FINDINGS, 2 x P3). PE-MASTER decision on both findings: POPRAWIONE I
ZWERYFIKOWANE (CORRECTED-AND-VERIFIED). Executor of the repair: pe-reconstruction
(RECORDS-ONLY micro-repair; zero new RE; zero EXE access; NO_NESTED_TASKS). Repairs:

- F-IND-1 (P3) — SUPERSESSION.md §S-4: the "no analysis is hidden behind RAW labels"
  citation re-attributed from FINAL_REPORT.md §4 (where the phrase does NOT exist) to
  CLAIM_MATRIX.csv CL-14, with the full genuine loci list (EDGE_ACCOUNTING_LEDGER.csv
  header line 8; PE_MASTER_REVIEW.md line 23; CLAIM_MATRIX.csv CL-14 evidence cell);
  S-4 substance unchanged. Secondary trivial fixes in the same file: S-3's QC-I10
  quote capitalization corrected to the source's "EXCEEDED by exactly 16"; every
  S-quote split by that file's own hard line wrap joined into a single-line contiguous
  (greppable) string (S-1..S-7 "Where" citations) — quote content otherwise unchanged
  (the whitespace/backtick normalization vs the source's own ~78-col hard wraps stays
  as verified by the independent QC I12; substance identical).
- F-IND-2 (P3) — QC_REPORT.md §1 reworded (above): it now describes exactly what
  qc_correction.py check C2 does (LEDGER_CLASS branch selector for the 24 E-rows +
  content verification of the 8 RV/NEIGH marker rows + derivational not-counted
  assignment for the remaining 37 rows) and records that the FULL per-row independent
  content adjudication of all 69 rows was performed by the independent internal QC
  (QC_IND_REPORT.md §2 / QC_IND_RESULTS.json I6: zero differences). qc_correction.py
  NOT modified (the defect was this self-description, not the classification); the
  C1–C21 check results stand. The equivalent wording in FINAL_REPORT.md §3 remains
  outside this repair's bounded 3-path allowlist — disclosed to PE-MASTER.

Scope of the F-IND-1/F-IND-2 micro-repair: 2 record files edited (SUPERSESSION.md, QC_REPORT.md — this
section included) + MANIFEST_SHA256.csv regenerated LAST (every-write-after-the-manifest
rule; scope formula unchanged: the physical files of OUTPUT_ROOT minus the manifest
itself; AUDIT_ENTRYPOINT.md still excluded pending persistence — the regenerated
manifest therefore also covers the 8 physical 00_CONTROL_INTERNAL_QC/ records present
since the independent QC, per that QC's I1 disclosure; ROW_COUNT 18 -> 26).
00_CONTROL_INTERNAL_QC/ read-only for this repair (zero writes); SOURCE_PACKAGE and all
historical packages untouched; the 6 foreign untracked roots untouched; HEAD == BASE
790e837; no commit/push (the persistence phase owns them); correction statuses, lessons
and science standings unchanged; no promotion of any kind.

Third micro-repair (same day, PE-MASTER direct dispatch — continuation of
PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1; RECORDS-ONLY; zero new RE; zero EXE
access; NO_NESTED_TASKS). Origin: the residual disclosure (a) of THIS executor at the
previous micro-repair — the F-IND-2 bullet above closed with "The equivalent wording in
FINAL_REPORT.md §3 remains outside this repair's bounded 3-path allowlist — disclosed
to PE-MASTER"; detected and adjudicated by PE-MASTER as CORRECT-AND-FIXED (the finding:
the SAME over-claiming self-description of qc_correction.py check C2 that QC_REPORT.md
§1 had already shed per F-IND-2 was still present in FINAL_REPORT.md §3, ~lines
127–129 of the QC_ORIGIN paragraph). Repair (the single content edit of this
micro-repair): FINAL_REPORT.md §3 — the phrase "the corrected ledger classification was
FULLY re-derived from the SOURCE ledger's recorded content (LEDGER_CLASS not trusted;
the corrected ledger's own columns only compared)" replaced with an honest description
consistent with the corrected §1 above: LEDGER_CLASS branch selector for the 24 E-rows
(row content checked within that branch — counted iff NEW_INTERPRETATION is non-empty)
+ CONTENT verification of the 8 marker rows RV-01..RV-07 + NEIGH-09 (the marker phrases
in NOT_COUNTED_REASON) + DERIVATIONAL not-counted assignment for the remaining 37 rows
without per-row content examination (the corrected ledger's own columns only compared,
never trusted) + the record that the FULL per-row independent content adjudication of
ALL 69 rows (zero differences vs the corrected ledger) was performed by the fresh
INDEPENDENT internal QC (00_CONTROL_INTERNAL_QC/QC_IND_REPORT.md §2 /
QC_IND_RESULTS.json check I6) — THAT adjudication, not C2, is the independence basis of
the 32/11/17/9 classification. No other FINAL_REPORT.md change; qc_correction.py NOT
modified (the F-IND-2 disposition stands — the defect was the self-description, not the
classification; the C1–C21 check results stand).

Scope of this third micro-repair: 3 files touched — FINAL_REPORT.md (1 content edit),
QC_REPORT.md (this §8 entry only, plus a 1-line clarity edit in the same §8 — the
earlier scope paragraph's heading retitled from "Scope of this repair:" to "Scope of
the F-IND-1/F-IND-2 micro-repair:" for unambiguous reference, zero substance change;
no other section changed), MANIFEST_SHA256.csv
(regenerated LAST per the every-write-after-the-manifest rule; scope formula unchanged
= the physical files of OUTPUT_ROOT minus the manifest itself; AUDIT_ENTRYPOINT.md
still excluded pending persistence; ROW_COUNT stays 26 — the two edited files' rows
re-hashed). 00_CONTROL_INTERNAL_QC/ read-only for this repair (zero writes);
SOURCE_PACKAGE and all historical packages untouched; the 6 foreign untracked roots
untouched; HEAD == BASE 790e837; no commit/push (the persistence phase owns them);
correction statuses, lessons and science standings unchanged; no promotion of any kind.
HANDOFF.md MANIFEST_ROWS = 18 remains the FROZEN PHASE RECORD of the original executor
phase (historically true at its generation time; the 18 -> 26 transition is documented
in this section above).
