# EVIDENCE_INDEX — PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009

Index of every evidence file of the package with its role. Physical
size/SHA256 of every package file: MANIFEST_SHA256.csv (generated LAST; the
authoritative machine-readable index — this file is the human-readable role
map). All paths repo-relative under
`docs/audits/PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009/` unless noted.
Executor + QC evidence FROZEN before this persistence phase (30 files:
executor 27 + QC 3); the persistence phase added
PE_MASTER_REVIEW.md / FINAL_REPORT.md / EVIDENCE_INDEX.md / HANDOFF.md and the
manifest.

## 1. Governance and provenance records

| File | Size (B) | Role |
|---|---:|---|
| PREREGISTRATION.md | 22192 | Written BEFORE science by the first (crashed) executor session: P1 authorization record, P2 the one bounded question, P3 exact scope/budgets/method, P4 preregistered hypotheses (H-A, H-B, H-BRIDGE), P5 the 12-case control matrix + artifact controls, P6 separate gates, P7 conditions/stop rules, P8 toolchain, P9 planned evidence files. P10 = the dated session-continuity disclosure appended by the fresh retry session (crash left exactly 3 files; their discovery SHAs recorded; P1–P9 byte-identical pre-science — mechanical proof: the first 19151 B hash to F36DE40AF53CEE9FE2F0F5A11A65475239E5035DE96F2FD45D4E5669E775EACC). PRE never rewritten to match POST. |
| INPUT_IDENTITIES.md | 12196 | Retry-session preflight from physical bytes: I1 authorization (contract 23187 B / 773C1310… verified MATCH before any action), I2 the crash/continuation disclosure with the 3 discovery SHAs and the verification/continuation decisions, I3 git triple (LOCAL_HEAD == origin/master == live remote == ce75b7b…; clean tracked worktree; foreign untracked inventory), I4 EXE identity re-hashed before AND after (8015872 B / E7785430…), I5 physical windows + PE mapping + decode census, I6 all 8 required repo inputs (physical size/SHA + worktree==HEAD blob equality incl. the pinned historical blobs 3648e1b8… / dc61d1b4…), I7 toolchain, I8 temp fixtures (outside Git, removed), I9 scope-compliance census. |
| SUPERSESSION_AND_STANDING.md | 7058 | Documentary standing record per contract §2/§8: the prior standing preserved VERBATIM (S = ESP at 0x00528E76; ARG1_DIRECT_SOURCE = CONFIRMED_STATIC_CONDITIONAL; UPSTREAM_PROVENANCE = UNRESOLVED_UPSTREAM; CMO_C1 = CLOSED_FOR_AUDITED_STATE; CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL; J3 three lines), this run's relation (CONSISTENT, NOT SUPERSEDING; ONE new qualified boundary; conditions AS1–AS5 + EAX≠0), scope fences (FIELD_SEMANTICS = UNVERIFIED; POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM; WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED; HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO), not-reopened/not-restored list, open findings, phase-delegation record. |
| EVIDENCE_INDEX.md | (this file) | This role map. |
| HANDOFF.md | (this phase) | Contract §10 terminal fields with ACTUAL measured values (see HANDOFF.md). |
| MANIFEST_SHA256.csv | (generated LAST) | Final persistence-scope manifest: every physical package file EXCEPT the manifest itself PLUS the updated AUDIT_ENTRYPOINT.md; repo-relative; size + SHA256 per file; bijection-verified (self-exclusion documented). |
| PE_MASTER_REVIEW.md | (this phase) | PE-MASTER MASTER_AUDIT verbatim (MASTER_ACCEPTED, advisory; ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE) — preflight, the finding, gate predicates, PE-MASTER counter-checks (9 instruction byte pins + the bridge arithmetic; the disclosed .text offset-shortcut tooling error), findings (F-QC-1..3 P3 open), standing preserved, coverage/NOT_CHECKED. |
| FINAL_REPORT.md | (this phase) | The final report: run/contract identity, preflight, the crash/continuation disclosure, window identities, tool provenance, Phase A + the three preservation proofs, Phase B + the LEA result + the path condition, the conditional bridge + the AS conditions table, the 24 control outcomes, the artifact controls, QC + PE-MASTER sections, scope census, standing verbatim, SCIENCE_OUTCOME and terminal governance. |

