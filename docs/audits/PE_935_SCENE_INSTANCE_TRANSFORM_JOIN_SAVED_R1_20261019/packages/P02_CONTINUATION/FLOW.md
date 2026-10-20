# FLOW.md — 0085C130 (single-path window [0085C130,0085C280))

1. Prolog; ECX->ESI (receiver); CALL 0085BFA0(self, &OUT[13 dwords]).
2. C-O: OUT slots +0x24/+0x28/+0x2C (QC-F1-corrected, continuous trio) minus [ESI+0x54/0x58/0x5C].
3. L1 = O + S1*(C-O)  (S1 = arg2 float).
4. v-trio:=0; CALL 0096CD10(ECX=ESI+0x30, &v).
5. u-trio:=0; CALL 0096CD10(ECX=&OUT, &u).
6. w := u-v; L2 := v + S1*w.
7. CALL 0096D7C0(ECX=arg1, [&L2,&L1]); return EAX=arg1.

No branches in the admitted window. All callee bodies opaque (0096CD10, 0096D7C0, deeper 0085BFA0 internals per frozen evidence).

