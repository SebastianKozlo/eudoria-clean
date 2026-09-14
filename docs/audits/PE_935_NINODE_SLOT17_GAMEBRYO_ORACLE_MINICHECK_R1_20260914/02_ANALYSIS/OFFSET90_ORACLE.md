# OFFSET90_ORACLE — returned_object +0x90 (Secondary mini-check, G7)

Question: what structural member/range of NiAVObject contains object offset +0x90 in
GB 1.1.2 and GB 1.2.2.6, separately, with empirical anchoring; and what is +0x90 in
Entropia — proven from Entropia bytes if possible.

## Method (non-circular)

Each version's answer is anchored in ITS OWN compiled code (not header math alone):

1. **Compiled constructors** (`??0NiAVObject@@IAE@XZ`) give the member base offsets:
   `lea ecx,[this+X]` / direct stores reveal m_uFlags, m_pkParent, m_kWorldBound,
   m_kLocal, m_kWorld, m_kPropertyList, m_spCollisionObject.
   Evidence: `03_EVIDENCE/GB112_NIAVOBJECT_CTOR_DISASM.txt`,
   `03_EVIDENCE/GB12_NIAVOBJECT_CTOR_DISASM.txt`.
2. **Compiled UpdateWorldData** gives the transform extents and the world-translate
   component offsets. GB112/Entropia copy loop `rep movsd` with count 0xD proves
   NiTransform = 13 dwords = 52 bytes; GB12 (SSE codegen) reads the parent world
   translate X/Y/Z at `[esi+0x8C]/[esi+0x90]/[esi+0x94]` and parent world scale at
   `[esi+0x98]`.
   Evidence: `03_EVIDENCE/GB112_NIAVOBJECT_UPDATEWORLDDATA_DISASM.txt`,
   `03_EVIDENCE/GB12_NIAVOBJECT_UPDATEWORLDDATA_DISASM.txt`,
   `03_EVIDENCE/ENTROPIA_SLOT_NEIGHBORS_DISASM.txt` (slot 27).