## 2. Window identity and raw disassembler outputs (01_RAW/)

| File | Size (B) | Role |
|---|---:|---|
| 01_RAW/WINDOW_A_OBJDUMP.txt | 1882 | Crash-left raw GNU objdump 2.44 output for ORIGINAL window A (verified-kept): header records tool, command (`--adjust-vma=0x528e50`), fixture provenance (66 B from the EXE at raw offset 1216080, SHA F8735567…), exit status 0; disassembly 23 instruction lines [0x00528E50,0x00528E92). Discovery SHA 7AABA008CFBD8BAF4CDF868BA25E3E9A014E9F732E375402553AAA3282D2C86B (unchanged since discovery; byte-identical to the retry's fresh invocation). |
| 01_RAW/WINDOW_A_OBJDUMP_RETRY.txt | 1795 | The retry session's own fresh objdump invocation on an independently extracted window-A fixture — the crash-continuation verification output (23/23 instruction lines byte-identical to the crash-left file). |
| 01_RAW/WINDOW_B_OBJDUMP.txt | 1557 | Crash-left raw objdump output for ORIGINAL window B (verified-kept): `--adjust-vma=0x4c4792`, 52 B at raw offset 804754, SHA B59E16DC…, rc 0; 17 text lines (16 instructions + 1 continuation). Discovery SHA B82C5533D1E10EE3116C7E74EA72471257FA1E3A110F7BCFEA0C452B01ED99CC (unchanged since discovery; byte-identical to the retry's fresh invocation). |
| 01_RAW/WINDOW_B_OBJDUMP_RETRY.txt | 1477 | The retry session's own fresh window-B invocation — crash-continuation verification (17/17 lines byte-identical). |
| 01_RAW/CONTROLS/A_CLEAN_OBJDUMP.txt | 1627 | Raw objdump output, control case A_CLEAN (original A bytes through the full pipeline). |
| 01_RAW/CONTROLS/B_CLEAN_NONNULL_OBJDUMP.txt | 1341 | Raw objdump output, control case B_CLEAN_NONNULL (original B; qualified EAX≠0 branch analysis input). |
| 01_RAW/CONTROLS/B_CLEAN_NULL_OBJDUMP.txt | 1329 | Raw objdump output, control case B_CLEAN_NULL (same original B; EAX==0 path analysis input). |
| 01_RAW/CONTROLS/M1_A_FRAME_OBJDUMP.txt | 1726 | Raw objdump output, mutant M1_A_FRAME (SUB 0x1C→0x18 @0x00528E5E in a synthetic copy): S=E−0x34; source [E+8]. |
| 01_RAW/CONTROLS/M2_A_SLOT_OBJDUMP.txt | 1727 | Raw objdump output, mutant M2_A_SLOT (disp 0x3C→0x38 @0x00528E84): source [E] under the original frame. |
| 01_RAW/CONTROLS/M3_B_LEA_DISP_OBJDUMP.txt | 1429 | Raw objdump output, mutant M3_B_LEA_DISP (LEA disp 0x14→0x18 @0x004C47BA): arg1 ADDRESS(T+0xC). |
| 01_RAW/CONTROLS/M4_B_LAST_PUSH_OBJDUMP.txt | 1416 | Raw objdump output, mutant M4_B_LAST_PUSH (51→52 @0x004C47BE): arg1 = MEM(T+0x4C), kind STACK_READ. |
| 01_RAW/CONTROLS/M5_B_EARLY_PUSH_ORDER_OBJDUMP.txt | 1457 | Raw objdump output, mutant M5_B_EARLY_PUSH_ORDER (51 52→52 51 @0x004C47B7..B8): arg1 ADDRESS(T+8) + slot UNCHANGED; arg3/arg4 swapped. |
| 01_RAW/CONTROLS/M6_B_SKIP_OBJDUMP.txt | 1397 | Raw objdump output, mutant M6_B_SKIP (JE→JMP 74 19→EB 19 @0x004C47AD): unconditional exit; no delivery. |
| 01_RAW/CONTROLS/M7_B_RECEIVER_ONLY_OBJDUMP.txt | 1442 | Raw objdump output, mutant M7_B_RECEIVER_ONLY (8B C8→8B CE @0x004C47BF): receiver ESI/unknown; arg1 + slot UNCHANGED. |
| 01_RAW/CONTROLS/M8_B_WRONG_TARGET_OBJDUMP.txt | 1455 | Raw objdump output, mutant M8_B_WRONG_TARGET (E8 8A 46 06 00→E8 8B 46 06 00 @0x004C47C1): actual target 0x00528E51 recomputed → bridge_valid=False. |
| 01_RAW/CONTROLS/M9_B_LEA_TO_MOV_OBJDUMP.txt | 1449 | Raw objdump output, mutant M9_B_LEA_TO_MOV (8D 4C→8B 4C @0x004C47BA): arg1 MEM(T+8), kind STACK_READ. |

All 16 raw files carry the tool/command/rc header; the fresh QC's raw-VA
census confirmed every decoded VA lies inside window A or B (0 outside).
No .bin window extracts are committed; 01_RAW artifacts are disassembly TEXT
only.

## 3. Load-bearing structured evidence

| File | Size (B) | Role |
|---|---:|---|
| WINDOW_IDENTITIES.json | 3644 | Machine-readable window identities: EXE path/size/SHA + read scope; objdump tool identity + command form + rc; per-window VA interval, size, raw offset (+hex), SHA256 (== contract pin), PE section mapping (.text; unique RAW-backed; RVA==raw-offset note), decode census (instructions, exact cover, first/last VA, visible CALLs with targets + bytes), raw/retry file pointers, crash-continuation verification (line-identical flags + counts). |
| ENTRY_FRAME_LEDGER.csv | 3078 | Instruction-by-instruction Phase A derivation (23 rows + header): SEQ, VA, BYTES, DECODED_OP, ESP_BEFORE/AFTER/DELTA, NOTES, STACK_WRITES, STACK_READS, SEGMENT_WRITES, FLAG_WRITER — the full write census (8 stack writes + 1 FS:[0] segment write; ZERO at [E+4]), the S=E−0x38 chain, the source read [E+4], EDI preservation, the delivery facts at CALL 0x00528E8D (ESP E−0x44/S−0xC before; E−0x48/S−0x10 at entry; RET_PUSH at [E−0x48]). |
| CALLER_STACK_LEDGER.csv | 3523 | Instruction-by-instruction Phase B derivation (NULL 8 rows + NONNULL 17 rows incl. the PATH FORK annotation rows — see F-QC-2): PUSH 0x128; opaque CALL 0x0095D3C4 (AS3); ADD ESP,4; TEST/JE; the EAX≠0 branch loads [T+0x50]/[T+0x4C]; three pushes → T−0xC; LEA = ADDRESS(T+8) (opcode 8D); PUSH ECX → [T−0x10] := ADDRESS(T+8); MOV ECX,EAX; CALL 0x00528E50 with the hardware return push at [T−0x14]. |
| BRIDGE_PROVENANCE.json | 32219 | The load-bearing claim set: window identities (embedded), phase_a (E, pivot S=E−0x38, source slot [E+4]≡[S+0x3C], preservation: the enumerated 8+1 write census with zero aliasing writes to the source slot, EDI reaching def, delivery + receiver channel), phase_b (null/nonnull paths; T; flags census; opaque call AS3; LEA instruction kind ADDRESS; arg1/arg_slots/receiver; call with target recomputed), bridge (join E=T−0x14; slot-address identity both ways; zero intervening writes; status POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL; conditions list), and the per-claim records A-1..A-8, B-1..B-5, BR-1, BR-2 with claim class, build/EXE identity, VA, opcode, ESP/register/memory facts, assumptions, evidence origin, status, remaining uncertainty and (for PASS records) MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED. |
| CLAIM_MATRIX.csv | 9120 | The 12-case × 2-side matrix: CASE, SIDE (PRODUCTION/QC_FRESH), EXPECTED_DISCRIMINATING_RESULT, ACTUAL_OUTCOME (structured facts JSON), VERDICT, EVIDENCE_REF per case. Production side 12/12 CONTROL_PASS; QC_FRESH side recorded by the executor as NOT_PERFORMED_BY_THIS_WORKER (separate fresh-QC session) — the QC side outcomes live in QC_RESULTS.json / QC_REPORT.md (12/12 CONTROL_PASS, agreeing field-by-field with production). |
| CONTROL_RESULTS.json | 58084 | Production structured results for the 12-case matrix: per-case fixture identity (name/size/SHA + the identity-only rule), the exact objdump command + rc + raw-output pointer, decode census, derived facts, per-fact expected/actual/match checks, verdict, phase_a/phase_b facts; matrix_total_expected 24; fresh_qc_side = NOT_PERFORMED_BY_THIS_WORKER (honestly recorded by the executor). |
| ARTIFACT_CONTROL_RESULTS.json | 14606 | Artifact controls (production gate): baseline re-read of the persisted load-bearing artifacts — 21 named fact checks (window SHA/size/interval vs physical EXE bytes; ledger row counts + S/ESP values vs the independent walk; source slot; delivery ESP facts; ADDRESS-vs-MEM kind vs opcode 0x8D; LEA expression; joined slot identity; all three CALL targets by rel32 recompute; flags census) all PASS; AC1 (copied artifact, ADDRESS(T+8)→MEM(T+8)) REJECTED on PROV-B-KIND + PROV-B-LEA; AC2 (copied artifact, [E+4]→[E+8]) REJECTED on PROV-A-SLOT; overall ARTIFACT_CONSISTENCY_PASS; scope notes (bypass confined to isolated synthetic copies; originals never mutated). |
| SUPERSESSION_AND_STANDING.md | 7058 | (see §1 above) |

## 4. Scripts (03_SCRIPTS/)

| File | Size (B) | Role |
|---|---:|---|
| 03_SCRIPTS/run_frame_bridge.py | 103544 | The executor's bounded decoder-assisted symbolic replay (production): consumes objdump raw text + physical bytes; window extraction/hashing/PE mapping; Phase A/B/bridge derivation; the 12-case control matrix; the artifact gate; fail-closed (Unresolved exceptions; no expected-result filling; the EXPECTED table is a comparison table encoded from the contract §7 matrix, used only for verdicts). Produced ENTRY_FRAME_LEDGER.csv, CALLER_STACK_LEDGER.csv, BRIDGE_PROVENANCE.json, CLAIM_MATRIX.csv (production half), CONTROL_RESULTS.json, ARTIFACT_CONTROL_RESULTS.json. Read to EOF by the fresh QC (2194 lines) — adjudicated fail-closed. |
| 03_SCRIPTS/qc_frame_bridge.py | 83103 | The fresh QC's OWN symbolic implementation (SHA256 EC9F3FBE152E7694B0E2540E1BB4F399994BBAB81CE8B33B64495B25A3CE1688): does NOT import the production script; own byte extraction/hashing/PE mapping, own objdump invocations, own replay + ESP walk, own expected-fact encoding from contract §7, own artifact gate (21 checks), own 12-case matrix, own join adjudication, own crash-continuation proof (the 19151-byte prefix hash), own scope/standing token scans. QC session's disclosed tooling repairs (F-QC-3) are visible in this file. |

## 5. Fresh QC outputs

| File | Size (B) | Role |
|---|---:|---|
| QC_RESULTS.json | 109626 | Machine-readable QC evidence for every duty (D1–D9): independence statement, EXE before/after hashes, PE mapping, own objdump raw outputs embedded, phase_a_mine/phase_b_mine step-by-step derivations, the join adjudication, the 12-case QC matrix outcomes, the artifact-gate re-run (baseline 21/21, AC1/AC2 REJECTED), the production comparison (56/56 field agreement; kind-nomenclature mapping), the crash/continuation physical verification (incl. the PREREGISTRATION prefix-hash proof), the raw-VA census (0 outside), the standing token scan (0 forbidden; all fences present), PASS-record provenance fields. SHA256 0DF6B9341CD8C4DEE31660747E867AAC11B3BCCDFCB77A13800B96E5AF0CD27D. |
| QC_REPORT.md | 25765 | The QC's human-readable report: QC_ORIGIN (internal to PE-MASTER; NOT a Desktop post-audit; NOT executor self-review), per-duty results D1–D9 (independence dimensions table with the honest same-disassembler statement), the 12/12 + 12/12 matrix, the artifact controls, the crash/continuation adjudication, the 7-repairs honesty adjudication, scope/standing scan, QC_VERDICT = QC_PASS with basis, FULL_READ_LOG + NOT_CHECKED (7 items with reasons), open findings F-QC-1/F-QC-2/F-QC-3, handoff pointers. |

## 6. Required repository inputs at BASE (contract §3; verified bytes + Git blobs)

| Repository path | Bytes | SHA256 |
|---|---:|---|
| docs/audits/PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913/01_RAW/F00528E50_CTOR_MOBJ.txt | 8613 | A6ECDFD8350EA511625E296337002F1C45E3CAA8309D79CA843B35088903AF56 (Git blob 3648e1b86aa6933df6017840a20704f04e642bc1) |
| docs/audits/PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913/01_RAW/F004C46C0_CREATE.txt | 14517 | 32BDC6455F98078ED7D198FA96AD98ACF5D86908CA1B4DC950E6127EA3F7AF6D (Git blob dc61d1b45df788b257c49771c0e55668fa2036b8) |
| docs/audits/PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009/FINAL_REPORT.md | 19514 | 0F84FC111D893778CA410DC83A439E2A8E653FBB9466F409828DC3BC419DF762 |
| docs/audits/PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009/ARG1_PROVENANCE.json | 10071 | 29FF09675BEC2A4604524CBD202E6542AA850FD54A6ABBAEFF0395BF6813F85E |
| docs/audits/PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009/SUPERSESSION_AND_STANDING.md | 6848 | 0AB2CDECE09CB2FF1419C48E9A1169832A0A061C618A7F94F290089C75F49921 |
| docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/SUPERSESSION.md | 8339 | DD11137A0E79491511A7688B7C1DE9252DB7BA443FA31892C345CA76CE136845 |
| docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/CORRECTED_STATUS_ALGEBRA.md | 8987 | 00D09B0F72F1F6859C9DAF8A73C592659F251B596588DA304D9BC6912A40FA9F |
| AUDIT_ENTRYPOINT.md | 273796 | 9F5E83940ECD0496FA21310C5AEAFE6F49D4631F86D495BF4E536548B6AD84A5 (BASE state; this persistence phase adds exactly ONE newest-first LATEST RUNS row — the post-update identity is recorded in MANIFEST_SHA256.csv) |

Read-only binary: Entropia.exe 8015872 B /
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
(D:\Eudoria_Reconstruction\pcg_install\Entropia.exe — local-only, never
committed; reads limited to whole-file hash, PE header/section mapping and the
two pinned window byte ranges).

## 7. Package census

30 frozen executor/QC files (executor 27 + QC 3) + 4 persistence-phase
documents (PE_MASTER_REVIEW.md, FINAL_REPORT.md, EVIDENCE_INDEX.md,
HANDOFF.md) + MANIFEST_SHA256.csv = **35 physical package files**; the
manifest covers 34 package rows + 1 entrypoint row = 35 rows (self-excluded).
Total changed paths of the commit: 36 (35 package files + AUDIT_ENTRYPOINT.md).
