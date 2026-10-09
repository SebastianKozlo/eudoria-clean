# EVIDENCE_INDEX — PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009

- Package root: docs/audits/PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009/
- This index is self-excluded (a file cannot contain its own SHA256).
- SCRATCH_ROOT (D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009\SCRATCH\)
  is local-only, NOT part of the package; its script/data hashes are recorded here for toolchain provenance.
- **AMENDMENT (records-correction round 2026-10-09)**: the eight package files edited by that
  round (BODY_END_ANALYSIS.json, SELF_CHECK.json, CALLEE_FIELD_ACCESS_CENSUS.json,
  CALL_EDGE_PROVENANCE.json, FALSIFIER_RESULTS.json, FINAL_REPORT.md, HANDOFF.md,
  POINTER_DATAFLOW.json) have their rows re-hashed to the POST-correction state; every
  old->new change with pre/post SHA256 is in AMEND_LOG.md. Files added AFTER package
  assembly are intentionally NOT indexed: QC_RESULTS.json + QC_REPORT.md (created by the
  internal QC, not by the executor run) and AMEND_LOG.md (the correction log itself —
  indexing it would create a hash circularity because it records this index's
  post-correction SHA256).

## Package files

```
a6e9428631f8ac970051c37e0a1fabf82cc38b3dc4ff37fb5c19bf016a1db68c      5996  01_RAW/BODY_END_ANALYSIS.json
709852263a18b3b1315fd893931604295b44db201d69706a50fcd6f035bc74c9      1754  01_RAW/F8_BODY_CROSSCHECK.json
c4e8d1fc1067b81868ccae7852f4461816b2d0284bf8f02694c14e4c6014eb2d     57351  01_RAW/GHIDRA_HYPOTHESIS_EXPORT.json
2f62a19cd94c2b680f979fa6f930d782788bd451731a6c7440b505f9ce4957e0     16968  01_RAW/KEY_REGION_LISTINGS.md
44df3b18c9b9e469e127d4c29db6b53f7201acbda4dadb3f1514ea850668699b     22615  01_RAW/OBJDUMP_LISTINGS/objdump_W_A_FUN_00511070.txt
f74008cc4f28c8b93e2654e57394c3556f349ea349e70fa09d68dca308f082b9     10121  01_RAW/OBJDUMP_LISTINGS/objdump_W_B_FUN_006C3F50.txt
396f503789955d325c6149c0731079c029b577f41755bd80d9394e6ee0fb5355     72031  01_RAW/OBJDUMP_LISTINGS/objdump_W_C_FUN_007CE1E0.txt
d43e59e5028679b17b058c3ae66d7d99e8efb5f9acbcc4706db5d908c2ef96e0     70705  01_RAW/OBJDUMP_LISTINGS/objdump_W_D_FUN_0040B070.txt
19abfad50b0e6876b23226e74073f206af191fc1d2e58edb38cd4e6a3dfc60b3      2826  01_RAW/OBJDUMP_LISTINGS/objdump_W_E1_FUN_0072F580.txt
17c1f3bbeb0ba0f13ae0f31306f06315098a6ade669ff22e1fc72a66c13e232c      3809  01_RAW/OBJDUMP_LISTINGS/objdump_W_E2_FUN_0043A550.txt
612b606bf827d6acc5b37f6748bff99dc9bf13a13cc25516d3cafc9ffed9d177   1780108  01_RAW/OWN_DECODER_WINDOWS.json
34fd1d286dca76697cc7bf7029dbe22a3d75b37e6b36cf0f7e1c00c41b91317c      7382  01_RAW/PHASE0_INPUT_IDENTITIES_RAW.json
41fd98f1355e18b088502659a846a5b687b21686b803f19bc011672d45399710      2304  01_RAW/SELF_CHECK.json
5fc76e061a912fc09cd881beb189325a64489cfe5e464f72bab704e510771c04       521  01_RAW/SENTINEL_00BA5800_DUMP.json
2faa18eb52ade9def32b7d14270c0358f023dfb03ccd85c44d28fcd3442e6877     24683  CALLEE_FIELD_ACCESS_CENSUS.json
0bc4d020bd54b14559e51279876db383d5feb48e2bae5068eb065ddb0773f652      6465  CALL_EDGE_PROVENANCE.json
cd809aa004c2bea73c3a0a1780f25bbbf514784a46302beb5e1160ed0bdf4f4e     11885  FALSIFIER_RESULTS.json
b695c2cda3140c55f390a18f295c4190f7823af1426e69be7f3df5d76601af29     18362  FINAL_REPORT.md
f02836c747bdc17f04248de8beaf14283ae9eb9e6626e8d8185e1c33181541bd     12825  HANDOFF.md
b3512d100802a768da038a6fabc3897ca1048152da3f7fe61f8d5567ce5e8f08      5618  INPUT_IDENTITIES.json
6d8d8e517b549c68d1fc9d1e3b1139d8ea48343a410b5bca60d52de9a50d1e6d     15977  POINTER_DATAFLOW.json
c50eb1e451c3ff4376714d70ca40e55dc6bb796fad8591bee8990047df7eb400     14967  PREREGISTRATION.md
```

