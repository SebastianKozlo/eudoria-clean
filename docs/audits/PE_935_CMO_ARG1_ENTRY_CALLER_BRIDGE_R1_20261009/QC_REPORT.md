# QC_REPORT — PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009 (fresh-context internal QC)

```text
RUN_ID        = PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009
ASSIGNMENT    = FRESH-CONTEXT INTERNAL QC of the bounded micro-run (contract §8)
QC_ORIGIN     = pe-master-auditor fresh-context internal QC session (2026-10-09,
                OpenCode agent pe-master-auditor, model nask-glm/glm-5-3;
                python3 -B, WSL distro PE-AI, Debian,
                kernel 6.18.33.2-microsoft-standard-WSL2)
              = INTERNAL TO PE-MASTER. It is NOT an independent Desktop
                post-audit and NOT executor self-review. PE_MASTER_REVIEW is
                internal/advisory only; CANONICAL_GATE_EFFECT = NONE.
BASE_SHA      = ce75b7b3ee0b7b87c1f0a03bc79167169aed71a0 (HEAD verified
                unchanged before and after the QC; no publication actions,
                no stage/commit/push, no entrypoint write by this QC)
QC_OUTPUTS    = 03_SCRIPTS/qc_frame_bridge.py (83,103 B,
                SHA256 EC9F3FBE152E7694B0E2540E1BB4F399994BBAB81CE8B33B64495B25A3CE1688)
                + QC_RESULTS.json (109,626 B,
                SHA256 0DF6B9341CD8C4DEE31660747E867AAC11B3BCCDFCB77A13800B96E5AF0CD27D)
                + this QC_REPORT.md
QC_VERDICT    = QC_PASS  (per-duty basis below; all inputs to the verdict
                measured by this session's own tooling)
```

## 1. Method and independence (honest statement)

This QC re-verified EVERYTHING from physical bytes with its own tooling; it
did not import `run_frame_bridge.py` and did not use the executor's ledgers,
CONTROL_RESULTS.json or BRIDGE_PROVENANCE.json as derivation inputs. The
executor's artifacts were read in full and used only as ADJUDICATION targets
(field-by-field agree/disagree) and for the production-half comparison of the
24-outcome matrix.

Independence dimensions:

