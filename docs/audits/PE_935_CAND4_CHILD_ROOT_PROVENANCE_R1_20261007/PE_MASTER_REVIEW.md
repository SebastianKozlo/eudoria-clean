# PE_MASTER_REVIEW — PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007
REVIEWED BY: PE-MASTER (supervisory controller; independent audit over executor + fresh internal QC + own byte re-pins)
DATE: 2026-10-07
BASE_SHA = d65fa12e5bae4e9aab291c3cc7815b1822e41cff
RUN_CLASS = BOUNDED_STATIC_RE; RUN_TYPE = CAND4_CHILD_MODEL_ROOT_PROVENANCE

## VERDICT
RUN_VERDICT = MASTER_ACCEPTED (advisory)
AUTHORITY_STATUS = ADVISORY_PRE_QUALIFICATION (PROVISIONAL_UNTIL_QUALIFIED; Q1 absent)
CANONICAL_GATE_EFFECT = NONE
SCIENCE OUTCOME = CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND (honest partial; contract question advanced but not closed)
PROCESS = NEW_INTERPROCEDURAL_EDGES 24 vs MAX 8 — EXCEEDED (ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL, honestly self-disclosed by the executor with a full census; RETROACTIVE_PRIOR_AUTHORIZATION = NO; NO present-exception adjudication exists for this breach; the FAIL stands as historical record; publication proceeds per contract §12 honest-state rule — publication != acceptance)

## INDEPENDENTLY VERIFIED BY PE-MASTER (own byte reads from pinned EXE)
- Getter FUN_006C66D0 @0x006C66D0 = `8B 41 68 C3` (mov eax,[ecx+0x68]; ret) — EXACT.
- Producer chain: ctor NULL-init `89 5E 68` @0x006C8FD3; writer [manager+0x68]=[instance+4] `89 7E 68` @0x006C67E2; read `8B 78 04` @0x006C67BE; store [manager+0x6C] `89 46 6C` @0x006C7008; join window `8B F8` @0x0050A3B7 / `57` @0x0050A3F6 — ALL MATCH.
- RTTI: COL 0x00AA6C58 -> `.?AVArkModelManagerMain@@`; COL 0x00AA6CD8 -> `.?AVArkModelManager@@` — MATCH.
- Census: 69 rows (24 ANALYZED_NEW + 7 RAW_VISIBLE_ONLY + 11 REPIN_PRIOR_SCOPE + 27 OUT_OF_ANALYZED_EXTENT); RP-08..11 (4 prior-scope intervening callsites) present post-F-QC-E.
- Manifest 27 rows: PE-MASTER full re-hash (path repo-relative, case-insensitive) zero mismatch.
- Repaired record files (F-QC-A..E): hashes verified vs executor claims; UTF-8 38/38.

## INTERNAL QC (fresh context, PE_935_CAND4_CHILD_ROOT_PROVENANCE_INTERNAL_QC_R2_20261007, QC_PASS_WITH_FINDINGS 5xP3 zero P1/P2)
Independent engine (own PE mapper, own x86 decoder, zero executor tooling): getter decode ModRM-verified (mov eax,[ecx+0x68], NOT [esi]); RTTI 3 walks (incl. .?AVArkModelResourceInstanceRef@@); 56/56 pins + 23/23 rel32 MATCH; producer chain 20 pins MATCH; join window clean caller-side (only EDI write = mov edi,eax @0x0050A3B7); 6 extents walked 100% (26 CALL == 26 ledger in-body rows bijection); EDGE ACCOUNTING: ACCOUNTED_EDGE_COUNT 24 == INDEPENDENT_RECONSTRUCTED_EDGE_COUNT 24 (exceedance exactly 24, not more; zero semantic analysis hidden under RAW_VISIBLE; census classes complete); budgets bodies 6/6, writers 2/6 + 3 explicit gaps, hops 2/3, candidates 3/3; PREREGISTRATION physically pre-dated (mtime 11:02:49Z < first decode 11:12:10Z); CTRL_1..4 replicated PASSx4 on QC's own checker (clean PASS -> mutated FAIL, correct predicates; real input POLICY_ONLY where applicable); algebra §8 literal (no promotion above weakest edge; no active SCIENCE_PASS anywhere); prior packages 49/49 + 27/27 blob-identity; manifest 27/27 .NET re-hash; governance verbatim consistent. Findings F-QC-A..E (5x P3 records-precision) -> ALL CORRECTED-AND-FIXED by executor records-repair (12 paths incl. 2 consequential consistency updates; census 65->69 rows; revalidated 45/45 per-finding tests; manifest regenerated LAST). Executor observation re RP-01/NEIGH-07/RV-04..07 citation depth — pre-existing, non-load-bearing, disclosed, untouched.