## SCRATCH scripts (toolchain provenance; all invoked with python -B)

```
f29e08952238dfcf0642d773df825989a36d707779373331cc28339ad6c161f3      8056  assemble_package.py
d54f48a6c571ec882712668dcc8d411e96a9042818dd8e562b6a2b014ea0952b      6193  body_end_analysis.py
029d94aaf192efe77ee8e38704ea6e468ffe08e7bcecd7b7f80be40abd29b93d      4106  crosscheck2.py
9099445f1aeff3beed95eb270a53e100ea7965332aa7d7ad35e9602a20799bbc      3242  crosscheck_objdump.py
b39e1c4fc30bec8cd8864fd8d291e157efa80d4bf3369c943816961c7773e9c2       871  dump_bodies.py
4508458fc193961d4ee07339c6c496e0d1496b0730cb8e624b19d9d55fc64cba      1610  dump_bodies2.py
ed466d2bfdd4afe8b46b1d1a46d38aa8edda18ea5865f8c26929546605533264      3309  final_identity_checks.py
53a987cef42ccaea7217ce0ab542f772506f74438c10f47f3525d1710d5f80a3      6422  gen_evidence_index.py
e87c289a47d9ba93523ccd54c2b7586038e3ffb578c267bf1903417fa3898324      2918  ghidra_export_fwd.py
964845b4d328affe3fda530353e6251f2122c9f2fb025a774fa8ebd854233d6d      4639  phase0_input_identities.py
99b2ad2f44ecdb88ad21f1945eb59916bb0547d786afe116b3e92e2ff226441a      4745  run_windows.py
92b1bb9c6ec000ddea11f51a83082a8d2781d280ef3f85dcb882c295125aa07f      8767  selfcheck.py
5fb54797c57580f7aaebeb29a12404bd37e0085fa8c48376a1330c57d133254b     32826  x86probe.py
```

## SCRATCH other intermediate files (local-only; slices/listings/JSONs)

```
947603d7b95a4e43890ef88bb31b505f8199d216bc236a5e1741370c2853c808      5084  body_end_analysis.json
709852263a18b3b1315fd893931604295b44db201d69706a50fcd6f035bc74c9      1754  f8_body_crosscheck.json
76a18290c907486e2ca06ea458616752f7670cc1ad0381065737484bd7cd2f89     14202  f8_boundary_crosscheck.json
df77466fb18293966ef034f9e9da96714c6e0031a8b688e9497e85a7d9233525      1153  final_identity_checks.json
6020991e417b1626d6e127056b33fe50bc66ef316b67092b293f935ea486f919     59677  ghidra_hypothesis_export.json
44df3b18c9b9e469e127d4c29db6b53f7201acbda4dadb3f1514ea850668699b     22615  objdump_W_A_FUN_00511070.txt
f74008cc4f28c8b93e2654e57394c3556f349ea349e70fa09d68dca308f082b9     10121  objdump_W_B_FUN_006C3F50.txt
396f503789955d325c6149c0731079c029b577f41755bd80d9394e6ee0fb5355     72031  objdump_W_C_FUN_007CE1E0.txt
d43e59e5028679b17b058c3ae66d7d99e8efb5f9acbcc4706db5d908c2ef96e0     70705  objdump_W_D_FUN_0040B070.txt
19abfad50b0e6876b23226e74073f206af191fc1d2e58edb38cd4e6a3dfc60b3      2826  objdump_W_E1_FUN_0072F580.txt
17c1f3bbeb0ba0f13ae0f31306f06315098a6ade669ff22e1fc72a66c13e232c      3809  objdump_W_E2_FUN_0043A550.txt
7da6496b88c11d57e10878ec78873dee5196b9ee055bd07a4b745cf9c4689d6f      2336  package_listing_stage1.json
34fd1d286dca76697cc7bf7029dbe22a3d75b37e6b36cf0f7e1c00c41b91317c      7382  phase0_input_identities.json
f77563d1ba5d9307d413b2d7f866daf19b45e495611366b6e3093e06944e8c84       463  selfcheck.json
fc608f8b2118a6c8088ae664b8760ded8de5f263599862a338e4a87e26abb2e2      1536  slice_W_A_FUN_00511070.bin
aeaf4c6636150e3877e319b90cde01125a6a48d9d9c7869bb254e98e310d8928       512  slice_W_B_FUN_006C3F50.bin
2e2bb46462eb7977c9498d665ead8ce61038bea09cee0fd319ce265236a95d28      4096  slice_W_C_FUN_007CE1E0.bin
21471ff5e66b0cc8a5678f0bfe44d98a5734112f75736a73e733e82d67039524      4096  slice_W_D_FUN_0040B070.bin
b879408575b81099313400605c719100ccb98c61c0ad911f73bbd173c253d509       128  slice_W_E1_FUN_0072F580.bin
a734c82b0958e7a45b1c639405dfaed47d86df309d0990dab268a57acd3fb9b9       192  slice_W_E2_FUN_0043A550.bin
374708fff7719dd5979ec875d56cd2286f6d3cf7ec317a3b25632aab28ec37bb        16  slice_W_F_SENTINEL_00BA5800.bin
612b606bf827d6acc5b37f6748bff99dc9bf13a13cc25516d3cafc9ffed9d177   1780108  windows_own_decode.json
```

