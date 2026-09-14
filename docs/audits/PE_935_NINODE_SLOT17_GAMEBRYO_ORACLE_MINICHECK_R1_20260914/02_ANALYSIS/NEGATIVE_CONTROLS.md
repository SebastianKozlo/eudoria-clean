# NEGATIVE_CONTROLS (G6) — all three executed, all meaningful

## NC1 — nearby Gamebryo virtuals with clearly different behavior; the Entropia
## matcher rejects them

Two layers of this control were run: (a) the ACTUAL slot-17 occupants of the two
pinned oracles — the two wrong labels a slot-number matcher would have produced;
(b) the MEASURED adjacent slots of the Entropia vtable itself (decoded this run,
`03_EVIDENCE/ENTROPIA_SLOT_NEIGHBORS_DISASM.txt`) — real neighboring methods with
clearly different behavior from 0x007B5390.

**(a) Oracle slot-17 occupants (wrong labels under slot-number matching):**

**Candidate A: `NiNode::ApplyTransform(const NiMatrix3&, const NiPoint3&, bool)` —
GB 1.2.2.6 NiNode slot 17** (compiled evidence, `GB12_NINODE_OBJ_VTABLE_DUMP.json`
slot 17, mangled `?ApplyTransform@NiNode@@UAEXABVNiMatrix3@@ABVNiPoint3@@_N@Z`).
Measured rejection grounds:
- takes THREE stack arguments (12 bytes) -> a matching Entropia callee would end
  `ret 0xC`; measured 0x007B5390 ends `ret 4` -> REJECT.
- returns VOID (no EAX result contract); measured 0x007B5390's result is consumed as
  pointer-or-NULL (`test eax,eax; jne`) by its own control flow -> REJECT.
- performs matrix math and writes the local transform; measured 0x007B5390 contains
  no floating-point instruction at all -> REJECT.
- no string/name comparison anywhere; measured helper 0x7BF220 is entirely a string
  comparison -> REJECT.

**Candidate B: `NiNode::SetSelectiveUpdateFlags(bool&, bool, bool&)` —
GB 1.1.2 NiNode slot 17** (compiled evidence, `GB112_NIMAIN_LIB_VTABLE_DUMP.json`
member /2822 slot 17, mangled `?SetSelectiveUpdateFlags@NiNode@@UAEXAA_N_N0@Z`).
Measured rejection grounds: three arguments -> `ret 0xC` vs measured `ret 4` ->
REJECT; void return -> REJECT; writes caller-provided bool flags; no name member
access, no first-match pointer return -> REJECT.

**(b) Measured Entropia neighbors (same vtable, adjacent ordinals):**

- **slot 16 = 0x007B4650** (transform applier): contains heavy x87 fp math
  (fld/fadd/fsub/fmul/fdiv on m_kLocal@+0x38), a boolean argument gate, and iterates
  the SAME children array (+0xCC/+0xD4) — but performs NO name access, NO string
  comparison and returns no first-match pointer; its child recursion dispatches its
  own slot. A behavioral matcher for 0x007B5390 rejects it on: name-comparison
  absent, fp present, argument-shape mismatch. (NC1 REAL, not hypothetical.)
- **slot 18 = 0x007B5160** (selective-update flags): takes `bool&`/`bool`/`bool&`
  (writes through the caller-provided pointers), writes the flag member at +0x20
  with masks 0x2/0x4/0x8/0x10, recurses at child vtable +0x48 (its own slot); no
  name member access, no string compare, void return. REJECT.

Conclusion: had the matcher been slot-number-based, GB112 would have labeled Entropia
slot 17 "SetSelectiveUpdateFlags" and GB12 would have labeled it "ApplyTransform" —
both wrongly, since both candidates are incompatible with the measured Entropia bytes;
the measured neighbors (slots 16/18) are equally incompatible. The behavioral matcher
is meaningfully selective.

## NC2 — does vtable numbering differ between 1.1.2 and 1.2.2.6 for the relevant chain?

**YES — proven, not assumed.** Compiled relocation evidence:

