# REPORT — PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914

RUN_CLASS MATERIAL. Bounded static mini-check, STATIC-ONLY (the Entropia client never
ran). Executor: pe-reconstruction, direct PE-MASTER dispatch, NO_NESTED_TASKS.
BASE_SHA 3644e5ac9cbf7b5445861e7f5342fb8642741346 (= origin/master = live remote
master = isolated worktree HEAD, re-verified).

---

## ANSWERS FIRST

**1. What method is GB 1.1.2 NiNode slot 17 (+0x44)?**

`NiNode::SetSelectiveUpdateFlags(bool&, bool, bool&)` — mangled
`?SetSelectiveUpdateFlags@NiNode@@UAEXAA_N_N0@Z`. Measured at slot 17 (+0x44) of the
compiled `??_7NiNode@@6B@` vtable in the era VC71 ReleaseLib NiMain.lib (member /2822,
32 slots). NiNode::GetObjectByName is at slot **16** (+0x40) in GB 1.1.2.
Evidence: 03_EVIDENCE/GB112_NIMAIN_LIB_VTABLE_DUMP.json; 01_RAW/GB112_SOURCE_LOCATORS.md.

**2. What method is GB 1.2.2.6 NiNode slot 17 (+0x44)?**

`NiNode::ApplyTransform(const NiMatrix3&, const NiPoint3&, bool)` — mangled
`?ApplyTransform@NiNode@@UAEXABVNiMatrix3@@ABVNiPoint3@@_N@Z`. Measured at slot 17
(+0x44) of the compiled `??_7NiNode@@6B@` vtable (gb12_build NiNode.obj, 34 slots).
NiNode::GetObjectByName is at slot **18** (+0x48) in GB 1.2.2.6. The +2 shift vs 1.1.2
is caused by `NiObject::GetGroup`/`SetGroup` becoming virtual in 1.2.2.6 (slots 13/14).
Evidence: 03_EVIDENCE/GB12_NINODE_OBJ_VTABLE_DUMP.json, GB12_CHAIN_OBJ_VTABLE_DUMP.json.

**NEITHER oracle places GetObjectByName at slot 17.** A slot-number-based matcher
would have produced two different wrong labels for Entropia slot 17 (SetSelectiveUpdateFlags
under GB112, ApplyTransform under GB12) — this is negative control NC2, and it is why
the Entropia identification had to be behavioral.

**3. What does Entropia 0x007B5390 actually do?**

Measured from physical Entropia.exe bytes (SHA256 pin re-verified inside the tools):
a **recursive named-object lookup** on an object that has a name member and a child
pointer array:

- Self-name-check FIRST: direct call to helper 0x007BF220, which NULL-guards the
  argument, reads the object's name at **this+0x0C**, runs an inlined byte-pair
  strcmp, and returns `this` on match, NULL otherwise.
- Then iterates children: count at **this+0xD4**, array at **this+0xCC**, 4-byte
  pointer stride, NULL entries skipped; for each child it makes a **recursive
  virtual call through the child's vtable slot +0x44 — the SAME slot this function
  occupies** — passing the SAME name argument.
- Returns the first non-NULL result; returns NULL on zero count, loop exhaustion,
  NULL name, or NULL object name.
- ABI: thiscall, one `const char*` stack argument (`ret 4`), EAX = object pointer
  or NULL. Extent 0x007B5390..0x007B53E0.

Additionally measured this run (vtable ABI prefix + neighborhood, all from Entropia
bytes): slot 0 = vector deleting dtor (flags&1 -> operator delete), slot 1 = scalar
deleting dtor thunk (`vtable[0](this,1)`), slot 2 = GetRTTI returning 0x00BA7218,
proven by the static initializer `NiRTTI(0x00BA7218, "NiNode", base 0x00BA7270)` to be
NiNode's Gamebryo NiRTTI with base NiAVObject — a second, independent RTTI system in
the same binary agreeing with the MSVC RTTI chain. Slots 16 (transform applier,
ApplyTransform-shaped), 18 (selective-update flags, with the exact GB SELECTIVE_*
flag masks at +0x20), and 27 (UpdateWorldData, instruction-near-identical to the
GB112 compiled body incl. m_kLocal@+0x38 / m_kWorld@+0x6C) were decoded as negative
controls and ABI anchors.

