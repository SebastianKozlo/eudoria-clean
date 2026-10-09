# FINAL_REPORT — PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009

RUN_ID = `PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009`
RUN_CLASS = BOUNDED_STATIC_RE
RUN_TYPE = CMO_SINGLE_WRITE_RECEIVER_AND_VALUE_SOURCE
PHASE = finalization/persistence (executor + fresh internal QC + PE-MASTER advisory review complete; this report finalizes the package)

## 1. Run identity and authorization

- Human-authorized frozen contract: `C:\Users\User\Downloads\OPENCODE_CMO_SINGLE_WRITE_PROVENANCE_R1_REVISED.md`
  — 20158 B, SHA256 `C6599C0CCEB93DA5CD0E6B950DC3EF8AE6826FA962ABE99492F3931C7244CEB5`
  — identity verified MATCH by executor, fresh QC and PE-MASTER before any work.
- Single pre-registered science question (contract §1): for ONE original instruction, if a
  defensible anchor exists — `ORIGINAL BYTES → EXACT MEMORY STORE → DESTINATION / BASE RECEIVER →
  STORED VALUE → IMMEDIATE VALUE SOURCE`.
- Authorization boundary: ONE bounded micro-run only. Terminal by contract §0:
  `NEXT_EXPERIMENT_AUTHORIZED=NO`, `HARD_STOP=YES`.
- Repository: `SebastianKozlo/eudoria-clean`, branch `master`.
- EXPECTED_BASE_SHA = `b2feef34122d2118da6ab38fc78f20f337315570` (measured identical by
  executor, QC and PE-MASTER; commit made at persistence per §14).
- Target: `Entropia.exe` (PCG_9_3_5) — 8015872 B, SHA256
  `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` — rehashed before and
  after the run by the executor and independently by QC; unchanged. STATIC-ONLY: the client
  never ran.

## 2. Preflight (fail-closed, measured)

- BASE triple equal: local HEAD == origin/master == actual remote `refs/heads/master` ==
  `b2feef34122d2118da6ab38fc78f20f337315570` (live ls-remote; re-verified at persistence).
- Tracked tree clean; OUTPUT_ROOT created fresh; foreign untracked census recorded and untouched.
- All 7 pinned source-pair identities MATCH (source A 4 files, source B 1 file, J3 2 files);
  further required historical-context files pinned read-only with measured identity;
  `PROJECT_STATE.json` absent — recorded N/A, not invented; `AUDIT_ENTRYPOINT.md` read as
  the governance input.
- Source J3 (`SUPERSESSION.md` 8339 B / `DD11137A…`, `CORRECTED_STATUS_ALGEBRA.md` 8987 B /
  `00D09B0F…`) — identity MATCH; S-5 read BEFORE any source-A use.

## 3. Anchor discovery and selection (committed evidence only)

- Search scope: previously documented CMO-related forensic evidence and scoped pre-existing
  disassembly ONLY (no EXE-wide xref scan, no generic subsystem search, no new callee analysis).
- Census result (ANCHOR_SELECTION.md): **6 qualifying stores** in FUN_0085B1B0 —
  the copy triple `89 4E 44` / `89 56 48` / `89 46 4C` @0x0085B281/0x0085B287/0x0085B28D
  and the zero-init fst triple `D9 56 44`/`D9 56 48`/`D9 56 4C` @0x0085B1E4/0x0085B1E7/0x0085B1EC
  — plus **10 reclassified/excluded records**, each genuine, each exclusion pin byte-verified
  by QC (including the FUN_00509510 `rep movsd` → `SF+0x4C` reclassification: NOT a CMO store;
  `CMO+0x4C` is not `SF+0x4C` per contract §3).
- Selection rule pre-registered (PREREGISTRATION.md): prefer the physical-byte-supported exact
  store with receiver lineage from the copy family over the zero-init bulk-idiom family
  (anti-manufacturing rule; the label `CMO` and three adjacent numeric offsets are not a
  candidate basis).
- Selected: the lowest-VA copy-family store `0x0085B281` (the honest lowest-VA tie-break
  alternative `fst @0x0085B1E4`, class CONSTANT, was disclosed and rejected with rationale:
  bulk zero-init idiom, not a value-source store).
- ANCHOR_DISCOVERY = SUFFICIENT.

## 4. A-outcome table (the established write)

