# PREREGISTRATION — PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009

- **RUN_ID**: PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009
- **RUN_CLASS**: BOUNDED_STATIC_CONSUMER_CENSUS
- **RECORDS**: STATIC_ONLY — the client never runs in this run. Every finding in this
  package is labeled STATIC_ONLY with an evidence maturity level
  (IDENTITY / BYTE_OBSERVATION / STRUCTURE / RELATION). No MECHANISM and no RUNTIME
  claims are made anywhere in this package.
- **Executor**: pe-reconstruction (dispatched by PE-MASTER, parent session).
- **Human authorization**: the human's direct instruction
  "kontynuuj szukanie budynków i ich lokalizacji" (2026-10-09) authorizes this
  building/placement workstream continuation.
- **Binary**: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe
  — EXPECTED 8,015,872 B / SHA256
  E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31.
  Re-hashed BEFORE all work (PASS, measured = expected) and to be re-hashed AFTER
  all work. ERA: PCG/EU 9.3.5 client. Addresses are VAs (image base 0x00400000).
- **This file is written BEFORE any census science below is executed.**

## 1. THE ONE PRE-REGISTERED P0 QUESTION

In the PCG 9.3.5 client binary, what is the COMPLETE static reference census of the
template-registry lookup FUN_0072F580 and its singleton getter FUN_0043A550
(registry tree DAT_00BA1824, per prior pinned evidence), and for EACH direct caller
found, what role does it play with the returned template object — specifically:
(a) can any caller path carry a template id (definition id, e.g. 4057) from a
persisted/static source into the lookup, and (b) does any caller read, write or
forward a transform/position/placement-relevant field of an object derived from the
returned template?

NO runtime claims; NO XYZ recovery claims; the question is census + role
classification only.

### Prior-evidence hypothesis status (to be RE-VERIFIED, never inherited)
- FUN_0072F580 = template-registry lookup — HYPOTHESIS. Byte re-pin REQUIRED this run
  (declared re-pin window, §4.1).
- FUN_0043A550 = registry singleton getter — HYPOTHESIS. Byte re-pin REQUIRED this run
  (declared re-pin window, §4.2).
- DAT_00BA1824 = registry tree / singleton storage — HYPOTHESIS. Byte re-pin REQUIRED
  this run: the reference(s) to 0x00BA1824 must be re-located in code and the .data
  location re-mapped (§4.3).
- Per prior FALSIFIER_REACH_CHECK.json: on the 4057 callsite path (0x0059AB12),
  FUN_0072F580 / FUN_0043A550 are NOT called; the immediate 4057 there is a
  string-table composite key {section_object, 4057} into the sids.vfs-loaded string map
  (0x98-manager singleton DAT_00BA12F4 via FUN_00415670) — a DIFFERENT namespace.
  This run does NOT reopen that chain except to state the namespace distinction.

## 2. DEFINITIONS / DISTINCTIONS (preserved VERBATIM all run)

- template definition 4057 -> model 218757 is a definition/resource relation,
  NOT a world instance.
- sids string-table id 4057 is a DIFFERENT namespace (its label is currently
  UNRECONCILED between prior records — do not cite either label as resolved).
- MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED.
- WORLD_XYZ_RECOVERED = NO.
- no CMO+0x44 -> X promotion.
- 0x0085B1B0 / 0x0095D3C4 bodies remain CLOSED this run.
- no T+0x10 producer investigation in this run.
- NO_DIRECT_XREF != DEAD_CODE (QH-007) — absence of direct calls is not death proof;
  address-taken/indirect classes must be enumerated before any such statement.

## 3. PRE-REGISTERED PASS/FAIL GATES

- **G1 CENSUS_COMPLETE**: every reference class enumerated for both functions with
  method + result per class. PASS requires no silently skipped class; NOT_CHECKED
  classes allowed only if explicitly listed with reason — then G1 = PARTIAL.
- **G2 CALLER_CLASSIFIED**: every in-budget direct caller has
  (VA, window bounds, id-source class, returned-object role class) with byte-anchored
  evidence; UNKNOWN provenance explicitly marked, never guessed.
- **G3 IDENTITY**: EXE SHA unchanged before/after; historical packages byte-unchanged
  (verified before AND after — baseline of the prior landmark package tree captured
  before work: 84 files, HISTORICAL_BASELINE_BEFORE.txt in local scratch).
