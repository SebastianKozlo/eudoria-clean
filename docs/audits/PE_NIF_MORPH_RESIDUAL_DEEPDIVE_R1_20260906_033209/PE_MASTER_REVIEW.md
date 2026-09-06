# PE_MASTER_REVIEW — PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209 (loop 0132d23c KROK 2)

AUDITED_RUN = PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209 (commit 03b00cc, loop 0132d23c KROK 2)
VERDICT = MASTER_ACCEPTED (advisory)
AUTHORITY_STATUS = ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE

## SNAPSHOT_STATE

Persisted 2026-09-06 by pe-master-auditor in the persistence batch of PE-MASTER loop 0132d23c-2f0f-42f2-bb07-fb74f637488b (KROK 2 of 3). The verdict text in this file is PE-MASTER's own, issued in the 2026-09-06 session from independent disk audit; this persistence adds no scientific claims beyond it. The audited run package stays byte-identical to its original commit (this review is an addition, not a modification); a byte-identical SYNC copy of this file exists in the 99_Audits tree.

## BASIS

BASIS (PE-MASTER independent disk audit, 2026-09-06): (1) commit scope = exactly 1 path (the run dir, 16 files); origin/master == HEAD == 03b00cc; (2) the coverage arithmetic re-derived from COVERAGE_STATE.json: canon 2,093/2,427 (86.2%) -> new 2,158/2,427 (+65 = H5a 39 + H5c 26, disjoint; 2,093+65 = 2,158; 2,158+269 = 2,427 ✓); the residual: 325 = 74 join-explained (H7) + 251 unexplained (74+251 = 325 ✓); (3) the baseline reproduction EXACT incl. the row-by-row R34 agreement 6,167/6,167 (accepted from the run's artifacts + the exit-3 hard gate); (4) the methodology verified structurally: the pre-registration file exists (00_CONTROL/PRE_REGISTERED_HYPOTHESES.json, before-tests marker) and the OVERFITTING CONTROL demonstrably has teeth — it REJECTED H3 (10 fits, 2/5 validation) and H4 (12 fits, 1/6 validation) while passing the coverage-increasing grammars (H5a 19/19, H5c1 12/12, H5c2 13/13, H7 37/37 validation-exact); (5) the negative controls meaningful (NC1 u±2 separations 7.8x/5.2x; the H6 base-rate 7.92% analysis that classifies the 130 at-some-shift fits as coincidental — a textbook falsification); (6) the 99_Audits mirror present (16/16 byte-identical — the KROK-1 mirror omission not repeated).

## THE P0 ANSWER

THE P0 ANSWER = PARTIALLY RESOLVED (the honest non-pass class PARTIAL, exactly as the campaign design allowed): the real-record coverage rises 86.2% -> 88.88% (2,158/2,427) via two validated grammar extensions (H5a truncated-tail records <=41 B with head idx<N: 39 spans; H5c idx-bound relaxations: 26 spans); the residual decomposes 325 -> 74 join-explained (H7: false-tag-split adjacency, prev 45 + next 50, overlap 14; ~4x separation vs the ~6% non-adjacent base rate) + 251 UNEXPLAINED = BLOCKED-SEGMENTATION with the complete falsification list machine-readable; H6 (phase-shift/misalignment) REFUTED as coincidental (diffuse histogram, base-rate 7.92%); H8 (third family) REFUTED; H2a/b/c (k-range/tolerances) REFUTED.

## NEW KNOWLEDGE

NEW KNOWLEDGE (for the record): (a) the H5a truncated-tail record class (short spans 22-41 B = complete var-k records with a bounded tail exception); (b) the idx-bound classes H5c1/H5c2 (idx < 2N and idx < 0x8000 accept 26 more real records — a weaker but validated relaxation); (c) the 62 previously-alt-fit spans characterized: ALL have mscan fits with weights at the RECORD HEAD (pair@0+1 x245; 23 all-paired, 39 partial); the remaining all-paired wide records ([idx][32 x f32], m=32, k~23 beyond the tested kmax) = the PRE-REGISTERED NEXT-RUN CANDIDATE (a hypothesis for a future campaign, NOT a claim).

## SUPERSEDED NUMBERS NOTE

SUPERSEDED NUMBERS NOTE (ordered follow-up, OUT of this loop's forbidden wiki scope): docs/nif/09-semantics.md L190-195 currently cites "byte-exact on 2,093/2,427 classifier-real spans (86.2%)" and "Residual: 325 heterogeneous spans" — both numbers are SUPERSEDED by this run (2,158/2,427 = 88.88%; 325 -> 74 join-explained + 251). A wording update proposal (the F-2 pattern) is the ordered follow-up; it is NOT applied in this loop (the mission forbids wiki edits).

## COVERAGE

COVERAGE: PE-MASTER disk audit = the report + COVERAGE_STATE.json + HYPOTHESIS_RESULTS.json arithmetic (re-derived) + the structural methodology checks (pre-registration, overfitting control, negative controls); accepted from the run's artifacts: the row-by-row baseline reproduction (6,167/6,167), the per-hypothesis fit counts, the join analyses; NOT_CHECKED: the raw per-span payload bytes re-decoded independently (the run's decoded artifacts accepted with the pin discipline); the 2003-side morph corpus (not used by this run — era 9.3.5 primary, honestly recorded); the runtime SEMANTIC layer (the 9-float grouping, the delta meaning — still runtime-gated).

## HANDOFF

HANDOFF: the entrypoint row (this batch); the loop backlog: KROK 3 (correlations) next; the wiki-numbers update proposal + the wide-record H-candidate = post-loop ordered items.
