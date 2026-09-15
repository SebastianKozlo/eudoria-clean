# HOLDER14_PROVENANCE.md — Phase C (G4, G5, G6): [this+0x14] writer census

RUN_ID: PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915
R2 CORRECTION (AMEND_LOG_R2.md; QC_AUDIT.md §2 P0-1): this document is the
corrected disposition. The R1 sections claimed universal NULL at every
construction; that verdict was falsified by the QC (branch-bypass edges at
the dispatcher factory blocks) and is superseded by the per-class table
below. Everything the QC re-verified as correct (denominators, the 3-writer
set, criterion-b sweep, census arithmetic) stands unchanged.
Evidence: 01_RAW/HOLDER14_WRITER_CENSUS.csv (all rows; byte-identical to the
R1 QC-verified census — the R2 regeneration reproduced it hash-for-hash),
01_RAW/HOLDER14_CENSUS_SUMMARY.txt (denominators + writer fields + [C4]
complete caller census + [C8] leaf histogram),
01_RAW/HOLDER14_WRITER_RAW.txt (anchor chain + R2 edge-aware slices +
[IV-8]/[IV-9] chain disposition),
01_RAW/B5_FUNCTION_MAP.csv (attribution layer).
Generators: phase_c_census.py (R2), phase_c_anchor.py (R2).

## C(i) Full-.text census — denominators (G4) — UNCHANGED (QC-re-verified)

- **Denominator = 10,711 rows**: every memory-WRITE operand with displacement
  0x14 in the linearly decoded .text (1,928,649 instructions; B.5 map of
  105,492 functions; zero UNKNOWN_CONTEXT attribution failures).
- Base-register categories: REG_INDIRECT=1,898; STACK_FRAME(esp/ebp)=8,811
  (EXCLUDED from the holder analysis, count recorded per contract); SIB=2
  (non-frame indexed forms, enumerated separately — 5 further esp/ebp-based
  SIB rows are counted inside STACK_FRAME); ABSOLUTE=0.
- Write-form coverage: capstone access-based detection with a declared
  architectural override for x87 stores (capability finding: capstone 5.0.7
  misreports `fstp [mem]` access as READ — see IDENTITY_VERIFICATION.txt [3]
  and AMEND_LOG_R1.md; without the override, x87 stores to [reg+0x14] would
  have been silently missed).
- R2 BULK-COPY CHANNEL BOUND (declared; AMEND_LOG_R2 R2-6): the disp-census
  is blind to `rep movs/stos` sites (memory writes without a disp==0x14
  operand). R2 census (HOLDER14_WRITER_RAW.txt [VIII]): 618 rep movs/stos
  sites decoded in .text (single-stream B.5 decode; the QC's own census
  counted 636 under its undisclosed rule — the load-bearing part agrees
  exactly: 4 sites inside the ArkAnimation family code cluster
  [0x006FAB40..0x006FFAF0): 0x006FBDD7/0x006FBDE8 (ArkAnimationRotation
  ctor fields [ebx+0x34]/[ebx+0x58]), 0x006FBF30 (child helper, destination
  [[edi+8]+0x38]), 0x006FEE22 (ArkTextureInfo ctor field [ebx+0x48]) —
  NONE touches a family object's +0x14; family ctors/dtors initialize
  field-by-field). DECLARED NOT_CHECKED: .text-wide destination-provenance
  tracing of the remaining 614 out-of-cluster rep sites (a family-object
  pointer would have to flow out and back; the family-function scan found
  no such handoff inside family code).

## C(ii) Classification — family provenance (G4) — UNCHANGED counts + R2 histogram

- FAMILY_CONTEXT_PROVEN = **3 rows** (all criterion (a) — enclosing family
  function):
  1. **0x006FABB5** `mov [eax+0x14], ecx` in the shared base ctor 0x006FABA0
     (ArkAnimationPredefined ctor).
  2. **0x006FAC25** `mov [esi+0x14], 0` in 0x006FAC00 (base dtor / release path;
     stores the Predefined vtable at entry).
  3. **0x006FAC75** `mov [esi+0x14], 0` in 0x006FAC50 (Predefined scalar
     deleting dtor, vtable slot [0]).
