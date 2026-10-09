# EVIDENCE INDEX — PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009

All evidence is STATIC_ONLY. Package root:
`D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009\`

## 1. Provenance chain (how each artifact was produced)

1. **PREREGISTRATION.md** — written BEFORE any science (question, gates, budgets,
   window rules, expected census classes). No measurement existed when it was
   written.
2. **s1_repin_raw_census.py** (pure Python 3.12, `python -B`) — own PE mapper
   (calibrated on two canon byte anchors: string "Parameters\templates.vfs"
   @0x00A86D30 → off 6,843,696; PUSH 0x3ED3 bytes @0x005B6597) → subject head
   byte pins, DAT_00BA1824 .data location mapping, raw E8/E9 rel32 scans of
   .text, whole-file absolute 4-byte-LE VA scans → `01_RAW\S1_REPIN_RAW_CENSUS.json`.
   Measured/interpreted separated; pin_provenance recorded inside the artifact.
3. **c2_ghidra_census.py** (Jython 2.7, Ghidra 11.2.1 headless postscript on the
   REUSED project LANDMARK4057, `-noanalysis`) — subject function listings +
   decompiles (declared re-pin windows W-SUBJ-1/2/3), ALL getReferencesTo dumps,
   datum refs, per-candidate Ghidra state, 12 caller windows (listings +
   decompiles + callsites + body-end contexts) → `01_RAW\C2_*` artifacts.
4. **s3_curate_census.py** (pure Python, `python -B`) — merges s1+c2 into the
   package: agreement tables, id-table dumps (fresh EXE byte reads), callsite
   context slices, and the master `CALLER_CENSUS.json` including the analysis
   layer (id-source classes, role classes with byte anchors — derived from the
   byte-anchored listings in the window files).

## 2. Script identities (hash-after-final-edit-before-execution discipline)

| Script | Location (SCRATCH, local-only) | SHA256 |
|---|---|---|
| s1_repin_raw_census.py | `99_Audits\PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009\SCRATCH\scripts\` | `05F61A5CB7E3A08F1BAE291B904B0C4986C0868B83DF9DE9F29BB8BC8F9B057C` |
| c2_ghidra_census.py (EXECUTED version) | same dir | `D073EC73994FA3B2A64898CFA6482CFF4FFBBB111203893C63D59E009AD16091` |
| c2 first-draft (FAILED run: Jython `Data.hasValue()` overload quirk; output discarded) | same dir, superseded in place | pre-fix hash `0D427663B9AF18657A870955E79B6916449A8B07A194AF4B1D50393D07974166` (disclosed; failed run logged at `SCRATCH\logs\analyzeHeadless_c2_log.txt` — overwritten by the successful run) |
| s3_curate_census.py | same dir | `6CDAC100BD9584ADD89C1C47374BC2E8DC210488DD990F0E41E15D4AF55952FD` |

Ghidra invocation (successful run):
`D:\ghidra_11.2.1_PUBLIC\support\analyzeHeadless.bat D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003\proj LANDMARK4057 -process Entropia.exe -noanalysis -postScript c2_ghidra_census.py -scriptPath <SCRATCH\scripts>`
Log: `SCRATCH\logs\analyzeHeadless_c2_log.txt`.

## 3. Package file hashes (SHA256, computed after final write)

```
EC4E70E91E83FDBE35117F1CE632B0079ADA5E5573C88CCEFAB8FBC0C07A676B  01_RAW\C2_CALLER_WINDOWS\c2_caller_00_00511070.json
06C7B5451E31E68A8F4D720C4AD1D93E112723899AD7F38030836536DA78344C  01_RAW\C2_CALLER_WINDOWS\c2_caller_01_006BAA20.json
86821A5B2B5D9C52426AA9B8775CC531B1A1F324AC448678FE7092A8E987BC98  01_RAW\C2_CALLER_WINDOWS\c2_caller_02_00733490.json
0B4B50B0FBD5043519D7BD80D2F13561ACDDA0D6135639C2A59F91EEF8EBDF57  01_RAW\C2_CALLER_WINDOWS\c2_caller_03_006C26B0.json
108637923A1A320075C6BA224FB8A8657ADBCA719F5A2EA693AD6172E5585A80  01_RAW\C2_CALLER_WINDOWS\c2_caller_04_006C2700.json
C7E8252BF975B0D0E92C8AD279BAC1CD6AA66E4CF90472977BF2A3BE77D7EAFD  01_RAW\C2_CALLER_WINDOWS\c2_caller_05_006C2750.json
C98E0DFB7C136BD6AB25F7A6B2444FAA81EC0A0D4E101347CA4143DA14D6FF57  01_RAW\C2_CALLER_WINDOWS\c2_caller_06_006C27A0.json
F49D373D9959E004E9C45C13625B660190A90DA39EAB0F5C85821B9EAC4E5F38  01_RAW\C2_CALLER_WINDOWS\c2_caller_07_006C27F0.json
5BEA8E87F93448E370B1C2F1D708174325C58326107D3919498E0ECCF3BE7BB6  01_RAW\C2_CALLER_WINDOWS\c2_caller_08_006C3F50.json
0CA97C90339C96E74FEB26D28E7BDE58B1192DED9F4F444F9CEEE749457B0B62  01_RAW\C2_CALLER_WINDOWS\c2_caller_09_00567170.json
128C1E64B3DF4EEA1A3A49F4F8D4C1976ADED1C6BAD022D95823B05475752E71  01_RAW\C2_CALLER_WINDOWS\c2_caller_10_006C2840.json
4EDE380B99BC43D50A3A828E4398C78FA3E3DF17750D24B8757012C1BF004299  01_RAW\C2_CALLER_WINDOWS\c2_caller_11_006C2870.json
6DF2502A83AD447F89B73AF1582EA74FFDB56B137E7ECFC78A2C1A112504F5D7  01_RAW\C2_SUBJECT_REPINS.json
076CEC6F45E5FABA38FC8C179C8E99F4381475D29BD8FFF31E0A9134D3F15D39  01_RAW\CALLSITE_CONTEXTS.json
89D2DF758484BD509A5714E38D8EF7334CE0735F2A8C1B1997F0FD4E69FA13F8  01_RAW\CENSUS_AGREEMENT.json
9698AEB22B610594A89C1005B29CB08A0CEC9FD132C0FDD7A3E0D3BDE30E6710  01_RAW\ID_TABLE_DUMPS.json
ED5B165A5B1C8C3862B66899B4CC77BB6129697BCBC0C70A51543632DDCFECBC  01_RAW\S1_REPIN_RAW_CENSUS.json
82D5A71F487C7F789930DA2FDDD063E7CA0625D762302BB48BDCCDE651011A97  CALLER_CENSUS.json
505E793E0F638DB72F45D2DB7DAC0F4D3FAB5AC9986245F17591C0416A8100FD  FINAL_REPORT.md
E03BB125BC7D296EF5D0FECB5A610C15C311F96A9FC3CE2A3F2B7790D9C99FDF  HANDOFF.md
983AA2E8C51AA19EEBE9799746923A0F50F198DD70BBB9331A42B98D43D84398  PREREGISTRATION.md
```

Hash refresh (records-correction round R1, 2026-10-09, pre-persistence, per the
internal QC findings ledger): the SHA256 values above for `01_RAW\ID_TABLE_DUMPS.json`,
`CALLER_CENSUS.json`, `FINAL_REPORT.md` and `HANDOFF.md` were re-computed AFTER the
in-place records corrections (F-QC-1..F-QC-10; every change old→new, reason and
pre/post hash recorded in `AMEND_LOG.md` in this package root). All other values
are unchanged from the run's final write. `AMEND_LOG.md` itself was created by the
correction round; its hash is not self-recorded here (the persistence-phase MANIFEST
covers it).

## 4. What each package file evidences

- `PREREGISTRATION.md` — pre-science registration (gates, budgets, window rules).
- `CALLER_CENSUS.json` — master census: per-reference-class method+result for both
  functions; per-caller records (12 classified with 4-tuples + byte anchors;
  20 IDENTIFIED_NOT_ANALYZED with callsites); datum census; question answers;
  budget ledger; self-check.
- `01_RAW\S1_REPIN_RAW_CENSUS.json` — EXE identity + PE header + mapper
  calibrations; subject head byte pins; DAT_00BA1824 zero-init-tail mapping;
  raw E8/E9 candidate scans (25/0 and 35/0); whole-file absolute VA scans
  (0/0/3).
- `01_RAW\C2_SUBJECT_REPINS.json` — FUN_0072F580 + FUN_0043A550 full listings
  (byte-anchored per instruction) + decompiles + ALL references; DAT_00BA1824
  refs + Ghidra data state; s1 head pins; interpreted role re-pins.
- `01_RAW\CENSUS_AGREEMENT.json` — dual-method agreement: raw↔Ghidra VA sets
  identical for both functions; datum operand↔instruction pair mapping; all
  candidates defined instructions.
- `01_RAW\C2_CALLER_WINDOWS\c2_caller_XX_<ENTRY>.json` — 12 windows, each:
  full listing (bytes + text), decompile, callsites to targets, all CALL edges
  in-window (callee edges only — bodies CLOSED), body-end context (RET-class +
  next-prologue adjacency).
- `01_RAW\CALLSITE_CONTEXTS.json` — ±22/±14 instruction byte-anchored context
  slices around every getter/lookup callsite of the 12 windows.
- `01_RAW\ID_TABLE_DUMPS.json` — measured .rdata id-table dwords for the 7
  accessor tables (with EXE SHA256 re-measured at dump time).

## 5. Identity verification record (G3)

- EXE SHA256 BEFORE (pre-work, measured by PowerShell Get-FileHash):
  `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` (8,015,872 B) —
  matches expected. Re-measured by s1 (Python hashlib): same. EXE SHA256 AFTER
  (post-work): same. Unchanged.
- Historical landmark package
  (`PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003`): 84/84 files
  SHA256-verified BEFORE work (baseline: `SCRATCH\..\HISTORICAL_BASELINE_BEFORE.txt`)
  and re-verified AFTER: byte-identical (0 mismatches).
- Reused Ghidra scratch sandbox EXE
  (`99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003\Entropia.exe`): SHA256
  verified before AND after = expected. Unchanged.
- `.pyc` residue created by this run: 0 in run scratch, 0 in package, 0 in
  historical package (all `python` invocations used `-B`). The repo tree (cwd)
  contains pre-existing foreign untracked .pyc/__pycache__ artifacts that
  predate this run (none created by it) — out of scope of this claim.
- AUDIT_ENTRYPOINT.md: does not exist at `docs\audits\AUDIT_ENTRYPOINT.md`; never
  created, never touched by this run.

## 6. SCRATCH (local-only, NOT part of the package)

`D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009\`
- `SCRATCH\scripts\` — the three scripts (hashes above).
- `SCRATCH\logs\analyzeHeadless_c2_log.txt` — Ghidra run log (the failed first
  attempt was overwritten by the successful run's log; both behaviors disclosed).
- `SCRATCH\ghidra_out\` — raw c2 outputs (census + 12 window files).
- `SCRATCH\01_RAW\S1_REPIN_RAW_CENSUS.json` — s1 working copy (byte-identical to
  the package copy).
- `HISTORICAL_BASELINE_BEFORE.txt` — 84-file baseline of the prior landmark
  package (hash lines), captured before any work.