| Dimension | Status |
|---|---|
| Window extraction, hashing, PE mapping | INDEPENDENT (own parse of the PE headers/section table; own extraction at the pinned raw offsets) |
| Disassembler | SAME TOOL as production — GNU objdump (GNU Binutils for Debian) 2.44 via WSL PE-AI. **The same GNU objdump is NOT two independent disassemblers**; no cross-disassembler claim is made anywhere in this QC |
| objdump invocations | INDEPENDENT (this session's own commands; rc 0 recorded for every invocation; raw outputs embedded in QC_RESULTS.json) |
| Symbolic replay / derivation | INDEPENDENT implementation (`03_SCRIPTS/qc_frame_bridge.py`; written fresh for this QC; no import of the production script) |
| ESP walk | INDEPENDENT minimal arithmetic walk, separate from the replay engine |
| Expected control facts | re-encoded directly from the dispatched contract §7 matrix by this session (not copied from the production EXPECTED table) |
| Artifact gate | INDEPENDENT implementation (21 fact checks re-derived from physical bytes + my own objdump + my own walk) |

EXE read scope of this QC: whole-file hash (before AND after), PE
header/section mapping, and the two pinned window byte ranges only. The EXE
was never altered; all fixtures were temp copies outside Git (removed at the
end); `python3 -B`; no `.pyc`/`__pycache__` residue (verified).

## 2. Per-duty results

### D1 — Input identity and window verification (MY OWN measurements)

- Contract identity BEFORE any action: 23187 B /
  SHA256 773C1310A2CB02B365068EE2D9C684A97765E4D416E30B415B8672D8CC09FF07 — MATCH.
- EXE: 8,015,872 B / SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 —
  re-hashed by this QC BEFORE and AFTER all work: UNCHANGED.
- My own PE32 parse: ImageBase 0x400000, machine 0x014C, 5 sections;
  `.text` VA 0x1000 / VSize 0x6735E5 / RAW 0x1000 / RSize 0x674000.
  Window A RVA 0x128E50 → unique `.text` hit, RAW-backed,
  raw-offset formula 1216080 == pinned 1216080; window B RVA 0xC4792 →
  unique `.text` hit, raw-offset formula 804754 == pinned 804754; both
  windows entirely inside the `.text` raw range [0x1000,0x675000); no
  BSS/ambiguous mapping.
- Window A: 66 B extracted at raw offset 1216080, SHA256
  f8735567340cd3be2f6b64b4bbc2be292487e97b6184758ca408e6ff1ce78e85 == pin.
  Window B: 52 B at 804754, SHA256
  b59e16dc116f4ce0438a1e92bc6b2cbc33fab0b19fabc24cb3a29c911c1efb6a == pin.
  Disjoint intervals; 66+52 = 118 unique original code bytes (== max).
- My own fresh objdump invocations (rc 0) decode window A as 23 contiguous
  instructions covering [0x00528E50,0x00528E92) EXACTLY (last call ends at
  0x00528E92) and window B as 16 instructions covering
  [0x004C4792,0x004C47C6) exactly (last call ends at 0x004C47C6). Three
  visible CALLs: 0x004C4797→0x0095D3C4 (incidental opaque), 0x004C47C1→0x00528E50
  (bridge target), 0x00528E8D→0x0085B1B0 (tail target) — all rel32 targets
  independently recomputed from the byte streams by this QC (match).
- All 8 required repository inputs verified physically: sizes and SHA256s
  equal to the contract pins, and the two historical listings' Git blobs equal
  the pinned blob IDs (3648e1b86aa6933df6017840a20704f04e642bc1 /
  dc61d1b45df788b257c49771c0e55668fa2036b8).

### D2 — Phase A independently re-derived (MY OWN symbolic replay)

My instruction-by-instruction derivation (23 steps persisted in
QC_RESULTS.json `phase_a_mine.steps`) yields, with every delta measured from
the decoded stream (none assumed):

- E→S chain: PUSH −1; PUSH 0x9BF53F; MOV EAX,FS:[0]; PUSH EAX → E−0x0C;
  SUB ESP,0x1C → E−0x28; PUSH EBX/ESI/EDI; MOV EAX,ds:0xB9D8D0;
  XOR EAX,ESP; PUSH EAX → **S = E−0x38** (ESP at 0x00528E76). FS:[0] loads,
  LEA and the cookie computation do not adjust ESP (measured).
- Source load @0x00528E84 `mov edi,[esp+0x3c]` with ESP=S: byte displacement
  0x3C (read from the instruction bytes by this QC) + S → **source slot
  [E+0x4] == [S+0x3C]** — the entry first stack-argument slot (AS2).
- Write census before the load (enumerated exhaustively from my replay's
  write log): 8 stack writes — [E−0x4], [E−0x8], [E−0xC] (SEH prologue),
  [E−0x2C], [E−0x30], [E−0x34] (register saves), [E−0x38] (cookie) via
  pushes and [E−0x28] via the `mov [esp+0x10],esi` store — plus ONE segment
  write FS:[0x0] := ADDRESS(E−0xC) (the LEA-computed value; AS4: FS/TIB is
  not a stack alias). **Zero writes at [E+4]**; aliasing list empty.
- EDI preservation: EDI's reaching definition at PUSH EDI 0x00528E8A is the
  load @0x00528E84; the two intervening pushes do not write EDI.
- Delivery @CALL 0x00528E8D: ESP before call = E−0x44 = **S−0xC** (three
  net pushes after S); hardware return push → callee entry ESP =
  E−0x48 = **S−0x10**; callee arg1 slot **[S−0xC]** written by PUSH EDI
  with the value loaded from [E+4]; my rel32 recompute of e8 1e 23 33 00 →
  **0x0085B1B0** (== objdump == prior pin). Receiver ECX = entry ECX via
  ESI (mov esi,ecx @0x00528E76; mov ecx,esi @0x00528E8B) — separate channel.

**Agreement with the executor's Phase A claims: field-by-field 26/26 AGREE
** (window identity 5, S/slot/preservation/delivery 21 — see
QC_RESULTS.json `adjudication`; zero disagreements).

### D3 — Phase B independently re-derived (MY OWN symbolic replay)

My 2-path derivation (NULL + NONNULL; 16 instructions each; steps persisted)
yields:

- Opaque-call structure (byte-derived neighbor check): PUSH 0x128 before,
  CALL 0x0095D3C4 (rel32 recomputed from bytes — match), ADD ESP,4 after;
  callee treated opaque, AS3 (normal ABI-compatible return: pops exactly its
  return address; return value in EAX) recorded as an ASSUMPTION, body never
  opened. **T = ESP at 0x004C47AF = T0 (window-start ESP), delta 0 under
  AS3** — measured.
- Flags: TEST EAX,EAX @0x004C47A3 defines ZF; the only intervening
  instruction `mov [esp+0x3c],0x0` writes no flags (my independent flag-writer
  census between the two VAs: EMPTY); JE @0x004C47AD branches precisely on
  EAX==0; my rel8 recompute: target **0x004C47C8 — OUTSIDE window B**
  (not opened, not interpreted).
- EAX≠0 (qualified) branch: loads ECX:=[T+0x50], EDX:=[T+0x4C]; three
  pushes → ESP=T−0xC; LEA ECX,[ESP+0x14] @0x004C47BA — **opcode byte 0x8D**
  verified by this QC → kind ADDRESS (computed, not a read) →
  **ADDRESS(T−0xC+0x14) = ADDRESS(T+8)**; PUSH ECX @0x004C47BE →
  **[T−0x10] := ADDRESS(T+8)**; MOV ECX,EAX → receiver = the opaque return
  value; CALL @0x004C47C1: my rel32 recompute of e8 8a 46 06 00 →
  **0x00528E50** (== objdump); callee entry ESP = T−0x14 =: E; entry arg1
  slot **[E+4] = [T−0x10]** containing **ADDRESS(T+8) — the ADDRESS value,
  NOT DWORD [T+8]** (no pointee read). Arg slots at entry measured:
  arg1 ADDRESS(T+8), arg2 ESI (producer outside window B — unknown),
  arg3 MEM(T+0x4C), arg4 MEM(T+0x50).
- EAX==0 branch: ZF=1 → JE taken → control exits at 0x004C47C8 (outside);
  the target CALL is NOT reached; **no delivery fabricated** (my null-path
  record carries delivered = None).

**Agreement with the executor's Phase B claims: field-by-field AGREE on all
compared fields** (T/flags/opaque/LEA/arg1/arg2-4/receiver/call/null —
part of the 56-field adjudication; zero disagreements).

### D4 — Bridge join independently adjudicated (MY OWN join, one coordinate system)

My join converts all A-side offsets into the B-side T0 coordinate system via
the measured E = callee_entry(=T−0x14):

- **join E = T−0x14** (measured in Phase B), a_src_T0 = E+src = −0x10,
  b_arg1_T0 = −0x10 → **slot-address identity holds** ([E+4] ≡ [T−0x10],
  the SAME slot).
- Combined write census between PUSH ECX @0x004C47BE and the load
  @0x00528E84 in ONE coordinate system: B-side after the final push — only
  the hardware return push @0x004C47C1 at T0 −0x14; A-side — pushes at
  T0 −0x18/−0x1C/−0x20, the [E−0x28]→T0 −0x3C store, and the prologue
  writes at −0x40…−0x4C; **ZERO writes at T0 −0x10** → the slot value
  survives from the B-side write to the A-side load.
- Same-pointer-value conclusion: **the SAME pointer value ADDRESS(T+8)** is
  delivered (1) as arg1 of FUN_00528E50 at CALL 0x004C47C1 (slot [E+4] =
  [T−0x10]) and (2) as arg1 of FUN_0085B1B0 at CALL 0x00528E8D (the loaded
  EDI pushed at [S−0xC]). My join status =
  **POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL**, conditions AS1/AS2
  (x86 push/call + cdecl order), AS3 (opaque normal return), EAX≠0
  (qualified branch only), AS4 (FS/TIB disjointness), AS5 (straight-line
  window-A path).
- Nothing about [T+8] contents, type, lifetime, frame layout or history is
  claimed by my derivation either; the address/value/slot/pointee/receiver
  distinction is preserved throughout.

**Adjudication of the executor's bridge claims (join expr, slot identity,
value, intervening writes, status): ALL AGREE.**

