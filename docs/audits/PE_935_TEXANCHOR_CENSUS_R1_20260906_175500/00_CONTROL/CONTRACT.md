# CONTRACT — RUN D: PE_935_TEXANCHOR_CENSUS_R1_20260906_175500

- RUN_CLASS: MATERIAL (declared by PE-MASTER at FORMALIZE per A1.1; a measurement refining the confirmed K1 claim's caveat — no new format-field meaning)
- EXECUTOR: pe-reconstruction | INTERNAL_QC: fresh pe-master-auditor context | PE-MASTER targeted deep audit follows
- PARENT: PE-MASTER loop bd17344b-a054-4cf4-be8d-5f0b250e8509 (iteration 4) | MILESTONE: EU935-M1 (NO crossing) | ERA: PCG_9_3_5
- BASE_SHA: b7c85a5a1aad8b6c69a642c4f44e9b469a4f50da

ONE_PRIMARY_QUESTION: "What fraction of the 24,508 K1 ArkTexture entries (era 9.3.5) are structurally name-anchored to their OWN file — (a) the entry-name's mesh part resolves to a mesh/material name present in the same file, AND (b) the entry's slot field equals the name's slot suffix — versus a seeded cross-file negative control at chance? This measures the mesh->texture ASSOCIATION strength beyond ID-membership, quantifying the K1 caveat (physically-verified ID-membership is not automatically proof of every mesh->texture association)."

## 1. RESULT-CLASS DISCIPLINE
An OBSERVED-labeled measurement run (the KROK-3 pattern): every output carries the standing sentence "correlation/association outputs are OBSERVED-level evidence; semantic roles remain runtime-gated; no semantic claims"; what the anchor MEANS stays runtime-gated. The K1 chain resolution (24,474/24,508) is NOT re-tested — it stands; this run refines its caveat only.

## 2. INPUTS (READ-ONLY; pins verified in-driver; HARD STOP on mismatch)
- The K1 table: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021\01_RAW\ARKTEXTURE_ID_TABLE.csv (SHA256 34f64fc8c4dc2ffe84dde52efa588a8cfa843197250b8efd57224729c7c1bbf9 — re-hash directly; never trust a manifest).
- Models.bnt 9.3.5 (SHA256 c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0, in-driver re-hash) — the source for the per-file mesh/material-name universe (the R61 frozen parser, 10/10 pins, READ-ONLY).
- The manifest spec: D:\Eudoria_Reconstruction\99_Audits\PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500\00_CONTROL\MANIFEST_SCHEMA_SPEC.md (this run's artifact_index follows it + the self-validation gate).

## 3. METHOD (pre-registered in 00_CONTROL BEFORE the run; PREREG_MARKER + hashes)
- Name-part extraction: entry `name` (e.g. "Box01_1_BASE") -> the mesh-part (strip the final _<slot>) + the slot-suffix (the final segment).
- The same-file mesh-name universe: per file, the set of mesh/material names the R61 parser exposes (NiTriShape / material names).
- The anchor predicate (EXPLICIT, frozen): anchored(entry) = (the name's mesh-part is a member of the entry's OWN file's mesh-name set) AND (the entry's slot field == the name's slot suffix). Also report the two components separately (mesh-part resolution alone; slot-suffix consistency alone).
- The negative control (seeded random.Random(20260906)): for 10,000 sampled entries, re-evaluate the anchor predicate with a randomly-chosen OTHER file's mesh-name set (uniform over the entry-bearing files) — the chance anchor rate; explicit denominators.
- Sub-censuses: per-slot (the 40-slot canon), per-grammar (v10/v4), per-class where applicable; exact binomial 95% CIs for every reported fraction.
- Per-record outcomes machine-readable (entry key, parts, outcome, reason); zero size-derived numbers; the EIGHT negative fixtures (the standard list) fail-closed.

## 4. GATES
- G-PINS: all pins in-driver before any parse; mismatch = HARD STOP.
- G-CENSUS: the 24,508 rows reproduce from the pinned K1 table (row count + the per-file entry counts + the 24,474/34 resolved split untouched); mismatch = HARD STOP.
- G-METHOD: the predicate + the NC procedure + the sub-census list written to 00_CONTROL BEFORE the run (PREREG_MARKER; hash-recorded).
- G-EXEC: per-record outcomes; the driver self-audit (zero size-derived validation numbers); the eight fixtures fail-closed.
- G-SCOPE: read-only originals; zero payloads; run-local tooling only in 00_CONTROL; the artifact_index per the spec + the self-validation PASS.
- NO PASS/FAIL on the anchor fractions themselves — this is a MEASUREMENT: the outputs are the numbers, the CIs, the NC rate, and the OBSERVED labels (a diagnostic run; the anchor fractions do not gate anything).

## 5. REQUIRED OUTPUTS
- 00_CONTROL: the driver + the frozen method + PREREG_MARKER + pin results.
- 01_RAW: per-entry anchor outcomes JSONL (entry key, mesh-part, slot-suffix, own-file resolution, slot consistency, anchored, reason); the NC trial records JSONL (explicit denominators); the eight fixture results.
- 05_ANALYSIS: ANCHOR_RESULTS.json (the anchored fraction + CIs; the component fractions; the per-slot + per-grammar sub-censuses; the NC rate + CI; the denominators everywhere); MANIFEST_VALIDATION.json.
- 06_REPORT: 00_FINAL_REPORT.md (the s15 essentials) + HANDOFF.md; STAGE_ACCEPTANCE_GATES.csv; artifact_index.csv per the spec.
- REPORTING: every number OBSERVED-labeled with its denominator; the K1-caveat refinement stated in one paragraph (the association strength now measured); the standing sentence everywhere.

## 6. HARD STOPS / FORBIDDEN
- HARD STOPS: any pin mismatch; G-CENSUS mismatch; any write outside the run dir.
- FORBIDDEN: modifying any completed run package; wiki (docs/nif); runtime work; the R61 parser; payloads; any M2/milestone action; semantic claims about what the anchor means.

## 7. FINAL HANDOFF SCHEMA
AUDIT_OUTPUT_ROOT / FINAL_REPORT_PATH / PRIMARY_EVIDENCE_PATHS / RUN_STATUS / HARD_STOP_REASON.
