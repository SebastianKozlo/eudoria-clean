# RECEIVER_IDENTITY_MATRIX

| question | answer | status | evidence |
|---|---|---|---|
| OWNER_IDENTITY (00527AA0 / 00528810 owner) | MovableObject-derived class; base vtable 0xA91E4C, derived vtable 0xA7DCB0; ctor 00528E50; base ctor 0085B1B0 RET 0xC | STRONGLY_SUPPORTED (name from decompiler RTTI label), CONFIRMED (vtable/field facts) | P04/P05/P09 |
| RECEIVER_POINTER_ORIGIN | [owner+0xC], one dereference, null-guarded; zeroed at construction; attach writer UNKNOWN | CONFIRMED / UNKNOWN | P01, P05/P09 |
| STORED_OBJECT_CLASS ([owner+0xC0]) | factory product of 00401360->00485050->0048CBB0(null-check)->EDI; 005247C0(EDI, 0085B120(this) result, 00414130 result) -> [owner+0xC0]; its +0x2C bit0 flag gated by 0085B750(this) type predicate {2..7} | CONFIRMED (chain), UNKNOWN (class) | P04 |
| Receiver class (of 0085BFA0) | polymorphic; slot+4 set-position-like; slot+0xC = 0085B6A0 type-gated position-trio getter; type field +0x8; whether same MovableObject family UNKNOWN | CONFIRMED (methods), UNKNOWN (class) | P07/P08, P03 |
| FIELD_2C_WRITER | not the ctors (007345C0 zero-inits; 0085B1B0 visible portion no store; bit0 writes only on [owner+0xC0]) | NOT_ESTABLISHED; bounded negatives with denominators | P04/P05/P09/P10 |
| SLOT24_TARGET | 12-float data-address mechanism (frozen R2); writer UNKNOWN | PARTIAL | frozen R2 + this run |
| SLOT28_TARGET | 3-float mechanism (frozen R2); not re-qualified in this run | UNVERIFIED (inherited frozen status) | frozen R2 |
| FIELD_PRESERVATION_AT_CALL | caller-frame path-exact; cross-opaque-callee preservation premises only | PARTIAL | P01/P02 |