- NON_FAMILY_OUT_OF_SCOPE = 1,895 rows, each with a per-row base-def verdict
  (see below). UNKNOWN_CONTEXT = 0.
- Criterion (b) was applied exhaustively to all 1,895 non-criterion-a rows:
  - (b2) family-vtable fingerprint: 0 hits.
  - (b1) base-def backward slices (levels<=3, 384-byte window, clobber-aware,
    caller-cross + this-cross, ctor-class resolution incl. operator-new
    chains): **0 rows prove family construction**.
  - R2 leaf-verdict histogram over the 1,895 rows (QC P2-2 fix; the R1
    printed breakdown summed to 1,892 — a development-pass artifact; the R2
    breakdown is regenerated in HOLDER14_CENSUS_SUMMARY.txt [C8] from the
    same per-row slices the classification used, under a DECLARED rule:
    PARAM_CHAIN if the base-def slice crossed to callers; else the first
    depth-first leaf kind):
    THIS_ENTRY=820, BOUND_EXHAUSTED=487, LEA_ADDR=244, OTHER_WRITE=224,
    PARAM_CHAIN=68, NO_RET=20, ZERO=21, ALIAS_RISK_NOTE=5, IMMEDIATE=2,
    PARTIAL_NOTE=2, CALLEE_UNDECODEABLE=1, X87_STORE=1
    → **TOTAL = 1,895 = the NON_FAMILY count** (exact by construction).
- The residual uncertainty is therefore localized to: unproven base params /
  thiscall-this entries in non-family functions (none family-proven within the
  declared bound), plus indexed/SIB computed-address writes (2 non-frame rows,
  both decoded and classified excluded in NEGCTL_RECEIVER_RAW.txt [N6]).

## C(iv) Anchor chain — shared base ctor 0x006FABA0 (G5) — decode UNCHANGED

Full decode (HOLDER14_WRITER_RAW.txt [IV-0]):

```
0x006FABA0  mov eax, ecx            ; eax = this (thiscall this=ECX)
0x006FABA2  mov ecx, [esp+0xC]      ; ecx = ARG2 = HELD OBJECT POINTER
0x006FABA6  test ecx, ecx           ; NULL TEST on the held param
0x006FABA8  mov [eax], 0xA864C0     ; store Predefined vtable
0x006FABAE  mov [eax+4], 0          ; own refcount field = 0
0x006FABB5  mov [eax+0x14], ecx     ; [this+0x14] := held param   <-- WRITE
0x006FABB8  mov edx, 1
0x006FABBD  je 0x6FABC2             ; skip refcount inc when held==NULL
0x006FABBF  add [ecx+4], edx        ; refcount++ ON HELD @+4       <-- PIN-CTOR
0x006FABC2  ... (float/byte param init: +0x18..+0x38)
0x006FABF5  ret 0xC                 ; 3 dword stack args
```

- PIN-CTOR VALIDATED with two refinements: (i) the ctor takes THREE stack
  args (ret 0xC): arg0 = byte flag -> [this+0x28], arg1 = float -> [this+0x2C],
  **arg2 = the held object** (read at [esp+0xC]) -> [this+0x14]; (ii) the
  refcount increment (`BA 01 00 00 00` / `01 51 04` — both byte-verified) is
  guarded by a NULL test — the pin did not note the guard.
- Base layout derived (this run): +0x00 vtable, +0x04 own refcount, +0x14
  HELD pointer, +0x18 state dword=1, +0x1C/+0x20/+0x24 floats, +0x28 byte
  arg0, +0x2C float arg1, +0x30 float const [0xA7B334], +0x34/+0x35 bytes,
  +0x38 dword 0. Object >= 0x3C bytes (measured new sizes 0x40..0xC4 for
  derived classes; R2: PSP and PSPMod also measured at 0x70 — cascade-size
  provenance in HOLDER14_WRITER_RAW.txt [IV-0d]).

## C(iv) The six call sites — R2 CORRECTED slices (AMEND_LOG_R2 R2-1/R2-2)

