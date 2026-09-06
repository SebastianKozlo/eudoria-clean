# HANDOFF — PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209

For PE-MASTER (KROK-2 audit from disk) and the external post-auditor:

1. **Verify driver hash** — SHA256_DRIVER.txt:
   `b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a`
   (hash taken after the last edit, before execution; the driver
   re-verifies it in-prologue and HARD-STOPS on post-hash edit).
2. **Reproduce**: `python 00_CONTROL\morph_residual_deepdive_r1.py`
   (~28 s). Expect every number in 06_REPORT/00_FINAL_REPORT.md
   "Reproduction" — in particular G2 EXACT (walk 10,274/6,167/65,050/
   143,874; R34 row agreement 6,167/6,167; rr 2,427/2,093/334 = 62+272;
   neither 3,438; unknown-325 = 325, 56 files, 551564 x84; R21 probe
   41/0.4197/0.8096).
3. **Pre-registration check (G3)**: 00_CONTROL/PRE_REGISTERED_HYPOTHESES.json
   + PREREG_MARKER.txt were written BEFORE any Phase-1/Phase-2 test
   (code order enforced in the driver; the marker timestamp precedes
   the test outputs). Every predicate in the table was evaluated as
   written; the report lists each with its result and counts.
4. **Evidence files**:
   - 05_ANALYSIS/BASELINE_REPRODUCTION.json — G2 numbers (all gates).
   - 05_ANALYSIS/HYPOTHESIS_RESULTS.json — per-hypothesis fits, negative
     controls, verdicts, and the OVERFITTING_CONTROL block (H3/H4
     killed by canonical-param validation 2/5 and 1/6; H5a/H5c/H7 PASS).
   - 05_ANALYSIS/COVERAGE_STATE.json — the machine-readable final
     state: real-record 2,158/2,427 (from 2,093), residual 325 -> 251
     unexplained + 74 join-explained; PARTIALLY_RESOLVED.
   - 01_RAW/NOFIT334_SPANS.txt + RESIDUAL333_SPANS.txt — full
     per-span raw hex (cap 2,048 B/span) of both target populations.
   - 01_RAW/H1_DESYNC_PROBE.json — POST-HOC, NON-COVERAGE
     characterization probe (largest-k-first 11; k2-first 10; k2-only 6;
     k1-only 0; the remaining all-paired spans are wide m=32 records,
     k≈23 > the tested kmax=16 — a NEXT-run pre-registration candidate).
5. **Claims to review**:
   - BASELINE: zero drift, row-exact vs the pinned R34 JSON.
   - H5a CONFIRMED: 39 spans parse as var-k + a <=41 B truncated record
     head (leftover 4 B dominant — consistent with a false tag-split
     cutting the next record); NC u±2 = 5; OC 20/19.
   - H5c CONFIRMED: 26 spans byte-exact var-k SHAPE with idx semantic
     relaxed (max-idx 768..1536 — the R33 even-32 head cluster);
     coverage caveat: shape-coverage, not vertex-index-semantic
     coverage. NC = 5; OC PASS.
   - H7 CONFIRMED: 74/325 residual spans are false-tag-split fragments
     (prev/next join Family-A-consumable; NC3 non-adjacent join ~6% vs
     22.8%); H6's diffuse 130-of-325 shift-fits classified COINCIDENTAL
     (per-start base rate 7.92%).
   - Everything else FALSIFIED with counts (H1/H1d 0/272; H2a 0; H2b 1;
     H2c 7-vs-NC5; H3 OC-FAIL; H4 OC-FAIL; H5b 0; H5d 0/0/0; H8 26<30).
6. **Honest disclosures**: H5a/H5c grammars are weaker than canon
   (bounded tail exception; idx<N dropped on some records); H7's greedy
   join evidence is permissiveness-bounded (the ~4x NC separation is
   the strength); H6a skipped 5 oversize spans, H7c skipped 32 oversize
   blocks (both recorded); the H1 desync probe is labeled post-hoc
   NON-COVERAGE; segmentation uniqueness remains unproven (unchanged
   from R34); the R21 HEX_UNKNOWN.txt contains 147 top-5-file dumps
   (not the full 333 as the contract described) — this run re-dumped
   all 333 to 01_RAW/RESIDUAL333_SPANS.txt.
7. **Git**: path-limited commit of exactly
   docs/audits/PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209/** +
   the byte-identical 99_Audits mirror; push; origin==HEAD verified.
