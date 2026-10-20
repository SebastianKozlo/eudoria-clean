# FLOW.md — 00528810 OwnerFn (this, f1, f2) RET 8

- guards: [this+0xC]!=0, [this+0x10]!=0 else exit; state checks via 0085B0A0/0085B0B0 (owner methods), 0085ACB0 vs 007105F0 compare.
- CALL 0085BFA0([this+0xC], &buf13@[ESP+0x18]).
- copy this{+0xD4,+0xD8,+0xDC} -> locals; 004B2A20 vector math; branch A: buf slots{+0x24,+0x28,+0x2C} -= this-trio; this-trio := globals[0x00BA921C..24]; branch B: extended math (0041C740, 0043AE80, 004B2A20), then trio arithmetic both directions.
- CALL 0085CDE0([this+0xC], &trio, 0).
- CALL 0085C130([this+0xC], &local, S1=f2); owner{+0x110..+0x118} := [local+0x24..+0x2C].
- else-path: e4 += f1; e0 += f1; conditional e0:=e8; CALL 0085C130([this+0xC], &local, S1_2=e0/e8); owner{+0x110..+0x118} := [local+0x24..+0x2C].
- tail: [this+0xC] methods 0085C330/0085C310/0085C280 or zero-trio; [this+0x10] methods 0040B070; owner{+0x11C..+0x124} trio; float getters -> owner{+0x104,+0x108,+0x10C}.
