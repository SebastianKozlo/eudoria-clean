# ARG2_ANALYSIS.md — PE_935_SF_ARG2_PROVENANCE_R1_20260914

Executor: pe-reconstruction (PE-MASTER loop `2ed038db-5d2e-4e7e-b679-2d29bf57501a`,
EU935-M1 Phase 2). STATIC-ONLY: Entropia.exe never executed; own byte reads + own
capstone disassembly only; every script fail-closed on SHA256+SIZE+PE32 identity
before any analysis read. All evidence below is re-derived IN-RUN from the pinned
EXE (`E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`, 8015872 B).

The primary question (contract §C): WHO supplies FUN_0050A050's arg2 (the name
argument of the SF slot-3 primary-path virtual dispatch to the NiNode
named-object lookup), WHAT VALUES does it take, and WHAT is its semantic role?

---

## 1. The four statuses (independent evidence trails)

### 1.1 ARG2_ABI — **CONFIRMED** (measured)

`FUN_0050A050` fully decoded by own capstone (CS_ARCH_X86, CS_MODE_32, detail),
B.5 boundary derivation applied: **extent 0x0050A050..0x0050A0AA (90 B)** — the
iterative terminal+padding rule finds the first ret (`C2 08 00` @0x0050A084) is
NOT the extent end (live branch target follows; padding invalid), and the second
ret (`C2 08 00` @0x0050A0A7) IS: CC×6 run completes to the next 16-aligned VA
0x0050A0B0, and the adjacent start 0x0050A0B0 is corroborated by its own
E8/E9 refs (0x0044CC41 E8, 0x0044CC92 E9, 0x0044CD64 E9). Published extent
0x0050A050..0x0050A0AA: AGREES. (Raw: 01_RAW/FUN_0050A050_DISASM.txt)

Measured ABI:
- thiscall; `this` = ECX at entry.
- stack args at entry: `[esp+4]` = **arg1** (out float3 buffer), `[esp+8]` =
  **arg2** (the name/query pointer). Callee cleanup: **ret 8** measured at BOTH
  ret sites (0x0050A084 `C2 08 00`, 0x0050A0A7 `C2 08 00`).
- The exact **eax def chain** for the dispatch push: `mov eax,[esp+8]` @0x0050A050
  (`8B 44 24 08`) → `test eax,eax` @0x0050A054 (`85 C0`) → `je 0x50A087`
  @0x0050A059 (`74 2C`, arg2==NULL → fallback) → … → `push eax` @0x0050A060
  (`50`) — arg2 is pushed as the SINGLE stack argument of the link-vtable
  slot-17 dispatch (`ecx = [SF+0x30]` this; `mov edx,[ecx]`; `mov eax,[edx+0x44]`;
  `call eax` @0x0050A064). This is consistent with the standing B.2 signature of
  the slot-17 target (thiscall, one `const char*` stack arg, ret 4 — NOT
  re-derived here; only the permitted value check made: dword
  [0x00A8CCF4+0x44] == 0x007B5390 — MATCH).
- Second exit path (published NOT_CHECKED "shared-tail polymorphism" note — now
  CHECKED): after the slot-17 call, `test eax,eax; je 0x50A087` @0x0050A068
  (lookup returned NULL → fallback). The tail contains NO polymorphism: it is the
  published fallback (self-slot-1 vcall returning &SF+0x34, then X/Y/Z reads
  [eax]/[eax+4]/[eax+8] = SF+0x34/0x38/0x3C and copies to arg1[0..8]; return
  value = arg1). One calling convention throughout; no second entry ABI.
- **NC-1 (ABI known-answer): PASS — 9/9 dispatch-window + fallback pins MATCH
  byte-for-byte; 0 PIN_MISMATCH findings.**

Caller-side requirement derived from the measured ABI (used in the census): a
well-formed call site must hold the receiver in ECX at the call and push exactly
2 stack args (callee ret 8).

### 1.2 ARG2_PROVENANCE — **UNVERIFIED** (measured-and-bounded; no proven supplier)

Three censuses executed with rules + denominators (raws: 01_RAW/CENSUS_E8_DIRECT.txt,
01_RAW/CENSUS_IMM32_0050A050.txt, 01_RAW/VIRTUAL_CALLSITE_CENSUS.csv +
01_RAW/ARG2_PRODUCER_TRACE.txt):

- **(a) E8 census** (.text 0x00401000..0x00A75000, 6,766,592 B; every 0xE8/0xE9/0xEB
  byte position treated as a potential opcode): 156,829 E8 byte occurrences;
  **0 matches to 0x0050A050** (0 E9, 0 EB). FUN_0050A050 has NO direct callers.
  CAL-2 known-answer PASS (same machinery on FUN_005247C0 → exactly 7 sites).
