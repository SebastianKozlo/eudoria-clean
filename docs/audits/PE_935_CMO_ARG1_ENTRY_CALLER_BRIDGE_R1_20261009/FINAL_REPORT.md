# FINAL_REPORT — PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009

```text
RUN_ID      = PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009
RUN_CLASS   = BOUNDED_STATIC_ARGUMENT_PROVENANCE
BASE_SHA    = ce75b7b3ee0b7b87c1f0a03bc79167169aed71a0
STATIC_ONLY = the client never ran; EXE reads limited to whole-file hash,
              PE header/section mapping and the two pinned window ranges
SCIENCE_OUTCOME = ENTRY_ARG1_AND_SINGLE_CALLER_BRIDGE_ESTABLISHED (CONDITIONAL)
```

## 1. Run and contract identity

- RUN_ID: PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009 (RUN_CLASS
  BOUNDED_STATIC_ARGUMENT_PROVENANCE) — the two-window entry-frame + single
  caller bridge micro-run.
- Authoritative contract:
  `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_ENTRY_CALLER_BRIDGE_PROMPT_REVIEW_20261009\OPENCODE_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_REVISED_20261009.md`
  — 23187 B, SHA256
  773C1310A2CB02B365068EE2D9C684A97765E4D416E30B415B8672D8CC09FF07 —
  verified byte-for-byte MATCH by the executor retry session, the fresh QC and
  PE-MASTER before any action. The dispatch authorizes exactly this one
  bounded static experiment (a one-time bounded exception; the standing lack of
  general static-placement authorization is NOT lifted); no milestone
  authority, no follow-up experiment.
- Executor: pe-reconstruction (first session model `nask-glm/glm-5-2` —
  crashed; retry session model `nask-glm/glm-5-3` — produced the science).
  Fresh internal QC: pe-master-auditor fresh-context (model
  `nask-glm/glm-5-3`), internal to PE-MASTER. PE-MASTER MASTER_AUDIT:
  advisory (ADVISORY_PRE_QUALIFICATION). NO_NESTED_TASKS; each phase directly
  dispatched by the parent.

## 2. Preflight (measured)

- Git triple at science: LOCAL_HEAD == origin/master == ACTUAL remote master
  (live ls-remote) == ce75b7b3ee0b7b87c1f0a03bc79167169aed71a0 == contract
  EXPECTED_BASE_SHA. Tracked worktree/index clean; foreign untracked paths
  (5 unrelated PE_935_* packages + experiments/) inventoried and untouched.
- EXE identity: Entropia.exe 8015872 B / SHA256
  E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 — rehashed
  3x independently (executor retry, fresh QC, PE-MASTER) and re-hashed before
  and after every analysis mode: UNCHANGED. No EXE access in this persistence
  phase.
- All 8 required repo inputs at BASE verified physically (size + SHA256) AND
  equal to the corresponding Git blob (incl. the two historical listings'
  pinned blobs 3648e1b86aa6933df6017840a20704f04e642bc1 /
  dc61d1b45df788b257c49771c0e55668fa2036b8 and AUDIT_ENTRYPOINT.md 273796 B /
  9F5E83940ECD0496FA21310C5AEAFE6F49D4631F86D495BF4E536548B6AD84A5).
  See INPUT_IDENTITIES.md I6.
- Governance/standing read (contract §0/§2; CMO_C1; J3 SUPERSESSION +
  CORRECTED_STATUS_ALGEBRA; prior ARG1_PROVENANCE.json): no genuine
  authorization conflict; the dispatched scope is not blanket milestone
  authority.

## 3. Session crash/continuation disclosure (two-session origin, mechanically proven)

The FIRST executor session (model glm-5-2) crashed mid-run and returned an
empty handoff, leaving exactly 3 files under OUTPUT_ROOT: PREREGISTRATION.md
(19151 B / F36DE40AF53CEE9FE2F0F5A11A65475239E5035DE96F2FD45D4E5669E775EACC),
01_RAW/WINDOW_A_OBJDUMP.txt (1882 B / 7AABA008…) and
01_RAW/WINDOW_B_OBJDUMP.txt (1557 B / B82C5533…). The fresh retry session
(glm-5-3):

