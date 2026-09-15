# RECEIVER_IDENTITY.md — Receiver proof ladder (G5) + SceneFeeder identity test (G6) + negative control (G7)

RUN_ID: PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915
R2 CORRECTION (AMEND_LOG_R2.md; QC_AUDIT.md §2 P0-1): the R1 ladder table
terminated every writer at L0 with "value = NULL". That was falsified by the
QC: the base-ctor writer's value is NULL for 5 classes + the error paths,
and a LIVE RTTI-IDENTIFIED CHILD OBJECT for the 4 param-chained classes on
their normal paths. The ladder is re-climbed below — to L3 with an L4
NEGATIVE for every child class.
Evidence: 01_RAW/HOLDER14_WRITER_RAW.txt ([IV-1..6] R2 slices, [IV-8] chain
disposition, [IV-9] per-class table), 01_RAW/HOLDER14_CENSUS_SUMMARY.txt
([C6] census-level value verdicts), 01_RAW/NEGCTL_RECEIVER_RAW.txt,
01_RAW/THUNK_CALLER_CENSUS.txt/.csv, 01_RAW/FUN_006FAB80_DISASM.txt,
01_RAW/IDENTITY_VERIFICATION.txt.

## LADDER application — per source value written into [this+0x14]

Contract ladder: L0 raw pointer source; L1 source object/vtable observed;
L2 RTTI class family; L3 exact vtable contains slot-3 target; L4 slot-3 ==
0x0050A050.

| writer | value source (R2 measured) | ladder level | disposition |
|--------|----------------------------|--------------|-------------|
| 0x006FABB5 (base ctor) — sites 1/2/3/5 (TimeController, NodeUpdate, AnimatedTexture, ParticleSystemPredefined; PSPMod chains via PSP) | ctor arg2 = immediate `push 0` (0x006FAFC0/0x006FB089/0x006FB402/0x006FE9E1) | **L0 terminal (NULL)** | Constant NULL for these 5 classes: no object, no vtable, no RTTI. |
| 0x006FABB5 (base ctor) — param-chained sites (Derivatives, CyclicLinear, CyclicSin; Cyclic inherits) | ctor arg2 = esi from the dispatcher factory blocks: NULL on the allocation-failure paths (`xor esi,esi` behind the child-alloc NULL-test je); **LIVE CHILD OBJECT** on the normal paths — the bypass edge (`jmp block_start+2`) carries the child ctor's return (`mov esi,eax` after `call <child_ctor>`; ret-this shape byte-proven for 5 of the 6 child ctors / 11 of the 13 child paths — there the child ctor returns `this`, itself the ??2 allocation just tested non-NULL; the 2 Alpha chains' ctor return-value shape is NOT derived in-package (construction + vtable store + bypass edge byte-proven; the returned value not shape-proven) | **L0 (xor-paths, NULL) + L1→L2→L3→L4-NEGATIVE per child chain (normal paths)** | L1: the child ctor's vtable store observed (0x006FBD0D/0x006FBDC4/0x006FBFB0/0x006FC48B/0x006FCD34/0x006FD463). L2: RTTI — .?AVArkAnimationScale@@, .?AVArkAnimationRotation@@, .?AVArkAnimationIntensity@@, .?AVArkAnimationColor@@, .?AVArkAnimationAlpha@@, .?AVArkAnimationTranslation@@, ALL rooted at .?AVArkAnimationFloatValue@@ (Transform <- {Scale, Rotation, Translation}; Color <- Intensity; Alpha). L3: each child vtable's slot-3 dword measured. L4: NEGATIVE — see table below. |
| 0x006FAC25 (base dtor) | imm 0 | L0 (terminal) | NULL (release-path zeroing). |
| 0x006FAC75 (deleting dtor) | imm 0 | L0 (terminal) | NULL (release-path zeroing). |

**Child vtable slot-3 measurements (R2; HOLDER14_WRITER_RAW.txt [IV-8]/[IV-9]):**

| child class | vtable | slot-3 dword | == 0x0050A050? |
|---|---|---|---|
| .?AVArkAnimationScale@@ | 0x00A865E0 | 0x006FFF00 | NO |
| .?AVArkAnimationRotation@@ | 0x00A865F4 | 0x006FFF00 | NO |
| .?AVArkAnimationIntensity@@ | 0x00A86608 | 0x009154A0 | NO |
| .?AVArkAnimationColor@@ | 0x00A8661C | 0x009154A0 | NO |
| .?AVArkAnimationAlpha@@ | 0x00A8663C | 0x009154A0 | NO |
| .?AVArkAnimationTranslation@@ | 0x00A86678 | 0x006FFF00 | NO |
| (.?AVSceneFeederObject@@ re-confirmed) | 0x00A7D458 | 0x0050A050 | (the ONLY slot-3==0x0050A050 receiver; NEGCTL [N1] 1/803) |