3. **Headers** (pinned, SHA256'd) supply the member names and the NiTransform member
   order (`m_Rotate` [36 bytes, `float m_pEntry[3][3]`], `m_Translate` [12 bytes],
   `m_fScale` [4]); the NiTransform class block is BYTE-IDENTICAL between the two
   oracle versions; `NI_DATA_ALIGMENT(16)` is EMPTY on Win32 (`NiRTLib.h` L37), so
   NiBound is a plain 16-byte member. NiTListBase/NiTArray each carry a vftable
   (virtual dtor), which is required for the member-size math and was proven by the
   compiled ctor's store to +0xA0 (list vtable) and by the children-array offsets.

## GB 1.1.2 NiAVObject layout (compiled-empirical)

| Offset | Member | Anchor |
|---|---|---|
| +0x00 | vptr | ctor vtable store (reloc to ??_7NiAVObject) |
| +0x04 | NiRefObject::m_uiRefCount | header L34 |
| +0x08 | NiObject::m_pkGroup | header L61 |
| +0x0C | NiObjectNET::m_pcName | compiled NiAVObject::GetObjectByName reads [this+0xC] |
| +0x10..+0x1F | m_spControllers, m_ppkExtra, m_uiExtraDataSize, m_uiMaxSize | header L140-145 |
| +0x20 | m_uFlags (u16, +2 pad) | ctor `mov word [esi+0x20], di` |
| +0x24 | m_pkParent | ctor `mov [esi+0x24], edi` (0); UWD reads parent at [ebx+0x24] |
| +0x28..+0x37 | m_kWorldBound (center +0x28..+0x33, radius +0x34) | ctor `lea eax,[esi+0x28]` |
| **+0x38..+0x67** | **m_kLocal (NiTransform, 52 bytes)** | ctor `lea ecx,[esi+0x38]`; UWD `lea esi,[ebx+0x38]` |
| **+0x6C..+0x9F** | **m_kWorld (NiTransform, 52 bytes)** | ctor `lea ecx,[esi+0x6C]`; UWD `lea edi,[ebx+0x6C]` + `rep movsd` x13 |
| +0xA0..+0xAF | m_kPropertyList (vftable + 3 fields) | ctor stores at 0xA0/0xA4/0xA8/0xAC |
| +0xB0 | m_spCollisionObject | ctor store + refcount handling at [esi+0xB0] |
| total size | 0xB4 | last member end |

Within both transforms: rotate at +0x00..+0x23 (36 bytes), **translate at +0x24..+0x2F**,
scale at +0x30.

**GB 1.1.2 ANSWER: +0x90 lies INSIDE m_kWorld, at m_kWorld+0x24 = `m_kWorld.m_Translate.x`
— the WORLD TRANSLATE X component.** (Local translate for contrast is at +0x5C;
world translate X/Y/Z at +0x90/+0x94/+0x98; world scale +0x9C.)

## GB 1.2.2.6 NiAVObject layout (compiled-empirical)

Identical member ORDER; the whole prefix is 4 bytes SMALLER because
NiObject::m_pkGroup was removed (NiObject.cpp L53-62):

| Offset | Member | Anchor |
|---|---|---|
| +0x00 | vptr | ctor vtable store (reloc) |
| +0x04 | m_uiRefCount | header |
| +0x08 | m_pcName | compiled NiAVObject::GetObjectByName reads [this+0x08] |
| +0x0C..+0x1B | m_spControllers, m_ppkExtra, m_uiExtraDataSize, m_uiMaxSize | header L140-145 |
| +0x1C | m_uFlags (u16, +2 pad) | ctor `mov word [esi+0x1C], ax` |
| +0x20 | m_pkParent | ctor `mov [esi+0x20], 0`; UWD reads parent at [edi+0x20] |
| +0x24..+0x33 | m_kWorldBound | ctor `movq [esi+0x24]` + `[esi+0x2C]` + radius `[esi+0x30]` |
| **+0x34..+0x67** | **m_kLocal (52 bytes)** | ctor `lea ecx,[esi+0x34]`; UWD `lea ebx,[edi+0x34]` |
| **+0x68..+0x9B** | **m_kWorld (52 bytes)** | ctor `lea ecx,[esi+0x68]`; UWD reads parent m_kWorld at [esi+0x68], scale [esi+0x98], own write `movups [edi+0x68]` |
| +0x9C..+0xAB | m_kPropertyList | ctor stores at 0x9C/0xA0/0xA4/0xA8 |
| +0xAC | m_spCollisionObject | ctor store + refcount handling at [esi+0xAC] |
| total size | 0xB0 | last member end |

**GB 1.2.2.6 ANSWER: +0x90 lies INSIDE m_kWorld, at m_kWorld+0x28 = `m_kWorld.m_Translate.y`
— the WORLD TRANSLATE Y component.** Direct compiled proof: UpdateWorldData reads the
parent's world translate X/Y/Z at `[esi+0x8C]/[esi+0x90]/[esi+0x94]`
(`addss xmm2,[esi+0x8C]`, `addss xmm0,[esi+0x90]`, `addss xmm1,[esi+0x94]`) and the
parent's world scale at `[esi+0x98]`.

## Entropia 9.3.5 — measured THIS RUN from Entropia bytes (G7 closure)

Bounded probe (one additional vtable slot, no transform-chain traversal):

- **slot 27 = 0x007E4820 = UpdateWorldData** (`03_EVIDENCE/ENTROPIA_SLOT_NEIGHBORS_DISASM.txt`):
  `mov eax,[this+0x24]` (parent); if parent: `lea ecx,[this+0x38]` (m_kLocal),
  `lea ecx,[parent+0x6C]` (parent m_kWorld), transform product via helper; else
  `lea esi,[this+0x38]`; then `lea edi,[this+0x6C]` (m_kWorld) and
  `mov ecx,0xD; rep movsd` — 13 dwords = 52 bytes copied into **m_kWorld at +0x6C**.
  This is instruction-for-instruction near-identical to the GB112 compiled
  UpdateWorldData (same +0x24/+0x38/+0x6C/+0xB0 offsets).
- **slot 16 = 0x007B4650 = transform applier** anchors the NiTransform INTERNAL layout
  in Entropia: it operates on m_kLocal@+0x38 treating +0x5C (=+0x38+0x24) as a
  NiPoint3 translate and +0x68 (=+0x38+0x30) as the scale float — i.e. rotate@+0x00,
  translate@+0x24, scale@+0x30, matching both oracles' NiTransform byte-for-byte.

**ENTROPIA ANSWER: +0x90 lies INSIDE m_kWorld, at m_kWorld+0x24 =
`m_kWorld.m_Translate.x` — the WORLD TRANSLATE X component.** (m_kLocal@+0x38..+0x67,
m_kWorld@+0x6C..+0x9F; world translate X/Y/Z at +0x90/+0x94/+0x98; world scale +0x9C.)

Honest boundary: Entropia's own m_kLocal/m_kWorld base offsets (+0x38/+0x6C) are
PROVEN from Entropia bytes; the NiTransform internal order (translate at +0x24) is
additionally anchored by Entropia's slot-16 byte usage (+0x5C translate, +0x68 scale),
so the +0x90 attribution does not depend on oracle transfer — the oracles only
corroborate. The Entropia NiNode data TAIL still differs from both oracles (children
array at +0xCC/+0xD4 vs GB112 +0xB8/+0xC0, i.e. +0x14 extra bytes after
m_spCollisionObject@+0xB0), which is consistent with its later engine generation and
does not affect the +0x90 answer (which sits inside the NiAVObject transform block).

## Summary table

| Version | m_kLocal range | m_kWorld range | +0x90 meaning |
|---|---|---|---|
| GB 1.1.2 | +0x38..+0x67 | +0x6C..+0x9F | **m_kWorld.m_Translate.x (world translate X)** |
| GB 1.2.2.6 | +0x34..+0x67 | +0x68..+0x9B | **m_kWorld.m_Translate.y (world translate Y)** |
| Entropia 9.3.5 | +0x38..+0x67 (measured) | +0x6C..+0x9F (measured) | **m_kWorld.m_Translate.x (world translate X) — measured this run from slot 27 + slot 16 bytes** |

The published (INPUT-only) SceneFeeder observation — the returned object's +0x90 feeds
the caller's position output — is CONSISTENT with a world-translate-X read, but this
run does NOT extend that downstream observation into any model-bridge claim; the +0x90
result here is a structural fact about the NiAVObject layout only.
