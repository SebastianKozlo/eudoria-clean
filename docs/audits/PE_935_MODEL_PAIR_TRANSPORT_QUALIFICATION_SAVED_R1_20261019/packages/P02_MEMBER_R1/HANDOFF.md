# HANDOFF P02_MEMBER_R1

Established:
- FUN_0040b070 = member-view getter return param+0x14 (decompiler-level CONFIRMED; program-identity UNVERIFIED: same-aggregate declaration only, stlp_std consistency noted).
- Registration semantics REJECTED at decompile level (counterevidence maintained).
- Getter is typeless; member at owner+0x14 type depends on owner class per callsite.
- PAIR_FRAME_TO_PROJECTED remains NOT_ESTABLISHED; 006C3640 copies 2 DWORD from callback result (P01).

Next edges for T3 (owning caller window [006C3F50,006C3FE0)):
1. Establish arg source: container arg4, range arg2/arg3 (element stride 0x20), callback arg5 from caller registers before CALL 006C3640.
2. Identify who reads the out slot arg1 after return: nearest real consumer.
3. Look for the {66h,A} frame pair and opaque 0043C700 usage relative to element construction.

Actuals: 1 body (decompile), 15 document lines, 0 instructions, 0 CALL sites; 2 variants (conservative).
Attribution: DIRECT_ANALYST_FALLBACK by PE-MASTER parent.