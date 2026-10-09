# PE_MASTER_REVIEW — PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009

REVIEW_TYPE = PE-MASTER MASTER_AUDIT (internal advisory; NOT an independent Desktop post-audit; NOT executor/QC self-review)
AUTHOR = PE-MASTER
AUDITED_RUN = PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009
AUDITED_RANGE = uncommitted working tree at BASE 34fc34749464de3e05527088ed46be9e215f1964 (MACHINERY_AND_CONTROL_CORRECTION; commit pending at persistence)
CONTRACT = C:\Users\User\Documents\ChatGPT\PE\PE_CMO_C1_HIGH_BYTE_CORRECTION_PROMPT_20261008\OPENCODE_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009.md — 16623 B, SHA256 61AAA55854942A22085F3767A7D64512248EDFAE3A7B9BB54A5CBE36F36D3981 — verified MATCH
SOURCE RUN (Desktop post-audited) = PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009 at 34fc347; finding CMO-C1/P2
TARGET_IDENTITY = Entropia.exe 8015872 B / E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (unchanged; reads limited to the approved windows)
VERDICT = MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE)
CORRECTION_VERDICT = PASS (all 11 contract acceptance gates)

## Preflight
LOCAL_HEAD == origin/master == actual remote master == 34fc34749464de3e05527088ed46be9e215f1964. OUTPUT_ROOT created fresh. All 4 mandatory source pins MATCH (repin_write_provenance.py 34043/45120C91…; qc_remeasure.py 31970/4E5426AE…; CONTROL_RESULTS.json 18509/9545D0D7…; QC_RESULTS.json 31350/DE7DF210…); contextual inputs independently recorded.

## Defect and correction
- ROOT CAUSE: opcode 0x88 register-direct byte destinations misread the ModRM reg field as a full-register index (reg=5 CH → REGS[5]=EBP in the writes-set). Two facets: (1) wrong writes-parent for high aliases; (2) the historical QC never recorded register-direct byte-source parents at all.
- PRE (immutable 00_PRE/, AST-extracted historical implementations, top-level never executed): the CH mutant 88 DD @0x0085B24D FALSE-PASSES in BOTH historical decoders (executor: writes ["ebp"], scan []; QC: writes ["ebp"], reads [], scan []). Historical 8×8 census: writes-parent correct 32/64 per decoder; QC source-parent 0/64.
- POST corrected successors (explicit OLD→NEW mappings with both hashes): C1 clean PASS (64 insns; end 0x0085B290; no clobber; core [arg1+8]); C2 CH → writes {ecx}, bits [8,16), DETECTED @0x0085B24D, VALUE_PROVENANCE_GATE FAIL via ECX_REACHING_DEF_BROKEN ALONE (the same production provenance predicate as clean — no hard-coded assertion); C3 CL → same single-cause FAIL; C4 the complete 8×8 matrix: 64 cases per decoder, 128/128 outcomes PASS (executor 64 + QC 64; independent reference tables; dest 8/8, source 8/8; 2 bytes each; partial-write-vs-full-32-bit distinction preserved); C5 negatives 6/6 (88 DF/DC/CE/FF + QC's own 88 D4/88 FB — correct parents, no false ECX); C6 regression PASS (23/23 pins; rel32; RTTI both identities; 64-insn decode + exact boundary; field-level equality with the re-executed historical decoder; the facet-2 fix visible on exactly 4 real 88 9E instructions); AUX-1 unsupported → controlled fail-closed.

## PE-MASTER counter-checks (own execution, in-memory mutants, real provenance gate)
clean → PASS; CH 88 DD → 'mov ch, bl', writes {ecx}, byte_dst_parent 'ecx', bits [8,16), partial_gpr_write, ecx_scan [0x0085B24D], gate FAIL; CL 88 D9 → writes {ecx}, bits [0,8), gate FAIL; BH 88 DF → writes {ebx}, ecx_scan [], gate PASS. ALL MATCH the contract's expected semantics.

## QC
QC_ORIGIN = pe-master-auditor fresh-context internal QC (internal to PE-MASTER; NOT an independent Desktop post-audit). QC_VERDICT = QC_PASS — 11/11 acceptance gates, all re-measured from scratch (own AST extraction; own corrected decoder; own reference table; own RTTI walk; own mutants). The QC's 5 disclosed bring-up repair steps of its OWN tooling (one session, intermediate states preserved, zero executor artifacts touched) ADJUDICATED: not a QC_REPAIR_ROUNDS violation — no correction defect was found or repaired; the budget governs post-QC correction rounds. The executor's 3 disclosed process repairs adjudicated HONEST (incl. C5.4: the corrected decoder itself caught the executor's test-data error 0xF7 vs 0xFF — positive evidence the fix works).

## Standing preserved (verbatim)
CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL (no promotion beyond the original static scope); FIELD_SEMANTICS = UNVERIFIED; WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED; HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO. J3: PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED; NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION; SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE; ORIGINAL_J3_EDGE_BUDGET_COMPLIANCE = FAIL. Documentary backlog: DOC-1/P3 (C3+CC CC CC contextual boundary evidence only), DOC-2/P3 (M1–M6 wording discipline). GENERAL_X86_DECODER_CORRECTNESS and GENERAL_UNSUPPORTED_FORM_FAIL_CLOSED = NOT ESTABLISHED (bounded window decoders).

## Findings
NONE material. Scope clean: 0 new bodies/edges/field-semantics/runtime/network/placement/model RE/Gamebryo-OpenMW; sibling stores +0x48/+0x4C untouched; upstream arg1 untouched; EXE unchanged. Disclosed process items recorded (3 executor + 5 QC bring-up steps + 1 key-name cosmetics note in QC_RESULTS).

## Coverage
Full read: contract (529 lines), executor/QC handoffs, PRE/POST indexes. PE-MASTER execution counter-check: C1/C2/C3/C5 semantics through the actual corrected production decoder + its real provenance gate. NOT_CHECKED: the QC decoder's non-contract 8A branch (implemented, not exercised — no such byte in the window), exclusion-census pins beyond approved windows, general x86 correctness (not established by design), runtime (prohibited).

SOURCE_DESKTOP_POST_AUDIT (CMO provenance run) = PERFORMED (the CMO-C1 finding's origin)
NEW_DESKTOP_POST_AUDIT = NOT_PERFORMED
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
