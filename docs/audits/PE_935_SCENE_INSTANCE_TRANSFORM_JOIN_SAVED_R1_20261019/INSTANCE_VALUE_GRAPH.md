# INSTANCE_VALUE_GRAPH — PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019

MODEL_RESOURCE -> INSTANCE_ROOT -> TRANSFORM_SOURCE -> WORLD_TRANSFORM path status:

| edge | finding | status |
|---|---|---|
| Owner class identity | MovableObject-derived (base vtable 0xA91E4C per raw hex 0085B1C2; derived vtable 0xA7DCB0 per ctor 00528EA2; decompiler label 'MovableObject::vftable' in saved decomp F0085B1B0.c — label provenance: RTTI-derived decompiler symbol of a prior frozen run) | STRONGLY_SUPPORTED (class name), CONFIRMED (vtable values, field sets) |
| Owner ctor | 00528E50 (RET 0x10, 3 forwarded args; inits +0xA4..+0x124; zero-inits +0xD4..+0x124 floats; +0xE8 const-gated by 0085B0A0(this); base ctor 0085B1B0 (RET 0xC) inits +0x44..+0x70 incl. +0x50..+0x58 from globals 0xBA921C/20/24) | CONFIRMED |
| Owner object identity at runtime | WHICH instance of the class the studied receiver chain belongs to is runtime-unbound (no captured instance) | UNKNOWN |
| RECEIVER_POINTER_ORIGIN (00527AF9 ECX) | [owner+0xC], exactly one dereference, null-guarded; owner member slot zeroed at construction (0085B1B0: [this+3]=0) -> receiver attached post-construction by UNKNOWN writer | CONFIRMED (origin-as-field), UNKNOWN (writer) |
| Receiver dispatch family | 0085BFA0, 0085C130(x2), 0085CDE0, 0085C280, 0085C310, 0085C330 on [owner+0xC]; owner-methods 0085B0A0(x5)/0085B0B0(x3)/0085ACB0(x2)/007105F0(x2) on ESI; [owner+0x10]-methods 0040B070/00861220/00734210/00861240 (QC-F2-corrected split) | CONFIRMED (window P03) |
| Receiver class identity | polymorphic (vtable slot+4 = position-set-like, slot+0xC = position-trio-getter 0085B6A0 with type-gated semantics; type field +0x8 in {2..7}); whether [owner+0xC] is an instance of the SAME MovableObject family or another class is UNRESOLVED | UNKNOWN (class), CONFIRMED (method behavior) |
| FIELD_2C_WRITER | +0x2C lies inside embedded subobject [this+0x14] (ctor 007345C0 zero-inits slot +0x18 = owner +0x2C); bit0-flag or/and writes exist only on [owner+0xC0] (ctor 00528E50) — different object; the data-address writer is UNKNOWN | NOT_ESTABLISHED (bounded negatives in P01/P03/P04/P06-P11 windows) |
| TRANSFORM_SOURCE | 0085BFA0(this, &out13): out13 = 9 copies + 3 components + 1.0f-shaped output read via receiver slot+0x24 data address (frozen R2 P04); consumer 0085C130 blends owner-trio/O+C trios with S1; S1 sources CONFIRMED (entry arg2 float; [owner+0xE0]/[owner+0xE8] ratio) | PARTIAL (mechanism CONFIRMED, data origin UNKNOWN) |
| RESOURCE_INSTANCE_JOIN | no evidence binds the receiver or owner to a model resource instance in the admitted corpus | NOT_ESTABLISHED |
| WORLD_XYZ_RECOVERED | no coordinates recovered as historical placement | NO |
| HISTORICAL_PLACEMENT | not established | NOT_ESTABLISHED |
| CURSOR_SOURCE_MEDIUM | unknown | UNKNOWN |
