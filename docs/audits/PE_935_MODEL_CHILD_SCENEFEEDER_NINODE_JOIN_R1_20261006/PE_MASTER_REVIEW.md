# PE_MASTER_REVIEW — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006
REVIEWED BY: PE-MASTER (supervisory controller; independent audit over executor + fresh internal QC + own byte re-pins)
DATE: 2026-10-06
BASE_SHA = 24f45e0108b922c26ff584fee9ef7749de0390b6
RUN_CLASS = BOUNDED_STATIC_RE; RUN_TYPE = MODEL_RESOURCE_TO_EXACT_SCENEFEEDER_NINODE_JOIN

## VERDICT
RUN_VERDICT = MASTER_ACCEPTED (advisory)
AUTHORITY_STATUS = ADVISORY_PRE_QUALIFICATION (PROVISIONAL_UNTIL_QUALIFIED; Q1 absent)
CANONICAL_GATE_EFFECT = NONE
SCIENCE OUTCOME = PARENT_FOUND_CHILD_UNRESOLVED (honest partial; contract question NOT closed)
INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED (status algebra does not average up: A=UNRESOLVED, B=CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 [scoped], C=STRONGLY_SUPPORTED, D=UNRESOLVED)
RUNTIME_JOIN_OBSERVED = NO (static-only run)
SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC (SEPARATE status; full pins verified by internal QC; does NOT promote the join)

## INDEPENDENTLY VERIFIED BY PE-MASTER (own byte reads from pinned EXE)
- Join site @0x0050A3E9..0x0050A3F7: `8B 4E 30 / 8B 01 / 8B 90 A4 00 00 00 / 6A 00 / 57 / FF D2` — receiver [ESI+0x30] (ESI=SF), vtable slot 41 [0x00A8CCF4+0xA4] = 0x007B5810 (EXACT match).
- [SF+0x20] install `89 7E 20` @0x0050A3AC; child getter call @0x0050A3AF → 0x006C66D0 (rel32 recomputed); accessor `8D 41 18 C3` @0x008BD720; scheduler imm `BB 20 D7 8B 00` @0x006C3FB0; SF vtable store `C7 45 00 58 D4 A7 00` @0x00509366 (vtable 0x00A7D458) — ALL MATCH.
- Repaired record files re-hashed: all 5 SHAs match executor claims; F-QC-1 CH2a caption corrected; F-QC-3 wording fix present ("fully decoded" → window vs true extent 0x0050A310..0x0050A45C); the remaining "fully decoded" occurrence is FUN_00509850 (extent == ledger extent, QC-confirmed accurate).

## INTERNAL QC (fresh context, LOAD_BEARING depth)
QC_VERDICT = QC_PASS_WITH_FINDINGS -> F-QC-1..4 (P2x3+P3) CORRECTED_AND_REVALIDATED by records-repair (5 paths, UTF-8 49/49, science outcome unchanged); F-QC-5/6 (P3) DISCLOSED_NO_ACTION. 61/61 own-engine re-pins PASS (own PE mapper + own x86 decoder, zero executor tooling): join-site bytes, install/getter/transform/accessor/vtable pins, FUN_007B5810 AttachChild fingerprint F1/F2/F4/F5 (F3 = direct call, body undecoded — STRONGLY_SUPPORTED never promoted), transform application gates (SF+0x24..0x2C) and translate x100 ([0x00A7A618]=100.0), 23/23 raw windows byte-identical. Budget census: 8/8 functions, 6/6 edges, 4/4 candidates, 2/2 wrappers, 1/1 oracle — exhausted NOT exceeded, ZERO after-the-fact exceptions. Qualification gate: reads proof-chain structure (not just 4 status strings); baseline PASS; CTRL-A/B/C each FAIL on its own predicate; real CAND-4 FAILs exactly on P_CHILD+P_VISUAL despite 5/5 bytes; QC's own falsifiers confirm the gate's failure barrier is exactly A/D (mutating +A+D makes the real chain pass — proving the predicates are live). PRE_REGISTERED_ANCHORS timestamped before decoding. Binding HANDOFF_NOTES constraints honored (no FUN_006CB020 visual-child anchor; no CB3C0 promotion by label; attach identified by vtable slot not name; VFX separation; transform kept separate from join). Ledger byte-identical with generator (no hand edits).

## CLAIM MATRIX (load-bearing)
- Join site on the ACLD (ArkClientLocalDynamic) path: SF-install-visual FUN_0050A310 calls NiNode vtable slot 41 (FUN_007B5810, AttachChild-equivalent) with receiver EXACTLY [SF+0x30] and child argument from FUN_006C66D0(ArkModelManagerMain @ [SF+0x20]) -> CONFIRMED (byte-pinned; scoped to the examined ACLD path instance).
- EXACT_PARENT (B): CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 in the ACLD-path scope — same SF class (vtable 0x00A7D458) and same creation chain as the prior SF island, but a DIFFERENT holder instance than CMO+0xC0; on the examined CMO path NO model-child join was found.
- JOIN_OPERATION (C): STRONGLY_SUPPORTED (fingerprint F1/F2/F4/F5 byte-verified vs pinned EXE; F3 call-through body undecoded; PCG engine-generation not era-exact with the Gb12 oracle — same status ceiling as the slot-17 canon).
- CHILD_PROVENANCE (A): UNRESOLVED — child = FUN_006C66D0(manager) getter; manager provenance and model/resource origin NOT traced (budget boundary; next input recorded: FUN_006C66D0 + manager provenance chain).
- VISUAL_ROLE (D): UNRESOLVED.
- Candidates: CAND-1 REJECTED (no child arg, no children-array write), CAND-2 REJECTED (transform != binding), CAND-3 NON_MODEL metadata, CAND-4 EXAMINED_UNRESOLVED (best; JOIN_SITE_VA 0x0050A3F7).
- Resource side: {0x66,A} emission + FUN_006C3640 entry @0x006C3FB0 re-pin MATCH; FUN_008BD720 = 4-byte accessor (NOT a completion handler); completion chain NOT followed (budget).
- [SF+0x20] external-writer census: 0 hits (true negative — the writer lives inside the SF class).

## DISCLOSED RESIDUE
F-QC-5 (three raw windows start mid-instruction — decoding artifacts, bytes correct), F-QC-6 (EDI child-preservation across 4 undecoded callees rests on calling convention; the parent ECX chain is fully byte-pinned). FINAL_EXTRADATA_STORAGE = NOT_CHECKED (FUN_007B68B0 remained DEFERRED_LEAD; its declared dependency was never triggered).

## COVERAGE / NOT_CHECKED
Internal QC FULL_READ 32/32 phase-1 package files + contract + HANDOFF_NOTES; PE-MASTER: preflight identities, own byte re-pins of the join-site and anchor pins, repair-file hashes, git state. NOT_CHECKED: FUN_006C66D0/FUN_007BF470/FUN_007B5A00/manager-family bodies, completion chain, ExtraData readback, all runtime behavior (STATIC-ONLY), payloads, the three private research report contents (hash-pinned only), external Desktop post-audit = NOT_PERFORMED (pending on the published SHA).

WORLD_XYZ_RECOVERED = NO; HISTORICAL_INSTANCE_DATA_RECOVERED = NO; STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED.
NEXT_EXPERIMENT_AUTHORIZED = NO (recorded next input, designed-not-executed: FUN_006C66D0 child provenance + manager chain). HARD_STOP = YES.
