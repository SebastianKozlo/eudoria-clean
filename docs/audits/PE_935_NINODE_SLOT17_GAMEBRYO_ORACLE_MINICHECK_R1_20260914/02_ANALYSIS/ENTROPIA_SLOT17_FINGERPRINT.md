# ENTROPIA_SLOT17_FINGERPRINT — 0x007B5390 decoded from physical bytes (Questions C/D)

Decoded STATIC-ONLY from `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`
(SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`,
re-verified inside the tools on every execution) by this run's own scripts. The
untracked WIP packages were NOT used. Raw listing: `01_RAW/ENTROPIA_007B5390_DISASM.txt`
(function + full helper). Neighbor-slot decodes, vtable/RTTI facts and the NiRTTI
static-init proof: `03_EVIDENCE/`.

## Measured object facts

- IMAGE_BASE 0x00400000; PE section table measured from the file: .text RVA 0x1000
  (raw==RVA), .rdata RVA 0x675000 (raw==RVA), .data RVA 0x76C000 (raw==RVA for
  RawSize 0x34000 only — the rest of VSize 0x3D6E4 is virtual-only, zero on disk).
- Primary NiNode vtable VA 0x00A8CCF4 (MSVC RTTI `.?AVNiNode@@`, base chain
  NiAVObject -> NiObjectNET -> NiObject -> NiRefObject — RTTI walk). Vtable extent:
  47 slots (0..46); slot 47 would be non-code (value 0x65666665).
- **[vtable+0x44] (slot 17) = 0x007B5390** (re-measured, `target_slot17.match = true`).

## Entropia vtable ABI prefix — measured (this run's new evidence)

Slots 0, 1, 2 were decoded to anchor the vtable layout before any comparison:

- **slot 0 = 0x0082E420** — vector deleting destructor: calls the dtor body 0x007B60D0,
  then `test flags&1` -> `call 0x0095D42A` (operator delete, MSVCR80 — consistent with
  the published SceneFeeder census) -> `ret 4`.
- **slot 1 = 0x00406D50** — scalar deleting destructor thunk:
  `test ecx,ecx; je ret; mov eax,[ecx]; mov edx,[eax]; push 1; call edx` — i.e.
  `if (this) vtable[0](this, 1)`.
- **slot 2 = 0x007B60C0** — `mov eax, 0x00BA7218; ret` = GetRTTI. Static-init proof
  (`03_EVIDENCE/ENTROPIA_NIRTTI_STATIC_INIT.txt`): initializer at 0x00A6C200 runs
  `NiRTTI(0x00BA7218 /*this*/, "NiNode"@0x00A8CE00, base 0x00BA7270 /*NiAVObject*/)`
  via ctor 0x007199E0 — Entropia's own Gamebryo RTTI names the class "NiNode" with
  base NiAVObject, agreeing with the MSVC RTTI chain.

Both pinned oracles have GetRTTI at slot 1 (their builds have a SINGLE destructor
slot: `??_7NiRefObject@@6B@` = exactly 1 slot in the era VC71 lib; all oracle vtables
start `??_E`, `GetRTTI`, ...). Entropia carries TWO destructor-related slots before
GetRTTI, so every GB112-analogous ordinal shifts by +1. Four later slots were decoded
to confirm the shifted alignment (`03_EVIDENCE/ENTROPIA_SLOT_NEIGHBORS_DISASM.txt`):

| Entropia slot | VA | Measured behavior | GB112 slot (−1 shift) | GB112 identity |
|---|---|---|---|---|
| 16 (+0x40) | 0x007B4650 | transform applier: fp matrix/vector math on m_kLocal@+0x38 (translate@+0x5C, scale@+0x68), bool arg gate, children loop (+0xCC/+0xD4) | 15 | ApplyTransform |
| **17 (+0x44)** | **0x007B5390** | **recursive named-object lookup (below)** | **16** | **GetObjectByName** |
| 18 (+0x48) | 0x007B5160 | selective-update flags: bool&/bool/bool& args; writes m_uFlags@+0x20 with masks 0x2/0x4/0x8/0x10 (GB SELECTIVE_* masks); child recursion at +0x48 | 17 | SetSelectiveUpdateFlags |
| 27 (+0x6C) | 0x007E4820 | UpdateWorldData: m_kWorld@+0x6C = parent? m_kLocal@+0x38 * parent->m_kWorld@+0x6C : m_kLocal; `rep movsd` 13 dwords; collision obj @+0xB0 -> dispatch [eax+0x3C] | 26 | UpdateWorldData |

The slot-27 decode is instruction-for-instruction near-identical to the GB112
compiled `NiAVObject_Win32.obj` `UpdateWorldData` (member offsets +0x24/+0x38/+0x6C/
+0xB0 identical; collision dispatch +0x3C vs +0x38 = the same +1 dtor-slot shift).

## Function 0x007B5390 — boundaries and ABI

- Entry 0x007B5390 (preceded by the prior function's epilogue tail; followed, after
  its own ret, by 0xCC padding) -> extent 0x007B5390..0x007B53E0; `ret 4` at
  0x007B53DE; padding 0xCC from 0x007B53E1.
- Calling convention: **thiscall** — `this` in ECX (saved to EDI: `mov edi, ecx`),
  ONE stack argument consumed by callee (`ret 4`), loaded `mov ebx, [esp+8]` and
  used as a `const char*` string pointer (see helper).

## Control flow (measured)

```
0x7B5390  push ebx
0x7B5391  mov  ebx, [esp+8]          ; arg1 (const char* name)
0x7B5395  push edi
0x7B5396  push ebx                   ; pass name
0x7B5397  mov  edi, ecx              ; this
0x7B5399  call 0x7BF220              ; SELF-NAME CHECK (base semantics), args (this, name)
0x7B539E  test eax, eax
0x7B53A0  jne  0x7B53DC              ; found -> return it
0x7B53A2  mov  eax, [edi+0xD4]       ; children COUNT (unsigned)
0x7B53A8  push esi
0x7B53A9  xor  esi, esi              ; i = 0
0x7B53AB  test eax, eax
0x7B53AD  jbe  0x7B53D9              ; count == 0 -> return NULL
0x7B53AF  cmp  eax, esi
0x7B53B1  jbe  0x7B53CC
0x7B53B3  mov  eax, [edi+0xCC]       ; children ARRAY (pointer elements, 4-byte stride)
0x7B53B9  mov  ecx, [eax+esi*4]      ; child = children[i]
0x7B53BC  test ecx, ecx
0x7B53BE  je   0x7B53CC              ; NULL element -> skip
0x7B53C0  mov  edx, [ecx]            ; child vtable
0x7B53C2  mov  eax, [edx+0x44]       ; SLOT 17 (+0x44) of the child's vtable
0x7B53C5  push ebx                    ; pass the SAME name argument
0x7B53C6  call eax                    ; recursive virtual call (SAME slot as this function)
0x7B53C8  test eax, eax
0x7B53CA  jne  0x7B53DB              ; found -> return it
0x7B53CC  mov  eax, [edi+0xD4]       ; reload count
0x7B53D2  add  esi, 1                ; ++i
0x7B53D5  cmp  eax, esi
0x7B53D7  ja   0x7B53B3              ; loop while count > i
0x7B53D9  xor  eax, eax              ; return NULL
0x7B53DB  pop  esi
0x7B53DC  pop  edi
0x7B53DD  pop  ebx
0x7B53DE  ret  4                     ; callee cleanup of the single 4-byte argument
```

The one opened callee, **0x007BF220**, was opened because it is the first and only
callee before the child loop and carries the name-comparison component that NC3
requires testing. Full extent 0x007BF220..0x007BF270 (`ret 4` at 0x007BF26D; int3
padding from 0x007BF275):

```
0x7BF220  mov  eax, [esp+4]         ; name
0x7BF224  test eax, eax
0x7BF226  je   0x7BF26B             ; name == NULL -> return NULL
0x7BF228  mov  edx, [ecx+0x0C]      ; GetName() == name member at this+0x0C
0x7BF22B  test edx, edx
0x7BF22D  je   0x7BF26B             ; this->name == NULL -> return NULL
0x7BF22F  ...                        ; INLINED strcmp: 2-bytes-per-iteration compare ladder
0x7BF24C  ...                        ; equal -> returns this (flag idiom: xor/neg/sbb/not; and eax, ecx)
0x7BF26A/0x7BF25A                    ; mismatch -> normalized to 0 -> and eax, ecx -> NULL
0x7BF26B  xor  eax, eax; ret 4      ; NULL epilogue
```

No other callee of 0x007B5390 exists; no downstream traversal was performed.

## Behavioral fingerprint of 0x007B5390 (measured facts)

1. **Self-name-check first**: direct call to a helper that (a) NULL-guards the argument,
   (b) reads the object's name member at **this+0x0C**, (c) inlined byte-pair strcmp,
   (d) returns `this` on match, NULL otherwise.
2. **Child iteration**: count at **this+0xD4** (unsigned), array at **this+0xCC**,
   4-byte pointer stride, NULL elements skipped.
3. **Recursive virtual dispatch through the SAME slot (+0x44)** used to reach this
   function — self-consistent override design: every NiAVObject-derived child answers
   the same query at the same ordinal.
4. **First-match return**, NULL on exhaustion / zero count / NULL name.
5. **ABI**: thiscall, one `const char*` stack argument, callee cleanup (`ret 4`),
   EAX = object pointer or NULL.

## Immediate object offsets measured (no others touched in this function)

| Offset | Meaning (measured role in this function) |
|---|---|
| +0x0C | name member of the NiObjectNET sub-object (read by the self-check helper) |
| +0xCC | children array pointer (NiNode, NiTArray-style: base then +8 used-count) |
| +0xD4 | children used count (NiNode) |
| child vtable +0x44 | recursive query slot (this function's own slot) |

## Structural identification (measured, non-circular)

Within the pinned oracles' NiNode method inventory the measured shape is
NiNode::GetObjectByName: it is nearly instruction-identical to the era VC71 compiled
`?GetObjectByName@NiNode@@UAEPAVNiAVObject@@PBD@Z` (GB 1.1.2 NiMain.lib, member
.\releaselib\NiNode.obj — same prologue, same guarded-loop idiom, same base-call-first
ordering, `call [edx+0x40]` vs Entropia `call [edx+0x44]` = the measured +1 dtor-slot
shift, children +0xB8/+0xC0 vs +0xCC/+0xD4 = version-tail data delta). See
CROSS_VERSION_COMPARISON.csv for the dimension-by-dimension comparison and
NEGATIVE_CONTROLS.md for the falsification tests.

## Classification (measured + bounded)

OBSERVED_OPERATION: recursive named-object lookup (self-name-check-first helper,
child-array iteration, same-slot recursive virtual dispatch, first-match-or-NULL,
thiscall/1 stack arg/ret 4).

FUNCTION_IDENTITY: **B — STRONGLY_SUPPORTED_GETOBJECTBYNAME**. The behavioral
equivalence to the oracles' compiled NiNode::GetObjectByName is exact in shape and
nearly exact in bytes, and the ABI alignment is anchored at seven decoded slots;
status stays at B (not A) because Entropia's engine generation is NOT the pinned
oracle versions — its NiNode vtable has 47 slots vs the oracles' 32/34, its NiNode
data tail carries +0x14 extra bytes before the children array, and slots 3..15 were
not individually decoded — so the slot-position alignment is a measured, partially
verified model rather than an exact/era-exact ABI transfer.

FINAL_SEMANTIC_ROLE (bounded by the model-bridge guard): 0x007B5390 is a
GetObjectByName-like NiNode lookup; at most "the SF+0x30 NiNode behaves as a
scene-graph root/container from which named NiAVObjects can be queried" (PLAUSIBLE).
TRANSFORM_TO_MODEL remains NOT_DEMONSTRATED and is untouched by this run.