1. reviewed PREREGISTRATION.md in full against the contract — complete and
   PRE-consistent; KEPT as the preregistration of record, extended only by the
   dated P10 continuity disclosure. MECHANICAL PROOF (fresh QC): the first
   19151 bytes of the current PREREGISTRATION.md hash EXACTLY to the crashed
   session's discovery SHA F36DE40A… — P10 is a pure append; P1–P9 are
   byte-identical with the pre-science preregistration; PRE was never rewritten
   to match POST.
2. re-ran its own fresh objdump invocations on independently extracted window
   fixtures — disassembly sections BYTE-IDENTICAL to both crash-left files
   (A: 23/23 lines, B: 17/17 lines; rc 0; fixture SHAs equal the contract
   pins); both files KEPT unchanged; the retry's own raw outputs additionally
   persisted as WINDOW_A_OBJDUMP_RETRY.txt / WINDOW_B_OBJDUMP_RETRY.txt.
3. re-performed the ENTIRE preflight and re-derived ALL science with its own
   pipeline (no unverified claim reused from the crashed session).

The model-origin change glm-5-2→glm-5-3 is recorded honestly in
PREREGISTRATION.md P10 / INPUT_IDENTITIES.md I2.

## 4. Window identities, PE mapping and tool provenance

| Window | Half-open VA interval | Bytes | Raw offset | SHA256 (physical == pin) | Decode |
|---|---|---:|---:|---|---|
| A | [0x00528E50,0x00528E92) | 66 | 1216080 / 0x128E50 | F8735567340CD3BE2F6B64B4BBC2BE292487E97B6184758CA408E6FF1CE78E85 | PASS — 23 instructions, exact cover (last CALL ends exactly at 0x00528E92) |
| B | [0x004C4792,0x004C47C6) | 52 | 804754 / 0x0C4792 | B59E16DC116F4CE0438A1E92BC6B2CBC33FAB0B19FABC24CB3A29C911C1EFB6A | PASS — 16 instructions, exact cover (last CALL ends exactly at 0x004C47C6) |

Both windows map uniquely into `.text` (RVA range [0x1000,0x6745E5), RAW-backed
raw range [0x1000,0x675000); raw offset == RVA for .text;
PointerToRawData == VirtualAddress == 0x1000) — no ambiguous/BSS mapping.
Intervals disjoint; 66+52 = 118 unique original code bytes (== the max).
Boundary provenance: pinned raw offsets + the pinned historical instruction
streams (F00528E50_CTOR_MOBJ.txt / F004C46C0_CREATE.txt — input records only);
function starts never inferred from CC/RET padding or E8 searches.

Tool: WSL GNU objdump (GNU Binutils for Debian) 2.44, distro PE-AI (Debian,
kernel 6.18.33.2-microsoft-standard-WSL2), raw-binary mode
`objdump -D -b binary -m i386 -M intel --adjust-vma=<VA> <fixture.bin>`, rc 0
recorded for every invocation; raw outputs persisted verbatim
(01_RAW/WINDOW_{A,B}_OBJDUMP.txt [crash-left, verified-kept] +
_WINDOW_{A,B}_OBJDUMP_RETRY.txt + 12 CONTROLS fixture outputs). Commands and
return codes recorded in each raw file. GNU objdump is the ONLY decoder in this
run; the symbolic replay helpers consume objdump output, never a handwritten
listing.

## 5. Phase A — entry frame and value preservation (ENTRY_FRAME_VALUE_IDENTITY = PASS)

E = symbolic ESP at entry 0x00528E50. The entire physical A window (23
instructions; instruction-by-instruction derivation in ENTRY_FRAME_LEDGER.csv)
yields:

