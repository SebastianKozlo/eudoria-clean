# STATIC_R1_EXTERNAL_POSTAUDIT_NOTICE — PE2003_MODEL_INSTANCE_PLACEMENT_STATIC_R1_20261024

Additive notice created by the PERSIST_PUBLISH worker of
RUN_ID PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025 (2026-10-25).
All R1 files in this directory are byte-untouched; this notice only records the
independent Desktop postaudit verdict and the corrected standing. It does not
modify any frozen R1 claim, artifact or manifest.

## Postaudit identity and verdict

Source (read-only): D:/Eudoria_Reconstruction/99_Audits/PE2003_STATIC_PLACEMENT_DESKTOP_POSTAUDIT_R1_20261025/REPORT.md
(SHA256 1946EABABD402BEAC7C7CCFDDD22FC640816A2D84535F97A629ABA3CA30DCBA4, re-verified MATCH in the R2 run INPUT_RECHECK.json).
Verdict: **REQUIRE_CORRECTIONS** — EVIDENCE_INTEGRITY=PASS; PUBLISHED_OBJECT_IDENTITY=PASS;
NATIVE_TASK_EXISTENCE=PASS; SCIENCE_VERDICT=PARTIAL_PASS_REQUIRES_MATERIAL_CORRECTIONS.
The postaudit explicitly preserves the value of the re-derived mechanisms and rejects the
strong R1 conclusions about local-position absence and static exhaustion; it does NOT assert
that positions exist in the files — both directions remained to be checked.

## SP-A01..SP-A09 dispositions (one paragraph each)

- **SP-A01 [P1] unproven absence of local positions / server-source exclusivity.**
  ACCEPTED. R2 standing corrected to **SOURCE_UNKNOWN** (neither local nor network exclusivity
  proven); the record[6]/struct-0x48 mechanism was precisely qualified but its object-identity
  join to 296445/218757 is STILL_AMBIGUOUS with exact missing edges (R2 REPORT §5). No
  NETWORK_ONLY wording is carried anywhere in R2.

- **SP-A02 [P1] float-triple scan proves nothing about positioning.** ACCEPTED. The v17
  scanner and its predicates were NOT repeated as evidence in R2; SELF_POSITIONING_FALSIFIED
  and ZERO_POSITIONAL_CONSTANTS are not carried (BASELINE_CORRECTIONS.md §B.5). Literal indexes
  were used only for navigation; conclusions come from dataflow, not pattern absence.

- **SP-A03 [P1] literal absence in 1936 files is not instance absence.** ACCEPTED. R2 carries
  the result only as the honest bounded negative "13 target ids, 0 foreign raw hits in the
  1936 corpus files + EXE" with the explicit MISSING_EDGE class for cross-DYN-dispatch
  consumers (J02_MODEL_ID_FLOW.json); no global NO_INSTANCE wording.

- **SP-A04 [P1] UDP-only transport overstates the bridge.** ACCEPTED. R2 wording is
  mechanism-level only (the message/transform channel reaches FUN_005030c0 on vt-0x5E2A3C
  class objects); transport exclusivity and per-definition occurrence remain UNKNOWN.

- **SP-A05 [P1] branches_exhausted unproven; runtime-only conflated with missing static work.**
  ACCEPTED. R2 executed the postaudit's own "next experiment" (B01/B02a/J01a/J01b/J02/P01/P02/
  J03/J04 — resolver/EXTN/PFIX ID space, native callback installers 0x0061E844/0x0061E858) and
  records the precise remaining static frontier (FRONTIER.md BLK-R2-01..10;
  PE2003_LOCAL_SOURCE_EXHAUSTED=NO). No exhaustion claim is made.

- **SP-A06 [P1] root modelID high vs declared default/medium policy.** ACCEPTED. R2 root and
  all children used modelID glm-5-3 with zero high (NATIVE_TASK_CENSUS.json; carried by QC);
  ROOT_MODEL_ID_POLICY noncompliance of the R1 amendment session remains on the R1 record.

- **SP-A07 [P1] malformed machine evidence tables.** ACCEPTED. R2 artifacts use strict JSON
  (no duplicate keys; ADMISSION_EVENTS is documented as a single strict-JSON object with an
  events[] wrapper, not JSON-lines) and re-hashed CSVs; the count/format conventions flagged
  by the postaudit are disclosed explicitly in the R2 REPORT §3 (P3-4/5/6). The frozen R1 CSVs
  are NOT modified.

- **SP-A08 [P2] closure/chronology not fully updated.** ACCEPTED. R2 closing documents carry
  tool-measured timestamps only (python datetime UTC) and separate tool measurements from
  declarations; no chronology PASS claim is made from unaggregated declarations.

- **SP-A09 [P2] unknown budget aggregates do not license no-cap-exceeded.** ACCEPTED.
  SEMANTIC_BUDGET_COMPLIANCE remains **UNVERIFIED** in R2 (REPORT §3 item 4; QC P1-1);
  ATTEMPT_CAP=PASS only. Process is PARTIAL_NONCOMPLIANT with disclosed defects, not COMPLIANT.

## Corrected standing (current canon, carried by R2)

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; **SOURCE_UNKNOWN** (replaces the
R1 NETWORK_RUNTIME_ONLY exclusivity wording); INSTANCE join: family-level ESTABLISHED,
object-instance STILL_AMBIGUOUS; **PE2003_LOCAL_SOURCE_EXHAUSTED=NO** (replaces the R1
branches_exhausted closure premise); no placement recovery claimed anywhere.

## Where the corrections were executed

PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025 — public sanitized projection:
`pe2003/research/PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025/`
(see its REPORT.md, BASELINE_CORRECTIONS.md, CORRECTION_LEDGER.json, FRONTIER.md, BACKLOG.json).