All six E8 sites of 0x006FABA0 re-derived (raw-byte verified = 6, no lattice
misses): 0x006FAFC7 (TimeController ctor), 0x006FB092 (NodeUpdate ctor),
0x006FB409 (AnimatedTexture ctor), 0x006FB5CD (Derivatives ctor),
0x006FE9E8 (ParticleSystemPredefined ctor), 0x006FFA87 (Cyclic ctor).

Held-param (arg2) slices (HOLDER14_WRITER_RAW.txt [IV-1..6], R2 edge-aware
at the declared 6-level bound; [IV-8] chain disposition; [IV-9] table):

- Sites 1,2,3,5 (TimeController, NodeUpdate, AnimatedTexture,
  ParticleSystemPredefined): the arg2 push is **`push 0` (immediate NULL)** —
  0x006FAFC0, 0x006FB089, 0x006FB402, 0x006FE9E1. UNCHANGED from R1.
  ParticleSystemPredefinedMod chains via the PSP ctor (PSPMod ctor ->
  PSP ctor call @0x006FEB4B) and inherits this NULL — held = NULL always.
- Site 4 (Derivatives ctor): arg2 <- ctor's own arg2 -> caller-cross to 3
  factory call sites (0x006D20DA, 0x006D22F7, 0x006D2457). R2: at EACH
  site the arg2 register (esi) is defined on a CONDITIONAL allocation-failure
  path (`xor esi,esi`, entered via the child-allocation NULL test je) and on
  the NORMAL path bypasses the xor via `jmp block_start+2` after constructing
  a LIVE CHILD object (Scale / Color / Intensity at sites A/B/C; the
  Deriv-C shared tail additionally receives three ALIAS blocks constructing
  Rotation / Translation / Alpha via `jmp 0x6D2441`).
- Site 6 (Cyclic ctor): arg2 <- Cyclic's own arg2 -> CyclicLinear ctor site
  0x006FBAD9 (forwards its own arg2 from [esp+0xC] @0x006FBAB8) and
  CyclicSin ctor site 0x006FD299 (same shape @0x006FD278) -> their factory
  sites: Linear 0x006D1DC6 (NULL|Translation child) and Sin
  0x006D1736/0x006D1828/0x006D1AF3/0x006D1CB3 (NULL|Translation / Alpha /
  Intensity / Scale|Rotation|Color — the Sin-4 block also receives two alias
  blocks via the shared-tail pattern).

**RESULT (R2 CORRECTED — replaces the R1 "NULL at EVERY statically-reachable
construction site"): held = NULL always for TimeController, NodeUpdate,
AnimatedTexture, ParticleSystemPredefined, ParticleSystemPredefinedMod;
held = NULL on the allocation-failure paths and = a LIVE, RTTI-IDENTIFIED
CHILD OBJECT (Scale/Color/Intensity/Rotation/Translation/Alpha — all
.?AVArkAnimationFloatValue@@-hierarchy classes) on the normal paths for
ArkAnimationDerivatives, ArkAnimationCyclicLinear, ArkAnimationCyclicSin;
ArkAnimationCyclic inherits the forwarded child.** The this(ECX) slices all
reach THIS_ENTRY (fresh operator-new objects; sizes measured at the ??2
sites, [IV-0d]).

## C(iii) Writer fields (contract 7(iii)) — see HOLDER14_CENSUS_SUMMARY.txt [C6]

- 0x006FABB5: VALUE_SOURCE=ecx=ctor arg2 (NULL-tested); PROVENANCE = the
  corrected per-class table above (R2: the census-level value slice now
  resolves PROVEN_OTHER to the six child classes — see [C6]); WIDTH=4;
  PATH_PRECONDITION none for the STORE itself (the store is unconditional;
  the VALUE is path-preconditioned at the sources); CONTEXT = base-ctor init
  of every family object; WRITER_CLASS = constructor-initialization.
- 0x006FAC25 / 0x006FAC75: VALUE_SOURCE=imm 0; WIDTH=4; PATH_PRECONDITION =
  the release-path conditionals (held!=NULL tests); CONTEXT = release path;
  WRITER_CLASS = destructor-release.

## Release path ([IV-0c]) — R2 CORRECTED reading

Base dtor 0x006FAC00 (and identically the deleting dtor 0x006FAC50 before the
delete flag test):

```
mov esi, ecx; mov [esi], 0xA864C0        ; restore base vtable
mov eax, [esi+0x14]                       ; held
test eax, eax; je skip
add dword [eax+4], -1                     ; refcount-- ON HELD @+4
jne skip
mov ecx, [esi+0x14]; test ecx, ecx; je skip
mov eax, [ecx]; mov edx, [eax]            ; HELD VTABLE SLOT 0
push 1; call edx                          ; held->vt[0](1)  = delete-the-object style
mov [esi+0x14], 0                         ; zero the field
```

The family expects a refcounted held object (refcount@held+4, deleting via
vtable slot 0 with flag=1). R2 CORRECTION: on the normal construction paths
this release path is LIVE — it decrements the child's refcount and deletes
it via the child's vtable slot 0 when the count reaches zero. The R1 "this
release path is defensive dead code (its NULL tests guard it)" reading is
RETRACTED (AMEND_LOG_R2 R2-3): the NULL tests guard the allocation-failure
constructions, not dead code. The slot-0 delete protocol remains
ABI-COMPATIBLE with SceneFeederObject's slot 0 (0x0050A460 scalar deleting
dtor) — compatibility noted, no identity claim: the actual held children are
the FloatValue-family classes.

