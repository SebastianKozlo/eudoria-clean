# FORWARDER_ANALYSIS.md — Phase A (G2) + Phase B (G3)

RUN_ID: PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915
Source of truth: D:/Eudoria_Reconstruction/pcg_install/Entropia.exe physical bytes
(identity re-verified by every generator; see 01_RAW/IDENTITY_VERIFICATION.txt).
All claims below carry evidence pointers into 01_RAW/.

## PHASE A — FUN_006FAB80 (the "thunk") — G2

**Measured (01_RAW/FUN_006FAB80_DISASM.txt, generator phase_a_thunk.py):**

- B.5 extent: [0x006FAB80..0x006FAB9A), 26 bytes, terminal `ret 8`, end_kind=pad
  (6 CC bytes), next_start = 0x006FABA0 (the shared base ctor — a structural
  adjacency that Phase C confirmed is real).
- ABI (measured): thiscall — this in ECX (base of the `mov ecx,[ecx+0x14]`
  load at 0x006FAB80); two dword stack args (arg1=[esp+4], arg2=[esp+8]);
  callee cleanup `ret 8` @0x006FAB97.
- Receiver path: `ECX(this) -> held=[this+0x14] @0x006FAB80 -> vt=[held]
  @0x006FAB8B -> target=[vt+0x0C] @0x006FAB8D -> call eax @0x006FAB95` —
  virtual slot displacement 0x0C = SLOT 3 (byte evidence 8B 40 0C).
- Forwarding fidelity (measured per operand):
  - arg1: [esp+4] --fld dword--> st0 --fstp dword [esp]--> receiver [esp+4].
    x87 ROUNDTRIP, not a register forward. The `push ecx` @0x006FAB91 is a
    slot-allocation push (value overwritten by the fstp into the same cell).
  - arg2: [esp+8] --mov edx--> push edx --> receiver [esp+8]; VERBATIM
    (no test, no arithmetic, no mutation).
- Bit-preservation classification (analytic, x87 architecture, stated in the
  raw): normals, denormals (x87 has no FTZ), infinities, qNaN payloads and
  POINTERS-AS-DWORDS survive bit-exact; sNaN quieting is not guaranteed.
  Implication (measured constraint): the receiver's arg1 could be an
  out-buffer POINTER or a genuine FLOAT VALUE — discriminable only at callers
  (Phase E: no statically-identifiable caller exists, so the discriminator
  is unresolvable at this seam).
- Side-effect/control-flow audit: 0 conditional branches, 1 call (the virtual
  dispatch), the only memory write is the fstp receiver-arg slot, no null test,
  no refcount operation, single basic block.
- PIN-THUNK: all 10 expected head-byte rows MATCH (raw [A8]).

**FORWARDER_OPERATION_STATUS = CONFIRMED** (all 10 determination checks true;
definition recorded in raw [A9]).

OBSERVED_OPERATION (status algebra): FUN_006FAB80 = virtual slot-3 forwarder
through the object held at [this+0x14]. FUNCTION_IDENTITY: vtable-only virtual
stub of the ArkAnimation family, slot ordinal 2 (Phase B).

## PHASE B — five class memberships — G3

**Measured (01_RAW/RTTI_COL_RAW.txt + 01_RAW/ARKANIMATION_VTABLE_MAP.csv +
01_RAW/VTABLE_INVENTORY.csv + 01_RAW/IMM32_THUNK_CENSUS.txt; generator
phase_b_rtti.py):**

- IMM32 whole-file census of 0x006FAB80: exactly 5 occurrences, all aligned
  .rdata vtable slot dwords. No .text immediates, no unaligned hits, no
  additional references anywhere in the file.
- Five COL-backed vtables contain the thunk, at slot ORDINAL 2 in ALL five
  (same ordinal — measured per slot dword):

| vtable    | COL class (re-derived) | extent slots | thunk slot |
|-----------|------------------------|--------------|------------|
| 0x00A864C0 | .?AVArkAnimationPredefined@@    | 8  | 2 |
| 0x00A86550 | .?AVArkAnimationDerivatives@@   | 8  | 2 |
| 0x00A86574 | .?AVArkAnimationCyclic@@        | 9  | 2 |
| 0x00A865A0 | .?AVArkAnimationCyclicLinear@@ | 9  | 2 |
| 0x00A86650 | .?AVArkAnimationCyclicSin@@    | 9  | 2 |