- **(b) imm32 census** (whole file, every byte position): **exactly 1 hit** — the
  SF vtable slot-3 dword at 0x00A7D464 (NC-4: measured 0x0050A050 — MATCH).
  FUN_0050A050 is vtable-addressed ONLY: the channel is exclusively virtual.
  CAL-1 known-answer PASS (same scanner on 0x00A7D458 reproduces both published
  vtable stores: `mov [ebp],0xA7D458` @0x00509366 and `mov [esi],0xA7D458`
  @0x0050A269).
- **(c) Virtual call-site census** (declared bound: TWO levels, 48-byte backward
  decode window per level, multi-start with cross-chain agreement check):
  - Pattern enumeration: P1 `call [reg+0x0C]` = 1; P1J `jmp [reg+0x0C]` = 0;
    P2 disp32 = 0; P3 `mov dst,[base+0x0C]` = 7,106 occurrences pre-check, 217
    after the follow-check (call/jmp dst within ≤3 non-control instructions) —
    **218 candidates examined**.
  - Outcomes: **0 PROVEN SF receivers**; 211 INSUFFICIENT_PROOF (recorded with
    per-site def-form evidence); 5 REJECTED_NOT_SF (**NC-2 satisfied**: slot-3
    calls on `.?AVNiD3DHLSLPixelShader@@`/`.?AVNiD3DPixelShader@@` and
    `.?AVNiBoundingVolume@@` `this` receivers (vtable-extent-verified per the
    R1 amendment 2026-09-14: the enclosing method 0x007F1D70 is vtable slot 1
    of `.?AVNiBoundingVolume@@`) — the census demonstrably rejects non-SF
    receivers); 2
    NOT_A_VTABLE_CALL (no vtable load in window — e.g. `call [ebp+0xC]` @0x005B0163
    is a frame-slot call, not a vtable call).
  - CAL-3 (self-added known-answer calibration of the receiver tracer, NOT run
    evidence): pointed at the published receiver-proof site (receiver ECX of the
    E8 call @0x00529020 → FUN_005094C0), the tracer classifies
    PROVEN_HOLDER_0xC0 — PASS. The tracer is calibrated; the zero-PROVEN census
    outcome is a property of the data within the declared bound, not a
    broken-machinery artifact.
  - **Method-1 holder-slot route** (B.3 holder offsets 0x04/0x0C/0x10/0x14/0x18
    /0xC0, register bases, non-SIB, clobber-aware forward accumulation):
    25,905 holder-offset reads enumerated; 18 flow into a GENUINE slot-3 vcall
    within 48 B. **ABI disposition vs the measured FUN_0050A050 ABI: 17 of 18
    ABI_INCOMPATIBLE** (0, 1, or 4 effective stack args, or `this` pushed on the
    stack — none can be a well-formed FUN_0050A050 call); **1 ABI-compatible
    family** (below).

**The closest candidate (recorded, NOT promoted):** `FUN_006FAB80` (B.5 start
0x006FAB80, vtable-only function — the E8/E9 lattice MIS-attributes its
enclosing start, a P2 finding) is a shared vtable slot function of 5 RTTI
classes (vtable-extent-verified per the R1 amendment 2026-09-14 — the list
read from the regenerated raw: `.?AVArkAnimationCyclic@@`,
`.?AVArkAnimationCyclicLinear@@`, `.?AVArkAnimationCyclicSin@@`,
`.?AVArkAnimationDerivatives@@`, `.?AVArkAnimationPredefined@@`) — a
**forwarding thunk**:

```
006FAB80  8B 49 14      mov ecx,[ecx+0x14]      ; receiver = [this+0x14]
006FAB83  D9 44 24 04   fld dword [esp+4]      ; arg1 (32-bit copy)
006FAB87  8B 54 24 08   mov edx,[esp+8]        ; arg2 (this thunk's own arg2)
006FAB8B  8B 01         mov eax,[ecx]          ; vtable of [this+0x14]
006FAB8D  8B 40 0C      mov eax,[eax+0xC]      ; slot 3
006FAB90  52             push edx               ; arg2 forwarded
006FAB91  51             push ecx               ; (reserve slot for fstp)
006FAB92  D9 1C 24      fstp dword [esp]       ; arg1 forwarded
006FAB95  FF D0          call eax               ; thiscall, 2 stack args
006FAB97  C2 08 00       ret 8
```

