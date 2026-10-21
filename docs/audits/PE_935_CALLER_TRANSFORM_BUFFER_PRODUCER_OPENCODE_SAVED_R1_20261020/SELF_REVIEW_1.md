# SELF REVIEW 1 - pointer flow / ABI / aliasing / countermodels

Finding-free items verified; findings listed with disposition.

1. ESP normalization re-derived end-to-end: prolog deltas; F after cookie push; PUSH ECX@85A1F8 consumed by 7C3BB0 RET 0x4 (literal); PUSH 0x20 and PUSH ECX pairs each closed by literal ADD ESP,4; loop 5 pushes closed by 857830 RET 0x14 (BOTH exits admitted). S=F holds on both control paths. VERIFIED.
2. Arg-slot overwrite subtlety re-checked: FSTP [ESP]@85A3C3 targets the 4th-push slot ([F-0x10]) because ESP=F-0x10 after 4 pushes; the arg2 of 857830 is the const float, NOT the pointer F+0x5C pushed at 85A39E. This reconciles the callee FLD [ESP+0x30] (arg2 as float). VERIFIED.
3. [F+0x94] boundary: buffer is [F+0x60..F+0x94) exclusive; FSTP [EDX] with EDX=F+0x94 writes OUTSIDE. One-past-end confirmed. VERIFIED.
4. REP MOVSD: DF=0 premise (no STD in admitted range; ABI convention); count 9; source/dest ranges re-derived. VERIFIED with premise label.
5. FINDING (corrected during run): coordinator initially read [F+0x38] as never-written; worker W002 refuted; re-verification confirmed write at 85A2AA (ESP=F-4). Correction recorded (NC2). No remaining instance of the misreading in artifacts (SOURCE_SLOT_MAP/FIRST drafts corrected before any file write).
6. FINDING (worker error logged): W001 claimed f1==f2==raw constant - refuted by the two distinct thunked helper calls; only store structure accepted; values remain H1(c)/H2(c) UNKNOWN. Recorded in QC_FINDINGS.
7. x87 residual: 7C3BB0 literal trace leaves one stack value unpopped; net balance depends on opaque import behavior. Recorded as limitation; not load-bearing for stored values.
8. Countermodels hunted: (a) loop ESI alias into buffer - no in-window premise; positive exclusion blocked by opaque import (NOT_ESTABLISHED, not REJECTED); (b) result2 alias into buffer - opaque, kept UNKNOWN_MODREF; (c) S!=F via unbalanced pushes - refuted by literal balance; (d) DF=1 - no STD row in admitted range, premise labeled; (e) arg-mapping shift inside 5-push window - independently re-counted by QC (CONFIRMED).
9. Opaque-callee discipline: no claim asserts "callee cannot write without receiving the address" - 413440/95D3C4/95D3BE/result2 chains all carried as UNKNOWN_MODREF with the bound-negative scoped.
Conclusion: no unresolved load-bearing countermodel within proven premises; limitations explicit.
