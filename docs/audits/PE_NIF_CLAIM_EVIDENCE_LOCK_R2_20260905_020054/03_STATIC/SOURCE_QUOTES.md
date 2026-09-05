# SOURCE_QUOTES — PE-NIF-CLAIM-EVIDENCE-LOCK-R2
# Every quote below was read from the physical file in this run (read-only).
# Format: S# | file (+line) | SHA256 of the quoted file | verbatim quote | why it matters here.

## S1 | 99_Audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119/00_CONTROL/control_r1.cjs L163-179 | SHA256 5ad889d34d7a1507f74fc7bf6005c5738f609093ffbce02035c517be9fc7a9a6
```js
const witness = {}; for (const f of FAMS) witness[f] = { changed_files_with_block: 0, changed_files_with_diff_inside_block_region: 0, old_only_files_with_block: 0 };
...
    for (const r of ranges) {
      if (!witness[r.fam]) continue;
      if (p953) witness[r.fam].changed_files_with_block++;
      else witness[r.fam].old_only_files_with_block++;
      for (const d of drs) if (d.start < r.regionEnd && d.end > r.start) {
        if (p953) witness[r.fam].changed_files_with_diff_inside_block_region++; else witness[r.fam].old_only_files_with_block++;
```
WHY: the R1 counting bug, verbatim — `ranges` has one entry PER ASCII OCCURRENCE, so both counters increment per occurrence, and an old-only row increments `old_only_files_with_block` TWICE (presence + the whole-file diff-region overlap). Reimplemented as a stage-local fixture (00_CONTROL/control_r2.cjs r1_bug_fixture); the historical script was NOT executed.

## S2 | R1 05_ANALYSIS/CLAIM_MATRIX.csv row C-R35-04 (proposed_wording) | SHA256 b6648cab04766b4d53d3dcb8d48651444e1f5f2b5f5157e5589a5c8f0771d183
> "Every family was validated on genuinely changed payloads at file level (214 changed + 4 old-only files all parsed by the R35 validators; family blocks present: 214/9/214/29/214)."
WHY: the superseded validator claim (no per-file/per-family validator join exists) + the occurrence/file conflation. Superseded by C2-A-02/03/05.

## S3 | R1 05_ANALYSIS/CLAIM_MATRIX.csv row C-R36-05 (proposed_wording) | same SHA256 as S2
> "All 10 TESTED single-era-observable formulas for d are falsified with exact 0 counts on both full corpora; this does not exclude untested deterministic functions - the wording must stay tied to the tested list."
WHY: the false ten-exact-zero wording. Physical recount (Node + Python + R36 agreement): NINE exact-zero; d==crc32(payload) = 3435/5596 + 3299/5426. Superseded by C2-B-01/02/03.

## S4 | R1 STAGE_ACCEPTANCE_GATES.csv G7 | SHA256 960bf69b552f630857616923cf71ff424299114bc5d128d15d9c6a81b1525b57
> "...file-level witnesses: anim/tex/imp 214/214, shader 9, morph 29; intra-block witnesses not established (documented limit)"
WHY: occurrence count (29) presented in a file-level witness gate. Superseded by R2G5/R2G6 wording.

## S5 | R1 STAGE_ACCEPTANCE_GATES.csv G8 | same SHA256 as S4
> "...10 tested formula families (exact-0); writer evidence absent; iff REJECTED"
WHY: the ten-exact-zero gate claim. Superseded by R2G8.

## S6 | R1 06_REPORT/PROPOSED_DOC_CORRECTIONS.md P6 | SHA256 5e8a44c4ce3bab23dbaea9328414e82b0589219ca22cf4b91e0b44d68924ae87
> "The 11 malformed rows are re-derived and listed in 01_RAW/CONTROL_R1_RESULTS.json (manifests[].strict_errors) and preserved row-exact in the sidecars (raw_text column)."
WHY: the false losslessness claim — no raw_text column exists in any of the 12 R1 sidecars; the R39 GAP role text was lost ("per-file gaps [priorities]"). Superseded by P6R2 + the 12 lossless sidecars.

## S7 | R1 06_REPORT/PROPOSED_DOC_CORRECTIONS.md P1-5 | same SHA256 as S6
> "- NEW: \"[9 × f32 delta triples — grouping structural; target quantity UNVERIFIED (position vs other; the 3-states-×-XYZ reading is an open hypothesis)]\""
WHY: "delta triples" asserts a grouping not established by divisibility of nine. Superseded by P1R2-5 ("9 × f32 trailing values; grouping and semantic role UNVERIFIED").