It forwards (arg1, arg2) VERBATIM to slot 3 of `[this+0x14]` — ABI-compatible
with FUN_0050A050 (thiscall, 2 stack args, ret 8). The receiver `[this+0x14]` is
a REFCOUNTED held object (the class ctor at 0x006FABA0: `mov [eax+0x14],ecx`
from a ctor parameter + `mov edx,1; add [ecx+4],edx` refcount — the increment
is via edx (`BA 01 00 00 00` then `01 51 04`), not an immediate; the dtor
decrements and virtually destroys it). Its class is **UNPROVEN within the
declared bound**: the
six ctor call sites (0x006FAFC7, 0x006FB092, 0x006FB409, 0x006FB5CD, 0x006FE9E8,
0x006FFA87) all pass the held pointer as their OWN parameter (bound exhausted);
`+0x14` is in the B.3 holder-offset set (container+0x0C/+0x10/+0x14, writer
FUN_0044D590), but the B.3 container's identity vs the ArkAnimation family is
unproven (FUN_0044D590's container reads its +0x24 as an object pointer for the
SF-factory call at 0x0044D677, while the ArkAnimation family's ctor writes a
float at +0x24 — a layout conflict arguing they are different classes).
Recorded as INSUFFICIENT_PROOF (bound-exhausted) with the full trail.

Structural side-finding (measured, context only): FUN_0044D590 calls
FUN_005247C0 (the function containing the SF-ctor call site 0x0052480F, i.e. the
SF factory) and stores its result into its container's slots
(e.g. `mov [esi+0x10],eax` @0x0044D680) — the writer side of the B.3 holder
slots re-verified from bytes.

### 1.3 ARG2_VALUE_CLASS — **UNVERIFIED** (zero values identified)

Zero verified call sites → zero arg2 producer chains completed → **zero arg2
values identified**. The single ABI-compatible candidate channel
(FUN_006FAB80) forwards an OPAQUE parameter (`[esp+8]` of the thunk); no string
literal, buffer, or field value was identified as an arg2 producer this run.
NC-3 therefore had no in-scope subject; the verbatim read-back machinery is
demonstrated on a known .rdata literal as a tooling calibration only
(01_RAW/NC3_MACHINERY_DEMO.txt; the demo literal reads back as `Entropia`,
NUL-terminated, 9 bytes, at 0x00A7957C — a FACT recorded verbatim with VA+bytes,
not adopted as arg2 evidence).

### 1.4 ARG2_FINAL_SEMANTIC_ROLE — **UNVERIFIED** (hypotheses stay hypotheses)

No direct producer→semantic link was established. The standing B.2 fact (NOT
re-derived; G6) constrains arg2's RUNTIME syntactic class — the slot-17 target
(0x007B5390, FUNCTION_IDENTITY = NiNode::GetObjectByName STRONGLY_SUPPORTED,
the locked B→A criterion) consumes it as a `const char*` name for a recursive
named-object lookup — but that does NOT establish the semantic role. Node name /
bone / socket / marker / other NiAVObject name / config key all remain
HYPOTHESES. Measured structural context (NO promotion): the
`.?AVArkAudioObjectInterface@@` vtable (@0x00A7D42C, exactly 6 slots,
RTTI-verified) is ADJACENT to the SF vtable in .rdata, separated by the
"ArkSceneFeeder" string literal (@0x00A7D444) and the SF COL pointer
(@0x00A7D454) — adjacency is NOT function sharing and NOT inheritance
evidence; each SF slot function has EXACTLY ONE vtable membership (the SF
vtable itself; the imm32 census bounds FUN_0050A050 to exactly one
whole-file address occurrence — the earlier "SF slots 0–4 == ArkAudio slots
11–15" membership reading was a VTABLE-BOUNDARY OVERRUN artifact of the
pre-fix fixed-16-slot RTTI enumeration, RETRACTED per PE-MASTER adjudication;
any SceneFeederObject↔ArkAudioObjectInterface inheritance relationship is
UNVERIFIED), and the one ABI-compatible forwarding family
is the ArkAnimation animation classes forwarding to a refcounted held scene
object. A "GetPosition(out, name)" on a scene-feeder feeding a NiNode
named-object lookup is CONSISTENT with a scene-graph-node-name hypothesis —
recorded as hypothesis only, per human order §32.

---

## 2. Rosetta-edge delta statement (vs the standing matrix)

Standing rows (SCIENCE_STATUS_MATRIX.csv, cleanup R1):
- "arg2 ABI" = `partially observed revalidate-pending` → this run re-derived the
  complete ABI from bytes: **CONFIRMED** (thiscall/2-arg/ret-8 measured at both
  ret sites; full eax def chain; NC-1 9/9 pins byte-exact).
- "arg2 provenance" = `UNVERIFIED` → this run executed the complete caller
  census with rules+denominators: **UNVERIFIED (measured-and-bounded)** — zero
  direct callers, vtable-addressed only, zero receiver-proven virtual call sites
  within the declared bound, 5 demonstrated rejections (NC-2), 17-of-18 holder
  leads ABI-excluded, and exactly one ABI-compatible forwarding-thunk candidate
  family recorded with its evidence trail.