### D5 — The 12-case matrix re-run through MY OWN analysis predicate

Fixtures built by this QC from MY OWN extraction of the EXE window bytes
(mutations per contract §7 applied to synthetic copies only; EXE untouched);
each case decoded by MY OWN objdump invocation and analyzed by MY OWN
implementation; expected facts re-encoded from the CONTRACT:

| Case | My verdict | Discriminating facts measured by my pipeline |
|---|---|---|
| A_CLEAN | CONTROL_PASS | S=−0x38; src slot +4; preserved; edi_ok; tail 0x0085B1B0; arg1 kind stack-read |
| B_CLEAN_NONNULL | CONTROL_PASS | T=0; call reachable; arg1 (ADDR,+8); slot −0x10; receiver OPRET; target 0x00528E50; flags ok; args 2-4 as claimed |
| B_CLEAN_NULL | CONTROL_PASS | JE taken (exit 0x004C47C8, outside); call NOT reached; delivered = None (no fabricated delivery) |
| M1_A_FRAME | CONTROL_PASS | S=−0x34 (−52); source [E+8] (not [E+4]) under the altered frame |
| M2_A_SLOT | CONTROL_PASS | source [E+0] (disp 0x38 under original frame) |
| M3_B_LEA_DISP | CONTROL_PASS | arg1 ADDRESS(T+0xC) (disp 0x18) |
| M4_B_LAST_PUSH | CONTROL_PASS | arg1 = the earlier EDX load value MEM(T+0x4C), kind stack-read (not the LEA address) |
| M5_B_EARLY_PUSH_ORDER | CONTROL_PASS | final arg1 ADDRESS(T+8) and slot −0x10 UNCHANGED; arg3/arg4 order changed (0x50/0x4C) — provenance not rejected for the unrelated difference |
| M6_B_SKIP | CONTROL_PASS | unconditional JMP exit; call not reached on any path |
| M7_B_RECEIVER_ONLY | CONTROL_PASS | arg1 ADDRESS(T+8) + slot UNCHANGED; receiver = ESI (UNK; producer unknown) |
| M8_B_WRONG_TARGET | CONTROL_PASS | actual target recomputed = 0x00528E51; bridge_valid=False; wrong target NOT followed (real target predicate, not a hash side-failure) |
| M9_B_LEA_TO_MOV | CONTROL_PASS | arg1 MEM(T+8) (opcode 0x8B read), kind stack-read; no pointee interpretation |

