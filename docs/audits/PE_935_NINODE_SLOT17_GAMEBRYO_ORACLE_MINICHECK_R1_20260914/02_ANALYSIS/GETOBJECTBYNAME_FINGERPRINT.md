# GETOBJECTBYNAME_FINGERPRINT — GB 1.1.2 vs GB 1.2.2.6 (Question B)

Compact behavioral fingerprint from the pinned oracles. Sources: 1.2.2.6 source
(`NiAVObject.cpp` L423-432, `NiNode.cpp` L749-767 — locators in
`01_RAW/GB12_SOURCE_LOCATORS.md`); 1.1.2 has no NiMain sources, so its body is taken
from the COMPILED NiMain.lib (disassembly evidence
`03_EVIDENCE/GB112_NIAVOBJECT_GETOBJECTBYNAME_DISASM.txt` and
`03_EVIDENCE/GB112_NINODE_GETOBJECTBYNAME_DISASM.txt`). For 1.2.2.6 the COMPILED
.obj disassemblies were also taken
(`03_EVIDENCE/GB12_NIAVOBJECT_GETOBJECTBYNAME_DISASM.txt`,
`03_EVIDENCE/GB12_NINODE_GETOBJECTBYNAME_DISASM.txt`) so that every claim below is
anchored in compiled code, not only in source text.

## NiAVObject::GetObjectByName — base (leaf) behavior

Derived pseudocode (identical in both versions):

```
NiAVObject* NiAVObject::GetObjectByName(const char* pcName)   // thiscall, RET 4
{
    if (pcName == NULL) return NULL;
    if (GetName() == NULL) return NULL;        // GetName() reads m_pcName
    if (strcmp(pcName, GetName()) == 0)       // inlined byte-pair strcmp ladder in both builds
        return this;
    return NULL;
}
```

Fingerprint elements:
1. NULL-name guard (argument) and NULL-object-name guard (this->name) -> NULL.
2. Fixed-string comparison via strcmp — both compiled builds inline it as a
   2-bytes-per-iteration compare ladder (see evidence files, offsets 0x12-0x2C in both).
3. Returns `this` on match; NULL otherwise (two epilogues in the 1.2.2.6 compiled body:
   `mov eax, esi; pop esi; ret 4` and `xor eax, eax; pop esi; ret 4`).
4. thiscall, ONE 4-byte stack argument, callee cleanup (`ret 4`) — both versions.
5. **Version delta (data): the name member offset differs.**
   - 1.1.2 compiled base reads the name at `[this+0x0C]` (evidence line
     `mov esi, dword ptr [edi + 0xc]`).
   - 1.2.2.6 compiled base reads it at `[this+0x08]` (evidence line
     `mov eax, dword ptr [esi + 8]`).
   Reason: 1.1.2 NiObject carries `m_pkGroup` at +0x08 (before `m_pcName` at +0x0C);
   1.2.2.6 removed the group member from NiObject (see `NiObject.cpp` L53-62), shifting
   `m_pcName` to +0x08. This is a DATA-LAYOUT delta, not a behavioral one.

## NiNode::GetObjectByName — recursive container behavior

Derived pseudocode (identical control flow in both versions' compiled code):

```
NiAVObject* NiNode::GetObjectByName(const char* pcName)       // thiscall, RET 4
{
    NiAVObject* obj = NiAVObject::GetObjectByName(pcName);     // direct call to base impl FIRST
    if (obj) return obj;
    for (unsigned i = 0; i < m_kChildren.GetSize(); i++) {     // count member
        NiAVObject* child = GetAt(i);                          // array member, 4-byte stride
        if (child) {
            obj = child->GetObjectByName(pcName);             // VIRTUAL recursive call
            if (obj) return obj;                               //   through the GetObjectByName SLOT
        }                                                       //   (same slot in both versions)
    }
    return NULL;
}
```

Fingerprint elements:
1. **Base-check-first**: a direct (non-virtual) call to `NiAVObject::GetObjectByName`
   with the same argument — the self-name test precedes the child walk.
2. **Child iteration**: count member read per loop; array member dereferenced with
   4-byte stride (pointer elements); NULL array elements skipped (`test ecx,ecx; je`).
3. **Recursive virtual dispatch through the GetObjectByName slot itself**:
   1.1.2 compiled: `mov edx,[ecx]; call [edx+0x40]` (slot 16);
   1.2.2.6 compiled: `mov eax,[ecx]; call [eax+0x48]` (slot 18).
4. First-match return; NULL when the loop exhausts; `ret 4`; EAX carries the
   pointer-or-NULL result; caller immediately tests it.
5. Prologue shape (identical in both compiled versions, and in Entropia):
   `push ebx; mov ebx,[esp+8]; push edi; push ebx; mov edi,ecx; call <base impl>; ...`

## Exact 1.1.2 vs 1.2.2.6 differences (measured)

| Property | GB 1.1.2 | GB 1.2.2.6 |
|---|---|---|
| GetObjectByName slot (NiAVObject & NiNode) | 16 (+0x40) | 18 (+0x48) |
| Recursive dispatch in NiNode | `call [edx+0x40]` | `call [eax+0x48]` |
| Children array member offset (NiNode) | +0xB8 | +0xB4 |
| Children count member offset (NiNode) | +0xC0 | +0xBC |
| Name member offset (NiObjectNET) | +0x0C | +0x08 |
| Zero-count branch form | `jbe` | `je` |
| Loop increment | `inc esi` | `inc esi` |
| strcmp style | inlined 2-byte ladder | inlined 2-byte ladder (same shape) |
| Everything else (guards, order, returns, ABI) | identical | identical |

Both differences are consequences of the 1.2.2.6 NiObject group-pointer removal
(+2 slot shift; -4 data shift), not semantic changes: **the behavioral fingerprint of
GetObjectByName is IDENTICAL across the two oracle versions.**

## Entropia compiled-shape note (for the comparison; measured this run)

The Entropia slot-17 function 0x007B5390 (decoded in
ENTROPIA_SLOT17_FINGERPRINT.md) is nearly instruction-identical to the era VC71
compiled `NiNode::GetObjectByName` above: identical prologue
(`push ebx; mov ebx,[esp+8]; push edi; push ebx; mov edi,ecx; call <base>; test; jne`),
identical guarded child-loop idiom (reload count / `cmp` / `ja` re-entry), same
base-call-first ordering, same inlined byte-pair strcmp ladder inside the self-check
callee, `ret 4`. Deltas are purely positional/structural: children array/size at
+0xCC/+0xD4 (GB112: +0xB8/+0xC0), recursion slot +0x44 (GB112: +0x40 — one extra
dtor-related slot in Entropia's vtable prefix, measured: slot 0 = vector deleting
dtor, slot 1 = scalar deleting dtor thunk, slot 2 = GetRTTI), and `add esi,1` vs
`inc esi` (compiler variant).
