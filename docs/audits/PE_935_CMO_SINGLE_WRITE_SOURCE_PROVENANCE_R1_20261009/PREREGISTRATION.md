# PREREGISTRATION — PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009

Written BEFORE the physical EXE re-pin (contract §3/§8 discipline: question,
exact budget, candidate priority rule and falsifiers are fixed here before any
new measurement). RUN_CLASS = BOUNDED_STATIC_RE; RUN_TYPE =
CMO_SINGLE_WRITE_RECEIVER_AND_VALUE_SOURCE. Era: PCG 9.3.5 / Entropia
Universe 9.3.5. STATIC-ONLY: no client execution, no runtime, no network, no
payload/VFS/BNT/NIF opening, no Gamebryo/OpenMW research, no transform RE, no
placement/XYZ interpretation. BASE_SHA b2feef34122d2118da6ab38fc78f20f337315570
(git triple verified at preflight; see INPUT_IDENTITIES.md).

## 1. The single pre-registered question (contract §1)

Establish for ONE original instruction, if a defensible anchor exists:

`ORIGINAL BYTES -> EXACT MEMORY STORE -> DESTINATION / BASE RECEIVER ->
STORED VALUE -> IMMEDIATE VALUE SOURCE`

Leads: `CMO+0x44`, `CMO+0x48`, `CMO+0x4C`. NONE of these is pre-confirmed as a
CMO write, field identity, vector, coordinate, world XYZ or building placement
(contract §1). "CMO" is a hypothesis to prove by base-pointer lineage, not a
substitute for it. Valid terminal source classifications:
DIRECT_FUNCTION_ARGUMENT / COPY_FROM_MEMORY / CONSTANT / LOCALLY_COMPUTED_VALUE
/ RETURN_FROM_CALLEE (callee unknown) / CONDITIONAL_MULTIPLE_SOURCES /
UNRESOLVED_WITHIN_BOUND.

## 2. Exact pre-registered budget (contract §8) — STOP BEFORE EXCEED

| Item | Limit | Pre-registered use |
|---|---|---|
| Target store instructions analyzed | 1 max | 1 selected store: 0x0085B281 `89 4E 44` (mov dword ptr [esi+0x44], ecx) in FUN_0085B1B0 (see §4 selection) |
| New detailed function bodies | ≤1, restricted to the selected store's enclosing function | FUN_0085B1B0 ONLY — and, honestly: FUN_0085B1B0 is ALREADY a fully decoded function in committed prior evidence (PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 06_REPORT/REPORT.md §4.1 "0085B1B0 (pełne)" with raw region 01_RAW/... T1_REGION_0085B100_0085B900.txt [commit-tracked]; PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 01_RAW/DECOMP/F0085B1B0.c; PE_NIGHT_AGGREGATE_20260905_160000 Ghidra disasm 0085b27a..0085b28d). This run performs a bounded PHYSICAL RE-PIN of the store window + an INDEPENDENT boundary decode + the store-specific provenance derivation. ZERO new body semantics are claimed as newly opened; the body is charged to the 1-body budget as the selected body in its already-decoded (re-pin) status. |
| New call edges followed | 0 | 0 new. The two edges used are ALREADY committed evidence: FUN_00528E50 -> FUN_0085B1B0 (call @0x00528E8D; PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 REPORT S8 "base FUN_0085B1B0 @0x00528E8D"; PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 REPORT.md §4.1; PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_202601006 FUNCTION_LEDGER) and FUN_0085B1B0 -> FUN_00746560 (call @0x0085B27A; the callee is the pinned 4-byte accessor `8D 41 08 C3` in PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 01_RAW/F00746560_CTOR_COPY.txt + T1 region). Both re-pinned physically; neither callee body is opened (FUN_00746560's 4 bytes are a prior pin re-read; FUN_00528E50's body is prior canon, only the 3 already-pinned instructions are re-read). |
| New callee bodies | 0 | 0. FUN_007345C0, FUN_004123D0, FUN_00746550, FUN_00746570, FUN_0040B070 bodies are NOT read this run. |
| Xref / callgraph expansion | 0 | 0. No new caller/callee census. Anchor discovery searched COMMITTED DOCUMENTATION ONLY (see ANCHOR_SELECTION.md §2 boundary); no EXE-wide scan. |
| Unrelated function bodies | 0 | 0. |
| Newly promoted semantic field roles | 0 | 0. FIELD_SEMANTICS ceiling pre-registered = UNVERIFIED (see §5). |
| Runtime / network / terrain / NIF-BNT-VFS / Gamebryo-OpenMW / Three.js / building census / placement interpretation | 0 | 0 (STATIC-ONLY). |

