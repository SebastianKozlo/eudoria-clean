# REPORT.md — PE_935_SF_ARG2_PROVENANCE_R1_20260914

Executor: pe-reconstruction · PE-MASTER loop `2ed038db-5d2e-4e7e-b679-2d29bf57501a`
(EU935-M1, 4h auto loop, Phase 2 science) · RUN_TYPE: STATIC_SEAM_PROBE
(Rosetta edge: SceneFeeder → named-object lookup) · MODE: STATIC-ONLY —
Entropia.exe was NEVER executed; all evidence is own byte reads + own capstone
disassembly of the pinned EXE (SHA256
`E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`, size 8015872,
re-measured fail-closed in every script).

## PRIMARY QUESTION (contract §C)

> WHO supplies FUN_0050A050's arg2 (the name argument of the SF slot-3
> primary-path virtual dispatch to the NiNode named-object lookup), WHAT VALUES
> does it take, and WHAT is its semantic role?

## THE FOUR STATUSES (independent)

| Status | Value | One-line evidence |
|---|---|---|
| ARG2_ABI | **CONFIRMED** | Full own decode: thiscall this=ECX, arg1=[esp+4] out float3 buffer, arg2=[esp+8]; eax def chain `mov eax,[esp+8]` @0x0050A050 (`8B 44 24 08`) → NULL-test `je 0x50A087` → `push eax` @0x0050A060 (`50`) as the slot-17 dispatch's single stack arg; **ret 8 (`C2 08 00`) measured at BOTH ret sites** (0x0050A084, 0x0050A0A7); B.5 extent 0x0050A050..0x0050A0AA (90 B) agrees with published; NC-1: 9/9 pins byte-exact, 0 PIN_MISMATCH. |
| ARG2_PROVENANCE | **UNVERIFIED** (measured-and-bounded) | E8 census: 0 direct callers (156,829 E8 bytes in .text, CAL-2 PASS); imm32 census: exactly 1 hit = the vtable slot-3 dword @0x00A7D464 (NC-4 MATCH, CAL-1 PASS) — the channel is exclusively virtual; virtual-call-site census: 218 candidates → 0 PROVEN SF receivers within the declared 2-level/48-byte bound, 5 REJECTED_NOT_SF (NC-2 PASS), 211 INSUFFICIENT_PROOF, 2 NOT_A_VTABLE_CALL (CAL-3 tracer calibration PASS); method-1 holder route: 25,905 holder-offset reads → 18 genuine slot-3 flows → 17 ABI-incompatible with the measured ABI, 1 ABI-compatible forwarding-thunk family (FUN_006FAB80, shared slot function of 5 vtable-extent-verified RTTI classes — the ArkAnimation family: `.?AVArkAnimationCyclic@@`, `.?AVArkAnimationCyclicLinear@@`, `.?AVArkAnimationCyclicSin@@`, `.?AVArkAnimationDerivatives@@`, `.?AVArkAnimationPredefined@@`; list read from the regenerated raw, corrected per the R1 amendment 2026-09-14) whose `[this+0x14]` receiver is a refcounted held object of UNPROVEN class within the bound. |
| ARG2_VALUE_CLASS | **UNVERIFIED** (zero values identified) | Zero verified call sites → zero arg2 producer chains → zero identified values; the only ABI-compatible candidate channel forwards an opaque parameter (`[esp+8]` of the thunk); NC-3 had no in-scope subjects (machinery calibrated on a known .rdata literal — tooling only). |
| ARG2_FINAL_SEMANTIC_ROLE | **UNVERIFIED** (hypotheses stay hypotheses) | No direct producer→semantic link; the standing B.2 fact constrains arg2's runtime syntactic class (`const char*` name consumed by the slot-17 named-object lookup — NOT re-derived; G6) but node name / bone / socket / marker / config key all remain HYPOTHESES; measured structural context only (the `.?AVArkAudioObjectInterface@@` vtable @0x00A7D42C — exactly 6 slots, RTTI-verified — is ADJACENT to the SF vtable in .rdata, separated by the "ArkSceneFeeder" string literal and the SF COL; adjacency is NOT sharing and NOT inheritance evidence; each SF slot function has EXACTLY ONE vtable membership, the SF vtable itself, per the whole-file imm32 census — the earlier "shared slots 11–15" reading was a vtable-boundary overrun artifact, RETRACTED per PE-MASTER adjudication; the ABI-compatible forwarding family is the ArkAnimation animation classes). |

