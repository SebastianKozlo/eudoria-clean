# P04 (Front B1) — SceneFeeder position writer 0x005094C0: signature and callsite record provenance

RUN_ID: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | Package: P04 | Front: B
RUN_STARTED: 2026-10-18T21:49:38Z | HARD STOP: 2026-10-18T22:25:00Z
Admission: A0af4119f1ccf | Source pin: GHIDRA_H5_VTABLE2.txt SHA256 642CC29A…CC1D8DB (verified)
Contract: P04.json SHA256 A42CBDFB…232E9 (verified)

## 1. Question

B1: the actual source of the stored SceneFeeder position. Writer 0x005094C0 signature (args, thiscall, fields written, dirty flag) and the argument/record provenance in its admitted callers 0x006A36F0, 0x0067B4F0, 0x0067C560, 0x0067C7C0. Does the record distinguish resource ID / instance ID / parent / position / rotation? Any attach/parent evidence qualifying the written node as instance root vs internal NIF node?

## 2. Writer signature (C1, CONFIRMED)

```
005094c0  MOV EAX,[ESP+4]        ; arg = ptr to 12-byte record
005094c4  MOV EDX,[EAX]
005094c6  MOV [ECX+0x34],EDX     ; SF+34 <- rec[0]
005094c9  MOV EDX,[EAX+4]
005094cc  MOV [ECX+0x38],EDX     ; SF+38 <- rec[4]
005094cf  MOV EAX,[EAX+8]
005094d2  MOV [ECX+0x3c],EAX     ; SF+3C <- rec[8]
005094d5  MOV byte [ECX+0x28],1  ; dirty
005094d9  RET 0x4                ; thiscall, callee-pops 1 DWORD arg
```

thiscall; receiver in ECX; exactly ONE stack arg = POINTER to a contiguous 3-DWORD record (deref at +0/+4/+8 — not three scalar args); writes SF+34/+38/+3C and sets byte SF+28:=1; no return value; no ID/parent/scale/rotation logic.

## 3. Per-callsite provenance table (C2–C5, CONFIRMED)

| Callsite | Caller (conv.) | Receiver (writer this) | Record base → offset → size | In-body producer? | Producer candidates (getters, un-admitted) | Dominance | ID/instance hints | Rotation write |
|---|---|---|---|---|---|---|---|---|
| 0x006A3727 | 0x006A36F0 (thiscall, RET 0x4, 1 arg) | [caller+0x18] (pre-existing field) | caller frame F → +0x3C → 12 B | NONE in-body | 85C280(out=&F+0xC, this=[caller+4]) alt-4x4-geometry; 85BFA0(out=&F+0x18, this=[caller+4]) tail at +0x24 | iff [caller+0x18]≠0; unconditional on path; dominates 96CD10/509510 | none in writer path | 509510(SF, &F+0 = **{0,0,0} constant**) |
| 0x0067B52E | 0x0067B4F0 (thiscall, RET 0x8, 2 args; arg1=EDI) | [caller+4] | caller frame F → +0x3C → 12 B | NONE in-body | 862850(this=arg1, out=&F+0xC) alt-geometry; 85BFA0(this=[caller+0], out=&F+0x18) tail at +0x24 | iff [caller+4]≠0; dominates distance tail + [caller+8] tail | [caller+0xC] → 004150F0 with f32(‖v‖·q[0x00A7AF80]) — AFTER writer, NOT in record | 509510(SF, **{0,0,0}**) |
| 0x0067C584 | 0x0067C560 (thiscall, RET 0x8, 2 args) | [caller+4] | caller frame F → +0x3C → 12 B | NONE in-body | **85BFA0 only** (this=[caller+0], out=&F+0x18) — discriminating witness; post-writer 862850 cannot produce this invocation's record | iff [caller+4]≠0; dominates zeros/509510 and the [caller+0xC]≠0 tail | [caller+0xC] guard + same 004150F0 pattern | 509510(SF, **{0,0,0}**) |
| 0x0067C8A8 | 0x0067C7C0 (SEH, frame 0xD8, window TRUNCATED at 0x0067C921) | [caller+4] **freshly created in-frame** via [0x00A75A38]→00401360→00485050→0048CBB0→005247C0 | **callee-returned pointer** = RET of 85C0C0(this=arg1→[caller+0], out=&P+8) → +0/+4/+8 → 12 B | none (callee return) | 85C0C0 (position getter) — internal arg1 field vs out-buffer unknown; 85C0F0 (rotation getter, same receiver/out) | iff [caller+4]≠0; dominates 509510/509190/arg2-lookup up to 72FCE0 test | arg2 → [arg2] → 43a550 → 72F580 → 72fce0 lookup + 0x130-record ctor 6C0D50 — AFTER writer | 509510(SF, **ret(85C0F0) = real data**) |