## S8 | R1 06_REPORT/PROPOSED_DOC_CORRECTIONS.md P4-3 | same SHA256 as S6
> "- NEW: \"This is the byte-complete, evidence-graded documentation of the NIF binary format as used by Project Entropia (parse closure 100% on both Models.bnt eras; per-family semantic status in the state table below)\""
WHY: "byte-complete" silently promoted from parser success. Superseded by P4R2-3 (evidence-graded for the tested corpora; four separated coverage metrics).

## S9 | R1 00_CONTROL/SHA256_CONTROL.txt | SHA256 71d1f5659058ab212041e6cdb70b9e2a23e3e0cbdc393e2350dd67ea21810c46
> "control_r1.cjs SHA256 (after last edit, before execution): 6A296CC778861FB6F9F684DBCCBD7CE0ACA938599E2BA300AFE327E4A36922BC
> EXECUTION 2 (after empty-line-trim fix; exec 1 hash 6A296CC7... ...): control_r1.cjs SHA256 (after last edit, before execution): 5AD889D34D7A1507F74FC7BF6005C5738F609093FFBCE02035C517BE9FC7A9A6"
WHY: exactly TWO recorded pre-execution hashes. The chat "3-execution history" has no recorded counterpart (C2-D-04a/04b).

## S10 | R1 02_LOGS/LOGS.md | SHA256 316e6687d1a05bb25fb030bf1073f04cff329a2b5f63874a0ec8d658fc5a095e
> "generate_claim_matrix.cjs — emits 05_ANALYSIS/CLAIM_MATRIX.csv (43 rows, all fields quoted). Iterated 3 times for column/status hygiene..."
WHY: the "3 iterations" refer to a DIFFERENT instrument (the claim-matrix generator), not the control script — the plausible source of the chat miscount; recorded as UNRESOLVED-origin, two-execution record (C2-D-04b).

## S11 | R1 00_CONTROL/generate_gates.cjs L6-24 | SHA256 14e29e023763b635f132b2cf41157fb0c608c628a0529840d213f0c98ee34b2a
> "const rows = [ ['G1','prompt SHA256 verified before execution','match','BFDB1D23... (recomputed = expected)','02_LOGS/LOGS.md'], ... ];"
WHY: the R1 gate ledger is a FIXED row array — conditions not computed from evidence (auditor finding F5). R2 gates are computed (run_gates.py) with negative-control fixtures; the R2 ledger is generated from TEST_RESULTS.json.

## S12 | 99_Audits/PE_NIF_FIELD_D_R36_20260904_171903/02_results/FIELD_D_TESTS.json T4_d_structure.census_953 | SHA256 2af4cd39d36db96a2013a6de75983469aa6e2e7856a40061de6c86c6d54ee043
> "name_derived_candidate_matches": { "d == crc32(payload) [== c]": 3435, "d == adler32(payload)": 0, "d == crc32(name)": 0, "d == crc32(name + 0x0A)": 0, "d == adler32(name)": 0, "d == crc32(name + u32size_le)": 0, "d == crc32(u32size_le + name)": 0, "d == fnv1a(name)": 0, "d == size": 0, "d == offset": 0 }
WHY: the TEN candidate keys with counts — nine exact-zero, the payload-CRC candidate nonzero (3435; 2003: 3299). Physically recomputed this run with 20/20 agreement (C2-B-01/02).

## S13 | 99_Audits/PE_NIF_FIELD_D_R36_20260904_171903/01_source/field_d_r36.py L110-122 + L502-533 | SHA256 3f74804ab264949bd473c6dc33057c68c510f420265c5c71502ea9faf9f8a8a6 (recomputed this run; equals FIELD_D_TESTS.json provenance.driver_self_hash_at_execution)
> "def crc32(b): return zlib.crc32(b) & 0xFFFFFFFF ... def fnv1a(b): x = 0x811C9DC5; for byte in b: x = ((x ^ byte) * 0x01000193) & 0xFFFFFFFF; return x ... cand["d == crc32(name + u32size_le)"] ..."
WHY: the candidate definitions used for the R2 physical recomputation (name bytes, u32size_le, FNV-1a parameters).

## S14 | 99_Audits/PE_NIF_CROSS_ERA_R35_20260904_170224/02_results/GRAMMAR_VALIDATION.json texture_slots['2003'] | SHA256 2f15df0d14dd03e1ee49d6f3d69cc4f7249ed7077800ffccc5174b8bdfa62d80
> "blocks": 5426, "grammar_split": { "v10": 4665, "v4": 761 }, "v10_field2_formula": { "blocks_checked": 4665, "exact_consumption_and_parser_agreement": 4665, "failures": [], "verdict": "CONFIRMED" }, "v4_raw_decode": { "blocks_checked": 761, "exact_consumption": 761, ... }
WHY: R35 validator results are CORPUS-LEVEL aggregates over all 5,426 files — no per-file/per-family validator join artifact exists, so family presence stays ASCII-name presence (C2-A-05/A-06).