The four statuses are independent: ABI CONFIRMED with provenance/value-class/
semantic-role UNVERIFIED is the honest measured outcome; the exhausted bounds
are recorded outcomes, not failures.

## CENSUS DENOMINATORS

- E8 census: .text 0x00401000..0x00A75000 (6,766,592 B); 156,829 E8 byte
  occurrences; 0 E8 + 0 E9 + 0 EB matches to 0x0050A050.
- imm32 census: whole file (8,015,872 B); exactly 1 LE-dword hit of 0x0050A050
  (VA 0x00A7D464, section .rdata — the SF vtable slot-3 entry).
- Virtual call-site census: 218 candidates (P1=1, P1J=0, P2=0, P3=217 after the
  follow-check); receiver-proof outcomes: 0 PROVEN / 5 REJECTED_NOT_SF /
  211 INSUFFICIENT_PROOF / 2 NOT_A_VTABLE_CALL; declared bound: 2 levels,
  48-byte backward windows, multi-start with cross-chain agreement.
- Method-1 holder route: reads enumerated by offset — +0x04: 12,535; +0x0C:
  5,957; +0x10: 2,615; +0x14: 2,841; +0x18: 1,761; +0xC0: 196; 18 genuine
  slot-3 flows; ABI disposition: 17 incompatible, 1 compatible.

## DISTINCT ARG2 VALUES FOUND

**None.** Zero verified call sites; zero producer chains completed; no string
literal, buffer or field value was identified as an arg2 producer. (The only
.rdata literal recorded verbatim this run — `Entropia` @0x00A7957C — is an
NC-3 tooling calibration, NOT arg2 evidence.)

## FALSIFIER OBSERVED

The census machinery was falsified twice in-run and both defects were caught by
in-run cross-checks and fixed with re-runs (the corrected census is the
deliverable):
1. The E8/E9-target lattice MIS-ATTRIBUTES the enclosing function of
   vtable-only functions (FUN_006FAB80 attributed to 0x006FAB20) — caught by the
   closest-candidate cross-check; fixed with B.5 padding-derived function
   starts.
2. The method-1 flow accumulator lacked register-clobber tracking and produced
   one false holder-flow positive (0x007B93D3 region: ecx re-assigned from
   [esi+0x160] before the vtable load) — caught by ABI-disposition decode;
   fixed with clobber-aware accumulation; re-run removed it.
Additionally the surprising P1 denominator (exactly ONE `call [reg+0xC]`
byte-pattern in .text) was independently verified against the analogous
slot-17 form (`FF 52 44` = 0 occurrences) — the compiler's vcall idiom is the
2-step `mov f,[vt+slot]; call f` form; the P1 result is a property of the data,
not an enumeration defect. The W1 first-terminal boundary logic initially
reported a false extent DISAGREES; the iterative terminal+padding rule (the
correct B.5 application) was applied and the extent AGREES with the published
pin.

## FINDINGS

