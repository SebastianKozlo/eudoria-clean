# CORRECTION_RUN_GIT_OBSERVATION
RUN_ID: PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915
OBSERVED_AT: 2026-09-15 (before any package mutation by this correction run; measurements taken prior to writing any file in this package, including the correction contract file)
REPO: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean

## S1 GIT OBSERVATION (fail-closed, live disk > prompt)

- branch                = master
- HEAD                  = 8a09e459eb5a930054f35b713afe3e28b6fa5abc
- origin/master (local) = 8a09e459eb5a930054f35b713afe3e28b6fa5abc
- git ls-remote origin master = 8a09e459eb5a930054f35b713afe3e28b6fa5abc  refs/heads/master
- Expected BASE (contract)= 8a09e459eb5a930054f35b713afe3e28b6fa5abc
- ADJUDICATION: HEAD == expected BASE. NO conflict. No intervening commits. Fail-closed gate PASSED.
- git status --short (untracked only, 30 entries):
```
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/00_CONTROL/RUN_CONTRACT.md
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/00_CONTROL/SOURCE_IDENTITIES.json
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/00_CONTROL/__pycache__/slot17_core.cpython-312.pyc
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/00_CONTROL/run_state.json
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/00_CONTROL/slot17_core.py
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/00_CONTROL/slot17_run.py
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/01_RAW/SLOT17_BODY_RAW.txt
?? experiments/eu1030/EU1030Coords.js
?? experiments/eu1030/EU1030CtcParser.js
?? experiments/eu1030/EU1030Method1Codec.js
?? experiments/eu1030/EU1030Objects.js
?? experiments/eu1030/EU1030Placement.js
?? experiments/eu1030/EU1030TerrainParser.js
?? experiments/eu1030/EU1030Vegetation.js
?? experiments/eu1030/EU1030Voxel.js
?? experiments/eu1030/EU1030VoxelChain.js
?? experiments/eu1030/demo/index.html
?? experiments/eu1030/demo/main.js
?? experiments/eu1030/package.json
?? experiments/eu1030/test/fixtures/bad_instoff.dat
?? experiments/eu1030/test/fixtures/corrupt_count.dat
?? experiments/eu1030/test/fixtures/corrupt_size.dat
?? experiments/eu1030/test/fixtures/expected.json
?? experiments/eu1030/test/fixtures/extra_byte.dat
?? experiments/eu1030/test/fixtures/no_records.dat
?? experiments/eu1030/test/fixtures/truncated.dat
?? experiments/eu1030/test/fixtures/valid.dat
?? experiments/eu1030/test/fixtures/wrong_endian.dat
?? experiments/eu1030/test/makeFixtures.mjs
?? experiments/eu1030/test/runTests.mjs
```
- ADJUDICATION of untracked inventory: matches the historically expected pre-existing untracked set
  (docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ and experiments/). No foreign writer
  active in this package tree. The pre-existing __pycache__ entry under the SLOT17 package is a
  prior-run artifact, NOT produced by this correction run; this run adds zero pycache/pyc.
  Policy: no clean, no sweep, pre-existing untracked paths untouched.

## git worktree list (observed; informational only — worktrees are forbidden reference)
```
D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean                              8a09e45 [master]
D:/Eudoria_Reconstruction/worktrees/PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1 5290e79 [audit/pe935-ninode-slot17-gb-oracle-minicheck-r1]
D:/Eudoria_Reconstruction/worktrees/WORK_AUDIT_REPORTS                          1312f89 [audit/work-audit-reports]
```
- No work-audit branch/worktree was read as canonical evidence, modified, merged or cherry-picked
  by this run. The main worktree only was measured and used.

## S2 SOURCE PIN (independently measured this run, before decoding)
- PATH     = D:\Eudoria_Reconstruction\pcg_install\Entropia.exe
- SIZE     = 8015872
- SHA256   = E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
- PIN CHECK= PASS (size + SHA256 match the contract pin; PE32 i386 / ImageBase 0x00400000 re-verified
  inside every measurement script from the file header bytes — fail-closed before any decode).

## GIT MUTATIONS BY THIS RUN
- ZERO. No commit, no push, no branch, no stage. File work inside the existing canonical package only.

## RUN-END GIT OBSERVATION (correction run end; appended by the same correction run)
- HEAD                  = 8a09e459eb5a930054f35b713afe3e28b6fa5abc (UNCHANGED from run start; == expected BASE)
- origin/master (local) = unchanged; git ls-remote not re-run at end (no push performed; HEAD is the authority for
  the zero-mutation claim and it equals the start-state HEAD)
- git status (package-relative census at run end):
  - modified tracked files inside this package: 24 (AMEND_LOG_R1.md; SCRIPT_SHA256.csv; scripts/census_triple_writes.py;
    scripts/gen_manifest.py; scripts/gen_raw_evidence.py; 01_RAW/{END_TO_END_VALUE_FLOW_RAW, FALLBACK_PRIMARY_COMPARISON,
    FUN_00437F70_DISASM, FUN_0050A050_DOWNSTREAM_DISASM, FUN_0082B5A0_DISASM, HELPER82B5A0_CALLER_CENSUS.txt,
    NEGATIVE_CONTROL_RAW, ORIGIN_TRIPLE_WRITE_CENSUS_RAW, SOURCE_VECTOR_LAYOUT_RAW}; 02_ANALYSIS/{HELPER_OPERATIONS,
    OUTPUT_VALUE_RELATION, POSITION_SEMANTICS, SCIENCE_STATUS_DELTA.csv}; 03_EVIDENCE/{EVIDENCE_INDEX.csv, README.md};
    06_REPORT/{HANDOFF, MANIFEST_SHA256.csv, REPORT, STAGE_ACCEPTANCE_GATES.csv})
  - HELPER437F70_CALLER_CENSUS.csv + HELPER82B5A0_CALLER_CENSUS.csv: regenerated BYTE-IDENTICAL (git sees NO change —
    instrument verification of measurement stability)
  - NEW untracked files inside this package (authorized): 00_CONTROL/PRE_EDIT_R2/** (27 .pre snapshots);
    00_CONTROL/CORRECTION_CONTRACT_ORIGIN_MUTABILITY_R1.md; 00_CONTROL/CORRECTION_EXECUTOR_RETURN.md;
    00_CONTROL/scripts/{sprov.py, probe_origin_setter.py, census_write_through.py, census_setter_reach.py,
    probe_output_formula.py}; 01_RAW/{ORIGIN_SETTER_458D90_DISASM.txt, ORIGIN_SINGLETON_WRITE_THROUGH_CENSUS.csv,
    ORIGIN_SINGLETON_WRITE_THROUGH_RAW.txt, ORIGIN_SETTER_CALLER_CENSUS.csv, ORIGIN_SETTER_REACHABILITY_RAW.txt,
    OUTPUT_FORMULA_REVALIDATION_RAW.txt, CORRECTION_RUN_GIT_OBSERVATION.md(this file)};
    02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md
  - NO new package root created (no docs/audits/PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915/ directory exists)
  - pre-existing untracked paths untouched: docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ and experiments/
  - __pycache__/.pyc inside this package: 0 (all python invocations used -B)
- GIT MUTATIONS BY THIS RUN: ZERO (no commit, no push, no branch, no stage — persistence is a later ordered pass)
