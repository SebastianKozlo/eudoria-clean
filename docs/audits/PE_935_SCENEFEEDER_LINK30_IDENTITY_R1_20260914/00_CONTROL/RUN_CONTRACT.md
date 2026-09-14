# RUN_CONTRACT.md — PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914

Executor: pe-reconstruction (direct PE-MASTER dispatch; NO_NESTED_TASKS; blockers
return to PE-MASTER, never to the human). Publication is a SEPARATE later step
(pe-master-auditor after PE-MASTER adjudication) — ZERO git mutations by this
executor; this run package exists on disk only.

The complete human order (verbatim):

---

RUN_ID: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914
(human contract name: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1; date suffix per repo convention)

RUN_CLASS: LOAD_BEARING (declared by PE-MASTER)
MODE: SINGLE SMALL BOUNDED RUN. STATIC-ONLY (the client NEVER runs; no process launches of any game binary; byte-reading scripts are fine). NO NESTED TASKS (task:deny — you cannot and may not launch subagents; if blocked, return to PE-MASTER). NO HUMAN PROMPTS (blockers return to PE-MASTER, never to the human). HARD STOP after deliverables. NO AUTO LOOP.
Executor: pe-reconstruction. Publication is a SEPARATE later step (pe-master-auditor after PE-MASTER adjudication) — you make ZERO git mutations: no commit, no push, no staging. You only create the run package on disk.

TIMEBOX_MINUTES: 45 (stop earlier when gates are met)

=== BASE (verify first, fail-closed) ===
Repo: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean (GitHub SebastianKozlo/eudoria-clean, branch master)
Expected BASE_SHA: 1a490eed4ca2b295e78cd3cf851a08ac9c93930b
PE-MASTER has already verified HEAD == origin/master == ls-remote == BASE at dispatch time. You re-verify: git rev-parse HEAD; git rev-parse origin/master; git ls-remote origin master; git status --short. Any drift from BASE_SHA (other than the known foreign untracked `experiments/` which you must NOT touch) -> HARD STOP: BASE_DRIFT.

Primary physical source:
D:\Eudoria_Reconstruction\pcg_install\Entropia.exe (era PCG_9_3_5)
Expected: SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, size 8015872, machine 0x014C (i386), PE32 opt_magic 0x010B, image_base 0x00400000, no ASLR.
Mismatch of SHA or size -> HARD STOP: SOURCE_IDENTITY_FAIL.
Record all of this in 00_CONTROL/SOURCE_IDENTITIES.json (own measurement, fail-closed asserts run first in every script).

=== ONE PRIMARY QUESTION ===
Co jest zapisywane do SceneFeederObject+0x30 i jaka jest najlepiej dowiedziona statycznie klasa/typ tego obiektu?
(What is written to SceneFeederObject+0x30, and what is the best statically-proven class/type of that object?)