- **G4 NO_PROMOTION**: zero XYZ/placement/building-instance claims; zero runtime
  claims; every finding labeled STATIC_ONLY with its evidence maturity level.

Non-pass classes: UNRESOLVED_CALLER_ROLE, INCONCLUSIVE_CENSUS, BUDGET_EXHAUSTED
(honest stop).

## 4. PRE-REGISTERED ENUMERATION PLAN (reference classes + methods)

For BOTH FUN_0072F580 (0x0072F580) and FUN_0043A550 (0x0043A550) separately:

| # | Class | Method (pre-registered) |
|---|-------|------------------------|
| C1 | direct CALL rel32 (E8) | Ghidra getReferencesTo(entry) filtered isCall() AND independent raw-byte scan of .text for `E8 rel32` with target == VA (dual method; both must agree, disagreements listed) |
| C2 | tail call / thunk JMP rel32 (E9) | raw-byte scan of .text for `E9 rel32` with target == VA; a hit whose function body is only that JMP = THUNK; a JMP at the end of a larger body = TAIL_CALL |
| C3 | indirect/computed calls | Ghidra references with flow_type.isComputed() and isCall(); PLUS raw scan for the VA used as an immediate (PUSH imm32 / MOV imm32 / any 4-byte LE occurrence) — such hits are the only static way an indirect call could reach the VA; genuinely register-computed calls (target never appearing as a constant) are NOT statically enumerable — declared NOT_CHECKED with reason if no immediate hits exist |
| C4 | address-taken refs | raw 4-byte LE scan of the ENTIRE file (all sections) for the VA value; every hit classified: code immediate vs data location; section recorded |
| C5 | data references | subset of C4: hits in .rdata/.data/.tls (non-code) — recorded with section + surrounding-dword context (vtable-like or not) |
| C6 | vtable slots | C4/C5 hits in .rdata where surrounding dwords are also code VAs (vtable-shaped run) — heuristic classification, labeled as such |
| C7 | callbacks | C4/C5 hits in data tables whose registration cannot be proven statically without chasing beyond scope — classified by location context only; semantics = UNRESOLVED (honest label) |
| C8 | thunks | covered by C2 (whole-function JMP) |
| C9 | jump tables | C4 hits located in Ghidra-recognized jump-table data (checked via raw hit location vs any Ghidra data-type; if unknown, recorded as data hit with UNKNOWN table semantics) |
| C10 | any other reference class Ghidra reports to the entry (getReferencesTo unfiltered, op_type recorded) | exhaustive dump of ALL reference types; anything not in C1..C9 is listed with its op_type verbatim |

NOT_CHECKED honest classes (pre-declared): none beyond the register-computed-call
limitation in C3 (fully stated above). No dynamic/runtime method is used at all.

## 5. PRE-REGISTERED WINDOW RULES (declared BEFORE analysis)

### 5.1 Declared re-pin windows (census subjects — allowed reads)
- **W-SUBJ-1**: FUN_0072F580 body @ 0x0072F580 — full listing + decompile, to
  re-verify: (a) it is a function; (b) whether it calls FUN_0043A550 (0x0043A550);
  (c) which map primitive it calls (prior hypothesis: FUN_004D1430 — NOT re-decoded,
  only the call edge is recorded); (d) its ABI (this/args/ret).
- **W-SUBJ-2**: FUN_0043A550 body @ 0x0043A550 — full listing + decompile, to
  re-verify: (a) it is a function; (b) whether it references DAT_00BA1824 (0x00BA1824);
  (c) its return.
- **W-SUBJ-3**: DAT_00BA1824 location @ 0x00BA1824 — PE-mapped file offset (or
  zero-initialized tail of .data if beyond raw size — record which); raw bytes at the
  location; every raw 4-byte-LE scan hit of 0x00BA1824 in the whole file (this
  enumerates the code references to the tree datum).
- Bodies 0x0085B1B0 and 0x0095D3C4 stay CLOSED. Callee bodies found inside caller
  windows stay CLOSED this run (their call edges are recorded, their bodies are not
  decoded).

### 5.2 Caller windows (budget: MAX 12 analyzed in depth)
- Window start: the containing function entry of a direct-call callsite (per Ghidra
  function manager).