**4. Does it match GetObjectByName?**

Yes — behaviorally, and nearly byte-for-byte. The Entropia function is almost
instruction-identical to the era VC71 compiled `?GetObjectByName@NiNode@@...`
(same prologue `push ebx; mov ebx,[esp+8]; push edi; push ebx; mov edi,ecx; call <base>;
test; jne`, same guarded child-loop idiom, same base-call-first ordering, same inlined
strcmp ladder in the self-check, `ret 4`), with positional deltas that are themselves
measured and consistent: children array/size at +0xCC/+0xD4 (GB112: +0xB8/+0xC0),
recursion slot +0x44 (GB112: +0x40 — Entropia's vtable carries one extra
destructor-related slot, measured at slots 0/1), name member at +0x0C (same as GB112;
GB12 moved it to +0x08). All 14+ comparison dimensions are in
02_ANALYSIS/CROSS_VERSION_COMPARISON.csv.

**5. Final FUNCTION_IDENTITY status?**

**B — STRONGLY_SUPPORTED_GETOBJECTBYNAME.** Not A (CONFIRMED): an A requires
exact/era-exact vtable/ABI support, and Entropia's actual engine generation is not
in the pinned oracle set — its NiNode vtable has 47 slots vs the oracles' 32/34, its
class data tail carries +0x14 extra bytes before the children array, and vtable
slots 3..15 were not individually decoded, so the slot-position alignment is a
measured, partially-verified model (anchored at slots 0/1/2/16/17/18/27), not an
exact ABI transfer. The behavioral equivalence alone (self-name-check + child
iteration + same-slot recursive virtual dispatch + first-match-or-NULL + thiscall/1-arg
`ret 4`) is highly distinctive and matches the oracles' compiled bodies; per the
status algebra that yields at most B, which is the verdict. OBSERVED_OPERATION:
recursive named-object lookup. FINAL_SEMANTIC_ROLE: "0x007B5390 = GetObjectByName-like
NiNode lookup" (this run's maximum permitted claim).

**6. What does +0x90 mean in GB112, GB12, and what for Entropia?**

- GB 1.1.2: **m_kWorld.m_Translate.x — the WORLD TRANSLATE X component**
  (m_kWorld at +0x6C..+0x9F; NiTransform translate at +0x24; compiled ctor +
  UpdateWorldData `rep movsd` x13 evidence).
- GB 1.2.2.6: **m_kWorld.m_Translate.y — the WORLD TRANSLATE Y component**
  (m_kWorld at +0x68..+0x9B; compiled UpdateWorldData reads parent world translate
  X/Y/Z at +0x8C/+0x90/+0x94). The oracle pair demonstrates that "+0x90 lies inside
  the world translate" is NOT transferable by component position between versions.
