# AUDIT NOTICE — independent deep postaudit of this campaign exists

This directory is the published sanitized projection (commit 2265ec6, 2026-10-18) of the
sealed building-placement campaign `PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018`.

**The campaign's independent deep postaudit exists at
`docs/audits/PE_935_BUILDING_PLACEMENT_5H_DEEP_POSTAUDIT_R1_20261019/`.**
It was performed AFTER campaign completion, saved-evidence only (no game, runtime,
debugger, Ghidra or original EXE access; source run and repo untouched).

## Verdicts (postaudit, superseding parts of this projection's own claims)

- Science: **PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS**
- Process: **NONCOMPLIANT_WITH_ADMISSION_AND_MANIFEST_CONTRACT**

The technical publication at 2265ec6 was verified by the postaudit as real and
manifest-consistent (217/217 publication manifest rows match the committed blobs,
218 changed paths fully covered, AUDIT_ENTRYPOINT 1 insertion/0 deletions). The semantic
corrections below supersede the corresponding overclaims in the campaign reports
published here; publication is NOT scientific acceptance.

## Key corrections (see the postaudit REPORT.md for full evidence)

1. **Manifest bijection:** 285 physical files vs 260 parent-manifest rows — 24 nested
   manifests were omitted from the parent manifest; the full parent bijection FAIL
   (260 listed + 24 omitted + parent itself = 285). All 260 listed payload hashes match;
   the listed-payload integrity is preserved, the seal completeness claim is not.
2. **CALL sites: 136, not 133** — P07 has 13 CALL sites vs 10 distinct targets; the QC
   conflated sites with targets. 1254 raw extract rows are source-identical; the
   union of unique instruction VAs is 1253.
3. **P06/P07 admission breaches are not waivable by VA-window compliance** — P06 had 3
   bodies vs 2 reserved; P07 used 148 rows vs 133 reserved and 13 CALL sites vs 10.
   VA-window/global-cap compliance does not restore process PASS; the science of the
   affected packages is preserved separately (no load-bearing claims on unintended
   bodies).
4. **P11 boundary error** — endpoint 006B6C9D was excluded by the end-exclusive window
   but present in the P11 extract (this duplicate explains 1254 sum vs 1253 union).
5. **P04 envelope mismatch** — the ADMIT event envelope did not cover the explicitly
   contracted caller subregion 006A36F0.
6. **Scheduler/registration semantics rejected** — the saved decompile of 0040B070 is a
   member-view getter (`return param+0x14`), not a callback registrar or scheduler
   component.
7. **Frame-pair to projected-pair identity NOT_ESTABLISHED** — {0x66, A} and the
   element pairs are siblings in one container; the value-flow bridge remains open;
   no 296445 transfer.
8. **Five-source historical negative stays scoped** — NO_QUALIFIED_HISTORICAL_INSTANCE_
   TRANSFORM_FOUND_IN_REVIEWED_SOURCES (5 reviewed documents); it is not a 967-source
   exhaustive negative and does not prove 9.3.5 server-only.

## Science preserved by the postaudit

Static SF writer (005094C0: 3-DWORD copy to SF+34/+38/+3C, dirty+28), the 008BD720
getter (ECX+18h, 2 rows, no dispatch), the 745A70 byte-compare (zero-extended byte vs
full DWORD — class 20006 + separate tag 6 remains possible), and the pair/worklist/
callback plumbing facts.

Standing labels unchanged: WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED;
CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE.

The follow-up qualification run that applied corrections C1-C9 of this postaudit is
published at `docs/audits/PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_SAVED_R1_20261019/`
(H1 synchronous collection/projection mechanism CONFIRMED instruction-level; science
PASS_WITH_QUALIFICATIONS, process PARTIAL_NONCOMPLIANT; QC PASS_WITH_FINDINGS).