- "arg2 semantic role" = `UNVERIFIED` → **UNVERIFIED (unchanged)** — hypotheses
  only; no promotion.
- NEW item this run: "arg2 value class" — NEW → **UNVERIFIED** (zero values
  identified; no verified call sites).

## 3. Findings

- **P0:** none.
- **P1 (measured, structural):**
  1. FUN_0050A050 is vtable-addressed ONLY (0 E8/E9/EB refs; imm32 count exactly
     1 = the vtable entry at 0x00A7D464) — the slot-3 channel is exclusively
     virtual.
  2. RETRACTED and corrected (PE-MASTER adjudication, R1 amendment 2026-09-14):
     the original item claimed the SF primary-vtable functions
     FUN_0050A460/0x5090A0/0x5090B0/0x50A050/0x5090C0 are ALSO slots 11–15 of
     the `.?AVArkAudioObjectInterface@@` vtable — a VTABLE-BOUNDARY OVERRUN
     artifact of the pre-fix fixed-16-slot RTTI enumeration (it read through
     the 6 real ArkAudioObjectInterface slots, the "ArkSceneFeeder" string
     literal, and the SF COL INTO the SF vtable). Corrected: each SF slot
     function has EXACTLY ONE vtable membership (the SF vtable itself; the
     imm32 census bounds FUN_0050A050 to exactly one whole-file occurrence);
     the `.?AVArkAudioObjectInterface@@` vtable (0x00A7D42C, exactly 6 slots,
     RTTI-verified) is ADJACENT to the SF vtable — adjacency is NOT sharing
     and NOT inheritance evidence (inheritance UNVERIFIED).
  3. This binary's RTTI COLs are POINTER-based (VA fields, signature 0), not
     the MSVC RVA layout — measured on the SF class chain
     (vtable[-1]→COL→+0x0C = VA(type descriptor)).
- **P2 (method/tooling):**
  1. The codebase's vcall idiom is the 2-step `mov f,[vt+slot]; call f` form:
     only ONE `call [reg+0x0C]` byte-pattern exists in .text (and it is a frame
     call, not a vtable call); even slot-17's `FF 52 44` form is 0.
  2. Enclosing-function attribution for vtable-only functions via the E8/E9
     target lattice MIS-FIRES (FUN_006FAB80 attributed to 0x006FAB20); B.5
     padding-derived function starts are required (demonstrated + fixed).
  3. The ABI dimension (stack-arg count + this-register) discriminates channel
     membership: 17 of 18 holder-offset slot-3 flows are excluded as
     ABI-incompatible with the measured FUN_0050A050 ABI.
  4. A flow accumulator without register-clobber tracking produced one false
     holder-flow positive (0x007B93D3-region, ecx reassigned from [esi+0x160]
     before the vtable load) — fixed with clobber-aware accumulation; re-run
     removed it.
- **P3 (candidate follow-ups, NOT performed — out of scope):**
  1. Upstream census of the ArkAnimation-family vtable slot channels (the
     FUN_006FAB80 thunk's virtual callers) to trace the ultimate arg2 producers
     and values.
  2. Identification of FUN_0044D590's container class (its +0x0C/+0x10/+0x14
     stores receive FUN_005247C0 SF-factory results) and a receiver-proof
     linkage (or disproof) between the B.3 container and the ArkAnimation
     family's `[this+0x14]` held object.
  3. The B.5 boundary derivation on the fallback tail confirmed the published
     extent; the SLOT_CENSUS "shared-tail polymorphism" NOT_CHECKED note is now
     CHECKED: the tail is the published fallback, no polymorphism, one ABI.

## 4. Bound declarations and honest exhaustion states

- W2(c) virtual-call-site receiver proof: 2 levels, 48-byte windows — 211
  candidates INSUFFICIENT_PROOF (their def chains leave the window or resolve to
  unproven bases); never silently dropped; every row in
  01_RAW/VIRTUAL_CALLSITE_CENSUS.csv.
- W3 arg2 producer analysis: applies to VERIFIED sites only — zero verified
  sites → no producer chains; the ABI-compatible thunk family's forwarded
  parameter recorded as the candidate channel (upstream census = P3 item 1).
- Method-1 forward window: 48 bytes, ≤7 instructions, mov-accumulation with
  clobber tracking; SIB forms excluded (declared).
- The P3 follow-check (≤3 non-control interstitials) missed the
  0x006FAB95 site (4 interstitials: push/push/fstp) — compensated by Method 1,
  which found and fully dispositioned it; the cross-check is recorded in the
  raw. INCOMPLETE is never PASS: this gap is declared, not claimed as coverage.
