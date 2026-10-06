# INPUT_IDENTITIES — PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006

## Pinned inputs (verified this run, fail-closed)

| Input | Identity | Verification |
|---|---|---|
| Contract file | `C:\Users\User\Documents\ChatGPT\PE\PE_935_INSTANCE_RESOURCE_MICRORUN_PROMPT_REVIEW_20261005\OPENCODE_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006.md` | SIZE 11,823 B; SHA256 `57A731683EE32E6FC43CCEC42664B03D4DC7FBA2138009B8BF7A0A8E634BABB6` — MATCH (read from disk before any work; contract not modified) |
| EXE (target) | `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` | 8,015,872 B; SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` — MATCH (verified at preflight, at QC time, and re-read by every instrument) |
| PE header ground truth | image_base 0x00400000; ASLR OFF; Machine 0x014C; PE32 magic 0x10B; .text VA 0x00401000..0x00A75000 (raw_size 0x674000) | own PE walk (03_SCRIPTS/pe935_core.py), fail-closed asserts |
| Repo | `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean` (SebastianKozlo/eudoria-clean, master) | LOCAL_HEAD == origin/master == actual remote master == `3921dbe2a43a9181f8a50fa5242d8586c85896b6` (ls-remote query 2026-10-05 23:53:49, exit 0); no relevant tracked changes; foreign untracked paths untouched |
| Human instruction | direct message in the OpenCode PE-MASTER session, received after publication of commit 3921dbe... | saved VERBATIM with source/time in GOVERNANCE_DECISION.md BEFORE science (file write time 2026-10-05 23:54:05.874, re-measured in 01_RAW/GovernanceWriteTime.txt) |

## Tools (with identity metadata)

| Tool | Version/Identity | Role |
|---|---|---|
| Own PE walk + byte readers | 03_SCRIPTS/pe935_core.py (run-local, this package) | EXE identity, VA→offset, byte windows, census |
| Ghidra headless | 11.2.1 PUBLIC (`D:\ghidra_11.2.1_PUBLIC\support\analyzeHeadless.bat`), x86:LE:32:default:windows | INDEPENDENT tool: instruction-start verification of all 6 E8 candidates, reference census, bounded decompiles of the 5 budgeted functions (postscript 03_SCRIPTS/ghidra_post.py, SHA256 after final edit `38FBCFBE2ADB79F0E11C66B9254B8BBE5E116BF170D7FC4AD2CBD401348E4800`, hashed 2026-10-05 23:57:33 BEFORE launch) |
| Ghidra sandbox | `C:\Users\User\AppData\Local\Temp\opencode\PE935K_GHIDRA\` (sandbox COPY of the EXE, SHA256 re-verified == pin; fresh project PE935K; run 2026-10-05 23:57:40..00:04:04, exit 0) | the original EXE is never imported/modified; outputs copied to 01_RAW |
| RTTI walker | 03_SCRIPTS/rtti_probes.py (run-local) | MSVC RTTI chains; calibration fail-closed on 3 BASE-canon vtables BEFORE any new probe |
| capstone / objdump | NOT USED (capstone not installed on this host; objdump not in PATH) | disclosed absence — no claim in this package depends on them |

## BASE evidence read AS INPUT (not extended by this run)

Per contract §2, the following BASE paths were READ as input; their claims were NOT
treated as unconditional proof for this run's edges and were re-derived where used:

| Path (relative to docs/audits/) | What was taken as input |
|---|---|
| PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913/06_REPORT/REPORT.md (+ ERRATA_R5) | the ctor chain FUN_00528E50 / FUN_0085B1B0 field layout (+0x74 = record[0] key via FUN_004123D0; +0x78; +0x44..0x4C position; +0x88 param-set id), FUN_005247C0/FUN_00509330 creation chain summary, FUN_00856190 insert summary, the +0xC0 = SceneFeeder pointer claim |
| PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/06_REPORT/REPORT.md (+ PE_MASTER_REVIEW_R2.md and supersessions) | SF ctor = FUN_00509330 (vtable 0x00A7D458), SF+0x30 = refcounted NiNode (0x118 B, FUN_007B6000, refcount @+4), SF+0x30 link identity `.?AVNiNode@@`, FUN_005247C0 ctor callers, the C9 SF-slot census |
| PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914/06_REPORT/REPORT.md | SF+0x30 NiNode as scene-graph root; GetObjectByName-like slot semantics; no transfer of engine-generation offsets |
| PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/ | x86dec.py/pebnd.py/cqc_battery.py tested limits (D1/D2) read as METHOD guidance only; no BASE decoder was used as this run's decoder; all this-run instruction boundaries were established by own byte decode + Ghidra cross-check |
| PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913, PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004, PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928, PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_202603T071348Z, PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004 (grep-level + targeted reads) | mgr1 singleton [0x00BA12E8] (getter FUN_004154F0), mgr1+0x10 hash_map, node {next, key@+4, value@+8}, the templates.vfs RB-tree registry root 0x00BA1824 (getter FUN_0043A550, lookup FUN_0072F580), FUN_004123D0 = `8B 01 C3` deref helper, candidate LEAD families |

## Era and negative status (unchanged, carried from the contract)

- Era: PCG 9.3.5 (Entropia.exe, the pinned EXE above). Historical 2003-era rules are NOT applied.
- WORLD_XYZ_RECOVERED = NO
- STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED
- HISTORICAL_INSTANCE_DATA_RECOVERED = NO
- PE_MASTER = PROVISIONAL_UNTIL_QUALIFIED (advisory only; CANONICAL_GATE_EFFECT = NONE)
- NEXT_EXPERIMENT_AUTHORIZED = NO