## SCRATCH intermediate data subfolder (local-only)

```
947603d7b95a4e43890ef88bb31b505f8199d216bc236a5e1741370c2853c808      5084  body_end_analysis.json
709852263a18b3b1315fd893931604295b44db201d69706a50fcd6f035bc74c9      1754  f8_body_crosscheck.json
76a18290c907486e2ca06ea458616752f7670cc1ad0381065737484bd7cd2f89     14202  f8_boundary_crosscheck.json
df77466fb18293966ef034f9e9da96714c6e0031a8b688e9497e85a7d9233525      1153  final_identity_checks.json
6020991e417b1626d6e127056b33fe50bc66ef316b67092b293f935ea486f919     59677  ghidra_hypothesis_export.json
7da6496b88c11d57e10878ec78873dee5196b9ee055bd07a4b745cf9c4689d6f      2336  package_listing_stage1.json
34fd1d286dca76697cc7bf7029dbe22a3d75b37e6b36cf0f7e1c00c41b91317c      7382  phase0_input_identities.json
612b606bf827d6acc5b37f6748bff99dc9bf13a13cc25516d3cafc9ffed9d177   1780108  windows_own_decode.json
```

## Evidence roles

| Artifact | Role |
|---|---|
| PREREGISTRATION.md | written BEFORE all science; windows/budgets/falsifiers pre-registered |
| INPUT_IDENTITIES.json | EXE before/after hashes, PE layout, git census, predecessor verify, toolchain identities |
| CALL_EDGE_PROVENANCE.json | every subject + anchor callsite: bytes, recomputed rel32 targets, preceding instruction |
| POINTER_DATAFLOW.json | per-edge register traces, sentinel/NULL cases, anchor body pinning, classifications |
| CALLEE_FIELD_ACCESS_CENSUS.json | 4 direct template-memory rows + 7 store/forward rows + 11 rejection classes + corrected machine-classifier rules + 135-operand census-completeness revalidation (records correction 2026-10-09, AMEND_LOG.md) |
| FALSIFIER_RESULTS.json | 8/8 falsifiers with MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED |
| FINAL_REPORT.md | the science report (this run's conclusions + honest NOT_CHECKED list) |
| HANDOFF.md | the mandatory handoff block |
| 01_RAW/OWN_DECODER_WINDOWS.json | own decoder output over all 7 windows (incl. W_F sentinel dump) |
| 01_RAW/BODY_END_ANALYSIS.json | pre-registered body-end rule application per window (flow-reachable RETs, padding runs) |
| 01_RAW/F8_BODY_CROSSCHECK.json | dual-decoder agreement: 451 instructions, 0 boundary, 0 call-target disagreements |
| 01_RAW/KEY_REGION_LISTINGS.md | dual-verified listings of every decision-relevant region |
| 01_RAW/SENTINEL_00BA5800_DUMP.json | sentinel VA mapping + 16 static zero bytes |
| 01_RAW/OBJDUMP_LISTINGS/*.txt | independent GNU objdump 2.44 disassembly of all 6 code windows (physical EXE slices) |
| 01_RAW/GHIDRA_HYPOTHESIS_EXPORT.json | Ghidra decompile/listing of the 6 windows — HYPOTHESIS ONLY, not identity evidence |
| 01_RAW/PHASE0_INPUT_IDENTITIES_RAW.json | machine-measured preflight (git/EXE/package/toolchain) |

## External inputs (read-only, unchanged)

| Input | Verification |
|---|---|
| Entropia.exe (physical) | SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 before AND after, 8015872 B |
| Ghidra sandbox Entropia.exe (LANDMARK4057 project import) | re-hashed this run == physical == expected |
| Predecessor package PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009 | 25/25 package rows re-hashed before AND after against its MANIFEST_SHA256.csv, 0 mismatches |
| Git BASE cea10e9cfcaa2e814f5cfe4269fd2a6a409d54da | HEAD == origin/master == live ls-remote, re-checked before and after |