**My 12 outcomes: 12/12 CONTROL_PASS, 0 FAIL, 0 UNRESOLVED.** Every case
reached the REAL analysis (structured facts, decode coverage, path
reachability, CALL target, the precise qualified/rejected relation); M5/M7
retain unchanged arg1 facts while reporting the altered other channel; M8
reaches the actual-target predicate; B_CLEAN_NULL shows no fabricated
delivery. Identity hashes qualified ORIGINAL inputs only; no synthetic case
was rejected by hash.

**The other half of the 24-outcome matrix (production records vs my
independent measurements): 12/12 AGREE field-by-field** (kind nomenclature
mapped: production STACK_READ ↔ QC MEM, ADDRESS ↔ ADDR, OPAQUE_RET ↔ OPRET,
UNKNOWN_REG ↔ UNK; every mapped fact equal; production verdicts all
CONTROL_PASS). Together: **all 24 expected matrix outcomes hold**.

### D6 — Artifact controls re-run through MY OWN gate

- Baseline: the persisted load-bearing artifacts (WINDOW_IDENTITIES.json,
  ENTRY_FRAME_LEDGER.csv, CALLER_STACK_LEDGER.csv, BRIDGE_PROVENANCE.json)
  re-read through MY ordinary final gate — **21/21 fact checks PASS**
  (window SHA/size/interval vs physical EXE bytes; ledger rows vs my fresh
  parse + my independent ESP walk, incl. boundary-call ESP semantics;
  provenance facts — A source slot [E+0x4] from the disp byte + walk,
  A delivery E−0x44/E−0x48, B arg1 kind vs opcode byte 0x8D, LEA expr
  ADDRESS(T+0x8), joined slot identity [E+4]==[T−0x10], all three call
  targets by my rel32 recompute, flags census empty).