- PIN-FIVE: all five expected RTTI names present, none missing, none extra.
- Vtable extent rule (first non-.text dword): applied to all five; no
  import-thunk/non-.text EXEC exceptions encountered (stop dwords are data —
  e.g. Predefined stops at 0x00AA7804, a COL pointer of the next structure).
- Base hierarchy (COL BCD walks, raw [B10]): the shared base of the family is
  **.?AVArkAnimationPredefined@@**:
  - Derivatives <- Predefined
  - Cyclic <- Predefined; CyclicLinear <- Cyclic <- Predefined;
    CyclicSin <- Cyclic <- Predefined.
- Shared base ctor 0x006FABA0 = **the ArkAnimationPredefined constructor**
  (its first store is `mov [eax], 0x00A864C0` — the Predefined vtable —
  byte-verified at 0x006FABA8 in the raw).
- Constructors identified (vtable store + shared-ctor-call + object-size
  evidence, raw [IV-0d] of HOLDER14_WRITER_RAW.txt):
  - Predefined base ctor 0x006FABA0 (called by six derived-class ctors)
  - TimeController ctor 0x006FAF90 (new size 0x44)
  - NodeUpdate ctor 0x006FB080 (0x40)
  - AnimatedTexture ctor 0x006FB3D0 (0x54)
  - Derivatives ctor 0x006FB590 (0x6C, 3 factory call sites)
  - ParticleSystemPredefined ctor 0x006FE9B0
  - Cyclic ctor 0x006FFA70; CyclicLinear ctor 0x006FBAB0 (0xC4);
    CyclicSin ctor 0x006FD270 (0x88, 4 factory call sites)
- Deleting destructors (vtable slot 0 pattern, `??3` import resolved):
  Predefined 0x006FAC50 (also 0x006FAC00 = base dtor), Derivatives 0x006FB740,
  Cyclic-family 0x006FD2E0 (shared by Cyclic/Linear/Sin — inherited slot).
- Family lineage closure (inventory-wide): 10 classes derive from
  ArkAnimationPredefined (five core + TimeController, NodeUpdate,
  AnimatedTexture, ParticleSystemPredefined, ParticleSystemPredefinedMod).
- PIN correction (finding F-2, see REPORT; R2 wording correction per QC
  P3-8, AMEND_LOG_R2 R2-4): the prior run's claim of a second
  `.?AVArkAnimationCyclic@@` vtable membership at 0x00AA7958 is NOT reproduced:
  no dword 0x006FAB80 occurs at or near 0x00AA7958; the IMM32 census is
  exhaustive (5 hits). Own re-measurement of the region: the CYCLIC class
  hierarchy descriptor (CHD) sits at 0x00AA7948 (sig=0, attributes=0,
  numBases=2); its base-class-descriptor pointer-array field @0x00AA7954
  points to the array at 0x00AA7958, whose first entry (dword @0x00AA7958 =
  0x00AA7964) is CYCLIC's own base-class descriptor (its TypeDescriptor
  pointer 0x00B8CBD8; the second array entry is 0x00AA77E8). The
  CyclicLinear COL is 0x00AA7980 (.?AVArkAnimationCyclicLinear@@), and the
  base-array of ITS hierarchy descriptor begins at 0x00AA79A4. 0x00AA7958 is
  therefore RTTI data (a base-class-descriptor array entry), NOT a vtable;
  no 0x006FAB80 dword exists anywhere in 0x00AA7930..0x00AA79A4.
- Sibling forwarder pattern (measured context, decode in RECEIVER_IDENTITY.md):
  slot 6 (0x006FAB40) forwards 1 arg to the SAME object's vtable slot 4;
  slot 7 (0x006FAB60) forwards 1 arg to the same object's vtable slot 5
  (both `mov eax,[ecx]; ... mov edx,[eax+0x10|0x14]; ... call edx; ret 4`).
  The base class implements several virtuals as delegation stubs; the slot-2
  thunk (delegate to [this+0x14]'s slot 3) belongs to this stub family.

G3 self-assessment: PASS (names re-derived; primary vtables + extents + slot
ordinals + ctors/dtors + hierarchy derived from own bytes; corrected findings
documented above).