## S15 | 99_Audits/PE_NIF_WIKI_AUDIT_R39_20260904_180213/artifact_index.csv line 5 (raw bytes; file carries a UTF-8 BOM) | SHA256 6a007dbb7d489a702258807babd3c758ecddbf87fe659160fd17579f0030ffa6
> 02_results/GAP_ANALYSIS.json,96AD4B7DD8E469AB86BC66B85D72273EA1BDB3E41F614B04F01B0C52BEDDA613,47354,per-file gaps, priorities, orphan/ambiguous-label classification,in-driver (hashlib.sha256 at run end)
WHY: the original row with the FULL role text ("per-file gaps, priorities, orphan/ambiguous-label classification") — 7 cells vs 5 header (malformed); preserved byte-exactly by the R2 sidecar (C2-C-02).

## S16 | R1 05_ANALYSIS/NORMALIZED_MANIFESTS/PE_NIF_WIKI_AUDIT_R39_20260904_180213.artifact_index.normalized.csv (GAP row) | SHA256 1a1a32224cab26841d95f971ed954d837f1d0be706c1bcd11ddd6e8e917b6373
> "...","5","02_results/GAP_ANALYSIS.json","per-file gaps [priorities]","96AD4B7D...",...
WHY: the R1 lossy normalization — the role field was reduced to "per-file gaps [priorities]" by taking positional cells of a malformed row and merging the displaced computed_by in brackets. The R39 manifest BOM (R2-NEW-1) was also silently stripped by R1's .trim().

## S17 | 99_Audits/PE_NIF_CLAIM_LOCK_POST_AUDIT_20260905_020054/06_REPORT/00_FINAL_REPORT.md (F1 table) | SHA256 f277afb5865aee61efe92b97c5a58a3a49a765f6edd48a060d5c2236989e7611 (recomputed this run; read-only input)
> "NiVertexMorphExtraData has 29 occurrences in THREE changed 2003-side files: 548296.nif (13), 548808.nif (13), 566482.nif (3)."
WHY: the auditor counterexample — INDEPENDENTLY REPRODUCED this run from the physical containers (13/13/3 in 3 unique files), not assumed.

## S18 | post-audit 00_CONTROL/verify.py + 01_RAW/verification.json | probe SHA256 6ff50e0b583ef450143a20d61c3c4f14572aa24b2e65f59a74510e142873dc22
> "def bnt(path): ... entries[name]=(payload,c,d) ... result['morph_changed_file_occurrences']={n:old[n][0].count(b'NiVertexMorphExtraData') ..."
WHY: the auditor's method was READ (read-only input) but no result copied — every R2 number is re-derived by control_r2.cjs (Node) AND run_gates.py (Python) from the physical sources.

## S19 | 99_Audits/PE_NIF_CLAIM_LOCK_POST_AUDIT_20260905_020054/00_CONTROL/OPENCODE_R2_PROMPT.md (Areas A-E + publication) | SHA256 46a2a99a9f1d03b4fe33f2fbfca89d2440fd702188a3d020e9bf29a7a370e5ed (verified pre-execution)
> "A. Reproduce and fix the population mismatch ... B. Repair candidate-formula wording ... C. Produce genuinely lossless sidecars ... D. Repair proposals without applying them ... E. Gates must detect failures ..."
WHY: the binding mandate of this run.

## S20 | R1 05_ANALYSIS/DENOMINATORS.json ("changed-payload family witnesses" entry) | SHA256 68bc7cf859790091647ec31138d5e77dcb151c27d9cf7923f31ab8c974328880
> "value": { "changed_files_total": 214, ..., "with_morph_block": 29, ... } ... "definition": "... All such blocks were validated by the R35 validators (which parsed all 5,426 files), so every family has FILE-LEVEL witnesses on genuinely changed payloads."
WHY: the denominator-inventory defect — occurrence count (29) stored under a file-count key plus the validator claim. Superseded by the four-counter taxonomy (C2-A-06).

## S21 | R1 05_ANALYSIS/COUNTEREXAMPLES.json CE-5 evidence (c) | SHA256 65217d21990e766674903f7dabc64b40439ff708fe2dd87051ae877986c9525a
> "(c) only 10 candidate formulas tested (all exact-0) - exclusion of tested formulas is not exclusion of all deterministic functions"
WHY: the ten-exact-zero error repeated in the counterexamples ledger. Superseded by the nine/ten correction.