| Field | Measured value |
|---|---|
| SELECTED_WRITE_VA | `0x0085B281` |
| WRITE_OPCODE_BYTES | `89 4E 44` (mov dword [esi+0x44], ecx; 3 B; 32-bit operand width) |
| WRITE_PHYSICAL_OFFSET | 4567681 (`0x45B281`) |
| WRITE_FUNCTION_START_VA | `0x0085B1B0` (FUN_0085B1B0; boundary proven: `C3` + 3×`CC` @0x0085B1AC-AF) |
| WRITE_DESTINATION_OPERAND | `[esi+0x44]` |
| RECEIVER (temporal nuance) | ESI = the FUN_0085B1B0 ctor `this` = the **MovableObject-under-construction** (base vtable `0x00A91E4C` = `.?AVMovableObject@@` stamped @0x0085B1C1, bytes `C7 06 4C 1E A9 00`), which FUN_00528E50 then stamps `0x00A7DCB0` = `.?AVClientMovableObject@@` on the SAME memory AFTER return (`C7 06 B0 DC A7 00` @0x00528EA2). **NOT a finished CMO at store time** — every claim site states this; no class-similarity conflation (SF/NiNode/CMO kept distinct). |
| VALUE_SOURCE_CLASS | COPY_FROM_MEMORY |
| VALUE_PRODUCER_VA | `0x0085B27F` (mov ecx,[eax] — `8B 08`) |
| INSTRUCTION_IDENTITY | CONFIRMED |
| RECEIVER_IDENTITY | CONFIRMED (scoped; temporal nuance QC-adjudicated SUPPORTED) |
| VALUE_PROVENANCE | CONFIRMED |
| FIELD_SEMANTICS | UNVERIFIED (ceiling kept; the historical 'position' label is prior context only) |
| WORLD_INSTANCE_IDENTITY | NOT_ESTABLISHED |
| HISTORICAL_PLACEMENT | NOT_ESTABLISHED |
| SCIENCE_OUTCOME | **A — WRITE_AND_IMMEDIATE_SOURCE_ESTABLISHED** |

## 5. Value chain (immediate source of the stored value)

```
FUN_0085B1B0 entry: arg1 at [esp+0x14]
  mov edi,[esp+0x14]      @0x0085B1DA      (arg1 -> edi)
  ...
  mov ecx,edi            @0x0085B24B      (edi -> ecx)
  call rel32             @0x0085B27A      (target recomputed 0x00746560)
FUN_00746560 (pinned 4-byte accessor, prior commit re-pin):
  lea eax,[ecx+8]                         (8D 41 08)
  ret                                     (C3)          -> eax = &arg1->field_8
  mov ecx,[eax]           @0x0085B27F      (8B 08)        -> ecx = *(arg1+8)
  mov [esi+0x44],ecx      @0x0085B281      (89 4E 44)     -> THE SELECTED STORE
```

- Straight-line 64-instruction/224-byte boundary decode inside FUN_0085B1B0 ends exactly at
  0x0085B290; QC's own clobber scans found zero intervening ESI/ECX/EDI writers and no calls
  in the open intervals (0x0085B24B,0x0085B27A) and (0x0085B27F,0x0085B281).
- Stored value = the dword at `[arg1+8]` — COPY_FROM_MEMORY, closest directly evidenced
  producer @0x0085B27F. arg1 upstream = committed historical context only (UNKNOWN beyond
  the ctor argument); the stored-dword representation f32-vs-u32 = UNKNOWN.
- ABI assumption disclosed: ESI/EDI preservation across FUN_007345C0 / FUN_004123D0 /
  FUN_00746550 / FUN_00746570 (bodies unread, callee-saved ABI) — a disclosed limitation,
  not contradicted by any measured byte.

## 6. Budget used (contract §8) — with ERRATA

| Budget item | Limit | Used |
|---|---|---|
| Target store instructions | 1 | **1/1** (0x0085B281; sibling stores +0x48/+0x4C byte-documented in the census, NOT analyzed) |
| New detailed function bodies | ≤1 (enclosing function only) | **1/1** — a re-pin of ALREADY fully-decoded committed evidence (T1_REGION raw + F0085B1B0.c + Ghidra H5); **0 new body semantics**; the 'already decoded' status charged honestly |
| New call edges followed | 0 | **0/0** (both used edges = prior committed evidence re-pinned: FUN_00528E50→FUN_0085B1B0 @0x00528E8D; FUN_0085B1B0→FUN_00746560 @0x0085B27A) |
| New callee bodies | 0 | **0/0** (FUN_00746560 = prior pin re-read, 4 B) |
| General xref/callgraph expansion | 0 | **0** |
| Newly promoted semantic field roles | 0 | **0** (FIELD_SEMANTICS = UNVERIFIED ceiling kept) |

