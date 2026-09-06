# HANDOFF — PE_M1_935_BINDING_CHAIN_REVALIDATION_R1 (era PCG_9_3_5)

- **RUN_ID**: PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021
- **RUN_STATUS**: COMPLETED (6/6 gates PASS; no HARD STOP)
- **HARD_STOP_REASON**: NONE
- **FINAL_REPORT_PATH**: docs/audits/PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021/06_REPORT/00_FINAL_REPORT.md
- **PRIMARY_EVIDENCE_PATHS**:
  - docs/audits/PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021/01_RAW/ARKTEXTURE_ID_TABLE.csv (24,508 rows, full id census)
  - docs/audits/PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021/01_RAW/DANGLING_LIST.csv + DANGLING_CLASSIFICATION.json (34 dangling, 15 unique ids, classes + 2003 comparison)
  - docs/audits/PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021/01_RAW/EDGE_COUNTS.json + STATIC_EDGES.csv + CONTROLLER_EDGES.csv + EFFECT_EDGES.csv
  - docs/audits/PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021/01_RAW/NEGATIVE_CONTROLS.json
  - docs/audits/PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021/01_RAW/CENSUS_RECONCILIATION.json (ITER-32 exact reconciliation, 40/40 slot join)
  - docs/audits/PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021/01_RAW/INDEX_VALIDATION.json (both BNT2 indexes, 0 anomalies)
  - docs/audits/PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021/05_ANALYSIS/ (controller-chain investigation)
  - docs/audits/PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021/STAGE_ACCEPTANCE_GATES.csv

## P0 ANSWER (one paragraph)

YES — the mesh → NiArkTextureExtraData → bnt2_id → Textures.bnt binding chain resolves on the PCG 9.3.5 corpus at the same closure level as the canon 2003 chain: **24,474/24,508 = 99.8613%** (2003: 23,455/23,488 = 99.8595%), census exact-reconciled with ITER-32 (24,508 = v10 19,637 + v4 4,871; 40/40 slot join), both BNT2 indexes byte-exact with 0 anomalies, static edges 21,390 with two-traversal Jaccard 1.000000, negative controls collapsed (NC1 0/10,000 = 0.0000%; NC4 shift/BE all 0.0000%). Dangling = **34 = 18 SuperSpray particle slots (the SAME 3 ids × 6 in the same 3 files as 2003) + 15 unshipped individual slots (the SAME ids as the 2003 fifteen) + 1 NEW 9.3.5 missing id (592148, 592146.nif Mesh01_0_BASE)**; 15 unique missing ids = the 2003 fourteen (all still missing) + 1 new; `only_in_2003 = []`.

## FINAL HANDOFF BLOCK

```
COMMIT_SHA      = (see commit of docs/audits/PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021 — path-limited; reported in chat handoff)
PUSH_STATUS     = (pushed to origin/master; origin/master == HEAD verified post-push)
PINS            = Models.bnt  c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0 (contract pin, match)
                  Textures.bnt 61acd13b140e130647eee24c1e2669d3734990b76cf74897ddd3ba0f4ea61393 (FULL SHA256 measured fresh; contract prefix 61ACD13B OK)
                  R61 frozen parser 10/10 (SHA256_SOURCE.json, verified in-driver before any parse)
RESOLUTION      = 24474/24508 = 99.8613% (2003 canon: 99.8595%)
                  dangling 34 = 18 SuperSpray (3 ids x 6: 425247/425261/425271.nif) + 15 SAME-as-2003 unshipped + 1 NEW_935 (592148 in 592146.nif)
                  15 unique missing ids; 2003's 14 all still missing; only_in_2003=[]; only_in_935=[592148]
EDGES           = static 21390 (Jaccard 1.000000, two independent traversals; bnt2 resolved 21374/dangling 16)
                  controller 118 DIRECT canon-V2 (chain-inclusive 125 from 126 NiFlipController; 7 next_controller chains + 1 unreachable)
                  effect 1798 = 1772 attached + 26 orphan (1694 NiTextureEffect blocks)
                  negative controls: NC1 0/10000 = 0.0000% (~0); NC2 in-range 1.56% vs density 1.42%; NC4 shift+1/-1/BE = 0.0000%/0.0000%/0.0000%
GATES           = G1 PASS (pins) | G2 PASS (0 index anomalies, both containers) | G3 PASS (census == 24,508 exact, 40/40 slot join) | G4 PASS (99.8613% >= 99.5%, full dangling classified) | G5 PASS (Jaccard 1.0 >= 0.99, NC ~0) | G6 PASS (originals re-hashed == pins, zero payloads, path-limited commit + push)
RUN_STATUS      = COMPLETED
HARD_STOP_REASON = NONE
```

## NOT_CHECKED (honest)

2003 side not re-run (audited canon reference); Textures.bnt payloads not decoded (index names only); 2003 V2 controller traversal code not extant (both 9.3.5 controller counts reported under explicit semantics); 592148 payload unretrievable (absent from index); shader/VFS/other block families out of scope.