**HELD_OBJECT_IDENTITY (R2): NOT a single identity — a per-class table.**
NULL always for TimeController, NodeUpdate, AnimatedTexture,
ParticleSystemPredefined, ParticleSystemPredefinedMod. For the 4
param-chained classes (Derivatives, CyclicLinear, CyclicSin, and Cyclic via
forwarding): NULL on the allocation-failure paths; a LIVE
ArkAnimationFloatValue-hierarchy CHILD OBJECT (channel animation:
Scale/Rotation/Translation/Intensity/Color/Alpha per chain) on the normal
paths. The ladder is FULLY TRAVERSED for the normal paths: L0 (new
allocation) → L1 (child vtable stores) → L2 (RTTI names) → L3 (slot-3
targets measured) → **L4 NEGATIVE for every child class** (slot-3 ≠
0x0050A050). LEVEL 4 would have permitted `HELD_RECEIVER =
SceneFeederObject CONFIRMED` — it is reached and answers NO.

## Strong positive test (G6) — executed under the corrected values, outcome NOT CONFIRMED

- **Test A** (writer stores a pointer whose current vtable is physically
  0x00A7D458): NO. The bypass-path sources store the CHILD vtables
  (0x00A865E0/0x00A865F4/0x00A86608/0x00A8661C/0x00A8663C/0x00A86678) —
  the only `mov [x], 0xA7D458` in the binary remains the SceneFeederObject
  own-ctor store at 0x00509366 (validated, HOLDER14_WRITER_RAW.txt [VI]).
- **Test B** (writer/source construction proven SceneFeederObject by RTTI/ctor
  chain AND slot-3 resolves to 0x0050A050): the writer/source construction IS
  now proven by RTTI — and it is NOT SceneFeeder: the receivers are the six
  ArkAnimationFloatValue-hierarchy channel classes, whose slot-3 targets are
  0x006FFF00 / 0x009154A0, NOT 0x0050A050. Test B executes and REJECTS.
- **Test C** (bounded exact call chain proves the held originates from known
  SF construction with no replacement): NO — the bounded chains originate
  from the dispatcher's child-construction blocks (??2 -> child ctor ->
  `mov esi,eax`), never from FUN_005247C0/FUN_00509330.

**SCENEFEEDER_LINK = REJECTED (R2 re-based).** The binding edge EXISTS and is
LIVE (a composite-animation mechanism: family objects holding channel-child
animations), so the seam is NOT "unbound/unexercised" — but the RECEIVER
IDENTITY LINK of the Rosetta chain is falsified: the receivers are the
ArkAnimationFloatValue-hierarchy channel classes, whose slot-3 ≠
FUN_0050A050. The Rosetta edge
"ArkAnimation -> [this+0x14] -> SceneFeeder slot3 -> NiNode::GetObjectByName"
does not hold: a slot-2 dispatch on a live composite would forward arg1/arg2
to the CHILD's slot-3 (0x006FFF00 / 0x009154A0), not to FUN_0050A050.

## SceneFeeder infrastructure validation (for the record; NOT family evidence)

All SceneFeeder pins were re-derived from own bytes (NEGCTL_RECEIVER_RAW.txt
[N3],[N4],[N5]):

- vtable 0x00A7D458 = `.?AVSceneFeederObject@@` (COL 0x00AA12B8, sig 0,
  offset 0), hierarchy SceneFeederObject <- ArkAudioObjectInterface.
- 6 slots exactly as PIN-SF1: 0x50A460/0x5090A0/0x5090B0/0x50A050/0x5090C0/
  0x509580; extent [0x00A7D458..0x00A7D470) ends at the first non-code dword
  0x53565064 = "dPVS" ASCII (pin detail confirmed byte-for-byte).
- FUN_0050A050 (slot 3): two B.5 chunks [0x0050A050..0x0050A087) +
  [0x0050A087..0x0050A0AA) = pin extent 0x0050A050..0x0050A0AA; ret 8 at
  BOTH ret sites (0x50A084 and 0x50A0A7); arg2 NULL-tested; main path:
  [SF+0x30] -> its vtable -> slot 0x44 (= slot 17) with arg2, then +0x90 ->
  0x437F70 -> 0x82B5A0 (P2 downstream — untouched, out of scope per contract
  §11); fallback path: SF vtable slot 1 -> copy float3 into arg1 out-buffer.