### ERRATA — F-QC-1 (required; applied HERE, not as an in-place edit)

`FUNCTION_AND_EDGE_BUDGET.csv` (frozen executor ledger, NOT edited) row `windows_read`
declares: "RTTI chain 0x00A7DCB0 = 4+20+25 = 49 B … TOTAL EXE BYTES READ = 381 B".
**The correct number is 382 B**: the chain length is 4+20+26 = 50 B (the executor's own
script reads `len(".?AVClientMovableObject@@")+1 = 26` name bytes). Corrected ledger of
EXE bytes read this run: W1 [0x0085B1A8,0x0085B290) = 232 B; W2 [0x00746560,0x00746564) =
4 B; W3 [0x00528E74,0x00528EA8) = 52 B; RTTI chain 0x00A7DCB0 = 50 B; RTTI chain
0x00A91E4C = 44 B; **total = 382 B** (post-F-QC-1-errata; executor declared 381).
Non-material to any predicate, gate or contract limit: no limit depends on this number
and all read bytes lie inside prior-pinned windows (100% overlap with committed evidence).

## 7. Controls summary

- **M1–M6 synthetic mutation controls: CONTROL_PASS** (executor) — wrong-VA / wrong-opcode /
  wrong-width / wrong-destination-base (SF or NiNode instead of the ctor this) / wrong-offset /
  broken reaching-definition detectors each reject the corresponding mutant; fresh-context QC
  independently re-ran M1/M2/M3/M5 with its own mutants plus the SF-conflation control — all
  rejection behavior reproduced.
- **M7/M8 token gates: PASS** — QC's 12/12-file scan (including both `.py` scripts) found zero
  forbidden active standing; the single occurrence of `SAME_INSTANCE_TRANSFORM_RELATION =
  CONFIRMED_STATIC` in the package is explicitly tagged superseded; `WORLD_XYZ_RECOVERED=YES`
  occurrences: 0; object-conflation tokens: 0. (Executor's own gate scanned 10/12 file suffixes —
  see F-QC-4 observation below.)
- **FALSIFIER_REJECTED_HYPOTHESIS = NOT_TRIGGERED** — correct per contract §9: F1/F2 were
  evaluated on UNMODIFIED original-client bytes and found no contradiction; synthetic-mutation
  rejections establish CONTROL_PASS only and never alone prove the production hypothesis.
- Boundary/control liveness: the decoder fails closed; the 64-instruction boundary decode proves
  instruction starts for all 64 instructions including the selected store.

## 8. Active J3 standing (carried verbatim; no restoration)

```
PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED
NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION
SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE
```

- The earlier `SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC` in source A remains
  SUPERSEDED AS AN ACTIVE, RUN-QUALIFIED CONCLUSION (J3 SUPERSESSION.md S-5). NOT restored,
  NOT requalified, NOT treated as a valid finding of that prior run.
- J3 historical `ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL` (22 analyzed edges versus the
  original limit 6) preserved WITHOUT transfer — this run used **0** new edges.
- Object distinctions preserved (contract §3): CMO / SF / NiNode / NiAVObject local-world
  transforms kept physically distinct; `CMO+0x4C` is not `SF+0x4C`, `NiNode+0x5C`, `m_kLocal`
  or `m_kWorld`; the FUN_00509510 `rep movsd` → `SF+0x4C` is NOT asserted as a CMO store.

## 9. PLUS4 standing (unchanged; not subjects of this run)

Original scope violation `FAIL`; `[R+4]:=P` first initialization (bounded conditional static);
`T==P` and later inequalities NOT_ESTABLISHED; P heap origin NOT_ESTABLISHED — all preserved
unchanged; no PLUS4 package file touched.

## 10. Fresh internal QC and findings

- **QC_ORIGIN**: pe-master-auditor fresh-context internal QC — internal to PE-MASTER;
  NOT an independent Desktop post-audit, NOT MASTER_ACCEPTED, NOT milestone closure.
- **QC_VERDICT = QC_PASS** — 9/9 duties, every load-bearing measurement re-done from scratch:
  own PE parser, own x86-32 boundary decoder, own RTTI walk, own rel32 recomputation, own
  clobber scans, own mutants, own token scans; W1 232 B byte-identical with the executor's
  declaration; all pins MATCH; the receiver temporal-nuance wording survives adjudication
  (SUPPORTED, no correction required); QC made NO edits to any executor file.