- ESP chain: PUSH −1; PUSH handler; MOV EAX,FS:[0]; PUSH EAX → E−0x0C; SUB
  ESP,0x1C → E−0x28; PUSH EBX; PUSH ESI; PUSH EDI; MOV EAX,ds:0xB9D8D0; XOR
  EAX,ESP (value combine — changes a value, not the push width); PUSH EAX →
  **S = E−0x38** (ESP at 0x00528E76). LEA and FS:[0] operations do not adjust
  ESP (measured).
- Three preservation/identity proofs, derived separately:
  (a) slot-address equivalence: the source load
      `mov edi,DWORD PTR [esp+0x3c]` @0x00528E84 at ESP=S reads
      **[S+0x3C] == [E+4]** — the entry first stack-argument slot (AS2);
  (b) entry-slot value preservation: write census
      [0x00528E50,0x00528E84) = 8 stack writes ([E−4], [E−8], [E−0xC],
      [E−0x2C], [E−0x30], [E−0x34], [E−0x38] via PUSHes; [E−0x28] via the
      `mov [esp+0x10],esi` store) + 1 FS:[0] TIB segment write — **ZERO
      writes at [E+4]** (AS4: FS/TIB disjoint from the live argument stack
      region);
  (c) EDI preservation: EDI's reaching definition at PUSH EDI @0x00528E8A is
      the load @0x00528E84; the two intervening PUSHes do not write EDI.
- Delivery at CALL 0x00528E8D (hardware return-address push): ESP_before =
  E−0x44 = **S−0xC** (three net pushes after S); callee entry ESP = E−0x48 =
  **S−0x10**; callee arg1 slot **[S−0xC]**, written by PUSH EDI with the value
  loaded from [E+4]; target **0x0085B1B0** (rel32 e8 1e 23 33 00 recomputed
  == objdump); receiver ECX = entry ECX via ESI (mov esi,ecx @0x00528E76;
  mov ecx,esi @0x00528E8B) — a separate channel from arg1. Delivery at entry
  does not require the callee to return.

Gate: ENTRY_FRAME_VALUE_IDENTITY = PASS (straight-line examined path only; no
claim about alternate entries/paths; no full signature inferred from visible
pushes).

## 6. Phase B — caller path and value (CALLER_PATH_AND_VALUE = PASS, after clean A)

T = ESP at 0x004C47AF. Instruction-by-instruction derivation in
CALLER_STACK_LEDGER.csv (NULL + NONNULL paths; 16 instructions):

- Opaque call: `push 0x128` @0x004C4792; CALL 0x0095D3C4 @0x004C4797 (rel32
  verified; body NEVER opened); `add esp,0x4` @0x004C479C. AS3 (assumption):
  normal ABI-compatible return — pops exactly its return address (ESP
  restored), return value in EAX. Under AS3, **T = window-start ESP, delta 0**.
- Flags: TEST EAX,EAX @0x004C47A3 defines ZF := (EAX==0); the only intervening
  instruction `mov [esp+0x3c],0x0` writes no flags (census: empty
  intervening-writer set); JE @0x004C47AD branches precisely on EAX==0; its
  target 0x004C47C8 lies OUTSIDE window B and is never opened.
- Qualified branch (EAX≠0): loads ECX := [T+0x50], EDX := [T+0x4C]; three
  PUSHes → ESP = T−0xC; **LEA ECX,[ESP+0x14] @0x004C47BA = ADDRESS(T−0xC+0x14)
  = ADDRESS(T+8)** — opcode 0x8D, kind ADDRESS (a computed address, NOT a
  memory read); PUSH ECX → **[T−0x10] := ADDRESS(T+8)**; MOV ECX,EAX
  @0x004C47BF → receiver = the opaque call's EAX return value; CALL
  0x004C47C1 (rel32 e8 8a 46 06 00 recomputed) → **0x00528E50**; hardware
  return push → callee entry ESP = **T−0x14 = E**; entry arg1 slot
  **[E+4] = [T−0x10] containing ADDRESS(T+8) — NOT MEM(T+8)**.
