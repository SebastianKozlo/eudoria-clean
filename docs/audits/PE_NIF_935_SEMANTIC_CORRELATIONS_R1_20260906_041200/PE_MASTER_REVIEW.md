# PE_MASTER_REVIEW — PE_NIF_935_SEMANTIC_CORRELATIONS_R1_20260906_041200 (loop 0132d23c KROK 3)

AUDITED_RUN = PE_NIF_935_SEMANTIC_CORRELATIONS_R1_20260906_041200 (commit 2d48831, loop 0132d23c KROK 3)
VERDICT = MASTER_ACCEPTED (advisory)
AUTHORITY_STATUS = ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE

## SNAPSHOT_STATE

Persisted 2026-09-06 by pe-master-auditor in the final persistence batch of PE-MASTER loop 0132d23c-2f0f-42f2-bb07-fb74f637488b (KROK 3 of 3 — the ladder's last deliverable). The verdict text in this file is PE-MASTER's own, issued in the 2026-09-06 session from independent disk audit; this persistence adds no scientific claims beyond it. The audited run package stays byte-identical to its original commit (this review is an addition, not a modification); a byte-identical SYNC copy of this file exists in the 99_Audits tree.

## BASIS

BASIS (PE-MASTER independent disk audit, 2026-09-06): (1) commit scope = exactly 1 path (18 files, 257,917 insertions); origin/master == HEAD == 2d48831; (2) the reconciliation census verified from the run's artifacts (importer flags 558/128/72; field1 3,042/1,796; events 263/136/113; viewport 2,304/752/592/79/11 — all EXACT vs canon); (3) PE-MASTER INDEPENDENTLY CROSS-CONFIRMED the run's most valuable finding from a DIFFERENT run's raw data: the field1=-256/low8=255 class = the v10 zero-entry files — from the KROK-1 ARKTEXTURE_ID_TABLE.csv PE-MASTER derived 3,767 entry-bearing files => 5,596 - 3,767 = 1,829 zero-entry files; the probe's 1,796 v10 zero-entry + 33 v4 zero-entry = 1,829 EXACTLY (the arithmetic closes across two independent runs' artifacts); (4) the methodology verified: all 33 executed tests carry 10,000-label permutation controls with the observed statistic vs the permuted p95/p99 recorded; constants -> NO TEST (no default-success); every verdict OBSERVED/NO OBSERVED/NO TEST with the standing no-semantic-proof sentence present in every output; (5) the transient CENSUS_MISMATCH hard-stop during development (the executor's reconciliation tuple bug) honestly disclosed with the gate-then-fix-then-rerun chain in the report + the driver hash chain — the discipline worked as designed.

## THE P0 ANSWER

THE P0 ANSWER (what the four probes OBSERVED — all OBSERVED-level, none semantic proof):
- PROBE-1 (importer 3-byte flags, 758 v4 files): OBSERVED correlations with the exporter string (chi2 61.6 vs perm p95 9.5), block count (21.1/12.5), geometry triangles (55.5/13.0), entry count (19.7/12.9); NO OBSERVED with the nif version (0.36/9.5); mesh/morph/mirror = constants (NO TEST). The flags correlate with the EXPORTER TOOL + model complexity — the strongest OBSERVED lead yet recorded for the flag region.
- PROBE-2 (field1/low8, 4,838 v10 files): THE STRUCTURAL DISCOVERY — the field1=-256/low8=255 class = 1,796/1,796 files with ZERO texture entries (entry-count histogram: C1 has 1..16+ entries; C2 has ONLY 0); every other slot/effect/mesh correlation is a correlate of that zero-entry structure; PE-MASTER's cross-check (above) confirms the classes partition entry-bearing vs zero-entry at OBSERVED level; the field2 packing documented as a deterministic function (entry_count<<8 | low8) — the "what the classes mean" open item now carries a measured structural correlate (the -256 VALUE semantics remain unknown).
- PROBE-3 (263 event strings): OBSERVED zero/non-zero partition by family (chi2 24.8 vs p95 9.0): SOUND_HIT never zero (0/20), END/MORPH1 never zero, MORPH_LR zero-rate 0.49, START_USETOOL 0.47, ANIMCMD 0.09 — the sound family ALWAYS carries a non-zero value (an OBSERVED pattern; the meaning remains runtime-gated).
- PROBE-4 (viewport floats): position-1 = exactly 2.0 in 592/592 + 79/79 camera blocks (POSITION-STATISTICS); the 43B subclasses 3/8 R28-exact; k-means 85B k=3 / 121B k=4 (pre-registered); the 85B outlier clusters OBSERVED-correlate with skinned (54.0/12.6) and block count (29.9/17.1); 121B clusters NO OBSERVED; the 27+4 non-finite bit patterns censused and sanitized (the pre-registered amendment recorded).

## FOLLOW-UPS GENERATED

FOLLOW-UPS GENERATED (ordered, post-loop): (a) the wiki 09-semantics morph numbers update proposal (with KROK 2: 2,158/2,427 = 88.88%; 325 -> 74 + 251) — NOT applied (the loop forbids wiki edits); (b) the wiki 08-ark-proprietary "field1 classes — what the classes mean" open row can now cite the measured zero-entry correlate (a wording proposal, NOT applied); (c) the wide-record [idx][32xf32] morph candidate (KROK 2's pre-registered next hypothesis) — a future campaign; (d) KROK 4 (runtime semantics) — environment-gated as standing.

## COVERAGE

COVERAGE: PE-MASTER disk audit = the report + the PROBE2_CONTINGENCY.json tables verified cell-by-cell + the independent cross-check via the KROK-1 id table (the 1,829 arithmetic) + the structural methodology checks; accepted from the run's artifacts: PROBE1/3/4 tables + the permutation-control numbers; NOT_CHECKED: the raw event/viewport bytes re-decoded independently (accepted with the pin + reconciliation discipline); the 2003-side corpus (era 9.3.5 primary); all SEMANTIC roles (runtime-gated — the standing sentence).

## HANDOFF

HANDOFF: the entrypoint row (this batch) closes the ladder 3/3; the loop then STOPS with COMPLETED per the mission.