| Identity | GB 1.1.2 slot | GB 1.2.2.6 slot | delta |
|---|---|---|---|
| NiObject::GetBlockAllocationSize | 12 | 12 | 0 |
| NiObject::GetGroup | (non-virtual) | 13 | +1 new |
| NiObject::SetGroup | (non-virtual) | 14 | +1 new |
| NiAVObject::UpdateControllers | 13 | 15 | +2 |
| NiAVObject::ApplyTransform | 15 | 17 | +2 |
| NiAVObject::GetObjectByName | 16 | 18 | +2 |
| NiAVObject::SetSelectiveUpdateFlags | 17 | 19 | +2 |
| NiNode::AttachChild | 27 | 29 | +2 |
| NiNode total slots | 32 | 34 | +2 |

Cause (source-proven): `GetGroup`/`SetGroup` became virtual in 1.2.2.6
(GB112 `NiObject.h` L53-54 non-virtual vs GB12 `NiObject.h` L59-60 virtual;
GB12 `NiObject.cpp` L53-62 shows the group member removed from NiObject storage).

**And the same control applied to Entropia:** Entropia's vtable carries TWO
destructor-related slots (slot 0 = vector deleting dtor 0x0082E420; slot 1 = scalar
deleting dtor thunk 0x00406D50 calling vtable[0] with flags=1) before GetRTTI at
slot 2 (0x007B60C0 -> NiNode::ms_RTTI 0x00BA7218, proven via the static initializer
`NiRTTI(0xBA7218, "NiNode", 0xBA7270)`), while BOTH oracles have GetRTTI at slot 1
with a single `??_E` dtor slot. Slot numbering is therefore version- AND
toolchain-dependent; no slot ordinal was used as identification evidence — the
Entropia identity rests on behavior, with the +1 shift recorded as a consistent
observation (slots 16/17/18/27 behaviorally match GB112 slots 15/16/17/26).

Consequences enforced by this run:
1. Slot ordinal alone CANNOT identify a method across versions or builds.
2. Entropia's slot-17 identity was determined behaviorally from Entropia bytes;
   the oracles supplied the comparison inventory.
3. The fact that Entropia's ordinal (17) sits between the two oracles' GetObjectByName
   ordinals (16, 18) is reported as an observation consistent with the measured
   +1-dtor-slot ABI shift — NOT used as proof.

## NC3 — distinctive behaviors whose absence would falsify the GetObjectByName hypothesis

Falsifiers defined BEFORE measurement; each is a measurable property of the Entropia
bytes; all four were found PRESENT. Had any been absent, FUNCTION_IDENTITY would have
been D/E (plausible/rejected/inconclusive):

| # | Falsifier (absence would falsify) | Measured status |
|---|---|---|
| 1 | No name/string comparison in the function or its self-check callee | PRESENT: helper 0x7BF220 reads [this+0x0C] and executes an inlined byte-pair strcmp ladder (0x7BF230..0x7BF265) |
| 2 | No child traversal (no array+count member pair, no loop) | PRESENT: loop over array [this+0xCC] with count [this+0xD4], 4-byte stride, NULL-skip (0x7B53B3..0x7B53D7) |
| 3 | Incompatible argument/return behavior (e.g. 3 args -> ret 0xC, void return, or non-pointer EAX) | PRESENT as COMPATIBLE: thiscall, one 4-byte char* arg (ret 4), EAX pointer-or-NULL with test/jne at both consumers, xor eax,eax null path |
| 4 | Recursion dispatching a DIFFERENT slot than the function's own slot (would break override coherence — children of other subclasses would call unrelated methods) | PRESENT as COHERENT: child recursion loads child vtable slot +0x44 — the same slot that contains 0x007B5390 in the NiNode vtable (self-consistent virtual override design) |

Additionally, the base-check-FIRST ordering (self name tested before children) and the
first-match short-circuit are both present and match both compiled oracles —
they are part of the fingerprint, though not individually falsifier-graded.

The hypothesis was falsifiable on four independent measured axes and survived all
four; combined with NC1 (the matcher rejects both real oracle slot-17 alternatives
AND the measured adjacent Entropia slots) and NC2 (slot-number transfer is proven
invalid in both directions), the negative-control suite is meaningful, not vacuous.