- SF slot 0 = 0x0050A460 = scalar deleting dtor (flag arg, ??3 delete) —
  ABI-COMPATIBLE with the family dtor's held release `held->vt[0](1)`
  (compatibility only; the actual children use their own slot-0 methods).
- PIN-SFCHAIN container correction: the "+0x10 store receiving FUN_005247C0
  result" at 0x0044D680 is inside function [0x0044D5D8..0x0044D787), NOT
  FUN_0044D590 (whose B.5 extent is a guard fragment [0x0044D590..0x0044D5D8)).
  The real container stores three factory results at +0x0C/+0x10/+0x14 (calls
  at 0x0044D625, 0x0044D677, 0x0044D6C8 with args 0xF0000000/1/2) and ORs
  their +0x2C flags.

## Negative control (G7) — FAILURE_CASE_DETECTED = YES

(NEGCTL_RECEIVER_RAW.txt [N1],[N2].)

- Slot-3 receiver-classifier selectivity across ALL 1,393 COL-backed vtables:
  803 have a valid slot-3 entry; **exactly 1** has slot-3 == 0x0050A050
  (0x00A7D458 .?AVSceneFeederObject@@). The classifier therefore does NOT
  classify every vtable/dispatch receiver as SceneFeeder — 802/803 valid
  slot-3 receivers are NOT SceneFeeder.
- PIN-NC anchors re-derived from own bytes: 0x007AC2F0 = vtable slot 14 of
  `.?AVNiD3DPixelShader@@` (vt 0x00A8C2EC) and `.?AVNiD3DHLSLPixelShader@@`
  (vt 0x00A8C59C); 0x007F1D70 = vtable slot 1 of `.?AVNiBoundingVolume@@`
  (vt 0x00A90304). Both classes are compatible-ABI vtable-dispatch receivers
  that are provably NOT SceneFeeder.
- Additionally, the 5 strongest-bounded Phase D dispatch candidates (proven
  other-class receivers: MaPanelText/Line/Rect/Map, ArkVegetationObservable)
  dispatch their own classes' slot-2 functions, byte-verified != the thunk
  (ARG2_VALUE_FLOW_RAW.txt [E3]; R2: ArkVegetationObservable has NO slot-2
  entry — its vtable extent is 1 slot; the dword at the slot-2 position is
  0x566B7241 = ASCII "ArkV" string data, not a code pointer).

G7 PASS: >=1 compatible-ABI non-SceneFeeder class demonstrated from own bytes;
FAILURE_CASE_DETECTED = YES.

## Interpretation (R2 CORRECTED)

The slot-2 thunk (delegate to [this+0x14]'s slot 3), its sibling delegation
stubs, the held-object refcounted release path, the SceneFeederObject
machinery, AND the binding edge (objects INTO [this+0x14]) all exist in the
binary — the binding edge is exercised at every bounded normal construction
of the 4 param-chained classes (the field is a LIVE COMPOSITE/CHANNEL-
ANIMATION BINDING: a family animation object holding an
ArkAnimationFloatValue-hierarchy channel child — Scale/Rotation/Translation/
Intensity/Color/Alpha). The construction layer is STATICALLY REACHABLE: the
dispatcher construct entry 0x006D0ED0 has 3 direct E8 callers
(0x0058EFD6/0x0058F19F/0x006D2B1C; R2 re-derived). The R1 "unexercised stub
layer" reading is RETRACTED (AMEND_LOG_R2 R2-3), as is the R1 crash-
consistency argument ("a hypothetical dispatch would fault at [NULL]") — a
slot-2 dispatch on a live composite forwards to the CHILD's slot-3 and would
NOT fault. What remains without a statically-identifiable caller is the
slot-2 forwarder itself (Phase D: 0 direct E8/E9/EB, imm32 only the 5 own
vtable slot dwords, 0 PROVEN dispatch candidates among 1,438; the 1,433
INSUFFICIENT_PROOF candidates remain honestly unproven — no fault-shortcut
is applied). The Rosetta edge
"ArkAnimation -> [this+0x14] -> SceneFeeder slot-3 -> NiNode::GetObjectByName"
is falsified AT THE RECEIVER-IDENTITY LINK. UNKNOWN stays UNKNOWN: no claim
is made about runtime-modified, patched, or computed-alias flows outside
static reach (declared failure classes, contract §8).