- Null branch (EAX==0): ZF=1 → JE taken → control exits the window at
  0x004C47C8; the constructor CALL is NOT reached; NO delivery fabricated;
  nothing asserted about the out-of-window branch or allocation success.

Gate: CALLER_PATH_AND_VALUE = PASS (EAX≠0 branch only; ESI's producer at
T remains UNKNOWN — outside window B, untraced).

## 7. The bridge (CROSS_CALL_IDENTITY = POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL)

Join: **E = T−0x14** (the callee-entry ESP measured in Phase B).

- Slot-address identity: Phase-A source slot [E+4] ≡ Phase-B prepared arg1
  slot [T−0x10] — derived both ways (A-side: [S+0x3C] = [E+4] with S=E−0x38
  and E=T−0x14 → [T−0x10]; B-side: final PUSH lands at [T−0x10] = [E+4]).
- Value preservation across the join: combined write census in ONE coordinate
  system (T-terms) between the B-side write @0x004C47BE and the A-side load
  @0x00528E84 — the hardware return-address push lands at [T−0x14]; all A-side
  writes are at or below [T−0x18]; the only writes above T are the two B-side
  caller-frame stores at [T+0x3C]/[T+0x44]; **ZERO intervening writes to the
  joined slot [T−0x10]**.
- Result: **the SAME pointer value ADDRESS(T+8) is delivered as arg1 of
  FUN_00528E50 at CALL 0x004C47C1 AND as arg1 of FUN_0085B1B0 at CALL
  0x00528E8D** (via the load into EDI @0x00528E84 and PUSH EDI @0x00528E8A).

Conditions (all explicitly stated; the bridge is CONDITIONAL):

| ID | Condition |
|---|---|
| AS1 | 32-bit x86 stack semantics (push = ESP−4 then store; call = ESP−4 then store return address) |
| AS2 | [ESP_at_entry+4] is the first explicit stack-argument slot (cdecl order) |
| AS3 | the opaque callee 0x0095D3C4 returns normally ABI-compatibly (pops exactly its return address; value in EAX); body never opened |
| AS4 | FS segment base (TIB) disjoint from the live argument stack region |
| AS5 | straight-line window-A path from entry 0x00528E50 (the examined path only) |
| — | EAX≠0 at 0x004C47AD (the qualified branch only; the EAX==0 branch exits the window) |

NOTHING about [T+8] contents/type/lifetime/caller-frame-layout/history is
claimed; pointee contents remain UNRESOLVED_UPSTREAM. No uniqueness claim
across unexamined callers/entries/paths.

## 8. Controls — 24 matrix outcomes (production + fresh QC)

12 cases × (production + fresh-QC analysis) = 24 separately recorded expected
outcomes (test outcomes, not 24 independent scientific discoveries). Same
byte → objdump → symbolic-analysis pipeline on every case; identity hashes
qualify ORIGINAL inputs only (synthetic fixtures never rejected by hash);
mutations in synthetic temp copies only (EXE never altered; temp fixtures
removed; python -B).