- Findings carried into this report:
  - **F-QC-1 (P2, required errata — APPLIED in §6 above)**: budget byte-total off-by-one,
    declared 381 B → correct 382 B (RTTI 0x00A7DCB0 chain = 4+20+26 = 50 B). Non-material.
  - **F-QC-2 (P2, optional — documented errata note)**: `ANCHOR_SELECTION.md` §3.2 census row
    C-L says "fstp [ebp+0x44] @0x005093E9"; the physical bytes `D9 55 44` (ModRM reg=2) are
    **FST**, and the committed file also shows `fst` for both 0x005093E9 and 0x005093F1.
    Correct reading: `fst [ebp+0x44] @0x005093E9`. Non-material (receiver EBP=SF; the
    reclassification and the mov pins stand). The frozen census file is NOT edited in place;
    this note is the documented correction.
  - **F-QC-3 (P3, optional — documented errata note)**: `ANCHOR_SELECTION.md` §3.2 census row
    C-K claims "+0x48/+0x4C stores @0x00855260 region" but the cited committed file
    (T2_HEX/mgr_ctor_FUN_008550C0.txt) ends at 0x008551DF. QC's own EXE probe byte-verified
    `89 46 48` @0x00855260 — the claim is physically true; the citation path does not document
    it. Non-material (the primary pin `89 46 44` @0x008551CA is in the cited file and
    byte-verified). Source annotation recommended for any future use of that census row.
  - **F-QC-4 (P3, observation)**: the executor's token_gates.py scanned 10/12 package files
    (suffix filter `.md/.txt/.csv/.json`; the two `.py` scripts excluded). QC's 12/12 scan
    (including both scripts) is clean — zero forbidden active standing anywhere. No correction
    required for THIS package; future runs should include `.py` files or record their exclusion.
- Executor check-specification corrections disclosed during the run (boundary precondition
  slice; promotion-probe wrap-tolerance) did not alter any measured evidence.

## 11. PE-MASTER advisory review

- **MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE)** —
  PE-MASTER independently re-measured ALL load-bearing bytes from the physical EXE (selected
  store, function boundary, both chain hops, the accessor body, `mov ecx,[eax]`, both RTTI
  chains, both vtable stamps) — ALL MATCH. Persisted verbatim as `PE_MASTER_REVIEW.md` in
  this package. PE-MASTER remains PROVISIONAL_UNTIL_QUALIFIED; this verdict gates nothing.

## 12. Coverage classes (separate epistemology; no promotion)

- CLIENT_KNOWLEDGE_COVERAGE: the exact store instruction, its function boundary, the receiver
  lineage (ctor this + base vtable stamp + post-return CMO vtable stamp) and the immediate
  value chain (arg1+8 via the pinned accessor) are byte-established in the examined static
  scope — this is knowledge ABOUT the client binary.
- RECONSTRUCTION_IMPLEMENTATION_COVERAGE: NONE. No Three.js/runtime/reconstruction file was
  touched by this run; nothing here changes the reconstruction.
- HISTORICAL_GAME_RECOVERY_COVERAGE: NONE. **WORKS != UNDERSTOOD** — one write plus synthetic
  tests proves NOTHING about world XYZ, placement, the instance-model join, or any semantic
  field role. FIELD_SEMANTICS = UNVERIFIED; WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED;
  HISTORICAL_PLACEMENT = NOT_ESTABLISHED.

## 13. Open items (honest; not blockers)

- Sibling stores `89 56 48` (+0x48) @0x0085B287 and `89 46 4C` (+0x4C) @0x0085B28D are
  byte-documented in the census but unanalyzed (1-store budget honored).
- arg1's upstream identity beyond the ctor argument = UNKNOWN (committed historical context
  only).
- Stored-dword representation f32-vs-u32 = UNKNOWN.
- FIELD_SEMANTICS (+0x44) = UNVERIFIED (the historical 'position' label is prior context,
  not asserted by this run).

## 14. Terminal governance

```
STOP_SCIENCE = YES (terminal: one store done)
GLOBAL_COORDINATE_FRAME = NOT_ESTABLISHED
HISTORICAL_PLACEMENT_RECORD = NOT_ESTABLISHED
INSTANCE_MODEL_JOIN = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEW_DESKTOP_POST_AUDIT = NOT_PERFORMED
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

One physically grounded original-client write and the nearest demonstrable recipient/value
producer were established within budget. WORKS != UNDERSTOOD. NEXT_EXPERIMENT_AUTHORIZED=NO.
HARD_STOP=YES.