Windows to read (all bounded, all overlapping PRIOR pinned scope only):
W1 = [0x0085B1A8, 0x0085B290) (0xE8 bytes; inside the committed
T1_REGION_0085B100_0085B900 window); W2 = [0x00746560, 0x00746564) (4 bytes;
prior pin F00746560_CTOR_COPY.txt); W3 = [0x00528E74, 0x00528EA8) (0x34 bytes;
prior pins: `8B F1` @0x00528E76, call @0x00528E8D, vtable store @0x00528EA2 —
MICRO_R1/attribute-seam canon); RTTI chains of vtables 0x00A7DCB0 and
0x00A91E4C (prior pins: MICRO_R1 RTTI_PROBES.json; attribute seam QC-5) —
same read method as Source B's own RTTI gate. No other EXE byte is read.

## 3. Mandatory active standing carried VERBATIM (contract §3)

```
PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED
NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION
SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE
```

- J3 (PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007)
  SUPERSESSION.md S-5 supersedes source-A `SAME_INSTANCE_TRANSFORM_RELATION =
  CONFIRMED_STATIC` as an ACTIVE run-qualified conclusion. This run does not
  restore it, does not call it a re-pin, claims no retroactive authorization.
- Historic J3 `ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL` (22 analyzed edges vs
  limit 6) is PRESERVED as the historical record; its count is NOT transferred
  to this run (this run: edge budget 0 used).
- Object distinctions enforced: CMO / SF (possibly [CMO+0xC0] on a historically
  measured path) / NiNode ([SF+0x30]) / NiAVObject transforms are PHYSICALLY
  DIFFERENT objects. `CMO+0x4C` is NOT `SF+0x4C`, NOT `NiNode+0x5C`, NOT
  m_kLocal/m_kWorld. The historically observed FUN_00509510 `rep movsd` to
  SF+0x4C must NOT be asserted as a CMO store. ACLD and CMO holders are not
  joined by class similarity.
- PLUS4 standing preserved (scope FAIL; [R+4]:=P first-init bounded conditional
  static; T==P and later inequalities NOT_ESTABLISHED; P heap origin
  NOT_ESTABLISHED) — not subjects of this run.

## 4. Candidate priority rule (fixed BEFORE selection; see ANCHOR_SELECTION.md for the census)

Primary: a defensible anchor = an EXACT memory-store instruction (not a load,
lea, stack store or argument preparation) to one of CMO+0x44/+0x48/+0x4C, with
physical-byte support in COMMITTED evidence, whose base register provably
carries the CMO-family instance (receiver lineage). Prefer the
physical-byte-supported exact store with receiver lineage; if genuinely tied,
lowest exact verified VA.

Pre-registered application to the committed census (all committed-evidence
candidates are listed in ANCHOR_SELECTION.md §3):

1. The bulk zero-init family (fst dword [esi+0x44/0x48/0x4C] @0x0085B1E4/E7/EC)
   is a 12-field bulk float-zero idiom (+0x44..+0x70); selecting its three
   members would be manufacturing a candidate "from three adjacent numerical
   offsets" (contract §4 prohibition), and its immediate value source is a
   degenerate CONSTANT with no producer chain. Ranked BELOW the copy family.
2. The record-copy family (mov dword [esi+0x44],ecx @0x0085B281; [esi+0x48],edx
   @0x0085B287; [esi+0x4C],eax @0x0085B28D) is the value-determining write
   group (straight-line body: no branch between the zero-init and the copy; the
   copy overwrites the zero-init in the same construction sequence) and matches
   the committed-evidence claims ("[+0x44..0x4C]=[FUN_00746560(record)+0..8]" —
   PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 REPORT.md §4.1 item 4 +
   ERRATA_R5; PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 REPORT S9/RESEARCH_FINDINGS).
   Its stored value has a real, in-body, directly evidenced producer chain.
3. Within the copy family (genuinely tied): lowest exact verified VA ->
   **SELECTED STORE = 0x0085B281, expected bytes `89 4E 44`
   (mov dword ptr [esi+0x44], ecx), enclosing function FUN_0085B1B0
   (entry 0x0085B1B0).**

Alternative honestly disclosed: a strictly mechanical lowest-VA reading across
ALL qualifying stores would pick the zero-init fst @0x0085B1E4 with a CONSTANT
source; this pre-registration records why that reading is rejected (bulk-init
idiom = the anti-manufacturing clause; degenerate value provenance; overwritten
by the copy in the same straight-line execution). The full census (all six
store VAs with bytes) is preserved in ANCHOR_SELECTION.md so the selection can
be independently re-adjudicated.

## 5. Pre-registered falsifiers (contract §5/§9 semantics)

- F1 INSTRUCTION_IDENTITY: physical bytes at 0x0085B281 are NOT `89 4E 44`
  (a MOV r/m32,r32 memory store) -> ANCHOR_REVALIDATION=FAIL ->
  SCIENCE_OUTCOME=ANCHOR_NOT_ESTABLISHED (no synthetic rescue).
- F2 BOUNDARY: independent linear decode from the padding-proven start
  0x0085B1B0 does not land an instruction boundary at 0x0085B281 with size 3,
  or is ambiguous -> INSTRUCTION_IDENTITY = UNVERIFIED -> anchor not
  established (finalize per §4).