| Case | Change (synthetic copy) | Production outcome | QC outcome |
|---|---|---|---|
| A_CLEAN | original A | CONTROL_PASS (S=E−0x38; source [E+4]; preserved; delivered) | CONTROL_PASS (own re-derivation; agrees) |
| B_CLEAN_NONNULL | original B, EAX≠0 | CONTROL_PASS (CALL reachable; arg1 ADDRESS(T+8); receiver OPAQUE_RET) | CONTROL_PASS (agrees) |
| B_CLEAN_NULL | same original B, EAX==0 | CONTROL_PASS (JE taken; CALL not reached; no fabricated delivery) | CONTROL_PASS (delivered = None) |
| M1_A_FRAME | SUB 0x1C→0x18 @0x00528E5E | CONTROL_PASS (S=E−0x34; source [E+8]) | CONTROL_PASS (agrees) |
| M2_A_SLOT | disp 0x3C→0x38 @0x00528E84 | CONTROL_PASS (source [E] under original frame) | CONTROL_PASS (agrees) |
| M3_B_LEA_DISP | disp 0x14→0x18 @0x004C47BA | CONTROL_PASS (arg1 ADDRESS(T+0xC)) | CONTROL_PASS (agrees) |
| M4_B_LAST_PUSH | PUSH ECX→PUSH EDX (51→52) @0x004C47BE | CONTROL_PASS (arg1 = MEM(T+0x4C), kind STACK_READ) | CONTROL_PASS (agrees) |
| M5_B_EARLY_PUSH_ORDER | push ecx/push edx swapped (51 52→52 51) | CONTROL_PASS (arg1 ADDRESS(T+8) + slot UNCHANGED; arg3/arg4 swapped reported) | CONTROL_PASS (arg1-retention verified independently) |
| M6_B_SKIP | JE→JMP (74 19→EB 19) @0x004C47AD | CONTROL_PASS (unconditional exit; no delivery) | CONTROL_PASS (agrees) |
| M7_B_RECEIVER_ONLY | MOV ECX,EAX→MOV ECX,ESI (8B C8→8B CE) | CONTROL_PASS (arg1 + slot UNCHANGED; receiver ESI/unknown producer) | CONTROL_PASS (agrees) |
| M8_B_WRONG_TARGET | rel32 +1 @0x004C47C1 (E8 8A→E8 8B 46 06 00) | CONTROL_PASS (actual target 0x00528E51 recomputed → bridge_valid=False; wrong target NOT followed — the real target predicate, not a hash failure) | CONTROL_PASS (agrees) |
| M9_B_LEA_TO_MOV | LEA→MOV (8D 4C→8B 4C) @0x004C47BA | CONTROL_PASS (arg1 MEM(T+8), kind STACK_READ; no pointee interpretation) | CONTROL_PASS (agrees) |

**All 24 outcomes CONTROL_PASS/QUALIFIED.** M5/M7 prove the checkers retain
unchanged arg1 facts while reporting the altered other channel (no blanket
fixture-rejection shortcut); M8 reaches the actual-target predicate; the QC's
expected facts were re-encoded directly from contract §7 (not copied from the
production table). Raw per-case outputs: 01_RAW/CONTROLS/<CASE>_OBJDUMP.txt
(12 files).

## 9. Artifact controls (both gates)

- Baseline: the persisted load-bearing artifacts (WINDOW_IDENTITIES.json,
  ENTRY_FRAME_LEDGER.csv, CALLER_STACK_LEDGER.csv, BRIDGE_PROVENANCE.json)
  re-read through the ordinary final gate — **21/21 fact checks PASS** on the
  executor gate AND **21/21 PASS** on the QC's independently implemented gate
  (instruction addresses/bytes, all three CALL targets by rel32 recompute, ESP
  states, ADDRESS-vs-MEM kind vs opcode 0x8D, entry-slot identity — facts,
  not just counts/field presence).
- AC1 (copied BRIDGE_PROVENANCE.json with ADDRESS(T+8)→MEM(T+8)): REJECTED by
  both gates (PROV-B-KIND / PROV-B-LEA fail) → CONTROL_PASS.
- AC2 (copied artifact with [E+4]→[E+8]): REJECTED by both gates (PROV-A-SLOT
  fails) → CONTROL_PASS.
- Overall: **ARTIFACT_CONSISTENCY_PASS**. Hash/manifest bypasses confined to
  the two isolated synthetic copied artifacts (OS temp dir, outside Git,
  removed); no historical file mutated.

Separate gates used (no generic SCIENCE_PASS, no semantic classifier):
ORIGINAL_IDENTITY / DECODE_COVERAGE / ENTRY_FRAME_VALUE_IDENTITY /
CALLER_PATH_AND_VALUE / CROSS_CALL_IDENTITY / REQUIRED_CONTROLS /
ARTIFACT_CONSISTENCY.

