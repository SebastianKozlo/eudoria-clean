# FLOW - frontier thread

E-F1: receiver -> [this+0x2C] @0085BFA6 (pointer level 1).
E-F2: [[this+0x2C]] vtable slot+0x24 -> callee returns ptr to 12 floats @0085BFB5-0085C00D.
E-F3: 12 floats -> (0096CB20, 0096CF80) -> 9-dword rotation block + 3-dword translation + FLD1 scale -> out[0..0x34) @0085C058-0085C0AB. CONFIRMED (helpers unopened).
E-F4: [[this+0x2C]] vtable slot+0x28 -> 3 floats position -> out (0085C0C0). CONFIRMED.
E-F5: callers: rotation-only rebuild (0085C0F0); translation minus receiver+0x54/+0x58 (0085C130 partial).
PRIMARY THREAD JOIN: NONE in admitted windows (P04-K09).