- F3 RECEIVER: the store base register (ESI) cannot be tied to the ctor entry
  `this` within the body (clobber / alternate reaching definition) ->
  WRITE_CONFIRMED_RECEIVER_UNRESOLVED.
- F4 VALUE: the source register chain ECX <- [EAX] <- FUN_00746560(ECX=EDI=arg1)
  is broken by a clobber/alternate path within the body ->
  WRITE_RECEIVER_CONFIRMED_SOURCE_UNRESOLVED.
- F5 J3/SEMANTIC: if this run's own outputs restore a superseded transform
  claim, conflate CMO+0x4C with SF+0x4C / NiNode+0x5C / m_kLocal, or promote
  +0x44/+0x48/+0x4C to position/XYZ/world-coordinate semantics as an ACTIVE
  finding -> process control failure (must be corrected before finalization).
- FALSIFIER_REJECTED_HYPOTHESIS will be used ONLY if unmodified original-client
  bytes and the examined path contradict a pre-registered real hypothesis.
  Synthetic mutation rejection establishes CONTROL_PASS only (contract §9).

## 6. Pre-registered status ceilings (contract §10)

- INSTRUCTION_IDENTITY: target CONFIRMED (physical re-pin + independent
  boundary decode + committed cross-references).
- RECEIVER_IDENTITY: target CONFIRMED scoped to the examined construction
  path (FUN_00528E50 -> FUN_0085B1B0 same-object chain). Temporal nuance
  pre-registered: at store time the object carries the BASE vtable 0x00A91E4C
  (.?AVMovableObject@@); the DERIVED vtable 0x00A7DCB0
  (.?AVClientMovableObject@@) is stamped by FUN_00528E50 AFTER the base ctor
  returns, on the SAME object memory. The receiver is honestly described as
  "the MovableObject under construction that FUN_00528E50 turns into a
  ClientMovableObject", not as a finished CMO at store time.
- VALUE_PROVENANCE: target CONFIRMED as COPY_FROM_MEMORY (stored value = the
  dword at [arg1+8]; arg1 = the ctor's first stack argument; producer chain
  inside the selected body + the already-pinned 4-byte accessor). The arg
  pointer's upstream identity is NOT re-derived this run (historical committed
  context only, clearly labeled).
- FIELD_SEMANTICS: UNVERIFIED (ceiling; no promotion; the historical
  "position" label of record+8..0x10 / instance+0x44..0x4C in prior committed
  evidence is cited ONLY as historical context with its own recorded
  axes/units-UNRESOLVED caveats).
- WORLD_INSTANCE_IDENTITY: NOT_ESTABLISHED. HISTORICAL_PLACEMENT:
  NOT_ESTABLISHED. WORLD_XYZ_RECOVERED = NO (terminal, unconditional for this
  run). GLOBAL_COORDINATE_FRAME = NOT_ESTABLISHED. INSTANCE_MODEL_JOIN =
  NOT_ESTABLISHED.
- Coverage split: CLIENT_KNOWLEDGE_COVERAGE = one store's write provenance in
  the CMO construction chain (bounded, this run); RECONSTRUCTION_IMPLEMENTATION_
  COVERAGE = NONE (no implementation touched); HISTORICAL_GAME_RECOVERY_
  COVERAGE = NONE (no historical value recovered).

## 7. Method pre-registration

- Physical reads: Source B reused READ-ONLY
  (docs/audits/PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008/03_SCRIPTS/checker_plus4_successor_v2.py,
  38568 B / SHA256 80EBEE27883AA61173737590FB822B3503B4658CDA511B4B690F8E75B6B64E62,
  import-inertness verified by full read: constants/classes/`__main__` guard
  only, `sys.dont_write_bytecode=True`). API used: `load_pinned()` (fail-closed
  size+SHA), `RangeSafePE.read/raw_offset/u32`.
- Disassembler: capstone is NOT installed in this environment and installing
  packages is not authorized; the independent decode is this run's own minimal
  pure-stdlib x86-32 instruction-length/ModRM decoder
  (03_SCRIPTS/x86_minidec.py, version recorded in its output), cross-checked
  against the committed prior decodes (T1_REGION raw bytes; PE_NIGHT_AGGREGATE
  Ghidra disassembly; committed capstone decodes). Boundary proof = linear
  decode from the CC-padding-proven function start 0x0085B1B0 through past the
  selected store; disagreement anywhere = UNVERIFIED per contract §5.
- All scripts run `python -B`; no bytecode residue; the EXE file is never
  modified (mutations are in-memory copies only).

## 8. Expected outcome class (pre-registered prediction)

If the committed-evidence candidate holds against the physical bytes:
SCIENCE_OUTCOME = A (WRITE_AND_IMMEDIATE_SOURCE_ESTABLISHED) with
VALUE_SOURCE_CLASS = COPY_FROM_MEMORY and VALUE_PRODUCER_VA = 0x0085B27F
(`8B 08` mov ecx, [eax]; address producer = call FUN_00746560 @0x0085B27A with
ECX = EDI = arg1). Any falsifier firing instead produces the corresponding
honest outcome (B/C/D/E) per contract §13.
