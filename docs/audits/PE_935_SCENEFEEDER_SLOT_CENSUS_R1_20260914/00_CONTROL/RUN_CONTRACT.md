# RUN_CONTRACT.md — PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914

Executor: pe-reconstruction (worker). Principal: PE-MASTER (direct dispatch 2026-09-14).
This file records the binding dispatch contract (verbatim in substance) plus the
input identities this run actually measured. Publication is NOT part of this run
(publisher step is separate, by pe-master-auditor after PE-MASTER adjudication).

## 1. RUN IDENTITY

- RUN_ID: PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914
- AUDIT_OUTPUT_ROOT: `D:\Eudoria_Reconstruction\99_Audits\PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914\`
  (PE-MASTER verified at dispatch: directory did NOT exist — no collision; executor created the
  skeleton: 00_CONTROL, 01_RAW, 02_ANALYSIS, 03_EVIDENCE, 06_REPORT)
- RUN_CLASS: MATERIAL (small census; its output feeds a later model-bridge decision)
- MODE: STATIC-ONLY. The client, Frida, x32dbg, mock-server and any game service were NOT run.
  Engine-execution layer is ABSENT by definition — that absence is never masked with the word
  "oracle".
- BASE_SHA (repo): 6465019298e66856a2fe9fa9750c047d057c97dd. PE-MASTER measured HEAD ==
  origin/master == ls-remote == this value at dispatch. Executor re-measured HEAD, origin/master
  and ls-remote (see §2) — identical; any other value would have been HARD_STOP BASE_DRIFT
  (no reset, no reconcile, report only).
- Physical source: `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` — expected SHA256
  E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, size 8015872, PE32 base
  0x00400000. Executor re-verified with its own fail-closed S0 (hash+size+PE32; mismatch =
  HARD_STOP SOURCE_IDENTITY_FAIL, no downstream).

## 2. THE ONE RESEARCH QUESTION (entire scope)

> Which slots of the SceneFeederObject vtable DIRECTLY read the corrected position stored at
> SF+0x34..0x3C, and what do they do with those values immediately after the read?

Out of scope (explicit): proving SceneFeeder→model; recovering 296445; historical placement,
terrain cells, network/ring/executor, template 4508, new NIFs, runtime, or ANY other subsystem
unless it is a direct one-hop callee of a studied slot.

## 3. KNOWN STARTING POINT (status quo NOT changed by this run)

From the accepted prior run (PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913,
commit 6465019): SceneFeederObject RTTI = `.?AVSceneFeederObject@@`, vtable 0x00A7D458; the
corrected position is copied by FUN_005094C0 from instance+0x44..0x4C to
SceneFeederObject+0x34..0x3C; TRANSFORM_TO_SCENEFEEDER = PROVEN; TRANSFORM_TO_MODEL =
NOT_DEMONSTRATED. This run does NOT change that status.

## 4. EXACT SCOPE — 6 SLOTS

Decode exactly: FUN_0050A460, FUN_005090A0, FUN_005090B0, FUN_0050A050, FUN_005090C0,
FUN_00509580. FIRST verify from the physical EXE bytes that these are actually the
corresponding entries of vtable 0x00A7D458 (read the vtable from .rdata; record each
function's slot INDEX; verify each entry points at the function start; verify the RTTI chain
vtable->COL->TD->name = .?AVSceneFeederObject@@ with the executor's own walk). The map was NOT
taken solely from the prior report.

For EACH slot determine:
1. exact function start;
2. exact function end (derived from own decode: RET/padding evidence, no assumed ends);
3. ALL direct reads/writes of [this+0x30], [this+0x34], [this+0x38], [this+0x3C];
4. whether the function: does not touch these fields / reads the +0x30 link / reads X/Y/Z /
   writes X/Y/Z / takes the structure address / copies values to local/stack/register;
5. if X/Y/Z flows directly into a CALL: the CALL VA, the target, which components are
   arguments, what the receiver is, and the minimal dataflow up to that CALL only.

## 5. DATAFLOW STOP RULE

STOP the dataflow at the FIRST CALL. Do not descend into callees. Only a short one-hop check is
allowed to resolve: the real target of a thunk, the RTTI of a receiver, or a trivially obvious
getter/setter. If a callee would need more RE: mark NEXT_SEAM = <function> and do NOT study it
in this run.

## 6. MANDATORY CENSUS TABLE

Exactly one CSV: `02_ANALYSIS/SCENEFEEDER_SLOT_CENSUS.csv` with columns (exactly these, in
order): slot_index, function_va, function_name, body_start, body_end, reads_sf30, reads_sf34,
reads_sf38, reads_sf3c, writes_sf34, writes_sf38, writes_sf3c, takes_position_address,
position_to_call, call_va, call_target, receiver, classification, evidence_ref.
classification may ONLY take: NO_RELEVANT_ACCESS / LINK_ONLY / POSITION_READ_LOCAL /
POSITION_TO_CALL / POSITION_WRITE / MIXED / UNRESOLVED. The table MUST contain 6/6 slots,
each with a disposition; report-only-interesting-slots is FORBIDDEN. A slot that does not read
the position is a fully valid NEGATIVE result.

## 7. GATES (06_REPORT/STAGE_ACCEPTANCE_GATES.csv; PASS/FAIL + boundary column)

- G1-SOURCE: PASS only if EXE SHA + size + PE32 all match (executor's own measurement).
- G2-VTABLE: PASS only if SceneFeederObject identity confirmed, vtable 0x00A7D458 confirmed,
  and the six studied entries derived from the physical vtable (not copied from a prior report).
- G3-COMPLETE-SLOT-CENSUS: PASS only if the table has 6/6 slots each with a disposition.
- G4-POSITION-ACCESS: for every slot that reads +0x34/+0x38/+0x3C show raw instruction
  evidence; a negative slot result is a fully valid result.
- G5-ONE-HOP-FLOW: if a slot passes the position into a CALL, prove only: SF position ->
  argument/register/stack -> CALL target. Do NOT declare MODEL / NiAVObject /
  ArkModelResourceInstanceRef / TRANSFORM_TO_MODEL on this basis unless the CALL site itself
  carries direct, independent RTTI/vtable identification visible WITHOUT new major RE. Even
  then the maximum outcome for this run is CANDIDATE_MODEL_BRIDGE, never CONFIRMED.

## 8. POSITIVE CONTROL (mandatory)

Re-decode the small window in FUN_005094C0 and confirm the copy instance+0x44..0x4C ->
SF+0x34..0x3C (expected byte pattern — re-derived, not trusted:
8B 44 24 04; 8B 10; 89 51 34; 8B 50 04; 89 51 38; 8B 40 08; 89 41 3C; C6 41 28 01; C2 04 00).
If the positive control fails: RUN_INVALID — stop and report. (Executor note: the window
itself proves [arg+0/4/8] -> [this+0x34/38/3C]; the "instance+0x44" arg identity is prior-run,
caller-side knowledge, not re-derived here and not needed for control validation.)

## 9. FINAL STATUS (exactly one)

A: at least one slot POSITION_TO_CALL -> give NEXT_SEAM = exactly ONE most direct call target,
   and finish.
B: a slot reads the position but does not send it to a CALL (POSITION_READ_LOCAL) -> finish and
   give exactly one next test.
C: none of the six slots reads the position -> NEGATIVE_SLOT_CLOSURE (do not auto-search the
   next path).
D: not all six slots completely decodable -> PARTIAL/UNRESOLVED; do not widen the scope.

## 10. EVIDENCE PACKAGE (small: ~12-20 files)

Required: 00_CONTROL/RUN_CONTRACT.md (this file) + SOURCE_IDENTITIES.json;
01_RAW/VTABLE_AND_SLOTS.txt (physical vtable dump + slot-index mapping + RTTI chain);
01_RAW/SLOT_DISASSEMBLY.txt (full disassembly of all 6 slot bodies — primary evidence);
01_RAW/POSITIVE_CONTROL_005094C0.txt; 02_ANALYSIS/SCENEFEEDER_SLOT_CENSUS.csv;
02_ANALYSIS/ONE_HOP_FLOW.md; 03_EVIDENCE/README.md; 06_REPORT/REPORT.md; 06_REPORT/HANDOFF.md;
06_REPORT/STAGE_ACCEPTANCE_GATES.csv; 06_REPORT/MANIFEST_SHA256.csv (every file, SHA256, no
self-row, zero missing, zero duplicate paths). Extra files only if genuinely needed for
reproduction (scripts + SCRIPT_SHA256.csv).

## 11. DISCIPLINE (binding)

- Fresh decodes from the physical EXE only (own PE parser + capstone; run-local tooling pattern
  adapted from the R1 package's 00_Control; no script copied verbatim — independent
  implementation, both hashed here).
- Layer separation in every claim: original bytes / disassembly / decompile (none needed) /
  hypothesis / synthetic (none) / engine execution (ABSENT).
- No mutation of anything outside AUDIT_OUTPUT_ROOT; originals read-only; the repo is read-only
  for the executor (zero git MUTATIONS; read-only identity measurements only: rev-parse HEAD,
  origin/master, ls-remote, status); foreign experiments untouched; historical packages
  untouched.
- If interrupted: save a RESUME_POINT on disk and return.

## §INPUT_IDENTITIES — what this run actually read (SHA256 / measured values)

| Input | Measured identity |
|---|---|
| `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` | SHA256 e7785430e81dffe648ce8f5312414b17bc9fce61389689a22f753765d5280f31 (lowercase of contract pin), size 8015872, machine 0x014C (i386), opt_magic 0x010B (PE32), image_base 0x00400000, entry_rva 0x0055DA11. Read-only. |
| Repo `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean` | HEAD = 6465019298e66856a2fe9fa9750c047d057c97dd; origin/master = same; `git ls-remote origin master` = same. Dirty set measured: only untracked `experiments/` (foreign, untouched). Zero git mutations performed. |
| R1 pattern reference (read only, not copied) | `99_Audits\PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913\00_Control\pe935_core.py` + `decode_dump.py` were READ as a tooling pattern; this run's scripts are an independent implementation (sf_core.py et al.), hashed in 00_CONTROL/SCRIPT_SHA256.csv. |
| Toolchain (measured at run time) | `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe` = Python 3.12.7; capstone 5.0.7 (capstone.__version__); CS_ARCH_X86 / CS_MODE_32, detail=True. |

## §EXECUTION LOG (this run, in order)

1. BASE_SHA + dirty-path measurement (read-only git): PASS, no drift.
2. EXE hash/size measurement: PASS. Skeleton created.
3. s1_vtable_slots.py: S0 fail-closed PASS; RTTI walk (own): vtable-4 @ 0x00A7D454 -> COL
   0x00AA12B8 (sig=0, offset=0, TD=0x00B78834, CHD=0x00AA12CC) -> TD name
   `.?AVSceneFeederObject@@` = PASS. Physical vtable: exactly 6 slots (0..5); the six contract
   functions ARE the complete vtable (slots 0,1,2,3,4,5 in the listed order: 0x50A460, 0x5090A0,
   0x5090B0, 0x50A050, 0x5090C0, 0x509580). Slot 6 would read ASCII "dPVS" data (0x53565064,
   not a code pointer) — vtable extent ends at slot 5.
4. s2_slot_disasm.py: full capstone decode of all six bodies; body ends derived by
   padding/next-entry/terminal evidence (slot 0 initially over-swept past a 2-byte CC pad into
   the adjacent function 0x50A480 — detection rule fixed to alignment-completing CC runs and
   re-run; all six boundaries then validated by independent function-start evidence: 0x50A480
   has its own 2 E8 callers, 0x50A0B0 has 1 E8 caller + 2 E9 jumpers, 0x5095A0 has 1 E8
   caller).
5. One-hop identification (stop rule honored): 0x0095D42A = FF 25 import thunk ->
   MSVCR80.dll.??3@YAXPAX@Z (operator delete) via own import-table walk; 0x50A240 (dtor body
   candidate), 0x437F70, 0x82B5A0, 0x4150F0, 0x8B71D0 = real functions (prologues + caller
   counts recorded), NOT decoded further.
6. s3_positive_control.py: FUN_005094C0 window — byte-exact match to the contract-expected
   pattern + 9/9 semantic checks = PASS.
7. Analysis + report package written (02_ANALYSIS, 06_REPORT).

## §HARD_STOPS (armed, none triggered)

- BASE_DRIFT (BASE_SHA mismatch) — NOT TRIGGERED (HEAD == origin/master == ls-remote == pin).
- SOURCE_IDENTITY_FAIL (EXE hash/size/PE32 mismatch) — NOT TRIGGERED (all measured equal).
- RUN_INVALID (positive control fail) — NOT TRIGGERED (byte-exact + semantic PASS).