## 10. Fresh internal QC (honest scope)

- QC_ORIGIN = pe-master-auditor fresh-context internal QC (2026-10-09,
  OpenCode agent pe-master-auditor, model glm-5-3) — **internal to
  PE-MASTER; NOT an independent Desktop post-audit; NOT executor
  self-review**. PE_MASTER_REVIEW is internal/advisory.
- Independence dimensions, honestly stated: own byte extraction / hashing / PE
  mapping; own objdump invocations (rc recorded); own symbolic replay
  implementation (03_SCRIPTS/qc_frame_bridge.py, 83103 B / EC9F3FBE…; does
  NOT import the production script; no production-ledger import into any
  derivation); own ESP walk; own expected-fact encoding from contract §7;
  own artifact gate. The SAME GNU objdump 2.44 is the only disassembler on
  both sides — **the same GNU objdump is NOT two independent disassemblers**
  (no cross-disassembler claim made).
- QC_VERDICT = **QC_PASS** — executor claim adjudication 56/56 field
  agreement on the load-bearing facts (zero disagreements); its own 12 matrix
  outcomes 12/12 CONTROL_PASS; the production half verified field-by-field
  (24/24 total); artifact controls re-run through its own gate (baseline
  21/21, AC1/AC2 rejections); the crash/continuation adjudicated WITH
  MECHANICAL PROOF (the 19151-byte prefix hash F36DE40A… = pure P10 append);
  the executor's 7 pipeline repairs adjudicated HONEST (fail-closed code; the
  EXPECTED table used only as the contract comparison table; defective
  intermediates preserved on disk).
- Open QC findings (all P3, non-blocking; a correction needs a new human
  decision): **F-QC-1** — the 7 executor repairs disclosed to the parent but
  not persisted as package documents (immaterial; final artifacts re-derive
  exactly); **F-QC-2** — CALLER_STACK_LEDGER.csv duplicates the JE row as a
  PATH FORK annotation (cosmetic); **F-QC-3** — the QC's own 3 tooling
  repairs disclosed (xor reg,esp opaque-combine acceptance; adjudication
  formatting; zero executor artifacts touched).

## 11. PE-MASTER MASTER_AUDIT (advisory)

- VERDICT = **MASTER_ACCEPTED** (advisory; ADVISORY_PRE_QUALIFICATION —
  PE-MASTER remains PROVISIONAL_UNTIL_QUALIFIED; CANONICAL_GATE_EFFECT =
  NONE).
- PE-MASTER independently re-verified, physically (pre-preflight): window
  A/B identities (bytes/SHA/raw offsets); **9 instruction byte pins from the
  physical EXE with a full PE-section parser** — LEA `8D 4C 24 14`
  @0x004C47BA; MOV ECX,EAX `8B C8` @0x004C47BF; CALL `E8 8A 46 06 00`
  @0x004C47C1 → target 0x00528E50; SUB `83 EC 1C` @0x00528E5E; MOV EDI
  `8B 7C 24 3C` @0x00528E84; TEST `85 C0` @0x004C47A3; JE `74 19`
  @0x004C47AD; PUSH ECX `51` @0x004C47BE — ALL MATCH; and **the bridge
  arithmetic by hand**: E−0x38+0x3C = E+4; T−0xC+0x14 = T+8; T−0x10−4 =
  T−0x14; [E+4] = [T−0x10] — CONSISTENT.
- Operational disclosure: one PE-MASTER counter-check script initially used a
  wrong simplified `.text` offset shortcut and produced apparent mismatches;
  re-run with the full section table — ALL MATCH (a PE-MASTER tooling error,
  disclosed; no package evidence affected).
- Full verbatim review persisted as PE_MASTER_REVIEW.md (this package).

## 12. Scope census (measured; contract §4)

