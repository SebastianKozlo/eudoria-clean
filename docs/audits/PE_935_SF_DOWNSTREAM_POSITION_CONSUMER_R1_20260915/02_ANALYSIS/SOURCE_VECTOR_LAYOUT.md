# SOURCE_VECTOR_LAYOUT — PHASE B ANALYSIS
# RUN_ID: PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915 (see raw: 01_RAW/SOURCE_VECTOR_LAYOUT_RAW.txt)

## VERDICT: SOURCE_VECTOR_LAYOUT = CONFIRMED (Entropia-local, no oracle premise)

| Dimension | Status | Evidence (measured) |
|---|---|---|
| SOURCE_OBJECT_IDENTITY | CONFIRMED | SF+0x30 = refcounted 0x118-byte NiNode-family object (ctor 0x509330: operator new(0x118)+0x7B6000, refcount@[obj+4]); lookup via vtable slot17 = 0x007B5390 (recursive children-array scan [+0xCC]/count [+0xD4], ret 4). Vtable matrix 0x00A8CCF4 holds slot17@+0x44 and slot27@+0x6C together — the NiAVObject-family layout. |
| SOURCE_FIELD_IDENTITY | CONFIRMED | `add eax,0x90` at 0x50A06E lands on m_kWorld.m_Translate (block start +0x6C + 36 rotate bytes = +0x90). |
| SOURCE_VECTOR_LAYOUT | CONFIRMED | Contiguous 3x f32 translate at +0x90/+0x94/+0x98 inside a 13-dword (52-byte) world block (9 rotate + 3 translate + 1 scale at +0x9C). |
| m_kWorld vs m_kLocal | DISTINGUISHED (CONFIRMED) | m_kLocal block at +0x38 (translate +0x5C, anchor `lea edi,[esi+0x5c]` in 0x7B4650); m_kWorld block at +0x6C (translate +0x90). UpdateWorldData (0x7E4820, slot27) copies local->world (13-dword rep movsd into +0x6C) or composes with parent's world (0x6eb380(parent+0x6C, ...)). |

## NiAVObject-family structure (this build, measured)
+0x00 vtable; +0x04 refcount; +0x24 m_pkParent; +0x38 m_kLocal{rotate +0x38, translate +0x5C, scale +0x68};
+0x6C m_kWorld{rotate +0x6C, translate +0x90, scale +0x9C}; +0xB0 child link; +0xCC children array; +0xD4 children count; size >= 0x118 (NiNode subclass).

## X/Y/Z offsets
X = +0x90, Y = +0x94, Z = +0x98 (component ORDER proven; absolute axis LABELS follow the NiPoint3 convention of the
same structure — the transform preserves order identically, see OUTPUT_VALUE_RELATION.md).

## Oracle discipline
Gamebryo oracle (package B) was used ONLY as secondary cross-check; every promoted fact above is measured from
Entropia.exe bytes in this run (raw file). Package B pins (slot27=0x7E4820, slot16=0x7B4650, slot17=0x7B5390,
+0x90=m_kWorld translate) were RE-MEASURED and MATCH (no pin mismatch finding).

## H1 evaluation
H1 ("NiAVObject+0x90 begins a contiguous 3-component world-translation vector"): CONFIRMED. Falsifier (noncontiguous
or different semantics) did not materialize; the 13-dword block copy and the translate anchor at +0x5C/+0x90 exactly
match the contiguous layout.