Frame arithmetic: R2 baseline ESP=F−4 (SUB ESP,0x4c + PUSH ESI); R3/R4 same with F−4 (R3's PUSH EDI occurs inside the guarded block making its baseline F−8); R5 P = entry ESP−0xE4 with SEH node at P+0xDC, args at P+0xE8/P+0xEC, locals at P+3/P+8/P+0x14. Full layouts in MEMORY_AND_IDENTITY.json.

Shared family pattern (R2/R3/R4): getter(out=&F+0x0C) → **509070(this=SF, arg=getter RET)** → 85BFA0(this=source, out=&F+0x18) → **5094C0(this=SF, arg=&F+0x3C = &F+0x18+0x24)** → 96CD10(this=&F+0x18, {0,0,0}) → 509510(this=SF, {0,0,0}). The record slot sits exactly at +0x24 into the 85BFA0 buffer (translation-row geometry of a 12-float buffer) and, in R2/R3, also at +0x30 into the 85C280/862850 buffer (translation-row geometry of a 16-float 4×4). Both geometries fit; R4 (only 85BFA0 precedes) is the discriminating witness (C7, PLAUSIBLE — extent unread).

## 4. Answers to the contract questions

1. **Record distinguishes resource ID / instance ID / parent / position / rotation?** NO (C6, STRONGLY_SUPPORTED). The record is a bare 12-byte transform-shaped triple. Rotation is a separate method (509510) with a separate argument. ID-shaped values exist in the callers ([caller+0xC]; R5's arg2 lookup) but flow through OTHER calls AFTER the writer and never enter the record. Premise preserved: three float-shaped DWORDs ≠ XYZ provenance.
2. **Attach/parent evidence qualifying root vs internal NIF node?** NONE in-window (C9, CONFIRMED negative). SF+30 is never written inside the admitted windows; no NiNode attach call identified; the candidate link-setter is 509070 (body un-admitted). Node role remains UNDETERMINED.
3. **Update mechanism vs data source?** R2/R3/R4 write rotation as constant zeros — update-mechanism shape, not historical restores (C8). R5 is a copy-initializer: fresh receiver, position AND rotation copied from source object arg1's paired getters (85C0C0/85C0F0). Per premise, none is promoted to a recovered data source.

## 5. Scoped result

**Producer identified up to the getter boundary.** The stored SF position = copy of a 12-byte triple whose bytes are produced by getter callees outside this admission: R2: 85C280 or 85BFA0 (ambiguous); R3: 862850 or 85BFA0 (ambiguous); R4: 85BFA0 only; R5: 85C0C0 return. Exact data-route gap = those getters' read semantics + extent (variants V1–V4 in CLAIMS C10). The record carries no identity channel; the identity-bearing edges observed (arg1 source object; R5's arg2 lookup + 0x130-record construction; 509070's getter-fed pointer) all lie in UN-ADMITTED bodies.

## 6. Counters (actual vs reserved)

Rows 291/291 (9+35+74+76+97); CALL sites 47/47 (0+6+11+11+19; 28 unique targets, 24 direct + 4 indirect); bodies 5/5 (R5 truncated at window boundary — epilogue un-admitted); candidates 4/4 (V1 85BFA0-tail / V2 4x4-row / V3 stale-frame / V4 85C0C0-return). No overrun; no unforeseen bodies inside windows; no semantic read outside admission.

## 7. Negative controls performed

- Rotation-constant claim falsification test: scanned all rows for any non-zero store into the 509510 argument buffer — only FLDZ (0.0f) stores found in R2/R3/R4; claim stands.
- Writer-signature falsification test: if the writer took three scalar args, R1 would show three [ESP+n] loads without EAX deref chain — the observed deref at +0/+4/+8 rejects that model.
- Stale-frame variant V3 not excluded: no in-body store to F+0x3C exists in R2/R3/R4 — recorded honestly as an open variant.

## 8. Premises preserved

All four contract premises preserved and enforced in claims (see CLAIMS.json premises_preserved). WORLD_XYZ_RECOVERED, HISTORICAL_PLACEMENT, CURSOR_SOURCE_MEDIUM unchanged (NO / NOT_ESTABLISHED / UNKNOWN per parent standing).

## 9. Files

See artifact_index.csv; HANDOFF.md carries the exact next-admission requests for the parent.