```text
AUTHORIZED_PARTIAL_CODE_WINDOWS        = 2 of max 2   (A 66 B, B 52 B; disjoint)
UNIQUE_ORIGINAL_CODE_BYTES_ANALYZED   = 118 of max 118  (66 + 52; exactly the max)
COMPLETE_FUNCTION_BODIES_TO_OPEN       = 0
NEW_CALLEE_BODIES                      = 0   (0x0085B1B0 / 0x0095D3C4 unopened)
TARGET_CALLSITES_ANALYZED              = {0x004C47C1, 0x00528E8D}  (2 of 2)
INCIDENTAL_OPAQUE_CALLSITE             = 0x004C4797 -> 0x0095D3C4 (opaque; AS3; body never opened)
UPSTREAM_BEYOND_WINDOW_B               = 0
OTHER_CALLSITES_OR_XREF_CENSUS         = 0
FIELD_SEMANTIC_PROMOTIONS              = 0
RUNTIME / NETWORK / MODEL / VFS_BNT_NIF_RE = 0
Gamebryo/OpenMW research/loading       = 0
```

Raw-VA census (fresh QC) over all 16 persisted raw objdump files: every decoded
VA lies inside window A or B — 0 VAs outside; zero package evidence of callee
bodies, other code or upstream. python -B; temp fixtures outside Git, removed;
no .bin window extracts committed (01_RAW artifacts are disassembly TEXT
only); no residue.

## 13. Standing preserved (verbatim; SUPERSESSION_AND_STANDING.md)

```text
S = ESP at 0x00528E76, not function-entry ESP
0x00528E84: EDI := DWORD [S+0x3C]
0x00528E8A: PUSH EDI
0x00528E8D: CALL 0x0085B1B0
ARG1_DIRECT_SOURCE = CONFIRMED_STATIC_CONDITIONAL
UPSTREAM_PROVENANCE = UNRESOLVED_UPSTREAM (prior bounded result)
CMO_C1 = CLOSED_FOR_AUDITED_STATE
CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL
PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED
NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION
SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE
```

No ACLD↔CMO identity transfer; R/P/T, PLUS4 and CMO-C1 correction loops remain
closed in their audited scopes; J3 preserved (no restoration); historical
labels such as record/position are not type evidence; the [arg1+8] →
MovableObject+0x44 store NOT reinterpreted; its callee NOT re-opened. The
prior ARG1_DIRECT_SOURCE result is PRESERVED and re-derived independently
(consistent, not superseding); UPSTREAM_PROVENANCE is extended by exactly ONE
qualified delivery boundary (this run's conditional bridge) and remains
UNRESOLVED_UPSTREAM beyond it.

## 14. Science outcome and terminal governance

```text
SCIENCE_OUTCOME = ENTRY_ARG1_AND_SINGLE_CALLER_BRIDGE_ESTABLISHED (CONDITIONAL)
  — the first upstream delivery boundary of the audited callsite qualified:
    the SAME pointer value ADDRESS(T+8) delivered as arg1 of FUN_00528E50 at
    CALL 0x004C47C1 and as arg1 of FUN_0085B1B0 at CALL 0x00528E8D
    (conditions AS1/AS2/AS3/AS4/AS5 + the EAX!=0 branch; pointee and earlier
    producer remain untraced).

POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM
FIELD_SEMANTICS = UNVERIFIED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
INDEPENDENT_DESKTOP_POST_AUDIT = NOT_PERFORMED
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

**A successful pointer delivery does NOT qualify the contents of the stack
area** ([T+8] is not read, typed or interpreted here) **and grants NO
historical XYZ claim**: no position, NiPoint3, world instance, building,
network packet, model or coordinate is assumed or established. WORKS !=
UNDERSTOOD. There is NO automatic upstream continuation: the pointee's
producer, the opaque callee body, the EAX==0 branch, the ESI-at-T producer and
everything beyond window B remain unopened by design; any next experiment
requires a separate human authorization.