## Read picture (NEGCTL_RECEIVER_RAW.txt [N7], R2)

R2 DECLARED BOUND (QC P3-1 fix): family function set = all slots of the 10
family vtables + all family-vtable-storing functions (ctors/dtors) + the
shared ctor + the PSPMod ctor = **57 functions**, each decoded over its
chunk closure (branch-target + conditional-fall-through + jump-table
joining). Total [reg+0x14] operand references over the declared bound =
**22** (enumerated per-ref in [N7]): the thunk read (0x006FAB80), the ctor
write, the two dtor-context read pairs + zero writes, the slot-7 delegation
stub read `mov edx,[eax+0x14]` @0x006FE899 (a VTABLE-slot-5 read — the PSP/
PSPMod slot-7 stub 0x006FE890), the PSP-ctor source-array reads
(`fld [eax+0x14]`/`fld [ecx+0x14]` @0x006FEA46/0x006FEA4C), esp-based
frame refs in the AT ctor (0x006FB3EA/0x006FB4EE), Derivatives slot 6
(0x006FB9D4), Linear/Sin ctors (0x006FBAB4/0x006FBAC2/0x006FD274/
0x006FD282), PSPMod ctor (0x006FEB55), Cyclic ctor (0x006FFAA7), and one
esp-based stack-local write (0x006FBA6A, not an object field). (R1 [N7]
scanned an undeclared 5-vtable subset and printed 10 — superseded.)

## C(v) Upstream continuation — R2 CORRECTED

The R1 statement "the six slices produce zero call-return leaves" was an
artifact of the R1 engine's function-entry assumption. The R2 slices
produce **6 child-ctor call-return leaves** (HOLDER14_WRITER_RAW.txt [V]):
0x006FBD00 Scale, 0x006FBDB0 Rotation, 0x006FBF90 Intensity, 0x006FC450
Color, 0x006FCD00 Alpha, 0x006FD420 Translation — each a real constructor
(vtable store byte-verified; this-return shape measured for 5 of the 6
child ctors — the Alpha ctor's ret site is measured (0x006FD268) but its
return-value shape is not derived in this package; chunk-closure decodes
in [IV-8]) with 2-3 direct E8 callers (the dispatcher's
child-construction blocks; the Intensity ctor's 3rd caller is the Color
ctor — Color is Intensity's RTTI base). The SceneFeeder factory chain
(FUN_005247C0, byte-validated in [VI]) still NEVER appears in any
held-param slice: no writer binds a SceneFeederObject. G4/G5
self-assessment: PASS under the corrected values (denominator recorded;
every row classified with per-row verdicts; all family writers carry full
fields; anchor chain fully decoded; no silent drops).