- Entropia: **m_kWorld.m_Translate.x — the WORLD TRANSLATE X component — MEASURED
  THIS RUN from Entropia bytes** (not oracle transfer): slot 27 = UpdateWorldData
  writes m_kWorld at **+0x6C** via `rep movsd` x13 (52-byte NiTransform), sourced
  from m_kLocal@+0x38 (or × parent's m_kWorld@+0x6C); slot 16 independently anchors
  the NiTransform internal layout (translate at transform+0x24 via the +0x5C usage,
  scale at transform+0x30 via +0x68). This closes what the interrupted prior
  sessions had honestly left UNKNOWN. (Entropia matches GB112's +0x90 semantics;
  the children-array tail offsets differ from GB112 — its generation remains
  unidentified.)

**7. Does this change TRANSFORM_TO_MODEL?**

**NO. TRANSFORM_TO_MODEL remains NOT_DEMONSTRATED** (unchanged, per the model-bridge
guard). This run establishes at most: "the SF+0x30 NiNode behaves as a scene-graph
root/container from which named NiAVObjects can be queried" (PLAUSIBLE). No bridge
from the found object to any "model", no scene-feeder channel semantics, and no
historical placement claims are made or implied by this run.

---

## Method (compact)

- Boot pins re-verified: Entropia.exe SHA256/size, gb12_oracle.exe SHA256 (banner
  treated as stale, identity by SHA only), BASE_SHA vs origin/master vs live
  `git ls-remote` — all matched.
- Two independent methods per oracle (contract §3): (1) inheritance-aware header
  reconstruction including ALL macro-expanded virtuals (NiDeclareRootRTTI/NiDeclareRTTI
  -> GetRTTI; NiDeclareClone -> CreateClone; NiDeclare[Abstract]Stream -> 5 streaming
  virtuals; NiDeclare[Abstract]ViewerStrings -> GetViewerStrings) and (2) compiled
  relocation evidence (`??_7Class@@6B@` vtable symbols mapped slot-by-slot to MSVC
  symbols via COFF relocation tables). The methods agree on every class in both
  versions. Both oracle builds use a SINGLE `??_E` dtor slot at index 0 (proven from
  the era VC71 lib: the root `??_7NiRefObject@@6B@` has exactly 1 slot).
- Entropia: everything re-measured from the physical exe (RTTI walk, vtable slot
  census, function + helper disassembly, neighbor slots, byte-pattern probes).
- Evidence: 01_RAW (raw listings + source locators with SHA256 pins),
  02_ANALYSIS (maps, fingerprints, comparison CSV, negative controls, +0x90 oracle),
  03_EVIDENCE (regenerated dumps + index + README). All evidence was regenerated by
  the completing session; see 00_CONTROL/RUN_CONTRACT.md honesty note about the two
  earlier interrupted sessions of this same RUN_ID.

## Gate summary

G0..G9 all PASS — details with MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH /
WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED per gate in
06_REPORT/STAGE_ACCEPTANCE_GATES.csv.

## Caveats and limitations

1. **Entropia's engine generation is unidentified.** The pinned oracles (GB 1.1.2,
   GB 1.2.2.6) are both earlier generations; Entropia's 47-slot NiNode vtable,
   its 2-slot dtor prefix (vs the oracles' 1), and its +0x14 class-tail delta prove
   it is neither. Gamebryo 2.6-era materials exist on disk (Gb26/, Gb26_src/) but
   are OUT of the contract-pinned oracle set and were deliberately NOT used.
2. **Slots 3..15 of the Entropia NiNode vtable were not decoded** — the +1-shift
   alignment model is anchored at seven slots (0, 1, 2, 16, 17, 18, 27), not the
   full prefix. This is why the verdict is B, not A.
3. GB12 compiled evidence comes from the project-built VS2022 objects; the build
   consumed a `gb12_build\src` copy verified byte-identical (SHA256) to
   `Gb12_Source` for the chain headers, and the two-method cross-check (headers vs
   relocations) still applies. Era-VC71 evidence for GB112 comes from NDL's own
   shipped lib.
4. The Entropia +0x90 result is a STRUCTURAL fact about the NiAVObject layout; it
   does not decode the SceneFeeder consumer chain (`returned_object+0x90 ->
   downstream`), which stays as published (INPUT) and out of scope here.
5. GB 1.1.2 evaluation SDK ships no NiMain .cpp; its GetObjectByName body is
   recovered from compiled code only (the disassembly IS the evidence).
6. The "NiNode" name provenance inside Entropia is proven via the static
   initializer call site + the "NiNode" .rdata literal; the NiRTTI object itself
   lives in .data's virtual-only tail (zero on disk, runtime-constructed).
7. No live/runtime evidence at all: the client never ran; every claim is static
   and reproducible from the pinned files.
