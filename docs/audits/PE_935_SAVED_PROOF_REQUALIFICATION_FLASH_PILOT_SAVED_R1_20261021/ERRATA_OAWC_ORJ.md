# ADDITIVE ERRATA — OAWC-A01..A08 and ORJ-A01..A09 (published by PE_935_SAVED_PROOF_REQUALIFICATION_FLASH_PILOT_SAVED_R1_20261021)

This file is an ADDITIVE erratum record. It does not modify any frozen run, history, checker or sealed package.
Sources (pinned, read as prior postaudits, not as new instructions): the deep postaudit of
PE_935_OWNER_ATTACH_WRITER_CLOSURE_DEEP_POSTAUDIT_R2_20261021 (REPORT.md / FINDINGS.json) and the independent
postaudit of PE_935_OWNER_R_JOIN_DEEP_POSTAUDIT_R1_20261021 (REPORT.md / FINDINGS.json). No raw packet rows,
model answers, prompts, DB/config/env contents or secrets are reproduced here.

## OAWC-A01..A08 (old OWNER_ATTACH R2 remains UNSEALED_NONPASS)
- A01: 46 actual science attempts (not 41); five obligations (O_BULKCOPY_TRACE2, O_QC_CTOR1, O_QC_CTOR2, O_QC_BULKCOPY, O_QC_LIST) have 3 attempts at cap 2. No retrospective reservations, suppression or reclassification.
- A02: manual prompt/seq transcription and incomplete process-death chronology at resume; no new R2 resume; literal prompt files and exclusive reservation before process are the required method (implemented by this pilot).
- A03: store/LEA census 16+12 over 4941 rows is COMPLETE; semantic qualification is PARTIAL; five LEA windows (0052872F, 005288F1, 00528981, 005298D3, 00529D9A) remain NOT_OPENED_WINDOW_CAP.
- A04: RET 0x10 at 00529072 = 16B/4-DWORD cleanup footprint; the three PUSHes to the base call are not three formal ctor parameters; footprint vs formal arity/types separated (needs ABI/stack-map).
- A05: the reader ECX comes from the SECOND lookup (CALL 004123D0 at 0048EE2A via MOV ECX,EAX at 0048EE2F), not the first (which is TESTed); wrapper 004154F0/008544D0 signatures not proved by PUSHes alone.
- A06: the intrusive-linked-list label is not unique; a tree-with-parent-and-two-children countermodel fits the shown operations; exact topology/type UNVERIFIED; no library/class name.
- A07: stack provenance does not prove pointer inequality to the actual owner: STACK_ORIGIN_CONFIRMED / ACTUAL_OWNER_JOIN_NOT_ESTABLISHED / DIRECT_OWNER_WRITER_NOT_SUPPORTED_IN_SCOPE.
- A08: visible helper stores do not close opaque effects; H02_85ad60 also spans neighboring virtual wrapper 0085AD80; 00414130 remains a concrete unopened edge.

## ORJ-A01..A09 (OWNER_R_JOIN R1: PUBLISHED report retains these scientific corrections; old publication stays as history)
- A01: the QC004-F1/CA-1 distinct-slot correction is REJECTED; all three wrapper/gate LEAs address the SAME slot under ESP shift (wrapper RET 0x4 included); the visible 0085B840 wrapper is the statically supported B-source wrapper (with explicit 004123D0 ABI/prior and slot-preservation premises).
- A02: the no-writer negative exceeds candidate qualification; keep the 7-site census; two EBP-based exclusions are conditional on missing frame provenance; the seventh site (0085B652) NOT_OPENED_CAP.
- A03: different definitions of T_slot and U_getter do not establish unequal pointer values; VALUE_EQUALITY(T_slot,U_getter)=UNKNOWN; alias countermodel consistent.
- A04: retry history exceeded the single-retry policy (W003 x3; QC002 x4 sessions); disclosed NONCOMPLIANT; final parity PASS does not retroactively authorize extra dispatches.
- A05: a partially explored saved frontier is not a data barrier: LOCAL_WINDOW_CAP and SEARCH_INCOMPLETE_WITHIN_SAVED_CORPUS are separate from SOURCE_NOT_AVAILABLE.
- A06: getter balance is conditional (x+y=4; x=0,y=4 also aggregate-balanced); the QC002 entryESP-0xC arithmetic is an additive erratum; the 13-DWORD copy result stands.
- A07: QC coverage and session attribution were overstated or stale; per-obligation coverage and final session IDs (QC002 final = ses_ea1b88e69ffe(REDACTED)) are the correct records.
- A08: the ORJ R1 publication WAS performed and commit-manifest-verified (remote master dfda081b...); the launcher/human false negative is corrected to PUBLISHED_VERIFIED; no duplicate publication.
- A09: the input CLAIMS census is 11 claims (8 CONFIRMED + 1 STRONGLY_SUPPORTED + 2 UNVERIFIED), not 6+1+2; the 0x128-argument allocator identity is not established by the shown call/argument/use chain alone.

## Standing of this pilot relative to the errata
The flash pilot (this run) was designed AFTER these corrections; its workers and reviewer did NOT receive the correction
key. The pilot's independent convergence with the A04/A05/A06 directions and the reviewer's independent re-derivation of
the ORJ-A01 slot aliasing are recorded in the run's DERIVED_CLAIMS.json as observations of this run only; they do not
promote any superseded historical claim and do not replace the pending external postaudit of this pilot.

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE.