=== STARTING POINT (from the accepted run PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914; verified by PE-MASTER against its 01_RAW/SLOT_DISASSEMBLY.txt; a STARTING POINT ONLY — NOT proof; re-derive in-run every fact you rely on) ===
- SceneFeederObject vtable = 0x00A7D458 (that run's own RTTI walk: [0x00A7D454]=0x00AA12B8 -> COL pTypeDescriptor=0x00B78834 -> TD name `.?AVSceneFeederObject@@`; six slots 0..5).
- FUN_0050A050 (vtable slot 3): 0x0050A057 mov esi,ecx; 0x0050A05B mov ecx,[esi+0x30]; 0x0050A05E mov edx,[ecx]; 0x0050A061 mov eax,[edx+0x44]; 0x0050A064 call eax. The link object's class is UNKNOWN. Do not treat any earlier class description of the link as evidence — there is none.
- Prior accepted-run reference for the SF creation chain (READ-ONLY pointer, re-derive from bytes before use): docs/audits/PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 — SceneFeederObject created via new(0x98) -> FUN_005247C0 -> ctor FUN_00509330; the SF pointer is stored at instance+0xC0; create arg3 = empty basic_string in f90rec+0x8C; FUN_005094C0 = the +0x34/+0x38/+0x3C triple + flag +0x28 writer (positive control of the prior run).
- ADMINISTRATIVE CORRECTION (Desktop post-audit; carry it into any reference to the previous run — do NOT propagate the old wrong figures "26 package files / 25 manifest rows"): the committed state of PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 is 27 package files, 26 manifest rows + manifest self (the L12 self-exclusion precedent), 28 commit paths including AUDIT_ENTRYPOINT.md. Administrative only; no impact on its science result.

=== TASK A — COMPLETE WRITER CENSUS ===
Find ALL static instructions that DIRECTLY write [SceneFeederObject+0x30]. Do not report only interesting hits — the census denominator must be auditable.
Requirements:
1. DOCUMENTED ENUMERATION RULE: state exactly which instruction forms were scanned over what address range (full .text linear sweep from physical bytes, own PE section-table walk; forms: mov [base+0x30] with disp8/disp32, base+index+disp variants, immediate stores to [base+0x30]; record the scan's raw hit count = the candidate denominator BEFORE classification).
2. SF-IDENTITY METHODOLOGY: document how "the receiver register is an SF-this" is proven for each classification: SF ctor sites re-derived in-run from the creation chain (new(0x98) -> ctor; the ctor's vtable store of 0x00A7D458 into [this+0]), `this`-flow through function bodies, pointers saved to stack/locals and reloaded.
3. COVERAGE CLASSES (each either scanned or explicitly declared UNRESOLVED with its bounds — a missing class makes G2 fail):
   (i) writes via a register holding SF-this;
   (ii) writes via an SF pointer held in a stack slot/local;
   (iii) combined-offset writes through the container that holds the SF pointer at +0xC0 (i.e. [container+0xF0] when SF@container+0xC0 is proven — scan for the +0xF0 disp form at the proven container sites);
   (iv) bulk initialization covering +0x30 (rep movsd / memcpy-style) at the SF ctor/init sites.
4. EVERY candidate row in 02_ANALYSIS/SF30_WRITER_CENSUS.csv with columns: writer_va, function_va, instruction, source_register_value, receiver_provenance, classification — classification EXACTLY one of: PROVEN_SF30_WRITER, POSSIBLE_ALIAS, REJECTED_ALIAS, UNRESOLVED. REJECTED_ALIAS rows must carry why (proven non-SF receiver, e.g. this belongs to another class). PROVEN rows must carry the dataflow evidence chain. The CSV counts (total/proven/possible/rejected/unresolved) must be RECOMPUTED from the CSV rows by a script — never hand-typed (COUNTER_ARITHMETIC).
5. Raw evidence: 01_RAW/SF30_WRITER_RAW.txt — the disassembly window (own capstone decode from the physical EXE) for EVERY census candidate (not only proven), plus the raw scan statistics.

=== TASK B — SOURCE PROVENANCE (PROVEN_SF30_WRITER only) ===
For each PROVEN_SF30_WRITER, trace the source of the value written to +0x30 UP TO its creation/receipt ONLY: e.g. allocation -> ctor -> stored at SF+0x30; function argument -> stored at SF+0x30; manager/singleton lookup -> returned pointer -> stored at SF+0x30. STOP at creation/receipt — do NOT follow the value's later behavior. If a chain would require substantial NEW reverse engineering beyond the creation/receipt point: mark SOURCE_PROVENANCE = UNRESOLVED for that edge and STOP on that edge (that is an allowed outcome, not a failure). Document each hop with VA + byte evidence in 02_ANALYSIS/SF30_PROVENANCE.md.

=== TASK C — TYPE IDENTITY ===
If the written object has a statically recognizable vtable: perform ONLY the RTTI walk object -> vtable -> [vtable-4] = COL -> COL.pTypeDescriptor -> TypeDescriptor -> TD+0x0C name string, ALL from physical bytes (record every dword VA and the raw name bytes) in 01_RAW/SF30_RTTI_RAW.txt.
MANDATORY KNOWN-ANSWER CALIBRATION FIRST: your RTTI walker must first reproduce the KNOWN answer from the SceneFeederObject vtable 0x00A7D458 (expected name `.?AVSceneFeederObject@@` from the accepted run) — only then walk the link object's vtable. Report RTTI_NAME verbatim (exact mangled string).
DO NOT decode ANY method of the link vtable. ESPECIALLY DO NOT DECODE SLOT 17 ([vtable+0x44]). Slot 17 is the NEXT seam, explicitly out of scope for this run.
If the written object has no statically recognizable vtable (e.g. a raw non-object pointer, or provenance ends before any vtable store): SF30_TYPE_IDENTITY = NO_VTABLE / UNKNOWN — that is allowed (status C or lower).

=== POSITIVE CONTROL (mandatory; missing/failing => RUN_INVALID) ===
Re-measure the minimal window FUN_0050A050 @ 0x0050A05B from physical bytes: confirm (a) 0x0050A05B = 8B 4E 30 (mov ecx,[esi+0x30]) with ESI = SF-this (mov esi,ecx @ 0x0050A057); (b) ECX is not modified between 0x0050A05B and the call @ 0x0050A064; (c) the receiver of CALL [vtable+0x44] @ 0x0050A064 is exactly [ESI+0x30] (edx=[ecx] @ 0x0050A05E, eax=[edx+0x44] @ 0x0050A061, call eax @ 0x0050A064). Persist in 01_RAW/POSITIVE_CONTROL_0050A050.txt with the measured bytes.

=== FORBIDDEN (HARD SCOPE — violation is a run defect) ===
- Decode vtable slot 17 / [vtable+0x44] target; analyze 0x437F70; analyze 0x82B5A0 (re-reading the 0x50A050 window bytes for the positive control is allowed; decoding those callees is not).
- Attempt to prove SceneFeeder->model. No MODEL_BRIDGE_CONFIRMED, no TRANSFORM_TO_MODEL — those outcomes are FORBIDDEN for this run. MAXIMUM semantic label: SF30_LINK_TYPE_IDENTIFIED. If the RTTI name literally reads like a "Model..." class: report the exact class name, but the model bridge remains NOT_DEMONSTRATED.
- 296445, 4508, terrain, NIF, network, any runtime work.
- Modifying ANY prior run package, shared tools, the repo, or experiments/ (all READ-ONLY). Your writes are ONLY inside docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/.
- Creating .pre files, extra dumps, or large censuses beyond contract need (a QC-discovered real correction need is the only exception, documented in an AMEND_LOG).
- Any git mutation (no add/commit/push; publication is a later separate step by pe-master-auditor).

=== OUTPUT PACKAGE (target ~10-15 evidence files + minimal run-local scripts; total <= ~18 files) ===
docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/ (create fresh; verified absent):
- 00_CONTROL/RUN_CONTRACT.md — this contract (embed the human order verbatim, including the administrative correction)
- 00_CONTROL/SOURCE_IDENTITIES.json — BASE_SHA, remote check results, EXE SHA256/size/PE facts, hashes of prior-run reference files used
- 00_CONTROL/<your scripts> + 00_CONTROL/SCRIPT_SHA256.csv — run-local instrumentation only (own PE parser + capstone decode; every count/claim derived from scripts)
- 01_RAW/SF30_WRITER_RAW.txt — per-candidate disasm windows + raw scan stats (the candidate denominator)
- 01_RAW/SF30_RTTI_RAW.txt — the RTTI walk raw bytes (calibration + link), if RTTI exists
- 01_RAW/POSITIVE_CONTROL_0050A050.txt
- 02_ANALYSIS/SF30_WRITER_CENSUS.csv
- 02_ANALYSIS/SF30_PROVENANCE.md
- 03_EVIDENCE/README.md — what each artifact is, generator, and how to reproduce
- 06_REPORT/REPORT.md, 06_REPORT/HANDOFF.md, 06_REPORT/STAGE_ACCEPTANCE_GATES.csv, 06_REPORT/MANIFEST_SHA256.csv (manifest self-exclusion per the L12 precedent: rows = package files minus the manifest itself; document the exclusion)

=== EXECUTABLE GATES (STAGE_ACCEPTANCE_GATES.csv; each fail-closed, with its raw denominator) ===
- G0-SOURCE-BASE: PASS iff measured EXE SHA+size match the pins AND HEAD==origin/master==ls-remote==BASE_SHA AND the only dirty path is the foreign untracked experiments/. Else HARD STOP.
- G1-POSITIVE-CONTROL: PASS iff the 0x50A05B window bytes + receiver chain measured exactly as specified. Else RUN_INVALID.
- G2-CENSUS-COMPLETENESS: PASS iff (a) the enumeration rule + scanned range + raw candidate denominator are documented; (b) EVERY candidate has a row with a 4-class classification; (c) counts recomputed from the CSV by script equal the report's counts; (d) coverage classes (i)-(iv) each scanned or explicitly UNRESOLVED-with-bounds.
- G3-PROVENANCE: PASS iff every PROVEN_SF30_WRITER row has a creation/receipt-level source chain with VA+byte evidence, or an explicit per-edge SOURCE_PROVENANCE=UNRESOLVED.
- G4-TYPE-IDENTITY: PASS iff the RTTI chain is byte-confirmed from the physical EXE (with the calibration PASS on the known SceneFeederObject name first), or NO_VTABLE/UNKNOWN is explicitly declared with the reason.
- G5-SCOPE-HELD: PASS iff the package contains no slot-17 decode, no 0x437F70/0x82B5A0 analysis, and no MODEL_BRIDGE/TRANSFORM_TO_MODEL claim (a script census over the package text asserts zero occurrences as RESULT claims; mentioning the forbidden labels as "not made / NOT_DEMONSTRATED" is fine).

=== FINAL STATUS (exactly the human contract taxonomy; do not widen scope to "get success") ===
A — IDENTIFIED: complete writer census + continuous provenance + RTTI/type identity.
B — STRONGLY_IDENTIFIED: writer and object provenance proven, but identity rests on strong structural evidence without full RTTI.
C — WRITER_FOUND_TYPE_UNKNOWN: writer proven, but the object's type remains UNKNOWN.
D — UNRESOLVED: could not prove the complete writer census / receiver provenance.

=== QUALITY BARS (project canon; violations are audit findings) ===
- Every cited VA byte-locked from physical bytes via your OWN VA->file-offset conversion (own PE section walk; no inherited tool output trusted unverified).
- COUNTER_ARITHMETIC: every count re-derived from raw artifacts by script; no hand-typed numbers in reports.
- Statuses only from the taxonomy; no "%"-style progress claims; era label PCG_9_3_5 everywhere; STATIC-ONLY stated (the client never ran — nothing is a runtime oracle result).
- Honest NOT_CHECKED section in REPORT.md (what this run did NOT examine).
- REPORT.md follows the 20-point reporting contract: human-first decision block, RUN_ID/milestone EU935-M1 header, state before->after, claim->evidence with statuses, denominators, gates, negative controls, hard stops, handoff block. Milestone context: EU935-M1 World Surface Fidelity; this run is the SF+0x30 link-identity seam of the SceneFeeder position chain.

=== FINAL_HANDOFF_SCHEMA (your final answer = delivery notice ONLY; PE-MASTER audits from disk) ===
RUN_ID / BASE_SHA / OBSERVED_HEAD_SHA (expected == BASE; you did not commit) /
WRITER_COUNT (total census candidates) / PROVEN_WRITER_COUNT /
SF30_SOURCE_PROVENANCE / SF30_TYPE_IDENTITY / RTTI_NAME (verbatim or N/A) /
FINAL_STATUS (A|B|C|D) / NEXT_SEAM (SLOT17 | NONE) /
REPORT_PATH / HANDOFF_PATH / MANIFEST_PATH /
RUN_STATUS (COMPLETE | PARTIAL | HARD_STOP) / HARD_STOP_REASON (or NONE) /
NOT_CHECKED (short list)

---

End of verbatim human order.

Executor's G0 dirty-path note (measured, in-run): the contract's G0 predicate names
"the only dirty path is the foreign untracked experiments/" as the PRE-RUN state.
Because the executor is forbidden from git mutations while being required to create
this package on disk, the package directory itself is an EXPECTED untracked path at
gate time. The executed G0 therefore allows exactly {experiments/ (foreign, untouched),
docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/ (this run's own output)}.
No tracked file was modified; git diff is empty; no commit/stage/push was made.
