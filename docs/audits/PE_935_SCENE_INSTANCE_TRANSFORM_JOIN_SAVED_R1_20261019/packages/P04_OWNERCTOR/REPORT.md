# REPORT.md — P04_OWNERCTOR (saved ctor text 00528E50)

AUTHOR: PE-MASTER_DIRECT_ANALYST_FALLBACK (two empty worker sessions, only RUN_STARTED.json from attempt 1; systemic pattern). Evidence: P04_EXTRACT (142 lines, admission Ab3209cc88389, source file F00528E50_CTOR_MOBJ.txt, own-decode provenance of a prior frozen run). Zero new admissions.

## Findings
1. 00528E50 is the DERIVED ctor of the owner class (vtable 0xA7DCB0): it initializes +0xA4..+0x124 — exactly the field families P01 (00527AA0) and P03 (00528810) write/read. OWNER_IDENTITY of the thread = this class: STRONGLY_SUPPORTED structural, name UNKNOWN.
2. Thread-relevant members +0xC (receiver) and +0x10 (secondary) are NOT initialized here — the base ctor CALL 0085B1B0 (0085B cluster) is the candidate producer. F0085B1B0.c is in the catalog (next admission).
3. A factory chain (00401360->00485050->0048CBB0->EDI null-checked; 0085B120(this)+00414130 as args) creates an object stored at [this+0xC0]; its +0x2C BIT0 flag is set/cleared (`or/and [ecx+0x2c],1/~1`) gated by 0085B750(this) AL. This is a bit-flag on a DIFFERENT object — NOT the receiver +0x2C data-address slot. FIELD_2C_WRITER(receiver): NOT_OBSERVED_IN_FILE (bounded negative, 142-line denominator).
4. [this+0xC0] receives setup methods with owner-subobject pointers (+0x44, +0x5C, +0x50) and a zero float pair; FLD [this+0x64] -> [this+0xB4]. Working labels only.

## Answers
- OWNER_IDENTITY: ctor 00528E50 of vtable-0xA7DCB0 class = the P01/P03 owner class (STRONGLY_SUPPORTED structural; name UNKNOWN).
- STORED_OBJECT_CLASS: [owner+0xC0] = factory product of 005247C0 chain (UNKNOWN class); NOT identified with [owner+0xC] receiver.
- FIELD_2C_WRITER (receiver): NOT_ESTABLISHED from this file; next candidate: base ctor 0085B1B0.

## Remaining barrier
Producer of [owner+0xC] and [owner+0x10], and writer of [receiver+0x2C] (data-address holder). Candidate evidence in catalog: F0085B1B0.c (base ctor), T1_REGION_0085B100_0085B900.txt, caller_of_ctor_region_00528C00.txt.