- Window end rule (documented, per trap L24): the containing function body end per
  Ghidra (flow-terminated), cross-checked by requiring the terminating instruction to
  be a RET-class instruction (RET / RET imm16) or followed by alignment padding
  (90/CC/int3 or the next function's prologue). If the callsite is NOT inside any
  defined function, the window is the bounded raw dump [callsite-0x100, callsite+0x100]
  and the window rule is recorded as UNOWNED_WINDOW (classification of id provenance
  = UNKNOWN per contract).
- Window hard cap: 64 KB of instructions. A caller larger than the cap gets its
  callsite neighborhood (±32 KB) dumped and is marked
  WINDOW_RULE=TRUNCATED_LARGE_FUNCTION, CLASSIFICATION_LIMIT=CALLSITE_NEIGHBORHOOD.
- For each caller window, classify:
  - (i) **id-source class** of the template-id argument at the call:
    IMMEDIATE_CONSTANT (value recorded) / REGISTER_OR_STACK_FROM_LOCAL (provenance
    inside window, recorded) / FIELD_READ (base+offset recorded) /
    UNKNOWN_PROVENANCE_LEAVES_WINDOW (never guessed — recorded verbatim as UNKNOWN).
  - (ii) **returned-object role class**: what the caller does with the value returned
    by the lookup: IGNORED / STORED_TO_LOCAL / STORED_TO_FIELD (base+offset) /
    FORWARDED_TO_CALL (callee VA recorded) / FIELD_ACCESS_READ (offsets+VAs recorded,
    byte-anchored) / FIELD_ACCESS_WRITE (offsets+VAs recorded, byte-anchored) /
    TRANSFORM_RELEVANT (any access at an offset with float/transform/position-plausible
    evidence visible IN-WINDOW — FPU loads, float stores; labeled BYTE_OBSERVATION only,
    never promoted to placement claims).
- If more than 12 direct callers exist (across both functions), the excess is recorded
  in the census table as IDENTIFIED_NOT_ANALYZED with count. Do not exceed the budget.

## 6. PRE-REGISTERED BUDGETS

- Caller windows analyzed in depth: MAX 12.
- Ghidra headless: REUSE of the existing LANDMARK4057 project at
  D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003\proj
  (disclosed; its imported sandbox Entropia.exe was re-hashed this run:
  E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 = expected, PASS).
  No re-import; -process Entropia.exe -noanalysis + postScripts. If the project fails
  to open, fall back to a FRESH project (disclosed).
- Raw byte scans: single pass over the 8,015,872-byte file per target value.
- No model/asset/NIF/GLB/ARK/VFS/BNT physical reads. No runtime/network experiments.

## 7. HARD STOPS (pre-registered)

- EXE SHA mismatch at any check (before/after) — STOP, HARD_STOP.
- Any historical package byte change — STOP, HARD_STOP.
- Ghidra unable to produce the census (tooling state recorded honestly; nothing
  fabricated) — STOP, HARD_STOP.
- Budget exhausted (more than 12 in-depth windows needed for G2 completeness) —
  honest stop class BUDGET_EXHAUSTED.

## 8. FORBIDDEN (acknowledged)

- new model/asset/NIF/GLB/ARK/VFS/BNT physical reads; runtime/network experiments;
  history rewrite; modifying any historical audit package or AUDIT_ENTRYPOINT.md
  (it does not currently exist at docs/audits/AUDIT_ENTRYPOINT.md — nothing to touch);
  new decode of bodies other than the declared windows (§5.1 subjects, §5.2 caller
  windows); `python -B` invocation discipline for all pure-Python scripts and zero
  .pyc residue anywhere (scratch and package) at the end.

## 9. DELIVERABLES (pre-declared)

- PREREGISTRATION.md (this file, written before science)
- 01_RAW\ — census artifacts: raw xref listings, per-caller disassembly excerpts with
  bytes, byte re-pin outputs, Ghidra postscript outputs
- CALLER_CENSUS.json — machine-readable: per reference class, per caller
- FINAL_REPORT.md
- HANDOFF.md
- EVIDENCE_INDEX.md
- SCRATCH stays local-only (scripts + logs + intermediate outputs; script SHA256s
  recorded in EVIDENCE_INDEX.md). No MANIFEST (persistence phase is the orchestrator's).