- AC1 (my copied BRIDGE_PROVENANCE.json with ADDRESS(T+8)→MEM(T+8)):
  **REJECTED by the same gate** (PROV-B-KIND and PROV-B-LEA fail) → CONTROL_PASS.
- AC2 (my copied artifact with [E+4]→[E+8]): **REJECTED** (PROV-A-SLOT
  fails) → CONTROL_PASS.
- Overall: **ARTIFACT_CONSISTENCY_PASS**. Hash/manifest bypasses applied
  only in these two isolated synthetic controls (copied artifacts in the OS
  temp dir outside Git; no historical file mutated).

### D7 — Crash/continuation and pipeline-repairs adjudication

Physical verification by this QC:

- The two crash-kept raw files hash EXACTLY to the discovery SHAs recorded
  in INPUT_IDENTITIES.md I2 (WINDOW_A_OBJDUMP.txt 1882 B /
  7AABA008CFBD8BAF4CDF868BA25E3E9A014E9F732E375402553AAA3282D2C86B;
  WINDOW_B_OBJDUMP.txt 1557 B /
  B82C5532D1E10EE3116C7E74EA72471257FA1E3A110F7BCFEA0C452B01ED99CC) —
  kept unchanged since discovery.
- **PREREGISTRATION.md: the first 19151 bytes of the current file hash to
  F36DE40AF53CEE9FE2F0F5A11A65475239E5035DE96F2FD45D4E5669E775EACC — the
  crashed session's discovery SHA.** Mechanical proof that P10 is a pure
  append: P1–P9 are byte-identical to the pre-science preregistration; PRE
  was never rewritten to match POST. P1–P9 were additionally reviewed in
  full: contract-derived hypotheses/controls only; no post-science leakage.
- My fresh objdump disassembly is BYTE-IDENTICAL to both the crash-kept
  files and the retry files (window A: 23 instruction lines; window B: 17
  text lines = 16 instructions + 1 continuation). The crashed session's
  outputs were sound and correctly kept; the retry's additional raw files
  are consistent.
- Executor's 7 disclosed in-run pipeline repairs (objdump LEA prefix;
  SymVal kind unification; M6 expected-facts fix; push-time value capture;
  ESP-expression parser; artifact-gate CALL-row semantics; ESP_DELTA
  format): adjudicated **HONEST — repairs to its own pipeline only**. I
  read `run_frame_bridge.py` TO EOF (2194 lines): the final code is
  fail-closed (Unresolved exceptions; no expected-result filling — the
  EXPECTED table is a comparison table encoded from the contract, used only
  for verdicts, and the M6 entry matches the contract's discriminating
  result); the persisted artifacts re-derive exactly through my independent
  gate (21/21) and my 12-case re-run (12/12 agree), so they come from the
  final revision. Issues surfaced as exceptions/gate-REJECTED first, not by
  silently rewriting results. One observation (P3): the 7 repairs are
  disclosed to the parent (handoff record) but not persisted as package
  documents — non-material; the defective intermediate artifacts that
  existed on disk (the crash-left files) ARE preserved.

### D8 — Scope and standing scan

- Raw-VA census over ALL 16 persisted raw objdump files: every decoded VA
  lies inside window A or window B; **0 VAs outside** → zero package
  evidence of callee bodies (0x0085B1B0 / 0x0095D3C4 unopened), no other
  code, no upstream beyond window B.
- Windows 2/2 (66+52 B); unique bytes 118/118 (disjoint, verified);
  callsites: 2 target (0x004C47C1→0x00528E50, 0x00528E8D→0x0085B1B0) +
  1 incidental opaque (0x004C4797→0x0095D3C4); 0 complete function bodies;
  0 callee bodies; 0 xrefs; 0 semantic promotions; 0 runtime/network/model/
  VFS-BNT-NIF RE; 0 Gamebryo/OpenMW research.