## CLAIM MATRIX (load-bearing)
- FUN_006C66D0 = DIRECT_FIELD_GETTER of ArkModelManagerMain+0x68: CONFIRMED (byte-pinned; extent resolved; 3 callers rel32-verified).
- Producer chain (lazy): ctor NULL [+0x68] -> trigger FUN_006C8B20 (guard [+0x68]==NULL) -> FUN_006C6F60 (validation +0x70; empty-string-key lookups 0x00A7957B; A = FUN_007CE1E0 getter-A prior canon {0x66=MODEL,A}; instance = FUN_006C9700 pump -> [manager+0x6C]) -> writer FUN_006C6780 [manager+0x68]=[instance+4] with smart-pointer refcount protocol (inc/dec, zero-destroy slot 1; NiObject-family protocol) + child used as named-lookup root ('ArkTexture' 0x00A859F8, 'ArkAnimation' 0x00A8547C, FUN_007B6C30, conditional): CONFIRMED as recorded chain facts.
- CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED (NOT CONFIRMED — honest: GAP-1 [instance+4] identity UNRESOLVED (FUN_006C9700 unopened; prior-canon ArkModelResourceInstanceRef map potentially inconsistent); GAP-2 alternative producer FUN_006C8BB0 NOT_CHECKED).
- MODEL_ROOT_RELATION = UNKNOWN (no clone operation observed; raw-vs-wrapper-vs-actor unresolved at [instance+4]); WRAPPER_DEPTH = 2.
- CHILD_VISUAL_ROLE = UNRESOLVED (no positive §6 proof of principal visual role; attachment alone insufficient; VFX/helper not excluded).
- CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED (caller-side window clean per own decode; 4 intervening callee bodies unopened — budget exhausted; ABI = support not proof).
- EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (carried, scoped ACLD+0x18; zero CMO<->ACLD transfer); JOIN_OPERATION = STRONGLY_SUPPORTED (ceiling; FUN_007BF470 NOT opened).
- CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND (CHILD_EVIDENCE_COMPLETE = FALSE; algebra literal).

## SUPERVISORY NOTE (systemic pattern, recorded)
THIRD consecutive budget-class execution breach in this chain (DA2: function #7 vs max 6; J2: edges >=22 vs max 6; THIS RUN: edges 24 vs max 8). In each case the executor disclosed honestly post-hoc and the census was complete, but the contract's STOP-BEFORE-EXCEEDING rule failed in execution every time. Byte evidence is NOT falsified by process non-compliance; the historical FAILs stand. Future contracts should require a running budget counter mechanism checked before each new analysis act (recommendation only — no tooling change performed or authorized here).

## COVERAGE / NOT_CHECKED
Internal QC FULL_READ 28/28 package files + contract 375 lines; own measurements 56 pins + 23 rel32 + 20 chain pins + 3 RTTI walks + 6 extents + join window + census CSV + .NET manifest re-hash + 76-file blob-identity. PE-MASTER: identities, own byte re-pins (getter/chain/join-window/RTTI), census parse 69/24, manifest re-hash, adjudications, git state. NOT_CHECKED: bodies of FUN_006C9700 (instance creation chain), FUN_006C8BB0 (alternative producer), 4 intervening callees (FUN_006C0F90/006C10B0/0050A1E0/005246E0), FUN_007B6C30/007BF900/007BF630, manager slots 0x006C0FD0/0x006C19B0, FUN_006C6780 continuation beyond 0x006C6848 (extent UNRESOLVED), all §9-listed NEIGH bodies, runtime (STATIC-ONLY), payloads, private executor scratch, independent Desktop post-audit of THIS run = NOT_PERFORMED (pending on the published SHA).

NEXT_EXPERIMENT_AUTHORIZED = NO (recorded next inputs, designed-not-executed: GAP-1 [instance+4] identity via FUN_006C9700 chain + prior-canon ArkModelResourceInstanceRef reconciliation; GAP-2 alternative producer; the 4 preservation bodies). WORLD_XYZ_RECOVERED = NO; STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED; HISTORICAL_INSTANCE_DATA_RECOVERED = NO; RUNTIME_JOIN_OBSERVED = NO; REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED. HARD_STOP = YES.
