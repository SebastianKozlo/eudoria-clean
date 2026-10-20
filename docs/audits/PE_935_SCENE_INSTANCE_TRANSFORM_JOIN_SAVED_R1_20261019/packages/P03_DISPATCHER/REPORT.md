# REPORT.md — P03_DISPATCHER (window [005287E0,00528BB9))

AUTHOR: PE-MASTER_DIRECT_ANALYST_FALLBACK (two empty worker sessions; RUN_STARTED.json was the only disk output of attempt 1, verified; attempt 2 also empty). Evidence: P03_EXTRACT 277 rows, admission Ac782f044c9e3. Zero new admissions by this package.

## Findings
1. OwnerFn@00528810 (this, f_arg1, f_arg2) is the transform-thread dispatcher: ALL thread calls dispatch on [this+0xC] — the SAME receiver member that P01's caller 00527AA0 uses. Structural profile match with 00527AA0's owner (+0xC, +0x10, +0xE0/E4/E8) => STRONGLY_SUPPORTED same class; name UNKNOWN.
2. S1 for CALL 0085C130@00528A18 = entry arg2 float. S1 for the second CALL@00528AC2 = [ESI+0xE0]/[ESI+0xE8] after accumulating entry arg1 into +0xE4 and +0xE0 (with a conditional override from +0xE8).
3. Owner stores the trio at [arg1_local+0x24..+0x2C] (written inside the 0085C130 path, mechanism CONDITIONAL on opaque 0096D7C0) into owner +0x110/+0x114/+0x118.
4. Owner trio +0xD4/+0xD8/+0xDC feeds 004B2A20 vector ops, interacts with 0085BFA0 out-buffer slots +0x24/+0x28/+0x2C, and is overwritten from a 12-byte global block (0x00BA921C/20/24) on one branch. Working labels only.
5. FIELD_2C_WRITER: NOT_OBSERVED_IN_WINDOW (bounded negative, denominator = 277 rows of this window).
6. ESP/FPU balanced on all paths (claims C11/C12). Callee-cleanup premises labeled.
7. CORRECTED_PER_QC_F2: In this window 7 calls dispatch on [owner+0xC] (0085BFA0, 0085C130×2, 0085CDE0, 0085C330, 0085C310, 0085C280) and 12 on the owner ESI (0085B0A0×5, 0085B0B0×3, 0085ACB0×2, 007105F0×2); the 0085B0A0..0085CDE0 cluster is a MIXED dispatch family; ctor/RTTI evidence NOT in this window.

## Remaining barrier (exact missing information)
Writer of [receiver+0x2C] and provenance of the slot+0x24 data-address (12-float source). Candidate next evidence: saved RTTI/ctor reports in catalog for the 0085B0A0..0085CDE0 receiver cluster; else admit receiver-method bodies (e.g., 0085C280/0085CDE0) or ctor candidates. The owner identity (class name) likewise needs saved RTTI or ctor evidence.