- Standing token scan over all 27 executor package files: **0 occurrences**
  of WORLD_XYZ_RECOVERED=YES, FIELD_SEMANTICS=VERIFIED,
  WORLD_INSTANCE_IDENTITY=ESTABLISHED, HISTORICAL_PLACEMENT=ESTABLISHED, or
  the J3-restoration form
  SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN=CONFIRMED_STATIC. All
  required fences PRESENT (ARG1_DIRECT_SOURCE = CONFIRMED_STATIC_CONDITIONAL
  preserved verbatim in SUPERSESSION_AND_STANDING.md §1 — carried, not
  reinterpreted; CMO_C1 = CLOSED_FOR_AUDITED_STATE;
  CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL; J3
  three lines verbatim; no ACLD↔CMO transfer — the only ACLD occurrences
  are fence statements; the only NiPoint3 occurrences are "no assumption"
  fences; FIELD_SEMANTICS = UNVERIFIED; POINTEE_CONTENTS_PROVENANCE =
  UNRESOLVED_UPSTREAM; WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED;
  HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO).
- Nothing about [T+8] contents/type/lifetime/history is claimed anywhere in
  the package (context adjudication of all "pointee" occurrences: fences
  only).

### D9 — PASS-record provenance (MEASURED / SOURCE / NON-CIRCULAR / FAILURE_CASE)

For every meaningful PASS this QC records (in QC_RESULTS.json and above):

- Phase A slot/preservation PASS:
  MEASURED = S chain + disp byte 0x3C + write census;
  SOURCE OF TRUTH = physical A bytes decoded by GNU objdump, replayed by an
  independent implementation; NON-CIRCULAR = no executor artifact entered
  the derivation; FAILURE CASE = controls M1/M2 (frame/slot mutations) flip
  S and the source slot exactly as the contract requires — the predicate
  discriminates.
- Phase B LEA/arg1 PASS: MEASURED = opcode byte 0x8D + disp 0x14 + ESP
  chain T−0xC; SOURCE = physical B bytes; NON-CIRCULAR = independent
  replay; FAILURE CASE = M3 (disp 0x18), M9 (0x8D→0x8B) and M4 (last push)
  all yield different, correctly-discriminated facts.
- Bridge PASS: MEASURED = slot identity + zero intervening writes in one
  coordinate system; SOURCE = both replays' write logs; NON-CIRCULAR =
  byte-derived census; FAILURE CASE = any write to [T−0x10] in the interval
  would be enumerated and would flip the join to REJECTED_SLOT_OVERWRITTEN;
  AC1/AC2 prove my final gate rejects mutated kind/slot claims.
- Matrix PASS: 12/12 through the real analysis predicate with the
  M5/M7 arg1-retention and M8 actual-target discriminations exercised.
- Artifact baseline PASS: 21/21 facts re-derived from physical bytes and
  fresh tool output, not from the artifacts under test.

## 3. QC verdict

```text
QC_VERDICT = QC_PASS

Basis (all measured by this session's own tooling):
  - clean A/B evidence predicates: ENTRY_FRAME_VALUE_IDENTITY and
    CALLER_PATH_AND_VALUE independently re-derived and CONFIRMED
  - CROSS_CALL_IDENTITY = POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL
    independently re-derived and CONFIRMED (conditions AS1-AS5 + EAX!=0)
  - all 24 expected matrix outcomes hold (my 12 CONTROL_PASS +
    production 12 verified field-by-field against my measurements)
  - artifact checks: baseline 21/21 + AC1/AC2 rejections (my own gate)
  - executor claim adjudication: 56/56 fields AGREE
  - crash-continuation physically verified (incl. the P10 pure-append proof)
  - scope/standing scan clean
```

This verdict is the fresh internal QC verdict only. It is NOT
MASTER_ACCEPTED, NOT milestone closure, NOT a canonical qualification, NOT
an independent Desktop post-audit, and carries no general
static-placement authorization. The positive bridge outcome remains
CONDITIONAL on AS3/AS4/EAX≠0/straight-line-window-A; WORKS ≠ UNDERSTOOD.

## 4. Coverage and NOT_CHECKED

FULL_READ_LOG (read to EOF by this session): the dispatched contract (305
lines); all 27 executor package files — PREREGISTRATION.md (314),
INPUT_IDENTITIES.md (191), WINDOW_IDENTITIES.json (108), both window raw
files (36/30), both retry files (38/32), all 12 control raw files,
ENTRY_FRAME_LEDGER.csv (24), CALLER_STACK_LEDGER.csv (26),
BRIDGE_PROVENANCE.json (662), CLAIM_MATRIX.csv (25), CONTROL_RESULTS.json
(1790), ARTIFACT_CONTROL_RESULTS.json (492),
SUPERSESSION_AND_STANDING.md (133), run_frame_bridge.py (2194 — the
load-bearing generator, read to EOF); plus this session's own outputs.