- **P0:** none.
- **P1 (measured, structural):** (1) FUN_0050A050 is vtable-addressed ONLY —
  the slot-3 channel is exclusively virtual; (2) RETRACTED and corrected by
  PE-MASTER adjudication (R1 amendment, 2026-09-14): the original item claimed
  the SF slot functions are shared with `.?AVArkAudioObjectInterface@@` vtable
  slots 11–15 — a VTABLE-BOUNDARY OVERRUN artifact of the pre-fix fixed-16-slot
  RTTI enumeration; the corrected structural statement: each SF slot function
  has EXACTLY ONE vtable membership (the SF vtable itself — the run's imm32
  census bounds FUN_0050A050 to exactly one whole-file address occurrence, the
  vtable dword 0x00A7D464), and the `.?AVArkAudioObjectInterface@@` vtable
  (0x00A7D42C, exactly 6 slots, RTTI-verified) is ADJACENT to the SF vtable in
  .rdata, separated by the "ArkSceneFeeder" string literal and the SF COL —
  adjacency is NOT sharing and NOT inheritance evidence (any
  SceneFeederObject↔ArkAudioObjectInterface inheritance relationship is
  UNVERIFIED); (3) this binary's RTTI COLs are POINTER-based (VA fields,
  signature 0), not MSVC RVA-based.
- **P2 (method):** (1) the 2-step vcall idiom dominates; (2) vtable-only
  functions need B.5 starts, not the E8/E9 lattice; (3) the ABI dimension
  (stack-arg count + this-register) discriminates channel membership — 17/18
  holder leads ABI-excluded; (4) the flow accumulator needs clobber tracking.
- **P3 (candidates, NOT performed — out of scope):** (1) upstream census of the
  ArkAnimation-family slot channels (the FUN_006FAB80 thunk's virtual callers)
  for the ultimate arg2 producers; (2) FUN_0044D590 container-class
  identification (its +0x10 store receives the FUN_005247C0 SF-factory result,
  measured) and linkage/disproof against the ArkAnimation family's +0x14
  holder; (3) the SLOT_CENSUS "shared-tail polymorphism" NOT_CHECKED note is
  now CHECKED — the tail is the published fallback, one ABI, no polymorphism.

## SCOPE / G6 DISCLOSURE

No downstream consumer analysis (the +0x90 → 0x437F70 → 0x82B5A0 flow appears
only as W1-decoded bytes of FUN_0050A050 itself; 0x437F70/0x82B5A0 were NOT
analyzed); no model/NIF corpus work; slot-17 NOT re-identified (only the
permitted value check dword [0x00A8CCF4+0x44]==0x007B5390 — MATCH). Bounded
receiver-class discrimination reads within the declared bound (SF ctor entry,
NiNode slot-3 entry value, container ctor region) are disclosed as
census-necessary value/entry reads. TRANSFORM_TO_MODEL / MODEL_BRIDGE: NOT_DEMONSTRATED.

## IMMUTABILITY / GIT

ZERO git mutations at any point. G7 file side: FIRSTCALL package 7/7 pinned
hashes MATCH, 3 empty dirs empty, no extra files; LINK30 census CSV hash MATCH
(SF30_WRITER_RAW.txt present/untouched); experiments/ untouched. G7 git side:
end-of-run HEAD == BASE_SHA `f239eb85cd0f56ae10cee52d57833a49f225965c`, zero
staged paths, no new commits, untracked set exactly the three expected
directories.

## OUTCOME

**PROPOSAL_ACCEPTED** — FRESH_QC_VERDICT: **QC_PASS_WITH_FINDINGS**
(06_REPORT/QC_AUDIT.md; the QC independently re-derived the full ABI byte chain,
all census denominators, the FUN_006FAB80 forwarding decode, and re-executed
7/7 scripts 9/9 deterministic). PE_MASTER_VERDICT: **MASTER_ACCEPTED**
(advisory; 06_REPORT/PE_MASTER_REVIEW.md persisted; the two correction batches
recorded in 00_CONTROL/AMEND_LOG_R1.md). PERSISTENCE_STATUS: **EXECUTED**
(this commit set — the pe-master-auditor G15 persistence step: package commit +
AUDIT_ENTRYPOINT row + push). The NOT_APPLICABLE gates stand where the subject
set is empty (honest list, no waived checks). No HARD_STOP triggered.