NOT_CHECKED (with reasons — none load-bearing for the QC verdict):

1. Cross-disassembler decoding: NOT PERFORMED — the same GNU objdump 2.44
   is the only disassembler in this QC (stated honestly; contract §4 forbids
   building/extending another x86 decoder).
2. AS3 (the opaque callee 0x0095D3C4's return behavior) and AS4 (FS/TIB
   disjointness at runtime): remain ASSUMPTIONS — statically unresolvable
   inside the authorized scope (callee unopened by design); the bridge stays
   CONDITIONAL on them.
3. Runtime behavior of any kind: NOT PERFORMED (STATIC_ONLY run; the client
   never ran; no runtime claims made by the executor either).
4. The out-of-window branch at 0x004C47C8 and everything beyond window B /
   before window A: NOT interpreted (scope fence; no package evidence
   exists — verified by the raw-VA census).
5. The historical listings F00528E50_CTOR_MOBJ.txt / F004C46C0_CREATE.txt:
   identity (size/SHA/blob) verified; their CONTENTS not re-derived (they
   are input records; the QC's independent boundary check is the exact
   window decode coverage from the pinned raw offsets).
6. The 7 pipeline-repair intermediate states of the executor's tooling:
   not persisted as files (only the final revision exists on disk); the
   repairs were adjudicated from the final code + disclosures (P3
   observation below).
7. Manifest/entrypoint/persistence phases: NOT this QC's assignment
   (parent phases; this QC performed no stage/commit/push).

## 5. Open findings (all non-blocking; a correction needs a new human decision)

- **F-QC-1 (P3, observation)**: the executor's 7 in-run pipeline repairs are
  disclosed in the parent-facing handoff but not persisted inside the
  package (no repair log file). Non-material: the final artifacts re-derive
  exactly under my independent gate/matrix, the code read to EOF is
  fail-closed, and the only on-disk defective-intermediate artifacts (the
  3 crash-left files) are preserved and verified. Suggested optional future
  note in FINAL_REPORT.md; no scientific claim affected.
- **F-QC-2 (P3, cosmetic)**: CALLER_STACK_LEDGER.csv repeats the JE row as
  a "PATH FORK" annotation row (17 NONNULL rows for 16 instructions). The
  duplicate VA row is presentation-only; the artifact gate and the
  instruction count (16, in WINDOW_IDENTITIES.json) are correct; no fact
  affected.
- **F-QC-3 (P3, disclosure — this QC's own repairs, all to THIS session's
  tooling, before final results; zero executor artifacts touched)**: (a)
  the first run of my replay fail-closed on `xor eax,esp` (ESP is tracked
  as an integer, not a register) — fixed by accepting xor reg,esp as an
  opaque value combine; (b) adjudication formatting initially reported 4
  cosmetic "disagreements" (decimal vs hex offset formatting and a
  double-formatted segment-write string) — fixed to the package's hex
  notation; the underlying facts never differed (52/52 factual agreement
  even before the fix; final 56/56). Both repairs are visible in
  03_SCRIPTS/qc_frame_bridge.py; no expected result was filled in; failures
  surfaced as exceptions/mismatches first.

## 6. Handoff pointers

Machine-readable evidence for every duty: `QC_RESULTS.json` (this package).
Bounded QC helper: `03_SCRIPTS/qc_frame_bridge.py` (this package). Temp
fixtures of this QC were created only under
`C:\Users\User\AppData\Local\Temp\opencode\QC_PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009\`
(outside Git; never staged; removed at the end of this session).

```text
QC_PASS_REQUIRES = all duties above hold with independent measurements — MET
NEXT_PARENT_ACTION = PE-MASTER adjudication → final report/review/standing/
                     evidence-index/handoff → entrypoint row → manifest →
                     path-limited commit/push (separate parent decision;
                     NOT performed and NOT authorized by this QC session)
```
